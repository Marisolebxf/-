# 科技数据资源 · 聚合服务 → 科学数据中心 · 上游接口需求（粗粒度）

> 状态：DRAFT · 待 **human:淮政玮** 审  
> 任务：`BE-DR-FE-API-ALIGN-L01`  
> **调用方**：展示系统聚合服务（Java BFF / `gkxlumen-display`）  
> **提供方**：第三方「科学数据中心」（接口包 `EXT-B3-RESOURCE`，清单 R-01～R-24）  
> **不写**：前端直连、门户「科技资源服务」、gapfill DDL、数据集成作业、过细 OpenAPI/样例报文  
> **对外四 GET 不变**：浏览器仍只吃 `/display/v1/data-ops/{overview|access|theme|application}/dataset`；本表是 BFF **背后**要调的上游能力，不扩对外路径。  
> ponytail: **off**（definition）

## 0. 读法约定

每条接口固定六列：**界面 | 需规seq | 接口中文名 | 输入必填 | 输入选填 | 期望输出**。

共性：

- 鉴权、限流、统一时区、`updated_at`、稳定主键（资源 ID / 主题库 ID）由供方约定；本文件不展开。
- 现行前端筛选、导出、分页在浏览器对整包做；上游列表类仍建议支持时间窗与分页，便于 BFF 拉取后组装。
- 现行 C1～C4 读 `gapfill_dr_*`；本文件描述切到科学数据中心**接口对接**时的能力需求，不要求本叶改 Java。
- 字段线索见 `对接澄清-科技数据资源-字段级.md`；勿写成数据集成。

速查索引：

| 视窗 | 接口 |
|---|---|
| 总体 | R-01～R-08 |
| 接入 | R-09～R-13 |
| 主题 | R-14～R-18 |
| 应用 | R-19～R-24 |

---

## 1. 总体视窗（DS-17）

| 界面 | 需规seq | 接口中文名 | 输入必填 | 输入选填 | 期望输出 |
|---|---|---|---|---|---|
| 总体·KPI 卡、类型分布、主题分布、年度接入趋势、来源机构活跃度 | 主 330；支撑 333、334 | R-01 资源接入总览统计接口 | （无，默认全量快照） | 统计时间起点、统计时间终点、时间粒度（年/月） | 资源类型/数量/占比、资源总量汇总（目录口径，禁实体存量）、主题分布 + 平均质量、按年接入总量/年度新增/同比（首年同比可空）、来源机构活跃度（机构接入次数、活跃度评分、状态）；聚合组装 overviewKPIs、resourceTypeDistribution、resourceThemeDistribution、overviewAnnualAccessTrend、overviewSourceActivity |
| 总体·来源分布图、来源分析详情（结构/对比/明细） | 主 331 | R-02 资源来源分析接口 | （无，默认全来源结构） | 来源类型过滤（国内数据库/国外数据库/科研院所/企业/开源平台）、统计时间起止 | 按来源类型的体量/条数/占比/相对上期变化、可靠性提示 + 平均质量、自动/人工归类统计摘要、按月/季结构趋势序列、相邻期结构对比行、可下钻来源明细（名称/提供方/区域/数据类型/采集时间/质量与可靠性等级/领域/关联项目/标签）；聚合组装 resourceSourceDistribution、overviewSourceAnalysis |
| 总体·接入资源详情表 | 主 332 | R-03 接入资源详情查询接口 | 单条查时须带 resource_id；批量查时须带 resource_ids（数组） | 关键词、分页页码、每页条数 | 每条资源：resource_id、名称、类型、类别、srs_source、渠道、采集时间、更新频率、最近更新时间、记录量、体量、状态、关联项目、质量分、学科领域、标签等元数据，足以支撑表格展示与筛选；聚合组装 resourceAccessDetailList |
| 总体·大数据资源中心概览（分类/库表规模） | 主 335 | R-04 主题库与资源中心目录接口 | （无，默认完整目录树） | 分类（科技要素库/领域主题库）、领域或技术类型标签 | 中心下各分类（分类名/说明/库数/表数/记录量/存储量/更新状态/技术领域标签）、主题库骨架行（theme_id、theme_name、tags、resource_count）、中心介绍文案；聚合组装 bigDataCenterStats 概览与分类，为主题页目录提供骨架 |
| 总体·大数据中心资源详情 / 更新动态 | 主 336 | R-05 资源详情深度浏览接口 | resource_id（须唯一定位） | （无强制项） | 该资源完整属性（类型、领域、技术类型、更新频率、结构摘要、记录量、体量、质量、近 7 日增长、活跃度、关联资源、关键词）、近期更新动作流（时间、动作、增量、状态）；聚合组装 bigDataCenterStats.resources、updateFeed 及详情抽屉字段 |
| 总体·知识关联图、节点详情、语义主题聚合 | 主 339～342；支撑 337、338 | R-06 资源关联关系查询接口 | （无，允许空挂接） | resource_id 或 theme_id（局部展开） | 目录级节点（node_id/name/category/color/size/desc_text）与边（src_id/dst_id/relation/strength）、节点详情（名称/类别/描述 + 可选记录量/质量/来源/用户/调用等）、图例分类、语义主题簇（cluster_name/member_names/score）；不造七要素图谱；聚合组装 knowledgeGraphData、knowledgeGraphCategories、knowledgeGraphNodeDetails、semanticThemeAggregation。**节点详情不要多出 parentDB 字段** |
| 总体·接口状态条、应用状态监控数字 | 主 343、344 | R-07 应用系统与接口状态监控接口 | （无，默认最近探针结果） | 探针时间窗（起止） | 各接口/系统的可用性标签与数值、平均响应时延 ms、告警总数、严重告警数、成功率（或等价失败率）；可选附调用频率等日志级指标；聚合组装 interfaceStatusMetrics、resourceUsageStats。**禁止在出给前端的 resourceUsageStats 里多出 totalCalls** |
| 总体·应用主体列表、累计调用分析 | 主 345、346 | R-08 应用主体与调用趋势接口 | （无，无调用账时整包空） | 统计周期、主体类型（机构/项目/用户/应用系统） | 应用主体清单（名称/类型/资源类型/用途/调用次数/价值占比/是否重点用户）、自上线以来累计调用/覆盖资源数/日均/高峰时段/热度生命周期提示、按周/月/季调用与累计序列、按资源类型累计与占比；聚合组装 resourceAppSubjects、cumulativeCallAnalysis |

---

## 2. 接入视窗（DS-18）

| 界面 | 需规seq | 接口中文名 | 输入必填 | 输入选填 | 期望输出 |
|---|---|---|---|---|---|
| 接入·KPI、完成度块、归集趋势图 | 主 347、349；支撑 350 | R-09 接入完成度与归集量统计接口 | （无，默认接入任务 + 归集量总览） | 统计时间起止、时间粒度（年/月/周/日）、接入方式（API/文件/库同步/人工/物联） | 接入任务总量/已完成/进行中/待处理计数、按渠道拆分完成态、归集数据量随时间的新增/更新序列（多粒度）；聚合组装 accessKPIs、accessCompletionData、resourceAccessTrend。**归集量口径≠实体存量** |
| 接入·来源渠道分析与明细 | 主 348、351～355 | R-10 来源渠道分析接口 | （无，默认全渠道结构） | 渠道名、业务类型、统计时间起止 | 各渠道归集体量/条数/占比/颜色/业务类型标签、按月/季渠道结构序列、按业务类型渠道交叉计数、明细行（资源名/渠道/数据类型/采集时间/质量等级/关联项目/领域/体量）；聚合组装 accessSourceAnalysis。**明细行足以支撑结构对比与浏览器侧筛选/导出** |
| 接入·分区详情、主题库列表骨架 | 主 356～359 | R-11 接入资源分区详情接口 | （无，默认全分区视图） | 区域、分库、来源机构、主题/学科过滤 | 按区域/分库/来源机构的资源数/体量/平均质量/结构化类型分布、下属机构列表（机构名/资源数/质量/代表资源名）、主题归类信息、分区说明块；聚合组装 partitionData、接入页 themeDatabases 骨架 |
| 接入·历史归集记录、历史仪表盘、更新周期统计 | 主 360～363 | R-12 历史接入与更新周期接口 | （无，默认可展示历史窗） | 渠道、表名、异常类型、时间起止 | 历史归集行（渠道/表名/接入日期/条数/体量/更新周期/更新时间/状态/异常类型与说明）、仪表盘汇总（归档次数/渠道数/表数/异常数/成功率）、分月接入量/更新成功率/异常数趋势、异常类型分布、更新状态分布、按渠道的平均周期/成功率/趋势；聚合组装 historyAccessRecords、historyAccessDashboard、updateCycleStats |
| 接入·问题资源列表与问题统计图 | 主 364～367 | R-13 问题资源清单与统计接口 | （无，无质量源时空列表 + 空统计） | 问题类型、级别（紧急/重要/普通）、状态、渠道 | 问题资源行（resource_id/名称/表名/类型/类别/数据集群/级别/状态/时间/渠道/详情/建议）、按类别/集群/类型/级别/渠道的计数、按月问题总量与已解决量；聚合组装 problemResources、problemResourceStats |

---

## 3. 主题视窗（DS-19）

| 界面 | 需规seq | 接口中文名 | 输入必填 | 输入选填 | 期望输出 |
|---|---|---|---|---|---|
| 主题·顶部四卡、主题库分类浏览列表 | 主 368、370 | R-14 主题库分类与资源分布接口 | （无，默认全部分类与概览计数） | 分类、标签过滤 | 顶部四卡纯数字：themeDatabaseCount（主题库总数）、tableCount（表总数）、recordCountLabel（记录量标签，如"10.2"，不含单位）、storageLabel（存储量标签，如"18.6"，不含单位）；各主题库列表头行：theme_id、名称、分类、resource_type、发布时间、record_yi、storage_tb、更新时间、描述、来源、区域、分区、联系人、采集时间、update_freq、数据结构说明、关联项目、tags[]、table_count、quality_score；聚合组装 themeDatabaseCount、tableCount、recordCountLabel、storageLabel、themeDatabases 列表头。**四卡涨跌文案由前端本地写，上游不必出涨跌字段** |
| 主题·主题库/数据集详情字段 | 主 371、372 | R-15 数据集元数据详情接口 | theme_id 或 resource_id / dataset_id（二选一，须唯一定位） | （无强制项） | 数据集名称、所属主题库、resource_type、数据量、source_name（来源单位）、采集与更新时间、update_freq、quality_score、related_project（关联项目）、responsible_person（维护责任人，可空）等完整元属性；聚合填入 themeDatabases[] 对应行字段 |
| 主题·主题库下表结构（字段级） | 主 373 | R-16 数据表结构查询接口 | theme_id 或 dataset_id（须定位到库） | table_name（只查一张表时） | 库下各表：table_name、table_comment（表注释/业务含义）；每表下各字段：field_name、field_type、business_meaning（业务含义）、required_flag（是否必填）；聚合组装 themeDatabases[].tableSchemas。**禁止用久新/snap 的列目录顶替本接口结果写入 tableSchemas** |
| 主题·数据集关联关系图 | 主 374 | R-17 数据集关联关系接口 | （无，允许空图） | theme_id（局部关系） | 目录级关联点（dataset_id/theme_id、名称、类别、描述、规模）与边（src_id/dst_id、关系类型如引用/衔接/主题交叉、强度 0–1）；不升格为全要素图谱；聚合组装 datasetRelationData |
| 主题·智能搜索壳（现行多为浏览器侧筛整包） | 主 369、375 | R-18 主题库检索接口 | BFF 现行组装四 GET 时**可不调用**本接口（整包目录到位后由浏览器筛选） | 关键词、类别、时间起止、主题、分页页码、每页条数 | 命中的主题库/数据集摘要列表（theme_id/dataset_id、名称、category、summary、update_time）及分页信息；非 NL2SQL、非图谱实体检索。**若供方只有检索、没有全量目录，须人批准是否改 BFF 组装策略；默认不扩对外 GET** |

---

## 4. 应用视窗（DS-20）

> 整窗依赖「资源调用账」。无账时允许各接口返回空集合；BFF 仍保持应用 Dataset 19 个根键。

| 界面 | 需规seq | 接口中文名 | 输入必填 | 输入选填 | 期望输出 |
|---|---|---|---|---|---|
| 应用·KPI、资产排行、调用趋势基线（实时监控跳动用） | 主 376～379 | R-19 数据应用排行与资产总览接口 | （无，无调用账允许空） | 统计时间起止、排序维度（调用量/主体/领域） | 应用侧 KPI（总调用、应用系统数、资产数等）；资产/应用排行行：asset_id、名称、类别、部门、数据类型、应用主体、部署位置、使用周期、业务类型、使用单位、最近活跃日、调用次数、用户数、增长率、业务模块；usageCallTrend[]（date、call_count、active_user_count）作为"实时监控"跳动基线（至少 30 天）；监控摘要可与 R-07 分工；聚合组装 applicationKPIs、assetRanking、usageCallTrend |
| 应用·字段使用详情表、使用详情趋势 | 主 380～383 | R-20 数据资源使用详情接口 | （无，无使用账允许空） | table_name、来源部门、统计时间起止 | columns[]：table_name、column_name、column_type、column_desc、source_dept、app_name、last_usage_time、usage_count、subscription_count；usage_detail_trend[]：按月使用次数序列；聚合组装 dataUsageDetails、usageDetailTrend。**column_type 与 R-16 一致** |
| 应用·主题被调用基本信息、趋势、用户/系统追踪 | 主 384～387 | R-21 主题调用统计与趋势接口 | （无，无调用账允许空） | 主题名、时间粒度（日/周/月）、统计时间起止 | 主题调用基本信息：theme_name、调用时间、调用频率、调用接口名、业务系统；theme_call_trend[]：多线序列（每主题一条线，至少 12 期月），横轴 period_label、纵轴 call_count；call_tracking[]：调用用户与应用系统追踪（user_name、部门、应用系统、主题、最近调用时间、client_ip、调用次数）；聚合组装 themeCallBasicInfo、themeCallTrend、callUserTracking |
| 应用·供应方汇总、区域分组、调用明细与趋势 | 主 388～391 | R-22 供应方调用统计接口 | （无，无调用账允许空） | 区域、统计周期、供应方名称 | 供应方归集（supplier_dept、部门、区域、资源数、**累计调用次数**、占比）；supplier_region_groups[]（区域、供应方数、资源数、**累计调用**、区域下供应方列表）；supplier_call_details[]（supplier_dept × data_product × biz_type × period，**须含累计调用**）；period_enum[]（周期枚举如日/周/月/季）；supplier_call_trend[]（多线趋势）；聚合组装 supplierStats、supplierRegionGroups、supplierCallDetails、supplierCallPeriods、supplierCallTrend。**此处行内累计调用字段要有**，与 R-07 禁止出站的 totalCalls 不是同一处 |
| 应用·需求方统计与调用趋势 | 主 392～395 | R-23 需求方调用统计接口 | （无，无调用账允许空） | 部门、业务类型、项目组 | 需求方归集（demander_name、部门、业务类型、项目组、累计调用、活跃天数、日均）；demander_call_trend[]（多线或行为分布序列）；聚合组装 demanderStats、demanderCallTrend |
| 应用·业务应用统计、部门分组、调用日志与趋势 | 主 396～399 | R-24 业务应用调用明细与导出接口 | （无，无调用账允许空） | 应用名称、来源部门、调用时间起止 | 业务应用归集（app_name、来源部门、业务类型、状态、应用数、调用量）；business_application_dept_groups[]（部门 → 应用列表 + 累计调用）；business_application_call_logs[]（调用明细日志：应用、部门、业务类型、用户、资源、调用时间、结果、耗时 ms、次数，列齐即可由浏览器导出）；business_call_trend[]（多线趋势）；聚合组装 businessApplicationStats、businessApplicationDeptGroups、businessApplicationCallLogs、businessCallTrend。**不要求单独「导出文件流」接口；导出频控由我方前端/网关控制** |

---

## 5. 边界与不做

| 项 | 说明 |
|---|---|
| 调用链 | 前端 → 聚合四 GET →（本文件）科学数据中心；**前端不直连** |
| 对外路径 | **不扩**四个 GET 以外的 `/display/v1/data-ops/**` |
| 数据集成 | 本模块**仅接口对接**；不写库表 DDL、不写 ETL 作业 |
| 门户轨 | 不把门户「科技资源服务」算进本轨 |
| 种子多键禁出站 | `resourceUsageStats.totalCalls`、`knowledgeGraphNodeDetails.*.parentDB` |
| 允许多出 | `origin`、`entityStock`（仅 overview）、`columnCatalog`（仅 theme）按契约；非本供方必出时可仍走久新/snap |

---

## 6. 计数

| 视窗 | 上游接口条数 | seq 覆盖 |
|---|---:|---|
| 总体 | 8（R-01～R-08） | 330–346 |
| 接入 | 5（R-09～R-13） | 347–367 |
| 主题 | 5（R-14～R-18） | 368–375 |
| 应用 | 6（R-19～R-24） | 376–399 |
| **合计** | **24** | 330–399 |

---

## 7. 修订

| 日期 | 说明 |
|---|---|
| 2026-11-11 | 首版：R-01～R-24 粗粒度入参/出参表 |
| 2026-11-11 | 修订：每条改为「输入需求 / 输出需求」明确文字说明 |
| 2026-11-12 | **修订**：全部四视窗重写为统一六列表格结构（界面 / 需规seq / 接口中文名 / 输入必填 / 输入选填 / 期望输出） |
