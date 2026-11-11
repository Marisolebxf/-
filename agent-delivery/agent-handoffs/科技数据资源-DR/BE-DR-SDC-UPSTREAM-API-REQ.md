# 科技数据资源 · 聚合服务 → 科学数据中心 · 上游接口需求（粗粒度）

> 状态：DRAFT · 待 **human:淮政玮** 审  
> 任务：`BE-DR-FE-API-ALIGN-L01`  
> **调用方**：展示系统聚合服务（Java BFF / `gkxlumen-display`）  
> **提供方**：第三方「科学数据中心」（接口包 `EXT-B3-RESOURCE`，清单 R-01～R-24）  
> **不写**：前端直连、门户「科技资源服务」、gapfill DDL、数据集成作业、过细 OpenAPI/样例报文  
> **对外四 GET 不变**：浏览器仍只吃 `/display/v1/data-ops/{overview|access|theme|application}/dataset`；本表是 BFF **背后**要调的上游能力，不扩对外路径。  
> ponytail: **off**（definition）

## 0. 读表约定

| 列 | 含义 |
|---|---|
| 界面 | 四视窗 + 页面区块（对齐 FE Dataset 根键 / 页面区） |
| 需规 seq | 展示 SRS 330–399；多对一已合并到 R-xx |
| 接口中文名 | 对齐清单 R-xx 名称（可与科学数据中心侧现名映射） |
| 输入必填 / 选填 | 参数名级；**不必** JSON Schema |
| 期望输出 | 聚合组装四 Dataset 时要用的字段/对象（列名级，不嵌到叶子） |

共性：

- 鉴权 / 限流 / `updated_at` / 稳定主键（`resource_id`、`theme_id` 等）由供方约定；本表不展开。
- 前端筛选、导出、分页现行在浏览器对整包做 → 上游列表类接口仍建议支持时间窗/分页，供 BFF 拉取后组装。
- 现行 C1～C4 读 `gapfill_dr_*`（D18 mock）；本表描述**切到科学数据中心接口对接**时的能力需求，**不是**要求本叶改 Java。
- 字段线索见 `对接澄清-科技数据资源-字段级.md`；勿写成数据集成。
- 必读「能力对照-科技数据资源-科学数据中心.md」在仓内**未找到**；本表以 R 清单 + 对接澄清 + FE/契约落点为准。若后续补齐能力对照，按监管人指示修订本表。

---

## 1. 总体视窗（DS-17）

| 界面 | 需规seq | 接口中文名 | 输入必填 | 输入选填 | 期望输出 |
|---|---|---|---|---|---|
| 总体 · KPI / 类型分布 / 年度接入 / 来源活跃度 | 330；支撑 333、334 | R-01 资源接入总览统计接口 | （无；全量快照即可） | `time_from`、`time_to`、`grain` | 资源类型/数量、分布占比、年度增长（年/`total`/`added`）、来源机构活跃度；供装 `overviewKPIs`、`resourceTypeDistribution`、`overviewAnnualAccessTrend`、`overviewSourceActivity`、`resourceThemeDistribution` |
| 总体 · 来源结构与分析 | 331 | R-02 资源来源分析接口 | （无） | `srs_source`、`time_from`、`time_to` | 来源结构/占比/变化、可靠性与质量相关字段、明细行；供装 `resourceSourceDistribution`、`overviewSourceAnalysis`（含 `classifyStats`/`sourceTypes`/`structureTrend`/`structureCompare`/`details`） |
| 总体 · 接入资源详情表 | 332 | R-03 接入资源详情查询接口 | （列表拉全量时可无） | `resource_id`、`keyword`、`page`、`page_size` | 元数据：名称、类型、学科/领域、采集/更新、关联项目、质量、关键词等；供装 `resourceAccessDetailList` |
| 总体 · 大数据中心 / 主题库目录 | 335 | R-04 主题库与资源中心目录接口 | （无） | `category`、`tags` | 主题库/要素库分类树或列表、库表记录存储概览；供装 `bigDataCenterStats`（及与主题页共用的目录骨架） |
| 总体 · 资源深度详情（抽屉/中心内） | 336 | R-05 资源详情深度浏览接口 | `resource_id` | — | 完整属性、更新流、近期增长/热点等；供装中心 `resources`/`updateFeed` 及详情抽屉 |
| 总体 · 关联图 / 语义聚合 | 339–342；支撑 337、338 | R-06 资源关联关系查询接口 | （无；可空挂接） | `resource_id`、`theme_id` | 目录级 `nodes`/`edges`（或交叉引用）、语义主题聚合；供装 `knowledgeGraphData`、`knowledgeGraphCategories`、`knowledgeGraphNodeDetails`、`semanticThemeAggregation`（**不验收**全要素图谱） |
| 总体 · 接口/应用状态监控 | 343、344 | R-07 应用系统与接口状态监控接口 | （无） | `probed_at` 窗 | 可用性、延迟、告警、调用频率/失败率等；供装 `interfaceStatusMetrics`、`resourceUsageStats`（**仅** `avgResponseTime`/`alarmCount`/`alarmCritical`/`successRate`；禁止多出 `totalCalls`） |
| 总体 · 应用主体与累计调用 | 345、346 | R-08 应用主体与调用趋势接口 | （无；无调用账可空） | `period`、`subject_type` | 应用主体列表、累计/分时调用；供装 `resourceAppSubjects`、`cumulativeCallAnalysis` |

---

## 2. 接入视窗（DS-18）

| 界面 | 需规seq | 接口中文名 | 输入必填 | 输入选填 | 期望输出 |
|---|---|---|---|---|---|
| 接入 · KPI / 完成度 / 归集趋势 | 347、349；支撑 350 | R-09 接入完成度与归集量统计接口 | （无） | `time_from`、`time_to`、`grain`、`ingest_method` | 完成度计数（完成/进行中/待处理）、归集体量与日/周/月趋势；供装 `accessKPIs`、`accessCompletionData`、`resourceAccessTrend` |
| 接入 · 来源渠道分析 | 348、351–355 | R-10 来源渠道分析接口 | （无） | `channel`、`biz_type`、`time_from`、`time_to` | 渠道占比/体量、结构对比、明细属性；供装 `accessSourceAnalysis`（`channels`/`byTime`/`byBizType`/`details`） |
| 接入 · 分区 / 主题下资源 | 356–359 | R-11 接入资源分区详情接口 | （无） | `region`、`db_partition`、`source_org`、`theme` | 分区清单、主题归类、质量、类型分布；供装 `partitionData`、接入页 `themeDatabases` 骨架 |
| 接入 · 历史归集与更新周期 | 360–363 | R-12 历史接入与更新周期接口 | （无） | `channel`、`table_name`、`anomaly_type`、`time_from`、`time_to` | 历史归集记录、更新周期与成功率/异常趋势；供装 `historyAccessRecords`、`historyAccessDashboard`、`updateCycleStats` |
| 接入 · 问题资源 | 364–367 | R-13 问题资源清单与统计接口 | （无；无质量源可空） | `issue_type`、`level`、`status`、`channel` | 问题列表（类型/级别/状态/详情/建议）与分级统计；供装 `problemResources`、`problemResourceStats` |

---

## 3. 主题视窗（DS-19）

| 界面 | 需规seq | 接口中文名 | 输入必填 | 输入选填 | 期望输出 |
|---|---|---|---|---|---|
| 主题 · 顶部四卡 + 分类浏览 | 368、370 | R-14 主题库分类与资源分布接口 | （无） | `category`、`tags` | 主题库树/分类、库数/表数/记录量/存储等概览；供装 `themeDatabaseCount`、`tableCount`、`recordCountLabel`、`storageLabel`、`themeDatabases` 列表头 |
| 主题 · 数据集元数据详情 | 371、372 | R-15 数据集元数据详情接口 | `theme_id` 或 `resource_id` | — | 名称、来源、类型、更新频率、质量、关联项目、责任人等；填入 `themeDatabases[]` 行字段 |
| 主题 · 表结构 | 373 | R-16 数据表结构查询接口 | `theme_id` 或数据集 ID | `table_name` | 表名、字段名/类型/含义/必填；供装 `themeDatabases[].tableSchemas`（**禁止**用久新 `columnCatalog` 顶替） |
| 主题 · 关联关系图 | 374 | R-17 数据集关联关系接口 | （无；可空） | `theme_id` | 目录级点边（可含 `strength`）；供装 `datasetRelationData` |
| 主题 · 检索壳（现行浏览器筛） | 369、375 | R-18 主题库检索接口 | （BFF 现行可不调；整包后浏览器筛） | `keyword`、`category`、`time_from`、`time_to`、`page`、`page_size` | 命中列表+分页；**现行对外四 GET 不强制**；若供方仅提供检索接口而无全量目录，BFF 再议是否改组装策略（须人批准，默认不扩对外 GET） |

---

## 4. 应用视窗（DS-20）

> 整窗依赖「资源调用账」。无账时允许上游返回空集合；BFF 仍保持 19 个根键。

| 界面 | 需规seq | 接口中文名 | 输入必填 | 输入选填 | 期望输出 |
|---|---|---|---|---|---|
| 应用 · KPI / 资产排行 / 监控基线 | 376–379 | R-19 数据应用排行与资产总览接口 | （无） | `time_from`、`time_to`、排序维 | 应用/资产排行与详情汇总、调用/用户/增长等；监控摘要（响应/成功率/告警可与 R-07 分工）；供装 `applicationKPIs`、`assetRanking`；实时监控跳动用本轨组装的 `usageCallTrend`（`dates`/`calls`/`users`） |
| 应用 · 字段使用详情 | 380–383 | R-20 数据资源使用详情接口 | （无） | `table_name`、`dept`、`time_from`、`time_to` | 字段属性、来源部门、使用次数/订阅、趋势序列；供装 `dataUsageDetails`、`usageDetailTrend` |
| 应用 · 主题被调用 | 384–387 | R-21 主题调用统计与趋势接口 | （无） | `theme`、`grain`、`time_from`、`time_to` | 主题调用基本信息、用户/系统追踪、日周趋势；供装 `themeCallBasicInfo`、`themeCallTrend`、`callUserTracking` |
| 应用 · 供应方 | 388–391 | R-22 供应方调用统计接口 | （无） | `region`、`period`、`supplier` | 供应部门归集、累计调用、区域分组、明细与趋势；供装 `supplierStats`、`supplierRegionGroups`、`supplierCallDetails`、`supplierCallPeriods`、`supplierCallTrend`（行内 **`totalCalls` 要有**） |
| 应用 · 需求方 | 392–395 | R-23 需求方调用统计接口 | （无） | `department`、`business_type`、`project_team` | 需求方归集、累计调用、行为分布/趋势；供装 `demanderStats`、`demanderCallTrend` |
| 应用 · 业务应用与明细 | 396–399 | R-24 业务应用调用明细与导出接口 | （无） | `app_name`、`department`、`time_from`、`time_to` | 业务应用归集、部门分组、调用明细日志；供装 `businessApplicationStats`、`businessApplicationDeptGroups`、`businessApplicationCallLogs`、`businessCallTrend`（导出由浏览器做，上游给齐可导出列即可） |

---

## 5. 边界与不做

| 项 | 说明 |
|---|---|
| 调用链 | 前端 → 聚合四 GET →（本表）科学数据中心；**前端不直连** |
| 对外路径 | **不扩**四个 GET 以外的 `/display/v1/data-ops/**` |
| 数据集成 | 本模块**仅接口对接**；不写库表 DDL、不写 ETL 作业 |
| 门户轨 | 不把门户「科技资源服务」/科学数据中心门户页算进本轨 |
| 种子多键 | `resourceUsageStats.totalCalls`、`knowledgeGraphNodeDetails.*.parentDB` → **禁止**经聚合 HTTP 出站给前端（见差异摘要） |
| 允许多出 | `origin`、`entityStock`（仅 overview）、`columnCatalog`（仅 theme）仍按契约；非科学数据中心必出项时可仍走久新/snap |

## 6. 计数

| 视窗 | 上游接口条数（R） | seq 覆盖 |
|---|---:|---|
| 总体 | 8（R-01～R-08） | 330–346 |
| 接入 | 5（R-09～R-13） | 347–367 |
| 主题 | 5（R-14～R-18） | 368–375 |
| 应用 | 6（R-19～R-24） | 376–399 |
| **合计** | **24** | 330–399 |

## 7. 修订

| 日期 | 说明 |
|---|---|
| 2026-11-11 | 首版：按 R-01～R-24 × 四视窗落粗粒度入参/出参；对齐 FE 根键落点；标明调用方=聚合、提供方=科学数据中心 |
