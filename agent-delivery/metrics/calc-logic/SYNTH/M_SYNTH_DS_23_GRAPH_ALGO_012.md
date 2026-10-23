# 社群结构自动识别（M_SYNTH_DS_23_GRAPH_ALGO_012）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_23_GRAPH_ALGO_012.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_23_GRAPH_ALGO_012.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_23_GRAPH_ALGO_012_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_DS_23_GRAPH_ALGO_012 |
| 指标名称 | 社群结构自动识别 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合／知识图谱算法 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 图谱页「社群发现」按钮、社群着色、社群列表与下钻 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_DS_23_GRAPH_ALGO_012.md` |

## 口径定义

社群识别不需要任何外挂业务字段，只需要边表：有边就能划分。gkx 里三张图表都不存在，但边可以从论文表重建，量也够；算法在 15,223 节点上是秒级的。所以判**完全转换支持**，同时把「社群只读作学术共著社群」「标号只在本快照内有效」写成硬边界。

## 计算逻辑说明

```text
mod = 1/(2m) * sum_uv [A_uv - k_u*k_v/(2m)] * delta(c_u,c_v)，Louvain 贪心最大化 + 聚合迭代
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_23_GRAPH_ALGO_012.md` §二（M_SYNTH_DS_23_GRAPH_ALGO_012.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_scholar_coauthor`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：社群识别不需要任何外挂业务字段，只需要边表；边表由 dwd_zh_paper.author_info_list 重建。在 15,223 节点 / 36,965 边上一轮 Louvain 得 60 个社群、模块度 0.755103，零模型 z=158.926，且与已归档的 011（60 个社群 / 0.755103）复算一致，说明结果可重复、不是随机划分。算法、数据、复算三者齐备，故判完全转换支持。
- **基期声明**：截面图口径：不按年切分、不做年度除法。建图层 `_collab_graph21.build()` 的 from_year/upto_year 默认 None，**未按年过滤**，图中 100900 篇论文覆盖 1980—2026 共 47 个年份（逐年篇数见本件 `paper_year_dist`），其中 2021—2024 占 51.65%。已归档的 M_SYNTH_DS_23_GRAPH_ALGO_011 把 `base_years_used` 写成 [2021,2022,2023,2024]，与建图代码行为不符；本批按实际年份声明，并在 §二 披露该口径差（图本身与 011 一致：20,436 节点 / 38,208 边）。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_23_GRAPH_ALGO_012.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_23_GRAPH_ALGO_012.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_23_GRAPH_ALGO_012_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

