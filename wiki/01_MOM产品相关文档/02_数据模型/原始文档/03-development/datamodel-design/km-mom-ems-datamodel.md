# 设备管理数据模型

## 文档说明

**基本信息**
- 文档版本：v1.6 | 更新日期：2026-02-25 | 维护团队：产品研发团队
- 目标受众：产品研发团队

**文档定位**

本文档定义KMMOM3.x设备管理模块(EMS)的数据模型设计，涵盖设备台账管理、维护保养、状态监控、点检计划、故障处理等设备全生命周期管理的核心实体及其属性规范。

**内容结构**

| 章节 | 核心问题 | 内容说明 |
|------|---------|----------|
| 一、术语、定义和缩略语 | EMS模块涉及哪些专业术语？ | 定义设备管理领域的业务术语、概念和缩略语 |
| 二、数据模型 | EMS模块包含哪些核心数据模型？ | 逐个定义设备台账、点检、维保、故障等业务实体 |

---

## 一、术语、定义和缩略语

| 术语 | 定义 | 缩略语 |
|------|------|--------|
| 设备管理系统 | 对设备进行全生命周期管理的信息系统，包括台账、维保、点检、故障等功能 | EMS |
| 设备台账 | 记录设备基本信息、技术参数、使用状态的主数据档案 | - |
| 点检 | 按照规定周期对设备进行定期检查，确认设备运行状态是否正常 | - |
| 维保 | 维护保养的简称，包括预防性维护、预测性维护、应急维护等 | - |
| 备件 | 用于设备维修和更换的零部件或材料 | - |
| 设备类型 | 按用途划分的设备分类（生产设备、仪器设备、特种设备、生产车辆） | - |
| 设备类别 | 按功能或工艺划分的设备分类体系（树形结构） | - |
| 工时消耗 | 完成维护或故障处理任务所花费的人工时间 | - |
| 提前期 | 在计划执行日期之前提前生成任务的天数 | - |

---

## 二、数据模型

### 设备台账（EquipLedger）
**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`AttachmentManaged` | **表名:** `MOM_EQUIP_LEDGER`

**说明**：该模型不继承生命周期，业务状态字段 `bizStatus` 表示设备资源运行状态，不属于通用业务流程五态

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 无 | 引用枚举:EquipLedgerBizStatus |
| 设备类别 | `category` | `CCATEGORY` | 分类 | - | 必填 | 引用分类:EquipCategory |
| 型号规格 | `modelSpec` | `CMODEL_SPEC` | 字符串 | 256 | 无 | 设备的具体型号和规格 |
| 安装位置 | `installLocation` | `CINSTALL_LOCATION` | 字符串 | 512 | 无 | 设备在车间内的具体位置描述 |
| 责任人 | `responsiblePerson` | `CRESPONSIBLE_PERSON` | 用户 | - | 无 | 设备的责任管理人员 |
| 供应商 | `supplier` | `CSUPPLIER` | 字符串 | 256 | 无 | 设备供应商名称 |
| 出厂编号 | `factoryNumber` | `CFACTORY_NUMBER` | 字符串 | 256 | 无 | 设备的出厂序列号 |
| 投用日期 | `putIntoUseDate` | `CPUT_INTO_USE_DATE` | 日期 | - | 无 | 设备正式开始投入使用的日期 |
| 累计运行时长 | `totalRunningHours` | `CTOTAL_RUNNING_HOURS` | 浮点型 | - | 无 | 设备累计运行时间（小时） |

### 设备故障单（EquipFault）
**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`AttachmentManaged` | **表名:** `MOM_EQUIP_FAULT`

**说明**：该模型不继承生命周期，使用业务状态字段 `bizStatus` 表示故障处理流程

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 无 | 引用枚举:EquipFaultBizStatus |
| 关联设备 | `equipLedger` | `CEQUIP_LEDGER` | 引用对象 | - | 必填 | 引用EquipLedger |
| 故障描述 | `faultDescription` | `CFAULT_DESCRIPTION` | CLOB | - | 必填 | 对故障现象的详细描述 |
| 初步处理措施 | `initialMeasure` | `CINITIAL_MEASURE` | 字符串 | 4000 | 无 | 故障发生后采取的初步应对措施 |
| 上报人员 | `reporter` | `CREPORTER` | 用户 | - | 必填 | 故障上报人 |
| 上报时间 | `reportTime` | `CREPORT_TIME` | 日期时间 | - | 必填 | 故障被上报的准确时间 |
| 故障发生时间 | `faultOccurTime` | `CFAULT_OCCUR_TIME` | 日期时间 | - | 无 | 故障实际发生的时间 |
| 故障类型 | `faultType` | `CFAULT_TYPE` | 枚举 | - | 必填 | 引用枚举:FaultType |
| 严重程度 | `severity` | `CSEVERITY` | 枚举 | - | 必填 | 引用枚举:Severity |
| 预计停机时长 | `estimatedDowntime` | `CESTIMATED_DOWNTIME` | 浮点型 | - | 无 | 预计故障导致的设备停机总时长（小时） |
| 处理人 | `processor` | `CPROCESSOR` | 用户 | - | 无 | 故障处理人员 |
| 处理时间 | `processTime` | `CPROCESS_TIME` | 日期时间 | - | 无 | 执行处理动作的时间点 |
| 处理步骤描述 | `processStepDescription` | `CPROCESS_STEP_DESCRIPTION` | CLOB | - | 无 | 对具体处理动作、诊断发现的详细描述 |
| 工时消耗 | `workDuration` | `CWORK_DURATION` | 浮点型 | - | 无 | 本次处理步骤所花费的时间（小时） |

### 设备点检策略（EquipInspectStrategy）
**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** 无 | **表名:** `MOM_EQUIP_INSPECT_STRATEGY`

**编码规则**：ITPL-NNNN

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 适用设备类别 | `category` | `CCATEGORY` | 分类 | - | 必填 | 引用分类:EquipCategory |
| 周期单位 | `cycleUnit` | `CCYCLE_UNIT` | 单位 | - | 必填 | 引用单位:CycleUnit |
| 周期值 | `cycleValue` | `CCYCLE_VALUE` | 浮点型 | - | 必填 | 与周期单位配合定义执行频率 |
| 启用标记 | `enableFlag` | `CENABLE_FLAG` | 布尔 | - | 必填 | 是否启用该模板 |
| 提前期 | `leadTime` | `CLEAD_TIME` | 整型 | - | 必填 | 在计划执行日期之前提前生成任务的天数 |

### 设备点检项（EquipInspectItemLink）
**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_EQUIP_INSPECT_ITEM_LINK` | **源数据实体:** `EquipInspectStrategy`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 点检项 | `itemName` | `CITEM_NAME` | 字符串 | 256 | 必填 | 点检项的具体内容 |
| 点检标准 | `checkStandard` | `CCHECK_STANDARD` | 字符串 | 4000 | 无 | 描述如何进行检查以及合格的标准 |
| 结论类型 | `conclusionType` | `CCONCLUSION_TYPE` | 枚举 | - | 必填 | 引用枚举:InspectionConclusionType |

### 设备维保策略（EquipMaintStrategy）
**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** 无 | **表名:** `MOM_EQUIP_MAINT_STRATEGY`

**编码规则**：MSTR-NNNN

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 适用设备类别 | `category` | `CCATEGORY` | 分类 | - | 必填 | 引用分类:EquipCategory |
| 维护类型 | `maintenanceType` | `CMAINTENANCE_TYPE` | 枚举 | - | 必填 | 引用枚举:MaintenanceType |
| 预计时长 | `estimatedDuration` | `CESTIMATED_DURATION` | 浮点型 | - | 必填 | 完成该项目的预估时间（小时） |
| 周期单位 | `cycleUnit` | `CCYCLE_UNIT` | 单位 | - | 必填 | 引用单位:CycleUnit |
| 周期值 | `cycleValue` | `CCYCLE_VALUE` | 浮点型 | - | 必填 | 与周期单位配合定义执行频率 |
| 启用标记 | `enableFlag` | `CENABLE_FLAG` | 布尔 | - | 必填 | 是否启用该模板 |
| 提前期 | `leadTime` | `CLEAD_TIME` | 整型 | - | 必填 | 在计划执行日期之前提前生成任务的天数 |

### 设备维保项（EquipMaintItemLink）
**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_EQUIP_MAINT_ITEM_LINK` | **源数据实体:** `EquipMaintStrategy`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 维保项 | `itemName` | `CITEM_NAME` | 字符串 | 256 | 必填 | 维护项目的具体内容 |
| 维保标准 | `qualityStandard` | `CQUALITY_STANDARD` | 字符串 | 4000 | 无 | 完成该项目后需要达到的质量标准 |

### 设备维保备件明细（EquipMaintPartReqLink）
**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_EQUIP_MAINT_PART_REQ_LINK` | **源数据实体:** `EquipMaintStrategy`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 备件 | `sparePart` | `CSPARE_PART` | 引用对象 | - | 必填 | 引用Material（备件类型） |
| 需求数量 | `requiredQuantity` | `CREQUIRED_QUANTITY` | 浮点型 | - | 必填 | 标准的备件需求数量 |
| 必换件标识 | `mustReplaceFlag` | `CMUST_REPLACE_FLAG` | 布尔 | - | 必填 | 是否必须更换的备件 |

### 设备维保策略关系（EquipMaintStrategyLink）
**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_EQUIP_MAINT_STRATEGY_LINK` | **源数据实体:** `EquipLedger`（设备）

**说明**：该模型属于ISA95计划层，定义设备与维保策略的关联关系（"设备A按照策略B定期维保"），系统根据此关系自动生成维保计划

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 维保策略 | `strategy` | `CSTRATEGY` | 引用对象 | - | 无 | 引用EquipMaintStrategy |
| 最后计划执行时间 | `lastPlanExecuteTime` | `CLAST_PLAN_EXECUTE_TIME` | 日期时间 | - | 无 | 当前设备该模板的最新一次计划的执行时间，用于计算下一次计划生成时间 |

### 设备点检策略关系（EquipInspectStrategyLink）
**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_EQUIP_INSPECT_STRATEGY_LINK` | **源数据实体:** `EquipLedger`（设备）

**说明**：该模型属于ISA95计划层，定义设备与点检策略的关联关系（"设备A按照策略B定期点检"），系统根据此关系自动生成点检计划

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 点检策略 | `strategy` | `CSTRATEGY` | 引用对象 | - | 无 | 引用EquipInspectStrategy |
| 最后计划执行时间 | `lastPlanExecuteTime` | `CLAST_PLAN_EXECUTE_TIME` | 日期时间 | - | 无 | 当前设备该模板的最新一次计划的执行时间，用于计算下一次计划生成时间 |

### 设备维护计划（EquipMaintenancePlan）
**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`LifecycleManaged` | **表名:** `MOM_EQUIP_MAINTENANCE_PLAN`

**生命周期模板**：COMMON_LIFECYCLE

**说明**：该模型融合了ISA95的计划层和任务层，涵盖从计划生成到执行完成的完整生命周期：
- **计划阶段**（`bizStatus`=初始）：系统根据模板关系自动生成维保计划
- **任务阶段**（`bizStatus`=已开始）：分配执行人后，成为具体的维保任务
- **记录阶段**（`bizStatus`=已完成）：填写结果后，成为维保记录

**编码规则**：MPLAN-YYYYMMDD-NNNN

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 无 | 引用枚举:SimpleActivityBizStatus |
| 关联设备 | `equipLedger` | `CEQUIP_LEDGER` | 引用对象 | - | 必填 | 引用EquipLedger |
| 维保策略 | `strategy` | `CSTRATEGY` | 引用对象 | - | 必填 | 引用EquipMaintStrategy |
| 计划开始时间 | `planStartTime` | `CPLAN_START_TIME` | 日期时间 | - | 必填 | 计划执行的开始时间窗口 |
| 计划完成时间 | `planCompleteTime` | `CPLAN_COMPLETE_TIME` | 日期时间 | - | 必填 | 计划执行的完成时间窗口 |
| 执行人 | `executor` | `CEXECUTOR` | 用户 | - | 无 | 维保执行人员 |
| 实际开始时间 | `actualStartTime` | `CACTUAL_START_TIME` | 日期时间 | - | 无 | 实际开始维护的时间 |
| 实际完成时间 | `actualCompleteTime` | `CACTUAL_COMPLETE_TIME` | 日期时间 | - | 无 | 实际完成维护的时间 |
| 结果描述 | `resultDescription` | `CRESULT_DESCRIPTION` | 字符串 | 4000 | 无 | 对维护过程和结果的详细描述 |

### 设备维护项记录（EquipMaintPlanItemLink）
**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_EQUIP_MAINT_PLAN_ITEM_LINK` | **源数据实体:** `EquipMaintenancePlan`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 维保项 | `itemName` | `CITEM_NAME` | 字符串 | 256 | 必填 | 维护项目的具体内容 |
| 维保标准 | `qualityStandard` | `CQUALITY_STANDARD` | 字符串 | 4000 | 无 | 完成该项目后需要达到的质量标准 |
| 维护结果 | `maintenanceResult` | `CMAINTENANCE_RESULT` | 枚举 | - | 无 | 引用枚举:EquipCheckResult |
| 备注 | `remark` | `CREMARK` | 字符串 | 4000 | 无 | 额外说明信息 |

### 设备点检计划（EquipInspectionPlan）
**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`LifecycleManaged` | **表名:** `MOM_EQUIP_INSPECTION_PLAN`

**生命周期模板**：COMMON_LIFECYCLE

**说明**：该模型融合了ISA95的计划层和任务层，涵盖从计划生成到执行完成的完整生命周期：
- **计划阶段**（`bizStatus`=初始）：系统根据模板关系自动生成点检计划
- **任务阶段**（`bizStatus`=已开始）：分配执行人后，成为具体的点检任务
- **记录阶段**（`bizStatus`=已完成）：填写结果后，成为点检记录

**编码规则**：IPLAN-YYYYMMDD-NNNN

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 无 | 引用枚举:SimpleActivityBizStatus |
| 关联设备 | `equipLedger` | `CEQUIP_LEDGER` | 引用对象 | - | 必填 | 引用EquipLedger |
| 点检策略 | `strategy` | `CSTRATEGY` | 引用对象 | - | 必填 | 引用EquipInspectStrategy |
| 计划执行时间 | `planExecuteTime` | `CPLAN_EXECUTE_TIME` | 日期时间 | - | 必填 | 计划执行的日期 |
| 执行人 | `executor` | `CEXECUTOR` | 用户 | - | 无 | 点检执行人员 |
| 实际执行时间 | `actualExecuteTime` | `CACTUAL_EXECUTE_TIME` | 日期时间 | - | 无 | 实际完成点检的时间 |
| 结果描述 | `resultDescription` | `CRESULT_DESCRIPTION` | 字符串 | 4000 | 无 | 对点检过程和异常结果的补充描述 |

### 设备点检项记录（EquipInspectPlanItemLink）
**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_EQUIP_INSPECT_PLAN_ITEM_LINK` | **源数据实体:** `EquipInspectionPlan`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|

| 点检项 | `itemName` | `CITEM_NAME` | 字符串 | 256 | 必填 | 点检项目的具体内容 |
| 点检标准 | `checkStandard` | `CCHECK_STANDARD` | 字符串 | 4000 | 无 | 描述如何进行检查以及合格的标准 |
| 结论类型 | `conclusionType` | `CCONCLUSION_TYPE` | 枚举 | - | 必填 | 引用枚举:InspectionConclusionType |
| 记录数值 | `recordValue` | `CRECORD_VALUE` | 字符串 | 256 | 无 | 对于需要记录读数的点检项，记录其具体数值 |
| 点检结果 | `inspectionResult` | `CINSPECTION_RESULT` | 枚举 | - | 无 | 引用枚举:EquipCheckResult |
| 备注 | `remark` | `CREMARK` | 字符串 | 4000 | 无 | 额外说明信息 |

### 备件更换记录（SparePartReplaceRecord）
**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_SPARE_PART_REPLACEMENT_RECORD`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 关联业务类型 | `relatedBizType` | `CRELATED_BIZ_TYPE` | 枚举 | - | 必填 | 引用枚举:PartRelaceType |
| 关联对象ID | `relatedObjectId` | `CRELATED_OBJECT_ID` | 字符串 | 256 | 无 | 关联业务对象的ID |
| 关联对象实体类型 | `relatedObjectEntityType` | `CRELATED_OBJECT_ENTITY_TYPE` | 字符串 | 256 | 无 | 关联业务对象的实体类型 |
| 关联对象实体编码 | `relatedObjectEntityCode` | `CRELATED_OBJECT_ENTITY_CODE` | 字符串 | 256 | 无 | 关联业务对象的编码 |
| 备件 | `sparePart` | `CSPARE_PART` | 引用对象 | - | 必填 | 引用Material（物料，物料类别=备件） |
| 更换数量 | `replacementQuantity` | `CREPLACEMENT_QUANTITY` | 浮点型 | - | 必填 | 更换或消耗的数量 |
| 更换时间 | `replacementTime` | `CREPLACEMENT_TIME` | 日期时间 | - | 无 | 备件被更换或消耗的准确时间 |
| 出库记录 | `outStoreRecord` | `COUT_STORE_RECORD` | 引用对象 | - | 无 | 引用出库记录 |
| 计量单位 | `unit` | `CUNIT` | 单位 | - | 无 | 引用单位:MeasureUnit |

### 设备调拨单（EquipTransferOrder）
**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`LifecycleManaged` | **表名:** `MOM_EQUIP_TRANSFER_ORDER`

**生命周期模板**：COMMON_LIFECYCLE

**说明**：该模型继承通用生命周期模板，无业务状态

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 关联设备 | `equipLedger` | `CEQUIP_LEDGER` | 引用对象 | - | 必填 | 引用EquipLedger |
| 申请人 | `applicant` | `CAPPLICANT` | 用户 | - | 必填 | 调拨申请人 |
| 申请时间 | `applyTime` | `CAPPLY_TIME` | 日期时间 | - | 必填 | 调拨申请发起的准确时间 |
| 申请原因 | `applyReason` | `CAPPLY_REASON` | 字符串 | 4000 | 无 | 申请调拨的具体原因说明 |
| 调入组织 | `transferInDept` | `CTRANSFER_IN_DEPT` | 引用对象 | - | 必填 | 引用BizOrg（设备计划调入的业务组织） |
| 完成时间 | `completeTime` | `CCOMPLETE_TIME` | 日期时间 | - | 无 | 调拨流程完成的时间 |

### 设备报废单（EquipScrapOrder）
**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`LifecycleManaged` | **表名:** `MOM_EQUIP_SCRAP_ORDER`

**生命周期模板**：COMMON_LIFECYCLE

**说明**：该模型继承通用生命周期模板，无业务状态

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 关联设备 | `equipLedger` | `CEQUIP_LEDGER` | 引用对象 | - | 必填 | 引用EquipLedger |
| 申请人 | `applicant` | `CAPPLICANT` | 用户 | - | 必填 | 报废申请人 |
| 申请时间 | `applyTime` | `CAPPLY_TIME` | 日期时间 | - | 必填 | 报废申请发起的准确时间 |
| 报废原因 | `scrapReason` | `CSCRAP_REASON` | 字符串 | 4000 | 无 | 申请报废的具体原因说明 |
| 评估意见- | `technicalAssessment` | `CTECHNICAL_ASSESSMENT` | 字符串 | 2000 | 无 | 由主管部门出具的评估意见 |
| 完成时间 | `completeTime` | `CCOMPLETE_TIME` | 日期时间 | - | 无 | 报废流程完成的时间 |


## 变更记录

| 日期 | 版本 | 变更内容 | 变更人 |
|-----|------|---------|-----|
| 2026-02-24 | v1.6 | 表名重构优化：9个实体重命名（InspectionTemplate→EquipInspectStrategy、MaintenanceTemplate→EquipMaintStrategy等），统一字段命名（template→strategy、equip→equipLedger），简化中文字段名，删除冗余字段（equipType、skillRequirement、transferOutDept、assetAssessment），删除故障知识库实体 | 危放 |
| 2026-01-22 | v1.5 | 修复关系实体元信息规范：为7个继承GenericLink的关系实体补充源数据实体字段（InspectionTemplateItemLink、MaintenanceTemplateItemLink、MaintenanceTemplatePartReqLink、EquipMaintTemplateLink、EquipInspectTemplateLink、MaintenancePlanDetailLink、InspectionPlanDetailLink） | 危放 |
| 2026-01-22 | v1.4 | 优化时长字段命名（downtimeMinutes→estimatedDowntime、workHours→workDuration），为计划层和任务层模型添加ISA95说明，修复组织引用（Org→BizOrg），将template字段设为必填、添加技术术语反引号 | 危放 |
| 2026-01-08 | v1.3 | 更新引用枚举、单位、分类| 危放 |
| 2025-12-29 | v1.2 | 改造业务属性为引用格式 | 王晴 |
| 2025-12-29 | v1.1 | 优化生命周期继承和业务状态：EquipLedger/EquipFault不继承生命周期，添加bizStatus属性字段；EquipMaintenancePlan/EquipInspectionPlan/EquipScrapOrder/EquipTransferOrder使用COMMON_LIFECYCLE，EquipMaintenancePlan/EquipInspectionPlan添加bizStatus属性字段 | 危放  |
| 2025-12-17 | v1.0 | 创建文档，规范化设备管理模块数据模型 | 王晴  |
