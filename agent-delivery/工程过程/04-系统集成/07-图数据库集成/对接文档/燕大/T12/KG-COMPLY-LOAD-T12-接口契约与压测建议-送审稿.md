# T12 后台接口契约与压测建议（送审稿）

任务 `KG-COMPLY-LOAD-T12`，李周，2026-11-12。范围为 SDD §2 的 23 项结果及 §4 两种部署落点。下文路径、字段和压测档位是评审建议。验收结果依据 T08–T10 已签收交付，接口实现及落点待另行确定。

## 1. 调用链与三态

两案的前端均经统一入口发起查询。案 1 由 Java REST 门面负责鉴权与结果聚合，经 Python `/internal/*` 读取图和离线结果。案 2 由网关把请求转发至燕大自带服务，服务在自有工程内读取图和离线结果。端点中的 `item` 选择 SDD 条目。同一类别复用端点，同一底层结果可支撑多个条目。每次响应只报告当前条目的状态，多个算法同时请求时按算法逐项标注。

| 状态 | HTTP | JSON 形状 | 前端表现 |
|---|---|---|---|
| 成功 | 200 | `{ "status": "ok", "item": "428", "data": { "items": [{ "nodeId": "example-node", "rank": 1, "degree": 2914 }], "metric": "degree", "degreeBasis": "edge_count_undirected_projection", "populationSize": 19430, "method": "T09-S1_recomputed", "nextCursor": "example-cursor" }, "meta": { "metric_source": { "formula": "count incident edges in full undirected simple graph" }, "snapshotId": "example-snapshot", "scope": "full_graph" } }` | 展示结果及适用范围。此例取 `topN=1`，`metric_source` 仅展示公式。 |
| 空态 | 200 | `{ "status": "empty", "item": "424", "data": null, "reason": { "code": "PATH_UNREACHABLE", "message": "指定点对不可达", "availability": "unreachable" } }` | 显示原因。查询无命中、算法未计算或上游待补时分别使用对应原因。 |
| 本期不支持 | 501 | `{ "status": "unsupported", "item": "M22", "unsupported": { "code": "GRAPH_SHAPE_UNSUPPORTED", "message": "有数据，当前形态不支持全网分析" } }` | 标明不支持原因。SDD 本期 23 项中仅 **436** 和 **M22** 固定返回 501。 |

格式错误按 400，鉴权失败按 401/403，服务异常按 5xx，客户端按既有错误处理。空态的 `reason` 必填 `code`、`message` 和 `availability`。`availability` 取 `missing`（缺数据或无匹配）、`deferred`（上游结果待补）或 `unreachable`（路径计算确认点对不可达）。501 通过 `unsupported` 说明本期限制。两者都带 `item`，图或结果版本已知时可附 `meta`。统一分页 `{ "items": [...], "nextCursor": null }`，游标绑定快照与过滤条件。合规结果面只消费已有结构与已发布快照；字段名是返回对象的属性，不扩展图库结构。

## 2. 查询端点与 JSON 字段

案 1 的 Java REST 路径示例使用 `/api/kg/comply` 前缀。案 2 由统一网关转发到燕大自带服务，REST 前缀由落点决定。两案共用下表的端点语义和三态结构。下表省略前缀，参数为 JSON 结构示意，必填项按条目区分。五类端点共用第 1 节的三态结构，第 3 节逐项注明本期触发条件。

| 类别 | 查询与入参 | 成功响应 `data` 主要字段 | 空态 / 501 |
|---|---|---|---|
| 读图 | `POST /graph/query`，`{ "item": "platform.tech_rel", "nodeIds": [], "chainId": null, "cursor": null, "limit": 100 }`。按条目校验点或链过滤。 | `nodes[{id,label,type}]`、`edges[{source,target,type,confidence,evidenceLevel}]`、`nextCursor`。M15 另附层级或依赖方向。按 M 编号查关系时传 `item=relation` 和 `relation=Mxx`，见 §4.5。 | `NO_GRAPH_MATCH` / `NO_RESULT`；M22 固定 501 `GRAPH_SHAPE_UNSUPPORTED`。 |
| 路径 | `POST /paths/query`，`{ "item": "424", "sourceId": "...", "targetId": "...", "algorithms": ["dijkstra"], "k": 1, "scenarioId": null }`。 | `paths[{algorithm,rank,nodeIds,edges,hopCount,totalCost}]`、`algorithmResults[{algorithm,status,reason}]`。`totalCost` 对无权算法为 `null`，加权算法填沿途代价和。加权路径的每条 `edges` 带 `cost`，按路径顺序返回。 | `NODE_NOT_FOUND`、`PATH_UNREACHABLE`、`RESULT_NOT_COMPUTED`；426 选择企业合作网时走 M22 的 501。 |
| 中心性 | `POST /centrality/query`，`{ "item": "428", "topN": 20, "cursor": null }`。 | `items` 的共同字段为 `nodeId`、`rank`，指标值字段按 `item` 定义。响应另带 `metric`、`degreeBasis`（适用时）、`populationSize`、`method`、`nextCursor`。428 的条目返回 `items[{nodeId,rank,degree}]`，按 `degree` 排序。中台 1 返回 `weighted_degree_recomputed`。432 附四项分值与权重。 | 无榜单或无匹配结果时返回空态 `NO_RANKING`，依赖的结果缺失时用 `DEPENDENCY_NO_RESULT`。 |
| 社群 | `POST /communities/query`，`{ "item": "435", "communityId": null, "algorithm": "louvain", "cursor": null, "limit": 100 }`。 | `communities[{communityId,memberCount,internalEdgeCount,avgDegree,density,coreNodeIds}]`、`members[{nodeId,communityId}]` 或 §4.3 的 437 结构，按条目返回。`meta` 附算法、分辨率、种子及范围。 | `RESULT_NOT_COMPUTED` / `NO_COMMUNITY_MATCH`；436 固定 501 `MULTI_SNAPSHOT_REQUIRED`。 |
| 关键路径 | `POST /key-paths/query`，`{ "item": "28", "pathId": null, "cursor": null, "limit": 100 }`。29 可加 `nodeIds`。 | `paths[{pathId,steps:[{stepOrder,nodeId}]}]` 或 `nodes[{nodeId,rank,mark,metric}]`，按 `stepOrder` 有序。 | `NO_PATH_STEPS` / `DEPENDENCY_NO_RESULT`；当前关键路径条目无固定 501。 |

## 3. SDD §2 的 23 项对照

需规条目以序号字符串作为 `item`。六项中台能力依次使用 `platform.weighted_degree`、`platform.tech_rel`、`platform.tech_path_step`、`platform.community_id`、`M22`、`M15`。三态结构见 §1。表中「—」表示本期该结果分支不触发。SDD §2 的 23 项只有 436 和 M22 本身进入 501 分支，426 选企业合作网时复用 M22 的 501。

| 条目 | 端点类别 | 成功 | 空态 | 501 |
|---|---|---|---|---|
| 423 多算法路径 | 路径 | 各已计算算法的路径和代价 | 点不存在、不可达或所选算法未计算。T08 验收结果可证 BFS、Dijkstra | — |
| 424 最优路径 | 路径 | Dijkstra 最低代价路径及节点顺序 | 点不存在或不可达 | — |
| 425 路径多样性 | 路径 | 备选路径、排序、跳数，注明备选策略和实际条数 | 无备选或未计算 | — |
| 426 场景化路径 | 路径 | 技术点图和已具备数据的人才合作网 M01 可作为场景。返回实际查询出的路径和场景范围 | 场景结果尚未计算或指定点对不可达 | 企业合作场景复用 M22 的 501，响应 `item=M22` |
| 427 交互路径 | 路径 | 指定点对的路径与高亮节点和边 | 点不存在或无匹配结果 | — |
| 428 度中心性 | 中心性 | 读取 T09-S1 `degree-full.json`，返回 `degree` 与 `degreeBasis=edge_count_undirected_projection`，全量 19,430 点可分页 | 重算榜缺失 | — |
| 429 紧密中心性 | 中心性 | T09 1,500 点诱导子图榜，标明范围和连通性修正 | 子图或榜单无结果 | — |
| 430 中介中心性 | 中心性 | T09 同一子图近似榜，300 源采样、种子 42 | 子图或榜单无结果 | — |
| 431 PageRank | 中心性 | T09 全图置信度加权榜，标明 α=0.85 | 榜单无结果 | — |
| 432 综合中心性 | 中心性 | 读取 T09-S1 `composite-recomputed.json`，返回 1,500 点等权综合榜、原始分项、归一化分项与权重 | 无已发布榜单或无匹配结果 | — |
| 433 多算法社群 | 社群 | 已算算法与分区摘要，当前验收算法为 Louvain | 某选定算法未计算，逐项说明 | — |
| 434 社群识别 | 社群 | T10 B′ 离线 `partition` 的成员与社群编号，覆盖 19,430 点 | 无分区结果或所查点未命中 | — |
| 435 社群属性 | 社群 | 成员数、去重内部边数、核心点、修正后的平均度和密度 | 无成员表或聚合结果 | — |
| 436 社群演化 | 社群 | — | — | `MULTI_SNAPSHOT_REQUIRED`，社群演化需要多期快照，本期仅有单份快照 |
| 437 社群可视化 | 社群 | 成员分区与渲染所需属性；平均度和密度用第 4 节口径 | 434 无分区或 435 所需结果未就绪 | — |
| 28 关键路径接收 | 关键路径 | 按 `pathId` 聚合且有序的路径步 | 路径或步表无匹配 | — |
| 29 关键节点标记 | 关键路径 | 基于有结果的中心性指标返回节点标记与依据 | 依赖的中心性结果缺失 | — |
| 中台 1 加权度 | 中心性 | 读取 T09-S1 `weighted-degree-full.json`，返回 19,430 点的 `weighted_degree_recomputed` 和 `degreeBasis=weight_sum_incident` | 无已发布榜单或无匹配结果 | — |
| 中台 2 技术点关系网 | 读图 | 已有技术点、技术关系、证据等级和置信度 | 所查范围无关系 | — |
| 中台 3 关键路径步 | 关键路径 | 已有关键路径及有序步骤 | 步表无匹配 | — |
| 中台 4 社群编号 | 社群 | T10 离线分区成员对应的编号，标明结果版本 | 未计算或点未命中 | — |
| 中台 5 企业合作网 M22 | 读图 | — | — | `GRAPH_SHAPE_UNSUPPORTED`，有 94,824 条存量边，图碎片化无法支撑全网排名与社群分析 |
| 中台 6 产业链依赖网 M15 | 读图 | 按链返回有向依赖、层级或溯源所需数据 | 链或依赖关系无命中 | — |

## 4. 本轮需评审的口径

### 4.1 428、432 与中台加权度

| 字段 | 含义 | 数据来源与当前使用范围 |
|---|---|---|
| `degree` | 全图无向简单投影的入射边条数 | 428 使用 T09-S1 `degree-full.json`，榜首为 2,914。 |
| `weighted_degree_recomputed` | 对入射边（入边 + 出边）的 `relation_confidence_score/100` 求和，单边权重尺度 0–1 | 中台 1 使用 T09-S1 `weighted-degree-full.json`。榜首 2,347 条入边与 567 条出边的权重合计为 1,478.04514324。 |
| `weighted_degree_stored` | 库内原 `weighted_degree` 的历史值 | 仅用于归档和核对。T09 旧综合表首行原始度分项约 1,010.91。 |

三份榜单基于原 T09 签收快照。该快照没有自环和重复的无向端点对，因此无向投影的度数与入边、出边合计等价。换用新快照时，须先核验这两项条件。

428 的 `topN` 为每页条数，默认 20，接受正整数。请求超过榜单剩余行数时返回剩余记录。排名沿用归档顺序，按度数降序，同度按 VID 升序。游标绑定条目与快照，续页可遍历全部 19,430 点，末页返回 `nextCursor=null`。

| 条目 | 已签收数据 | `meta.scope` | 结果字段 |
|---|---|---|---|
| 428 | [无权度整榜](../T09-S1/degree-full.json) | `full_graph` | `items[{nodeId,rank,degree}]`，`degreeBasis=edge_count_undirected_projection` |
| 432 | [重算综合榜](../T09-S1/composite-recomputed.json) | `t09_composite_1500` | `items[{nodeId,rank,score,raw,normalized}]`，四项权重各 0.25 |
| 中台 1 | [重算加权度整榜](../T09-S1/weighted-degree-full.json) | `full_graph` | `items[{nodeId,rank,weighted_degree_recomputed}]`，`degreeBasis=weight_sum_incident` |

出参用归档行的 `id` 填 `nodeId`。三项的 `meta.metric_source` 透传归档的同名对象，含快照时间、节点与边的摘要及计算公式。`meta.scope` 按表中范围标识返回，`populationSize` 取归档 `scope.population_count`。

432 读取已签收综合榜，其中 `raw.degree` 是同一批 1,500 个点的全图无权度。PageRank、紧密中心性和中介中心性的原始值沿用 T09。四项在这 1,500 个点内分别做 min-max，常量列归零，再等权合成；`data.weights` 返回四项各 0.25。中台 1 直接返回已签收的入射加权度榜。两项均按成功结构返回可用榜单，查询无匹配时用普通空态。

### 4.2 423、424 与 426 路径

423 和 424 的加权路径沿用 T08 签收口径。每条边的 `cost = 1 / relation_confidence_score`，置信度必须有限且大于 0。路径的 `totalCost` 为各边代价之和，BFS 使用 `hopCount`，`totalCost` 为 `null`。已归档固定点对只证明对应点对的结果。426 对技术点图和 M01 人才合作网按实际可用结果返回。企业合作场景按 M22 形态不支持处理，保留原请求条目 `requestedItem=426` 和 `scenarioId` 便于客户端定位。

### 4.3 434、435 与 437 社群

434 从 T10 签收的 `t10_full_s42_r8.0_all.json` 的 `partition` 读 19,430 条成员记录。图内 `community_id` 在核验时全为空字符串。B′ 使用 python-louvain、分辨率 8.0、种子 42，共 287 个社群编号，其中 180 个多节点成形社群、107 个单点社群。社群筛选项从 `partition` 提取全部编号。社群编号随快照变化，响应附算法及快照版本。

435 直接读取 T10 修订后汇总的「平均度」和「密度」列，分别映射为 `avgDegree` 和 `density`。两列已按无向图 `2E/N` 和 `2E/[N(N-1)]` 计算，`N` 为成员数，`E` 为无向去重内部边数。社群 55 的归档值为 15.6 和 0.024455。437 对齐 T10 的接口档，每个社群返回 `{community_id, size, member_vids[], inner_edges, avg_degree, density, core_points[]}`，其中成员来自同一快照的 `partition`，平均度与密度复用 435 的已修订值。单点社群平均度为 0，密度为 `null` 并标注不适用。单点社群仍提供成员记录。查询没有匹配社群时使用空态。

### 4.4 436 与 M22 的 501

436 返回 `MULTI_SNAPSHOT_REQUIRED`，消息为「社群演化需要多期快照，本期仅有单份快照」。M22 返回 `GRAPH_SHAPE_UNSUPPORTED`，消息为「有数据，当前形态不支持全网分析」。M22 的存量边数 94,824 可附在响应元数据，前端仍按不支持状态显示。

### 4.5 按 M 编号查关系

`POST /graph/query` 接受 `{"item":"relation","relation":"M19"}`。`relation` 仅接受 M01–M24，格式错误或编号越界返回 400。合法编号无匹配时返回 HTTP 200 空态。以下 16 项本期无供数，`reason.code=RELATION_EMPTY`、`reason.availability=missing`，`reason.message` 按编号返回。M22 使用 §4.4 的 501，并将响应的 `item` 设为 `M22`。

| 编号 | 空态原因 |
|---|---|
| M03 | 源表有 202,795 行，涉及的 8,784 个机构全部为企业，无法形成符合本编号的人才到科研机构关系。 |
| M05 | 本期未提供科研机构之间的隶属关系。 |
| M06 | 本期无符合论文引用语义的数据源。 |
| M07 | 源表仅有受资助成果署名记录，无法确认人才直接参与项目。 |
| M10 | 本期未提供科研机构发布政策的关系记录。 |
| M11 | 本期未提供政策之间的关联记录。 |
| M12 | 源侧缺企业稳定 ID 列，无法建立企业端点。 |
| M13 | 源侧缺人才稳定 ID 列，无法建立人才端点。 |
| M14 | 源侧只有发文机构名称，缺科研机构稳定 ID，无法建立科研机构端点。 |
| M16 | 本期未提供政策引用政策的记录。 |
| M18 | 本期服务机构到产业链环节为 0 条，机构间存量另行归账。 |
| M19 | 机构合作同源数据已归入 M02，本期没有单建专边。 |
| M20 | 人才合作同源数据已归入 M01，本期没有单建专边。 |
| M21 | 本期未提供服务机构服务企业的关系记录。 |
| M23 | 本期未提供企业间供给关系，旧供给边已停用。 |
| M24 | 本期未提供企业间母子关系的记录。 |

M12–M14 的稳定 ID 缺口见 [L04 政策入图路径](../../../KG-7ELEM-LOAD-PATH-L04-政策.md)。现存 `apply_to` 的 10,957 条政策适用范围边指向产业链或环节，单列在历史存量。

M08、M09 已入图边的 `weight` 恒为 1.0，只表示该批次的固定值。若出参暴露该字段，元数据标明 `weightMeaning=constant_no_strength`，前端按无强度信息处理。

## 5. 两案压测建议

两案使用相同的图快照、T08–T10 结果版本、查询参数、分页上限、数据范围、并发档位和请求顺序。分别记录冷缓存与热缓存。前端均经统一入口。案 1 分段记录 Java REST 门面、Python 和数据读取耗时，案 2 分段记录网关转发、燕大服务和数据读取耗时。各段通过链路标识关联。

| 场景 | 负载与证据 | 案 1 集成项目 | 案 2 燕大服务 |
|---|---|---|---|
| 端到端读图 | 固定技术点邻接和 M15 按链查询，分别测首屏与连续分页。记录 p50/p95/p99、返回字节、超时率、最大实际扫描范围和图查询耗时。 | 分段计 Java 门面、Python 查询及可能的跨网结果读取。 | 分段计统一入口转发、服务内图查询及序列化，记录额外网络耗时。 |
| 算法结果查询并发 | 固定路径点对、中心性首屏与 428 整榜续页、社群成员/属性、关键路径各一组。建议并发 1/5/10/20，从单用户基线递增；每档 1 分钟预热、3 分钟采样，可按环境缩小。记录吞吐、p95/p99、错误/超时、队列与资源峰值。 | 区分 Java 排队、离线结果读取及跨网络回取。 | 区分网关转发、服务内结果读取与序列化。 |
| 三态与错误隔离 | 每档混入成功、未命中、436/M22 两种 501；按状态单独统计时延与比例，核对消息和快照标识。 | 核验 Java 转换和 HTTP 状态保留。 | 核验网关转发保留状态、原因与结果版本。 |

先在两案各做单请求功能核对，再做等负载比较。判定优先看页面读图与算法结果查询的 p95、错误率、稳定吞吐和资源占用，辅以链路分段定位。正式阈值由集成方按环境和验收要求确认。图查询按既有端点类型和分页范围锚定；压测不包含在线重跑大规模算法。

## 6. 评审资料

- [T09-S1 签收与 T12 收尾要求](../../../KG-COMPLY-答复-李周-加权度口径确认与S1签收-20261112.md) · [T09-S1 技术验收记录](../../../KG-COMPLY-ACCEPT-T09-S1-技术验收记录.md)

- [T07 送审与 T12 二稿评审](../../../KG-COMPLY-答复-李周-T07送审与T12二稿评审-20261112.md)

- [SDD §2、§4、T12](../../../KG-COMPLY-SDD-L01-详细设计说明书.md)
- [唐绍祖 T12 六项评审意见](../../../KG-COMPLY-答复-李周-T12初稿评审-20261112.md) · [T09-S1 补数与 435/437 口径更新](../../../KG-COMPLY-答复-李周-T07认领恢复与T09补数-20261112.md)
- [T07 验收总表](../T07/KG-COMPLY-LOAD-T07-M01-M24入图验收总表-送审稿.md)
- [T03/T08 技术验收](../../../KG-COMPLY-ACCEPT-T03-T08-技术验收记录.md)
- [T02/T09 技术验收](../../../KG-COMPLY-ACCEPT-T02-T09-技术验收记录.md)
- [T10 技术验收](../../../KG-COMPLY-ACCEPT-T10-技术验收记录.md)
- [T10 修订后 435 汇总](../../../KG-COMPLY-LOAD-T10-交付-20261112/T10-435-社群属性汇总.md) · [B′ 离线分区](../../../KG-COMPLY-LOAD-T10-交付-20261112/out/t10_full_s42_r8.0_all.json)
- [T09 度数和综合分证据](../T09/result.json) · [原 1,500 点综合表](../T09/composite.json)
