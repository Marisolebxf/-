ponytail: off

# POL-L2-DS10-CMP-METRIC · 科创政策全景政策重点比对指标设计

- 任务：`POL-L2-DS10-CMP-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 用户故事：`US-DS-POL-04`
- 上游：`sdd/l2/POL-L2-DS10-CMP-ARCH.md`（2026-11-03 已签收，签收人 human:淮政玮）
- 会签态：未会签

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| 说明 | 任务开工时已是 `in_progress`。本叶不再认领，不调用 task-registry 写工具，不改 `task-registry.yaml`，不改任务状态。定义单。只写 213–218 的指标挂接。不写代码，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过已有 `metric_id`、缺项表行、D4=`mock`、QPOL-02 和未会签。

## 范围与实现

科创政策全景 · 二级「政策重点比对」。只覆盖 SRS 序号 213–218，用户故事 `US-DS-POL-04`。指标身份沿说明书第 2 节与 `sdd/指标与501.md` 213–218 行已有 `metric_id`。读面沿已签收的 `POL-L2-DS10-CMP-ARCH`。本叶不改这两份上游，不新造 `metric_id`，不改 D4。

| 序号 | 叶子 | 指标 |
|---|---|---|
| 213 | 政策新旧对比 | 没有 `metric_id`，不新造，不写公式。页面读 `gapfill_policy_version_diff` 的行。行内文字不是指标结果 |
| 214 | 政策详情对比 | 只挂 `M_POLICY_INTENSITY_SCORE`。MODEL。D4 仍是 mock。走 `jobs`，`sub_type=policy_intensity`。未接通则该格空，不补演示分。不挂力度指数 |
| 215 | 部门政策对比 | 只挂 `M_POLICY_TOTAL_COUNT`。STAT。D4 仍是 mock。部门件数在 `gapfill_policy_impl_dept`，不登记成新指标 |
| 216 | 标杆比对功能 | 只挂 `M_POLICY_SUPPORT_STRENGTH`。COMPUTE。D4 仍是 mock。同步 `stats`，不进 Job。金额档缺失则该维空 |
| 217 | 对标报告生成与导出 | 没有 `metric_id`，不新造，不写公式。页面读 `gapfill_policy_benchmark_report` 的行。行内文字不是指标结果 |
| 218 | 对标结果可视化展示 | 只挂 `M_POLICY_INTENSITY_SCORE`。MODEL。D4 仍是 mock。走 `jobs`。未接通则图空，不补演示分。不挂力度指数 |

去重后本二级只用上述 3 个已有 `metric_id`。八件套来自 2026-11-03 的 `metric-get`。214、218 的展示读数指向仓库里已有的 `polan.eval.intensity.run`，不重写公式，不改这份代码。

## 挂接表

| 序号 | metric_id | MCP 中文名 | algorithm_type | D4 |
|---|---|---|---|---|
| 213 | （无） | — | — | 无注册指标，不改 D4 |
| 214 | `M_POLICY_INTENSITY_SCORE` | 政策力度评分 | MODEL | mock |
| 215 | `M_POLICY_TOTAL_COUNT` | 政策总数 | STAT | mock |
| 216 | `M_POLICY_SUPPORT_STRENGTH` | 支持力度 | COMPUTE | mock |
| 217 | （无） | — | — | 无注册指标，不改 D4 |
| 218 | `M_POLICY_INTENSITY_SCORE` | 政策力度评分 | MODEL | mock |

不新造指标。不改 D4。不挂 `M_POLICY_INTENSITY_INDEX`。

## 偏离

无新 `metric_id`。中文名与叶子名不一致时以 MCP 为准，见上表。

DoD「未注册模型保持 501」相对已签收架构已经过时。说明书第 2 节和 `指标与501.md` 仍把 213、217 写成 501，把 214、218 的判定列写成 501、页面空态。说明书第 11.2 节仍把重点比对放在未开工二级。本叶不改那两份文件。读面按已签收架构：213、217 读缺项表行，行内文字不是指标结果；214、218 走 `jobs` 读 `ads.policy_intensity` 的力度分，未接通则空，不补演示分；216 同步 `stats`，不进 Job，金额档缺失则该维空。

`M_POLICY_TOTAL_COUNT` 的需求来源页就是序号 215。197、207 的复用留在原叶，本叶不改 `srs_refs`。部门件数不改挂成这条总数。

`M_POLICY_INTENSITY_SCORE` 的需求来源含 02/214 与 02/218，另有专题 05/167。本叶只在这两叶使用。`M_POLICY_SUPPORT_STRENGTH` 的需求来源含 02/216 与 05/167，只挂 216。

`metric-get` 核对 `M_POLICY_INTENSITY_INDEX`：政策力度指数，MODEL，D1=`aligned`，D4=`mock`，需求来源只有专题 05/167。214、218 不挂。QPOL-02 不闭合。

本叶未会签。不写会签通过。不标 done。不改任务状态。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-CMP-METRIC.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-CMP-METRIC.md`

未改指标 seed、矩阵、说明书、`指标与501.md`、`CMP-ARCH`、QRY/SENT/TREND 分册、`task-registry.yaml`。未写代码。未新注册指标。未改 D4。

## 验收证据

- `metric-get`：`M_POLICY_INTENSITY_SCORE` 为 MODEL，`M_POLICY_TOTAL_COUNT` 为 STAT，`M_POLICY_SUPPORT_STRENGTH` 为 COMPUTE。三条均 `found.seed=true`、`found.matrix=true`、`found.srs_map=true`。D1=`aligned`，D2=`partial` 且 `d2_assessed=provisional`，D4=`mock`，`is_mock=true`。总数 D3=`full`，力度评分与支持力度 D3=`partial`。
- `metric-get`：`M_POLICY_INTENSITY_INDEX` 为 MODEL、D4=`mock`，需求来源只有专题 05/167。本二级不挂。
- 指标设计稿与本 handoff 已落在工作区。定义单，无业务 PR，无 pipeline。
- 未改任务状态。任务保持 `in_progress`。未会签。不标 done。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单不写算法实现。214、218 只指向已有 `polan.eval.intensity.run`。Java 不打分 |
| 调用链 | ✅ 沿已签收架构稿。浏览器只打 `/display/v1/policy/**`。力度 Job 经 `gkxlumen-topic-async-service` 再进 `/internal/policy/jobs/execute`。216 同步 `stats`，不进 Job。本单不改链 |
| 图谱 | ✅ 本二级不读图，不写 nGQL |
| 可观测 | ✅ 不新设计观测点，沿既有展示链 |
| D9 | ✅ 只用已注册的三条 metric_id。八件套与 D1–D4 分开写。D4 保持 mock。213、217 不新造 id。不挂力度指数 |
| D16 | ✅ 213、217、214 的条件与材料、215 的实施部门只接受 `gkxlumenx_gapfill` 的 `gapfill_` 表。行内文字不是指标结果。本单不建表、不灌数 |
| D18 | ✅ 214、216、218 读已有 `ads.policy_intensity`。做不到的块由接口读缺项表。未接通不补演示分，不在返回语句里写死 mock |
| D12 | ✅ 不把展示调用链改去 demo 服务。注册表里的 demo 计算文件只作索引，本单不改、不调用 |
| D17 | ✅ 不改唐绍祖锁定的合规算法。本单不写算法实现 |
| D14 | ✅ 本单不写对象存储。217 的导出不落桶 |
| CI/CD | ✅ 定义文档随本次提交推 `origin/dev`。无业务 pipeline。未 force |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.05 |
| cost_warn | green |

无控制台分项。按本单 `estimated_tokens` 8000、algorithm 75/25、B 档 `$3/$15` 回填：`8000×0.75×3/1e6 + 8000×0.25×15/1e6 = 0.048`，记 `0.05`。定义单，未改注册表成本字段。

## 修改内容

- `sdd/l2/POL-L2-DS10-CMP-METRIC.md`
- 本 handoff

未会签。不新造指标，D4 保持 mock。213、217 读缺项表行。214、218 只挂力度评分并走 jobs。215 只挂政策总数。216 只挂支持力度并同步读 stats。
