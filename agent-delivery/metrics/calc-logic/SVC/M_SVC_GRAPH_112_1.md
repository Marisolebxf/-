# 服务机构实体识别构建（M_SVC_GRAPH_112_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_112_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_112_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_112_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_GRAPH_112_1 |
| 指标名称 | 服务机构实体识别构建 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构图谱 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·服务机构图谱（SRS seq 131/132 页面族） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2026] |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_GRAPH_112_1.md` |

## 口径定义

实体域 44,153 家可完整圈定（主档对齐 44,132 家，99.95%），七类类型轴与四项主档属性都能现转；但需规点名的「人数」属性只有 1,582 家（3.58%）有观测，且 gkx 没有任何图谱挂载表，节点号只能按 `org_id` 确定性派生、没有物化落库。实体识别这件事本身是通的，属性面的「人」这一维是空的，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_112_1.md` §二（M_SVC_GRAPH_112_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_org_product_info`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：实体域 44153 家（主档对齐 44132，99.95%）与七类类型轴、四项主档属性可现转；但原文点名的「人数」属性仅 1582 家（3.58%）有观测——年报人数字段在池内覆盖率过低，且 gkx 无图谱挂载表（节点号只能确定性派生、无物化），故落部分支持，不抬到完全转换。
- **基期声明**：实体识别是截面件（以采集时点 2026-10 的池为口径），不涉及跨年比较；人数属性取各机构最近一个有值的财务年份，未把缺年按 0 摊入。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_GRAPH_112_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_112_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_GRAPH_112_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

