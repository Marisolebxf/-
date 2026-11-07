# TS-L2-DS02-PATH-API · 科学技术全景 · 展示关键路径和关键节点 · 后台接口设计

- 任务：`TS-L2-DS02-PATH-API`
- 日期：2026-11-07
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`（arch-agent 代写）
- 强度：ponytail off（定义任务，不缩文档）
- 状态：as-built 稿已落盘；四角色已会签（`sdd/l2/会签/TS-L2-DS02-L2SET-SIGNOFF-*.md`），未签收
- 上游：`sdd/l2/TS-L2-DS02-PATH-ARCH.md`（本分册以它为准）；说明书第 3、6 节；`sdd/l2/TS-L2-DS02-ARCH.md` 第 2 节
- as-built 依据：`lumen-svc-platform` `SituationPanoramaService` / `TechGraphReadAdapter` / `JdbcPanoramaScores`（`cbd6f10`、`271109c`）；`lumen-algo-py` `tech_graph_read.py`（`a03c52b`、`4e7f453`、`07ffa9f`）；`lumen-ui-science-pc` `liveGraph.ts`、`panorama.ts`（`e6fb1dd`）

本分册只写序号 **28–33** 用到的接口读面。不新增接口，不新开第八块业务数据，不冻结枚举。字段名按代码实际写。

## 1. 公开资源

只有一条。

| 方法 | 公开路径 | 服务内路径 | 读法 |
|---|---|---|---|
| POST | `/display/v1/situation/panorama/graph` | `/v1/situation/panorama/graph`（`gkxlumen-display`） | 同步。选中技术点后才带路径 |

32 比较、33 播放在页面内完成，不另发请求。28 不接收上传。没有路径专用资源。

## 2. 七个字段中本二级用到的

| 字段 | 本二级用不用 | 用在哪 |
|---|---|---|
| `keyPathOptions` | 用（主块） | 28 路径列表、30 详情、31 筛选、32 比较候选、33 播放步 |
| `nodes` | 用 | 29：画布节点的 `role` / `strength` 做关键节点样式；选中点的 `centrality` 显示中心度格 |
| `timeline` | 只用 `currentYear` 作游标 | 33 不按年份换图。`years` / `events` 来自 `tech_rel` 的年份，不是路径步 |
| `relations` | 不用 | 属于图谱功能。路径的 `relationIds` 为空数组 |
| `listRecords` | 不用 | 属于关联实体功能 |
| `relationTypeOptions` | 不用 | 属于图谱功能 |
| `factorItems` | 不用 | 属于图谱功能 |

另有 `truncated`（超限标记）与 `emptyReason`，不是业务块。

## 3. 请求

页面发出的体（`graphReadParams`）：

| 参数 | 本二级 | 要点 |
|---|---|---|
| `selectedNodeId` | 必须有值才带路径 | Java 依次认 `techPointId`、`nodeId`、`selectedNodeId`、`selectedGraphNodeId` |
| `keyword` | 可空 | 属于搜索定位 |
| `selectedFieldValues` | 可空 | 子学科收窄。Java 先换成 `technology_node_ids`（最多 200） |
| `timeRange` | 透传 | 不截路径 |
| `currentYear` | 固定 `null` | 只回写 `timeline.currentYear`，不换图 |
| `includeLowEvidence` | 可空 | 只影响 `tech_rel`，不影响路径 |

以下请求不读图，直接 501：`action` / `op` / `operation` 为 `import`、`write`、`create`、`upsert`、`delete`、`manual`、`save`；或带 `import`、`manualInput`、`manualNode`、`excel`、`file`；或 `entityRelations=true`。另有 `POST /import`、`POST /manual`、`POST /entity-relations` 均为 501。

## 4. 响应中 `keyPathOptions[]`

`R` 包络 `code=0`，`data.keyPathOptions` 为数组，最多 20 条。

| 字段 | 来源 | 说明 |
|---|---|---|
| `id` | 边属性 `path_id` | 缺 `path_id` 时用 `{src_id}->{dst_id}` |
| `name` / `title` | 拼接 | 步上端点名用「 → 」连接。为空时退为 `id` |
| `summary` | 固定空串 | 技术意义、历程、突破没有正文 |
| `rank` | 读到的顺序 | 1 起。不是优先级 |
| `stageIds` | 端点 | 按 `step_order` 排序后的技术点编号 |
| `nodes[]` | 端点 | 见下表 |
| `relationIds` | 固定空数组 | 路径不挂 `tech_rel` |
| `pathPriority` | 分数表 | Java 按 `id` 读 `path_priority`。无行则 `null`。键总在 |

`nodes[]` 每项：

| 字段 | 来源 |
|---|---|
| `id` / `graphNodeId` | 点 `technology_node_id`，缺则 vid |
| `name` / `name_zh` | `name_zh`，空则 `name_en`，再空则编号。中文空不抄英文进 `name_zh` |
| `role` | 点 `community_role` |
| `strength` | 点 `weighted_degree`。无值不写此键 |
| `stageKey` | 步序下标字符串（`"0"` 起） |
| `typeKey` | 固定 `technology` |
| `timeLabel`、`graphMappingStatus`、`graphMappingLabel` | 固定空串 |
| `graphRelationIds` | 固定空数组 |

路径上没有 `typeKey` / `pathType` 路径级字段。页面类型筛选因此不截数据。

## 5. 响应中 `nodes[].centrality`

Java 在顶层 `nodes[]` 每项都写 `centrality`（无行为 `null`）。数来自分数表 `score_kind=centrality`。Python 载荷里若自带 `centrality` / `influence` / `pathPriority` / `path_priority`，Java 先剥掉再按表填，不透传写死数。

## 6. 下游 `POST /internal/tech-graph/read`

| 项 | 值 |
|---|---|
| 服务 | `lumen-algo-py`（Feign 名 `lumen-platform-algo-py`） |
| Java 发出 | `space=demo_gkx_chain`、`techPointId`（选中时）、`keyword`、`fieldValues`、`includeLowEvidence`、`limits{techPoints:200, relations:200, entitiesPerType:20, paths:20}`、`technology_node_ids`（子学科时） |
| Python 认的选中键 | `technology_node_id` 或 `technologyNodeId`。**不认 `techPointId`**，见第 9 节 |
| Python 认的上限 | 代码常量，不读 `limits` |
| 空间 | `space` 不是 `demo_gkx_chain` 则 422；环境空间不对同样拒绝 |
| 路径查询 | `MATCH (a:tech_point)-[e:tech_path_step]->(b:tech_point)`，`a` 或 `b` 为选中点。返回 `path_id`、`step_order` 和两端 `technology_node_id`、`name_zh`、`name_en`、`community_role`、`weighted_degree` |
| 路径步上限 | `LIMIT 168` |
| 归组 | 按 `path_id` 分组，按 `step_order` 升序。首步取起点，之后每步取终点 |
| 路径上限 | 20 条，超出 `truncated.paths=true` |
| 图上无该边类型 | 视为空数组，不报错 |
| 成功 | `{"code":0,"msg":"ok","data":{...}}` |
| 失败 | 422 空间不对；400 体不是对象；503 nGQL 失败或口令未配。`data` 为空壳，Java 按 `code` 非 0 处理 |

Python 不读分数表，不算中心度、关键节点、优先级。

## 7. 分数只读

| 项 | 值 |
|---|---|
| 实现 | `JdbcPanoramaScores` |
| 表 | `demo_gkxlumenx_ads.ads_technology_panorama_score` |
| SQL | `SELECT subject_id, score_kind, score_value FROM ... WHERE subject_id IN (?, ...)` |
| 编号 | 顶层 `nodes`、`listRecords`、`keyPathOptions` 的 `id` 合并去重，最多 400 个，单个 ≤128 字 |
| 本二级用到的 `score_kind` | `centrality` → `nodes[].centrality`；`path_priority` → `keyPathOptions[].pathPriority` |
| 连接 | 只读连接。口令 `DISPLAY_ADS_PASSWORD`，空则 `ELEMENT_MYSQL_PASSWORD` |
| 失败 | 表不在、连不上、口令空：两格 `null`，路径照常，HTTP 仍 200 |
| 写 | 无。请求内不 INSERT / UPDATE |

## 8. 空态对照

| 情况 | `keyPathOptions` | `pathPriority` | `centrality` | HTTP |
|---|---|---|---|---|
| 未选技术点 | `[]` | — | 有点时按表 | 200 |
| 选中但无路径步 | `[]` | — | 按表 | 200 |
| 有路径无分数行 | 有 | `null` | 按表 | 200 |
| 点列表空 | `[]`，`emptyReason=GRAPH_EMPTY` | — | — | 200 |
| 读图失败 / 空间不对 | 无 `data` | — | — | 502 |
| 写操作 / 实体间关系 | 不读 | — | — | 501 |

## 9. as-built 不一致（只登记，不改）

- 选中键不一致：Java 发 `techPointId`，Python 只认 `technology_node_id` / `technologyNodeId`。经完整链路时 Python 不回路径。归 `TS-L2-DS02-SEL-FIX-L01`。
- `truncated` 不透传：Java 丢掉 Python 的 `truncated`，只写自己截的块；Python 已截到 20，Java 不会再截，路径超限标记不出现。归 `TS-L2-DS02-SEL-FIX-L01`（DoD「可选同单」）。
- `limits` 不生效：Python 用常量，与 Java 发出的值相同，暂无影响。
- 路径只带与选中点相连的步，不是整条路径。口径项，转客户决策清单；改读法未建单。

## 10. 明确不做

- 不新增接口，不拆路径资源，不加第八块。
- 不冻结 `keyPathOptions` 枚举。不写 DTO。
- 不改代码，不改说明书。
- 不新造 `metric_id`，不改 D4。
