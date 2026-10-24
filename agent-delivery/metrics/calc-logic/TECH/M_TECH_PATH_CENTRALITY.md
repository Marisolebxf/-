# 技术路径中心性（深圳 IPC4 技术点图五维中心性）（M_TECH_PATH_CENTRALITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_PATH_CENTRALITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_PATH_CENTRALITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_PATH_CENTRALITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_PATH_CENTRALITY |
| 指标名称 | 技术路径中心性（深圳 IPC4 技术点图五维中心性） |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术路径中心性（TOPIC-TECH-05 / DS-02-TECHPATH）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_PATH_CENTRALITY.md` |

## 口径定义

以**深圳**为唯一主体，把 238 个 IPC4 技术点作为节点、把「同一深圳申请人名下共现 ≥20 户且 Jaccard ≥0.05」作为边（1,464 条），在 226 点的巨连通块上算五维中心性。实测结果：度、强度、PageRank 三维可用，介数因阈值敏感降为**有条件可用**，调和接近中心性在巨块内 p95/p05 只有 1.99 倍、70.8% 的节点挤在 0.30—0.51 的窄带里，判**退化**。按四档口径落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_PATH_CENTRALITY.md` §二（M_TECH_PATH_CENTRALITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：以**深圳**为唯一主体，把 238 个 IPC4 技术点作为节点、把「同一深圳申请人名下共现 ≥20 户且 Jaccard ≥0.05」作为边（1,464 条），在 226 点的巨连通块上算五维中心性。实测结果：度、强度、PageRank 三维可用，介数因阈值敏感降为**有条件可用**，调和接近中心性在巨块内 p95/p05 只有 1.99 倍、70.8% 的节点挤在 0.30—0.51 的窄带里，判**退化**。按四档口径落**部分支持**。
- **基期声明**：图结构用 2021—2024 四年深圳件累计共现；2025/2026 不入图（2026 为残年）；库内 2017—2020 无专利行，不补零
- **复现实测耗时**：约 5.8 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_PATH_CENTRALITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_PATH_CENTRALITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_PATH_CENTRALITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

