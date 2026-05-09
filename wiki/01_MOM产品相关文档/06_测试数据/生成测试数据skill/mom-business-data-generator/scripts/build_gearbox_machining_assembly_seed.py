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

SCENARIO = 'gearbox_machining_assembly'
NAMESPACE = 'GBM31S01'
VOLUME_PROFILE = '大体量版'
ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'gearbox_machining_assembly_seed_big.json'
VARIANT_SPECS = (
    ('gearbox_machining_assembly_seed.json', 'GBM20S01', '标准版'),
    ('gearbox_machining_assembly_seed_big.json', 'GBM31S01', '大体量版'),
    ('gearbox_machining_assembly_seed_ultra.json', 'GBM42S01', '超大体量版'),
)

CONFIG = {
    'metadata': {
        'name': '变速箱机加装配一体化MOM种子',
        'industry': '汽车零部件',
        'product_family': '自动变速箱',
        'product_model': '8AT450自动变速箱',
        'description': '面向单工厂机加+装配场景构建的变速箱生产主数据，覆盖箱体机加、齿轮轴系加工、外协热处理、总装、冷试与终检。',
    },
    'admins': [
        ('0', '公司', 'ADM-GBM-HQ', '启岳传动系统有限公司', '启岳传动'),
        ('ADM-GBM-HQ', '部门', 'ADM-GBM-TECH', '工艺技术部', '工艺技术'),
        ('ADM-GBM-HQ', '部门', 'ADM-GBM-PMC', '生产运营部', '生产运营'),
        ('ADM-GBM-HQ', '部门', 'ADM-GBM-QA', '质量管理部', '质量管理'),
        ('ADM-GBM-HQ', '部门', 'ADM-GBM-WM', '仓储物流部', '仓储物流'),
        ('ADM-GBM-HQ', '部门', 'ADM-GBM-EM', '设备工装部', '设备工装'),
        ('ADM-GBM-HQ', '工厂', 'ADM-GBM-PLANT', '变速箱机加装配一体工厂', '一体工厂', '负责变速箱关键件机加、外协热处理协同和总装检测'),
    ],
    'bizs': [
        ('0', 'BIZ-GBM-COMPANY', '启岳传动系统有限公司', '启岳传动', '公司', 'ADM-GBM-HQ', '', '单工厂机加装配一体化方案'),
        ('BIZ-GBM-COMPANY', 'BIZ-GBM-TECH', '工艺技术部', '工艺技术', '部门', 'ADM-GBM-TECH'),
        ('BIZ-GBM-COMPANY', 'BIZ-GBM-PMC', '生产运营部', '生产运营', '部门', 'ADM-GBM-PMC'),
        ('BIZ-GBM-COMPANY', 'BIZ-GBM-QA', '质量管理部', '质量管理', '部门', 'ADM-GBM-QA'),
        ('BIZ-GBM-COMPANY', 'BIZ-GBM-WM', '仓储物流部', '仓储物流', '部门', 'ADM-GBM-WM'),
        ('BIZ-GBM-COMPANY', 'BIZ-GBM-EM', '设备工装部', '设备工装', '部门', 'ADM-GBM-EM'),
        ('BIZ-GBM-COMPANY', 'BIZ-GBM-PLANT', '变速箱机加装配一体工厂', '一体工厂', '工厂', 'ADM-GBM-PLANT', '机械加工专业', '箱体、齿轮轴系机加与总装检测在同厂协同完成'),
        ('BIZ-GBM-PLANT', 'BIZ-GBM-MACH-WS', '机加车间', '机加车间', '车间', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-PLANT', 'BIZ-GBM-ASM-WS', '总装检测车间', '总装检测', '车间', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-MACH-WS', 'BIZ-GBM-HSG-SEC', '箱体机加工段', '箱体机加', '工段', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-MACH-WS', 'BIZ-GBM-GEAR-SEC', '齿轮加工段', '齿轮加工', '工段', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-MACH-WS', 'BIZ-GBM-SHAFT-SEC', '轴系加工段', '轴系加工', '工段', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-MACH-WS', 'BIZ-GBM-HT-SEC', '热处理协同段', '热处理协同', '工段', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-ASM-WS', 'BIZ-GBM-DIFF-SEC', '差速器预装段', '差速器预装', '工段', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-ASM-WS', 'BIZ-GBM-MAINASM-SEC', '总装工段', '总装工段', '工段', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-ASM-WS', 'BIZ-GBM-TEST-SEC', '检测试验段', '检测试验', '工段', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-ASM-WS', 'BIZ-GBM-PACK-SEC', '包装工段', '包装工段', '工段', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-HSG-SEC', 'BIZ-GBM-HSG-A', '箱体机加甲班', '箱体甲班', '班组', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-GEAR-SEC', 'BIZ-GBM-GEAR-A', '齿轮加工甲班', '齿轮甲班', '班组', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-SHAFT-SEC', 'BIZ-GBM-SHAFT-A', '轴系加工甲班', '轴系甲班', '班组', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-DIFF-SEC', 'BIZ-GBM-DIFF-A', '差速器预装甲班', '差速器甲班', '班组', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-MAINASM-SEC', 'BIZ-GBM-MAINASM-A', '总装甲班', '总装甲班', '班组', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-TEST-SEC', 'BIZ-GBM-TEST-A', '测试甲班', '测试甲班', '班组', 'ADM-GBM-PLANT'),
        ('BIZ-GBM-PACK-SEC', 'BIZ-GBM-PACK-A', '包装甲班', '包装甲班', '班组', 'ADM-GBM-PLANT'),
    ],
    'users': [
        ('U-GBM-001', '沈嘉豪', '重要', '男', 'ADM-GBM-TECH', 'BIZ-GBM-TECH', '工艺平台主管'),
        ('U-GBM-002', '苏清妍', '重要', '女', 'ADM-GBM-TECH', 'BIZ-GBM-TECH', '箱体机加工艺工程师'),
        ('U-GBM-003', '贺承宇', '重要', '男', 'ADM-GBM-TECH', 'BIZ-GBM-TECH', '热处理工艺工程师'),
        ('U-GBM-004', '熊语汐', '重要', '女', 'ADM-GBM-TECH', 'BIZ-GBM-TECH', '总装工艺工程师'),
        ('U-GBM-005', '石景明', '重要', '男', 'ADM-GBM-PMC', 'BIZ-GBM-PMC', '主计划员'),
        ('U-GBM-006', '乐安宁', '一般', '女', 'ADM-GBM-QA', 'BIZ-GBM-QA', '机加质量工程师'),
        ('U-GBM-007', '邹书恒', '一般', '男', 'ADM-GBM-QA', 'BIZ-GBM-QA', '终检工程师'),
        ('U-GBM-008', '常可欣', '一般', '女', 'ADM-GBM-WM', 'BIZ-GBM-WM', '仓库管理员'),
        ('U-GBM-009', '安景程', '一般', '男', 'ADM-GBM-EM', 'BIZ-GBM-EM', '设备工程师'),
        ('U-GBM-010', '毕思远', '一般', '男', 'ADM-GBM-PLANT', 'BIZ-GBM-HSG-A', '箱体机加班组长'),
        ('U-GBM-011', '郝晨悦', '一般', '女', 'ADM-GBM-PLANT', 'BIZ-GBM-HSG-A', '机加操作工'),
        ('U-GBM-012', '殷清雅', '一般', '女', 'ADM-GBM-PLANT', 'BIZ-GBM-GEAR-A', '齿轮加工班组长'),
        ('U-GBM-013', '滕启航', '一般', '男', 'ADM-GBM-PLANT', 'BIZ-GBM-GEAR-A', '机加操作工'),
        ('U-GBM-014', '汤嘉宁', '一般', '女', 'ADM-GBM-PLANT', 'BIZ-GBM-SHAFT-A', '轴系加工班组长'),
        ('U-GBM-015', '倪承泽', '一般', '男', 'ADM-GBM-PLANT', 'BIZ-GBM-SHAFT-A', '磨削操作工'),
        ('U-GBM-016', '贺书远', '一般', '男', 'ADM-GBM-PLANT', 'BIZ-GBM-DIFF-A', '差速器预装工'),
        ('U-GBM-017', '韦语桐', '一般', '女', 'ADM-GBM-PLANT', 'BIZ-GBM-MAINASM-A', '总装班组长'),
        ('U-GBM-018', '陆安然', '一般', '男', 'ADM-GBM-PLANT', 'BIZ-GBM-MAINASM-A', '装配操作工'),
        ('U-GBM-019', '范可宁', '一般', '女', 'ADM-GBM-PLANT', 'BIZ-GBM-TEST-A', '冷试检验员'),
        ('U-GBM-020', '金景川', '一般', '男', 'ADM-GBM-PLANT', 'BIZ-GBM-PACK-A', '包装操作工'),
    ],
    'suppliers': [
        {'code': 'SUP-GBM-CAST', 'name': '苏州壳体铸件有限公司', 'short': '壳体铸件', 'remark': '供应箱体毛坯'},
        {'code': 'SUP-GBM-STEEL', 'name': '常州合金钢材有限公司', 'short': '合金钢材', 'remark': '供应齿轮和轴系原材料'},
        {'code': 'SUP-GBM-HT', 'name': '无锡热处理服务有限公司', 'short': '无锡热处理', 'remark': '承担齿轮渗碳淬火与回火外协'},
        {'code': 'SUP-GBM-CLUTCH', 'name': '芜湖离合器系统有限公司', 'short': '离合器系统', 'remark': '供应离合器组件'},
        {'code': 'SUP-GBM-DIFF', 'name': '南京差速器科技有限公司', 'short': '差速器科技', 'remark': '供应差速器零组件'},
    ],
    'work_centers': [
        {'code': 'WC-GBM-HSG-MACH', 'name': '箱体精密机加线', 'biz': 'BIZ-GBM-HSG-SEC', 'wc_type': '产线', 'wc_class': '加工', 'remark': '负责箱体粗精加工和孔系加工'},
        {'code': 'WC-GBM-GEAR-HOB', 'name': '齿轮滚齿线', 'biz': 'BIZ-GBM-GEAR-SEC', 'wc_type': '产线', 'wc_class': '加工'},
        {'code': 'WC-GBM-SHAFT-GRIND', 'name': '轴系磨削线', 'biz': 'BIZ-GBM-SHAFT-SEC', 'wc_type': '产线', 'wc_class': '加工'},
        {'code': 'WC-GBM-OUT-HT', 'name': '外协热处理中心', 'biz': 'BIZ-GBM-HT-SEC', 'wc_type': '外委', 'wc_class': '加工', 'remark': '承担齿轮渗碳淬火和回火'},
        {'code': 'WC-GBM-CLEAN', 'name': '清洗去毛刺工位', 'biz': 'BIZ-GBM-HSG-SEC', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBM-CMM', 'name': '三坐标检测工位', 'biz': 'BIZ-GBM-HSG-SEC', 'wc_type': '组织', 'wc_class': '检验'},
        {'code': 'WC-GBM-DIFF', 'name': '差速器预装工位', 'biz': 'BIZ-GBM-DIFF-SEC', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBM-MAINASM', 'name': '总装线', 'biz': 'BIZ-GBM-MAINASM-SEC', 'wc_type': '产线', 'wc_class': '加工'},
        {'code': 'WC-GBM-FLUID', 'name': '灌油工位', 'biz': 'BIZ-GBM-MAINASM-SEC', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBM-COLDTEST', 'name': '冷试工位', 'biz': 'BIZ-GBM-TEST-SEC', 'wc_type': '组织', 'wc_class': '检验'},
        {'code': 'WC-GBM-LEAK', 'name': '密封终检工位', 'biz': 'BIZ-GBM-TEST-SEC', 'wc_type': '组织', 'wc_class': '检验'},
        {'code': 'WC-GBM-PACK', 'name': '包装入库工位', 'biz': 'BIZ-GBM-PACK-SEC', 'wc_type': '组织', 'wc_class': '加工'},
    ],
    'equipments': [
        {'code': 'EQ-GBM-HSG-01', 'name': '卧式加工中心', 'model': 'HMC-800', 'biz': 'BIZ-GBM-HSG-SEC', 'bottle': YES},
        {'code': 'EQ-GBM-HSG-02', 'name': '阀体面精铣中心', 'model': 'FM-600', 'biz': 'BIZ-GBM-HSG-SEC', 'bottle': NO},
        {'code': 'EQ-GBM-GEAR-01', 'name': '数控滚齿机', 'model': 'GH-350', 'biz': 'BIZ-GBM-GEAR-SEC', 'bottle': YES},
        {'code': 'EQ-GBM-GEAR-02', 'name': '磨齿机', 'model': 'GG-280', 'biz': 'BIZ-GBM-GEAR-SEC', 'bottle': YES},
        {'code': 'EQ-GBM-SHAFT-01', 'name': '数控外圆磨床', 'model': 'OG-630', 'biz': 'BIZ-GBM-SHAFT-SEC', 'bottle': YES},
        {'code': 'EQ-GBM-CLEAN-01', 'name': '高压清洗机', 'model': 'CL-20', 'biz': 'BIZ-GBM-HSG-SEC', 'bottle': NO},
        {'code': 'EQ-GBM-CMM-01', 'name': '三坐标测量机', 'model': 'CMM-1200', 'biz': 'BIZ-GBM-HSG-SEC', 'bottle': NO},
        {'code': 'EQ-GBM-DIFF-01', 'name': '差速器压装机', 'model': 'DP-160', 'biz': 'BIZ-GBM-DIFF-SEC', 'bottle': NO},
        {'code': 'EQ-GBM-ASM-01', 'name': '总装输送线', 'model': 'ASM-24M', 'biz': 'BIZ-GBM-MAINASM-SEC', 'bottle': YES},
        {'code': 'EQ-GBM-FILL-01', 'name': '定量灌油机', 'model': 'OF-16', 'biz': 'BIZ-GBM-MAINASM-SEC', 'bottle': NO},
        {'code': 'EQ-GBM-COLD-01', 'name': '变速箱冷试台', 'model': 'CT-450', 'biz': 'BIZ-GBM-TEST-SEC', 'bottle': YES},
        {'code': 'EQ-GBM-LEAK-01', 'name': '泄漏检测仪', 'model': 'LK-08', 'biz': 'BIZ-GBM-TEST-SEC', 'bottle': NO},
        {'code': 'EQ-GBM-PACK-01', 'name': '封箱工作站', 'model': 'PK-08', 'biz': 'BIZ-GBM-PACK-SEC', 'bottle': NO},
    ],
    'tools': [
        {'code': 'TOOL-GBM-HSG-01', 'name': '箱体定位夹具', 'material_category': CAT_KIT, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_KEY, 'model': 'JG-HSG-11', 'spec': '箱体定位', 'remark': '控制箱体孔系加工定位', 'life_times': 100000, 'life_days': 365},
        {'code': 'TOOL-GBM-GEAR-01', 'name': '滚齿夹具', 'material_category': CAT_KIT, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_IMPORTANT, 'model': 'JG-GR-21', 'spec': '滚齿定位', 'remark': '用于齿坯滚齿定位', 'life_times': 90000, 'life_days': 365},
        {'code': 'TOOL-GBM-SHAFT-01', 'name': '轴系磨削顶尖', 'material_category': CAT_PART, 'make_type': MAKE_BUY, 'tooling_category': '通用工具', 'feature': FEATURE_IMPORTANT, 'model': 'TP-63', 'spec': '磨削顶尖', 'remark': '用于轴系外圆磨削', 'life_times': 60000, 'life_days': 180},
        {'code': 'TOOL-GBM-DIFF-01', 'name': '差速器预装工装', 'material_category': CAT_KIT, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_KEY, 'model': 'JG-DIFF-01', 'spec': '差速器预装', 'remark': '用于差速器轴承与行星架预装', 'life_times': 70000, 'life_days': 365},
        {'code': 'TOOL-GBM-TORQUE-01', 'name': '多轴扭矩枪', 'material_category': CAT_PART, 'make_type': MAKE_BUY, 'tooling_category': '通用工具', 'feature': FEATURE_KEY, 'model': 'TW-180', 'spec': '30-180Nm', 'remark': '采集总装紧固扭矩', 'life_times': 50000, 'life_days': 180},
    ],
    'wc_user_links': [
        ('WC-GBM-HSG-MACH', 'U-GBM-002'), ('WC-GBM-HSG-MACH', 'U-GBM-010'), ('WC-GBM-HSG-MACH', 'U-GBM-011'),
        ('WC-GBM-GEAR-HOB', 'U-GBM-003'), ('WC-GBM-GEAR-HOB', 'U-GBM-012'), ('WC-GBM-GEAR-HOB', 'U-GBM-013'),
        ('WC-GBM-SHAFT-GRIND', 'U-GBM-014'), ('WC-GBM-SHAFT-GRIND', 'U-GBM-015'), ('WC-GBM-OUT-HT', 'U-GBM-005'),
        ('WC-GBM-DIFF', 'U-GBM-016'), ('WC-GBM-MAINASM', 'U-GBM-004'), ('WC-GBM-MAINASM', 'U-GBM-017'), ('WC-GBM-MAINASM', 'U-GBM-018'),
        ('WC-GBM-COLDTEST', 'U-GBM-019'), ('WC-GBM-LEAK', 'U-GBM-007'), ('WC-GBM-PACK', 'U-GBM-020'),
    ],
    'wc_eq_links': [
        ('WC-GBM-HSG-MACH', 'EQ-GBM-HSG-01'), ('WC-GBM-HSG-MACH', 'EQ-GBM-HSG-02'), ('WC-GBM-CLEAN', 'EQ-GBM-CLEAN-01'), ('WC-GBM-CMM', 'EQ-GBM-CMM-01'),
        ('WC-GBM-GEAR-HOB', 'EQ-GBM-GEAR-01'), ('WC-GBM-GEAR-HOB', 'EQ-GBM-GEAR-02'), ('WC-GBM-SHAFT-GRIND', 'EQ-GBM-SHAFT-01'),
        ('WC-GBM-DIFF', 'EQ-GBM-DIFF-01'), ('WC-GBM-MAINASM', 'EQ-GBM-ASM-01'), ('WC-GBM-FLUID', 'EQ-GBM-FILL-01'),
        ('WC-GBM-COLDTEST', 'EQ-GBM-COLD-01'), ('WC-GBM-LEAK', 'EQ-GBM-LEAK-01'), ('WC-GBM-PACK', 'EQ-GBM-PACK-01'),
    ],
    'wc_sup_links': [('WC-GBM-OUT-HT', 'SUP-GBM-HT')],
    'warehouses': [
        ('WH-GBM-RAW', '原材料库', 'BIZ-GBM-WM', 'ERP一级库', '普通库房', '存放箱体毛坯、钢材和外购件'),
        ('WH-GBM-WIP', '在制品暂存库', 'BIZ-GBM-WM', '车间二级库', '普通库房', '存放机加件、热处理回厂件和待装总成'),
        ('WH-GBM-FG', '成品库', 'BIZ-GBM-WM', 'ERP二级库', '普通库房', '存放放行后的变速箱成品'),
    ],
    'locations': [
        ('LOC-GBM-RAW-01', '箱体毛坯区', 'BIZ-GBM-WM', 'WH-GBM-RAW'), ('LOC-GBM-RAW-02', '钢材外购件区', 'BIZ-GBM-WM', 'WH-GBM-RAW'),
        ('LOC-GBM-WIP-01', '箱体在制区', 'BIZ-GBM-WM', 'WH-GBM-WIP'), ('LOC-GBM-WIP-02', '热处理回厂区', 'BIZ-GBM-WM', 'WH-GBM-WIP'), ('LOC-GBM-WIP-03', '待装区', 'BIZ-GBM-WM', 'WH-GBM-WIP'),
        ('LOC-GBM-FG-01', '成品待发区', 'BIZ-GBM-WM', 'WH-GBM-FG'),
    ],
    'materials': [
        {'code': 'MAT-GBM-HSG-RAW', 'name': '箱体毛坯', 'category': CAT_RAW, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': '8AT450-HSG-001'},
        {'code': 'MAT-GBM-HSG-FIN', 'name': '箱体精加工件', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': '8AT450-HSG-101'},
        {'code': 'MAT-GBM-GEAR-BLK', 'name': '齿轮坯件', 'category': CAT_RAW, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': '8AT450-GR-001'},
        {'code': 'MAT-GBM-GEAR-HOB', 'name': '滚齿件', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_IMPORTANT, 'drawing': '8AT450-GR-101'},
        {'code': 'MAT-GBM-GEAR-HT', 'name': '热处理齿轮件', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_IMPORTANT, 'drawing': '8AT450-GR-201'},
        {'code': 'MAT-GBM-GEAR-FIN', 'name': '磨齿成品件', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': '8AT450-GR-301'},
        {'code': 'MAT-GBM-SHAFT-BLK', 'name': '轴坯', 'category': CAT_RAW, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': '8AT450-SFT-001'},
        {'code': 'MAT-GBM-SHAFT-FIN', 'name': '轴系成品件', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': '8AT450-SFT-101'},
        {'code': 'MAT-GBM-DIFF-ASM', 'name': '差速器总成', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': '8AT450-DIFF-101'},
        {'code': 'MAT-GBM-CLUTCH-ASM', 'name': '离合器组件', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_KEY, 'drawing': '8AT450-CL-101'},
        {'code': 'MAT-GBM-FIX-KIT', 'name': '紧固件包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': '8AT450-FIX-901'},
        {'code': 'MAT-GBM-SEAL-KIT', 'name': '密封件包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': '8AT450-SEAL-902'},
        {'code': 'MAT-GBM-OIL', 'name': '变速箱油', 'category': CAT_AUX, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': '8AT450-OIL-903', 'unit': '个'},
        {'code': 'MAT-GBM-PKG-KIT', 'name': '包装防护包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': '8AT450-PKG-904'},
        {'code': 'MAT-GBM-GEARBOX-FIN', 'name': '8AT450变速箱总成', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': '8AT450-ASM-999', 'serial': YES},
    ],
    'mboms': [
        {
            'code': 'MBOM-GBM-ASM-A01',
            'material_code': 'MAT-GBM-GEARBOX-FIN',
            'name': '8AT450变速箱总成MBOM',
            'nodes': [
                {'level': 0, 'material_code': 'MAT-GBM-GEARBOX-FIN', 'qty': 1},
                {'level': 1, 'material_code': 'MAT-GBM-HSG-FIN', 'qty': 1, 'parent_material': 'MAT-GBM-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBM-GEAR-FIN', 'qty': 4, 'parent_material': 'MAT-GBM-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBM-SHAFT-FIN', 'qty': 2, 'parent_material': 'MAT-GBM-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBM-DIFF-ASM', 'qty': 1, 'parent_material': 'MAT-GBM-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBM-CLUTCH-ASM', 'qty': 1, 'parent_material': 'MAT-GBM-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBM-FIX-KIT', 'qty': 1, 'parent_material': 'MAT-GBM-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBM-SEAL-KIT', 'qty': 1, 'parent_material': 'MAT-GBM-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBM-OIL', 'qty': 5, 'parent_material': 'MAT-GBM-GEARBOX-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-GBM-PKG-KIT', 'qty': 1, 'parent_material': 'MAT-GBM-GEARBOX-FIN', 'parent_version': 'A.01'},
            ],
        },
    ],
    'routes': [
        {
            'code': 'RT-GBM-HSG-A01',
            'name': '箱体精密机加工艺',
            'route_spec': '机加',
            'biz': 'BIZ-GBM-MACH-WS',
            'material_code': 'MAT-GBM-HSG-FIN',
            'proc_spec': '机械加工专业',
            'remark': '完成箱体基准面、孔系和阀体面加工',
            'ops': [
                {'no': '0010', 'name': '箱体粗铣与定位基准建立', 'type': '加工', 'wc': 'WC-GBM-HSG-MACH', 'prep': 16, 'run': 34, 'out': 'MAT-GBM-HSG-FIN', 'content': '完成箱体基准面粗铣与主定位基准建立', 'materials': [('MAT-GBM-HSG-RAW', 1)], 'steps': [('装夹箱体毛坯', '装夹箱体毛坯并复核定位状态'), ('建立加工基准', '粗铣关键基准面并建立定位基准')]},
                {'no': '0020', 'name': '轴承孔与阀体面精加工', 'type': '加工', 'wc': 'WC-GBM-HSG-MACH', 'prep': 14, 'run': 30, 'out': 'MAT-GBM-HSG-FIN', 'content': '完成轴承孔、阀体面和油路孔加工', 'materials': [], 'steps': [('精镗轴承孔', '精镗关键轴承孔并控制同轴度'), ('精铣阀体面', '加工阀体安装面与油路孔')]},
                {'no': '0030', 'name': '清洗去毛刺', 'type': '加工', 'wc': 'WC-GBM-CLEAN', 'prep': 8, 'run': 14, 'out': 'MAT-GBM-HSG-FIN', 'content': '完成切屑清理、去毛刺和吹扫', 'materials': [], 'steps': [('高压清洗', '对箱体执行高压清洗和吹扫'), ('人工去毛刺', '清理孔口毛刺并复核倒角')]},
                {'no': '0040', 'name': '三坐标终检', 'type': '检验', 'wc': 'WC-GBM-CMM', 'prep': 10, 'run': 18, 'out': 'MAT-GBM-HSG-FIN', 'content': '完成箱体关键尺寸终检', 'materials': [], 'steps': [('执行尺寸检测', '执行孔系和安装面关键尺寸检测'), ('判定放行状态', '判定箱体加工件放行状态')]},
            ],
        },
        {
            'code': 'RT-GBM-GEAR-A01',
            'name': '齿轮机加热处理工艺',
            'route_spec': '机加',
            'biz': 'BIZ-GBM-MACH-WS',
            'material_code': 'MAT-GBM-GEAR-FIN',
            'proc_spec': '机械加工专业',
            'remark': '完成齿轮坯件车削、滚齿、外协热处理和磨齿放行',
            'ops': [
                {'no': '0010', 'name': '齿坯车削', 'type': '加工', 'wc': 'WC-GBM-GEAR-HOB', 'prep': 12, 'run': 24, 'out': 'MAT-GBM-GEAR-HOB', 'content': '完成齿坯端面、外圆和基准孔车削', 'materials': [('MAT-GBM-GEAR-BLK', 1)], 'steps': [('车削端面外圆', '完成端面和外圆加工'), ('加工基准孔', '加工中心孔和定位基准')]},
                {'no': '0020', 'name': '滚齿成形', 'type': '加工', 'wc': 'WC-GBM-GEAR-HOB', 'prep': 10, 'run': 26, 'out': 'MAT-GBM-GEAR-HOB', 'content': '完成齿形滚削与齿向控制', 'materials': [], 'steps': [('执行滚齿', '执行齿形滚削并控制齿向'), ('复核齿坯状态', '复核齿坯齿顶余量和齿面状态')]},
                {'no': '0030', 'name': '外协渗碳淬火', 'type': '外委', 'wc': 'WC-GBM-OUT-HT', 'prep': 12, 'run': 240, 'out': 'MAT-GBM-GEAR-HT', 'content': '通过外协渗碳淬火提升齿面硬度和疲劳性能', 'materials': [('MAT-GBM-GEAR-HOB', 1)], 'steps': [('生成外协批次', '生成外协委外单和批次追溯信息'), ('回厂检收', '完成热处理回厂检收和报告核对')]},
                {'no': '0040', 'name': '磨齿精修', 'type': '加工', 'wc': 'WC-GBM-GEAR-HOB', 'prep': 14, 'run': 28, 'out': 'MAT-GBM-GEAR-FIN', 'content': '完成磨齿修形与齿面粗糙度控制', 'materials': [('MAT-GBM-GEAR-HT', 1)], 'steps': [('执行磨齿修形', '完成齿形齿向修形'), ('复核齿面质量', '复核齿面粗糙度和齿向误差')]},
                {'no': '0050', 'name': '齿轮终检', 'type': '检验', 'wc': 'WC-GBM-CMM', 'prep': 8, 'run': 16, 'out': 'MAT-GBM-GEAR-FIN', 'content': '完成齿轮精度和热处理状态终检', 'materials': [], 'steps': [('检测齿轮精度', '检测齿形、齿向和跳动精度'), ('核对热处理结果', '核对硬度和金相报告')]},
            ],
        },
        {
            'code': 'RT-GBM-SHAFT-A01',
            'name': '轴系精密加工艺',
            'route_spec': '机加',
            'biz': 'BIZ-GBM-MACH-WS',
            'material_code': 'MAT-GBM-SHAFT-FIN',
            'proc_spec': '机械加工专业',
            'remark': '完成轴坯车削、花键加工、磨削与终检',
            'ops': [
                {'no': '0010', 'name': '轴坯车削与基准建立', 'type': '加工', 'wc': 'WC-GBM-SHAFT-GRIND', 'prep': 12, 'run': 22, 'out': 'MAT-GBM-SHAFT-FIN', 'content': '完成轴坯端面、外圆和中心孔加工', 'materials': [('MAT-GBM-SHAFT-BLK', 1)], 'steps': [('车削外圆', '完成外圆和端面车削'), ('建立中心孔', '建立磨削基准中心孔')]},
                {'no': '0020', 'name': '花键与油槽加工', 'type': '加工', 'wc': 'WC-GBM-SHAFT-GRIND', 'prep': 10, 'run': 20, 'out': 'MAT-GBM-SHAFT-FIN', 'content': '完成花键滚压和油槽加工', 'materials': [], 'steps': [('加工花键', '完成花键成形和去毛刺'), ('加工油槽', '完成油槽和关键槽口加工')]},
                {'no': '0030', 'name': '外圆磨削', 'type': '加工', 'wc': 'WC-GBM-SHAFT-GRIND', 'prep': 10, 'run': 20, 'out': 'MAT-GBM-SHAFT-FIN', 'content': '完成关键轴颈外圆磨削', 'materials': [], 'steps': [('磨削轴颈', '完成轴颈和挡肩外圆磨削'), ('复核跳动', '复核同轴度和圆跳动')]},
                {'no': '0040', 'name': '轴系终检', 'type': '检验', 'wc': 'WC-GBM-CMM', 'prep': 8, 'run': 14, 'out': 'MAT-GBM-SHAFT-FIN', 'content': '完成轴系尺寸和跳动终检', 'materials': [], 'steps': [('检测关键尺寸', '检测轴系尺寸、公差和表面粗糙度'), ('判定放行', '判定轴系成品放行状态')]},
            ],
        },
        {
            'code': 'RT-GBM-ASM-A01',
            'name': '变速箱总装检测工艺',
            'route_spec': '装配',
            'biz': 'BIZ-GBM-ASM-WS',
            'material_code': 'MAT-GBM-GEARBOX-FIN',
            'proc_spec': '装配专业',
            'remark': '完成差速器预装、总装、灌油、冷试和终检包装',
            'ops': [
                {'no': '0010', 'name': '差速器预装', 'type': '加工', 'wc': 'WC-GBM-DIFF', 'prep': 12, 'run': 18, 'out': 'MAT-GBM-DIFF-ASM', 'content': '完成差速器轴承和行星架预装', 'materials': [('MAT-GBM-FIX-KIT', 1)], 'steps': [('压装差速器轴承', '完成差速器轴承压装'), ('复核预装状态', '复核间隙和旋转阻力')]},
                {'no': '0020', 'name': '箱体与齿轮轴系合装', 'type': '加工', 'wc': 'WC-GBM-MAINASM', 'prep': 16, 'run': 28, 'out': 'MAT-GBM-GEARBOX-FIN', 'content': '完成箱体、齿轮件和轴系成品件合装', 'materials': [('MAT-GBM-HSG-FIN', 1), ('MAT-GBM-GEAR-FIN', 4), ('MAT-GBM-SHAFT-FIN', 2), ('MAT-GBM-FIX-KIT', 1)], 'steps': [('装入齿轮和轴系', '完成齿轮件、轴系成品件装配'), ('复核啮合间隙', '复核啮合侧隙和转动阻力')]},
                {'no': '0030', 'name': '离合器组件安装', 'type': '加工', 'wc': 'WC-GBM-MAINASM', 'prep': 12, 'run': 20, 'out': 'MAT-GBM-GEARBOX-FIN', 'content': '完成离合器组件和差速器总成装配', 'materials': [('MAT-GBM-DIFF-ASM', 1), ('MAT-GBM-CLUTCH-ASM', 1), ('MAT-GBM-SEAL-KIT', 1)], 'steps': [('安装差速器', '完成差速器总成装入'), ('安装离合器组件', '安装离合器组件并复核密封状态')]},
                {'no': '0040', 'name': '加注油液', 'type': '加工', 'wc': 'WC-GBM-FLUID', 'prep': 8, 'run': 12, 'out': 'MAT-GBM-GEARBOX-FIN', 'content': '完成定量灌油和液位核对', 'materials': [('MAT-GBM-OIL', 5)], 'steps': [('执行灌油', '按工艺要求定量加注油液'), ('核对液位', '核对液位和油液追溯信息')]},
                {'no': '0050', 'name': '冷试与密封检测', 'type': '检验', 'wc': 'WC-GBM-COLDTEST', 'prep': 10, 'run': 18, 'out': 'MAT-GBM-GEARBOX-FIN', 'content': '完成冷试、挡位响应和阻力分析', 'materials': [], 'steps': [('执行冷试', '执行总成冷试和换挡响应测试'), ('采集性能参数', '记录阻力、温升和换挡数据')]},
                {'no': '0060', 'name': '终检包装入库', 'type': '检验', 'wc': 'WC-GBM-LEAK', 'prep': 10, 'run': 16, 'out': 'MAT-GBM-GEARBOX-FIN', 'content': '完成气密终检、外观确认和包装入库', 'materials': [('MAT-GBM-PKG-KIT', 1)], 'steps': [('执行气密终检', '完成密封和外观状态终检'), ('包装入库', '完成包装并转入成品库')]},
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

