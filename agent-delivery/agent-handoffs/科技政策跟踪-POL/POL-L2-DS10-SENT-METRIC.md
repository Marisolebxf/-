ponytail: off

# POL-L2-DS10-SENT-METRIC · 科创政策全景政策舆情评估指标设计

- 任务：`POL-L2-DS10-SENT-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 用户故事：`US-DS-POL-03`
- 上游：`sdd/l2/POL-L2-DS10-SENT-ARCH.md`（已签收）
- 会签态：`draft`

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| 说明 | 认领已完成。定义单。只写 207–212 的指标挂接。不写代码，不回写 registry，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过已有 metric_id、空态和 D4=mock。

## 范围与实现

科创政策全景 · 二级「政策舆情评估」。只覆盖 SRS 序号 207–212，用户故事 `US-DS-POL-03`。挂接沿 `sdd/指标与501.md` 全景表 207–212 行。读面沿已签收的 `POL-L2-DS10-SENT-ARCH`。本叶不改这两份上游，不新造 `metric_id`，不改 D4。

| 序号 | 叶子 | 指标 |
|---|---|---|
| 207 | 政策查询与对比 | 可接统计读面。`M_POLICY_TOTAL_COUNT`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST`。STAT。D4 仍是 mock。无独立对比模型。空不造 0。深度交叉对比不在本叶 |
| 208 | 区域政策差异性分析 | 跨项索引。`M_POLICY_GRAPH_107_1`。GRAPH。D4 仍是 mock。地区件数可借 `M_POLICY_NATIONAL_DIST`、`M_POLICY_SZ_DIST`，不把 208 改判成 STAT。支持力度不挂本叶 |
| 209 | 政策实施效果跟踪 | `M_POLICY_IMPLEMENTATION_EFFECT`。注册中文名「落地实效性」。MODEL。D4 仍是 mock。QPOL-02。读 `ads.policy_effect`（`scope_type=region_effect`）和时序里该 id。无行则空。不用 501 充当功能 |
| 210 | 政策受众反馈收集 | 无已挂 `metric_id`。不新注册。缺项表 `metric_id` 留空 |
| 211 | 政策效果评估报告 | 无已挂 `metric_id`。不新注册。缺项表 `metric_id` 留空。不假挂成效果指标 |
| 212 | 政策匹配与推送 | `M_POLICY_MATCH`、`M_POLICY_INDUSTRY_FIT`。都是 MODEL。D4 仍是 mock。QPOL-03。同一张 `ads.policy_match`，一个 sub_type `policy_match`。推送和邮件不新挂指标 |

八件套来自 2026-11-03 的 `metric-get`。209、212 的展示读数指向仓库里已有的 `polan/eval/effect.py`、`polan/text/match.py`，不重写公式，不改这两份代码。主体是受控画像，不是企业库。演示页 35 分不是展示返回值。

## 挂接表

| 序号 | metric_id | MCP 中文名 | algorithm_type | D4 |
|---|---|---|---|---|
| 207 | `M_POLICY_TOTAL_COUNT` | 政策总数 | STAT | mock |
| 207 | `M_POLICY_TYPE_DIST` | 政策类型分布 | STAT | mock |
| 207 | `M_POLICY_LEVEL_DIST` | 政策级别分布 | STAT | mock |
| 208 | `M_POLICY_GRAPH_107_1` | 政策实体关系抽取 | GRAPH | mock |
| 209 | `M_POLICY_IMPLEMENTATION_EFFECT` | 落地实效性 | MODEL | mock |
| 210 | （无） | — | — | 无注册指标，不改 D4 |
| 211 | （无） | — | — | 无注册指标，不改 D4 |
| 212 | `M_POLICY_MATCH` | 政策匹配推送 | MODEL | mock |
| 212 | `M_POLICY_INDUSTRY_FIT` | 政策产业适配性 | MODEL | mock |

208 可借、不改判：`M_POLICY_NATIONAL_DIST`（全国政策分布，STAT，mock）、`M_POLICY_SZ_DIST`（深圳政策分布，STAT，mock）。

不新造指标。不改 D4。

## 偏离

无新 `metric_id`。中文名与叶子名不一致时以 MCP 为准，见上表。

`M_POLICY_TOTAL_COUNT` 的需求来源页是序号 215。本叶仍按 `指标与501` 与架构稿挂在 207，不改 `srs_refs`。

`M_POLICY_IMPLEMENTATION_EFFECT` 的需求来源含推演页 02/235。本叶不扩展那一页。`effect.run()` 写入 `ads.policy_effect` 时，行上 `metric_id` 列是 `M_POLICY_EFFECT_SCORE`；落地实效在时序表，`metric_id` 为 `M_POLICY_IMPLEMENTATION_EFFECT`。本叶不把效果评分改挂到 209。

`指标与501` 将 209、212 的判定列记为 501、页面空态。本叶不改那份文件。读面按已签收架构：无行则空，不用 501 充当功能。

`metric-query` 关键词「反馈」命中落地实效性，因为口径里有反馈维。210 不挂它。「推送」另命中 `M_POLICY_DS_11_POLICY_EVAL_012`（评价页 226，MODEL，D4=`mock`）。212 的通知和邮件不挂它。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-SENT-METRIC.md`
- 本 handoff

未改指标 seed、矩阵、说明书、`指标与501.md`、`SENT-ARCH`、QRY/TREND 分册、WBS、`task-registry.yaml`。未写代码。未提交 git。

## 验收证据

- `metric-get`：上表 207、208、209、212 的指标均 `found.seed=true`、`found.matrix=true`。D4 均为 `mock`。207 三条为 STAT，208 为 GRAPH，209 与 212 为 MODEL。
- `metric-get` 复核可借指标：`M_POLICY_NATIONAL_DIST`、`M_POLICY_SZ_DIST` 均为 STAT、D4=`mock`。
- `metric-get` 复核排除项，D4 仍为 `mock`：`M_POLICY_SUPPORT_STRENGTH`（COMPUTE）、`M_POLICY_EFFECT_SCORE`（MODEL）、`M_POLICY_DEEP_168_1`（MODEL）、`M_POLICY_DS_11_POLICY_EVAL_012`（MODEL）。本叶不挂。
- `metric-query`（domain=政策）：受众、问卷、意见征集、评估报告均为 0 条。210、211 无已挂 `metric_id`。
- 指标设计稿与本 handoff 已落盘。定义单，无业务 PR，无 pipeline。
- 会签态 `draft`。不写会签通过。不标 done。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单不改算法。209、212 只指向已有 `polan.eval.effect.run`、`polan.text.match.run` |
| 调用链 | ✅ 沿已签收架构稿。浏览器只打 `/display/v1/policy/**`。本单不改链 |
| 图谱 | ✅ 208 只消费已有子图，类型保持 GRAPH。不写 nGQL，不改判 STAT |
| 可观测 | ✅ 不新设计观测点，沿既有展示链 |
| D9 | ✅ 只用已注册 metric_id。八件套与 D1–D4 分开写。D4 保持 mock。210、211 不新造 id |
| D12 | ✅ 不把展示调用链改去 demo 页面。demo 与 vendor 中的计算文件只作已有实现指认，本单不改、不调用 |
| D16 / D18 | ✅ 209、212 读已有 ADS。210、211 的缺项表 `metric_id` 留空。不用 501 充当 209、212。本单不灌数 |
| D17 | ✅ 不改锁定算法，不改 `effect.py`、`match.py` |
| D14 | ✅ 本单不写对象存储 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | 未计 |

本定义单未回填成本，未改 task-registry。

## 修改内容

- `sdd/l2/POL-L2-DS10-SENT-METRIC.md`
- 本 handoff
