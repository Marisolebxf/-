# 深圳创新能力指数（M_INNOV_CITY_INDEX_SZ）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_CITY_INDEX_SZ |
| 指标名称 | 深圳创新能力指数 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 深圳创新监测 / 科技发展城市分析展示 |
| 口径版本 | V1.6-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

衡量深圳在创新资源、创新主体、创新环境上的综合水平，取值 0—100。对象=深圳，可并列对标城指数。本页排名底物。

## 计算逻辑说明

深圳与对标城入集。需求未列指数构成维度，二级按《中国区域创新能力评价报告》收口。采用加权平均，三维：创新资源（研发经费/人员）/ 创新主体（机构+高企）/ 创新环境（有效政策）。本批城内极值归一。

对标宇宙与对比指标相同。三维在本批城内归一后等权 ×100。城市排名指标按序号 130 四维另算，不读本指数。

1. **创新资源**：研发经费合计，否则研发人员合计。
2. **创新主体**：存续机构去重数与高企去重数，本批各归一后等权。
3. **创新环境**：有效政策去重件数。

输出一行一城，含三子项原始值、`index_score`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 深圳创新能力指数 | 创新资源 | 研发经费，否则研发人员。 | SUM(research_development_amount)；空则 SUM(development_employee) | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 | 无 |
| 深圳创新能力指数 | 创新主体 | 存续机构与高企。 | 0.5×norm(机构数)+0.5×norm(高企数) | dwd_org_base_info(org_id, city, reg_status) — 存续机构；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签 | 无 |
| 深圳创新能力指数 | 创新环境 | 有效政策去重件数。 | COUNT(DISTINCT id) | dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 城市机构入集
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外机构入集
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入
- dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员
- dwd_org_tech_tag(org_id, org_tag) — 高新技术标签
- dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策件数

## 待建字段

- 无

## 参考资料

[1] 深圳创新能力指数｜科技部｜创新型国家评价指标体系｜2017年https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/P020131204326192340968.pdf.

