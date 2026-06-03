from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


WORD_NAMESPACE = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
YEAR_RE = re.compile(r"^(?P<year>\d{4})\s*年$")
MONTH_RE = re.compile(r"^(?P<month>\d{1,2})月$")
DAY_RE = re.compile(r"^(?P<month>\d{1,2})月(?P<day>\d{1,2})日(?:[（(].*?[)）])?$")
SKIP_PREFIXES = ("休息", "请假", "清明假期")


def read_docx_paragraphs(docx_path: Path) -> list[str]:
    with zipfile.ZipFile(docx_path) as archive:
        xml_bytes = archive.read("word/document.xml")
    root = ET.fromstring(xml_bytes)

    paragraphs: list[str] = []
    for para in root.findall(".//w:p", WORD_NAMESPACE):
        texts = []
        for node in para.findall(".//w:t", WORD_NAMESPACE):
            if node.text:
                texts.append(node.text)
        text = "".join(texts)
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def should_skip_entry(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    return any(stripped.startswith(prefix) for prefix in SKIP_PREFIXES)


def extract_month_entries(paragraphs: list[str], target_month: str) -> list[tuple[str, str]]:
    target_year, target_month_num = target_month.split("-", 1)
    active_year = target_year
    current_date = ""
    current_parts: list[str] = []
    entries: list[tuple[str, str]] = []

    def flush_current() -> None:
        nonlocal current_date, current_parts
        if not current_date:
            return
        body = " ".join(current_parts).strip()
        if body and not should_skip_entry(body):
            entries.append((current_date, body))
        current_date = ""
        current_parts = []

    for para in paragraphs:
        year_match = YEAR_RE.match(para)
        if year_match:
            flush_current()
            active_year = year_match.group("year")
            continue

        month_match = MONTH_RE.match(para)
        if month_match:
            flush_current()
            continue

        day_match = DAY_RE.match(para)
        if day_match:
            flush_current()
            date = f"{active_year}-{int(day_match.group('month')):02d}-{int(day_match.group('day')):02d}"
            if date.startswith(f"{target_year}-{target_month_num}"):
                current_date = date
            else:
                current_date = ""
            continue

        if current_date:
            current_parts.append(para)

    flush_current()
    return entries


def build_markdown(entries: list[tuple[str, str]], issue_key: str, source_docx: Path) -> str:
    lines = [
        f"# Jira Worklog Source for {issue_key}",
        "",
        f"> Generated from {source_docx.name}",
        "",
    ]
    for date, body in entries:
        lines.extend(
            [
                f"## {date}",
                "### 总条目清单",
                f"- 【{issue_key}】{body}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将中文日期的 Word 工作日志转换为 Jira worklog skill 可读的 Markdown")
    parser.add_argument("--docx", required=True, help="Word 日志路径")
    parser.add_argument("--month", required=True, help="目标月份，格式 YYYY-MM")
    parser.add_argument("--issue-key", required=True, help="统一挂工时的 Jira issue key")
    parser.add_argument("--output", required=True, help="输出 Markdown 路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    docx_path = Path(args.docx)
    output_path = Path(args.output)

    paragraphs = read_docx_paragraphs(docx_path)
    entries = extract_month_entries(paragraphs, args.month)
    markdown = build_markdown(entries, args.issue_key, docx_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print({"ok": True, "entry_count": len(entries), "output": str(output_path)})


if __name__ == "__main__":
    main()
