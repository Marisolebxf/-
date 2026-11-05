# TS-L2-DS02-TEST-L01 · 科学技术全景 · 三个功能主路径

- 任务：`TS-L2-DS02-TEST-L01`
- 日期：2026-11-05
- 执行：`agent:qa-agent`；监管：`human:淮政玮`
- 页面：`/trend/tech-panorama`（`lumen-ui-science-pc` `src/views/situation/panorama/`）
- 设计：`agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/科学技术全景-系统详细设计说明书.md`（序号 17–33）
- 实现（本地 `dev` 已含这些 commit，本轮未改业务仓）：
  - 前端 `e6fb1dd`（HEAD `05863d0` 的祖先；全景相关文件此后无新提交）
  - Java `cbd6f10`（`gkxlumen-display` `POST /v1/situation/panorama/graph`）
  - Python 读图 `a03c52b`（`POST /internal/tech-graph/read`）
  - 灌数 `828315a`（`demo_gkxlumenx_ads.ads_technology_panorama_score`：centrality 19430，influence 252363，path_priority 0；图上没有 `tech_path_step`）
- 强度：ponytail full
- 已发布镜像：本轮未核，未打公开接口，无 HTTP 状态码。下列「镜像」列一律未测。

本地可复核：在 `lumen-ui-science-pc` 执行 `node src/lib/graph/liveGraph.selfcheck.mjs`。本轮输出 `liveGraph.selfcheck ok`，退出码 0。

## TC-01 打开

| 项 | 内容 |
|---|---|
| 前置 | `USE_MOCK=false`。菜单「科学技术全景」。 |
| 步骤 | 打开 `/trend/tech-panorama`。 |
| 预期 | 只请求一次 `POST /display/v1/situation/panorama/graph`。空图为 `emptyReason=GRAPH_EMPTY`，画布不补种子节点。 |
| 实际结果 | **本地通过（走查 + 自检）**。`src/api/situation/panorama.ts` 的 `fetchPanoramaGraph` 只 `post` 这一条 `graph`，再 `coerceLiveGraph`。`index.vue` 的 `loadPanoramaGraph` 在非 Mock 时用 `graphReadParams`。自检断言空图收成 `GRAPH_EMPTY`，且不出现 `id=robot`。**镜像未测。** |

## TC-02 搜索

| 项 | 内容 |
|---|---|
| 前置 | 同 TC-01。 |
| 步骤 | 在全景搜索框输入关键词，等防抖后看画布。 |
| 预期 | 同一次 `graph` 带上搜索字。命中节点留下；没有命中则空，不造点。 |
| 实际结果 | **本地通过（自检 + 走查）**。`graphReadParams` 会 trim 关键词（自检：` 量子 ` → `量子`）。`index.vue` 把 `debouncedKeyword` 放进同一次加载，并用 `filterGraphNodesAndRelations` 做页内过滤。浏览器里的高亮与居中**镜像未测**。 |

## TC-03 点技术点，看实体

| 项 | 内容 |
|---|---|
| 前置 | 同 TC-01。图上已有技术点时才有可点节点；空图则实体区为空。 |
| 步骤 | 点一个技术点，看关联实体与详情。 |
| 预期 | 换点后再次 `graph` 带 `selectedNodeId`。实体只保留人、机构、论文、专利。没有的字段空着。 |
| 实际结果 | **本地通过（自检 + 走查）**。选中点变化会重新 `loadPanoramaGraph`。`entityRowsFor` 在自检里只留下「一篇论文」，丢掉项目和实体—实体边。`USE_MOCK=false` 时详情只用节点上已有属性（`buildGraphNodeDetail`）。点击与抽屉**镜像未测**。 |

## TC-04 看路径

| 项 | 内容 |
|---|---|
| 前置 | 灌数事实：`path_priority` 0 行；图上没有 `tech_path_step`。 |
| 步骤 | 打开关键路径，看路径优先级。 |
| 预期 | 没有路径步时列表为空。`pathPriority` 无行则为空。空格按通过计。 |
| 实际结果 | **本地通过（自检 + 走查）**。Java `SituationPanoramaService.overlay` 按 `path_priority` 填 `pathPriority`，查不到则为 null。自检：无优先级且重要性档不是「全部」时，该路径视图为空，文案含「优先级」。**镜像未测。** |

## TC-05 播放

| 项 | 内容 |
|---|---|
| 前置 | 同 TC-04。有路径步才有可播放的阶段。 |
| 步骤 | 进入路径播放，点播放 / 暂停。 |
| 预期 | 按已取回的路径步在页内推进。`currentYear` 只是播放游标，不向服务端要第二套图。没有步时播放区为空，按通过计。 |
| 实际结果 | **本地通过（走查 + 自检）**。`graphReadParams` 固定 `currentYear: null`（自检已断言）。播放计时在 `index.vue` 的 `playbackTimer`，组件是 `KeyPathPlaybackMode.vue`。按钮手感**镜像未测**。 |

## TC-06 序号 17：导入、手工、撤销

| 项 | 内容 |
|---|---|
| 前置 | `USE_MOCK=false`。 |
| 步骤 | 看导入、手动添加、撤销是否写到服务端。 |
| 预期 | 不落库。接口若被调用则 HTTP 501。前端不发写请求，并标明未落库，也算通过。 |
| 实际结果 | **本地通过（走查）**。见下节文件结论。**未对集群调用这些接口，镜像未测。** |

走查：

- `lumen-ui-science-pc/src/api/situation/panorama.ts`：真实请求只有 `POST /display/v1/situation/panorama/graph`。
- `src/views/situation/panorama/index.vue`：`handleGraphImportFile`、`handleManualGraphSubmit`、`undoGraphEdit` 只改 `importedGraphExtras` / `graphEditPast`。非 Mock 提示为「服务端不接收写入（501），未落库。」撤销不发请求。
- `lumen-svc-platform` `SituationPanoramaController`：`POST /v1/situation/panorama/import` 与 `/manual` 调用 `rejected`。`SituationPanoramaService.graph` 见到 `action=import` 等写入动作也返回 501，且不读图。`SituationPanoramaControllerTest.writeAndEntityRelationReturn501WithoutReading` 写了同样断言；本轮未重跑 Maven。

## TC-07 序号 26：实体与实体、多快照

| 项 | 内容 |
|---|---|
| 前置 | `USE_MOCK=false`。 |
| 步骤 | 看实体关联关系区，并切换年份。 |
| 预期 | 实体之间的网为空，或对应接口 501。不按年份再取一套关系。 |
| 实际结果 | **本地通过（走查）**。见下节。**镜像未测。** |

走查：

- `GraphAnalysisPanel.vue`：`live` 时 `entityRelationSnapshot` 固定 `{ nodes: [], links: [], empty: true }`，文案「实体间关系暂无数据」。年份按钮只改 `entityRelationYear`。
- `liveGraph.ts` 的 `graphReadParams` 不把 `currentYear` 发给服务端。`entityRowsFor` 跳过两端都是实体的边。
- `SituationPanoramaController`：`POST /v1/situation/panorama/entity-relations` 返回 501。`graph` 在 `entityRelations=true` 时同样 501，不读图。

## TC-08 `USE_MOCK=false` 不出现种子节点

| 项 | 内容 |
|---|---|
| 前置 | 自检可在前端仓本地跑，不依赖已发布镜像。 |
| 步骤 | `node src/lib/graph/liveGraph.selfcheck.mjs`。 |
| 预期 | 空图不补种子；页面不引用 `mock/modules/panorama`。 |
| 实际结果 | **本地通过。** 2026-11-05 输出 `liveGraph.selfcheck ok`，退出码 0。断言包括：空图 `GRAPH_EMPTY`、无 `robot`、分析上下文无「鹏城实验室」、统计值不是种子里的 `1,148`、`index.vue` 不引用 `mock/modules/panorama`。**镜像未测。** |

## 汇总

| 编号 | 覆盖 | 本地 | 已发布镜像 |
|---|---|---|---|
| TC-01 | 打开 | 走查 + 自检通过 | 未测 |
| TC-02 | 搜索 | 自检 + 走查通过 | 未测 |
| TC-03 | 点技术点、看实体 | 自检 + 走查通过 | 未测 |
| TC-04 | 看路径（优先级空格按通过） | 自检 + 走查通过 | 未测 |
| TC-05 | 播放 | 走查 + 自检通过 | 未测 |
| TC-06 | 序号 17 导入 / 手工 / 撤销 | 走查通过 | 未测 |
| TC-07 | 序号 26 实体网 / 多快照 | 走查通过 | 未测 |
| TC-08 | 关掉 Mock 后无种子节点 | 自检通过 | 未测 |
