# 预测分析（城市专利年度序列外推）（M_SYNTH_DS_21_GRAPH_ANALYSIS_006）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_21_GRAPH_ANALYSIS_006.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_21_GRAPH_ANALYSIS_006.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_21_GRAPH_ANALYSIS_006_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_DS_21_GRAPH_ANALYSIS_006 |
| 指标名称 | 预测分析（城市专利年度序列外推） |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_DS_21_GRAPH_ANALYSIS_006.md` |

## 口径定义

本指标对深圳、广州、东莞、惠州四市 2021—2024 年专利申请件数做外推，预测 2025—2027 年。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_21_GRAPH_ANALYSIS_006.md` §二（M_SYNTH_DS_21_GRAPH_ANALYSIS_006.py 零改语义复算）。

## 源表字段

源件未点名任何 dwd_/ads_/ods_ 物理表（纯派生/合成件，输入为兄弟件产物或快照）；依赖清单见源件 §〇/§三。

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四市 2021–2024 专利件数是全量面板实测值（合计 2,086,838 件），序列干净、口径唯一，预测链条可完整复现；但只有 4 个年度观测，ARIMA(1,1,0) 无法识别，回测只有 8 个一步预测点（4 城 × 2 原点），MAPE 的置信度很低；2025 年在城市维没有键（面板 2025 总量 440,401，为公开滞后截断），2026 为残年，都无法作为样本外验证。因此只能给趋势示意，不能作为阈值判定依据。
- **基期声明**：专利库 apdt_year 只有 2021–2026；2017–2020 一行都没有，不得按 0 摊入趋势拟合或分母。2025 在城市维无键（总量 440,401，公开滞后），2026 为残年（74,810），均不参与拟合，只作为预测目标年。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_21_GRAPH_ANALYSIS_006.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_21_GRAPH_ANALYSIS_006.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_21_GRAPH_ANALYSIS_006_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

