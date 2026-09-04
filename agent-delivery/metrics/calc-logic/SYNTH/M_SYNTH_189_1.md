# 区域创新要素领域综合评价模型（M_SYNTH_189_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SYNTH-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_189_1 |
| 指标名称 | 区域创新要素领域综合评价模型 |
| 一级模块 | 综合智能分析 |
| 二级模块 | 区域创新要素分析 |
| 三级模块 | 要素领域 |
| 更新频率 | 年度 |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q-SYNTH-02 / Q-SYNTH-E-01 |

## 口径定义

选定区域内、统计年度的区域创新要素领域指数，从产业领域覆盖广度、技术领域应用深度、创新产出强度、人才结构合理性、经济贡献度五个维度合成，取值 0—100。分数越高表示创新要素在各领域的综合发展水平越高。

## 计算逻辑说明

**同M_SYNTH_ELEM_DOMAIN_INDEX 区域创新要素领域指数**

第一步：各指标标准化

各指标原始数据通过极值归一化法消除量纲，转换为 0—100 之间的标准化得分：
$$
指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij}为第 i个区域在第j个指标上的原始值，\min(x_j)和 \max(x_j)分别为该指标在所有区域中的最小值和最大值。
$$

第二步：各维度得分计算

各维度得分为其下两个指标标准化得分的加权平均（可采用等权重，也可根据评估重点自行制定各指标权重）：
$$
产业领域覆盖广度得分= w_1 \times高新技术企业数得分+ w_2 \times规上工业增加值得分
$$

$$
技术领域应用深度得分= w_3 \times每万从业人员发明专利授权数得分+ w_4 \times研发经费投入强度得分
$$

$$
创新产出强度得分= w_5 \times专利授权量得分+ w_6 \times专利转移件数得分
$$

$$
人才结构合理性得分= w_7 \times研发人员占比得分+ w_8 \times高学历人才占比得分
$$

$$
经济贡献度得分=w_9 \times全员劳动生产率得分+ w_{10} \times高技术产业营业收入占比得分
$$

宏观取数：`dwd_macro_index_data`，`is_deleted=0`，`dim_cal=JDZ`，`dim_dur=DNLJ`，按 12 位 `area_code` 与统计年对齐；深圳=`440300000000`。地区生产总值=`gmjj_jjzl_01`。规上工业增加值=`gmjj_jjzl_01_02_01_01`（字典名「按规模分:规上工业企业增加值」）。高学历与类型/层次指数对齐：学者学历表硕/博，不用从业人员本科。每万从业人员发明专利的分母、全员劳动生产率的分母均为年报 `employees_number` 合计，不是官方人口或就业人员。专利转移件数按 `pn` 去重、按转移生效年入窗，不是技术合同成交额。

第三步：区域创新要素领域指数综合得分

五个维度得分加权汇总（可采用等权重，各维度权重 = 1/5；也可根据评估重点自行制定各维度权重）：
$$
区域创新要素领域指数 = \sum_{k=1}^{5} W_k \times 维度得分_k
$$
其中，各维度权重可采用等权重（各占 20%），也可根据评估重点自行制定，\sum W = 1。得分越高，表明该区域的创新要素在各领域的综合发展水平越高。

| 维度                 | 指标                       | 指标说明                                                     | 计算方法                                                     | 源表字段                                                     | 待建字段 |
| :------------------- | :------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | ------------------------------------------------------------ | -------- |
| **产业领域覆盖广度** | 高新技术企业数             | 反映区域内高新技术产业的覆盖规模和广度。                     | 统计区域内有效期内的高新技术企业总数                         | dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无       |
|                      | 规上工业增加值             | 反映区域内规模以上工业的产出规模。                           | 直接取 gmjj_jjzl_01_02_01_01 绝对值，当年累计                | dwd_macro_index_data(index_code, occur_period, area_code, dim_cal, dim_dur, index_value, unit_use) — 宏观事实,按12位area_code与统计年取数；dwd_dim_index_attribute(index_code, index_name, data_freq) — 指标字典；dwd_dim_admin_area(area_code, area_name) — 行政区划,深圳=440300000000；dwd_dim_index_cal(dim_cal, cal_name) — 计量口径；dwd_dim_index_dur(dim_dur, dur_name) — 时间跨度；dwd_dim_source_code(source_code, source_name) — 数据来源；index_code=gmjj_jjzl_01_02_01_01 — 按规模分:规上工业企业增加值 | 无       |
| **技术领域应用深度** | 每万从业人员发明专利授权数 | 反映区域内按从业人员计的发明授权密度。                       | 发明专利授权数 ÷ 年报从业人员合计（万人）                    | dwd_patent(pn, kind, granted_number, first_applicant_name, applicants, pbdt_year, apdt_year) — 专利去重,发明授权,申请人对齐,联合申请人,年窗；dwd_org_annual_financial_info(org_id, year, employees_number) — 年报从业人数；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无       |
|                      | 研发经费投入强度           | 反映区域对技术研发的投入力度，体现技术领域应用的支撑强度。   | 企业年报/上市研发投入合计 ÷ 地区生产总值(gmjj_jjzl_01) × 100% | dwd_org_annual_financial_info(org_id, year, `arch development am`) — 研发投入；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年；dwd_macro_index_data(index_code, occur_period, area_code, dim_cal, dim_dur, index_value, unit_use) — 宏观事实,按12位area_code与统计年取数；dwd_dim_index_attribute(index_code, index_name, data_freq) — 指标字典；dwd_dim_admin_area(area_code, area_name) — 行政区划,深圳=440300000000；dwd_dim_index_cal(dim_cal, cal_name) — 计量口径；dwd_dim_index_dur(dim_dur, dur_name) — 时间跨度；dwd_dim_source_code(source_code, source_name) — 数据来源；index_code=gmjj_jjzl_01 — 地区生产总值 | 无       |
| **创新产出强度**     | 专利授权量                 | 反映区域技术成果的产出规模和技术积累水平。                   | 统计年度内发明专利、实用新型专利、外观设计专利授权总量       | dwd_patent(pn, kind, granted_number, first_applicant_name, applicants, pbdt_year, apdt_year) — 专利去重,发明授权,申请人对齐,联合申请人,年窗；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无       |
|                      | 专利转移件数               | 反映区域技术成果转移活跃度。按件计数，不是成交额。           | 统计年度内专利转移去重件数                                   | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效年窗；dwd_patent(pn, kind, granted_number, first_applicant_name, applicants, pbdt_year) — 申请人对齐；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无       |
| **人才结构合理性**   | 研发人员占比               | 反映区域从业人员中研发人员的密度，体现人才结构的创新导向。   | 研发人员数 ÷ 从业人员总数 × 100%                             | dwd_org_annual_financial_info(org_id, year, development_employee, employees_number) — 研发人员,从业人数；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无       |
|                      | 高学历人才占比             | 与类型/层次指数对齐：学者最高学历含硕/博的占比。             | 最高学历含硕/博的学者 ÷ 从业人员总数 × 100%                  | dwd_scholar_education_background(scholar_id, degree_zh, degree_en) — 最高学历；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 学者入集；dwd_org_annual_financial_info(org_id, year, employees_number) — 从业人员；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集 | 无       |
| **经济贡献度**       | 全员劳动生产率             | 反映区域产出效率。分母为企业年报从业人数，不是官方就业人员。 | 地区生产总值(gmjj_jjzl_01) ÷ 年报从业人员合计                | dwd_macro_index_data(index_code, occur_period, area_code, dim_cal, dim_dur, index_value, unit_use) — 宏观事实,按12位area_code与统计年取数；dwd_dim_index_attribute(index_code, index_name, data_freq) — 指标字典；dwd_dim_admin_area(area_code, area_name) — 行政区划,深圳=440300000000；dwd_dim_index_cal(dim_cal, cal_name) — 计量口径；dwd_dim_index_dur(dim_dur, dur_name) — 时间跨度；dwd_dim_source_code(source_code, source_name) — 数据来源；index_code=gmjj_jjzl_01 — 地区生产总值；dwd_org_annual_financial_info(org_id, year, employees_number) — 年报从业人数；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无       |
|                      | 高技术产业营业收入占比     | 反映高技术产业对区域经济的贡献程度。                         | 高技术产业营业收入 ÷ 规模以上工业企业营业收入 × 100%         | dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签；dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, development_employee, employees_number, total_assets, `arch development am`, pure_profit) — 营收,研发人员,从业人数,资产,研发投入,净利润；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年 | 无       |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,存续,成立年
- dwd_org_annual_financial_info(org_id, year, operating_revenue, development_employee, employees_number, `arch development am`) — 营收,研发人员,从业人数,研发投入
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发
- dwd_patent(pn, kind, granted_number, first_applicant_name, applicants, pbdt_year, apdt_year) — 专利去重,发明授权,申请人对齐,联合申请人,年窗
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效年窗
- dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 学者入集,所属机构
- dwd_scholar_education_background(scholar_id, degree_zh, degree_en) — 最高学历
- dwd_macro_index_data(index_code, occur_period, area_code, dim_cal, dim_dur, index_value, unit_use) — 宏观指标事实
- dwd_dim_index_attribute(index_code, index_name, data_freq, unit_use) — 指标字典
- dwd_dim_admin_area(area_code, area_name) — 行政区划,深圳=440300000000
- dwd_dim_index_cal(dim_cal, cal_name) — 计量口径
- dwd_dim_index_dur(dim_dur, dur_name) — 时间跨度
- dwd_dim_source_code(source_code, source_name) — 数据来源

## 待建字段

无
