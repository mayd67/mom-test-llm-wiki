# 先看这里

## 这是什么

这是一套可直接运行的 MOM 业务数据生成器。

已内置：

- `templates/` 四个 Excel 模板
- `assets/` 种子 JSON
- `scripts/` 生成和打包脚本
- `references/` 字段关系与约束文档
- `README_SHARE.md` 、`SKILL.md` 、`PORTABILITY.md` 等说明文件

## 怎么用

### 方式 1：AI 工具会自动读取指令文件

直接打开本目录，让工具先读 `AGENTS.md` 或 `CLAUDE.md`。

### 方式 2：AI 工具不会自动读取

先打开 `PROMPT_TEMPLATE.md`，把里面的提示词复制到对话首轮。

### 方式 3：手工命令行

```powershell
pip install -r requirements.txt
python scripts/build_common_seed_packages.py --list
python scripts/build_common_seed_packages.py --scenario bearing_machining_standard --template-dir .\最新模板
python scripts/build_common_seed_packages.py --scenario bicycle_assembly_standard --template-dir .\最新模板
```

## 模板使用规则

- 用户提供了最新导入模板时，必须优先使用用户提供的模板目录
- 不要直接覆盖 `templates/`
- 除非已明确确认 `templates/` 就是最新模板，否则生成和校验命令都显式传 `--template-dir <最新模板目录>`
- 导出的 Excel 必须按本次任务确认的最新模板输出

## 建议阅读顺序

1. `START_HERE.md`
2. `PORTABILITY.md`
3. `README_SHARE.md`
4. `SKILL.md`
5. `references/` 下的约束文档
