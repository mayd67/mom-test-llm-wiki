# Skills

本目录保存仓库内可直接复用的 skill 本体，以及对应的 `agents` 元数据、参考资料、脚本、模板和验证文件。

## 目录定位

- `skills/`：保存可复用能力封装，主入口始终是 `skills/<skill-name>/SKILL.md`
- `raw/`：保存原始输入资料
- `wiki/`：保存知识沉淀、专题页、规则页和长期说明
- `outputs/`：保存当前任务的实际交付物

除脚本、模板、参考资料和测试外，业务执行产物不要反向落回 `skills/`。

## 推荐结构

| 路径 | 说明 |
| --- | --- |
| `SKILL.md` | 必选入口文件，负责触发描述和执行说明 |
| `agents/openai.yaml` | UI 展示名、短描述和默认提示词 |
| `references/` | 按需读取的规则、约束、映射和流程文档 |
| `scripts/` | 需要稳定复用的脚本 |
| `assets/` | 模板、示例种子、CSV 模板等资源 |
| `tests/` | 针对复杂脚本或生成逻辑的校验 |

## 当前技能清单

| Skill | 主要职责 | 关键资源 | 默认产物或说明 |
| --- | --- | --- | --- |
| `requirement-to-testpoints` | 从需求、原型、流程图拆测试点、风险点和待确认项 | `references/testpoint-dimensions.md`、`assets/testpoint-output-template.md` | `outputs/02_测试点/测试点/` |
| `requirement-to-testcases` | 从需求材料或测试点生成模板化测试用例 | `references/testcase-rules.md`、`assets/testcase-template.md` | Markdown 工作稿进 `outputs/03_测试用例/测试用例/`，导入版 Excel 进 `outputs/03_测试用例/MeterSphere导入/` |
| `review-functional-testcases` | 按需求文档、RPD、原型、流程和测试点基线评审现有功能测试用例 | `references/review-dimensions.md`、`references/mom-testcase-review-checklist.md`、`assets/review-output-template.md` | 默认输出测试用例评审稿或问题清单，建议落到 `outputs/03_测试用例/评审/` |
| `user-manual-writer` | 生成或改写 MOM 用户操作手册、模块说明和培训稿 | `references/manual-writing-rules.md`、`assets/manual-outline-template.md` | 交付稿默认进 `outputs/05_用户操作手册/`；知识沉淀稿可进入 `wiki/` |
| `mom-business-data-generator` | 生成 MOM 主数据、资源、工艺和生产订单导入包 | `templates/`、`references/template_relationships.md`、`scripts/build_common_seed_packages.py` | `outputs/06_测试数据/`；目录内保留跨 Agent 兼容资料 |
| `defect-report-generator` | 把零散缺陷素材整理为 Jira 可导入 CSV | `references/jira-defect-rules.md`、`assets/jira-import-template.csv`、`scripts/generate_jira_csv.py` | `outputs/04_测试执行/03_缺陷导出/` |
| `test-output-placement` | 判断测试产物该进入哪个 `outputs/` 目录并规范命名 | `references/output-directory-rules.md` | 自身不产出业务文件 |
| `raw-to-wiki-ingest` | 按仓库规则把 `raw/` 新文件安全入库到 `wiki/` | `references/routing-rules.md` | 主要写入 `wiki/` 镜像页或调用 builder，不产出 `outputs/` 业务文件 |

## 维护约定

- `SKILL.md` 的 frontmatter 只保留 `name` 和 `description`；`name` 使用小写连字符命名。
- 文本文件优先使用 `UTF-8` 无 BOM；至少 `SKILL.md` 必须无 BOM，否则标准校验会失败。
- 修改 `SKILL.md` 后，同步检查 `agents/openai.yaml` 的 `display_name`、`short_description`、`default_prompt` 是否仍然匹配。
- 可复用规则优先沉淀到 `references/`；不要把一次性业务交付物、临时导出结果或过程稿放到 skill 根目录。
- `mom-business-data-generator` 当前保留 `AGENTS.md`、`CLAUDE.md`、`START_HERE.md` 等跨 Agent 兼容文件；它们是补充入口，不替代 `SKILL.md`。

## 快速校验

在 Windows 下运行校验脚本时，先打开 `UTF-8` 读取，避免本机默认 `gbk` 导致误报：

```powershell
$env:PYTHONUTF8=1
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\requirement-to-testpoints
```

如需批量校验，在 `skills/` 根目录遍历各个子目录执行同一命令即可。
