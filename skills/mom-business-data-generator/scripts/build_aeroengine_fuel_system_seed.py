from __future__ import annotations

import json
import sys
from collections import Counter
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
    YES,
    SeedBuilder,
    summarize_seed,
)
from production_order_seed import apply_production_orders
from scene_seed_upgrades import (
    apply_namespace,
    apply_project_collaboration,
    clear_tool_strategy_relations,
    filter_wc_supplier_relations,
    normalize_poc_security,
    normalize_release_user,
    normalize_sequence_relations,
    normalize_storage_factory_org,
    normalize_user_codes,
    rebuild_route_sequences,
    remove_transfer_operations,
)

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

SCENARIO = 'aeroengine_fuel_system_multi_factory'
NAMESPACE = 'AFS20S01'
VOLUME_PROFILE = '标准版'
ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'aeroengine_fuel_system_seed.json'

BASE_CONFIG = {
    'metadata': {
        'name': '航发燃油系统总成多工厂协同MOM种子',
        'industry': '航空发动机',
        'product_family': '燃油系统',
        'product_model': 'AFS-900航发燃油系统总成',
        'description': '面向铸造、机加工、热处理、装配、试车多工厂协同的航发燃油系统总成示例数据，包含生产部主导的一级工艺、一级生产订单，以及完整的车间/工段/班组组织。',
        'project_collaboration': {
            'enabled': True,
            'admin': {
                'parent': 'Adm001',
                'code': 'Adm031',
                'name': '生产部',
                'short': '生产部',
            },
            'biz': {
                'parent': 'Biz001',
                'code': 'Biz031',
                'name': '生产部',
                'short': '生产部',
                'factory_type': '装配专业',
                'remark': '用于航发燃油系统总成跨工厂协同排产和一级生产订单承载。',
            },
            'route': {
                'code': 'Rt901',
                'name': '航发燃油系统一级协同工艺',
                'material_code': 'Mat015',
                'spec': '通用',
                'remark': '生产部统筹铸造、机加、热处理、装配和试车交付节奏。',
            },
            'phases': [
                {
                    'no': '0010',
                    'name': '铸造阶段完成',
                    'wc_code': 'Wc901',
                    'wc_name': '铸造协同排产中心',
                    'content': '生产部按铸造工厂产能组织燃油系统壳体铸件协同排产。',
                    'op_spec': '机械加工专业',
                    'output_code': 'Mat002',
                },
                {
                    'no': '0020',
                    'name': '机加工阶段完成',
                    'wc_code': 'Wc902',
                    'wc_name': '机加协同排产中心',
                    'content': '生产部按机加工工厂产能组织壳体精加工协同排产。',
                    'op_spec': '机械加工专业',
                    'output_code': 'Mat004',
                },
                {
                    'no': '0030',
                    'name': '热处理阶段完成',
                    'wc_code': 'Wc903',
                    'wc_name': '热处理协同排产中心',
                    'content': '生产部按热处理工厂产能组织固溶时效与表面强化协同排产。',
                    'op_spec': '机械加工专业',
                    'output_code': 'Mat005',
                },
                {
                    'no': '0040',
                    'name': '总装阶段完成',
                    'wc_code': 'Wc904',
                    'wc_name': '总装协同排产中心',
                    'content': '生产部统筹燃油系统总装齐套、装配和静压检漏节奏。',
                    'op_spec': '装配专业',
                    'output_code': 'Mat014',
                },
                {
                    'no': '0050',
                    'name': '试车交付完成',
                    'wc_code': 'Wc905',
                    'wc_name': '试车交付协同中心',
                    'content': '生产部统筹冷试、热态试车、放行包装和交付。',
                    'op_type': '检验',
                    'wc_class': '检验',
                    'op_spec': '装配专业',
                    'output_code': 'Mat015',
                },
            ],
        },
    },
    'admins': [
        ('0', '公司', 'Adm001', '启航航发燃油系统有限公司', '启航航发'),
        ('Adm001', '部门', 'Adm002', '工艺技术中心', '工艺技术'),
        ('Adm001', '部门', 'Adm003', '生产运营中心', '生产运营'),
        ('Adm001', '部门', 'Adm004', '质量管理中心', '质量管理'),
        ('Adm001', '部门', 'Adm005', '物流仓储中心', '物流仓储'),
        ('Adm001', '部门', 'Adm006', '设备工装中心', '设备工装'),
        ('Adm001', '工厂', 'Adm007', '壳体铸造工厂', '铸造工厂'),
        ('Adm001', '工厂', 'Adm008', '精密机加工工厂', '机加工厂'),
        ('Adm001', '工厂', 'Adm009', '热处理表面工厂', '热处理厂'),
        ('Adm001', '工厂', 'Adm010', '燃油系统装配工厂', '装配工厂'),
        ('Adm001', '工厂', 'Adm011', '试车验证工厂', '试车工厂'),
    ],
    'bizs': [
        ('0', 'Biz001', '启航航发燃油系统有限公司', '启航航发', '公司', 'Adm001', '', '航发燃油系统总成多工厂协同场景'),
        ('Biz001', 'Biz002', '工艺技术中心', '工艺技术', '部门', 'Adm002'),
        ('Biz001', 'Biz003', '生产运营中心', '生产运营', '部门', 'Adm003'),
        ('Biz001', 'Biz004', '质量管理中心', '质量管理', '部门', 'Adm004'),
        ('Biz001', 'Biz005', '物流仓储中心', '物流仓储', '部门', 'Adm005'),
        ('Biz001', 'Biz006', '设备工装中心', '设备工装', '部门', 'Adm006'),
        ('Biz001', 'Biz007', '壳体铸造工厂', '铸造工厂', '工厂', 'Adm007', '机械加工专业', '负责壳体精密铸造、清理和无损检测'),
        ('Biz001', 'Biz008', '精密机加工工厂', '机加工厂', '工厂', 'Adm008', '机械加工专业', '负责壳体粗精加工、清洗和尺寸放行'),
        ('Biz001', 'Biz009', '热处理表面工厂', '热处理厂', '工厂', 'Adm009', '机械加工专业', '负责固溶时效、表面强化和热后终检'),
        ('Biz001', 'Biz010', '燃油系统装配工厂', '装配工厂', '工厂', 'Adm010', '装配专业', '负责齐套上线、阀组装配、总装和静压检漏'),
        ('Biz001', 'Biz011', '试车验证工厂', '试车工厂', '工厂', 'Adm011', '装配专业', '负责冷试、热态试车、交付放行和包装入库'),
        ('Biz007', 'Biz101', '铸造车间', '铸造车间', '车间', 'Adm007'),
        ('Biz008', 'Biz102', '机加车间', '机加车间', '车间', 'Adm008'),
        ('Biz009', 'Biz103', '热处理车间', '热处理车间', '车间', 'Adm009'),
        ('Biz010', 'Biz104', '装配车间', '装配车间', '车间', 'Adm010'),
        ('Biz011', 'Biz105', '试车车间', '试车车间', '车间', 'Adm011'),
        ('Biz101', 'Biz111', '精铸工段', '精铸工段', '工段', 'Adm007'),
        ('Biz101', 'Biz112', '铸件检验工段', '检验工段', '工段', 'Adm007'),
        ('Biz102', 'Biz113', '粗加工工段', '粗加工工段', '工段', 'Adm008'),
        ('Biz102', 'Biz114', '精加工工段', '精加工工段', '工段', 'Adm008'),
        ('Biz103', 'Biz115', '热处理工段', '热处理工段', '工段', 'Adm009'),
        ('Biz103', 'Biz116', '热后检验工段', '热后检验', '工段', 'Adm009'),
        ('Biz104', 'Biz117', '齐套预装工段', '预装工段', '工段', 'Adm010'),
        ('Biz104', 'Biz118', '总装检漏工段', '总装工段', '工段', 'Adm010'),
        ('Biz105', 'Biz119', '冷试工段', '冷试工段', '工段', 'Adm011'),
        ('Biz105', 'Biz120', '热试包装工段', '热试包装', '工段', 'Adm011'),
        ('Biz111', 'Biz121', '精铸甲班', '精铸甲班', '班组', 'Adm007'),
        ('Biz112', 'Biz122', '检验甲班', '检验甲班', '班组', 'Adm007'),
        ('Biz113', 'Biz123', '粗加工甲班', '粗加工甲班', '班组', 'Adm008'),
        ('Biz114', 'Biz124', '精加工甲班', '精加工甲班', '班组', 'Adm008'),
        ('Biz115', 'Biz125', '热处理甲班', '热处理甲班', '班组', 'Adm009'),
        ('Biz116', 'Biz126', '热后检验甲班', '热检甲班', '班组', 'Adm009'),
        ('Biz117', 'Biz127', '预装甲班', '预装甲班', '班组', 'Adm010'),
        ('Biz118', 'Biz128', '总装甲班', '总装甲班', '班组', 'Adm010'),
        ('Biz119', 'Biz129', '冷试甲班', '冷试甲班', '班组', 'Adm011'),
        ('Biz120', 'Biz130', '热试包装甲班', '热试甲班', '班组', 'Adm011'),
    ],
    'users': [
        ('U-AFS-001', '顾知远', '核心', '男', 'Adm002', 'Biz002', '工艺平台主管'),
        ('U-AFS-002', '沈若岚', '重要', '女', 'Adm003', 'Biz003', '主计划员'),
        ('U-AFS-003', '韩承岳', '重要', '男', 'Adm004', 'Biz004', '质量工程师'),
        ('U-AFS-004', '苏清禾', '一般', '女', 'Adm005', 'Biz005', '仓库管理员'),
        ('U-AFS-005', '梁叙白', '一般', '男', 'Adm006', 'Biz006', '设备工程师'),
        ('U-AFS-006', '周行简', '一般', '男', 'Adm007', 'Biz121', '精铸班组长'),
        ('U-AFS-007', '白宁川', '一般', '男', 'Adm007', 'Biz122', '无损检测员'),
        ('U-AFS-008', '宋闻溪', '一般', '女', 'Adm008', 'Biz123', '粗加工班组长'),
        ('U-AFS-009', '林嘉树', '重要', '男', 'Adm008', 'Biz124', '精加工艺员'),
        ('U-AFS-010', '叶清和', '一般', '男', 'Adm009', 'Biz125', '热处理班组长'),
        ('U-AFS-011', '唐予安', '重要', '女', 'Adm009', 'Biz126', '热后检验员'),
        ('U-AFS-012', '程时叙', '一般', '男', 'Adm010', 'Biz127', '预装班组长'),
        ('U-AFS-013', '许南乔', '一般', '女', 'Adm010', 'Biz128', '总装操作工'),
        ('U-AFS-014', '陆星衍', '重要', '男', 'Adm011', 'Biz129', '试车工程师'),
        ('U-AFS-015', '顾知夏', '重要', '女', 'Adm011', 'Biz130', '试车放行员'),
    ],
    'suppliers': [],
    'work_centers': [
        {'code': 'Wc001', 'name': '壳体浇注中心', 'biz': 'Biz111', 'wc_type': '设备组', 'wc_class': '加工', 'remark': '完成壳体制壳、熔炼和浇注'},
        {'code': 'Wc002', 'name': '铸件清理检验中心', 'biz': 'Biz112', 'wc_type': '设备组', 'wc_class': '检验', 'remark': '完成切割清理、补焊和无损检测'},
        {'code': 'Wc003', 'name': '壳体粗加工中心', 'biz': 'Biz113', 'wc_type': '设备组', 'wc_class': '加工'},
        {'code': 'Wc004', 'name': '壳体精加工中心', 'biz': 'Biz114', 'wc_type': '设备组', 'wc_class': '加工'},
        {'code': 'Wc005', 'name': '机加清洗检验中心', 'biz': 'Biz114', 'wc_type': '设备组', 'wc_class': '检验'},
        {'code': 'Wc006', 'name': '固溶时效中心', 'biz': 'Biz115', 'wc_type': '设备组', 'wc_class': '加工'},
        {'code': 'Wc007', 'name': '表面强化中心', 'biz': 'Biz115', 'wc_type': '设备组', 'wc_class': '加工'},
        {'code': 'Wc008', 'name': '热后终检中心', 'biz': 'Biz116', 'wc_type': '设备组', 'wc_class': '检验'},
        {'code': 'Wc009', 'name': '装配齐套中心', 'biz': 'Biz117', 'wc_type': '设备组', 'wc_class': '加工'},
        {'code': 'Wc010', 'name': '阀组装配中心', 'biz': 'Biz117', 'wc_type': '设备组', 'wc_class': '加工'},
        {'code': 'Wc011', 'name': '总装锁紧中心', 'biz': 'Biz118', 'wc_type': '设备组', 'wc_class': '加工'},
        {'code': 'Wc012', 'name': '静压检漏中心', 'biz': 'Biz118', 'wc_type': '设备组', 'wc_class': '检验'},
        {'code': 'Wc013', 'name': '冷试校验中心', 'biz': 'Biz119', 'wc_type': '设备组', 'wc_class': '检验'},
        {'code': 'Wc014', 'name': '热态试车中心', 'biz': 'Biz120', 'wc_type': '设备组', 'wc_class': '检验'},
        {'code': 'Wc015', 'name': '交付包装中心', 'biz': 'Biz120', 'wc_type': '设备组', 'wc_class': '加工'},
    ],
    'equipments': [
        {'code': 'Eq001', 'name': '中频熔炼炉', 'model': 'ZP-IMF-02', 'biz': 'Biz111'},
        {'code': 'Eq002', 'name': '真空浇注单元', 'model': 'ZP-VC-05', 'biz': 'Biz111'},
        {'code': 'Eq003', 'name': '射线检测系统', 'model': 'ZP-RT-01', 'biz': 'Biz112', 'bottle': YES},
        {'code': 'Eq004', 'name': '五轴卧式加工中心1', 'model': 'ZP-HMC-500', 'biz': 'Biz113', 'bottle': YES},
        {'code': 'Eq005', 'name': '五轴卧式加工中心2', 'model': 'ZP-HMC-500', 'biz': 'Biz114'},
        {'code': 'Eq006', 'name': '三坐标检测机', 'model': 'ZP-CMM-12', 'biz': 'Biz114'},
        {'code': 'Eq007', 'name': '固溶时效炉', 'model': 'ZP-HT-08', 'biz': 'Biz115', 'bottle': YES},
        {'code': 'Eq008', 'name': '喷丸强化机', 'model': 'ZP-SP-03', 'biz': 'Biz115'},
        {'code': 'Eq009', 'name': '荧光渗透检测台', 'model': 'ZP-FPI-06', 'biz': 'Biz116'},
        {'code': 'Eq010', 'name': '装配压装台', 'model': 'ZP-ASM-11', 'biz': 'Biz117'},
        {'code': 'Eq011', 'name': '扭矩紧固台', 'model': 'ZP-TRQ-02', 'biz': 'Biz118', 'bottle': YES},
        {'code': 'Eq012', 'name': '静压检漏台', 'model': 'ZP-LK-02', 'biz': 'Biz118'},
        {'code': 'Eq013', 'name': '冷试校验台', 'model': 'ZP-COLD-07', 'biz': 'Biz119'},
        {'code': 'Eq014', 'name': '热态试车台', 'model': 'ZP-HOT-03', 'biz': 'Biz120', 'bottle': YES},
        {'code': 'Eq015', 'name': '防护包装工位', 'model': 'ZP-PACK-01', 'biz': 'Biz120'},
    ],
    'tools': [],
    'wc_user_links': [
        ('Wc001', 'U-AFS-006'),
        ('Wc002', 'U-AFS-007'),
        ('Wc003', 'U-AFS-008'),
        ('Wc004', 'U-AFS-009'),
        ('Wc006', 'U-AFS-010'),
        ('Wc008', 'U-AFS-011'),
        ('Wc010', 'U-AFS-012'),
        ('Wc011', 'U-AFS-013'),
        ('Wc014', 'U-AFS-014'),
        ('Wc015', 'U-AFS-015'),
    ],
    'wc_eq_links': [
        ('Wc001', 'Eq001'),
        ('Wc001', 'Eq002'),
        ('Wc002', 'Eq003'),
        ('Wc003', 'Eq004'),
        ('Wc004', 'Eq005'),
        ('Wc005', 'Eq006'),
        ('Wc006', 'Eq007'),
        ('Wc007', 'Eq008'),
        ('Wc008', 'Eq009'),
        ('Wc010', 'Eq010'),
        ('Wc011', 'Eq011'),
        ('Wc012', 'Eq012'),
        ('Wc013', 'Eq013'),
        ('Wc014', 'Eq014'),
        ('Wc015', 'Eq015'),
    ],
    'eq_user_links': [
        ('Eq003', 'U-AFS-007'),
        ('Eq004', 'U-AFS-008'),
        ('Eq007', 'U-AFS-010'),
        ('Eq011', 'U-AFS-013'),
        ('Eq014', 'U-AFS-014'),
    ],
    'wc_sup_links': [],
    'warehouses': [
        ('Wh001', '铸造原料库', 'Biz007', 'ERP一级库', '普通库房', '存放高温合金和制壳辅料'),
        ('Wh002', '机加在制库', 'Biz008', '车间二级库', '普通库房', '存放壳体机加在制件'),
        ('Wh003', '热处理周转库', 'Biz009', '车间二级库', '普通库房', '存放热处理待转序件'),
        ('Wh004', '装配齐套库', 'Biz010', '车间二级库', '普通库房', '存放总装齐套件和配套件'),
        ('Wh005', '试车成品库', 'Biz011', 'ERP二级库', '普通库房', '存放试车完成后的待交付成品'),
    ],
    'locations': [
        ('Loc001', '合金区', 'Biz007', 'Wh001'),
        ('Loc002', '制壳辅料区', 'Biz007', 'Wh001'),
        ('Loc003', '待浇注区', 'Biz007', 'Wh001'),
        ('Loc004', '粗加工暂存区', 'Biz008', 'Wh002'),
        ('Loc005', '精加工暂存区', 'Biz008', 'Wh002'),
        ('Loc006', '清洗待检区', 'Biz008', 'Wh002'),
        ('Loc007', '待热处理区', 'Biz009', 'Wh003'),
        ('Loc008', '热后暂存区', 'Biz009', 'Wh003'),
        ('Loc009', '热后待检区', 'Biz009', 'Wh003'),
        ('Loc010', '壳体齐套区', 'Biz010', 'Wh004'),
        ('Loc011', '阀组待装区', 'Biz010', 'Wh004'),
        ('Loc012', '总装待检区', 'Biz010', 'Wh004'),
        ('Loc013', '冷试待入区', 'Biz011', 'Wh005'),
        ('Loc014', '热试待放行区', 'Biz011', 'Wh005'),
        ('Loc015', '交付成品区', 'Biz011', 'Wh005'),
    ],
    'materials': [
        {'code': 'Mat001', 'name': '高温合金母材', 'category': CAT_RAW, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'AFS-M-001', 'unit': '个'},
        {'code': 'Mat002', 'name': '燃油调节器壳体铸件', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_IMPORTANT, 'drawing': 'AFS-C-201'},
        {'code': 'Mat003', 'name': '燃油调节器壳体粗加件', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_IMPORTANT, 'drawing': 'AFS-M-202'},
        {'code': 'Mat004', 'name': '燃油调节器壳体机加件', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': 'AFS-M-203'},
        {'code': 'Mat005', 'name': '燃油调节器壳体热处理件', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': 'AFS-H-204'},
        {'code': 'Mat006', 'name': '计量阀组件', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_KEY, 'drawing': 'AFS-A-301'},
        {'code': 'Mat007', 'name': '驱动齿轮组件', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'AFS-A-302'},
        {'code': 'Mat008', 'name': '高压油路组件', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'AFS-A-303'},
        {'code': 'Mat009', 'name': '过滤组件', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_IMPORTANT, 'drawing': 'AFS-A-304'},
        {'code': 'Mat010', 'name': '密封件套', 'category': CAT_AUX, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'AFS-A-305'},
        {'code': 'Mat011', 'name': '紧固件套', 'category': CAT_AUX, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'AFS-A-306'},
        {'code': 'Mat012', 'name': '试车介质', 'category': CAT_AUX, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'AFS-T-401', 'unit': '个'},
        {'code': 'Mat013', 'name': '防护包装件', 'category': CAT_AUX, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': 'AFS-P-402'},
        {'code': 'Mat014', 'name': '待试航发燃油系统总成', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': 'AFS-A-998', 'serial': YES},
        {'code': 'Mat015', 'name': '航发燃油系统总成', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_KEY, 'drawing': 'AFS-A-999', 'serial': YES},
    ],
    'mboms': [
        {
            'code': 'Mb001',
            'material_code': 'Mat015',
            'name': '航发燃油系统总成MBOM',
            'nodes': [
                {'level': 0, 'material_code': 'Mat015', 'qty': 1},
                {'level': 1, 'material_code': 'Mat014', 'qty': 1, 'parent_material': 'Mat015', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat013', 'qty': 1, 'parent_material': 'Mat015', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'Mat005', 'qty': 1, 'parent_material': 'Mat014', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'Mat006', 'qty': 1, 'parent_material': 'Mat014', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'Mat007', 'qty': 1, 'parent_material': 'Mat014', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'Mat008', 'qty': 1, 'parent_material': 'Mat014', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'Mat009', 'qty': 1, 'parent_material': 'Mat014', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'Mat010', 'qty': 1, 'parent_material': 'Mat014', 'parent_version': 'A.01'},
                {'level': 2, 'material_code': 'Mat011', 'qty': 1, 'parent_material': 'Mat014', 'parent_version': 'A.01'},
            ],
        },
    ],
    'routes': [
        {
            'code': 'Rt001',
            'name': '燃油系统壳体铸造工艺',
            'route_spec': '铸造',
            'biz': 'Biz007',
            'material_code': 'Mat002',
            'proc_spec': '机械加工专业',
            'remark': '铸造工厂完成制壳、浇注和铸件放行。',
            'ops': [
                {'no': '0010', 'name': '制壳熔炼与浇注', 'type': '加工', 'wc': 'Wc001', 'prep': 20, 'run': 48, 'out': 'Mat002', 'content': '完成型壳准备、高温合金熔炼和真空浇注。', 'materials': [('Mat001', 8)], 'steps': [('执行制壳准备', '完成壳型检查和浇注准备'), ('实施熔炼浇注', '完成高温合金熔炼和真空浇注')]},
                {'no': '0020', 'name': '清理补焊与无损检测', 'type': '检验', 'wc': 'Wc002', 'prep': 16, 'run': 32, 'out': 'Mat002', 'content': '完成冒口清理、必要补焊和射线无损检测。', 'materials': [], 'steps': [('执行清理修整', '完成铸件切割清理和局部修整'), ('完成射线检测', '完成铸件无损检测和放行判定')]},
            ],
        },
        {
            'code': 'Rt002',
            'name': '燃油系统壳体机加工艺',
            'route_spec': '机加',
            'biz': 'Biz008',
            'material_code': 'Mat004',
            'proc_spec': '机械加工专业',
            'remark': '机加工工厂完成壳体粗精加工、清洗和尺寸放行。',
            'ops': [
                {'no': '0010', 'name': '基准面与安装面粗加工', 'type': '加工', 'wc': 'Wc003', 'prep': 18, 'run': 36, 'out': 'Mat003', 'content': '完成壳体基准面、安装面和主要腔体粗加工。', 'materials': [('Mat002', 1)], 'steps': [('建立加工基准', '完成壳体装夹定位和基准建立'), ('执行粗加工', '完成壳体基准面和安装面粗加工')]},
                {'no': '0020', 'name': '精加工与孔系加工', 'type': '加工', 'wc': 'Wc004', 'prep': 20, 'run': 42, 'out': 'Mat004', 'content': '完成密封面、阀腔和孔系精加工。', 'materials': [('Mat003', 1)], 'steps': [('执行精加工', '完成关键密封面和安装孔系精加工'), ('复核关键尺寸', '完成孔系与关键配合尺寸复核')]},
                {'no': '0030', 'name': '清洗与尺寸终检', 'type': '检验', 'wc': 'Wc005', 'prep': 12, 'run': 20, 'out': 'Mat004', 'content': '完成壳体清洗、三坐标检测和尺寸放行。', 'materials': [], 'steps': [('执行清洗', '完成切屑去除和内腔清洗'), ('完成尺寸终检', '完成三坐标检测和放行')]},
            ],
        },
        {
            'code': 'Rt003',
            'name': '燃油系统壳体热处理工艺',
            'route_spec': '热表',
            'biz': 'Biz009',
            'material_code': 'Mat005',
            'proc_spec': '机械加工专业',
            'remark': '热处理工厂完成固溶时效、表面强化和热后终检。',
            'ops': [
                {'no': '0010', 'name': '固溶时效热处理', 'type': '加工', 'wc': 'Wc006', 'prep': 24, 'run': 120, 'out': 'Mat005', 'content': '完成壳体固溶和时效处理。', 'materials': [('Mat004', 1)], 'steps': [('装炉固溶', '完成壳体固溶热处理'), ('执行时效', '完成时效处理并记录曲线')]},
                {'no': '0020', 'name': '表面强化与去应力', 'type': '加工', 'wc': 'Wc007', 'prep': 16, 'run': 28, 'out': 'Mat005', 'content': '完成喷丸强化和表面去应力处理。', 'materials': [], 'steps': [('执行喷丸强化', '完成关键表面喷丸处理'), ('完成去应力', '完成表面去应力与状态复核')]},
                {'no': '0030', 'name': '热后终检放行', 'type': '检验', 'wc': 'Wc008', 'prep': 14, 'run': 24, 'out': 'Mat005', 'content': '完成热后硬度、渗透和外观终检。', 'materials': [], 'steps': [('执行硬度检测', '完成热后硬度检测'), ('完成渗透与外观检查', '完成热后渗透检测和放行判定')]},
            ],
        },
        {
            'code': 'Rt004',
            'name': '航发燃油系统总装工艺',
            'route_spec': '装配',
            'biz': 'Biz010',
            'material_code': 'Mat014',
            'proc_spec': '装配专业',
            'remark': '装配工厂完成齐套上线、阀组装配、总装锁紧和静压检漏。',
            'ops': [
                {'no': '0010', 'name': '齐套上线与壳体预装', 'type': '加工', 'wc': 'Wc009', 'prep': 12, 'run': 18, 'out': 'Mat014', 'content': '完成热处理壳体、阀组和配套件齐套上线。', 'materials': [('Mat005', 1), ('Mat010', 1), ('Mat011', 1)], 'steps': [('执行齐套核对', '完成壳体和辅料齐套确认'), ('完成预装准备', '完成壳体上架和预装定位')]},
                {'no': '0020', 'name': '计量阀与驱动机构装配', 'type': '加工', 'wc': 'Wc010', 'prep': 16, 'run': 26, 'out': 'Mat014', 'content': '完成计量阀、驱动齿轮和过滤组件装配。', 'materials': [('Mat006', 1), ('Mat007', 1), ('Mat009', 1)], 'steps': [('装配阀组', '完成计量阀与驱动机构装配'), ('复核阀组状态', '完成阀组间隙与动作状态复核')]},
                {'no': '0030', 'name': '总装锁紧与油路连接', 'type': '加工', 'wc': 'Wc011', 'prep': 18, 'run': 30, 'out': 'Mat014', 'content': '完成高压油路连接、总装锁紧和扭矩复核。', 'materials': [('Mat008', 1), ('Mat011', 1)], 'steps': [('连接高压油路', '完成高压油路组件安装'), ('执行扭矩锁紧', '完成关键连接点扭矩锁紧和复核')]},
                {'no': '0040', 'name': '静压检漏与待试放行', 'type': '检验', 'wc': 'Wc012', 'prep': 12, 'run': 18, 'out': 'Mat014', 'content': '完成静压密封检漏并放行至试车工厂。', 'materials': [], 'steps': [('执行静压检漏', '完成静压密封检漏'), ('完成待试放行', '完成总装状态确认并放行')]},
            ],
        },
        {
            'code': 'Rt005',
            'name': '航发燃油系统试车交付工艺',
            'route_spec': '通用',
            'biz': 'Biz011',
            'material_code': 'Mat015',
            'proc_spec': '装配专业',
            'remark': '试车工厂完成冷试、热态试车、放行包装和入库。',
            'ops': [
                {'no': '0010', 'name': '冷试校验', 'type': '检验', 'wc': 'Wc013', 'prep': 14, 'run': 26, 'out': 'Mat015', 'content': '完成冷态流量、压力和动作响应校验。', 'materials': [('Mat014', 1), ('Mat012', 3)], 'steps': [('执行冷试', '完成冷态流量和压力校验'), ('采集响应参数', '完成动作响应和稳定性采集')]},
                {'no': '0020', 'name': '热态试车与性能复核', 'type': '检验', 'wc': 'Wc014', 'prep': 18, 'run': 36, 'out': 'Mat015', 'content': '完成热态试车、供油曲线复核和性能判定。', 'materials': [('Mat012', 5)], 'steps': [('执行热态试车', '完成热态试车和性能采集'), ('完成性能复核', '完成供油曲线和关键指标判定')]},
                {'no': '0030', 'name': '交付放行与包装入库', 'type': '加工', 'wc': 'Wc015', 'prep': 10, 'run': 16, 'out': 'Mat015', 'content': '完成交付放行、包装防护和成品入库。', 'materials': [('Mat013', 1)], 'steps': [('执行交付放行', '完成试车放行和交付确认'), ('完成包装入库', '完成防护包装和成品入库')]},
            ],
        },
    ],
}


def _inflate_mbom_density(config: dict, module_count: int = 120) -> dict:
    expanded = deepcopy(config)
    materials = expanded['materials']
    mboms = expanded['mboms']
    top_mbom = mboms[0]
    top_nodes = [
        {'level': 0, 'material_code': 'Mat015', 'qty': 1},
        {'level': 1, 'material_code': 'Mat014', 'qty': 1, 'parent_material': 'Mat015', 'parent_version': 'A.01'},
        {'level': 1, 'material_code': 'Mat013', 'qty': 1, 'parent_material': 'Mat015', 'parent_version': 'A.01'},
    ]

    for index in range(1, module_count + 1):
        module_code = f'Mat{15 + index:03d}'
        child_a_code = f'Mat{136 + (index - 1) * 2:03d}'
        child_b_code = f'Mat{137 + (index - 1) * 2:03d}'
        part_a_code = f'Mat{376 + (index - 1) * 3:03d}'
        part_b_code = f'Mat{377 + (index - 1) * 3:03d}'
        part_c_code = f'Mat{378 + (index - 1) * 3:03d}'
        mbom_code = f'Mb{index + 1:03d}'

        materials.extend([
            {'code': module_code, 'name': f'燃油功能模块{index:03d}', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_IMPORTANT, 'drawing': f'AFS-MOD-{index:03d}'},
            {'code': child_a_code, 'name': f'计量阀分总成{index:03d}', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_IMPORTANT, 'drawing': f'AFS-SUBA-{index:03d}'},
            {'code': child_b_code, 'name': f'驱动油路分总成{index:03d}', 'category': CAT_PART, 'make_type': MAKE_SELF, 'feature': FEATURE_IMPORTANT, 'drawing': f'AFS-SUBB-{index:03d}'},
            {'code': part_a_code, 'name': f'计量喷嘴片{index:03d}', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': f'AFS-PA-{index:03d}'},
            {'code': part_b_code, 'name': f'密封衬套{index:03d}', 'category': CAT_AUX, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': f'AFS-PB-{index:03d}'},
            {'code': part_c_code, 'name': f'管路接头{index:03d}', 'category': CAT_PART, 'make_type': MAKE_BUY, 'feature': FEATURE_NORMAL, 'drawing': f'AFS-PC-{index:03d}'},
        ])

        top_nodes.append({'level': 1, 'material_code': module_code, 'qty': 1, 'parent_material': 'Mat015', 'parent_version': 'A.01'})

        mboms.append({
            'code': mbom_code,
            'material_code': module_code,
            'name': f'燃油功能模块{index:03d}MBOM',
            'nodes': [
                {'level': 0, 'material_code': module_code, 'qty': 1},
                {'level': 1, 'material_code': child_a_code, 'qty': 1, 'parent_material': module_code, 'parent_version': 'A.01'},
                {'level': 1, 'material_code': child_b_code, 'qty': 1, 'parent_material': module_code, 'parent_version': 'A.01'},
                {'level': 2, 'material_code': part_a_code, 'qty': 2, 'parent_material': child_a_code, 'parent_version': 'A.01'},
                {'level': 2, 'material_code': part_b_code, 'qty': 2, 'parent_material': child_a_code, 'parent_version': 'A.01'},
                {'level': 2, 'material_code': part_c_code, 'qty': 1, 'parent_material': child_b_code, 'parent_version': 'A.01'},
            ],
        })

    top_mbom['nodes'] = top_nodes
    return expanded


def _shorten_user_codes(seed: dict) -> dict:
    workbooks = seed.get('workbooks', {})
    system = workbooks.get('系统配置_模板.xlsx', {})
    factory = workbooks.get('工厂资源_模板.xlsx', {})
    order_book = workbooks.get('生产订单_模板.xlsx', {})

    user_rows = system.get('用户', [])
    user_map = {
        str(row.get('*编号', '')).strip(): f'U{index:03d}'
        for index, row in enumerate(user_rows, start=1)
    }
    for row in user_rows:
        old_code = str(row.get('*编号', '')).strip()
        if old_code in user_map:
            row['*编号'] = user_map[old_code]

    for row in factory.get('工作中心与用户关系', []):
        user_code = str(row.get('*用户', '')).strip()
        if user_code in user_map:
            row['*用户'] = user_map[user_code]

    for row in factory.get('设备与用户的关系实体类', []):
        user_code = str(row.get('*用户', '')).strip()
        if user_code in user_map:
            row['*用户'] = user_map[user_code]

    for row in order_book.get('生产订单', []):
        planner_code = str(row.get('计划员', '')).strip()
        if planner_code in user_map:
            row['计划员'] = user_map[planner_code]

    return seed


def _shorten_order_codes(seed: dict) -> dict:
    order_book = seed.get('workbooks', {}).get('生产订单_模板.xlsx', {})
    order_rows = order_book.get('生产订单', [])
    pick_rows = order_book.get('备料清单', [])
    order_map = {
        str(row.get('*编码', '')).strip(): f'Mo{index:03d}'
        for index, row in enumerate(order_rows, start=1)
    }

    for row in order_rows:
        old_code = str(row.get('*编码', '')).strip()
        if old_code in order_map:
            new_code = order_map[old_code]
            row['*编码'] = new_code
            row['集成数据主键'] = new_code

    for row in pick_rows:
        order_code = str(row.get('*生产订单编码', '')).strip()
        if order_code in order_map:
            row['*生产订单编码'] = order_map[order_code]

    return seed


def build_variant(namespace: str = NAMESPACE, volume_profile: str = VOLUME_PROFILE) -> dict:
    config = _inflate_mbom_density(BASE_CONFIG)
    metadata = deepcopy(config['metadata'])
    metadata['default_version'] = 'A.01'
    metadata['default_security'] = '内部'
    metadata['volume_profile'] = volume_profile

    builder = SeedBuilder(metadata)
    builder.build_from_config(config)
    seed = builder.seed

    apply_project_collaboration(seed)
    remove_transfer_operations(seed)
    apply_namespace(seed, namespace)
    normalize_user_codes(seed, namespace)
    normalize_poc_security(seed)
    normalize_storage_factory_org(seed)
    normalize_release_user(seed)
    clear_tool_strategy_relations(seed)
    filter_wc_supplier_relations(seed)
    rebuild_route_sequences(seed)
    normalize_sequence_relations(seed)
    apply_production_orders(seed, SCENARIO, namespace)
    _shorten_user_codes(seed)
    _shorten_order_codes(seed)
    return seed


def build() -> dict:
    return build_variant()


def summarize(seed: dict) -> dict:
    summary = summarize_seed(seed)
    mbom_nodes = seed['workbooks']['产品与工艺_模板.xlsx']['MBOM节点']
    summary['mbom_level_counts'] = dict(sorted(Counter(int(row.get('*层级', 0)) for row in mbom_nodes).items()))
    return summary


def main() -> None:
    seed = build()
    ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    ASSET_PATH.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding='utf-8-sig')
    print(json.dumps(summarize(seed), ensure_ascii=False, indent=2))
    print(f'已写入种子文件: {ASSET_PATH}')


if __name__ == '__main__':
    main()
