# 论文影响力（M_INNOV_PAPER_INFLUENCE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PAPER_INFLUENCE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PAPER_INFLUENCE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PAPER_INFLUENCE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PAPER_INFLUENCE |
| 指标名称 | 论文影响力 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | DS-01 科技全域态势 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 科技发展态势 → 科技全域态势 → 科创要素（论文详情页属性）；需求原文另在「人才学术力评估分析·多指标评价体系」把「被引次数」列为学术力维度 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"] |
| 缺失年份 | ["2024", "2025", "2026"] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_PAPER_INFLUENCE.md` |

## 口径定义

被引次数维**有表有值但只覆盖 2 万条、能挂回主表的仅 782 篇（0.775%）**，影响因子维**整列为空**（`dwd_zh_journal.impact_score` 0/2,796），下载量维**整列为 0**（100,900 行 SUM=0）；库内参考文献只能构造出 166 条入边。按 §〇 定义，被引这一必需维在主库语料上无法取到足够数据，判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PAPER_INFLUENCE.md` §二（M_INNOV_PAPER_INFLUENCE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_paper`
- `dwd_en_paper_cited_by_info`
- `dwd_scholar_paper_relation`
- `dwd_scholar_papers`
- `dwd_zh_journal`
- `dwd_zh_paper`
- `dwd_zh_paper_citation`
- `dwd_zh_paper_reference_content`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：被引次数维**有表有值但只覆盖 2 万条、能挂回主表的仅 782 篇（0.775%）**，影响因子维**整列为空**（`dwd_zh_journal.impact_score` 0/2,796），下载量维**整列为 0**（100,900 行 SUM=0）；库内参考文献只能构造出 166 条入边。按 §〇 定义，被引这一必需维在主库语料上无法取到足够数据，判**部分支持**。
- **基期声明**：论文年度序列 1980—2026 真实存在，但 2024 是采集批次断点（32,379 篇，为 2023 年的 4.87 倍）、2025/2026 为残年；任何「前 N 年基线/CAGR」只能用 2015—2023 这段，2024 起三年不得按真实增长处理，更不得按 0 摊入分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PAPER_INFLUENCE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PAPER_INFLUENCE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PAPER_INFLUENCE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

