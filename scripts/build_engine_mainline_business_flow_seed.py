from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_SCRIPT_DIR = Path(
    r"C:\Users\Administrator\.codex\skills\.system\mom-business-data-generator\scripts"
)

if str(SKILL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_SCRIPT_DIR))

from gearbox_seed_support import (  # type: ignore  # noqa: E402
    CAT_AUX,
    CAT_KIT,
    CAT_PART,
    FEATURE_IMPORTANT,
    FEATURE_KEY,
    FEATURE_NORMAL,
    MAKE_BUY,
    MAKE_SELF,
    SeedBuilder,
    summarize_seed,
)
from production_order_seed import apply_production_orders  # type: ignore  # noqa: E402
from scene_seed_upgrades import (  # type: ignore  # noqa: E402
    apply_namespace,
    apply_project_collaboration,
    clear_tool_strategy_relations,
    filter_wc_supplier_relations,
    normalize_poc_security,
    normalize_release_user,
    normalize_sequence_relations,
    normalize_storage_factory_org,
    normalize_user_codes,
    rebuild_route_sequences,
    remove_transfer_operations,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SCENARIO = "engine_mainline_business_flow"
NAMESPACE = "ENG20S01"
VOLUME_PROFILE = "标准版"
OUTPUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "outputs"
    / "06_测试数据"
    / "发动机主线业务流程-多工厂一级工艺版"
)
ASSET_PATH = OUTPUT_DIR / "发动机主线业务流程-测试数据种子-V1.0.json"


def normalize_latest_order_enums(seed: dict) -> dict:
    order_rows = (
        seed.get("workbooks", {})
        .get("生产订单_模板.xlsx", {})
        .get("生产订单", [])
    )
    for row in order_rows:
        if row.get("计划类型") == "零部件交付计划":
            row["计划类型"] = "零部件生产计划"
        if row.get("排产状态") == "零部件交付计划已排产":
            row["排产状态"] = "零部件生产已排产"
    return seed


def build_config() -> dict:
    metadata = {
        "name": "发动机主线业务流程多工厂一级工艺种子",
        "industry": "航空发动机",
        "product_family": "发动机总装",
        "product_model": "AE-100航空发动机总成",
        "description": (
            "面向 MOM 主线业务流程演示构建的多工厂测试数据，覆盖生产部一级工艺、"
            "机加厂/盘轴厂/叶片厂/装配厂正式工艺，以及厂际协同计划和各分厂生产订单。"
        ),
        "project_collaboration": {
            "enabled": True,
            "admin": {
                "parent": "Adm001",
                "code": "Adm900",
                "name": "生产部",
                "short": "生产部",
            },
            "biz": {
                "parent": "Biz001",
                "code": "Biz900",
                "name": "生产部",
                "short": "生产部",
                "factory_type": "装配专业",
                "remark": "用于生产部持单的一级工艺、厂际协同计划与多工厂排产总览。",
            },
            "route": {
                "code": "Rt900",
                "name": "发动机一级协同工艺",
                "material_code": "Mat011",
                "spec": "通用",
                "remark": "生产部统一承接厂际协同计划，按参与工厂拆解一级工艺。",
            },
            "phases": [
                {
                    "no": "0010",
                    "name": "10-机加厂阶段完成",
                    "wc_code": "Wc901",
                    "wc_name": "10-机加厂协同中心",
                    "content": "生产部确认机加厂机匣件完工与交付节拍。",
                    "op_spec": "机械加工专业",
                    "output_code": "Mat002",
                },
                {
                    "no": "0020",
                    "name": "20-盘轴厂阶段完成",
                    "wc_code": "Wc902",
                    "wc_name": "20-盘轴厂协同中心",
                    "content": "生产部确认盘轴厂关键转子模块完工与交付节拍。",
                    "op_spec": "机械加工专业",
                    "output_code": "Mat004",
                },
                {
                    "no": "0030",
                    "name": "30-叶片厂阶段完成",
                    "wc_code": "Wc903",
                    "wc_name": "30-叶片厂协同中心",
                    "content": "生产部确认叶片厂关键叶片组件完工与交付节拍。",
                    "op_spec": "机械加工专业",
                    "output_code": "Mat006",
                },
                {
                    "no": "0040",
                    "name": "40-装配厂总装试车完成",
                    "wc_code": "Wc904",
                    "wc_name": "40-装配厂协同中心",
                    "content": "生产部确认总装、试车和交付窗口，形成整机交付承诺。",
                    "op_spec": "装配专业",
                    "output_code": "Mat011",
                },
            ],
        },
    }

    admins = [
        ("0", "公司", "Adm001", "启航航空发动机制造有限公司", "启航航发"),
        ("Adm001", "工厂", "Adm010", "10-机加厂", "机加厂"),
        ("Adm001", "工厂", "Adm020", "20-盘轴厂", "盘轴厂"),
        ("Adm001", "工厂", "Adm030", "30-叶片厂", "叶片厂"),
        ("Adm001", "工厂", "Adm040", "40-装配厂", "装配厂"),
    ]

    bizs = [
        ("0", "Biz001", "启航航空发动机制造有限公司", "启航航发", "公司", "Adm001", "", "发动机主线业务流程示例公司"),
        ("Biz001", "Biz010", "10-机加厂", "机加厂", "工厂", "Adm010", "机械加工专业", "负责机匣类关键件机加与尺寸放行"),
        ("Biz010", "Biz011", "机加车间", "机加车间", "车间", "Adm010"),
        ("Biz011", "Biz012", "机加班组", "机加班组", "班组", "Adm010"),
        ("Biz011", "Biz013", "机加检验班组", "机加检验", "班组", "Adm010"),
        ("Biz001", "Biz020", "20-盘轴厂", "盘轴厂", "工厂", "Adm020", "机械加工专业", "负责盘轴类关键件加工、平衡与终检"),
        ("Biz020", "Biz021", "盘轴车间", "盘轴车间", "车间", "Adm020"),
        ("Biz021", "Biz022", "盘轴加工班组", "盘轴加工", "班组", "Adm020"),
        ("Biz021", "Biz023", "盘轴检验班组", "盘轴检验", "班组", "Adm020"),
        ("Biz001", "Biz030", "30-叶片厂", "叶片厂", "工厂", "Adm030", "机械加工专业", "负责叶片成型、涂层与叶片终检"),
        ("Biz030", "Biz031", "叶片车间", "叶片车间", "车间", "Adm030"),
        ("Biz031", "Biz032", "叶片加工班组", "叶片加工", "班组", "Adm030"),
        ("Biz031", "Biz033", "叶片检验班组", "叶片检验", "班组", "Adm030"),
        ("Biz001", "Biz040", "40-装配厂", "装配厂", "工厂", "Adm040", "装配专业", "负责整机装配、试车与交付放行"),
        ("Biz040", "Biz041", "总装试车车间", "总装试车", "车间", "Adm040"),
        ("Biz041", "Biz042", "总装班组", "总装班组", "班组", "Adm040"),
        ("Biz041", "Biz043", "试车放行班组", "试车放行", "班组", "Adm040"),
    ]

    users = [
        ("U9001", "顾明川", "重要", "男", "Adm900", "Biz900", "生产部部长"),
        ("U9002", "林清越", "重要", "女", "Adm900", "Biz900", "主计划员"),
        ("U9003", "许知行", "重要", "男", "Adm900", "Biz900", "工艺工程师"),
        ("U1001", "沈安和", "一般", "男", "Adm010", "Biz012", "机加班组长"),
        ("U1002", "宋言舟", "一般", "男", "Adm010", "Biz012", "机加操作工"),
        ("U1003", "顾若宁", "一般", "女", "Adm010", "Biz013", "机加检验员"),
        ("U1004", "唐书远", "一般", "男", "Adm010", "Biz010", "仓库管理员"),
        ("U2001", "周景程", "一般", "男", "Adm020", "Biz022", "盘轴班组长"),
        ("U2002", "陆知夏", "一般", "女", "Adm020", "Biz022", "盘轴操作工"),
        ("U2003", "韩以宁", "一般", "男", "Adm020", "Biz023", "盘轴检验员"),
        ("U2004", "乔云舒", "一般", "女", "Adm020", "Biz020", "仓库管理员"),
        ("U3001", "温清妍", "一般", "女", "Adm030", "Biz032", "叶片班组长"),
        ("U3002", "郑承泽", "一般", "男", "Adm030", "Biz032", "叶片操作工"),
        ("U3003", "程可欣", "一般", "女", "Adm030", "Biz033", "叶片检验员"),
        ("U3004", "谢闻笙", "一般", "男", "Adm030", "Biz030", "仓库管理员"),
        ("U4001", "苏景明", "一般", "男", "Adm040", "Biz042", "装配班组长"),
        ("U4002", "叶安宁", "一般", "女", "Adm040", "Biz042", "装配操作工"),
        ("U4003", "梁知远", "一般", "男", "Adm040", "Biz043", "检验员"),
        ("U4004", "秦若衡", "一般", "女", "Adm040", "Biz040", "仓库管理员"),
    ]

    work_centers = [
        {"code": "Wc101", "name": "机匣机加中心", "biz": "Biz012", "wc_type": "组织", "wc_class": "加工", "remark": "负责机匣找正、粗精加工"},
        {"code": "Wc102", "name": "机匣尺寸检验中心", "biz": "Biz013", "wc_type": "组织", "wc_class": "检验", "remark": "负责机加尺寸、同轴度和表面质量放行"},
        {"code": "Wc201", "name": "盘轴复合加工中心", "biz": "Biz022", "wc_type": "组织", "wc_class": "加工", "remark": "负责盘轴类关键件车铣复合加工"},
        {"code": "Wc202", "name": "盘轴动平衡中心", "biz": "Biz023", "wc_type": "组织", "wc_class": "加工", "remark": "负责盘轴动平衡修正与配重"},
        {"code": "Wc203", "name": "盘轴终检中心", "biz": "Biz023", "wc_type": "组织", "wc_class": "检验", "remark": "负责盘轴探伤与尺寸终检"},
        {"code": "Wc301", "name": "叶片成型中心", "biz": "Biz032", "wc_type": "组织", "wc_class": "加工", "remark": "负责叶片型面成型与冷端修整"},
        {"code": "Wc302", "name": "叶片涂层中心", "biz": "Biz032", "wc_type": "组织", "wc_class": "加工", "remark": "负责叶片保护涂层与固化"},
        {"code": "Wc303", "name": "叶片检测中心", "biz": "Biz033", "wc_type": "组织", "wc_class": "检验", "remark": "负责叶片流道、型面和外观终检"},
        {"code": "Wc401", "name": "整机总装中心", "biz": "Biz042", "wc_type": "组织", "wc_class": "加工", "remark": "负责整机总装、联接和复核"},
        {"code": "Wc402", "name": "整机试车放行中心", "biz": "Biz043", "wc_type": "组织", "wc_class": "检验", "remark": "负责试车、质量结论和交付放行"},
    ]

    equipments = [
        {"code": "Eq101", "name": "五轴龙门加工中心", "model": "GM-500", "biz": "Biz012", "remark": "机匣关键孔面加工"},
        {"code": "Eq102", "name": "三坐标测量机", "model": "CMM-1200", "biz": "Biz013", "remark": "机匣尺寸测量"},
        {"code": "Eq201", "name": "车铣复合机床", "model": "TM-600", "biz": "Biz022", "remark": "盘轴复合加工"},
        {"code": "Eq202", "name": "高速动平衡机", "model": "DB-300", "biz": "Biz023", "remark": "盘轴动平衡修正"},
        {"code": "Eq203", "name": "超声探伤台", "model": "UT-80", "biz": "Biz023", "remark": "盘轴无损终检"},
        {"code": "Eq301", "name": "叶片成型磨床", "model": "LM-220", "biz": "Biz032", "remark": "叶片型面成型"},
        {"code": "Eq302", "name": "涂层喷涂柜", "model": "TC-90", "biz": "Biz032", "remark": "叶片表面保护涂层"},
        {"code": "Eq303", "name": "叶片流量检测台", "model": "FL-30", "biz": "Biz033", "remark": "叶片流道与通流检测"},
        {"code": "Eq401", "name": "总装定位工位", "model": "ASM-100", "biz": "Biz042", "remark": "整机总装定位与联接"},
        {"code": "Eq402", "name": "发动机试车台", "model": "TEST-900", "biz": "Biz043", "remark": "整机试车与放行"},
    ]

    tools = [
        {
            "code": "Tool101",
            "name": "机匣定位夹具",
            "material_category": CAT_PART,
            "make_type": MAKE_SELF,
            "tooling_category": "专用工装",
            "feature": FEATURE_KEY,
            "model": "JJ-101",
            "spec": "机匣孔面定位",
            "remark": "机匣加工定位夹具",
            "life_times": 60000,
            "life_days": 365,
        },
        {
            "code": "Tool201",
            "name": "盘轴平衡工装",
            "material_category": CAT_PART,
            "make_type": MAKE_SELF,
            "tooling_category": "专用工装",
            "feature": FEATURE_IMPORTANT,
            "model": "PJ-201",
            "spec": "盘轴平衡修正",
            "remark": "盘轴平衡修正工装",
            "life_times": 50000,
            "life_days": 365,
        },
        {
            "code": "Tool301",
            "name": "叶片型面检具",
            "material_category": CAT_PART,
            "make_type": MAKE_SELF,
            "tooling_category": "专用工装",
            "feature": FEATURE_KEY,
            "model": "YJ-301",
            "spec": "叶片型面检测",
            "remark": "叶片型面快速检测检具",
            "life_times": 50000,
            "life_days": 365,
        },
        {
            "code": "Tool401",
            "name": "整机总装吊具",
            "material_category": CAT_PART,
            "make_type": MAKE_SELF,
            "tooling_category": "专用工装",
            "feature": FEATURE_IMPORTANT,
            "model": "DJ-401",
            "spec": "整机吊装定位",
            "remark": "整机总装吊具",
            "life_times": 30000,
            "life_days": 365,
        },
    ]

    wc_user_links = [
        ("Wc101", "U1001"),
        ("Wc102", "U1003"),
        ("Wc201", "U2001"),
        ("Wc202", "U2002"),
        ("Wc203", "U2003"),
        ("Wc301", "U3001"),
        ("Wc302", "U3002"),
        ("Wc303", "U3003"),
        ("Wc401", "U4001"),
        ("Wc402", "U4003"),
    ]

    wc_eq_links = [
        ("Wc101", "Eq101"),
        ("Wc102", "Eq102"),
        ("Wc201", "Eq201"),
        ("Wc202", "Eq202"),
        ("Wc203", "Eq203"),
        ("Wc301", "Eq301"),
        ("Wc302", "Eq302"),
        ("Wc303", "Eq303"),
        ("Wc401", "Eq401"),
        ("Wc402", "Eq402"),
    ]

    eq_user_links = [
        ("Eq101", "U1002"),
        ("Eq102", "U1003"),
        ("Eq201", "U2002"),
        ("Eq202", "U2003"),
        ("Eq301", "U3002"),
        ("Eq401", "U4002"),
        ("Eq402", "U4003"),
    ]

    warehouses = [
        ("Wh010", "机加在制品库", "Biz010", "ERP一级库", "普通库房", "存放机匣毛坯与机加完件"),
        ("Wh020", "盘轴在制品库", "Biz020", "ERP一级库", "普通库房", "存放盘轴锻件与盘轴模块"),
        ("Wh030", "叶片在制品库", "Biz030", "ERP一级库", "普通库房", "存放叶片毛坯、涂层件与叶片组件"),
        ("Wh040", "装配成套库", "Biz040", "ERP一级库", "普通库房", "存放总装齐套件、成套包装件与待发运总成"),
    ]

    locations = [
        ("Loc011", "机匣毛坯区", "Biz010", "Wh010"),
        ("Loc012", "机加完件区", "Biz010", "Wh010"),
        ("Loc013", "待发装配区", "Biz010", "Wh010"),
        ("Loc021", "盘轴锻件区", "Biz020", "Wh020"),
        ("Loc022", "平衡待检区", "Biz020", "Wh020"),
        ("Loc023", "盘轴合格区", "Biz020", "Wh020"),
        ("Loc031", "叶片毛坯区", "Biz030", "Wh030"),
        ("Loc032", "涂层待检区", "Biz030", "Wh030"),
        ("Loc033", "叶片合格区", "Biz030", "Wh030"),
        ("Loc041", "总装齐套区", "Biz040", "Wh040"),
        ("Loc042", "试车待放行区", "Biz040", "Wh040"),
        ("Loc043", "发运成套区", "Biz040", "Wh040"),
    ]

    materials = [
        {
            "code": "Mat001",
            "name": "机匣毛坯",
            "category": CAT_PART,
            "make_type": MAKE_SELF,
            "feature": FEATURE_KEY,
            "drawing": "AE-100-001",
            "model": "",
            "spec": "机匣毛坯件",
            "remark": "机加厂输入件",
        },
        {
            "code": "Mat002",
            "name": "机匣机加完件",
            "category": CAT_PART,
            "make_type": MAKE_SELF,
            "feature": FEATURE_KEY,
            "drawing": "AE-100-002",
            "model": "",
            "spec": "机加阶段完成件",
            "remark": "10-机加厂正式工艺产出物",
        },
        {
            "code": "Mat003",
            "name": "盘轴锻件",
            "category": CAT_PART,
            "make_type": MAKE_SELF,
            "feature": FEATURE_KEY,
            "drawing": "AE-100-003",
            "model": "",
            "spec": "盘轴毛坯件",
            "remark": "盘轴厂输入件",
        },
        {
            "code": "Mat004",
            "name": "盘轴模块",
            "category": CAT_PART,
            "make_type": MAKE_SELF,
            "feature": FEATURE_KEY,
            "drawing": "AE-100-004",
            "model": "",
            "spec": "盘轴阶段完成件",
            "remark": "20-盘轴厂正式工艺产出物",
        },
        {
            "code": "Mat005",
            "name": "叶片毛坯",
            "category": CAT_PART,
            "make_type": MAKE_SELF,
            "feature": FEATURE_IMPORTANT,
            "drawing": "AE-100-005",
            "model": "",
            "spec": "叶片毛坯件",
            "remark": "叶片厂输入件",
        },
        {
            "code": "Mat006",
            "name": "叶片组件",
            "category": CAT_PART,
            "make_type": MAKE_SELF,
            "feature": FEATURE_KEY,
            "drawing": "AE-100-006",
            "model": "",
            "spec": "叶片阶段完成件",
            "remark": "30-叶片厂正式工艺产出物",
        },
        {
            "code": "Mat007",
            "name": "紧固件标准包",
            "category": CAT_KIT,
            "make_type": MAKE_BUY,
            "feature": FEATURE_NORMAL,
            "drawing": "AE-100-007",
            "model": "",
            "spec": "总装标准件包",
            "remark": "总装工位标准件",
        },
        {
            "code": "Mat008",
            "name": "密封垫组件",
            "category": CAT_KIT,
            "make_type": MAKE_BUY,
            "feature": FEATURE_IMPORTANT,
            "drawing": "AE-100-008",
            "model": "",
            "spec": "总装密封件",
            "remark": "总装密封组件",
        },
        {
            "code": "Mat009",
            "name": "叶片涂层辅料",
            "category": CAT_AUX,
            "make_type": MAKE_BUY,
            "feature": FEATURE_NORMAL,
            "drawing": "AE-100-009",
            "model": "",
            "spec": "叶片保护涂层",
            "remark": "叶片厂涂层辅料",
        },
        {
            "code": "Mat010",
            "name": "试车介质包",
            "category": CAT_AUX,
            "make_type": MAKE_BUY,
            "feature": FEATURE_NORMAL,
            "drawing": "AE-100-010",
            "model": "",
            "spec": "整机试车介质",
            "remark": "装配厂试车耗材",
        },
        {
            "code": "Mat011",
            "name": "航空发动机总成",
            "category": CAT_PART,
            "make_type": MAKE_SELF,
            "feature": FEATURE_KEY,
            "drawing": "AE-100-011",
            "model": "AE-100",
            "spec": "整机成品",
            "remark": "发动机主线业务流程最终交付物",
            "batch": "是",
            "serial": "是",
        },
        {
            "code": "Mat012",
            "name": "发运包装组件",
            "category": CAT_KIT,
            "make_type": MAKE_BUY,
            "feature": FEATURE_NORMAL,
            "drawing": "AE-100-012",
            "model": "",
            "spec": "发运包装辅件",
            "remark": "整机交付包装材料",
        },
    ]

    mboms = [
        {
            "code": "Mb001",
            "material_code": "Mat011",
            "name": "航空发动机总成MBOM",
            "nodes": [
                {"level": 0, "material_code": "Mat011", "qty": 1},
                {"level": 1, "material_code": "Mat002", "qty": 1, "parent_material": "Mat011", "parent_version": "A.01"},
                {"level": 1, "material_code": "Mat004", "qty": 1, "parent_material": "Mat011", "parent_version": "A.01"},
                {"level": 1, "material_code": "Mat006", "qty": 12, "parent_material": "Mat011", "parent_version": "A.01"},
                {"level": 1, "material_code": "Mat007", "qty": 1, "parent_material": "Mat011", "parent_version": "A.01"},
                {"level": 1, "material_code": "Mat008", "qty": 1, "parent_material": "Mat011", "parent_version": "A.01"},
                {"level": 1, "material_code": "Mat012", "qty": 1, "parent_material": "Mat011", "parent_version": "A.01"},
            ],
        }
    ]

    routes = [
        {
            "code": "Rt010",
            "name": "10-机加厂正式工艺",
            "route_spec": "机加",
            "biz": "Biz010",
            "material_code": "Mat002",
            "proc_spec": "机械加工专业",
            "remark": "机加厂负责机匣件找正、机加和尺寸放行。",
            "ops": [
                {
                    "no": "0010",
                    "name": "机匣毛坯上线与找正",
                    "type": "加工",
                    "wc": "Wc101",
                    "prep": 10,
                    "run": 18,
                    "out": "Mat002",
                    "content": "完成机匣毛坯上线、找正和工艺准备。",
                    "materials": [("Mat001", 1)],
                    "steps": [
                        ("核对毛坯状态", "核对机匣毛坯批次、状态和余量。"),
                        ("装夹找正", "完成机匣毛坯装夹、找正和程序确认。"),
                    ],
                },
                {
                    "no": "0020",
                    "name": "机匣五轴粗精加工",
                    "type": "加工",
                    "wc": "Wc101",
                    "prep": 14,
                    "run": 36,
                    "out": "Mat002",
                    "content": "完成机匣关键孔面、安装面和外形粗精加工。",
                    "materials": [],
                    "steps": [
                        ("执行五轴加工", "完成关键孔面与安装面粗精加工。"),
                        ("清理去毛刺", "完成机加后清理和去毛刺。"),
                    ],
                },
                {
                    "no": "0030",
                    "name": "机匣尺寸终检",
                    "type": "检验",
                    "wc": "Wc102",
                    "prep": 8,
                    "run": 16,
                    "out": "Mat002",
                    "content": "完成机匣尺寸、同轴度和表面质量终检。",
                    "materials": [],
                    "steps": [
                        ("三坐标检测", "完成关键尺寸和安装面的三坐标检测。"),
                        ("放行判定", "形成机匣完件放行结论。"),
                    ],
                },
            ],
        },
        {
            "code": "Rt020",
            "name": "20-盘轴厂正式工艺",
            "route_spec": "机加",
            "biz": "Biz020",
            "material_code": "Mat004",
            "proc_spec": "机械加工专业",
            "remark": "盘轴厂负责盘轴关键件复合加工、平衡修正和终检。",
            "ops": [
                {
                    "no": "0010",
                    "name": "盘轴复合加工",
                    "type": "加工",
                    "wc": "Wc201",
                    "prep": 12,
                    "run": 28,
                    "out": "Mat004",
                    "content": "完成盘轴类关键件车铣复合加工。",
                    "materials": [("Mat003", 1)],
                    "steps": [
                        ("复合加工准备", "核对盘轴锻件状态并完成装夹。"),
                        ("盘轴车铣加工", "完成盘轴关键面和接口加工。"),
                    ],
                },
                {
                    "no": "0020",
                    "name": "盘轴动平衡修正",
                    "type": "加工",
                    "wc": "Wc202",
                    "prep": 8,
                    "run": 20,
                    "out": "Mat004",
                    "content": "完成盘轴动平衡检测与修正。",
                    "materials": [],
                    "steps": [
                        ("执行动平衡检测", "完成盘轴动平衡初检与偏差记录。"),
                        ("配重修正", "完成配重修正和复核。"),
                    ],
                },
                {
                    "no": "0030",
                    "name": "盘轴终检放行",
                    "type": "检验",
                    "wc": "Wc203",
                    "prep": 8,
                    "run": 18,
                    "out": "Mat004",
                    "content": "完成盘轴无损、尺寸和外观终检。",
                    "materials": [],
                    "steps": [
                        ("无损检测", "完成盘轴无损探伤和记录。"),
                        ("尺寸外观判定", "完成盘轴尺寸、外观和放行判定。"),
                    ],
                },
            ],
        },
        {
            "code": "Rt030",
            "name": "30-叶片厂正式工艺",
            "route_spec": "热表",
            "biz": "Biz030",
            "material_code": "Mat006",
            "proc_spec": "机械加工专业",
            "remark": "叶片厂负责叶片成型、涂层与叶片终检。",
            "ops": [
                {
                    "no": "0010",
                    "name": "叶片成型加工",
                    "type": "加工",
                    "wc": "Wc301",
                    "prep": 10,
                    "run": 22,
                    "out": "Mat006",
                    "content": "完成叶片型面成型和冷端修整。",
                    "materials": [("Mat005", 1)],
                    "steps": [
                        ("叶片基准定位", "完成叶片毛坯定位和程序确认。"),
                        ("型面成型", "完成叶片型面加工和冷端修整。"),
                    ],
                },
                {
                    "no": "0020",
                    "name": "叶片表面涂层处理",
                    "type": "加工",
                    "wc": "Wc302",
                    "prep": 12,
                    "run": 26,
                    "out": "Mat006",
                    "content": "完成叶片保护涂层喷涂和固化。",
                    "materials": [("Mat009", 1)],
                    "steps": [
                        ("涂层前处理", "完成叶片表面清洁和遮蔽处理。"),
                        ("喷涂固化", "完成涂层喷涂、固化和冷却。"),
                    ],
                },
                {
                    "no": "0030",
                    "name": "叶片终检放行",
                    "type": "检验",
                    "wc": "Wc303",
                    "prep": 8,
                    "run": 16,
                    "out": "Mat006",
                    "content": "完成叶片型面、流道和外观终检。",
                    "materials": [],
                    "steps": [
                        ("型面与流道检测", "完成叶片型面和通流复核。"),
                        ("外观放行", "完成叶片外观复核和放行。"),
                    ],
                },
            ],
        },
        {
            "code": "Rt040",
            "name": "40-装配厂正式工艺",
            "route_spec": "装配",
            "biz": "Biz040",
            "material_code": "Mat011",
            "proc_spec": "装配专业",
            "remark": "装配厂负责齐套确认、总装试车和整机交付放行。",
            "ops": [
                {
                    "no": "0010",
                    "name": "齐套确认",
                    "type": "加工",
                    "wc": "Wc401",
                    "prep": 8,
                    "run": 12,
                    "out": "Mat011",
                    "content": "完成机匣件、盘轴模块、叶片组件和装配配套件齐套确认。",
                    "materials": [("Mat002", 1), ("Mat004", 1), ("Mat006", 12), ("Mat007", 1), ("Mat008", 1)],
                    "steps": [
                        ("关键件齐套复核", "复核机匣件、盘轴模块和叶片组件到位。"),
                        ("装配配套确认", "确认紧固件和密封件配套齐全。"),
                    ],
                },
                {
                    "no": "0020",
                    "name": "整机总装",
                    "type": "加工",
                    "wc": "Wc401",
                    "prep": 14,
                    "run": 32,
                    "out": "Mat011",
                    "content": "完成发动机核心机、盘轴和叶片相关总装联接。",
                    "materials": [],
                    "steps": [
                        ("核心机装配", "完成机匣、盘轴和叶片关键部位总装。"),
                        ("联接复核", "完成关键联接点力矩和状态复核。"),
                    ],
                },
                {
                    "no": "0030",
                    "name": "整机试车与交付放行",
                    "type": "检验",
                    "wc": "Wc402",
                    "prep": 10,
                    "run": 24,
                    "out": "Mat011",
                    "content": "完成整机试车、质量结论和交付放行。",
                    "materials": [("Mat010", 1), ("Mat012", 1)],
                    "steps": [
                        ("执行整机试车", "完成整机试车与关键参数采集。"),
                        ("交付放行", "完成质量结论、包装确认和交付放行。"),
                    ],
                },
            ],
        },
    ]

    return {
        "metadata": metadata,
        "admins": admins,
        "bizs": bizs,
        "users": users,
        "suppliers": [],
        "work_centers": work_centers,
        "equipments": equipments,
        "tools": tools,
        "wc_user_links": wc_user_links,
        "wc_eq_links": wc_eq_links,
        "eq_user_links": eq_user_links,
        "wc_sup_links": [],
        "warehouses": warehouses,
        "locations": locations,
        "materials": materials,
        "mboms": mboms,
        "routes": routes,
    }


CONFIG = build_config()


def build_variant(namespace: str = NAMESPACE) -> dict:
    metadata = dict(CONFIG["metadata"])
    metadata["default_version"] = "A.01"
    metadata["default_security"] = "内部"
    metadata["volume_profile"] = VOLUME_PROFILE

    builder = SeedBuilder(metadata)
    builder.build_from_config(CONFIG)
    seed = builder.seed

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
    apply_production_orders(seed, SCENARIO, namespace)
    normalize_latest_order_enums(seed)
    return seed


def build() -> dict:
    return build_variant()


def main() -> None:
    seed = build()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_PATH.write_text(
        json.dumps(seed, ensure_ascii=False, indent=2),
        encoding="utf-8-sig",
    )
    print(json.dumps(summarize_seed(seed), ensure_ascii=False, indent=2))
    print(f"已写入种子文件: {ASSET_PATH}")


if __name__ == "__main__":
    main()
