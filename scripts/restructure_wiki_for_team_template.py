from __future__ import annotations

import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
TODAY = date.today().isoformat()
MOVED: list[str] = []
CREATED: list[str] = []

SECTIONS = {
    "01_通用规范": ["组织与岗位职责", "研发流程标准", "管理制度&安全"],
    "02_测试标准&模板": ["测试过程规范", "缺陷管理体系", "可复用模板"],
    "03_业务系统": ["MOM/系统总览", "MOM/模块业务手册", "MOM/接口&数据字典", "MOM/业务常见问题库"],
    "04_技术手册": ["基础环境运维", "数据库专项", "版本与代码管理", "测试工具使用"],
    "05_问题沉淀库": ["日常环境问题", "线上故障复盘", "高频报错手册"],
    "06_专项测试": ["功能测试", "接口测试", "性能测试", "安全测试"],
    "07_新人赋能": ["入职学习路线", "工具安装配置", "快速上手指引", "术语词典"],
}

OLD_TOP_DIRS = [
    "00_规范中心",
    "01_产品知识库",
    "02_业务知识库",
    "03_测试资产库",
    "04_文档模板库",
    "05_流程&工具手册",
    "06_项目归档",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def ensure_dirs() -> None:
    for section, subdirs in SECTIONS.items():
        (WIKI / section).mkdir(parents=True, exist_ok=True)
        for subdir in subdirs:
            (WIKI / section / subdir).mkdir(parents=True, exist_ok=True)
        if section == "03_业务系统":
            for module in ["登录权限模块", "后台管理模块", "核心业务模块", "第三方对接模块", "原型需求"]:
                (WIKI / section / "MOM" / "模块业务手册" / module).mkdir(parents=True, exist_ok=True)


def move_page(source_rel: str, target_rel: str) -> None:
    source = WIKI / source_rel
    target = WIKI / target_rel
    if not source.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if source.read_bytes() == target.read_bytes():
            source.unlink()
        else:
            fallback = target.with_name(f"{target.stem}_旧目录迁移{target.suffix}")
            shutil.move(str(source), str(fallback))
            MOVED.append(f"{rel(source)} -> {rel(fallback)}")
        return
    shutil.move(str(source), str(target))
    MOVED.append(f"{rel(source)} -> {rel(target)}")


def move_explicit_pages() -> None:
    mapping = {
        "00_规范中心/LLM生成指令标准.md": "01_通用规范/管理制度&安全/LLM生成指令标准.md",
        "00_规范中心/产品测试流程规范.md": "01_通用规范/研发流程标准/产品测试流程规范.md",
        "00_规范中心/测试流程规范图谱.md": "01_通用规范/研发流程标准/测试流程规范图谱.md",
        "00_规范中心/文档编写规范.md": "01_通用规范/管理制度&安全/文档编写规范.md",
        "00_规范中心/操作手册编写规范.md": "02_测试标准&模板/可复用模板/操作手册编写规范.md",
        "00_规范中心/测试报告规范.md": "02_测试标准&模板/可复用模板/测试报告规范.md",
        "00_规范中心/测试用例规范.md": "02_测试标准&模板/测试过程规范/测试用例规范.md",
        "00_规范中心/测试用例设计规程.md": "02_测试标准&模板/测试过程规范/测试用例设计规程.md",
        "00_规范中心/测试用例评审规程.md": "02_测试标准&模板/测试过程规范/测试用例评审规程.md",
        "00_规范中心/接口测试用例设计规范.md": "06_专项测试/接口测试/接口测试用例设计规范.md",
        "00_规范中心/产品缺陷管理规程.md": "02_测试标准&模板/缺陷管理体系/产品缺陷管理规程.md",
        "00_规范中心/缺陷分级&提交规范.md": "02_测试标准&模板/缺陷管理体系/缺陷分级&提交规范.md",
        "00_规范中心/规范中心总览.md": "01_通用规范/管理制度&安全/规范中心总览.md",
        "03_测试资产库/测试资产库总览.md": "02_测试标准&模板/测试过程规范/测试资产库总览.md",
        "03_测试资产库/回归测试清单/回归测试清单.md": "02_测试标准&模板/测试过程规范/回归测试清单.md",
        "03_测试资产库/测试用例库/测试用例设计.md": "02_测试标准&模板/测试过程规范/测试用例设计.md",
        "05_流程&工具手册/如何为新需求建立测试分析路径.md": "02_测试标准&模板/测试过程规范/如何为新需求建立测试分析路径.md",
        "05_流程&工具手册/测试策略.md": "02_测试标准&模板/测试过程规范/测试策略.md",
        "05_流程&工具手册/缺陷管理.md": "02_测试标准&模板/缺陷管理体系/缺陷管理.md",
        "05_流程&工具手册/测试全流程指南.md": "01_通用规范/研发流程标准/测试全流程指南.md",
        "05_流程&工具手册/项目协作流程.md": "01_通用规范/研发流程标准/项目协作流程.md",
        "05_流程&工具手册/测试环境使用手册.md": "04_技术手册/基础环境运维/测试环境使用手册.md",
        "05_流程&工具手册/性能测试.md": "06_专项测试/性能测试/性能测试.md",
        "05_流程&工具手册/自动化测试.md": "04_技术手册/测试工具使用/自动化测试.md",
        "05_流程&工具手册/流程与工具手册总览.md": "04_技术手册/测试工具使用/流程与工具手册总览.md",
        "05_流程&工具手册/测试工具使用/JMeter.md": "04_技术手册/测试工具使用/JMeter.md",
        "05_流程&工具手册/测试工具使用/Playwright.md": "04_技术手册/测试工具使用/Playwright.md",
        "05_流程&工具手册/测试工具使用/Pytest.md": "04_技术手册/测试工具使用/Pytest.md",
        "05_流程&工具手册/测试工具使用/UI自动化框架对比.md": "04_技术手册/测试工具使用/UI自动化框架对比.md",
        "06_项目归档/项目归档总览.md": "05_问题沉淀库/线上故障复盘/项目归档总览.md",
    }
    for source, target in mapping.items():
        move_page(source, target)


def move_product_pages() -> None:
    old_root = WIKI / "01_产品知识库"
    if not old_root.exists():
        return
    for source in sorted(old_root.rglob("*.md")):
        parts = source.relative_to(old_root).parts
        if source.stem == "角色权限矩阵":
            target = "03_业务系统/MOM/模块业务手册/登录权限模块/角色权限矩阵.md"
        elif parts[0] == "原型需求":
            target = f"03_业务系统/MOM/模块业务手册/原型需求/{source.name}"
        else:
            target = f"03_业务系统/MOM/系统总览/{source.name}"
        move_page(str(source.relative_to(WIKI)).replace("\\", "/"), target)


def move_business_pages() -> None:
    old_root = WIKI / "02_业务知识库"
    if not old_root.exists():
        return
    for source in sorted(old_root.rglob("*.md")):
        parts = source.relative_to(old_root).parts
        if len(parts) == 1:
            target = f"03_业务系统/MOM/系统总览/{source.name}"
        else:
            target = f"03_业务系统/MOM/模块业务手册/{parts[0]}/{source.name}"
        move_page(str(source.relative_to(WIKI)).replace("\\", "/"), target)


def move_template_pages() -> None:
    old_root = WIKI / "04_文档模板库"
    if not old_root.exists():
        return
    for source in sorted(old_root.rglob("*.md")):
        target = f"02_测试标准&模板/可复用模板/{source.name}"
        move_page(str(source.relative_to(WIKI)).replace("\\", "/"), target)


def remove_old_dirs() -> None:
    for name in OLD_TOP_DIRS:
        target = WIKI / name
        if target.exists():
            shutil.rmtree(target)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    CREATED.append(rel(path))


def frontmatter(title: str, page_type: str, status: str, tags: list[str], summary: str) -> str:
    tag_lines = "\n".join(f"  - {tag}" for tag in tags)
    return f"""---
title: {title}
type: {page_type}
status: {status}
tags:
{tag_lines}
summary: {summary}
source:
  - user_prompt/企业内部LLM-Wiki知识库目录模板
updated: {TODAY}
---"""


def page(title: str, page_type: str, tags: list[str], summary: str, body: str, status: str = "active") -> str:
    return f"{frontmatter(title, page_type, status, tags, summary)}\n\n# {title}\n\n{body.strip()}\n"


def write_overview_pages() -> None:
    pages = {
        "01_通用规范/通用规范总览.md": page("通用规范总览", "standard", ["testing", "team", "process"], "团队组织、研发流程、管理制度与安全要求的统一入口。", """
## 目录结构

- [[组织与岗位职责总览]]：测试团队组织架构、岗位职责、交付物与跨部门协作
- [[研发流程标准总览]]：需求、开发、测试、上线、紧急变更与补丁发布流程
- [[管理制度与安全总览]]：文档管理、账号权限、数据保密、日志与敏感信息脱敏
- [[LLM入库规则]]：保证企业内部 LLM 问答检索精准的入库约束

## 适用场景

- 新人理解团队工作方式
- 测试活动进入前确认职责与流程
- 内部知识库内容治理与安全审查
"""),
        "01_通用规范/组织与岗位职责/组织与岗位职责总览.md": page("组织与岗位职责总览", "standard", ["testing", "team"], "沉淀测试团队组织、岗位职责、交付物和跨部门协作规范。", """
## 应沉淀内容

- 测试团队组织架构
- 测试工程师岗位职责与交付物清单
- 跨部门协作对接规范

## 关联页面

- [[通用规范总览]]
- [[项目协作流程]]
""", "seed"),
        "01_通用规范/研发流程标准/研发流程标准总览.md": page("研发流程标准总览", "standard", ["testing", "process"], "覆盖需求、开发、测试、上线以及紧急变更的研发流程标准入口。", """
## 应沉淀内容

- 完整迭代流程：需求 → 开发 → 测试 → 上线
- 需求评审、设计评审准入标准
- 测试准入、测试准出、上线审批规范
- 紧急变更、热更新、补丁发布流程

## 已有关联

- [[产品测试流程规范]]
- [[测试全流程指南]]
- [[测试流程规范图谱]]
- [[项目协作流程]]
"""),
        "01_通用规范/管理制度&安全/管理制度与安全总览.md": page("管理制度与安全总览", "standard", ["testing", "security", "governance"], "文档管理、账号权限、数据安全和敏感信息脱敏的统一入口。", """
## 应沉淀内容

- 文档管理、版本归档规范
- 账号权限申请与变更流程
- 数据保密、生产数据使用规范
- 日志、敏感信息脱敏要求

## 关联页面

- [[文档编写规范]]
- [[LLM生成指令标准]]
- [[LLM入库规则]]
"""),
        "01_通用规范/管理制度&安全/LLM入库规则.md": page("LLM入库规则", "standard", ["testing", "llm", "knowledge-base"], "规范企业内部 LLM-Wiki 文档入库格式、安全边界和检索友好写法。", """
## 文档统一格式

- 标题
- 简介
- 正文
- 关键字
- 更新日期
- 责任人

## 安全要求

- 全量文档去除密码、真实 IP、生产敏感数据
- 日志、截图、接口样例需完成敏感信息脱敏
- 涉及生产数据时仅保留必要的业务含义和字段结构

## 检索友好要求

- 单文档聚焦一个主题，避免大杂烩
- 高频问答、操作步骤尽量条目化、步骤化
- 标题和小标题使用业务可搜索关键词
- 重要页面通过 `[[wikilinks]]` 连接上下游知识

## 目录式查询规范

- 查询必须从 `wiki/index.md` 出发，先定位对应业务域、知识域或模块菜单
- 命中菜单后，优先进入对应总览页、资料地图、模块手册或专题入口，再下钻到具体页面
- 查询模块、功能、菜单、界面、接口、字段、枚举、状态等内容时，应先在对应目录分支内查找，不直接跨目录散搜
- 仅当当前目录分支证据不足时，才扩展到关联页面、同级总览页或 `wiki/` 全文检索
- 若 `wiki/index.md`、总览页或资料地图缺少目标入口，应记录导航缺口，并补充索引页、总览页或交叉链接
- 回答时尽量给出“`wiki/index.md` → 总览页 → 主题页 → 具体页面”的查询路径，便于复核和复用

## 问答检索策略

- 用户直接用自然语言提问时，默认只从 `wiki/` 结构化知识层检索并整合答案
- 检索入口优先级：先读 `wiki/index.md` 全局导航，再进入相关总览页和主题页，最后按关键词全文检索 `wiki/`
- 对模块、菜单类问题，应先从 `wiki/index.md` 找到对应菜单，再进入对应总览页、资料地图或界面说明页查询
- 回答优先采用 `status: active`、有 `summary`、`tags`、`source` 和清晰标题层级的知识页
- 当多个页面存在上下游关系时，沿 `[[wikilinks]]` 扩展到关联页面，避免只基于单页片段作答
- `raw/` 仅作为原始资料备查层；只有当用户明确要求追溯原文、结构化页面依据不足，或知识页 `source` 指向原始资料时才检索 `raw/`
- 根目录工程文件、脚本、临时文件不作为业务问答默认检索范围，除非问题涉及知识库维护、脚本、目录规则或工程配置
- 若 `wiki/` 内没有充分依据，应明确说明“未在知识库中找到充分依据”，并列出已检索的入口或建议补充的资料
- 若检索到冲突信息，应保留冲突来源、更新时间和判断依据，不静默合并为单一结论
"""),
        "02_测试标准&模板/测试标准与模板总览.md": page("测试标准与模板总览", "standard", ["testing", "standard", "template"], "测试过程规范、缺陷管理体系和可复用交付模板的统一入口。", """
## 目录结构

- [[测试过程规范总览]]：用例、评审、范围评估、回归、冒烟、集成、验收规范
- [[缺陷管理体系总览]]：缺陷流转、分级分类、拒绝延期、遗留缺陷与高频缺陷
- [[可复用模板总览]]：测试计划、方案、用例、数据、报告、操作手册等模板

## 关联页面

- [[测试策略]]
- [[测试用例设计]]
- [[缺陷管理]]
"""),
        "02_测试标准&模板/测试过程规范/测试过程规范总览.md": page("测试过程规范总览", "standard", ["testing", "case-design", "process"], "用例编写、评审、范围评估、回归策略与各类测试准则的入口。", """
## 应沉淀内容

- 用例编写规范、用例评审标准
- 测试范围评估、回归测试策略
- 冒烟测试、集成测试、验收测试规范

## 已有关联

- [[测试用例规范]]
- [[测试用例设计规程]]
- [[测试用例评审规程]]
- [[回归测试清单]]
- [[测试策略]]
"""),
        "02_测试标准&模板/缺陷管理体系/缺陷管理体系总览.md": page("缺陷管理体系总览", "standard", ["testing", "defect"], "缺陷状态流转、缺陷分级分类、遗留缺陷和高频缺陷治理入口。", """
## 应沉淀内容

- 缺陷状态流转、缺陷分级与分类标准
- 缺陷拒绝、延期、遗留缺陷管理规则
- 高频缺陷归类与规避准则

## 已有关联

- [[产品缺陷管理规程]]
- [[缺陷分级&提交规范]]
- [[缺陷管理]]
"""),
        "02_测试标准&模板/可复用模板/可复用模板总览.md": page("可复用模板总览", "template", ["testing", "template"], "测试计划、方案、用例、数据清单、报告和手册模板入口。", """
## 模板类型

- 测试计划、测试方案
- 测试用例、测试数据清单
- 缺陷单、测试日报、周报、月报
- 版本测试报告、上线验收报告
- 操作手册、维护手册、用户手册

## 已有关联

- [[测试用例模板]]
- [[完整版本测试报告模板]]
- [[送测测试报告模板]]
- [[上线验收报告模板]]
- [[功能操作手册模板]]
"""),
        "03_业务系统/业务系统总览.md": page("业务系统总览", "business", ["testing", "business-system", "mom"], "按 MOM、MES、ERP、WMS、中间件平台等系统沉淀业务知识。", """
## 当前系统

- [[MOM系统总览]]：MOM 产品架构、功能地图、需求拆解和模块业务手册

## 推荐拆分方式

- 系统总览：系统架构图、上下游对接关系、核心业务场景、环境划分
- 模块业务手册：菜单功能、字段释义、业务规则、特殊场景、数据流转
- 接口&数据字典：接口清单、入参出参、数据库表结构、关键字段、同步任务
- 业务常见问题库：FAQ、历史功能异常、业务规则争议案例
"""),
        "03_业务系统/MOM/MOM系统总览.md": page("MOM系统总览", "business", ["testing", "mom", "business-system"], "MOM 系统知识入口，连接系统总览、模块业务手册、接口数据字典与 FAQ。", """
## 子目录

- [[MOM需求分析总览]]：基于原始需求文档形成的需求拆解总入口
- [[产品功能地图]]：MOM 产品模块、能力和上下游关系地图
- [[模块业务手册总览]]：按模块沉淀业务规则、字段、流程和特殊场景
- [[接口与数据字典总览]]：接口、数据库、同步任务和消息队列说明
- [[业务常见问题库总览]]：FAQ、历史异常和规则争议沉淀
"""),
        "03_业务系统/MOM/模块业务手册/模块业务手册总览.md": page("模块业务手册总览", "business", ["testing", "mom", "module"], "按 MOM 模块聚合菜单功能、字段释义、业务规则、流程和测试关注点。", """
## 模块入口

- [[登录权限需求导航]]
- [[后台管理需求导航]]
- [[核心业务需求导航]]
- [[智能能力需求导航]]
- [[原型评审关注点]]

## 维护建议

- 一个页面聚焦一个模块或一个业务主题
- 保留来源文档路径，便于追溯
- 用 `[[wikilinks]]` 连接上下游模块、测试策略和用例资产
"""),
        "03_业务系统/MOM/接口&数据字典/接口与数据字典总览.md": page("接口与数据字典总览", "business", ["testing", "interface", "data-dictionary"], "沉淀 MOM 核心接口、入参出参、数据表、关键字段、同步任务和消息队列说明。", """
## 应沉淀内容

- 核心接口清单、入参出参说明
- 数据库表结构、业务关键字段说明
- 定时任务、同步任务、消息队列说明

## 维护建议

- 接口变更需关联对应需求拆解页
- 数据字典需说明字段业务含义、取值范围和上下游影响
""", "seed"),
        "03_业务系统/MOM/业务常见问题库/业务常见问题库总览.md": page("业务常见问题库总览", "query", ["testing", "faq", "mom"], "沉淀 MOM 业务高频疑问、历史功能异常和业务规则争议案例。", """
## 应沉淀内容

- 业务高频疑问 FAQ
- 历史功能异常
- 业务规则争议案例

## 维护建议

- 问题页应包含现象、原因、处理方案、关联需求和更新时间
""", "seed"),
        "04_技术手册/技术手册总览.md": page("技术手册总览", "manual", ["testing", "technical-manual"], "环境运维、数据库、版本代码管理和测试工具使用的统一入口。", """
## 目录结构

- [[基础环境运维总览]]：Linux、服务、端口、部署、重置、数据初始化
- [[数据库专项总览]]：达梦、MySQL、SQL、数据清理、权限、备份恢复
- [[版本与代码管理总览]]：Git 分支、TortoiseGit、提交合并、冲突解决、Tag
- [[测试工具使用总览]]：缺陷工具、接口测试、抓包、日志分析、监控平台
"""),
        "04_技术手册/基础环境运维/基础环境运维总览.md": page("基础环境运维总览", "manual", ["testing", "ops"], "Linux 排查、服务启停、端口排查、测试环境部署与数据初始化入口。", """
## 应沉淀内容

- Linux 常用排查命令、日志查看指南
- 服务启停、进程查看、端口排查
- 测试环境部署、重置、数据初始化操作

## 已有关联

- [[测试环境使用手册]]
""", "seed"),
        "04_技术手册/数据库专项/数据库专项总览.md": page("数据库专项总览", "manual", ["testing", "database"], "达梦、MySQL 等数据库查询、比对、清理、权限、备份恢复和报错处理入口。", """
## 应沉淀内容

- 常用查询 SQL、批量操作语句
- 数据比对、脏数据清理脚本
- 数据库权限、备份与恢复操作
- 数据库常见报错处理
""", "seed"),
        "04_技术手册/版本与代码管理/版本与代码管理总览.md": page("版本与代码管理总览", "manual", ["testing", "git", "release"], "Git 分支策略、TortoiseGit 操作、提交合并、冲突解决和 Tag 规范入口。", """
## 应沉淀内容

- Git 分支管理策略：开发、测试、发布分支
- TortoiseGit 可视化操作指南
- 拉取、提交、合并、冲突解决标准步骤
- 代码合并、版本打 Tag 规范
""", "seed"),
        "04_技术手册/测试工具使用/测试工具使用总览.md": page("测试工具使用总览", "manual", ["testing", "tools"], "缺陷管理、接口测试、抓包、日志分析、监控平台和自动化工具入口。", """
## 应沉淀内容

- 缺陷管理工具：禅道、Jira
- 接口测试工具、抓包工具使用
- 日志分析、监控平台操作指南

## 已有关联

- [[JMeter]]
- [[Playwright]]
- [[Pytest]]
- [[UI自动化框架对比]]
- [[自动化测试]]
"""),
        "05_问题沉淀库/问题沉淀库总览.md": page("问题沉淀库总览", "archive", ["testing", "incident", "troubleshooting"], "日常环境问题、线上故障复盘和高频报错手册入口。", """
## 目录结构

- [[日常环境问题总览]]：环境无法访问、服务宕机、连接超时、账号权限、缓存、配置
- [[线上故障复盘总览]]：线上问题记录、根因分析、临时方案、永久优化、改进项跟踪
- [[高频报错手册总览]]：后端日志、数据库异常、接口异常、测试过程踩坑
"""),
        "05_问题沉淀库/日常环境问题/日常环境问题总览.md": page("日常环境问题总览", "archive", ["testing", "environment", "troubleshooting"], "沉淀测试环境无法访问、服务宕机、连接超时、权限、缓存和配置问题。", """
## 应沉淀内容

- 环境无法访问、服务宕机、连接超时
- 账号权限不足、缓存异常、配置错误

## 记录模板

- 问题现象
- 排查步骤
- 根因判断
- 处理方案
- 关联环境与更新时间
""", "seed"),
        "05_问题沉淀库/线上故障复盘/线上故障复盘总览.md": page("线上故障复盘总览", "archive", ["testing", "incident", "postmortem"], "沉淀历史线上问题、根因分析、应急方案、永久优化方案和改进项跟踪。", """
## 应沉淀内容

- 历史线上问题记录与根因分析
- 临时应急方案与永久优化方案
- 故障复盘报告、改进项跟踪

## 已有关联

- [[项目归档总览]]
""", "seed"),
        "05_问题沉淀库/高频报错手册/高频报错手册总览.md": page("高频报错手册总览", "manual", ["testing", "error", "troubleshooting"], "沉淀后端日志关键字、数据库异常、接口请求异常和测试过程高频踩坑。", """
## 应沉淀内容

- 后端日志关键字报错解读
- 数据库异常合集
- 接口请求异常合集
- 测试过程高频踩坑清单
""", "seed"),
        "06_专项测试/专项测试总览.md": page("专项测试总览", "asset", ["testing", "special-test"], "功能、接口、性能、安全等专项测试资料入口。", """
## 目录结构

- [[功能测试检查项]]：功能测试、兼容性测试检查项
- [[接口测试要点]]：接口测试、边界值、异常场景测试要点
- [[性能测试总览]]：性能测试基础指标、压测场景和简单排查
- [[安全测试关注点]]：安全测试、数据权限、越权测试关注点
"""),
        "06_专项测试/功能测试/功能测试检查项.md": page("功能测试检查项", "asset", ["testing", "functional-test"], "功能测试与兼容性测试检查项模板。", """
## 检查项

- 主流程是否可完成
- 必填、唯一、格式、长度、边界校验是否正确
- 新增、编辑、删除、查询、导入、导出是否覆盖
- 权限、状态、异常、并发、兼容性是否覆盖
""", "seed"),
        "06_专项测试/接口测试/接口测试要点.md": page("接口测试要点", "asset", ["testing", "api-test"], "接口测试、边界值和异常场景测试要点。", """
## 检查项

- 入参必填、类型、枚举、长度、边界值
- 鉴权、越权、数据范围、重复提交
- 成功响应、失败响应、错误码和错误信息
- 接口幂等、事务一致性、上下游联动

## 关联页面

- [[接口测试用例设计规范]]
""", "seed"),
        "06_专项测试/性能测试/性能测试总览.md": page("性能测试总览", "asset", ["testing", "performance"], "性能测试基础指标、压测场景和简单排查入口。", """
## 应沉淀内容

- 基础指标：响应时间、吞吐量、并发数、错误率、资源使用率
- 压测场景：登录、查询、保存、导入、报表、批处理
- 简单排查：CPU、内存、数据库慢 SQL、接口超时、队列堆积

## 已有关联

- [[性能测试]]
- [[JMeter]]
"""),
        "06_专项测试/安全测试/安全测试关注点.md": page("安全测试关注点", "asset", ["testing", "security-test"], "安全测试、数据权限和越权测试关注点。", """
## 检查项

- 未登录访问、会话过期、接口直连
- 角色权限、数据权限、组织范围越权
- 敏感字段展示、导出、日志落盘
- SQL 注入、XSS、文件上传、弱口令风险
""", "seed"),
        "07_新人赋能/新人赋能总览.md": page("新人赋能总览", "manual", ["testing", "onboarding"], "新员工学习路线、工具配置、账号申请、快速上手和术语词典入口。", """
## 目录结构

- [[新员工入职学习路线]]：必看文档、学习顺序和阶段目标
- [[必配工具安装配置]]：必配工具安装包与配置教程
- [[环境账号申请与快速上手]]：环境账号申请、快速上手操作指引
- [[常用术语词典]]：常用缩写、业务术语、技术名词解释
"""),
        "07_新人赋能/入职学习路线/新员工入职学习路线.md": page("新员工入职学习路线", "manual", ["testing", "onboarding"], "测试新人入职学习路线与必看文档入口。", """
## 建议路径

1. 阅读 [[通用规范总览]]，理解团队职责、流程和安全要求
2. 阅读 [[测试标准与模板总览]]，掌握测试交付规范
3. 阅读 [[MOM系统总览]]，理解业务系统和模块关系
4. 阅读 [[技术手册总览]]，完成环境、工具、数据库基础上手
5. 阅读 [[问题沉淀库总览]]，学习常见问题排查方式
""", "seed"),
        "07_新人赋能/工具安装配置/必配工具安装配置.md": page("必配工具安装配置", "manual", ["testing", "onboarding", "tools"], "新人必配工具安装包、配置教程和检查项。", """
## 应沉淀内容

- 浏览器、办公工具、Markdown/Obsidian 工具
- 缺陷管理工具、接口测试工具、抓包工具
- 数据库客户端、Git/TortoiseGit、远程连接工具
- 工具安装后的验证步骤
""", "seed"),
        "07_新人赋能/快速上手指引/环境账号申请与快速上手.md": page("环境账号申请与快速上手", "manual", ["testing", "onboarding", "environment"], "环境账号申请、权限确认和快速上手操作指引。", """
## 应沉淀内容

- 环境访问地址与用途说明
- 账号权限申请流程
- 测试数据初始化方式
- 常用模块快速操作路径
""", "seed"),
        "07_新人赋能/术语词典/常用术语词典.md": page("常用术语词典", "concept", ["testing", "glossary"], "测试、MOM/MES/ERP、制造业务和技术常用术语解释。", """
## 术语类型

- 常用缩写
- 业务术语
- 技术名词
- 系统与模块简称

## 维护建议

- 每个术语包含中文名、英文名、解释、适用场景和关联页面
""", "seed"),
    }
    for relative_path, content in pages.items():
        write_text(WIKI / relative_path, content)


def write_schema() -> None:
    content = f"""# Wiki Schema

## Domain

本知识库用于沉淀测试工程师在团队规范、测试标准、业务系统、技术工具、问题排查、专项测试和新人赋能中的长期知识，适配软件测试团队、制造业 IT、MOM/MES/ERP 系统、私有化 LLM 问答检索、新人赋能和问题自查。

## Architecture

知识库采用“原始资料 + 结构化知识 + 导航/日志”三层组织：

- `raw/`：原始资料层，保存测试日常工作中的输入材料
- `raw/需求文档/`：需求说明、用户故事、变更单、需求评审材料
- `raw/项目文档/`：项目计划、排期、提测单、版本说明、项目沟通材料
- `raw/产品资料/`：产品介绍、原型图、功能说明、产品方案资料
- `raw/接口资料/`：接口文档、字段说明、对接说明、接口示例
- `raw/测试资料/`：历史测试用例、测试报告、回归清单、缺陷导出资料
- `raw/会议纪要/`：需求评审、问题复盘、项目会议、访谈纪要
- `raw/截图附件/`：截图、流程图、原型导出图、现场问题图片等附件
- `wiki/`：结构化知识层，按企业内部测试知识用途组织目录
- `wiki/index.md` / `wiki/log.md`：导航与维护层，分别负责全局入口和操作留痕

## Directory Rules

结构化知识统一存放在 `wiki/` 下，并采用带序号的目录保证导航顺序：

- `wiki/01_通用规范/`：组织与岗位职责、研发流程标准、管理制度与安全、LLM 入库规则
- `wiki/02_测试标准&模板/`：测试过程规范、缺陷管理体系、全套可复用模板
- `wiki/03_业务系统/`：按 MOM/MES/ERP/WMS/中间件平台等系统沉淀业务知识
- `wiki/03_业务系统/MOM/产品资料库/`：沉淀 `raw/产品资料/km-mom-docs/` 的 IPD 全流程产品资料拆解页
- `wiki/04_技术手册/`：基础环境运维、数据库专项、版本与代码管理、测试工具使用
- `wiki/05_问题沉淀库/`：日常环境问题、线上故障复盘、高频报错手册
- `wiki/06_专项测试/`：功能测试、接口测试、性能测试、安全测试等专项资料
- `wiki/07_新人赋能/`：入职学习路线、工具安装配置、快速上手指引、术语词典

## Page Types

页面 `type` 按知识形态组织，可使用：

- `standard`
- `product`
- `business`
- `asset`
- `template`
- `manual`
- `archive`
- `concept`
- `entity`
- `comparison`
- `query`

## Frontmatter

所有知识页建议包含以下字段：

```yaml
---
title: 页面标题
type: standard | product | business | asset | template | manual | archive | concept | entity | comparison | query
status: seed | active | review | archived
tags:
  - testing
summary: 一句话摘要
source:
  - raw/需求文档/xxx.md
updated: {TODAY}
---
```

## Placement Rules

- 属于团队组织、岗位职责、协作方式、研发流程、管理制度、安全要求、LLM 入库规则：放 `01_通用规范`
- 属于用例、评审、测试范围、回归、缺陷、测试报告、交付模板：放 `02_测试标准&模板`
- 属于 MOM/MES/ERP/WMS 等业务系统、模块业务手册、业务规则、接口数据字典、业务 FAQ：放 `03_业务系统`
- 属于 Linux、服务、数据库、Git、部署、抓包、监控、测试工具：放 `04_技术手册`
- 属于环境问题、线上故障、根因分析、应急方案、高频报错、踩坑清单：放 `05_问题沉淀库`
- 属于功能、接口、性能、安全、兼容性等专项测试检查项和测试要点：放 `06_专项测试`
- 属于新人学习路线、工具安装、账号申请、快速上手、术语解释：放 `07_新人赋能`

## LLM Ingestion Rules

- 文档统一格式：标题、简介、正文、关键字、更新日期、责任人
- 全量文档去除密码、真实 IP、生产敏感数据
- 单文档聚焦一个主题，不要大杂烩，便于分段向量化
- 高频问答、操作步骤尽量条目化、步骤化，提升大模型问答命中率
- 优先使用 `[[wikilinks]]` 建立跨目录链接
- 原始资料只放在 `raw/`，不直接在结构化知识目录中堆放原文

## Wiki Completion Criteria

原始文档转 Wiki 文档补全完成后，应满足以下验收要求：

- 任意一个 `raw/` 文件，都能在 `wiki/` 中找到对应的结构化页面、总览页或索引入口
- 任意一个 Wiki 结论，都能通过页面 `source`、正文引用或关联页面追溯到原始文件
- 查询表名、字段、枚举、接口、业务状态时，应优先在 `wiki/` 直接获得结构化答案，不需要回到 `raw/` 二次翻找
- 查询某个需求时，应能看到对应的业务规则、验收标准和测试点，必要时关联上下游需求与变更信息
- 查询某个模块时，应能看到相关需求、接口、数据模型、状态流转和测试关注点
- `wiki/index.md` 应能导航到所有核心知识入口，避免关键主题成为孤岛页面
- `wiki/log.md` 应记录每次批量入库、批量补全和关键结构调整动作，确保维护过程可追踪

## Query/Retrieval Policy

- 用户直接用自然语言提问时，默认只从 `wiki/` 结构化知识层检索并整合答案
- 查询必须遵循“`wiki/index.md` → 对应菜单/总览页 → 主题页/界面页 → 结论页”的目录式路径，不应直接跳到零散页面作答
- 对模块、功能、菜单、界面、接口、字段、枚举、状态等问题，应先在命中的目录分支内检索；只有当前分支依据不足时，才扩展到关联页面或 `wiki/` 全文检索
- 检索入口优先级：先读 `wiki/index.md` 全局导航，再进入相关总览页和主题页，最后按关键词全文检索 `wiki/`
- 回答优先采用 `status: active`、有 `summary`、`tags`、`source` 和清晰标题层级的知识页
- 当多个页面存在上下游关系时，沿 `[[wikilinks]]` 扩展到关联页面，避免只基于单页片段作答
- `raw/` 仅作为原始资料备查层；只有当用户明确要求追溯原文、结构化页面依据不足，或知识页 `source` 指向原始资料时才检索 `raw/`
- 根目录工程文件、脚本、临时文件不作为业务问答默认检索范围，除非问题涉及知识库维护、脚本、目录规则或工程配置
- 若 `wiki/index.md`、总览页或资料地图缺少目标入口，应先记录导航缺口，并补充索引页、总览页或交叉链接
- 若 `wiki/` 内没有充分依据，应明确说明“未在知识库中找到充分依据”，并列出已检索的入口或建议补充的资料
- 若检索到冲突信息，应保留冲突来源、更新时间和判断依据，不静默合并为单一结论

## Update Policy

- 新增、修改、删除 `wiki/` 内容：必须执行 `python scripts/sync_wiki_meta.py`，同步刷新 `wiki/index.md` 与 `wiki/log.md`
- 新增关键内容：同步检查 `wiki/index.md` 和 `wiki/log.md` 是否完整反映变更
- 新增目录或标签：先更新 `SCHEMA.md`
- 批量整理资料：先进入 `raw/`，再提炼到结构化知识目录
- 同一主题有冲突：保留冲突来源和判断，不静默覆盖
- 每月至少回顾一次 `review` 状态页面
"""
    write_text(ROOT / "SCHEMA.md", content)


def write_readme() -> None:
    content = """# 测试工程师 LLM WIKI

这是一个面向测试工程师的本地知识库，采用 Markdown + YAML frontmatter + `[[wikilinks]]` 组织长期积累的测试知识，适配企业内部私有化 LLM 问答检索、新人赋能和问题自查。

## 目标

- 长期积累：沉淀团队规范、测试标准、业务系统、技术工具、问题复盘和专项测试资料
- 可交叉链接：通过 `[[页面名]]` 建立规范、模板、系统、工具、问题和新人学习之间的关系
- 可查询：通过全局导航 `wiki/index.md`、目录结构、标签和全文搜索快速定位内容
- 可持续更新：通过 `wiki/log.md` 记录结构调整、内容新增与维护历史

## 当前知识库结构

- `SCHEMA.md`：知识库约定、目录规则、页面规范和维护原则
- `wiki/index.md`：全局导航首页、快速入口
- `wiki/log.md`：操作日志与结构调整记录
- `raw/`：原始资料，不直接改写
- `wiki/01_通用规范/`：组织与岗位职责、研发流程标准、管理制度与安全、LLM 入库规则
- `wiki/02_测试标准&模板/`：测试过程规范、缺陷管理体系、全套可复用模板
- `wiki/03_业务系统/`：MOM/MES/ERP/WMS/中间件等业务系统知识库
- `wiki/03_业务系统/MOM/产品资料库/`：`km-mom-docs` 产品资料拆解页、阶段地图和附件清单
- `wiki/04_技术手册/`：基础环境运维、数据库专项、版本与代码管理、测试工具使用
- `wiki/05_问题沉淀库/`：日常环境问题、线上故障复盘、高频报错手册
- `wiki/06_专项测试/`：功能、接口、性能、安全等专项测试资料
- `wiki/07_新人赋能/`：入职学习路线、工具安装配置、快速上手指引、术语词典

## 元数据同步

- 执行命令：`python scripts/sync_wiki_meta.py`
- 脚本会扫描 `wiki/` 目录，自动刷新 `wiki/index.md`
- 脚本会根据 `wiki/` 页面新增、修改、删除情况自动写入 `wiki/log.md`
- 每次新增、修改、删除 `wiki/` 内容后，都必须执行一次该脚本
- 执行后应检查 `wiki/index.md` 与 `wiki/log.md` 是否已同步更新

## Wiki 补全完成标准

- 任意一个 `raw/` 文件，都能在 `wiki/` 中找到对应的结构化页面、总览页或索引入口
- 任意一个 Wiki 结论，都能通过页面 `source`、正文引用或关联页面追溯到原始文件
- 查询表名、字段、枚举、接口、业务状态时，应优先在 `wiki/` 直接获得结构化答案，不需要回到 `raw/` 二次翻找
- 查询某个需求时，应能看到对应的业务规则、验收标准和测试点，必要时关联上下游需求与变更信息
- 查询某个模块时，应能看到相关需求、接口、数据模型、状态流转和测试关注点
- `wiki/index.md` 应能导航到所有核心知识入口，避免关键主题成为孤岛页面
- `wiki/log.md` 应记录每次批量入库、批量补全和关键结构调整动作，确保维护过程可追踪

## 首批入口

- `[[通用规范总览]]`
- `[[测试标准与模板总览]]`
- `[[业务系统总览]]`
- `[[技术手册总览]]`
- `[[问题沉淀库总览]]`
- `[[专项测试总览]]`
- `[[新人赋能总览]]`

## LLM 问答检索策略

- 自然语言提问默认从 `wiki/` 结构化知识层检索并整合答案
- 查询先从 `wiki/index.md` 定位业务域或模块菜单，再进入对应总览页、资料地图、主题页或界面页
- 查询模块、功能、菜单、界面、接口、字段、枚举、状态时，优先在该目录分支内下钻，不直接跨目录散搜
- 优先使用 `wiki/index.md`、总览页、主题页、`[[wikilinks]]` 和全文搜索定位内容
- 回答优先采用 `status: active`、带 `summary`、`tags`、`source` 且标题层级清晰的知识页
- 当多个页面存在上下游关系时，应沿 `[[wikilinks]]` 扩展到关联页面，避免只基于单页片段作答
- `raw/` 仅在追溯原文、依据不足或知识页 `source` 指向原始资料时作为备查层
- 根目录工程文件、脚本、临时文件不作为业务问答默认检索范围，除非问题涉及知识库维护、脚本、目录规则或工程配置
- 若 `wiki/index.md`、总览页或资料地图缺少目标入口，应先补导航，再沉淀答案
- 若 `wiki/` 没有充分依据，回答时应明确说明，并给出已检索入口或建议补充资料
- 若检索到冲突信息，应保留冲突来源、更新时间和判断依据，不静默合并为单一结论

## LLM 入库规则

- 文档统一格式：标题、简介、正文、关键字、更新日期、责任人
- 全量文档去除密码、真实 IP、生产敏感数据
- 单文档聚焦一个主题，避免大杂烩，便于分段向量化
- 高频问答和操作步骤尽量条目化、步骤化
- 优先使用 `[[wikilinks]]` 建立跨目录链接
- 原始资料只放在 `raw/`，不直接在结构化知识目录中堆放原文
"""
    write_text(ROOT / "README.md", content)


def update_sync_script() -> None:
    path = ROOT / "scripts" / "sync_wiki_meta.py"
    text = path.read_text(encoding="utf-8")
    section_block = '''SECTION_DESCRIPTIONS = OrderedDict(
    [
        ("01_通用规范", "组织与岗位职责、研发流程标准、管理制度与安全"),
        ("02_测试标准&模板", "测试过程规范、缺陷管理体系和可复用模板"),
        ("03_业务系统", "MOM/MES/ERP/WMS 等业务系统、模块手册、接口与数据字典"),
        ("04_技术手册", "环境运维、数据库、版本代码管理和测试工具"),
        ("05_问题沉淀库", "环境问题、线上故障复盘、高频报错和踩坑清单"),
        ("06_专项测试", "功能、接口、性能、安全等专项测试资料"),
        ("07_新人赋能", "入职学习路线、工具配置、快速上手和术语词典"),
    ]
)'''
    important_block = '''IMPORTANT_PAGES = [
    "通用规范总览",
    "测试标准与模板总览",
    "业务系统总览",
    "MOM系统总览",
    "MOM需求分析总览",
    "技术手册总览",
    "问题沉淀库总览",
    "专项测试总览",
    "新人赋能总览",
    "LLM入库规则",
    "测试策略",
    "测试用例设计",
    "缺陷管理",
    "性能测试",
    "Playwright",
    "Pytest",
    "JMeter",
]'''
    text = re.sub(r'SECTION_DESCRIPTIONS = OrderedDict\(\n    \[\n.*?\n    \]\n\)', section_block, text, flags=re.S)
    text = re.sub(r'IMPORTANT_PAGES = \[\n.*?\n\]', important_block, text, flags=re.S)
    path.write_text(text, encoding="utf-8")


def update_requirement_generator() -> None:
    path = ROOT / "scripts" / "build_requirements_wiki.py"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = text.replace("WIKI / '01_产品知识库' / '功能地图'", "WIKI / '03_业务系统' / 'MOM' / '系统总览'")
    text = text.replace("WIKI / '01_产品知识库' / '版本特性'", "WIKI / '03_业务系统' / 'MOM' / '系统总览'")
    text = text.replace("WIKI / '02_业务知识库' / '登录权限模块'", "WIKI / '03_业务系统' / 'MOM' / '模块业务手册' / '登录权限模块'")
    text = text.replace("WIKI / '02_业务知识库' / '后台管理模块'", "WIKI / '03_业务系统' / 'MOM' / '模块业务手册' / '后台管理模块'")
    text = text.replace("WIKI / '02_业务知识库' / '核心业务模块'", "WIKI / '03_业务系统' / 'MOM' / '模块业务手册' / '核心业务模块'")
    text = text.replace("WIKI / '02_业务知识库' / '第三方对接模块'", "WIKI / '03_业务系统' / 'MOM' / '模块业务手册' / '第三方对接模块'")
    text = text.replace("item['path'] = WIKI / '02_业务知识库' / item['domain'] / f\"{item['title']}.md\"", "item['path'] = WIKI / '03_业务系统' / 'MOM' / '模块业务手册' / item['domain'] / f\"{item['title']}.md\"")
    path.write_text(text, encoding="utf-8")


def write_log_entry() -> None:
    path = WIKI / "log.md"
    old = path.read_text(encoding="utf-8") if path.exists() else "# Wiki Log\n"
    title = f"## {TODAY} update | 按企业内部 LLM-Wiki 模板调整目录"
    if title in old:
        return
    lines = [
        "# Wiki Log",
        "",
        title,
        "",
        "- 将结构化知识目录调整为 `01_通用规范` 至 `07_新人赋能` 七大类",
        "- 迁移既有规范、模板、MOM 需求拆解、工具手册、专项测试与归档页面到新目录",
        "- 新增团队通用规范、测试标准、业务系统、技术手册、问题沉淀、专项测试和新人赋能骨架页",
        "- 同步更新 `SCHEMA.md`、`README.md`、`scripts/sync_wiki_meta.py` 与需求拆解生成脚本",
    ]
    body = old.strip()
    if body.startswith("# Wiki Log"):
        body = body[len("# Wiki Log"):].strip()
    if body:
        lines.extend(["", body])
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    ensure_dirs()
    move_explicit_pages()
    move_product_pages()
    move_business_pages()
    move_template_pages()
    remove_old_dirs()
    ensure_dirs()
    write_overview_pages()
    write_schema()
    write_readme()
    update_sync_script()
    update_requirement_generator()
    write_log_entry()
    print(f"moved_pages={len(MOVED)}")
    print(f"written_pages={len(CREATED)}")


if __name__ == "__main__":
    main()




