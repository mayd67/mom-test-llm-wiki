from __future__ import annotations

import json
import sys
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

SCENARIO = 'blade_project_collaboration'
NAMESPACE = 'BLD20S01'
VOLUME_PROFILE = '标准版'
ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'blade_project_collaboration_seed.json'


def build_config() -> dict:
    metadata = {
        'name': '高压涡轮叶片多工厂协同MOM种子',
        'industry': '航空发动机零部件',
        'product_family': '高温叶片',
        'product_model': 'BL-1001高压涡轮叶片',
        'description': '面向精密铸造、叶片机加工、热处理涂层多工厂协同的高压涡轮叶片示例数据，包含生产项目部一级工艺与零部件交付计划订单。',
        'project_collaboration': {
            'enabled': True,
            'admin': {
                'parent': 'Adm001',
                'code': 'Adm009',
                'name': '生产项目部',
                'short': '项目部',
            },
            'biz': {
                'parent': 'Biz001',
                'code': 'Biz016',
                'name': '生产项目部',
                'short': '项目部',
                'factory_type': '装配专业',
                'remark': '用于叶片跨工厂协同计划排产、装配交付协同与一级生产订单承载。',
            },
            'route': {
                'code': 'Rt901',
                'name': '高压涡轮叶片一级协同工艺',
                'material_code': 'Mat011',
                'spec': '通用',
                'remark': '生产项目部按参与工厂产能组织协同排产。',
            },
            'phases': [
                {
                    'no': '0010',
                    'name': '精密铸造阶段完成',
                    'wc_code': 'Wc901',
                    'wc_name': '铸造协同排产中心',
                    'content': '项目部按精密铸造工厂产能组织叶片铸造阶段协同排产。',
                    'op_spec': '机械加工专业',
                    'output_code': 'Mat005',
                },
                {
                    'no': '0020',
                    'name': '机加工阶段完成',
                    'wc_code': 'Wc902',
                    'wc_name': '机加协同排产中心',
                    'content': '项目部按叶片机加工工厂产能组织机加工阶段协同排产。',
                    'op_spec': '机械加工专业',
                    'output_code': 'Mat008',
                },
                {
                    'no': '0030',
                    'name': '热处理涂层阶段完成',
                    'wc_code': 'Wc903',
                    'wc_name': '热处理涂层协同中心',
                    'content': '项目部按热处理涂层工厂产能组织热处理与涂层阶段协同排产。',
                    'op_spec': '机械加工专业',
                    'output_code': 'Mat010',
                },
                {
                    'no': '0040',
                    'name': '装配交付阶段完成',
                    'wc_code': 'Wc904',
                    'wc_name': '装配交付协同中心',
                    'content': '生产项目部按装配交付工厂产能组织装配交付与放行协同排产。',
                    'op_spec': '装配专业',
                    'output_code': 'Mat011',
                },
                {
                    'no': '0050',
                    'name': '交付计划放行',
                    'wc_code': 'Wc905',
                    'wc_name': '交付放行协同中心',
                    'content': '生产项目部完成零部件交付计划放行。',
                    'op_type': '检验',
                    'wc_class': '检验',
                    'op_spec': '装配专业',
                    'output_code': 'Mat011',
                },
            ],
        },
    }

    admins = [
        ('0', '公司', 'Adm001', '启航航发部件制造有限公司', '启航航件'),
        ('Adm001', '部门', 'Adm002', '工艺技术中心', '工艺技术'),
        ('Adm001', '部门', 'Adm003', '计划运营中心', '计划运营'),
        ('Adm001', '部门', 'Adm004', '质量管理中心', '质量管理'),
        ('Adm001', '部门', 'Adm005', '设备工装中心', '设备工装'),
        ('Adm001', '工厂', 'Adm006', '精密铸造工厂', '精密铸造'),
        ('Adm001', '工厂', 'Adm007', '叶片机加工工厂', '叶片机加'),
        ('Adm001', '工厂', 'Adm008', '热处理涂层工厂', '热处理涂层'),
        ('Adm001', '工厂', 'Adm010', '装配交付工厂', '装配交付'),
    ]

    bizs = [
        ('0', 'Biz001', '启航航发部件制造有限公司', '启航航件', '公司', 'Adm001', '', '高压涡轮叶片多工厂协同示例'),
        ('Biz001', 'Biz002', '工艺技术中心', '工艺技术', '部门', 'Adm002'),
        ('Biz001', 'Biz003', '计划运营中心', '计划运营', '部门', 'Adm003'),
        ('Biz001', 'Biz004', '质量管理中心', '质量管理', '部门', 'Adm004'),
        ('Biz001', 'Biz005', '设备工装中心', '设备工装', '部门', 'Adm005'),
        ('Biz001', 'Biz006', '精密铸造工厂', '精密铸造', '工厂', 'Adm006', '机械加工专业', '负责蜡模、制壳、浇注和铸态检验'),
        ('Biz001', 'Biz007', '叶片机加工工厂', '叶片机加', '工厂', 'Adm007', '机械加工专业', '负责榫头、叶身和冷却孔机加工'),
        ('Biz001', 'Biz008', '热处理涂层工厂', '热处理涂层', '工厂', 'Adm008', '机械加工专业', '负责热处理、喷丸、涂层和终检包装'),
        ('Biz001', 'Biz017', '装配交付工厂', '装配交付', '工厂', 'Adm010', '装配专业', '负责齐套确认、交付装配、成套包装与发运放行'),
        ('Biz006', 'Biz009', '蜡模制壳车间', '蜡模制壳', '车间', 'Adm006'),
        ('Biz006', 'Biz010', '浇注清理班组', '浇注清理', '班组', 'Adm006'),
        ('Biz007', 'Biz011', '五轴机加车间', '五轴机加', '车间', 'Adm007'),
        ('Biz007', 'Biz012', '冷却孔加工班组', '冷却孔加工', '班组', 'Adm007'),
        ('Biz008', 'Biz013', '热处理涂层车间', '热处理涂层', '车间', 'Adm008'),
        ('Biz013', 'Biz014', '热处理班组', '热处理班组', '班组', 'Adm008'),
        ('Biz013', 'Biz015', '终检包装班组', '终检包装', '班组', 'Adm008'),
        ('Biz017', 'Biz018', '装配交付车间', '装配交付', '车间', 'Adm010'),
        ('Biz018', 'Biz019', '交付保障班组', '交付保障', '班组', 'Adm010'),
    ]

    users = [
        ('U001', '沈知远', '重要', '男', 'Adm002', 'Biz002', '工艺总师'),
        ('U002', '叶清和', '重要', '女', 'Adm002', 'Biz002', '铸造工艺工程师'),
        ('U003', '何若川', '重要', '男', 'Adm002', 'Biz002', '机加工艺工程师'),
        ('U004', '顾言溪', '重要', '女', 'Adm002', 'Biz002', '热处理工艺工程师'),
        ('U005', '宋承安', '重要', '男', 'Adm003', 'Biz003', '主计划员'),
        ('U006', '陆星辞', '一般', '女', 'Adm003', 'Biz003', '生产计划员'),
        ('U007', '周书宁', '重要', '女', 'Adm004', 'Biz004', '质量主管'),
        ('U008', '许见山', '一般', '男', 'Adm004', 'Biz004', '无损检测工程师'),
        ('U009', '唐知夏', '一般', '女', 'Adm004', 'Biz004', '终检工程师'),
        ('U010', '林见川', '一般', '男', 'Adm005', 'Biz005', '设备工程师'),
        ('U011', '韩书远', '一般', '男', 'Adm005', 'Biz005', '工装工程师'),
        ('U012', '乔云舒', '一般', '女', 'Adm006', 'Biz009', '制壳班组长'),
        ('U013', '苏景程', '一般', '男', 'Adm006', 'Biz009', '制蜡操作工'),
        ('U014', '季安和', '一般', '男', 'Adm006', 'Biz010', '浇注操作工'),
        ('U015', '温清妍', '一般', '女', 'Adm006', 'Biz010', '铸态检验员'),
        ('U016', '邵言舟', '一般', '男', 'Adm007', 'Biz011', '机加班组长'),
        ('U017', '沈可欣', '一般', '女', 'Adm007', 'Biz011', '五轴加工操作工'),
        ('U018', '郑明哲', '一般', '男', 'Adm007', 'Biz012', '电火花打孔操作工'),
        ('U019', '陆雨桐', '一般', '女', 'Adm007', 'Biz011', '三坐标检验员'),
        ('U020', '周景程', '一般', '男', 'Adm008', 'Biz014', '热处理班组长'),
        ('U021', '许安宁', '一般', '女', 'Adm008', 'Biz014', '热处理操作工'),
        ('U022', '宋知行', '一般', '男', 'Adm008', 'Biz013', '喷丸涂层操作工'),
        ('U023', '温以宁', '一般', '女', 'Adm008', 'Biz015', '包装入库员'),
        ('U024', '顾明川', '一般', '男', 'Adm008', 'Biz015', '终检放行员'),
        ('U025', '秦若衡', '一般', '男', 'Adm010', 'Biz018', '装配交付班组长'),
        ('U026', '程知夏', '一般', '女', 'Adm010', 'Biz019', '交付装配操作工'),
        ('U027', '谢闻笙', '一般', '男', 'Adm010', 'Biz019', '发运放行员'),
    ]

    suppliers = [
        {'code': 'Sup001', 'name': '航材高温合金有限公司', 'short': '航材合金', 'remark': '供应高温合金母材'},
        {'code': 'Sup002', 'name': '云岭精密陶壳材料有限公司', 'short': '云岭陶壳', 'remark': '供应陶壳型砂与面层材料'},
        {'code': 'Sup003', 'name': '远澄检测耗材有限公司', 'short': '远澄检测', 'remark': '供应荧光渗透与射线检测耗材'},
        {'code': 'Sup004', 'name': '星河涂层材料有限公司', 'short': '星河涂层', 'remark': '供应热障涂层粉末'},
        {'code': 'Sup005', 'name': '锐锋刀具科技有限公司', 'short': '锐锋刀具', 'remark': '供应叶片专用刀具与电极丝'},
        {'code': 'Sup006', 'name': '启盛包装材料有限公司', 'short': '启盛包装', 'remark': '供应包装箱、标签与防护材料'},
    ]

    work_centers = [
        {'code': 'Wc001', 'name': '蜡模制备中心', 'biz': 'Biz009', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责蜡模压型与组树'},
        {'code': 'Wc002', 'name': '制壳焙烧中心', 'biz': 'Biz009', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责制壳、干燥和焙烧'},
        {'code': 'Wc003', 'name': '浇注清理中心', 'biz': 'Biz010', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责真空浇注、脱壳和切割清理'},
        {'code': 'Wc004', 'name': '铸态检验中心', 'biz': 'Biz010', 'wc_type': '组织', 'wc_class': '检验', 'remark': '负责铸态尺寸与无损检验'},
        {'code': 'Wc005', 'name': '基准加工中心', 'biz': 'Biz011', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责基准面和叶身初加工'},
        {'code': 'Wc006', 'name': '榫头精加工中心', 'biz': 'Biz011', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责榫头和型面精加工'},
        {'code': 'Wc007', 'name': '冷却孔加工中心', 'biz': 'Biz012', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责电火花冷却孔加工'},
        {'code': 'Wc008', 'name': '机加检验中心', 'biz': 'Biz011', 'wc_type': '组织', 'wc_class': '检验', 'remark': '负责三坐标和流道复核'},
        {'code': 'Wc009', 'name': '热处理中心', 'biz': 'Biz013', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责固溶时效处理'},
        {'code': 'Wc010', 'name': '喷丸涂层中心', 'biz': 'Biz013', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责喷丸校形和热障涂层'},
        {'code': 'Wc011', 'name': '终检包装中心', 'biz': 'Biz015', 'wc_type': '组织', 'wc_class': '检验', 'remark': '负责终检、包装和入库'},
        {'code': 'Wc012', 'name': '工装准备中心', 'biz': 'Biz005', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责叶片专用工装准备和维护'},
        {'code': 'Wc013', 'name': '齐套确认中心', 'biz': 'Biz018', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责装配前齐套确认与交付成套复核'},
        {'code': 'Wc014', 'name': '装配交付中心', 'biz': 'Biz019', 'wc_type': '组织', 'wc_class': '加工', 'remark': '负责防护装配、成套包装和交付放行'},
    ]

    equipments = [
        {'code': 'Eq001', 'name': '蜡模压型机', 'model': 'WM-180', 'biz': 'Biz009', 'remark': '蜡模压型'},
        {'code': 'Eq002', 'name': '组树工位台', 'model': 'GS-12', 'biz': 'Biz009', 'remark': '蜡模组树'},
        {'code': 'Eq003', 'name': '制壳线A', 'model': 'SK-A', 'biz': 'Biz009', 'remark': '陶壳制备'},
        {'code': 'Eq004', 'name': '焙烧炉', 'model': 'BS-950', 'biz': 'Biz009', 'remark': '陶壳焙烧'},
        {'code': 'Eq005', 'name': '真空熔炼炉', 'model': 'VM-50', 'biz': 'Biz010', 'remark': '高温合金熔炼'},
        {'code': 'Eq006', 'name': '定向凝固炉', 'model': 'DG-12', 'biz': 'Biz010', 'remark': '定向凝固浇注'},
        {'code': 'Eq007', 'name': '切割清理机', 'model': 'QG-300', 'biz': 'Biz010', 'remark': '脱壳切割清理'},
        {'code': 'Eq008', 'name': 'X射线检测机', 'model': 'RT-900', 'biz': 'Biz010', 'remark': '铸态无损检测'},
        {'code': 'Eq009', 'name': '荧光渗透检测线', 'model': 'PT-500', 'biz': 'Biz010', 'remark': '表面缺陷检测'},
        {'code': 'Eq010', 'name': '五轴加工中心1', 'model': 'MC-500', 'biz': 'Biz011', 'remark': '叶身精加工'},
        {'code': 'Eq011', 'name': '五轴加工中心2', 'model': 'MC-500', 'biz': 'Biz011', 'remark': '榫头精加工'},
        {'code': 'Eq012', 'name': '数控成型磨', 'model': 'MG-220', 'biz': 'Biz011', 'remark': '榫头修磨'},
        {'code': 'Eq013', 'name': '电火花打孔机1', 'model': 'EDM-80', 'biz': 'Biz012', 'remark': '冷却孔加工'},
        {'code': 'Eq014', 'name': '电火花打孔机2', 'model': 'EDM-80', 'biz': 'Biz012', 'remark': '冷却孔加工'},
        {'code': 'Eq015', 'name': '三坐标测量机', 'model': 'CMM-1200', 'biz': 'Biz011', 'remark': '尺寸检测'},
        {'code': 'Eq016', 'name': '流量测试台', 'model': 'FL-30', 'biz': 'Biz011', 'remark': '冷却孔流量检测'},
        {'code': 'Eq017', 'name': '真空热处理炉1', 'model': 'HT-900', 'biz': 'Biz013', 'remark': '固溶热处理'},
        {'code': 'Eq018', 'name': '真空热处理炉2', 'model': 'HT-900', 'biz': 'Biz013', 'remark': '时效热处理'},
        {'code': 'Eq019', 'name': '喷丸机', 'model': 'PM-400', 'biz': 'Biz013', 'remark': '喷丸强化'},
        {'code': 'Eq020', 'name': '热障涂层喷涂柜', 'model': 'TC-220', 'biz': 'Biz013', 'remark': '热障涂层制备'},
        {'code': 'Eq021', 'name': '涂层烧结炉', 'model': 'SJ-600', 'biz': 'Biz013', 'remark': '涂层固化'},
        {'code': 'Eq022', 'name': '包装标识台', 'model': 'PK-20', 'biz': 'Biz015', 'remark': '包装与标签'},
        {'code': 'Eq023', 'name': '齐套复核台', 'model': 'KT-30', 'biz': 'Biz018', 'remark': '交付前齐套与配套复核'},
        {'code': 'Eq024', 'name': '真空防护包装台', 'model': 'VP-60', 'biz': 'Biz019', 'remark': '成品防护包装与封装'},
        {'code': 'Eq025', 'name': '发运称重复核台', 'model': 'SC-15', 'biz': 'Biz019', 'remark': '成品发运称重与出库复核'},
    ]

    tools = [
        {'code': 'Tool001', 'name': '蜡模压型模具', 'material_category': CAT_PART, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_KEY, 'model': 'WMJ-01', 'spec': '叶片蜡模', 'remark': '叶片蜡模压型模具', 'life_times': 120000, 'life_days': 365},
        {'code': 'Tool002', 'name': '组树夹具', 'material_category': CAT_PART, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_IMPORTANT, 'model': 'GSJ-01', 'spec': '组树定位', 'remark': '蜡模组树定位夹具', 'life_times': 80000, 'life_days': 365},
        {'code': 'Tool003', 'name': '制壳挂具', 'material_category': CAT_PART, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_IMPORTANT, 'model': 'SKG-01', 'spec': '制壳挂具', 'remark': '陶壳制备挂具', 'life_times': 60000, 'life_days': 365},
        {'code': 'Tool004', 'name': '叶身定位夹具', 'material_category': CAT_PART, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_KEY, 'model': 'JYJ-01', 'spec': '叶身定位', 'remark': '叶身基准加工夹具', 'life_times': 90000, 'life_days': 365},
        {'code': 'Tool005', 'name': '榫头精加工夹具', 'material_category': CAT_PART, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_KEY, 'model': 'STJ-01', 'spec': '榫头夹具', 'remark': '榫头精加工定位夹具', 'life_times': 90000, 'life_days': 365},
        {'code': 'Tool006', 'name': '冷却孔定位夹具', 'material_category': CAT_PART, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_IMPORTANT, 'model': 'LKJ-01', 'spec': '冷却孔夹具', 'remark': '电火花打孔定位夹具', 'life_times': 70000, 'life_days': 365},
        {'code': 'Tool007', 'name': '叶片型面检具', 'material_category': CAT_PART, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_KEY, 'model': 'JJ-01', 'spec': '型面检具', 'remark': '叶片型面快速检验', 'life_times': 70000, 'life_days': 365},
        {'code': 'Tool008', 'name': '热处理料篮', 'material_category': CAT_PART, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_IMPORTANT, 'model': 'RL-01', 'spec': '热处理料篮', 'remark': '热处理装炉料篮', 'life_times': 50000, 'life_days': 365},
        {'code': 'Tool009', 'name': '喷丸吊具', 'material_category': CAT_PART, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_IMPORTANT, 'model': 'PMD-01', 'spec': '喷丸吊具', 'remark': '喷丸作业吊具', 'life_times': 60000, 'life_days': 365},
        {'code': 'Tool010', 'name': '涂层遮蔽工装', 'material_category': CAT_PART, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_IMPORTANT, 'model': 'TCZ-01', 'spec': '遮蔽工装', 'remark': '涂层遮蔽与保护工装', 'life_times': 50000, 'life_days': 365},
        {'code': 'Tool011', 'name': '包装托架', 'material_category': CAT_PART, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_NORMAL, 'model': 'PKJ-01', 'spec': '包装托架', 'remark': '成品包装周转托架', 'life_times': 40000, 'life_days': 365},
        {'code': 'Tool012', 'name': '流量检测堵具', 'material_category': CAT_PART, 'make_type': MAKE_SELF, 'tooling_category': '专用工装', 'feature': FEATURE_IMPORTANT, 'model': 'LLJ-01', 'spec': '流量堵具', 'remark': '冷却孔流量检测堵具', 'life_times': 50000, 'life_days': 365},
    ]

    wc_user_links = [
        ('Wc001', 'U012'), ('Wc001', 'U013'),
        ('Wc002', 'U012'), ('Wc002', 'U013'),
        ('Wc003', 'U014'), ('Wc003', 'U015'),
        ('Wc004', 'U008'), ('Wc004', 'U015'),
        ('Wc005', 'U016'), ('Wc005', 'U017'),
        ('Wc006', 'U016'), ('Wc006', 'U017'),
        ('Wc007', 'U018'), ('Wc007', 'U019'),
        ('Wc008', 'U019'), ('Wc008', 'U007'),
        ('Wc009', 'U020'), ('Wc009', 'U021'),
        ('Wc010', 'U022'), ('Wc010', 'U021'),
        ('Wc011', 'U023'), ('Wc011', 'U024'), ('Wc011', 'U009'),
        ('Wc012', 'U010'), ('Wc012', 'U011'),
        ('Wc013', 'U025'), ('Wc013', 'U026'),
        ('Wc014', 'U026'), ('Wc014', 'U027'),
    ]

    wc_eq_links = [
        ('Wc001', 'Eq001'), ('Wc001', 'Eq002'),
        ('Wc002', 'Eq003'), ('Wc002', 'Eq004'),
        ('Wc003', 'Eq005'), ('Wc003', 'Eq006'), ('Wc003', 'Eq007'),
        ('Wc004', 'Eq008'), ('Wc004', 'Eq009'),
        ('Wc005', 'Eq010'),
        ('Wc006', 'Eq011'), ('Wc006', 'Eq012'),
        ('Wc007', 'Eq013'), ('Wc007', 'Eq014'),
        ('Wc008', 'Eq015'), ('Wc008', 'Eq016'),
        ('Wc009', 'Eq017'), ('Wc009', 'Eq018'),
        ('Wc010', 'Eq019'), ('Wc010', 'Eq020'), ('Wc010', 'Eq021'),
        ('Wc011', 'Eq022'),
        ('Wc013', 'Eq023'),
        ('Wc014', 'Eq024'), ('Wc014', 'Eq025'),
    ]

    eq_user_links = [
        ('Eq001', 'U013'), ('Eq002', 'U013'), ('Eq003', 'U012'), ('Eq004', 'U012'),
        ('Eq005', 'U014'), ('Eq006', 'U014'), ('Eq007', 'U014'), ('Eq008', 'U008'), ('Eq009', 'U015'),
        ('Eq010', 'U017'), ('Eq011', 'U017'), ('Eq012', 'U016'), ('Eq013', 'U018'), ('Eq014', 'U018'),
        ('Eq015', 'U019'), ('Eq016', 'U019'), ('Eq017', 'U021'), ('Eq018', 'U021'), ('Eq019', 'U022'),
        ('Eq020', 'U022'), ('Eq021', 'U022'), ('Eq022', 'U023'),
        ('Eq023', 'U025'), ('Eq024', 'U026'), ('Eq025', 'U027'),
    ]

    warehouses = [
        ('Wh001', '铸造原辅料库', 'Biz006', 'ERP一级库', '普通库房', '存放合金母材、蜡料和陶壳材料'),
        ('Wh002', '铸态毛坯库', 'Biz006', 'ERP一级库', '普通库房', '存放铸态叶片毛坯和待机加件'),
        ('Wh003', '机加在制品库', 'Biz007', 'ERP一级库', '普通库房', '存放机加半成品和待热处理件'),
        ('Wh004', '热处理待处理库', 'Biz008', 'ERP一级库', '普通库房', '存放待热处理与待涂层件'),
        ('Wh005', '成品交付库', 'Biz008', 'ERP一级库', '普通库房', '存放终检合格叶片成品'),
        ('Wh006', '装配交付成套库', 'Biz017', 'ERP一级库', '普通库房', '存放待交付齐套件、包装成套件与待发运成品'),
    ]

    locations = [
        ('Loc001', '合金母材区', 'Biz006', 'Wh001'), ('Loc002', '蜡料区', 'Biz006', 'Wh001'), ('Loc003', '制壳材料区', 'Biz006', 'Wh001'), ('Loc004', '检测耗材区', 'Biz006', 'Wh001'),
        ('Loc005', '铸态待检区', 'Biz006', 'Wh002'), ('Loc006', '合格毛坯区', 'Biz006', 'Wh002'), ('Loc007', '返修判定区', 'Biz006', 'Wh002'), ('Loc008', '待转机加区', 'Biz006', 'Wh002'),
        ('Loc009', '基准加工待制区', 'Biz007', 'Wh003'), ('Loc010', '榫头精加工区', 'Biz007', 'Wh003'), ('Loc011', '打孔待检区', 'Biz007', 'Wh003'), ('Loc012', '机加合格区', 'Biz007', 'Wh003'),
        ('Loc013', '待热处理区', 'Biz008', 'Wh004'), ('Loc014', '热处理完成区', 'Biz008', 'Wh004'), ('Loc015', '待喷丸区', 'Biz008', 'Wh004'), ('Loc016', '待涂层区', 'Biz008', 'Wh004'),
        ('Loc017', '终检待判区', 'Biz008', 'Wh005'), ('Loc018', '成品暂存区', 'Biz008', 'Wh005'), ('Loc019', '包装完成区', 'Biz008', 'Wh005'), ('Loc020', '交付发运区', 'Biz008', 'Wh005'),
        ('Loc021', '齐套待确认区', 'Biz017', 'Wh006'), ('Loc022', '交付装配区', 'Biz017', 'Wh006'), ('Loc023', '成套包装区', 'Biz017', 'Wh006'), ('Loc024', '待发运放行区', 'Biz017', 'Wh006'),
    ]

    material_specs = [
        ('Mat001', '高温合金母材', CAT_RAW, MAKE_BUY, FEATURE_KEY, 'BL-1001-001', '个', '', '母材锭料', '叶片铸造用高温合金母材'),
        ('Mat002', '叶片蜡模', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'BL-1001-002', '个', '', '蜡模件', '精密铸造用叶片蜡模'),
        ('Mat003', '陶壳材料', CAT_AUX, MAKE_BUY, FEATURE_IMPORTANT, 'BL-1001-003', '个', '', '面层背层材料', '制壳焙烧辅料'),
        ('Mat004', '铸态叶片毛坯', CAT_PART, MAKE_SELF, FEATURE_KEY, 'BL-1001-004', '个', '', '铸态毛坯', '真空浇注后的叶片毛坯'),
        ('Mat005', '清理合格叶片毛坯', CAT_PART, MAKE_SELF, FEATURE_KEY, 'BL-1001-005', '个', '', '铸造阶段完成件', '完成脱壳切割和铸态检验'),
        ('Mat006', '基准加工叶片', CAT_PART, MAKE_SELF, FEATURE_IMPORTANT, 'BL-1001-006', '个', '', '基准加工件', '完成基准面和叶身初加工'),
        ('Mat007', '电极丝', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'BL-1001-007', '个', '', '打孔耗材', '冷却孔电火花加工耗材'),
        ('Mat008', '机加工完成叶片', CAT_PART, MAKE_SELF, FEATURE_KEY, 'BL-1001-008', '个', '', '机加工阶段完成件', '完成榫头精加工和冷却孔加工'),
        ('Mat009', '热处理叶片', CAT_PART, MAKE_SELF, FEATURE_KEY, 'BL-1001-009', '个', '', '热处理件', '固溶时效后的叶片'),
        ('Mat010', '涂层叶片', CAT_PART, MAKE_SELF, FEATURE_KEY, 'BL-1001-010', '个', '', '涂层件', '完成热障涂层后的叶片'),
        ('Mat011', '高压涡轮叶片', CAT_PART, MAKE_SELF, FEATURE_KEY, 'BL-1001-011', '个', '', '成品叶片', '最终交付的高压涡轮叶片成品'),
        ('Mat012', '荧光渗透液', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'BL-1001-012', '个', '', '渗透检测辅料', '无损检验辅料'),
        ('Mat013', '射线检测耗材', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'BL-1001-013', '个', '', '射线检测辅料', '铸态射线检测耗材'),
        ('Mat014', '喷丸介质', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'BL-1001-014', '个', '', '喷丸辅料', '喷丸强化介质'),
        ('Mat015', '热障涂层粉末', CAT_AUX, MAKE_BUY, FEATURE_IMPORTANT, 'BL-1001-015', '个', '', '涂层粉末', '叶片热障涂层粉末'),
        ('Mat016', '专用包装盒', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'BL-1001-016', '个', '', '包装盒', '叶片交付包装盒'),
        ('Mat017', '防护袋', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'BL-1001-017', '个', '', '防护袋', '成品防护包装袋'),
        ('Mat018', '标签卡', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'BL-1001-018', '个', '', '标签卡', '条码和标签标识材料'),
        ('Mat019', '周转托盘', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'BL-1001-019', '个', '', '周转托盘', '叶片在制与成品周转托盘'),
        ('Mat020', '终检对比样片', CAT_PART, MAKE_SELF, FEATURE_NORMAL, 'BL-1001-020', '个', '', '样件', '终检对比和讲解展示样件'),
        ('Mat021', '交付防护组件', CAT_AUX, MAKE_BUY, FEATURE_IMPORTANT, 'BL-1001-021', '个', '', '防护组件', '成品交付装配防护组件'),
        ('Mat022', '发运外箱', CAT_AUX, MAKE_BUY, FEATURE_NORMAL, 'BL-1001-022', '个', '', '发运外箱', '成套交付发运外包装箱'),
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
            'material_code': 'Mat011',
            'name': '高压涡轮叶片MBOM',
            'nodes': [
                {'level': 0, 'material_code': 'Mat011', 'qty': 1},
                {'level': 1, 'material_code': 'Mat001', 'qty': 1, 'parent_material': 'Mat011', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat003', 'qty': 1, 'parent_material': 'Mat011', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat007', 'qty': 1, 'parent_material': 'Mat011', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat012', 'qty': 1, 'parent_material': 'Mat011', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat013', 'qty': 1, 'parent_material': 'Mat011', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat014', 'qty': 1, 'parent_material': 'Mat011', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat015', 'qty': 1, 'parent_material': 'Mat011', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat016', 'qty': 1, 'parent_material': 'Mat011', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat017', 'qty': 1, 'parent_material': 'Mat011', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat018', 'qty': 1, 'parent_material': 'Mat011', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat021', 'qty': 1, 'parent_material': 'Mat011', 'parent_version': 'A.01'},
                {'level': 1, 'material_code': 'Mat022', 'qty': 1, 'parent_material': 'Mat011', 'parent_version': 'A.01'},
            ],
        },
    ]

    routes = [
        {
            'code': 'Rt001',
            'name': '叶片精密铸造工艺',
            'route_spec': '铸造',
            'biz': 'Biz006',
            'material_code': 'Mat005',
            'proc_spec': '机械加工专业',
            'remark': '精密铸造工厂完成蜡模、制壳、浇注和铸态检验。',
            'ops': [
                {'no': '0010', 'name': '蜡模压型与组树', 'type': '加工', 'wc': 'Wc001', 'prep': 12, 'run': 20, 'out': 'Mat002', 'content': '完成叶片蜡模压型和组树。', 'materials': [], 'steps': [('压制蜡模', '完成叶片蜡模压制'), ('组树校形', '完成蜡模组树和形位校核')]},
                {'no': '0020', 'name': '制壳与焙烧', 'type': '加工', 'wc': 'Wc002', 'prep': 16, 'run': 36, 'out': 'Mat002', 'content': '完成多层制壳、干燥和焙烧。', 'materials': [('Mat003', 1)], 'steps': [('重复挂浆撒砂', '完成面层和背层制壳'), ('焙烧壳型', '完成壳型焙烧和强度确认')]},
                {'no': '0030', 'name': '真空浇注脱壳清理', 'type': '加工', 'wc': 'Wc003', 'prep': 20, 'run': 40, 'out': 'Mat004', 'content': '完成高温合金浇注、脱壳和切割清理。', 'materials': [('Mat001', 1)], 'steps': [('真空熔炼浇注', '完成高温合金熔炼和浇注'), ('脱壳切割清理', '完成脱壳、冒口切除和清理')]},
                {'no': '0040', 'name': '铸态无损与尺寸检验', 'type': '检验', 'wc': 'Wc004', 'prep': 12, 'run': 18, 'out': 'Mat005', 'content': '完成铸态荧光渗透、射线和尺寸检验。', 'materials': [('Mat012', 1), ('Mat013', 1)], 'steps': [('执行无损检测', '执行荧光渗透和射线检测'), ('铸态尺寸判定', '完成铸态尺寸与外观放行')]},
            ],
        },
        {
            'code': 'Rt002',
            'name': '叶片机加工工艺',
            'route_spec': '机加',
            'biz': 'Biz007',
            'material_code': 'Mat008',
            'proc_spec': '机械加工专业',
            'remark': '叶片机加工工厂完成基准加工、榫头精加工和冷却孔加工。',
            'ops': [
                {'no': '0010', 'name': '基准面与叶身初加工', 'type': '加工', 'wc': 'Wc005', 'prep': 12, 'run': 24, 'out': 'Mat006', 'content': '完成基准面与叶身初加工。', 'materials': [('Mat005', 1)], 'steps': [('建立加工基准', '完成叶片基准定位'), ('叶身初加工', '完成叶身余量去除')]},
                {'no': '0020', 'name': '榫头与型面精加工', 'type': '加工', 'wc': 'Wc006', 'prep': 14, 'run': 28, 'out': 'Mat008', 'content': '完成榫头与关键型面精加工。', 'materials': [('Mat006', 1)], 'steps': [('榫头精铣', '完成榫头尺寸和表面质量控制'), ('型面精修', '完成叶身型面精修')]},
                {'no': '0030', 'name': '冷却孔电火花加工', 'type': '加工', 'wc': 'Wc007', 'prep': 12, 'run': 22, 'out': 'Mat008', 'content': '完成冷却孔电火花加工与修整。', 'materials': [('Mat007', 1)], 'steps': [('冷却孔加工', '完成冷却孔打孔'), ('孔口修整', '完成孔口去毛刺与流道修整')]},
                {'no': '0040', 'name': '机加尺寸与流量检验', 'type': '检验', 'wc': 'Wc008', 'prep': 10, 'run': 16, 'out': 'Mat008', 'content': '完成三坐标、型面和流量检验。', 'materials': [], 'steps': [('三坐标检测', '完成关键尺寸检测'), ('流量复核', '完成冷却孔流量复核')]},
            ],
        },
        {
            'code': 'Rt003',
            'name': '叶片热处理涂层工艺',
            'route_spec': '热表',
            'biz': 'Biz008',
            'material_code': 'Mat010',
            'proc_spec': '机械加工专业',
            'remark': '热处理涂层工厂完成热处理、喷丸和热障涂层。',
            'ops': [
                {'no': '0010', 'name': '固溶时效热处理', 'type': '加工', 'wc': 'Wc009', 'prep': 16, 'run': 60, 'out': 'Mat009', 'content': '完成固溶和时效热处理。', 'materials': [('Mat008', 1)], 'steps': [('装炉热处理', '完成固溶热处理'), ('时效处理', '完成时效处理并记录曲线')]},
                {'no': '0020', 'name': '喷丸校形', 'type': '加工', 'wc': 'Wc010', 'prep': 12, 'run': 18, 'out': 'Mat009', 'content': '完成喷丸强化和校形。', 'materials': [('Mat014', 1)], 'steps': [('喷丸强化', '完成叶片喷丸强化'), ('校形复核', '完成叶片变形校形复核')]},
                {'no': '0030', 'name': '热障涂层制备', 'type': '加工', 'wc': 'Wc010', 'prep': 14, 'run': 26, 'out': 'Mat010', 'content': '完成热障涂层喷涂与固化。', 'materials': [('Mat015', 1)], 'steps': [('喷涂遮蔽', '完成关键区域遮蔽与喷涂'), ('涂层固化', '完成涂层烧结固化')]},
            ],
        },
        {
            'code': 'Rt004',
            'name': '叶片装配交付工艺',
            'route_spec': '装配',
            'biz': 'Biz017',
            'material_code': 'Mat011',
            'proc_spec': '装配专业',
            'remark': '装配交付工厂完成齐套确认、防护装配、成套包装与交付放行。',
            'ops': [
                {'no': '0010', 'name': '齐套确认', 'type': '加工', 'wc': 'Wc013', 'prep': 8, 'run': 12, 'out': 'Mat010', 'content': '完成涂层叶片、包装物料和交付附件齐套确认。', 'materials': [('Mat010', 1), ('Mat016', 1), ('Mat017', 1), ('Mat018', 1)], 'steps': [('物料齐套复核', '完成交付件与包装辅料齐套复核'), ('交付资料确认', '完成标签、流转卡和交付资料确认')]},
                {'no': '0020', 'name': '防护装配与交付包装', 'type': '加工', 'wc': 'Wc014', 'prep': 10, 'run': 18, 'out': 'Mat011', 'content': '完成成品防护装配、外箱包装与交付放行。', 'materials': [('Mat021', 1), ('Mat022', 1)], 'steps': [('防护装配', '完成叶片防护组件装配与状态确认'), ('成套包装', '完成发运外箱包装与标识'), ('交付放行', '完成交付放行与发运确认')]},
            ],
        },
    ]

    return {
        'metadata': metadata,
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
    metadata = dict(CONFIG['metadata'])
    metadata['default_version'] = 'A.01'
    metadata['default_security'] = '内部'
    metadata['volume_profile'] = volume_profile

    builder = SeedBuilder(metadata)
    builder.build_from_config(CONFIG)
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
