# 政策实体关系抽取（M_POLICY_GRAPH_107_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_GRAPH_107_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_GRAPH_107_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_GRAPH_107_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_GRAPH_107_1 |
| 指标名称 | 政策实体关系抽取 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策／政策图谱 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 政策图谱页「实体关系」视图、政策详情页的「关联产业/发文机关/适用地区」侧栏 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2024] |
| 缺失年份 | [2023, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_GRAPH_107_1.md` |

## 口径定义

五项点名关系里，「实施主体」能借 `ministry` 弱建（方向是发文方），其余四类分别是「2 行真值」「整列为空」「字面 null 陷阱」「连列都没有」。图谱能建、能遍历、能出 89,460 条边，但**建的边与需求要的边不是同一批边**，因此落**部分支持**而不是「完全转换支持」。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_GRAPH_107_1.md` §二（M_POLICY_GRAPH_107_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_global_policy_base`
- `dwd_global_policy_base_bak_20260923`
- `dwd_industry_chain_info`
- `dwd_policy_base`
- `dwd_policy_base_bak_20260923`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：需求点名的五类关系里只有「实施主体」能弱建成（发文机关 19989/20000 行，方向是发文方而非实施方），「政策主题」「政策目标」「受益对象」「监管机构」四类无字段承载（theme 仅 2 行、keypoints 与 policy_support 真值 0 行、无监管机构字段）；gkx 也没有 policy_graph_edge / policy_entity 现成边表，全部边为字段现建、属本件自定义口径。政策侧骨架（机关/层级/文种/地区/产业节点，共 89460 条边）可遍历，但五类点名关系只落实 1 类且为方向性替代，故落部分支持。
- **基期声明**：本件是截面关系图，不做同比；基期字段只用于声明政策语料的年份覆盖。publish_year 有 37 个不同取值，2000—2026 窗口内 24 年有量、3 年为零行（[2023, 2025, 2026]），2000 年以前另有 138 条历史文本，不进年度序列也不摊 0。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_GRAPH_107_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_GRAPH_107_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_GRAPH_107_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

