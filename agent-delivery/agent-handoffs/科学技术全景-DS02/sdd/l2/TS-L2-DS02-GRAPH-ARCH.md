# TS-L2-DS02-GRAPH-ARCH · 科学技术全景 · 展示技术点图谱 · 架构（as-built）

- 任务：`TS-L2-DS02-GRAPH-ARCH`
- 日期：2026-11-07
- 监管：`human:淮政玮`
- 认领：`agent:arch-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 状态：as-built 稿已落盘；四角色已会签（`sdd/l2/会签/TS-L2-DS02-L2SET-SIGNOFF-*.md`），未签收
- 2026-11-07 复查：图上已有技术点关系、关联实体与路径步。样本 `tcn_000f21ac06aceb9cdd0575e82d0d85fc` 用 `technology_node_id` 直调 Python 读图：关系 65、实体 61、路径 2。`path_priority` 仍 0 行。正文 11-05 的现状保留作记录，以本行为准。见 `工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS02-GRAPH-合规演示用例.md`
- 上游：`sdd/科学技术全景-系统详细设计说明书.md` §2.1、§3、§4、§6、§7；`sdd/l2/TS-L2-DS02-ARCH.md`；`功能拆解.md` 序号 17–21；`方案-算法中台基础数据准备.md`；需规 `科学技术全景.md` 序号 17–21
- 实现事实：`TS-L2-DS02-READ-PY-L01`、`SYSINT-05-01B-L01`、`SYSINT-05-01A-L01`、`TS-L2-DS02-TEST-L01`
- 图：`TS-L2-DS02-GRAPH-SEQ`、`TS-L2-DS02-GRAPH-DATA`（本文两张 Mermaid，无 frontmatter，记 `draft`）

本分册只写需规二级「展示技术点图谱」（序号 17–21）按已实现代码的样子。不重开说明书已定的决策，不新造 `metric_id`，不新增接口。

核对的代码版本：

| 仓 | commit | 内容 |
|---|---|---|
| `lumen-algo-py` | `a03c52b`、`4e7f453`、`07ffa9f` | `POST /internal/tech-graph/read`；按编号收窄；IndexNotFound 当空 |
| `lumen-svc-platform` | `cbd6f10`、`271109c` | `gkxlumen-display` 装配七个字段；子学科收窄 |
| `lumen-ui-science-pc` | `e6fb1dd`、`b603e63`、`034d7fb`、`0640f1b`、`5e6e96e` | 只消费一次 `graph`；无边网格布局；技术领域改子学科多选 |

## 1. 范围

| 序号 | 功能 | 判定 | 页面位置 |
|---|---|---|---|
| 17 | 技术点图谱数据输入 | 501。本页不收输入 | 工具栏「导入」「手动添加」只改本次浏览 |
| 18 | 图结构自动生成 | 真读已有图 | 主画布「图谱」 |
| 19 | 图谱交互操作 | 页面内完成，不另发请求 | 主画布 |
| 20 | 技术点搜索定位 | 真读。同一次 `graph` 带搜索字 | 筛选条搜索框 |
| 21 | 技术点详情查看 | 真读该点已有属性 | 详情抽屉 |

不在本二级：序号 22–27（关联实体）、28–33（关键路径）、34–47（维护）。同一次 `graph` 会顺带返回实体和路径，本分册只写图谱用到的部分。

## 2. 调用链

```mermaid
flowchart LR
  page["全景页<br/>lumen-ui-science-pc<br/>src/views/situation/panorama"]
  gw["gkxlumen-platform-gateway<br/>/display/**"]
  bff["gkxlumen-display<br/>POST /v1/situation/panorama/graph"]
  py["lumen-algo-py（Feign 名 lumen-platform-algo-py）<br/>POST /internal/tech-graph/read"]
  graph["Nebula demo_gkx_chain"]
  dict["gkxlumen-platform-search-py（lumen-topic-py）<br/>POST /internal/gkx-svc/dict/query"]
  score["demo_gkxlumenx_ads<br/>ads_technology_panorama_score"]
  page -->|"一次 graph"| gw --> bff
  bff -->|"技术点、技术点关系"| py -->|"只读 MATCH"| graph
  bff -->|"选了技术领域时：子学科 → 技术点编号"| dict
  bff -->|"按编号只读 centrality"| score
```

| 跳 | 实现 | 要点 |
|---|---|---|
| 浏览器 → 网关 | `src/api/situation/panorama.ts` 的 `post` | 只打 `/display/v1/situation/panorama/graph`。不打 Python，不打 `/ops/v1/tech-graphs/**` |
| display → Python | Feign `RemoteTechGraphClient`，name `lumen-platform-algo-py`，默认 `http://lumen-platform-algo-py:8000`，`@NoToken` | 请求带 `space=demo_gkx_chain`。响应 `space` 不是它就 502 |
| Python → 图 | `tech_graph_read.py` | `USE demo_gkx_chain` 后只发 `MATCH`。请求 `space` 不是 `demo_gkx_chain` 返回 422 |
| display → 字典 | Feign `RemoteDisciplineDictClient`，op `technology_graph_subfield_nodes` | 只在请求带技术领域时调用。见第 6 节偏离 |
| display → 分数表 | `JdbcPanoramaScores` 只读 `SELECT` | 本二级只用到点上的 `centrality`。无行、表不在、连不上，该格 null |

Java 不写 nGQL，不经 `gkxlumen-graph`，不调用 `demo-*`。三个数字不在请求内计算。

## 3. 数据流

```mermaid
flowchart TD
  l1["SYSINT-TECHGRAPH-02-L01<br/>技术点入库 + 技术点入图"]
  l2["SYSINT-TECHGRAPH-02-L02<br/>技术点关系上图（backlog）"]
  tp["Tag tech_point"]
  tr["Edge tech_rel"]
  f18["18 画布：点 + 选中后的关系"]
  f20["20 搜索：名称包含"]
  f21["21 详情：已有属性"]
  l1 --> tp
  l2 -.-> tr
  tp --> f18
  tp --> f20
  tp --> f21
  tr --> f18
```

本二级不准备数据。点和边都由第 2 项按钮写入。本页不把 `mock/modules/panorama.ts` 的节点灌进图，接口也不返回它们。

## 4. 功能流程（as-built）

1. 打开页面：前端发一次 `graph`，不带 `selectedNodeId`。Python 回最多 200 个 `tech_point`，不查边。画布只画技术点。
2. 无边时：前端用网格布局画点（`b603e63`）。之前径向布局在无边时排不出坐标，画布空白。
3. 序号 19：缩放、平移、拖拽、高亮在 `KnowledgeGraphCanvas.vue` 内完成，不发请求。
4. 序号 20：搜索字以 `keyword` 发出。Python 对 `name_zh`、`name_en` 做 `CONTAINS`。命中点由前端高亮并居中。没有单独的精确匹配参数。
5. 序号 21：点一个技术点，前端再发一次 `graph`，带 `selectedNodeId`。抽屉显示该点已有字段。没有描述、发展状态时对应行空。
6. 序号 17：导入、手动添加、撤销只改本次浏览的 `importedGraphExtras`，提示写明「服务端不接收写入（501），未落库」。Java 的 `/import`、`/manual` 与带写入动作的 `/graph` 返回 501。

## 5. 空态、失败态、上限

| 情形 | 后端 | 前端 |
|---|---|---|
| 图上没有点 | HTTP 200，七个字段为空，`emptyReason=GRAPH_EMPTY` | 画布空。不用种子填 |
| 有点、无边 | HTTP 200，`relations=[]`，无 `emptyReason` | 网格布局画点 |
| 搜索无命中 | 同「没有点」：`GRAPH_EMPTY` | 画布空 |
| Python 422（空间不对）/ 400 / 503（nGQL 失败或未配密码） | display 收到 `code≠0` 或 Feign 异常，返回 HTTP 502，`data=null` | 保留上一次成功结果，提示读取失败。不画种子 |
| 子学科字典失败 | HTTP 502，「子学科技术点读取失败」 | 同上 |
| 分数表不可读 | 图照常返回，`centrality=null` | 详情抽屉不显示中心度卡 |
| 写入（序号 17） | HTTP 501，`R.failed("序号 17 不在本页写入")`，不调读图 | 只留本次浏览 |

| 上限 | Python | Java |
|---|---|---|
| 未选点 | `tech_point` 取 201 行，留 200，`truncated.nodes=true` | 再截 200，自己的 `truncated.nodes` |
| 选中点后的关系 | `tech_rel` 取 201 行，留 200；默认只要 `HIGH`、`MEDIUM` | 再滤一次低证据；两端都不在 `nodes` 里的关系丢掉；截 200 |
| 子学科 | — | 子学科最多 50 个；对上的技术点编号最多 200 个下发 |

这是页面一次能看的范围，不是入图规则。

## 6. 偏离与不一致（as-built 对说明书）

| 项 | 说明书 | as-built | 处理 |
|---|---|---|---|
| 领域筛选 | §3：只留已经挂上产业的技术点 | 改成子学科多选。display 经 `lumen-topic-py` op `technology_graph_subfield_nodes`（`ads_technology_paper` ⋈ `ads_discipline_topic`，按代表论文 Primary Topic）换成技术点编号，再交 Python 用 `technology_node_ids` 收窄。另加 `POST /v1/situation/panorama/subfields` 读子学科选项。子学科两步读的是 `lumen-topic-py` 的 `JX_ADS_DATABASE`（默认 `gkx_technology_analysis_dev` @ `47.93.119.170`），不是 `demo_gkxlumenx_ads` | 记偏离。四角色同意 as-built；「技术领域」口径转客户决策清单（见 `会签/TS-L2-DS02-L2SET-SIGNOFF-PRODUCT.md`）。本分册不改代码，不把它写成新接口设计 |
| 选中点入参 | 说明书不定字段名 | Java 下发 `techPointId`；Python 只认 `technology_node_id` / `technologyNodeId` | 选中点不会到达 Python，关系、实体、路径恒空。见 API 分册第 5 节。待修，归 `TS-L2-DS02-SEL-FIX-L01`（原实现单 `SYSINT-05-01B-L01`、`TS-L2-DS02-READ-PY-L01` 已 done） |
| 截断标记 | §3：超过上限要标明截断 | Java 不透传 Python 的 `truncated`，只写自己 `cap` 出的标记。Python 已截到 200 时，Java 看不到超限 | 待修，归 `TS-L2-DS02-SEL-FIX-L01`（该单 DoD 写的是「可选同单」） |
| 查询缺口 | §6：读失败不用空壳冒充成功 | `07ffa9f` 起 `IndexNotFound` 一律当空。属性 `WHERE` 没有索引时，搜索（`CONTAINS`）、领域收窄（`technology_node_id IN [...]`）、选中点（`id() == … OR 属性 == …` 写在同一个 `WHERE`）、关系都可能返回空而不报错，对外表现为 `GRAPH_EMPTY` 或空块 | 与说明书 §6 相冲：查询失败被当成空图。待补索引或改按 VID 查。未建单。`SEL-FIX` 修完后若不同时处理，选中点仍会空 |
| 搜索精确匹配 | 需规序号 20：模糊匹配和精确匹配 | 只有 `CONTAINS`（包含匹配），没有精确匹配开关 | 记偏离。范围解释转登记（见产品会签）。未建单 |

## 7. 现状（截至 2026-11-05）

- 图上已有技术点等点（L01 方案口径约 19,430 个技术点）。尚无 `tech_rel`、`tech_has_*`、`tech_path_step` 边。
- `SYSINT-TECHGRAPH-02-L01` 进行中。`L02`（边、路径、关联实体）backlog。
- 选中节点后，读图按属性 `WHERE` 报 `IndexNotFound`（查询缺口）。2026-11-06 `07ffa9f` 改为当空，未补索引。
- 前端无边时用网格布局画技术点（`b603e63`）。
- 镜像发布、K8s rollout、线上请求均未核（各实现 handoff 原文）。

## 8. 边界

- 只读 `demo_gkx_chain`。不改去 `gkx_chain`、`entan`。
- 技术点不并进七要素「技术」，不改 M01–M24。
- 本二级不写点、不写边、不挂产业。
- `currentYear` 前端固定发 `null`。Java 只回写时间轴游标，不换图。
- `USE_MOCK=true` 仍走冻结种子，仅供开关打开时用。
