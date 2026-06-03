---
title: 原始资料-项目文档-README
type: manual
status: active
tags:
  - testing
  - raw
  - mirror
  - auto-ingest
summary: 自动镜像 wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/datamodels/README.md，作为当前 legacy wiki 结构下的安全入库入口。
source:
  - wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/datamodels/README.md
updated: 2026-05-27
---

<!-- raw-to-wiki-ingest:auto -->

# 原始资料-项目文档-README

## 来源说明

- 原始路径：`wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/datamodels/README.md`
- 目标路径：`wiki/02_HX项目资料/99_原始资料镜像/bjhx_process/02_需求与方案/datamodels/README.md`
- 提取方式：`markdown`
- 说明：本页由统一入库脚本自动生成，不覆盖人工整理页。

## 原始内容镜像

## 数据模型目录说明

本目录用于统一管理需求编制过程中涉及的数据模型资料，区分产品标准数据模型与项目数据模型，避免引用口径不一致。

### 1. 目录定位

- `product-standard/`
  - 存放产品标准数据模型的索引说明。
  - 产品标准数据模型的权威正文不在本项目目录重复维护。
- `project-extension/`
  - 存放项目级数据模型资料。
  - 包括项目系统导出的原始 `json`，以及按统一规则整理后的项目数据模型 `md` 文档。

### 2. 管理原则

- 产品标准数据模型以统一文档库中的正式文档为准，本项目只记录引用关系和使用说明，不复制标准正文。
- 项目数据模型以项目系统导出的 `json` 为原始事实来源。
- 项目数据模型的 `md` 文档为面向需求、设计、评审和 AI 使用的可读版本，其内容应来源于 `json`，不得脱离原始模型随意编写。
- 如项目模型已更新，应优先更新原始 `json`，再按规则同步更新对应 `md`。

### 3. 建议使用方式

- 编写需求文档 `2.4 数据描述` 时：
  - 产品标准模型优先引用 `product-standard/` 中说明的权威来源。
  - 项目级扩展模型优先引用 `project-extension/project-datamodels/` 中的可读文档。
- 如发现 `project-datamodels/` 与 `source-json/` 不一致，应以 `source-json/` 为准，并重新整理对应 `md`。

### 4. 目录结构

```text
datamodels/
├─ README.md
├─ product-standard/
│  └─ README.md
└─ project-extension/
   ├─ README.md
   ├─ json-to-md-rule.md
   ├─ source-json/
   └─ project-datamodels/
```
