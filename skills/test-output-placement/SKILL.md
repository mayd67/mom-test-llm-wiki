---
name: test-output-placement
description: Decide where testing deliverables should be stored under `outputs/`, and enforce folder, stage, and filename conventions for requirement reviews, test points, test cases, test data packages, execution records, user manuals, and archive materials. Use when Codex needs to place a newly generated artifact, reorganize an existing artifact, recommend a delivery path, or check whether a file belongs in `raw/`, `wiki/`, or a specific `outputs/` subdirectory.（用途说明：用于判断测试交付物应该放到 `outputs/` 的哪个目录，并统一测试点、测试用例、测试数据、测试执行记录、用户手册和归档材料的目录落位、阶段子目录和命名规范。适用于新增产物、迁移旧产物、检查目录是否放对、或判断资料应进入 `raw/`、`wiki/` 还是 `outputs/` 的场景。）
---

# Test Output Placement

在新增、移动或检查测试交付物时使用这个 skill。

## 工作流程

1. 识别产物属性。
- 先判断产物类型：需求评审、测试点、测试用例、测试执行、用户手册、测试数据、归档材料。
- 再判断状态：待评审、已评审、导入版、执行中、已沉淀、历史归档。
- 同时判断文件形态：Markdown、Excel、CSV、ZIP、脚本输出目录、截图集或说明页。

2. 判断三层边界。
- 先阅读 [references/output-directory-rules.md](references/output-directory-rules.md)。
- 原始输入资料放 `raw/`。
- 可长期复用的知识、方法、模板、专题页放 `wiki/`。
- 当前需求、项目或阶段的实际交付物放 `outputs/`。

3. 映射到具体目录。
- 按参考规则中的目录映射表定位到 `outputs/01_需求评审/` 到 `outputs/99_归档/`。
- 处理测试点时优先使用 `01_待评审/`、`02_已评审/`、`03_已沉淀/`。
- 处理测试用例时优先区分评审稿、定稿和 MeterSphere 导入版。
- 处理测试数据时按“一个业务场景一个子目录”组织。

4. 给出落位与命名建议。
- 默认输出“建议目录 + 建议文件名 + 放置理由”。
- 如果状态不明确，先说明假设，不要擅自把文件跨评审阶段迁移。
- 用户用中文提问时，默认输出中文。

## 执行规则

- 不在 `outputs/` 根目录直接堆放业务产物；根目录只保留 README 和标准编号目录。
- 不新增新的 `outputs/` 顶层编号目录，除非用户明确要求调整仓库结构。
- 如果文件已经生成但位置错误，优先建议迁移到正确子目录；只有在状态明确时才直接移动。
- 如果历史文件状态不清楚，先保留原处并标记待整理，或在用户确认后归档到 `99_归档/`。
- 如果一个产物同时具备“工作稿”和“导入版”，两者分目录保存，不混在同一层。

## 典型触发语

- "这个测试用例应该放哪个目录"
- "帮我规范 outputs 目录"
- "把这些产物按测试流程归位"
- "这个文件应该进 wiki 还是 outputs"
- "给这个导入包起一个符合规范的文件名"

## 配套资源

- 目录映射、状态判定和命名规则：[references/output-directory-rules.md](references/output-directory-rules.md)
