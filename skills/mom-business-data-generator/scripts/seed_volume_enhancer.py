from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from functools import lru_cache
from math import gcd

WB_SYSTEM = '系统配置_模板.xlsx'
WB_FACTORY = '工厂资源_模板.xlsx'
WB_PRODUCT = '产品与工艺_模板.xlsx'

SH_BIZ = '业务组织'
SH_USER = '用户'
SH_EQ = '设备'
SH_EQ_USER = '设备与用户的关系实体类'
SH_WC = '工作中心'
SH_WC_USER = '工作中心与用户关系'
SH_WC_EQ = '工作中心与设备的关系'
SH_PLIB = '工序库'
SH_MAT = '物料'
SH_MBOM_NODE = 'MBOM节点'
SH_ROUTE = '工艺路线'
SH_OP = '工艺路线工序'
SH_SEQ = '工艺路线工序序列'
SH_OPMAT = '工艺路线工序物料'
SH_STEP = '工艺路线工步'

F_CODE = '*编码'
F_ID = '*编号'
F_NAME = '*名称'
F_BIZ_CODE = '业务组织编码'
F_ADMIN_CODE = '行政组织编码'
F_PARENT = '*父组织编码'
F_ORG_TYPE = '工厂组织类型'
F_FACTORY_ORG = '*工厂组织'
F_WC_CODE = '*工作中心编码'
F_EQ_CODE = '*设备编码'
F_USER_REF = '*用户'
F_VERSION = '*版本号'
F_ROUTE_CODE = '*工艺路线编码'
F_ROUTE_VERSION = '*工艺路线版本号'
F_ROUTE_NAME = '*名称'
F_ROUTE_SPEC = '工艺专业'
F_ROUTE_MATERIAL_CODE = '物料编码'
F_ROUTE_MATERIAL_VERSION = '物料版本号'
F_OP_NO = '*工序号'
F_OP_TYPE = '*工序类型'
F_OP_NAME = '*工序名称'
F_OP_CONTENT = '工序内容'
F_OP_WC = '*工作中心编码'
F_OP_PREP = '*定额辅助工时'
F_OP_RUN = '*定额加工时间'
F_OP_UNIT = '*时间单位'
F_OP_EXECUTE = '执行标记'
F_OP_YIELD = '产出比'
F_OP_OUTPUT_VERSION = '产出物料版本号'
F_OP_OUTPUT_CODE = '产出物料编码'
F_OP_SPEC = '工序专业类型'
F_STEP_NO = '*工步序号'
F_STEP_NAME = '*工步名称'
F_STEP_CONTENT = '工步内容'
F_SEQ_REL = '*接续关系'
F_SEQ_UPSTREAM = '*上道工序号'
F_MAT_CLASS = '*物料分类'
F_MAT_NAME = '*名称'
F_MAT_CATEGORY = '物料类别'
F_MAT_DRAWING = '图号'
F_MAT_MODEL = '型号'
F_MAT_SPEC = '规格'
F_MAT_MAKE = '*制造类型'
F_MAT_UNIT = '计量单位'
F_MAT_FEATURE = '特性分类'
F_MAT_BATCH = '启用批次标记'
F_MAT_SN = '启用序列号标记'
F_MAT_STAGE = '物料阶段'
F_MAT_RELEASE_TIME = '发布版本时间'
F_MAT_RELEASE_USER = '发布人'
F_MAT_SECURITY = '*密级'
F_MAT_REMARK = '备注'
F_ROUTE_MAT_CODE = '*物料编码'
F_ROUTE_MAT_VERSION = '*物料版本号'
F_ROUTE_MAT_QTY = '数量'
F_MBOM_VERSION = '*MBOM版本号'
F_MBOM_CODE = '*MBOM编码'
F_MBOM_MAT_CODE = '*物料编码'
F_MBOM_MAT_NAME = '物料名称'
F_MBOM_MAT_DRAWING = '物料图号'
F_MBOM_MAT_VERSION = '*物料版本'
F_MBOM_MAT_CATEGORY = '*物料类别'
F_MBOM_MAKE = '制造类型'
F_MBOM_QTY = '数量'
F_MBOM_UNIT = '计量单位'
F_MBOM_LEVEL = '*层级'
F_MBOM_SEQ = '*序号'
F_MBOM_STAGE = '物料阶段'
F_MBOM_PARENT_CODE = '父物料编码'
F_MBOM_PARENT_VERSION = '父物料版本'

YES = '是'
NO = '否'
SECURITY = '公开'
TIME_MIN = '分钟'
VERSION = 'A.01'
SEQ_ES = 'ES'
MATERIAL_CLASS = '物料'
CATEGORY_AUX = '辅助材料'
CATEGORY_KIT = '配套件'
CATEGORY_PART = '零部件'
MAKE_BUY = '外购件'
FEATURE_NORMAL = '一般件'
STAGE_MP = '量产'
RELEASE_TIME = '2025-03-01 08:00:00'

COMMON_SURNAMES = [
    '王','李','张','刘','陈','杨','黄','赵','周','吴','徐','孙','胡','朱','高','林','何','郭','马','罗',
    '梁','宋','郑','谢','韩','唐','冯','于','董','萧','程','曹','袁','邓','许','傅','沈','曾','彭','吕',
    '苏','卢','蓋','蔡','贾','丁','魏','薛','叶','阎','余','潘','杜','戴','夏','钟','汪','田','任','姜',
    '崔','谭','廖','范','金','陆','韦','贺','倪','汤','滕','殷','毕','郝','安','常','乐','邹','石','熊',
]
MALE_GIVEN_NAMES = [
    '建国','建军','志强','志勇','国栋','国强','晓峰','振华','海涛','立伟',
    '立军','德强','德明','文斌','文博','俊杰','俊峰','俊豪','永强','永军',
    '宏伟','宏斌','宏涛','庆伟','庆峰','继东','继业','家豪','家俊','家成',
    '天宇','子轩','宇航','浩然','浩宇','博文','博远','明轩','明哲','志鹏',
    '志远','景明','承泽','承宇','启航','启明','嘉豪','嘉树','书恒','书远',
]
FEMALE_GIVEN_NAMES = [
    '丽娜','丽娟','丽萍','丽华','晓燕','晓红','晓莉','晓琳','慧敏','慧娟',
    '静雯','静怡','静雅','佳宁','佳怡','雅婷','雅雯','倩雯','雪梅','雪琴',
    '玉兰','玉梅','春梅','秋萍','海燕','海霞','文静','文娟','敏慧','敏仪',
    '梦洁','梦瑶','梦婷','怡宁','怡然','欣怡','欣妍','晨曦','晨悦','可欣',
    '嘉怡','嘉宁','思雨','思妍','语桐','语汐','清妍','清雅','安琪','安宁',
]
NEUTRAL_GIVEN_NAMES = [
    '嘉宁','嘉怡','书远','书恒','清妍','清雅','景明','景程','安宁','安然',
    '思远','思源','知行','知远','子睿','子涵','云舒','云帆','星宇','星辰',
]

DEFAULT_VOLUME_PROFILE = '标准版'
SUPPORTED_VOLUME_PROFILES = ('标准版', '大体量版', '超大体量版')

VOLUME_PROFILE_CONFIG = {
    '标准版': {
        'resource_clone_count': {'default': 1, 'outsource': 1},
        'user_multiplier': {
            'default': {'班组': 6, '工段': 3, '车间': 1},
            'boeing_737_leap1b': {'班组': 8, '工段': 4, '车间': 2},
        },
        'wc_limit': {'default': 2, 'key_role': 3},
        'eq_limit': {'default': 2, 'key_role': 4},
        'support_variant_labels': [''],
        'route_phase_profile': '标准版',
        'mbom_support_limit': 3,
    },
    '大体量版': {
        'resource_clone_count': {'default': 2, 'outsource': 1},
        'user_multiplier': {
            'default': {'班组': 10, '工段': 5, '车间': 2},
            'boeing_737_leap1b': {'班组': 12, '工段': 5, '车间': 2},
        },
        'wc_limit': {'default': 2, 'key_role': 3},
        'eq_limit': {'default': 2, 'key_role': 4},
        'support_variant_labels': ['', '补充'],
        'route_phase_profile': '大体量版',
        'mbom_support_limit': 6,
    },
    '超大体量版': {
        'resource_clone_count': {'default': 4, 'outsource': 2},
        'user_multiplier': {
            'default': {'班组': 14, '工段': 7, '车间': 3},
            'boeing_737_leap1b': {'班组': 16, '工段': 8, '车间': 3},
        },
        'wc_limit': {'default': 3, 'key_role': 4},
        'eq_limit': {'default': 3, 'key_role': 6},
        'support_variant_labels': ['', '补充', '备用'],
        'route_phase_profile': '超大体量版',
        'mbom_support_limit': 9,
    },
}

ROUTE_PHASE_LIBRARY = {
    '标准版': [
        {
            'kind': 'prep',
            'name': '{op_name}准备点检',
            'op_type': '检验预置',
            'prep_ratio': 0.4,
            'run_ratio': 0.25,
            'min_prep': 5,
            'min_run': 6,
            'content': '执行{op_name}前的工装、设备、程序和来料确认',
            'steps': [
                ('核对工单与来料状态', '核对工单、来料、批次和工装状态'),
                ('确认程序参数与质量要求', '确认程序版本、工艺参数、质量控制点和防错要求'),
            ],
            'attach_support_material': True,
        },
        {'kind': 'main', 'main': True},
        {
            'kind': 'check',
            'name': '{op_name}过程确认',
            'op_type': '检验',
            'prep_ratio': 0.3,
            'run_ratio': 0.2,
            'min_prep': 4,
            'min_run': 5,
            'content': '完成{op_name}后的过程确认、质量记录和报工归档',
            'steps': [
                ('执行过程自检', '对{op_name}结果执行自检、互检或专检确认'),
                ('记录结果并完成报工', '记录关键质量结果、追溯信息并完成工序报工'),
            ],
            'attach_support_material': True,
        },
    ],
    '大体量版': [
        {
            'kind': 'prep',
            'name': '{op_name}准备点检',
            'op_type': '检验预置',
            'prep_ratio': 0.4,
            'run_ratio': 0.25,
            'min_prep': 5,
            'min_run': 6,
            'content': '执行{op_name}前的工装、设备、程序和来料确认',
            'steps': [
                ('核对工单与来料状态', '核对工单、来料、批次和工装状态'),
                ('确认程序参数与质量要求', '确认程序版本、工艺参数、质量控制点和防错要求'),
            ],
            'attach_support_material': True,
        },
        {
            'kind': 'first_article',
            'name': '{op_name}首件确认',
            'op_type': '检验',
            'prep_ratio': 0.3,
            'run_ratio': 0.22,
            'min_prep': 4,
            'min_run': 5,
            'content': '执行{op_name}后的首件尺寸、参数和状态确认',
            'steps': [
                ('执行首件检测', '对{op_name}首件执行尺寸、状态和参数检测'),
                ('确认首件放行', '完成首件确认并办理放行记录'),
            ],
            'attach_support_material': True,
        },
        {'kind': 'main', 'main': True},
        {
            'kind': 'check',
            'name': '{op_name}过程确认',
            'op_type': '检验',
            'prep_ratio': 0.3,
            'run_ratio': 0.2,
            'min_prep': 4,
            'min_run': 5,
            'content': '完成{op_name}后的过程确认、质量记录和报工归档',
            'steps': [
                ('执行过程自检', '对{op_name}结果执行自检、互检或专检确认'),
                ('记录结果并完成报工', '记录关键质量结果、追溯信息并完成工序报工'),
            ],
            'attach_support_material': True,
        },
    ],
    '超大体量版': [
        {
            'kind': 'prep',
            'name': '{op_name}准备点检',
            'op_type': '检验预置',
            'prep_ratio': 0.4,
            'run_ratio': 0.25,
            'min_prep': 5,
            'min_run': 6,
            'content': '执行{op_name}前的工装、设备、程序和来料确认',
            'steps': [
                ('核对工单与来料状态', '核对工单、来料、批次和工装状态'),
                ('确认程序参数与质量要求', '确认程序版本、工艺参数、质量控制点和防错要求'),
            ],
            'attach_support_material': True,
        },
        {
            'kind': 'first_article',
            'name': '{op_name}首件确认',
            'op_type': '检验',
            'prep_ratio': 0.3,
            'run_ratio': 0.22,
            'min_prep': 4,
            'min_run': 5,
            'content': '执行{op_name}后的首件尺寸、参数和状态确认',
            'steps': [
                ('执行首件检测', '对{op_name}首件执行尺寸、状态和参数检测'),
                ('确认首件放行', '完成首件确认并办理放行记录'),
            ],
            'attach_support_material': True,
        },
        {'kind': 'main', 'main': True},
        {
            'kind': 'patrol',
            'name': '{op_name}过程巡检',
            'op_type': '检验',
            'prep_ratio': 0.25,
            'run_ratio': 0.18,
            'min_prep': 4,
            'min_run': 5,
            'content': '对{op_name}执行中的关键参数、质量趋势和节拍状态进行巡检确认',
            'steps': [
                ('执行过程巡检', '抽检关键尺寸、扭矩、参数或过程状态'),
                ('记录SPC与异常结果', '记录过程能力、异常点并形成追溯数据'),
            ],
            'attach_support_material': True,
        },
        {
            'kind': 'final',
            'name': '{op_name}完工复核',
            'op_type': '检验',
            'prep_ratio': 0.3,
            'run_ratio': 0.2,
            'min_prep': 4,
            'min_run': 5,
            'content': '完成{op_name}后的完工复核、交接确认和报工归档',
            'steps': [
                ('复核关键特性', '复核关键质量特性、参数记录和防错状态'),
                ('办理完工交接与报工', '完成完工交接确认并提交工序报工'),
            ],
            'attach_support_material': True,
        },
    ],
}


def resolve_volume_profile(volume_profile: object = None) -> str:
    value = _norm(volume_profile)
    if value in SUPPORTED_VOLUME_PROFILES:
        return value
    return DEFAULT_VOLUME_PROFILE


def get_volume_profile_config(volume_profile: object = None) -> dict:
    return VOLUME_PROFILE_CONFIG[resolve_volume_profile(volume_profile)]


def _user_multiplier(scenario: str, profile_config: dict) -> dict:
    user_config = profile_config.get('user_multiplier', {})
    default_multiplier = user_config.get('default', {'班组': 6, '工段': 3, '车间': 1})
    multiplier = dict(default_multiplier)
    multiplier.update(user_config.get(scenario, {}))
    return multiplier


def _route_phase_templates(profile_config: dict) -> list[dict]:
    profile_name = profile_config.get('route_phase_profile', DEFAULT_VOLUME_PROFILE)
    return ROUTE_PHASE_LIBRARY[profile_name]


def _rows(seed: dict, workbook: str, sheet: str) -> list[dict]:
    return seed['workbooks'][workbook][sheet]


def _norm(value: object) -> str:
    return str(value or '').strip()


def _append_unique(rows: list[dict], new_rows: list[dict], key_fields: tuple[str, ...]) -> None:
    existing = {tuple(_norm(row.get(field, '')) for field in key_fields) for row in rows}
    for row in new_rows:
        key = tuple(_norm(row.get(field, '')) for field in key_fields)
        if key in existing:
            continue
        rows.append(row)
        existing.add(key)


def _int_value(value: object, default: int = 0) -> int:
    text = _norm(value)
    digits = ''.join(ch for ch in text if ch.isdigit())
    return int(digits) if digits else default


def _format_no(value: int) -> str:
    return f'{value:04d}'


@lru_cache(maxsize=None)
def _name_shuffle_params(space_size: int) -> tuple[int, int]:
    step = 97
    while gcd(step, space_size) != 1:
        step += 2
    offset = (space_size // 3) + 11
    return step, offset % space_size


def _given_name_pool(gender: str) -> list[str]:
    if gender == '男':
        return MALE_GIVEN_NAMES
    if gender == '女':
        return FEMALE_GIVEN_NAMES
    return NEUTRAL_GIVEN_NAMES


def _unique_name(index: int, gender: str = '') -> str:
    given_names = _given_name_pool(gender)
    pair_space = len(COMMON_SURNAMES) * len(given_names)
    step, offset = _name_shuffle_params(pair_space)
    shuffled = (max(index, 0) * step + offset) % pair_space
    given_index, surname_index = divmod(shuffled, len(COMMON_SURNAMES))
    return COMMON_SURNAMES[surname_index] + given_names[given_index]


def _masked_phone(index: int) -> str:
    tail = 1000 + (index % 9000)
    return f'13{index % 10}****{tail:04d}'


def _masked_email(index: int, scenario: str) -> str:
    scenario_key = ''.join(ch for ch in scenario if ch.isalpha())[:6] or 'scene'
    return f'{scenario_key}{index:04d}@hqpt-demo.com'


def _masked_birth(index: int) -> str:
    year = 1985 + (index % 15)
    month = (index % 12) + 1
    day = (index % 27) + 1
    return f'{year:04d}-{month:02d}-{day:02d}'


def _masked_id(index: int) -> str:
    area = 1100 + (index % 89)
    tail = 1000 + (index % 9000)
    return f'{area:04d}********{tail:04d}'


def _infer_process_prefix(text: str) -> str:
    value = _norm(text)
    mapping = [
        (('总装', '装配', '装调', '座椅', '靠背', '扶手'), '装配'),
        (('机加', '加工', '铣', '车', '磨', '钻', '镗', '珩', 'CNC'), '机加'),
        (('铸', '浇', '熔炼', '低压'), '铸造'),
        (('锻', '模锻'), '锻造'),
        (('热处理', '淬火', '回火', '热表'), '热处理'),
        (('试验', '试车', '热试', '冷试', '验证'), '试验'),
        (('电气', '数控', '线束', '电柜', 'USB'), '电气'),
        (('质量', '检验', '检测', '放行'), '质量'),
        (('物流', '仓储', '库房', '配送'), '物流'),
    ]
    for keywords, label in mapping:
        if any(keyword in value for keyword in keywords):
            return label
    return '生产'


def _build_support_templates(route_text: str, spec_text: str) -> list[tuple[str, str, str, int]]:
    text = f'{_norm(route_text)} {_norm(spec_text)}'
    if any(keyword in text for keyword in ('装配', '总装', '座椅', '靠背', '扶手', '电气')):
        return [
            ('紧固件标准包', 'M6/M8混合标准件', CATEGORY_KIT, 1),
            ('定位垫片包', '0.1/0.2/0.5mm组合垫片', CATEGORY_KIT, 1),
            ('螺纹锁固剂', '中强度锁固剂 10ml', CATEGORY_AUX, 1),
            ('装配润滑脂', '高温锂基脂 30g', CATEGORY_AUX, 1),
            ('工序流转卡', '条码追溯流转卡', CATEGORY_AUX, 1),
            ('防护包装件', '总成周转防护件', CATEGORY_KIT, 1),
        ]
    if any(keyword in text for keyword in ('铸', '浇', '熔炼', '低压')):
        return [
            ('铝液精炼剂', '铝液除气精炼剂', CATEGORY_AUX, 1),
            ('低压铸造脱模剂', '水基脱模剂', CATEGORY_AUX, 1),
            ('陶瓷过滤片', '蜂窝过滤片', CATEGORY_AUX, 1),
            ('覆盖剂', '铝液覆盖保温剂', CATEGORY_AUX, 1),
            ('铸件流转卡', '浇注批次追溯卡', CATEGORY_AUX, 1),
            ('铸件周转料框', '耐热周转料框', CATEGORY_KIT, 1),
        ]
    if any(keyword in text for keyword in ('热处理', '淬火', '回火', '热表')):
        return [
            ('保护气体', '热处理保护气体', CATEGORY_AUX, 1),
            ('淬火介质', '聚合物淬火液', CATEGORY_AUX, 1),
            ('回火托盘', '耐热工艺托盘', CATEGORY_KIT, 1),
            ('工艺标签', '耐高温工艺标签', CATEGORY_AUX, 1),
            ('热处理流转卡', '热处理追溯卡', CATEGORY_AUX, 1),
            ('热处理防护件', '防磕碰保护件', CATEGORY_KIT, 1),
        ]
    if any(keyword in text for keyword in ('检验', '检测', '放行', '试验', '试车', '验证')):
        return [
            ('检验记录卡', '过程检验记录卡', CATEGORY_AUX, 1),
            ('追溯标签', '条码追溯标签', CATEGORY_AUX, 1),
            ('封签件', '检验防拆封签', CATEGORY_KIT, 1),
            ('样件防护套', '检测样件防护套', CATEGORY_KIT, 1),
            ('测试记录单', '试验过程记录单', CATEGORY_AUX, 1),
            ('交检包装件', '交检防护包装件', CATEGORY_KIT, 1),
        ]
    return [
        ('刀具耗材包', '标准工艺耗材套装', CATEGORY_KIT, 1),
        ('切削液', '全合成切削液', CATEGORY_AUX, 1),
        ('清洗剂', '水基清洗剂', CATEGORY_AUX, 1),
        ('防锈油', '薄膜防锈油', CATEGORY_AUX, 1),
        ('工序流转卡', '条码追溯流转卡', CATEGORY_AUX, 1),
        ('周转防护件', '半成品周转防护件', CATEGORY_KIT, 1),
    ]


def _build_material_row(code: str, name: str, category: str, spec: str, route_name: str) -> dict:
    return {
        F_MAT_CLASS: MATERIAL_CLASS,
        F_MAT_NAME: name,
        F_MAT_CATEGORY: category,
        F_MAT_DRAWING: code.replace('MAT-', ''),
        F_MAT_MODEL: '',
        F_MAT_SPEC: spec,
        F_MAT_MAKE: MAKE_BUY,
        F_MAT_UNIT: '个',
        F_MAT_FEATURE: FEATURE_NORMAL,
        F_MAT_BATCH: YES,
        F_MAT_SN: NO,
        F_MAT_STAGE: STAGE_MP,
        F_MAT_RELEASE_TIME: RELEASE_TIME,
        F_MAT_RELEASE_USER: '',
        F_VERSION: VERSION,
        F_CODE: code,
        F_MAT_SECURITY: SECURITY,
        F_MAT_REMARK: f'{route_name}自动扩展辅料',
    }


def _build_process_lib_row(op_row: dict) -> dict:
    return {
        '序专业类型': _norm(op_row.get(F_OP_SPEC, '')),
        F_NAME: _norm(op_row.get(F_OP_NAME, '')),
        '*工序类型': _norm(op_row.get(F_OP_TYPE, '')),
        F_WC_CODE: _norm(op_row.get(F_OP_WC, '')),
        '*定额准备时间': op_row.get(F_OP_PREP, 0),
        '*定额加工时间': op_row.get(F_OP_RUN, 0),
        '执行标记': YES,
        '*时间单位': _norm(op_row.get(F_OP_UNIT, TIME_MIN)) or TIME_MIN,
        '产出比': op_row.get(F_OP_YIELD, 1) or 1,
        '工序内容': _norm(op_row.get(F_OP_CONTENT, '')),
        '*密级': SECURITY,
    }


def _build_step(route_version: str, route_code: str, op_no: str, step_no: int, name: str, content: str) -> dict:
    return {
        F_ROUTE_VERSION: route_version,
        F_ROUTE_CODE: route_code,
        F_OP_NO: op_no,
        F_STEP_NO: str(step_no),
        F_STEP_NAME: name,
        F_STEP_CONTENT: content,
    }


def _build_route_material(route_version: str, route_code: str, op_no: str, material_code: str, qty: int) -> dict:
    return {
        F_ROUTE_VERSION: route_version,
        F_ROUTE_CODE: route_code,
        F_ROUTE_MAT_VERSION: VERSION,
        F_ROUTE_MAT_CODE: material_code,
        F_OP_NO: op_no,
        F_ROUTE_MAT_QTY: qty,
    }


def _clone_op(op_row: dict, op_no: str, name: str, op_type: str, prep: int, run: int, content: str) -> dict:
    cloned = deepcopy(op_row)
    cloned[F_OP_NO] = op_no
    cloned[F_OP_NAME] = name
    cloned[F_OP_TYPE] = op_type
    cloned[F_OP_PREP] = prep
    cloned[F_OP_RUN] = run
    cloned[F_OP_CONTENT] = content
    return cloned


def _lineage_builder(biz_rows: list[dict]):
    parent_map = { _norm(row.get(F_CODE, '')): _norm(row.get(F_PARENT, '')) for row in biz_rows }

    @lru_cache(maxsize=None)
    def lineage(code: str) -> tuple[str, ...]:
        result: list[str] = []
        current = _norm(code)
        guard: set[str] = set()
        while current and current != '0' and current not in guard:
            result.append(current)
            guard.add(current)
            current = parent_map.get(current, '')
        return tuple(result)

    return lineage


def expand_seed_volume(seed: dict, scenario: str, volume_profile: str = DEFAULT_VOLUME_PROFILE) -> dict:
    profile_name = resolve_volume_profile(volume_profile)
    profile_config = get_volume_profile_config(profile_name)
    seed.setdefault('metadata', {})['volume_profile'] = profile_name
    _expand_resources(seed, profile_config)
    _expand_users(seed, scenario, profile_config)
    _expand_route_details(seed, scenario, profile_config)
    normalize_sequence_relations(seed)
    return seed


def normalize_sequence_relations(seed: dict) -> dict:
    for row in _rows(seed, WB_PRODUCT, SH_SEQ):
        row[F_SEQ_REL] = SEQ_ES
    return seed


def _expand_resources(seed: dict, profile_config: dict) -> None:
    workcenters = _rows(seed, WB_FACTORY, SH_WC)
    equipments = _rows(seed, WB_FACTORY, SH_EQ)
    wc_equipment = _rows(seed, WB_FACTORY, SH_WC_EQ)

    clone_config = profile_config.get('resource_clone_count', {})
    default_clone_count = int(clone_config.get('default', 1))
    outsource_clone_count = int(clone_config.get('outsource', 1))

    existing_wc_codes = {_norm(row.get(F_CODE, '')) for row in workcenters}
    existing_eq_codes = {_norm(row.get(F_CODE, '')) for row in equipments}
    equipment_by_code = {_norm(row.get(F_CODE, '')): row for row in equipments}
    wc_rel_map: dict[str, list[str]] = defaultdict(list)
    for row in wc_equipment:
        wc_rel_map[_norm(row.get(F_WC_CODE, ''))].append(_norm(row.get(F_EQ_CODE, '')))

    new_workcenters: list[dict] = []
    clone_map: dict[str, list[str]] = defaultdict(list)
    for row in list(workcenters):
        base_code = _norm(row.get(F_CODE, ''))
        if not base_code or '-P' in base_code:
            continue
        wc_type = _norm(row.get('*类型', ''))
        clone_count = outsource_clone_count if wc_type in ('外委', '外协') else default_clone_count
        for index in range(1, clone_count + 1):
            clone_code = f'{base_code}-P{index:02d}'
            if clone_code in existing_wc_codes:
                continue
            clone_row = deepcopy(row)
            clone_row[F_CODE] = clone_code
            clone_row[F_NAME] = f"{_norm(row.get(F_NAME, ''))}{index:02d}单元"
            remark = _norm(row.get('备注', ''))
            clone_row['备注'] = f'{remark}；并行作业单元{index:02d}'.strip('；')
            new_workcenters.append(clone_row)
            clone_map[base_code].append(clone_code)
            existing_wc_codes.add(clone_code)
    workcenters.extend(new_workcenters)

    new_equipments: list[dict] = []
    new_wc_equipment: list[dict] = []
    for base_wc, clone_wcs in clone_map.items():
        related_eq_codes = wc_rel_map.get(base_wc, [])
        for clone_index, clone_wc in enumerate(clone_wcs, start=1):
            for eq_code in related_eq_codes:
                eq_row = equipment_by_code.get(eq_code)
                if not eq_row:
                    continue
                clone_eq_code = f'{eq_code}-P{clone_index:02d}'
                if clone_eq_code not in existing_eq_codes:
                    clone_eq = deepcopy(eq_row)
                    clone_eq[F_CODE] = clone_eq_code
                    clone_eq[F_NAME] = f"{_norm(eq_row.get(F_NAME, ''))}-{clone_index:02d}#"
                    clone_eq['备注'] = f"{_norm(eq_row.get('备注', ''))}；并行设备{clone_index:02d}".strip('；')
                    clone_eq['瓶颈资源'] = '否'
                    new_equipments.append(clone_eq)
                    existing_eq_codes.add(clone_eq_code)
                new_wc_equipment.append({F_EQ_CODE: clone_eq_code, F_WC_CODE: clone_wc})
    equipments.extend(new_equipments)
    _append_unique(wc_equipment, new_wc_equipment, (F_EQ_CODE, F_WC_CODE))


def _expand_users(seed: dict, scenario: str, profile_config: dict) -> None:
    bizs = _rows(seed, WB_SYSTEM, SH_BIZ)
    users = _rows(seed, WB_SYSTEM, SH_USER)
    workcenters = _rows(seed, WB_FACTORY, SH_WC)
    equipments = _rows(seed, WB_FACTORY, SH_EQ)
    wc_users = _rows(seed, WB_FACTORY, SH_WC_USER)
    eq_users = _rows(seed, WB_FACTORY, SH_EQ_USER)

    lineage = _lineage_builder(bizs)
    wc_rows_by_org: dict[str, list[dict]] = defaultdict(list)
    eq_rows_by_org: dict[str, list[dict]] = defaultdict(list)
    for row in workcenters:
        wc_rows_by_org[_norm(row.get(F_FACTORY_ORG, ''))].append(row)
    for row in equipments:
        eq_rows_by_org[_norm(row.get(F_FACTORY_ORG, ''))].append(row)

    multipliers = _user_multiplier(scenario, profile_config)
    wc_limit_config = profile_config.get('wc_limit', {})
    eq_limit_config = profile_config.get('eq_limit', {})
    next_index = len(users) + 1
    new_users: list[dict] = []

    for org_row in bizs:
        org_code = _norm(org_row.get(F_CODE, ''))
        org_type = _norm(org_row.get(F_ORG_TYPE, ''))
        org_name = _norm(org_row.get(F_NAME, ''))
        admin_code = _norm(org_row.get(F_ADMIN_CODE, ''))
        prefix = _infer_process_prefix(org_name)
        role_plan: list[tuple[str, int]] = []
        if org_type == '班组':
            role_plan.append((f'{prefix}操作工', multipliers.get('班组', 6)))
            role_plan.append((f'{prefix}班组长', 1))
        elif org_type == '工段':
            quality_count = max(1, (multipliers.get('工段', 3) + 1) // 2)
            role_plan.extend([
                (f'{prefix}质量员', quality_count),
                ('设备维修工', 1),
                ('设备保养员', 1),
                ('物流配送员', 1),
            ])
        elif org_type == '车间':
            role_plan.extend([
                ('生产计划员', max(1, multipliers.get('车间', 1))),
                (f'{prefix}工艺工程师', max(1, multipliers.get('车间', 1))),
            ])
        if not role_plan:
            continue

        for role_name, count in role_plan:
            for _ in range(count):
                user_index = next_index
                next_index += 1
                new_users.append({
                    F_ID: f'U-EXTRA-{scenario}-{user_index:04d}',
                    '名称': _unique_name(user_index),
                    '用户安全等级': '一般',
                    '性别': '男' if user_index % 2 else '女',
                    F_ADMIN_CODE: admin_code,
                    F_BIZ_CODE: org_code,
                    '备注': role_name,
                    '联系方式': _masked_phone(user_index),
                    '电子邮箱': _masked_email(user_index, scenario),
                    '出生日期': _masked_birth(user_index),
                    '身份证号': _masked_id(user_index),
                })

    _append_unique(users, new_users, (F_ID,))

    for user_row in new_users:
        user_code = _norm(user_row.get(F_ID, ''))
        user_biz = _norm(user_row.get(F_BIZ_CODE, ''))
        role_name = _norm(user_row.get('备注', ''))
        candidate_wc_codes: list[str] = []
        candidate_eq_codes: list[str] = []
        for org_code in lineage(user_biz):
            candidate_wc_codes.extend(_norm(row.get(F_CODE, '')) for row in wc_rows_by_org.get(org_code, []))
            candidate_eq_codes.extend(_norm(row.get(F_CODE, '')) for row in eq_rows_by_org.get(org_code, []))
        candidate_wc_codes = [code for code in dict.fromkeys(candidate_wc_codes) if code]
        candidate_eq_codes = [code for code in dict.fromkeys(candidate_eq_codes) if code]

        wc_limit = int(wc_limit_config.get('key_role', 3)) if any(keyword in role_name for keyword in ('维修', '保养', '班组长')) else int(wc_limit_config.get('default', 2))
        eq_limit = int(eq_limit_config.get('key_role', 4)) if any(keyword in role_name for keyword in ('维修', '保养')) else int(eq_limit_config.get('default', 2))
        wc_rel_rows = [{F_WC_CODE: code, F_USER_REF: user_code} for code in candidate_wc_codes[:wc_limit]]
        eq_rel_rows = [{F_EQ_CODE: code, F_USER_REF: user_code} for code in candidate_eq_codes[:eq_limit]]
        _append_unique(wc_users, wc_rel_rows, (F_WC_CODE, F_USER_REF))
        _append_unique(eq_users, eq_rel_rows, (F_EQ_CODE, F_USER_REF))


def _expand_route_details(seed: dict, scenario: str, profile_config: dict) -> None:
    routes = _rows(seed, WB_PRODUCT, SH_ROUTE)
    materials = _rows(seed, WB_PRODUCT, SH_MAT)
    mbom_nodes = _rows(seed, WB_PRODUCT, SH_MBOM_NODE)
    ops = _rows(seed, WB_PRODUCT, SH_OP)
    seqs = _rows(seed, WB_PRODUCT, SH_SEQ)
    op_mats = _rows(seed, WB_PRODUCT, SH_OPMAT)
    steps = _rows(seed, WB_PRODUCT, SH_STEP)
    process_lib = _rows(seed, WB_FACTORY, SH_PLIB)

    material_lookup = {_norm(row.get(F_CODE, '')): row for row in materials}
    ops_by_route: dict[tuple[str, str], list[dict]] = defaultdict(list)
    steps_by_op: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    mats_by_op: dict[tuple[str, str, str], list[dict]] = defaultdict(list)

    for row in ops:
        ops_by_route[(_norm(row.get(F_ROUTE_VERSION, '')), _norm(row.get(F_ROUTE_CODE, '')))].append(deepcopy(row))
    for row in steps:
        steps_by_op[(_norm(row.get(F_ROUTE_VERSION, '')), _norm(row.get(F_ROUTE_CODE, '')), _norm(row.get(F_OP_NO, '')))].append(deepcopy(row))
    for row in op_mats:
        mats_by_op[(_norm(row.get(F_ROUTE_VERSION, '')), _norm(row.get(F_ROUTE_CODE, '')), _norm(row.get(F_OP_NO, '')))].append(deepcopy(row))

    support_variant_labels = profile_config.get('support_variant_labels', [''])
    phase_templates = _route_phase_templates(profile_config)
    generated_support_by_route: dict[str, list[tuple[str, int]]] = {}
    new_materials: list[dict] = []
    for route_row in routes:
        route_code = _norm(route_row.get(F_CODE, ''))
        route_name = _norm(route_row.get(F_ROUTE_NAME, ''))
        route_spec = _norm(route_row.get(F_ROUTE_SPEC, ''))
        support_codes: list[tuple[str, int]] = []
        template_rows = _build_support_templates(route_name, route_spec)
        for variant_index, variant_label in enumerate(support_variant_labels, start=1):
            for support_index, (support_name, support_spec, support_category, qty) in enumerate(template_rows, start=1):
                mat_code = f'MAT-AUX-{route_code.replace("-", "_")}-V{variant_index:02d}-{support_index:02d}'
                material_name = f'{route_name}{support_name}'
                if variant_label:
                    material_name = f'{material_name}（{variant_label}）'
                if mat_code not in material_lookup:
                    material_row = _build_material_row(mat_code, material_name, support_category, support_spec, route_name)
                    new_materials.append(material_row)
                    material_lookup[mat_code] = material_row
                support_codes.append((mat_code, qty))
        generated_support_by_route[route_code] = support_codes
    _append_unique(materials, new_materials, (F_CODE,))

    new_ops: list[dict] = []
    new_seqs: list[dict] = []
    new_op_mats: list[dict] = []
    new_steps: list[dict] = []
    new_process_lib: list[dict] = []
    existing_process_lib_keys = {(_norm(row.get(F_NAME, '')), _norm(row.get(F_WC_CODE, ''))) for row in process_lib}

    for route_row in routes:
        route_version = _norm(route_row.get(F_VERSION, VERSION)) or VERSION
        route_code = _norm(route_row.get(F_CODE, ''))
        route_key = (route_version, route_code)
        route_ops = sorted(ops_by_route.get(route_key, []), key=lambda row: _int_value(row.get(F_OP_NO, '0')))
        if not route_ops:
            continue

        support_codes = generated_support_by_route.get(route_code, [])
        support_cursor = 0
        expanded_op_nos: list[str] = []
        current_no = 10
        for op_row in route_ops:
            old_op_no = _norm(op_row.get(F_OP_NO, ''))
            op_name = _norm(op_row.get(F_OP_NAME, ''))
            op_type = _norm(op_row.get(F_OP_TYPE, '')) or '加工'
            op_content = _norm(op_row.get(F_OP_CONTENT, '')) or op_name
            source_steps = sorted(steps_by_op.get((route_version, route_code, old_op_no), []), key=lambda row: _int_value(row.get(F_STEP_NO, '0')))
            source_materials = mats_by_op.get((route_version, route_code, old_op_no), [])

            for phase in phase_templates:
                phase_no = _format_no(current_no)
                current_no += 10
                if phase.get('main'):
                    phase_row = deepcopy(op_row)
                    phase_row[F_OP_NO] = phase_no
                    new_ops.append(phase_row)
                    expanded_op_nos.append(phase_no)
                    if source_steps:
                        for step_index, step_row in enumerate(source_steps, start=1):
                            new_step = deepcopy(step_row)
                            new_step[F_OP_NO] = phase_no
                            new_step[F_STEP_NO] = str(step_index * 10)
                            new_steps.append(new_step)
                    else:
                        new_steps.extend([
                            _build_step(route_version, route_code, phase_no, 10, f'{op_name}执行', op_content),
                            _build_step(route_version, route_code, phase_no, 20, f'{op_name}结果确认', f'完成{op_name}并确认结果满足工艺要求'),
                        ])
                    for material_row in source_materials:
                        cloned_material = deepcopy(material_row)
                        cloned_material[F_OP_NO] = phase_no
                        new_op_mats.append(cloned_material)
                    continue

                phase_op_type = _norm(phase.get('op_type', ''))
                if phase_op_type == '检验预置':
                    phase_op_type = '检验' if op_type == '检验' else '加工'
                prep = max(int(phase.get('min_prep', 4)), int(_int_value(op_row.get(F_OP_PREP, 10)) * float(phase.get('prep_ratio', 0.3))))
                run = max(int(phase.get('min_run', 5)), int(_int_value(op_row.get(F_OP_RUN, 20)) * float(phase.get('run_ratio', 0.2))))
                content = _norm(phase.get('content', '')).format(op_name=op_name)
                phase_row = _clone_op(
                    op_row,
                    phase_no,
                    _norm(phase.get('name', '{op_name}')).format(op_name=op_name),
                    phase_op_type or '检验',
                    prep,
                    run,
                    content,
                )
                new_ops.append(phase_row)
                expanded_op_nos.append(phase_no)

                for step_index, (step_name, step_content) in enumerate(phase.get('steps', []), start=1):
                    new_steps.append(
                        _build_step(
                            route_version,
                            route_code,
                            phase_no,
                            step_index * 10,
                            step_name.format(op_name=op_name),
                            step_content.format(op_name=op_name),
                        )
                    )

                if phase.get('attach_support_material') and support_codes:
                    support_code, support_qty = support_codes[support_cursor % len(support_codes)]
                    support_cursor += 1
                    new_op_mats.append(_build_route_material(route_version, route_code, phase_no, support_code, support_qty))

        for prev_no, current_op_no in zip(expanded_op_nos, expanded_op_nos[1:]):
            new_seqs.append({
                F_SEQ_REL: SEQ_ES,
                F_OP_NO: current_op_no,
                F_SEQ_UPSTREAM: prev_no,
                F_ROUTE_VERSION: route_version,
                F_ROUTE_CODE: route_code,
            })

    ops[:] = new_ops
    seqs[:] = new_seqs
    op_mats[:] = new_op_mats
    steps[:] = new_steps

    for op_row in new_ops:
        plib_key = (_norm(op_row.get(F_OP_NAME, '')), _norm(op_row.get(F_OP_WC, '')))
        if plib_key in existing_process_lib_keys:
            continue
        process_lib_row = _build_process_lib_row(op_row)
        new_process_lib.append(process_lib_row)
        existing_process_lib_keys.add(plib_key)
    _append_unique(process_lib, new_process_lib, (F_NAME, F_WC_CODE))

    _expand_mbom_nodes(
        routes,
        generated_support_by_route,
        material_lookup,
        mbom_nodes,
        int(profile_config.get('mbom_support_limit', 3)),
    )


def _expand_mbom_nodes(
    routes: list[dict],
    generated_support_by_route: dict[str, list[tuple[str, int]]],
    material_lookup: dict[str, dict],
    mbom_nodes: list[dict],
    support_limit: int,
) -> None:
    next_seq_map: dict[tuple[str, int], int] = defaultdict(int)
    node_by_material: dict[str, list[dict]] = defaultdict(list)
    for node in mbom_nodes:
        node_by_material[_norm(node.get(F_MBOM_MAT_CODE, ''))].append(node)
        key = (_norm(node.get(F_MBOM_CODE, '')), _int_value(node.get(F_MBOM_LEVEL, 0)))
        next_seq_map[key] = max(next_seq_map[key], _int_value(node.get(F_MBOM_SEQ, 0)))

    new_nodes: list[dict] = []
    for route_row in routes:
        route_code = _norm(route_row.get(F_CODE, ''))
        material_code = _norm(route_row.get(F_ROUTE_MATERIAL_CODE, ''))
        support_codes = generated_support_by_route.get(route_code, [])[:support_limit]
        parent_candidates = node_by_material.get(material_code, [])
        if not parent_candidates:
            continue
        parent_node = parent_candidates[0]
        parent_level = _int_value(parent_node.get(F_MBOM_LEVEL, 0))
        child_level = parent_level + 1
        mbom_code = _norm(parent_node.get(F_MBOM_CODE, ''))
        mbom_version = _norm(parent_node.get(F_MBOM_VERSION, VERSION)) or VERSION
        parent_material_version = _norm(parent_node.get(F_MBOM_MAT_VERSION, VERSION)) or VERSION
        for support_code, qty in support_codes:
            material_row = material_lookup.get(support_code)
            if not material_row:
                continue
            seq_key = (mbom_code, child_level)
            next_seq_map[seq_key] += 10
            new_nodes.append({
                F_MBOM_VERSION: mbom_version,
                F_MBOM_CODE: mbom_code,
                F_MBOM_MAT_CODE: support_code,
                F_MBOM_MAT_NAME: _norm(material_row.get(F_MAT_NAME, '')),
                F_MBOM_MAT_DRAWING: _norm(material_row.get(F_MAT_DRAWING, '')),
                F_MBOM_MAT_VERSION: _norm(material_row.get(F_VERSION, VERSION)) or VERSION,
                F_MBOM_MAT_CATEGORY: _norm(material_row.get(F_MAT_CATEGORY, CATEGORY_AUX)) or CATEGORY_AUX,
                F_MBOM_MAKE: _norm(material_row.get(F_MAT_MAKE, MAKE_BUY)) or MAKE_BUY,
                F_MBOM_QTY: qty,
                F_MBOM_UNIT: _norm(material_row.get(F_MAT_UNIT, '个')) or '个',
                F_MBOM_LEVEL: child_level,
                F_MBOM_SEQ: next_seq_map[seq_key],
                F_MBOM_STAGE: _norm(material_row.get(F_MAT_STAGE, STAGE_MP)) or STAGE_MP,
                F_MBOM_PARENT_CODE: _norm(parent_node.get(F_MBOM_MAT_CODE, '')),
                F_MBOM_PARENT_VERSION: parent_material_version,
            })
    _append_unique(mbom_nodes, new_nodes, (F_MBOM_CODE, F_MBOM_LEVEL, F_MBOM_SEQ))
