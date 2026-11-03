# POL-L2-DS10-SENT-SIGNOFF-ARCH · 科创政策全景 · 政策舆情评估 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS10-SENT-API` / `POL-L2-DS10-SENT-METRIC` / `POL-L2-DS10-SENT-DATA`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS10-SENT-ARCH`（2026-11-03 `human:淮政玮` 已签收）。本页不重新设计，不改那份架构
- 范围：只覆盖上述三张分册。SRS 207–212。说明书第 11.1 节舆情两行只作表和灌数对照

## 结论

同意会签

## 核对

| 项 | 三张分册 | 判定 |
|---|---|---|
| 浏览器只打 `/display/v1/policy/**` | API 公开资源全部在此前缀下。209、212 的 `/topic/v1/analysis/tasks` 只在 `gkxlumen-display` 内部。浏览器不打 `/topic/v1/policy`、`/policy/topic/v1/policy`、`/topicAsync/**`、`/v1/policy/**`。METRIC、DATA 不另开浏览器路径 | 一致 |
| 207 内部委托 `gkxlumen-topic-policy` | API：`stats` → `metrics` + `indicators`，`search` → `search`，`{id}/detail` → `docs/{id}`。DATA 同一跳：前端 → 网关 → `gkxlumen-display` → `gkxlumen-topic-policy` → Python `/internal/policy`。不另建 element 的 policy 包。METRIC 只挂已有三条 STAT，并列查看按条读 detail | 一致 |
| 208 不设资源，Java 不写 nGQL | API 不新开 `/display/v1/policy` 资源，不把专题 `/graph` 改成浏览器地址。DATA 不建表，不把 `policy_graph_node`、`policy_graph_edge` 写成落点。METRIC 保持 `M_POLICY_GRAPH_107_1` 为 GRAPH，不改判成 STAT | 一致 |
| 209、212：`jobs` → topic-async → `/internal/policy/jobs/execute`，查已有 ADS，不用 501 | API：`POST /display/v1/policy/panorama/jobs` → `POST /topic/v1/analysis/tasks` → `PolicyAnalysisAdapterImpl` → `POST /internal/policy/jobs/execute`。下游 `gkxlumen-platform-entan-py`。`policy_effect` 查 `ads.policy_effect`（`scope_type=region_effect`）和 `ads.policy_metric_timeseries`（`metric_id=M_POLICY_IMPLEMENTATION_EFFECT`）。`policy_match` 查 `ads.policy_match`。无行则空，不返回 501，不写死效果数，不返回演示分。METRIC、DATA 同一对表、同一空态 | 一致 |
| 210、211：`gkxlumen-element` 只读 gapfill | `GET .../panorama/feedback` 只读 `gkxlumenx_gapfill.gapfill_policy_audience_feedback`。`GET .../panorama/assessment-report` 只读 `gkxlumenx_gapfill.gapfill_policy_assessment_report`。display 不直连库。不进专题政策门面。METRIC 的 `metric_id` 留空 | 一致 |
| 不调用 `demo-*` 服务 | API 写明不调用任何 `demo-*`，不嵌算法中台页，不打 `/v1/policy/match` 与 `/v1/policy/analysis/effect`。METRIC 写明注册表里的 demo 仓路径不是展示调用链。DATA 不点 demo 服务 | 一致 |
| 不新建桶 | API、DATA：211 下载从读到的行生成，不写对象存储，不走 `report/jobs`。三张分册都没有新桶名 | 一致 |
| 路径、表、`sub_type` 不互相打架 | 见下表。没有第二套路径，没有第二套表，没有第二个 `sub_type` | 一致 |

## 路径、表、sub_type

| 序号 | 公开路径 | 表 | sub_type |
|---|---|---|---|
| 207 | `GET /display/v1/policy/panorama/stats`、`search`、`{id}/detail` | 不另建。正式行沿检索叶；无正式行读已有 `gapfill_policy_qry_stat`、`gapfill_policy_qry_doc`。不读 `gapfill_policy_qry_rank` | 无。同步委托，不是 Job |
| 208 | 不设 | 无 | 无 |
| 209 | `POST /display/v1/policy/panorama/jobs` | 已有 `policy_effect`、`policy_metric_timeseries`。不加列 | `policy_effect` |
| 210 | `GET /display/v1/policy/panorama/feedback` | `gkxlumenx_gapfill.gapfill_policy_audience_feedback` | 无 |
| 211 | `GET /display/v1/policy/panorama/assessment-report` | `gkxlumenx_gapfill.gapfill_policy_assessment_report` | 无 |
| 212 | 与 209 同一条 `jobs` | 已有 `policy_match`。`M_POLICY_MATCH` 与 `M_POLICY_INDUSTRY_FIT` 同一张表、同一 `sub_type`。不灌假通知、假邮件 | `policy_match` |

DATA 把 209、212 的物理库写成 `ads.md` 已登记的 `demo_gkxlumenx_ads`，并写明不把这三张表再放到 `gkxlumenx_ads` 或 `gkxlumenx_gapfill`，查询仍读 `run()` 写入的同一张表。API、METRIC 沿已签收架构写作 `ads.<表名>`。这是同一组已有表，不是另建 ADS，也不是去调 `demo-*` 服务。

`policy_effect`、`policy_match` 不走产业链码与技术领域二选一。API 写明这条例外不扩大到其它 `sub_type`。Java 不打分，不写 nGQL。

说明书第 11.1 节舆情两行：210、211 是上述两张 `gapfill_` 表；209、212 是已有 `ads.policy_effect`、`ads.policy_match`，不另建表，不新造指标，不第二套打分。三张分册与这两行相同。灌数单 `POL-L2-DS10-SENT-MOCK-ADS`、`MOCK-210`、`MOCK-211` 都未执行。查询不灌数。接口不直接返回写死的 mock。

## 铁律

1. 算法只在 Python。209、212 调用已有 `polan.eval.effect.run`、`polan.text.match.run`。Java 不打分。
2. 调用链是前端 → Java → Python `/internal/*`。展示不直连 Python，不直连 `gkx_search_service`，不直连库。
3. 208 只消费第 7 项已有子图。不写 nGQL，不重开 GDF。
4. 可观测沿既有展示链和已有异步任务链。本分册不新设计观测点。
5. 本页是设计会签，不在这里做 K8s rollout。
6. 不把 lumen 展示改去调 `demo-*` 服务。算法中台页面留在原处。
7. 方案 A：浏览器不改打专题 URL。207 的专题门面、209 与 212 的异步任务都是内部委托。
8. 209、212 读已有 ADS。210、211 只读 `gkxlumenx_gapfill`，不写 ODS、DWD、ADS、供应方库。
9. 不新建桶，不写对象存储。
10. 六叶各自有一条现在就能照着做的链路。无行则空。不用 501 充当功能。

D4 保持 mock。不新造 `metric_id`。`GDF-POLICY-MOCK-GATE-L01` 仍按架构稿未解开。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。
