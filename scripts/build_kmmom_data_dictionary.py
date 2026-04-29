from __future__ import annotations

import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "raw" / "产品资料" / "km-mom-docs" / "03-development" / "datamodel-design"
WIKI_ROOT = ROOT / "wiki" / "03_业务系统" / "MOM" / "接口&数据字典"
TABLE_ROOT = WIKI_ROOT / "数据库表"
ENUM_ROOT = WIKI_ROOT / "枚举字典"
TABLE_INDEX = WIKI_ROOT / "数据库表索引.md"
ENUM_INDEX = WIKI_ROOT / "枚举字典总览.md"
STATUS_INDEX = WIKI_ROOT / "业务状态枚举索引.md"
TODAY = date.today().isoformat()

MODEL_FILE_LABELS = {
    "km-mom-platform-datamodel.md": "平台模块数据模型",
    "km-mom-mes-datamodel.md": "制造执行系统（MES）数据模型",
    "km-mom-aps-datamodel.md": "APS数据模型",
    "km-mom-bds-datamodel.md": "BDS业务数据统计模块",
    "km-mom-ems-datamodel.md": "设备管理数据模型",
    "km-mom-tms-datamodel.md": "工具工装管理数据模型",
    "km-mom-wms-datamodel.md": "仓储物料管理数据模型",
}

SECTION_RE = re.compile(r"^###\s+(.+?)\s*$")
INFO_RE = re.compile(r"\*\*(.+?):\*\*\s*(.+)")
TITLE_RE = re.compile(r"^(?:[\d.]+\s+)?(.+?)[（(]([^）)]+)[）)]$")
ENUM_REF_RE = re.compile(r"引用枚举[:：]?\s*([A-Za-z0-9_]+)")
UNIT_REF_RE = re.compile(r"引用单位[:：]?\s*([A-Za-z0-9_]+)")
OBJ_REF_RE = re.compile(r"引用([A-Za-z0-9_]+)")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def relative_posix(path: Path, start: Path) -> str:
    return path.relative_to(start).as_posix()


def sanitize_filename(name: str) -> str:
    return re.sub(r"[<>:\"/\\|?*]", "_", name)


def split_markdown_row(line: str) -> list[str]:
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    return [cell.strip() for cell in text.split("|")]


def parse_markdown_table(lines: list[str], start: int) -> tuple[list[str], list[list[str]], int]:
    header = split_markdown_row(lines[start])
    index = start + 2
    rows: list[list[str]] = []
    while index < len(lines) and lines[index].strip().startswith("|"):
        row = split_markdown_row(lines[index])
        if len(row) < len(header):
            row = row + [""] * (len(header) - len(row))
        elif len(row) > len(header):
            row = row[: len(header)]
        rows.append(row)
        index += 1
    return header, rows, index


def iter_sections(lines: list[str]) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_title: str | None = None
    current_body: list[str] = []
    for line in lines:
        match = SECTION_RE.match(line.strip())
        if match:
            if current_title is not None:
                sections.append((current_title, current_body))
            current_title = match.group(1).strip()
            current_body = []
            continue
        if current_title is not None:
            current_body.append(line)
    if current_title is not None:
        sections.append((current_title, current_body))
    return sections


def parse_title(value: str) -> tuple[str, str]:
    match = TITLE_RE.match(value.strip())
    if match:
        return match.group(1).strip(), match.group(2).strip().strip("`")
    title = re.sub(r"^[\d.]+\s+", "", value.strip())
    return title, title


def parse_info_line(line: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for part in [item.strip() for item in line.split("|") if item.strip()]:
        match = INFO_RE.match(part)
        if match:
            result[match.group(1).strip()] = match.group(2).replace("`", "").strip()
    return result


def model_output_dir(source_name: str) -> Path:
    label = MODEL_FILE_LABELS[source_name]
    safe = sanitize_filename(label)
    return TABLE_ROOT / safe


def extract_reference_sets(rows: list[list[str]]) -> tuple[list[str], list[str], list[str]]:
    enum_refs: set[str] = set()
    object_refs: set[str] = set()
    unit_refs: set[str] = set()
    for row in rows:
        desc = row[6] if len(row) > 6 else ""
        for match in ENUM_REF_RE.findall(desc):
            enum_refs.add(match)
        for match in UNIT_REF_RE.findall(desc):
            unit_refs.add(match)
        for match in OBJ_REF_RE.findall(desc):
            if match not in enum_refs and match not in unit_refs:
                object_refs.add(match)
    return sorted(enum_refs), sorted(object_refs), sorted(unit_refs)


def parse_models(file_path: Path) -> list[dict[str, object]]:
    lines = read_text(file_path).splitlines()
    models: list[dict[str, object]] = []
    for raw_title, body in iter_sections(lines):
        info_line = next((line.strip() for line in body if "**模型类型:**" in line), "")
        if not info_line:
            continue
        cn_name, code = parse_title(raw_title)
        info = parse_info_line(info_line)
        description_lines: list[str] = []
        header: list[str] = []
        rows: list[list[str]] = []
        for index, line in enumerate(body):
            if line.strip().startswith("| 属性中文名称 |"):
                header, rows, _ = parse_markdown_table(body, index)
                break
            stripped = line.strip()
            if stripped and stripped != info_line and stripped != "---":
                description_lines.append(stripped)
        table_name = info.get("表名", "")
        source_entity = info.get("源数据实体", "")
        enum_refs, object_refs, unit_refs = extract_reference_sets(rows)
        models.append(
            {
                "source_file": file_path,
                "source_rel": relative_posix(file_path, ROOT),
                "module_label": MODEL_FILE_LABELS[file_path.name],
                "cn_name": cn_name,
                "code": code,
                "title": f"{table_name}（{cn_name}）" if table_name else f"{code}（{cn_name}）",
                "table_name": table_name,
                "model_type": info.get("模型类型", "-"),
                "parent_model": info.get("父模型", "-"),
                "interfaces": info.get("接口", "-"),
                "source_entity": source_entity,
                "description": description_lines,
                "header": header,
                "rows": rows,
                "enum_refs": enum_refs,
                "object_refs": object_refs,
                "unit_refs": unit_refs,
            }
        )
    return models


def parse_enums(file_path: Path) -> list[dict[str, object]]:
    lines = read_text(file_path).splitlines()
    enums: list[dict[str, object]] = []
    for raw_title, body in iter_sections(lines):
        info_line = next((line.strip() for line in body if "**枚举编码:**" in line), "")
        if not info_line:
            continue
        cn_name, code = parse_title(raw_title)
        info = parse_info_line(info_line)
        header: list[str] = []
        rows: list[list[str]] = []
        for index, line in enumerate(body):
            if line.strip().startswith("| 值编码 |"):
                header, rows, _ = parse_markdown_table(body, index)
                break
        enums.append(
            {
                "source_file": file_path,
                "source_rel": relative_posix(file_path, ROOT),
                "cn_name": cn_name,
                "code": info.get("枚举编码", code),
                "title": f"{info.get('枚举编码', code)}（{cn_name}）",
                "description": info.get("枚举说明", cn_name),
                "header": header,
                "rows": rows,
            }
        )
    return enums


def render_table(header: list[str], rows: list[list[str]]) -> list[str]:
    if not header:
        return ["- 无结构化表格"]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * len(header)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |")
    return lines


def enum_page_title(enum_code: str, enum_name_map: dict[str, str]) -> str:
    return enum_name_map.get(enum_code, enum_code)


def render_model_page(model: dict[str, object], enum_name_map: dict[str, str]) -> str:
    required_fields = [row[0] for row in model["rows"] if len(row) > 5 and "必填" in row[5]]
    enum_fields = [row[0] for row in model["rows"] if len(row) > 3 and row[3] == "枚举"]
    linked_enums = [f"[[{enum_page_title(code, enum_name_map)}]]" for code in model["enum_refs"]]
    linked_units = [f"`{code}`" for code in model["unit_refs"]]
    linked_objects = [f"`{code}`" for code in model["object_refs"]]
    lines = [
        "---",
        f"title: {model['title']}",
        "type: business",
        "status: active",
        "tags:",
        "  - testing",
        "  - mom",
        "  - data-dictionary",
        "  - table",
        f"summary: 结构化沉淀 {model['cn_name']} 的数据库表、字段定义和引用关系。",
        "source:",
        f"  - {model['source_rel']}",
        f"updated: {TODAY}",
        "---",
        "",
        f"# {model['title']}",
        "",
        "## 模型概览",
        "",
        f"- 中文名称：{model['cn_name']}",
        f"- 模型编码：`{model['code']}`",
        f"- Table: ``{model['table_name']}``" if model['table_name'] else "- Table: -",
        f"- 模型类型：{model['model_type']}",
        f"- 父模型：{model['parent_model']}",
        f"- 接口：{model['interfaces']}",
        f"- 来源模块：{model['module_label']}",
        f"- 源数据实体：`{model['source_entity']}`" if model['source_entity'] else "- 源数据实体：-",
        f"- 原始文档：`{model['source_rel']}`",
        "",
        "## 测试关注点",
        "",
        f"- 必填字段数：{len(required_fields)}{'；' + '、'.join(required_fields[:8]) if required_fields else ''}",
        f"- 枚举字段数：{len(enum_fields)}{'；' + '、'.join(enum_fields[:8]) if enum_fields else ''}",
        f"- 对象引用数：{len(model['object_refs'])}；单位引用数：{len(model['unit_refs'])}",
        "- 回归测试时优先关注：必填约束、枚举值合法性、引用对象存在性、冗余字段回写一致性。",
        "",
        "## 字段清单",
        "",
    ]
    lines.extend(render_table(model["header"], model["rows"]))
    lines.extend(["", "## 引用关系", ""])
    lines.append(f"- 枚举：{'、'.join(linked_enums) if linked_enums else '-'}")
    lines.append(f"- 引用对象：{'、'.join(linked_objects) if linked_objects else '-'}")
    lines.append(f"- 单位引用：{'、'.join(linked_units) if linked_units else '-'}")
    if model["description"]:
        lines.extend(["", "## 说明摘要", ""])
        lines.extend(f"- {item}" for item in model["description"])
    lines.extend(["", "## 相关页面", "", "- [[接口与数据字典总览]]", "- [[数据库表索引]]"])
    return "\n".join(lines)


def render_enum_page(enum: dict[str, object], referenced_by: list[dict[str, str]]) -> str:
    lines = [
        "---",
        f"title: {enum['title']}",
        "type: business",
        "status: active",
        "tags:",
        "  - testing",
        "  - mom",
        "  - data-dictionary",
        "  - enum",
        f"summary: 结构化沉淀枚举 {enum['code']} 的取值范围和业务含义。",
        "source:",
        f"  - {enum['source_rel']}",
        f"updated: {TODAY}",
        "---",
        "",
        f"# {enum['title']}",
        "",
        "## 枚举概览",
        "",
        f"- 中文名称：{enum['cn_name']}",
        f"- 枚举编码：`{enum['code']}`",
        f"- 说明：{enum['description']}",
        f"- 原始文档：`{enum['source_rel']}`",
        "",
        "## 取值清单",
        "",
    ]
    lines.extend(render_table(enum["header"], enum["rows"]))
    lines.extend(["", "## 被引用模型", ""])
    if referenced_by:
        for item in referenced_by:
            lines.append(f"- [[{item['title']}]]：字段 `{item['field']}`")
    else:
        lines.append("- 当前未在已解析的数据模型字段中命中引用")
    lines.extend(["", "## 相关页面", "", "- [[接口与数据字典总览]]", "- [[枚举字典总览]]"])
    return "\n".join(lines)


def render_table_index(models: list[dict[str, object]]) -> str:
    counts = Counter(model["module_label"] for model in models)
    rows = sorted(models, key=lambda item: (str(item["module_label"]), str(item["table_name"]), str(item["cn_name"])))
    lines = [
        "---",
        "title: 数据库表索引",
        "type: business",
        "status: active",
        "tags:",
        "  - testing",
        "  - mom",
        "  - data-dictionary",
        "  - table",
        "summary: 汇总 KMMOM 数据模型中的数据库表、模型编码和结构化页面入口。",
        "source:",
        "  - raw/产品资料/km-mom-docs/03-development/datamodel-design/",
        f"updated: {TODAY}",
        "---",
        "",
        "# 数据库表索引",
        "",
        "## 统计",
        "",
        f"- 数据模型总数：{len(models)}",
    ]
    for module_label, count in counts.items():
        lines.append(f"- {module_label}：{count}")
    lines.extend([
        "",
        "## 表清单",
        "",
        "| 表名 | 中文名称 | 模型编码 | 来源模块 | 页面 | |",
        "|---|---|---|---|---|---|",
    ])
    for item in rows:
        lines.append(
            f"| `{item['table_name'] or '-'}` | {item['cn_name']} | `{item['code']}` | {item['module_label']} | [[{item['title']}]] | `{item['source_rel']}` |"
        )
    return "\n".join(lines)


def render_enum_index(enums: list[dict[str, object]], status_only: bool = False) -> str:
    title = "业务状态枚举索引" if status_only else "枚举字典总览"
    summary = "汇总 KMMOM 状态类枚举，便于测试状态流转与编码检索。" if status_only else "汇总 KMMOM 基础枚举及结构化页面入口。"
    source_page = "raw/产品资料/km-mom-docs/03-development/datamodel-design/basic-data/km-mom-enum.md"
    selected = []
    for item in enums:
        code = str(item["code"])
        cn_name = str(item["cn_name"])
        if status_only:
            if not ("状态" in cn_name or code.lower().endswith("status") or code.lower().endswith("state")):
                continue
        selected.append(item)
    selected.sort(key=lambda item: str(item["code"]).lower())
    lines = [
        "---",
        f"title: {title}",
        "type: business",
        "status: active",
        "tags:",
        "  - testing",
        "  - mom",
        "  - data-dictionary",
        "  - enum",
        f"summary: {summary}",
        "source:",
        f"  - {source_page}",
        f"updated: {TODAY}",
        "---",
        "",
        f"# {title}",
        "",
        "## 统计",
        "",
        f"- 枚举总数：{len(selected)}",
        "",
        "## 枚举清单",
        "",
        "| 枚举编码 | 中文名称 | 页面 | 来源 |",
        "|---|---|---|---|",
    ]
    for item in selected:
        lines.append(
            f"| `{item['code']}` | {item['cn_name']} | [[{item['title']}]] | `{item['source_rel']}` |"
        )
    return "\n".join(lines)


def main() -> None:
    model_files = [
        RAW_ROOT / name
        for name in MODEL_FILE_LABELS
        if (RAW_ROOT / name).exists()
    ]
    models: list[dict[str, object]] = []
    for file_path in model_files:
        models.extend(parse_models(file_path))

    enum_file = RAW_ROOT / "basic-data" / "km-mom-enum.md"
    enums = parse_enums(enum_file)
    enum_name_map = {str(item["code"]): str(item["title"]) for item in enums}
    enum_referenced_by: dict[str, list[dict[str, str]]] = defaultdict(list)
    for model in models:
        for row in model["rows"]:
            if len(row) < 7:
                continue
            desc = row[6]
            for code in ENUM_REF_RE.findall(desc):
                enum_referenced_by[code].append({"title": str(model["title"]), "field": (row[1] or row[0]).strip("`")})

    for model in models:
        dir_path = model_output_dir(Path(str(model["source_file"])).name)
        file_name = sanitize_filename(f"{model['title']}.md")
        write_text(dir_path / file_name, render_model_page(model, enum_name_map))

    for enum in enums:
        file_name = sanitize_filename(f"{enum['title']}.md")
        write_text(ENUM_ROOT / file_name, render_enum_page(enum, enum_referenced_by.get(str(enum["code"]), [])))

    write_text(TABLE_INDEX, render_table_index(models))
    write_text(ENUM_INDEX, render_enum_index(enums, status_only=False))
    write_text(STATUS_INDEX, render_enum_index(enums, status_only=True))
    print(f"Generated {len(models)} model pages and {len(enums)} enum pages")


if __name__ == "__main__":
    main()
