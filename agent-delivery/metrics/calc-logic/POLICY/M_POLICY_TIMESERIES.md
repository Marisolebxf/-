# 政策时序指标（M_POLICY_TIMESERIES）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_TIMESERIES.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TIMESERIES.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TIMESERIES_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_TIMESERIES |
| 指标名称 | 政策时序指标 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统「政策时序分析」趋势图、政策追踪页的年度柱状与同比标注 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2015, 2016, 2017, 2018, 2019, 2020, 2021] |
| 缺失年份 | [2022, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_TIMESERIES.md` |

## 口径定义

时序的**历史段**（2015-01—2022-08）结构、数据、月份覆盖三者齐备，可以逐月复算；**当前段**（2022-09 之后）库内没有记录。一个只有历史段、没有当前段的「时序指标」可以发布历史趋势，但不能承担需求里「趋势监测」的用途，因此判**部分支持**而不是「完全转换支持」。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_TIMESERIES.md` §二（M_POLICY_TIMESERIES.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：时序的**历史段**（2015-01—2022-08）结构、数据、月份覆盖三者齐备，可以逐月复算；**当前段**（2022-09 之后）库内没有记录。一个只有历史段、没有当前段的「时序指标」可以发布历史趋势，但不能承担需求里「趋势监测」的用途，因此判**部分支持**而不是「完全转换支持」。
- **基期声明**：同比与年化只取 2015—2021 七个完整年（每年 12 个月都有记录）。2022 库内只有 1—8 月记录（9、11、12 月空），按不完整年排除，不入任何分母；2023 全年 0 行、2024 仅 1 行（2024-02-18），是采集断档，不按 0 摊入均值或趋势；2025—2026 未入库。故本件不产出 2022 年以后的同比与年化。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_TIMESERIES.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TIMESERIES.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TIMESERIES_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

