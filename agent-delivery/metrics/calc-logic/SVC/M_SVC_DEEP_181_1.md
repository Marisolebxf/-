# 服务机构培育推荐模型（M_SVC_DEEP_181_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SVC-seed.yaml。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SVC_DEEP_181_1 |
| 指标名称 | 服务机构培育推荐模型 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 产业服务链分析 |
| 三级模块 | 培育服务机构推荐分析 |
| 更新频率 | 按需 |
| 对齐状态判定 | 已按算法库9.10展开；与前端培育四维分列 |
| 是否在数据库 | 否 |
| 关联Q编号 |  |

## 口径定义

对深圳本土服务机构的培育推荐指数，从竞争力、产业相关度、政策匹配度、发展潜力四个维度评定，取值 0—100。

## 计算逻辑说明

第一步：各指标标准化

各指标原始数据通过极值归一化法消除量纲，转换为 0—100 之间的标准化得分：
$$
指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij}为第 i 个机构在第 j 个指标上的原始值，\min(x_j)和 \max(x_j)分别为该指标在所有机构中的最小值和最大值。
$$

第二步：各维度得分计算

各维度得分为其下各指标标准化得分的加权平均（可采用等权重，也可根据评估重点自行制定各指标权重）：
$$
竞争力得分 = w_1 \times研发投入强度得分+ w_2 \times研发人员占比得分
$$

$$
产业相关度得分 = w_3 \times 产业契合度得分+ w_4 \times产业链协同度得分
$$

$$
政策匹配度得分 = 政策契合度得分
$$

$$
发展潜力得分= w_5 \times营业收入增长率得分+ w_6 \times净利润增长率得分
$$

第三步：培育推荐综合得分

四个维度得分加权汇总（可采用等权重，各维度权重 = 1/4；也可根据评估重点自行制定各维度权重）：
$$
培育推荐得分 = W_1 \times 竞争力得分 + W_2 \times 产业相关度得分 + W_3 \times 政策匹配度得分 + W_4 \times 发展潜力得分
$$
其中，W_1、W_2、W_3、W_4 为各维度权重，可采用等权重（各占 25%），也可根据评估重点自行制定，\sum W = 1。得分越高，表明该服务机构越值得被推荐培育。

服务机构培育推荐模型指标体系

| 维度           | 指标           | 指标说明                                                 | 计算方法                                                     | 源表字段 | 待建字段 |
| :------------- | :------------- | :------------------------------------------------------- | :----------------------------------------------------------- | -------- | -------- |
| **竞争力** | 研发投入强度 | 研发费用占营业收入的比例，反映机构技术创新投入水平 | 研发费用 ÷ 营业收入 × 100% | dwd_org_annual_financial_info(org_id, arch development am, operating_revenue, year) — 研发投入,营收 | 无 |
|  | 研发人员占比 | 研发人员占从业人员总数的比例，反映机构人才储备与创新能力 | 研发人员数 ÷ 从业人员总数 × 100% | dwd_org_annual_financial_info(org_id, development_employee, employees_number, year) — 研发人员,从业人数 | 无 |
| **产业相关度** | 产业契合度 | 机构主营业务与目标产业方向的匹配程度 | 匹配关键词数 ÷ 目标产业关键词库总数 × 100% | demo_gkxlumenx_ods.svc_org_card(org_id, industry) — 机构行业；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 已挂产业；dwd_industry_chain_info(industry_name, industry_link_name) — 目标词表 | 无 |
|  | 产业链协同度 | 机构在产业链中的位置与上下游协同价值 | 机构上下游关联企业数量 ÷ 目标产业链总企业数 × 100% | dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 机构覆盖环节；dwd_industry_chain_info(industry_code, industry_link_code) — 目标链环节 | 无 |
| **政策匹配度** | 政策契合度 | 机构业务方向与产业政策支持方向的匹配程度 | 机构参与政策宣贯、产业规划等相关项目/活动数 ÷ 政策相关项目/活动总数 × 100%（或通过政策关键词匹配度评估） | dwd_policy_base(id, title, keywords, theme, keypoints, city, status) — 政策文本；dwd_org_industry_tags(credit_code, industry_name) — 机构产业词 | svc_org_policy_hit-机构与政策匹配标记 |
| **发展潜力** | 营业收入增长率 | 近两年营业收入的年均增长率，反映机构成长速度 | （本年营业收入 − 上年营业收入）÷ 上年营业收入 × 100% | dwd_org_annual_financial_info(org_id, operating_revenue, year) — 营收 | 无 |
|  | 净利润增长率 | 近两年净利润的年均增长率，反映机构盈利能力的提升趋势 | （本年净利润 − 上年净利润）÷ 上年净利润 × 100% | dwd_org_annual_financial_info(org_id, pure_profit, year) — 净利润 | 无 |

## 源表字段

- demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, industry, service_type_candidate) — 服务机构清单,深圳城市筛选
- dwd_org_base_info(org_id, external_id) — 信用代码对齐
- dwd_org_annual_financial_info(org_id, arch development am, operating_revenue, development_employee, employees_number, pure_profit, year) — 研发投入,营收,研发人员,从业人数,净利润
- dwd_org_industry_tags(credit_code, industry_code, industry_link_code, industry_name) — 已挂产业,覆盖环节
- dwd_industry_chain_info(industry_code, industry_link_code) — 标准环节
- dwd_policy_base(id, title, keywords, theme, keypoints, city, status) — 政策文本

## 待建字段

- svc_org_policy_hit-机构与政策匹配标记

## 参考资料

[1]服务机构培育推荐模型｜河北省软件集成电路与人工智能协会｜软件和信息技术服务企业核心竞争力评价规范：T/HASIC 001-2025｜2025-12-30｜https://ndls.cnis.ac.cn/standard/detail/a9fafb1645a480f9fecc37291a57ba3d.

[2]服务机构培育推荐模型 | 科技部 | “创新积分制”工作指引（全国试行版） | 2024-08-12 | https://kjj.hebi.gov.cn/kjdt/art/2024/art_d7af249cd56041c38c5227b4e92af48f.html.
