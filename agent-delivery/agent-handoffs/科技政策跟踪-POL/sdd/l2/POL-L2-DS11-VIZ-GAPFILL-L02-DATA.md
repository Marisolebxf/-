# POL-L2-DS11-VIZ-GAPFILL-L02-DATA · 政策分析评价 · Tab1 七可视化块 · 数据落点

- 任务：`POL-L2-DS11-VIZ-GAPFILL-L02-DATA`
- 日期：2026-11-12
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`（主会话代认领，registry 状态推进与本单 handoff 登记由主会话收口）
- 强度：ponytail off（定义任务，不缩文档）
- 上游：`POL-L2-DS11-MOCKAUDIT-L01` 盘点表（Tab1 六卡 FIX-03 违规判定与下线记录）、`POL-L2-DS11-VIZ-ARCH` / `POL-L2-DS11-VIZ-DATA`（219–222 四叶，已定稿，本单不改）、`POL-L2-DS12-EST-DATA`（列清单格式先例）、`POL-SIM-HEADER-SCORE-DATA`（页头得分表先例）
- 对照：`agent-delivery/metrics/request/展示系统/pages/DS-11-POLICY-EVAL.yaml`（只读）

本叶只定政策分析评价页 Tab1「分析报告可视化」里 **七个无 SRS 序号的可视化块** 的数据落点。这七块是 demo 复刻保留块（走查档 A），不在需规 219–222 十三叶原文里；FIX-03（MOCKAUDIT-L01）已把前端 fixture 按合规下线，真轨（USE_MOCK=false）现为诚实空态「无读面出处」。本单给七块定列级落点，供后续灌数单建表灌行。列级定义只定粒度和必要列。下面的列清单不是可执行 SQL，本单不建库、不灌数、不跑脚本、不改代码。

上游只引用，不改写：MOCKAUDIT 盘点表、VIZ-ARCH 第 2/5/9 节、VIZ-DATA 第 2–5/7 节、DS-11 页面指标 yaml。不新造 `metric_id`，不改 D4。

## 1. 范围与逐块裁定

七块都挂在 `lumen-ui-science-pc/src/views/policy/analysis/` 的 Tab1。浏览器只打 `/display/v1/policy/**`（具体入口形态待拍板，见第 8 节第 1 条）。查询只读。查询请求不灌数。表里没有行就返回空。接口不直接返回写死的 mock。空态是空。

| # | 块 | 组件 | 种子（mock 真源） | 判定 | 库表 |
|---|---|---|---|---|---|
| 1 | 评估指标体系卡（进度条列表+雷达） | `index.vue` 内联块 | `policySeed.evaluationMetrics` | 新定列 | `gapfill_policy_eval_viz_metric` |
| 2 | 政策/企业/人才画像（摘要+抽屉详情） | `PortraitTrio.vue` | `policySeed.policyPortraitSummaries` | 新定列 | `gapfill_policy_eval_viz_portrait` |
| 3 | 地理分布图（中国地图+城市气泡） | `GeographicMapPanel.vue` | `policySeed.geographicDistributionData` | 新定列 | `gapfill_policy_eval_viz_geo` |
| 4 | 分地区落实率表 | `ImplementationByRegion.vue` | `policySeed.implementationByRegionData` | 新定列 | `gapfill_policy_eval_viz_region_impl` |
| 5 | 话题热力图 | `TopicHeatmapWithSentiment.vue`（热力部分） | `policySeed.topicHeatmapData` | 新定列 | `gapfill_policy_eval_viz_topic_heat` |
| 6 | 情感分布（堆叠柱+环形） | `TopicHeatmapWithSentiment.vue`（情感部分） | `policySeed.topicSentimentSummary` | 新定列 | `gapfill_policy_eval_viz_topic_sentiment` |
| 7 | 产业影响力气泡图 | `index.vue` 内联块（`bubbleOption`） | `policySeed.bubbleChartData` | 新定列 | `gapfill_policy_eval_viz_bubble` |

归并裁定：**七块全部新定列，无一块归并既有读面，无一块维持有意空态**（本单就是 FIX-03 空态文案里指的「待立 DATA 单」）。逐块不归并的理由：

| 归并候选 | 裁定 | 理由 |
|---|---|---|
| `gapfill_policy_sim_score`（页头得分，FIX-01 真轨） | 不归并块 1 | 该表行种类是「页面得分」，`jobs kind=页面得分` 会把整表行喂给页头卡；写进维度行会被页头卡读出伪得分，污染既有读面 |
| `gapfill_policy_eval_trend`（219） | 不归并块 1 | 219 行粒度是「维位置 × 指标名 × 一个对照值」，块 1 需要「维度键 × 当前分 × 权重」；语义与拣行键都不同 |
| `gapfill_policy_eval_partition`（220） | 不归并块 3、4、7 | 220 行是「对象 × 对照数 × 投向」，缺经纬度、代表政策、落实率四率、影响力四元组；写进去会作为地区行混进分区柱状/热力读面；给已签收的 VIZ-DATA 加列等于改签收稿 |
| `gapfill_policy_eval_shell`（224/225 壳表） | 不归并块 2 | 壳表行种类只有解读条目和多媒体条目（VIZ-ARCH §5.4 已收窄），画像不是解读条目 |
| `ads.policy_focus` / 全景分布类 ADS（DS-10） | 不归并块 3、5 | 全景分布、舆情动向是 DS-10 页读面；指标 yaml `seed_ids_not_this_page` 明确禁止本页借用 |
| `ads.policy_metric_timeseries` / `M_POLICY_IMPLEMENTATION_EFFECT` | 不归并块 4 | 落实率不是 IMPLEMENTATION_EFFECT 口径；该指标属 DS-12/POL-03，`metrics_not_consumed_from_pol06` 明确不进本页 |

七块与页面维度条（DimensionBar）无联动：`appliedDimensions` 只传入 219（TrendMetricsChart）和 220（RegionGroupCompare），七个可视化组件不接收维度 props。因此行上不设时间/区域/类别切换条件列；块内自带的行本键（地区名、话题名、统计月）见第 4 节。

本叶新建的表只有第 2 节的七张，都在 `gkxlumenx_gapfill`，表名都以 `gapfill_` 开头。本单只定列，不建库，不插入。不写 `gkxlumenx_ods`、`gkxlumenx_dwd`、`gkxlumenx_ads`，不写供应方库。

`gkxlumen-display` 不直连库。读方是展示链路 Java（`gkxlumen-element` 或等价只读服务），只读这七张表；入口形态本单不写 OpenAPI（待拍板，见第 8 节）。

## 2. 七张新表总览

命名沿用先例格式。这七个块没有 SRS 序号，`gap_item` 用「`DS11-VIZ ` + Tab1 块名」，与 DS12 先例「序号 叶子名」同构。

| 表 | 块 | `gap_item` 固定值 | `metric_id` |
|---|---|---|---|
| `gapfill_policy_eval_viz_metric` | 块 1 | `DS11-VIZ 评估指标体系卡` | 留空 |
| `gapfill_policy_eval_viz_portrait` | 块 2 | `DS11-VIZ 三联画像` | 留空 |
| `gapfill_policy_eval_viz_geo` | 块 3 | `DS11-VIZ 地理分布图` | 留空 |
| `gapfill_policy_eval_viz_region_impl` | 块 4 | `DS11-VIZ 分地区落实率` | 留空 |
| `gapfill_policy_eval_viz_topic_heat` | 块 5 | `DS11-VIZ 话题热力图` | 留空 |
| `gapfill_policy_eval_viz_topic_sentiment` | 块 6 | `DS11-VIZ 情感分布` | 留空 |
| `gapfill_policy_eval_viz_bubble` | 块 7 | `DS11-VIZ 产业影响力气泡图` | 留空 |

每张表建表时必须显式 `CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci`（D19；等值拣行键如 `region_name`、`topic_name` 不得依赖库默认排序规则）。建表语句由灌数单 `POL-L2-DS11-VIZ-GAPFILL-L02` 落地。本单不执行该单，也不在这里给出可执行脚本。

D16 行级列与先例一致：`metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`，外加 `is_mock=1`。`is_mock` 恒 1，D4 仍是 `mock`，不把缺项行写成已上线。`fill_method` 固定 `manual`，因此不设 `fill_model`。谁写：灌数单里的 Python 脚本。谁读：仅展示功能验收链路的 Java 只读服务。生产配置不读 `gkxlumenx_gapfill`。本叶不把读到的行写入 ADS，因此不产生 `gapfill_` 前缀的 `calc_batch_id`。

种类用不到的列留空，写 NULL，不写空字符串。同表唯一性由灌数单保管（见各表），本单不写唯一索引语句。

## 3. 拣行键与请求参数的映射

七块当前都是**无用户选择条件的直读块**：组件不接收页面筛选 props，维度条不联动（第 1 节）。因此本单的拣行语义是：

- 一次请求只读**一个块**的行：按 `gap_item` 等值拣（或按入口种类等价限定）。七块互不混读，一次响应不拼两个块的行。
- 无更多条件时返回该块全部行；条件对不上则该块空，不补默认行。
- 各表已保留块内自然拣行键，供后续 FE 加筛选时不改表：块 3 `region_name`、块 5 `topic_name` + `stat_month`（支持月份等值/范围）、块 6 `scope_kind` + `topic_name`、块 7 `category`。当前 FE 未提交这些条件，不参与过滤。
- 查询不插入行来凑数。表没建、或建了但没有行，该块保持 FIX-03 的诚实空态。

前端渲染常量不落列、不参与拣行：块 1 雷达 max=100 与进度条色阶、块 3 visualMap 色带、块 4 落实率色阶（88/80/75）与延期项红标阈值（>10）、块 5 visualMap（50–100）与月份标签、块 6 柱图/环形配色、块 7 轴范围（60–100）与类别配色。这些是前端渲染规则，灌数行不带。

## 4. 逐表列清单与行内容范式

每小节先列（列名/类型/空/约束与语义），后写行内容范式：灌数行要含哪些语义，与 FE 组件消费字段一一对应。

### 4.1 `gapfill_policy_eval_viz_metric`（块 1 评估指标体系卡）

一行是一个评估指标维度：维度键、中文名、当前评估分、权重。列表与雷达读同一批行（雷达 indicator=行上中文名，value=当前评估分）。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `dim_key` | varchar(64) | 否 | 维度键（FE `key`）。词表来自行本身，不另编闭集 |
| `dim_label` | varchar(128) | 否 | 维度中文名（FE `label`；雷达 indicator name） |
| `score_value` | decimal(5,2) | 否 | 当前评估分，0–100（FE `value`；雷达值、进度条 percent） |
| `weight_pct` | decimal(5,2) | 否 | 权重百分比（FE `weight`）。语义挂 QPOL-02 权重未确认（PE-B01），行级标记见 `pending_ref` |
| `pending_ref` | varchar(64) | 是 | 待确认引用。灌数行写 `QPOL-02`。仅本表设此列：权重是已登记的甲方决策项，其余六表无此债务 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空。见第 5 节 |
| `gap_item` | varchar(128) | 否 | 固定 `DS11-VIZ 评估指标体系卡` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写 |
| `generated_at` | datetime | 否 | 行写入时间。由灌数单填写 |

唯一性：同一 `dim_key` 只一行。

行内容范式：每行含维度键、维度名、一个 0–100 当前分、一个权重百分数。演示种子五维（覆盖广度/深度力度/协同程度/实施效果/创新引领）是行语义示例，灌数单按同语义灌行，行数不少于维度闭环所需（种子为 5 维）。不灌页头聚合分：效果评分聚合在 `gapfill_policy_sim_score`（页头卡读面），本表不放总分行。

### 4.2 `gapfill_policy_eval_viz_portrait`（块 2 政策/企业/人才画像）

一行是一类画像对象：卡面字段 + 抽屉详情的展示原文。卡与抽屉读同一行。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `portrait_type` | varchar(16) | 否 | 只有 `政策`、`企业`、`人才`（FE `type` 三闭集；与 WF 第 6 列 `portrait_type` 对上） |
| `title` | varchar(128) | 否 | 卡题（FE `title`） |
| `subtitle` | varchar(256) | 是 | 副题（FE `subtitle`） |
| `summary_text` | text | 否 | 卡面摘要一段（FE `summary`） |
| `kpi_label` | varchar(128) | 否 | KPI 名（FE `kpi.label`） |
| `kpi_value` | decimal(18,4) | 否 | KPI 数值（FE `kpi.value`）。展示数值，不做指标口径声明 |
| `kpi_unit` | varchar(32) | 否 | KPI 单位（FE `kpi.unit`），如 `分` |
| `tags_text` | text | 是 | 若干个标签（FE `tags[]`），组数不固定，写在同一行 |
| `detail_overview` | text | 是 | 抽屉概述一段（FE `detail.overview`） |
| `detail_metrics_text` | text | 是 | 抽屉指标若干组「标签、值」（FE `detail.metrics[]`，值是展示原文可含单位），组数不固定 |
| `detail_highlights_text` | text | 是 | 抽屉要点若干条（FE `detail.highlights[]`），条数不固定 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空 |
| `gap_item` | varchar(128) | 否 | 固定 `DS11-VIZ 三联画像` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次 |
| `generated_at` | datetime | 否 | 行写入时间 |

唯一性：同一 `portrait_type` 只一行（三行一组：政策、企业、人才）。

行内容范式：三类各一行。行是展示原文（摘要、要点、指标组），不是解析行，不存画像正文文件。不灌 `detail` 之外的演示交互（MockBadge/抽屉开合是前端行为）。

### 4.3 `gapfill_policy_eval_viz_geo`（块 3 地理分布图）

一行是一个地区上的政策分布点：地区名、政策量、经纬度、代表政策名。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `region_name` | varchar(128) | 否 | 地区名（FE `name`；tooltip 首行）。一段名称，不拆省/市/区编码列，不建区划字典（先例 §5） |
| `policy_count` | int | 否 | 该地区政策量（FE `value`；visualMap 与气泡大小） |
| `lng` | decimal(10,6) | 否 | 经度（FE `coord[0]`）。effectScatter 落点必需 |
| `lat` | decimal(10,6) | 否 | 纬度（FE `coord[1]`） |
| `sample_policies_text` | text | 是 | 代表政策名若干个（FE `policies[]`；tooltip 顿号连接），个数不固定 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空 |
| `gap_item` | varchar(128) | 否 | 固定 `DS11-VIZ 地理分布图` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次 |
| `generated_at` | datetime | 否 | 行写入时间 |

唯一性：同一 `region_name` 只一行。

行内容范式：每行一个地区点。不灌种子里的 `flows` 政策流向连线——当前 FE 组件不消费 flows（只渲染 regions），本单不为未消费数据定列。不灌地图文件、geojson、对象存储键：底图走仓内 mapRegistry 静态资源，与行数据无关。

### 4.4 `gapfill_policy_eval_viz_region_impl`（块 4 分地区落实率）

一行是一个地区的四个落实数字。表格行与色阶读同一批行。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `region_name` | varchar(128) | 否 | 地区名（FE `region`；row-key）。与块 3 的 `region_name` 是同一业务键但不同表，不建外键 |
| `implement_rate` | decimal(5,2) | 否 | 落实率%（FE `rate`；进度条 + 色阶前端渲染） |
| `funded_rate` | decimal(5,2) | 否 | 资金到位%（FE `funded`） |
| `declared_rate` | decimal(5,2) | 否 | 申报完成%（FE `declared`） |
| `delayed_count` | int | 否 | 延期项数（FE `delayed`；>10 红标为前端渲染） |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空 |
| `gap_item` | varchar(128) | 否 | 固定 `DS11-VIZ 分地区落实率` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次 |
| `generated_at` | datetime | 否 | 行写入时间 |

唯一性：同一 `region_name` 只一行。

行内容范式：每行一个地区四率。排序（落实率降序/延期项降序）是前端表格行为，不落排序列。不借 `M_POLICY_IMPLEMENTATION_EFFECT` 时序口径（见第 1 节归并裁定与第 5 节）。

### 4.5 `gapfill_policy_eval_viz_topic_heat`（块 5 话题热力图）

一行是一个话题在一个月上的热度值。FE 的 `topics[]`/`months[]`/`values[ti][mi]` 矩阵由行集组装：话题集 = `topic_name` 去重，月份集 = `stat_month` 去重排序，格子 = 行上热度值。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `topic_name` | varchar(128) | 否 | 话题名（FE `topics[]` 项）。词表来自行本身，不另编闭集 |
| `stat_month` | varchar(7) | 否 | 统计月，`YYYY-MM`（FE `months[]` 项）。格式由灌数单保证 |
| `heat_value` | decimal(5,2) | 否 | 该话题该月热度（FE `values[ti][mi]` 单格；visualMap 前端渲染） |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空 |
| `gap_item` | varchar(128) | 否 | 固定 `DS11-VIZ 话题热力图` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次 |
| `generated_at` | datetime | 否 | 行写入时间 |

唯一性：同一 `topic_name` × 同一 `stat_month` 只一行。话题 × 月份不要求满矩阵：缺格 = 该格无值，FE 组装按行集事实，不补 0。

行内容范式：话题 × 月份展开成行。不迁整块种子矩阵常量到单格文本。月份范围拣行已可支撑（第 3 节），当前 FE 无筛选则全量读。

### 4.6 `gapfill_policy_eval_viz_topic_sentiment`（块 6 情感分布）

一行是一份情感构成：总体一行（环形图），或一个话题一行（堆叠柱）。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `scope_kind` | varchar(16) | 否 | 只有 `总体`、`分话题`。总体行喂环形图，分话题行喂堆叠柱 |
| `topic_name` | varchar(128) | 是 | 分话题行必填（FE `byTopic[].topic`）；总体行留空 |
| `positive_pct` | decimal(5,2) | 否 | 正面占比%（FE `positive`） |
| `neutral_pct` | decimal(5,2) | 否 | 中性占比%（FE `neutral`） |
| `negative_pct` | decimal(5,2) | 否 | 负面占比%（FE `negative`） |
| `sample_size` | bigint | 是 | 样本量。仅总体行必填：占比的口径支撑（D9 诚实性，ⓘ 用）；分话题行留空。FE 暂未渲染此列，不为渲染设列，为口径留证 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空 |
| `gap_item` | varchar(128) | 否 | 固定 `DS11-VIZ 情感分布` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次 |
| `generated_at` | datetime | 否 | 行写入时间（≈种子 `updatedAt` 语义，不另设时间列） |

唯一性：`scope_kind=总体` 只一行；同一 `topic_name` 的分话题行只一行。`scope_kind=总体` 时 `topic_name` 必空，`scope_kind=分话题` 时必填。三列占比合计应约 100，由灌数单自检保证。

行内容范式：总体一行 + 各话题一行。样本量只随总体行。种子 `updatedAt` 不迁：行写入时间即数据时间。

### 4.7 `gapfill_policy_eval_viz_bubble`（块 7 产业影响力气泡图）

一行是一个产业气泡：名称、类别、影响力、关注度、资金投入、增长率。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `bubble_name` | varchar(128) | 否 | 气泡名（FE `name`；label 与 tooltip 首行） |
| `category` | varchar(64) | 否 | 类别（FE `category`）。词表不编闭集：图例 = 行上 `category` 去重，不设 categories 表或列 |
| `influence_value` | decimal(5,2) | 否 | 影响力（FE x 轴 `influence`） |
| `attention_value` | decimal(5,2) | 否 | 关注度（FE y 轴 `attention`） |
| `funding_amount` | decimal(18,4) | 否 | 资金投入，亿元（FE `funding`；气泡大小） |
| `growth_rate` | decimal(5,2) | 否 | 增长率%（FE `growth`；tooltip） |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空 |
| `gap_item` | varchar(128) | 否 | 固定 `DS11-VIZ 产业影响力气泡图` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次 |
| `generated_at` | datetime | 否 | 行写入时间 |

唯一性：同一 `bubble_name` 只一行。

行内容范式：每行一个产业四元组 + 类别。注：FE 色板目前含 `科技/产业/前沿` 三个键，灌数行若用新类别值，颜色回退 series 默认色（本单不改代码，展示语义无损）；类别词表从行上长出来。轴范围与颜色映射不落列。

## 5. `metric_id` 引用裁定

只允许引用既有 metric，不新造。DS-11 页面 yaml（`DS-11-POLICY-EVAL.yaml`）里本页既有可引用指标为：`M_POLICY_EFFECT_SCORE`、`M_POLICY_FOCUS_INDEX`、`M_POLICY_SHORTBOARD_COUNT`、`M_POLICY_OPPORTUNITY_COUNT`、`M_POLICY_LAYOUT_REC_COUNT`（TRACE/WF mapped 五枚），以及 `M_POLICY_DS_11_POLICY_EVAL_012`、`M_POLICY_DS_11_POLICY_EVAL_015`（missing 两枚）。

**七张表的 `metric_id` 全部留空**：

- 七块在 yaml 里全部是 `metric_id: null` 的壳（PE-D05–D11、D16、D17 一类的 other_system / n/a_ops 壳判定逻辑同理），且 `wireframe_col6_non_metric` 已明确登记 `geo_region_value`、`implementation_rate`、`sentiment_pos/neu/neg`、`portrait_type` 为非指标列——本单七块的行正是这些非指标列的行级落地。
- EFFECT_SCORE 等五枚是页头卡与 223/227 读面的指标，七块的图表值不是它们的口径；把指标 ID 抄上壳行会伪造 D9 血缘。
- `M_POLICY_DS_11_POLICY_EVAL_012/015` 是摘要、路径风险的 missing A 类，与七块无关。
- 禁止为了填满该列，把 DS-10 全景分布类（`M_POLICY_NATIONAL_DIST` / `M_POLICY_SZ_DIST` / `M_POLICY_TOTAL_COUNT` 等 `seed_ids_not_this_page` 名单）或 DS-12 的 `M_POLICY_IMPLEMENTATION_EFFECT` 抄到这七张表上。

## 6. 灌数单

灌数单 `POL-L2-DS11-VIZ-GAPFILL-L02` 依赖本单。执行人 `data-agent`，监管 `human:淮政玮`。registry 建单/认领由主会话统一收口，本单不碰 MCP、不认领、不执行、不建库、不插入行、不改任何任务注册字段。

执行时建表按第 2 节（D19 字符集），行按第 4 节。最少内容：

| 表 | 灌数单以后要灌 | 不灌 |
|---|---|---|
| `…_viz_metric` | 评估指标维度行若干（≥ 维度闭环所需），每行键/名/分/权重 + `pending_ref=QPOL-02` | 页头总分行（归 `gapfill_policy_sim_score`）、权重词表闭集 |
| `…_viz_portrait` | 政策、企业、人才各一行，卡面 + 抽屉详情展示原文 | 画像正文文件、解析行、第四类画像 |
| `…_viz_geo` | 地区行若干，每行名/政策量/经纬度/代表政策名 | 种子 `flows` 连线、geojson、地图文件、对象键、「全国」兜底行 |
| `…_viz_region_impl` | 地区行若干，每行四率一延期数 | 色阶阈值列、排序列 |
| `…_viz_topic_heat` | 话题 × 月份热度行（话题集、月份集自定，允许非满矩阵） | 整块矩阵 JSON、visualMap 常量列、话题词表闭集 |
| `…_viz_topic_sentiment` | 总体一行（带样本量）+ 分话题行若干 | 每话题样本量（FE 未消费）、`updatedAt` 列 |
| `…_viz_bubble` | 产业气泡行若干，每行四元组 + 类别 | 轴范围列、类别配色表、categories 独立行 |

七张表行全部 `is_mock=1`、`fill_method=manual`、`gapfill_batch_id` 由灌数单生成、`metric_id` 留空。查询请求不调用灌数单。空表返回空。

## 7. 跨项只写消费边界

| 序号或资源 | 边界 |
|---|---|
| `gapfill_policy_sim_score`、页头六卡（FIX-01） | 页头得分读面不动。块 1 不写总分行进本表，页头卡不读七张 viz 表 |
| `gapfill_policy_eval_trend` / `partition` / `template`（219/220/222） | 已定稿三张表不加列、不混入七块行。七张 viz 表与它们互不读写 |
| `gapfill_policy_eval_shell`（224/225）、`gapfill_policy_eval_scheme`（227–231） | 壳表与方案表不承接七块。画像不是解读条目，气泡不是方案对照 |
| `evaluation/counts`、`jobs` 上的焦点/摘要/路径 | 223/226/229 读面不动，不与七块共用一次请求 |
| `ads.policy_focus`、全景分布类 ADS | DS-10 读面留在 DS-10。块 3、5 不借全景分布与舆情动向行 |
| `M_POLICY_IMPLEMENTATION_EFFECT` | 块 4 不借。该指标属 DS-12/POL-03 |
| `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` | 与七块无关（221 跨项照旧） |
| 维度条（DimensionBar） | 只作用 219/220。七块行不设维度切换条件列 |
| `POL-L2-DS11-VIZ-API` | 入口与参数名由该单（或其修订）定；本单只定表与拣行键语义 |
| `GDF-POLICY-MOCK-GATE-L01` | 与七张表无关，本单不改那道闸门 |

## 8. 与 ARCH 的悬置点（需人拍板，本单不自行决策）

1. **读面入口 ✅ 已裁定（2026-11-12 03:48 监管人 human:淮政玮 拍板 = ③）**：三个候选曾为 ① `evaluation/jobs` 扩七种 kind；② 复用 `analysis/dataset` 读面；③ 新独立资源。**裁定 ③**：display `PolicyEvaluationController` 加 `GET /v1/policy/evaluation/viz`（`block` 参数收七块）→ element `PolicyGapfillController` 加 `@Inner @GetMapping("/evaluation/viz")`（BE 侦察笔记 §3 落点）。ARCH 边界说明：`/evaluation/viz` 是既有 `/evaluation` 读面的子路径扩展（与 counts/shells/jobs 并列），不是 `/display/v1/policy` 下第 4 条并列路径，不触 VIZ-ARCH「不加第 4 条路径」红线；如架构师复核有异议再修订。API 契约与 FE 接线按 ③ 落地（BE 笔记、FE 接线说明书均已按 ③ 写好落点）。本单七张表与拣行键在 ③ 下成立，无需改列。
2. **`gap_item` 命名格式**：块无 SRS 序号，本单自定「`DS11-VIZ ` + 块名」。若监管人要求改用编号格式（如 `DS11-VIZ-GB1…GB7`），灌数单开工前改第 2 节即可，不影响列设计。
3. **块 1 权重的 QPOL-02 升格路径**：本单把权重行留 `metric_id` 空并挂 `pending_ref=QPOL-02`。若甲方确认指标体系与权重（QPOL-02 关闭）后，维度分是否升格为 `M_POLICY_EFFECT_SCORE` 的维度行、或是新注册指标体系，属后续修订，本单不预设。
4. **七块的需规定位**：七块是 demo 复刻保留块，不在需规十三叶原文。MOCKAUDIT 结论「如需恢复数据，须先立 DATA 单」即本单；灌数灌什么内容、真实性边界（演示口径 vs 真实统计）由灌数单执行时与监管人确认，本单只定列与行语义形状。

## 9. 明确不做

- 不写可执行 SQL，不建库，不灌数，不跑脚本。
- 不重开 GDF，不写 nGQL，不加 ODS、DWD、ADS 表，不写供应方库。
- 不改已定稿的 `gapfill_policy_eval_trend` / `partition` / `template` 列，不把七块行写进任何既有表（污染既有读面）。
- 不新造 `metric_id`，不改 D4，不把缺项行写成已上线。七张表 `metric_id` 留空。
- 不灌种子 `flows` 连线、地图文件、geojson、对象存储键、画像正文文件。
- 不落前端渲染常量（色阶、轴范围、visualMap、类别配色）为列。
- 查询不插入。空态是空，不写成 501。列清单不是可执行 SQL。
- 不改 MOCKAUDIT 盘点表、VIZ-ARCH、VIZ-DATA、指标分册、说明书、WBS。
- 不碰 task-registry MCP（主会话统一收口）；本单不 commit 不 push（主会话收口）。
- 不认领 `POL-L2-DS11-VIZ-GAPFILL-L02` 灌数单。
- 不把本单标成 done 或 ready_to_sign。
