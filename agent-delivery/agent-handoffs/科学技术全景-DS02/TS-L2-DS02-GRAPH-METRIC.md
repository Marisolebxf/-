# TS-L2-DS02-GRAPH-METRIC · 科学技术全景 · 展示技术点图谱 · 指标挂接 as-built

ponytail: off（定义任务）

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent`（兼 algorithm） |
| supervised_by | `human:淮政玮` |
| claim_type | 派单直写。本单不改 task-registry |
| 说明 | as-built 稿已落盘，待四角色会签，未签收。不标 done |

## Ponytail

ponytail: off（定义任务）

不缩文档。未用 YAGNI 跳过 D9 ⓘ / MockBadge 对照。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | 无。本分册无图 |
| 图 diff | 无 |
| 会签态 | — |
| 说明 | 调用链见 `sdd/l2/TS-L2-DS02-GRAPH-ARCH.md` |

## 范围与实现

序号 17–21 不挂任何 `metric_id`。`M_TECH_GRAPH_STRUCT`（序号 18 图结构）、`M_TECH_EDGE_STRENGTH`（连线权重）不挂：注册口径是 IPC4 域，不是 `tech_point`。画布和权重用图上已有点、边属性。

2026-11-07 经 MCP `metric-registry` `metric-get` 查三条：

| metric_id | D1 | D4 | 本二级 |
|---|---|---|---|
| `M_TECH_GRAPH_STRUCT` | aligned | mock | 不挂 |
| `M_TECH_EDGE_STRENGTH` | aligned | mock | 不挂 |
| `M_TECH_PATH_CENTRALITY` | aligned | mock | 不挂，归 29 |

## 偏离

无设计偏离。as-built 记录一处 D9 缺口：序号 21 详情抽屉（`index.vue` `buildGraphNodeDetail`）有「中心度」卡，取自分数表 `centrality`（身份 `M_TECH_PATH_CENTRALITY`，D4 mock），旁边无 ⓘ、无 MockBadge。同卡组的「关系强度」实际是点的 `weighted_degree`，名称与内容不符。处理口径（补 ⓘ + MockBadge，或从抽屉移除）交会签。

## 产物清单

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-GRAPH-METRIC.md`
- 本 handoff

## 验收证据

- 三条 `metric-get` 返回 `found.seed=true`、`found.matrix=true`；`algorithm_type=third_party`；D4 全为 mock。未读 `metrics/registry/` YAML。
- 前端走查：`GraphAnalysisPanel.vue` 中心度、影响力、路径优先级旁有 ⓘ 与 MockBadge；`index.vue` 详情抽屉中心度卡没有。
- 定义单，无业务代码，无 CI。未 commit。

## 架构合规自检

| 公约 §2 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ 请求内不算任何指标 |
| 2 调用链 | ✅ 不涉及新跳 |
| 3 图谱 Nebula | ✅ 只读 `demo_gkx_chain` 已有属性 |
| 4 可观测 | ✅ 不涉及 |
| 5 CI/CD | ✅ 定义稿，`cicd: skip` |
| 6 demo2 只读 merge | ✅ 无 merge |
| 7 共享聚合核心 | ✅ 分数只读 ADS |
| 8 数据策略 | ✅ 不造数 |
| 9 D8 | ✅ 不涉及 |
| 10 D9 | ⚠️ 不新造 `metric_id`，不改 D4。抽屉中心度卡缺 ⓘ / MockBadge，待会签 |
| 11 D10 | ✅ 不涉及 |
| 12 D12 | ✅ 不调用 `demo-*`。注册表 `algo_server_location` 指向 `demo-algo-science`，本页不调用它 |
| 13 D14 | ✅ 不涉及 |
| 14 D16 | ✅ 不涉及 |
| 15 D17 | ✅ 不改合规算法；不出 `-合规` / `-合理` 展示名 |
| 16 D18 | ✅ `centrality` 只来自分数表 mock 行，D4 保持 mock |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 20000（估算） |
| model_used | claude-opus |
| actual_cost | 0.54 |
| cost_warn | green |

按 C 档 `$15/$75`、80/20：`20000×0.8×15/1e6 + 20000×0.2×75/1e6 = 0.54`。本单不写 registry。

## 未做事项

- 未改前端抽屉，未补 ⓘ。
- 未改注册表、seed、矩阵。未 commit，未改 task-registry。
