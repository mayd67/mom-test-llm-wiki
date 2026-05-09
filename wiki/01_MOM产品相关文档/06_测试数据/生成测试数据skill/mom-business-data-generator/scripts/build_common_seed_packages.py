from __future__ import annotations

import argparse
import gc
import importlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from generate_seed_workbooks import (
    TEMPLATE_FILES,
    build_summary,
    default_output_root_for_template_dir,
    fill_workbook,
    resolve_template_dir,
    load_template_headers,
    load_template_list_validations,
    validate_list_values,
    validate_order_refs,
    validate_references,
    validate_route_refs,
    validate_storage_org_rules,
    validate_structure,
    validate_unique,
)

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass


@dataclass(frozen=True)
class ScenarioSpec:
    key: str
    label: str
    module_name: str
    output_parts: tuple[str, str]
    build_method: str = 'build'
    namespace: str | None = None
    volume_profile: str | None = None


def scenario_registry() -> dict[str, ScenarioSpec]:
    return {
        'bearing_machining_standard': ScenarioSpec(
            key='bearing_machining_standard',
            label='轴承单工厂机加工标准版',
            module_name='build_bearing_machining_seed',
            output_parts=('深沟球轴承外圈（6206）', '单工厂机加工-标准版'),
        ),
        'fuel_pump_assembly_standard': ScenarioSpec(
            key='fuel_pump_assembly_standard',
            label='燃油泵单工厂装配标准版',
            module_name='build_fuel_pump_assembly_seed',
            output_parts=('电动燃油泵总成（FP220）', '单工厂装配-标准版'),
        ),
        'bicycle_assembly_standard': ScenarioSpec(
            key='bicycle_assembly_standard',
            label='城市通勤自行车单工厂总装标准版',
            module_name='build_bicycle_assembly_seed',
            output_parts=('城市通勤自行车整车（CTB-26S）', '单工厂总装检测-标准版'),
        ),
        'gearbox_assembly_standard': ScenarioSpec(
            key='gearbox_assembly_standard',
            label='湿式双离合变速箱总装标准版',
            module_name='build_gearbox_assembly_seed',
            output_parts=('湿式双离合变速箱总成（DCT380）', '单工厂总装检测-标准版'),
            build_method='build_variant',
            namespace='GBA20S01',
            volume_profile='标准版',
        ),
        'gearbox_machining_assembly_standard': ScenarioSpec(
            key='gearbox_machining_assembly_standard',
            label='自动变速箱机加装配标准版',
            module_name='build_gearbox_machining_assembly_seed',
            output_parts=('自动变速箱（8AT450）', '单工厂机加装配-标准版'),
            build_method='build_variant',
            namespace='GBM20S01',
            volume_profile='标准版',
        ),
        'gearbox_multi_factory_standard': ScenarioSpec(
            key='gearbox_multi_factory_standard',
            label='自动变速箱多工厂协同标准版',
            module_name='build_gearbox_multi_factory_seed',
            output_parts=('自动变速箱总成（8AT480）', '多工厂协同-标准版'),
            build_method='build_variant',
            namespace='GBX20S01',
            volume_profile='标准版',
        ),
        'mom_promo_video_standard': ScenarioSpec(
            key='mom_promo_video_standard',
            label='MOM宣传视频综合演示标准版',
            module_name='build_mom_promo_video_seed',
            output_parts=('自动变速箱总成（8AT480）', 'MOM宣传视频综合演示-标准版'),
            build_method='build_variant',
            namespace='MPV20S01',
            volume_profile='标准版',
        ),
        'blade_project_collaboration_standard': ScenarioSpec(
            key='blade_project_collaboration_standard',
            label='高压涡轮叶片项目部协同标准版',
            module_name='build_blade_project_collaboration_seed',
            output_parts=('高压涡轮叶片（BL-1001）', '多工厂协同-项目部一级工艺版'),
        ),
        'aeroengine_fuel_system_multi_factory_standard': ScenarioSpec(
            key='aeroengine_fuel_system_multi_factory_standard',
            label='航发燃油系统总成多工厂协同标准版',
            module_name='build_aeroengine_fuel_system_seed',
            output_parts=('航发燃油系统总成（AFS-900）', '多工厂协同-生产部一级工艺版'),
        ),
    }


def _resolve_paths(template_dir: Path | None = None, output_root: Path | None = None) -> tuple[Path, Path]:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    resolved_template_dir = resolve_template_dir(template_dir, skill_dir)
    resolved_output_root = output_root or default_output_root_for_template_dir(resolved_template_dir)
    return resolved_template_dir.resolve(), resolved_output_root.resolve()


def _load_module(spec: ScenarioSpec):
    return importlib.import_module(spec.module_name)


def _build_seed(spec: ScenarioSpec) -> tuple[object, dict]:
    module = _load_module(spec)
    if spec.build_method == 'build_variant':
        seed = module.build_variant(spec.namespace, spec.volume_profile)
    else:
        seed = module.build()
    return module, seed


def _validate_seed(seed: dict, template_dir: Path) -> tuple[list[str], list[str]]:
    headers = load_template_headers(template_dir)
    template_validations = load_template_list_validations(template_dir)
    structure_errors, warnings = validate_structure(seed, headers)
    errors = structure_errors
    errors += validate_list_values(seed, template_validations)
    errors += validate_unique(seed)
    errors += validate_references(seed)
    errors += validate_storage_org_rules(seed)
    errors += validate_route_refs(seed)
    errors += validate_order_refs(seed)
    return warnings, errors


def _write_seed_asset(module, seed: dict) -> Path:
    asset_path = getattr(module, 'ASSET_PATH', None)
    if asset_path is None:
        asset_path = Path(__file__).resolve().parent.parent / 'assets' / f'{module.__name__}.json'
    asset_path = Path(asset_path)
    asset_path.parent.mkdir(parents=True, exist_ok=True)
    asset_path.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding='utf-8-sig')
    return asset_path


def _export_seed(seed: dict, template_dir: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    for workbook_name in TEMPLATE_FILES:
        fill_workbook(template_dir / workbook_name, output_dir / workbook_name, seed.get('workbooks', {}).get(workbook_name, {}))
    legacy_summary = output_dir / 'seed_summary.json'
    if legacy_summary.exists():
        legacy_summary.unlink()
    summary_path = output_dir / '种子概览.json'
    summary_path.write_text(json.dumps(build_summary(seed), ensure_ascii=False, indent=2), encoding='utf-8')
    return summary_path


def resolve_scenarios(scenario_keys: list[str] | None = None) -> list[ScenarioSpec]:
    registry = scenario_registry()
    if not scenario_keys:
        return list(registry.values())
    missing = [key for key in scenario_keys if key not in registry]
    if missing:
        raise KeyError(f'未注册的场景: {", ".join(missing)}')
    return [registry[key] for key in scenario_keys]


def build_packages(
    scenario_keys: list[str] | None = None,
    template_dir: Path | None = None,
    output_root: Path | None = None,
    validate_only: bool = False,
) -> list[dict]:
    resolved_template_dir, resolved_output_root = _resolve_paths(template_dir, output_root)
    results: list[dict] = []
    for spec in resolve_scenarios(scenario_keys):
        module, seed = _build_seed(spec)
        warnings, errors = _validate_seed(seed, resolved_template_dir)
        if errors:
            raise ValueError(f'{spec.key} 校验失败: ' + '; '.join(errors))
        asset_path = _write_seed_asset(module, seed)
        output_dir = resolved_output_root.joinpath(*spec.output_parts)
        summary_path = None
        if not validate_only:
            summary_path = _export_seed(seed, resolved_template_dir, output_dir)
        results.append(
            {
                'scenario_key': spec.key,
                'label': spec.label,
                'asset_path': asset_path,
                'output_dir': output_dir,
                'summary_path': summary_path,
                'warnings': warnings,
                'metadata': seed.get('metadata', {}),
            }
        )
        del seed
        gc.collect()
    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='一键批量生成常用 MOM 场景种子与中文 Excel 数据包。')
    parser.add_argument('--scenario', action='append', dest='scenarios', help='指定要生成的场景 key，可重复传入；不传则生成全部常用场景。')
    parser.add_argument('--template-dir', type=Path, default=None, help='模板目录；可直接传 templates 目录、生成器目录或工作区根目录，默认自动优先查找内置 templates。')
    parser.add_argument('--output-root', type=Path, default=None, help='输出根目录，默认按模板目录自动推断；内置 templates 场景下输出到工作区 output。')
    parser.add_argument('--validate-only', action='store_true', help='仅校验和写种子，不导出 Excel 数据包。')
    parser.add_argument('--list', action='store_true', help='仅列出已注册的批量场景。')
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    registry = scenario_registry()
    if args.list:
        print(json.dumps({key: {'label': spec.label, 'output_parts': spec.output_parts} for key, spec in registry.items()}, ensure_ascii=False, indent=2))
        return 0

    try:
        results = build_packages(
            scenario_keys=args.scenarios,
            template_dir=args.template_dir,
            output_root=args.output_root,
            validate_only=args.validate_only,
        )
    except (KeyError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps([
        {
            'scenario_key': item['scenario_key'],
            'label': item['label'],
            'asset_path': str(item['asset_path']),
            'output_dir': str(item['output_dir']),
            'summary_path': str(item['summary_path']) if item['summary_path'] else '',
        }
        for item in results
    ], ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())



