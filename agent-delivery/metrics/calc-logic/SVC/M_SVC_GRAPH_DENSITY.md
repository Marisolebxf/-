# 服务网络密度（M_SVC_GRAPH_DENSITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_DENSITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_DENSITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_DENSITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_GRAPH_DENSITY |
| 指标名称 | 服务网络密度 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构图谱 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·服务网络概览（SRS seq 133/134） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2026] |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_GRAPH_DENSITY.md` |

## 口径定义

密度公式 $D = 2|E|/(|N|(|N|-1))$ 只需边数与节点数，本件在 13,141 条资本边上算出全池密度 **1.348180e-05**、活跃子网密度 **1.578251e-04**，可能边 9.747e+08、实现占比 0.00134818%，计算链完整。但会签口径 **Q-SVCCHAIN-03 明确裁决「服务网络密度的边不算投资/股东」**，而正式的服务关系边在 gkx 无承载表，因此本件的数值只能以「资本纽带密度（代理）」身份披露，不能宣称正式服务网络密度——这是本件判 **部分支持** 的决定性理由。

## 计算逻辑说明

```text
D = 2|E| / (|N| * (|N| - 1))
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_DENSITY.md` §二（M_SVC_GRAPH_DENSITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_invest_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：代理密度可现转（全池 1.348e-05 / 活跃子网 1.578e-04），结构与计算链完整；但会签口径 Q-SVCCHAIN-03 明确「服务网络密度的边不算投资/股东」，正式服务关系边在 gkx 无承载表，始终有一维缺正式数据，故落部分支持。
- **基期声明**：密度是截面量（快照时点存量边），不做年度序列；库内边表无「关系生效年」字段，按年拆边会把存量关系误摊成流量，故不拆。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_DENSITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_DENSITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_DENSITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

