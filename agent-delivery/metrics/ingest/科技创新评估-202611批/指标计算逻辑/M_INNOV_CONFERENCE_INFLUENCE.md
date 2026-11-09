# 会议影响力（M_INNOV_CONFERENCE_INFLUENCE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_CONFERENCE_INFLUENCE |
| 指标名称 | 会议影响力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.2-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

科技会议作为科创要素的影响程度。统计对象为选定范围内的科技会议实体，从会议热度、投稿数、参与人数三个维度综合评分，取值 0—100。分数越高，会议影响力越强。

## 计算逻辑说明

不用融资/投资/并购类表。会议实体从出版物表识别，三个子项都用论文与出版物现成字段直算。

第一步：入集

取 `dwd_zh_journal`、`dwd_en_journal` 中 `publication_type` 为 conference / 会议（大小写不敏感）的记录，按 `publication_id` 去重。  
无出版物主数据时，用 `dwd_zh_paper` / `dwd_en_paper` 中同类型记录，按 `publication_id`（空则用会议名）聚合。

第二步：三个子项（统计年取论文 `cover_year_start`）

1. **会议热度**：优先读该会 `impact_score`；没有则用该会论文 `download_num` 合计（空当 0）。
2. **投稿数**：该会统计年中英文会议论文去重件数。
3. **参与人数**：上述论文对应作者去重件数（优先 `author_id`，没有用姓名）。

第三步：合成

三子项在本批入集会内分别极值归一，默认权重热度 0.50、投稿 0.25、参与 0.25，加权后 ×100。缺测子项不补 0，剩余维权重按比例重归一。

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
会议影响力=(0.5\times norm(热度)+0.25\times norm(投稿)+0.25\times norm(参与))\times 100
$$

输出：一行一个会议，含三子项原始值与 `influence_score`（0—100）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 会议影响力 | 会议热度 | 会议影响指数；没有则用论文下载量合计。 | 优先 impact_score；否则 SUM(download_num) | dwd_zh_journal / dwd_en_journal(publication_id, publication_type, impact_score) — 会议,影响指数；dwd_zh_paper(id, publication_id, publication_type, download_num, cover_year_start) — 会议论文,下载量 | 无 |
| 会议影响力 | 投稿数 | 统计年该会已发表会议论文数。 | COUNT(DISTINCT 会议论文id) | dwd_zh_paper(id, publication_id, publication_type, cover_year_start) — 中文会议论文；dwd_en_paper(id, publication_id, publication_type, cover_year_start) — 英文会议论文 | 无 |
| 会议影响力 | 参与人数 | 统计年该会会议论文去重作者数。 | COUNT(DISTINCT author_id)；无 id 用姓名去重 | dwd_zh_author(paper_id, author_id, zh_name, en_name) — 中文作者；dwd_en_author(paper_id, author_id, zh_name, en_name) — 英文作者 | 无 |

## 源表字段

- dwd_zh_journal(publication_id, publication_type, zh_name, en_name, impact_score) — 中文侧会议实体,影响指数
- dwd_en_journal(publication_id, publication_type, zh_name, en_name, impact_score) — 英文侧会议实体,影响指数
- dwd_zh_paper(id, publication_id, publication_type, publication_zh_name, download_num, cover_year_start) — 中文会议论文,下载量,统计年
- dwd_en_paper(id, publication_id, publication_type, publication_en_name, cover_year_start) — 英文会议论文,统计年
- dwd_zh_author(paper_id, author_id, zh_name, en_name) — 中文作者
- dwd_en_author(paper_id, author_id, zh_name, en_name) — 英文作者

## 待建字段

- 无

## 参考资料

[1]会议影响力｜University of Oxford（牛津大学），University of Bonn（波恩大学），RWTH Aachen University（亚琛工业大学）等｜DFG（LA 3745/4-1）；ERC（819536）；Projekt DEAL｜Vahdati S, Fathalla S, Lange C, Behrend A, Say A, Say Z, Auer S. A comprehensive quality assessment framework for scientific events[J].Scientometrics, 2021, 126(1): 641-682.
