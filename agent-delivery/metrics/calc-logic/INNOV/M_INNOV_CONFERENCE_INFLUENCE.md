# 会议影响力（M_INNOV_CONFERENCE_INFLUENCE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CONFERENCE_INFLUENCE |
| 指标名称 | 会议影响力 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技全域态势 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

科技会议作为科创要素的影响程度。统计对象为选定范围内的科技会议实体，从会议热度、投稿数、参与人数三个维度综合评分，取值 0—100。

## 计算逻辑说明

用出版物类型识别会议。热度优先读影响指数，没有则用该会论文下载量合计；投稿取统计年会议论文数；参与取会议论文去重作者数。三维在本批会议内标准化后按 0.5/0.25/0.25 加权合成 0 到 100。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 会议热度 |  | 会议影响指数；没有则用该会论文下载量合计。 | 优先读 impact_score；没有则对该会论文 download_num 求和，空当 0。 | dwd_zh_journal / dwd_en_journal(publication_id, publication_type, impact_score) — 会议,影响指数；dwd_zh_paper(id, publication_id, publication_type, download_num, cover_year_start) — 会议论文,下载量 |
| 投稿数 |  | 统计年该会已发表会议论文数。 | 统计年中英文会议论文按 id 去重计数。 | dwd_zh_paper(id, publication_id, publication_type, cover_year_start) — 中文会议论文；dwd_en_paper(id, publication_id, publication_type, cover_year_start) — 英文会议论文 |
| 参与人数 |  | 统计年该会会议论文去重作者数。 | 作者优先按 author_id 去重，没有 id 时用姓名去重。 | dwd_zh_author(paper_id, author_id, zh_name, en_name) — 中文作者；dwd_en_author(paper_id, author_id, zh_name, en_name) — 英文作者 |

## 源表字段

dwd_zh_journal(publication_id, publication_type, zh_name, en_name, impact_score) — 中文侧会议,影响指数；dwd_en_journal(publication_id, publication_type, zh_name, en_name, impact_score) — 英文侧会议,影响指数；dwd_zh_paper(id, publication_id, publication_type, publication_zh_name, download_num, cover_year_start) — 中文会议论文,下载量,统计年；dwd_en_paper(id, publication_id, publication_type, publication_en_name, cover_year_start) — 英文会议论文,统计年；dwd_zh_author(paper_id, author_id, zh_name, en_name) — 中文作者；dwd_en_author(paper_id, author_id, zh_name, en_name) — 英文作者

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技全域态势.md|序号 11「支持要素影响力分析，通过算法模型评估各要素的重要性和影响力」。05 无会议评价专叶，内部默认以会议热度为主、投稿数/参与人数为辅，公式未签。参考权威机构方案。会议实体评价表数据源标准缺失，需郭经理与数据采购方沟通。
