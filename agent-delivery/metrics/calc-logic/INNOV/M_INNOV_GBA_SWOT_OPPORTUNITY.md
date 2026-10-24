# 湾区创新能力机会因素（M_INNOV_GBA_SWOT_OPPORTUNITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_SWOT_OPPORTUNITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SWOT_OPPORTUNITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SWOT_OPPORTUNITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_SWOT_OPPORTUNITY |
| 指标名称 | 湾区创新能力机会因素 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 粤港澳大湾区创新指标数据 GIS（指标勾选）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_GBA_SWOT_OPPORTUNITY.md` |

## 口径定义

王惠口径的三维里，**D1 政策窗口在源侧已停采**（2023 年起全国 0 条）、**D3 跨城联合专利在本库不可识别**（无共申请人列，只能换论文合著）、**D2 用增长比替代 burst**（只有四年序列）；两个可评维度出得出有区分度的分，但机会来源缺了最直接的「政策」一维 → **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_SWOT_OPPORTUNITY.md` §二（M_INNOV_GBA_SWOT_OPPORTUNITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：王惠口径的三维里，**D1 政策窗口在源侧已停采**（2023 年起全国 0 条）、**D3 跨城联合专利在本库不可识别**（无共申请人列，只能换论文合著）、**D2 用增长比替代 burst**（只有四年序列）；两个可评维度出得出有区分度的分，但机会来源缺了最直接的「政策」一维 → **部分支持**。
- **基期声明**：由产物中实际出现的年度键反推：used=[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。
- **复现实测耗时**：约 0.39 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_SWOT_OPPORTUNITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SWOT_OPPORTUNITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SWOT_OPPORTUNITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

