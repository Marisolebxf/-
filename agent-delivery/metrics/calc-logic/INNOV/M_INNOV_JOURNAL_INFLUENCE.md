# 期刊影响力（M_INNOV_JOURNAL_INFLUENCE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_JOURNAL_INFLUENCE |
| 指标名称 | 期刊影响力 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技全域态势 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

期刊在学术传播中的影响程度。统计对象为期刊实体，从影响指数、发文量、被引用量综合，取值 0—100。

## 计算逻辑说明

采用加权平均。三维：影响指数 / 发文量 / 被引用量（权重 0.50 / 0.25 / 0.25，缺测维重归一）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 影响指数 |  | 期刊影响指数。 | 期刊影响指数（空则该维缺测） | dwd_zh_journal(publication_id, impact_score) — 中文影响指数；dwd_en_journal(publication_id, impact_score) — 英文影响指数 |
| 发文量 |  | 期刊发文规模。 | 优先期刊发文量；没有则统计年挂刊论文去重件数 | dwd_zh_journal(publication_id, paper_nums) — 中文发文量；dwd_en_journal(publication_id, paper_nums) — 英文发文量；dwd_zh_paper(id, publication_id, cover_year_start) — 中文发文回退,统计年；dwd_en_paper(id, publication_id, cover_year_start) — 英文发文回退,统计年 |
| 被引用量 |  | 期刊累计被引。 | 期刊累计被引（英文刊无该字段则该维缺测） | dwd_zh_journal(publication_id, cite_nums) — 中文被引用量 |

## 源表字段

dwd_zh_journal(publication_id, publication_type, zh_name, impact_score, paper_nums, cite_nums) — 中文期刊入集,影响指数,发文量,被引用量；dwd_en_journal(publication_id, publication_type, en_name, impact_score, paper_nums) — 英文期刊入集,影响指数,发文量；dwd_zh_paper(id, publication_id, publication_type, cover_year_start) — 中文发文回退,统计年；dwd_en_paper(id, publication_id, publication_type, cover_year_start) — 英文发文回退,统计年

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技全域态势.md|序号 11「支持要素影响力分析，通过算法模型评估各要素的重要性和影响力」。05 无期刊评价专叶，seq 96 影响因子仅为机构筛选输入。参考权威机构方案。
