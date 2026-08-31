# calc-logic/SVC/ — 产业服务域指标计算逻辑

> 迁入：2026-08-22 自 `lumen-algo-py/docs/metrics/` 指标计算逻辑-V1。本目录 = 口径细稿真源；8 件套仍以根目录 seed / 就绪度矩阵为准。
> 2026-08-31 更新：按王惠调研结果（`指标建模任务/王惠阶段性成果/20260829_产业服务分析`）入库 18 个 MODEL 指标，覆盖旧口径并新增 M_SVC_DEEP_* 系列。
> 条数：**39**

## 本轮入库（王惠 20260829，MODEL）

| # | 指标ID | 标题 | 算法类型 | 文件 |
|---|--------|------|----------|------|
| 1 | 🔸 `M_SVC_CHAIN_BOTTLENECK` | 瓶颈堵点判定 | MODEL | [MD](./M_SVC_CHAIN_BOTTLENECK.md) |
| 2 | 🔸 `M_SVC_GRAPH_INFLUENCE` | 生态影响力评分 | MODEL | [MD](./M_SVC_GRAPH_INFLUENCE.md) |
| 3 | 🔸 `M_SVC_ORG_COVERAGE_DEPTH` | 服务机构产业领域覆盖评分 | MODEL | [MD](./M_SVC_ORG_COVERAGE_DEPTH.md) |
| 4 | 🔸 `M_SVC_ORG_MARKET_HEAT` | 市场热度评级 | MODEL | [MD](./M_SVC_ORG_MARKET_HEAT.md) |
| 5 | 🔸 `M_SVC_ORG_TECH_SCORE` | 服务机构影响力 | MODEL | [MD](./M_SVC_ORG_TECH_SCORE.md) |
| 6 | 🔸 `M_SVC_REC_ATTRACT_SCORE` | 招引综合评分 | MODEL | [MD](./M_SVC_REC_ATTRACT_SCORE.md) |
| 7 | 🔸 `M_SVC_REC_CULTIVATE_SCORE` | 培育综合评分 | MODEL | [MD](./M_SVC_REC_CULTIVATE_SCORE.md) |
| 8 | 🔸 `M_SVC_SZ_TIER` | 深圳梯队位置 | MODEL | [MD](./M_SVC_SZ_TIER.md) |
| 9 | 🔸 `M_SVC_DEEP_172_1` | 服务链短板分析模型 | MODEL | [MD](./M_SVC_DEEP_172_1.md) |
| 10 | 🔸 `M_SVC_DEEP_173_1` | 服务关系链模型 | MODEL | [MD](./M_SVC_DEEP_173_1.md) |
| 11 | 🔸 `M_SVC_DEEP_174_1` | 金融服务机构技术力评价模型 | MODEL | [MD](./M_SVC_DEEP_174_1.md) |
| 12 | 🔸 `M_SVC_DEEP_175_1` | 知识产权服务机构技术力评价模型 | MODEL | [MD](./M_SVC_DEEP_175_1.md) |
| 13 | 🔸 `M_SVC_DEEP_176_1` | 人力资源服务机构技术力评价模型 | MODEL | [MD](./M_SVC_DEEP_176_1.md) |
| 14 | 🔸 `M_SVC_DEEP_177_1` | 市场营销服务机构技术力评价模型 | MODEL | [MD](./M_SVC_DEEP_177_1.md) |
| 15 | 🔸 `M_SVC_DEEP_178_1` | 咨询服务机构技术力评价模型 | MODEL | [MD](./M_SVC_DEEP_178_1.md) |
| 16 | 🔸 `M_SVC_DEEP_179_1` | 科技创新服务机构技术力评价模型 | MODEL | [MD](./M_SVC_DEEP_179_1.md) |
| 17 | 🔸 `M_SVC_DEEP_180_1` | 服务机构引入推荐模型 | MODEL | [MD](./M_SVC_DEEP_180_1.md) |
| 18 | 🔸 `M_SVC_DEEP_181_1` | 服务机构培育推荐模型 | MODEL | [MD](./M_SVC_DEEP_181_1.md) |

## 既有指标（历史批次，未在本轮更新）

| # | 指标ID | 标题 | 算法类型 | 文件 |
|---|--------|------|----------|------|
| 1 |    `M_SVC_CHAIN_SEGMENT_AVG_DEPTH` | 环节平均服务深度 | STAT | [MD](./M_SVC_CHAIN_SEGMENT_AVG_DEPTH.md) |
| 2 |    `M_SVC_CHAIN_SEGMENT_ORG_COUNT` | 环节服务机构数 | STAT | [MD](./M_SVC_CHAIN_SEGMENT_ORG_COUNT.md) |
| 3 |    `M_SVC_GRAPH_CENTRALITY` | 节点度中心性 | GRAPH | [MD](./M_SVC_GRAPH_CENTRALITY.md) |
| 4 |    `M_SVC_GRAPH_DENSITY` | 服务网络密度 | GRAPH | [MD](./M_SVC_GRAPH_DENSITY.md) |
| 5 |    `M_SVC_ORG_COVERAGE_BREADTH` | 服务广度(覆盖领域数) | STAT | [MD](./M_SVC_ORG_COVERAGE_BREADTH.md) |
| 6 |    `M_SVC_ORG_NEW_COUNT` | 年度新增服务机构数 | STAT | [MD](./M_SVC_ORG_NEW_COUNT.md) |
| 7 |    `M_SVC_ORG_SELECTED_COUNT` | 当前分析机构数 | STAT | [MD](./M_SVC_ORG_SELECTED_COUNT.md) |
| 8 |    `M_SVC_ORG_TOTAL` | 入库服务机构总数 | STAT | [MD](./M_SVC_ORG_TOTAL.md) |
| 9 |    `M_SVC_PT_CHAIN_NODE_ORG` | 产业链节点服务机构数 | STAT | [MD](./M_SVC_PT_CHAIN_NODE_ORG.md) |
| 10 |    `M_SVC_PT_GLOBAL_SCALE_DIST` | 全球服务机构规模分布 | STAT | [MD](./M_SVC_PT_GLOBAL_SCALE_DIST.md) |
| 11 |    `M_SVC_PT_GLOBAL_TOTAL` | 全球服务机构总数 | STAT | [MD](./M_SVC_PT_GLOBAL_TOTAL.md) |
| 12 |    `M_SVC_PT_GLOBAL_TYPE_DIST` | 全球服务机构类型分布 | STAT | [MD](./M_SVC_PT_GLOBAL_TYPE_DIST.md) |
| 13 |    `M_SVC_PT_KEYORG_SCALE` | 重点机构规模档案值 | STAT | [MD](./M_SVC_PT_KEYORG_SCALE.md) |
| 14 |    `M_SVC_PT_REGION_ORG` | 区域服务机构数 | STAT | [MD](./M_SVC_PT_REGION_ORG.md) |
| 15 |    `M_SVC_PT_SZ_FIELD_DIST` | 深圳机构产业领域分布 | STAT | [MD](./M_SVC_PT_SZ_FIELD_DIST.md) |
| 16 |    `M_SVC_PT_SZ_REGION_ORG` | 深圳机构区域分布 | STAT | [MD](./M_SVC_PT_SZ_REGION_ORG.md) |
| 17 |    `M_SVC_PT_SZ_TOTAL` | 深圳产业服务机构数量 | STAT | [MD](./M_SVC_PT_SZ_TOTAL.md) |
| 18 |    `M_SVC_PT_SZ_TYPE_DIST` | 深圳机构类型统计 | STAT | [MD](./M_SVC_PT_SZ_TYPE_DIST.md) |
| 19 |    `M_SVC_REC_CANDIDATE_CNT` | 候选机构数 | STAT | [MD](./M_SVC_REC_CANDIDATE_CNT.md) |
| 20 |    `M_SVC_SZ_CHAIN_COMPLETENESS` | 服务链完整度 | STAT | [MD](./M_SVC_SZ_CHAIN_COMPLETENESS.md) |
| 21 |    `M_SVC_SZ_COMPARE_METRIC` | 城市对比指标值 | STAT | [MD](./M_SVC_SZ_COMPARE_METRIC.md) |
