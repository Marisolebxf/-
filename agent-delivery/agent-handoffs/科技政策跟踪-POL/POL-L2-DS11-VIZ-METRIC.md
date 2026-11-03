ponytail: off

# POL-L2-DS11-VIZ-METRIC · 政策分析评价政策分析报告可视化呈现指标设计

- 任务：`POL-L2-DS11-VIZ-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-VIZ-ARCH.md`（`task-get` 为 `done`；note：淮政玮 2026-11-03 签收。四角色复会签同意）
- 会签态：未会签

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| 说明 | 任务开工时已是 `in_progress`。本叶不再认领，不调用 task-registry 写工具，不改 `task-registry.yaml`，不改任务状态。定义单。只写 219–222 的指标挂接。不写代码，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过已有判定列、缺项表、第 7 项只消费、D4=`mock`、QPOL 与未会签。

## 范围与实现

政策分析评价 · 二级「政策分析报告可视化呈现」。只覆盖 SRS 序号 219–222，用户故事 `US-DS-POL-05`。指标身份沿说明书第 2 节与 `sdd/指标与501.md` 219–222 行已有 `metric_id` 和三档判定。读面沿已签收的 `POL-L2-DS11-VIZ-ARCH` 与 `sdd/l2/会签/POL-L2-DS11-VIZ-SIGNOFF-ARCH.md` 复会签。本叶不改这两份上游，不新造 `metric_id`，不改 D4。

架构稿抬头仍写「会签未完成。未签收」。本叶不改那份抬头。任务注册状态以 `task-get` 的 `done` 与签收 note 为准。

| 序号 | 叶子 | 指标 |
|---|---|---|
| 219 | 多维指标趋势图 | 没有专属 `metric_id`。判定保持 501。真路径保持「不借用 `M_POLICY_TIMESERIES`」。读 `gapfill_policy_eval_trend`。无行则图空 |
| 220 | 分区/群体对比分析图 | 没有专属 `metric_id`。判定保持 501。真路径保持「不挂全景分布类 STAT」。读 `gapfill_policy_eval_partition`。无行则图空 |
| 221 | 多维结构关联图 | `metric_id` 保持「未见」。判定保持「跨项索引」。只消费第 7 项已有子图。不新造图指标。不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` |
| 222 | 报告模板定制与批量导出 | 没有专属 `metric_id`。判定保持 501。调研交互壳为「未见」。无导出模型。读壳表模板选用行。无选用行则模板区空 |

本二级挂接 0 个已有 `metric_id`。查询日 2026-11-03。展示读数沿架构稿查已有表或已有子图，不重写公式，不改计算代码。

## 挂接表

| 序号 | metric_id | MCP 中文名 | algorithm_type | D4 | 三档 |
|---|---|---|---|---|---|
| 219 | （无） | — | — | 无注册指标，不改 D4 | 501 |
| 220 | （无） | — | — | 无注册指标，不改 D4 | 501 |
| 221 | （无） | — | — | 无注册指标，不改 D4 | 跨项索引 |
| 222 | （无） | — | — | 无注册指标，不改 D4 | 501 |

不新造指标。不改 D4。无行则空，不写假公式。

## 明确不挂

均经 2026-11-03 `metric-get`。D4 都是 `mock`，本叶不改。

- 全景时序 `M_POLICY_TIMESERIES`：政策时序指标，STAT，D4=`mock`。需求来源 02/205、02/206、05/100，页在全景。219 的真路径写明不借用。
- 效果分 `M_POLICY_EFFECT_SCORE`：政策效果评分（王惠三维口径 v2 复现），MODEL，D4=`mock`，QPOL-02。需求来源 02/232、02/233、05/168。不挂趋势图。
- `M_POLICY_IMPLEMENTATION_EFFECT`：落地实效性，MODEL，D4=`mock`，QPOL-02。需求来源 02/209、02/235、05/168。架构稿把它和效果分一起放在效果评估，不挂本叶。
- 全景分布：`M_POLICY_NATIONAL_DIST`（全国政策分布，D3=`full`）、`M_POLICY_TYPE_DIST`（政策类型分布，QPOL-01）、`M_POLICY_LEVEL_DIST`（政策级别分布，D3=`full`）、`M_POLICY_SZ_DIST`（深圳政策分布）。四条都是 STAT，D4=`mock`，需求来源都是专题 05/100，页在全景。不挂 220。
- `M_POLICY_GRAPH_107_1`：政策实体关系抽取，GRAPH，D4=`mock`。需求来源没有 02/221。不挂 221。
- `M_POLICY_RELATION_DEGREE`：政策关联度，GRAPH，D4=`mock`，`srs_refs` 为空。不挂 221。221 不新造图指标。
- `counts` 上的短板 `M_POLICY_SHORTBOARD_COUNT`：政策短板清单条数，STAT，D4=`mock`，需求来源 05/169，序号在 223。不进本叶。
- `counts` 上的机遇 `M_POLICY_OPPORTUNITY_COUNT`：政策机遇清单条数（王惠机遇计数 v2 全维复现），STAT，D4=`mock`，需求来源 05/170。没有 219–222 的序号。不进本叶。

`metric-query` 关键词「分布」还命中 `M_POLICY_BASE_100_1`、`M_POLICY_DEEP_167_1`。说明书第 2 节 219–222 没有这两条，本叶不挂。

序号 223 焦点、226 摘要、229 实施路径，以及 224、225、227–231，沿 `指标与501` 留在各自序号。`compare/jobs`、`report/jobs`、`benchmark-report` 不是 222。

## 偏离

无新 `metric_id`。219、220、222 的 `metric_id` 列保持「未见」，判定保持 501。221 的 `metric_id` 列保持「未见」，判定保持「跨项索引」。本叶不改这些字。

DoD「未注册模型保持 501」按指标分册落在 219、220、222。221 的分册判定本来就是「跨项索引」，本叶不把它改判成 501，也不新造图指标。

已签收架构把功能空态收成读表或只消费子图：无行则空，无子图则空。不用 501 充当接口返回，也不在返回里写死 mock。本叶不改 `指标与501.md` 和说明书。

本叶未会签。不写会签通过。不标 done。不改任务状态。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-VIZ-METRIC.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-VIZ-METRIC.md`

未改指标 seed、矩阵、说明书、`指标与501.md`、`VIZ-ARCH`、会签页、`task-registry.yaml`。未写代码。未新注册指标。未改 D4。

主工作区在提交时有其他会话的未提交文件，且落后 `origin/dev`。本单在临时 worktree（基线 `origin/dev`）里只加入上述两个文件。

## 验收证据

- 说明书第 2 节与 `指标与501` 219–222：`metric_id` 都是「未见」。219、220、222 判定为 501。221 判定为「跨项索引」。本叶未改这些字。
- `metric-get` 核对后明确不挂：`M_POLICY_TIMESERIES`（STAT，D4=`mock`）、`M_POLICY_EFFECT_SCORE`（MODEL，D4=`mock`）、`M_POLICY_IMPLEMENTATION_EFFECT`（MODEL，D4=`mock`）、`M_POLICY_NATIONAL_DIST`（STAT，D3=`full`，D4=`mock`）、`M_POLICY_TYPE_DIST`（STAT，D4=`mock`）、`M_POLICY_LEVEL_DIST`（STAT，D3=`full`，D4=`mock`）、`M_POLICY_SZ_DIST`（STAT，D4=`mock`）、`M_POLICY_GRAPH_107_1`（GRAPH，D4=`mock`）、`M_POLICY_RELATION_DEGREE`（GRAPH，D4=`mock`，`srs_refs` 为空）、`M_POLICY_SHORTBOARD_COUNT`（STAT，D4=`mock`）、`M_POLICY_OPPORTUNITY_COUNT`（STAT，D4=`mock`）。以上 `found.seed=true`、`found.matrix=true`。除关联度 `found.srs_map=false` 外，其余 `found.srs_map=true`。
- 本二级挂接的已有 `metric_id` 为 0。未写可算出数的公式。未改 D4。
- 指标设计稿与本 handoff 已落在 worktree。定义单，无业务 PR，无 pipeline。
- 未改任务状态。任务保持 `in_progress`。未会签。不标 done。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单不写算法实现。219、220 的同步读不调 Python，不算趋势、不算分区。222 不写导出模型。Java 不算这些数 |
| 调用链 | ✅ 沿已签收架构稿。浏览器只打 `/display/v1/policy/**`。219、220 经 `gkxlumen-element` 查缺项表，不建任务。222 读 `shells`。221 不设展示新资源。本单不改链 |
| 图谱 | ✅ 不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`。221 不新造图指标。只消费第 7 项已有子图，挂接可空。Java 不写 nGQL |
| 可观测 | ✅ 不新设计观测点，沿既有展示链 |
| D9 | ✅ 不新造 metric_id。219、220、222 保持 501。221 保持「跨项索引」。八件套与接入状态分开。不写假公式。不改 D4 |
| D16 | ✅ 219、220 只接受 `gkxlumenx_gapfill` 的两张 `gapfill_` 表。222 只读已有壳表的模板选用行，不灌模板，不灌文件。221 不建表。本单不建表、不灌数 |
| D18 | ✅ 无行则空，无子图则空，无选用行则模板区空。不在返回语句里写死曲线、矩阵、弦线或 PDF。不用 501 充当画面 |
| D12 | ✅ 不把展示调用链改去 demo 服务。注册表里的 demo 计算文件只作索引，本单不改、不调用 |
| D17 | ✅ 不改唐绍祖锁定的合规算法。本单不写算法实现 |
| D14 | ✅ 本单不写对象存储。222 不灌 PDF、Excel |
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

- `sdd/l2/POL-L2-DS11-VIZ-METRIC.md`
- 本 handoff

未会签。不新造指标，D4 保持 mock。219、220、222 没有专属已注册模型，判定保持 501。221 判定保持「跨项索引」，不新造图指标。不借全景时序、效果分、全景分布。不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`。`counts` 上的短板和机遇不进本叶。
