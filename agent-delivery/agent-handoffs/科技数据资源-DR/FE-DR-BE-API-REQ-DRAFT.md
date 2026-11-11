# 科技数据资源 · 后台接口需求（前端视角 · 可审）

> 状态：**READY_FOR_SIGN**（frontend-agent 2026-11-11 按现仓复核；待 **human:淮政玮** 审）  
> 任务：`FE-DR-BE-API-REQ-L01`  
> 分工：只写**前端 → 聚合服务（Java BFF）**要消费的 HTTP（路径 / 信封 / `data` 根键与页面用途）。  
> **不写**：供方 EXT-B3 / R-01～R-24 明细、科学数据中心上游表、gapfill DDL、久新直查方案、业务仓接线代码。  
> 不替代：`BE-DR-CONTRACT-01` 冻结正文（契约仍为 Java 实现真源；本草稿供叶 2 差异核对）。  
> 派单合册：`派单说明-DR-FE-BE-API-REQ.md`。监管人：**human:淮政玮**。  
> ponytail: **off**（definition）

## 整理依据（前端真源，已核对）

| 来源 | 路径 | 用途 |
|---|---|---|
| 四 Dataset 根键 | `lumen-ui-science-pc/src/types/dataResources.ts` | **必有根键真源**；冲突时优先于方案/种子多键 |
| API 现状 | `src/api/dataResources.ts` | 四条 `defineApi`；**`real()` 仍 `create*Dataset()`，未走网关 `request()`** |
| 拼包 | `src/mock/modules/dataResources.ts` | 四 `create*Dataset` 根键与 interface 一一对应 |
| 嵌套形 | `src/mock/modules/dataResourcesSeed.ts` | `typeof import(seed)` 键形；种子可多出类型无的键 |
| 页面读键 | `src/views/data-resources/{overview,access,theme,application}/` | 用途摘要 |
| 契约对照（勿扩写） | `BE-DR-CONTRACT-01.md` | 路径/信封/`origin` 已冻 |
| 方案对照（勿扩写） | `方案-科技数据资源-后台接口.md` §5 | 四 GET 边界 |

---

## 1. 结论（给聚合服务的最小集合）

前端四页**各只要 1 个无参 GET**，一次拉整包 Dataset；筛选 / 导出 / 分页在浏览器做。不要再拆 `/sources`、`/themes`、`/usage` 等资源路径。前端**不直连**科学数据中心。

| # | 方法 | 网关路径（浏览器） | 展示服务映射 | 响应 `data` 类型 | 页面 |
|---|---|---|---|---|---|
| 1 | GET | `{VITE_APP_BASE_API}/display/v1/data-ops/overview/dataset` | `/v1/data-ops/overview/dataset` | `DataResourcesOverviewDataset` | 总体视窗 |
| 2 | GET | `.../access/dataset` | `/v1/data-ops/access/dataset` | `DataResourcesAccessDataset` | 接入视窗 |
| 3 | GET | `.../theme/dataset` | `/v1/data-ops/theme/dataset` | `DataResourcesThemeDataset` | 主题视窗 |
| 4 | GET | `.../application/dataset` | `/v1/data-ops/application/dataset` | `DataResourcesApplicationDataset` | 应用视窗 |

### 信封与空库

- Query / Path 参数：**无**。
- 信封：`{ "code": 0, "msg": "ok", "data": {…} }`。仅当 `code === 0` 时前端才用 `data`（与仓内 `request.ts` / `ResultEnum.SUCCESS` 一致）。
- 空库仍 HTTP 200 + `code=0`：数组 `[]`、数字 `0`、字符串 `""`（例外见主题 `recordCountLabel` / `storageLabel` 空库为 `"0"`）、对象**键保留**。不要用 404 表示没数。
- 键名以 `types/dataResources.ts` 为准：**禁止少根键、改键名**。允许多出 `origin`、`entityStock`（仅 overview）、`columnCatalog`（仅 theme）。缺根键 → 空图/空表。
- 嵌套：`typeof` 自种子的块以种子对象键为准；契约已细表处以 `BE-DR-CONTRACT-01` 为准；**冲突时 interface / 类型优先**。

### 行为边界（前端侧）

- 应用页「实时监控」**不另开接口 / WS**，用本包 `usageCallTrend` 在浏览器跳动。
- 主题页四张卡**涨跌**写在 `theme/index.vue`（本地 `trend`/`change`），接口只给四个计数字段（§4）。

---

## 2. 与现前端接线状态（事实 · 2026-11-11 复核）

| 项 | 现状 |
|---|---|
| `src/api/dataResources.ts` | 四条 `real()` **固定** `create*Dataset()`；文件头注释「接线已撤回」；**不请求网关、不拆 PigX 信封** |
| 四页 `index.vue` | 初值均为 `create*Dataset()`；图/表读 Dataset 根键（见下表） |
| `DR-RES-D1-L01` | 接线叶曾规划改 `request()` + MockBadge；**当前仓内 api 仍为种子返回**（与 D1 handoff 叙述可能不同步，属叶 2/接线核对项） |
| `BE-DR-CONTRACT-01` / C1～C4 | 契约与 Java 按四 GET 推进；与前端「未接网关」**并存** |
| 本草稿 | 把前端**已按类型消费的键**收成接口需求；**不改** api/views；正式接线仍属 `DR-RES-D1` 或后续叶 |

---

## 3. 总体视窗 · `GET .../overview/dataset`

`DataResourcesOverviewDataset` **必有根键 17**：

| 根键 | 页面用途 | 嵌套/元素要点（前端最小） |
|---|---|---|
| `overviewKPIs` | KPI 卡 | `label/value/unit`；须保留 `key=total`（资源总量）、`key=theme`（主题库数量）；可选 `trend`/`change`/`origin` |
| `resourceTypeDistribution` | 类型分布图 | `name,value`；可选 `color` |
| `resourceThemeDistribution` | 主题分布图 | `name,value,avgQuality` |
| `resourceSourceDistribution` | 来源柱/饼 + 下钻 | `name,value,trend,change` |
| `overviewAnnualAccessTrend` | 年度接入趋势 | `year,total,added,yoy`（`yoy` 可为 `null`；无年行时勿造占位年） |
| `overviewSourceActivity` | 来源活跃度 | `name,accessCount,activity,status` |
| `overviewSourceAnalysis` | 来源分析详情 | 须含种子形：`classifyStats`、`sourceTypes`、`structureTrend`、`structureCompare`、`details` |
| `resourceAccessDetailList` | 接入资源详情表 | 行字段同种子（`id,name,type,…,quality,keywords[]` 等） |
| `semanticThemeAggregation` | 语义聚合 | `clusters[]`、`fusionTrends[]`（种子形） |
| `knowledgeGraphData` | 关联图 | `nodes[]`：`id,name,category,size`；`links[]`：`source,target,relation` |
| `knowledgeGraphCategories` | 图例 | `key,name,color` |
| `knowledgeGraphNodeDetails` | 节点详情抽屉 | `Record<id,{name,category,desc,…}>`；**不要**依赖种子多出的 `parentDB` |
| `interfaceStatusMetrics` | 接口状态条 | `label,value,status` |
| `resourceUsageStats` | 应用状态监控 | **仅** `avgResponseTime,alarmCount,alarmCritical,successRate`（**不要** HTTP 出站种子多键 `totalCalls`） |
| `resourceAppSubjects` | 应用主体列表 | 行字段同种子；页面汇总 `callCount` 等自列表算 |
| `cumulativeCallAnalysis` | 累计调用趋势 | 同种子结构 |
| `bigDataCenterStats` | 大数据中心详情 | 种子形：`overview/categories/resources/growthTrend/updateFeed` 等 |

可选附加（页面可不读）：根上 `entityStock` + 各块 `origin`。**禁止**把实体存量写进 `overviewKPIs` 资源总量。

---

## 4. 接入视窗 · `GET .../access/dataset`

`DataResourcesAccessDataset` **必有根键 11**：

| 根键 | 页面用途 |
|---|---|
| `accessKPIs` | 接入 KPI 行 |
| `resourceAccessTrend` | 接入趋势图（种子形含 `months` / `datasets` 等粒度副本） |
| `accessCompletionData` | 完成度块（`completed` / `inProgress` / `pending` 等） |
| `accessSourceAnalysis` | 来源渠道分析 + `details` |
| `problemResources` | 问题资源列表（筛选/导出） |
| `problemResourceStats` | 问题统计图（`byType` / `byChannel` / `monthlyTrend` 等） |
| `partitionData` | 分区说明块 |
| `themeDatabases` | 主题库列表（与主题页同形，接入页复用） |
| `historyAccessRecords` | 历史归集记录 |
| `historyAccessDashboard` | 历史仪表盘汇总 |
| `updateCycleStats` | 更新周期统计 |

嵌套以种子 + 契约细表为准；冲突时 **interface 优先**。

---

## 5. 主题视窗 · `GET .../theme/dataset`

`DataResourcesThemeDataset` **必有根键 6**：

| 根键 | 页面用途 |
|---|---|
| `themeDatabaseCount` | 顶部卡：主题库数（`number`） |
| `tableCount` | 顶部卡：表数（`number`） |
| `recordCountLabel` | 顶部卡：记录量（**纯数字字符串**，单位「亿条」在页面） |
| `storageLabel` | 顶部卡：存储量（**纯数字字符串**，单位「TB」在页面） |
| `themeDatabases` | 分类浏览 / 筛选 / 详情；含 `tableSchemas`（表字段） |
| `datasetRelationData` | 关联关系图（`links` 可含 `strength`） |

可选附加：`columnCatalog`（`origin=snap`）。**禁止**并入 `tableSchemas`。  
涨跌文案：页面本地硬编码，**非**接口字段。

---

## 6. 应用视窗 · `GET .../application/dataset`

`DataResourcesApplicationDataset` **必有根键 19**：

| 根键 | 页面用途 |
|---|---|
| `applicationKPIs` | KPI 行 |
| `usageCallTrend` | 调用趋势 + 实时监控基线（`dates` / `calls` / `users`） |
| `assetRanking` | 资产排行（总览 Tab + 主题调用 Tab） |
| `supplierStats` | 供应方汇总（含行内 `totalCalls` 等——**此为类型/种子必有字段，与 §3 `resourceUsageStats.totalCalls` 不同**） |
| `supplierRegionGroups` | 供应方区域分组 |
| `supplierCallDetails` | 供应方调用明细 |
| `supplierCallPeriods` | 供应方周期筛选项 |
| `demanderStats` | 需求方统计 |
| `businessApplicationStats` | 业务应用统计 |
| `businessApplicationDeptGroups` | 业务应用部门分组 |
| `businessApplicationCallLogs` | 业务应用调用日志 |
| `dataUsageDetails` | 字段使用详情 |
| `usageDetailTrend` | 使用详情趋势 |
| `themeCallTrend` | 主题被调用趋势 |
| `themeCallBasicInfo` | 主题调用基本信息 |
| `supplierCallTrend` | 供应方调用趋势 |
| `demanderCallTrend` | 需求方调用趋势 |
| `businessCallTrend` | 业务应用调用趋势 |
| `callUserTracking` | 用户与系统追踪 |

---

## 7. 前端明确不要求后台提供的能力

| 项 | 说明 |
|---|---|
| 带筛选 / 分页的列表 API | 现行整包下发，浏览器筛 |
| 导出专用 API | Export 组件出浏览器侧数据 |
| 实时监控独立流 / WebSocket | 用 `usageCallTrend` 本地跳动 |
| 主题卡涨跌字段 | 写死在 `theme/index.vue` |
| 前端直连科学数据中心 | 只吃聚合四 GET |
| 七要素 / Nebula 全图接口 | 本模块目录级图（overview KG / theme relation），不验收全图 |
| 对端 R-01～R-24 直出形态 | 前端只吃四个 Dataset；供方/上游由叶 2 / 总集另表 |
| HTTP 出站种子多键 | 见 §9：`resourceUsageStats.totalCalls`、`knowledgeGraphNodeDetails.*.parentDB` |

---

## 8. 建议后端联调验收（前端侧 · 接线后）

1. 四路径各返回信封 `code=0`，`data` 根键与上表一致（可用 `create*Dataset()` 对照根键集合）。  
2. `USE_MOCK=false` 且 api 改 `request()` 后，四页图/表有数；缺键或非 0 走现有失败提示。  
3. 若带 `origin=mock`，接线叶挂 MockBadge（`DR-RES-D1`）。  
4. 空库：键在、数组空、数字 0 / 标签 `"0"`，页面不崩。

---

## 9. 待对齐项（交 `BE-DR-FE-API-ALIGN-L01`）

| # | 问题 | 说明 | 建议处置 |
|---|---|---|---|
| A | 前端未接网关 vs C1～C4 已实现 | 当前 `real()` 回种子；正式接线仍在前端叶 | 叶 2 记差异；不扩对外四 GET |
| B | 种子多键 vs 类型少键 | `resourceUsageStats.totalCalls`；`knowledgeGraphNodeDetails.*.parentDB` | HTTP **不要多**；以类型为准（契约已写） |
| C | 易混淆的 `totalCalls` | 应用页 `supplierStats` / 区域组 / 明细行的 `totalCalls` **要有**；仅 overview 监控块禁止种子多键 | 叶 2 差异表须分开写 |
| D | 嵌套块细字段 | `overviewSourceAnalysis` / `bigDataCenterStats` / `themeDatabases.tableSchemas` / `resourceAccessTrend` 等 | 以契约细表 + 种子为准出差异表 |
| E | `origin` / `entityStock` / `columnCatalog` | 契约允许多出；现组件基本不读；MockBadge 属接线叶 | 聚合可返回；勿冒进 KPI |
| F | 契约文「裸 fetch」vs 现仓「回种子」 | `BE-DR-CONTRACT-01` §现有 real() 叙述与现 `dataResources.ts` 不完全一致 | 叶 2 注明事实源=现仓代码；契约叙述可另开修订（本叶不改契约） |
| G | 聚合 → 科学数据中心 | 本草稿**不列**上游接口 | 叶 2 主交付 `BE-DR-SDC-UPSTREAM-API-REQ.md` |

---

## 10. 根键清单速查（与 interface 对齐）

| Dataset | 必有根键数 | 列表 |
|---|---|---|
| overview | 17 | 见 §3 |
| access | 11 | 见 §4 |
| theme | 6 | 见 §5 |
| application | 19 | 见 §6 |

---

## 11. 修订

| 日期 | 说明 |
|---|---|
| 2026-11-11 | 首版草稿：按 types + 四页消费 + api 现状整理四个 GET |
| 2026-11-11 | **FE-DR-BE-API-REQ-L01 审定**：升 READY_FOR_SIGN；补根键计数、接线撤回事实、`totalCalls` 易混淆项、不直连科学数据中心、待对齐 A–G |
