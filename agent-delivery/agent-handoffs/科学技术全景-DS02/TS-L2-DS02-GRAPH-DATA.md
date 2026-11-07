# TS-L2-DS02-GRAPH-DATA · 科学技术全景 · 展示技术点图谱 · 数据落点 as-built

ponytail: off（定义任务）

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent`（兼 data） |
| supervised_by | `human:淮政玮` |
| claim_type | 派单直写。本单不改 task-registry |
| 说明 | as-built 稿已落盘，待四角色会签，未签收。不标 done |

## Ponytail

ponytail: off（定义任务）

不缩文档。未用 YAGNI 跳过写入方对照和无边表现。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `TS-L2-DS02-GRAPH-DATA` |
| 图 diff | 本分册不改图 |
| 会签态 | 源文件无 frontmatter，记 `draft` |
| 说明 | 图在 `sdd/l2/TS-L2-DS02-GRAPH-ARCH.md` 第 3 节 |

## 范围与实现

序号 17–21 只读 Nebula `demo_gkx_chain`：

- Tag `tech_point`：读 `technology_node_id`、`name_zh`、`name_en`、`community_role`、`weighted_degree`。由 `SYSINT-TECHGRAPH-02-L01`「技术点入库」+「技术点入图」写入。
- Edge `tech_rel`：读 `relation_type`、`evidence_level`、`relation_confidence_score`、`first_evidence_year`。由 `SYSINT-TECHGRAPH-02-L02`「技术点关系上图」「低证据关系上图」写入（backlog）。

没有边时：`relations=[]`，不算失败，前端网格布局画点。领域筛选 as-built 读 MySQL `ads_discipline_subfield`、`ads_technology_paper` ⋈ `ads_discipline_topic`（经 `lumen-topic-py`），不读挂产业表。

## 偏离

无设计偏离。as-built 记录：

1. 领域筛选按子学科，不按说明书 §3 的挂产业表 `dwd_technology_topic_industry`。
2. 读图读 `tech_rel.first_evidence_year`，写入 schema 没有这一属性，`year` 恒空。
3. `tech_point` 没有「描述」「发展状态」「层级」属性，序号 21 对应行空。
4. 属性扫描无 Tag 索引，`IndexNotFound` 自 `07ffa9f` 起被当空。

## 产物清单

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-GRAPH-DATA.md`
- 本 handoff

## 验收证据

- 分册已落盘：点属性表、边属性表、写入方表、子学科读路径表、无边表现表、现状小节。
- 读写两侧 schema 对过 `tech_graph.py` `_TAGS` / `_EDGES` 与 `tech_graph_read.py` 读语句；子学科 SQL 对过 `jx_dict.py` `technology_graph_subfield_nodes`。
- 未连库、未连图，现状沿用 2026-11-05 已知事实。未 commit。

## 架构合规自检

| 公约 §2 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ 读图在 `lumen-algo-py`；子学科 SQL 在 `lumen-topic-py` |
| 2 调用链 | ✅ 前端 → Java → Python `/internal/*` → 图 / MySQL |
| 3 图谱 Nebula | ✅ `demo_gkx_chain`，只读 |
| 4 可观测 | ✅ 不涉及新跳 |
| 5 CI/CD | ✅ 定义稿，`cicd: skip` |
| 6 demo2 只读 merge | ✅ 无 merge |
| 7 共享聚合核心 | ✅ Java 不直连图库 |
| 8 数据策略 | ✅ 点未写入时空，不灌种子 |
| 9 D8 | ✅ 不涉及 |
| 10 D9 | ✅ 不涉及指标落点 |
| 11 D10 | ✅ 不涉及 |
| 12 D12 | ✅ 不读 demo 服务；算法中台 `demo-ui-system-test` 只负责写图，展示链不调用它 |
| 13 D14 | ✅ 不写对象存储 |
| 14 D16 | ✅ 不读写 `gapfill_` |
| 15 D17 | ✅ 不涉及 |
| 16 D18 | ✅ 本二级无 mock 数字落表 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 20000（估算） |
| model_used | claude-opus |
| actual_cost | 0.54 |
| cost_warn | green |

按 C 档 `$15/$75`、80/20：`20000×0.8×15/1e6 + 20000×0.2×75/1e6 = 0.54`。本单不写 registry。

## 未做事项

- 未建索引，未改读写 schema，未连库复测。
- 未改 `方案-算法中台基础数据准备.md`。未 commit，未改 task-registry。
