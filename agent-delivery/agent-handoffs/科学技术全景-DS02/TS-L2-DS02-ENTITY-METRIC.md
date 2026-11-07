# TS-L2-DS02-ENTITY-METRIC · 科学技术全景 · 展示技术点关联实体 · 指标挂接

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:arch-agent`（兼 algorithm 分册） |
| supervised_by | `human:淮政玮` |
| claim_type | 监管人会话派单。本会话不改 task-registry，未经 MCP 认领 |
| 说明 | 只写文档。不改注册表，不改 D1–D4。不标 done |

## Ponytail

ponytail: off（定义任务）

不缩文档。未用 YAGNI 跳过 D9 身份、ⓘ、MockBadge。

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `TS-L2-DS02-ENTITY-ARCH-DATA` |
| 图 diff | 本分册不改图 |
| 会签态 | 源文件无 frontmatter，记 `draft` |
| 说明 | 分数表只供给影响力一个数，见架构分册第 3 节 |

## 范围与实现

序号 22–27 的指标挂接。2026-11-07 经 MCP `user-metric-registry` `metric-get` 查四个 ID：

| metric_id | 本二级 | D1 | D4 |
|---|---|---|---|
| `M_TECH_ENTITY_INFLUENCE` | 只作影响力列身份 | aligned | mock |
| `M_TECH_ENTITY_TOP5` | 不挂 | aligned | mock |
| `M_TECH_PAPER_PATENT_CNT` | 不挂 | aligned | mock |
| `M_TECH_ENTITY_REL` | 不挂（26 为 501 / 空） | aligned | mock |

影响力数来自 `ads_technology_panorama_score` 的 D18 mock 行，不是注册公式输出。界面 live 下 Top5 标题旁挂 `MetricSpecHint`（`M_TECH_ENTITY_INFLUENCE`）+ `MockBadge`。D4 保持 mock。

## 偏离

无偏离。与说明书 §5 一致。

补记：说明书写影响力注册口径为「IPC4 PageRank」，`metric-get` 的 `algorithm_type` 为 `third_party`，`update_freq` 为 `pending`。二者不冲突，本叶照实记录。

## 产物清单

- `sdd/l2/TS-L2-DS02-ENTITY-METRIC.md`
- 本 handoff

## 验收证据

- 四条 `metric-get` 均 `found.seed=true`、`found.matrix=true`、`srs_map=false`、`srs_refs=[]`。
- 未读 `metrics/registry/` 下 YAML，未改注册表。
- 页面挂接核对 `GraphAnalysisPanel.vue`：`metric-id="M_TECH_ENTITY_INFLUENCE"`、`MockBadge reason="D4 仍是 mock，分数来自灌数行"`。
- 定义单，无业务 CI。未 commit。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ 请求内不算影响力；灌数在 Python 脚本 |
| 2 调用链 | ✅ 不改 |
| 3 图谱 Nebula | ✅ 不涉及写图 |
| 4 可观测 | ✅ 不新加 |
| 5 CI/CD | ✅ 定义文档 |
| 6 demo 只读 | ✅ `algo_server_location` 指向 demo 仓只是注册索引，不改展示调用链 |
| 7 共享聚合核心 | ✅ Java 只读 ADS |
| 8 数据策略 | ✅ ADS mock 先行 |
| 9 D8 | ✅ 不改页面 |
| 10 D9 | ✅ 影响力数旁 ⓘ + MockBadge；不新造 id；`TEMP_DS02_*` 不当正式 ID |
| 11 D10 | ✅ 不改交互 |
| 12 D12 | ✅ 不调 `demo-*` |
| 13 D14 | ✅ 不涉及 |
| 14 D16 | ✅ 不用 `gapfill_` |
| 15 D17 | ✅ 不改唐绍祖锁定算法 |
| 16 D18 | ✅ 影响力只读新建 ADS 表 mock 行；公式未另签前 D4 不改 live |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 25000（估算） |
| model_used | claude-opus |
| actual_cost | 0.68 |
| cost_warn | green |

按 architect 80/20、C 档 `$15/$75`：`25000×27/1e6 = 0.675`，记 `0.68`。

## 遗留风险

- 人物影响力 0 行；图上无实体边，影响力暂无对象可填。
- 注册口径点是 IPC4，不是 `technology_node_id`。公式未由 `human:唐绍祖` 按技术点另签前，影响力不得改 live。

## CI/CD

- 分支：`gkx-orchestration` `dev`（未提交，等监管人确认）
- pipeline：编排仓无业务 CI
- K8s rollout：无

## 涉及文件

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-ENTITY-METRIC.md`
- `agent-delivery/agent-handoffs/科学技术全景-DS02/TS-L2-DS02-ENTITY-METRIC.md`
