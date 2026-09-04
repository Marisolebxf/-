# 区域创新活力指数（M_SYNTH_VIT_INDEX）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SYNTH-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_VIT_INDEX |
| 指标名称 | 区域创新活力指数 |
| 一级模块 | 综合智能分析 |
| 二级模块 | 区域创新活力分析 |
| 三级模块 | 综合评价模型 |
| 更新频率 | 年度 |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q-SYNTH-01 / Q-SYNTH-V-01 |

## 口径定义

选定区域内、统计年度的区域创新活力综合指数，从科技、产业、人才、政策四维评定，取值 0—100。分数越高表示区域创新动能越强。

## 计算逻辑说明

第一步：各指标标准化

各指标原始数据通过极值归一化法消除量纲，转换为 0—100 之间的标准化得分：
$$
指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij}为第 i个区域在第 j个指标上的原始值，\min(x_j)和 \max(x_j)分别为该指标在所有区域中的最小值和最大值。
$$

第二步：各维度得分计算

各维度得分为其下各指标标准化得分的加权平均（可采用等权重，也可根据评估重点自行制定各指标权重）：

科技维度得分=（专利授权量得分 + 高质量论文数量得分 + 技术转化成效得分）÷ 3
产业维度得分=（高新技术企业数量得分 + 新产品销售收入占比得分 + 创新服务机构绩效得分）÷ 3
人才维度得分=（研发人员数量得分 + 高学历人才占比得分 + 人才成果产出得分）÷ 3
政策维度得分=（产业创新政策数量得分 + 政策类型覆盖度得分 + 政策实施效果指数得分）÷ 3

深圳宏观取 `area_code='440300000000'`。名称对得上的才挂宏观，对不上的不编造替代。

- 高质量论文：被引 ≥ 本批 P70。
- 技术转化成效：专利转移去重数 ÷ 研发投入合计。
- 新产品销售收入占比：规上工业R&D新产品销售收入(a77234) ÷ 区域企业主营业务收入合计 × 100%。a77234为只覆盖进入 R&D 统计的规上工业。
- 创新服务机构绩效：沿用产业服务 `M_SVC_ORG_COVERAGE_DEPTH`。入集 `svc_org_card.service_type_candidate=INNOV`，机构得分=服务广度与服务深度等权，区域绩效=区域内机构得分均值。
- 高学历人才占比：`dwd_scholar_education_background.degree_zh` / `degree_en` 判定硕博。
- 政策实施效果：政策分析 V2 无兑现资金台账。沿用 `M_POLICY_DS_07_POLICY_GUARD_008` 的「政策实施效果」：实施时效性与政策可见度等权。是实施周期/公开渠道完备率，不是资金兑付率。

第三步：区域创新能力指数综合得分

四个维度得分加权汇总（可采用等权重，各维度权重 = 1/4；也可根据评估重点自行制定各维度权重）：
$$
区域创新能力指数 = \sum_{k=1}^{4} W_k \times 维度得分_k
$$
其中，W_k为各维度权重，可采用等权重（各占 25%），也可根据评估重点自行制定，\sum W = 1。得分越高，表明该区域的综合创新能力越强。

区域创新能力指标体系

| 一级维度 | 二级指标 | 指标说明 | 计算方法 | 源表字段 | 待建字段 |
| :------- | :------- | :------- | :------- | -------- | -------- |
| **科技** | 专利授权量 | 反映区域的创新产出规模和技术成果积累水平。 | 统计年度内发明专利、实用新型专利、外观设计专利授权总量 | dwd_patent(pn, kind, granted_number, first_applicant_name, applicants, pbdt_year, apdt_year) — 专利去重,发明授权,申请人对齐,联合申请人,年窗；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无 |
|  | 高质量论文数量 | 反映区域的基础研究和前沿探索能力。 | 统计年度内被引≥本批P70的论文去重数 | dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,区域对齐；dwd_en_author(paper_id, institution) — 英文作者单位,区域对齐；dwd_zh_paper_citation(id, citation_num) — 中文被引；dwd_en_paper_reference(id, citation_count) — 英文被引；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无 |
|  | 技术转化成效 | 反映研发投入转化为技术成果的效率。 | 专利转移去重数 ÷ 研发投入合计 | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移；dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, development_employee, employees_number, total_assets, `arch development am`, pure_profit) — 营收,研发人员,从业人数,资产,研发投入,净利润；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount, operating_revenue) — 上市研发,营收；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无 |
| **产业** | 高新技术企业数量 | 反映区域创新主体的规模和高新技术产业发展水平。 | 统计年度内经认定的国家级高新技术企业总数 | dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无 |
|  | 新产品销售收入占比 | 反映企业创新成果的市场化应用效果。 | 规上工业R&D新产品销售收入(a77234) ÷ 区域企业主营业务收入合计 × 100% | dwd_macro_index_data(index_code, occur_period, area_code, dim_cal, dim_dur, index_value, unit_use) — 宏观事实,按12位area_code与统计年取数；dwd_dim_index_attribute(index_code, index_name, data_freq) — 指标字典；dwd_dim_admin_area(area_code, area_name) — 行政区划,深圳=440300000000；dwd_dim_index_cal(dim_cal, cal_name) — 计量口径；dwd_dim_index_dur(dim_dur, dur_name) — 时间跨度；dwd_dim_source_code(source_code, source_name) — 数据来源；index_code=a77234 — 规上工业研究与试验发展(R&D)新产品销售收入；dwd_org_annual_financial_info(org_id, year, main_business_revenue) — 企业产品销售收入分母；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无 |
|  | 创新服务机构绩效 | 反映区域创新服务体系覆盖能力。沿用产业服务 M_SVC_ORG_COVERAGE_DEPTH。 | 区域内科技创新服务机构覆盖得分均值；机构得分=(服务广度_z+服务深度_z)/2 | demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, service_type_candidate) — 科技创新服务机构,INNOV；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, external_id) — 区域入集,信用代码对齐；dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 覆盖产业领域,覆盖环节；dwd_industry_chain_info(industry_code, industry_link_code) — 标准产业领域,标准环节 | 无 |
| **人才** | 研发人员数量 | 反映区域创新人力资本的投入规模。 | 统计年度内从事R&D活动的人员总数 | dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, development_employee, employees_number, total_assets, `arch development am`, pure_profit) — 营收,研发人员,从业人数,资产,研发投入,净利润；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无 |
|  | 高学历人才占比 | 反映区域人才队伍的知识密集程度。宏观库无区域学历结构。 | 最高学历含硕/博的学者 ÷ 从业人员总数 × 100% | dwd_scholar_education_background(scholar_id, degree_zh, degree_en) — 最高学历；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id, paper_nums, h_index) — 学者存量,所属机构,成果量；dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, development_employee, employees_number, total_assets, `arch development am`, pure_profit) — 营收,研发人员,从业人数,资产,研发投入,净利润；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无 |
|  | 人才成果产出 | 反映人才队伍的人均创新产出效率和实际贡献。 | 人均专利/论文产出指数 =（专利授权数 + 论文发表数）÷ 研发人员总数 | dwd_patent(pn, kind, granted_number, first_applicant_name, applicants, pbdt_year, apdt_year) — 专利去重,发明授权,申请人对齐,联合申请人,年窗；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,区域对齐；dwd_en_author(paper_id, institution) — 英文作者单位,区域对齐；dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, development_employee, employees_number, total_assets, `arch development am`, pure_profit) — 营收,研发人员,从业人数,资产,研发投入,净利润；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id, paper_nums, h_index) — 学者存量,所属机构,成果量；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无 |
| **政策** | 产业创新政策数量 | 反映区域产业创新政策的供给规模和丰富程度。 | 统计年度内出台的产业创新相关政策文件总数 | dwd_policy_base(id, city, status, expire_date, type, theme, publish_year, rank) — 有效政策去重,城市,类型,主题,级别 | 无 |
|  | 政策类型覆盖度 | 反映政策体系对财政、土地、人才、金融等多维度的覆盖完整程度。 | 实际覆盖的政策类型数（财政/土地/人才/金融等）÷ 应覆盖的政策类型总数 × 100% | dwd_policy_base(id, city, status, expire_date, type, theme, publish_year, rank) — 有效政策去重,城市,类型,主题,级别 | 无 |
|  | 政策实施效果指数 | 从实施时效性、 政策可见度评估。沿用政策分析 M_POLICY_DS_07_POLICY_GUARD_008 政策实施效果。 | (实施时效性 + 政策可见度)/2；实施时效性=当前日在实施日与失效日之间的政策数/政策总数；政策可见度=link非空政策数/政策总数 | dwd_policy_base(id, city, status, expire_date, implementation_date, link, type, theme, publish_year, rank) — 有效政策,实施日,失效日,公开链接 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年
- dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, development_employee, employees_number, total_assets, `arch development am`, pure_profit) — 营收,研发人员,从业人数,资产,研发投入,净利润
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount, operating_revenue) — 上市研发,营收
- dwd_patent(pn, kind, granted_number, first_applicant_name, applicants, pbdt_year, apdt_year) — 专利去重,发明授权,申请人对齐,联合申请人,年窗
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,区域对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,区域对齐
- dwd_zh_paper_citation(id, citation_num) — 中文被引
- dwd_en_paper_reference(id, citation_count) — 英文被引
- dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签
- dwd_policy_base(id, city, status, expire_date, implementation_date, link, type, theme, publish_year, rank) — 有效政策去重,城市,实施日,失效日,公开链接,类型,主题,级别
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id, paper_nums, h_index) — 学者存量,所属机构,成果量
- dwd_scholar_education_background(scholar_id, degree_zh, degree_en) — 最高学历
- demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, service_type_candidate) — 科技创新服务机构,INNOV
- dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 覆盖产业领域,覆盖环节
- dwd_industry_chain_info(industry_code, industry_link_code) — 标准产业领域,标准环节
- dwd_macro_index_data(index_code, occur_period, area_code, dim_cal, dim_dur, index_value, unit_use) — 宏观指标事实
- dwd_dim_index_attribute(index_code, index_name, data_freq, unit_use) — 指标字典
- dwd_dim_admin_area(area_code, area_name, parent_code) — 行政区划,深圳=440300000000
- dwd_dim_index_cal(dim_cal, cal_name) — 计量口径
- dwd_dim_index_dur(dim_dur, dur_name) — 时间跨度
- dwd_dim_source_code(source_code, source_name) — 数据来源

## 待建字段

