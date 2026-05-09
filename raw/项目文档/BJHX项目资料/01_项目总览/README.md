# BJHX 项目过程记录

> 本仓库记录北京 HX MOM 系统项目的全过程资产，包括沟通、需求、问题、进度、部署等非代码类文档。

## 使用入口

- 仓库维护规则：[`维护规则.md`](E:/lld-workspace/mom3_projects/BJHX/BJHX_PROCESS/维护规则.md)
- 项目总控台账：[`项目总控台账.md`](E:/lld-workspace/mom3_projects/BJHX/BJHX_PROCESS/项目总控台账.md)
- 需求主索引：[`02_需求与方案/requirements/index.md`](E:/lld-workspace/mom3_projects/BJHX/BJHX_PROCESS/02_需求与方案/requirements/index.md)
- 风险台账：[`03_问题与决策/risk_register.md`](E:/lld-workspace/mom3_projects/BJHX/BJHX_PROCESS/03_问题与决策/risk_register.md)
- 行动项台账：[`03_问题与决策/action_register.md`](E:/lld-workspace/mom3_projects/BJHX/BJHX_PROCESS/03_问题与决策/action_register.md)
- 决策索引：[`03_问题与决策/decision_index.md`](E:/lld-workspace/mom3_projects/BJHX/BJHX_PROCESS/03_问题与决策/decision_index.md)
- 里程碑台账：[`04_进度与里程碑/milestones/index.md`](E:/lld-workspace/mom3_projects/BJHX/BJHX_PROCESS/04_进度与里程碑/milestones/index.md)
- 清单管控：[`06_清单管控/说明.md`](E:/lld-workspace/mom3_projects/BJHX/BJHX_PROCESS/06_清单管控/说明.md)

## 目录结构

```
BJHX_PROCESS/
├── README.md               # 仓库入口与导航
├── 项目概况.md             # 项目背景、现状架构、目标架构、组织角色
├── 项目总控台账.md         # 项目级驾驶舱与关键状态摘要
├── 维护规则.md             # 仓库维护规则与状态同步要求
│
├── 01_沟通与会议/          # 会议纪要、沟通记录
│   ├── meetings/           # 正式会议纪要（命名格式：YYYYMMDD_主题）
│   └── communications/     # 非正式沟通（邮件要点、通话记录等）
│
├── 02_需求与方案/          # 业务需求与技术方案
│   ├── requirements/       # 需求文档、业务流程说明
│   └── solutions/          # 技术方案、架构设计、选型决策
│
├── 03_问题与决策/          # 问题追踪与重要决策
│   ├── issues/             # 问题记录及解决方案（命名格式：YYYYMMDD_问题简述）
│   └── decisions/          # 重要决策记录（记录背景、选项、结论、原因）
│
├── 04_进度与里程碑/        # 项目进度跟踪
│   ├── weekly/             # 周报、阶段总结
│   └── milestones/         # 里程碑记录（关键节点成果）
│
├── 05_部署与运维/          # 部署方案与运维记录
│   ├── deployment/         # 部署方案、服务器资源、环境配置
│   └── operations/         # 运维记录、巡检报告、故障处理
│
├── 06_清单管控/            # 在线开发任务清单快照与规则说明
│   ├── 开发任务跟踪表/     # 在线任务表导出的 Excel 快照（命名格式：BJHX-MOM项目开发任务跟踪表_YYYY-MM-DD_HHMM.xlsx）
│   └── 说明.md             # 清单范围、快照规则、需求映射说明
```

## 项目背景

详见 [项目概况.md](项目概况.md)

## 维护原则

- 先更新主台账，再补充明细文档。
- 会议纪要记录事实，状态变化必须同步到对应主台账。
- 需求、风险、行动项、决策、里程碑均采用固定状态枚举，禁止自由命名。
- 在线开发任务清单导出的 Excel 快照统一归档到 `06_清单管控/开发任务跟踪表/`，按导出时间新增快照，不覆盖历史。
- 人工或 AI 修改文档后，必须检查是否需要同步更新主索引。

## 文件命名规范

| 类型     | 格式                | 示例                              |
| -------- | ------------------- | --------------------------------- |
| 会议纪要 | `YYYYMMDD_主题`     | `20260419_出差前事项对齐会议纪要` |
| 问题记录 | `YYYYMMDD_问题简述` | `20260420_批量报工功能异常`       |
| 周报     | `YYYYMMDD_周报`     | `20260421_周报`                   |
| 决策记录 | `YYYYMMDD_决策主题` | `20260421_高可用方案选型`         |
| 任务清单快照 | `BJHX-MOM项目开发任务跟踪表_YYYY-MM-DD_HHMM.xlsx` | `BJHX-MOM项目开发任务跟踪表_2026-04-30_1730.xlsx` |
