# 市场热度评级（M_SVC_ORG_MARKET_HEAT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_MARKET_HEAT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_MARKET_HEAT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_MARKET_HEAT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_ORG_MARKET_HEAT |
| 指标名称 | 市场热度评级 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（新增服务机构动态的派生评级） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业服务链分析·新增动态·热度标签 / 算法库·服务机构基础指标模型（序号 101） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022] |
| 缺失年份 | [2023, 2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_ORG_MARKET_HEAT.md` |

## 口径定义

热度评级 = 新增序列的**相对斜率**（OLS 斜率 / 均值）与**变异系数**（std / mean）按王惠阈值分档。本件用 2013—2022 十个完整年算出斜率 −305.34 家/年、相对斜率 −14.63%、CV 46.07%，落「下行期」。但 2023—2025 成立年右截断（218/66/12 家），评级窗口只能止于 2022，「当前热度」实为「截至 2022 的历史判断」，故落 **部分支持**。本件与 `M_SVC_ORG_TOTAL`、`M_SVC_NEW_CNT`、`M_SVC_ORG_NEW_COUNT` 等九件同池（44,153 家）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_MARKET_HEAT.md` §二（M_SVC_ORG_MARKET_HEAT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：2013—2022 十个完整年可算 OLS 斜率（-305.34 家/年，相对 -14.63%）与 CV（46.07%），按王惠表落「下行期」；但 2023—2025 成立年右截断（218/66/12 家），评级窗口止于 2022，「当前热度」只能作历史判断，不能当 2026 年现状
- **基期声明**：回归窗口 2013—2022 十个完整年；2023—2025 成立年右截断，按缺失处理、不进分母；2026 无行。对照窗口 2016—2025 仅用于说明右截断对斜率的放大效应，不作评级

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_MARKET_HEAT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_MARKET_HEAT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_MARKET_HEAT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

