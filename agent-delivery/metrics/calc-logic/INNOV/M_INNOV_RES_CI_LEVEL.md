# 竞争情报等级（M_INNOV_RES_CI_LEVEL）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_RES_CI_LEVEL.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_RES_CI_LEVEL.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_RES_CI_LEVEL_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_RES_CI_LEVEL |
| 指标名称 | 竞争情报等级 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（创新技术 / RES-CI） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 · 科技发展态势 · 科技发展规划 · 研究领域分析 · 竞争情报等级 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_RES_CI_LEVEL.md` |

## 口径定义

66 对企业的 0—100 分、三档等级、12×12 矩阵均可复现，且与 `M_INNOV_RES_GRADE` 100% 同档；但分值只由 IPC4 Jaccard 决定，「竞争情报」在本库只能读作「技术分类重叠度」，不能读作市场竞争强度，故判**部分支持**。

## 计算逻辑说明

```text
{'score': 'overlap × 100', 'thresholds': {'t_high': 48.43, 't_low': 39.66, 'rule': 'score ≥ t_high → 高；t_low ≤ score < t_high → 中；否则 低'}}
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_RES_CI_LEVEL.md` §二（M_INNOV_RES_CI_LEVEL.py 零改语义复算）。

## 源表字段

源件未点名任何 dwd_/ads_/ods_ 物理表（纯派生/合成件，输入为兄弟件产物或快照）；依赖清单见源件 §〇/§三。

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：66 对企业的分值、三档等级与 12×12 矩阵均可复现，且与 RES_GRADE 100% 同档；但分值完全由 IPC4 集合 Jaccard 决定——学者维 0 对可用，论文主题、项目学科、市场重叠均未进入；「竞争情报」在本库只能读作「技术分类重叠度」，不能读作市场竞争强度。
- **基期声明**：IPC 集合为全期累计；专利表申请年只有 2021—2026（2017—2020 零行），故不产出年度竞争强度序列，只给截面矩阵。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_RES_CI_LEVEL.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_RES_CI_LEVEL.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_RES_CI_LEVEL_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

