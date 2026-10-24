# 项目（含课题）影响力（M_INNOV_PROJECT_INFLUENCE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PROJECT_INFLUENCE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PROJECT_INFLUENCE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PROJECT_INFLUENCE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PROJECT_INFLUENCE |
| 指标名称 | 项目（含课题）影响力 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | DS-01 科技全域态势 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 科技发展态势 → 科技全域态势 → 科创要素（项目详情页属性） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021] |
| 缺失年份 | [2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_PROJECT_INFLUENCE.md` |

## 口径定义

王惠口径的三维里，**金额维 100% 有值**（58,453 行全非空）、**结题完备维只有代理指标**（`final_report_abstract` 填充 81.09%，`completion_status` 整列为空）、**参与机构维实际不可算**（`participating_institution` 是单值依托单位，1,592 个取值里 58,423 行只有一个名字，只有 29 行含分隔符；`funded_institution` 整列为空）。三个维度里两个降级、一个退化，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PROJECT_INFLUENCE.md` §二（M_INNOV_PROJECT_INFLUENCE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_project`
- `dwd_patent`
- `dwd_zh_project`
- `dwd_zh_project_output`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：王惠口径的三维里，**金额维 100% 有值**（58,453 行全非空）、**结题完备维只有代理指标**（`final_report_abstract` 填充 81.09%，`completion_status` 整列为空）、**参与机构维实际不可算**（`participating_institution` 是单值依托单位，1,592 个取值里 58,423 行只有一个名字，只有 29 行含分隔符；`funded_institution` 整列为空）。三个维度里两个降级、一个退化，故判**部分支持**。
- **基期声明**：dwd_zh_project 的 approval_year 覆盖 1986—2023，但 2022 仅 58 条、2023 仅 6 条，2024—2026 无记录；任何「前 N 年均值 / CAGR」只能用 1986—2021 这段真实年份做分母，2022 起三年不得按 0 摊入。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PROJECT_INFLUENCE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PROJECT_INFLUENCE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PROJECT_INFLUENCE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

