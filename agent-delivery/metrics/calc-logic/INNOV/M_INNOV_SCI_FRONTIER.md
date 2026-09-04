# 科学研究前沿性（M_INNOV_SCI_FRONTIER）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_SCI_FRONTIER |
| 指标名称 | 科学研究前沿性 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

识别选定领域内的研究前沿和热点方向，并给出前沿主题的时间演变与空间分布。对象=领域主题（共被引簇/关键词）。

## 计算逻辑说明

按题名入集领域论文。四维：研究前沿 / 热点方向 / 时间演变 / 空间分布。引文落 citation_id_list，不用作者关系表。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 研究前沿 |  | 高被引论文共被引连通簇。 | 共被引≥2 的连通分量；簇强度=簇内论文数×总被引 | dwd_zh_paper_citation(id, citation_num, citation_id_list) — 中文被引次数,被引列表；dwd_en_paper_reference(id, citation_count, cited_reference_id_list) — 英文被引次数,被引列表；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词 |
| 热点方向 |  | 高频且共现的关键词。 | COUNT(DISTINCT 论文id)；词对共现≥2 | dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词 |
| 时间演变 |  | 主题词近窗相对基线的增幅。 | (近3年均值-前5年均值)/max(前5年均值,1) | dwd_zh_paper(id, cover_year_start) — 中文发表年；dwd_en_paper(id, cover_year_start) — 英文发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词 |
| 空间分布 |  | 主题论文在各城的份额。 | COUNT(该城论文)/COUNT(主题论文) | dwd_zh_author(paper_id, institution, affiliation) — 中文作者单位,地址；dwd_en_author(paper_id, institution, affiliation) — 英文作者单位,地址；dwd_org_base_info(org_id, name_cn, city, province) — 名称对齐,城市 |

## 源表字段

dwd_zh_paper(id, zh_name, en_name, cover_year_start) — 中文论文去重,题名入集,发表年；dwd_en_paper(id, zh_name, en_name, cover_year_start) — 英文论文去重,题名入集,发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词；dwd_zh_paper_citation(id, citation_num, citation_id_list) — 中文被引次数,被引列表；dwd_en_paper_reference(id, citation_count, cited_reference_id_list) — 英文被引次数,被引列表；dwd_zh_author(paper_id, institution, affiliation) — 中文作者单位,地址；dwd_en_author(paper_id, institution, affiliation) — 英文作者单位,地址；dwd_org_base_info(org_id, name_cn, city, province) — 名称对齐,城市

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|科技创新评估.md|科学研究前沿性分析 · 序号 138(通过文献计量学和引文网络分析，识别特定领域内的研究前沿和热点方向，用户可查看前沿主题的时间演变和空间分布)
