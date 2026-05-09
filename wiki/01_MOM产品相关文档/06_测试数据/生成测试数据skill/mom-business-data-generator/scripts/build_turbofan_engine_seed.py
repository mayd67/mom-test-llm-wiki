from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import build_b737_leap1b_seed as leap_seed
from production_order_seed import apply_production_orders

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

NAMESPACE = 'TFAN9001'
DEFAULT_VOLUME_PROFILE = '标准版'
ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'turbofan_engine_seed.json'
VARIANT_SPECS = [
    ('turbofan_engine_seed.json', NAMESPACE, DEFAULT_VOLUME_PROFILE),
]


def _replace_strings(value, replacements: list[tuple[str, str]]):
    if isinstance(value, dict):
        return {key: _replace_strings(subvalue, replacements) for key, subvalue in value.items()}
    if isinstance(value, list):
        return [_replace_strings(item, replacements) for item in value]
    if isinstance(value, str):
        result = value
        for old, new in replacements:
            result = result.replace(old, new)
        return result
    return value


def _genericize(seed: dict, namespace: str, volume_profile: str) -> dict:
    replacements = [
        ('Boeing 737 MAX', '通用窄体客机'),
        ('CFM LEAP-1B', '通用高涵道比涡扇发动机'),
        ('LEAP-1B', '高涵道比涡扇'),
        ('LEAP1B', 'TFAN'),
        ('737发动机事业部', '民航涡扇事业部'),
        ('LEAP-1B制造中心', '涡扇发动机制造中心'),
    ]
    generic = _replace_strings(copy.deepcopy(seed), replacements)
    metadata = generic.setdefault('metadata', {})
    metadata.update({
        'name': '涡扇发动机MOM种子',
        'aircraft_family': '通用窄体客机',
        'engine_model': '通用高涵道比涡扇发动机',
        'description': '基于公开民航涡扇制造逻辑构建的典型涡扇发动机MOM主数据种子。',
        'public_fact_note': '采用公开涡扇制造链条作为拟真基线，体现风扇、压气机、燃烧室、涡轮、附件、总装和试车放行等核心环节。',
        'namespace': namespace,
        'volume_profile': volume_profile,
    })
    for row in generic.get('workbooks', {}).get('系统配置_模板.xlsx', {}).get('行政组织', []):
        if row.get('简称') == '737事业部':
            row['简称'] = '涡扇事业部'
        if row.get('简称') == 'LEAP中心':
            row['简称'] = '涡扇中心'
    for row in generic.get('workbooks', {}).get('系统配置_模板.xlsx', {}).get('业务组织', []):
        if row.get('简称') == '737事业部':
            row['简称'] = '涡扇事业部'
        if row.get('简称') == 'LEAP中心':
            row['简称'] = '涡扇中心'
    for row in generic.get('workbooks', {}).get('产品与工艺_模板.xlsx', {}).get('物料', []):
        if str(row.get('*编码', '')).endswith('-TFAN-ENG'):
            row['*名称'] = '高涵道比涡扇发动机总成'
    return generic


def summarize(seed_data: dict) -> dict:
    return {
        'metadata': seed_data.get('metadata', {}),
        'counts': {
            workbook: {sheet: len(rows) for sheet, rows in sheets.items()}
            for workbook, sheets in seed_data.get('workbooks', {}).items()
        },
    }


def build_variant(namespace: str = NAMESPACE, volume_profile: str = DEFAULT_VOLUME_PROFILE) -> dict:
    base_seed = leap_seed.build_variant(namespace=namespace, volume_profile=volume_profile)
    seed = _genericize(base_seed, namespace, volume_profile)
    apply_production_orders(seed, 'turbofan_engine', namespace)
    return seed


def build() -> dict:
    return build_variant(NAMESPACE, DEFAULT_VOLUME_PROFILE)


def main() -> None:
    ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    for asset_name, namespace, volume_profile in VARIANT_SPECS:
        seed = build_variant(namespace, volume_profile)
        asset_path = ASSET_PATH.parent / asset_name
        asset_path.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding='utf-8-sig')
        print(json.dumps(summarize(seed), ensure_ascii=False, indent=2))
        print(f'已写入种子文件: {asset_path}')


if __name__ == '__main__':
    main()
