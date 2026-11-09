# 深圳城市科技发展排名（M_INNOV_CITY_RANK_SZ）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_CITY_RANK_SZ |
| 指标名称 | 深圳城市科技发展排名 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 深圳创新监测 / 科技发展城市分析展示 |
| 口径版本 | V1.6-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

深圳在各科技发展指标上相对对标城的名次。对象=城市；宇宙=深圳+对标。科技发展指标收口需求序号 130：研发投入、专利数量、高新技术企业数量、创新人才。名次从 1 起。

## 计算逻辑说明

深圳与对标城入集。四维：研发投入 / 专利数量 / 高新技术企业数量 / 创新人才。各维分别降序排名，综合名次按四维等权得分。

入集与原始值同 `M_INNOV_CITY_COMPARE_SZ`。各维在对标宇宙内极值归一后等权得综合分，再编 `rank`。输出一行一城，含四维原始值、四维名次、综合名次；主读面取深圳行。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 深圳城市科技发展排名 | 研发投入 | 该城上市研发经费，否则研发人员。 | SUM(research_development_amount)；空则 SUM(development_employee) | dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入 | 无 |
| 深圳城市科技发展排名 | 专利数量 | 该城专利去重件数。 | COUNT(DISTINCT pn) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年 | 无 |
| 深圳城市科技发展排名 | 高新技术企业数量 | org_tag 含高新技术的机构去重数。 | COUNT(DISTINCT org_id WHERE org_tag 含高新技术) | dwd_org_tech_tag(org_id, org_tag) — 高新技术标签 | 无 |
| 深圳城市科技发展排名 | 创新人才 | 对齐到该城的学者与研发人员。 | 学者去重数 + SUM(development_employee) | dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 城市机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外机构入集
- dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年
- dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入
- dwd_org_tech_tag(org_id, org_tag) — 高新技术标签
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名

## 待建字段

- 无

## 参考资料

[1] 深圳城市科技发展排名｜科技部｜创新型国家评价指标体系｜2017年https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/P020131204326192340968.pdf..
