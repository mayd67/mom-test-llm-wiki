import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_fuel_pump_assembly_seed as fuel_pump_seed
import build_gearbox_multi_factory_seed as gearbox_multi_factory_seed
import build_transmission_shaft_seed as shaft_seed


class StorageFactoryOrgRuleTests(unittest.TestCase):
    def assert_storage_orgs_are_plants(self, seed: dict) -> None:
        workbooks = seed['workbooks']
        biz_rows = workbooks['系统配置_模板.xlsx']['业务组织']
        biz_type_map = {
            str(row.get('*编码', '')).strip(): str(row.get('工厂组织类型', '')).strip()
            for row in biz_rows
        }
        factory_rows = workbooks['工厂资源_模板.xlsx']
        for sheet_name in ('库房', '库位'):
            rows = factory_rows[sheet_name]
            self.assertTrue(rows, msg=f'{sheet_name} 不应为空')
            for row in rows:
                factory_org = str(row.get('*工厂组织', '')).strip()
                self.assertTrue(factory_org, msg=f'{sheet_name} 存在空的 *工厂组织: {row}')
                self.assertEqual(
                    biz_type_map.get(factory_org),
                    '工厂',
                    msg=f'{sheet_name} 的 *工厂组织 必须是工厂级组织: {row}',
                )

    def test_fuel_pump_storage_orgs_point_to_plant(self):
        self.assert_storage_orgs_are_plants(fuel_pump_seed.build())

    def test_transmission_shaft_storage_orgs_point_to_plant(self):
        self.assert_storage_orgs_are_plants(shaft_seed.build())

    def test_multi_factory_storage_orgs_point_to_each_plant(self):
        seed = gearbox_multi_factory_seed.build()
        self.assert_storage_orgs_are_plants(seed)
        rows = seed['workbooks']['工厂资源_模板.xlsx']['库房']
        plant_codes = {str(row.get('*工厂组织', '')).strip() for row in rows}
        self.assertGreaterEqual(len(plant_codes), 2)


if __name__ == '__main__':
    unittest.main()
