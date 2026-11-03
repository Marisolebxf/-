# BE-DR-CONTRACT-01 · 科技数据资源四视窗 HTTP 契约

ponytail: off

冻结四个 GET 的路径、PigX 信封、`data` 键名和 `origin`。类型以 `repos/lumen-ui-science-pc/src/types/dataResources.ts` 为准。`typeof import('@/mock/modules/dataResourcesSeed')` 的键以种子对象的键为准（四个 `create*Dataset` 只是按这些键拼包）。不写 Java，不改前端。

## 任务认领

| 字段 | 值 |
|---|---|
| task-id | `BE-DR-CONTRACT-01` |
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`（长任务总控 2026-11-03：后续认领不必再问） |
| 状态 | 开工时已是 `in_progress`。本叶不改登记表，不标 `done` |
| 仓 | `gkx-orchestration`（只新增本 handoff） |

| 字段 | 值 |
|---|---|
| ponytail | `off` |
| 说明 | 派单强度为契约全文，不缩键、不省略嵌套。未用 YAGNI 跳过调用链、信封或 D18 的「接口不内嵌 mock」 |

## 范围

本文件是 `DR-RES-C1-L01`～`C4-L01` 与 `DR-RES-D1-L01` 的 HTTP 真源。输入是方案第 5 节，键名冲突时以类型为准。

做：

- 四个无查询参数的 GET，以及网关路径与展示服务映射。
- HTTP 体 `{ code, msg, data }`。`code === 0` 时 `data` 才是数据集。
- 四个 `data` 的键，含嵌套。允许比类型多 `origin`、`entityStock`、`columnCatalog`。
- `origin` 只取 `jiuxin`、`snap`、`mock`。实体存量只放 `entityStock`。列目录只放 `columnCatalog`。

不做：

- 不写 Java、Python、DDL、灌数，不改 `lumen-ui-science-pc`。
- 不改方案、WBS、`DR-RES-长任务总控.md`、`task-registry.yaml`、`DR-RES-A0` 产物。
- 不定义 `/sources`、`/themes`、`/usage` 或其他 `/display/v1/data-ops/**`。
- 不把 `entityStock` / `columnCatalog` 的内部列名写死。那是 `DR-RES-A0-L01` 的矩阵。本契约只冻它们的位置和 `origin`。

页面：总体视窗、接入视窗、主题视窗、应用视窗。筛选、导出、分页都在浏览器里对整包做。

## 调用与信封

浏览器经 axios `baseURL`（`src/constants/index.ts` 的 `BASE_URL = import.meta.env.VITE_APP_BASE_API`）请求：

| 方法与网关路径 | `data` 类型 | 展示服务映射 | 页面 |
|---|---|---|---|
| `GET {VITE_APP_BASE_API}/display/v1/data-ops/overview/dataset` | `DataResourcesOverviewDataset` | `GET /v1/data-ops/overview/dataset` | 总体视窗 |
| `GET {VITE_APP_BASE_API}/display/v1/data-ops/access/dataset` | `DataResourcesAccessDataset` | `GET /v1/data-ops/access/dataset` | 接入视窗 |
| `GET {VITE_APP_BASE_API}/display/v1/data-ops/theme/dataset` | `DataResourcesThemeDataset` | `GET /v1/data-ops/theme/dataset` | 主题视窗 |
| `GET {VITE_APP_BASE_API}/display/v1/data-ops/application/dataset` | `DataResourcesApplicationDataset` | `GET /v1/data-ops/application/dataset` | 应用视窗 |

无 path 参数，无 query。成功体：

```json
{ "code": 0, "msg": "ok", "data": { } }
```

| 字段 | 规则 |
|---|---|
| `code` | 成功为数字 `0`，等于 `ResultEnum.SUCCESS`。`src/utils/request.ts` 在 `code === 0` 时把 `data` 交给调用方 |
| `msg` | 字符串。成功示例 `ok` |
| `data` | 上表类型的对象，不是再包一层 |

空库也是 HTTP 200 且 `code = 0`。不用 404 表示没数。此时：

- 四个 `data` 的根键都在，包括允许多出的 `entityStock`、`columnCatalog`。
- 数组为 `[]`。
- 数字为 `0`。`yoy` 的类型是 `number | null`，没有年行时不要造占位年；有年行时第一年的 `yoy` 为 `null`。
- 字符串为 `""`。例外：`recordCountLabel`、`storageLabel` 为纯数字字符串，空库为 `"0"`。单位「亿条」「TB」在页面上，不进这两个字段。
- 对象键仍在。中文序列键（见各表）空库时键还在，值是 `[]` 或 `0`。
- 类型上标了 `?` 的键可以不出现。没有 `?` 的键不能省。

`code !== 0` 走现有请求失败提示。本契约不另定错误码表。

`request()` 成功后可能在内存对象上挂不可枚举的 `__traceId`。那不是 HTTP 字段，响应体不要写 `__traceId`。

## origin、entityStock、columnCatalog

`origin` 取值只有 `jiuxin` | `snap` | `mock`。

| 放在哪 | 取值 |
|---|---|
| KPI 元素上 | `mock` |
| 对象数组的每个元素（列表行、图点、图边）上 | `mock` |
| 根上类型为对象的统计块，写在该对象根上 | `mock` |
| 行内再嵌套的子对象（如 `tableSchemas`、`typeDist`、`series`） | 不再加一层 `origin` |
| `entityStock` | `jiuxin`（直查久新）或 `snap`（读 `snap_` 批次） |
| `columnCatalog` | `snap`（方案 5.3：直读 `SHOW COLUMNS` 与 `snap_` 批次都写 `snap`） |

实体存量（论文 / 专利 / 项目条数，按年的序列）只出现在总体视窗的 `entityStock` 内。不得写入 `overviewKPIs` 的「资源总量」、`overviewAnnualAccessTrend`，也不得参与另外三页的 KPI。

列目录只出现在主题视窗的 `columnCatalog` 内。不得写入 `themeDatabases[].tableSchemas`。

这两个对象内部可以再有 `DR-RES-A0-L01` 矩阵定的子键。那些子键不得冒到对象外面。本契约不冻结 `years` 等子键名（方案第 2 节点过 `entityStock.years`，类型和第 5 节都没有把它写成必填键）。两对象至少有 `origin`。

页面上的目录、接入、质量、调用都来自 mock 表，对应块的 `origin` 为 `mock`。现有组件还不读 `origin`。`DR-RES-D1-L01` 才按 `origin=mock` 挂 MockBadge。本契约不改组件。

种子有、类型接口没有、因此响应不写的两处：

- `resourceUsageStats.totalCalls`（页面只读 `avgResponseTime`、`alarmCount`、`alarmCritical`、`successRate`）
- `knowledgeGraphNodeDetails.*` 上的 `parentDB`（详情类型无此键，页面不读）

## 现有 real() 与接线边界

`src/api/dataResources.ts` 四条 `real()` 仍是裸 `fetch('/display/v1/data-ops/.../dataset')`，把整段 JSON 当成数据集。没有加 `{VITE_APP_BASE_API}`，也没有按 `code === 0` 拆 `data`。

本契约不改这四条。`DR-RES-D1-L01` 才改成 `request()`。接线之后路径仍是上面四个 GET。Java 从本契约起就返回信封，不等前端改完。

四个 `create*Dataset` 的根键与四个 interface 一致。Mock 运行时 `resourceUsageStats` 多一个 `totalCalls`，HTTP 不跟着多。

应用页「实时监控」不另开接口，浏览器用本响应的 `usageCallTrend` 按秒跳动。

主题页四张卡的涨跌写在 `theme/index.vue`，接口只给 `themeDatabaseCount`、`tableCount`、`recordCountLabel`、`storageLabel`。

## 字段表约定

- 「必有」：类型无 `?`，对象一旦出现就必须有该键。
- 「可省」：类型有 `?`。
- 数组元素键在元素上。数组本身可以是 `[]`。
- `origin` 不占类型键列，按上一节加。

### 1. `GET .../overview/dataset`

根键（全部必有）：

| 键 | 类型 | 空库 |
|---|---|---|
| `overviewKPIs` | `DrKpiItem[]` | `[]` |
| `resourceTypeDistribution` | `DrDistributionItem[]` | `[]` |
| `resourceThemeDistribution` | `DrThemeDistributionItem[]` | `[]` |
| `resourceSourceDistribution` | `DrSourceDistributionItem[]` | `[]` |
| `interfaceStatusMetrics` | `DrInterfaceStatusMetric[]` | `[]` |
| `knowledgeGraphData` | `DrKnowledgeGraphData` | 对象键在，`nodes`/`links` 为 `[]` |
| `knowledgeGraphNodeDetails` | `Record<string, DrKnowledgeGraphNodeDetail>` | `{}` |
| `knowledgeGraphCategories` | `DrKnowledgeGraphCategory[]` | `[]` |
| `resourceUsageStats` | `DrResourceUsageStats` | 四个数字为 `0` |
| `overviewAnnualAccessTrend` | `DrAnnualAccessTrendItem[]` | `[]` |
| `overviewSourceActivity` | `DrSourceActivityItem[]` | `[]` |
| `overviewSourceAnalysis` | `DrOverviewSourceAnalysis` | 见下，对象键在 |
| `semanticThemeAggregation` | `DrSemanticThemeAggregation` | 见下 |
| `resourceAccessDetailList` | `DrResourceAccessDetail[]` | `[]` |
| `bigDataCenterStats` | `DrBigDataCenterStats` | 见下 |
| `resourceAppSubjects` | `DrResourceAppSubject[]` | `[]` |
| `cumulativeCallAnalysis` | `DrCumulativeCallAnalysis` | 见下 |
| `entityStock` | 类型没有。允许多出 | 至少 `{ "origin": "jiuxin" \| "snap" }` |

`DrKpiItem`：`label` string 必有，`value` string 必有，`unit` string 必有，`trend` `'rise' \| 'fall'` 可省，`change` number 可省，`key` string 可省。总体视窗已有键名必须保留：资源总量的 `key` 为 `total`，主题库数量的 `key` 为 `theme`。资源类型数在种子里没有 `key`，不要新造。

| 数组 | 元素必有 | 元素可省 |
|---|---|---|
| `resourceTypeDistribution` | `name` string，`value` number | `color` string |
| `resourceThemeDistribution` | `name`，`value` number，`avgQuality` number | — |
| `resourceSourceDistribution` | `name`，`value` number，`trend` string，`change` number | — |
| `interfaceStatusMetrics` | `label`，`value` number，`status` string | — |
| `knowledgeGraphCategories` | `key`，`name`，`color` | — |
| `overviewAnnualAccessTrend` | `year` string，`total` number，`added` number，`yoy` number \| null | — |
| `overviewSourceActivity` | `name`，`accessCount` number，`activity` number，`status` | — |

`resourceUsageStats` 只此四键，全是 number：`avgResponseTime`、`alarmCount`、`alarmCritical`、`successRate`。

`knowledgeGraphData`：

| 键 | 元素 |
|---|---|
| `nodes[]` | 必有 `id`、`name`、`category`、`size` number。类型有字符串索引签名，不增加必填键 |
| `links[]` | 必有 `source`、`target`、`relation`。不要求 `strength`（`strength` 只在主题视窗 `datasetRelationData.links`） |

`knowledgeGraphNodeDetails` 的每个值：必有 `name`、`category`、`desc`。可省：`records` string、`quality` number、`source` string、`users` string \| number、`calls` string、`datasets` number、`relatedNodes` string[]。键名 `n1` 这类是数据，不是契约必填键。空库为 `{}`。

`overviewSourceAnalysis`：

| 路径 | 键 |
|---|---|
| `classifyStats` | `totalResources`、`autoTagged`、`manualReview`、`accuracy` number；`lastRun` string |
| `sourceTypes[]` | `key`、`name`、`volume`、`count`、`share`、`change` number；`trend`、`color`、`reliabilityHint` string；`reliability`、`avgQuality` number；`sampleTags` string[] |
| `structureTrend.month` / `.quarter` | `labels` string[]；`series` 必有键 `国内数据库`、`国外数据库`、`科研院所`、`企业`、`开源平台`，值均为 number[] |
| `structureCompare` | `previousPeriod`、`currentPeriod` string；`rows[]` 必有 `name`、`current`、`previous`、`delta` number |
| `details[]` | `id`、`name`、`sourceType`、`provider`、`region`、`dataType`、`collectTime`、`qualityLevel`、`reliabilityLevel`、`field`、`relatedProject` string；`qualityScore`、`reliabilityScore`、`volume` number；`autoTags` string[] |

`semanticThemeAggregation`：

| 路径 | 键 |
|---|---|
| `clusters[]` | `id`、`theme` string；`features` string[]；`cohesion` number；`resourceCount` number；`resources[]`：`id`、`name`、`category` string，`similarity` number |
| `fusionTrends[]` | `id`、`direction`、`insight` string；`themes` string[]；`strength` number；`relatedClusterIds` string[] |

`resourceAccessDetailList[]`：`id`、`name`、`type`、`category`、`source`、`channel`、`collectTime`、`updateFreq`、`lastUpdateTime`、`recordCount`、`size`、`status`、`relatedProject` string；`quality` number；`keywords` string[]。

`bigDataCenterStats`：

| 路径 | 键 |
|---|---|
| `overview` | `totalDatabases`、`totalTables` number；`totalRecords`、`totalStorage` string |
| `categories[]` | `key`、`name`、`description`、`updateStatus` string；`count`、`tables` number；`records` string；`fields`、`techTypes` string[] |
| `resources[]` | `id`、`name`、`categoryKey`、`category`、`dataType`、`field`、`techType`、`updateTime`、`updateFreq`、`schema`、`recordCount`、`size`、`status` string；`quality`、`growth7d`、`activityScore` number；`relatedIds`、`keywords` string[] |
| `growthTrend` | `days` string[]；`series[]`：`name` string，`data` number[] |
| `updateFeed[]` | `id`、`time`、`resource`、`action`、`delta`、`status` string |

`resourceAppSubjects[]`：`id`、`name`、`subjectType`、`resourceType`、`purpose` string；`callCount`、`valueShare` number；`isKeyUser` boolean。

`cumulativeCallAnalysis`：

| 路径 | 键 |
|---|---|
| `summary` | `totalSinceLaunch`、`resourceCovered`、`avgDaily` number；`peakPeriod`、`heatLevel`、`lifecycleHint` string |
| `periods.week` / `.month` / `.quarter` | `labels` string[]；`calls`、`cumulative` number[] |
| `byResourceType[]` | `type`、`heat`、`lifecycle` string；`cumulative`、`share` number |

### 2. `GET .../access/dataset`

根键（全部必有）：

| 键 | 类型 | 空库 |
|---|---|---|
| `accessKPIs` | `DrKpiItem[]` | `[]`。种子三项都没有 `key`，不要新造 |
| `resourceAccessTrend` | `DrResourceAccessTrend` | 对象键在 |
| `accessCompletionData` | `DrAccessCompletionData` | 数字 `0`，`byChannel` 为 `[]` |
| `accessSourceAnalysis` | `DrAccessSourceAnalysis` | 对象键在 |
| `problemResources` | `DrProblemResource[]` | `[]` |
| `problemResourceStats` | `DrProblemResourceStats` | 六个数组为 `[]` |
| `partitionData` | `DrPartitionData` | 三个数组为 `[]` |
| `themeDatabases` | `DrThemeDatabase[]` | `[]`。与主题视窗同一元素形状 |
| `historyAccessRecords` | `DrHistoryAccessRecord[]` | `[]` |
| `historyAccessDashboard` | `DrHistoryAccessDashboard` | 对象键在 |
| `updateCycleStats` | `DrUpdateCycleStat[]` | `[]` |

`resourceAccessTrend` 必有 `month`、`week`、`day`、`months`、`datasets`。`month` / `week` / `day` 各有 `labels` string[] 与 `datasets[]`（`name` string，`data` number[]）。根上的 `months` 是月度标签副本，`datasets` 是月度序列副本，元素同为 `name` + `data`。

`accessCompletionData`：`total`、`completed`、`inProgress`、`pending` number；`byChannel[]`：`channel` string，`completed`、`inProgress`、`pending` number。

`accessSourceAnalysis`：

| 路径 | 键 |
|---|---|
| `channels[]` | `name` string；`volume`、`count`、`share` number；`color` string；`bizTypes` string[] |
| `byTime.month` / `.quarter` | `labels` string[]；`series` 必有键 `科研院所`、`企业`、`第三方平台`，值均为 number[] |
| `byBizType[]` | `name` string；以及 number 键 `科研院所`、`企业`、`第三方平台` |
| `details[]` | `id`、`name`、`channel`、`dataType`、`collectTime`、`qualityLevel`、`relatedProject`、`field` string；`qualityScore`、`volume` number |

`problemResources[]`：`id`、`name`、`tableName`、`type`、`category`、`dataCluster`、`level`、`status`、`time`、`channel`、`detail`、`suggestion` string。

`problemResourceStats`：

| 键 | 元素 |
|---|---|
| `byCategory[]` | `category` string，`count` number，`color` string |
| `byDataCluster[]` | `cluster` string，`count` number |
| `byType[]` | `type` string，`count` number，`color` string |
| `byLevel[]` | `level` string，`count` number，`color` string |
| `byChannel[]` | `channel` string，`count` number |
| `monthlyTrend[]` | `month` string，`total`、`resolved` number |

`partitionData`：

| 键 | 元素必有 |
|---|---|
| `byRegion[]`、`byDatabase[]` | `name` string；`resourceCount` number；`dataVolume` string；`avgQuality` number；`typeDist`；`orgs` string[]；`trend` number[]。无 `topResource` |
| `byInstitution[]` | 同上，另有 `topResource` string |
| `typeDist` | 必有键 `结构化`、`非结构化`、`半结构化`、`实时流`，值均为 number |

`themeDatabases[]`（接入与主题共用）：`id`、`name`、`category`、`resourceType`、`publishTime`、`records`、`size`、`updateTime`、`description`、`source`、`region`、`partition`、`contactPerson`、`collectTime`、`updateFreq`、`dataStructure`、`relatedProject` string；`tags` string[]；`tables`、`quality` number；`tableSchemas[]`。`tableSchemas[]`：`tableName`、`tableComment` string；`columns[]`：`fieldName`、`fieldType`、`meaning` string，`required` boolean。

`historyAccessRecords[]`：`id`、`channelName`、`tableName`、`accessDate`、`size`、`updateCycle`、`updateTime`、`status`、`anomalyType`、`anomalyNote` string；`dataCount` number。

`historyAccessDashboard`：

| 路径 | 键 |
|---|---|
| `summary` | `archiveCount`、`channelCount`、`tableCount`、`anomalyCount` number；`successRate` number |
| `trend` | `labels` string[]；`accessVolume`、`updateSuccessRate`、`anomalyCount` number[] |
| `anomalyByType[]` | `type` string，`count` number，`color` string |
| `updateStatus[]` | `name` string，`value` number，`color` string |

`updateCycleStats[]`：`channel`、`avgCycle` string；`successRate` number；`trend` number[]。

### 3. `GET .../theme/dataset`

根键（全部必有）：

| 键 | 类型 | 空库 |
|---|---|---|
| `themeDatabaseCount` | number | `0` |
| `tableCount` | number | `0` |
| `recordCountLabel` | string | `"0"` |
| `storageLabel` | string | `"0"` |
| `themeDatabases` | `DrThemeDatabase[]` | `[]`。元素同接入视窗 |
| `datasetRelationData` | `DrDatasetRelationData` | `nodes`/`links` 为 `[]` |
| `columnCatalog` | 类型没有。允许多出 | 至少 `{ "origin": "snap" }` |

`datasetRelationData.nodes[]`：`id`、`name`、`category`、`desc` string；`size` number。`links[]`：`source`、`target`、`relation` string；`strength` number。

### 4. `GET .../application/dataset`

根键（全部必有）：

| 键 | 类型 | 空库 |
|---|---|---|
| `applicationKPIs` | `DrKpiItem[]` | `[]`。种子没有 `key`，不要新造 |
| `usageCallTrend` | `DrUsageCallTrend` | `dates`、`calls`、`users` 均为 `[]` |
| `assetRanking` | `DrAssetRankingItem[]` | `[]` |
| `supplierStats` | `DrSupplierStat[]` | `[]` |
| `supplierRegionGroups` | `DrSupplierRegionGroup[]` | `[]` |
| `supplierCallDetails` | `DrSupplierCallDetail[]` | `[]` |
| `supplierCallPeriods` | string[] | `[]` |
| `demanderStats` | `DrDemanderStat[]` | `[]` |
| `businessApplicationStats` | `DrBusinessApplicationStat[]` | `[]` |
| `businessApplicationDeptGroups` | `DrBusinessApplicationDeptGroup[]` | `[]` |
| `businessApplicationCallLogs` | `DrBusinessApplicationCallLog[]` | `[]` |
| `dataUsageDetails` | `DrDataUsageDetail[]` | `[]` |
| `usageDetailTrend` | `DrUsageDetailTrend` | `months`、`calls` 为 `[]` |
| `themeCallTrend` | `DrApplicationMultiLineTrend` | `months` 为 `[]`，`datasets` 为 `[]` |
| `themeCallBasicInfo` | `DrThemeCallBasicInfo[]` | `[]` |
| `supplierCallTrend` | 同上多线趋势 | 同 `themeCallTrend` |
| `demanderCallTrend` | 同上 | 同上 |
| `businessCallTrend` | 同上 | 同上 |
| `callUserTracking` | `DrCallUserTracking[]` | `[]` |

`usageCallTrend`：`dates` string[]，`calls` number[]，`users` number[]。

`usageDetailTrend`：`months` string[]，`calls` number[]。

`themeCallTrend`、`supplierCallTrend`、`demanderCallTrend`、`businessCallTrend`：`months` string[]；`datasets[]`：`name` string，`data` number[]。

| 数组 | 元素必有 |
|---|---|
| `assetRanking` | `id`、`name`、`category`、`department`、`dataType`、`appSubject`、`deployLocation`、`usageCycle`、`businessType`、`usageUnit`、`lastActiveDate` string；`calls`、`users`、`growth` number；`businessModules` string[] |
| `supplierStats` | `id`、`name`、`department`、`region` string；`resourceCount`、`totalCalls`、`share` number |
| `supplierRegionGroups` | `region` string；`supplierCount`、`resourceCount`、`totalCalls` number；`departments[]`：`name` string，`suppliers` string[]，`resourceCount` number |
| `supplierCallDetails` | `id`、`supplierName`、`dataProduct`、`businessType`、`period` string；`totalCalls` number |
| `demanderStats` | `id`、`name`、`department`、`businessType`、`projectTeam` string；`calls`、`activeDays`、`avgDaily` number |
| `businessApplicationStats` | `id`、`name`、`department`、`businessType`、`status` string；`appCount`、`calls` number |
| `businessApplicationDeptGroups` | `department` string；`apps` string[]；`appCount`、`totalCalls` number |
| `businessApplicationCallLogs` | `id`、`appName`、`department`、`businessType`、`userName`、`resource`、`callTime`、`result` string；`durationMs`、`callCount` number |
| `dataUsageDetails` | `id`、`tableName`、`columnName`、`columnType`、`columnDesc`、`sourceDept`、`appName`、`lastUsed` string；`usageCount`、`subscriberCount` number |
| `themeCallBasicInfo` | `theme`、`callTime`、`callFreq`、`callInterface`、`businessSystems` string |
| `callUserTracking` | `userId`、`userName`、`department`、`application`、`theme`、`lastCallTime`、`ipAddress` string；`callCount` number |

## 与方案第 5 节的对照

方案第 5 节已经写明、本契约照单冻结的：

- 只有四个 GET，无查询参数。路径与第 5 节表格一致，并写上 `{VITE_APP_BASE_API}` 与展示服务 `/v1/data-ops/.../dataset`。
- 信封 `{ code: 0, msg, data }`，与 `request.ts` 的 `code === 0` 拆包一致。空库 `code = 0`，数组 `[]`，数字 `0`，键不缺。
- 四个 Dataset 的根键，第 5.1–5.4 都点了名，类型里一个都不少，名字没有改。
- 允许多出的就是 `origin`、`entityStock`、`columnCatalog`。第 5 节有这三处，类型接口没有。
- 不再定义 `/sources`、`/themes`、`/usage`。
- `recordCountLabel`、`storageLabel` 是纯数字字符串。`resourceAccessTrend` 保留 `months`、`datasets`。`usageCallTrend` 含 `dates`、`calls`、`users`。`yoy` 第一年可为 `null`。`overviewSourceAnalysis` 含 `sourceTypes`、`details`、`classifyStats`。`bigDataCenterStats.overview` 在。`themeDatabases[].tableSchemas` 在。

方案第 5 节有、类型没有，按「允许多出」收进响应，不视为类型缺键：`origin`、`entityStock`、`columnCatalog`。

类型顶层没有「方案第 5 节没写到」的键。差集全是嵌套键。下面这些键在 `dataResources.ts`（含种子 `typeof`）里，方案第 5 节正文没有出现：

`accessCount`、`accessDate`、`accessVolume`、`accuracy`、`action`、`activeDays`、`activity`、`activityScore`、`alarmCount`、`alarmCritical`、`anomalyByType`、`anomalyCount`、`anomalyNote`、`anomalyType`、`appCount`、`appName`、`appSubject`、`apps`、`archiveCount`、`autoTagged`、`autoTags`、`avgCycle`、`avgDaily`、`avgResponseTime`、`bizTypes`、`businessModules`、`businessSystems`、`businessType`、`byBizType`、`byCategory`、`byChannel`、`byDataCluster`、`byDatabase`、`byInstitution`、`byLevel`、`byRegion`、`byResourceType`、`byTime`、`byType`、`callCount`、`callFreq`、`callInterface`、`callTime`、`categories`、`category`、`categoryKey`、`channel`、`channelCount`、`channelName`、`channels`、`cluster`、`clusters`、`cohesion`、`collectTime`、`columnDesc`、`columnName`、`columnType`、`columns`、`completed`、`contactPerson`、`count`、`current`、`currentPeriod`、`dataCluster`、`dataCount`、`dataProduct`、`dataStructure`、`dataType`、`dataVolume`、`days`、`delta`、`department`、`departments`、`deployLocation`、`desc`、`description`、`detail`、`direction`、`durationMs`、`features`、`field`、`fieldName`、`fieldType`、`fields`、`fusionTrends`、`growth`、`growth7d`、`growthTrend`、`heat`、`heatLevel`、`id`、`inProgress`、`insight`、`ipAddress`、`isKeyUser`、`keywords`、`label`、`labels`、`lastActiveDate`、`lastCallTime`、`lastRun`、`lastUpdateTime`、`lastUsed`、`level`、`lifecycle`、`lifecycleHint`、`links`、`manualReview`、`meaning`、`monthlyTrend`、`name`、`nodes`、`orgs`、`peakPeriod`、`period`、`periods`、`previous`、`previousPeriod`、`projectTeam`、`provider`、`publishTime`、`purpose`、`quality`、`qualityLevel`、`qualityScore`、`quarter`、`recordCount`、`records`、`region`、`relatedClusterIds`、`relatedIds`、`relatedNodes`、`relatedProject`、`relation`、`reliability`、`reliabilityHint`、`reliabilityLevel`、`reliabilityScore`、`required`、`resolved`、`resource`、`resourceCount`、`resourceCovered`、`resourceType`、`resources`、`result`、`rows`、`sampleTags`、`schema`、`series`、`share`、`similarity`、`size`、`source`、`sourceDept`、`sourceType`、`strength`、`structureCompare`、`structureTrend`、`subjectType`、`subscriberCount`、`successRate`、`suggestion`、`summary`、`supplierCount`、`supplierName`、`suppliers`、`tableComment`、`tableName`、`tables`、`tags`、`target`、`techType`、`techTypes`、`time`、`topResource`、`totalCalls`、`totalDatabases`、`totalRecords`、`totalResources`、`totalSinceLaunch`、`totalStorage`、`totalTables`、`type`、`typeDist`、`unit`、`updateCycle`、`updateFeed`、`updateFreq`、`updateStatus`、`updateSuccessRate`、`updateTime`、`usageCount`、`usageCycle`、`usageUnit`、`userId`、`userName`、`valueShare`、`volume`。

另有 9 个中文对象键，第 5 节没有写：`企业`、`半结构化`、`国内数据库`、`国外数据库`、`实时流`、`开源平台`、`科研院所`、`第三方平台`、`结构化`。它们是 `structureTrend.series`、`byTime.series`、`byBizType[]`、`typeDist` 上的固定键，不是展示文案。

第 5 节写了组装来源（表名、`list_code`、`series_code`）。那些是库列，不是响应键。本契约不改第 4 节的表，也不把库列名当成 JSON 键。

## 明确不做

- 不实现 `/display/v1/data-ops/sources`、`/themes`、`/usage`。
- 不在接口里返回写死的 mock JSON。数从久新或 `gapfill_dr_*` 来，由后续 Java 叶读库组装。
- 不把实体存量写进「资源总量」或年度接入。不把 `SHOW COLUMNS` 写进 `tableSchemas`。
- 不新增第 5 节以外的路径，不增加类型以外的响应键（`origin`、`entityStock`、`columnCatalog` 除外）。
- 不改主题页四张卡上的涨跌文案。
- 不代替 `SYSINT-05-04-L01` 的页面交付。

## 架构合规

| 铁律 | 结果 |
|---|---|
| 调用链：页面 → Java REST，不直连 Python / 久新 / ADS | ✅ 路径停在展示服务 `/v1/data-ops/.../dataset` |
| Java 不写算法、不内嵌 mock | ✅ 本叶无实现；契约禁止 data 里写死 fixture |
| D12 不调 demo 服务 | ✅ |
| D18 真查或读 ADS 表 | ✅ 契约只定响应形状；读哪张表仍以方案第 4–5 节为准 |
| 可观测 | ✅ 不新造 trace 字段；沿用现有请求头 |
| 前端代码 | ✅ 未改。`real()` 仍是裸 fetch |

## 测试与 CI

- 无代码改动，未跑构建，未 commit，未 push。
- 对照材料：`dataResources.ts` 四个 interface、`dataResourcesSeed.ts` 的 `typeof` 键、`mock/modules/dataResources.ts` 四个 `create*Dataset`、`request.ts` 第 137–143 行（`code === 0` 返回 `data`）、方案第 5 节。

## 遗留

- `entityStock`、`columnCatalog` 的子键等 `DR-RES-A0-L01`。子键只能留在这两个对象里。
- 前端在 `DR-RES-D1-L01` 之前，`USE_MOCK=false` 的裸 `fetch` 不会拆信封。这是已拍板的接线顺序，不是本契约要补的代码。

## 涉及文件

- 新增：`agent-delivery/agent-handoffs/科技数据资源-DR/BE-DR-CONTRACT-01.md`
- 只读：方案第 5 节、`DR-RES-长任务总控.md`、`lumen-ui-science-pc` 的 `src/types/dataResources.ts`、`src/api/dataResources.ts`、`src/utils/request.ts`、`src/mock/modules/dataResources.ts`、`src/mock/modules/dataResourcesSeed.ts`
