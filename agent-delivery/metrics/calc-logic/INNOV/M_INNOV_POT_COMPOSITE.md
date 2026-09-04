# 产业发展潜力综合评估（M_INNOV_POT_COMPOSITE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_POT_COMPOSITE |
| 指标名称 | 产业发展潜力综合评估 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

将投入、成熟度、产值、科学影响力、技术影响力按自定义权重计算的产业发展潜力综合得分与排名。对象=选定产业，取值 0—100，分数越高发展潜力越大。

## 计算逻辑说明

选定产业入集。采用加权平均，五维：产业投入（研发投入强度/固投增长率/人才投入强度） / 技术产品成熟度（授权比例/发明占比/市场渗透） / 产业产值（总产值/利润总额） / 科学影响力（论文被引/国际合作） / 技术影响力（专利被引/同族规模）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 产业投入 |  | 从研发投入强度、固定资产投资增长率和人才投入强度评估产业投入。 | 维内三项极值归一后等权。 | dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount, operating_revenue, fixed_assets) — 上市研发,营收,固定资产；dwd_org_annual_financial_info(org_id, year, fixed_assets, development_employee, employees_number) — 年报固定资产,研发人员,从业人数 |
| 产业投入 | 研发投入强度 | 产业研发投入占营业收入比。 | SUM(research_development_amount) ÷ SUM(operating_revenue) × 100% | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount, operating_revenue) — 上市研发投入,营业收入；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |
| 产业投入 | 固定资产投资增长率 | 产业固定资产同比增速。 | （本期固定资产 − 上期固定资产）÷ 上期固定资产 × 100% | dwd_org_annual_financial_info(org_id, year, fixed_assets) — 年报固定资产,年；dwd_org_stock_finance_info(org_id, occur_period, fixed_assets) — 上市固定资产；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |
| 产业投入 | 人才投入强度 | 产业研发人员占从业人员比。 | SUM(development_employee) ÷ SUM(employees_number) × 100% | dwd_org_annual_financial_info(org_id, year, development_employee, employees_number) — 研发人员,从业人数；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |
| 技术产品成熟度 |  | 从授权比例、发明占比、市场渗透评估技术产品成熟度。 | 维内三项极值归一后等权。与 M_INNOV_POT_MATURITY 同一三维，按产业汇总。 | dwd_patent(pn, kind, granted_number, first_applicant_name, apdt_year) — 专利去重,申请类型,授权号,申请人对齐,申请年；dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |
| 技术产品成熟度 | 授权比例 | 授权专利占全部专利比。 | 授权专利数 / 专利数 | dwd_patent(pn, first_applicant_name, granted_number, apdt_year) — 申请人对齐,授权号,申请年；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |
| 技术产品成熟度 | 发明占比 | 发明专利占全部专利比。 | 发明专利数 / 专利数 | dwd_patent(pn, first_applicant_name, kind, apdt_year) — 申请人对齐,申请类型,申请年；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |
| 技术产品成熟度 | 市场渗透 | 发生转移的专利占比。 | 转移专利数 / 专利数 | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_patent(pn, first_applicant_name, apdt_year) — 专利分母,申请人对齐；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |
| 产业产值 |  | 从总产值和利润总额评估产业产值。 | 维内两项极值归一后等权。 | dwd_org_annual_financial_info(org_id, year, main_business_revenue, operating_revenue, total_profit) — 年报主营,营收,利润；dwd_org_stock_finance_info(org_id, occur_period, main_business_revenue, operating_revenue, total_profit) — 上市主营,营收,利润；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |
| 产业产值 | 总产值 | 产业主营业务收入（空则用营业收入）合计。 | SUM(main_business_revenue)；空则用 operating_revenue | dwd_org_annual_financial_info(org_id, year, main_business_revenue, operating_revenue) — 年报主营,营收；dwd_org_stock_finance_info(org_id, occur_period, main_business_revenue, operating_revenue) — 上市主营,营收；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |
| 产业产值 | 利润总额 | 产业利润总额合计。 | SUM(total_profit) | dwd_org_annual_financial_info(org_id, year, total_profit) — 年报利润总额；dwd_org_stock_finance_info(org_id, occur_period, total_profit) — 上市利润总额；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |
| 科学影响力 |  | 从论文被引次数和国际合作论文比例评估科学影响力。 | 维内两项极值归一后等权。与 M_INNOV_POT_SCI_INFL 同一二维。 | dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_citation(id, citation_num) — 中文论文被引；dwd_zh_author(paper_id, institution, affiliation) — 中文作者单位,地址国别；dwd_en_author(paper_id, institution, affiliation) — 英文作者单位,地址国别；dwd_scholar(scholar_id, scholar_org_name_zh, citation_nums) — 学者被引 |
| 科学影响力 | 论文被引次数 | 产业相关论文被引合计。 | SUM(citation_num) | dwd_zh_paper_citation(id, citation_num) — 中文论文被引；dwd_scholar(scholar_id, scholar_org_name_zh, citation_nums) — 学者被引；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |
| 科学影响力 | 国际合作论文比例 | 作者地址跨两个及以上国家的论文占比。 | 国际合作论文数 / 论文数 | dwd_zh_author(paper_id, institution, affiliation) — 中文作者单位,地址国别；dwd_en_author(paper_id, institution, affiliation) — 英文作者单位,地址国别；dwd_zh_paper(id, cover_year_start) — 中文论文分母,发表年；dwd_en_paper(id, cover_year_start) — 英文论文分母,发表年；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |
| 技术影响力 |  | 从专利被引次数和同族规模评估技术影响力。 | 维内两项极值归一后等权。与 M_INNOV_POT_TECH_INFL 同一二维。 | dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签；dwd_patent(pn, first_applicant_name, other_Versions, apdt_year) — 专利去重,申请人对齐,同族,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数 |
| 技术影响力 | 专利被引次数 | 产业相关专利被其他专利引用的总次数。 | SUM(cited_by_nums) | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |
| 技术影响力 | 同族规模 | 产业专利海外布局广度，用同族成员数均值衡量。 | 同族成员数合计 / 专利数 | dwd_patent(pn, first_applicant_name, other_Versions, apdt_year) — 同族专利,申请人对齐,申请年；dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签 |

## 源表字段

dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount, operating_revenue, main_business_revenue, total_profit, fixed_assets) — 上市研发,营收,主营,利润,固定资产；dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, total_profit, fixed_assets, development_employee, employees_number) — 年报营收,主营,利润,固定资产,研发人员,从业人数；dwd_patent(pn, kind, granted_number, first_applicant_name, other_Versions, apdt_year) — 专利去重,申请类型,授权号,申请人对齐,同族,申请年；dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_citation(id, citation_num) — 中文论文被引；dwd_zh_author(paper_id, institution, affiliation) — 中文作者单位,地址国别；dwd_en_author(paper_id, institution, affiliation) — 英文作者单位,地址国别；dwd_scholar(scholar_id, scholar_org_name_zh, citation_nums) — 学者被引

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|科技创新评估.md|序号 151「将产业发展潜力的各项指标进行综合展示，用户可自定义指标权重，支持根据权重计算综合得分，提供产业发展潜力的综合评估结果和排名」。二级来自 seq 146-150（投入/成熟度/产值/科学影响力/技术影响力）。对照 183：成果三维≠本页潜力五项，对不上。禁止伪 mapped 183。
