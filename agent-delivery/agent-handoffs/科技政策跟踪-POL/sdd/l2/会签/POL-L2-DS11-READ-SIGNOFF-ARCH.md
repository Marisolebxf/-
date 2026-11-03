# POL-L2-DS11-READ-SIGNOFF-ARCH · 政策分析评价 · 结果解读报告多维展示 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-READ-ARCH`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS11-READ-ARCH`（2026-11-03）。本页不重新设计，不改那份架构。下游 `POL-L2-DS11-READ-API` / `METRIC` / `DATA` 尚未成册，本页不等、不代写
- 范围：SRS 序号 223–226。说明书第 11 节与 `sdd/调用链与边界.md` 只作对照

## 结论

同意会签

## 核对

| 项 | 架构稿 | 判定 |
|---|---|---|
| 算法只在 Python。Java 不算指数、不写 nGQL | 223 焦点在 Job 里调用已有 `polan.eval.focus.run`，再读表。223 短板由 `gkxlumen-element` 读 `gap.run` 已写入的行，GET 不算指数。226 只查询已有 `summary`。`gkxlumen-display` 不写算法。Java 只经 `PolicyAnalysisAdapterImpl` 转发 `POST /internal/policy/jobs/execute`。本叶不为此读图，Java 不写 nGQL | 一致 |
| 浏览器只打 `/display/v1/policy/**` | 公开资源是 `evaluation/counts`、`evaluation/jobs`、`evaluation/shells`。`POST /topic/v1/analysis/tasks` 只在 `gkxlumen-display` 内部。`/v1/policy/analysis/*`、`/v1/policy/text/parse`、`focus-one` 留给算法中台。不把 `/topic/v1/policy`、`/v1/policy/**` 写成对外入口。不调用 `demo-*`，不嵌中台页 | 一致 |
| 有 ADS 且有 `run()` 则读表；没有算法也没有表则只允许 `gapfill_` | 223 短板读 `ads.policy_effect`（`scope_type=region_gap`），不建 `ads.policy_gap`。223 焦点读 `ads.policy_focus`（`policy_id` 非空），不建 `gapfill_policy_eval_focus`。226 读 `ads.policy_text_parse`，不建 `gapfill_policy_eval_summary`。224、225 无专属算法、无已有表，只建 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。无行则空。接口不直接返回写死的 mock。不用 501 充当功能 | 一致 |
| 旧 `policy_focus` 仍走 harness，且保留 items | `polan/job.py` 里 `policy_focus` 仍进 `harness.dispatch(items)`。`PolicyAnalysisTypes.FOCUS` 与 Adapter 上「产业、技术领域、items 或正文」的校验保持原样。展示看板走新键 `policy_focus_ads`：调用 `focus.run` 后读表，不收 items，不把 harness 的返回当成热点看板 | 一致 |
| 226 的请求路径不调用 `parse.run` | `polan.text.parse.run` 插入前 `truncate` 整张 `ads.policy_text_parse`。`sub_type=policy_text_parse` 只查询 `summary`。当前 `JOB_SUB_TYPES` 没有这个键；实现时按只读例外加入，请求不接到 `parse.run` | 一致 |
| 机遇条数、222 模板、227–231、关联度不改挂到 223–226 | `M_POLICY_OPPORTUNITY_COUNT` 留在 `counts` 上已有读面。`focus.run` 仍只删除 `policy_id IS NOT NULL`。222 的模板选用不灌入 shell。227–231 与 `M_POLICY_DS_11_POLICY_EVAL_015` 不进本四叶。`M_POLICY_RELATION_DEGREE` 仍在同一行的 `relation_degree`，不改挂到 223 | 一致 |
| 不新建桶，不灌视频。display 不直连库、不直连 Python | 225 只读条目标题和一句说明，不写对象存储，前端不直连 RustFS。同步读经 `gkxlumen-element`。Job 经 `gkxlumen-topic-async-service` 再进 Python `/internal/policy/jobs/execute` | 一致 |

## 路径、表、sub_type

| 序号 | 公开路径 | 表 | sub_type |
|---|---|---|---|
| 223 短板 | `GET /display/v1/policy/evaluation/counts` | 已有 `ads.policy_effect`（`scope_type=region_gap` 的 `shortboard_cnt`）。不另建表 | 无。同步读，不是 Job |
| 223 焦点 | `POST /display/v1/policy/evaluation/jobs` | 已有 `ads.policy_focus`（`policy_id` 非空）。不另建 `gapfill_policy_eval_focus` | `policy_focus_ads` |
| 224、225 | `GET /display/v1/policy/evaluation/shells` | `gkxlumenx_gapfill.gapfill_policy_eval_shell`。不灌视频、不灌模板 | 无。同步读，不是 Job |
| 226 | `POST /display/v1/policy/evaluation/jobs` | 已有 `ads.policy_text_parse.summary`。不另建 `gapfill_policy_eval_summary` | `policy_text_parse` |

223 焦点与 226 摘要的内部跳是：`gkxlumen-display` → `POST /topic/v1/analysis/tasks` → `PolicyAnalysisAdapterImpl` → `POST /internal/policy/jobs/execute`。浏览器不看见这条内部地址。

说明书第 11.2 节把 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`、`gapfill_policy_eval_shell` 写在 222–226 同一行。本叶按第 11 节总规则收窄：焦点和摘要已经有 ADS，也有可调用的 `run()`，接口读已有表。shell 只服务 224、225。222 的模板选用不在本叶灌入。

调用链第 2 节：短板条数同步读，源模型不在这条链上计算。本叶 `counts` 只读 `shortboard_cnt`，这次 GET 不调用 `gap.run`。第 3 节把焦点指数和智能摘要写在「模型未注册则 501」。这两处已有可调用 `run()` 和 ADS，本叶改走读表，无行则空，不用 501 充当功能。效果评分、分区、方案、参数模拟、实施路径仍不进入 223–226。本页不改写调用链文件。

代码落点（只核对，未改代码）：

- `polan/eval/gap.py` 的 `run()` 写入 `ads.policy_effect`，`scope_type=region_gap`，列为 `shortboard_cnt`。
- `polan/eval/focus.py` 的 `run()` 删除 `policy_id IS NOT NULL` 后写入 `focus_score`，以及 `ext` 里的 `title`、`explanation`。`polan/eval/opportunity.py` 只删除 `policy_id IS NULL` 的区域机遇行。
- `polan/job.py`：`policy_focus` 与 `policy_shard` 走 `harness.dispatch`；`policy_effect`、`policy_match` 是已有的先算再读例外。`policy_focus_ads`、`policy_text_parse` 尚未进入 `JOB_SUB_TYPES`。
- `polan/text/parse.py` 的 `run()` 在插入前 `truncate` 整张 `ads.policy_text_parse`。
- `PolicyAnalysisTypes` 的白名单含 `policy_focus`。`skipsIndustryVidXor` 只放行 `policy_effect`、`policy_match`。`PolicyAnalysisAdapterImpl` 在焦点既无产业、也无技术领域、也无 items、也无正文时拒绝创建。

D4 保持 mock。不新造 `metric_id`。`QPOL-02` 未闭合。`GDF-POLICY-MOCK-GATE-L01` 仍按架构稿未解开。本叶不执行灌数。

## 铁律

1. 算法只在 Python。223 焦点调用已有 `polan.eval.focus.run`。223 短板与 226 摘要由查询读已有表。Java 不算指数，不写 nGQL。
2. 调用链是浏览器 → `/display/v1/policy/**` → Java → 需要计算时再进 Python `/internal/*`。展示不直连 Python，不直连库，不调用 `demo-*`。
3. 223、226 读已有 ADS，不另建缺项表。224、225 只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。接口不直接返回写死的 mock，不用 501 充当功能。
4. 带 items 的 `policy_focus` 仍走 `harness.dispatch`。看板用新键 `policy_focus_ads`，不改旧路径。
5. `polan.text.parse.run` 会清空 `ads.policy_text_parse`。226 的请求只查询，不调用它。
6. 机遇条数、序号 222 的模板、227–231 的方案、`M_POLICY_RELATION_DEGREE` 不改挂到 223–226。
7. 不新建桶，不灌视频文件。display 不直连库，不直连 Python。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。
