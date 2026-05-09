# 通用提示词模板

可将下面这段内容直接复制到不支持 `.codex/skills`、`AGENTS.md` 或 `CLAUDE.md` 自动发现机制的 AI 工具中。

```text
请把当前目录当作一个可执行的 MOM 业务数据生成器项目来处理。

开始前请先阅读：
1. START_HERE.md
2. PORTABILITY.md
3. README_SHARE.md
4. SKILL.md
5. 如需要字段和引用关系细节，再阅读 references/template_relationships.md 和 references/template_constraint_dictionary.md

执行时请遵守以下规则：
- 模板默认使用 templates/ 目录
- 输出默认写到工作区根目录 output/
- 输出名称优先中文
- 摘要文件优先使用 种子概览.json
- 库房和库位的 *工厂组织 必须挂到 工厂组织类型=工厂 的业务组织
- 未明确要求时，不生成 厂内转工 / 厂际转工
- 编码优先短编码，例如 Eq001、Wc001、Wh001、Loc001、Mat001、Rt001
- 优先复用现有脚本，不要手工拼 Excel

优先使用以下命令：
- python scripts/build_common_seed_packages.py --list
- python scripts/build_common_seed_packages.py --scenario bearing_machining_standard
- python scripts/generate_seed_workbooks.py --seed assets/bearing_machining_seed.json --validate-only
- python scripts/organize_output_by_material_name.py --clean

如果我要你生成新业务数据，请先判断属于单工厂、多工厂还是项目部协同场景，再选择最接近的现有脚本或按相同结构扩展。
```
