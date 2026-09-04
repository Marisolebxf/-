# 本地科技创新特色与优势（M_INNOV_PLAN_LOCAL_ADV）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PLAN_LOCAL_ADV |
| 指标名称 | 本地科技创新特色与优势 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技发展规划 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q149 / Q-MO-DS09-01 |

## 口径定义

本地（默认深圳）相对全域的区位商。领域主键就是 IPC 前 4 位。专利区位商>1 为优势领域。

## 计算逻辑说明

本地（默认深圳）按 IPC 前 4 位入集。三维：专利区位商 / 论文区位商 / 创新资源区位商。区位商>1 为优势领域。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 专利区位商 |  | 本地该 IPC4 专利份额相对全域份额。 | (本地该方向专利/本地专利) / (全域该方向专利/全域专利) | dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,关键词袋,申请人对齐,IPC领域,申请年；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤 |
| 论文区位商 |  | 本地该方向论文份额相对全域份额。 | (本地该方向论文/本地论文) / (全域该方向论文/全域论文) | dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 创新资源区位商 |  | 本地该方向活跃机构份额相对全域份额。 | (本地该方向机构/本地机构) / (全域该方向机构/全域机构) | dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_org_annual_financial_info(org_id, year, development_employee) — 研发人员 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤；dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,关键词袋,申请人对齐,IPC领域,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_org_annual_financial_info(org_id, year, development_employee) — 研发人员

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技发展规划.md|序号 181「分析本地在科技创新方面的特色和优势，用户可查看本地优势领域、创新资源分布等分析结果，提供与全球水平的对比分析」。对象=规划页「本地」区域（Q-MO-DS09-01：未选时默认深圳）。不是深圳城市竞争力拆项。参考权威机构方案。
