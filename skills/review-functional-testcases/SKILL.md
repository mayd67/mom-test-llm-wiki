---
name: review-functional-testcases
description: Review existing functional test cases against requirement documents, RPD/PRD, wireframes, flowcharts, test point baselines, and change notes. Use when Codex needs to check whether a testcase set has correct coverage, traceability, granularity, priorities, preconditions, steps, expected results, data setup, permission/state coverage, and template compliance; identify missing, incorrect, redundant, or over-merged cases; or output review findings and revision suggestions before testcase signoff, execution, or import.（用途说明：用于按需求文档、RPD/PRD、原型图、流程图、测试点等基线评审现有功能测试用例。适用于“检查是否漏测”“检查用例是否理解错需求”“核对步骤和预期是否可执行”“检查优先级、粒度、追踪关系和模板字段是否合理”等场景。）
---

# Review Functional Testcases

在已有功能测试用例需要正式评审、联调前检查或导入前复核时使用这个 skill。

## 工作流程

1. 统一输入材料。
- 读取需求文档、RPD/PRD、原型图、流程图、测试点、测试用例工作稿或导入版 Excel。
- 若材料很大，先按模块、角色或业务流程拆分。
- 若只有测试用例没有需求基线，先说明只能做结构与可执行性检查，不能做严格覆盖评审。

2. 建立评审基线。
- 先阅读 [references/review-dimensions.md](references/review-dimensions.md)。
- 若需求属于制造/MES/MOM 场景，再阅读 [references/mom-testcase-review-checklist.md](references/mom-testcase-review-checklist.md)。
- 从基线材料中提取角色、业务对象、关键字段、状态流转、权限规则、异常处理、接口联动和验收条件。
- 若需求文档按功能描述逐节展开，必须对每个功能点继续抽取：`功能目标`、`适用角色`、`前置条件`、`触发方式/操作步骤`、`系统处理逻辑`、`输出结果`、`异常处理/边界处理`、`涉及页面/入口`、`补充说明`。
- 对 `系统处理逻辑` 中编号列出的规则，默认按“一个关键规则一个评审检查点”拆开，不要只看最终是否成功。
- 对 `异常处理/边界处理` 中列出的阻断提示、非法状态、边界值、恢复限制、跳过规则等，默认检查是否存在单独负向用例。
- 建立轻量映射：`需求/RPD章节 -> 测试点/测试用例编号`。

3. 输出评审发现。
- 发现项必须优先输出，按严重级别排序。
- 每条发现只描述一个问题，并尽量给出：依据章节、对应用例、问题类型、影响、修订建议。
- 优先关注：漏覆盖、误覆盖、多个验证目标混在一条用例、前置条件不足、步骤不可执行、预期结果不可验证、优先级失真、重复冗余、模板字段不规范。
- 对需求功能描述里写明的 `系统处理逻辑` 和 `异常处理/边界处理`，优先检查以下问题：
  - 系统处理逻辑写了多条编号规则，但测试用例只覆盖最终 happy path。
  - 异常处理写了明确提示或阻断条件，但测试用例未覆盖。
  - 输出结果写了状态变化、字段回写、重新计算、排除统计、只读锁定等结果，但测试用例没有断言。
- 如果材料不完整但能继续评审，就继续评审，并把不确定项标记为 `待确认`。
- 如果输入是本地文件，尽量给出文件路径和行号引用。

4. 需要修订时再扩展。
- 默认先出评审意见，不直接重写整套用例，除非用户明确要求修订。
- 若发现是结构性漏测，先补测试点，再补测试用例。
- 若用户要求落文件且未指定目录，默认把评审稿放到 `outputs/03_测试用例/评审/`。

## 评审规则

- 一个测试用例只验证一个明确目标，不把多个规则硬塞在同一条。
- 每条关键需求规则至少有一条对应测试用例；核心主流程通常应同时有正常和关键异常验证。
- 角色、状态、权限、异常、边界、数据规则应拆开评审，不混成一句“已覆盖”。
- 如果一个功能点的 `系统处理逻辑` 明确列了 `1. 2. 3. 4.` 这样的规则，默认不能只用一条“操作成功”用例认定已覆盖；至少要检查关键校验、关键状态变化和关键副作用是否各有落点。
- 如果一个功能点写了 `异常处理/边界处理`，默认应有对应负向或边界用例；除非该条目本身明确不在测试范围。
- 如果 `系统处理逻辑` 或 `补充说明` 写了只读字段、默认值、禁止修改、唯一性校验、不参与统计、不参与校验、直接执行无需审批、自动跳过等规则，评审时应优先检查是否存在专门断言，而不是只看页面能否操作成功。
- 前置条件只写必须满足的环境、数据和状态，不能缺关键前提。
- 步骤必须可执行，避免“测试提交功能”这种抽象写法。
- 预期结果必须可验证，避免“系统正常”“提交成功”这种空结果。
- 不要臆造字段、状态、权限矩阵、接口返回或数据库逻辑。
- 若测试用例已对齐本地模板列结构，评审时不要擅自改列，只指出问题或按用户要求修订。
- 用户明确说“review/评审”时，先出 findings，再出 open questions 或 change summary。

## 常见输出

- 测试用例评审问题清单
- 覆盖缺口清单
- 待确认问题
- 局部修订建议
- 若用户明确要求，可进一步产出修订后的测试用例草稿或导入版文件

## 典型触发语

- “评审这批功能测试用例”
- “对照需求文档和 RPD 检查测试用例是否漏测”
- “帮我 review 测试用例覆盖是否完整”
- “检查这些测试用例是否符合需求和原型”
- “按需求说明书找出测试用例问题和修订建议”
- “按功能描述里的系统处理逻辑和异常处理评审测试用例”

## 配套资源

- 通用评审维度：[references/review-dimensions.md](references/review-dimensions.md)
- MOM/MES 专项检查清单：[references/mom-testcase-review-checklist.md](references/mom-testcase-review-checklist.md)
- 默认输出模板：[assets/review-output-template.md](assets/review-output-template.md)
