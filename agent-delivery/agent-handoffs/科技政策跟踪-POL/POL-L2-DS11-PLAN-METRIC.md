ponytail: off

# POL-L2-DS11-PLAN-METRIC · 政策分析评价推荐方案报告交互展示指标设计

- 任务：`POL-L2-DS11-PLAN-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md`（2026-11-03 已签收，签收人 human:淮政玮）
- 会签态：未会签

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| 说明 | 任务开工时已是 `in_progress`。本叶不再认领，不调用 task-registry 写工具，不改 `task-registry.yaml`，不改任务状态。定义单。只写 227–231 的指标挂接。不写代码，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过已有 `metric_id`、缺项表行、D4=`mock`、229 的 501 三档、布局推荐与推演的分界，以及未会签。

## 范围与实现

政策分析评价 · 二级「推荐方案报告交互展示」。只覆盖 SRS 序号 227–231，用户故事 `US-DS-POL-05`。指标身份沿说明书第 2 节与 `sdd/指标与501.md` 227–231 行已有 `metric_id` 和三档判定。读面沿已签收的 `POL-L2-DS11-PLAN-ARCH` 与 `sdd/l2/会签/POL-L2-DS11-PLAN-SIGNOFF-ARCH.md`。本叶不改这两份上游，不新造 `metric_id`，不改 D4。

| 序号 | 叶子 | 指标 |
|---|---|---|
| 227 | 多方案对比展示 | 没有专属 `metric_id`，不新造，不写公式。判定保持 501。读 `gapfill_policy_eval_scheme` 的方案对照行。行上 `metric_id` 留空。少于两行则对比空 |
| 228 | 方案参数自定义模拟 | 没有专属 `metric_id`，不新造，不写公式。判定保持 501。按方案和参数档读参数模拟行。请求内不按 `simulate.run` 现算。对不上则空 |
| 229 | 实施路径与风险辅助 | 只挂 `M_POLICY_DS_11_POLICY_EVAL_015`。GRAPH。判定保持 501。D4 仍是 mock。读路径与风险行。不读图。无行则空 |
| 230 | 互动意见收集与专家参与 | 没有专属 `metric_id`，不新造，不写公式。判定保持 501。读意见行。请求不插入 |
| 231 | 方案报告导出与归档 | 没有专属 `metric_id`，不新造，不写公式。判定保持 501。从当次读到的方案行和意见行生成导出。不灌文件 |

去重后本二级只用上述 1 个已有 `metric_id`。八件套来自 2026-11-03 的 `metric-get`。展示读数指向已有缺项行，不重写公式，不改计算代码。

## 挂接表

| 序号 | metric_id | MCP 中文名 | algorithm_type | D4 | 三档 |
|---|---|---|---|---|---|
| 227 | （无） | — | — | 无注册指标，不改 D4 | 501 |
| 228 | （无） | — | — | 无注册指标，不改 D4 | 501 |
| 229 | `M_POLICY_DS_11_POLICY_EVAL_015` | 实施路径与风险辅助 | GRAPH | mock | 501 |
| 230 | （无） | — | — | 无注册指标，不改 D4 | 501 |
| 231 | （无） | — | — | 无注册指标，不改 D4 | 501 |

不新造指标。不改 D4。无行则空，不写假公式。请求内不按 `simulate.run` 现算。

## 明确不挂

- `M_POLICY_SIMULATE`：政策效果推演。`metric-get` 为 MODEL、D4=`mock`，`srs_refs` 为空，`found.srs_map=false`。留在推演键。228 与 229 都不挂。五叶的请求不调用 `polan.text.simulate.run`。
- 布局推荐 `M_POLICY_LAYOUT_REC_COUNT`：政策布局建议条数（王惠对冲计数 v2 复现）。STAT，D4=`mock`。`srs_refs` 含展示 02/227、02/241 与专题 05/171。`指标与501` 仍把 227 写成未见专属指标，并写明不把布局建议条数写入本页。本叶不挂，不改 `srs_refs`。
- 布局推荐 `M_POLICY_DEEP_171_1`：政策布局推荐模型。MODEL，D4=`mock`。需求来源只有专题 05/171。不写入方案对照，不顶替 229。
- 序号 219–226、232–242：不进本五叶。241 的路径预测不顶替 229。`M_POLICY_DS_11_POLICY_EVAL_015` 不改挂到 241。
- `evaluation/counts` 上的短板条数、机遇条数：不在本二级。

## 偏离

无新 `metric_id`。229 的叶子名与注册中文名一致，都是「实施路径与风险辅助」。

DoD「未注册模型保持 501」按指标分册的三档保持。227、228、230、231 仍没有专属指标。229 仍是 501。本叶不把路径与风险改写成可算公式，也不把请求路径写成现算 `simulate.run`。

已签收架构把功能空态收成读表：无行则空，不用 501 充当接口返回，也不在返回里写死 mock。本叶不改 `指标与501.md` 和说明书。227、228、230 读缺项表行。231 从当次读到的行生成导出。行内文字和对照值不是新指标结果。

`M_POLICY_DS_11_POLICY_EVAL_015` 的需求来源是展示 02/229。本叶不改 `srs_refs`。布局建议条数的 `srs_refs` 虽含 02/227，本叶不据此把 227 改判成跨项索引。

本叶未会签。不写会签通过。不标 done。不改任务状态。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-PLAN-METRIC.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-PLAN-METRIC.md`

未改指标 seed、矩阵、说明书、`指标与501.md`、`PLAN-ARCH`、会签页、`task-registry.yaml`。未写代码。未新注册指标。未改 D4。

## 验收证据

- `metric-get`：`M_POLICY_DS_11_POLICY_EVAL_015` 为 GRAPH，中文名「实施路径与风险辅助」。`found.seed=true`、`found.matrix=true`、`found.srs_map=true`。D1=`aligned`，D2=`partial` 且 `d2_assessed=provisional`，D3=`partial`，D4=`mock`，`is_mock=true`。需求来源为展示 02/229。
- `metric-get` 核对后明确不挂：`M_POLICY_SIMULATE`（MODEL，D4=`mock`，`srs_refs` 为空）、`M_POLICY_LAYOUT_REC_COUNT`（STAT，D4=`mock`，`srs_refs` 含 02/227、02/241、05/171）、`M_POLICY_DEEP_171_1`（MODEL，D4=`mock`，需求来源 05/171）。
- 指标设计稿与本 handoff 已落在工作区。定义单，无业务 PR，无 pipeline。
- 未改任务状态。任务保持 `in_progress`。未会签。不标 done。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单不写算法实现。五叶的请求不算方案、不算参数、不生成路径。Java 不按弹性现算 |
| 调用链 | ✅ 沿已签收架构稿。浏览器只打 `/display/v1/policy/**`。227–229 经 `gkxlumen-display` 到 `gkxlumen-element` 读 `jobs`。230–231 读 `shells`。不进 `gkxlumen-topic-async-service`，不调用 `simulate.run`。本单不改链 |
| 图谱 | ✅ 229 的类型仍是 GRAPH，读面是缺项表行。本二级不读图，不写 nGQL |
| 可观测 | ✅ 不新设计观测点，沿既有展示链 |
| D9 | ✅ 只用已注册的一条 metric_id。八件套与 D1–D4 分开写。D4 保持 mock。227、228、230、231 不新造 id。229 保持 501，不写成可算公式 |
| D16 | ✅ 五叶只接受 `gkxlumenx_gapfill` 的 `gapfill_policy_eval_scheme`。行内文字不是新指标结果。231 不灌文件。本单不建表、不灌数 |
| D18 | ✅ 227–230 读已有缺项行，231 从当次读到的行生成导出。无行则空，不在返回语句里写死 mock |
| D12 | ✅ 不把展示调用链改去 demo 服务。注册表里的 demo 计算文件只作索引，本单不改、不调用 |
| D17 | ✅ 不改唐绍祖锁定的合规算法。本单不写算法实现 |
| D14 | ✅ 本单不写对象存储。231 不灌导出文件 |
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

- `sdd/l2/POL-L2-DS11-PLAN-METRIC.md`
- 本 handoff

未会签。不新造指标，D4 保持 mock。229 只挂实施路径与风险辅助，三档保持 501。227、228、230、231 不新造指标。不挂政策效果推演，不挂布局推荐。请求内不按 `simulate.run` 现算。
