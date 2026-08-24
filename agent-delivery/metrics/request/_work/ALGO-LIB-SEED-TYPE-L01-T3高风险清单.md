# ALGO-LIB-SEED-TYPE-L01 · T3 高风险清单

> 供 `human:唐绍祖` 事后抽查。共 **209** 条（T3 共 276 条中的 formula 占位符项）。
> 这些指标的 formula 是 `pending_*` / 未签占位，机器初判 type 主要靠中文名，是 522 条里最可能误判的部分。
> 初判 type 已按「全部采纳」回填进 seed；抽查后如需更正，告诉我改哪条即可。

| # | metric_id | domain | 中文名 | 初判 type | formula(截断) |
|---|---|---|---|---|---|
| 1 | `M_CHAIN_ACADEMIC_COOP_SCORE` | CHAIN | 产学研合作强度 | MODEL | pending_algorithm（联合专利数*w1+联合项目数*w2+人才流动*w3） |
| 2 | `M_CHAIN_ACADEMIC_POWER` | CHAIN | 科研实力指数 | MODEL | pending_algorithm（专利密度*w1 + 论文密度*w2 + 高校数量*w3） |
| 3 | `M_CHAIN_BOTTLENECK_SEVERITY` | CHAIN | 瓶颈严重度 | MODEL | pending_algorithm（MAX(severity_score) FROM dwd.industry_bott |
| 4 | `M_CHAIN_BREAK_RISK_COUNT` | CHAIN | 产业链断链风险数 | GRAPH | pending_algorithm（供应链节点中心性+替代性+地域集中度综合判定） |
| 5 | `M_CHAIN_CHOKE_LINK_COUNT` | CHAIN | 卡脖子环节数 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 6 | `M_CHAIN_COMPETITIVENESS_INDEX` | CHAIN | 区域竞争力指数 | MODEL | pending_algorithm（M_CHAIN_REGION_INDEX + 排名归一化 + 趋势因子） |
| 7 | `M_CHAIN_COMPLETENESS_SCORE` | CHAIN | 产业链完整度评分 | MODEL | pending_algorithm（覆盖环节数/全链环节数*100 * 企业分布均匀度修正因子） |
| 8 | `M_CHAIN_CONCENTRATION_INDEX` | CHAIN | 产业集中度 | STAT | pending_algorithm（HHI = SUM(企业市场份额^2) 或 CR_N = TopN企业市场份额之和） |
| 9 | `M_CHAIN_CYCLE_STAGE` | CHAIN | 周期阶段 | MODEL | pending_algorithm（基于企业增速/专利增速/投融资趋势/市场集中度的周期判定模型 CHAIN_CYCLE |
| 10 | `M_CHAIN_DEVELOPMENT_MILESTONE_COUNT` | CHAIN | 发展里程碑数 | MODEL | pending_algorithm（基于 dwd.industry_chain_news + 政策事件 NLP 提取里程 |
| 11 | `M_CHAIN_EDGE_COUNT` | CHAIN | 产业链边数 | GRAPH | pending_algorithm（NebulaGraph gkx_chain 边统计） |
| 12 | `M_CHAIN_ENTERPRISE_POWER` | CHAIN | 企业实力指数 | MODEL | pending_algorithm（AVG(chain_score) * 企业规模/资质加权因子） |
| 13 | `M_CHAIN_GLOBAL_CASE_MATCH` | CHAIN | 全球成功案例匹配 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 14 | `M_CHAIN_HIGH_VALUE_RATIO` | CHAIN | 高价值环节占比 | STAT | pending_algorithm（高价值环节数 / 全部环节数 * 100） |
| 15 | `M_CHAIN_HOTSPOT_COUNT` | CHAIN | 热点领域数 | MODEL | pending_algorithm（企业增速*w1+投融资热度*w2+专利密度*w3 >= 阈值） |
| 16 | `M_CHAIN_HOTSPOT_SCORE` | CHAIN | 热点评分 | MODEL | pending_algorithm（企业增速*w1+投融资热度*w2+专利密度*w3+资讯热度*w4） |
| 17 | `M_CHAIN_INTERNATIONALIZATION_INDEX` | CHAIN | 产业链国际化程度 | STAT | pending_algorithm（海外企业占比*w1+海外专利占比*w2+进出口数据*w3） |
| 18 | `M_CHAIN_INVEST_TOTAL` | CHAIN | 投融资总额 | MODEL | pending_algorithm（NLP抽取融资金额 / 采购数据聚合） |
| 19 | `M_CHAIN_LAYOUT_PRIORITY_SCORE` | CHAIN | 布局优先级评分 | MODEL | pending_algorithm（战略重要性*w1+深圳缺口*w2+市场前景*w3+技术可行*w4） |
| 20 | `M_CHAIN_LINK_HEALTH` | CHAIN | 环节健康度 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 21 | `M_CHAIN_NEWS_SENTIMENT_RATIO` | CHAIN | 资讯正面情感占比 | STAT | pending_algorithm（COUNT(sentiment='positive') / COUNT(*) * 1 |
| 22 | `M_CHAIN_NODE_COUNT` | CHAIN | 产业链节点数 | GRAPH | pending_algorithm（NebulaGraph gkx_chain LOOKUP COUNT） |
| 23 | `M_CHAIN_PHASE_DETERMINATION` | CHAIN | 阶段判定 | MODEL | pending_algorithm（基于环节数据的分阶段判定模型） |
| 24 | `M_CHAIN_POLICY_MATCH_SCORE` | CHAIN | 产业政策匹配度 | MODEL | pending_algorithm（产业链标签 vs 政策标签匹配评分） |
| 25 | `M_CHAIN_REG_COMMERCIALIZATION` | CHAIN | 企业商业化能力 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 26 | `M_CHAIN_REG_COMP_ACADEMIC` | CHAIN | 学术生态 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 27 | `M_CHAIN_REG_COMP_ENTERPRISE` | CHAIN | 企业能力 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 28 | `M_CHAIN_REG_COMP_SUPPORT` | CHAIN | 配套生态力 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 29 | `M_CHAIN_REG_ECOSYSTEM` | CHAIN | 配套生态 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 30 | `M_CHAIN_REG_FINANCING` | CHAIN | 融资事件 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 31 | `M_CHAIN_REG_PAPERS` | CHAIN | 高校论文 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 32 | `M_CHAIN_REG_PATENT` | CHAIN | 专利 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 33 | `M_CHAIN_REG_POLICY_COVERAGE` | CHAIN | 政策覆盖率 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 34 | `M_CHAIN_REG_RESEARCH_ORG` | CHAIN | 科研机构 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 35 | `M_CHAIN_REG_REVENUE` | CHAIN | 营收 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 36 | `M_CHAIN_REG_SERVICE_ORG` | CHAIN | 服务机构 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 37 | `M_CHAIN_REG_TALENT_STRUCTURE` | CHAIN | 人才结构 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 38 | `M_CHAIN_REG_TECH_BARRIER` | CHAIN | 技术壁垒 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 39 | `M_CHAIN_REG_TECH_MATURITY` | CHAIN | 技术成熟度 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 40 | `M_CHAIN_REGION_INDEX` | CHAIN | 区域产业综合指数 | MODEL | pending_algorithm（enterprise_power_score*W1 + academic_power |
| 41 | `M_CHAIN_STAGE_SCORE` | CHAIN | 周期阶段评分 | MODEL | pending_algorithm（CHAIN_CYCLE 模型置信度输出） |
| 42 | `M_CHAIN_STRATEGIC_IMPORTANCE` | CHAIN | 战略重要性评分 | MODEL | pending_algorithm（技术壁垒*w1+市场集中度*w2+国产化率*w3+政策导向*w4） |
| 43 | `M_CHAIN_SUPPLY_RELATION_COUNT` | CHAIN | 供应链关系数 | GRAPH | pending_algorithm（NebulaGraph gkx_chain supplies 边 COUNT） |
| 44 | `M_CHAIN_SUPPORT_POWER` | CHAIN | 配套支撑指数 | MODEL | pending_algorithm（政策匹配度*w1 + 服务机构密度*w2 + 基础设施*w3） |
| 45 | `M_CHAIN_SZ_ADVANTAGE_RANK` | CHAIN | 深圳优势排名 | MODEL | pending_algorithm（RANK() OVER ORDER BY 优势评分 DESC） |
| 46 | `M_CHAIN_SZ_ADVANTAGE_SCORE` | CHAIN | 深圳优势评分 | MODEL | pending_algorithm（深圳产业密度*w1+企业实力*w2+科研实力*w3+政策支撑*w4） |
| 47 | `M_CHAIN_SZ_COMPLETENESS` | CHAIN | 深圳产业链完整度 | MODEL | pending_algorithm（深圳覆盖环节数 / 全链环节数 * 100） |
| 48 | `M_CHAIN_SZ_ENTERPRISE` | CHAIN | 对比四维-企业 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 49 | `M_CHAIN_SZ_KEY_NODE_COVERAGE` | CHAIN | 深圳关键环节覆盖率 | MODEL | pending_algorithm（深圳覆盖关键环节数 / 全链关键环节数 * 100） |
| 50 | `M_CHAIN_SZ_OPPORTUNITY_COUNT` | CHAIN | 深圳产业机遇数 | MODEL | pending_algorithm（基于产业缺口+深圳优势匹配的机遇识别模型） |
| 51 | `M_CHAIN_SZ_OPPORTUNITY_SCORE` | CHAIN | 深圳产业机遇评分 | MODEL | pending_algorithm（产业缺口*w1+深圳匹配度*w2+政策机遇*w3） |
| 52 | `M_CHAIN_SZ_PATENT` | CHAIN | 对比四维-专利 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 53 | `M_CHAIN_SZ_POLICY` | CHAIN | 对比四维-政策 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 54 | `M_CHAIN_SZ_TALENT` | CHAIN | 对比四维-人才 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 55 | `M_CHAIN_TECH_MATURITY_SCORE` | CHAIN | 技术成熟度评分 | MODEL | pending_algorithm（专利平均年龄*w1+专利增长率*w2+技术覆盖度*w3） |
| 56 | `M_CHAIN_TECH_POWER` | CHAIN | 技术力 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 57 | `M_CHAIN_TREND_INDEX` | CHAIN | 产业链变化趋势指数 | MODEL | pending_algorithm（企业增速*w1+专利增速*w2+资讯热度变化*w3+投融资变化*w4） |
| 58 | `M_ENT_AGGLOMERATION_INDEX` | ENT | 集聚指数 | MODEL | pending_algorithm（区位熵 LQ 或 基尼系数） |
| 59 | `M_ENT_CHAIN_COMPLETENESS` | ENT | 产业链完整度 | MODEL | pending_algorithm（覆盖环节数 / 全链环节数 * 100） |
| 60 | `M_ENT_CITY_AVG_TECH_POWER` | ENT | 城市平均技术力 | MODEL | pending_algorithm（AVG(tech_score) GROUP BY city） |
| 61 | `M_ENT_CITY_DENSITY` | ENT | 企业密度 | MODEL | pending_algorithm（城市企业数 / 城市面积或单位GDP） |
| 62 | `M_ENT_DIVERSIFICATION_INDEX` | ENT | 多元化指数 | MODEL | pending_algorithm（领域分布熵 Shannon entropy） |
| 63 | `M_ENT_DOMAIN_COVERAGE_BREADTH` | ENT | 覆盖广度 | MODEL | pending_algorithm（覆盖领域数 / 产业领域全集） |
| 64 | `M_ENT_DOMAIN_COVERAGE_DEPTH` | ENT | 参与深度 | MODEL | pending_algorithm（dwd_org_industry_chain_dtl.chain_score + 产 |
| 65 | `M_ENT_DS_02_ENTITY_004` | ENT | [新增] 技术点影响力 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 66 | `M_ENT_DS_07_INDUSTRY_POTENTIAL_004` | ENT | 科学影响力评估 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 67 | `M_ENT_DS_07_INDUSTRY_POTENTIAL_005` | ENT | 技术影响力评估 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 68 | `M_ENT_DS_07_INDUSTRY_POTENTIAL_006` | ENT | 产业发展潜力综合评估 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 69 | `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT` | ENT | 覆盖未来产业数 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 70 | `M_ENT_GROWTH_POTENTIAL` | ENT | 成长潜力 | MODEL | pending_algorithm（营收/研发增速 + 技术壁垒 + 团队规模 加权） |
| 71 | `M_ENT_HIGH_TECH_COUNT` | ENT | 高企数量 | STAT | pending_algorithm（解析 dwd_company_honor_tags/dwd_org_tag_info |
| 72 | `M_ENT_INDUSTRY_MATCH_SCORE` | ENT | 产业匹配度 | MODEL | pending_algorithm（基于 dwd_org_industry_chain_dtl.chain_score |
| 73 | `M_ENT_INNOVATIVE_COUNT` | ENT | 创新型企业数 | STAT | pending_algorithm（is_high_tech/is_little_giant/is_gazelle/is |
| 74 | `M_ENT_KEY_TOTAL` | ENT | 重点企业总数 | STAT | pending_cosign: human:唐绍祖（未签） |
| 75 | `M_ENT_MARKET_SHARE` | ENT | 市场份额 | STAT | pending_algorithm（企业营收 / 细分市场总规模）——缺市场规模数据 |
| 76 | `M_ENT_POLICY_MATCH_SCORE` | ENT | 政策匹配度 | MODEL | pending_algorithm（企业属性 vs 政策标签匹配评分） |
| 77 | `M_ENT_PROFIT_MARGIN` | ENT | 利润率 | MODEL | pending_algorithm（net_profit / operating_revenue * 100） |
| 78 | `M_ENT_RD_INVESTMENT_RATIO` | ENT | 研发投入占比 | STAT | pending_algorithm（rd_investment / revenue_latest * 100） |
| 79 | `M_ENT_REGIONAL_DENSITY` | ENT | 区域企业密度 | MODEL | pending_algorithm（区域企业数 / 区域面积 或 / 单位GDP） |
| 80 | `M_ENT_RESEARCHER_COUNT` | ENT | 全球企业科研人数 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 81 | `M_ENT_REVENUE_GROWTH_RATE` | ENT | 营收增长率 | STAT | pending_algorithm（(本年 operating_revenue − 上年) / 上年 * 100） |
| 82 | `M_ENT_STAR_ENTERPRISE_COUNT` | ENT | 明星企业数 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 83 | `M_ENT_TECH_RANK` | ENT | 技术力排名 | MODEL | pending_algorithm（RANK() OVER ORDER BY tech_score DESC） |
| 84 | `M_INNOV_DS_01_EVENTS_001` | INNOV | 事件关注度 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 85 | `M_INNOV_DS_01_EVENTS_002` | INNOV | 事件影响力 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 86 | `M_INNOV_DS_01_EVENTS_003` | INNOV | 重要性等级 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 87 | `M_INNOV_DS_02_PATH_001` | INNOV | 中心度 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 88 | `M_INNOV_DS_02_PATH_002` | INNOV | 关键节点重要性 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 89 | `M_INNOV_DS_02_PATH_003` | INNOV | 节点优先级/重要度 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 90 | `M_INNOV_DS_04_ACHIEVE_OVERVIEW_001` | INNOV | 创新价值 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 91 | `M_INNOV_DS_04_CARRIER_RANK_001` | INNOV | 创新能力指数 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 92 | `M_INNOV_DS_04_CARRIER_RANK_002` | INNOV | 多维度排名展示 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 93 | `M_INNOV_DS_04_MONITOR_001` | INNOV | 创新点发现 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 94 | `M_INNOV_DS_04_MONITOR_002` | INNOV | 创新价值评估 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 95 | `M_INNOV_DS_04_REALTIME_004` | INNOV | 创新影响分数 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 96 | `M_INNOV_DS_04_REALTIME_005` | INNOV | 创新影响预测 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 97 | `M_INNOV_DS_05_GBA_ACHIEVE_004` | INNOV | 创新热点区域识别 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 98 | `M_INNOV_DS_05_GBA_ANALYSIS_003` | INNOV | 优势因素分析 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 99 | `M_INNOV_DS_05_GBA_ANALYSIS_004` | INNOV | 短板因素分析 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 100 | `M_INNOV_DS_05_GBA_ANALYSIS_005` | INNOV | 机会因素分析 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 101 | `M_INNOV_DS_05_GBA_ANALYSIS_006` | INNOV | 威胁因素分析 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 102 | `M_INNOV_DS_06_CARRIER_003` | INNOV | 创新价值排名 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 103 | `M_INNOV_DS_07_SCI_CREATE_004` | INNOV | 科学创造力趋势预测 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 104 | `M_INNOV_DS_09_COMPREHENSIVE_005` | INNOV | 本地特色与优势分析 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 105 | `M_INNOV_DS_09_COMPREHENSIVE_006` | INNOV | 科技人才流动监控 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 106 | `M_INNOV_DS_09_COMPREHENSIVE_008` | INNOV | 潜在科技发展方向预警 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 107 | `M_INNOV_DS_09_RESEARCH_001` | INNOV | 研究领域重叠度 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 108 | `M_INNOV_DS_09_RESEARCH_002` | INNOV | 研究领域等级划分 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 109 | `M_INNOV_DS_09_RESEARCH_003` | INNOV | 竞争情报等级 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 110 | `M_INNOV_DS_09_RESEARCH_004` | INNOV | 多企业竞争情报比对 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 111 | `M_INNOV_DS_25_SOFTSCI_012` | INNOV | 影响力评价与应用反馈 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 112 | `M_INNOV_DS_26_ECO_012` | INNOV | 协同绩效与影响力智能评估 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 113 | `M_INNOV_DS_27_SPATIO_003` | INNOV | 热点区域自动识别与预警 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 114 | `M_INNOV_DS_27_SPATIO_012` | INNOV | 主题演化路径与创新前沿发现 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 115 | `M_INNOV_DS_29_INCUBATOR_006` | INNOV | 影响力评价 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 116 | `M_INNOV_DS_FACTORS_008` | INNOV | 要素影响力 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 117 | `M_INNOV_DS_FACTORS_012` | INNOV | 要素影响力 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 118 | `M_INNOV_DS_FACTORS_014` | INNOV | 要素影响力 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 119 | `M_INNOV_DS_FACTORS_015` | INNOV | 要素影响力 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 120 | `M_INNOV_DS_FACTORS_016` | INNOV | 要素聚类分析 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 121 | `M_INNOV_DS_FACTORS_018` | INNOV | 监测趋势预测 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 122 | `M_INNOV_DS_FACTORS_019` | INNOV | 监测异常点识别 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 123 | `M_POLICY_DS_07_POLICY_GUARD_001` | POLICY | 发展战略引导力评估 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 124 | `M_POLICY_DS_07_POLICY_GUARD_008` | POLICY | 政策与条件保障力综合评估 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 125 | `M_POLICY_DS_11_POLICY_EVAL_012` | POLICY | 智能摘要与结论推送 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 126 | `M_POLICY_DS_11_POLICY_EVAL_015` | POLICY | 实施路径与风险辅助 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 127 | `M_POLICY_EFFECT_SCORE` | POLICY | 政策效果评分 | MODEL | pending_algorithm（执行效果*w1 + 社会经济效应*w2 + 环境影响*w3；关键输入待采购，权重待 |
| 128 | `M_POLICY_FOCUS_INDEX` | POLICY | 政策焦点指数 | MODEL | pending_algorithm（焦点维度指标体系加权打分，维度/阈值待 QPOL-02） |
| 129 | `M_POLICY_IMPLEMENTATION_EFFECT` | POLICY | 落地实效性 | MODEL | pending_algorithm（落地执行率 + 受益覆盖 + 反馈满意度加权；关键输入待采购，权重待 QPOL-02 |
| 130 | `M_POLICY_INDUSTRY_COVERAGE` | POLICY | 政策产业覆盖度 | STAT | pending_algorithm（DISTINCT 覆盖产业节点数 / 产业链全节点数 * 100） |
| 131 | `M_POLICY_INDUSTRY_FIT` | POLICY | 产业适配性 | MODEL | pending_algorithm（政策标签 vs 产业需求标签相似度加权，匹配规则待 QPOL-03） |
| 132 | `M_POLICY_INTENSITY_INDEX` | POLICY | 政策力度指数 | MODEL | pending_algorithm（补贴*w1 + 税收优惠*w2 + 政策数量*w3 + 执行周期*w4，权重待 QP |
| 133 | `M_POLICY_INTENSITY_SCORE` | POLICY | 政策力度评分 | MODEL | pending_algorithm（效果维度*w1 + 覆盖维度*w2 + 成本维度*w3，权重待 QPOL-02） |
| 134 | `M_POLICY_LAYOUT_REC_COUNT` | POLICY | 政策布局建议数 | MODEL | pending_algorithm（COUNT(布局建议 WHERE 优先级评分 >= 阈值)，融合机遇/短板/专家策略 |
| 135 | `M_POLICY_OPPORTUNITY_COUNT` | POLICY | 政策机遇数 | MODEL | pending_algorithm（COUNT(政策 WHERE 关注度/影响力/稳定性 >= 阈值)，维度/阈值待 Q |
| 136 | `M_POLICY_RELATION_DEGREE` | POLICY | 政策关联度 | GRAPH | pending_algorithm（NebulaGraph gkx_policy 加权度中心性：扶持/适用/监管/引用 |
| 137 | `M_POLICY_SHORTBOARD_COUNT` | POLICY | 政策短板数 | MODEL | pending_algorithm（COUNT(短板维度 WHERE 评估值 < 阈值)，维度/阈值待 QPOL-02） |
| 138 | `M_POLICY_SUPPORT_STRENGTH` | POLICY | 支持力度 | STAT | pending_algorithm（扶持力度档位*w1 + 政策层级权重*w2 + 政策数量*w3，权重待 QPOL-0 |
| 139 | `M_POLICY_TYPE_DIST` | POLICY | 政策类型分布 | COMPUTE | pending_algorithm（解析 topic_type/ma_contenttypenew/complextag |
| 140 | `M_POLICY_VALIDITY_RATE` | POLICY | 政策时效 | STAT | pending_algorithm（COUNT(status=1 AND (expire_date IS NULL OR |
| 141 | `M_SVC_CHAIN_BOTTLENECK` | SVC | 瓶颈堵点判定 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 142 | `M_SVC_CHAIN_SEGMENT_AVG_DEPTH` | SVC | 环节平均服务深度 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 143 | `M_SVC_CHAIN_SEGMENT_ORG_COUNT` | SVC | 环节服务机构数 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 144 | `M_SVC_GRAPH_CENTRALITY` | SVC | 节点度中心性 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 145 | `M_SVC_GRAPH_DENSITY` | SVC | 服务网络密度 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 146 | `M_SVC_GRAPH_INFLUENCE` | SVC | 生态影响力评分 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 147 | `M_SVC_ORG_COVERAGE_BREADTH` | SVC | 服务广度 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 148 | `M_SVC_ORG_COVERAGE_DEPTH` | SVC | 服务深度得分 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 149 | `M_SVC_ORG_MARKET_HEAT` | SVC | 市场热度评级 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 150 | `M_SVC_ORG_NEW_COUNT` | SVC | 年度新增服务机构数 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 151 | `M_SVC_ORG_SELECTED_COUNT` | SVC | 当前分析机构数 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 152 | `M_SVC_ORG_TOTAL` | SVC | 入库服务机构总数 | STAT | pending_cosign: human:唐绍祖（未签） |
| 153 | `M_SVC_PT_CHAIN_NODE_ORG` | SVC | 产业链节点服务机构数 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 154 | `M_SVC_PT_GLOBAL_SCALE_DIST` | SVC | 全球服务机构规模分布 | STAT | pending_cosign: human:唐绍祖（未签） |
| 155 | `M_SVC_PT_GLOBAL_TOTAL` | SVC | 全球服务机构总数 | STAT | pending_cosign: human:唐绍祖（未签） |
| 156 | `M_SVC_PT_GLOBAL_TYPE_DIST` | SVC | 全球服务机构类型分布 | STAT | pending_cosign: human:唐绍祖（未签） |
| 157 | `M_SVC_PT_KEYORG_SCALE` | SVC | 重点机构规模档案值 | STAT | pending_cosign: human:唐绍祖（未签） |
| 158 | `M_SVC_PT_REGION_ORG` | SVC | 区域服务机构数 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 159 | `M_SVC_PT_SZ_FIELD_DIST` | SVC | 深圳机构产业领域分布 | STAT | pending_cosign: human:唐绍祖（未签） |
| 160 | `M_SVC_PT_SZ_REGION_ORG` | SVC | 深圳机构区域分布 | STAT | pending_cosign: human:唐绍祖（未签） |
| 161 | `M_SVC_PT_SZ_TOTAL` | SVC | 深圳产业服务机构数量 | STAT | pending_cosign: human:唐绍祖（未签） |
| 162 | `M_SVC_PT_SZ_TYPE_DIST` | SVC | 深圳机构类型统计 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 163 | `M_SVC_REC_ATTRACT_SCORE` | SVC | 招引综合评分 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 164 | `M_SVC_REC_CANDIDATE_CNT` | SVC | 候选机构数 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 165 | `M_SVC_REC_CULTIVATE_SCORE` | SVC | 培育综合评分 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 166 | `M_SVC_SZ_CHAIN_COMPLETENESS` | SVC | 服务链完整度 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 167 | `M_SVC_SZ_COMPARE_METRIC` | SVC | 城市对比指标值 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 168 | `M_SVC_SZ_TIER` | SVC | 深圳梯队位置 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 169 | `M_SYNTH_COLLAB_CENTRALITY` | SYNTH | 协同网络中心度 | GRAPH | pending_algorithm（节点度中心性 degree/(N-1)；正式算法待 Q-SYNTH-C-01 闭合） |
| 170 | `M_SYNTH_COLLAB_COMPLETENESS` | SYNTH | 协同网络完整度 | MODEL | pending_algorithm（已建立有效合作关系的主体数 / 纳入分析的有效主体总数 × 100%；正式分母待 Q |
| 171 | `M_SYNTH_COLLAB_DENSITY` | SYNTH | 协同网络密度 | GRAPH | pending_algorithm（无向简单图 2E/[N×(N-1)]；正式图模型待 Q-SYNTH-C-01 闭合） |
| 172 | `M_SYNTH_COLLAB_INDEX` | SYNTH | 区域创新协同指数 | MODEL | pending_algorithm（三指标归一化后加权合成；权重/校准待 Q-SYNTH-C-02 闭合） |
| 173 | `M_SYNTH_COLLAB_OUTPUT_CORR` | SYNTH | 协同—创新产出关联结果 | MODEL | pending_algorithm（Pearson/Spearman 相关；方法/样本门槛待 Q-SYNTH-C-03 |
| 174 | `M_SYNTH_DS_21_GRAPH_ANALYSIS_005` | SYNTH | 自动模式识别 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 175 | `M_SYNTH_DS_21_GRAPH_ANALYSIS_006` | SYNTH | 预测分析 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 176 | `M_SYNTH_DS_21_GRAPH_ANALYSIS_007` | SYNTH | 分类与聚类 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 177 | `M_SYNTH_DS_21_GRAPH_ANALYSIS_008` | SYNTH | 智能推荐 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 178 | `M_SYNTH_DS_23_GRAPH_ALGO_001` | SYNTH | 多种路径搜索算法支持 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 179 | `M_SYNTH_DS_23_GRAPH_ALGO_002` | SYNTH | 最优路径发现与展示 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 180 | `M_SYNTH_DS_23_GRAPH_ALGO_006` | SYNTH | 度中心性计算与展示 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 181 | `M_SYNTH_DS_23_GRAPH_ALGO_007` | SYNTH | 紧密中心性计算与展示 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 182 | `M_SYNTH_DS_23_GRAPH_ALGO_008` | SYNTH | 中介中心性计算与展示 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 183 | `M_SYNTH_DS_23_GRAPH_ALGO_009` | SYNTH | PageRank算法计算与展示 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 184 | `M_SYNTH_DS_23_GRAPH_ALGO_011` | SYNTH | 多种社群发现算法支持 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 185 | `M_SYNTH_DS_23_GRAPH_ALGO_012` | SYNTH | 社群结构自动识别 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 186 | `M_SYNTH_DS_23_GRAPH_ALGO_013` | SYNTH | 社群属性与特征分析 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 187 | `M_SYNTH_DS_23_GRAPH_ALGO_014` | SYNTH | 社群动态演化追踪 | GRAPH | pending_cosign: human:唐绍祖（未签） |
| 188 | `M_SYNTH_ELEM_CONTRIB` | SYNTH | 要素贡献度与影响路径 | GRAPH | pending_algorithm（贡献度量化 + 影响路径识别；方法待 Q-SYNTH-E-02 闭合） |
| 189 | `M_SYNTH_ELEM_DOMAIN_INDEX` | SYNTH | 区域创新要素领域指数 | MODEL | pending_algorithm（领域维度加权 + 归一化；权重待 Q-SYNTH-E-01 闭合） |
| 190 | `M_SYNTH_ELEM_INDEX` | SYNTH | 区域创新要素指数（综合） | MODEL | pending_algorithm（三维加权合成；权重/公式待 Q-SYNTH-02 闭合） |
| 191 | `M_SYNTH_ELEM_INDICATOR` | SYNTH | 要素分项指标值与得分 | MODEL | pending_algorithm（分项指标采集 + 归一化评分） |
| 192 | `M_SYNTH_ELEM_LEVEL_INDEX` | SYNTH | 区域创新要素层次指数 | MODEL | pending_algorithm（结构维度加权 + 达标判定；权重/阈值待 Q-SYNTH-E-01 闭合） |
| 193 | `M_SYNTH_ELEM_LEVEL_SCORE` | SYNTH | 七大结构层次评价 | MODEL | pending_algorithm（结构达标判定 + 层次评分） |
| 194 | `M_SYNTH_ELEM_TYPE_INDEX` | SYNTH | 区域创新要素类型指数 | MODEL | pending_algorithm（七要素加权 + 归一化；权重待 Q-SYNTH-E-01 闭合） |
| 195 | `M_SYNTH_ELEM_TYPE_SCORE` | SYNTH | 七要素类型维得分 | MODEL | pending_algorithm（各要素类型维加权评分；权重待 Q-SYNTH-E-01 闭合） |
| 196 | `M_SYNTH_ELEM_WEIGHT` | SYNTH | 类型/层次/领域权重分布 | STAT | pending_algorithm（三维权重分配待 Q-SYNTH-E-01 闭合） |
| 197 | `M_SYNTH_VIT_DIM_SCORE` | SYNTH | 四维单维评分 | MODEL | pending_algorithm（维度内加权求和 + 归一化；权重待 Q-SYNTH-V-01 闭合） |
| 198 | `M_SYNTH_VIT_INDEX` | SYNTH | 区域创新活力指数 | MODEL | pending_algorithm（四维加权求和；权重/归一化基准待 Q-SYNTH-01 闭合） |
| 199 | `M_SYNTH_VIT_INDICATOR` | SYNTH | 活力分项指标值与得分 | MODEL | pending_algorithm（分项指标值采集 + 归一化评分） |
| 200 | `M_SYNTH_VIT_WEIGHT` | SYNTH | 维度权重分布 | STAT | pending_algorithm（权重分配方案待 Q-SYNTH-V-01 闭合） |
| 201 | `M_TALENT_DS_16_TALENT_RECRUIT_005` | TALENT | 沟通障碍智能检测 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 202 | `M_TALENT_DS_16_TALENT_RECRUIT_006` | TALENT | 文化融合风险评估 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 203 | `M_TALENT_DS_16_TALENT_RECRUIT_007` | TALENT | 国际流动壁垒分析 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 204 | `M_TALENT_DS_16_TALENT_RECRUIT_010` | TALENT | 引进阻力量化评分 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 205 | `M_TALENT_DS_16_TALENT_RECRUIT_013` | TALENT | 高精度成本模型构建 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 206 | `M_TALENT_DS_16_TALENT_RECRUIT_025` | TALENT | 团队组合与协同分析 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 207 | `M_TECH_DS_07_TECH_INNOV_002` | TECH | 专利质量评估 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 208 | `M_TECH_DS_07_TECH_INNOV_004` | TECH | 技术创新力综合评估 | MODEL | pending_cosign: human:唐绍祖（未签） |
| 209 | `M_TECH_DS_07_TECH_INNOV_006` | TECH | 技术创新趋势预测 | MODEL | pending_cosign: human:唐绍祖（未签） |

## 分布

| domain | 条数 |
|---|---|
| CHAIN | 57 |
| INNOV | 39 |
| SYNTH | 32 |
| SVC | 28 |
| ENT | 26 |
| POLICY | 18 |
| TALENT | 6 |
| TECH | 3 |