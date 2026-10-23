# 机会因素分析（M_INNOV_DS_05_GBA_ANALYSIS_005）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_05_GBA_ANALYSIS_005.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_05_GBA_ANALYSIS_005.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_05_GBA_ANALYSIS_005_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_05_GBA_ANALYSIS_005 |
| 指标名称 | 机会因素分析 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技创新 / 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统·科技发展态势·湾区创新监测·创新能力分析（SWOT）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_05_GBA_ANALYSIS_005.md` |

## 口径定义

三个机会探测维中，政策窗口可独立复算（四城全部未达 1.5）、新兴技术可产出计数但方法存在「base=0 即突现」的判定缺陷、外溢合作因 `applicants` 覆盖 0.99% 完全缺测 → 三维仅一维可消费，**部分支持**，与 `code/M_INNOV_DS_05_GBA_ANALYSIS_005_out.json` 的 `support_judgment` 一致。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_05_GBA_ANALYSIS_005.md` §二（M_INNOV_DS_05_GBA_ANALYSIS_005.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_base_info`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_applicants`
- `dwd_policy_base`
- `dwd_research_institute_base_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三个机会探测维中，政策窗口可独立复算（四城全部未达 1.5）、新兴技术可产出计数但方法存在「base=0 即突现」的判定缺陷、外溢合作因 `applicants` 覆盖 0.99% 完全缺测 → 三维仅一维可消费，**部分支持**，与 `code/M_INNOV_DS_05_GBA_ANALYSIS_005_out.json` 的 `support_judgment` 一致。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_05_GBA_ANALYSIS_005.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_05_GBA_ANALYSIS_005.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_05_GBA_ANALYSIS_005_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

