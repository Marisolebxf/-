# TS-L2-DS02-L2SET-SIGNOFF-ALGO · 科学技术全景 · 二级四单 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-07
- 对象：`TS-L2-DS02-{GRAPH,ENTITY,PATH}-{ARCH,API,METRIC,DATA}`（12 份 as-built）
- 监管：`human:淮政玮`
- 指标查询：2026-11-07 经 MCP `user-metric-registry` `metric-get` 查 `M_TECH_GRAPH_STRUCT`、`M_TECH_EDGE_STRENGTH`、`M_TECH_PATH_CENTRALITY`、`M_TECH_PATH_PRIORITY`、`M_TECH_PATH_KEYNODE`、`M_TECH_ENTITY_INFLUENCE`、`M_TECH_PAPER_PATENT_CNT`。未读 `metrics/registry` 下 YAML
- 代码只读抽查：`lumen-algo-py` `lumen_common/algorithms/tech_graph_read.py`、`tech_graph.py`；`scripts/seed/seed_technology_panorama_score.py`
- 本页不改代码，不改 seed，不 commit，不写 task-registry

## 总结论

| 二级 | 结论 |
|---|---|
| GRAPH（17–21） | 有条件同意 |
| ENTITY（22–27） | 有条件同意 |
| PATH（28–33） | 同意 as-built；口径项转登记 |

本角色未直接改被审稿。架构会签已改的归属、`IndexNotFound` 登记与本页判断一致，不再重复。

## 1. GRAPH（序号 17–21）

结论：有条件同意。

条件 A1：架构会签 C1（查询缺口建单）是算法侧的事，本角色作为该返修单的承接方附建议如下，不另提新条件。

| 项 | 稿 | 抽查 | 判定 |
|---|---|---|---|
| 请求内不算结构、边强度、中心度 | METRIC 第 1、5 节 | `tech_graph_read.py` 只拼 `MATCH`、截断、改名；无 PageRank、中心性、聚类计算 | 一致 |
| 不挂 `M_TECH_GRAPH_STRUCT`、`M_TECH_EDGE_STRENGTH` | METRIC 第 1、2 节 | 注册口径节点是 IPC4 域（STRUCT 200 个、EDGE_STRENGTH 620 个），不是 `tech_point`。D1 aligned、D3 partial / full、D4 mock 与稿相同 | 一致。不挂是对的 |
| 连线权重 = `relation_confidence_score` 原样 | METRIC 第 1 节、DATA 第 3 节 | `_rel_ngql` 取 `e.relation_confidence_score AS weight` | 一致 |
| 搜索 = 名称 `CONTAINS` | ARCH 第 4 节 | `_points_ngql` | 一致。不是指标 |
| `IndexNotFound` 当空 | ARCH 第 6 节（已改） | `_ABSENT` 元组把 `indexnotfound` 与 `unknown tag / edge` 合并 | 如实 |

给 C1 返修单的建议（不是会签条件）：

1. `_ABSENT` 拆两组。「边类型 / Tag 不存在」当空是对的（L02 未落边时合理）。`indexnotfound` 不当空，回 503 让 Java 502。
2. 选中点、关系、实体、路径四条查询去掉属性等值，只留 `id(x) == "tech_point:{id}"`。VID 规则已在写入侧固定（`tech_point:` + `technology_node_id`），不需要属性兜底。
3. 搜索与领域收窄必须走属性时，先在 `demo_gkx_chain` 为 `tech_point(name_zh, name_en, technology_node_id)` 建 Tag 索引；这一步写图库，归 `SYSINT-TECHGRAPH-02` 侧，不在读图单内做。

## 2. ENTITY（序号 22–27）

结论：有条件同意。

条件 A2：`relationCount` 恒 1 须建返修单（同架构会签 C3）。这是读图输出与说明书第 2.2 节「条数是邻居个数」不符，归算法侧。

| 项 | 稿 | 抽查 / 注册表 | 判定 |
|---|---|---|---|
| 影响力只作列身份 | METRIC 第 1、4 节 | `M_TECH_ENTITY_INFLUENCE`：third_party，D1 aligned，D2 partial（provisional），D3 full，D4 mock。口径是 IPC4 共类网 PageRank 叠加规模与增速 | 一致。表行不是该口径输出，稿已写明 |
| 分数行怎么来的 | DATA 第 4 节 | 灌数脚本 `mock_value` = 基数 + sha256 前 2 字节取模 / 1000，可复现，不是模型 | 一致。不冒充算法 |
| 不挂 TOP5、CNT、REL | METRIC 第 1、5 节 | `M_TECH_PAPER_PATENT_CNT` 口径自述「技术点粒度不成立」，`acceptance_unit_id=TOPIC-TECH-05` | 一致 |
| Top5 排序 | ARCH 第 8 节 #3 | 读图按 `name_zh`、`name_en`、编号升序截 20；页面再切 5 | 「无强度不造数」兜底，同意。不是算法 |
| `relationCount` | ARCH 第 8 节 #4 | 第 379 行写死 `1` | 如实登记；须返修（A2） |
| 人物影响力 0 行 | METRIC 第 6 节 | `tech_person` 0 点 | 如实 |

D17：不改唐绍祖锁定的计算；三条注册口径的 `algo_server_location` 都在 `demo-algo-science`，本页不调用，不构成 D12 越界。通过。

## 3. PATH（序号 28–33）

结论：同意 as-built；「整条 vs 局部」「重要性分档线」两项口径转登记。

| 项 | 稿 | 抽查 / 注册表 | 判定 |
|---|---|---|---|
| 中心度、优先级只作列身份 | METRIC 第 1、3 节 | `M_TECH_PATH_CENTRALITY`、`M_TECH_PATH_PRIORITY` 注册对象是深圳 238 个 IPC4 点；本页是 19,430 个 `tech_point` | 一致。不调用、不冒充 |
| 不挂 `M_TECH_PATH_KEYNODE` | METRIC 第 4 节 | 注册口径「介数 40% + 跨部类共现 35% + 强度 25%」，对象同样是 IPC4 | 一致。样式用 `community_role` / `weighted_degree` 是图上已有属性，不是本页现算 |
| 路径归组 | DATA 第 2.1 节 | 按 `path_id` 分组、`step_order` 升序；非数字按 0 | 一致。排序与分组不是算法 |
| 路径只带选中点前后一步 | ARCH 第 8 节 #2 | `_path_ngql` 只取与选中点相连的边；`_PATH_FETCH` 有 `ponytail:` 注释写明上限与升级路径（按 `path_id` 再查） | 如实。是否要整条属业务口径，本角色不替甲方定 |
| 重要性不分档 | ARCH 第 8 节 #4 | 注册口径 PRIORITY 自带 0.75 / 0.55 两条切线，但那是 238 个 IPC4 点内的百分位，mock 值域 70.000–78.999 不在同一刻度 | 不能把注册切线直接搬到 mock 值上。分档线转登记 |
| `extras.ui_mount` 指向专题、`srs_refs` 空 | METRIC 第 7 节 | 三条都是 `TOPIC-TECH-05 / DS-02-TECHPATH`，`srs_map=false` | 如实登记。回填归 data-agent |

## 签收边界

本页不把任务标 done，签收由 `human:淮政玮` 做。同意会签不是签收。D4 不得改 live，公式未由 `human:唐绍祖` 按技术点另签前，三个数字仍是 mock。
