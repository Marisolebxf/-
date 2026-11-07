# TS-L2-DS02-GRAPH-API · 科学技术全景 · 展示技术点图谱 · 后台接口 as-built

ponytail: off（定义任务）

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent`（兼 api） |
| supervised_by | `human:淮政玮` |
| claim_type | 派单直写。本单不改 task-registry |
| 说明 | as-built 稿已落盘，待四角色会签，未签收。不标 done |

## Ponytail

ponytail: off（定义任务）

不缩文档。未用 YAGNI 跳过 501、502 与 `GRAPH_EMPTY` 的区分，也未跳过下游字段对照。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `TS-L2-DS02-GRAPH-SEQ` |
| 图 diff | 本分册不改图 |
| 会签态 | 源文件无 frontmatter，记 `draft` |
| 说明 | 图在 `sdd/l2/TS-L2-DS02-GRAPH-ARCH.md` 第 2 节 |

## 范围与实现

序号 17–21。公开资源只用已有 `POST /display/v1/situation/panorama/graph`；序号 17 的 `/import`、`/manual` 与带写入动作的 `/graph` 为 501。

七个字段里本二级用 `nodes`、`relations`、`relationTypeOptions`、`factorItems`；`timeline`、`listRecords`、`keyPathOptions` 归 22–33。请求字段按前端实发（`selectedFieldValues`、`keyword`、`selectedNodeId`、`currentYear=null`、`timeRange`）与 Java 别名列全。空态 `emptyReason=GRAPH_EMPTY`；读失败 502；写入 501。下游 `POST /internal/tech-graph/read` 的入参、Python 实际读取字段、响应与状态码逐项对照。

## 偏离

无设计偏离，不新增接口。as-built 记录：

1. `POST /v1/situation/panorama/subfields`（2026-11-06 `271109c`）说明书未列，只记录不设计。
2. **入参字段不一致**：display 下发 `techPointId`，Python 只认 `technology_node_id` / `technologyNodeId`。选中点后关系、实体、路径恒空。两侧单测各用各的字段名，未覆盖这一跳。
3. Java 丢弃 Python `truncated`，公开响应看不到 Python 侧超限。
4. Python 不读 `fieldValues`、`limits`；上限两侧写死一致。

## 产物清单

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-GRAPH-API.md`
- 本 handoff

## 验收证据

- 分册已落盘：公开资源表、请求字段两张表、响应字段表、空态失败态表、下游入参出参表、截断说明。
- 字段名逐个对过 `SituationPanoramaController`、`SituationPanoramaService`、`TechGraphReadAdapter`、`RemoteTechGraphClient`、`views/tech_graph_read.py`、`algorithms/tech_graph_read.py`、`liveGraph.ts`、`panorama.ts`。
- 定义单，无业务代码，无 PR，无 CI。未 commit。

## 架构合规自检

| 公约 §2 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ 读图与 nGQL 在 `lumen-algo-py`；Java 不打分 |
| 2 调用链 | ✅ 浏览器只打 `/display/**`；display → Python `/internal/tech-graph/read` |
| 3 图谱 Nebula | ✅ `space` 固定 `demo_gkx_chain`，不对则 422 / 502 |
| 4 可观测 | ✅ 沿用既有 trace 头与中间件，不新设观测点 |
| 5 CI/CD | ✅ 定义稿，`cicd: skip` |
| 6 demo2 只读 merge | ✅ 无 merge |
| 7 共享聚合核心 | ✅ 前端只调 Java；Java 不直连图库 |
| 8 数据策略 | ✅ 接口不返回 fixture，不再返回 `GRAPH_NOT_READY` |
| 9 D8 | ✅ 不涉及视觉 |
| 10 D9 | ✅ 不新造 `metric_id`；`centrality` 身份见 METRIC 分册 |
| 11 D10 | ✅ 不涉及 |
| 12 D12 | ✅ Feign 只指向 `lumen-platform-algo-py`、`gkxlumen-platform-search-py`，不调用 `demo-*`，不经 `gkxlumen-graph` |
| 13 D14 | ✅ 不写对象存储 |
| 14 D16 | ✅ 不涉及 `gapfill_` |
| 15 D17 | ✅ 不改合规算法 URL |
| 16 D18 | ✅ 分数只读 ADS；Python 载荷自带分数先剥掉 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 25000（估算） |
| model_used | claude-opus |
| actual_cost | 0.68 |
| cost_warn | green |

按 C 档 `$15/$75`、80/20：`25000×0.8×15/1e6 + 25000×0.2×75/1e6 = 0.675`，记 `0.68`。本单不写 registry。

## 未做事项

- 未改控制器、Feign、Python 视图；未修 `techPointId` 字段名。
- 未打线上接口，没有状态码实测。
- 未冻结 OpenAPI。未 commit，未改 task-registry。
