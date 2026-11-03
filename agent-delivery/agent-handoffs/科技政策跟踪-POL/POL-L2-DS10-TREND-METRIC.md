ponytail: off

# POL-L2-DS10-TREND-METRIC · 科创政策全景政策动向指标设计

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| 说明 | 任务开工时已是 `in_progress`。本叶不再认领，不调用 task-registry 写工具，不改 `task-registry.yaml`。定义单。只写 203–206 的指标挂接。不写代码，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过已有 `metric_id`、缺项表、D4=`mock` 和 QPOL-07。

## 范围与实现

科创政策全景 · 二级「政策动向跟踪」。只覆盖 SRS 序号 203–206，用户故事 `US-DS-POL-02`。挂接以已签收的 `POL-L2-DS10-TREND-ARCH` 和说明书第 11 节为准。

| 序号 | 叶子 | 指标 |
|---|---|---|
| 203 | 政策来源监控与更新 | 没有 `metric_id`，不新造。跨项索引，读已有入库 |
| 204 | 政策订阅服务 | 不是指标。不新造。不建缺项表 |
| 205 | 重点领域政策分析 · 趋势 | 只用已有 `M_POLICY_TIMESERIES`。数值从已有表读。D4 仍是 mock。D2 provisional 保留待核验 |
| 205 | 热点、影响、深度报告 | 没有已挂 `metric_id`，不新注册。读三张 `gapfill_` 表。`gap_item` 写序号和叶子名 |
| 206 | 时间轴、趋势 | 只用已有 `M_POLICY_TIMESERIES`。D4 仍是 mock。D2 provisional 保留待核验 |
| 206 | 地域热力 | 只用已有 `M_POLICY_NATIONAL_DIST`。不另开地域指标，不改挂评价页 219。D4 仍是 mock |
| 206 | 主题分布 | 没有已挂 `metric_id`，不新注册。读 `gapfill_policy_theme_dist` |

去重后本二级只用上述 2 个已有 `metric_id`，类型都是 STAT。八件套来自 2026-11-03 的 `metric-get`。科创发展、人才引进、资金扶持是筛选条件，不写成三条新指标。QPOL-07 不闭合。

不改挂 `M_POLICY_FOCUS_INDEX`、`M_POLICY_IMPLEMENTATION_EFFECT`、`M_POLICY_SIMULATE`。

读面沿 `POL-L2-DS10-TREND-ARCH`：趋势、时间轴、地域热力走已有 `stats`；来源监控走已有 `ingest`；订阅由展示委托 `gkxlumen-topic-policy`；热点、影响、深度报告和主题分布读 `gkxlumenx_gapfill`。本叶不改这条路径，不写算法实现。

## 偏离

DoD「未注册模型保持 501」已过时。2026-11-03 `human:淮政玮` 签收的动向架构，以及说明书第 11.1 节，改为读 `gapfill_` 表。205 热点、205 政策影响评估、205 深度分析报告、206 主题分布没有已挂 `metric_id`，本叶不新注册，不用 501 充当这几块。`gap_item` 分别为 `205 热点识别`、`205 政策影响评估`、`205 深度分析报告`、`206 主题分布`。`metric_id` 列留空。D4 仍是 mock。

说明书第 2 节和 `sdd/指标与501.md` 仍把热点、影响、深度报告写成 501，本叶不改那两份文件。

204 在 `指标与501.md` 写成 501。本叶定为不是指标。第 11 节要求走专题门面、不灌假订阅。204 不建缺项表。

203 没有 `metric_id`，与说明书第 2 节的跨项索引一致，不新造。

`M_POLICY_TIMESERIES`、`M_POLICY_NATIONAL_DIST` 的 D4 保持 mock，本叶未改。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-TREND-METRIC.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-TREND-METRIC.md`

未改指标 seed、矩阵、说明书、调研分册、架构稿、`task-registry.yaml`。未写代码。未 git commit，未 push。

## 验收证据

- `metric-get`：`M_POLICY_TIMESERIES`、`M_POLICY_NATIONAL_DIST` 均 `found.seed=true`、`found.matrix=true`，D1=`aligned`，D2=`partial` 且 `d2_assessed=provisional`，D4=`mock`，`algorithm_type`=STAT。时序 D3=`partial`，全国分布 D3=`full`。
- `metric-get`：`M_POLICY_FOCUS_INDEX`、`M_POLICY_IMPLEMENTATION_EFFECT`、`M_POLICY_SIMULATE` 均为 MODEL、D4=`mock`。本二级不改挂。
- 指标设计稿与本 handoff 已落在工作区。定义单，无业务 PR，无 pipeline。
- 未改任务状态。任务保持 `in_progress`。不标 done。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单不写算法实现。已有 STAT 仍由 Python 计算，Java 不打分。缺项四块不进 Python |
| 调用链 | ✅ 沿架构稿。浏览器只打 `/display/v1/policy/**`。本单不改链，展示不直连 Python |
| 图谱 | ✅ 本二级不读图，不写 nGQL |
| 可观测 | ✅ 不新设计观测点，沿既有展示链 |
| D9 | ✅ 只用已注册的两条 metric_id。八件套与 D1–D4 分开写。D4 保持 mock。未注册叶子不新造 id |
| D16 | ✅ 热点、影响、深度报告、主题分布只接受 `gkxlumenx_gapfill` 的 `gapfill_` 表。`metric_id` 留空，`gap_item` 写序号和叶子名。本单不建表、不灌数 |
| D18 | ✅ 做不到的块由接口读缺项表。不用 501 充当这几块，不在返回语句里写死 mock |
| D12 | ✅ 不把展示调用链改去 demo 服务。注册表里的 demo 计算文件只作索引，本单不改、不调用 |
| D17 | ✅ 不改唐绍祖锁定的合规算法。本单不写算法实现 |
| D14 | ✅ 本单不写对象存储 |
| CI/CD | ✅ 定义文档只落工作区。未 commit，未 push，未 force |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.05 |
| cost_warn | green |

无控制台分项。按本单 `estimated_tokens` 8000、algorithm 75/25、B 档 `$3/$15` 回填：`8000×0.75×3/1e6 + 8000×0.25×15/1e6 = 0.048`，记 `0.05`。定义单，未改注册表成本字段。

## 修改内容

- `sdd/l2/POL-L2-DS10-TREND-METRIC.md`
- 本 handoff
