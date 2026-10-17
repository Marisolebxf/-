# 联调台 catalog 快照（by-api 接口真源）

- git SHA：`099142da8639f52d3848e3e1b2fe7e64c0b5d4c4`
- 仓：`repos/lumen-ui-algo-apiview`
- 路径：`src/catalog/{entan,chain,policy,svc,comp,innov}.json`
- 本文件由 `scripts/_dump_algo_apiview_catalog.py` 生成；拆点前再跑一次，SHA 变了要更新原则稿冻结值

## entan（15 页）

| id | title | menuPath | endpoints | running | unavailable | local_mock |
|---|---|---|---:|---:|---:|---:|
| `entan.basic` | 企业基础指标 | `/entan/basic` | 7 | 0 | 7 | 0 |
| | `GET /entan/v1/meta/filters` | | | | | |
| | `GET /entan/v1/key-enterprises` | | | | | |
| | `GET /entan/v1/type-distribution` | | | | | |
| | `GET /entan/v1/domain-distribution` | | | | | |
| | `GET /entan/v1/new-enterprises` | | | | | |
| | `GET /entan/v1/news/stats` | | | | | |
| | `GET /entan/v1/news` | | | | | |
| `entan.competitiveness` | 深圳企业竞争力水平分析 | `/entan/competitiveness` | 2 | 0 | 2 | 0 |
| | `POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute` | | | | | |
| | `POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute` | | | | | |
| `entan.history` | 企业发展历程 | `/entan/history` | 2 | 0 | 2 | 0 |
| | `GET /entan/v1/enterprises` | | | | | |
| | `GET /entan/v1/history` | | | | | |
| `entan.pain-points` | 企业发展痛难点识别 | `/entan/pain-points` | 2 | 0 | 2 | 0 |
| | `POST /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute` | | | | | |
| | `POST /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute` | | | | | |
| `entan.supply-chain` | 企业供应链关系分析 | `/entan/supply-chain` | 1 | 0 | 1 | 0 |
| | `POST /entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute` | | | | | |
| `entan.tech` | 企业技术力评估 | `/entan/tech` | 4 | 0 | 4 | 0 |
| | `POST /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute` | | | | | |
| | `GET /entan/v1/tech-power/{orgId}` | | | | | |
| | `GET /entan/v1/eval/weights` | | | | | |
| | `GET /entan/v1/enterprises/{orgId}/report` | | | | | |
| `entan.biz` | 企业商业力评估 | `/entan/biz` | 4 | 0 | 4 | 0 |
| | `POST /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute` | | | | | |
| | `GET /entan/v1/biz-power/{orgId}` | | | | | |
| | `GET /entan/v1/eval/weights` | | | | | |
| | `GET /entan/v1/enterprises/{orgId}/report` | | | | | |
| `entan.attract` | 招引企业综合推荐 | `/entan/attract` | 1 | 0 | 1 | 0 |
| | `POST /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute` | | | | | |
| `entan.cultivate` | 培育企业综合推荐 | `/entan/cultivate` | 1 | 0 | 1 | 0 |
| | `POST /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute` | | | | | |
| `entan.graph` | 企业实体与关系 | `/entan/graph` | 12 | 0 | 12 | 0 |
| | `POST /entan/v1/entan/graph/ner` | | | | | |
| | `POST /entan/v1/entan/graph/intra` | | | | | |
| | `POST /entan/v1/entan/graph/intra` | | | | | |
| | `POST /entan/v1/entan/graph/intra` | | | | | |
| | `POST /entan/v1/entan/graph/intra` | | | | | |
| | `POST /entan/v1/entan/graph/hang` | | | | | |
| | `POST /entan/v1/entan/graph/hang` | | | | | |
| | `POST /entan/v1/entan/graph/hang` | | | | | |
| | `POST /entan/v1/entan/graph/hang` | | | | | |
| | `POST /entan/v1/entan/graph/hang` | | | | | |
| | `POST /entan/v1/entan/graph/hang` | | | | | |
| | `GET /entan/v1/entan/graph` | | | | | |
| `entan.risk` | 风险评分 | `/entan/risk` | 1 | 0 | 1 | 0 |
| | `GET /entan/v1/risk` | | | | | |
| `entan.eval-async` | 企业评估（异步） | `/entan/eval-async` | 1 | 0 | 1 | 1 |
| | `POST ` | | | | | |
| `entan.innovation` | 企业创新能力评估 | `/entan/innovation` | 1 | 0 | 1 | 0 |
| | `POST /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute` | | | | | |
| `entan.chain-coverage` | 企业产业链洞察 | `/entan/chain-coverage` | 3 | 0 | 3 | 0 |
| | `POST /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute` | | | | | |
| | `POST /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute` | | | | | |
| | `POST /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute` | | | | | |
| `entan.growth-match` | 企业成长与产业匹配 | `/entan/growth-match` | 2 | 0 | 2 | 0 |
| | `POST /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute` | | | | | |
| | `POST /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute` | | | | | |

## chain（17 页）

| id | title | menuPath | endpoints | running | unavailable | local_mock |
|---|---|---|---:|---:|---:|---:|
| `chain.basic` | 产业链基础指标 | `/chain/basic` | 10 | 0 | 3 | 0 |
| | `GET /innov/v1/industry/list` | | | | | |
| | `GET /innov/v1/industry/market-stats` | | | | | |
| | `GET /innov/v1/industry/enterprise-stats` | | | | | |
| | `GET /innov/v1/industry/institution-stats` | | | | | |
| | `GET /innov/v1/industry/investment-stats` | | | | | |
| | `GET /innov/v1/industry/global-dist` | | | | | |
| | `GET /innov/v1/industry/national-dist` | | | | | |
| | `GET /innov/v1/industry/news-stats` | | | | | |
| | `GET /innov/v1/industry/sz-elements` | | | | | |
| | `GET /innov/v1/industry/sz-dist` | | | | | |
| `chain.wave1` | 第一波 16 STAT（ADS） | `/chain/wave1` | 16 | 0 | 0 | 0 |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_TOTAL_COUNT/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_ENTERPRISE_COUNT/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_ENTERPRISE_NEW_COUNT/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_NATIONAL_REGION_COUNT/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_SZ_REGION_COUNT/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_SZ_ENTERPRISE_COUNT/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_SZ_ENTERPRISE_RATIO/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_MARKET_SIZE/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_MARKET_GROWTH/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_INVEST_COUNT/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_REG_FINANCING/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_REG_REVENUE/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_REG_PATENT/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_SZ_COMPLETENESS/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_PATENT_COUNT/compute` | | | | | |
| | `POST /innov/v1/industry/chainan/metric/M_CHAIN_PRODUCT_COUNT/compute` | | | | | |
| `chain.panorama` | 产业链全景 | `/chain/panorama` | 2 | 2 | 0 | 0 |
| | `POST /chain/v1/chain/graph/ops/{op_id}` | | | | | |
| | `GET /chain/v1/chain/{chainId}/panorama` | | | | | |
| `chain.topic-panorama` | 深圳产业链 | `/chain/topic-panorama` | 2 | 2 | 0 | 0 |
| | `POST /chain/v1/chain/graph/ops/{op_id}` | | | | | |
| | `GET /chain/v1/chain/{chainId}/panorama` | | | | | |
| `chain.cycle` | 产业周期分析 | `/chain/cycle` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/industry/{chainId}/cycle` | | | | | |
| `chain.stage` | 产业阶段分析 | `/chain/stage` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/industry/{chainId}/cycle` | | | | | |
| `chain.keynodes` | 产业链关键环节识别 | `/chain/keynodes` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/industry/{chainId}/key-nodes` | | | | | |
| `chain.bottleneck` | 产业瓶颈堵点识别 | `/chain/bottleneck` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/industry/{chainId}/bottlenecks` | | | | | |
| `chain.region` | 区域产业指数 | `/chain/region` | 2 | 0 | 2 | 0 |
| | `GET /innov/v1/industry/{chainId}/region-index` | | | | | |
| | `GET /innov/v1/industry/{chainId}/competitiveness` | | | | | |
| `chain.shenzhen` | 深圳产业优势识别 | `/chain/shenzhen` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/industry/{chainId}/shenzhen` | | | | | |
| `chain.sz-problem` | 深圳问题识别 | `/chain/sz-problem` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/industry/{chainId}/shenzhen` | | | | | |
| `chain.sz-opportunity` | 深圳机遇分析 | `/chain/sz-opportunity` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/industry/{chainId}/shenzhen` | | | | | |
| `chain.hotspot` | 产业热点领域识别 | `/chain/hotspot` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/industry/{chainId}/hotspot` | | | | | |
| `chain.roadmap` | 产业发展路线历程 | `/chain/roadmap` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/industry/{chainId}/roadmap` | | | | | |
| `chain.layout` | 重点布局产业推荐 | `/chain/layout` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/industry/{chainId}/recommendation` | | | | | |
| `chain.tech-maturity` | 技术成熟度分析 | `/chain/tech-maturity` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/industry/{chainId}/tech-maturity` | | | | | |
| `chain.strategic-importance` | 产业战略重要性分析 | `/chain/strategic-importance` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/industry/{chainId}/strategic-importance` | | | | | |

## policy（16 页）

| id | title | menuPath | endpoints | running | unavailable | local_mock |
|---|---|---|---:|---:|---:|---:|
| `policy.basic` | 政策基础指标 | `/policy/basic` | 2 | 0 | 2 | 0 |
| | `GET /policy/v1/policy/metrics` | | | | | |
| | `GET /policy/v1/policy/indicators` | | | | | |
| `policy.graph` | 政策实体与关系 | `/policy/graph` | 6 | 0 | 6 | 0 |
| | `POST /policy/v1/policy/graph/ner` | | | | | |
| | `POST /policy/v1/policy/graph/intra` | | | | | |
| | `POST /policy/v1/policy/graph/hang` | | | | | |
| | `POST /policy/v1/policy/graph/hang` | | | | | |
| | `POST /policy/v1/policy/graph/hang` | | | | | |
| | `GET /policy/v1/policy/graph` | | | | | |
| `policy.focus` | 政策焦点识别 | `/policy/focus` | 1 | 0 | 1 | 0 |
| | `GET /policy/v1/policy/analysis/focus` | | | | | |
| `policy.focus-one` | 焦点识别(单个政策) | `/policy/focus-one` | 1 | 0 | 1 | 0 |
| | `POST /policy/v1/policy/analysis/focus-one` | | | | | |
| `policy.intensity` | 政策力度评估 | `/policy/intensity` | 1 | 0 | 1 | 0 |
| | `GET /policy/v1/policy/analysis/intensity` | | | | | |
| `policy.effect` | 政策效果评估 | `/policy/effect` | 1 | 0 | 1 | 0 |
| | `GET /policy/v1/policy/analysis/effect` | | | | | |
| `policy.gap` | 政策短板识别 | `/policy/gap` | 1 | 0 | 1 | 0 |
| | `GET /policy/v1/policy/analysis/gap` | | | | | |
| `policy.opportunity` | 政策机遇识别 | `/policy/opportunity` | 1 | 0 | 1 | 0 |
| | `GET /policy/v1/policy/analysis/opportunity` | | | | | |
| `policy.layout` | 政策布局推荐 | `/policy/layout` | 1 | 0 | 1 | 0 |
| | `GET /policy/v1/policy/analysis/layout` | | | | | |
| `policy.text` | 文本解析 · 匹配 · 推演 | `/policy/text` | 3 | 0 | 3 | 0 |
| | `GET /policy/v1/policy/text/parse` | | | | | |
| | `GET /policy/v1/policy/match` | | | | | |
| | `GET /policy/v1/policy/simulate` | | | | | |
| `policy.parse` | 文本解析 · 智能摘要 | `/policy/parse` | 1 | 0 | 1 | 0 |
| | `GET /policy/v1/policy/text/parse` | | | | | |
| `policy.match` | 匹配推送 | `/policy/match` | 1 | 0 | 1 | 0 |
| | `GET /policy/v1/policy/match` | | | | | |
| `policy.simulate` | 效果推演 · 实施路径 | `/policy/simulate` | 1 | 0 | 1 | 0 |
| | `GET /policy/v1/policy/simulate` | | | | | |
| `policy.guide` | 发展战略引导力 | `/policy/guide` | 1 | 0 | 1 | 0 |
| | `GET /policy/v1/policy/analysis/guide` | | | | | |
| `policy.guard` | 条件保障力 | `/policy/guard` | 1 | 0 | 1 | 0 |
| | `GET /policy/v1/policy/analysis/guard` | | | | | |
| `policy.deep` | 算法库后端模型 | `/policy/deep` | 1 | 0 | 1 | 0 |
| | `GET /policy/v1/policy/analysis/deep` | | | | | |

## svc（14 页）

| id | title | menuPath | endpoints | running | unavailable | local_mock |
|---|---|---|---:|---:|---:|---:|
| `svc.basic` | 服务机构基础指标 | `/industry-service/basic` | 1 | 0 | 1 | 0 |
| | `GET /entan/v1/svc/indicators` | | | | | |
| `svc.graph` | 服务机构实体与关系 | `/industry-service/graph` | 10 | 0 | 10 | 0 |
| | `POST /entan/v1/svc/graph/ner` | | | | | |
| | `POST /entan/v1/svc/graph/intra` | | | | | |
| | `POST /entan/v1/svc/graph/hang` | | | | | |
| | `POST /entan/v1/svc/graph/hang` | | | | | |
| | `POST /entan/v1/svc/graph/hang` | | | | | |
| | `POST /entan/v1/svc/graph/hang` | | | | | |
| | `POST /entan/v1/svc/graph/hang` | | | | | |
| | `POST /entan/v1/svc/graph/hang` | | | | | |
| | `POST /entan/v1/svc/graph/hang` | | | | | |
| | `GET /entan/v1/svc/graph` | | | | | |
| `svc.gap` | 服务链短板分析 | `/industry-service/gap` | 1 | 0 | 1 | 0 |
| | `GET /entan/v1/svc/models` | | | | | |
| `svc.relation` | 服务关系链 | `/industry-service/relation` | 2 | 0 | 2 | 0 |
| | `GET /entan/v1/svc/models` | | | | | |
| | `GET /entan/v1/svc/graph` | | | | | |
| `svc.tech-finance` | 金融服务机构技术力评估 | `/industry-service/tech-finance` | 1 | 0 | 1 | 0 |
| | `GET /entan/v1/svc/models` | | | | | |
| `svc.tech-ip` | 知识产权服务机构技术力评估 | `/industry-service/tech-ip` | 1 | 0 | 1 | 0 |
| | `GET /entan/v1/svc/models` | | | | | |
| `svc.tech-hr` | 人力资源服务机构技术力评估 | `/industry-service/tech-hr` | 1 | 0 | 1 | 0 |
| | `GET /entan/v1/svc/models` | | | | | |
| `svc.tech-mkt` | 市场营销服务机构技术力评估 | `/industry-service/tech-mkt` | 1 | 0 | 1 | 0 |
| | `GET /entan/v1/svc/models` | | | | | |
| `svc.tech-consult` | 咨询服务机构技术力评估 | `/industry-service/tech-consult` | 1 | 0 | 1 | 0 |
| | `GET /entan/v1/svc/models` | | | | | |
| `svc.tech-innov` | 科技创新服务机构技术力评估 | `/industry-service/tech-innov` | 1 | 0 | 1 | 0 |
| | `GET /entan/v1/svc/models` | | | | | |
| `svc.attract` | 服务机构引入推荐 | `/industry-service/attract` | 1 | 0 | 1 | 0 |
| | `GET /entan/v1/svc/models` | | | | | |
| `svc.cultivate` | 服务机构培育推荐 | `/industry-service/cultivate` | 1 | 0 | 1 | 0 |
| | `GET /entan/v1/svc/models` | | | | | |
| `svc.market-heat` | 市场热度评级 | `/industry-service/market-heat` | 1 | 0 | 1 | 0 |
| | `GET /entan/v1/svc/market-heat` | | | | | |
| `svc.sz-tier` | 深圳梯队位置 | `/industry-service/sz-tier` | 1 | 0 | 1 | 0 |
| | `GET /entan/v1/svc/sz-tier` | | | | | |

## comp（12 页）

| id | title | menuPath | endpoints | running | unavailable | local_mock |
|---|---|---|---:|---:|---:|---:|
| `comp.basic` | 产业综合上游依赖 | `/industry-comp/basic` | 1 | 0 | 1 | 1 |
| | `GET /comp/v1/comp/upstream-deps` | | | | | |
| `comp.graph` | 产业全要素图谱 API | `/industry-comp/graph` | 6 | 0 | 0 | 0 |
| | `GET /industry-comp/v1/comp/graph` | | | | | |
| | `GET /industry-comp/v1/comp/graph/entities` | | | | | |
| | `GET /industry-comp/v1/comp/graph/relations` | | | | | |
| | `GET /industry-comp/v1/comp/graph/viz` | | | | | |
| | `POST /industry-comp/v1/comp/graph/similar` | | | | | |
| | `GET /industry-comp/v1/comp/graph/metrics` | | | | | |
| `comp.tech-outcome` | 区域科技创新成果综合评价 | `/industry-comp/tech-outcome` | 1 | 0 | 1 | 1 |
| | `GET /comp/v1/comp/region-tech-outcome` | | | | | |
| `comp.industry-outcome` | 区域产业创新成果综合评价 | `/industry-comp/industry-outcome` | 1 | 0 | 1 | 1 |
| | `GET /comp/v1/comp/region-industry-outcome` | | | | | |
| `comp.talent-outcome` | 区域产业创新人才综合评价 | `/industry-comp/talent-outcome` | 1 | 0 | 1 | 1 |
| | `GET /comp/v1/comp/region-talent-outcome` | | | | | |
| `comp.policy-outcome` | 区域产业创新政策综合评价 | `/industry-comp/policy-outcome` | 1 | 0 | 1 | 1 |
| | `GET /comp/v1/comp/region-policy-outcome` | | | | | |
| `comp.vitality` | 区域创新活力综合分析 | `/industry-comp/vitality` | 1 | 0 | 1 | 1 |
| | `GET /comp/v1/comp/region-vitality` | | | | | |
| `comp.element-type` | 区域创新要素类型综合评价 | `/industry-comp/element-type` | 1 | 0 | 1 | 1 |
| | `GET /comp/v1/comp/element-type` | | | | | |
| `comp.element-layer` | 区域创新要素层次综合评价 | `/industry-comp/element-layer` | 1 | 0 | 1 | 1 |
| | `GET /comp/v1/comp/element-layer` | | | | | |
| `comp.element-domain` | 区域创新要素领域综合评价 | `/industry-comp/element-domain` | 1 | 0 | 1 | 1 |
| | `GET /comp/v1/comp/element-domain` | | | | | |
| `comp.element-synthesis` | 区域创新要素综合分析 | `/industry-comp/element-synthesis` | 1 | 0 | 1 | 1 |
| | `GET /comp/v1/comp/element-synthesis` | | | | | |
| `comp.synergy` | 区域创新协同分析 | `/industry-comp/synergy` | 1 | 0 | 1 | 1 |
| | `GET /comp/v1/comp/innov-synergy` | | | | | |

## innov（15 页）

| id | title | menuPath | endpoints | running | unavailable | local_mock |
|---|---|---|---:|---:|---:|---:|
| `innov.events` | M1 科创事件地图 | `/innov/events` | 6 | 6 | 0 | 0 |
| | `GET /innov/v1/events` | | | | | |
| | `GET /innov/v1/events` | | | | | |
| | `GET /innov/v1/events/heatmap` | | | | | |
| | `GET /innov/v1/events/{eventId}` | | | | | |
| | `GET /innov/v1/events/{eventId}/relations` | | | | | |
| | `GET /innov/v1/dict/event-types` | | | | | |
| `innov.graph` | M2 创新点落图与赋分 | `/innov/graph` | 3 | 3 | 0 | 0 |
| | `GET /innov/v1/graph/domains` | | | | | |
| | `GET /innov/v1/graph/subgraph` | | | | | |
| | `GET /innov/v1/graph/influence/rank` | | | | | |
| `innov.carriers` | M3 创新载体排行 | `/innov/carriers` | 3 | 3 | 0 | 0 |
| | `GET /innov/v1/carriers/rank` | | | | | |
| | `GET /innov/v1/carriers/{carrierId}` | | | | | |
| | `GET /innov/v1/carriers/index-method` | | | | | |
| `innov.cities` | M4 城市创新能力 | `/innov/cities` | 4 | 4 | 0 | 0 |
| | `GET /innov/v1/cities/rank` | | | | | |
| | `GET /innov/v1/cities/compare` | | | | | |
| | `GET /innov/v1/cities/{cityCode}/advice` | | | | | |
| | `GET /innov/v1/cities/index-method` | | | | | |
| `innov.forecast` | M5 创新影响预测 | `/innov/forecast` | 3 | 3 | 0 | 0 |
| | `GET /innov/v1/forecast/domain/{domainId}` | | | | | |
| | `GET /innov/v1/forecast/contributions` | | | | | |
| | `GET /innov/v1/forecast/bursts` | | | | | |
| `innov.risk` | 风险洞察（异步） | `/innov/risk` | 2 | 0 | 2 | 2 |
| | `POST ` | | | | | |
| | `POST ` | | | | | |
| `innov.recommend` | 引育推荐（异步） | `/innov/recommend` | 2 | 0 | 2 | 2 |
| | `POST ` | | | | | |
| | `POST ` | | | | | |
| `innov.tech-evaluation` | 科技创新评估 | `/innov/tech-evaluation` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/innov/metrics` | | | | | |
| `innov.tech-planning` | 科技发展规划 | `/innov/tech-planning` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/innov/metrics` | | | | | |
| `innov.tech-landscape` | 科技全域态势 | `/innov/tech-landscape` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/innov/metrics` | | | | | |
| `innov.global-monitoring` | 全球创新监测 | `/innov/global-monitoring` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/innov/metrics` | | | | | |
| `innov.sz-monitoring` | 深圳创新监测 | `/innov/sz-monitoring` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/innov/metrics` | | | | | |
| `innov.bay-area-monitoring` | 湾区创新监测 | `/innov/bay-area-monitoring` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/innov/metrics` | | | | | |
| `innov.topic-strategy` | 科技专题战略分析 | `/innov/topic-strategy` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/innov/metrics` | | | | | |
| `innov.service-org` | 服务机构管理 | `/innov/service-org` | 1 | 0 | 1 | 0 |
| | `GET /innov/v1/innov/metrics` | | | | | |

## 合计

- 页：89
- endpoint 声明：184
- 唯一 METHOD+path：135
- status：{'unavailable': 132, 'available': 29, 'running': 23}
- runtime：{'java_api': 168, 'local_mock': 16}
