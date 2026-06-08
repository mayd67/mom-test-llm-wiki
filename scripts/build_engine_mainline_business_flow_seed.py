from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_SCRIPT_DIR = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "mom-business-data-generator"
    / "scripts"
)

if str(SKILL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_SCRIPT_DIR))

from gearbox_seed_support import (  # type: ignore  # noqa: E402
    CAT_AUX,
    CAT_KIT,
    CAT_PART,
    CAT_RAW,
    FEATURE_IMPORTANT,
    FEATURE_KEY,
    FEATURE_NORMAL,
    MAKE_BUY,
    MAKE_SELF,
    SeedBuilder,
    summarize_seed,
)
from scene_seed_upgrades import (  # type: ignore  # noqa: E402
    clear_tool_strategy_relations,
    filter_wc_supplier_relations,
    normalize_poc_security,
    normalize_release_user,
    normalize_sequence_relations,
    normalize_storage_factory_org,
    rebuild_route_sequences,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

DEFAULT_VERSION = "A.01"
SCENARIO_DATE = "2026-06-03"
OUTPUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "outputs"
    / "06_测试数据"
    / "发动机主线业务流程-多工厂一级工艺版"
)
ASSET_PATH = OUTPUT_DIR / "发动机主线业务流程-测试数据种子-V1.0.json"
NOTE_PATH = OUTPUT_DIR / "说明文件.md"


def build_config() -> dict:
    metadata = {
        "name": "发动机多工厂协同主线测试数据",
        "industry": "航空发动机",
        "product_family": "发动机总装",
        "product_model": "航发总成A1000",
        "description": (
            "根据《MOM产品主线业务场景用例-发动机多工厂协同主线》构建的导入种子，"
            "覆盖生产部一级工艺、4 个分厂子生产订单，以及装配厂执行闭环所需主数据。"
        ),
        "default_version": DEFAULT_VERSION,
        "default_security": "公开",
        "volume_profile": "标准版",
    }

    admins = [
        ("0", "公司", "ADM-CORP-001", "启航航空发动机制造有限公司", "启航航发"),
        ("ADM-CORP-001", "部门", "ADM-PD-001", "生产部", "生产部"),
        ("ADM-CORP-001", "工厂", "ADM-MC-001", "10-机加厂", "机加厂"),
        ("ADM-CORP-001", "工厂", "ADM-SH-001", "20-盘轴厂", "盘轴厂"),
        ("ADM-CORP-001", "工厂", "ADM-BL-001", "30-叶片厂", "叶片厂"),
        ("ADM-CORP-001", "工厂", "ADM-AS-001", "40-装配厂", "装配厂"),
    ]

    bizs = [
        (
            "0",
            "ORG-CORP-001",
            "启航航空发动机制造有限公司",
            "启航航发",
            "公司",
            "ADM-CORP-001",
            "",
            "发动机多工厂协同主线示例公司",
        ),
        (
            "ORG-CORP-001",
            "ORG-PD-001",
            "生产部",
            "生产部",
            "工厂",
            "ADM-PD-001",
            "装配专业",
            "承接厂际协同计划与一级工艺展开。",
        ),
        (
            "ORG-CORP-001",
            "ORG-MC-001",
            "10-机加厂",
            "机加厂",
            "工厂",
            "ADM-MC-001",
            "机械加工专业",
            "负责机匣组件机加与尺寸放行。",
        ),
        ("ORG-MC-001", "ORG-MC-WS-001", "机加车间", "机加车间", "车间", "ADM-MC-001"),
        ("ORG-MC-WS-001", "ORG-MC-TM-001", "机加班组", "机加班组", "班组", "ADM-MC-001"),
        ("ORG-MC-WS-001", "ORG-MC-QC-001", "机加检验组", "机加检验", "班组", "ADM-MC-001"),
        (
            "ORG-CORP-001",
            "ORG-SH-001",
            "20-盘轴厂",
            "盘轴厂",
            "工厂",
            "ADM-SH-001",
            "机械加工专业",
            "负责盘轴组件加工、平衡与终检。",
        ),
        ("ORG-SH-001", "ORG-SH-WS-001", "盘轴车间", "盘轴车间", "车间", "ADM-SH-001"),
        ("ORG-SH-WS-001", "ORG-SH-TM-001", "盘轴班组", "盘轴班组", "班组", "ADM-SH-001"),
        ("ORG-SH-WS-001", "ORG-SH-QC-001", "盘轴检验组", "盘轴检验", "班组", "ADM-SH-001"),
        (
            "ORG-CORP-001",
            "ORG-BL-001",
            "30-叶片厂",
            "叶片厂",
            "工厂",
            "ADM-BL-001",
            "机械加工专业",
            "负责叶片成型、涂层与终检。",
        ),
        ("ORG-BL-001", "ORG-BL-WS-001", "叶片车间", "叶片车间", "车间", "ADM-BL-001"),
        ("ORG-BL-WS-001", "ORG-BL-TM-001", "叶片班组", "叶片班组", "班组", "ADM-BL-001"),
        ("ORG-BL-WS-001", "ORG-BL-QC-001", "叶片检验组", "叶片检验", "班组", "ADM-BL-001"),
        (
            "ORG-CORP-001",
            "ORG-AS-001",
            "40-装配厂",
            "装配厂",
            "工厂",
            "ADM-AS-001",
            "装配专业",
            "负责总装、试车、完工入库与交付放行。",
        ),
        ("ORG-AS-001", "ORG-AS-WS-001", "总装车间", "总装车间", "车间", "ADM-AS-001"),
        ("ORG-AS-WS-001", "ORG-AS-TM-001", "总装班组", "总装班组", "班组", "ADM-AS-001"),
        ("ORG-AS-WS-001", "ORG-AS-QC-001", "总装检验组", "总装检验", "班组", "ADM-AS-001"),
    ]

    users = [
        ("zhangqiang", "张强", "重要", "男", "ADM-PD-001", "ORG-PD-001", "生产部部长"),
        ("liumin", "刘敏", "重要", "女", "ADM-PD-001", "ORG-PD-001", "计划员"),
        ("chengang", "陈刚", "一般", "男", "ADM-MC-001", "ORG-MC-TM-001", "机加班组长"),
        ("wanglei", "王磊", "一般", "男", "ADM-AS-001", "ORG-AS-001", "仓库管理员"),
        ("zhaoyun", "赵云", "一般", "男", "ADM-AS-001", "ORG-AS-TM-001", "装配班组长"),
        ("qianfeng", "钱峰", "一般", "男", "ADM-AS-001", "ORG-AS-TM-001", "装配操作工"),
        ("sunjie", "孙洁", "一般", "女", "ADM-AS-001", "ORG-AS-QC-001", "检验员"),
        ("hanbo", "韩博", "一般", "男", "ADM-SH-001", "ORG-SH-TM-001", "盘轴班组长"),
        ("linna", "林娜", "一般", "女", "ADM-BL-001", "ORG-BL-TM-001", "叶片班组长"),
        ("chenrui", "陈睿", "重要", "男", "ADM-PD-001", "ORG-PD-001", "工艺工程师"),
    ]

    work_centers = [
        {"code": "WC-PD-MC-01", "name": "10-机加厂协同中心", "biz": "ORG-PD-001", "wc_type": "组织", "wc_class": "加工", "remark": "一级工艺阶段 10-机加厂。"},
        {"code": "WC-PD-SH-01", "name": "20-盘轴厂协同中心", "biz": "ORG-PD-001", "wc_type": "组织", "wc_class": "加工", "remark": "一级工艺阶段 20-盘轴厂。"},
        {"code": "WC-PD-BL-01", "name": "30-叶片厂协同中心", "biz": "ORG-PD-001", "wc_type": "组织", "wc_class": "加工", "remark": "一级工艺阶段 30-叶片厂。"},
        {"code": "WC-PD-AS-01", "name": "40-装配厂协同中心", "biz": "ORG-PD-001", "wc_type": "组织", "wc_class": "加工", "remark": "一级工艺阶段 40-装配厂。"},
        {"code": "WC-MC-01", "name": "机加粗加工中心", "biz": "ORG-MC-TM-001", "wc_type": "组织", "wc_class": "加工", "remark": "机匣组件粗精加工。"},
        {"code": "WC-QC-MC-01", "name": "机加尺寸检验中心", "biz": "ORG-MC-QC-001", "wc_type": "组织", "wc_class": "检验", "remark": "机匣组件终检放行。"},
        {"code": "WC-SH-01", "name": "盘轴加工中心", "biz": "ORG-SH-TM-001", "wc_type": "组织", "wc_class": "加工", "remark": "盘轴组件加工与平衡。"},
        {"code": "WC-QC-SH-01", "name": "盘轴终检中心", "biz": "ORG-SH-QC-001", "wc_type": "组织", "wc_class": "检验", "remark": "盘轴组件终检放行。"},
        {"code": "WC-BL-01", "name": "叶片加工中心", "biz": "ORG-BL-TM-001", "wc_type": "组织", "wc_class": "加工", "remark": "叶片组件成型与涂层。"},
        {"code": "WC-QC-BL-01", "name": "叶片终检中心", "biz": "ORG-BL-QC-001", "wc_type": "组织", "wc_class": "检验", "remark": "叶片组件终检放行。"},
        {"code": "WC-ASM-01", "name": "总装工作中心", "biz": "ORG-AS-TM-001", "wc_type": "组织", "wc_class": "加工", "remark": "总装准备、总装与完工装配。"},
        {"code": "WC-QC-ASM-01", "name": "总装检验中心", "biz": "ORG-AS-QC-001", "wc_type": "组织", "wc_class": "检验", "remark": "装配厂首检、专检与放行检验。"},
    ]

    equipments = [
        {"code": "EQ-MC-01", "name": "五轴龙门加工中心", "model": "MC-500", "biz": "ORG-MC-TM-001", "remark": "机匣组件关键孔面加工。"},
        {"code": "EQ-QC-MC-01", "name": "机匣三坐标测量机", "model": "CMM-1200", "biz": "ORG-MC-QC-001", "remark": "机匣组件尺寸终检。"},
        {"code": "EQ-SH-01", "name": "盘轴复合加工机", "model": "SH-600", "biz": "ORG-SH-TM-001", "remark": "盘轴组件复合加工与动平衡。"},
        {"code": "EQ-QC-SH-01", "name": "盘轴探伤检测台", "model": "UT-200", "biz": "ORG-SH-QC-001", "remark": "盘轴组件超声终检。"},
        {"code": "EQ-BL-01", "name": "叶片成型磨床", "model": "BL-220", "biz": "ORG-BL-TM-001", "remark": "叶片型面成型与修整。"},
        {"code": "EQ-QC-BL-01", "name": "叶片流道检测台", "model": "FL-30", "biz": "ORG-BL-QC-001", "remark": "叶片流道与外观检测。"},
        {"code": "EQ-ASM-01", "name": "发动机总装定位工位", "model": "ASM-100", "biz": "ORG-AS-TM-001", "remark": "总装定位与联接。"},
        {"code": "EQ-QC-ASM-01", "name": "发动机总装检验台", "model": "QC-ASM-01", "biz": "ORG-AS-QC-001", "remark": "首检、专检和总装终检。"},
    ]

    tools = [
        {
            "code": "TOOL-MC-01",
            "name": "机匣定位夹具",
            "material_category": CAT_PART,
            "make_type": MAKE_SELF,
            "tooling_category": "专用工装",
            "feature": FEATURE_KEY,
            "model": "MC-JJ-01",
            "spec": "机匣找正定位",
            "remark": "机加厂机匣组件专用定位夹具。",
            "life_times": 50000,
            "life_days": 365,
        },
        {
            "code": "TOOL-SH-01",
            "name": "盘轴动平衡工装",
            "material_category": CAT_PART,
            "make_type": MAKE_SELF,
            "tooling_category": "专用工装",
            "feature": FEATURE_IMPORTANT,
            "model": "SH-PH-01",
            "spec": "盘轴平衡校正",
            "remark": "盘轴厂动平衡修正工装。",
            "life_times": 40000,
            "life_days": 365,
        },
        {
            "code": "TOOL-BL-01",
            "name": "叶片型面检具",
            "material_category": CAT_PART,
            "make_type": MAKE_SELF,
            "tooling_category": "专用工装",
            "feature": FEATURE_KEY,
            "model": "BL-JJ-01",
            "spec": "叶片型面检测",
            "remark": "叶片厂型面快速检测检具。",
            "life_times": 40000,
            "life_days": 365,
        },
        {
            "code": "TOOL-ASM-01",
            "name": "发动机总装吊具",
            "material_category": CAT_PART,
            "make_type": MAKE_SELF,
            "tooling_category": "专用工装",
            "feature": FEATURE_IMPORTANT,
            "model": "ASM-DJ-01",
            "spec": "整机吊装定位",
            "remark": "装配厂总装吊装定位工装。",
            "life_times": 30000,
            "life_days": 365,
        },
    ]

    wc_user_links = [
        ("WC-PD-MC-01", "liumin"),
        ("WC-PD-SH-01", "liumin"),
        ("WC-PD-BL-01", "liumin"),
        ("WC-PD-AS-01", "liumin"),
        ("WC-MC-01", "chengang"),
        ("WC-SH-01", "hanbo"),
        ("WC-BL-01", "linna"),
        ("WC-ASM-01", "zhaoyun"),
        ("WC-ASM-01", "qianfeng"),
        ("WC-QC-ASM-01", "sunjie"),
    ]

    wc_eq_links = [
        ("WC-MC-01", "EQ-MC-01"),
        ("WC-QC-MC-01", "EQ-QC-MC-01"),
        ("WC-SH-01", "EQ-SH-01"),
        ("WC-QC-SH-01", "EQ-QC-SH-01"),
        ("WC-BL-01", "EQ-BL-01"),
        ("WC-QC-BL-01", "EQ-QC-BL-01"),
        ("WC-ASM-01", "EQ-ASM-01"),
        ("WC-QC-ASM-01", "EQ-QC-ASM-01"),
    ]

    eq_user_links = [
        ("EQ-MC-01", "chengang"),
        ("EQ-SH-01", "hanbo"),
        ("EQ-BL-01", "linna"),
        ("EQ-ASM-01", "qianfeng"),
        ("EQ-QC-ASM-01", "sunjie"),
    ]

    warehouses = [
        ("WH-MC-01", "机加在制品库", "ORG-MC-001", "ERP一级库", "普通库房", "存放机匣毛坯与机加完件。"),
        ("WH-SH-01", "盘轴在制品库", "ORG-SH-001", "ERP一级库", "普通库房", "存放盘轴毛坯与盘轴组件。"),
        ("WH-BL-01", "叶片在制品库", "ORG-BL-001", "ERP一级库", "普通库房", "存放叶片毛坯与叶片组件套。"),
        ("WH-ASM-RAW", "装配原材料库", "ORG-AS-001", "ERP一级库", "普通库房", "装配厂齐套与装入物料。"),
        ("WH-FG-01", "发动机成品库", "ORG-AS-001", "ERP一级库", "普通库房", "装配厂合格完工入库。"),
        ("WH-SCR-01", "废品库", "ORG-AS-001", "ERP一级库", "普通库房", "装配厂报废隔离库存放。"),
    ]

    locations = [
        ("LOC-MC-01", "MC-01-01", "ORG-MC-001", "WH-MC-01", "机匣毛坯区。"),
        ("LOC-MC-02", "MC-01-02", "ORG-MC-001", "WH-MC-01", "机匣完件区。"),
        ("LOC-SH-01", "SH-01-01", "ORG-SH-001", "WH-SH-01", "盘轴毛坯区。"),
        ("LOC-SH-02", "SH-01-02", "ORG-SH-001", "WH-SH-01", "盘轴完件区。"),
        ("LOC-BL-01", "BL-01-01", "ORG-BL-001", "WH-BL-01", "叶片毛坯区。"),
        ("LOC-BL-02", "BL-01-02", "ORG-BL-001", "WH-BL-01", "叶片组件区。"),
        ("LOC-ASM-RAW-01", "A-01-01", "ORG-AS-001", "WH-ASM-RAW", "装配原材料库主库位。"),
        ("LOC-FG-01", "FG-01-01", "ORG-AS-001", "WH-FG-01", "发动机成品库位。"),
        ("LOC-SCR-01", "SCR-01-01", "ORG-AS-001", "WH-SCR-01", "报废库存放库位。"),
    ]

    materials = [
        {
            "code": "MAT-CAS-BLANK-001",
            "name": "机匣毛坯件",
            "category": CAT_RAW,
            "make_type": MAKE_BUY,
            "feature": FEATURE_IMPORTANT,
            "drawing": "A1000-CAS-BLK",
            "spec": "机匣毛坯",
            "remark": "机加厂输入件。",
        },
        {
            "code": "MAT-SHAFT-BLANK-001",
            "name": "盘轴毛坯件",
            "category": CAT_RAW,
            "make_type": MAKE_BUY,
            "feature": FEATURE_IMPORTANT,
            "drawing": "A1000-SHAFT-BLK",
            "spec": "盘轴毛坯",
            "remark": "盘轴厂输入件。",
        },
        {
            "code": "MAT-BLADE-BLANK-001",
            "name": "叶片毛坯件",
            "category": CAT_RAW,
            "make_type": MAKE_BUY,
            "feature": FEATURE_NORMAL,
            "drawing": "A1000-BLADE-BLK",
            "spec": "叶片毛坯",
            "remark": "叶片厂输入件。",
        },
        {
            "code": "MAT-COAT-001",
            "name": "叶片涂层辅料",
            "category": CAT_AUX,
            "make_type": MAKE_BUY,
            "feature": FEATURE_NORMAL,
            "drawing": "A1000-COAT-001",
            "spec": "叶片保护涂层辅料",
            "remark": "叶片组件涂层处理耗材。",
        },
        {
            "code": "MAT-CAS-001",
            "name": "机匣组件",
            "category": CAT_PART,
            "make_type": MAKE_SELF,
            "feature": FEATURE_KEY,
            "drawing": "A1000-CAS-001",
            "spec": "机匣组件",
            "remark": "用于装配领料。",
        },
        {
            "code": "MAT-SHAFT-001",
            "name": "盘轴组件",
            "category": CAT_PART,
            "make_type": MAKE_SELF,
            "feature": FEATURE_KEY,
            "drawing": "A1000-SHAFT-001",
            "spec": "盘轴组件",
            "remark": "用于装配领料。",
        },
        {
            "code": "MAT-BLADESET-001",
            "name": "叶片组件套",
            "category": CAT_PART,
            "make_type": MAKE_SELF,
            "feature": FEATURE_KEY,
            "drawing": "A1000-BLADESET-001",
            "spec": "叶片组件套",
            "remark": "用于装配领料。",
        },
        {
            "code": "MAT-ENG-001",
            "name": "航发总成A1000",
            "category": CAT_PART,
            "make_type": MAKE_SELF,
            "feature": FEATURE_KEY,
            "drawing": "A1000-ENG-001",
            "model": "A1000",
            "spec": "发动机总成",
            "remark": "主线场景最终交付物。",
            "batch": "是",
            "serial": "是",
        },
        {
            "code": "MAT-STD-001",
            "name": "总装标准件包",
            "category": CAT_KIT,
            "make_type": MAKE_BUY,
            "feature": FEATURE_NORMAL,
            "drawing": "A1000-STD-001",
            "spec": "紧固件标准包",
            "remark": "装配辅助标准件。",
        },
        {
            "code": "MAT-SEAL-001",
            "name": "密封组件包",
            "category": CAT_KIT,
            "make_type": MAKE_BUY,
            "feature": FEATURE_IMPORTANT,
            "drawing": "A1000-SEAL-001",
            "spec": "密封组件",
            "remark": "装配密封类辅件。",
        },
    ]

    mboms = [
        {
            "code": "MBOM-ENG-A1000-V1",
            "material_code": "MAT-ENG-001",
            "name": "航发总成A1000 MBOM",
            "nodes": [
                {"level": 0, "material_code": "MAT-ENG-001", "qty": 1},
                {"level": 1, "material_code": "MAT-CAS-001", "qty": 1, "parent_material": "MAT-ENG-001", "parent_version": DEFAULT_VERSION},
                {"level": 1, "material_code": "MAT-SHAFT-001", "qty": 1, "parent_material": "MAT-ENG-001", "parent_version": DEFAULT_VERSION},
                {"level": 1, "material_code": "MAT-BLADESET-001", "qty": 1, "parent_material": "MAT-ENG-001", "parent_version": DEFAULT_VERSION},
                {"level": 1, "material_code": "MAT-STD-001", "qty": 1, "parent_material": "MAT-ENG-001", "parent_version": DEFAULT_VERSION},
                {"level": 1, "material_code": "MAT-SEAL-001", "qty": 1, "parent_material": "MAT-ENG-001", "parent_version": DEFAULT_VERSION},
            ],
        }
    ]

    routes = [
        {
            "code": "RT-L1-ENG-A1000-V1",
            "name": "RT-L1-ENG-A1000-V1",
            "route_spec": "通用",
            "proc_spec": "机械加工专业",
            "biz": "ORG-PD-001",
            "material_code": "MAT-ENG-001",
            "remark": "一级工艺路线：10-机加厂、20-盘轴厂、30-叶片厂、40-装配厂。",
            "ops": [
                {
                    "no": "10",
                    "name": "10-机加厂",
                    "type": "加工",
                    "wc": "WC-PD-MC-01",
                    "prep": 10,
                    "run": 20,
                    "out": "MAT-CAS-001",
                    "spec": "机械加工专业",
                    "content": "生产部协同机加厂完成机匣组件交付。",
                    "steps": [
                        ("确认机匣组件计划", "确认机加厂子生产订单、数量与交付节拍。"),
                        ("接收机匣组件完工反馈", "接收并确认机匣组件完工状态。"),
                    ],
                },
                {
                    "no": "20",
                    "name": "20-盘轴厂",
                    "type": "加工",
                    "wc": "WC-PD-SH-01",
                    "prep": 10,
                    "run": 20,
                    "out": "MAT-SHAFT-001",
                    "spec": "机械加工专业",
                    "content": "生产部协同盘轴厂完成盘轴组件交付。",
                    "steps": [
                        ("确认盘轴组件计划", "确认盘轴厂子生产订单、数量与交付节拍。"),
                        ("接收盘轴组件完工反馈", "接收并确认盘轴组件完工状态。"),
                    ],
                },
                {
                    "no": "30",
                    "name": "30-叶片厂",
                    "type": "加工",
                    "wc": "WC-PD-BL-01",
                    "prep": 10,
                    "run": 20,
                    "out": "MAT-BLADESET-001",
                    "spec": "机械加工专业",
                    "content": "生产部协同叶片厂完成叶片组件套交付。",
                    "steps": [
                        ("确认叶片组件计划", "确认叶片厂子生产订单、数量与交付节拍。"),
                        ("接收叶片组件完工反馈", "接收并确认叶片组件套完工状态。"),
                    ],
                },
                {
                    "no": "40",
                    "name": "40-装配厂",
                    "type": "加工",
                    "wc": "WC-PD-AS-01",
                    "prep": 12,
                    "run": 28,
                    "out": "MAT-ENG-001",
                    "spec": "装配专业",
                    "content": "生产部协同装配厂完成总装试车与交付。",
                    "steps": [
                        ("确认装配厂计划", "确认装配厂子生产订单、正式工艺路线与释放条件。"),
                        ("接收装配完工反馈", "接收并确认装配、试车、入库与交付状态。"),
                    ],
                },
            ],
        },
        {
            "code": "RT-MC-CAS-A1000-V1",
            "name": "机匣组件正式工艺",
            "route_spec": "机加",
            "proc_spec": "机械加工专业",
            "biz": "ORG-MC-001",
            "material_code": "MAT-CAS-001",
            "remark": "机加厂正式工艺。",
            "ops": [
                {
                    "no": "OP10",
                    "name": "机匣粗加工",
                    "type": "加工",
                    "wc": "WC-MC-01",
                    "prep": 12,
                    "run": 40,
                    "out": "MAT-CAS-001",
                    "spec": "机械加工专业",
                    "content": "完成机匣毛坯装夹、粗加工与找正。",
                    "materials": [("MAT-CAS-BLANK-001", 1)],
                    "steps": [
                        ("毛坯核对", "核对机匣毛坯批次与状态。"),
                        ("粗加工", "完成关键孔面与外形粗加工。"),
                    ],
                },
                {
                    "no": "OP20",
                    "name": "机匣精加工",
                    "type": "加工",
                    "wc": "WC-MC-01",
                    "prep": 10,
                    "run": 32,
                    "out": "MAT-CAS-001",
                    "spec": "机械加工专业",
                    "content": "完成机匣关键孔面与装配基准精加工。",
                    "steps": [
                        ("精加工关键面", "完成机匣关键孔面与安装面精加工。"),
                        ("清理去毛刺", "完成清理、去毛刺和外观复核。"),
                    ],
                },
                {
                    "no": "OP30",
                    "name": "机匣终检",
                    "type": "检验",
                    "wc": "WC-QC-MC-01",
                    "prep": 8,
                    "run": 18,
                    "out": "MAT-CAS-001",
                    "spec": "机械加工专业",
                    "content": "完成机匣组件尺寸终检与放行。",
                    "steps": [
                        ("三坐标检测", "完成关键尺寸与同轴度检测。"),
                        ("终检放行", "形成机匣组件终检结论。"),
                    ],
                },
            ],
        },
        {
            "code": "RT-SH-SHAFT-A1000-V1",
            "name": "盘轴组件正式工艺",
            "route_spec": "机加",
            "proc_spec": "机械加工专业",
            "biz": "ORG-SH-001",
            "material_code": "MAT-SHAFT-001",
            "remark": "盘轴厂正式工艺。",
            "ops": [
                {
                    "no": "OP10",
                    "name": "盘轴加工",
                    "type": "加工",
                    "wc": "WC-SH-01",
                    "prep": 12,
                    "run": 36,
                    "out": "MAT-SHAFT-001",
                    "spec": "机械加工专业",
                    "content": "完成盘轴毛坯复合加工。",
                    "materials": [("MAT-SHAFT-BLANK-001", 1)],
                    "steps": [
                        ("毛坯装夹", "完成盘轴毛坯装夹和基准确认。"),
                        ("车铣复合加工", "完成盘轴关键面复合加工。"),
                    ],
                },
                {
                    "no": "OP20",
                    "name": "盘轴动平衡",
                    "type": "加工",
                    "wc": "WC-SH-01",
                    "prep": 8,
                    "run": 20,
                    "out": "MAT-SHAFT-001",
                    "spec": "机械加工专业",
                    "content": "完成盘轴组件动平衡与修正。",
                    "steps": [
                        ("动平衡检测", "完成盘轴动平衡检测。"),
                        ("配重修正", "完成配重调整和复测。"),
                    ],
                },
                {
                    "no": "OP30",
                    "name": "盘轴终检",
                    "type": "检验",
                    "wc": "WC-QC-SH-01",
                    "prep": 8,
                    "run": 16,
                    "out": "MAT-SHAFT-001",
                    "spec": "机械加工专业",
                    "content": "完成盘轴组件终检与放行。",
                    "steps": [
                        ("无损检测", "完成盘轴探伤与尺寸检查。"),
                        ("终检放行", "形成盘轴组件终检结论。"),
                    ],
                },
            ],
        },
        {
            "code": "RT-BL-BLADESET-A1000-V1",
            "name": "叶片组件套正式工艺",
            "route_spec": "热表",
            "proc_spec": "机械加工专业",
            "biz": "ORG-BL-001",
            "material_code": "MAT-BLADESET-001",
            "remark": "叶片厂正式工艺。",
            "ops": [
                {
                    "no": "OP10",
                    "name": "叶片成型",
                    "type": "加工",
                    "wc": "WC-BL-01",
                    "prep": 10,
                    "run": 28,
                    "out": "MAT-BLADESET-001",
                    "spec": "机械加工专业",
                    "content": "完成叶片毛坯成型与修整。",
                    "materials": [("MAT-BLADE-BLANK-001", 1)],
                    "steps": [
                        ("型面定位", "完成叶片毛坯定位与程序确认。"),
                        ("成型修整", "完成叶片型面成型与冷端修整。"),
                    ],
                },
                {
                    "no": "OP20",
                    "name": "叶片涂层",
                    "type": "加工",
                    "wc": "WC-BL-01",
                    "prep": 10,
                    "run": 24,
                    "out": "MAT-BLADESET-001",
                    "spec": "机械加工专业",
                    "content": "完成叶片保护涂层处理。",
                    "materials": [("MAT-COAT-001", 1)],
                    "steps": [
                        ("表面前处理", "完成表面清洁与前处理。"),
                        ("喷涂固化", "完成保护涂层喷涂与固化。"),
                    ],
                },
                {
                    "no": "OP30",
                    "name": "叶片终检",
                    "type": "检验",
                    "wc": "WC-QC-BL-01",
                    "prep": 8,
                    "run": 16,
                    "out": "MAT-BLADESET-001",
                    "spec": "机械加工专业",
                    "content": "完成叶片组件套终检与放行。",
                    "steps": [
                        ("型面检测", "完成型面、流道与外观复核。"),
                        ("终检放行", "形成叶片组件套终检结论。"),
                    ],
                },
            ],
        },
        {
            "code": "RT-ASM-ENG-A1000-V1",
            "name": "装配厂正式工艺",
            "route_spec": "装配",
            "proc_spec": "装配专业",
            "biz": "ORG-AS-001",
            "material_code": "MAT-ENG-001",
            "remark": "装配厂正式工艺路线，包含 OP10 装配准备、OP20 总装、OP30 完工装配。",
            "ops": [
                {
                    "no": "OP10",
                    "name": "装配准备",
                    "type": "加工",
                    "wc": "WC-ASM-01",
                    "prep": 10,
                    "run": 18,
                    "out": "MAT-ENG-001",
                    "spec": "装配专业",
                    "content": "完成装配准备与齐套确认。",
                    "materials": [
                        ("MAT-CAS-001", 1),
                        ("MAT-SHAFT-001", 1),
                        ("MAT-BLADESET-001", 1),
                    ],
                    "steps": [
                        ("核对装配齐套", "核对机匣组件、盘轴组件和叶片组件套。"),
                        ("装配工位准备", "确认工位、工具、SOP 与质量前置条件。"),
                    ],
                },
                {
                    "no": "OP20",
                    "name": "总装",
                    "type": "加工",
                    "wc": "WC-ASM-01",
                    "prep": 14,
                    "run": 36,
                    "out": "MAT-ENG-001",
                    "spec": "装配专业",
                    "content": "完成发动机总装联接。",
                    "steps": [
                        ("ST20-01 机匣定位", "完成机匣定位与装配基准确认。"),
                        ("ST20-02 盘轴装配", "完成盘轴装配与关键连接紧固。"),
                        ("ST20-03 叶片组件装配", "完成叶片组件装配与间隙复核。"),
                    ],
                },
                {
                    "no": "OP30",
                    "name": "完工装配",
                    "type": "加工",
                    "wc": "WC-ASM-01",
                    "prep": 12,
                    "run": 24,
                    "out": "MAT-ENG-001",
                    "spec": "装配专业",
                    "content": "完成完工装配、试车前状态确认与入库前准备。",
                    "materials": [
                        ("MAT-STD-001", 1),
                        ("MAT-SEAL-001", 1),
                    ],
                    "steps": [
                        ("完工复核", "完成关键连接复核与状态确认。"),
                        ("入库准备", "完成入库前标签、批次和状态准备。"),
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


def ensure_order_workbook(seed: dict) -> tuple[list[dict], list[dict]]:
    workbook = seed.setdefault("workbooks", {}).setdefault("生产订单_模板.xlsx", {})
    orders = workbook.setdefault("生产订单", [])
    picks = workbook.setdefault("备料清单", [])
    orders.clear()
    picks.clear()
    return orders, picks


def build_orders(seed: dict) -> None:
    orders, picks = ensure_order_workbook(seed)

    common = {
        "订单类型": "标准",
        "*密级": "公开",
        "集成系统": "MOM-SEED",
    }

    orders.extend(
        [
            {
                **common,
                "*物料版本号": DEFAULT_VERSION,
                "*物料编码": "MAT-ENG-001",
                "BOM版本号": DEFAULT_VERSION,
                "BOM编码": "MBOM-ENG-A1000-V1",
                "制造型号": "A1000",
                "工艺路线版本号": DEFAULT_VERSION,
                "工艺路线编码": "RT-L1-ENG-A1000-V1",
                "*计量单位": "个",
                "*计划数量": 10,
                "计划产出数量": 10,
                "合格数量": 0,
                "报废数量": 0,
                "已释放数量": 0,
                "*计划开始时间": "2026-06-03 09:00:00",
                "*计划结束时间": "2026-06-20 18:00:00",
                "实际开始时间": "",
                "计划类型": "零部件生产计划",
                "排产状态": "零部件生产已排产",
                "实际结束时间": "",
                "业务状态": "已展开",
                "优先级": 1,
                "计划员": "liumin",
                "*控制状态": "正常",
                "释放状态": "未释放",
                "*所属组织": "ORG-PD-001",
                "*编码": "PO-ENG-A1000-20260603-0001",
                "备注": "厂际协同计划父生产订单，对应 E2E-MOM-ENG-001。",
                "集成数据主键": "PO-ENG-A1000-20260603-0001",
                "*集成创建时间": "2026-06-03 08:30:00",
            },
            {
                **common,
                "*物料版本号": DEFAULT_VERSION,
                "*物料编码": "MAT-CAS-001",
                "BOM版本号": "",
                "BOM编码": "",
                "制造型号": "A1000",
                "工艺路线版本号": DEFAULT_VERSION,
                "工艺路线编码": "RT-MC-CAS-A1000-V1",
                "*计量单位": "个",
                "*计划数量": 10,
                "计划产出数量": 10,
                "合格数量": 0,
                "报废数量": 0,
                "已释放数量": 0,
                "*计划开始时间": "2026-06-03 10:00:00",
                "*计划结束时间": "2026-06-11 18:00:00",
                "实际开始时间": "",
                "计划类型": "零部件加工计划",
                "排产状态": "无",
                "实际结束时间": "",
                "业务状态": "初始",
                "优先级": 2,
                "计划员": "liumin",
                "*控制状态": "正常",
                "释放状态": "未释放",
                "*所属组织": "ORG-MC-001",
                "*编码": "PO-ENG-A1000-20260603-0001-001",
                "备注": "10-机加厂子生产订单。",
                "集成数据主键": "PO-ENG-A1000-20260603-0001-001",
                "*集成创建时间": "2026-06-03 09:00:00",
            },
            {
                **common,
                "*物料版本号": DEFAULT_VERSION,
                "*物料编码": "MAT-SHAFT-001",
                "BOM版本号": "",
                "BOM编码": "",
                "制造型号": "A1000",
                "工艺路线版本号": DEFAULT_VERSION,
                "工艺路线编码": "RT-SH-SHAFT-A1000-V1",
                "*计量单位": "个",
                "*计划数量": 10,
                "计划产出数量": 10,
                "合格数量": 0,
                "报废数量": 0,
                "已释放数量": 0,
                "*计划开始时间": "2026-06-03 10:00:00",
                "*计划结束时间": "2026-06-12 18:00:00",
                "实际开始时间": "",
                "计划类型": "零部件加工计划",
                "排产状态": "无",
                "实际结束时间": "",
                "业务状态": "初始",
                "优先级": 2,
                "计划员": "liumin",
                "*控制状态": "正常",
                "释放状态": "未释放",
                "*所属组织": "ORG-SH-001",
                "*编码": "PO-ENG-A1000-20260603-0001-002",
                "备注": "20-盘轴厂子生产订单。",
                "集成数据主键": "PO-ENG-A1000-20260603-0001-002",
                "*集成创建时间": "2026-06-03 09:05:00",
            },
            {
                **common,
                "*物料版本号": DEFAULT_VERSION,
                "*物料编码": "MAT-BLADESET-001",
                "BOM版本号": "",
                "BOM编码": "",
                "制造型号": "A1000",
                "工艺路线版本号": DEFAULT_VERSION,
                "工艺路线编码": "RT-BL-BLADESET-A1000-V1",
                "*计量单位": "个",
                "*计划数量": 10,
                "计划产出数量": 10,
                "合格数量": 0,
                "报废数量": 0,
                "已释放数量": 0,
                "*计划开始时间": "2026-06-03 10:00:00",
                "*计划结束时间": "2026-06-13 18:00:00",
                "实际开始时间": "",
                "计划类型": "零部件加工计划",
                "排产状态": "无",
                "实际结束时间": "",
                "业务状态": "初始",
                "优先级": 2,
                "计划员": "liumin",
                "*控制状态": "正常",
                "释放状态": "未释放",
                "*所属组织": "ORG-BL-001",
                "*编码": "PO-ENG-A1000-20260603-0001-003",
                "备注": "30-叶片厂子生产订单。",
                "集成数据主键": "PO-ENG-A1000-20260603-0001-003",
                "*集成创建时间": "2026-06-03 09:10:00",
            },
            {
                **common,
                "*物料版本号": DEFAULT_VERSION,
                "*物料编码": "MAT-ENG-001",
                "BOM版本号": DEFAULT_VERSION,
                "BOM编码": "MBOM-ENG-A1000-V1",
                "制造型号": "A1000",
                "工艺路线版本号": DEFAULT_VERSION,
                "工艺路线编码": "RT-ASM-ENG-A1000-V1",
                "*计量单位": "个",
                "*计划数量": 10,
                "计划产出数量": 10,
                "合格数量": 0,
                "报废数量": 0,
                "已释放数量": 0,
                "*计划开始时间": "2026-06-13 08:30:00",
                "*计划结束时间": "2026-06-20 18:00:00",
                "实际开始时间": "",
                "计划类型": "零部件加工计划",
                "排产状态": "无",
                "实际结束时间": "",
                "业务状态": "初始",
                "优先级": 1,
                "计划员": "liumin",
                "*控制状态": "正常",
                "释放状态": "未释放",
                "*所属组织": "ORG-AS-001",
                "*编码": "PO-ENG-A1000-20260603-0001-004",
                "备注": "40-装配厂子生产订单，释放数量与释放状态由后续业务动作驱动。",
                "集成数据主键": "PO-ENG-A1000-20260603-0001-004",
                "*集成创建时间": "2026-06-03 09:15:00",
            },
        ]
    )

    picks.extend(
        [
            {
                "*生产订单编码": "PO-ENG-A1000-20260603-0001-001",
                "*物料版本号": DEFAULT_VERSION,
                "*物料编码": "MAT-CAS-BLANK-001",
                "工序名称": "机匣粗加工",
                "*需求数量": 10,
                "*子件比例": 1,
                "替换件物料版本号": "",
                "替换件物料编码": "",
                "是否必须装入": "是",
                "工序编码": "OP10",
            },
            {
                "*生产订单编码": "PO-ENG-A1000-20260603-0001-002",
                "*物料版本号": DEFAULT_VERSION,
                "*物料编码": "MAT-SHAFT-BLANK-001",
                "工序名称": "盘轴加工",
                "*需求数量": 10,
                "*子件比例": 1,
                "替换件物料版本号": "",
                "替换件物料编码": "",
                "是否必须装入": "是",
                "工序编码": "OP10",
            },
            {
                "*生产订单编码": "PO-ENG-A1000-20260603-0001-003",
                "*物料版本号": DEFAULT_VERSION,
                "*物料编码": "MAT-BLADE-BLANK-001",
                "工序名称": "叶片成型",
                "*需求数量": 10,
                "*子件比例": 1,
                "替换件物料版本号": "",
                "替换件物料编码": "",
                "是否必须装入": "是",
                "工序编码": "OP10",
            },
            {
                "*生产订单编码": "PO-ENG-A1000-20260603-0001-004",
                "*物料版本号": DEFAULT_VERSION,
                "*物料编码": "MAT-CAS-001",
                "工序名称": "装配准备",
                "*需求数量": 10,
                "*子件比例": 1,
                "替换件物料版本号": "",
                "替换件物料编码": "",
                "是否必须装入": "是",
                "工序编码": "OP10",
            },
            {
                "*生产订单编码": "PO-ENG-A1000-20260603-0001-004",
                "*物料版本号": DEFAULT_VERSION,
                "*物料编码": "MAT-SHAFT-001",
                "工序名称": "装配准备",
                "*需求数量": 10,
                "*子件比例": 1,
                "替换件物料版本号": "",
                "替换件物料编码": "",
                "是否必须装入": "是",
                "工序编码": "OP10",
            },
            {
                "*生产订单编码": "PO-ENG-A1000-20260603-0001-004",
                "*物料版本号": DEFAULT_VERSION,
                "*物料编码": "MAT-BLADESET-001",
                "工序名称": "装配准备",
                "*需求数量": 10,
                "*子件比例": 1,
                "替换件物料版本号": "",
                "替换件物料编码": "",
                "是否必须装入": "是",
                "工序编码": "OP10",
            },
        ]
    )


def mark_level1_route(seed: dict) -> None:
    routes = (
        seed.get("workbooks", {})
        .get("产品与工艺_模板.xlsx", {})
        .get("工艺路线", [])
    )
    for row in routes:
        if row.get("*编码") == "RT-L1-ENG-A1000-V1":
            row["*工艺类型"] = "一级工艺"
            row["工艺专业"] = "通用"
            row["备注"] = "生产部一级工艺路线，用于一级工艺展开。"

    ops = (
        seed.get("workbooks", {})
        .get("产品与工艺_模板.xlsx", {})
        .get("工艺路线工序", [])
    )
    for row in ops:
        if row.get("*工艺路线编码") == "RT-L1-ENG-A1000-V1" and row.get("*工序号") == "40":
            row["工序专业类型"] = "装配专业"


def build_seed() -> dict:
    builder = SeedBuilder(CONFIG["metadata"])
    builder.build_from_config(CONFIG)
    seed = builder.seed

    mark_level1_route(seed)
    rebuild_route_sequences(seed)
    normalize_sequence_relations(seed)
    normalize_storage_factory_org(seed)
    normalize_release_user(seed)
    normalize_poc_security(seed)
    clear_tool_strategy_relations(seed)
    filter_wc_supplier_relations(seed)
    build_orders(seed)
    return seed


def write_note(summary: dict) -> None:
    counts = summary["counts"]
    NOTE_PATH.write_text(
        "\n".join(
            [
                "# 发动机主线业务流程测试数据说明",
                "",
                "## 场景说明",
                "",
                "本套数据按《MOM产品主线业务场景用例-发动机多工厂协同主线》生成，采用“多工厂总装协同蓝图 + 生产部一级工艺”建模。",
                "",
                "已对齐的关键编码示例：",
                "",
                "- 组织：`ORG-PD-001`、`ORG-MC-001`、`ORG-SH-001`、`ORG-BL-001`、`ORG-AS-001`",
                "- 物料：`MAT-ENG-001`、`MAT-CAS-001`、`MAT-SHAFT-001`、`MAT-BLADESET-001`",
                "- 工作中心：`WC-MC-01`、`WC-SH-01`、`WC-BL-01`、`WC-ASM-01`、`WC-QC-ASM-01`",
                "- 工艺路线：`RT-L1-ENG-A1000-V1`、`RT-ASM-ENG-A1000-V1`",
                "- 生产订单：`PO-ENG-A1000-20260603-0001` 及 4 个子生产订单",
                "",
                "## 当前导入包包含",
                "",
                "- 四本 Excel 导入模板对应的数据：系统配置、工厂资源、产品与工艺、生产订单",
                "- 父生产订单 1 张、子生产订单 4 张，所有子生产订单均保持初始未释放状态，释放数量与释放状态由后续业务操作驱动",
                "",
                "## 未包含在当前模板导入包中的前置项",
                "",
                "- 质量方案、检验分类、检查项、检验报告模板",
                "- 工艺文件对象及 `SOP-ASM-A1000-V1.pdf` 的系统内文档关系",
                "- 实际库存批次、序列号、批次生成记录",
                "- 工厂级汇报项配置（`合格 / 报废 / 待定`）",
                "",
                "以上项目不在当前四本标准模板范围内，需要在目标环境中另行配置或通过其他导入入口补齐。",
                "",
                "## 数据规模摘要",
                "",
                f"- 行政组织：{counts['系统配置_模板.xlsx']['行政组织']}",
                f"- 业务组织：{counts['系统配置_模板.xlsx']['业务组织']}",
                f"- 用户：{counts['系统配置_模板.xlsx']['用户']}",
                f"- 工作中心：{counts['工厂资源_模板.xlsx']['工作中心']}",
                f"- 物料：{counts['产品与工艺_模板.xlsx']['物料']}",
                f"- 工艺路线：{counts['产品与工艺_模板.xlsx']['工艺路线']}",
                f"- 生产订单：{counts['生产订单_模板.xlsx']['生产订单']}",
            ]
        ),
        encoding="utf-8-sig",
    )


def main() -> None:
    seed = build_seed()
    summary = summarize_seed(seed)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_PATH.write_text(
        json.dumps(seed, ensure_ascii=False, indent=2),
        encoding="utf-8-sig",
    )
    write_note(summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"已写入种子文件: {ASSET_PATH}")


if __name__ == "__main__":
    main()
