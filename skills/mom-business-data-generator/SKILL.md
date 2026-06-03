---
name: mom-business-data-generator
description: Generate MOM business seed packages and import-ready Excel workbooks from user-provided latest Excel templates or built-in JSON seeds. Use when Codex needs to create, regenerate, validate, expand, or adapt single-factory, multi-factory, project-collaboration, process, or production-order demo and test data for MOM imports, POC delivery, or environment initialization, especially when the user has supplied newer import templates that must be used for the exported workbooks.
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

2. 先确认模板来源。
- 用户提供了最新导入模板时，必须优先使用用户提供的模板目录导出 Excel，不要默认回落到 skill 自带 `templates/`。
- 不要直接覆盖 skill 目录下的 `templates/`；优先把最新模板复制到当前业务场景目录下的 `模板输入/`、`latest_templates/` 或其他独立目录，并统一重命名为标准文件名：
  - `系统配置_模板.xlsx`
  - `工厂资源_模板.xlsx`
  - `产品与工艺_模板.xlsx`
  - `生产订单_模板.xlsx`
- 只要不是明确确认“skill 自带模板就是最新模板”，所有生成和校验命令都显式传 `--template-dir <最新模板目录>`。
- 只有当用户未提供更新模板，且工作区内也没有明确指定的最新模板目录时，才回退到 skill 自带 `templates/`。

3. 选择生成入口。
- 先执行 `python scripts/build_common_seed_packages.py --list` 查看已内置标准场景。
- 命中内置场景时，优先执行 `python scripts/build_common_seed_packages.py --scenario <scenario_name> --template-dir <最新模板目录>`。
- 用户提供了自定义种子时，优先执行 `python scripts/generate_seed_workbooks.py --seed <seed.json> --template-dir <最新模板目录>`。
- 只想先检查种子合法性时，执行 `python scripts/generate_seed_workbooks.py --seed <seed.json> --template-dir <最新模板目录> --validate-only`。
- 对旧版字段口径的 `seed.json`，优先继续复用；共享生成器会按 `--template-dir` 指向的最新导入模板自动做字段对齐。
- 只有在用户明确要求扩容数据量、升级大样本或补充批量对象时，才继续使用 `seed_volume_enhancer.py`、`scene_seed_upgrades.py` 等增强脚本。

4. 输出结果。
- 导出的 Excel 必须以本次任务确认的最新模板为准；如果用户提供了模板，导出结果必须与用户提供模板的 Sheet 和列头保持一致。
- 优先从 `--template-dir` 指定的目录读取四本 Excel 模板：`系统配置_模板.xlsx`、`工厂资源_模板.xlsx`、`产品与工艺_模板.xlsx`、`生产订单_模板.xlsx`。
- skill 自带 `templates/` 只作为兜底基线模板，不作为“最新模板”的默认结论。
- 新增的资质等级、资质关系、文件关系等 Sheet 默认允许留空。
- 默认输出到工作区根目录 `outputs/06_测试数据/`。
- 默认按“一个业务场景一个子目录”的方式组织输出。
- 输出目录、摘要文件和业务标签优先使用中文；摘要文件优先命名为 `种子概览.json`。

5. 校验关键约束。
- 不要编造模板不存在的下拉枚举、状态值、工艺专业或组织类型。
- `库房`、`库位` 的 `*工厂组织` 必须挂到工厂级业务组织，不能挂到部门、车间、工段或班组。
- 未明确要求时，默认不生成 `厂内转工`、`厂际转工`。
- 只有当用户明确要求“一级工艺 + 项目部/生产部协同层”时，才生成项目协同扩展层。
- 引用字段统一填写真实存在的对象编码；涉及版本号时一并填写版本号。
- `资质等级`、`资质等级与用户`、`工序库与资质等级`、`工艺路线与资质等级关系`、`物料与文件关系` 默认保持空表；只有用户明确提供合法编码和映射关系时才补数据。
- 如果最新模板的下拉枚举或字段口径与 skill 内置模板不同，以本次 `--template-dir` 指向模板的实际约束为准。

6. 回复结果。
- 说明采用的蓝图、关键假设、是否使用内置标准场景。
- 如果已生成文件，回复中给出输出目录、关键工作簿名称，以及本次实际使用的模板目录。
- 如果只做了校验，优先返回未通过的约束项，不要伪造“已成功生成”结论。

## 常用命令

```powershell
python scripts/build_common_seed_packages.py --list
python scripts/build_common_seed_packages.py --scenario bearing_machining_standard --template-dir .\最新模板
python scripts/build_common_seed_packages.py --scenario gearbox_multi_factory_standard --template-dir .\最新模板
python scripts/generate_seed_workbooks.py --seed assets/bearing_machining_seed.json --template-dir .\最新模板 --validate-only
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
- 如需按用户最新模板导出，统一通过 `--template-dir` 显式指定模板目录。

## 兼容层说明

当前目录还保留 `AGENTS.md`、`CLAUDE.md`、`START_HERE.md`、`PORTABILITY.md`、`PROMPT_TEMPLATE.md` 等跨 Agent 兼容文件。把它们视为补充入口；本仓库内仍以 `SKILL.md` 作为主入口和规范来源。
