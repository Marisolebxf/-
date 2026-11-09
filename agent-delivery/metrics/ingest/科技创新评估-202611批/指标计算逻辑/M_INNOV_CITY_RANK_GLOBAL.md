# 城市创新能力排名（M_INNOV_CITY_RANK_GLOBAL）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_CITY_RANK_GLOBAL |
| 指标名称 | 城市创新能力排名 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 城市创新能力分析 |
| 口径版本 | V1.6-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

全球主要城市创新能力名次。对象=城市，宇宙=有产出的全球城市。排序底物与城市对标同一三维，取值名次从 1 起。

## 计算逻辑说明

有产出城市入集。需求未列构成维度，二级沿用同页序号 85。采用加权平均，三维：创新投入 / 创新产出 / 创新环境。按综合分降序排名。

三维公式与 `M_INNOV_CITY_BENCHMARK_GLOBAL` 相同。宇宙=统计年专利或论文件数 > 0 的城市（海外用 `country`/`city`）。

本批至少 2 城才做极值归一。按综合分降序编 `rank`。输出一行一城，含三维原始值、`score`（0—100）、`rank`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 城市创新能力排名 | 创新投入 | 上市研发经费，否则研发人员。 | SUM(research_development_amount)；空则 SUM(development_employee) | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 | 无 |
| 城市创新能力排名 | 创新产出 | 专利与论文去重件数。 | COUNT(DISTINCT pn)+COUNT(DISTINCT 论文id) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 城市创新能力排名 | 创新环境 | 有效政策与高企覆盖。 | 0.5×norm(政策数)+0.5×norm(高企数) | dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策件数；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签 | 无 |

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
- dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策件数
- dwd_org_tech_tag(org_id, org_tag) — 高新技术标签

## 待建字段

- 无

## 参考资料

[1]城市创新能力排名｜科学技术部｜国家高新技术产业开发区综合评价指标体系：国科发火〔2021〕106号｜2021-04-22｜[科技部关于印发《国家高新技术产业开发区综合评价指标体系》的通知-中华人民共和国科学技术部](https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2021/202104/t20210429_174232.html).
