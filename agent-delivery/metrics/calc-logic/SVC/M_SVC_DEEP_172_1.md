# 服务链短板分析模型（M_SVC_DEEP_172_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SVC-seed.yaml。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SVC_DEEP_172_1 |
| 指标名称 | 服务链短板分析模型 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 产业服务链分析 |
| 三级模块 | 服务链短板分析 |
| 更新频率 | 按需 |
| 对齐状态判定 | 已按算法库9.1展开；待甲方确认阈值与成因规则 |
| 是否在数据库 | 否 |
| 关联Q编号 |  |

## 口径定义

选定产业服务链在统计窗口内的短板分析综合结果，从服务质量、经营效益、服务类型结构三维度定位短板环节并给出成因，输出短板环节、成因与优化建议。

## 计算逻辑说明

入集：demo_gkxlumenx_ads.svc_org_card— 服务机构认定；

第一步：按算法库三维计算各环节原始值并标空白/薄弱/瓶颈/正常（前端六环节判定见 M_SVC_CHAIN_BOTTLENECK）。

第二步：成因规则（资源投入不足←经营效益低于阈值；流程/匹配不足←类型结构缺失；体验不足←服务质量低于阈值）。

第三步：按环节输出优化建议文本模板。阈值与模板待甲方确认。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 服务链短板分析模型 | 服务质量 |  | 从环节服务质量评价识别体验类短板。 | 待评价源；低于阈值记短板 | 无 | svc_quality_score-环节服务质量评价 |
| 服务链短板分析模型 | 经营效益 | 营业收入中位数 | 从环节经营效益识别投入与产出短板。 | MEDIAN(operating_revenue) 环节 vs 全链 | dwd_org_annual_financial_info(org_id, operating_revenue, year) — 环节营收 | 无 |
| 服务链短板分析模型 | 经营效益 | 销售利润率中位数 | 从环节经营效益识别投入与产出短板。 | MEDIAN(pure_profit / operating_revenue) 环节 vs 全链 | dwd_org_annual_financial_info(org_id, operating_revenue, pure_profit, year) — 利润率 | 无 |
| 服务链短板分析模型 | 服务类型结构 |  | 从服务类型是否齐全识别结构短板。 | 1 − 环节已出现类型数 / 6 | demo_gkxlumenx_ods.svc_org_card（service_type_candidate） | 无 |

## 源表字段

- dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 环节归属
- dwd_industry_chain_info(industry_code, industry_link_code) — 标准环节
- dwd_org_annual_financial_info(org_id, operating_revenue, pure_profit, year) — 经营效益
- demo_gkxlumenx_ads.svc_org_card（service_type_candidate）— 服务类型结构

## 待建字段

- svc_quality_score-环节服务质量评价

## 参考资料

合成评分+经济合作与发展组织+https://www.oecd.org/en/publications/handbook-on-constructing-composite-indicators-methodology-and-user-guide_9789264043466-en.html

服务质量+Texas A&M University+Parasuraman A, Zeithaml V A, Berry L L. SERVQUAL: a multiple-item scale for measuring consumer perceptions of service quality[J]. Journal of Retailing, 1988, 64(1): 12-40.
