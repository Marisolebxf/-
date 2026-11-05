# TS-L2-DS02-ARCH-SIGNOFF-ALGO · 科学技术全景 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-05
- 对象：`TS-L2-DS02-ARCH`
- 监管：`human:淮政玮`
- 对照：`sdd/科学技术全景-系统详细设计说明书.md`、`功能拆解.md`，以及 `lumen-algo-py` 现有 `tech_graph`（只读核对，未改代码）
- 本页不改架构、不改代码、不改 task-registry
- 指标：2026-11-05 经 `metric-registry` 的 `metric-get` 查询。未读 `agent-delivery/metrics/registry` 下的 yaml，未新造 `metric_id`，未把 D4 改成 live

## 结论

同意会签。

展示读图不是新模型。`lumen-algo-py` 现有 `tech_graph` 只有入图写点 `POST /internal/tech-graph/vertex`，没有 `POST /internal/tech-graph/read`。说明书第 7 节与功能拆解第 5 节把该读接口放在 `TS-L2-DS02-READ-PY-L01`，会签前 backlog。接口还没写，不构成反对。

三个数字只读 `ads_technology_panorama_score` 的 mock 行，请求内不算 PageRank、中心度或深圳卡位。序号 17、序号 26 保持 501 / 空，不要求算法现算。Java 不写图算法，读失败不回退 fixture。本页不改唐绍祖锁定的合规算法闭包。

## 核对

| 序号或能力 | 架构稿 | 代码或注册表 | 判定 |
|---|---|---|---|
| 展示读图 | 真读已有技术点图。Python 只读 `demo_gkx_chain`。不是新模型 | `lumen_algo_service/views/tech_graph.py` 只注册 `POST /internal/tech-graph/vertex`。全仓无 `/internal/tech-graph/read`。说明书把读图定为 `TS-L2-DS02-READ-PY-L01`（backlog）：只读、不写图、不返回 fixture | 同意。缺读接口合法 |
| 空间 | 空间只许 `demo_gkx_chain`。`gkx_chain` 与 `entan` 拒绝。不读燕大产业链全景来填本页 | `chain_space()` 只返回 `demo_gkx_chain`。`gkx_chain` 有测试拒绝。`entan`、`demo_entan` 以及其他空间在 `chain_space()` 抛 `NonDemoNebulaSpaceError`。vertex 写出的 `USE` 只含 `demo_gkx_chain` | 同意 |
| 读图是否写 nGQL | 本页读图只读。Java 不写 nGQL，`gkxlumen-display` 不直连图库 | 读接口不存在，当前没有读图语句。已有 `write_vertices` 会 `INSERT VERTEX` / `UPDATE VERTEX`，那是入图写点，空间仍锁在 `demo_gkx_chain`，且拒绝写 Edge。本页读图单不得复用这条写路径 | 同意 |
| 第 2 节数据流图 | 图上箭头从 display 指向图库。同节正文写明 display 不直连图库，图由 Python 只读 | 说明书第 3 节的调用链是 display → `POST /internal/tech-graph/read` → `demo_gkx_chain` | 正文与说明书为准。图示少画 Python 一跳，不因此不同意 |
| 序号 17 导入 | 手动输入、Excel、JSON 不是本页功能。写请求 501。无写接口。点由第 2 项写入 | 功能拆解不建输入单，数据在 `SYSINT-TECHGRAPH-02-L01`。`tech_graph` 无导入路由 | 同意。不要求算法现算导入 |
| 序号 18–21 图谱 | 真读技术点与选中后的关系。搜索、详情走同一次 `graph`。不挂 `M_TECH_GRAPH_STRUCT`。交互在页内完成 | `M_TECH_GRAPH_STRUCT`：D1 `aligned`，D4 `mock`，口径是 200 个 IPC4 域的共现骨干，节点不是本页技术点。`lumen-algo-py` 无该计算 | 同意 |
| 序号 22–25 关联实体 | 真读该点的人、机构、论文、专利。无强度不造数。条数是邻居个数。时间只在关系确有年份时收窄 | `M_TECH_ENTITY_TOP5`、`M_TECH_EDGE_STRENGTH`、`M_TECH_PAPER_PATENT_CNT` 均 D1 `aligned`、D4 `mock`。Top5 口径是 IPC4 与申请人、论文标题。论文/专利条数口径写明技术点粒度不成立。仓内无这些函数 | 同意。不调用这三项计算 |
| 序号 26 实体间关系与多快照 | 501 / 空。没有实体—实体边，也没有第二份快照。不挂 `M_TECH_ENTITY_REL` | `M_TECH_ENTITY_REL`：D1 `aligned`，D4 `mock`，口径是专利转移、共同申请、论文合著。无多快照读接口 | 同意。不要求算法现算关系网 |
| 序号 27、29、31 三个数字 | 影响力、中心度、路径优先级只读 `ads_technology_panorama_score`。无行则该格空。灌数不在 `graph` 请求里做。D4 保持 mock。公式待 `human:唐绍祖` 按技术点另签，未签不得改 live | 三 ID 均在册，D1 `aligned`，D4 `mock`。`M_TECH_ENTITY_INFLUENCE` 口径是 IPC4 PageRank；`M_TECH_PATH_CENTRALITY` 是深圳 IPC4 五维中心性；`M_TECH_PATH_PRIORITY` 是卡位 × 势头 × 体量。`tech_graph` 未挂这三个计算。灌数在 `TS-L2-DS02-SCORE-L01`（backlog） | 同意。三 ID 只作列身份，请求内不算 |
| 序号 28–33 路径 | 真读已有路径步。关键节点样式用点上角色和加权度。不挂 `M_TECH_PATH_KEYNODE`。比较与按步播放不另建模型，不按 `currentYear` 换图 | `M_TECH_PATH_KEYNODE`：D1 `aligned`，D4 `mock`，口径是深圳 IPC4 卡位域。仓内无该函数 | 同意 |
| 旁路 PageRank / 卡位 | 禁止用 IPC4、深圳卡位或 PageRank 的结果填本页的图、名单、路径或三个数字 | `vendor/innov-py` 有创新点 PersonalizedPageRank；`vendor/entan-py` 有企业图 PageRank 与 `/v1/centrality`。二者都未挂到 `tech_graph`。注册表把九个 TECH 计算记在 `demo-algo-science`，不在本页调用链 | 同意。读图单与灌数单不得调用这些函数 |
| 失败与 Java | 读失败不用演示种子，不用 `mock/modules/panorama.ts`，不用 `GRAPH_NOT_READY` 冒充成功。Java 不写算法、不写 nGQL | 说明书写明不允许接口返回写死 mock，也不许用页面 fixture 填这三个功能。`READ-PY-L01` 写明不返回 fixture | 同意 |
| 截断上限 | 首屏最多 200 个技术点且不铺边；选中后每类实体最多 20、路径最多 20，超过上限标明截断。架构稿未写选中后的关系条数 | 说明书第 3 节把选中后的关系写成最多 200 条。`READ-PY-L01` 按该节执行 | 不阻塞。实现跟说明书第 3 节 |
| D17 | 不改已锁定的合规算法闭包，不复用锁定 URL，不把上述 IPC4 / 深圳口径改成 live | 本会签不改 `demo-algo-science` 中的计算包。D4 九条均为 mock，保持 mock | 同意 |

九个已核对 ID：`M_TECH_GRAPH_STRUCT`、`M_TECH_EDGE_STRENGTH`、`M_TECH_ENTITY_TOP5`、`M_TECH_PAPER_PATENT_CNT`、`M_TECH_ENTITY_REL`、`M_TECH_ENTITY_INFLUENCE`、`M_TECH_PATH_CENTRALITY`、`M_TECH_PATH_KEYNODE`、`M_TECH_PATH_PRIORITY`。D1 均为 `aligned`，D4 均为 `mock`。`M_TECH_PAPER_PATENT_CNT` 的 algorithm_type 为 `STAT`，其余八个为 `third_party`。

## 签收边界

本页不把任务标 done。`TS-L2-DS02-ARCH` 以及 `TS-L2-DS02-READ-PY-L01`、`TS-L2-DS02-SCORE-L01`、`TS-L2-DS02-TEST-L01` 的状态都不由本会签改写。签收仍由 `human:淮政玮` 做。
