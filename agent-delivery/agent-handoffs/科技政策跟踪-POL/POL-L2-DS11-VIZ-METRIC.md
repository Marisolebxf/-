ponytail: off

# POL-L2-DS11-VIZ-METRIC · 政策分析评价可视化呈现指标设计

- 任务：`POL-L2-DS11-VIZ-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-VIZ-ARCH.md`（2026-11-03 返工后第二轮，四角色同意，待 `human:淮政玮` 签收）
- 会签态：`draft`

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| lock_hours | 24 |
| 说明 | 任务已认领，状态为 in_progress。定义单。只写 219–222 的指标挂接。不写代码，不标 done，不标 ready_to_sign |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过已有 metric_id 的排除、501 与读表的区分、221 的跨项读图，以及 D4 保持原样。

## 范围与实现

政策分析评价 · 二级「政策分析报告可视化呈现」。只覆盖 SRS 序号 219–222，用户故事 `US-DS-POL-05`。挂接沿 `sdd/指标与501.md` 评价表 219–222 行。读面沿 `POL-L2-DS11-VIZ-ARCH`。本叶不改这些上游，不新造 `metric_id`，不改 D4。

| 序号 | 叶子 | 指标 |
|---|---|---|
| 219 | 多维指标趋势图 | 无专属 `metric_id`，无趋势模型。判定列仍是 501。页面读 `gapfill_policy_eval_trend`。无行则图空。不用 501 充当画面。不挂 `M_POLICY_TIMESERIES`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT` |
| 220 | 分区/群体对比分析图 | 无专属 `metric_id`，无分区模型。判定列仍是 501。页面读 `gapfill_policy_eval_partition`。无行则图空。不挂全景分布 |
| 221 | 多维结构关联图 | 无专属 `metric_id`。判定列仍是跨项索引。只消费第 7 项已有子图。不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`。子图没有则空 |
| 222 | 报告模板定制与批量导出 | 无专属 `metric_id`，无导出模型。判定列仍是 501。页面读 `gapfill_policy_eval_template`。无行则模板空。不用 501 充当画面 |

未见 metric MCP。注册中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1、D2、D3 未查，分册里没有把它们写成已查到。被排除号的 D4 只转述 `指标与501` 已有行，本叶不改。

## 挂接表

四叶都不挂已有 `metric_id`，也不新造号。

| 序号 | metric_id | 注册中文名 | algorithm_type | D4 |
|---|---|---|---|---|
| 219 | （无） | — | — | 无专属指标，不改 D4 |
| 220 | （无） | — | — | 无专属指标，不改 D4 |
| 221 | （无） | — | — | 无专属指标，不改 D4。跨项只消费子图 |
| 222 | （无） | — | — | 无专属指标，不改 D4 |

不新造指标。不改 D4。

## 偏离

无新 `metric_id`。

`指标与501` 将 219、220、222 的判定列记为 501、页面空态。那是调研判定。本叶不改那份文件。读面按架构稿：读缺项表，无行则空，不用 501 充当画面。221 的判定列仍是跨项索引，本叶不改档。

效果分写入 `ads.policy_effect`（`scope_type=region_effect`，行上 `metric_id` 为 `M_POLICY_EFFECT_SCORE`）。落地实效写入 `ads.policy_metric_timeseries`（`metric_id` 为 `M_POLICY_IMPLEMENTATION_EFFECT`）。两者都不挂本叶。本叶不调用 `effect.run`，不调用 `simulate.run`。

`PolicyAnalysisTypes` 的规范键没有趋势图、分区对比、模板导出。219、220、222 不进入该白名单。

未见 metric MCP，所以本叶没有中文名与叶子名的对照，也没有 `srs_refs` 对照。不把别的分册里曾经查到的中文名抄进来充当这次查询。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-VIZ-METRIC.md`
- 本 handoff

未改指标 seed、矩阵、说明书、`指标与501.md`、`POL-L2-DS11-VIZ-ARCH.md`、`POL-L2-DS11-READ-METRIC.md`、PLAN、WBS。未手改 `task-registry.yaml`。未写代码。未写 OpenAPI。未提交 git。

## 验收证据

- 开工时任务已是 `in_progress`，认领人 `agent:algorithm-agent`，监管 `human:淮政玮`。本叶不重新认领。
- 动态工具目录中无 metric 命名空间，无 `metric-get`。分册写明「未见 metric MCP」。未读 seed 与矩阵 YAML。未编造 D1–D3。
- 挂接结论：219、220、222 仍无专属模型、无专属 `metric_id`，页面读缺项表，不用 501 充当画面。221 跨项只消费第 7 项已有子图，不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`。
- 不挂 `M_POLICY_TIMESERIES`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT`、全景分布（`M_POLICY_NATIONAL_DIST`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST`）。
- 只读核对 `polan/eval/effect.py`：效果分插入 `ads.policy_effect`，落地实效插入 `ads.policy_metric_timeseries`。只读核对 `PolicyAnalysisTypes`：`CANONICAL` 九键不含本四叶。未调用 `effect.run`、`simulate.run`。未改这两处代码。
- 指标设计稿与本 handoff 已落盘。定义单，无业务 PR，无 pipeline。
- 会签态 `draft`。待会签。不代签。不标 done。不标 `ready_to_sign`。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单不改算法。效果分与落地实效只指认已有 `polan.eval.effect.run` 的写表位置。展示请求不调用 `effect.run`，不调用 `simulate.run`。Java 不打分 |
| 调用链 | ✅ 沿架构稿。浏览器只打 `/display/v1/policy/**`。219、220 不建任务、不进异步。221 不新开资源。222 走 `shells`。本单不改链，不写 OpenAPI |
| 图谱 | ✅ 221 只消费第 7 项已有子图。不挂两个图指标。不写 nGQL |
| 可观测 | ✅ 不新设计观测点，沿既有展示链 |
| D9 | ✅ 不新造 metric_id。八件套与 D1–D4 分开。未见 metric MCP 的字段留空不编。不改 D4。219、220、222 无专属指标 |
| D12 | ✅ 不把展示调用链改去 demo 页面或 `/v1/policy/**`。已有 `run()` 只作指认，本单不改、不调用 |
| D16 / D18 | ✅ 219、220、222 读 `gapfill_` 表，接口只查询。221 不建表。不用 501 充当画面。本单不灌数，不把 mock 写成已上线。不写 ODS、DWD、ADS |
| D17 | ✅ 不改锁定算法，不改 `effect.py`、`simulate.py` |
| D14 | ✅ 本单不写对象存储。222 不灌 PDF、Excel |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

与 `task-update-fields` 一致。`user_story` 为 `US-DS-POL-05`。

## 测试结果

定义单。未改业务仓，无单测，无 pipeline。核对方式是对照架构稿与 `指标与501` 219–222 行，并只读 `effect.py` 的两次插入和 `PolicyAnalysisTypes` 的 `CANONICAL` / `WHITELIST`。确认没有新 id、没有改 D4、没有假公式、没有调用 `effect.run` 或 `simulate.run`。

## 遗留风险

- 未见 metric MCP。注册中文名、口径、公式、注册源表、D1–D3 仍未在本叶核对。下游若要写八件套全文，须等 metric MCP 可用后再查，不能把本叶的空项当成「注册表没有这些字段」。
- 219、220、222 没有专属指标。缺项表没有行时，趋势图、分区图、模板区为空。灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01` 本叶不执行。
- 221 依赖第 7 项已有子图。`GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog。子图读不到则该块空。
- 效果分与落地实效的 `ext` 仍带 `QPOL-02`。本叶不闭合该决策，也不把这两条 ADS 写入当成可视化已上线。
- 架构稿待 `human:淮政玮` 签收。本叶不代签。

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

## 图

- 本叶不改 `POL-L2-DS11-VIZ-ARCH-SEQ`。架构稿记该图 `draft`（源文件无 frontmatter）。本叶不另画，不自填 approved

## 涉及文件

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-VIZ-METRIC.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-VIZ-METRIC.md`

## 修改内容

- `sdd/l2/POL-L2-DS11-VIZ-METRIC.md`
- 本 handoff
