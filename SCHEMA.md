# Wiki Schema

## Domain

本知识库当前聚焦 MOM 3.0 产品测试工作，覆盖以下几类核心内容：

- MOM 产品需求、设计、数据模型和操作手册
- BJHX 等项目资料的测试总览、环境风险和需求分析
- 测试点、测试用例、测试数据、缺陷管理相关方法与复用能力
- 面向测试工程师的知识导航、长期沉淀和 LLM 检索问答支撑

它不是一个抽象的“通用企业测试百科”，而是一套已经落地到 MOM 产品测试场景的 LLM Wiki。

## Root Architecture

当前仓库采用“五层结构 + 导航留痕”的组织方式：

- `raw/`：原始资料层，只保存来源，不直接承载知识结论
- `wiki/`：结构化知识层，保存面向长期复用的知识页、总览页和专题页
- `outputs/`：测试交付物层，保存评审、设计、执行和导入类产物
- `scripts/`：辅助脚本层，保存镜像构建、资料整理、覆盖检查和历史同步脚本
- `skills/`：仓库级能力层，保存可复用的 Codex skill、路由规则和 agent 元数据

与知识库导航直接相关的文件：

- `wiki/index.md`：当前知识库主导航
- `wiki/log.md`：知识库结构和内容维护日志
- `README.md`：仓库级说明
- `SCHEMA.md`：目录规则、页面规范和维护约定
- `skills/README.md`：skill 目录总览、能力清单和默认产物落位说明

## Actual Directory Schema

### raw

当前 `raw/` 主要作为证据层，实际目录包括：

- `raw/需求文档/`
- `raw/项目文档/`
- `raw/产品资料/`
- `raw/接口资料/`
- `raw/测试资料/`
- `raw/测试流程规范/`
- `raw/截图附件/`

规则：

- 原始资料优先进入 `raw/`
- 不直接在 `raw/` 中写知识结论
- 仅在需要追溯原文时，从 `wiki/` 回到 `raw/`

### wiki

当前 `wiki/` 以两个主入口组织：

- `wiki/01_MOM产品相关文档/`
- `wiki/02_HX项目资料/`

其中 `wiki/01_MOM产品相关文档/` 采用带序号目录保证导航稳定，当前规则如下：

- `00_方法规范/`：放知识库规则、测试流程、评审清单、使用指南
- `01_产品需求文档/`：放产品需求整理页，按标准功能、MOM-AI、优化需求细分
- `02_数据模型/`：放数据模型总览、模块设计地图、原始设计导航和专题页
- `03_测试点/`：放测试点模板、测试分析资料和 skill 入口页
- `04_测试用例/`：放测试用例样例、导入模板说明和 skill 入口页
- `05_产品操作手册/`：放操作手册正文和按模块整理的文档树
- `06_测试数据/`：放测试数据说明页、模板说明和 skill 入口页
- `07_缺陷管理/`：放缺陷管理说明页、Jira 规则说明和 skill 入口页

`wiki/02_HX项目资料/` 当前用于承接项目级资料，主要放：

- 项目测试总览
- 环境与风险测试关注点
- 重点需求测试分析页

### outputs

当前 `outputs/` 用于保存测试交付物，实际目录包括：

- `outputs/01_需求评审/`
- `outputs/02_测试点/`
- `outputs/03_测试用例/`
- `outputs/04_测试执行/`
- `outputs/05_用户操作手册/`
- `outputs/06_测试数据/`
- `outputs/99_归档/`

规则：

- 当前需求、当前项目、当前阶段的实际产出进入 `outputs/`
- 临时草稿可以放在对应交付目录，但长期复用规则应反哺回 `wiki/`
- skill 运行结果、导入文件、执行记录等不长期保存在 skill 目录中

## Skill Placement Rules

当前仓库统一把可复用 skill 本体保存在根目录 `skills/` 中，`wiki/` 只保留能力入口页、使用说明和业务上下文：

- 测试点 skill：放 `skills/requirement-to-testpoints/`
- 测试用例 skill：放 `skills/requirement-to-testcases/`
- 用户手册编写 skill：放 `skills/user-manual-writer/`
- 测试数据 skill：放 `skills/mom-business-data-generator/`
- 缺陷单 skill：放 `skills/defect-report-generator/`
- 交付物目录规范 skill：放 `skills/test-output-placement/`
- raw 入库编排 skill：放 `skills/raw-to-wiki-ingest/`

skill 目录可包含：

- `SKILL.md`
- `assets/`
- `references/`
- `scripts/`
- `templates/`
- `tests/`
- 兼容不同 AI 工具的辅助说明文件

不建议纳入 `wiki/` 的内容：

- skill 本体目录
- `output/`
- `exports/`
- `output_regen/`
- `raw_notes/`
- `__pycache__/`
- `.pytest_cache/`
- 纯运行缓存和一次性执行结果

## Page Conventions

### Naming

- 中文知识页可使用中文标题和中文文件名
- 目录保持当前带序号结构，避免频繁改名
- skill 包目录优先使用稳定、可复用的英文名，例如 `mom-business-data-generator`
- 新增大类目录前，应先确认是否已存在语义合适的上级目录

### Writing Style

- 一页聚焦一个明确主题
- 优先写“测试工程师怎么理解、怎么使用、怎么落地”
- 事实、结论和待确认项要区分清楚
- 能引用已有页面时，优先用 `[[wikilinks]]` 建立关联
- 不把超长原文、整包截图或过程性草稿直接堆进知识页正文

## Frontmatter Rules

当前知识页实际使用的 frontmatter 以以下结构为准：

```yaml
---
title: 页面标题
type: manual
status: active
tags:
  - testing
summary: 一句话摘要
source:
  - raw/需求文档/xxx.md
updated: YYYY-MM-DD
---
```

字段规则：

- `title`：页面标题，必须与正文主题一致
- `type`：当前知识页统一使用 `manual`
- `status`：当前知识页统一使用 `active`
- `tags`：至少包含一个能表达主题的标签
- `summary`：一句话说明页面解决什么问题
- `source`：写明来源目录、原始文件或关联知识页
- `updated`：最后更新时间，格式固定为 `YYYY-MM-DD`

如果未来要引入新的 `type` 或 `status` 值，应先更新本 `SCHEMA.md`，再批量使用。

## Placement Rules

### raw 与 wiki

以下内容必须至少在 `wiki/` 中形成可直接消费的整理页、总览页或导航页：

- 直接支撑测试分析的需求资料
- 直接支撑测试点设计的模块设计和接口设计资料
- 直接支撑测试数据准备的数据模型资料
- 可长期复用的方法、规则、模板和经验

以下内容通常保留在 `raw/`，并由 `wiki/` 提供索引或摘要：

- 超长原始需求和设计全文
- 大量截图和附件原图
- 原始导入模板或中间转换文件
- 讨论纪要、临时草稿和未定稿方案

### wiki 与 outputs

以下内容优先进入 `outputs/`：

- 当前需求的测试点初稿、已评审测试点
- 当前需求的测试用例初稿和导入文件
- 当前项目的测试执行记录、报告和缺陷统计
- 用户操作手册交付版本

以下内容适合沉淀回 `wiki/`：

- 测试流程与评审规则
- 模块级稳定测试关注点
- 长期复用的模板和示例
- skill 的说明、规则和使用入口

## Query / Retrieval Policy

- 用户直接提问时，默认优先从 `wiki/` 检索和作答
- 推荐检索路径是：`wiki/index.md` -> 对应目录总览页 -> 主题页 -> 必要时回溯 `raw/`
- 对需求、模块、接口、字段、状态、菜单、配置等问题，应优先在命中的目录分支内查找
- 对项目风险、环境约束、项目定制需求，应优先查看 `wiki/02_HX项目资料/`
- 如果 `wiki/` 内没有充分依据，应明确说明知识库缺口，而不是臆造结论
- 当 `wiki/` 与 `raw/` 存在信息差异时，应保留来源和时间信息，不静默覆盖

## Update Policy

- 新增、修改、删除 `wiki/` 结构化页面后，应同步检查 `wiki/index.md` 和 `wiki/log.md`
- 新增大类目录、调整主入口或修改主要工作流后，应同步更新 `README.md` 和 `SCHEMA.md`
- 新增 skill 或调整 skill 目录时，应同步补充对应总览页和索引入口
- 新进入 `raw/` 的资料如果要自动入库，优先通过 `python scripts/raw_to_wiki_ingest.py plan|apply|watch` 进入统一编排入口
- 在当前 `legacy` 结构下，自动入库应只写安全镜像目录，不应覆盖人工整理页
- `raw/` 中的原始资料非必要不改写；如需调整原文，应有明确理由
- 运行脚本前，应先确认脚本输出结构与当前知识库真实结构一致
- 涉及 `wiki/index.md` 自动重建的脚本，不应无检查直接覆盖当前手工维护导航

## Completion Criteria

当前知识库的结构完整性应至少满足以下要求：

- `wiki/index.md` 能导航到所有核心知识入口
- `01_MOM产品相关文档/` 下各主目录都有明确职责，不相互混放
- `02_HX项目资料/` 中项目页与产品资料页边界清晰
- 关键方法页、测试数据页、缺陷管理页都能从主导航定位
- 重要结论能通过 `source` 或关联页追溯到 `raw/`、`wiki/` 或交付物来源
- 当前阶段新增的 skill 已有总览页和放置规则，不会变成孤立目录
