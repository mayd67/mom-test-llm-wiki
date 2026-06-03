---
title: 原始资料-项目文档-HX服务器资源
type: manual
status: active
tags:
  - testing
  - raw
  - mirror
  - auto-ingest
summary: 自动镜像 wiki/02_HX项目资料/99_原始资料/bjhx_process/05_部署与运维/deployment/HX服务器资源.md，作为当前 legacy wiki 结构下的安全入库入口。
source:
  - wiki/02_HX项目资料/99_原始资料/bjhx_process/05_部署与运维/deployment/HX服务器资源.md
updated: 2026-05-27
---

<!-- raw-to-wiki-ingest:auto -->

# 原始资料-项目文档-HX服务器资源

## 来源说明

- 原始路径：`wiki/02_HX项目资料/99_原始资料/bjhx_process/05_部署与运维/deployment/HX服务器资源.md`
- 目标路径：`wiki/02_HX项目资料/99_原始资料镜像/bjhx_process/05_部署与运维/deployment/HX服务器资源.md`
- 提取方式：`markdown`
- 说明：本页由统一入库脚本自动生成，不覆盖人工整理页。

## 原始内容镜像

4台物理服务器，编号ABCD便于叙事，每台服务器配置：
| 配置项   | 规格                                                 |
| -------- | ---------------------------------------------------- |
| CPU      | 海光C86 7375 ×2，32核心64线程，2.0GHz（兼容X86架构） |
| 内存     | 256GB                                                |
| SSD存储  | 1.92TB SSD ×2                                        |
| SATA存储 | 16TB SATA ×4（已做磁盘阵列）                         |
| 操作系统 | 麒麟V10SP3                                           |
| 部署方式 | 物理部署，不使用Docker等虚拟化技术                   |
| 网络环境 | 纯内网部署                                           |
