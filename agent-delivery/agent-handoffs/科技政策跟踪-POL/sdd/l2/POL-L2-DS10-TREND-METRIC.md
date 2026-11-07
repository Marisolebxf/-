# POL-L2-DS10-TREND-METRIC · 科创政策全景 · 政策动向跟踪 · 后台指标设计

- 任务：`POL-L2-DS10-TREND-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`（已认领，本叶不再认领）
- 强度：ponytail off（定义任务，不缩文档）
- 查询：2026-11-03 经 MCP `metric-get`。未读 seed、矩阵 YAML，未改注册表

本叶只写科创政策全景二级「政策动向跟踪」的指标挂接。SRS 序号 **203–206**。用户故事 `US-DS-POL-02`。

上游只引用，不改写：`sdd/l2/POL-L2-DS10-TREND-ARCH.md`、说明书第 11 节、说明书第 2 节 DS-10 里 203–206 四行。不新注册指标，不改 D4，不闭合 QPOL-07，不写算法实现，不写 OpenAPI。

## 1. 范围

四叶都在全景动向工作区里完成。挂接以 2026-11-03 已签收的动向架构和说明书第 11 节为准。

| 序号 | 叶子 | 本叶 |
|---|---|---|
| 203 | 政策来源监控与更新 | 没有 `metric_id`。不新造。跨项索引，读已有入库 |
| 204 | 政策订阅服务 | 不是指标。不新造。不建缺项表 |
| 205 | 重点领域政策分析 · 趋势 | 只用已有 `M_POLICY_TIMESERIES`。数值从已有表读。D4 仍是 `mock` |
| 205 | 热点、影响、深度报告 | 没有已挂 `metric_id`。不新注册。读三张缺项表 |
| 206 | 时间轴、趋势 | 只用已有 `M_POLICY_TIMESERIES`。与 205 趋势同一条。D4 仍是 `mock` |
| 206 | 地域热力 | 只用已有 `M_POLICY_NATIONAL_DIST`。D4 仍是 `mock` |
| 206 | 主题分布 | 没有已挂 `metric_id`。不新注册。读 `gapfill_policy_theme_dist` |

科创发展、人才引进、资金扶持是筛选条件，写在 `stats` 的条件上，也写在缺项表的行上。本叶不把这三个名称写成三条新指标。

205 的趋势、206 的时间轴和地域热力，D4 仍是 `mock`。`GDF-POLICY-MOCK-GATE-L01` 本叶不写成已解开。闸门未解开时，正式值仍是 mock。无行则对应图空，不造 0。

## 2. 本二级用到的已有 metric_id

去重后 2 条。`metric-get` 均为 `found.seed=true`、`found.matrix=true`。`algorithm_type` 都是 STAT。D4 都是 `mock`。

| metric_id | 中文名 | 挂在 |
|---|---|---|
| `M_POLICY_TIMESERIES` | 政策时序指标 | 205 趋势；206 时间轴与趋势 |
| `M_POLICY_NATIONAL_DIST` | 全国政策分布 | 206 地域热力 |

这两条之外，本二级不新造 `metric_id`。

`stats` 上还读得到总数、类型、级别、深圳分布、有效率、行业覆盖、支持力度。它们分别留给检索、部门件数、标杆比对和没有序号的行业覆盖。本叶只读时序和全国分布，不改这条资源的其余挂接。`M_POLICY_TIMESERIES` 在检索叶序号 198 上已有挂接，本叶不拆掉那一处，205 与 206 按本指标已有需求来源继续用同一条。

## 3. 八件套

八件套只含身份：`metric_id`、中文名、口径、公式、`algorithm_type`、源表、源系统、更新频率、`version`。D1–D4、`lifecycle_stage`、`srs_refs` 不放进本节。

两条注册公式都是同一类过程指针：见 calc-logic「计算逻辑说明」与 20261021 正本 §二；公式是过程式复算，未浓缩为单行表达式；禁手抄，实现时以 `code/<metric_id>.py` 为准。本叶不手抄、不展开成可执行式，也不另写一条能算出数的式子。

源系统两条相同：`gkx @ 183.240.141.251:3318（只读）`。`version` 都是 `1`。源表都是 `dwd_policy_base`。更新频率都是 daily。

| metric_id | 中文名 | algorithm_type | 源表 | 更新频率 |
|---|---|---|---|---|
| `M_POLICY_TIMESERIES` | 政策时序指标 | STAT | `dwd_policy_base` | daily |
| `M_POLICY_NATIONAL_DIST` | 全国政策分布 | STAT | `dwd_policy_base` | daily |

口径按 `metric-get` 的 `kit.definition` 摘录，不改写：

| metric_id | 口径 |
|---|---|
| `M_POLICY_TIMESERIES` | 历史段（2015-01—2022-08）可以逐月复算；当前段（2022-09 之后）库内没有记录。可以发布历史趋势，不能单独承担需求里的「趋势监测」。注册判定为部分支持。连续性口径仍是 QPOL-07，本叶不闭合，也不改口径 |
| `M_POLICY_NATIONAL_DIST` | `province` 单列可归省，未归省可逐类拆开，合计与底表行数闭合。注册判定为完全转换支持 |

`extras.algo_server_location` 指向 demo 仓既有计算文件。那是注册表索引，不是本二级的展示调用链。本叶不改那些文件，也不把展示改去调 demo 服务。展示仍按架构稿：浏览器只打 `/display/v1/policy/**`。

## 4. 接入状态

接入状态不是八件套。下表来自 `metric-get` 的 `readiness`。两条 D1 都是 `aligned`，D2 都是 `partial` 且 `d2_assessed=provisional`（待核验），D4 都是 `mock`。本叶不改任何一维。D2 的 provisional 保留「待核验」，不在本叶改绿。

| metric_id | D1 | D2 | D3 | D4 |
|---|---|---|---|---|
| `M_POLICY_TIMESERIES` | aligned | partial，待核验 | partial | mock |
| `M_POLICY_NATIONAL_DIST` | aligned | partial，待核验 | full | mock |

`is_mock=true`。`d4_note` 写算法服务未上线，保持 mock。对齐前数值仍是 mock。本叶不改 D4。

需求来源不是八件套。沿用查询结果，本叶不改挂：

| metric_id | srs_refs | 本叶用法 |
|---|---|---|
| `M_POLICY_TIMESERIES` | 展示 02/205、02/206；专题 05/100 | 205 趋势，206 时间轴与趋势。同一条时序，不拆成按领域的新指标 |
| `M_POLICY_NATIONAL_DIST` | 05/100。说明里点到 206 热力 | 只挂 206 地域热力。不另开地域指标。不改挂评价页序号 219 |

## 5. 205 趋势、206 时间轴与地域怎么读

读面沿 `POL-L2-DS10-TREND-ARCH`，不新开路径。统计在已有 `GET /display/v1/policy/panorama/stats`。`gkxlumen-display` 内部委托沿用检索叶已经写明的 `stats`。本叶不另建一条统计查询，不在接口里造点。

### 5.1 205 趋势

只用 `M_POLICY_TIMESERIES`。数值从该指标已有源表 `dwd_policy_base` 经已有 `stats` 读出。不新建缺项表，不把这些点灌进检索的 `gapfill_policy_qry_stat`，不往 ADS 写 mock 点数。无点则趋势图空，不造 0。

重点领域名称只作为 `stats` 的筛选条件。不新造「科创发展时序」「人才引进时序」「资金扶持时序」。

历史段可以复算。2022-09 之后当前段库内没有记录，所以这条不能单独承担「趋势监测」已完全支持。QPOL-07 不闭合。D2 provisional 保留待核验。D4 仍是 `mock`。

### 5.2 206 时间轴与趋势

时间轴和趋势图用同一条 `M_POLICY_TIMESERIES`，与第 5.1 节同一次 `stats` 读取。不另建查询。无点则对应图空，不造 0。D2 provisional 保留待核验。D4 仍是 `mock`。

### 5.3 206 地域热力

只用 `M_POLICY_NATIONAL_DIST`。数值从该指标已有源表 `dwd_policy_base` 经已有 `stats` 读出。不另开地域指标，不新建缺项表，不把省行灌进 `gapfill_policy_qry_stat`。无省行则热力空，不造 0。D2 provisional 保留待核验。D4 仍是 `mock`。

评价页序号 219（多维指标趋势图）有自己的缺项表 `gapfill_policy_eval_trend`。本叶不把时序或全国分布改挂到 219。

## 6. 没有已挂指标的叶子

下列叶子本叶不新注册 `metric_id`，不写能算出数的公式。

### 6.1 203 政策来源监控与更新

没有 `metric_id`，本叶不新造。判定保持跨项索引：`GET /display/v1/policy/panorama/ingest` 读第 6 项已经落入 ADS 的入库列表和管线阶段。无入库行则列表空。本叶不把来源监控写成统计指标，不建缺项表，不在展示侧建抓取。

2026-11-07 变更（`POL-L2-DS10-SRCMON-SYNTH-L01`）：「立即同步」写入的 LLM 合成政策落在 DWD，`source_plane='domestic'`，检索和 205/206 的统计都计入（`human:淮政玮` 批准）。受此影响的已注册指标 D4 仍是 `mock`，不改。合成行可按 `source='llm-synth'` 识别，删除后统计回到只含真实政策的口径。

### 6.2 204 政策订阅服务

订阅条件（类别、领域、部门、地区，以及日/周/月和通知、邮件、短信）不是指标。本叶不新造 `metric_id`，不写公式，不把推送条数写成统计数。

签收后的说明书第 11 节写明：订阅条件不灌假记录，204 接通后走专题门面，不建缺项表。展示只委托 `gkxlumen-topic-policy`。没有订阅则空列表。本叶不建 `gapfill_` 表来充当订阅，也不把 501 写成这条的指标挂接。实现单 `E-E7-POLICY-M1-L11`、`L12`、`L13` 本叶不认领。

### 6.3 205 热点、影响、深度报告与 206 主题分布

这四块没有已挂 `metric_id`。2026-11-03 `metric-get` 未给它们分配 id。本叶不预占、不新注册。

读缺项表，表在库 `gkxlumenx_gapfill`。依据是说明书第 11.1 节动向一行，以及 `POL-L2-DS10-TREND-ARCH` 第 7.2–7.3 节。这几块不用 501 充当实现。接口经既有 Java 服务读表，原样返回行。无行则该块空，不造 0，不在返回语句里写死报告或主题桶。

| 结果 | 表 | `gap_item` |
|---|---|---|
| 205 热点识别 | `gapfill_policy_trend_hotspot` | `205 热点识别` |
| 205 政策影响评估 | `gapfill_policy_trend_impact` | `205 政策影响评估` |
| 205 深度分析报告 | `gapfill_policy_trend_report` | `205 深度分析报告` |
| 206 主题分布 | `gapfill_policy_theme_dist` | `206 主题分布` |

每行带 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。这四张没有已挂指标，`metric_id` 留空。`fill_method` 用 `manual`。`gap_item` 写上表的序号和叶子名。D4 保持 mock。读到的行不改判成已上线。

热点走 `POST /display/v1/policy/panorama/jobs`，由 `gkxlumen-element` 读前三张表。这三种不进 Python。主题分布挂在 `stats` 上，由 element 读 `gapfill_policy_theme_dist`。display 不生成主题桶，不借用类型分布冒充主题。

要灌的内容沿架构稿第 7.3 节：三个领域的热点名称和一句说明；影响对象、方向和一句结论；报告标题与正文；主题名和件数。不灌分数、文件、类型分布桶。列由 `POL-L2-DS10-TREND-DATA` 定，灌数由 `POL-L2-DS10-TREND-GAPFILL-L01` 执行。本叶不写列，不灌数，不认领这两张单。

重点领域名称仍是行上的筛选条件。科创发展、人才引进、资金扶持不是三条新指标。

## 7. 点名不挂

下列已注册指标本二级不改挂到 203–206，D4 保持 `mock`，本叶不改。

| metric_id | 注册身份（metric-get） | 不挂本二级的原因 |
|---|---|---|
| `M_POLICY_FOCUS_INDEX` | 政策焦点指数；MODEL；D1=`aligned`；D4=`mock`；需求来源在评价页（05/166，`DS-11-POLICY-EVAL`） | 评价页序号 223 的焦点指数。不改挂成 205 热点 |
| `M_POLICY_IMPLEMENTATION_EFFECT` | 落地实效性；MODEL；D1=`aligned`；D4=`mock`；需求来源含展示 02/209 | 序号 209 的实施效果。不改挂成 205 政策影响评估 |
| `M_POLICY_SIMULATE` | 政策效果推演；MODEL；D1=`aligned`；D4=`mock`；`srs_refs` 为空 | 推演页的推演模型。不改挂成 205 政策影响评估 |

序号 211 的效果评估报告、序号 217 的对标报告、核增研报 614–618，都不是 205 的深度分析报告。本叶不改挂。

`M_POLICY_TIMESERIES` 不改挂到评价页序号 219。`M_POLICY_NATIONAL_DIST` 不另开地域指标，也不改挂到 219。

## 8. 偏离

DoD 写「未注册模型保持 501」。这句话相对 2026-11-03 的架构签收已经过时。

说明书第 2 节和 `sdd/指标与501.md` 仍把 205 的热点、影响与深度报告写成 501。说明书开篇也写过「未注册模型保持 501」。说明书第 11.1 节与已签收的 `POL-L2-DS10-TREND-ARCH` 改为：这几块读 `gkxlumenx_gapfill` 的 `gapfill_` 表，接口只读行。本叶按签收写挂接。205 热点、205 影响、205 深度报告、206 主题分布不用 501 充当实现。

206 在 `指标与501.md` 整行写成可接统计读面，只点了时序和全国分布。主题分布没有已挂 `metric_id`。本叶不把主题并进这两条 STAT，改按第 11.1 节读 `gapfill_policy_theme_dist`。

204 在 `指标与501.md` 写成 501。本叶把它定为不是指标。第 11 节要求订阅走专题门面、不灌假记录。204 不建缺项表，也不把 501 写成指标挂接。

203 与说明书第 2 节一致：没有 `metric_id`，跨项索引，不新造。

本叶不改说明书、不改 `指标与501.md`、不改架构稿、不改注册表。两条已挂指标的 D4 保持 `mock`。

## 9. 明确不做

- 不新注册指标，不改 D4，不把 mock 写成已上线。
- 不闭合 QPOL-07，不改时序口径，不把 D2 provisional 改绿。
- 不把科创发展、人才引进、资金扶持写成三条新指标。
- 不给热点、影响、深度报告、主题分布、订阅、来源监控写能算出数的公式。
- 不改挂 `M_POLICY_FOCUS_INDEX`、`M_POLICY_IMPLEMENTATION_EFFECT`、`M_POLICY_SIMULATE`。
- 不把时序或全国分布改挂到评价页序号 219。
- 不把 501 充当 205 热点、影响、深度报告和 206 主题分布。
- 不改唐绍祖锁定的合规算法。本单不写算法实现，不改 demo 仓计算文件。
- 不重开 GDF，不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 不改说明书、调研分册、架构稿、注册表和指标 seed。
- 不写 OpenAPI 字段、请求体、响应体、枚举。不写代码。

2026-11-03 human:淮政玮 签收。不新造指标，D4 保持 mock，缺项块读表。
