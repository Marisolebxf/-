# 区域产业竞争力指数（M_CHAIN_COMPETITIVENESS_INDEX）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_COMPETITIVENESS_INDEX |
| 指标名称 | 区域产业竞争力指数 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业竞争力评价 |
| 三级模块 | 竞争力指数 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q055+QC05 |


## 口径定义

区域产业竞争力评估的综合指数，满分0—100分，综合反映企业能力、学术生态、配套环境三个维度的综合水平。

## 计算逻辑说明

采用加权平均。三维：企业能力/学术生态/配套环境。权重与归一化口径待甲方确认。

第一步：各三级指标标准化

各指标原始数据通过极值归一化法消除量纲，转换为 0—100 之间的标准化得分：
$$
正向指标（数值越大越好）：指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij}为区域 i 在第 j 个指标上的原始值，\min(x_j) 和 \max(x_j) 分别为该指标在所有区域中的最小值和最大值。
$$

第二步：各维度得分计算

将各维度下三级指标的标准化得分加权求和（可采用等权重，也可根据实际情况自行制定各指标权重）：
$$
企业能力_i = w_1 \times 人均产值得分 + w_2 \times 研发投入强度得分 + w_3 \times 有效专利数量得分
$$

$$
学术生态_i = w_4 \times 论文产出得分 + w_5 \times 人才储备得分 + w_6 \times 科研机构得分
$$

$$
配套环境_i = w_7 \times 政府覆盖率得分 + w_8 \times 融资事件得分
$$

其中，各维度内三级指标权重可采用等权重（各占 1/3 或 1/2），也可根据研究需要自行制定。

第三步：区域产业竞争力指数综合得分
$$
区域产业竞争力指数_i = W_1 \times 企业能力_i + W_2 \times 学术生态_i + W_3 \times 配套环境_i
$$

$$
其中，W_1、W_2、W_3 为各一级维度权重，可采用等权重（各占 1/3），也可根据研究需要自行制定，i 为区域编号。最终得分越高，表明该区域的产业竞争力越强。
$$

### 区域产业竞争力指数指标体系

| 一级维度     | 三级指标             | 计算方式/测度方法                                       | 源表字段 | 待建字段 |
| :----------- | :------------------- | :------------------------------------------------------ | -------- | -------- |
| **企业能力** | 人均产值             | 人均产值 = 总产值（或营业收入）÷ 企业平均人数           | dwd_org_annual_financial_info(operating_revenue, employees_number) | 无 |
|              | 研发投入强度         | 研发投入强度 = R&D经费 ÷ 营业收入 × 100%                | dwd_org_stock_finance_info(research_development_amount, operating_revenue) | 无 |
|              | 有效专利数量         | 区域在指定产业链上，企业作为第一专利权人拥有的有效发明专利总量 | dwd_patent(patent_id, first_current_assignee_name, kind, granted_number); dwd_patent_legal(status, expiration_year) | 无 |
| **学术生态** | 论文产出     | 区域在指定产业链上，链上高校与科研机构所属学者在统计年及以前发表论文的去重件数。 | dwd_scholar(scholar_id, scholar_org_name_zh); dwd_scholar_paper_relation(scholar_id, paper_id, year); dwd_scholar_papers(id, status); dwd_org_heis_info(name_cn, city); dwd_research_institute_base_info(name_cn, city) | 无 |
|              | 人才储备     | 区域在指定产业链上，链上高校与科研机构所属学者的去重人数。   | dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh); dwd_org_heis_info(name_cn, city); dwd_research_institute_base_info(name_cn, city) | 无 |
| | 科研机构     | 区域在指定产业链上，高校与科研机构的去重数量。               | dwd_org_heis_info(org_id, external_id, name_cn, city); dwd_research_institute_base_info(org_id, external_id, name_cn, city); dwd_org_industry_tags(credit_code) | 无 |
| **配套环境** | 政策覆盖率   | 区域在指定产业链上，相关政策覆盖环节占全链环节数的比例。     | dwd_industry_chain_info(industry_link_code, industry_link_name); dwd_policy_base(id, title, keywords, keypoints, theme, city, status) | 无 |
|              | 融资事件     | 区域在指定产业链上，链上企业融资事件的去重件数。             | dwd_org_financing_info(org_id, external_id, completion_date); dwd_org_industry_tags(credit_code); dwd_org_base_info(city) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 目标产业链范围, 产业链名称, 全链环节去重, 环节名称匹配政策
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业/机构筛选, 信用代码关联, 名称匹配
- dwd_org_base_info(external_id, city) — 企业信用代码关联, 区域城市筛选
- dwd_org_annual_financial_info(external_id, year, operating_revenue, employees_number) — 人均产值用营业收入与从业人数
- dwd_org_stock_finance_info(external_id, occur_period, operating_revenue, research_development_amount) — 研发投入强度
- dwd_patent(patent_id, first_current_assignee_name, kind, granted_number) — 有效发明专利去重, 第一专利权人, 发明识别, 授权判定
- dwd_patent_legal(pn, status, expiration_year) — 专利法律状态(有效), 到期年
- dwd_org_heis_info(org_id, external_id, name_cn, city) — 高校去重, 信用代码关联, 机构名称匹配学者, 区域筛选
- dwd_research_institute_base_info(org_id, external_id, name_cn, city) — 科研机构去重, 信用代码关联, 机构名称匹配学者, 区域筛选
- dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh) — 学者去重(人才储备), 所属机构关联
- dwd_scholar_paper_relation(scholar_id, paper_id, year) — 学者论文关联, 论文去重, 发表年
- dwd_scholar_papers(id, status) — 论文去重, 有效状态
- dwd_policy_base(id, title, keywords, keypoints, theme, city, status) — 政策去重, 标题/关键词/要点/主题匹配环节, 区域, 有效状态
- dwd_org_financing_info(org_id, external_id, completion_date) — 融资事件去重, 信用代码关联链上企业, 融资时间

## 待建字段

- 无

## 参考文献

[1] 区域产业竞争力指数 | 同济大学  | 周文泳. 衡量产业创新生态的四把尺子[J]. 同济大学学报（社会科学版）, 2016. https://news.tongji.edu.cn/info/1007/11760.htm.

[2] 区域产业竞争力指数 | 浙江大学 | 范钧. 区域软环境对企业竞争力的作用机制及其评价体系[J]. 科研管理, 2007, 28(2): 99-104. DOI: 10.3969/j.issn.1000-2995.2007.02.015.

[3]区域产业竞争力指数 | 陈宗映， 韩伟亚 | 成渝“双圈”工业竞争力动态演变及特征[J]. 当代县域经济， 2025(7). [https://www.ddxyjjzz.com](https://www.ddxyjjzz.com/).
