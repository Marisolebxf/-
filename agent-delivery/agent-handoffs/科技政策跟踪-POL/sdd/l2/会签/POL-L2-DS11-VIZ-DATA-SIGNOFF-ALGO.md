# POL-L2-DS11-VIZ-DATA 会签 · algorithm-agent

- 任务：`POL-L2-DS11-VIZ-DATA`
- 角色：agent:algorithm-agent（监管 human:淮政玮）
- 日期：2026-11-03
- 结论：**同意会签**

## 核对表（算法角色重点）

| # | 核对项 | 结果 | 证据 |
|---|---|---|---|
| 1 | 三张表不带可算公式 | ✅ | 第 2 节 `gapfill_policy_eval_trend` 只有 `compare_value`（一个对照值，无推导式）；第 3 节 `gapfill_policy_eval_partition` 只有 `compare_count`（写明「这不是新的效果指标」）；第 5 节 `gapfill_policy_eval_template` 只有选用行，无任何计算列。`fill_method` 三表均固定 `manual` 且不设 `fill_model`，即没有任何模型公式挂在这三张表上 |
| 2 | `metric_id` 列留空 | ✅ | 三张表 `metric_id` 均为可空列、约束「留空」，并写明不许把 `M_POLICY_TIMESERIES`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT`、全景分布或任何新造标识抄进该列；第 8 节「三张表的 metric_id 留空」 |
| 3 | `is_mock=1` | ✅ | 三张表 `is_mock` tinyint 非空，「每行必须为 1」；`compare_value`/`compare_count`/模板行全部落在 mock 行语义下 |
| 4 | 灌入行是 mock 不是真算法 | ✅ | 第 1 节「行是以后灌入的 mock，D4 仍是 mock，不把缺项表写成已上线」；灌数单独立（`POL-L2-DS11-VIZ-GAPFILL-L01`），查询请求不灌数；不写 ODS/DWD/ADS/供应方库，符合 D16 缺项表边界 |
| 5 | 对照 `effect.py` 无交叉污染 | ✅ | 只读核对 `polan/eval/effect.py` 的 `run()`：其写入目标是 `ads.policy_effect`（`scope_type='region_effect'`）与 `ads.policy_metric_timeseries`，均带 `calc_batch_id`/`ext.is_mock` 语义，与三张 `gapfill_` 表互不相干。分册第 7 节写明这两张 ADS 表不进三表读面、不调 `effect.run`，属实 |
| 6 | 无已注册模型被虚构进表结构 | ✅ | 对照 `policy_routes.py` 的 `_MODEL_TABLE`（八键）与 `polan/eval/` 目录：无趋势/分区/导出模型。三张表均不设 `fill_model`、不设公式列，没有把任何未注册算法写成像 `effect.py` 那样的实算链路 |
| 7 | 不灌的内容清单闭合 | ✅ | 第 6 节：全景时序、效果分、五维雷达、写死曲线、全景分布、演示城市名单、新的效果指标、弦线矩阵、演示路径、图指标、PDF、Excel、假日志、两套演示模板、解读条目、多媒体条目全部点名不灌；壳表 `gapfill_policy_eval_shell` 只服务 224/225 |
| 8 | 列清单不是可执行 SQL；不建库不灌数 | ✅ | 头部与第 8 节：本单不建库、不插行、不写唯一索引语句，建表与灌数归灌数单 |

## 算法侧补充说明

- 三张表的行结构（趋势点/对照数/模板选用）都是「灌入的静态 mock 行」，与 `effect.py` 里「实算 + 受控随机代理」的真实算法行不同类。分册没有把前者包装成后者，也没有反向把 `effect.py` 的输出改写进 `gapfill_` 表，算法侧无异议。
- `generated_at` 由灌数单填写、`gapfill_batch_id` 由灌数单生成，数据分册不越权生成，边界干净。

本页不把任务标 done，签收仍由 human:淮政玮 做。
