# 区域创新要素类型综合评价模型（M_SYNTH_187_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SYNTH-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_187_1 |
| 指标名称 | 区域创新要素类型综合评价模型 |
| 一级模块 | 综合智能分析 |
| 二级模块 | 区域创新要素分析 |
| 三级模块 | 要素类型 |
| 更新频率 | 年度 |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q-SYNTH-02 / Q-SYNTH-E-01 |

## 口径定义

选定区域内、统计年度的区域创新要素类型指数，从创新人才、企业、政策、服务机构、科研机构、资金、空间七类要素配置水平合成，取值 0—100。分数越高表示要素类型配置越充分。

## 计算逻辑说明

**同M_SYNTH_ELEM_TYPE_INDEX-区域创新要素类型指数**

第一步：各指标标准化

各指标原始数据通过极值归一化法消除量纲，转换为 0—100 之间的标准化得分：
$$
指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij}为第 i个区域在第j个指标上的原始值，\min(x_j)和 \max(x_j)分别为该指标在所有区域中的最小值和最大值。
$$

第二步：各维度得分计算

各维度得分为其下各指标标准化得分的加权平均（可采用等权重，也可根据评估重点自行制定各指标权重）：
$$
创新人才得分=w_1 \times研发人员占比得分+ w_2 \times高学历人才占比得分
$$

$$
企业得分=w_4 \times企业注册数量得分+ w_5 \times科技型企业占比得分+ w_6 \times企业规模分布得分
$$

$$
政策得分=w_7 \times政策文件数量得分+ w_8 \times政策类型分布得分
$$

$$
服务机构得分= w_9 \times服务机构数量得分+ w_{10} \times服务机构类型数得分
$$

$$
科研机构得分=w_{11} \times科研机构数量得分+ w_{12} \times科研机构类型数得分+ w_{13} \times科研产出总量得分
$$

资金得分= w_{14} \times R&D经费投入规模得分 + w_{16} \times融资总额得分
$$
空间得分=w_{17} \times产业园区数量得分+ w_{18} \times创新空间面积得分+ w_{19} \times创新空间密度得分
$$

服务机构入集只用 `svc_org_card.service_type_candidate` 规则 A 六类（FINANCE/IP/HR/MKT/CONSULT/INNOV）。已删除财政科技支出占比。产业园区数量用机构名称弱代理；创新空间面积与密度仍待建。企业规模分布用 `dwd_org_base_info.org_size='大型'`。

第三步：区域创新要素类型指数综合得分

七个维度得分加权汇总（可采用等权重，各维度权重 = 1/7；也可根据评估重点自行制定各维度权重）：
$$
区域创新要素类型指数 = \sum_{k=1}^{7} W_k \times 维度得分_k
$$
其中，W_k为各维度权重，可采用等权重（各占约 14.3%），也可根据评估重点自行制定，\sum W = 1。得分越高，表明该区域的创新要素配置水平和发展能力越强。

| 维度         | 指标            | 指标说明                                                     | 计算方法                                                     | 源表字段                                                     | 待建字段                                                     |
| :----------- | :-------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **创新人才** | 研发人员占比    | 反映区域从业人员中研发人员的密度和创新人力资本投入强度。     | 研发人员数 ÷ 从业人员总数 × 100%                             | dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, development_employee, employees_number, total_assets, `arch development am`, pure_profit) — 营收,研发人员,从业人数,资产,研发投入,净利润；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无                                                           |
|              | 高学历人才占比  | 反映区域人才队伍的知识密集程度和高质量人才储备水平。         | 最高学历含硕/博的学者 ÷ 从业人员总数 × 100%                  | dwd_scholar_education_background(scholar_id, degree_zh, degree_en) — 最高学历；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 学者入集；dwd_org_annual_financial_info(org_id, year, employees_number, development_employee) — 从业人员；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集 | 无                                                           |
| **企业**     | 企业注册数量    | 反映区域创新主体的活跃度和新生企业增长趋势。                 | 统计年度内新注册企业总数                                     | dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无                                                           |
|              | 科技型企业占比  | 反映区域企业群体中创新主体的结构比例。                       | 科技型中小企业数 ÷ 全部企业数 × 100%                         | dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无                                                           |
|              | 企业规模分布    | 反映区域大、中、小型企业的合理梯次结构。                     | COUNT(org_size='大型') ÷ 存续企业数 × 100%                   | dwd_org_base_info(org_id, name_cn, city, province, area, org_size, org_type, reg_status, incorporation_year) — 区域入集,机构规模,存续,成立年 | 无                                                           |
| **政策**     | 政策文件数量    | 反映区域产业创新政策的供给规模和丰富程度。                   | 统计年度内出台的产业创新相关政策文件总数                     | dwd_policy_base(id, city, status, expire_date, type, theme, publish_year, rank) — 有效政策去重,城市,类型,主题,级别 | 无                                                           |
|              | 政策类型覆盖率  | 反映政策体系在财政、土地、人才、金融等维度的覆盖完整程度。   | 实际覆盖的政策类型数 ÷ 应覆盖的政策类型总数 × 100%           | dwd_policy_base(id, city, status, expire_date, type, theme, publish_year, rank) — 有效政策去重,城市,类型,主题,级别 | 无                                                           |
| **服务机构** | 服务机构数量    | 反映区域创新服务体系的总体规模和供给能力。                   | svc_org_card中service_type_candidate∈{FINANCE,IP,HR,MKT,CONSULT,INNOV}且落入本区域的机构去重数 | demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, service_type_candidate) — 服务机构清单,规则A六类；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集 | 无                                                           |
|              | 服务机构类型数  | 反映科技孵化器、技术转移中心、知识产权服务等机构类型的完备程度。 | 本区域实际出现的service_type_candidate去重数（金融服务/知识产权/人力资源/市场营销/咨询/科技创新） | demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, service_type_candidate) — 服务机构清单,规则A六类；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集 | 无                                                           |
| **科研机构** | 科研机构数量    | 反映区域基础研究和应用研究的机构支撑水平。                   | 统计区域内高校、科研院所、重点实验室等机构总数               | dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构入集；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无                                                           |
|              | 科研机构类型数  | 反映高等院校、科研院所、企业研发中心等机构类型的完备程度。   | 统计实际覆盖的科研机构类型数量                               | dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构入集；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无                                                           |
|              | 科研产出总量    | 反映科研机构的成果产出规模。                                 | 统计年度内论文、专利、获奖等成果总数                         | dwd_patent(pn, kind, granted_number, first_applicant_name, applicants, pbdt_year, apdt_year) — 专利去重,发明授权,申请人对齐,联合申请人,年窗；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,区域对齐；dwd_en_author(paper_id, institution) — 英文作者单位,区域对齐；dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构入集；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无                                                           |
| **资金**     | R&D经费投入规模 | 反映区域研发活动的资金投入总量。                             | 统计年度内R&D经费内部支出总额                                | dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, development_employee, employees_number, total_assets, `arch development am`, pure_profit) — 营收,研发人员,从业人数,资产,研发投入,净利润；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount, operating_revenue) — 上市研发,营收；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无                                                           |
|              | 融资总额        | 反映区域创新企业的资本获得能力和市场认可度。                 | 统计年度内区域内企业获得的风险投资、股权融资等总额           | dwd_org_financing_info(org_id, funding_amount, completion_date) — 融资额,融资时点；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无                                                           |
| **空间**     | 产业园区数量    | 反映区域产业载体的空间供给水平。                             | org_type或name_cn含园区、高新区、众创、孵化、特色产业基地的存续机构去重数（弱代理） | dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,机构类型,名称 | 无                                                           |
|              | 创新空间面积    | 反映区域内用于创新活动的物理空间规模。                       | 统计科技园区、孵化器、众创空间等总面积                       | dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | innovation_space_area-创新载体/园区面积                      |
|              | 创新空间密度    | 反映区域创新空间分布的集中程度。                             | 创新空间面积 ÷ 区域总面积 × 100%                             | dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | innovation_space_area-创新载体/园区面积；regional_area-区域总面积 |


第五步：结构分析与优势短板识别

将各维度得分进行横向比较，计算各维度与平均水平的偏离程度，识别区域在七大创新要素中的相对强弱——得分高于区域均值的维度为优势领域，低于区域均值的维度为薄弱环节。对得分偏低的短板维度，进一步拆解其内部各指标的得分情况，定位具体短板指标（如资金维度偏低时，需分析R&D经费投入规模、融资总额中哪个指标拖累），为精准施策提供依据。

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, org_size, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,机构规模,存续,成立年
- dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, development_employee, employees_number, total_assets, `arch development am`, pure_profit) — 营收,研发人员,从业人数,资产,研发投入,净利润
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount, operating_revenue) — 上市研发,营收
- dwd_patent(pn, kind, granted_number, first_applicant_name, applicants, pbdt_year, apdt_year) — 专利去重,发明授权,申请人对齐,联合申请人,年窗
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,区域对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,区域对齐
- dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签
- dwd_policy_base(id, city, status, expire_date, type, theme, publish_year, rank) — 有效政策去重,城市,类型,主题,级别
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id, paper_nums, h_index) — 学者存量,所属机构,成果量
- dwd_scholar_education_background(scholar_id, degree_zh, degree_en) — 最高学历
- demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, service_type_candidate) — 服务机构清单,规则A六类
- dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构入集
- dwd_org_financing_info(org_id, funding_amount, completion_date) — 融资额,融资时点

## 待建字段

- innovation_space_area-创新载体/园区面积
- regional_area-区域总面积
