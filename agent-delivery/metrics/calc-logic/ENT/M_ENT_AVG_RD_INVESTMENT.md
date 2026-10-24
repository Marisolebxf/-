# 平均研发投入（M_ENT_AVG_RD_INVESTMENT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_AVG_RD_INVESTMENT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_AVG_RD_INVESTMENT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_AVG_RD_INVESTMENT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_AVG_RD_INVESTMENT |
| 指标名称 | 平均研发投入 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／企业总览／企业整体概况 |
| 更新频率 | 年 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业概览·平均研发投入 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2025] |
| 缺失年份 | [2020, 2021, 2022, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_AVG_RD_INVESTMENT.md` |

## 口径定义

gkx 国内年报宽表的研发列 **`arch_development_am` 非空 0 行 / 90,926 行**（`development_employee`、`fixed_assets` 同为 0），按 calc-logic 口径算不出「全部法人平均研发投入」；唯一有数的是上市财务表 **645 家 FY2025**（研发费 > 0），合计 **153,500,926,172.53 元**、均值 **237,985,932.05 元**、中位 **67,217,167.37 元**，占底册 189,116 家的 **0.4632%**；其中 495 家能挂到 12 条未来产业链（76.7442%），链上样本占比最高的是集成电路（0.357499%），最低的是软件与信息服务（0.006864%）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_AVG_RD_INVESTMENT.md` §二（M_ENT_AVG_RD_INVESTMENT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_foreign_org_annual_financial_info`
- `dwd_org_annual_financial_info`
- `dwd_org_industry_tags`
- `dwd_org_stock_finance_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：gkx 国内年报宽表的研发列 **`arch_development_am` 非空 0 行 / 90,926 行**（`development_employee`、`fixed_assets` 同为 0），按 calc-logic 口径算不出「全部法人平均研发投入」；唯一有数的是上市财务表 **645 家 FY2025**（研发费 > 0），合计 **153,500,926,172.53 元**、均值 **237,985,932.05 元**、中位 **67,217,167.37 元**，占底册 189,116 家的 **0.4632%**；其中 495 家能挂到 12 条未来产业链（76.7442%），链上样本占比最高的是集成电路（0.357499%），最低的是软件与信息服务（0.006864%）。
- **基期声明**：「最近一个完整自然年」= 2025（上市财报表 occur_period=202512 的 743 行年报口径）。2026 只有一季报、残年，不进均值；2020—2024 未单年出均值——vintage 差异会让同一家企业在不同年份进不同的样本，跨年不具可比性，故只取 2025 一个锚年，其余年份显式列为未用

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_AVG_RD_INVESTMENT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_AVG_RD_INVESTMENT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_AVG_RD_INVESTMENT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

