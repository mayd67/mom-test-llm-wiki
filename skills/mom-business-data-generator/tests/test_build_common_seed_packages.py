import json
import gc
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_common_seed_packages as batch_builder
import generate_seed_workbooks as workbook_builder


class BuildCommonSeedPackagesTests(unittest.TestCase):
    def test_registry_includes_common_standard_scenarios(self):
        scenarios = batch_builder.scenario_registry()

        self.assertIn('bearing_machining_standard', scenarios)
        self.assertIn('bicycle_assembly_standard', scenarios)
        self.assertIn('fuel_pump_assembly_standard', scenarios)
        self.assertIn('gearbox_assembly_standard', scenarios)
        self.assertIn('gearbox_machining_assembly_standard', scenarios)
        self.assertIn('gearbox_multi_factory_standard', scenarios)
        self.assertIn('mom_promo_video_standard', scenarios)
        self.assertIn('blade_project_collaboration_standard', scenarios)

        blade = scenarios['blade_project_collaboration_standard']
        self.assertEqual(blade.module_name, 'build_blade_project_collaboration_seed')
        self.assertEqual(blade.output_parts[0], '高压涡轮叶片（BL-1001）')
        self.assertEqual(blade.output_parts[1], '多工厂协同-项目部一级工艺版')

        promo = scenarios['mom_promo_video_standard']
        self.assertEqual(promo.module_name, 'build_mom_promo_video_seed')
        self.assertEqual(promo.output_parts[0], '自动变速箱总成（8AT480）')
        self.assertEqual(promo.output_parts[1], 'MOM宣传视频综合演示-标准版')

    def test_resolve_paths_prefers_internal_templates_dir(self):
        template_dir, output_root = batch_builder._resolve_paths()

        self.assertEqual(template_dir, ROOT / 'templates')
        self.assertEqual(output_root, ROOT.parents[1] / 'outputs' / '06_测试数据')

    def test_find_template_dir_prefers_nested_templates_folder(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            skill_dir = workspace / 'mom-template-seed-generator'
            nested_templates = skill_dir / 'templates'
            nested_templates.mkdir(parents=True, exist_ok=True)
            for workbook_name in workbook_builder.TEMPLATE_FILES:
                (workspace / workbook_name).write_bytes(b'root')
                (nested_templates / workbook_name).write_bytes(b'nested')

            self.assertEqual(workbook_builder.find_template_dir(skill_dir), nested_templates)
            self.assertEqual(workbook_builder.default_output_root_for_template_dir(nested_templates), workspace / 'output')

    def test_build_packages_can_generate_single_blade_package(self):
        template_dir = ROOT / 'templates'
        with tempfile.TemporaryDirectory() as temp_dir:
            results = batch_builder.build_packages(
                scenario_keys=['blade_project_collaboration_standard'],
                template_dir=template_dir,
                output_root=Path(temp_dir),
            )

            self.assertEqual(len(results), 1)
            result = results[0]
            self.assertEqual(result['scenario_key'], 'blade_project_collaboration_standard')
            self.assertTrue(result['asset_path'].exists())
            self.assertTrue(result['output_dir'].exists())
            generated_files = {item.name for item in result['output_dir'].iterdir() if item.is_file()}
            self.assertTrue(set(workbook_builder.TEMPLATE_FILES).issubset(generated_files))
            self.assertIn('种子概览.json', generated_files)
            gc.collect()

    def test_build_packages_can_generate_single_promo_video_package(self):
        template_dir = ROOT / 'templates'
        with tempfile.TemporaryDirectory() as temp_dir:
            results = batch_builder.build_packages(
                scenario_keys=['mom_promo_video_standard'],
                template_dir=template_dir,
                output_root=Path(temp_dir),
            )

            self.assertEqual(len(results), 1)
            result = results[0]
            self.assertEqual(result['scenario_key'], 'mom_promo_video_standard')
            self.assertTrue(result['asset_path'].exists())
            self.assertTrue(result['output_dir'].exists())
            generated_files = {item.name for item in result['output_dir'].iterdir() if item.is_file()}
            self.assertTrue(set(workbook_builder.TEMPLATE_FILES).issubset(generated_files))
            self.assertIn('种子概览.json', generated_files)
            gc.collect()

    def test_build_packages_aligns_legacy_seed_fields_to_latest_templates(self):
        template_dir = ROOT / 'templates'
        with tempfile.TemporaryDirectory() as temp_dir:
            results = batch_builder.build_packages(
                scenario_keys=['bicycle_assembly_standard'],
                template_dir=template_dir,
                output_root=Path(temp_dir),
            )

            seed = json.loads(results[0]['asset_path'].read_text(encoding='utf-8-sig'))
            workbooks = seed['workbooks']
            system = workbooks[workbook_builder.WB_SYSTEM]
            factory = workbooks[workbook_builder.WB_FACTORY]
            product = workbooks[workbook_builder.WB_PRODUCT]

            admin_row = system[workbook_builder.SH_ADMIN][0]
            user_row = system[workbook_builder.SH_USER][0]
            warehouse_row = factory[workbook_builder.SH_WAREHOUSE][0]
            process_row = factory[workbook_builder.SH_PROCESS_LIB][0]
            tooling_row = factory[workbook_builder.SH_TOOLING][0]
            material_row = product[workbook_builder.SH_MATERIAL][0]
            mbom_node_row = product[workbook_builder.SH_MBOM_NODE][0]

            self.assertIn('*密级', admin_row)
            self.assertIn('*名称', user_row)
            self.assertIn('*用户安全等级', user_row)
            self.assertNotIn('名称', user_row)
            self.assertNotIn('用户安全等级', user_row)
            self.assertIn('*作业模式', warehouse_row)
            self.assertNotIn('作业模式', warehouse_row)
            self.assertIn('工序专业类型', process_row)
            self.assertNotIn('序专业类型', process_row)
            self.assertNotIn('发布版本时间', tooling_row)
            self.assertNotIn('发布人', tooling_row)
            self.assertNotIn('发布版本时间', material_row)
            self.assertNotIn('发布人', material_row)
            self.assertIn('*MBom版本号', mbom_node_row)
            self.assertIn('*MBom编码', mbom_node_row)
            self.assertNotIn('*MBOM版本号', mbom_node_row)
            self.assertNotIn('*MBOM编码', mbom_node_row)


if __name__ == '__main__':
    unittest.main()
