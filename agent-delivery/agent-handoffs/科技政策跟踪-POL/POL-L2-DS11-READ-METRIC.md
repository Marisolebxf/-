ponytail: off

# POL-L2-DS11-READ-METRIC · 政策分析评价结果解读报告多维展示指标设计

- 任务：`POL-L2-DS11-READ-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-READ-ARCH.md`（2026-11-03 已签收，签收人 human:淮政玮）
- 会签态：未会签

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| 说明 | 任务开工时已是 `in_progress`。本叶不再认领，不调用 task-registry 写工具，不改 `task-registry.yaml`，不改任务状态。定义单。只写 223–226 的指标挂接。不写代码，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过已有 `metric_id`、缺项表行、D4=`mock`、QPOL-02、焦点指数的 501 三档和未会签。

## 范围与实现

政策分析评价 · 二级「结果解读报告多维展示」。只覆盖 SRS 序号 223–226，用户故事 `US-DS-POL-05`。指标身份沿说明书第 2 节与 `sdd/指标与501.md` 223–226 行已有 `metric_id` 和三档判定。读面沿已签收的 `POL-L2-DS11-READ-ARCH` 与 `sdd/l2/会签/POL-L2-DS11-READ-SIGNOFF-ARCH.md`。本叶不改这两份上游，不新造 `metric_id`，不改 D4。

| 序号 | 叶子 | 指标 |
|---|---|---|
| 223 短板 | 热点问题分析看板 | 只挂 `M_POLICY_SHORTBOARD_COUNT`。STAT。已有统计读面。D4 仍是 mock。同步 `counts` 只读 `shortboard_cnt`。GET 不调用 `gap.run`。无行则空，不造 0 |
| 223 焦点 | 热点问题分析看板 | 只挂 `M_POLICY_FOCUS_INDEX`。MODEL。三档保持指标分册的 501。不改成可算公式。D4 仍是 mock。读已有 `ads.policy_focus` 的行。无行则空 |
| 224 | 分主题分指标互动解读 | 没有专属 `metric_id`，不新造，不写公式。判定保持 501。页面读 `gapfill_policy_eval_shell` 的解读条目。行内文字不是指标结果 |
| 225 | 多媒体辅助解读 | 没有专属 `metric_id`，不新造，不写公式。判定保持 501。读同一张缺项表的标题和一句说明。不灌视频 |
| 226 | 智能摘要与结论推送 | 只挂 `M_POLICY_DS_11_POLICY_EVAL_012`。MODEL。判定保持 501。D4 仍是 mock。请求只读已有 `summary` 列，不写成现算 `parse.run`。无行则空 |

去重后本二级只用上述 3 个已有 `metric_id`。八件套来自 2026-11-03 的 `metric-get`。展示读数指向已有表上的列，不重写公式，不改计算代码。

## 挂接表

| 序号 | metric_id | MCP 中文名 | algorithm_type | D4 | 三档 |
|---|---|---|---|---|---|
| 223 短板 | `M_POLICY_SHORTBOARD_COUNT` | 政策短板清单条数 | STAT | mock | 可接统计读面 |
| 223 焦点 | `M_POLICY_FOCUS_INDEX` | 政策焦点指数 | MODEL | mock | 501 |
| 224 | （无） | — | — | 无注册指标，不改 D4 | 501 |
| 225 | （无） | — | — | 无注册指标，不改 D4 | 501 |
| 226 | `M_POLICY_DS_11_POLICY_EVAL_012` | 智能摘要与结论推送 | MODEL | mock | 501 |

不新造指标。不改 D4。无行则空，不写假公式。

## 明确不挂

- 机遇条数 `M_POLICY_OPPORTUNITY_COUNT`：没有 223–226 的序号。`metric-get` 为 STAT、D4=`mock`，需求来源只有专题 05/170。留在页 KPI 的 `counts` 读面，本叶不改。
- `M_POLICY_RELATION_DEGREE`：GRAPH，D4=`mock`，`srs_refs` 为空。留在焦点行的 `relation_degree`，不改挂到 223，不为此读图。
- 序号 222 的报告模板：未见专属 `metric_id`，不新造。模板选用不灌入 shell。
- 序号 227–231：不进本四叶。`M_POLICY_DS_11_POLICY_EVAL_015` 的需求来源是 02/229，不改挂到 223–226。
- `M_POLICY_EFFECT_SCORE`、`M_POLICY_TEXT_PARSE`、`M_POLICY_DEEP_169_1` 都不挂进这四叶的展示身份。226 的行上 id 仍是 `M_POLICY_TEXT_PARSE`，本叶不改。短板同步链不计算源模型。

## 偏离

无新 `metric_id`。中文名与叶子名不一致时以 MCP 为准：短板条数的注册中文名是「政策短板清单条数」；焦点指数的注册中文名是「政策焦点指数」。

DoD「未注册模型保持 501」按指标分册的三档保持。223 短板仍是可接统计读面。223 焦点、224、225、226 仍是 501。本叶不把焦点指数改写成可算公式，不把 226 的请求路径写成现算 `parse.run`。

已签收架构把功能空态收成读表：无行则空，不用 501 充当接口返回，也不在返回里写死 mock。本叶不改 `指标与501.md` 和说明书。224、225 读缺项表行，行内文字不是指标结果。

`M_POLICY_SHORTBOARD_COUNT` 的需求来源是专题 05/169，不是 02/223。`M_POLICY_FOCUS_INDEX` 的需求来源是专题 05/166。`M_POLICY_DS_11_POLICY_EVAL_012` 的需求来源是展示 02/226。本叶不改 `srs_refs`。

本叶未会签。不写会签通过。不标 done。不改任务状态。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-READ-METRIC.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-READ-METRIC.md`

未改指标 seed、矩阵、说明书、`指标与501.md`、`READ-ARCH`、会签页、`task-registry.yaml`。未写代码。未新注册指标。未改 D4。

## 验收证据

- `metric-get`：`M_POLICY_SHORTBOARD_COUNT` 为 STAT，中文名「政策短板清单条数」。`M_POLICY_FOCUS_INDEX` 为 MODEL，中文名「政策焦点指数」。`M_POLICY_DS_11_POLICY_EVAL_012` 为 MODEL，中文名「智能摘要与结论推送」。三条均 `found.seed=true`、`found.matrix=true`、`found.srs_map=true`。D1=`aligned`，D2=`partial` 且 `d2_assessed=provisional`，D3=`partial`，D4=`mock`，`is_mock=true`。
- `metric-get` 核对后明确不挂：`M_POLICY_OPPORTUNITY_COUNT`（STAT，D4=`mock`，需求来源 05/170）、`M_POLICY_RELATION_DEGREE`（GRAPH，D4=`mock`，`srs_refs` 为空）、`M_POLICY_DEEP_169_1`（MODEL，D4=`mock`）、`M_POLICY_TEXT_PARSE`（MODEL，D4=`mock`，`srs_refs` 为空）、`M_POLICY_EFFECT_SCORE`（MODEL，D4=`mock`，需求来源 02/232、02/233、05/168）、`M_POLICY_DS_11_POLICY_EVAL_015`（GRAPH，D4=`mock`，需求来源 02/229）。
- 指标设计稿与本 handoff 已落在工作区。定义单，无业务 PR，无 pipeline。
- 未改任务状态。任务保持 `in_progress`。未会签。不标 done。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单不写算法实现。短板 GET 不算条数。焦点不在本叶展开公式。226 的请求只查询摘要列。Java 不算指数 |
| 调用链 | ✅ 沿已签收架构稿。浏览器只打 `/display/v1/policy/**`。短板与 224、225 经 `gkxlumen-element` 查表。焦点与摘要经 `gkxlumen-topic-async-service` 再进 `/internal/policy/jobs/execute`。226 的请求不调用 `parse.run`。本单不改链 |
| 图谱 | ✅ 不挂 `M_POLICY_RELATION_DEGREE`。本二级不读图，不写 nGQL |
| 可观测 | ✅ 不新设计观测点，沿既有展示链 |
| D9 | ✅ 只用已注册的三条 metric_id。八件套与 D1–D4 分开写。D4 保持 mock。224、225 不新造 id。焦点保持 501，不写成可算公式 |
| D16 | ✅ 224、225 只接受 `gkxlumenx_gapfill` 的 `gapfill_policy_eval_shell`。行内文字不是指标结果。不灌视频，不灌模板。本单不建表、不灌数 |
| D18 | ✅ 223 短板读已有 `ads.policy_effect`，223 焦点读已有 `ads.policy_focus`，226 读已有 `ads.policy_text_parse.summary`。224、225 读缺项表。无行则空，不在返回语句里写死 mock |
| D12 | ✅ 不把展示调用链改去 demo 服务。注册表里的 demo 计算文件只作索引，本单不改、不调用 |
| D17 | ✅ 不改唐绍祖锁定的合规算法。本单不写算法实现 |
| D14 | ✅ 本单不写对象存储。225 不灌视频文件 |
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

- `sdd/l2/POL-L2-DS11-READ-METRIC.md`
- 本 handoff

未会签。不新造指标，D4 保持 mock。223 短板只挂政策短板清单条数，保持统计读面。223 焦点只挂政策焦点指数，三档保持 501，不写成可算公式。224、225 不新造指标。226 只挂智能摘要与结论推送，请求只读已有摘要列。机遇条数、关联度、222 模板、227–231 不挂。
