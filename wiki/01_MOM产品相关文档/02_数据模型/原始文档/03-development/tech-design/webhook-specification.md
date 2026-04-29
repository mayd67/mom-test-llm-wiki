# WebHook规范

## 规范概述

本文档定义了MOM系统中WebHook的完整规范，基于`@BizWebHook`注解属性，统一所有WebHook的命名标准，确保系统的一致性和可维护性。

### WebHook属性结构

每个WebHook定义包含以下5个核心属性：

1. **业务域（domain）** - WebHook所属的业务领域
2. **分类（category）** - 功能模块分类
3. **编码（code）** - 唯一标识符，格式：`mom.{domain}.{category}.{action}.{timing}`
4. **WebHook中文名称（name）** - 业务友好的简述
5. **描述（description）** - 详细的触发场景和用途说明

原始需求：https://uig9b1u98i3.feishu.cn/wiki/Fl9VwtEXgilvlDkkBoGcFR7tnke#share-KK5CduePiodKpXxO6rBcyATRnYg

## 完整属性规范

### 1. 业务域（domain）

业务域定义WebHook所属的业务领域，对应`@BizWebHook`注解的`domain`属性。

#### 业务域划分
| 业务域代码 | 业务域名称 | 说明 |
|------------|------------|------|
| platform | 平台管理 | 系统平台相关功能 |
| mes | 制造执行 | 生产制造相关功能 |
| aps | 高级排产 | 计划排程相关功能 |
| wms | 仓储管理 | 仓储物流相关功能 |
| ems | 设备管理 | 设备维护相关功能 |

### 2. 分类（category）

分类定义WebHook的功能模块，对应`@BizWebHook`注解的`category`属性，定位于具体的业务概念。

#### 分类规范
- 使用**snake_case**命名法（小写+下划线）
- 表达核心业务概念，如："生产订单"、"制造订单"、"制造任务"
- 避免过于技术化的命名

#### 常用分类示例
| 分类代码 | 分类名称 | 所属业务域 | 说明 |
|----------|----------|------------|------|
| prod_order | 生产订单 | mes | 生产订单相关功能 |
| manu_order | 制造订单 | mes | 制造订单相关功能 |
| manu_task | 制造任务 | mes | 制造任务相关功能 |

### 3. 编码（code）

编码是WebHook的唯一标识符，对应`@BizWebHook`注解的`code`属性。

#### 编码格式
统一使用固定前缀+业务域+分类+动作+时机的5段式结构：

```
mom.{domain}.{category}.{action}.{timing}
```

#### 编码规范

| 组成部分 | 要求 | 示例 | 是否必填 |
|----------|------|------|----------|
| mom | 固定前缀，表示MOM系统 | mom | ✅ |
| domain | 业务域代码 | mes, aps, wms, ems, platform | ✅ |
| category | 分类代码，snake_case | prod_order, manu_task | ✅ |
| action | 动作代码，snake_case | publish, schedule, complete | ✅ |
| timing | 时机标识 | before, after | ✅ |

> **说明**：尽管当前需求中的WebHook都是在业务操作完成后触发（使用`after`），但规范中保留`before`选项是为了支持未来可能的**前置通知**场景，保持规范的完整性和扩展性。

### 4. WebHook中文名称（name）

WebHook中文名称对应`@BizWebHook`注解的`name`属性，用于业务人员理解。

#### name规范
- 使用简洁明了的中文描述
- 格式：`{业务动作}{时机}`
- 避免过于技术化的术语
- 便于业务人员快速理解WebHook含义

#### name示例
| name示例 | 对应code | 说明 |
|----------|----------|------|
| 生产订单发布后事件 | mom.mes.prod_order.publish.after | 生产订单发布后触发 |
| 制造任务完工事件 | mom.mes.manu_task.complete.after | 制造任务完成后通知 |
| 生产计划排程后事件 | mom.aps.plan_management.schedule.after | 生产计划排程完成后触发 |
| 库存更新后事件 | mom.wms.inventory.update.after | 库存数据更新后触发 |

### 5. 描述（description）

描述对应`@BizWebHook`注解的`description`属性，详细说明WebHook的触发场景和用途。

#### 描述（description）
- 使用完整的句子描述
- 格式：`{业务动作}{时机}触发，用于{业务场景}`
- 说明WebHook的触发条件和用途
- 帮助开发人员理解业务背景

#### description示例
| description示例 | 对应name | 说明 |
|-----------------|----------|------|
| 生产订单发布完成后触发，用于通知下游系统开始生产准备 | 生产订单发布-后 | 说明触发时机和用途 |
| 制造任务完成后通知，用于更新生产进度和统计工时 | 制造任务完工通知 | 说明业务影响 |
| 生产计划排程完成后触发，用于下发车间执行 | 生产计划排程-后 | 说明后续业务流程 |
| 库存数据更新后触发，用于同步库存状态和预警 | 库存更新-后 | 说明数据同步场景 |

## WebHook触发位置原则

### WebHook触发位置选择

WebHook触发位置的选择应基于以下核心考虑：确保业务逻辑纯粹性、维护架构层次清晰、保证数据一致性。基于MOM系统的分层架构设计，WebHook应在**应用服务层（Application Service）**触发，而非领域服务层（Domain Service）。

### 推荐方案：应用服务层触发

**Application Service层触发WebHook的核心优势：**

1. **确保事务数据可见性**  
   应用服务层可确保WebHook在事务提交后触发，避免外部系统收到通知但无法读取到最新数据的尴尬情况。例如：订单创建WebHook发出后，外部系统查询却发现订单不存在（事务未提交）。
   
   >  - 事务控制通常在应用服务层实现，应用层可通过编程式事务（如Spring的TransactionTemplate）确保WebHook在事务提交后触发
   >  - 这种机制从根本上避免了"事务数据不可见"问题，确保外部系统收到WebHook时能够查询到最新的业务数据

2. **保持领域层业务逻辑纯粹性**  
   领域服务（Domain Service）应专注于核心业务规则实现，WebHook触发属于外部交互职责，放在应用服务层可避免领域层承担非业务职责，符合DDD分层架构原则。

3. **确保业务完整性**  
   应用服务层负责事务管理，可确保WebHook只在业务操作完全成功后触发。若领域服务触发WebHook后事务回滚，会导致外部系统收到错误通知，造成数据不一致。

4. **提升代码可测试性**  
   领域服务可独立测试核心业务逻辑，无需关注WebHook触发。WebHook触发逻辑在应用服务层单独测试，降低测试复杂度，提高测试覆盖率。

5. **降低系统耦合度**  
   将WebHook触发逻辑从领域服务中分离，减少领域层对外部系统的依赖，使核心业务逻辑更加稳定和可复用。

### 不推荐方案：领域服务层触发

**Domain Service层触发的主要问题：**

1. **事务数据可见性问题**  
   WebHook在事务中触发时，外部系统收到通知后立即查询数据，但由于事务未提交，无法读取到最新数据。例如：收到"订单创建"WebHook但查询不到订单信息，导致外部系统处理失败或重试。

2. **破坏领域层纯粹性**  
   领域服务承担外部通知职责，违反了DDD中领域层应专注于业务规则的原则，使核心业务逻辑与外部交互耦合。

3. **事务边界处理复杂**  
   WebHook触发时机难以与事务状态保持一致，可能在业务操作最终失败时已发出通知，导致外部系统数据不一致。

4. **增加测试复杂度**  
   测试领域服务时需要模拟WebHook触发逻辑，无法独立验证核心业务规则，降低了单元测试的纯粹性和有效性。

5. **提高系统耦合度**  
   领域层直接依赖WebHook机制，使核心业务逻辑与外部通知系统紧密耦合，降低了代码的可复用性和可维护性。

### 触发位置决策矩阵

| 评估维度 | Application层 | Domain层 | 说明 |
|----------|---------------|----------|------|
| 事务数据可见性 | 保证 ✅ | 问题 ❌ | Application层确保事务提交后触发，外部系统能查到最新数据 |
| 领域层纯粹性 | 保持 ✅ | 破坏 ❌ | 领域层专注业务规则，WebHook属于外部交互职责 |
| 事务一致性 | 易保证 ✅ | 难控制 ❌ | Application层控制事务边界，确保业务成功后才发通知 |
| 测试独立性 | 高 ✅ | 低 ❌ | 领域逻辑可独立测试，不受WebHook影响 |
| 系统耦合度 | 低 ✅ | 高 ❌ | 领域层不依赖外部通知机制 |
| 职责分离 | 清晰 ✅ | 混乱 ❌ | 各层职责明确，符合架构设计原则 |
| 维护成本 | 低 ✅ | 高 ❌ | 代码结构清晰，易于维护和扩展 |

## WebHook订阅规范

本章节定义WebHook消息体和订阅消费的设计原则。WebHook采用统一的消息格式，所有订阅都通过Web API接口实现。

### 消息结构格式

WebHook消息由系统自动生成完整的消息结构示例：

```json
{
  "header": {
    "createTime": "1759124777826",
    "requestId": "req_492c6e82c040",
    "userId": "10002001"
  },
  "data": {
    "items": [
      {
        "parentProdOrderId": 100,
        "childrenProdOrderIds": [1001, 1002]
      }
    ]
  }
}
```

#### 消息字段说明

**header（消息头）**

- `createTime`: 消息创建时间戳（毫秒）
- `requestId`: 唯一请求标识，用于链路追踪
- `userId`: 触发WebHook的用户ID

**data（业务数据）**

- WebHook的业务负载（Payload），结构由@BizWebHook注解的XxxxPayload类定义

### 订阅消费设计原则

WebHook设计为**单向通知机制**，具有以下核心特点：

1. **纯通知性质**：WebHook仅负责发送业务活动通知，不关注消费方的处理结果
2. **无返回处理**：无论消费方是同步还是异步处理，WebHook都不处理返回结果
3. **业务独立性**：业务活动的执行不受WebHook订阅消费是否成功的影响，确保核心业务流程的稳定性
4. **日志记录**：系统会记录消费方的响应日志，用于监控、问题排查和失败重试
5. **Web API订阅**：所有WebHook订阅都通过Web API接口实现

这种设计确保了WebHook的简洁性和可靠性，避免了复杂的双向依赖，使系统保持松耦合架构。业务系统可以独立运行，即使WebHook消费失败也不会影响正常的业务流程。

## 完整示例

以下示例展示`@BizWebHook`注解所有属性的完整规范：

| domain | category | code | name | description | 说明 |
|--------|----------|------|------|-------------|------|
| mes | prod_order | mom.mes.prod_order.publish.after | 生产订单发布-后 | 生产订单发布完成后触发，用于通知下游系统开始生产准备 | 标准生产订单发布场景 |
| mes | manu_task | mom.mes.manu_task.complete.after | 制造任务完工通知 | 制造任务完成后通知，用于更新生产进度和统计工时 | 制造任务完工场景 |
| aps | plan | mom.aps.plan.schedule.after | 生产计划排程-后 | 生产计划排程完成后触发，用于下发车间执行 | 计划排程完成场景 |
| ems | equipment | mom.ems.equipment.maintain.before | 设备维护-前 | 设备维护操作前触发，用于检查设备状态和准备维护资源 | 设备维护前检查场景 |

## 命名规范

### 模块标识
| 系统代码 | 系统名称 |
|----------|----------|
| mes | 制造执行 |
| wms | 仓储管理 |
| ems | 设备管理 |
| aps | 高级排产 |
| tms | 工装管理 |

### 实体命名
- 使用**snake_case**命名法（小写+下划线）
- 优先使用系统中已有的实体名称

**常用实体示例**：

- `prod_order` - 生产订单
- `manu_order` - 制造订单
- `inventory` - 库存

### 动作命名
- 使用**snake_case**命名法（小写+下划线）
- 使用动词或动宾结构
- 保持语义清晰、简洁

**常用动作示例**：
- `insert` - 新增
- `update` - 更新
- `delete` - 删除
- `publish` - 发布
- `expand` - 展开
- `schedule` - 排产
- `sync` - 同步
- `calc` - 计算
- `receive` - 接收

### 时机标识
- 仅使用 `before` 或 `after`
- 表示业务操作的触发时机
- `before`：业务操作执行前触发
- `after`：业务操作执行后触发

## 完整属性检查清单

在定义新的WebHook时，请检查所有`@BizWebHook`注解属性：

#### 业务域（domain）
- [ ] 是否使用标准业务域：platform/mes/aps/wms/ems
- [ ] 是否正确反映业务归属

#### 分类（category）
- [ ] 是否表达核心业务概念（如"生产订单"、"制造任务"）
- [ ] 是否使用snake_case命名
- [ ] 是否避免技术化术语

#### 编码（code）
- [ ] 是否以mom开头
- [ ] 是否遵循5段式：mom.{domain}.{category}.{action}.{timing}
- [ ] domain是否与注解domain属性一致
- [ ] category是否与注解category属性一致

#### WebHook中文名称（name）
- [ ] 是否使用简洁中文描述
- [ ] 格式是否为：{业务动作}{时机}
- [ ] 是否便于业务人员理解

#### 描述（description）
- [ ] 是否完整描述触发场景
- [ ] 格式是否为：{业务动作}{时机}触发，用于{业务场景}
- [ ] 是否说明用途和业务价值

## 最佳实践

本章节以**生产订单一级工艺展开WebHook**为例，展示如何按照本规范设计和实现WebHook。

### 案例背景

大型离散制造企业常面临多厂协同生产难题：因MBOM层级简化，无法直接拆解出各厂生产计划，导致企业级计划员难以统筹整体进度。MOM系统通过“一级工艺展开”功能，基于厂际间流水将企业级交付订单展开为各制造厂子级订单，实现多厂计划统一协调。

### 完整实现示例

#### 1. WebHook定义（Payload类）

```java
@BizWebHook(
    code = ProdOrderPrimaryExpandAfterPayload.HOOK_CODE,
    name = "生产订单一级工艺展开后通知",
    domain = "mes",
    category = "prod_order",
    description = "生产订单一级工艺展开完成后触发，用于通知订阅方处理子订单相关业务，如工艺路线匹配、备料清单生成等"
)
public class ProdOrderPrimaryExpandAfterPayload {
    //编码
    public static final String HOOK_CODE="mom.mes.prod_order.expand.after";
    /**
     * 生产订单展开项集合
     */
    List<ProdOrderPrimaryExpandedItem> items;
}

/**
 * 生产订单展开项
 */
public class ProdOrderPrimaryExpandedItem {
    /**
     * 父生产订单id
     */
    Long parentProdOrderId;
    /**
     * 展开后的子订单集合
     */
    List<Long> childrenProdOrderIds;
}
```

#### 2. 业务触发实现（应用服务层）

```java
/**
 * 一级工艺展开
 */
public Result<BatchSummary> primaryRoutingExpand(List<Long> prodOrderIds) {
    if (CollectionUtil.isEmpty(prodOrderIds)) {
        return Result.success(new BatchSummary());
    }
    
    // 编程式事务，调用领域服务完成业务活动
    ProdOrderExpandResult expandResult = transactionTemplate.execute(status -> {
        // 调用领域服务进行展开
        return prodOrderPrExpandService.expand(prodOrderIds);
    });

    // 事务提交后（保证事务可见性），发布生产订单一级工艺展开 WebHook
    publishProdOrderExpandWebHook(expandResult.getItems());

    return expandResult.getSummary();
}
/**
 * 执行发布生产订单一级工艺展开WebHook
 */
private void publishProdOrderExpandWebHook(List<ProdOrderPrimaryExpandedItem> items) {
    if (CollectionUtil.isEmpty(items)) {
        return;
    }
    //构建payload
    ProdOrderPrimaryExpandAfterPayload payload = new ProdOrderPrimaryExpandAfterPayload();
    payload.setItems(items);
    //使用WebHookTrigger Bean,触发webhook
    webHookTrigger.trigger(ProdOrderPrimaryExpandAfterPayload.HOOK_CODE, payload);
}
```

### 设计要点说明

#### 1. 为什么采用这样的Payload结构？

本案例中的Payload设计充分考虑了业务特性：

- **父子订单关系**：生产订单展开操作会创建父子订单的关联关系，需要同时通知父订单和对应的子订单集合
- **批量处理**：支持一次展开多个生产订单，每个订单可能有多个子订单
- **数据结构清晰**：使用`ProdOrderPrimaryExpandedItem`封装单个订单的展开结果，便于订阅方消费处理

这种设计确保了订阅方能够准确理解订单展开后的完整关联关系。

#### 2. 规范符合性分析

| 规范要求 | 实现情况 | 说明 |
|----------|----------|------|
| **编码格式** | ✅ 符合 | `mom.mes.prod_order.expand.after` 遵循5段式结构 |
| **业务域** | ✅ 符合 | 使用`mes`（制造执行）正确反映业务归属 |
| **分类命名** | ✅ 符合 | `prod_order`使用snake_case，表达核心业务概念 |
| **动作语义** | ✅ 符合 | `expand`准确表达展开业务动作 |
| **触发时机** | ✅ 符合 | `after`确保操作完成后触发 |
| **中文名称** | ✅ 符合 | `生产订单一级工艺展开后`简洁明了 |
| **描述完整** | ✅ 符合 | 完整描述触发场景和业务用途 |

#### 3. 架构设计亮点

- **应用服务层触发**：确保事务提交后发布WebHook，保证数据一致性
- **编程式事务控制**：使用`TransactionTemplate`精确控制触发时机
- **单向通知机制**：WebHook仅负责通知，不处理消费方响应
- **领域层纯粹性**：核心业务逻辑与外部通知职责分离

### 使用建议

此最佳实践适用于以下场景：

1. **需要通知下游系统业务数据变更**的场景
2. **涉及多实体关联关系变更**的复杂业务操作
3. **对数据一致性要求较高**的核心业务流程
4. **需要批量处理**的业务操作

参考此实现时，请根据具体业务需求调整Payload结构，但保持相同的架构设计原则和规范符合性。

---

### 通用最佳实践原则

1. **保持简洁**：编码应该简洁明了，避免过长的名称
2. **语义清晰**：通过编码就能理解业务场景
3. **一致性**：相同类型的业务使用相同的命名模式
4. **可扩展**：为未来可能的扩展预留空间
5. **文档化**：为新定义的Hook编码添加详细说明

## 优势

- **系统标识统一**：mom前缀明确表示MOM系统WebHook
- **结构统一**：所有WebHook遵循相同的5段式结构
- **语义清晰**：通过业务领域、分类、动作、时机准确表达业务含义
- **业务导向**：业务领域和分类更符合业务思维，降低技术理解成本
- **易于理解**：命名规范直观，降低跨团队沟通成本
- **维护简单**：统一的格式便于管理和维护
- **扩展性好**：支持未来业务扩展和新业务领域接入

## 版本记录

| 版本 | 日期 | 变更内容 | 备注 |
|------|------|----------|------|
| v2.0 | 2025-11 | 统一5段式结构 | 废弃4段式，统一使用mom.业务领域.分类.动作.时机 |
| v1.0 | 2025-11 | 初始版本 | 建立基础规范 |

---

**注意**：本规范自发布之日起生效，所有新开发的WebHook必须遵循此规范。对于已有的WebHook编码，建议在后续版本迭代中逐步迁移到新的规范。