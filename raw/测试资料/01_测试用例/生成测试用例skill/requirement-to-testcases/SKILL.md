---
name: requirement-to-testcases
description: Generate structured test cases from requirement documents, wireframes, flowcharts, and existing functional test points. Use when Codex needs to turn requirement analysis material into executable test cases that directly follow the local `测试用例模版.xlsx` field layout. Also use when the user already has functional test points and wants them expanded into template-ready test cases with module path, preconditions, step rows, expected results, priority, and traceability notes.（用途说明：根据需求文档、原型图、流程图以及现有功能测试点生成结构化测试用例。当 Codex 需要将需求分析材料转换为可直接套用本地“测试用例模版.xlsx”的测试用例时使用。若用户已经有功能测试点，希望进一步展开为可执行、可导出、可追踪的模板化测试用例，也应使用。）
---

# Requirement To Testcases

在完成需求分析后、准备进入测试设计或测试执行前使用这个 skill。

## 工作流程

1. 统一输入材料。
- 读取需求文档、原型图、流程图、功能测试点或这些材料的组合。
- 如果用户已经提供了测试点，优先以测试点为主生成测试用例。
- 如果只有需求材料，没有测试点，则先按功能、异常、边界、权限、状态等维度抽出关键测试点，再继续写用例。

2. 生成测试用例。
- 先阅读 [references/testcase-rules.md](references/testcase-rules.md)。
- 将每个清晰可验证的测试点扩展成标准测试用例。
- 默认补齐模板所需字段：`用例名称`、`所属模块`、`标签`、`前置条件`、`步骤描述`、`预期结果`、`编辑模式`、`备注`、`用例状态`、`责任人`、`用例等级`。
- 对高风险主流程优先生成完整用例；对明显的异常和边界场景也要补充。

3. 输出结果。
- 默认按 [assets/testcase-template.md](assets/testcase-template.md) 输出。
- 默认对齐本地模板 [../../测试用例模版.xlsx](../../测试用例模版.xlsx) 的列结构，不再默认输出旧版“用例编号/用例标题/来源测试点/功能点”表。
- 如用户仅需要文本结果，则输出与 Excel 模板同列顺序的 Markdown 表格。
- 如用户明确要求产出文件，且工作区存在模板文件，则优先基于该模板直接生成 `.xlsx` 文件。
- 单条用例包含多步时，按模板拆成多行：首行填写共享字段，后续行仅填写 `步骤描述`、`预期结果`，其余列留空以便映射到 Excel 合并单元格效果。
- 用户用中文提问时，默认输出中文。
- 如果用户要的是“先出核心用例”，优先输出 P0/P1 的主流程和高风险异常用例。

## 用例生成规则

- 一个测试用例只覆盖一个明确目标，不要把多个验证目标塞进同一条用例。
- 将主流程、异常流程、边界场景、权限场景、状态场景分开生成。
- 步骤要可执行，避免写成抽象目标，例如“测试提交功能”。
- 预期结果要可验证，避免只写“提交成功”“系统正常”。
- `所属模块` 默认使用路径形式，例如 `/一级模块/二级模块/功能点`；若需求文档已有清晰章节，则可用 `/产品/章节/功能点`。
- `用例名称` 默认建议保留可追踪标识；如果已有测试点编号或用例编号，可拼成 `TC-001 用例标题`。
- `标签` 默认取需求名称、模块名称或文档名称；无明确标签时使用当前需求主题名。
- `编辑模式` 默认填写 `TEST`，`用例状态` 默认填写 `未开始`，`责任人` 无明确信息时留空。
- `备注` 默认承载未单独成列的追踪信息，至少包含：`来源测试点`、`场景类型`、`验证结果`；如果存在不确定规则，再补 `待确认信息`。
- 表格输出时，列顺序必须与模板保持一致；不要擅自增加额外列。

## 追问与推断规则

- 只有当材料过于模糊、无法识别测试对象时，才追问用户。
- 如果规则不完整但仍可写出初版用例，应先输出并在 `备注` 中标记 `待确认信息`。
- 不要虚构字段名、状态值、权限矩阵、接口返回或数据库逻辑。
- 如果需求中只描述了 happy path，应补出合理的异常/边界用例，但不要捏造业务规则。

## 典型触发语

- "根据这份需求生成测试用例"
- "根据原型图和测试点展开成标准测试用例"
- "把这些功能测试点转成可执行测试用例"
- "按测试用例模版输出测试用例"
- "直接生成 Excel 模版格式的测试用例"

## 配套资源

- 测试用例编写规则：[references/testcase-rules.md](references/testcase-rules.md)
- 默认输出模板：[assets/testcase-template.md](assets/testcase-template.md)
- 本地 Excel 模版：[../../测试用例模版.xlsx](../../测试用例模版.xlsx)
