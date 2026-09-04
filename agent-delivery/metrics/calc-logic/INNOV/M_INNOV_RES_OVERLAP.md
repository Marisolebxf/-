# 研究领域重叠度（M_INNOV_RES_OVERLAP）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_RES_OVERLAP |
| 指标名称 | 研究领域重叠度 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技发展规划 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

企业对研究领域重叠度，取值 0—1。集合从专利 IPC、专利/论文关键词、所属学者现表抽取，不另建关键词集合。

## 计算逻辑说明

选定企业入集。采用加权平均，三维：IPC重叠 / 关键词重叠 / 学者重叠（均为 Jaccard）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| IPC重叠 |  | 两家企业专利 IPC4 集合的 Jaccard。 | \|A∩B\| / \|A∪B\| | dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, further_classification_ipcr, apdt_year) — 专利去重,关键词,申请人对齐,主分类,附加分类,申请年；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 企业入集,名称对齐,空间过滤 |
| 关键词重叠 |  | 两家企业专利与论文关键词集合的 Jaccard。 | \|A∩B\| / \|A∪B\| | dwd_patent(pn, keywords, first_applicant_name, apdt_year) — 专利关键词,申请人对齐；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 学者重叠 |  | 两家企业所属学者集合的 Jaccard。 | \|A∩B\| / \|A∪B\| | dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 企业入集,名称对齐,空间过滤；dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, further_classification_ipcr, apdt_year) — 专利去重,关键词,申请人对齐,主分类,附加分类,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技发展规划.md|序号 191「基于企业－专家－学术文献－研究关键词等知识图谱数据，分析两家企业在研究领域上的重叠度……提供重叠度计算结果和可视化展示」。对象≠ 05 seq 191 区域创新协同，≠ 116 两实体通用语义相似度。参考权威机构方案。
