# POL-L2-DS11-VIZ-DATA · 政策分析评价 · 政策分析报告可视化呈现 · 数据落点

- 任务：`POL-L2-DS11-VIZ-DATA`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`（状态已是 `in_progress`，本单不改状态）
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 会签态：未会签。本叶不代签，不标 done
- 上游架构：`sdd/l2/POL-L2-DS11-VIZ-ARCH.md` 第 9 节（同稿第 3、5、8 节供拣行和空态）。本单只写数据落点，不改那份架构，不改图。

本叶只定政策分析评价二级「政策分析报告可视化呈现」的数据落点。SRS 序号 **219–222**。列级定义只定粒度和必要列。下面的列清单不是可执行 SQL，本单不建库、不灌数、不跑脚本。

上游只引用，不改写：架构第 9 节、说明书第 11.2 节「评价 · 可视化 219–221」那一行、`sdd/l2/POL-L2-DS11-READ-DATA.md` 第 5 节已定的壳表列。指标沿用已有登记。不新造 `metric_id`，不改 D4。

说明书第 11.2 节把 221 放在「不建表」，把趋势表和分区表交给 `POL-L2-DS11-VIZ-GAPFILL-L01`。本叶不改说明书。表名、要灌的内容和灌数单与该行以及架构第 9 节一致。列和拣行键写在这里。

## 1. 范围

四叶都在政策分析评价页的可视化区里完成。浏览器只打 `/display/v1/policy/**`。`gkxlumen-display` 不直连库，不直连 Python，不写算法，不写 nGQL。查询只读。查询请求不灌数。对不上行就返回空。接口不直接返回写死的 mock。

新建表只有库 `gkxlumenx_gapfill` 下这两张：

| 表 | 序号 | 灌数方 | 读取方 | 拣行键 |
|---|---|---|---|---|
| `gapfill_policy_eval_trend` | 219 | `POL-L2-DS11-VIZ-GAPFILL-L01` | `gkxlumen-element` | `switch_dim` 与 `metric_name` |
| `gapfill_policy_eval_partition` | 220 | 同一张灌数单 | `gkxlumen-element` | `object_kind`；投向有值时再加 `resource_direction` |

不写 ODS、DWD、ADS，不加已有 ADS 列，不写供应方库。不建第三张可视化表。不建日志表。不建模板表。

221 不建表。222 不建表。壳表 `gapfill_policy_eval_shell` 由解读二级建立，本叶不加列。

| 序号 | 叶子 | 库表 | 本单 |
|---|---|---|---|
| 219 | 多维指标趋势图 | `gkxlumenx_gapfill.gapfill_policy_eval_trend` | 本单定逻辑列。灌数单才建表 |
| 220 | 分区/群体对比分析图 | `gkxlumenx_gapfill.gapfill_policy_eval_partition` | 本单定逻辑列。同一张灌数单 |
| 221 | 多维结构关联图 | 无。第 7 项已有政策子图 | 不建表。无子图则空 |
| 222 | 报告模板定制与批量导出 | 已有 `gkxlumenx_gapfill.gapfill_policy_eval_shell` | 本叶不建。无模板选用行则空 |

这两张缺项表只服务功能验收。生产配置不读 `gkxlumenx_gapfill`。行上带 D16 规定列。缺项表有行也不把 D4 改成 live。`GDF-POLICY-MOCK-GATE-L01` 与这两张表无关，本叶不改那道闸门。

## 2. 已有 ADS 与已落库结果

219、220、222 的画面数不读 ODS、DWD、ADS。

| 序号 | 读什么 | 不读 |
|---|---|---|
| 219 | 只读 `gapfill_policy_eval_trend` | `ads.policy_effect` 上的效果分。全景时序 `M_POLICY_TIMESERIES`。五维雷达 |
| 220 | 只读 `gapfill_policy_eval_partition` | 全景的全国分布、类型分布、级别分布。不把对照数登记成新的效果指标 |
| 221 | 只消费第 7 项已有政策子图。`E-E7-POLICY-M1-L02` 已完成 | 不读 ADS。不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`。不读专题门面 `/graph`，不读算法中台 `/v1/policy/graph` |
| 222 | 只读已有壳表里的模板选用行 | 不读 ADS。不把 224 的解读正文或 225 的多媒体标题当成模板 |

`polan.eval.effect.run` 写入 `ads.policy_effect` 的效果分，需求来源不在 219。本叶不改 `run()`，不把效果分改挂到趋势图。221 的子图抽取脚本 `GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog。本叶不认领、不重开、不写 nGQL。子图读不到则该块空。

D4 保持 mock。无行则该图、该下拉或该模板区空，不造 0。

## 3. 219 多维指标趋势图

没有多维效能趋势模型。库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_trend`。一行是一个趋势点：时间、区域或类别上的一个位置，一个评估指标名，一个对照值。重点和波动标在这个点上，不另算一条指标，也不另起一行。

维和指标名只从本表的行里读出。表空则下拉空，图也空。不迁 2020–2026 的序列，不迁五维雷达，不迁全景时序，不迁效果分。

拣行键：`switch_dim` 与 `metric_name`。同一维、同一指标名下的多个 `dim_value` 一起返回，组成这一条序列。未勾选的维不读。条件对不上的行不返回。至少要有一维和一项指标名；少了则该块空，查询不补默认对象。

灌数时同一 `switch_dim`、`dim_value`、`metric_name` 只留一行。

灌数方：`POL-L2-DS11-VIZ-GAPFILL-L01`。读取方：`gkxlumen-element`，经 `POST /display/v1/policy/evaluation/jobs` 的趋势段。只要趋势时 `gkxlumen-display` 不建任务，不转发 `gkxlumen-topic-async-service`，不调 Python。display 不直连库。不写入 ODS、DWD、ADS、供应方库。

下列是逻辑列，不是可执行 DDL。建表由灌数单落地。本单不执行。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `switch_dim` | varchar(16) | 否 | 拣行键。`时间`、`区域`、`类别` 三者之一 |
| `dim_value` | varchar(128) | 否 | 该维上的一个位置。时间点、区域名或类别名。不另编词表 |
| `metric_name` | varchar(128) | 否 | 拣行键。评估指标名。只来自本表已有名称。不是 `metric_id`，不新注册 |
| `point_value` | decimal(18,4) | 否 | 该点的对照值。不是新指标 |
| `is_key_point` | tinyint | 否 | `1` 在该点标重点，`0` 不标。不是新指标 |
| `is_fluctuation` | tinyint | 否 | `1` 在该点标波动，`0` 不标。不是新指标 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空。219 没有已挂指标，不新注册。不填 `M_POLICY_TIMESERIES`，不填效果分 |
| `gap_item` | varchar(128) | 否 | 固定 `219 多维指标趋势图` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间 |

`fill_method` 固定 `manual`，因此不设 `fill_model`。不设曲线 JSON，不设文件列，不设雷达列。查询不插入行。

## 4. 220 分区/群体对比分析图

没有分区效果模型。库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_partition`。一行是一个对象上的对照：地区、行业或目标群体中的一个名称，一个对照数。资源投向要筛时，值写在同一行，不另造指标。

对象名和投向只从本表的行里读出。不迁演示城市名单，不迁资金、人才、平台、税收这四类页内常量，不迁全景分布。

拣行键：`object_kind`。请求带了资源投向时，再按 `resource_direction` 拣。图种不参与拣行，不落列。柱状和热力读同一批行。未选的对象不读。投向对不上则该图空。表无行则图空，不返回演示矩阵。

灌数时同一 `object_kind`、`object_name`、`resource_direction` 只留一行。`resource_direction` 为空的行彼此按空值算同一档。

灌数方：`POL-L2-DS11-VIZ-GAPFILL-L01`。读取方：`gkxlumen-element`，经同一条 `POST /display/v1/policy/evaluation/jobs` 的分区段。只要分区时同样不建任务。display 不直连库。不写入 ODS、DWD、ADS、供应方库。不建第三张可视化表。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `object_kind` | varchar(16) | 否 | 拣行键。`地区`、`行业`、`目标群体` 三者之一 |
| `object_name` | varchar(128) | 否 | 该对象上的名称。候选项只来自本列 |
| `compare_value` | decimal(18,4) | 否 | 对照数。不是新指标 |
| `resource_direction` | varchar(128) | 是 | 资源投向。可空。投向不在本叶编目，只接受本列已有的值。请求带了投向才用它拣行 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空。不新注册效果指标 |
| `gap_item` | varchar(128) | 否 | 固定 `220 分区/群体对比分析图` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间 |

`fill_method` 固定 `manual`，因此不设 `fill_model`。不设 `chart_type`。不设文件列。查询不插入行。

## 5. 221 多维结构关联图

不建表。不新开 `/display/v1/policy` 资源。不把弦线矩阵、三条演示路径或共词网络灌进缺项表。不新造图指标。

读取方：展示只消费第 7 项已有政策子图。`E-E7-POLICY-M1-L02` 已完成。挂接可空。`gkxlumen-display` 不把这次查看转成新的查图任务，不委托专题门面 `/graph`，不打开算法中台 `/v1/policy/graph`。Java 不写 nGQL。

灌数方：无。本叶没有灌数单。`GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog，本叶不认领、不重开。

拣行键：无表行。图种只有弦线图、关系网，两图用同一份子图，不分成两套数据，不落列。传导路径是这份子图上的路径查看。子图没有则两图都空，路径也空。不接受演示页上的节点 id 作为拣行键。

## 6. 222 报告模板定制与批量导出

不建表。不把模板行拆进 `gapfill_policy_eval_trend`。不把模板选用加进 `POL-L2-DS11-READ-GAPFILL-L01`。不另开一张模板灌数单。

壳表 `gkxlumenx_gapfill.gapfill_policy_eval_shell` 由解读二级建立。`sdd/l2/POL-L2-DS11-READ-DATA.md` 第 5 节已经把列定死：`entry_kind` 只有 `解读`、`多媒体`，并与 `gap_item` 成对写成 `224 分主题分指标互动解读`、`225 多媒体辅助解读`。该灌数单只灌这两类行。本叶不加第三种 `entry_kind`，不加列，不改那份解读分册。

读取方：`gkxlumen-element`，经 `GET /display/v1/policy/evaluation/shells`，只取模板选用行。

灌数方：无。

拣行键：模板选用。按这个键到壳表上拣行时，对不上 `entry_kind` 与 `gap_item` 的现有两对，因此没有选用行。无选用行则模板区空，模板名下拉也空。不用 224 的结论、应用建议或 225 的标题把模板区填上。222 这一段为空时，不得用模板正文把整条 `shells` 填满。224、225 仍按解读分册返回，本叶不改它们的拣行。

汇报周期、分析维度、图表类型、导出格式是这次请求的条件，不落壳表的列。模板必选；没有选用行时这些条件没有可绑定的行，该次导出空。周期、维度、图表类型不齐则该次导出空。格式只有 PDF、Excel。不选格式则只看选用行，不生成文件。要文件时，只从这次读到的选用行生成。当前没有选用行，因此不生成文件。文件字节不进 MySQL，不进对象存储。不写桶名和对象键。

操作日志不建缺项表，不灌假日志。没有真实导出记录则日志空。

不迁两套演示模板，不迁近 1 年、近 3 年、近 5 年，不收饼图和散点。核增 `report/jobs`（614–618）和全景 `benchmark-report` 不是这条。

## 7. 灌数单

只点名，本单不执行，不建库，不插入行。

| 灌数单 | 做什么 | 本单 |
|---|---|---|
| `POL-L2-DS11-VIZ-GAPFILL-L01` | 按第 3、4 节建 `gapfill_policy_eval_trend`、`gapfill_policy_eval_partition` 并灌 mock 行。执行人 `data-agent`，监管 `human:淮政玮`。依赖本架构和本数据叶 | 不执行。查询请求不调用它 |
| `POL-L2-DS11-READ-GAPFILL-L01` | 解读二级的壳表灌数。只灌 224、225 | 本叶不认领、不执行。不把模板选用加进这张单 |

219、220 的灌数方都是 `POL-L2-DS11-VIZ-GAPFILL-L01`，读取方都是 `gkxlumen-element`。221 的灌数方无。222 的灌数方无。空则空。

## 8. 跨项只写消费边界

| 序号或资源 | 边界 |
|---|---|
| `evaluation/counts` | 短板条数、机遇条数。本叶不读，也不把趋势点或分区对照数写进那次响应 |
| `jobs` 上的焦点、效能、摘要、实施路径 | 序号 223、226、229 和页上效能得分。不是趋势图，不进这两张缺项表 |
| 224、225 | 壳表的解读行和多媒体行。本叶不改列，不改灌数范围 |
| 227–231 | 方案。不读 `gapfill_policy_eval_scheme` |
| `M_POLICY_TIMESERIES`、全景分布 | 不借给 219、220 |
| `M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT` | 在 `ads.policy_effect`。不挂趋势图 |
| `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` | 不挂 221 |
| `compare/jobs`、`report/jobs`、`benchmark-report` | 核增对比、核增研报、全景对标报告。不是 222 |
| 第 7 项子图 | 221 只消费。不重做抽取，不重开 GDF，不写 nGQL |

`jobs` 上已有指标的模型段仍走异步管道。请求里若带了趋势或分区，这两段由 element 同步读第 3、4 节的表。模型段失败时，不清空已经读到的趋势和分区。只选趋势或分区时，不写任务行。某一块读失败，不清空同页已经返回的短板条数和机遇条数。

## 9. 明确不做

- 不写可执行 SQL，不建库，不灌数。
- 不重开 GDF，不写 nGQL。
- 新表只有第 1 节两张 `gkxlumenx_gapfill.gapfill_` 表：`gapfill_policy_eval_trend`、`gapfill_policy_eval_partition`。不写 ODS、DWD、ADS 新表，不加已有 ADS 列。
- 221 不建表。不灌弦线矩阵、演示路径、新的图指标。
- 222 不建表。不把模板选用加进 `POL-L2-DS11-READ-GAPFILL-L01`。不加壳表列。不灌 PDF、Excel、假操作日志、两套演示模板。
- 不新造 `metric_id`，不改 D4，不把缺项行写成已上线。不改指标分册里 219、220、222 的「无模型」判定。
- 不把缺项行写入 ODS、DWD、ADS、供应方库。
- 不在接口里直接返回写死的曲线、矩阵、弦线、模板或 PDF。
- 不改架构稿、说明书、WBS、`POL-L2-DS11-READ-DATA.md`、注册表。
- 不把本单标成 done。会签态记未会签。
