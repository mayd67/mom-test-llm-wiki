from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

EXCLUDED_TOP_LEVEL = {
    'template_constraints',
    '按物料中文名称分类',
}

SCENE_DIR_LABELS = [
    ('gearbox_machining_assembly', '单工厂机加装配'),
    ('gearbox_multi_factory', '多工厂协同'),
    ('gearbox_assembly', '单工厂总装检测'),
    ('fuel_pump_assembly', '单工厂装配'),
    ('transmission_shaft', '单工厂机加工'),
    ('aircraft_seat_economy_line', '经济舱产线'),
    ('automotive_engine', '专业版'),
    ('boeing_737_leap1b', ''),
    ('cnc_machine', ''),
    ('turbofan_engine', ''),
    ('turbojet_engine', ''),
]

SCENE_NAME_LABELS = [
    ('单工厂总装检测', '单工厂总装检测'),
    ('机加装配一体化', '单工厂机加装配'),
    ('多工厂协同', '多工厂协同'),
    ('单工厂装配', '单工厂装配'),
    ('单工厂机加工', '单工厂机加工'),
    ('经济舱线', '经济舱产线'),
    ('专业版', '专业版'),
]

GENERIC_PREFIXES = [
    '变速箱',
    '燃油泵',
    '传动轴',
    '汽车发动机',
    '航空座椅',
    '数控机床',
]

INVALID_CHARS = '<>:"/\\|?*'


@dataclass
class PackageInfo:
    source: Path
    relative_source: str
    group_name: str
    package_name: str
    seed_name: str
    product_family: str
    volume_profile: str
    scene_label: str
    deprecated: bool


def sanitize_name(text: str) -> str:
    cleaned = ''.join('、' if char in INVALID_CHARS else char for char in text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip().strip('.')
    return cleaned or '未命名'


def load_metadata(summary_file: Path) -> dict:
    payload = json.loads(summary_file.read_text(encoding='utf-8-sig'))
    for value in payload.values():
        if isinstance(value, dict) and any(key in value for key in ('product_model', 'product_family', 'name')):
            return value
    return {}


def build_group_name(metadata: dict) -> str:
    for key in ('product_model', 'product_family', 'name'):
        value = str(metadata.get(key, '')).strip()
        if not value:
            continue
        if key == 'name':
            value = re.sub(r'MOM种子$', '', value)
        return sanitize_name(value)
    return '未识别物料'


def infer_scene_label(dir_name: str, seed_name: str) -> str:
    for key, label in SCENE_DIR_LABELS:
        if key in dir_name:
            return label

    for key, label in SCENE_NAME_LABELS:
        if key in seed_name:
            return label

    fallback = re.sub(r'MOM种子$', '', seed_name).strip()
    for prefix in GENERIC_PREFIXES:
        if fallback.startswith(prefix):
            fallback = fallback[len(prefix):].strip()
            break
    return sanitize_name(fallback) if fallback else ''


def infer_suffix(dir_name: str) -> str:
    suffix_parts: list[str] = []
    if '_v2' in dir_name:
        suffix_parts.append('（第二版）')
    elif '_v3' in dir_name:
        suffix_parts.append('（第三版）')

    if '_fixed' in dir_name:
        suffix_parts.append('（修正版）')
    if '_ns31' in dir_name:
        suffix_parts.append('（命名空间31）')
    if '_ns42' in dir_name:
        suffix_parts.append('（命名空间42）')

    return ''.join(suffix_parts)


def build_package_name(dir_name: str, metadata: dict, deprecated: bool) -> tuple[str, str, str]:
    seed_name = str(metadata.get('name', '')).strip()
    volume_profile = str(metadata.get('volume_profile', '')).strip() or '标准版'
    scene_label = infer_scene_label(dir_name, seed_name)

    if scene_label and scene_label != volume_profile:
        package_name = f'{scene_label}-{volume_profile}'
    else:
        package_name = volume_profile

    if deprecated:
        package_name = f'历史废弃-{package_name}'

    package_name = f'{package_name}{infer_suffix(dir_name)}'
    return sanitize_name(package_name), volume_profile, scene_label


def collect_packages(output_root: Path) -> tuple[list[PackageInfo], list[str]]:
    packages: list[PackageInfo] = []
    skipped: list[str] = []

    for directory in sorted((path for path in output_root.iterdir() if path.is_dir()), key=lambda item: item.name):
        if directory.name in EXCLUDED_TOP_LEVEL:
            skipped.append(f'{directory.as_posix()}：模板约束或分类目录，未纳入生产数据分类')
            continue

        if directory.name == '_deprecated':
            for child in sorted((path for path in directory.iterdir() if path.is_dir()), key=lambda item: item.name):
                package = create_package_info(output_root, child, deprecated=True)
                if package is None:
                    skipped.append(f'{child.as_posix()}：缺少 种子概览.json 或 seed_summary.json，未纳入分类')
                    continue
                packages.append(package)
            continue

        package = create_package_info(output_root, directory, deprecated=False)
        if package is None:
            skipped.append(f'{directory.as_posix()}：缺少 种子概览.json 或 seed_summary.json，未纳入分类')
            continue
        packages.append(package)

    return packages, skipped


def create_package_info(output_root: Path, directory: Path, deprecated: bool) -> PackageInfo | None:
    summary_candidates = [directory / '种子概览.json', directory / 'seed_summary.json']
    summary_file = next((path for path in summary_candidates if path.exists()), None)
    if summary_file is None:
        return None

    metadata = load_metadata(summary_file)
    group_name = build_group_name(metadata)
    package_name, volume_profile, scene_label = build_package_name(directory.name, metadata, deprecated)
    seed_name = str(metadata.get('name', '')).strip() or '未命名种子'
    product_family = str(metadata.get('product_family', '')).strip()

    return PackageInfo(
        source=directory,
        relative_source=directory.as_posix(),
        group_name=group_name,
        package_name=package_name,
        seed_name=seed_name,
        product_family=product_family,
        volume_profile=volume_profile,
        scene_label=scene_label,
        deprecated=deprecated,
    )


def ensure_unique_package_names(packages: list[PackageInfo]) -> list[PackageInfo]:
    groups: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    normalized: list[PackageInfo] = []

    for package in sorted(packages, key=lambda item: (item.group_name, item.package_name, item.relative_source)):
        groups[package.group_name][package.package_name] += 1
        sequence = groups[package.group_name][package.package_name]
        if sequence == 1:
            normalized.append(package)
            continue

        unique_name = f'{package.package_name}（包{sequence}）'
        normalized.append(
            PackageInfo(
                source=package.source,
                relative_source=package.relative_source,
                group_name=package.group_name,
                package_name=unique_name,
                seed_name=package.seed_name,
                product_family=package.product_family,
                volume_profile=package.volume_profile,
                scene_label=package.scene_label,
                deprecated=package.deprecated,
            )
        )

    return normalized


def copy_packages(packages: list[PackageInfo], target_root: Path) -> None:
    for package in packages:
        group_dir = target_root / sanitize_name(package.group_name)
        package_dir = group_dir / sanitize_name(package.package_name)
        group_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            package.source,
            package_dir,
            ignore=shutil.ignore_patterns('~$*'),
        )

        legacy_summary = package_dir / 'seed_summary.json'
        chinese_summary = package_dir / '种子概览.json'
        if legacy_summary.exists() and not chinese_summary.exists():
            legacy_summary.rename(chinese_summary)


def write_summary_files(packages: list[PackageInfo], skipped: list[str], target_root: Path) -> None:
    packages_by_group: dict[str, list[PackageInfo]] = defaultdict(list)
    for package in packages:
        packages_by_group[package.group_name].append(package)

    summary_lines = [
        '按物料中文名称分类整理结果',
        f'生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        '',
        '说明：',
        '1. 本目录为中文分类副本，原始 output 目录未被改动。',
        '2. 复制后的包内已将 seed_summary.json 改名为 种子概览.json，便于中文查看。',
        '3. template_constraints 属于模板约束资料，不属于生产数据包，因此未纳入分类目录。',
        '',
        f'共整理 {len(packages)} 个生产数据包，归入 {len(packages_by_group)} 个物料分组。',
        '',
        '分类清单：',
    ]

    for index, group_name in enumerate(sorted(packages_by_group), start=1):
        summary_lines.append(f'{index}. {group_name}')
        for package in sorted(packages_by_group[group_name], key=lambda item: item.package_name):
            scene_text = package.scene_label or '通用场景'
            deprecated_text = '是' if package.deprecated else '否'
            summary_lines.append(
                f'   - {package.package_name} <- {package.relative_source} | 场景：{scene_text} | 容量：{package.volume_profile} | 历史废弃：{deprecated_text}'
            )
        summary_lines.append('')

    if skipped:
        summary_lines.extend(['未纳入分类：'])
        summary_lines.extend(f'- {item}' for item in skipped)
        summary_lines.append('')

    (target_root / '分类说明.txt').write_text('\n'.join(summary_lines), encoding='utf-8-sig')

    with (target_root / '分类清单.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['物料中文名称', '中文包名', '原始相对路径', '场景', '容量版本', '历史废弃', '种子名称', '产品族'])
        for package in sorted(packages, key=lambda item: (item.group_name, item.package_name, item.relative_source)):
            writer.writerow([
                package.group_name,
                package.package_name,
                package.relative_source,
                package.scene_label or '通用场景',
                package.volume_profile,
                '是' if package.deprecated else '否',
                package.seed_name,
                package.product_family,
            ])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='将 outputs/06_测试数据 下已生成的 MOM 数据包按物料中文名称分类整理。')
    parser.add_argument('--output-root', default='outputs/06_测试数据', help='原始测试数据输出根目录，默认 outputs/06_测试数据')
    parser.add_argument('--target-root', default='outputs/06_测试数据/按物料中文名称分类', help='中文分类目录，默认 outputs/06_测试数据/按物料中文名称分类')
    parser.add_argument('--clean', action='store_true', help='若目标目录已存在，则先删除后重建')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_root = Path(args.output_root)
    target_root = Path(args.target_root)

    if not output_root.exists():
        raise SystemExit(f'未找到 output 根目录：{output_root}')

    if target_root.exists():
        if not args.clean:
            raise SystemExit(f'目标目录已存在，请先删除或追加 --clean：{target_root}')
        shutil.rmtree(target_root)

    packages, skipped = collect_packages(output_root)
    normalized_packages = ensure_unique_package_names(packages)

    target_root.mkdir(parents=True, exist_ok=True)
    copy_packages(normalized_packages, target_root)
    write_summary_files(normalized_packages, skipped, target_root)

    print(f'已整理 {len(normalized_packages)} 个数据包到：{target_root.as_posix()}')


if __name__ == '__main__':
    main()
