# 共性信息趋势查询（M_COMMON_INFO_TREND_QUERY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-COMMON-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_COMMON_INFO_TREND_QUERY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_COMMON_INFO_TREND_QUERY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_COMMON_INFO_TREND_QUERY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_COMMON_INFO_TREND_QUERY |
| 指标名称 | 共性信息趋势查询 |
| 所属域 | COMMON（跨要素查询） |
| 一级模块 | 产业服务／产业情报／信息热度 |
| 更新频率 | 建议日更 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链情报页「信息热度趋势」折线图 + 月份钻取｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2025, 2026] |
| 缺失年份 | [2018, 2019, 2020, 2021, 2022, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/COMMON/M_COMMON_INFO_TREND_QUERY.md` |

## 口径定义

108,052 条链标签新闻可出 18 个月（2025-02 至 2026-07）逐链月度序列与环比，但只有两年、出不了同比，判部分支持。

## 计算逻辑说明

```text
series(chain, month) = COUNT(DISTINCT news) WHERE chain_code ∈ industry_code；环比 = 本月/上月-1；同比需同月两年齐全
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_COMMON_INFO_TREND_QUERY.md` §二（M_COMMON_INFO_TREND_QUERY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_industry_chain_news_info`
- `dwd_news_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：enterprise_news_stat 结果面不存在，但趋势查询的原料齐全且是真数据：108,052 条带链标签的新闻、18 个月、206 个来源，逐月去重计数即可回答「某链信息量怎么走」。不能判完全转换支持的原因是时间窗只有 2025—2026：18 个月够看月度起伏与环比，但不够同比，也看不到 2018—2024 的长趋势（长窗口旁证表只有 20,000 行且无链标签）。故判部分支持。
- **基期声明**：链标签新闻只有 2025—2026 两年（2026 截至 5 月），2018—2024 在链标签表里一行都没有——不是补 0，而是该表根本没有这些年份。dwd_news_base 有 2018-06 起的长窗口，但无链标签，只能做总量旁证，不能补链级序列。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_COMMON_INFO_TREND_QUERY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_COMMON_INFO_TREND_QUERY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_COMMON_INFO_TREND_QUERY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

