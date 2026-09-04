# 要素聚类（M_INNOV_FACTOR_CLUSTER）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_FACTOR_CLUSTER |
| 指标名称 | 要素聚类 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技全域态势 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

对会议、项目（含课题）、专利、期刊四类科创要素，用各自影响力得分做无监督分簇。输出簇标签与簇规模，不是 0—100 分。

## 计算逻辑说明

对会议/项目/专利/期刊四类要素，分别取对应影响力得分后聚类。特征为类型独热 + 影响力分。样本≥30用K-Means（K=2到8取最大轮廓），5到29用层次聚类。

## 源表字段

dwd_zh_journal(publication_id, publication_type, impact_score, paper_nums, cite_nums) — 会议/期刊入集,影响指数,发文量,被引用量；dwd_en_journal(publication_id, publication_type, impact_score, paper_nums) — 会议/期刊入集,影响指数,发文量；dwd_zh_paper(id, publication_id, publication_type, download_num, cover_year_start) — 会议论文,下载量,期刊发文回退,统计年；dwd_en_paper(id, publication_id, publication_type, cover_year_start) — 会议论文,期刊发文回退,统计年；dwd_zh_author(paper_id, author_id, zh_name, en_name) — 中文作者,会议参与人数；dwd_en_author(paper_id, author_id, zh_name, en_name) — 英文作者,会议参与人数；dwd_zh_project(id, funded_amount, participating_institution, funded_institution, final_report_abstract, approval_year) — 国内项目入集,资助金额,参与机构,结题摘要,立项年；dwd_en_project(id, funded_amount, participating_institution, funded_institution, final_report_abstract, approval_year) — 国外项目入集,资助金额,参与机构,结题摘要,立项年；dwd_patent(pn, value, apdt_year, pbdt_year) — 专利去重,专利价值,申请年,公开年；dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技全域态势.md|序号 11「提供要素聚类分析，将相似要素进行自动分类和归纳」。库无专叶，保持 missing。禁止把 seq 96 区域论文「数据处理/聚类分析」写成 mapped。参考权威机构方案。
