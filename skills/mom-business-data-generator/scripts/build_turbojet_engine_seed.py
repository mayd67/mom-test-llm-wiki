from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import build_turbofan_engine_seed as turbofan_seed
from production_order_seed import apply_production_orders

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

WB_SYSTEM = '系统配置_模板.xlsx'
WB_FACTORY = '工厂资源_模板.xlsx'
WB_PRODUCT = '产品与工艺_模板.xlsx'
WB_ORDER = '生产订单_模板.xlsx'

SH_ADMIN = '行政组织'
SH_BIZ = '业务组织'
SH_USER = '用户'
SH_EQ = '设备'
SH_EQ_USER = '设备与用户的关系实体类'
SH_TOOL = '工装工具'
SH_WC = '工作中心'
SH_WC_USER = '工作中心与用户关系'
SH_WC_EQ = '工作中心与设备的关系'
SH_WH = '库房'
SH_LOC = '库位'
SH_PLIB = '工序库'
SH_MAT = '物料'
SH_MBOM = 'MBOM'
SH_MBOM_NODE = 'MBOM节点'
SH_ROUTE = '工艺路线'
SH_OP = '工艺路线工序'
SH_SEQ = '工艺路线工序序列'
SH_OPMAT = '工艺路线工序物料'
SH_STEP = '工艺路线工步'

NAMESPACE = 'TJET9001'
DEFAULT_VOLUME_PROFILE = '标准版'
ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'turbojet_engine_seed.json'
VARIANT_SPECS = [
    ('turbojet_engine_seed.json', NAMESPACE, DEFAULT_VOLUME_PROFILE),
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


def _text_has_fan_chain(*parts: str) -> bool:
    text = ' '.join(str(part or '') for part in parts)
    return any(token in text for token in ('FAN', '风扇', '复材', 'AFP', 'RTM', 'AUTOCLAVE'))


def _rows(seed: dict, workbook: str, sheet: str) -> list[dict]:
    return seed['workbooks'][workbook][sheet]


def _strip_fan_chain(seed: dict) -> dict:
    jet = copy.deepcopy(seed)

    admin_rows = _rows(jet, WB_SYSTEM, SH_ADMIN)
    initial_remove_admin = {
        str(row.get('*编码', '')).strip()
        for row in admin_rows
        if _text_has_fan_chain(row.get('*编码', ''), row.get('*名称', ''), row.get('简称', ''))
    }
    remove_admin_codes = set(initial_remove_admin)
    changed = True
    while changed:
        changed = False
        for row in admin_rows:
            code = str(row.get('*编码', '')).strip()
            parent = str(row.get('*父组织编码', '')).strip()
            if parent in remove_admin_codes and code not in remove_admin_codes:
                remove_admin_codes.add(code)
                changed = True
    _rows(jet, WB_SYSTEM, SH_ADMIN)[:] = [
        row for row in admin_rows if str(row.get('*编码', '')).strip() not in remove_admin_codes
    ]

    biz_rows = _rows(jet, WB_SYSTEM, SH_BIZ)
    initial_remove = {
        str(row.get('*编码', '')).strip()
        for row in biz_rows
        if _text_has_fan_chain(row.get('*编码', ''), row.get('*名称', ''))
    }
    remove_biz_codes = set(initial_remove)
    changed = True
    while changed:
        changed = False
        for row in biz_rows:
            code = str(row.get('*编码', '')).strip()
            parent = str(row.get('*父组织编码', '')).strip()
            if parent in remove_biz_codes and code not in remove_biz_codes:
                remove_biz_codes.add(code)
                changed = True

    _rows(jet, WB_SYSTEM, SH_BIZ)[:] = [
        row for row in biz_rows if str(row.get('*编码', '')).strip() not in remove_biz_codes
    ]
    _rows(jet, WB_SYSTEM, SH_USER)[:] = [
        row for row in _rows(jet, WB_SYSTEM, SH_USER)
        if str(row.get('业务组织编码', '')).strip() not in remove_biz_codes
    ]
    keep_user_codes = {str(row.get('*编号', '')).strip() for row in _rows(jet, WB_SYSTEM, SH_USER)}

    _rows(jet, WB_FACTORY, SH_EQ)[:] = [
        row for row in _rows(jet, WB_FACTORY, SH_EQ)
        if str(row.get('*工厂组织', '')).strip() not in remove_biz_codes
        and not _text_has_fan_chain(row.get('*编码', ''), row.get('*名称', ''))
    ]
    _rows(jet, WB_FACTORY, SH_TOOL)[:] = [
        row for row in _rows(jet, WB_FACTORY, SH_TOOL)
        if not _text_has_fan_chain(row.get('*编码', ''), row.get('*名称', ''), row.get('图号', ''))
    ]
    keep_eq_codes = {str(row.get('*编码', '')).strip() for row in _rows(jet, WB_FACTORY, SH_EQ)}

    _rows(jet, WB_FACTORY, SH_WC)[:] = [
        row for row in _rows(jet, WB_FACTORY, SH_WC)
        if str(row.get('*工厂组织', '')).strip() not in remove_biz_codes
        and not _text_has_fan_chain(row.get('*编码', ''), row.get('*名称', ''))
    ]
    keep_wc_codes = {str(row.get('*编码', '')).strip() for row in _rows(jet, WB_FACTORY, SH_WC)}

    _rows(jet, WB_FACTORY, SH_EQ_USER)[:] = [
        row for row in _rows(jet, WB_FACTORY, SH_EQ_USER)
        if str(row.get('*设备编码', '')).strip() in keep_eq_codes and str(row.get('*用户', '')).strip() in keep_user_codes
    ]
    _rows(jet, WB_FACTORY, SH_WC_USER)[:] = [
        row for row in _rows(jet, WB_FACTORY, SH_WC_USER)
        if str(row.get('*工作中心编码', '')).strip() in keep_wc_codes and str(row.get('*用户', '')).strip() in keep_user_codes
    ]
    _rows(jet, WB_FACTORY, SH_WC_EQ)[:] = [
        row for row in _rows(jet, WB_FACTORY, SH_WC_EQ)
        if str(row.get('*工作中心编码', '')).strip() in keep_wc_codes and str(row.get('*设备编码', '')).strip() in keep_eq_codes
    ]
    _rows(jet, WB_FACTORY, SH_WH)[:] = [
        row for row in _rows(jet, WB_FACTORY, SH_WH)
        if str(row.get('*工厂组织', '')).strip() not in remove_biz_codes
    ]
    keep_wh_codes = {str(row.get('*编码', '')).strip() for row in _rows(jet, WB_FACTORY, SH_WH)}
    _rows(jet, WB_FACTORY, SH_LOC)[:] = [
        row for row in _rows(jet, WB_FACTORY, SH_LOC)
        if str(row.get('*工厂组织', '')).strip() not in remove_biz_codes and str(row.get('*库房编码', '')).strip() in keep_wh_codes
    ]
    _rows(jet, WB_FACTORY, SH_PLIB)[:] = [
        row for row in _rows(jet, WB_FACTORY, SH_PLIB)
        if str(row.get('*工作中心编码', '')).strip() in keep_wc_codes
        and not _text_has_fan_chain(row.get('*编码', ''), row.get('*名称', ''))
    ]

    route_rows = _rows(jet, WB_PRODUCT, SH_ROUTE)
    remove_route_codes = {
        str(row.get('*编码', '')).strip()
        for row in route_rows
        if str(row.get('*工厂组织', '')).strip() in remove_biz_codes
        or _text_has_fan_chain(row.get('*编码', ''), row.get('*名称', ''))
    }
    _rows(jet, WB_PRODUCT, SH_ROUTE)[:] = [
        row for row in route_rows if str(row.get('*编码', '')).strip() not in remove_route_codes
    ]
    keep_route_codes = {str(row.get('*编码', '')).strip() for row in _rows(jet, WB_PRODUCT, SH_ROUTE)}

    for sheet in (SH_OP, SH_SEQ, SH_OPMAT, SH_STEP):
        _rows(jet, WB_PRODUCT, sheet)[:] = [
            row for row in _rows(jet, WB_PRODUCT, sheet)
            if str(row.get('*工艺路线编码', '')).strip() in keep_route_codes
        ]

    _rows(jet, WB_PRODUCT, SH_MBOM_NODE)[:] = [
        row for row in _rows(jet, WB_PRODUCT, SH_MBOM_NODE)
        if not _text_has_fan_chain(row.get('*物料编码', ''), row.get('物料名称', ''))
    ]

    referenced_material_codes = set()
    for row in _rows(jet, WB_PRODUCT, SH_ROUTE):
        referenced_material_codes.add(str(row.get('物料编码', '')).strip())
    for row in _rows(jet, WB_PRODUCT, SH_OPMAT):
        referenced_material_codes.add(str(row.get('*物料编码', '')).strip())
    for row in _rows(jet, WB_PRODUCT, SH_MBOM_NODE):
        referenced_material_codes.add(str(row.get('*物料编码', '')).strip())
        referenced_material_codes.add(str(row.get('父物料编码', '')).strip())
    referenced_material_codes.discard('')

    _rows(jet, WB_PRODUCT, SH_MAT)[:] = [
        row for row in _rows(jet, WB_PRODUCT, SH_MAT)
        if str(row.get('*编码', '')).strip() in referenced_material_codes
        and (
            str(row.get('*编码', '')).strip().endswith('-TFAN-ENG')
            or not _text_has_fan_chain(row.get('*编码', ''), row.get('*名称', ''))
        )
    ]
    keep_material_codes = {str(row.get('*编码', '')).strip() for row in _rows(jet, WB_PRODUCT, SH_MAT)}

    _rows(jet, WB_PRODUCT, SH_OPMAT)[:] = [
        row for row in _rows(jet, WB_PRODUCT, SH_OPMAT)
        if str(row.get('*物料编码', '')).strip() in keep_material_codes
    ]

    _rows(jet, WB_PRODUCT, SH_MBOM_NODE)[:] = [
        row for row in _rows(jet, WB_PRODUCT, SH_MBOM_NODE)
        if str(row.get('*物料编码', '')).strip() in keep_material_codes
        and (not str(row.get('父物料编码', '')).strip() or str(row.get('父物料编码', '')).strip() in keep_material_codes)
    ]
    _rows(jet, WB_PRODUCT, SH_ROUTE)[:] = [
        row for row in _rows(jet, WB_PRODUCT, SH_ROUTE)
        if str(row.get('物料编码', '')).strip() in keep_material_codes
    ]
    keep_route_codes = {str(row.get('*编码', '')).strip() for row in _rows(jet, WB_PRODUCT, SH_ROUTE)}
    for sheet in (SH_OP, SH_SEQ, SH_OPMAT, SH_STEP):
        _rows(jet, WB_PRODUCT, sheet)[:] = [
            row for row in _rows(jet, WB_PRODUCT, sheet)
            if str(row.get('*工艺路线编码', '')).strip() in keep_route_codes
        ]

    replacements = [
        ('民航涡扇事业部', '涡喷发动机事业部'),
        ('涡扇发动机制造中心', '涡喷发动机制造中心'),
        ('通用窄体客机', '高速飞行器'),
        ('高涵道比涡扇', '小型涡喷'),
        ('风扇与附件系统集成', '核心机与附件系统集成'),
        ('风扇模块装入', '附件模块装入'),
        ('TFAN', 'TJET'),
    ]
    return _replace_strings(jet, replacements)


def summarize(seed_data: dict) -> dict:
    return {
        'metadata': seed_data.get('metadata', {}),
        'counts': {
            workbook: {sheet: len(rows) for sheet, rows in sheets.items()}
            for workbook, sheets in seed_data.get('workbooks', {}).items()
        },
    }


def build_variant(namespace: str = NAMESPACE, volume_profile: str = DEFAULT_VOLUME_PROFILE) -> dict:
    base_seed = turbofan_seed.build_variant(namespace=namespace, volume_profile=volume_profile)
    seed = _strip_fan_chain(base_seed)
    metadata = seed.setdefault('metadata', {})
    metadata.update({
        'name': '涡喷发动机MOM种子',
        'aircraft_family': '高速飞行器',
        'engine_model': '通用小型涡喷发动机',
        'description': '基于公开小型涡喷制造逻辑构建的典型涡喷发动机MOM主数据种子。',
        'public_fact_note': '采用公开涡喷制造链条作为拟真基线，体现压气机、燃烧室、涡轮、尾喷与整机试车放行等核心环节。',
        'namespace': namespace,
        'volume_profile': volume_profile,
    })
    for row in seed.get('workbooks', {}).get(WB_SYSTEM, {}).get(SH_ADMIN, []):
        if row.get('简称') == '737事业部':
            row['简称'] = '涡喷事业部'
        if row.get('简称') == 'LEAP中心' or row.get('简称') == '涡扇中心':
            row['简称'] = '涡喷中心'
    for row in seed.get('workbooks', {}).get(WB_SYSTEM, {}).get(SH_BIZ, []):
        if row.get('简称') == '737事业部':
            row['简称'] = '涡喷事业部'
        if row.get('简称') == 'LEAP中心' or row.get('简称') == '涡扇中心':
            row['简称'] = '涡喷中心'
    for row in seed.get('workbooks', {}).get(WB_PRODUCT, {}).get(SH_MAT, []):
        if str(row.get('*编码', '')).endswith('-TJET-ENG'):
            row['*名称'] = '小型涡喷发动机总成'
    apply_production_orders(seed, 'turbojet_engine', namespace)
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
