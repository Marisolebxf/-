# TS-L2-DS02-GRAPH-DATA · 科学技术全景 · 展示技术点图谱 · 数据落点（as-built）

- 任务：`TS-L2-DS02-GRAPH-DATA`
- 日期：2026-11-07
- 监管：`human:淮政玮`
- 认领：`agent:arch-agent`（兼 data）
- 强度：ponytail off（定义任务，不缩文档）
- 状态：as-built 稿已落盘；四角色已会签（`sdd/l2/会签/TS-L2-DS02-L2SET-SIGNOFF-*.md`），未签收
- 2026-11-07 复查：图上已有技术点关系、关联实体与路径步。样本 `tcn_000f21ac06aceb9cdd0575e82d0d85fc` 用 `technology_node_id` 直调 Python 读图：关系 65、实体 61、路径 2。`path_priority` 仍 0 行。正文 11-05 的现状保留作记录，以本行为准。见 `工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS02-GRAPH-合规演示用例.md`
- 上游：说明书 §3、§4；`方案-算法中台基础数据准备.md`（`SYSINT-TECHGRAPH-02`，已签收方案另存）；`sdd/l2/TS-L2-DS02-GRAPH-ARCH.md`
- 核对代码：`lumen-algo-py` `lumen_common/algorithms/tech_graph.py`（写入 schema `_TAGS` / `_EDGES`）、`tech_graph_read.py`（读法）；`lumen-topic-py` `gkx_svc_service/jx_dict.py`（子学科收窄）

本分册只写序号 17–21 读哪些数据、由谁写入。不写 SQL、DDL、nGQL，不改库。

## 1. 图空间

| 项 | 值 |
|---|---|
| 库 | NebulaGraph（TRSGraph） |
| 空间 | `demo_gkx_chain`。读写两侧都拒绝别的空间 |
| 读法 | `lumen-algo-py` 只发 `MATCH`，不发写语句 |
| 不读 | `gkx_chain`、`entan`、燕大产业链全景、七要素 Tag |

## 2. 点

只读 Tag `tech_point`。VID = `tech_point:` + `technology_node_id`。

| 属性 | 写入类型 | 本二级读 | 用在 |
|---|---|---|---|
| `technology_node_id` | string | 读 | `nodes[].id`；选中点、按编号收窄 |
| `name_zh` | string | 读 | 显示名、搜索 `CONTAINS`。空就空 |
| `name_en` | string | 读 | 中文空时显示；搜索 `CONTAINS` |
| `community_role` | string | 读 | `nodes[].role`，关键节点样式 |
| `weighted_degree` | double | 读 | `nodes[].strength` |
| `community_id` | string | 不读 | — |
| `graph_release_id` | string | 不读 | — |
| `data_version` | string | 不读 | — |

需规序号 21 的「描述」「发展状态」「层级」在 `tech_point` 上没有属性。详情抽屉对应行空，不补文字。

`tech_paper`、`tech_patent`、`tech_institution`、`tech_person` 在同一次读里会读，但归序号 22–27，本分册不展开。

## 3. 边

只读 Edge `tech_rel`（`tech_point` ↔ `tech_point`，按无向 `MATCH`）。只在选中一个点后读。

| 属性 | 写入 schema 有无 | 本二级读 | 用在 |
|---|---|---|---|
| `relation_type` | 有 | 读 | `relations[].relationType`、`relationTypeOptions` |
| `evidence_level` | 有 | 读 | 默认只要 `HIGH`、`MEDIUM` |
| `relation_confidence_score` | 有 | 读 | `relations[].weight` |
| `first_evidence_year` | **无** | 读 | `relations[].year`。写入侧没有这一属性，`year` 会一直为空 |
| `direction_status` | 有 | 不读 | — |

`tech_path_step`、`tech_has_*` 归 22–33，本分册不展开。

## 4. 由谁写入

| 数据 | 按钮（算法中台 `/ops/tech-graph`） | 来源 | 任务 | 状态（2026-11-05） |
|---|---|---|---|---|
| `dwd_technology_graph_node` | 技术点入库 | `ads_technology_profile` 左连 `ads_technology_graph_node`，约 19,430 行 | `SYSINT-TECHGRAPH-02-L01` | 进行中，按钮已在 |
| Tag `tech_point` | 技术点入图 | 本侧 `dwd_technology_graph_node` | `SYSINT-TECHGRAPH-02-L01` | 进行中，图上已有点 |
| Edge `tech_rel`（HIGH、MEDIUM） | 技术点关系上图 | `ads_technology_graph_edge`（587,252 行） | `SYSINT-TECHGRAPH-02-L02` | backlog，图上无边 |
| Edge `tech_rel`（LOW） | 低证据关系上图 | 同一张边表 | `SYSINT-TECHGRAPH-02-L02` | backlog |

本二级不写任何一项。页面没有这些按钮，也不调用 `/ops/v1/tech-graphs/**`。

## 5. 领域筛选读的数据（as-built）

说明书 §3 写的是按挂产业表 `dwd_technology_topic_industry` 筛（`SYSINT-TECHGRAPH-02-L03`，backlog）。as-built 没有读这张表，改成子学科：

| 步 | 读什么 | 谁读 |
|---|---|---|
| 选项 | `ads_discipline_subfield` | `lumen-topic-py` op `subfield_list`，经 display `POST .../subfields` |
| 子学科 → 技术点 | `ads_technology_paper` 内连 `ads_discipline_topic`（`openalex_topic_id = primary_topic_id`），按 `subfield_id` 取去重 `technology_node_id` | `lumen-topic-py` op `technology_graph_subfield_nodes` |
| 收窄 | 下发 `technology_node_ids`（最多 200）给读图 | display → Python |

这是 MySQL 只读，不进 Nebula，不写挂产业表。读的库是 `lumen-topic-py` `jx_dict.py` 的 `JX_ADS_DATABASE`，默认 `gkx_technology_analysis_dev`，主机 `JX_ADS_HOST` 默认 `47.93.119.170`。不是 `demo_gkxlumenx_ads`，也不是供应方库 `gkx`。该库 `ads_technology_paper.technology_node_id` 与图上 `tech_point.technology_node_id` 是否同一批编号，本稿未核。记偏离，四角色同意 as-built，口径转客户决策清单。

## 6. 没有边时的表现

| 情形 | 接口 | 页面 |
|---|---|---|
| 未选点 | 本来就不查边，`relations=[]` | 网格布局画最多 200 个技术点（`b603e63`） |
| 选中点，图上无 `tech_rel` | `relations=[]`，`relationTypeOptions=[]`，不算失败 | 只画点；关系类型下拉空 |
| 边有但缺 `evidence_level` | 默认过滤掉，`relations=[]` | 同上 |
| `factorItems` | 有点时只有「技术点」一项 | 图例一项 |

不用种子关系补线，不现算关系。

## 7. 现状（截至 2026-11-05）

- 图上已有技术点等点。尚无技术点关系边（`tech_rel`）、技术点连实体边（`tech_has_*`）、路径步边（`tech_path_step`）。
- `SYSINT-TECHGRAPH-02-L01` 进行中；`L02`（边、路径、关联实体）backlog。
- 选中节点后读图按属性 `WHERE` 报 `IndexNotFound`（查询缺口）：`tech_point.technology_node_id`、`tech_paper.technology_node_id` 等属性等值或 `CONTAINS` 扫描没有 Tag 索引。2026-11-06 `07ffa9f` 把这一错误当空，未建索引。读图语句把 `id(a) == "tech_point:…"` 与属性等值写在同一个 `OR` 里，整条报错时整条当空。搜索走属性 `CONTAINS`，领域收窄走 `v.tech_point.technology_node_id IN [...]`，同样依赖索引，可能静默为空（对外是 `GRAPH_EMPTY`）。写入侧 `tech_graph.py` 的注释也记了「WHERE 在 `demo_gkx_chain` 上会 IndexNotFound」。本稿未在线上复测。补索引或改按 VID 查，未建单。
- 前端无边时用网格布局画技术点（`b603e63`）。

## 8. 明确不做

- 不写 SQL、DDL、nGQL，不建索引。
- 不读 demo 库给 lumen 填数，不把 `mock/modules/panorama.ts` 灌进图。
- 不读 `gapfill_` 表，不写 ODS / DWD / ADS。
- 不改 `方案-算法中台基础数据准备.md`。
