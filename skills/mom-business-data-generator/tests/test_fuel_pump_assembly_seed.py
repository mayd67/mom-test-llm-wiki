import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_fuel_pump_assembly_seed as fuel_pump_seed


class FuelPumpAssemblySeedTests(unittest.TestCase):
    def test_build_generates_simple_single_factory_standard_seed_without_outsource(self):
        seed = fuel_pump_seed.build()

        metadata = seed.get('metadata', {})
        workbooks = seed['workbooks']
        biz_rows = workbooks['系统配置_模板.xlsx']['业务组织']
        supplier_rows = workbooks['工厂资源_模板.xlsx']['供应商']
        workcenter_rows = workbooks['工厂资源_模板.xlsx']['工作中心']
        route_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线']
        route_op_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序']
        route_seq_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序序列']
        order_rows = workbooks['生产订单_模板.xlsx']['生产订单']

        self.assertEqual(metadata.get('volume_profile'), '标准版')
        self.assertEqual(sum(row.get('工厂组织类型') == '工厂' for row in biz_rows), 1)
        self.assertFalse(supplier_rows)
        self.assertGreaterEqual(len(workcenter_rows), 5)
        self.assertGreaterEqual(len(route_rows), 1)
        self.assertLessEqual(len(route_rows), 2)
        self.assertGreaterEqual(len(route_op_rows), 4)
        self.assertLessEqual(len(route_op_rows), 12)
        self.assertTrue(order_rows)
        self.assertFalse(any(row.get('*类型') == '外委' for row in workcenter_rows))
        self.assertFalse(any(row.get('*工序类型') == '外委' for row in route_op_rows))
        self.assertFalse(any(row.get('*工序类型') == '厂际转工' for row in route_op_rows))
        self.assertTrue(route_seq_rows)
        self.assertTrue(all(row.get('*接续关系') == 'ES' for row in route_seq_rows))
        self.assertTrue(any('装配' in str(row.get('*名称', '')) for row in route_rows))


if __name__ == '__main__':
    unittest.main()
