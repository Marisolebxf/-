ponytail: off

# POL-L2-DS12-SIM-METRIC · 政策效果推演科技政策推演指标设计

- 任务：`POL-L2-DS12-SIM-METRIC`
- 日期：2026-11-05
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 用户故事：`US-DS-POL-06`
- 上游：`sdd/l2/POL-L2-DS12-SIM-ARCH.md`（含 2026-11-05 第 7、9 节）
- 会签态：`draft`

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | task-get 未返回。开工时任务已是 `in_progress`，本叶不重复认领 |
| 说明 | 定义单。只写 237–242 的指标挂接。不写代码，不改任务状态，不标 done，不标 `ready_to_sign` |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过已有 `metric_id`、空号、501 与读表的区分、240 的跨项索引，以及 D4=`mock`。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS12-SIM-ARCH-SEQ` |
| 图 diff | 本叶不改图，不加边 |
| 会签态 | 架构稿写明源文件无 frontmatter，记 `draft`。本叶不改成 `approved` |
| 说明 | 指标挂接沿架构稿的读表与跨项消费，不另画流程 |

## 范围与实现

政策效果推演 · 二级「科技政策推演」。只覆盖 SRS 序号 237–242，用户故事 `US-DS-POL-06`。挂接沿 `sdd/指标与501.md` §3.2 的 237–242 行，以及说明书第 2 节 DS-12 已有的 `metric_id` 与三档。读面沿 `POL-L2-DS12-SIM-ARCH`（含 2026-11-05 第 7、9 节）。本叶不改这些上游，不新造 `metric_id`，不改 D4。

推演页只认已有 `M_POLICY_SIMULATE`。该号只挂 232–234，归 `POL-L2-DS12-EST-METRIC`。本叶六叶不挂这条。

| 序号 | 叶子 | 指标 |
|---|---|---|
| 237 | 政策文本智能解析 | 不新建指标。行上保持已有 `M_POLICY_TEXT_PARSE`。MODEL。D4 仍是 mock。判定仍是 501。读 `ads.policy_text_parse` 的解析行。不调用 `polan.text.parse.run`。不灌缺项文本解析 |
| 238 | 政策重点可视化展示 | 无专属 `metric_id`。判定仍是 501。不挂 `M_POLICY_FOCUS_INDEX`，不挂 `M_POLICY_SIMULATE`。重点行上的号留空。读 `gapfill_policy_sim_result` 的重点行 |
| 239 | 政策影响范围分析 | 无专属 `metric_id`。判定仍是 501。不改成统计读面。不挂 `M_POLICY_SIMULATE`。影响范围行上的号留空。读同一张缺项表，跟随该政策上下文 |
| 240 | 政策关联分析 | 无独立 `metric_id`。判定仍是跨项索引。纸面 `M_POLICY_RELATION_DEGREE`（GRAPH，D4=`mock`）留在第 7 项。无 HTTP 资源。页面消费已有政策子图 |
| 241 | 政策实施路径预测 | 无专属 `metric_id`。判定仍是 501。不挂 `M_POLICY_LAYOUT_REC_COUNT`，不挂 `M_POLICY_DS_11_POLICY_EVAL_015`。路径环节行上的号留空。读同一张缺项表 |
| 242 | 政策解读报告生成 | 无专属 `metric_id`。判定仍是 501。解读段落行上的号留空。读同一张缺项表。页面呈现正文。不产生文件 |

未见 metric MCP。注册中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1、D2、D3 未查，分册里没有把它们写成已查到。回退出处是 `sdd/指标与501.md`。D4=`mock` 只转述该文件与架构稿。238、239、241、242 没有可改的 D4。

## 挂接表

| 序号 | metric_id | 注册中文名 | algorithm_type | D4 |
|---|---|---|---|---|
| 237 | `M_POLICY_TEXT_PARSE`（行上已有，不新建） | 未查（未见 metric MCP） | MODEL | mock |
| 238 | （空） | — | — | 无专属指标，不改 D4 |
| 239 | （空） | — | — | 无专属指标，不改 D4 |
| 240 | （无独立号。纸面跨项 `M_POLICY_RELATION_DEGREE` 不收成资源） | 未查（未见 metric MCP） | GRAPH（纸面，不改） | mock（纸面，不改） |
| 241 | （空） | — | — | 无专属指标，不改 D4 |
| 242 | （空） | — | — | 无专属指标，不改 D4 |

不新造指标。不改 D4。

`M_POLICY_SIMULATE` 不在上表。推演只认这一条已有号，挂在 232–234，本叶不写进 237–242 的行。

`POLICY_TEXT_PARSE` 的 `metric_ids` 同时列着 `M_POLICY_TEXT_PARSE` 与 `M_POLICY_DS_11_POLICY_EVAL_012`。`parse.run` 只把 `M_POLICY_TEXT_PARSE` 写入 `ads.policy_text_parse`，并会清空整表。本叶不改这份模型注册表，也不调用 `run()`。012 留在评价页 226。

## 偏离

无新 `metric_id`。与架构稿的读法差异：无。

`指标与501` 将 237、238、239、241、242 的判定列记为 501、页面空态，将 240 记为跨项索引。那是调研判定。本叶不改那份文件。读面按架构稿：237 读已有解析表；238、239、241、242 读 `gapfill_policy_sim_result`，无行则空，不用 501 充当功能；240 消费第 7 项子图，不设资源。三档不改：这六叶仍不是可接统计读面。240 仍是跨项索引。

相对 `task-get` 返回的 DoD「未注册模型保持 501」，以及说明书 11.2 仍把「文本解析」列在 SIM 组要灌清单：判定列保持 501。237 收窄为不灌文本解析，只读 `ads.policy_text_parse`。242 收窄为读解读段落行，不产生文件。这条收窄写在分册 §1.1，不回改说明书和 DoD。

`M_POLICY_SIMULATE` 不挂 237–242。`M_POLICY_FOCUS_INDEX` 不挂 238。`M_POLICY_LAYOUT_REC_COUNT` 与 `M_POLICY_DS_11_POLICY_EVAL_015` 不挂 241。232–236 只交叉引用 `POL-L2-DS12-EST-METRIC`。

未见 metric MCP，所以本叶没有中文名与叶子名的对照，也没有 `srs_refs` 对照。不把别的分册里曾经查到的中文名抄进来充当这次查询。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-SIM-METRIC.md`
- 本 handoff

未改指标 seed、矩阵、说明书、`指标与501.md`、`POL-L2-DS12-SIM-ARCH.md`、调研分册、WBS、模型注册表、`parse.py`、代码仓、`task-registry.yaml`。未调用 `task-update-status` / `task-update-fields`。未写代码。未写 OpenAPI。未提交 git。未 push。

## 验收证据

- 开工时 `task-get`（`project-0-gkx-orchestration-task-registry`）：`POL-L2-DS12-SIM-METRIC` 已是 `in_progress`，`claimed_by=agent:algorithm-agent`，`supervised_by=human:淮政玮`，`task_type=definition`，`depends_on` 含 `POL-L2-DS12-SIM-ARCH`。DoD 仍是「只用说明书第 2 节已有 metric_id 与三档」和「未注册模型保持 501，不写假公式，不改 D4，不新注册指标」。本叶未改状态。
- 动态工具目录中无 metric 命名空间，无 `metric-get`。分册写明「未见 metric MCP」，身份回退 `sdd/指标与501.md`。未读 seed 与矩阵 YAML。未编造 D1–D3。
- 挂接只使用说明书第 2 节 DS-12 与 `指标与501` §3 已有 id：237 行上保持 `M_POLICY_TEXT_PARSE`（MODEL，D4=`mock`，判定 501）。240 的纸面号是 `M_POLICY_RELATION_DEGREE`（GRAPH，D4=`mock`，跨项索引），本叶不设独立号、不设 HTTP 资源。238、239、241、242 仍无专属 id，行上留空。`M_POLICY_SIMULATE` 只认不挂。
- 读表沿架构稿：237 读 `ads.policy_text_parse` 解析行。238 重点、239 影响范围、241 路径环节、242 解读段落读 `gkxlumenx_gapfill.gapfill_policy_sim_result`。242 不产生文件。240 消费第 7 项子图。无行则该区空。
- 核对 `vendor/entan-py/polan/text/parse.py`：`run()` 清空 `ads.policy_text_parse` 后插入，行上 `metric_id` 固定 `M_POLICY_TEXT_PARSE`。本叶不调用 `run()`，不把截取收成公式。
- 核对 `cfg_model_registry.yaml`：`POLICY_TEXT_PARSE` 含 `M_POLICY_TEXT_PARSE` 与 `M_POLICY_DS_11_POLICY_EVAL_012`；`POLICY_SIMULATE` 含 `M_POLICY_SIMULATE`；`POLICY_RE` 与 `POLICY_FOCUS` 含 `M_POLICY_RELATION_DEGREE`。本叶不改该文件，不调用这些 `invoke_path`。
- 未写可算出数的公式。未把 237 收成缺项灌数。未把 242 收成文件。未把 232–236 写进本分册正文挂接。
- 指标设计稿与本 handoff 已落盘。定义单，无业务 PR，无 pipeline。
- 会签态 `draft`。不代签。不标 done。不标 `ready_to_sign`。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单不改算法。解析只作指认：`polan.text.parse.run` 会清空解析表，展示请求不调用它 |
| 调用链 | ✅ 沿架构稿。237/238/239/241/242 走 `POST /display/v1/policy/simulation/jobs`。240 无 HTTP 资源。本单不改链，不写 OpenAPI |
| 图谱 | ✅ 240 消费第 7 项已有子图。不写 nGQL，不建查图任务 |
| 可观测 | ✅ 不新设计观测点，沿既有展示链 |
| D9 | ✅ 只用已有 metric_id。八件套与 D1–D4 分开。未见 metric MCP 的字段留空不编。`M_POLICY_TEXT_PARSE` 与纸面 `M_POLICY_RELATION_DEGREE`、`M_POLICY_SIMULATE` 的 D4 保持 mock。238、239、241、242 不新造 id |
| D12 | ✅ 不把展示调用链改去 demo 文本解析签、`/v1/policy/text/parse` 或 `/internal/analysis/policy/text-parse`。已有 `run()` 只作指认，本单不改、不调用 |
| D16 / D18 | ✅ 238、239、241、242 读 `gapfill_policy_sim_result`，行上号留空。237 读已有 ADS 解析行，不灌缺项文本解析。不用 501 充当功能。本单不灌数，不把 mock 写成已上线。接口不直接返回写死的 mock |
| D17 | ✅ 不改锁定算法，不改 `parse.py`，不改模型注册表 |
| D14 | ✅ 本单不写对象存储。242 不产生文件 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000（与任务 `estimated_tokens` 同量级的定义单记录；无 Console 分项） |
| model_used | grok-4.7 |
| actual_cost | 未回写。价表无 grok-4.7 档。本会话不调用 `task-update-fields` |
| cost_warn | 未回写 |

`user_story` 为 `US-DS-POL-06`。证据为本 handoff。状态未改。

## 测试结果

定义单。未改业务仓，无单测，无 pipeline。核对方式是对照架构稿（含 2026-11-05 第 7、9 节）、`指标与501` §3 的 237–242 行、说明书第 2 节 DS-12 与第 11.2 节，以及 `parse.py` 与 `POLICY_TEXT_PARSE` 注册项，确认没有新 id、没有改 D4、没有假公式、237 不调用 `run()` 且不灌文本解析、240 无独立号且无 HTTP 资源、242 不产生文件、`M_POLICY_SIMULATE` 不挂本叶。

## 遗留风险

- 未见 metric MCP。注册中文名、口径、公式、注册源表、D1–D3 仍未在本叶核对。下游若要写八件套全文，须等 metric MCP 可用后再查，不能把本叶的空项当成「注册表没有这些字段」。
- `GDF-POLICY-MOCK-GATE-L01` 在 `指标与501` 里仍是 blocked。缺项行在对齐前仍是 mock。`M_POLICY_TEXT_PARSE` 的 D4 仍是 mock，解析行已落库也不升 live。
- 238、239、241、242 没有专属指标。缺项表没有行时，重点、影响范围、路径和解读正文为空。
- 说明书 11.2 仍把文本解析写在要灌清单里。灌数单须按架构 §9 执行「文本解析不灌」。本叶不改说明书。
- 模型注册表把 `M_POLICY_TEXT_PARSE` 标成 active 并给出内部 `invoke_path`。展示请求仍不调用 `run()`。下游不要据此在 237 的请求路径里跑解析。
- `M_POLICY_RELATION_DEGREE` 同时出现在 `POLICY_RE` 与 `POLICY_FOCUS`。240 仍无独立号、无 HTTP 资源。下游不要为它单开 `simulation/jobs` 种类。
- 232–236 的指标分册尚未在本工作区见到。本叶只交叉引用 `POL-L2-DS12-EST-METRIC`，不代写。

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

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-SIM-METRIC.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS12-SIM-METRIC.md`

## 修改内容

- `sdd/l2/POL-L2-DS12-SIM-METRIC.md`
- 本 handoff
