# 培育综合评分（M_SVC_REC_CULTIVATE_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SVC-seed.yaml。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SVC_REC_CULTIVATE_SCORE |
| 指标名称 | 培育综合评分 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 产业服务链分析 |
| 三级模块 | 培育服务机构推荐分析 |
| 更新频率 | 按需 |
| 对齐状态判定 | 待甲方Q-SVCCHAIN-05；规模/创新已对extract |
| 是否在数据库 | 否 |
| 关联Q编号 | Q-SVCCHAIN-05 |

## 口径定义

对深圳本土在库服务机构的培育综合评分，从现有规模、技术创新能力、服务成效、市场缺口四个维度评定，取值 0—100。

## 计算逻辑说明

第一步：各指标标准化

各指标原始数据通过极值归一化法消除量纲，转换为 0—100 之间的标准化得分：
$$
指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij} 为第 i 个机构在第 j 个指标上的原始值，\min(x_j) 和 \max(x_j) 分别为该指标在所有机构中的最小值和最大值。
$$

第二步：各维度得分计算

各维度得分为其下各指标标准化得分的等权加权平均：

现有规模得分 =（从业人员数得分 + 资产规模得分）÷ 2
技术创新能力得分 =（研发人才结构得分 + 研发投入强度得分）÷ 2
服务成效得分 =（服务企业数量得分 + 服务项目数量得分）÷ 2
市场缺口得分 = 市场占有率得分

第三步：培育综合评分计算

四个维度得分按等权加权汇总：
$$
培育综合评分 = \frac{现有规模得分 + 技术创新能力得分 + 服务成效得分 + 市场缺口得分}{4}
$$
其中，各维度可采用等权重（各占 25%），也可根据评估重点自行制定各维度权重。得分越高表明机构的培育综合能力越强。

培育综合评分指标体系

| 维度             | 指标         | 指标说明                                                     | 计算公式                                       | 源表字段 | 待建字段 |
| :--------------- | :----------- | :----------------------------------------------------------- | :--------------------------------------------- | -------- | -------- |
| **现有规模** | 从业人员数 | 机构全职从事科创服务的职工总数，反映人力资源规模 | 上年度全职从事科创服务职工总数 | dwd_org_annual_financial_info(org_id, employees_number, year) — 从业人数 | 无 |
|  | 资产规模 | 机构拥有的资产总额，反映经济实力和经营基础 | 资产总额（资产负债表中“资产总计”科目期末余额） | dwd_org_annual_financial_info(org_id, total_assets, year) — 资产总额 | 无 |
| **技术创新能力** | 研发人才结构 | 研发人员占从业人员总数的比重，反映机构研发人力投入强度和创新人才储备 | 研发人员数 ÷ 从业人员总数 × 100% | dwd_org_annual_financial_info(org_id, development_employee, employees_number, year) — 研发人员,从业人数 | 无 |
|  | 研发投入强度 | 研发经费内部支出占营业收入的比重，反映机构对技术创新的重视程度和投入能力 | 研发经费内部支出 ÷ 营业收入 × 100% | dwd_org_annual_financial_info(org_id, arch development am, operating_revenue, year) — 研发投入,营收 | 无 |
| **服务成效** | 服务企业数量 | 评价周期内实际服务的企业总数，反映服务覆盖广度 | 评价周期内服务企业总数 | dwd_org_important_news_info(org_id, news_title, news_date) — 服务成效代理 | svc_served_ent_count-服务企业数 |
|  | 服务项目数量 | 评价周期内承接并完成的服务项目总量，反映业务活跃度 | 评价周期内完成服务项目总数 | dwd_org_important_news_info(org_id, news_title, news_date) — 服务成效代理 | svc_project_count-服务项目数 |
| **市场缺口** | 市场占有率 | 机构营业收入占目标市场同类机构营业收入总额的比重，反映市场竞争地位和成长空间 | 机构营业收入 ÷ 目标市场同类机构营收总额 × 100% | demo_gkxlumenx_ods.svc_org_card(org_id, industry) — 同类机构清单；dwd_org_annual_financial_info(org_id, operating_revenue, year) — 机构营收,同类营收 | 无 |

## 源表字段

- demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, industry, service_type_candidate) — 服务机构清单,深圳城市筛选
- dwd_org_base_info(org_id, external_id) — 信用代码对齐
- dwd_org_annual_financial_info(org_id, employees_number, total_assets, development_employee, arch development am, operating_revenue, year) — 从业人数,资产总额,研发人员,研发投入,营收
- dwd_org_important_news_info(org_id, news_title, news_date) — 服务成效代理
- dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 所属产业

## 待建字段

- svc_served_ent_count-服务企业数
- svc_project_count-服务项目数

## 参考资料

[1]培育综合评分｜安阳市科学技术局｜安阳市科技服务机构考评奖补办法（试行）：安科〔2022〕21号｜2022-05-26｜[《安阳市科技服务机构考评奖补办法（试行）》政策解读_政策解读_安阳市科学技术局](https://ayskjj.anyang.gov.cn/2022/07-21/2352930.html).

[2]培育综合评分｜江苏省市场监督管理局｜科技服务机构星级评定规范：DB32/T 5108-2025｜2025-03-25｜https://dbba.sacinfo.org.cn/attachment/onlineRead/a0698473576de40c89372a7a7c44a9226580a1feed9ab56bde88156de762bb43?file=%2Fportal%2Fdownload%2Fa0698473576de40c89372a7a7c44a9226580a1feed9ab56bde88156de762bb43#zoom=auto&disablerange=true&disablestream=true&disableautofetch=true.
