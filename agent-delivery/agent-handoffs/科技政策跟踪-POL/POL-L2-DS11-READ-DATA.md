ponytail: off

# POL-L2-DS11-READ-DATA · 政策分析评价结果解读数据落点

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| lock_until | `2026-11-03T19:44:11.121Z` |
| 状态 | `in_progress`。本单不改任务状态 |
| 说明 | 定义单。只写数据落点。列级定义只定粒度和必要列。不建库，不灌数，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过 D9、D16 行级列、调用链、三张已有 ADS 和 shell 的拣行键。

## 范围

政策分析评价 · 二级「结果解读报告多维展示」。SRS 序号 223–226，用户故事 `US-DS-POL-05`。上游是已会签的 `POL-L2-DS11-READ-ARCH` 第 8 节（该稿没有第 9 节）和四份会签页，以及说明书第 11.2 节解读那一行。数据落点写在 `sdd/l2/POL-L2-DS11-READ-DATA.md`。

新表只有 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。只灌 224 的解读条目，以及 225 的多媒体标题和一句说明。不灌视频，不灌 PDF，不灌模板选用。不建 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`。

223 短板读已有 `ads.policy_effect`（`scope_type=region_gap`）。223 焦点读已有 `ads.policy_focus`（`policy_id` 非空）。226 读已有 `ads.policy_text_parse.summary`。

| 序号 | 叶子 | 落点 | 读取方 | 灌数方 | 拣行 |
|---|---|---|---|---|---|
| 223 短板 | 热点问题分析看板 | 已有 `policy_effect` | `gkxlumen-element` | 已有 `gap.run`。`counts` 不调用 | `scope_type=region_gap` |
| 223 焦点 | 热点问题分析看板 | 已有 `policy_focus` | Python Job `policy_focus_ads` | 同一次已有 `focus.run` | `policy_id` 非空 |
| 224 | 分主题分指标互动解读 | shell 的解读行 | `gkxlumen-element` | `POL-L2-DS11-READ-GAPFILL-L01` | `entry_kind=解读` |
| 225 | 多媒体辅助解读 | shell 的多媒体行 | `gkxlumen-element` | 同一张灌数单 | `entry_kind=多媒体` |
| 226 | 智能摘要与结论推送 | 已有 `policy_text_parse.summary` | Python Job `policy_text_parse` | 已有 `parse.run`。展示请求不调用 | 现有行，只取 `summary` |

接口只读表，不直接返回 mock。无行则空。

## 表与粒度

223 短板一行是一个区域在 `scope_type=region_gap` 上的 `shortboard_cnt`，分项原因在已有 `ext.reasons`。行上 `metric_id` 仍是 `M_POLICY_SHORTBOARD_COUNT`。不建 `ads.policy_gap`。

223 焦点一行是 `policy_id` 非空的一条政策。读 `focus_score`、`ext.title`、`ext.explanation`。行上 `metric_id` 仍是 `M_POLICY_FOCUS_INDEX/M_POLICY_RELATION_DEGREE`。`relation_degree` 不改挂。不建 `gapfill_policy_eval_focus`。

224 一行是一个专题或指标名、一句结论、一句应用建议。225 一行是一个标题和一句说明。两类行都在 `gapfill_policy_eval_shell`，用 `entry_kind` 与 `gap_item` 成对拣行。不设视频、PDF、模板列。

226 只读已有 `summary`。行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。展示读面仍是已有 `M_POLICY_DS_11_POLICY_EVAL_012`。不建 `gapfill_policy_eval_summary`。展示请求不调用 `parse.run`。

shell 每行 `is_mock=1`。`metric_id` 没有已挂指标则留空。`fill_method=manual`，不设 `fill_model`。`gap_item` 带序号和叶子名。另有 `gapfill_batch_id`、`generated_at`。列清单在数据落点正文第 5 节。那是逻辑列，不是可执行 SQL。

D4 保持 mock。空表返回空。

## 灌数单

只点名，本单不执行。

| 灌数单 | 点名内容 |
|---|---|
| `POL-L2-DS11-READ-GAPFILL-L01` | 按本单逻辑列建 shell，只灌 224 解读条目和 225 标题加一句说明。依赖本单。查询请求不调用它 |
| 已有 `gap.run` | 写短板行。不进灌数单。本单不执行、不改公式 |
| 已有 `focus.run` | 焦点 Job 调用它后再读。本单不执行、不改公式 |
| 已有 `parse.run` | 写 `summary`。展示请求不调用。本单不执行 |

## 不重开 GDF

不重开 GDF。不写 nGQL。不加已有 ADS 列。不新造 `metric_id`。不把 D4 从 mock 改绿。不写 ODS、DWD、ADS、供应方库。

## 偏离

无实现偏离。本单不改代码，不建表。

架构第 7 节写说明书第 11.2 节仍把焦点缺项表、摘要缺项表和 shell 放在同一行。当前说明书该行已经只列 `gapfill_policy_eval_shell`，并写明三张已有 ADS 的读法，以及不灌 PDF、不灌视频。本单不改说明书，不改架构稿。落点与该行、架构第 8 节、数据会签页一致。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-READ-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-READ-DATA.md`（本 handoff）

未改代码仓，未改 `task-registry.yaml`，未改 WBS、说明书、READ-ARCH、会签页、兄弟分册、GDF 派单包。任务状态保持 `in_progress`。主工作区有其他未提交文件，本单在临时 worktree 提交，不触碰那些文件。

## 验收证据

- 新建表只有 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。未列入 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`、`ads.policy_gap`。
- shell 只灌 224 解读条目和 225 标题加一句说明。不灌视频、PDF、模板选用。
- 223 短板拣行键是 `scope_type=region_gap`。223 焦点拣行键是 `policy_id` 非空。226 只取已有 `summary`。224、225 按 `entry_kind` 与 `gap_item` 成对拣行。
- 每张表都写了读取方和灌数方。无行则空。接口不直接返回写死 mock。
- 灌数单只出现在点名表。本单没有建库、没有插入、没有调用 `run()`。
- 定义任务，未跑业务 CI，未部署。本数据叶未会签。不标 done。

## 架构合规自检

- ✅ 调用链：浏览器只打 `/display/v1/policy/**`。短板和 shell 由 `gkxlumen-element` 只读。焦点和摘要走已有异步任务管道，再到 Python `/internal/*`。display 不直连库，不直连 Python。
- ✅ Java 不写算法。焦点沿用已有 `polan.eval.focus.run`。短板和摘要的展示请求不调用 `gap.run`、`parse.run`。本单不改这些函数。
- ✅ 不写 nGQL，不重开 GDF。关联度不改挂。
- ✅ D9：不新造 `metric_id`，不改 D4。无行不造 0。
- ✅ D16：新表只在 `gkxlumenx_gapfill`，行上带规定列。不写 ODS、DWD、ADS、供应方库。生产配置不读缺项库。
- ✅ D14：不写对象存储。多媒体不灌文件。
- ✅ D18：接口只读表，不直接返回 mock。223、226 不另建表。三张 ADS 已有。
- ✅ 本数据叶未会签，不标 done。

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | 未计 |

未回写注册表的成本字段。本单不改任务状态。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS11-READ-ARCH-SEQ` |
| 图 diff | 本数据叶不改图、不加边。读路径沿用架构第 2 节 |
| 会签态 | 上游四页 2026-11-03 同意。源文件无 frontmatter，不自填绿。本数据叶未会签 |
| 说明 | 数据落点不替代该图 |

## 修改内容

- 新增 `sdd/l2/POL-L2-DS11-READ-DATA.md`
- 新增本 handoff
