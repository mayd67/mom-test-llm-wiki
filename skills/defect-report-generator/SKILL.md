---
name: defect-report-generator
description: Generate Jira-importable KMMOM defect CSV files from rough bug notes, chat snippets, screenshot summaries, log summaries, or incomplete defect drafts, using the built-in company Jira defect-entry rules and template to auto-fill and validate controlled fields. Use when Codex needs to turn scattered issue material into one or more Jira defects during defect preparation, split multiple independent issues into separate CSV rows, infer allowed enum values, or produce an import-ready CSV instead of a Markdown bug report.（用途说明：当用户提供零散问题记录、聊天片段、截图摘要、日志摘要或不完整缺陷草稿，并希望按公司 Jira 缺陷录入规则整理为可导入 CSV 时使用。）
---

# Defect Report Generator

将用户随手写的问题描述、聊天片段、截图摘要、日志摘要或不完整缺陷草稿，按照内置缺陷录入规程和公司 Jira 模板整理为可直接导入 Jira 的 KMMOM 缺陷 CSV，并自动生成问题类型、状态、概要、优先级、模块、严重程度、用户影响、描述、影响范围、责任字段、到期日、使用的版本、修复的版本和 Sprint，确保字段值落在允许枚举内。

默认终点是 Jira 可导入的 CSV，不是 Markdown 缺陷单。

## 先读哪些文件

1. [references/defect-entry-checklist.md](references/defect-entry-checklist.md)
2. [references/jira-defect-rules.md](references/jira-defect-rules.md)
3. [assets/jira-import-template.csv](assets/jira-import-template.csv)
4. 如需查看完整使用与 Jira 导入流程：[references/usage-and-jira-import.md](references/usage-and-jira-import.md)

## 不可违反的规则

1. 当前 skill 默认用于缺陷编制阶段；除非用户明确给出其他流转状态，否则 `状态` 默认输出 `缺陷编制中`。
2. 缺陷描述必须客观、中性，只写事实、现象、条件、步骤、实际结果和期望结果；不写评价性结论。
3. `缺陷严重程度`、`优先级` 必须准确、客观；优先采用用户明确给值，其次按内置定义推断。
4. 一个独立问题对应一条缺陷；多个独立问题必须拆分成多行 CSV。
5. 无法确认的信息不编造：
   - 枚举字段用允许值或默认值
   - 账号字段优先取用户提供的 Jira 账号
   - 当用户输入为中文姓名时，默认按“姓氏全拼 + 名字首字母”生成 Jira 账号，例如 `李飞 -> lif`、`马雨逗 -> mayd`
   - 账号字段缺失，且无法依据中文姓名规则生成时，允许二次询问；仍未提供再留空
   - 待确认项不写入 Jira CSV 的 `描述` 字段；仅保留在原始素材或由回复单独提示
6. `暂停` 出现在历史缺陷管理定义中，但不在当前 Jira CSV 允许枚举内；遇到该值时必须追问或标为待确认，不能静默映射。

## 输出合同

1. 项目上下文固定为 `KMMOM-3(KMMOM3)`。
2. `问题类型` 固定为 `缺陷`。
3. `概要` 如包含页面/模块前缀，统一使用中文全角括号 `【】`，推荐格式为 `【页面/模块】 执行某操作后出现某异常`；若原始素材使用英文半角括号 `[]`，输出时也必须规范化为 `【】`。
4. `描述` 必须严格使用以下结构：

```text
环境：测试环境：http://192.168.30.186:32053/ant-web/#/user/login
问题描述：...
操作步骤：
1. ...
2. ...
实际结果：...
期望结果：...
```

5. `影响范围分析` 必须单独输出，不并入 `描述`。
6. 到期日按内置时限规则推算，输出格式固定为 `yyyy/MM/dd`：`当前系统日期` 为默认起算日；仅当用户明确提供业务日期或明确要求回填历史日期时，才允许传入 `--today` 覆盖。
   - `P0-重要紧急(120)` -> 缺陷提出日当日
   - `P1-重要不紧急(100)` -> `缺陷提出日 + 1D`
   - `P2-紧急不重要(100)` -> `缺陷提出日 + 3D`
   - `P3-不重要不紧急(80)` -> `缺陷提出日 + 5D`
7. `Sprint` 输出 Jira 实际值，不输出显示名；优先读取项目 Sprint 目录并按当前日期自动推荐，无法读取时才回退到静态默认值 `276`。
8. `使用的版本` 默认规则：
   - `2026-04-15` 之前 -> `KMMOM Cloud V3.4`
   - `2026-04-15`（含）之后 -> `KMMOM Cloud V3.5`

## 执行顺序

1. 先判断素材对应一条还是多条缺陷。
   - 若文本中出现多个编号标题，如 `问题1：...`、`缺陷2：...`、`bug3: ...`、`issue4: ...`，按多条缺陷拆分；标题冒号后的文本优先视为该条缺陷的概要候选。
   - 若文本中出现分隔线 `---`、`===`、`***`，按分隔线拆分为多条缺陷。
   - 若素材仅包含一个连续问题描述，且不存在明确多问题分隔标记，则按单条缺陷处理。
2. 提取显式字段；显式值优先于推断值。
3. 按内置规则推断 `优先级`、`模块`、`缺陷严重程度`、`对用户的影响程度`。
4. 对缺失值使用允许的默认值；`责任人`、`测试责任人`、`缺陷产生者` 能从中文姓名转换时直接转换，无法生成时允许留空。
   - 若用户把责任信息直接写在问题标题或正文括号里，例如 `（缺陷产生者和开发责任人是薛启宽、测试责任人是马雨逗）`，也应自动抽取为责任字段，并避免把这段元信息混入概要和问题描述。
5. 用户提供了足够素材且未明确禁止写文件时，默认直接整理 `raw_notes` 并生成 Jira CSV；若识别为多条缺陷，则写入同一个 CSV 文件的多行，不要拆成多个 CSV，也不要为了确认“是否需要再整理成 Jira CSV”而追问。
6. 回复中同时给出精简缺陷内容和实际生成文件路径；若写文件失败，再退回内联 CSV 文本。

## 默认调用脚本

用户提供了可整理的缺陷素材时，默认调用脚本直接生成可导入文件；仅当用户明确要求“只要文本，不落文件”时，才只输出文本内容。默认不要传 `--today`，文件名日期、到期日计算、版本默认值判断都应使用脚本执行时的当前系统日期。

```bash
python scripts/generate_jira_csv.py --input raw_notes.txt
```

默认不要手写输出文件名；直接使用脚本默认输出，让脚本在 `outputs/04_测试执行/03_缺陷导出/` 下自动生成严格符合 `jira_import_(MM-DD-NNN).csv` 的文件名，例如 `jira_import_(03-26-002).csv`。

也可直接传文本：

```bash
python scripts/generate_jira_csv.py --text "问题描述..."
```

当输入文本包含中文批量缺陷内容时，优先使用 `--input raw_notes.txt` 读取 UTF-8 文件，避免在 Windows shell 中因为控制台编码导致正文乱码。

补填责任字段时可这样调用：

```bash
python scripts/generate_jira_csv.py --input raw_notes.txt --owner zhangs --qa-owner lis --creator wangw --fix-version "KMMOM Cloud V3.4"
```

以上四个参数仅在原始素材未提供对应字段时生效。

若希望根据项目实际 Sprint 自动给出合适值，优先先读取项目 Sprint 目录：

```bash
python ../jira-defect-importer/scripts/import_jira_defects.py sprints --config ../jira-defect-importer/assets/jira-import-config.local.json --report sprint_catalog.json
python scripts/generate_jira_csv.py --input raw_notes.txt --sprint-catalog sprint_catalog.json
```

也可一步到位直接让脚本读取 Jira：

```bash
python scripts/generate_jira_csv.py --input raw_notes.txt --jira-config ../jira-defect-importer/assets/jira-import-config.local.json
```

如确需传入 `--output`，只能传目录，或传入已符合当日格式 `jira_import_(MM-DD-NNN).csv` 的完整文件名；不得再使用业务含义型自定义文件名。若未收到用户明确指定的业务日期，不得传入固定历史 `--today`。

## 何时追问

仅在以下情况追问：

1. 无法判断是一条还是多条缺陷，且会影响导入结果。
2. 用户明确要求必须补齐 `责任人`、`测试责任人`、`缺陷产生者`，但素材中缺失且无法依据中文姓名规则生成。
3. 用户明确给出的状态、优先级、模块、严重程度、影响程度、修复的版本或 Sprint 不在允许列表中。
4. 当前日期在 `2026-04-15`（含）之后，且素材未明确给出 `修复的版本`，需要先询问用户是否确认使用默认候选值 `KMMOM Cloud V3.5`。
5. 素材明确要求 `暂停` 优先级。

其他缺失信息不追问，先按规则输出；待确认项不要写入 Jira CSV 的 `描述` 字段。不要仅为了确认是否生成 Jira CSV 或是否落文件而追问。

## 资源

1. 录入摘要：[references/defect-entry-checklist.md](references/defect-entry-checklist.md)
2. 字段规则：[references/jira-defect-rules.md](references/jira-defect-rules.md)
3. CSV 模板：[assets/jira-import-template.csv](assets/jira-import-template.csv)
4. 转换脚本：[scripts/generate_jira_csv.py](scripts/generate_jira_csv.py)
5. 使用说明与 Jira 导入步骤：[references/usage-and-jira-import.md](references/usage-and-jira-import.md)
