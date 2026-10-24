# 创新点价值评估（M_INNOV_POINT_VALUE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POINT_VALUE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POINT_VALUE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POINT_VALUE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_POINT_VALUE |
| 指标名称 | 创新点价值评估 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（创新机会） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 创新机会 → 机会点价值 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_POINT_VALUE.md` |

## 口径定义

候选词条的三维价值分：新颖性 1/(1+T−t0)、影响潜力（关联成果被引合计）、成熟度（授权专利/专利数）；同 point_type 内极值归一，缺测维重归一

> 一句话口径（源件 §0.3）：三个子维里只有一个（新颖性）在两类词条上都完整；影响潜力在专利侧**整维不可用**（`dwd_patent_cited` 20,515 行只有 467 行能按 `patent_id` 连上主表，2.28%），在论文侧只有 799 篇有时间轴；成熟度在专利侧可算，但测的是「已授权文献占比」而不是「申请→授权转化率」，论文侧没有授权概念。结构与量都够出分，但每个 point_type 实际只有 2 个维度可用、且维度组合不同，分数**不可跨类型比较**。判**部分支持**。本档位与 `code/M_INNOV_POINT_VALUE_out.json` 的 `support_judgment` 一致。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POINT_VALUE.md` §二（M_INNOV_POINT_VALUE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_patent_cited`
- `dwd_zh_journal`
- `dwd_zh_paper`
- `dwd_zh_paper_citation`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三个子维里只有一个（新颖性）在两类词条上都完整；影响潜力在专利侧**整维不可用**（`dwd_patent_cited` 20,515 行只有 467 行能按 `patent_id` 连上主表，2.28%），在论文侧只有 799 篇有时间轴；成熟度在专利侧可算，但测的是「已授权文献占比」而不是「申请→授权转化率」，论文侧没有授权概念。结构与量都够出分，但每个 point_type 实际只有 2 个维度可用、且维度组合不同，分数**不可跨类型比较**。判**部分支持**。本档位与 `code/M_INNOV_POINT_VALUE_out.json` 的 `support_judgment` 一致。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 3.7 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POINT_VALUE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POINT_VALUE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POINT_VALUE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

