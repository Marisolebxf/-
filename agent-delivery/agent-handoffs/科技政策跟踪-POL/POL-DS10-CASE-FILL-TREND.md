# POL-DS10-CASE-FILL-TREND

- 任务：`POL-DS10-CASE-FILL-TREND`
- 监管人：`human:淮政玮`
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-TREND-合规演示用例.md`
- 日期：2026-11-07
- ponytail: N/A（文档）

本叶只补动向跟踪 203–206 的合规演示用例。未改业务仓，未改索引、其他用例和 LOOP 计划，未改 `task-registry.yaml`，未 commit，未打 `https://edu.itic-sci.com`。

## 查了哪些表

查库时间：2026-11-07 16:02:18（`NOW()`）。主机 `10.50.11.76`，端口 `3306`，用户 `gkxlumenx`。只读 `SELECT`。口令没有写入本文件。

本进程启动时没有环境变量 `LUMEN_ALGO_MYSQL_PASSWORD`。连接口令只在进程内存里读取，没有打印。

展示读面以 `lumen-svc-platform` 的调用链为准，再落到算法仓里 stats 实际执行的 SQL：

| 接口 | 代码 | 实际读的表 | 本次行数 |
|---|---|---|---|
| `GET .../panorama/ingest` | `PolicyGapfillController.INGEST_SQL`，`{dwd}` 默认 `demo_gkxlumenx_dwd` | `demo_gkxlumenx_dwd.policy_base_info`（`is_deleted = 0`） | 20008 |
| `GET .../panorama/stats` 时序、地域 | `policy_routes.policy_indicators`；未带 live 平面时 `conn.ads = demo_gkxlumenx_ads`。行数不为 0，不读 `gapfill_policy_qry_stat` | `demo_gkxlumenx_ads.policy_timeseries`；`demo_gkxlumenx_ads.policy_national_dist` | 46；31 |
| `stats` 的 `theme_dist` | `THEME_SQL`，`gapfill-db` 默认 `gkxlumenx_gapfill` | `gkxlumenx_gapfill.gapfill_policy_theme_dist` | 5（本次列出的 id 6–10） |
| `POST .../panorama/jobs` `kind=深度分析报告` | `TREND_REPORT_SQL` | `gkxlumenx_gapfill.gapfill_policy_trend_report` | 领域「科创发展」1 行（id 4）。同表还有人才引进、资金扶持各 1 行 |
| 同 jobs 的热点、影响（本条用例未把它们写成第二个请求） | `HOTSPOT_SQL`、`IMPACT_SQL` | `gapfill_policy_trend_hotspot`、`gapfill_policy_trend_impact` | 热点 6 行（科创发展 / 人才引进 / 资金扶持各 2）；影响 3 行（三领域各 1） |
| `GET .../panorama/subscriptions` | `JdbcPolicySubscriptionStore.listActive` | `gkxlumenx_topic_policy.policy_subscription` | `active = 1` 共 3 行，`user_id` 都是 `184` |

`information_schema` 里 `gkxlumenx_dwd.policy_base_info`、`gkxlumenx_ads.policy_timeseries`、`gkxlumenx_ads.policy_national_dist` 也有表。展示这条链读的是上面的 demo 面和 `gkxlumenx_gapfill`，正式库行没有拿来写期望。

## 每条序号

### 203 可演

不填条件，进入动向页即 `GET /ingest`。排序后第一条是 `id` 20008。

原句出处：`demo_gkxlumenx_dwd.policy_base_info` 的 `title`「蓄电池产业战略（最终汇总）」、`publish_organization`「日本经济产业省」、`publish_date`「2022-08-31」、`policy_id`「gl-meti-20220831」、`policy_type`「战略」、`source_plane`「global」、`url`「https://www.meti.go.jp/press/2022/08/20220831001/20220831001.html」、`created_time`「2026-10-27 20:58:22」。`province`、`status`、`etl_batch_id` 为空，`issued_number` 为空字符串。

### 204 可演

登录用户 `184` 打开「我的订阅」。`GET /subscriptions` 无查询参数。

原句出处：`gkxlumenx_topic_policy.policy_subscription`。`id` 1 的 `policy_type`「sci-tech,industry,park,investment,talent,finance,ip」，`industry_code`「CL-SEI-01,INB1309」，`frequency`「week」，`channels`「system」。`id` 2 的条件列为空，`channels`「system」。`id` 3 的条件列为空，`channels`「system,sms」。三行 `ingest_watermark`、`last_outbound_at` 为空。服务把 `pushes` 固定成空列表，期望按这个空列表写，没有另编推送正文。

### 205 可演

界面选择领域「科创发展」，点「查看深度分析报告」。请求只带 `{"kind":"深度分析报告","domain":"科创发展"}`。

原句出处：`gkxlumenx_gapfill.gapfill_policy_trend_report` `id` 4 的 `title`「科创发展领域政策动向演示」，`body`「缺项演示，正文只写在本行。科创发展条款集中在研发机构布局和成果转化通道，企业落地与技术转移被写在同一组措施里。」，`generated_at`「2026-11-03 14:10:00」。

同领域库内还有行，本条只选报告这一组请求：热点 `id` 7 `hotspot_name`「研发机构布局」，`brief`「缺项演示。重点实验室与新型研发机构落地被反复写进科创发展条款。」；影响 `id` 4 `impact_object`「科技型企业」，`impact_direction`「支持范围扩大」，`conclusion`「缺项演示。研发机构与成果转化条款使科技型企业获得更明确的落地支持。」

### 206 可演

不填产业和地域，进入动向页即 `GET /stats?kind=all`。

原句出处：

- `demo_gkxlumenx_ads.policy_timeseries`：`period_key`「2026」`publish_count` 3；`period_key`「2020」`publish_count` 2402；`period_type`「Y」；`metric_id`「M_POLICY_TIMESERIES」
- `demo_gkxlumenx_ads.policy_national_dist`：`province_name`「北京市」，`province_code`「110000」，`policy_count` 2268，`metric_id`「M_POLICY_NATIONAL_DIST」
- `gkxlumenx_gapfill.gapfill_policy_theme_dist`：`theme_name`「研发费用加计扣除」，`item_count` 12，`stat_year` 2024

## 调度核对

可演 4 行（203、204、205、206）。覆盖不到 0 行。主路径只串这四行。
