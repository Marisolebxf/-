# 科技人才流动（产业界↔学术界）（M_INNOV_PLAN_TALENT_FLOW）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_TALENT_FLOW.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_TALENT_FLOW.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_TALENT_FLOW_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PLAN_TALENT_FLOW |
| 指标名称 | 科技人才流动（产业界↔学术界） |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技发展规划页「人才流动」卡片（学界→产业 / 产业→学界双序列 + 预警灯） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024] |
| 缺失年份 | [2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_PLAN_TALENT_FLOW.md` |

## 口径定义

方向维（学界→产业、产业→学界）与时间维都能出数：核心技术人才池 6,580 人（院士 112 人 + `h_index ≥ 池内 P70 = 24`），在有 ≥2 段经历的 12,427 人里按相邻两段性质变化识别跨界，得到 **82 次核心人才跨界事件**（学界→产业 31 次、产业→学界 51 次），全池口径为 1,681 次；但**空间维不可用**：57,117 段经历的机构名只有 456 条（0.8%）能对上工商底册，高校、科研院所、海外机构根本不在底册里，另有 8,827 段（15.45%）机构名无法判定性质，按口径第四步须整段跳过。三向里缺一向，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_TALENT_FLOW.md` §二（M_INNOV_PLAN_TALENT_FLOW.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_university_org_info`
- `dwd_org_base_info`
- `dwd_research_institute_base_info`
- `dwd_scholar`
- `dwd_scholar_talent_flag`
- `dwd_scholar_work_experience`
- `dwd_zh_author`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：方向维（学界→产业、产业→学界）与时间维都能出数：核心技术人才池 6,580 人（院士 112 人 + `h_index ≥ 池内 P70 = 24`），在有 ≥2 段经历的 12,427 人里按相邻两段性质变化识别跨界，得到 **82 次核心人才跨界事件**（学界→产业 31 次、产业→学界 51 次），全池口径为 1,681 次；但**空间维不可用**：57,117 段经历的机构名只有 456 条（0.8%）能对上工商底册，高校、科研院所、海外机构根本不在底册里，另有 8,827 段（15.45%）机构名无法判定性质，按口径第四步须整段跳过。三向里缺一向，故判**部分支持**。
- **基期声明**：burst 以 2024 为 T：近窗 2022—2024、基线 2017—2021；2025 只有 9 次事件、2026 尚未成段，均不进分母

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_TALENT_FLOW.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_TALENT_FLOW.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_TALENT_FLOW_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

