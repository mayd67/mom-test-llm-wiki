import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_turbofan_engine_seed as turbofan_seed


class TurbofanEngineSeedTests(unittest.TestCase):
    def test_build_generates_standard_generic_turbofan_seed(self):
        seed = turbofan_seed.build()

        metadata = seed.get('metadata', {})
        serialized = json.dumps(seed, ensure_ascii=False)
        route_rows = seed['workbooks']['产品与工艺_模板.xlsx']['工艺路线']
        material_rows = seed['workbooks']['产品与工艺_模板.xlsx']['物料']

        self.assertEqual(metadata.get('namespace'), 'TFAN9001')
        self.assertEqual(metadata.get('volume_profile'), '标准版')
        self.assertIn('涡扇', metadata.get('engine_model', ''))
        self.assertNotIn('LEAP-1B', serialized)
        self.assertNotIn('LEAP1B', serialized)
        self.assertNotIn('737发动机事业部', serialized)
        self.assertTrue(any('风扇' in str(row.get('*名称', '')) for row in route_rows))
        self.assertTrue(any('涡扇发动机' in str(row.get('*名称', '')) for row in material_rows))
        self.assertGreaterEqual(len(route_rows), 10)
        self.assertGreaterEqual(len(material_rows), 100)


if __name__ == '__main__':
    unittest.main()
