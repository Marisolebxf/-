# POL-L2-DS10-SENT-SIGNOFF-ALGO · 科创政策全景 · 政策舆情评估 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-03
- 对象：三张分册 `POL-L2-DS10-SENT-API.md`、`POL-L2-DS10-SENT-METRIC.md`、`POL-L2-DS10-SENT-DATA.md`
- 对照：`POL-L2-DS10-SENT-ARCH.md`（2026-11-03 已签收）。本页不改它
- 监管：`human:淮政玮`
- 范围：SRS 207–212。只读核对。不改已有文件，不改算法代码，不动 task-registry

## 结论

同意会签。

## 核对

2026-11-03 用 MCP `metric-get` 复核。下列身份与三张分册的挂接一致。D4 都是 `mock`。210、211 不新注册。

| 序号 | metric_id | algorithm_type | 三张分册 |
|---|---|---|---|
| 207 | `M_POLICY_TOTAL_COUNT`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST` | STAT | 只挂这三条 |
| 208 | `M_POLICY_GRAPH_107_1` | GRAPH | 不改判成 STAT。全国、深圳分布仍是序号 197 的件数，不挂进 208 |
| 209 | `M_POLICY_IMPLEMENTATION_EFFECT` | MODEL | 只挂这一条 |
| 210、211 | 无 | — | 缺项表 `metric_id` 留空 |
| 212 | `M_POLICY_MATCH`、`M_POLICY_INDUSTRY_FIT` | MODEL | 两条都读 `ads.policy_match` |

`M_POLICY_EFFECT_SCORE`、`M_POLICY_DEEP_168_1` 不改挂到 209 或 211。API、METRIC、DATA 三处都写明不挂。`effect.run()` 写在 `policy_effect.metric_id` 上的仍是 `M_POLICY_EFFECT_SCORE`，本叶只读、不改挂。

sub_type 与表：

- 209：`policy_effect`。查 `ads.policy_effect`（`scope_type=region_effect`）和 `ads.policy_metric_timeseries`（`metric_id=M_POLICY_IMPLEMENTATION_EFFECT`）。DATA 写的物理库是 `demo_gkxlumenx_ads`，就是 `run()` 正在写的那一库，不另建表。
- 212：`policy_match`。`M_POLICY_MATCH` 与 `M_POLICY_INDUSTRY_FIT` 读同一张 `ads.policy_match`。行上 `metric_id` 仍是 `M_POLICY_MATCH`，不改成第二条，不另写打分。
- 210：`gkxlumenx_gapfill.gapfill_policy_audience_feedback`
- 211：`gkxlumenx_gapfill.gapfill_policy_assessment_report`

209、212 无行则空。不用 501 充当功能，不返回演示分。三张分册都不重写 `polan/eval/effect.py` 与 `polan/text/match.py`。`demo-algo-ent-analysis` 与 `lumen-algo-py/vendor/entan-py` 的现有 `run()` 一致：匹配为产业命中 +40、地区适用或国家级普适取其一 +25、诉求重合每项 +10、未过期 +10，每主体 Top 8。D4 保持 mock。

未发现三张分册在指标挂接、`policy_effect` / `policy_match`、落表上的矛盾。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。
