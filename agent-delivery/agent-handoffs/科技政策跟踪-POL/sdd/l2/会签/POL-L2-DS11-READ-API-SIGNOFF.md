# POL-L2-DS11-READ-API-SIGNOFF · 政策分析评价 · 结果解读报告多维展示 · 接口分册架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-03
- 对象：`sdd/l2/POL-L2-DS11-READ-API.md`，交接 `POL-L2-DS11-READ-API.md`
- 监管：`human:淮政玮`
- 对照：已签收的 `sdd/l2/POL-L2-DS11-READ-ARCH.md`（2026-11-03）
- 本页不改分册正文，不改架构稿，不改任务状态

## 结论

同意

## 核对

| 项 | 分册与交接 | 对照架构 | 判定 |
|---|---|---|---|
| 223 短板 | `GET /display/v1/policy/evaluation/counts`。同步。`gkxlumen-element` 只读 `ads.policy_effect` 里 `scope_type=region_gap` 的 `shortboard_cnt`。这次 GET 不调用 `gap.run`。无行则空，不造 0 | §2、§4.1：同步读，GET 不调用 `gap.run` | 一致 |
| 223 焦点 | `POST /display/v1/policy/evaluation/jobs`。`sub_type=policy_focus_ads`。调用已有 `focus.run` 后读 `ads.policy_focus` 里 `policy_id` 非空的行。旧键 `policy_focus` 仍走 `harness.dispatch`，不改旧键 | §2、§4.1：新键 `policy_focus_ads`，旧键仍走 harness | 一致 |
| 224、225 | 同一条 `GET /display/v1/policy/evaluation/shells`。只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。不灌模板选用，不灌视频 | §4.2、§4.3、§8：壳表只服务 224、225，不灌模板 | 一致 |
| 226 | 同一条 `POST evaluation/jobs`。`sub_type=policy_text_parse`。只查 `ads.policy_text_parse.summary`。请求不调用 `parse.run` | §4.4：请求只查询，避免清空整表 | 一致 |
| 浏览器 | 只打 `/display/v1/policy/**`。不把 `/topic/v1/policy`、`/v1/policy/**` 写成入口 | §2 | 一致 |
| display | 不直连 Python，不直连库。焦点和摘要只提交 `POST /topic/v1/analysis/tasks`，`PolicyAnalysisAdapterImpl` 再调 `POST /internal/policy/jobs/execute` | §2 | 一致 |

交接表与分册第 1–6 节同口径。机遇条数留在 `counts` 已有读面，不挂进 223–226。序号 222、227–231 不进本分册。接口不直接返回写死的 mock，不用 501 充当这四叶的画面。

阻断句：无。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。
