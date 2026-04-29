# 仓储物料管理数据模型

## 文档说明

**基本信息**

- 文档版本：v1.9 | 更新日期：2026-04-08 | 维护团队：产品研发团队
- 目标受众：产品研发团队、项目交付团队

**文档定位**

本文档定义KMMOM3.x仓储物料管理（WMS）模块的数据模型，包括仓储物料管理、库存控制、出入库作业、物流管理等业务功能的实体定义、属性规范和持久化映射，确保仓储业务数据结构的完整性和一致性。

**内容结构**

| 章节                   | 核心问题                   | 内容说明                                       |
| ---------------------- | -------------------------- | ---------------------------------------------- |
| 一、术语、定义和缩略语 | WMS模块涉及哪些专业术语？  | 定义入库、出库、库存、盘点等业务术语和缩略语   |
| 二、入库管理           | 入库业务需要哪些数据模型？ | 定义入库申请单、入库申请单物料、入库记录等模型 |
| 三、出库管理           | 出库业务需要哪些数据模型？ | 定义出库申请单、出库申请单物料、出库记录等模型 |
| 四、库存管理           | 库存管理需要哪些数据模型？ | 定义库存、库存批次属性等模型                   |
| 五、箱号管理           | 箱号管理需要哪些数据模型？ | 定义组箱记录等模型                             |
| 六、上架任务管理       | 上架任务需要哪些数据模型？ | 定义上架任务、上架任务明细等模型               |
| 七、下架任务管理       | 下架任务需要哪些数据模型？ | 定义下架任务、下架任务明细等模型               |
| 八、产品退货管理       | 产品退货需要哪些数据模型？ | 定义产品退货单、产品退货单明细等模型           |
| 九、盘点管理           | 盘点业务需要哪些数据模型？ | 定义盘点单、盘点单物料明细等模型               |
| 十、物流管理           | 物流管理需要哪些数据模型？ | 定义位置、位置绑定关系、物流任务、物流任务明细等模型 |

---

## 一、术语、定义和缩略语

| 术语       | 定义                                                 | 缩略语 |
| ---------- | ---------------------------------------------------- | ------ |
| 入库申请单 | 记录物料入库业务需求的单据，用于申请将物料存入仓库   | -      |
| 出库申请单 | 记录物料出库业务需求的单据，用于申请从仓库取出物料   | -      |
| 库存       | 物料在仓库中的存储状态、数量及位置信息               | -      |
| 盘点       | 对仓库中实际库存进行清点核对，确保账实一致的业务活动 | -      |
| 库房       | 存储物料的物理仓库，是库存管理的基本单元             | -      |
| 库位       | 仓库内的具体存储位置，用于精细化管理物料存放         | -      |
| 批次号     | 物料的批次标识，用于追溯同批次物料的来源和流向       | -      |
| 序列号     | 物料的唯一标识，用于追踪单个物料的全生命周期         | SN     |
| 过账       | 将盘点结果正式记录到库存账目中，使盘点数据生效       | -      |
| 物流位置   | 用于承载仓储、工位、工序、下货区域等物流落点的通用位置主数据 | -      |
| 到货点     | 物料或空车默认到达的物流位置                         | -      |
| 出货点     | 物料默认发出的物流位置                               | -      |
| 物流任务   | 面向发料、退料、工序间周转、入库周转、临时周转等场景的执行任务 | -      |
| 空车呼叫   | 请求空车到达指定位置的物流任务类型                   | -      |

---

## 二、入库管理

### 2.1 入库申请单（InStoreApplyBill）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`, `LifecycleManaged` | **表名:** `MOM_IN_STORE_APPLY_BILL`

| 属性中文名称 | 属性英文名称     | 数据库列名          | 数据类型 | 长度 | 约束 | 说明                               |
| ------------ | ---------------- | ------------------- | -------- | ---- | ---- | ---------------------------------- |
| 入库方式     | `inStoreType`    | `CIN_STORE_TYPE`    | 枚举     | 256  | 必填 | 引用枚举:IN_STORE_TYPE             |
| 入库工厂     | `inStoreFactory` | `CIN_STORE_FACTORY` | 引用对象 | -    | 必填 | 引用BizOrg                         |
| 关闭标记     | `closeFlag`      | `CCLOSE_FLAG`       | 布尔     | -    | 无   | 标识申请单是否已关闭               |
| 来源单号     | `sourceBillCode` | `CSOURCE_BILL_CODE` | 字符串   | 256  | 无   | 来源单号                           |
| 目标仓库     | `warehouse`      | `CWAREHOUSE`        | 引用对象 | -    | 必填 | 引用Warehouse                      |
| 业务状态     | `bizStatus`      | `CBIZ_STATUS`       | 枚举     | 256  | 无   | 引用枚举:InStoreApplyBillBizStatus |

### 2.2 入库申请单明细（InStoreApplyBillMaterialLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_IN_STORE_APPLY_BILL_MATERIAL_LINK` | **源数据实体:** `InStoreApplyBill`

| 属性中文名称 | 属性英文名称        | 数据库列名            | 数据类型 | 长度 | 约束 | 说明                               |
| ------------ | ------------------- | --------------------- | -------- | ---- | ---- | ---------------------------------- |
| 物料         | `material`          | `CMATERIAL`           | 引用对象 | -    | 必填 | 引用Material                       |
| 计量单位     | `measureUnit`       | `CMEASURE_UNIT`       | 单位     | -    | 无   | 引用单位:measureUnit               |
| 计划数量     | `planQty`           | `CPLAN_QTY`           | 浮点型   | -    | 必填 | 申请入库的计划数量                 |
| 已入库数量   | `inQty`             | `CIN_QTY`             | 浮点型   | -    | 无   | 已完成入库的数量                   |
| 库房         | `warehouse`         | `CWAREHOUSE`          | 引用对象 | -    | 无   | 引用Warehouse                      |
| 库位         | `warehouseLocation` | `CWAREHOUSE_LOCATION` | 引用对象 | -    | 无   | 引用WarehouseLocation              |
| 批次号       | `batchNo`           | `CBATCH_NO`           | 字符串   | 256  | 无   | 物料批次标识                       |
| 序列号       | `sn`                | `CSN`                 | 字符串   | 256  | 无   | 物料序列号                         |
| 生产厂家     | `manufacturer`      | `CMANUFACTURER`       | 引用对象 | -    | 无   | 引用BizOrg                         |
| 业务状态     | `bizStatus`         | `CBIZ_STATUS`         | 枚举     | 256  | 无   | 引用枚举:InStoreApplyBillBizStatus |
| 已组箱数量   | `packedQty`         | `CPACKED_QTY`         | 浮点型   |      |      | 已组箱数量                         |
| 组箱状态     | `packStatus `       | `CPACK_STATUS`        | 枚举     |      |      | 引用枚举:WmsPackStatus             |

### 2.3 入库单（InStoreBill）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_IN_STORE_BILL`

| 属性中文名称 | 属性英文名称       | 数据库列名             | 数据类型 | 长度 | 约束 | 说明                   |
| ------------ | ------------------ | ---------------------- | -------- | ---- | ---- | ---------------------- |
| 入库单号     | `code`             | `CCODE`                | 字符串   | 256  | 无   | 入库单号               |
| 申请单号     | `applyCode`        | `CAPPLY_CODE`          | 字符串   | 256  | 无   | 申请单号               |
| 来源单号     | `sourceBillCode`   | `CSOURCE_BILL_CODE`    | 字符串   | 256  | 无   | 来源单号               |
| 入库方式     | `inStoreType`      | `CIN_STORE_TYPE`       | 枚举     | 256  | 必填 | 引用枚举:IN_STORE_TYPE |
| 入库申请单   | `inStoreApplyBill` | `CIN_STORE_APPLY_BILL` | 引用对象 | -    | 必填 | 引用InStoreApplyBill   |
| 入库人       | `inStorePerson`    | `CIN_STORE_PERSON`     | 用户     | -    | -    | 入库人                 |
| 入库时间     | `inStoreTime`      | `CIN_STORE_TIME`       | 日期时间 | -    | -    | 入库时间               |
| 库房         | `warehouse`        | `CWAREHOUSE`           | 引用对象 | -    | 必填 | 引用Warehouse          |
| 组箱记录     | `PackRecord`       | `CPACK_RECORD`         | 引用对象 | -    | 必填 | 引用PackRecord         |

### 2.4 入库单明细（InStoreBillLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_IN_STORE_BILL_LINK` | **源数据实体:** `InStoreBill`

| 属性中文名称   | 属性英文名称               | 数据库列名                      | 数据类型 | 长度 | 约束 | 说明                             |
| -------------- | -------------------------- | ------------------------------- | -------- | ---- | ---- | -------------------------------- |
| 入库单编码     | `inStoreBillCode`          | `CIN_STORE_BILL_CODE`           | 字符串   | 256  | 无   | 入库单编码                       |
| 入库申请单     | `inStoreApplyBill`         | `CIN_STORE_APPLY_BILL`          | 引用对象 | -    | 必填 | 引用InStoreApplyBill             |
| 入库申请单物料 | `inStoreApplyBillMaterial` | `CIN_STORE_APPLY_BILL_MATERIAL` | 引用对象 | -    | 必填 | 引用InStoreApplyBillMaterialLink |
| 物料           | `material`                 | `CMATERIAL`                     | 引用对象 | -    | 必填 | 引用Material                     |
| 计量单位       | `measureUnit`              | `CMEASURE_UNIT`                 | 单位     | -    | 无   | 引用单位:measureUnit             |
| 库房           | `warehouse`                | `CWAREHOUSE`                    | 引用对象 | -    | 必填 | 引用Warehouse                    |
| 库位           | `warehouseLocation`        | `CWAREHOUSE_LOCATION`           | 引用对象 | -    | 无   | 引用WarehouseLocation            |
| 入库数量       | `qty`                      | `CQTY`                          | 浮点型   | -    | 必填 | 实际入库数量                     |
| 批次号         | `batchNo`                  | `CBATCH_NO`                     | 字符串   | 256  | 无   | 物料批次标识                     |
| 序列号         | `sn`                       | `CSN`                           | 字符串   | 256  | 无   | 物料序列号                       |
| 入库方式       | `inStoreType`              | `CIN_STORE_TYPE`                | 枚举     | 256  | 必填 | 引用枚举:IN_STORE_TYPE           |

---

## 三、出库管理

### 3.1 出库申请单（OutStoreApplyBill）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`, `LifecycleManaged` | **表名:** `MOM_OUT_STORE_APPLY_BILL`

| 属性中文名称 | 属性英文名称      | 数据库列名           | 数据类型 | 长度 | 约束 | 说明                                |
| ------------ | ----------------- | -------------------- | -------- | ---- | ---- | ----------------------------------- |
| 出库方式     | `outStoreType`    | `COUT_STORE_TYPE`    | 枚举     | 256  | 必填 | 引用枚举:OUT_STORE_TYPE             |
| 出库工厂     | `outStoreFactory` | `COUT_STORE_FACTORY` | 引用对象 | -    | 必填 | 引用BizOrg                          |
| 关闭标记     | `closeFlag`       | `CCLOSE_FLAG`        | 布尔     | -    | -    | 标识申请单是否已关闭                |
| 控制状态     | `controlStatus`   | `CCONTROL_STATUS`    | 枚举     | 256  | 必填 | 引用枚举controlStatus               |
| 来源单号     | `sourceBillCode`  | `CSOURCE_BILL_CODE`  | 字符串   | 256  | 无   | 来源单号                            |
| 库房         | `warehouse`       | `CWAREHOUSE`         | 引用对象 | -    | 必填 | 引用Warehouse                       |
| 业务状态     | `bizStatus`       | `CBIZ_STATUS`        | 枚举     | 256  | 无   | 引用枚举:OutStoreApplyBillBizStatus |

### 3.2 出库申请单明细（OutStoreApplyBillMaterialLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_OUT_STORE_APPLY_BILL_MATERIAL_LINK` | **源数据实体:** `OutStoreApplyBill`

| 属性中文名称 | 属性英文名称          | 数据库列名              | 数据类型 | 长度 | 约束 | 说明                                |
| ------------ | --------------------- | ----------------------- | -------- | ---- | ---- | ----------------------------------- |
| 物料         | `material`            | `CMATERIAL`             | 引用对象 | -    | 必填 | 引用Material                        |
| 计量单位     | `measureUnit`         | `CMEASURE_UNIT`         | 单位     | -    | 无   | 引用单位:measureUnit                |
| 计划数量     | `planQty`             | `CPLAN_QTY`             | 浮点型   | -    | 必填 | 申请出库的计划数量                  |
| 已出库数量   | `outQty`              | `COUT_QTY`              | 浮点型   | -    | 无   | 已完成出库的数量                    |
| 库房         | `warehouse`           | `CWAREHOUSE`            | 引用对象 | -    | 必填 | 引用Warehouse                       |
| 库位         | `warehouseLocation`   | `CWAREHOUSE_LOCATION`   | 引用对象 | -    | 无   | 引用WarehouseLocation               |
| 需求到料时间 | `needTime`            | `CNEED_TIME`            | 日期时间 | -    | 无   | 来源于物料准备计划明细的需求到料时间 |
| 到货位置     | `inboundLocation`     | `CINBOUND_LOCATION`     | 引用对象 | -    | 无   | 来源于物料准备计划明细的到货位置，引用LogisticsLocation |
| 批次号       | `batchNo`             | `CBATCH_NO`             | 字符串   | 256  | 无   | 物料批次标识                        |
| 序列号       | `sn`                  | `CSN`                   | 字符串   | 256  | 无   | 物料序列号                          |
| 替换件物料   | `replacementMaterial` | `CREPLACEMENT_MATERIAL` | 引用对象 | -    | 无   | 引用Material（允许使用替换件）      |
| 业务状态     | `bizStatus`           | `CBIZ_STATUS`           | 枚举     | 256  | 无   | 引用枚举:OutStoreApplyBillBizStatus |
| 控制状态     | `controlStatus`       | `CCONTROL_STATUS`       | 枚举     | 256  | 必填 | 引用枚举controlStatus               |
| 已拣配数量   | `pickedQty`           | `CPICKED_QTY`           | 浮点型   | -    | 无   | 已拣配数量                          |
| 已拣配状态   | `pickStatus`          | `CPICK_STATUS`          | 枚举     | 256  | 无   | 引用枚举:WmsPickStatus              |

### 3.3 出库单（OutStoreBill）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `FactoryManaged` | **表名:** `MOM_OUT_STORE_BILL`

| 属性中文名称 | 属性英文名称        | 数据库列名              | 数据类型 | 长度 | 约束 | 说明                    |
| ------------ | ------------------- | ----------------------- | -------- | ---- | ---- | ----------------------- |
| 出库单号     | `code`              | `CCODE`                 | 字符串   | 256  | 无   | 无                      |
| 申请单号     | `applyCode`         | `CAPPLY_CODE`           | 字符串   | 256  | 无   | 出库申请单              |
| 来源单号     | `sourceBillCode`    | `CSOURCE_BILL_CODE`     | 字符串   | 256  | 无   | 来源单号                |
| 出库方式     | `outStoreType`      | `COUT_STORE_TYPE`       | 枚举     | 256  | 必填 | 引用枚举:OUT_STORE_TYPE |
| 出库申请单   | `outStoreApplyBill` | `COUT_STORE_APPLY_BILL` | 引用对象 | -    | -    | 引用OutStoreApplyBill   |
| 出库原因     | `outStoreReason`    | `COUT_STORE_REASON`     | 字符串   | 256  | 无   | 出库原因                |
| 出库人       | `outStorePerson`    | `COUT_STORE_PERSON`     | 用户     | -    | 无   | 出库人                  |
| 出库时间     | `outStoreTime`      | `COUT_STORE_TIME`       | 日期时间 | -    | -    | 出库时间                |
| 库房         | `warehouse`         | `CWAREHOUSE`            | 引用对象 | -    | 必填 | 引用Warehouse           |
| 组箱记录     | `PackRecord`        | `CPACK_RECORD`          | 引用对象 | -    | 必填 | 引用PackRecord          |

### 3.4 出库单明细（OutStoreBillLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_OUT_STORE_BILL_LINK` | **源数据实体:** `OutStoreBill`

| 属性中文名称   | 属性英文名称                | 数据库列名                       | 数据类型 | 长度 | 约束 | 说明                              |
| -------------- | --------------------------- | -------------------------------- | -------- | ---- | ---- | --------------------------------- |
| 编码           | `outStoreBillCode`          | `COUT_STORE_BILL_CODE`           | 字符串   | 256  | 必填 | 出库单编码                        |
| 出库申请单     | `outStoreApplyBill`         | `COUT_STORE_APPLY_BILL`          | 引用对象 | -    | 无   | 引用OutStoreApplyBill             |
| 出库方式       | `outStoreType`              | `COUT_STORE_TYPE`                | 枚举     | 256  | 必填 | 引用枚举:OUT_STORE_TYPE           |
| 出库申请单物料 | `outStoreApplyBillMaterial` | `COUT_STORE_APPLY_BILL_MATERIAL` | 引用对象 | -    | 无   | 引用OutStoreApplyBillMaterialLink |
| 物料           | `material`                  | `CMATERIAL`                      | 引用对象 | -    | 必填 | 引用Material                      |
| 计量单位       | `measureUnit`               | `CMEASURE_UNIT`                  | 单位     | -    | 无   | 引用单位:measureUnit              |
| 库房           | `warehouse`                 | `CWAREHOUSE`                     | 引用对象 | -    | 必填 | 引用Warehouse                     |
| 库位           | `warehouseLocation`         | `CWAREHOUSE_LOCATION`            | 引用对象 | -    | 无   | 引用WarehouseLocation             |
| 出库数量       | `qty`                       | `CQTY`                           | 浮点型   | -    | 必填 | 实际出库数量                      |
| 批次号         | `batchNo`                   | `CBATCH_NO`                      | 字符串   | 256  | 无   | 物料批次标识                      |
| 序列号         | `sn`                        | `CSN`                            | 字符串   | 256  | 无   | 物料序列号                        |
| 库存批次属性   | `inventoryBatchAttribute`   | `CINVENTORY_BATCH_ATTRIBUTE`     | 引用对象 | -    | 无   | 引用InventoryBatchAttribute       |

---

## 四、库存管理

### 4.1 库存（Inventory）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`| **表名:** `MOM_INVENTORY`

| 属性中文名称 | 属性英文名称              | 数据库列名                   | 数据类型 | 长度 | 约束 | 说明                                     |
| ------------ | ------------------------- | ---------------------------- | -------- | ---- | ---- | ---------------------------------------- |
| 库存标识     | `inventoryMark`           | `CINVENTORY_MARK`            | 字符串   | 512  | 必填 | 库房、库位、物料、批次号、顺序号确定唯一 |
| 库房         | `warehouse`               | `CWAREHOUSE`                 | 引用对象 | -    | 必填 | 引用Warehouse                            |
| 库位         | `warehouseLocation`       | `CWAREHOUSE_LOCATION`        | 引用对象 | -    | 无   | 引用WarehouseLocation                    |
| 物料         | `material`                | `CMATERIAL`                  | 引用对象 | -    | 必填 | 引用Material                             |
| 计量单位     | `measureUnit`             | `CMEASURE_UNIT`              | 单位     | -    | 无   | 引用单位:measureUnit                     |
| 库存数量     | `qty`                     | `CQTY`                       | 浮点型   | -    | 必填 | 当前库存数量                             |
| 批次号       | `batchNo`                 | `CBATCH_NO`                  | 字符串   | 256  | 无   | 物料批次标识                             |
| 序列号       | `sn`                      | `CSN`                        | 字符串   | 256  | 无   | 物料序列号                               |
| 库存批次属性 | `inventoryBatchAttribute` | `CINVENTORY_BATCH_ATTRIBUTE` | 引用对象 | -    | 无   | 引用InventoryBatchAttribute              |
| 业务状态     | `bizStatus`               | `CBIZ_STATUS`                | 枚举     |      | 无   | 引用枚举:InventoryBizStatus              |
| 箱号         | `boxNo`                   | `CBOX_NO`                    | 字符串   | 256  | 无   |                                          |

### 4.2 库存批次属性（InventoryBatchAttribute）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_INVENTORY_BATCH_ATTRIBUTE`

| 属性中文名称 | 属性英文名称         | 数据库列名              | 数据类型 | 长度 | 约束 | 说明               |
| ------------ | -------------------- | ----------------------- | -------- | ---- | ---- | ------------------ |
| 批次属性标识 | `batchAttributeMark` | `CBATCH_ATTRIBUTE_MARK` | 字符串   | 256  | 无   | 批次属性的唯一标识 |
| 物料         | `material`           | `CMATERIAL`             | 引用对象 | -    | 无   | 引用Material       |
| 批次号       | `batchNo`            | `CBATCH_NO`             | 字符串   | 256  | 无   | 物料批次标识       |
| 生产厂家     | `manufacturer`       | `CMANUFACTURER`         | 引用对象 | -    | 无   | 引用BizOrg         |

---

## 五、箱号管理

### 5.1 组箱记录（PackRecord）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`, `LifecycleManaged` | **表名:** `MOM_PACK_RECORD`

| 属性中文名称 | 属性英文名称     | 数据库列名          | 数据类型 | 长度 | 约束     | 说明                                         |
| ------------ | ---------------- | ------------------- | -------- | ---- | -------- | -------------------------------------------- |
| 编码         | `code`           | `CCODE`            | 字符串   | 256  | 必填     | 系统自动生成，格式：BOX-YYYYMMDD-XXX         |
| 组箱类型     | `packType`       | `CPACK_TYPE`        | 枚举     | 256  | 必填     | 入库组箱、拣配组箱、移库组箱、退货组箱       |
| 来源单据类型 | `sourceBillType` | `CSOURCE_BILL_TYPE` | 枚举     | 256  | 必填     | 入库申请单、出库申请单、移库任务、产品退货单 |
| 来源单据号   | `sourceBillCode` | `CSOURCE_BILL_CODE` | 字符串   | 256  | 必填     | 对应来源单据编号                             |
| 来源单据ID   | `sourceBillId`   | `CSOURCE_BILL_ID`   | 长整型   |      | 无       | 对应来源单据ID                               |
| 目标料箱号   | `targetBoxNo`    | `CTARGET_BOX_NO`    | 字符串   | 256  | 必填     | 组箱完成后的目标料箱号                       |
| 组箱方式     | `packMethod`     | `CPACK_METHOD`      | 枚举     | 256  | 条件必填 | 空箱组箱、已有箱组箱（入库组箱时必填）       |
| 组箱状态     | `bizStatus`      | `CBIZ_STATUS`       | 枚举     | 256  | 必填     | 暂存、已确认、已取消                         |
| 确认人       | `confirmer`      | `CCONFIRMER`        | 用户     | -    | 条件记录 | 组箱状态为“已确认”时记录                     |
| 确认时间     | `confirmTime`    | `CCONFIRM_TIME`     | 日期时间 | -    | 条件记录 | 组箱状态为“已确认”时记录                     |
| 备注         | `remark`         | `CREMARK`           | 字符串   | 1024 | 无       | 组箱补充说明                                 |

### 5.2 组箱记录明细（PackRecordLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_PACK_RECORD_LINK` | **源数据实体:** `PackRecord`

| 属性中文名称     | 属性英文名称     | 数据库列名          | 数据类型 | 长度 | 约束     | 说明                                 |
| ---------------- | ---------------- | ------------------- | -------- | ---- | -------- | ------------------------------------ |
| 组箱记录         | `source`         | `CSOURCE`           | 引用对象 | -    | 必填     | 引用PackRecord                       |
| 物料             | `material`       | `CMATERIAL`         | 引用对象 | -    | 必填     | 引用Material                         |
| 批次号           | `batchNo`        | `CBATCH_NO`         | 字符串   | 256  | 无       | 物料批次标识                         |
| 序列号           | `sn`             | `CSN`               | 字符串   | 256  | 无       | 物料序列号                           |
| 数量             | `qty`            | `CQTY`              | 浮点型   | -    | 无       | 组箱数量                             |
| 来源单据明细ID   | `sourceLinkId`   | `CSOURCE_LINK_ID`   | 长整型   |      | 无       | 对应来源单据明细ID                   |
| 组箱状态         | `bizStatus`      | `CBIZ_STATUS`       | 枚举     | 256  | 必填     | 暂存、已确认、已取消                 |
| 来源单据明细类型 | `sourceLinkType` | `CSOURCE_LINK_TYPE` | 字符串   | 256  | 必填     | 对应来源单明细类型                   |
| 原料箱号         | `sourceBoxNo`    | `CSOURCE_BOX_NO`    | 字符串   | 256  | 条件必填 | 拣配组箱、移库组箱、已有箱组箱时必填 |

### 5.3 箱号位置记录（BoxLocationRecord）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`, `LifecycleManaged` | **表名:** `MOM_BOX_LOCATION_RECORD`

| 属性中文名称 | 属性英文名称        | 数据库列名            | 数据类型 | 长度 | 约束     | 说明                  |
| ------------ | ------------------- | --------------------- | -------- | ---- | -------- | --------------------- |
| 箱号         | `boxNo`             | `CBOX_NO`             | 字符串   | 256  | 条件必填 |                       |
| 目标库房     | `warehouse`         | `CWAREHOUSE`          | 引用对象 | -    | 无       | 引用Warehouse         |
| 库位         | `warehouseLocation` | `CWAREHOUSE_LOCATION` | 引用对象 | -    | 无       | 引用WarehouseLocation |
| 状态         | `status`            | `CSTATUS`             | 枚举     | 256  | 必填     | 引用枚举:WmsBoxStatus |



---

## 六、上架任务管理

### 6.1 上架任务（PutawayTask）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `SecurityManaged`, `FactoryManaged` | **表名:** `MOM_PUTAWAY_TASK`

| 属性中文名称 | 属性英文名称        | 数据库列名              | 数据类型 | 长度 | 约束 | 说明                         |
| ------------ | ------------------- | ----------------------- | -------- | ---- | ---- | ---------------------------- |
| 任务编码     | `code`              | `CCODE`                 | 字符串   | 256  | 必填 | 上架任务编码                 |
| 料箱号       | `boxNo`             | `CBOX_NO`               | 字符串   | 256  | 无   | 料箱号                       |
| 目标库房     | `warehouse`         | `CWAREHOUSE`            | 引用对象 | -    | 无   | 引用Warehouse                |
| 库位         | `warehouseLocation` | `CWAREHOUSE_LOCATION`   | 引用对象 | -    | 无   | 引用WarehouseLocation        |
| 任务状态     | `bizStatus`         | `CBIZ_STATUS`           | 枚举     | 256  | 必填 | 引用枚举:WmsTaskStatus       |
| 任务类型     | `taskType`          | `CTASK_TYPE`            | 枚举     | 256  | 必填 | 引用枚举:PutawayTaskType     |
| 完成时间     | `completeTime`      | `CCOMPLETE_TIME`        | 日期时间 | -    | 无   | 任务完成时间                 |

### 6.2 上架任务与组箱记录的关系（PutawayTaskPackLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_PUTAWAY_TASK_PACK_LINK` | **源数据实体:** `PutawayTask`

| 属性中文名称 | 属性英文名称 | 数据库列名     | 数据类型 | 长度 | 约束 | 说明           |
| ------------ | ------------ | -------------- | -------- | ---- | ---- | -------------- |
| 组箱记录     | `PackRecord` | `CPACK_RECORD` | 引用对象 | -    | 必填 | 引用PackRecord |

### 6.3 上架任务明细（PutawayTaskLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_PUTAWAY_TASK_LINK` | **源数据实体:** `PutawayTask`

| 属性中文名称     | 属性英文名称       | 数据库列名          | 数据类型 | 长度 | 约束 | 说明               |
| ---------------- | ------------------ | ------------------- | -------- | ---- | ---- | ------------------ |
| 上架任务         | `source`           | `CSOURCE`           | 引用对象 | -    | 必填 | 引用PutawayTask    |
| 物料             | `material`         | `CMATERIAL`         | 引用对象 | -    | 必填 | 引用Material       |
| 批次号           | `batchNo`          | `CBATCH_NO`         | 字符串   | 256  | 无   | 物料批次标识       |
| 序列号           | `sn`               | `CSN`               | 字符串   | 256  | 无   | 物料序列号         |
| 数量             | `qty`              | `CQTY`              | 浮点型   | -    | 必填 | 上架数量           |
| 来源单据号       | `sourceBillCode`   | `CSOURCE_BILL_CODE` | 字符串   | 256  | 必填 | 对应来源单据编号   |
| 来源单据明细类型 | `sourceLinkType`   | `CSOURCE_LINK_TYPE` | 字符串   | 256  | 必填 | 对应来源单明细类型 |
| 来源单据明细ID   | `sourceLinkId`     | `CSOURCE_LINK_ID`   | 长整型   |      | 无   | 对应来源单据明细ID |
| 组箱记录明细ID   | `packRecordLinkId` | `CPACK_RECORD_LINK` | 长整型   |      | 无   | 组箱记录明细ID     |

---

## 七、下架任务管理

### 7.1 下架任务（PickingTask）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `SecurityManaged`, `FactoryManaged` | **表名:** `MOM_PICKING_TASK`

| 属性中文名称 | 属性英文名称        | 数据库列名            | 数据类型 | 长度 | 约束 | 说明                     |
| ------------ | ------------------- | --------------------- | -------- | ---- | ---- | ------------------------ |
| 编码         | `code`              | `CCODE`               | 字符串   | 256  | 必填 | 下架任务编码             |
| 任务类型     | `taskType`          | `CTASK_TYPE`          | 枚举     | 256  | 无   | 引用枚举:WmsPickdownType |
| 源库房       | `warehouse`         | `CWAREHOUSE`          | 引用对象 | -    | 无   | 引用Warehouse            |
| 源库位       | `warehouseLocation` | `CWAREHOUSE_LOCATION` | 引用对象 | -    | 无   | 引用WarehouseLocation    |
| 箱号         | `boxNo`             | `CBOX_NO`             | 字符串   | 256  | 无   | 箱号                     |
| 任务状态     | `bizStatus`         | `CBIZ_STATUS`         | 枚举     | 256  | 必填 | 引用枚举:WmsTaskStatus   |
| 完成时间     | `completeTime`      | `CCOMPLETE_TIME`      | 日期时间 | -    | 无   | 任务完成时间             |

### 7.2 下架任务明细（PickingTaskLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_PICKING_TASK_LINK` | **源数据实体:** `PickingTask`

| 属性中文名称     | 属性英文名称       | 数据库列名          | 数据类型 | 长度 | 约束 | 说明               |
| ---------------- | ------------------ | ------------------- | -------- | ---- | ---- | ------------------ |
| 下架任务         | `source`           | `CSOURCE`           | 引用对象 | -    | 必填 | 引用PickingTask    |
| 物料             | `material`         | `CMATERIAL`         | 引用对象 | -    | 必填 | 引用Material       |
| 批次号           | `batchNo`          | `CBATCH_NO`         | 字符串   | 256  | 无   | 物料批次标识       |
| 序列号           | `sn`               | `CSN`               | 字符串   | 256  | 无   | 物料序列号         |
| 数量             | `qty`              | `CQTY`              | 浮点型   | -    | 无   | 下架数量           |
| 来源单据号       | `sourceBillCode`   | `CSOURCE_BILL_CODE` | 字符串   | 256  | 无   | 对应来源单据编号   |
| 来源单据明细类型 | `sourceLinkType`   | `CSOURCE_LINK_TYPE` | 字符串   | 256  | 无   | 对应来源单明细类型 |
| 来源单据明细ID   | `sourceLinkId`     | `CSOURCE_LINK_ID`   | 长整型   |      | 无   | 对应来源单据明细ID |
| 组箱记录明细ID   | `packRecordLinkId` | `CPACK_RECORD_LINK` | 长整型   |      | 无   | 组箱记录明细ID     |

---

## 八、产品退货管理

### 8.1 产品退货单（ProductReturnOrder）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `SecurityManaged`, `FactoryManaged` | **表名:** `MOM_PRODUCT_RETURN_ORDER`

| 属性中文名称 | 属性英文名称   | 数据库列名         | 数据类型 | 长度 | 约束 | 说明                      |
| ------------ | -------------- | ------------------ | -------- | ---- | ---- | ------------------------- |
| 编码         | `code`         | `CCODE`            | 字符串   | 256  | 必填 | 产品退货单编码            |
| 入库单       | `inStoreBill`  | `CIN_STORE_BILL`   | 引用对象 | -    | 无   | 引用InStoreBill           |
| 退货日期     | `returnDate`   | `CRETURN_DATE`     | 日期时间 | -    | 无   | 退货日期                  |
| 退货原因     | `returnReason` | `CRETURN_REASON`   | 字符串   | 256  | 无   | 退货原因                  |
| 退货状态     | `bizStatus`    | `CRETURN_STATUS`   | 枚举     | 256  | 无   | 引用枚举:WmsReturnStatus  |
| 备注         | `remark`       | `CREMARK`          | 字符串   | 256  | 无   | 备注信息                  |

### 8.2 产品退货单明细（ProductReturnOrderLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_PRODUCT_RETURN_ORDER_LINK` | **源数据实体:** `ProductReturnOrder`

| 属性中文名称 | 属性英文名称   | 数据库列名       | 数据类型 | 长度 | 约束 | 说明                     |
| ------------ | -------------- | ---------------- | -------- | ---- | ---- | ------------------------ |
| 产品退货单   | `source`       | `CSOURCE`        | 引用对象 | -    | 必填 | 引用ProductReturnOrder   |
| 物料         | `material`     | `CMATERIAL`      | 引用对象 | -    | 无   | 引用Material             |
| 批次号       | `batchNo`      | `CBATCH_NO`      | 字符串   | 256  | 无   | 物料批次标识             |
| 序列号       | `sn`           | `CSN`            | 字符串   | 256  | 无   | 物料序列号               |
| 数量         | `qty`          | `CQTY`           | 浮点型   | -    | 无   | 退货数量                 |
| 不良原因     | `defectReason` | `CDEFECT_REASON` | 字符串   | 256  | 无   | 不良原因                 |

---

## 九、盘点管理

### 9.1 盘点单（StoreCountBill）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged` | **表名:** `MOM_STORE_COUNT_BILL`

_注：盘点单主体属性由 `BusinessObject` 和扩展接口提供。_

| 属性中文名称 | 属性英文名称         | 数据库列名              | 数据类型 | 长度 | 约束 | 说明               |
| ------------ | -------------------- | ----------------------- | -------- | ---- | ---- | ------------------ |
| 业务状态 | `bizStatus` | `CBIZ_STATUS` | 枚举   |   | 无   | 引用枚举:StoreCountBillBizStatus |

### 9.2 盘点单物料明细（StoreCountBillMaterialLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_STORE_COUNT_BILL_MATERIAL_LINK` | **源数据实体:** `StoreCountBill`

| 属性中文名称 | 属性英文名称        | 数据库列名            | 数据类型 | 长度 | 约束 | 说明                             |
| ------------ | ------------------- | --------------------- | -------- | ---- | ---- | -------------------------------- |
| 物料         | `material`          | `CMATERIAL`           | 引用对象 | -    | 必填 | 引用Material                     |
| 计量单位     | `measureUnit`       | `CMEASURE_UNIT`       | 单位     | -    | 无   | 引用单位:measureUnit             |
| 库存数量     | `qty`               | `CQTY`                | 浮点型   | -    | 必填 | 盘点数量                         |
| 库房         | `warehouse`         | `CWAREHOUSE`          | 引用对象 | -    | 必填 | 引用Warehouse                    |
| 库位         | `warehouseLocation` | `CWAREHOUSE_LOCATION` | 引用对象 | -    | 无   | 引用WarehouseLocation            |
| 批次号       | `batchNo`           | `CBATCH_NO`           | 字符串   | 256  | 无   | 物料批次标识                     |
| 序列号       | `sn`                | `CSN`                 | 字符串   | 256  | 无   | 物料序列号                       |
| 实盘数量     | `actualQty`         | `CACTUAL_QTY`         | 浮点型     | - | 无   | 实盘数量 |
| 库存   | `inventory` | `CINVENTORY` | 引用对象 | - | 无   | 引用库存 |

---

## 十、物流管理

### 10.1 位置（LogisticsLocation）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged` | **表名:** `MOM_LOGISTICS_LOCATION`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
| ------------ | ------------ | ---------- | -------- | ---- | ---- | ---- |
| 位置类型     | `locationType` | `CLOCATION_TYPE` | 枚举 | 256 | 必填 | 引用枚举:LogisticsLocationType |

### 10.2 工作中心位置绑定关系（WorkCenterLocationBinding）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `FactoryManaged` | **表名:** `MOM_WORK_CENTER_LOCATION_BINDING`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
| ------------ | ------------ | ---------- | -------- | ---- | ---- | ---- |
| 工作中心     | `workCenter` | `CWORK_CENTER` | 引用对象 | - | 必填 | 引用WorkCenter；同一工作中心仅允许一条绑定关系 |
| 到货点       | `inboundLocation` | `CINBOUND_LOCATION` | 引用对象 | - | 无 | 引用LogisticsLocation，默认到货位置 |
| 出货点       | `outboundLocation` | `COUTBOUND_LOCATION` | 引用对象 | - | 无 | 引用LogisticsLocation，默认出货位置 |
| 备注         | `remark` | `CREMARK` | 字符串 | 1024 | 无 | 绑定关系补充说明 |

### 10.3 设备位置绑定关系（EquipLocationBinding）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `FactoryManaged` | **表名:** `MOM_EQUIP_LOCATION_BINDING`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
| ------------ | ------------ | ---------- | -------- | ---- | ---- | ---- |
| 设备         | `equip` | `CEQUIP` | 引用对象 | - | 必填 | 引用Equip；同一设备仅允许一条绑定关系 |
| 到货点       | `inboundLocation` | `CINBOUND_LOCATION` | 引用对象 | - | 无 | 引用LogisticsLocation，默认到货位置 |
| 出货点       | `outboundLocation` | `COUTBOUND_LOCATION` | 引用对象 | - | 无 | 引用LogisticsLocation，默认出货位置 |
| 备注         | `remark` | `CREMARK` | 字符串 | 1024 | 无 | 绑定关系补充说明 |

### 10.4 物流任务（LogisticsTask）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:**  | **表名:** `MOM_LOGISTICS_TASK`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
| ------------ | ------------ | ---------- | -------- | ---- | ---- | ---- |
| 任务类型     | `taskType` | `CTASK_TYPE` | 枚举 | 256 | 必填 | 引用枚举:LogisticsTaskType |
| 业务状态     | `bizStatus` | `CBIZ_STATUS` | 枚举 | 256 | 必填 | 引用枚举:LogisticsTaskStatus |
| 发出组织     | `sourceBizOrg` | `CSOURCE_BIZ_ORG` | 引用对象 | - | 无 | 引用BizOrg；周转类任务由发出位置自动带出，空车呼叫不填 |
| 到达组织     | `targetBizOrg` | `CTARGET_BIZ_ORG` | 引用对象 | - | 无 | 引用BizOrg；由到达位置自动带出，周转类任务和空车呼叫均可识别 |
| 发出位置     | `sourceLocation` | `CSOURCE_LOCATION` | 引用对象 | - | 无 | 引用LogisticsLocation；周转类任务必填，空车呼叫不填 |
| 到达位置     | `targetLocation` | `CTARGET_LOCATION` | 引用对象 | - | 无 | 引用LogisticsLocation；空车呼叫必填，发料周转、退料周转、工序间周转、入库周转、临时周转必填 |
| 工作中心     | `workCenter` | `CWORK_CENTER` | 引用对象 | - | 无 | 引用WorkCenter |
| 设备         | `equip` | `CEQUIP` | 引用对象 | - | 无 | 引用Equip |
| 接收人       | `receiveUser` | `CRECEIVE_USER` | 用户 | - | 无 | 接收任务的执行人；若未先接收而直接完成，则回写为当前完成人 |
| 接收时间     | `receiveTime` | `CRECEIVE_TIME` | 日期时间 | - | 无 | 任务被接收的时间；若未先接收而直接完成，则回写为直接完成时刻 |
| 完成时间     | `completeTime` | `CCOMPLETE_TIME` | 日期时间 | - | 无 | 任务确认完成或到位的时间 |

### 10.5 物流任务明细（LogisticsTaskLink）

**模型类型:** 业务模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_LOGISTICS_TASK_LINK` | **源数据实体:** `LogisticsTask`

_注：明细模型继承 `GenericLink` 的 `source` 属性，此处不重复展开。_

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
| ------------ | ------------ | ---------- | -------- | ---- | ---- | ---- |
| 物料准备计划明细     | `materialPreparePlanDetail` | `CMATERIAL_PREPARE_PLAN_DETAIL` | 引用对象 | - | 无 | 引用MaterialPreparationPlanDetailLink，来源单据 |
| 制造任务     | `manuTask` | `CMANU_TASK` | 引用对象 | - | 无 | 引用ManuTask，来源单据 |
| 物料         | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material；同一物流任务内同一物料仅允许多行 |
| 数量         | `qty` | `CQTY` | 浮点型 | - | 必填 | 物流任务物料数量 |
| 批次号       | `batchNumber` | `CBATCH_NUMBER` | 字符串 | 256 | 无 | 从来源出库明细或来源业务对象继承展示，不要求物流人员重复录入 |
| 序列号       | `serialNumber` | `CSERIAL_NUMBER` | 字符串 | 256 | 无 | 从来源出库明细或来源业务对象继承展示，不要求物流人员重复录入 |

---
## 变更记录

| 日期       | 版本 | 变更内容                                                                                                                                                           | 变更人 |
| ---------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| 2026-04-08 | v1.9 | 出库申请单明细（OutStoreApplyBillMaterialLink）增加需求到料时间、到货位置，并同步物流任务类型描述 | Codex |
| 2026-04-03 | v1.8 | 物流任务明细（LogisticsTaskLink）增加批次号（batchNumber）、序列号（serialNumber），从来源出库明细或来源业务对象继承展示 | 危放 |
| 2026-03-27 | v1.7 | 调整物流任务模型，补充发出组织、到达组织属性及说明 | 危放 |
| 2026-03-27 | v1.6 | 新增”十、物流管理”章节，补充位置、工作中心位置绑定关系、设备位置绑定关系、物流任务、物流任务明细模型，并补充相关术语与目录 | 危放 |
| 2026-03-05 | v1.5 | 新增”六、上架任务管理”、”七、下架任务管理”、”八、产品退货管理”章节及相关模型；原”盘点管理”章节顺延为”九、盘点管理”                                                | 李飞 |
| 2026-03-04 | v1.4 | 新增”五、箱号管理”章节及”组箱记录（PackRecord）”模型；原”盘点管理”章节顺延为”六、盘点管理”，并同步调整目录章节编号                                                | 李飞 |
| 2026-01-26 | v1.3 | 修复引用枚举类型编码，确保与数据库定义一致                                                                                                                         | 危放   |
| 2026-01-23 | v1.2 | 修复组织引用使用错误类型（4处Org改为BizOrg）、修复OutStoreBill接口格式错误、补充StoreCountBillMaterialLink完整属性、为继承GenericLink的3个模型添加源数据实体元信息 | 李飞   |
| 2025-12-29 | v1.1 | 改造业务属性为引用格式                                                                                                                                             | 王晴   |
| 2025-12-17 | v1.0 | 整合仓储管理和库存管理数据模型，创建符合新规范的WMS数据模型文档                                                                                                    | 王晴   |


