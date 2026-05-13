import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_transmission_shaft_seed as shaft_seed


class TransmissionShaftSeedTests(unittest.TestCase):
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

    def test_build_variants_cover_standard_and_ultra_profiles(self):
        standard = shaft_seed.build_variant(namespace='TS20S01', volume_profile='标准版')
        big = shaft_seed.build_variant(namespace='TS31S01', volume_profile='大体量版')
        ultra = shaft_seed.build_variant(namespace='TS42S01', volume_profile='超大体量版')

        self.assertEqual(standard.get('metadata', {}).get('namespace'), 'TS20S01')
        self.assertEqual(standard.get('metadata', {}).get('volume_profile'), '标准版')
        self.assertEqual(big.get('metadata', {}).get('namespace'), 'TS31S01')
        self.assertEqual(big.get('metadata', {}).get('volume_profile'), '大体量版')
        self.assertEqual(ultra.get('metadata', {}).get('namespace'), 'TS42S01')
        self.assertEqual(ultra.get('metadata', {}).get('volume_profile'), '超大体量版')

        std_counts = self.counts(standard)
        big_counts = self.counts(big)
        ultra_counts = self.counts(ultra)

        self.assertLess(std_counts['users'], big_counts['users'])
        self.assertLess(big_counts['users'], ultra_counts['users'])
        self.assertLess(std_counts['equipment'], big_counts['equipment'])
        self.assertLess(big_counts['equipment'], ultra_counts['equipment'])
        self.assertLess(std_counts['workcenters'], big_counts['workcenters'])
        self.assertLess(big_counts['workcenters'], ultra_counts['workcenters'])
        self.assertLess(std_counts['materials'], big_counts['materials'])
        self.assertLess(big_counts['materials'], ultra_counts['materials'])
        self.assertLess(std_counts['ops'], big_counts['ops'])
        self.assertLess(big_counts['ops'], ultra_counts['ops'])
        self.assertLess(std_counts['steps'], big_counts['steps'])
        self.assertLess(big_counts['steps'], ultra_counts['steps'])

    def test_build_generates_big_single_factory_seed_with_outsource_heat_treatment(self):
        seed = shaft_seed.build()

        metadata = seed.get('metadata', {})
        workbooks = seed['workbooks']
        biz_rows = workbooks['系统配置_模板.xlsx']['业务组织']
        user_rows = workbooks['系统配置_模板.xlsx']['用户']
        supplier_rows = workbooks['工厂资源_模板.xlsx']['供应商']
        equipment_rows = workbooks['工厂资源_模板.xlsx']['设备']
        workcenter_rows = workbooks['工厂资源_模板.xlsx']['工作中心']
        wc_supplier_rows = workbooks['工厂资源_模板.xlsx']['工作中心与供应商的关系']
        material_rows = workbooks['产品与工艺_模板.xlsx']['物料']
        route_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线']
        route_op_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序']
        route_step_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工步']
        route_seq_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序序列']
        order_rows = workbooks['生产订单_模板.xlsx']['生产订单']

        self.assertEqual(metadata.get('volume_profile'), '大体量版')
        self.assertEqual(metadata.get('namespace'), 'TS31S01')
        self.assertEqual(sum(row.get('工厂组织类型') == '工厂' for row in biz_rows), 1)

        self.assertGreaterEqual(len(user_rows), 80)
        self.assertGreaterEqual(len(equipment_rows), 20)
        self.assertGreaterEqual(len(workcenter_rows), 18)
        self.assertGreaterEqual(len(material_rows), 18)
        self.assertGreaterEqual(len(route_rows), 1)
        self.assertGreaterEqual(len(route_op_rows), 28)
        self.assertGreaterEqual(len(route_step_rows), 56)
        self.assertGreaterEqual(len(order_rows), 1)

        self.assertTrue(supplier_rows)
        self.assertTrue(wc_supplier_rows)
        self.assertTrue(any(row.get('*类型') == '外委' for row in workcenter_rows))
        self.assertTrue(any(row.get('*工序类型') == '外委' for row in route_op_rows))
        self.assertFalse(any(row.get('*工序类型') == '厂际转工' for row in route_op_rows))
        self.assertTrue(route_seq_rows)
        self.assertTrue(all(row.get('*接续关系') == 'ES' for row in route_seq_rows))

        operator_count = sum('操作工' in str(row.get('备注', '')) for row in user_rows)
        self.assertGreaterEqual(operator_count, 40)


if __name__ == '__main__':
    unittest.main()
