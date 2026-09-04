# 竞争情报等级（M_INNOV_RES_CI_LEVEL）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_RES_CI_LEVEL |
| 指标名称 | 竞争情报等级 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技发展规划 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q151 / Q-MO-DS09-03 |

## 口径定义

多家企业两两竞争情报强弱。分值=重叠度×100，等级与 GRADE 同一阈值。输出竞争矩阵。

## 计算逻辑说明

选定企业入集。竞争情报分值 = 重叠度 ×100；等级复用分档阈值。输出企业对矩阵。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 竞争情报分值 |  | 企业对研究领域重叠度换算为 0—100。 | overlap × 100 | dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 企业入集,名称对齐,空间过滤；dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, further_classification_ipcr, apdt_year) — 专利去重,关键词,申请人对齐,主分类,附加分类,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名 |
| 竞争情报等级 |  | 按与 GRADE 相同的阈值分高/中/低。 | ≥P70高；P30–P70中；<P30低（可改） | 本批 overlap 分位或页面阈值 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 企业入集,名称对齐,空间过滤；dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, further_classification_ipcr, apdt_year) — 专利去重,关键词,申请人对齐,主分类,附加分类,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技发展规划.md|序号 193「支持比对多家不同企业之间的竞争情报等级，用户可选择多家企业进行比对分析，并提供竞争矩阵和战略定位图」。半成品独立主项：用量化指标对重叠度划分等级，反映企业间竞争情报强弱。与 GRADE 同族。参考权威机构方案。
