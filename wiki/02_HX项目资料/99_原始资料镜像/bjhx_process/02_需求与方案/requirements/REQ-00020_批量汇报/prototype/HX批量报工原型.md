---
title: 原始资料-项目文档-HX批量报工原型
type: manual
status: active
tags:
  - testing
  - raw
  - mirror
  - auto-ingest
summary: 自动镜像 wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/requirements/REQ-00020_批量汇报/prototype/HX批量报工原型.html，作为当前 legacy wiki 结构下的安全入库入口。
source:
  - wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/requirements/REQ-00020_批量汇报/prototype/HX批量报工原型.html
updated: 2026-05-27
---

<!-- raw-to-wiki-ingest:auto -->

# 原始资料-项目文档-HX批量报工原型

## 来源说明

- 原始路径：`wiki/02_HX项目资料/99_原始资料/bjhx_process/02_需求与方案/requirements/REQ-00020_批量汇报/prototype/HX批量报工原型.html`
- 目标路径：`wiki/02_HX项目资料/99_原始资料镜像/bjhx_process/02_需求与方案/requirements/REQ-00020_批量汇报/prototype/HX批量报工原型.md`
- 提取方式：`html`
- 说明：本页由统一入库脚本自动生成，不覆盖人工整理页。

## 原始内容镜像

REQ-00020 批量汇报原型
:root {
      --bg: #eef3fb;
      --panel: #ffffff;
      --panel-soft: #f7f9fc;
      --line: #d9e1ee;
      --text: #1f2a3d;
      --muted: #6a7486;
      --primary: #2f80ed;
      --primary-soft: #e8f1ff;
      --success: #27ae60;
      --success-soft: #eaf8f0;
      --warn: #f2994a;
      --warn-soft: #fff3e5;
      --danger: #eb5757;
      --danger-soft: #ffeded;
      --shadow: 0 16px 32px rgba(46, 82, 138, 0.12);
      --radius: 20px;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0) 32%),
        linear-gradient(180deg, #f4f7fc 0%, #e9eff8 100%);
    }

    .app {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      padding: 18px 26px;
      background: rgba(255, 255, 255, 0.9);
      border-bottom: 1px solid rgba(217, 225, 238, 0.9);
      position: sticky;
      top: 0;
      z-index: 10;
      backdrop-filter: blur(16px);
    }

    .brand {
      font-size: 20px;
      font-weight: 700;
      letter-spacing: 0.5px;
    }

    .nav {
      display: flex;
      gap: 24px;
      align-items: center;
      flex-wrap: wrap;
    }

    .nav span {
      color: var(--muted);
      font-weight: 600;
      padding-bottom: 8px;
      border-bottom: 3px solid transparent;
    }

    .nav .active {
      color: var(--primary);
      border-color: var(--primary);
    }

    .user {
      display: flex;
      align-items: center;
      gap: 12px;
      color: var(--muted);
    }

    .avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: var(--primary);
      color: #fff;
      display: grid;
      place-items: center;
      font-weight: 700;
    }

    .filters {
      display: grid;
      grid-template-columns: 220px 180px 220px 220px 180px 220px;
      gap: 16px;
      padding: 20px 26px 6px;
    }

    .pill,
    .filter,
    .ghost-btn,
    .primary-btn,
    .outline-btn {
      border-radius: 18px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.92);
    }

    .filter {
      min-height: 56px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 18px;
      color: var(--muted);
      box-shadow: 0 10px 24px rgba(46, 82, 138, 0.06);
    }

    .filter strong {
      color: var(--text);
      font-weight: 600;
    }

    .workspace {
      display: grid;
      grid-template-columns: 1.65fr 0.95fr;
      gap: 20px;
      padding: 12px 26px 120px;
    }

    .surface {
      background: rgba(255, 255, 255, 0.9);
      border: 1px solid rgba(217, 225, 238, 0.9);
      border-radius: 24px;
      box-shadow: var(--shadow);
    }

    .task-board {
      padding: 18px;
    }

    .section-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 14px;
    }

    .section-head h2,
    .sidebar h2,
    .modal-head h2 {
      margin: 0;
      font-size: 18px;
    }

    .section-head small,
    .sidebar small {
      color: var(--muted);
    }

    .chip-row {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 600;
      background: var(--panel-soft);
      color: var(--muted);
      border: 1px solid var(--line);
    }

    .chip.primary {
      background: var(--primary-soft);
      color: var(--primary);
      border-color: #cfe0ff;
    }

    .chip.success {
      background: var(--success-soft);
      color: var(--success);
      border-color: #cbeed8;
    }

    .chip.warn {
      background: var(--warn-soft);
      color: #b96a1b;
      border-color: #ffd6af;
    }

    .chip.danger {
      background: var(--danger-soft);
      color: var(--danger);
      border-color: #ffc8c8;
    }

    .task-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }

    .task-card {
      position: relative;
      padding: 18px;
      border-radius: 22px;
      border: 1px solid #dfe7f2;
      background: linear-gradient(180deg, #ffffff 0%, #f9fbff 100%);
      min-height: 250px;
      cursor: pointer;
    }

    .task-card.selected {
      border-color: #8fc0ff;
      box-shadow: 0 0 0 3px rgba(47, 128, 237, 0.14);
    }

    .task-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 12px;
    }

    .check {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      border: 2px solid #c7d2e3;
      display: inline-grid;
      place-items: center;
      flex: 0 0 auto;
      margin-top: 2px;
    }

    .task-card.selected .check {
      border-color: var(--primary);
      background: var(--primary);
      color: #fff;
    }

    .task-title {
      flex: 1;
      min-width: 0;
    }

    .task-title h3 {
      margin: 0 0 8px;
      font-size: 18px;
      color: var(--primary);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .task-title p {
      margin: 0 0 8px;
      color: #3d495c;
      line-height: 1.45;
    }

    .task-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 18px;
    }

    .ghost-btn,
    .primary-btn,
    .outline-btn {
      min-height: 42px;
      padding: 0 18px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
    }

    .ghost-btn {
      background: #fff;
      color: var(--text);
    }

    .outline-btn {
      background: #fff;
      color: var(--primary);
      border-color: #afd1ff;
    }

    .primary-btn {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }

    .sidebar {
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .panel {
      padding: 18px;
      border-radius: 20px;
      background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
      border: 1px solid #e0e8f2;
    }

    .panel h3 {
      margin: 0 0 10px;
      font-size: 16px;
    }

    .panel p,
    .panel li {
      margin: 0;
      color: #465266;
      line-height: 1.6;
      font-size: 14px;
    }

    .panel ul {
      margin: 10px 0 0;
      padding-left: 18px;
    }

    .permission-box {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 12px;
    }

    .permission-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 10px 12px;
      border: 1px solid #e0e8f2;
      border-radius: 14px;
      background: #fbfdff;
      font-size: 14px;
    }

    .permission-row label {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
    }

    .summary-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }

    .summary-card {
      border-radius: 18px;
      padding: 14px;
      background: var(--panel-soft);
      border: 1px solid #dee7f2;
    }

    .summary-card strong {
      display: block;
      font-size: 24px;
      margin-bottom: 6px;
      color: var(--text);
    }

    .summary-card span {
      color: var(--muted);
      font-size: 13px;
    }

    .dock {
      position: fixed;
      left: 0;
      right: 0;
      bottom: 0;
      display: flex;
      align-items: center;
      gap: 18px;
      padding: 16px 22px;
      background: rgba(255, 255, 255, 0.94);
      border-top: 1px solid rgba(217, 225, 238, 0.92);
      backdrop-filter: blur(18px);
      z-index: 8;
    }

    .dock-info {
      min-width: 180px;
    }

    .dock-info strong {
      display: block;
      font-size: 18px;
      margin-bottom: 4px;
    }

    .dock-info span {
      color: var(--muted);
      font-size: 13px;
    }

    .dock-actions {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 14px;
      flex: 1;
    }

    .dock-actions button {
      min-height: 54px;
      border-radius: 28px;
      font-size: 16px;
    }

    .modal {
      position: fixed;
      inset: 0;
      background: rgba(9, 22, 44, 0.42);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 24px;
      z-index: 20;
    }

    .modal.open {
      display: flex;
    }

    .modal-card {
      width: min(1320px, 100%);
      max-height: calc(100vh - 48px);
      overflow: auto;
      border-radius: 28px;
      background: #f7faff;
      box-shadow: 0 28px 72px rgba(12, 31, 62, 0.32);
      border: 1px solid rgba(255, 255, 255, 0.85);
    }

    .modal-head {
      padding: 22px 24px 14px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 18px;
    }

    .modal-head p {
      margin: 8px 0 0;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.6;
    }

    .close-btn {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      border: 1px solid var(--line);
      background: #fff;
      cursor: pointer;
      font-size: 18px;
    }

    .modal-body {
      padding: 0 24px 24px;
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 18px;
    }

    .list-panel,
    .result-panel {
      background: #fff;
      border-radius: 22px;
      border: 1px solid #dee7f2;
      padding: 18px;
    }

    .toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 14px;
      flex-wrap: wrap;
    }

    .toolbar-left,
    .toolbar-right {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
    }

    .executor-panel {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      padding: 14px 16px;
      margin-bottom: 14px;
      border: 1px solid #dee7f2;
      border-radius: 18px;
      background: #f8fbff;
    }

    .field {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .field.hidden {
      display: none;
    }

    .field label {
      font-size: 12px;
      font-weight: 600;
      color: var(--muted);
    }

    .field select {
      width: 100%;
      min-height: 42px;
      padding: 0 14px;
      border-radius: 14px;
      border: 1px solid #d5dfec;
      background: #fff;
      color: var(--text);
      font-size: 14px;
    }

    .field-tip {
      grid-column: 1 / -1;
      font-size: 12px;
      color: var(--muted);
      line-height: 1.5;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }

    th,
    td {
      text-align: left;
      padding: 12px 10px;
      border-bottom: 1px solid #ebf0f7;
      vertical-align: top;
    }

    th {
      color: var(--muted);
      font-weight: 600;
      background: #f8fbff;
      position: sticky;
      top: 0;
    }

    .row-disabled {
      background: #fafbfd;
      color: #9aa6b8;
    }

    .status-note {
      display: inline-flex;
      align-items: center;
      padding: 4px 8px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 600;
      background: #f4f7fb;
      color: var(--muted);
      border: 1px solid #e1e8f1;
    }

    .status-note.ok {
      background: var(--success-soft);
      color: var(--success);
      border-color: #cbeed8;
    }

    .status-note.fail {
      background: var(--danger-soft);
      color: var(--danger);
      border-color: #ffcaca;
    }

    .status-note.block {
      background: var(--warn-soft);
      color: #b96a1b;
      border-color: #ffd6af;
    }

    .result-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 12px;
    }

    .result-item {
      border: 1px solid #e2e9f4;
      border-radius: 16px;
      padding: 12px 14px;
      background: #fafcff;
    }

    .result-item strong {
      display: block;
      margin-bottom: 6px;
      font-size: 14px;
    }

    .result-item p {
      margin: 0;
      color: #526074;
      font-size: 13px;
      line-height: 1.5;
    }

    .alert {
      margin-top: 14px;
      padding: 12px 14px;
      border-radius: 16px;
      font-size: 13px;
      line-height: 1.5;
      display: none;
    }

    .alert.show {
      display: block;
    }

    .alert.info {
      background: var(--primary-soft);
      color: var(--primary);
      border: 1px solid #cfe0ff;
    }

    .alert.error {
      background: var(--danger-soft);
      color: var(--danger);
      border: 1px solid #ffcaca;
    }

    .helper {
      font-size: 12px;
      color: var(--muted);
    }

    @media (max-width: 1280px) {
      .filters,
      .workspace,
      .modal-body {
        grid-template-columns: 1fr;
      }

      .task-grid {
        grid-template-columns: 1fr;
      }

      .dock-actions {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 860px) {
      .topbar,
      .filters,
      .workspace {
        padding-left: 14px;
        padding-right: 14px;
      }

      .nav {
        display: none;
      }

      .dock {
        flex-direction: column;
        align-items: stretch;
      }

      .dock-info {
        min-width: 0;
      }
    }
KMMOM CLOUD 开目制造运行系统
班组工作台
班组派工
工序任务报工
完工任务
检验任务报工
危放
危
我的
班组
扫码
可报工
任务编号
MO-WF_YD_0325
任务名称
方向机加工
状态
正常
创建时间
2026-04-27
工序任务一级界面原型
参考产品标准报工入口，增加批量汇报入口和业务演示
组织：ZZCJ / DZCJ
适用：总装 / 电装
当前示例：工序任务报工
业务说明
原始文档与正式需求合并后的原型表达
入口方式
在现有工序任务报工一级界面中保留单工序操作，同时增加“横向批量汇报”和“纵向批量汇报”入口。原型里使用底部操作条触发。
横向批量汇报
同生产订单、同工序号、已开工。
支持全选、反选、单选。
校验物料装入、拍照附件、上道工序。
失败项保留原因，修正后重提。
纵向批量汇报
从当前工序向后筛选，按工序号升序。
默认全选后续工序，可跳过部分工序。
遇到“检验 / 专检”后停止一键汇报。
按顺序执行，失败即停止后续处理。
结果反馈
原型内置校验结果、提交结果、日志摘要。重点展示成功、失败、阻断三类业务反馈，而不是做高保真视觉。
权限演示
横向和纵向按钮按权限独立控制。取消勾选后，一级界面和卡片上的对应入口会禁用。
横向批量汇报权限
ZZCJ / DZCJ
纵向批量汇报权限
ZZCJ / DZCJ
0
当前选中工序
5
示例校验规则
2
批量入口模式
1
单页 HTML 原型
已选
0
条工序
先在左侧勾选主工序，再选择横向或纵向批量汇报
批量开工
横向批量汇报
纵向批量汇报
批量汇报
×
全选
反选
执行校验
批量汇报提交
汇报执行人（默认当前提交人）
互检执行人
人员选择范围：当前用户所在班组成员。汇报执行人默认当前提交人，可改选。命中互检标记时，互检执行人必选，且每个工序任务都会记录该人员。
选
任务编码
WBS号/令号/产品编号
物料名称
工序号和工序名称
工序内容
设备名称
互检标记
汇报数量
计划开始
计划结束
校验
结果面板
成功 0
失败 0
阻断 0
这里用于展示准入校验、批量提交和失败原因，方便评审业务规则是否完整。
const taskCards = [
      {
        id: "main-1",
        title: "MO-WF_YD_0325_01-0010:10",
        taskCode: "MO-WF_YD_0325_01-0010:10",
        orderNo: "WF_YD_0325_01",
        opNo: 10,
        opName: "粗加工",
        material: "K001方向机",
        product: "P-20260427-001",
        workCenter: "YD_机加厂",
        device: "K001_FXJ",
        line: "总装一班",
        status: "已派工 / 正常",
        reportable: true
      },
      {
        id: "main-2",
        title: "MO-WF_YD_0325_01-0020:20",
        taskCode: "MO-WF_YD_0325_01-0020:20",
        orderNo: "WF_YD_0325_01",
        opNo: 20,
        opName: "精加工",
        material: "K001方向机",
        product: "P-20260427-002",
        workCenter: "YD_机加厂",
        device: "K001_FXJ",
        line: "总装一班",
        status: "已派工 / 正常",
        reportable: true
      },
      {
        id: "main-3",
        title: "MO-WF_YD_0325_01-0030:30",
        taskCode: "MO-WF_YD_0325_01-0030:30",
        orderNo: "WF_YD_0325_01",
        opNo: 30,
        opName: "装配",
        material: "K001方向机",
        product: "P-20260427-003",
        workCenter: "YD_机加厂",
        device: "K001_ZP01",
        line: "总装一班",
        status: "已派工 / 正常",
        reportable: true
      },
      {
        id: "main-4",
        title: "MO-WF_YD_0325_02-0010:10",
        taskCode: "MO-WF_YD_0325_02-0010:10",
        orderNo: "WF_YD_0325_02",
        opNo: 10,
        opName: "粗加工",
        material: "K002转向体",
        product: "P-20260427-004",
        workCenter: "YD_机加厂",
        device: "K002_FXJ",
        line: "电装二班",
        status: "已派工 / 正常",
        reportable: true
      }
    ];

    const currentUser = {
      id: "u01",
      name: "张伟",
      team: "总装一班"
    };

    const teamMembers = [
      { id: "u01", name: "张伟" },
      { id: "u02", name: "李敏" },
      { id: "u03", name: "王强" },
      { id: "u04", name: "赵娜" }
    ];

    const horizontalRows = [
      {
        id: "hz-1",
        taskCode: "MO-WF_YD_0325_01-0020:20",
        ref: "WBS-A01 / LH-001 / P-20260427-002",
        material: "K001方向机",
        process: "20 精加工",
        content: "精加工外圆与定位孔",
        device: "K001_FXJ",
        qty: 12,
        planStart: "2026-04-28 08:00",
        planEnd: "2026-04-28 08:30",
        mutualCheck: false,
        status: "已开工",
        selected: true,
        validations: []
      },
      {
        id: "hz-2",
        taskCode: "MO-WF_YD_0325_01-0021:20",
        ref: "WBS-A01 / LH-002 / P-20260427-008",
        material: "K001方向机",
        process: "20 精加工",
        content: "精加工外圆与定位孔",
        device: "K001_FXJ",
        qty: 10,
        planStart: "2026-04-28 08:10",
        planEnd: "2026-04-28 08:40",
        mutualCheck: true,
        status: "已开工",
        selected: true,
        validations: ["material"]
      },
      {
        id: "hz-3",
        taskCode: "MO-WF_YD_0325_01-0022:20",
        ref: "WBS-A01 / LH-003 / P-20260427-009",
        material: "K001方向机",
        process: "20 精加工",
        content: "精加工外圆与定位孔",
        device: "K001_FXJ",
        qty: 8,
        planStart: "2026-04-28 08:20",
        planEnd: "2026-04-28 08:50",
        mutualCheck: false,
        status: "已开工",
        selected: true,
        validations: ["photo"]
      },
      {
        id: "hz-4",
        taskCode: "MO-WF_YD_0325_01-0023:20",
        ref: "WBS-A01 / LH-004 / P-20260427-010",
        material: "K001方向机",
        process: "20 精加工",
        content: "精加工外圆与定位孔",
        device: "K001_FXJ",
        qty: 6,
        planStart: "2026-04-28 08:30",
        planEnd: "2026-04-28 09:00",
        mutualCheck: true,
        status: "已开工",
        selected: false,
        validations: ["previous"]
      }
    ];

    const verticalRows = [
      {
        id: "vt-1",
        taskCode: "MO-WF_YD_0325_01-0030:30",
        ref: "WBS-A01 / LH-001 / P-20260427-002",
        material: "K001方向机",
        process: "30 装配",
        content: "完成部件装配与扭矩确认",
        device: "K001_ZP01",
        qty: 12,
        planStart: "2026-04-28 09:00",
        planEnd: "2026-04-28 09:20",
        mutualCheck: false,
        status: "已开工",
        selected: true,
        type: "normal",
        validations: []
      },
      {
        id: "vt-2",
        taskCode: "MO-WF_YD_0325_01-0040:40",
        ref: "WBS-A01 / LH-001 / P-20260427-002",
        material: "K001方向机",
        process: "40 紧固",
        content: "完成关键螺栓紧固与复核",
        device: "K001_JG01",
        qty: 12,
        planStart: "2026-04-28 09:20",
        planEnd: "2026-04-28 09:40",
        mutualCheck: true,
        status: "已开工",
        selected: true,
        type: "normal",
        validations: []
      },
      {
        id: "vt-3",
        taskCode: "MO-WF_YD_0325_01-0050:50",
        ref: "WBS-A01 / LH-001 / P-20260427-002",
        material: "K001方向机",
        process: "50 检验",
        content: "填写检验结果与检验参数",
        device: "QA-01",
        qty: 12,
        planStart: "2026-04-28 09:40",
        planEnd: "2026-04-28 10:00",
        mutualCheck: false,
        status: "已开工",
        selected: true,
        type: "inspection",
        validations: ["inspection"]
      },
      {
        id: "vt-4",
        taskCode: "MO-WF_YD_0325_01-0060:60",
        ref: "WBS-A01 / LH-001 / P-20260427-002",
        material: "K001方向机",
        process: "60 包装",
        content: "包装入箱并完成标签绑定",
        device: "BZ-01",
        qty: 12,
        planStart: "2026-04-28 10:00",
        planEnd: "2026-04-28 10:20",
        mutualCheck: false,
        status: "已开工",
        selected: true,
        type: "after-inspection",
        validations: ["inspection"]
      }
    ];

    const validationMessages = {
      material: "当前制造任务还有物料待装入，无法继续汇报。",
      photo: "任务需提交不少于 2 张照片，请拍照并上传完毕后提交任务。",
      previous: "选中数据有上道工序未完工，不能汇报。",
      inspection: "检验 / 专检工序需单独处理，后续工序停止一键汇报。"
    };

    const state = {
      selectedTaskIds: new Set(["main-2"]),
      mode: null,
      candidates: [],
      validated: false,
      results: [],
      reportExecutor: currentUser.id,
      mutualExecutor: "",
      permissions: {
        horizontal: true,
        vertical: true
      }
    };

    const taskGrid = document.getElementById("taskGrid");
    const selectedCount = document.getElementById("selectedCount");
    const dockSelected = document.getElementById("dockSelected");
    const modal = document.getElementById("modal");
    const modalTitle = document.getElementById("modalTitle");
    const modalDesc = document.getElementById("modalDesc");
    const modalChips = document.getElementById("modalChips");
    const candidateBody = document.getElementById("candidateBody");
    const resultList = document.getElementById("resultList");
    const resultSuccess = document.getElementById("resultSuccess");
    const resultFail = document.getElementById("resultFail");
    const resultBlock = document.getElementById("resultBlock");
    const resultHint = document.getElementById("resultHint");
    const submitAlert = document.getElementById("submitAlert");
    const helperText = document.getElementById("helperText");
    const reportExecutor = document.getElementById("reportExecutor");
    const mutualExecutor = document.getElementById("mutualExecutor");
    const mutualField = document.getElementById("mutualField");
    const executorTip = document.getElementById("executorTip");

    function fillMemberOptions(selectEl, includeEmpty) {
      const options = [];
      if (includeEmpty) {
        options.push('<option value="">请选择</option>');
      }
      teamMembers.forEach((member) => {
        options.push(`<option value="${member.id}">${member.name}（${currentUser.team}）</option>`);
      });
      selectEl.innerHTML = options.join("");
    }

    function getMemberName(memberId) {
      return teamMembers.find((member) => member.id === memberId)?.name || "";
    }

    function hasSelectedMutualCheck() {
      return state.candidates.some((row) => row.selected && row.mutualCheck);
    }

    function syncExecutorPanel() {
      fillMemberOptions(reportExecutor, false);
      reportExecutor.value = state.reportExecutor || currentUser.id;

      fillMemberOptions(mutualExecutor, true);
      mutualExecutor.value = state.mutualExecutor || "";

      const mutualRequired = hasSelectedMutualCheck();
      mutualField.classList.toggle("hidden", !mutualRequired);
      executorTip.textContent = mutualRequired
        ? `人员选择范围：${currentUser.team}。汇报执行人默认当前提交人，可改选。当前选中工序存在互检标记，互检执行人必选，且每个成功汇报的工序任务都会记录该人员。`
        : `人员选择范围：${currentUser.team}。汇报执行人默认当前提交人，可改选。当前选中工序未命中互检标记，无需选择互检执行人。`;
      if (!mutualRequired) {
        state.mutualExecutor = "";
        mutualExecutor.value = "";
      }
    }

    function renderTasks() {
      taskGrid.innerHTML = "";
      taskCards.forEach((task) => {
        const card = document.createElement("article");
        card.className = "task-card" + (state.selectedTaskIds.has(task.id) ? " selected" : "");
        card.innerHTML = `
          <div class="task-top">
            <div class="check">${state.selectedTaskIds.has(task.id) ? "✓" : ""}</div>
            <div class="task-title">
              <h3>${task.title}</h3>
              <p>${task.taskCode}</p>
              <p>${task.material} | ${task.opNo} | ${task.device}</p>
              <p>${task.workCenter} | ${task.line}</p>
              <p>${task.orderNo}</p>
            </div>
            <div class="chip-row">
              <span class="chip danger">已派工</span>
              <span class="chip success">正常</span>
            </div>
          </div>
          <div class="task-actions">
            <button class="ghost-btn" type="button">开工</button>
            <button class="ghost-btn" type="button">报工</button>
            <button class="ghost-btn" type="button">待定报工</button>
            <button class="outline-btn quick-horizontal" type="button" ${state.permissions.horizontal ? "" : "disabled"}>横向批量</button>
            <button class="outline-btn quick-vertical" type="button" ${state.permissions.vertical ? "" : "disabled"}>纵向批量</button>
          </div>
        `;

        card.addEventListener("click", (event) => {
          if (event.target.tagName === "BUTTON") {
            return;
          }
          toggleTaskSelection(task.id);
        });

        card.querySelector(".quick-horizontal").addEventListener("click", (event) => {
          event.stopPropagation();
          if (!state.permissions.horizontal) {
            return;
          }
          state.selectedTaskIds = new Set([task.id]);
          updateSelectionCount();
          renderTasks();
          openModal("horizontal", task);
        });

        card.querySelector(".quick-vertical").addEventListener("click", (event) => {
          event.stopPropagation();
          if (!state.permissions.vertical) {
            return;
          }
          state.selectedTaskIds = new Set([task.id]);
          updateSelectionCount();
          renderTasks();
          openModal("vertical", task);
        });

        taskGrid.appendChild(card);
      });
    }

    function toggleTaskSelection(taskId) {
      if (state.selectedTaskIds.has(taskId)) {
        state.selectedTaskIds.delete(taskId);
      } else {
        state.selectedTaskIds.add(taskId);
      }
      updateSelectionCount();
      renderTasks();
    }

    function updateSelectionCount() {
      const count = state.selectedTaskIds.size;
      selectedCount.textContent = String(count);
      dockSelected.textContent = String(count);
    }

    function openModal(mode, task) {
      state.mode = mode;
      state.validated = false;
      state.results = [];
      state.reportExecutor = currentUser.id;
      state.mutualExecutor = "";
      submitAlert.className = "alert error";
      submitAlert.textContent = "";
      resultHint.className = "alert info show";
      resultHint.textContent = "这里用于展示准入校验、批量提交和失败原因，方便评审业务规则是否完整。";

      if (mode === "horizontal") {
        state.candidates = JSON.parse(JSON.stringify(horizontalRows));
        modalTitle.textContent = "横向批量汇报";
        modalDesc.textContent = `基于当前工序 ${task.opNo} - ${task.opName} 自动筛选同生产订单、同工序号、已开工工序。`;
        helperText.textContent = "校验项：物料装入、拍照附件、上道工序、互检执行人";
        modalChips.innerHTML = `
          <span class="chip primary">当前主工序：${task.taskCode}</span>
          <span class="chip success">权限：横向批量汇报</span>
          <span class="chip">筛选条件：同生产订单</span>
          <span class="chip">筛选条件：同工序号</span>
          <span class="chip">筛选条件：已开工</span>
          <span class="chip warn">执行人范围：当前班组</span>
        `;
      } else {
        state.candidates = JSON.parse(JSON.stringify(verticalRows));
        modalTitle.textContent = "纵向批量汇报";
        modalDesc.textContent = `基于当前工序 ${task.opNo} - ${task.opName} 自动筛选后续工序，并按工序号升序展示。`;
        helperText.textContent = "校验项：物料装入、拍照附件、互检执行人、检验工序拦截";
        modalChips.innerHTML = `
          <span class="chip primary">当前主工序：${task.taskCode}</span>
          <span class="chip success">权限：纵向批量汇报</span>
          <span class="chip">筛选条件：后续工序</span>
          <span class="chip">按工序号升序</span>
          <span class="chip warn">遇检验 / 专检即停止</span>
          <span class="chip warn">执行人范围：当前班组</span>
        `;
      }

      syncExecutorPanel();
      renderCandidateTable();
      renderResults();
      modal.classList.add("open");
    }

    function renderCandidateTable() {
      candidateBody.innerHTML = "";
      state.candidates.forEach((row, index) => {
        const blockedByInspection = state.mode === "vertical" && (row.type === "inspection" || row.type === "after-inspection");
        const rowClass = blockedByInspection ? "row-disabled" : "";
        const result = row.result || null;
        const tr = document.createElement("tr");
        tr.className = rowClass;
        tr.innerHTML = `
          <td><input type="checkbox" ${row.selected ? "checked" : ""} ${blockedByInspection ? "disabled" : ""}></td>
          <td>${row.taskCode}</td>
          <td>${row.ref}</td>
          <td>${row.material}</td>
          <td>${row.process}</td>
          <td>${row.content}</td>
          <td>${row.device}</td>
          <td>${row.mutualCheck ? '<span class="status-note block">需互检</span>' : '<span class="status-note ok">无互检</span>'}</td>
          <td>${row.qty}</td>
          <td>${row.planStart}</td>
          <td>${row.planEnd}</td>
          <td>${renderRowStatus(row, result, blockedByInspection, index)}</td>
        `;

        const checkbox = tr.querySelector("input");
        checkbox.addEventListener("change", () => {
          row.selected = checkbox.checked;
          syncExecutorPanel();
        });
        candidateBody.appendChild(tr);
      });
    }

    function renderRowStatus(row, result, blockedByInspection, index) {
      if (blockedByInspection) {
        return '<span class="status-note block">检验拦截</span>';
      }
      if (!state.validated) {
        return '<span class="status-note">待校验</span>';
      }
      if (result && result.kind === "success") {
        return '<span class="status-note ok">可汇报</span>';
      }
      if (result && result.kind === "failure") {
        return `<span class="status-note fail">${result.short}</span>`;
      }
      if (state.mode === "vertical" && index > 0) {
        const previous = state.candidates[index - 1];
        if (previous.result && previous.result.kind !== "success") {
          return '<span class="status-note block">后续停止</span>';
        }
      }
      return '<span class="status-note">待校验</span>';
    }

    function runValidation() {
      state.validated = true;
      state.results = [];

      if (state.mode === "horizontal") {
        state.candidates.forEach((row) => {
          if (!row.selected) {
            row.result = { kind: "skipped", short: "未选中", detail: "当前工序未被纳入本次提交。" };
            return;
          }
          const error = row.validations[0];
          if (error) {
            row.result = { kind: "failure", short: "校验失败", detail: validationMessages[error] };
          } else {
            row.result = { kind: "success", short: "通过", detail: "准入校验通过，可执行批量汇报。" };
          }
          state.results.push({
            title: row.taskCode,
            kind: row.result.kind,
            detail: row.result.detail
          });
        });
      } else {
        let blocked = false;
        state.candidates.forEach((row) => {
          if (!row.selected) {
            row.result = { kind: "skipped", short: "未选中", detail: "当前工序未被纳入本次提交。" };
            return;
          }
          if (blocked || row.type === "inspection" || row.type === "after-inspection") {
            row.result = {
              kind: "blocked",
              short: "检验拦截",
              detail: validationMessages.inspection
            };
            blocked = true;
          } else {
            row.result = { kind: "success", short: "通过", detail: "顺序校验通过，可继续处理后续工序。" };
          }
          state.results.push({
            title: row.taskCode,
            kind: row.result.kind === "blocked" ? "blocked" : row.result.kind,
            detail: row.result.detail
          });
        });
      }

      renderCandidateTable();
      renderResults();
      resultHint.className = "alert info show";
      resultHint.textContent = "已完成准入校验。失败或阻断项不会进入正式汇报。";
    }

    function submitBatch() {
      if (!state.validated) {
        submitAlert.className = "alert error show";
        submitAlert.textContent = "请先执行校验，再进行批量汇报提交。";
        return;
      }

      const selectedRows = state.candidates.filter((row) => row.selected);
      if (!selectedRows.length) {
        submitAlert.className = "alert error show";
        submitAlert.textContent = "至少选择一条工序后再提交。";
        return;
      }

      if (!state.reportExecutor) {
        submitAlert.className = "alert error show";
        submitAlert.textContent = "请先选择汇报执行人。";
        return;
      }

      if (hasSelectedMutualCheck() && !state.mutualExecutor) {
        submitAlert.className = "alert error show";
        submitAlert.textContent = "当前选中工序存在互检标记，请先选择互检执行人。";
        return;
      }

      const invalidRows = selectedRows.filter((row) => !row.result || row.result.kind !== "success");
      if (invalidRows.length) {
        submitAlert.className = "alert error show";
        submitAlert.textContent = "当前仍有失败或阻断工序，请取消这些工序或修正问题后重新提交。";
        return;
      }

      const reportExecutorName = getMemberName(state.reportExecutor);
      const mutualExecutorName = getMemberName(state.mutualExecutor);
      submitAlert.className = "alert info show";
      submitAlert.textContent = hasSelectedMutualCheck()
        ? `批量汇报提交成功：实际执行人默认当前提交人，本次记录为 ${reportExecutorName}；互检执行人为 ${mutualExecutorName}，结果已记录到操作日志。`
        : `批量汇报提交成功：实际执行人默认当前提交人，本次记录为 ${reportExecutorName}，结果已记录到操作日志。`;

      state.results = selectedRows.map((row) => ({
        title: row.taskCode,
        kind: "success",
        detail: hasSelectedMutualCheck()
          ? `批量汇报成功，已记录汇报执行人 ${reportExecutorName} 与互检执行人 ${mutualExecutorName}。`
          : `批量汇报成功，已记录汇报执行人 ${reportExecutorName}。`
      }));

      renderResults();
      resultHint.className = "alert info show";
      resultHint.textContent = state.mode === "horizontal"
        ? "横向批量汇报已完成：同工序号多条工序已统一报工，命中互检标记时已为每个成功任务记录互检执行人。"
        : "纵向批量汇报已完成：后续工序按顺序汇报，遇检验工序前停止，命中互检标记时已为每个成功任务记录互检执行人。";
    }

    function renderResults() {
      const success = state.results.filter((item) => item.kind === "success").length;
      const fail = state.results.filter((item) => item.kind === "failure").length;
      const block = state.results.filter((item) => item.kind === "blocked").length;

      resultSuccess.textContent = `成功 ${success}`;
      resultFail.textContent = `失败 ${fail}`;
      resultBlock.textContent = `阻断 ${block}`;

      resultList.innerHTML = "";
      if (!state.results.length) {
        const empty = document.createElement("div");
        empty.className = "result-item";
        empty.innerHTML = "<strong>尚未执行</strong><p>点击“执行校验”查看规则命中情况，再决定是否提交。</p>";
        resultList.appendChild(empty);
        return;
      }

      state.results.forEach((item) => {
        const card = document.createElement("div");
        const kindClass = item.kind === "success" ? "ok" : item.kind === "failure" ? "fail" : "block";
        card.className = "result-item";
        card.innerHTML = `
          <strong>${item.title}</strong>
          <div style="margin-bottom:6px;"><span class="status-note ${kindClass}">${item.kind === "success" ? "成功" : item.kind === "failure" ? "失败" : "阻断"}</span></div>
          <p>${item.detail}</p>
        `;
        resultList.appendChild(card);
      });
    }

    document.getElementById("horizontalBtn").addEventListener("click", () => {
      if (!state.permissions.horizontal) {
        alert("当前用户无横向批量汇报权限。");
        return;
      }
      const task = taskCards.find((item) => state.selectedTaskIds.has(item.id)) || taskCards[1];
      openModal("horizontal", task);
    });

    document.getElementById("verticalBtn").addEventListener("click", () => {
      if (!state.permissions.vertical) {
        alert("当前用户无纵向批量汇报权限。");
        return;
      }
      const task = taskCards.find((item) => state.selectedTaskIds.has(item.id)) || taskCards[1];
      openModal("vertical", task);
    });

    document.getElementById("startBtn").addEventListener("click", () => {
      alert("原型说明：本页重点演示批量汇报，不展开批量开工流程。");
    });

    document.getElementById("closeModal").addEventListener("click", () => {
      modal.classList.remove("open");
    });

    modal.addEventListener("click", (event) => {
      if (event.target === modal) {
        modal.classList.remove("open");
      }
    });

    document.getElementById("selectAllBtn").addEventListener("click", () => {
      state.candidates.forEach((row) => {
        if (!(state.mode === "vertical" && (row.type === "inspection" || row.type === "after-inspection"))) {
          row.selected = true;
        }
      });
      syncExecutorPanel();
      renderCandidateTable();
    });

    document.getElementById("invertBtn").addEventListener("click", () => {
      state.candidates.forEach((row) => {
        if (!(state.mode === "vertical" && (row.type === "inspection" || row.type === "after-inspection"))) {
          row.selected = !row.selected;
        }
      });
      syncExecutorPanel();
      renderCandidateTable();
    });

    document.getElementById("validateBtn").addEventListener("click", runValidation);
    document.getElementById("submitBtn").addEventListener("click", submitBatch);
    reportExecutor.addEventListener("change", () => {
      state.reportExecutor = reportExecutor.value;
    });
    mutualExecutor.addEventListener("change", () => {
      state.mutualExecutor = mutualExecutor.value;
    });
    document.getElementById("permHorizontal").addEventListener("change", (event) => {
      state.permissions.horizontal = event.target.checked;
      document.getElementById("horizontalBtn").disabled = !state.permissions.horizontal;
      renderTasks();
    });
    document.getElementById("permVertical").addEventListener("change", (event) => {
      state.permissions.vertical = event.target.checked;
      document.getElementById("verticalBtn").disabled = !state.permissions.vertical;
      renderTasks();
    });

    updateSelectionCount();
    document.getElementById("horizontalBtn").disabled = !state.permissions.horizontal;
    document.getElementById("verticalBtn").disabled = !state.permissions.vertical;
    renderTasks();
    fillMemberOptions(reportExecutor, false);
    fillMemberOptions(mutualExecutor, true);
