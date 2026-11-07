# TS-L2-DS02-GRAPH-API · 科学技术全景 · 展示技术点图谱 · 后台接口（as-built）

- 任务：`TS-L2-DS02-GRAPH-API`
- 日期：2026-11-07
- 监管：`human:淮政玮`
- 认领：`agent:arch-agent`（兼 api）
- 强度：ponytail off（定义任务，不缩文档）
- 状态：as-built 稿已落盘；四角色已会签（`sdd/l2/会签/TS-L2-DS02-L2SET-SIGNOFF-*.md`），未签收
- 上游：`sdd/l2/TS-L2-DS02-GRAPH-ARCH.md`（本分册以它为准）；说明书 §3、§6；`SYSINT-05-01B-L01`、`TS-L2-DS02-READ-PY-L01`、`SYSINT-05-01A-L01`
- 核对代码：`lumen-svc-platform` `SituationPanoramaController` / `SituationPanoramaService` / `TechGraphReadAdapter` / `RemoteTechGraphClient`（`271109c`）；`lumen-algo-py` `views/tech_graph_read.py`、`algorithms/tech_graph_read.py`（`07ffa9f`）；`lumen-ui-science-pc` `src/api/situation/panorama.ts`、`src/lib/graph/liveGraph.ts`

本分册写序号 17–21 用到的接口，按代码实际字段名。不新增接口，不冻结 OpenAPI，不改七个字段的名字。

## 1. 公开资源

浏览器经网关 `/display/**` 打 `gkxlumen-display`。服务内路径前缀 `/v1/situation/panorama`。

| 序号 | 资源 | 读法 |
|---|---|---|
| 18、20、21 | `POST /display/v1/situation/panorama/graph` | 同步。成功 200；空图 200 + `GRAPH_EMPTY`；读失败 502 |
| 17 | `POST /display/v1/situation/panorama/import`、`POST .../manual` | 501，不落库，不调读图 |
| 17 | `POST .../graph` 带写入动作 | 501，同上 |
| 19 | 无 | 页面内完成 |
| 领域下拉（as-built） | `POST /display/v1/situation/panorama/subfields` | 同步。读子学科字典，失败时 `items=[]` + `note`。2026-11-06 加入，说明书未列，记偏离 |

响应包络是 `R`：`{code, msg, data}`。`code=0` 成功；501 / 502 时 `code=1`，`data=null`。

## 2. `graph` 请求体

前端 `graphReadParams` 实际发出：

| 字段 | 序号 | 值 |
|---|---|---|
| `selectedFieldValues` | 18（领域筛选） | 子学科 `subfield_id` 列表。空则不收窄 |
| `timeRange` | — | 前端照发。Java 不读 |
| `currentYear` | — | 固定 `null`。不是第二套快照入参 |
| `keyword` | 20 | 搜索字，去空白。空则不发 |
| `selectedNodeId` | 21 | 选中技术点的 `id`（= `technology_node_id`）。未选为 `null` |

Java 认的字段（含别名，取第一个非空）：

| 用途 | 字段 |
|---|---|
| 选中点 | `techPointId`、`nodeId`、`selectedNodeId`、`selectedGraphNodeId` |
| 搜索字 | `keyword`、`q`、`globalSearchTerm` |
| 领域 | `selectedFieldValues`、`fieldValues` |
| 低证据 | `includeLowEvidence`（`true` / `"true"`） |
| 播放游标 | `currentYear`，只回写 `timeline.currentYear` |
| 判为写入（→ 501） | `action` / `op` / `operation` 取 `import`、`write`、`create`、`upsert`、`delete`、`manual`、`save`；或带 `import`、`manualInput`、`manualNode`、`excel`、`file` 任一键 |
| 判为实体间关系（序号 26，→ 501） | `entityRelations=true`；或 `feature` / `scope` 为 `26`、`entity-relation`、`entity-relations` |

## 3. `graph` 响应：本二级用哪几块

七个字段全部返回。序号 17–21 只用其中四块。

| 字段 | 本二级 | 用在 |
|---|---|---|
| `nodes` | 用 | 18 画点、20 命中高亮、21 详情 |
| `relations` | 用 | 18 画技术点关系。未选点时恒为 `[]` |
| `relationTypeOptions` | 用 | 18 区分关系类型。由 `relations[].relationType` 去重而来 |
| `factorItems` | 用 | 18 图例。有点时含 `{key: technology, label: 技术点}` |
| `timeline` | 不用 | 播放游标，归 33 |
| `listRecords` | 不用 | 关联实体，归 22–27 |
| `keyPathOptions` | 不用 | 关键路径，归 28–33 |

另有两个非业务字段：`truncated`（超限才出现，见第 6 节）、`emptyReason`（只在 `nodes` 为空时出现，值 `GRAPH_EMPTY`）。不是第八块业务数据。

`nodes[]` 字段：

| 字段 | 来源 | 说明 |
|---|---|---|
| `id` | `tech_point.technology_node_id`，缺则 VID | 业务编号 |
| `label`、`name` | `name_zh`，空则 `name_en`，再空则 `id` | 显示名 |
| `name_zh`、`name_en` | 点属性原样 | 中文空就空，不抄英文 |
| `type` | 固定 `技术点` | — |
| `factorKey` | 固定 `technology` | — |
| `role` | `community_role` | 关键节点样式 |
| `strength` | `weighted_degree`，无则不写 | 详情抽屉标为「关系强度」 |
| `centrality` | Java 从分数表叠加；无行为 `null` | 身份 `M_TECH_PATH_CENTRALITY`，归 29。见 METRIC 分册 |
| `influence` | 仅分数表有行时叠加 | 归 27 |

Python 载荷里若自带 `influence`、`centrality`、`pathPriority`，Java 先剥掉，再按编号叠加分数表的值。

`relations[]` 字段：

| 字段 | 来源 |
|---|---|
| `id` | `tech_rel:{source}:{target}:{relation_type}:{序号}` |
| `source`、`target` | 两端 `technology_node_id` |
| `type`、`relationType`、`label` | `relation_type` |
| `evidenceLevel` | `evidence_level` 转大写 |
| `weight` | `relation_confidence_score`，无则不写 |
| `year` | `first_evidence_year` 为四位年时才写 |

## 4. 空态与失败态

| 情形 | HTTP | `data` |
|---|---|---|
| 有点 | 200 | 七个字段，无 `emptyReason` |
| 有点无边 | 200 | `relations=[]`、`relationTypeOptions=[]` |
| 无点（含搜索无命中、子学科对不上任何技术点） | 200 | 七个字段为空，`emptyReason=GRAPH_EMPTY` |
| 读图失败（Python 非 0、Feign 异常、无 `data`、`space` 不是 `demo_gkx_chain`） | 502 | `null`，`msg=技术点图读取失败` 或 `图空间不是 demo_gkx_chain` |
| 子学科字典失败 | 502 | `null`，`msg=子学科技术点读取失败` |
| 分数表不可读 | 200 | 图照常，`centrality=null` |
| 序号 17 写入 | 501 | `null`，`msg=序号 17 不在本页写入` |

不再返回 `GRAPH_NOT_READY`。前端 `coerceLiveGraph` 若仍收到它，有点时去掉，无点时改成 `GRAPH_EMPTY`。

## 5. 下游 `POST /internal/tech-graph/read`

display 下发（`SituationPanoramaService.query`）：

| 字段 | 值 |
|---|---|
| `space` | 固定 `demo_gkx_chain` |
| `techPointId` | 选中点，有才发 |
| `keyword` | 搜索字，有才发 |
| `fieldValues` | 领域原样 |
| `includeLowEvidence` | 布尔 |
| `limits` | `{techPoints:200, relations:200, entitiesPerType:20, paths:20}` |
| `technology_node_ids` | 选了领域时，子学科对上的技术点编号，最多 200 |

Python 实际读的字段：

| 字段 | 作用 |
|---|---|
| `space` | 非空且不是 `demo_gkx_chain` → 422 |
| `technology_node_id` / `technologyNodeId` | 选中点。有才查关系、实体、路径 |
| `keyword` | `name_zh` / `name_en` `CONTAINS` |
| `technology_node_ids` / `technologyNodeIds` | 按编号收窄点。空列表 → 无点 |
| `include_low_evidence` / `includeLowEvidence` | 带上 `LOW` |

Python 不读 `techPointId`、`fieldValues`、`limits`。上限写死在 Python 常量里，与 Java 一致。

**不一致**：display 用 `techPointId` 下发选中点，Python 不认。按 2026-11-07 的代码，选中技术点后 Python 仍按「未选点」处理，`relations`、`listRecords`、`keyPathOptions` 恒空。两侧单测各用各的字段名（Java 测 `techPointId`，Python 测 `technology_node_id`），没有覆盖这一跳。已登记修复单 `TS-L2-DS02-SEL-FIX-L01`（ready，改 Java 一侧为 `technology_node_id`，加一条断言下发字段的单测）。原实现单 `SYSINT-05-01B-L01`、`TS-L2-DS02-READ-PY-L01` 已 done，不再挂账。本分册不改代码。

另：Python 按选中点查点时把 `id(v) == …` 与属性等值写在同一个 `WHERE`，属性无索引报 `IndexNotFound` 后整条当空（ARCH 分册第 6 节「查询缺口」，未建单）。只修字段名，选中点仍可能取空。

Python 响应：`{code, msg, data}`。

| HTTP | `code` | 情形 |
|---|---|---|
| 200 | 0 | `data` = `space` + 七个字段 + `truncated` + 空图时 `emptyReason=GRAPH_EMPTY` |
| 422 | 1 | 空间不对。`data` 为空壳 |
| 400 | 1 | body 不是对象 |
| 503 | 1 | nGQL 失败、`USE` 失败、Nebula 密码未配置 |

Python `truncated` 键：`nodes`、`relations`、`person`、`institution`、`paper`、`patent`、`paths`。nGQL 报错含 `not found`、`unknown column`、`IndexNotFound` 等时当空，不算失败。

## 6. 截断

Java 只输出自己截出来的 `truncated`：`nodes`、`relations`、`entities`、`paths`，都没超限时不出现这个字段。Python 每类多取一行判断超限后截到上限，Java 收到的已是上限内条数，所以 Python 的超限标记在公开响应里丢失。说明书 §3 要求标明截断，这一处待修，归 `TS-L2-DS02-SEL-FIX-L01`（该单 DoD 写的是「可选同单」）。

## 7. 明确不做

- 不新增接口。`/subfields` 是已有实现，只记录，不在本分册设计。
- 不冻结 OpenAPI 与枚举闭集。
- 序号 17 不设计写接口。
- 不写代码，不改控制器、Feign、Python 视图。
