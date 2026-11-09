# POL-L2-DS10-TREND · 政策动向跟踪 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 科创政策全景
- 需规序号：203–206
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-07
- 查库时间：2026-11-07 16:02:18（库内 `NOW()`）；**2026-11-09 09:58 随库刷新**（`POL-L2-DS10-EXPECT-REFRESH-L01`：并行灌数单合法新增/重算顶掉 11-07 冻结值，按现行读面重新冻结；读面响应键名为 camelCase）
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
| 203 政策来源监控与更新 | 科创政策全景 · 动向 · 最新入库政策 | 不填 | 进入「政策动向跟踪」 | `GET /display/v1/policy/panorama/ingest` | 不传 `limit`（服务默认 20，clamp 100） | `records` 第一条：`id` 22858，`policy_id`「SYN202611096f5e2e9518-H1」，`source_plane`「domestic」，`title`「深圳市财政局关于印发《深圳市高端装备产业人才引进与创新激励实施细则（试行）》的通知」，`issued_number`「深财规〔2024〕第号」，`publish_organization`「深圳市财政局」，`publish_date`「2024-02-04」，`policy_type`「实施细则」，`province`「广东省」，`status`「已废止」，`etl_batch_id`「SYNTH-20261109095516」，`created_time`「2026-11-09 09:58:11」。⚠️ 该读面随「立即同步」持续灌新行，首条会漂移；验收时以「首条字段齐全（id/policy_id/title/组织/日期/类型非空）且为最新 `created_time`」为准，不锚死单条 | 可演（2026-11-09 刷新） |
| 204 政策订阅服务 | 科创政策全景 · 动向 · 我的订阅 | 登录用户 `3101`（2026-11-09 重绑：换发令牌后展示系统登录主体）。已保存订阅 `id` 4：条件列全空，频率落库 `week`（界面选项值 `weekly`，文案「每周推送」），通道落库 `system`（界面「系统通知」） | 点「我的订阅」。身份来自登录用户，请求不带 `user_id` | `GET /display/v1/policy/panorama/subscriptions` | 无查询参数。须为用户 `3101` 的登录态；匿名时 `subscriptions` 为空列表 | 用户 `3101` 的有效订阅 `id` 4：`policy_type`、`industry_code`、`publish_organization`、`province`、`city`、`region` 为空，`frequency`「week」，`channels` 原文 `["system"]`，`active` 1，`ingest_watermark` 与 `last_outbound_at` 都为空。`pushes` 为空列表，`honesty.source`「gkxlumenx_topic_policy」 | 可演（2026-11-09 主体重绑 3101） |
| 205 重点领域政策分析 | 科创政策全景 · 动向 · 重点领域政策分析 | 领域「科创发展」 | 点该领域卡片上的「查看深度分析报告」 | `POST /display/v1/policy/panorama/jobs` | `{"kind":"深度分析报告","domain":"科创发展"}` | `records` 中 `id` 4：`title`「科创发展领域政策动向演示」，`domain_name`「科创发展」，`body`「缺项演示，正文只写在本行。科创发展条款集中在研发机构布局和成果转化通道，企业落地与技术转移被写在同一组措施里。」，`generated_at`「2026-11-03 14:10:00」 | 可演 |
| 206 政策动态可视化展示 | 科创政策全景 · 动向 · 发布趋势 / 地域分布 / 主题分布 | 不填。不传产业码，不传地域 | 进入「政策动向跟踪」 | `GET /display/v1/policy/panorama/stats` | `kind=all` | `indicators.timeseries` 含 `period_type`「Y」、`period_key`「2026」、`publish_count` 73、`growth_rate` 421.43、`continuity_rate` 86.96；同表 `period_key`「2020」的 `publish_count` 为 2421（现序列峰值）。`indicators.national` 含 `province_name`「北京市」、`province_code`「110000」、`policy_count` 1933。`theme_dist` 含 `themeName`「研发费用加计扣除」、`itemCount` 12、`statYear` 2024。⚠️ 时序/地域读 ADS `policy_timeseries`、`policy_national_dist`，随并行灌数重算会漂移，验收锚定三点：2020=2421 为序列峰值、北京市 policy_count≥1900、主题行 12/2024；行级 `metric_id` as-built 不返回（指标标识在响应 `metrics` 层与库行 `metric_id`，见文末契约裁定） | 可演（2026-11-09 刷新） |

## 一条主路径

按页面从上到下，只走上面四行。条件不另做排列组合。先以用户 `3101` 登录（2026-11-09 主体重绑），再打开科创政策全景 · 动向。

1. 序号 204：点「我的订阅」。请求 `GET /display/v1/policy/panorama/subscriptions`。应看到用户 `3101` 的一条有效订阅 `id` 4：条件列全空，`frequency` 为「week」，`channels` 原文 `["system"]`。`pushes` 为空列表。
2. 序号 203：同一页「最新入库政策」已随进入页面发出 `GET /display/v1/policy/panorama/ingest`。首条字段齐全（id/policy_id/title/发布单位/日期/类型非空）且为最新 `created_time`；该读面随「立即同步」持续灌新行，不锚死单条（快照参考 2026-11-09 09:58：id 22858 深圳市财政局实施细则）。
3. 序号 206：同一页统计区已发出 `GET /display/v1/policy/panorama/stats?kind=all`。时序应出现 2020 年 2421 为序列峰值；地域应出现北京市 1933（≥1900）；主题应出现「研发费用加计扣除」12，`statYear` 2024。
4. 序号 205：在「重点领域政策分析」里对「科创发展」点「查看深度分析报告」。请求 `{"kind":"深度分析报告","domain":"科创发展"}`。应看到标题「科创发展领域政策动向演示」，正文「缺项演示，正文只写在本行。科创发展条款集中在研发机构布局和成果转化通道，企业落地与技术转移被写在同一组措施里。」

## 调度核对

可演 4 行。覆盖不到 0 行。需规 203、204、205、206 各有一行。

## 契约裁定（2026-11-09，`POL-L2-DS10-EXPECT-REFRESH-L01`）

206 行级 `metric_id`：as-built `vendor/entan-py/api/policy_routes.py` `policy_indicators` 的 timeseries/national SELECT 列表不含 `metric_id`（指标标识在响应 `metrics.metric_ids`/`portal_gaps` 层与 ADS 库行）。裁定：**改期望对齐 as-built**，不为演示补列（补列属接口变更，另走 api 单）。203 读面持续灌新行、206 时序/地域随重算漂移的波动语义已写进对应行。
