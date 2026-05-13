from __future__ import annotations

from copy import deepcopy
import os

from seed_volume_enhancer import expand_seed_volume, normalize_sequence_relations, resolve_volume_profile

WB_SYSTEM = '系统配置_模板.xlsx'
WB_FACTORY = '工厂资源_模板.xlsx'
WB_PRODUCT = '产品与工艺_模板.xlsx'

SH_ADMIN = '行政组织'
SH_BIZ = '业务组织'
SH_USER = '用户'
SH_SUP = '供应商'
SH_EQ = '设备'
SH_EQ_USER = '设备与用户的关系实体类'
SH_TOOL = '工装工具'
SH_TOOL_INS = '工装检定策略关系'
SH_TOOL_MNT = '工装保养策略关系'
SH_WC = '工作中心'
SH_WC_USER = '工作中心与用户关系'
SH_WC_SUP = '工作中心与供应商的关系'
SH_WC_EQ = '工作中心与设备的关系'
SH_WH = '库房'
SH_LOC = '库位'
SH_PLIB = '工序库'
SH_MAT = '物料'
SH_MBOM = 'MBOM'
SH_MBOM_NODE = 'MBOM节点'
SH_ROUTE = '工艺路线'
SH_OP = '工艺路线工序'
SH_SEQ = '工艺路线工序序列'
SH_OPMAT = '工艺路线工序物料'
SH_STEP = '工艺路线工步'

F_CODE = '*编码'
F_PARENT = '*父组织编码'
F_ADMIN_CODE = '行政组织编码'
F_BIZ_CODE = '业务组织编码'
F_ORG_TYPE = '工厂组织类型'
F_FACTORY_TYPE = '工厂类型'
F_ADMIN_TYPE = '行政组织类型'
F_ID = '*编号'
F_FACTORY_ORG = '*工厂组织'
F_NAME = '*名称'
F_VERSION = '*版本号'
F_ROUTE_TYPE = '*工艺类型'
F_ROUTE_SPEC = '工艺专业'
F_ROUTE_MATERIAL_VERSION = '物料版本号'
F_ROUTE_MATERIAL_CODE = '物料编码'
F_OP_NO = '*工序号'
F_OP_TYPE = '*工序类型'
F_OP_NAME = '*工序名称'
F_OP_ROUTE_VERSION = '*工艺路线版本号'
F_OP_ROUTE_CODE = '*工艺路线编码'
F_OP_WC = '*工作中心编码'
F_OP_PREP = '*定额辅助工时'
F_OP_RUN = '*定额加工时间'
F_OP_UNIT = '*时间单位'
F_OP_OUTPUT_VERSION = '产出物料版本号'
F_OP_OUTPUT_CODE = '产出物料编码'
F_OP_SPEC = '工序专业类型'
F_SEQ_REL = '*接续关系'
F_SEQ_UPSTREAM = '*上道工序号'
F_TIME_UNIT = '*时间单位'
F_EXECUTE_FLAG = '执行标记'
F_YIELD = '产出比'
F_OP_CONTENT = '工序内容'
F_STEP_ROUTE_VERSION = '*工艺路线版本号'
F_STEP_ROUTE_CODE = '*工艺路线编码'
F_STEP_OP_NO = '*工序号'
F_STEP_NO = '*工步序号'
F_STEP_NAME = '*工步名称'
F_STEP_CONTENT = '工步内容'
F_WC_TYPE = '*类型'
F_WC_CLASS = '*分类'

SKIP_PREFIXES = ('CAL-', 'PM-')
DEFAULT_SECURITY = '公开'
DEFAULT_USER_SECURITY = '一般'
DEFAULT_VERSION = 'A.01'
DEFAULT_TIME_UNIT = '分钟'
DEFAULT_EXECUTE = '是'
DEFAULT_YIELD = 1
DEFAULT_ROUTE_TYPE = '一级工艺'
DEFAULT_WC_TYPE = '组织'
TRANSFER_OP_TYPES = {'厂际转工', '厂内转工'}
RELEASE_USER_RULES = {
    (WB_FACTORY, SH_TOOL): (('工装', '标准工时', '刀具', '夹具', '检具'), ('工艺总师', '工艺平台主管', '工艺工程师', '工艺')),
    (WB_PRODUCT, SH_MAT): (('工艺总师', '工艺平台主管', '产品工程师', '工艺工程师', '工艺'), ('工程师',)),
    (WB_PRODUCT, SH_MBOM): (('工艺总师', '工艺平台主管', '工艺工程师', '工艺'), ('工程师',)),
}
PRIMARY_CODE_FIELDS = {
    F_CODE,
    F_ID,
}
REFERENCE_CODE_FIELDS = {
    F_PARENT,
    F_ADMIN_CODE,
    F_BIZ_CODE,
    F_FACTORY_ORG,
    '*设备编码',
    '*用户',
    '*工作中心编码',
    '*供应商',
    '*库房编码',
    '*物料编码',
    '物料编码',
    '父物料编码',
    '*MBOM编码',
    '*工艺路线编码',
    '产出物料编码',
    '*工装工具编码',
}


def _append_missing(rows: list[dict], new_rows: list[dict], key_fields: tuple[str, ...]) -> None:
    existing = {tuple(str(row.get(field, '')).strip() for field in key_fields) for row in rows}
    for row in new_rows:
        key = tuple(str(row.get(field, '')).strip() for field in key_fields)
        if key in existing:
            continue
        rows.append(deepcopy(row))
        existing.add(key)


def _rows(seed: dict, workbook: str, sheet: str) -> list[dict]:
    return seed['workbooks'][workbook][sheet]


def _find_row(rows: list[dict], code_field: str, value: str) -> dict | None:
    for row in rows:
        if str(row.get(code_field, '')).strip() == value:
            return row
    return None


def _upsert_row(rows: list[dict], key_field: str, row: dict) -> None:
    existing = _find_row(rows, key_field, str(row.get(key_field, '')).strip())
    if existing is None:
        rows.append(deepcopy(row))
        return
    existing.update(deepcopy(row))


def _op_sort_key(value: str) -> tuple[int, str]:
    text = str(value).strip()
    digits = ''.join(ch for ch in text if ch.isdigit())
    if digits:
        return int(digits), text
    return 999999, text


def rebuild_route_sequences(seed: dict) -> dict:
    product = seed.get('workbooks', {}).get(WB_PRODUCT, {})
    ops = product.get(SH_OP, [])
    grouped_ops: dict[tuple[str, str], list[dict]] = {}
    for row in ops:
        key = (str(row.get(F_OP_ROUTE_VERSION, '')).strip(), str(row.get(F_OP_ROUTE_CODE, '')).strip())
        grouped_ops.setdefault(key, []).append(row)

    new_sequences: list[dict] = []
    for (route_version, route_code), route_ops in grouped_ops.items():
        ordered = sorted(route_ops, key=lambda row: _op_sort_key(row.get(F_OP_NO, '')))
        for previous, current in zip(ordered, ordered[1:]):
            new_sequences.append({
                F_SEQ_REL: 'ES',
                F_OP_NO: str(current.get(F_OP_NO, '')).strip(),
                F_SEQ_UPSTREAM: str(previous.get(F_OP_NO, '')).strip(),
                F_OP_ROUTE_VERSION: route_version,
                F_OP_ROUTE_CODE: route_code,
            })

    product[SH_SEQ] = new_sequences
    return seed


def remove_transfer_operations(seed: dict) -> dict:
    factory = seed.get('workbooks', {}).get(WB_FACTORY, {})
    product = seed.get('workbooks', {}).get(WB_PRODUCT, {})

    factory[SH_PLIB] = [
        row for row in factory.get(SH_PLIB, [])
        if str(row.get(F_OP_TYPE, '')).strip() not in TRANSFER_OP_TYPES
    ]

    kept_ops: list[dict] = []
    kept_op_keys: set[tuple[str, str, str]] = set()
    kept_route_keys: set[tuple[str, str]] = set()
    for row in product.get(SH_OP, []):
        if str(row.get(F_OP_TYPE, '')).strip() in TRANSFER_OP_TYPES:
            continue
        route_key = (str(row.get(F_OP_ROUTE_VERSION, '')).strip(), str(row.get(F_OP_ROUTE_CODE, '')).strip())
        op_key = route_key + (str(row.get(F_OP_NO, '')).strip(),)
        kept_ops.append(row)
        kept_route_keys.add(route_key)
        kept_op_keys.add(op_key)

    product[SH_OP] = kept_ops
    product[SH_ROUTE] = [
        row for row in product.get(SH_ROUTE, [])
        if (str(row.get(F_VERSION, '')).strip(), str(row.get(F_CODE, '')).strip()) in kept_route_keys
    ]
    product[SH_OPMAT] = [
        row for row in product.get(SH_OPMAT, [])
        if (
            str(row.get(F_OP_ROUTE_VERSION, '')).strip(),
            str(row.get(F_OP_ROUTE_CODE, '')).strip(),
            str(row.get(F_OP_NO, '')).strip(),
        ) in kept_op_keys
    ]
    product[SH_STEP] = [
        row for row in product.get(SH_STEP, [])
        if (
            str(row.get(F_STEP_ROUTE_VERSION, '')).strip(),
            str(row.get(F_STEP_ROUTE_CODE, '')).strip(),
            str(row.get(F_STEP_OP_NO, '')).strip(),
        ) in kept_op_keys
    ]

    referenced_wc_codes = {str(row.get(F_OP_WC, '')).strip() for row in kept_ops if str(row.get(F_OP_WC, '')).strip()}
    transfer_wc_codes = {
        str(row.get(F_CODE, '')).strip()
        for row in factory.get(SH_WC, [])
        if any(token in ' '.join([
            str(row.get(F_CODE, '')).strip().upper(),
            str(row.get(F_NAME, '')).strip(),
            str(row.get('备注', '')).strip(),
        ]) for token in ('TRANSFER', '转工'))
    }
    removable_wc_codes = {code for code in transfer_wc_codes if code and code not in referenced_wc_codes}
    if removable_wc_codes:
        factory[SH_WC] = [row for row in factory.get(SH_WC, []) if str(row.get(F_CODE, '')).strip() not in removable_wc_codes]
        factory[SH_WC_USER] = [row for row in factory.get(SH_WC_USER, []) if str(row.get(F_OP_WC, '')).strip() not in removable_wc_codes]
        factory[SH_WC_EQ] = [row for row in factory.get(SH_WC_EQ, []) if str(row.get(F_OP_WC, '')).strip() not in removable_wc_codes]
        factory[SH_WC_SUP] = [row for row in factory.get(SH_WC_SUP, []) if str(row.get(F_OP_WC, '')).strip() not in removable_wc_codes]

    rebuild_route_sequences(seed)
    return seed


def apply_project_collaboration(seed: dict) -> dict:
    metadata = seed.setdefault('metadata', {})
    collaboration = metadata.get('project_collaboration') or {}
    if not collaboration or not collaboration.get('enabled'):
        return seed

    admin_rows = _rows(seed, WB_SYSTEM, SH_ADMIN)
    biz_rows = _rows(seed, WB_SYSTEM, SH_BIZ)
    wc_rows = _rows(seed, WB_FACTORY, SH_WC)
    process_rows = _rows(seed, WB_FACTORY, SH_PLIB)
    route_rows = _rows(seed, WB_PRODUCT, SH_ROUTE)
    op_rows = _rows(seed, WB_PRODUCT, SH_OP)
    step_rows = _rows(seed, WB_PRODUCT, SH_STEP)

    version = str(metadata.get('default_version') or DEFAULT_VERSION).strip() or DEFAULT_VERSION
    security = str(metadata.get('default_security') or DEFAULT_SECURITY).strip() or DEFAULT_SECURITY

    admin_config = collaboration.get('admin') or {}
    biz_config = collaboration.get('biz') or {}
    route_config = collaboration.get('route') or {}
    phases = collaboration.get('phases') or []
    if not admin_config or not biz_config or not route_config or not phases:
        return seed

    admin_code = str(admin_config.get('code', '')).strip()
    biz_code = str(biz_config.get('code', '')).strip()
    route_code = str(route_config.get('code', '')).strip()
    material_code = str(route_config.get('material_code', '')).strip()
    if not admin_code or not biz_code or not route_code or not material_code:
        return seed

    _upsert_row(admin_rows, F_CODE, {
        F_PARENT: str(admin_config.get('parent', '0')).strip() or '0',
        F_ADMIN_TYPE: '工厂',
        F_CODE: admin_code,
        F_NAME: str(admin_config.get('name', '生产项目部')).strip() or '生产项目部',
        '简称': str(admin_config.get('short', '项目部')).strip() or '项目部',
    })
    _upsert_row(biz_rows, F_CODE, {
        F_PARENT: str(biz_config.get('parent', '0')).strip() or '0',
        '*密级': security,
        F_CODE: biz_code,
        F_NAME: str(biz_config.get('name', '生产项目部')).strip() or '生产项目部',
        '简称': str(biz_config.get('short', '项目部')).strip() or '项目部',
        F_ORG_TYPE: '工厂',
        F_ADMIN_CODE: admin_code,
        F_FACTORY_TYPE: str(biz_config.get('factory_type', '机械加工专业')).strip() or '机械加工专业',
        '备注': str(biz_config.get('remark', '用于一级工艺与协同计划排产')).strip() or '用于一级工艺与协同计划排产',
    })

    _upsert_row(route_rows, F_CODE, {
        F_NAME: str(route_config.get('name', '协同一级工艺')).strip() or '协同一级工艺',
        F_ROUTE_TYPE: str(route_config.get('route_type', DEFAULT_ROUTE_TYPE)).strip() or DEFAULT_ROUTE_TYPE,
        F_ROUTE_SPEC: str(route_config.get('spec', '通用')).strip() or '通用',
        F_ROUTE_MATERIAL_VERSION: version,
        F_ROUTE_MATERIAL_CODE: material_code,
        F_VERSION: version,
        F_CODE: route_code,
        '*密级': security,
        F_FACTORY_ORG: biz_code,
        '备注': str(route_config.get('remark', '项目部一级协同工艺')).strip() or '项目部一级协同工艺',
    })

    for index, phase in enumerate(phases, start=1):
        wc_code = str(phase.get('wc_code', '')).strip()
        op_no = str(phase.get('no', '')).strip()
        phase_name = str(phase.get('name', '')).strip()
        if not wc_code or not op_no or not phase_name:
            continue

        op_type = str(phase.get('op_type', '加工')).strip() or '加工'
        wc_class = str(phase.get('wc_class', '检验' if op_type == '检验' else '加工')).strip() or ('检验' if op_type == '检验' else '加工')
        op_spec = str(phase.get('op_spec', '机械加工专业')).strip() or '机械加工专业'
        content = str(phase.get('content', f'{phase_name}')).strip() or phase_name
        prep = int(phase.get('prep', 8) or 8)
        run = int(phase.get('run', 12) or 12)
        output_code = str(phase.get('output_code', material_code)).strip() or material_code
        steps = phase.get('steps') or [
            ('确认阶段产能', f'按{phase_name}对应工厂产能确认阶段排产与执行状态'),
            ('完成阶段交付', f'完成{phase_name}并更新项目部一级协同节点状态'),
        ]

        _upsert_row(wc_rows, F_CODE, {
            F_NAME: str(phase.get('wc_name', phase_name)).strip() or phase_name,
            F_WC_TYPE: str(phase.get('wc_type', DEFAULT_WC_TYPE)).strip() or DEFAULT_WC_TYPE,
            F_WC_CLASS: wc_class,
            F_CODE: wc_code,
            '*密级': security,
            F_FACTORY_ORG: biz_code,
            '备注': str(phase.get('remark', f'{phase_name}对应的项目部协同排产中心')).strip() or f'{phase_name}对应的项目部协同排产中心',
        })
        _append_missing(process_rows, [{
            '序专业类型': op_spec,
            F_NAME: phase_name,
            F_OP_TYPE: op_type,
            F_OP_WC: wc_code,
            '*定额准备时间': prep,
            '*定额加工时间': run,
            F_EXECUTE_FLAG: DEFAULT_EXECUTE,
            F_TIME_UNIT: DEFAULT_TIME_UNIT,
            F_YIELD: DEFAULT_YIELD,
            F_OP_CONTENT: content,
            '*密级': security,
        }], (F_NAME, F_OP_TYPE, F_OP_WC))
        _append_missing(op_rows, [{
            F_OP_NO: op_no,
            F_OP_TYPE: op_type,
            F_OP_CONTENT: content,
            F_OP_WC: wc_code,
            F_OP_PREP: prep,
            F_OP_RUN: run,
            F_OP_UNIT: DEFAULT_TIME_UNIT,
            F_EXECUTE_FLAG: DEFAULT_EXECUTE,
            F_YIELD: DEFAULT_YIELD,
            F_OP_ROUTE_VERSION: version,
            F_OP_ROUTE_CODE: route_code,
            F_OP_NAME: phase_name,
            F_OP_OUTPUT_VERSION: version,
            F_OP_OUTPUT_CODE: output_code,
            F_OP_SPEC: op_spec,
        }], (F_OP_ROUTE_VERSION, F_OP_ROUTE_CODE, F_OP_NO))

        for step_index, step in enumerate(steps, start=1):
            if isinstance(step, (list, tuple)):
                step_name, step_content = step
            else:
                step_name = str(step).strip() or phase_name
                step_content = step_name
            _append_missing(step_rows, [{
                F_STEP_ROUTE_VERSION: version,
                F_STEP_ROUTE_CODE: route_code,
                F_STEP_OP_NO: op_no,
                F_STEP_NO: f'{step_index * 10:02d}',
                F_STEP_NAME: str(step_name).strip() or phase_name,
                F_STEP_CONTENT: str(step_content).strip() or phase_name,
            }], (F_STEP_ROUTE_VERSION, F_STEP_ROUTE_CODE, F_STEP_OP_NO, F_STEP_NO))

    rebuild_route_sequences(seed)
    return seed


def _namespace_code(value: str, namespace: str) -> str:
    raw = str(value).strip()
    if not raw or raw == '0' or raw.startswith(SKIP_PREFIXES):
        return raw
    if '-' not in raw:
        return raw
    head, tail = raw.split('-', 1)
    if tail.startswith(f'{namespace}-'):
        return raw
    return f'{head}-{namespace}-{tail}'


def apply_namespace(seed: dict, namespace: str) -> dict:
    seed.setdefault('metadata', {})['namespace'] = namespace
    seed['external_references'] = ['0']
    for workbook in seed.get('workbooks', {}).values():
        for rows in workbook.values():
            for row in rows:
                for field in list(row.keys()):
                    if field in PRIMARY_CODE_FIELDS or field in REFERENCE_CODE_FIELDS:
                        row[field] = _namespace_code(row.get(field, ''), namespace)
    return seed


def _resolve_seed_volume_profile(seed: dict, volume_profile: str | None = None) -> str:
    metadata = seed.setdefault('metadata', {})
    requested_profile = str(volume_profile or '').strip()
    if not requested_profile:
        requested_profile = str(metadata.get('volume_profile') or '').strip()
    if not requested_profile:
        requested_profile = str(os.getenv('MOM_SEED_VOLUME_PROFILE') or '').strip()
    resolved_profile = resolve_volume_profile(requested_profile)
    metadata['volume_profile'] = resolved_profile
    return resolved_profile


def normalize_user_codes(seed: dict, namespace: str) -> dict:
    users = _rows(seed, WB_SYSTEM, SH_USER)
    if not users:
        return seed

    digits = ''.join(ch for ch in namespace if ch.isdigit())
    bucket = (digits[:2] if len(digits) >= 2 else digits).ljust(2, '0')
    width = max(2, len(str(len(users))))

    user_map: dict[str, str] = {}
    for index, row in enumerate(users, start=1):
        old_code = str(row.get(F_ID, '')).strip()
        if not old_code:
            continue
        user_map[old_code] = f'K{bucket}{index:0{width}d}'

    for row in users:
        old_code = str(row.get(F_ID, '')).strip()
        if old_code in user_map:
            row[F_ID] = user_map[old_code]

    ref_fields = {F_ID, '*用户', '计划员'}
    for workbook in seed.get('workbooks', {}).values():
        for rows in workbook.values():
            for row in rows:
                for field in ref_fields:
                    value = str(row.get(field, '')).strip()
                    if value in user_map:
                        row[field] = user_map[value]
    return seed



def _match_release_user(users: list[dict], keyword_groups: tuple[tuple[str, ...], ...]) -> str:
    if not users:
        return ''

    for keywords in keyword_groups:
        for row in users:
            text = ' '.join(str(row.get(field, '')).strip() for field in ('备注', '名称'))
            if any(keyword and keyword in text for keyword in keywords):
                return str(row.get(F_ID, '')).strip()

    for row in users:
        code = str(row.get(F_ID, '')).strip()
        if code:
            return code
    return ''


def normalize_release_user(seed: dict) -> dict:
    publisher_field = '发布人'
    users = _rows(seed, WB_SYSTEM, SH_USER)
    for (workbook, sheet), keyword_groups in RELEASE_USER_RULES.items():
        release_user = _match_release_user(users, keyword_groups)
        if not release_user:
            continue
        for row in _rows(seed, workbook, sheet):
            row[publisher_field] = release_user
    for row in _rows(seed, WB_PRODUCT, SH_ROUTE):
        row[publisher_field] = ''
    return seed


def normalize_poc_security(seed: dict) -> dict:
    security_field = '*密级'
    user_security_field = '用户安全等级'
    metadata = seed.setdefault('metadata', {})
    metadata['default_security'] = DEFAULT_SECURITY
    for workbook in seed.get('workbooks', {}).values():
        for rows in workbook.values():
            for row in rows:
                if security_field in row:
                    row[security_field] = DEFAULT_SECURITY
                if user_security_field in row:
                    row[user_security_field] = DEFAULT_USER_SECURITY
    return seed

def normalize_storage_factory_org(seed: dict) -> dict:
    biz_rows = _rows(seed, WB_SYSTEM, SH_BIZ)
    if not biz_rows:
        return seed

    plant_type = '工厂'
    name_field = '*名称'
    warehouse_code_field = '*库房编码'

    parent_map: dict[str, str] = {}
    org_type_map: dict[str, str] = {}
    org_name_map: dict[str, str] = {}
    plant_codes: list[str] = []
    for row in biz_rows:
        code = str(row.get(F_CODE, '')).strip()
        if not code:
            continue
        org_type = str(row.get(F_ORG_TYPE, '')).strip()
        parent_map[code] = str(row.get(F_PARENT, '')).strip()
        org_type_map[code] = org_type
        org_name_map[code] = str(row.get(name_field, '')).strip()
        if org_type == plant_type:
            plant_codes.append(code)

    ancestor_cache: dict[str, str] = {}

    def resolve_ancestor_plant(code: str) -> str:
        current = str(code).strip()
        if not current:
            return ''
        if current in ancestor_cache:
            return ancestor_cache[current]

        origin = current
        visited: set[str] = set()
        while current and current != '0' and current not in visited:
            visited.add(current)
            if org_type_map.get(current) == plant_type:
                ancestor_cache[origin] = current
                return current
            current = parent_map.get(current, '')

        ancestor_cache[origin] = ''
        return ''

    def infer_shared_storage_plant(row: dict) -> str:
        if not plant_codes:
            return ''
        if len(plant_codes) == 1:
            return plant_codes[0]

        code_text = str(row.get(F_CODE, '')).strip().upper()
        name_text = str(row.get(name_field, '')).strip()
        combined = f'{code_text} {name_text}'
        candidate_groups = (
            (('FG', '成品', '待发', '包装', '放行'), ('试验', '包装', '总装')),
            (('WIP', '在制', '转工', '待装', '热后'), ('总装', '试验', '热处理')),
            (('RAW', '原材', '毛坯', '钢材', '外购'), ('机加', '箱体', '齿轮', '机械加工')),
        )
        for hints, plant_keywords in candidate_groups:
            if any(hint in combined for hint in hints):
                for plant_code in plant_codes:
                    plant_name = org_name_map.get(plant_code, '')
                    if any(keyword in plant_name for keyword in plant_keywords):
                        return plant_code

        if 'FG' in code_text or '成品' in combined:
            return plant_codes[-1]
        return plant_codes[0]

    factory = seed.get('workbooks', {}).get(WB_FACTORY, {})
    warehouses = factory.get(SH_WH, [])
    locations = factory.get(SH_LOC, [])

    warehouse_plant_map: dict[str, str] = {}
    for row in warehouses:
        warehouse_code = str(row.get(F_CODE, '')).strip()
        current_org = str(row.get(F_FACTORY_ORG, '')).strip()
        plant_org = resolve_ancestor_plant(current_org)
        if not plant_org:
            plant_org = infer_shared_storage_plant(row)
        if plant_org:
            row[F_FACTORY_ORG] = plant_org
        if warehouse_code:
            warehouse_plant_map[warehouse_code] = str(row.get(F_FACTORY_ORG, '')).strip()

    for row in locations:
        warehouse_code = str(row.get(warehouse_code_field, '')).strip()
        current_org = str(row.get(F_FACTORY_ORG, '')).strip()
        plant_org = warehouse_plant_map.get(warehouse_code) or resolve_ancestor_plant(current_org)
        if not plant_org:
            plant_org = infer_shared_storage_plant(row)
        if plant_org:
            row[F_FACTORY_ORG] = plant_org

    return seed


def clear_tool_strategy_relations(seed: dict) -> dict:
    factory = seed.get('workbooks', {}).get(WB_FACTORY, {})
    factory[SH_TOOL_INS] = []
    factory[SH_TOOL_MNT] = []
    return seed


def filter_wc_supplier_relations(seed: dict) -> dict:
    factory = seed.get('workbooks', {}).get(WB_FACTORY, {})
    workcenters = factory.get(SH_WC, [])
    wc_type_field = '*类型'
    wc_code_field = '*工作中心编码'
    outsource_type = '外委'
    wc_type_map = {str(row.get(F_CODE, '')).strip(): str(row.get(wc_type_field, '')).strip() for row in workcenters}
    relations = factory.get(SH_WC_SUP, [])
    filtered = []
    for row in relations:
        wc_code = str(row.get(wc_code_field, '')).strip()
        if wc_type_map.get(wc_code) == outsource_type:
            filtered.append(row)
    factory[SH_WC_SUP] = filtered
    return seed

def _upgrade_b737(seed: dict) -> None:
    admins = _rows(seed, WB_SYSTEM, SH_ADMIN)
    bizs = _rows(seed, WB_SYSTEM, SH_BIZ)
    users = _rows(seed, WB_SYSTEM, SH_USER)
    eqs = _rows(seed, WB_FACTORY, SH_EQ)
    wcs = _rows(seed, WB_FACTORY, SH_WC)

    admin_updates = {
        'ADM-737BU': {F_PARENT: 'ADM-AERO', F_ADMIN_TYPE: '部门', '*名称': '737发动机事业部', '简称': '737事业部'},
        'ADM-PLANT': {F_PARENT: 'ADM-737BU', F_ADMIN_TYPE: '部门', '*名称': 'LEAP-1B协同制造中心', '简称': 'LEAP中心'},
    }
    for code, updates in admin_updates.items():
        row = _find_row(admins, F_CODE, code)
        if row:
            row.update(updates)

    _append_missing(admins, [
        {F_PARENT: 'ADM-PLANT', F_ADMIN_TYPE: '工厂', F_CODE: 'ADM-FAN-PLANT', '*名称': '风扇与复材工厂', '简称': '风扇复材'},
        {F_PARENT: 'ADM-PLANT', F_ADMIN_TYPE: '工厂', F_CODE: 'ADM-COMP-PLANT', '*名称': '压气机工厂', '简称': '压气机厂'},
        {F_PARENT: 'ADM-PLANT', F_ADMIN_TYPE: '工厂', F_CODE: 'ADM-COMB-PLANT', '*名称': '燃烧室工厂', '简称': '燃烧室厂'},
        {F_PARENT: 'ADM-PLANT', F_ADMIN_TYPE: '工厂', F_CODE: 'ADM-TURB-PLANT', '*名称': '涡轮工厂', '简称': '涡轮厂'},
        {F_PARENT: 'ADM-PLANT', F_ADMIN_TYPE: '工厂', F_CODE: 'ADM-AGB-PLANT', '*名称': '附件传动工厂', '简称': '附件传动'},
        {F_PARENT: 'ADM-PLANT', F_ADMIN_TYPE: '工厂', F_CODE: 'ADM-FINAL-PLANT', '*名称': '总装试车工厂', '简称': '总装试车'},
    ], (F_CODE,))

    biz_updates = {
        'BIZ-737BU': {F_PARENT: 'BIZ-AERO', F_ORG_TYPE: '部门', F_ADMIN_CODE: 'ADM-737BU'},
        'BIZ-LEAP-CENTER': {F_PARENT: 'BIZ-737BU', F_ORG_TYPE: '部门', F_ADMIN_CODE: 'ADM-PLANT'},
        'BIZ-FAN': {F_PARENT: 'BIZ-LEAP-CENTER', F_ORG_TYPE: '工厂', F_ADMIN_CODE: 'ADM-FAN-PLANT', F_FACTORY_TYPE: '机械加工专业', '*名称': '风扇与复材工厂', '简称': '风扇复材'},
        'BIZ-COMP': {F_PARENT: 'BIZ-LEAP-CENTER', F_ORG_TYPE: '工厂', F_ADMIN_CODE: 'ADM-COMP-PLANT', F_FACTORY_TYPE: '机械加工专业', '*名称': '压气机工厂', '简称': '压气机厂'},
        'BIZ-COMB': {F_PARENT: 'BIZ-LEAP-CENTER', F_ORG_TYPE: '工厂', F_ADMIN_CODE: 'ADM-COMB-PLANT', F_FACTORY_TYPE: '装配专业', '*名称': '燃烧室工厂', '简称': '燃烧室厂'},
        'BIZ-TURB': {F_PARENT: 'BIZ-LEAP-CENTER', F_ORG_TYPE: '工厂', F_ADMIN_CODE: 'ADM-TURB-PLANT', F_FACTORY_TYPE: '装配专业', '*名称': '涡轮工厂', '简称': '涡轮厂'},
        'BIZ-AGB': {F_PARENT: 'BIZ-LEAP-CENTER', F_ORG_TYPE: '工厂', F_ADMIN_CODE: 'ADM-AGB-PLANT', F_FACTORY_TYPE: '装配专业', '*名称': '附件传动工厂', '简称': '附件传动'},
        'BIZ-FINAL': {F_PARENT: 'BIZ-LEAP-CENTER', F_ORG_TYPE: '工厂', F_ADMIN_CODE: 'ADM-FINAL-PLANT', F_FACTORY_TYPE: '装配专业', '*名称': '总装试车工厂', '简称': '总装试车'},
        'BIZ-QUALITY': {F_PARENT: 'BIZ-LEAP-CENTER', F_ORG_TYPE: '部门', F_ADMIN_CODE: 'ADM-QA'},
        'BIZ-WARE': {F_PARENT: 'BIZ-LEAP-CENTER', F_ORG_TYPE: '部门', F_ADMIN_CODE: 'ADM-WM'},
        'BIZ-DIGI': {F_PARENT: 'BIZ-LEAP-CENTER', F_ORG_TYPE: '部门', F_ADMIN_CODE: 'ADM-DIGI'},
    }
    for code, updates in biz_updates.items():
        row = _find_row(bizs, F_CODE, code)
        if row:
            row.update(updates)

    _append_missing(bizs, [
        {F_PARENT: 'BIZ-FAN', '*密级': '内部', F_CODE: 'BIZ-FAN-BLADE-WS', '*名称': '风扇叶片车间', '简称': '叶片车间', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-FAN-PLANT'},
        {F_PARENT: 'BIZ-FAN-BLADE-WS', '*密级': '内部', F_CODE: 'BIZ-FAN-BLADE-SEC', '*名称': '叶片铺层工段', '简称': '铺层工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-FAN-PLANT'},
        {F_PARENT: 'BIZ-FAN-BLADE-SEC', '*密级': '内部', F_CODE: 'BIZ-FAN-BLADE-A', '*名称': '叶片铺层甲班', '简称': '铺层甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-FAN-PLANT'},
        {F_PARENT: 'BIZ-FAN', '*密级': '内部', F_CODE: 'BIZ-FAN-CASE-WS', '*名称': '风扇机匣车间', '简称': '机匣车间', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-FAN-PLANT'},
        {F_PARENT: 'BIZ-FAN-CASE-WS', '*密级': '内部', F_CODE: 'BIZ-FAN-CASE-SEC', '*名称': '机匣成型工段', '简称': '机匣工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-FAN-PLANT'},
        {F_PARENT: 'BIZ-FAN-CASE-SEC', '*密级': '内部', F_CODE: 'BIZ-FAN-CASE-A', '*名称': '机匣成型甲班', '简称': '机匣甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-FAN-PLANT'},
        {F_PARENT: 'BIZ-COMP', '*密级': '内部', F_CODE: 'BIZ-COMP-LPC-WS', '*名称': '低压压气机车间', '简称': 'LPC车间', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-COMP-PLANT'},
        {F_PARENT: 'BIZ-COMP-LPC-WS', '*密级': '内部', F_CODE: 'BIZ-COMP-LPC-SEC', '*名称': 'LPC转子工段', '简称': 'LPC工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-COMP-PLANT'},
        {F_PARENT: 'BIZ-COMP-LPC-SEC', '*密级': '内部', F_CODE: 'BIZ-COMP-LPC-A', '*名称': 'LPC装配甲班', '简称': 'LPC甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-COMP-PLANT'},
        {F_PARENT: 'BIZ-COMP', '*密级': '内部', F_CODE: 'BIZ-COMP-HPC-WS', '*名称': '高压压气机车间', '简称': 'HPC车间', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-COMP-PLANT'},
        {F_PARENT: 'BIZ-COMP-HPC-WS', '*密级': '内部', F_CODE: 'BIZ-COMP-HPC-SEC', '*名称': 'HPC盘鼓工段', '简称': 'HPC工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-COMP-PLANT'},
        {F_PARENT: 'BIZ-COMP-HPC-SEC', '*密级': '内部', F_CODE: 'BIZ-COMP-HPC-A', '*名称': 'HPC装配甲班', '简称': 'HPC甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-COMP-PLANT'},
        {F_PARENT: 'BIZ-COMB', '*密级': '内部', F_CODE: 'BIZ-COMB-LINER-WS', '*名称': '燃烧室衬套车间', '简称': '衬套车间', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-COMB-PLANT'},
        {F_PARENT: 'BIZ-COMB-LINER-WS', '*密级': '内部', F_CODE: 'BIZ-COMB-LINER-SEC', '*名称': '衬套焊装工段', '简称': '衬套工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-COMB-PLANT'},
        {F_PARENT: 'BIZ-COMB-LINER-SEC', '*密级': '内部', F_CODE: 'BIZ-COMB-LINER-A', '*名称': '衬套焊装甲班', '简称': '衬套甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-COMB-PLANT'},
        {F_PARENT: 'BIZ-TURB', '*密级': '内部', F_CODE: 'BIZ-TURB-HPT-WS', '*名称': '高压涡轮车间', '简称': 'HPT车间', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-TURB-PLANT'},
        {F_PARENT: 'BIZ-TURB-HPT-WS', '*密级': '内部', F_CODE: 'BIZ-TURB-HPT-SEC', '*名称': 'HPT转子工段', '简称': 'HPT工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-TURB-PLANT'},
        {F_PARENT: 'BIZ-TURB-HPT-SEC', '*密级': '内部', F_CODE: 'BIZ-TURB-HPT-A', '*名称': 'HPT装配甲班', '简称': 'HPT甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-TURB-PLANT'},
        {F_PARENT: 'BIZ-TURB', '*密级': '内部', F_CODE: 'BIZ-TURB-LPT-WS', '*名称': '低压涡轮车间', '简称': 'LPT车间', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-TURB-PLANT'},
        {F_PARENT: 'BIZ-TURB-LPT-WS', '*密级': '内部', F_CODE: 'BIZ-TURB-LPT-SEC', '*名称': 'LPT转子工段', '简称': 'LPT工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-TURB-PLANT'},
        {F_PARENT: 'BIZ-TURB-LPT-SEC', '*密级': '内部', F_CODE: 'BIZ-TURB-LPT-A', '*名称': 'LPT装配甲班', '简称': 'LPT甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-TURB-PLANT'},
        {F_PARENT: 'BIZ-AGB', '*密级': '内部', F_CODE: 'BIZ-AGB-ASM-WS', '*名称': '附件机匣装配车间', '简称': '附件装配', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-AGB-PLANT'},
        {F_PARENT: 'BIZ-AGB-ASM-WS', '*密级': '内部', F_CODE: 'BIZ-AGB-ASM-SEC', '*名称': '齿轮箱装配工段', '简称': '齿箱工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-AGB-PLANT'},
        {F_PARENT: 'BIZ-AGB-ASM-SEC', '*密级': '内部', F_CODE: 'BIZ-AGB-ASM-A', '*名称': '齿轮箱装配甲班', '简称': '齿箱甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-AGB-PLANT'},
        {F_PARENT: 'BIZ-AGB', '*密级': '内部', F_CODE: 'BIZ-AGB-CTRL-WS', '*名称': '控制集成车间', '简称': '控制集成', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-AGB-PLANT'},
        {F_PARENT: 'BIZ-AGB-CTRL-WS', '*密级': '内部', F_CODE: 'BIZ-AGB-CTRL-SEC', '*名称': 'FADEC集成工段', '简称': 'FADEC工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-AGB-PLANT'},
        {F_PARENT: 'BIZ-AGB-CTRL-SEC', '*密级': '内部', F_CODE: 'BIZ-AGB-CTRL-A', '*名称': 'FADEC集成甲班', '简称': 'FADEC甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-AGB-PLANT'},
        {F_PARENT: 'BIZ-FINAL', '*密级': '内部', F_CODE: 'BIZ-FINAL-CORE-WS', '*名称': '核心机装配车间', '简称': '核心机装配', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
        {F_PARENT: 'BIZ-FINAL-CORE-WS', '*密级': '内部', F_CODE: 'BIZ-FINAL-CORE-SEC', '*名称': '核心机对接工段', '简称': '核心机工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
        {F_PARENT: 'BIZ-FINAL-CORE-SEC', '*密级': '内部', F_CODE: 'BIZ-FINAL-CORE-A', '*名称': '核心机装配甲班', '简称': '核心机甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
        {F_PARENT: 'BIZ-FINAL', '*密级': '内部', F_CODE: 'BIZ-FINAL-ASM-WS', '*名称': '整机总装车间', '简称': '整机总装', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
        {F_PARENT: 'BIZ-FINAL-ASM-WS', '*密级': '内部', F_CODE: 'BIZ-FINAL-ASM-SEC', '*名称': '整机总装工段', '简称': '总装工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
        {F_PARENT: 'BIZ-FINAL-ASM-SEC', '*密级': '内部', F_CODE: 'BIZ-FINAL-ASM-A', '*名称': '整机总装甲班', '简称': '总装甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
        {F_PARENT: 'BIZ-FINAL', '*密级': '内部', F_CODE: 'BIZ-FINAL-TEST-WS', '*名称': '整机试车车间', '简称': '整机试车', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
        {F_PARENT: 'BIZ-FINAL-TEST-WS', '*密级': '内部', F_CODE: 'BIZ-FINAL-TEST-SEC', '*名称': '性能试车工段', '简称': '试车工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
        {F_PARENT: 'BIZ-FINAL-TEST-SEC', '*密级': '内部', F_CODE: 'BIZ-FINAL-TEST-A', '*名称': '性能试车甲班', '简称': '试车甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
    ], (F_CODE,))

    user_updates = {
        'U-LEAP-007': {F_ADMIN_CODE: 'ADM-FAN-PLANT', F_BIZ_CODE: 'BIZ-FAN-BLADE-SEC', '备注': '复材叶片工艺工程师'},
        'U-LEAP-008': {F_ADMIN_CODE: 'ADM-COMP-PLANT', F_BIZ_CODE: 'BIZ-COMP-HPC-SEC', '备注': '高压压气机工艺工程师'},
        'U-LEAP-010': {F_ADMIN_CODE: 'ADM-FINAL-PLANT', F_BIZ_CODE: 'BIZ-FINAL-TEST-SEC', '备注': '试车平台主管'},
        'U-LEAP-011': {F_ADMIN_CODE: 'ADM-FINAL-PLANT', F_BIZ_CODE: 'BIZ-FINAL-ASM-SEC', '备注': '整机总装工程师'},
        'U-LEAP-012': {F_ADMIN_CODE: 'ADM-FAN-PLANT', F_BIZ_CODE: 'BIZ-FAN-BLADE-A', '备注': '风扇叶片班组长'},
        'U-LEAP-013': {F_ADMIN_CODE: 'ADM-COMP-PLANT', F_BIZ_CODE: 'BIZ-COMP-HPC-A', '备注': '压气机班组长'},
        'U-LEAP-014': {F_ADMIN_CODE: 'ADM-COMB-PLANT', F_BIZ_CODE: 'BIZ-COMB-LINER-A', '备注': '燃烧室班组长'},
        'U-LEAP-015': {F_ADMIN_CODE: 'ADM-TURB-PLANT', F_BIZ_CODE: 'BIZ-TURB-HPT-A', '备注': '涡轮班组长'},
        'U-LEAP-016': {F_ADMIN_CODE: 'ADM-AGB-PLANT', F_BIZ_CODE: 'BIZ-AGB-CTRL-SEC', '备注': '控制系统集成工程师'},
        'U-LEAP-017': {F_ADMIN_CODE: 'ADM-WM', F_BIZ_CODE: 'BIZ-WARE', '备注': '仓储物流计划员'},
        'U-LEAP-018': {F_ADMIN_CODE: 'ADM-PLANT', F_BIZ_CODE: 'BIZ-LEAP-CENTER', '备注': '设备工程师'},
        'U-LEAP-020': {F_ADMIN_CODE: 'ADM-FINAL-PLANT', F_BIZ_CODE: 'BIZ-FINAL-TEST-A', '备注': '性能试车工程师'},
    }
    for code, updates in user_updates.items():
        row = _find_row(users, F_ID, code)
        if row:
            row.update(updates)

    _append_missing(users, [
        {F_ID: 'U-LEAP-021', '名称': '沈沐尧', '备注': '主计划员', '用户安全等级': '重要', '性别': '男', F_ADMIN_CODE: 'ADM-SCM', F_BIZ_CODE: 'BIZ-LEAP-CENTER'},
        {F_ID: 'U-LEAP-022', '名称': '陆清妍', '备注': '仓库管理员', '用户安全等级': '一般', '性别': '女', F_ADMIN_CODE: 'ADM-WM', F_BIZ_CODE: 'BIZ-WARE'},
        {F_ID: 'U-LEAP-023', '名称': '宋知远', '备注': '设备维修工', '用户安全等级': '一般', '性别': '男', F_ADMIN_CODE: 'ADM-PLANT', F_BIZ_CODE: 'BIZ-LEAP-CENTER'},
        {F_ID: 'U-LEAP-024', '名称': '姜雨宁', '备注': '设备保养员', '用户安全等级': '一般', '性别': '女', F_ADMIN_CODE: 'ADM-PLANT', F_BIZ_CODE: 'BIZ-LEAP-CENTER'},
        {F_ID: 'U-LEAP-025', '名称': '贺言之', '备注': '风扇复材操作工', '用户安全等级': '一般', '性别': '男', F_ADMIN_CODE: 'ADM-FAN-PLANT', F_BIZ_CODE: 'BIZ-FAN-CASE-A'},
        {F_ID: 'U-LEAP-026', '名称': '顾思齐', '备注': '高压压气机装配操作工', '用户安全等级': '一般', '性别': '男', F_ADMIN_CODE: 'ADM-COMP-PLANT', F_BIZ_CODE: 'BIZ-COMP-HPC-A'},
        {F_ID: 'U-LEAP-027', '名称': '邵语桐', '备注': '燃烧室质量员', '用户安全等级': '重要', '性别': '女', F_ADMIN_CODE: 'ADM-QA', F_BIZ_CODE: 'BIZ-COMB-LINER-SEC'},
        {F_ID: 'U-LEAP-028', '名称': '孟书航', '备注': '涡轮装配操作工', '用户安全等级': '一般', '性别': '男', F_ADMIN_CODE: 'ADM-TURB-PLANT', F_BIZ_CODE: 'BIZ-TURB-LPT-A'},
        {F_ID: 'U-LEAP-029', '名称': '韩嘉禾', '备注': '附件机匣装配操作工', '用户安全等级': '一般', '性别': '女', F_ADMIN_CODE: 'ADM-AGB-PLANT', F_BIZ_CODE: 'BIZ-AGB-ASM-A'},
        {F_ID: 'U-LEAP-030', '名称': '蒋承霖', '备注': '总装质量主管', '用户安全等级': '核心', '性别': '男', F_ADMIN_CODE: 'ADM-QA', F_BIZ_CODE: 'BIZ-QUALITY'},
    ], (F_ID,))

    wc_org_map = {
        'WC-FAN-BLADE': 'BIZ-FAN-BLADE-SEC',
        'WC-FAN-CASE': 'BIZ-FAN-CASE-SEC',
        'WC-FAN-MOD': 'BIZ-FAN-CASE-SEC',
        'WC-LPC-MOD': 'BIZ-COMP-LPC-SEC',
        'WC-HPC-MOD': 'BIZ-COMP-HPC-SEC',
        'WC-COMB-MOD': 'BIZ-COMB-LINER-SEC',
        'WC-HPT-MOD': 'BIZ-TURB-HPT-SEC',
        'WC-LPT-MOD': 'BIZ-TURB-LPT-SEC',
        'WC-AGB-MOD': 'BIZ-AGB-ASM-SEC',
        'WC-CTRL-SYS': 'BIZ-AGB-CTRL-SEC',
        'WC-CORE-ASM': 'BIZ-FINAL-CORE-SEC',
        'WC-FINAL-ASM': 'BIZ-FINAL-ASM-SEC',
        'WC-TEST': 'BIZ-FINAL-TEST-SEC',
    }
    for row in wcs:
        code = str(row.get(F_CODE, '')).strip()
        if code in wc_org_map:
            row[F_FACTORY_ORG] = wc_org_map[code]

    eq_org_map = {
        'EQ-AFP-01': 'BIZ-FAN-BLADE-SEC',
        'EQ-RTM-01': 'BIZ-FAN-BLADE-SEC',
        'EQ-AUTOCLAVE-01': 'BIZ-FAN-CASE-SEC',
        'EQ-5AXIS-01': 'BIZ-FAN-BLADE-SEC',
        'EQ-EBW-01': 'BIZ-COMB-LINER-SEC',
        'EQ-LASER-01': 'BIZ-COMB-LINER-SEC',
        'EQ-HT-01': 'BIZ-TURB-HPT-SEC',
        'EQ-BRAZE-01': 'BIZ-TURB-HPT-SEC',
        'EQ-AM-01': 'BIZ-COMB-LINER-SEC',
        'EQ-BAL-01': 'BIZ-TURB-LPT-SEC',
        'EQ-COREASM-01': 'BIZ-FINAL-CORE-SEC',
        'EQ-FINALASM-01': 'BIZ-FINAL-ASM-SEC',
        'EQ-COLDTEST-01': 'BIZ-FINAL-TEST-SEC',
        'EQ-HOTTEST-01': 'BIZ-FINAL-TEST-SEC',
        'EQ-VIB-01': 'BIZ-FINAL-TEST-SEC',
    }
    for row in eqs:
        code = str(row.get(F_CODE, '')).strip()
        if code in eq_org_map:
            row[F_FACTORY_ORG] = eq_org_map[code]


def _upgrade_cnc(seed: dict) -> None:
    admins = _rows(seed, WB_SYSTEM, SH_ADMIN)
    bizs = _rows(seed, WB_SYSTEM, SH_BIZ)
    users = _rows(seed, WB_SYSTEM, SH_USER)
    eqs = _rows(seed, WB_FACTORY, SH_EQ)
    wcs = _rows(seed, WB_FACTORY, SH_WC)

    admin_updates = {
        'ADM-CNC-BU': {F_PARENT: 'ADM-MT', F_ADMIN_TYPE: '部门', '*名称': '数控机床事业部', '简称': '数控事业部'},
        'ADM-CNC-PLANT': {F_PARENT: 'ADM-CNC-BU', F_ADMIN_TYPE: '部门', '*名称': '五轴加工中心协同制造中心', '简称': '五轴中心'},
    }
    for code, updates in admin_updates.items():
        row = _find_row(admins, F_CODE, code)
        if row:
            row.update(updates)

    _append_missing(admins, [
        {F_PARENT: 'ADM-CNC-PLANT', F_ADMIN_TYPE: '工厂', F_CODE: 'ADM-CAST-PLANT', '*名称': '结构件机加工厂', '简称': '结构件厂'},
        {F_PARENT: 'ADM-CNC-PLANT', F_ADMIN_TYPE: '工厂', F_CODE: 'ADM-SPINDLE-PLANT', '*名称': '主轴进给工厂', '简称': '主轴进给'},
        {F_PARENT: 'ADM-CNC-PLANT', F_ADMIN_TYPE: '工厂', F_CODE: 'ADM-ATC-PLANT', '*名称': '刀库换刀工厂', '简称': '刀库工厂'},
        {F_PARENT: 'ADM-CNC-PLANT', F_ADMIN_TYPE: '工厂', F_CODE: 'ADM-ELEC-PLANT', '*名称': '电气数控工厂', '简称': '电气数控'},
        {F_PARENT: 'ADM-CNC-PLANT', F_ADMIN_TYPE: '工厂', F_CODE: 'ADM-FINAL-PLANT', '*名称': '总装调试工厂', '简称': '总装调试'},
    ], (F_CODE,))

    biz_updates = {
        'BIZ-CNC-BU': {F_PARENT: 'BIZ-MT', F_ORG_TYPE: '部门', F_ADMIN_CODE: 'ADM-CNC-BU'},
        'BIZ-CNC-CENTER': {F_PARENT: 'BIZ-CNC-BU', F_ORG_TYPE: '部门', F_ADMIN_CODE: 'ADM-CNC-PLANT'},
        'BIZ-CAST': {F_PARENT: 'BIZ-CNC-CENTER', F_ORG_TYPE: '工厂', F_ADMIN_CODE: 'ADM-CAST-PLANT', F_FACTORY_TYPE: '机械加工专业', '*名称': '结构件机加工厂', '简称': '结构件厂'},
        'BIZ-SPINDLE': {F_PARENT: 'BIZ-CNC-CENTER', F_ORG_TYPE: '工厂', F_ADMIN_CODE: 'ADM-SPINDLE-PLANT', F_FACTORY_TYPE: '装配专业', '*名称': '主轴进给工厂', '简称': '主轴进给'},
        'BIZ-ATC': {F_PARENT: 'BIZ-CNC-CENTER', F_ORG_TYPE: '工厂', F_ADMIN_CODE: 'ADM-ATC-PLANT', F_FACTORY_TYPE: '装配专业', '*名称': '刀库换刀工厂', '简称': '刀库工厂'},
        'BIZ-ELEC': {F_PARENT: 'BIZ-CNC-CENTER', F_ORG_TYPE: '工厂', F_ADMIN_CODE: 'ADM-ELEC-PLANT', F_FACTORY_TYPE: '装配专业', '*名称': '电气数控工厂', '简称': '电气数控'},
        'BIZ-FINAL': {F_PARENT: 'BIZ-CNC-CENTER', F_ORG_TYPE: '工厂', F_ADMIN_CODE: 'ADM-FINAL-PLANT', F_FACTORY_TYPE: '装配专业', '*名称': '总装调试工厂', '简称': '总装调试'},
        'BIZ-QUALITY': {F_PARENT: 'BIZ-CNC-CENTER', F_ORG_TYPE: '部门', F_ADMIN_CODE: 'ADM-QA'},
        'BIZ-WARE': {F_PARENT: 'BIZ-CNC-CENTER', F_ORG_TYPE: '部门', F_ADMIN_CODE: 'ADM-WM'},
        'BIZ-DIGI': {F_PARENT: 'BIZ-CNC-CENTER', F_ORG_TYPE: '部门', F_ADMIN_CODE: 'ADM-DIGI'},
    }
    for code, updates in biz_updates.items():
        row = _find_row(bizs, F_CODE, code)
        if row:
            row.update(updates)

    _append_missing(bizs, [
        {F_PARENT: 'BIZ-CAST', '*密级': '内部', F_CODE: 'BIZ-CAST-BED-WS', '*名称': '床身机加车间', '简称': '床身机加', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-CAST-PLANT'},
        {F_PARENT: 'BIZ-CAST-BED-WS', '*密级': '内部', F_CODE: 'BIZ-CAST-BED-SEC', '*名称': '床身导轨工段', '简称': '床身工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-CAST-PLANT'},
        {F_PARENT: 'BIZ-CAST-BED-SEC', '*密级': '内部', F_CODE: 'BIZ-CAST-BED-A', '*名称': '床身机加甲班', '简称': '床身甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-CAST-PLANT'},
        {F_PARENT: 'BIZ-CAST', '*密级': '内部', F_CODE: 'BIZ-CAST-COL-WS', '*名称': '立柱鞍座车间', '简称': '立柱鞍座', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-CAST-PLANT'},
        {F_PARENT: 'BIZ-CAST-COL-WS', '*密级': '内部', F_CODE: 'BIZ-CAST-COL-SEC', '*名称': '立柱镗铣工段', '简称': '立柱工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-CAST-PLANT'},
        {F_PARENT: 'BIZ-CAST-COL-SEC', '*密级': '内部', F_CODE: 'BIZ-CAST-COL-A', '*名称': '立柱机加甲班', '简称': '立柱甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-CAST-PLANT'},
        {F_PARENT: 'BIZ-CAST', '*密级': '内部', F_CODE: 'BIZ-CAST-TBL-WS', '*名称': '工作台回转轴车间', '简称': '工作台车间', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-CAST-PLANT'},
        {F_PARENT: 'BIZ-CAST-TBL-WS', '*密级': '内部', F_CODE: 'BIZ-CAST-TBL-SEC', '*名称': '回转轴工段', '简称': '回转轴工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-CAST-PLANT'},
        {F_PARENT: 'BIZ-CAST-TBL-SEC', '*密级': '内部', F_CODE: 'BIZ-CAST-TBL-A', '*名称': '回转轴甲班', '简称': '回转轴甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-CAST-PLANT'},
        {F_PARENT: 'BIZ-SPINDLE', '*密级': '内部', F_CODE: 'BIZ-SPINDLE-ASM-WS', '*名称': '主轴装配车间', '简称': '主轴装配', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-SPINDLE-PLANT'},
        {F_PARENT: 'BIZ-SPINDLE-ASM-WS', '*密级': '内部', F_CODE: 'BIZ-SPINDLE-ASM-SEC', '*名称': '主轴预装工段', '简称': '主轴工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-SPINDLE-PLANT'},
        {F_PARENT: 'BIZ-SPINDLE-ASM-SEC', '*密级': '内部', F_CODE: 'BIZ-SPINDLE-ASM-A', '*名称': '主轴装配甲班', '简称': '主轴甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-SPINDLE-PLANT'},
        {F_PARENT: 'BIZ-SPINDLE', '*密级': '内部', F_CODE: 'BIZ-SPINDLE-FEED-WS', '*名称': '进给装配车间', '简称': '进给装配', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-SPINDLE-PLANT'},
        {F_PARENT: 'BIZ-SPINDLE-FEED-WS', '*密级': '内部', F_CODE: 'BIZ-SPINDLE-FEED-SEC', '*名称': '丝杠导轨工段', '简称': '进给工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-SPINDLE-PLANT'},
        {F_PARENT: 'BIZ-SPINDLE-FEED-SEC', '*密级': '内部', F_CODE: 'BIZ-SPINDLE-FEED-A', '*名称': '丝杠导轨甲班', '简称': '进给甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-SPINDLE-PLANT'},
        {F_PARENT: 'BIZ-ATC', '*密级': '内部', F_CODE: 'BIZ-ATC-ASM-WS', '*名称': '刀库换刀装配车间', '简称': '刀库装配', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-ATC-PLANT'},
        {F_PARENT: 'BIZ-ATC-ASM-WS', '*密级': '内部', F_CODE: 'BIZ-ATC-ASM-SEC', '*名称': '刀库换刀工段', '简称': '刀库工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-ATC-PLANT'},
        {F_PARENT: 'BIZ-ATC-ASM-SEC', '*密级': '内部', F_CODE: 'BIZ-ATC-ASM-A', '*名称': '刀库装配甲班', '简称': '刀库甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-ATC-PLANT'},
        {F_PARENT: 'BIZ-ELEC', '*密级': '内部', F_CODE: 'BIZ-ELEC-PANEL-WS', '*名称': '电柜装配车间', '简称': '电柜装配', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-ELEC-PLANT'},
        {F_PARENT: 'BIZ-ELEC-PANEL-WS', '*密级': '内部', F_CODE: 'BIZ-ELEC-PANEL-SEC', '*名称': '线束接线工段', '简称': '接线工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-ELEC-PLANT'},
        {F_PARENT: 'BIZ-ELEC-PANEL-SEC', '*密级': '内部', F_CODE: 'BIZ-ELEC-PANEL-A', '*名称': '电柜装配甲班', '简称': '电柜甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-ELEC-PLANT'},
        {F_PARENT: 'BIZ-ELEC', '*密级': '内部', F_CODE: 'BIZ-ELEC-CNC-WS', '*名称': '数控系统集成车间', '简称': '数控集成', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-ELEC-PLANT'},
        {F_PARENT: 'BIZ-ELEC-CNC-WS', '*密级': '内部', F_CODE: 'BIZ-ELEC-CNC-SEC', '*名称': '系统联调工段', '简称': '联调工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-ELEC-PLANT'},
        {F_PARENT: 'BIZ-ELEC-CNC-SEC', '*密级': '内部', F_CODE: 'BIZ-ELEC-CNC-A', '*名称': '系统联调甲班', '简称': '联调甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-ELEC-PLANT'},
        {F_PARENT: 'BIZ-FINAL', '*密级': '内部', F_CODE: 'BIZ-FINAL-ASM-WS', '*名称': '整机总装车间', '简称': '整机总装', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
        {F_PARENT: 'BIZ-FINAL-ASM-WS', '*密级': '内部', F_CODE: 'BIZ-FINAL-ASM-SEC', '*名称': '整机总装工段', '简称': '总装工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
        {F_PARENT: 'BIZ-FINAL-ASM-SEC', '*密级': '内部', F_CODE: 'BIZ-FINAL-ASM-A', '*名称': '整机总装甲班', '简称': '总装甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
        {F_PARENT: 'BIZ-FINAL', '*密级': '内部', F_CODE: 'BIZ-FINAL-TEST-WS', '*名称': '整机试车车间', '简称': '整机试车', F_ORG_TYPE: '车间', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
        {F_PARENT: 'BIZ-FINAL-TEST-WS', '*密级': '内部', F_CODE: 'BIZ-FINAL-TEST-SEC', '*名称': '精度调试工段', '简称': '试车工段', F_ORG_TYPE: '工段', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
        {F_PARENT: 'BIZ-FINAL-TEST-SEC', '*密级': '内部', F_CODE: 'BIZ-FINAL-TEST-A', '*名称': '整机试车甲班', '简称': '试车甲班', F_ORG_TYPE: '班组', F_ADMIN_CODE: 'ADM-FINAL-PLANT'},
    ], (F_CODE,))

    user_updates = {
        'U-CNC-007': {F_ADMIN_CODE: 'ADM-CAST-PLANT', F_BIZ_CODE: 'BIZ-CAST-BED-SEC', '备注': '结构件工艺工程师'},
        'U-CNC-008': {F_ADMIN_CODE: 'ADM-SPINDLE-PLANT', F_BIZ_CODE: 'BIZ-SPINDLE-ASM-SEC', '备注': '主轴工艺工程师'},
        'U-CNC-010': {F_ADMIN_CODE: 'ADM-FINAL-PLANT', F_BIZ_CODE: 'BIZ-FINAL-TEST-SEC', '备注': '整机调试主管'},
        'U-CNC-011': {F_ADMIN_CODE: 'ADM-FINAL-PLANT', F_BIZ_CODE: 'BIZ-FINAL-ASM-SEC', '备注': '总装工程师'},
        'U-CNC-012': {F_ADMIN_CODE: 'ADM-CAST-PLANT', F_BIZ_CODE: 'BIZ-CAST-BED-A', '备注': '结构件班组长'},
    }
    for code, updates in user_updates.items():
        row = _find_row(users, F_ID, code)
        if row:
            row.update(updates)

    _append_missing(users, [
        {F_ID: 'U-CNC-021', '名称': '陆明哲', '备注': '生产计划员', '用户安全等级': '重要', '性别': '男', F_ADMIN_CODE: 'ADM-SCM', F_BIZ_CODE: 'BIZ-CNC-CENTER'},
        {F_ID: 'U-CNC-022', '名称': '唐语霏', '备注': '仓库管理员', '用户安全等级': '一般', '性别': '女', F_ADMIN_CODE: 'ADM-WM', F_BIZ_CODE: 'BIZ-WARE'},
        {F_ID: 'U-CNC-023', '名称': '周启航', '备注': '设备维修工', '用户安全等级': '一般', '性别': '男', F_ADMIN_CODE: 'ADM-CNC-PLANT', F_BIZ_CODE: 'BIZ-CNC-CENTER'},
        {F_ID: 'U-CNC-024', '名称': '宋雨荷', '备注': '设备保养员', '用户安全等级': '一般', '性别': '女', F_ADMIN_CODE: 'ADM-CNC-PLANT', F_BIZ_CODE: 'BIZ-CNC-CENTER'},
        {F_ID: 'U-CNC-025', '名称': '何靖远', '备注': '主轴装配班组长', '用户安全等级': '一般', '性别': '男', F_ADMIN_CODE: 'ADM-SPINDLE-PLANT', F_BIZ_CODE: 'BIZ-SPINDLE-ASM-A'},
        {F_ID: 'U-CNC-026', '名称': '姚可欣', '备注': '电柜装配工程师', '用户安全等级': '重要', '性别': '女', F_ADMIN_CODE: 'ADM-ELEC-PLANT', F_BIZ_CODE: 'BIZ-ELEC-PANEL-SEC'},
        {F_ID: 'U-CNC-027', '名称': '谢知远', '备注': '刀库装配操作工', '用户安全等级': '一般', '性别': '男', F_ADMIN_CODE: 'ADM-ATC-PLANT', F_BIZ_CODE: 'BIZ-ATC-ASM-A'},
        {F_ID: 'U-CNC-028', '名称': '高语彤', '备注': '总装质量主管', '用户安全等级': '核心', '性别': '女', F_ADMIN_CODE: 'ADM-QA', F_BIZ_CODE: 'BIZ-QUALITY'},
        {F_ID: 'U-CNC-029', '名称': '梁承安', '备注': '整机试车工程师', '用户安全等级': '重要', '性别': '男', F_ADMIN_CODE: 'ADM-FINAL-PLANT', F_BIZ_CODE: 'BIZ-FINAL-TEST-A'},
        {F_ID: 'U-CNC-030', '名称': '苏沐晴', '备注': '精度检测工程师', '用户安全等级': '重要', '性别': '女', F_ADMIN_CODE: 'ADM-QA', F_BIZ_CODE: 'BIZ-QUALITY'},
    ], (F_ID,))

    wc_org_map = {
        'WC-BED-MACH': 'BIZ-CAST-BED-SEC',
        'WC-COLUMN-MACH': 'BIZ-CAST-COL-SEC',
        'WC-TABLE-MACH': 'BIZ-CAST-TBL-SEC',
        'WC-SPINDLE-ASM': 'BIZ-SPINDLE-ASM-SEC',
        'WC-FEED-ASM': 'BIZ-SPINDLE-FEED-SEC',
        'WC-ATC-ASM': 'BIZ-ATC-ASM-SEC',
        'WC-ELEC-PANEL': 'BIZ-ELEC-PANEL-SEC',
        'WC-CNC-INTEG': 'BIZ-ELEC-CNC-SEC',
        'WC-FINAL-ASM': 'BIZ-FINAL-ASM-SEC',
        'WC-TEST': 'BIZ-FINAL-TEST-SEC',
    }
    for row in wcs:
        code = str(row.get(F_CODE, '')).strip()
        if code in wc_org_map:
            row[F_FACTORY_ORG] = wc_org_map[code]

    eq_org_map = {
        'EQ-GANTRY-GRIND': 'BIZ-CAST-BED-SEC',
        'EQ-HBM': 'BIZ-CAST-BED-SEC',
        'EQ-VMC': 'BIZ-CAST-COL-SEC',
        'EQ-BORING': 'BIZ-CAST-TBL-SEC',
        'EQ-SPINDLE-BAL': 'BIZ-SPINDLE-ASM-SEC',
        'EQ-BALLSCREW-ASM': 'BIZ-SPINDLE-FEED-SEC',
        'EQ-ATC-ASM': 'BIZ-ATC-ASM-SEC',
        'EQ-WIRING': 'BIZ-ELEC-PANEL-SEC',
        'EQ-CNC-BURN': 'BIZ-ELEC-CNC-SEC',
        'EQ-GEO-PLAT': 'BIZ-FINAL-ASM-SEC',
        'EQ-RUNIN': 'BIZ-FINAL-TEST-SEC',
        'EQ-CUTTEST': 'BIZ-FINAL-TEST-SEC',
        'EQ-HYD-TEST': 'BIZ-FINAL-TEST-SEC',
    }
    for row in eqs:
        code = str(row.get(F_CODE, '')).strip()
        if code in eq_org_map:
            row[F_FACTORY_ORG] = eq_org_map[code]


def apply_scene_upgrade(seed: dict, scenario: str, namespace: str, volume_profile: str | None = None) -> dict:
    resolved_volume_profile = _resolve_seed_volume_profile(seed, volume_profile)
    if scenario == 'boeing_737_leap1b':
        _upgrade_b737(seed)
    elif scenario == 'cnc_machine':
        _upgrade_cnc(seed)
    expand_seed_volume(seed, scenario, resolved_volume_profile)
    apply_project_collaboration(seed)
    remove_transfer_operations(seed)
    apply_namespace(seed, namespace)
    normalize_user_codes(seed, namespace)
    normalize_poc_security(seed)
    normalize_storage_factory_org(seed)
    normalize_release_user(seed)
    clear_tool_strategy_relations(seed)
    filter_wc_supplier_relations(seed)
    rebuild_route_sequences(seed)
    normalize_sequence_relations(seed)
    return seed
