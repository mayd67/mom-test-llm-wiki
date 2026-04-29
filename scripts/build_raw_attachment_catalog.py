from __future__ import annotations

import os
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "raw"
WIKI_DIR = ROOT / "wiki"
TODAY = date.today().isoformat()
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
IGNORED_FILE_NAMES = {".gitkeep", ".gitignore"}
IGNORED_DIR_NAMES = {".git"}

GROUP_OUTPUTS = {
    "产品资料": WIKI_DIR / "03_业务系统" / "MOM" / "原始资料镜像",
    "需求文档": WIKI_DIR / "03_业务系统" / "MOM" / "原始资料镜像",
    "接口资料": WIKI_DIR / "03_业务系统" / "MOM" / "原始资料镜像",
    "项目文档": WIKI_DIR / "03_业务系统" / "MOM" / "原始资料镜像",
    "截图附件": WIKI_DIR / "03_业务系统" / "MOM" / "原始资料镜像",
    "测试流程规范": WIKI_DIR / "02_测试标准&模板" / "原始资料镜像",
    "测试资料": WIKI_DIR / "02_测试标准&模板" / "原始资料镜像",
}


def should_include(path: Path) -> bool:
    if path.suffix.lower() not in IMAGE_EXTENSIONS:
        return False
    if any(part.lower() in IGNORED_DIR_NAMES for part in path.parts):
        return False
    if path.name.lower() in IGNORED_FILE_NAMES:
        return False
    return True


def relative_posix(path: Path, start: Path) -> str:
    return path.relative_to(start).as_posix()


def output_path_for(raw_dir: Path) -> Path:
    parts = raw_dir.relative_to(RAW_DIR).parts
    group = parts[0]
    output_root = GROUP_OUTPUTS[group]
    return output_root.joinpath(*parts) / "附件索引.md"


def render_page(raw_dir: Path, images: list[Path]) -> str:
    raw_rel_dir = relative_posix(raw_dir, ROOT)
    title = f"原始附件索引-{raw_dir.relative_to(RAW_DIR).parts[0]}-{raw_dir.name}"
    lines = [
        "---",
        f"title: {title}",
        "type: source",
        "status: active",
        "tags:",
        "  - testing",
        "  - raw-source",
        "  - attachment",
        f"summary: 汇总 `{raw_rel_dir}` 目录下的原始图片附件，提供 Wiki 可检索入口。",
        "source:",
        f"  - {raw_rel_dir}/",
        f"updated: {TODAY}",
        "---",
        "",
        f"# {title}",
        "",
        "## 原始目录",
        "",
        f"- 路径：`{raw_rel_dir}`",
        f"- 附件数：{len(images)}",
        "- 说明：本页为图片附件索引页，保留原始附件的 Wiki 入口与文件级链接。",
        "",
        "## 附件清单",
        "",
    ]
    out_path = output_path_for(raw_dir)
    for image in images:
        target = os.path.relpath(image, out_path.parent).replace("\\", "/")
        lines.append(f"- [{image.name}]({target})")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    by_dir: dict[Path, list[Path]] = defaultdict(list)
    for image in sorted(path for path in RAW_DIR.rglob("*") if path.is_file() and should_include(path)):
        by_dir[image.parent].append(image)

    for raw_dir, images in by_dir.items():
        output_path = output_path_for(raw_dir)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_page(raw_dir, images), encoding="utf-8")

    print(f"Indexed {sum(len(images) for images in by_dir.values())} attachments across {len(by_dir)} directories")


if __name__ == "__main__":
    main()
