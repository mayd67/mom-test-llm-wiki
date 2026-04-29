from __future__ import annotations

import os
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "raw"
WIKI_DIR = ROOT / "wiki"
TODAY = date.today().isoformat()

GROUP_OUTPUTS = {
    "产品资料": WIKI_DIR / "03_业务系统" / "MOM" / "原始资料镜像",
    "需求文档": WIKI_DIR / "03_业务系统" / "MOM" / "原始资料镜像",
    "接口资料": WIKI_DIR / "03_业务系统" / "MOM" / "原始资料镜像",
    "项目文档": WIKI_DIR / "03_业务系统" / "MOM" / "原始资料镜像",
    "截图附件": WIKI_DIR / "03_业务系统" / "MOM" / "原始资料镜像",
    "测试流程规范": WIKI_DIR / "02_测试标准&模板" / "原始资料镜像",
    "测试资料": WIKI_DIR / "02_测试标准&模板" / "原始资料镜像",
}

IGNORED_FILE_NAMES = {".gitkeep", ".gitignore"}
IGNORED_SUFFIXES = {".sample", ".idx", ".pack", ".rev"}
IGNORED_DIR_NAMES = {".git"}
LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def should_include_raw_markdown(path: Path) -> bool:
    if path.suffix.lower() != ".md":
        return False
    if any(part.lower() in IGNORED_DIR_NAMES for part in path.parts):
        return False
    if path.name.lower() in IGNORED_FILE_NAMES:
        return False
    if path.suffix.lower() in IGNORED_SUFFIXES:
        return False
    return True


def relative_posix(path: Path, start: Path) -> str:
    return path.relative_to(start).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def infer_title(raw_file: Path, content: str) -> str:
    match = TITLE_RE.search(content)
    if match:
        return match.group(1).strip()
    return raw_file.stem


def mirror_title(raw_file: Path, content: str) -> str:
    group = raw_file.relative_to(RAW_DIR).parts[0]
    return f"原始资料-{group}-{infer_title(raw_file, content)}"


def output_path_for(raw_file: Path) -> Path:
    parts = raw_file.relative_to(RAW_DIR).parts
    group = parts[0]
    output_root = GROUP_OUTPUTS[group]
    return output_root.joinpath(*parts).with_suffix(".md")


def related_wiki_pages(raw_rel: str) -> list[str]:
    pages: list[str] = []
    for page in sorted(WIKI_DIR.rglob("*.md")):
        if not page.is_file():
            continue
        if "原始资料镜像" in page.parts:
            continue
        text = read_text(page)
        if raw_rel in text:
            title_match = re.search(r"^title:\s*(.+?)\s*$", text, re.MULTILINE)
            if title_match:
                pages.append(title_match.group(1).strip().strip('"'))
                continue
            heading_match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
            pages.append(heading_match.group(1).strip() if heading_match else page.stem)
    return sorted(set(pages))[:8]


def extract_headings(content: str) -> list[str]:
    result: list[str] = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        level = len(stripped) - len(stripped.lstrip("#"))
        title = stripped[level:].strip()
        if title:
            result.append(f"{'  ' * max(level - 1, 0)}- {title}")
    return result[:120]


def shift_headings(content: str) -> str:
    lines: list[str] = []
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#"):
            indent = line[: len(line) - len(stripped)]
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped[level:].strip()
            new_level = min(6, level + 2)
            lines.append(f"{indent}{'#' * new_level} {title}")
        else:
            lines.append(line)
    return "\n".join(lines).strip()


def rewrite_links(content: str, raw_file: Path, output_path: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        prefix, target, suffix = match.groups()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        if target.startswith("<") and target.endswith(">"):
            return match.group(0)
        if target.startswith(("./", "../")):
            resolved = (raw_file.parent / target).resolve()
            if resolved.exists():
                new_target = os.path.relpath(resolved, output_path.parent).replace("\\", "/")
                return f"{prefix}{new_target}{suffix}"
        return match.group(0)

    return LINK_RE.sub(replace, content)


def render_page(raw_file: Path) -> str:
    content = read_text(raw_file)
    raw_rel = relative_posix(raw_file, ROOT)
    title = mirror_title(raw_file, content)
    headings = extract_headings(content)
    related = related_wiki_pages(raw_rel)
    output_path = output_path_for(raw_file)
    mirrored = shift_headings(rewrite_links(content, raw_file, output_path))
    tags = ["testing", "raw-source"]
    if raw_file.parts[1] == "产品资料":
        tags.append("mom")
    if raw_file.parts[1] == "需求文档":
        tags.extend(["mom", "requirement"])
    summary = f"镜像 `{raw_rel}` 的 Markdown 原始内容，供 Wiki 检索、追溯与后续结构化提炼。"

    lines = [
        "---",
        f"title: {title}",
        "type: source",
        "status: active",
        "tags:",
    ]
    for tag in tags:
        lines.append(f"  - {tag}")
    lines.extend(
        [
            f"summary: {summary}",
            "source:",
            f"  - {raw_rel}",
            f"updated: {TODAY}",
            "---",
            "",
            f"# {title}",
            "",
            "## 原始文件",
            "",
            f"- 路径：`{raw_rel}`",
            "- 说明：本页镜像 raw Markdown 原始内容，便于在 Wiki 层直接检索原文；后续结构化知识页可继续从本页提炼。",
            "",
            "## 现有 Wiki 关联",
            "",
        ]
    )
    if related:
        lines.extend(f"- [[{item}]]" for item in related)
    else:
        lines.append("- 暂无现有结构化页面直接关联")

    lines.extend(["", "## 文档结构", ""])
    if headings:
        lines.extend(headings)
    else:
        lines.append("- 未识别到 Markdown 标题层级")

    lines.extend(["", "## 原始内容镜像", "", mirrored, ""])
    return "\n".join(lines)


def write_overview(output_root: Path, group_counts: dict[str, int]) -> None:
    title = "原始资料镜像总览"
    lines = [
        "---",
        f"title: {title}",
        "type: product",
        "status: active",
        "tags:",
        "  - testing",
        "  - raw-source",
        "  - overview",
        "summary: 汇总已镜像到 Wiki 的 raw Markdown 原始资料页面。",
        "source:",
        "  - raw/",
        f"updated: {TODAY}",
        "---",
        "",
        f"# {title}",
        "",
        "## 覆盖统计",
        "",
    ]
    for group, count in sorted(group_counts.items()):
        lines.append(f"- `{group}`：{count} 页")
    lines.extend(["", "## 说明", "", "- 本目录保存 raw Markdown 的镜像页，用于提升 Wiki 层的原文可检索性。", "- 结构化知识页应继续沉淀到现有业务、测试、接口和数据字典目录中。", ""])
    (output_root / f"{title}.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    counts: dict[Path, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for raw_file in sorted(path for path in RAW_DIR.rglob("*") if path.is_file() and should_include_raw_markdown(path)):
        output_path = output_path_for(raw_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_page(raw_file), encoding="utf-8")
        group = raw_file.relative_to(RAW_DIR).parts[0]
        counts[GROUP_OUTPUTS[group]][group] += 1

    for output_root, group_counts in counts.items():
        write_overview(output_root, group_counts)

    total = sum(sum(group_counts.values()) for group_counts in counts.values())
    print(f"Mirrored {total} Markdown raw files")


if __name__ == "__main__":
    main()
