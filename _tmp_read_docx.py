from pathlib import Path
from docx import Document

root = Path(r"D:\06_AI协同工作\01_MOM3.0产品\10_LLM WIKI\raw\测试流程规范")
for path in sorted(root.glob("*.docx")):
    print(f"===== {path.name} =====")
    doc = Document(path)
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        style = para.style.name if para.style else ""
        print(f"[{style}] {text}")
    print()