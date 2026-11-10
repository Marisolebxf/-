# 产业发展潜力综合评估（M_INNOV_POT_COMPOSITE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_POT_COMPOSITE |
| 指标名称 | 产业发展潜力综合评估 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 产业发展潜力指标展示 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

将投入、成熟度、产值、科学影响力、技术影响力按自定义权重计算的产业发展潜力综合得分与排名。对象=选定产业，取值 0—100，分数越高发展潜力越大。成熟度三维与 `M_INNOV_POT_MATURITY` 一致；科学影响力与 `M_INNOV_POT_SCI_INFL` 一致；技术影响力与 `M_INNOV_POT_TECH_INFL` 一致。

## 计算逻辑说明

选定产业入集。采用加权平均，五维：产业投入（研发投入强度 / 固定资产投资增长率 / 人才投入强度）/ 技术产品成熟度（授权比例 / 发明占比 / 市场渗透）/ 产业产值（总产值 / 利润总额）/ 科学影响力（论文被引 / 国际合作）/ 技术影响力（专利被引 / 同族规模）。

### 第一步：入集

页面年窗、空间（可选）、产业。

机构：`dwd_org_base_info` 按 `org_id` 去重；`reg_status` 含「存续」。产业用 `industry` / `industry_l1_code`，或 `external_id` 对齐 `dwd_org_industry_tags.credit_code` 后取 `industry_code`。名称用 `name_cn`。

专利：`dwd_patent` 按 `pn` 去重；`apdt_year` 落年窗；`first_applicant_name` 对齐机构名后继承产业。  
论文：`dwd_zh_paper` / `dwd_en_paper` 按 `id` 去重；`cover_year_start` 落年窗；作者 `institution` 对齐机构名后继承产业。  
财务：年报 `year`、上市 `occur_period` 落年窗，按 `org_id` 对齐产业。

一行一个产业。本批至少 2 个产业才做极值归一。缺测维不补 0，剩余维权重重归一。

### 第二步：各指标标准化

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

指标得分 \(=norm(x)\times 100\)。同一维在**本批产业**内归一。

### 第三步：各维度得分

默认维内等权，页面可改权重，须 \(\sum w=1\)。

$$
产业投入=w_1\cdot norm(研发投入强度)+w_2\cdot norm(固投增长率)+w_3\cdot norm(人才投入强度)
$$

$$
技术产品成熟度=\frac{norm(授权比例)+norm(发明占比)+norm(市场渗透)}{3}
$$

$$
产业产值=0.5\cdot norm(总产值)+0.5\cdot norm(利润总额)
$$

$$
科学影响力=0.5\cdot norm(论文被引)+0.5\cdot norm(国际合作比例)
$$

$$
技术影响力=0.5\cdot norm(专利被引)+0.5\cdot norm(同族规模)
$$

### 第四步：综合得分

默认五维等权（各 20%），页面可改，须 \(\sum W=1\)。

$$
产业发展潜力综合得分=\sum_{k=1}^{5} W_k\cdot 维度得分_k\times 100
$$

输出：一行一个产业，含各子项原始值、五维得分、`score`（0—100）、`rank`。

### 产业发展潜力综合评估指标体系

| 维度 | 指标 | 指标说明 | 计算方法 | 源表字段 | 待建字段 |
| :----------------- | :----------------- | :------------------------------------------------- | :----------------------------------------------------------- | -------- | -------- |
| **产业投入** | 研发投入强度 | 反映产业对技术创新的资金投入力度和重视程度。 | SUM(research_development_amount) ÷ SUM(operating_revenue) × 100% | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount, operating_revenue) — 上市研发投入,营业收入 | 无 |
| | 固定资产投资增长率 | 反映产业在设备、厂房等固定资产方面的投资扩张趋势。 | （本期固定资产 − 上期固定资产）÷ 上期固定资产 × 100% | dwd_org_annual_financial_info(org_id, year, fixed_assets) — 年报固定资产,年；dwd_org_stock_finance_info(org_id, occur_period, fixed_assets) — 上市固定资产 | 无 |
| | 人才投入强度 | 反映产业对高素质人才的吸引和集聚能力。 | SUM(development_employee) ÷ SUM(employees_number) × 100% | dwd_org_annual_financial_info(org_id, year, development_employee, employees_number) — 研发人员,从业人数 | 无 |
| **技术产品成熟度** | 授权比例 | 授权专利占全部专利比。 | 授权专利数 / 专利数 | dwd_patent(pn, first_applicant_name, granted_number, apdt_year) — 申请人对齐,授权号,申请年 | 无 |
| | 发明占比 | 发明专利占全部专利比。 | 发明专利数 / 专利数 | dwd_patent(pn, first_applicant_name, kind, apdt_year) — 申请人对齐,申请类型,申请年 | 无 |
| | 市场渗透 | 发生转移的专利占比。 | 转移专利数 / 专利数 | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_patent(pn, first_applicant_name, apdt_year) — 专利分母,申请人对齐 | 无 |
| **产业产值** | 总产值 | 反映产业在一定时期内生产活动成果的总规模。 | SUM(main_business_revenue)；空则用 operating_revenue | dwd_org_annual_financial_info(org_id, year, main_business_revenue, operating_revenue) — 年报主营,营收；dwd_org_stock_finance_info(org_id, occur_period, main_business_revenue, operating_revenue) — 上市主营,营收 | 无 |
| | 利润总额 | 反映产业最终经营成果和盈利能力。 | SUM(total_profit) | dwd_org_annual_financial_info(org_id, year, total_profit) — 年报利润总额；dwd_org_stock_finance_info(org_id, occur_period, total_profit) — 上市利润总额 | 无 |
| **科学影响力** | 论文被引次数 | 反映产业相关科学研究的学术影响力和知识传播广度。 | SUM(citation_num)；论文级缺测时用学者 citation_nums | dwd_zh_paper_citation(id, citation_num) — 中文论文被引；dwd_scholar(scholar_id, scholar_org_name_zh, citation_nums) — 学者被引；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| | 国际合作论文比例 | 反映产业科研活动的国际化程度和全球协作能力。 | 作者地址国别 ≥ 2 的论文数 ÷ 论文总数 × 100% | dwd_zh_author(paper_id, institution, affiliation) — 中文作者单位,地址国别；dwd_en_author(paper_id, institution, affiliation) — 英文作者单位,地址国别；dwd_zh_paper(id, cover_year_start) — 中文论文分母,发表年；dwd_en_paper(id, cover_year_start) — 英文论文分母,发表年 | 无 |
| **技术影响力** | 专利被引次数 | 反映产业专利技术的行业影响力和技术扩散程度。 | SUM(cited_by_nums) | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐 | 无 |
| | 同族规模 | 反映产业专利的海外布局广度与技术控制范围。 | 专利 other_Versions 成员数合计 / 专利数；空数组记 1 | dwd_patent(pn, first_applicant_name, other_Versions, apdt_year) — 同族专利,申请人对齐,申请年 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐
- dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount, operating_revenue, main_business_revenue, total_profit, fixed_assets) — 上市研发,营收,主营,利润,固定资产
- dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, total_profit, fixed_assets, development_employee, employees_number) — 年报营收,主营,利润,固定资产,研发人员,从业人数
- dwd_patent(pn, kind, granted_number, first_applicant_name, other_Versions, apdt_year) — 专利去重,申请类型,授权号,申请人对齐,同族,申请年
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日
- dwd_patent_cited(pn, cited_by_nums) — 专利被引次数
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_citation(id, citation_num) — 中文论文被引
- dwd_zh_author(paper_id, institution, affiliation) — 中文作者单位,地址国别
- dwd_en_author(paper_id, institution, affiliation) — 英文作者单位,地址国别
- dwd_scholar(scholar_id, scholar_org_name_zh, citation_nums) — 学者被引

## 待建字段

- 无

## 参考资料

[1]产业发展潜力综合评估｜国家统计局｜什么是研究与试验发展（R&D）经费及投入强度｜2025-03-21｜https://www.stats.gov.cn/zs/tjws/tjzb/202301/t20230101_1903948.html.

[2]产业发展潜力综合评估|固定资产投资增长率：株洲市产业振兴指标体系和评价方法研究｜株洲市统计局｜2024-08-06｜[湖南省统计局 - 株洲市产业振兴指标体系和评价方法研究](https://tjj.hunan.gov.cn/hntj/tjfx/sxfx/zzs/201507/t20150717_3802782.html).

[3]产业发展潜力综合评估｜国家统计局｜反映工业质量与效益的主要指标有哪些｜2025-03-20｜https://www.stats.gov.cn/zs/tjws/tjzb/202301/t20230101_1903942.html.
