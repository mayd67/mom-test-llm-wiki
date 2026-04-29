# 制造执行系统(MES)数据模型

## 文档说明

**基本信息**
- 文档版本：v1.13 | 更新日期：2026-04-22 | 维护团队：产品研发团队
- 目标受众：产品研发团队

**文档定位**

本文档定义KMMOM3.x制造执行系统(MES)的数据模型设计，涵盖计划管理、执行管理、工时管理、质量检验、外委管理、采购管理、生产异常等业务领域的完整数据模型定义。

**内容结构**

| 章节 | 核心问题 | 内容说明 |
|------|---------|----------|
| 一、术语、定义和缩略语 | MES领域的专业术语是什么？ | 定义生产运行管理相关的业务概念和缩略语 |
| 二、计划管理 | 如何管理生产订单、制造订单、制造任务？ | 定义生产计划层级结构及制造任务相关模型 |
| 三、执行管理 | 如何管理报工、物料准备和在制品？ | 定义生产执行过程中的操作模型 |
| 四、工时管理 | 如何记录和管理工时数据？ | 定义工时明细数据模型 |
| 五、质量检验 | 如何管理检验任务、检验报工和不合格品审理？ | 定义检验分类配置、质量方案、检验任务、检验报工凭证、质量填报模版和不合格品处理相关模型 |
| 六、外委管理 | 如何管理外委需求、订单、发货收货等？ | 定义外委需求、订单、发货收货等模型 |
| 七、采购管理 | 如何管理采购需求和执行？ | 定义采购需求、订单、收货退货等模型 |
| 八、生产异常 | 如何管理生产过程中的异常？ | 定义异常类别、异常任务等模型 |

---

## 一、术语、定义和缩略语

| 术语 | 定义 | 缩略语 |
|------|------|--------|
| 生产运行管理 | 制造设施协调、指导、管理和跟踪生产活动，包括成本、质量、数量、安全和时效性要求下使用的原料、能源、设备、人员和信息来生产产品的诸多功能 | Production Operation Management |
| 生产订单 | 根据客户需求或生产计划生成的顶层生产指令，定义产品、数量、交期等基本信息 | PO (Production Order) |
| 制造订单 | 生产订单释放后生成的制造执行指令，关联具体的工艺路线和物料清单 | MO (Manufacturing Order) |
| 制造任务 | 制造订单按工艺路线展开后的工序级执行单元，是派工和报工的基础 | MT (Manufacturing Task) |
| 在制品 | 生产过程中已完成部分工序但尚未完工的半成品 | WIP (Work In Process) |
| 外委 | 将部分或全部工序委托给外部供应商完成的生产方式 | Outsourcing |

---

## 二、计划管理

### 2.1 生产订单（ProdOrder）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`IntegrationManaged`、`LifecycleManaged`、`SecurityManaged` | **表名:** `MOM_PROD_ORDER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 名称 | `name` | `CNAME` | 字符串 | 512 | 无 | |
| 订单类型 | `orderType` | `CORDER_TYPE` | 枚举 | - | 无 | 引用枚举:orderType|
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |
| BOM | `bom` | `CBOM` | 引用对象 | - | 无 | 引用BOM |
| 制造型号 | `manuModel` | `CMANU_MODEL` | 字符串 | 256 | 无 | |
| 工艺路线 | `routing` | `CROUTING` | 引用对象 | - | 无 | 引用Routing |
| 计量单位 | `unit` | `CUNIT` | 单位 | - | 必填 | 引用单位:measureUnit |
| 计划数量 | `plannedQty` | `CPLANNED_QTY` | 浮点型 | - | 必填 | |
| 计划产出数量 | `plannedOutputQty` | `CPLANNED_OUTPUT_QTY` | 浮点型 | - | 无 | 不用于功能；用于数据对比分析 |
| 合格数量 | `qualifiedQty` | `CQUALIFIED_QTY` | 浮点型 | - | 无 | 回写冗余字段 |
| 报废数量 | `scrappedQty` | `CSCRAPPED_QTY` | 浮点型 | - | 无 | 回写冗余字段 |
| 已释放数量 | `releasedQty` | `CRELEASED_QTY` | 浮点型 | - | 无 | 回写冗余字段 |
| 计划开始时间 | `plannedStartTime` | `CPLANNED_START_TIME` | 日期时间 | - | 无 | |
| 计划结束时间 | `plannedEndTime` | `CPLANNED_END_TIME` | 日期时间 | - | 必填 | |
| 实际开始时间 | `actualStartTime` | `CACTUAL_START_TIME` | 日期时间 | - | 无 | |
| 实际结束时间 | `actualEndTime` | `CACTUAL_END_TIME` | 日期时间 | - | 无 | |
| 优先级 | `priority` | `CPRIORITY` | 整型 | - | 无 | |
| 计划员 | `planner` | `CPLANNER` | 用户 | - | 无 | |
| 控制状态 | `controlStatus` | `CCONTROL_STATUS` | 枚举 | - | 必填 | 引用枚举:controlStatus |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填 | 引用枚举:ProdOrderBizStatus |
| 释放状态 | `releasedStatus` | `CRELEASED_STATUS` | 枚举 | - | 无 | 引用枚举:ReleasedStatus|
| 计划类型 | `prodPlanType` | `CPROD_PLAN_TYPE` | 枚举 | - | 无 | 引用枚举:ProdPlanType|
| 排产状态 | `prodScheduleState` | `CPROD_SCHEDULE_STATE` | 枚举 | - | 无 | 引用枚举:ProdScheduleState|

### 2.2 生产订单一级工艺展开结构表（ProdOrderPrExpandLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_PROD_ORDER_PR_EXPAND_LINK` | **源数据实体:** `ProdOrder`

专用于通过一级工艺展开生产订单结构信息，PR=primary routing 即一级工艺。

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 子订单 | `childOrder` | `CCHILD_ORDER` | 引用对象 | - | 必填 | 引用ProdOrder |
| 子订单号 | `childOrderCode` | `CCHILD_ORDER_CODE` | 字符串 | 256 | 必填 | 冗余字段 |
| 子订单所属工厂 | `childOrderFactory` | `CCHILD_ORDER_FACTORY` | 引用对象 | - | 无 | 引用BizOrg |
| 子订单工序 | `childOrderProc` | `CCHILD_ORDER_PROC` | 引用对象 | - | 必填 | 子订单在一级工艺中对应的工序 |
| 子订单工序号 | `childOrderProcNum` | `CCHILD_ORDER_PROC_NUM` | 字符串 | 256 | 必填 | 冗余字段 |
| 子订单工序名称 | `childOrderProcName` | `CCHILD_ORDER_PROC_NAME` | 字符串 | 256 | 必填 | 冗余字段 |
| 子订单分派资源 | `childOrderRes` | `CCHILD_ORDER_RES` | 引用对象 | - | 无 | 子订单在协同排产时分派资源 |
| 序号 | `index` | `CINDEX` | 整型 | - | 必填 | 表示子订单在相同父订单下顺序 |

### 2.3 生产订单释放记录（ProdOrderReleaseLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** `FactoryManaged` | **表名:** `MOM_PROD_ORDER_RELEASE_LINK` | **源数据实体:** `ProdOrder`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造订单 | `manuOrder` | `CMANU_ORDER` | 引用对象 | - | 必填 | 引用ManuOrder |
| 数量 | `qty` | `CQTY` | 浮点型 | - | 必填 | |

### 2.4 备料清单（ProdOrderPreparationLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_PROD_ORDER_PREPARATION_LINK` | **源数据实体:** `ProdOrder`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | |
| 工序号 | `processNum` | `CPROCESS_NUM` | 字符串 | 256 | 无 | |
| 工序名称 | `processName` | `CPROCESS_NAME` | 字符串 | 256 | 无 | |
| 需求数量 | `requireQty` | `CREQUIRE_QTY` | 浮点型 | - | 必填 | |
| 子件比例 | `componentRatio` | `CCOMPONENT_RATIO` | 整型 | - | 必填 | 默认为1 |
| 替换件物料 | `replacementMaterial` | `CREPLACEMENT_MATERIAL` | 引用对象 | - | 无 | 引用Material |
| 是否必须装入 | `mustReceiveFlag` | `CMUST_RECEIVE_FLAG` | 布尔 | - | 无 |  |

### 2.5 生产订单动作变迁记录（ProdOrderActionRecordLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_PROD_ORDER_ACTION_RECORD_LINK` | **源数据实体:** `ProdOrder`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 操作人 | `operator` | `COPERATOR` | 长整型 | - | 必填 | 操作人ID |
| 操作人编码 | `operatorCode` | `COPERATOR_CODE` | 字符串 | 256 | 必填 | |
| 操作人名称 | `operatorName` | `COPERATOR_NAME` | 字符串 | 256 | 必填 | |
| 操作时间 | `operatorTime` | `COPERATOR_TIME` | 日期时间 | - | 必填 | |
| 操作员IP | `operatorIp` | `COPERATOR_IP` | 字符串 | 256 | 无 | |
| 操作 | `action` | `CACTION` | 字符串 | 256 | 无 | |
| 操作内容 | `actionContent` | `CACTION_CONTENT` | CLOB | - | 无 | |
| 状态变动标记 | `statusChangeFlag` | `CSTATUS_CHANGE_FLAG` | 布尔 | - | 无 | |
| 当前状态 | `currentStatus` | `CCURRENT_STATUS` | 字符串 | 256 | 无 | |
| 目标状态 | `targetStatus` | `CTARGET_STATUS` | 字符串 | 256 | 无 | |

### 2.6 制造订单（ManuOrder）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`LifecycleManaged`、`SecurityManaged` | **表名:** `MOM_MANU_ORDER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 订单制造类型 | `manuType` | `CMANU_TYPE` | 枚举 | - | 必填 | 引用枚举:ManuType|
| 生产订单 | `prodOrder` | `CPROD_ORDER` | 引用对象 | - | 必填 | 引用ProdOrder |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |
| 制造型号 | `manuModel` | `CMANU_MODEL` | 字符串 | 256 | 无 | |
| BOM | `bom` | `CBOM` | 引用对象 | - | 无 | 引用BOM |
| 工艺路线 | `routing` | `CROUTING` | 引用对象 | - | 无 | 引用Routing |
| 计量单位 | `unit` | `CUNIT` | 单位 | - | 必填 | 引用单位:measureUnit |
| 计划数量 | `plannedQty` | `CPLANNED_QTY` | 浮点型 | - | 必填 | |
| 合格数量 | `qualifiedQty` | `CQUALIFIED_QTY` | 浮点型 | - | 无 | 冗余回写字段 |
| 报废数量 | `scrappedQty` | `CSCRAPPED_QTY` | 浮点型 | - | 无 | 冗余回写字段 |
| 计划开始时间 | `plannedStartTime` | `CPLANNED_START_TIME` | 日期时间 | - | 必填 | 排产时间 |
| 计划结束时间 | `plannedEndTime` | `CPLANNED_END_TIME` | 日期时间 | - | 必填 | |
| 实际开始时间 | `actualStartTime` | `CACTUAL_START_TIME` | 日期时间 | - | 无 | |
| 实际结束时间 | `actualEndTime` | `CACTUAL_END_TIME` | 日期时间 | - | 无 | |
| 指定计划开始时间 | `specifiedPlannedStartTime` | `CSPECIFIED_PLANNED_START_TIME` | 日期时间 | - | 无 | |
| 指定计划结束时间 | `specifiedPlannedEndTime` | `CSPECIFIED_PLANNED_END_TIME` | 日期时间 | - | 无 |  |
| 优先级 | `priority` | `CPRIORITY` | 整型 | - | 无 | |
| 计划员 | `planner` | `CPLANNER` | 用户 | - | 无 | |
| 控制状态 | `controlStatus` | `CCONTROL_STATUS` | 枚举 | - | 必填 | 引用枚举:controlStatus |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填 | 引用枚举:ManuOrderBizStatus |
| 启用序列号标记 | `serialNumberFlag` | `CSERIAL_NUMBER_FLAG` | 布尔 | - | 无 | |
| 排程标记 | `scheduledFlag` | `CSCHEDULED_FLAG` | 布尔 | - | 必填 | 默认false |
| 是否外委 | `outsourcingFlag` | `COUTSOURCING_FLAG` | 布尔 | - | 无 | |
| 物料准备计划 | `preparationPlan` | `CPREPARATION_PLAN` | 引用对象 | - | 无 | 引用MaterialPreparationPlan |
| 已申请报废入库数量 | `appliedScrapInStorageQty` | `CAPPLIED_SCRAP_IN_STORAGE_QTY` | 浮点型 | - | 无 |  |
| 已申请合格入库数量 | `appliedInStorageQty` | `CAPPLIED_IN_STORAGE_QTY` | 浮点型 | - | 无 | |
| 分卡标记 | `splitCardFlag` | `CSPLIT_CARD_FLAG` | 布尔 | - | 无 | 默认false |
| 返工/返修来源制造订单 | `reworkSourceManuOrder` | `CREWORK_SOURCE_MANU_ORDER` | 引用对象 | - | 无 | |
| 分卡来源制造订单 | `splitCardSourceManuOrder` | `CSPLIT_CARD_SOURCE_MANU_ORDER` | 引用对象 | - | 无 | |
| 是否入库 | `storedFlag` | `CSTORED_FLAG` | 布尔 | - | 无 | 默认false 已入库的标记 |

### 2.7 制造订单与不合格品审理单结论关系（ManuOrderDefectiveReviewLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MANU_ORDER_DEFECTIVE_REVIEW_LINK` | **源数据实体:** `ManuOrder`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 不合格品审理结论 | `defectiveReviewConclusion` | `CDEFECTIVE_REVIEW_CONCLUSION` | 引用对象 | - | 无 | 引用DefectiveProductReview |
| 不合格品子件审理结论 | `defectiveReviewSubConclusion` | `CDEFECTIVE_REVIEW_SUB_CONCLUSION` | 引用对象 | - | 无 | 引用DefectiveReviewSubConclusionLink |
| 审理结论类型 | `conclusionType` | `CCONCLUSION_TYPE` | 枚举 | - | 无 | 引用枚举:DefectiveProductReviewConclusionType|

### 2.8 制造订单动作变迁记录（ManuOrderActionRecordLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MANU_ORDER_ACTION_RECORD_LINK` | **源数据实体:** `ManuOrder`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 操作人 | `operator` | `COPERATOR` | 长整型 | - | 必填 | 操作人ID |
| 操作人编码 | `operatorCode` | `COPERATOR_CODE` | 字符串 | 256 | 必填 | |
| 操作人名称 | `operatorName` | `COPERATOR_NAME` | 字符串 | 256 | 必填 | |
| 操作时间 | `operatorTime` | `COPERATOR_TIME` | 日期时间 | - | 必填 | |
| 操作员IP | `operatorIp` | `COPERATOR_IP` | 字符串 | 256 | 必填 | |
| 操作 | `action` | `CACTION` | 字符串 | 256 | 无 | |
| 操作内容 | `actionContent` | `CACTION_CONTENT` | CLOB | - | 无 | |
| 状态变动标记 | `statusChangeFlag` | `CSTATUS_CHANGE_FLAG` | 布尔 | - | 无 | |
| 当前状态 | `currentStatus` | `CCURRENT_STATUS` | 字符串 | 256 | 无 | |
| 目标状态 | `targetStatus` | `CTARGET_STATUS` | 字符串 | 256 | 无 | |

### 2.9 制造订单序列号（ManuOrderSerialNumberLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MANU_ORDER_SERIAL_NUMBER_LINK` | **源数据实体:** `ManuOrder`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 必填 | |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |

### 2.10 制造订单产出序列号（ManuOrderOutputSerialNumberLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MANU_ORDER_OUT_PUT_SERIAL_NUMBER_LINK` | **源数据实体:** `ManuOrder`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 必填 | |
| 汇报项类型 | `reportType` | `CREPORT_TYPE` | 字符串 | 256 | 必填 | |

### 2.11 已发布排程结果（ReleasedScheduleResult）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_RELEASED_SCHEDULE_RESULT`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 订单ID | `orderId` | `CORDER_ID` | 长整型 | - | 必填 | |
| 排产开始时间 | `assignedBeginTime` | `CASSIGNED_BEGIN_TIME` | 日期时间 | - | 必填 | 记录最新排产的任务开始时间 |
| 排产结束时间 | `assignedEndTime` | `CASSIGNED_END_TIME` | 日期时间 | - | 必填 | 记录最新排产的任务结束时间 |
| 排产资源类型 | `resCategory` | `CRES_CATEGORY` | 枚举 | - | 无 | 引用枚举:ResCategory|
| 工作中心 | `workCenter` | `CWORK_CENTER` | 引用对象 | - | 无 | 引用WorkCenter |
| 设备 | `equipment` | `CEQUIPMENT` | 引用对象 | - | 无 | 引用Equip |
| 分派时间槽 | `assignedTimeSlots` | `CASSIGNED_TIME_SLOTS` | 字符串 | 4096 | 无 | 表示本次分派时间段，格式：20241201090000-20241201123000;20241201140000-20241201183000; |

### 2.12 制造任务（ManuTask）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`SecurityManaged` | **表名:** `MOM_MANU_TASK`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束            | 说明 |
|-------------|-------------|-----------|---------|------|---------------|------|
| 生产订单 | `prodOrder` | `CPROD_ORDER` | 引用对象 | - | 无             | 引用ProdOrder |
| 生产订单号 | `prodOrderCode` | `CPROD_ORDER_CODE` | 字符串 | 256 | 无             | 冗余存储（工控网隔离） |
| 制造订单 | `manuOrder` | `CMANU_ORDER` | 引用对象 | - | 无             | 引用ManuOrder |
| 制造订单号 | `manuOrderCode` | `CMANU_ORDER_CODE` | 字符串 | 256 | 无             | 冗余存储（工控网隔离） |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填            | 引用Material |
| 物料名称 | `materialName` | `CMATERIAL_NAME` | 字符串 | 512 | 无             | 冗余存储（工控网隔离） |
| 物料编码 | `materialCode` | `CMATERIAL_CODE` | 字符串 | 256 | 无             | 冗余存储（工控网隔离） |
| 物料图号 | `materialDwgNumber` | `CMATERIAL_DWG_NUMBER` | 字符串 | 256 | 无             | 冗余存储（工控网隔离） |
| 物料版本 | `materialVersion` | `CMATERIAL_VERSION` | 字符串 | 256 | 无             | 冗余存储（工控网隔离） |
| 工艺路线 | `routing` | `CROUTING` | 引用对象 | - | 必填            | 引用Routing |
| 工艺路线名称 | `routingName` | `CROUTING_NAME` | 字符串 | 512 | 无             | 冗余存储（工控网隔离） |
| 工艺路线编码 | `routingCode` | `CROUTING_CODE` | 字符串 | 256 | 无             | 冗余存储（工控网隔离） |
| 工艺路线版本 | `routingVersion` | `CROUTING_VERSION` | 字符串 | 256 | 无             | 冗余存储（工控网隔离） |
| 计量单位 | `unit` | `CUNIT` | 单位 | - | 必填            | 引用单位:measureUnit |
| 计划数量 | `plannedQty` | `CPLANNED_QTY` | 浮点型 | - | 必填            | |
| 合格数量 | `qualifiedQty` | `CQUALIFIED_QTY` | 浮点型 | - | 无             | 冗余回写字段 |
| 报废数量 | `scrappedQty` | `CSCRAPPED_QTY` | 浮点型 | - | 无             | 冗余回写字段 |
| 待定数量 | `pendingQty` | `CPENDING_QTY` | 浮点型 | - | 无             | 冗余回写字段 |
| 在制品数量 | `wipQty` | `CWIP_QTY` | 浮点型 | - | 无 |  |
| 工艺路线工序 | `routingProcess` | `CROUTING_PROCESS` | 引用对象 | - | 无             | |
| 工序号 | `processNum` | `CPROCESS_NUM` | 字符串 | 256 | 必填            | 冗余存储（工控网隔离） |
| 工序名称 | `processName` | `CPROCESS_NAME` | 字符串 | 256 | 无             | 冗余存储（工控网隔离） |
| 工序类型 | `processType` | `CPROCESS_TYPE` | 枚举 | - | 无             | 引用枚举:ProcessType|
| 工作中心 | `workCenter` | `CWORK_CENTER` | 引用对象 | - | 无             | 引用WorkCenter |
| 设备 | `equipment` | `CEQUIPMENT` | 引用对象 | - | 无             | 引用Equip |
| 计划开始时间 | `plannedStartTime` | `CPLANNED_START_TIME` | 日期时间 | - | 无             | |
| 计划结束时间 | `plannedEndTime` | `CPLANNED_END_TIME` | 日期时间 | - | 必填            | |
| 实际开始时间 | `actualStartTime` | `CACTUAL_START_TIME` | 日期时间 | - | 无             | |
| 实际结束时间 | `actualEndTime` | `CACTUAL_END_TIME` | 日期时间 | - | 无             | |
| 指定工作中心 | `specifiedWorkCenter` | `CSPECIFIED_WORK_CENTER` | 引用对象 | - | 无             | 适用于排产锁定工作中心 |
| 控制状态 | `controlStatus` | `CCONTROL_STATUS` | 枚举 | - | 必填            | 引用枚举:controlStatus|
| 是否末道工序 | `lastProcFlag` | `CLAST_PROC_FLAG` | 布尔 | - | 无             | |
| 序号 | `index` | `CINDEX` | 整型 | - | 无             | |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无             | |
| 执行标记 | `executionFlag` | `CEXECUTION_FLAG` | 布尔 | - | 无             | |
| 产出比 | `productivityRate` | `CPRODUCTIVITY_RATE` | 整型 | - | 无             | |
| 父任务标记 | `parentFlag` | `CPARENT_FLAG` | 布尔 | - | 无             | |
| 父任务 | `parentTask` | `CPARENT_TASK` | 引用对象 | - | 无             | |
| 根任务 | `rootTask` | `CROOT_TASK` | 引用对象 | - | 无             | |
| 到料数量 | `inputMaterialQty` | `CINPUT_MATERIAL_QTY` | 浮点型 | - | 无             | |
| 到料状态 | `inputMaterialStatus` | `CINPUT_MATERIAL_STATUS` | 枚举 | - | 无             | 引用枚举:inputMaterialType|
| 定额准备时间 | `preparationTime` | `CPREPARATION_TIME` | 浮点型 | - | 无             | |
| 定额加工时间 | `processingTime` | `CPROCESSING_TIME` | 浮点型 | - | 无             | |
| 时间单位 | `timeUnit` | `CTIME_UNIT` | 单位 | - | 引用单位:`timeUnit` | |
| 实作工时 | `actualWorkHours` | `CACTUAL_WORK_HOURS` | 浮点型 | - | 无             | |
| 定额总工时 | `quotaWorkHours` | `CQUOTA_WORK_HOURS` | 浮点型 | - | 无             | |
| 定额分配状态 | `quotaStatus` | `CQUOTA_STATUS` | 枚举 | - | 无             | 引用枚举:QuotaStatus |
| 实作工时单位 | `actualTimeUnit` | `CACTUAL_TIME_UNIT` | 单位 | - | 无             | |
| 启用序列号标记 | `serialNumberFlag` | `CSERIAL_NUMBER_FLAG` | 布尔 | - | 无             | |
| 外委标记 | `outsourcingFlag` | `COUTSOURCING_FLAG` | 布尔 | - | 无             | |
| 自检标记 | `selfInspectFlag` | `CSELF_INSPECT_FLAG` | 布尔 | - | 无             | 默认为false |
| 互检标记 | `mutualInspectFlag` | `CMUTUAL_INSPECT_FLAG` | 布尔 | - | 无             | 默认为false |
| 专检标记 | `specialInspectFlag` | `CSPECIAL_INSPECT_FLAG` | 布尔 | - | 无             | 默认为false |
| 客户检标记 | `customerInspectFlag` | `CCUSTOMER_INSPECT_FLAG` | 布尔 | - | 无             | 默认为false |
| 首检标记 | `firstInspectFlag` | `CFIRST_INSPECT_FLAG` | 布尔 | - | 无             | 默认为false |
| 首检状态 | `firstInspectStatus` | `CFIRST_INSPECT_STATUS` | 枚举 | - | 无             | 引用枚举:manuTaskFirstInspectStatus|
| 派工方式 | `dispatchMode` | `CDISPATCH_MODE` | 枚举 | - | 无             | 引用枚举:DispatchMode|
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填            | 引用枚举:ManuTaskBizStatus |

### 2.13 制造任务动作变迁记录（ManuTaskActionRecordLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MANU_TASK_ACTION_RECORD_LINK` | **源数据实体:** `ManuTask`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 操作人 | `operator` | `COPERATOR` | 长整型 | - | 必填 | 操作人ID |
| 操作人编码 | `operatorCode` | `COPERATOR_CODE` | 字符串 | 256 | 必填 | |
| 操作人名称 | `operatorName` | `COPERATOR_NAME` | 字符串 | 256 | 必填 | |
| 操作时间 | `operatorTime` | `COPERATOR_TIME` | 日期时间 | - | 必填 | |
| 操作员IP | `operatorIp` | `COPERATOR_IP` | 字符串 | 256 | 无 | |
| 操作 | `action` | `CACTION` | 字符串 | 256 | 无 | |
| 操作内容 | `actionContent` | `CACTION_CONTENT` | CLOB | - | 无 | |
| 状态变动标记 | `statusChangeFlag` | `CSTATUS_CHANGE_FLAG` | 布尔 | - | 无 | |
| 当前状态 | `currentStatus` | `CCURRENT_STATUS` | 字符串 | 256 | 无 | |
| 目标状态 | `targetStatus` | `CTARGET_STATUS` | 字符串 | 256 | 无 | |

### 2.14 上道制造任务关系（ManuTaskPrevRelationLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MANU_TASK_PREV_RELATION_LINK` | **源数据实体:** `ManuTask`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 当前任务 | `taskId` | `CTASK_ID` | 引用对象 | - | 必填 | 只有父任务关系 |
| 上道任务 | `prevTask` | `CPREV_TASK` | 引用对象 | - | 必填 | 引用ManuTask |
| 制造订单id | `manuOrder` | `CMANU_ORDER` | 引用对象 | - | 必填 | 引用ManuOrder |
| 上道可执行工序 | `executionPrevTask` | `CEXECUTION_PREV_TASK` | 引用对象 | - | 无 | |
| 接续关系 | `timeConstraintMethod` | `CTIME_CONSTRAINT_METHOD` | 字符串 | 256 | 无 | ES\|SSEE |

### 2.15 制造任务分派执行人（ManuTaskExecutorLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MANU_TASK_EXECUTOR_LINK` | **源数据实体:** `ManuTask`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 执行人 | `executor` | `CEXECUTOR` | 用户 | - | 无 | |



---

## 三、执行管理

### 3.1 物料准备计划（MaterialPreparationPlan）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`SecurityManaged`| **表名:** `MOM_MATERIAL_PREPARATION_PLAN`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造订单 | `manuOrder` | `CMANU_ORDER` | 引用对象 | - | 必填 | 引用ManuOrder |
| 控制状态 | `controlStatus` | `CCONTROL_STATUS` | 枚举 | - | 必填 | 引用枚举:controlStatus |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填 | 引用枚举:MaterialPreparationPlanBizStatus |

### 3.2 物料准备计划明细（MaterialPreparationPlanDetailLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MATERIAL_PREPARE_PLAN_DETAIL_LINK` | **源数据实体:** `MaterialPreparationPlan`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造订单 | `manuOrder` | `CMANU_ORDER` | 引用对象 | - | 必填 | 引用ManuOrder |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |
| 工序号 | `processCode` | `CPROCESS_CODE` | 字符串 | 256 | 无 | |
| 工序名称 | `processName` | `CPROCESS_NAME` | 字符串 | 256 | 无 | |
| 需求数量 | `requireQty` | `CREQUIRE_QTY` | 浮点型 | - | 必填 | |
| 子件比例 | `componentRatio` | `CCOMPONENT_RATIO` | 整型 | - | 必填 | 默认为1 |
| 已申请数量 | `requestQty` | `CREQUEST_QTY` | 浮点型 | - | 必填 | 默认为0 |
| 已收料数量 | `receiveQty` | `CRECEIVE_QTY` | 浮点型 | - | 必填 | 默认为0 |
| 需求到料时间 | `needTime` | `CNEED_TIME` | 日期时间 | - | 必填 | |
| 到货位置 | `inboundLocation` | `CINBOUND_LOCATION` | 引用对象 | - | 无 | 引用LogisticsLocation |
| 是否必须装入 | `mustReceiveFlag` | `CMUST_RECEIVE_FLAG` | 布尔 | - | 无 | |
| 替换件物料 | `replacementMaterial` | `CREPLACEMENT_MATERIAL` | 引用对象 | - | 无 | 引用Material |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填 | 引用枚举:MaterialPlanLinkBizStatus |

### 3.3 领料申请明细（MaterialPreparationPlanRequestDetailLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MATERIAL_PREPARATION_PLAN_REQUEST_DETAIL_LINK` | **源数据实体:** `MaterialPreparationPlan`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 出库申请单 | `outStoreApplyBill` | `COUT_STORE_APPLY_BILL` | 引用对象 | - | 必填 | |
| 出库申请单物料 | `outStoreApplyBillMaterial` | `COUT_STORE_APPLY_BILL_MATERIAL` | 引用对象 | - | 必填 | |
| 物料准备计划明细 | `materialPreparationPlanDetail` | `CMATERIAL_PREPARE_PLAN_DETAIL` | 引用对象 | - | 必填 | |
| 申请人 | `applicant` | `CAPPLICANT` | 用户 | - | 必填 | |
| 申请时间 | `applicantTime` | `CAPPLICANT_TIME` | 日期时间 | - | 必填 | |

### 3.4 收料确认明细（MaterialPreparationPlanReceivingDetailLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MATERIAL_PREPARATION_PLAN_RECEIVING_DETAIL_LINK` | **源数据实体:** `MaterialPreparationPlan`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 出库单 | `outStoreRecord` | `COUT_STORE_RECORD` | 引用对象 | - | 必填 | |
| 物料准备计划明细 | `materialPreparationPlanDetail` | `CMATERIAL_PREPARE_PLAN_DETAIL` | 引用对象 | - | 必填 | |
| 实际接受物料 | `receivedMaterial` | `CRECEIVED_MATERIAL` | 引用对象 | - | 无 | 引用Material |
| 批次号 | `batchNo` | `CBATCH_NO` | 字符串 | 256 | 无 | |
| 序列号 | `sn` | `CSN` | 字符串 | 256 | 无 | |
| 收料人 | `receiver` | `CRECEIVER` | 用户 | - | 必填 | |
| 收料时间 | `receiveTime` | `CRECEIVE_TIME` | 日期时间 | - | 必填 | |
| 收料数量 | `receiveQty` | `CRECEIVE_QTY` | 浮点型 | - | 必填 | |
| 装入数量 | `inputQty` | `CINPUT_QTY` | 浮点型 | - | 无 | |
| 已退数量 | `returnedQty` | `CRETURNED_QTY` | 浮点型 | - | 无 | |
| 库存批次属性 | `inventoryBatchAttribute` | `CINVENTORY_BATCH_ATTRIBUTE` | 引用对象 | - | 无 | |

### 3.5 退料申请明细（MaterialPreparationPlanReturnDetailLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MATERIAL_PREPARATION_PLAN_RETURN_DETAIL_LINK` | **源数据实体:** `MaterialPreparationPlan`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 入库单 | `inStoreApplyBill` | `CIN_STORE_APPLY_BILL` | 引用对象 | - | 必填 | |
| 入库申请单关联物料 | `inStoreApplyBillMaterial` | `CIN_STORE_APPLY_BILL_MATERIAL` | 引用对象 | - | 必填 | |
| 物料准备计划明细 | `materialPreparationPlanDetail` | `CMATERIAL_PREPARE_PLAN_DETAIL` | 引用对象 | - | 必填 | |
| 收料确认明细 | `materialPreparationPlanReceivingDetail` | `CMATERIAL_PREPARATION_PLAN_RECEIVING_DETAIL` | 引用对象 | - | 必填 | 基于收料确认明细做的退料 |
| 申请人 | `applicant` | `CAPPLICANT` | 用户 | - | 必填 | |
| 申请时间 | `applicantTime` | `CAPPLICANT_TIME` | 日期时间 | - | 必填 | |
| 退料原因 | `returnReason` | `CRETURN_REASON` | 字符串 | 512 | 必填 | |
| 退料数量 | `returnQty` | `CRETURN_QTY` | 浮点型 | - | 必填 | |

### 3.6 物料装入清单（MaterialLoadList）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_MATERIAL_LOAD_LIST`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造订单 | `manuOrder` | `CMANU_ORDER` | 引用对象 | - | 必填 | 引用ManuOrder |
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 无 | 引用ManuTask |
| 装入物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |
| 替换件物料 | `replacementMaterial` | `CREPLACEMENT_MATERIAL` | 引用对象 | - | 无 | 引用Material |
| 工序号 | `processCode` | `CPROCESS_CODE` | 字符串 | 256 | 无 | |
| 工序名称 | `processName` | `CPROCESS_NAME` | 字符串 | 256 | 无 | |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | 任务批次号 |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | 任务顺序号 |
| 需求数量 | `requireQty` | `CREQUIRE_QTY` | 浮点型 | - | 必填 | |
| 已装入数量 | `actualQty` | `CACTUAL_QTY` | 浮点型 | - | 无 | |
| 物料准备计划明细 | `materialPlanDetail` | `CMATERIAL_PLAN_DETAIL` | 引用对象 | - | 无 | |

### 3.7 物料实际装入（MaterialActualLoadLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MATERIAL_ACTUAL_LOAD_LINK` | **源数据实体:** `MaterialLoadList`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |
| 收料确认明细 | `materialReceivingDetail` | `CMATERIAL_RECEIVING_DETAIL` | 引用对象 | - | 无 | |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | |
| 操作人 | `operator` | `COPERATOR` | 用户 | - | 无 | |
| 已装数量 | `operatorQty` | `COPERATOR_QTY` | 浮点型 | - | 必填 | |
| 装入时间 | `operatorTime` | `COPERATOR_TIME` | 日期时间 | - | 必填 | |
| 库存批次属性 | `inventoryBatchAttribute` | `CINVENTORY_BATCH_ATTRIBUTE` | 引用对象 | - | 无 | |

### 3.8 物料拆装操作记录（MaterialLoadRecordLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MATERIAL_LOAD_RECORD_LINK` | **源数据实体:** `MaterialLoadList`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | 库存 批次号 |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | 库存 顺序号 |
| 操作类型 | `loadType` | `CLOAD_TYPE` | 枚举 | - | 必填 | 引用枚举:materialLoadType|
| 操作人 | `operator` | `COPERATOR` | 用户 | - | 无 | |
| 操作数量 | `operatorQty` | `COPERATOR_QTY` | 浮点型 | - | 必填 | |
| 操作时间 | `operatorTime` | `COPERATOR_TIME` | 日期时间 | - | 必填 | |
| 操作说明 | `operatorRemark` | `COPERATOR_REMARK` | 字符串 | 1024 | 无 | |

### 3.9 在制品（Wip）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`SecurityManaged` | **表名:** `MOM_WIP`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造订单 | `manuOrder` | `CMANU_ORDER` | 引用对象 | - | 无 | 引用ManuOrder |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 无 | 引用Material |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | |
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 无 | 引用ManuTask |
| 数量 | `qty` | `CQTY` | 浮点型 | - | 无 | |
| 状态 | `wipStatus` | `CWIP_STATUS` | 枚举 | - | 无 | 引用枚举:WipStatus|
| 下道任务 | `nextManuTask` | `CNEXT_MANU_TASK` | 引用对象 | - | 无 | 引用ManuTask |

### 3.10 报工凭证（ReportProof）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `FactoryManaged`、`SecurityManaged` | **表名:** `MOM_REPORT_PROOF`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造订单 | `manuOrder` | `CMANU_ORDER` | 引用对象 | - | 必填 | 引用ManuOrder |
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 必填 | 引用ManuTask |
| 汇报人 | `reporter` | `CREPORTER` | 用户 | - | 必填 | |
| 汇报时间 | `reportTime` | `CREPORT_TIME` | 日期时间 | - | 必填 | |
| 合格数量 | `qualifiedQty` | `CQUALIFIED_QTY` | 浮点型 | - | 无 | 冗余回写字段（汇总） |
| 报废数量 | `scrappedQty` | `CSCRAPPED_QTY` | 浮点型 | - | 无 | 冗余回写字段（汇总） |

### 3.11 报工凭证明细（ReportProofItemLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** `SecurityManaged` | **表名:** `MOM_REPORT_PROOF_ITEM_LINK` | **源数据实体:** `ReportProof`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 必填 | 冗余 |
| 汇报项名称 | `itemName` | `CITEM_NAME` | 字符串 | 256 | 必填 | |
| 汇报项编码 | `itemCode` | `CITEM_CODE` | 字符串 | 256 | 必填 | |
| 汇报项类型 | `itemType` | `CITEM_TYPE` | 枚举 | 256 | 必填 | 引用：ReportItemType |
| 汇报项数量 | `qty` | `CQTY` | 浮点型 | - | 必填 | |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` |    | 256 | 无 | |

### 3.12 报工凭证执行人（ReportProofExecutorLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** `SecurityManaged` | **表名:** `MOM_REPORT_PROOF_EXECUTOR_LINK` | **源数据实体:** `ReportProof`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 必填 | 冗余 |
| 执行人 | `executor` | `CEXECUTOR` | 用户 | - | 必填 | |

### 3.13 制造订单分卡关系表（ManuOrderSplitRelationLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MANU_ORDER_SPLIT_RELATION_LINK` | **源数据实体:** `ManuOrder`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 新制造订单 | `manuOrder` | `CMANU_ORDER` | 引用对象 | - | 必填 | |
| 源制造任务 | `sourceManuTask` | `CSOURCE_MANU_TASK` | 引用对象 | - | 必填 | |
| 源根制造任务 | `sourceRootManuTask` | `CSOURCE_ROOT_MANU_TASK` | 引用对象 | - | 必填 | 非分割场景sourceManuTask和sourceRootManuTask值一致 |
| 分卡工序号 | `splitProcCode` | `CSPLIT_PROC_CODE` | 字符串 | 256 | 必填 | |
| 源制造订单根节点 | `rootSourceManuOrder` | `CROOT_SOURCE_MANU_ORDER` | 引用对象 | - | 必填 | |
| 源制造订单全路径 | `fullPathSourceManuOrder` | `CFULL_PATH_SOURCE_MANU_ORDER` | 字符串 | 1024 | 必填 | |
| 源制造任务根节点 | `rootSourceManuTask` | `CROOT_SOURCE_MANU_TASK` | 引用对象 | - | 必填 | |
| 源制造任务全路径 | `fullPathSourceManuTask` | `CFULL_PATH_SOURCE_MANU_TASK` | 字符串 | 1024 | 必填 | |
| 汇报项编码 | `itemCode` | `CITEM_CODE` | 字符串 | 256 | 无 | |
| 汇报项类型 | `itemType` | `CITEM_TYPE` | 字符串 | 256 | 无 | |
| 汇报项名称 | `itemName` | `CITEM_NAME` | 字符串 | 256 | 必填 | |
| 报工凭证 | `reportProof` | `CREPORT_PROOF` | 引用对象 | - | 无 | 用于追溯 |
| 源检验任务 | `originInspectTask` | `CORIGIN_INSPECT_TASK` | 引用对象 | - | 无 | |
| 检验报工凭证 | `inspectReportProof` | `CINSPECT_REPORT_PROOF` | 引用对象 | - | 无 | 用于追溯 |

### 3.14 工步报工凭证（StepReportProof）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `FactoryManaged` 、`SecurityManaged`| **表名:** `MOM_STEP_REPORT_PROOF`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 必填 | 引用ManuTask |
| 工步 | `step` | `CSTEP` | 引用对象 | - | 必填 | 引用RoutingProcessStepLink |
| 执行人       | `executor`   | `CEXECUTOR`    | 用户     | -    | 必填 |                            |
| 执行时间     | `executeTime` | `CEXECUTE_TIME` | 日期时间 | -    | 必填 | |

---

## 四、工时管理

### 4.1 工时明细（WorkHourDetail）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `FactoryManaged`、`SecurityManaged` | **表名:** `MOM_WORK_HOUR_DETAIL`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 必填 | 引用ManuTask |
| 执行人 | `executor` | `CEXECUTOR` | 用户 | - | 必填 | |
| 执行人工时 | `workHour` | `CWORK_HOUR` | 浮点型 | - | 必填 | |
| 工时单位 | `timeUnit` | `CTIME_UNIT` | 单位 | - | 必填 | |

---

## 五、质量检验

### 5.1 工艺检验分类配置（RoutingProcInspectCategory）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `FactoryManaged` | **表名:** `MOM_ROUTING_PROC_INSPECT_CATEGORY`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 序号 | `index` | `CINDEX` | 整型 | - | 必填 | 描述检验顺序：注意：自检存在时，其顺序必须第一 |
| 工艺 | `routing` | `CROUTING` | 引用对象 | - | 必填 | 引用Routing |
| 工序 | `routingProc` | `CROUTING_PROC` | 引用对象 | - | 无 | 若工序不为空则应用到工序，否则应用在整个工艺 |
| 检验分类 | `inspectCategory` | `CINSPECT_CATEGORY` | 枚举 | - | 必填 | 引用枚举:InspectCategory|
| 检验工作中心 | `inspectWorkCenter` | `CINSPECT_WORK_CENTER` | 引用对象 | - | 无 | 引用检验类的工作中心 |

### 5.2 检验任务（InspectTask）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged` | **表名:** `MOM_INSPECT_TASK`

**编码规则：** IT+10位流水

**说明**：该模型不继承生命周期，使用业务状态字段表示检验流程

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明                                                                                                                                                   |
|-------------|-------------|-----------|---------|------|------|------------------------------------------|
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 无 | 引用枚举:InspectTaskBizStatus                                                               |
| 生产订单 | `prodOrder` | `CPROD_ORDER` | 引用对象 | - | 无 | 引用ProdOrder                                                                                                                                          |
| 生产订单号 | `prodOrderCode` | `CPROD_ORDER_CODE` | 字符串 | 256 | 无 | 冗余存储（工控网隔离）                                                                                                                                          |
| 制造订单 | `manuOrder` | `CMANU_ORDER` | 引用对象 | - | 无 | 引用ManuOrder                                                                                                                                          |
| 制造订单号 | `manuOrderCode` | `CMANU_ORDER_CODE` | 字符串 | 256 | 无 | 冗余存储（工控网隔离）                                                                                                                                          |
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 无 | 引用ManuTask                                                                                                                                           |
| 制造任务号 | `manuTaskCode` | `CMANU_TASK_CODE` | 字符串 | 256 | 无 | 冗余存储（工控网隔离）                                                                                                                                          |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material                                                                                                                                           |
| 物料名称 | `materialName` | `CMATERIAL_NAME` | 字符串 | 256 | 无 | 冗余存储（工控网隔离）                                                                                                                                          |
| 物料编码 | `materialCode` | `CMATERIAL_CODE` | 字符串 | 256 | 无 | 冗余存储（工控网隔离）                                                                                                                                          |
| 物料图号 | `materialDwgNumber` | `CMATERIAL_DWG_NUMBER` | 字符串 | 256 | 无 | 冗余存储（工控网隔离）                                                                                                                                          |
| 物料版本 | `materialVersion` | `CMATERIAL_VERSION` | 字符串 | 256 | 无 | 冗余存储（工控网隔离）                                                                                                                                          |
| 工艺路线 | `routing` | `CROUTING` | 引用对象 | - | 无 | 引用Routing                                                                                                                                            |
| 工艺路线名称 | `routingName` | `CROUTING_NAME` | 字符串 | 256 | 无 | 冗余存储（工控网隔离）                                                                                                                                          |
| 工艺路线编码 | `routingCode` | `CROUTING_CODE` | 字符串 | 256 | 无 | 冗余存储（工控网隔离）                                                                                                                                          |
| 工艺路线版本 | `routingVersion` | `CROUTING_VERSION` | 字符串 | 256 | 无 | 冗余存储（工控网隔离）                                                                                                                                          |
| 工艺工序 | `routingProc` | `CROUTING_PROC` | 引用对象 | - | 无 | 引用RoutingProc                                                                                                                                        |
| 工序号 | `routingProcNum` | `CROUTING_PROC_NUM` | 字符串 | 256 | 无 | 冗余存储（工控网隔离）                                                                                                                                          |
| 工序名称 | `routingProcName` | `CROUTING_PROC_NAME` | 字符串 | 256 | 无 | 冗余存储（工控网隔离）                                                                                                                                          |
| 检验分类 | `inspectCategory` | `CINSPECT_CATEGORY` | 枚举 | - | 必填 | 引用枚举:InspectCategory|
| 检验工作中心 | `inspectWorkCenter` | `CINSPECT_WORK_CENTER` | 引用对象 | - | 无 | 引用WorkCenter                                                                                                                                         |
| 计划数量 | `plannedQty` | `CPLANNED_QTY` | 浮点型 | - | 必填 |                                                                                                                                                      |
| 已接收数量 | `receivedQty` | `CRECEIVED_QTY` | 浮点型 | - | 必填 | 默认为0，已接收数量总数，流转时刷新                                                                                                                                   |
| 合格数量 | `qualifiedQty` | `CQUALIFIED_QTY` | 浮点型 | - | 必填 | 默认为0，已汇报合格总数根据报工活动刷新                                                                                                                                 |
| 已报工数量 | `reportedQty` | `CREPORTED_QTY` | 浮点型 | - | 必填 | 默认为0，已报工总数根据报工活动刷新                                                                                                                                   |
| 可报工数量 | `reportableQty` | `CREPORTABLE_QTY` | 浮点型 | - | 必填 | 默认为0，可报工数量根据报工活动刷新                                                                                                                                   |
| 接收完毕标记 | `receiveFinishFlag` | `CRECEIVE_FINISH_FLAG` | 布尔 | - | 必填 | 默认false，表示接收是否完毕                                                                                                                                     |
| 计划开始时间 | `plannedStartTime` | `CPLANNED_START_TIME` | 日期时间 | - | 无 |                                                                                                                                                      |
| 计划结束时间 | `plannedEndTime` | `CPLANNED_END_TIME` | 日期时间 | - | 无 |                                                                                                                                                      |
| 实际开始时间 | `actualStartTime` | `CACTUAL_START_TIME` | 日期时间 | - | 无 |                                                                                                                                                      |
| 实际结束时间 | `actualEndTime` | `CACTUAL_END_TIME` | 日期时间 | - | 无 |                                                                                                                                                      |
| 控制状态 | `controlStatus` | `CCONTROL_STATUS` | 枚举 | - | 必填 | 引用枚举:controlStatus|
| 启用序列号标记 | `serialNumberFlag` | `CSERIAL_NUMBER_FLAG` | 布尔 | - | 无 |                                                                                                                                                      |
| 执行标记 | `executionFlag` | `CEXECUTION_FLAG` | 布尔 | - | 无 |                                                                                                                                                      |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 |                                                                                                                                                      |
| 序号 | `index` | `CINDEX` | 整型 | - | 必填 | 同一加工任务内的检验任务顺序                                                                                                                                       |
| 报废数量 | `scrappedQty` | `CSCRAPPED_QTY` | 浮点型 | - | 无 | 冗余回写字段                                                                                                                                               |
| 待定数量 | `pendingQty` | `CPENDING_QTY` | 浮点型 | - | 无 | 冗余回写字段                                                                                                                                               |

### 5.3 检验任务接收序列号（InspectTaskReceivedSnLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** `FactoryManaged` | **表名:** `MOM_INSPECT_TASK_RECEIVED_SN_LINK` | **源数据实体:** `InspectTask`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 必填 | |
| 已报工标记 | `reportedFlag` | `CREPORTED_FLAG` | 布尔 | - | 必填 | 默认false |

### 5.4 检验任务动作变迁记录（InspectActionRecordLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_INSPECT_ACTION_RECORD_LINK` | **源数据实体:** `InspectTask`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 操作人 | `operator` | `COPERATOR` | 长整型 | - | 必填 | 操作人ID |
| 操作人编码 | `operatorCode` | `COPERATOR_CODE` | 字符串 | 256 | 必填 | |
| 操作人名称 | `operatorName` | `COPERATOR_NAME` | 字符串 | 256 | 必填 | |
| 操作时间 | `operatorTime` | `COPERATOR_TIME` | 日期时间 | - | 必填 | |
| 操作员IP | `operatorIp` | `COPERATOR_IP` | 字符串 | 256 | 无 | |
| 操作 | `action` | `CACTION` | 字符串 | 256 | 无 | |
| 操作内容 | `actionContent` | `CACTION_CONTENT` | CLOB | - | 无 | |
| 状态变动标记 | `statusChangeFlag` | `CSTATUS_CHANGE_FLAG` | 布尔 | - | 无 | |
| 当前状态 | `currentStatus` | `CCURRENT_STATUS` | 字符串 | 256 | 无 | 业务状态 |
| 目标状态 | `targetStatus` | `CTARGET_STATUS` | 字符串 | 256 | 无 | 业务状态 |

### 5.5 检验报工凭证（InspectReportProof）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `FactoryManaged`、、`SecurityManaged` | **表名:** `MOM_INSPECT_REPORT_PROOF`

**编码规则：** ITRP+10位数字

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 报工凭证编号 | `code` | `CCODE` | 字符串 | 256 | 必填 | ITRP+10位数字 |
| 检验任务 | `inspectTask` | `CINSPECT_TASK` | 引用对象 | - | 必填 | 引用InspectTask |
| 制造订单 | `manuOrder` | `CMANU_ORDER` | 引用对象 | - | 无 | 引用ManuOrder |
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 无 | 引用ManuTask |
| 汇报人 | `reporter` | `CREPORTER` | 用户 | - | 必填 | |
| 汇报时间 | `reportTime` | `CREPORT_TIME` | 日期时间 | - | 必填 | |
| 合格数量 | `qualifiedQty` | `CQUALIFIED_QTY` | 浮点型 | - | 无 | 冗余回写字段（汇总） |

### 5.6 检验报工凭证明细（InspectReportProofItemLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** `SecurityManaged`、`FactoryManaged` | **表名:** `MOM_INSPECT_REPORT_PROOF_ITEM_LINK` | **源数据实体:** `InspectReportProof`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 检验任务 | `inspectTask` | `CINSPECT_TASK` | 引用对象 | - | 必填 | 引用InspectTask |
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 无 | 冗余 |
| 汇报项名称 | `itemName` | `CITEM_NAME` | 字符串 | 256 | 必填 | |
| 汇报项编码 | `itemCode` | `CITEM_CODE` | 字符串 | 256 | 必填 | 配置项的实际值 |
| 汇报项类型 | `itemType` | `CITEM_TYPE` | 字符串 | 256 | 必填 | 合格/待定/报废 |
| 汇报项数量 | `qty` | `CQTY` | 浮点型 | - | 必填 | 序列号时为1 |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | |
| 不合格结论标记 | `defectiveConclusionFlag` | `CDEFECTIVE_CONCLUSION_FLAG` | 布尔 | - | 无 | 默认false，true表示来自不合格审理的结论 |
| 分卡标记 | `splitFlag` | `CSPLIT_FLAG` | 布尔 | - | 无 | 默认false |

### 5.7 检验报工凭证执行人（InspectReportProofExecutorLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** `SecurityManaged`、`FactoryManaged` | **表名:** `MOM_INSPECT_REPORT_PROOF_EXECUTOR_LINK` | **源数据实体:** `InspectReportProof`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 检验任务 | `inspectTask` | `CINSPECT_TASK` | 引用对象 | - | 必填 | 引用InspectTask |
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 无 | 冗余 |
| 执行人 | `executor` | `CEXECUTOR` | 用户 | - | 必填 | |

### 5.8 质量填报模版（QMRecordTmpl）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`LifecycleManaged` | **表名:** `MOM_QM_RECORD_TMPL`

**生命周期模板**：COMMON_LIFECYCLE

**编码规则：** QRT+6位数字 (QRT000001至QRT999999)，全局唯一

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 主填报模型 | `masterRecordEntityType` | `CMASTER_RECORD_ENTITY_TYPE` | 字符串 | 128 | 无 | 质量模版对应的主要的填报数据模型类型（即对象类编码）此类模型必须扩展QMRecordManaged接口 |
| 数据查询url | `browseDataApiUrl` | `CBROWSE_DATA_API_URL` | 字符串 | 512 | 无 | |
| 数据保存url | `inputDataApiUrl` | `CINPUT_DATA_API_URL` | 字符串 | 512 | 无 | |
| 设计内容 | `designContent` | `CDESIGN_CONTENT` | CLOB | - | 无 | 存储设计json |

### 5.9 质量填报模版关联（QMRecordTmplBindLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** `FactoryManaged` | **表名:** `MOM_QM_RECORD_TMPL_BIND_LINK` | **源数据实体:** `QMRecordTmpl`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 序号 | `index` | `CINDEX` | 整型 | - | 必填 | |
| 绑定数据模型 | `bindEntityType` | `CBIND_ENTITY_TYPE` | 枚举 | - | 必填 | 引用枚举:QM_RECORD_BIND_ENTITY_TYPE|
| 绑定数据对象id | `bindObjectId` | `CBIND_OBJECT_ID` | 长整型 | - | 必填 | 表示应用此模版的数据对象，例如具体的物料、工艺路线、工序等数据对象id |

### 5.10 质量填报模板规范约定及建模实例

**说明：** 检验填报实体需要实现`QMRecordManaged`接口。除了必要属性外，其他自定义属性应该允许为空，由业务来决定是否必填。

#### 5.10.1 质量填报接口（QMRecordManaged）

**接口要求：** 实现`QMRecordManaged`接口的模型必须包含以下属性：

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造订单 | `manuOrder` | `CMANU_ORDER` | 引用对象 | - | 无 | 引用ManuOrder |
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 无 | 引用ManuTask |
| 检验任务 | `inspectTask` | `CINSPECT_TASK` | 引用对象 | - | 无 | 引用InspectTask |
| 质量填报模版编码 | `qmRecordTmplCode` | `CQM_RECORD_TMPL_CODE` | 字符串 | 256 | 无 | |

#### 5.10.2 靶材制造部熔炼填报（QmSmeltReport）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `QMRecordManaged` | **表名:** `MOM_QM_SMELT_REPORT`

**说明：** 填报模板模型实例，项目可参考进行新模板建模或者扩展

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 材质清洗方式 | `czqxfs` | `CCZQXFS` | 字符串 | 256 | 无 | |
| 材质名称1 | `czmc1` | `CCZMC1` | 字符串 | 256 | 无 | |
| 材质批号1 | `czph1` | `CCZPH1` | 字符串 | 256 | 无 | |
| 材质名称2 | `czmc2` | `CCZMC2` | 字符串 | 256 | 无 | |
| 材质批号2 | `czph2` | `CCZPH2` | 字符串 | 256 | 无 | |
| 重量2 | `zl2` | `CZL2` | 浮点型 | - | 无 | |
| 材质名称3 | `czmc3` | `CCZMC3` | 字符串 | 256 | 无 | |
| 重量3 | `zl3` | `CZL3` | 浮点型 | - | 无 | |
| 重量1 | `zl1` | `CZL1` | 浮点型 | - | 无 | |
| 材质批号3 | `czph3` | `CCZPH3` | 字符串 | 256 | 无 | |
| 材质名称4 | `czmc4` | `CCZMC4` | 字符串 | 256 | 无 | |
| 材质批号4 | `czph4` | `CCZPH4` | 字符串 | 256 | 无 | |
| 重量4 | `zl4` | `CZL4` | 浮点型 | - | 无 | |
| 材质名称5 | `czmc5` | `CCZMC5` | 字符串 | 256 | 无 | |
| 材质批号5 | `czph5` | `CCZPH5` | 字符串 | 256 | 无 | |
| 重量5 | `zl5` | `CZL5` | 浮点型 | - | 无 | |
| 材质名称6 | `czmc6` | `CCZMC6` | 字符串 | 256 | 无 | |
| 材质批号6 | `czph6` | `CCZPH6` | 字符串 | 256 | 无 | |
| 重量6 | `zl6` | `CZL6` | 浮点型 | - | 无 | |
| 单炉配料 | `dlpl` | `CDLPL` | 字符串 | 256 | 无 | |
| 炉次 | `lc` | `CLC` | 字符串 | 256 | 无 | |
| 配料人 | `plr` | `CPLR` | 字符串 | 256 | 无 | |
| 核准人 | `hzr` | `CHZR` | 字符串 | 256 | 无 | |
| 设备名称 | `equipName` | `CEQUIP_NAME` | 字符串 | 256 | 无 | |
| 涂料材质 | `tlcz` | `CTLCZ` | 字符串 | 256 | 无 | |
| 模具温度 | `mjwd` | `CMJWD` | 浮点型 | - | 无 | |
| 坩埚尺寸 | `gwcq` | `CGWCQ` | 字符串 | 256 | 无 | |
| 坩埚材质 | `gwcz` | `CGWCZ` | 字符串 | 256 | 无 | |
| 模具尺寸 | `mjcq` | `CMJCQ` | 字符串 | 256 | 无 | |
| 模具材质 | `mjcz` | `CMJCZ` | 字符串 | 256 | 无 | |
| 主操作 | `zcz` | `CZCZ` | 字符串 | 256 | 无 | |
| 铸锭尺寸 | `zdcc` | `CZDCC` | 字符串 | 256 | 无 | |
| 副操作 | `fcz` | `CFCZ` | 字符串 | 256 | 无 | |
| 铸锭缺陷 | `zdqx` | `CZDQX` | 字符串 | 256 | 无 | |

#### 5.10.3 靶材制造部熔炼操作（QmSmeltReportOptLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** `QMRecordManaged` | **表名:** `MOM_QM_SMELT_REPORT_OPT_LINK` | **源数据实体:** `QmSmeltReport`

**说明：** 填报模板模型实例，项目可参考进行新模板建模或者扩展

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 操作项 | `optItem` | `COPT_ITEM` | 字符串 | 256 | 无 | |
| 真空度 | `vacuumDegree` | `CVACUUM_DEGREE` | 字符串 | 256 | 无 | |
| 功率 | `power` | `CPOWER` | 字符串 | 256 | 无 | |
| 备注 | `remark` | `CREMARK` | 字符串 | 256 | 无 | |
| 操作时间 | `optDate` | `COPT_DATE` | 字符串 | 256 | 无 | |

#### 5.10.4 靶材制造部熔炼记录（QmSmeltReportRecordLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** `QMRecordManaged` | **表名:** `MOM_QM_SMELT_REPORT_RECORD_LINK` | **源数据实体:** `QmSmeltReport`

**说明：** 填报模板模型实例，项目可参考进行新模板建模或者扩展

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 配料 | `pl` | `CPL` | 字符串 | 256 | 无 | |
| 铸锭 | `zd` | `CZD` | 字符串 | 256 | 无 | |
| 损耗 | `loss` | `CLOSS` | 字符串 | 256 | 无 | |
| 平衡 | `ph` | `CPH` | 字符串 | 256 | 无 | |

### 5.11 不合格品审理单（DefectiveProductReview）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`LifecycleManaged` | **表名:** `MOM_DEFECTIVE_PRODUCT_REVIEW`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 源制造任务 | `sourceManuTask` | `CSOURCE_MANU_TASK` | 引用对象 | - | 无 | 引用ManuTask |
| 检验任务 | `inspectTask` | `CINSPECT_TASK` | 引用对象 | - | 无 | |
| 审理结论类型 | `conclusionType` | `CCONCLUSION_TYPE` | 枚举 | - | 无 | 引用枚举:DefectiveProductReviewConclusionType|
| 汇报项编码 | `itemCode` | `CITEM_CODE` | 字符串 | 256 | 无 | |
| 汇报项类型 | `itemType` | `CITEM_TYPE` | 字符串 | 256 | 无 | |
| 汇报项名称 | `itemName` | `CITEM_NAME` | 字符串 | 256 | 无 | |
| 报工凭证 | `reportProof` | `CREPORT_PROOF` | 引用对象 | - | 无 | 用于追溯 |
| 检验报工凭证 | `inspectReportProof` | `CINSPECT_REPORT_PROOF` | 引用对象 | - | 无 | 用于追溯 |
| 数量 | `qty` | `CQTY` | 浮点型 | - | 无 | |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 无 | 引用Material |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | |

### 5.12 不合格品主件审理结论（DefectiveProductReviewConclusionLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_DEFECTIVE_PRODUCT_REVIEW_CONCLUSION_LINK` | **源数据实体:** `DefectiveProductReview`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | |
| 数量 | `qty` | `CQTY` | 浮点型 | - | 无 | |
| 结论 | `reviewConclusion` | `CREVIEW_CONCLUSION` | 枚举 | - | 无 | 引用枚举:ReviewConclusion|
| 分卡标记 | `splitFlag` | `CSPLIT_FLAG` | 布尔 | - | 无 | 是否分卡 |
| 状态 | `status` | `CSTATUS` | 枚举 | - | 无 | 引用枚举:DefectiveReviewConclusionStatus|
| 备注 | `remark` | `CREMARK` | 字符串 | 1024 | 无 | |

### 5.13 不合格品子件审理结论（DefectiveReviewSubConclusionLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_DEFECTIVE_REVIEW_SUB_CONCLUSION_LINK` | **源数据实体:** `DefectiveProductReview`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 主件序列号 | `mainPartSerialNumber` | `CMAIN_PART_SERIAL_NUMBER` | 字符串 | 256 | 无 | |
| 生产厂家 | `manufacturer` | `CMANUFACTURER` | 引用对象 | - | 无 | 引用BizOrg |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 无 | 引用Material |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | |
| 数量 | `qty` | `CQTY` | 浮点型 | - | 无 | |
| 结论 | `reviewConclusion` | `CREVIEW_CONCLUSION` | 枚举 | - | 无 | 引用枚举:ReviewConclusion|
| 状态 | `status` | `CSTATUS` | 枚举 | - | 无 | 引用枚举:DefectiveReviewConclusionStatus|
| 备注 | `remark` | `CREMARK` | 字符串 | 1024 | 无 | |

### 5.14 质量方案（QualityScheme）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `IntegrationManaged` | **表名:** `MOM_QUALITY_SCHEME`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 方案类型 | `schemeType` | `CSCHEME_TYPE` | 枚举 | - | 必填 | 引用枚举:QualitySchemeTypeEnum |
| 启用标记 | `enabledFlag` | `CENABLED_FLAG` | 布尔 | - | 无 | 默认true |

### 5.15 质量方案检验分类（QualitySchemeInspectLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_QUALITY_SCHEME_INSPECT_LINK` | **源数据实体:** `QualityScheme`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 质量方案 | `source` | `CSOURCE` | 引用对象 | - | 必填 | 引用QualityScheme |
| 检验分类 | `inspectCategory` | `CINSPECT_CATEGORY` | 枚举 | - | 无 | 引用枚举:inspectCategory |
| 检验工作中心 | `inspectWorkCenter` | `CINSPECT_WORK_CENTER` | 引用对象 | - | 无 | 引用WorkCenter |

### 5.16 质量方案检查项（QualitySchemeCheckItemLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_QUALITY_SCHEME_CHECK_ITEM_LINK` | **源数据实体:** `QualityScheme`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 质量方案 | `source` | `CSOURCE` | 引用对象 | - | 必填 | 引用QualityScheme |
| 编码 | `code` | `CCODE` | 字符串 | 256 | 无 | |
| 名称 | `name` | `CNAME` | 字符串 | 256 | 必填 | |
| 工装 | `tooling` | `CTOOLING` | 引用对象 | - | 无 | 引用Material |
| 检验特征 | `characteristicType` | `CCHARACTERISTIC_TYPE` | 枚举 | - | 必填 | 引用枚举:inspectCharacteristicType |
| 标准值 | `standardValue` | `CSTANDARD_VALUE` | 字符串 | 256 | 无 | |
| 上限值 | `upperLimit` | `CUPPER_LIMIT` | 浮点型 | - | 无 | |
| 下限值 | `lowerLimit` | `CLOWER_LIMIT` | 浮点型 | - | 无 | |
| 检验方法 | `inspectionMethod` | `CINSPECTION_METHOD` | 字符串 | 256 | 无 | |

### 5.17 质量方案与质量记录模板（QualitySchemeReportTmplLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_QUALITY_SCHEME_REPORT_TMPL_LINK` | **源数据实体:** `QualityScheme`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 质量方案 | `source` | `CSOURCE` | 引用对象 | - | 必填 | 引用QualityScheme |
| 质量记录模板 | `reportTmpl` | `CREPORT_TMPL` | 引用对象 | - | 必填 | 引用QMRecordTmpl |

### 5.18 工艺质量方案配置（RoutingQualitySchemeConfig）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_ROUTING_QUALITY_SCHEME_CONFIG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 工艺路线 | `routing` | `CROUTING` | 引用对象 | - | 无 | 引用Routing |
| 工艺工序 | `routingProc` | `CROUTING_PROC` | 引用对象 | - | 无 | 引用RoutingProcessLink |
| 过程检验质量方案 | `ipqcQualityScheme` | `CIPQC_QUALITY_SCHEME` | 引用对象 | - | 无 | 引用QualityScheme |

### 5.19 物料质量方案配置（MaterialQualitySchemeConfig）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_MATERIAL_QUALITY_SCHEME_CONFIG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 无 | 引用Material |
| 入厂检验质量方案 | `iqcQualityScheme` | `CIQC_QUALITY_SCHEME` | 引用对象 | - | 无 | 引用QualityScheme |
| 过程检验质量方案 | `ipqcQualityScheme` | `CIPQC_QUALITY_SCHEME` | 引用对象 | - | 无 | 引用QualityScheme |
| 出厂检验质量方案 | `oqcQualityScheme` | `COQC_QUALITY_SCHEME` | 引用对象 | - | 无 | 引用QualityScheme |

### 5.20 组织质量方案配置（OrgDefaultQualitySchemeConfig）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_ORG_DEFAULT_QUALITY_SCHEME_CONFIG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 入厂检验质量方案 | `iqcQualityScheme` | `CIQC_QUALITY_SCHEME` | 引用对象 | - | 无 | 引用QualityScheme |
| 过程检验质量方案 | `ipqcQualityScheme` | `CIPQC_QUALITY_SCHEME` | 引用对象 | - | 无 | 引用QualityScheme |
| 出厂检验质量方案 | `oqcQualityScheme` | `COQC_QUALITY_SCHEME` | 引用对象 | - | 无 | 引用QualityScheme |
| 业务组织 | `bizOrg` | `CBIZ_ORG` | 引用对象 | - | 必填 | 引用BizOrg |

### 5.21 质量检查项记录（QualityCheckItemRecord）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `SecurityManaged`、`FactoryManaged` | **表名:** `MOM_QUALITY_CHECK_ITEM_RECORD`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 无 | 引用ManuTask |
| 检验任务 | `inspectTask` | `CINSPECT_TASK` | 引用对象 | - | 无 | 引用InspectTask |
| 来源质量方案 | `sourceQualityScheme` | `CSOURCE_QUALITY_SCHEME` | 引用对象 | - | 必填 | 引用QualityScheme |
| 来源质量方案检查项 | `sourceCheckItemLink` | `CSOURCE_CHECK_ITEM_LINK` | 引用对象 | - | 必填 | 引用QualitySchemeCheckItemLink |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | |
| 实测值 | `actualValue` | `CACTUAL_VALUE` | 字符串 | 256 | 无 | |
| 实测结果 | `actualResult` | `CACTUAL_RESULT` | 枚举 | - | 必填 | 引用枚举:QualityCheckItemResultType |
| 来源任务类型 | `sourceTaskType` | `CSOURCE_TASK_TYPE` | 字符串 | 256 | 必填 | |
---

## 六、外委管理

### 6.1 外委需求（OutsourcingRequire）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`SecurityManaged`、`LifecycleManaged` | **表名:** `MOM_OUTSOURCING_REQUIRE`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造订单 | `manuOrder` | `CMANU_ORDER` | 引用对象 | - | 无 | 引用ManuOrder |
| 工作中心 | `workCenter` | `CWORK_CENTER` | 引用对象 | - | 无 | 引用WorkCenter |
| 供应商 | `supplier` | `CSUPPLIER` | 引用对象 | - | 无 | 引用BizOrg |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |
| 预计发货数量 | `estimatedShipQty` | `CESTIMATED_SHIP_QTY` | 浮点型 | - | 必填 | |
| 预计收货数量 | `estimatedReceiveQty` | `CESTIMATED_RECEIVE_QTY` | 浮点型 | - | 必填 | |
| 预计发货时间 | `estimatedShipDate` | `CESTIMATED_SHIP_DATE` | 日期时间 | - | 无 | |
| 要求交付时间 | `requiredDeliveryDate` | `CREQUIRED_DELIVERY_DATE` | 日期时间 | - | 无 | |
| 外委类型 | `outsourcingType` | `COUTSOURCING_TYPE` | 枚举 | - | 必填 | 引用枚举:OutsourcingType|
| 来源类型 | `sourceType` | `CSOURCE_TYPE` | 枚举 | - | 必填 | 引用枚举:outsourcingSourceType|
| 是否连续外委 | `continuousFlag` | `CCONTINUOUS_FLAG` | 布尔 | - | 无 | |
| 不合格品子件审理结论 | `defectiveReviewSubConclusion` | `CDEFECTIVE_REVIEW_SUB_CONCLUSION` | 引用对象 | - | 无 | |
| 业务状态             | `bizStatus`                    | `CBIZ_STATUS`                     | 枚举     | -    | 必填 | 引用枚举:OutsourcingRequireBizStatus |

### 6.2 外委需求明细（OutsourcingRequireDetailLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_OUTSOURCING_REQUIRE_DETAIL_LINK` | **源数据实体:** `OutsourcingRequire`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 必填 | 引用ManuTask |
| 数量 | `qty` | `CQTY` | 浮点型 | - | 无 | |
| 是否首道标记 | `isFirst` | `CIS_FIRST` | 布尔 | - | 无 | 记录连续工序的头工序 |
| 是否末道标记 | `isLast` | `CIS_LAST` | 布尔 | - | 无 | 记录连续工序的尾工序 |

### 6.3 外委采购订单（OutsourcingPurchaseOrder）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`SecurityManaged` | **表名:** `MOM_OUTSOURCING_PURCHASE_ORDER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| PO号 | `poNumber` | `CPO_NUMBER` | 字符串 | 256 | 无 | erp来源 |
| 行号 | lineNum | CLINE_NUM | 字符串 | 256 | 无 | erp来源 |
| 计划数量 | `plannedQty` | `CPLANNED_QTY` | 浮点型 | - | 必填 | |
| 已发货数量 | `shippedQty` | `CSHIPPED_QTY` | 浮点型 | - | 无 | |
| 已收货数量 | `receivedQty` | `CRECEIVED_QTY` | 浮点型 | - | 无 | |
| 退货数量 | `returnQty` | `CRETURN_QTY` | 浮点型 | - | 无 | |
| 外委需求 | `outsourcingRequire` | `COUTSOURCING_REQUIRE` | 引用对象 | - | 无 | 引用OutsourcingRequire |
| 供应商 | `supplier` | `CSUPPLIER` | 引用对象 | - | 无 | 引用BizOrg |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 无 | 引用Material |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填 | 引用枚举:OutsourcingPurchaseOrderBizStatus |

### 6.4 外委发货单（OutsourcingDeliveryOrder）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`SecurityManaged` | **表名:** `MOM_OUTSOURCING_DELIVERY_ORDER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 发货物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |
| 发货数量 | `qty` | `CQTY` | 浮点型 | - | 必填 | |
| 采购订单 | `purchaseOrder` | `CPURCHASE_ORDER` | 引用对象 | - | 无 | |

### 6.5 外委收货单（OutsourcingReceiptOrder）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`SecurityManaged` | **表名:** `MOM_OUTSOURCING_RECEIPT_ORDER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 收货物料 | `material` | `CMATERIAL` | 引用对象 | - | 无 | 引用Material |
| 收货数量 | `receiptQty` | `CRECEIPT_QTY` | 浮点型 | - | 必填 | |
| 退货数量 | `returnQty` | `CRETURN_QTY` | 浮点型 | - | 无 | |
| 收货类型 | `receiptType` | `CRECEIPT_TYPE` | 枚举 | - | 无 | 引用枚举:outsourcingReceiptType|
| 采购订单 | `purchaseOrder` | `CPURCHASE_ORDER` | 引用对象 | - | 无 | |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填 | 引用枚举:OutsourcingReceiptOrderBizStatus |

### 6.6 外委收货单明细（OutsourcingReceiptOrderLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_OUTSOURCING_RECEIPT_ORDER_LINK` | **源数据实体:** `OutsourcingReceiptOrder`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 引用对象 | - | 无 | |
| 是否退货 | `isReturned` | `CIS_RETURNED` | 布尔 | - | 无 | |

### 6.7 外委退货单（OutsourcingReturnOrder）

**模型类型:** 业务模型 | **父模型:** `BusinessObject ` | **接口:** `FactoryManaged`、`SecurityManaged`、 | **表名:** `MOM_OUTSOURCING_RETURN_ORDER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 退货单类型 | `returnType` | `CRETURN_TYPE` | 枚举 | - | 无 | 引用枚举:OutsourcingReturnType |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |
| 退货数量 | `returnQty` | `CRETURN_QTY` | 浮点型 | - | 必填 | |
| 退货原因 | `returnReason` | `CRETURN_REASON` | 字符串 | 512 | 必填 | |
| 收货单 | `receiptOrder` | `CRECEIPT_ORDER` | 引用对象 | - | 无 | |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填 | 引用枚举:OutsourcingReturnOrderBizStatus |

---

## 七、采购管理（待需求确认）

### 7.1 采购需求（PurchaseRequisition）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`SecurityManaged`、`LifecycleManaged` | **表名:** `MOM_PURCHASE_REQUISITION`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 申请人 | `requester` | `CREQUESTER` | 引用对象 | - | 必填 | |
| 需求日期 | `requirementDate` | `CREQUIREMENT_DATE` | 日期时间 | - | 必填 | |
| 优先级 | `priorityLevel` | `CPRIORITY_LEVEL` | 枚举 | - | 无 | 引用枚举:PriorityLevel 和生产订单优先级一样 |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |
| 数量 | `qty` | `CQTY` | 浮点型 | - | 必填 | |
| 期望到货时间 | `expectedArrivalTime` | `CEXPECTED_ARRIVAL_TIME` | 日期时间 | - | 必填 | |
| 供应商 | `supplier` | `CSUPPLIER` | 引用对象 | - | 无 | 引用BizOrg |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填 | 引用枚举:PurchaseRequisitionBizStatus |

### 7.2 采购订单（PurchaseOrder）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`SecurityManaged` | **表名:** `MOM_PURCHASE_ORDER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| PO号 | `poNumber` | `CPO_NUMBER` | 字符串 | 256 | 无 | erp来源 |
| 行号 | lineNum | CLINE_NUM | 字符串 | 256 | 无 | erp来源 |
| 采购需求 | `purchaseRequisition` | `CPURCHASE_REQUISITION` | 引用对象 | - | 无 | 引用PurchaseRequisition |
| 供应商 | `supplier` | `CSUPPLIER` | 引用对象 | - | 无 | 引用BizOrg |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 无 | 引用Material |
| 计划数量 | `plannedQty` | `CPLANNED_QTY` | 浮点型 | - | 必填 | |
| 已收货数量 | `receivedQty` | `CRECEIVED_QTY` | 浮点型 | - | 无 | |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填 | 引用枚举:PurchaseOrderBizStatus |

### 7.3 采购收货单（PurchaseReceipt）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`SecurityManaged` | **表名:** `MOM_PURCHASE_RECEIPT`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 收货物料 | `material` | `CMATERIAL` | 引用对象 | - | 无 | 引用Material |
| 收货数量 | `receiptQty` | `CRECEIPT_QTY` | 浮点型 | - | 必填 | |
| 退货数量 | `returnQty` | `CRETURN_QTY` | 浮点型 | - | 无 | |
| 采购订单 | `purchaseOrder` | `CPURCHASE_ORDER` | 引用对象 | - | 无 | 引用PurchaseOrder |
| 库房 | `warehouse` | `CWAREHOUSE` | 引用对象 | - | 必填 | |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填 | 引用枚举:PurchaseReceiptBizStatus |

### 7.4 采购收货单明细（PurchaseReceiptLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_PURCHASE_RECEIPT_LINK` | **源数据实体:** `PurchaseReceipt`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 引用对象 | - | 无 | |
| 是否退货 | `isReturned` | `CIS_RETURNED` | 布尔 | - | 无 | |

### 7.5 采购退货单（PurchaseReturn）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `FactoryManaged`、`SecurityManaged`、`LifecycleManaged` | **表名:** `MOM_PURCHASE_RETURN`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |
| 退货数量 | `returnQty` | `CRETURN_QTY` | 浮点型 | - | 必填 | |
| 退货原因 | `returnReason` | `CRETURN_REASON` | 字符串 | 512 | 必填 | |
| 收货单 | `purchaseReceipt` | `CPURCHASE_RECEIPT` | 引用对象 | - | 无 | 引用PurchaseReceipt |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填 | 引用枚举:PurchaseReturnBizStatus |

---

## 八、生产异常

### 8.1 异常类别（AbnormalCategory）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** 无 | **表名:** `MOM_ABNORMAL_CATEGORY`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 流程标识 | `flowCode` | `CFLOW_CODE` | 字符串 | 256 | 无 | |
| 是否预定义 | `predefinedFlag` | `CPREDEFINED_FLAG` | 布尔 | - | 必填 | 默认值：false |

### 8.2 异常描述库（AbnormalDescription）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** 无 | **表名:** `MOM_ABNORMAL_DESCRIPTION`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 异常类别 | `abnormalCategory` | `CABNORMAL_CATEGORY` | 引用对象 | - | 必填 | 引用AbnormalCategory |
| 异常描述 | `abnormalDescription` | `CABNORMAL_DESCRIPTION` | 字符串 | 4000 | 必填 | |

### 8.3 异常任务（AbnormalTask）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`LifecycleManaged` | **表名:** `MOM_ABNORMAL_TASK`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 异常类别 | `abnormalCategory` | `CABNORMAL_CATEGORY` | 引用对象 | - | 必填 | 引用AbnormalCategory |
| 异常描述 | `abnormalDesc` | `CABNORMAL_DESC` | 字符串 | 4000 | 无 | |
| 处理措施 | `processMeasures` | `CPROCESS_MEASURES` | 字符串 | 4000 | 无 | |
| 异常原因 | `abnormalCause` | `CABNORMAL_CAUSE` | 字符串 | 4000 | 无 | |
| 需求解决时间 | `requiredFinishTime` | `CREQUIRED_FINISH_TIME` | 日期时间 | - | 无 | |
| 处理人 | `handler` | `CHANDLER` | 用户 | - | 必填 | |
| 设备 | `equip` | `CEQUIP` | 引用对象 | - | 无 | 根据异常类别判断是否必填 |
| 处理完成时间 | `promiseResolutionTime` | `CPROMISE_RESOLUTION_TIME` | 日期时间 | - | 无 | |
| 关闭人 | `closer` | `CCLOSER` | 用户 | - | 无 | |
| 关闭时间 | `closeTime` | `CCLOSE_TIME` | 日期时间 | - | 无 | |
| 发起人 | `initiator` | `CINITIATOR` | 用户 | - | 无 | |
| 关闭说明 | `closureExplanation` | `CCLOSURE_EXPLANATION` | CLOB | - | 无 | |

### 8.4 异常操作记录（AbnormalTaskLogLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_ABNORMAL_TASK_LOG_LINK` | **源数据实体:** `AbnormalTask`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 操作类型 | `operationType` | `COPERATION_TYPE` | 枚举 | - | 必填 | 引用枚举:AbnormalOperationType|
| 操作描述 | `operationDesc` | `COPERATION_DESC` | 字符串 | 256 | 必填 | |
| 操作人 | `operator` | `COPERATOR` | 用户 | - | 必填 | |
| 操作时间 | `operationTime` | `COPERATION_TIME` | 日期时间 | - | 必填 | |

### 8.5 生产异常任务与附件关系（AbnormalTaskFileLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_ABNORMAL_TASK_FILE_LINK` | **源数据实体:** `AbnormalTask`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 附件 | `attachment` | `CATTACHMENT` | 引用对象 | - | 必填 | 引用MOM_ATTACHMENT |

### 8.6 生产异常任务与制造任务关系（AbnormalTaskManuTaskLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_ABNORMAL_TASK_MANU_TASK_LINK` | **源数据实体:** `AbnormalTask`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 制造任务 | `manuTask` | `CMANU_TASK` | 引用对象 | - | 必填 | 引用ManuTask |

### 8.7 生产异常任务与检验任务关系（AbnormalTaskInspectTaskLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_ABNORMAL_TASK_INSPECT_TASK_LINK` | **源数据实体:** `AbnormalTask`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 检验任务 | `inspectTask` | `CINSPECT_TASK` | 引用对象 | - | 必填 | |

---

## 变更记录

| 日期 | 版本 | 变更内容 | 变更人 |
|-----|------|---------|-----|
| 2026-04-22 | v1.13 | 补充质量方案相关模型：质量方案、质量方案检查项、质量方案配置及质量检查项记录等 | 薛启宽 |
| 2026-04-08 | v1.12 | 调整到货位置字段归属：从制造任务（ManuTask）移至物料准备计划明细（MaterialPreparationPlanDetailLink） | Codex |
| 2026-03-30 | v1.11 | 在物料准备计划明细（MaterialPreparationPlanDetailLink）中增加到货位置引用属性，引用LogisticsLocation模型 | 危放 |
| 2026-02-25 | v1.10 | 删除检验任务（InspectTask）模型中的不合格审理状态字段 | 危放 |
| 2026-01-26 | v1.9 | 优化MES数据模型属性定义：统一术语表达（物料清单→BOM、顺序号→序列号等），补充字段说明，完善引用对象标注；修正数据类型（汇报项类型改为枚举）和模型结构（MaterialLoadList父模型调整等）；删除冗余字段，补充必要字段（制造订单已申请报废入库数量、制造任务在制品数量等） | 李鸿坤 |
| 2026-01-26 | v1.8 | 修复引用枚举类型编码，确保与数据库定义一致| 危放  |
| 2026-01-23 | v1.7 | 修复关系实体源数据实体元信息：为33个继承GenericLink的关系模型添加源数据实体标注，符合数据模型规范要求 | Claude |
| 2026-01-09 | v1.6 | 统一业务状态枚举引用格式：将ProdOrder、ManuOrder、ManuTask、MaterialPreparationPlan等模型的业务状态字段改为引用枚举格式 | 李鸿坤 |
| 2026-01-09 | v1.5 | 统一所有单位、枚举、分类的引用格式为"引用XX:编码"规范格式 | 危放 |
| 2025-12-29 | v1.4 | 改造业务属性为引用格式 | 王晴 |
| 2025-12-29 | v1.3 | 优化生命周期继承和业务状态：InspectTask不继承LifecycleManaged接口，添加bizStatus属性字段；QMRecordTmpl使用COMMON_LIFECYCLE | 危放  |
| 2025-12-19 | v1.2 | 补充质量检验模块相关模型：检验分类配置、检验任务、检验报工凭证、质量填报模版等 | 危放  |
| 2025-12-18 | v1.1 | 删除待补充及非原模型定义的模型，修正索引编号 | 李鸿坤 |
| 2025-12-17 | v1.0 | 创建文档，整合生产管理和生产异常数据模型 | 王晴  |
