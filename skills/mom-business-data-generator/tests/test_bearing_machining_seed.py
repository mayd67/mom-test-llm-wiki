import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_bearing_machining_seed as bearing_seed


class BearingMachiningSeedTests(unittest.TestCase):
    def test_build_generates_professional_standard_bearing_machining_seed_with_short_codes(self):
        seed = bearing_seed.build()

        metadata = seed.get('metadata', {})
        workbooks = seed['workbooks']
        biz_rows = workbooks['系统配置_模板.xlsx']['业务组织']
        supplier_rows = workbooks['工厂资源_模板.xlsx']['供应商']
        equipment_rows = workbooks['工厂资源_模板.xlsx']['设备']
        tooling_rows = workbooks['工厂资源_模板.xlsx']['工装工具']
        warehouse_rows = workbooks['工厂资源_模板.xlsx']['库房']
        location_rows = workbooks['工厂资源_模板.xlsx']['库位']
        workcenter_rows = workbooks['工厂资源_模板.xlsx']['工作中心']
        material_rows = workbooks['产品与工艺_模板.xlsx']['物料']
        route_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线']
        route_op_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序']
        order_rows = workbooks['生产订单_模板.xlsx']['生产订单']

        self.assertEqual(metadata.get('volume_profile'), '标准版')
        self.assertEqual(metadata.get('namespace'), 'BRG20S01')
        self.assertEqual(metadata.get('product_model'), '6206深沟球轴承外圈')
        self.assertEqual(sum(row.get('工厂组织类型') == '工厂' for row in biz_rows), 1)

        self.assertGreaterEqual(len(supplier_rows), 5)
        self.assertGreaterEqual(len(equipment_rows), 20)
        self.assertGreaterEqual(len(tooling_rows), 12)
        self.assertGreaterEqual(len(warehouse_rows), 5)
        self.assertGreaterEqual(len(location_rows), 20)
        self.assertGreaterEqual(len(workcenter_rows), 8)
        self.assertGreaterEqual(len(material_rows), 20)
        self.assertEqual(len(route_rows), 1)
        self.assertEqual(len(route_op_rows), 5)
        self.assertTrue(order_rows)

        self.assertFalse(any(row.get('*类型') == '外委' for row in workcenter_rows))
        self.assertFalse(any(row.get('*工序类型') == '外委' for row in route_op_rows))
        self.assertFalse(any(row.get('*工序类型') == '厂际转工' for row in route_op_rows))

        biz_type_map = {
            str(row.get('*编码', '')).strip(): str(row.get('工厂组织类型', '')).strip()
            for row in biz_rows
        }
        for sheet_name in ('库房', '库位'):
            for row in workbooks['工厂资源_模板.xlsx'][sheet_name]:
                self.assertEqual(biz_type_map.get(row.get('*工厂组织')), '工厂')

        self.assertTrue(all(re.fullmatch(r'Eq\d{3}', str(row.get('*编码', ''))) for row in equipment_rows))
        self.assertTrue(all(re.fullmatch(r'Wh\d{3}', str(row.get('*编码', ''))) for row in warehouse_rows))
        self.assertTrue(all(re.fullmatch(r'Loc\d{3}', str(row.get('*编码', ''))) for row in location_rows))
        self.assertTrue(all(re.fullmatch(r'Mat\d{3}', str(row.get('*编码', ''))) for row in material_rows))
        self.assertTrue(all(re.fullmatch(r'Wc\d{3}', str(row.get('*编码', ''))) for row in workcenter_rows))


if __name__ == '__main__':
    unittest.main()
