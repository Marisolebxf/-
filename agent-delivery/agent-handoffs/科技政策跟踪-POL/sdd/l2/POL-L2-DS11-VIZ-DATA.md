# POL-L2-DS11-VIZ-DATA · 政策分析评价 · 政策分析报告可视化呈现 · 数据落点

- 任务：`POL-L2-DS11-VIZ-DATA`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游架构：`POL-L2-DS11-VIZ-ARCH` 第 5、9 节。注册表该单状态为 done，note 写 `human:淮政玮` 签收。架构稿正文头仍写待签收。本单不改那份架构，不改图，不改它的状态句。

本叶只定政策分析评价二级「政策分析报告可视化呈现」的数据落点。SRS 序号 **219–222**。列级定义只定粒度和必要列。下面的列清单不是可执行 SQL，本单不建库、不灌数、不跑脚本。

上游只引用，不改写：`sdd/l2/POL-L2-DS11-VIZ-ARCH.md` 第 5、9 节及第 3 节闭集、`sdd/指标与501.md` 219–222、同目录 `POL-L2-DS11-READ-DATA.md` 里壳表只服务 224、225 的句子。不新造 `metric_id`，不改 D4。指标分册里 219、220、222 的 501、221 的跨项索引，本单不改字。

## 1. 范围

四叶都在政策分析评价的可视化区里完成。浏览器只打 `/display/v1/policy/**`。查询只读。查询请求不灌数。表里没有行就返回空。接口不直接返回写死的 mock。

| 序号 | 叶子 | 库 | 表 | 本单 |
|---|---|---|---|---|
| 219 | 多维指标趋势图 | `gkxlumenx_gapfill` | `gapfill_policy_eval_trend` | 本单定列。建表与灌数在灌数单 |
| 220 | 分区/群体对比分析图 | 同一库 | `gapfill_policy_eval_partition` | 本单定列。与 219 同一张灌数单 |
| 221 | 多维结构关联图 | 不建库表 | 第 7 项已有政策子图 | 不建表，不定点边列 |
| 222 | 报告模板定制与批量导出 | `gkxlumenx_gapfill` | `gapfill_policy_eval_template` | 本单定列。与 219、220 同一张灌数单 |

219、220、222 不读已有 ADS。`ads.policy_effect`、`ads.policy_metric_timeseries`、全景时序、全景分布都不进入这三张表的读面。221 不读 ADS，只消费第 7 项已有子图。

这三叶没有专属 `metric_id`。三张表上的 `metric_id` 留空。行是以后灌入的 mock，D4 仍是 `mock`。不把缺项表写成已上线。`GDF-POLICY-MOCK-GATE-L01` 与这三张表无关，本叶不改那道闸门。

本叶新建的表只有这三张，都在 `gkxlumenx_gapfill`，表名都以 `gapfill_` 开头。本单只定列，不建库，不插入。不写 ODS、DWD、ADS、供应方库。不写 `gapfill_policy_eval_shell`。那张壳表只服务 224、225。

`gkxlumen-display` 不直连库。219、220 由 `gkxlumen-element` 在 `jobs` 里只读各自的表，不建任务。222 由 `gkxlumen-element` 在 `shells` 里只读模板表。

## 2. 219 多维指标趋势图

库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_trend`。

一行是一个趋势点。一个点只落在一个切换维上：时间，或区域，或类别。同一指标要在两个维上各有位置时，写成两行。一行上有评估指标名，以及一个对照值。

`jobs` 只要趋势时，`gkxlumen-element` 只读这张表。按用户勾选的维读 `axis_kind`，按所选指标名读 `metric_name`。未勾选的维不读。条件对不上则图空，不在接口里补一段曲线，也不把查询转到 Python 现造一个点。重点和波动只标在读到的点上。本单不另建重点列、波动列，不另存一条指标。

下列是必要列。建表语句由灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01` 落地。本单不执行该单，也不在这里给出可执行脚本。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `axis_kind` | varchar(16) | 否 | 只有 `时间`、`区域`、`类别` |
| `axis_position` | varchar(256) | 否 | 该维上的一个位置。位置文本来自行本身。本单不另编词表 |
| `metric_name` | varchar(256) | 否 | 评估指标名。这是行上的名称，不是 `metric_id` |
| `compare_value` | decimal(18,4) | 否 | 一个对照值。不另建单位列，不另建第二条序列 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空。219 没有专属指标 |
| `gap_item` | varchar(128) | 否 | 固定 `219 多维指标趋势图` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间。由灌数单填写 |

同一 `axis_kind`、同一 `axis_position`、同一 `metric_name` 只应有一行。灌数单保证。本单不写唯一索引语句。

`fill_method` 固定 `manual`，因此不设 `fill_model`。

`metric_id` 留空。不允许为了填满该列，把 `M_POLICY_TIMESERIES`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT` 或任何新造标识抄到这张表上。

不设年份闭集，不迁 2020–2026 的序列，不迁五维雷达，不迁页内常量曲线。无行则图空，不造 0。D4 保持 mock。

## 3. 220 分区/群体对比分析图

库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_partition`。

一行是一个对象上的对照：地区、行业或目标群体中的一类，一个对象名称，一个对照数。资源投向写在同一行，可以空。柱状和热力读同一批行。不建第三张可视化表。图种不落列。

`jobs` 只要分区时，`gkxlumen-element` 只读这张表。未选的对象不读。图种不选时，柱状和热力都用这次按对象拣出的行。未选投向时，不按 `invest_direction` 过滤。选了投向时，只返回该列等于所选值的行。空投向对不上任何一个已选投向。对不上则该图空。不返回演示矩阵。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `object_kind` | varchar(16) | 否 | 只有 `地区`、`行业`、`目标群体`。不另收 `群体` 作为第四个值 |
| `object_name` | varchar(256) | 否 | 该对象的名称。名称来自行本身 |
| `compare_count` | decimal(18,4) | 否 | 一个对照数。不另建单位列。这不是新的效果指标 |
| `invest_direction` | varchar(256) | 是 | 资源投向。可空。本叶不编投向词表，只接受行上已有的值。空字符串不充当一种投向，灌数时留空 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空。220 没有专属指标 |
| `gap_item` | varchar(128) | 否 | 固定 `220 分区/群体对比分析图` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间。由灌数单填写 |

同一 `object_kind`、同一 `object_name`、同一 `invest_direction`（空与空视为同一）只应有一行。灌数单保证。本单不写唯一索引语句。

不设 `fill_model`。`metric_id` 留空。不把全景分布类指标或新的效果指标抄到这张表上。不迁演示城市名单，不迁资金、人才、平台、税收这四类页内常量。无行则图空，不造 0。D4 保持 mock。

## 4. 221 多维结构关联图

不建表，不加列，不建缺项表。本序号没有专属 `metric_id`。不挂 `M_POLICY_GRAPH_107_1`，不挂 `M_POLICY_RELATION_DEGREE`。

已有落库结果是第 7 项政策子图。政策子图任务 `E-E7-POLICY-M1-L02` 已完成。抽取脚本 `GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog。本单不重开它，不改它的状态，不写 nGQL，不定点边列。展示只消费该子图。子图读不到则弦线图和关系网都空，路径也空。挂接可空。

不把演示页的弦线矩阵和三条路径灌进 219、220、222 的任何一张表。不把共词网络写成新算法。不新开 `/display/v1/policy` 资源。

## 5. 222 报告模板定制与批量导出

库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_template`。

一行是一条模板选用：一个模板名，以及该行允许的一个汇报周期、一个分析维度、一个图表类型。同一模板允许多种组合时分成多行。不把多个周期、多个维度或多个图表类型用分隔符写进同一格。不把模板行拆进趋势表或分区表。趋势点和分区对照也不抄进这张表。

`GET /display/v1/policy/evaluation/shells` 的种类为模板选用时，`gkxlumen-element` 只读这张表。按模板名拣行。周期、维度、图表类型不齐则该次导出空。未勾选的图表类型不进该次导出。不选格式则只返回选用行，不生成文件。没有选用行时模板区空。不返回一套写死的模板。

导出要文件时，从这次读到的选用行生成 PDF 或 Excel。格式只有这两种，不落列。不写对象存储。不灌 PDF，不灌 Excel。操作日志不建表。没有真实导出则日志空。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `template_name` | varchar(256) | 否 | 模板名。不写模板正文 |
| `report_period` | varchar(64) | 否 | 该行允许的一个汇报周期。第 3 节没有周期词表。本单不把近 1 年、近 3 年、近 5 年收成闭集 |
| `analysis_dim` | varchar(16) | 否 | 只有 `时间`、`区域`、`类别`、`地区`、`行业`、`目标群体`。219 的三维和 220 的三类对象都保留。`区域` 与 `地区` 是两个值 |
| `chart_kind` | varchar(16) | 否 | 只有 `趋势`、`柱状`、`热力`、`弦线`、`关系网` |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空。222 没有专属指标 |
| `gap_item` | varchar(128) | 否 | 固定 `222 报告模板定制与批量导出` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间。由灌数单填写 |

同一 `template_name`、同一 `report_period`、同一 `analysis_dim`、同一 `chart_kind` 只应有一行。灌数单保证。本单不写唯一索引语句。

不设 `fill_model`。`metric_id` 留空。不新造导出指标。

不设模板正文、模板编号、文件地址、对象键、PDF、Excel、操作日志。不灌这些内容。不拿 224 的解读条目或 225 的多媒体条目充当模板行。不把模板选用写入 `gapfill_policy_eval_shell`。

`shells` 上的多媒体、互动意见、方案报告不在本表。本表为空时，不用模板正文把整条 `shells` 填满。无行则模板区空。D4 保持 mock。

## 6. 灌数单

灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01` 依赖本单和 `POL-L2-DS11-VIZ-ARCH`。执行人仍是 `data-agent`，监管仍是 `human:淮政玮`。本单只点名，不认领，不执行，不建库，不插入行，不改那张任务的注册字段。

该单当前仍是 `backlog`。注册完成定义仍只写两张表：

- 在 `gkxlumenx_gapfill` 建 `gapfill_policy_eval_trend`、`gapfill_policy_eval_partition`。不写 ODS、DWD、ADS 和供应方库
- 独立脚本灌入趋势点和分区对照数。接口只读表
- 221 不建表。不改 D4，不新造 `metric_id`

注册 note 已写明还要灌 `gapfill_policy_eval_template`，并以架构第 9 节为准。本分册把第三张表的列定下来。收窄后的灌数范围：

| 登记完成定义 | 本分册 |
|---|---|
| 建 `gapfill_policy_eval_trend` | 保留。列按第 2 节 |
| 建 `gapfill_policy_eval_partition` | 保留。列按第 3 节 |
| 未写 `gapfill_policy_eval_template` | 补上。同一张灌数单建第 5 节这张表。本单不改注册字段 |
| 灌趋势点和分区对照数 | 保留。趋势点按第 2 节，分区对照按第 3 节 |
| 未写模板选用行 | 补上。只灌第 5 节的选用行 |
| 221 不建表 | 保持 |
| 不改 D4，不新造 `metric_id` | 保持。三张表的 `metric_id` 都留空 |
| 不写 ODS、DWD、ADS、供应方库 | 保持。也不写 `gapfill_policy_eval_shell` |

不灌的内容：全景时序、效果分、五维雷达、写死曲线、全景分布、演示城市名单、新的效果指标、弦线矩阵、演示路径、新的图指标、PDF、Excel、假操作日志、两套演示模板、解读条目、多媒体条目。

查询请求不调用这张灌数单。空表返回空。

## 7. 跨项只写消费边界

| 序号或资源 | 边界 |
|---|---|
| `ads.policy_effect`、`M_POLICY_EFFECT_SCORE` | 效果分的需求来源在推演。219 不读这张表，不调用 `effect.run` |
| `ads.policy_metric_timeseries`、`M_POLICY_IMPLEMENTATION_EFFECT` | 不挂 219 |
| `M_POLICY_TIMESERIES`、全景分布类 STAT | 指标分册写明不借给 219、220。本单不改那句 |
| `gapfill_policy_eval_shell` | 只服务 224、225 的解读条目和多媒体条目。本叶不写这张表，不把模板选用、趋势点、分区对照写入它 |
| `POL-L2-DS11-READ-GAPFILL-L01` | 不承接 222。本叶不改那张灌数单 |
| `evaluation/counts` | 短板条数和机遇条数。不把趋势点或分区对照数写入那次响应 |
| `jobs` 上的焦点、摘要 | 异步键只有 `policy_focus_ads`、`policy_text_parse`。不读本叶三张表 |
| 序号 229、`gapfill_policy_eval_scheme` | 方案二级。不进本叶三张表 |
| 227–231 | 方案、参数模拟、实施路径、意见与归档。不读本叶三张表 |
| `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` | 不挂 221。本单不读图列 |
| `compare/jobs`、`report/jobs`、`benchmark-report` | 核增对比、核增研报、全景对标报告。不写入本叶三张表 |
| `E-E7-POLICY-M1-L06`、专题 `/graph`、`/v1/policy/graph` | 不是 221 的展示读法。展示只消费第 7 项已有子图 |
| 说明书第 11.2 节 | 模板选用仍可能写在解读壳表那一行。本单不改说明书。可执行落点以架构第 9 节和本分册为准 |

## 8. 明确不做

- 不写可执行 SQL，不建库，不灌数。
- 不重开 GDF，不写 nGQL，不加 ODS、DWD、ADS 表，不写供应方库。
- 不写 `gapfill_policy_eval_shell`。壳表只服务 224、225。
- 221 不建表。不灌弦线矩阵、演示路径、图指标。
- 不新造 `metric_id`。三张表的 `metric_id` 留空。不改 D4。不改指标分册里 219、220、222 的 501 和 221 的跨项索引。
- 不把缺项行写成已上线。不把 mock 行并入 ODS、DWD、ADS、供应方库。
- 不灌 PDF、Excel、假操作日志、解读条目、多媒体条目、两套演示模板。
- 不建日志缺项表，不写对象存储，不写对象键。
- 查询不插入。列清单不是可执行 SQL。
- 不改说明书、WBS、`指标与501.md`、解读分册、方案分册、架构稿、注册表里的灌数单。
- 不认领 `POL-L2-DS11-VIZ-GAPFILL-L01`。
- 不把本单标成 done 或 ready_to_sign。
