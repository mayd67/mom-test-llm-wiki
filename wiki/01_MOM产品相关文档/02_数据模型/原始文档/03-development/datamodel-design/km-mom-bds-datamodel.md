# 数据模型设计 - BDS业务数据统计模块

## 文档说明

**基本信息**
- 文档版本：v1.3 | 更新日期：2026-01-22 | 维护团队：产品研发团队
- 目标受众：产品研发团队

**文档定位**

本文档定义KMMOM3.x业务数据统计（BDS，Business Data Statistics）模块的数据模型设计，包括质量履历及其关联的生产过程、实物BOM等数据模型，用于支持业务数据的统计分析、报表生成和数据可视化功能。

**内容结构**

| 章节 | 核心问题 | 内容说明 |
|------|---------|----------|
| 术语、定义和缩略语 | BDS模块的专业术语是什么？ | 定义模块内的业务术语和缩略语 |
| 数据模型 | BDS模块包含哪些数据模型？ | 定义质量履历、路径、生产过程记录、实物BOM等数据模型 |

---

## 术语、定义和缩略语

| 术语 | 定义 | 缩略语 |
|------|------|--------|
| 业务数据统计 | 对制造执行过程中产生的业务数据进行统计分析、报表生成和数据可视化的功能模块 | BDS |
| 质量履历 | 记录产品在制造全生命周期中的质量相关信息，包括生产过程、检验记录、物料追溯等 | QH |
| 实物BOM | 产品实际生产过程中使用的物料清单，记录实际装配关系和批次序列号 | - |
| 产品批次号 | 同一批次生产的产品的标识编号 | - |
| 产品序列号 | 单个产品的唯一标识编号 | - |

---

## 数据模型

### 质量履历（QualityHistory）

**模型类型:** 业务模型 | **父模型:** `VersionObject` | **接口:** `LifecycleManaged` | **表名:** `MOM_QUALITY_HISTORY`

**生命周期模板**：COMMON_LIFECYCLE

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 产品批次号 | `prodBatch` | `CPROD_BATCH` | 字符串 | 256 | 无 | 产品批次 |
| 产品序列号 | `prodSn` | `CPROD_SN` | 字符串 | 256 | 无 | 产品序列号 |
| 制造订单号 | `manuOrderCode` | `CMANU_ORDER_CODE` | 字符串 | 256 | 无 | 制造订单编码 |
| 制造订单ID | `manuOrderId` | `CMANU_ORDER_ID` | 长整型 | - | 无 | 隐藏字段，记录制造订单ID |
| 物料图号 | `materialDwgNo` | `CMATERIAL_DWG_NO` | 字符串 | 512 | 无 | 物料图纸编号 |
| 物料编码 | `materialCode` | `CMATERIAL_CODE` | 字符串 | 256 | 必填 | 物料编码 |
| 物料名称 | `materialName` | `CMATERIAL_NAME` | 字符串 | 256 | 必填 | 物料名称 |
| 物料ID | `materialId` | `CMATERIAL_ID` | 长整型 | - | 必填 | 隐藏字段，记录物料ID |
| 生产单位编码 | `prodBizOrgCode` | `CPROD_BIZ_ORG_CODE` | 字符串 | 256 | 无 | 生产业务组织编码 |
| 生产单位名称 | `prodBizOrgName` | `CPROD_BIZ_ORG_NAME` | 字符串 | 256 | 无 | 生产业务组织名称 |
| 生产单位ID | `prodBizOrgId` | `CPROD_BIZ_ORG_ID` | 长整型 | - | 无 | 隐藏字段，生产业务组织ID |
| 制造型号 | `manuModel` | `CMANU_MODEL` | 字符串 | 256 | 无 | 产品制造型号 |
| 标识 | `qhMark` | `CQH_MARK` | 字符串 | 512 | 无 | 隐藏字段，用作业务处理。统一格式：{物料id}\|{批次号}\|{序列号}，空值使用-代替 |

### 质量履历路径（QualityHistoryPath）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **表名:** `MOM_QUALITY_HISTORY_PATH`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 上级质量履历ID | `aboveQhId` | `CABOVE_QH_ID` | 长整型 | - | 无 | 记录直接父节点和递归父节点ID |
| 下级质量履历ID | `belowQhId` | `CBELOW_QH_ID` | 长整型 | - | 必填 | 记录直接子节点和递归子节点ID |
| 层号 | `levelNum` | `CPATH_DEPTH` | 整型 | - | 必填 | 每个节点都是自己的祖先（levelNum=0）；直接父子关系（levelNum=1）；间接父子关系（levelNum>1） |

### 质量履历-生产过程记录（QualityHistoryProcRecordLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_QUALITY_HISTORY_PROC_RECORD_LINK` | **源数据实体:** `QualityHistory`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造订单号 | `manuOrderCode` | `CMANU_ORDER_CODE` | 字符串 | 256 | 无 | 制造订单编码 |
| 制造订单ID | `manuOrderId` | `CMANU_ORDER_ID` | 长整型 | - | 无 | 隐藏字段，记录制造订单ID |
| 制造/检验任务号 | `taskCode` | `CTASK_CODE` | 字符串 | 256 | 无 | 任务编码 |
| 关联任务ID | `relatedTaskId` | `CRELATED_TASK_ID` | 长整型 | - | 无 | 隐藏字段，关联的制造任务/检验任务ID |
| 任务实体类型 | `taskEntityType` | `CTASK_ENTITY_TYPE` | 字符串 | 64 | 无 | 任务实体类型标识 |
| 检验分类 | `inspectCategory` | `CINSPECT_CATEGORY` | 枚举 | - | 无 | 引用枚举:InspectCategory |
| 返修标记 | `repairFlag` | `CREPAIR_FLAG` | 布尔 | - | 必填 | 表示是否为返修工序任务，默认值：false |
| 工艺路线名称 | `routingName` | `CROUTING_NAME` | 字符串 | 256 | 无 | 工艺路线名称 |
| 工艺路线编码 | `routingCode` | `CROUTING_CODE` | 字符串 | 256 | 无 | 工艺路线编码 |
| 工艺路线版本 | `routingVersion` | `CROUTING_VERSION` | 字符串 | 256 | 无 | 工艺路线版本号 |
| 工艺路线ID | `routingId` | `CROUTING_ID` | 长整型 | - | 无 | 隐藏字段，工艺路线ID |
| 工序号 | `routingProcNum` | `CROUTING_PROC_NUM` | 字符串 | 256 | 无 | 工序编号 |
| 工序名称 | `routingProcName` | `CROUTING_PROC_NAME` | 字符串 | 256 | 无 | 工序名称 |
| 工艺工序ID | `routingProcId` | `CROUTING_PROC_ID` | 长整型 | - | 无 | 隐藏字段，工艺工序ID |
| 操作员编码 | `operatorCode` | `COPERATOR_CODE` | 字符串 | 256 | 无 | 操作员编码 |
| 操作员名称 | `operatorName` | `COPERATOR_NAME` | 字符串 | 256 | 无 | 操作员名称 |
| 操作员ID | `operatorId` | `COPERATOR_ID` | 长整型 | - | 无 | 隐藏字段，操作员ID |
| 完工时间 | `completedTime` | `CCOMPLETED_TIME` | 日期时间 | - | 无 | 加工任务的实际完成时间 |
| 合格数量 | `qualifiedQty` | `CQUALIFIED_QTY` | 浮点型 | - | 无 | 任务完成的合格数量 |
| 设备编码 | `equipCode` | `CEQUIP_CODE` | 字符串 | 256 | 无 | 使用设备的编码 |
| 设备名称 | `equipName` | `CEQUIP_NAME` | 字符串 | 256 | 无 | 使用设备的名称 |
| 设备ID | `equipId` | `CEQUIP_ID` | 长整型 | - | 无 | 隐藏字段，设备ID |

### 质量履历-实物BOM（QualityHistoryPhysicalBomLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_QUALITY_HISTORY_PHYSICAL_BOM_LINK` | **源数据实体:** `QualityHistory`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 子物料图号 | `materialDwgNo` | `CMATERIAL_DWG_NO` | 字符串 | 512 | 无 | 子物料图纸编号 |
| 子物料编码 | `materialCode` | `CMATERIAL_CODE` | 字符串 | 256 | 必填 | 子物料编码 |
| 子物料名称 | `materialName` | `CMATERIAL_NAME` | 字符串 | 256 | 必填 | 子物料名称 |
| 子物料批次 | `materialBatch` | `CMATERIAL_BATCH` | 字符串 | 256 | 无 | 子物料批次号 |
| 子物料序列号 | `materialSn` | `CMATERIAL_SN` | 字符串 | 256 | 无 | 子物料序列号 |
| 使用数量 | `useQty` | `CUSE_QTY` | 浮点型 | - | 必填 | 该物料在单个产品中的使用数量 |
| 子物料ID | `materialId` | `CMATERIAL_ID` | 长整型 | - | 必填 | 隐藏字段，记录子物料ID |

---

## 变更记录

| 日期 | 版本 | 变更内容 | 变更人 |
|-----|------|---------|-----|
| 2025-12-17 | v1.0 | 创建文档，定义质量履历及关联数据模型 | 王晴  |
| 2025-12-29 | v1.1 | 优化生命周期继承：QualityHistory使用COMMON_LIFECYCLE | 危放  |
| 2025-12-29 | v1.2 | 改造业务属性为引用格式 | 王晴 |
| 2026-01-22 | v1.3 | 补充关系实体源数据实体元信息：QualityHistoryProcRecordLink、QualityHistoryPhysicalBomLink | 危放 |
