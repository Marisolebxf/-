# 企业实体关系抽取（M_ENT_GRAPH_109_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_GRAPH_109_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_GRAPH_109_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_GRAPH_109_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_GRAPH_109_1 |
| 指标名称 | 企业实体关系抽取 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业关系图谱 → 以企业为中心的邻居展开；关系类型筛选器（9 类，4 类可用、1 类样本不足、4 类置灰） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_GRAPH_109_1.md` |

## 口径定义

9 类关系里，投资/归属/产业所属/技术应用 4 类有边（技术应用是「申请人 × IPC」代理），科研合作只有 14 对，人才/政策/服务/合作 4 类连外键都没有。关系覆盖率 4/9 = 44.4444%，但其中 1 类是代理，严格直取只有 3/9 = 33.3333%。故判**部分支持**，证型 `partial_relation_coverage`。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_GRAPH_109_1.md` §二（M_ENT_GRAPH_109_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_industry_tags`
- `dwd_org_invest_info`
- `dwd_org_shareholder_info`
- `dwd_patent`
- `dwd_patent_assignees`
- `dwd_patent_inventors`
- `dwd_patent_transfer`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：9 类关系里，投资/归属/产业所属/技术应用 4 类有边（技术应用是「申请人 × IPC」代理），科研合作只有 14 对，人才/政策/服务/合作 4 类连外键都没有。关系覆盖率 4/9 = 44.4444%，但其中 1 类是代理，严格直取只有 3/9 = 33.3333%。故判**部分支持**，证型 `partial_relation_coverage`。
- **基期声明**：截面件：关系边是库内当前快照，无统一年度键；投资/转让有日期字段但不构成年度序列，不设基期，不做跨年增长率。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_GRAPH_109_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_GRAPH_109_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_GRAPH_109_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

