# 重判明细 · CHAIN（99 条）

| # | metric_id | 分组 | 中文名 | 现type | definition | formula | 新判type | 理由 |
|---|---|---|---|---|---|---|---|---|
| 1 | `M_CHAIN_ACADEMIC_COOP_SCORE` | T3 | 产学研合作强度 | MODEL | pending_data_lead：产业链中企业与高校/科研机构的合作强度评分；合作类型与权重待确认。 | pending_algorithm（联合专利数*w1+联合项目数*w2+人才流动*w3） |  |  |
| 2 | `M_CHAIN_ACADEMIC_POWER` | T3 | 科研实力指数 | MODEL | pending_data_lead(QC05)：区域产业链科研实力指数；以专利/论文密度为基础，权重待确认。 | pending_algorithm（专利密度*w1 + 论文密度*w2 + 高校数量*w3） |  |  |
| 3 | `M_CHAIN_BOTTLENECK_COUNT` | T3 | 瓶颈堵点数 | STAT | pending_data_lead(QC04)：产业链中识别出的瓶颈/堵点数；瓶颈类型细分口径(5维是否完整)待甲方确认。 | COUNT(DISTINCT id) FROM dwd.industry_bottleneck |  |  |
| 4 | `M_CHAIN_BOTTLENECK_SEVERITY` | T3 | 瓶颈严重度 | MODEL | pending_data_lead(QC04)：产业链瓶颈的严重度评分（0-100，取最高严重度）；评分口径同 QC04。 | pending_algorithm（MAX(severity_score) FROM dwd.industry_bottleneck） |  |  |
| 5 | `M_CHAIN_BOTTLENECK_TYPE_DIST` | T3 | 瓶颈类型分布 | STAT | pending_data_lead(QC04)：按瓶颈类型（技术/人才/市场/资本/政策）的分布统计；类型口径同 QC04。 | COUNT(*) GROUP BY bottleneck_type FROM dwd.industry_bottleneck |  |  |
| 6 | `M_CHAIN_BREAK_RISK_COUNT` | T3 | 产业链断链风险数 | GRAPH | pending_data_lead(QC04)：产业链中存在断链风险的环节数；断链风险判定规则依赖 QC04。 | pending_algorithm（供应链节点中心性+替代性+地域集中度综合判定） |  |  |
| 7 | `M_CHAIN_CHOKE_LINK_COUNT` | T3 | 卡脖子环节数 | MODEL | 瓶颈∧severity=高；⊆ 瓶颈数；与图谱角标同计数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 8 | `M_CHAIN_COMPETITIVENESS_INDEX` | T3 | 区域竞争力指数 | MODEL | pending_data_lead(QC05)：区域产业链综合竞争力指数；派生自三维指数加权，权重同 QC05。 | pending_algorithm（M_CHAIN_REGION_INDEX + 排名归一化 + 趋势因子） |  |  |
| 9 | `M_CHAIN_COMPLETENESS_SCORE` | T3 | 产业链完整度评分 | MODEL | pending_data_lead(QC01)：产业链完整度综合评分（0-100）；基于上下游覆盖完整度、企业分布均匀度等，口径同 QC01。 | pending_algorithm（覆盖环节数/全链环节数*100 * 企业分布均匀度修正因子） |  |  |
| 10 | `M_CHAIN_CONCENTRATION_INDEX` | T3 | 产业集中度 | STAT | pending_data_lead(QC02)：产业链企业分布的集中度指数（HHI 或 CR_N）；口径与 N 值待甲方确认。 | pending_algorithm（HHI = SUM(企业市场份额^2) 或 CR_N = TopN企业市场份额之和） |  |  |
| 11 | `M_CHAIN_CYCLE_STAGE` | T3 | 周期阶段 | MODEL | pending_data_lead(QC03)：产业链当前所处生命周期阶段（萌芽期/成长期/成熟期/衰退期）；判定模型输入与阈值待甲方确认。 | pending_algorithm（基于企业增速/专利增速/投融资趋势/市场集中度的周期判定模型 CHAIN_CYCLE） |  |  |
| 12 | `M_CHAIN_DEVELOPMENT_MILESTONE_COUNT` | T3 | 发展里程碑数 | MODEL | 产业链发展路线中的里程碑事件数（重大技术突破/政策出台/龙头入驻等）；基于资讯+政策+企业事件综合提取。 | pending_algorithm（基于 dwd.industry_chain_news + 政策事件 NLP 提取里程碑） |  |  |
| 13 | `M_CHAIN_DOWNSTREAM_COUNT` | T3 | 下游环节数 | GRAPH | 产业链中下游环节去重计数；对象范围 dwd.industry_chain WHERE chain_stage='downstream'。 | COUNT(DISTINCT node_name) WHERE chain_stage='downstream' |  |  |
| 14 | `M_CHAIN_EDGE_COUNT` | T3 | 产业链边数 | GRAPH | 产业链图谱中所有关系边总数（belongs_to/participates/supplies/depends_on）；由 NebulaGraph gkx_chain 空间统计。 | pending_algorithm（NebulaGraph gkx_chain 边统计） |  |  |
| 15 | `M_CHAIN_ENTERPRISE_COUNT` | T3 | 产业链关联企业数 | STAT | 纳入产业链要素库的关联企业去重总数；统计窗口为最新批次快照，对象范围 dwd.industry_chain_enterprise 全量，按 enterprise_code 去重。 | COUNT(DISTINCT dwd.industry_chain_enterprise.enterprise_code) |  |  |
| 16 | `M_CHAIN_ENTERPRISE_NEW_COUNT` | T3 | 新增关联企业数 | STAT | 按年份分组新增产业链关联企业数；统计窗口为逐年，按 chain_score 首次出现年份或注册年份归集去重。 | COUNT(DISTINCT enterprise_code) GROUP BY YEAR(首次关联时间) |  |  |
| 17 | `M_CHAIN_ENTERPRISE_POWER` | T3 | 企业实力指数 | MODEL | pending_data_lead(QC05)：区域产业链企业实力指数；以 chain_score 为基础结合企业规模/营收/资质加权，权重待确认。 | pending_algorithm（AVG(chain_score) * 企业规模/资质加权因子） |  |  |
| 18 | `M_CHAIN_GLOBAL_CASE_MATCH` | T3 | 全球成功案例匹配 | MODEL | 算法库 05 产业链 13 叶无「全球成功案例匹配」叶子。V1 不宣称交付。禁止新造 M_*。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 19 | `M_CHAIN_GLOBAL_REGION_COUNT` | T3 | 全球分布区域数 | STAT | 产业链关联企业/机构覆盖的全球国家/地区去重数；按企业总部所在国家/地区 DISTINCT 计数。 | COUNT(DISTINCT region_code) WHERE scope='global' |  |  |
| 20 | `M_CHAIN_HIGH_VALUE_RATIO` | T3 | 高价值环节占比 | STAT | pending_data_lead(QC02)：高价值环节数占全部环节数比例；高价值判定口径同 QC02。 | pending_algorithm（高价值环节数 / 全部环节数 * 100） |  |  |
| 21 | `M_CHAIN_HOT_NEWS_COUNT` | T3 | 热门资讯数 | MODEL | pending_data_lead：热度评分达到阈值的资讯计数；阈值待甲方确认，临时默认 heat_score>=80。 | COUNT(DISTINCT news_id) WHERE heat_score >= 80 |  |  |
| 22 | `M_CHAIN_HOTSPOT_COUNT` | T3 | 热点领域数 | MODEL | 基于企业增速/投融资热度/专利密度等综合评分达到阈值的产业链/环节去重数；阈值与权重待确认。 | pending_algorithm（企业增速*w1+投融资热度*w2+专利密度*w3 >= 阈值） |  |  |
| 23 | `M_CHAIN_HOTSPOT_SCORE` | T3 | 热点评分 | MODEL | pending_data_lead：产业链/环节的热度综合评分；评分维度与权重待甲方确认。 | pending_algorithm（企业增速*w1+投融资热度*w2+专利密度*w3+资讯热度*w4） |  |  |
| 24 | `M_CHAIN_INSTITUTION_COUNT` | T3 | 产业链关联机构数 | STAT | 产业链关联科研机构/高校去重总数；对象范围 dwd.industry_chain_enterprise 中 org_type=机构 的记录，按 enterprise_name 去重。 | COUNT(DISTINCT enterprise_name) WHERE org_type='机构' |  |  |
| 25 | `M_CHAIN_INTERNATIONALIZATION_INDEX` | T3 | 产业链国际化程度 | STAT | pending_data_lead：产业链国际化程度指数；基于海外企业/专利/贸易数据，口径与权重待确认。 | pending_algorithm（海外企业占比*w1+海外专利占比*w2+进出口数据*w3） |  |  |
| 26 | `M_CHAIN_INVEST_COUNT` | T3 | 投融资事件数 | STAT | pending_data_lead(QC07)：产业链相关投融资事件去重计数；数据源同 M_CHAIN_INVEST_TOTAL。 | COUNT(DISTINCT news_id) WHERE news_type='financing' |  |  |
| 27 | `M_CHAIN_INVEST_TOTAL` | T3 | 投融资总额 | MODEL | pending_data_lead(QC07)：产业链相关投融资事件总金额（单位：万元）；可基于 dwd_industry_chain_news_info 融资类资讯+NLP抽取金额，或采购三方投融资数据库。 | pending_algorithm（NLP抽取融资金额 / 采购数据聚合） |  |  |
| 28 | `M_CHAIN_KEY_NODE_COUNT` | T3 | 关键环节数 | GRAPH | pending_data_lead(QC02)：产业链中被判定为关键环节的节点计数；判定阈值依赖 QC02。 | COUNT(DISTINCT node_name) WHERE is_key_node=1 |  |  |
| 29 | `M_CHAIN_LAYOUT_PRIORITY_SCORE` | T3 | 布局优先级评分 | MODEL | pending_data_lead(QC09)：产业链/环节的布局优先级综合评分；评分维度与权重依赖 QC09。 | pending_algorithm（战略重要性*w1+深圳缺口*w2+市场前景*w3+技术可行*w4） |  |  |
| 30 | `M_CHAIN_LAYOUT_RECOMMEND_COUNT` | T3 | 重点布局推荐数 | MODEL | pending_data_lead(QC09)：算法推荐的重点布局产业链/环节数；推荐算法权重与阈值待甲方确认。 | COUNT(DISTINCT chain_id) WHERE 布局优先级评分 >= 阈值 |  |  |
| 31 | `M_CHAIN_LINK_HEALTH` | T3 | 环节健康度 | MODEL | 专题要各环节健康度评分，算法库瓶颈叶只做五维堵点识别，无环节健康度叶子；B 轨无对应 ID。禁止用瓶颈计数或阶段模型冒充。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 32 | `M_CHAIN_MARKET_GROWTH` | T3 | 市场增长率 | STAT | 产业链市场规模同比增长率；依赖 M_CHAIN_MARKET_SIZE 相邻两年计算结果。 | (M_CHAIN_MARKET_SIZE(y)-M_CHAIN_MARKET_SIZE(y-1))/NULLIF(M_CHAIN_MARKET_SIZE(y-1),0)*100 |  |  |
| 33 | `M_CHAIN_MARKET_SIZE` | T3 | 市场规模 | STAT | 产业链下全部关联企业的年报营收合计（仅企业，不计机构/人才等）；单位默认亿元（展示换算在 ADS）。统计年与 ENT 年报字段对齐。非 ODS 直灌、非外购市调默认口径。 | SUM(ent_annual_revenue) WHERE enterprise_code IN (SELECT entity_id FROM industry_chain_entity_rel WHERE chain_id=:chain_ |  |  |
| 34 | `M_CHAIN_MIDSTREAM_COUNT` | T3 | 中游环节数 | GRAPH | 产业链中中游环节去重计数；对象范围 dwd.industry_chain WHERE chain_stage='midstream'。 | COUNT(DISTINCT node_name) WHERE chain_stage='midstream' |  |  |
| 35 | `M_CHAIN_NATIONAL_REGION_COUNT` | T3 | 全国分布区域数 | STAT | 产业链关联企业/机构覆盖的全国省/市去重数；按企业总部所在省/市 DISTINCT 计数。 | COUNT(DISTINCT headquarters_city) WHERE scope='national' |  |  |
| 36 | `M_CHAIN_NEWS_COUNT` | T3 | 动态资讯数 | STAT | 产业链相关资讯去重总数；统计窗口为最新批次快照，对象范围 dwd.industry_chain_news 全量，按 news_id 去重。 | COUNT(DISTINCT dwd.industry_chain_news.news_id) |  |  |
| 37 | `M_CHAIN_NEWS_SENTIMENT_RATIO` | T3 | 资讯正面情感占比 | STAT | 产业链相关资讯中正面情感占比（%）；基于 NLP 情感分析结果统计。 | pending_algorithm（COUNT(sentiment='positive') / COUNT(*) * 100） |  |  |
| 38 | `M_CHAIN_NODE_COUNT` | T3 | 产业链节点数 | GRAPH | 产业链图谱中所有节点去重总数（含产业链/环节/企业/机构节点）；由 NebulaGraph gkx_chain 空间统计。 | pending_algorithm（NebulaGraph gkx_chain LOOKUP COUNT） |  |  |
| 39 | `M_CHAIN_PATENT_COUNT` | T3 | 产业链关联专利数 | STAT | 产业链关联专利去重总数；对象范围 dwd.industry_chain_patent 全量，按 patent_id 去重。 | COUNT(DISTINCT dwd.industry_chain_patent.patent_id) |  |  |
| 40 | `M_CHAIN_PHASE_DETERMINATION` | T3 | 阶段判定 | MODEL | pending_data_lead(QC03)：产业链细分环节的发展阶段判定（技术突破期/产业化期/规模化期/转型期）；判定口径依赖 QC03。 | pending_algorithm（基于环节数据的分阶段判定模型） |  |  |
| 41 | `M_CHAIN_POLICY_MATCH_SCORE` | T3 | 产业政策匹配度 | MODEL | pending_data_lead：产业链与当前政策导向的匹配程度评分；需跨政策域数据，权重与口径待确认。 | pending_algorithm（产业链标签 vs 政策标签匹配评分） |  |  |
| 42 | `M_CHAIN_PRODUCT_COUNT` | T3 | 产业链关联产品数 | STAT | 产业链关联产品去重总数；对象范围 dwd.industry_chain_product 全量，按 product_id 去重。 | COUNT(DISTINCT dwd.industry_chain_product.product_id) |  |  |
| 43 | `M_CHAIN_REG_COMMERCIALIZATION` | T3 | 企业商业化能力 | MODEL | 区域内产业企业商业化落地与市场转化能力 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 44 | `M_CHAIN_REG_COMP_ACADEMIC` | T3 | 学术生态 | MODEL | 竞争力评价固定维度·学术生态 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 45 | `M_CHAIN_REG_COMP_ENTERPRISE` | T3 | 企业能力 | MODEL | 竞争力评价固定维度·企业能力 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 46 | `M_CHAIN_REG_COMP_SUPPORT` | T3 | 配套生态力 | MODEL | 竞争力评价固定维度·配套生态力（算法 Bid 称配套生态竞争力） 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 47 | `M_CHAIN_REG_ECOSYSTEM` | T3 | 配套生态 | MODEL | 区域内产业配套生态 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 48 | `M_CHAIN_REG_FINANCING` | T3 | 融资事件 | MODEL | 区域内产业相关融资事件 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 49 | `M_CHAIN_REG_PAPERS` | T3 | 高校论文 | MODEL | 区域内高校论文产出 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 50 | `M_CHAIN_REG_PATENT` | T3 | 专利 | MODEL | 区域内产业相关专利 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 51 | `M_CHAIN_REG_POLICY_COVERAGE` | T3 | 政策覆盖率 | MODEL | 区域内产业政策覆盖率 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 52 | `M_CHAIN_REG_RESEARCH_ORG` | T3 | 科研机构 | MODEL | 区域内科研机构规模或密度 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 53 | `M_CHAIN_REG_REVENUE` | T3 | 营收 | MODEL | 区域内相关企业营收规模 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 54 | `M_CHAIN_REG_SERVICE_ORG` | T3 | 服务机构 | MODEL | 区域内产业服务机构 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 55 | `M_CHAIN_REG_TALENT_STRUCTURE` | T3 | 人才结构 | MODEL | 区域内产业人才结构 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 56 | `M_CHAIN_REG_TECH_BARRIER` | T3 | 技术壁垒 | MODEL | 区域内产业技术壁垒 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 57 | `M_CHAIN_REG_TECH_MATURITY` | T3 | 技术成熟度 | MODEL | 区域内产业技术成熟度 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 58 | `M_CHAIN_REGION_INDEX` | T3 | 区域产业综合指数 | MODEL | pending_data_lead(QC05)：区域产业链综合指数（企业实力+科研实力+配套支撑三维加权）；权重 W1/W2/W3 待甲方确认。 | pending_algorithm（enterprise_power_score*W1 + academic_power_score*W2 + support_power_score*W3） |  |  |
| 59 | `M_CHAIN_STAGE_SCORE` | T3 | 周期阶段评分 | MODEL | pending_data_lead(QC03)：产业链当前周期阶段的确定性评分（0-100）；评分依赖周期判定模型 QC03。 | pending_algorithm（CHAIN_CYCLE 模型置信度输出） |  |  |
| 60 | `M_CHAIN_STRATEGIC_IMPORTANCE` | T3 | 战略重要性评分 | MODEL | pending_data_lead(QC02)：产业链/环节的战略重要性综合评分；评分维度与权重待甲方确认。 | pending_algorithm（技术壁垒*w1+市场集中度*w2+国产化率*w3+政策导向*w4） |  |  |
| 61 | `M_CHAIN_SUPPLY_RELATION_COUNT` | T3 | 供应链关系数 | GRAPH | 产业链中企业间供应链关系去重总数；由 NebulaGraph gkx_chain 空间 supplies 边统计。 | pending_algorithm（NebulaGraph gkx_chain supplies 边 COUNT） |  |  |
| 62 | `M_CHAIN_SUPPORT_POWER` | T3 | 配套支撑指数 | MODEL | pending_data_lead(QC05)：区域产业链配套支撑指数；以政策/服务密度为基础，权重待确认。 | pending_algorithm（政策匹配度*w1 + 服务机构密度*w2 + 基础设施*w3） |  |  |
| 63 | `M_CHAIN_SZ_ADVANTAGE_RANK` | T3 | 深圳优势排名 | MODEL | pending_data_lead(QC08)：深圳在产业链中的优势排名（与对标城市比较）；对标城市集合同 QC08。 | pending_algorithm（RANK() OVER ORDER BY 优势评分 DESC） |  |  |
| 64 | `M_CHAIN_SZ_ADVANTAGE_SCORE` | T3 | 深圳优势评分 | MODEL | pending_data_lead(QC08)：深圳在产业链中的综合优势评分；对标城市集合与权重待甲方确认。 | pending_algorithm（深圳产业密度*w1+企业实力*w2+科研实力*w3+政策支撑*w4） |  |  |
| 65 | `M_CHAIN_SZ_COMPLETENESS` | T3 | 深圳产业链完整度 | MODEL | pending_data_lead(QC01)：深圳覆盖的产业链环节数占全链环节数比例；完整度口径（按节点数/按企业覆盖/按产值覆盖）待甲方确认。 | pending_algorithm（深圳覆盖环节数 / 全链环节数 * 100） |  |  |
| 66 | `M_CHAIN_SZ_ENTERPRISE` | T3 | 对比四维-企业 | MODEL | 深圳与标杆在企业集聚等维度的对比值。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 67 | `M_CHAIN_SZ_ENTERPRISE_COUNT` | T3 | 深圳产业链企业数 | STAT | 总部在深圳且属目标产业链的企业去重数；按 headquarters_city=深圳 + chain_id 筛选 COUNT。 | COUNT(DISTINCT enterprise_code) WHERE headquarters_city='深圳' AND chain_id IN(:chains) |  |  |
| 68 | `M_CHAIN_SZ_ENTERPRISE_RATIO` | T3 | 深圳产业链企业占比 | STAT | 深圳产业链关联企业数占全国该产业链企业总数比例；直接聚合计算。 | M_CHAIN_SZ_ENTERPRISE_COUNT / M_CHAIN_ENTERPRISE_COUNT * 100 |  |  |
| 69 | `M_CHAIN_SZ_INSTITUTION_COUNT` | T3 | 深圳产业链机构数 | STAT | 总部在深圳且属目标产业链的科研机构/高校去重数；口径同 M_CHAIN_SZ_ENTERPRISE_COUNT 加 org_type=机构。 | COUNT(DISTINCT enterprise_name) WHERE headquarters_city='深圳' AND org_type='机构' |  |  |
| 70 | `M_CHAIN_SZ_KEY_NODE_COUNT` | T3 | 深圳关键环节覆盖数 | GRAPH | 深圳企业覆盖的产业链关键环节数；基于 industry_chain_enterprise + is_key_node 统计。 | COUNT(DISTINCT node_name) WHERE is_key_node=1 AND headquarters_city='深圳' |  |  |
| 71 | `M_CHAIN_SZ_KEY_NODE_COVERAGE` | T3 | 深圳关键环节覆盖率 | MODEL | pending_data_lead(QC02)：深圳覆盖的关键环节数占全链关键环节总数比例；关键环节判定口径同 QC02。 | pending_algorithm（深圳覆盖关键环节数 / 全链关键环节数 * 100） |  |  |
| 72 | `M_CHAIN_SZ_OPPORTUNITY_COUNT` | T3 | 深圳产业机遇数 | MODEL | pending_data_lead：深圳在产业链中可把握的机遇数量；机遇识别口径与阈值待甲方确认。 | pending_algorithm（基于产业缺口+深圳优势匹配的机遇识别模型） |  |  |
| 73 | `M_CHAIN_SZ_OPPORTUNITY_SCORE` | T3 | 深圳产业机遇评分 | MODEL | pending_data_lead：深圳在产业链中的机遇综合评分；评分维度与权重待甲方确认。 | pending_algorithm（产业缺口*w1+深圳匹配度*w2+政策机遇*w3） |  |  |
| 74 | `M_CHAIN_SZ_PATENT` | T3 | 对比四维-专利 | MODEL | 深圳与标杆在专利产出等维度的对比值。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 75 | `M_CHAIN_SZ_POLICY` | T3 | 对比四维-政策 | MODEL | 深圳与标杆在政策供给等维度的对比值。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 76 | `M_CHAIN_SZ_PROBLEM_COUNT` | T3 | 深圳产业问题数 | STAT | 深圳在产业链中面临的问题/短板数量；基于瓶颈识别+深圳切片统计。 | COUNT(DISTINCT id) FROM dwd.industry_bottleneck WHERE region_code LIKE '4403%' |  |  |
| 77 | `M_CHAIN_SZ_REGION_COUNT` | T3 | 深圳产业分布区域数 | STAT | 深圳产业链关联企业/机构覆盖的区/县去重数；按深圳下辖区划 DISTINCT 计数。 | COUNT(DISTINCT headquarters_district) WHERE headquarters_city='深圳' |  |  |
| 78 | `M_CHAIN_SZ_TALENT` | T3 | 对比四维-人才 | MODEL | 深圳与标杆在人才供给等维度的对比值。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 79 | `M_CHAIN_TECH_MATURITY_SCORE` | T3 | 技术成熟度评分 | MODEL | pending_data_lead(QC03)：产业链技术成熟度评分（基于专利生命周期/技术迭代速度等）；评分口径依赖 QC03。 | pending_algorithm（专利平均年龄*w1+专利增长率*w2+技术覆盖度*w3） |  |  |
| 80 | `M_CHAIN_TECH_POWER` | T3 | 技术力 | MODEL | 区域内专利、技术成熟度与技术壁垒综合得分 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 81 | `M_CHAIN_TOTAL_COUNT` | T3 | 产业链总数 | STAT | 纳入要素库的产业链去重总数；统计窗口为最新批次快照，对象范围 dwd.industry_chain 全量，按 chain_id 去重。 | COUNT(DISTINCT dwd.industry_chain.chain_id) |  |  |
| 82 | `M_CHAIN_TREND_INDEX` | T3 | 产业链变化趋势指数 | MODEL | pending_data_lead：产业链近期变化趋势综合指数（企业增减/专利增速/资讯热度变化等）；口径与权重待确认。 | pending_algorithm（企业增速*w1+专利增速*w2+资讯热度变化*w3+投融资变化*w4） |  |  |
| 83 | `M_CHAIN_UPSTREAM_COUNT` | T3 | 上游环节数 | GRAPH | 产业链中上游环节去重计数；对象范围 dwd.industry_chain WHERE chain_stage='upstream'。 | COUNT(DISTINCT node_name) WHERE chain_stage='upstream' |  |  |
| 84 | `M_CHAIN_BASE_95_1` | TTEMP | 产业链基础指标模型构建 | STAT | 产业链基础指标模型构建：对应算法库 SRS ALGO-CHAIN-BASE-95，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 85 | `M_CHAIN_DEEP_117_1` | TTEMP | 产业链全景模型构建 | MODEL | 产业链全景模型构建：对应算法库 SRS ALGO-CHAIN-DEEP-117，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 86 | `M_CHAIN_DEEP_118_1` | TTEMP | 深圳产业链模型构建 | MODEL | 深圳产业链模型构建：对应算法库 SRS ALGO-CHAIN-DEEP-118，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 87 | `M_CHAIN_DEEP_119_1` | TTEMP | 产业发展路线历程模型 | MODEL | 产业发展路线历程模型：对应算法库 SRS ALGO-CHAIN-DEEP-119，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 88 | `M_CHAIN_DEEP_120_1` | TTEMP | 产业热点领域识别模型 | MODEL | 产业热点领域识别模型：对应算法库 SRS ALGO-CHAIN-DEEP-120，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 89 | `M_CHAIN_DEEP_121_1` | TTEMP | 深圳产业优势识别模型 | MODEL | 深圳产业优势识别模型：对应算法库 SRS ALGO-CHAIN-DEEP-121，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 90 | `M_CHAIN_DEEP_122_1` | TTEMP | 产业周期分析模型 | MODEL | 产业周期分析模型：对应算法库 SRS ALGO-CHAIN-DEEP-122，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 91 | `M_CHAIN_DEEP_123_1` | TTEMP | 产业阶段分析模型 | MODEL | 产业阶段分析模型：对应算法库 SRS ALGO-CHAIN-DEEP-123，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 92 | `M_CHAIN_DEEP_124_1` | TTEMP | 产业链关键环节识别模型 | MODEL | 产业链关键环节识别模型：对应算法库 SRS ALGO-CHAIN-DEEP-124，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 93 | `M_CHAIN_DEEP_125_1` | TTEMP | 产业瓶颈堵点识别模型 | MODEL | 产业瓶颈堵点识别模型：对应算法库 SRS ALGO-CHAIN-DEEP-125，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 94 | `M_CHAIN_DEEP_126_1` | TTEMP | 区域产业指数模型 | MODEL | 区域产业指数模型：对应算法库 SRS ALGO-CHAIN-DEEP-126，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 95 | `M_CHAIN_DEEP_127_1` | TTEMP | 深圳问题识别模型 | MODEL | 深圳问题识别模型：对应算法库 SRS ALGO-CHAIN-DEEP-127，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 96 | `M_CHAIN_DEEP_128_1` | TTEMP | 深圳机遇分析模型 | MODEL | 深圳机遇分析模型：对应算法库 SRS ALGO-CHAIN-DEEP-128，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 97 | `M_CHAIN_DEEP_129_1` | TTEMP | 重点布局产业推荐模型 | MODEL | 重点布局产业推荐模型：对应算法库 SRS ALGO-CHAIN-DEEP-129，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 98 | `M_CHAIN_GRAPH_102_1` | TTEMP | 产业实体识别构建 | GRAPH | 产业实体识别构建：对应算法库 SRS ALGO-CHAIN-GRAPH-102，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 99 | `M_CHAIN_GRAPH_103_1` | TTEMP | 产业实体关系抽取 | GRAPH | 产业实体关系抽取：对应算法库 SRS ALGO-CHAIN-GRAPH-103，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
