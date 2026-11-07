# POL-DS10-CASE-FILL-SENT · 政策舆情评估合规演示用例填充

ponytail: N/A（文档）

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 任务已是 in_progress。本会话不改 task-registry，不标 done |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `N/A`（文档） |
| 说明 | 只填本叶用例和本 handoff。未改业务仓，未改索引，未改另外三份用例 |

## 查了哪些表

查库时间 2026-11-07 15:56:52。主机 `10.50.11.76`，用户 `gkxlumenx`，取自 `lumen-algo-py/scripts/seed/seed_synth_elem.py` 缺省。口令只进本次进程，未打印，未写入文件。只读 SELECT，未 `--apply`。

展示实际读面（`lumen-svc-platform` 与它委托的 Python）：

| 用途 | 代码 | 库.表 | 本次结果 |
|---|---|---|---|
| 207 检索 | `PolicyPanoramaService.search` → `polan.search.search_policies` | `demo_gkxlumenx_dwd.policy_base_info` | 关键词「人工智能」73 行 |
| 209 效果 | `polan.job._policy_effect_rows` | `demo_gkxlumenx_ads.policy_effect`（`scope_type=region_effect`） | 31 行 |
| 209 时序 | 同上 | `demo_gkxlumenx_ads.policy_metric_timeseries`（`metric_id=M_POLICY_IMPLEMENTATION_EFFECT`） | 抽到 `region_code=440000` |
| 210 反馈 | `PolicyGapfillController.FEEDBACK_SQL` | `gkxlumenx_gapfill.gapfill_policy_audience_feedback` | 6 行，三渠道各 2 |
| 211 报告 | `PolicyGapfillController.REPORT_SQL` | `gkxlumenx_gapfill.gapfill_policy_assessment_report` | 2 行 |
| 212 匹配 | `polan.job._policy_match_rows` | `demo_gkxlumenx_ads.policy_match` | 全表 111 行；`E0001` 5 行 |

对照未采用：`gkxlumenx_ads.policy_effect` 的 `region_effect` 为 0 行。`gkxlumenx_dwd.policy_base_info` 同一关键词也是 73 条，展示默认平面不读这张。208 不查图、不编数字。

## 每条序号

| 序号 | 数据情况 | 输入 | 原句出处 |
|---|---|---|---|
| 207 | 可演 | 关键词「人工智能」 | `demo_gkxlumenx_dwd.policy_base_info`：`policy_id`、`title`、`publish_organization`、`publish_date`。首条 18323509 |
| 208 | 设计无资源 | 不填、不请求 | 详设 §2：跨项索引，不设 `/display/v1/policy` 资源 |
| 209 | 可演 | 不填区域，`sub_type=policy_effect` | `demo_gkxlumenx_ads.policy_effect.effect_score` 与 `ext` 内 `explanation`；`policy_metric_timeseries.metric_value`、`dim_key`、`stat_date`。抽广东省 440000 |
| 210 | 可演 | 渠道「问卷调查」 | `gkxlumenx_gapfill.gapfill_policy_audience_feedback`：`subject_name`、`channel`、`opinion_text`、`score`、`policy_id` |
| 211 | 可演 | 不填，看列表首条 | `gkxlumenx_gapfill.gapfill_policy_assessment_report`：`scope_text`、`achievement_text`、`social_impact`、`problem_text`、`suggestion_text`、`report_body`。首条 `id` 2 |
| 212 | 可演 | 主体「华芯生物有限公司（E0001）」 | `demo_gkxlumenx_ads.policy_match`：`subject_name`、`policy_title`、`match_score`、`match_reasons`、`rank_no`。推送没有库内投递原文，期望停在匹配行 |

契约里 209、210、211、212 曾标 501 或未见。这次库内有展示会读的行，所以记可演。D4 未改。

209 的 jobs 会先跑 `effect.run()` 再读表。本次 `stat_date` 是 2026-11-07，分数和口径说明以这次 SELECT 为准。212 的 jobs 会先跑 `match.run()` 再按 `subject_id` 读表。期望用的是读到的现成行，不是新编的一句。

## 产物

- `agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-SENT-合规演示用例.md`
- 本 handoff

可演 5 行，覆盖不到 0 行，设计无资源 1 行。未改索引、未改其他用例、未改业务仓、未 commit、未 push。

## CI/CD

- 未 commit，未 push
- 未改业务仓，无 pipeline
