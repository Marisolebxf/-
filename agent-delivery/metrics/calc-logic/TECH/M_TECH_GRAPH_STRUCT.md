# 技术点网图结构（M_TECH_GRAPH_STRUCT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_GRAPH_STRUCT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_GRAPH_STRUCT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_GRAPH_STRUCT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_GRAPH_STRUCT |
| 指标名称 | 技术点网图结构 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术图谱（TOPIC-TECH-12 / DS-02-TECHGRAPH）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_GRAPH_STRUCT.md` |

## 口径定义

本件在 200 个 IPC4 技术域的共现骨干图上复算结构指标：**200 节点、2,643 边、密度 0.1328、平均度 26.43、最大度 73、4 个连通分量（最大 197）、平均聚类系数 0.5782、权重合计 1,085,258**。结构指标本身可以全量复算，但节点是「IPC4 域」而不是 Nebula 的「技术点实体」，图壳属性（层级、类型配色、布局坐标）不在本库，故按四档口径落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_GRAPH_STRUCT.md` §二（M_TECH_GRAPH_STRUCT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：本件在 200 个 IPC4 技术域的共现骨干图上复算结构指标：**200 节点、2,643 边、密度 0.1328、平均度 26.43、最大度 73、4 个连通分量（最大 197）、平均聚类系数 0.5782、权重合计 1,085,258**。结构指标本身可以全量复算，但节点是「IPC4 域」而不是 Nebula 的「技术点实体」，图壳属性（层级、类型配色、布局坐标）不在本库，故按四档口径落**部分支持**。
- **基期声明**：节点筛选用全期（2021—2026）聚合截面，2021—2024 在库；不设基期（used=[]、missing=[]），不做跨年比较。
- **复现实测耗时**：约 2.0 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_GRAPH_STRUCT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_GRAPH_STRUCT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_GRAPH_STRUCT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

