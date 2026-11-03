ponytail: off

# POL-L2-DS10-CMP-DATA · 科创政策全景政策重点比对数据落点

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| lock_until | `2026-11-03T14:29:55.375Z` |
| 状态 | `in_progress`。本单不改任务状态 |
| 说明 | 定义单。只写数据落点。列级定义只定粒度和必要列。不建库，不灌数，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过 D9、D16 行级列、调用链、已有力度表和四张缺项表的拣行键。

## 范围

科创政策全景 · 二级「政策重点比对」。SRS 序号 213–218，用户故事 `US-DS-POL-04`。上游是已签收的 `POL-L2-DS10-CMP-ARCH` 第 5 节和第 9 节，以及说明书第 11.2 节重点比对那一行。数据落点写在 `sdd/l2/POL-L2-DS10-CMP-DATA.md`。

新表只有 `gkxlumenx_gapfill` 下四张：`gapfill_policy_version_diff`、`gapfill_policy_detail_compare`、`gapfill_policy_benchmark_report`、`gapfill_policy_impl_dept`。不建 `gapfill_policy_benchmark_viz`。不写 ODS、DWD、ADS 新表。

`ads.policy_intensity` 已有。支持力度由 `gkxlumen-element` 同步读。力度分由已有 `run()` 写入，请求不现算。

| 序号 | 叶子 | 落点 | 拣行 |
|---|---|---|---|
| 213 | 政策新旧对比 | `gapfill_policy_version_diff` | 政策加两个发布时间。时点不从缺项表反查 |
| 214 | 政策详情对比 | 条件与材料：`gapfill_policy_detail_compare`。力度分：已有 `policy_intensity` | 条件材料按政策 |
| 215 | 部门政策对比 | `gapfill_policy_impl_dept` | 区域、部门、方面 |
| 216 | 标杆比对功能 | 已有力度表上的支持力度。element 同步读 | 不进灌数单。请求不现算 |
| 217 | 对标报告生成与导出 | `gapfill_policy_benchmark_report` | 对标对象和已勾字段 |
| 218 | 对标结果可视化展示 | 已有力度表 | 不建可视化缺项表 |

四张缺项表的灌数方都是 `POL-L2-DS10-CMP-GAPFILL-L01`，读取方都是 `gkxlumen-element`。接口只读表，不直接返回 mock。

## 表与粒度

213 一行是同一政策在两个 `publish_date` 之间的一条变更（新增、修改、删除）和一句摘要。两个日期列是 `publish_date_a`、`publish_date_b`。时点来自已有 `policy_base_info.publish_date`。同一政策只有一个发布日期时对比空。不设版本号。

214 的申报时间、受理部门、产业类别留在已有正文。缺项表一行一条政策，列是 `apply_condition`、`apply_material`。力度分是 `policy_intensity.intensity_score`（`scope_type=policy`，`metric_id=M_POLICY_INTENSITY_SCORE`），由已有 `polan.eval.intensity.run()` 写入。展示请求不在返回语句里现算。

215 一行是一个区域、一个实施部门、一个方面（`项目类别` 或 `技术类别`），带 `item_count` 和 `list_title`。件数不挂 `M_POLICY_TOTAL_COUNT`。区域和类别词表仍走已有目录。

216 不加列。element 在 `panorama/stats` 上同步读已有 `run()` 写下的支持力度。这次统计请求不调用 `run()`。同一份 `run()` 把 `M_POLICY_SUPPORT_STRENGTH` 写在同库已有 `policy_metric_timeseries`（`metric_value`，`dim_key` 为支持力度）。`policy_intensity` 没有支持力度列。本单不补列。

217 一行是一个对标对象加一个已勾字段（政策类型、支持力度、覆盖范围），含差异、优劣、借鉴和报告正文。导出文件从读到的行生成，不落文件列。

218 不建表。图读 214 的力度分和 216 的支持力度。

四张缺项表都带 `is_mock=1`。`metric_id` 留空。`fill_method=manual`，不设 `fill_model`。`gap_item` 带序号和叶子名。另有 `gapfill_batch_id`、`generated_at`。列清单在数据落点正文第 3、4、5、7 节。那是逻辑列，不是可执行 SQL。

D4 保持 mock。空表返回空。

## 灌数单

只点名，本单不执行。

| 灌数单 | 点名内容 |
|---|---|
| `POL-L2-DS10-CMP-GAPFILL-L01` | 按本单逻辑列建四张缺项表并灌数。依赖本单。查询请求不调用它 |
| 已有 `intensity.run()` | 写入力度分和支持力度。216 不进灌数单。本单不执行、不改公式 |

## 不重开 GDF

不重开 GDF。不写 nGQL。不加已有 ADS 列。不新造 `metric_id`。不把 D4 从 mock 改绿。

## 偏离

无实现偏离。本单不改代码，不建表。

架构第 5.4 节写 element 只读 `ads.policy_intensity` 里已经写下的支持力度。`ads.md` 展示窗口也把 `M_POLICY_SUPPORT_STRENGTH` 映到 `policy_intensity`。已有 `run()` 实际把该指标写在同库 `policy_metric_timeseries`。`policy_intensity` 上没有支持力度列，力度分在 `intensity_score`。本单不补列，不改 `run()`，不改 `ads.md`，不改架构稿。element 仍是同步读取方，统计请求仍不现算。

说明书第 11.2 节仍把重点比对放在未开工二级。本单不改说明书。四张表名和灌数单与该行一致。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-CMP-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-CMP-DATA.md`（本 handoff）

未改代码仓，未改 `task-registry.yaml`，未改 WBS、说明书、CMP-ARCH、兄弟分册、GDF 派单包。任务状态保持 `in_progress`。

## 验收证据

- 四张缺项表与架构第 9 节、说明书第 11.2 节重点比对那一行的表名一致。未列入 `gapfill_policy_benchmark_viz`。
- 213 拣行键是政策加两个发布时间，时点来自已有 `publish_date`。214 按政策。215 按区域、部门、方面。217 按对标对象和已勾字段。
- 力度分落在已有 `policy_intensity.intensity_score`，由已有 `run()` 写入。支持力度由 element 同步读，统计请求不调用 `run()`。
- 灌数单只出现在点名表。本单没有建库、没有插入、没有调用 `run()`。
- 定义任务，未跑业务 CI，未部署。未会签。不标 done。

## 架构合规自检

- ✅ 调用链：浏览器只打 `/display/v1/policy/**`。缺项表由 `gkxlumen-element` 只读。正文、区域和类别仍委托 `gkxlumen-topic-policy`。力度 Job 仍走已有异步任务管道。display 不直连库，不直连 Python。
- ✅ Java 不写算法。力度沿用已有 `polan.eval.intensity.run`。本单不改该函数。
- ✅ 不写 nGQL，不重开 GDF。
- ✅ D9：不新造 `metric_id`，不改 D4。无行不造 0。
- ✅ D16：四张新表只在 `gkxlumenx_gapfill`，行上带规定列。不写 ODS、DWD、ADS、供应方库。生产配置不读缺项库。
- ✅ D18：接口只读表，不直接返回 mock。216、218 不另建表。`ads.policy_intensity` 已有。
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
| diagram_id | `POL-L2-DS10-CMP-ARCH-SEQ` |
| 图 diff | 本数据叶不改图、不加边。读路径沿用架构第 5 节 |
| 会签态 | 未会签。源文件无 frontmatter，记 `draft`。不自填绿 |
| 说明 | 数据落点不替代该图。未会签通过 |

## 修改内容

- 新增 `sdd/l2/POL-L2-DS10-CMP-DATA.md`
- 新增本 handoff
