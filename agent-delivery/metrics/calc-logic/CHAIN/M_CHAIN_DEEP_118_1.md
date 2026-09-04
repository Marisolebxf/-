# 深圳产业链模型构建（M_CHAIN_DEEP_118_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_118_1 |
| 指标名称 | 深圳产业链模型构建 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 是 |
| 关联Q编号 | - |

## 口径定义

在产业链全景模型基础上，按地域属性自动筛选深圳（行政区划编码 440300000000）域内的产业链节点与主体，统计深圳域内各环节节点、关联主体（企业、科研机构、人才）数量及区（district）分布，形成深圳产业链全景。对象=深圳域内产业链要素，区域口径以企业/机构注册地 city=深圳 或 area_code=440300 为准。

## 计算逻辑说明

① 地域入集：企业用 `dwd_org_base_info.city='深圳'`（或 `area_code='440300000000'`），科研机构用 `dwd_research_institute_base_info.city`，人才用机构归属地。② 环节与主体统计：深圳环节节点数、深圳环节企业数/科研机构数/人才数。③ 区县分布：按 `district`/`area` 分组统计企业与机构数。

- 深圳环节节点数 = COUNT(DISTINCT node_id) WHERE 主体 city=深圳
- 深圳环节企业数 = COUNT(DISTINCT credit_code) WHERE city=深圳
- 深圳各区企业数 = COUNT(DISTINCT credit_code) GROUP BY area
- 深圳产业要素汇总 = 企业数 + 科研机构数 + 人才数

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 深圳产业链模型构建 | 深圳环节结构 | 深圳环节节点数 | 深圳域内产业链去重环节节点数。 | COUNT(DISTINCT node_id) WHERE 深圳 | demo_gkxlumenx_dwd.industry_chain_node(node_id, chain_id, node_code, node_name, node_level, stage_code)；dwd_org_industry_tags(industry_link_code, credit_code)；dwd_org_base_info(city) | 无 |
| 深圳产业链模型构建 | 深圳主体分布 | 深圳环节企业数 | 深圳域内各环节挂接的去重企业数。 | COUNT(DISTINCT credit_code) WHERE city=深圳 | dwd_org_industry_tags(industry_code, industry_link_code, company_name, credit_code)；dwd_org_base_info(org_id, name_cn, external_id, city, area, province) | 无 |
|  |  | 深圳环节科研机构数 | 深圳域内关联科研机构去重数。 | COUNT(DISTINCT org_id) WHERE city=深圳 | dwd_research_institute_base_info(org_id, name_cn, external_id, city, area, province, org_type) | 无 |
|  |  | 深圳环节人才数 | 深圳域内关联人才(学者)去重数。 | COUNT(DISTINCT scholar_id) WHERE 机构city=深圳 | dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id, paper_nums, h_index)；dwd_org_base_info(org_id, name_cn, city) | 无 |
| 深圳产业链模型构建 | 深圳区域分布 | 深圳各区企业数 | 深圳各区（district）去重企业数。 | COUNT(DISTINCT credit_code) GROUP BY area | dwd_org_base_info(org_id, external_id, city, area, province)；dwd_org_industry_tags(credit_code) | 无 |
|  |  | 深圳各区机构数 | 深圳各区科研机构去重数。 | COUNT(DISTINCT org_id) GROUP BY area | dwd_research_institute_base_info(org_id, city, area) | 无 |
| 深圳产业链模型构建 | 深圳全景汇总 | 深圳产业链要素汇总 | 深圳企业/机构/人才/营收汇总。 | 读取 enterprise_count/institution_count/talent_count/total_revenue | gkxlumenx_ads.chain_sz_panorama(chain_id, chain_name, enterprise_count, node_count, nodes, edges, district_dist)；gkxlumenx_ads.chain_sz_elements(chain_id, chain_name, enterprise_count, institution_count, talent_count, total_revenue)；gkxlumenx_ads.chain_sz_dist(chain_id, chain_name, district, enterprise_count, institution_count) | 无 |

## 源表字段

- dwd_org_industry_tags(industry_code, industry_link_code, company_name, credit_code) — 企业到环节挂接
- dwd_org_base_info(org_id, name_cn, external_id, province, city, area, reg_status, org_type) — 企业地域与属性
- dwd_research_institute_base_info(org_id, name_cn, external_id, city, area, province, org_type) — 科研机构地域
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id, paper_nums, h_index) — 人才存量与归属
- demo_gkxlumenx_dwd.industry_chain_node(node_id, chain_id, node_code, node_name, node_level, stage_code) — 归一化环节节点
- demo_gkxlumenx_dwd.industry_chain_entity_rel(node_id, entity_type, entity_id) — 环节-主体关系
- dwd_dim_admin_area(cur_code, cur_name, province_name, city_name, area_name, parent_code) — 深圳=440300000000 行政区划
- gkxlumenx_ads.chain_sz_panorama(chain_id, chain_name, enterprise_count, node_count, nodes, edges, district_dist) — 深圳全景汇总
- gkxlumenx_ads.chain_sz_elements(chain_id, chain_name, enterprise_count, institution_count, talent_count, total_revenue) — 深圳要素汇总
- gkxlumenx_ads.chain_sz_dist(chain_id, chain_name, district, enterprise_count, institution_count) — 深圳各区分布

## 待建字段

- 无

## 参考资料

[1] 深圳市产业链「链长制」及产业集群布局|深圳市工业和信息化局|深圳「20+8」产业集群行动方案|https://gxj.sz.gov.cn/

[2] 区域创新能力监测指标体系|科学技术部|https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/t20131129_110674.html

[3] 国民经济行业分类 GB/T 4754—2017|国家统计局|https://www.stats.gov.cn/
