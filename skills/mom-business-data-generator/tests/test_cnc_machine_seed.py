import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_cnc_machine_seed as cnc_seed


class CncMachineSeedTests(unittest.TestCase):
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

    def test_build_variants_cover_standard_big_and_ultra_profiles(self):
        standard = cnc_seed.build_variant(namespace='CNC85001', volume_profile='标准版')
        big = cnc_seed.build_variant(namespace='CNC85031', volume_profile='大体量版')
        ultra = cnc_seed.build_variant(namespace='CNC85042', volume_profile='超大体量版')

        self.assertEqual(standard.get('metadata', {}).get('namespace'), 'CNC85001')
        self.assertEqual(standard.get('metadata', {}).get('volume_profile'), '标准版')
        self.assertEqual(big.get('metadata', {}).get('namespace'), 'CNC85031')
        self.assertEqual(big.get('metadata', {}).get('volume_profile'), '大体量版')
        self.assertEqual(ultra.get('metadata', {}).get('namespace'), 'CNC85042')
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

    def test_build_keeps_standard_variant_as_default(self):
        seed = cnc_seed.build()

        metadata = seed.get('metadata', {})
        workbooks = seed['workbooks']
        workcenter_rows = workbooks['工厂资源_模板.xlsx']['工作中心']
        supplier_link_rows = workbooks['工厂资源_模板.xlsx']['工作中心与供应商的关系']

        self.assertEqual(metadata.get('namespace'), 'CNC85001')
        self.assertEqual(metadata.get('volume_profile'), '标准版')
        self.assertGreaterEqual(len(workbooks['系统配置_模板.xlsx']['用户']), 120)
        self.assertGreaterEqual(len(workbooks['工厂资源_模板.xlsx']['设备']), 20)
        self.assertGreaterEqual(len(workcenter_rows), 18)
        self.assertGreaterEqual(len(workbooks['产品与工艺_模板.xlsx']['物料']), 100)
        self.assertGreaterEqual(len(workbooks['产品与工艺_模板.xlsx']['工艺路线工序']), 100)
        self.assertGreaterEqual(len(workbooks['产品与工艺_模板.xlsx']['工艺路线工步']), 200)
        self.assertFalse(supplier_link_rows)
        self.assertFalse(any(row.get('*类型') == '外委' for row in workcenter_rows))


if __name__ == '__main__':
    unittest.main()
