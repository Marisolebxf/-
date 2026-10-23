# 深圳科技发展指标看板（M_INNOV_KPI_BOARD_SZ）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KPI_BOARD_SZ.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KPI_BOARD_SZ.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KPI_BOARD_SZ_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_KPI_BOARD_SZ |
| 指标名称 | 深圳科技发展指标看板 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 创新评价 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技发展态势 · 深圳科技看板｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_KPI_BOARD_SZ.md` |

## 口径定义

专利、论文、机构、基金、政策五格有真实属地字段且量足，属「直接支持」；期刊无城市字段、学者属地覆盖 0.91%，属「部分」；会议无表、项目归属字段全空、主题表退化、载体唯一承载为单批模板数据，属「不支持」。三类叠加，整体判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KPI_BOARD_SZ.md` §二（M_INNOV_KPI_BOARD_SZ.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industrial_fund_basic_info`
- `dwd_industry_analysis_topics`
- `dwd_org_base_info`
- `dwd_policy_base`
- `dwd_research_institute_base_info`
- `dwd_scholar`
- `dwd_zh_journal`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：可算格均落在真实源表且有属地字段；不可算格是「字段/承载缺失」而非「算法难」，故整体判部分支持，不能宣称深圳看板已可整体交付。
- **基期声明**：由产物中实际出现的年度键反推：used=[2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。
- **复现实测耗时**：约 217.5 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KPI_BOARD_SZ.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KPI_BOARD_SZ.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KPI_BOARD_SZ_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

