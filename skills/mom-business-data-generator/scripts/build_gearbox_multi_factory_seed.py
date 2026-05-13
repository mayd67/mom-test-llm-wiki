from __future__ import annotations

import json
import sys
from pathlib import Path

from gearbox_seed_support import (
    CAT_AUX,
    CAT_KIT,
    CAT_PART,
    CAT_RAW,
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

SCENARIO = 'gearbox_multi_factory'
NAMESPACE = 'GBX31S01'
VOLUME_PROFILE = '大体量版'
ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'gearbox_multi_factory_seed_big.json'
VARIANT_SPECS = (
    ('gearbox_multi_factory_seed.json', 'GBX20S01', '标准版'),
    ('gearbox_multi_factory_seed_big.json', 'GBX31S01', '大体量版'),
    ('gearbox_multi_factory_seed_ultra.json', 'GBX42S01', '超大体量版'),
)

CONFIG = {
    'metadata': {
        'name': '变速箱多工厂协同MOM种子',
        'industry': '汽车零部件',
        'product_family': '自动变速箱',
        'product_model': '8AT480自动变速箱总成',
        'description': '面向多工厂协同制造场景构建的变速箱生产主数据，覆盖箱体机加、齿轮轴系机加、热处理、总装和试验等协同制造过程。',
    },
    'admins': [
        ('0', '公司', 'ADM-GBX-HQ', '曜华动力总成有限公司', '曜华动力'),
        ('ADM-GBX-HQ', '部门', 'ADM-GBX-TECH', '工艺技术中心', '工艺技术'),
        ('ADM-GBX-HQ', '部门', 'ADM-GBX-PMC', '计划运营中心', '计划运营'),
        ('ADM-GBX-HQ', '部门', 'ADM-GBX-QA', '质量中心', '质量中心'),
        ('ADM-GBX-HQ', '部门', 'ADM-GBX-WM', '物流仓储中心', '物流仓储'),
        ('ADM-GBX-HQ', '工厂', 'ADM-GBX-HSG-PLANT', '箱体机加工厂', '箱体机加'),
        ('ADM-GBX-HQ', '工厂', 'ADM-GBX-GEAR-PLANT', '齿轮轴系机加工厂', '齿轴机加'),
        ('ADM-GBX-HQ', '工厂', 'ADM-GBX-HT-PLANT', '热处理精整工厂', '热处理厂'),
        ('ADM-GBX-HQ', '工厂', 'ADM-GBX-ASM-PLANT', '变速箱总装工厂', '总装工厂'),
        ('ADM-GBX-HQ', '工厂', 'ADM-GBX-TEST-PLANT', '试验包装工厂', '试验工厂'),
    ],
    'bizs': [
        ('0', 'BIZ-GBX-COMPANY', '曜华动力总成有限公司', '曜华动力', '公司', 'ADM-GBX-HQ', '', '多工厂变速箱协同制造方案'),
        ('BIZ-GBX-COMPANY', 'BIZ-GBX-TECH', '工艺技术中心', '工艺技术', '部门', 'ADM-GBX-TECH'),
        ('BIZ-GBX-COMPANY', 'BIZ-GBX-PMC', '计划运营中心', '计划运营', '部门', 'ADM-GBX-PMC'),
        ('BIZ-GBX-COMPANY', 'BIZ-GBX-QA', '质量中心', '质量中心', '部门', 'ADM-GBX-QA'),
        ('BIZ-GBX-COMPANY', 'BIZ-GBX-WM', '物流仓储中心', '物流仓储', '部门', 'ADM-GBX-WM'),
        ('BIZ-GBX-COMPANY', 'BIZ-GBX-HSG', '箱体机加工厂', '箱体机加', '工厂', 'ADM-GBX-HSG-PLANT', '机械加工专业', '负责箱体粗精加工与关键尺寸放行'),
        ('BIZ-GBX-COMPANY', 'BIZ-GBX-GEAR', '齿轮轴系机加工厂', '齿轴机加', '工厂', 'ADM-GBX-GEAR-PLANT', '机械加工专业', '负责齿轮和轴系毛坯加工与成形'),
        ('BIZ-GBX-COMPANY', 'BIZ-GBX-HT', '热处理精整工厂', '热处理厂', '工厂', 'ADM-GBX-HT-PLANT', '机械加工专业', '负责热处理、精整和热后终检'),
        ('BIZ-GBX-COMPANY', 'BIZ-GBX-ASM', '变速箱总装工厂', '总装工厂', '工厂', 'ADM-GBX-ASM-PLANT', '装配专业', '负责总装、灌油和条码绑定'),
        ('BIZ-GBX-COMPANY', 'BIZ-GBX-TEST', '试验包装工厂', '试验工厂', '工厂', 'ADM-GBX-TEST-PLANT', '装配专业', '负责冷试、EOL、包装入库'),
        ('BIZ-GBX-HSG', 'BIZ-GBX-HSG-SEC', '箱体机加工段', '箱体机加', '工段', 'ADM-GBX-HSG-PLANT'),
        ('BIZ-GBX-GEAR', 'BIZ-GBX-GEAR-SEC', '齿轮加工段', '齿轮加工', '工段', 'ADM-GBX-GEAR-PLANT'),
        ('BIZ-GBX-GEAR', 'BIZ-GBX-SHAFT-SEC', '轴系加工段', '轴系加工', '工段', 'ADM-GBX-GEAR-PLANT'),
        ('BIZ-GBX-HT', 'BIZ-GBX-HT-SEC', '热处理精整段', '热处理精整', '工段', 'ADM-GBX-HT-PLANT'),
        ('BIZ-GBX-ASM', 'BIZ-GBX-DIFF-SEC', '差速器预装段', '差速器预装', '工段', 'ADM-GBX-ASM-PLANT'),
        ('BIZ-GBX-ASM', 'BIZ-GBX-MAINASM-SEC', '总装工段', '总装工段', '工段', 'ADM-GBX-ASM-PLANT'),
        ('BIZ-GBX-TEST', 'BIZ-GBX-TEST-SEC', '试验工段', '试验工段', '工段', 'ADM-GBX-TEST-PLANT'),
        ('BIZ-GBX-TEST', 'BIZ-GBX-PACK-SEC', '包装工段', '包装工段', '工段', 'ADM-GBX-TEST-PLANT'),
        ('BIZ-GBX-HSG-SEC', 'BIZ-GBX-HSG-A', '箱体机加甲班', '箱体甲班', '班组', 'ADM-GBX-HSG-PLANT'),
        ('BIZ-GBX-GEAR-SEC', 'BIZ-GBX-GEAR-A', '齿轮加工甲班', '齿轮甲班', '班组', 'ADM-GBX-GEAR-PLANT'),
        ('BIZ-GBX-SHAFT-SEC', 'BIZ-GBX-SHAFT-A', '轴系加工甲班', '轴系甲班', '班组', 'ADM-GBX-GEAR-PLANT'),
        ('BIZ-GBX-HT-SEC', 'BIZ-GBX-HT-A', '热处理甲班', '热处理甲班', '班组', 'ADM-GBX-HT-PLANT'),
        ('BIZ-GBX-DIFF-SEC', 'BIZ-GBX-DIFF-A', '差速器预装甲班', '差速器甲班', '班组', 'ADM-GBX-ASM-PLANT'),
        ('BIZ-GBX-MAINASM-SEC', 'BIZ-GBX-MAINASM-A', '总装甲班', '总装甲班', '班组', 'ADM-GBX-ASM-PLANT'),
        ('BIZ-GBX-TEST-SEC', 'BIZ-GBX-TEST-A', '试验甲班', '试验甲班', '班组', 'ADM-GBX-TEST-PLANT'),
        ('BIZ-GBX-PACK-SEC', 'BIZ-GBX-PACK-A', '包装甲班', '包装甲班', '班组', 'ADM-GBX-TEST-PLANT'),
    ],
    'users': [
        ('U-GBX-001', '王景明', '重要', '男', 'ADM-GBX-TECH', 'BIZ-GBX-TECH', '工艺平台主管'),
        ('U-GBX-002', '李语桐', '重要', '女', 'ADM-GBX-TECH', 'BIZ-GBX-TECH', '箱体工艺工程师'),
        ('U-GBX-003', '张承宇', '重要', '男', 'ADM-GBX-TECH', 'BIZ-GBX-TECH', '齿轮轴系工艺工程师'),
        ('U-GBX-004', '刘安宁', '重要', '女', 'ADM-GBX-TECH', 'BIZ-GBX-TECH', '热处理工艺工程师'),
        ('U-GBX-005', '陈清妍', '重要', '女', 'ADM-GBX-TECH', 'BIZ-GBX-TECH', '总装试验工艺工程师'),
        ('U-GBX-006', '杨书恒', '重要', '男', 'ADM-GBX-PMC', 'BIZ-GBX-PMC', '主计划员'),
        ('U-GBX-007', '黄嘉宁', '一般', '女', 'ADM-GBX-QA', 'BIZ-GBX-QA', '质量工程师'),
        ('U-GBX-008', '赵可欣', '一般', '女', 'ADM-GBX-WM', 'BIZ-GBX-WM', '仓储物流计划员'),
        ('U-GBX-009', '周景程', '一般', '男', 'ADM-GBX-HSG-PLANT', 'BIZ-GBX-HSG-A', '箱体机加班组长'),
        ('U-GBX-010', '吴启航', '一般', '男', 'ADM-GBX-HSG-PLANT', 'BIZ-GBX-HSG-A', '机加操作工'),
        ('U-GBX-011', '徐清雅', '一般', '女', 'ADM-GBX-GEAR-PLANT', 'BIZ-GBX-GEAR-A', '齿轮加工班组长'),
        ('U-GBX-012', '孙书远', '一般', '男', 'ADM-GBX-GEAR-PLANT', 'BIZ-GBX-GEAR-A', '机加操作工'),
        ('U-GBX-013', '胡安然', '一般', '男', 'ADM-GBX-GEAR-PLANT', 'BIZ-GBX-SHAFT-A', '轴系加工班组长'),
        ('U-GBX-014', '朱晨悦', '一般', '女', 'ADM-GBX-GEAR-PLANT', 'BIZ-GBX-SHAFT-A', '磨削操作工'),
        ('U-GBX-015', '高景川', '一般', '男', 'ADM-GBX-HT-PLANT', 'BIZ-GBX-HT-A', '热处理班组长'),
        ('U-GBX-016', '林思源', '一般', '男', 'ADM-GBX-ASM-PLANT', 'BIZ-GBX-DIFF-A', '差速器预装工'),
        ('U-GBX-017', '何嘉豪', '一般', '男', 'ADM-GBX-ASM-PLANT', 'BIZ-GBX-MAINASM-A', '总装班组长'),
        ('U-GBX-018', '郭安琪', '一般', '女', 'ADM-GBX-ASM-PLANT', 'BIZ-GBX-MAINASM-A', '装配操作工'),
        ('U-GBX-019', '马书恒', '一般', '男', 'ADM-GBX-TEST-PLANT', 'BIZ-GBX-TEST-A', '试验工程师'),
        ('U-GBX-020', '罗梦洁', '一般', '女', 'ADM-GBX-TEST-PLANT', 'BIZ-GBX-PACK-A', '包装操作工'),
    ],
    'suppliers': [
        {'code': 'SUP-GBX-CAST', 'name': '常州壳体铸件有限公司', 'short': '常州壳体', 'remark': '供应箱体毛坯'},
        {'code': 'SUP-GBX-STEEL', 'name': '江阴合金钢有限公司', 'short': '江阴钢材', 'remark': '供应齿轮和轴系原材料'},
        {'code': 'SUP-GBX-CLUTCH', 'name': '芜湖离合系统有限公司', 'short': '芜湖离合', 'remark': '供应离合器和机电控制模块'},
        {'code': 'SUP-GBX-DIFF', 'name': '南京差速器科技有限公司', 'short': '南京差速器', 'remark': '供应差速器零组件'},
    ],
    'work_centers': [
        {'code': 'WC-GBX-HSG-MACH', 'name': '箱体机加线', 'biz': 'BIZ-GBX-HSG-SEC', 'wc_type': '产线', 'wc_class': '加工'},
        {'code': 'WC-GBX-HSG-TRANSFER', 'name': '箱体转运中心', 'biz': 'BIZ-GBX-HSG', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBX-GEAR-MACH', 'name': '齿轮机加线', 'biz': 'BIZ-GBX-GEAR-SEC', 'wc_type': '产线', 'wc_class': '加工'},
        {'code': 'WC-GBX-SHAFT-MACH', 'name': '轴系机加线', 'biz': 'BIZ-GBX-SHAFT-SEC', 'wc_type': '产线', 'wc_class': '加工'},
        {'code': 'WC-GBX-MACH-TRANSFER', 'name': '齿轴转运中心', 'biz': 'BIZ-GBX-GEAR', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBX-HT-LINE', 'name': '热处理线', 'biz': 'BIZ-GBX-HT-SEC', 'wc_type': '产线', 'wc_class': '加工'},
        {'code': 'WC-GBX-HT-FIN', 'name': '热后精整工位', 'biz': 'BIZ-GBX-HT-SEC', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBX-HT-CHECK', 'name': '热后终检工位', 'biz': 'BIZ-GBX-HT-SEC', 'wc_type': '组织', 'wc_class': '检验'},
        {'code': 'WC-GBX-HT-TRANSFER', 'name': '热处理转运中心', 'biz': 'BIZ-GBX-HT', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBX-DIFF', 'name': '差速器预装工位', 'biz': 'BIZ-GBX-DIFF-SEC', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBX-MAINASM', 'name': '总装线', 'biz': 'BIZ-GBX-MAINASM-SEC', 'wc_type': '产线', 'wc_class': '加工'},
        {'code': 'WC-GBX-FLUID', 'name': '灌油工位', 'biz': 'BIZ-GBX-MAINASM-SEC', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBX-ASM-TRANSFER', 'name': '总装转运中心', 'biz': 'BIZ-GBX-ASM', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBX-TEST-COLD', 'name': '冷试工位', 'biz': 'BIZ-GBX-TEST-SEC', 'wc_type': '组织', 'wc_class': '检验'},
        {'code': 'WC-GBX-TEST-EOL', 'name': 'EOL终检工位', 'biz': 'BIZ-GBX-TEST-SEC', 'wc_type': '组织', 'wc_class': '检验'},
        {'code': 'WC-GBX-PACK', 'name': '包装入库工位', 'biz': 'BIZ-GBX-PACK-SEC', 'wc_type': '组织', 'wc_class': '加工'},
    ],
    'equipments': [
        {'code': 'EQ-GBX-HSG-01', 'name': '卧式加工中心', 'model': 'HMC-900', 'biz': 'BIZ-GBX-HSG-SEC', 'bottle': YES},
        {'code': 'EQ-GBX-HSG-02', 'name': '三坐标测量机', 'model': 'CMM-1500', 'biz': 'BIZ-GBX-HSG-SEC', 'bottle': NO},
        {'code': 'EQ-GBX-GEAR-01', 'name': '滚齿机', 'model': 'GH-420', 'biz': 'BIZ-GBX-GEAR-SEC', 'bottle': YES},
        {'code': 'EQ-GBX-GEAR-02', 'name': '插齿机', 'model': 'GS-220', 'biz': 'BIZ-GBX-GEAR-SEC', 'bottle': NO},
        {'code': 'EQ-GBX-SHAFT-01', 'name': '外圆磨床', 'model': 'OG-720', 'biz': 'BIZ-GBX-SHAFT-SEC', 'bottle': YES},
        {'code': 'EQ-GBX-HT-01', 'name': '渗碳炉', 'model': 'HT-650', 'biz': 'BIZ-GBX-HT-SEC', 'bottle': YES},
        {'code': 'EQ-GBX-HT-02', 'name': '回火炉', 'model': 'TP-420', 'biz': 'BIZ-GBX-HT-SEC', 'bottle': NO},
        {'code': 'EQ-GBX-HT-03', 'name': '硬度检测仪', 'model': 'HD-03', 'biz': 'BIZ-GBX-HT-SEC', 'bottle': NO},
        {'code': 'EQ-GBX-DIFF-01', 'name': '差速器压装机', 'model': 'DP-180', 'biz': 'BIZ-GBX-DIFF-SEC', 'bottle': NO},
        {'code': 'EQ-GBX-ASM-01', 'name': '总装输送线', 'model': 'ASM-30M', 'biz': 'BIZ-GBX-MAINASM-SEC', 'bottle': YES},
        {'code': 'EQ-GBX-FILL-01', 'name': '定量灌油机', 'model': 'OF-20', 'biz': 'BIZ-GBX-MAINASM-SEC', 'bottle': NO},
        {'code': 'EQ-GBX-COLD-01', 'name': '变速箱冷试台', 'model': 'CT-480', 'biz': 'BIZ-GBX-TEST-SEC', 'bottle': YES},
        {'code': 'EQ-GBX-EOL-01', 'name': 'EOL综合检测台', 'model': 'EOL-480', 'biz': 'BIZ-GBX-TEST-SEC', 'bottle': YES},
        {'code': 'EQ-GBX-PACK-01', 'name': '封箱工作站', 'model': 'PK-10', 'biz': 'BIZ-GBX-PACK-SEC', 'bottle': NO},
    ],
    'tools': [
        {'code': 'TOOL-GBX-HSG-01', 'name': '箱体定位夹具', 'material_category': CAT_KIT, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_KEY, 'model': 'JG-HSG-31', 'spec': '箱体定位', 'remark': '箱体孔系加工定位基准', 'life_times': 110000, 'life_days': 365},
        {'code': 'TOOL-GBX-GEAR-01', 'name': '齿轮滚齿夹具', 'material_category': CAT_KIT, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_IMPORTANT, 'model': 'JG-GR-31', 'spec': '滚齿定位', 'remark': '齿轮滚齿定位工装', 'life_times': 90000, 'life_days': 365},
        {'code': 'TOOL-GBX-HT-01', 'name': '热处理料盘', 'material_category': CAT_KIT, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_IMPORTANT, 'model': 'TR-HT-31', 'spec': '热处理周转', 'remark': '热处理转运与炉内摆放料盘', 'life_times': 100000, 'life_days': 365},
        {'code': 'TOOL-GBX-ASM-01', 'name': '总装定位工装', 'material_category': CAT_KIT, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_KEY, 'model': 'JG-ASM-31', 'spec': '总装定位', 'remark': '总装线箱体和轴系定位工装', 'life_times': 80000, 'life_days': 365},
        {'code': 'TOOL-GBX-TQ-01', 'name': '数显扭矩枪', 'material_category': CAT_PART, 'make_type': MAKE_BUY, 'tooling_category': '通用工具', 'feature': FEATURE_KEY, 'model': 'TW-220', 'spec': '30-220Nm', 'remark': '采集总装紧固扭矩', 'life_times': 50000, 'life_days': 180},
    ],
    'wc_user_links': [
        ('WC-GBX-HSG-MACH', 'U-GBX-002'), ('WC-GBX-HSG-MACH', 'U-GBX-009'), ('WC-GBX-HSG-MACH', 'U-GBX-010'),
        ('WC-GBX-GEAR-MACH', 'U-GBX-003'), ('WC-GBX-GEAR-MACH', 'U-GBX-011'), ('WC-GBX-GEAR-MACH', 'U-GBX-012'),
        ('WC-GBX-SHAFT-MACH', 'U-GBX-013'), ('WC-GBX-SHAFT-MACH', 'U-GBX-014'), ('WC-GBX-HT-LINE', 'U-GBX-004'), ('WC-GBX-HT-LINE', 'U-GBX-015'),
        ('WC-GBX-DIFF', 'U-GBX-016'), ('WC-GBX-MAINASM', 'U-GBX-005'), ('WC-GBX-MAINASM', 'U-GBX-017'), ('WC-GBX-MAINASM', 'U-GBX-018'),
        ('WC-GBX-TEST-COLD', 'U-GBX-019'), ('WC-GBX-TEST-EOL', 'U-GBX-007'), ('WC-GBX-PACK', 'U-GBX-020'),
    ],
    'wc_eq_links': [
        ('WC-GBX-HSG-MACH', 'EQ-GBX-HSG-01'), ('WC-GBX-HSG-TRANSFER', 'EQ-GBX-HSG-02'),
        ('WC-GBX-GEAR-MACH', 'EQ-GBX-GEAR-01'), ('WC-GBX-GEAR-MACH', 'EQ-GBX-GEAR-02'), ('WC-GBX-SHAFT-MACH', 'EQ-GBX-SHAFT-01'),
        ('WC-GBX-HT-LINE', 'EQ-GBX-HT-01'), ('WC-GBX-HT-LINE', 'EQ-GBX-HT-02'), ('WC-GBX-HT-CHECK', 'EQ-GBX-HT-03'),
        ('WC-GBX-DIFF', 'EQ-GBX-DIFF-01'), ('WC-GBX-MAINASM', 'EQ-GBX-ASM-01'), ('WC-GBX-FLUID', 'EQ-GBX-FILL-01'),
        ('WC-GBX-TEST-COLD', 'EQ-GBX-COLD-01'), ('WC-GBX-TEST-EOL', 'EQ-GBX-EOL-01'), ('WC-GBX-PACK', 'EQ-GBX-PACK-01'),
    ],
    'warehouses': [
        ('WH-GBX-RAW', '原材料库', 'BIZ-GBX-WM', 'ERP一级库', '普通库房', '存放铸件毛坯、钢材和外购模块'),
        ('WH-GBX-WIP', '跨厂在制品库', 'BIZ-GBX-WM', '车间二级库', '普通库房', '存放厂际转工件和待装件'),
        ('WH-GBX-FG', '成品库', 'BIZ-GBX-WM', 'ERP二级库', '普通库房', '存放试验放行后的成品总成'),
    ],
    'locations': [
        ('LOC-GBX-RAW-01', '毛坯钢材区', 'BIZ-GBX-WM', 'WH-GBX-RAW'), ('LOC-GBX-RAW-02', '外购模块区', 'BIZ-GBX-WM', 'WH-GBX-RAW'),
        ('LOC-GBX-WIP-01', '箱体转工区', 'BIZ-GBX-WM', 'WH-GBX-WIP'), ('LOC-GBX-WIP-02', '热后件区', 'BIZ-GBX-WM', 'WH-GBX-WIP'), ('LOC-GBX-WIP-03', '总装待试区', 'BIZ-GBX-WM', 'WH-GBX-WIP'),
        ('LOC-GBX-FG-01', '成品待发区', 'BIZ-GBX-WM', 'WH-GBX-FG'),
    ],
    'materials': [
        {'code': 'MAT-GBX-HSG-RAW', 'name': '箱体毛坯', 'category': CAT_RAW, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': '8AT480-HSG-001'},
        {'code': 'MAT-GBX-HSG-FIN', 'name': '箱体精加工件', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': '8AT480-HSG-101'},
        {'code': 'MAT-GBX-GEAR-BLK', 'name': '齿轮坯件', 'category': CAT_RAW, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': '8AT480-GR-001'},
        {'code': 'MAT-GBX-GEAR-MACH', 'name': '齿轮机加工件', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_IMPORTANT, 'drawing': '8AT480-GR-101'},
        {'code': 'MAT-GBX-GEAR-FIN', 'name': '热后精整齿轮件', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': '8AT480-GR-201'},
        {'code': 'MAT-GBX-SHAFT-BLK', 'name': '轴坯', 'category': CAT_RAW, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': '8AT480-SFT-001'},
        {'code': 'MAT-GBX-SHAFT-FIN', 'name': '轴系成品件', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': '8AT480-SFT-101'},
        {'code': 'MAT-GBX-DIFF-ASM', 'name': '差速器总成', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': '8AT480-DIFF-101'},
        {'code': 'MAT-GBX-CLUTCH-MOD', 'name': '离合机电模块', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_KEY, 'drawing': '8AT480-CL-101'},
        {'code': 'MAT-GBX-FIX-KIT', 'name': '紧固件包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': '8AT480-FIX-901'},
        {'code': 'MAT-GBX-SEAL-KIT', 'name': '密封件包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': '8AT480-SEAL-902'},
        {'code': 'MAT-GBX-OIL', 'name': '变速箱油', 'category': CAT_AUX, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': '8AT480-OIL-903', 'unit': '个'},
        {'code': 'MAT-GBX-PKG-KIT', 'name': '包装防护包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': '8AT480-PKG-904'},
        {'code': 'MAT-GBX-GEARBOX-FIN', 'name': '8AT480变速箱总成', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': '8AT480-ASM-999', 'serial': YES},
    ],
    'mboms': [
        {
            'code': 'MBOM-GBX-ASM-A01',
            'material_code': 'MAT-GBX-GEARBOX-FIN',
            'name': '8AT480变速箱总成MBOM',
            'nodes': [
                {'level': 0, 'material_code': 'MAT-GBX-GEARBOX-FIN', 'qty': 1},
                {'level': 1, 'material_code': 'MAT-GBX-HSG-FIN', 'qty': 1, 'parent_material': 'MAT-GBX-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBX-GEAR-FIN', 'qty': 4, 'parent_material': 'MAT-GBX-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBX-SHAFT-FIN', 'qty': 2, 'parent_material': 'MAT-GBX-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBX-DIFF-ASM', 'qty': 1, 'parent_material': 'MAT-GBX-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBX-CLUTCH-MOD', 'qty': 1, 'parent_material': 'MAT-GBX-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBX-FIX-KIT', 'qty': 1, 'parent_material': 'MAT-GBX-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBX-SEAL-KIT', 'qty': 1, 'parent_material': 'MAT-GBX-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBX-OIL', 'qty': 5, 'parent_material': 'MAT-GBX-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBX-PKG-KIT', 'qty': 1, 'parent_material': 'MAT-GBX-GEARBOX-FIN', 'parent_version': 'A.01'},
            ],
        },
    ],
    'routes': [
        {
            'code': 'RT-GBX-HSG-A01',
            'name': '箱体机加工艺',
            'route_spec': '机加',
            'biz': 'BIZ-GBX-HSG',
            'material_code': 'MAT-GBX-HSG-FIN',
            'proc_spec': '机械加工专业',
            'remark': '箱体工厂完成箱体精密机加并转总装工厂',
            'ops': [
                {'no': '0010', 'name': '箱体粗铣与定位基准建立', 'type': '加工', 'wc': 'WC-GBX-HSG-MACH', 'prep': 16, 'run': 30, 'out': 'MAT-GBX-HSG-FIN', 'content': '完成箱体粗铣和定位基准建立', 'materials': [('MAT-GBX-HSG-RAW', 1)], 'steps': [('装夹箱体毛坯', '装夹毛坯并检查定位状态'), ('建立基准', '粗铣关键基准面并建立定位')]},
                {'no': '0020', 'name': '轴承孔与安装面精加工', 'type': '加工', 'wc': 'WC-GBX-HSG-MACH', 'prep': 14, 'run': 28, 'out': 'MAT-GBX-HSG-FIN', 'content': '完成箱体孔系和安装面精加工', 'materials': [], 'steps': [('精镗轴承孔', '完成轴承孔系精加工'), ('精铣安装面', '完成安装面和油路孔精加工')]},
                {'no': '0030', 'name': '箱体尺寸终检', 'type': '检验', 'wc': 'WC-GBX-HSG-TRANSFER', 'prep': 8, 'run': 14, 'out': 'MAT-GBX-HSG-FIN', 'content': '完成箱体尺寸和外观终检', 'materials': [], 'steps': [('检测关键尺寸', '检测箱体关键尺寸和孔位精度'), ('确认放行', '确认箱体放行条件')]},
                {'no': '0040', 'name': '厂际转工至总装工厂', 'type': '厂际转工', 'wc': 'WC-GBX-HSG-TRANSFER', 'prep': 8, 'run': 18, 'out': 'MAT-GBX-HSG-FIN', 'content': '将箱体精加工件转入总装工厂', 'materials': [], 'steps': [('生成转工单据', '生成箱体厂际转工单据'), ('转运至总装待装区', '转运至总装工厂待装区')]},
            ],
        },
        {
            'code': 'RT-GBX-GEAR-A01',
            'name': '齿轮机加工艺',
            'route_spec': '机加',
            'biz': 'BIZ-GBX-GEAR',
            'material_code': 'MAT-GBX-GEAR-MACH',
            'proc_spec': '机械加工专业',
            'remark': '齿轮工厂完成齿坯加工并转热处理工厂',
            'ops': [
                {'no': '0010', 'name': '齿坯车削', 'type': '加工', 'wc': 'WC-GBX-GEAR-MACH', 'prep': 12, 'run': 22, 'out': 'MAT-GBX-GEAR-MACH', 'content': '完成齿坯端面、外圆和基准孔车削', 'materials': [('MAT-GBX-GEAR-BLK', 1)], 'steps': [('车削端面外圆', '完成端面和外圆车削'), ('加工基准孔', '完成中心孔和定位基准加工')]},
                {'no': '0020', 'name': '滚齿与修缘', 'type': '加工', 'wc': 'WC-GBX-GEAR-MACH', 'prep': 10, 'run': 24, 'out': 'MAT-GBX-GEAR-MACH', 'content': '完成齿形加工和修缘', 'materials': [], 'steps': [('执行滚齿', '执行齿形滚削'), ('修缘去毛刺', '完成修缘和去毛刺')]},
                {'no': '0030', 'name': '厂际转工至热处理工厂', 'type': '厂际转工', 'wc': 'WC-GBX-MACH-TRANSFER', 'prep': 8, 'run': 16, 'out': 'MAT-GBX-GEAR-MACH', 'content': '将齿轮机加工件转入热处理工厂', 'materials': [], 'steps': [('生成转工批次', '生成齿轮转工批次'), ('转运至热处理待加工区', '转运至热处理工厂待加工区')]},
            ],
        },
        {
            'code': 'RT-GBX-SHAFT-A01',
            'name': '轴系机加工艺',
            'route_spec': '机加',
            'biz': 'BIZ-GBX-GEAR',
            'material_code': 'MAT-GBX-SHAFT-FIN',
            'proc_spec': '机械加工专业',
            'remark': '齿轴工厂完成轴系加工并转总装工厂',
            'ops': [
                {'no': '0010', 'name': '轴坯车削与基准建立', 'type': '加工', 'wc': 'WC-GBX-SHAFT-MACH', 'prep': 12, 'run': 20, 'out': 'MAT-GBX-SHAFT-FIN', 'content': '完成轴坯外圆、端面和中心孔加工', 'materials': [('MAT-GBX-SHAFT-BLK', 1)], 'steps': [('车削外圆', '完成轴坯外圆车削'), ('建立磨削基准', '建立中心孔和磨削基准')]},
                {'no': '0020', 'name': '花键与油槽加工', 'type': '加工', 'wc': 'WC-GBX-SHAFT-MACH', 'prep': 10, 'run': 18, 'out': 'MAT-GBX-SHAFT-FIN', 'content': '完成花键和油槽加工', 'materials': [], 'steps': [('加工花键', '完成花键成形'), ('加工油槽', '完成油槽和关键槽口加工')]},
                {'no': '0030', 'name': '外圆磨削与终检', 'type': '检验', 'wc': 'WC-GBX-SHAFT-MACH', 'prep': 10, 'run': 16, 'out': 'MAT-GBX-SHAFT-FIN', 'content': '完成轴系磨削、尺寸和跳动终检', 'materials': [], 'steps': [('执行磨削', '完成外圆磨削和精修'), ('完成终检', '完成轴系尺寸和跳动终检')]},
                {'no': '0040', 'name': '厂际转工至总装工厂', 'type': '厂际转工', 'wc': 'WC-GBX-MACH-TRANSFER', 'prep': 8, 'run': 16, 'out': 'MAT-GBX-SHAFT-FIN', 'content': '将轴系成品件转入总装工厂', 'materials': [], 'steps': [('生成转工单据', '生成轴系转工单据'), ('转运至总装待装区', '转运至总装工厂待装区')]},
            ],
        },
        {
            'code': 'RT-GBX-HT-A01',
            'name': '齿轮热处理精整工艺',
            'route_spec': '机加',
            'biz': 'BIZ-GBX-HT',
            'material_code': 'MAT-GBX-GEAR-FIN',
            'proc_spec': '机械加工专业',
            'remark': '热处理工厂完成渗碳淬火、精整与热后放行',
            'ops': [
                {'no': '0010', 'name': '渗碳淬火', 'type': '加工', 'wc': 'WC-GBX-HT-LINE', 'prep': 16, 'run': 220, 'out': 'MAT-GBX-GEAR-FIN', 'content': '完成齿轮渗碳淬火和冷却', 'materials': [('MAT-GBX-GEAR-MACH', 1)], 'steps': [('装炉渗碳', '完成齿轮装炉和渗碳'), ('淬火冷却', '按工艺曲线完成淬火冷却')]},
                {'no': '0020', 'name': '热后精整', 'type': '加工', 'wc': 'WC-GBX-HT-FIN', 'prep': 12, 'run': 24, 'out': 'MAT-GBX-GEAR-FIN', 'content': '完成热后回火和精整修形', 'materials': [], 'steps': [('执行回火', '完成回火稳定处理'), ('热后精整', '完成热后精整和去毛刺')]},
                {'no': '0030', 'name': '热后终检', 'type': '检验', 'wc': 'WC-GBX-HT-CHECK', 'prep': 10, 'run': 18, 'out': 'MAT-GBX-GEAR-FIN', 'content': '完成硬度、金相和尺寸终检', 'materials': [], 'steps': [('检测硬度金相', '检测热处理硬度和金相状态'), ('检测尺寸精度', '检测热后尺寸和变形状态')]},
                {'no': '0040', 'name': '厂际转工至总装工厂', 'type': '厂际转工', 'wc': 'WC-GBX-HT-TRANSFER', 'prep': 8, 'run': 16, 'out': 'MAT-GBX-GEAR-FIN', 'content': '将热后齿轮件转入总装工厂', 'materials': [], 'steps': [('生成转工单据', '生成热后齿轮厂际转工单据'), ('转运至总装待装区', '转运至总装工厂待装区')]},
            ],
        },
        {
            'code': 'RT-GBX-ASM-A01',
            'name': '变速箱总成总装工艺',
            'route_spec': '装配',
            'biz': 'BIZ-GBX-ASM',
            'material_code': 'MAT-GBX-GEARBOX-FIN',
            'proc_spec': '装配专业',
            'remark': '总装工厂完成差速器预装、总装和灌油并转试验工厂',
            'ops': [
                {'no': '0010', 'name': '差速器预装', 'type': '加工', 'wc': 'WC-GBX-DIFF', 'prep': 10, 'run': 16, 'out': 'MAT-GBX-DIFF-ASM', 'content': '完成差速器总成预装', 'materials': [('MAT-GBX-FIX-KIT', 1)], 'steps': [('压装轴承', '完成差速器轴承压装'), ('复核预装状态', '复核差速器间隙和预紧')]},
                {'no': '0020', 'name': '箱体与齿轮轴系合装', 'type': '加工', 'wc': 'WC-GBX-MAINASM', 'prep': 16, 'run': 28, 'out': 'MAT-GBX-GEARBOX-FIN', 'content': '完成箱体、齿轮件和轴系成品件合装', 'materials': [('MAT-GBX-HSG-FIN', 1), ('MAT-GBX-GEAR-FIN', 4), ('MAT-GBX-SHAFT-FIN', 2)], 'steps': [('装入齿轮与轴系', '装入齿轮件和轴系件'), ('复核啮合状态', '复核啮合侧隙和转动阻力')]},
                {'no': '0030', 'name': '离合机电模块安装', 'type': '加工', 'wc': 'WC-GBX-MAINASM', 'prep': 12, 'run': 20, 'out': 'MAT-GBX-GEARBOX-FIN', 'content': '完成离合机电模块和差速器总成装配', 'materials': [('MAT-GBX-DIFF-ASM', 1), ('MAT-GBX-CLUTCH-MOD', 1), ('MAT-GBX-SEAL-KIT', 1), ('MAT-GBX-FIX-KIT', 1)], 'steps': [('安装差速器总成', '安装差速器总成并复核状态'), ('安装离合机电模块', '安装离合机电模块并连接接口')]},
                {'no': '0040', 'name': '灌油与条码绑定', 'type': '加工', 'wc': 'WC-GBX-FLUID', 'prep': 8, 'run': 12, 'out': 'MAT-GBX-GEARBOX-FIN', 'content': '完成定量灌油和条码绑定', 'materials': [('MAT-GBX-OIL', 5)], 'steps': [('执行灌油', '按工艺要求加注油液'), ('绑定条码', '绑定总成条码和关键件追溯')]},
                {'no': '0050', 'name': '厂际转工至试验工厂', 'type': '厂际转工', 'wc': 'WC-GBX-ASM-TRANSFER', 'prep': 8, 'run': 16, 'out': 'MAT-GBX-GEARBOX-FIN', 'content': '将总装完成件转入试验工厂', 'materials': [], 'steps': [('生成转工单据', '生成总装件厂际转工单据'), ('转运至试验待试区', '转运至试验工厂待试区')]},
            ],
        },
        {
            'code': 'RT-GBX-TEST-A01',
            'name': '变速箱试验包装工艺',
            'route_spec': '通用',
            'biz': 'BIZ-GBX-TEST',
            'material_code': 'MAT-GBX-GEARBOX-FIN',
            'proc_spec': '装配专业',
            'remark': '试验工厂完成冷试、EOL、包装和入库',
            'ops': [
                {'no': '0010', 'name': '冷试与换挡响应验证', 'type': '检验', 'wc': 'WC-GBX-TEST-COLD', 'prep': 10, 'run': 18, 'out': 'MAT-GBX-GEARBOX-FIN', 'content': '完成冷试、换挡响应和阻力分析', 'materials': [], 'steps': [('执行冷试', '执行变速箱冷试和换挡响应验证'), ('采集性能参数', '采集阻力和换挡性能参数')]},
                {'no': '0020', 'name': 'EOL综合终检', 'type': '检验', 'wc': 'WC-GBX-TEST-EOL', 'prep': 10, 'run': 16, 'out': 'MAT-GBX-GEARBOX-FIN', 'content': '完成密封、报码和外观终检', 'materials': [], 'steps': [('执行EOL检测', '执行EOL综合检测和报码读取'), ('完成放行判定', '完成终检判定和放行')]},
                {'no': '0030', 'name': '包装入库', 'type': '加工', 'wc': 'WC-GBX-PACK', 'prep': 8, 'run': 12, 'out': 'MAT-GBX-GEARBOX-FIN', 'content': '完成包装防护并转入成品库', 'materials': [('MAT-GBX-PKG-KIT', 1)], 'steps': [('执行包装', '完成包装防护和标签粘贴'), ('转入成品库', '转入成品库并完成交接')]},
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

