from copy import deepcopy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_gearbox_assembly_seed as gearbox_assembly_seed
import build_gearbox_machining_assembly_seed as gearbox_machining_seed
import build_gearbox_multi_factory_seed as gearbox_multi_factory_seed
from gearbox_seed_support import build_seed


class GearboxSeedScenarioTests(unittest.TestCase):
    def counts(self, seed: dict) -> dict:
        workbooks = seed['workbooks']
        return {
            'users': len(workbooks['系统配置_模板.xlsx']['用户']),
            'equipment': len(workbooks['工厂资源_模板.xlsx']['设备']),
            'workcenters': len(workbooks['工厂资源_模板.xlsx']['工作中心']),
            'materials': len(workbooks['产品与工艺_模板.xlsx']['物料']),
            'ops': len(workbooks['产品与工艺_模板.xlsx']['工艺路线工序']),
            'steps': len(workbooks['产品与工艺_模板.xlsx']['工艺路线工步']),
        }

    def assert_profile_growth(self, module, namespaces: tuple[str, str, str]) -> None:
        standard = module.build_variant(namespaces[0], '标准版')
        big = module.build_variant(namespaces[1], '大体量版')
        ultra = module.build_variant(namespaces[2], '超大体量版')

        self.assertEqual(standard.get('metadata', {}).get('namespace'), namespaces[0])
        self.assertEqual(standard.get('metadata', {}).get('volume_profile'), '标准版')
        self.assertEqual(big.get('metadata', {}).get('namespace'), namespaces[1])
        self.assertEqual(big.get('metadata', {}).get('volume_profile'), '大体量版')
        self.assertEqual(ultra.get('metadata', {}).get('namespace'), namespaces[2])
        self.assertEqual(ultra.get('metadata', {}).get('volume_profile'), '超大体量版')

        standard_counts = self.counts(standard)
        big_counts = self.counts(big)
        ultra_counts = self.counts(ultra)

        for key in standard_counts:
            self.assertLess(standard_counts[key], big_counts[key], msg=f'{module.__name__}:{key}')
            self.assertLess(big_counts[key], ultra_counts[key], msg=f'{module.__name__}:{key}')

    def test_all_gearbox_scenarios_support_three_volume_profiles(self):
        cases = [
            (gearbox_assembly_seed, ('GBA20S01', 'GBA31S01', 'GBA42S01')),
            (gearbox_machining_seed, ('GBM20S01', 'GBM31S01', 'GBM42S01')),
            (gearbox_multi_factory_seed, ('GBX20S01', 'GBX31S01', 'GBX42S01')),
        ]
        for module, namespaces in cases:
            with self.subTest(module=module.__name__):
                self.assert_profile_growth(module, namespaces)

    def test_single_factory_assembly_scheme_builds_assembly_and_test_flow(self):
        seed = gearbox_assembly_seed.build()

        metadata = seed.get('metadata', {})
        workbooks = seed['workbooks']
        biz_rows = workbooks['系统配置_模板.xlsx']['业务组织']
        supplier_rows = workbooks['工厂资源_模板.xlsx']['供应商']
        workcenter_rows = workbooks['工厂资源_模板.xlsx']['工作中心']
        route_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线']
        route_op_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序']
        order_rows = workbooks['生产订单_模板.xlsx']['生产订单']

        self.assertEqual(metadata.get('volume_profile'), '大体量版')
        self.assertEqual(sum(row.get('工厂组织类型') == '工厂' for row in biz_rows), 1)
        self.assertGreaterEqual(len(supplier_rows), 5)
        self.assertGreaterEqual(len(workcenter_rows), 10)
        self.assertGreaterEqual(len(route_rows), 2)
        self.assertGreaterEqual(len(route_op_rows), 20)
        self.assertTrue(order_rows)
        self.assertTrue(any('装配' in str(row.get('*名称', '')) for row in route_rows))
        self.assertTrue(any('试验' in str(row.get('*名称', '')) or '检测' in str(row.get('*名称', '')) for row in route_rows))
        self.assertFalse(any(row.get('*工序类型') == '厂际转工' for row in route_op_rows))

    def test_single_factory_machining_scheme_keeps_outsource_and_no_inter_factory_transfer(self):
        seed = gearbox_machining_seed.build()

        metadata = seed.get('metadata', {})
        workbooks = seed['workbooks']
        biz_rows = workbooks['系统配置_模板.xlsx']['业务组织']
        wc_supplier_rows = workbooks['工厂资源_模板.xlsx']['工作中心与供应商的关系']
        material_rows = workbooks['产品与工艺_模板.xlsx']['物料']
        route_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线']
        route_op_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序']

        self.assertEqual(metadata.get('volume_profile'), '大体量版')
        self.assertEqual(sum(row.get('工厂组织类型') == '工厂' for row in biz_rows), 1)
        self.assertGreaterEqual(len(material_rows), 12)
        self.assertGreaterEqual(len(route_rows), 3)
        self.assertGreaterEqual(len(route_op_rows), 30)
        self.assertTrue(wc_supplier_rows)
        self.assertTrue(any(row.get('*工序类型') == '外委' for row in route_op_rows))
        self.assertFalse(any(row.get('*工序类型') == '厂际转工' for row in route_op_rows))
        self.assertTrue(any('机加' in str(row.get('工艺专业', '')) for row in route_rows))
        self.assertTrue(any('装配' in str(row.get('工艺专业', '')) for row in route_rows))

    def test_multi_factory_scheme_removes_transfer_ops_and_keeps_total_assembly(self):
        seed = gearbox_multi_factory_seed.build()

        metadata = seed.get('metadata', {})
        workbooks = seed['workbooks']
        biz_rows = workbooks['系统配置_模板.xlsx']['业务组织']
        workcenter_rows = workbooks['工厂资源_模板.xlsx']['工作中心']
        process_rows = workbooks['工厂资源_模板.xlsx']['工序库']
        route_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线']
        route_op_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序']
        order_rows = workbooks['生产订单_模板.xlsx']['生产订单']

        self.assertEqual(metadata.get('volume_profile'), '大体量版')
        self.assertGreaterEqual(sum(row.get('工厂组织类型') == '工厂' for row in biz_rows), 4)
        self.assertGreaterEqual(len(workcenter_rows), 16)
        self.assertGreaterEqual(len(route_rows), 4)
        self.assertGreaterEqual(len(route_op_rows), 36)
        self.assertTrue(order_rows)
        self.assertFalse(any(row.get('*工序类型') in {'厂际转工', '厂内转工'} for row in route_op_rows))
        self.assertFalse(any(row.get('*工序类型') in {'厂际转工', '厂内转工'} for row in process_rows))
        self.assertTrue(any('总装' in str(row.get('*名称', '')) or '总成' in str(row.get('*名称', '')) for row in route_rows))

    def test_multi_factory_scheme_can_opt_in_project_collaboration_route_and_delivery_order(self):
        config = deepcopy(gearbox_multi_factory_seed.CONFIG)
        config['metadata']['project_collaboration'] = {
            'enabled': True,
            'admin': {
                'parent': 'ADM-GBX-HQ',
                'code': 'ADM-GBX-PROJ',
                'name': '生产项目部',
                'short': '项目部',
            },
            'biz': {
                'parent': 'BIZ-GBX-COMPANY',
                'code': 'BIZ-GBX-PROJ',
                'name': '生产项目部',
                'short': '项目部',
                'factory_type': '机械加工专业',
                'remark': '用于多工厂协同计划与一级工艺排产',
            },
            'route': {
                'code': 'RT-GBX-PROJ-A01',
                'name': '变速箱总成交付协同一级工艺',
                'material_code': 'MAT-GBX-GEARBOX-FIN',
                'spec': '通用',
                'remark': '项目部持单的一级协同工艺',
            },
            'phases': [
                {
                    'no': '0010',
                    'name': '箱体机加阶段完成',
                    'wc_code': 'WC-GBX-PROJ-HSG',
                    'wc_name': '箱体机加协同排产中心',
                    'content': '项目部按箱体机加工厂产能组织协同排产',
                    'op_spec': '机械加工专业',
                },
                {
                    'no': '0020',
                    'name': '齿轴机加阶段完成',
                    'wc_code': 'WC-GBX-PROJ-GEAR',
                    'wc_name': '齿轴机加协同排产中心',
                    'content': '项目部按齿轮轴系机加工厂产能组织协同排产',
                    'op_spec': '机械加工专业',
                },
                {
                    'no': '0030',
                    'name': '热处理阶段完成',
                    'wc_code': 'WC-GBX-PROJ-HT',
                    'wc_name': '热处理协同排产中心',
                    'content': '项目部按热处理工厂产能组织协同排产',
                    'op_spec': '机械加工专业',
                },
                {
                    'no': '0040',
                    'name': '交付放行',
                    'wc_code': 'WC-GBX-PROJ-REL',
                    'wc_name': '交付放行协同中心',
                    'content': '项目部完成零部件交付计划放行',
                    'op_type': '检验',
                    'wc_class': '检验',
                    'op_spec': '装配专业',
                },
            ],
        }

        seed = build_seed(config, gearbox_multi_factory_seed.SCENARIO, 'GBX99S01', '标准版')

        workbooks = seed['workbooks']
        biz_rows = workbooks['系统配置_模板.xlsx']['业务组织']
        workcenter_rows = workbooks['工厂资源_模板.xlsx']['工作中心']
        wc_user_rows = workbooks['工厂资源_模板.xlsx']['工作中心与用户关系']
        wc_eq_rows = workbooks['工厂资源_模板.xlsx']['工作中心与设备的关系']
        route_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线']
        route_op_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序']
        order_rows = workbooks['生产订单_模板.xlsx']['生产订单']

        project_biz = next((row for row in biz_rows if row.get('*名称') == '生产项目部'), None)
        self.assertIsNotNone(project_biz)
        self.assertEqual(project_biz.get('工厂组织类型'), '工厂')

        top_routes = [row for row in route_rows if row.get('*工艺类型') == '一级工艺']
        self.assertEqual(len(top_routes), 1)
        top_route = top_routes[0]
        self.assertEqual(top_route.get('*工厂组织'), project_biz.get('*编码'))

        project_wcs = [row for row in workcenter_rows if row.get('*工厂组织') == project_biz.get('*编码')]
        self.assertGreaterEqual(len(project_wcs), 4)
        self.assertTrue(all(row.get('*类型') == '组织' for row in project_wcs))

        project_wc_codes = {row.get('*编码') for row in project_wcs}
        self.assertFalse(any(rel.get('*工作中心编码') in project_wc_codes for rel in wc_user_rows))
        self.assertFalse(any(rel.get('*工作中心编码') in project_wc_codes for rel in wc_eq_rows))

        top_route_ops = [row for row in route_op_rows if row.get('*工艺路线编码') == top_route.get('*编码')]
        self.assertEqual(len(top_route_ops), 4)
        self.assertFalse(any(row.get('*工序类型') in {'厂际转工', '厂内转工'} for row in top_route_ops))

        top_orders = [row for row in order_rows if row.get('工艺路线编码') == top_route.get('*编码')]
        self.assertEqual(len(top_orders), 1)
        self.assertEqual(top_orders[0].get('订单类型'), '标准')
        self.assertEqual(top_orders[0].get('计划类型'), '零部件交付计划')
        self.assertEqual(top_orders[0].get('排产状态'), '零部件交付计划已排产')
        self.assertEqual(top_orders[0].get('*所属组织'), project_biz.get('*编码'))


if __name__ == '__main__':
    unittest.main()
