# POL-L2-DS10-CMP-API · 科创政策全景 · 政策重点比对 · 后台接口设计

ponytail: off

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 认领已完成，状态保持 in_progress。本单只写接口设计分册。不改注册表，不标 done |

## 范围

科创政策全景 · 二级「政策重点比对」。SRS 序号 213–218。用户故事 `US-DS-POL-04`。

本分册是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不写实现代码，不写 OpenAPI 字段表、DTO、枚举闭包。不新开资源。

浏览器只打 `/display/v1/policy/**`。DoD「不复用 `/topic/v1/policy`」指浏览器不改打专题 URL。内部委托不算违反。不把 `/topic/v1/policy` 或 `/v1/policy` 写成对外入口。不改 `ARCH-DISPLAY-01`。`E-E7-POLICY-M1-L06` 不是展示联调单。`gkxlumen-display` 不直连 Python，不直连库。

| 序号 | 落点 |
|---|---|
| 213 | `GET panorama/version-diff`。同步。element 只读 `gapfill_policy_version_diff`。时点是已有发布时间。无行则空，不返回写死差异 |
| 214 正文 | `GET panorama/search` 与 `{id}/detail`。同步。正文委托 topic-policy。受理部门读正文，不读部门缺项表 |
| 214 条件、材料 | 同一次 `{id}/detail`。element 只读 `gapfill_policy_detail_compare`。无行则该列空 |
| 214 力度分 | `POST panorama/jobs`。`sub_type=policy_intensity`。display 只提交 `POST /topic/v1/analysis/tasks`。未挂上白名单则结果空，不返回演示分 |
| 215 | `GET panorama/stats`。区域、类别委托 topic-policy。实施部门由 element 只读 `gapfill_policy_impl_dept`。总件数仍是 `M_POLICY_TOTAL_COUNT`。无行则空，不造 0 |
| 216 | 同一条 `GET panorama/stats`。同步。element 只读 `ads.policy_intensity` 的 `M_POLICY_SUPPORT_STRENGTH`。不进 Job。无行则该卡空，不造 0 |
| 217 | `GET panorama/benchmark-report`。同步。element 只读 `gapfill_policy_benchmark_report`。不内嵌写死的 PDF |
| 218 | 同一条 `POST panorama/jobs`。`sub_type=policy_intensity`。无行则图空，不返回演示序列 |

## 与架构的对应

上游 `sdd/l2/POL-L2-DS10-CMP-ARCH.md` 已于 2026-11-03 由 `human:淮政玮` 签收。本分册按该稿和当日会签修订写路径和委托，不改架构稿。

- 213 对应架构 §5.1：`version-diff` 同步，element 只读 `gapfill_policy_version_diff`，时点用已有发布时间
- 214 对应架构 §5.2：正文走 topic-policy；条件与材料在同一次 detail 由 element 读 `gapfill_policy_detail_compare`；力度分走 `jobs` 的 `policy_intensity`
- 215 对应架构 §5.3：`stats` 上区域和类别委托 topic-policy，实施部门读 `gapfill_policy_impl_dept`，总件数仍是 `M_POLICY_TOTAL_COUNT`
- 216 对应架构 §5.4 与会签修订：`stats` 同步读 `M_POLICY_SUPPORT_STRENGTH`，不进 Job
- 217 对应架构 §5.5：`benchmark-report` 只读 `gapfill_policy_benchmark_report`，导出从读到的行生成
- 218 对应架构 §5.6：与 214 力度分共用 `jobs`，读 `ads.policy_intensity`，不建可视化缺项表
- 会签修订：缺项表走 `gkxlumen-element`；力度 Job 只提交 `gkxlumen-topic-async-service` 的 `POST /topic/v1/analysis/tasks`；216 留在 `GET panorama/stats`
- 契约输入清单里上述资源行只作路径对照。清单里的「未见」不覆盖签收读法：无行则空

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-CMP-API.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-CMP-API.md`

## 架构合规

| 铁律 | 结果 |
|---|---|
| 调用链 | 浏览器只打 `/display/v1/policy/**`。正文、区域、类别内部委托 `gkxlumen-topic-policy`。缺项表与 216 的支持力度由 `gkxlumen-element` 只读。214、218 内部委托 `gkxlumen-topic-async-service`，再进 `POST /internal/policy/jobs/execute` |
| 不直连 Python | `gkxlumen-display` 不直连 Python，不直连库，不直接打 `jobs/execute`，不打 `/v1/policy/**`。Java 不打分，不写 nGQL |
| D12 | 不调用 `demo-*` 服务。算法中台页面不是展示实现。`run()` 用 lumen 仓已有实现 |
| D14 | 217 的文件从当次读到的行生成。不新建桶，不内嵌写死的 PDF，不走 `report/jobs` |
| D18 | 做不到的只读缺项表或已有 ADS。接口不直接返回写死差异、分数或报告 |
| 不改 D4 | 不新造 `metric_id`。215、216 的 D4 保持 mock。不把灌数写成已上线 |

## ponytail

ponytail: off

定义任务。未用 YAGNI 删掉调用链、空态、element 只读和 216 不进 Job 的边界。

## 会签态

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS10-CMP-ARCH-SEQ` |
| 图 diff | 本分册不改图。沿用 CMP-ARCH 第 2 节（会签修订后的 element 与 analysis/tasks） |
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
- 未改 CMP-ARCH、QRY-API、SENT-API、TREND-API 及任何兄弟分册
- 未调 task-registry，未改 `task-registry.yaml`，未改任务状态
- 未写业务代码，未另建 API-POL，未新开资源
