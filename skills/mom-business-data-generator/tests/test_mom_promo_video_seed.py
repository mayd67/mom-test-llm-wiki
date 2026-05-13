import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_mom_promo_video_seed as promo_seed


class MomPromoVideoSeedTests(unittest.TestCase):
    def test_build_generates_video_aligned_multi_factory_seed(self):
        seed = promo_seed.build()

        metadata = seed.get('metadata', {})
        workbooks = seed['workbooks']
        biz_rows = workbooks['系统配置_模板.xlsx']['业务组织']
        tool_rows = workbooks['工厂资源_模板.xlsx']['工装工具']
        workcenter_rows = workbooks['工厂资源_模板.xlsx']['工作中心']
        location_rows = workbooks['工厂资源_模板.xlsx']['库位']
        route_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线']
        route_op_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工序']
        step_rows = workbooks['产品与工艺_模板.xlsx']['工艺路线工步']
        order_rows = workbooks['生产订单_模板.xlsx']['生产订单']

        self.assertEqual(metadata.get('namespace'), 'MPV20S01')
        self.assertEqual(metadata.get('volume_profile'), '标准版')
        self.assertEqual(metadata.get('name'), 'MOM宣传视频综合演示种子')

        project_biz = next((row for row in biz_rows if row.get('*名称') == '生产项目部'), None)
        self.assertIsNotNone(project_biz)
        self.assertEqual(project_biz.get('工厂组织类型'), '工厂')

        top_route = next((row for row in route_rows if row.get('*名称') == 'MOM宣传视频协同一级工艺'), None)
        self.assertIsNotNone(top_route)
        self.assertEqual(top_route.get('*工艺类型'), '一级工艺')
        self.assertEqual(top_route.get('*工厂组织'), project_biz.get('*编码'))

        top_orders = [row for row in order_rows if row.get('工艺路线编码') == top_route.get('*编码')]
        self.assertEqual(len(top_orders), 1)
        self.assertEqual(top_orders[0].get('计划类型'), '零部件交付计划')
        self.assertEqual(top_orders[0].get('排产状态'), '零部件交付计划已排产')

        wc_names = {row.get('*名称') for row in workcenter_rows}
        self.assertTrue({'收料齐套工位', '质量审理工位', '返修拆装工位', '履历归档工位', '工装借还台账中心'}.issubset(wc_names))

        location_names = {row.get('*名称') for row in location_rows}
        self.assertTrue({'返修判定区', '返修拆装区', '工装借还区', '待检定工装区', '履历归档区'}.issubset(location_names))

        self.assertTrue(any(row.get('*名称') == '智能扭矩扳手' for row in tool_rows))

        assembly_route = next(row for row in route_rows if row.get('*名称') == '变速箱总成总装工艺')
        assembly_ops = {
            row.get('*工序名称')
            for row in route_op_rows
            if row.get('*工艺路线编码') == assembly_route.get('*编码')
        }
        self.assertIn('收料齐套与工艺浏览', assembly_ops)
        self.assertIn('序列号报工、灌油与AI记录校验', assembly_ops)

        test_route = next(row for row in route_rows if row.get('*名称') == '变速箱试验包装工艺')
        test_ops = {
            row.get('*工序名称')
            for row in route_op_rows
            if row.get('*工艺路线编码') == test_route.get('*编码')
        }
        self.assertTrue({'不合格审理与返修判定', '返修拆装与复测', '履历归档与交付放行'}.issubset(test_ops))

        self.assertTrue(any('AI' in str(row.get('工步内容', '')) for row in step_rows))
        self.assertFalse(any(row.get('*工序类型') in {'厂际转工', '厂内转工'} for row in route_op_rows))


if __name__ == '__main__':
    unittest.main()
