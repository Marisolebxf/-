ponytail: off

# POL-L2-DS12-EST-METRIC · 政策效果推演效果预估指标设计

- 任务：`POL-L2-DS12-EST-METRIC`
- 日期：2026-11-05
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 用户故事：`US-DS-POL-06`
- 上游：`sdd/l2/POL-L2-DS12-EST-ARCH.md`（2026-11-05 任务状态 `integration`，会签中，不标 done）
- 会签态：`draft`

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 开工时任务已是 `in_progress`，本叶不重复认领。定义单。只写 232–236 的指标挂接。不写代码，不改任务状态，不标 done，不标 `ready_to_sign` |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `off` |
| 说明 | 定义任务，不缩文档。未用 YAGNI 跳过已有 `metric_id`、空号、501 与读表的区分，以及 D4=`mock` |

ponytail: off

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS12-EST-ARCH-SEQ` |
| 图 diff | 本叶不改图，不加边 |
| 会签态 | 架构稿写明源文件无 frontmatter，记 `draft`。本叶不改成 `approved` |
| 说明 | 指标挂接沿当前架构稿的读表，不另画流程 |

## 范围与实现

政策效果推演 · 二级「效果预估」。只覆盖 SRS 序号 232–236，用户故事 `US-DS-POL-06`。挂接沿 `sdd/指标与501.md` §3 的 232–236 行，以及说明书第 2 节 DS-12 已有的 `metric_id` 与三档。读面沿当前 `POL-L2-DS12-EST-ARCH`。本叶不改这些上游，不新造 `metric_id`，不改 D4。

| 序号 | 叶子 | 指标 |
|---|---|---|
| 232 | 未出台政策仿真模拟 | 沿用已有 `M_POLICY_SIMULATE`。MODEL。D4 仍是 mock。判定仍是 501。未出台仿真行上写这个号。读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。参数档对不上则空 |
| 233 | 新出台政策效果预测 | 同一条 `M_POLICY_SIMULATE`。MODEL。D4 仍是 mock。判定仍是 501。没有独立指标。新出台预测行上写这个号。读同一张缺项表。不调 `parse/jobs`。无行则空 |
| 234 | 区域经济发展空间模拟 | 同一条 `M_POLICY_SIMULATE`。MODEL。D4 仍是 mock。判定仍是 501。没有独立指标。区域空间行上写这个号。读同一张缺项表。对不上则空 |
| 235 | 多维度效果评估 | 无专属 `metric_id`。判定仍是 501。不挂 `M_POLICY_SIMULATE`。不借用 `M_POLICY_DEEP_168_1`。多维评估行上的号留空。读 `gkxlumenx_gapfill.gapfill_policy_sim_result`。无行则空 |
| 236 | 利益攸关方参与评估 | 无专属 `metric_id`。判定仍是 501。不挂 `M_POLICY_SIMULATE`。参与意见行上的号留空。读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`。请求不插入。无行则空 |

未见 metric MCP，已回退读 `指标与501.md`。注册中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1、D2、D3 未查，分册里没有把它们写成已查到。D4=`mock` 只转述 `指标与501` 232–234 行和当前架构稿。235、236 没有可改的 D4。

## 挂接表

| 序号 | metric_id | 注册中文名 | algorithm_type | D4 |
|---|---|---|---|---|
| 232 | `M_POLICY_SIMULATE` | 未查（未见 metric MCP，回退文件无注册中文名） | MODEL | mock |
| 233 | `M_POLICY_SIMULATE` | 未查（同上，与 232 共用） | MODEL | mock |
| 234 | `M_POLICY_SIMULATE` | 未查（同上，与 232 共用） | MODEL | mock |
| 235 | （空） | — | — | 无专属指标，不改 D4 |
| 236 | （空） | — | — | 无专属指标，不改 D4 |

不新造指标。不改 D4。

`POLICY_SIMULATE` 的 `metric_ids` 同时列着 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015`。`simulate.run` 只把 `M_POLICY_SIMULATE` 写入 `ads.policy_simulate`，写的是省级力度情景，不写本二级的预估行，也不写 015。本叶不改这份模型注册表，也不调用 `run()`。232–234 不因此去读推演表。

## 偏离

无新 `metric_id`。与架构稿的差异：无。

`指标与501` 将 232–236 的判定列记为 501、页面空态。那是调研判定。本叶不改那份文件。读面按当前架构稿：读缺项表，无行则空，不用 501 充当功能。真推演未注册仍是 501。三档不改：这五叶仍不是可接统计读面，也不是跨项索引。

`M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1` 不挂 232–236。布局推荐键的 STAT 不改成推演页的可接统计读面。`M_POLICY_SIMULATE` 只挂 232–234 的预测行，不挂 235、236。本二级不读 `ads.policy_simulate`。

未见 metric MCP，所以本叶没有中文名与叶子名的注册对照，也没有 `srs_refs` 对照。不把别的分册里曾经查到的中文名抄进来充当这次查询。回退出处是 `sdd/指标与501.md` §3 与说明书第 2 节 DS-12。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-EST-METRIC.md`
- 本 handoff

未改指标 seed、矩阵、说明书、`指标与501.md`、`POL-L2-DS12-EST-ARCH.md`、调研分册、WBS、模型注册表、`simulate.py`、`task-registry.yaml` 文件本身。未调用 `task-update-status`、`task-update-fields`。未写代码。未写 OpenAPI。未写 DDL。未提交 git。

## 验收证据

- 开工时 `task-get`：`POL-L2-DS12-EST-METRIC` 已是 `in_progress`，`claimed_by=agent:algorithm-agent`，`supervised_by=human:淮政玮`。DoD 两条：只使用说明书第 2 节已有 `metric_id` 与三档；未注册模型保持 501，不写可算出数的假公式，不改 D4，不新注册指标。上游 `POL-L2-DS12-EST-ARCH` 为 `integration`，note 为架构稿已落盘。本叶不改这两条状态。
- 动态工具目录中无 metric 命名空间，无 `metric-get` / `metric-query`。分册写明回退读 `sdd/指标与501.md`。未读 seed 与矩阵 YAML。未编造 D1–D3。
- 挂接只使用说明书第 2 节 DS-12 与 `指标与501` 232–236 已有 id：232、233、234 为 `M_POLICY_SIMULATE`（MODEL，D4=`mock`，判定 501）。235、236 仍无专属 id，行上留空。
- 读表沿当前架构稿，只作引用：232–234 读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`；235 读 `gkxlumenx_gapfill.gapfill_policy_sim_result`；236 读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`。无行则空。列定义归 DATA 分册，本叶不写 DDL。
- 核对 `vendor/entan-py/polan/text/simulate.py`：`run()` 写入 `ads.policy_simulate`，`metric_id` 固定 `M_POLICY_SIMULATE`，写的是省级力度情景，不产出未出台四类参数、新出台预测、区域空间、维度得分或意见。本叶不调用 `run()`，不把情景弹性收成公式，232–234 不读 `ads.policy_simulate`。
- 核对 `cfg_model_registry.yaml` 的 `POLICY_SIMULATE`：`metric_ids` 含 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015`。本叶不改该文件。015 不写进预估行。
- 未写可算出数的公式。未把布局推荐键写成推演指标。未把 501 改写成可接统计。
- 指标设计稿与本 handoff 已落盘。定义单，无业务 PR，无 pipeline。
- 会签态 `draft`。不代签。不标 done。不标 `ready_to_sign`。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单不改算法。推演函数只作指认：`polan.text.simulate.run` 不产出本二级预估行，展示请求不调用它 |
| 调用链 | ✅ 沿当前架构稿。浏览器只打 `/display/v1/policy/**`。本单不改链，不写 OpenAPI |
| 图谱 | ✅ 本二级不读图，不写 nGQL。240 的 `M_POLICY_RELATION_DEGREE` 不在本叶 |
| 可观测 | ✅ 不新设计观测点，沿既有展示链 |
| D9 | ✅ 只用已有 metric_id。八件套与 D1–D4 分开。未见 metric MCP 的字段留空不编。232–234 的 D4 保持 mock。235、236 不新造 id |
| D12 | ✅ 不把展示调用链改去 demo 页面、算法中台效果推演签或 `/v1/policy/simulate`。已有 `run()` 只作指认，本单不改、不调用 |
| D16 / D18 | ✅ 232–234 读 `gapfill_policy_sim_forecast`，235 读 `gapfill_policy_sim_result`，236 读 `gapfill_policy_sim_stakeholder`。232–234 行上用已有号，235、236 行号留空。不用 501 充当功能。本单不灌数，不把 mock 写成已上线。接口不直接返回写死的 mock |
| D17 | ✅ 不改锁定算法，不改 `simulate.py`，不改模型注册表 |
| D14 | ✅ 本单不写对象存储 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

`actual_tokens` 取本任务 `estimated_tokens`。未见 Console 精确拆分。`actual_cost` 沿同模块定义单 `POL-L2-DS11-PLAN-METRIC` 的同档。`cost_warn` 为 green。本叶不调用 `task-update-fields`，这四项只写在本 handoff。`user_story` 为 `US-DS-POL-06`。证据即本 handoff。

## 测试结果

定义单。未改业务仓，无单测，无 pipeline。核对方式是对照当前架构稿、`指标与501` §3 的 232–236 行、说明书第 2 节 DS-12，以及 `simulate.py` 与 `POLICY_SIMULATE` 注册项，确认没有新 id、没有改 D4、没有假公式、235 与 236 不挂推演号、布局推荐不挂本二级、501 没有改写成可接统计。

## 遗留风险

- 未见 metric MCP。注册中文名、口径、公式、注册源表、D1–D3 仍未在本叶核对。下游若要写八件套全文，须等 metric MCP 可用后再查，不能把本叶的空项当成「注册表没有这些字段」。
- `GDF-POLICY-MOCK-GATE-L01` 仍按架构稿与 `指标与501` 视为未解开。缺项行在对齐前仍是 mock。`M_POLICY_SIMULATE` 的 D4 仍是 mock。
- 235、236 没有专属指标。缺项表没有行时，多维评估和参与意见为空。页面新提交的意见不落库。
- 模型注册表把 `M_POLICY_DS_11_POLICY_EVAL_015` 列在 `POLICY_SIMULATE` 下，函数只写 `M_POLICY_SIMULATE`，且维度是省级力度情景。本叶不改注册表。下游不要据此让 232–234 去读 `ads.policy_simulate`，也不要在本二级调用 `simulate.run`。
- 真推演仍未进入异步白名单。缺项读面与 501 空态并存。本叶不把 501 改成可接统计。
- 架构稿仍是 `integration` / `draft`。本叶不代签。

## CI/CD

- 分支：未提交
- commit：无
- pipeline URL / ID：无。定义单，无业务 CI
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：无

## 可观测性

- 本叶不新设计观测点
- trace 沿既有展示链，无新抽样

## 涉及文件

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-EST-METRIC.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS12-EST-METRIC.md`

## 修改内容

- `sdd/l2/POL-L2-DS12-EST-METRIC.md`
- 本 handoff
