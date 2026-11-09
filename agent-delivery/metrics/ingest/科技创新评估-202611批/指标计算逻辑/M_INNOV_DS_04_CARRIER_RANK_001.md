# 创新能力指数（M_INNOV_DS_04_CARRIER_RANK_001）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_04_CARRIER_RANK_001 |
| 指标名称 | 创新能力指数 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 创新载体排行榜 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_CARRIER_INDEX_GLOBAL（创新载体创新能力指数）**。

## 计算逻辑说明

本指标与 **M_INNOV_CARRIER_INDEX_GLOBAL（创新载体创新能力指数）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_org_base_info(org_id, name_cn, org_type, reg_status, province, city) — 国内载体入集,名称对齐,存续过滤,空间筛选
- dwd_research_institute_base_info(org_id, name_cn, org_type, reg_status, province, city) — 科研机构入集,名称对齐,存续过滤
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外载体入集,名称对齐,国家城市
- dwd_org_annual_financial_info(org_id, year, development_employee, employees_number, operating_revenue) — 年报研发人员,从业人数,营收
- dwd_org_stock_finance_info(org_id, occur_period, operating_revenue) — 上市营收
- dwd_org_tech_tag(org_id, org_tag) — 高新技术等科技型标签
- dwd_patent(pn, first_applicant_name, granted_number, apdt_year) — 专利去重,申请人对齐,授权号,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,统计年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,统计年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐

## 待建字段

- 无

## 参考资料

[1]创新载体创新能力指数｜科学技术部｜国家高新技术产业开发区综合评价指标体系：国科发火〔2021〕106号｜2021-04-22｜[科技部关于印发《国家高新技术产业开发区综合评价指标体系》的通知-中华人民共和国科学技术部](https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2021/202104/t20210429_174232.html).
