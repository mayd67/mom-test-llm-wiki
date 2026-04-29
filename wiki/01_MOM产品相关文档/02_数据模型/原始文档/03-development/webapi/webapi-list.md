# KM-MOM WebAPI 接口清单

## 概览

### 统计信息

| 统计项 | 数量 |
|--------|------|
| 接口总数 | 9 |
| 最后更新 | 2026-03-06 |

### 服务分布

| 服务 | 接口数量 | 说明 |
|------|---------|------|
| MES（制造执行系统） | 3 | 生产订单管理 |
| Approval（审批流程） | 6 | 审批流执行 |

## MES（制造执行系统）

### 生产订单API

**服务标识：** `mes`

**资源路径：** `/api/mes/v1/prodOrder`

---

#### 模拟释放生产订单

**基本信息**

```
接口路径: /api/mes/v1/prodOrder/simulateRelease
请求方法: POST
接口描述: 模拟释放生产订单
```

**详细说明**

```
1. 校验订单状态，确保可以释放
2. 校验释放数量的合法性
3. 根据订单数据和释放参数生成释放预览数据
4. 返回预览数据，但不保存到数据库
```

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| object | List<Mes_SimulatedProdOrderDTO> | 否 | 请求体对象 |
| └─ id | Long | 是 | 生产订单id |
| └─ currentQty | BigDecimal | 是 | 本次释放数量 |
| └─ unitQty | BigDecimal | 是 | 每份数量 |

**请求示例**

```json
{
  "object": [
    {
      "id": 123,
      "currentQty": 100.0,
      "unitQty": 100.0
    }
  ]
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer |  |
| errCode | String |  |
| message | String |  |
| data | List<Mes_SimulateReleaseManuOrderVO> |  |
| ├─ id | Long | 制造订单ID |
| ├─ code | String | 制造订单编码 |
| ├─ name | String | 制造订单名称 |
| ├─ manuType | String | 制造订单类型枚举值： MT_010_STANDARD - 标准操作 MT_020_TRANSFER - 转工 MT_030_REWORK - 返工 MT_040_REPAIR - 返修 |
| ├─ prodOrderId | Long | 生产订单ID |
| ├─ materialId | Long | 物料ID |
| ├─ materialCode | String | 物料编码 |
| ├─ materialName | String | 物料名称 |
| ├─ materialVersion | String | 物料版本 |
| ├─ materialDrawingNumber | String | 物料图号 |
| ├─ routingId | Long | 工艺路线ID |
| ├─ routingCode | String | 工艺路线编码 |
| ├─ routingName | String | 工艺路线名称 |
| ├─ routingVersion | String | 工艺路线版本 |
| ├─ bomId | Long | BOM ID |
| ├─ bomCode | String | BOM编码 |
| ├─ bomName | String | BOM名称 |
| ├─ bizOrgId | Long | 业务组织ID |
| ├─ bizOrgCode | String | 业务组织编码 |
| ├─ bizOrgName | String | 业务组织名称 |
| ├─ factoryId | Long | 工厂ID |
| ├─ factoryCode | String | 工厂编码 |
| ├─ factoryName | String | 工厂名称 |
| ├─ manuModel | String | 制造型号 |
| ├─ plannedQty | BigDecimal | 计划数量 |
| ├─ plannedStartTime | LocalDateTime | 计划开始时间 |
| ├─ plannedEndTime | LocalDateTime | 计划结束时间 |
| ├─ specifiedPlannedStartTime | LocalDateTime | 指定计划开始时间 |
| ├─ specifiedPlannedEndTime | LocalDateTime | 指定计划结束时间 |
| details | List<String> |  |
| ok | Boolean |  |

**响应示例**

```json
{
  "code": 123,
  "errCode": "ERRCODE_202503060001",
  "message": "message_value",
  "data": [
    {
      "id": 123,
      "code": "CODE_202503060001",
      "name": "示例name",
      "manuType": "STANDARD",
      "prodOrderId": 123,
      "materialId": 123,
      "materialCode": "MATERIALCODE_202503060001",
      "materialName": "示例materialName",
      "materialVersion": "materialVersion_value",
      "materialDrawingNumber": "materialDrawingNumber_value",
      "routingId": 123,
      "routingCode": "ROUTINGCODE_202503060001",
      "routingName": "示例routingName",
      "routingVersion": "routingVersion_value",
      "bomId": 123,
      "bomCode": "BOMCODE_202503060001",
      "bomName": "示例bomName",
      "bizOrgId": 123,
      "bizOrgCode": "BIZORGCODE_202503060001",
      "bizOrgName": "示例bizOrgName",
      "factoryId": 123,
      "factoryCode": "FACTORYCODE_202503060001",
      "factoryName": "示例factoryName",
      "manuModel": "manuModel_value",
      "plannedQty": 100.0,
      "plannedStartTime": "2026-03-06T15:52:33",
      "plannedEndTime": "2026-03-06T15:52:33",
      "specifiedPlannedStartTime": "2026-03-06T15:52:33",
      "specifiedPlannedEndTime": "2026-03-06T15:52:33"
    }
  ],
  "details": [
    "details_value"
  ],
  "ok": true
}
```

---

#### 根据生产订单ID列表获取可释放的订单信息（API专用）

**基本信息**

```
接口路径: /api/mes/v1/prodOrder/listProdOrderByIdsForRelease
请求方法: POST
接口描述: 传入生产订单id集合，返回拉平Material属性的生产订单数据，便于前端处理
```

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| object | List<Long> | 否 | 请求体对象 |

**请求示例**

```json
{
  "object": [
    123
  ]
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer |  |
| errCode | String |  |
| message | String |  |
| data | Mes_ProdOrderToReleaseApiData |  |
| ├─ prodOrderReleaseList | List<Mes_ProdOrderReleaseApiVO> | 生产订单信息集合 |
| │  ├─ id | Long | 生产订单id |
| │  ├─ code | String | 生产订单编码 |
| │  ├─ name | String | 生产订单名称 |
| │  ├─ remark | String | 备注 |
| │  ├─ securityLevel | String | 密级: /**  * 公开  */ PUBLIC("10", "公开"), /**  * 内部  */ INTERIOR("20", "内部"), /**  * 秘密  */ SECRET("30", "秘密"), /**  * 机密  */ CONFIDENTIAL("40", "机密"); |
| │  ├─ validMark | Boolean | 合法标记 |
| │  ├─ editMark | Boolean | 编辑标记 |
| │  ├─ orderType | String | 订单类型: /** * 标准生产订单 */ STANDARD("OT_010_STANDARD", "标准"),  /** * 试验生产订单 */ EXPERIMENTAL("OT_020_EXPERIMENTAL", "试验"),  /** * 返修生产订单 */ REPAIR("OT_030_REPAIR", "返修"); |
| │  ├─ materialId | Long | 物料ID |
| │  ├─ materialCode | String | 物料编码 |
| │  ├─ materialVersion | String | 物料版本 |
| │  ├─ materialName | String | 物料名称 |
| │  ├─ materialDrawingNumber | String | 物料图号 |
| │  ├─ manuModel | String | 制造型号 |
| │  ├─ unit | String | 计量单位 |
| │  ├─ plannedQty | BigDecimal | 计划数量 |
| │  ├─ currentQty | BigDecimal | 本次释放数量 |
| │  ├─ unitQty | BigDecimal | 每份数量 |
| │  ├─ economicBatch | BigDecimal | 经济批量 |
| │  ├─ plannedOutputQty | BigDecimal | 计划产出数量 |
| │  ├─ qualifiedQty | BigDecimal | 合格数量 |
| │  ├─ scrappedQty | BigDecimal | 报废数量 |
| │  ├─ releasedQty | BigDecimal | 已释放数量 |
| │  ├─ plannedStartTime | LocalDateTime | 计划开始时间 |
| │  ├─ plannedEndTime | LocalDateTime | 计划结束时间 |
| │  ├─ actualStartTime | LocalDateTime | 实际开始时间 |
| │  ├─ actualEndTime | LocalDateTime | 实际结束时间 |
| │  ├─ priority | Integer | 优先级 |
| │  ├─ planner | Mes_User |  |
| │  │  ├─ id | Long |  |
| │  │  ├─ entityType | String |  |
| │  │  ├─ code | String |  |
| │  │  ├─ name | String |  |
| │  ├─ controlStatus | String | 控制状态:          /**          * 正常          */          NORMAL("CS_010_NORMAL", "正常"),          /**          * 暂停          */          PAUSED("CS_020_PAUSED", "暂停"),           /**          * 取消          */          CANCEL("CS_030_CANCEL", "取消"); |
| │  ├─ bizOrgId | Long | 业务组织ID |
| │  ├─ bizOrgCode | String | 业务组织编码 |
| │  ├─ bizOrgName | String | 业务组织名称 |
| │  ├─ factoryId | Long | 所属工厂ID |
| │  ├─ factoryCode | String | 所属工厂编码 |
| │  ├─ factoryName | String | 所属工厂名称 |
| │  ├─ lifecycleState | String | 生命周期状态 |
| │  ├─ lifecycleTemplate | String | 生命周期模板 |
| ├─ releaseMethod | String | 释放方法, /**  * 自由分配策略  */ FREE_SPLIT_STRATEGY("freeSplitStrategy", "按自由拆分释放"),  /**  * 剩余可释放数量策略  */ REMAINING_QUANTITY_STRATEGY("remainingQuantityStrategy", "按剩余可释放数量释放"),  /**  * 释放方法  */ ECONOMIC_BATCH_QUANTITY_STRATEGY("economicBatchQuantityStrategy", "按经济批量释放"); |
| ├─ timeConstraintMethod | String | 释放约束方法: /** * 不约束 */ NO_CONSTRAINT("noConstraint", "不约束"), /** * 弱约束 */ WEEK_CONSTRAINT("weekConstraint", "弱约束"), /** * 强约束 */ STRONG_CONSTRAINT("strongConstraint", "强约束"); |
| details | List<String> |  |
| ok | Boolean |  |

**响应示例**

```json
{
  "code": 123,
  "errCode": "ERRCODE_202503060001",
  "message": "message_value",
  "data": {
    "prodOrderReleaseList": [
      {
        "id": 123,
        "code": "CODE_202503060001",
        "name": "示例name",
        "remark": "remark_value",
        "securityLevel": "securityLevel_value",
        "validMark": true,
        "editMark": true,
        "orderType": "STANDARD",
        "materialId": 123,
        "materialCode": "MATERIALCODE_202503060001",
        "materialVersion": "materialVersion_value",
        "materialName": "示例materialName",
        "materialDrawingNumber": "materialDrawingNumber_value",
        "manuModel": "manuModel_value",
        "unit": "unit_value",
        "plannedQty": 100.0,
        "currentQty": 100.0,
        "unitQty": 100.0,
        "economicBatch": 100.0,
        "plannedOutputQty": 100.0,
        "qualifiedQty": 100.0,
        "scrappedQty": 100.0,
        "releasedQty": 100.0,
        "plannedStartTime": "2026-03-06T15:52:33",
        "plannedEndTime": "2026-03-06T15:52:33",
        "actualStartTime": "2026-03-06T15:52:33",
        "actualEndTime": "2026-03-06T15:52:33",
        "priority": 123,
        "planner": {
          "id": 123,
          "entityType": "STANDARD",
          "code": "CODE_202503060001",
          "name": "示例name"
        },
        "controlStatus": "NORMAL",
        "bizOrgId": 123,
        "bizOrgCode": "BIZORGCODE_202503060001",
        "bizOrgName": "示例bizOrgName",
        "factoryId": 123,
        "factoryCode": "FACTORYCODE_202503060001",
        "factoryName": "示例factoryName",
        "lifecycleState": "lifecycleState_value",
        "lifecycleTemplate": "lifecycleTemplate_value"
      }
    ],
    "releaseMethod": "releaseMethod_value",
    "timeConstraintMethod": "2026-03-06T15:52:33"
  },
  "details": [
    "details_value"
  ],
  "ok": true
}
```

---

#### 确认释放生产订单

**基本信息**

```
接口路径: /api/mes/v1/prodOrder/confirmRelease
请求方法: POST
接口描述: 确认释放生产订单
```

**详细说明**

```
1. 校验释放数据的有效性
2. 校验释放数量的合法性
3. 校验计划时间的合理性
4. 保存释放的订单数据
5. 更新原订单状态和数量
6. 记录操作日志
```

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| object | List<Mes_ProdOrderReleaseConfirmDTO> | 否 | 请求体对象 |
| └─ id | Long | 否 | 释放得到的制造订单id |
| └─ prodOrderId | Long | 是 | 进行释放的生产订单id |
| └─ planQty | BigDecimal | 是 | 制造订单计划数量 |
| └─ planStartTime | LocalDateTime | 是 | 制造订单计划开始 |
| └─ planEndTime | LocalDateTime | 是 | 制造订单计划结束 |

**请求示例**

```json
{
  "object": [
    {
      "id": 123,
      "prodOrderId": 123,
      "planQty": 100.0,
      "planStartTime": "2026-03-06T15:52:33",
      "planEndTime": "2026-03-06T15:52:33"
    }
  ]
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer |  |
| errCode | String |  |
| message | String |  |
| data | Mes_BatchSummary |  |
| ├─ total | Integer |  |
| ├─ success | Integer |  |
| ├─ failure | Integer |  |
| ├─ successIds | List<Long> |  |
| ├─ failureIds | List<Long> |  |
| ├─ empty | Boolean |  |
| ├─ allFailure | Boolean |  |
| ├─ allSuccess | Boolean |  |
| ├─ successCount | Integer |  |
| ├─ failureCount | Integer |  |
| ├─ partialSuccess | Boolean |  |
| ├─ successRate | Double |  |
| ├─ failureRate | Double |  |
| details | List<String> |  |
| ok | Boolean |  |

**响应示例**

```json
{
  "code": 123,
  "errCode": "ERRCODE_202503060001",
  "message": "message_value",
  "data": {
    "total": 123,
    "success": 123,
    "failure": 123,
    "successIds": [
      123
    ],
    "failureIds": [
      123
    ],
    "empty": true,
    "allFailure": true,
    "allSuccess": true,
    "successCount": 123,
    "failureCount": 123,
    "partialSuccess": true,
    "successRate": 100.0,
    "failureRate": 100.0
  },
  "details": [
    "details_value"
  ],
  "ok": true
}
```

---

## Approval（审批流程）

### 审批流执行对外api接口

**服务标识：** `approval`

**资源路径：** `/api/approval/v1/flow-exec-api`

---

#### 发起流程

**基本信息**

```
接口路径: /api/approval/v1/flow-exec-api/initFlow
请求方法: POST
接口描述: 创建并启动一个新的审批流程实例
```

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| object | Approval_FlowInitCmd | 否 | 请求体对象 |
| └─ processDefKey | String | 否 |  |
| └─ bizEntityType | String | 否 |  |
| └─ bizEntityId | Long | 否 |  |
| └─ initUserId | Long | 否 |  |
| └─ appointNextAssignees | List<Long> | 否 |  |

**请求示例**

```json
{
  "object": {
    "processDefKey": "processDefKey_value",
    "bizEntityType": "STANDARD",
    "bizEntityId": 123,
    "initUserId": 123,
    "appointNextAssignees": [
      123
    ]
  }
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer |  |
| errCode | String |  |
| message | String |  |
| data | Approval_FlowInitResult |  |
| ├─ bizEntityId | Long |  |
| ├─ processInstanceId | String |  |
| ├─ repeatInitFlag | Boolean |  |
| details | List<String> |  |
| ok | Boolean |  |

**响应示例**

```json
{
  "code": 123,
  "errCode": "ERRCODE_202503060001",
  "message": "message_value",
  "data": {
    "bizEntityId": 123,
    "processInstanceId": "123456",
    "repeatInitFlag": true
  },
  "details": [
    "details_value"
  ],
  "ok": true
}
```

---

#### 取消流程

**基本信息**

```
接口路径: /api/approval/v1/flow-exec-api/cancelFlow
请求方法: POST
接口描述: 取消指定的审批流程实例
```

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| object | Approval_FlowCancelCmd | 否 | 请求体对象 |
| └─ processInstanceId | String | 否 |  |
| └─ bizEntityId | Long | 否 |  |
| └─ reason | String | 否 |  |
| └─ userId | Long | 否 |  |

**请求示例**

```json
{
  "object": {
    "processInstanceId": "123456",
    "bizEntityId": 123,
    "reason": "reason_value",
    "userId": 123
  }
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer |  |
| errCode | String |  |
| message | String |  |
| data | Object |  |
| details | List<String> |  |
| ok | Boolean |  |

**响应示例**

```json
{
  "code": 123,
  "errCode": "ERRCODE_202503060001",
  "message": "message_value",
  "data": {},
  "details": [
    "details_value"
  ],
  "ok": true
}
```

---

#### 批量发起流程

**基本信息**

```
接口路径: /api/approval/v1/flow-exec-api/batchInitFlow
请求方法: POST
接口描述: 批量创建并启动多个审批流程实例
```

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| object | List<Approval_FlowInitCmd> | 否 | 请求体对象 |
| └─ processDefKey | String | 否 |  |
| └─ bizEntityType | String | 否 |  |
| └─ bizEntityId | Long | 否 |  |
| └─ initUserId | Long | 否 |  |
| └─ appointNextAssignees | List<Long> | 否 |  |

**请求示例**

```json
{
  "object": [
    {
      "processDefKey": "processDefKey_value",
      "bizEntityType": "STANDARD",
      "bizEntityId": 123,
      "initUserId": 123,
      "appointNextAssignees": [
        123
      ]
    }
  ]
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer |  |
| errCode | String |  |
| message | String |  |
| data | List<Approval_FlowInitResult> |  |
| ├─ bizEntityId | Long |  |
| ├─ processInstanceId | String |  |
| ├─ repeatInitFlag | Boolean |  |
| details | List<String> |  |
| ok | Boolean |  |

**响应示例**

```json
{
  "code": 123,
  "errCode": "ERRCODE_202503060001",
  "message": "message_value",
  "data": [
    {
      "bizEntityId": 123,
      "processInstanceId": "123456",
      "repeatInitFlag": true
    }
  ],
  "details": [
    "details_value"
  ],
  "ok": true
}
```

---

#### 批量取消流程

**基本信息**

```
接口路径: /api/approval/v1/flow-exec-api/batchCancelFlow
请求方法: POST
接口描述: 批量取消多个审批流程实例
```

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| object | List<Approval_FlowCancelCmd> | 否 | 请求体对象 |
| └─ processInstanceId | String | 否 |  |
| └─ bizEntityId | Long | 否 |  |
| └─ reason | String | 否 |  |
| └─ userId | Long | 否 |  |

**请求示例**

```json
{
  "object": [
    {
      "processInstanceId": "123456",
      "bizEntityId": 123,
      "reason": "reason_value",
      "userId": 123
    }
  ]
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer |  |
| errCode | String |  |
| message | String |  |
| data | Object |  |
| details | List<String> |  |
| ok | Boolean |  |

**响应示例**

```json
{
  "code": 123,
  "errCode": "ERRCODE_202503060001",
  "message": "message_value",
  "data": {},
  "details": [
    "details_value"
  ],
  "ok": true
}
```

---

#### 根据业务实体类型查询关联的流程定义集合

**基本信息**

```
接口路径: /api/approval/v1/flow-exec-api/listProcessDefByBizEntityType
请求方法: GET
接口描述: 根据实体类型查询关联的流程定义，只查询有效的流程定义，按流程标识排序
```

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| bizEntityType | String | 是 |  |

**响应参数**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer |  |
| errCode | String |  |
| message | String |  |
| data | List<Approval_ProcessDefinitionInfo> |  |
| ├─ processDefKey | String |  |
| ├─ processDefName | String |  |
| ├─ processDefVersion | Integer |  |
| details | List<String> |  |
| ok | Boolean |  |

**响应示例**

```json
{
  "code": 123,
  "errCode": "ERRCODE_202503060001",
  "message": "message_value",
  "data": [
    {
      "processDefKey": "processDefKey_value",
      "processDefName": "示例processDefName",
      "processDefVersion": 123
    }
  ],
  "details": [
    "details_value"
  ],
  "ok": true
}
```

---

#### 判断实体是否加入过流程

**基本信息**

```
接口路径: /api/approval/v1/flow-exec-api/judgeJoinedFLow
请求方法: GET
接口描述: 检查指定业务实体是否曾经参与过任何审批流程
```

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| bizEntityId | Long | 是 | 业务实体ID |

**响应参数**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer |  |
| errCode | String |  |
| message | String |  |
| data | Boolean |  |
| details | List<String> |  |
| ok | Boolean |  |

**响应示例**

```json
{
  "code": 123,
  "errCode": "ERRCODE_202503060001",
  "message": "message_value",
  "data": true,
  "details": [
    "details_value"
  ],
  "ok": true
}
```

---

## 附录

### 常用数据类型定义

#### Request 包装器

```java
public class Request<T> {
    private T object;  // 业务数据对象
}
```

#### Response 包装器

```java
public class Response<T> {
    private Integer code;           // HTTP 状态码
    private String errCode;         // 业务错误码
    private String message;         // 响应消息
    private T data;                 // 业务数据
    private List<String> details;   // 详细错误信息
    private Boolean ok;             // 操作是否成功
}
```

#### BatchSummary（批量操作摘要）

```java
public class BatchSummary {
    private Integer total;              // 总数
    private Integer success;            // 成功数
    private Integer failure;            // 失败数
    private List<Long> successIds;      // 成功的ID列表
    private List<Long> failureIds;      // 失败的ID列表
    private Double successRate;         // 成功率
    private Double failureRate;         // 失败率
}
```

### 参考资源

- OpenAPI 3.0 规范：https://swagger.io/specification/
- API 文档生成配置：`km-common-apidoc` 组件
- API 文档聚合位置：`km-mom-gateway` 网关层
- 生成的 API 文档：`km-mom-gateway/src/main/resources/api-docs/kmmom-api-docs.json`

---


## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.7 | 2026-03-06 | 自动更新 API 接口清单 |
| v1.6 | 2026-03-06 | 自动更新 API 接口清单 |
| v1.5 | 2026-03-06 | 自动更新 API 接口清单 |
| v1.4 | 2026-03-06 | 自动更新 API 接口清单 |
| v1.3 | 2026-03-06 | 自动更新 API 接口清单 |
| v1.2 | 2026-03-06 | 自动更新 API 接口清单 |
| v1.1 | 2026-03-06 | 自动更新 API 接口清单 |
| v1.0 | 2026-03-06 | 自动更新 API 接口清单 |

**维护者：** KM-MOM 开发团队
