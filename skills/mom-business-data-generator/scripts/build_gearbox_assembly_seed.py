from __future__ import annotations

import json
import sys
from pathlib import Path

from gearbox_seed_support import (
    CAT_AUX,
    CAT_KIT,
    CAT_PART,
    FEATURE_IMPORTANT,
    FEATURE_KEY,
    FEATURE_NORMAL,
    MAKE_BUY,
    MAKE_SELF,
    NO,
    YES,
    build_seed,
    summarize_seed,
)

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

SCENARIO = 'gearbox_assembly'
NAMESPACE = 'GBA31S01'
VOLUME_PROFILE = '大体量版'
ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'gearbox_assembly_seed_big.json'
VARIANT_SPECS = (
    ('gearbox_assembly_seed.json', 'GBA20S01', '标准版'),
    ('gearbox_assembly_seed_big.json', 'GBA31S01', '大体量版'),
    ('gearbox_assembly_seed_ultra.json', 'GBA42S01', '超大体量版'),
)

CONFIG = {
    'metadata': {
        'name': '变速箱单工厂总装检测MOM种子',
        'industry': '汽车零部件',
        'product_family': '双离合变速箱',
        'product_model': 'DCT380湿式双离合变速箱总成',
        'description': '面向单工厂总装检测场景构建的变速箱生产主数据，覆盖外购模块齐套、总装、灌油、冷试、换挡性能试验、终检打码和包装入库。',
    },
    'admins': [
        ('0', '公司', 'ADM-GBA-HQ', '星联传动科技有限公司', '星联传动'),
        ('ADM-GBA-HQ', '部门', 'ADM-GBA-TECH', '工艺技术部', '工艺技术'),
        ('ADM-GBA-HQ', '部门', 'ADM-GBA-PMC', '生产运营部', '生产运营'),
        ('ADM-GBA-HQ', '部门', 'ADM-GBA-QA', '质量管理部', '质量管理'),
        ('ADM-GBA-HQ', '部门', 'ADM-GBA-WM', '仓储物流部', '仓储物流'),
        ('ADM-GBA-HQ', '部门', 'ADM-GBA-EM', '设备工装部', '设备工装'),
        ('ADM-GBA-HQ', '部门', 'ADM-GBA-IT', '信息化部', '信息化'),
        ('ADM-GBA-HQ', '工厂', 'ADM-GBA-PLANT', '变速箱总装检测工厂', '总装工厂', '负责变速箱总装、测试与包装入库'),
    ],
    'bizs': [
        ('0', 'BIZ-GBA-COMPANY', '星联传动科技有限公司', '星联传动', '公司', 'ADM-GBA-HQ', '', '单工厂变速箱总装检测方案'),
        ('BIZ-GBA-COMPANY', 'BIZ-GBA-TECH', '工艺技术部', '工艺技术', '部门', 'ADM-GBA-TECH'),
        ('BIZ-GBA-COMPANY', 'BIZ-GBA-PMC', '生产运营部', '生产运营', '部门', 'ADM-GBA-PMC'),
        ('BIZ-GBA-COMPANY', 'BIZ-GBA-QA', '质量管理部', '质量管理', '部门', 'ADM-GBA-QA'),
        ('BIZ-GBA-COMPANY', 'BIZ-GBA-WM', '仓储物流部', '仓储物流', '部门', 'ADM-GBA-WM'),
        ('BIZ-GBA-COMPANY', 'BIZ-GBA-EM', '设备工装部', '设备工装', '部门', 'ADM-GBA-EM'),
        ('BIZ-GBA-COMPANY', 'BIZ-GBA-IT', '信息化部', '信息化', '部门', 'ADM-GBA-IT'),
        ('BIZ-GBA-COMPANY', 'BIZ-GBA-PLANT', '变速箱总装检测工厂', '总装工厂', '工厂', 'ADM-GBA-PLANT', '装配专业', '聚焦模块齐套、总装、性能试验与放行'),
        ('BIZ-GBA-PLANT', 'BIZ-GBA-ASM-WS', '总装车间', '总装车间', '车间', 'ADM-GBA-PLANT'),
        ('BIZ-GBA-PLANT', 'BIZ-GBA-TEST-WS', '检测试验车间', '检测试验', '车间', 'ADM-GBA-PLANT'),
        ('BIZ-GBA-ASM-WS', 'BIZ-GBA-PREASM-SEC', '预装工段', '预装工段', '工段', 'ADM-GBA-PLANT'),
        ('BIZ-GBA-ASM-WS', 'BIZ-GBA-MAINASM-SEC', '主装工段', '主装工段', '工段', 'ADM-GBA-PLANT'),
        ('BIZ-GBA-ASM-WS', 'BIZ-GBA-FLUID-SEC', '灌油转运工段', '灌油转运', '工段', 'ADM-GBA-PLANT'),
        ('BIZ-GBA-TEST-WS', 'BIZ-GBA-COLDTEST-SEC', '冷试工段', '冷试工段', '工段', 'ADM-GBA-PLANT'),
        ('BIZ-GBA-TEST-WS', 'BIZ-GBA-FINALCHK-SEC', '终检工段', '终检工段', '工段', 'ADM-GBA-PLANT'),
        ('BIZ-GBA-TEST-WS', 'BIZ-GBA-PACK-SEC', '包装工段', '包装工段', '工段', 'ADM-GBA-PLANT'),
        ('BIZ-GBA-PREASM-SEC', 'BIZ-GBA-PREASM-A', '预装甲班', '预装甲班', '班组', 'ADM-GBA-PLANT'),
        ('BIZ-GBA-MAINASM-SEC', 'BIZ-GBA-MAINASM-A', '主装甲班', '主装甲班', '班组', 'ADM-GBA-PLANT'),
        ('BIZ-GBA-FLUID-SEC', 'BIZ-GBA-FLUID-A', '灌油转运甲班', '灌油甲班', '班组', 'ADM-GBA-PLANT'),
        ('BIZ-GBA-COLDTEST-SEC', 'BIZ-GBA-COLDTEST-A', '冷试甲班', '冷试甲班', '班组', 'ADM-GBA-PLANT'),
        ('BIZ-GBA-FINALCHK-SEC', 'BIZ-GBA-FINALCHK-A', '终检甲班', '终检甲班', '班组', 'ADM-GBA-PLANT'),
        ('BIZ-GBA-PACK-SEC', 'BIZ-GBA-PACK-A', '包装甲班', '包装甲班', '班组', 'ADM-GBA-PLANT'),
    ],
    'users': [
        ('U-GBA-001', '顾承宇', '重要', '男', 'ADM-GBA-TECH', 'BIZ-GBA-TECH', '工艺平台主管'),
        ('U-GBA-002', '林若汐', '重要', '女', 'ADM-GBA-TECH', 'BIZ-GBA-TECH', '变速箱装配工艺工程师'),
        ('U-GBA-003', '何景川', '重要', '男', 'ADM-GBA-TECH', 'BIZ-GBA-TECH', '试验工艺工程师'),
        ('U-GBA-004', '梁知夏', '重要', '女', 'ADM-GBA-PMC', 'BIZ-GBA-PMC', '主计划员'),
        ('U-GBA-005', '郑宇恒', '一般', '男', 'ADM-GBA-PMC', 'BIZ-GBA-PMC', '物流计划员'),
        ('U-GBA-006', '宋清妍', '重要', '女', 'ADM-GBA-QA', 'BIZ-GBA-QA', '过程质量工程师'),
        ('U-GBA-007', '陆景明', '重要', '男', 'ADM-GBA-QA', 'BIZ-GBA-QA', '终检工程师'),
        ('U-GBA-008', '周可欣', '一般', '女', 'ADM-GBA-WM', 'BIZ-GBA-WM', '仓库管理员'),
        ('U-GBA-009', '韩书恒', '一般', '男', 'ADM-GBA-EM', 'BIZ-GBA-EM', '设备工程师'),
        ('U-GBA-010', '杨思源', '一般', '男', 'ADM-GBA-EM', 'BIZ-GBA-EM', '工装管理员'),
        ('U-GBA-011', '谢语桐', '一般', '女', 'ADM-GBA-PLANT', 'BIZ-GBA-PREASM-A', '预装班组长'),
        ('U-GBA-012', '邓启航', '一般', '男', 'ADM-GBA-PLANT', 'BIZ-GBA-PREASM-A', '装配操作工'),
        ('U-GBA-013', '董安宁', '一般', '女', 'ADM-GBA-PLANT', 'BIZ-GBA-MAINASM-A', '主装班组长'),
        ('U-GBA-014', '许博远', '一般', '男', 'ADM-GBA-PLANT', 'BIZ-GBA-MAINASM-A', '装配操作工'),
        ('U-GBA-015', '曹清雅', '一般', '女', 'ADM-GBA-PLANT', 'BIZ-GBA-FLUID-A', '灌油转运操作工'),
        ('U-GBA-016', '唐承泽', '一般', '男', 'ADM-GBA-PLANT', 'BIZ-GBA-COLDTEST-A', '冷试操作工'),
        ('U-GBA-017', '冯嘉宁', '一般', '女', 'ADM-GBA-PLANT', 'BIZ-GBA-FINALCHK-A', '终检检验员'),
        ('U-GBA-018', '于景程', '一般', '男', 'ADM-GBA-PLANT', 'BIZ-GBA-PACK-A', '包装操作工'),
    ],
    'suppliers': [
        {'code': 'SUP-GBA-HSG', 'name': '苏州精铸壳体有限公司', 'short': '精铸壳体', 'remark': '供应变速箱前后箱体模块'},
        {'code': 'SUP-GBA-GEAR', 'name': '常州齿轮精密科技有限公司', 'short': '常州齿轮', 'remark': '供应齿轮副与同步器组件'},
        {'code': 'SUP-GBA-SHAFT', 'name': '无锡轴系制造有限公司', 'short': '无锡轴系', 'remark': '供应输入轴和中间轴组件'},
        {'code': 'SUP-GBA-DIFF', 'name': '宁波差速器系统有限公司', 'short': '宁波差速器', 'remark': '供应差速器总成'},
        {'code': 'SUP-GBA-CLUTCH', 'name': '芜湖离合机电有限公司', 'short': '离合机电', 'remark': '供应离合及机电控制模块'},
        {'code': 'SUP-GBA-BRG', 'name': '洛阳精密轴承股份有限公司', 'short': '洛阳轴承', 'remark': '供应轴承配套包'},
        {'code': 'SUP-GBA-SEAL', 'name': '青岛密封科技有限公司', 'short': '青岛密封', 'remark': '供应密封件、油封与胶料'},
    ],
    'work_centers': [
        {'code': 'WC-GBA-PREASM', 'name': '组件预装线', 'biz': 'BIZ-GBA-PREASM-SEC', 'wc_type': '产线', 'wc_class': '加工', 'remark': '负责输入轴、轴承和差速器模块预装'},
        {'code': 'WC-GBA-MAINASM', 'name': '主箱合装线', 'biz': 'BIZ-GBA-MAINASM-SEC', 'wc_type': '产线', 'wc_class': '加工', 'remark': '负责齿轮系、箱体和机电控制单元合装'},
        {'code': 'WC-GBA-TORQUE', 'name': '智能拧紧工位', 'biz': 'BIZ-GBA-MAINASM-SEC', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBA-FLUID', 'name': '灌油工位', 'biz': 'BIZ-GBA-FLUID-SEC', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBA-TRANSFER', 'name': '总装转运中心', 'biz': 'BIZ-GBA-FLUID-SEC', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBA-COLDTEST', 'name': '冷试工位', 'biz': 'BIZ-GBA-COLDTEST-SEC', 'wc_type': '组织', 'wc_class': '检验'},
        {'code': 'WC-GBA-SHIFTTEST', 'name': '换挡性能试验台', 'biz': 'BIZ-GBA-COLDTEST-SEC', 'wc_type': '组织', 'wc_class': '检验'},
        {'code': 'WC-GBA-LEAK', 'name': '密封检测工位', 'biz': 'BIZ-GBA-FINALCHK-SEC', 'wc_type': '组织', 'wc_class': '检验'},
        {'code': 'WC-GBA-ENDCHK', 'name': '终检工位', 'biz': 'BIZ-GBA-FINALCHK-SEC', 'wc_type': '组织', 'wc_class': '检验'},
        {'code': 'WC-GBA-LASER', 'name': '激光打码工位', 'biz': 'BIZ-GBA-FINALCHK-SEC', 'wc_type': '组织', 'wc_class': '检验'},
        {'code': 'WC-GBA-PACK', 'name': '包装入库工位', 'biz': 'BIZ-GBA-PACK-SEC', 'wc_type': '组织', 'wc_class': '加工'},
    ],
    'equipments': [
        {'code': 'EQ-GBA-PRESS-01', 'name': '轴承压装机', 'model': 'PR-220', 'biz': 'BIZ-GBA-PREASM-SEC', 'bottle': NO},
        {'code': 'EQ-GBA-LIFT-01', 'name': '差速器翻转吊具', 'model': 'LT-600', 'biz': 'BIZ-GBA-PREASM-SEC', 'bottle': NO},
        {'code': 'EQ-GBA-CONVEY-01', 'name': '主箱合装输送线', 'model': 'CV-18M', 'biz': 'BIZ-GBA-MAINASM-SEC', 'bottle': YES},
        {'code': 'EQ-GBA-TORQUE-01', 'name': '多轴智能拧紧系统', 'model': 'TQ-180', 'biz': 'BIZ-GBA-MAINASM-SEC', 'bottle': YES},
        {'code': 'EQ-GBA-GLUE-01', 'name': '定量涂胶机', 'model': 'GL-08', 'biz': 'BIZ-GBA-MAINASM-SEC', 'bottle': NO},
        {'code': 'EQ-GBA-FILL-01', 'name': '定量灌油机', 'model': 'OF-20', 'biz': 'BIZ-GBA-FLUID-SEC', 'bottle': NO},
        {'code': 'EQ-GBA-COLD-01', 'name': '变速箱冷试台', 'model': 'CT-380', 'biz': 'BIZ-GBA-COLDTEST-SEC', 'bottle': YES},
        {'code': 'EQ-GBA-SHIFT-01', 'name': '换挡性能试验台', 'model': 'ST-380', 'biz': 'BIZ-GBA-COLDTEST-SEC', 'bottle': YES},
        {'code': 'EQ-GBA-LEAK-01', 'name': '气密泄漏检测仪', 'model': 'LK-06', 'biz': 'BIZ-GBA-FINALCHK-SEC', 'bottle': NO},
        {'code': 'EQ-GBA-CODE-01', 'name': '激光打码机', 'model': 'LM-30', 'biz': 'BIZ-GBA-FINALCHK-SEC', 'bottle': NO},
        {'code': 'EQ-GBA-PACK-01', 'name': '包装封箱工作站', 'model': 'PK-12', 'biz': 'BIZ-GBA-PACK-SEC', 'bottle': NO},
    ],
    'tools': [
        {'code': 'TOOL-GBA-HSG-01', 'name': '箱体定位工装', 'material_category': CAT_KIT, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_KEY, 'model': 'JG-HSG-01', 'spec': '箱体定位', 'remark': '控制箱体合装定位基准', 'life_times': 120000, 'life_days': 365},
        {'code': 'TOOL-GBA-SHAFT-01', 'name': '输入轴压装工装', 'material_category': CAT_KIT, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_IMPORTANT, 'model': 'JG-SFT-01', 'spec': '轴系压装', 'remark': '保障输入轴和轴承压装深度', 'life_times': 80000, 'life_days': 365},
        {'code': 'TOOL-GBA-TORQUE-01', 'name': '数显扭矩扳手', 'material_category': CAT_PART, 'make_type': MAKE_BUY, 'tooling_category': '通用工具', 'feature': FEATURE_KEY, 'model': 'TW-150', 'spec': '20-150Nm', 'remark': '采集关键螺栓扭矩', 'life_times': 50000, 'life_days': 180},
        {'code': 'TOOL-GBA-LEAK-01', 'name': '密封检测检具', 'material_category': CAT_PART, 'make_type': MAKE_BUY, 'tooling_category': '专用工装', 'feature': FEATURE_IMPORTANT, 'model': 'JG-LK-01', 'spec': '密封接口检具', 'remark': '用于气密检测密封接口转换', 'life_times': 40000, 'life_days': 180},
        {'code': 'TOOL-GBA-TRAY-01', 'name': '总成转运托盘', 'material_category': CAT_KIT, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_NORMAL, 'model': 'TR-GBA-01', 'spec': '总成转运', 'remark': '用于总装到终检的周转防护', 'life_times': 100000, 'life_days': 365},
    ],
    'wc_user_links': [
        ('WC-GBA-PREASM', 'U-GBA-002'), ('WC-GBA-PREASM', 'U-GBA-011'), ('WC-GBA-PREASM', 'U-GBA-012'),
        ('WC-GBA-MAINASM', 'U-GBA-002'), ('WC-GBA-MAINASM', 'U-GBA-013'), ('WC-GBA-MAINASM', 'U-GBA-014'),
        ('WC-GBA-FLUID', 'U-GBA-015'), ('WC-GBA-COLDTEST', 'U-GBA-003'), ('WC-GBA-COLDTEST', 'U-GBA-016'),
        ('WC-GBA-SHIFTTEST', 'U-GBA-003'), ('WC-GBA-LEAK', 'U-GBA-006'), ('WC-GBA-ENDCHK', 'U-GBA-007'),
        ('WC-GBA-LASER', 'U-GBA-017'), ('WC-GBA-PACK', 'U-GBA-018'),
    ],
    'wc_eq_links': [
        ('WC-GBA-PREASM', 'EQ-GBA-PRESS-01'), ('WC-GBA-PREASM', 'EQ-GBA-LIFT-01'),
        ('WC-GBA-MAINASM', 'EQ-GBA-CONVEY-01'), ('WC-GBA-TORQUE', 'EQ-GBA-TORQUE-01'), ('WC-GBA-MAINASM', 'EQ-GBA-GLUE-01'),
        ('WC-GBA-FLUID', 'EQ-GBA-FILL-01'), ('WC-GBA-COLDTEST', 'EQ-GBA-COLD-01'), ('WC-GBA-SHIFTTEST', 'EQ-GBA-SHIFT-01'),
        ('WC-GBA-LEAK', 'EQ-GBA-LEAK-01'), ('WC-GBA-LASER', 'EQ-GBA-CODE-01'), ('WC-GBA-PACK', 'EQ-GBA-PACK-01'),
    ],
    'eq_user_links': [
        ('EQ-GBA-TORQUE-01', 'U-GBA-014'), ('EQ-GBA-COLD-01', 'U-GBA-016'), ('EQ-GBA-LEAK-01', 'U-GBA-017'),
    ],
    'warehouses': [
        ('WH-GBA-KIT', '外购配套件库', 'BIZ-GBA-WM', 'ERP一级库', '普通库房', '存放箱体、齿轮模块、差速器和机电控制件'),
        ('WH-GBA-AUX', '油液辅料库', 'BIZ-GBA-WM', 'ERP一级库', '普通库房', '存放齿轮油、胶料和包装辅料'),
        ('WH-GBA-WIP', '在制品暂存库', 'BIZ-GBA-WM', '车间二级库', '普通库房', '存放待试与待检总成'),
        ('WH-GBA-FG', '成品库', 'BIZ-GBA-WM', 'ERP二级库', '普通库房', '存放放行后的变速箱总成'),
    ],
    'locations': [
        ('LOC-GBA-KIT-01', '箱体模块区', 'BIZ-GBA-WM', 'WH-GBA-KIT'), ('LOC-GBA-KIT-02', '齿轮差速器区', 'BIZ-GBA-WM', 'WH-GBA-KIT'),
        ('LOC-GBA-AUX-01', '油液区', 'BIZ-GBA-WM', 'WH-GBA-AUX'), ('LOC-GBA-AUX-02', '胶料包装区', 'BIZ-GBA-WM', 'WH-GBA-AUX'),
        ('LOC-GBA-WIP-01', '待试区', 'BIZ-GBA-WM', 'WH-GBA-WIP'), ('LOC-GBA-WIP-02', '待检区', 'BIZ-GBA-WM', 'WH-GBA-WIP'),
        ('LOC-GBA-FG-01', '成品待发区', 'BIZ-GBA-WM', 'WH-GBA-FG'),
    ],
    'materials': [
        {'code': 'MAT-GBA-GEARBOX-FIN', 'name': 'DCT380变速箱总成', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': 'DCT380-ASM-001', 'remark': '最终交付的变速箱总成', 'serial': YES},
        {'code': 'MAT-GBA-HOUSING-KIT', 'name': '箱体总成', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_KEY, 'drawing': 'DCT380-HSG-101', 'remark': '前后箱体与阀体安装基座'},
        {'code': 'MAT-GBA-GEARTRAIN-MOD', 'name': '齿轮传动模块', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_KEY, 'drawing': 'DCT380-GEAR-201', 'remark': '齿轮副、同步器和中间轴模块'},
        {'code': 'MAT-GBA-INPUT-SHAFT', 'name': '输入轴组件', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'DCT380-SFT-301', 'remark': '输入轴与花键连接组件'},
        {'code': 'MAT-GBA-DIFF-ASM', 'name': '差速器总成', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_KEY, 'drawing': 'DCT380-DIFF-401', 'remark': '差速器与壳体配套总成'},
        {'code': 'MAT-GBA-CLUTCH-MECH', 'name': '离合机电控制组件', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_KEY, 'drawing': 'DCT380-MECH-501', 'remark': '双离合和机电控制集成组件'},
        {'code': 'MAT-GBA-BRG-KIT', 'name': '轴承配套包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'DCT380-BRG-601'},
        {'code': 'MAT-GBA-SEAL-KIT', 'name': '密封件包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'DCT380-SEAL-701'},
        {'code': 'MAT-GBA-FIX-KIT', 'name': '紧固件包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'DCT380-FIX-801'},
        {'code': 'MAT-GBA-ATF-OIL', 'name': '变速箱润滑油', 'category': CAT_AUX, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'DCT380-OIL-901', 'unit': '个'},
        {'code': 'MAT-GBA-PKG-KIT', 'name': '包装防护包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'DCT380-PKG-902'},
    ],
    'mboms': [
        {
            'code': 'MBOM-GBA-ASM-A01',
            'material_code': 'MAT-GBA-GEARBOX-FIN',
            'name': 'DCT380变速箱总成MBOM',
            'nodes': [
                {'level': 0, 'material_code': 'MAT-GBA-GEARBOX-FIN', 'qty': 1},
                {'level': 1, 'material_code': 'MAT-GBA-HOUSING-KIT', 'qty': 1, 'parent_material': 'MAT-GBA-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBA-GEARTRAIN-MOD', 'qty': 1, 'parent_material': 'MAT-GBA-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBA-DIFF-ASM', 'qty': 1, 'parent_material': 'MAT-GBA-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBA-CLUTCH-MECH', 'qty': 1, 'parent_material': 'MAT-GBA-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBA-BRG-KIT', 'qty': 1, 'parent_material': 'MAT-GBA-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBA-SEAL-KIT', 'qty': 1, 'parent_material': 'MAT-GBA-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBA-FIX-KIT', 'qty': 1, 'parent_material': 'MAT-GBA-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBA-ATF-OIL', 'qty': 4, 'parent_material': 'MAT-GBA-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBA-PKG-KIT', 'qty': 1, 'parent_material': 'MAT-GBA-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'MAT-GBA-INPUT-SHAFT', 'qty': 1, 'parent_material': 'MAT-GBA-GEARTRAIN-MOD', 'parent_version': 'A.01'},
            ],
        },
    ],
    'routes': [
        {
            'code': 'RT-GBA-ASM-A01',
            'name': '变速箱总装配工艺',
            'route_spec': '装配',
            'biz': 'BIZ-GBA-ASM-WS',
            'material_code': 'MAT-GBA-GEARBOX-FIN',
            'proc_spec': '装配专业',
            'remark': '完成模块上线、主箱合装、灌油和转入试验',
            'ops': [
                {'no': '0010', 'name': '来料核对与组件上线', 'type': '加工', 'wc': 'WC-GBA-PREASM', 'prep': 10, 'run': 18, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '核对箱体、齿轮模块、差速器和机电组件批次后上线', 'materials': [('MAT-GBA-HOUSING-KIT', 1), ('MAT-GBA-GEARTRAIN-MOD', 1), ('MAT-GBA-DIFF-ASM', 1), ('MAT-GBA-CLUTCH-MECH', 1)], 'steps': [('核对模块批次', '核对箱体、齿轮模块和差速器批次状态'), ('完成组件上线', '按工位节拍完成组件上线和防错扫描')]},
                {'no': '0020', 'name': '输入轴组件预装', 'type': '加工', 'wc': 'WC-GBA-PREASM', 'prep': 12, 'run': 22, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '完成输入轴、轴承和垫片预装', 'materials': [('MAT-GBA-INPUT-SHAFT', 1), ('MAT-GBA-BRG-KIT', 1), ('MAT-GBA-FIX-KIT', 1)], 'steps': [('压装输入轴组件', '执行输入轴和轴承压装'), ('复核预装尺寸', '复核端面间隙和压装深度')]},
                {'no': '0030', 'name': '差速器与齿轮系合装', 'type': '加工', 'wc': 'WC-GBA-MAINASM', 'prep': 12, 'run': 24, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '将差速器和齿轮模块装入主箱腔体', 'materials': [('MAT-GBA-DIFF-ASM', 1), ('MAT-GBA-GEARTRAIN-MOD', 1), ('MAT-GBA-FIX-KIT', 1)], 'steps': [('装入差速器', '完成差速器吊装和定位'), ('装入齿轮模块', '完成齿轮模块合装并检查自由转动')]},
                {'no': '0040', 'name': '箱体清洗与定量涂胶', 'type': '加工', 'wc': 'WC-GBA-MAINASM', 'prep': 8, 'run': 16, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '完成箱体结合面清洗、涂胶和密封准备', 'materials': [('MAT-GBA-HOUSING-KIT', 1), ('MAT-GBA-SEAL-KIT', 1)], 'steps': [('清洗结合面', '清洗箱体结合面和密封槽'), ('执行定量涂胶', '按工艺要求定量涂覆密封胶')]},
                {'no': '0050', 'name': '主箱合装与轴系间隙调整', 'type': '加工', 'wc': 'WC-GBA-TORQUE', 'prep': 14, 'run': 26, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '完成箱体合装、螺栓紧固和轴系间隙调整', 'materials': [('MAT-GBA-FIX-KIT', 1)], 'steps': [('执行箱体合装', '完成前后箱体对合与定位销装配'), ('紧固与调整间隙', '按扭矩程序紧固并调整关键间隙')]},
                {'no': '0060', 'name': '机电控制单元安装', 'type': '加工', 'wc': 'WC-GBA-TORQUE', 'prep': 10, 'run': 20, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '完成机电控制单元、传感器和线束连接', 'materials': [('MAT-GBA-CLUTCH-MECH', 1), ('MAT-GBA-FIX-KIT', 1)], 'steps': [('安装机电控制模块', '安装机电控制单元并连接接口'), ('复核传感器状态', '复核位置传感器和线束连接状态')]},
                {'no': '0070', 'name': '加注润滑油', 'type': '加工', 'wc': 'WC-GBA-FLUID', 'prep': 8, 'run': 14, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '按定量加注变速箱润滑油并核对液位', 'materials': [('MAT-GBA-ATF-OIL', 4)], 'steps': [('执行定量灌油', '按工艺要求加注润滑油'), ('复核油位状态', '复核液位和油液条码信息')]},
                {'no': '0080', 'name': '厂内转工至试验工位', 'type': '厂内转工', 'wc': 'WC-GBA-TRANSFER', 'prep': 6, 'run': 10, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '完成总装报工后转入冷试工位', 'materials': [], 'steps': [('绑定总成条码', '绑定总成唯一条码和追溯信息'), ('转运至冷试区', '转运至冷试工位缓存区')]},
            ],
        },
        {
            'code': 'RT-GBA-TEST-A01',
            'name': '变速箱试验放行工艺',
            'route_spec': '通用',
            'biz': 'BIZ-GBA-TEST-WS',
            'material_code': 'MAT-GBA-GEARBOX-FIN',
            'proc_spec': '装配专业',
            'remark': '完成冷试、换挡试验、密封检测、终检打码和包装入库',
            'ops': [
                {'no': '0010', 'name': '冷试磨合', 'type': '检验', 'wc': 'WC-GBA-COLDTEST', 'prep': 10, 'run': 18, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '完成空载冷试和拖动阻力分析', 'materials': [], 'steps': [('建立冷试程序', '装夹总成并加载冷试程序'), ('采集阻力曲线', '采集转速和阻力曲线并判定状态')]},
                {'no': '0020', 'name': '换挡性能试验', 'type': '检验', 'wc': 'WC-GBA-SHIFTTEST', 'prep': 12, 'run': 20, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '完成各挡位换挡响应与执行器动作测试', 'materials': [], 'steps': [('执行换挡动作', '测试各挡位切换响应和执行器动作'), ('记录关键参数', '记录换挡时间、压力和电流参数')]},
                {'no': '0030', 'name': '密封性检测', 'type': '检验', 'wc': 'WC-GBA-LEAK', 'prep': 8, 'run': 12, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '完成总成气密与接口密封检测', 'materials': [], 'steps': [('连接检测接口', '连接密封检测检具和接口'), ('判定泄漏结果', '执行保压检测并判定泄漏值')]},
                {'no': '0040', 'name': '终检与激光打码', 'type': '检验', 'wc': 'WC-GBA-ENDCHK', 'prep': 10, 'run': 16, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '完成外观终检、软件版本核对和激光打码', 'materials': [], 'steps': [('执行外观终检', '复核外观、接口和条码状态'), ('核对软件与版本', '核对控制单元版本并确认放行条件')]},
                {'no': '0050', 'name': '激光打码', 'type': '检验', 'wc': 'WC-GBA-LASER', 'prep': 6, 'run': 10, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '执行激光打码并绑定追溯信息', 'materials': [], 'steps': [('生成打码内容', '生成变速箱序列号和批次信息'), ('完成打码绑定', '完成激光打码和追溯绑定')]},
                {'no': '0060', 'name': '包装入库', 'type': '加工', 'wc': 'WC-GBA-PACK', 'prep': 8, 'run': 12, 'out': 'MAT-GBA-GEARBOX-FIN', 'content': '完成防护包装并转入成品库', 'materials': [('MAT-GBA-PKG-KIT', 1)], 'steps': [('安装防护包装', '安装防护件、干燥剂和包装标签'), ('转入成品库', '转入成品库并完成入库交接')]},
            ],
        },
    ],
}


def build_variant(namespace: str, volume_profile: str) -> dict:
    return build_seed(CONFIG, SCENARIO, namespace, volume_profile)


def build() -> dict:
    return build_variant(NAMESPACE, VOLUME_PROFILE)


def summarize(seed: dict) -> dict:
    return summarize_seed(seed)


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


