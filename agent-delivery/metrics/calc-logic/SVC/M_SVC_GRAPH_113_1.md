# 服务机构实体关系抽取（M_SVC_GRAPH_113_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_113_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_113_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_113_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_GRAPH_113_1 |
| 指标名称 | 服务机构实体关系抽取 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构图谱 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·服务机构图谱关系视图（SRS seq 131/132） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2026] |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_GRAPH_113_1.md` |

## 口径定义

需规点名六类关系（服务类型、服务内容、服务范围、合作伙伴、客户、资本纽带），gkx 里**只有资本纽带一类有表**（投资 41,888 行触池、机构股东 372,205 行触池），其余五类没有任何承载表；子公司表虽在，但双端在池 0 条。已完成边集是 13,141 条无向去重边、覆盖 12,905 个节点（29.23%），图结构与度数分布都能算，但「服务关系网络」这个语义只落地了资本一维，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_113_1.md` §二（M_SVC_GRAPH_113_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_heis_info`
- `dwd_org_invest_info`
- `dwd_org_shareholder_info`
- `dwd_org_subsidiary_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：资本纽带边（投资 + 机构股东）双端在池 13141 条、覆盖 12905 个节点，可现转；但需求点名的服务类型/服务内容/服务范围/合作伙伴/客户五类语义边在 gkx 无承载表（子公司表双端在池 0 条），多元关系仅落地一类，故落部分支持。
- **基期声明**：关系抽取为截面件（边集为快照时点的存量关系），不做年度序列；投资金额字段存在但非本件合成输入，未按年折算。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_113_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_113_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_113_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

