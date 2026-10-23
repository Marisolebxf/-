# 投融资总额（M_CHAIN_INVEST_TOTAL）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_INVEST_TOTAL.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_INVEST_TOTAL.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_INVEST_TOTAL_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_INVEST_TOTAL |
| 指标名称 | 投融资总额 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 / 深圳产业发展分析 / 投融资规模 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链详情页「投融资规模」卡、季度投融资趋势线 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2019, 2020, 2021, 2022, 2023, 2024, 2025] |
| 缺失年份 | [2026] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_INVEST_TOTAL.md` |

## 口径定义

真源 `chain_investment`（明细 + 汇总）在 gkx 的 280 张表里不存在；改源 `gkx.dwd_org_financing_info` 后，事件数、币种、金额文本、完成日期四列都有结构，但金额只填了 42.01%、链归属只覆盖 56.38%、币种不能相加——**结构与数据都只到「部分」**，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_INVEST_TOTAL.md` §二（M_CHAIN_INVEST_TOTAL.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_financing_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：事件数与单币种金额可算，但 65.6% 的事件无金额、43.6% 的事件挂不上链、三种币种不能相加，且增长率只在 CNY 子集内成立——按四档定义属「始终有部分维度不可得」。
- **基期声明**：2019—2025 为年度金额序列；2026 年表内有 253 起事件但只到 7 月，属残年，不计入分母、不参与同比；1990 年以前无事件。年度金额只对 CNY 单币种成立，USD/HKD 不折算。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_INVEST_TOTAL.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_INVEST_TOTAL.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_INVEST_TOTAL_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

