# 产业技术影响力（M_INNOV_POT_TECH_INFL）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POT_TECH_INFL.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POT_TECH_INFL.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POT_TECH_INFL_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_POT_TECH_INFL |
| 指标名称 | 产业技术影响力 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 产业发展潜力评估页「技术影响力评估」——产业技术影响力指标的分布与排名 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_POT_TECH_INFL.md` |

## 口径定义

口径要两个分量：专利被引（`cited_by_nums`）与同族规模（`other_Versions`）。实测被引表 20,515 行里只有 **475 件（0.0162%）** 能按 `patent_id` 回连 `dwd_patent` 的 2,939,895 行；同族字段在 3,000 行主键前缀样本里 **0 行非空**，`dwd_patent_family` 只有 20,593 行且**没有申请人字段**。两个分量都无法落到「产业」，故判**完全不支持**：本文件不产出任何产业分，只交付可复核的覆盖率证据与修复清单。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POT_TECH_INFL.md` §二（M_INNOV_POT_TECH_INFL.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_cited`
- `dwd_patent_family`
- `dwd_zh_author`
- `dwd_zh_paper_citation`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：口径要两个分量：专利被引（`cited_by_nums`）与同族规模（`other_Versions`）。实测被引表 20,515 行里只有 **475 件（0.0162%）** 能按 `patent_id` 回连 `dwd_patent` 的 2,939,895 行；同族字段在 3,000 行主键前缀样本里 **0 行非空**，`dwd_patent_family` 只有 20,593 行且**没有申请人字段**。两个分量都无法落到「产业」，故判**完全不支持**：本文件不产出任何产业分，只交付可复核的覆盖率证据与修复清单。
- **基期声明**：被引表无申请年字段且回连率 0.0162%，无法构造任何年度分母

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POT_TECH_INFL.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POT_TECH_INFL.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POT_TECH_INFL_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

