# 人才实体关系抽取（M_TALENT_GRAPH_111_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_GRAPH_111_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_GRAPH_111_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_GRAPH_111_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_GRAPH_111_1 |
| 指标名称 | 人才实体关系抽取 |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 人才／人才图谱 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才图谱页「实体关系」视图、人才详情页的「所属机构 / 合作网络 / 研究方向」侧栏 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_GRAPH_111_1.md` |

## 口径定义

五类点名关系里，「科研机构」可强建（20,829 条，按机构名称串聚合），「技术」可弱建（研究方向自由文本），其余三类无表无字段。骨架活、共著图稀疏但可用，语义关系只落实一类强一类弱，按 §〇 落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_GRAPH_111_1.md` §二（M_TALENT_GRAPH_111_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_scholar`
- `dwd_scholar_coauthor`
- `dwd_scholar_paper_relation`
- `dwd_scholar_research_direction`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：需求明列的 5 类实体关系里只有「科研机构」可强建成（20,829 条，按机构名称串），「技术」只能弱建成（研究方向自由文本，97,249 个不同标签、82.3% 只出现一次，无受控词表）；「企业 / 产业 / 服务机构 / 政策」四类在 gkx 无任何关系表或可映射字段。共著关系仅 0.73% 的行落在人才主档内（8,675/1,187,606），机构 ID 整列为空，主档内网络 61.21% 的学者是孤点。骨架可建、六类关系只落实一类强一类弱，故落部分支持。
- **基期声明**：本件不做年度环比，基期只用于声明语料年份覆盖：dwd_scholar_paper_relation.year 的取值有效区间为 1980—2026（另有 year=0 与 year=2099 的脏值，已剔除、不摊 0）。关系图本身是截面，不随年份重算。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_GRAPH_111_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_GRAPH_111_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_GRAPH_111_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

