# POL-L2-DS10-SENT-ARCH · 科创政策全景政策舆情评估架构

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 只写政策舆情评估的实现架构。不标 done，不会签 |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过调用链、501 空态和与 197–206、213–218 的边界。

## 范围

科创政策全景 · 二级「政策舆情评估」。只覆盖 SRS 序号 207–212，用户故事 `US-DS-POL-03`。

| 序号 | 叶子 | 流程 |
|---|---|---|
| 207 | 政策查询与对比 | 同步，复用多维检索的门面委托 |
| 208 | 区域政策差异性分析 | 跨项读图，不新开资源 |
| 209 | 政策实施效果跟踪 | 当前 501。接通时复刻算法库效果评估 |
| 210 | 政策受众反馈收集 | 读 `gapfill_policy_audience_feedback`。mock 在表里，接口不直接返回 mock |
| 211 | 政策效果评估报告 | 读 `gapfill_policy_assessment_report`。mock 在表里，接口不直接返回 mock |
| 212 | 政策匹配与推送 | 当前 501。接通时复刻算法库匹配推送 |

207 读已有 `stats`、`search`、`{id}/detail`。浏览器只打 `/display/v1/policy/**`。`gkxlumen-display` 内部委托 `gkxlumen-topic-policy`。无行则空，不造 0。D4 仍是 mock。

208 不设资源。只消费第 7 项已有子图，挂接可空。不走 `E-E7-POLICY-M1-L06`。

209、212 走 `POST panorama/jobs`。正式 Python 未挂上时 501。接通后复刻算法库已有计算：209 用 `polan.eval.effect` 写 `ads.policy_effect`，212 用 `polan.text.match` 写 `ads.policy_match`。经 `gkxlumen-topic-async-service` 进 `/internal/policy`，不进专题政策门面，Java 不打分。

210 走 `feedback`，211 走 `assessment-report`。真实采集和真实报告做不到。只新建 `gkxlumenx_gapfill` 的两张 `gapfill_` 表，Python 把 mock 写入表，查询只 `SELECT`。接口不直接返回 mock。表空则空列表，不造行。

## 产物路径

`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-SENT-ARCH.md`

## 与相邻序号的边界

本叶不写 197–206、213–218 的流程。深度交叉对比不进 207。支持力度不进 208。推演页不展开 209 的同一指标。匹配推送不走 `share` 或 `subscriptions`。

## 未做事项

- 未写 OpenAPI 字段表
- 未新造 `metric_id`，未改 D4
- 未改前端单，未重开 GDF
- 未把 `E-E7-POLICY-M1-L06` 写成展示路径
- 未把本单标 done。会签不在本单

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS10-SENT-ARCH-SEQ` |
| 图 diff | 207 同步委托专题政策门面；208 只消费已有子图；209 复刻 `polan.eval.effect` 并读 `ads.policy_effect`，212 复刻 `polan.text.match` 并读 `ads.policy_match`；210、211 只查 `gkxlumenx_gapfill` 两张缺项表。禁止边：浏览器改打专题 URL、`L06`、本叶新开查图资源、本叶新指标、本叶新写打分公式、接口直接返回 mock |
| 会签态 | 本叶新图。源文件无 frontmatter，记 `draft`。不自填绿 |
| 说明 | 图在架构稿第 2 节 |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | green |

未回写注册表的成本字段。

## 修改内容

- 新增 `sdd/l2/POL-L2-DS10-SENT-ARCH.md`
- 新增本 handoff
