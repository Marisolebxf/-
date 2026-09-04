# 多城市企业群对标值（M_ENT_CITY_COMPARE_TOPIC）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_CITY_COMPARE_TOPIC |
| 指标名称 | 多城市企业群对标值 |
| 一级模块 | 企业分析 |
| 二级模块 | 重点企业类型分析 |
| 三级模块 | - |
| 更新频率 | 周（随评分批次） |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q009 / Q016 / Q077 |

## 口径定义

统计窗口默认自然年。将深圳企业群与对照城市集合（北京/上海/苏州等，Q016 待甲方确认）横向对标，按城市聚合输出平均技术力、平均商业力、企业密度等城市对标值。对象=城市企业群的聚合值，不是单家企业。对照集合默认全国加权参照（Q-MO-ENT-06）。

## 计算逻辑说明

按城市 `GROUP BY` 聚合三类对标值，各自独立产出、不合并为一个总分。

### 第一步：入集

企业落到城市：优先 `enterprise_base.region_id` 市码 `LEFT(region_id,4)`；无该列时以 `dwd_org_base_info.city` 中文名对齐（缺列缺口与 `M_ENT_REGIONAL_COUNT` 一致）。已出分企业进均；无分不进均。

### 第二步：三个对标项

1. **平均技术力** = `AVG(tech_power_index)`，五维分项同法 `AVG(talent/innovation/transfer/cooperation/investment_score)`。
2. **平均商业力** = `AVG(biz_power_index)`，六维分项同法。
3. **企业密度** = `COUNT(DISTINCT 企业)` ÷ 城市辖区面积，单位 家/km²。

产业筛选：当前筛选产业 ∩ 已出分企业再聚合。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 多城市企业群对标值 | 平均技术力 | 城市平均技术力指数 | 城市企业群技术力指数算术平均。 | AVG(tech_power_index) | tech_power(org_id, enterprise_name, headquarters_city, talent_score, innovation_score, transfer_score, cooperation_score, investment_score, tech_power_index) — 技术力评分；dwd_org_base_info(org_id, external_id, city, province, area) — 城市入集 | 无 |
|  |  | 技术力五维分项均值 | 人才/创新/转化/合作/投入五维均值。 | AVG(各维 score) | tech_power(org_id, talent_score, innovation_score, transfer_score, cooperation_score, investment_score) — 技术力五维 | 无 |
| 多城市企业群对标值 | 平均商业力 | 城市平均商业力指数 | 城市企业群商业力指数算术平均。 | AVG(biz_power_index) | biz_power(org_id, enterprise_name, headquarters_city, market_score, product_score, brand_score, cooperation_score, chain_coverage_score, chain_keynode_score, biz_power_index) — 商业力评分；dwd_org_base_info(org_id, external_id, city, province, area) — 城市入集 | 无 |
|  |  | 商业力六维分项均值 | 市场/产品/品牌/合作/链覆盖/关键节点六维均值。 | AVG(各维 score) | biz_power(org_id, market_score, product_score, brand_score, cooperation_score, chain_coverage_score, chain_keynode_score) — 商业力六维 | 无 |
| 多城市企业群对标值 | 企业密度 | 城市企业密度 | 城市企业去重数 ÷ 城市辖区面积。 | COUNT(DISTINCT 企业)/面积 | dwd_org_base_info(org_id, external_id, city, province, area) — 企业密度分子 | 城市辖区面积字段 |
|  |  | 目标产业企业密度 | 目标产业企业去重数 ÷ 城市辖区面积。 | COUNT(DISTINCT 产业内企业)/面积 | dwd_org_base_info(org_id, external_id, city, province, area, industry_l1_code, industry_l2_code) — 产业内企业密度分子；dwd_org_industry_tags(credit_code, industry_code) — 产业归类 | 城市辖区面积字段 |

## 源表字段

- tech_power(org_id, enterprise_name, headquarters_city, talent_score, innovation_score, transfer_score, cooperation_score, investment_score, tech_power_index) — 技术力评分（ADS，依赖 M_ENT_TECH_POWER_SCORE）
- biz_power(org_id, enterprise_name, headquarters_city, market_score, product_score, brand_score, cooperation_score, chain_coverage_score, chain_keynode_score, biz_power_index) — 商业力评分（ADS，依赖 M_ENT_BUSINESS_POWER_SCORE）
- dwd_org_base_info(org_id, external_id, city, province, area, industry_l1_code, industry_l2_code) — 企业城市入集+产业归类
- dwd_org_industry_tags(credit_code, industry_code) — 企业与产业链归类

## 待建字段

- 城市辖区面积字段：`gkxlumenx_dim.code_region.area` 现网全 NULL，需灌数或另建城市面积表；灌入前「企业密度」无法产出。
- 对标城市集合（Q016）：待甲方确认，未闭合前只用已有 city_code 行。
- 主档 `enterprise_base.region_id` 缺列：以 `city` 中文名暂代（缺口同 `M_ENT_REGIONAL_COUNT`）。

## 参考资料

[1] 深圳企业现状分析·多城市横向对标分析 | 需规 SRS《企业分析.md》序号48 | 平均技术力/商业力/企业密度 | 关联 Q009 / Q016 / Q077。

[2] 城市平均技术力 | 王惠已入库指标 M_ENT_CITY_AVG_TECH_POWER（AVG(tech_power_index) 口径对齐）。

[3] 城市企业密度 | 王惠已入库指标 M_ENT_CITY_DENSITY（企业数/城市面积口径对齐）。
