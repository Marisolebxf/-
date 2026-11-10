# 企业影响力（M_INNOV_ENTERPRISE_INFLUENCE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_ENTERPRISE_INFLUENCE |
| 指标名称 | 企业影响力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.3-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

企业作为科创要素在科技创新、成果转化、产业带动上的影响程度。统计对象为选定范围内的企业主体，从这三个维度综合评分，取值 0—100。分数越高，企业影响力越强。

## 计算逻辑说明

源表字段以第三方要素库 md-extract 为准。不用废弃表：`dwd_org_base_info_patent_rel`、`dwd_org_merger_acquisition_info`、`dwd_org_financing_info`、`dwd_org_invest_info`。

第一步：入集

`dwd_org_base_info` 按 `org_id` 去重；`reg_status` 含「存续」；`org_type` 含「公司」或「企业」。空间筛选用 `province/city/area`。名称对齐一律用 `name_cn`。

第二步：三个子项

1. **科技创新**：统计年该企业专利去重数 + 中英文论文去重数。
   - 专利：`dwd_patent.first_applicant_name` 对齐 `name_cn`，`apdt_year` 落统计年，`COUNT(DISTINCT pn)`。
   - 论文：`dwd_zh_author.institution` / `dwd_en_author.institution` 对齐 `name_cn`，经 `paper_id` 挂到论文；`cover_year_start` 落统计年，分别 `COUNT(DISTINCT id)`。
2. **成果转化**：统计窗内该企业作为转移前或转移后权利人出现的专利转移去重件数。`transfer_before.name` 或 `transfer_after.name` 对齐 `name_cn`，`transfer_effective_date` 落窗，`COUNT(DISTINCT pn)`。
3. **产业带动**：子公司去重数（`dwd_org_subsidiary_info.sub_org_id`）；为 0 时改用年报/上市 `operating_revenue`（年报取 `year`，上市取最近 `occur_period`）。

第三步：合成

三子项在本批入集企业内分别极值归一，等权后 ×100。缺测子项不补 0，剩余维权重按比例重归一。

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
企业影响力=\frac{norm(科技创新)+norm(成果转化)+norm(产业带动)}{3}\times 100
$$

输出：一行一个企业，含三子项原始值与 `influence_score`（0—100）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 企业影响力 | 科技创新 | 企业专利与论文产出规模。 | COUNT(DISTINCT pn)+COUNT(DISTINCT 中文论文id)+COUNT(DISTINCT 英文论文id) | dwd_org_base_info(org_id, name_cn) — 名称对齐；dwd_patent(pn, first_applicant_name, apdt_year) — 专利,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,统计年；dwd_en_paper(id, cover_year_start) — 英文论文,统计年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 企业影响力 | 成果转化 | 企业专利权属流转规模，代理技术交易。 | COUNT(DISTINCT 转移pn) | dwd_org_base_info(org_id, name_cn) — 名称对齐；dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,转移前后权利人 | 无 |
| 企业影响力 | 产业带动 | 企业对其他主体的带动面；无子公司时用营收。 | COUNT(DISTINCT sub_org_id)；为 0 时取 operating_revenue | dwd_org_subsidiary_info(org_id, sub_org_id) — 子公司；dwd_org_annual_financial_info(org_id, operating_revenue, year) — 年报营收； | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 企业入集,空间筛选,名称对齐
- dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,第一原始申请人,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文,统计年
- dwd_en_paper(id, cover_year_start) — 英文论文,统计年
- dwd_zh_author(paper_id, institution) — 中文作者单位,挂论文
- dwd_en_author(paper_id, institution) — 英文作者单位,挂论文
- dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,生效日,转移前后权利人
- dwd_org_subsidiary_info(org_id, sub_org_id) — 子公司
- dwd_org_annual_financial_info(org_id, operating_revenue, year) — 年报营收
- dwd_org_stock_finance_info(org_id, operating_revenue, occur_period) — 上市营收

## 待建字段

- 无

## 参考资料

[1]企业影响力｜中国海洋石油总公司科技发展部｜沈伟，刘旭，陈伟. 科技成果综合指标在企业绩效评价中的应用[J]. 科研管理, 2009, 30(S1): 123-126. DOI: 10.19571/j.cnki.1000-2995.2009.s1.023.
