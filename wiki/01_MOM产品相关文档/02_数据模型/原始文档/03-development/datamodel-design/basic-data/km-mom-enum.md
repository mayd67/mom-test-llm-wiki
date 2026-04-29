# 枚举定义文档

## 文档说明

**基本信息**
- 文档版本:v1.10 | 更新日期:2026-04-08 | 维护团队:产品研发团队
- 目标受众:产品研发团队

**文档定位**

本文档集中定义KMMOM3.x系统中所有枚举类型,作为数据模型设计的统一枚举值引用源,确保枚举定义的一致性和可维护性。数据模型属性定义时,在说明列中引用枚举编码即可(格式:`引用枚举:枚举编码`),无需重复罗列枚举值。

---

## 一、Platform模块枚举

### 用户状态(UserState)

**枚举编码:** `UserState` | **枚举说明:** 用户账号的状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| INACTIVE | 未激活 | 用户账号已创建但未激活 |
| ACTIVE | 正常 | 用户账号正常可用 |
| DISABLED | 已禁用 | 用户账号被管理员禁用 |
| DELETED | 已注销 | 用户账号已注销 |

---

### 用户性别(Sex)

**枚举编码:** `Sex` | **枚举说明:** 用户性别

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| M | 男 | 男性 |
| F | 女 | 女性 |

---

### 在职状态(EmployedStatus)

**枚举编码:** `EmployedStatus` | **枚举说明:** 用户在职状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| EMPLOYED | 在职 | 员工在职 |
| TERMINATED | 离职 | 员工已离职 |
| REHIRED | 返聘 | 离职后返聘 |

---

### 在岗状态(DutyStatus)

**枚举编码:** `DutyStatus` | **枚举说明:** 用户在岗状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| WORK | 在岗 | 员工在岗工作 |
| LEAVE | 脱岗 | 员工临时脱岗(请假、出差等) |

---

### 用户类型(UserType)

**枚举编码:** `UserType` | **枚举说明:** 用户账号类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| SUPER | 超级管理员 | 系统超级管理员 |
| TRIAD | 三员管理 | 三员管理人员(安全员、审计员、系统管理员) |
| USER | 普通用户 | 普通业务用户 |

---

### 用户密级(personLevel)

**枚举编码:** `personLevel` | **枚举说明:** 用户账号的密级

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 10 | 一般 | 普通密级用户 |
| 20 | 重要 | 重要密级用户 |
| 30 | 核心 | 核心密级用户 |

---

### 角色类型(RoleType)

**枚举编码:** `RoleType` | **枚举说明:** 角色类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| SUPER | 超级管理员 | 超级管理员角色 |
| TRIAD | 三员管理员 | 三员管理角色 |
| USER | 普通用户 | 普通用户角色 |

---

### 角色状态(RoleState)

**枚举编码:** `RoleState` | **枚举说明:** 角色状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ACTIVE | 正常 | 角色正常可用 |
| DISABLED | 已禁用 | 角色被禁用 |

---

### 终端类型(terminalType)

**枚举编码:** `terminalType` | **枚举说明:** 功能权限适用的终端类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PC | PC | PC端 |
| APP | 移动端 | 移动端APP |

---

### 数据权限范围(scope)

**枚举编码:** `scope` | **枚举说明:** 数据权限范围

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ALL | 全部 | 全部数据 |
| ORG | 本部门 | 仅本部门数据 |
| ORG_BELOW | 本部门及以下 | 本部门及下级部门数据 |
| CUSTOMIZE | 自定义 | 自定义范围 |

---

### 行政组织类型(OrgType)

**枚举编码:** `OrgType` | **枚举说明:** 行政组织类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 10 | 公司 | 公司级组织 |
| 20 | 工厂 | 工厂级组织 |
| 30 | 部门 | 部门级组织 |

---

### 业务组织类型(BizOrgType)

**枚举编码:** `BizOrgType` | **枚举说明:** 业务组织类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 10 | 公司 | 公司级业务组织 |
| 20 | 工厂 | 工厂级业务组织 |
| 30 | 车间 | 车间级业务组织 |
| 40 | 工段 | 工段级业务组织 |
| 50 | 班组 | 班组级业务组织 |
| 110 | 供应商 | 供应商组织 |

---

### 功能类型(FeatureType)

**枚举编码:** `featureType` | **枚举说明:** 系统功能类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| MENU | 导航 | 导航菜单 |
| BUTTON | 按钮 | 功能按钮 |
| EXTENSION_BUTTON | 扩展按钮 | 扩展功能按钮 |

---

### 功能范围(FeatureScope)

**枚举编码:** `featureScope` | **枚举说明:** 功能所属范围

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| SYS | 管理 | 系统管理功能 |
| BIZ | 业务 | 业务功能 |

---

### 链接类型(LinkType)

**枚举编码:** `linkType` | **枚举说明:** 功能链接类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ROUTE | 路由 | 系统内路由 |
| URL | 外部链接 | 外部URL链接 |

---

### 打开方式(LinkTarget)

**枚举编码:** `linkTarget` | **枚举说明:** 功能链接打开方式

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| INTERNAL | 系统内 | 在系统内打开 |
| NEWTAB | 新标签 | 在新标签页打开 |

---

### 所属站点(Site)

**枚举编码:** `site` | **枚举说明:** 功能所属的站点

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| MANAGEMENT_PLATFORM | 管理平台 | 管理平台站点 |
| WORKBENCH | 工作台 | 工作台站点 |

---

### 码段类型(SegmentType)

**枚举编码:** `SegmentType` | **枚举说明:** 编码规则的码段类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| T001 | 固定值 | 固定字符串 |
| T002 | 日期时间 | 日期时间格式 |
| T003 | 流水号 | 自增流水号 |
| T004 | 占位符 | 动态占位符 |

---

### 日期格式(DateFormat)

**枚举编码:** `DateFormat` | **枚举说明:** 编码规则中的日期格式

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| D001 | 年 | yyyy |
| D002 | 年月 | yyyyMM |
| D003 | 年月日 | yyyyMMdd |
| D004 | 年月日时分秒 | yyyyMMddHHmmss |

---

### 服务端脚本分类(ServerSideScriptCategory)

**枚举编码:** `serverSideScriptCategory` | **枚举说明:** 服务端脚本分类

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| BarcodeParse | 条码解析 | 物料条码解析脚本 |
| EncodeBuild | 编码生成 | 编码生成脚本 |
| StdEventSub | 标准事件订阅 | 标准事件订阅处理脚本 |

---

### WebHook请求方式(WebHookMethod)

**枚举编码:** `webHookMethod` | **枚举说明:** WebHook的HTTP请求方式

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| POST | POST | 固定为POST方式 |

---

### WebHook执行模式(WebHookMode)

**枚举编码:** `webHookMode` | **枚举说明:** WebHook执行模式

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| SYNC | 同步 | 同步执行 |
| ASYNC | 异步 | 异步执行 |

---

### 配置包类型(PackageType)

**枚举编码:** `packageType` | **枚举说明:** 配置包导出类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PRODUCT | 产品包 | 标准产品配置包 |
| PROJECT | 项目包 | 项目定制配置包 |

---

### 物料制造类型(ManufactureType)

**枚举编码:** `ManufactureType` | **枚举说明:** 物料的制造类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 10 | 自制件 | 自行生产制造 |
| 20 | 外购件 | 外部采购 |
| 30 | 自制+外购 | 既可自制也可外购 |

---

### 物料特性分类(FeatureCategory)

**枚举编码:** `FeatureCategory` | **枚举说明:** 物料特性分类

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 10 | 重要件 | 重要物料 |
| 20 | 关键件 | 关键物料 |
| 30 | 一般件 | 一般物料 |

---

### 物料阶段(MaterialStage)

**枚举编码:** `MaterialStage` | **枚举说明:** 物料所处的研发阶段

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| C | C | C阶段 |
| S | S | S阶段 |
| D | D | D阶段 |
| P | P | P阶段 |

---

### 物料分类(MaterialCategory)

**枚举编码:** `MaterialCategory` | **枚举说明:** 物料大类分类

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| MC_10 | 物料 | 普通物料 |
| MC_20 | 工装工具 | 工装工具类物料 |

---

### 管理方式(ManagementMethod)

**枚举编码:** `managementMethod` | **枚举说明:** 物料/工装的管理方式

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| SINGLE | 单件管理 | 按单件进行管理 |
| BATCH | 批次管理 | 按批次进行管理 |

---

### 工序类型(ProcessType)

**枚举编码:** `ProcessType` | **枚举说明:** 工序类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PROCESS | 加工 | 加工工序 |
| CHECKOUT | 检验 | 检验工序 |
| OUTER_FAC_TRANSFER | 厂际转工 | 厂际转工工序 |
| INNER_FAC_TRANSFER | 厂内转工 | 厂内转工工序 |
| OUTSOURCING | 外委 | 外委加工工序 |

---

### 工艺类型(RoutingType)

**枚举编码:** `RoutingType` | **枚举说明:** 工艺路线类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| FORMAL | 正式工艺 | 正式工艺路线 |
| TYPICAL | 典型工艺 | 典型工艺路线 |
| TEMPORARY | 临时工艺 | 临时工艺路线 |
| PRIMARY | 一级工艺 | 一级工艺路线 |
| REWORK | 返工工艺 | 返工工艺路线 |
| REPAIR | 返修工艺 | 返修工艺路线 |

---

### 工艺专业(ProcessSpecialty)

**枚举编码:** `ProcessSpecialty` | **枚举说明:** 工艺专业分类

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PS100 | 机加 | 机械加工专业 |
| PS200 | 装配 | 装配专业 |
| PS300 | 热表 | 热处理表面处理专业 |
| PS400 | 铸造 | 铸造专业 |
| PS500 | 钣焊 | 钣金焊接专业 |
| PS600 | 锻造 | 锻造专业 |
| PS700 | 通用 | 通用专业 |

---

### 工序接续方式(continuationType)

**枚举编码:** `continuationType` | **枚举说明:** 工序之间的接续方式

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ES | ES | 结束-开始关系 |
| SSEE | SSEE | 同步开始-同步结束关系 |
| none | 无 | 无接续关系 |

---

### 工作中心类型(WorkCenterType)

**枚举编码:** `WorkCenterType` | **枚举说明:** 工作中心类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| CX | 产线 | 生产线 |
| SB | 设备组 | 设备 |
| RY | 人员组 | 个人 |
| WW | 外委 | 外委单位 |
| ZZ | 组织 | 组织 |

---

### 工作中心分类(WorkCenterCategory)

**枚举编码:** `WorkCenterCategory` | **枚举说明:** 工作中心分类

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| INSPECT | 检验 | 检验工作中心 |
| PROCESS | 加工 | 加工工作中心 |
| ASSEMBLE | 装配 | 装配工作中心 |
| GENERAL | 通用生产 | 通用生产工作中心 |

---

### 资质(qualification)

**枚举编码:** `qualification` | **枚举说明:** 人员资质等级

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 10 | 钳工 | 钳工资质 |
| 20 | 车工 | 车工资质 |
| 30 | 焊工 | 焊工资质 |

---

### 库房类型(WarehouseType)

**枚举编码:** `WarehouseType` | **枚举说明:** 库房类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| WT_010_ERP | ERP一级库 | ERP一级库房 |
| WT_020_ERP | ERP二级库 | ERP二级库房 |
| WT_030_WORKCENTER | 车间二级库 | 车间二级库房 |
| WT_040_EQUIPMENT | 设备备件库 | 设备备件库房 |
| WT_050_TOOLING | 工装备件库 | 工装备件库房 |

---

### 设备模板类型(equipTepmlateType)

**枚举编码:** `equipTemplateType` | **枚举说明:** 设备主数据的模板分类

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ETT_010_MAINTENANCE | 维护 | 维护维度模板 |
| ETT_020_INSPECTION | 点检 | 点检维度模板 |

---

### 设备计划结论(equipPlanConclusion)

**枚举编码:** `equipPlanConclusion` | **枚举说明:** 设备计划的执行结论

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| EPC_10_PASS | 通过 | 计划执行通过 |
| EPC_20_REJECT | 不通过 | 计划执行未通过 |

---

### 图片文件组类型(ImageFileGroupType)

**枚举编码:** `imageFileGroupType` | **枚举说明:** 图片文件组类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 10 | 图片 | 图片文件 |
| 20 | 视频 | 视频文件 |

---

### 日志类型(LogType)

**枚举编码:** `logType` | **枚举说明:** 系统日志类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 10 | 安全日志 | 安全相关日志 |
| 20 | 文档日志 | 文档操作日志 |
| 30 | 操作日志 | 一般操作日志 |
| 40 | 系统日志 | 系统日志 |
| 50 | 标准事件消费 | 标准事件消费日志 |
| 60 | 标准事件消费重试 | 标准事件消费重试日志 |

---

### 审计意见(AuditResult)

**枚举编码:** `auditResult` | **枚举说明:** 审计意见

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 10 | 通过 | 审计通过 |
| 20 | 不通过 | 审计不通过 |

---

### 审计状态(AuditStatus)

**枚举编码:** `auditStatus` | **枚举说明:** 审计状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 0 | 待审计 | 待审计 |
| 1 | 已审计 | 已审计 |

---

### 重试执行状态(RetryTraceState)

**枚举编码:** `retryTraceState` | **枚举说明:** 事件消费重试执行状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| RETRY_10_NONE | 无须重试 | 无须重试 |
| RETRY_20_WAIT | 待重试 | 待重试 |
| RETRY_30_FAIL | 重试失败 | 重试失败 |
| RETRY_40_SUCCESS | 重试成功 | 重试成功 |
| RETRY_50_CLOSE | 关闭重试 | 关闭重试 |

---

### 简单活动业务状态(SimpleActivityBizStatus)

**枚举编码:** `SimpleActivityBizStatus` | **枚举说明:** 初始、已开始、已完成

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| CBS_010_INITIAL | 初始 | 计划已创建 |
| CBS_030_STARTED | 已开始 | 计划已开始执行 |
| CBS_040_COMPLETED | 已完成 | 计划已完成 |

---

### 安全等级(securityLevel)

**枚举编码:** `securityLevel` | **枚举说明:** 用户账号的安全等级

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 10 | 公开 | 公开级别 |
| 20 | 内部 | 内部级别 |
| 30 | 秘密 | 秘密级别 |
| 40 | 机密 | 机密级别 |

---

### 配置展示类型(showType)

**枚举编码:** `showType` | **枚举说明:** 配置项在系统中的展示类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| item | 项目 | 单个项目展示 |
| group | 组 | 分组展示 |

---

### 组件类型(compType)

**枚举编码:** `compType` | **枚举说明:** 系统前端组件的分类

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| TEXT | 文本 | 文本类组件 |
| NUM | 数值 | 数值类组件 |

---

### 功能动作类型(FeatureActionType)

**枚举编码:** `FeatureActionType` | **枚举说明:** 物料特性变更的动作类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PRODUCT_TAB | 产品内Tab | 产品内Tab展示 |
| BROWSER_TAB | 浏览器Tab | 浏览器Tab展示 |
| MODAL | Modal | Modal弹窗展示 |

---

### 用户布局分享范围(UserLayoutSharingScope)

**枚举编码:** `UserLayoutSharingScope` | **枚举说明:** 用户个性化布局的分享权限范围

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| USER | 指定用户 | 分享给指定用户 |
| ORG | 指定组织 | 分享给指定组织 |
| ROLE | 指定角色 | 分享给指定角色 |
| ALL | 全体用户 | 分享给全体用户 |

---

### 计量单位(measureUnit)

**枚举编码:** `measureUnit` | **枚举说明:** 物料、产品等的计量单位

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PCS | 个 | 件数计量 |

---

### 锁定状态(lockState)

**枚举编码:** `lockState` | **枚举说明:** 资源或任务的锁定状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| UNLOCKED | 未锁定 | 未锁定状态 |
| RESOURCE_LOCKED | 资源锁定 | 资源被锁定 |
| RESOURCE_TIME_LOCKED | 资源时间锁定 | 资源和时间被锁定 |

---

### 工装类别(toolingType)

**枚举编码:** `toolingType` | **枚举说明:** 工装、夹具的分类方式

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| TT_010_SPECIAL_TOOL | 专用工装 | 专用工装 |
| TT_020_COMMON_TOOL | 通用工具 | 通用工具 |

---

### 生命周期阶段(lifecycleStateType)

**枚举编码:** `lifecycleStateType` | **枚举说明:** 业务对象的生命周期阶段划分

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| CREATE | 创建 | 创建阶段 |
| ACTIVE | 活动 | 活动阶段 |
| RELEASE | 发布 | 发布阶段 |
| OBSOLETE | 废弃 | 废弃阶段 |

---

### 通用活动业务状态(CommonActivityBizStatus)

**枚举编码:** `CommonActivityBizStatus` | **枚举说明:** 通用业务活动的生命周期状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| CBS_010_INITIAL | 初始 | 活动已创建 |
| CBS_020_DISPATCHED | 已分派 | 活动已分派 |
| CBS_030_STARTED | 已开始 | 活动已开始执行 |
| CBS_040_COMPLETED | 已完成 | 活动已完成 |

---

### 工厂类型(factoryType)

**枚举编码:** `factoryType` | **枚举说明:** 工厂组织的专业类型分类

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| MACHINING | 机械加工专业 | 机械加工工厂 |
| ASSEMBLY | 装配专业 | 装配工厂 |

---

## 二、WMS模块枚举

### 入库方式(IN_STORE_TYPE)

**枚举编码:** `IN_STORE_TYPE` | **枚举说明:** 入库方式

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| RAW_MTL_IN | 原料调拨入库 | 原料调拨入库 |
| SURPLUS_IN | 余料入库 | 余料入库 |
| FG_COMP_IN | 成品完工入库 | 成品完工入库 |
| SUB_SCRAP_IN | 子件报废入库 | 子件报废入库 |
| FG_SCRAP_IN | 成品报废入库 | 成品报废入库 |
| PRODUCTION_RETURN | 生产退料 | 生产退料 |

---

### 出库方式(OUT_STORE_TYPE)

**枚举编码:** `OUT_STORE_TYPE` | **枚举说明:** 出库方式

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PRM_OUT | 原料生产领用出库 | 原料生产领用出库 |
| EXP_RM_RET | 原料过期退料出库 | 原料过期退料出库 |
| SCRAP_RM_OUT | 原料报废出库 | 原料报废出库 |
| FG_TRANS_OUT | 成品调拨出库 | 成品调拨出库 |
| SPARE_PART_OUT | 备件出库 | 备件出库 |
| TSR_OUT | 临时出库 | 临时出库 |

---

### 入库申请单业务状态(InStoreApplyBillBizStatus)

**枚举编码:** `InStoreApplyBillBizStatus` | **枚举说明:** 入库申请单业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| INS_010_NO | 待入库 | 待入库状态 |
| INS_020_PART | 部分入库 | 部分入库状态 |
| INS_030_ALL | 全部入库 | 全部入库状态 |

---

### 出库申请单业务状态(OutStoreApplyBillBizStatus)

**枚举编码:** `OutStoreApplyBillBizStatus` | **枚举说明:** 出库申请单业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| OUTS_010_NO | 待出库 | 待出库状态 |
| OUTS_020_PART | 部分出库 | 部分出库状态 |
| OUTS_030_ALL | 全部出库 | 全部出库状态 |

---

### 盘点单业务状态(StoreCountBillBizStatus)

**枚举编码:** `StoreCountBillBizStatus` | **枚举说明:** 盘点单业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| SCB_010_TO_CHECK | 待盘点 | 待盘点状态 |
| SCB_020_POSTED | 已过账 | 已过账状态 |

---

### 库存业务状态(InventoryBizStatus)

**枚举编码:** `InventoryBizStatus` | **枚举说明:** 库存业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| STOCK_010_QUALIFIED | 合格 | 合格状态 |
| STOCK_020_UNQUALIFIED | 不合格 | 不合格状态 |
| STOCK_030_SCRAPPED | 报废 | 报废状态 |

---

### 入库状态(InStorageStatus)

**枚举编码:** `InStorageStatus` | **枚举说明:** WMS模块物料入库的状态机

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PENDING | 待入库 | 等待入库处理 |
| IN_STORAGE | 已入库 | 已完成入库 |

---

### 物流位置类型(LogisticsLocationType)

**枚举编码:** `LogisticsLocationType` | **枚举说明:** WMS物流场景下通用位置主数据的类型划分

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 010_WAREHOUSE_LOCATION | 库房位置 | 用于标识库房、库区、库位等仓储物流位置 |
| 020_WORKBENCH_LOCATION | 工作台位置 | 用于标识工位、工作台等作业位置 |
| 030_PROCESS_LOCATION | 工序位置 | 用于标识工序流转中的中间位置 |
| 040_DROPOFF_AREA | 下货区域 | 用于标识物料下货、暂放、交接区域 |
| 050_OTHER | 其他位置 | 其他未归类的物流位置 |

---

### 物流任务类型(LogisticsTaskType)

**枚举编码:** `LogisticsTaskType` | **枚举说明:** WMS物流任务的业务类型划分

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 010_DELIVERY_TRANSFER | 发料周转 | 物料完成出库后，从库房向线边、工位、设备或工作中心到货位置移动的物流任务 |
| 020_RETURN_TRANSFER | 退料周转 | 将剩余物料、退回物料送回指定位置的物流任务 |
| 030_PROCESS_TRANSFER | 工序间周转 | 工序之间进行物料转运的物流任务 |
| 040_IN_STORE_TRANSFER | 入库周转 | 物料加工完成后，向指定入库位置或库房回运的物流任务 |
| 050_TEMPORARY_TRANSFER | 临时周转 | 临时发起的物料转运任务 |
| 060_EMPTY_CART_CALL | 空车呼叫 | 请求空车到达指定位置的物流任务 |

---

### 物流任务状态(LogisticsTaskStatus)

**枚举编码:** `LogisticsTaskStatus` | **枚举说明:** WMS物流任务的业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 010_PENDING_RECEIVE | 待接收 | 物流任务已创建，等待执行人接收 |
| 020_RECEIVED | 已接收 | 物流任务已被执行人接收 |
| 030_COMPLETED | 已完成 | 物流任务已执行完成 |

---

## 三、EMS模块枚举

### 设备类型-EMS(EquipType)

**枚举编码:** `EquipType` | **枚举说明:** 设备类型(EMS模块定义,用于设备台账)

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ET_010_PRODUCTION | 生产设备 | 生产设备 |
| ET_020_INSTRUMENT | 仪器设备 | 仪器设备 |
| ET_030_SPECIAL | 特种设备 | 特种设备 |
| ET_040_VEHICLE | 生产车辆 | 生产车辆 |

---

### 故障类型(FaultType)

**枚举编码:** `FaultType` | **枚举说明:** 设备故障类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| FT_010_MECHANICAL | 机械 | 机械故障 |
| FT_020_ELECTRICAL | 电气 | 电气故障 |
| FT_030_HYDRAULIC | 液压 | 液压故障 |
| FT_040_SOFTWARE | 软件 | 软件故障 |
| FT_050_OTHER | 其他 | 其他故障 |

---

### 严重程度(Severity)

**枚举编码:** `Severity` | **枚举说明:** 故障严重程度

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| SV_010_MINOR | 轻微 | 轻微故障 |
| SV_020_NORMAL | 一般 | 一般故障 |
| SV_030_MAJOR | 严重 | 严重故障 |
| SV_040_URGENT | 紧急 | 紧急故障 |

---

### 点检结论类型(InspectionConclusionType)

**枚举编码:** `InspectionConclusionType` | **枚举说明:** 点检项的结论类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| DT_010_NORMAL_ABNORMAL | 正常/异常 | 二选一判定 |
| DT_020_NUMERIC | 数值 | 记录数值 |
| DT_030_TEXT | 文本 | 记录文本 |

---

### 设备维护类型(MaintenanceType)

**枚举编码:** `MaintenanceType` | **枚举说明:** 设备维护类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| MT_010_PREVENTIVE | 预防性 | 预防性维护 |
| MT_020_PREDICTIVE | 预测性 | 预测性维护 |
| MT_030_EMERGENCY | 应急 | 应急维护 |

---

### 技能要求(SkillRequirement)

**枚举编码:** `SkillRequirement` | **枚举说明:** 维护项目技能要求

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| SR_010_JUNIOR | 初级 | 初级技能 |
| SR_020_MIDDLE | 中级 | 中级技能 |
| SR_030_SENIOR | 高级 | 高级技能 |

---

### 设备点检项结果(EquipCheckResult)

**枚举编码:** `EquipCheckResult` | **枚举说明:** 设备点检项结果

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| IR_010_NORMAL | 正常 | 维护正常 |
| IR_020_ABNORMAL | 异常 | 维护发现异常 |

---

### 备件更换类型(PartRelaceType)

**枚举编码:** `PartRelaceType` | **枚举说明:** 备件更换记录关联的业务类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| RBT_010_MAINTENANCE | 设备维保 | 设备维保业务 |
| RBT_020_FAULT | 设备故障 | 设备故障业务 |
| RBT_030_TOOLING_MAINT | 工装保养 | 工装保养业务 |
| RBT_040_TOOLING_REPAIR | 工装维修 | 工装维修业务 |

---

### 设备台账业务状态(EquipLedgerBizStatus)

**枚举编码:** `EquipLedgerBizStatus` | **枚举说明:** 设备台账的业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| CBS_RS_010_RUNNING | 在用 | 设备正常运行中 |
| CBS_RS_020_STOPPED | 停机 | 设备临时停机 |
| CBS_RS_030_MAINTENANCE | 维护中 | 设备正在进行维护保养 |
| CBS_RS_040_FAULT | 故障 | 设备发生故障 |
| CBS_RS_050_SCRAPPED | 报废 | 设备已报废 |

---

### 设备故障单业务状态(EquipFaultBizStatus)

**枚举编码:** `EquipFaultBizStatus` | **枚举说明:** 设备故障单的业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PS_010_CREATED | 待处理 | 故障单已创建,等待处理 |
| PS_020_COMPLETED | 待验证 | 故障已处理完成,待验证 |
| PS_030_CLOSED | 已完成 | 故障单已关闭 |

---

## 七、TMS模块枚举

### 工装策略类型(strategyType)

**枚举编码:** `strategyType` | **枚举说明:** 工装策略类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| TIME | 时间周期 | 时间周期策略 |
| FREQUENCY | 次数周期 | 次数周期策略 |


---

### 共享状态(shareState)

**枚举编码:** `shareState` | **枚举说明:** 共享状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| SS_10_INIT | 未共享 | 未共享状态 |
| SS_20_PREPARING | 待共享 | 待共享状态 |
| SS_30_SHARED | 已共享 | 已共享状态 |

---

### 工装保养项结论(ToolingMaintenanceResult)

**枚举编码:** `ToolingMaintenanceResult` | **枚举说明:** 工装保养项结论

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| TMR_010_INIT | 未保养 | 未保养状态 |
| TMR_020_QUALIFIED | 已保养 | 已保养状态 |

---

### 工装归还检查结论(ToolingReturnCheckResult)

**枚举编码:** `ToolingReturnCheckResult` | **枚举说明:** 工装归还检查结论

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| TRC_010_AVAILABLE | 可用 | 归还检查可用 |

---

### 工装台账操作类型(ToolingLedgerOperationType)

**枚举编码:** `ToolingLedgerOperationType` | **枚举说明:** 工装台账操作类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| TLO_10_CREATE | 创建 | 创建操作 |
| TLO_20_INBOUND | 入库 | 入库操作 |
| TLO_30_BORROW | 借用 | 借用操作 |
| TLO_40_VERIFICATION | 检定 | 检定操作 |
| TLO_50_MAINTENANCE | 保养 | 保养操作 |
| TLO_60_REPAIR | 维修 | 维修操作 |
| TLO_70_SEAL_UNSEAL | 封存启封 | 封存启封操作 |
| TLO_80_SCRAP | 报废 | 报废操作 |
| TLO_90_TRANSFER | 调拨 | 调拨操作 |
| TLO_200_OTHER | 其他 | 其他操作 |

---

### 工装检定结果(ToolingCalibrateResult)

**枚举编码:** `ToolingCalibrateResult` | **枚举说明:** 工装检定结果

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| TCR_10_QUALIFIED | 合格 | 检定合格 |
| TCR_20_SCRAP | 报废 | 检定报废 |

---

### 工装检定项结论(ToolingCalibrateItemResult)

**枚举编码:** `ToolingCalibrateItemResult` | **枚举说明:** 工装检定项结论

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| TCR_010_QUALIFIED | 合格 | 检定项合格 |
| TCR_020_NO_QUALIFIED | 不合格 | 检定项不合格 |

---

### 工装保养类型(ToolingMaintenanceType)

**枚举编码:** `toolingMaintenanceType` | **枚举说明:** 工装保养类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| TM_010_PREVENTIVE_PERIODIC | 预防性周期保养 | 按照预防性周期策略执行的保养 |
| TM_020_DAILY | 日常保养 | 日常维护保养 |
---

### 工装调拨申请单明细业务状态(ToolingTransferApplyOrderLinkBizStatus)

**枚举编码:** `ToolingTransferApplyOrderLinkBizStatus` | **枚举说明:** 工装调拨申请单明细业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| TAO_010_CREATED | 已创建 | 已创建状态 |
| TAO_020_TO_TRANSFER | 待调拨 | 待调拨状态 |
| TAO_030_TRANSFERRED | 已调拨 | 已调拨状态 |
| TAO_040_CANCELED | 已取消 | 已取消状态 |

---

### 工装报废申请单明细业务状态(ToolingScrapApplyOrderLinkBizStatus)

**枚举编码:** `ToolingScrapApplyOrderLinkBizStatus` | **枚举说明:** 工装报废申请单明细业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| SCAO_010_CREATED | 已创建 | 已创建状态 |
| SCAO_020_TO_SCRAPP | 待报废 | 待报废状态 |
| SCAO_030_SCRAPPED | 已报废 | 已报废状态 |
| SCAO_040_CANCELED | 已取消 | 已取消状态 |

---

### 工装台账业务状态(ToolingLedgerBizStatus)

**枚举编码:** `ToolingLedgerBizStatus` | **枚举说明:** 工装台账业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| RS_001_CREATED | 已创建 | 已创建状态 |
| RS_010_AVAILABLE | 在库(可用) | 在库可用状态 |
| RS_020_IN_USE | 领用中 | 领用中状态 |
| RS_030_BORROWED | 在库(借用中) | 在库借用中状态 |
| RS_040_CALIBRATING | 在库(检定中) | 在库检定中状态 |
| RS_050_MAINTAINING | 在库(保养中) | 在库保养中状态 |
| RS_060_REPAIRING | 在库(维修中) | 在库维修中状态 |
| RS_070_PENDING_STORAGE | 在库(待封存) | 在库待封存状态 |
| RS_080_STORED | 在库(已封存) | 在库已封存状态 |
| RS_090_PENDING_UNSTORAGE | 在库(待启封) | 在库待启封状态 |
| RS_100_PENDING_DISPOSAL | 在库(待处置) | 在库待处置状态 |
| RS_110_PENDING_SCRAP | 在库(待报废) | 在库待报废状态 |
| RS_120_SCRAPPED_IN_STORAGE | 在库(已报废) | 在库已报废状态 |
| RS_130_PENDING_TRANSFER | 在库(待调拨) | 在库待调拨状态 |
| RS_140_TRANSFERRED | 已调拨 | 已调拨状态 |
| RS_150_SCRAPPED | 已报废 | 已报废状态 |

---

### 工装保养任务业务状态(ToolMaintTaskBizStatus)

**枚举编码:** `ToolMaintTaskBizStatus` | **枚举说明:** 工装保养任务业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| TMT_010_INITIAL | 待保养 | 待保养状态 |
| TMT_020_STARTED | 保养中 | 保养中状态 |
| TMT_030_COMPLETED | 保养完成 | 保养完成状态 |

---

### 工装检定任务业务状态(ToolCalibrateTaskBizStatus)

**枚举编码:** `ToolCalibrateTaskBizStatus` | **枚举说明:** 工装检定任务业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| TCT_010_INITIAL | 待检定 | 待检定状态 |
| TCT_020_STARTED | 检定中 | 检定中状态 |
| TCT_030_COMPLETED | 检定完成 | 检定完成状态 |

---

### 工装借用单业务状态(BorrowOrderBizStatus)

**枚举编码:** `BorrowOrderBizStatus` | **枚举说明:** 工装借用单业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| BO_010_CREATED | 已创建 | 已创建状态 |
| BO_020_PENDING_RETURN | 待归还 | 待归还状态 |
| BO_030_PARTIALLY_RETURNED | 部分归还 | 部分归还状态 |
| BO_040_FULLY_RETURNED | 全部归还 | 全部归还状态 |
| BO_050_CANCELED | 已取消 | 已取消状态 |

---

## 五、MES模块枚举

### 生产订单类型(OrderType)

**枚举编码:** `orderType` | **枚举说明:** 生产订单类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| OT_010_STANDARD | 标准 | 标准生产订单 |
| OT_020_EXPERIMENTAL | 试验 | 试验生产订单 |
| OT_030_REPAIR | 返修 | 返修生产订单 |

---

### 生产订单业务状态(ProdOrderBizStatus)

**枚举编码:** `ProdOrderBizStatus` | **枚举说明:** 生产订单业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PO_010_CREATED | 初始 | 生产订单已创建 |
| PO_030_EXPANDED | 已展开 | 生产订单已展开 |
| PO_040_RELEASED | 已释放 | 生产订单已释放 |
| PO_050_STARTED | 已开工 | 生产订单已开工 |
| PO_060_FINISHED | 已完工 | 生产订单已完工 |

---

### 控制状态(controlStatus)

**枚举编码:** `controlStatus` | **枚举说明:** 订单/任务控制状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| CS_010_NORMAL | 正常 | 正常执行 |
| CS_020_PAUSED | 暂停 | 暂停执行 |
| CS_030_CANCEL | 取消 | 取消执行 |

---

### 释放状态(ReleasedStatus)

**枚举编码:** `ReleasedStatus` | **枚举说明:** 生产订单释放状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PO_010_NO | 未释放 | 未释放 |
| PO_020_PART | 部分释放 | 部分释放 |
| PO_030_ALL | 全部释放 | 全部释放 |

---

### 生产计划类型(ProdPlanType)

**枚举编码:** `ProdPlanType` | **枚举说明:** 生产计划类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PPT_010_NONE | 无 | 无计划 |
| PPT_030_PRODUCE | 零部件生产计划 | 零部件生产计划 |
| PPT_050_PROCESS | 零部件加工计划 | 零部件加工计划 |

---

### 排产状态(ProdScheduleState)

**枚举编码:** `ProdScheduleState` | **枚举说明:** 生产订单排产状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PSS_010_NONE | 未排产 | 未排产 |
| PSS_030_PRODUCE | 零部件生产已排产 | 零部件生产已排产 |

---

### 制造订单类型(ManuType)

**枚举编码:** `ManuType` | **枚举说明:** 制造订单制造类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| MT_010_STANDARD | 标准 | 标准制造 |
| MT_020_TRANSFER | 转工 | 转工制造 |
| MT_030_REWORK | 返工 | 返工制造 |
| MT_040_REPAIR | 返修 | 返修制造 |

---

### 制造订单业务状态(ManuOrderBizStatus)

**枚举编码:** `ManuOrderBizStatus` | **枚举说明:** 制造订单业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| MO_010_CREATED | 初始 | 制造订单已创建 |
| MO_030_EXPANDED | 已展开 | 制造订单已展开 |
| MO_040_SCHEDULED | 已排产 | 制造订单已排产 |
| MO_050_STARTED | 已开工 | 制造订单已开工 |
| MO_060_FINISHED | 已完工 | 制造订单已完工 |

---

### 到料状态(inputMaterialType)

**枚举编码:** `inputMaterialType` | **枚举说明:** 制造任务到料状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PARTIALLY_RECEIVED | 部分到料 | 部分到料 |
| NOT_RECEIVED | 未到料 | 未到料 |
| ALL_RECEIVED | 全部到料 | 全部到料 |

---

### 定额分配状态(QuotaStatus)

**枚举编码:** `QuotaStatus` | **枚举说明:** 制造任务定额分配状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PENDING | 待分配 | 待分配 |
| ALLOCATED | 已分配 | 已分配 |

---

### 派工方式(DispatchMode)

**枚举编码:** `DispatchMode` | **枚举说明:** 制造任务派工方式

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| DM_10_NONE | 未派工 | 未派工 |
| DM_20_AUTO | 自动派工 | 自动派工 |
| DM_30_MANUAL | 手动派工 | 手动派工 |

---

### 首检状态(manuTaskFirstInspectStatus)

**枚举编码:** `manuTaskFirstInspectStatus` | **枚举说明:** 制造任务首检状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| CREATED | 初始 | 初始状态 |
| INSPECTING | 检验中 | 检验中 |
| QUALIFIED | 合格 | 首检合格 |
| SCRAPPED | 报废 | 首检报废 |

---

### 制造任务业务状态(ManuTaskBizStatus)

**枚举编码:** `ManuTaskBizStatus` | **枚举说明:** 制造任务业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| MT_010_CREATED | 初始 | 制造任务已创建 |
| MT_020_DISPATCHED | 已派工 | 制造任务已派工 |
| MT_030_CONFIRMED | 已确认 | 制造任务已确认 |
| MT_040_STARTED | 已开工 | 制造任务已开工 |
| MT_050_INSPECTED | 已送检 | 制造任务已送检 |
| MT_060_FINISHED | 已完工 | 制造任务已完工 |

---

### 物料准备计划业务状态(MaterialPreparationPlanBizStatus)

**枚举编码:** `MaterialPreparationPlanBizStatus` | **枚举说明:** 物料准备计划业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| MPP_010_CREATED | 初始 | 物料准备计划已创建 |
| MPP_020_PREPARATION | 备料中 | 物料准备计划备料中 |
| MPP_030_COMPLETED | 备料完成 | 物料准备计划备料完成 |

---

### 物料准备计划明细业务状态(MaterialPlanLinkBizStatus)

**枚举编码:** `MaterialPlanLinkBizStatus` | **枚举说明:** 物料准备计划明细业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| MPP_010_CREATED | 初始 | 物料准备计划明细已创建 |
| MPP_020_PREPARATION | 已申请 | 物料准备计划明细已申请 |
| MPP_030_COMPLETED | 已收料 | 物料准备计划明细已收料 |

---

### 在制品状态(WipStatus)

**枚举编码:** `WipStatus` | **枚举说明:** 在制品状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| WIP_010_PENDING_PROCESS | 待加工 | 待加工 |
| WIP_020_PENDING_INSPECTION | 待检验 | 待检验 |
| WIP_030_COMPLETED | 已完成 | 已完成 |
| WIP_040_SCRAPPED | 已报废 | 已报废 |
| WIP_050_WAITING_FOR_MERGE | 待合并 | 待合并 |

---

### 物料装载操作类型(materialLoadType)

**枚举编码:** `materialLoadType` | **枚举说明:** 物料装载记录操作类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| LOAD | 装入 | 装入物料 |
| DETACH | 拆卸 | 拆卸物料 |

---

### 检验分类(InspectCategory)

**枚举编码:** `InspectCategory` | **枚举说明:** 检验分类

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| INS_CATEGORY_100_SELF | 自检 | 自检 |
| INS_CATEGORY_150_FIRST | 首检 | 首检 |
| INS_CATEGORY_200_MUTUAL | 互检 | 互检 |
| INS_CATEGORY_300_SPECIAL | 专检 | 专检 |
| INS_CATEGORY_400_CUSTOMER | 客户检 | 客户检 |

---

### 不合格品审批结论(ReviewConclusion)

**枚举编码:** `ReviewConclusion` | **枚举说明:** 不合格品审批结论

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| QUALIFIED | 合格 | 合格 |
| ACCEPTED | 让步接收 | 让步接收 |
| REWORK | 返工 | 返工 |
| REPAIR | 返修 | 返修 |
| SCRAP | 报废 | 报废 |
| OUTSOURCING_REPAIR | 外委返修 | 外委返修 |


---

### 外委类型(OutsourcingType)

**枚举编码:** `OutsourcingType` | **枚举说明:** 外委类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| OT_010_WHOLE_ORDER | 整单外委 | 整单外委 |
| OT_020_PROCESS | 工序外委 | 工序外委 |
| OT_030_REWORK_REPAIR | 返修外委 | 返修外委 |

---

### 外委来源类型(outsourcingSourceType)

**枚举编码:** `outsourcingSourceType` | **枚举说明:** 外委来源类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ST_010_PREDEFINED | 预定义外委 | 预定义外委 |
| ST_020_TEMPORARY | 临时外委 | 临时外委 |

---

### 收货类型(outsourcingReceiptType)

**枚举编码:** `outsourcingReceiptType` | **枚举说明:** 收货类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ORT_010_PURCHASE | 采购收货 | 采购收货 |
| ORT_020_OUTSOURCING | 外委收货 | 外委收货 |

---

### 退货类型(OutsourcingReturnType)

**枚举编码:** `OutsourcingReturnType` | **枚举说明:** 退货单类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ORO_010_PURCHASE_RETURN | 采购退货 | 采购退货 |
| ORO_020_OUTSOURCING_RETURN | 外委退货 | 外委退货 |

---

### 外委需求业务状态(OutsourcingRequireBizStatus)

**枚举编码:** `OutsourcingRequireBizStatus` | **枚举说明:** 外委需求业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| OR_10_INITIAL | 初始 | 外委需求已创建 |
| MO_20_PUBLISHED | 已发送 | 外委需求已发送 |
| MO_30_COMPLETED | 已完成 | 外委需求已完成 |

---

### 外委采购订单业务状态(OutsourcingPurchaseOrderBizStatus)

**枚举编码:** `OutsourcingPurchaseOrderBizStatus` | **枚举说明:** 外委采购订单业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| OPO_10_INITIAL | 初始 | 外委采购订单已创建 |
| OPO_20_SHIPPED | 已发货 | 外委采购订单已发货 |
| OPO_30_PARTIAL_RECEIVED | 部分收货 | 外委采购订单部分收货 |
| OPO_40_FULLY_RECEIVED | 全部收货 | 外委采购订单全部收货 |
| OPO_50_IN_STOCK | 已入库 | 外委采购订单已入库 |
| OPO_60_RETURNED | 已退货 | 外委采购订单已退货 |

---

### 外委收货单业务状态(OutsourcingReceiptOrderBizStatus)

**枚举编码:** `OutsourcingReceiptOrderBizStatus` | **枚举说明:** 外委收货单业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ORR_10_PENDING_INSPECTION | 待检验 | 外委收货单待检验 |
| ORR_20_COMPLETED | 已完成 | 外委收货单已完成 |

---

### 外委退货单类型(OutsourcingReturnType)

**枚举编码:** `OutsourcingReturnType` | **枚举说明:** 外委退货单类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ORO_010_PURCHASE_RETURN | 采购退货 | 采购退货 |
| ORO_020_OUTSOURCING_RETURN | 外委退货 | 外委退货 |

---

### 外委退货单业务状态(OutsourcingReturnOrderBizStatus)

**枚举编码:** `OutsourcingReturnOrderBizStatus` | **枚举说明:** 外委退货单业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ORO_10_PENDING_RETURN | 待退货 | 外委退货单待退货 |
| ORO_20_RETURNED | 已退货 | 外委退货单已退货 |

---

### 采购需求业务状态(PurchaseRequisitionBizStatus)

**枚举编码:** `PurchaseRequisitionBizStatus` | **枚举说明:** 采购需求业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PR_10_INITIAL | 已创建 | 采购需求已创建 |
| PR_20_PUBLISHED | 已发送 | 采购需求已发送 |

---

### 采购订单业务状态(PurchaseOrderBizStatus)

**枚举编码:** `PurchaseOrderBizStatus` | **枚举说明:** 采购订单业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PO_10_INITIAL | 初始 | 采购订单已创建 |
| PO_30_PARTIAL_RECEIVED | 部分收货 | 采购订单部分收货 |
| PO_40_FULLY_RECEIVED | 全部收货 | 采购订单全部收货 |
| PO_50_IN_STOCK | 已入库 | 采购订单已入库 |
| PO_60_RETURNED | 已退货 | 采购订单已退货 |

---

### 采购收货单业务状态(PurchaseReceiptBizStatus)

**枚举编码:** `PurchaseReceiptBizStatus` | **枚举说明:** 采购收货单业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| RR_10_PENDING_INSPECTION | 待检验 | 采购收货单待检验 |
| RR_20_COMPLETED | 已完成 | 采购收货单已完成 |

---

### 采购退货单业务状态(PurchaseReturnBizStatus)

**枚举编码:** `PurchaseReturnBizStatus` | **枚举说明:** 采购退货单业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| RO_10_PENDING_RETURN | 待退货 | 采购退货单待退货 |
| RO_20_RETURNED | 已退货 | 采购退货单已退货 |

---

### 优先级(PriorityLevel)

**枚举编码:** `PriorityLevel` | **枚举说明:** 采购申请优先级

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| NORMAL | 普通 | 普通优先级 |
| HIGH | 紧急 | 紧急优先级 |
| URGENT | 特急 | 特急优先级 |

---

### 异常任务操作类型(AbnormalOperationType)

**枚举编码:** `AbnormalOperationType` | **枚举说明:** 异常任务日志操作类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| CREATE | 创建 | 创建异常 |
| PROCESS | 处理 | 处理异常 |
| CLOSE | 关闭 | 关闭异常 |

---

### 绑定数据模型(QM_RECORD_BIND_ENTITY_TYPE)

**枚举编码:** `QM_RECORD_BIND_ENTITY_TYPE` | **枚举说明:** 质量记录模板绑定的数据模型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| MATERIAL | 物料 | 物料模型 |
| ROUTING | 工艺 | 工艺模型 |
| PROC | 工序 | 工序模型 |

---

---

### 检验任务业务状态(InspectTaskBizStatus)

**枚举编码:** `InspectTaskBizStatus` | **枚举说明:** 检验任务业务状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| IT_100_CREATED | 初始 |  |
| IT_200_PROCESS | 检验中 |  |
| IT_300_FINISHED | 已完工 |  |

---

---

### 不合格品审理结论处理状态(DefectiveReviewConclusionStatus)

**枚举编码:** `DefectiveReviewConclusionStatus` | **枚举说明:** 不合格品审理结论处理状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| PENDING | 待处理 |  |
| COMPLETED | 已完成 |  |

---

### 不合格品审理结论类型(DefectiveProductReviewConclusionType)

**枚举编码:** `DefectiveProductReviewConclusionType` | **枚举说明:** 不合格品审理结论类型

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| MAIN_PART | 主件审理结论 | 主件审理结论 |
| SUB_PART | 子件审理结论 | 子件审理结论 |

---

### 检验记录填报方式(inspectRecordMode)

**枚举编码:** `inspectRecordMode` | **枚举说明:** 检验记录的数据填报方式

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| QSI_MODE_100_SINGLE | 单项 | 单个项目填报 |
| QSI_MODE_200_TABLE | 表格 | 表格形式填报 |

---

### 质量记录模板类型(QMRecordTmplType)

**枚举编码:** `QMRecordTmplType` | **枚举说明:** 质量检验记录的模板分类

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| INTERNAL | 内部模版 | 内部质量模板 |
| EXTERNAL | 外部模版 | 外部质量模板 |

---

### 标准审批状态(standardApprovalStatus)

**枚举编码:** `standardApprovalStatus` | **枚举说明:** 技术标准的审批流程状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| AP_010_INITIAL | 初始 | 标准初始状态 |
| AP_020_IN_APPROVAL | 审批中 | 标准审批中 |
| AP_030_APPROVED | 审批通过 | 标准审批通过 |
| AP_040_REJECTED | 审批驳回 | 标准审批驳回 |

---

### 采购优先级(purchaseRequisitionPriority)

**枚举编码:** `purchaseRequisitionPriority` | **枚举说明:** 采购申请的优先级

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| URGENT | 特急 | 特急优先级 |
| HIGH | 紧急 | 紧急优先级 |
| NORMAL | 普通 | 普通优先级 |

---

### 制造订单序列号状态(ManuOrderSerialNumberStatus)

**枚举编码:** `ManuOrderSerialNumberStatus` | **枚举说明:** 制造订单序列号的状态

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ACTIVE | 正常 | 序列号正常 |
| CANCELLED | 已取消 | 序列号已取消 |

---

### 汇报类型（ReportItemType)

**枚举编码:** `ManuOrderSerialNumberStatus` | **枚举说明:** 制造订单序列号的状态

| 值编码    | 值名称 | 说明            |
| --------- | ------ | --------------- |
| QUALIFIED | 合格   | 汇报项类型-合格 |
| SCRAP     | 报废   | 汇报项类型-报废 |
| TBD       | 待定   | 汇报项类型-待定 |

---



## 六、APS模块枚举

### 日历分类(CalendarCategory)

**枚举编码:** `CalendarCategory` | **枚举说明:** 工作日历分类

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| ORG | 组织型 | 组织日历 |
| RESOURCE | 资源型 | 资源日历 |

---

### 资源分类(ResCategory)

**枚举编码:** `ResCategory` | **枚举说明:** 排程资源分类

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| C010 | 工作中心 | 工作中心资源 |
| C020 | 设备类 | 设备类资源 |
| C030 | 人员类 | 人员类资源 |

---

### 分派方法(AssignMethod)

**枚举编码:** `AssignMethod` | **枚举说明:** 排程分派方法

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| LIMITED | 有限产能 | 有限产能排程 |
| UNLIMITED | 无限产能 | 无限产能排程 |

---

### 分派方向(AssignDirection)

**枚举编码:** `AssignDirection` | **枚举说明:** 排程分派方向

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| FORWARD | 正向 | 正向排程 |
| REVERSE | 逆向 | 逆向排程 |
| REVERSE_TO_FORWARD | 逆向-允许转正向 | 逆向排程允许转正向 |

---

### 分派资源策略(AssignStrategy)

**枚举编码:** `AssignStrategy` | **枚举说明:** 排程分派资源策略

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| EAT | 资源最早空闲时间 | 选择最早空闲的资源 |
| MIP | 资源负荷 | 选择负荷最小的资源 |
| RP | 资源优先级 | 按资源优先级选择 |
| MR | 制造效率 | 按制造效率选择 |

---

### 锁定模式(LockModel)

**枚举编码:** `LockModel` | **枚举说明:** 排程任务锁定模式

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| NONE | 无锁定 | 不锁定 |
| RES_LOCKED | 资源锁定 | 锁定资源 |
| TIME_LOCKED | 时间锁定 | 锁定时间 |
| RES_TIME_LOCKED | 资源时间锁定 | 锁定资源和时间 |

---

### 加工时间单位(makeTimeUnit)

**枚举编码:** `makeTimeUnit` | **枚举说明:** 用于APS排程的加工时间单位

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| h | 小时 | 时间单位-小时 |
| m | 分钟 | 时间单位-分钟 |
| s | 秒 | 时间单位-秒 |
| d | 天 | 时间单位-天 |
| ph | 件/小时 | 每小时生产件数 |
| hp | 小时/件 | 每件耗时小时数 |
| mp | 分钟/件 | 每件耗时分钟数 |
| pm | 件/分钟 | 每分钟生产件数 |
| sp | 秒/件 | 每件耗时秒数 |
| ps | 件/秒 | 每秒生产件数 |
| pd | 件/天 | 每天生产件数 |
| dp | 天/件 | 每件耗时天数 |

---

### 库房作业模式(WarehouseOperationMode)

**枚举编码:** `WarehouseOperationMode` | **枚举说明:**库房作业模式

| 值编码 | 值名称 | 说明 |
|--------|--------|------|
| 010_FLAT | 普通库房 |  |
| 020_ASRS | 立体库 |  |

---



### 资质等级状态(QualificationRelationStatus)

**枚举编码:** `QualificationRelationStatus` | **枚举说明:**资质等级状态

| 值编码  | 值名称 | 说明 |
| ------- | ------ | ---- |
| VALID   | 有效   |      |
| INVALID | 失效   |      |

---



## 变更记录

| 日期 | 版本 | 变更内容 | 变更人 |
|-----|------|---------|--------|
| 2026-04-08 | v1.10 | 修正物流任务类型（LogisticsTaskType）为发料周转、退料周转、工序间周转、入库周转、临时周转、空车呼叫 | Codex |
| 2026-03-27 | v1.9 | 新增WMS模块物流位置类型、物流任务类型、物流任务状态枚举 | 危放 |
| 2026-03-18 | v1.8 | 添加资质等级状态枚举 | 李鸿坤 |
| 2026-02-25 | v1.7 | 删除不合格审批状态(DefectiveApprovalStatus)、工装管理方式(methodType) | 危放 |
| 2026-01-26 | v1.6 | 【规范性修正】根据枚举值.md实际定义，修正所有枚举编码格式,确保文档与实际数据库定义完全一致。 | 危放 |
| 2026-01-26 | v1.5 | 补充缺失的枚举定义：securityLevel、showType、compType、resType、toolingType、measureUnit、lockState、lifecycleStateType、UserLayoutSharingScope、CommonActivityBizStatus、factoryType、equipTepmlateType、equipPlanConclusion、InStorageStatus、inspectRecordMode、QMRecordTmplType、standardApprovalStatus、purchaseRequisitionPriority、ManuOrderSerialNumberStatus；更新WarehouseType的值编码、补充RoutingType的REWORK和REPAIR值、更新WorkCenterType为实际编码、补充ManuOrderBizStatus的MO_040_SCHEDULED | 危放 |
| 2026-01-22 | v1.4 | 添加MES模块枚举:DefectiveProductReviewConclusionType（不合格品审理结论类型） | 薛启宽 |
| 2026-01-09 | v1.3 | 添加MES模块业务状态枚举： | 李鸿坤 |
| 2026-01-08 | v1.2 | 添加TMS模块缺失的枚举 | 李飞 |
| 2026-01-08 | v1.1 | 添加EMS模块缺失的枚举:EquipLedgerBizStatus、EquipFaultBizStatus、MaintenancePlanBizStatus，将ProductivityUnit从单位改为枚举 | 危放 |
| 2025-12-29 | v1.0 | 创建文档,定义所有模块枚举 | 王晴 |
