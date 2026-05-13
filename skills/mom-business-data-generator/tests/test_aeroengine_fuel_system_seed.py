import re
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_aeroengine_fuel_system_seed as fuel_system_seed


class AeroengineFuelSystemSeedTests(unittest.TestCase):
    def test_build_generates_dense_multi_factory_seed_with_sections_and_teams(self):
        seed = fuel_system_seed.build()

        metadata = seed.get('metadata', {})
        workbooks = seed['workbooks']
        biz_rows = workbooks['系统配置_模板.xlsx']['业务组织']
        user_rows = workbooks['系统配置_模板.xlsx']['用户']
        workcenter_rows = workbooks['工厂资源_模板.xlsx']['工作中心']
        warehouse_rows = workbooks['工厂资源_模板.xlsx']['库房']
        location_rows = workbooks['工厂资源_模板.xlsx']['库位']
        route_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线']
        route_op_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序']
        material_rows = workbooks['产品与工艺_模板.xlsx']['物料']
        mbom_rows = workbooks['产品与工艺_模板.xlsx']['MBOM']
        mbom_node_rows = workbooks['产品与工艺_模板.xlsx']['MBOM节点']
        order_rows = workbooks['生产订单_模板.xlsx']['生产订单']

        self.assertEqual(metadata.get('volume_profile'), '标准版')
        self.assertEqual(metadata.get('namespace'), 'AFS20S01')
        self.assertEqual(metadata.get('product_model'), 'AFS-900航发燃油系统总成')

        org_type_counts = Counter(str(row.get('工厂组织类型', '')).strip() for row in biz_rows)
        self.assertGreaterEqual(org_type_counts['工厂'], 6)
        self.assertGreaterEqual(org_type_counts['车间'], 5)
        self.assertGreaterEqual(org_type_counts['工段'], 10)
        self.assertGreaterEqual(org_type_counts['班组'], 10)

        self.assertGreaterEqual(len(workcenter_rows), 20)
        self.assertGreaterEqual(len(material_rows), 700)
        self.assertGreaterEqual(len(mbom_rows), 120)
        self.assertEqual(len(route_rows), 6)
        self.assertEqual(len(order_rows), 6)

        production_biz = next((row for row in biz_rows if row.get('*名称') == '生产部' and row.get('工厂组织类型') == '工厂'), None)
        self.assertIsNotNone(production_biz)

        top_routes = [row for row in route_rows if row.get('*工艺类型') == '一级工艺']
        self.assertEqual(len(top_routes), 1)
        top_route = top_routes[0]
        self.assertEqual(top_route.get('*工厂组织'), production_biz.get('*编码'))

        top_route_ops = [row for row in route_op_rows if row.get('*工艺路线编码') == top_route.get('*编码')]
        self.assertEqual(len(top_route_ops), 5)
        self.assertTrue(any('铸造' in str(row.get('*工序名称', '')) for row in top_route_ops))
        self.assertTrue(any('机加工' in str(row.get('*工序名称', '')) for row in top_route_ops))
        self.assertTrue(any('热处理' in str(row.get('*工序名称', '')) for row in top_route_ops))
        self.assertTrue(any('总装' in str(row.get('*工序名称', '')) for row in top_route_ops))
        self.assertTrue(any('试车' in str(row.get('*工序名称', '')) for row in top_route_ops))
        self.assertFalse(any(row.get('*工序类型') in {'外委', '厂内转工', '厂际转工'} for row in route_op_rows))

        top_orders = [row for row in order_rows if row.get('工艺路线编码') == top_route.get('*编码')]
        self.assertEqual(len(top_orders), 1)
        self.assertEqual(top_orders[0].get('计划类型'), '零部件交付计划')
        self.assertEqual(top_orders[0].get('排产状态'), '零部件交付计划已排产')
        self.assertEqual(top_orders[0].get('*所属组织'), production_biz.get('*编码'))

        level_counts = Counter(int(row.get('*层级')) for row in mbom_node_rows)
        self.assertGreaterEqual(level_counts[0], 100)
        self.assertGreaterEqual(level_counts[1], 100)
        self.assertGreaterEqual(level_counts[2], 100)

        biz_type_map = {
            str(row.get('*编码', '')).strip(): str(row.get('工厂组织类型', '')).strip()
            for row in biz_rows
        }
        for sheet_name in ('库房', '库位'):
            for row in workbooks['工厂资源_模板.xlsx'][sheet_name]:
                self.assertEqual(biz_type_map.get(row.get('*工厂组织')), '工厂')

        self.assertTrue(all(re.fullmatch(r'Biz\d{3}', str(row.get('*编码', ''))) for row in biz_rows))
        self.assertTrue(all(re.fullmatch(r'Wc\d{3}', str(row.get('*编码', ''))) for row in workcenter_rows))
        self.assertTrue(all(re.fullmatch(r'Wh\d{3}', str(row.get('*编码', ''))) for row in warehouse_rows))
        self.assertTrue(all(re.fullmatch(r'Loc\d{3}', str(row.get('*编码', ''))) for row in location_rows))
        self.assertTrue(all(re.fullmatch(r'Mat\d{3}', str(row.get('*编码', ''))) for row in material_rows))
        self.assertTrue(all(re.fullmatch(r'Rt\d{3}', str(row.get('*编码', ''))) for row in route_rows))
        self.assertTrue(all(re.fullmatch(r'Mb\d{3}', str(row.get('*编码', ''))) for row in mbom_rows))
        self.assertTrue(all(re.fullmatch(r'U\d{3}', str(row.get('*编号', ''))) for row in user_rows))
        self.assertTrue(all(re.fullmatch(r'Mo\d{3}', str(row.get('*编码', ''))) for row in order_rows))


if __name__ == '__main__':
    unittest.main()
