ponytail: off

# POL-L2-DS11-VIZ-DATA · 政策分析评价政策分析报告可视化呈现数据落点

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 本单查询未返回该字段。注册表已是 in_progress，claimed_by 为 `agent:data-agent`。本 handoff 不重新认领 |
| 说明 | 定义单。只写数据落点。列级定义只定粒度和必要列。不建库，不灌数，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过 D9、D16 行级列、调用链和空表返回空。

## 范围

政策分析评价 · 二级「政策分析报告可视化呈现」。SRS 序号 219–222，用户故事 `US-DS-POL-05`。上游是 `POL-L2-DS11-VIZ-ARCH` 第 5、9 节。注册表该架构单为 done，note 写 `human:淮政玮` 签收。架构稿正文头仍写待签收。本单不改那份稿，不改图。数据落点写在 `sdd/l2/POL-L2-DS11-VIZ-DATA.md`。

| 序号 | 叶子 | 落点 |
|---|---|---|
| 219 | 多维指标趋势图 | `gkxlumenx_gapfill.gapfill_policy_eval_trend`。一行一个趋势点 |
| 220 | 分区/群体对比分析图 | `gkxlumenx_gapfill.gapfill_policy_eval_partition`。一行一个对象对照 |
| 221 | 多维结构关联图 | 不建表。只消费第 7 项已有政策子图 |
| 222 | 报告模板定制与批量导出 | `gkxlumenx_gapfill.gapfill_policy_eval_template`。一行一条模板选用 |

## 表与粒度

219 一行一个趋势点，只落在一个切换维上。维只有时间、区域、类别。行上有该维的一个位置、评估指标名、一个对照值。`metric_id` 留空。`gap_item` 为 `219 多维指标趋势图`。`fill_method=manual`。另有 `gapfill_batch_id`、`generated_at`、`is_mock=1`。不设 `fill_model`。未勾选的维不读。无行则图空，不造 0。

220 一行一个对象对照。对象只有地区、行业、目标群体。行上有对象名称、一个对照数、可空的资源投向。图种不落列，柱和热力读同一批行。`metric_id` 留空。`gap_item` 为 `220 分区/群体对比分析图`。`fill_method=manual`。无行则图空。

221 不定点边列。`E-E7-POLICY-M1-L02` 已完成。`GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog，本单不重开。子图没有则该块空。

222 一行一条模板选用：模板名，以及该行允许的一个汇报周期、一个分析维度、一个图表类型。多种允许组合分成多行。分析维度取时间、区域、类别、地区、行业、目标群体。图表类型取趋势、柱状、热力、弦线、关系网。汇报周期写在行上，本单不把近 1 年、近 3 年、近 5 年收成闭集。格式 PDF、Excel 不落列。`metric_id` 留空。`gap_item` 为 `222 报告模板定制与批量导出`。`fill_method=manual`。无行则模板区空。

三张表只在 `gkxlumenx_gapfill`。不读已有 ADS。不写 ODS、DWD、ADS、供应方库。不写 `gapfill_policy_eval_shell`。壳表只服务 224、225。D4 保持 mock。查询不插入。列清单不是可执行 SQL。

## 灌数单

只点名，本单不认领，不执行。

| 灌数单 | 点名内容 |
|---|---|
| `POL-L2-DS11-VIZ-GAPFILL-L01` | 按本单第 2、3、5 节建三张表并灌趋势点、分区对照、模板选用行。依赖本单。状态仍是 backlog |

该单登记完成定义仍只写趋势表和分区表。注册 note 已指向架构第 9 节的第三张表。本分册补上 `gapfill_policy_eval_template` 的列。执行时以本分册和架构第 9 节为准，覆盖三张表。本单不改那张灌数单的注册字段。

不灌 PDF、Excel、假操作日志、解读条目、多媒体条目、弦线矩阵、演示路径。查询请求不灌数。

## 不重开 GDF

不重开 GDF。不写 nGQL。不写第二套统计脚本。不新造 `metric_id`。不把 D4 从 mock 改绿。

## 偏离

无实现偏离。219、220、222 的库表与架构第 5、9 节一致。221 与架构一致，不建表。

灌数单注册完成定义仍只写两张表。本单不改那张任务。执行时以本分册和架构第 9 节为准，三张表都建。

架构稿正文头仍写待签收。注册表该单已是 done。本单不改架构稿。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-VIZ-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-VIZ-DATA.md`（本 handoff）

未改代码仓，未改 `task-registry.yaml`，未 commit，未 push。未改说明书、WBS、`指标与501.md`、解读分册、方案分册、架构稿。未认领 `POL-L2-DS11-VIZ-GAPFILL-L01`。未建库，未灌数。

## 验收证据

- 219、220、222 的库表与架构第 5、9 节一致。221 不建表。
- 三张表的 D16 列按本单写明：`metric_id` 留空，`gap_item` 带序号和叶子名，`fill_method=manual`，`gapfill_batch_id`，`generated_at`。
- 壳表不在本叶。不灌 PDF、Excel、假日志、解读条目、多媒体条目。
- 灌数单只出现在点名表。本单没有建库、没有插入。
- 定义任务，未跑业务 CI，未部署。待会签。不标 done，不标 ready_to_sign。

## 架构合规自检

- ✅ 调用链：219、220 的 `jobs` 与 222 的 `shells` 由 `gkxlumen-element` 只读。展示不直连库，不直连 Python。221 不新开资源。
- ✅ Java 不写算法。本单不改代码。
- ✅ 不写 nGQL。221 只消费第 7 项已有子图。
- ✅ D9：不新造 `metric_id`，不改 D4。无行不造 0。三叶 `metric_id` 留空。
- ✅ D14：不灌 PDF、Excel，不新建桶，不写对象键。
- ✅ D16：三张表只在 `gkxlumenx_gapfill`，表名以 `gapfill_` 开头，行上带规定列，`fill_method=manual`。不写 ODS、DWD、ADS、供应方库。
- ✅ D18：mock 先落缺项表再被查询。查询不直接返回 mock。221 无子图则空。
- ✅ 不重开 GDF。

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS11-VIZ-ARCH-SEQ` |
| 图 diff | 本数据叶不改图、不加边。读路径沿用架构第 5、9 节 |
| 会签态 | `draft`。源文件无 frontmatter，沿架构稿记 draft。不自填绿 |
| 说明 | 数据落点不替代该图。本单待会签。不标 done |

## 问题清单

- `POL-L2-DS11-VIZ-GAPFILL-L01` 的登记完成定义仍只写趋势表和分区表。执行该单时以本分册和架构第 9 节为准，覆盖三张表。本单不改那张任务。
- 架构稿正文头仍写待签收，注册表该单已是 done。本单不改架构稿。

## 修改内容

- 新增 `sdd/l2/POL-L2-DS11-VIZ-DATA.md`
- 新增本 handoff

## 测试结果

- 只读核对 `POL-L2-DS11-VIZ-ARCH.md` 第 5、9 节与第 3 节闭集。
- 只读核对 `指标与501.md` 219–222：219、220、222 仍是 501，221 仍是跨项索引。本单未改这些句子。
- 只读核对灌数单注册完成定义仍是两张表、状态 backlog。未建库，未插入。

## 遗留风险

- 灌数单登记完成定义与本分册不一致，直到该单按本分册执行。本单不认领它。
- 说明书第 11.2 节仍可能把模板选用写在壳表。可执行落点以架构第 9 节和本分册为准。本单不改说明书。

## CI/CD

- 分支：未提交
- commit：无
- pipeline URL / ID：无。定义任务，`cicd: skip`
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：未部署。未建库，未灌数

## 可观测性

- OTEL_SERVICE_NAME：本叶不新设计观测点。trace 沿既有展示链
- traceId（dev 抽样）：无。未发请求
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-VIZ-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-VIZ-DATA.md`
