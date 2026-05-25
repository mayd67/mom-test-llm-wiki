---
name: mom-business-data-generator
description: Generate MOM business seed packages and import-ready Excel workbooks from local templates and built-in JSON seeds. Use when Codex needs to create, regenerate, validate, expand, or adapt single-factory, multi-factory, project-collaboration, process, or production-order demo and test data for MOM imports, POC delivery, or environment initialization.
---

# MOM Business Data Generator

使用这个 skill 生成、校验或扩展 MOM 导入数据包。

## 先读哪些文件

1. [references/scenario_blueprints.md](references/scenario_blueprints.md)
2. [references/template_relationships.md](references/template_relationships.md)
3. [references/template_constraint_dictionary.md](references/template_constraint_dictionary.md)
4. 如需按既有场景批量组织导入节奏，再补读对应的 `references/*_import_batches.md`

## 工作流程

1. 先判断场景类型。
- 单零件、单部件、单工厂机加或装配场景，优先走单工厂蓝图。
- 总成、多专业协同、跨厂流转、项目部协同场景，优先走多工厂蓝图。
- 用户已提供现成 `seed.json` 时，优先在现有种子上增改，不要直接从 Excel 表头反推整套数据。

2. 选择生成入口。
- 先执行 `python scripts/build_common_seed_packages.py --list` 查看已内置标准场景。
- 命中内置场景时，优先直接执行 `python scripts/build_common_seed_packages.py --scenario <scenario_name>`。
- 用户提供了自定义种子时，优先执行 `python scripts/generate_seed_workbooks.py --seed <seed.json>`。
- 只想先检查种子合法性时，执行 `python scripts/generate_seed_workbooks.py --seed <seed.json> --validate-only`。
- 只有在用户明确要求扩容数据量、升级大样本或补充批量对象时，才继续使用 `seed_volume_enhancer.py`、`scene_seed_upgrades.py` 等增强脚本。

3. 输出结果。
- 默认从 `templates/` 读取四本 Excel 模板：`系统配置_模板.xlsx`、`工厂资源_模板.xlsx`、`产品与工艺_模板.xlsx`、`生产订单_模板.xlsx`。
- 默认输出到工作区根目录 `outputs/06_测试数据/`。
- 默认按“一个业务场景一个子目录”的方式组织输出。
- 输出目录、摘要文件和业务标签优先使用中文；摘要文件优先命名为 `种子概览.json`。

4. 校验关键约束。
- 不要编造模板不存在的下拉枚举、状态值、工艺专业或组织类型。
- `库房`、`库位` 的 `*工厂组织` 必须挂到工厂级业务组织，不能挂到部门、车间、工段或班组。
- 未明确要求时，默认不生成 `厂内转工`、`厂际转工`。
- 只有当用户明确要求“一级工艺 + 项目部/生产部协同层”时，才生成项目协同扩展层。
- 引用字段统一填写真实存在的对象编码；涉及版本号时一并填写版本号。

5. 回复结果。
- 说明采用的蓝图、关键假设、是否使用内置标准场景。
- 如果已生成文件，回复中给出输出目录和关键工作簿名称。
- 如果只做了校验，优先返回未通过的约束项，不要伪造“已成功生成”结论。

## 常用命令

```powershell
python scripts/build_common_seed_packages.py --list
python scripts/build_common_seed_packages.py --scenario bearing_machining_standard
python scripts/build_common_seed_packages.py --scenario gearbox_multi_factory_standard
python scripts/generate_seed_workbooks.py --seed assets/bearing_machining_seed.json --validate-only
```

## 当前内置标准场景

- `bearing_machining_standard`
- `fuel_pump_assembly_standard`
- `bicycle_assembly_standard`
- `gearbox_assembly_standard`
- `gearbox_machining_assembly_standard`
- `gearbox_multi_factory_standard`
- `mom_promo_video_standard`
- `blade_project_collaboration_standard`
- `aeroengine_fuel_system_multi_factory_standard`

## 配套资源

- 场景判定蓝图：[references/scenario_blueprints.md](references/scenario_blueprints.md)
- 模板引用关系：[references/template_relationships.md](references/template_relationships.md)
- 模板枚举与约束字典：[references/template_constraint_dictionary.md](references/template_constraint_dictionary.md)
- 常用生成入口：[scripts/build_common_seed_packages.py](scripts/build_common_seed_packages.py)
- 工作簿生成器：[scripts/generate_seed_workbooks.py](scripts/generate_seed_workbooks.py)

## 兼容层说明

当前目录还保留 `AGENTS.md`、`CLAUDE.md`、`START_HERE.md`、`PORTABILITY.md`、`PROMPT_TEMPLATE.md` 等跨 Agent 兼容文件。把它们视为补充入口；本仓库内仍以 `SKILL.md` 作为主入口和规范来源。
