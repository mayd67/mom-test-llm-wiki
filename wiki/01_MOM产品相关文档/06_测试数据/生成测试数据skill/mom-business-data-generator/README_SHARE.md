# MOM 模板种子生成器共享说明

## 1. 这份包是干什么的

这是一套基于 Excel 模板生成 MOM 业务数据、工厂数据、工艺数据和生产订单数据的共享目录。

适合：

- 团队内部复用
- 售前 POC 演示
- 换电脑后恢复生成能力
- 配合不同 AI 工具复用

## 2. 目录结构

```text
mom-template-seed-generator/
- templates/
- assets/
- scripts/
- references/
- tests/
- SKILL.md
- README_SHARE.md
- DELIVERY_PACKAGE_CHECKLIST.md
- START_HERE.md
- PORTABILITY.md
- PROMPT_TEMPLATE.md
- AGENTS.md
- CLAUDE.md
- requirements.txt
```

说明：

- `templates/` 内含四个 Excel 模板
- `assets/` 内含已有种子 JSON
- `scripts/` 内含生成、校验、分类整理、打包等脚本
- `references/` 内含模板字段关系和约束说明

## 3. 最常用命令

```powershell
python scripts/build_common_seed_packages.py --list
python scripts/build_common_seed_packages.py --scenario bearing_machining_standard
python scripts/build_common_seed_packages.py --scenario bicycle_assembly_standard
python scripts/generate_seed_workbooks.py --seed assets/bearing_machining_seed.json --validate-only
python scripts/organize_output_by_material_name.py --clean
```

## 4. 默认规则

- 模板默认使用 `templates/`
- 输出默认写到工作区根目录 `output/`
- 输出目录优先中文
- 摘要文件优先 `种子概览.json`
- `库房`、`库位` 的 `*工厂组织` 必须挂到工厂级业务组织
- 未明确要求时，不生成 `厂内转工` / `厂际转工`
- 编码优先短编码

## 5. 跨 Agent 使用

- 支持自动读取指令文件的工具：直接打开本目录
- 不支持自动发现的工具：先看 `PROMPT_TEMPLATE.md`，把提示词复制到对话首轮
- 如需打包给别人，可使用 `scripts/build_portable_agent_package.py`

## 6. 多 Agent 兼容附加文件

当前目录额外提供：

- `AGENTS.md`
- `CLAUDE.md`
- `START_HERE.md`
- `PORTABILITY.md`
- `PROMPT_TEMPLATE.md`
- `requirements.txt`
- `scripts/build_portable_agent_package.py`

只要目标工具能读取本目录文件并执行 Python 命令，就能复用同样的业务数据生成能力。
