# 社群属性与特征分析（M_SYNTH_DS_23_GRAPH_ALGO_013）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_23_GRAPH_ALGO_013.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_23_GRAPH_ALGO_013.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_23_GRAPH_ALGO_013_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_DS_23_GRAPH_ALGO_013 |
| 指标名称 | 社群属性与特征分析 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合图谱 / 社群分析 |
| 更新频率 | 未定义 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 综合图谱 → 社群属性面板（社群画像卡 + 跨社群联系） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_DS_23_GRAPH_ALGO_013.md` |

## 口径定义

「社群属性与特征分析」要在社群划分之上回答「每个社群是谁、做什么、和谁来往」。划分本身完全可算（共著图 + Louvain，模块度 0.755103）；但「做什么」依赖主题词表（只覆盖 0.7919% 论文）、「是谁」依赖机构底册（精确匹配 11.4038%），两样都薄。所以结果拆成两层：**拓扑属性（规模、密度、电导、跨社群权重）可直接交付**，**语义属性（主题、类型、城市）只能标为线索**。判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_23_GRAPH_ALGO_013.md` §二（M_SYNTH_DS_23_GRAPH_ALGO_013.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_zh_paper`
- `dwd_zh_paper_classification`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：「社群属性与特征分析」要在社群划分之上回答「每个社群是谁、做什么、和谁来往」。划分本身完全可算（共著图 + Louvain，模块度 0.755103）；但「做什么」依赖主题词表（只覆盖 0.7919% 论文）、「是谁」依赖机构底册（精确匹配 11.4038%），两样都薄。所以结果拆成两层：**拓扑属性（规模、密度、电导、跨社群权重）可直接交付**，**语义属性（主题、类型、城市）只能标为线索**。判**部分支持**。
- **基期声明**：截面图件：建图用全部 100,900 篇论文（1980—2026），不按年切分，不做年度除法。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_23_GRAPH_ALGO_013.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_23_GRAPH_ALGO_013.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_23_GRAPH_ALGO_013_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

