ponytail: off

# POL-L2-DS11-PLAN-METRIC · 政策分析评价推荐方案报告交互展示指标设计

- 任务：`POL-L2-DS11-PLAN-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md`（2026-11-03 已签收）
- 会签态：`draft`

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 开工时任务已是 `in_progress`，本叶不重复认领。定义单。只写 227–231 的指标挂接。不写代码，不标 done，不标 `ready_to_sign` |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过已有 `metric_id`、空号、501 与读表的区分，以及 D4=`mock`。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS11-PLAN-ARCH-SEQ` |
| 图 diff | 本叶不改图，不加边 |
| 会签态 | 架构稿写明源文件无 frontmatter，记 `draft`。本叶不改成 `approved` |
| 说明 | 指标挂接沿已签收架构的读表，不另画流程 |

## 范围与实现

政策分析评价 · 二级「推荐方案报告交互展示」。只覆盖 SRS 序号 227–231，用户故事 `US-DS-POL-05`。挂接沿 `sdd/指标与501.md` 评价表 227–231 行，以及说明书第 2 节 DS-11 已有的 `metric_id` 与三档。读面沿已签收的 `POL-L2-DS11-PLAN-ARCH`。本叶不改这些上游，不新造 `metric_id`，不改 D4。

| 序号 | 叶子 | 指标 |
|---|---|---|
| 227 | 多方案对比展示 | 无专属 `metric_id`。判定仍是 501。不挂 `M_POLICY_LAYOUT_REC_COUNT`。方案对照行上的号留空。读 `gapfill_policy_eval_scheme` 的方案对照行。少于两行则对比空 |
| 228 | 方案参数自定义模拟 | 无专属 `metric_id`。判定仍是 501。不挂 `M_POLICY_SIMULATE`。不读 `ads.policy_simulate`。不调用 `simulate.run`。参数模拟行上的号留空。按方案和参数档读缺项表。对不上则空 |
| 229 | 实施路径与风险辅助 | 沿用已有 `M_POLICY_DS_11_POLICY_EVAL_015`。GRAPH。D4 仍是 mock。判定仍是 501。路径与风险行上写这个号。读同一张缺项表。不读图。不被序号 241 顶替 |
| 230 | 互动意见收集与专家参与 | 无专属 `metric_id`。判定仍是 501（交互壳，不升第四档）。意见行上的号留空。只读已灌行。请求不插入 |
| 231 | 方案报告导出与归档 | 无专属 `metric_id`。判定仍是 501（交互壳，不升第四档）。不单独占种类。从方案对照行和意见行生成。不灌文件 |

未见 metric MCP。注册中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1、D2、D3 未查，分册里没有把它们写成已查到。D4=`mock` 只转述 `指标与501` 229 行和已签收架构稿。227、228、230、231 没有可改的 D4。

## 挂接表

| 序号 | metric_id | 注册中文名 | algorithm_type | D4 |
|---|---|---|---|---|
| 227 | （空） | — | — | 无专属指标，不改 D4 |
| 228 | （空） | — | — | 无专属指标，不改 D4 |
| 229 | `M_POLICY_DS_11_POLICY_EVAL_015` | 未查（未见 metric MCP） | GRAPH | mock |
| 230 | （空） | — | — | 无专属指标，不改 D4 |
| 231 | （空） | — | — | 无专属指标，不改 D4 |

不新造指标。不改 D4。

`POLICY_SIMULATE` 的 `metric_ids` 同时列着 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015`。`simulate.run` 只把 `M_POLICY_SIMULATE` 写入 `ads.policy_simulate`，不写路径。本叶不改这份模型注册表，也不调用 `run()`。229 不因此去读推演表。

## 偏离

无新 `metric_id`。

`指标与501` 将 227–231 的判定列记为 501、页面空态。那是调研判定。本叶不改那份文件。读面按已签收架构：读缺项表，无行则空，不用 501 充当功能。三档不改：这五叶仍不是可接统计读面，也不是跨项索引。230、231 仍是并入 501 的交互壳，不升第四档。

`M_POLICY_LAYOUT_REC_COUNT` 不挂 227。`M_POLICY_SIMULATE` 不挂 228，本二级不读 `ads.policy_simulate`。序号 241 不顶替 229。`M_POLICY_DS_11_POLICY_EVAL_015` 也不顶替 241。

未见 metric MCP，所以本叶没有中文名与叶子名的对照，也没有 `srs_refs` 对照。不把别的分册里曾经查到的中文名抄进来充当这次查询。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-PLAN-METRIC.md`
- 本 handoff

未改指标 seed、矩阵、说明书、`指标与501.md`、`POL-L2-DS11-PLAN-ARCH.md`、`POL-L2-DS11-READ-METRIC.md`、模型注册表、`simulate.py`、`task-registry.yaml` 文件本身。证据与状态只经 MCP。未写代码。未写 OpenAPI。未提交 git。

## 验收证据

- 开工时 `task-get`：`POL-L2-DS11-PLAN-METRIC` 已是 `in_progress`，`claimed_by=agent:algorithm-agent`，`supervised_by=human:淮政玮`。上游 `POL-L2-DS11-PLAN-ARCH` 已是 `done`，note 为 `human:淮政玮` 签收。
- 动态工具目录中无 metric 命名空间，无 `metric-get`。分册写明「未见 metric MCP」。未读 seed 与矩阵 YAML。未编造 D1–D3。
- 挂接只使用说明书第 2 节 DS-11 与 `指标与501` 227–231 已有 id：229 为 `M_POLICY_DS_11_POLICY_EVAL_015`（GRAPH，D4=`mock`，判定 501）。227、228、230、231 仍无专属 id，行上留空。
- 读表沿已签收架构：五叶读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。227 方案对照，228 参数模拟，229 路径与风险，230 意见，231 从方案对照行和意见行生成。无行则空。
- 核对 `vendor/entan-py/polan/text/simulate.py`：`run()` 只写省级力度情景，`metric_id` 固定 `M_POLICY_SIMULATE`，不产出路径，不写 `M_POLICY_DS_11_POLICY_EVAL_015`。本叶不调用 `run()`，228 与 229 不读 `ads.policy_simulate`。
- 核对 `cfg_model_registry.yaml` 的 `POLICY_SIMULATE`：`metric_ids` 含上述两个号。本叶不改该文件。
- 未写可算出数的公式。未把情景弹性收成 228 或 229 的公式。未把序号 241 写成 229 的顶替。
- 指标设计稿与本 handoff 已落盘。定义单，无业务 PR，无 pipeline。
- 会签态 `draft`。不代签。不标 done。不标 `ready_to_sign`。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单不改算法。推演只作指认：`polan.text.simulate.run` 不产出 229，展示请求不调用它 |
| 调用链 | ✅ 沿已签收架构稿。浏览器只打 `/display/v1/policy/**`。本单不改链，不写 OpenAPI |
| 图谱 | ✅ 229 的类型仍是 GRAPH，读面是缺项表，不读第 7 项子图，不写 nGQL |
| 可观测 | ✅ 不新设计观测点，沿既有展示链 |
| D9 | ✅ 只用已有 metric_id。八件套与 D1–D4 分开。未见 metric MCP 的字段留空不编。229 的 D4 保持 mock。227、228、230、231 不新造 id |
| D12 | ✅ 不把展示调用链改去 demo 页面、算法中台效果推演签或 `/internal/analysis/policy/simulate`。已有 `run()` 只作指认，本单不改、不调用 |
| D16 / D18 | ✅ 五叶读 `gapfill_policy_eval_scheme`。229 行上用已有号，其余行号留空。不用 501 充当功能。本单不灌数，不把 mock 写成已上线。接口不直接返回写死的 mock |
| D17 | ✅ 不改锁定算法，不改 `simulate.py`，不改模型注册表 |
| D14 | ✅ 本单不写对象存储。231 不灌导出文件 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

与 `task-update-fields` 一致。`user_story` 为 `US-DS-POL-05`。`evidence` 为本 handoff。

## 测试结果

定义单。未改业务仓，无单测，无 pipeline。核对方式是对照已签收架构稿、`指标与501` 227–231 行、说明书第 2 节 DS-11，以及 `simulate.py` 与 `POLICY_SIMULATE` 注册项，确认没有新 id、没有改 D4、没有假公式、228 不挂推演、227 不挂布局建议条数、241 不顶替 229。

## 遗留风险

- 未见 metric MCP。注册中文名、口径、公式、注册源表、D1–D3 仍未在本叶核对。下游若要写八件套全文，须等 metric MCP 可用后再查，不能把本叶的空项当成「注册表没有这些字段」。
- `GDF-POLICY-MOCK-GATE-L01` 仍按架构稿视为未解开。缺项行在对齐前仍是 mock。229 的 D4 仍是 mock。
- 227、228、230、231 没有专属指标。缺项表没有行时，对比、参数预览、意见和导出为空。
- 模型注册表把 `M_POLICY_DS_11_POLICY_EVAL_015` 列在 `POLICY_SIMULATE` 下，函数只写 `M_POLICY_SIMULATE`。本叶不改注册表。下游不要据此让 229 去读 `ads.policy_simulate`，也不要在本二级调用 `simulate.run`。
- 序号 241 仍无路径预测模型。它不顶替 229，015 也不顶替 241。

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

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-PLAN-METRIC.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-PLAN-METRIC.md`

## 修改内容

- `sdd/l2/POL-L2-DS11-PLAN-METRIC.md`
- 本 handoff
