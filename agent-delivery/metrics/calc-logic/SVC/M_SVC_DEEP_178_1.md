# 咨询服务机构技术力评价模型（M_SVC_DEEP_178_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SVC-seed.yaml。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SVC_DEEP_178_1 |
| 指标名称 | 咨询服务机构技术力评价模型 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 产业服务链分析 |
| 三级模块 | 服务机构技术力评估分析 |
| 更新频率 | 按需 |
| 对齐状态判定 | 已按算法库9.7展开；成功案例待建 |
| 是否在数据库 | 否 |
| 关联Q编号 |  |

## 口径定义

选定咨询服务机构在统计年度的技术力指数，从人才密度、行业经验、成功案例数、行业声誉四个维度评定，取值 0—100。

## 计算逻辑说明

第一步：入集demo_gkxlumenx_ads.svc_org_card(service_type_candidate=CONSULT) — 咨询服务机构认定。

第二步：四维原始值。

第三步：合成：各维截面 min-max 到 [0,1]，缺维不补 0、不进平均；等权后 ×100。

| 一级指标                   | 二级指标   | 三级指标   | 指标说明                           | 计算公式                                | 源表字段                                                     | 待建字段                                |
| -------------------------- | ---------- | ---------- | ---------------------------------- | --------------------------------------- | ------------------------------------------------------------ | --------------------------------------- |
| 咨询服务机构技术力评价模型 | 人才密度   |            | 从技术类人才占比评估人才密度。     | development_employee / employees_number | dwd_org_annual_financial_info(org_id, development_employee, employees_number, year) — 研发人员占比代理 | 无                                      |
| 咨询服务机构技术力评价模型 | 行业经验   | 成立年限   | 从从业时间与行业覆盖评估行业经验。 | 统计年 − incorporation_year             | dwd_org_base_info(org_id, incorporation_year) — 成立年份     | 无                                      |
| 咨询服务机构技术力评价模型 | 行业经验   | 覆盖产业数 | 从从业时间与行业覆盖评估行业经验。 | COUNT(DISTINCT industry_code)           | dwd_org_industry_tags(credit_code, industry_code) — 行业范围 | 无                                      |
| 咨询服务机构技术力评价模型 | 成功案例数 |            | 从可验证成果项目数评估成功案例。   | 待建直读；现用资讯条数代理              | dwd_org_important_news_info(org_id, news_title, news_date) — 资讯代理 | svc_success_case_count-可验证成功案例数 |
| 咨询服务机构技术力评价模型 | 行业声誉   |            | 从荣誉标签与资讯声量评估行业声誉。 | 荣誉标签加权 + 资讯条数等权             | dwd_org_tech_tag(org_id, org_tag) — 荣誉；dwd_org_important_news_info(org_id, news_title, news_date) — 声量 | 无                                      |

## 源表字段

- demo_gkxlumenx_ads.svc_org_card(service_type_candidate=CONSULT) — 咨询服务机构认定
- dwd_org_annual_financial_info(org_id, development_employee, employees_number, year) — 人才密度
- dwd_org_industry_tags(credit_code, industry_code) — 行业覆盖
- dwd_org_tech_tag(org_id, org_tag) — 荣誉声誉
- dwd_org_important_news_info(org_id, news_title, news_date) — 声量/案例代理

## 待建字段

- svc_success_case_count-可验证成功案例数

## 参考资料

[1]咨询服务机构技术力评价模型｜深圳市市场监督管理局｜管理咨询机构等级评定规范：DB4403/T 559—2024｜2024-12-20｜[https://amr.sz.gov.cn](https://amr.sz.gov.cn/).

[2]咨询服务机构技术力评价模型｜山东科技咨询协会｜科技咨询机构及科技咨询师评价规范：T/SDASTC 016-2025｜2025年｜[http://www.sdastc.com](http://www.sdastc.com/).
