from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

WB_SYSTEM = '系统配置_模板.xlsx'
WB_PRODUCT = '产品与工艺_模板.xlsx'
WB_ORDER = '生产订单_模板.xlsx'

SH_USER = '用户'
SH_MATERIAL = '物料'
SH_MBOM = 'MBOM'
SH_ROUTE = '工艺路线'
SH_ROUTE_OP = '工艺路线工序'
SH_ROUTE_OPMAT = '工艺路线工序物料'
SH_ORDER = '生产订单'
SH_PICK = '备料清单'

F_CODE = '*编码'
F_VERSION = '*版本号'
F_ID = '*编号'
F_BIZ_CODE = '业务组织编码'
F_ROUTE_VERSION = '*版本号'
F_ROUTE_CODE = '*编码'
F_ROUTE_MATERIAL_VERSION = '物料版本号'
F_ROUTE_MATERIAL_CODE = '物料编码'
F_ROUTE_ORG = '*工厂组织'
F_ROUTE_NAME = '*名称'
F_ROUTE_SPEC = '工艺专业'
F_OP_NO = '*工序号'
F_OP_NAME = '*工序名称'
F_OP_ROUTE_VERSION = '*工艺路线版本号'
F_OP_ROUTE_CODE = '*工艺路线编码'
F_OPMAT_VERSION = '*物料版本号'
F_OPMAT_CODE = '*物料编码'
F_OPMAT_QTY = '数量'
F_MAT_NAME = '*名称'
F_MAT_MODEL = '型号'
F_MAT_DRAWING = '图号'
F_MAT_UNIT = '计量单位'
F_MAT_VERSION = '*版本号'
F_MAT_CODE = '*编码'
F_MBOM_VERSION = '*版本号'
F_MBOM_CODE = '*编码'
F_MBOM_MATERIAL_VERSION = '*物料版本号'
F_MBOM_MATERIAL_CODE = '*物料编码'
F_USER_REMARK = '备注'
F_USER_NAME = '名称'
F_SECURITY = '*密级'


def _normalize(value) -> str:
    if value is None:
        return ''
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _rows(seed: dict, workbook: str, sheet: str) -> list[dict]:
    workbooks = seed.setdefault('workbooks', {})
    workbook_rows = workbooks.setdefault(workbook, {})
    return workbook_rows.setdefault(sheet, [])


def _format_dt(value: datetime | None) -> str:
    if value is None:
        return ''
    return value.strftime('%Y-%m-%d %H:%M:%S')


def _number(value) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return Decimal('0')


def _clean_number(value: Decimal):
    if value == value.to_integral_value():
        return int(value)
    return float(value.quantize(Decimal('0.001')))


def _pick_planner(users: list[dict]) -> dict | None:
    priorities = ('主计划', '计划', 'PMC', '排产', '供应链')

    def score(row: dict) -> tuple[int, str]:
        text = ' '.join(_normalize(row.get(field)) for field in (F_USER_REMARK, F_USER_NAME, F_BIZ_CODE))
        weight = 0
        for index, keyword in enumerate(priorities):
            if keyword in text:
                weight = len(priorities) - index
                break
        return weight, _normalize(row.get(F_ID))

    ranked = sorted(users, key=score, reverse=True)
    return ranked[0] if ranked else None


def _plan_quantity(scenario: str, route_row: dict, material_row: dict) -> int:
    material_name = _normalize(material_row.get(F_MAT_NAME))
    route_name = _normalize(route_row.get(F_ROUTE_NAME))
    profession = _normalize(route_row.get(F_ROUTE_SPEC))

    if scenario == 'automotive_engine':
        if '发动机' in material_name:
            return 8
        if any(keyword in material_name for keyword in ('长缸', '短缸', '缸盖')):
            return 12
        if profession in {'铸造', '锻造'}:
            return 40
        if profession in {'机加', '热表'}:
            return 20
        if profession == '装配' or '装配' in route_name:
            return 10
        return 8

    if scenario == 'cnc_machine':
        if '整机' in material_name:
            return 3
        if any(keyword in material_name for keyword in ('主轴', '刀库', '电气', '电柜', '模块')):
            return 4
        if any(keyword in route_name for keyword in ('试运行', '切削验证', '精度检测')):
            return 2
        return 3

    if scenario == 'aircraft_seat_economy_line':
        if '座椅总成' in material_name:
            return 12
        if any(keyword in material_name for keyword in ('骨架总成', '靠背总成', '电气配套组件')):
            return 14
        if any(keyword in route_name for keyword in ('检测', '放行')):
            return 10
        return 16

    if scenario == 'bicycle_assembly':
        if '自行车整车' in material_name or '整车' in material_name:
            return 18
        if any(keyword in material_name for keyword in ('前轮总成', '后轮总成')):
            return 20
        if any(keyword in route_name for keyword in ('检测', '路试', '调校')):
            return 16
        return 18

    if '整机' in route_name or '发动机总成' in material_name or '总装' in route_name:
        return 2
    if '叶片' in material_name or '叶片' in route_name:
        return 4
    if '模块' in material_name:
        return 3
    return 2


def _duration_hours(scenario: str, route_row: dict) -> int:
    route_name = _normalize(route_row.get(F_ROUTE_NAME))
    profession = _normalize(route_row.get(F_ROUTE_SPEC))

    if scenario == 'automotive_engine':
        if profession in {'铸造', '锻造'}:
            return 36
        if profession in {'机加', '热表'}:
            return 24
        if '试' in route_name:
            return 12
        if profession == '装配':
            return 16
        return 20

    if scenario == 'cnc_machine':
        if '检测' in route_name or '试运行' in route_name or '验证' in route_name:
            return 14
        if profession == '机加':
            return 20
        if profession == '装配':
            return 16
        return 12

    if scenario == 'aircraft_seat_economy_line':
        if '检测' in route_name or '放行' in route_name:
            return 10
        if profession == '装配':
            return 14
        return 12

    if scenario == 'bicycle_assembly':
        if any(keyword in route_name for keyword in ('检测', '路试', '调校')):
            return 12
        if profession == '装配':
            return 10
        return 8

    if '试车' in route_name or '放行' in route_name:
        return 18
    if profession == '机加':
        return 24
    if profession == '装配':
        return 18
    return 16


def _status_profile(index: int, total: int, quantity: int) -> dict:
    return {
        '业务状态': '初始',
        '释放状态': '未释放',
        '计划类型': '零部件加工计划',
        '排产状态': '无',
        '已释放数量': 0,
        '合格数量': 0,
        '报废数量': 0,
        'has_actual_start': False,
        'has_actual_end': False,
    }


def _apply_route_order_profile(route_row: dict, state: dict) -> dict:
    route_type = _normalize(route_row.get('*工艺类型'))
    if route_type != '一级工艺':
        return state

    updated = dict(state)
    updated['计划类型'] = '零部件交付计划'
    updated['排产状态'] = '零部件交付计划已排产'
    return updated


def _route_sort_key(route_row: dict) -> tuple[str, str]:
    return _normalize(route_row.get(F_ROUTE_ORG)), _normalize(route_row.get(F_ROUTE_CODE))


def apply_production_orders(seed: dict, scenario: str, namespace: str) -> dict:
    users = _rows(seed, WB_SYSTEM, SH_USER)
    materials = _rows(seed, WB_PRODUCT, SH_MATERIAL)
    mboms = _rows(seed, WB_PRODUCT, SH_MBOM)
    routes = sorted(_rows(seed, WB_PRODUCT, SH_ROUTE), key=_route_sort_key)
    route_ops = _rows(seed, WB_PRODUCT, SH_ROUTE_OP)
    route_materials = _rows(seed, WB_PRODUCT, SH_ROUTE_OPMAT)

    orders = _rows(seed, WB_ORDER, SH_ORDER)
    picks = _rows(seed, WB_ORDER, SH_PICK)
    orders.clear()
    picks.clear()

    material_map = {(_normalize(row.get(F_MAT_VERSION)), _normalize(row.get(F_MAT_CODE))): row for row in materials}
    mbom_map = {(_normalize(row.get(F_MBOM_MATERIAL_VERSION)), _normalize(row.get(F_MBOM_MATERIAL_CODE))): row for row in mboms}

    op_name_map: dict[tuple[str, str, str], str] = {}
    for row in route_ops:
        key = (_normalize(row.get(F_OP_ROUTE_VERSION)), _normalize(row.get(F_OP_ROUTE_CODE)), _normalize(row.get(F_OP_NO)))
        op_name_map[key] = _normalize(row.get(F_OP_NAME))

    op_material_map: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in route_materials:
        key = (_normalize(row.get(F_OP_ROUTE_VERSION)), _normalize(row.get(F_OP_ROUTE_CODE)))
        op_material_map[key].append(row)
    for rows in op_material_map.values():
        rows.sort(key=lambda row: (_normalize(row.get(F_OP_NO)), _normalize(row.get(F_OPMAT_CODE))))

    planner = _pick_planner(users)
    planner_code = _normalize(planner.get(F_ID)) if planner else ''
    base_time_map = {
        'boeing_737_leap1b': datetime(2025, 3, 10, 8, 0, 0),
        'cnc_machine': datetime(2025, 3, 15, 8, 0, 0),
        'automotive_engine': datetime(2025, 3, 20, 8, 0, 0),
        'aircraft_seat_economy_line': datetime(2025, 3, 25, 8, 0, 0),
        'bicycle_assembly': datetime(2025, 3, 28, 8, 0, 0),
    }
    base_time = base_time_map.get(scenario, datetime(2025, 3, 1, 8, 0, 0))
    security = _normalize(seed.get('metadata', {}).get('default_security')) or '内部'

    for index, route_row in enumerate(routes, start=1):
        route_version = _normalize(route_row.get(F_ROUTE_VERSION))
        route_code = _normalize(route_row.get(F_ROUTE_CODE))
        material_version = _normalize(route_row.get(F_ROUTE_MATERIAL_VERSION))
        material_code = _normalize(route_row.get(F_ROUTE_MATERIAL_CODE))
        factory_org = _normalize(route_row.get(F_ROUTE_ORG))
        material_row = material_map.get((material_version, material_code), {})
        mbom_row = mbom_map.get((material_version, material_code))
        material_name = _normalize(material_row.get(F_MAT_NAME))
        model = _normalize(material_row.get(F_MAT_MODEL)) or _normalize(material_row.get(F_MAT_DRAWING)) or material_code
        quantity = _plan_quantity(scenario, route_row, material_row)
        duration_hours = _duration_hours(scenario, route_row)
        start_time = base_time + timedelta(days=(index - 1) * 2)
        end_time = start_time + timedelta(hours=duration_hours)
        state = _apply_route_order_profile(route_row, _status_profile(index - 1, len(routes), quantity))
        actual_start = start_time + timedelta(hours=2) if state['has_actual_start'] else None
        actual_end = end_time - timedelta(hours=1) if state['has_actual_end'] else None
        order_code = f'MO-{namespace}-{index:03d}'
        order_note = f'{material_name or material_code}生产订单，按{_normalize(route_row.get(F_ROUTE_NAME))}组织执行'

        orders.append({
            '订单类型': '标准',
            '*物料版本号': material_version,
            '*物料编码': material_code,
            'BOM版本号': '',
            'BOM编码': '',
            '制造型号': model,
            '工艺路线版本号': route_version,
            '工艺路线编码': route_code,
            '*计量单位': _normalize(material_row.get(F_MAT_UNIT)) or '个',
            '*计划数量': quantity,
            '计划产出数量': quantity,
            '合格数量': state['合格数量'],
            '报废数量': state['报废数量'],
            '已释放数量': state['已释放数量'],
            '*计划开始时间': _format_dt(start_time),
            '*计划结束时间': _format_dt(end_time),
            '实际开始时间': _format_dt(actual_start),
            '计划类型': state['计划类型'],
            '排产状态': state['排产状态'],
            '实际结束时间': _format_dt(actual_end),
            '业务状态': state['业务状态'],
            '优先级': max(1, 6 - min(index, 5)),
            '计划员': planner_code,
            '*控制状态': '正常',
            '释放状态': state['释放状态'],
            '*所属组织': factory_org,
            '*编码': order_code,
            '备注': order_note,
            '*密级': security,
            '集成系统': 'MOM-SEED',
            '集成数据主键': order_code,
            '*集成创建时间': _format_dt(start_time - timedelta(hours=4)),
        })

        route_key = (route_version, route_code)
        for row in op_material_map.get(route_key, []):
            unit_qty = _number(row.get(F_OPMAT_QTY))
            demand_qty = _clean_number(unit_qty * Decimal(str(quantity)))
            component_ratio = _clean_number(unit_qty)
            op_no = _normalize(row.get(F_OP_NO))
            picks.append({
                '*生产订单编码': order_code,
                '*物料版本号': _normalize(row.get(F_OPMAT_VERSION)),
                '*物料编码': _normalize(row.get(F_OPMAT_CODE)),
                '工序名称': op_name_map.get((route_version, route_code, op_no), ''),
                '*需求数量': demand_qty,
                '*子件比例': component_ratio,
                '替换件物料版本号': '',
                '替换件物料编码': '',
                '是否必须装入': '是',
                '工序编码': op_no,
            })

    return seed
