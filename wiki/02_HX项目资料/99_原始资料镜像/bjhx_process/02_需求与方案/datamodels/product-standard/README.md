---
title: 原始资料-项目文档-README
type: manual
status: active
tags:
  - testing
  - raw
  - mirror
  - auto-ingest
summary: 自动镜像 wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/datamodels/product-standard/README.md，作为当前 legacy wiki 结构下的安全入库入口。
source:
  - wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/datamodels/product-standard/README.md
updated: 2026-05-27
---

<!-- raw-to-wiki-ingest:auto -->

# 原始资料-项目文档-README

## 来源说明

- 原始路径：`wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/datamodels/product-standard/README.md`
- 目标路径：`wiki/02_HX项目资料/99_原始资料镜像/bjhx_process/02_需求与方案/datamodels/product-standard/README.md`
- 提取方式：`markdown`
- 说明：本页由统一入库脚本自动生成，不覆盖人工整理页。

## 原始内容镜像

## 产品标准数据模型说明

本目录用于记录本项目引用的产品标准数据模型来源和使用约定，不重复保存产品标准数据模型正文。

### 1. 权威来源

产品标准数据模型的权威目录为：

`E:\lld-workspace\documents\km-mom-docs\03-development\datamodel-design`

### 2. 常用模型文档

根据当前项目需求场景，常用产品标准数据模型文档包括但不限于：

- `km-mom-mes-datamodel.md`
- `km-mom-platform-datamodel.md`
- `km-mom-aps-datamodel.md`
- `km-mom-wms-datamodel.md`
- `km-mom-bds-datamodel.md`
- `km-mom-ems-datamodel.md`
- `km-mom-tms-datamodel.md`

### 3. 使用约定

- 需求文档中引用产品标准模型时，应以正式数据模型文档中的模型名、属性名、关系名为准。
- 模型名通常使用大驼峰（`PascalCase`）。
- 属性名使用小驼峰（`camelCase`）。
- 如正式模型中存在历史命名或拼写习惯，需求文档仍应沿用正式定义，不擅自修正。
- 本目录仅用于记录来源和规则，不作为产品标准数据模型正文副本。
