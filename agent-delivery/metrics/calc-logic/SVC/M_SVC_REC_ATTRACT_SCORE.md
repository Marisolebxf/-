# 招引综合评分（M_SVC_REC_ATTRACT_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SVC-seed.yaml。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SVC_REC_ATTRACT_SCORE |
| 指标名称 | 招引综合评分 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 产业服务链分析 |
| 三级模块 | 引入服务机构推荐分析 |
| 更新频率 | 按需 |
| 对齐状态判定 | 待甲方Q-SVCCHAIN-05；四维已对extract |
| 是否在数据库 | 否 |
| 关联Q编号 | Q-SVCCHAIN-05 |

## 口径定义

针对深圳拟发展产业方向，对外部服务机构的招引综合评分，从产业匹配度、技术领先性、发展潜力、对外合作意愿四个维度评定，取值 0—100。

## 计算逻辑说明

第一步：各指标标准化

各指标原始数据通过极值归一化法消除量纲，转换为 0—100 之间的标准化得分：
$$
指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij} 为第 i 个机构在第 j个指标上的原始值，\min(x_j) 和 \max(x_j)分别为该指标在所有机构中的最小值和最大值。
$$

第二步：各维度得分计算

各维度得分为其下各指标标准化得分的加权平均（可采用等权重，也可根据评估重点自行制定各指标权重）：
$$
产业匹配度得分 = w_1 \times 产业契合度得分 + w_2 \times 产业链协同度得分
$$

$$
技术领先性得分 = w_3 \times 研发投入强度得分+ w_4 \times专利申请量得分
$$

$$
发展潜力得分 = w_5 \times营业收入同比增长率得分+ w_6 \times净利润同比增长率得分
$$

$$
对外合作意愿得分 = w_7 \times$ 对外合作项目数量得分+ w_8 \times对外合作覆盖范围得分
$$

第三步：招引综合评分计算

四个维度得分加权汇总（可采用等权重，各维度权重 = 1/4；也可根据评估重点自行制定各维度权重）：
$$
招引综合评分 = W_1 \times 产业匹配度得分 + W_2 \times 技术领先性得分 + W_3 \times 发展潜力得分 + W_4 \times 对外合作意愿得分
$$
其中，W_1、W_2、W_3、W_4 为各维度权重，可采用等权重（各占 25%），也可根据评估重点自行制定，\sum W = 1。得分越高，表明机构的招引价值越大，越值得优先引进。



| 维度             | 指标             | 指标说明                                                     | 计算方法                                             | 源表字段 | 待建字段 |
| :--------------- | :--------------- | :----------------------------------------------------------- | :--------------------------------------------------- | -------- | -------- |
| **产业匹配度** | 产业契合度 | 机构主营业务与目标产业方向的匹配程度 | 匹配关键词数 ÷ 目标产业关键词库总数 × 100% | demo_gkxlumenx_ods.svc_org_card(org_id, industry) — 机构行业；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 已挂产业；dwd_industry_chain_info(industry_name, industry_link_name) — 目标词表 | 无 |
|  | 产业链协同度 | 机构在产业链中的位置与上下游协同价值 | 机构上下游关联企业数量 ÷ 目标产业链总企业数 × 100% | dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 机构覆盖环节；dwd_industry_chain_info(industry_code, industry_link_code) — 目标链环节；dwd_org_invest_info(org_id, inv_org_id) — 上下游关联代理 | 无 |
| **技术领先性** | 研发投入强度 | 机构研发费用占营业收入的比例 | 研发经费内部支出 ÷ 营业收入 × 100% | dwd_org_annual_financial_info(org_id, arch development am, operating_revenue, year) — 研发投入,营收 | 无 |
|  | 发明专利占比 | 有效发明专利占有效专利总数的比重 | 有效发明专利数 ÷ 有效专利总数 × 100% | dwd_patent(patent_id, kind, first_applicant_name) — 专利类型,申请人对齐；dwd_patent_legal(pn, status) — 授权有效 | 无 |
| **发展潜力** | 营业收入增长率 | 反映机构本年营业收入相比上年同期的增长情况，体现短期营收增长趋势 | （本年营业收入 − 上年营业收入）÷ 上年营业收入 × 100% | dwd_org_annual_financial_info(org_id, operating_revenue, year) — 营收 | 无 |
|  | 净利润增长率 | 反映机构本年净利润相比上年同期的增长情况，体现短期盈利增长趋势 | （本年净利润 − 上年净利润）÷ 上年净利润 × 100% | dwd_org_annual_financial_info(org_id, pure_profit, year) — 净利润 | 无 |
| **对外合作意愿** | 对外合作项目数量 | 机构近三年参与或发起的对外合作项目总数 | 统计近三年对外合作项目总数 | dwd_org_invest_info(org_id, inv_org_id) — 对外投资代理 | svc_coop_project_count-对外合作项目数 |
|  | 对外合作覆盖范围 | 机构对外合作的区域覆盖广度 | 统计对外合作覆盖的省份或城市数量 | dwd_org_invest_info(org_id, inv_org_id) — 对外投资；dwd_org_base_info(org_id, city, province) — 对端区域 | svc_coop_region_count-对外合作覆盖区域数 |

## 源表字段

- demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, industry, service_type_candidate) — 服务机构清单,外部城市筛选
- dwd_org_base_info(org_id, external_id, city, province) — 信用代码对齐,对端区域
- dwd_org_industry_tags(credit_code, industry_code, industry_name) — 已挂产业
- dwd_industry_chain_info(industry_name, industry_link_name) — 目标产业词表
- dwd_org_annual_financial_info(org_id, arch development am, operating_revenue, pure_profit, year) — 研发投入,营收,净利润
- dwd_patent(patent_id, kind, first_applicant_name) — 专利类型,申请人对齐
- dwd_patent_legal(pn, status) — 授权有效
- dwd_org_invest_info(org_id, inv_org_id) — 对外投资

## 待建字段

- svc_coop_project_count-对外合作项目数
- svc_coop_region_count-对外合作覆盖区域数

## 参考资料

[1]招引综合评分 | 国家统计局 | 什么是研究与试验发展（R&D）经费及投入强度 | 2025-03-21 | https://www.stats.gov.cn/zs/tjws/tjzb/202301/t20230101_1903948.html.

[2]招引综合评分 | 科技部 | “创新积分制”工作指引（全国试行版） | 2024-08-12 | https://kjj.hebi.gov.cn/kjdt/art/2024/art_d7af249cd56041c38c5227b4e92af48f.html.

[3]招引综合评分 | 国家统计局 | 2025年1—5月份全国规模以上工业企业利润下降1.1% | 2025-06-27 | https://www.stats.gov.cn/sj/zxfb/202506/t20250627_1960270.html.

[4]招引综合评分| 工业和信息化部 | 《中外中小企业合作区管理暂行办法》（工信部企业〔2024〕168号） | 2024-09-03 | http://www.scio.gov.cn/live/2024/35043/wjzc/202410/t20241022_870437.html.

[5]招引综合评分 | 峄城区人民政府 | 对区政协十届四次会议第38号提案的答复（关于优化招商引资考核工作机制的提案） | 2025-09-09 | http://www.ycq.gov.cn/zwgk/gkzt/jytabl/qzxtabljg/202509/t20250909_2151247.html.
