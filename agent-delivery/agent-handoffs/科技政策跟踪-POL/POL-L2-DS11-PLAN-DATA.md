ponytail: off

# POL-L2-DS11-PLAN-DATA · 政策分析评价推荐方案数据落点

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| lock_until | `2026-11-03T19:53:23.439Z` |
| 状态 | `in_progress`。本单不改任务状态 |
| 说明 | 定义单。只写数据落点。列级定义只定粒度和必要列。不建库，不灌数，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过 D9、D16 行级列、调用链、一张缺项表的四种行和拣行键。

## 范围

政策分析评价 · 二级「推荐方案报告交互展示」。SRS 序号 227–231，用户故事 `US-DS-POL-05`。上游是 `POL-L2-DS11-PLAN-ARCH` 第 5 节和第 9 节，以及说明书第 11.2 节「评价 · 方案 227–231」那一行。数据落点写在 `sdd/l2/POL-L2-DS11-PLAN-DATA.md`。

新表只有 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。不写 ODS、DWD、ADS 新表。本二级不读已有 ADS。

| 序号 | 叶子 | 落点 | 拣行 |
|---|---|---|---|
| 227 | 多方案对比展示 | 方案对照行 | `scheme_name`。不选则读全部。少于两行则对比空 |
| 228 | 方案参数自定义模拟 | 参数模拟行 | `scheme_name` + `param_band`。对不上则空 |
| 229 | 实施路径与风险辅助 | 路径与风险行 | `scheme_name`。无行则路径和风险都空 |
| 230 | 互动意见收集与专家参与 | 互动意见行 | `scheme_name`。不选或无行则列表空 |
| 231 | 方案报告导出与归档 | 不另建行。读方案对照行和意见行 | 没有方案对照行则导出空 |

读取方都是 `gkxlumen-element`。灌数方是 `POL-L2-DS11-PLAN-GAPFILL-L01`。接口只读表，不直接返回 mock。

## 表与粒度

一张表，四种 `row_kind`：方案对照、参数模拟、路径与风险、互动意见。231 不占种类。

227 一行是一个方案：名称、一句说明、对照维度和数值、优劣结论、实施建议。方案名在方案对照行上互不相同。

228 一行是一个方案上的一个参数档，含评估结果、一句趋势、一条归档说明。同一方案同一参数档只留一行。采纳不插入新行。

229 一行是一个方案上的一个节点，含时间进度、节点说明、风险标题和一句风险。一个方案可以多行。`metric_id` 使用已有 `M_POLICY_DS_11_POLICY_EVAL_015`。不改这条指标，不改 D4。

230 一行是一个方案上的一条已定意见：主体、分类（评价、评论、建议）、正文、时间。意见请求不插入新行。

231 不灌。导出从当次读到的方案对照行和意见行生成，不落文件列。

每行 `is_mock=1`。`fill_method=manual`，不设 `fill_model`。`gap_item` 带序号和叶子名。另有 `gapfill_batch_id`、`generated_at`。227、228、230 的 `metric_id` 留空。列清单在数据落点正文第 3 节。那是逻辑列，不是可执行 SQL。

D4 保持 mock。空表或对不上的行返回空。

## 灌数单

只点名，本单不执行。

| 灌数单 | 点名内容 |
|---|---|
| `POL-L2-DS11-PLAN-GAPFILL-L01` | 灌方案对照、参数模拟、路径与风险、已定意见行。不灌 231 的导出文件。意见请求不插入新行。依赖本单。查询请求不调用它 |

## 不重开 GDF

不重开 GDF。不写 nGQL。不写 ODS、DWD、ADS、供应方库。不新造 `metric_id`。不把 D4 从 mock 改绿。不改 `M_POLICY_DS_11_POLICY_EVAL_015`。

## 偏离

无实现偏离。本单不改代码，不建表。

本二级不读已有 ADS。`ads.policy_simulate` 留在推演键，不写入本表。说明书第 11.2 节仍是「评价 · 方案」那一行的表名和灌数单。本单不改说明书。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-PLAN-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-PLAN-DATA.md`（本 handoff）

未改代码仓，未改 `task-registry.yaml`，未改 WBS、说明书、PLAN-ARCH、`POL-L2-DS11-READ-DATA.md`、`POL-L2-DS11-VIZ-DATA.md`。任务状态保持 `in_progress`。

## 验收证据

- 新表只有 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`，与架构第 9 节、说明书第 11.2 节一致。
- 227 按方案。228 按方案和参数档。229、230 按方案。231 不另建行。
- 229 行带已有 `M_POLICY_DS_11_POLICY_EVAL_015`。其余三种 `metric_id` 留空。未新造 `metric_id`，未改 D4。
- 灌数单只出现在点名表。本单没有建库、没有插入。
- 定义任务，未跑业务 CI，未部署。未会签。不标 done。

## 架构合规自检

- ✅ 调用链：浏览器只打 `/display/v1/policy/**`。缺项表由 `gkxlumen-element` 只读。display 不直连库，不直连 Python。
- ✅ Java 不写算法。不调用 `polan.text.simulate`。
- ✅ 不写 nGQL，不重开 GDF。
- ✅ D9：不新造 `metric_id`，不改 D4。无行不造数。
- ✅ D16：新表只在 `gkxlumenx_gapfill`，行上带规定列。不写 ODS、DWD、ADS、供应方库。生产配置不读缺项库。
- ✅ D18：接口只读表，不直接返回 mock。231 不灌文件。
- ✅ 未会签，不标 done。

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
| diagram_id | `POL-L2-DS11-PLAN-ARCH-SEQ` |
| 图 diff | 本数据叶不改图、不加边。读路径沿用架构第 2 节 |
| 会签态 | 未会签。源文件无 frontmatter，记 `draft`。不自填绿 |
| 说明 | 数据落点不替代该图。未会签通过 |

## CI/CD

- 分支：`origin/dev`
- 定义任务，未跑业务 CI，未部署

## 修改内容

- 新增 `sdd/l2/POL-L2-DS11-PLAN-DATA.md`
- 新增本 handoff
