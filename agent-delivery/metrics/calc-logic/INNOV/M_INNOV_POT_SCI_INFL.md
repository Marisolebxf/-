# 产业科学影响力（M_INNOV_POT_SCI_INFL）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_POT_SCI_INFL |
| 指标名称 | 产业科学影响力 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

按论文被引次数、国际合作论文比例综合评分，取值 0—100。

## 计算逻辑说明

选定产业入集。采用加权平均，二维：论文被引次数（citation_num）/ 国际合作论文比例（作者地址国别≥2）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 论文被引次数 |  | 产业相关论文被引合计。 | SUM(citation_num) | dwd_zh_paper_citation(id, citation_num) — 中文论文被引；dwd_scholar(scholar_id, scholar_org_name_zh, citation_nums) — 学者被引；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 国际合作论文比例 |  | 作者地址跨两个及以上国家的论文占比。 | 国际合作论文数 / 论文数 | dwd_zh_author(paper_id, institution, affiliation) — 中文作者单位,地址国别；dwd_en_author(paper_id, institution, affiliation) — 英文作者单位,地址国别；dwd_zh_paper(id, cover_year_start) — 中文论文分母,发表年；dwd_en_paper(id, cover_year_start) — 英文论文分母,发表年 |

## 源表字段

dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_citation(id, citation_num) — 中文论文被引；dwd_zh_author(paper_id, institution, affiliation) — 中文作者单位,地址国别；dwd_en_author(paper_id, institution, affiliation) — 英文作者单位,地址国别；dwd_scholar(scholar_id, scholar_org_name_zh, citation_nums) — 学者被引

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技创新评估.md|序号 149「基于论文引用、国际合作等数据，评估特定产业的科学影响力……（如论文被引次数、国际合作论文比例）」。对象=产业（非区域）。182「学术影响力」是区域科技成果分项，对象不符。参考权威机构方案。
