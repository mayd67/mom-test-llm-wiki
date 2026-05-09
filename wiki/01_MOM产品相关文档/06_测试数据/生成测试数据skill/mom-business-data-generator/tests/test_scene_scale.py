import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from scene_seed_upgrades import apply_scene_upgrade


class SceneScaleTests(unittest.TestCase):
    def load_seed(self, name: str) -> dict:
        return json.loads((ROOT / 'assets' / name).read_text(encoding='utf-8-sig'))

    def build_minimal_seed(self) -> dict:
        return {
            'metadata': {
                'name': '测试种子',
                'default_version': 'A.01',
                'default_security': '公开',
            },
            'external_references': ['0'],
            'workbooks': {
                '系统配置_模板.xlsx': {
                    '行政组织': [
                        {'*父组织编码': '0', '行政组织类型': '公司', '*编码': 'ADM-COMP', '*名称': '测试公司', '简称': '测试'},
                        {'*父组织编码': 'ADM-COMP', '行政组织类型': '工厂', '*编码': 'ADM-PLANT', '*名称': '测试工厂', '简称': '工厂'},
                    ],
                    '业务组织': [
                        {'*父组织编码': '0', '*密级': '公开', '*编码': 'BIZ-COMP', '*名称': '测试公司', '简称': '测试', '工厂组织类型': '公司', '行政组织编码': 'ADM-COMP'},
                        {'*父组织编码': 'BIZ-COMP', '*密级': '公开', '*编码': 'BIZ-PLANT', '*名称': '测试工厂', '简称': '工厂', '工厂组织类型': '工厂', '工厂类型': '机加厂', '行政组织编码': 'ADM-PLANT'},
                        {'*父组织编码': 'BIZ-PLANT', '*密级': '公开', '*编码': 'BIZ-SEC', '*名称': '精加一工段', '简称': '精加工段', '工厂组织类型': '工段', '行政组织编码': 'ADM-PLANT'},
                        {'*父组织编码': 'BIZ-SEC', '*密级': '公开', '*编码': 'BIZ-TEAM', '*名称': '精加甲班', '简称': '甲班', '工厂组织类型': '班组', '行政组织编码': 'ADM-PLANT'},
                    ],
                    '用户': [
                        {'*编号': 'U-BASE-001', '名称': '张晨', '备注': '基础计划员', '用户安全等级': '一般', '性别': '男', '行政组织编码': 'ADM-PLANT', '业务组织编码': 'BIZ-PLANT'},
                    ],
                },
                '工厂资源_模板.xlsx': {
                    '供应商': [],
                    '设备': [
                        {'*编码': 'EQ-001', '*名称': '立式加工中心', '型号': 'VMC-850', '*工厂组织': 'BIZ-SEC', '*密级': '公开', '瓶颈资源': '是'},
                    ],
                    '设备与用户的关系实体类': [],
                    '工装工具': [],
                    '工装检定策略关系': [],
                    '工装保养策略关系': [],
                    '工作中心': [
                        {'*编码': 'WC-001', '*名称': '精加工中心', '*工厂组织': 'BIZ-SEC', '*类型': '加工', '*密级': '公开'},
                    ],
                    '工作中心与用户关系': [],
                    '工作中心与供应商的关系': [],
                    '工作中心与设备的关系': [
                        {'*设备编码': 'EQ-001', '*工作中心编码': 'WC-001'},
                    ],
                    '库房': [],
                    '库位': [],
                    '工序库': [
                        {'*名称': '精车外圆', '*工序类型': '加工', '*工作中心编码': 'WC-001', '*定额准备时间': 10, '*定额加工时间': 30, '*时间单位': '分钟', '执行标记': '是', '产出比': 1, '工序内容': '精车外圆至图纸尺寸', '*密级': '公开'},
                    ],
                },
                '产品与工艺_模板.xlsx': {
                    '物料': [
                        {'*物料分类': '物料', '*名称': '高精度传动轴', '物料类别': '零部件', '图号': 'TS-001', '*制造类型': '自制件', '计量单位': '件', '特性分类': '关键件', '启用批次标记': '是', '启用序列号标记': '否', '物料阶段': '量产', '*版本号': 'A.01', '*编码': 'MAT-001', '*密级': '公开', '发布人': 'U-BASE-001'},
                    ],
                    'MBOM': [
                        {'*MBOM版本号': 'A.01', '*MBOM编码': 'MBOM-001', '物料版本号': 'A.01', '物料编码': 'MAT-001', '发布人': 'U-BASE-001', '*密级': '公开'},
                    ],
                    'MBOM节点': [
                        {'*MBOM版本号': 'A.01', '*MBOM编码': 'MBOM-001', '*物料编码': 'MAT-001', '物料名称': '高精度传动轴', '物料图号': 'TS-001', '*物料版本': 'A.01', '*物料类别': '零部件', '制造类型': '自制件', '数量': 1, '计量单位': '件', '*层级': 0, '*序号': 10, '物料阶段': '量产', '父物料编码': '0', '父物料版本': '0'},
                    ],
                    '工艺路线': [
                        {'*版本号': 'A.01', '*编码': 'ROUTE-001', '*名称': '传动轴机加工路线', '工艺专业': '机加', '物料版本号': 'A.01', '物料编码': 'MAT-001', '*密级': '公开'},
                    ],
                    '工艺路线工序': [
                        {'*工序号': '10', '*工序类型': '加工', '工序内容': '精车外圆至图纸尺寸', '*工作中心编码': 'WC-001', '*定额辅助工时': 10, '*定额加工时间': 30, '*时间单位': '分钟', '执行标记': '是', '产出比': 1, '*工艺路线版本号': 'A.01', '*工艺路线编码': 'ROUTE-001', '*工序名称': '精车外圆', '产出物料版本号': 'A.01', '产出物料编码': 'MAT-001', '工序专业类型': '机加'},
                    ],
                    '工艺路线工序序列': [],
                    '工艺路线工序物料': [],
                    '工艺路线工步': [
                        {'*工艺路线版本号': 'A.01', '*工艺路线编码': 'ROUTE-001', '*工序号': '10', '*工步序号': '10', '*工步名称': '精车', '工步内容': '执行精车外圆加工'},
                    ],
                },
            },
        }

    def profile_counts(self, profile: str) -> dict:
        seed = self.build_minimal_seed()
        upgraded = apply_scene_upgrade(copy.deepcopy(seed), 'cnc_machine', 'CNC85001', volume_profile=profile)
        workbooks = upgraded['workbooks']
        return {
            'profile': upgraded.get('metadata', {}).get('volume_profile'),
            'users': len(workbooks['系统配置_模板.xlsx']['用户']),
            'equipment': len(workbooks['工厂资源_模板.xlsx']['设备']),
            'workcenters': len(workbooks['工厂资源_模板.xlsx']['工作中心']),
            'materials': len(workbooks['产品与工艺_模板.xlsx']['物料']),
            'ops': len(workbooks['产品与工艺_模板.xlsx']['工艺路线工序']),
            'steps': len(workbooks['产品与工艺_模板.xlsx']['工艺路线工步']),
            'seqs': list(workbooks['产品与工艺_模板.xlsx']['工艺路线工序序列']),
        }

    def test_apply_scene_upgrade_defaults_to_standard_profile(self):
        seed = self.build_minimal_seed()
        upgraded = apply_scene_upgrade(copy.deepcopy(seed), 'cnc_machine', 'CNC85001')
        self.assertEqual(upgraded.get('metadata', {}).get('volume_profile'), '标准版')

    def test_volume_profiles_increase_by_level_and_keep_es(self):
        standard = self.profile_counts('标准版')
        big = self.profile_counts('大体量版')
        ultra = self.profile_counts('超大体量版')

        self.assertEqual(standard['profile'], '标准版')
        self.assertEqual(big['profile'], '大体量版')
        self.assertEqual(ultra['profile'], '超大体量版')

        self.assertLess(standard['users'], big['users'])
        self.assertLess(big['users'], ultra['users'])
        self.assertLess(standard['equipment'], big['equipment'])
        self.assertLess(big['equipment'], ultra['equipment'])
        self.assertLess(standard['workcenters'], big['workcenters'])
        self.assertLess(big['workcenters'], ultra['workcenters'])
        self.assertLess(standard['materials'], big['materials'])
        self.assertLess(big['materials'], ultra['materials'])
        self.assertLess(standard['ops'], big['ops'])
        self.assertLess(big['ops'], ultra['ops'])
        self.assertLess(standard['steps'], big['steps'])
        self.assertLess(big['steps'], ultra['steps'])

        for result in (standard, big, ultra):
            self.assertTrue(result['seqs'])
            self.assertTrue(all(row.get('*接续关系') == 'ES' for row in result['seqs']))

    def test_cnc_built_seed_uses_standard_profile_and_keeps_es(self):
        seed = self.load_seed('cnc_machine_seed.json')

        workbooks = seed['workbooks']
        users = workbooks['系统配置_模板.xlsx']['用户']
        equipment = workbooks['工厂资源_模板.xlsx']['设备']
        workcenters = workbooks['工厂资源_模板.xlsx']['工作中心']
        materials = workbooks['产品与工艺_模板.xlsx']['物料']
        route_ops = workbooks['产品与工艺_模板.xlsx']['工艺路线工序']
        route_steps = workbooks['产品与工艺_模板.xlsx']['工艺路线工步']
        route_seqs = workbooks['产品与工艺_模板.xlsx']['工艺路线工序序列']

        self.assertEqual(seed.get('metadata', {}).get('volume_profile'), '标准版')
        self.assertGreaterEqual(len(users), 160)
        self.assertGreaterEqual(len(equipment), 30)
        self.assertGreaterEqual(len(workcenters), 20)
        self.assertGreaterEqual(len(materials), 120)
        self.assertGreaterEqual(len(route_ops), 140)
        self.assertGreaterEqual(len(route_steps), 280)
        self.assertTrue(route_seqs)
        self.assertTrue(all(row.get('*接续关系') == 'ES' for row in route_seqs))

        operator_count = sum('操作工' in str(row.get('备注', '')) for row in users)
        self.assertGreaterEqual(operator_count, 30)


if __name__ == '__main__':
    unittest.main()
