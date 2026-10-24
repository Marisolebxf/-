# 分类与聚类（合著网络社区发现 + 企业资质向量聚类）（M_SYNTH_DS_21_GRAPH_ANALYSIS_007）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_21_GRAPH_ANALYSIS_007.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_21_GRAPH_ANALYSIS_007.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_21_GRAPH_ANALYSIS_007_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_DS_21_GRAPH_ANALYSIS_007 |
| 指标名称 | 分类与聚类（合著网络社区发现 + 企业资质向量聚类） |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_DS_21_GRAPH_ANALYSIS_007.md` |

## 口径定义

本指标做两层无监督聚类。第一层在 2021—2024 四市机构合著网上跑 Louvain：1,094 个节点、1,174 条边，得到 479 个社区，模块度 Q=0.714468，最大社区 92 个节点（占 8.41%）；

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_21_GRAPH_ANALYSIS_007.md` §二（M_SYNTH_DS_21_GRAPH_ANALYSIS_007.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent_applicants`
- `dwd_scholar_paper_relation`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：两层聚类都有真实输入：合著网 1,094 节点 / 1,174 边可算社区与模块度（Q=0.714468），32,322 家企业的 55 个资质标签可算 KMeans 与轮廓系数（0.304095）；但 L1 的节点只覆盖「有中文论文且机构串可判城」的机构：4 年窗口 52,119 篇里只有 24,835 篇（47.65%）至少含一个可判城机构，署名对层面 37,597/103,263（36.41%）可判城；L2 的标签全部是资质认定类（高企/科技型/专精特新），不含技术领域，簇的经济含义只是「资质等级」而非「技术方向」；55 维二值特征稀疏度 88.61%，高企与国家级高企的 φ 相关 0.5586，轮廓系数 0.304095 属「弱结构」。两条都属「可算但解释力有限」，判部分支持。
- **基期声明**：聚类输入为 2021–2024 窗口累计（4 个真实年份），不做年度除法；企业资质标签为截面存量，无年份维度。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_21_GRAPH_ANALYSIS_007.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_21_GRAPH_ANALYSIS_007.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_21_GRAPH_ANALYSIS_007_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

