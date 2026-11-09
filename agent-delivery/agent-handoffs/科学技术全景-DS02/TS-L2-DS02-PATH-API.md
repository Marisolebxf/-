# TS-L2-DS02-PATH-API · 科学技术全景 · 展示关键路径和关键节点 · 后台接口设计

ponytail: off（定义任务）

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent`（arch-agent 代写） |
| supervised_by | `human:淮政玮` |
| claim_type | 派单直写。本会话未调用 task-registry，未改状态 |
| 说明 | 只写接口分册。不写代码、不改库、不 commit、不改注册表，不标 done |

## Ponytail

ponytail: off（定义任务）

定义任务，不缩文档。未用 YAGNI 跳过下游读图、分数只读、501 与空态的差别。

## 范围与实现

序号 28–33 只用一条公开资源 `POST /display/v1/situation/panorama/graph`。不新增接口。

| 七字段 | 本二级 |
|---|---|
| `keyPathOptions` | 主块：路径列表、详情、筛选、比较候选、播放步 |
| `nodes` | 关键节点样式（`role` / `strength`）与中心度格（`centrality`） |
| `timeline` | 只用 `currentYear` 作游标 |
| `relations`、`listRecords`、`relationTypeOptions`、`factorItems` | 不用 |

- 请求：页面发 `selectedNodeId`、`keyword`、`selectedFieldValues`、`timeRange`、`currentYear=null`。写动作与 `entityRelations=true` 直接 501。
- 响应 `keyPathOptions[]`：`id`（`path_id`）、`name` / `title`、`summary`（空）、`rank`、`stageIds`、`nodes[]`（`id`、`name`、`name_zh`、`role`、`strength`、`stageKey`、`typeKey`、`graphNodeId`）、`relationIds`（空）、`pathPriority`（分数表，无行 `null`）。最多 20 条。
- 下游 `POST /internal/tech-graph/read`：只读 `demo_gkx_chain`；路径查询 `tech_path_step`，返回 `path_id`、`step_order` 与两端点属性；`LIMIT 168`；按 `path_id` 归组、`step_order` 排序；最多 20 条。空间不对 422，nGQL 失败 503。
- 分数：`JdbcPanoramaScores` 对 `demo_gkxlumenx_ads.ads_technology_panorama_score` 按 `subject_id` 只读；`centrality` → `nodes[].centrality`，`path_priority` → `keyPathOptions[].pathPriority`。表不在或连不上，两格 `null`，HTTP 仍 200。

## 偏离

无设计偏离。as-built 不一致登记在分册第 9 节：

- Java 发 `techPointId`，Python 不认，完整链路不回路径。
- Java 不透传 Python `truncated`。
- Python 不读 Java 发的 `limits`（值相同，暂无影响）。
- 路径只带与选中点相连的步。

## 产物清单

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-PATH-API.md`
- 本 handoff
- 业务仓：无改动

## 验收证据

- 分册已落盘：公开资源、七字段用法、请求、`keyPathOptions` 字段表、`centrality`、下游读图、分数只读、空态对照、不一致清单。
- 字段名逐个对照 `SituationPanoramaService.java`（`query`、`assemble`、`overlay`）、`TechGraphReadAdapter.java`、`JdbcPanoramaScores.java`、`tech_graph_read.py`（`_path_ngql`、`_path_option`、`_load_paths`）、`views/tech_graph_read.py`、`liveGraph.ts`（`graphReadParams`、`filterLivePath`）。
- 定义单，无 CI，无 PR。未 commit。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ Java 只装配，不算分；Python 读图不算分 |
| 2 调用链 | ✅ 浏览器只打 `/display/**`；display → `/internal/tech-graph/read` |
| 3 图谱 NebulaGraph | ✅ `demo_gkx_chain` 只读；Java 不写 nGQL |
| 4 可观测 | ✅ 沿用现有 trace 传递，本叶不新增观测点 |
| 5 CI/CD | ✅ 定义文档，无业务 CI |
| 6 demo 只读 | ✅ 未引用 demo 接口作契约 |
| 7 共享聚合核心 | ✅ 不涉及 |
| 8 数据策略 | ✅ 只读 ADS |
| 9 D8 | ✅ 不改页面 |
| 10 D9 | ✅ 不新造 `metric_id`，两个数字带身份 |
| 11 D10 | ✅ 不改交互 |
| 12 D12 | ✅ 下游只有 `lumen-platform-algo-py` 与 lumen ADS，无 `demo-*` |
| 13 D14 | ✅ 不涉及对象存储 |
| 14 D16 | ✅ 不用 `gapfill_` |
| 15 D17 | ✅ 不动合规算法 |
| 16 D18 | ✅ 分数只读 mock 表，Java 剥掉 Python 自带分数，不写死 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 25000（估算） |
| model_used | claude-opus |
| actual_cost | 0.68 |
| cost_warn | green |

按 api 80/20、`$15/$75` 每百万：`25000×0.8×15/1e6 + 25000×0.2×75/1e6 = 0.675`，记 0.68。无控制台分项。

## 遗留风险

- 键名不一致修复前，路径相关字段在线上恒为空。
- `keyPathOptions` 字段未冻结为 DTO，后续改名需同步三仓。

## 涉及文件

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-PATH-API.md`
- `agent-delivery/agent-handoffs/科学技术全景-DS02/TS-L2-DS02-PATH-API.md`
