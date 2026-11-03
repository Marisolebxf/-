# POL-L2-DS10-TREND-DATA · 科创政策全景 · 政策动向跟踪 · 数据落点

- 任务：`POL-L2-DS10-TREND-DATA`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`（已认领，本单不再认领）
- 强度：ponytail off（定义任务，定列，不缩文档）
- 上游架构：`POL-L2-DS10-TREND-ARCH` 第 7.3 节（禁止修改）。本单只定列，不改那份架构，不改图。

本叶只定科创政策全景二级「政策动向跟踪」的数据落点。SRS 序号 **203–206**。用户故事 `US-DS-POL-02`。不写 SQL，不写 DDL，不写代码，不写 OpenAPI。不建表，不灌数，不跑数据库。

上游只引用，不改写：架构第 7.3 节、说明书第 11.1 节动向一行、`data-lineage-policy.md` §2.4、派单包 `GDF-POLICY-WORKPACK-v2/17-指标离线加工-POLICY-MDC.md`、`storage/POLICY/stores/mysql/ads.md` 里已登记的统计表。不新造 `metric_id`，不改 D4。不重开 GDF。

灌数执行单是 `POL-L2-DS10-TREND-GAPFILL-L01`（仍是 backlog）。本单不认领、不执行。本单不把任务标成 done。

## 1. 范围

| 序号 | 叶子 | 数据角色 | 本单 |
|---|---|---|---|
| 203 | 政策来源监控与更新 | 读第 6 项已有入库 | 不加表，不加字段 |
| 204 | 政策订阅服务 | 专题门面持有订阅 | 不落展示库，不建缺项表，不灌假订阅 |
| 205 趋势 | 重点领域政策分析 · 趋势 | 读已有时序统计表 | 不另建缺项表，不往 ADS 写 mock |
| 205 热点 | 热点识别 | `gapfill_policy_trend_hotspot` | 只定列 |
| 205 影响 | 政策影响评估 | `gapfill_policy_trend_impact` | 只定列 |
| 205 深度报告 | 深度分析报告 | `gapfill_policy_trend_report` | 只定列 |
| 206 时间、地域 | 时间轴、趋势、地域热力 | 读已有时序表和全国分布表 | 不另建缺项表，不往 ADS 写 mock |
| 206 主题 | 主题分布 | `gapfill_policy_theme_dist` | 只定列 |

库只允许 `gkxlumenx_gapfill`。四张缺项表不进 ODS、DWD、ADS，不写供应方库。D4 保持 mock。`GDF-POLICY-MOCK-GATE-L01` 不在本单解开。QPOL-07 不改。

205 的趋势、206 的时间与地域，不把点改灌进检索的 `gapfill_policy_qry_stat`。

## 2. 203 政策来源监控与更新

第 6 项已有入库列表，本单不新开表。

读已有资源：`GET /display/v1/policy/panorama/ingest`。链路仍是前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → 第 6 项已有入库结果。加工在第 6 项。`GDF-POLICY-WORKPACK-V2-L01` 已完成，`GDF-POLICY-MDC-DOC-L01` 为 integration。本单不重开这些包。

政策 GDF 派单包与已签收的 `ads.md` 没有另点名一张「来源监控入库」表。本单不编造 ADS 表名，不加字段。打开一条详情仍走全景已有 `{id}/detail`，本单不新开详情表。来源监控没有 `metric_id`，本单不新造。无入库行则列表空，不造行。

## 3. 204 政策订阅服务

不落展示库，不建缺项表，不灌假订阅。

订阅条件（类别、领域、部门、地区、日/周/月、通知/邮件/短信）由 `gkxlumen-topic-policy` 持有。`gkxlumen-display` 只委托，不保存订阅关系，不把订阅写进 `gkxlumen-element` 或 ADS。本单不设计订阅表，不写订阅列。说明书第 11 节写明订阅条件不灌假记录。

实现单是 `E-E7-POLICY-M1-L11`、`L12`、`L13`。本单不认领。没有订阅则空列表。页面 localStorage 不是这条记录。

## 4. 205 趋势 · 206 时间与地域

不另建缺项表。不往 ADS 写 mock。已有表没有行则对应图空，不造 0。

| 读什么 | 指标 | 已有落点 | 源 |
|---|---|---|---|
| 205 趋势；206 时间轴和趋势 | `M_POLICY_TIMESERIES` | `gkxlumenx_ads.policy_timeseries` | 架构已写源表 `dwd_policy_base`。结果表以派单包 17 与 `ads.md` 为准 |
| 206 地域热力 | `M_POLICY_NATIONAL_DIST` | `gkxlumenx_ads.policy_national_dist` | 派单包 17 与 `ads.md`。不另开地域指标 |

时序只沿已有列读：`period_type`、`period_key`、`publish_count`。派单包 17 第一批只写年行，`growth_rate`、`continuity_rate` 留空。本单不加列。重点领域名称只作为 `stats` 的筛选条件，不新造「科创发展时序」「人才引进时序」「资金扶持时序」。

地域只沿已有列读：`province` 分组已落在 `province_name`、`policy_count`。派单包 17 把 `province_code`、`yoy`、`center_lng`、`center_lat` 留空。本单不加列。

两条都是 STAT，D1 aligned，D4 mock。D2 为 provisional 时保留「待核验」。本单不改这四维，不把 mock 写成已上线。展示链不直查供应库 `dwd_policy_base`，读的是上表已登记的 ADS 结果。

## 5. 四张缺项表

只定下面四张，与架构第 7.3 节、说明书第 11.1 节动向一行相同。列由本单定。行由 `POL-L2-DS10-TREND-GAPFILL-L01` 灌。本单不建表，不写一行。

热点、影响、深度报告由 `gkxlumen-element` 在 `POST /display/v1/policy/panorama/jobs` 上按种类读表，原样返回行。这三种不进 Python，不进 `gkxlumen-topic-async-service`。主题分布挂在 `stats` 上，由 element 读 `gapfill_policy_theme_dist`。display 不组装报告，不生成主题桶。

表无行则该块空，不造 0，不在接口里写死报告。

### 5.1 行上必有的 D16 列

四张表相同。对齐 `data-lineage-policy.md` §2.4 与架构第 7.3 节。`fill_method` 固定 `manual`，不调用模型，所以不设 `fill_model`，也不填这个字段。

| 列 | 类型 | 空 | 本单怎么定 |
|---|---|---|---|
| `metric_id` | varchar(128) | 空 | 留空（NULL）。这四张没有已挂指标。不新注册 |
| `gap_item` | varchar(64) | 非空 | 写序号和叶子名。见各表，灌数单不得改成别的叶子 |
| `fill_method` | varchar(16) | 非空 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 非空 | 列留给定。具体批次由灌数单填写。本单不赋值 |
| `generated_at` | datetime | 非空 | 列留给定。写入时刻由灌数单填写。本单不赋值 |

不设热度分、实施效果分、推演情景、文件路径、对象存储键、政策类型列。

引擎若要求主键，灌数单只能加与业务无关的自增行号。本单不把行号当业务列，本单不写 DDL。

### 5.2 `gkxlumenx_gapfill.gapfill_policy_trend_hotspot`

叶子：205 热点识别。`gap_item` 固定 `205 热点识别`。

科创发展、人才引进、资金扶持各若干条。领域名写在行上，不是三条新指标。不挂 `M_POLICY_FOCUS_INDEX`。

| 业务列 | 类型 | 空 | 放下什么 |
|---|---|---|---|
| `domain_name` | varchar(64) | 非空 | 领域名 |
| `hotspot_name` | varchar(128) | 非空 | 热点名称 |
| `brief` | varchar(512) | 非空 | 一句说明 |

不放：热度分、焦点指数，以及任何分数字段。

### 5.3 `gkxlumenx_gapfill.gapfill_policy_trend_impact`

叶子：205 政策影响评估。`gap_item` 固定 `205 政策影响评估`。

上述三个领域各一条。不挂 `M_POLICY_IMPLEMENTATION_EFFECT`、`M_POLICY_SIMULATE`。

| 业务列 | 类型 | 空 | 放下什么 |
|---|---|---|---|
| `domain_name` | varchar(64) | 非空 | 领域名 |
| `impact_object` | varchar(128) | 非空 | 影响对象 |
| `impact_direction` | varchar(64) | 非空 | 影响方向。文本，本单不规定枚举 |
| `conclusion` | varchar(512) | 非空 | 一句结论 |

不放：实施效果分、推演情景。

### 5.4 `gkxlumenx_gapfill.gapfill_policy_trend_report`

叶子：205 深度分析报告。`gap_item` 固定 `205 深度分析报告`。

上述三个领域各一份。正文在行里。不挂序号 211 的评估报告、序号 217 的对标报告，也不挂核增研报。

| 业务列 | 类型 | 空 | 放下什么 |
|---|---|---|---|
| `title` | varchar(256) | 非空 | 标题 |
| `domain_name` | varchar(64) | 非空 | 领域名 |
| `body` | text | 非空 | 正文。写在这一列，不另存文件 |

不放：文件路径、桶名、对象键。不写对象存储。

### 5.5 `gkxlumenx_gapfill.gapfill_policy_theme_dist`

叶子：206 主题分布。`gap_item` 固定 `206 主题分布`。

若干主题名和件数。不新造主题指标。不读、不抄 `policy_type_dist`，不用 `policy_type` 冒充主题。QPOL-01 未闭合，类型分布的桶不是这一维。

| 业务列 | 类型 | 空 | 放下什么 |
|---|---|---|---|
| `theme_name` | varchar(128) | 非空 | 主题名 |
| `item_count` | int | 非空 | 件数 |
| `stat_year` | smallint | 可空 | 年份。无年份则 NULL |

不放：政策类型、占比、同比，以及 `policy_type_dist` 上的桶。

## 6. 本单不灌数

本单不 INSERT，不写脚本，不连库，不建表。

要灌的内容已经写在架构第 7.3 节，执行单是 `POL-L2-DS10-TREND-GAPFILL-L01`：

| 表 | 灌数单要写的行 | 不灌 |
|---|---|---|
| `gapfill_policy_trend_hotspot` | 科创发展、人才引进、资金扶持各若干条 | 焦点指数、热度分 |
| `gapfill_policy_trend_impact` | 三个领域各一条 | 实施效果分、推演情景 |
| `gapfill_policy_trend_report` | 三个领域各一份。正文在 `body` | 文件、对象存储 |
| `gapfill_policy_theme_dist` | 若干主题名和件数，年份可空 | 政策类型分布的桶 |

那张单仍是 backlog。本单不认领、不执行。接口只读表，不在返回语句里写 mock。D4 保持 mock。

## 7. 明确不做

- 不写 SQL，不写 DDL，不写代码，不写 nGQL，不跑数据库。
- 不建表，不灌数，不把四张缺项表放进 ODS、DWD、ADS 或供应方库。
- 不新开 GDF，不加已有表的字段，不往 ADS 写 mock 点数。
- 不新造 `metric_id`，不改 D4，不闭合 QPOL-07，不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 不把 203 编成一张新的 ADS 表名。
- 不给 204 建缺项表，不灌假订阅，不认领 `E-E7-POLICY-M1-L11` / `L12` / `L13`。
- 不设 `fill_model`。不把热点改挂焦点指数，不把影响改挂实施效果或推演，不把深度报告改挂 211、217。
- 不改架构稿、说明书、WBS、注册表、调研分册、`ads.md`。
- 不把本单标成 done。不写会签结论。
