# TS-L2-DS02-ARCH-SIGNOFF-DATA · 科学技术全景 · 数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-05
- 对象：`TS-L2-DS02-ARCH`（对照 `sdd/科学技术全景-系统详细设计说明书.md`、`功能拆解.md`；三份只读）
- 监管：`human:淮政玮`
- 指标查询：2026-11-05，经 MCP `user-metric-registry` 的 `metric-get`。未读 `agent-delivery/metrics/registry` 下 yaml
- 本页不改架构、不改 seed、不改 task-registry

## 结论

同意会签。

图只读第 2 项已写入的 `demo_gkx_chain`（Tag `tech_point`，以及同方案的 `tech_paper`、`tech_patent`、`tech_institution`、`tech_person`）。本页不写图、不写挂产业表、不把论文全表扫进节点。三个数字只新建 ADS 表 `ads_technology_panorama_score`。稿里库名写成「与 `gkxlumen-display` 现读的 ADS 同库」，核对现读库是 `demo_gkxlumenx_ads`，对得上，不阻塞。该表是 D18 的 mock 结果表，不用 `gapfill_` 前缀，不进 ODS、DWD、供应方库。Python 灌 mock 行，Java 在同一次 `graph` 里按编号只读；无行则该格空；D4 保持 mock，界面留 MockBadge。九个 ID 都在册，D1 为 `aligned`，D4 为 `mock`。不新造 `metric_id`。影响力、中心度、路径优先级三个 ID 只作列身份；注册对象是 IPC4 PageRank 或深圳卡位，稿已写明表行不是那些函数的输出，公式待 `human:唐绍祖` 按技术点另签。不要求改口径，不要求改 D4。图、实体名单、路径步不进这张分数表。接口不直接返回写死数字。

## 核对

| 数据对象 | 架构稿 | 注册表或库 | 判定 |
|---|---|---|---|
| 图空间与标签 | 三个功能使用第 2 项已经写入的技术点图。Python 只读 `demo_gkx_chain`。空间不是这个就拒绝，不改去 `gkx_chain` 或 `entan`。不读燕大产业链全景来填本页 | 第 2 项方案 `方案-SYSINT-TECHGRAPH-02-L01.md`（2026-11-05 已签收）把空间定为 `demo_gkx_chain`。Tag：`tech_point`、`tech_paper`、`tech_patent`、`tech_institution`、`tech_person`。边上图用 `tech_rel`、`tech_has_paper`、`tech_has_patent`、`tech_has_institution`、`tech_has_person`、`tech_path_step` | 同意。本页不另建空间、不另造标签 |
| 本页是否写图 | 不写技术点入图、边上图。写请求 501。Java 不写 nGQL。`gkxlumen-display` 不直连图库。点未写入时三个功能一起空，不用 `mock/modules/panorama.ts` 填节点 | 入图仍在第 2 项 `SYSINT-TECHGRAPH-02-L01` / `L02`。读图单 `TS-L2-DS02-READ-PY-L01` 写明只读、不写图、不返回 fixture | 同意 |
| 挂产业表 | 领域筛选只作用于已经挂上产业的技术点。一个都没挂上则筛选为空。本页不写挂产业那张表 | 第 2 项挂产业写入 `demo_gkxlumenx_dwd.dwd_technology_topic_industry`。本页展示链不写这张 DWD 表 | 同意。不把分数表或筛选结果写进该 DWD 表 |
| 论文是否扫全表进节点 | 实体来自选中技术点在图上的邻居。每类最多 20 条。论文条数、专利条数是邻居个数。不挂 `M_TECH_PAPER_PATENT_CNT` | 注册口径写明按技术点对齐的双计数不成立（`dwd_zh_paper` 等供应方表上没有技术点实体）。D4 `mock`。本页读图不打开这些全表 | 同意。不把论文全表扫进节点 |
| 三个数字的承载 | 只有影响力、中心度、路径优先级新建 `ads_technology_panorama_score`。一行是一个技术点或一条路径，加 `influence`、`centrality`、`path_priority` 之一。图谱、实体名单、路径步来自已有图，不进这张表 | D18：做不到真模型时只接受新建 ADS 表、Python 灌 mock 行、Java 只读。表名、灌数方（`TS-L2-DS02-SCORE-L01`）、读取接口（同一次 `POST /display/v1/situation/panorama/graph`）三样稿里都有 | 同意。没有把图、名单、路径步灌进分数表 |
| 库名 | 「与 `gkxlumen-display` 现读的 ADS 同库。不建在 ODS、DWD、供应方库，也不用 `gapfill_`」 | BFF 自身不连 MySQL。它现读 ADS 的下游库名一致为 `demo_gkxlumenx_ads`：`gkxlumen-element` 的 `ELEMENT_MYSQL_DB` / `ELEMENT_ADS_DB` 默认、helm `INNOV_MYSQL_DB` 与 `INNOV_MYSQL_ADS_DB`、展示门面 `gkx_show_service` 的 `MYSQL_DATABASE` 默认。正式库名 `gkxlumenx_ads` 只出现在「以后切换」的注释里，不是现读默认。久新 Doris 不是这套 ADS | 对得上，不阻塞。落库用 `demo_gkxlumenx_ads`。不落 `demo_gkxlumenx_ods`、`demo_gkxlumenx_dwd`、供应方库 `gkx`、久新 Doris |
| D16 与 D18 | 表名 `ads_technology_panorama_score`，明确不用 `gapfill_`。行是 mock。D4 保持 mock | D16 缺项表只许 `gkxlumenx_gapfill.gapfill_*`。本表没有缺项登记，不走那条。D18 的 mock ADS 表 D4 仍是 mock | 同意。这是 D18 表，不是 D16 缺项表 |
| 谁灌、谁读、空行 | Python 独立灌数，不在 `graph` 请求里写。Java 按编号只读。没有行则该格空，名单和路径仍在。读失败只空数字，不用演示种子或 fixture 填这三个数 | 血缘规约 §7.4：禁止接口直接返回 mock JSON、常量列表或内存 fixture。现网 `SituationPanoramaController` 只回空集合和 `GRAPH_NOT_READY`，没有写死分数。接入后空图用 `GRAPH_EMPTY` | 同意。没有接口直接返回写死数字 |
| 界面与 D4 | D4 保持 mock。界面保留 MockBadge。未由唐绍祖按技术点另签公式之前不得改成 live | 九个 ID 的 `d4_ingestion_status` 现均为 `mock`，`is_mock` 为 true。本会签不改 seed | 同意。D4 不得改 live |
| `M_TECH_GRAPH_STRUCT` | 不作为序号 18 的图结构自动生成 | 在册。D1 `aligned`，D4 `mock`，`algorithm_type=third_party`。口径对象是 200 个 IPC4 域的共现骨干，节点是 IPC4 域 | 同意。不调用该计算 |
| `M_TECH_EDGE_STRENGTH` | 关系强度用图上已有权重 | 在册。D1 `aligned`，D4 `mock`，`algorithm_type=third_party`。口径对象是 IPC4 共类边权 | 同意。不调用该计算 |
| `M_TECH_ENTITY_TOP5` | Top5 是该技术点在图上的关联实体，不调用此 ID | 在册。D1 `aligned`，D4 `mock`，`algorithm_type=third_party`。口径对象是 IPC4 与申请人、论文标题 | 同意。不调用该计算 |
| `M_TECH_PAPER_PATENT_CNT` | 不挂在实体详情的条数上 | 在册。D1 `aligned`，D4 `mock`，`algorithm_type=STAT`。口径写明技术点粒度不成立 | 同意。不调用该计算 |
| `M_TECH_ENTITY_REL` | 序号 26 保持空，不挂此 ID | 在册。D1 `aligned`，D4 `mock`，`algorithm_type=third_party`。口径对象是专利转移、共同申请、论文合著 | 同意。不调用该计算 |
| `M_TECH_ENTITY_INFLUENCE` | 只作影响力列的身份。表行不是该函数的输出 | 在册。D1 `aligned`，D4 `mock`，`algorithm_type=third_party`。口径对象是 IPC4 共类网上的 PageRank，再叠加规模与增速 | 合法。不改口径，不改 D4。公式待 `human:唐绍祖` 另签 |
| `M_TECH_PATH_CENTRALITY` | 只作中心度列的身份。请求内不算 | 在册。D1 `aligned`，D4 `mock`，`algorithm_type=third_party`。口径对象是深圳 IPC4 技术点图的五维中心性 | 合法。不改口径，不改 D4。公式待 `human:唐绍祖` 另签 |
| `M_TECH_PATH_KEYNODE` | 不挂。关键节点样式用点上已有角色和加权度 | 在册。D1 `aligned`，D4 `mock`，`algorithm_type=third_party`。口径对象是深圳 IPC4 卡位域 | 同意。不调用该计算 |
| `M_TECH_PATH_PRIORITY` | 只作路径优先级列的身份 | 在册。D1 `aligned`，D4 `mock`，`algorithm_type=third_party`。口径对象是深圳 IPC4 上的卡位 × 势头 × 体量 | 合法。不改口径，不改 D4。公式待 `human:唐绍祖` 另签 |
| 是否新造 ID | 不新造 `metric_id`。`TEMP_DS02_*` 不是正式 ID。不把 `M_CHAIN_*`、`M_SVC_GRAPH_*`、`M_SVC_REC_*` 改挂到本页 | 上表九个 ID 均 `found.seed=true` 且 `found.matrix=true`。本会签未写 seed | 同意 |

## 签收边界

本页不把任务标 done，签收仍由 `human:淮政玮` 做。D4 不得改 live。

`TS-L2-DS02-ARCH` 以及 `TS-L2-DS02-READ-PY-L01`、`TS-L2-DS02-SCORE-L01`、`TS-L2-DS02-TEST-L01` 的状态都不由本会签改写。不改架构稿，不改指标 seed。灌数叶落库时用本会签核对的库 `demo_gkxlumenx_ads`，表 `ads_technology_panorama_score`；mock 行与真实行分开时沿血缘规约使用 `mock_` 批次前缀。这不构成改稿条件。
