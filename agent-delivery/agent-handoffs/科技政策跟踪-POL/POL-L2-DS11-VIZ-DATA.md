ponytail: off

# POL-L2-DS11-VIZ-DATA · 政策分析评价可视化数据落点

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| lock_until | `2026-11-03T19:53:22.152Z` |
| 状态 | `in_progress`。本单不改任务状态 |
| 说明 | 定义单。只写数据落点。列级定义只定粒度和必要列。不建库，不灌数，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过 D9、D16 行级列、调用链、两张缺项表的拣行键，以及 221 只消费、222 无选用行则空。

## 范围

政策分析评价 · 二级「政策分析报告可视化呈现」。SRS 序号 219–222，用户故事 `US-DS-POL-05`。上游是 `POL-L2-DS11-VIZ-ARCH` 第 9 节，以及说明书第 11.2 节评价可视化那一行。数据落点写在 `sdd/l2/POL-L2-DS11-VIZ-DATA.md`。

新表只有 `gkxlumenx_gapfill` 下两张：`gapfill_policy_eval_trend`、`gapfill_policy_eval_partition`。不写 ODS、DWD、ADS。221 不建表。222 不建表。

| 序号 | 叶子 | 落点 | 读取方 | 灌数方 | 拣行 |
|---|---|---|---|---|---|
| 219 | 多维指标趋势图 | `gapfill_policy_eval_trend` | `gkxlumen-element` | `POL-L2-DS11-VIZ-GAPFILL-L01` | `switch_dim` 与 `metric_name`。无行则图空 |
| 220 | 分区/群体对比分析图 | `gapfill_policy_eval_partition` | `gkxlumen-element` | 同一张灌数单 | `object_kind`；投向有值时再按 `resource_direction`。无行则图空 |
| 221 | 多维结构关联图 | 第 7 项已有政策子图 | 展示只消费该子图 | 无 | 无表行。无子图则空 |
| 222 | 报告模板定制与批量导出 | 已有 `gapfill_policy_eval_shell` | `gkxlumen-element` | 无。不把模板选用加进 `POL-L2-DS11-READ-GAPFILL-L01` | 模板选用。无选用行则空 |

接口只读表或只消费已有子图，不直接返回 mock。

## 表与粒度

219 一行是一个趋势点：`switch_dim`（时间、区域、类别）、`dim_value`、`metric_name`、`point_value`。重点和波动是该点上的 `is_key_point`、`is_fluctuation`，不另算指标。查询按维和指标名拣出该序列上的全部点。

220 一行是一个对象上的对照：`object_kind`（地区、行业、目标群体）、`object_name`、`compare_value`，投向在 `resource_direction`。图种不落列。柱和热力读同一批行。

221 不建表。`E-E7-POLICY-M1-L02` 已完成。抽取脚本 `GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog，本单不重开。Java 不写 nGQL。

222 读解读分册已经定下的壳表。`entry_kind` 只有解读和多媒体，并与 224、225 的 `gap_item` 成对。没有模板选用这一对。本单不加列。按模板选用拣行则空。文件和操作日志不灌。

两张新缺项表都带 `is_mock=1`。`metric_id` 留空。`fill_method=manual`，不设 `fill_model`。`gap_item` 带序号和叶子名。另有 `gapfill_batch_id`、`generated_at`。列清单在数据落点正文第 3、4 节。那是逻辑列，不是可执行 SQL。

D4 保持 mock。空表返回空。

## 灌数单

只点名，本单不执行。

| 灌数单 | 点名内容 |
|---|---|
| `POL-L2-DS11-VIZ-GAPFILL-L01` | 按本单逻辑列建两张缺项表并灌数。依赖本单。查询请求不调用它 |
| `POL-L2-DS11-READ-GAPFILL-L01` | 只灌 224、225。本单不把模板选用加进去，不执行 |

## 不重开 GDF

不重开 GDF。不写 nGQL。不加已有 ADS 列。不新造 `metric_id`。不把 D4 从 mock 改绿。

## 偏离

无实现偏离。本单不改代码，不建表。

壳表的列以已落盘的 `POL-L2-DS11-READ-DATA` 第 5 节为准。该分册没有模板选用行。本单按架构第 9 节保持「无选用行则空」，不回头给壳表加一种行。

说明书第 11.2 节仍把可视化放在未开工二级。本单不改说明书。两张表名和灌数单与该行一致。221 不建表与该行一致。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-VIZ-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-VIZ-DATA.md`（本 handoff）

未改代码仓，未改 `task-registry.yaml`，未改 `POL-L2-DS11-READ-DATA.md`，未改 WBS、说明书、VIZ-ARCH、兄弟分册、GDF 派单包。任务状态保持 `in_progress`。

## 验收证据

- 新建表只有 `gapfill_policy_eval_trend`、`gapfill_policy_eval_partition`，库是 `gkxlumenx_gapfill`。灌数单是 `POL-L2-DS11-VIZ-GAPFILL-L01`。不写 ODS、DWD、ADS。
- 219 拣行键是切换维和指标名。220 拣行键是对象，投向有值时再按投向。读取方都是 `gkxlumen-element`。无行则空。
- 221 不建表，只消费第 7 项已有子图。无子图则空。
- 222 读已有 `gapfill_policy_eval_shell`。本叶不建表。模板选用不进入 `POL-L2-DS11-READ-GAPFILL-L01`。无选用行则空。
- 灌数单只出现在点名表。本单没有建库、没有插入。
- 定义任务，未跑业务 CI，未部署。未会签。不标 done。

## 架构合规自检

- ✅ 调用链：浏览器只打 `/display/v1/policy/**`。219、220、222 由 `gkxlumen-element` 只读。221 不新开查图。display 不直连库，不直连 Python。
- ✅ Java 不写算法。本叶没有可迁移的趋势、分区或导出模型。
- ✅ 不写 nGQL，不重开 GDF。
- ✅ D9：不新造 `metric_id`，不改 D4。无行不造 0。
- ✅ D16：两张新表只在 `gkxlumenx_gapfill`，行上带规定列。不写 ODS、DWD、ADS、供应方库。生产配置不读缺项库。
- ✅ D18：接口只读表或只消费已有子图，不直接返回 mock。221、222 不另建表。
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
| diagram_id | `POL-L2-DS11-VIZ-ARCH-SEQ` |
| 图 diff | 本数据叶不改图、不加边。读路径沿用架构第 2 节和第 5 节 |
| 会签态 | 未会签。源文件无 frontmatter，记 `draft`。不自填绿 |
| 说明 | 数据落点不替代该图。未会签通过 |

## 修改内容

- 新增 `sdd/l2/POL-L2-DS11-VIZ-DATA.md`
- 新增本 handoff
