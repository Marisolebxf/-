# TS-L2-DS02-GRAPH-METRIC · 科学技术全景 · 展示技术点图谱 · 指标挂接（as-built）

- 任务：`TS-L2-DS02-GRAPH-METRIC`
- 日期：2026-11-07
- 监管：`human:淮政玮`
- 认领：`agent:arch-agent`（兼 algorithm）
- 强度：ponytail off（定义任务，不缩文档）
- 状态：as-built 稿已落盘；四角色已会签（`sdd/l2/会签/TS-L2-DS02-L2SET-SIGNOFF-*.md`），未签收
- 上游：说明书 §2.1、§5；`sdd/l2/TS-L2-DS02-ARCH.md` 第 5、7 节；`sdd/l2/TS-L2-DS02-GRAPH-ARCH.md`
- 查询：2026-11-07 经 MCP `metric-registry` `metric-get` 查 `M_TECH_GRAPH_STRUCT`、`M_TECH_EDGE_STRENGTH`、`M_TECH_PATH_CENTRALITY`。未读 seed、矩阵 YAML，未改注册表

本分册只写序号 17–21 挂哪些 `metric_id`。结论：本二级不挂任何 `metric_id`。不新造 ID，不改 D4。

## 1. 逐叶

| 序号 | 功能 | 挂接 | 理由 |
|---|---|---|---|
| 17 | 技术点图谱数据输入 | 无 | 501，不是指标 |
| 18 | 图结构自动生成 | 不挂 `M_TECH_GRAPH_STRUCT` | 画布是图上已有的点和边，请求内不算结构指标 |
| 18 | 关系连线粗细 / 权重 | 不挂 `M_TECH_EDGE_STRENGTH` | 权重是边上已有 `relation_confidence_score`，原样显示 |
| 19 | 图谱交互操作 | 无 | 页面行为 |
| 20 | 技术点搜索定位 | 无 | 名称匹配，不是指标 |
| 21 | 技术点详情查看 | 无 | 显示点上已有属性。见第 3 节中心度 |

## 2. 查询结果

| metric_id | 中文名 | algorithm_type | D1 | D3 | D4 | 注册口径对象 | 本二级 |
|---|---|---|---|---|---|---|---|
| `M_TECH_GRAPH_STRUCT` | 技术点网图结构 | `third_party` | aligned | partial | mock | 200 个 IPC4 域的共现骨干图 | 不挂 |
| `M_TECH_EDGE_STRENGTH` | 技术–技术关联强度 | `third_party` | aligned | full | mock | IPC4 共类网络边权 | 不挂 |
| `M_TECH_PATH_CENTRALITY` | 技术路径中心性（深圳 IPC4 技术点图五维中心性） | `third_party` | aligned | partial | mock | 深圳 238 个 IPC4 技术点 | 不挂本二级。归序号 29 |

三条都是 `found.seed=true`、`found.matrix=true`，`srs_refs` 为空，D2 `partial`（`provisional`）。注册口径的节点是 IPC4 域，不是 `tech_point`（`technology_node_id`）。所以不能用这些函数的输出充当本页的图或连线。

`TEMP_DS02_*` 不是正式 ID。不把 `M_CHAIN_*`、`M_SVC_GRAPH_*`、`M_SVC_REC_*` 改挂到本页。

## 3. 详情抽屉里的数字（as-built）

`index.vue` `buildGraphNodeDetail`（`USE_MOCK=false`）在序号 21 的抽屉里出两张数字卡：

| 卡名 | 取值 | 身份 | 现状 |
|---|---|---|---|
| 关系强度 | `node.strength`，即点上 `weighted_degree` | 图上属性，不是指标 | 卡名写「关系强度」，实际是点的加权度。名称与内容不符 |
| 中心度 | `node.centrality`，Java 按编号读 `ads_technology_panorama_score` 的 `centrality` | `M_TECH_PATH_CENTRALITY`（D4 mock） | 抽屉里无 ⓘ、无 MockBadge。右侧分析面板同一数字有 ⓘ 和 MockBadge |

D9 要求每个统计数字旁有 ⓘ，D4 为 mock 时带 MockBadge。抽屉这张「中心度」卡未满足。处理口径二选一，由会签定：

1. 在抽屉中心度卡旁补 ⓘ（`M_TECH_PATH_CENTRALITY`）和 MockBadge；
2. 或从序号 21 抽屉移除这张卡，中心度只在序号 29 的分析面板出现。

会签取口径 1（见 `会签/TS-L2-DS02-L2SET-SIGNOFF-PRODUCT.md`）。「关系强度」卡同时改名为「加权度」，并按 D9 交 `DS-02-METRIC-OPEN-L01` 判定该数字的身份（挂已有 ID 或按 D1 `missing` 显红问号）。两处改码未建单。

本分册不改代码。`centrality=null` 时这张卡不出现。

## 4. 不在本二级的指标

| metric_id | 归属 |
|---|---|
| `M_TECH_ENTITY_TOP5`、`M_TECH_PAPER_PATENT_CNT`、`M_TECH_ENTITY_REL`、`M_TECH_ENTITY_INFLUENCE` | 22–27 |
| `M_TECH_PATH_CENTRALITY`、`M_TECH_PATH_KEYNODE`、`M_TECH_PATH_PRIORITY` | 28–33 |

说明书 §5 的挂法不变，本分册不重开。

## 5. 明确不做

- 不新造 `metric_id`，不改 D1–D4，不把 mock 写成 live。
- 不在请求内算结构、边强度、中心度。
- 不读 `metrics/registry/` 下 YAML。
