# TS-L2-DS02-PATH-METRIC · 科学技术全景 · 展示关键路径和关键节点 · 指标挂接

- 任务：`TS-L2-DS02-PATH-METRIC`
- 日期：2026-11-07
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`（arch-agent 代写）
- 强度：ponytail off（定义任务，不缩文档）
- 状态：as-built 稿已落盘；四角色已会签（`sdd/l2/会签/TS-L2-DS02-L2SET-SIGNOFF-*.md`），未签收
- 上游：说明书第 2.3、4、5 节；`sdd/l2/TS-L2-DS02-ARCH.md` 第 5、7 节；`sdd/l2/TS-L2-DS02-PATH-ARCH.md`
- 查询：2026-11-07 经 MCP `metric-registry` 的 `metric-get` 逐条查询。未读 seed、矩阵 YAML，未改注册表

本叶只写序号 **28–33** 的指标挂接。不新造 `metric_id`，不改口径，不改 D4。三条注册口径都不在请求里计算。

## 1. 挂接结论

| metric_id | 本二级 | 挂在 | 页面 |
|---|---|---|---|
| `M_TECH_PATH_CENTRALITY` | 只作列身份 | 序号 29：技术点中心度格 | ⓘ `MetricSpecHint` + MockBadge |
| `M_TECH_PATH_PRIORITY` | 只作列身份 | 序号 31：路径优先级格、重要性筛选 | ⓘ `MetricSpecHint` + MockBadge |
| `M_TECH_PATH_KEYNODE` | 不挂 | — | 无。关键节点样式用点上已有 `role`（`community_role`）和 `strength`（`weighted_degree`） |

序号 28、30、32、33 没有指标。步序、端点名、比较、播放都是图上字段或页面逻辑，不挂 `metric_id`。

「列身份」的意思：格子里的数来自 `ads_technology_panorama_score` 的 mock 行。`metric_id` 只说明这一列对应注册表哪一条，不表示数是按注册公式算出来的。

## 2. 查询结果（2026-11-07）

三条 `found.seed=true`、`found.matrix=true`、`found.srs_map=false`。

| metric_id | 中文名 | algorithm_type | D1 | D2 | D3 | D4 | srs_refs |
|---|---|---|---|---|---|---|---|
| `M_TECH_PATH_CENTRALITY` | 技术路径中心性（深圳 IPC4 技术点图五维中心性） | third_party | aligned | partial（provisional） | partial | mock | 空 |
| `M_TECH_PATH_PRIORITY` | 技术路径优先级（卡位 × 势头 × 体量） | third_party | aligned | partial（provisional） | partial | mock | 空 |
| `M_TECH_PATH_KEYNODE` | 技术路径关键节点（深圳 IPC4 卡位域识别） | third_party | aligned | partial（provisional） | partial | mock | 空 |

D4 阶段清单三条相同：`ods_synced` todo、`dwd_loaded` todo、`es_indexed` n/a、`graph_loaded` n/a、`verified` todo。

## 3. 八件套（身份，只读）

八件套只含身份字段。D1–D4、`lifecycle_stage`、`srs_refs` 不在本节。

| metric_id | 口径要点 | 公式 | 源表 | 源系统 | 更新频率 | version |
|---|---|---|---|---|---|---|
| `M_TECH_PATH_CENTRALITY` | 深圳为唯一主体，238 个 IPC4 技术点、1464 条共现边，在 226 点巨连通块上算五维中心性；判部分支持 | 过程式复算指针，见 calc-logic，禁手抄 | `dwd_patent` | `gkx @ 183.240.141.251:3318（只读）` | pending | 1 |
| `M_TECH_PATH_PRIORITY` | 卡位 P 40% + 势头 S 35% + 体量 V 25%，按 0.75 / 0.55 切三层；判部分支持 | 同上 | `dwd_patent` | 同上 | pending | 1 |
| `M_TECH_PATH_KEYNODE` | 介数 40% + 跨部类共现 35% + 强度 25% 三合一卡位分，分三层；判部分支持 | 同上 | `dwd_patent` | 同上 | pending | 1 |

三条口径的对象是深圳 IPC4 技术点（238 个）。本页对象是 `demo_gkx_chain` 的 `tech_point`（`technology_node_id`，19430 个）和 `tech_path_step` 归出的路径。两者不是同一套点。所以本页不调用这三条的计算，也不把 mock 行说成它们的输出。

## 4. 为什么 `M_TECH_PATH_KEYNODE` 不挂

- 说明书第 2.3、5 节已定：不挂，样式用点上已有角色。本叶不重开。
- 页面关键节点没有一个「关键节点分」格子。样式直接读 `role` 和 `strength`，不需要指标身份。
- 分数表 `score_kind` 闭集只有 `influence`、`centrality`、`path_priority`，没有关键节点列。

## 5. D4 与角标

| 项 | 现状 | 本叶 |
|---|---|---|
| D4 | 三条均 `mock` | 保持 mock。不改 live |
| MockBadge | `GraphAnalysisPanel.vue` 在中心度（两处）与路径优先级旁挂 `MockBadge`，原因「D4 仍是 mock，分数来自灌数行」 | 保留 |
| ⓘ | 同处 `MetricSpecHint`，`metric-id` 分别为 `M_TECH_PATH_CENTRALITY`、`M_TECH_PATH_PRIORITY` | 保留 |
| 无行 | 格子空，不填默认分 | 保留 |
| 改 live 的条件 | 公式由 `human:唐绍祖` 按技术点另签，且有真实计算写入 | 本叶不推进 |

## 6. 数据现状（截至 2026-11-05）

| score_kind | 行数 | 对应 metric_id |
|---|---|---|
| `centrality` | 19430 | `M_TECH_PATH_CENTRALITY` |
| `path_priority` | 0 | `M_TECH_PATH_PRIORITY` |

`path_priority` 0 行，因为图上还没有 `tech_path_step`，没有可对齐的 `path_id`。`SYSINT-TECHGRAPH-02-L02` 写入路径后重跑灌数脚本 `--apply` 补行。

## 7. 注册表与本页的偏差（只登记）

- 三条 `extras.ui_mount` 写的是「科技专题·技术路径…（TOPIC-TECH-05 / DS-02-TECHPATH）」，不是展示页 `/trend/tech-panorama`。本页只借用列身份，不改注册表。
- 三条 `srs_refs` 为空，`srs_map=false`。没有回填到 SRS 序号 29、31。是否回填由 data-agent 按 `metrics/README.md` 决定。
- `extras.algo_server_location` 指向 `repos/demo-algo-science`。本页不调用该计算，不构成 D12 越界。

## 8. 明确不做

- 不新造 `metric_id`，不加 `TEMP_DS02_*`。
- 不改口径、公式、`algorithm_type`、D1–D4。
- 不把 `M_CHAIN_*`、`M_SVC_GRAPH_*`、`M_SVC_REC_*` 挂到本二级。
- 不在请求里算中心度、关键节点、优先级。
