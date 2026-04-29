from __future__ import annotations

import hashlib
import json
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = ROOT / "wiki"
RAW_DIR = ROOT / "raw"
INDEX_PATH = WIKI_DIR / "index.md"
LOG_PATH = WIKI_DIR / "log.md"
STATE_PATH = ROOT / ".wiki_sync_state.json"

SECTION_DESCRIPTIONS = OrderedDict(
    [
        ("01_通用规范", "组织与岗位职责、研发流程标准、管理制度与安全"),
        ("02_测试标准&模板", "测试过程规范、缺陷管理体系和可复用模板"),
        ("03_业务系统", "MOM/MES/ERP/WMS 等业务系统、模块手册、接口与数据字典"),
        ("04_技术手册", "环境运维、数据库、版本代码管理和测试工具"),
        ("05_问题沉淀库", "环境问题、线上故障复盘、高频报错和踩坑清单"),
        ("06_专项测试", "功能、接口、性能、安全等专项测试资料"),
        ("07_新人赋能", "入职学习路线、工具配置、快速上手和术语词典"),
    ]
)

RAW_DESCRIPTIONS = OrderedDict(
    [
        ("需求文档", "需求说明、变更单、评审材料"),
        ("项目文档", "项目计划、提测单、版本说明、沟通材料、治理规范"),
        ("产品资料", "产品介绍、原型图、功能说明"),
        ("接口资料", "接口文档、字段说明、对接资料"),
        ("测试资料", "历史用例、测试报告、回归清单、缺陷导出"),
        ("会议纪要", "需求评审、复盘、项目会议纪要"),
        ("截图附件", "截图、流程图、原型导出图、现场附件"),
    ]
)

IMPORTANT_PAGES = [
    "通用规范总览",
    "测试标准与模板总览",
    "LLM Wiki维护规范总览",
    "测试标准原始资料镜像总览",
    "业务系统总览",
    "MOM系统总览",
    "MOM需求分析总览",
    "MOM原始资料镜像总览",
    "接口与数据字典总览",
    "MOM接口总览",
    "MOM枚举与状态总览",
    "MOM数据模型与表字段总览",
    "KMMOM产品资料总览",
    "KMMOM计划阶段资料地图",
    "KMMOM开发阶段资料地图",
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
]

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def sha1_of_file(path: Path) -> str:
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def wiki_paths() -> list[Path]:
    return sorted(
        path
        for path in WIKI_DIR.rglob("*.md")
        if path.is_file() and not path.name.startswith(".") and path not in {INDEX_PATH, LOG_PATH}
    )


def build_state(paths: list[Path]) -> dict[str, str]:
    return {relative_path(path): sha1_of_file(path) for path in paths}


def load_state() -> dict[str, str] | None:
    if not STATE_PATH.exists():
        return None
    return json.loads(read_text(STATE_PATH))


def save_state(state: dict[str, str]) -> None:
    write_text(STATE_PATH, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def diff_states(old: dict[str, str] | None, new: dict[str, str]) -> tuple[list[str], list[str], list[str]]:
    if old is None:
        return sorted(new.keys()), [], []

    old_keys = set(old)
    new_keys = set(new)
    added = sorted(new_keys - old_keys)
    removed = sorted(old_keys - new_keys)
    modified = sorted(path for path in (old_keys & new_keys) if old[path] != new[path])
    return added, removed, modified


def first_md_in_dir(directory: Path) -> Path | None:
    direct_pages = sorted(path for path in directory.glob("*.md") if path.is_file())
    overview_pages = [path for path in direct_pages if path.stem.endswith("总览")]
    if overview_pages:
        return overview_pages[0]
    if direct_pages:
        return direct_pages[0]
    return None


def wikilink_for(path: Path) -> str:
    return f"[[{path.stem}]]"


def joined_links(paths: list[Path]) -> str:
    return "、".join(wikilink_for(path) for path in paths)


def build_index(paths: list[Path]) -> str:
    path_by_name = {path.stem: path for path in paths}
    lines: list[str] = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines.append("# Index")
    lines.append("")
    lines.append("> 本文件由 `scripts/sync_wiki_meta.py` 自动生成，用于同步 `wiki/` 目录导航。")
    lines.append(f"> 最近同步时间：{timestamp}")
    lines.append("")
    lines.append("测试工程师知识库全局导航首页。")
    lines.append("")
    lines.append("## 快速入口")
    lines.append("")
    for section_name, description in SECTION_DESCRIPTIONS.items():
        section_dir = WIKI_DIR / section_name
        overview = first_md_in_dir(section_dir) if section_dir.exists() else None
        label = wikilink_for(overview) if overview else f"`{section_name}`"
        lines.append(f"- {label}：{description}")
    lines.append("")

    lines.append("## 原始资料入口")
    lines.append("")
    for folder_name, description in RAW_DESCRIPTIONS.items():
        lines.append(f"- `raw/{folder_name}/`：{description}")
    lines.append("")

    lines.append("## 结构化知识概览")
    lines.append("")
    for section_name, description in SECTION_DESCRIPTIONS.items():
        section_dir = WIKI_DIR / section_name
        lines.append(f"### {section_name}")
        lines.append(f"- 目录说明：{description}")
        if not section_dir.exists():
            lines.append("- 当前状态：目录不存在")
            lines.append("")
            continue

        overview = first_md_in_dir(section_dir)
        if overview:
            lines.append(f"- 总览页：{wikilink_for(overview)}")

        direct_pages = sorted(
            path for path in section_dir.glob("*.md") if path.is_file() and path != overview
        )
        if direct_pages:
            lines.append(f"- 目录页面：{joined_links(direct_pages)}")

        subdirs = sorted(path for path in section_dir.iterdir() if path.is_dir())
        if subdirs:
            for subdir in subdirs:
                sub_pages = sorted(path for path in subdir.glob("*.md") if path.is_file())
                nested_dirs = sorted(path for path in subdir.iterdir() if path.is_dir())
                nested_added = False
                if sub_pages:
                    lines.append(f"- `{subdir.name}`：{joined_links(sub_pages)}")
                for nested_dir in nested_dirs:
                    nested_pages = sorted(path for path in nested_dir.glob("*.md") if path.is_file())
                    if nested_pages:
                        lines.append(f"- `{subdir.name}/{nested_dir.name}`：{joined_links(nested_pages)}")
                        nested_added = True
                if not sub_pages and not nested_added:
                    lines.append(f"- `{subdir.name}`：待补充")
        lines.append("")

    lines.append("## 当前重点页面")
    lines.append("")
    for page_name in IMPORTANT_PAGES:
        if page_name in path_by_name:
            lines.append(f"- [[{page_name}]]")
    lines.append("")

    lines.append("## 维护规则")
    lines.append("")
    lines.append("- 原始资料先入 `raw/` 的工作资料目录")
    lines.append("- 结构化知识统一进入 `wiki/`")
    lines.append("- 每次新增、修改、删除 `wiki/` 内容后，必须执行 `python scripts/sync_wiki_meta.py`")
    lines.append("- 执行同步后，需确认 `wiki/index.md` 和 `wiki/log.md` 已更新")
    lines.append("")
    return "\n".join(lines)


def split_log(text: str) -> tuple[str, str]:
    stripped = text.strip()
    if not stripped:
        return "# Wiki Log", ""
    if not stripped.startswith("# Wiki Log"):
        return "# Wiki Log", stripped
    lines = stripped.splitlines()
    header = lines[0]
    body_lines = lines[1:]
    while body_lines and body_lines[0].strip() == "":
        body_lines.pop(0)
    return header, "\n".join(body_lines).strip()


def make_log_entry(added: list[str], removed: list[str], modified: list[str], total_pages: int, initialized: bool) -> str | None:
    today = datetime.now().strftime("%Y-%m-%d")
    if initialized:
        return "\n".join(
            [
                f"## {today} sync | 初始化 wiki 元数据同步",
                "",
                f"- 扫描并建立 {total_pages} 个结构化知识页面的同步基线",
                "- 自动生成并刷新 `wiki/index.md`",
                "- 建立后续 `wiki/` 内容变更的自动日志对比基础",
            ]
        )

    if not any([added, removed, modified]):
        return None

    lines = [f"## {today} sync | wiki 内容同步", ""]
    if added:
        lines.append("- 新增页面：" + "、".join(f"`{item}`" for item in added))
    if modified:
        lines.append("- 更新页面：" + "、".join(f"`{item}`" for item in modified))
    if removed:
        lines.append("- 删除页面：" + "、".join(f"`{item}`" for item in removed))
    lines.append("- 自动刷新 `wiki/index.md` 并同步更新 `wiki/log.md`")
    lines.append(f"- 当前结构化知识页总数：{total_pages}")
    return "\n".join(lines)


def prepend_log_entry(entry: str) -> None:
    existing_text = read_text(LOG_PATH) if LOG_PATH.exists() else "# Wiki Log\n"
    header, body = split_log(existing_text)
    parts = [header, "", entry.strip()]
    if body:
        parts.extend(["", body])
    write_text(LOG_PATH, "\n".join(parts).rstrip() + "\n")


def main() -> None:
    paths = wiki_paths()
    current_state = build_state(paths)
    previous_state = load_state()
    added, removed, modified = diff_states(previous_state, current_state)

    index_content = build_index(paths)
    write_text(INDEX_PATH, index_content)

    entry = make_log_entry(
        added=added,
        removed=removed,
        modified=modified,
        total_pages=len(paths),
        initialized=previous_state is None,
    )
    if entry:
        prepend_log_entry(entry)

    save_state(current_state)


if __name__ == "__main__":
    main()



