# TS-L2-DS02-PATH-METRIC · 科学技术全景 · 展示关键路径和关键节点 · 指标挂接

ponytail: off（定义任务）

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent`（arch-agent 代写） |
| supervised_by | `human:淮政玮` |
| claim_type | 派单直写。本会话未调用 task-registry，未改状态 |
| 说明 | 只写指标分册。不改注册表、不改 D4、不 commit，不标 done |

## Ponytail

ponytail: off（定义任务）

定义任务，不缩文档。未用 YAGNI 跳过 ⓘ、MockBadge、D1–D4 现状。

## 范围与实现

序号 28–33 的指标挂接：

| metric_id | 本二级 |
|---|---|
| `M_TECH_PATH_CENTRALITY` | 只作中心度列身份（序号 29） |
| `M_TECH_PATH_PRIORITY` | 只作路径优先级列身份（序号 31） |
| `M_TECH_PATH_KEYNODE` | 不挂。关键节点样式用点上 `role` / `strength` |

2026-11-07 经 MCP `metric-get` 查询：三条 `algorithm_type=third_party`，D1 aligned，D2 partial（provisional），D3 partial，D4 mock，`srs_refs` 空。口径对象是深圳 IPC4 238 点，不是本页 `tech_point`，所以请求内不调用计算，mock 行不算这些函数的输出。

页面现状：中心度两处、路径优先级一处挂 `MetricSpecHint` + `MockBadge`。无行则格子空。

数据现状（截至 2026-11-05）：`centrality` 19430 行，`path_priority` 0 行。

## 偏离

无偏离。注册表侧三处偏差只登记、不改：`ui_mount` 写的是科技专题 TOPIC-TECH-05；`srs_refs` 未回填 29、31；`algo_server_location` 指向 `demo-algo-science`（本页不调用）。

## 产物清单

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-PATH-METRIC.md`
- 本 handoff
- 业务仓：无改动

## 验收证据

- `GetDynamicTools` namespace=`user-metric-registry` 取 `metric-get` schema；`CallDynamicTool` `metric-get` 三次（`M_TECH_PATH_CENTRALITY`、`M_TECH_PATH_PRIORITY`、`M_TECH_PATH_KEYNODE`），均 `found.seed=true`、`found.matrix=true`。
- 未读 `metrics/registry/` 下任何 YAML。
- 页面角标核对 `GraphAnalysisPanel.vue` 中 `metric-id` 与 `MockBadge`。
- 定义单，无 CI。未 commit。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ 不在请求里算三条指标 |
| 2 调用链 | ✅ 数字经 display 只读 ADS 进入页面 |
| 3 图谱 NebulaGraph | ✅ 不涉及图写入 |
| 4 可观测 | ✅ 不新增 |
| 5 CI/CD | ✅ 定义文档 |
| 6 demo 只读 | ✅ 不调用 `demo-algo-science` 的计算 |
| 7 共享聚合核心 | ✅ 不涉及 |
| 8 数据策略 | ✅ ADS mock 先行 |
| 9 D8 | ✅ 不改页面 |
| 10 D9 | ✅ 每个数字旁 ⓘ + MockBadge；不新造 `metric_id`；八件套经 MCP 查询 |
| 11 D10 | ✅ 不改交互 |
| 12 D12 | ✅ 不调用 `demo-*` |
| 13 D14 | ✅ 不涉及 |
| 14 D16 | ✅ 不用 `gapfill_` |
| 15 D17 | ✅ 不动合规算法闭包 |
| 16 D18 | ✅ mock 只在 ADS 表；D4 保持 mock |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 20000（估算） |
| model_used | claude-opus |
| actual_cost | 0.54 |
| cost_warn | green |

按 algorithm 80/20、`$15/$75` 每百万：`20000×0.8×15/1e6 + 20000×0.2×75/1e6 = 0.54`。无控制台分项。

## 遗留风险

- D4 改 live 须唐绍祖按技术点另签公式，本叶不推进。
- `path_priority` 要等 L02 写入路径后重跑灌数才有行。

## 涉及文件

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-PATH-METRIC.md`
- `agent-delivery/agent-handoffs/科学技术全景-DS02/TS-L2-DS02-PATH-METRIC.md`
