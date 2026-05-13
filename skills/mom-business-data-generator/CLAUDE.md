# Claude Code 使用说明

## 开始前先看

1. `START_HERE.md`
2. `PORTABILITY.md`
3. `README_SHARE.md`
4. `SKILL.md`

## 默认口径

- 模板默认在 `templates/`
- 输出默认到工作区根目录 `outputs/06_测试数据/`
- 输出名称优先中文
- 摘要文件优先 `种子概览.json`
- `库房`、`库位` 工厂组织必须挂到工厂级组织
- 未明确要求时，不生成 `厂内转工` / `厂际转工`

## 常用命令

```powershell
python scripts/build_common_seed_packages.py --list
python scripts/build_common_seed_packages.py --scenario bearing_machining_standard
python scripts/generate_seed_workbooks.py --seed assets/bearing_machining_seed.json --validate-only
python scripts/organize_output_by_material_name.py --clean
```

如果工具不会自动读取本地指令文件，请使用 `PROMPT_TEMPLATE.md`。

