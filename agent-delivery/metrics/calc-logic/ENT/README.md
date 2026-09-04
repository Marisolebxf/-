# calc-logic/ENT/ —— 企业域指标计算逻辑真源（王惠口径）

> **真源**：王惠《企业分析模型指标字段清单》20260816 底稿（Excel 工作底稿，不进 git）。
> **本目录**：底稿经 data-agent 正式化后的 md 文件，供编排智能体（Cursor 等）按需读取。
> **生成日期**：2026-08-18
> **入库更新**：2026-08-26 按《指标入库操作指南》重入 14 个 MODEL/MIXED 指标（王惠三大模块正式口径，覆盖占位 md）。
> ****指标总数**：71 个唯一指标 ID（134 行，含 9 个多级子指标）

## 文件清单

| # | 指标ID | 指标名称 | 子指标行数 | 对齐状态 | 是否在数据库 | 文件 |
|---|--------|---------|-----------|---------|------------|------|
| 1 | `M_ENT_TOTAL_COUNT` | 企业总数 | 1 | 已对齐 | 是 | [M_ENT_TOTAL_COUNT.md](./M_ENT_TOTAL_COUNT.md) |
| 2 | `M_ENT_RESEARCHER_COUNT` | 企业科研人数 | 1 | 未对齐 | 是 | [M_ENT_RESEARCHER_COUNT.md](./M_ENT_RESEARCHER_COUNT.md) |
| 3 | `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT` | 覆盖未来产业数 | 1 | 未对齐 | 是 | [M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT.md](./M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT.md) |
| 4 | `M_ENT_REGIONAL_COUNT` | 区域企业数 | 1 | 已对齐 | 是 | [M_ENT_REGIONAL_COUNT.md](./M_ENT_REGIONAL_COUNT.md) |
| 5 | `M_ENT_STAR_PATENT_COUNT` | 明星企业专利数 | 1 | 部分对齐 | 是 | [M_ENT_STAR_PATENT_COUNT.md](./M_ENT_STAR_PATENT_COUNT.md) |
| 6 | `M_ENT_STAR_RD_RATIO` | 研发投入占比 | 1 | 已对齐 | 是 | [M_ENT_STAR_RD_RATIO.md](./M_ENT_STAR_RD_RATIO.md) |
| 7 | `M_ENT_SZ_COUNT` | 深圳企业数 | 1 | 已对齐 | 是 | [M_ENT_SZ_COUNT.md](./M_ENT_SZ_COUNT.md) |
| 8 | `M_ENT_SZ_SCALE_DIST` | 深圳企业规模分布 | 1 | 部分对齐 | 是 | [M_ENT_SZ_SCALE_DIST.md](./M_ENT_SZ_SCALE_DIST.md) |
| 9 | `M_ENT_STATE_OWNED_COUNT` | 国有企业数 | 1 | 部分对齐 | 是 | [M_ENT_STATE_OWNED_COUNT.md](./M_ENT_STATE_OWNED_COUNT.md) |
| 10 | `M_ENT_NEW_COUNT_Y` | 历年新增企业数 | 1 | 未对齐 | 是 | [M_ENT_NEW_COUNT_Y.md](./M_ENT_NEW_COUNT_Y.md) |
| 11 | `M_ENT_HIGH_TECH_COUNT` | 高企数量 | 1 | 未对齐 | 是 | [M_ENT_HIGH_TECH_COUNT.md](./M_ENT_HIGH_TECH_COUNT.md) |
| 12 | `M_ENT_INNOVATIVE_COUNT` | 创新型企业数 | 1 | 未对齐 | 是 | [M_ENT_INNOVATIVE_COUNT.md](./M_ENT_INNOVATIVE_COUNT.md) |
| 13 | `M_ENT_AVG_RD_INVESTMENT` | 平均研发投入 | 1 | 部分对齐 | 是 | [M_ENT_AVG_RD_INVESTMENT.md](./M_ENT_AVG_RD_INVESTMENT.md) |
| 14 | `M_ENT_PATENT_TOTAL` | 专利总量 | 1 | 部分对齐 | 是 | [M_ENT_PATENT_TOTAL.md](./M_ENT_PATENT_TOTAL.md) |
| 15 | `M_ENT_SEARCH_RESULT_COUNT` | 检索命中企业数 | 1 | 已对齐 | 是 | [M_ENT_SEARCH_RESULT_COUNT.md](./M_ENT_SEARCH_RESULT_COUNT.md) |
| 16 | `M_ENT_REVENUE_LATEST` | 营收 | 1 | 已对齐 | 是 | [M_ENT_REVENUE_LATEST.md](./M_ENT_REVENUE_LATEST.md) |
| 17 | `M_ENT_PATENT_VALID_COUNT` | 有效专利数 | 1 | 部分对齐 | 是 | [M_ENT_PATENT_VALID_COUNT.md](./M_ENT_PATENT_VALID_COUNT.md) |
| 18 | `M_ENT_TECH_SCORE` | 技术力分 | 1 | 未对齐 | 部分 | [M_ENT_TECH_SCORE.md](./M_ENT_TECH_SCORE.md) |
| 19 | `M_ENT_BUSINESS_SCORE` | 商业力分 | 1 | 未对齐 | 部分 | [M_ENT_BUSINESS_SCORE.md](./M_ENT_BUSINESS_SCORE.md) |
| 20 | `M_ENT_TYPE_COUNT` | 各类型企业数 | 1 | 未对齐 | 是 | [M_ENT_TYPE_COUNT.md](./M_ENT_TYPE_COUNT.md) |
| 21 | `M_ENT_TYPE_RATIO` | 企业类型占比 | 1 | 已对齐 | 是 | [M_ENT_TYPE_RATIO.md](./M_ENT_TYPE_RATIO.md) |
| 22 | `M_ENT_CLUSTER_INDEX` | 企业集聚指数 | 1 | 未对齐 | 是 | [M_ENT_CLUSTER_INDEX.md](./M_ENT_CLUSTER_INDEX.md) |
| 23 | `M_ENT_DOMAIN_COVERAGE_COUNT` | 覆盖领域数 | 1 | 已对齐 | 是 | [M_ENT_DOMAIN_COVERAGE_COUNT.md](./M_ENT_DOMAIN_COVERAGE_COUNT.md) |
| 24 | `M_ENT_DOMAIN_COVERAGE_BREADTH` | 领域覆盖广度 | 1 | 未对齐 | 是 | [M_ENT_DOMAIN_COVERAGE_BREADTH.md](./M_ENT_DOMAIN_COVERAGE_BREADTH.md) |
| 25 | `M_ENT_DOMAIN_COVERAGE_DEPTH` | 领域覆盖深度 | 1 | 未对齐 | 是 | [M_ENT_DOMAIN_COVERAGE_DEPTH.md](./M_ENT_DOMAIN_COVERAGE_DEPTH.md) |
| 26 | `M_ENT_DIVERSIFICATION_INDEX` | 多元化指数 | 1 | 未对齐 | 是 | [M_ENT_DIVERSIFICATION_INDEX.md](./M_ENT_DIVERSIFICATION_INDEX.md) |
| 27 | `M_ENT_TECH_POWER_SCORE` | 技术力得分 | 12 | 未对齐 | 部分 | [M_ENT_TECH_POWER_SCORE.md](./M_ENT_TECH_POWER_SCORE.md) |
| 28 | `M_ENT_TECH_RANK` | 技术力排名 | 1 | 未对齐 | 否 | [M_ENT_TECH_RANK.md](./M_ENT_TECH_RANK.md) |
| 29 | `M_ENT_PATENT_GRANT_COUNT` | 专利授权量 | 1 | 部分对齐 | 是 | [M_ENT_PATENT_GRANT_COUNT.md](./M_ENT_PATENT_GRANT_COUNT.md) |
| 30 | `M_ENT_RD_INVESTMENT_RATIO` | 研发投入强度 | 1 | 已对齐 | 是 | [M_ENT_RD_INVESTMENT_RATIO.md](./M_ENT_RD_INVESTMENT_RATIO.md) |
| 31 | `M_ENT_RD_INVEST_AVG` | 平均研发投入 | 1 | 部分对齐 | 是 | [M_ENT_RD_INVEST_AVG.md](./M_ENT_RD_INVEST_AVG.md) |
| 32 | `M_ENT_BUSINESS_POWER_SCORE` | 商业力得分 | 13 | 未对齐 | 部分 | [M_ENT_BUSINESS_POWER_SCORE.md](./M_ENT_BUSINESS_POWER_SCORE.md) |
| 33 | `M_ENT_REVENUE_GROWTH_RATE` | 营业收入增长率 | 1 | 已对齐 | 是 | [M_ENT_REVENUE_GROWTH_RATE.md](./M_ENT_REVENUE_GROWTH_RATE.md) |
| 34 | `M_ENT_PROFIT_MARGIN` | 利润率 | 1 | 已对齐 | 是 | [M_ENT_PROFIT_MARGIN.md](./M_ENT_PROFIT_MARGIN.md) |
| 35 | `M_ENT_MARKET_SHARE` | 市场份额 | 1 | 未对齐 | 是 | [M_ENT_MARKET_SHARE.md](./M_ENT_MARKET_SHARE.md) |
| 36 | `M_ENT_COMPETITIVENESS_SCORE` | 综合竞争力得分 | 10 | 未对齐 | 部分 | [M_ENT_COMPETITIVENESS_SCORE.md](./M_ENT_COMPETITIVENESS_SCORE.md) |
| 37 | `M_ENT_COMPETITIVENESS_RANK` | 综合竞争力排名 | 1 | 未对齐 | 否 | [M_ENT_COMPETITIVENESS_RANK.md](./M_ENT_COMPETITIVENESS_RANK.md) |
| 38 | `M_ENT_SHORTBOARD_COUNT` | 短板指标数 | 1 | 未对齐 | 部分 | [M_ENT_SHORTBOARD_COUNT.md](./M_ENT_SHORTBOARD_COUNT.md) |
| 39 | `M_ENT_INNOVATION_INDEX` | 创新能力指数 | 18 | 未对齐 | 部分 | [M_ENT_INNOVATION_INDEX.md](./M_ENT_INNOVATION_INDEX.md) |
| 40 | `M_ENT_CHAIN_COMPLETENESS` | 产业链完整度 | 1 | 已对齐 | 是 | [M_ENT_CHAIN_COMPLETENESS.md](./M_ENT_CHAIN_COMPLETENESS.md) |
| 41 | `M_ENT_CITY_RANK` | 多城市对标排名 | 4 | 未对齐 | 部分 | [M_ENT_CITY_RANK.md](./M_ENT_CITY_RANK.md) |
| 42 | `M_ENT_CITY_AVG_TECH_POWER` | 城市平均技术力 | 1 | 未对齐 | 部分 | [M_ENT_CITY_AVG_TECH_POWER.md](./M_ENT_CITY_AVG_TECH_POWER.md) |
| 43 | `M_ENT_CITY_DENSITY` | 城市企业密度 | 1 | 未对齐 | 是 | [M_ENT_CITY_DENSITY.md](./M_ENT_CITY_DENSITY.md) |
| 44 | `M_ENT_PAINPOINT_COUNT` | 痛难点反映企业数 | 7 | 未对齐 | 部分 | [M_ENT_PAINPOINT_COUNT.md](./M_ENT_PAINPOINT_COUNT.md) |
| 45 | `M_ENT_PAINPOINT_SEVERITY` | 痛难点严重度 | 1 | 未对齐 | 否 | [M_ENT_PAINPOINT_SEVERITY.md](./M_ENT_PAINPOINT_SEVERITY.md) |
| 46 | `M_ENT_SUPPLIER_COUNT` | 供应商节点数 | 1 | 未对齐 | 否 | [M_ENT_SUPPLIER_COUNT.md](./M_ENT_SUPPLIER_COUNT.md) |
| 47 | `M_ENT_NODE_CENTRALITY` | 供应链中心性 | 1 | 未对齐 | 否 | [M_ENT_NODE_CENTRALITY.md](./M_ENT_NODE_CENTRALITY.md) |
| 48 | `M_ENT_SUPPLY_CHAIN_RISK` | 断链风险等级 | 1 | 未对齐 | 部分 | [M_ENT_SUPPLY_CHAIN_RISK.md](./M_ENT_SUPPLY_CHAIN_RISK.md) |
| 49 | `M_ENT_ATTRACTION_INDEX` | 招引推荐指数 | 6 | 未对齐 | 部分 | [M_ENT_ATTRACTION_INDEX.md](./M_ENT_ATTRACTION_INDEX.md) |
| 50 | `M_ENT_CULTIVATION_INDEX` | 培育推荐指数 | 7 | 未对齐 | 是 | [M_ENT_CULTIVATION_INDEX.md](./M_ENT_CULTIVATION_INDEX.md) |
| 51 | `M_ENT_INDUSTRY_MATCH_SCORE` | 产业匹配度 | 1 | 未对齐 | 部分 | [M_ENT_INDUSTRY_MATCH_SCORE.md](./M_ENT_INDUSTRY_MATCH_SCORE.md) |
| 52 | `M_ENT_GROWTH_POTENTIAL` | 成长潜力 | 4 | 未对齐 | 是 | [M_ENT_GROWTH_POTENTIAL.md](./M_ENT_GROWTH_POTENTIAL.md) |
| 53 | `M_ENT_CHAIN_STAGE_COVERAGE` | 产业链环节覆盖 | 1 | 部分对齐 | 是 | [M_ENT_CHAIN_STAGE_COVERAGE.md](./M_ENT_CHAIN_STAGE_COVERAGE.md) |
| 54 | `M_ENT_KEY_NODE_COUNT` | 关键节点数 | 1 | 部分对齐 | 是 | [M_ENT_KEY_NODE_COUNT.md](./M_ENT_KEY_NODE_COUNT.md) |
| 55 | `M_ENT_KEY_TOTAL` | 重点企业总数 | 1 | 部分对齐 | 是 | [M_ENT_KEY_TOTAL.md](./M_ENT_KEY_TOTAL.md) |
| 56 | `M_ENT_REGION_COVERAGE` | 区域覆盖数 | 1 | 已对齐 | 是 | [M_ENT_REGION_COVERAGE.md](./M_ENT_REGION_COVERAGE.md) |
| 57 | `M_ENT_REGION_HOT_COUNT` | 区域热点企业数 | 1 | 已对齐 | 是 | [M_ENT_REGION_HOT_COUNT.md](./M_ENT_REGION_HOT_COUNT.md) |
| 58 | `M_ENT_KEYPANO_DOMAIN_SUMMARY` | 重点企业全景图 | 1 | 部分对齐 | 部分 | [M_ENT_KEYPANO_DOMAIN_SUMMARY.md](./M_ENT_KEYPANO_DOMAIN_SUMMARY.md) |
| 59 | `M_ENT_KEYPANO_ENTERPRISE_LIST` | 重点企业全景图 | 1 | 部分对齐 | 部分 | [M_ENT_KEYPANO_ENTERPRISE_LIST.md](./M_ENT_KEYPANO_ENTERPRISE_LIST.md) |
| 60 | `M_ENT_KEYPANO_QUAL_DISTRIBUTION` | 重点企业全景图 | 1 | 部分对齐 | 部分 | [M_ENT_KEYPANO_QUAL_DISTRIBUTION.md](./M_ENT_KEYPANO_QUAL_DISTRIBUTION.md) |
| 61 | `M_ENT_AGGLOMERATION_INDEX` | 集聚指数 | 1 | 部分对齐 | 是 | [M_ENT_AGGLOMERATION_INDEX.md](./M_ENT_AGGLOMERATION_INDEX.md) |
| 62 | `M_ENT_CITY_COMPARE_TOPIC` | 多城市企业群对标值 | 1 | 部分对齐 | 部分 | [M_ENT_CITY_COMPARE_TOPIC.md](./M_ENT_CITY_COMPARE_TOPIC.md) |
| 63 | `M_ENT_DEEP_142_1` | 企业发展历程模型 | 1 | 部分对齐 | 部分 | [M_ENT_DEEP_142_1.md](./M_ENT_DEEP_142_1.md) |
| 64 | `M_ENT_DS_02_ENTITY_004` | [新增] 技术点影响力 | 1 | 未对齐 | 部分 | [M_ENT_DS_02_ENTITY_004.md](./M_ENT_DS_02_ENTITY_004.md) |
| 65 | `M_ENT_DS_07_INDUSTRY_POTENTIAL_004` | 科学影响力评估 | 1 | 部分对齐 | 部分 | [M_ENT_DS_07_INDUSTRY_POTENTIAL_004.md](./M_ENT_DS_07_INDUSTRY_POTENTIAL_004.md) |
| 66 | `M_ENT_DS_07_INDUSTRY_POTENTIAL_005` | 技术影响力评估 | 1 | 部分对齐 | 部分 | [M_ENT_DS_07_INDUSTRY_POTENTIAL_005.md](./M_ENT_DS_07_INDUSTRY_POTENTIAL_005.md) |
| 67 | `M_ENT_DS_07_INDUSTRY_POTENTIAL_006` | 产业发展潜力综合评估 | 1 | 部分对齐 | 部分 | [M_ENT_DS_07_INDUSTRY_POTENTIAL_006.md](./M_ENT_DS_07_INDUSTRY_POTENTIAL_006.md) |
| 68 | `M_ENT_PAINPOINT_GAP` | 痛难点改进差距 | 1 | 部分对齐 | 部分 | [M_ENT_PAINPOINT_GAP.md](./M_ENT_PAINPOINT_GAP.md) |
| 69 | `M_ENT_PAINPOINT_TOPIC` | 发展痛难点诊断 | 1 | 部分对齐 | 部分 | [M_ENT_PAINPOINT_TOPIC.md](./M_ENT_PAINPOINT_TOPIC.md) |
| 70 | `M_ENT_POLICY_MATCH_SCORE` | 政策匹配度 | 1 | 未对齐 | 部分 | [M_ENT_POLICY_MATCH_SCORE.md](./M_ENT_POLICY_MATCH_SCORE.md) |
| 71 | `M_ENT_RELATION_STRENGTH` | 关系强度 | 1 | 部分对齐 | 部分 | [M_ENT_RELATION_STRENGTH.md](./M_ENT_RELATION_STRENGTH.md) |

## 多级子指标说明

以下 9 个指标 ID 含 L2/L3 子指标，已合并为单文件（文件内按 L1→L2→L3 分节）：

| 指标ID | 指标名称 | 子指标行数 | L2 维度数 |
|--------|---------|-----------|----------|
| `M_ENT_TECH_POWER_SCORE` | 技术力得分 | 12 | 5 |
| `M_ENT_BUSINESS_POWER_SCORE` | 商业力得分 | 13 | 6 |
| `M_ENT_COMPETITIVENESS_SCORE` | 综合竞争力得分 | 10 | 4 |
| `M_ENT_INNOVATION_INDEX` | 创新能力指数 | 18 | 3 |
| `M_ENT_CITY_RANK` | 多城市对标排名 | 4 | 3 |
| `M_ENT_PAINPOINT_COUNT` | 痛难点反映企业数 | 7 | 4 |
| `M_ENT_ATTRACTION_INDEX` | 招引推荐指数 | 6 | 3 |
| `M_ENT_CULTIVATION_INDEX` | 培育推荐指数 | 7 | 3 |
| `M_ENT_GROWTH_POTENTIAL` | 成长潜力 | 4 | 3 |

## 维护规则

1. **口径变更流程**：王惠更新 Excel 底稿 → data-agent 重新生成对应 md 文件 → commit message 标 `[agent:data-agent]` 并注明「正式化自 王惠 {日期} Excel 底稿」
2. **与 seed yaml 的关系**：`cfg_metric-ENT-seed.yaml` 中的 `calc_logic_ref` 字段指向本目录下的 md 文件路径
3. **Excel 底稿不进 git**：符合 `metrics/README.md` §2 政策
4. **文件命名**：`{metric_id}.md`，与 `metric_id` 一一对应
5. **多级指标合并**：同一 `metric_id` 的所有 L1/L2/L3 行合并为单文件，文件内按层级分节
