# MOM 模板种子生成器交付包检查清单

## 1. 最小交付内容

至少应包含：

- `mom-template-seed-generator/` 整个目录
- `templates/` 内的四个 Excel 模板

## 2. 建议一起附带的文件

- `README_SHARE.md`
- `SKILL.md`
- `START_HERE.md`
- `PORTABILITY.md`
- `PROMPT_TEMPLATE.md`
- `AGENTS.md`
- `CLAUDE.md`
- `requirements.txt`

## 3. 打包前自检

- `templates/` 中四个模板名称未被改名
- `scripts/build_common_seed_packages.py` 可正常执行
- `scripts/generate_seed_workbooks.py` 可正常校验种子
- `README_SHARE.md` 和 `SKILL.md` 可正常打开，无乱码
- 输出口径为中文目录 + `种子概览.json`

## 4. 建议验证命令

```powershell
python scripts/build_common_seed_packages.py --list
python scripts/build_common_seed_packages.py --scenario bearing_machining_standard
python scripts/generate_seed_workbooks.py --seed assets/bearing_machining_seed.json --validate-only
```

## 5. 多 Agent 兼容附加检查

如果目标是跨工具复用，请确认交付包中已包含：

- `AGENTS.md`
- `CLAUDE.md`
- `START_HERE.md`
- `PORTABILITY.md`
- `PROMPT_TEMPLATE.md`
- `requirements.txt`
- `scripts/build_portable_agent_package.py`

## 6. 发给同事时可直接附带的话术

```text
这是 MOM 数据生成器的共享包。
请先看 START_HERE.md，再看 README_SHARE.md 和 SKILL.md。
四个模板默认在 templates/ 目录下，不要改名。
如果工具不支持自动读取指令文件，请先打开 PROMPT_TEMPLATE.md 并把内容复制到对话首轮。
```
