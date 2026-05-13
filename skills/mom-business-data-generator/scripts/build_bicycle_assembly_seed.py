from __future__ import annotations

import json
import sys
from copy import deepcopy
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
    YES,
    SeedBuilder,
    summarize_seed,
)
from production_order_seed import apply_production_orders
from scene_seed_upgrades import (
    clear_tool_strategy_relations,
    filter_wc_supplier_relations,
    normalize_poc_security,
    normalize_storage_factory_org,
    normalize_release_user,
    normalize_sequence_relations,
    normalize_user_codes,
)

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

SCENARIO = 'bicycle_assembly'
NAMESPACE = 'BCA20S01'
VOLUME_PROFILE = '标准版'
ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'bicycle_assembly_seed.json'

CONFIG = {
    'metadata': {
        'name': '自行车单工厂总装MOM种子',
        'industry': '两轮车制造',
        'product_family': '城市通勤自行车',
        'product_model': 'CTB-26S城市通勤自行车整车',
        'description': '面向单工厂自行车总装检测场景构建的标准版主数据，覆盖来料齐套、轮组预装、传动与制动安装、整车总装调校、路试与包装入库。',
    },
    'admins': [
        ('0', '公司', 'ADM-BCA-HQ', '启航两轮科技有限公司', '启航两轮'),
        ('ADM-BCA-HQ', '部门', 'ADM-BCA-TECH', '工艺技术部', '工艺技术'),
        ('ADM-BCA-HQ', '部门', 'ADM-BCA-PMC', '生产运营部', '生产运营'),
        ('ADM-BCA-HQ', '部门', 'ADM-BCA-QA', '质量管理部', '质量管理'),
        ('ADM-BCA-HQ', '部门', 'ADM-BCA-WM', '仓储物流部', '仓储物流'),
        ('ADM-BCA-HQ', '部门', 'ADM-BCA-EM', '设备工装部', '设备工装'),
        ('ADM-BCA-HQ', '工厂', 'ADM-BCA-PLANT', '自行车总装工厂', '自行车工厂', '负责城市通勤自行车的总装、调校、检测和包装入库'),
    ],
    'bizs': [
        ('0', 'BIZ-BCA-COMPANY', '启航两轮科技有限公司', '启航两轮', '公司', 'ADM-BCA-HQ', '', '单工厂自行车总装场景'),
        ('BIZ-BCA-COMPANY', 'BIZ-BCA-TECH', '工艺技术部', '工艺技术', '部门', 'ADM-BCA-TECH'),
        ('BIZ-BCA-COMPANY', 'BIZ-BCA-PMC', '生产运营部', '生产运营', '部门', 'ADM-BCA-PMC'),
        ('BIZ-BCA-COMPANY', 'BIZ-BCA-QA', '质量管理部', '质量管理', '部门', 'ADM-BCA-QA'),
        ('BIZ-BCA-COMPANY', 'BIZ-BCA-WM', '仓储物流部', '仓储物流', '部门', 'ADM-BCA-WM'),
        ('BIZ-BCA-COMPANY', 'BIZ-BCA-EM', '设备工装部', '设备工装', '部门', 'ADM-BCA-EM'),
        ('BIZ-BCA-COMPANY', 'BIZ-BCA-PLANT', '自行车总装工厂', '自行车工厂', '工厂', 'ADM-BCA-PLANT', '装配专业', '单工厂自行车总装，不含外委和跨厂转工'),
        ('BIZ-BCA-PLANT', 'BIZ-BCA-ASM-WS', '总装车间', '总装车间', '车间', 'ADM-BCA-PLANT'),
        ('BIZ-BCA-ASM-WS', 'BIZ-BCA-KIT-SEC', '齐套工段', '齐套工段', '工段', 'ADM-BCA-PLANT'),
        ('BIZ-BCA-ASM-WS', 'BIZ-BCA-WHEEL-SEC', '轮组预装工段', '轮组预装', '工段', 'ADM-BCA-PLANT'),
        ('BIZ-BCA-ASM-WS', 'BIZ-BCA-MAIN-SEC', '整车总装工段', '整车总装', '工段', 'ADM-BCA-PLANT'),
        ('BIZ-BCA-ASM-WS', 'BIZ-BCA-TUNE-SEC', '调校检测工段', '调校检测', '工段', 'ADM-BCA-PLANT'),
        ('BIZ-BCA-ASM-WS', 'BIZ-BCA-PACK-SEC', '包装入库工段', '包装入库', '工段', 'ADM-BCA-PLANT'),
        ('BIZ-BCA-KIT-SEC', 'BIZ-BCA-KIT-A', '齐套甲班', '齐套甲班', '班组', 'ADM-BCA-PLANT'),
        ('BIZ-BCA-WHEEL-SEC', 'BIZ-BCA-WHEEL-A', '轮组甲班', '轮组甲班', '班组', 'ADM-BCA-PLANT'),
        ('BIZ-BCA-MAIN-SEC', 'BIZ-BCA-MAIN-A', '总装甲班', '总装甲班', '班组', 'ADM-BCA-PLANT'),
        ('BIZ-BCA-TUNE-SEC', 'BIZ-BCA-TUNE-A', '调校甲班', '调校甲班', '班组', 'ADM-BCA-PLANT'),
        ('BIZ-BCA-PACK-SEC', 'BIZ-BCA-PACK-A', '包装甲班', '包装甲班', '班组', 'ADM-BCA-PLANT'),
    ],
    'users': [
        ('U-BCA-001', '程亦凡', '重要', '男', 'ADM-BCA-TECH', 'BIZ-BCA-TECH', '工艺工程师'),
        ('U-BCA-002', '夏知遥', '重要', '女', 'ADM-BCA-PMC', 'BIZ-BCA-PMC', '主计划员'),
        ('U-BCA-003', '沈嘉树', '一般', '男', 'ADM-BCA-QA', 'BIZ-BCA-QA', '质量工程师'),
        ('U-BCA-004', '顾念慈', '一般', '女', 'ADM-BCA-WM', 'BIZ-BCA-WM', '仓库管理员'),
        ('U-BCA-005', '陆承泽', '一般', '男', 'ADM-BCA-EM', 'BIZ-BCA-EM', '设备工程师'),
        ('U-BCA-006', '温可昕', '一般', '女', 'ADM-BCA-PLANT', 'BIZ-BCA-KIT-A', '齐套班组长'),
        ('U-BCA-007', '许观澜', '一般', '男', 'ADM-BCA-PLANT', 'BIZ-BCA-WHEEL-A', '轮组装配工'),
        ('U-BCA-008', '唐雨杭', '一般', '男', 'ADM-BCA-PLANT', 'BIZ-BCA-MAIN-A', '总装班组长'),
        ('U-BCA-009', '林舒窈', '一般', '女', 'ADM-BCA-PLANT', 'BIZ-BCA-MAIN-A', '整车装配工'),
        ('U-BCA-010', '顾星野', '一般', '男', 'ADM-BCA-PLANT', 'BIZ-BCA-TUNE-A', '调校检验员'),
        ('U-BCA-011', '许安歌', '一般', '女', 'ADM-BCA-PLANT', 'BIZ-BCA-PACK-A', '包装操作工'),
    ],
    'work_centers': [
        {'code': 'WC-BCA-KIT', 'name': '来料齐套工作中心', 'biz': 'BIZ-BCA-KIT-SEC', 'wc_type': '产线', 'wc_class': '加工'},
        {'code': 'WC-BCA-WHEEL', 'name': '轮组预装工作中心', 'biz': 'BIZ-BCA-WHEEL-SEC', 'wc_type': '产线', 'wc_class': '加工'},
        {'code': 'WC-BCA-MAIN', 'name': '整车总装工作中心', 'biz': 'BIZ-BCA-MAIN-SEC', 'wc_type': '产线', 'wc_class': '加工'},
        {'code': 'WC-BCA-TUNE', 'name': '调校检测工作中心', 'biz': 'BIZ-BCA-TUNE-SEC', 'wc_type': '产线', 'wc_class': '检验'},
        {'code': 'WC-BCA-PACK', 'name': '包装入库工作中心', 'biz': 'BIZ-BCA-PACK-SEC', 'wc_type': '产线', 'wc_class': '加工'},
    ],
    'equipments': [
        {'code': 'Eq001', 'name': '轮组校圆架', 'model': 'TR-200', 'biz': 'BIZ-BCA-WHEEL-SEC'},
        {'code': 'Eq002', 'name': '扭矩锁附台', 'model': 'TK-320', 'biz': 'BIZ-BCA-MAIN-SEC'},
        {'code': 'Eq003', 'name': '刹车调校台', 'model': 'BR-160', 'biz': 'BIZ-BCA-TUNE-SEC'},
        {'code': 'Eq004', 'name': '滚筒路试台', 'model': 'RT-260', 'biz': 'BIZ-BCA-TUNE-SEC', 'bottle': YES},
        {'code': 'Eq005', 'name': '整车包装台', 'model': 'PK-120', 'biz': 'BIZ-BCA-PACK-SEC'},
    ],
    'wc_user_links': [
        ('WC-BCA-KIT', 'U-BCA-006'),
        ('WC-BCA-WHEEL', 'U-BCA-007'),
        ('WC-BCA-MAIN', 'U-BCA-008'),
        ('WC-BCA-MAIN', 'U-BCA-009'),
        ('WC-BCA-TUNE', 'U-BCA-010'),
        ('WC-BCA-PACK', 'U-BCA-011'),
    ],
    'wc_eq_links': [
        ('WC-BCA-WHEEL', 'Eq001'),
        ('WC-BCA-MAIN', 'Eq002'),
        ('WC-BCA-TUNE', 'Eq003'),
        ('WC-BCA-TUNE', 'Eq004'),
        ('WC-BCA-PACK', 'Eq005'),
    ],
    'warehouses': [
        ('Wh001', '自行车原料库', 'BIZ-BCA-PLANT', 'ERP一级库', '普通库房', '存放车架、轮组、套件和包装物料'),
        ('Wh002', '自行车成品库', 'BIZ-BCA-PLANT', 'ERP二级库', '普通库房', '存放整车成品待发运'),
    ],
    'locations': [
        ('Loc001', '车架存储区', 'BIZ-BCA-PLANT', 'Wh001', '车架与前叉存放位'),
        ('Loc002', '套件存储区', 'BIZ-BCA-PLANT', 'Wh001', '传动制动与附件存放位'),
        ('Loc003', '成品暂存区', 'BIZ-BCA-PLANT', 'Wh002', '整车包装后的待发运库位'),
    ],
    'tools': [
        {'code': 'Tool-BCA-001', 'name': '辐条张力计', 'material_category': CAT_AUX, 'make_type': MAKE_BUY, 'tooling_category': '通用工具', 'feature': FEATURE_IMPORTANT, 'model': 'TG-88', 'spec': '0-2000N', 'life_days': 365},
        {'code': 'Tool-BCA-002', 'name': '碟刹校正夹具', 'material_category': CAT_AUX, 'make_type': MAKE_BUY, 'tooling_category': '专用工装', 'feature': FEATURE_NORMAL, 'model': 'BC-24', 'spec': '160/180兼容', 'life_days': 365},
        {'code': 'Tool-BCA-003', 'name': '脚踏锁附套筒', 'material_category': CAT_AUX, 'make_type': MAKE_BUY, 'tooling_category': '专用工装', 'feature': FEATURE_NORMAL, 'model': 'PD-15', 'spec': '15mm', 'life_times': 8000},
    ],
    'materials': [
        {'code': 'MAT-BCA-FRAME', 'name': '铝合金车架', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_KEY, 'drawing': 'CTB-FRM-101', 'serial': YES},
        {'code': 'MAT-BCA-FORK', 'name': '前叉总成', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'CTB-FRK-102'},
        {'code': 'MAT-BCA-WHEEL-F', 'name': '前轮总成', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_IMPORTANT, 'drawing': 'CTB-WHF-201', 'serial': YES},
        {'code': 'MAT-BCA-WHEEL-R', 'name': '后轮总成', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_IMPORTANT, 'drawing': 'CTB-WHR-202', 'serial': YES},
        {'code': 'MAT-BCA-HUB-F', 'name': '前花鼓', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-HBF-211'},
        {'code': 'MAT-BCA-RIM-F', 'name': '前轮圈', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-RMF-212'},
        {'code': 'MAT-BCA-SPOKE-F', 'name': '前轮辐条组件', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-SPF-213'},
        {'code': 'MAT-BCA-HUB-R', 'name': '后花鼓', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-HBR-214'},
        {'code': 'MAT-BCA-RIM-R', 'name': '后轮圈', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-RMR-215'},
        {'code': 'MAT-BCA-SPOKE-R', 'name': '后轮辐条组件', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-SPR-216'},
        {'code': 'MAT-BCA-TIRE', 'name': '外胎内胎套件', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-TIR-203'},
        {'code': 'MAT-BCA-DRIVE', 'name': '传动套件', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'CTB-DRV-301'},
        {'code': 'MAT-BCA-CRANK', 'name': '牙盘曲柄组件', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'CTB-CRK-311'},
        {'code': 'MAT-BCA-CHAIN', 'name': '链条', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-CHN-312'},
        {'code': 'MAT-BCA-FLYWHEEL', 'name': '飞轮组件', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-FWH-313'},
        {'code': 'MAT-BCA-BRAKE', 'name': '制动套件', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'CTB-BRK-302'},
        {'code': 'MAT-BCA-HANDLE', 'name': '把立车把组件', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'CTB-HDL-303'},
        {'code': 'MAT-BCA-SADDLE', 'name': '坐垫组件', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-SDL-304'},
        {'code': 'MAT-BCA-PEDAL', 'name': '脚踏组件', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-PDL-305'},
        {'code': 'MAT-BCA-ACC', 'name': '随车附件包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-ACC-306'},
        {'code': 'MAT-BCA-LUBE', 'name': '装配润滑脂', 'category': CAT_AUX, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-AUX-401', 'unit': '个', 'batch': YES},
        {'code': 'MAT-BCA-LABEL', 'name': '整车条码标签', 'category': CAT_AUX, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-AUX-402', 'unit': '个', 'batch': YES},
        {'code': 'MAT-BCA-PKG', 'name': '整车包装套件', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'CTB-PKG-501'},
        {'code': 'MAT-BCA-BIKE-FIN', 'name': 'CTB-26S城市通勤自行车整车', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': 'CTB-ASM-999', 'serial': YES},
    ],
    'mboms': [
        {
            'code': 'MBOM-BCA-ASM-A01',
            'material_code': 'MAT-BCA-BIKE-FIN',
            'name': 'CTB-26S城市通勤自行车整车MBOM',
            'nodes': [
                {'level': 0, 'material_code': 'MAT-BCA-BIKE-FIN', 'qty': 1},
                {'level': 1, 'material_code': 'MAT-BCA-FRAME', 'qty': 1, 'parent_material': 'MAT-BCA-BIKE-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-BCA-FORK', 'qty': 1, 'parent_material': 'MAT-BCA-BIKE-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-BCA-WHEEL-F', 'qty': 1, 'parent_material': 'MAT-BCA-BIKE-FIN', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'MAT-BCA-HUB-F', 'qty': 1, 'parent_material': 'MAT-BCA-WHEEL-F', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'MAT-BCA-RIM-F', 'qty': 1, 'parent_material': 'MAT-BCA-WHEEL-F', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'MAT-BCA-SPOKE-F', 'qty': 1, 'parent_material': 'MAT-BCA-WHEEL-F', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-BCA-WHEEL-R', 'qty': 1, 'parent_material': 'MAT-BCA-BIKE-FIN', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'MAT-BCA-HUB-R', 'qty': 1, 'parent_material': 'MAT-BCA-WHEEL-R', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'MAT-BCA-RIM-R', 'qty': 1, 'parent_material': 'MAT-BCA-WHEEL-R', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'MAT-BCA-SPOKE-R', 'qty': 1, 'parent_material': 'MAT-BCA-WHEEL-R', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-BCA-TIRE', 'qty': 1, 'parent_material': 'MAT-BCA-BIKE-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-BCA-DRIVE', 'qty': 1, 'parent_material': 'MAT-BCA-BIKE-FIN', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'MAT-BCA-CRANK', 'qty': 1, 'parent_material': 'MAT-BCA-DRIVE', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'MAT-BCA-CHAIN', 'qty': 1, 'parent_material': 'MAT-BCA-DRIVE', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'MAT-BCA-FLYWHEEL', 'qty': 1, 'parent_material': 'MAT-BCA-DRIVE', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-BCA-BRAKE', 'qty': 1, 'parent_material': 'MAT-BCA-BIKE-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-BCA-HANDLE', 'qty': 1, 'parent_material': 'MAT-BCA-BIKE-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-BCA-SADDLE', 'qty': 1, 'parent_material': 'MAT-BCA-BIKE-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-BCA-PEDAL', 'qty': 1, 'parent_material': 'MAT-BCA-BIKE-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-BCA-ACC', 'qty': 1, 'parent_material': 'MAT-BCA-BIKE-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-BCA-PKG', 'qty': 1, 'parent_material': 'MAT-BCA-BIKE-FIN', 'parent_version': 'A.01'},
            ],
        },
    ],
    'routes': [
        {
            'code': 'RT-BCA-ASM-A01',
            'name': '城市通勤自行车总装工艺',
            'route_spec': '装配',
            'biz': 'BIZ-BCA-ASM-WS',
            'material_code': 'MAT-BCA-BIKE-FIN',
            'proc_spec': '装配专业',
            'remark': '单工厂自行车装配路线，不含外委和跨厂转工',
            'ops': [
                {'no': '0010', 'name': '来料核对与车架齐套', 'type': '加工', 'wc': 'WC-BCA-KIT', 'prep': 8, 'run': 12, 'out': 'MAT-BCA-BIKE-FIN', 'content': '核对车架、前叉、轮组和套件批次，完成上线齐套', 'materials': [('MAT-BCA-FRAME', 1), ('MAT-BCA-FORK', 1), ('MAT-BCA-DRIVE', 1), ('MAT-BCA-BRAKE', 1), ('MAT-BCA-HANDLE', 1), ('MAT-BCA-SADDLE', 1), ('MAT-BCA-PEDAL', 1)], 'steps': [('核对关键组件', '核对车架、前叉、传动和制动套件批次'), ('完成上线齐套', '按工单完成物料扫码和齐套确认')]},
                {'no': '0020', 'name': '轮组预装与校圆', 'type': '加工', 'wc': 'WC-BCA-WHEEL', 'prep': 10, 'run': 18, 'out': 'MAT-BCA-BIKE-FIN', 'content': '完成轮胎装配、轮组校圆和平衡确认', 'materials': [('MAT-BCA-WHEEL-F', 1), ('MAT-BCA-WHEEL-R', 1), ('MAT-BCA-TIRE', 1)], 'steps': [('安装轮胎套件', '完成前后轮胎和内胎装配'), ('执行轮组校圆', '完成轮组跳动调整并确认张力')]},
                {'no': '0030', 'name': '传动制动与车把安装', 'type': '加工', 'wc': 'WC-BCA-MAIN', 'prep': 12, 'run': 24, 'out': 'MAT-BCA-BIKE-FIN', 'content': '完成前叉、车把、传动和制动系统装配', 'materials': [('MAT-BCA-FORK', 1), ('MAT-BCA-DRIVE', 1), ('MAT-BCA-BRAKE', 1), ('MAT-BCA-HANDLE', 1), ('MAT-BCA-LUBE', 1)], 'steps': [('安装前叉和车把', '完成头管装配并锁附把立车把组件'), ('装配传动制动系统', '完成变速器、链条和制动系统安装')]},
                {'no': '0040', 'name': '整车总装与扭矩调校', 'type': '加工', 'wc': 'WC-BCA-MAIN', 'prep': 10, 'run': 20, 'out': 'MAT-BCA-BIKE-FIN', 'content': '完成坐垫、脚踏、附件安装和整车扭矩调校', 'materials': [('MAT-BCA-SADDLE', 1), ('MAT-BCA-PEDAL', 1), ('MAT-BCA-ACC', 1), ('MAT-BCA-LABEL', 1)], 'steps': [('安装坐垫脚踏', '完成座管、坐垫和脚踏安装'), ('执行扭矩复核', '按标准复核关键紧固点扭矩并粘贴标签')]},
                {'no': '0050', 'name': '路试检测与包装转序', 'type': '检验', 'wc': 'WC-BCA-TUNE', 'prep': 12, 'run': 18, 'out': 'MAT-BCA-BIKE-FIN', 'content': '完成制动变速调校、滚筒路试和放行确认', 'materials': [('MAT-BCA-PKG', 1)], 'steps': [('执行路试检测', '完成滚筒路试并确认制动与变速性能'), ('放行并转包装', '确认整车状态后流转至包装工位')]},
                {'no': '0060', 'name': '整车包装入库', 'type': '加工', 'wc': 'WC-BCA-PACK', 'prep': 8, 'run': 14, 'out': 'MAT-BCA-BIKE-FIN', 'content': '完成整车折叠保护、装箱和成品入库', 'materials': [('MAT-BCA-PKG', 1), ('MAT-BCA-ACC', 1)], 'steps': [('执行整车保护', '安装防护件并完成装箱固定'), ('成品入库', '打印装箱信息并转入成品库位')]},
            ],
        },
    ],
}


def renumber_user_codes_numeric(seed: dict, start: int = 100) -> dict:
    users = seed.get('workbooks', {}).get('系统配置_模板.xlsx', {}).get('用户', [])
    if not users:
        return seed

    user_map: dict[str, str] = {}
    for offset, row in enumerate(users):
        old_code = str(row.get('*编号', '')).strip()
        if not old_code:
            continue
        user_map[old_code] = str(start + offset)

    for row in users:
        old_code = str(row.get('*编号', '')).strip()
        if old_code in user_map:
            row['*编号'] = user_map[old_code]

    ref_fields = {'*编号', '*用户', '计划员', '发布人'}
    for workbook in seed.get('workbooks', {}).values():
        for rows in workbook.values():
            for row in rows:
                for field in ref_fields:
                    value = str(row.get(field, '')).strip()
                    if value in user_map:
                        row[field] = user_map[value]
    return seed


def build_variant(namespace: str = NAMESPACE, volume_profile: str = VOLUME_PROFILE) -> dict:
    metadata = deepcopy(CONFIG['metadata'])
    metadata['default_version'] = 'A.01'
    metadata['default_security'] = '内部'
    metadata['volume_profile'] = volume_profile

    builder = SeedBuilder(metadata)
    builder.build_from_config(CONFIG)
    seed = builder.seed

    seed.setdefault('metadata', {})['namespace'] = namespace
    seed['external_references'] = ['0']
    renumber_user_codes_numeric(seed)
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

