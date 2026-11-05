# POL-L2-DS12-EST-DATA-SIGNOFF-ARCH · 政策效果推演 · 效果预估 · 数据分册架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-EST-DATA`（2026-11-05）。本页不改这份分册，不改 `POL-L2-DS12-EST-ARCH`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS12-EST-ARCH` 第 9 节，以及第 5.1–5.3 节的行内容。`POL-L2-DS11-PLAN-DATA` 的 `is_mock` 列只作同款对照。这些文件本页都不改
- 范围：SRS 序号 232–234 的列。只写本会签。强度 ponytail off

## 结论

同意会签

分册只给库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_forecast` 定列。`row_kind` 只有未出台仿真、新出台预测、区域空间。235、236 只点到各自的库和表，不展开 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder` 的列。不灌文本解析。不写 ODS、DWD、ADS。空态是空。库与表分开写。`is_mock` 与 DS11 缺项表同款，多这一列不构成否决。

## 核对

| 项 | 分册 | 判定 |
|---|---|---|
| 只给定一张缺项表的列 | 第 1、2 节：唯一新表是库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_forecast`。232、233、234 同一张表，不另建。列清单不是可执行 SQL。建表与灌数归 `POL-L2-DS12-EST-GAPFILL-L01`，本单不执行 | 一致。与架构第 9 节「本叶组的表只有这一张」「字段级 DDL 由 EST-DATA 定」一致 |
| `row_kind` 闭集 | 第 2 节只有 `未出台仿真`、`新出台预测`、`区域空间`。写明没有第四个值。235、236 的行不写入本表 | 一致。与架构第 9 节三种种类一致 |
| 不展开 result / stakeholder 列 | 第 1 节末句：235 的列归 `POL-L2-DS12-SIM-DATA` 的库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_result`；236 归同一单的库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_stakeholder`。第 7 节写本文不写那两张表的列。正文没有这两张表的字段清单 | 一致。读路径仍指架构 §5.4/§5.5，列不在本分册展开 |
| 不灌文本解析 | 第 1、4、6、7、8 节：`ads.policy_text_parse` 的解析行不进入本表。`similar_basis_text` 是行内一句依据，不存放解析标题、摘要、标签或条款。不调 `parse/jobs`，不用解析结果顶替预测行 | 一致。与架构第 5.2、9 节「不另开解析通道」「不灌独立文本解析行」一致 |
| 不写 ODS / DWD / ADS | 第 1、8 节：不写 `gkxlumenx_ods`、`gkxlumenx_dwd`、`gkxlumenx_ads`，不写供应方库。`ads.policy_simulate` 留在中台读面，行不复制进本表 | 一致。与架构第 9 节库边界、D16 一致 |
| 空态是空 | 第 1、3、4、5、6、8 节：无行或条件对不上则该区空。查询不插入。不把空表写成 501。接口不直接返回写死的预测。真模型未注册时如何返回仍以架构稿为准，不落在本表 | 一致。与架构「无行则该区空」「查询请求不灌数」一致 |
| 库与表分开 | 第 1 节表头分列「库」「表」。全文写库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_forecast`。235、236 也是库、表分写，没有把库名和表名粘成一个标识 | 一致 |
| `is_mock` 同 DS11 缺项表 | 第 2 节：`is_mock` tinyint，非空，每行必须为 1，D4 仍是 mock。D16 行级列仍是 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`，外加这一列。`fill_method` 固定 `manual`，不设 `fill_model` | 一致。与 `POL-L2-DS11-PLAN-DATA` 缺项表同款。架构第 9 节未单列此列。多这一列不否决 |
| 行上指标与读链 | 三叶 `metric_id` 固定已有 `M_POLICY_SIMULATE`。不新注册，不改 D4。`gkxlumen-display` 不直连库。`gkxlumen-element` 按种类只读。Java 不生成方案、不按弹性现算、不插入行。浏览器只打 `/display/v1/policy/**`，三叶走 `POST /display/v1/policy/simulation/jobs` | 一致。与架构第 2、5.1–5.3、9 节一致 |

## 路径、表、sub_type

| 序号 | 公开路径 | 表 | sub_type |
|---|---|---|---|
| 232 | `POST /display/v1/policy/simulation/jobs` | 库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_forecast`，`row_kind=未出台仿真` | 无。不进 `PolicyAnalysisTypes`，不进 `JOB_SUB_TYPES`。同步读 |
| 233 | 同上 | 同库同表，`row_kind=新出台预测`。`metric_id` 用已有 `M_POLICY_SIMULATE` | 无。不调 `parse/jobs` |
| 234 | 同上 | 同库同表，`row_kind=区域空间`。`metric_id` 用已有 `M_POLICY_SIMULATE` | 无。服务端只回行 |

232–234 的结果跳是：浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element` → 库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_forecast`。不进入 `gkxlumen-topic-async-service`，不进入 Python `/internal/*`。

235、236 的列不在本表。本页不展开。

## 铁律

1. 本分册只定库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_forecast` 的列。不建库，不灌数。列清单不是可执行 SQL。
2. `row_kind` 只有未出台仿真、新出台预测、区域空间。
3. 不展开 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder` 的列。不灌文本解析。不写 ODS、DWD、ADS，不写供应方库。
4. 空态是空。查询不插入。不用 501 充当这三叶的功能。接口不直接返回写死的预测。
5. 库与表分开写。`is_mock=1` 与 DS11 缺项表同款。不因多这一列否决。
6. 不新造 `metric_id`，不改 D4。Java 不生成预测，不按弹性现算，不写 nGQL。展示不直连库，不直连 Python。

## 签收边界

本页不把任务标 done。签收仍由 human:淮政玮 做。同意会签不是签收。
