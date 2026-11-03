# POL-L2-DS11-VIZ-DATA-SIGNOFF-DATA · 政策分析评价 · 政策分析报告可视化呈现 · 数据会签（DATA 分册）

- 角色：`agent:data-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-VIZ-DATA`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS11-VIZ-ARCH` 第 5、9 节；`POL-L2-DS11-READ-ARCH` 里壳表只服务 224、225 的句子；`sdd/指标与501.md` 219–222 行（只转述，不改）
- 范围：SRS 219–222 的库表、列级定义、灌数单归属核对
- 结论：**同意会签**

本页只核对 DATA 分册的列级定义与架构第 9 节是否一致、灌数单归属是否唯一。不改 DATA 分册，不改架构稿，不改注册表，不建库，不灌数，不跑脚本。

## 核对表

### 库表与前缀

| 口径 | DATA 分册原文落点 | 判定 |
|---|---|---|
| 三张表都在 `gkxlumenx_gapfill`，表名 `gapfill_` 前缀 | 第 1 节范围表：219 `gapfill_policy_eval_trend`、220 `gapfill_policy_eval_partition`、222 `gapfill_policy_eval_template`，库均为 `gkxlumenx_gapfill`。第 1 节末段「本叶新建的表只有这三张，都在 `gkxlumenx_gapfill`，表名都以 `gapfill_` 开头」 | 一致。符合 D16：gapfill 表不进 ODS/DWD/ADS/供应方库 |
| 221 不建表 | 第 1、4 节：不建库表，不定点边列，不建缺项表，只消费第 7 项已有子图 | 一致 |
| 不写壳表 | 第 1 节末段「不写 `gapfill_policy_eval_shell`。那张壳表只服务 224、225」。第 7 节跨项表同。与 READ-ARCH 第 7、8 节口径一致 | 一致 |
| 不写 ODS、DWD、ADS、供应方库 | 第 1、6、8 节多处写明 | 一致 |

### 219 `gapfill_policy_eval_trend` 列级定义

| 口径 | DATA 分册第 2 节 | 架构第 9 节 | 判定 |
|---|---|---|---|
| `axis_kind` 闭集只有 时间/区域/类别 | 「只有 `时间`、`区域`、`类别`」 | 一行是一个趋势点：时间、区域或类别 | 一致 |
| 一行一个维上位置 + 指标名 + 一个对照值 | `axis_position`、`metric_name`、`compare_value` | 含指标名 | 一致 |
| `metric_id` 留空 | 「留空。219 没有专属指标」，点名不抄 `M_POLICY_TIMESERIES` 等 | 不新造 `metric_id` | 一致 |
| `is_mock` 每行 1 | 「每行必须为 1」 | D4 保持 mock | 一致 |
| `fill_method` 固定 `manual`，不设 `fill_model` | 第 2 节末两段 | — | 一致 |

### 220 `gapfill_policy_eval_partition` 列级定义

| 口径 | DATA 分册第 3 节 | 架构第 9 节 | 判定 |
|---|---|---|---|
| `object_kind` 闭集只有 地区/行业/目标群体 | 「只有 `地区`、`行业`、`目标群体`。不另收 `群体`」 | 地区、行业或群体的对照数 | 一致 |
| 投向写在同一行、可空、不编词表 | `invest_direction` 可空，空串不充当投向 | 投向写在行里 | 一致 |
| `metric_id` 留空、`is_mock`=1、`fill_method`=`manual` | 同 219 口径 | 不新造 `metric_id` | 一致 |
| 不建第三张可视化表，图种不落列 | 第 3 节首段 | 不另建第三张 | 一致 |

### 222 `gapfill_policy_eval_template` 列级定义

| 口径 | DATA 分册第 5 节 | 架构第 9 节 | 判定 |
|---|---|---|---|
| 一行 = 模板名 + 一个汇报周期 + 一个分析维度 + 一个图表类型，多组合拆多行 | `template_name`、`report_period`、`analysis_dim`、`chart_kind`；「不把多个周期、多个维度或多个图表类型用分隔符写进同一格」 | 模板选用行：模板名，以及该行允许的汇报周期、分析维度、图表类型 | 一致 |
| 维度闭集合并 219 三维与 220 三类对象 | `analysis_dim` 只有 `时间/区域/类别/地区/行业/目标群体`，「`区域` 与 `地区` 是两个值」 | 维度只用 219 的三维和 220 的三类对象 | 一致 |
| 图表类型闭集 趋势/柱状/热力/弦线/关系网 | `chart_kind` 闭集 | 架构第 3 节同 | 一致 |
| `metric_id` 留空、`is_mock`=1、`fill_method`=`manual` | 同 219 口径 | 不新造 `metric_id` | 一致 |
| 不落模板正文/文件地址/对象键/日志列 | 第 5 节「不设模板正文、模板编号、文件地址、对象键、PDF、Excel、操作日志」 | 不灌 PDF、Excel、假操作日志 | 一致 |

### 灌数单归属

| 口径 | DATA 分册 | 架构第 9 节 | 判定 |
|---|---|---|---|
| 唯一灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01`，同一张单覆盖三张表 | 第 6 节点名该单，收窄表把第三张表补上，「同一张灌数单建第 5 节这张表」 | 末段「这一张单覆盖 219、220、222 三张表」 | 一致 |
| 221 不进灌数单 | 第 6 节收窄表「221 不建表」保持 | 不建表。无子图则空 | 一致 |
| 不灌清单 | 第 6 节末段逐项列出不灌内容（全景时序、效果分、五维雷达、写死曲线、全景分布、演示城市名单、新的效果指标、弦线矩阵、演示路径、新的图指标、PDF、Excel、假操作日志、两套演示模板、解读条目、多媒体条目） | 第 9 节不灌列 | 一致 |
| 查询请求不灌数、空表返回空 | 第 6 节末段 | 查询请求不灌数 | 一致 |

### 观察（不构成不同意）

| 观察 | 说明 |
|---|---|
| 灌数单登记 DoD 只写两张表 | `POL-L2-DS11-VIZ-GAPFILL-L01` 注册完成定义正文只写 `gapfill_policy_eval_trend`、`gapfill_policy_eval_partition`，未写 `gapfill_policy_eval_template`。架构第 9 节已写明一张单覆盖三张表，DATA 分册第 6 节收窄表也已补上第三张。执行该灌数单时以架构第 9 节为准，本页不改注册，记为观察 |

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。
