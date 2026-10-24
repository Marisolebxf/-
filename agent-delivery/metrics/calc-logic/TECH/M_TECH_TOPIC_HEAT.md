# 技术话题热度（M_TECH_TOPIC_HEAT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_TOPIC_HEAT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_TOPIC_HEAT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_TOPIC_HEAT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_TOPIC_HEAT |
| 指标名称 | 技术话题热度 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 创新分析 |
| 更新频率 | 季度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 技术热点榜、技术趋势雷达、招商技术方向推荐 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_TOPIC_HEAT.md` |

## 口径定义

技术话题热度要回答的是「哪些技术方向正在变热」。回答它需要两样东西：一套把原始分类码归到「人可读主题」的字典，和一份跨专利、论文、媒体三侧一致的计数。gkx 有原始分类码（IPC4、中图分类号、产业链节点名），也有足量记录，但没有官方主题字典：`dwd_tech_topic` 0 张，`dwd_industry_analysis_topics` 只有 3 个主题名且是英文残片。字典只能自建，权重也只能自定，加上论文分类覆盖率不足两成，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_TOPIC_HEAT.md` §二（M_TECH_TOPIC_HEAT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_analysis_topics`
- `dwd_industry_chain_info`
- `dwd_industry_chain_news_info`
- `dwd_patent`
- `dwd_tech_topic`
- `dwd_zh_paper_classification`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：专利 IPC、论文中图分类、产业链新闻三侧都有真实数据可算，但「技术词→主题」没有官方映射：`dwd_tech_topic` 0 张表，`dwd_industry_analysis_topics` 只有 3 个不同主题名（字典残片），IPC 与中图分类也无官方对照表。主题字典为自建，且论文分类只覆盖 20,048/100,900（19.87%），有整维口径缺口，故判部分支持。
- **基期声明**：专利侧 2017—2020 零行，不按 0 摊入；2025/2026 为采集残年，不进增速。论文分类表没有日期列，只能给截面，不能给年度趋势；链新闻覆盖 2025-02-01—2026-07-27，媒体分量是 2025—2026 单窗。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_TOPIC_HEAT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_TOPIC_HEAT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_TOPIC_HEAT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

