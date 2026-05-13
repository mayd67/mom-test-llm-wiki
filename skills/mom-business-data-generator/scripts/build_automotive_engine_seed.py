from __future__ import annotations

import json
import sys
from pathlib import Path

from scene_seed_upgrades import apply_scene_upgrade
from tooling_strategy_profiles import apply_profile
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
CAT_SPARE = '设备备件'
MAKE_SELF = '自制件'
MAKE_BUY = '外购件'
MAKE_BOTH = '自制+外购'
FEATURE_KEY = '关键件'
FEATURE_IMPORTANT = '重要件'
FEATURE_NORMAL = '一般件'
STAGE = '量产'
SEQ_TYPE = 'ES'
RELEASE_TIME = '2025-03-01 08:00:00'
RELEASE_USER = ''
NAMESPACE = 'AE20T01'

ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'automotive_engine_seed.json'
VARIANT_SPECS = [
    ('automotive_engine_seed.json', 'AE20T01', '标准版'),
    ('automotive_engine_seed_big.json', 'AE31T01', '大体量版'),
    ('automotive_engine_seed_ultra.json', 'AE42T01', '超大体量版'),
]


def new_seed() -> dict:
    return {
        'metadata': {
            'name': '汽车发动机MOM专业版种子',
            'industry': '汽车发动机',
            'product_family': '乘用车动力总成',
            'product_model': '2.0T缸内直喷涡轮增压汽油发动机',
            'description': '面向售前演示与模板导入的专业版汽车发动机主数据，覆盖多工厂协同、外协热处理、完整组织层级、资源、MBOM与工艺路线。',
            'default_version': VER,
            'default_security': SEC,
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
    row = {
        '*物料分类': TOOL_CLASS,
        '*名称': name,
        '物料类别': material_category,
        '图号': code,
        '型号': model,
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
        '发布人': RELEASE_USER,
        '*版本号': VER,
        '*编码': code,
        '*密级': SEC,
    }
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


def l_wc_sup(wc_code: str, sup_code: str) -> None:
    uniq(WC_SUP, (wc_code, sup_code), WB_FACTORY, SH_WC_SUP, {'*工作中心编码': wc_code, '*供应商': sup_code})


def l_wc_eq(wc_code: str, eq_code: str) -> None:
    uniq(WC_EQ, (wc_code, eq_code), WB_FACTORY, SH_WC_EQ, {'*设备编码': eq_code, '*工作中心编码': wc_code})


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


def a_mat(code: str, name: str, category: str, make_type: str, feature: str, drawing: str, model: str = '', spec: str = '', remark: str = '', batch: str = YES, serial: str = NO) -> None:
    row = {
        '*物料分类': MAT_CLASS,
        '*名称': name,
        '物料类别': category,
        '图号': drawing,
        '型号': model,
        '规格': spec,
        '*制造类型': make_type,
        '计量单位': '个',
        '特性分类': feature,
        '启用批次标记': batch,
        '启用序列号标记': serial,
        '物料阶段': STAGE,
        '发布版本时间': RELEASE_TIME,
        '发布人': RELEASE_USER,
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
    row = {
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
    }
    add(WB_PRODUCT, SH_MBOM_NODE, row)


def a_route(code: str, name: str, route_spec: str, biz: str, material_code: str, remark: str = '') -> None:
    row = {'*名称': name, '*工艺类型': ROUTE_TYPE, '工艺专业': route_spec, '物料版本号': VER, '物料编码': material_code, '*版本号': VER, '*编码': code, '*密级': SEC, '*工厂组织': biz}
    if remark:
        row['备注'] = remark
    add(WB_PRODUCT, SH_ROUTE, row)


def a_op(route_code: str, op_no: str, name: str, op_type: str, wc_code: str, prep: int, run: int, output_code: str, spec: str, content: str = '') -> None:
    add(
        WB_PRODUCT,
        SH_OP,
        {
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
        },
    )
    a_proc(name, op_type, wc_code, prep, run, spec, content)


def a_seq(route_code: str, op_no: str, prev_op: str, rel: str = SEQ_TYPE) -> None:
    add(WB_PRODUCT, SH_SEQ, {'*接续关系': rel, '*工序号': op_no, '*上道工序号': prev_op, '*工艺路线版本号': VER, '*工艺路线编码': route_code})


def a_opmat(route_code: str, op_no: str, material_code: str, qty: int) -> None:
    add(WB_PRODUCT, SH_OPMAT, {'*工艺路线版本号': VER, '*工艺路线编码': route_code, '*物料版本号': VER, '*物料编码': material_code, '*工序号': op_no, '数量': qty})


def a_step(route_code: str, op_no: str, step_no: str, name: str, content: str = '') -> None:
    add(WB_PRODUCT, SH_STEP, {'*工艺路线版本号': VER, '*工艺路线编码': route_code, '*工序号': op_no, '*工步序号': step_no, '*工步名称': name, '工步内容': content or name})


def build_organizations() -> None:
    admins = [
        ('0', '公司', 'ADM-POWER', '华擎动力总成有限公司', '华擎动力', '集团级动力总成制造主体'),
        ('ADM-POWER', '工厂', 'ADM-CAST-PLANT', '铸造工厂', '铸造工厂', '负责缸体缸盖毛坯铸造'),
        ('ADM-POWER', '工厂', 'ADM-MACH-PLANT', '机加工厂', '机加工厂', '负责缸体缸盖曲轴连杆精密机加工'),
        ('ADM-POWER', '工厂', 'ADM-ASM-PLANT', '总装工厂', '总装工厂', '负责缸盖、短缸、长缸和整机装配'),
        ('ADM-POWER', '工厂', 'ADM-TEST-PLANT', '试验工厂', '试验工厂', '负责冷试、热试和EOL放行'),
        ('ADM-POWER', '部门', 'ADM-TECH', '工艺技术部', '工艺技术', '负责工艺规划和工装定额管理'),
        ('ADM-POWER', '部门', 'ADM-QA', '质量管理部', '质量管理', '负责质量策划与过程质量放行'),
        ('ADM-POWER', '部门', 'ADM-SCM', '供应链管理部', '供应链', '负责采购、供应商和外协管理'),
        ('ADM-POWER', '部门', 'ADM-PMC', '计划物流部', '计划物流', '负责主计划与物流协调'),
        ('ADM-POWER', '部门', 'ADM-EAM', '设备管理部', '设备管理', '负责设备维修与保养'),
    ]
    for row in admins:
        a_admin(*row)

    biz_rows = [
        ('0', 'BIZ-POWER', '动力总成制造中心', '动力中心', '公司', 'ADM-POWER', '', '多工厂协同的动力总成业务顶层组织'),
        ('BIZ-POWER', 'BIZ-CAST', '铸造工厂', '铸造厂', '工厂', 'ADM-CAST-PLANT', '机械加工专业', '负责缸体缸盖低压铸造与毛坯检验'),
        ('BIZ-CAST', 'BIZ-CAST-BLOCK-WS', '缸体铸造车间', '缸体铸造', '车间', 'ADM-CAST-PLANT', '', '缸体低压铸造与清理'),
        ('BIZ-CAST-BLOCK-WS', 'BIZ-CAST-BLOCK-SEC', '缸体铸造工段', '缸体工段', '工段', 'ADM-CAST-PLANT', '', '缸体制芯、浇注和切冒口'),
        ('BIZ-CAST-BLOCK-SEC', 'BIZ-CAST-BLOCK-A', '缸体铸造甲班', '缸体甲班', '班组', 'ADM-CAST-PLANT', '', '缸体铸造执行班组'),
        ('BIZ-CAST', 'BIZ-CAST-HEAD-WS', '缸盖铸造车间', '缸盖铸造', '车间', 'ADM-CAST-PLANT', '', '缸盖低压铸造与清理'),
        ('BIZ-CAST-HEAD-WS', 'BIZ-CAST-HEAD-SEC', '缸盖铸造工段', '缸盖工段', '工段', 'ADM-CAST-PLANT', '', '缸盖制芯、浇注和X光检验'),
        ('BIZ-CAST-HEAD-SEC', 'BIZ-CAST-HEAD-A', '缸盖铸造甲班', '缸盖甲班', '班组', 'ADM-CAST-PLANT', '', '缸盖铸造执行班组'),
        ('BIZ-CAST', 'BIZ-CAST-QA', '铸造质量室', '铸造质量', '部门', 'ADM-QA', '', '铸造过程质量控制'),
        ('BIZ-POWER', 'BIZ-MACH', '机加工厂', '机加工厂', '工厂', 'ADM-MACH-PLANT', '机械加工专业', '负责关键件精密机加工与外协热处理协同'),
        ('BIZ-MACH', 'BIZ-MACH-BLOCK-WS', '缸体机加车间', '缸体机加', '车间', 'ADM-MACH-PLANT', '', '缸体基准面、缸孔和主轴承座加工'),
        ('BIZ-MACH-BLOCK-WS', 'BIZ-MACH-BLOCK-SEC', '缸体精加工工段', '缸体精加', '工段', 'ADM-MACH-PLANT', '', '缸孔珩磨和清洗终检'),
        ('BIZ-MACH-BLOCK-SEC', 'BIZ-MACH-BLOCK-A', '缸体机加甲班', '缸体甲班', '班组', 'ADM-MACH-PLANT', '', '缸体加工执行班组'),
        ('BIZ-MACH', 'BIZ-MACH-HEAD-WS', '缸盖机加车间', '缸盖机加', '车间', 'ADM-MACH-PLANT', '', '燃烧室、导管和凸轮孔系加工'),
        ('BIZ-MACH-HEAD-WS', 'BIZ-MACH-HEAD-SEC', '缸盖精加工工段', '缸盖精加', '工段', 'ADM-MACH-PLANT', '', '缸盖火面加工、气密试验与终检'),
        ('BIZ-MACH-HEAD-SEC', 'BIZ-MACH-HEAD-A', '缸盖机加甲班', '缸盖甲班', '班组', 'ADM-MACH-PLANT', '', '缸盖加工执行班组'),
        ('BIZ-MACH', 'BIZ-MACH-CRANK-WS', '曲轴机加车间', '曲轴机加', '车间', 'ADM-MACH-PLANT', '', '曲轴车削、磨削与动平衡'),
        ('BIZ-MACH-CRANK-WS', 'BIZ-MACH-CRANK-SEC', '曲轴加工工段', '曲轴工段', '工段', 'ADM-MACH-PLANT', '', '曲轴精磨、外协热处理和探伤'),
        ('BIZ-MACH-CRANK-SEC', 'BIZ-MACH-CRANK-A', '曲轴机加甲班', '曲轴甲班', '班组', 'ADM-MACH-PLANT', '', '曲轴加工执行班组'),
        ('BIZ-MACH', 'BIZ-MACH-CONROD-WS', '连杆机加车间', '连杆机加', '车间', 'ADM-MACH-PLANT', '', '连杆孔系加工与分组选配'),
        ('BIZ-MACH-CONROD-WS', 'BIZ-MACH-CONROD-SEC', '连杆加工工段', '连杆工段', '工段', 'ADM-MACH-PLANT', '', '连杆裂解、镗珩与称重配对'),
        ('BIZ-MACH-CONROD-SEC', 'BIZ-MACH-CONROD-A', '连杆机加甲班', '连杆甲班', '班组', 'ADM-MACH-PLANT', '', '连杆加工执行班组'),
        ('BIZ-MACH', 'BIZ-MACH-QA', '机加质量室', '机加质量', '部门', 'ADM-QA', '', '机加工过程质量和计量管理'),
        ('BIZ-POWER', 'BIZ-ASM', '总装工厂', '总装工厂', '工厂', 'ADM-ASM-PLANT', '装配专业', '负责缸盖、短缸、长缸及整机总装'),
        ('BIZ-ASM', 'BIZ-ASM-HEAD-WS', '缸盖装配车间', '缸盖装配', '车间', 'ADM-ASM-PLANT', '', '气门机构和凸轮轴装配'),
        ('BIZ-ASM-HEAD-WS', 'BIZ-ASM-HEAD-SEC', '缸盖装配工段', '缸盖工段', '工段', 'ADM-ASM-PLANT', '', '缸盖预装和密封检验'),
        ('BIZ-ASM-HEAD-SEC', 'BIZ-ASM-HEAD-A', '缸盖装配甲班', '缸盖甲班', '班组', 'ADM-ASM-PLANT', '', '缸盖装配执行班组'),
        ('BIZ-ASM', 'BIZ-ASM-SHORT-WS', '短缸装配车间', '短缸装配', '车间', 'ADM-ASM-PLANT', '', '曲轴、活塞连杆与主轴承盖装配'),
        ('BIZ-ASM-SHORT-WS', 'BIZ-ASM-SHORT-SEC', '短缸装配工段', '短缸工段', '工段', 'ADM-ASM-PLANT', '', '短缸拧紧和旋转阻力检查'),
        ('BIZ-ASM-SHORT-SEC', 'BIZ-ASM-SHORT-A', '短缸装配甲班', '短缸甲班', '班组', 'ADM-ASM-PLANT', '', '短缸装配执行班组'),
        ('BIZ-ASM', 'BIZ-ASM-FINAL-WS', '整机总装车间', '整机总装', '车间', 'ADM-ASM-PLANT', '', '长缸、附件和电控系统装配'),
        ('BIZ-ASM-FINAL-WS', 'BIZ-ASM-FINAL-SEC', '整机总装工段', '总装工段', '工段', 'ADM-ASM-PLANT', '', '整机附件装配、条码绑定和电检'),
        ('BIZ-ASM-FINAL-SEC', 'BIZ-ASM-FINAL-A', '整机总装甲班', '总装甲班', '班组', 'ADM-ASM-PLANT', '', '整机总装执行班组'),
        ('BIZ-ASM', 'BIZ-ASM-QA', '总装质量室', '总装质量', '部门', 'ADM-QA', '', '总装过程审核和扭矩放行'),
        ('BIZ-POWER', 'BIZ-TEST', '试验工厂', '试验工厂', '工厂', 'ADM-TEST-PLANT', '装配专业', '负责冷试、热试、EOL放行和包装入库'),
        ('BIZ-TEST', 'BIZ-TEST-WS', '试验车间', '试验车间', '车间', 'ADM-TEST-PLANT', '', '整机冷试热试与EOL检测'),
        ('BIZ-TEST-WS', 'BIZ-TEST-SEC', '试验工段', '试验工段', '工段', 'ADM-TEST-PLANT', '', '冷试、热试和报码'),
        ('BIZ-TEST-SEC', 'BIZ-TEST-A', '试验甲班', '试验甲班', '班组', 'ADM-TEST-PLANT', '', '试验执行班组'),
        ('BIZ-TEST', 'BIZ-TEST-QA', '试验放行室', '试验放行', '部门', 'ADM-QA', '', 'EOL放行和成品审核'),
        ('BIZ-POWER', 'BIZ-TECH', '工艺技术部', '工艺技术', '部门', 'ADM-TECH', '', '标准工艺、工装和工时管理'),
        ('BIZ-POWER', 'BIZ-QA', '质量管理部', '质量管理', '部门', 'ADM-QA', '', '集团级质量策划和异常闭环'),
        ('BIZ-POWER', 'BIZ-PMC', '计划物流部', '计划物流', '部门', 'ADM-PMC', '', '主计划、齐套和物流协调'),
        ('BIZ-POWER', 'BIZ-SCM', '供应链管理部', '供应链', '部门', 'ADM-SCM', '', '采购、供应商开发和外协管理'),
        ('BIZ-POWER', 'BIZ-WARE', '仓储配送中心', '仓储中心', '部门', 'ADM-SCM', '', '原材料、线边库和成品库管理'),
        ('BIZ-POWER', 'BIZ-EAM', '设备管理部', '设备管理', '部门', 'ADM-EAM', '', '设备维修、保养和TPM推进'),
    ]
    for row in biz_rows:
        a_biz(*row)


def build_users() -> None:
    users = [
        ('U-TECH-01', '周承宇', '核心', '男', 'ADM-TECH', 'BIZ-TECH', '工艺平台主管', '139****0215', 'zhoucy@hqpt-demo.com', '1986-05-12', '3101********3214'),
        ('U-TECH-02', '何雅宁', '重要', '女', 'ADM-TECH', 'BIZ-TECH', '工装与标准工时工程师', '136****2486', 'heyn@hqpt-demo.com', '1990-11-03', '3205********2418'),
        ('U-PMC-01', '马会岚', '核心', '女', 'ADM-PMC', 'BIZ-PMC', '主计划经理', '138****3391', 'mahuilan@hqpt-demo.com', '1987-07-21', '4101********4217'),
        ('U-PMC-02', '郑博文', '重要', '男', 'ADM-PMC', 'BIZ-PMC', '生产计划员', '137****1542', 'zhengbw@hqpt-demo.com', '1992-09-14', '3302********1537'),
        ('U-SCM-01', '龚辰逸', '重要', '男', 'ADM-SCM', 'BIZ-SCM', '采购工程师', '135****8173', 'gongcy@hqpt-demo.com', '1989-03-26', '3401********8176'),
        ('U-SCM-02', '卢安琪', '重要', '女', 'ADM-SCM', 'BIZ-SCM', '外协管理专员', '134****2068', 'luaq@hqpt-demo.com', '1993-01-09', '3201********2064'),
        ('U-CAST-01', '魏昊然', '重要', '男', 'ADM-CAST-PLANT', 'BIZ-CAST-BLOCK-SEC', '缸体铸造工艺工程师', '139****4721', 'weihr@hqpt-demo.com', '1988-04-18', '3701********4722'),
        ('U-CAST-02', '马慧娟', '一般', '女', 'ADM-CAST-PLANT', 'BIZ-CAST-BLOCK-A', '缸体铸造班组长', '136****5219', 'mahj@hqpt-demo.com', '1991-06-07', '3203********5212'),
        ('U-CAST-03', '邵子恒', '一般', '男', 'ADM-CAST-PLANT', 'BIZ-CAST-HEAD-A', '缸盖浇注操作工', '138****6835', 'shaozh@hqpt-demo.com', '1995-10-16', '3412********6831'),
        ('U-CAST-04', '许若宁', '重要', '女', 'ADM-QA', 'BIZ-CAST-QA', '铸造质量工程师', '137****9052', 'xurn@hqpt-demo.com', '1990-02-11', '3306********9054'),
        ('U-MACH-01', '罗景澄', '重要', '男', 'ADM-MACH-PLANT', 'BIZ-MACH-BLOCK-SEC', '缸体机加工艺工程师', '139****1437', 'luojc@hqpt-demo.com', '1987-08-29', '4201********1431'),
        ('U-MACH-02', '顾嘉宁', '重要', '女', 'ADM-MACH-PLANT', 'BIZ-MACH-HEAD-SEC', '缸盖机加工艺工程师', '136****3348', 'gujn@hqpt-demo.com', '1992-12-04', '3205********3342'),
        ('U-MACH-03', '马汇峰', '重要', '男', 'ADM-MACH-PLANT', 'BIZ-MACH-CRANK-SEC', '曲轴工艺与外协工程师', '138****5116', 'mahf@hqpt-demo.com', '1988-09-02', '4102********5119'),
        ('U-MACH-04', '曹文涛', '一般', '男', 'ADM-MACH-PLANT', 'BIZ-MACH-CONROD-SEC', '连杆工艺工程师', '135****7208', 'caowt@hqpt-demo.com', '1991-03-13', '3202********7205'),
        ('U-MACH-05', '程思远', '一般', '男', 'ADM-MACH-PLANT', 'BIZ-MACH-BLOCK-A', '缸体珩磨操作工', '134****6180', 'chengsy@hqpt-demo.com', '1994-05-24', '3713********6184'),
        ('U-MACH-06', '蒋可欣', '一般', '女', 'ADM-QA', 'BIZ-MACH-QA', '机加质量工程师', '137****4283', 'jiangkx@hqpt-demo.com', '1993-08-08', '3304********4288'),
        ('U-ASM-01', '陈思源', '重要', '男', 'ADM-ASM-PLANT', 'BIZ-ASM-HEAD-SEC', '缸盖装配工程师', '139****3627', 'chensy@hqpt-demo.com', '1989-11-19', '3201********3621'),
        ('U-ASM-02', '李沐宸', '重要', '男', 'ADM-ASM-PLANT', 'BIZ-ASM-SHORT-SEC', '短缸装配工程师', '138****2774', 'limc@hqpt-demo.com', '1990-06-26', '4201********2779'),
        ('U-ASM-03', '邱雅雯', '重要', '女', 'ADM-ASM-PLANT', 'BIZ-ASM-FINAL-SEC', '整机总装工程师', '136****1736', 'qiuyw@hqpt-demo.com', '1992-01-17', '3301********1738'),
        ('U-ASM-04', '蒋志鹏', '一般', '男', 'ADM-ASM-PLANT', 'BIZ-ASM-FINAL-A', '整机总装班组长', '135****5402', 'jiangzp@hqpt-demo.com', '1988-12-22', '3206********5409'),
        ('U-ASM-05', '马汇东', '一般', '男', 'ADM-ASM-PLANT', 'BIZ-ASM-SHORT-A', '扭矩拧紧操作工', '134****8621', 'mahd@hqpt-demo.com', '1995-07-11', '3411********8625'),
        ('U-ASM-06', '方嘉宁', '一般', '女', 'ADM-QA', 'BIZ-ASM-QA', '总装质量工程师', '137****2946', 'fangjn@hqpt-demo.com', '1991-09-15', '3502********2941'),
        ('U-TEST-01', '韩书逸', '重要', '男', 'ADM-TEST-PLANT', 'BIZ-TEST-SEC', '试验工程师', '139****4851', 'hansy@hqpt-demo.com', '1987-10-05', '3207********4857'),
        ('U-TEST-02', '魏可岚', '一般', '女', 'ADM-TEST-PLANT', 'BIZ-TEST-A', '热试操作工', '138****9117', 'weikl@hqpt-demo.com', '1994-04-09', '3303********9114'),
        ('U-TEST-03', '袁致远', '重要', '男', 'ADM-QA', 'BIZ-TEST-QA', 'EOL放行工程师', '136****6012', 'yuanzy@hqpt-demo.com', '1988-02-28', '4103********6016'),
        ('U-QA-01', '宋雨泽', '核心', '男', 'ADM-QA', 'BIZ-QA', '质量主管', '139****7420', 'songyz@hqpt-demo.com', '1985-06-30', '3208********7422'),
        ('U-EAM-01', '梁泽宇', '重要', '男', 'ADM-EAM', 'BIZ-EAM', '设备维修主管', '138****2563', 'liangzy@hqpt-demo.com', '1986-03-03', '3410********2568'),
        ('U-EAM-02', '郝雨晨', '一般', '男', 'ADM-EAM', 'BIZ-EAM', '设备保养员', '135****3069', 'haoyc@hqpt-demo.com', '1993-11-27', '3209********3063'),
        ('U-WARE-01', '马慧珊', '一般', '女', 'ADM-SCM', 'BIZ-WARE', '原材料库管理员', '137****1586', 'mahs@hqpt-demo.com', '1991-05-06', '3305********1588'),
        ('U-WARE-02', '徐敬尧', '一般', '男', 'ADM-SCM', 'BIZ-WARE', '成品库管理员', '136****4489', 'xujy@hqpt-demo.com', '1990-08-20', '4206********4481'),
    ]
    for row in users:
        a_user(*row)

def build_resources() -> None:
    suppliers = [
        ('SUP-ALLOY', '华东轻合金材料有限公司', '轻合金', '供应A356铝合金锭与回炉料配比服务'),
        ('SUP-FORG', '江苏精锻传动件有限公司', '精锻件', '供应曲轴与连杆锻坯'),
        ('SUP-STD', '苏州恒驰标准件有限公司', '标准件', '供应螺栓、密封垫及标准辅件'),
        ('SUP-HT', '无锡金石热处理有限公司', '热处理', '承担曲轴调质与氮化外协工序'),
        ('SUP-TURBO', '博驰增压系统科技有限公司', '增压系统', '供应涡轮增压器总成'),
        ('SUP-FUEL', '德迈燃油系统科技有限公司', '燃油系统', '供应喷油器与燃油轨总成'),
    ]
    for row in suppliers:
        a_sup(*row)

    equipments = [
        ('EQ-CAST-FURNACE-01', '熔炼保温炉', 'AL-MF-12T', 'BIZ-CAST-BLOCK-SEC', YES, '缸体铝液熔炼瓶颈设备'),
        ('EQ-CAST-LPDC-01', '缸体低压铸造机', 'LPDC-1600', 'BIZ-CAST-BLOCK-SEC', YES, '缸体低压浇注设备'),
        ('EQ-CAST-XRAY-01', 'X射线探伤机', 'XR-450', 'BIZ-CAST-QA', NO, '铸件内部缺陷检测'),
        ('EQ-CAST-HEAD-01', '缸盖低压铸造机', 'LPDC-1200', 'BIZ-CAST-HEAD-SEC', YES, '缸盖低压浇注设备'),
        ('EQ-MACH-BLOCK-HMC-01', '缸体卧式加工中心', 'HMC-630', 'BIZ-MACH-BLOCK-SEC', YES, '缸体基准面与孔系加工'),
        ('EQ-MACH-BLOCK-HONE-01', '缸孔珩磨机', 'HM-500', 'BIZ-MACH-BLOCK-SEC', YES, '缸孔最终珩磨设备'),
        ('EQ-MACH-CMM-01', '三坐标测量机', 'CMM-12108', 'BIZ-MACH-QA', NO, '缸体缸盖尺寸终检'),
        ('EQ-MACH-HEAD-VMC-01', '缸盖立式加工中心', 'VMC-800', 'BIZ-MACH-HEAD-SEC', YES, '缸盖火面与导管加工'),
        ('EQ-MACH-HEAD-LEAK-01', '缸盖气密试验机', 'LT-4C', 'BIZ-MACH-HEAD-SEC', NO, '缸盖水套气密检测'),
        ('EQ-MACH-CRANK-TURN-01', '曲轴数控车床', 'CK-50C', 'BIZ-MACH-CRANK-SEC', NO, '曲轴基准车削'),
        ('EQ-MACH-CRANK-GRIND-01', '曲轴磨床', 'MK82125', 'BIZ-MACH-CRANK-SEC', YES, '主轴颈与连杆颈磨削'),
        ('EQ-MACH-BAL-01', '曲轴动平衡机', 'DB-500', 'BIZ-MACH-CRANK-SEC', NO, '曲轴动平衡校正'),
        ('EQ-MACH-CONROD-01', '连杆镗珩机', 'TH-220', 'BIZ-MACH-CONROD-SEC', NO, '连杆大小头孔加工'),
        ('EQ-ASM-HEAD-PRESS-01', '气门油封压装机', 'VP-12', 'BIZ-ASM-HEAD-SEC', NO, '缸盖装配专机'),
        ('EQ-ASM-SHORT-TORQUE-01', '主轴承盖柔性拧紧机', 'FTS-8', 'BIZ-ASM-SHORT-SEC', YES, '短缸关键拧紧设备'),
        ('EQ-ASM-LEAK-01', '长缸密封试验台', 'LT-ENG-02', 'BIZ-ASM-FINAL-SEC', NO, '长缸密封性检测'),
        ('EQ-ASM-FINAL-TORQUE-01', '整机附件柔性拧紧机', 'FTS-12', 'BIZ-ASM-FINAL-SEC', YES, '整机关键扭矩控制设备'),
        ('EQ-TEST-COLD-01', '发动机冷试台', 'CT-2000', 'BIZ-TEST-SEC', YES, '整机冷试与摩擦扭矩检测'),
        ('EQ-TEST-HOT-01', '发动机热试台', 'HT-350', 'BIZ-TEST-SEC', YES, '整机热试性能验证'),
        ('EQ-TEST-EOL-01', 'EOL报码诊断台', 'EOL-DX', 'BIZ-TEST-QA', NO, '报码、泄漏和放行诊断'),
    ]
    for row in equipments:
        a_eq(*row)

    tools = [
        ('TOOL-TORQUE-01', '智能数显扭矩扳手', CAT_SPARE, MAKE_BUY, '通用工具', FEATURE_KEY, 'TW-200N', '20-200N·m', '缸盖螺栓与关键附件拧紧复核工具', 50000, 365),
        ('TOOL-BLOCK-TURN-01', '缸体翻转架', CAT_KIT, MAKE_SELF, '专用工装', FEATURE_KEY, 'BTF-01', '适配2.0T缸体', '缸体机加工及短缸装配周转翻转工装', 20000, 720),
        ('TOOL-CRANK-FIX-01', '曲轴装配定位工装', CAT_KIT, MAKE_SELF, '专用工装', FEATURE_IMPORTANT, 'CFX-02', '五点定位', '短缸装配曲轴定位与端隙控制工装', 18000, 540),
        ('TOOL-PISTON-RING-01', '活塞环压装工具', CAT_PART, MAKE_BUY, '通用工具', FEATURE_IMPORTANT, 'PRT-4C', '四缸通用', '活塞环压缩与导向装入工具', 30000, 365),
        ('TOOL-HEAD-TORQUE-01', '缸盖分步拧紧扭矩扳手', CAT_PART, MAKE_BUY, '通用工具', FEATURE_KEY, 'HTW-250', '30-250N·m', '缸盖螺栓分步拧紧及复核使用', 50000, 365),
        ('TOOL-ENG-CART-01', '发动机总成转运台', CAT_PART, MAKE_SELF, '专用工装', FEATURE_IMPORTANT, 'ECT-01', '承载450kg', '整机跨工段与跨工厂转运周转台', 12000, 720),
    ]
    for row in tools:
        a_tool(*row)

    workcenters = [
        ('WC-CAST-BLOCK', '缸体低压铸造线', 'BIZ-CAST-BLOCK-SEC', '产线', '加工', '覆盖制芯、浇注、切冒口'),
        ('WC-CAST-HEAD', '缸盖低压铸造线', 'BIZ-CAST-HEAD-SEC', '产线', '加工', '覆盖制芯、浇注、清理'),
        ('WC-CAST-QA', '铸件无损检测中心', 'BIZ-CAST-QA', '设备组', '检验', '铸件X光和外观放行'),
        ('WC-CAST-TRANSFER', '铸件转运中心', 'BIZ-CAST', '组织', '加工', '铸造到机加工厂的厂际转工节点'),
        ('WC-MACH-BLOCK', '缸体精密机加线', 'BIZ-MACH-BLOCK-SEC', '产线', '加工', '基准面、缸孔和主轴承座加工'),
        ('WC-MACH-HEAD', '缸盖精密机加线', 'BIZ-MACH-HEAD-SEC', '产线', '加工', '燃烧室、导管和凸轮孔系加工'),
        ('WC-MACH-CRANK', '曲轴磨削线', 'BIZ-MACH-CRANK-SEC', '产线', '加工', '曲轴车磨和动平衡'),
        ('WC-MACH-CONROD', '连杆机加线', 'BIZ-MACH-CONROD-SEC', '产线', '加工', '连杆孔系加工与称重配对'),
        ('WC-MACH-CMM', '机加计量终检中心', 'BIZ-MACH-QA', '设备组', '检验', '三坐标、气密与磁粉检测'),
        ('WC-OUT-HT', '外协热处理中心', 'BIZ-MACH', '外委', '加工', '曲轴调质氮化外协节点'),
        ('WC-MACH-TRANSFER', '机加转运中心', 'BIZ-MACH', '组织', '加工', '机加工厂向总装工厂的厂际转工节点'),
        ('WC-ASM-HEAD', '缸盖装配线', 'BIZ-ASM-HEAD-SEC', '产线', '加工', '缸盖气门机构与凸轮轴装配'),
        ('WC-ASM-SHORT', '短缸装配线', 'BIZ-ASM-SHORT-SEC', '产线', '加工', '曲轴、活塞连杆和主轴承盖装配'),
        ('WC-ASM-FINAL', '整机总装线', 'BIZ-ASM-FINAL-SEC', '产线', '加工', '长缸、附件和电控系统总装'),
        ('WC-ASM-LEAK', '总装密封检验中心', 'BIZ-ASM-QA', '设备组', '检验', '长缸和整机密封性检查'),
        ('WC-ASM-TRANSFER', '总装转运中心', 'BIZ-ASM', '组织', '加工', '总装工厂内部及跨厂转工节点'),
        ('WC-TEST-COLD', '发动机冷试中心', 'BIZ-TEST-SEC', '产线', '检验', '冷试、机油循环和阻力分析'),
        ('WC-TEST-HOT', '发动机热试中心', 'BIZ-TEST-SEC', '产线', '检验', '热试功率、油耗和排放验证'),
        ('WC-TEST-EOL', 'EOL放行中心', 'BIZ-TEST-QA', '设备组', '检验', '报码、泄漏和最终放行'),
    ]
    for row in workcenters:
        a_wc(*row)

    for wc_code, sup_code in [('WC-OUT-HT', 'SUP-HT')]:
        l_wc_sup(wc_code, sup_code)

    wc_user_links = [
        ('WC-CAST-BLOCK', 'U-CAST-01'), ('WC-CAST-BLOCK', 'U-CAST-02'), ('WC-CAST-HEAD', 'U-CAST-03'), ('WC-CAST-QA', 'U-CAST-04'),
        ('WC-MACH-BLOCK', 'U-MACH-01'), ('WC-MACH-BLOCK', 'U-MACH-05'), ('WC-MACH-HEAD', 'U-MACH-02'), ('WC-MACH-CRANK', 'U-MACH-03'),
        ('WC-MACH-CONROD', 'U-MACH-04'), ('WC-MACH-CMM', 'U-MACH-06'), ('WC-OUT-HT', 'U-SCM-02'), ('WC-ASM-HEAD', 'U-ASM-01'),
        ('WC-ASM-SHORT', 'U-ASM-02'), ('WC-ASM-SHORT', 'U-ASM-05'), ('WC-ASM-FINAL', 'U-ASM-03'), ('WC-ASM-FINAL', 'U-ASM-04'),
        ('WC-ASM-LEAK', 'U-ASM-06'), ('WC-TEST-COLD', 'U-TEST-01'), ('WC-TEST-HOT', 'U-TEST-02'), ('WC-TEST-EOL', 'U-TEST-03'),
    ]
    for wc_code, user_code in wc_user_links:
        l_wc_user(wc_code, user_code)

    eq_user_links = [
        ('EQ-CAST-FURNACE-01', 'U-CAST-01'), ('EQ-CAST-LPDC-01', 'U-CAST-02'), ('EQ-CAST-XRAY-01', 'U-CAST-04'), ('EQ-CAST-HEAD-01', 'U-CAST-03'),
        ('EQ-MACH-BLOCK-HMC-01', 'U-MACH-01'), ('EQ-MACH-BLOCK-HONE-01', 'U-MACH-05'), ('EQ-MACH-CMM-01', 'U-MACH-06'), ('EQ-MACH-HEAD-VMC-01', 'U-MACH-02'),
        ('EQ-MACH-HEAD-LEAK-01', 'U-MACH-02'), ('EQ-MACH-CRANK-TURN-01', 'U-MACH-03'), ('EQ-MACH-CRANK-GRIND-01', 'U-MACH-03'), ('EQ-MACH-BAL-01', 'U-MACH-03'),
        ('EQ-MACH-CONROD-01', 'U-MACH-04'), ('EQ-ASM-HEAD-PRESS-01', 'U-ASM-01'), ('EQ-ASM-SHORT-TORQUE-01', 'U-ASM-02'), ('EQ-ASM-LEAK-01', 'U-ASM-06'),
        ('EQ-ASM-FINAL-TORQUE-01', 'U-ASM-03'), ('EQ-TEST-COLD-01', 'U-TEST-01'), ('EQ-TEST-HOT-01', 'U-TEST-02'), ('EQ-TEST-EOL-01', 'U-TEST-03'),
    ]
    for eq_code, user_code in eq_user_links:
        l_eq_user(eq_code, user_code)

    wc_eq_links = [
        ('WC-CAST-BLOCK', 'EQ-CAST-FURNACE-01'), ('WC-CAST-BLOCK', 'EQ-CAST-LPDC-01'), ('WC-CAST-QA', 'EQ-CAST-XRAY-01'), ('WC-CAST-HEAD', 'EQ-CAST-HEAD-01'),
        ('WC-MACH-BLOCK', 'EQ-MACH-BLOCK-HMC-01'), ('WC-MACH-BLOCK', 'EQ-MACH-BLOCK-HONE-01'), ('WC-MACH-CMM', 'EQ-MACH-CMM-01'), ('WC-MACH-HEAD', 'EQ-MACH-HEAD-VMC-01'),
        ('WC-MACH-CMM', 'EQ-MACH-HEAD-LEAK-01'), ('WC-MACH-CRANK', 'EQ-MACH-CRANK-TURN-01'), ('WC-MACH-CRANK', 'EQ-MACH-CRANK-GRIND-01'), ('WC-MACH-CRANK', 'EQ-MACH-BAL-01'),
        ('WC-MACH-CONROD', 'EQ-MACH-CONROD-01'), ('WC-ASM-HEAD', 'EQ-ASM-HEAD-PRESS-01'), ('WC-ASM-SHORT', 'EQ-ASM-SHORT-TORQUE-01'), ('WC-ASM-LEAK', 'EQ-ASM-LEAK-01'),
        ('WC-ASM-FINAL', 'EQ-ASM-FINAL-TORQUE-01'), ('WC-TEST-COLD', 'EQ-TEST-COLD-01'), ('WC-TEST-HOT', 'EQ-TEST-HOT-01'), ('WC-TEST-EOL', 'EQ-TEST-EOL-01'),
    ]
    for wc_code, eq_code in wc_eq_links:
        l_wc_eq(wc_code, eq_code)

    warehouses = [
        ('WH-RM', '原材料总库', 'BIZ-WARE', 'ERP一级库', '承担铝锭、锻坯和标准件入库'),
        ('WH-CAST-WIP', '铸件在制库', 'BIZ-CAST', '车间二级库', '铸件毛坯暂存和厂际转运前缓存'),
        ('WH-MACH-WIP', '机加在制库', 'BIZ-MACH', '车间二级库', '机加半成品与待外协件缓存'),
        ('WH-ASM-LINE', '总装线边库', 'BIZ-ASM', '车间二级库', '装配线边齐套与拉动供料'),
        ('WH-FG', '成品库', 'BIZ-WARE', 'ERP一级库', '试验放行后的整机入库'),
        ('WH-SPARE', '设备备件库', 'BIZ-EAM', '设备备件库', '设备备件和易损件管理'),
        ('WH-TOOL', '工装工具库', 'BIZ-EAM', '工装备件库', '工装工具收发与保养管理'),
    ]
    for code, name, biz, biz_type, remark in warehouses:
        a_wh(code, name, biz, biz_type, '普通库房', remark)

    locations = [
        ('LOC-RM-AL-01', '铝锭区-A01', 'BIZ-WARE', 'WH-RM', '铝合金锭货位'),
        ('LOC-RM-FORG-01', '锻坯区-B01', 'BIZ-WARE', 'WH-RM', '曲轴与连杆锻坯货位'),
        ('LOC-CAST-BLOCK-01', '缸体毛坯区-C01', 'BIZ-CAST', 'WH-CAST-WIP', '缸体毛坯待转运'),
        ('LOC-CAST-HEAD-01', '缸盖毛坯区-C02', 'BIZ-CAST', 'WH-CAST-WIP', '缸盖毛坯待转运'),
        ('LOC-MACH-BLOCK-01', '缸体半成品区-M01', 'BIZ-MACH', 'WH-MACH-WIP', '缸体加工中在制区'),
        ('LOC-MACH-CRANK-01', '曲轴待外协区-M02', 'BIZ-MACH', 'WH-MACH-WIP', '曲轴待热处理缓存区'),
        ('LOC-ASM-KIT-01', '短缸齐套区-A01', 'BIZ-ASM', 'WH-ASM-LINE', '短缸线边齐套'),
        ('LOC-ASM-KIT-02', '整机附件区-A02', 'BIZ-ASM', 'WH-ASM-LINE', '整机装配附件齐套'),
        ('LOC-FG-01', '成品发动机区-F01', 'BIZ-WARE', 'WH-FG', '试验放行成品区'),
        ('LOC-SPARE-01', '关键备件区-S01', 'BIZ-EAM', 'WH-SPARE', '设备关键备件'),
        ('LOC-TOOL-01', '扭矩工具区-T01', 'BIZ-EAM', 'WH-TOOL', '扭矩工具收纳区'),
    ]
    for row in locations:
        a_loc(*row)


def build_materials() -> None:
    materials = [
        ('MAT-ENG-20TGDI', '2.0T缸内直喷涡轮增压汽油发动机', CAT_PART, MAKE_SELF, FEATURE_KEY, 'ENG-20TGDI', 'EA888-G4', '四缸/涡轮增压/国六b', '整机交付产品'),
        ('MAT-LONG-BLK', '长缸总成', CAT_PART, MAKE_SELF, FEATURE_KEY, 'ENG-LB-20T', 'LB-20T', '含缸盖与正时系统', '长缸装配阶段件'),
        ('MAT-SHORT-BLK', '短缸总成', CAT_PART, MAKE_SELF, FEATURE_KEY, 'ENG-SB-20T', 'SB-20T', '含曲轴与活塞连杆', '短缸装配阶段件'),
        ('MAT-CYL-HEAD-ASM', '缸盖总成', CAT_PART, MAKE_SELF, FEATURE_KEY, 'ENG-HEAD-ASM', 'CH-20T', '含气门机构与凸轮轴', '缸盖装配阶段件'),
        ('MAT-BLOCK-CAST', '缸体铸件', CAT_PART, MAKE_SELF, FEATURE_KEY, 'BLK-CAST-20T', 'BLK-CAST', 'A356低压铸造毛坯', '缸体铸造阶段件'),
        ('MAT-BLOCK-ROUGH', '缸体粗加工件', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'BLK-RGH-20T', 'BLK-RGH', '缸体粗加工后状态', '待精加工与清洗'),
        ('MAT-BLOCK-FIN', '缸体精加工件', CAT_PART, MAKE_SELF, FEATURE_KEY, 'BLK-FIN-20T', 'BLK-FIN', '缸孔与主轴承座加工完成', '可转入短缸装配'),
        ('MAT-HEAD-CAST', '缸盖铸件', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'HEAD-CAST-20T', 'HEAD-CAST', 'A356低压铸造毛坯', '缸盖铸造阶段件'),
        ('MAT-HEAD-ROUGH', '缸盖粗加工件', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'HEAD-RGH-20T', 'HEAD-RGH', '缸盖粗加工后状态', '待精加工与气密'),
        ('MAT-HEAD-FIN', '缸盖精加工件', CAT_PART, MAKE_SELF, FEATURE_KEY, 'HEAD-FIN-20T', 'HEAD-FIN', '火面、导管和孔系加工完成', '可转入缸盖装配'),
        ('MAT-CRANK-FORG', '曲轴锻坯', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'CRK-FORG-20T', 'CRK-FORG', '42CrMo调质锻坯', '外购曲轴锻坯'),
        ('MAT-CRANK-ROUGH', '曲轴粗加工件', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'CRK-RGH-20T', 'CRK-RGH', '车削磨削前状态', '待热处理'),
        ('MAT-CRANK-HT', '曲轴热处理后件', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'CRK-HT-20T', 'CRK-HT', '调质+氮化后状态', '待抛光与动平衡'),
        ('MAT-CRANK-FIN', '曲轴成品件', CAT_PART, MAKE_SELF, FEATURE_KEY, 'CRK-FIN-20T', 'CRK-FIN', '磨削、抛光和动平衡完成', '短缸装配关键件'),
        ('MAT-CONROD-FORG', '连杆锻坯', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'ROD-FORG-20T', 'ROD-FORG', '40Cr连杆锻坯', '外购连杆锻坯'),
        ('MAT-CONROD-FIN', '连杆成品件', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'ROD-FIN-20T', 'ROD-FIN', '镗珩、裂解和称重配对完成', '短缸装配关键零件'),
        ('MAT-PISTON-ASSY', '活塞总成', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'PST-ASM-20T', 'PST-20T', '铝合金活塞总成', '含活塞销'),
        ('MAT-RING-SET', '活塞环组件', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'RING-SET-20T', 'RING-20T', '镀铬耐磨环', '四缸用活塞环'),
        ('MAT-BRG-MAIN-SET', '主轴承组件', CAT_KIT, MAKE_BUY, FEATURE_IMPORTANT, 'BRG-MAIN-20T', 'MBRG-20T', '主轴承上/下瓦', '短缸装配使用'),
        ('MAT-BRG-CONROD-SET', '连杆轴承组件', CAT_KIT, MAKE_BUY, FEATURE_IMPORTANT, 'BRG-ROD-20T', 'RBRG-20T', '连杆瓦组件', '连杆装配使用'),
        ('MAT-BOLT-MAIN-SET', '主轴承盖螺栓组', CAT_KIT, MAKE_BUY, FEATURE_IMPORTANT, 'BOLT-MAIN-20T', 'M10*1.5', '一次性拧紧螺栓', '主轴承盖紧固件'),
        ('MAT-HEAD-GASKET', '缸盖垫', CAT_PART, MAKE_BUY, FEATURE_KEY, 'GSK-HEAD-20T', 'MLS-20T', '多层钢缸盖垫', '长缸装配关键密封件'),
        ('MAT-BOLT-HEAD-SET', '缸盖螺栓组', CAT_KIT, MAKE_BUY, FEATURE_KEY, 'BOLT-HEAD-20T', 'M11拉伸螺栓', '缸盖关键拧紧件', '一次性使用'),
        ('MAT-TIMING-KIT', '正时链系统组件', CAT_KIT, MAKE_BUY, FEATURE_IMPORTANT, 'TMG-KIT-20T', 'CHAIN-20T', '链条、导轨和涨紧器', '长缸装配使用'),
        ('MAT-COVER-VALVE', '气门室盖总成', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'VC-ASM-20T', 'VC-20T', 'PA66+GF30', '带PCV阀组件'),
        ('MAT-TURBO-CHARGER', '涡轮增压器总成', CAT_PART, MAKE_BUY, FEATURE_KEY, 'TURBO-20T', 'GTD-1752', '单涡管增压器', '整机性能关键外购件'),
        ('MAT-EXH-MANIFOLD', '排气歧管总成', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'EXH-MFD-20T', 'EM-20T', '耐热铸钢歧管', '与增压器配装'),
        ('MAT-FUEL-RAIL', '燃油轨总成', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'FR-ASM-20T', '350bar', '高压燃油轨', '燃油系统关键件'),
        ('MAT-INJECTOR', '高压喷油器', CAT_PART, MAKE_BUY, FEATURE_KEY, 'INJ-20T', '350bar-GDI', '缸内直喷喷油器', '单缸一支'),
        ('MAT-FLYWHEEL', '飞轮总成', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'FLY-20T', 'DMF-20T', '双质量飞轮', '整机末端件'),
        ('MAT-ENG-HARNESS', '发动机线束', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'HRN-ENG-20T', '12V', '发动机本体线束', '整机电连接件'),
        ('MAT-IGNITION-COIL', '点火线圈', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'IGN-COIL-20T', 'COP-20T', '独立点火线圈', '单缸一支'),
        ('MAT-SPARK-PLUG', '火花塞', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'SPK-PLUG-20T', 'M14*1.25', '铱金火花塞', '单缸一支'),
        ('MAT-CAM-IN', '进气凸轮轴', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'CAM-IN-20T', 'VVT-IN', '带相位器接口', '缸盖总成关键件'),
        ('MAT-CAM-EX', '排气凸轮轴', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'CAM-EX-20T', 'VVT-EX', '带相位器接口', '缸盖总成关键件'),
        ('MAT-VALVE-SET', '气门机构组件', CAT_KIT, MAKE_BUY, FEATURE_IMPORTANT, 'VALVE-SET-20T', '16V', '气门、弹簧、锁片与油封', '缸盖装配件'),
        ('MAT-PUMP-OIL', '机油泵总成', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'PUMP-OIL-20T', 'OP-20T', '变量机油泵', '整机润滑系统件'),
        ('MAT-AL-A356', 'A356铝合金锭', CAT_RAW, MAKE_BUY, FEATURE_NORMAL, 'AL-A356', 'A356', '铸造用铝合金', '缸体缸盖原材料'),
        ('MAT-CORE-SAND', '树脂覆膜砂', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'CORE-SAND', 'RS-01', '制芯辅料', '铸造制芯材料'),
        ('MAT-SEALANT-ASM', '厌氧密封胶', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'SEALANT-01', '50ml', '装配密封辅料', '长缸与附件密封使用'),
        ('MAT-TEST-OIL', '试验机油', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'TEST-OIL-5W30', '5W-30', '冷试热试介质', '试验工厂使用'),
        ('MAT-TEST-FUEL', '试验燃油', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'TEST-FUEL-95', '95#', '热试燃油介质', '热试台使用'),
    ]
    for row in materials:
        a_mat(*row)


def build_mboms() -> None:
    a_mbom('MBOM-HEAD-A01', 'MAT-CYL-HEAD-ASM', '缸盖总成MBOM', '面向缸盖装配工厂')
    a_mbom('MBOM-SHORT-A01', 'MAT-SHORT-BLK', '短缸总成MBOM', '面向短缸装配工厂')
    a_mbom('MBOM-LONG-A01', 'MAT-LONG-BLK', '长缸总成MBOM', '面向长缸合装工厂')
    a_mbom('MBOM-ENG-A01', 'MAT-ENG-20TGDI', '发动机总成MBOM', '面向整机总装与试验工厂')

    for mbom_code, root_mat in [
        ('MBOM-HEAD-A01', 'MAT-CYL-HEAD-ASM'),
        ('MBOM-SHORT-A01', 'MAT-SHORT-BLK'),
        ('MBOM-LONG-A01', 'MAT-LONG-BLK'),
        ('MBOM-ENG-A01', 'MAT-ENG-20TGDI'),
    ]:
        a_mbom_node(mbom_code, 0, root_mat, 1, '0', '')

    for child, qty in [('MAT-HEAD-FIN', 1), ('MAT-CAM-IN', 1), ('MAT-CAM-EX', 1), ('MAT-VALVE-SET', 1), ('MAT-SEALANT-ASM', 1)]:
        a_mbom_node('MBOM-HEAD-A01', 1, child, qty, 'MAT-CYL-HEAD-ASM', VER)

    for child, qty in [('MAT-BLOCK-FIN', 1), ('MAT-CRANK-FIN', 1), ('MAT-CONROD-FIN', 4), ('MAT-PISTON-ASSY', 4), ('MAT-RING-SET', 4), ('MAT-BRG-MAIN-SET', 1), ('MAT-BRG-CONROD-SET', 1), ('MAT-BOLT-MAIN-SET', 1), ('MAT-PUMP-OIL', 1)]:
        a_mbom_node('MBOM-SHORT-A01', 1, child, qty, 'MAT-SHORT-BLK', VER)

    for child, qty in [('MAT-SHORT-BLK', 1), ('MAT-CYL-HEAD-ASM', 1), ('MAT-HEAD-GASKET', 1), ('MAT-BOLT-HEAD-SET', 1), ('MAT-TIMING-KIT', 1), ('MAT-COVER-VALVE', 1)]:
        a_mbom_node('MBOM-LONG-A01', 1, child, qty, 'MAT-LONG-BLK', VER)

    for child, qty in [('MAT-LONG-BLK', 1), ('MAT-TURBO-CHARGER', 1), ('MAT-EXH-MANIFOLD', 1), ('MAT-FUEL-RAIL', 1), ('MAT-INJECTOR', 4), ('MAT-FLYWHEEL', 1), ('MAT-ENG-HARNESS', 1), ('MAT-IGNITION-COIL', 4), ('MAT-SPARK-PLUG', 4)]:
        a_mbom_node('MBOM-ENG-A01', 1, child, qty, 'MAT-ENG-20TGDI', VER)

def build_routes() -> None:
    routes = [
        {
            'code': 'RT-BLOCK-CAST-A01', 'name': '缸体低压铸造工艺', 'route_spec': '铸造', 'biz': 'BIZ-CAST', 'material': 'MAT-BLOCK-CAST', 'proc_spec': '机械加工专业', 'remark': '铸造工厂完成缸体毛坯制造并转机加工厂',
            'ops': [
                {'no': '0010', 'name': '铝液熔炼与成分调整', 'type': '加工', 'wc': 'WC-CAST-BLOCK', 'prep': 40, 'run': 90, 'out': 'MAT-BLOCK-CAST', 'content': '完成A356铝液熔炼、除气和成分复核', 'materials': [('MAT-AL-A356', 18)], 'steps': ['核对铝锭批次与炉号', '完成熔炼、扒渣和在线成分调整']},
                {'no': '0020', 'name': '制芯与模具准备', 'type': '加工', 'wc': 'WC-CAST-BLOCK', 'prep': 30, 'run': 70, 'out': 'MAT-BLOCK-CAST', 'content': '完成水套砂芯、模具清理与喷涂', 'materials': [('MAT-CORE-SAND', 6)], 'steps': ['装配砂芯并确认定位销状态', '完成模具喷涂与预热']},
                {'no': '0030', 'name': '低压浇注与凝固控制', 'type': '加工', 'wc': 'WC-CAST-BLOCK', 'prep': 20, 'run': 45, 'out': 'MAT-BLOCK-CAST', 'content': '执行低压浇注、保压和凝固曲线控制', 'materials': [], 'steps': ['按照标准压力曲线执行浇注', '记录保压和冷却参数']},
                {'no': '0040', 'name': '切冒口与铸件清理', 'type': '加工', 'wc': 'WC-CAST-BLOCK', 'prep': 15, 'run': 30, 'out': 'MAT-BLOCK-CAST', 'content': '完成切冒口、抛丸与外观清理', 'materials': [], 'steps': ['切除浇冒口并处理飞边', '抛丸清理后转入待检区']},
                {'no': '0050', 'name': 'X光探伤与外观检验', 'type': '检验', 'wc': 'WC-CAST-QA', 'prep': 10, 'run': 20, 'out': 'MAT-BLOCK-CAST', 'content': '完成内部缺陷探伤和外观放行', 'materials': [], 'steps': ['执行X光探伤并判定缩孔风险', '完成外观与关键尺寸抽检']},
                {'no': '0060', 'name': '厂际转工至机加工厂', 'type': '厂际转工', 'wc': 'WC-CAST-TRANSFER', 'prep': 10, 'run': 25, 'out': 'MAT-BLOCK-CAST', 'content': '缸体铸件转入机加工厂在制库', 'materials': [], 'steps': ['生成转工批次与随行卡', '转运至机加工厂缸体在制库']},
            ],
        },
        {
            'code': 'RT-BLOCK-MACH-A01', 'name': '缸体精密机加工艺', 'route_spec': '机加', 'biz': 'BIZ-MACH', 'material': 'MAT-BLOCK-FIN', 'proc_spec': '机械加工专业', 'remark': '机加工厂完成缸体粗精加工与终检',
            'ops': [
                {'no': '0010', 'name': '基准面粗铣与定位基准建立', 'type': '加工', 'wc': 'WC-MACH-BLOCK', 'prep': 20, 'run': 55, 'out': 'MAT-BLOCK-ROUGH', 'content': '完成缸体基准面粗铣和主定位基准建立', 'materials': [('MAT-BLOCK-CAST', 1)], 'steps': ['装夹缸体铸件并复核定位销', '粗铣火面和侧面建立加工基准']},
                {'no': '0020', 'name': '主轴承座与缸孔半精加工', 'type': '加工', 'wc': 'WC-MACH-BLOCK', 'prep': 18, 'run': 65, 'out': 'MAT-BLOCK-ROUGH', 'content': '完成主轴承座、缸孔和油道关键孔加工', 'materials': [], 'steps': ['加工主轴承座孔系与螺纹孔', '半精镗缸孔并校核同轴度']},
                {'no': '0030', 'name': '缸孔珩磨与火面精铣', 'type': '加工', 'wc': 'WC-MACH-BLOCK', 'prep': 15, 'run': 60, 'out': 'MAT-BLOCK-FIN', 'content': '完成缸孔珩磨和火面精加工', 'materials': [], 'steps': ['按珩磨网纹要求完成缸孔精加工', '精铣火面并校核平面度']},
                {'no': '0040', 'name': '清洗去毛刺', 'type': '加工', 'wc': 'WC-MACH-BLOCK', 'prep': 10, 'run': 25, 'out': 'MAT-BLOCK-FIN', 'content': '完成高压清洗、去毛刺和通道吹扫', 'materials': [], 'steps': ['清洗切屑并吹扫油道水道', '人工复核关键倒角与毛刺状态']},
                {'no': '0050', 'name': '三坐标与清洁度终检', 'type': '检验', 'wc': 'WC-MACH-CMM', 'prep': 12, 'run': 30, 'out': 'MAT-BLOCK-FIN', 'content': '完成缸体关键尺寸和清洁度放行', 'materials': [], 'steps': ['执行三坐标尺寸检测', '完成清洁度与表面缺陷判定']},
                {'no': '0060', 'name': '厂际转工至短缸装配', 'type': '厂际转工', 'wc': 'WC-MACH-TRANSFER', 'prep': 8, 'run': 20, 'out': 'MAT-BLOCK-FIN', 'content': '缸体精加工件转入总装工厂', 'materials': [], 'steps': ['生成缸体转工单据', '转运至总装工厂短缸线边库']},
            ],
        },
        {
            'code': 'RT-HEAD-CAST-A01', 'name': '缸盖低压铸造工艺', 'route_spec': '铸造', 'biz': 'BIZ-CAST', 'material': 'MAT-HEAD-CAST', 'proc_spec': '机械加工专业', 'remark': '铸造工厂完成缸盖毛坯制造并转机加工厂',
            'ops': [
                {'no': '0010', 'name': '铝液熔炼与除气', 'type': '加工', 'wc': 'WC-CAST-HEAD', 'prep': 35, 'run': 80, 'out': 'MAT-HEAD-CAST', 'content': '完成缸盖用铝液熔炼和除气处理', 'materials': [('MAT-AL-A356', 10)], 'steps': ['核对缸盖铸造合金牌号', '完成铝液除气与温度稳定']},
                {'no': '0020', 'name': '制芯与模具装配', 'type': '加工', 'wc': 'WC-CAST-HEAD', 'prep': 25, 'run': 60, 'out': 'MAT-HEAD-CAST', 'content': '完成缸盖复杂水套砂芯装配', 'materials': [('MAT-CORE-SAND', 4)], 'steps': ['装配水套砂芯和排气道芯', '完成模具预热与锁模检查']},
                {'no': '0030', 'name': '低压浇注', 'type': '加工', 'wc': 'WC-CAST-HEAD', 'prep': 18, 'run': 40, 'out': 'MAT-HEAD-CAST', 'content': '执行缸盖低压浇注与保压凝固', 'materials': [], 'steps': ['执行浇注曲线并记录关键参数', '完成保压和冷却节拍控制']},
                {'no': '0040', 'name': '切冒口与抛丸清理', 'type': '加工', 'wc': 'WC-CAST-HEAD', 'prep': 12, 'run': 28, 'out': 'MAT-HEAD-CAST', 'content': '完成切冒口和表面清理', 'materials': [], 'steps': ['去除浇冒口与多余飞边', '抛丸后转入待检工位']},
                {'no': '0050', 'name': 'X光探伤与尺寸抽检', 'type': '检验', 'wc': 'WC-CAST-QA', 'prep': 10, 'run': 20, 'out': 'MAT-HEAD-CAST', 'content': '完成气道和水套区域探伤', 'materials': [], 'steps': ['重点检查气门座附近缩松', '抽检关键安装面尺寸']},
                {'no': '0060', 'name': '厂际转工至机加工厂', 'type': '厂际转工', 'wc': 'WC-CAST-TRANSFER', 'prep': 8, 'run': 18, 'out': 'MAT-HEAD-CAST', 'content': '缸盖铸件转入机加工厂在制库', 'materials': [], 'steps': ['生成缸盖转工批次', '转运至机加工厂缸盖在制库']},
            ],
        },
        {
            'code': 'RT-HEAD-MACH-A01', 'name': '缸盖精密机加工艺', 'route_spec': '机加', 'biz': 'BIZ-MACH', 'material': 'MAT-HEAD-FIN', 'proc_spec': '机械加工专业', 'remark': '机加工厂完成缸盖火面、导管和孔系加工',
            'ops': [
                {'no': '0010', 'name': '火面精铣与基准定位', 'type': '加工', 'wc': 'WC-MACH-HEAD', 'prep': 16, 'run': 45, 'out': 'MAT-HEAD-ROUGH', 'content': '建立缸盖机加工定位基准并完成火面初加工', 'materials': [('MAT-HEAD-CAST', 1)], 'steps': ['装夹缸盖铸件并确认基准销', '完成火面精铣与关键孔预加工']},
                {'no': '0020', 'name': '燃烧室与导管孔系加工', 'type': '加工', 'wc': 'WC-MACH-HEAD', 'prep': 15, 'run': 55, 'out': 'MAT-HEAD-ROUGH', 'content': '完成燃烧室、气门导管和火花塞孔加工', 'materials': [], 'steps': ['加工燃烧室型面和喷油器座孔', '完成导管孔与火花塞孔加工']},
                {'no': '0030', 'name': '凸轮孔系与端面精加工', 'type': '加工', 'wc': 'WC-MACH-HEAD', 'prep': 15, 'run': 50, 'out': 'MAT-HEAD-FIN', 'content': '完成凸轮轴孔系和安装端面加工', 'materials': [], 'steps': ['加工凸轮轴孔系并校核同轴度', '精加工进排气侧安装面']},
                {'no': '0040', 'name': '清洗与去毛刺', 'type': '加工', 'wc': 'WC-MACH-HEAD', 'prep': 10, 'run': 20, 'out': 'MAT-HEAD-FIN', 'content': '完成缸盖清洗、去毛刺和孔道吹扫', 'materials': [], 'steps': ['高压清洗并清除铝屑', '人工复核油道水道毛刺状态']},
                {'no': '0050', 'name': '气密试验与尺寸终检', 'type': '检验', 'wc': 'WC-MACH-CMM', 'prep': 12, 'run': 25, 'out': 'MAT-HEAD-FIN', 'content': '完成缸盖气密检测与关键尺寸放行', 'materials': [], 'steps': ['执行水套气密试验', '完成关键尺寸与平面度判定']},
                {'no': '0060', 'name': '厂际转工至缸盖装配', 'type': '厂际转工', 'wc': 'WC-MACH-TRANSFER', 'prep': 8, 'run': 20, 'out': 'MAT-HEAD-FIN', 'content': '缸盖精加工件转入总装工厂', 'materials': [], 'steps': ['生成缸盖转工单据', '转运至缸盖装配线边库']},
            ],
        },
        {
            'code': 'RT-CRANK-MACH-A01', 'name': '曲轴机加工与外协热处理工艺', 'route_spec': '机加', 'biz': 'BIZ-MACH', 'material': 'MAT-CRANK-FIN', 'proc_spec': '机械加工专业', 'remark': '机加工厂完成曲轴车磨、外协热处理和终检',
            'ops': [
                {'no': '0010', 'name': '曲轴基准车削', 'type': '加工', 'wc': 'WC-MACH-CRANK', 'prep': 18, 'run': 45, 'out': 'MAT-CRANK-ROUGH', 'content': '完成曲轴端面、中心孔和基准外圆车削', 'materials': [('MAT-CRANK-FORG', 1)], 'steps': ['装夹曲轴锻坯并校正中心孔', '完成端面和基准外圆车削']},
                {'no': '0020', 'name': '主轴颈与连杆颈磨削', 'type': '加工', 'wc': 'WC-MACH-CRANK', 'prep': 16, 'run': 55, 'out': 'MAT-CRANK-ROUGH', 'content': '完成关键轴颈磨削和圆角过渡控制', 'materials': [], 'steps': ['磨削主轴颈和连杆颈', '校核圆角和表面粗糙度']},
                {'no': '0030', 'name': '外协调质与氮化', 'type': '外委', 'wc': 'WC-OUT-HT', 'prep': 12, 'run': 240, 'out': 'MAT-CRANK-HT', 'content': '通过外协热处理提升曲轴疲劳强度', 'materials': [], 'steps': ['生成外协委外单和批次标识', '完成调质与氮化回厂检收']},
                {'no': '0040', 'name': '抛光与动平衡校正', 'type': '加工', 'wc': 'WC-MACH-CRANK', 'prep': 14, 'run': 40, 'out': 'MAT-CRANK-FIN', 'content': '完成曲轴抛光和动平衡校正', 'materials': [], 'steps': ['抛光关键轴颈并控制粗糙度', '执行动平衡校正并记录补偿值']},
                {'no': '0050', 'name': '磁粉探伤与尺寸终检', 'type': '检验', 'wc': 'WC-MACH-CMM', 'prep': 10, 'run': 20, 'out': 'MAT-CRANK-FIN', 'content': '完成曲轴裂纹探伤和关键尺寸放行', 'materials': [], 'steps': ['执行磁粉探伤排查裂纹', '检测轴颈尺寸和跳动值']},
                {'no': '0060', 'name': '厂际转工至短缸装配', 'type': '厂际转工', 'wc': 'WC-MACH-TRANSFER', 'prep': 8, 'run': 18, 'out': 'MAT-CRANK-FIN', 'content': '曲轴成品件转入总装工厂', 'materials': [], 'steps': ['生成曲轴转工单据', '转运至短缸线边库']},
            ],
        },
        {
            'code': 'RT-CONROD-MACH-A01', 'name': '连杆机加工艺', 'route_spec': '机加', 'biz': 'BIZ-MACH', 'material': 'MAT-CONROD-FIN', 'proc_spec': '机械加工专业', 'remark': '机加工厂完成连杆孔系加工与重量分组选配',
            'ops': [
                {'no': '0010', 'name': '连杆端面铣削', 'type': '加工', 'wc': 'WC-MACH-CONROD', 'prep': 15, 'run': 35, 'out': 'MAT-CONROD-FIN', 'content': '完成连杆大小头端面基准加工', 'materials': [('MAT-CONROD-FORG', 4)], 'steps': ['装夹连杆锻坯并建立定位基准', '完成大小头端面加工']},
                {'no': '0020', 'name': '大小头孔镗珩', 'type': '加工', 'wc': 'WC-MACH-CONROD', 'prep': 12, 'run': 40, 'out': 'MAT-CONROD-FIN', 'content': '完成连杆大小头孔加工', 'materials': [], 'steps': ['粗镗大头孔与小头孔', '执行孔系珩磨并校核圆度']},
                {'no': '0030', 'name': '裂解配对与螺栓装配', 'type': '加工', 'wc': 'WC-MACH-CONROD', 'prep': 12, 'run': 30, 'out': 'MAT-CONROD-FIN', 'content': '完成裂解分割、配对和连杆螺栓预装', 'materials': [], 'steps': ['完成裂解分割并回配', '安装连杆螺栓并检查配合面']},
                {'no': '0040', 'name': '称重分组选配', 'type': '检验', 'wc': 'WC-MACH-CMM', 'prep': 8, 'run': 15, 'out': 'MAT-CONROD-FIN', 'content': '按重量差分组选配连杆', 'materials': [], 'steps': ['称量大小头重量', '完成配组并标识批次']},
                {'no': '0050', 'name': '厂际转工至短缸装配', 'type': '厂际转工', 'wc': 'WC-MACH-TRANSFER', 'prep': 8, 'run': 18, 'out': 'MAT-CONROD-FIN', 'content': '连杆成品件转入总装工厂', 'materials': [], 'steps': ['生成连杆转工单据', '转运至短缸装配线边库']},
            ],
        },
        {
            'code': 'RT-HEAD-ASM-A01', 'name': '缸盖总成装配工艺', 'route_spec': '装配', 'biz': 'BIZ-ASM', 'material': 'MAT-CYL-HEAD-ASM', 'proc_spec': '装配专业', 'remark': '总装工厂完成缸盖预装、相位确认和密封检查',
            'ops': [
                {'no': '0010', 'name': '气门油封与气门组件压装', 'type': '加工', 'wc': 'WC-ASM-HEAD', 'prep': 12, 'run': 30, 'out': 'MAT-CYL-HEAD-ASM', 'content': '完成缸盖油封、气门和弹簧组件装配', 'materials': [('MAT-HEAD-FIN', 1), ('MAT-VALVE-SET', 1)], 'steps': ['清洁缸盖装配面并压装油封', '安装气门、弹簧和锁片组件']},
                {'no': '0020', 'name': '凸轮轴与轴承盖装配', 'type': '加工', 'wc': 'WC-ASM-HEAD', 'prep': 10, 'run': 25, 'out': 'MAT-CYL-HEAD-ASM', 'content': '完成进排气凸轮轴装配和定位', 'materials': [('MAT-CAM-IN', 1), ('MAT-CAM-EX', 1)], 'steps': ['安装进排气凸轮轴', '按顺序拧紧轴承盖并记录角度']},
                {'no': '0030', 'name': '密封胶施涂与附件预装', 'type': '加工', 'wc': 'WC-ASM-HEAD', 'prep': 8, 'run': 18, 'out': 'MAT-CYL-HEAD-ASM', 'content': '完成关键密封面施胶和附件预装', 'materials': [('MAT-SEALANT-ASM', 1)], 'steps': ['按标准轨迹施涂密封胶', '完成必要附件与堵盖预装']},
                {'no': '0040', 'name': '配气相位与气密检查', 'type': '检验', 'wc': 'WC-ASM-LEAK', 'prep': 10, 'run': 20, 'out': 'MAT-CYL-HEAD-ASM', 'content': '完成配气相位校核和缸盖气密检查', 'materials': [], 'steps': ['校核凸轮相位与锁止状态', '执行气密检查并判定放行']},
                {'no': '0050', 'name': '厂内转工至长缸合装', 'type': '厂内转工', 'wc': 'WC-ASM-TRANSFER', 'prep': 6, 'run': 10, 'out': 'MAT-CYL-HEAD-ASM', 'content': '缸盖总成转入长缸合装工位', 'materials': [], 'steps': ['生成缸盖总成转工标签', '转运至长缸合装缓存区']},
            ],
        },
        {
            'code': 'RT-SHORT-BLK-A01', 'name': '短缸总成装配工艺', 'route_spec': '装配', 'biz': 'BIZ-ASM', 'material': 'MAT-SHORT-BLK', 'proc_spec': '装配专业', 'remark': '总装工厂完成曲轴、活塞连杆和主轴承盖装配',
            'ops': [
                {'no': '0010', 'name': '主轴承安装与曲轴下装', 'type': '加工', 'wc': 'WC-ASM-SHORT', 'prep': 15, 'run': 28, 'out': 'MAT-SHORT-BLK', 'content': '完成主轴承铺设和曲轴下装', 'materials': [('MAT-BLOCK-FIN', 1), ('MAT-BRG-MAIN-SET', 1), ('MAT-CRANK-FIN', 1)], 'steps': ['安装主轴承瓦并涂覆装配油', '下装曲轴并检测轴向间隙']},
                {'no': '0020', 'name': '连杆活塞分组与活塞环装配', 'type': '加工', 'wc': 'WC-ASM-SHORT', 'prep': 12, 'run': 25, 'out': 'MAT-SHORT-BLK', 'content': '完成活塞、连杆配组和活塞环装配', 'materials': [('MAT-CONROD-FIN', 4), ('MAT-PISTON-ASSY', 4), ('MAT-RING-SET', 4), ('MAT-BRG-CONROD-SET', 1)], 'steps': ['按缸别配组连杆和活塞', '安装活塞环并复核开口方向']},
                {'no': '0030', 'name': '活塞连杆总成压入', 'type': '加工', 'wc': 'WC-ASM-SHORT', 'prep': 10, 'run': 20, 'out': 'MAT-SHORT-BLK', 'content': '完成活塞连杆总成导向压入缸体', 'materials': [], 'steps': ['使用活塞环压装工具导向压入', '复核连杆方向与缸号一致性']},
                {'no': '0040', 'name': '主轴承盖拧紧与转矩角校验', 'type': '加工', 'wc': 'WC-ASM-SHORT', 'prep': 10, 'run': 18, 'out': 'MAT-SHORT-BLK', 'content': '完成主轴承盖螺栓分步拧紧', 'materials': [('MAT-BOLT-MAIN-SET', 1)], 'steps': ['按顺序完成预紧与终拧', '记录转矩角并完成复核']},
                {'no': '0050', 'name': '短缸旋转阻力检查', 'type': '检验', 'wc': 'WC-ASM-LEAK', 'prep': 8, 'run': 12, 'out': 'MAT-SHORT-BLK', 'content': '检查短缸旋转阻力和装配异常', 'materials': [], 'steps': ['测量曲轴旋转阻力', '复核异响和卡滞风险']},
                {'no': '0060', 'name': '厂内转工至长缸合装', 'type': '厂内转工', 'wc': 'WC-ASM-TRANSFER', 'prep': 6, 'run': 10, 'out': 'MAT-SHORT-BLK', 'content': '短缸总成转入长缸合装区域', 'materials': [], 'steps': ['绑定短缸序列标识', '转运至长缸合装工位']},
            ],
        },
        {
            'code': 'RT-LONG-BLK-A01', 'name': '长缸总成装配工艺', 'route_spec': '装配', 'biz': 'BIZ-ASM', 'material': 'MAT-LONG-BLK', 'proc_spec': '装配专业', 'remark': '总装工厂完成缸盖合装、正时系统和密封检查',
            'ops': [
                {'no': '0010', 'name': '缸盖垫放置与缸盖合装', 'type': '加工', 'wc': 'WC-ASM-FINAL', 'prep': 12, 'run': 22, 'out': 'MAT-LONG-BLK', 'content': '完成缸盖垫放置和缸盖总成合装', 'materials': [('MAT-SHORT-BLK', 1), ('MAT-CYL-HEAD-ASM', 1), ('MAT-HEAD-GASKET', 1)], 'steps': ['放置缸盖垫并复核朝向', '完成缸盖合装与定位']},
                {'no': '0020', 'name': '缸盖螺栓分步拧紧', 'type': '加工', 'wc': 'WC-ASM-FINAL', 'prep': 10, 'run': 18, 'out': 'MAT-LONG-BLK', 'content': '完成缸盖螺栓分步拧紧和角度校验', 'materials': [('MAT-BOLT-HEAD-SET', 1)], 'steps': ['执行预紧、复紧和终拧步骤', '完成关键拧紧数据追溯']},
                {'no': '0030', 'name': '正时链系统装配', 'type': '加工', 'wc': 'WC-ASM-FINAL', 'prep': 10, 'run': 20, 'out': 'MAT-LONG-BLK', 'content': '完成正时链条、导轨和涨紧器装配', 'materials': [('MAT-TIMING-KIT', 1)], 'steps': ['装配导轨与涨紧器', '校核正时标记和链条预紧状态']},
                {'no': '0040', 'name': '气门室盖密封装配', 'type': '加工', 'wc': 'WC-ASM-FINAL', 'prep': 8, 'run': 15, 'out': 'MAT-LONG-BLK', 'content': '完成气门室盖与上部密封装配', 'materials': [('MAT-COVER-VALVE', 1), ('MAT-SEALANT-ASM', 1)], 'steps': ['施胶并装配气门室盖', '复核周边密封和紧固件状态']},
                {'no': '0050', 'name': '长缸密封性检查', 'type': '检验', 'wc': 'WC-ASM-LEAK', 'prep': 10, 'run': 18, 'out': 'MAT-LONG-BLK', 'content': '完成长缸密封和关键接口检查', 'materials': [], 'steps': ['执行压力保持和泄漏判定', '复核进排气接口与密封面']},
                {'no': '0060', 'name': '厂内转工至整机总装', 'type': '厂内转工', 'wc': 'WC-ASM-TRANSFER', 'prep': 6, 'run': 10, 'out': 'MAT-LONG-BLK', 'content': '长缸总成转入整机总装区域', 'materials': [], 'steps': ['绑定长缸条码信息', '转运至整机总装工位']},
            ],
        },
        {
            'code': 'RT-FINAL-ASM-A01', 'name': '整机总装工艺', 'route_spec': '装配', 'biz': 'BIZ-ASM', 'material': 'MAT-ENG-20TGDI', 'proc_spec': '装配专业', 'remark': '总装工厂完成附件、燃油、电控和飞轮装配后转试验工厂',
            'ops': [
                {'no': '0010', 'name': '机油泵与前端附件装配', 'type': '加工', 'wc': 'WC-ASM-FINAL', 'prep': 12, 'run': 22, 'out': 'MAT-ENG-20TGDI', 'content': '完成机油泵及前端附件装配', 'materials': [('MAT-LONG-BLK', 1), ('MAT-PUMP-OIL', 1)], 'steps': ['装配机油泵并复核间隙', '完成前端附件安装']},
                {'no': '0020', 'name': '增压器及排气歧管装配', 'type': '加工', 'wc': 'WC-ASM-FINAL', 'prep': 10, 'run': 18, 'out': 'MAT-ENG-20TGDI', 'content': '完成涡轮增压器和排气歧管装配', 'materials': [('MAT-TURBO-CHARGER', 1), ('MAT-EXH-MANIFOLD', 1)], 'steps': ['装配排气歧管并复核平面度', '安装增压器并完成油路接口检查']},
                {'no': '0030', 'name': '燃油轨、喷油器与点火系统装配', 'type': '加工', 'wc': 'WC-ASM-FINAL', 'prep': 10, 'run': 20, 'out': 'MAT-ENG-20TGDI', 'content': '完成燃油系统和点火系统装配', 'materials': [('MAT-FUEL-RAIL', 1), ('MAT-INJECTOR', 4), ('MAT-IGNITION-COIL', 4), ('MAT-SPARK-PLUG', 4)], 'steps': ['装配喷油器和燃油轨', '装配点火线圈和火花塞并复核扭矩']},
                {'no': '0040', 'name': '飞轮与发动机线束装配', 'type': '加工', 'wc': 'WC-ASM-FINAL', 'prep': 10, 'run': 16, 'out': 'MAT-ENG-20TGDI', 'content': '完成飞轮、线束与传感器连接', 'materials': [('MAT-FLYWHEEL', 1), ('MAT-ENG-HARNESS', 1)], 'steps': ['装配飞轮并完成定位锁紧', '连接线束与关键传感器接口']},
                {'no': '0050', 'name': '条码绑定与整机电检', 'type': '检验', 'wc': 'WC-ASM-LEAK', 'prep': 8, 'run': 12, 'out': 'MAT-ENG-20TGDI', 'content': '完成整机条码绑定与电气连续性检查', 'materials': [], 'steps': ['绑定整机序列号与关键件号', '执行电检并确认接口状态']},
                {'no': '0060', 'name': '厂际转工至试验工厂', 'type': '厂际转工', 'wc': 'WC-ASM-TRANSFER', 'prep': 8, 'run': 16, 'out': 'MAT-ENG-20TGDI', 'content': '整机总成转入试验工厂冷试工位', 'materials': [], 'steps': ['生成整机转工单据', '转运至试验工厂待试区']},
            ],
        },
        {
            'code': 'RT-ENG-TEST-A01', 'name': '发动机冷试热试与EOL放行工艺', 'route_spec': '通用', 'biz': 'BIZ-TEST', 'material': 'MAT-ENG-20TGDI', 'proc_spec': '装配专业', 'remark': '试验工厂完成冷试、热试、EOL放行与包装入库',
            'ops': [
                {'no': '0010', 'name': '冷试与机油循环建立', 'type': '检验', 'wc': 'WC-TEST-COLD', 'prep': 12, 'run': 18, 'out': 'MAT-ENG-20TGDI', 'content': '完成冷试拖动、摩擦扭矩和机油循环验证', 'materials': [('MAT-TEST-OIL', 1)], 'steps': ['注入试验机油并建立油压', '执行冷试拖动并分析阻力曲线']},
                {'no': '0020', 'name': '热试性能标定', 'type': '检验', 'wc': 'WC-TEST-HOT', 'prep': 15, 'run': 30, 'out': 'MAT-ENG-20TGDI', 'content': '完成热试功率、油耗与怠速稳定性验证', 'materials': [('MAT-TEST-FUEL', 1)], 'steps': ['接入热试台完成点火启动', '记录功率、油耗和关键温压参数']},
                {'no': '0030', 'name': 'OBD报码与泄漏复判', 'type': '检验', 'wc': 'WC-TEST-EOL', 'prep': 10, 'run': 18, 'out': 'MAT-ENG-20TGDI', 'content': '完成报码、泄漏和功能复判', 'materials': [], 'steps': ['读取报码并清除临时故障', '执行泄漏复判和最终审核']},
                {'no': '0040', 'name': '防锈封存与包装', 'type': '加工', 'wc': 'WC-TEST-EOL', 'prep': 8, 'run': 15, 'out': 'MAT-ENG-20TGDI', 'content': '完成防锈封存、护具安装和包装', 'materials': [], 'steps': ['执行防锈封存和接口防护', '安装周转护具并完成包装标签']},
                {'no': '0050', 'name': '转入成品库', 'type': '厂内转工', 'wc': 'WC-TEST-EOL', 'prep': 6, 'run': 10, 'out': 'MAT-ENG-20TGDI', 'content': '试验放行后的整机转入成品库', 'materials': [], 'steps': ['生成成品入库单据', '转运至成品库指定货位']},
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


def build_variant(namespace: str, volume_profile: str | None = None) -> dict:
    reset()
    build_organizations()
    build_users()
    build_resources()
    build_materials()
    build_mboms()
    build_routes()
    apply_profile(seed, 'automotive_engine')
    apply_scene_upgrade(seed, 'automotive_engine', namespace, volume_profile=volume_profile)
    apply_production_orders(seed, 'automotive_engine', namespace)
    return seed


def build() -> dict:
    return build_variant(NAMESPACE)


def counts() -> dict[str, int]:
    result: dict[str, int] = {}
    for workbook in seed['workbooks'].values():
        for sheet_name, rows in workbook.items():
            result[sheet_name] = len(rows)
    return result


def main() -> None:
    for asset_name, namespace, volume_profile in VARIANT_SPECS:
        build_variant(namespace, volume_profile)
        asset_path = ASSET_PATH.parent / asset_name
        asset_path.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding='utf-8-sig')
        print(f'已生成: {asset_path}')
        for sheet_name, total in counts().items():
            print(f'{sheet_name}: {total}')


if __name__ == '__main__':
    main()
