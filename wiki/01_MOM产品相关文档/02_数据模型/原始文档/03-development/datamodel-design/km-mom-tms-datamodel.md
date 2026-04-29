# 工具工装管理数据模型

## 文档说明

**基本信息**
- 文档版本：v1.6 | 更新日期：2026-02-25 | 维护团队：产品研发团队
- 目标受众：产品研发团队

**文档定位**

本文档定义KMMOM3.x工具工装管理模块的数据模型设计，涵盖工装台账管理、保养策略与任务、检定策略与任务、借用归还、封存启封、调拨共享、报废处置、维修管理等全生命周期业务场景，为工装工具的申请、使用、归还、维护提供完整的数据支撑。

**内容结构**

| 章节 | 核心问题 | 内容说明 |
|------|---------|----------|
| 一、术语、定义和缩略语 | 工具工装管理涉及哪些专业术语？ | 定义工装类别、单件标记、保养检定等关键业务概念 |
| 二、数据模型 | 工具工装管理需要哪些数据模型？ | 定义21个业务模型，涵盖台账、策略、任务、申请单等核心实体 |

---

## 一、术语、定义和缩略语

| 术语 | 定义 | 缩略语 |
|------|------|--------|
| 工装台账 | 工装工具的库存管理记录,记录工装的位置、数量、状态及使用情况 | - |
| 单件标记 | 工装的管理粒度,包括单件管理(每个工装有唯一序列号)和批次管理(按批次统一管理) | - |
| 保养策略 | 定义工装保养的触发机制、周期、项目及备件需求的规则模板 | - |
| 检定策略 | 定义工装强制检定的周期、项目及责任单位的规则模板 | - |
| 保养任务 | 根据保养策略或临时需求生成的具体保养执行单,记录保养过程和结果 | - |
| 检定任务 | 根据检定策略或临时需求生成的具体检定执行单,记录检定过程和结果 | - |
| 使用寿命 | 工装已使用的次数或天数,用于判断是否达到保养/检定阈值 | - |
| 共享状态 | 工装是否可以跨组织共享使用的标识 | - |

---

## 二、数据模型

### 2.1 工装保养策略（ToolingMaintStrategy）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged` | **表名:** `MOM_TOOLING_MAINT_STRATEGY`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明                                                        |
|-------------|-------------|-----------|---------|------|------|-----------------------------------------------------------|
| 工装类别 | `type` | `CTYPE` | 分类 | - | 必填 | 引用分类:toolingType                                          |
| 策略类型 | `strategyType` | `CSTRATEGY_TYPE` | 枚举 | - | 必填 | 引用枚举:strategyType                                         |
| 周期单位 | `cycleUnit` | `CCYCLE_UNIT` | 单位 | - | 必填 | 引用单位:cycleUnit                                            |
| 周期值 | `cycleValue` | `CCYCLE_VALUE` | 整型 | - | 必填 | 定义保养的时间间隔值                                                |
| 预计时长 | `duration` | `CDURATION` | 整型 | - | 无 | 预计完成所有项目所需的时间（小时）                                         |
| 使用次数阈值 | `usageThreshold` | `CUSAGE_THRESHOLD` | 整型 | - | 无 | 定义触发保养的使用次数阈值                                             |
| 预警提前期(天/次) | `advancePeriod` | `CADVANCE_PERIOD` | 整型 | - | 无 | 按时间周期保养:距离下次保养提前多少天生成任务,必须≤检定周期；按使用次数保养:距离使用次数阈值提前多少次生成任务 |
| 默认保养单位 | `defaultMaintOrg` | `CDEFAULT_MAINT_ORG` | 引用对象 | - | 必填 | 引用BizOrg                                                  |
| 启用标记 | `enableFlag` | `CENABLE_FLAG` | 布尔 | - | 必填 | 默认值:是 |

### 2.2 工装保养项（ToolingMaintItemLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** - | **表名:** `MOM_TOOLING_MAINT_ITEM_LINK` | **源数据实体:** ToolingMaintStrategy

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 保养项 | `name` | `CNAME` | 字符串 | 512 | 必填 | 保养项目的名称,如"清洁"、"润滑"、"更换密封圈" |
| 保养标准 | `standard` | `CSTANDARD` | 字符串 | 512 | 无 | 执行该项目所需的标准要求 |
| 预计时长 | `estimatedTime` | `CESTIMATED_TIME` | 整型 | - | 无 | 预计完成该项目所需的时间（单位:分钟） |

### 2.3 工装保养备件明细（ToolingMaintSparePartLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** - | **表名:** `MOM_TOOLING_MAINT_SPARE_PART_LINK` | **源数据实体:** ToolingMaintStrategy

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 备件 | `sparePart` | `CSPARE_PART` | 引用对象 | - | 必填 | 引用Material,关联工装类别为"工装备件"类型的物料 |
| 需求数量 | `requiredQty` | `CREQUIRED_QTY` | 浮点型 | - | 必填 | 该备件在该保养项目中的需求数量 |
| 计量单位 | `unit` | `CUNIT` | 单位 | - | 必填 | 引用单位:measureUnit |

### 2.4 工装检定策略（ToolingCalibrateStrategy）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged` | **表名:** `MOM_TOOLING_CALIBRATE_STRATEGY`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 工装类别 | `type` | `CTYPE` | 分类 | - | 必填 | 引用分类:toolingType |
| 检定周期单位 | `cycleUnit` | `CCYCLE_UNIT` | 单位 | - | 必填 | 引用单位:cycleUnit |
| 检定周期值 | `cycleValue` | `CCYCLE_VALUE` | 整型 | - | 必填 | 定义强制检定的时间间隔值 |
| 提前期 | `advanceDays` | `CADVANCE_DAYS` | 整型 | - | 无 | 距离下次检定提前多少天生成任务,必须≤检定周期 |
| 预计时长 | `estimatedDuration` | `CESTIMATED_DURATION` | 整型 | - | 无 | 预计完成检定所需的时间（单位:小时） |
| 默认检定单位 | `defaultCalibrateOrg` | `CDEFAULT_CALIBRATE_ORG` | 引用对象 | - | 必填 | 引用BizOrg |
| 启用标记 | `enableFlag` | `CENABLE_FLAG` | 布尔 | - | 必填 | 默认值:是 |

### 2.5 工装检定项（ToolingCalibrateItemLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** - | **表名:** `MOM_TOOLING_CALIBRATE_ITEM_LINK` | **源数据实体:** ToolingCalibrateStrategy

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 检定项 | `name` | `CNAME` | 字符串 | 512 | 必填 | 检定项目的名称,如"外观检查"、"精度测试" |
| 检定标准 | `standard` | `CSTANDARD` | 字符串 | 512 | 必填 | 该检定项目的具体检查标准或要求 |

### 2.6 工装保养任务（ToolingMaintTask）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`LifecycleManaged` | **表名:** `MOM_TOOLING_MAINT_TASK`

**生命周期模板**：COMMON_LIFECYCLE

**说明**：该模型继承通用生命周期模板

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 无 | 引用枚举:ToolMaintTaskBizStatus |
| 工装工具 | `tooling` | `CTOOLING` | 引用对象 | - | 无 | 引用Material,明确库存记录对应的工装主数据 |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | 冗余工装物理批次的批次号 |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | 冗余工装物理实例的序列号 |
| 工装台账 | `ledger` | `CLEDGER` | 引用对象 | - | 必填 | 引用ToolingLedger,本次保养的目标工装（保养中台账） |
| 保养数量 | `quantity` | `CQUANTITY` | 浮点型 | - | 必填 | 本次保养的数量 |
| 计量单位 | `unit` | `CUNIT` | 单位 | - | 无 | 引用单位:measureUnit |
| 保养策略 | `strategy` | `CSTRATEGY` | 引用对象 | - | 必填 | 引用ToolingMaintStrategy,标识该任务是否由保养策略生成,方便追溯 |
| 保养类型 | `type` | `CTYPE` | 枚举 | - | 无 | 引用枚举:toolingMaintenanceType |
| 当前已用寿命(次) | `currentLifeTimes` | `CCURRENT_LIFE_TIMES` | 整型 | - | 无 | 实时记录已用寿命/次数,用于寿命预警和计算 |
| 预计时长 | `estimatedDuration` | `CESTIMATED_DURATION` | 整型 | - | 无 | 预计完成保养所需的时间（单位:小时） |
| 计划开始时间 | `plannedStartTime` | `CPLANNED_START_TIME` | 日期时间 | - | 无 | 计划的保养开始时间 |
| 计划完成时间 | `plannedEndTime` | `CPLANNED_END_TIME` | 日期时间 | - | 无 | 计划的保养完成时间 |
| 实际开始时间 | `actualStartTime` | `CACTUAL_START_TIME` | 日期时间 | - | 无 | 实际保养开始时间 |
| 实际完成时间 | `actualEndTime` | `CACTUAL_END_TIME` | 日期时间 | - | 无 | 实际保养完成时间 |
| 保养单位 | `maintenanceOrg` | `CMAINTENANCE_ORG` | 引用对象 | - | 必填 | 引用BizOrg |
| 保养负责人 | `maintenanceTaskMaster` | `CMAINTENANCE_TASK_MASTER` | 引用对象 | - | 无 | 引用User |
| 执行人 | `executor` | `CEXECUTOR` | 引用对象 | - | 无 | 引用User |
| 来源工装台账ID | `sourceLedgerId` | `CSOURCE_LEDGER_ID` | 长整型 | - | 无 | 记录任务来源台账的ID（不展示，可用状态的台账，保养完成时使用） |

### 2.7 工装保养任务项记录（ToolingMaintTaskItemLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** - | **表名:** `MOM_TOOLING_MAINT_TASK_ITEM_LINK` | **源数据实体:** ToolingMaintTask

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 保养项 | `name` | `CNAME` | 字符串 | 512 | 必填 | 保养项目的名称,如"清洁"、"润滑"、"更换密封圈" |
| 预计时长 | `estimatedTime` | `CESTIMATED_TIME` | 整型 | - | 无 | 预计完成该项目所需的时间（单位:分钟） |
| 保养标准 | `standard` | `CSTANDARD` | 字符串 | 512 | 必填 | 完成该保养项目后的验收质量标准 |
| 保养结果 | `conclusion` | `CCONCLUSION` | 枚举 | - | 必填 | 引用枚举:ToolingMaintenanceResult |
| 操作内容描述 | `operationDescription` | `COPERATION_DESCRIPTION` | CLOB | - | 无 | 详细描述本次保养的操作内容 |

### 2.8 工装检定任务（ToolingCalibrateTask）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`LifecycleManaged` | **表名:** `MOM_TOOLING_CALIBRATE_TASK`

**生命周期模板**：COMMON_LIFECYCLE

**说明**：该模型继承通用生命周期模板

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 无 | 引用枚举:ToolCalibrateTaskBizStatus |
| 工装工具 | `tooling` | `CTOOLING` | 引用对象 | - | 必填 | 引用Material,明确库存记录对应的工装主数据 |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | 冗余工装物理批次的批次号 |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | 冗余工装物理实例的序列号 |
| 工装台账 | `ledger` | `CLEDGER` | 引用对象 | - | 必填 | 引用ToolingLedger,本次检定的目标工装 |
| 检定数量 | `quantity` | `CQUANTITY` | 浮点型 | - | 必填 | 本次检定的工装数量 |
| 计量单位 | `unit` | `CUNIT` | 单位 | - | 无 | 引用单位:measureUnit |
| 检定策略 | `strategy` | `CSTRATEGY` | 引用对象 | - | 必填 | 引用ToolingCalibrateStrategy,标识该任务是否由检定策略生成,方便追溯 |
| 检定结论 | `calibrateResult` | `CCALIBRATE_RESULT` | 枚举 | - | 无 | 引用枚举:ToolingCalibrateResult |
| 检定单位 | `calibrationOrg` | `CCALIBRATION_ORG` | 引用对象 | - | 必填 | 引用BizOrg |
| 检定负责人 | `calibrationTaskMaster` | `CCALIBRATION_TASK_MASTER` | 引用对象 | - | 无 | 引用User |
| 执行人 | `executor` | `CEXECUTOR` | 引用对象 | - | 无 | 引用User |
| 来源工装台账ID | `sourceLedgerId` | `CSOURCE_LEDGER_ID` | 长整型 | - | 无 | 记录任务来源台账的ID |
| 预计时长 | `estimatedDuration` | `CESTIMATED_DURATION` | 整型 | - | 无 | 预计完成检定所需的时间（单位:小时） |
| 计划开始时间 | `plannedStartTime` | `CPLANNED_START_TIME` | 日期时间 | - | 无 | 计划的检定开始时间 |
| 计划完成时间 | `plannedEndTime` | `CPLANNED_END_TIME` | 日期时间 | - | 无 | 计划的检定完成时间 |
| 实际开始时间 | `actualStartTime` | `CACTUAL_START_TIME` | 日期时间 | - | 无 | 实际检定开始时间 |
| 实际完成时间 | `actualEndTime` | `CACTUAL_END_TIME` | 日期时间 | - | 无 | 实际检定完成时间 |

### 2.9 工装检定任务项记录（ToolingCalibrateTaskItemLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** - | **表名:** `MOM_TOOLING_CALIBRATE_TASK_ITEM_LINK` | **源数据实体:** ToolingCalibrateTask

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 检定项 | `name` | `CNAME` | 字符串 | 512 | 必填 | 检定项目的名称,如"外观检查"、"精度测试" |
| 检定标准 | `standard` | `CSTANDARD` | 字符串 | 512 | 必填 | 该检定项目的具体检查标准或要求 |
| 检定结果 | `conclusion` | `CCONCLUSION` | 枚举 | - | 无 | 引用枚举:ToolingCalibrateItemResult |
| 操作内容描述 | `operationDescription` | `COPERATION_DESCRIPTION` | CLOB | - | 无 | 详细描述本次检定的操作内容 |

### 2.10 工装台账（ToolingLedger）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`SecurityManaged` | **表名:** `MOM_TOOLING_LEDGER`


| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明                                                                             |
|-------------|-------------|-----------|---------|------|------|--------------------------------------------------------------------------------|
| 工装工具 | `tooling` | `CTOOLING` | 引用对象 | - | 必填 | 引用Material                                                                     |
| 工装工具编码 | `toolingCode` | `CTOOLING_CODE` | 字符串 | 256 | 无 | 冗余属性,方便日志记录                                                                    |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | 工装物理批次的批次号                                                                     |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | 工装物理实例的序列号                                                                     |
| 单件标记 | `singleFlag` | `CSINGLE_FLAG` | 布尔 | - | 必填 | 默认false |
| 库房 | `warehouse` | `CWAREHOUSE` | 引用对象 | - | 无 | 引用Warehouse,台账对应的库房                                                            |
| 库位 | `warehouseLocation` | `CWAREHOUSE_LOCATION` | 引用对象 | - | 无 | 引用WarehouseLocation,台账对应的库位                                                    |
| 计量单位 | `unit` | `CUNIT` | 单位 | - | 无 | 引用单位:measureUnit                                                                           |
| 共享状态 | `shareState` | `CSHARE_STATE` | 枚举 | - | 无 | 引用枚举:shareState                                                                |
| 库存数量 | `inventoryQty` | `CINVENTORY_QTY` | 浮点型 | - | 无 | 当前库位中该型号工装的实际数量                                                                |
| 入库日期 | `inboundDate` | `CINBOUND_DATE` | 日期时间 | - | 无 | 最近一次入库操作的日期                                                                    |
| 当前使用寿命（次） | `currentUsedLifeTimes` | `CCURRENT_USED_LIFE_TIMES` | 整型 | - | 无 | 工装当前已使用的次数                                                                     |
| 当前使用寿命（天） | `currentUsedLifeDays` | `CCURRENT_USED_LIFE_DAYS` | 整型 | - | 无 | 工装当前已使用的天数                                                                     |
| 上次检定日期 | `lastCalibrationDate` | `CLAST_CALIBRATION_DATE` | 日期时间 | - | 无 | 工装上次检定的日期                                                                      |
| 下次检定日期 | `nextCalibrationDate` | `CNEXT_CALIBRATION_DATE` | 日期时间 | - | 无 | 工装下次检定的日期                                                                      |
| 上次保养日期 | `lastMaintenanceDate` | `CLAST_MAINTENANCE_DATE` | 日期时间 | - | 无 | 工装上次保养的日期                                                                      |
| 下次保养日期 | `nextMaintenanceDate` | `CNEXT_MAINTENANCE_DATE` | 日期时间 | - | 无 | 工装下次保养的日期                                                                      |
| 合并业务主键 | `mergeBizKey` | `CMERGE_BIZ_KEY` | 字符串 | 256 | 无 | 库存唯一约束主键,格式:{组织}_{工装工具ID}_{库位ID}_{批次号}_{序列号}_{状态}_{库房}_{库位},不存在用#代替,用于进行台账拆分合并 |
| 实物业务主键 | `physicalBizKey` | `CPHYSICAL_BIZ_KEY` | 字符串 | 256 | 无 | 实物唯一约束主键,格式:{组织}_{工装工具ID}_{批次号}_{序列号},不存在用#代替                                  |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 无 | 引用枚举:ToolingLedgerBizStatus                                                    |

### 2.11 工装保养策略关系（ToolingMaintStrategyLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** `FactoryManaged` | **表名:** `MOM_TOOLING_MAINT_STRATEGY_LINK` | **源数据实体:** Material

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 保养策略 | `strategy` | `CSTRATEGY` | 引用对象 | - | 必填 | 引用ToolingMaintStrategy |
| 最后计划执行时间 | `lastPlanExecuteTime` | `CLAST_PLAN_EXECUTE_TIME` | 日期时间 | - | 无 | 当前工装该策略的最新一次计划执行时间,用于自动生成保养任务计算。下一次计划生成时间=该时间+周期-提前期 |

### 2.12 工装检定策略关系（ToolingCalibrateStrategyLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** `FactoryManaged` | **表名:** `MOM_TOOLING_CALIBRATE_STRATEGY_LINK` | **源数据实体:** Material

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 检定策略 | `strategy` | `CSTRATEGY` | 引用对象 | - | 无 | 引用ToolingCalibrateStrategy |
| 最后计划执行时间 | `lastPlanExecuteTime` | `CLAST_PLAN_EXECUTE_TIME` | 日期时间 | - | 无 | 当前工装该策略的最新一次计划执行时间,用于自动生成检定任务计算。下一次计划生成时间=该时间+周期-提前期 |

### 2.13 工装借用单（ToolingBorrowOrder）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged` | **表名:** `MOM_TOOLING_BORROW_ORDER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明                        |
|-------------|-------------|-----------|---------|------|------|---------------------------|
| 预计归还日期 | `estimatedReturnDate` | `CESTIMATED_RETURN_DATE` | 日期时间 | - | 必填 | 用于超期预警                    |
| 借用人 | `borrower` | `CBORROWER` | 引用对象 | - | 必填 | 引用User,借用工装的责任人           |
| 借用部门 | `borrowDepartment` | `CBORROW_DEPARTMENT` | 引用对象 | - | 必填 | 引用BizOrg,借用工装的责任人部门       |
| 借用时间 | `borrowTime` | `CBORROW_TIME` | 日期时间 | - | 必填 | 借用工装的时间,系统自动生成            |
| 借用事由 | `borrowReason` | `CBORROW_REASON` | 字符串 | 512 | 无 | 说明本次临时借用的目的               |
| 工装工具 | `tooling` | `CTOOLING` | 引用对象 | - | 必填 | 引用Material,当前关联的台账（借用中）   |
| 工装台账 | `ledger` | `CLEDGER` | 引用对象 | - | 必填 | 引用ToolingLedger           |
| 借用数量 | `borrowQty` | `CBORROW_QTY` | 浮点型 | - | 必填 | 借用数量                      |
| 已归还数量 | `returnedQty` | `CRETURNED_QTY` | 浮点型 | - | 无 | 已归还数量                     |
| 计量单位 | `unit` | `CUNIT` | 单位 | - | 无 | 引用单位:measureUnit                      |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | 冗余工装物理批次的批次号              |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | 冗余工装物理实例的序列号              |
| 单件标记 | `singleFlag` | `CSINGLE_FLAG` | 布尔 | - | 必填 | 默认false |
| 来源工装台账ID | `sourceLedgerId` | `CSOURCE_LEDGER_ID` | 长整型 | - | 无 | 记录来源台账的ID                 |
| 工装工具实物业务主键 | `physicalBizKey` | `CPHYSICAL_BIZ_KEY` | 字符串 | - | 无 | 工装工具实物业务主键                |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 无 | 引用枚举:BorrowOrderBizStatus |

### 2.14 工装借用单归还明细（ToolingBorrowReturnDetailLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** - | **表名:** `MOM_TOOLING_BORROW_RETURN_DETAIL_LINK` | **源数据实体:** `ToolingBorrowOrder`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 归还人 | `returnPerson` | `CRETURN_PERSON` | 引用对象 | - | 必填 | 引用User |
| 归还数量 | `returnQty` | `CRETURN_QTY` | 浮点型 | - | 必填 | 本次归还数量 |
| 归还检查结论 | `inspectionResult` | `CINSPECTION_RESULT` | 枚举 | - | 必填 | 引用枚举:ToolingReturnCheckResult |
| 归还描述 | `returnDesc` | `CRETURN_DESC` | 字符串 | 512 | 无 | 归还情况描述 |
| 实际归还日期 | `actualReturnDate` | `CACTUAL_RETURN_DATE` | 日期时间 | - | 无 | 实际归还日期 |

### 2.15 工装台账操作记录（ToolingLedgerOperationRecord）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `SecurityManaged`、`FactoryManaged` | **表名:** `MOM_TOOLING_LEDGER_OPERATION_RECORD`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 工装工具 | `tooling` | `CTOOLING` | 引用对象 | - | 无 | 引用Material |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | 工装物理批次的批次号 |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | 工装物理实例的序列号 |
| 操作类型 | `type` | `CTYPE` | 枚举 | - | 无 | 引用枚举:ToolingLedgerOperationType |
| 数量 | `qty` | `CQTY` | 浮点型 | - | 无 | 操作数量 |
| 操作内容 | `content` | `CCONTENT` | 字符串 | 512 | 无 | 操作内容描述 |
| 原始状态 | `originState` | `CORIGIN_STATE` | 字符串 | 64 | 无 | 操作前状态 |
| 目标状态 | `targetState` | `CTARGET_STATE` | 字符串 | 64 | 无 | 操作后状态 |

### 2.16 工装调拨申请单（ToolingTransferApplyOrder）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`LifecycleManaged` | **表名:** `MOM_TOOLING_TRANSFER_APPLY_ORDER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 调入组织 | `inOrg` | `CIN_ORG` | 引用对象 | - | 必填 | 引用BizOrg,资产接收的组织 |
| 期望到货日期 | `expectedDate` | `CEXPECTED_DATE` | 日期 | - | 无 | 期望工装到达调入工厂的日期 |
| 申请人 | `applicant` | `CAPPLICANT` | 引用对象 | - | 必填 | 引用User,申请调拨的用户 |
| 申请时间 | `applyTime` | `CAPPLY_TIME` | 日期时间 | - | 必填 | 发起调拨申请的时间,系统自动获取 |
| 申请原因 | `applyReason` | `CAPPLY_REASON` | 字符串 | 2000 | 无 | 申请调拨的原因说明 |

### 2.17 工装调拨申请单明细（ToolingTransferApplyOrderLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** `FactoryManaged` | **表名:** `MOM_TOOLING_TRANSFER_APPLY_ORDER_LINK`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 申请单编码 | `applyCode` | `CAPPLY_CODE` | 字符串 | - | 必填 | 申请单编码 |
| 调入组织 | `inOrg` | `CIN_ORG` | 引用对象 | - | 必填 | 引用BizOrg,资产接收的组织 |
| 实际到货日期 | `actualDate` | `CACTUAL_DATE` | 日期 | - | 无 | 实际工装到达调入工厂的日期 |
| 申请原因 | `applyReason` | `CAPPLY_REASON` | 字符串 | 500 | 无 | 申请调拨的原因说明 |
| 工装工具 | `tooling` | `CTOOLING` | 引用对象 | - | 无 | 引用Material,明确库存记录对应的工装主数据 |
| 工装台账 | `ledger` | `CLEDGER` | 引用对象 | - | 无 | 引用ToolingLedger,关联到具体的工装台账 |
| 库房 | `warehouse` | `CWAREHOUSE` | 引用对象 | - | 必填 | 引用Warehouse |
| 库位 | `warehouseLocation` | `CWAREHOUSE_LOCATION` | 引用对象 | - | 无 | 
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | 工装物理批次的批次号 |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | 工装物理实例的序列号 |
| 数量 | `quantity` | `CQUANTITY` | 整型 | - | 无 | 本次调拨的工装数量 |
| 计量单位 | `unit` | `CUNIT` | 单位 | - | 无 | 引用单位:measureUnit |
| 来源工装台账ID | `sourceLedgerId` | `CSOURCE_LEDGER_ID` | 长整型 | - | 无 | 记录来源台账的ID |
| 工装工具实物业务主键 | `physicalBizKey` | `CPHYSICAL_BIZ_KEY` | 字符串 | - | 无 | 工装工具实物业务主键 |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填 | 引用枚举:ToolingTransferApplyOrderLinkBizStatus |


### 2.18 工装报废申请单（ToolingScrapApplyOrder）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`LifecycleManaged` | **表名:** `MOM_TOOLING_SCRAP_APPLY_ORDER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 报废原因 | `scrapReason` | `CSCRAP_REASON` | 字符串 | 2000 | 必填 | 详细说明申请报废的理由 |
| 申请人 | `applicant` | `CAPPLICANT` | 引用对象 | - | 必填 | 引用User,申请报废的用户 |
| 申请时间 | `applyTime` | `CAPPLY_TIME` | 日期时间 | - | 必填 | 发起报废申请的时间,系统自动获取 |

### 2.19 工装报废申请单明细（ToolingScrapApplyOrderLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** `FactoryManaged` | **表名:** `MOM_TOOLING_SCRAP_APPLY_ORDER_LINK`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 申请单编码 | `applyCode` | `CAPPLY_CODE` | 字符串 | - | 必填 | 申请单编码 |
| 报废原因 | `scrapReason` | `CSCRAP_REASON` | 字符串 | 2000 | 必填 | 详细说明申请报废的理由 |
| 执行人 | `executor` | `CEXECUTOR` | 引用对象 | - | 无 | 引用User,执行物理报废操作的用户 |
| 执行时间 | `executeTime` | `CEXECUTE_TIME` | 日期时间 | - | 无 | 执行物理报废操作的时间 |
| 工装工具 | `tooling` | `CTOOLING` | 引用对象 | - | 无 | 引用Material,明确库存记录对应的工装主数据 |
| 工装台账 | `ledger` | `CLEDGER` | 引用对象 | - | 无 | 引用ToolingLedger,关联到具体的工装台账 |
| 批次号 | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | 工装物理批次的批次号 |
| 序列号 | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | 工装物理实例的序列号 |
| 报废数量 | `quantity` | `CQUANTITY` | 整型 | - | 无 | 本次报废的工装数量 |
| 计量单位 | `unit` | `CUNIT` | 单位 | - | 无 | 引用单位:measureUnit |
| 工装工具实物业务主键 | `physicalBizKey` | `CPHYSICAL_BIZ_KEY` | 字符串 | - | 无 | 工装工具实物业务主键 |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举 | - | 必填 | 引用枚举:ToolingScrapApplyOrderLinkBizStatus |
| 来源工装台账ID | `sourceLedgerId` | `CSOURCE_LEDGER_ID` | 长整型 | - | 无 | 记录来源台账的ID |

---

## 变更记录

| 日期 | 版本 | 变更内容 | 变更人 |
|-----|------|---------|-----|
| 2026-02-25 | v1.6 | 优化数据模型属性定义：统一术语表达（管理方式→单件标记、项目名称→保养项等），补充字段说明，完善引用对象标注；删除冗余字段（ToolingMaintItemLink/ToolingMaintPlanItemLink的技能要求、ToolingCalibrateTask的结果描述等），删除4个模型的bizOrg/factory冗余字段 | 危放 |
| 2026-01-26 | v1.5 | 修复引用枚举类型编码，确保与数据库定义一致| 危放  |
| 2026-01-23 | v1.4 | 修复数据类型名称不规范（文本大对象改为CLOB，3处）、枚举类型长度标注不规范、字符串长度超出推荐范围（name字段从256改为512，3处）、resultDescription长度调整（4000改为2000，2处）、枚举引用格式不统一（添加引用枚举:前缀） | 李飞 |
| 2026-01-09 | v1.2 | 统一所有单位、枚举、分类的引用格式为"引用XX:编码"规范格式，移除ToolingLedger的生命周期状态说明 | 危放 |
| 2026-01-23 | v1.3 | 修复FactoryManaged接口属性缺失（4个模型添加bizOrg和factory字段）、为继承GenericLink的7个模型添加源数据实体元信息 | 李飞 |
| 2025-12-29 | v1.1 | 优化生命周期继承和业务状态：ToolingMaintTask/ToolingCalibrateTask使用COMMON_LIFECYCLE，添加bizStatus属性字段 | 危放  |
| 2025-12-17 | v1.0 | 基于原工具工装数据模型,按照数据模型规范重新组织和规范化 | 王晴  |
