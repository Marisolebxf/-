# 深圳科技发展指标对比（M_INNOV_CITY_COMPARE_SZ）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_CITY_COMPARE_SZ |
| 指标名称 | 深圳科技发展指标对比 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 深圳创新监测 / 科技发展城市分析展示 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

深圳市与选定对标城市在研发投入、专利数量、高新技术企业数量、创新人才上的横向对比。对象=城市，不是载体、不是湾区 11 城固定集合。

## 计算逻辑说明

深圳与对标城入集。四维：研发投入（研发经费/人员）/ 专利数量 / 高新技术企业数量 / 创新人才（学者+研发人员）。本批城内对比。

### 第一步：入集

深圳必入。对标城由页面选定；未选则取本批专利+论文件数前 8 城（含深圳）。机构按 `city` 入城。

### 第二步：四个子项

各维在所选城市内极值归一后展示 0—100 分，同时保留原始值。不强制合成单分；页面要综合分时四维等权。

输出一行一城，含四子项原始值与维得分。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 深圳科技发展指标对比 | 研发投入 | 该城上市研发经费，否则研发人员。 | SUM(research_development_amount)；空则 SUM(development_employee) | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 | 无 |
| 深圳科技发展指标对比 | 专利数量 | 该城专利去重件数。 | COUNT(DISTINCT pn) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年 | 无 |
| 深圳科技发展指标对比 | 高新技术企业数量 | org_tag 含高新技术的机构去重数。 | COUNT(DISTINCT org_id WHERE org_tag 含高新技术) | dwd_org_tech_tag(org_id, org_tag) — 高新技术标签 | 无 |
| 深圳科技发展指标对比 | 创新人才 | 对齐到该城的学者与研发人员。 | 学者去重数 + SUM(development_employee) | dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 城市机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外机构入集
- dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位
- dwd_en_author(paper_id, institution) — 英文作者单位
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入
- dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员
- dwd_org_tech_tag(org_id, org_tag) — 高新技术标签
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名

## 待建字段

- 无

## 参考资料

[1]深圳科技发展指标对比｜科学技术部｜国家高新技术产业开发区综合评价指标体系：国科发火〔2021〕106号｜2021-04-22｜[科技部关于印发《国家高新技术产业开发区综合评价指标体系》的通知-中华人民共和国科学技术部](https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2021/202104/t20210429_174232.html).
