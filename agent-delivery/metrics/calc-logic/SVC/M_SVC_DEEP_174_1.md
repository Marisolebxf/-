# 金融服务机构技术力评价模型（M_SVC_DEEP_174_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SVC-seed.yaml。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SVC_DEEP_174_1 |
| 指标名称 | 金融服务机构技术力评价模型 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 产业服务链分析 |
| 三级模块 | 服务机构技术力评估分析 |
| 更新频率 | 按需 |
| 对齐状态判定 | 已按算法库9.3展开；融资成本/服务质量待建 |
| 是否在数据库 | 否 |
| 关联Q编号 |  |

## 口径定义

选定金融服务机构在统计年度的技术力指数，从资金规模、融资成本、资金风险、服务质量四个维度评定，取值 0—100。

## 计算逻辑说明

入集：按 org_id 去重。金融服务机构认定读 demo_gkxlumenx_ads.svc_org_card(service_type_candidate=FINANCE )

第一步：入集并取财务、融资、风险、资讯。

第二步：四维原始值（见下表）。

第三步：合成：各维截面 min-max 到 [0,1]，缺维不补 0、不进平均；等权（默认权重待甲方确认）后 ×100。全市/全样本同值取 0.5。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 金融服务机构技术力评价模型 | 资金规模 | 资产总额 | 从资产与注册资本评估资金运作规模。 | total_assets（年报优先，上市可用 stock 表同期） | dwd_org_annual_financial_info(org_id, total_assets, year) — 资产总额 | 无 |
| 金融服务机构技术力评价模型 | 资金规模 | 注册资本 | 从资产与注册资本评估资金运作规模。 | registered_capital_value | dwd_org_base_info(org_id, registered_capital_value) — 注册资本 | 无 |
| 金融服务机构技术力评价模型 | 融资成本 |  | 从融资成本率评估融资效率。 | 待建直读；现表无利率 | 无 | financing_cost_rate-融资成本率 |
| 金融服务机构技术力评价模型 | 资金风险 | 资产负债率 | 从杠杆与信用风险事件评估资金风险。 | total_liabilities / total_assets | dwd_org_annual_financial_info(org_id, total_assets, total_liabilities, year) — 资产负债 | 无 |
| 金融服务机构技术力评价模型 | 资金风险 | 失信与处罚件数 | 从杠杆与信用风险事件评估资金风险。 | COUNT(失信)+COUNT(处罚)，反向计分 | dwd_org_risk_shixin(org_id) — 失信；dwd_org_company_punish(org_id) — 处罚 | 无 |
| 金融服务机构技术力评价模型 | 服务质量 | 资讯提及量 | 从客户服务水平评估金融服务质量（无评价源时用资讯代理）。 | COUNT(DISTINCT news_title) 统计年 | dwd_org_important_news_info(org_id, news_title, news_date) — 资讯代理 | svc_quality_score-金融机构服务质量评价 |

## 源表字段

- demo_gkxlumenx_ads.svc_org_card(service_type_candidate=FINANCE )
- dwd_org_annual_financial_info(org_id, total_assets, total_liabilities, year) — 资产与负债
- dwd_org_financing_info(org_id, funding_amount, completion_date) — 融资事件
- dwd_org_risk_shixin(org_id) — 失信（风险反向）
- dwd_org_company_punish(org_id) — 处罚（风险/服务反向）
- dwd_org_important_news_info(org_id, news_title, news_date) — 服务质量资讯代理

## 待建字段

- financing_cost_rate-融资成本率
- svc_quality_score-金融机构服务质量评价
