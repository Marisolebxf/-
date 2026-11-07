# TS-L2-DS02-ENTITY-API · 科学技术全景 · 展示技术点关联实体 · 后台接口

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:arch-agent`（兼 api 分册） |
| supervised_by | `human:淮政玮` |
| claim_type | 监管人会话派单。本会话不改 task-registry，未经 MCP 认领 |
| 说明 | 只写文档。不写代码、不改库、不 commit。不标 done |

## Ponytail

ponytail: off（定义任务）

不缩文档。未用 YAGNI 跳过 501 与空态的差别、字段名断点、下游错误码。

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `TS-L2-DS02-ENTITY-ARCH-SEQ` |
| 图 diff | 本分册不改图，只补字段 |
| 会签态 | 源文件无 frontmatter，记 `draft` |
| 说明 | 图在 `sdd/l2/TS-L2-DS02-ENTITY-ARCH.md` 第 2 节 |

## 范围与实现

序号 22–27。只写已有接口的读面，不新增接口：

| 序号 | 资源 | 读法 |
|---|---|---|
| 22–25、27 | `POST /display/v1/situation/panorama/graph` | 同步。七个字段里用 `listRecords`、`factorItems`，间接用 `nodes` |
| 26 | `POST /display/v1/situation/panorama/entity-relations`；`graph` 带 `entityRelations=true` | 501 |

要点：

- 选中点：前端发 `selectedNodeId`；Java 认 `techPointId` / `nodeId` / `selectedNodeId` / `selectedGraphNodeId`；转给 Python 用 `techPointId`。
- 下游 `POST /internal/tech-graph/read`：空间恒 `demo_gkx_chain`；实体每类 ≤20，按名称排序；422 / 400 / 503 时 Java 一律 502。
- 类型、时间筛选与排序都在前端，对已取回结果做。排序字段 `relationStrength` / `name` / `type` / `time`，live 下加 `influence`。
- 影响力：Java 按 `listRecords[].id` 只读 `demo_gkxlumenx_ads.ads_technology_panorama_score` 的 `score_kind=influence`，无行为 null。

## 偏离

文档本身无偏离。as-built 不一致见分册第 8 节，主要两条：

1. Python 只认 `technology_node_id` / `technologyNodeId`，不认 Java 发的 `techPointId`。选中点不生效。
2. 前端 live 实体区不读 `listRecords`。

## 产物清单

- `sdd/l2/TS-L2-DS02-ENTITY-API.md`
- 本 handoff

## 验收证据

- 分册已落盘：公开资源、七字段用法、`listRecords` 行字段、三段请求参数、下游出入参与错误码、影响力读法、筛选排序分层、序号 26 入口、差异表。
- 字段名逐个对照代码：`SituationPanoramaService.query()`、`assemble()`、`isEntityRelation()`；`tech_graph_read.py` `_node_id()`、`_record()`、`_entity_ngql()`；`liveGraph.ts` `graphReadParams()`；`GraphAnalysisPanel.vue` 排序筛选；`entityRanking.ts` 选项。
- 定义单，无业务 CI，无 PR。未 commit。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ Java 不排序、不打分；影响力只 SELECT |
| 2 调用链 | ✅ 浏览器只打 `/display/**`；Java 调 `/internal/tech-graph/read` |
| 3 图谱 Nebula | ✅ `space` 恒 `demo_gkx_chain`，Java 不写 nGQL |
| 4 可观测 | ✅ 沿既有链路 trace，本叶不新加 |
| 5 CI/CD | ✅ 定义文档，无部署 |
| 6 demo 只读 | ✅ 不引用 demo 代码 |
| 7 共享聚合核心 | ✅ 前端只调 Java；Java 只读 ADS |
| 8 数据策略 | ✅ 实体真读图，影响力读 ADS mock |
| 9 D8 | ✅ 不改页面 |
| 10 D9 | ✅ 不新造 `metric_id`，影响力挂已有 id |
| 11 D10 | ✅ 不改交互 |
| 12 D12 | ✅ Feign `lumen-platform-algo-py`，不调 `demo-*` |
| 13 D14 | ✅ 不涉及对象存储 |
| 14 D16 | ✅ 不用 `gapfill_` |
| 15 D17 | ✅ 不改锁定算法 |
| 16 D18 | ✅ 接口不写死分数，Python 载荷里的分数被剥掉，只认 ADS 表 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 45000（估算） |
| model_used | claude-opus |
| actual_cost | 1.22 |
| cost_warn | green |

按 architect 80/20、C 档 `$15/$75`：`45000×0.8×15/1e6 + 45000×0.2×75/1e6 = 1.215`，记 `1.22`。

## 遗留风险

- 字段名断点不修，边上图后实体仍为空。Java 单测用假读图器，覆盖不到这条。
- 集群 display 未配 `DISPLAY_ADS_PASSWORD` 时影响力全空。
- `API-TS-M2` 未冻结，本分册不替代它。

## CI/CD

- 分支：`gkx-orchestration` `dev`（未提交，等监管人确认）
- pipeline：编排仓无业务 CI
- K8s rollout：无

## 涉及文件

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-ENTITY-API.md`
- `agent-delivery/agent-handoffs/科学技术全景-DS02/TS-L2-DS02-ENTITY-API.md`
