---
title: 原始资料-项目文档-_index
type: manual
status: active
tags:
  - testing
  - raw
  - mirror
  - auto-ingest
summary: 自动镜像 wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/requirements/REQ-00030_制造订单完工报送ERP接口/original/_index.md，作为当前 legacy wiki 结构下的安全入库入口。
source:
  - wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/requirements/REQ-00030_制造订单完工报送ERP接口/original/_index.md
updated: 2026-05-27
---

<!-- raw-to-wiki-ingest:auto -->

# 原始资料-项目文档-_index

## 来源说明

- 原始路径：`wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/requirements/REQ-00030_制造订单完工报送ERP接口/original/_index.md`
- 目标路径：`wiki/02_HX项目资料/99_原始资料镜像/bjhx_process/02_需求与方案/requirements/REQ-00030_制造订单完工报送ERP接口/original/_index.md`
- 提取方式：`markdown`
- 说明：本页由统一入库脚本自动生成，不覆盖人工整理页。

## 原始内容镜像

## 原始材料索引

| 文件名 | 类型 | 来源 | 说明 | 收集日期 |
| ------ | ---- | ---- | ---- | -------- |
| 20260509_MOM完工报送ERP.docx | Word | 用户附件 | 原始需求说明，描述制造订单完工后报送 ERP 的业务规则与校验要求 | 2026-05-09 |
| 20260509_MOM-SAP-接口文档.xlsx | Excel | 用户附件 | SAP 接口字段映射，当前识别到工作表为“订单完工调用SAP接口” | 2026-05-09 |
| 20260509_zws_pp_jy_code_based.wsdl | WSDL | 用户附件 | SAP WebService 接口定义文件，接口名为 `ZWS_PP_JY` | 2026-05-09 |
| 20260509_订单信息推SAP事宜沟通文字版.txt | 文本 | 用户附件 | 需求沟通会议文字记录，补充自动触发、失败后手动重发、必填校验和推送数量计算口径 | 2026-05-09 |
| 20260509_订单信息推SAP事宜.wav | 音频 | 用户附件 | 需求沟通会议录音原件，用于还原会议上下文与确认细节 | 2026-05-09 |

### 当前识别结论

- 该需求当前按仓库规则归档为 `REQ-00030`。
- 当前主题先命名为“制造订单完工报送ERP接口”，后续如客户明确要求使用 `SAP` 或 `ERP` 中的固定称谓，再统一调整目录和文档标题。
- 原始材料已归档，暂未改写原件内容。
- 从新增文字记录中，已进一步识别出以下口径：
  - 自动触发时机为制造订单关联工序全部完成，若存在检验工序，则检验也需完成。
  - 接口失败后不自动重试，需在制造订单管理界面通过“发送SAP”按钮手动重发。
  - 手动发送场景当前只支持单选。
