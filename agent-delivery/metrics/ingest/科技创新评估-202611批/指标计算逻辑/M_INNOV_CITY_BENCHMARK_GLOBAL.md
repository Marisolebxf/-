# 城市对标分析（M_INNOV_CITY_BENCHMARK_GLOBAL）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_CITY_BENCHMARK_GLOBAL |
| 指标名称 | 城市对标分析 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 城市创新能力分析 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

用户选定至少 2 城，对比创新投入、创新产出、创新环境。对象=城市。取值展示原始值与 0—100 维得分，不另开公式。

## 计算逻辑说明

选定城市入集。采用加权平均，三维：创新投入（研发经费/人员）/ 创新产出（专利+论文）/ 创新环境（政策+高企）。本批城内极值归一后对比。

### 第一步：入集

用户选城（至少 2 个）。机构按 `city`（海外 `country`/`city`）入城；`reg_status` 含「存续」。专利 `first_applicant_name`、论文 `institution` 对齐机构名。

### 第二步：三个子项

同一维在**所选城市**内极值归一。缺测维不补 0，剩余维权重重归一。

1. **创新投入**：`research_development_amount` 合计；全空则 `development_employee` 合计。
2. **创新产出**：专利去重件数 + 中英文论文去重件数。
3. **创新环境**：有效政策去重件数与高企去重数，本批各归一后等权。

### 第三步：对比

输出一行一城，含三子项原始值、维得分、等权综合分。对比视图直接读这些列。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 城市对标分析 | 创新投入 | 上市研发经费，否则研发人员。 | SUM(research_development_amount)；空则 SUM(development_employee) | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 | 无 |
| 城市对标分析 | 创新产出 | 专利与论文去重件数。 | COUNT(DISTINCT pn)+COUNT(DISTINCT 论文id) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 城市对标分析 | 创新环境 | 有效政策与高企覆盖。 | 0.5×norm(政策数)+0.5×norm(高企数) | dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策件数；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签 | 无 |

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

[1]城市对标分析｜科学技术部｜国家高新技术产业开发区综合评价指标体系：国科发火〔2021〕106号｜2021-04-22｜[科技部关于印发《国家高新技术产业开发区综合评价指标体系》的通知-中华人民共和国科学技术部](https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2021/202104/t20210429_174232.html).
