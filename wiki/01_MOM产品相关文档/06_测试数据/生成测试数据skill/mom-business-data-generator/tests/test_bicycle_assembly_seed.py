import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_bicycle_assembly_seed as bicycle_seed


class BicycleAssemblySeedTests(unittest.TestCase):
    def test_build_generates_single_factory_bicycle_assembly_seed_without_outsource(self):
        seed = bicycle_seed.build()

        metadata = seed.get('metadata', {})
        workbooks = seed['workbooks']
        biz_rows = workbooks['系统配置_模板.xlsx']['业务组织']
        user_rows = workbooks['系统配置_模板.xlsx']['用户']
        warehouse_rows = workbooks['工厂资源_模板.xlsx']['库房']
        location_rows = workbooks['工厂资源_模板.xlsx']['库位']
        supplier_rows = workbooks['工厂资源_模板.xlsx']['供应商']
        workcenter_rows = workbooks['工厂资源_模板.xlsx']['工作中心']
        route_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线']
        route_op_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序']
        route_seq_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序序列']
        mbom_node_rows = workbooks['产品与工艺_模板.xlsx']['MBOM节点']
        order_rows = workbooks['生产订单_模板.xlsx']['生产订单']
        plant_codes = [row.get('*编码') for row in biz_rows if row.get('工厂组织类型') == '工厂']

        self.assertEqual(metadata.get('volume_profile'), '标准版')
        self.assertEqual(len(plant_codes), 1)
        self.assertFalse(supplier_rows)
        self.assertEqual([row.get('*编号') for row in user_rows], [str(i) for i in range(100, 100 + len(user_rows))])
        self.assertGreaterEqual(len(workcenter_rows), 5)
        self.assertGreaterEqual(len(route_rows), 1)
        self.assertGreaterEqual(len(route_op_rows), 6)
        self.assertTrue(order_rows)
        self.assertTrue(route_seq_rows)
        self.assertTrue(all(row.get('*接续关系') == 'ES' for row in route_seq_rows))
        self.assertFalse(any(row.get('*类型') == '外委' for row in workcenter_rows))
        self.assertFalse(any(row.get('*工序类型') == '外委' for row in route_op_rows))
        self.assertFalse(any(row.get('*工序类型') == '厂际转工' for row in route_op_rows))
        self.assertTrue(any('自行车' in str(row.get('*名称', '')) for row in route_rows))
        self.assertTrue(all(row.get('*工厂组织') == plant_codes[0] for row in warehouse_rows))
        self.assertTrue(all(row.get('*工厂组织') == plant_codes[0] for row in location_rows))
        self.assertGreaterEqual(max(int(row.get('*层级', 0)) for row in mbom_node_rows), 2)
        self.assertTrue(any(row.get('父物料编码', '').endswith('WHEEL-F') for row in mbom_node_rows if int(row.get('*层级', 0)) == 2))

    def test_build_keeps_core_codes_compact(self):
        seed = bicycle_seed.build()
        workbooks = seed['workbooks']

        admin_codes = [row.get('*编码', '') for row in workbooks['系统配置_模板.xlsx']['行政组织']]
        biz_codes = [row.get('*编码', '') for row in workbooks['系统配置_模板.xlsx']['业务组织']]
        workcenter_codes = [row.get('*编码', '') for row in workbooks['工厂资源_模板.xlsx']['工作中心']]
        material_codes = [row.get('*编码', '') for row in workbooks['产品与工艺_模板.xlsx']['物料']]

        for codes in (admin_codes, biz_codes, workcenter_codes, material_codes):
            self.assertTrue(codes)
            self.assertTrue(all('BCA20S01' not in str(code) for code in codes))

        self.assertIn('ADM-BCA-HQ', admin_codes)
        self.assertIn('BIZ-BCA-PLANT', biz_codes)
        self.assertIn('WC-BCA-KIT', workcenter_codes)
        self.assertIn('MAT-BCA-BIKE-FIN', material_codes)


if __name__ == '__main__':
    unittest.main()

