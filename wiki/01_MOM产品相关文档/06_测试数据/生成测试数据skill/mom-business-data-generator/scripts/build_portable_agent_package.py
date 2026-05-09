from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path

IGNORE_PATTERNS = shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo', '~$*')
TEXT_SUFFIXES = {'.md', '.txt'}


def normalize_text_files(root: Path) -> None:
    for path in root.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding='utf-8-sig')
        path.write_text(text, encoding='utf-8-sig')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='打包跨 Agent 兼容版 MOM 数据生成器。')
    parser.add_argument('--source-dir', type=Path, default=None, help='源目录，默认当前脚本上级目录。')
    parser.add_argument('--output-root', type=Path, default=None, help='输出根目录，默认工作区 delivery_packages。')
    parser.add_argument('--include-output', action='store_true', help='同时打包工作区 output 目录。')
    parser.add_argument('--zip', action='store_true', help='额外生成 zip 压缩包。')
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    source_dir = (args.source_dir or script_dir.parent).resolve()
    workspace_root = source_dir.parent
    output_root = (args.output_root or workspace_root / 'delivery_packages').resolve()
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    package_root = output_root / f'mom_data_generator_multi_agent_share_{timestamp}'
    skill_target = package_root / source_dir.name

    if package_root.exists():
        shutil.rmtree(package_root)
    package_root.mkdir(parents=True, exist_ok=True)

    shutil.copytree(source_dir, skill_target, ignore=IGNORE_PATTERNS)
    normalize_text_files(skill_target)

    if args.include_output:
        output_dir = workspace_root / 'output'
        if output_dir.exists():
            shutil.copytree(output_dir, package_root / 'output', ignore=IGNORE_PATTERNS)

    (package_root / '打包说明.txt').write_text(
        '\n'.join([
            '这是 MOM 数据生成器的跨 Agent 兼容共享包。',
            '建议先看 mom-template-seed-generator/START_HERE.md。',
            '如工具不支持自动读取指令文件，请打开 PROMPT_TEMPLATE.md 并复制其中提示词。',
            '安装依赖命令：pip install -r mom-template-seed-generator/requirements.txt',
            '列出场景命令：python mom-template-seed-generator/scripts/build_common_seed_packages.py --list',
        ]),
        encoding='utf-8-sig',
    )

    print(f'已生成目录：{package_root}')
    if args.zip:
        zip_path = shutil.make_archive(str(package_root), 'zip', root_dir=package_root.parent, base_dir=package_root.name)
        print(f'已生成压缩包：{zip_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
