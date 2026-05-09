#!/usr/bin/env python3
"""Convert raw defect notes into KMMOM Jira-importable CSV rows."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from pypinyin import lazy_pinyin
except ImportError:
    lazy_pinyin = None

DEFAULT_COLUMNS = [
    "问题类型",
    "状态",
    "概要",
    "优先级",
    "模块",
    "缺陷严重程度",
    "对用户的影响程度",
    "描述",
    "影响范围分析",
    "责任人",
    "测试责任人",
    "缺陷产生者",
    "到期日",
    "使用的版本",
    "修复的版本",
    "Sprint",
]

TARGET_PROJECT = "KMMOM-3(KMMOM3)"
DEFAULT_ISSUE_TYPE = "缺陷"
DEFAULT_STATUS = "缺陷编制中"
DEFAULT_ENV = "测试环境：http://192.168.30.69:40000"
DEFAULT_SPRINT_ID = "276"
OUTPUT_DIRNAME = "exports"
VERSION_CUTOFF = date(2026, 4, 15)

STATUS_OPTIONS = [
    "缺陷编制中",
    "缺陷分派中",
    "打开",
    "打开（重新打开）",
    "打开（验证失败）",
    "已修复待签发",
    "已签发测试中",
    "缺陷关闭",
]

PRIORITY_OPTIONS = [
    "P0-重要紧急(120)",
    "P1-重要不紧急(100)",
    "P2-紧急不重要(100)",
    "P3-不重要不紧急(80)",
]
PRIORITY_DUE_DAYS = {
    "P0-重要紧急(120)": 0,
    "P1-重要不紧急(100)": 1,
    "P2-紧急不重要(100)": 3,
    "P3-不重要不紧急(80)": 5,
}

SEVERITY_OPTIONS = ["一级", "二级", "三级", "四级", "五级", "六级", "建议"]
IMPACT_OPTIONS = ["无", "高", "中", "低"]
VERSION_OPTIONS = [
    "KMMOM Cloud V3.2",
    "KMMOM Cloud V3.3",
    "KMMOM Cloud V3.4",
    "KMMOM Cloud V3.5",
]
SPRINT_DISPLAY_TO_ID = {
    "V3.4-a1(260131)": "263",
    "V3.4-a2(260214)": "264",
    "V3.4-a3(260307)": "270",
    "V3.4-a4(260321)": "271",
    "V3.4-a5(260404)": "274",
    "V3.4-a6(260418)": "276",
}
SPRINT_ID_TO_DISPLAY = {value: key for key, value in SPRINT_DISPLAY_TO_ID.items()}
MODULE_OPTIONS = [
    "01-mom-platform",
    "02-mom-mes",
    "03-mom-aps",
    "04-mom-wms",
    "05-mom-ems",
    "06-mom-tms",
    "07-mom-bds",
    "08-mom-approve",
]
MODULE_KEYWORDS: Dict[str, List[str]] = {
    "01-mom-platform": ["系统管理", "主数据", "platform", "用户管理", "角色", "权限", "字典"],
    "02-mom-mes": ["计划管理", "制造执行", "mes", "工单", "报工", "生产", "工序", "工位", "派工"],
    "03-mom-aps": ["aps", "apsp", "排程", "排产", "甘特", "计划排程"],
    "04-mom-wms": ["wms", "仓储", "物流", "入库", "出库", "移库", "盘点", "库位"],
    "05-mom-ems": ["ems", "设备", "点检", "维保", "保养", "设备台账", "故障"],
    "06-mom-tms": ["tms", "工装", "夹具", "治具", "刀具", "工装台账"],
    "07-mom-bds": ["bds", "统计", "分析", "报表", "看板", "指标", "bi"],
    "08-mom-approve": ["approve", "审批", "审批流", "工作流", "流程审批"],
}

FIELD_ALIASES: Dict[str, str] = {
    "问题类型": "issue_type",
    "类型": "issue_type",
    "issue type": "issue_type",
    "issuetype": "issue_type",
    "状态": "status",
    "state": "status",
    "status": "status",
    "概要": "summary",
    "标题": "summary",
    "summary": "summary",
    "优先级": "priority",
    "priority": "priority",
    "模块": "module",
    "module": "module",
    "缺陷严重程度": "severity",
    "严重程度": "severity",
    "severity": "severity",
    "对用户的影响程度": "user_impact",
    "用户影响": "user_impact",
    "影响程度": "user_impact",
    "impact level": "user_impact",
    "描述": "description",
    "环境": "environment",
    "问题描述": "problem",
    "问题": "problem",
    "现象": "problem",
    "操作步骤": "steps",
    "复现步骤": "steps",
    "steps": "steps",
    "实际结果": "actual",
    "actual": "actual",
    "期望结果": "expected",
    "expected": "expected",
    "影响范围分析": "impact",
    "影响范围": "impact",
    "影响": "impact",
    "责任人": "owner",
    "assignee": "owner",
    "测试责任人": "qa_owner",
    "测试负责人": "qa_owner",
    "缺陷产生者": "creator",
    "报告人": "creator",
    "reporter": "creator",
    "到期日": "due_date",
    "duedate": "due_date",
    "使用的版本": "version",
    "修复的版本": "fix_version",
    "修复版本": "fix_version",
    "fix version": "fix_version",
    "fixversion": "fix_version",
    "version": "version",
    "sprint": "sprint",
    "附件": "pending",
    "截图": "pending",
    "日志": "pending",
    "录屏": "pending",
    "待确认": "pending",
    "pending": "pending",
}

SECTION_KEYS = {"environment", "problem", "steps", "actual", "expected", "impact", "pending"}

STATUS_ALIAS = {
    "编制中": "缺陷编制中",
    "分派中": "缺陷分派中",
    "重新打开": "打开（重新打开）",
    "验证失败": "打开（验证失败）",
    "待签发": "已修复待签发",
    "测试中": "已签发测试中",
    "关闭": "缺陷关闭",
}
PRIORITY_ALIAS = {
    "p0": "P0-重要紧急(120)",
    "p1": "P1-重要不紧急(100)",
    "p2": "P2-紧急不重要(100)",
    "p3": "P3-不重要不紧急(80)",
    "重要紧急": "P0-重要紧急(120)",
    "重要不紧急": "P1-重要不紧急(100)",
    "紧急不重要": "P2-紧急不重要(100)",
    "不重要不紧急": "P3-不重要不紧急(80)",
}
SEVERITY_ALIAS = {
    "1": "一级",
    "2": "二级",
    "3": "三级",
    "4": "四级",
    "5": "五级",
    "6": "六级",
    "一级": "一级",
    "二级": "二级",
    "三级": "三级",
    "四级": "四级",
    "五级": "五级",
    "六级": "六级",
    "建议": "建议",
}
IMPACT_ALIAS = {
    "无": "无",
    "高": "高",
    "中": "中",
    "低": "低",
    "none": "无",
    "high": "高",
    "medium": "中",
    "low": "低",
}

DELIMITER_LINE = re.compile(r"^\s*(?:-{3,}|={3,}|\*{3,})\s*$")
HEADING_SPLIT = re.compile(r"(?im)^\s*(?:问题|缺陷|bug|issue)\s*#?\d+\s*[:：].*$")
ISSUE_HEADER_LINE = re.compile(r"^\s*(?:问题|缺陷|bug|issue)\s*#?\d+\s*[:：]?\s*$", re.IGNORECASE)
ISSUE_HEADER_WITH_TITLE = re.compile(r"^\s*(?:\u95ee\u9898|\u7f3a\u9677|bug|issue)\s*#?\d+\s*[:\uff1a]\s*(.+?)\s*$", re.IGNORECASE)
FIELD_LINE = re.compile(r"^\s*([^:：]{1,40})\s*[:：]\s*(.*)\s*$")
OWNER_RE = re.compile(r"^[a-z][a-z0-9._-]*$")
CJK_NAME_RE = re.compile(r"^[㐀-䶿一-鿿??]+$")
COMPOUND_SURNAMES = {
    "??", "??", "??", "??", "??", "??", "??", "??", "??", "??",
    "??", "??", "??", "??", "??", "??", "??", "??", "??", "??",
    "??", "??", "??", "??", "??", "??", "??", "??", "??", "??",
    "??", "??", "??", "??", "??", "??", "??", "??", "??", "??",
    "??", "??", "??", "??", "??", "??", "??", "??", "??", "??",
    "??", "??", "??", "??", "??", "??", "??", "??", "??", "??",
    "??", "??", "??", "??", "??", "??", "??", "??", "??", "??",
    "??", "??", "??", "??", "??",
}


@dataclass
class ParsedIssue:
    fields: Dict[str, str] = field(default_factory=dict)
    sections: Dict[str, List[str]] = field(
        default_factory=lambda: {
            "environment": [],
            "problem": [],
            "steps": [],
            "actual": [],
            "expected": [],
            "impact": [],
            "pending": [],
        }
    )


def normalize_key(raw: str) -> str:
    cleaned = raw.lstrip("\ufeff").strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.replace("_", " ")
    return cleaned


def split_issues(text: str) -> List[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff").strip()
    if not text:
        return []

    lines = text.split("\n")
    if any(DELIMITER_LINE.match(line) for line in lines):
        blocks: List[str] = []
        bucket: List[str] = []
        for line in lines:
            if DELIMITER_LINE.match(line):
                if bucket:
                    blocks.append("\n".join(bucket).strip())
                    bucket = []
            else:
                bucket.append(line)
        if bucket:
            blocks.append("\n".join(bucket).strip())
        return [block for block in blocks if block]

    headings = list(HEADING_SPLIT.finditer(text))
    if len(headings) >= 2:
        blocks = []
        for idx, match in enumerate(headings):
            start = match.start()
            end = headings[idx + 1].start() if idx + 1 < len(headings) else len(text)
            block = text[start:end].strip()
            if block:
                blocks.append(block)
        return blocks

    return [text]


def strip_issue_heading(line: str) -> str:
    match = ISSUE_HEADER_WITH_TITLE.match((line or "").strip())
    if match:
        return match.group(1).strip()
    return (line or "").strip()


def parse_issue(block: str) -> ParsedIssue:
    issue = ParsedIssue()
    current_target = "problem"

    for raw_line in block.splitlines():
        line = raw_line.lstrip("\ufeff").strip()
        if not line:
            continue

        heading_match = ISSUE_HEADER_WITH_TITLE.match(line)
        if heading_match:
            heading_summary = heading_match.group(1).strip()
            if heading_summary and not issue.fields.get("summary"):
                issue.fields["summary"] = heading_summary
            continue

        if ISSUE_HEADER_LINE.match(line):
            continue

        field_match = FIELD_LINE.match(line)
        if field_match:
            key = normalize_key(field_match.group(1))
            value = field_match.group(2).strip()
            mapped = FIELD_ALIASES.get(key)
            if mapped:
                current_target = mapped if mapped in SECTION_KEYS else current_target
                if mapped in SECTION_KEYS:
                    if value:
                        issue.sections[mapped].append(value)
                elif mapped == "description":
                    if value:
                        issue.sections["problem"].append(value)
                elif mapped == "summary":
                    if value:
                        issue.fields[mapped] = value
                else:
                    if value and mapped not in issue.fields:
                        issue.fields[mapped] = value
                    elif value and mapped in issue.fields:
                        issue.fields[mapped] = f"{issue.fields[mapped]} {value}".strip()
                continue

        target = current_target if current_target in SECTION_KEYS else "problem"
        issue.sections[target].append(line)

    if not issue.sections["problem"]:
        fallback = issue.fields.get("summary", "").strip() or strip_issue_heading(block.strip())
        issue.sections["problem"].append(fallback)
    return issue

def normalize_choice(raw: str, options: List[str], alias_map: Dict[str, str]) -> str:
    value = (raw or "").strip()
    if not value:
        return ""
    if value in options:
        return value

    low = value.lower()
    if low in alias_map:
        return alias_map[low]
    if value in alias_map:
        return alias_map[value]

    for option in options:
        if value in option or option in value:
            return option
    return ""


def join_all_text(issue: ParsedIssue) -> str:
    parts = []
    for key in ["summary", "status", "module", "severity", "user_impact", "priority", "version", "fix_version", "sprint"]:
        if issue.fields.get(key):
            parts.append(issue.fields[key])
    for section in ["environment", "problem", "steps", "actual", "expected", "impact", "pending"]:
        parts.extend(issue.sections[section])
    return "\n".join(parts)


def normalize_summary_prefix(summary: str) -> str:
    normalized = (summary or "").strip()
    if not normalized:
        return normalized
    normalized = re.sub(r"^\[([^\[\]]+)\]", lambda match: f"\u3010{match.group(1)}\u3011", normalized)
    normalized = re.sub(r"^［([^［］]+)］", lambda match: f"\u3010{match.group(1)}\u3011", normalized)
    return normalized


def derive_summary(issue: ParsedIssue) -> str:
    explicit = normalize_summary_prefix(issue.fields.get("summary", ""))
    if explicit:
        return explicit

    source_lines = issue.sections["problem"] + issue.sections["actual"]
    for line in source_lines:
        candidate = re.sub(r"^[\-\*\d\.\)\s]+", "", line).strip(" \t\"'????")
        candidate = strip_issue_heading(candidate)
        if not candidate or ISSUE_HEADER_LINE.match(candidate):
            continue
        candidate = re.sub(r"\s+", " ", candidate)
        if len(candidate) > 120:
            candidate = candidate[:117] + "..."
        return normalize_summary_prefix(candidate)
    return "???????"

def detect_module(issue: ParsedIssue) -> Tuple[str, str]:
    explicit = normalize_choice(issue.fields.get("module", ""), MODULE_OPTIONS, {})
    if explicit:
        return explicit, ""

    text = join_all_text(issue).lower()
    best_module = "01-mom-platform"
    best_score = 0
    for module, keywords in MODULE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword.lower() in text)
        if score > best_score:
            best_score = score
            best_module = module

    if best_score == 0:
        return best_module, "模块无法从素材中明确识别，已按默认值 01-mom-platform 输出，请确认。"
    return best_module, ""


def detect_severity(issue: ParsedIssue) -> Tuple[str, str]:
    explicit = normalize_choice(issue.fields.get("severity", ""), SEVERITY_OPTIONS, SEVERITY_ALIAS)
    if explicit:
        return explicit, ""

    text = join_all_text(issue)
    if re.search(r"建议|优化|改进|易用性|拓展延伸|新需求|希望支持", text, re.IGNORECASE):
        return "建议", ""
    if re.search(r"操作系统.*(挂起|崩溃)|蓝屏|系统级崩溃|os crash", text, re.IGNORECASE):
        return "一级", ""
    if re.search(r"软件.*(挂起|崩溃)|应用.*(挂起|崩溃)|系统.*(挂起|崩溃|闪退|卡死|冻结|非法退出)|闪退|非法退出|卡死|冻结", text, re.IGNORECASE):
        return "二级", ""
    if re.search(r"不能完成|无法完成|无法(提交|保存|新增|创建|删除|查询|执行|登录|下单|审核|审批|发布)|功能未实现|主流程失败|核心流程失败", text, re.IGNORECASE):
        return "三级", ""
    if re.search(r"边界|异常输入|非正常输入|空值|超长|非法字符|格式约束|数据边界", text, re.IGNORECASE):
        return "五级", ""
    if re.search(r"文本|文案|错别字|显示|布局|样式|UI|界面字符|提示信息", text, re.IGNORECASE):
        return "六级", ""
    if re.search(r"报错|异常|超时|失败|状态错误|功能错误|兼容", text, re.IGNORECASE):
        return "四级", ""
    return "三级", "缺陷严重程度未明确，已按默认值 三级 输出，请确认。"


def detect_user_impact(issue: ParsedIssue) -> Tuple[str, str]:
    explicit = normalize_choice(issue.fields.get("user_impact", ""), IMPACT_OPTIONS, IMPACT_ALIAS)
    if explicit:
        return explicit, ""

    text = join_all_text(issue)
    if re.search(r"无影响|不影响", text, re.IGNORECASE):
        return "无", ""
    if re.search(r"全部用户|大面积|无法使用|阻塞|中断|停摆", text, re.IGNORECASE):
        return "高", ""
    if re.search(r"部分用户|部分流程|影响效率|偶发", text, re.IGNORECASE):
        return "中", ""
    if re.search(r"低频|边缘|可绕过|影响较小", text, re.IGNORECASE):
        return "低", ""
    return "中", "对用户的影响程度未明确，已按默认值 中 输出，请确认。"


def detect_priority(issue: ParsedIssue, severity: str, user_impact: str) -> Tuple[str, str]:
    explicit = normalize_choice(issue.fields.get("priority", ""), PRIORITY_OPTIONS, PRIORITY_ALIAS)
    if explicit:
        return explicit, ""

    text = join_all_text(issue)
    if re.search(r"暂停|暂缓|暂不处理", text, re.IGNORECASE):
        return "P3-不重要不紧急(80)", "历史缺陷管理定义中存在“暂停”优先级，但当前 CSV 枚举不支持，已临时按 P3 输出，请人工确认。"
    if re.search(r"阻碍开发|阻碍测试|阻塞|停摆|系统性故障|系统无法执行|崩溃|冻结|死循环|死机|非法退出|数据库链接错误|严重数据计算错误|通讯错误|通信错误", text, re.IGNORECASE):
        return "P0-重要紧急(120)", ""
    if re.search(r"模块功能错误|功能未实现|乱码|链接模块有误|基本按键使用有误|用户数据丢失|数据丢失|数据破坏|计算有误|保存有误|严重错误", text, re.IGNORECASE):
        return "P1-重要不紧急(100)", ""
    if re.search(r"优化建议|易用性|显示不恰当|页面优化|提示文案优化|更好的实现方式|拓展延伸|新需求", text, re.IGNORECASE):
        return "P3-不重要不紧急(80)", ""
    if re.search(r"次要功能|不影响用户使用|界面图表|界面字符|提示信息错误|辅助说明不清|边界|格式约束未实现|需求不一致|一般性错误|不影响操作", text, re.IGNORECASE):
        return "P2-紧急不重要(100)", ""
    if severity in {"一级", "二级"}:
        return "P0-重要紧急(120)", ""
    if severity == "三级":
        return "P1-重要不紧急(100)", ""
    if severity == "四级":
        return ("P1-重要不紧急(100)", "") if user_impact == "高" else ("P2-紧急不重要(100)", "")
    if severity in {"五级", "六级"}:
        return "P2-紧急不重要(100)", ""
    if severity == "建议" or user_impact in {"低", "无"}:
        return "P3-不重要不紧急(80)", ""
    if user_impact == "高":
        return "P1-重要不紧急(100)", ""
    if user_impact == "中":
        return "P2-紧急不重要(100)", ""
    return "P1-重要不紧急(100)", "优先级未明确，已按默认值 P1-重要不紧急(100) 输出，请确认。"


def resolve_status(issue: ParsedIssue) -> Tuple[str, str]:
    explicit = normalize_choice(issue.fields.get("status", ""), STATUS_OPTIONS, STATUS_ALIAS)
    raw_status = issue.fields.get("status", "").strip()
    if explicit:
        return explicit, ""
    if raw_status:
        return DEFAULT_STATUS, f"状态 {raw_status} 不在允许列表中，已按默认值 缺陷编制中 输出，请确认。"
    return DEFAULT_STATUS, ""


def chinese_name_to_owner(value: str) -> str:
    cleaned = re.sub(r"\s+", "", (value or "").strip())
    cleaned = cleaned.replace("?", "").replace("?", "")
    if not cleaned or lazy_pinyin is None or not CJK_NAME_RE.match(cleaned):
        return ""

    surname_len = 2 if len(cleaned) >= 3 and cleaned[:2] in COMPOUND_SURNAMES else 1
    surname = cleaned[:surname_len]
    given_name = cleaned[surname_len:]
    if not surname or not given_name:
        return ""

    surname_pinyin = "".join(lazy_pinyin(surname))
    given_name_pinyin = lazy_pinyin(given_name)
    initials = "".join(item[0] for item in given_name_pinyin if item)
    account = f"{surname_pinyin}{initials}".lower()
    return account if OWNER_RE.match(account) else ""


def sanitize_owner(value: str, label: str) -> Tuple[str, str]:
    cleaned = (value or "").strip()
    if not cleaned:
        return "", ""

    normalized = cleaned.lower()
    if OWNER_RE.match(normalized):
        return normalized, ""

    generated = chinese_name_to_owner(cleaned)
    if generated:
        return generated, ""

    return "", f"{label} {value} 不符合账号格式，需使用姓氏全拼+名字首字母，如 mayd。"


def parse_date_text(value: str) -> date | None:
    text = (value or "").strip()
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def resolve_due_date(issue: ParsedIssue, today: date, priority: str) -> str:
    explicit = parse_date_text(issue.fields.get("due_date", ""))
    if explicit:
        return explicit.strftime("%Y/%m/%d")
    offset_days = PRIORITY_DUE_DAYS.get(priority, 1)
    return (today + timedelta(days=offset_days)).strftime("%Y/%m/%d")


def resolve_version(issue: ParsedIssue, today: date) -> str:
    explicit = normalize_choice(issue.fields.get("version", ""), VERSION_OPTIONS, {})
    if explicit:
        return explicit
    if today >= VERSION_CUTOFF:
        return "KMMOM Cloud V3.5"
    return "KMMOM Cloud V3.4"

def resolve_fix_version(issue: ParsedIssue, today: date, default_fix_version: str = "") -> Tuple[str, str]:
    explicit_source = issue.fields.get("fix_version", "").strip() or default_fix_version
    explicit = normalize_choice(explicit_source, VERSION_OPTIONS, {})
    if explicit:
        return explicit, ""
    if today >= VERSION_CUTOFF:
        return "KMMOM Cloud V3.5", "当前日期已达到 2026-04-15 及之后，修复的版本默认候选值为 KMMOM Cloud V3.5；请先与用户确认。"
    return "KMMOM Cloud V3.4", ""


def resolve_sprint(issue: ParsedIssue) -> Tuple[str, str]:
    raw = issue.fields.get("sprint", "").strip()
    if not raw:
        return DEFAULT_SPRINT_ID, ""
    if raw in SPRINT_ID_TO_DISPLAY:
        return raw, ""
    if raw in SPRINT_DISPLAY_TO_ID:
        return SPRINT_DISPLAY_TO_ID[raw], ""
    for display, sprint_id in SPRINT_DISPLAY_TO_ID.items():
        if raw in display:
            return sprint_id, ""
    return DEFAULT_SPRINT_ID, f"Sprint {raw} 不在允许列表中，已按默认值 276 输出，请确认。"


def format_steps(lines: List[str]) -> str:
    clean_lines = [line.strip() for line in lines if line.strip()]
    if not clean_lines:
        return "1. 待补充"

    output: List[str] = []
    index = 1
    for line in clean_lines:
        item = re.sub(r"^[\-\*\d\.\)\s]+", "", line).strip()
        if not item:
            continue
        output.append(f"{index}. {item}")
        index += 1
    return "\n".join(output) if output else "1. 待补充"


def build_description(issue: ParsedIssue, pending_notes: List[str]) -> str:
    env_extra = "；".join([value for value in issue.sections["environment"] if value.strip()])
    environment = DEFAULT_ENV if not env_extra else f"{DEFAULT_ENV}；{env_extra}"
    problem = "\n".join(issue.sections["problem"]).strip() or "待补充"
    actual = "\n".join(issue.sections["actual"]).strip() or "待补充"
    expected = "\n".join(issue.sections["expected"]).strip() or "待补充"
    steps = format_steps(issue.sections["steps"])

    lines = [
        f"环境：{environment}",
        f"问题描述：{problem}",
        "操作步骤：",
        steps,
        f"实际结果：{actual}",
        f"期望结果：{expected}",
    ]
    return "\n".join(lines)


def build_impact(issue: ParsedIssue) -> str:
    content = "\n".join(issue.sections["impact"]).strip()
    if content:
        return content
    return "影响范围待确认（请补充受影响角色、流程与数据范围）"


def to_csv_row(
    issue: ParsedIssue,
    columns: List[str],
    today: date,
    default_owner: str = "",
    default_qa_owner: str = "",
    default_creator: str = "",
    default_fix_version: str = "",
) -> Dict[str, str]:
    pending_notes: List[str] = []

    status, status_note = resolve_status(issue)
    if status_note:
        pending_notes.append(status_note)

    module, module_note = detect_module(issue)
    if module_note:
        pending_notes.append(module_note)

    severity, severity_note = detect_severity(issue)
    if severity_note:
        pending_notes.append(severity_note)

    user_impact, impact_note = detect_user_impact(issue)
    if impact_note:
        pending_notes.append(impact_note)

    priority, priority_note = detect_priority(issue, severity, user_impact)
    if priority_note:
        pending_notes.append(priority_note)

    sprint_id, sprint_note = resolve_sprint(issue)
    if sprint_note:
        pending_notes.append(sprint_note)

    fix_version, fix_version_note = resolve_fix_version(issue, today, default_fix_version)
    if fix_version_note:
        pending_notes.append(fix_version_note)

    owner_input = issue.fields.get("owner", "").strip() or default_owner
    owner, owner_note = sanitize_owner(owner_input, "责任人")
    if owner_note:
        pending_notes.append(owner_note)

    qa_owner_input = issue.fields.get("qa_owner", "").strip() or default_qa_owner
    qa_owner, qa_note = sanitize_owner(qa_owner_input, "测试责任人")
    if qa_note:
        pending_notes.append(qa_note)

    creator_input = issue.fields.get("creator", "").strip() or default_creator
    creator, creator_note = sanitize_owner(creator_input, "缺陷产生者")
    if creator_note:
        pending_notes.append(creator_note)

    row = {
        "问题类型": DEFAULT_ISSUE_TYPE,
        "状态": status,
        "概要": derive_summary(issue),
        "优先级": priority,
        "模块": module,
        "缺陷严重程度": severity,
        "对用户的影响程度": user_impact,
        "描述": build_description(issue, pending_notes),
        "影响范围分析": build_impact(issue),
        "责任人": owner,
        "测试责任人": qa_owner,
        "缺陷产生者": creator,
        "到期日": resolve_due_date(issue, today, priority),
        "使用的版本": resolve_version(issue, today),
        "修复的版本": fix_version,
        "Sprint": sprint_id,
    }
    return {column: row.get(column, "") for column in columns}



def next_output_path(output_dir: Path, today: date) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    date_tag = today.strftime("%m-%d")
    pattern = re.compile(rf"^jira_import_\({re.escape(date_tag)}-(\d{{3}})\)\.csv$")
    max_seq = 0
    for existing in output_dir.iterdir():
        if not existing.is_file():
            continue
        match = pattern.match(existing.name)
        if match:
            max_seq = max(max_seq, int(match.group(1)))
    return output_dir / f"jira_import_({date_tag}-{max_seq + 1:03d}).csv"


def resolve_output_path(output_arg: str, today: date, skill_root: Path) -> Path:
    if not output_arg:
        return next_output_path(skill_root / OUTPUT_DIRNAME, today)
    candidate = Path(output_arg)
    if candidate.suffix.lower() == ".csv":
        date_tag = today.strftime("%m-%d")
        expected_pattern = re.compile(rf"^jira_import_\({re.escape(date_tag)}-\d{{3}}\)\.csv$")
        if not expected_pattern.match(candidate.name):
            raise ValueError(f"--output filename must match jira_import_({date_tag}-NNN).csv")
        return candidate
    return next_output_path(candidate, today)
def load_columns(template_path: Path) -> List[str]:
    if not template_path.exists():
        return list(DEFAULT_COLUMNS)
    with template_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration:
            return list(DEFAULT_COLUMNS)
    clean_header = [column.strip() for column in header if column.strip()]
    return clean_header if clean_header else list(DEFAULT_COLUMNS)


def read_input(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.input:
        return Path(args.input).read_text(encoding="utf-8-sig")
    if not sys.stdin.isatty():
        return sys.stdin.read().lstrip("\ufeff")
    raise ValueError("Provide --text, --input, or stdin content.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert raw defect notes to KMMOM Jira CSV")
    parser.add_argument("--input", type=str, help="Path to UTF-8 text input")
    parser.add_argument("--text", type=str, help="Raw defect text")
    parser.add_argument("--output", type=str, default="", help="Output CSV file path or directory; default uses exports/jira_import_(MM-DD-NNN).csv")
    parser.add_argument(
        "--template",
        type=str,
        default=str(Path(__file__).resolve().parents[1] / "assets" / "jira-import-template.csv"),
        help="CSV template path for header order",
    )
    parser.add_argument("--today", type=str, default="", help="Override current system date with YYYY-MM-DD for backfill or explicit business date scenarios")
    parser.add_argument("--owner", type=str, default="", help="Fallback Jira account for 责任人 when raw notes omit it")
    parser.add_argument("--qa-owner", dest="qa_owner", type=str, default="", help="Fallback Jira account for 测试责任人 when raw notes omit it")
    parser.add_argument("--creator", type=str, default="", help="Fallback Jira account for 缺陷产生者 when raw notes omit it")
    parser.add_argument("--fix-version", dest="fix_version", type=str, default="", help="Fallback value for 修复的版本 when raw notes omit it")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        raw_text = read_input(args)
    except Exception as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 1

    blocks = split_issues(raw_text)
    if not blocks:
        print("No defect content found.", file=sys.stderr)
        return 1

    today = parse_date_text(args.today) if args.today else date.today()
    if today is None:
        print("--today must use YYYY-MM-DD.", file=sys.stderr)
        return 1
    columns = load_columns(Path(args.template))
    rows = [
        to_csv_row(
            parse_issue(block),
            columns,
            today,
            default_owner=args.owner,
            default_qa_owner=args.qa_owner,
            default_creator=args.creator,
            default_fix_version=args.fix_version,
        )
        for block in blocks
    ]

    skill_root = Path(__file__).resolve().parents[1]
    output_path = resolve_output_path(args.output, today, skill_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} issue row(s) for {TARGET_PROJECT}: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())





