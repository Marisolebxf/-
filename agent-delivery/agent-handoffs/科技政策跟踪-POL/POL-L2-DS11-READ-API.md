# POL-L2-DS11-READ-API · 政策分析评价 · 结果解读报告多维展示 · 后台接口设计

ponytail: off

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| lock_hours | 24 |
| 说明 | 认领已完成，状态经 claimed 进入 in_progress。本单只写接口设计分册。不标 done，不标 ready_to_sign |

## 范围

政策分析评价 · 二级「结果解读报告多维展示」。SRS 序号 223–226。用户故事 `US-DS-POL-05`。

本分册是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不写实现代码，不写 OpenAPI 字段表、DTO、枚举闭包。

浏览器只打 `/display/v1/policy/**`。对外只有三条：`GET evaluation/counts`、`GET evaluation/shells`、`POST evaluation/jobs`。`jobs` 上本二级只定 `policy_focus_ads` 与 `policy_text_parse`。

| 序号 | 落点 |
|---|---|
| 223 短板 | `GET evaluation/counts`。同步。element 只读 `ads.policy_effect` 且 `scope_type=region_gap` 的 `shortboard_cnt`。GET 不调用 `gap.run`。无行则计数空，不造 0 |
| 223 焦点 | `POST evaluation/jobs`。`sub_type=policy_focus_ads`。调用已有 `polan.eval.focus.run` 后读 `ads.policy_focus` 且 `policy_id` 非空。不走产业 VID XOR，不收 items |
| 224、225 | `GET evaluation/shells`。同步。element 只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell` 的解读条目与多媒体条目。点选只筛选已返回行。不返回视频、动画、PDF、模板字节 |
| 226 | 同一 `jobs`。`sub_type=policy_text_parse`。只查 `ads.policy_text_parse.summary`。请求不调用 `parse.run`。不走产业 VID XOR，不收 items |

`counts` 上已有的机遇读面不改。既有 `policy_focus` 仍走 harness，不改它。

jobs 内部链：`gkxlumen-display` → `POST /topic/v1/analysis/tasks` → `PolicyAnalysisAdapterImpl` → `POST /internal/policy/jobs/execute`。这是内部委托。切条件不自动起任务。Job 失败不清空已经返回的 counts 和 shells。不用 501 充当功能。接口不直接返回写死的 mock。

## 偏离

- DoD「不复用 `/topic/v1/policy`」指浏览器不改打专题 URL。display 内部委托 `POST /topic/v1/analysis/tasks` 不算违反。浏览器仍只打 `/display/v1/policy/**`。
- DoD 原文写着「焦点/解读/多媒体/摘要 501」。`指标与501.md` 仍把 223 焦点、224、225、226 写成 501。已签收的 `POL-L2-DS11-READ-ARCH` 把这些改成读表。本分册按签收架构写空态：无行则空，不返回 501。不回头改 DoD 所在的上游文件，不改 VIZ、PLAN。
- 223 短板本来是可接统计读面，不是那句 501。无行仍是计数空，不造 0。

## 与架构的对应

上游 `sdd/l2/POL-L2-DS11-READ-ARCH.md` 已于 2026-11-03 由 `human:淮政玮` 签收。本分册按该稿第 2–4 节写路径和委托，不改架构稿。

- 223 短板对应架构 §4.1 同步链，写成 `evaluation/counts`
- 223 焦点对应架构 §4.1 Job 链，写成 `evaluation/jobs` 的 `policy_focus_ads`
- 224、225 对应架构 §4.2、§4.3，展示不直连库，element 只读 `gapfill_policy_eval_shell`
- 226 对应架构 §4.4，写成同一 `jobs` 的 `policy_text_parse`，请求只查询
- 契约输入清单里上述资源行只作路径对照。清单和指标与 501 里的旧 501 空态不覆盖签收读法

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-READ-API.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-READ-API.md`

## 未做

- 未改代码，未改 Python，未改 Java
- 未建表，未灌数，未写 DDL。`POL-L2-DS11-READ-GAPFILL-L01` 与 `POL-L2-DS11-READ-DATA` 不在本单执行
- 未冻结枚举、响应字段名和 DTO
- 未改说明书、WBS、契约输入清单、调用链与边界、`指标与501.md`、调研、VIZ、PLAN、`FE-POL-02A`
- 未新建前端单，未会签
- 未 commit，未 push
- 无业务 CI。定义单不部署

## 验收

- 分册已落盘，三条资源的路径、方法、同步或 Job、内部委托、空态与已签收架构一致
- 偏离已写明：501 改为读表；`/topic/v1/analysis/tasks` 只作内部委托
- 空态是空。短板不造 0。不返回 501。接口不直接返回写死的 mock
- 未改本单范围外的文件
- 待 `human:淮政玮` 签收。状态停在 integration，不进入 ready_to_sign，不进入 done

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/**`。counts、shells 由 `gkxlumen-element` 只读。jobs 内部委托 `gkxlumen-topic-async-service` 的 `POST /topic/v1/analysis/tasks`，再进 `POST /internal/policy/jobs/execute`。Java 不算法 |
| 不直连 | ✅ `gkxlumen-display` 不直连库，不直连 Python，不写 nGQL，不打 `/v1/policy/**` |
| D12 | ✅ 不调用 `demo-*`。不嵌算法中台页。`run()` 用 lumen 仓已有实现，不抄进 Java |
| D14 | ✅ shells 不返回视频、动画、PDF、模板字节。不新建桶，不写对象存储，前端不直连 RustFS |
| D16 / D18 | ✅ 223、226 读已有 ADS，不另建表。224、225 只点名 `gapfill_policy_eval_shell`，建表灌数不在本单。不建 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`。无行则空。接口不直接返回 mock，不用 501 充当功能 |
| D9 | ✅ 不新造 `metric_id`。不改 D4。不把 mock 写成已上线。`QPOL-02` 与 `GDF-POLICY-MOCK-GATE-L01` 仍按架构稿保持未闭合 |
| 可观测 | ✅ trace 沿既有展示链和已有异步任务链。本分册不新设计观测点 |

## ponytail

ponytail: off

定义任务。未用 YAGNI 删掉调用链、空态、偏离和内部委托。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS11-READ-ARCH-SEQ` |
| 图 diff | 本分册不改图。沿用 READ-ARCH 第 2 节 |
| 会签态 | 源文件无 frontmatter，记 `draft` |
| 本单 | 会签未做。不把本单写成已会签。不标 done |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |
| user_story | `US-DS-POL-05` |
