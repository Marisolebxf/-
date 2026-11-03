# POL-L2-DS10-SENT-API · 科创政策全景 · 政策舆情评估 · 后台接口设计

ponytail: off

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 认领已完成。本单只写接口设计分册。不改注册表，不标 done |

## 范围

科创政策全景 · 二级「政策舆情评估」。SRS 序号 207–212。用户故事 `US-DS-POL-03`。

本分册是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不写实现代码，不写 OpenAPI 字段表、DTO、枚举闭包。

浏览器只打 `/display/v1/policy/**`。DoD「不复用 `/topic/v1/policy`」指浏览器不改打专题 URL。内部委托不算违反。不改 `ARCH-DISPLAY-01`。`E-E7-POLICY-M1-L06` 不是展示联调单。

| 序号 | 落点 |
|---|---|
| 207 | `GET panorama/stats`、`search`、`{id}/detail`。同步。display 内部委托 topic-policy（metrics + indicators、search、`docs/{id}`）。无行则空，不造 0。并列查看是多次读正文 |
| 208 | 不设展示资源。只消费第 7 项已有子图，可空。Java 不写 nGQL |
| 209 | `POST panorama/jobs`。`sub_type=policy_effect`。已有 `polan.eval.effect.run` 后查 `ads.policy_effect`（`scope_type=region_effect`）及对应时序。该 sub_type 不走产业 VID XOR。无行则空 |
| 212 | 同一 `jobs`。`sub_type=policy_match`。已有 `polan.text.match.run` 后查 `ads.policy_match`。无行则空。不返回演示分。没有外发通道则推送记录为空 |
| 210 | `GET panorama/feedback`。element 只读 `gapfill_policy_audience_feedback`。无行则空列表。不进专题政策门面 |
| 211 | `GET panorama/assessment-report`。element 只读 `gapfill_policy_assessment_report`。下载内容来自该行。不新建桶 |

209、212：display → `gkxlumen-topic-async-service` `POST /topic/v1/analysis/tasks`（浏览器不打 `/topicAsync`）→ `PolicyAnalysisAdapterImpl` → `POST /internal/policy/jobs/execute`。切条件不自动起任务。Job 失败不清空 207 已返回的统计、目录和正文。不用 501 充当功能。

## 与架构的对应

上游 `sdd/l2/POL-L2-DS10-SENT-ARCH.md` 已于 2026-11-03 由 `human:淮政玮` 签收。本分册按该稿第 2–4 节写路径和委托，不改架构稿。

- 207 对应架构 §4.1，并复用 `POL-L2-DS10-QRY-API` 已写的三条同步资源，不重列参数
- 208 对应架构 §4.2，确认不设资源
- 209、212 对应架构 §4.3、§4.6，把已有 ADS 查询写成 `panorama/jobs` 的两个 sub_type
- 210、211 对应架构 §4.4、§4.5，展示不直连库，element 只读两张 `gapfill_` 表
- 契约输入清单里上述资源行只作路径对照。清单末列的旧空态不覆盖签收读法：无行则空

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-SENT-API.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-SENT-API.md`

## 架构合规

| 铁律 | 结果 |
|---|---|
| 调用链 | 浏览器只打 `/display/v1/policy/**`。207 内部委托 `gkxlumen-topic-policy`。209、212 内部委托 `gkxlumen-topic-async-service`，再进 `POST /internal/policy/jobs/execute`。210、211 由 `gkxlumen-element` 只读 gapfill。208 不设资源 |
| 不直连 Python | `gkxlumen-display` 不直连 Python，不直连 `gkx_search_service`，不打 `/v1/policy/match` 或 `/v1/policy/analysis/effect`。Java 不打分，不写 nGQL |
| D12 | 不调用 `demo-*` 服务。算法中台页面不是展示实现。`run()` 用 lumen 仓已有实现 |
| D14 | 211 的下载内容来自缺项表该行。不新建桶，不走 `report/jobs` |
| 不改 D4 | 不新造 `metric_id`。207、208、209、210、211、212 的 D4 保持 mock。不把灌数写成已上线 |

## ponytail

ponytail: off

定义任务。未用 YAGNI 删掉调用链、空态和内部委托。

## 会签态

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS10-SENT-ARCH-SEQ` |
| 图 diff | 本分册不改图。沿用 SENT-ARCH 第 2 节 |
| 会签态 | 源文件无 frontmatter，记 `draft` |
| 本单 | 会签未做。不写会签通过。不标 done |

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
- 未改 QRY-API、QRY-ARCH、TREND-ARCH、SENT-ARCH 及任何兄弟分册
- 未调 task-registry，未改 `task-registry.yaml`
- 未 commit，未 push
- 未写业务代码，未另建 API-POL
