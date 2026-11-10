# 深圳与对标城市趋势（M_INNOV_CITY_TREND_SZ）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_CITY_TREND_SZ |
| 指标名称 | 深圳与对标城市趋势 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 深圳创新监测 / 科技发展城市分析展示 |
| 口径版本 | V1.6-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

深圳与对标城市在科技发展指标上的历史变化与短期外推。科技发展指标收口需求序号 130：研发投入、专利数量、高新技术企业数量、创新人才。历史与预测共核一条 ID。输出点预测与约 80% 区间。

## 计算逻辑说明

深圳与对标城入集。逐年四维：研发投入 / 专利数量 / 高新技术企业数量 / 创新人才。满 8 期 Holt 外推，输出点预测与区间。

综合分是截面相对分，不直接外推。对四维逐年原始值各自拟合。

### 第一步：年序列

年键：研发 `year`/`occur_period`，专利 `apdt_year`，高企按机构首次打标年缺则用统计年存量，人才用学者存量+`development_employee`。缺年补 0。\(n<8\) 不出预测。

### 第二步：Holt

年频向前 \(h=2\)：\(\hat{y}_{T+k}=\ell+kb\)。下限截 0。约 80% 区间 \(\hat{y}\pm 1.28\hat{\sigma}\sqrt{k}\)。残差 < 5 只出点预测。

输出：一行一城一维一期，含 `yhat`、`yhat_lo`、`yhat_hi`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 深圳与对标城市趋势 | 研发投入 | 年研发经费（或人员）外推。 | Holt(年研发投入) | dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入 | 无 |
| 深圳与对标城市趋势 | 专利数量 | 年申请量外推。 | Holt(年专利数) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年 | 无 |
| 深圳与对标城市趋势 | 高新技术企业数量 | 年高企存量外推。 | Holt(年高企数) | dwd_org_tech_tag(org_id, org_tag) — 高新技术标签 | 无 |
| 深圳与对标城市趋势 | 创新人才 | 年学者与研发人员外推。 | Holt(学者去重数+研发人员) | dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 城市机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外机构入集
- dwd_patent(pn, first_applicant_name, apdt_year) — 专利年序列,申请人对齐
- dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入
- dwd_org_tech_tag(org_id, org_tag) — 高新技术标签
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名

## 待建字段

- 无

## 参考资料

[1] 深圳与对标城市趋势｜科技部｜创新型国家评价指标体系｜2017年https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/P020131204326192340968.pdf.
