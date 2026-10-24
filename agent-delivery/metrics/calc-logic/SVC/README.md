# calc-logic/SVC/ — 产业服务链域指标计算逻辑

> 生成任务：E-METRIC-ALGOLIB-LAUNCH-L01（阶段1）· 2026-10-23。本目录 = 口径细稿真源；
> 8 件套+version 以 `metrics/registry/cfg_metric-SVC-seed.yaml` 为准，四维就绪度以
> `metrics/registry/metric-readiness-matrix-SVC.yaml` 为准。条数：**51**
> （20261021 王惠批全量入库；支持度图例：直=完全直接支持，转=完全转换支持，部=部分支持，否=完全不支持）。

| # | 指标ID | 标题 | 算法类型 | 支持度 | 文件 |
|---|--------|------|----------|--------|------|
| 1 | `M_SVC_BASE_101_1` | 服务机构基础指标模型构建 | STAT | 部 | [M_SVC_BASE_101_1.md](./M_SVC_BASE_101_1.md) |
| 2 | `M_SVC_CHAIN_BOTTLENECK` | 瓶颈堵点判定 | MODEL | 部 | [M_SVC_CHAIN_BOTTLENECK.md](./M_SVC_CHAIN_BOTTLENECK.md) |
| 3 | `M_SVC_CHAIN_SEGMENT_AVG_DEPTH` | 环节平均服务深度 | STAT | 部 | [M_SVC_CHAIN_SEGMENT_AVG_DEPTH.md](./M_SVC_CHAIN_SEGMENT_AVG_DEPTH.md) |
| 4 | `M_SVC_CHAIN_SEGMENT_ORG_COUNT` | 环节服务机构数 | STAT | 部 | [M_SVC_CHAIN_SEGMENT_ORG_COUNT.md](./M_SVC_CHAIN_SEGMENT_ORG_COUNT.md) |
| 5 | `M_SVC_DEEP_172_1` | 服务链短板分析模型 | MODEL | 部 | [M_SVC_DEEP_172_1.md](./M_SVC_DEEP_172_1.md) |
| 6 | `M_SVC_DEEP_173_1` | 服务关系链模型 | MODEL | 部 | [M_SVC_DEEP_173_1.md](./M_SVC_DEEP_173_1.md) |
| 7 | `M_SVC_DEEP_174_1` | 金融服务机构技术力评价模型 | MODEL | 部 | [M_SVC_DEEP_174_1.md](./M_SVC_DEEP_174_1.md) |
| 8 | `M_SVC_DEEP_175_1` | 知识产权服务机构技术力评价模型 | MODEL | 部 | [M_SVC_DEEP_175_1.md](./M_SVC_DEEP_175_1.md) |
| 9 | `M_SVC_DEEP_176_1` | 人力资源服务机构技术力评价模型 | MODEL | 部 | [M_SVC_DEEP_176_1.md](./M_SVC_DEEP_176_1.md) |
| 10 | `M_SVC_DEEP_177_1` | 市场营销服务机构技术力评价模型 | MODEL | 部 | [M_SVC_DEEP_177_1.md](./M_SVC_DEEP_177_1.md) |
| 11 | `M_SVC_DEEP_178_1` | 咨询服务机构技术力评价模型 | MODEL | 部 | [M_SVC_DEEP_178_1.md](./M_SVC_DEEP_178_1.md) |
| 12 | `M_SVC_DEEP_179_1` | 科技创新服务机构技术力评价模型 | MODEL | 部 | [M_SVC_DEEP_179_1.md](./M_SVC_DEEP_179_1.md) |
| 13 | `M_SVC_DEEP_180_1` | 服务机构引入推荐模型 | MODEL | 部 | [M_SVC_DEEP_180_1.md](./M_SVC_DEEP_180_1.md) |
| 14 | `M_SVC_DEEP_181_1` | 服务机构培育推荐模型 | MODEL | 部 | [M_SVC_DEEP_181_1.md](./M_SVC_DEEP_181_1.md) |
| 15 | `M_SVC_GRAPH_112_1` | 服务机构实体识别构建 | GRAPH | 部 | [M_SVC_GRAPH_112_1.md](./M_SVC_GRAPH_112_1.md) |
| 16 | `M_SVC_GRAPH_113_1` | 服务机构实体关系抽取 | GRAPH | 部 | [M_SVC_GRAPH_113_1.md](./M_SVC_GRAPH_113_1.md) |
| 17 | `M_SVC_GRAPH_CENTRALITY` | 节点度中心性 | GRAPH | 部 | [M_SVC_GRAPH_CENTRALITY.md](./M_SVC_GRAPH_CENTRALITY.md) |
| 18 | `M_SVC_GRAPH_DENSITY` | 服务网络密度 | GRAPH | 部 | [M_SVC_GRAPH_DENSITY.md](./M_SVC_GRAPH_DENSITY.md) |
| 19 | `M_SVC_GRAPH_INFLUENCE` | 生态影响力评分 | MODEL | 部 | [M_SVC_GRAPH_INFLUENCE.md](./M_SVC_GRAPH_INFLUENCE.md) |
| 20 | `M_SVC_INDUSTRY_LAYOUT` | 全球服务机构产业布局 | STAT | 部 | [M_SVC_INDUSTRY_LAYOUT.md](./M_SVC_INDUSTRY_LAYOUT.md) |
| 21 | `M_SVC_INVEST_Y` | 服务机构投融资动态 | STAT | 部 | [M_SVC_INVEST_Y.md](./M_SVC_INVEST_Y.md) |
| 22 | `M_SVC_NEW_CNT` | 新增服务机构动态 | STAT | 部 | [M_SVC_NEW_CNT.md](./M_SVC_NEW_CNT.md) |
| 23 | `M_SVC_ORG_CNT` | 全球服务机构分布（按国家计数） | STAT | 部 | [M_SVC_ORG_CNT.md](./M_SVC_ORG_CNT.md) |
| 24 | `M_SVC_ORG_COVERAGE_BREADTH` | 服务广度 | STAT | 部 | [M_SVC_ORG_COVERAGE_BREADTH.md](./M_SVC_ORG_COVERAGE_BREADTH.md) |
| 25 | `M_SVC_ORG_COVERAGE_DEPTH` | 服务机构产业领域覆盖评分 | MODEL | 部 | [M_SVC_ORG_COVERAGE_DEPTH.md](./M_SVC_ORG_COVERAGE_DEPTH.md) |
| 26 | `M_SVC_ORG_MARKET_HEAT` | 市场热度评级 | MODEL | 部 | [M_SVC_ORG_MARKET_HEAT.md](./M_SVC_ORG_MARKET_HEAT.md) |
| 27 | `M_SVC_ORG_NEW_COUNT` | 年度新增服务机构数 | STAT | 部 | [M_SVC_ORG_NEW_COUNT.md](./M_SVC_ORG_NEW_COUNT.md) |
| 28 | `M_SVC_ORG_SELECTED_COUNT` | 当前分析机构数 | STAT | 否 | [M_SVC_ORG_SELECTED_COUNT.md](./M_SVC_ORG_SELECTED_COUNT.md) |
| 29 | `M_SVC_ORG_TECH_SCORE` | 服务机构影响力 | MODEL | 部 | [M_SVC_ORG_TECH_SCORE.md](./M_SVC_ORG_TECH_SCORE.md) |
| 30 | `M_SVC_ORG_TOTAL` | 入库服务机构总数 | STAT | 转 | [M_SVC_ORG_TOTAL.md](./M_SVC_ORG_TOTAL.md) |
| 31 | `M_SVC_PT_CHAIN_NODE_ORG` | 产业链节点服务机构数 | STAT | 部 | [M_SVC_PT_CHAIN_NODE_ORG.md](./M_SVC_PT_CHAIN_NODE_ORG.md) |
| 32 | `M_SVC_PT_GLOBAL_SCALE_DIST` | 全球服务机构规模分布 | STAT | 部 | [M_SVC_PT_GLOBAL_SCALE_DIST.md](./M_SVC_PT_GLOBAL_SCALE_DIST.md) |
| 33 | `M_SVC_PT_GLOBAL_TOTAL` | 全球服务机构总数 | STAT | 部 | [M_SVC_PT_GLOBAL_TOTAL.md](./M_SVC_PT_GLOBAL_TOTAL.md) |
| 34 | `M_SVC_PT_GLOBAL_TYPE_DIST` | 全球服务机构类型分布 | STAT | 部 | [M_SVC_PT_GLOBAL_TYPE_DIST.md](./M_SVC_PT_GLOBAL_TYPE_DIST.md) |
| 35 | `M_SVC_PT_KEYORG_SCALE` | 重点机构规模档案值 | STAT | 部 | [M_SVC_PT_KEYORG_SCALE.md](./M_SVC_PT_KEYORG_SCALE.md) |
| 36 | `M_SVC_PT_REGION_ORG` | 区域服务机构数 | STAT | 部 | [M_SVC_PT_REGION_ORG.md](./M_SVC_PT_REGION_ORG.md) |
| 37 | `M_SVC_PT_SZ_FIELD_DIST` | 深圳机构产业领域分布 | STAT | 部 | [M_SVC_PT_SZ_FIELD_DIST.md](./M_SVC_PT_SZ_FIELD_DIST.md) |
| 38 | `M_SVC_PT_SZ_REGION_ORG` | 深圳机构区域分布 | STAT | 转 | [M_SVC_PT_SZ_REGION_ORG.md](./M_SVC_PT_SZ_REGION_ORG.md) |
| 39 | `M_SVC_PT_SZ_TOTAL` | 深圳产业服务机构数量 | STAT | 转 | [M_SVC_PT_SZ_TOTAL.md](./M_SVC_PT_SZ_TOTAL.md) |
| 40 | `M_SVC_PT_SZ_TYPE_DIST` | 深圳服务机构类型分布 | STAT | 部 | [M_SVC_PT_SZ_TYPE_DIST.md](./M_SVC_PT_SZ_TYPE_DIST.md) |
| 41 | `M_SVC_REC_ATTRACT_SCORE` | 招引综合评分 | MODEL | 部 | [M_SVC_REC_ATTRACT_SCORE.md](./M_SVC_REC_ATTRACT_SCORE.md) |
| 42 | `M_SVC_REC_CANDIDATE_CNT` | 候选机构数 | STAT | 否 | [M_SVC_REC_CANDIDATE_CNT.md](./M_SVC_REC_CANDIDATE_CNT.md) |
| 43 | `M_SVC_REC_CULTIVATE_SCORE` | 培育综合评分 | MODEL | 部 | [M_SVC_REC_CULTIVATE_SCORE.md](./M_SVC_REC_CULTIVATE_SCORE.md) |
| 44 | `M_SVC_RELATION_DENSITY` | 服务关系链密度 | STAT | 部 | [M_SVC_RELATION_DENSITY.md](./M_SVC_RELATION_DENSITY.md) |
| 45 | `M_SVC_RELATION_RISK` | 服务关系风险 | STAT | 部 | [M_SVC_RELATION_RISK.md](./M_SVC_RELATION_RISK.md) |
| 46 | `M_SVC_SZ_CHAIN_COMPLETENESS` | 服务链完整度 | STAT | 否 | [M_SVC_SZ_CHAIN_COMPLETENESS.md](./M_SVC_SZ_CHAIN_COMPLETENESS.md) |
| 47 | `M_SVC_SZ_COMPARE_METRIC` | 城市对比指标值 | STAT | 部 | [M_SVC_SZ_COMPARE_METRIC.md](./M_SVC_SZ_COMPARE_METRIC.md) |
| 48 | `M_SVC_SZ_DISTRICT` | 深圳服务机构分布 | STAT | 转 | [M_SVC_SZ_DISTRICT.md](./M_SVC_SZ_DISTRICT.md) |
| 49 | `M_SVC_SZ_SCALE` | 深圳服务机构规模 | STAT | 转 | [M_SVC_SZ_SCALE.md](./M_SVC_SZ_SCALE.md) |
| 50 | `M_SVC_SZ_TIER` | 深圳梯队位置 | MODEL | 部 | [M_SVC_SZ_TIER.md](./M_SVC_SZ_TIER.md) |
| 51 | `M_SVC_TYPE_DIST_QUERY` | 查询结果·服务类型分布 | STAT | 部 | [M_SVC_TYPE_DIST_QUERY.md](./M_SVC_TYPE_DIST_QUERY.md) |
