# 城市创新能力要素表现（M_INNOV_CITY_FACTOR_GLOBAL）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_CITY_FACTOR_GLOBAL |
| 指标名称 | 城市创新能力要素表现 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 城市创新能力分析 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

各城在人才、资金、政策三要素上的量化表现，取值 0—100。对象=城市。不拆成多条 ID。

## 计算逻辑说明

城市入集。采用加权平均，三维：人才（学者+研发人员）/ 资金（研发经费）/ 政策（有效政策数）。本批城内极值归一。

### 第一步：入集

页面年窗。机构按城入集并名称对齐，规则同城市对标。

### 第二步：三个子项

1. **人才**：`dwd_scholar` 机构名切开后对齐该城机构的 `scholar_id` 去重数 + `development_employee` 合计。
2. **资金**：该城机构 `research_development_amount` 合计；全空该维缺测。
3. **政策**：`dwd_policy_base` 有效且 `city`/`province` 命中的政策去重件数。

### 第三步：合成

本批城内极值归一后等权 ×100。输出一行一城，含三子项原始值与要素得分。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 城市创新能力要素表现 | 人才 | 学者与研发人员。 | 学者去重数 + SUM(development_employee) | dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 | 无 |
| 城市创新能力要素表现 | 资金 | 上市研发投入。 | SUM(research_development_amount) | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入 | 无 |
| 城市创新能力要素表现 | 政策 | 有效政策去重件数。 | COUNT(DISTINCT id) | dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 城市机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外机构入集
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名
- dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入
- dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策件数

## 待建字段

- 无

## 参考资料

[1]城市创新能力要素表现｜科学技术部｜国家高新技术产业开发区综合评价指标体系：国科发火〔2021〕106号｜2021-04-22｜[科技部关于印发《国家高新技术产业开发区综合评价指标体系》的通知-中华人民共和国科学技术部](https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2021/202104/t20210429_174232.html).
