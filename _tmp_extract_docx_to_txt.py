from pathlib import Path
from docx import Document

src = Path(r"D:\06_AI协同工作\01_MOM3.0产品\10_LLM WIKI\raw\测试流程规范")
out = Path(r"D:\06_AI协同工作\01_MOM3.0产品\10_LLM WIKI\_tmp_docx_extracts")
out.mkdir(exist_ok=True)
for path in sorted(src.glob("*.docx")):
    doc = Document(path)
    lines = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            lines.append(text)
    (out / f"{path.stem}.txt").write_text("\n".join(lines), encoding="utf-8")
    print(path.stem)