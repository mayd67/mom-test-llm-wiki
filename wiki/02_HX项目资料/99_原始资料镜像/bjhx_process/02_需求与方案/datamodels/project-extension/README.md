---
title: 原始资料-项目文档-README
type: manual
status: active
tags:
  - testing
  - raw
  - mirror
  - auto-ingest
summary: 自动镜像 wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/datamodels/project-extension/README.md，作为当前 legacy wiki 结构下的安全入库入口。
source:
  - wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/datamodels/project-extension/README.md
updated: 2026-05-27
---

<!-- raw-to-wiki-ingest:auto -->

# 原始资料-项目文档-README

## 来源说明

- 原始路径：`wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/datamodels/project-extension/README.md`
- 目标路径：`wiki/02_HX项目资料/99_原始资料镜像/bjhx_process/02_需求与方案/datamodels/project-extension/README.md`
- 提取方式：`markdown`
- 说明：本页由统一入库脚本自动生成，不覆盖人工整理页。

## 原始内容镜像

## 项目数据模型说明

本目录用于管理项目级数据模型，包括对产品标准模型的项目扩展属性，以及项目新增模型。

### 1. 目录分工

- `source-json/`
  - 存放从项目系统导出的原始 `json` 数据模型文件。
  - 该目录内容是项目模型的原始事实来源。
- `project-datamodels/`
  - 存放根据 `json` 整理形成的项目数据模型 `md` 文档。
  - 该目录内容用于需求、设计、评审和 AI 阅读引用。
- `json-to-md-rule.md`
  - 规定如何将项目 `json` 数据模型转换为 `md` 文档。

### 2. 管理原则

- `source-json/` 是项目数据模型的唯一事实来源。
- `project-datamodels/` 是根据 `source-json/` 整理形成的阅读版文档，不作为独立事实源。
- 原始 `json` 与整理后的项目数据模型 `md` 应成对维护。
- 如项目系统重新导出模型，应先更新 `source-json/`，再同步更新 `project-datamodels/`。
- `project-datamodels/` 的格式应尽量与产品标准数据模型文档保持一致，便于统一阅读和引用。
- 若项目模型中同时包含“标准模型扩展属性”和“项目新增模型”，应在生成的 `md` 中分别表达，不混淆层级。
- 项目数据模型文档描述的是当前已经存在的模型和属性，不预写未来规划中的模型内容。
- 项目数据模型文档中的模型组织应优先按业务相关性排序，而非按导出顺序排序。

### 3. 使用约定

- 编写项目类需求时，涉及项目扩展属性或项目新增模型，应优先引用 `project-datamodels/` 中的文档。
- 如 `project-datamodels/` 尚未整理或信息不完整，可暂时回看 `source-json/`，但应尽快补齐对应 `md`。
- AI 在整理项目数据模型时，应先读取本目录规则文档，再执行 `json` 到 `md` 的整理。

### 4. 维护流程

1. 将项目系统最新导出的模型文件放入 `source-json/`
2. 识别本次 `json` 相对于上一版的模型和属性变化
3. 按 `json-to-md-rule.md` 更新 `project-datamodels/` 中对应文档
4. 检查模型名、属性名、关系名是否与 `source-json/` 一致
5. 检查文档是否按“标准模型扩展属性 / 项目新增模型 / 项目新增关系”正确分类
6. 检查文档是否按业务相关性完成排序
7. 如变更影响需求或设计文档，同步更新相关文档中的数据模型描述
