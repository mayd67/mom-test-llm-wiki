from __future__ import annotations

import json
import sys
from pathlib import Path

from production_order_seed import apply_production_orders
from scene_seed_upgrades import apply_scene_upgrade

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
RELEASE_TIME = '2025-03-28 08:00:00'
NAMESPACE = 'TS31S01'
VOLUME_PROFILE = '大体量版'

ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'transmission_shaft_seed_big.json'

VARIANT_SPECS = (
    ('transmission_shaft_seed.json', 'TS20S01', '标准版'),
    ('transmission_shaft_seed_big.json', 'TS31S01', '大体量版'),
    ('transmission_shaft_seed_ultra.json', 'TS42S01', '超大体量版'),
)


def new_seed() -> dict:
    return {
        'metadata': {
            'name': '传动轴单工厂机加工MOM种子',
            'industry': '通用机械加工',
            'product_family': '高精度传动轴',
            'product_model': '42CrMo高精度花键传动轴',
            'description': '面向典型机加工厂单工厂场景构建的高精度传动轴主数据，体现下料、粗半精车、外协热处理、精磨、探伤、清洗防锈和包装入库的完整链条。',
            'default_version': VER,
            'default_security': SEC,
            'volume_profile': VOLUME_PROFILE,
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
MBOM_SEQ = {0: 10, 1: 10, 2: 10, 3: 10, 4: 10}


def reset() -> None:
    global seed, MAT, PROC, EQ_USER, WC_USER, WC_SUP, WC_EQ, MBOM_SEQ
    seed = new_seed()
    MAT = {}
    PROC = set()
    EQ_USER = set()
    WC_USER = set()
    WC_SUP = set()
    WC_EQ = set()
    MBOM_SEQ = {0: 10, 1: 10, 2: 10, 3: 10, 4: 10}


def add(workbook: str, sheet: str, row: dict) -> None:
    seed['workbooks'][workbook][sheet].append(row)


def uniq(store: set, key: tuple, workbook: str, sheet: str, row: dict) -> None:
    if key not in store:
        store.add(key)
        add(workbook, sheet, row)


def next_mbom(level: int) -> int:
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


def a_user(code: str, name: str, level: str, gender: str, admin: str, biz: str, remark: str = '') -> None:
    row = {'*编号': code, '名称': name, '用户安全等级': level, '性别': gender, '行政组织编码': admin, '业务组织编码': biz}
    if remark:
        row['备注'] = remark
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


def a_tool(code: str, name: str, material_category: str, make_type: str, tooling_category: str, feature: str, spec: str = '', remark: str = '') -> None:
    row = {
        '*物料分类': TOOL_CLASS,
        '*名称': name,
        '物料类别': material_category,
        '图号': code,
        '规格': spec,
        '*制造类型': make_type,
        '计量单位': '个',
        '特性分类': feature,
        '启用批次标记': NO,
        '启用序列号标记': NO,
        '工装类别': tooling_category,
        '一次性工装标记': NO,
        '单件工装标记': NO,
        '物料阶段': STAGE,
        '发布版本时间': RELEASE_TIME,
        '发布人': '',
        '*版本号': VER,
        '*编码': code,
        '*密级': SEC,
    }
    if remark:
        row['备注'] = remark
    add(WB_FACTORY, SH_TOOL, row)


def a_wc(code: str, name: str, biz: str, wc_type: str, wc_class: str, remark: str = '') -> None:
    row = {'*名称': name, '*类型': wc_type, '*分类': wc_class, '*编码': code, '*密级': SEC, '*工厂组织': biz}
    if remark:
        row['备注'] = remark
    add(WB_FACTORY, SH_WC, row)


def l_wc_user(wc_code: str, user_code: str) -> None:
    uniq(WC_USER, (wc_code, user_code), WB_FACTORY, SH_WC_USER, {'*工作中心编码': wc_code, '*用户': user_code})


def l_wc_sup(wc_code: str, sup_code: str) -> None:
    uniq(WC_SUP, (wc_code, sup_code), WB_FACTORY, SH_WC_SUP, {'*工作中心编码': wc_code, '*供应商': sup_code})


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
    uniq(
        PROC,
        (name, wc_code),
        WB_FACTORY,
        SH_PLIB,
        {
            '序专业类型': spec,
            '*名称': name,
            '*工序类型': op_type,
            '*工作中心编码': wc_code,
            '*定额准备时间': prep,
            '*定额加工时间': run,
            '执行标记': YES,
            '*时间单位': TIME,
            '产出比': 1,
            '工序内容': content or name,
            '*密级': SEC,
        },
    )


def a_mat(code: str, name: str, category: str, make_type: str, feature: str, drawing: str, spec: str = '', unit: str = '个', remark: str = '', batch: str = YES, serial: str = NO) -> None:
    row = {
        '*物料分类': MAT_CLASS,
        '*名称': name,
        '物料类别': category,
        '图号': drawing,
        '规格': spec,
        '*制造类型': make_type,
        '计量单位': unit,
        '特性分类': feature,
        '启用批次标记': batch,
        '启用序列号标记': serial,
        '物料阶段': STAGE,
        '发布版本时间': RELEASE_TIME,
        '发布人': '',
        '*版本号': VER,
        '*编码': code,
        '*密级': SEC,
    }
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
    add(WB_PRODUCT, SH_MBOM_NODE, {
        '*MBOM版本号': VER,
        '*MBOM编码': mbom_code,
        '*物料编码': material_code,
        '物料名称': meta['name'],
        '物料图号': meta['drawing'],
        '*物料版本': VER,
        '*物料类别': meta['category'],
        '制造类型': meta['make'],
        '数量': qty,
        '计量单位': '个',
        '*层级': level,
        '*序号': next_mbom(level),
        '物料阶段': STAGE,
        '父物料编码': parent_material,
        '父物料版本': parent_version,
    })


def a_route(code: str, name: str, route_spec: str, biz: str, material_code: str, remark: str = '') -> None:
    row = {'*名称': name, '*工艺类型': ROUTE_TYPE, '工艺专业': route_spec, '物料版本号': VER, '物料编码': material_code, '*版本号': VER, '*编码': code, '*密级': SEC, '*工厂组织': biz}
    if remark:
        row['备注'] = remark
    add(WB_PRODUCT, SH_ROUTE, row)


def a_op(route_code: str, op_no: str, name: str, op_type: str, wc_code: str, prep: int, run: int, output_code: str, spec: str, content: str = '') -> None:
    add(WB_PRODUCT, SH_OP, {
        '*工序号': op_no,
        '*工序类型': op_type,
        '工序内容': content or name,
        '*工作中心编码': wc_code,
        '*定额辅助工时': prep,
        '*定额加工时间': run,
        '*时间单位': TIME,
        '执行标记': YES,
        '产出比': 1,
        '*工艺路线版本号': VER,
        '*工艺路线编码': route_code,
        '*工序名称': name,
        '产出物料版本号': VER,
        '产出物料编码': output_code,
        '工序专业类型': spec,
    })
    a_proc(name, op_type, wc_code, prep, run, spec, content)


def a_seq(route_code: str, op_no: str, prev_op: str, rel: str = SEQ_TYPE) -> None:
    add(WB_PRODUCT, SH_SEQ, {'*接续关系': rel, '*工序号': op_no, '*上道工序号': prev_op, '*工艺路线版本号': VER, '*工艺路线编码': route_code})


def a_opmat(route_code: str, op_no: str, material_code: str, qty: int) -> None:
    add(WB_PRODUCT, SH_OPMAT, {'*工艺路线版本号': VER, '*工艺路线编码': route_code, '*物料版本号': VER, '*物料编码': material_code, '*工序号': op_no, '数量': qty})


def a_step(route_code: str, op_no: str, step_no: str, name: str, content: str) -> None:
    add(WB_PRODUCT, SH_STEP, {'*工艺路线版本号': VER, '*工艺路线编码': route_code, '*工序号': op_no, '*工步序号': step_no, '*工步名称': name, '工步内容': content})


def build_organizations() -> None:
    a_admin('0', '公司', 'ADM-TS-COMP', '华川精密传动件有限公司', '华川精密')
    a_admin('ADM-TS-COMP', '工厂', 'ADM-TS-PLANT', '传动轴机加工厂', '传动轴厂')
    a_admin('ADM-TS-PLANT', '部门', 'ADM-TS-PROD', '制造部', '制造部')
    a_admin('ADM-TS-PLANT', '部门', 'ADM-TS-SUP', '质量物流部', '质物流')

    a_biz('0', 'BIZ-TS-COMP', '华川精密传动件有限公司', '华川精密', '公司', 'ADM-TS-COMP')
    a_biz('BIZ-TS-COMP', 'BIZ-TS-PLANT', '传动轴机加工厂', '传动轴厂', '工厂', 'ADM-TS-PLANT', '机械加工专业', '单工厂典型机加工场景')
    a_biz('BIZ-TS-PLANT', 'BIZ-TS-PROD', '制造部', '制造部', '部门', 'ADM-TS-PROD')
    a_biz('BIZ-TS-PLANT', 'BIZ-TS-SUP', '质量物流部', '质物流', '部门', 'ADM-TS-SUP')

    biz_rows = [
        ('BIZ-TS-PROD', 'BIZ-TS-CUT-WS', '下料车间', '下料车间', '车间', 'ADM-TS-PLANT'),
        ('BIZ-TS-PROD', 'BIZ-TS-MACH-WS', '轴类机加车间', '机加车间', '车间', 'ADM-TS-PLANT'),
        ('BIZ-TS-PROD', 'BIZ-TS-FIN-WS', '清洗防锈车间', '后处理车间', '车间', 'ADM-TS-PLANT'),
        ('BIZ-TS-SUP', 'BIZ-TS-QA-WS', '质量检测车间', '质检车间', '车间', 'ADM-TS-PLANT'),
        ('BIZ-TS-SUP', 'BIZ-TS-WH-WS', '仓储配送车间', '仓储车间', '车间', 'ADM-TS-PLANT'),
        ('BIZ-TS-CUT-WS', 'BIZ-TS-CUT-SEC', '下料工段', '下料工段', '工段', 'ADM-TS-PLANT'),
        ('BIZ-TS-MACH-WS', 'BIZ-TS-ROUGH-SEC', '粗车工段', '粗车工段', '工段', 'ADM-TS-PLANT'),
        ('BIZ-TS-MACH-WS', 'BIZ-TS-SEMI-SEC', '半精车工段', '半精工段', '工段', 'ADM-TS-PLANT'),
        ('BIZ-TS-MACH-WS', 'BIZ-TS-SPLINE-SEC', '花键螺纹工段', '花键工段', '工段', 'ADM-TS-PLANT'),
        ('BIZ-TS-MACH-WS', 'BIZ-TS-HT-SEC', '热处理协同工段', '热协工段', '工段', 'ADM-TS-PLANT'),
        ('BIZ-TS-MACH-WS', 'BIZ-TS-GRIND-SEC', '精磨工段', '精磨工段', '工段', 'ADM-TS-PLANT'),
        ('BIZ-TS-FIN-WS', 'BIZ-TS-FINISH-SEC', '清洗防锈工段', '后处理工段', '工段', 'ADM-TS-PLANT'),
        ('BIZ-TS-QA-WS', 'BIZ-TS-QA-SEC', '质量检测工段', '质检工段', '工段', 'ADM-TS-PLANT'),
        ('BIZ-TS-WH-WS', 'BIZ-TS-WH-SEC', '仓储配送工段', '仓储工段', '工段', 'ADM-TS-PLANT'),
        ('BIZ-TS-CUT-SEC', 'BIZ-TS-CUT-TEAM', '下料甲班', '下料甲班', '班组', 'ADM-TS-PLANT'),
        ('BIZ-TS-ROUGH-SEC', 'BIZ-TS-ROUGH-TEAM', '粗车甲班', '粗车甲班', '班组', 'ADM-TS-PLANT'),
        ('BIZ-TS-SEMI-SEC', 'BIZ-TS-SEMI-TEAM', '半精车甲班', '半精甲班', '班组', 'ADM-TS-PLANT'),
        ('BIZ-TS-SPLINE-SEC', 'BIZ-TS-SPLINE-TEAM', '花键螺纹甲班', '花键甲班', '班组', 'ADM-TS-PLANT'),
        ('BIZ-TS-HT-SEC', 'BIZ-TS-HT-TEAM', '热处理协同班', '热协班', '班组', 'ADM-TS-PLANT'),
        ('BIZ-TS-GRIND-SEC', 'BIZ-TS-GRIND-TEAM', '精磨甲班', '精磨甲班', '班组', 'ADM-TS-PLANT'),
        ('BIZ-TS-FINISH-SEC', 'BIZ-TS-FINISH-TEAM', '清洗防锈甲班', '后处理甲班', '班组', 'ADM-TS-PLANT'),
        ('BIZ-TS-QA-SEC', 'BIZ-TS-QA-TEAM', '检测甲班', '检测甲班', '班组', 'ADM-TS-PLANT'),
        ('BIZ-TS-WH-SEC', 'BIZ-TS-WH-TEAM', '仓储配送甲班', '仓储甲班', '班组', 'ADM-TS-PLANT'),
    ]
    for parent, code, name, short, org_type, admin in biz_rows:
        a_biz(parent, code, name, short, org_type, admin)


def build_users() -> None:
    users = [
        ('U-TS-001', '郭明远', '一般', '男', 'ADM-TS-PLANT', 'BIZ-TS-PLANT', '工厂厂长'),
        ('U-TS-002', '顾辰逸', '一般', '男', 'ADM-TS-PROD', 'BIZ-TS-PROD', '生产计划员'),
        ('U-TS-003', '林知远', '一般', '男', 'ADM-TS-PROD', 'BIZ-TS-PROD', '工艺总师'),
        ('U-TS-004', '沈沐航', '一般', '男', 'ADM-TS-PROD', 'BIZ-TS-MACH-WS', '工艺工程师'),
        ('U-TS-005', '周可然', '一般', '女', 'ADM-TS-PROD', 'BIZ-TS-MACH-WS', '工装工程师'),
        ('U-TS-006', '唐书宁', '一般', '女', 'ADM-TS-SUP', 'BIZ-TS-QA-WS', '质量主管'),
        ('U-TS-007', '郑星宇', '一般', '男', 'ADM-TS-SUP', 'BIZ-TS-WH-SEC', '仓库管理员'),
        ('U-TS-008', '韩景川', '一般', '男', 'ADM-TS-PROD', 'BIZ-TS-HT-SEC', '外协管理员'),
        ('U-TS-009', '马清越', '一般', '男', 'ADM-TS-PROD', 'BIZ-TS-MACH-WS', '设备维修工'),
        ('U-TS-010', '薛云桐', '一般', '女', 'ADM-TS-PROD', 'BIZ-TS-MACH-WS', '设备保养员'),
    ]
    for row in users:
        a_user(*row)


def build_resources() -> None:
    suppliers = [
        ('SUP-STEEL-01', '华东优钢材料有限公司', '华东优钢', '42CrMo圆钢主供方'),
        ('SUP-HT-01', '嘉信热处理服务有限公司', '嘉信热处', '调质和感应淬火外协供应商'),
        ('SUP-PKG-01', '辰丰包装材料有限公司', '辰丰包装', '防锈包装与周转件供应商'),
    ]
    for row in suppliers:
        a_sup(*row)

    equipment = [
        ('EQ-CUT-SAW-01', '数控带锯床', 'GZ4235', 'BIZ-TS-CUT-SEC', YES, '圆钢锯切下料'),
        ('EQ-CUT-LATHE-01', '端面中心孔车床', 'CJ0632', 'BIZ-TS-CUT-SEC', NO, '端面和中心孔加工'),
        ('EQ-ROUGH-CNC-01', '粗车数控车床', 'CK6150', 'BIZ-TS-ROUGH-SEC', YES, '粗车外圆与台阶'),
        ('EQ-ROUGH-CNC-02', '粗车数控车床', 'CK6150', 'BIZ-TS-ROUGH-SEC', NO, '粗车并行设备'),
        ('EQ-SEMI-CNC-01', '半精车数控车床', 'CK6136', 'BIZ-TS-SEMI-SEC', YES, '半精车轴肩与退刀槽'),
        ('EQ-SPLINE-01', '花键滚压机', 'SK7632', 'BIZ-TS-SPLINE-SEC', NO, '花键滚压成形'),
        ('EQ-THREAD-01', '螺纹滚压机', 'ZG-30', 'BIZ-TS-SPLINE-SEC', NO, '外螺纹加工'),
        ('EQ-STRAIGHT-01', '液压校直机', 'YJ-60', 'BIZ-TS-HT-SEC', NO, '热处理回厂校直'),
        ('EQ-HARD-01', '洛氏硬度计', 'HR-150A', 'BIZ-TS-HT-SEC', NO, '热处理后硬度检验'),
        ('EQ-GRIND-01', '外圆磨床', 'M1432B', 'BIZ-TS-GRIND-SEC', YES, '外圆和轴颈精磨'),
        ('EQ-GRIND-02', '数控外圆磨床', 'MK1320', 'BIZ-TS-GRIND-SEC', NO, '精磨并行设备'),
        ('EQ-CLEAN-01', '超声波清洗机', 'QX-900', 'BIZ-TS-FINISH-SEC', NO, '清洗去油和烘干'),
        ('EQ-MARK-01', '激光打标机', 'LM-20', 'BIZ-TS-FINISH-SEC', NO, '追溯码打标'),
        ('EQ-MPI-01', '磁粉探伤机', 'CDG-800', 'BIZ-TS-QA-SEC', YES, '表面裂纹探伤'),
        ('EQ-CMM-01', '圆跳动检测仪', 'RT-300', 'BIZ-TS-QA-SEC', NO, '圆跳动和同轴度终检'),
    ]
    for row in equipment:
        a_eq(*row)

    tools = [
        ('TOOL-SHAFT-FIX-01', '传动轴粗车组合夹具', CAT_KIT, MAKE_SELF, '专用工装', FEATURE_KEY, '适配42CrMo轴类粗车', '粗车外圆与台阶定位夹具'),
        ('TOOL-CENTER-FIX-01', '中心孔定位夹具', CAT_KIT, MAKE_SELF, '专用工装', FEATURE_IMPORTANT, '端面中心孔组合夹具', '端面与中心孔装夹工装'),
        ('TOOL-SPLINE-FIX-01', '花键滚压定位胎具', CAT_KIT, MAKE_SELF, '专用工装', FEATURE_IMPORTANT, '花键滚压专用胎具', '花键滚压和螺纹加工定位工装'),
        ('TOOL-GRIND-GAUGE-01', '外圆精磨检具', CAT_PART, MAKE_BUY, '通用工具', FEATURE_KEY, '轴颈尺寸检具', '精磨尺寸快速复核检具'),
        ('TOOL-MPI-RACK-01', '探伤周转架', CAT_KIT, MAKE_SELF, '专用工装', FEATURE_NORMAL, '探伤周转架', '探伤和终检周转工装'),
        ('TOOL-SHAFT-CART-01', '传动轴周转车', CAT_KIT, MAKE_SELF, '专用工装', FEATURE_NORMAL, '轴类转运车', '线边周转和包装转运工装'),
    ]
    for row in tools:
        a_tool(*row)

    workcenters = [
        ('WC-CUT', '下料中心', 'BIZ-TS-CUT-SEC', '组织', '加工', '圆钢锯切和端面中心孔工序'),
        ('WC-ROUGH', '粗车中心', 'BIZ-TS-ROUGH-SEC', '组织', '加工', '粗车外圆和台阶'),
        ('WC-SEMI', '半精车中心', 'BIZ-TS-SEMI-SEC', '组织', '加工', '半精车轴肩和退刀槽'),
        ('WC-SPLINE', '花键螺纹中心', 'BIZ-TS-SPLINE-SEC', '组织', '加工', '花键滚压和螺纹滚压'),
        ('WC-HEAT-OUT', '外协热处理中心', 'BIZ-TS-HT-SEC', '外委', '加工', '委外执行调质和感应淬火'),
        ('WC-HT-INSP', '热处理回厂复检中心', 'BIZ-TS-HT-SEC', '组织', '检验', '回厂校直和硬度复检'),
        ('WC-GRIND', '精磨中心', 'BIZ-TS-GRIND-SEC', '组织', '加工', '外圆精磨和轴颈精磨'),
        ('WC-FINISH', '清洗防锈中心', 'BIZ-TS-FINISH-SEC', '组织', '加工', '清洗烘干和防锈打标'),
        ('WC-QA', '终检中心', 'BIZ-TS-QA-SEC', '组织', '检验', '磁粉探伤和圆跳动终检'),
        ('WC-PACK', '包装入库中心', 'BIZ-TS-WH-SEC', '组织', '加工', '包装、贴标和入成品库'),
    ]
    for row in workcenters:
        a_wc(*row)

    wc_eq_relations = [
        ('WC-CUT', 'EQ-CUT-SAW-01'), ('WC-CUT', 'EQ-CUT-LATHE-01'),
        ('WC-ROUGH', 'EQ-ROUGH-CNC-01'), ('WC-ROUGH', 'EQ-ROUGH-CNC-02'),
        ('WC-SEMI', 'EQ-SEMI-CNC-01'),
        ('WC-SPLINE', 'EQ-SPLINE-01'), ('WC-SPLINE', 'EQ-THREAD-01'),
        ('WC-HT-INSP', 'EQ-STRAIGHT-01'), ('WC-HT-INSP', 'EQ-HARD-01'),
        ('WC-GRIND', 'EQ-GRIND-01'), ('WC-GRIND', 'EQ-GRIND-02'),
        ('WC-FINISH', 'EQ-CLEAN-01'), ('WC-FINISH', 'EQ-MARK-01'),
        ('WC-QA', 'EQ-MPI-01'), ('WC-QA', 'EQ-CMM-01'),
    ]
    for wc_code, eq_code in wc_eq_relations:
        l_wc_eq(wc_code, eq_code)

    l_wc_sup('WC-HEAT-OUT', 'SUP-HT-01')

    base_relations = [
        ('WC-ROUGH', 'U-TS-004'), ('WC-GRIND', 'U-TS-004'), ('WC-CUT', 'U-TS-005'), ('WC-SPLINE', 'U-TS-005'),
        ('WC-QA', 'U-TS-006'), ('WC-PACK', 'U-TS-007'), ('WC-HEAT-OUT', 'U-TS-008'), ('WC-HT-INSP', 'U-TS-008'),
        ('WC-ROUGH', 'U-TS-009'), ('WC-GRIND', 'U-TS-010'),
    ]
    for wc_code, user_code in base_relations:
        l_wc_user(wc_code, user_code)

    eq_user_relations = [
        ('EQ-ROUGH-CNC-01', 'U-TS-009'), ('EQ-GRIND-01', 'U-TS-010'), ('EQ-MPI-01', 'U-TS-006'), ('EQ-CUT-SAW-01', 'U-TS-005'),
    ]
    for eq_code, user_code in eq_user_relations:
        l_eq_user(eq_code, user_code)

    warehouses = [
        ('WH-TS-RAW', '原材料库', 'BIZ-TS-WH-SEC', 'ERP一级库', '圆钢原料收料和存储'),
        ('WH-TS-WIP', '轴类在制库', 'BIZ-TS-WH-SEC', '车间二级库', '粗车半精车在制周转'),
        ('WH-TS-HT', '热处理回厂待检库', 'BIZ-TS-WH-SEC', '车间二级库', '热处理回厂待检和隔离'),
        ('WH-TS-FIN', '成品库', 'BIZ-TS-WH-SEC', 'ERP一级库', '终检合格成品入库'),
        ('WH-TS-AUX', '辅料库', 'BIZ-TS-WH-SEC', 'ERP二级库', '刀具耗材、防锈包装和检验辅料'),
    ]
    for code, name, biz, biz_type, remark in warehouses:
        a_wh(code, name, biz, biz_type, remark=remark)

    locations = [
        ('LOC-TS-RAW-01', '圆钢原料区', 'BIZ-TS-WH-SEC', 'WH-TS-RAW'),
        ('LOC-TS-WIP-01', '粗加工周转区', 'BIZ-TS-WH-SEC', 'WH-TS-WIP'),
        ('LOC-TS-HT-01', '热处理回厂待检区', 'BIZ-TS-WH-SEC', 'WH-TS-HT'),
        ('LOC-TS-FIN-01', '成品存放区', 'BIZ-TS-WH-SEC', 'WH-TS-FIN'),
        ('LOC-TS-AUX-01', '刀具辅料区', 'BIZ-TS-WH-SEC', 'WH-TS-AUX'),
    ]
    for code, name, biz, warehouse in locations:
        a_loc(code, name, biz, warehouse)


def build_materials() -> None:
    materials = [
        ('MAT-BAR-42CRMO', '42CrMo圆钢料', CAT_RAW, MAKE_BUY, FEATURE_KEY, 'BAR-42CRMO', 'Φ65×6000mm', '个', '传动轴原材料圆钢'),
        ('MAT-SHAFT-BLANK', '传动轴下料件', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'TS-BLANK', 'Φ65×820mm', '个', '圆钢锯切后的下料毛坯'),
        ('MAT-SHAFT-ROUGH', '传动轴粗加工件', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'TS-ROUGH', '粗车后阶段件', '个', '完成粗车后的阶段件'),
        ('MAT-SHAFT-SEMI', '传动轴半精加工件', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'TS-SEMI', '半精车后阶段件', '个', '完成半精车和花键预加工后的阶段件'),
        ('MAT-SHAFT-HT', '传动轴热处理后件', CAT_PART, MAKE_SELF, FEATURE_KEY, 'TS-HT', '调质后阶段件', '个', '外协热处理返回的阶段件'),
        ('MAT-SHAFT-FIN', '高精度花键传动轴', CAT_PART, MAKE_SELF, FEATURE_KEY, 'TS-FIN', '成品轴', '个', '终检合格后的最终交付件'),
        ('MAT-CUT-OIL', '锯切冷却液', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'CUT-OIL', '20L/桶', '个', '下料锯切冷却耗材'),
        ('MAT-TURN-INSERT', '数控车削刀片包', CAT_KIT, MAKE_BUY, FEATURE_NORMAL, 'TURN-INSERT', 'CNMG120408', '个', '粗半精车刀具耗材'),
        ('MAT-GRIND-WHEEL', '外圆磨砂轮', CAT_PART, MAKE_BUY, FEATURE_NORMAL, 'GRIND-WHEEL', 'WA46K', '个', '精磨耗材'),
        ('MAT-MPI-POWDER', '磁粉探伤耗材包', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'MPI-POWDER', '磁悬液+反差剂', '个', '终检探伤耗材'),
        ('MAT-CLEAN-AGENT', '轴类清洗剂', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'CLEAN-AGENT', '水基清洗剂', '个', '清洗去油耗材'),
        ('MAT-RUST-OIL', '防锈油', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'RUST-OIL', '薄膜防锈油', '个', '终检后防锈处理'),
        ('MAT-PKG-KIT', '包装防护组件', CAT_KIT, MAKE_BUY, FEATURE_NORMAL, 'PKG-KIT', '护套+瓦楞盒+缓冲材料', '个', '包装入库防护件'),
        ('MAT-TRACE-LABEL', '追溯标签包', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'TRACE-LABEL', '二维码标签', '个', '打标和追溯标签'),
    ]
    for code, name, category, make_type, feature, drawing, spec, unit, remark in materials:
        a_mat(code, name, category, make_type, feature, drawing, spec=spec, unit=unit, remark=remark)


def build_mboms() -> None:
    a_mbom('MBOM-SHAFT-A01', 'MAT-SHAFT-FIN', '高精度花键传动轴MBOM', '单工厂典型轴类机加工结构')
    a_mbom_node('MBOM-SHAFT-A01', 0, 'MAT-SHAFT-FIN', 1)
    a_mbom_node('MBOM-SHAFT-A01', 1, 'MAT-SHAFT-HT', 1, 'MAT-SHAFT-FIN', VER)
    a_mbom_node('MBOM-SHAFT-A01', 2, 'MAT-SHAFT-SEMI', 1, 'MAT-SHAFT-HT', VER)
    a_mbom_node('MBOM-SHAFT-A01', 3, 'MAT-SHAFT-ROUGH', 1, 'MAT-SHAFT-SEMI', VER)
    a_mbom_node('MBOM-SHAFT-A01', 4, 'MAT-SHAFT-BLANK', 1, 'MAT-SHAFT-ROUGH', VER)
    a_mbom_node('MBOM-SHAFT-A01', 1, 'MAT-PKG-KIT', 1, 'MAT-SHAFT-FIN', VER)
    a_mbom_node('MBOM-SHAFT-A01', 1, 'MAT-TRACE-LABEL', 1, 'MAT-SHAFT-FIN', VER)


def build_routes() -> None:
    route = {
        'code': 'RT-SHAFT-MACH-A01',
        'name': '传动轴单工厂机加工艺',
        'route_spec': '机加',
        'biz': 'BIZ-TS-PLANT',
        'material': 'MAT-SHAFT-FIN',
        'proc_spec': '机械加工专业',
        'remark': '覆盖典型轴类件下料、粗半精车、外协热处理、精磨、终检和包装入库全流程',
        'ops': [
            {'no': '0010', 'name': '圆钢领料与锯切下料', 'type': '加工', 'wc': 'WC-CUT', 'prep': 12, 'run': 30, 'out': 'MAT-SHAFT-BLANK', 'content': '从原材料库领料并完成圆钢锯切下料', 'materials': [('MAT-BAR-42CRMO', 1), ('MAT-CUT-OIL', 1)], 'steps': ['核对圆钢炉批号和规格', '执行锯切并首件复测长度']},
            {'no': '0020', 'name': '端面车削与中心孔加工', 'type': '加工', 'wc': 'WC-CUT', 'prep': 10, 'run': 24, 'out': 'MAT-SHAFT-BLANK', 'content': '建立端面与中心孔定位基准', 'materials': [('MAT-SHAFT-BLANK', 1), ('MAT-TURN-INSERT', 1)], 'steps': ['装夹下料件并校正跳动', '加工端面和双端中心孔']},
            {'no': '0030', 'name': '粗车外圆与台阶', 'type': '加工', 'wc': 'WC-ROUGH', 'prep': 14, 'run': 42, 'out': 'MAT-SHAFT-ROUGH', 'content': '完成粗车外圆、台阶和余量控制', 'materials': [('MAT-SHAFT-BLANK', 1), ('MAT-TURN-INSERT', 1)], 'steps': ['粗车外圆与轴肩台阶', '复核关键余量并转序']},
            {'no': '0040', 'name': '半精车轴肩与退刀槽', 'type': '加工', 'wc': 'WC-SEMI', 'prep': 12, 'run': 36, 'out': 'MAT-SHAFT-SEMI', 'content': '完成半精车轴肩、挡肩和退刀槽', 'materials': [('MAT-SHAFT-ROUGH', 1), ('MAT-TURN-INSERT', 1)], 'steps': ['半精车主轴颈和安装段', '加工退刀槽并复测尺寸']},
            {'no': '0050', 'name': '花键滚压与螺纹加工', 'type': '加工', 'wc': 'WC-SPLINE', 'prep': 12, 'run': 32, 'out': 'MAT-SHAFT-SEMI', 'content': '完成花键滚压和外螺纹成形', 'materials': [('MAT-SHAFT-SEMI', 1), ('MAT-TURN-INSERT', 1)], 'steps': ['执行花键滚压并检首件', '完成端部螺纹成形和去毛刺']},
            {'no': '0060', 'name': '外协调质与感应淬火', 'type': '外委', 'wc': 'WC-HEAT-OUT', 'prep': 10, 'run': 180, 'out': 'MAT-SHAFT-HT', 'content': '委外执行调质和感应淬火并回厂', 'materials': [('MAT-SHAFT-SEMI', 1)], 'steps': ['生成外协批次与流转卡', '回厂接收并核对热处理报告']},
            {'no': '0070', 'name': '校直与硬度复检', 'type': '检验', 'wc': 'WC-HT-INSP', 'prep': 8, 'run': 22, 'out': 'MAT-SHAFT-HT', 'content': '完成热处理回厂校直和硬度复检', 'materials': [('MAT-SHAFT-HT', 1)], 'steps': ['执行轴类校直并记录偏摆', '复测硬度和热处理状态']},
            {'no': '0080', 'name': '外圆精磨与轴颈精磨', 'type': '加工', 'wc': 'WC-GRIND', 'prep': 14, 'run': 44, 'out': 'MAT-SHAFT-FIN', 'content': '完成关键外圆和轴颈精磨', 'materials': [('MAT-SHAFT-HT', 1), ('MAT-GRIND-WHEEL', 1)], 'steps': ['精磨关键外圆和轴颈', '复核同轴度与表面粗糙度']},
            {'no': '0090', 'name': '清洗防锈与激光打标', 'type': '加工', 'wc': 'WC-FINISH', 'prep': 10, 'run': 20, 'out': 'MAT-SHAFT-FIN', 'content': '完成清洗烘干、防锈和追溯打标', 'materials': [('MAT-SHAFT-FIN', 1), ('MAT-CLEAN-AGENT', 1), ('MAT-RUST-OIL', 1), ('MAT-TRACE-LABEL', 1)], 'steps': ['超声波清洗并烘干', '执行防锈处理和激光打标']},
            {'no': '0100', 'name': '磁粉探伤与圆跳动终检', 'type': '检验', 'wc': 'WC-QA', 'prep': 12, 'run': 24, 'out': 'MAT-SHAFT-FIN', 'content': '完成磁粉探伤和圆跳动终检放行', 'materials': [('MAT-SHAFT-FIN', 1), ('MAT-MPI-POWDER', 1)], 'steps': ['执行磁粉探伤排查裂纹', '检测圆跳动并签发放行结果']},
            {'no': '0110', 'name': '包装入库', 'type': '厂内转工', 'wc': 'WC-PACK', 'prep': 8, 'run': 14, 'out': 'MAT-SHAFT-FIN', 'content': '完成防护包装并转入成品库', 'materials': [('MAT-SHAFT-FIN', 1), ('MAT-PKG-KIT', 1), ('MAT-TRACE-LABEL', 1)], 'steps': ['安装包装防护组件并贴箱唛', '转入成品库指定货位']},
        ],
    }

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


def build_variant(namespace: str, volume_profile: str) -> dict:
    reset()
    build_organizations()
    build_users()
    build_resources()
    build_materials()
    build_mboms()
    build_routes()
    apply_scene_upgrade(seed, 'transmission_shaft', namespace, volume_profile=volume_profile)
    apply_production_orders(seed, 'transmission_shaft', namespace)
    return seed


def build() -> dict:
    return build_variant(NAMESPACE, VOLUME_PROFILE)


def summarize(seed_data: dict) -> dict:
    return {'metadata': seed_data['metadata'], 'counts': {workbook: {sheet: len(rows) for sheet, rows in sheets.items()} for workbook, sheets in seed_data['workbooks'].items()}}


def summary() -> dict:
    return summarize(seed)


def main() -> None:
    ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    for asset_name, namespace, volume_profile in VARIANT_SPECS:
        variant_seed = build_variant(namespace, volume_profile)
        asset_path = ASSET_PATH.parent / asset_name
        asset_path.write_text(json.dumps(variant_seed, ensure_ascii=False, indent=2), encoding='utf-8-sig')
        print(json.dumps(summarize(variant_seed), ensure_ascii=False, indent=2))
        print(f'已写入种子文件: {asset_path}')


if __name__ == '__main__':
    main()
