# POL-L2-DS10-TREND · 政策动向跟踪 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 科创政策全景
- 需规序号：203–206
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-07
- 查库时间：2026-11-07 16:02:18（库内 `NOW()`）；**2026-11-09 09:58 随库刷新**（`POL-L2-DS10-EXPECT-REFRESH-L01`：并行灌数单合法新增/重算顶掉 11-07 冻结值，按现行读面重新冻结；读面响应键名为 camelCase）
- **2026-11-12 COVER**：卡1=A、卡2=A；补 G3 形态期望（时间轴 / 中国地图省域热力 / 折线 / 主题卡 / 热点 / 影响 / 同步区 / 通道诚实）；205-3 维持折线+热点按钮；mock 轨保留月×地区矩阵、live 为中国地图（见 `sdd/简报/2026-11-12-政策动向跟踪-需规分句闭合.md`）
- 调度核对：见文末

203 只留入库列表，**不抓取外站**（立即同步 = LLM 合成入库，ARCH 2026-11-07 淮政玮批）。下面的期望都是这次只读 SELECT / 读面读到的字段原文；形态期望写「须见…」。

## 查库

主机 `10.50.11.76`，端口 `3306`，用户 `gkxlumenx`（见 `lumen-algo-py/scripts/seed/seed_synth_elem.py` 的默认主机和用户）。口令未写入本文。

展示服务实际读的库（代码确认后再查，未用正式库行顶替）：

| 读面 | 库.表 | 出处 |
|---|---|---|
| `GET /display/v1/policy/panorama/ingest` | `demo_gkxlumenx_dwd.policy_base_info` | `gkxlumen-element` `PolicyGapfillController` `INGEST_SQL`；`{dwd}` 默认 `demo_gkxlumenx_dwd`（`application.yml` `gkxlumen.element.dwd-db`）。条件 `is_deleted = 0`，`ORDER BY created_time DESC, id DESC`，不传 `limit` 时默认 20 |
| `GET /display/v1/policy/panorama/sync-history` | 同步作业历史（展示委托 element/entan） | 动向页「来源监控」；有 `running` 则前端轮询 |
| `GET /display/v1/policy/panorama/stats` 的时序、地域 | `demo_gkxlumenx_ads.policy_timeseries`、`demo_gkxlumenx_ads.policy_national_dist` | `lumen-algo-py` `vendor/entan-py/api/policy_routes.py` `policy_indicators`。`conn.ads` 在未带 live 平面时为 `demo_gkxlumenx_ads`。两表行数分别是 46 和 31，读 ADS，不回退 `gapfill_policy_qry_stat` |
| 同上响应里的 `theme_dist` | `gkxlumenx_gapfill.gapfill_policy_theme_dist` | `PolicyGapfillController` `THEME_SQL`；`PolicyPanoramaService.stats` 把 `records` 挂到 `theme_dist` |
| `POST /display/v1/policy/panorama/jobs` 且 `kind=深度分析报告` | `gkxlumenx_gapfill.gapfill_policy_trend_report` | `TREND_REPORT_SQL`，`WHERE domain_name = ?`；`PolicyPanoramaService.syncTrendKind` |
| 同上 `kind=热点识别` | `gkxlumenx_gapfill.gapfill_policy_trend_hotspot` | seed：`scripts/seed_gapfill_policy_trend.py`；科创发展 2 条 |
| 同上 `kind=政策影响评估` | `gkxlumenx_gapfill.gapfill_policy_trend_impact` | 同上 seed；科创发展 1 条 |
| `GET /display/v1/policy/panorama/subscriptions` | `gkxlumenx_topic_policy.policy_subscription` | `JdbcPolicySubscriptionStore.listActive`：`user_id = ? AND active = 1 ORDER BY id DESC`。展示侧只转发已登录用户 |

历史集成测试记录保持原文件。这里只写基于现有数据选定的一组输入。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 203 政策来源监控与更新 | 科创政策全景 · 动向 · 最新入库政策 / 来源监控 | 不填 | 进入「政策动向跟踪」 | `GET /display/v1/policy/panorama/ingest`；同页另发 `GET …/sync-history` | ingest 不传 `limit`（服务默认 20，clamp 100）；sync-history 无必填查询参数 | `records` 第一条字段齐全（id/policy_id/title/组织/日期/类型非空）且为最新 `created_time`；随「立即同步」灌新会漂移，**不锚死单条**（快照参考 2026-11-09：id 22858 深圳市财政局实施细则）。**形态期望（COVER）**：① 须见「最新入库」表；② 须见来源监控区（最近同步时间或作业表至少其一）；③ 诚实口径：立即同步为 LLM 合成入库，**不抓取外站**（文案或 ARCH 已声明即可，不以「外站 URL 列表」为验收项） | 可演（2026-11-09 刷新） |
| 204 政策订阅服务 | 科创政策全景 · 动向 · 我的订阅 | 登录用户 `3101`（2026-11-09 重绑）。已保存订阅 `id` 4：条件列全空，频率落库 `week`（界面「每周推送」），通道落库 `system`（界面「系统通知」） | 点「我的订阅」。身份来自登录用户，请求不带 `user_id` | `GET /display/v1/policy/panorama/subscriptions` | 无查询参数。须为用户 `3101` 的登录态；匿名时 `subscriptions` 为空列表 | 用户 `3101` 的有效订阅 `id` 4：条件列空，`frequency`「week」，`channels` 原文 `["system"]`，`active` 1；`pushes` 为空列表，`honesty.source`「gkxlumenx_topic_policy」。**形态期望（COVER）**：须见通道枚举含系统通知/邮件/短信（表单或说明）；外发未上线时须见诚实提示（如「外发通道未上线…推送收件箱暂无真实推送记录」类文案），不以真发邮件/短信为验收项（G6） | 可演（2026-11-09 主体重绑 3101） |
| 205 重点领域 · 深度分析报告 | 科创政策全景 · 动向 · 重点领域政策分析 | 领域「科创发展」 | 点该领域卡片「查看深度分析报告」 | `POST /display/v1/policy/panorama/jobs`；导出另走 `POST /display/v1/situation/report/generate` | `{"kind":"深度分析报告","domain":"科创发展"}` | `records` 中 `id` 4：`title`「科创发展领域政策动向演示」，`domain_name`「科创发展」，`body`「缺项演示，正文只写在本行。科创发展条款集中在研发机构布局和成果转化通道，企业落地与技术转移被写在同一组措施里。」，`generated_at`「2026-11-03 14:10:00」。**形态期望（KEYFIELD-FDE）**：须见弹窗 + 进度条 → 展示上述标题与正文；完成后可导出 PDF（真字节）/ Word（html→.doc）；无行空态不产文件；禁打印另存 / text/plain | 可演 |
| 205 重点领域 · 热点识别 | 同页 · 热点识别 | 领域上下文「科创发展」（全页热点按钮不带 domain 时读缺项全表亦可；本路径以科创发展两条为准） | **用户点击**「热点识别」（切条件不自动起任务，I2-12） | `POST /display/v1/policy/panorama/jobs` | `{"kind":"热点识别"}`（若实现带 domain：`domain=科创发展`） | 缺项表种子（`seed_gapfill_policy_trend.py`）：科创发展至少含热点「研发机构布局」「成果转化通道」及对应 brief（「缺项演示。重点实验室…」「缺项演示。高校院所技术…」）。**形态期望（COVER）**：点击后须见热点结果列表/表；无行则空态，不前端拼热点 | 可演（gapfill） |
| 205 重点领域 · 影响评估 | 同页 · 影响评估 | 领域「科创发展」 | **用户点击**该领域「影响评估」 | `POST /display/v1/policy/panorama/jobs`；导出另走 `situation/report/generate` | `{"kind":"政策影响评估","domain":"科创发展"}` | 种子行：`domain_name`「科创发展」，`impact_object`「科技型企业」，`impact_direction`「支持范围扩大」，`conclusion`「缺项演示。研发机构与成果转化条款使科技型企业获得更明确的落地支持。」。**形态期望（KEYFIELD-FDE）**：须见弹窗 + 进度条 → 对象/方向/结论；完成后可导出 PDF/Word；无行空态不产文件 | 可演（gapfill） |
| 205 重点领域 · 趋势分析（卡1=A） | 同页 · 发布时序 / 热点 | 不填 | 进入动向 Tab（时序随 stats）；热点见上行点击 | `GET …/stats?kind=all`；热点见上行 | `kind=all` | 趋势分析 live **不以** mock 本周/月/年 KPI 卡与 fixture TOP5 为验收项。**形态期望（COVER）**：须见「发布时序」折线图（见 206）；热点识别走上行按钮。与 ARCH 一致 | 可演 |
| 206 政策动态可视化展示 | 科创政策全景 · 动向 · 时间轴 / 地域热力 / 发布时序 / 主题分布 | 不填。不传产业码，不传地域 | 进入「政策动向跟踪」 | `GET /display/v1/policy/panorama/stats` | `kind=all` | `indicators.timeseries`：锚定 2020=`publish_count` 2421 为序列峰值；含 `period_key`「2026」等点（随重算可漂移，峰值锚点优先）。`indicators.national`：北京市 `policy_count`≥1900（快照 1933）。`theme_dist`：主题「研发费用加计扣除」`itemCount` 12、`statYear` 2024。行级 `metric_id` as-built 不返回（见文末）。**形态期望（COVER）**：① **时间轴**须见「政策动态时间轴」区块（有时序点则出轴项，无点空态）；② **地域热力（live）**须见中国地图省域着色（`map: china` + visualMap 色阶），标题「地域热力」；**禁止**以横向条形图冒充热力；无省行则图空；`USE_MOCK=true` 仍可为月×地区矩阵（卡2=A 双轨）；③ **趋势图**须见「发布时序」折线；④ **主题分布**须见主题卡网格（名称+件数） | 可演（2026-11-09 刷新；形态随 2026-11-12 地图热力推送） |

## 一条主路径

按页面从上到下。条件不另做排列组合。先以用户 `3101` 登录（2026-11-09 主体重绑），再打开科创政策全景 · 动向。

1. 序号 204：点「我的订阅」。请求 `GET /display/v1/policy/panorama/subscriptions`。应看到用户 `3101` 的一条有效订阅 `id` 4：条件列全空，`frequency` 为「week」，`channels` 原文 `["system"]`。`pushes` 为空列表。同屏须能看到通道说明/诚实条（外发未上线不挡本步）。
2. 序号 203：同一页「最新入库政策」已随进入发出 `GET …/ingest`；来源监控区可见最近同步或作业表。首条字段齐全且为最新 `created_time`；不锚死单条。不以「外站抓取」为通过条件。
3. 序号 206：同一页已发 `GET …/stats?kind=all`。时序峰值 2020=2421；地域北京市≥1900；主题「研发费用加计扣除」12/2024。同屏须见：时间轴、中国地图地域热力（非条形）、发布时序折线、主题卡。
4. 序号 205：对「科创发展」点「查看深度分析报告」→ 弹窗进度完成后标题与正文与覆盖表一致，可导出 PDF/Word。再点「热点识别」→ 见「研发机构布局」「成果转化通道」。再点「影响评估」→ 弹窗进度完成后见对象「科技型企业」与结论句，可导出。

## 调度核对

可演行：203、204、205（深度/热点/影响）、206。覆盖不到 0 行。需规 203–206 均有着落；205 拆三行形态验收，趋势分析按卡1=A 并入折线+热点。

## 契约裁定（2026-11-09，`POL-L2-DS10-EXPECT-REFRESH-L01`）

206 行级 `metric_id`：as-built `vendor/entan-py/api/policy_routes.py` `policy_indicators` 的 timeseries/national SELECT 列表不含 `metric_id`（指标标识在响应 `metrics.metric_ids`/`portal_gaps` 层与 ADS 库行）。裁定：**改期望对齐 as-built**，不为演示补列（补列属接口变更，另走 api 单）。203 读面持续灌新行、206 时序/地域随重算漂移的波动语义已写进对应行。

## COVER 裁定（2026-11-12）

| 卡 | 选择 | 落地 |
|---|---|---|
| 卡1 · 205-3 趋势分析 | **A** | live 不回 mock KPI/TOP5；折线 + 热点识别 jobs |
| 卡2 · 206 mock 矩阵 | **A** | mock 保留月×地区矩阵；live 中国地图省域热力（已推 `lumen-ui-science-pc`） |
| G3 | 本文件形态期望 | 不改 ARCH/四单/业务代码 |
| G6 | 203 不抓外站；204 外发诚实；205 全球举措 gapfill | 记有意，不派实现 |
