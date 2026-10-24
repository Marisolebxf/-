# 全球创新实时看板指标（M_INNOV_KPI_BOARD）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KPI_BOARD.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KPI_BOARD.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KPI_BOARD_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_KPI_BOARD |
| 指标名称 | 全球创新实时看板指标 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 创新分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 全球创新实时看板首页、领导驾驶舱、专题汇报首屏 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_KPI_BOARD.md` |

## 口径定义

看板要回答的是「一眼看到创新全局」。它不需要新算一个指标，只需要把已经验收过的兄弟件读数按固定格子摆好。因此本件的核心风险不是算法，而是**来源纪律**：只要有一格是自己估的、或是从暂存区半成品抄的，整块看板就失去可追溯性。gkx 没有看板结果面，但 7 份兄弟件已经覆盖专利、论文、经费、主体四类，14 格可以逐格指到「件 ID + 键路径」；剩下 2 格事件类，事件面本身缺源（`dwd_event` 仅 20 行单一展会系列），同类指标件交的是代理读数与负证据，本件宁可留白也不填代理。有整类缺口，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KPI_BOARD.md` §二（M_INNOV_KPI_BOARD.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_event`
- `dwd_indicator`
- `dwd_innovation_event`
- `dwd_kpi`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：看板 16 格中 14 格能从正式区兄弟件读到已归档读数（专利/论文/经费/主体四类），2 格（事件条数、事件关注度）因事件面缺源置 null——不是缺件，是缺数据。本件不新造任何口径，也不把暂存区半成品当来源；因此整体判部分支持，而不是完全转换支持。
- **基期声明**：看板主窗取 2021—2024，与专利/研发四件同窗；2017—2020 专利表零行，不按 0 摊入。论文 2024 为入库批次峰（32,379 篇），本板只展示 2023 截面，不把 2024 当趋势。投资金额格取 2024 年；其余截面格（高企、基金、技术域）不参与年度序列。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KPI_BOARD.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KPI_BOARD.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KPI_BOARD_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

