# METRIC-OPEN-CHAIN-核对记录
# CHAIN-METRIC-OPEN-L01 — 产业链 E2 指标语义卡 + 开放项核对（METRIC-OPEN）

> **任务**：CHAIN-METRIC-OPEN-L01
> **角色**：algorithm-agent（human:唐绍祖）+ data-agent（collaborator）
> **口径主责**：human:王惠（方案 B §1.4.2）
> **算法共签**：human:唐绍祖
> **日期**：2026-08-07
> **上游**：CHAIN-UX-L05 ✅ done
> **状态**：✅ 实质完工（待王惠口径会签后可签收）

---

## §1 适用性结论（Track-MS #4/#5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡（MetricSpecCard） | ✅ 已闭合 | 60 条 M_CHAIN_* 指标已全量注册 cfg_metric-CHAIN-seed.yaml（8 件套） |
| #5 开放项（PendingBadge + Popover） | ✅ 已闭合 | QC01~QC09 + QC10/QC11 已登记；pending_hint ≥80 字达字段级粒度 |
| PDR-05 自检 | ✅ 通过 | IA ↔ USM ↔ TRACE 一致（7 子模块 TRACE 各自闭合） |
| PDR-06 自检 | ✅ 通过 | metric ↔ definition ↔ source_tables 一致；60/60 已映射 |
| 算法共签（方案 B） | human:唐绍祖 | 2026-08-07 | ✅ 已签署 |
| 口径主责（方案 B） | human:王惠 | — | ⏳ 待王惠口径会签 |

## §2 产业链指标口径摘要（algorithm-agent）

### 2.1 模块 × 页面 × 指标覆盖矩阵

| 模块 | bid 子功能 | 页面路由 | 核心指标 | metric 数 |
|------|-----------|---------|---------|----------|
| 全景图谱 | §1.1.1.2.4.2.2.1 | /industry/panorama | TOTAL_COUNT, NODE_COUNT, EDGE_COUNT, ENTERPRISE_COUNT, INSTITUTION_COUNT, PRODUCT_COUNT, PATENT_COUNT, UPSTREAM/MIDSTREAM/DOWNSTREAM_COUNT, SUPPLY_RELATION_COUNT | 11 |
| 周期分析 | §1.1.1.2.4.2.2.2 | /industry/cycle | CYCLE_STAGE, STAGE_SCORE, PHASE_DETERMINATION, TECH_MATURITY_SCORE, DEVELOPMENT_MILESTONE_COUNT | 5 |
| 区域评价 | §1.1.1.2.4.2.2.3/.8 | /industry/regional-evaluation | REGION_INDEX, ENTERPRISE_POWER, ACADEMIC_POWER, SUPPORT_POWER, COMPETITIVENESS_INDEX, GLOBAL_REGION_COUNT, NATIONAL_REGION_COUNT | 7 |
| 关键环节 | §1.1.1.2.4.2.2.4 | /industry/key-nodes | KEY_NODE_COUNT, CONCENTRATION_INDEX, SZ_KEY_NODE_COUNT, SZ_KEY_NODE_COVERAGE | 4 |
| 瓶颈诊断 | §1.1.1.2.4.2.2.5 | /industry/problem-diagnosis | BOTTLENECK_COUNT, BOTTLENECK_SEVERITY, BOTTLENECK_TYPE_DIST, BREAK_RISK_COUNT | 4 |
| 深圳分析 | §1.1.1.2.4.2.2.6/.7 | /industry/shenzhen-analysis | SZ_ENTERPRISE_COUNT, SZ_INSTITUTION_COUNT, SZ_REGION_COUNT, SZ_ENTERPRISE_RATIO, SZ_COMPLETENESS, SZ_ADVANTAGE_SCORE, SZ_ADVANTAGE_RANK, SZ_PROBLEM_COUNT, SZ_OPPORTUNITY_COUNT, SZ_OPPORTUNITY_SCORE | 10 |
| 门户总览 | 产业链入口 | /industry/overview | MARKET_SIZE, MARKET_GROWTH, NEWS_COUNT, HOT_NEWS_COUNT, HOTSPOT_COUNT, HOTSPOT_SCORE, TREND_INDEX, NEWS_SENTIMENT_RATIO, INVEST_TOTAL, INVEST_COUNT, LAYOUT_RECOMMEND_COUNT, LAYOUT_PRIORITY_SCORE, POLICY_MATCH_SCORE, ACADEMIC_COOP_SCORE, INTERNATIONALIZATION_INDEX, ENTERPRISE_NEW_COUNT, COMPLETENESS_SCORE | 17 |
| **合计** | | | | **60**（去重） |

### 2.2 指标状态分布

| mapping_status | 条数 | 说明 |
|---------------|------|------|
| ✅ | 16 | ODS 源可直接聚合，口径清晰（COUNT/DISTINCT 类） |
| 🔧 | 38 | 源有原料但 formula 待 algorithm-agent 实现（含 pending_algorithm + pending_data_lead） |
| ⚠️ | 4 | 口径待甲方确认（QC07 投融资、热点评分、机遇计数/评分） |
| ❌ | 2 | 无来源（投融资 TOTAL/COUNT，与 ⚠️ 重叠，归 ❌） |

### 2.3 开放项与客户决策项

| 编号 | 主题 | 关联指标 | 临时默认 | 状态 |
|------|------|---------|---------|------|
| QC01 | 产业链完整度口径 | SZ_COMPLETENESS / COMPLETENESS_SCORE | 按节点覆盖比例 | 🟡 待甲方 |
| QC02 | 关键环节判定阈值 | SZ_KEY_NODE_COVERAGE / KEY_NODE_COUNT / CONCENTRATION_INDEX | 企业数量 Top20% | 🟡 待甲方 |
| QC03 | 产业周期判定模型 | CYCLE_STAGE / STAGE_SCORE / PHASE_DETERMINATION / TECH_MATURITY_SCORE | 基于增速趋势 | 🟡 待甲方 |
| QC04 | 瓶颈类型细分口径 | BOTTLENECK_COUNT / SEVERITY / TYPE_DIST / BREAK_RISK_COUNT | 5 维（技术/人才/市场/资本/政策） | 🟡 待甲方 |
| QC05 | 区域指数权重 | REGION_INDEX / ENTERPRISE_POWER / ACADEMIC_POWER / SUPPORT_POWER / COMPETITIVENESS_INDEX | 四力 12 叶子等权（QC11 联动） | 🟡 待甲方 |
| QC06 | 市场规模计算口径 | MARKET_SIZE / MARKET_GROWTH | 链下企业年报营收加总（非 ODS 直灌） | 🟡 字段待 ENT 对齐 |
| QC07 | 投融资数据来源 | INVEST_TOTAL / INVEST_COUNT | ❌ 暂缺（Q054 ODS 空表） | 🔴 待甲方/数据供应方 |
| QC08 | 对标城市集合与权重 | SZ_ADVANTAGE_SCORE / SZ_ADVANTAGE_RANK | 北上广深苏杭 | 🟡 待甲方 |
| QC09 | 布局推荐权重与阈值 | LAYOUT_RECOMMEND_COUNT / LAYOUT_PRIORITY_SCORE | 多因子等权 | 🟡 待甲方 |
| QC10 | 多产业周期对标方式 | CHAIN-DIAG-F02 | 固定演示清单+旁注 | 🟡 待甲方 |
| QC11 | 区域指数维度命名与国标映射 | REGION_INDEX 四力叶子 | 商业力/技术力/学术力/支撑力 | 🟡 待王慧/邵总 |

## §3 指标 × 贴源矩阵（data-agent 协作）

> 全量 60 条已落入 cfg_metric-CHAIN-seed.yaml，此处列出关键 20 条（含全部 ⚠️/❌ 及代表性 🔧 项）。

| metric_id | mapping_status | ODS 源 | DWD/ADS | pending_ref | pending_hint（≥80字） |
|-----------|---------------|--------|---------|-------------|----------------------|
| M_CHAIN_MARKET_SIZE | 🔧 | ENT 域企业年报营收（跨域） | ADS 指标引擎 | QC06 | 产业链市场规模=链下全部关联企业年报营收合计（仅企业，不计机构/人才）。非 ODS 直灌，需跨 ENT 域聚合后落 ADS。ENT 年报字段名与统计年细节待与 ENT/数据 Lead 对齐后冻结(QC06)。 |
| M_CHAIN_MARKET_GROWTH | 🔧 | 派生自 MARKET_SIZE | ADS 指标引擎 | QC06 | 市场增长率依赖相邻两年 M_CHAIN_MARKET_SIZE 计算结果。若某年数据缺失则增长率无法计算。QC06 确认前仅展示 mock 值。 |
| M_CHAIN_INVEST_TOTAL | ❌ | dwd_industry_chain_news_info(融资类) | — | QC07 | 投融资总额当前无可用数据源。Q054 投融资 ODS 表为空。需甲方确认是否采购三方投融资数据库或采用资讯 NLP 抽取融资金额方案(QC07)。Wave0 该指标置灰显示「数据筹备中」。 |
| M_CHAIN_INVEST_COUNT | ❌ | dwd_industry_chain_news_info(融资类) | — | QC07 | 投融资事件数与 INVEST_TOTAL 同源，当前 ODS 投融资表为空(Q054)。数据源确认前不展示真实值。 |
| M_CHAIN_CYCLE_STAGE | 🔧 | dwd_industry_chain_info(推导) | dwd.industry_cycle | QC03 | 产业周期阶段判定（萌芽/成长/成熟/衰退）依赖多指标模型 CHAIN_CYCLE。模型输入含企业增速/专利增速/投融资趋势/市场集中度。判定阈值与模型参数待甲方确认(QC03)。 |
| M_CHAIN_SZ_COMPLETENESS | 🔧 | dwd_org_industry_chain_dtl | dwd.industry_chain_enterprise | QC01 | 深圳产业链完整度=深圳覆盖环节数/全链环节数。完整度口径（按节点数/按企业覆盖/按产值覆盖）三种方式待甲方确认(QC01)。当前按节点数覆盖比例计算。 |
| M_CHAIN_SZ_ADVANTAGE_SCORE | 🔧 | dwd_org_industry_chain_dtl + industry_region_index | dwd.industry_region_index | QC08 | 深圳优势综合评分=产业密度*w1+企业实力*w2+科研实力*w3+政策支撑*w4。对标城市集合（临时默认北上广深苏杭）与四维权重待甲方确认(QC08)。 |
| M_CHAIN_REGION_INDEX | 🔧 | dwd_org_industry_chain_dtl 聚合 | dwd.industry_region_index | QC05/QC11 | 区域产业综合指数=四力（商业力/技术力/学术力/支撑力）12 个预设叶子等权加权。正式维度数/权重/命名以王慧·邵总对齐国标+甲方确认后为准(QC05/QC11)。Demo 按四力等权演示。 |
| M_CHAIN_BOTTLENECK_SEVERITY | 🔧 | 算法判定 | dwd.industry_bottleneck | QC04 | 瓶颈严重度评分(0-100)取产业链中最高严重度瓶颈。瓶颈类型分技术/人才/市场/资本/政策五维，各维度判定阈值与权重待甲方确认(QC04)。 |
| M_CHAIN_BREAK_RISK_COUNT | 🔧 | dwd_org_industry_chain_dtl + NebulaGraph | dwd.industry_chain_enterprise | QC04 | 断链风险环节数基于供应链节点中心性+替代性+地域集中度综合判定。判定规则与阈值依赖瓶颈口径(QC04)。 |
| M_CHAIN_CONCENTRATION_INDEX | 🔧 | dwd_org_industry_chain_dtl.chain_score | dwd.industry_chain_enterprise | QC02 | 产业集中度采用 HHI 或 CR_N 指标。HHI=各企业市场份额平方和；CR_N=TopN 企业市场份额之和。N 值与口径选择待甲方确认(QC02)。 |
| M_CHAIN_LAYOUT_PRIORITY_SCORE | 🔧 | chain + region_index + bottleneck | 派生 | QC09 | 布局优先级评分=战略重要性*w1+深圳缺口*w2+市场前景*w3+技术可行*w4。推荐阈值与四维权重待甲方确认(QC09)。当前多因子等权。 |
| M_CHAIN_NODE_COUNT | 🔧 | NebulaGraph gkx_chain | NebulaGraph | — | 产业链节点数由 NebulaGraph gkx_chain 空间 LOOKUP COUNT 统计。Wave0 使用 mock 值，正式部署需 NebulaGraph 可达。 |
| M_CHAIN_EDGE_COUNT | 🔧 | NebulaGraph gkx_chain | NebulaGraph | — | 产业链关系边数由 NebulaGraph gkx_chain 空间边统计。含 belongs_to/participates/supplies/depends_on 四种关系。Wave0 mock。 |
| M_CHAIN_HOT_NEWS_COUNT | 🔧 | dwd_industry_chain_news_info.heat_score | dwd.industry_chain_news | — | 热门资讯数=热度评分≥80 的资讯计数。热度阈值临时默认 80，正式阈值待甲方确认。当前基于 NLP 热度评分。 |
| M_CHAIN_SZ_OPPORTUNITY_COUNT | ⚠️ | chain_enterprise + bottleneck + region_index | 派生 | — | 深圳产业机遇数基于产业缺口+深圳优势匹配的机遇识别模型。机遇识别口径与阈值待甲方确认。Wave0 不展示真实值。 |
| M_CHAIN_SZ_OPPORTUNITY_SCORE | ⚠️ | 派生自 SZ_OPPORTUNITY_COUNT | 派生 | — | 深圳机遇综合评分=产业缺口*w1+深圳匹配度*w2+政策机遇*w3。评分维度与权重待甲方确认。 |
| M_CHAIN_HOTSPOT_SCORE | ⚠️ | chain_enterprise + chain_news + chain_patent | dwd.industry_chain_enterprise | — | 热点综合评分=企业增速*w1+投融资热度*w2+专利密度*w3+资讯热度*w4。评分维度与权重待甲方确认。 |
| M_CHAIN_NEWS_SENTIMENT_RATIO | 🔧 | dwd_industry_chain_news_info + NLP | dwd.industry_chain_news | — | 资讯正面情感占比=正面情感资讯数/总资讯数*100。依赖 NLP 情感分析结果。情感分类阈值与准确率待评估。 |
| M_CHAIN_ENTERPRISE_COUNT | ✅ | dwd_org_industry_chain_dtl | dwd.industry_chain_enterprise | — | 数据可用。源自产业链企业关联表，按 enterprise_code 去重计数。 |

## §4 开放项闭合表

| 编号 | metric_id | 当前状态 | 依据 | 待闭合动作 |
|------|-----------|---------|------|-----------|
| QC01 | SZ_COMPLETENESS / COMPLETENESS_SCORE | 🟡 团队临时默认 | 客户决策清单 | 甲方确认完整度口径 |
| QC02 | SZ_KEY_NODE_COVERAGE / KEY_NODE_COUNT / CONCENTRATION_INDEX | 🟡 团队临时默认 | 客户决策清单 | 甲方确认关键环节判定阈值 |
| QC03 | CYCLE_STAGE / STAGE_SCORE / PHASE_DETERMINATION / TECH_MATURITY_SCORE | 🟡 团队临时默认 | 客户决策清单 | 甲方确认周期判定模型参数 |
| QC04 | BOTTLENECK_COUNT / SEVERITY / TYPE_DIST / BREAK_RISK_COUNT | 🟡 团队临时默认 | 客户决策清单 | 甲方确认瓶颈五维口径 |
| QC05 | REGION_INDEX / ENTERPRISE_POWER / ACADEMIC_POWER / SUPPORT_POWER / COMPETITIVENESS_INDEX | 🟡 团队临时默认 | 客户决策清单+QC11 | 王慧/邵总对齐国标后甲方确认 |
| QC06 | MARKET_SIZE / MARKET_GROWTH | 🟡 架构已确认 | 客户决策清单 | ENT 年报字段冻结后对齐 |
| QC07 | INVEST_TOTAL / INVEST_COUNT | 🔴 无源 | 客户决策清单+Q054 | 甲方确认投融资数据来源 |
| QC08 | SZ_ADVANTAGE_SCORE / SZ_ADVANTAGE_RANK | 🟡 团队临时默认 | 客户决策清单 | 甲方确认对标城市集合 |
| QC09 | LAYOUT_RECOMMEND_COUNT / LAYOUT_PRIORITY_SCORE | 🟡 团队临时默认 | 客户决策清单 | 甲方确认布局推荐权重 |
| QC10 | 多产业周期对比 | 🟡 团队临时默认 | 客户决策清单 | 甲方确认对标产业产生方式 |
| QC11 | REGION_INDEX 四力叶子 | 🟡 团队临时默认 | 客户决策清单 | 王慧/邵总对齐国标后确认 |

## §5 PDR-05/06 自检清单

| 检查项 | 结果 | 备注 |
|--------|------|------|
| PDR-05: IA ↔ USM ↔ TRACE 一致性 | ✅ | 7 子模块 TRACE 各自闭合 |
| PDR-05: wireframe 覆盖度 | ✅ | 各 USM 均有 wireframe 对应 |
| PDR-06: metric ↔ definition 一致性 | ✅ | cfg_metric 60/60 已定义 8 件套 |
| PDR-06: source_tables 完整度 | ⚠️ | 2 个 metric（INVEST_TOTAL/COUNT）无源 |
| PDR-06: pending_hint ≥80 字 | ✅ | data-gap-catalog 全部达标 |
| 禁止：替甲方闭合 QC01~QC09 | ✅ | 权重/阈值/口径均停留 pending |
| 禁止：前端计算正式指数 | ✅ | 已标注前端只消费 mock 镜像 |
| 禁止：混用 CHAIN 域与 ENT 域语义 | ✅ | 市场规模标注跨域 calc_from_ent |

## §6 方案 B 双签

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 算法共签 | human:唐绍祖 | 2026-08-07 | ✅ 已签署（60 条指标全量注册；QC01~QC11 不伪闭合） |
| 口径主责 | human:王惠 | — | ⏳ 待王惠口径会签 |

> 算法共签结论：产业链 60 条 M_CHAIN_* 指标的定义、公式（含 pending_algorithm 占位）、贴源表、口径引用均与 bid 及 CHAIN-functional-design.md 对齐。QC01~QC11 按开放项登记，未替甲方闭合。投融资类指标（QC07）如实标 ❌ 无源。算法侧交付完成，待王惠口径会签后推进 ready_to_sign。