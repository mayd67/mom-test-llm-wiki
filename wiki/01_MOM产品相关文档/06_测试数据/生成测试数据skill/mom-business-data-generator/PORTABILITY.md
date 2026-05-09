# 跨 Agent 兼容说明

## 目标

这个目录已按“脚本能力通用 + 指令文件尽量兼容”的方式整理。

## 你可以怎么理解

- “生成能力兼容”：只要 AI 工具能读取本目录文件、并执行 Python 命令，就可以复用同样的数据生成能力。
- “skill 机制兼容”：不保证每个 AI 工具都原生支持 `.codex/skills` 或同样的 auto-discovery 机制。

## 对不同工具的建议

- Codex / OpenAI Agent：优先读 `AGENTS.md` + `SKILL.md`
- Claude Code：优先读 `CLAUDE.md`
- Trae / Workbuddy / OpenClaw / 小龙虾 / 其他 Agent：建议先看 `START_HERE.md`，再把 `PROMPT_TEMPLATE.md` 作为首轮提示词

## 环境要求

- Python 3.10+
- `openpyxl`

安装命令：

```powershell
pip install -r requirements.txt
```
