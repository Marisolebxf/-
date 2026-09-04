# 企业影响力（M_INNOV_ENTERPRISE_INFLUENCE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_ENTERPRISE_INFLUENCE |
| 指标名称 | 企业影响力 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技全域态势 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

企业作为科创要素在科技创新、成果转化、产业带动上的影响程度。统计对象为选定范围内的企业主体，从这三个维度综合评分，取值 0—100。

## 计算逻辑说明

科技创新：专利用第一申请人对齐企业名，论文用作者单位对齐企业名；成果转化：转移前后权利人对齐企业名计转移件数；产业带动：子公司数，为 0 时用营收。三维本批极值归一后等权合成 0 到 100。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 科技创新 |  | 企业专利与论文产出规模。 | 统计年专利去重件数加中英文论文去重件数。专利用第一申请人对齐企业名；论文用作者单位对齐企业名。 | dwd_org_base_info(org_id, name_cn) — 名称对齐；dwd_patent(pn, first_applicant_name, apdt_year) — 专利,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,统计年；dwd_en_paper(id, cover_year_start) — 英文论文,统计年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 成果转化 |  | 企业专利权属流转规模，代理技术交易。 | 统计窗内转移前或转移后权利人对齐企业名的专利转移去重件数。 | dwd_org_base_info(org_id, name_cn) — 名称对齐；dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,转移前后权利人 |
| 产业带动 |  | 企业对其他主体的带动面；无子公司时用营收。 | 子公司去重计数；为 0 时改读年报或上市营收。 | dwd_org_subsidiary_info(org_id, sub_org_id) — 子公司；dwd_org_annual_financial_info(org_id, operating_revenue, year) — 年报营收；dwd_org_stock_finance_info(org_id, operating_revenue, occur_period) — 上市营收 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 企业入集,空间筛选,名称对齐；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,第一原始申请人,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,统计年；dwd_en_paper(id, cover_year_start) — 英文论文,统计年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移；dwd_org_subsidiary_info(org_id, sub_org_id) — 子公司；dwd_org_annual_financial_info(org_id, operating_revenue, year) — 年报营收；dwd_org_stock_finance_info(org_id, operating_revenue, occur_period) — 上市营收

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技全域态势.md|序号 11「支持要素影响力分析，通过算法模型评估各要素的重要性和影响力」。对照 seq 145 技术力（辅 146/97），第三方不展开。禁止消费展示企业包 M_ENT_*。态势要素核，参考权威机构方案。
