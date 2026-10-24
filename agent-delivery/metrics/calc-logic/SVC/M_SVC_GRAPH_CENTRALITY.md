# 节点度中心性（M_SVC_GRAPH_CENTRALITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_CENTRALITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_CENTRALITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_CENTRALITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_GRAPH_CENTRALITY |
| 指标名称 | 节点度中心性 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构图谱 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·服务机构图谱中心性榜单（SRS seq 133） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2026] |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_GRAPH_CENTRALITY.md` |

## 口径定义

度中心性的公式本身没有任何数据依赖，只要边集就位就能算；本件在 13,141 条资本边（投资 ∪ 机构股东，双端在池、无向去重）上实测出全池 DC 最大 0.0074515（深创投，度 329）、活跃子网口径最大 0.025496，分布与榜单完整可交付。但需求语义里的「服务关系边」（合作/交易/客户）在 gkx 无承载表，算出来的度是**资本度**而不是**服务度**，正式语义的服务网络度无源，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_CENTRALITY.md` §二（M_SVC_GRAPH_CENTRALITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_invest_info`
- `dwd_org_shareholder_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：代理边集（投资 + 机构股东，双端在池 13141 条）上度中心性可现算并已出榜单；但需求口径的「服务关系边」（合作/交易/客户）在 gkx 无承载表，正式语义的服务网络度无源，故落部分支持。
- **基期声明**：度是截面量（快照时点的存量关系），无年度序列；同一机构在不同年份的边会增减，但库内没有边的生效年份字段可拆年，故不做年度度序列、也不补任何年份为 0。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_CENTRALITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_CENTRALITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_CENTRALITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

