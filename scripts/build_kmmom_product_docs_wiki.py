from __future__ import annotations

import re
import shutil
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path.cwd()
SOURCE_ROOT = ROOT / "raw" / "产品资料" / "km-mom-docs"
WIKI = ROOT / "wiki"
OUTPUT_ROOT = WIKI / "03_业务系统" / "MOM" / "产品资料库"
TODAY = date.today().isoformat()

STAGES = {
    "01-concept": {
        "name": "概念阶段",
        "map_title": "KMMOM概念阶段资料地图",
        "description": "战略规划、产品路标、Charter 与 PCR 决策输入。",
        "anchor": ["MOM系统总览", "产品功能地图", "业务系统总览"],
        "type": "product",
    },
    "02-plan": {
        "name": "计划阶段",
        "map_title": "KMMOM计划阶段资料地图",
        "description": "版本规划、需求管理、架构设计与 PDCP 计划决策输入。",
        "anchor": ["MOM需求分析总览", "模块业务手册总览", "产品功能地图"],
        "type": "business",
    },
    "03-development": {
        "name": "开发阶段",
        "map_title": "KMMOM开发阶段资料地图",
        "description": "数据模型、模块设计、技术设计和 WebAPI 资料。",
        "anchor": ["模块业务手册总览", "接口与数据字典总览", "技术手册总览"],
        "type": "business",
    },
    "04-verification": {
        "name": "验证阶段",
        "map_title": "KMMOM验证阶段资料地图",
        "description": "测试计划、测试报告和交付文档相关资料。",
        "anchor": ["测试标准与模板总览", "测试过程规范总览", "测试策略"],
        "type": "asset",
    },
    "05-release": {
        "name": "发布阶段",
        "map_title": "KMMOM发布阶段资料地图",
        "description": "发布检查、部署 SOP、发布说明和推广 FAQ。",
        "anchor": ["技术手册总览", "基础环境运维总览", "版本与代码管理总览"],
        "type": "manual",
    },
    "06-lifecycle": {
        "name": "生命周期阶段",
        "map_title": "KMMOM生命周期资料地图",
        "description": "运营管理、支持知识库和生命周期改进资料。",
        "anchor": ["问题沉淀库总览", "业务常见问题库总览", "日常环境问题总览"],
        "type": "archive",
    },
    "07-governance": {
        "name": "治理支撑",
        "map_title": "KMMOM治理支撑资料地图",
        "description": "决策记录、会议纪要、复盘模板和产品研发规范。",
        "anchor": ["通用规范总览", "管理制度与安全总览", "研发流程标准总览"],
        "type": "standard",
    },
    "root": {
        "name": "仓库总览",
        "map_title": "KMMOM仓库总览资料地图",
        "description": "km-mom-docs 根目录说明、任务清单和协作约定。",
        "anchor": ["MOM系统总览", "业务系统总览", "LLM入库规则"],
        "type": "product",
    },
}

SUBTOPIC_LABELS = {
    "charter-versions": "Charter版本",
    "architecture": "架构设计",
    "requirements": "需求管理",
    "version-planning": "版本计划",
    "datamodel-design": "数据模型设计",
    "module-design": "模块设计",
    "tech-design": "技术设计",
    "webapi": "WebAPI",
    "documentation": "交付文档",
    "test-plan": "测试计划",
    "test-reports": "测试报告",
    "deployment": "部署SOP",
    "promotion": "推广FAQ",
    "release-notes": "发布说明",
    "operations": "运营管理",
    "support": "支持知识库",
    "meetings": "会议纪要",
    "retrospectives": "复盘模板",
    "standards": "规范标准",
    "basic-data": "基础数据",
    "product-roadmap.md": "产品路标",
    "strategy-planning.md": "战略规划",
    "release-checklist.md": "发布检查清单",
    "decisions.md": "决策记录",
}

WEAK_HEADINGS = {
    "目录", "概述", "背景", "说明", "总结", "变更记录", "参考资料", "附录", "文档信息", "README"
}

MODULE_KEYWORDS = {
    "角色权限": ["角色权限需求拆解", "角色权限矩阵", "登录权限需求导航"],
    "配置管理": ["配置管理需求拆解", "后台管理需求导航"],
    "系统配置引导": ["系统配置引导需求拆解", "后台管理需求导航"],
    "首页角色工作台": ["首页角色工作台需求拆解", "登录权限需求导航"],
    "系统菜单管理": ["系统菜单管理需求拆解", "登录权限需求导航"],
    "客户端布局": ["客户端布局需求拆解", "后台管理需求导航"],
    "服务端布局": ["服务端布局需求拆解", "后台管理需求导航"],
    "扩展能力": ["扩展能力需求拆解", "后台管理需求导航"],
    "工厂建模": ["工厂建模需求拆解", "核心业务需求导航"],
    "产品数据": ["产品数据需求拆解", "核心业务需求导航"],
    "工艺数据": ["工艺数据需求拆解", "核心业务需求导航"],
    "工序库": ["工序库需求拆解", "核心业务需求导航"],
    "生产异常": ["生产异常需求拆解", "核心业务需求导航"],
    "计划管理": ["计划管理需求拆解", "核心业务需求导航"],
    "计划调度": ["计划调度需求拆解", "核心业务需求导航"],
    "任务调度": ["任务调度需求拆解", "核心业务需求导航"],
    "外委计划": ["外委计划需求拆解", "核心业务需求导航"],
    "变更管理": ["变更管理需求拆解", "核心业务需求导航"],
    "备料管理": ["备料管理需求拆解", "核心业务需求导航"],
    "物料动态占用": ["物料动态占用与优先级管理需求拆解", "核心业务需求导航"],
    "工时管理": ["工时管理需求拆解", "核心业务需求导航"],
    "物料采购": ["物料采购管理需求拆解", "核心业务需求导航"],
    "质量方案": ["质量方案需求拆解", "核心业务需求导航"],
    "质量执行": ["质量执行需求拆解", "核心业务需求导航"],
    "质量记录": ["质量记录需求拆解", "核心业务需求导航"],
    "质量不合格": ["质量不合格处理需求拆解", "核心业务需求导航"],
    "返工返修": ["返工返修需求拆解", "核心业务需求导航"],
    "质量履历": ["质量履历需求拆解", "核心业务需求导航"],
    "计划排产": ["计划排产需求拆解", "核心业务需求导航"],
    "计划排程": ["计划排程（AS）需求拆解", "核心业务需求导航"],
    "协同排产": ["协同排产需求拆解", "核心业务需求导航"],
    "装配排程": ["装配排程需求拆解", "核心业务需求导航"],
    "仓储管理": ["仓储管理需求拆解", "核心业务需求导航"],
    "物流管理": ["物流管理需求拆解", "核心业务需求导航"],
    "设备管理": ["设备管理需求拆解", "核心业务需求导航"],
    "工装工具": ["工装工具管理需求拆解", "核心业务需求导航"],
    "工装备料": ["工装备料计划管理需求拆解", "核心业务需求导航"],
    "看板": ["看板&报表需求拆解", "核心业务需求导航"],
    "审批流": ["审批流管理需求拆解", "后台管理需求导航"],
    "智能问数": ["智能问数需求拆解", "智能能力需求导航"],
    "文档智能识别": ["文档智能识别需求拆解", "智能能力需求导航"],
    "APS": ["APS智能体需求拆解", "智能能力需求导航"],
    "产品标准化": ["产品标准化问题需求拆解", "后台管理需求导航"],
}


def clean_inline(text: str) -> str:
    text = text.replace("\ufeff", "").replace("\u200b", "")
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def heading_text(text: str) -> str:
    text = clean_inline(text)
    text = re.sub(r"^[#\s]+", "", text)
    text = re.sub(r"^\d+(?:\.\d+)*[.、]?\s*", "", text)
    return text.strip(" -—:：")


def sanitize_filename(text: str, max_length: int = 90) -> str:
    text = re.sub(r"[<>:\"/\\|?*\[\]]", "-", text)
    text = re.sub(r"\s+", "", text)
    text = text.strip(" .-_")
    if len(text) > max_length:
        text = text[:max_length].rstrip("-_")
    return text or "未命名页面"


def relative_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def stage_key_for(path: Path) -> str:
    parts = path.relative_to(SOURCE_ROOT).parts
    if len(parts) == 1:
        return "root"
    return parts[0]


def subtopic_for(path: Path) -> str:
    parts = path.relative_to(SOURCE_ROOT).parts
    if len(parts) == 1:
        return "根目录"
    if len(parts) >= 3 and parts[1] == "datamodel-design":
        return SUBTOPIC_LABELS.get(parts[2], SUBTOPIC_LABELS.get(parts[1], parts[1]))
    return SUBTOPIC_LABELS.get(parts[1], parts[1])


def output_folder_for(path: Path) -> Path:
    stage_key = stage_key_for(path)
    stage_name = STAGES[stage_key]["name"]
    subtopic = subtopic_for(path)
    if stage_key == "root":
        return OUTPUT_ROOT / "00_仓库总览"
    return OUTPUT_ROOT / f"{stage_key}_{stage_name}" / subtopic


def parse_sections(text: str) -> list[dict[str, object]]:
    lines = text.splitlines()
    headings: list[tuple[int, int, str]] = []
    for line_index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.*\S)\s*$", line)
        if match:
            headings.append((line_index, len(match.group(1)), heading_text(match.group(2))))
    sections: list[dict[str, object]] = []
    for heading_index, (line_index, level, title) in enumerate(headings):
        end_index = headings[heading_index + 1][0] if heading_index + 1 < len(headings) else len(lines)
        sections.append({"level": level, "title": title, "body": lines[line_index + 1:end_index]})
    return sections


def first_heading(path: Path, sections: list[dict[str, object]]) -> str:
    for section in sections:
        if int(section["level"]) == 1 and str(section["title"]).strip():
            return str(section["title"])
    stem = path.stem
    if stem.lower() == "readme":
        parent = path.parent.name
        return f"{SUBTOPIC_LABELS.get(parent, parent)}说明"
    return stem


def snippet_from_lines(lines: list[str], limit: int = 120) -> str:
    snippets: list[str] = []
    for line in lines:
        if re.match(r"^\s*#", line):
            continue
        value = clean_inline(line)
        if not value or value.startswith("|") or re.fullmatch(r"[-:| ]+", value):
            continue
        if re.search(r"\.(png|jpg|jpeg|xlsx)$", value, re.I):
            continue
        snippets.append(value)
        if len("；".join(snippets)) >= limit or len(snippets) >= 2:
            break
    return "；".join(snippets)[:limit]


def outline_for(sections: list[dict[str, object]], limit: int = 10) -> list[str]:
    outline: list[str] = []
    for section in sections:
        title = str(section["title"])
        level = int(section["level"])
        if not title or title in WEAK_HEADINGS or level > 3:
            continue
        if title not in outline:
            outline.append(title)
        if len(outline) >= limit:
            break
    return outline


def key_points_for(sections: list[dict[str, object]], limit: int = 6) -> list[str]:
    points: list[str] = []
    for section in sections:
        title = str(section["title"])
        if not title or title in WEAK_HEADINGS:
            continue
        snippet = snippet_from_lines(list(section["body"]), 100)
        if snippet:
            points.append(f"{title}：{snippet}")
        else:
            points.append(title)
        if len(points) >= limit:
            break
    return points


def tags_for(stage_key: str, subtopic: str) -> list[str]:
    tags = ["testing", "mom", "product-docs", "km-mom-docs"]
    tags.append(stage_key.replace("-", "_"))
    if subtopic:
        tags.append(re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "_", subtopic).strip("_"))
    return list(dict.fromkeys(tags))


def page_type_for(stage_key: str, subtopic: str) -> str:
    if stage_key == "07-governance":
        return "standard" if subtopic in {"规范标准", "决策记录"} else "archive"
    if stage_key == "04-verification":
        return "asset"
    if stage_key in {"05-release", "06-lifecycle"}:
        return "manual"
    if subtopic in {"WebAPI", "数据模型设计", "基础数据"}:
        return "business"
    return STAGES.get(stage_key, STAGES["root"])["type"]


def existing_wiki_stems() -> set[str]:
    return {
        path.stem
        for path in WIKI.rglob("*.md")
        if path.name not in {"index.md", "log.md"}
    }


def module_links_for(title: str, source_rel: str, known_pages: set[str]) -> list[str]:
    links: list[str] = []
    haystack = f"{title} {source_rel}"
    code_match = re.search(r"DNW\d{5}", haystack, re.I)
    if code_match:
        code = code_match.group(0).upper()
        for stem in sorted(known_pages):
            if code in stem and stem not in links:
                links.append(stem)
    for keyword, candidates in MODULE_KEYWORDS.items():
        if keyword in haystack:
            for candidate in candidates:
                if candidate in known_pages and candidate not in links:
                    links.append(candidate)
    return links[:8]


def write_page(path: Path, title: str, page_type: str, status: str, tags: list[str], summary: str, sources: list[str], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tag_lines = "\n".join(f"  - {tag}" for tag in tags)
    source_lines = "\n".join(f"  - {source}" for source in sources)
    content = f"""---
title: {title}
type: {page_type}
status: {status}
tags:
{tag_lines}
summary: {summary}
source:
{source_lines}
updated: {TODAY}
---

# {title}

{body.strip()}
"""
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def collect_documents() -> list[dict[str, object]]:
    docs: list[dict[str, object]] = []
    existing_stems = existing_wiki_stems()
    used_stems: Counter[str] = Counter()
    markdown_paths = sorted(
        path for path in SOURCE_ROOT.rglob("*.md")
        if ".git" not in path.parts
    )
    for source_path in markdown_paths:
        source_rel = relative_path(source_path)
        text = source_path.read_text(encoding="utf-8", errors="ignore")
        sections = parse_sections(text)
        source_title = first_heading(source_path, sections)
        stage_key = stage_key_for(source_path)
        stage = STAGES.get(stage_key, STAGES["root"])
        subtopic = subtopic_for(source_path)
        page_title = f"KMMOM产品资料-{source_title}"
        page_stem = sanitize_filename(page_title)
        used_stems[page_stem] += 1
        if used_stems[page_stem] > 1:
            page_stem = sanitize_filename(f"{page_title}-{used_stems[page_stem]}")
        output_path = output_folder_for(source_path) / f"{page_stem}.md"
        outline = outline_for(sections)
        key_points = key_points_for(sections)
        intro = snippet_from_lines(text.splitlines(), 160)
        module_links = module_links_for(source_title, source_rel, existing_stems)
        code_match = re.search(r"DNW\d{5}", f"{source_title} {source_rel}", re.I)
        docs.append({
            "source_path": source_path,
            "source_rel": source_rel,
            "source_title": source_title,
            "page_title": page_title,
            "page_stem": output_path.stem,
            "output_path": output_path,
            "stage_key": stage_key,
            "stage_name": stage["name"],
            "subtopic": subtopic,
            "outline": outline,
            "key_points": key_points,
            "intro": intro,
            "page_type": page_type_for(stage_key, subtopic),
            "tags": tags_for(stage_key, subtopic),
            "module_links": module_links,
            "code": code_match.group(0).upper() if code_match else "",
        })
    return docs


def related_docs_for(doc: dict[str, object], docs: list[dict[str, object]]) -> list[str]:
    related: list[str] = []
    code = str(doc["code"])
    if code:
        for other in docs:
            if other is doc:
                continue
            if other.get("code") == code and str(other["page_stem"]) not in related:
                related.append(str(other["page_stem"]))
    if len(related) < 6:
        for other in docs:
            if other is doc:
                continue
            if other["stage_key"] == doc["stage_key"] and other["subtopic"] == doc["subtopic"]:
                stem = str(other["page_stem"])
                if stem not in related:
                    related.append(stem)
            if len(related) >= 6:
                break
    return related[:6]


def render_doc_page(doc: dict[str, object], docs: list[dict[str, object]]) -> str:
    stage_map = STAGES[str(doc["stage_key"])] ["map_title"]
    anchor_links = list(STAGES[str(doc["stage_key"])] ["anchor"])
    if str(doc["subtopic"]) in {"WebAPI", "数据模型设计", "基础数据"}:
        anchor_links.insert(0, "接口与数据字典总览")
    related = related_docs_for(doc, docs)
    body: list[str] = []
    body.extend([
        "## 简介",
        "",
        f"- 来源路径：`{doc['source_rel']}`",
        f"- IPD 阶段：`{doc['stage_name']}`",
        f"- 资料主题：`{doc['subtopic']}`",
        f"- 内容定位：{doc['intro'] or '来源文档未提供可直接抽取的简介，需结合原文继续补充。'}",
        "- 说明：本页为结构化摘要，最终口径以来源文档为准。",
        "",
        "## 正文摘要",
        "",
    ])
    for point in (doc["key_points"] or ["待结合来源文档补充关键内容。"]):
        body.append(f"- {point}")
    body.extend(["", "## 文档结构", ""])
    for item in (doc["outline"] or [str(doc["source_title"])]):
        body.append(f"- {item}")
    body.extend(["", "## 链接关系", "", f"- [[KMMOM产品资料总览]]", f"- [[{stage_map}]]"])
    for link in anchor_links:
        if link not in {"KMMOM产品资料总览", stage_map}:
            body.append(f"- [[{link}]]")
    for link in doc["module_links"]:
        body.append(f"- [[{link}]]")
    body.extend(["", "## 同源相关文档", ""])
    for stem in related:
        body.append(f"- [[{stem}]]")
    if not related:
        body.append(f"- 通过 [[{stage_map}]] 查看同阶段资料。")
    body.extend([
        "",
        "## 关键字",
        "",
        f"- KMMOM",
        f"- {doc['stage_name']}",
        f"- {doc['subtopic']}",
    ])
    if doc["code"]:
        body.append(f"- {doc['code']}")
    body.extend(["", "## 更新日期", "", f"- {TODAY}", "", "## 责任人", "", "- 待确认"])
    return "\n".join(body)


def render_overview(docs: list[dict[str, object]], attachment_info: dict[str, object]) -> None:
    stage_counts = Counter(str(doc["stage_key"]) for doc in docs)
    subtopic_counts = Counter(str(doc["subtopic"]) for doc in docs)
    body: list[str] = [
        "## 简介",
        "",
        "`KMMOM产品资料总览` 用于沉淀 `raw/产品资料/km-mom-docs/` 的 IPD 全流程产品资料，连接战略规划、需求、架构、设计、验证、发布、生命周期和治理规范。",
        "",
        "## 资料统计",
        "",
        "| 类型 | 数量 |",
        "| --- | ---: |",
        f"| Markdown 文档 | {len(docs)} |",
        f"| 图片附件 | {attachment_info['image_count']} |",
        f"| Excel 附件 | {attachment_info['xlsx_count']} |",
        "",
        "## 阶段地图",
        "",
    ]
    for stage_key, stage in STAGES.items():
        count = stage_counts.get(stage_key, 0)
        body.append(f"- [[{stage['map_title']}]]：{stage['description']}（{count} 篇）")
    body.extend(["", "## 主题分布", "", "| 主题 | 文档数 |", "| --- | ---: |"])
    for subtopic, count in subtopic_counts.most_common():
        body.append(f"| {subtopic} | {count} |")
    body.extend([
        "",
        "## 核心入口",
        "",
        "- [[MOM系统总览]]",
        "- [[MOM需求分析总览]]",
        "- [[模块业务手册总览]]",
        "- [[接口与数据字典总览]]",
        "- [[技术手册总览]]",
        "- [[测试标准与模板总览]]",
        "- [[KMMOM产品资料附件清单]]",
        "",
        "## 关键字",
        "",
        "- KMMOM",
        "- MOM",
        "- IPD",
        "- 产品资料",
        "- 需求管理",
        "- 架构设计",
        "- 模块设计",
        "- 发布部署",
        "",
        "## 更新日期",
        "",
        f"- {TODAY}",
        "",
        "## 责任人",
        "",
        "- 待确认",
    ])
    write_page(
        WIKI / "03_业务系统" / "MOM" / "KMMOM产品资料总览.md",
        "KMMOM产品资料总览",
        "product",
        "active",
        ["testing", "mom", "product-docs", "km-mom-docs", "navigation"],
        "汇总 raw/产品资料/km-mom-docs 的 IPD 全流程产品资料，并连接 MOM 业务系统知识页。",
        ["raw/产品资料/km-mom-docs/"],
        "\n".join(body),
    )


def render_stage_maps(docs: list[dict[str, object]]) -> None:
    by_stage: dict[str, list[dict[str, object]]] = defaultdict(list)
    for doc in docs:
        by_stage[str(doc["stage_key"])].append(doc)
    for stage_key, stage in STAGES.items():
        stage_docs = sorted(by_stage.get(stage_key, []), key=lambda item: (str(item["subtopic"]), str(item["page_title"])))
        body: list[str] = [
            "## 简介",
            "",
            f"- 阶段定位：{stage['description']}",
            f"- 来源范围：`raw/产品资料/km-mom-docs/{'' if stage_key == 'root' else stage_key + '/'}`",
            f"- 收录文档：{len(stage_docs)} 篇",
            "",
            "## 文档清单",
            "",
        ]
        grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
        for doc in stage_docs:
            grouped[str(doc["subtopic"])].append(doc)
        for subtopic in sorted(grouped):
            body.append(f"### {subtopic}")
            for doc in grouped[subtopic]:
                intro = str(doc["intro"] or "查看来源文档结构化摘要。")
                body.append(f"- [[{doc['page_stem']}]]：{intro[:80]}")
            body.append("")
        body.extend(["## 关联页面", "", "- [[KMMOM产品资料总览]]"])
        for link in stage["anchor"]:
            body.append(f"- [[{link}]]")
        body.extend(["", "## 关键字", "", f"- {stage['name']}", "- KMMOM", "- 产品资料", "", "## 更新日期", "", f"- {TODAY}", "", "## 责任人", "", "- 待确认"])
        write_page(
            OUTPUT_ROOT / f"{stage_key}_{stage['name']}" / f"{stage['map_title']}.md" if stage_key != "root" else OUTPUT_ROOT / "00_仓库总览" / f"{stage['map_title']}.md",
            str(stage["map_title"]),
            str(stage["type"]),
            "active",
            ["testing", "mom", "product-docs", "km-mom-docs", "navigation", stage_key.replace("-", "_")],
            str(stage["description"]),
            ["raw/产品资料/km-mom-docs/" if stage_key == "root" else f"raw/产品资料/km-mom-docs/{stage_key}/"],
            "\n".join(body),
        )


def attachment_summary() -> dict[str, object]:
    files = [path for path in SOURCE_ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    image_files = [path for path in files if path.suffix.lower() in {".png", ".jpg", ".jpeg"}]
    excel_files = [path for path in files if path.suffix.lower() == ".xlsx"]
    by_folder = Counter(
        "/".join(path.relative_to(SOURCE_ROOT).parts[:2]) if len(path.relative_to(SOURCE_ROOT).parts) > 1 else "root"
        for path in image_files + excel_files
    )
    body: list[str] = [
        "## 简介",
        "",
        "本页汇总 `km-mom-docs` 中的图片与 Excel 附件，便于后续做原型、流程图、表格资产的二次整理。",
        "",
        "## 附件统计",
        "",
        "| 类型 | 数量 |",
        "| --- | ---: |",
        f"| 图片附件 | {len(image_files)} |",
        f"| Excel 附件 | {len(excel_files)} |",
        "",
        "## 分布概览",
        "",
        "| 来源目录 | 附件数 |",
        "| --- | ---: |",
    ]
    for folder, count in by_folder.most_common(30):
        body.append(f"| raw/产品资料/km-mom-docs/{folder}/ | {count} |")
    body.extend(["", "## Excel 附件清单", ""])
    for path in excel_files[:80]:
        body.append(f"- `{relative_path(path)}`")
    if not excel_files:
        body.append("- 暂无 Excel 附件。")
    body.extend(["", "## 关联页面", "", "- [[KMMOM产品资料总览]]", "- [[MOM系统总览]]", "", "## 关键字", "", "- KMMOM", "- 附件", "- 图片", "- Excel", "", "## 更新日期", "", f"- {TODAY}", "", "## 责任人", "", "- 待确认"])
    write_page(
        WIKI / "03_业务系统" / "MOM" / "KMMOM产品资料附件清单.md",
        "KMMOM产品资料附件清单",
        "asset",
        "active",
        ["testing", "mom", "product-docs", "attachment"],
        "汇总 raw/产品资料/km-mom-docs 中的图片与 Excel 附件分布。",
        ["raw/产品资料/km-mom-docs/"],
        "\n".join(body),
    )
    return {"image_count": len(image_files), "xlsx_count": len(excel_files)}


def append_section_once(path: Path, marker: str, section: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    path.write_text(text.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")


def update_anchor_pages() -> None:
    updates = {
        WIKI / "03_业务系统" / "MOM" / "MOM系统总览.md": """
## KMMOM产品资料库入口

- [[KMMOM产品资料总览]]：IPD 全流程产品资料入口
- [[KMMOM计划阶段资料地图]]：版本规划、需求管理和架构设计资料
- [[KMMOM开发阶段资料地图]]：数据模型、模块设计、技术设计和 WebAPI 资料
- [[KMMOM产品资料附件清单]]：图片与 Excel 附件分布清单
""",
        WIKI / "03_业务系统" / "MOM" / "模块业务手册" / "模块业务手册总览.md": """
## KMMOM需求与设计资料

- [[KMMOM计划阶段资料地图]]：需求管理与架构资料入口
- [[KMMOM开发阶段资料地图]]：模块设计与技术设计资料入口
- [[KMMOM产品资料总览]]：产品资料库总入口
""",
        WIKI / "03_业务系统" / "MOM" / "接口&数据字典" / "接口与数据字典总览.md": """
## KMMOM模型与接口资料

- [[KMMOM开发阶段资料地图]]：数据模型、WebAPI 和技术设计资料入口
- [[KMMOM产品资料总览]]：产品资料库总入口
""",
        WIKI / "03_业务系统" / "业务系统总览.md": """
## KMMOM产品资料入口

- [[KMMOM产品资料总览]]：连接 km-mom-docs 的概念、计划、开发、验证、发布、生命周期和治理资料
""",
        WIKI / "04_技术手册" / "技术手册总览.md": """
## KMMOM发布与技术资料

- [[KMMOM发布阶段资料地图]]：部署 SOP、发布检查与发布说明
- [[KMMOM开发阶段资料地图]]：技术设计、WebAPI 和模型资料
""",
        WIKI / "02_测试标准&模板" / "测试标准与模板总览.md": """
## KMMOM验证资料

- [[KMMOM验证阶段资料地图]]：测试计划、测试报告和交付文档资料
""",
        WIKI / "01_通用规范" / "通用规范总览.md": """
## KMMOM治理资料

- [[KMMOM治理支撑资料地图]]：决策记录、会议纪要、复盘模板和产品研发规范
""",
    }
    for path, section in updates.items():
        if path.exists():
            marker = next((line.strip() for line in section.splitlines() if line.strip()), "")
            append_section_once(path, marker, section)


def update_schema_and_readme() -> None:
    schema_path = ROOT / "SCHEMA.md"
    schema = schema_path.read_text(encoding="utf-8")
    schema_marker = "- `wiki/03_业务系统/MOM/产品资料库/`：沉淀 `raw/产品资料/km-mom-docs/` 的 IPD 全流程产品资料拆解页"
    if schema_marker not in schema:
        schema = schema.replace(
            "- `wiki/03_业务系统/`：按 MOM/MES/ERP/WMS/中间件平台等系统沉淀业务知识",
            "- `wiki/03_业务系统/`：按 MOM/MES/ERP/WMS/中间件平台等系统沉淀业务知识\n" + schema_marker,
        )
    schema_path.write_text(schema, encoding="utf-8")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    readme_marker = "- `wiki/03_业务系统/MOM/产品资料库/`：`km-mom-docs` 产品资料拆解页、阶段地图和附件清单"
    if readme_marker not in readme:
        readme = readme.replace(
            "- `wiki/03_业务系统/`：MOM/MES/ERP/WMS/中间件等业务系统知识库",
            "- `wiki/03_业务系统/`：MOM/MES/ERP/WMS/中间件等业务系统知识库\n" + readme_marker,
        )
    readme_path.write_text(readme, encoding="utf-8")


def update_sync_script() -> None:
    script_path = ROOT / "scripts" / "sync_wiki_meta.py"
    text = script_path.read_text(encoding="utf-8")
    marker = '    "KMMOM产品资料总览",'
    if marker not in text:
        text = text.replace(
            '    "MOM需求分析总览",\n',
            '    "MOM需求分析总览",\n    "KMMOM产品资料总览",\n    "KMMOM计划阶段资料地图",\n    "KMMOM开发阶段资料地图",\n',
        )
    script_path.write_text(text, encoding="utf-8")


def update_log(created_count: int) -> None:
    log_path = WIKI / "log.md"
    text = log_path.read_text(encoding="utf-8") if log_path.exists() else "# Wiki Log\n"
    title = f"## {TODAY} update | 拆解 km-mom-docs 产品资料"
    if title in text:
        return
    body = text.strip()
    if body.startswith("# Wiki Log"):
        body = body[len("# Wiki Log"):].strip()
    entry = "\n".join([
        "# Wiki Log",
        "",
        title,
        "",
        f"- 基于 `raw/产品资料/km-mom-docs/` 生成 {created_count} 个产品资料结构化页面",
        "- 新增 `KMMOM产品资料总览`、7 个 IPD 阶段资料地图和附件清单",
        "- 建立产品资料页与 MOM 系统总览、模块业务手册、接口数据字典、技术手册和测试标准之间的 wikilinks",
        "- 同步更新 `SCHEMA.md`、`README.md` 与 `scripts/sync_wiki_meta.py` 的入口说明",
    ])
    if body:
        entry += "\n\n" + body
    log_path.write_text(entry.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    docs = collect_documents()
    for doc in docs:
        body = render_doc_page(doc, docs)
        write_page(
            Path(doc["output_path"]),
            str(doc["page_title"]),
            str(doc["page_type"]),
            "review",
            list(doc["tags"]),
            f"基于 {doc['source_rel']} 提炼的 KMMOM 产品资料结构化摘要。",
            [str(doc["source_rel"])],
            body,
        )
    attachment_info = attachment_summary()
    render_overview(docs, attachment_info)
    render_stage_maps(docs)
    update_anchor_pages()
    update_schema_and_readme()
    update_sync_script()
    created_count = len(docs) + len(STAGES) + 2
    update_log(created_count)
    print(f"source_docs={len(docs)}")
    print(f"generated_pages={created_count}")
    print(f"images={attachment_info['image_count']}")
    print(f"xlsx={attachment_info['xlsx_count']}")


if __name__ == "__main__":
    main()
