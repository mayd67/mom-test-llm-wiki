---
name: jira-defect-importer
description: Create KMMOM Jira defects from normalized defect CSV rows or from rough defect notes that should first be converted to CSV with the existing defect-report-generator skill. Use when Codex needs to inspect Jira field ids, preview REST payloads, or directly create one or more MOM defects in Jira instead of stopping at CSV export.
---

# Jira Defect Importer

将规范化的 KMMOM 缺陷数据直接创建到 Jira。若用户给的是零散缺陷素材，先复用现有缺陷整理规则生成标准 CSV，再用本 skill 导入。

## 先读哪些文件

1. [references/jira-rest-mapping.md](references/jira-rest-mapping.md)
2. [assets/jira-import-config.example.json](assets/jira-import-config.example.json)
3. 若输入仍是原始缺陷记录，再读 [../defect-report-generator/SKILL.md](../defect-report-generator/SKILL.md)

## 工作流

1. 先判断输入是否已经是标准缺陷 CSV。
   - 若是 `defect-report-generator` 产出的 CSV，直接走导入流程。
   - 若是聊天片段、日志摘要、截图摘要、缺陷草稿，先调用：

```bash
python skills/defect-report-generator/scripts/generate_jira_csv.py --input raw_notes.txt
```

2. 先准备 Jira 配置文件。
   - 默认使用 [assets/jira-import-config.example.json](assets/jira-import-config.example.json) 作为模板。
   - 若需要读取项目 Sprint，请在配置中提供 `board_id`；若省略，可通过 `project_code + km_rde_db_sql_path` 自动从 `km-rde` 项目参数 SQL 里发现 `jira.boardId`。
   - 若需要切换 Jira 登录用户，可直接改配置里的 `username`，或执行脚本时追加 `--username ...` 临时覆盖。
   - 不要编造 Jira 自定义字段 ID、账号字段类型或状态流转名称。
   - 若 `模块`、`对用户的影响程度`、`Sprint` 等字段 ID 未知，先运行字段探测命令。

3. 若需要给缺陷自动推荐 Sprint，先读取项目 Sprint 目录。
   - 默认先运行：

```bash
python skills/jira-defect-importer/scripts/import_jira_defects.py sprints --config jira-import-config.json --report sprint_catalog.json
```

   - 该命令会读取项目看板 Sprint 列表，按当前日期给出 `suggested_sprint`。
   - 产出的 `sprint_catalog.json` 可直接给 `defect-report-generator --sprint-catalog` 使用。

4. 先做 dry-run，再做真实导入。
   - 默认先运行：

```bash
python skills/jira-defect-importer/scripts/import_jira_defects.py import --config jira-import-config.json --csv defects.csv --dry-run
```

   - dry-run 只构造请求体与检查遗漏字段，不写 Jira。
   - 只有当用户明确要求真正创建缺陷时，才去掉 `--dry-run`。

5. 真实导入后返回结果。
   - 返回创建成功的 Jira Key。
   - 明确列出跳过的字段、缺失的字段映射和失败原因。

## 字段探测

当 Jira 自定义字段 ID 未知时，先查询字段列表：

```bash
python skills/jira-defect-importer/scripts/import_jira_defects.py fields --config jira-import-config.json --names 模块 对用户的影响程度 Sprint 影响范围分析
```

当状态流转名称未知时，先查询某个已有缺陷的可用流转：

```bash
python skills/jira-defect-importer/scripts/import_jira_defects.py transitions --config jira-import-config.json --issue-key KMMOM3-123
```

如果要读取项目 Sprint 并给出建议值：

```bash
python skills/jira-defect-importer/scripts/import_jira_defects.py sprints --config jira-import-config.json
```

## 真实导入

确认字段映射后再执行真实导入：

```bash
python skills/jira-defect-importer/scripts/import_jira_defects.py import --config jira-import-config.json --csv defects.csv --report jira-import-report.json
```

如果只想试前几条：

```bash
python skills/jira-defect-importer/scripts/import_jira_defects.py import --config jira-import-config.json --csv defects.csv --limit 2 --dry-run
```

## 不可违反的规则

1. 不要编造 Jira 凭据、字段 ID、transition 名称或 transition ID。
2. 不要假设 CSV 里的 `状态` 可以在创建接口里直接写入。除非配置了流转映射，否则只创建，不强行改状态。
3. 对 live Jira 的写操作默认先 dry-run；只有用户明确要求真正导入时才执行。
4. 若自定义字段未映射，不要静默伪造字段；脚本会给出 warning。必要时用 `extra_fields` 补充实例特有的必填字段。
5. 若输入是原始缺陷素材，优先复用 `defect-report-generator` 的规则与脚本，不要重新发明一套缺陷整理逻辑。
6. Sprint 推荐必须优先依据项目真实 Sprint 列表和日期区间；只有无法读取时才回退到静态默认值。

## 输出合同

1. dry-run 时，回复里给出：
   - 计划导入条数
   - 每条缺陷的概要
   - 将被跳过的字段和原因
2. 真实导入时，回复里给出：
   - 成功创建的 Jira Key 列表
   - 失败条目的行号、概要和错误信息
   - 若执行了状态流转，说明流转到的目标状态
