# POL-L2-DS11-READ-SIGNOFF-ALGO · 政策分析评价 · 结果解读报告多维展示 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-READ-ARCH.md`（2026-11-03。本页不改它）
- 对照：`lumen-algo-py/vendor/entan-py` 的 `polan/eval/focus.py`、`polan/eval/gap.py`、`polan/text/parse.py`、`polan/job.py`、`api/policy_routes.py`；判定引自 `sdd/指标与501.md` 223–226
- 监管：`human:淮政玮`
- 范围：SRS 223–226。只读核对。下游分册未到，本页不写分册。不改公式，不改 Python

## 结论

同意会签。

## 核对

2026-11-03 本会话工具目录没有 `metric-registry`，未见 `metric-get`。`algorithm_type` 与 D4 只取 `指标与501.md`。不编 D1–D3。

| 序号 | metric_id | algorithm_type | D4 | 代码 |
|---|---|---|---|---|
| 223 短板 | `M_POLICY_SHORTBOARD_COUNT` | STAT | mock | `polan.eval.gap.run` 写入 `ads.policy_effect`，`scope_type=region_gap`，行上 `metric_id` 即此号 |
| 223 焦点 | `M_POLICY_FOCUS_INDEX` | MODEL | mock | `polan.eval.focus.run` 写入 `ads.policy_focus`。删除条件是 `policy_id IS NOT NULL`。行上 `metric_id` 仍是 `M_POLICY_FOCUS_INDEX/M_POLICY_RELATION_DEGREE` |
| 226 | `M_POLICY_DS_11_POLICY_EVAL_012` | MODEL | mock | 读面。`polan.text.parse.run` 用规则截取写入 `ads.policy_text_parse.summary`，行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`，并 `TRUNCATE` 整表 |
| 224、225 | 无 | — | — | `指标与501.md` 写未见。架构稿不把这两序号写成已有 NLP |

短板：

- `gap.run` 按区域写覆盖盲区、失效占比、平均力度不足，`ext` 含 `is_mock` 与 `pending=QPOL-02`。公式与权重本叶不改，`QPOL-02` 不闭合。
- 中台页 `GapOpportunity.vue` 的提示源写成 `ads.policy_gap`。落表以 `gap.py` 为准，是 `ads.policy_effect`。架构稿不建 `ads.policy_gap`。
- `GET /v1/policy/analysis/gap` 只查 `policy_effect` 且 `scope_type=region_gap`，函数体内不调用 `gap.run`。`api/policy_routes.py` 的请求处理不调用 `gap.run`。`GET /display/v1/policy/evaluation/counts` 在本包内还没有实现；架构稿规定这条 GET 只读同一张表、同一范围，请求里不调用 `gap.run`。
- `job.py` 的 `policy_effect` 调用 `polan.eval.effect.run`，读 `scope_type=region_effect`。短板不走这条分支。

焦点：

- `focus.run` 先 `DELETE FROM ads.policy_focus WHERE policy_id IS NOT NULL`，再插入带 `policy_id` 的行。`policy_id` 为空的机遇行留在表上。
- 展示键 `policy_focus_ads` 当前不在 `JOB_SUB_TYPES`。架构稿把它定为新例外：调用这份 `focus.run`，再读 `policy_id` 非空的行。看板不收 harness 返回的 items，不调 `POST /v1/policy/analysis/focus-one`。
- 既有 `policy_focus`（别名 `focus`、`policy:focus`）落在 `execute_policy_job` 的 else，只调 `harness.dispatch`。架构稿写明这条保持原样。
- `focus-one` 的 `analyze` 返回 `persisted: False`，`metric_id` 为 `M_POLICY_DEEP_166_1`，不写 ADS。

摘要：

- `_summary` 取摘要或正文，去换行后截到 80 字。请求路径保持这段规则截取。
- `GET /v1/policy/text/parse` 只 `SELECT ads.policy_text_parse`，不调用 `parse.run`。
- 架构稿的 `policy_text_parse` 同样是新键：请求里只查 `summary`。`clause_job` 把条款写在同一张表的 `structured_elements` 上，并写明灌数重灌会清空该表。展示请求不调用 `parse.run`，从而避开这次 `TRUNCATE`。
- 中台 `policyHelp.ts` 已把 `M_POLICY_DS_11_POLICY_EVAL_012` 写成读 `ads.policy_text_parse.summary` 的展示身份。行上写入号仍是 `M_POLICY_TEXT_PARSE`。`polan/metrics/metrics.py` 的 `TABLE_MAP` 另把该号指到 `policy_summary`。架构稿采用 `parse.run` 的落表 `ads.policy_text_parse`，不把 `policy_summary` 当本叶的表。

不改挂：

- `M_POLICY_RELATION_DEGREE` 留在焦点行的 `relation_degree` 与拼接 `metric_id` 上。本二级不改挂，不为此读图。
- `M_POLICY_OPPORTUNITY_COUNT` 由 `polan.eval.opportunity.run` 写入 `policy_id IS NULL` 的行。无 223–226 序号。`counts` 上的机遇读面本叶不改。
- `M_POLICY_EFFECT_SCORE` 由 `effect.run` 写入 `scope_type=region_effect`。在既有 `policy_effect` Job 上，不挂 223–226。
- `M_POLICY_DS_11_POLICY_EVAL_015` 在 `指标与501.md` 属于序号 229。架构稿不挂本二级。

224、225 在所列代码里没有专属 `run`，也没有专属 `metric_id`。架构稿只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。

未发现架构稿在上述落表、删除范围、请求是否调用 `run`、以及四条不改挂上与代码矛盾。不新造 `metric_id`，不改 D4，不闭合 `QPOL-02`。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。
