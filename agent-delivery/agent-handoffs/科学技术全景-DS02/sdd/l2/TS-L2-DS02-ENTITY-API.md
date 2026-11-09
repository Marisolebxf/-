# TS-L2-DS02-ENTITY-API · 科学技术全景 · 展示技术点关联实体 · 后台接口

- 任务：`TS-L2-DS02-ENTITY-API`
- 日期：2026-11-07
- 监管：`human:淮政玮`
- 认领：`agent:arch-agent`（兼 api 分册）
- 状态：as-built 稿已落盘；四角色已会签（`sdd/l2/会签/TS-L2-DS02-L2SET-SIGNOFF-*.md`），未签收
- 强度：ponytail off（定义任务，不缩文档）
- 上游：`sdd/科学技术全景-系统详细设计说明书.md` §2.2、§3、§6；`sdd/l2/TS-L2-DS02-ARCH.md` §2、§4.2；本目录 `TS-L2-DS02-ENTITY-ARCH.md`
- 代码核对：`lumen-svc-platform` `SituationPanoramaController` / `SituationPanoramaService` / `TechGraphReadAdapter` / `JdbcPanoramaScores`；`lumen-algo-py` `lumen_common/algorithms/tech_graph_read.py`、`lumen_algo_service/views/tech_graph_read.py`；`lumen-ui-science-pc` `src/lib/graph/liveGraph.ts`、`src/api/situation/panorama.ts`、`GraphAnalysisPanel.vue`

本分册只写序号 22–27 用到的接口读面。不新增接口，不改字段名，不冻结 OpenAPI。字段名按代码现状写。

## 1. 公开资源

| 资源 | 方法 | 本二级用途 | 返回 |
|---|---|---|---|
| `/display/v1/situation/panorama/graph` | POST | 22–25、27 | 200 七个字段；读图失败 502 |
| `/display/v1/situation/panorama/entity-relations` | POST | 26 | 501，`msg=序号 26 没有实体间关系` |

服务内路径是 `/v1/situation/panorama/graph`，网关只转 `/display/**`。响应包络是 `R`（`code` / `msg` / `data`）。

## 2. 七个字段里本二级用哪几块

| 字段 | 本二级 | 说明 |
|---|---|---|
| `listRecords` | 用 | 实体名单。只在选中技术点后有内容 |
| `nodes` | 间接用 | 选中点高亮、实体详情里的关联技术点名称 |
| `relations` | 不用 | 只放技术点之间的 `tech_rel`，不放技术点到实体的边 |
| `timeline` | 不用 | 年份来自 `tech_rel.first_evidence_year`，不是实体时间线 |
| `factorItems` | 用 | 实体类型开关。Python 按 `listRecords` 里出现的类型追加 `person` / `institution` / `paper` / `patent` |
| `keyPathOptions` | 不用 | 归关键路径 |
| `relationTypeOptions` | 不用 | 技术点关系类型 |

另有 `truncated`（超上限时出现）和 `emptyReason=GRAPH_EMPTY`（技术点为空时）。二者不是第八块业务数据。

### 2.1 `listRecords[]` 一行

由 Python 产出。Java 只在缺省时补 `id`、`name`、`label`，并填 `influence`。

| 字段 | 值 |
|---|---|
| `id` | 业务编号：`paper_id` / `patent_id` / `institution_id` / `talent_id`；缺则用顶点 vid |
| `typeKey` | `person` / `institution` / `paper` / `patent` |
| `typeLabel` | 人 / 机构 / 论文 / 专利 |
| `name` | `name_zh`，空则 `name_en`，再空则编号 |
| `name_zh`、`name_en` | 顶点原值。中文空就空 |
| `nodeIds` | `[选中技术点编号]` |
| `relationCount` | 恒为 1（见 §8） |
| `regionKeys`、`owner`、`summary`、`updatedAt` | 空 |
| `source_paper`、`source_topic` | 仅 `person`，布尔 |
| `influence` | Java 填。分数表 `influence` 值；无行为 null |

没有 `weight`、`relationStrength`、`year` 字段。

## 3. 请求参数

### 3.1 前端 → Java

前端 live 下由 `graphReadParams` 生成请求体：

| 字段 | 值 |
|---|---|
| `selectedNodeId` | 选中技术点编号；未选为 null |
| `selectedFieldValues` | 技术领域（子学科）多选 |
| `keyword` | 搜索字，可空 |
| `timeRange` | 页面时间范围。Java 不读 |
| `currentYear` | 恒为 null。不作为第二套快照入参 |

Java 认的选中点别名：`techPointId`、`nodeId`、`selectedNodeId`、`selectedGraphNodeId`，取第一个非空。

### 3.2 Java → Python

`POST /internal/tech-graph/read`，Feign 服务名 `lumen-platform-algo-py`。

| 字段 | 值 |
|---|---|
| `space` | 恒为 `demo_gkx_chain` |
| `techPointId` | 选中点编号；未选不带 |
| `keyword` | 搜索字 |
| `fieldValues` | 原样转发。Python 不读 |
| `technology_node_ids` | 有领域筛选时，子学科字典解出的技术点编号，最多 200 |
| `includeLowEvidence` | 布尔，默认 false |
| `limits` | `techPoints=200`、`relations=200`、`entitiesPerType=20`、`paths=20`。Python 用自身常量，不读 |

### 3.3 Python 认的字段

| 字段 | Python 读法 |
|---|---|
| 选中点 | `technology_node_id`，或 `technologyNodeId` |
| 搜索字 | `keyword` |
| 技术点范围 | `technology_node_ids`，或 `technologyNodeIds` |
| 低证据 | `include_low_evidence`，或 `includeLowEvidence` |
| 空间 | `space`；非 `demo_gkx_chain` 拒绝 |

**字段名断点**：Java 发 `techPointId`，Python 不认。选中点到不了 Python，返回的是概览（只有技术点，`listRecords=[]`）。见 §8 第 1 条。

## 4. 下游 `POST /internal/tech-graph/read`

| 项 | 要点 |
|---|---|
| 成功 | `{"code":0,"msg":"ok","data":{...}}` |
| 空间不对 | 422，`code=1`，`data` 为空形状 |
| 入参不是对象 | 400 |
| nGQL 失败 / 未配密码 | 503 |
| `data` 键 | `space`、`nodes`、`relations`、`keyPathOptions`、`timeline`、`listRecords`、`relationTypeOptions`、`factorItems`、`truncated`，空图另带 `emptyReason=GRAPH_EMPTY` |
| 未选点 | 只回最多 200 个 `tech_point`，不查边、实体、路径 |
| 选中点 | 读 `tech_rel` ≤200、四类实体各 ≤20、`tech_path_step` 归成路径 ≤20 |
| 实体查询 | 论文 / 专利 / 机构先按点属性 `technology_node_id` 扫，再按 `tech_point` 经 `tech_has_*` 走边；两路按 vid 去重。人只走边 |
| 实体排序 | 按 `name_zh`、`name_en`、编号升序后截 20 |
| 吞掉当空的错误 | `not found`、`unknown tag/edge/column`、`invalid ... property`、`IndexNotFound` 等 |
| 截断 | `truncated.person / institution / paper / patent` |
| 不做 | 不写图，不算影响力、中心度、优先级，不返回 fixture |

Java 收到 `code≠0`、连不上、没有 `data`、`space` 不是 `demo_gkx_chain`，一律 502，不改成空图。

## 5. 影响力

| 项 | 值 |
|---|---|
| 库表 | `demo_gkxlumenx_ads.ads_technology_panorama_score` |
| 读法 | `SELECT subject_id, score_kind, score_value FROM ... WHERE subject_id IN (?...)`，只读连接 |
| 键 | `subject_id` = `listRecords[].id` |
| 取值 | `score_kind=influence` → `listRecords[].influence` |
| 编号上限 | 一次 400 个（技术点、实体、路径合并去重） |
| 剥离 | Python 载荷里自带的 `influence` / `centrality` / `pathPriority` 先删，只认分数表 |
| 失败 | 无行、表不在、连不上、未配口令 → null，名单照常 |
| 连接 | 默认 `jdbc:mysql://10.50.11.76:3306/demo_gkxlumenx_ads`，用户 `gkxlumenx`；口令 `DISPLAY_ADS_PASSWORD`，空则 `ELEMENT_MYSQL_PASSWORD` |

## 6. 筛选与排序在哪层

| 动作 | 层 | 字段 |
|---|---|---|
| 22 取前 5 | 前端 | `scopedEntityRanking = 排好序的全部行.slice(0, 5)` |
| 23 换点 | 前端触发，后端重读 | `selectedNodeId` 变化即重发 `graph` |
| 25 按类型 | 前端 | `entityRankingType`；另有实体类型开关 `enabledFactorKeys` |
| 25 按时间 | 前端 | `entityRankingTimeRange`（全部 / 2024-2026 / 2022-2023 / 2020-2021）。按行的 `year`；没有年份的行不截 |
| 27 排序 | 前端 | `entityRankingSortBy`：`relationStrength`（关联强度）、`name`、`type`、`time`；live 下另加 `influence` |
| 27 按影响力 | 前端 | 过滤 `influence != null` 后降序 |

Java 与 Python 都不接收类型、时间、排序参数。

## 7. 序号 26

| 入口 | 结果 |
|---|---|
| `POST /display/v1/situation/panorama/entity-relations` | 501，不调读图 |
| `POST .../graph` 带 `entityRelations=true` | 501，不调读图 |
| `POST .../graph` 带 `feature` / `scope` 为 `26`、`entity-relation`、`entity-relations` | 501 |
| 页面 live | 不发请求，该块空，文案「实体间关系暂无数据」 |

## 8. as-built 与说明书的差异

| # | 现象 | 影响 | 归属 |
|---|---|---|---|
| 1 | Java 发 `techPointId`，Python 只认 `technology_node_id` / `technologyNodeId` | 选中点不生效，实体永远为空 | `TS-L2-DS02-SEL-FIX-L01`（ready）。原单 `SYSINT-05-01B-L01`、`TS-L2-DS02-READ-PY-L01` 已 done |
| 2 | 前端 live 实体区由 `nodes` + `relations` 推导，不读 `listRecords` | 后端有实体也不显示 | `TS-L2-DS02-FE-ENTITY-FIX-L01`（backlog，依赖 `SEL-FIX`）。原单 `SYSINT-05-01A-L01` 已 done |
| 3 | 实体行无 `weight` / `relationStrength` / `year` | 关联强度空；时间筛选不起作用 | 写边规格现定 `tech_has_*` 不带强度、年份；要加须改写边规格，归 `SYSINT-TECHGRAPH-02-L02`。读图补取未建单 |
| 4 | `relationCount` 恒 1 | 不是说明书写的邻居个数 | 原单 `TS-L2-DS02-READ-PY-L01` 已 done，返修未建单 |
| 5 | Java 不透传 Python 分类型截断标记 | 实体截断标记丢失 | `TS-L2-DS02-SEL-FIX-L01`（DoD「可选同单」） |
| 6 | Java 转发 `fieldValues`、`limits`，Python 不读 | 无功能影响，属冗余字段 | 不改 |

## 9. 不做

- 不新增接口，不新增字段块，不改七个字段名。
- 不在 Java 算排序、强度、影响力。
- 不为序号 26 建写接口或实体间查询。
- 不冻结 `API-TS-M2`。
