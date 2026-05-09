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

SCENARIO = 'fuel_pump_assembly'
NAMESPACE = 'FPA20S01'
VOLUME_PROFILE = '标准版'
ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'fuel_pump_assembly_seed.json'

CONFIG = {
    'metadata': {
        'name': '燃油泵单工厂装配MOM种子',
        'industry': '汽车零部件',
        'product_family': '燃油供给系统',
        'product_model': 'FP220电动燃油泵总成',
        'description': '面向单工厂装配场景构建的燃油泵标准版主数据，覆盖来料核对、泵芯预装、总装锁紧、流量检测和包装入库。',
    },
    'admins': [
        ('0', '公司', 'ADM-FPA-HQ', '启航汽车零部件有限公司', '启航部件'),
        ('ADM-FPA-HQ', '部门', 'ADM-FPA-TECH', '工艺技术部', '工艺技术'),
        ('ADM-FPA-HQ', '部门', 'ADM-FPA-PMC', '生产运营部', '生产运营'),
        ('ADM-FPA-HQ', '部门', 'ADM-FPA-QA', '质量管理部', '质量管理'),
        ('ADM-FPA-HQ', '部门', 'ADM-FPA-WM', '仓储物流部', '仓储物流'),
        ('ADM-FPA-HQ', '部门', 'ADM-FPA-EM', '设备工装部', '设备工装'),
        ('ADM-FPA-HQ', '工厂', 'ADM-FPA-PLANT', '燃油泵装配工厂', '燃油泵工厂', '负责燃油泵装配、检测和包装入库'),
    ],
    'bizs': [
        ('0', 'BIZ-FPA-COMPANY', '启航汽车零部件有限公司', '启航部件', '公司', 'ADM-FPA-HQ', '', '单工厂燃油泵装配场景'),
        ('BIZ-FPA-COMPANY', 'BIZ-FPA-TECH', '工艺技术部', '工艺技术', '部门', 'ADM-FPA-TECH'),
        ('BIZ-FPA-COMPANY', 'BIZ-FPA-PMC', '生产运营部', '生产运营', '部门', 'ADM-FPA-PMC'),
        ('BIZ-FPA-COMPANY', 'BIZ-FPA-QA', '质量管理部', '质量管理', '部门', 'ADM-FPA-QA'),
        ('BIZ-FPA-COMPANY', 'BIZ-FPA-WM', '仓储物流部', '仓储物流', '部门', 'ADM-FPA-WM'),
        ('BIZ-FPA-COMPANY', 'BIZ-FPA-EM', '设备工装部', '设备工装', '部门', 'ADM-FPA-EM'),
        ('BIZ-FPA-COMPANY', 'BIZ-FPA-PLANT', '燃油泵装配工厂', '燃油泵工厂', '工厂', 'ADM-FPA-PLANT', '装配专业', '简单装配工厂，不含外委工序'),
        ('BIZ-FPA-PLANT', 'BIZ-FPA-ASM-WS', '装配车间', '装配车间', '车间', 'ADM-FPA-PLANT'),
        ('BIZ-FPA-ASM-WS', 'BIZ-FPA-PREASM-SEC', '预装工段', '预装工段', '工段', 'ADM-FPA-PLANT'),
        ('BIZ-FPA-ASM-WS', 'BIZ-FPA-MAINASM-SEC', '总装工段', '总装工段', '工段', 'ADM-FPA-PLANT'),
        ('BIZ-FPA-ASM-WS', 'BIZ-FPA-TEST-SEC', '检测工段', '检测工段', '工段', 'ADM-FPA-PLANT'),
        ('BIZ-FPA-ASM-WS', 'BIZ-FPA-PACK-SEC', '包装工段', '包装工段', '工段', 'ADM-FPA-PLANT'),
        ('BIZ-FPA-PREASM-SEC', 'BIZ-FPA-PREASM-A', '预装甲班', '预装甲班', '班组', 'ADM-FPA-PLANT'),
        ('BIZ-FPA-MAINASM-SEC', 'BIZ-FPA-MAINASM-A', '总装甲班', '总装甲班', '班组', 'ADM-FPA-PLANT'),
        ('BIZ-FPA-TEST-SEC', 'BIZ-FPA-TEST-A', '检测甲班', '检测甲班', '班组', 'ADM-FPA-PLANT'),
        ('BIZ-FPA-PACK-SEC', 'BIZ-FPA-PACK-A', '包装甲班', '包装甲班', '班组', 'ADM-FPA-PLANT'),
    ],
    'users': [
        ('U-FPA-001', '林景明', '重要', '男', 'ADM-FPA-TECH', 'BIZ-FPA-TECH', '工艺工程师'),
        ('U-FPA-002', '周清妍', '重要', '女', 'ADM-FPA-PMC', 'BIZ-FPA-PMC', '主计划员'),
        ('U-FPA-003', '吴嘉宁', '一般', '男', 'ADM-FPA-QA', 'BIZ-FPA-QA', '质量工程师'),
        ('U-FPA-004', '郑语桐', '一般', '女', 'ADM-FPA-WM', 'BIZ-FPA-WM', '仓库管理员'),
        ('U-FPA-005', '许承宇', '一般', '男', 'ADM-FPA-EM', 'BIZ-FPA-EM', '设备工程师'),
        ('U-FPA-006', '冯可欣', '一般', '女', 'ADM-FPA-PLANT', 'BIZ-FPA-PREASM-A', '预装班组长'),
        ('U-FPA-007', '邓书恒', '一般', '男', 'ADM-FPA-PLANT', 'BIZ-FPA-PREASM-A', '装配操作工'),
        ('U-FPA-008', '宋安宁', '一般', '女', 'ADM-FPA-PLANT', 'BIZ-FPA-MAINASM-A', '总装班组长'),
        ('U-FPA-009', '韩景程', '一般', '男', 'ADM-FPA-PLANT', 'BIZ-FPA-MAINASM-A', '装配操作工'),
        ('U-FPA-010', '唐晨悦', '一般', '女', 'ADM-FPA-PLANT', 'BIZ-FPA-TEST-A', '检测员'),
        ('U-FPA-011', '谢书远', '一般', '男', 'ADM-FPA-PLANT', 'BIZ-FPA-PACK-A', '包装操作工'),
    ],
    'suppliers': [],
    'work_centers': [
        {'code': 'WC-FPA-KIT', 'name': '来料齐套工位', 'biz': 'BIZ-FPA-PREASM-SEC', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责燃油泵组件来料核对'},
        {'code': 'WC-FPA-PREASM', 'name': '泵芯预装工位', 'biz': 'BIZ-FPA-PREASM-SEC', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责泵芯和电机组件预装'},
        {'code': 'WC-FPA-MAINASM', 'name': '总装工位', 'biz': 'BIZ-FPA-MAINASM-SEC', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责壳体、线束和锁紧装配'},
        {'code': 'WC-FPA-TEST', 'name': '流量检测工位', 'biz': 'BIZ-FPA-TEST-SEC', 'wc_type': '组织', 'wc_class': '检验', 'remark': '负责流量和密封状态检测'},
        {'code': 'WC-FPA-PACK', 'name': '包装入库工位', 'biz': 'BIZ-FPA-PACK-SEC', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责包装、贴标和入库'},
    ],
    'equipments': [
        {'code': 'EQ-FPA-SCAN-01', 'name': '条码扫描工作站', 'model': 'SCAN-10', 'biz': 'BIZ-FPA-PREASM-SEC', 'bottle': NO},
        {'code': 'EQ-FPA-PRESS-01', 'name': '泵芯压装机', 'model': 'PR-120', 'biz': 'BIZ-FPA-PREASM-SEC', 'bottle': NO},
        {'code': 'EQ-FPA-TORQUE-01', 'name': '数显扭矩枪', 'model': 'TQ-60', 'biz': 'BIZ-FPA-MAINASM-SEC', 'bottle': YES},
        {'code': 'EQ-FPA-FLOW-01', 'name': '燃油泵流量检测台', 'model': 'FL-220', 'biz': 'BIZ-FPA-TEST-SEC', 'bottle': YES},
        {'code': 'EQ-FPA-LABEL-01', 'name': '贴标工作站', 'model': 'LB-20', 'biz': 'BIZ-FPA-PACK-SEC', 'bottle': NO},
    ],
    'tools': [
        {'code': 'TOOL-FPA-LOC-01', 'name': '泵壳定位工装', 'material_category': CAT_KIT, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_KEY, 'model': 'JG-FP-01', 'spec': '泵壳定位', 'remark': '控制泵壳装配定位', 'life_times': 60000, 'life_days': 365},
        {'code': 'TOOL-FPA-PRESS-01', 'name': '泵芯压装工装', 'material_category': CAT_KIT, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_IMPORTANT, 'model': 'JG-FP-02', 'spec': '泵芯压装', 'remark': '控制泵芯压装深度', 'life_times': 50000, 'life_days': 365},
        {'code': 'TOOL-FPA-TORQUE-01', 'name': '扭矩扳手', 'material_category': CAT_PART, 'make_type': MAKE_BUY, 'tooling_category': '通用工具', 'feature': FEATURE_KEY, 'model': 'TW-50', 'spec': '5-50Nm', 'remark': '采集装配锁紧扭矩', 'life_times': 30000, 'life_days': 180},
    ],
    'wc_user_links': [
        ('WC-FPA-KIT', 'U-FPA-004'), ('WC-FPA-KIT', 'U-FPA-006'),
        ('WC-FPA-PREASM', 'U-FPA-001'), ('WC-FPA-PREASM', 'U-FPA-006'), ('WC-FPA-PREASM', 'U-FPA-007'),
        ('WC-FPA-MAINASM', 'U-FPA-008'), ('WC-FPA-MAINASM', 'U-FPA-009'),
        ('WC-FPA-TEST', 'U-FPA-003'), ('WC-FPA-TEST', 'U-FPA-010'),
        ('WC-FPA-PACK', 'U-FPA-011'),
    ],
    'wc_eq_links': [
        ('WC-FPA-KIT', 'EQ-FPA-SCAN-01'), ('WC-FPA-PREASM', 'EQ-FPA-PRESS-01'),
        ('WC-FPA-MAINASM', 'EQ-FPA-TORQUE-01'), ('WC-FPA-TEST', 'EQ-FPA-FLOW-01'), ('WC-FPA-PACK', 'EQ-FPA-LABEL-01'),
    ],
    'eq_user_links': [
        ('EQ-FPA-PRESS-01', 'U-FPA-007'), ('EQ-FPA-TORQUE-01', 'U-FPA-009'), ('EQ-FPA-FLOW-01', 'U-FPA-010'),
    ],
    'warehouses': [
        ('WH-FPA-KIT', '组件库', 'BIZ-FPA-WM', 'ERP一级库', '普通库房', '存放电机、泵芯、壳体和辅料'),
        ('WH-FPA-WIP', '在制品库', 'BIZ-FPA-WM', '车间二级库', '普通库房', '存放待检和待包装燃油泵'),
        ('WH-FPA-FG', '成品库', 'BIZ-FPA-WM', 'ERP二级库', '普通库房', '存放已放行燃油泵总成'),
    ],
    'locations': [
        ('LOC-FPA-KIT-01', '电机组件区', 'BIZ-FPA-WM', 'WH-FPA-KIT'), ('LOC-FPA-KIT-02', '壳体辅料区', 'BIZ-FPA-WM', 'WH-FPA-KIT'),
        ('LOC-FPA-WIP-01', '待检区', 'BIZ-FPA-WM', 'WH-FPA-WIP'), ('LOC-FPA-FG-01', '成品待发区', 'BIZ-FPA-WM', 'WH-FPA-FG'),
    ],
    'materials': [
        {'code': 'MAT-FPA-MOTOR', 'name': '电机组件', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'FP220-MTR-101'},
        {'code': 'MAT-FPA-CORE', 'name': '泵芯组件', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_KEY, 'drawing': 'FP220-COR-102'},
        {'code': 'MAT-FPA-HOUSING', 'name': '泵壳组件', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'FP220-HSG-103'},
        {'code': 'MAT-FPA-SEAL', 'name': '密封件包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'FP220-SEA-104'},
        {'code': 'MAT-FPA-WIRE', 'name': '线束组件', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'FP220-WIR-105'},
        {'code': 'MAT-FPA-FIX', 'name': '紧固件包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'FP220-FIX-106'},
        {'code': 'MAT-FPA-TEST-MEDIA', 'name': '检测介质包', 'category': CAT_AUX, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'FP220-TST-107'},
        {'code': 'MAT-FPA-PKG', 'name': '包装辅料包', 'category': CAT_KIT, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'FP220-PKG-108'},
        {'code': 'MAT-FPA-PUMP-FIN', 'name': 'FP220燃油泵总成', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': 'FP220-ASM-999', 'serial': YES},
    ],
    'mboms': [
        {
            'code': 'MBOM-FPA-ASM-A01',
            'material_code': 'MAT-FPA-PUMP-FIN',
            'name': 'FP220燃油泵总成MBOM',
            'nodes': [
                {'level': 0, 'material_code': 'MAT-FPA-PUMP-FIN', 'qty': 1},
                {'level': 1, 'material_code': 'MAT-FPA-MOTOR', 'qty': 1, 'parent_material': 'MAT-FPA-PUMP-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-FPA-CORE', 'qty': 1, 'parent_material': 'MAT-FPA-PUMP-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-FPA-HOUSING', 'qty': 1, 'parent_material': 'MAT-FPA-PUMP-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-FPA-SEAL', 'qty': 1, 'parent_material': 'MAT-FPA-PUMP-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-FPA-WIRE', 'qty': 1, 'parent_material': 'MAT-FPA-PUMP-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-FPA-FIX', 'qty': 1, 'parent_material': 'MAT-FPA-PUMP-FIN', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'MAT-FPA-PKG', 'qty': 1, 'parent_material': 'MAT-FPA-PUMP-FIN', 'parent_version': 'A.01'},
            ],
        },
    ],
    'routes': [
        {
            'code': 'RT-FPA-ASM-A01',
            'name': '燃油泵装配工艺',
            'route_spec': '装配',
            'biz': 'BIZ-FPA-ASM-WS',
            'material_code': 'MAT-FPA-PUMP-FIN',
            'proc_spec': '装配专业',
            'remark': '简单装配路线，不含外委和跨厂转工',
            'ops': [
                {'no': '0010', 'name': '来料核对与组件齐套', 'type': '加工', 'wc': 'WC-FPA-KIT', 'prep': 8, 'run': 12, 'out': 'MAT-FPA-PUMP-FIN', 'content': '核对电机、泵芯、泵壳和辅料批次后齐套上线', 'materials': [('MAT-FPA-MOTOR', 1), ('MAT-FPA-CORE', 1), ('MAT-FPA-HOUSING', 1), ('MAT-FPA-SEAL', 1), ('MAT-FPA-WIRE', 1), ('MAT-FPA-FIX', 1)], 'steps': [('核对物料批次', '核对主要组件批次和状态'), ('执行齐套扫描', '完成来料条码扫描和齐套确认')]},
                {'no': '0020', 'name': '泵芯与电机预装', 'type': '加工', 'wc': 'WC-FPA-PREASM', 'prep': 10, 'run': 16, 'out': 'MAT-FPA-PUMP-FIN', 'content': '完成泵芯与电机组件压装预装', 'materials': [('MAT-FPA-MOTOR', 1), ('MAT-FPA-CORE', 1)], 'steps': [('执行压装', '完成泵芯与电机预装压装'), ('复核压装状态', '复核压装深度和旋转状态')]},
                {'no': '0030', 'name': '总装锁紧与线束安装', 'type': '加工', 'wc': 'WC-FPA-MAINASM', 'prep': 10, 'run': 18, 'out': 'MAT-FPA-PUMP-FIN', 'content': '完成泵壳装配、线束连接和锁紧', 'materials': [('MAT-FPA-HOUSING', 1), ('MAT-FPA-WIRE', 1), ('MAT-FPA-FIX', 1)], 'steps': [('装入泵壳', '完成泵芯组件装入泵壳'), ('锁紧并连接线束', '完成锁紧和线束连接')]},
                {'no': '0040', 'name': '流量检测与包装入库', 'type': '检验', 'wc': 'WC-FPA-TEST', 'prep': 10, 'run': 18, 'out': 'MAT-FPA-PUMP-FIN', 'content': '完成燃油泵流量检测、放行确认和包装入库', 'materials': [('MAT-FPA-TEST-MEDIA', 1), ('MAT-FPA-PKG', 1)], 'steps': [('执行流量检测', '检测燃油泵流量和电流参数'), ('确认放行并包装', '确认放行状态后完成包装入库')]},
            ],
        },
    ],
}


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

