---
name: mom-business-data-generator
description: 基于 Excel 模板快速生成 MOM 业务数据、工厂数据、工艺数据和生产订单数据，适用于单工厂、多工厂和项目部协同场景。
---

# MOM 业务数据生成 Skill

## 作用

根据 `templates/` 中的 Excel 模板和 `assets/` 中的种子 JSON，生成可导入 MOM 系统的 Excel 数据包。

## 包含的主要对象

- `系统配置_模板.xlsx`
- `工厂资源_模板.xlsx`
- `产品与工艺_模板.xlsx`
- `生产订单_模板.xlsx`

## 默认规则

- 模板默认从 `templates/` 读取
- 输出默认写到工作区根目录 `outputs/06_测试数据/`
- 默认按“一个业务场景一个子目录”的方式组织输出
- 输出目录优先中文
- 摘要文件优先 `种子概览.json`
- 编码优先短编码
- `库房`、`库位` 的 `*工厂组织` 必须挂到工厂级业务组织
- 未明确要求时，默认不生成 `厂内转工` / `厂际转工`
- 只有当用户明确要求“一级工艺 + 生产项目部一级生产订单”时，才生成项目部协同层

## 优先脚本

```powershell
python scripts/build_common_seed_packages.py --list
python scripts/build_common_seed_packages.py --scenario bearing_machining_standard
python scripts/generate_seed_workbooks.py --seed assets/bearing_machining_seed.json --validate-only
```

## 当前已内置的常用场景

- `bearing_machining_standard`
- `bicycle_assembly_standard`
- `fuel_pump_assembly_standard`
- `gearbox_assembly_standard`
- `gearbox_machining_assembly_standard`
- `gearbox_multi_factory_standard`
- `blade_project_collaboration_standard`

## 跨 Agent 兼容层

为了便于在不同 AI 工具中复用，当前目录还提供：

- `AGENTS.md`
- `CLAUDE.md`
- `START_HERE.md`
- `PORTABILITY.md`
- `PROMPT_TEMPLATE.md`
- `requirements.txt`
- `scripts/build_portable_agent_package.py`

只要目标工具能读取本目录文件并执行 Python 命令，就能复用同样的业务数据生成能力。

