from __future__ import annotations

from copy import deepcopy

from production_order_seed import apply_production_orders
from scene_seed_upgrades import apply_scene_upgrade

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
RELEASE_TIME = '2025-04-08 08:00:00'
RELEASE_USER = ''


class SeedBuilder:
    def __init__(self, metadata: dict):
        self.seed = {
            'metadata': metadata,
            'external_references': ['0'],
            'workbooks': {
                WB_SYSTEM: {SH_ADMIN: [], SH_BIZ: [], SH_USER: []},
                WB_FACTORY: {
                    SH_SUP: [], SH_EQ: [], SH_EQ_USER: [], SH_TOOL: [], SH_TOOL_INS: [], SH_TOOL_MNT: [],
                    SH_WC: [], SH_WC_USER: [], SH_WC_SUP: [], SH_WC_EQ: [], SH_WH: [], SH_LOC: [], SH_PLIB: [],
                },
                WB_PRODUCT: {SH_MAT: [], SH_MBOM: [], SH_MBOM_NODE: [], SH_ROUTE: [], SH_OP: [], SH_SEQ: [], SH_OPMAT: [], SH_STEP: []},
            },
        }
        self.materials: dict[str, dict] = {}
        self.proc: set[tuple] = set()
        self.eq_user: set[tuple] = set()
        self.wc_user: set[tuple] = set()
        self.wc_sup: set[tuple] = set()
        self.wc_eq: set[tuple] = set()
        self.mbom_seq: dict[int, int] = {}

    def add(self, workbook: str, sheet: str, row: dict) -> None:
        self.seed['workbooks'][workbook][sheet].append(row)

    def uniq(self, store: set, key: tuple, workbook: str, sheet: str, row: dict) -> None:
        if key not in store:
            store.add(key)
            self.add(workbook, sheet, row)

    def next_mbom(self, level: int) -> int:
        if level not in self.mbom_seq:
            self.mbom_seq[level] = 10
        value = self.mbom_seq[level]
        self.mbom_seq[level] += 10
        return value

    def a_admin(self, parent: str, org_type: str, code: str, name: str, short: str, remark: str = '') -> None:
        row = {'*父组织编码': parent, '行政组织类型': org_type, '*编码': code, '*名称': name, '简称': short}
        if remark:
            row['备注'] = remark
        self.add(WB_SYSTEM, SH_ADMIN, row)

    def a_biz(self, parent: str, code: str, name: str, short: str, org_type: str, admin: str, factory_type: str = '', remark: str = '') -> None:
        row = {'*父组织编码': parent, '*密级': SEC, '*编码': code, '*名称': name, '简称': short, '工厂组织类型': org_type, '行政组织编码': admin}
        if factory_type:
            row['工厂类型'] = factory_type
        if remark:
            row['备注'] = remark
        self.add(WB_SYSTEM, SH_BIZ, row)

    def a_user(self, code: str, name: str, level: str, gender: str, admin: str, biz: str, remark: str = '', phone: str = '', email: str = '', birthday: str = '', id_no: str = '') -> None:
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
        self.add(WB_SYSTEM, SH_USER, row)

    def a_sup(self, code: str, name: str, short: str, remark: str = '') -> None:
        row = {'*密级': SEC, '*编码': code, '*名称': name, '简称': short, '启用': YES}
        if remark:
            row['备注'] = remark
        self.add(WB_FACTORY, SH_SUP, row)

    def a_eq(self, code: str, name: str, model: str, biz: str, bottle: str = NO, remark: str = '') -> None:
        row = {'*名称': name, '型号规格': model, '瓶颈资源': bottle, '*编码': code, '*密级': SEC, '*工厂组织': biz}
        if remark:
            row['备注'] = remark
        self.add(WB_FACTORY, SH_EQ, row)

    def l_eq_user(self, eq_code: str, user_code: str) -> None:
        self.uniq(self.eq_user, (eq_code, user_code), WB_FACTORY, SH_EQ_USER, {'*设备编码': eq_code, '*用户': user_code})

    def a_tool(self, code: str, name: str, material_category: str, make_type: str, tooling_category: str, feature: str, model: str = '', spec: str = '', remark: str = '', life_times: int | None = None, life_days: int | None = None) -> None:
        row = {
            '*物料分类': TOOL_CLASS, '*名称': name, '物料类别': material_category, '图号': code, '型号': model, '规格': spec,
            '*制造类型': make_type, '计量单位': '个', '特性分类': feature, '启用批次标记': NO, '启用序列号标记': NO,
            '工装类别': tooling_category, '一次性工装标记': NO, '单件工装标记': NO, '物料阶段': STAGE,
            '发布版本时间': RELEASE_TIME, '发布人': RELEASE_USER, '*版本号': VER, '*编码': code, '*密级': SEC,
        }
        if remark:
            row['备注'] = remark
        if life_times is not None:
            row['理论寿命(次)'] = life_times
        if life_days is not None:
            row['理论寿命(天)'] = life_days
        self.add(WB_FACTORY, SH_TOOL, row)

    def a_wc(self, code: str, name: str, biz: str, wc_type: str, wc_class: str, remark: str = '') -> None:
        row = {'*名称': name, '*类型': wc_type, '*分类': wc_class, '*编码': code, '*密级': SEC, '*工厂组织': biz}
        if remark:
            row['备注'] = remark
        self.add(WB_FACTORY, SH_WC, row)

    def l_wc_user(self, wc_code: str, user_code: str) -> None:
        self.uniq(self.wc_user, (wc_code, user_code), WB_FACTORY, SH_WC_USER, {'*工作中心编码': wc_code, '*用户': user_code})

    def l_wc_sup(self, wc_code: str, sup_code: str) -> None:
        self.uniq(self.wc_sup, (wc_code, sup_code), WB_FACTORY, SH_WC_SUP, {'*工作中心编码': wc_code, '*供应商': sup_code})

    def l_wc_eq(self, wc_code: str, eq_code: str) -> None:
        self.uniq(self.wc_eq, (eq_code, wc_code), WB_FACTORY, SH_WC_EQ, {'*设备编码': eq_code, '*工作中心编码': wc_code})

    def a_wh(self, code: str, name: str, biz: str, biz_type: str, mode: str = '普通库房', remark: str = '') -> None:
        row = {'*工厂组织': biz, '*名称': name, '作业模式': mode, '*业务类型': biz_type, '*编码': code, '*密级': SEC}
        if remark:
            row['备注'] = remark
        self.add(WB_FACTORY, SH_WH, row)

    def a_loc(self, code: str, name: str, biz: str, warehouse: str, remark: str = '') -> None:
        row = {'*工厂组织': biz, '*库房编码': warehouse, '*名称': name, '*编码': code, '*密级': SEC}
        if remark:
            row['备注'] = remark
        self.add(WB_FACTORY, SH_LOC, row)

    def a_proc(self, name: str, op_type: str, wc_code: str, prep: int, run: int, spec: str, content: str = '') -> None:
        self.uniq(self.proc, (name, wc_code), WB_FACTORY, SH_PLIB, {
            '序专业类型': spec, '*名称': name, '*工序类型': op_type, '*工作中心编码': wc_code,
            '*定额准备时间': prep, '*定额加工时间': run, '执行标记': YES, '*时间单位': TIME,
            '产出比': 1, '工序内容': content or name, '*密级': SEC,
        })

    def a_mat(self, code: str, name: str, category: str, make_type: str, feature: str, drawing: str, unit: str = '个', model: str = '', spec: str = '', remark: str = '', batch: str = YES, serial: str = NO) -> None:
        row = {
            '*物料分类': MAT_CLASS, '*名称': name, '物料类别': category, '图号': drawing, '型号': model, '规格': spec,
            '*制造类型': make_type, '计量单位': unit, '特性分类': feature, '启用批次标记': batch,
            '启用序列号标记': serial, '物料阶段': STAGE, '发布版本时间': RELEASE_TIME, '发布人': RELEASE_USER,
            '*版本号': VER, '*编码': code, '*密级': SEC,
        }
        if remark:
            row['备注'] = remark
        self.add(WB_PRODUCT, SH_MAT, row)
        self.materials[code] = {'name': name, 'category': category, 'make': make_type, 'drawing': drawing, 'unit': unit}

    def a_mbom(self, code: str, material_code: str, name: str, remark: str = '') -> None:
        row = {'*物料版本号': VER, '*物料编码': material_code, '*版本号': VER, '*编码': code, '*密级': SEC, '名称': name}
        if remark:
            row['备注'] = remark
        self.add(WB_PRODUCT, SH_MBOM, row)

    def a_mbom_node(self, mbom_code: str, level: int, material_code: str, qty: int, parent_material: str = '0', parent_version: str = '') -> None:
        meta = self.materials[material_code]
        self.add(WB_PRODUCT, SH_MBOM_NODE, {
            '*MBOM版本号': VER, '*MBOM编码': mbom_code, '*物料编码': material_code, '物料名称': meta['name'],
            '物料图号': meta['drawing'], '*物料版本': VER, '*物料类别': meta['category'], '制造类型': meta['make'],
            '数量': qty, '计量单位': meta['unit'], '*层级': level, '*序号': self.next_mbom(level), '物料阶段': STAGE,
            '父物料编码': parent_material, '父物料版本': parent_version,
        })

    def a_route(self, code: str, name: str, route_spec: str, biz: str, material_code: str, remark: str = '') -> None:
        row = {'*名称': name, '*工艺类型': ROUTE_TYPE, '工艺专业': route_spec, '物料版本号': VER, '物料编码': material_code, '*版本号': VER, '*编码': code, '*密级': SEC, '*工厂组织': biz}
        if remark:
            row['备注'] = remark
        self.add(WB_PRODUCT, SH_ROUTE, row)

    def a_op(self, route_code: str, op_no: str, name: str, op_type: str, wc_code: str, prep: int, run: int, output_code: str, spec: str, content: str = '') -> None:
        self.add(WB_PRODUCT, SH_OP, {
            '*工序号': op_no, '*工序类型': op_type, '工序内容': content or name, '*工作中心编码': wc_code,
            '*定额辅助工时': prep, '*定额加工时间': run, '*时间单位': TIME, '执行标记': YES, '产出比': 1,
            '*工艺路线版本号': VER, '*工艺路线编码': route_code, '*工序名称': name,
            '产出物料版本号': VER, '产出物料编码': output_code, '工序专业类型': spec,
        })
        self.a_proc(name, op_type, wc_code, prep, run, spec, content)

    def a_seq(self, route_code: str, op_no: str, prev_op: str, rel: str = SEQ_TYPE) -> None:
        self.add(WB_PRODUCT, SH_SEQ, {'*接续关系': rel, '*工序号': op_no, '*上道工序号': prev_op, '*工艺路线版本号': VER, '*工艺路线编码': route_code})

    def a_opmat(self, route_code: str, op_no: str, material_code: str, qty: int) -> None:
        self.add(WB_PRODUCT, SH_OPMAT, {'*工艺路线版本号': VER, '*工艺路线编码': route_code, '*物料版本号': VER, '*物料编码': material_code, '*工序号': op_no, '数量': qty})

    def a_step(self, route_code: str, op_no: str, step_no: str, name: str, content: str) -> None:
        self.add(WB_PRODUCT, SH_STEP, {'*工艺路线版本号': VER, '*工艺路线编码': route_code, '*工序号': op_no, '*工步序号': step_no, '*工步名称': name, '工步内容': content})

    def build_from_config(self, config: dict) -> None:
        for row in config.get('admins', []):
            self.a_admin(*row)
        for row in config.get('bizs', []):
            self.a_biz(*row)
        for row in config.get('users', []):
            self.a_user(*row)
        for row in config.get('suppliers', []):
            self.a_sup(**row)
        for row in config.get('work_centers', []):
            self.a_wc(**row)
        for row in config.get('equipments', []):
            self.a_eq(**row)
        for row in config.get('tools', []):
            self.a_tool(**row)
        for row in config.get('wc_user_links', []):
            self.l_wc_user(*row)
        for row in config.get('wc_eq_links', []):
            self.l_wc_eq(*row)
        for row in config.get('wc_sup_links', []):
            self.l_wc_sup(*row)
        for row in config.get('eq_user_links', []):
            self.l_eq_user(*row)
        for row in config.get('warehouses', []):
            self.a_wh(*row)
        for row in config.get('locations', []):
            self.a_loc(*row)
        for row in config.get('materials', []):
            self.a_mat(**row)
        for row in config.get('mboms', []):
            self.a_mbom(row['code'], row['material_code'], row['name'], row.get('remark', ''))
            for node in row.get('nodes', []):
                self.a_mbom_node(row['code'], node['level'], node['material_code'], node['qty'], node.get('parent_material', '0'), node.get('parent_version', ''))
        for route in config.get('routes', []):
            self.a_route(route['code'], route['name'], route['route_spec'], route['biz'], route['material_code'], route.get('remark', ''))
            prev_no = ''
            for op in route.get('ops', []):
                self.a_op(route['code'], op['no'], op['name'], op['type'], op['wc'], op['prep'], op['run'], op['out'], route['proc_spec'], op.get('content', ''))
                if prev_no:
                    self.a_seq(route['code'], op['no'], prev_no)
                for material_code, qty in op.get('materials', []):
                    self.a_opmat(route['code'], op['no'], material_code, qty)
                for index, step in enumerate(op.get('steps', []), start=1):
                    if isinstance(step, (list, tuple)):
                        step_name, step_content = step
                    else:
                        step_name = step
                        step_content = step
                    self.a_step(route['code'], op['no'], f'{index * 10:02d}', step_name, step_content)
                prev_no = op['no']


def build_seed(config: dict, scenario: str, namespace: str, volume_profile: str) -> dict:
    metadata = deepcopy(config['metadata'])
    metadata['default_version'] = VER
    metadata['default_security'] = SEC
    metadata['volume_profile'] = volume_profile
    builder = SeedBuilder(metadata)
    builder.build_from_config(config)
    seed = builder.seed
    apply_scene_upgrade(seed, scenario, namespace, volume_profile=volume_profile)
    apply_production_orders(seed, scenario, namespace)
    return seed


def summarize_seed(seed: dict) -> dict:
    return {'metadata': seed['metadata'], 'counts': {workbook: {sheet: len(rows) for sheet, rows in sheets.items()} for workbook, sheets in seed['workbooks'].items()}}

