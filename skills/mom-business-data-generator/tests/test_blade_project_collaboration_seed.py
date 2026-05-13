import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_blade_project_collaboration_seed as blade_seed


class BladeProjectCollaborationSeedTests(unittest.TestCase):
    def test_build_generates_project_collaboration_blade_seed_with_short_codes(self):
        seed = blade_seed.build()

        metadata = seed.get('metadata', {})
        workbooks = seed['workbooks']
        biz_rows = workbooks['系统配置_模板.xlsx']['业务组织']
        supplier_rows = workbooks['工厂资源_模板.xlsx']['供应商']
        equipment_rows = workbooks['工厂资源_模板.xlsx']['设备']
        tooling_rows = workbooks['工厂资源_模板.xlsx']['工装工具']
        warehouse_rows = workbooks['工厂资源_模板.xlsx']['库房']
        location_rows = workbooks['工厂资源_模板.xlsx']['库位']
        workcenter_rows = workbooks['工厂资源_模板.xlsx']['工作中心']
        wc_user_rows = workbooks['工厂资源_模板.xlsx']['工作中心与用户关系']
        wc_eq_rows = workbooks['工厂资源_模板.xlsx']['工作中心与设备的关系']
        material_rows = workbooks['产品与工艺_模板.xlsx']['物料']
        route_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线']
        route_op_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序']
        order_rows = workbooks['生产订单_模板.xlsx']['生产订单']

        self.assertEqual(metadata.get('volume_profile'), '标准版')
        self.assertEqual(metadata.get('namespace'), 'BLD20S01')
        self.assertEqual(metadata.get('product_model'), 'BL-1001高压涡轮叶片')

        self.assertGreaterEqual(len(supplier_rows), 6)
        self.assertGreaterEqual(len(equipment_rows), 25)
        self.assertGreaterEqual(len(tooling_rows), 12)
        self.assertGreaterEqual(len(warehouse_rows), 6)
        self.assertGreaterEqual(len(location_rows), 24)
        self.assertGreaterEqual(len(workcenter_rows), 19)
        self.assertGreaterEqual(len(material_rows), 22)
        self.assertEqual(len(route_rows), 5)
        self.assertEqual(len(order_rows), 5)

        self.assertFalse(any(row.get('*工序类型') in {'外委', '厂内转工', '厂际转工'} for row in route_op_rows))

        biz_type_map = {
            str(row.get('*编码', '')).strip(): str(row.get('工厂组织类型', '')).strip()
            for row in biz_rows
        }
        biz_parent_map = {
            str(row.get('*编码', '')).strip(): str(row.get('*父组织编码', '')).strip()
            for row in biz_rows
        }
        for sheet_name in ('库房', '库位'):
            for row in workbooks['工厂资源_模板.xlsx'][sheet_name]:
                self.assertEqual(biz_type_map.get(row.get('*工厂组织')), '工厂')

        project_biz = next((row for row in biz_rows if row.get('*名称') == '生产项目部'), None)
        self.assertIsNotNone(project_biz)
        self.assertEqual(project_biz.get('工厂组织类型'), '工厂')
        self.assertEqual(project_biz.get('工厂类型'), '装配专业')

        assembly_factory = next((row for row in biz_rows if row.get('*名称') == '装配交付工厂'), None)
        self.assertIsNotNone(assembly_factory)
        self.assertEqual(assembly_factory.get('工厂组织类型'), '工厂')
        self.assertEqual(assembly_factory.get('工厂类型'), '装配专业')

        top_routes = [row for row in route_rows if row.get('*工艺类型') == '一级工艺']
        self.assertEqual(len(top_routes), 1)
        top_route = top_routes[0]
        self.assertEqual(top_route.get('*工厂组织'), project_biz.get('*编码'))

        project_wcs = [row for row in workcenter_rows if row.get('*工厂组织') == project_biz.get('*编码')]
        self.assertEqual(len(project_wcs), 5)
        self.assertTrue(all(row.get('*类型') == '组织' for row in project_wcs))

        project_wc_codes = {row.get('*编码') for row in project_wcs}
        self.assertFalse(any(rel.get('*工作中心编码') in project_wc_codes for rel in wc_user_rows))
        self.assertFalse(any(rel.get('*工作中心编码') in project_wc_codes for rel in wc_eq_rows))

        top_route_ops = [row for row in route_op_rows if row.get('*工艺路线编码') == top_route.get('*编码')]
        self.assertEqual(len(top_route_ops), 5)
        self.assertFalse(any(row.get('*工序类型') in {'厂际转工', '厂内转工'} for row in top_route_ops))
        self.assertTrue(any(row.get('工序专业类型') == '装配专业' for row in top_route_ops))

        top_orders = [row for row in order_rows if row.get('工艺路线编码') == top_route.get('*编码')]
        self.assertEqual(len(top_orders), 1)
        self.assertEqual(top_orders[0].get('订单类型'), '标准')
        self.assertEqual(top_orders[0].get('计划类型'), '零部件交付计划')
        self.assertEqual(top_orders[0].get('排产状态'), '零部件交付计划已排产')
        self.assertEqual(top_orders[0].get('*所属组织'), project_biz.get('*编码'))

        assembly_routes = [row for row in route_rows if row.get('*工厂组织') == assembly_factory.get('*编码')]
        self.assertEqual(len(assembly_routes), 1)
        self.assertEqual(assembly_routes[0].get('工艺专业'), '装配')

        assembly_org_codes = {assembly_factory.get('*编码')}
        changed = True
        while changed:
            changed = False
            for code, parent in biz_parent_map.items():
                if parent in assembly_org_codes and code not in assembly_org_codes:
                    assembly_org_codes.add(code)
                    changed = True

        assembly_wcs = [row for row in workcenter_rows if row.get('*工厂组织') in assembly_org_codes]
        self.assertGreaterEqual(len(assembly_wcs), 2)
        assembly_wc_codes = {row.get('*编码') for row in assembly_wcs}
        self.assertTrue(any(rel.get('*工作中心编码') in assembly_wc_codes for rel in wc_user_rows))
        self.assertTrue(any(rel.get('*工作中心编码') in assembly_wc_codes for rel in wc_eq_rows))

        assembly_ops = [
            row for row in route_op_rows
            if row.get('*工艺路线编码') == assembly_routes[0].get('*编码')
        ]
        self.assertEqual(len(assembly_ops), 2)
        self.assertTrue(all(row.get('工序专业类型') == '装配专业' for row in assembly_ops))

        self.assertTrue(all(re.fullmatch(r'Eq\d{3}', str(row.get('*编码', ''))) for row in equipment_rows))
        self.assertTrue(all(re.fullmatch(r'Wh\d{3}', str(row.get('*编码', ''))) for row in warehouse_rows))
        self.assertTrue(all(re.fullmatch(r'Loc\d{3}', str(row.get('*编码', ''))) for row in location_rows))
        self.assertTrue(all(re.fullmatch(r'Mat\d{3}', str(row.get('*编码', ''))) for row in material_rows))
        self.assertTrue(all(re.fullmatch(r'Wc\d{3}', str(row.get('*编码', ''))) for row in workcenter_rows))


if __name__ == '__main__':
    unittest.main()
