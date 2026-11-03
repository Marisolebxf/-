# POL-L2-DS11-VIZ-DATA-SIGNOFF-ARCH · 政策分析评价 · 政策分析报告可视化呈现 · 数据分册架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-VIZ-DATA`
- 监管：`human:淮政玮`
- 对照：已签收 `POL-L2-DS11-VIZ-ARCH`（2026-11-03 返工后第二轮四角色同意，注册表已签收）第 3、5、9 节。本页只核分册是否落在架构基准内，不重新设计，不改分册，不改架构稿，不改 task-registry，不改代码
- 范围：SRS 序号 219–222

## 结论

同意会签

分册只定 `gkxlumenx_gapfill` 里 trend、partition、template 三张 `gapfill_` 表的列，221 不建表，查询不灌数，不写 ODS/DWD/ADS/供应方库，不碰壳表；列闭集与架构第 3 节及接口分册逐值对上，`metric_id` 全部留空。

## 核对

| 项 | 分册写法 | 对架构判定 |
|---|---|---|
| 只建三张 `gkxlumenx_gapfill` 表 | 第 1 节范围表：219 `gapfill_policy_eval_trend`、220 `gapfill_policy_eval_partition`、222 `gapfill_policy_eval_template`，全部 `gkxlumenx_gapfill`、`gapfill_` 前缀。「本叶新建的表只有这三张」「本单只定列，不建库，不插入」 | 一致。表清单与架构第 9 节逐行对应，无第四张表。DDL 落地和灌数都归 `POL-L2-DS11-VIZ-GAPFILL-L01`，本单不执行 |
| 221 不建表 | 第 4 节：「不建表，不加列，不建缺项表。」只消费第 7 项已有子图，挂接可空，不写 nGQL，不定点边列，不重开 `GDF-POLICY-GRAPH-EXT-L01`。不把演示弦线矩阵和路径灌进任何一张表 | 一致。与架构 5.3 节及调用链 6.4 节相符 |
| 查询不灌数、接口不返回写死 mock | 第 1 节：「查询只读。查询请求不灌数。表里没有行就返回空。接口不直接返回写死的 mock。」第 6 节：「查询请求不调用这张灌数单。空表返回空。」 | 一致。灌数是独立脚本，不是请求处理，符合 D18 读表口径 |
| 不写 ODS/DWD/ADS/供应方库 | 第 1、6、8 节三处重申。第 7 节：`ads.policy_effect`、`ads.policy_metric_timeseries` 不读不写；缺项行不并入 ODS/DWD/ADS/供应方库 | 一致。符合 D16：缺项只在 `gkxlumenx_gapfill` 的 `gapfill_` 表 |
| 不碰壳表 | 第 1 节：「不写 `gapfill_policy_eval_shell`。那张壳表只服务 224、225。」第 5 节不把模板选用写入壳表；第 7 节壳表边界行；第 8 节重申 | 一致。与已签收解读稿的壳表收窄一致，模板行不拆进趋势表或分区表 |
| 列闭集对架构第 3 节 | trend：`axis_kind` 只有时间/区域/类别，`metric_name` 是行名不是 `metric_id`，不设年份闭集，不迁 2020–2026 序列与五维雷达。partition：`object_kind` 只有地区/行业/目标群体（不另收 `群体` 第四值），`invest_direction` 可空不编词表，图种不落列。template：`analysis_dim` 六值且「`区域` 与 `地区` 是两个值」，`chart_kind` 五值，`report_period` 不收三年闭集，不设模板正文/文件地址/对象键/日志列 | 一致。三表粒度均为一行一事实（一趋势点、一对象对照、一条模板选用组合），条件拣行语义与架构第 3 节「条件对不上行则图空」对上 |
| `metric_id` 留空、不改 D4 | 三张表 `metric_id` 列均为可空留空；「不允许为了填满该列，把 `M_POLICY_TIMESERIES`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT` 或任何新造标识抄到这张表上」；`is_mock` 每行 1；`GDF-POLICY-MOCK-GATE-L01` 不解开 | 一致。与指标分册零挂接互相咬合，D4 保持 mock，不把缺项写成已上线 |
| 灌数单收窄 | 第 6 节：注册完成定义只写两张表，note 已写明以架构第 9 节为准，本分册把第三张表的列定下来并补进灌数范围，同一张单覆盖三张表，不改注册字段、不认领、不执行 | 一致。与架构「这一张单覆盖 219、220、222 三张表。不灌 `gapfill_policy_eval_shell`」一致。不灌清单覆盖全景时序、效果分、演示城市名单、PDF/Excel、假操作日志、解读条目、多媒体条目、两套演示模板 |
| 上游状态差如实登记 | 头部：注册表架构单状态为 done、note 写 `human:淮政玮` 签收，架构稿正文头仍写待签收，「本单不改那份架构，不改图，不改它的状态句」 | 一致。状态差只登记不处理，以注册表为准，下游以已签收架构为基准，不构成偏差 |
| 读链 | 第 1 节：display 不直连库，219、220 由 element 在 `jobs` 里只读各自的表，222 由 element 在 `shells` 里只读模板表 | 一致。与架构第 2 节内部跳一致 |

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。同意会签不是签收。
