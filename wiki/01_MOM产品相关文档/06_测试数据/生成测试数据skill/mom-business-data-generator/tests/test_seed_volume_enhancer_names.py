import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import seed_volume_enhancer as enhancer


class SeedVolumeEnhancerNameTests(unittest.TestCase):
    def test_early_generated_names_use_diverse_given_names(self):
        male_names = [enhancer._unique_name(index, '男') for index in range(20)]
        female_names = [enhancer._unique_name(index, '女') for index in range(20)]

        male_given_names = {name[1:] for name in male_names}
        female_given_names = {name[1:] for name in female_names}

        self.assertEqual(len(male_names), len(set(male_names)))
        self.assertEqual(len(female_names), len(set(female_names)))
        self.assertGreaterEqual(len(male_given_names), 8)
        self.assertGreaterEqual(len(female_given_names), 8)

    def test_gender_specific_name_pools_are_distinct(self):
        male_given_names = {enhancer._unique_name(index, '男')[1:] for index in range(12)}
        female_given_names = {enhancer._unique_name(index, '女')[1:] for index in range(12)}

        self.assertNotEqual(male_given_names, female_given_names)


if __name__ == '__main__':
    unittest.main()
