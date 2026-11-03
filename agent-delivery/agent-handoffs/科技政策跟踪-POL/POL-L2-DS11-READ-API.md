# POL-L2-DS11-READ-API · 政策分析评价 · 结果解读报告多维展示 · 后台接口设计

ponytail: off

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 认领已完成，状态保持 in_progress。本单只写接口设计分册。不改注册表，不标 done |

## 范围

政策分析评价 · 二级「结果解读报告多维展示」。SRS 序号 223–226。用户故事 `US-DS-POL-05`。

本分册是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不写实现代码，不写 OpenAPI 字段表、DTO、枚举闭包。不新开资源。

浏览器只打 `/display/v1/policy/**`。DoD「不复用 `/topic/v1/policy`」指浏览器不改打专题政策 URL。内部提交 `POST /topic/v1/analysis/tasks` 不算违反。不把 `/topic/v1/policy` 或 `/v1/policy/**` 写成对外入口。不改 `ARCH-DISPLAY-01`。`E-E7-POLICY-M1-L06` 不是展示联调单。`gkxlumen-display` 不直连 Python，不直连库。

| 序号 | 落点 |
|---|---|
| 223 短板 | `GET evaluation/counts`。同步。element 只读 `ads.policy_effect` 里 `scope_type=region_gap` 的 `shortboard_cnt`。这次 GET 不调用 `gap.run`。无行则计数空，不造 0 |
| 223 焦点 | `POST evaluation/jobs`。Job。`sub_type=policy_focus_ads`。display 只提交 `POST /topic/v1/analysis/tasks`。适配器再调 `jobs/execute`。调用已有 `focus.run` 后读 `ads.policy_focus`。旧键 `policy_focus` 仍走 harness，不改旧键。无行则焦点块空 |
| 224 | `GET evaluation/shells`。同步。element 只读 `gapfill_policy_eval_shell` 的解读条目。点选只筛选已返回的行。无行则解读块空 |
| 225 | 同一条 `GET evaluation/shells`。同步。只读多媒体条目的标题和一句说明。不灌视频，不灌模板选用。无行则该块空 |
| 226 | 同一条 `POST evaluation/jobs`。Job。`sub_type=policy_text_parse`。display 只提交 `analysis/tasks`。只查 `ads.policy_text_parse.summary`。请求不调用 `parse.run`（`run` 会清空整表）。无行则摘要空 |

机遇条数留在 `counts` 已有读面，不挂进 223–226。序号 222、227–231 不进本分册。四叶无行则空，不写死 mock，不用 501 充当画面。

## 与架构的对应

上游 `sdd/l2/POL-L2-DS11-READ-ARCH.md` 按本单派令已签收。会签页 `sdd/l2/会签/POL-L2-DS11-READ-SIGNOFF-ARCH.md` 同意。本分册按该稿写路径和委托，不改架构稿，不改会签页。

- 223 短板对应架构 §4.1：`GET evaluation/counts` 同步，element 只读 `ads.policy_effect` 的 `region_gap.shortboard_cnt`，这次 GET 不调用 `gap.run`
- 223 焦点对应架构 §4.1：`POST evaluation/jobs`，`sub_type=policy_focus_ads`，调用已有 `polan.eval.focus.run` 后读 `ads.policy_focus`。旧 `policy_focus` 仍走 harness
- 224、225 对应架构 §4.2、§4.3：`GET evaluation/shells` 同步，element 只读 `gapfill_policy_eval_shell`。不灌视频，不灌模板选用
- 226 对应架构 §4.4：同一条 `jobs`，`sub_type=policy_text_parse`，只查 `ads.policy_text_parse.summary`。请求不调用 `parse.run`
- 会签页：display 只提交 `POST /topic/v1/analysis/tasks`，适配器再调 `POST /internal/policy/jobs/execute`。浏览器只打 `/display/v1/policy/**`
- 机遇条数留在 `counts` 已有读面。222、227–231 不进本分册
- 契约输入清单里上述资源行只作路径对照。清单里的「未见」和 501 列不覆盖签收读法：无行则空

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-READ-API.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-READ-API.md`

## 架构合规

| 铁律 | 结果 |
|---|---|
| 调用链 | 浏览器只打 `/display/v1/policy/**`。223 短板与 224、225 由 `gkxlumen-element` 只读。223 焦点与 226 内部委托 `gkxlumen-topic-async-service` 的 `POST /topic/v1/analysis/tasks`，再进 `POST /internal/policy/jobs/execute` |
| 不直连 Python | `gkxlumen-display` 不直连 Python，不直连库，不直接打 `jobs/execute`，不打 `/v1/policy/**`。Java 不算指数，不写 nGQL |
| D12 | 不调用 `demo-*` 服务。算法中台页面不是展示实现。`focus.run` 用 lumen 仓已有实现。226 的请求不调用 `parse.run` |
| D14 | 225 不灌视频，不写对象存储，前端不直连 RustFS |
| D18 | 223、226 读已有 ADS。224、225 只读一张 gapfill 表。接口不直接返回写死 mock。不用 501 充当这四叶的画面 |
| 不改 D4 | 不新造 `metric_id`。223、226 的 D4 保持 mock。不把灌数写成已上线。旧键 `policy_focus` 不改 |

## ponytail

ponytail: off

定义任务。未用 YAGNI 删掉调用链、空态、element 只读、`parse.run` 不进请求，以及与机遇条数、222、227–231 的边界。

## 会签态

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS11-READ-ARCH-SEQ` |
| 图 diff | 本分册不改图。沿用 READ-ARCH 第 2 节（短板与 shell 走 element；焦点 `policy_focus_ads` 与摘要 `policy_text_parse` 走 analysis/tasks） |
| 会签态 | 源文件无 frontmatter，记 `draft` |
| 本单 | 未会签。不写会签通过。不标 done |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | green |

定义单未跑控制台分项。cost 未计。`cost_warn` 记 green。

## 未改动

- 未改 WBS、说明书、契约输入清单、调用链与边界、指标与 501
- 未改 READ-ARCH、会签页及任何兄弟分册
- 未调 task-registry，未改 `task-registry.yaml`，未改任务状态
- 未写业务代码，未另建 API-POL，未新开资源
