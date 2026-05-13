from __future__ import annotations

from copy import deepcopy

WB_FACTORY = '工厂资源_模板.xlsx'
SH_TOOL = '工装工具'
SH_TOOL_INS = '工装检定策略关系'
SH_TOOL_MNT = '工装保养策略关系'

F_TOOL_VERSION = '*工装工具版本号'
F_TOOL_CODE = '*工装工具编码'
F_INSPECTION_POLICY = '*检定策略编码'
F_MAINT_POLICY = '*保养策略编码'
F_LAST_PLAN = '最后计划执行时间'
F_FACTORY_ORG = '*工厂组织'
F_CODE = '*编码'
F_VERSION = '*版本号'


def tooling_row(code: str, name: str, material_category: str, make_type: str, tooling_category: str, feature: str) -> dict:
    return {
        '*物料分类': '工装工具',
        '*名称': name,
        '物料类别': material_category,
        '图号': code,
        '*制造类型': make_type,
        '计量单位': '个',
        '特性分类': feature,
        '启用批次标记': '否',
        '启用序列号标记': '否',
        '工装类别': tooling_category,
        '一次性工装标记': '否',
        '单件工装标记': '否',
        '物料阶段': '量产',
        '*版本号': 'A.01',
        '*编码': code,
        '*密级': '内部',
    }


def inspection_row(tool_code: str, factory_org: str, policy_code: str, last_plan: str, version: str = 'A.01') -> dict:
    return {
        F_TOOL_VERSION: version,
        F_TOOL_CODE: tool_code,
        F_INSPECTION_POLICY: policy_code,
        F_LAST_PLAN: last_plan,
        F_FACTORY_ORG: factory_org,
    }


def maintenance_row(tool_code: str, factory_org: str, policy_code: str, last_plan: str, version: str = 'A.01') -> dict:
    return {
        F_TOOL_VERSION: version,
        F_TOOL_CODE: tool_code,
        F_MAINT_POLICY: policy_code,
        F_LAST_PLAN: last_plan,
        F_FACTORY_ORG: factory_org,
    }


PROFILES = {
    'boeing_737_leap1b': {
        'extra_tools': [],
        'inspection_relations': [
            inspection_row('TOOL-FAN-BLADE-LAYUP', 'BIZ-FAN', 'CAL-COMP-MOLD-HY-01', '2025-01-12 08:00:00'),
            inspection_row('TOOL-FAN-CASE-MOLD', 'BIZ-FAN', 'CAL-COMP-MOLD-HY-01', '2025-01-13 08:00:00'),
            inspection_row('TOOL-HPC-ROTOR-FIX', 'BIZ-COMP', 'CAL-ASM-FIX-QTR-01', '2025-01-15 08:00:00'),
            inspection_row('TOOL-HPT-ASM-FIX', 'BIZ-TURB', 'CAL-ASM-FIX-QTR-01', '2025-01-16 08:00:00'),
            inspection_row('TOOL-CORE-CART', 'BIZ-FINAL', 'CAL-TRANSFER-TOOL-HY-01', '2025-01-18 08:00:00'),
            inspection_row('TOOL-ENG-HOIST', 'BIZ-FINAL', 'CAL-LIFT-TOOL-HY-01', '2025-01-20 08:00:00'),
        ],
        'maintenance_relations': [
            maintenance_row('TOOL-FAN-BLADE-LAYUP', 'BIZ-FAN', 'PM-COMP-MOLD-MONTH-01', '2025-01-05 08:00:00'),
            maintenance_row('TOOL-FAN-CASE-MOLD', 'BIZ-FAN', 'PM-COMP-MOLD-MONTH-01', '2025-01-06 08:00:00'),
            maintenance_row('TOOL-HPC-ROTOR-FIX', 'BIZ-COMP', 'PM-ASM-FIX-MONTH-01', '2025-01-08 08:00:00'),
            maintenance_row('TOOL-HPT-ASM-FIX', 'BIZ-TURB', 'PM-ASM-FIX-MONTH-01', '2025-01-09 08:00:00'),
            maintenance_row('TOOL-CORE-CART', 'BIZ-FINAL', 'PM-TRANSFER-TOOL-MONTH-01', '2025-01-10 08:00:00'),
            maintenance_row('TOOL-ENG-HOIST', 'BIZ-FINAL', 'PM-LIFT-TOOL-MONTH-01', '2025-01-11 08:00:00'),
        ],
    },
    'cnc_machine': {
        'extra_tools': [],
        'inspection_relations': [
            inspection_row('TOOL-BED-FIX', 'BIZ-CAST', 'CAL-FIXTURE-QTR-01', '2025-01-08 08:00:00'),
            inspection_row('TOOL-SPINDLE-FIX', 'BIZ-SPINDLE', 'CAL-ASM-FIX-QTR-01', '2025-01-10 08:00:00'),
            inspection_row('TOOL-BSCREW-FIX', 'BIZ-SPINDLE', 'CAL-ASM-FIX-QTR-01', '2025-01-11 08:00:00'),
            inspection_row('TOOL-TABLE-FIX', 'BIZ-FINAL', 'CAL-ASM-FIX-QTR-01', '2025-01-12 08:00:00'),
            inspection_row('TOOL-ELEC-CART', 'BIZ-ELEC', 'CAL-TRANSFER-TOOL-HY-01', '2025-01-14 08:00:00'),
            inspection_row('TOOL-PACK-KIT', 'BIZ-WARE', 'CAL-HANDTOOL-YEAR-01', '2025-01-16 08:00:00'),
        ],
        'maintenance_relations': [
            maintenance_row('TOOL-BED-FIX', 'BIZ-CAST', 'PM-FIXTURE-MONTH-01', '2025-01-03 08:00:00'),
            maintenance_row('TOOL-SPINDLE-FIX', 'BIZ-SPINDLE', 'PM-ASM-FIX-MONTH-01', '2025-01-04 08:00:00'),
            maintenance_row('TOOL-BSCREW-FIX', 'BIZ-SPINDLE', 'PM-ASM-FIX-MONTH-01', '2025-01-05 08:00:00'),
            maintenance_row('TOOL-TABLE-FIX', 'BIZ-FINAL', 'PM-ASM-FIX-MONTH-01', '2025-01-06 08:00:00'),
            maintenance_row('TOOL-ELEC-CART', 'BIZ-ELEC', 'PM-TRANSFER-TOOL-MONTH-01', '2025-01-07 08:00:00'),
            maintenance_row('TOOL-PACK-KIT', 'BIZ-WARE', 'PM-HANDTOOL-QTR-01', '2025-01-09 08:00:00'),
        ],
    },
    'automotive_engine': {
        'extra_tools': [
            tooling_row('TOOL-BLOCK-TURN-01', '缸体翻转架', '配套件', '自制件', '专用工装', '关键件'),
            tooling_row('TOOL-CRANK-FIX-01', '曲轴装配定位工装', '配套件', '自制件', '专用工装', '重要件'),
            tooling_row('TOOL-PISTON-RING-01', '活塞环压装工具', '零部件', '外购件', '通用工具', '一般件'),
            tooling_row('TOOL-HEAD-TORQUE-01', '缸盖拧紧数显扭矩扳手', '零部件', '外购件', '通用工具', '关键件'),
            tooling_row('TOOL-ENG-CART-01', '发动机总成转运台', '零部件', '自制件', '专用工装', '重要件'),
        ],
        'inspection_relations': [
            inspection_row('TOOL-TORQUE-01', 'BIZ-ASM', 'CAL-TORQUE-WRENCH-MONTH-01', '2025-01-08 08:00:00'),
            inspection_row('TOOL-BLOCK-TURN-01', 'BIZ-MACH', 'CAL-FIXTURE-QTR-01', '2025-01-10 08:00:00'),
            inspection_row('TOOL-CRANK-FIX-01', 'BIZ-ASM', 'CAL-ASM-FIX-QTR-01', '2025-01-12 08:00:00'),
            inspection_row('TOOL-PISTON-RING-01', 'BIZ-ASM', 'CAL-HANDTOOL-HY-01', '2025-01-14 08:00:00'),
            inspection_row('TOOL-HEAD-TORQUE-01', 'BIZ-ASM', 'CAL-TORQUE-WRENCH-MONTH-01', '2025-01-16 08:00:00'),
            inspection_row('TOOL-ENG-CART-01', 'BIZ-ASM', 'CAL-TRANSFER-TOOL-HY-01', '2025-01-18 08:00:00'),
        ],
        'maintenance_relations': [
            maintenance_row('TOOL-TORQUE-01', 'BIZ-ASM', 'PM-TORQUE-TOOL-MONTH-01', '2025-01-04 08:00:00'),
            maintenance_row('TOOL-BLOCK-TURN-01', 'BIZ-MACH', 'PM-FIXTURE-MONTH-01', '2025-01-05 08:00:00'),
            maintenance_row('TOOL-CRANK-FIX-01', 'BIZ-ASM', 'PM-ASM-FIX-MONTH-01', '2025-01-06 08:00:00'),
            maintenance_row('TOOL-PISTON-RING-01', 'BIZ-ASM', 'PM-HANDTOOL-QTR-01', '2025-01-07 08:00:00'),
            maintenance_row('TOOL-HEAD-TORQUE-01', 'BIZ-ASM', 'PM-TORQUE-TOOL-MONTH-01', '2025-01-09 08:00:00'),
            maintenance_row('TOOL-ENG-CART-01', 'BIZ-ASM', 'PM-TRANSFER-TOOL-MONTH-01', '2025-01-11 08:00:00'),
        ],
    },
}


def _ensure_factory_sheets(seed: dict) -> dict:
    workbooks = seed.setdefault('workbooks', {})
    factory = workbooks.setdefault(WB_FACTORY, {})
    factory.setdefault(SH_TOOL, [])
    factory.setdefault(SH_TOOL_INS, [])
    factory.setdefault(SH_TOOL_MNT, [])
    return factory


def _append_missing(rows: list[dict], new_rows: list[dict], key_fields: tuple[str, ...]) -> int:
    existing = {tuple(str(row.get(field, '')).strip() for field in key_fields) for row in rows}
    added = 0
    for row in new_rows:
        key = tuple(str(row.get(field, '')).strip() for field in key_fields)
        if key in existing:
            continue
        rows.append(deepcopy(row))
        existing.add(key)
        added += 1
    return added


def apply_profile(seed: dict, profile_name: str) -> dict:
    if profile_name not in PROFILES:
        raise KeyError(f'未知工装策略配置: {profile_name}')
    profile = PROFILES[profile_name]
    factory = _ensure_factory_sheets(seed)
    added_tools = _append_missing(factory[SH_TOOL], profile['extra_tools'], (F_CODE,))
    added_inspection = _append_missing(factory[SH_TOOL_INS], profile['inspection_relations'], (F_TOOL_VERSION, F_TOOL_CODE, F_INSPECTION_POLICY, F_FACTORY_ORG))
    added_maintenance = _append_missing(factory[SH_TOOL_MNT], profile['maintenance_relations'], (F_TOOL_VERSION, F_TOOL_CODE, F_MAINT_POLICY, F_FACTORY_ORG))
    return {
        'profile': profile_name,
        'added_tools': added_tools,
        'added_inspection_relations': added_inspection,
        'added_maintenance_relations': added_maintenance,
        'tool_count': len(factory[SH_TOOL]),
        'inspection_relation_count': len(factory[SH_TOOL_INS]),
        'maintenance_relation_count': len(factory[SH_TOOL_MNT]),
    }
