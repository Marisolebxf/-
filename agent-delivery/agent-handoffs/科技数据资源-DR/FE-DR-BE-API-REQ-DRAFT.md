# 科技数据资源 · 后台接口需求草稿（前端视角）

> 状态：**DRAFT** · 2026-11-11  
> 分工边界：只写**前端消费的后台 HTTP 接口**（路径 / 信封 / `data` 键形）。不写供方 EXT-B3-RESOURCE、不写 gapfill DDL、不写久新直查方案。  
> 整理依据（现仓实现）：  
> - `lumen-ui-science-pc/src/types/dataResources.ts`（四 Dataset 根键真源）  
> - `src/api/dataResources.ts`（四条 defineApi；**当前 real() 仍回种子，未走网关**）  
> - `src/mock/modules/dataResources.ts` + `dataResourcesSeed.ts`（拼包与嵌套形）  
> - `src/views/data-resources/{overview,access,theme,application}/`（页面实际读键）  
> 已有对照：`BE-DR-CONTRACT-01`（已 done，冻四个 GET）；方案 `方案-科技数据资源-后台接口.md`；实现叶 `DR-RES-C1～C4`（integration）。  
> 任务：`FE-DR-BE-API-REQ-L01`（本草稿）· `BE-DR-FE-API-ALIGN-L01`（Java 对照差异）。  
> 监管人（两叶）：**human:淮政玮**。派单说明：`派单说明-DR-FE-BE-API-REQ.md`（同夹）。

---

## 1. 结论（给后端的最小集合）

前端四页**各只要 1 个无参 GET**，一次拉整包 Dataset；筛选 / 导出 / 分页在浏览器做。不要再拆 `/sources`、`/themes`、`/usage` 等资源路径。

| # | 方法 | 网关路径（浏览器） | 展示服务映射 | 响应 `data` 类型 | 页面 |
|---|---|---|---|---|---|
| 1 | GET | `{VITE_APP_BASE_API}/display/v1/data-ops/overview/dataset` | `/v1/data-ops/overview/dataset` | `DataResourcesOverviewDataset` | 总体视窗 |
| 2 | GET | `.../access/dataset` | `/v1/data-ops/access/dataset` | `DataResourcesAccessDataset` | 接入视窗 |
| 3 | GET | `.../theme/dataset` | `/v1/data-ops/theme/dataset` | `DataResourcesThemeDataset` | 主题视窗 |
| 4 | GET | `.../application/dataset` | `/v1/data-ops/application/dataset` | `DataResourcesApplicationDataset` | 应用视窗 |

- Query / Path 参数：**无**。  
- 信封：`{ "code": 0, "msg": "ok", "data": {…} }`；`code===0` 时前端才用 `data`（与仓内 `request.ts` 一致）。空库仍 `code=0`，数组 `[]`、数字 `0`、对象键保留。不要用 404 表示没数。  
- 键名以 `src/types/dataResources.ts` 为准；**缺根键会空图/空表**。允许多出 `origin`、`entityStock`（仅 overview）、`columnCatalog`（仅 theme）；**禁止少键、改键名**。  
- 应用页「实时监控」**不另开接口**，用本包 `usageCallTrend` 在浏览器跳动。  
- 主题页四张卡涨跌写在 `theme/index.vue`，接口只给四个计数字段（见 §4）。

---

## 2. 与现前端接线状态（事实）

| 项 | 现状 |
|---|---|
| `src/api/dataResources.ts` | 四条 `real()` **固定** `create*Dataset()`，注释写明「接线已撤回」；**不请求网关** |
| 页面 `index.vue` | 多数仍直接 `create*Dataset()` 初值；联调态以种子为准 |
| `BE-DR-CONTRACT-01` / C1～C4 | 契约与 Java 叶已按四 GET 推进；与前端「未接网关」并存 |
| 本草稿用途 | 把前端**已经按类型消费的键**收成接口需求，供后端对齐 / 差异核对，**不替代**已签收契约全文 |

前端正式改走 `request()` 仍属 `DR-RES-D1-L01`（或后续接线叶），本草稿不改代码。

---

## 3. 总体视窗 · `data` 根键（必有）

来源：`DataResourcesOverviewDataset` + overview 页/组件读用。

| 根键 | 前端用途摘要 | 元素/嵌套要点（前端最小） |
|---|---|---|
| `overviewKPIs` | KPI 卡 | `label/value/unit`；`key=total`（资源总量）、`key=theme`（主题库数量）须保留 |
| `resourceTypeDistribution` | 类型分布图 | `name,value`；可选 `color` |
| `resourceThemeDistribution` | 主题分布图 | `name,value,avgQuality` |
| `resourceSourceDistribution` | 来源柱/饼 | `name,value,trend,change` |
| `overviewAnnualAccessTrend` | 年度接入趋势 | `year,total,added,yoy`（`yoy` 可为 `null`） |
| `overviewSourceActivity` | 来源活跃度 | `name,accessCount,activity,status` |
| `overviewSourceAnalysis` | 来源分析详情块 | 须含 `classifyStats`、`sourceTypes`、`structureTrend`、`structureCompare`、`details`（形见种子/契约） |
| `resourceAccessDetailList` | 接入资源详情表 | 行：`id,name,type,…,quality,keywords[]` 等 |
| `semanticThemeAggregation` | 语义聚合块 | `clusters[]`、`fusionTrends[]` |
| `knowledgeGraphData` | 关联图 | `nodes[]`：`id,name,category,size`；`links[]`：`source,target,relation` |
| `knowledgeGraphCategories` | 图例 | `key,name,color` |
| `knowledgeGraphNodeDetails` | 节点详情 | `Record<id,{name,category,desc,…}>` |
| `interfaceStatusMetrics` | 接口状态条 | `label,value,status` |
| `resourceUsageStats` | 应用状态监控 | **仅** `avgResponseTime,alarmCount,alarmCritical,successRate`（不要依赖种子多出的 `totalCalls`） |
| `resourceAppSubjects` | 应用主体列表 | 列表行字段同种子 |
| `cumulativeCallAnalysis` | 累计调用趋势 | 同种子结构 |
| `bigDataCenterStats` | 大数据中心详情 | `overview/categories/resources/growthTrend/updateFeed` 等 |

可选附加（页面可不读）：`entityStock` + `origin`。**禁止**把实体存量写进 `overviewKPIs` 资源总量。

---

## 4. 接入视窗 · `data` 根键（必有）

| 根键 | 前端用途摘要 |
|---|---|
| `accessKPIs` | 接入 KPI |
| `resourceAccessTrend` | 接入趋势（含 months/datasets 等种子形） |
| `accessCompletionData` | 完成度（按接入方式） |
| `accessSourceAnalysis` | 来源渠道分析 + details |
| `problemResources` | 问题资源列表 |
| `problemResourceStats` | 问题统计图 |
| `partitionData` | 分区说明块 |
| `themeDatabases` | 主题库列表（与主题页同形，接入页复用） |
| `historyAccessRecords` | 历史归集记录 |
| `historyAccessDashboard` | 历史仪表盘汇总 |
| `updateCycleStats` | 更新周期统计 |

嵌套字段以 `dataResourcesSeed` 导出对象为准；契约已细表的以 `BE-DR-CONTRACT-01` 为准，冲突时**类型 interface 优先**。

---

## 5. 主题视窗 · `data` 根键（必有）

| 根键 | 前端用途摘要 |
|---|---|
| `themeDatabaseCount` | 顶部卡：主题库数 |
| `tableCount` | 顶部卡：表数 |
| `recordCountLabel` | 顶部卡：记录量（**纯数字字符串**，单位在页面） |
| `storageLabel` | 顶部卡：存储量（同上） |
| `themeDatabases` | 分类浏览/筛选/详情；含 `tableSchemas`（表字段） |
| `datasetRelationData` | 关联关系图（`links` 可含 `strength`） |

可选附加：`columnCatalog`（`origin=snap`）。**禁止**并入 `tableSchemas`。

涨跌文案：页面本地，**非**接口字段。

---

## 6. 应用视窗 · `data` 根键（必有）

| 根键 | 前端用途摘要 |
|---|---|
| `applicationKPIs` | KPI |
| `usageCallTrend` | 调用趋势 + 实时监控基线（`dates/calls/users`） |
| `assetRanking` | 资产排行 |
| `supplierStats` / `supplierRegionGroups` / `supplierCallDetails` / `supplierCallPeriods` | 供应方 |
| `demanderStats` | 需求方 |
| `businessApplicationStats` / `businessApplicationDeptGroups` / `businessApplicationCallLogs` | 业务应用 |
| `dataUsageDetails` | 字段使用详情 |
| `usageDetailTrend` | 使用详情趋势 |
| `themeCallTrend` / `themeCallBasicInfo` | 主题被调用 |
| `supplierCallTrend` / `demanderCallTrend` / `businessCallTrend` | 各方调用趋势 |
| `callUserTracking` | 用户与系统追踪 |

---

## 7. 前端明确不要求后台提供的能力

| 项 | 说明 |
|---|---|
| 带筛选的列表 API | 现行整包下发，浏览器筛 |
| 导出专用 API | Export 组件出浏览器侧数据 |
| 实时监控独立流/WS | 用 `usageCallTrend` 本地跳动 |
| 主题卡涨跌字段 | 写死在 `theme/index.vue` |
| 七要素 / Nebula 图接口 | 本模块目录级图，不验收全图 |
| 对端 R-01～R-24 直出形态 | 前端只吃四个 Dataset；供方包由数据/总集侧另表 |

---

## 8. 建议后端联调验收（前端侧）

1. 四路径各返回信封 `code=0`，`data` 根键与上表一致（可用种子对照）。  
2. `USE_MOCK=false` 且 api 改 `request()` 后，四页图/表有数；缺键或非 0 走现有失败提示。  
3. 若带 `origin=mock`，接线叶挂 MockBadge（`DR-RES-D1`）。  
4. 空库：键在、数组空、数字 0，页面不崩。

---

## 9. 待对齐项（交 `BE-DR-FE-API-ALIGN-L01`）

| # | 问题 | 说明 |
|---|---|---|
| A | 前端未接网关 vs C1～C4 已实现 | 接线责任仍在前端叶；本草稿确认**键集合未再扩** |
| B | 种子多键 vs 类型少键 | 如 `resourceUsageStats.totalCalls`：HTTP **不要多**；以类型为准 |
| C | 嵌套块细字段 | overviewSourceAnalysis / bigDataCenterStats / themeDatabases.tableSchemas 等以契约细表 + 种子为准，对齐时出差异表 |
| D | `origin` / MockBadge | 契约允许多出；组件读 `origin` 等接线叶 |

---

## 10. 修订

| 日期 | 说明 |
|---|---|
| 2026-11-11 | 首版草稿：按现仓 types + 四页消费 + api 现状整理四个 GET 的前端侧后台接口需求 |
