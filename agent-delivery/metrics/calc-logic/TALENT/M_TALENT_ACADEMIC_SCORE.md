# M_TALENT_ACADEMIC_SCORE（M_TALENT_ACADEMIC_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_ACADEMIC_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_ACADEMIC_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_ACADEMIC_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_ACADEMIC_SCORE |
| 指标名称 | M_TALENT_ACADEMIC_SCORE |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才详情页「学术影响力分析」卡片（雷达 + 分档 + 池内位次） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_ACADEMIC_SCORE.md` |

## 口径定义

需求给的五维里，论文数、被引次数、H 指数三列在 `gkx.dwd_scholar` 上 **20,420 条有姓名记录 100% 非空**，可直接出分；期刊影响力维无任何分区/影响因子承载（`gkx.dwd_zh_journal` 2,796 行、`impact_score` 非空 **0**），学术合作广度维只有 `dwd_scholar_coauthor` 1,187,606 行的合著**数量**、没有期刊与机构维度——两维始终补不齐，故判**部分支持**，交付「三维学术力指数」而不是「五维学术力」。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_ACADEMIC_SCORE.md` §二（M_TALENT_ACADEMIC_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_scholar`
- `dwd_scholar_coauthor`
- `dwd_scholar_paper_relation`
- `dwd_scholar_papers`
- `dwd_scholar_research_direction`
- `dwd_scholar_talent_flag`
- `dwd_zh_journal`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：需求五维中三维（论文/被引/H）在 gkx.dwd_scholar 100% 非空、可全量打分；期刊影响力维无任何期刊分区/影响因子表（dwd_zh_journal.impact_score 2,796 行非空 0），学术合作广度维只有 dwd_scholar_coauthor 1,187,606 行的合著数量、无期刊/机构维度，两维始终无法补齐 → 部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 0.4 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_ACADEMIC_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_ACADEMIC_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_ACADEMIC_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

