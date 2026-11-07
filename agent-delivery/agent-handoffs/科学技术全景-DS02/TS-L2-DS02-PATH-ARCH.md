# TS-L2-DS02-PATH-ARCH · 科学技术全景 · 展示关键路径和关键节点 · 实现架构

ponytail: off（定义任务）

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 派单直写。本会话未调用 task-registry，未改状态 |
| 说明 | 只写文档。不写代码、不改库、不 commit、不改注册表，不标 done |

## Ponytail

ponytail: off（定义任务）

定义任务，不缩文档。未用 YAGNI 跳过调用链、D12、D18、空态与上限。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `TS-L2-DS02-PATH-ARCH-SEQ`、`TS-L2-DS02-PATH-ARCH-DATA` |
| 图 diff | 新增二级两张图：关键路径一次 `graph` 的五跳调用链；路径步从 L02 进图、`path_priority` 由灌数脚本按 `path_id` 写入。与说明书第 3、4 节语义一致，未改上级图 |
| 会签态 | 源文件无 frontmatter，记 `draft`。待四角色会签 |
| 说明 | 图在 `sdd/l2/TS-L2-DS02-PATH-ARCH.md` 第 2、3 节 |

## 范围与实现

对照 SRS「科学技术全景」二级「展示关键路径和关键节点」序号 28–33，说明书第 2.3 节逐叶。按已实现写 as-built：

- 调用链：页面 → 网关 `/display/**` → `gkxlumen-display` `POST /v1/situation/panorama/graph` → `lumen-algo-py` `POST /internal/tech-graph/read` → `demo_gkx_chain`；中心度、路径优先级由 display 按编号只读 `demo_gkxlumenx_ads.ads_technology_panorama_score`。
- 六叶流程：28 读路径步；29 样式用 `role` / `strength`，中心度读分数表；30 侧栏显示步序与端点名；31 重要性读 `pathPriority`；32 页面比较 2–5 条；33 页面按步播放、可调速暂停。
- 空态与失败态八种，路径区空时图谱和实体保留。
- 上限：路径 20 条、单次 168 步、分数编号 400 个。
- 现状（截至 2026-11-05）：图上无路径步边，L01 in_progress，L02 backlog，`path_priority` 0 行，`centrality` 19430 行。

## 偏离

无设计偏离。未重开说明书决策，未新增接口，未新造 `metric_id`。

as-built 核对发现五处与说明书或跨仓代码不一致，已登记在分册第 8 节，本单不改代码：

1. Java 发 `techPointId`，Python 只认 `technology_node_id` / `technologyNodeId`。完整链路下路径区恒空。
2. Python 只取与选中点相连的步，不补整条路径。
3. Java 不透传 Python 的 `truncated`，路径截断标记不出现。
4. 页面重要性筛选只判有无 `pathPriority`，不按数值分档。
5. 分数只填顶层 `nodes[]`，不填路径内节点。

## 产物清单

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-PATH-ARCH.md`
- 本 handoff
- 业务仓：无改动

## 验收证据

- 分册已落盘，含范围、调用链 Mermaid、数据流 Mermaid、六步流程、空态失败态表、上限表、现状、不一致清单。
- 只读核对的代码：`lumen-algo-py` `tech_graph_read.py`、`tech_graph.py`；`lumen-svc-platform` `SituationPanoramaService.java`、`TechGraphReadAdapter.java`、`JdbcPanoramaScores.java`；`lumen-ui-science-pc` `liveGraph.ts`、`index.vue`、`GraphAnalysisPanel.vue`。
- `git log` 只读核对：读图最近提交 `07ffa9f`，display 装配最近提交 `271109c`。
- 定义单，无 CI，无 PR。未 commit。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ Java 不算中心度、关键节点、优先级；Python 也只读不算，数来自 D18 mock 表 |
| 2 调用链 | ✅ 前端 → 网关 → `gkxlumen-display` → `lumen-algo-py` `/internal/tech-graph/read`，不越层 |
| 3 图谱 NebulaGraph | ✅ 只读 `demo_gkx_chain`，Java 不写 nGQL，不经 `gkxlumen-graph`，无 Neo4j |
| 4 可观测 | ✅ 沿用 display Java Agent、Python `TraceHeaderMiddleware`、前端 `@/utils/request` trace 头；本叶不新增 |
| 5 CI/CD | ✅ 定义文档，无业务 CI |
| 6 demo 只读 | ✅ 未 merge demo，未读 demo 代码作契约 |
| 7 共享聚合核心 | ✅ 不涉及专题前端 |
| 8 数据策略 | ✅ 分数只读 ADS 表；路径来自已入图数据 |
| 9 D8 | ✅ 未改页面，沿用 `FE-TS-02A` 区域 |
| 10 D9 | ✅ 两个数字旁 ⓘ + MockBadge；不新造 `metric_id` |
| 11 D10 | ✅ 未改交互 |
| 12 D12 | ✅ 不调用任何 `demo-*`；Feign 名 `lumen-platform-algo-py` |
| 13 D14 | ✅ 不涉及对象存储 |
| 14 D16 | ✅ 不用 `gapfill_` |
| 15 D17 | ✅ 不动合规算法闭包 |
| 16 D18 | ✅ 两个数字只读新建 ADS 表 mock 行，接口不写死 mock；D4 保持 mock |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 30000（估算） |
| model_used | claude-opus |
| actual_cost | 0.81 |
| cost_warn | green |

按 architect 80/20、`$15/$75` 每百万：`30000×0.8×15/1e6 + 30000×0.2×75/1e6 = 0.81`。无控制台分项。本会话未改 task-registry，四字段待 coordinator 回填。

## 遗留风险

- 第 1 条键名不一致不修，L02 入图后路径区仍空。需派 `SYSINT-05-01B-L01` 或读图单返修。
- 「整条路径」还是「局部路径」说明书未定，需会签定口径。
- 重要性分档线未定，需产品定。

## 涉及文件

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-PATH-ARCH.md`
- `agent-delivery/agent-handoffs/科学技术全景-DS02/TS-L2-DS02-PATH-ARCH.md`
