# TS-L2-DS02-PATH-DATA · 科学技术全景 · 展示关键路径和关键节点 · 数据落点

ponytail: off（定义任务）

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent`（arch-agent 代写） |
| supervised_by | `human:淮政玮` |
| claim_type | 派单直写。本会话未调用 task-registry，未改状态 |
| 说明 | 只写数据分册。不写 SQL、不改库、不灌数、不 commit，不标 done |

## Ponytail

ponytail: off（定义任务）

定义任务，不缩文档。未用 YAGNI 跳过 D18 表结构、步序规则、现状。

## 范围与实现

序号 28–33 读两处数据：

- 图：Nebula `demo_gkx_chain`。边 `tech_path_step`（`tech_point` → `tech_point`），起点键 `previous_technology_node_id`、终点键 `technology_node_id`，属性 `path_id`（string）、`step_order`（int），rank 按 `path_id:step_order` 的 crc32。上游 `ads_technology_evolution_path_step`。端点属性 `technology_node_id`、`name_zh`、`name_en`、`community_role`、`weighted_degree`。读图按 `step_order` 升序组 `nodes[]`。
- 分数表：`demo_gkxlumenx_ads.ads_technology_panorama_score`，D18 mock。列 `subject_id` VARCHAR(128)、`score_kind` VARCHAR(32)（CHECK `influence` / `centrality` / `path_priority`）、`score_value` DOUBLE，主键 (`subject_id`, `score_kind`)。本二级用 `centrality`（技术点编号，40.000–48.999）和 `path_priority`（`path_id`，70.000–78.999）。
- 灌数：`seed_technology_panorama_score.py`，sha256 可重复 mock；技术点分页扫全量；路径扫全部 `tech_path_step` 按 `path_id` 归组；先删后插，单事务。
- 路径由 `SYSINT-TECHGRAPH-02-L02` 写入。

现状（截至 2026-11-05）：`tech_point` 19430；`tech_path_step` 0；`centrality` 19430 行；`path_priority` 0 行；L01 in_progress，L02 backlog。

## 偏离

无偏离。as-built 风险登记在分册第 6 节：

- Java→Python 选中键不一致，L02 写入后路径仍读不回。
- 读图只带局部步，灌数按整条路径给分；编号相同，分数可对上。
- `path_id` 为空会退成单步编号，L02 须保证非空。

## 产物清单

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-PATH-DATA.md`
- 本 handoff
- 业务仓：无改动

## 验收证据

- 分册已落盘：两处数据、边规格、端点属性、读取范围、表结构、灌数规则、现状、边界、风险。
- 只读核对：`lumen-algo-py` `lumen_common/algorithms/tech_graph.py`（`tech_path_step` 写边规格与 rank）、`tech_graph_read.py`（`_path_ngql`、`_path_option`、`_step`）、`scripts/mysql/ads_technology_panorama_score.sql`、`scripts/seed/seed_technology_panorama_score.py`（`mock_value`、`_graph_rows`、`_path_options`、`apply`）。
- 现状数字取自 `TS-L2-DS02-SCORE-L01` handoff 的 `--apply` 结果。本会话未连库、未连图。
- 定义单，无 CI。未 commit。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ 灌数在 Python 脚本 |
| 2 调用链 | ✅ Java 只读 ADS，不读图 |
| 3 图谱 NebulaGraph | ✅ 只用 `demo_gkx_chain`；不读 `gkx_chain`、`entan` |
| 4 可观测 | ✅ 不新增 |
| 5 CI/CD | ✅ 定义文档 |
| 6 demo 只读 | ✅ 不用 demo 种子灌图 |
| 7 共享聚合核心 | ✅ 不涉及 |
| 8 数据策略 | ✅ ADS mock 先行，路径来自入图 |
| 9 D8 | ✅ 不涉及 |
| 10 D9 | ✅ 两列对应已有 `metric_id`，不新造 |
| 11 D10 | ✅ 不涉及 |
| 12 D12 | ✅ 不调用 `demo-*` 服务 |
| 13 D14 | ✅ 不涉及对象存储 |
| 14 D16 | ✅ 表名无 `gapfill_`，不写 ODS / DWD / 供应方库 |
| 15 D17 | ✅ 不涉及 |
| 16 D18 | ✅ 新建 ADS 表 + Python 灌 mock + Java 只读；D4 保持 mock |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 20000（估算） |
| model_used | claude-opus |
| actual_cost | 0.54 |
| cost_warn | green |

按 data 80/20、`$15/$75` 每百万：`20000×0.8×15/1e6 + 20000×0.2×75/1e6 = 0.54`。无控制台分项。

## 遗留风险

- L02 未开工，路径与 `path_priority` 均为空。
- L02 写入后须重跑 `--apply`，并实测读图带回路径。

## 涉及文件

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-PATH-DATA.md`
- `agent-delivery/agent-handoffs/科学技术全景-DS02/TS-L2-DS02-PATH-DATA.md`
