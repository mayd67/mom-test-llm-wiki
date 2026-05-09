from __future__ import annotations

import json
import sys
from pathlib import Path

from scene_seed_upgrades import apply_scene_upgrade
from production_order_seed import apply_production_orders

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

WB_SYSTEM = '系统配置_模板.xlsx'
WB_FACTORY = '工厂资源_模板.xlsx'
WB_PRODUCT = '产品与工艺_模板.xlsx'

SH_ADMIN = '行政组织'
SH_BIZ = '业务组织'
SH_USER = '用户'
SH_SUP = '供应商'
SH_EQ = '设备'
SH_EQ_USER = '设备与用户的关系实体类'
SH_TOOL = '工装工具'
SH_TOOL_INS = '工装检定策略关系'
SH_TOOL_MNT = '工装保养策略关系'
SH_WC = '工作中心'
SH_WC_USER = '工作中心与用户关系'
SH_WC_SUP = '工作中心与供应商的关系'
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

SEC = '内部'
VER = 'A.01'
YES = '是'
NO = '否'
TIME = '分钟'
ROUTE_TYPE = '正式工艺'
MAT_CLASS = '物料'
TOOL_CLASS = '工装工具'
CAT_RAW = '原材料'
CAT_AUX = '辅助材料'
CAT_PART = '零部件'
CAT_KIT = '配套件'
MAKE_SELF = '自制件'
MAKE_BUY = '外购件'
FEATURE_KEY = '关键件'
FEATURE_IMPORTANT = '重要件'
FEATURE_NORMAL = '一般件'
STAGE = '量产'
SEQ_TYPE = 'ES'
RELEASE_TIME = '2025-03-25 08:00:00'
RELEASE_USER = ''
NAMESPACE = 'SEAT9301'

ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'aircraft_seat_economy_line_seed.json'


def new_seed() -> dict:
    return {
        'metadata': {
            'name': '航空座椅经济舱线MOM种子',
            'industry': '航空内饰',
            'product_family': '航空客舱座椅',
            'product_model': '窄体机经济舱三联座椅总成',
            'description': '基于经济舱线控制要素、采集要素和线体布局文档构建的航空座椅经济舱总装检测线主数据，覆盖骨架支线、靠背支线、总装检测线、质量采集点和订单数据。',
            'default_version': VER,
            'default_security': SEC,
            'source_documents': ['本次调研正对与MES系统的落地调研问题项.docx', '线体布局.docx', '经济舱线控制要素和采集要素.docx'],
        },
        'external_references': ['0'],
        'workbooks': {
            WB_SYSTEM: {SH_ADMIN: [], SH_BIZ: [], SH_USER: []},
            WB_FACTORY: {
                SH_SUP: [], SH_EQ: [], SH_EQ_USER: [], SH_TOOL: [], SH_TOOL_INS: [], SH_TOOL_MNT: [],
                SH_WC: [], SH_WC_USER: [], SH_WC_SUP: [], SH_WC_EQ: [], SH_WH: [], SH_LOC: [], SH_PLIB: []
            },
            WB_PRODUCT: {SH_MAT: [], SH_MBOM: [], SH_MBOM_NODE: [], SH_ROUTE: [], SH_OP: [], SH_SEQ: [], SH_OPMAT: [], SH_STEP: []},
        },
    }


seed = new_seed()
MAT: dict[str, dict] = {}
PROC: set[tuple] = set()
EQ_USER: set[tuple] = set()
WC_USER: set[tuple] = set()
WC_SUP: set[tuple] = set()
WC_EQ: set[tuple] = set()
MBOM_SEQ = {0: 10, 1: 10, 2: 10, 3: 10}


def reset() -> None:
    global seed, MAT, PROC, EQ_USER, WC_USER, WC_SUP, WC_EQ, MBOM_SEQ
    seed = new_seed()
    MAT = {}
    PROC = set()
    EQ_USER = set()
    WC_USER = set()
    WC_SUP = set()
    WC_EQ = set()
    MBOM_SEQ = {0: 10, 1: 10, 2: 10, 3: 10}


def add(workbook: str, sheet: str, row: dict) -> None:
    seed['workbooks'][workbook][sheet].append(row)


def uniq(store: set, key: tuple, workbook: str, sheet: str, row: dict) -> None:
    if key not in store:
        store.add(key)
        add(workbook, sheet, row)


def next_mbom(level: int) -> int:
    if level not in MBOM_SEQ:
        MBOM_SEQ[level] = 10
    value = MBOM_SEQ[level]
    MBOM_SEQ[level] += 10
    return value


def a_admin(parent: str, org_type: str, code: str, name: str, short: str, remark: str = '') -> None:
    row = {'*父组织编码': parent, '行政组织类型': org_type, '*编码': code, '*名称': name, '简称': short}
    if remark:
        row['备注'] = remark
    add(WB_SYSTEM, SH_ADMIN, row)


def a_biz(parent: str, code: str, name: str, short: str, org_type: str, admin: str, factory_type: str = '', remark: str = '') -> None:
    row = {'*父组织编码': parent, '*密级': SEC, '*编码': code, '*名称': name, '简称': short, '工厂组织类型': org_type, '行政组织编码': admin}
    if factory_type:
        row['工厂类型'] = factory_type
    if remark:
        row['备注'] = remark
    add(WB_SYSTEM, SH_BIZ, row)


def a_user(code: str, name: str, level: str, gender: str, admin: str, biz: str, remark: str = '', phone: str = '', email: str = '', birthday: str = '', id_no: str = '') -> None:
    row = {'*编号': code, '名称': name, '用户安全等级': level, '性别': gender, '行政组织编码': admin, '业务组织编码': biz}
    if remark:
        row['备注'] = remark
    if phone:
        row['联系方式'] = phone
    if email:
        row['电子邮箱'] = email
    if birthday:
        row['出生日期'] = birthday
    if id_no:
        row['身份证号'] = id_no
    add(WB_SYSTEM, SH_USER, row)


def a_sup(code: str, name: str, short: str, remark: str = '') -> None:
    row = {'*密级': SEC, '*编码': code, '*名称': name, '简称': short, '启用': YES}
    if remark:
        row['备注'] = remark
    add(WB_FACTORY, SH_SUP, row)


def a_eq(code: str, name: str, model: str, biz: str, bottle: str = NO, remark: str = '') -> None:
    row = {'*名称': name, '型号规格': model, '瓶颈资源': bottle, '*编码': code, '*密级': SEC, '*工厂组织': biz}
    if remark:
        row['备注'] = remark
    add(WB_FACTORY, SH_EQ, row)


def l_eq_user(eq_code: str, user_code: str) -> None:
    uniq(EQ_USER, (eq_code, user_code), WB_FACTORY, SH_EQ_USER, {'*设备编码': eq_code, '*用户': user_code})


def a_tool(code: str, name: str, material_category: str, make_type: str, tooling_category: str, feature: str, model: str = '', spec: str = '', remark: str = '', life_times: int | None = None, life_days: int | None = None) -> None:
    row = {'*物料分类': TOOL_CLASS, '*名称': name, '物料类别': material_category, '图号': code, '型号': model, '规格': spec, '*制造类型': make_type, '计量单位': '个', '特性分类': feature, '启用批次标记': NO, '启用序列号标记': NO, '工装类别': tooling_category, '一次性工装标记': NO, '单件工装标记': NO, '物料阶段': STAGE, '发布版本时间': RELEASE_TIME, '发布人': RELEASE_USER, '*版本号': VER, '*编码': code, '*密级': SEC}
    if remark:
        row['备注'] = remark
    if life_times is not None:
        row['理论寿命(次)'] = life_times
    if life_days is not None:
        row['理论寿命(天)'] = life_days
    add(WB_FACTORY, SH_TOOL, row)


def a_wc(code: str, name: str, biz: str, wc_type: str, wc_class: str, remark: str = '') -> None:
    row = {'*名称': name, '*类型': wc_type, '*分类': wc_class, '*编码': code, '*密级': SEC, '*工厂组织': biz}
    if remark:
        row['备注'] = remark
    add(WB_FACTORY, SH_WC, row)


def l_wc_user(wc_code: str, user_code: str) -> None:
    uniq(WC_USER, (wc_code, user_code), WB_FACTORY, SH_WC_USER, {'*工作中心编码': wc_code, '*用户': user_code})


def l_wc_eq(wc_code: str, eq_code: str) -> None:
    uniq(WC_EQ, (eq_code, wc_code), WB_FACTORY, SH_WC_EQ, {'*设备编码': eq_code, '*工作中心编码': wc_code})


def a_wh(code: str, name: str, biz: str, biz_type: str, mode: str = '普通库房', remark: str = '') -> None:
    row = {'*工厂组织': biz, '*名称': name, '作业模式': mode, '*业务类型': biz_type, '*编码': code, '*密级': SEC}
    if remark:
        row['备注'] = remark
    add(WB_FACTORY, SH_WH, row)


def a_loc(code: str, name: str, biz: str, warehouse: str, remark: str = '') -> None:
    row = {'*工厂组织': biz, '*库房编码': warehouse, '*名称': name, '*编码': code, '*密级': SEC}
    if remark:
        row['备注'] = remark
    add(WB_FACTORY, SH_LOC, row)


def a_proc(name: str, op_type: str, wc_code: str, prep: int, run: int, spec: str, content: str = '') -> None:
    uniq(PROC, (name, wc_code), WB_FACTORY, SH_PLIB, {'序专业类型': spec, '*名称': name, '*工序类型': op_type, '*工作中心编码': wc_code, '*定额准备时间': prep, '*定额加工时间': run, '执行标记': YES, '*时间单位': TIME, '产出比': 1, '工序内容': content or name, '*密级': SEC})


def a_mat(code: str, name: str, category: str, make_type: str, feature: str, drawing: str, model: str = '', spec: str = '', remark: str = '', batch: str = YES, serial: str = NO) -> None:
    row = {'*物料分类': MAT_CLASS, '*名称': name, '物料类别': category, '图号': drawing, '型号': model, '规格': spec, '*制造类型': make_type, '计量单位': '个', '特性分类': feature, '启用批次标记': batch, '启用序列号标记': serial, '物料阶段': STAGE, '发布版本时间': RELEASE_TIME, '发布人': RELEASE_USER, '*版本号': VER, '*编码': code, '*密级': SEC}
    if remark:
        row['备注'] = remark
    add(WB_PRODUCT, SH_MAT, row)
    MAT[code] = {'name': name, 'category': category, 'make': make_type, 'drawing': drawing}


def a_mbom(code: str, material_code: str, name: str, remark: str = '') -> None:
    row = {'*物料版本号': VER, '*物料编码': material_code, '*版本号': VER, '*编码': code, '*密级': SEC, '名称': name}
    if remark:
        row['备注'] = remark
    add(WB_PRODUCT, SH_MBOM, row)


def a_mbom_node(mbom_code: str, level: int, material_code: str, qty: int, parent_material: str = '0', parent_version: str = '') -> None:
    meta = MAT[material_code]
    add(WB_PRODUCT, SH_MBOM_NODE, {'*MBOM版本号': VER, '*MBOM编码': mbom_code, '*物料编码': material_code, '物料名称': meta['name'], '物料图号': meta['drawing'], '*物料版本': VER, '*物料类别': meta['category'], '制造类型': meta['make'], '数量': qty, '计量单位': '个', '*层级': level, '*序号': next_mbom(level), '物料阶段': STAGE, '父物料编码': parent_material, '父物料版本': parent_version})


def a_route(code: str, name: str, route_spec: str, biz: str, material_code: str, remark: str = '') -> None:
    row = {'*名称': name, '*工艺类型': ROUTE_TYPE, '工艺专业': route_spec, '物料版本号': VER, '物料编码': material_code, '*版本号': VER, '*编码': code, '*密级': SEC, '*工厂组织': biz}
    if remark:
        row['备注'] = remark
    add(WB_PRODUCT, SH_ROUTE, row)


def a_op(route_code: str, op_no: str, name: str, op_type: str, wc_code: str, prep: int, run: int, output_code: str, spec: str, content: str = '') -> None:
    add(WB_PRODUCT, SH_OP, {'*工序号': op_no, '*工序类型': op_type, '工序内容': content or name, '*工作中心编码': wc_code, '*定额辅助工时': prep, '*定额加工时间': run, '*时间单位': TIME, '执行标记': YES, '产出比': 1, '*工艺路线版本号': VER, '*工艺路线编码': route_code, '*工序名称': name, '产出物料版本号': VER, '产出物料编码': output_code, '工序专业类型': spec})
    a_proc(name, op_type, wc_code, prep, run, spec, content)


def a_seq(route_code: str, op_no: str, prev_op: str, rel: str = SEQ_TYPE) -> None:
    add(WB_PRODUCT, SH_SEQ, {'*接续关系': rel, '*工序号': op_no, '*上道工序号': prev_op, '*工艺路线版本号': VER, '*工艺路线编码': route_code})


def a_opmat(route_code: str, op_no: str, material_code: str, qty: int) -> None:
    add(WB_PRODUCT, SH_OPMAT, {'*工艺路线版本号': VER, '*工艺路线编码': route_code, '*物料版本号': VER, '*物料编码': material_code, '*工序号': op_no, '数量': qty})


def a_step(route_code: str, op_no: str, step_no: str, name: str, content: str = '') -> None:
    add(WB_PRODUCT, SH_STEP, {'*工艺路线版本号': VER, '*工艺路线编码': route_code, '*工序号': op_no, '*工步序号': step_no, '*工步名称': name, '工步内容': content or name})

def build_organizations() -> None:
    admins = [
        ('0', '公司', 'ADM-SEAT-HQ', '嘉泰航空座椅制造有限公司', '嘉泰座椅'),
        ('ADM-SEAT-HQ', '部门', 'ADM-SEAT-TECH', '工艺技术部', '工艺技术'),
        ('ADM-SEAT-HQ', '部门', 'ADM-SEAT-PMC', '生产运营部', '生产运营'),
        ('ADM-SEAT-HQ', '部门', 'ADM-SEAT-QA', '质量保证部', '质量保证'),
        ('ADM-SEAT-HQ', '部门', 'ADM-SEAT-WM', '仓储物流部', '仓储物流'),
        ('ADM-SEAT-HQ', '部门', 'ADM-SEAT-EM', '设备工装部', '设备工装'),
        ('ADM-SEAT-HQ', '部门', 'ADM-SEAT-IT', '信息化部', '信息化'),
        ('ADM-SEAT-HQ', '工厂', 'ADM-SEAT-ECO-PLANT', '经济舱座椅总装工厂', '经济舱工厂'),
    ]
    for row in admins:
        a_admin(*row)

    bizs = [
        ('0', 'BIZ-SEAT-COMPANY', '嘉泰航空座椅制造有限公司', '嘉泰座椅', '公司', 'ADM-SEAT-HQ', '', '单工厂经济舱座椅线场景'),
        ('BIZ-SEAT-COMPANY', 'BIZ-SEAT-TECH', '工艺技术部', '工艺技术', '部门', 'ADM-SEAT-TECH'),
        ('BIZ-SEAT-COMPANY', 'BIZ-SEAT-PMC', '生产运营部', '生产运营', '部门', 'ADM-SEAT-PMC'),
        ('BIZ-SEAT-COMPANY', 'BIZ-SEAT-QA', '质量保证部', '质量保证', '部门', 'ADM-SEAT-QA'),
        ('BIZ-SEAT-COMPANY', 'BIZ-SEAT-WM', '仓储物流部', '仓储物流', '部门', 'ADM-SEAT-WM'),
        ('BIZ-SEAT-COMPANY', 'BIZ-SEAT-EM', '设备工装部', '设备工装', '部门', 'ADM-SEAT-EM'),
        ('BIZ-SEAT-COMPANY', 'BIZ-SEAT-IT', '信息化部', '信息化', '部门', 'ADM-SEAT-IT'),
        ('BIZ-SEAT-COMPANY', 'BIZ-SEAT-ECO-PLANT', '经济舱座椅总装工厂', '经济舱工厂', '工厂', 'ADM-SEAT-ECO-PLANT', '装配专业', '依据线体布局，经济舱总装检测线长度约80米、宽度约10米'),
        ('BIZ-SEAT-ECO-PLANT', 'BIZ-SEAT-FRAME-WS', '骨架装配车间', '骨架车间', '车间', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-ECO-PLANT', 'BIZ-SEAT-BACK-WS', '靠背装配车间', '靠背车间', '车间', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-ECO-PLANT', 'BIZ-SEAT-MAIN-WS', '总装检测车间', '总装检测', '车间', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-FRAME-WS', 'BIZ-SEAT-FRAME-PRESS-SEC', '骨架压装工段', '骨架压装', '工段', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-FRAME-WS', 'BIZ-SEAT-FRAME-ASM-SEC', '骨架装配工段', '骨架装配', '工段', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-FRAME-WS', 'BIZ-SEAT-FRAME-CHK-SEC', '骨架检测工段', '骨架检测', '工段', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-BACK-WS', 'BIZ-SEAT-BACK-ASM-SEC', '靠背装配工段', '靠背装配', '工段', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-BACK-WS', 'BIZ-SEAT-BACK-CHK-SEC', '靠背检测工段', '靠背检测', '工段', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-MAIN-WS', 'BIZ-SEAT-MAIN-ASM1-SEC', '总装一工段', '总装一段', '工段', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-MAIN-WS', 'BIZ-SEAT-MAIN-ASM2-SEC', '总装二工段', '总装二段', '工段', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-MAIN-WS', 'BIZ-SEAT-MAIN-TUNE-SEC', '调试工段', '调试工段', '工段', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-MAIN-WS', 'BIZ-SEAT-MAIN-CHK-SEC', '检测归档工段', '检测归档', '工段', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-FRAME-PRESS-SEC', 'BIZ-SEAT-FRAME-PRESS-A', '骨架压装甲班', '压装甲班', '班组', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-FRAME-ASM-SEC', 'BIZ-SEAT-FRAME-ASM-A', '骨架装配甲班', '骨架甲班', '班组', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-FRAME-CHK-SEC', 'BIZ-SEAT-FRAME-CHK-A', '骨架检测甲班', '检测甲班', '班组', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-BACK-ASM-SEC', 'BIZ-SEAT-BACK-ASM-A', '靠背装配甲班', '靠背甲班', '班组', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-BACK-CHK-SEC', 'BIZ-SEAT-BACK-CHK-A', '靠背检测甲班', '靠背检甲', '班组', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-MAIN-ASM1-SEC', 'BIZ-SEAT-MAIN-ASM1-A', '总装一工段甲班', '总装一甲', '班组', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-MAIN-ASM2-SEC', 'BIZ-SEAT-MAIN-ASM2-A', '总装二工段甲班', '总装二甲', '班组', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-MAIN-TUNE-SEC', 'BIZ-SEAT-MAIN-TUNE-A', '调试工段甲班', '调试甲班', '班组', 'ADM-SEAT-ECO-PLANT'),
        ('BIZ-SEAT-MAIN-CHK-SEC', 'BIZ-SEAT-MAIN-CHK-A', '检测归档甲班', '归档甲班', '班组', 'ADM-SEAT-ECO-PLANT'),
    ]
    for row in bizs:
        a_biz(*row)


def build_users() -> None:
    users = [
        ('U-SEAT-001', '江承宇', '重要', '男', 'ADM-SEAT-TECH', 'BIZ-SEAT-TECH', '工艺平台主管', '139****1201', 'jiangcy@jt-seat-demo.com', '1985-03-16', '3101********1201'),
        ('U-SEAT-002', '苏雅宁', '重要', '女', 'ADM-SEAT-TECH', 'BIZ-SEAT-TECH', '骨架工艺工程师', '136****2082', 'suyn@jt-seat-demo.com', '1990-07-12', '3205********2082'),
        ('U-SEAT-003', '周启航', '重要', '男', 'ADM-SEAT-TECH', 'BIZ-SEAT-TECH', '靠背工艺工程师', '138****3153', 'zhouqh@jt-seat-demo.com', '1988-05-28', '3302********3153'),
        ('U-SEAT-004', '唐可欣', '重要', '女', 'ADM-SEAT-TECH', 'BIZ-SEAT-TECH', '总装工艺工程师', '137****4264', 'tangkx@jt-seat-demo.com', '1991-10-09', '4201********4264'),
        ('U-SEAT-005', '贺景澄', '重要', '男', 'ADM-SEAT-TECH', 'BIZ-SEAT-TECH', '工装与标准工时工程师', '135****5375', 'hejc@jt-seat-demo.com', '1987-01-24', '3701********5375'),
        ('U-SEAT-006', '孟书瑶', '重要', '女', 'ADM-SEAT-PMC', 'BIZ-SEAT-PMC', '主计划经理', '134****6416', 'mengsy@jt-seat-demo.com', '1986-08-03', '4101********6416'),
        ('U-SEAT-007', '何知远', '一般', '男', 'ADM-SEAT-PMC', 'BIZ-SEAT-PMC', '生产计划员', '139****7547', 'hezy@jt-seat-demo.com', '1992-11-14', '4301********7547'),
        ('U-SEAT-008', '罗嘉宁', '一般', '女', 'ADM-SEAT-WM', 'BIZ-SEAT-WM', '仓库主管', '136****8678', 'luojn@jt-seat-demo.com', '1989-06-18', '3201********8678'),
        ('U-SEAT-009', '魏昊然', '一般', '男', 'ADM-SEAT-WM', 'BIZ-SEAT-WM', '仓库管理员', '135****9789', 'weihr@jt-seat-demo.com', '1993-04-21', '3501********9789'),
        ('U-SEAT-010', '顾雨桐', '一般', '女', 'ADM-SEAT-WM', 'BIZ-SEAT-WM', '物流配送员', '138****1020', 'guyt@jt-seat-demo.com', '1994-12-06', '3401********1020'),
        ('U-SEAT-011', '林博文', '重要', '男', 'ADM-SEAT-QA', 'BIZ-SEAT-QA', '来料质量工程师', '137****2141', 'linbw@jt-seat-demo.com', '1988-09-17', '3601********2141'),
        ('U-SEAT-012', '许若宁', '重要', '女', 'ADM-SEAT-QA', 'BIZ-SEAT-QA', '过程质量工程师', '135****3262', 'xurn@jt-seat-demo.com', '1990-02-26', '5101********3262'),
        ('U-SEAT-013', '邵子恒', '重要', '男', 'ADM-SEAT-QA', 'BIZ-SEAT-QA', '检测工程师', '139****4383', 'shaozh@jt-seat-demo.com', '1987-07-08', '4201********4383'),
        ('U-SEAT-014', '叶欣然', '一般', '女', 'ADM-SEAT-EM', 'BIZ-SEAT-EM', '设备主管', '136****5404', 'yexr@jt-seat-demo.com', '1986-03-30', '3203********5404'),
        ('U-SEAT-015', '梁承安', '一般', '男', 'ADM-SEAT-EM', 'BIZ-SEAT-EM', '设备维修工', '138****6525', 'liangca@jt-seat-demo.com', '1989-11-02', '4302********6525'),
        ('U-SEAT-016', '宋雨荷', '一般', '女', 'ADM-SEAT-EM', 'BIZ-SEAT-EM', '工装管理员', '137****7646', 'songyh@jt-seat-demo.com', '1991-01-11', '3301********7646'),
        ('U-SEAT-017', '黄嘉宁', '一般', '男', 'ADM-SEAT-ECO-PLANT', 'BIZ-SEAT-FRAME-ASM-A', '骨架班组长', '135****8767', 'huangjn@jt-seat-demo.com', '1987-05-13', '3206********8767'),
        ('U-SEAT-018', '马睿哲', '一般', '男', 'ADM-SEAT-ECO-PLANT', 'BIZ-SEAT-FRAME-ASM-A', '骨架装配操作工', '136****9888', 'marz@jt-seat-demo.com', '1994-09-29', '4102********9888'),
        ('U-SEAT-019', '吴雅雯', '一般', '女', 'ADM-SEAT-ECO-PLANT', 'BIZ-SEAT-FRAME-CHK-A', '骨架尺寸检测员', '138****1099', 'wuyw@jt-seat-demo.com', '1993-03-05', '4206********1099'),
        ('U-SEAT-020', '郑博文', '一般', '男', 'ADM-SEAT-ECO-PLANT', 'BIZ-SEAT-BACK-ASM-A', '靠背班组长', '137****2110', 'zhengbw@jt-seat-demo.com', '1988-04-12', '3302********2110'),
        ('U-SEAT-021', '顾星瑶', '一般', '女', 'ADM-SEAT-ECO-PLANT', 'BIZ-SEAT-BACK-ASM-A', '靠背装配操作工', '135****3221', 'guxy@jt-seat-demo.com', '1995-08-22', '3402********3221'),
        ('U-SEAT-022', '谢知远', '一般', '男', 'ADM-SEAT-ECO-PLANT', 'BIZ-SEAT-BACK-CHK-A', '靠背检验员', '139****4332', 'xiezy@jt-seat-demo.com', '1992-06-14', '3607********4332'),
        ('U-SEAT-023', '孙沐晴', '一般', '女', 'ADM-SEAT-ECO-PLANT', 'BIZ-SEAT-MAIN-ASM1-A', '总装班组长', '136****5443', 'sunmq@jt-seat-demo.com', '1989-12-17', '5101********5443'),
        ('U-SEAT-024', '徐靖涵', '一般', '男', 'ADM-SEAT-ECO-PLANT', 'BIZ-SEAT-MAIN-ASM1-A', '总装装配操作工', '138****6554', 'xujh@jt-seat-demo.com', '1994-02-01', '3208********6554'),
        ('U-SEAT-025', '姚可欣', '一般', '女', 'ADM-SEAT-ECO-PLANT', 'BIZ-SEAT-MAIN-TUNE-A', '总装调试员', '137****7665', 'yaokx@jt-seat-demo.com', '1991-11-19', '4301********7665'),
        ('U-SEAT-026', '苏沐辰', '一般', '男', 'ADM-SEAT-ECO-PLANT', 'BIZ-SEAT-MAIN-CHK-A', '影像记录员', '135****8776', 'sumc@jt-seat-demo.com', '1993-10-03', '3307********8776'),
        ('U-SEAT-027', '秦若溪', '一般', '女', 'ADM-SEAT-ECO-PLANT', 'BIZ-SEAT-MAIN-CHK-A', 'TSO标牌记录员', '136****9887', 'qinrx@jt-seat-demo.com', '1992-01-26', '3209********9887'),
        ('U-SEAT-028', '韩启鸣', '一般', '男', 'ADM-SEAT-ECO-PLANT', 'BIZ-SEAT-MAIN-ASM2-A', 'USB电气装配员', '139****1998', 'hanqm@jt-seat-demo.com', '1994-05-07', '4205********1998'),
    ]
    for row in users:
        a_user(*row)

def build_resources() -> None:
    suppliers = [
        ('SUP-ALU', '中航铝材（苏州）有限公司', '中航铝材', '供应骨架铝合金型材与支板'),
        ('SUP-FAST', '上海航标紧固件有限公司', '航标紧固件', '供应航空级螺栓、螺母、垫圈及铆钉'),
        ('SUP-TRIM', '嘉盛软包系统（昆山）有限公司', '嘉盛软包', '供应坐垫、背垫和包覆组件'),
        ('SUP-BELT', '华安航空安全系统有限公司', '华安安全带', '供应旅客安全带组件'),
        ('SUP-ELEC', '苏州航电互联科技有限公司', '航电互联', '供应USB电源组件与线束'),
        ('SUP-DECOR', '宁波蓝翼客舱饰件有限公司', '蓝翼饰件', '供应装饰件、标牌和表面饰面件'),
    ]
    for row in suppliers:
        a_sup(*row)

    work_centers = [
        ('WC-FRAME-LINE', '骨架支线', 'BIZ-SEAT-FRAME-WS', '产线', '加工', '承担骨架组件压装、装配与检测'),
        ('WC-FRAME-PRESS', '骨架压装工位', 'BIZ-SEAT-FRAME-PRESS-SEC', '组织', '加工'),
        ('WC-FRAME-ASM', '骨架装配工位', 'BIZ-SEAT-FRAME-ASM-SEC', '组织', '加工'),
        ('WC-FRAME-CHK', '骨架检测工位', 'BIZ-SEAT-FRAME-CHK-SEC', '组织', '检验'),
        ('WC-BACK-LINE', '靠背支线', 'BIZ-SEAT-BACK-WS', '产线', '加工', '承担靠背组件装配与外观功能确认'),
        ('WC-BACK-PRESS', '靠背压装工位', 'BIZ-SEAT-BACK-ASM-SEC', '组织', '加工'),
        ('WC-BACK-ASM', '靠背装配工位', 'BIZ-SEAT-BACK-ASM-SEC', '组织', '加工'),
        ('WC-BACK-CHK', '靠背检测工位', 'BIZ-SEAT-BACK-CHK-SEC', '组织', '检验'),
        ('WC-MAIN-LINE', '经济舱总装检测线', 'BIZ-SEAT-MAIN-WS', '产线', '加工', '依据布局图，整线长度约80米、宽度约10米'),
        ('WC-MAIN-ASM1', '总装一工位', 'BIZ-SEAT-MAIN-ASM1-SEC', '组织', '加工'),
        ('WC-MAIN-ASM2', '总装二工位', 'BIZ-SEAT-MAIN-ASM2-SEC', '组织', '加工'),
        ('WC-TUNE', '调试工位', 'BIZ-SEAT-MAIN-TUNE-SEC', '组织', '加工'),
        ('WC-WEIGHT-LABEL', '称重标识工位', 'BIZ-SEAT-MAIN-CHK-SEC', '组织', '检验'),
        ('WC-FINAL-CHK', '外观功能检测工位', 'BIZ-SEAT-MAIN-CHK-SEC', '组织', '检验'),
        ('WC-IMAGE', '影像留存工位', 'BIZ-SEAT-MAIN-CHK-SEC', '组织', '检验'),
    ]
    for row in work_centers:
        a_wc(*row)

    equipments = [
        ('EQ-FRAME-PRESS-01', '骨架支板压装机', 'P-120伺服压装机', 'BIZ-SEAT-FRAME-PRESS-SEC', NO, '用于支板压装力控制'),
        ('EQ-FRAME-TORQUE-01', '骨架装配数显扭矩系统', 'TQ-80A', 'BIZ-SEAT-FRAME-ASM-SEC', YES, '采集椅腿与支板装配扭矩'),
        ('EQ-RIVET-01', '骨架铆接工作站', 'RV-160', 'BIZ-SEAT-FRAME-ASM-SEC', NO, '完成行李挡杆及支撑件铆接'),
        ('EQ-COAX-GAUGE-01', '骨架同轴度检测台', 'CX-240', 'BIZ-SEAT-FRAME-CHK-SEC', NO, '检测支板轴套与销子同轴度'),
        ('EQ-BACK-PRESS-01', '靠背锁板压装机', 'P-80A', 'BIZ-SEAT-BACK-ASM-SEC', NO, '用于锁连接板与衬套压装'),
        ('EQ-BACK-RIVET-01', '靠背铆接工作站', 'RV-120', 'BIZ-SEAT-BACK-ASM-SEC', NO, '完成靠背支撑件铆接'),
        ('EQ-BACK-TORQUE-01', '靠背装配扭矩站', 'TQ-35A', 'BIZ-SEAT-BACK-ASM-SEC', NO, '采集书报盒和头靠底座装配扭矩'),
        ('EQ-MAIN-CONVEY-01', '经济舱总装输送线', 'CV-80M', 'BIZ-SEAT-MAIN-WS', YES, '座椅总成自动上线、输送和下线'),
        ('EQ-MAIN-TORQUE-01', '总装多轴扭矩枪', 'MT-120', 'BIZ-SEAT-MAIN-ASM1-SEC', YES, '总装锁紧扭矩自动采集'),
        ('EQ-FOLD-FORCE-01', '扶手上折力测试仪', 'FF-30', 'BIZ-SEAT-MAIN-ASM1-SEC', NO, '检测扶手上折力与功能一致性'),
        ('EQ-ELEC-TEST-01', 'USB电源功能测试台', 'USB-TEST-02', 'BIZ-SEAT-MAIN-ASM2-SEC', NO, '检测USB单元通电输出'),
        ('EQ-ANGLE-MEAS-01', '餐桌角度检测仪', 'AG-3D', 'BIZ-SEAT-MAIN-TUNE-SEC', NO, '检测餐桌角度与打开速度'),
        ('EQ-HEIGHT-GAUGE-01', '座椅总高测量仪', 'HG-1144', 'BIZ-SEAT-MAIN-TUNE-SEC', NO, '检测座椅总高和靠背姿态'),
        ('EQ-WEIGH-01', '座椅自动称重台', 'WT-300', 'BIZ-SEAT-MAIN-CHK-SEC', NO, '记录座椅重量'),
        ('EQ-LABEL-01', 'TSO标牌打印机', 'LP-TSO', 'BIZ-SEAT-MAIN-CHK-SEC', NO, '打印并绑定TSO标识'),
        ('EQ-VISION-01', '影像采集终端', 'CAM-4K', 'BIZ-SEAT-MAIN-CHK-SEC', NO, '留存下线前结构与外观影像'),
        ('EQ-TEMP-HUM-01', '温湿度采集器', 'TH-900', 'BIZ-SEAT-MAIN-ASM2-SEC', NO, '监控螺纹胶与勾绒带粘接环境'),
        ('EQ-CLEAN-01', '吸尘清洁工位', 'CL-55', 'BIZ-SEAT-MAIN-ASM2-SEC', NO, '清理多余物和异物'),
        ('EQ-FINAL-QC-01', '外观功能检测台', 'QC-SEAT-01', 'BIZ-SEAT-MAIN-CHK-SEC', NO, '外观与功能最终判定'),
    ]
    for row in equipments:
        a_eq(*row)

    eq_user_links = [
        ('EQ-FRAME-PRESS-01', 'U-SEAT-002'), ('EQ-FRAME-TORQUE-01', 'U-SEAT-017'), ('EQ-RIVET-01', 'U-SEAT-018'), ('EQ-COAX-GAUGE-01', 'U-SEAT-019'),
        ('EQ-BACK-PRESS-01', 'U-SEAT-003'), ('EQ-BACK-RIVET-01', 'U-SEAT-020'), ('EQ-BACK-TORQUE-01', 'U-SEAT-021'),
        ('EQ-MAIN-CONVEY-01', 'U-SEAT-023'), ('EQ-MAIN-TORQUE-01', 'U-SEAT-024'), ('EQ-FOLD-FORCE-01', 'U-SEAT-025'), ('EQ-ELEC-TEST-01', 'U-SEAT-028'),
        ('EQ-ANGLE-MEAS-01', 'U-SEAT-025'), ('EQ-HEIGHT-GAUGE-01', 'U-SEAT-025'), ('EQ-WEIGH-01', 'U-SEAT-027'), ('EQ-LABEL-01', 'U-SEAT-027'),
        ('EQ-VISION-01', 'U-SEAT-026'), ('EQ-TEMP-HUM-01', 'U-SEAT-016'), ('EQ-CLEAN-01', 'U-SEAT-024'), ('EQ-FINAL-QC-01', 'U-SEAT-013'),
    ]
    for eq_code, user_code in eq_user_links:
        l_eq_user(eq_code, user_code)

    tools = [
        ('TOOL-FRAME-PRESS-DIE-01', '骨架支板压装模具', CAT_KIT, MAKE_SELF, '专用工装', FEATURE_KEY, 'PD-FRAME-01', '支板压装模', '用于控制压装力与安装深度', 120000, 365),
        ('TOOL-LOCKAXIS-JIG-01', '锁轴安装辅助工装', CAT_KIT, MAKE_SELF, '专用工装', FEATURE_IMPORTANT, 'JG-LA-01', '锁轴定位', '确保锁轴方向和位置一致', 80000, 365),
        ('TOOL-FOOTREST-TORQUE-01', '脚踏装配数显扭矩扳手', CAT_PART, MAKE_BUY, '通用工具', FEATURE_KEY, 'TW-60', '0-60Nm', '采集脚踏安装扭矩', 50000, 180),
        ('TOOL-BACKREST-LOC-01', '靠背装配定位工装', CAT_KIT, MAKE_SELF, '专用工装', FEATURE_IMPORTANT, 'JG-BK-01', '靠背定位', '控制靠背装配基准', 60000, 365),
        ('TOOL-TABLE-ANGLE-GAUGE-01', '餐桌角度调节检具', CAT_PART, MAKE_BUY, '通用工具', FEATURE_KEY, 'AG-TB-01', '3°量规', '检测餐桌角度和一致性', 40000, 180),
        ('TOOL-TSO-MARK-JIG-01', 'TSO标牌定位工装', CAT_KIT, MAKE_SELF, '专用工装', FEATURE_NORMAL, 'JG-TSO-01', '标牌定位', '保证标牌位置一致', 30000, 365),
        ('TOOL-SEAT-TRANSFER-PALLET-01', '座椅转运托盘', CAT_KIT, MAKE_SELF, '专用工装', FEATURE_IMPORTANT, 'TR-SEAT-01', '总装转运', '实现骨架上线与自动解锁下线周转', 100000, 365),
    ]
    for row in tools:
        a_tool(*row)

    wc_user_links = [
        ('WC-FRAME-PRESS', 'U-SEAT-002'), ('WC-FRAME-PRESS', 'U-SEAT-017'), ('WC-FRAME-ASM', 'U-SEAT-017'), ('WC-FRAME-ASM', 'U-SEAT-018'), ('WC-FRAME-CHK', 'U-SEAT-019'),
        ('WC-BACK-PRESS', 'U-SEAT-003'), ('WC-BACK-ASM', 'U-SEAT-020'), ('WC-BACK-ASM', 'U-SEAT-021'), ('WC-BACK-CHK', 'U-SEAT-022'),
        ('WC-MAIN-ASM1', 'U-SEAT-004'), ('WC-MAIN-ASM1', 'U-SEAT-023'), ('WC-MAIN-ASM1', 'U-SEAT-024'), ('WC-MAIN-ASM2', 'U-SEAT-028'), ('WC-MAIN-ASM2', 'U-SEAT-024'),
        ('WC-TUNE', 'U-SEAT-025'), ('WC-WEIGHT-LABEL', 'U-SEAT-027'), ('WC-FINAL-CHK', 'U-SEAT-013'), ('WC-FINAL-CHK', 'U-SEAT-012'), ('WC-IMAGE', 'U-SEAT-026'),
    ]
    for wc_code, user_code in wc_user_links:
        l_wc_user(wc_code, user_code)

    wc_eq_links = [
        ('WC-FRAME-PRESS', 'EQ-FRAME-PRESS-01'), ('WC-FRAME-ASM', 'EQ-FRAME-TORQUE-01'), ('WC-FRAME-ASM', 'EQ-RIVET-01'), ('WC-FRAME-CHK', 'EQ-COAX-GAUGE-01'),
        ('WC-BACK-PRESS', 'EQ-BACK-PRESS-01'), ('WC-BACK-ASM', 'EQ-BACK-RIVET-01'), ('WC-BACK-ASM', 'EQ-BACK-TORQUE-01'),
        ('WC-MAIN-LINE', 'EQ-MAIN-CONVEY-01'), ('WC-MAIN-ASM1', 'EQ-MAIN-TORQUE-01'), ('WC-MAIN-ASM1', 'EQ-FOLD-FORCE-01'), ('WC-MAIN-ASM2', 'EQ-ELEC-TEST-01'),
        ('WC-TUNE', 'EQ-ANGLE-MEAS-01'), ('WC-TUNE', 'EQ-HEIGHT-GAUGE-01'), ('WC-WEIGHT-LABEL', 'EQ-WEIGH-01'), ('WC-WEIGHT-LABEL', 'EQ-LABEL-01'),
        ('WC-IMAGE', 'EQ-VISION-01'), ('WC-MAIN-ASM2', 'EQ-TEMP-HUM-01'), ('WC-MAIN-ASM2', 'EQ-CLEAN-01'), ('WC-FINAL-CHK', 'EQ-FINAL-QC-01'),
    ]
    for wc_code, eq_code in wc_eq_links:
        l_wc_eq(wc_code, eq_code)

    warehouses = [
        ('WH-RAW', '原材料库', 'BIZ-SEAT-WM', 'ERP一级库', '普通库房', '存放铝材、铆钉、螺纹胶等原辅料'),
        ('WH-KIT', '外购配套件库', 'BIZ-SEAT-WM', 'ERP一级库', '普通库房', '存放扶手、USB、安全带等外购件'),
        ('WH-WIP', '在制品暂存库', 'BIZ-SEAT-WM', '车间二级库', '普通库房', '存放骨架、靠背和待检测在制品'),
        ('WH-FG', '成品库', 'BIZ-SEAT-WM', 'ERP二级库', '普通库房', '存放检测放行后的成品座椅'),
    ]
    for row in warehouses:
        a_wh(*row)

    locations = [
        ('LOC-RAW-01', '原辅料A区', 'BIZ-SEAT-WM', 'WH-RAW'), ('LOC-RAW-02', '粘接辅料区', 'BIZ-SEAT-WM', 'WH-RAW'),
        ('LOC-KIT-01', '外购件A区', 'BIZ-SEAT-WM', 'WH-KIT'), ('LOC-KIT-02', '电气配套区', 'BIZ-SEAT-WM', 'WH-KIT'),
        ('LOC-WIP-01', '骨架在制区', 'BIZ-SEAT-WM', 'WH-WIP'), ('LOC-WIP-02', '靠背在制区', 'BIZ-SEAT-WM', 'WH-WIP'),
        ('LOC-WIP-03', '待检暂存区', 'BIZ-SEAT-WM', 'WH-WIP'), ('LOC-FG-01', '成品待发区', 'BIZ-SEAT-WM', 'WH-FG'),
    ]
    for row in locations:
        a_loc(*row)

def build_materials() -> None:
    materials = [
        ('MAT-SEAT-ECON-3S', '窄体机经济舱三联座椅总成', CAT_PART, MAKE_SELF, FEATURE_KEY, 'JT-ECO3-ASM-001', 'JT-ECO3-01', '三联座椅', '经济舱总装检测线主产品', YES, YES),
        ('MAT-FRAME-BASE', '骨架基座组件', CAT_PART, MAKE_SELF, FEATURE_KEY, 'JT-FRM-BASE-001', 'FB-01', '骨架基座', '支板压装后的骨架基座件', YES, YES),
        ('MAT-FRAME-LEG-ASM', '椅腿组件', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'JT-FRM-LEG-001', 'FL-01', '椅腿组件', '骨架支线关键组件', YES, YES),
        ('MAT-FRAME-ASM', '骨架总成', CAT_PART, MAKE_SELF, FEATURE_KEY, 'JT-FRM-ASM-001', 'FA-01', '骨架总成', '总装上线前骨架主组件', YES, YES),
        ('MAT-BACKREST-ASM', '靠背总成', CAT_PART, MAKE_SELF, FEATURE_KEY, 'JT-BK-ASM-001', 'BA-01', '靠背总成', '靠背支线输出件', YES, YES),
        ('MAT-ELEC-KIT', '电气配套组件', CAT_KIT, MAKE_SELF, FEATURE_IMPORTANT, 'JT-EL-KIT-001', 'EK-01', '电气配套', 'USB单元与线束集成件', YES, YES),
        ('MAT-CUSHION-KIT', '坐垫背垫组件', CAT_KIT, MAKE_BUY, FEATURE_IMPORTANT, 'JT-CUS-001', 'CK-01', '坐垫背垫', '总装工位安装件', YES, YES),
        ('MAT-SAFETY-BELT', '安全带组件', CAT_KIT, MAKE_BUY, FEATURE_KEY, 'JT-BELT-001', 'SB-01', '安全带', '乘员约束关键件', YES, YES),
        ('MAT-ARMREST-LH', '左扶手组件', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'JT-ARM-L-001', 'ARML-01', '左扶手', '含上折力检测', YES, YES),
        ('MAT-ARMREST-RH', '右扶手组件', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'JT-ARM-R-001', 'ARMR-01', '右扶手', '含上折力检测', YES, YES),
        ('MAT-FOOTREST', '脚踏组件', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'JT-FOOT-001', 'FR-01', '脚踏', '总装阶段安装件', YES, YES),
        ('MAT-TABLE-ASM', '餐桌组件', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'JT-TABLE-001', 'TB-01', '餐桌', '需调节打开速度与角度', YES, YES),
        ('MAT-HEADREST-KIT', '头靠组件', CAT_KIT, MAKE_BUY, FEATURE_NORMAL, 'JT-HD-001', 'HR-01', '头靠组件', '含头靠软包和连接件', YES, YES),
        ('MAT-LOCK-AXIS', '锁轴组件', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'JT-LAX-001', 'LA-01', '锁轴', '锁轴转动灵活性受控', YES, YES),
        ('MAT-USB-UNIT', 'USB电源单元', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'JT-USB-001', 'USB-01', 'USB单元', '单件追溯件', YES, YES),
        ('MAT-DECOR-KIT', '装饰件包', CAT_KIT, MAKE_BUY, FEATURE_NORMAL, 'JT-DEC-001', 'DK-01', '装饰件包', '含侧装饰件和饰盖', YES, YES),
        ('MAT-TSO-PLATE', 'TSO标牌', CAT_PART, MAKE_BUY, FEATURE_NORMAL, 'JT-TSO-001', 'TSO-01', 'TSO标牌', '用于成品标识建档', YES, YES),
        ('MAT-FRAME-SUPPORT-PLATE', '支板', CAT_PART, MAKE_BUY, FEATURE_KEY, 'JT-SUPP-001', 'SP-01', '支板', '骨架关键受力件', YES, YES),
        ('MAT-FRAME-LEG-LH', '左椅腿', CAT_PART, MAKE_BUY, FEATURE_KEY, 'JT-LEG-L-001', 'LL-01', '左椅腿', '关键结构件', YES, YES),
        ('MAT-FRAME-LEG-RH', '右椅腿', CAT_PART, MAKE_BUY, FEATURE_KEY, 'JT-LEG-R-001', 'LR-01', '右椅腿', '关键结构件', YES, YES),
        ('MAT-BAGGAGE-BAR', '行李挡杆', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'JT-BAR-001', 'BG-01', '挡杆', '骨架侧向约束结构件', YES, YES),
        ('MAT-BACK-FRAME', '靠背骨架', CAT_PART, MAKE_BUY, FEATURE_KEY, 'JT-BKF-001', 'BF-01', '靠背骨架', '靠背主承力件', YES, YES),
        ('MAT-LOCK-PLATE', '锁连接板', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'JT-LP-001', 'LP-01', '锁连接板', '需压装质量确认', YES, YES),
        ('MAT-BUSHING', '靠背衬套', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'JT-BSH-001', 'BSH-01', '衬套', '压装件', YES, YES),
        ('MAT-MAGAZINE-BOX', '高位书报盒组件', CAT_PART, MAKE_BUY, FEATURE_NORMAL, 'JT-MAG-001', 'MB-01', '书报盒组件', '外观功能件', YES, YES),
        ('MAT-PED-BRACKET', 'PED支架组件', CAT_PART, MAKE_BUY, FEATURE_NORMAL, 'JT-PED-001', 'PED-01', 'PED支架', '电气附件支撑件', YES, YES),
        ('MAT-HEADREST-SLIDER', '头靠滑块', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'JT-SLD-001', 'SLD-01', '滑块', '影响头靠顺畅度', YES, YES),
        ('MAT-HYD-LOCK', '液压锁', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'JT-HLK-001', 'HL-01', '液压锁', '锁扣功能关键件', YES, YES),
        ('MAT-LINK-ROD', '连接杆', CAT_PART, MAKE_BUY, FEATURE_NORMAL, 'JT-LR-001', 'LNK-01', '连接杆', '液压锁连接件', YES, YES),
        ('MAT-CABLE-KIT', '电气线束包', CAT_KIT, MAKE_BUY, FEATURE_IMPORTANT, 'JT-CBL-001', 'CBL-01', '线束包', 'USB和标识电路配套件', YES, YES),
        ('MAT-LABEL-KIT', '条码标签包', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'JT-LAB-001', 'LAB-01', '条码标签', '条码建档和工位识别', YES, NO),
        ('MAT-RAW-FASTENER-KIT', '紧固件包', CAT_RAW, MAKE_BUY, FEATURE_NORMAL, 'JT-FST-001', 'FST-01', '紧固件', '螺栓、螺母、垫片组合', YES, NO),
        ('MAT-RAW-RIVET', '铆钉包', CAT_RAW, MAKE_BUY, FEATURE_NORMAL, 'JT-RVT-001', 'RVT-01', '铆钉', '靠背和骨架铆接辅料', YES, NO),
        ('MAT-AUX-THREAD-GLUE', '螺纹胶', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'JT-GLU-001', 'GLU-01', '螺纹胶', '受温湿度控制', YES, NO),
        ('MAT-AUX-HOOK-LOOP', '勾绒带与救生衣袋辅料', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'JT-HK-001', 'HK-01', '勾绒带', '总装前段安装辅料', YES, NO),
        ('MAT-AUX-CLEAN-KIT', '清洁辅料包', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'JT-CLN-001', 'CLN-01', '清洁辅料', '异物清洁与终检清洁', YES, NO),
    ]
    for row in materials:
        a_mat(*row)


def build_mboms() -> None:
    mboms = [
        ('MBOM-FRAME-A01', 'MAT-FRAME-ASM', '骨架总成MBOM', '骨架支线装配件'),
        ('MBOM-BACK-A01', 'MAT-BACKREST-ASM', '靠背总成MBOM', '靠背支线装配件'),
        ('MBOM-ELEC-A01', 'MAT-ELEC-KIT', '电气配套组件MBOM', '电气配套预装件'),
        ('MBOM-SEAT-A01', 'MAT-SEAT-ECON-3S', '经济舱三联座椅总成MBOM', '总装检测线主产品'),
    ]
    for row in mboms:
        a_mbom(*row)
    for mbom_code, root_material in [('MBOM-FRAME-A01', 'MAT-FRAME-ASM'), ('MBOM-BACK-A01', 'MAT-BACKREST-ASM'), ('MBOM-ELEC-A01', 'MAT-ELEC-KIT'), ('MBOM-SEAT-A01', 'MAT-SEAT-ECON-3S')]:
        a_mbom_node(mbom_code, 0, root_material, 1, '0', '')
    for child, qty in [('MAT-FRAME-BASE', 1), ('MAT-FRAME-LEG-ASM', 1), ('MAT-LOCK-AXIS', 2), ('MAT-FOOTREST', 1), ('MAT-RAW-FASTENER-KIT', 1)]:
        a_mbom_node('MBOM-FRAME-A01', 1, child, qty, 'MAT-FRAME-ASM', VER)
    for child, qty in [('MAT-BACK-FRAME', 1), ('MAT-LOCK-PLATE', 1), ('MAT-BUSHING', 2), ('MAT-MAGAZINE-BOX', 1), ('MAT-PED-BRACKET', 1), ('MAT-HEADREST-SLIDER', 2), ('MAT-HYD-LOCK', 1), ('MAT-LINK-ROD', 1), ('MAT-RAW-RIVET', 1), ('MAT-RAW-FASTENER-KIT', 1)]:
        a_mbom_node('MBOM-BACK-A01', 1, child, qty, 'MAT-BACKREST-ASM', VER)
    for child, qty in [('MAT-USB-UNIT', 1), ('MAT-CABLE-KIT', 1), ('MAT-LABEL-KIT', 1)]:
        a_mbom_node('MBOM-ELEC-A01', 1, child, qty, 'MAT-ELEC-KIT', VER)
    for child, qty in [('MAT-FRAME-ASM', 1), ('MAT-BACKREST-ASM', 1), ('MAT-ELEC-KIT', 1), ('MAT-CUSHION-KIT', 1), ('MAT-SAFETY-BELT', 1), ('MAT-ARMREST-LH', 1), ('MAT-ARMREST-RH', 1), ('MAT-TABLE-ASM', 1), ('MAT-HEADREST-KIT', 1), ('MAT-DECOR-KIT', 1), ('MAT-TSO-PLATE', 1)]:
        a_mbom_node('MBOM-SEAT-A01', 1, child, qty, 'MAT-SEAT-ECON-3S', VER)

def build_routes() -> None:
    routes = [
        {
            'code': 'RT-FRAME-BASE-A01', 'name': '骨架基座压装工艺', 'route_spec': '装配', 'biz': 'BIZ-SEAT-FRAME-WS', 'material': 'MAT-FRAME-BASE', 'proc_spec': '装配专业', 'remark': '对应控制要素中的支板压装、支板固定和间隙检查',
            'ops': [
                {'no': '0010', 'name': '支板压装', 'type': '加工', 'wc': 'WC-FRAME-PRESS', 'prep': 12, 'run': 25, 'out': 'MAT-FRAME-BASE', 'content': '完成骨架支板压装并记录压装力曲线', 'materials': [('MAT-FRAME-SUPPORT-PLATE', 1)], 'steps': ['确认压装模具状态和工装编号', '执行支板压装并保存压装力曲线']},
                {'no': '0020', 'name': '支板固定', 'type': '加工', 'wc': 'WC-FRAME-ASM', 'prep': 10, 'run': 20, 'out': 'MAT-FRAME-BASE', 'content': '完成支板锁紧、扭矩和铆接间隙控制', 'materials': [('MAT-RAW-FASTENER-KIT', 1), ('MAT-RAW-RIVET', 1), ('MAT-AUX-THREAD-GLUE', 1)], 'steps': ['按规范涂覆螺纹胶并完成锁紧', '检查铆接间隙和支板定位状态']},
                {'no': '0030', 'name': '支板间距检测', 'type': '检验', 'wc': 'WC-FRAME-CHK', 'prep': 8, 'run': 12, 'out': 'MAT-FRAME-BASE', 'content': '检测支板间距和关键安装尺寸', 'materials': [], 'steps': ['检测支板间距480±0.5mm', '记录关键尺寸并判定是否合格']},
                {'no': '0040', 'name': '转入骨架装配工段', 'type': '厂内转工', 'wc': 'WC-FRAME-LINE', 'prep': 5, 'run': 8, 'out': 'MAT-FRAME-BASE', 'content': '骨架基座组件转入骨架装配工位', 'materials': [], 'steps': ['生成在制流转记录', '转入骨架装配缓存区']},
            ],
        },
        {
            'code': 'RT-FRAME-LEG-A01', 'name': '椅腿组件装配工艺', 'route_spec': '装配', 'biz': 'BIZ-SEAT-FRAME-WS', 'material': 'MAT-FRAME-LEG-ASM', 'proc_spec': '装配专业', 'remark': '对应控制要素中的椅腿组件装配、椅腿固定和行李挡杆安装',
            'ops': [
                {'no': '0010', 'name': '椅腿组件装配', 'type': '加工', 'wc': 'WC-FRAME-ASM', 'prep': 12, 'run': 28, 'out': 'MAT-FRAME-LEG-ASM', 'content': '完成左右椅腿装配并记录扭矩值', 'materials': [('MAT-FRAME-LEG-LH', 1), ('MAT-FRAME-LEG-RH', 1), ('MAT-RAW-FASTENER-KIT', 1)], 'steps': ['装配左右椅腿并完成初锁紧', '记录关键安装扭矩和复核左右件方向']},
                {'no': '0020', 'name': '椅腿固定', 'type': '加工', 'wc': 'WC-FRAME-ASM', 'prep': 10, 'run': 22, 'out': 'MAT-FRAME-LEG-ASM', 'content': '执行关键工序扭矩锁紧并控制椅腿间距', 'materials': [('MAT-AUX-THREAD-GLUE', 1)], 'steps': ['按22±1Nm执行关键锁紧', '检测椅腿间距527±0.38与520±1关键尺寸']},
                {'no': '0030', 'name': '安装行李挡杆', 'type': '加工', 'wc': 'WC-FRAME-ASM', 'prep': 8, 'run': 16, 'out': 'MAT-FRAME-LEG-ASM', 'content': '完成行李挡杆安装、铆接间隙和防漏装检查', 'materials': [('MAT-BAGGAGE-BAR', 1), ('MAT-RAW-RIVET', 1)], 'steps': ['安装行李挡杆并复核挡杆定位', '检查铆接间隙和堵盖螺钉防漏装']},
                {'no': '0040', 'name': '同轴度与尺寸检测', 'type': '检验', 'wc': 'WC-FRAME-CHK', 'prep': 8, 'run': 12, 'out': 'MAT-FRAME-LEG-ASM', 'content': '检测同轴度、挡杆关键尺寸和外观状态', 'materials': [], 'steps': ['检测支板轴套与销子同轴度◎0.24', '记录挡杆关键尺寸并判定合格']},
            ],
        },
        {
            'code': 'RT-FRAME-FINAL-A01', 'name': '骨架总成装配工艺', 'route_spec': '装配', 'biz': 'BIZ-SEAT-FRAME-WS', 'material': 'MAT-FRAME-ASM', 'proc_spec': '装配专业', 'remark': '骨架支线输出件，用于总装骨架上线',
            'ops': [
                {'no': '0010', 'name': '骨架预穿与防护', 'type': '加工', 'wc': 'WC-FRAME-ASM', 'prep': 10, 'run': 18, 'out': 'MAT-FRAME-ASM', 'content': '执行骨架预穿和防划伤防护处理', 'materials': [('MAT-FRAME-BASE', 1), ('MAT-FRAME-LEG-ASM', 1)], 'steps': ['完成骨架预穿配合并核对外观', '布置防护件防止后续划伤']},
                {'no': '0020', 'name': '锁轴与脚踏安装', 'type': '加工', 'wc': 'WC-FRAME-ASM', 'prep': 10, 'run': 20, 'out': 'MAT-FRAME-ASM', 'content': '完成锁轴和脚踏组件安装并记录扭矩', 'materials': [('MAT-LOCK-AXIS', 2), ('MAT-FOOTREST', 1), ('MAT-RAW-FASTENER-KIT', 1)], 'steps': ['安装锁轴并确认转动灵活', '安装脚踏并记录扭矩值']},
                {'no': '0030', 'name': '骨架尺寸终检', 'type': '检验', 'wc': 'WC-FRAME-CHK', 'prep': 8, 'run': 15, 'out': 'MAT-FRAME-ASM', 'content': '完成骨架终检并转总装线', 'materials': [], 'steps': ['执行骨架总成外形尺寸终检', '完成放行并绑定在制编码']},
            ],
        },
        {
            'code': 'RT-BACKREST-A01', 'name': '靠背总成装配工艺', 'route_spec': '装配', 'biz': 'BIZ-SEAT-BACK-WS', 'material': 'MAT-BACKREST-ASM', 'proc_spec': '装配专业', 'remark': '对应控制要素中的靠背压装、书报盒/PED支架装配和锁扣功能检查',
            'ops': [
                {'no': '0010', 'name': '压装锁连接板与衬套', 'type': '加工', 'wc': 'WC-BACK-PRESS', 'prep': 12, 'run': 20, 'out': 'MAT-BACKREST-ASM', 'content': '完成锁连接板和靠背衬套压装', 'materials': [('MAT-BACK-FRAME', 1), ('MAT-LOCK-PLATE', 1), ('MAT-BUSHING', 2)], 'steps': ['检查靠背骨架定位状态', '执行压装并确认压装质量']},
                {'no': '0020', 'name': '书报盒与PED支架装配', 'type': '加工', 'wc': 'WC-BACK-ASM', 'prep': 10, 'run': 22, 'out': 'MAT-BACKREST-ASM', 'content': '装配书报盒和PED支架并记录扭矩', 'materials': [('MAT-MAGAZINE-BOX', 1), ('MAT-PED-BRACKET', 1), ('MAT-RAW-FASTENER-KIT', 1)], 'steps': ['装配书报盒并确认外观缝隙', '装配PED支架并记录0.4±0.1Nm扭矩']},
                {'no': '0030', 'name': '安装开口挡圈与支撑件铆接', 'type': '加工', 'wc': 'WC-BACK-ASM', 'prep': 10, 'run': 18, 'out': 'MAT-BACKREST-ASM', 'content': '安装开口挡圈并完成支撑件铆接', 'materials': [('MAT-RAW-RIVET', 1)], 'steps': ['检查开口挡圈错漏装', '完成支撑件铆接并检查间隙']},
                {'no': '0040', 'name': '安装头靠滑块与高位书报盒', 'type': '加工', 'wc': 'WC-BACK-ASM', 'prep': 12, 'run': 20, 'out': 'MAT-BACKREST-ASM', 'content': '完成头靠滑块、高位书报盒和罩壳装配', 'materials': [('MAT-HEADREST-SLIDER', 2), ('MAT-HEADREST-KIT', 1), ('MAT-RAW-FASTENER-KIT', 1)], 'steps': ['装配头靠滑块并检查顺畅度', '装配高位书报盒与罩壳并检查缝隙一致性']},
                {'no': '0050', 'name': '安装液压锁与连接杆', 'type': '加工', 'wc': 'WC-BACK-ASM', 'prep': 10, 'run': 16, 'out': 'MAT-BACKREST-ASM', 'content': '完成液压锁和连接杆装配', 'materials': [('MAT-HYD-LOCK', 1), ('MAT-LINK-ROD', 1)], 'steps': ['装配液压锁和连接杆', '确认开口销状态和方向正确']},
                {'no': '0060', 'name': '外观与锁扣功能检查', 'type': '检验', 'wc': 'WC-BACK-CHK', 'prep': 8, 'run': 14, 'out': 'MAT-BACKREST-ASM', 'content': '执行靠背外观和锁扣功能检查', 'materials': [], 'steps': ['检查外观和间隙一致性', '执行锁扣功能检查并记录结果']},
            ],
        },
        {
            'code': 'RT-ELEC-A01', 'name': '电气配套组件工艺', 'route_spec': '装配', 'biz': 'BIZ-SEAT-MAIN-WS', 'material': 'MAT-ELEC-KIT', 'proc_spec': '装配专业', 'remark': '对应采集要素中的USB单元追溯和电气功能验证',
            'ops': [
                {'no': '0010', 'name': 'USB单元安装', 'type': '加工', 'wc': 'WC-MAIN-ASM2', 'prep': 8, 'run': 15, 'out': 'MAT-ELEC-KIT', 'content': '完成USB单元与线束装配', 'materials': [('MAT-USB-UNIT', 1), ('MAT-CABLE-KIT', 1)], 'steps': ['扫码记录USB单元单件编码', '完成USB单元和线束装配']},
                {'no': '0020', 'name': '线缆整理与防错校验', 'type': '加工', 'wc': 'WC-MAIN-ASM2', 'prep': 6, 'run': 12, 'out': 'MAT-ELEC-KIT', 'content': '完成线缆整理、防错和多余物清洁', 'materials': [('MAT-AUX-CLEAN-KIT', 1)], 'steps': ['完成线缆固定和防错复核', '执行多余物清洁确认']},
                {'no': '0030', 'name': '电气功能测试', 'type': '检验', 'wc': 'WC-MAIN-ASM2', 'prep': 6, 'run': 10, 'out': 'MAT-ELEC-KIT', 'content': '验证USB单元通电和输出功能', 'materials': [], 'steps': ['执行通电和输出检测', '记录功能结果并绑定条码']},
                {'no': '0040', 'name': '条码建档', 'type': '检验', 'wc': 'WC-WEIGHT-LABEL', 'prep': 4, 'run': 8, 'out': 'MAT-ELEC-KIT', 'content': '生成电气配套组件条码并归档', 'materials': [('MAT-LABEL-KIT', 1)], 'steps': ['打印组件条码', '完成条码绑定和归档']},
            ],
        },
        {
            'code': 'RT-FINAL-ASM-A01', 'name': '经济舱座椅总装工艺', 'route_spec': '装配', 'biz': 'BIZ-SEAT-MAIN-WS', 'material': 'MAT-SEAT-ECON-3S', 'proc_spec': '装配专业', 'remark': '对应控制要素中的骨架上线、扶手/靠背/餐桌安装、调试和整形',
            'ops': [
                {'no': '0010', 'name': '骨架上线', 'type': '加工', 'wc': 'WC-MAIN-LINE', 'prep': 8, 'run': 12, 'out': 'MAT-SEAT-ECON-3S', 'content': '骨架总成与托盘绑定后自动上线', 'materials': [('MAT-FRAME-ASM', 1)], 'steps': ['扫描骨架总成条码并绑定托盘', '执行自动上线和工位识别']},
                {'no': '0020', 'name': '安装锁轴与脚踏', 'type': '加工', 'wc': 'WC-MAIN-ASM1', 'prep': 10, 'run': 18, 'out': 'MAT-SEAT-ECON-3S', 'content': '安装锁轴和脚踏组件并记录扭矩', 'materials': [('MAT-LOCK-AXIS', 2), ('MAT-FOOTREST', 1), ('MAT-RAW-FASTENER-KIT', 1)], 'steps': ['安装锁轴并确认转动灵活', '完成脚踏锁紧并采集扭矩']},
                {'no': '0030', 'name': '安装扶手并测上折力', 'type': '加工', 'wc': 'WC-MAIN-ASM1', 'prep': 12, 'run': 20, 'out': 'MAT-SEAT-ECON-3S', 'content': '安装左右扶手并检测上折力', 'materials': [('MAT-ARMREST-LH', 1), ('MAT-ARMREST-RH', 1), ('MAT-RAW-FASTENER-KIT', 1)], 'steps': ['安装左右扶手并记录扭矩', '检测扶手上折力和功能一致性']},
                {'no': '0040', 'name': '电气安装', 'type': '加工', 'wc': 'WC-MAIN-ASM2', 'prep': 10, 'run': 18, 'out': 'MAT-SEAT-ECON-3S', 'content': '完成电气配套组件和勾绒带安装', 'materials': [('MAT-ELEC-KIT', 1), ('MAT-AUX-HOOK-LOOP', 1)], 'steps': ['安装电气配套组件并复核接口', '安装勾绒带及救生衣袋辅料并确认环境状态']},
                {'no': '0050', 'name': '安装靠背与餐桌', 'type': '加工', 'wc': 'WC-MAIN-ASM2', 'prep': 12, 'run': 22, 'out': 'MAT-SEAT-ECON-3S', 'content': '完成靠背总成和餐桌组件装配', 'materials': [('MAT-BACKREST-ASM', 1), ('MAT-TABLE-ASM', 1), ('MAT-RAW-FASTENER-KIT', 1)], 'steps': ['安装靠背总成并完成锁紧', '安装餐桌组件并检查动作顺畅度']},
                {'no': '0060', 'name': '调节靠背与总高', 'type': '加工', 'wc': 'WC-TUNE', 'prep': 10, 'run': 18, 'out': 'MAT-SEAT-ECON-3S', 'content': '调节靠背初始姿态并检测座椅总高', 'materials': [], 'steps': ['调节靠背初始和后倾尺寸', '检测座椅总高1143.9（0，-10）']},
                {'no': '0070', 'name': '调节餐桌速度与角度', 'type': '加工', 'wc': 'WC-TUNE', 'prep': 8, 'run': 15, 'out': 'MAT-SEAT-ECON-3S', 'content': '调节餐桌打开速度和角度', 'materials': [], 'steps': ['检测餐桌角度3±0.5°', '确认餐桌打开功能正常且速度一致']},
                {'no': '0080', 'name': '安装坐垫与安全带整形', 'type': '加工', 'wc': 'WC-MAIN-ASM2', 'prep': 12, 'run': 20, 'out': 'MAT-SEAT-ECON-3S', 'content': '完成坐垫背垫和安全带装配并整体整形', 'materials': [('MAT-CUSHION-KIT', 1), ('MAT-SAFETY-BELT', 1)], 'steps': ['安装坐垫和背垫并记录批次', '安装安全带并完成整形']},
                {'no': '0090', 'name': '安装装饰件与转入检测', 'type': '厂内转工', 'wc': 'WC-MAIN-LINE', 'prep': 6, 'run': 10, 'out': 'MAT-SEAT-ECON-3S', 'content': '安装装饰件后转入检测单元', 'materials': [('MAT-DECOR-KIT', 1)], 'steps': ['安装装饰件并确认无漏装', '转入检测单元等待称重与放行']},
            ],
        },
        {
            'code': 'RT-FINAL-CHK-A01', 'name': '经济舱座椅检测放行工艺', 'route_spec': '通用', 'biz': 'BIZ-SEAT-MAIN-WS', 'material': 'MAT-SEAT-ECON-3S', 'proc_spec': '装配专业', 'remark': '对应控制要素中的自动称重、TSO标牌、外观功能检测、影像留存和自动解锁下线',
            'ops': [
                {'no': '0010', 'name': '自动称重', 'type': '检验', 'wc': 'WC-WEIGHT-LABEL', 'prep': 6, 'run': 10, 'out': 'MAT-SEAT-ECON-3S', 'content': '自动采集座椅重量并记录', 'materials': [], 'steps': ['执行自动称重', '记录重量至小数点后一位']},
                {'no': '0020', 'name': '安装TSO标牌', 'type': '检验', 'wc': 'WC-WEIGHT-LABEL', 'prep': 6, 'run': 10, 'out': 'MAT-SEAT-ECON-3S', 'content': '打印、安装和拍照留存TSO标识', 'materials': [('MAT-TSO-PLATE', 1)], 'steps': ['打印并安装TSO标牌', '拍照记录标识信息']},
                {'no': '0030', 'name': '外观功能检测', 'type': '检验', 'wc': 'WC-FINAL-CHK', 'prep': 10, 'run': 18, 'out': 'MAT-SEAT-ECON-3S', 'content': '执行座椅尺寸、外观和功能检查', 'materials': [], 'steps': ['按尺寸检查表进行尺寸检测', '按检验文件完成外观功能检查']},
                {'no': '0040', 'name': '影像留存', 'type': '检验', 'wc': 'WC-IMAGE', 'prep': 6, 'run': 10, 'out': 'MAT-SEAT-ECON-3S', 'content': '下线前执行结构外观和总体影像留存', 'materials': [], 'steps': ['拍照记录座椅结构外观', '拍照记录下线前总体外观']},
                {'no': '0050', 'name': '自动解锁下线并入成品区', 'type': '厂内转工', 'wc': 'WC-MAIN-LINE', 'prep': 6, 'run': 10, 'out': 'MAT-SEAT-ECON-3S', 'content': '自动解锁、抓取下线并转入成品区', 'materials': [], 'steps': ['执行自动解锁和抓取下线', '转运至成品待发区并完成交接']},
            ],
        },
    ]

    for route in routes:
        a_route(route['code'], route['name'], route['route_spec'], route['biz'], route['material'], route['remark'])
        prev_no = ''
        for op in route['ops']:
            a_op(route['code'], op['no'], op['name'], op['type'], op['wc'], op['prep'], op['run'], op['out'], route['proc_spec'], op['content'])
            if prev_no:
                a_seq(route['code'], op['no'], prev_no)
            for material_code, qty in op['materials']:
                a_opmat(route['code'], op['no'], material_code, qty)
            for index, step in enumerate(op['steps'], start=1):
                a_step(route['code'], op['no'], f'{index * 10:02d}', step, step)
            prev_no = op['no']

def build() -> dict:
    reset()
    build_organizations()
    build_users()
    build_resources()
    build_materials()
    build_mboms()
    build_routes()
    apply_scene_upgrade(seed, 'aircraft_seat_economy_line', NAMESPACE)
    apply_production_orders(seed, 'aircraft_seat_economy_line', NAMESPACE)
    return seed


def summary() -> dict:
    return {'metadata': seed['metadata'], 'counts': {workbook: {sheet: len(rows) for sheet, rows in sheets.items()} for workbook, sheets in seed['workbooks'].items()}}


def main() -> None:
    build()
    ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    ASSET_PATH.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding='utf-8-sig')
    print(json.dumps(summary(), ensure_ascii=False, indent=2))
    print(f'已写入种子文件: {ASSET_PATH}')


if __name__ == '__main__':
    main()
