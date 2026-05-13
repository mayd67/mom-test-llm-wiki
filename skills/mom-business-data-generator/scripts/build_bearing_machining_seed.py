from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

from gearbox_seed_support import (
    CAT_AUX,
    CAT_PART,
    CAT_RAW,
    FEATURE_IMPORTANT,
    FEATURE_KEY,
    FEATURE_NORMAL,
    MAKE_BUY,
    MAKE_SELF,
    NO,
    YES,
    SeedBuilder,
    summarize_seed,
)
from production_order_seed import apply_production_orders
from scene_seed_upgrades import (
    apply_namespace,
    clear_tool_strategy_relations,
    filter_wc_supplier_relations,
    normalize_poc_security,
    normalize_release_user,
    normalize_sequence_relations,
    normalize_storage_factory_org,
    normalize_user_codes,
)

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

SCENARIO = 'bearing_machining'
NAMESPACE = 'BRG20S01'
VOLUME_PROFILE = '标准版'
ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'bearing_machining_seed.json'


def build_config() -> dict:
    admins = [
        ('0', '公司', 'Adm001', '启航轴承制造有限公司', '启航轴承'),
        ('Adm001', '部门', 'Adm002', '工艺技术部', '工艺技术'),
        ('Adm001', '部门', 'Adm003', '生产运营部', '生产运营'),
        ('Adm001', '部门', 'Adm004', '质量管理部', '质量管理'),
        ('Adm001', '部门', 'Adm005', '设备工装部', '设备工装'),
        ('Adm001', '工厂', 'Adm006', '轴承机加工厂', '轴承工厂', '负责轴承套圈车削、热处理、磨削和终检入库'),
    ]

    bizs = [
        ('0', 'Biz001', '启航轴承制造有限公司', '启航轴承', '公司', 'Adm001', '', '单工厂轴承机加工场景'),
        ('Biz001', 'Biz002', '工艺技术部', '工艺技术', '部门', 'Adm002'),
        ('Biz001', 'Biz003', '生产运营部', '生产运营', '部门', 'Adm003'),
        ('Biz001', 'Biz004', '质量管理部', '质量管理', '部门', 'Adm004'),
        ('Biz001', 'Biz005', '设备工装部', '设备工装', '部门', 'Adm005'),
        ('Biz001', 'Biz006', '轴承机加工厂', '轴承工厂', '工厂', 'Adm006', '机械加工专业', '标准版轴承机加工工厂'),
        ('Biz006', 'Biz007', '车削车间', '车削车间', '车间', 'Adm006'),
        ('Biz006', 'Biz008', '热处理车间', '热处理车间', '车间', 'Adm006'),
        ('Biz006', 'Biz009', '磨削车间', '磨削车间', '车间', 'Adm006'),
        ('Biz006', 'Biz010', '仓储物流车间', '仓储物流', '车间', 'Adm006'),
        ('Biz006', 'Biz011', '终检包装车间', '终检包装', '车间', 'Adm006'),
        ('Biz007', 'Biz012', '车削甲班', '车削甲班', '班组', 'Adm006'),
        ('Biz008', 'Biz013', '热处理甲班', '热处理甲班', '班组', 'Adm006'),
        ('Biz009', 'Biz014', '磨削甲班', '磨削甲班', '班组', 'Adm006'),
        ('Biz011', 'Biz015', '终检包装甲班', '终检包装甲班', '班组', 'Adm006'),
    ]

    users = [
        ('U001', '沈知远', '重要', '男', 'Adm002', 'Biz002', '工艺负责人'),
        ('U002', '叶清和', '重要', '女', 'Adm002', 'Biz002', '工艺工程师'),
        ('U003', '何若川', '重要', '男', 'Adm003', 'Biz003', '主计划员'),
        ('U004', '顾言溪', '一般', '女', 'Adm003', 'Biz003', '生产计划员'),
        ('U005', '宋承安', '一般', '男', 'Adm004', 'Biz004', '质量工程师'),
        ('U006', '陆星辞', '一般', '男', 'Adm004', 'Biz004', '终检主管'),
        ('U007', '周书宁', '一般', '女', 'Adm005', 'Biz005', '设备工程师'),
        ('U008', '许见山', '一般', '男', 'Adm005', 'Biz005', '工装工程师'),
        ('U009', '唐知夏', '一般', '女', 'Adm006', 'Biz010', '仓储主管'),
        ('U010', '林见川', '一般', '男', 'Adm006', 'Biz010', '仓库管理员'),
        ('U011', '韩书远', '一般', '男', 'Adm006', 'Biz012', '车削班组长'),
        ('U012', '乔云舒', '一般', '女', 'Adm006', 'Biz012', '车削操作工'),
        ('U013', '苏景程', '一般', '男', 'Adm006', 'Biz012', '车削操作工'),
        ('U014', '季安和', '一般', '男', 'Adm006', 'Biz012', '来料检验员'),
        ('U015', '温清妍', '一般', '女', 'Adm006', 'Biz013', '热处理班组长'),
        ('U016', '邵言舟', '一般', '男', 'Adm006', 'Biz013', '热处理操作工'),
        ('U017', '沈可欣', '一般', '女', 'Adm006', 'Biz013', '热处理操作工'),
        ('U018', '郑明哲', '一般', '男', 'Adm006', 'Biz014', '磨削班组长'),
        ('U019', '陆雨桐', '一般', '女', 'Adm006', 'Biz014', '磨削操作工'),
        ('U020', '周景程', '一般', '男', 'Adm006', 'Biz014', '磨削操作工'),
        ('U021', '许安宁', '一般', '女', 'Adm006', 'Biz015', '终检员'),
        ('U022', '宋知行', '一般', '男', 'Adm006', 'Biz015', '包装入库员'),
    ]

    suppliers = [
        {'code': 'Sup001', 'name': '华北轴承钢材料有限公司', 'short': '华北轴承钢', 'remark': '供应GCr15轴承钢环件毛坯'},
        {'code': 'Sup002', 'name': '瑞成热处理介质有限公司', 'short': '瑞成介质', 'remark': '供应淬火介质与保护气氛耗材'},
        {'code': 'Sup003', 'name': '精锋数控刀具有限公司', 'short': '精锋刀具', 'remark': '供应车削刀片和刀杆'},
        {'code': 'Sup004', 'name': '优博砂轮科技有限公司', 'short': '优博砂轮', 'remark': '供应磨削砂轮与修整件'},
        {'code': 'Sup005', 'name': '恒安工业包装有限公司', 'short': '恒安包装', 'remark': '供应包装盒、防锈袋和标签'},
        {'code': 'Sup006', 'name': '精测量仪服务有限公司', 'short': '精测量仪', 'remark': '供应量检具和校准服务'},
    ]

    work_centers = [
        {'code': 'Wc001', 'name': '来料检验工位', 'biz': 'Biz010', 'wc_type': '组织', 'wc_class': '检验', 'remark': '负责毛坯和辅料来料确认'},
        {'code': 'Wc002', 'name': '车削线A', 'biz': 'Biz007', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责外圈端面和外圆车削'},
        {'code': 'Wc003', 'name': '车削线B', 'biz': 'Biz007', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责沟道精车与尺寸复核'},
        {'code': 'Wc004', 'name': '热处理线A', 'biz': 'Biz008', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责淬火处理'},
        {'code': 'Wc005', 'name': '热处理线B', 'biz': 'Biz008', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责回火与硬度确认'},
        {'code': 'Wc006', 'name': '磨削线A', 'biz': 'Biz009', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责沟道粗精磨'},
        {'code': 'Wc007', 'name': '磨削线B', 'biz': 'Biz009', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责外圆精磨与超精'},
        {'code': 'Wc008', 'name': '清洗防锈工位', 'biz': 'Biz011', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责清洗烘干与防锈'},
        {'code': 'Wc009', 'name': '终检工位', 'biz': 'Biz011', 'wc_type': '组织', 'wc_class': '检验', 'remark': '负责尺寸、圆度和外观终检'},
        {'code': 'Wc010', 'name': '包装入库工位', 'biz': 'Biz011', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责贴标、包装和入库'},
    ]

    equipment_specs = [
        ('Eq001', '外圈数控车床1', 'CKA6136', 'Biz007', YES),
        ('Eq002', '外圈数控车床2', 'CKA6136', 'Biz007', NO),
        ('Eq003', '沟道车床1', 'QXC-80', 'Biz007', YES),
        ('Eq004', '沟道车床2', 'QXC-80', 'Biz007', NO),
        ('Eq005', '自动上下料车床', 'AutoTurn-12', 'Biz007', NO),
        ('Eq006', '尺寸在线检测站', 'Gauge-20', 'Biz007', NO),
        ('Eq007', '可控气氛淬火炉1', 'RQ-160', 'Biz008', YES),
        ('Eq008', '可控气氛淬火炉2', 'RQ-160', 'Biz008', NO),
        ('Eq009', '回火炉', 'HW-120', 'Biz008', NO),
        ('Eq010', '硬度检测台', 'HD-200', 'Biz008', NO),
        ('Eq011', '磨削线体1', 'MKS1332', 'Biz009', YES),
        ('Eq012', '磨削线体2', 'MKS1332', 'Biz009', NO),
        ('Eq013', '外圆磨床1', 'MQ1350', 'Biz009', YES),
        ('Eq014', '外圆磨床2', 'MQ1350', 'Biz009', NO),
        ('Eq015', '超精机', 'CJ-6206', 'Biz009', NO),
        ('Eq016', '砂轮修整站', 'XZ-12', 'Biz009', NO),
        ('Eq017', '清洗烘干机', 'QX-20', 'Biz011', NO),
        ('Eq018', '激光打标机', 'LB-08', 'Biz011', NO),
        ('Eq019', '圆度粗糙度检测仪', 'RD-6206', 'Biz011', NO),
        ('Eq020', '气动量仪', 'Air-6206', 'Biz011', NO),
    ]
    equipments = [
        {'code': code, 'name': name, 'model': model, 'biz': biz, 'bottle': bottle}
        for code, name, model, biz, bottle in equipment_specs
    ]

    tool_specs = [
        ('Tl001', '外圈车削定位夹具', '专用工装', FEATURE_KEY, 'JG-6206-01', '端面外圆定位', '用于端面和外圆车削定位'),
        ('Tl002', '沟道车削夹具', '专用工装', FEATURE_KEY, 'JG-6206-02', '沟道精车定位', '用于沟道精车定位'),
        ('Tl003', '热处理装炉托盘', '专用工装', FEATURE_IMPORTANT, 'JG-6206-03', '装炉承载', '用于热处理批量装炉'),
        ('Tl004', '热处理隔离篮筐', '工装备件', FEATURE_NORMAL, 'JG-6206-04', '热后周转', '用于热处理后隔离周转'),
        ('Tl005', '沟道磨削修整器', '通用工具', FEATURE_IMPORTANT, 'JG-6206-05', '砂轮修整', '用于沟道磨削砂轮修整'),
        ('Tl006', '外圆磨削顶尖', '通用工具', FEATURE_IMPORTANT, 'JG-6206-06', '磨削支撑', '用于外圆磨削定位支撑'),
        ('Tl007', '终检样圈', '专用工装', FEATURE_IMPORTANT, 'JG-6206-07', '尺寸复核', '用于终检基准复核'),
        ('Tl008', '圆度检具', '专用工装', FEATURE_KEY, 'JG-6206-08', '圆度复核', '用于圆度与跳动复核'),
        ('Tl009', '打标定位工装', '专用工装', FEATURE_NORMAL, 'JG-6206-09', '打标定位', '用于激光打标定位'),
        ('Tl010', '包装周转托盘', '工装备件', FEATURE_NORMAL, 'JG-6206-10', '包装周转', '用于终检后包装周转'),
        ('Tl011', '换刀预调台', '通用工具', FEATURE_NORMAL, 'JG-6206-11', '刀具预调', '用于刀具预调和刀补确认'),
        ('Tl012', '量仪校准块', '通用工具', FEATURE_IMPORTANT, 'JG-6206-12', '量仪校准', '用于气动量仪日常校准'),
    ]
    tools = [
        {
            'code': code,
            'name': name,
            'material_category': CAT_PART,
            'make_type': MAKE_SELF if category != '通用工具' else MAKE_BUY,
            'tooling_category': category,
            'feature': feature,
            'model': model,
            'spec': spec,
            'remark': remark,
            'life_times': 50000,
            'life_days': 365,
        }
        for code, name, category, feature, model, spec, remark in tool_specs
    ]

    warehouses = [
        ('Wh001', '原料库', 'Biz006', 'ERP一级库', '普通库房', '存放轴承钢环件毛坯和关键外购件'),
        ('Wh002', '辅料库', 'Biz006', 'ERP二级库', '普通库房', '存放清洗剂、防锈油、标签和包装辅料'),
        ('Wh003', '车削在制库', 'Biz006', '车间二级库', '普通库房', '存放车削完成待热处理的在制品'),
        ('Wh004', '热后在制库', 'Biz006', '车间二级库', '普通库房', '存放热处理完成待磨削的在制品'),
        ('Wh005', '成品库', 'Biz006', 'ERP一级库', '普通库房', '存放终检放行后的轴承外圈成品'),
    ]

    location_specs = [
        ('Loc001', '毛坯A区', 'Wh001'), ('Loc002', '毛坯B区', 'Wh001'), ('Loc003', '毛坯待检区', 'Wh001'), ('Loc004', '原料备料区', 'Wh001'),
        ('Loc005', '防锈油区', 'Wh002'), ('Loc006', '清洗剂区', 'Wh002'), ('Loc007', '标签包装区', 'Wh002'), ('Loc008', '辅料待发区', 'Wh002'),
        ('Loc009', '车削待转区', 'Wh003'), ('Loc010', '车削合格区', 'Wh003'), ('Loc011', '车削复检区', 'Wh003'), ('Loc012', '车削夜班周转区', 'Wh003'),
        ('Loc013', '热后待磨区', 'Wh004'), ('Loc014', '热后隔离区', 'Wh004'), ('Loc015', '热后抽检区', 'Wh004'), ('Loc016', '热后合格区', 'Wh004'),
        ('Loc017', '成品待包区', 'Wh005'), ('Loc018', '成品待发区', 'Wh005'), ('Loc019', '样件保留区', 'Wh005'), ('Loc020', '成品复核区', 'Wh005'),
    ]
    locations = [(code, name, 'Biz006', warehouse) for code, name, warehouse in location_specs]

    material_specs = [
        ('Mat001', 'GCr15轴承钢环件毛坯', CAT_RAW, MAKE_BUY, FEATURE_IMPORTANT, 'DW-6206-001', '个', '', '6206外圈毛坯', '外购轴承钢热轧环件毛坯'),
        ('Mat002', '6206外圈车削件', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'DW-6206-002', '个', '', '车削半成品', '完成端面和沟道车削后的半成品'),
        ('Mat003', '6206外圈热处理件', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'DW-6206-003', '个', '', '热后半成品', '完成淬火回火后的半成品'),
        ('Mat004', '6206深沟球轴承外圈', CAT_PART, MAKE_SELF, FEATURE_KEY, 'DW-6206-004', '个', '', '成品外圈', '机加工完成后的轴承外圈成品'),
        ('Mat005', '磨削液', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'DW-6206-005', '个', '', '磨削辅料', '磨削工序辅料'),
        ('Mat006', '防锈油', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'DW-6206-006', '个', '', '防锈辅料', '终检防锈辅料'),
        ('Mat007', '清洗剂', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'DW-6206-007', '个', '', '清洗辅料', '终检清洗辅料'),
        ('Mat008', '6206内圈毛坯', CAT_RAW, MAKE_BUY, FEATURE_IMPORTANT, 'DW-6206-008', '个', '', '内圈毛坯', '轴承内圈毛坯备料'),
        ('Mat009', '6206内圈车削件', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'DW-6206-009', '个', '', '内圈车削件', '内圈车削半成品'),
        ('Mat010', '6206深沟球轴承内圈', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'DW-6206-010', '个', '', '内圈成品', '内圈机加工成品'),
        ('Mat011', '6206钢球组', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'DW-6206-011', '个', '', '钢球组件', '轴承总成用钢球组件'),
        ('Mat012', '6206保持架', CAT_PART, MAKE_BUY, FEATURE_IMPORTANT, 'DW-6206-012', '个', '', '保持架', '轴承总成用保持架'),
        ('Mat013', '6206防尘盖', CAT_PART, MAKE_BUY, FEATURE_NORMAL, 'DW-6206-013', '个', '', '防尘盖', '轴承密封防护件'),
        ('Mat014', '6206深沟球轴承总成', CAT_PART, MAKE_SELF, FEATURE_KEY, 'DW-6206-014', '个', '', '轴承总成', '用于产品族演示的总成物料'),
        ('Mat015', '包装盒', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'DW-6206-015', '个', '', '包装盒', '单件包装盒'),
        ('Mat016', '防锈袋', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'DW-6206-016', '个', '', '防锈袋', '单件防锈包装袋'),
        ('Mat017', '标签纸', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'DW-6206-017', '个', '', '标签纸', '成品标签辅料'),
        ('Mat018', '周转托盘', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'DW-6206-018', '个', '', '周转托盘', '过程周转托盘'),
        ('Mat019', '6207深沟球轴承外圈', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'DW-6207-001', '个', '', '同族产品', '用于产品族演示的相邻规格外圈'),
        ('Mat020', '终检样圈', CAT_PART, MAKE_SELF, FEATURE_NORMAL, 'DW-6206-020', '个', '', '检验样件', '终检留样与对比样件'),
    ]
    materials = [
        {
            'code': code,
            'name': name,
            'category': category,
            'make_type': make_type,
            'feature': feature,
            'drawing': drawing,
            'unit': unit,
            'model': model,
            'spec': spec,
            'remark': remark,
        }
        for code, name, category, make_type, feature, drawing, unit, model, spec, remark in material_specs
    ]

    mboms = [
        {
            'code': 'Mb001',
            'material_code': 'Mat004',
            'name': '6206外圈MBOM',
            'nodes': [
                {'level': 0, 'material_code': 'Mat004', 'qty': 1},
                {'level': 1, 'material_code': 'Mat001', 'qty': 1, 'parent_material': 'Mat004', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat005', 'qty': 1, 'parent_material': 'Mat004', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat006', 'qty': 1, 'parent_material': 'Mat004', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat007', 'qty': 1, 'parent_material': 'Mat004', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat015', 'qty': 1, 'parent_material': 'Mat004', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat016', 'qty': 1, 'parent_material': 'Mat004', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat017', 'qty': 1, 'parent_material': 'Mat004', 'parent_version': 'A.01'},
            ],
        },
    ]

    routes = [
        {
            'code': 'Rt001',
            'name': '6206轴承外圈机加工工艺',
            'route_spec': '机加',
            'biz': 'Biz007',
            'material_code': 'Mat004',
            'proc_spec': '机械加工专业',
            'remark': '标准版轴承机加工路线，保持简单工艺但扩展资源与产品主数据',
            'ops': [
                {'no': '0010', 'name': '来料检验与上料准备', 'type': '检验', 'wc': 'Wc001', 'prep': 8, 'run': 10, 'out': 'Mat001', 'content': '完成毛坯和辅料来料确认后齐套上线', 'materials': [('Mat001', 1)], 'steps': [('核对来料批次', '核对轴承钢环件毛坯批次和外观状态'), ('执行上线准备', '完成条码确认和上线齐套准备')]},
                {'no': '0020', 'name': '端面外圆与沟道车削', 'type': '加工', 'wc': 'Wc002', 'prep': 10, 'run': 18, 'out': 'Mat002', 'content': '完成端面、外圆和滚道基准车削', 'materials': [('Mat001', 1)], 'steps': [('装夹车削', '完成端面和外圆车削'), ('沟道精车', '完成外圈滚道精车并复核尺寸')]},
                {'no': '0030', 'name': '淬火回火处理', 'type': '加工', 'wc': 'Wc004', 'prep': 10, 'run': 120, 'out': 'Mat003', 'content': '完成淬火回火并控制硬度范围', 'materials': [('Mat002', 1)], 'steps': [('装炉淬火', '按热处理曲线装炉淬火'), ('回火抽检', '完成回火和硬度抽检记录')]},
                {'no': '0040', 'name': '沟道与外圆磨削', 'type': '加工', 'wc': 'Wc006', 'prep': 8, 'run': 18, 'out': 'Mat004', 'content': '完成沟道、外圆精磨与圆度控制', 'materials': [('Mat003', 1), ('Mat005', 1)], 'steps': [('沟道精磨', '完成外圈沟道精磨'), ('外圆精磨', '完成外圆精磨并控制圆度')]},
                {'no': '0050', 'name': '清洗防锈终检入库', 'type': '检验', 'wc': 'Wc009', 'prep': 8, 'run': 12, 'out': 'Mat004', 'content': '完成清洗、防锈、终检、包装和入库', 'materials': [('Mat006', 1), ('Mat007', 1), ('Mat015', 1), ('Mat016', 1), ('Mat017', 1)], 'steps': [('清洗防锈', '完成清洗烘干和防锈处理'), ('终检包装', '完成尺寸终检、贴标和包装入库')]},
            ],
        },
    ]

    wc_user_links = [
        ('Wc001', 'U009'), ('Wc001', 'U010'), ('Wc001', 'U014'),
        ('Wc002', 'U011'), ('Wc002', 'U012'), ('Wc002', 'U013'),
        ('Wc003', 'U011'), ('Wc003', 'U012'),
        ('Wc004', 'U015'), ('Wc004', 'U016'), ('Wc004', 'U017'),
        ('Wc005', 'U015'), ('Wc005', 'U016'),
        ('Wc006', 'U018'), ('Wc006', 'U019'), ('Wc006', 'U020'),
        ('Wc007', 'U018'), ('Wc007', 'U019'),
        ('Wc008', 'U021'), ('Wc008', 'U022'),
        ('Wc009', 'U005'), ('Wc009', 'U006'), ('Wc009', 'U021'),
        ('Wc010', 'U009'), ('Wc010', 'U010'), ('Wc010', 'U022'),
    ]

    wc_eq_links = [
        ('Wc001', 'Eq006'),
        ('Wc002', 'Eq001'), ('Wc002', 'Eq002'), ('Wc002', 'Eq005'),
        ('Wc003', 'Eq003'), ('Wc003', 'Eq004'),
        ('Wc004', 'Eq007'), ('Wc004', 'Eq008'),
        ('Wc005', 'Eq009'), ('Wc005', 'Eq010'),
        ('Wc006', 'Eq011'), ('Wc006', 'Eq012'),
        ('Wc007', 'Eq013'), ('Wc007', 'Eq014'), ('Wc007', 'Eq015'), ('Wc007', 'Eq016'),
        ('Wc008', 'Eq017'),
        ('Wc009', 'Eq019'), ('Wc009', 'Eq020'),
        ('Wc010', 'Eq018'),
    ]

    eq_user_links = [
        ('Eq001', 'U012'), ('Eq002', 'U013'), ('Eq003', 'U012'), ('Eq004', 'U013'), ('Eq005', 'U011'), ('Eq006', 'U014'),
        ('Eq007', 'U016'), ('Eq008', 'U017'), ('Eq009', 'U016'), ('Eq010', 'U015'),
        ('Eq011', 'U019'), ('Eq012', 'U020'), ('Eq013', 'U019'), ('Eq014', 'U020'), ('Eq015', 'U018'), ('Eq016', 'U018'),
        ('Eq017', 'U021'), ('Eq018', 'U022'), ('Eq019', 'U021'), ('Eq020', 'U006'),
    ]

    return {
        'metadata': {
            'name': '轴承单工厂机加工MOM种子',
            'industry': '轴承制造',
            'product_family': '滚动轴承',
            'product_model': '6206深沟球轴承外圈',
            'description': '面向单工厂标准版轴承机加工场景构建的主数据，保持简单工艺路线，同时补齐更专业的产品与工厂资源数据。',
        },
        'admins': admins,
        'bizs': bizs,
        'users': users,
        'suppliers': suppliers,
        'work_centers': work_centers,
        'equipments': equipments,
        'tools': tools,
        'wc_user_links': wc_user_links,
        'wc_eq_links': wc_eq_links,
        'eq_user_links': eq_user_links,
        'wc_sup_links': [],
        'warehouses': warehouses,
        'locations': locations,
        'materials': materials,
        'mboms': mboms,
        'routes': routes,
    }


CONFIG = build_config()


def build_variant(namespace: str = NAMESPACE, volume_profile: str = VOLUME_PROFILE) -> dict:
    metadata = deepcopy(CONFIG['metadata'])
    metadata['default_version'] = 'A.01'
    metadata['default_security'] = '内部'
    metadata['volume_profile'] = volume_profile

    builder = SeedBuilder(metadata)
    builder.build_from_config(CONFIG)
    seed = builder.seed

    apply_namespace(seed, namespace)
    normalize_user_codes(seed, namespace)
    normalize_poc_security(seed)
    normalize_storage_factory_org(seed)
    normalize_release_user(seed)
    clear_tool_strategy_relations(seed)
    filter_wc_supplier_relations(seed)
    normalize_sequence_relations(seed)
    apply_production_orders(seed, SCENARIO, namespace)
    return seed


def build() -> dict:
    return build_variant()


def summarize(seed: dict) -> dict:
    return summarize_seed(seed)


def main() -> None:
    seed = build()
    ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    ASSET_PATH.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding='utf-8-sig')
    print(json.dumps(summarize(seed), ensure_ascii=False, indent=2))
    print(f'已写入种子文件: {ASSET_PATH}')


if __name__ == '__main__':
    main()
