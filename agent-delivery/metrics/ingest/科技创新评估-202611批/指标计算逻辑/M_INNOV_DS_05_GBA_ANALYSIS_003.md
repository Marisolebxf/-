# 优势因素分析（M_INNOV_DS_05_GBA_ANALYSIS_003）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_05_GBA_ANALYSIS_003 |
| 指标名称 | 湾区创新能力优势因素 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新能力分析（SWOT） |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_GBA_SWOT_STRENGTH（湾区创新能力优势因素）**。

## 计算逻辑说明

本指标与 **M_INNOV_GBA_SWOT_STRENGTH（湾区创新能力优势因素）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集
- dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 专利去重,共申请人,申请人对齐,申请年
- dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 合作项目
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入
- dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员
- dwd_org_tech_tag(org_id, org_tag) — 高新技术标签
- dwd_policy_base(id, city, province, status, expire_date, publish_year, rank, theme) — 政策供给,主题,有效

## 待建字段

- 无

## 参考资料

[1]优势因素分析｜中国科技发展战略研究小组、中国科学院大学｜—｜《中国区域创新能力评价报告2025》｜2025-09-27｜http://gdstc.gd.gov.cn/kjzx_n/gdkj_n/content/post_4779246.html.

[2]优势因素分析｜江苏省科学技术情报研究所｜2023年度江苏省知识产权科研项目（KY20230077_05）｜陈长益，吴华珠，李向辉，姜迪. 专利导航在区域创新质量评价中的应用研究——以长三角城市群为例[J]. 情报探索, 2025(2): 51-58.
