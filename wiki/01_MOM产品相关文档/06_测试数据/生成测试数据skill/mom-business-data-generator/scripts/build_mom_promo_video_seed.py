from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

import build_gearbox_multi_factory_seed as gearbox_seed
from gearbox_seed_support import CAT_KIT, FEATURE_IMPORTANT, MAKE_SELF, NO, build_seed, summarize_seed

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass


SCENARIO = 'mom_promo_video'
NAMESPACE = 'MPV20S01'
VOLUME_PROFILE = '标准版'
ASSET_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'mom_promo_video_seed.json'


def _find_route(config: dict, route_code: str) -> dict:
    for route in config.get('routes', []):
        if route.get('code') == route_code:
            return route
    raise KeyError(f'未找到工艺路线: {route_code}')


def _find_op(route: dict, op_no: str) -> dict:
    for op in route.get('ops', []):
        if str(op.get('no', '')).strip() == op_no:
            return op
    raise KeyError(f'未找到工序: {route.get("code")}/{op_no}')


def _insert_before(route: dict, before_op_no: str, op: dict) -> None:
    ops = route.setdefault('ops', [])
    for index, item in enumerate(ops):
        if str(item.get('no', '')).strip() == before_op_no:
            ops.insert(index, op)
            return
    ops.append(op)


def build_config() -> dict:
    config = deepcopy(gearbox_seed.CONFIG)

    metadata = config['metadata']
    metadata.update({
        'name': 'MOM宣传视频综合演示种子',
        'description': '面向用户大会 MOM 产品宣传视频构建的综合演示数据，覆盖多工厂协同计划、AI 辅助调度、执行报工、质量闭环、工装台账与履历追溯。',
    })
    metadata['project_collaboration'] = {
        'enabled': True,
        'admin': {
            'parent': 'ADM-GBX-HQ',
            'code': 'ADM-GBX-PROJ',
            'name': '生产项目部',
            'short': '项目部',
        },
        'biz': {
            'parent': 'BIZ-GBX-COMPANY',
            'code': 'BIZ-GBX-PROJ',
            'name': '生产项目部',
            'short': '项目部',
            'factory_type': '机械加工专业',
            'remark': '用于集团视角下的多工厂协同计划、调度分析与交付承诺管理。',
        },
        'route': {
            'code': 'RT-GBX-PROJ-A01',
            'name': 'MOM宣传视频协同一级工艺',
            'material_code': 'MAT-GBX-GEARBOX-FIN',
            'spec': '通用',
            'remark': '项目部持单，统一承接协同排产、调度分析与交付放行。',
        },
        'phases': [
            {
                'no': '0010',
                'name': '集团订单协同计划确认',
                'wc_code': 'WC-GBX-PROJ-PLAN',
                'wc_name': '集团协同排产中心',
                'content': '项目部汇总订单、产能与交期约束，形成跨工厂协同计划。',
                'output_code': 'MAT-GBX-HSG-FIN',
                'steps': [
                    ('汇总集团订单与产能', '汇总集团订单、工厂产能与交付约束。'),
                    ('AI生成跨厂分配建议', 'AI 评估负荷平衡并生成首轮跨工厂分配建议。'),
                ],
            },
            {
                'no': '0020',
                'name': '关键件工厂AI重排锁定',
                'wc_code': 'WC-GBX-PROJ-SYNC',
                'wc_name': '关键件协同调度中心',
                'content': '针对缺料、设备波动与插单风险执行 AI 辅助重排。',
                'output_code': 'MAT-GBX-GEAR-FIN',
                'steps': [
                    ('识别关键件异常', '识别齿轴机加与热处理阶段的缺料、设备波动和插单风险。'),
                    ('AI重排并锁定优先级', 'AI 计算影响范围并给出跨工厂调度优先级。'),
                ],
            },
            {
                'no': '0030',
                'name': '总装齐套与试验窗口锁定',
                'wc_code': 'WC-GBX-PROJ-ASM',
                'wc_name': '总装试验协同中心',
                'content': '基于齐套状态锁定总装与试验窗口，保障交付节奏。',
                'output_code': 'MAT-GBX-GEARBOX-FIN',
                'op_spec': '装配专业',
                'steps': [
                    ('确认齐套与到货节奏', '确认关键件到货、总装齐套状态与试验窗口。'),
                    ('同步排产承诺', '同步总装与试验工厂的协同节拍和交付承诺。'),
                ],
            },
            {
                'no': '0040',
                'name': '履历归集与交付承诺放行',
                'wc_code': 'WC-GBX-PROJ-REL',
                'wc_name': '交付承诺协同中心',
                'content': '归集序列号履历、质量结论与交付状态，完成集团放行。',
                'op_type': '检验',
                'wc_class': '检验',
                'op_spec': '装配专业',
                'output_code': 'MAT-GBX-GEARBOX-FIN',
                'steps': [
                    ('归集履历与质量结论', '归集总成、关键件、工序和质量事件履历。'),
                    ('确认交付承诺', '完成交付承诺确认并形成集团视角总览。'),
                ],
            },
        ],
    }

    config['users'].extend([
        ('U-GBX-021', '梁博文', '一般', '男', 'ADM-GBX-PMC', 'BIZ-GBX-PMC', '调度员'),
        ('U-GBX-022', '宋雨桐', '一般', '女', 'ADM-GBX-WM', 'BIZ-GBX-WM', '工装管理员'),
        ('U-GBX-023', '许明哲', '一般', '男', 'ADM-GBX-TEST-PLANT', 'BIZ-GBX-TEST-SEC', '返修技术员'),
    ])
    config['work_centers'].extend([
        {'code': 'WC-GBX-KITTING', 'name': '收料齐套工位', 'biz': 'BIZ-GBX-MAINASM-SEC', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBX-QUALITY', 'name': '质量审理工位', 'biz': 'BIZ-GBX-TEST-SEC', 'wc_type': '组织', 'wc_class': '检验'},
        {'code': 'WC-GBX-REPAIR', 'name': '返修拆装工位', 'biz': 'BIZ-GBX-TEST-SEC', 'wc_type': '组织', 'wc_class': '加工'},
        {'code': 'WC-GBX-HISTORY', 'name': '履历归档工位', 'biz': 'BIZ-GBX-TEST-SEC', 'wc_type': '组织', 'wc_class': '检验'},
        {'code': 'WC-GBX-TOOLCRIB', 'name': '工装借还台账中心', 'biz': 'BIZ-GBX-WM', 'wc_type': '组织', 'wc_class': '加工'},
    ])
    config['equipments'].extend([
        {'code': 'EQ-GBX-KIT-01', 'name': '扫码收料终端', 'model': 'KIT-01', 'biz': 'BIZ-GBX-MAINASM-SEC', 'bottle': NO, 'remark': '用于收料扫码与齐套确认'},
        {'code': 'EQ-GBX-QUALITY-01', 'name': '质量审理终端', 'model': 'QA-REVIEW', 'biz': 'BIZ-GBX-TEST-SEC', 'bottle': NO, 'remark': '用于不合格审理与返修判定'},
        {'code': 'EQ-GBX-REPAIR-01', 'name': '返修拆装台', 'model': 'RP-200', 'biz': 'BIZ-GBX-TEST-SEC', 'bottle': NO, 'remark': '用于返修拆装与复测'},
        {'code': 'EQ-GBX-HISTORY-01', 'name': '履历追溯终端', 'model': 'TR-100', 'biz': 'BIZ-GBX-TEST-SEC', 'bottle': NO, 'remark': '用于履历归档与交付放行'},
        {'code': 'EQ-GBX-TOOL-01', 'name': '工装借还柜', 'model': 'TC-12', 'biz': 'BIZ-GBX-WM', 'bottle': NO, 'remark': '用于工装借用、归还和台账登记'},
    ])
    config['tools'].append({
        'code': 'TOOL-GBX-TORQUE-02',
        'name': '智能扭矩扳手',
        'material_category': CAT_KIT,
        'make_type': MAKE_SELF,
        'tooling_category': '专用工装',
        'feature': FEATURE_IMPORTANT,
        'model': 'IW-120',
        'spec': '总装扭矩校核',
        'remark': '用于借还登记、检定提醒和关键扭矩记录。',
        'life_times': 60000,
        'life_days': 180,
    })
    config['wc_user_links'].extend([
        ('WC-GBX-KITTING', 'U-GBX-017'),
        ('WC-GBX-KITTING', 'U-GBX-018'),
        ('WC-GBX-QUALITY', 'U-GBX-007'),
        ('WC-GBX-QUALITY', 'U-GBX-023'),
        ('WC-GBX-REPAIR', 'U-GBX-023'),
        ('WC-GBX-HISTORY', 'U-GBX-007'),
        ('WC-GBX-TOOLCRIB', 'U-GBX-022'),
    ])
    config['wc_eq_links'].extend([
        ('WC-GBX-KITTING', 'EQ-GBX-KIT-01'),
        ('WC-GBX-QUALITY', 'EQ-GBX-QUALITY-01'),
        ('WC-GBX-REPAIR', 'EQ-GBX-REPAIR-01'),
        ('WC-GBX-HISTORY', 'EQ-GBX-HISTORY-01'),
        ('WC-GBX-TOOLCRIB', 'EQ-GBX-TOOL-01'),
    ])
    config['locations'].extend([
        ('LOC-GBX-WIP-04', '返修判定区', 'BIZ-GBX-WM', 'WH-GBX-WIP'),
        ('LOC-GBX-WIP-05', '返修拆装区', 'BIZ-GBX-WM', 'WH-GBX-WIP'),
        ('LOC-GBX-WIP-06', '工装借还区', 'BIZ-GBX-WM', 'WH-GBX-WIP'),
        ('LOC-GBX-WIP-07', '待检定工装区', 'BIZ-GBX-WM', 'WH-GBX-WIP'),
        ('LOC-GBX-FG-02', '履历归档区', 'BIZ-GBX-WM', 'WH-GBX-FG'),
    ])

    assembly_route = _find_route(config, 'RT-GBX-ASM-A01')
    _insert_before(assembly_route, '0010', {
        'no': '0005',
        'name': '收料齐套与工艺浏览',
        'type': '加工',
        'wc': 'WC-GBX-KITTING',
        'prep': 8,
        'run': 10,
        'out': 'MAT-GBX-GEARBOX-FIN',
        'content': '完成收料扫码、齐套确认和工艺浏览。',
        'materials': [('MAT-GBX-HSG-FIN', 1), ('MAT-GBX-GEAR-FIN', 4), ('MAT-GBX-SHAFT-FIN', 2)],
        'steps': [
            ('扫码收料', '扫码确认来料批次、齐套状态和关键件到位情况。'),
            ('浏览作业内容', '查看作业指导、关键参数和质量注意事项。'),
        ],
    })
    fill_op = _find_op(assembly_route, '0040')
    fill_op.update({
        'name': '序列号报工、灌油与AI记录校验',
        'content': '完成序列号报工、定量灌油和 AI 装配记录校验。',
        'steps': [
            ('执行灌油与序列号报工', '按工艺要求完成灌油并采集序列号报工信息。'),
            ('AI校验装配记录与条码绑定', 'AI 校验关键记录并绑定总成条码和关键件追溯关系。'),
        ],
    })

    test_route = _find_route(config, 'RT-GBX-TEST-A01')
    cold_op = _find_op(test_route, '0010')
    cold_op['steps'] = [
        ('执行冷试', '执行变速箱冷试和换挡响应验证。'),
        ('AI分析性能参数', 'AI 分析阻力曲线、换挡响应和异常趋势。'),
    ]
    eol_op = _find_op(test_route, '0020')
    eol_op['content'] = '完成密封、报码、外观终检并生成质量审理输入。'
    eol_op['steps'] = [
        ('执行EOL检测', '执行 EOL 综合检测、报码读取和外观复核。'),
        ('生成质量审理输入', '输出不合格审理所需的质量结论和异常信息。'),
    ]
    pack_op = _find_op(test_route, '0030')
    pack_op['no'] = '0060'
    pack_op['name'] = '包装入库与发运交接'
    pack_op['steps'] = [
        ('执行包装', '完成包装防护、标签粘贴和发运资料准备。'),
        ('转入成品库', '转入成品库并完成发运交接。'),
    ]
    _insert_before(test_route, '0060', {
        'no': '0030',
        'name': '不合格审理与返修判定',
        'type': '检验',
        'wc': 'WC-GBX-QUALITY',
        'prep': 10,
        'run': 16,
        'out': 'MAT-GBX-GEARBOX-FIN',
        'content': '结合检测结果和履历信息完成不合格审理与返修判定。',
        'materials': [],
        'steps': [
            ('审理异常报码', '结合检测结论和履历信息完成不合格审理。'),
            ('AI生成返修建议', 'AI 辅助给出返修方案与影响范围建议。'),
        ],
    })
    _insert_before(test_route, '0060', {
        'no': '0040',
        'name': '返修拆装与复测',
        'type': '加工',
        'wc': 'WC-GBX-REPAIR',
        'prep': 12,
        'run': 20,
        'out': 'MAT-GBX-GEARBOX-FIN',
        'content': '执行返修拆装、关键件更换和复测。',
        'materials': [('MAT-GBX-SEAL-KIT', 1), ('MAT-GBX-FIX-KIT', 1)],
        'steps': [
            ('拆解定位故障件', '按履历定位故障件并完成拆装返修。'),
            ('返修后复测', '完成返修后复测并记录结论。'),
        ],
    })
    _insert_before(test_route, '0060', {
        'no': '0050',
        'name': '履历归档与交付放行',
        'type': '检验',
        'wc': 'WC-GBX-HISTORY',
        'prep': 8,
        'run': 12,
        'out': 'MAT-GBX-GEARBOX-FIN',
        'content': '形成多层级履历并完成交付放行。',
        'materials': [],
        'steps': [
            ('归集序列号履历', '归集总成、关键件、工序和质量事件履历。'),
            ('完成放行归档', '完成放行归档并同步交付看板。'),
        ],
    })

    return config


CONFIG = build_config()


def build_variant(namespace: str = NAMESPACE, volume_profile: str = VOLUME_PROFILE) -> dict:
    return build_seed(deepcopy(CONFIG), SCENARIO, namespace, volume_profile)


def build() -> dict:
    return build_variant()


def summarize(seed: dict) -> dict:
    return summarize_seed(seed)


def main() -> None:
    seed = build()
    ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    ASSET_PATH.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding='utf-8-sig')
    print(json.dumps(summarize(seed), ensure_ascii=False, indent=2))
    print(f'已写入种子文件: {ASSET_PATH}')


if __name__ == '__main__':
    main()
