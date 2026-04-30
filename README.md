# MOM 测试知识库与交付物工程

这是一个围绕 MOM 3.0 产品资料构建的本地工程，目标不是单纯存放文档，而是把原始资料整理为可检索的 Wiki、可追溯的测试分析资产，以及可复用的用户操作手册输出。

当前仓库已经形成 4 个核心分层：

- `raw/`：原始资料层，保存需求文档、产品资料、开发设计资料、截图附件等来源文件
- `wiki/`：结构化知识层，按 MOM 产品知识体系整理后的 Markdown Wiki
- `outputs/`：测试与交付产物层，保存测试点、测试用例、用户操作手册等结果文件
- `scripts/`：构建与维护脚本层，用于批量镜像、结构化整理、索引同步和覆盖检查

## 当前项目内容

当前 `wiki/` 已经围绕 `01_MOM产品相关文档` 建立主入口，主要覆盖以下内容：

- `00_方法规范/`：raw 与 wiki 分层规则、测试点/测试用例生成与评审流程、检查清单
- `01_产品需求文档/`：标准功能、MOM-AI、优化需求等需求资料整理页
- `02_数据模型/`：开发阶段数据模型、模块设计、技术设计与接口专题
- `03_测试点/`：测试点模板、测试点生成 skill 与参考资料
- `04_测试用例/`：测试用例模板、样例、导入说明与生成 skill
- `05_产品操作手册/`：按快速入门、部署运维、产品平台、核心模块、统计分析、数据模型、开发指南、智能应用等分类整理的手册内容

当前 `outputs/` 中已经存在示例产物：

- `outputs/02_测试点/01_待评审/`
- `outputs/02_测试点/02_已评审/`
- `outputs/03_测试用例/`
- `outputs/05_用户操作手册/docs/`

这意味着该仓库已经不仅是知识库底座，也已经承接了实际测试分析和文档交付工作。

## 推荐阅读入口

- `wiki/index.md`：当前 Wiki 主导航
- `wiki/log.md`：结构调整与内容维护日志
- `SCHEMA.md`：知识库分层规则、页面规范与维护原则
- `outputs/README.md`：测试交付物目录约定
- `wiki/01_MOM产品相关文档/00_方法规范/00_方法规范总览.md`：方法规范首页
- `wiki/01_MOM产品相关文档/00_方法规范/LLM WIKI操作使用指南-生成测试用例.md`：从知识库生成测试资产的使用说明

## 目录说明

```text
mom-test-llm-wiki/
├── raw/                    # 原始资料，不直接在此层做知识结论
├── wiki/                   # 结构化知识库
├── outputs/                # 测试点、测试用例、手册等交付物
├── scripts/                # 批处理与同步脚本
├── SCHEMA.md               # Wiki 规则与治理约定
└── README.md               # 项目说明
```

补充说明：

- `raw/` 保留来源证据，强调“可追溯”
- `wiki/` 面向检索、问答、导航和长期复用
- `outputs/` 面向评审、交付和版本沉淀
- `scripts/` 面向批量化治理，避免手工重复整理

## 已有脚本

当前仓库已包含以下脚本：

- `scripts/sync_wiki_meta.py`：同步 `wiki/index.md` 与 `wiki/log.md`
- `scripts/build_requirements_wiki.py`：从需求文档构建需求整理页
- `scripts/build_kmmom_product_docs_wiki.py`：构建 MOM 产品资料 Wiki
- `scripts/build_kmmom_data_dictionary.py`：整理数据字典/数据模型相关内容
- `scripts/build_raw_markdown_mirror.py`：构建原始 Markdown 镜像
- `scripts/build_raw_office_mirror.py`：构建 Office 文档镜像
- `scripts/build_raw_attachment_catalog.py`：生成原始附件目录
- `scripts/build_test_case_wiki.py`：整理测试用例相关 Wiki 内容
- `scripts/build_wiki_coverage_matrix.py`：检查 Wiki 覆盖情况
- `scripts/restructure_wiki_for_team_template.py`：用于 Wiki 结构重整

## 常用命令

```powershell
python .\scripts\sync_wiki_meta.py
python .\scripts\build_requirements_wiki.py
python .\scripts\build_kmmom_product_docs_wiki.py
python .\scripts\build_kmmom_data_dictionary.py
python .\scripts\build_raw_markdown_mirror.py
python .\scripts\build_raw_office_mirror.py
python .\scripts\build_raw_attachment_catalog.py
python .\scripts\build_test_case_wiki.py
python .\scripts\build_wiki_coverage_matrix.py
```

建议在批量新增或调整 `wiki/` 内容后，至少执行一次：

```powershell
python .\scripts\sync_wiki_meta.py
```

## 推荐工作流

### 1. 原始资料入库

- 将需求、设计、手册、附件等资料放入 `raw/`
- 保持原文件不被直接改写，优先通过镜像和整理脚本生成派生内容

### 2. 结构化整理

- 将长期复用的信息沉淀到 `wiki/`
- 对需求、数据模型、操作手册等建立总览页、专题页、导航页
- 使用方法规范中的流程与模板统一整理口径

### 3. 测试资产输出

- 从 `wiki/` 和 `raw/` 中提炼测试点
- 将已评审测试点沉淀到 `outputs/02_测试点/`
- 基于测试点继续形成测试用例并输出到 `outputs/03_测试用例/`
- 将可交付的操作说明输出到 `outputs/05_用户操作手册/`

### 4. 索引与留痕

- 变更 `wiki/` 后执行 `scripts/sync_wiki_meta.py`
- 通过 `wiki/index.md` 保持主导航可用
- 通过 `wiki/log.md` 记录关键维护动作

## 当前治理原则

- 证据优先于生成：先保证来源可追溯，再生成测试资产
- raw / wiki / outputs 分层明确：避免原始资料、结构化知识和交付物混放
- 缺口显式化：如果资料不足，优先记录缺口，不用模糊描述掩盖问题
- 先导航后扩写：优先补入口页、地图页、索引页，再补充局部主题
- 交付物反哺知识库：稳定规则、模板和经验应回写到 `wiki/`

## 适用场景

这个工程适合以下工作场景：

- 面向 MOM 3.0 产品做需求分析与测试分析
- 基于产品资料、设计文档和手册沉淀长期知识库
- 从需求文档持续生成测试点、测试用例和评审产物
- 输出面向实施、测试、培训或交付的用户操作手册
- 为本地私有化 LLM 问答、知识检索和测试协同提供资料底座

## 维护建议

- 不直接把结论写回 `raw/`
- 不把临时草稿长期堆在 `outputs/` 根目录
- 新增大批量页面后及时同步索引与日志
- 新目录命名尽量延续当前序号化结构，保证导航稳定
- 如果目录结构发生明显变化，同步更新 `README.md`、`SCHEMA.md` 与 `outputs/README.md`
