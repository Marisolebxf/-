# 智能推荐（机构合作者推荐）（M_SYNTH_DS_21_GRAPH_ANALYSIS_008）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_21_GRAPH_ANALYSIS_008.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_21_GRAPH_ANALYSIS_008.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_21_GRAPH_ANALYSIS_008_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_DS_21_GRAPH_ANALYSIS_008 |
| 指标名称 | 智能推荐（机构合作者推荐） |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_DS_21_GRAPH_ANALYSIS_008.md` |

## 口径定义

本指标在真实机构合著网上做链路预测，回答「哪两个机构未来可能合作」。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_21_GRAPH_ANALYSIS_008.md` §二（M_SYNTH_DS_21_GRAPH_ANALYSIS_008.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent_applicants`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：图谱协同推荐链路已跑通并可离线评估：训练图 7742 节点 / 7736 边，2021 年后新增测试边 5801 条；PPR AUC=0.7666、Adamic-Adar AUC=0.5517、AA Precision@10=0.0205、PPR Precision@10=0.0258。但需求点名的『用户查询行为/兴趣偏好』在 gkx 中没有任何日志表，『文献/研究项目/技术方案』三类对象也没有对应的推荐边，无法做个性化排序与在线 A/B，只能交付机构/专家的图谱关系推荐，故判部分支持。
- **基期声明**：训练图用 ≤2020 的全部真实年份（1980—2020 逐年有论文，无补零）；测试边用 2021—2026 的新增共著对，2026 为残年但只作测试集的一小部分，不进分母。
- **复现实测耗时**：约 144.6 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_21_GRAPH_ANALYSIS_008.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_21_GRAPH_ANALYSIS_008.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_21_GRAPH_ANALYSIS_008_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

