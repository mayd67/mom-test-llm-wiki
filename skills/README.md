# Skills Index

本目录统一保存仓库内所有可复用的 skill 本体、参考资料、脚本和 agent 元数据。

`wiki/` 负责业务入口页、使用说明和知识上下文；`skills/` 负责 skill 本体。

## 使用规则

- 新增 skill：默认放到 `skills/<skill-name>/`
- `wiki/` 中不再放 skill 本体目录，只保留能力总览页和入口说明
- skill 运行产物默认不留在 `skills/`，应按类型进入 `outputs/`
- 如需判断落位规则，优先参考 `skills/test-output-placement/` 和 `outputs/README.md`

## 当前技能清单

| Skill | 作用 | 默认产物落位 |
| --- | --- | --- |
| `requirement-to-testpoints` | 从需求材料拆测试点 | `outputs/02_测试点/01_待评审/` |
| `requirement-to-testcases` | 从需求/测试点生成测试用例 | Markdown: `outputs/03_测试用例/01_待评审/`；导入版 Excel: `outputs/03_测试用例/03_MeterSphere导入/` |
| `user-manual-writer` | 生成或改写用户操作手册 | 交付稿默认 `outputs/05_用户操作手册/`；知识沉淀稿进入 `wiki/` |
| `mom-business-data-generator` | 生成 MOM 测试数据、导入包和场景种子 | `outputs/06_测试数据/` |
| `defect-report-generator` | 生成 Jira 导入 CSV | `outputs/04_测试执行/03_缺陷导出/` |
| `test-output-placement` | 判断交付物应该进入哪个 `outputs/` 目录 | 自身不产出业务文件 |
| `raw-to-wiki-ingest` | 编排 `raw/ -> wiki/` 入库 | 自身不产出 `outputs/` 文件 |

## 推荐阅读

- `outputs/README.md`
- `skills/test-output-placement/SKILL.md`
- `skills/raw-to-wiki-ingest/SKILL.md`

