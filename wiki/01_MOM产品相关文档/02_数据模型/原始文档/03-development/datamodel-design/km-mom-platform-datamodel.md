# 平台模块数据模型

## 文档说明

**基本信息**
- 文档版本：v1.14 | 更新日期：2026-04-22 | 维护团队：产品研发团队
- 目标受众：产品研发团队

**文档定位**

本文档定义 KMMOM3.x 平台模块的数据模型设计，包括主数据管理、认证授权、配置管理、监控等核心功能的数据结构，为产品平台提供统一的数据模型基础。

**内容结构**

| 章节 | 核心问题 | 内容说明 |
|------|---------|----------|
| 一、术语、定义和缩略语 | 核心术语如何定义？ | 定义平台模块涉及的业务术语和缩略语 |
| 二、认证授权 | 认证授权如何设计？ | 行政组织、用户、角色、权限、功能菜单、API密钥、审计等 |
| 三、系统配置 | 配置管理包含哪些功能？ | 业务配置、编码规则、条码规则、脚本管理、WebHook、文档工具等 |
| 四、主数据 | 主数据包含哪些实体？ | 业务组织、物料、工艺路线、工作中心、设备、库房等主数据实体 |
| 五、监控管理 | 系统如何记录日志？ | 业务日志、审计日志、图像文件等 |

---

## 一、术语、定义和缩略语

| 术语 | 定义 | 缩略语 |
|------|------|--------|
| 工作中心 | 生产执行的基本单元，可以是产线、设备、人员小组或外委单位 | WC |
| 工时精度 | 工作中心记录工时的最小时间单位，单位为分钟 | - |
| 资质等级 | 人员操作技能的等级认证（如钳工、车工、焊工） | - |
| MBOM | 制造物料清单，描述产品的物料组成结构 | Manufacturing BOM |
| 工艺路线 | 产品制造过程中的工序序列及相关参数 | Routing |
| 生命周期 | 对象从创建到报废的状态变化过程 | Lifecycle |
| 审计日志 | 记录系统安全相关操作的日志，用于合规审计 | Audit Log |
| WebHook | HTTP回调机制，用于事件触发后的外部系统通知 | - |

---

## 二、认证授权

### 2.1 行政组织（Org）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** `IntegrationManaged` | **表名:** `SYS_ORG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|------|------|------|-----|
| 编码 | `code` | `CCODE` | 字符串  | 512 | 必填 | |
| 名称 | `name` | `CNAME` | 字符串  | 512 | 必填 | |
| 备注 | `remark` | `CREMARK` | 字符串  | 1024 | 无 | |
| 行政组织类型 | `orgType` | `CORG_TYPE` | 字符串  | 256 | 必填 | |
| 序号 | `index` | `CINDEX` | 整型   | - | 无 | |
| 简称 | `shortName` | `CSHORT_NAME` | 字符串  | 256 | 无 | |
| 启用标记 | `enableFlag` | `CENABLE_FLAG` | 布尔   | - | 必填 | |
| 根节点 | `rootId` | `CROOT_ID` | 长整型  | - | 无 | |
| 父节点 | `parentId` | `CPARENT_ID` | 长整型  | - | 无 | |
| 编码路径 | `fullPath` | `CFULL_PATH` | 字符串  | 4000 | 无 | |

### 2.2 行政组织与用户关系（OrgUser）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_ORG_USER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 行政组织 | `orgId` | `CORG_ID` | 长整型 | - | 必填 | 引用Org |
| 用户 | `userId` | `CUSER_ID` | 长整型 | - | 必填 | 引用用户 |

### 2.4 用户（User）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** `IntegrationManaged` | **表名:** `SYS_USER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 用户账号 | `code` | `CCODE` | 字符串 | 512 | 必填 | |
| 姓名 | `name` | `CNAME` | 字符串 | 512 | 必填 | |
| 用户类型 | `userType` | `CUSER_TYPE` | 字符串 | 256 | 必填 |  |
| 备注 | `remark` | `CREMARK` | 字符串 | 1024 | 无 | |
| 密码 | `password` | `CPASSWORD` | 字符串 | 256 | 必填 | 使用SHA-256+Salt加密存储 |
| 用户密级 | `personLevel` | `CPERSON_LEVEL` | 枚举 | - | 必填 | 引用枚举:personLevel |
| 状态 | `state` | `CSTATE` | 字符串 | 256 | 必填 |  |
| 锁定标记 | `lockFlag` | `CLOCK_FLAG` | 布尔 | - | 必填 | |
| 锁定原因 | `lockReason` | `CLOCK_REASON` | 字符串 | 256 | 无 | 人为锁定:MANUAL_LOCK\|密码错误超限:PWD_ERROR |
| 系统标记 | `sysFlag` | `CSYS_FLAG` | 布尔 | - | 必填 | true:系统内置\|false:业务扩展 |
| 密码验证失败次数 | `pwdErrNum` | `CPWD_ERR_NUM` | 整型 | - | 无 | |
| 密码最近更新时间 | `pwdUpdateTime` | `CPWD_UPDATE_TIME` | 日期时间 | - | 无 | |
| 密码重置标记 | `pwdResetFlag` | `CPWD_RESET_FLAG` | 布尔 | - | 必填 | true:密码已被重置需强制修改\|false:正常状态 |
| 密码使用次数 | `pwdUseNum` | `CPWD_USE_NUM` | 整型 | - | 无 | |
| 性别         | `sex`            | `CSEX`             | 字符串  | 256 | 无   |                                    |
| 出生日期     | `birthDate`      | `CBIRTH_DATE`      | 日期     | -    | 无   |                                              |
| 联系方式     | `phoneNumber`    | `CPHONE_NUMBER`    | 字符串   | 20   | 无   |                                              |
| 邮箱地址     | `email`          | `CEMAIL`           | 字符串   | 100  | 无   |                                              |
| 在职状态     | `employedStatus` | `CEMPLOYED_STATUS` | 字符串  | 256 | 无   |  |
| 在岗状态     | `dutyStatus`     | `CDUTY_STATUS`     | 字符串  | 256 | 无   |                         |
| 证件号码     | `idNo`           | `CID_NO`           | 字符串   | 50    | 无   |                                              |


### 2.5 角色（Role）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_ROLE`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 编码 | `code` | `CCODE` | 字符串 | 512 | 必填 | |
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 | |
| 备注 | `remark` | `CREMARK` | 字符串 | 1024 | 无 | |
| 角色类型 | `roleType` | `CROLE_TYPE` | 字符串 | 256 | 必填 |  |
| 状态 | `state` | `CSTATE` | 字符串 | 256 | 必填 |  |
| 系统标记 | `sysFlag` | `CSYS_FLAG` | 布尔 | - | 必填 | true:系统内置\|false:业务扩展 |

### 2.6 角色与用户关系（RoleUser）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_ROLE_USER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 角色 | `roleId` | `CROLE_ID` | 长整型 | - | 必填 | 引用Role |
| 用户 | `userId` | `CUSER_ID` | 长整型 | - | 必填 | 引用User |

### 2.7 菜单（Menu）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_MENU`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 编码 | `code` | `CCODE` | 字符串 | 512 | 必填 | |
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 | |
| 备注 | `remark` | `CREMARK` | 字符串 | 1024 | 无 | |
| 功能类型 | `featureType` | `CFEATURE_TYPE` | 字符串 | 256 | 无 |  |
| 功能范围 | `featureScope` | `CFEATURE_SCOPE` | 字符串 | 256 | 必填 |  |
| 图标 | `icon` | `CICON` | 字符串 | 256 | 无 | |
| 链接类型 | `linkType` | `CLINK_TYPE` | 字符串 | 256 | 无 |  |
| 打开方式 | `linkTarget` | `CLINK_TARGET` | 字符串 | 256 | 无 |      |
| 路由 | `linkUrl` | `CLINK_URL` | 字符串 | 256 | 无 | |
| 序号 | `index` | `CINDEX` | 整型 | - | 必填 | |
| 导航显示 | `visibleFlag` | `CVISIBLE_FLAG` | 布尔 | - | 无 | |
| 当前节点全路径 | `fullPath` | `CFULL_PATH` | 字符串 | 1024 | 无 | |
| 父节点 | `parentId` | `CPARENT_ID` | 长整型 | - | 无 | |
| 根节点 | `rootId` | `CROOT_ID` | 长整型 | - | 无 | |
| 所属站点 | `site` | `CSITE` | 字符串 | 256  | 必填 |  |

### 2.7 功能权限定义（FeatureDefine）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_FEATURE_DEFINE`

| 属性中文名称  | 属性英文名称         | 数据库列名 | 数据类型 | 长度 | 约束 | 说明       |
|---------|----------------|-----------|------|------|------|----------|
| 编码      | `code`         | `CCODE` | 字符串  | 512 | 必填 |          |
| 名称      | `name`         | `CNAME` | 字符串  | 512 | 必填 |          |
| 备注      | `remark`       | `CREMARK` | 字符串  | 1024 | 无 |          |
| 类型      | `type`         | `CTYPE` | 字符串  | 256 | 无 | 功能分组 功能码 |
| 序号      | `index`        | `CINDEX` | 整型   | - | 必填 |          |
| 范围	      | `scope`        | `CSCOPE` | 字符串  | - | 必填 |          |
| 预定义标记	      | `predefinedFlag`        | `CPREDEFINED_FLAG` | 布尔   | - | 必填 |          |
| 当前节点全路径 | `fullPath`     | `CFULL_PATH` | 字符串  | 1024 | 无 |          |
| 父节点     | `parentId`     | `CPARENT_ID` | 长整型  | - | 无 |          |
| 根节点     | `rootId`       | `CROOT_ID` | 长整型  | - | 无 |          |

### 2.8 菜单收藏（FavoriteMenu）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_FAVORITE_MENU`

| 属性中文名称 | 属性英文名称   | 数据库列名      | 数据类型 | 长度 | 约束 | 说明     |
|-------------|----------|------------|---------|------|------|--------|
| 类型 | `type`   | `CTYPE`    | 字符串 | 256 | 必填 |        |
| 用户 | `userId` | `CUSER_ID` | 长整型 | - | 必填 | 引用User |
| 菜单 | `menuId` | `CMENU_ID` | 长整型 | - | 必填 | 引用Menu |

### 2.9 角色与菜单权限关系（RoleMenuPermission）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_ROLE_MENU_PERMISSION`

| 属性中文名称 | 属性英文名称         | 数据库列名            | 数据类型 | 长度 | 约束 | 说明 |
|--------|----------------|------------------|---------|------|------|------|
| 角色     | `roleId`       | `CROLE_ID`       | 长整型 | - | 必填 | 引用Role |
| 终端类型   | `terminalType` | `CTERMINAL_TYPE` | 字符串 | 256 | 必填 |  |
| 菜单     | `menuId`       | `CMENU_ID`       | 长整型 | - | 必填 | 引用Menu |


### 2.9 角色与功能权限定义关系（RoleFeatureDefinePermission）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_ROLE_FEATURE_DEFINE_PERMISSION`

| 属性中文名称 | 属性英文名称 | 数据库列名          | 数据类型 | 长度 | 约束 | 说明              |
|--------|-------------|----------------|---------|------|------|-----------------|
| 角色     | `roleId` | `CROLE_ID`     | 长整型 | - | 必填 | 引用Role          |
| 功能权限定义 | `featureDefineId` | `CFEATURE_DEFINE_ID` | 长整型 | - | 必填 | 引用FeatureDefine |


### 2.10 角色与业务组织权限关系（RoleBizOrgPermission）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_ROLE_BIZ_ORG_PERMISSION`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 角色 | `roleId` | `CROLE_ID` | 长整型 | - | 必填 | 引用Role |
| 范围 | `scope` | `CSCOPE` | 字符串 | 256 | 必填 |  |
| 组织 | `bizOrgIds` | `CBIZ_ORG_IDS` | CLOB | - | 无 | |

### 2.11 角色与属性权限关系（RolePropertyPermission）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_ROLE_PROPERTY_PERMISSION`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 角色 | `roleId` | `CROLE_ID` | 长整型 | - | 必填 | 引用Role |
| 实体类型 | `entityModel` | `CENTITY_MODEL` | 字符串 | 256 | 必填 | |
| 属性编码 | `propertyCode` | `CPROPERTY_CODE` | 字符串 | 256 | 必填 | |
| 属性名称 | `propertyName` | `CPROPERTY_NAME` | 字符串 | 256 | 无 | |
| 允许浏览标记 | `allowBrowseFlag` | `CALLOW_BROWSE_FLAG` | 布尔 | - | 必填 | |
| 允许编辑标记 | `allowEditFlag` | `CALLOW_EDIT_FLAG` | 布尔 | - | 必填 | |

### 2.12 角色与实体操作权限关系（RoleEntityOperationPermission）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_ROLE_ENTITY_OPERATION_PERMISSION`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 角色 | `roleId` | `CROLE_ID` | 长整型 | - | 必填 | 引用Role |
| 实体类型 | `entityModel` | `CENTITY_MODEL` | 字符串 | 256 | 必填 | |
| 操作编码 | `operationCode` | `COPERATION_CODE` | 字符串 | 256 | 必填 | |
| 操作名称 | `operationName` | `COPERATION_NAME` | 字符串 | 256 | 无 | |

### 2.13 API密钥（ApiKey）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_API_KEY`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 名称 | `name` | `CNAME` | 字符串 | 256 | 必填 | |
| 密钥 | `apiKey` | `CAPI_KEY` | 字符串 | 256 | 无 | |
| 描述 | `description` | `CDESCRIPTION` | 字符串 | 1024 | 无 | |
| 路径规则 | `pathRules` | `CPATH_RULES` | CLOB | - | 无 | |
| 状态 | `status` | `CSTATUS` | 字符串 | 256 | 无 | |
| 绑定用户 | `bindUser` | `CBIND_USER` | 长整型 | - | 无 | 引用User |

### 2.14 审计日志（AuditLog）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_AUDIT_LOG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 操作人 | `operator` | `COPERATOR` | 长整型 | - | 必填 | |
| 操作人编码 | `operatorCode` | `COPERATOR_CODE` | 字符串 | 256 | 必填 | |
| 操作人名称 | `operatorName` | `COPERATOR_NAME` | 字符串 | 256 | 必填 | |
| 日志类型 | `logType` | `CLOG_TYPE` | 字符串 | 256 | 必填 | 审计日志:10 |
| 操作内容 | `actionContent` | `CACTION_CONTENT` | CLOB | - | 无 | |
| 审计状态 | `auditStatus` | `CAUDIT_STATUS` | 整型 | 255 | 无 | 待审计:0\|已审计:1 |
| 审计人 | `auditor` | `CAUDITOR` | 长整型 | - | 无 | |
| 审计意见 | `auditResult` | `CAUDIT_RESULT` | 字符串 | 256 | 无 | |
| 审计时间 | `auditTime` | `CAUDIT_TIME` | 日期时间 | - | 无 | |
| 审计人IP | `auditIp` | `CAUDIT_IP` | 字符串 | 256 | 无 | |
| 审计说明 | `auditRemark` | `CAUDIT_REMARK` | 字符串 | 1024 | 无 | |
| 日志审计编号 | `auditNo` | `CAUDIT_NO` | 字符串 | 256 | 无 | |
| 审计人编码 | `auditorCode` | `CAUDITOR_CODE` | 字符串 | 256 | 无 | |
| 审计人名称 | `auditorName` | `CAUDITOR_NAME` | 字符串 | 256 | 无 | |

### 2.15 角色日志浏览审计权限关系（RoleAuditLogPermission）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_ROLE_AUDIT_LOG_PERMISSION`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 角色 | `roleId` | `CROLE_ID` | 长整型 | - | 无 | |
| 目标角色ID | `targetRoleId` | `CTARGET_ROLE_ID` | 长整型 | - | 无 | |
| 是否允许 | `allowed` | `CALLOWED` | 布尔 | - | 无 | |

### 2.16 角色分组（RoleGroup）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_ROLE_GROUP`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 名称 | `name` | `CNAME` | 字符串 | 256 | 必填 |  |
| 父节点 | `parentId` | `CPARENT_ID` | 长整型 | - | 无 |  |
| 根节点 | `rootId` | `CROOT_ID` | 长整型 | - | 无 |  |
| 备注 | `remark` | `CREMARK` | 字符串 | 512 | 无 |  |
| 分组ID路径 | `fullPath` | `CFULL_PATH` | 字符串 | 4000 | 无 |  |

---

## 三、系统配置

### 3.1 业务配置定义（ConfigDefinition）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_CONFIG_DEFINITION`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 编码 | `code` | `CCODE` | 字符串 | 512 | 必填 | |
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 | |
| 备注 | `remark` | `CREMARK` | 字符串 | 1024 | 无 | |
| 应用编码 | `app` | `CAPP` | 字符串 | 256 | 无 | |
| 配置展示类型 | `showType` | `CSHOW_TYPE` | 字符串 | 128 | 无 | 取值范围：item\|group |
| 描述 | `description` | `CDESCRIPTION` | 字符串 | 1024 | 无 | |
| 组件类型 | `compType` | `CCOMP_TYPE` | 字符串 | 256 | 无 | 取值范围：TEXT\|NUM |
| 组件配置 | `compConfig` | `CCOMP_CONFIG` | CLOB | - | 无 | |
| 父节点 | `parent` | `CPARENT` | 字符串 | 256 | 无 | |
| 序号 | `index` | `CINDEX` | 整型 | - | 无 | |
| 默认值 | `defaultValue` | `CDEFAULT_VALUE` | 字符串 | 4000 | 无 | 单值以字符串存储，多值以JSON存储 |
| 模块 | `mould` | `CMOULD` | 字符串 | 256 | 无 | |

### 3.2 业务配置值（ConfigValue）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_CONFIG_VALUE`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 应用编码 | `app` | `CAPP` | 字符串 | 256 | 必填 | |
| 所属组织 | `bizOrg` | `CBIZ_ORG` | 引用对象 | - | 无 | 引用BizOrg，0表示工厂级别 |
| 编码 | `code` | `CCODE` | 字符串 | 256 | 必填 | |
| 值 | `value` | `CVALUE` | 字符串 | 4000 | 必填 | |

### 3.3 项目配置方案（ProjectConfigScheme）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_PROJECT_CONFIG_SCHEME`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 项目编码         | `code`       | `CCODE`    | 字符串   | 256  | 必填 |      |
| 项目名称         | `name`       | `CNAME`    | 字符串   | 256  | 必填 | |
| 启用标记 | `enableFlag` | `CENABLE_FLAG` | 布尔 | - | 无 |  |
| 描述 | `remark` | `CREMARK` | 字符串 | 256 | 无 | |


### 3.4 条码规则（BarCodeRule）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_BAR_CODE_RULE`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 编码 | `code` | `CCODE` | 字符串 | 256 | 必填 | |
| 名称 | `name` | `CNAME` | 字符串 | 256 | 必填 | |
| 脚本 | `script` | `CSCRIPT` | 字符串 | 512 | 无 | |
| 预定义标记 | `isPredefined` | `CIS_PREDEFINED` | 布尔 | - | 无 | 默认false |
| 备注 | `remark` | `CREMARK` | 字符串 | 1024 | 无 | |

### 3.5 脚本（Script）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_SCRIPT`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 编码 | `code` | `CCODE` | 字符串 | 256 | 必填 | |
| 名称 | `name` | `CNAME` | 字符串 | 256 | 必填 | |
| 脚本分类 | `scriptCategory` | `CSCRIPT_CATEGORY` | 分类 | - | 必填 | 引用分类:ScriptCategory |
| 脚本内容 | `scriptContent` | `CSCRIPT_CONTENT` | CLOB | - | 必填 | |
| 启用标记 | `enableFlag` | `CENABLE_FLAG` | 布尔 | - | 必填 | |
| 备注 | `remark` | `CREMARK` | 字符串 | 512 | 无 | |

### 3.6 脚本执行日志（ScriptExecutionLog）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_SCRIPT_EXECUTION_LOG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 脚本编码 | `scriptCode` | `CSCRIPT_CODE` | 字符串 | 256 | 必填 | |
| 脚本名称 | `scriptName` | `CSCRIPT_NAME` | 字符串 | 256 | 必填 | |
| 脚本分类 | `scriptCategory` | `CSCRIPT_CATEGORY` | 分类 | - | 必填 | 引用分类:ScriptCategory |
| 执行参数 | `inputParams` | `CINPUT_PARAMS` | CLOB | - | 无 | |
| 返回结果详情 | `outputResult` | `COUTPUT_RESULT` | CLOB | - | 无 | |
| 执行结果 | `executionResult` | `CEXECUTION_RESULT` | 布尔 | - | 无 | |
| 错误信息 | `errorMessage` | `CERROR_MESSAGE` | CLOB | - | 无 | |
| 执行时间 | `executionTime` | `CEXECUTION_TIME` | 长整型 | - | 无 | |

### 3.7 WebHook配置（WebHookConfig）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_WEB_HOOK_CONFIG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| WebHook编码 | `hookCode` | `CHOOK_CODE` | 字符串 | 256 | 必填 | |
| WebHook名称 | `hookName` | `CHOOK_NAME` | 字符串 | 256 | 必填 | |
| 接口地址 | `url` | `CURL` | 字符串 | 1024 | 必填 | |
| 请求方式 | `method` | `CMETHOD` | 字符串 | 256 | 必填 | |
| 执行模式 | `mode` | `CMODE` | 字符串 | 256 | 必填 | |
| API密钥 | `secret` | `CSECRET` | 字符串 | 1024 | 必填 | |
| 连接超时时间 | `timeoutSeconds` | `CTIMEOUT_SECONDS` | 整型 | - | 无 | |
| 最大重试次数 | `maxRetries` | `CMAX_RETRIES` | 整型 | - | 无 | |
| 优先级 | `priority` | `CPRIORITY` | 整型 | - | 无 | |
| 启用标记 | `active` | `CACTIVE` | 布尔 | - | 必填 | |
| 描述 | `description` | `CDESCRIPTION` | 字符串 | 1024 | 无 | |
| 请求头 | `headers` | `CHEADERS` | 字符串 | 1024 | 无 | |
| API来源 | `apiSource` | `CAPI_SOURCE` | 字符串 | 256 | 无 | |

### 3.8 WebHook执行日志（WebHookExecutionLog）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_WEB_HOOK_EXECUTION_LOG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 配置ID | `configId` | `CCONFIG_ID` | 长整型 | - | 无 | 引用WebHookConfig |
| WebHook编码 | `hookCode` | `CHOOK_CODE` | 字符串 | 256 | 必填 | |
| WebHook名称 | `hookName` | `CHOOK_NAME` | 字符串 | 256 | 必填 | |
| 接口地址 | `url` | `CURL` | 字符串 | 1024 | 必填 | |
| 请求方式 | `method` | `CMETHOD` | 字符串 | 256 | 必填 | |
| 执行模式 | `mode` | `CMODE` | 字符串 | 256 | 必填 | |
| 请求头 | `requestHeaders` | `CREQUEST_HEADERS` | CLOB | - | 无 | |
| 请求载荷 | `requestPayload` | `CREQUEST_PAYLOAD` | CLOB | - | 无 | |
| 响应状态码 | `responseStatus` | `CRESPONSE_STATUS` | 整型 | - | 无 | |
| 响应头 | `responseHeaders` | `CRESPONSE_HEADERS` | CLOB | - | 无 | |
| 响应内容 | `responseBody` | `CRESPONSE_BODY` | CLOB | - | 无 | |
| 初始时间 | `initTime` | `CINIT_TIME` | 日期时间 | - | 无 | |
| 开始时间 | `startTime` | `CSTART_TIME` | 日期时间 | - | 无 | |
| 结束时间 | `endTime` | `CEND_TIME` | 日期时间 | - | 无 | |
| 执行耗时 | `executionTime` | `CEXECUTION_TIME` | 长整型 | - | 无 | |
| 执行状态 | `success` | `CSUCCESS` | 布尔 | - | 无 | |
| 错误消息 | `errorMessage` | `CERROR_MESSAGE` | 字符串 | 4000 | 无 | |
| 重试次数 | `retryCount` | `CRETRY_COUNT` | 整型 | - | 无 | |
| 请求ID | `requestId` | `CREQUEST_ID` | 字符串 | 256 | 无 | |
| 触发用户 | `triggeredBy` | `CTRIGGERED_BY` | 长整型 | - | 无 | |
| 触发用户编码 | `triggeredByCode` | `CTRIGGERED_BY_CODE` | 字符串 | 256 | 无 | |
| 触发用户名称 | `triggeredByName` | `CTRIGGERED_BY_NAME` | 字符串 | 256 | 无 | |
| 执行时配置 | `executionConfig` | `CEXECUTION_CONFIG` | 字符串 | 256 | 无 | |

### 3.9 文档工具（DocTool）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_DOC_TOOL`

| 属性中文名称 | 属性英文名称       | 数据库列名          | 数据类型 | 长度 | 约束 | 说明 |
|-------------|--------------|----------------|---------|------|------|------|
| 编码 | `code`       | `CCODE`        | 字符串 | 256 | 必填 | 唯一标识，不可修改 |
| 名称 | `name`       | `CNAME`        | 字符串 | 256 | 必填 | |
| 备注 | `remark`     | `CREMARK`      | 字符串 | 512 | 无 | |
| 内置标记 | `sysFlag`    | `CSYS_FLAG`    | 布尔 | - | 必填 | 默认否，内置数据不允许修改 |
| 浏览标记 | `browseFlag` | `CBROWSE_FLAG` | 布尔 | - | 必填 | 默认否 |

### 3.10 文档模型与工具关系（DocModelToolRelation）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_DOC_MODEL_TOOL_RELATION`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 文档实体类型 | `docEntityType` | `CDOC_ENTITY_TYPE` | 字符串 | 256 | 必填 | |
| 浏览工具 | `browseTool` | `CBROWSE_TOOL` | 字符串 | 256 | 无 | |

### 3.11 配置包导出记录（ConfigPackageExport）

**模型类型:** 系统模型 | **父模型:** `FileObject` | **接口:** 无 | **表名:** `SYS_CONFIG_PACKAGE_EXPORT`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 版本号 | `version` | `CVERSION` | 字符串 | 256 | 无 | |
| 说明 | `remark` | `CREMARK` | 字符串 | 512 | 无 | |
| 数据范围 | `detailScope` | `CDETAIL_SCOPE` | CLOB | - | 无 | 序列化导出模型及ID的集合 |
| 类型 | `packageType` | `CPACKAGE_TYPE` | 枚举 | 128 | 必填 | 引用枚举:packageType |

### 3.12 配置包导入记录（ConfigPackageImport）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_CONFIG_PACKAGE_IMPORT`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 导入包名 | `importPackageName` | `CIMPORT_PACKAGE_NAME` | 字符串 | 512 | 无 | |
| 导入包摘要 | `importPackageManifest` | `CIMPORT_PACKAGE_MANIFEST` | CLOB | - | 无 | |
| 导入包类型 | `importPackageType` | `CIMPORT_PACKAGE_TYPE` | 字符串 | 128 | 无 | |
| 成功标记 | `successFlag` | `CSUCCESS_FLAG` | 布尔 | - | 必填 | |
| 存在时覆盖标记 | `overwriteFlag` | `COVERWRITE_FLAG` | 布尔 | - | 必填 | |

### 3.13 系统外观配置（AppearanceConfig）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_APPEARANCE_CONFIG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 系统主标题 | `systemMainTitle` | `CSYSTEM_MAIN_TITLE` | 字符串 | 256 | 必填 | |
| 系统子标题 | `systemSubTitle` | `CSYSTEM_SUB_TITLE` | 字符串 | 256 | 无 | |
| 平台LOGO | `platformLogo` | `CPLATFORM_LOGO` | 引用对象 | - | 无 | |
| 网站图标 | `websiteIcon` | `CWEBSITE_ICON` | 引用对象 | - | 无 | |
| 用户头像 | `userAvatar` | `CUSER_AVATAR` | 引用对象 | - | 无 | |
| 预设背景静态文件路径 | `loginBackgroundPath` | `CLOGIN_BACKGROUND_PATH` | 字符串 | 256 | 无 | |
| 自定义登录背景 | `loginCustomBg` | `CLOGIN_CUSTOM_BG` | 引用对象 | - | 无 | |
| 登录页面欢迎语 | `loginWelcomeMessage` | `CLOGIN_WELCOME_MESSAGE` | 字符串 | 512 | 无 | |
| 首页背景图片静态文件路径 | `homeBackgroundPath` | `CHOME_BACKGROUND_PATH` | 字符串 | 256 | 无 | |
| 首页背景图片 | `homeBackground` | `CHOME_BACKGROUND` | 引用对象 | - | 无 | |
| 水印显示开启状态 | `displayEnabled` | `CDISPLAY_ENABLED` | 布尔 | - | 无 | |
| 水印类型 | `watermarkType` | `CWATERMARK_TYPE` | 字符串 | 256 | 无 | |
| 文字水印内容 | `watermarkText` | `CWATERMARK_TEXT` | 字符串 | 256 | 无 | |
| 图片水印文件 | `watermarkImage` | `CWATERMARK_IMAGE` | 引用对象 | - | 无 | |
| 水印是否显示当前用户名 | `watermarkShowUsername` | `CWATERMARK_SHOW_USERNAME` | 布尔 | - | 无 | |
| 水印是否显示当前用户编码 | `watermarkShowUserCode` | `CWATERMARK_SHOW_USERCODE` | 布尔 | - | 无 | |
| 水印是否显示当前时间 | `watermarkShowTime` | `CWATERMARK_SHOW_TIME` | 布尔 | - | 无 | |
| 水印是否显示当前组织 | `watermarkShowOrg` | `CWATERMARK_SHOW_ORG` | 布尔 | - | 无 | |

### 3.14 页面事件配置（PageEventConfig）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_PAGE_EVENT_CONFIG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 编码 | `code` | `CCODE` | 字符串 | 256 | 无 |  |
| 名称 | `name` | `CNAME` | 字符串 | 256 | 无 |  |
| 站点 | `site` | `CSITE` | 字符串 | 256 | 无 |  |
| 配置值 | `configValue` | `CCONFIG_VALUE` | CLOB | - | 无 |  |

### 3.15 新服务端布局配置（ServerSideLayoutConfig）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `ConfigManaged` | **表名:** `MOM_SERVER_SIDE_LAYOUT_CONFIG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 布局编码 | `layoutCode` | `CLAYOUT_CODE` | 字符串 | 256 | 必填 |  |
| 布局类型 | `layoutType` | `CLAYOUT_TYPE` | 字符串 | 256 | 必填 |  |
| 所属实体类型 | `belongEntityType` | `CBELONG_ENTITY_TYPE` | 字符串 | 256 | 无 |  |
| 配置值 | `configValue` | `CCONFIG_VALUE` | CLOB | - | 无 |  |
| 名称 | `name` | `CNAME` | 字符串 | 256 | 无 |  |

### 3.16 服务端扩展按钮配置（ServerSideActionConfig）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_SERVER_SIDE_ACTION_CONFIG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-----------|-------------|-----------|------|------|------|-----|
| 功能编码 | `code` | `CCODE` | 字符串  | 512 | 必填 | 命名规范：大写字母+下划线，如CUSTOM_EXPORT |
| 功能名称 | `name` | `CNAME` | 字符串  | 512 | 必填 | |
| 所属权限组 | `featureDefineCode` | `CDEATURE_DEFINE_CODE` | 字符串  | - | 无 | |
| 所属实体类型 | `belongEntityType` | `CBELONG_ENTITY_TYPE` | 字符串  | 256 | 无 | |
| 布局类型 | `layoutType` | `CLAYOUT_TYPE` | 字符串  | 256 | 无 | 如object-table、object-form、detail-form |
| 显示顺序 | `index` | `CINDEX` | 整型   | - | 无 | 数值越小越靠前 |
| 类型 | `type` | `CTYPE` | 字符串   | - | 无 | 数值越小越靠前 |
| 布局编码 | `layoutCode` | `CLAYOUT_CODE` | 字符串   | - | 无 | 数值越小越靠前 |
| 启用标记 | `enabledFlag` | `CENABLED_FLAG` | 整型   | - | 无 | 数值越小越靠前 |

### 3.17 用户布局配置（UserLayoutConfig）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_USER_LAYOUT_CONFIG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 所属用户 | `user` | `CUSER` | 用户 | - | 必填 | 引用User |
| 所属实体类型 | `belongEntityType` | `CBELONG_ENTITY_TYPE` | 字符串 | 256 | 必填 |  |
| 布局编码 | `layoutCode` | `CLAYOUT_CODE` | 字符串 | 256 | 必填 |  |
| 布局类型 | `layoutType` | `CLAYOUT_TYPE` | 字符串 | 256 | 必填 |  |
| 所属站点 | `site` | `CSITE` | 字符串 | 256 | 必填 |  |
| 配置值 | `configValue` | `CCONFIG_VALUE` | CLOB | - | 必填 |  |

### 3.18 用户布局方案分享（UserLayoutSolutionSharing）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_USER_LAYOUT_SOLUTION_SHARING`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 名称 | `name` | `CNAME` | 字符串 | 256 | 必填 |  |
| 所属站点 | `site` | `CSITE` | 字符串 | 256 | 必填 |  |
| 分享范围 | `sharingScope` | `CSHARING_SCOPE` | 枚举 | 256 | 必填 | 引用枚举:UserLayoutSharingScope |
| 是否需要通知 | `notifyFlag` | `CNOTIFY_FLAG` | 布尔 | - | 必填 |  |
| 分享者 | `sharer` | `CSHARER` | 用户 | - | 必填 | 引用User |

### 3.19 用户布局方案分享配置（UserLayoutSolutionSharingConfigLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_USER_LAYOUT_SOLUTION_SHARING_CONFIG_LINK` | **源数据实体:** UserLayoutSolutionSharing

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 所属模型 | `belongEntityType` | `CBELONG_ENTITY_TYPE` | 字符串 | 256 | 必填 |  |
| 布局编码 | `layoutCode` | `CLAYOUT_CODE` | 字符串 | 256 | 必填 |  |
| 布局类型 | `layoutType` | `CLAYOUT_TYPE` | 字符串 | 256 | 必填 |  |
| 所属站点 | `site` | `CSITE` | 字符串 | 256 | 必填 |  |
| 配置值 | `configValue` | `CCONFIG_VALUE` | CLOB | - | 无 |  |

### 3.20 用户布局方案分享接受者（UserLayoutSolutionSharingReceiverLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_USER_LAYOUT_SOLUTION_SHARING_RECEIVER_LINK` | **源数据实体:** UserLayoutSolutionSharing

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 接收用户 | `user` | `CUSER` | 用户 | - | 无 | 引用User |
| 接收组织 | `org` | `CORG` | 引用对象 | - | 无 | 引用BizOrg |

### 3.21 WebHook异常（WebHookException）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_WEB_HOOK_EXCEPTION`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 配置ID | `configId` | `CCONFIG_ID` | 长整型 | - | 无 |  |
| 日志ID | `logId` | `CLOG_ID` | 长整型 | - | 无 |  |
| 钩子编码 | `hookCode` | `CHOOK_CODE` | 字符串 | 256 | 无 |  |
| URL地址 | `url` | `CURL` | 字符串 | 1024 | 无 |  |
| 错误信息 | `errorMessage` | `CERROR_MESSAGE` | 字符串 | 4000 | 无 |  |
| 请求载荷 | `requestPayload` | `CREQUEST_PAYLOAD` | CLOB | - | 无 |  |
| 总重试次数 | `totalRetryCount` | `CTOTAL_RETRY_COUNT` | 整型 | - | 无 |  |
| 最后尝试时间 | `lastAttemptTime` | `CLAST_ATTEMPT_TIME` | 日期时间 | - | 无 |  |
| 状态 | `status` | `CSTATUS` | 字符串 | 50 | 无 |  |
| 解决人 | `resolvedBy` | `CRESOLVED_BY` | 长整型 | - | 无 |  |
| 解决时间 | `resolvedTime` | `CRESOLVED_TIME` | 日期时间 | - | 无 |  |
| 解决备注 | `resolveNote` | `CRESOLVE_NOTE` | 字符串 | 1024 | 无 |  |
| 触发人 | `triggeredBy` | `CTRIGGERED_BY` | 长整型 | - | 无 |  |
| 触发人编码 | `triggeredByCode` | `CTRIGGERED_BY_CODE` | 字符串 | 256 | 无 |  |
| 触发人名称 | `triggeredByName` | `CTRIGGERED_BY_NAME` | 字符串 | 256 | 无 |  |

---

## 四、主数据

### 4.1 业务组织（BizOrg）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `IntegrationManaged` | **表名:** `SYS_BIZ_ORG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 编码 | `code` | `CCODE` | 字符串 | 512 | 必填 | |
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 | |
| 备注 | `remark` | `CREMARK` | 字符串 | 1024 | 无 | |
| 业务组织类型 | `bizOrgType` | `CBIZ_ORG_TYPE` | 字符串 | 256 | 必填 |  |
| 序号 | `index` | `CINDEX` | 整型 | - | 无 | |
| 简称 | `shortName` | `CSHORT_NAME` | 字符串 | 256 | 无 | |
| 启用标记 | `enableFlag` | `CENABLE_FLAG` | 布尔 | - | 必填 | |
| 根节点 | `rootId` | `CROOT_ID` | 长整型 | - | 无 | |
| 父节点 | `parentId` | `CPARENT_ID` | 长整型 | - | 无 | |
| 编码路径 | `fullPath` | `CFULL_PATH` | 字符串 | 4000 | 无 | |
| 行政组织 | `orgId` | `CORG_ID` | 长整型 | - | 无 | 引用`Org` |
| 工厂类型 | `factoryType` | `CFACTORY_TYPE` | 枚举 | - | 无 | 引用枚举:factoryType |
| 密级 | `securityLevel` | `CSECURITY_LEVEL` | 枚举 | - | 无 | 引用枚举:securityLevel |

### 4.2 业务组织与用户关系（BizOrgUser）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_BIZ_ORG_USER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 业务组织 | `bizOrgId` | `CBIZ_ORG_ID` | 长整型 | - | 必填 | 引用BizOrg |
| 用户 | `userId` | `CUSER_ID` | 长整型 | - | 必填 | 引用用户 |

### 4.3 物料（Material）

**模型类型:** 业务模型 | **父模型:** `VersionObject` | **接口:** `LifecycleManaged`、`IntegrationManaged` | **表名:** `MOM_MATERIAL`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 |  |
| 物料类别 | `materialType` | `CMATERIAL_TYPE` | 分类 | - | 无 | 引用分类:MaterialType |
| 图号 | `drawingNumber` | `CDRAWING_NUMBER` | 字符串 | 512 | 无 | |
| 型号 | `modelNumber` | `CMODEL_NUMBER` | 字符串 | 512 | 无 | |
| 规格 | `spec` | `CSPEC` | 字符串 | 512 | 无 | |
| 制造类型 | `manufactureType` | `CMANUFACTURE_TYPE` | 枚举 | - | 必填 | 引用枚举:ManufactureType |
| 计量单位 | `measureUnit` | `CMEASURE_UNIT` | 单位 | - | 无 | 引用单位:measureUnit |
| 特性分类 | `featureCategory` | `CFEATURE_CATEGORY` | 枚举 | - | 无 | 引用枚举:FeatureCategory |
| 启用批次标记 | `batchNumberFlag` | `CBATCH_NUMBER_FLAG` | 布尔 | - | 无 | |
| 启用序列号标记 | `serialNumberFlag` | `CSERIAL_NUMBER_FLAG` | 布尔 | - | 无 | |
| 最低库存 | `minStock` | `CMIN_STOCK` | 浮点型 | - | 无 | |
| 安全库存 | `safetyStock` | `CSAFETY_STOCK` | 浮点型 | - | 无 | |
| 有效天数 | `validDays` | `CVALID_DAYS` | 整型 | - | 无 | |
| 经济批量 | `economicBatch` | `CECONOMIC_BATCH` | 浮点型 | - | 无 | |
| 物料阶段 | `materialStage` | `CMATERIAL_STAGE` | 枚举 | - | 无 | 引用枚举:MaterialStage |
| 物料分类 | `materialCategory` | `CMATERIAL_CATEGORY` | 枚举 | - | 必填 | 引用枚举:MaterialCategory |
| 工装类别 | `toolingType` | `CTOOLING_TYPE` | 分类 | - | 无 | 引用分类:ToolingType |
| 单件工装标记 | `singleToolingFlag` | `CSINGLE_TOOLING_FLAG` | 布尔 | - | 无 |  |
| 理论寿命(次) | `theoreticalLifeCycleCount` | `CTHEORETICAL_LIFE_CYCLE_COUNT` | 整型 | - | 无 | |
| 理论寿命(天) | `theoreticalLifeDayCount` | `CTHEORETICAL_LIFE_DAY_COUNT` | 整型 | - | 无 | |
| 一次性工装标记 | `disposableToolingFlag` | `CDISPOSABLE_TOOLING_FLAG` | 布尔 | - | 无 | |

### 4.4 物料与文件关系（MaterialFileLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MATERIAL_FILE_LINK` | **源数据实体:** Material

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 文档对象ID | `documentId` | `CDOCUMENT_ID` | 长整型 | - | 必填 | |
| 文档实体类型 | `docEntityType` | `CDOC_ENTITY_TYPE` | 字符串 | 256 | 必填 | |

### 4.5 物料文件（MaterialFile）

**模型类型:** 业务模型 | **父模型:** `VersionObject` | **接口:** `FactoryManaged`、`FileManaged`、`LifecycleManaged`、`IntegrationManaged` | **表名:** `MOM_MATERIAL_FILE`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 名称 | `name` | `CNAME` | 字符串 | 512 | 无 | |
| 密级 | `securityLevel` | `CSECURITY_LEVEL` | 枚举 | - | 无 | 引用枚举:securityLevel |

*注：文件相关属性由 `FileManaged` 接口提供*

### 4.6 MBOM（MBom）

**模型类型:** 业务模型 | **父模型:** `VersionObject` | **接口:** `FactoryManaged`、`LifecycleManaged`、`IntegrationManaged`| **表名:** `MOM_MBOM`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |

### 4.7 MBOM节点（MBomNodeLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_MBOM_NODE_LINK` | **源数据实体:** MBom

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 父节点 | `parent` | `CPARENT` | 引用对象 | - | 必填 | 引用MBomNode |
| 物料编码 | `materialCode` | `CMATERIAL_CODE` | 字符串 | 256 | 必填 | |
| 物料名称 | `materialName` | `CMATERIAL_NAME` | 字符串 | 256 | 无 | |
| 物料图号 | `materialDrawingNumber` | `CMATERIAL_DRAWING_NUMBER` | 字符串 | 512 | 无 | |
| 物料版本 | `materialVersion` | `CMATERIAL_VERSION` | 字符串 | 256 | 必填 | 格式：V1.0、V2.1等 |
| 物料阶段 | `materialStage` | `CMATERIAL_STAGE` | 枚举 | - | 无 | 引用枚举:MaterialStage |
| 物料类别 | `materialType` | `CMATERIAL_TYPE` | 分类 | - | 必填 | 引用分类:MaterialType |
| 制造类型 | `manufactureType` | `CMANUFACTURE_TYPE` | 枚举 | - | 无 | 引用枚举:ManufactureType |
| 数量 | `qty` | `CQTY` | 浮点型 | - | 必填 | |
| 计量单位 | `measureUnit` | `CMEASURE_UNIT` | 单位 | - | 无 | 引用单位:measureUnit |
| 层级 | `level` | `CLEVEL` | 整型 | - | 必填 | 自动生成 |
| 序号 | `index` | `CINDEX` | 整型 | - | 必填 | 自动生成 |
| 外序号 | `userIndex` | `CUSER_INDEX` | 字符串 | 256 | 无 | 外部指定 |
| 引用物料 | `referenceMaterial` | `CREFERENCE_MATERIAL` | 引用对象 | - | 无 | 引用Material |
| 全路径 | `fullPath` | `CFULL_PATH` | 字符串 | 1024 | 必填 | CID全路径 |

### 4.8 工序库（Process）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:**  `SecurityManaged`| **表名:** `MOM_PROCESS`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 | |
| 工序类型 | `processType` | `CPROCESS_TYPE` | 枚举 | 256 | 必填 | 引用枚举:ProcessType |
| 工序内容 | `content` | `CCONTENT` | 字符串 | 512 | 无 | |
| 工作中心 | `workCenter` | `CWORK_CENTER` | 引用对象 | - | 无 | 引用WorkCenter |
| 定额准备时间 | `preparationTime` | `CPREPARATION_TIME` | 浮点型 | - | 必填 | 默认为0 |
| 定额加工时间 | `processingTime` | `CPROCESSING_TIME` | 浮点型 | - | 必填 | 默认为0 |
| 时间单位 | `timeUnit` | `CTIME_UNIT` | 单位 | - | 必填 | 引用单位:timeUnit |
| 执行标记 | `executionFlag` | `CEXECUTION_FLAG` | 布尔 | - | 无 | |
| 产出比 | `productivityRate` | `CPRODUCTIVITY_RATE` | 整型 | - | 无 | |
| 备注 | `remark` | `CREMARK` | 字符串 | 256 | 无 | |
| 工序专业类型 | processSpecialty | CPROCESS_SPECIALTY | 枚举 | - | 无 | 引用枚举:FactoryType |
| 工厂组织 | `bizOrg` | `CBIZ_ORG` | 引用对象 | - | 无 | 引用BizOrg |

### 4.9 工序库与资质等级关系（ProcessQualificationLevelLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_PROCESS_QUALIFICATION_LEVEL_LINK` | **源数据实体:** Process

*注：1.15批次不建立该数据模型*

| 属性中文名称 | 属性英文名称         | 数据库列名             | 数据类型 | 长度 | 约束 | 说明                   |
| ------------ | -------------------- | ---------------------- | -------- | ---- | ---- | ---------------------- |
| 资质等级     | `qualificationLevel` | `CQUALIFICATION_LEVEL` | 引用对象 | -    | 必填 | 引用QualificationLevel |

### 4.10 资质等级（QualificationLevel）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:** `SecurityManaged`、`IntegrationManaged` | **表名:** `MOM_QUALIFICATION_LEVEL`

| 属性中文名称   | 属性英文名称       | 数据库列名           | 数据类型 | 长度 | 约束 | 说明           |
| -------------- | ------------------ | -------------------- | -------- | ---- | ---- | -------------- |
| 名称           | `name`             | `CNAME`              | 字符串   | 512  | 必填 |                |
| 资质           | `qualification`    | `CQUALIFICATION`     | 枚举     | 256  | 必填 | 引用WorkCenter |
| 资质等级值     | `value`            | `CVALUE`             | 整型     | 11   | 无   |                |
| 资质证书有效期 | `expiryDate`       | `CEXPIRY_DATE`       | 日期     | -    | 无   |                |
| 发证机关       | `issuingAuthority` | `CISSUING_AUTHORITY` | 字符串   | -    | 必填 |                |

### 4.11 资质等级与用户（QualificationLevelUser）

**模型类型:** 业务模型 | **父模型:** `BaseObject` | **接口:**  `SecurityManaged`| **表名:** `MOM_QUALIFICATION_LEVEL_USER`

| 属性中文名称 | 属性英文名称         | 数据库列名             | 数据类型 | 长度 | 约束 | 说明                                               |
| ------------ | -------------------- | ---------------------- | -------- | ---- | ---- | -------------------------------------------------- |
| 资质等级     | `qualificationLevel` | `CQUALIFICATION_LEVEL` | 引用对象 | 512  | 必填 | 引用:QualificationLevel                            |
| 用户         | `user`               | `CUSER`                | 用户     | 256  | 必填 |                                                    |
| 生效日期     | `effectiveDate`      | `CEFFECTIVE_DATE`      | 日期     | -    | 无   |                                                    |
| 失效日期     | `expiryDate`         | `CEXPIRY_DATE`         | 日期     | -    | 无   |                                                    |
| 状态         | `status`             | `CSTATUS`              | 枚举     | -    | 无   | 引入枚举：QualificationRelationStatus 默认（有效） |

### 4.12 工艺路线（Routing）

**模型类型:** 业务模型 | **父模型:** `VersionObject` | **接口:** `FactoryManaged`、`LifecycleManaged`、`IntegrationManaged` | **表名:** `MOM_ROUTING`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 | |
| 工厂组织 | `bizOrg` | `CBIZ_ORG` | 引用对象 | - | 必填 | 引用BizOrg |
| 所属工厂 | `factory` | `CFACTORY` | 引用对象 | - | 必填 | 引用BizOrg |
| 工艺类型 | `routingType` | `CROUTING_TYPE` | 枚举 | 256 | 必填 | 引用枚举:RoutingType |
| 工艺专业 | `processSpecialty` | `CPROCESS_SPECIALTY` | 枚举 | 256 | 无 | 引用枚举:ProcessSpecialty |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 无 | 引用Material |

### 4.13 工艺路线工序（RoutingProcessLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_ROUTING_PROCESS_LINK` | **源数据实体:** Routing

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束  | 说明                                        |
|--------|-------------|-----------|---------|------|-----|-------------------------------------------|
| 工序号    | `processNum` | `CPROCESS_NUM` | 字符串 | 256 | 必填  |                                           |
| 工序名称   | `processName` | `CPROCESS_NAME` | 字符串 | 512 | 必填  |                                           |
| 工序类型   | `processType` | `CPROCESS_TYPE` | 枚举 | 256 | 必填  | 引用枚举:ProcessType                          |
| 工序内容   | `content` | `CCONTENT` | 字符串 | 1024 | 必填  |                                           |
| 序号     | `index` | `CINDEX` | 整型 | - | 必填  |                                           |
| 工作中心   | `workCenter` | `CWORK_CENTER` | 引用对象 | - | 无   | 引用WorkCenter                              |
| 定额准备时间 | `preparationTime` | `CPREPARATION_TIME` | 浮点型 | - | 必填  | 默认为0                                      |
| 定额加工时间 | `processingTime` | `CPROCESSING_TIME` | 浮点型 | - | 必填  | 默认为0                                      |
| 时间单位   | `timeUnit` | `CTIME_UNIT` | 单位 | - | 必填  | 引用单位:timeUnit       |
| 执行标记   | `executionFlag` | `CEXECUTION_FLAG` | 布尔 | - | 无   |                                           |
| 产出比    | `productivityRate` | `CPRODUCTIVITY_RATE` | 整型 | - | 无   | 1.切件比例；2.协同排产业务:上级物料和子级物料比例               |
| 产出物料   | `producedMaterial` | `CPRODUCED_MATERIAL` | 引用对象 | - | 无   | 引用Material，协同排产业务增加                       |
| 主制单位   | `masterManuOrg` | `CMASTER_MANU_ORG` | 引用对象 | - | 无   | 引用BizOrg，协同排产业务增加                         |
| 前置工序   | `prevProcess` | `CPREV_PROCESS` | 字符串 | 512 | 无   | 冗余字段，格式：工序号(接续关系)，多个用逗号分隔，如：10(ES),20(SS) |



### 4.14 工艺路线物料（RoutingMaterialLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_ROUTING_MATERIAL_LINK` | **源数据实体:** Routing

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 工序号 | `processNum` | `CPROCESS_NUM` | 字符串 | 256 | 无 | |
| 物料 | `material` | `CMATERIAL` | 引用对象 | - | 必填 | 引用Material |
| 数量 | `qty` | `CQTY` | 浮点型 | - | 无 | |

### 4.15 工艺路线工序序列（RoutingSequenceLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_ROUTING_SEQUENCE_LINK` | **源数据实体:** Routing

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 当前工序号 | `processNum` | `CPROCESS_NUM` | 字符串 | 256 | 必填 | |
| 上道工序号 | `prevProcessNum` | `CPREV_PROCESS_NUM` | 字符串 | 256 | 必填 | 首道工序用大写S表示 |
| 接续关系 | `timeConstraintMethod` | `CTIME_CONSTRAINT_METHOD` | 枚举 | - | 必填 | 引用枚举:continuationType |

### 4.16 工艺路线与资质等级关系（RoutingQualificationLevelLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_ROUTING_QUALIFICATION_LEVEL_LINK` | **源数据实体:** Routing

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 工序号 | `processNum` | `CPROCESS_NUM` | 字符串 | 256 | 必填 | |
| 资质等级 | `qualificationLevel` | `CQUALIFICATION_LEVEL` | 引用对象 | - | 必填 | 引用QualificationLevel |

### 4.17 工艺路线与文件关系（RoutingFileLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_ROUTING_FILE_LINK` | **源数据实体:** Routing

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 工序号 | `processNum` | `CPROCESS_NUM` | 字符串 | 256 | 无 | |
| 文档对象ID | `documentId` | `CDOCUMENT_ID` | 长整型 | - | 必填 | |
| 文档实体类型 | `docEntityType` | `CDOC_ENTITY_TYPE` | 字符串 | 256 | 必填 | |

### 4.14 工艺路线工序工装清单（RoutingToolingLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_ROUTING_TOOLING_LINK` | **源数据实体:** Routing

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 工装 | `tooling` | `CTOOLING` | 引用对象 | - | 必填 | 引用Material（工装定义） |
| 工序号 | `processNum` | `CPROCESS_NUM` | 字符串 | 256 | 无 | |
| 需求数量 | `qty` | `CQTY` | 浮点型 | - | 无 | |

### 4.16 工艺文件（RoutingFile）

**模型类型:** 业务模型 | **父模型:** `VersionObject` | **接口:** `FileManaged`、`IntegrationManaged` | **表名:** `MOM_ROUTING_FILE`

*注：文件相关属性由 `FileManaged` 接口提供*

### 4.19 工作中心（WorkCenter）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`IntegrationManaged` | **表名:** `MOM_WORK_CENTER`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 |  |
| 类型 | `workCenterType` | `CWORK_CENTER_TYPE` | 枚举 | - | 必填 | 引用枚举:WorkCenterType |
| 分类 | `workCenterCategory` | `CWORK_CENTER_CATEGORY` | 枚举 | - | 必填 | 引用枚举:WorkCenterCategory |

### 4.20 工作中心与设备关系（WorkCenterEquipLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_WORK_CENTER_EQUIP_LINK` | **源数据实体:** WorkCenter

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 设备 | `equip` | `CEQUIP` | 引用对象 | - | 必填 | 引用Equip |

### 4.21 工作中心与用户关系（WorkCenterUserLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_WORK_CENTER_USER_LINK` | **源数据实体:** WorkCenter

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 用户 | `user` | `CUSER` | 引用对象 | - | 必填 | 引用User |

### 4.22 工作中心与供应商关系（WorkCenterSupplierLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_WORK_CENTER_SUPPLIER_LINK` | **源数据实体:** WorkCenter

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 供应商 | `supplier` | `CSUPPLIER` | 引用对象 | - | 必填 | 引用BizOrg |

### 4.23 工作中心仓储配置（WorkCenterWarehouseConfig）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_WORK_CENTER_WAREHOUSE_CONFIG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 编码 | `code` | `CCODE` | 字符串 | 512 | 必填 | |
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 | |
| 配置展示类型 | `showType` | `CSHOW_TYPE` | 字符串 | 128 | 无 | 取值范围：item\|group |
| 描述 | `description` | `CDESCRIPTION` | 字符串 | 1024 | 无 | |
| 组件类型 | `compType` | `CCOMP_TYPE` | 字符串 | 256 | 无 | 取值范围：TEXT\|NUM |
| 组件配置 | `compConfig` | `CCOMP_CONFIG` | CLOB | - | 无 | |
| 父节点 | `parent` | `CPARENT` | 字符串 | 256 | 无 | |
| 序号 | `index` | `CINDEX` | 整型 | - | 无 | |
| 默认值 | `defaultValue` | `CDEFAULT_VALUE` | 字符串 | 4000 | 无 | 单值以字符串存储，多值以JSON存储 |

### 4.24 工作中心仓储配置值（WorkCenterWarehouseConfigValue）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_WORK_CENTER_WAREHOUSE_CONFIG_VALUE`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 所属组织 | `bizOrg` | `CBIZ_ORG` | 引用对象 | - | 无 | 引用BizOrg，0表示工厂级别 |
| 工作中心 | `workCenter` | `CWORK_CENTER` | 引用对象 | - | 无 | 引用WorkCenter |
| 库房 | `warehouse` | `CWAREHOUSE` | 引用对象 | - | 无 | 引用Warehouse |
| 编码 | `code` | `CCODE` | 字符串 | 256 | 必填 | |
| 值 | `value` | `CVALUE` | CLOB | - | 必填 | |

### 4.25 设备（Equip）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged`、`IntegrationManaged` | **表名:** `MOM_EQUIP`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 | |
| 型号规格 | `modelSpec` | `CMODEL_SPEC` | 字符串 | 512 | 无 | |
| 瓶颈资源 | `bottleneckFlag` | `CBOTTLENECK_FLAG` | 布尔 | - | 无 | |

### 4.26 设备与用户关系（EquipUserLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_EQUIP_USER_LINK` | **源数据实体:** Equip

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 用户 | `user` | `CUSER` | 用户 | - | 必填 | 引用User |

### 4.27 库房（Warehouse）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged` | **表名:** `MOM_WAREHOUSE`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 | |
| 工厂组织 | `bizOrg` | `CBIZ_ORG` | 引用对象 | - | 必填 | 引用BizOrg |
| 所属工厂 | `factory` | `CFACTORY` | 引用对象 | - | 必填 | 引用BizOrg |
| 库房业务类型 | `warehouseType` | `CWAREHOUSE_TYPE` | 枚举 | 256 | 必填 | 引用枚举:WarehouseType |
| 库房作业模式 | `operationMode` | `COPERATION_MODE` | 枚举 | - | 无 | 引用枚举:WarehouseOperationMode |
| 有效期预警提前期(天) | `expiryWarningDays` | `CEXPIRY_WARNING_DAYS` | 整型 | - | 无 | |
| 呆滞物料预警时长(年) | `dormantMaterialWarningYears` | `CDORMANT_MATERIAL_WARNING_YEARS` | 整型 | - | 无 | |

### 4.28 库位（WarehouseLocation）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FactoryManaged` | **表名:** `MOM_WAREHOUSE_LOCATION`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 | |
| 工厂组织 | `bizOrg` | `CBIZ_ORG` | 引用对象 | - | 必填 | 引用BizOrg |
| 所属工厂 | `factory` | `CFACTORY` | 引用对象 | - | 必填 | 引用BizOrg |
| 库房 | `warehouse` | `CWAREHOUSE` | 引用对象 | - | 必填 | 引用Warehouse |
| 启用标记 | `enableFlag` | `CENABLE_FLAG` | 布尔 | - | 无 | |

### 4.29 附件（Attachment）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** `FileManaged` | **表名:** `MOM_ATTACHMENT`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 文件名 | `fileName` | `CFILE_NAME` | 字符串 | 512 | 无 | |
| 编码 | `code` | `CCODE` | 字符串 | 512 | 无 | |
| 备注 | `remark` | `CREMARK` | 字符串 | 1024 | 无 | |
| 密级 | `securityLevel` | `CSECURITY_LEVEL` | 枚举 | - | 无 | 引用枚举:securityLevel |

### 4.30 对象与附件关系（ObjectAttachmentRel）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `MOM_OBJECT_ATTACHMENT_REL`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 对象ID | `objectId` | `COBJECT_ID` | 长整型 | - | 必填 | |
| 对象实体类型 | `objectEntityType` | `COBJECT_ENTITY_TYPE` | 字符串 | 128 | 必填 | |
| 附件 | `attachment` | `CATTACHMENT` | 引用对象 | - | 必填 | 引用Attachment |
| 备注 | `remark` | `CREMARK` | 字符串 | 512 | 无 | |

### 4.31 工艺路线工步（RoutingProcessStepLink）

**模型类型:** 系统模型 | **父模型:** `GenericLink` | **接口:** 无 | **表名:** `MOM_ROUTING_PROCESS_STEP_LINK` | **源数据实体:** Routing

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 工序号 | `processNum` | `CPROCESS_NUM` | 字符串 | 256 | 无 | |
| 工步序号 | `stepNum` | `CSTEP_NUM` | 字符串 | 36 | 必填 | 唯一标识 |
| 工步名称 | `stepName` | `CSTEP_NAME` | 字符串 | 256 | 必填 | |
| 工步内容 | `stepContent` | `CSTEP_CONTENT` | 字符串 | 512 | 无 | |
| 序号     | `index` | `CINDEX` | 整型 | - | 必填  |                                           |

### 4.32 异常类别（AbnormalCategory）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** 无 | **表名:** `MOM_ABNORMAL_CATEGORY`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 流程标识 | `flowCode` | `CFLOW_CODE` | 字符串 | 256 | 无 |  |
| 是否预定义 | `predefinedFlag` | `CPREDEFINED_FLAG` | 布尔 | - | 必填 |  |
| 编码 | `code` | `CCODE` | 字符串 | 512 | 必填 |  |
| 密级 | `securityLevel` | `CSECURITY_LEVEL` | 枚举 | 256 | 必填 | 引用枚举:securityLevel |
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 |  |
| 备注 | `remark` | `CREMARK` | 字符串 | 1024 | 无 |  |

### 4.33 异常描述库（AbnormalDescription）

**模型类型:** 业务模型 | **父模型:** `BusinessObject` | **接口:** 无 | **表名:** `MOM_ABNORMAL_DESCRIPTION`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 异常类别 | `abnormalCategory` | `CABNORMAL_CATEGORY` | 引用对象 | - | 必填 | 引用AbnormalCategory |
| 异常描述 | `abnormalDescription` | `CABNORMAL_DESCRIPTION` | 字符串 | 4000 | 必填 |  |
| 名称 | `name` | `CNAME` | 字符串 | 512 | 无 |  |
| 编码 | `code` | `CCODE` | 字符串 | 512 | 必填 |  |
| 备注 | `remark` | `CREMARK` | 字符串 | 1024 | 无 |  |
| 密级 | `securityLevel` | `CSECURITY_LEVEL` | 枚举 | 256 | 必填 | 引用枚举:securityLevel |

---

## 五、监控管理

### 5.1 业务日志（SysLog）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_LOG`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 操作人 | `operator` | `COPERATOR` | 长整型 | - | 必填 | |
| 操作人编码 | `operatorCode` | `COPERATOR_CODE` | 字符串 | 256 | 必填 | |
| 操作人名称 | `operatorName` | `COPERATOR_NAME` | 字符串 | 256 | 必填 | |
| 操作时间 | `operatorTime` | `COPERATOR_TIME` | 日期时间 | - | 必填 | |
| 操作员安全等级 | `securityLevel` | `CSECURITY_LEVEL` | 字符串 | 256 | 无 | |
| 操作员IP | `operatorIp` | `COPERATOR_IP` | 字符串 | 256 | 无 | |
| 日志类型 | `logType` | `CLOG_TYPE` | 字符串 | 256 | 必填 | |
| 操作 | `action` | `CACTION` | 字符串 | 256 | 无 | |
| 操作内容 | `actionContent` | `CACTION_CONTENT` | CLOB | - | 无 | |
| 审计状态 | `auditStatus` | `CAUDIT_STATUS` | 整型 | 256 | 无 | 待审计:0\|已审计:1 |
| 审计人 | `auditor` | `CAUDITOR` | 长整型 | - | 无 | |
| 审计意见 | `auditResult` | `CAUDIT_RESULT` | 字符串 | 256 | 无 | 通过:10\|不通过:20 |
| 审计时间 | `auditTime` | `CAUDIT_TIME` | 日期时间 | - | 无 | |
| 审计人IP | `auditIp` | `CAUDIT_IP` | 字符串 | 256 | 无 | |
| 审计说明 | `auditRemark` | `CAUDIT_REMARK` | 字符串 | 1024 | 无 | |
| 日志审计编号 | `auditNo` | `CAUDIT_NO` | 字符串 | 256 | 无 | |
| 审计人编码 | `auditorCode` | `CAUDITOR_CODE` | 字符串 | 256 | 无 | |
| 审计人名称 | `auditorName` | `CAUDITOR_NAME` | 字符串 | 256 | 无 | |

### 5.2 图像文件分类（ImageFileGroup）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_IMAGE_FILE_GROUP`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 编码 | `code` | `CCODE` | 字符串 | 512 | 必填 | |
| 名称 | `name` | `CNAME` | 字符串 | 512 | 必填 | |
| 类型 | `type` | `CTYPE` | 字符串 | 256 | 必填 | |
| 父节点 | `parentId` | `CPARENT_ID` | 长整型 | - | 无 | |

### 5.3 图像文件（ImageFile）

**模型类型:** 系统模型 | **父模型:** `BaseObject` | **接口:** 无 | **表名:** `SYS_IMAGE_FILE`

| 属性中文名称 | 属性英文名称 | 数据库列名 | 数据类型 | 长度 | 约束 | 说明 |
|-------------|-------------|-----------|---------|------|------|------|
| 文件组 | `groupCode` | `CGROUP_CODE` | 字符串 | 512 | 无 | |
| 文件名称 | `fileName` | `CFILE_NAME` | 字符串 | 256 | 无 | |
| 文件存储桶名称 | `bucketName` | `CBUCKET_NAME` | 字符串 | 512 | 无 | |
| 文件夹名称 | `dir` | `CDIR` | 字符串 | 512 | 无 | |
| 原始文件名 | `original` | `CORIGINAL` | 字符串 | 512 | 无 | |
| 文件类型 | `type` | `CTYPE` | 字符串 | 50 | 无 | |
| MD5 | `md5` | `CMD5` | 字符串 | 50 | 无 | |
| 文件大小 | `size` | `CSIZE` | 长整型 | - | 无 | |

---

## 变更记录

| 日期         | 版本   | 变更内容                                                    | 变更人 |
|------------|------|---------------------------------------------------------|--------|
| 2026-04-22 | v1.14 | 根据 `km-mom-platform-integration-managed-analysis.md`，为最终确认要集成的模型补充 `IntegrationManaged` 接口 | 危放 |
| 2026-04-22 | v1.13 | 删除 `4.15 主制辅制工艺关系`、`4.30 出勤模式`、`4.31 主制辅制工艺关系` 章节，并顺延主数据章节编号 | 危放 |
| 2026-03-18 | v1.12 | 将 `ServerSideActionConfig` 从认证授权章节调整到 `ServerSideLayoutConfig` 后，并顺延系统配置章节编号 | Codex |
| 2026-03-18 | v1.11 | 删除 `CodeRule`、`CodeRuleSegment` 章节，并顺延系统配置章节编号 | Codex |
| 2026-03-18 | v1.10 | 删除 `OrgPerson`、`Feature`、`FavoriteFeature`、`RoleFeaturePermission`、`LayoutModule`、`OrgConfigActivation`、`Bom`、`BizOrgPerson`、`BomLink` 章节，并顺延相关编号 | Codex |
| 2026-03-18 | v1.9 | 删除 `Person` 模型章节，并顺延认证授权章节编号 | Codex |
| 2026-03-18 | v1.8 | 删除 `3.20 服务端布局配置` 及表名以 `DM_` 开头的内部模型定义，顺延系统配置章节编号 | Codex |
| 2026-03-18 | v1.7 | 基于 `KMMOM_DM_20260317100714.dm.json` 补齐 `sys`、`mds` 模块缺失模型定义，并修正文档中个别错位章节 | Codex |
| 2025-12-17 | v1.0 | 整合主数据、系统管理、业务配置三个数据模型文档，统一格式规范，按平台模块重新组织结构              | 王晴 |
| 2025-12-29 | v1.1 | 修改文档工具DocTool模型属性内置标记重命名为sysFlag                        | 危放  |
| 2025-01-06 | v1.2 | 增加工艺路线工步表RoutingProcessStepLink,删除工序表中无用的检验标记,工序表增加前置工序 | 危放  |
| 2026-01-14 | v1.3 | 删除工序和工序链接中的工序简码字段；优化工序链接字段约束和命名；新增工步链接序号字段 | 危放  |
| 2026-01-23 | v1.4 | 基于元数据定义同步更新文档属性：补充GenericLink子模型source属性、补充设备/工艺路线/库房/库位等模型缺失属性、修正数据类型、删除文档中多余属性 | 危放  |
| 2026-01-26 | v1.5 | 修复引用枚举类型编码，确保与数据库定义一致| 危放  |
| 2026-03-09 | v1.6 | 修正工艺文件（RoutingFile）模型接口定义，移除FactoryManaged，仅保留FileManaged | 危放  |
| 2026-03-18 | v1.7 | 添加资质等级模型，及资质等级与用户关系模型 | 李鸿坤 |
| 2026-03-06 | v1.6 | 新增扩展功能（ExtensionFeature）实体定义，用于支持模块自定义扩展功能按钮 | 危放  |
