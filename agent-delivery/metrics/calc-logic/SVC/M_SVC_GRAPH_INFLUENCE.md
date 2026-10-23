# 生态影响力评分（M_SVC_GRAPH_INFLUENCE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_INFLUENCE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_INFLUENCE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_INFLUENCE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_GRAPH_INFLUENCE |
| 指标名称 | 生态影响力评分 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构图谱 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·生态影响力榜单（SRS seq 133/135） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2026] |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_GRAPH_INFLUENCE.md` |

## 口径定义

三中心性（度、介数、接近）在资本边集上全部可算：度用 Freeman 相对度、介数用 Brandes（巨型分量 7,040 节点取 1,000 个固定种子抽样、其余分量精确）、接近用调和中心性（scipy 无权最短路精确），三维 min-max 后等权合成 ×100，实测最高分 **96.30**（深创投）、中位 13.13、共 12,905 个机构有分。会签裁决 Q-SVCCHAIN-03 只约束「密度」不许用投资/股东边，未约束影响力评分。但**需求语义是「服务机构在服务生态中的影响力」，而边集只有资本纽带**（投资 + 机构股东），服务关系边在库内无承载表——按四档定义，主体可算、至少一个必需维只能用代理变量，落在「部分支持」，不是「完全转换支持」。评的是**资本纽带网络影响力**，这个主语必须始终带上（§2.6 与附录 G）。

## 计算逻辑说明

```text
Influence = 100/3 * (DC_hat + BC_hat + CC_hat)，各分量在全部有度节点上 min-max
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_INFLUENCE.md` §二（M_SVC_GRAPH_INFLUENCE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_invest_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三中心性在代理边集（投资 + 机构股东，双端在池 13141 条、12905 个有度节点）上全部可算，合成分与 Top10 已落盘；但需求语义是「服务机构在服务生态中的影响力」，服务关系边库内无承载表、只能用资本纽带代理，且介数为 1,000 种子抽样估计（SE≈3.2%）→ 主体可算、必需维为代理，判部分支持。
- **基期声明**：影响力是截面量（快照时点存量边上的结构位置），不做年度序列；库内边表无生效年字段，按年拆会把存量关系误摊成流量，故不拆、也不补 0。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_INFLUENCE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_INFLUENCE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_INFLUENCE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

