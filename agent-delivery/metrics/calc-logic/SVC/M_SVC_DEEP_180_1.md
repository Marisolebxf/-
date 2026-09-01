# 服务机构引入推荐模型（M_SVC_DEEP_180_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SVC-seed.yaml。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SVC_DEEP_180_1 |
| 指标名称 | 服务机构引入推荐模型 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 产业服务链分析 |
| 三级模块 | 引入服务机构推荐分析 |
| 更新频率 | 按需 |
| 对齐状态判定 | 已按算法库9.9展开；与前端招引四维分列 |
| 是否在数据库 | 否 |
| 关联Q编号 |  |

## 口径定义

对外部服务机构的引入推荐指数，从竞争力、产业相关度、政策匹配度、深圳连接度四个维度评定，取值 0—100，并生成优先级排序。

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
深圳连接度= 深圳供应链关联度得分
$$

第三步：培育推荐综合得分

四个维度得分加权汇总（可采用等权重，各维度权重 = 1/4；也可根据评估重点自行制定各维度权重）：
$$
培育推荐得分 = W_1 \times 竞争力得分 + W_2 \times 产业相关度得分 + W_3 \times 政策匹配度得分 + W_4 \times 深圳连接度得分
$$
其中，W_1、W_2、W_3、W_4 为各维度权重，可采用等权重（各占 25%），也可根据评估重点自行制定，\sum W = 1。得分越高，表明该服务机构越值得被推荐引入。

第四步：优先级排序

将各机构按引入推荐得分从高到低排序，生成服务机构引入优先级排名。

### 服务机构引入推荐模型指标体系

| 维度           | 指标             | 指标说明                                   | 计算方法                                                     | 源表字段 | 待建字段 |
| :------------- | :--------------- | :----------------------------------------- | :----------------------------------------------------------- | -------- | -------- |
| **竞争力** | 研发投入强度 | 从研发投入强度和研发人员占比评估竞争力。 | 研发费用 ÷ 营业收入 × 100% | dwd_org_annual_financial_info(org_id, arch development am, operating_revenue, year) — 研发投入,营收 | 无 |
|  | 研发人员占比 | 从研发投入强度和研发人员占比评估竞争力。 | 研发人员数 ÷ 从业人员总数 × 100% | dwd_org_annual_financial_info(org_id, development_employee, employees_number, year) — 研发人员,从业人数 | 无 |
| **产业相关度** | 产业契合度 | 从产业契合度和产业链协同度评估产业相关度。 | 匹配关键词数 ÷ 目标产业关键词库总数 × 100% | demo_gkxlumenx_ods.svc_org_card(org_id, industry) — 机构行业；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 已挂产业；dwd_industry_chain_info(industry_name, industry_link_name) — 目标词表 | 无 |
|  | 产业链协同度 | 从产业契合度和产业链协同度评估产业相关度。 | 机构上下游关联企业数量 ÷ 目标产业链总企业数 × 100% | dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 机构覆盖环节；dwd_industry_chain_info(industry_code, industry_link_code) — 目标链环节；dwd_org_invest_info(org_id, inv_org_id) — 上下游关联代理 | 无 |
| **政策匹配度** | 政策契合度 | 从政策契合度评估政策匹配度。 | 政策关键词匹配度评估（或按机构参与政策宣贯、产业规划等项目数占比计分） | dwd_policy_base(id, title, keywords, theme, keypoints, status) — 政策文本；dwd_org_industry_tags(credit_code, industry_name) — 机构产业词 | svc_org_policy_hit-机构与政策匹配标记 |
| **深圳连接度** | 深圳供应链关联度 | 从深圳供应链关联度评估深圳连接度。 | 机构在深圳地区的客户/供应商数量 ÷ 机构总客户/供应商数量 × 100% | dwd_org_invest_info(org_id, inv_org_id) — 投资连接；dwd_org_shareholder_info(org_id, inv_org_id, owners_type) — 机构股东；dwd_org_subsidiary_info(org_id, sub_org_id) — 子公司；dwd_org_base_info(org_id, city) — 对端城市 | 无 |

## 源表字段

- demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, industry, service_type_candidate) — 服务机构清单,外部城市筛选
- dwd_org_base_info(org_id, external_id) — 信用代码对齐
- dwd_org_industry_tags(credit_code, industry_code, industry_name) — 已挂产业
- dwd_industry_chain_info(industry_code, industry_name, industry_link_name) — 目标产业词表
- dwd_org_annual_financial_info(org_id, arch development am, operating_revenue, development_employee, employees_number, year) — 研发投入,营收,研发人员,从业人数
- dwd_policy_base(id, title, keywords, theme, keypoints, status) — 政策文本
- dwd_org_invest_info(org_id, inv_org_id) — 深圳连接
- dwd_org_shareholder_info(org_id, inv_org_id, owners_type) — 深圳连接
- dwd_org_subsidiary_info(org_id, sub_org_id) — 深圳子公司
- dwd_org_base_info(org_id, city) — 对端城市

## 待建字段

- svc_org_policy_hit-机构与政策匹配标记

## 参考资料

[1]服务机构引入推荐模型 ｜河北省软件集成电路与人工智能协会｜软件和信息技术服务企业核心竞争力评价规范：T/HASIC 001-2025｜2025-12-30｜[T/HASIC 001-2025-软件和信息技术服务企业核心竞争力评价规范-国家标准馆·国家数字标准馆](https://ndls.cnis.ac.cn/standard/detail/a9fafb1645a480f9fecc37291a57ba3d)

[2]服务机构培育推荐模型 | 科技部 | “创新积分制”工作指引（全国试行版） | 2024-08-12 | https://kjj.hebi.gov.cn/kjdt/art/2024/art_d7af249cd56041c38c5227b4e92af48f.html.

[3]服务机构引入推荐模型｜深圳市工业和信息化局、深圳市商务局｜《深圳市加快推进供应链创新与发展三年行动计划（2023-2025年）》｜2023年9月｜[https://www.sz.gov.cn](https://www.sz.gov.cn/).
