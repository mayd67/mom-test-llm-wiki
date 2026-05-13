---
name: raw-to-wiki-ingest
description: Ingest newly added raw files into wiki through a profile-aware entrypoint. Use when Codex needs to detect whether the repository is on the legacy wiki layout or the team-template layout, then plan, apply, or watch raw-to-wiki synchronization without overwriting curated manual pages. Also use when the user wants a safe auto-ingest layer that writes mirror pages, attachment indexes, and builder routes according to repository rules.（用途说明：当需要把新进入 raw 的文件按仓库规则整理进 wiki 时使用。该 skill 会先识别当前仓库使用的是旧版 wiki 结构还是 team-template 新结构，再决定是写入安全镜像目录，还是调用现有 build 脚本批量生成。适用于“统一入库入口”“自动镜像”“增量同步”“避免覆盖人工整理页”等场景。）
---

# Raw To Wiki Ingest

在“原始文件进入 `raw/` 后，需要自动按规则整理进 `wiki/`”这个场景下使用该 skill。

先读 [references/routing-rules.md](references/routing-rules.md)。

## 工作流程

1. 先识别当前 wiki 结构。
- 先执行 `python scripts/raw_to_wiki_ingest.py plan`。
- 重点看输出里的 `detected_profile`。
- 如果结果是 `legacy`，说明当前仓库仍以 `wiki/01_MOM产品相关文档/` 和 `wiki/02_HX项目资料/` 为主。
- 如果结果是 `team-template`，说明可以走 `scripts/` 下新的批量构建脚本。
- 如果结果是 `mixed` 或 `unknown`，先停下，不要自动写入。

2. 在 `legacy` 结构下执行安全入库。
- 使用 `python scripts/raw_to_wiki_ingest.py apply --incremental`。
- 该模式只写入专门的自动镜像目录，例如 `99_原始资料镜像`、`10_自动入库镜像`。
- 不要把自动入库直接写到现有人工整理页里。
- 不要在 `legacy` 模式下顺手执行 `scripts/sync_wiki_meta.py`，因为当前同步脚本面向的是新结构。

3. 在 `team-template` 结构下走批量 builder。
- `apply` 模式会根据 raw 文件类型与目录选择现有 `build_*` 脚本。
- 该模式适合已经切换到 `01_通用规范`、`02_测试标准&模板`、`03_业务系统` 这些新目录的仓库。
- builder 跑完后允许同步 `wiki/index.md` 和 `wiki/log.md`。

4. 需要持续监听时使用 `watch`。
- 使用 `python scripts/raw_to_wiki_ingest.py watch --interval 30`。
- 该模式通过轮询 `raw/` 做增量检测，适合作为本地守护或定时任务入口。
- 删除 `raw/` 文件时默认不自动删 `wiki` 镜像页，避免误删人工补充内容。

## 使用边界

- 该 skill 解决的是“原始资料先安全入库到 wiki”。
- 它不负责把镜像页自动提炼成高质量专题页、测试点、测试用例或业务结论页。
- 如果用户要的是结构化测试分析产物，应继续转到需求拆解、测试点或测试用例相关 skill。
- 如果当前仓库结构和 builder 目标结构不一致，不要强行串跑全部脚本。

## 典型触发语

- "把 raw 新文件自动整理到 wiki"
- "给 raw 到 wiki 做统一入库入口"
- "需要一个自动镜像和增量同步方案"
- "不要覆盖人工整理页，先安全入库"
- "帮我看这个仓库应该走 legacy 还是新模板 builder"

## 常用命令

- 规划：`python scripts/raw_to_wiki_ingest.py plan`
- 单次执行：`python scripts/raw_to_wiki_ingest.py apply`
- 增量执行：`python scripts/raw_to_wiki_ingest.py apply --incremental`
- 持续监听：`python scripts/raw_to_wiki_ingest.py watch --interval 30`

