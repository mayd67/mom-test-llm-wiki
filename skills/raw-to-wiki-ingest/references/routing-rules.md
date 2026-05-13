# Routing Rules

## 目标

`raw_to_wiki_ingest.py` 不是再造一套业务整理逻辑，而是给 `raw/ -> wiki/` 提供一个统一、显式、可增量执行的入口。

它先解决三件事：

1. 当前仓库到底是旧结构还是新结构
2. 新进入 `raw/` 的文件能不能安全自动入库
3. 哪些内容应该镜像，哪些内容只应该建附件索引，哪些内容应交给现有 builder

## 结构识别

### legacy

命中条件：

- `wiki/01_MOM产品相关文档/`
- `wiki/02_HX项目资料/`

执行规则：

- 只写入自动镜像目录
- 不覆盖人工整理页
- 不调用 `scripts/sync_wiki_meta.py`

### team-template

命中条件：

- `wiki/01_通用规范/`
- `wiki/02_测试标准&模板/`
- `wiki/03_业务系统/`

执行规则：

- 可调用现有 `build_*` 脚本批量生成
- 允许最后执行 `scripts/sync_wiki_meta.py`

### mixed / unknown

执行规则：

- 停止自动写入
- 先确认仓库以后到底维护哪套 wiki 结构

## legacy 路由

### 文本文档

- `raw/需求文档/` -> `wiki/01_MOM产品相关文档/01_产品需求文档/99_原始资料镜像/`
- `raw/产品资料/` -> `wiki/01_MOM产品相关文档/02_数据模型/10_自动入库镜像/`
- `raw/接口资料/` -> `wiki/01_MOM产品相关文档/02_数据模型/10_自动入库镜像/接口资料/`
- `raw/项目文档/` -> `wiki/02_HX项目资料/99_原始资料镜像/`
- `raw/测试资料/` -> `wiki/01_MOM产品相关文档/04_测试用例/99_原始资料镜像/`
- `raw/测试流程规范/` -> `wiki/01_MOM产品相关文档/00_方法规范/99_原始资料镜像/测试流程规范/`

处理方式：

- `.md`：保留正文并提升标题层级
- `.txt/.yaml/.yml`：按文本镜像
- `.html`：抽纯文本后镜像
- `.docx`：提取段落与表格
- `.xlsx`：提取工作表与前若干行摘要

### 附件

- `.png/.jpg/.jpeg/.gif/.webp/.bmp/.mp4` 不直接搬进 wiki 正文
- 在对应自动镜像目录里生成 `附件索引.md`
- 原件继续保留在 `raw/`

## team-template 路由

根据命中的 raw 文件选择 builder：

- `raw/需求文档/` -> `scripts/build_requirements_wiki.py`
- Markdown 原文镜像 -> `scripts/build_raw_markdown_mirror.py`
- Office 原文镜像 -> `scripts/build_raw_office_mirror.py`
- 图片/视频附件索引 -> `scripts/build_raw_attachment_catalog.py`
- `raw/产品资料/km-mom-docs/` -> `scripts/build_kmmom_product_docs_wiki.py`
- `raw/产品资料/km-mom-docs/03-development/datamodel-design/` -> `scripts/build_kmmom_data_dictionary.py`
- `raw/测试资料/01_测试用例/` -> `scripts/build_test_case_wiki.py`
- 收尾同步 -> `scripts/build_wiki_coverage_matrix.py`、`scripts/sync_wiki_meta.py`

## 风险边界

- 自动入库页不是最终知识结论页
- raw 删除后默认不自动删除 wiki 镜像
- 只要输出路径上已经存在非自动页，就跳过，不覆盖
- 如果以后正式切到 team-template，应先做一次全库迁移，再放开 builder 自动写入

