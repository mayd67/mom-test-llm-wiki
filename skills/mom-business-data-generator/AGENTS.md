# AGENTS.md

## 适用范围

本文件作用于当前目录及其全部子目录。

## 这是什么

这是一套用于生成 MOM 业务数据的本地项目目录。

包含：

- `templates/` 四个 Excel 模板
- `assets/` 种子 JSON
- `scripts/` 生成与打包脚本
- `references/` 字段关系和约束文档

## 阅读顺序

1. `START_HERE.md`
2. `PORTABILITY.md`
3. `README_SHARE.md`
4. `SKILL.md`

## 默认规则

- 用户提供了最新导入模板时，必须优先使用用户提供的模板目录
- 不要直接覆盖 `templates/`；优先把最新模板复制到当前业务目录下的独立模板目录，并统一重命名为标准文件名
- 除非已明确确认 `templates/` 就是最新模板，否则生成和校验命令都显式传 `--template-dir <最新模板目录>`
- 输出默认写到工作区根目录 `outputs/06_测试数据/`
- 输出目录优先中文，推荐 `outputs/06_测试数据/<物料中文名>/<中文方案>`
- 摘要文件优先 `种子概览.json`
- `库房`、`库位` 的 `*工厂组织` 必须挂到工厂级业务组织
- 未明确要求时，默认不生成 `厂内转工` / `厂际转工`
- 编码优先短编码，如 `Eq001`、`Wc001`、`Wh001`、`Loc001`、`Mat001`、`Rt001`

## 优先使用的脚本

- `scripts/build_common_seed_packages.py`
- `scripts/generate_seed_workbooks.py`
- `scripts/organize_output_by_material_name.py`
- `scripts/build_portable_agent_package.py`

## 模板使用要求

- 导出的 Excel 必须按本次任务确认的最新模板输出
- 如果用户提供了新模板，导出结果必须与用户模板的 Sheet 和列头保持一致
- 如果模板口径与 skill 自带 `templates/` 不一致，以本次 `--template-dir` 指向模板的实际约束为准

