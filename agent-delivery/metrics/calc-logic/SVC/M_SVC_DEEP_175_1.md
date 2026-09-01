# 知识产权服务机构技术力评价模型（M_SVC_DEEP_175_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SVC-seed.yaml。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SVC_DEEP_175_1 |
| 指标名称 | 知识产权服务机构技术力评价模型 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 产业服务链分析 |
| 三级模块 | 服务机构技术力评估分析 |
| 更新频率 | 按需 |
| 对齐状态判定 | 已按算法库9.4展开；成功案例待建 |
| 是否在数据库 | 否 |
| 关联Q编号 |  |

## 口径定义

选定知识产权服务机构在统计年度的技术力指数，从专业能力、业务范围、成功案例数、合作伙伴四个维度评定，取值 0—100。

## 计算逻辑说明

入集：知识产权服务机构认定读 demo_gkxlumenx_ads.svc_org_card(service_type_candidate=IP )

第一步：入集。专业能力优先用 dwd_patent.agency 对齐机构名称。

第二步：四维原始值。

第三步：合成：各维截面 min-max 到 [0,1]，缺维不补 0、不进平均；等权（默认权重待甲方确认）后 ×100。全市/全样本同值取 0.5。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 知识产权服务机构技术力评价模型 | 专业能力 | 代理专利件数 | 从代理专利规模与发明专利占比评估专业能力。 | COUNT(DISTINCT patent_id) WHERE agency 对齐机构名 | dwd_patent(patent_id, agency, kind) — 代理机构 | 无 |
| 知识产权服务机构技术力评价模型 | 专业能力 | 发明专利占比 | 从代理专利规模与发明专利占比评估专业能力。 | 代理发明专利数 / 代理专利总数 | dwd_patent(patent_id, agency, kind)；dwd_patent_legal(pn, status) — 有效发明占比 | 无 |
| 知识产权服务机构技术力评价模型 | 业务范围 |  | 从服务覆盖的产业领域数评估业务范围。 | COUNT(DISTINCT industry_code) | dwd_org_industry_tags(credit_code, industry_code) — 已挂产业 | 无 |
| 知识产权服务机构技术力评价模型 | 成功案例数 |  | 从可验证成功案例评估业务成果。 | 待建直读；现用资讯条数代理 | dwd_org_important_news_info(org_id, news_title, news_date) — 资讯代理 | svc_success_case_count-可验证成功案例数 |
| 知识产权服务机构技术力评价模型 | 合作伙伴 |  | 从机构股东与对外投资连接评估合作伙伴网络。 | COUNT(DISTINCT 机构股东)+COUNT(DISTINCT 被投机构) | dwd_org_shareholder_info(org_id, inv_org_id, owners_type) — 机构股东；dwd_org_invest_info(org_id, inv_org_id) — 对外投资 | 无 |

## 源表字段

- demo_gkxlumenx_ads.svc_org_card(service_type_candidate=IP )
- dwd_patent(patent_id, agency, first_applicant_name, kind) — 代理机构与专利
- dwd_patent_legal(pn, status) — 有效专利
- dwd_org_industry_tags(credit_code, industry_code) — 业务覆盖产业
- dwd_org_invest_info(org_id, inv_org_id) — 合作/投资伙伴
- dwd_org_shareholder_info(org_id, inv_org_id, owners_type) — 机构股东
- dwd_org_important_news_info(org_id, news_title, news_date) — 案例资讯代理

## 待建字段

- svc_success_case_count-可验证成功案例数

## 参考资料

> 第一作者单位：大连理工大学；基金项目：辽宁省社科规划基金
>
> GB/T7714‑2025：马翔，丁堃，杨阳，等。专利代理服务质量综合评价体系及实证研究 [J]. 科技进步与对策，2021,38 (13):118‑125.
>
> 官方参考来源（行业标准）：上海市地方标准 DB 31/T 1444—2023《专利代理机构信用综合评价指南》｜[https://sipa.sh.gov.cn/cmsres/a1/a14fe5120d8c40c9a48b8a1dd63a4c0d/168c9ed99f0180573636355de10de292.pdf](https://link.wtturl.cn/?target=https%3A%2F%2Fsipa.sh.gov.cn%2Fcmsres%2Fa1%2Fa14fe5120d8c40c9a48b8a1dd63a4c0d%2F168c9ed99f0180573636355de10de292.pdf&scene=im&aid=582478&lang=zh)
