# 专家学者影响力（M_INNOV_SCHOLAR_INFLUENCE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCHOLAR_INFLUENCE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCHOLAR_INFLUENCE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCHOLAR_INFLUENCE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_SCHOLAR_INFLUENCE |
| 指标名称 | 专家学者影响力 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技全域态势页「要素影响力」卡片与「专家 H 指数排行」联动视图 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_SCHOLAR_INFLUENCE.md` |

## 口径定义

三维口径（H 指数 / 被引数量 / 论文数量）在 `gkx.dwd_scholar` 上**三列全有、21,316 行全非空**（h 正值为 20,914 行、被引正值为 20,914 行、发文正值为 21,301 行），院士标签另有 20,030 行可挂；没有现成影响力结果面，但结构与当日数据量都已足够，脚本一次跑通并落 `_out.json`，故判**完全转换支持**。唯一需要披露的是供应方字段内部矛盾（719 行 `h_index > paper_nums`，占 3.37%）与院士标签 32 人未落在学者主表上，这两点均已在 §四列明，且不阻断三维合成。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCHOLAR_INFLUENCE.md` §二（M_INNOV_SCHOLAR_INFLUENCE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_scholar`
- `dwd_scholar_citation_by_year`
- `dwd_scholar_coauthor`
- `dwd_scholar_paper_relation`
- `dwd_scholar_papers`
- `dwd_scholar_research_direction`
- `dwd_scholar_talent_flag`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：三维口径（H 指数 / 被引数量 / 论文数量）在 `gkx.dwd_scholar` 上**三列全有、21,316 行全非空**（h 正值为 20,914 行、被引正值为 20,914 行、发文正值为 21,301 行），院士标签另有 20,030 行可挂；没有现成影响力结果面，但结构与当日数据量都已足够，脚本一次跑通并落 `_out.json`，故判**完全转换支持**。唯一需要披露的是供应方字段内部矛盾（719 行 `h_index > paper_nums`，占 3.37%）与院士标签 32 人未落在学者主表上，这两点均已在 §四列明，且不阻断三维合成。
- **基期声明**：本指标为截面排行，无年度分母需求

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCHOLAR_INFLUENCE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCHOLAR_INFLUENCE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCHOLAR_INFLUENCE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

