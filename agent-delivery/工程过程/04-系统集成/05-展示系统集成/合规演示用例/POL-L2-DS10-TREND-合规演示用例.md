# POL-L2-DS10-TREND · 政策动向跟踪 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 科创政策全景
- 需规序号：203–206
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-07
- 查库时间：2026-11-07 16:02:18（库内 `NOW()`）
- 调度核对：见文末

203 只留入库列表，不新开抓取。下面的期望都是这次只读 SELECT 读到的字段原文。

## 查库

主机 `10.50.11.76`，端口 `3306`，用户 `gkxlumenx`（见 `lumen-algo-py/scripts/seed/seed_synth_elem.py` 的默认主机和用户）。口令未写入本文。

展示服务实际读的库（代码确认后再查，未用正式库行顶替）：

| 读面 | 库.表 | 出处 |
|---|---|---|
| `GET /display/v1/policy/panorama/ingest` | `demo_gkxlumenx_dwd.policy_base_info` | `gkxlumen-element` `PolicyGapfillController` `INGEST_SQL`；`{dwd}` 默认 `demo_gkxlumenx_dwd`（`application.yml` `gkxlumen.element.dwd-db`）。条件 `is_deleted = 0`，`ORDER BY created_time DESC, id DESC`，不传 `limit` 时默认 20 |
| `GET /display/v1/policy/panorama/stats` 的时序、地域 | `demo_gkxlumenx_ads.policy_timeseries`、`demo_gkxlumenx_ads.policy_national_dist` | `lumen-algo-py` `vendor/entan-py/api/policy_routes.py` `policy_indicators`。`conn.ads` 在未带 live 平面时为 `demo_gkxlumenx_ads`。两表行数分别是 46 和 31，读 ADS，不回退 `gapfill_policy_qry_stat` |
| 同上响应里的 `theme_dist` | `gkxlumenx_gapfill.gapfill_policy_theme_dist` | `PolicyGapfillController` `THEME_SQL`；`PolicyPanoramaService.stats` 把 `records` 挂到 `theme_dist` |
| `POST /display/v1/policy/panorama/jobs` 且 `kind=深度分析报告` | `gkxlumenx_gapfill.gapfill_policy_trend_report` | `TREND_REPORT_SQL`，`WHERE domain_name = ?`；`PolicyPanoramaService.syncTrendKind` |
| `GET /display/v1/policy/panorama/subscriptions` | `gkxlumenx_topic_policy.policy_subscription` | `JdbcPolicySubscriptionStore.listActive`：`user_id = ? AND active = 1 ORDER BY id DESC`。展示侧只转发已登录用户 |

历史集成测试记录保持原文件。这里只写基于现有数据选定的一组输入。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 203 政策来源监控与更新 | 科创政策全景 · 动向 · 最新入库政策 | 不填 | 进入「政策动向跟踪」 | `GET /display/v1/policy/panorama/ingest` | 不传 `limit`（服务默认 20） | `records` 第一条：`id` 20008，`policy_id`「gl-meti-20220831」，`source_plane`「global」，`title`「蓄电池产业战略（最终汇总）」，`issued_number` 为空字符串，`publish_organization`「日本经济产业省」，`publish_date`「2022-08-31」，`policy_type`「战略」，`province` 为空，`status` 为空，`url`「https://www.meti.go.jp/press/2022/08/20220831001/20220831001.html」，`etl_batch_id` 为空，`created_time`「2026-10-27 20:58:22」。未删除行共 20008 条，本请求只返回按上述排序的前 20 条 | 可演 |
| 204 政策订阅服务 | 科创政策全景 · 动向 · 我的订阅 | 登录用户 `184`。已保存订阅 `id` 1：政策类别 `sci-tech,industry,park,investment,talent,finance,ip`；行业领域 `CL-SEI-01,INB1309`；发布部门、省、市、地区为空；频率落库 `week`（界面选项值 `weekly`，文案「每周推送」）；通道落库 `system`（界面「系统通知」） | 点「我的订阅」。身份来自登录用户，请求不带 `user_id` | `GET /display/v1/policy/panorama/subscriptions` | 无查询参数。须为用户 `184` 的登录态；匿名时 `subscriptions` 为空列表 | 用户 `184` 的有效订阅按 `id` 倒序为 3、2、1，`frequency` 都是「week」，`active` 都是 1，`ingest_watermark` 与 `last_outbound_at` 都为空。`id` 3：`policy_type`、`industry_code`、`publish_organization`、`province`、`city`、`region` 为空，`channels` 原文「system,sms」。`id` 2：上述条件列为空，`channels` 原文「system」。`id` 1：`policy_type`「sci-tech,industry,park,investment,talent,finance,ip」，`industry_code`「CL-SEI-01,INB1309」，发布部门与省市区为空，`channels` 原文「system」。`pushes` 为空列表 | 可演 |
| 205 重点领域政策分析 | 科创政策全景 · 动向 · 重点领域政策分析 | 领域「科创发展」 | 点该领域卡片上的「查看深度分析报告」 | `POST /display/v1/policy/panorama/jobs` | `{"kind":"深度分析报告","domain":"科创发展"}` | `records` 中 `id` 4：`title`「科创发展领域政策动向演示」，`domain_name`「科创发展」，`body`「缺项演示，正文只写在本行。科创发展条款集中在研发机构布局和成果转化通道，企业落地与技术转移被写在同一组措施里。」，`generated_at`「2026-11-03 14:10:00」 | 可演 |
| 206 政策动态可视化展示 | 科创政策全景 · 动向 · 发布趋势 / 地域分布 / 主题分布 | 不填。不传产业码，不传地域 | 进入「政策动向跟踪」 | `GET /display/v1/policy/panorama/stats` | `kind=all` | `indicators.timeseries` 含 `period_type`「Y」、`period_key`「2026」、`publish_count` 3、`metric_id`「M_POLICY_TIMESERIES」；同表 `period_key`「2020」的 `publish_count` 为 2402。`indicators.national` 含 `province_name`「北京市」、`province_code`「110000」、`policy_count` 2268、`metric_id`「M_POLICY_NATIONAL_DIST」。`theme_dist` 含 `theme_name`「研发费用加计扣除」、`item_count` 12、`stat_year` 2024 | 可演 |

## 一条主路径

按页面从上到下，只走上面四行。条件不另做排列组合。先以用户 `184` 登录，再打开科创政策全景 · 动向。

1. 序号 204：点「我的订阅」。请求 `GET /display/v1/policy/panorama/subscriptions`。应看到用户 `184` 的三条有效订阅，其中 `id` 1 的 `policy_type` 为「sci-tech,industry,park,investment,talent,finance,ip」，`industry_code` 为「CL-SEI-01,INB1309」，`frequency` 为「week」，`channels` 原文「system」。`pushes` 为空列表。
2. 序号 203：同一页「最新入库政策」已随进入页面发出 `GET /display/v1/policy/panorama/ingest`。第一条标题「蓄电池产业战略（最终汇总）」，发布单位「日本经济产业省」，发布日期「2022-08-31」，`policy_id`「gl-meti-20220831」。
3. 序号 206：同一页统计区已发出 `GET /display/v1/policy/panorama/stats?kind=all`。时序应出现 2026 年发布量 3、2020 年发布量 2402；地域应出现北京市 2268；主题应出现「研发费用加计扣除」12，`stat_year` 2024。
4. 序号 205：在「重点领域政策分析」里对「科创发展」点「查看深度分析报告」。请求 `{"kind":"深度分析报告","domain":"科创发展"}`。应看到标题「科创发展领域政策动向演示」，正文「缺项演示，正文只写在本行。科创发展条款集中在研发机构布局和成果转化通道，企业落地与技术转移被写在同一组措施里。」

## 调度核对

可演 4 行。覆盖不到 0 行。需规 203、204、205、206 各有一行。
