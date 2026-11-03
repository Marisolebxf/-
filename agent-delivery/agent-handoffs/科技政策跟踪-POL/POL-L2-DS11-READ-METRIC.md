ponytail: off

# POL-L2-DS11-READ-METRIC · 政策分析评价结果解读多维展示指标设计

- 任务：`POL-L2-DS11-READ-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-READ-ARCH.md`（2026-11-03 已签收）
- 会签态：`draft`

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| lock_hours | 24 |
| 说明 | 认领时任务为 ready，认领后已改为 in_progress。定义单。只写 223–226 的指标挂接。不写代码，不标 done，不标 ready_to_sign |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过已有 metric_id、空态、501 与读表的区分，以及 D4=mock。

## 范围与实现

政策分析评价 · 二级「结果解读报告多维展示」。只覆盖 SRS 序号 223–226，用户故事 `US-DS-POL-05`。挂接沿 `sdd/指标与501.md` 评价表 223–226 行，以及说明书第 2 节 DS-11 已有的 `metric_id` 与三档。读面沿已签收的 `POL-L2-DS11-READ-ARCH`。本叶不改这些上游，不新造 `metric_id`，不改 D4。

| 序号 | 叶子 | 指标 |
|---|---|---|
| 223 短板 | 热点问题分析看板 · 短板条数 | 可接统计读面。`M_POLICY_SHORTBOARD_COUNT`。STAT。D4 仍是 mock。读 `ads.policy_effect` 的 `region_gap.shortboard_cnt`。源模型 `M_POLICY_DEEP_169_1` 仍是 MODEL，不在同步链上计算。QPOL-02 未闭合。不改 `gap.run`。无行则空，不造 0 |
| 223 焦点 | 热点问题分析看板 · 焦点指数 | `M_POLICY_FOCUS_INDEX`。MODEL。D4 仍是 mock。读 `ads.policy_focus` 且 `policy_id` 非空的 `focus_score`。名称和一句说明用该行 `ext.title`、`ext.explanation`。不改 `focus.run` 权重。无行则空 |
| 224 | 分主题分指标互动解读 | 无专属 `metric_id`。不新注册。指不到则留空 |
| 225 | 多媒体辅助解读 | 无专属 `metric_id`。不新注册。指不到则留空 |
| 226 | 智能摘要与结论推送 | 展示读面 `M_POLICY_DS_11_POLICY_EVAL_012`。MODEL。D4 仍是 mock。读 `ads.policy_text_parse.summary`。行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。写入是规则截取，不把截取写成 NLP 已经做到。不另写摘要模型。无行则空 |

未见 metric MCP。注册中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1、D2、D3 未查，分册里没有把它们写成已查到。D4=mock 只转述 `指标与501` 已有行和已签收架构稿。

## 挂接表

| 序号 | metric_id | 注册中文名 | algorithm_type | D4 |
|---|---|---|---|---|
| 223 短板 | `M_POLICY_SHORTBOARD_COUNT` | 未查（未见 metric MCP） | STAT | mock |
| 223 焦点 | `M_POLICY_FOCUS_INDEX` | 未查。展示名称用行上 `ext.title` | MODEL | mock |
| 224 | （无） | — | — | 无专属指标，不改 D4 |
| 225 | （无） | — | — | 无专属指标，不改 D4 |
| 226 展示读面 | `M_POLICY_DS_11_POLICY_EVAL_012` | 未查（未见 metric MCP） | MODEL | mock |

226 行上不改的号：`M_POLICY_TEXT_PARSE`。它不是第二条挂接，也不是另一套摘要。

不新造指标。不改 D4。

## 偏离

无新 `metric_id`。

`指标与501` 将 223 焦点、224、225、226 的判定列记为 501、页面空态。那是调研判定。本叶不改那份文件。读面按已签收架构：读表，无行则空，不用 501 充当功能。223 短板的判定列仍是可接统计读面，本叶不改档。

`M_POLICY_RELATION_DEGREE` 留在焦点行的 `relation_degree`，不改挂到 223。`M_POLICY_OPPORTUNITY_COUNT` 不挂本二级。`M_POLICY_DEEP_169_1` 仍是短板的源模型，不在同步链上计算。

未见 metric MCP，所以本叶没有中文名与叶子名的对照，也没有 `srs_refs` 对照。不把别的分册里曾经查到的中文名抄进来充当这次查询。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-READ-METRIC.md`
- 本 handoff

未改指标 seed、矩阵、说明书、`指标与501.md`、`POL-L2-DS11-READ-ARCH.md`、VIZ、PLAN、WBS、`task-registry.yaml`。未写代码。未写 OpenAPI。未提交 git。

## 验收证据

- 开工前经 `task-claim` 成功，状态曾为 `claimed`，随即改为 `in_progress`。认领参数：`claimed_by=agent:algorithm-agent`，`supervised_by=human:淮政玮`，`lock_hours=24`。
- 动态工具目录中无 metric 命名空间，无 `metric-get`。分册写明「未见 metric MCP」。未读 seed 与矩阵 YAML。未编造 D1–D3。
- 挂接只使用说明书第 2 节 DS-11 与 `指标与501` 223–226 已有 id：短板 `M_POLICY_SHORTBOARD_COUNT`（可接统计读面），焦点 `M_POLICY_FOCUS_INDEX`（判定列 501），226 `M_POLICY_DS_11_POLICY_EVAL_012`（判定列 501）。224、225 仍无专属 id。
- 读表与空态沿已签收架构：短板读 `ads.policy_effect` 的 `region_gap.shortboard_cnt`；焦点读 `ads.policy_focus` 的 `focus_score` 与 `ext.title`、`ext.explanation`；226 读 `ads.policy_text_parse.summary`。无行则空。
- 未写可算出数的公式。未改 `gap.run`、`focus.run`、`parse.run`。未把规则截取写成 NLP 已经做到。
- 指标设计稿与本 handoff 已落盘。定义单，无业务 PR，无 pipeline。
- 会签态 `draft`。不代签。不标 done。不标 `ready_to_sign`。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单不改算法。短板、焦点、摘要只指向已有 `polan.eval.gap.run`、`polan.eval.focus.run`、`polan.text.parse.run`。展示请求不调用 `gap.run` 与 `parse.run` |
| 调用链 | ✅ 沿已签收架构稿。浏览器只打 `/display/v1/policy/**`。本单不改链，不写 OpenAPI |
| 图谱 | ✅ `M_POLICY_RELATION_DEGREE` 不改挂到 223，不为此读图，不写 nGQL |
| 可观测 | ✅ 不新设计观测点，沿既有展示链 |
| D9 | ✅ 只用已有 metric_id。八件套与 D1–D4 分开。未见 metric MCP 的字段留空不编。D4 保持 mock。224、225 不新造 id |
| D12 | ✅ 不把展示调用链改去 demo 页面或 `/v1/policy/**`。已有 `run()` 只作指认，本单不改、不调用 |
| D16 / D18 | ✅ 223、226 读已有 ADS。224、225 的缺项表 `metric_id` 留空。不用 501 充当功能。本单不灌数，不把 mock 写成已上线 |
| D17 | ✅ 不改锁定算法，不改 `gap.run`、`focus.run`、`parse.run` |
| D14 | ✅ 本单不写对象存储。225 不灌视频文件 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

与 `task-update-fields` 一致。`user_story` 为 `US-DS-POL-05`。

## 测试结果

定义单。未改业务仓，无单测，无 pipeline。核对方式是对照已签收架构稿与 `指标与501` 223–226 行，确认没有新 id、没有改 D4、没有假公式。

## 遗留风险

- 未见 metric MCP。注册中文名、口径、公式、注册源表、D1–D3 仍未在本叶核对。下游若要写八件套全文，须等 metric MCP 可用后再查，不能把本叶的空项当成「注册表没有这些字段」。
- `QPOL-02` 未闭合。短板与焦点的正式值在对齐前仍是 mock。`GDF-POLICY-MOCK-GATE-L01` 仍按架构稿视为未解开。
- 224、225 没有专属指标。缺项表没有行时，解读块和多媒体块为空。
- 226 的写入仍是规则截取。需规里的 NLP 摘要尚未另有模型。本叶不把截取当成 NLP 已完成。

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

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-READ-METRIC.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-READ-METRIC.md`

## 修改内容

- `sdd/l2/POL-L2-DS11-READ-METRIC.md`
- 本 handoff
