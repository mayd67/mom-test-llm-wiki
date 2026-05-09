import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_turbofan_engine_seed as turbofan_seed
import build_turbojet_engine_seed as turbojet_seed


class TurbojetEngineSeedTests(unittest.TestCase):
    def test_build_generates_standard_turbojet_seed_without_fan_chain(self):
        turbojet = turbojet_seed.build()
        turbofan = turbofan_seed.build()

        metadata = turbojet.get('metadata', {})
        serialized = json.dumps(turbojet, ensure_ascii=False)
        route_rows = turbojet['workbooks']['产品与工艺_模板.xlsx']['工艺路线']
        material_rows = turbojet['workbooks']['产品与工艺_模板.xlsx']['物料']

        self.assertEqual(metadata.get('namespace'), 'TJET9001')
        self.assertEqual(metadata.get('volume_profile'), '标准版')
        self.assertIn('涡喷', metadata.get('engine_model', ''))
        self.assertNotIn('风扇', serialized)
        self.assertNotIn('-FAN', serialized)
        self.assertTrue(any('涡喷发动机' in str(row.get('*名称', '')) for row in material_rows))
        self.assertLess(len(route_rows), len(turbofan['workbooks']['产品与工艺_模板.xlsx']['工艺路线']))
        self.assertLess(len(material_rows), len(turbofan['workbooks']['产品与工艺_模板.xlsx']['物料']))
        self.assertGreaterEqual(len(route_rows), 8)
        self.assertGreaterEqual(len(material_rows), 70)


if __name__ == '__main__':
    unittest.main()
