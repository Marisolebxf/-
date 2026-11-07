# TS-L2-DS02-ENTITY-DATA · 科学技术全景 · 展示技术点关联实体 · 数据落点

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:arch-agent`（兼 data 分册） |
| supervised_by | `human:淮政玮` |
| claim_type | 监管人会话派单。本会话不改 task-registry，未经 MCP 认领 |
| 说明 | 只写文档。不改库、不改图、不 commit。不标 done |

## Ponytail

ponytail: off（定义任务）

不缩文档。未用 YAGNI 跳过 D18 表结构、现状数、落边后核对项。

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `TS-L2-DS02-ENTITY-ARCH-DATA` |
| 图 diff | 本分册不改图 |
| 会签态 | 源文件无 frontmatter，记 `draft` |
| 说明 | 数据流图在 `sdd/l2/TS-L2-DS02-ENTITY-ARCH.md` 第 3 节 |

## 范围与实现

序号 22–27 的数据落点：

| 源 | 内容 |
|---|---|
| Nebula `demo_gkx_chain` | 点 `tech_point` / `tech_paper` / `tech_patent` / `tech_institution` / `tech_person`；边 `tech_has_paper` / `tech_has_patent` / `tech_has_institution` / `tech_has_person`。读图对这四种边不取属性，没有强度和年份 |
| `demo_gkxlumenx_ads.ads_technology_panorama_score` | 三列 `subject_id` VARCHAR(128)、`score_kind` VARCHAR(32)、`score_value` DOUBLE；主键 (`subject_id`, `score_kind`)；`score_kind` CHECK 闭集。本二级读 `influence` |

边由 `SYSINT-TECHGRAPH-02-L02` 写入。分数由 `TS-L2-DS02-SCORE-L01` 灌入。

## 偏离

文档本身无偏离。登记两处与说明书的落差：

1. 说明书 22、25、27 期待边上有强度和年份。读图对 `tech_has_*` 不取任何边属性，强度、年份都空。
2. 人的来源标记：方案写在 `tech_has_person` 边上；读图读的是人顶点的 `source_paper` / `source_topic`。

## 现状（截至 2026-11-05，另注 2026-11-06）

- 图上尚无技术点连实体的边。`SYSINT-TECHGRAPH-02-L01` 进行中；`L02`（边、路径、关联实体）backlog。
- 选中节点后按属性 WHERE 报 `IndexNotFound`，属查询缺口，归 `lumen-algo-py` 读图。2026-11-06 `07ffa9f` 改为当空，不再打断读图。
- 分数表人物影响力 0 行；`influence` 共 252,363 行（论文 108,337、专利 126,484、机构 17,542）。

## 产物清单

- `sdd/l2/TS-L2-DS02-ENTITY-DATA.md`
- 本 handoff

## 验收证据

- 分册已落盘：点表、边表（强度 / 年份列）、分数表列与主键、现状表、落边后三项核对。
- 名字对照 `tech_graph_read.py` `_ENTITIES`、`_entity_ngql()`、`_rel_ngql()`；表结构对照 `scripts/mysql/ads_technology_panorama_score.sql`；读法对照 `JdbcPanoramaScores.selectSql()`。
- 行数引自 `TS-L2-DS02-SCORE-L01` 交接（2026-11-05）。本会话未连库、未查图。
- 定义单，无业务 CI。未 commit。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ 不涉及计算 |
| 2 调用链 | ✅ 不改 |
| 3 图谱 Nebula | ✅ 只读 `demo_gkx_chain`，不写 `gkx_chain` / `entan` |
| 4 可观测 | ✅ 不新加 |
| 5 CI/CD | ✅ 定义文档 |
| 6 demo 只读 | ✅ 不读 demo 库填展示 |
| 7 共享聚合核心 | ✅ Java 只读 ADS |
| 8 数据策略 | ✅ ADS 表先行，mock 行填充 |
| 9 D8 | ✅ 不涉及 |
| 10 D9 | ✅ 影响力身份沿用 `M_TECH_ENTITY_INFLUENCE` |
| 11 D10 | ✅ 不涉及 |
| 12 D12 | ✅ 不调 `demo-*` |
| 13 D14 | ✅ 不写对象存储 |
| 14 D16 | ✅ 分数表不是 `gapfill_` 表，不写 ODS / DWD / 供应方库 |
| 15 D17 | ✅ 不改锁定算法 |
| 16 D18 | ✅ 新建 ADS 表、Python 灌 mock、Java 只读，D4 mock |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 35000（估算） |
| model_used | claude-opus |
| actual_cost | 0.95 |
| cost_warn | green |

按 architect 80/20、C 档 `$15/$75`：`35000×27/1e6 = 0.945`，记 `0.95`。

## 遗留风险

- L02 落边时边名、强度与年份属性名若与读图不一致，实体或强度会读空。
- 实体编号若与分数表 `subject_id` 不一致，影响力全空。
- 人物无点、无影响力行。

## CI/CD

- 分支：`gkx-orchestration` `dev`（未提交，等监管人确认）
- pipeline：编排仓无业务 CI
- K8s rollout：无

## 涉及文件

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-ENTITY-DATA.md`
- `agent-delivery/agent-handoffs/科学技术全景-DS02/TS-L2-DS02-ENTITY-DATA.md`
