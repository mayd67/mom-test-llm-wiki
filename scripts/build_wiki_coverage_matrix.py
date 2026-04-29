from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "raw"
WIKI_DIR = ROOT / "wiki"
OUTPUT_PATH = WIKI_DIR / "01_通用规范" / "管理制度&安全" / "原始资料入库覆盖矩阵.md"
TODAY = date.today().isoformat()

DOC_EXTENSIONS = {".md", ".docx", ".xlsx"}
ATTACHMENT_EXTENSIONS = {".png", ".jpg", ".jpeg"}
IGNORED_FILE_NAMES = {".gitkeep", ".gitignore"}
IGNORED_SUFFIXES = {".sample", ".idx", ".pack", ".rev"}
IGNORED_DIR_NAMES = {".git"}

RAW_REF_RE = re.compile(r"raw/[^\n\r`]+")
FRONTMATTER_TITLE_RE = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)
FIRST_HEADING_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")

SUMMARY_HINTS = (
    "本页为结构化摘要",
    "## 正文摘要",
    "## 文档结构",
    "## 同源相关文档",
    "## 需求摘要",
    "## 原始文档结构",
    "当前重点覆盖",
)


@dataclass
class WikiRef:
    path: Path
    title: str
    kind: str


def relative_posix(path: Path, start: Path) -> str:
    return path.relative_to(start).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_raw_ref(raw_ref: str) -> str:
    return raw_ref.replace("\\", "/").strip().rstrip("/.")


def should_include_raw_file(path: Path) -> bool:
    if any(part.lower() in IGNORED_DIR_NAMES for part in path.parts):
        return False
    if path.name.lower() in IGNORED_FILE_NAMES:
        return False
    if path.suffix.lower() in IGNORED_SUFFIXES:
        return False
    return True


def page_title(path: Path, text: str) -> str:
    match = FRONTMATTER_TITLE_RE.search(text)
    if match:
        return match.group(1).strip().strip('"')
    match = FIRST_HEADING_RE.search(text)
    if match:
        return match.group(1).strip()
    return path.stem


def page_kind(path: Path, text: str) -> str:
    hits = sum(1 for hint in SUMMARY_HINTS if hint in text)
    rel = relative_posix(path, ROOT)
    if hits >= 2:
        return "summary"
    if "产品资料库" in rel and "KMMOM产品资料-" in path.name and hits >= 1:
        return "summary"
    if "需求拆解" in path.name and "## 原始文档结构" in text:
        return "summary"
    return "structured"


def collect_wiki_refs() -> dict[str, list[WikiRef]]:
    refs: dict[str, list[WikiRef]] = defaultdict(list)
    for page in sorted(WIKI_DIR.rglob("*.md")):
        if not page.is_file() or page == OUTPUT_PATH:
            continue
        text = read_text(page)
        title = page_title(page, text)
        kind = page_kind(page, text)
        found = {normalize_raw_ref(item) for item in RAW_REF_RE.findall(text)}
        for match in LINK_RE.finditer(text):
            target = match.group(2).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (page.parent / target).resolve()
            try:
                rel = relative_posix(resolved, ROOT)
            except ValueError:
                continue
            if resolved.is_file() and rel.startswith("raw/"):
                found.add(rel)
        for item in sorted(found):
            refs[item].append(WikiRef(path=page, title=title, kind=kind))
    return refs


def coverage_status(raw_file: Path, refs: list[WikiRef]) -> str:
    extension = raw_file.suffix.lower()
    if extension in DOC_EXTENSIONS:
        if any(ref.kind == "structured" for ref in refs):
            return "已结构化"
        if refs:
            return "仅摘要/导航"
        return "未入库"
    if extension in ATTACHMENT_EXTENSIONS:
        return "附件已引用" if refs else "附件未引用"
    return "已引用" if refs else "未入库"


def status_rank(status: str) -> int:
    order = {
        "未入库": 0,
        "附件未引用": 1,
        "仅摘要/导航": 2,
        "附件已引用": 3,
        "已引用": 4,
        "已结构化": 5,
    }
    return order.get(status, 0)


def escape(text: str) -> str:
    return text.replace("|", "\\|")


def build_row(raw_file: Path, refs: list[WikiRef]) -> tuple[str, str, str, int, str, str]:
    rel = relative_posix(raw_file, ROOT)
    top_group = raw_file.relative_to(RAW_DIR).parts[0] if raw_file != RAW_DIR else "raw"
    extension = raw_file.suffix.lower() or "[none]"
    status = coverage_status(raw_file, refs)
    wiki_pages = "；".join(sorted({ref.title for ref in refs})[:3]) if refs else "-"
    return top_group, rel, extension, len(refs), status, wiki_pages


def build_summary(rows: list[tuple[str, str, str, int, str, str]]) -> dict[str, int]:
    counter = Counter(row[4] for row in rows)
    docs = [row for row in rows if row[2] in DOC_EXTENSIONS]
    attachments = [row for row in rows if row[2] in ATTACHMENT_EXTENSIONS]
    return {
        "raw_total": len(rows),
        "doc_total": len(docs),
        "attachment_total": len(attachments),
        "structured": counter["已结构化"],
        "summary_only": counter["仅摘要/导航"],
        "uncovered": counter["未入库"],
        "attachment_ref": counter["附件已引用"],
        "attachment_unref": counter["附件未引用"],
    }


def build_group_table(rows: list[tuple[str, str, str, int, str, str]]) -> list[str]:
    grouped: dict[str, list[tuple[str, str, str, int, str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row[0]].append(row)

    lines = [
        "| 来源目录 | 原始文件总数 | 可结构化文档 | 已结构化 | 仅摘要/导航 | 未入库 | 附件已引用 | 附件未引用 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for group in sorted(grouped):
        items = grouped[group]
        doc_rows = [row for row in items if row[2] in DOC_EXTENSIONS]
        lines.append(
            f"| {escape(group)} | {len(items)} | {len(doc_rows)} | "
            f"{sum(1 for row in items if row[4] == '已结构化')} | "
            f"{sum(1 for row in items if row[4] == '仅摘要/导航')} | "
            f"{sum(1 for row in items if row[4] == '未入库')} | "
            f"{sum(1 for row in items if row[4] == '附件已引用')} | "
            f"{sum(1 for row in items if row[4] == '附件未引用')} |"
        )
    return lines


def build_priority_table(rows: list[tuple[str, str, str, int, str, str]], limit: int = 80) -> list[str]:
    candidates = [row for row in rows if row[2] in DOC_EXTENSIONS and row[4] != "已结构化"]
    candidates.sort(key=lambda row: (status_rank(row[4]), row[0], row[1]))
    lines = [
        "| 状态 | 原始文件 | 类型 | Wiki引用数 | 当前命中页面 |",
        "|---|---|---|---:|---|",
    ]
    for row in candidates[:limit]:
        _, rel, extension, ref_count, status, wiki_pages = row
        lines.append(f"| {status} | `{escape(rel)}` | `{escape(extension)}` | {ref_count} | {escape(wiki_pages)} |")
    return lines


def build_doc_matrix(rows: list[tuple[str, str, str, int, str, str]]) -> list[str]:
    doc_rows = [row for row in rows if row[2] in DOC_EXTENSIONS]
    doc_rows.sort(key=lambda row: (row[0], status_rank(row[4]), row[1]))
    lines = [
        "| 来源目录 | 状态 | 原始文件 | 类型 | Wiki引用数 | 当前命中页面 |",
        "|---|---|---|---|---:|---|",
    ]
    for group, rel, extension, ref_count, status, wiki_pages in doc_rows:
        lines.append(
            f"| {escape(group)} | {status} | `{escape(rel)}` | `{escape(extension)}` | {ref_count} | {escape(wiki_pages)} |"
        )
    return lines


def build_attachment_summary(rows: list[tuple[str, str, str, int, str, str]]) -> list[str]:
    attachment_rows = [row for row in rows if row[2] in ATTACHMENT_EXTENSIONS]
    by_group_ext: dict[tuple[str, str], list[tuple[str, str, str, int, str, str]]] = defaultdict(list)
    for row in attachment_rows:
        by_group_ext[(row[0], row[2])].append(row)
    lines = [
        "| 来源目录 | 附件类型 | 总数 | 已引用 | 未引用 |",
        "|---|---|---:|---:|---:|",
    ]
    for (group, extension), items in sorted(by_group_ext.items()):
        lines.append(
            f"| {escape(group)} | `{escape(extension)}` | {len(items)} | "
            f"{sum(1 for row in items if row[4] == '附件已引用')} | "
            f"{sum(1 for row in items if row[4] == '附件未引用')} |"
        )
    return lines


def render_report(rows: list[tuple[str, str, str, int, str, str]]) -> str:
    summary = build_summary(rows)
    parts = [
        "---",
        "title: 原始资料入库覆盖矩阵",
        "type: standard",
        "status: active",
        "tags:",
        "  - testing",
        "  - knowledge-base",
        "  - governance",
        "  - coverage",
        "summary: 盘点 raw 原始资料到 wiki 结构化知识层的覆盖情况，识别仅摘要、未入库和待结构化来源。",
        "source:",
        "  - raw/",
        f"updated: {TODAY}",
        "---",
        "",
        "# 原始资料入库覆盖矩阵",
        "",
        "## 结论摘要",
        "",
        f"- 当前纳入盘点的 `raw/` 业务文件共 {summary['raw_total']} 个，其中可结构化文档 {summary['doc_total']} 个，附件 {summary['attachment_total']} 个。",
        f"- 已结构化文档 {summary['structured']} 个，仅摘要/导航 {summary['summary_only']} 个，未入库文档 {summary['uncovered']} 个。",
        f"- 附件已引用 {summary['attachment_ref']} 个，附件未引用 {summary['attachment_unref']} 个。",
        "- 已自动排除 `.git/`、`.gitkeep`、`.gitignore` 等非业务文件，避免污染入库覆盖率。",
        "",
        "## 状态口径",
        "",
        "- `已结构化`：至少存在 1 个非摘要型 Wiki 页面直接引用该原始文件。",
        "- `仅摘要/导航`：已有 Wiki 页面引用，但页面形态仍以摘要、导航、文档结构罗列为主。",
        "- `未入库`：当前未发现任何 Wiki 页面直接引用该原始文件。",
        "- `附件已引用/附件未引用`：主要针对 `.png/.jpg/.jpeg` 等附件，表示是否已被 Wiki 页面挂载或索引。",
        "",
        "## 按来源目录统计",
        "",
        *build_group_table(rows),
        "",
        "## 优先补全清单",
        "",
        *build_priority_table(rows),
        "",
        "## 可结构化文档全量矩阵",
        "",
        *build_doc_matrix(rows),
        "",
        "## 附件覆盖概览",
        "",
        *build_attachment_summary(rows),
        "",
        "## 建议动作",
        "",
        "- 先处理 `仅摘要/导航` 的文档，它们已有来源关系，最容易升级成可查询知识页。",
        "- 再处理 `未入库` 的 `.md/.docx/.xlsx` 文件，按需求、数据模型、接口、会议纪要分别建立模板。",
        "- 对图片附件按目录聚合到来源页或主题页，避免把大量截图直接堆成孤立页面。",
        "- 每次批量补全后，重新执行本脚本并同步 `wiki/index.md`，持续缩小 `仅摘要/导航` 和 `未入库` 数量。",
    ]
    return "\n".join(parts) + "\n"


def main() -> None:
    refs = collect_wiki_refs()
    rows = []
    for raw_file in sorted(path for path in RAW_DIR.rglob("*") if path.is_file() and should_include_raw_file(path)):
        rel = relative_posix(raw_file, ROOT)
        raw_refs = refs.get(rel.replace("\\", "/"), [])
        rows.append(build_row(raw_file, raw_refs))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_report(rows), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()






