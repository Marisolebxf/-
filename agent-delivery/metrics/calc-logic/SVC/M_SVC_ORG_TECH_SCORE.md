# 服务机构影响力（M_SVC_ORG_TECH_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SVC-seed.yaml。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SVC_ORG_TECH_SCORE |
| 指标名称 | 服务机构影响力 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 产业服务链分析 |
| 三级模块 | 服务机构技术力评估分析 |
| 更新频率 | 按需 |
| 对齐状态判定 | 待甲方Q-SVCCHAIN-01；专利/财务维已对extract |
| 是否在数据库 | 否 |
| 关联Q编号 | Q-SVCCHAIN-01 / Q111 |

## 口径定义

选定服务机构在统计年度的技术力综合评分，从专利数量、研发投入、核心专家、成功案例、标准制定五个维度评定，取值 0—100。分数越高表示技术能力越强。

## 计算逻辑说明

入集：demo_gkxlumenx_ads.svc_org_card— 服务机构认定

专利与机构用 dwd_patent.first_applicant_name 对齐 dwd_org_base_info.name_cn（无 org_id）。发明口径：kind 为发明/发明公布（样例值为 A，码表待业务确认）。有效：dwd_patent_legal.status 含「授权」且 anticipated_expiration 空或不早于统计日。

第一步：从 svc_org_circle 取入集机构，并对齐专利申请人、财务 org_id。

第二步：五维原始值（见下表）。缺维不补 0，该维不进入平均。

第三步：对比集合内各维 min-max 到 [0,1]；全市同值取 0.5。

第四步：等权平均 ×100。正式默认权重待 Q-SVCCHAIN-01。算法库 9.3–9.8 按类型另起模型，本指标不按类型另起一级。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 服务机构影响力 | 专利数量 | 有效发明专利数 | 从有效发明专利存量、发明专利占比及当年新增申请量等维度评估机构核心技术产出能力与创新活跃度。 | COUNT(DISTINCT patent_id) WHERE kind∈发明口径 AND status含授权 | dwd_patent(patent_id, kind, first_applicant_name) — 发明识别与申请人对齐；dwd_patent_legal(pn, status, anticipated_expiration) — 授权/有效 | 无 |
| 服务机构影响力 | 专利数量 | 发明专利占比 | 从有效发明专利存量、发明专利占比及当年新增申请量等维度评估机构核心技术产出能力与创新活跃度。 | 有效发明专利数 / 有效专利总数 | dwd_patent(patent_id, kind, first_applicant_name) — 专利类型；dwd_patent_legal(pn, status) — 有效专利分母 | 无 |
| 服务机构影响力 | 专利数量 | 当年新增专利申请量 | 从有效发明专利存量、发明专利占比及当年新增申请量等维度评估机构核心技术产出能力与创新活跃度。 | COUNT(DISTINCT patent_id) WHERE application_reference.apdt_year=统计年 | dwd_patent(patent_id, first_applicant_name, application_reference.apdt_year) — 申请年 | 无 |
| 服务机构影响力 | 研发投入 | 研发投入金额 | 从研发投入金额与研发投入强度评估机构技术资源投入规模。 | 年报「arch development am」 | dwd_org_annual_financial_info(org_id, arch development am, year) — 年报研发投入 | 无 |
| 服务机构影响力 | 研发投入 | 研发投入强度 | 从研发投入金额与研发投入强度评估机构技术资源投入规模。 | 研发投入金额 / operating_revenue | 上表 + dwd_org_annual_financial_info(org_id, operating_revenue, year) / dwd_org_stock_finance_info(org_id, operating_revenue) — 营收分母 | 无 |
| 服务机构影响力 | 核心专家 | 研发人员数量 | 从研发人员数量及研发人员占职工总数的比重评估机构技术人才储备。 | development_employee | dwd_org_annual_financial_info(org_id, development_employee, year) — 年报研发人员数 | 无 |
| 服务机构影响力 | 核心专家 | 研发人员占职工总数的比重 | 从研发人员数量及研发人员占职工总数的比重评估机构技术人才储备。 | development_employee / employees_number | dwd_org_annual_financial_info(org_id, development_employee, employees_number, year) — 研发人员与从业人数 | 无 |
| 服务机构影响力 | 成功案例 | 可验证成功案例数 | 从可验证成功案例与案例资讯提及量评估机构服务成果。 | 待建直读 | 无 | svc_success_case_count-可验证成功案例数 |
| 服务机构影响力 | 成功案例 | 案例资讯提及量 | 从可验证成功案例与案例资讯提及量评估机构服务成果。 | COUNT(DISTINCT news_title) WHERE news_date 落在统计年 | dwd_org_important_news_info(org_id, news_title, news_date) — 案例资讯代理 | 无 |
| 服务机构影响力 | 标准制定 | 国家标准参与数 | 从国家标准与行业标准参与情况评估机构标准话语权。 | 待建直读 | 无 | gb_standard_count-国家标准参与数 |
| 服务机构影响力 | 标准制定 | 行业标准参与数 | 从国家标准与行业标准参与情况评估机构标准话语权。 | 待建直读 | 无 | industry_standard_count-行业标准参与数 |

## 源表字段

- demo_gkxlumenx_ads.svc_org_card— 服务机构认定
- dwd_patent(patent_id, kind, first_applicant_name, application_reference.apdt_year) — 专利类型、申请人、申请年
- dwd_patent_legal(pn, status, anticipated_expiration) — 授权/有效
- dwd_org_annual_financial_info(org_id, arch development am, operating_revenue, development_employee, employees_number, year) — 年报研发投入、营收、研发人员、从业人数
- dwd_org_important_news_info(org_id, news_title, news_date) — 案例资讯代理

## 待建字段

- svc_success_case_count-可验证成功案例数
- gb_standard_count-国家标准参与数
- industry_standard_count-行业标准参与数

## 参考资料

合成评分+经济合作与发展组织+https://www.oecd.org/en/publications/handbook-on-constructing-composite-indicators-methodology-and-user-guide_9789264043466-en.html
