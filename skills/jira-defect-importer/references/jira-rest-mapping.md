# Jira REST 导入参考

## 代码来源

下列信息来自 `D:\07_Git\km-rde`：

1. `backend/km-rde/km-rde-biz/src/main/java/com/kmsoft/rde/biz/infra/client/JiraClient.java`
2. `backend/km-rde/km-rde-api/src/main/java/com/kmsoft/rde/api/constant/JiraConstants.java`
3. `backend/km-rde/km-rde-api/src/main/java/com/kmsoft/rde/api/constant/JiraFieldConstants.java`
4. `backend/km-rde/scripts/db.sql`

## 已确认的信息

### 认证方式

- `JiraClient.createAuthHeaders()` 使用 Basic Auth。
- 参数编码来自 `db.sql` 与 `JiraConstants.java`：
  - `jira.apiBaseUrl`
  - `jira.projectKey`
  - `jira.username`
  - `jira.password`

### 已确认的 Jira REST 路径

- 查项目看板 Sprint：`GET /rest/agile/1.0/board/{boardId}/sprint`
- 查单个 Sprint 明细：`GET /rest/agile/1.0/sprint/{sprintId}`
- 搜索：`POST /rest/api/2/search`
- 查流转：`GET /rest/api/2/issue/{issueKey}/transitions`
- 执行流转：`POST /rest/api/2/issue/{issueKey}/transitions`
- 更新问题：`PUT /rest/api/2/issue/{issueKey}`
- 添加评论：`POST /rest/api/2/issue/{issueKey}/comment`
- 查字段：`GET /rest/api/2/field`

### 创建缺陷接口

- `km-rde` 中没有直接封装“创建缺陷”方法。
- 本 skill 使用标准 Jira Server/Data Center REST v2 创建接口：
  - `POST /rest/api/2/issue`
- 这是基于同一套 `/rest/api/2/...` 常量和 `JiraClient` 认证方式做出的保守推断。

### 已确认的自定义字段 ID

| 业务字段 | Jira 字段 |
| --- | --- |
| 责任人 | `customfield_10257` |
| 缺陷严重程度 | `customfield_10605` |
| 缺陷来源 | `customfield_10604` |
| 缺陷引入阶段 | `customfield_11806` |
| 缺陷产生者 | `customfield_11238` |
| 测试责任人 | `customfield_11002` |

## 未在 km-rde 中确认的字段

下列字段在当前代码中未发现固定 ID，导入前应先用 `fields` 子命令查询：

- `模块`
- `对用户的影响程度`
- `Sprint`
- `影响范围分析`

## CSV 到 Jira 的默认映射

| CSV 列 | 默认 Jira 映射 |
| --- | --- |
| 问题类型 | `fields.issuetype.name` |
| 概要 | `fields.summary` |
| 描述 | `fields.description` |
| 优先级 | `fields.priority.name` |
| 到期日 | `fields.duedate` |
| 使用的版本 | `fields.versions[].name` |
| 修复的版本 | `fields.fixVersions[].name` |
| 责任人 | `field_map["责任人"]` |
| 测试责任人 | `field_map["测试责任人"]` |
| 缺陷产生者 | `field_map["缺陷产生者"]` |
| 缺陷严重程度 | `field_map["缺陷严重程度"]` |
| 模块 | `field_map["模块"]` |
| 对用户的影响程度 | `field_map["对用户的影响程度"]` |
| Sprint | `field_map["Sprint"]` |
| 影响范围分析 | `field_map["影响范围分析"]`，未配置时可追加到描述 |
| 状态 | 创建后按 transition 处理，不直接进入 create payload |

## 配置文件约定

最小配置：

```json
{
  "api_base_url": "http://jira-host:8080",
  "project_key": "KMMOM3",
  "project_code": "KMMOM",
  "board_id": "149",
  "username": "your-jira-user",
  "password": "your-jira-password"
}
```

或使用环境变量：

```json
{
  "api_base_url": "http://jira-host:8080",
  "project_key": "KMMOM3",
  "project_code": "KMMOM",
  "board_id": "149",
  "username_env": "JIRA_USERNAME",
  "password_env": "JIRA_PASSWORD"
}
```

优先级如下：

1. 命令行 `--username` / `--password`
2. 命令行 `--username-env` / `--password-env`
3. 配置文件 `username` / `password`
4. 配置文件 `username_env` / `password_env`

若 `board_id` 未写入配置，可额外提供：

```json
{
  "project_code": "KMMOM",
  "km_rde_db_sql_path": "D:/07_Git/km-rde/backend/km-rde/scripts/db.sql"
}
```

脚本会尝试从 `km-rde` 项目参数 SQL 中读取 `jira.boardId`。

常用扩展项：

```json
{
  "user_identity_key": "name",
  "default_issue_type": "缺陷",
  "default_create_status": "缺陷编制中",
  "append_impact_analysis_to_description": true,
  "strict_custom_fields": false,
  "field_map": {
    "责任人": "customfield_10257",
    "测试责任人": "customfield_11002",
    "缺陷产生者": "customfield_11238",
    "缺陷严重程度": "customfield_10605",
    "缺陷来源": "customfield_10604",
    "缺陷引入阶段": "customfield_11806",
    "模块": "",
    "对用户的影响程度": "",
    "Sprint": "",
    "影响范围分析": ""
  },
  "defaults": {
    "缺陷来源": "测试",
    "缺陷引入阶段": "测试阶段"
  },
  "transition_name_map": {
    "缺陷分派中": "分派"
  },
  "extra_fields": {
    "customfield_99999": {
      "value": "实例特有必填项"
    }
  }
}
```

## 修改 Jira 登录用户

如果只是临时切换登录用户，优先用命令行覆盖，不要改模板文件：

```bash
python skills/jira-defect-importer/scripts/import_jira_defects.py import --config jira-import-config.json --csv defects.csv --dry-run --username wangqing --password-env JIRA_PASSWORD
```

如果希望长期固定某个账号，直接修改配置文件里的 `username`，或修改 `username_env` 指向的环境变量名。

## 读取项目 Sprint 并推荐缺陷 Sprint

默认命令：

```bash
python skills/jira-defect-importer/scripts/import_jira_defects.py sprints --config jira-import-config.json --report sprint_catalog.json
```

输出内容包括：

1. `sprints`：项目看板读出的 Sprint 列表
2. `suggested_sprint`：按当前日期推荐的 Sprint
3. `suggestion_reason`：推荐原因

推荐规则：

1. 若当前日期落在某个 Sprint 的 `start_date ~ end_date` 内，优先选该 Sprint。
2. 若当前日期早于所有已知 Sprint，选最近即将开始的 Sprint。
3. 若当前日期晚于所有已知 Sprint，选最近结束的 Sprint。

生成的 `sprint_catalog.json` 可以直接给 `defect-report-generator --sprint-catalog` 使用。

## 常见失败原因

### `HTTP 400`

优先检查：

1. 必填自定义字段是否缺失
2. 自定义字段 ID 是否写错
3. 账号字段是否应使用 `name` 还是 `accountId`
4. `Sprint` 字段是否允许在 create 时写入
5. transition 名称是否与目标状态同名

### 创建成功但状态不对

不要假设 Jira 创建时支持直接写 `状态`。应：

1. 创建缺陷
2. 查询该缺陷可用 transition
3. 根据 `transition_name_map` 或 `transition_id_map` 做流转

### 字段没有落进去

如果脚本报告某列“未配置字段 ID 已跳过”，先运行：

```bash
python skills/jira-defect-importer/scripts/import_jira_defects.py fields --config jira-import-config.json --names 模块 对用户的影响程度 Sprint 影响范围分析
```
