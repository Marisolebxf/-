# POL-L2-DS10-SENT-SIGNOFF-DATA · 科创政策全景 · 政策舆情评估 · 数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS10-SENT-API`、`POL-L2-DS10-SENT-METRIC`、`POL-L2-DS10-SENT-DATA`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS10-SENT-ARCH` 第 8 节；`科技政策跟踪-系统详细设计说明书.md` 第 11.1 节舆情两行
- 范围：SRS 207–212
- 结论：**同意会签**

本页只核对三张分册的数据落点是否与架构第 8 节、说明书第 11.1 节舆情两行一致。不改已有文件，不改任务状态，不建库，不灌数。

## 核对

| 口径 | 三张分册 | 判定 |
|---|---|---|
| 207 不另建缺项表，复用检索叶 `gapfill_policy_qry_doc`、`gapfill_policy_qry_stat` | DATA 第 1–2 节：不另建、不第二套灌数、不执行 `POL-L2-DS10-QRY-GAPFILL-L01`、不读 `gapfill_policy_qry_rank`。正式行沿检索叶；无正式行读这两张。API 第 3 节与 METRIC 第 5.1 节与检索叶同一条 `stats` / `search` / `{id}/detail`，不另开表 | 一致 |
| 208 不建表 | DATA 第 3 节不建表、不把 `policy_graph_node` / `policy_graph_edge` 写成落点。API 第 4 节、METRIC 第 5.2 节不新开资源，只消费已有子图 | 一致 |
| 209 读已有 `policy_effect`（`scope_type=region_effect`）与 `policy_metric_timeseries`，不往 ADS 加列 | 三张分册表名相同。DATA 第 4 节列都落在已有列或已有 `ext`，写明不加列、不新增 `is_mock` 列。时序只读 `metric_id=M_POLICY_IMPLEMENTATION_EFFECT`。`policy_effect.metric_id` 仍是已有 `M_POLICY_EFFECT_SCORE`，本叶不改挂 | 一致 |
| 212 读已有 `policy_match`，不灌假推送 | 三张分册都读 `policy_match`。`M_POLICY_INDUSTRY_FIT` 与 `M_POLICY_MATCH` 同一张表、同一批行。DATA 第 7 节、API 第 6 节、METRIC 第 5.4 节都不建通知表、邮件表，不灌假通知、假邮件 | 一致 |
| 210 `gapfill_policy_audience_feedback`、211 `gapfill_policy_assessment_report`，只在 `gkxlumenx_gapfill` | API 第 2、7、8 节，METRIC 第 6 节，DATA 第 5–6 节库表名相同。DATA 定列：`metric_id` 可空且留空，`gap_item` 为 `210 政策受众反馈收集` / `211 政策效果评估报告`，`fill_method` 固定 `manual`，另有 `gapfill_batch_id`、`generated_at` | 一致 |
| 不写 ODS / DWD / ADS / 供应方库；三张灌数单未执行；查询不灌数；空表返回空；接口不直接返回 mock | 210、211 的行只进 `gkxlumenx_gapfill`。209、212 不另建 ADS 表、不加列，写入仍是以后的 `POL-L2-DS10-SENT-MOCK-ADS` 调用已有 `run()`。DATA 第 8 节写明 `MOCK-ADS`、`MOCK-210`、`MOCK-211` 本单不执行。API、METRIC 不执行灌数。无行则空，查询不插入，接口不返回写死的 mock | 一致 |

## 库表名

| 序号 | DATA | API | METRIC |
|---|---|---|---|
| 207 | `gkxlumenx_gapfill.gapfill_policy_qry_doc`、`gapfill_policy_qry_stat`（复用，不另建） | 与检索叶同一条读面，不另点一张新表 | 同 API，不另点一张新表 |
| 208 | 无表 | 无表 | 无表 |
| 209 | `demo_gkxlumenx_ads.policy_effect`、`policy_metric_timeseries` | `ads.policy_effect`、`ads.policy_metric_timeseries` | 同 API |
| 210 | `gkxlumenx_gapfill.gapfill_policy_audience_feedback` | 同左 | 同左 |
| 211 | `gkxlumenx_gapfill.gapfill_policy_assessment_report` | 同左 | 同左 |
| 212 | `demo_gkxlumenx_ads.policy_match` | `ads.policy_match` | 同 API |

209、212 的表名是 `policy_effect`、`policy_metric_timeseries`、`policy_match`。DATA 把物理库写成 `ads.md` 已登记的 `demo_gkxlumenx_ads`，并写明不把这三张表再放到 `gkxlumenx_ads` 或 `gkxlumenx_gapfill`。API、METRIC 沿架构第 8 节写作 `ads.<表名>`，指的是同一组已有表。

210、211 的 `metric_id` 留空，不新注册。`fill_method=manual`，因此不设 `fill_model`。

## 灌数单

`POL-L2-DS10-SENT-MOCK-ADS`、`POL-L2-DS10-SENT-MOCK-210`、`POL-L2-DS10-SENT-MOCK-211` 在三张分册里都是未执行。本页也不执行。

本页不把任务标 done，签收仍由 human:淮政玮 做。
