---
name: requirement-to-testpoints
description: Convert requirement documents, wireframes, and flowcharts into structured test point lists for requirement analysis. Use when Codex needs to extract functional, exception, boundary, data, permission, and state-transition test points from requirement materials before test case writing. Also use when the user wants requirement-phase outputs such as test point lists, requirement gaps, review questions, or obvious cross-module impact hints.（用途说明：将需求文档、原型图和流程图转换为用于需求分析的结构化测试点清单。当 Codex 需要在编写测试用例之前，从需求材料中提取功能、异常、边界、数据、权限以及状态流转等测试点时，可以使用这个 skill。当用户希望得到需求阶段的产出物时，也可以使用这个 skill，例如测试点清单、需求缺口、评审问题，或明显的跨模块影响提示。）
---

# Requirement To Testpoints

在需求分析阶段、正式编写测试用例之前使用这个 skill。

## 工作流程

1. 统一输入材料。
- 读取需求文档、原型图、流程图或混合说明材料。
- 提取模块、角色、入口、业务对象、关键动作、校验规则、状态和依赖关系。
- 如果材料覆盖多个流程，先按模块或业务流程拆开再分析。

2. 构建测试点集合。
- 先阅读 [references/testpoint-dimensions.md](references/testpoint-dimensions.md)。
- 如果需求属于制造/MES/MOM 场景，继续阅读 [references/mom-functional-testpoint-checklist.md](references/mom-functional-testpoint-checklist.md)。
- 覆盖材料中能识别出的核心测试维度。
- 将每条关键校验、业务规则和状态流转拆成独立测试点。
- 对未明确的规则，不要忽略，直接标记为 `to confirm`。

3. 输出分析结果。
- 默认按 [assets/testpoint-output-template.md](assets/testpoint-output-template.md) 输出。
- 默认输出为 Markdown 表格，清单类信息优先使用表格承载。
- 用户用中文提问时，默认输出中文。
- 默认保持在“需求分析产物”层级，不直接扩展成完整可执行测试用例，除非用户明确要求。
- 如果材料里明显能看出风险点、评审问题或跨模块影响，也一起补充。

## 拆分规则

- 尽量做到一个测试点只描述一个可验证行为。
- 像 `新增/编辑/删除` 这种混合描述应拆成多个测试点。
- 将界面校验、业务校验、权限控制、数据规则、状态流转和联动影响拆开分析。
- 面对流程图时，同时覆盖合法流转和非法流转。
- 面对原型图时，关注必填项、默认值、隐藏态、禁用态和提示反馈。
- 面对需求正文时，重点检查前置条件、触发条件、结果条件和异常处理。
- 表格输出时，一行表示一个测试点、一个风险点或一个待确认项，避免在同一单元格混入多个独立结论。

## 制造/MOM 需求补充规则

- 主数据型需求优先拆出 `查询`、`新增`、`编辑`、`删除`、`引用限制`、`共享可见性`。
- 执行型需求优先拆出 `派工`、`报工`、`报检`、`授权放开`、`审计留痕`。
- 配置型需求覆盖 `配置主体`、`匹配优先级`、`必填联动`、`最小可用配置`、`禁用态`。
- 复制或引入类需求覆盖 `复制范围`、`深拷贝/浅拷贝`、`后续修改是否同步`、`未命中时是否阻断`。
- `组织`、`工作中心`、`工序`、`质量方案`、`资质` 等跨对象规则优先拆联动测试点。
- 正文引用嵌入表格但无法解析时，输出到 `待确认信息`，不要臆造属性。

## 追问与推断规则

- 只有当材料过于单薄、连功能或动作都无法识别时，才追问用户。
- 如果需求不完整但仍可分析，就先完成分析，并明确标出假设或 `to confirm` 项。
- 不要虚构字段名、角色规则、接口行为或状态定义。

## 典型触发语

- "Turn this requirement into test points"
- "Extract test points from this wireframe"
- "Analyze this flowchart from a testing perspective"
- "List requirement risks and review questions"
- "Find missing edge cases in this requirement"

## 配套资源

- 测试点覆盖维度与拆分规则：[references/testpoint-dimensions.md](references/testpoint-dimensions.md)
- 制造/MES/MOM 功能测试点补充清单：[references/mom-functional-testpoint-checklist.md](references/mom-functional-testpoint-checklist.md)
- 默认输出模板：[assets/testpoint-output-template.md](assets/testpoint-output-template.md)
