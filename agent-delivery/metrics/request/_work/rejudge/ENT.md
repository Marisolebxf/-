# 重判明细 · ENT（79 条）

| # | metric_id | 分组 | 中文名 | 现type | definition | formula | 新判type | 理由 |
|---|---|---|---|---|---|---|---|---|
| 1 | `M_ENT_ATTRACTION_INDEX` | T1 | 招引推荐指数 | MODEL | 对企业作为招商引资目标对象的价值进行综合量化评价的指数，综合反映企业在产业相关度、政策匹配度、深圳连接度三个维度的价值。 | 各维度极值归一化、三维(产业相关度/政策匹配度/深圳连接度)加权汇总。 |  |  |
| 2 | `M_ENT_BUSINESS_POWER_SCORE` | T1 | 商业力得分 | MODEL | 企业商业力评估的综合得分，满分0-100分，综合反映企业在市场、产品、品牌、技术合作、产业链覆盖率、产业关键环节参与度六个维度的综合水平。采用主成分分析法。 | 六维主成分分析：市场(营收/市占率/盈利) + 产品(产品线覆盖/新产品收入/质量) + 品牌(声量/行业声誉) + 技术合作(产学研项目/外部专家) + 产业链覆盖率 + 关键环节参与度 |  |  |
| 3 | `M_ENT_COMPETITIVENESS_SCORE` | T1 | 综合竞争力得分 | MODEL | 企业综合竞争力评估的综合得分，满分0-100分，综合反映企业在企业规模、财务状况、人力资源、市场表现四个维度的综合水平。采用加权汇总法。 | 各指标极值归一化、四维加权汇总：企业规模(资产总额/从业人员数) + 财务状况(营收利润率/资产负债率/总资产周转率) + 人力资源(本科及以上占比/研发人员占比) + 市场表现(市场占有率/销售收入) |  |  |
| 4 | `M_ENT_CULTIVATION_INDEX` | T1 | 培育推荐指数 | MODEL | 对区域优质中小企业培育推荐工作成效进行综合量化评价的指数，综合反映企业在产业相关度、政策匹配度、企业潜力三个维度的培育价值。 | 将产业相关度、政策匹配度、企业潜力三个维度的得分按权重加权求和，得出培育推荐指数综合得分。 |  |  |
| 5 | `M_ENT_DOMAIN_COVERAGE_COUNT` | T1 | 覆盖领域数 | STAT | 企业涉及的产业领域去重数；对象范围 dwd.enterprise_industry，按 industry_chain/领域字段 DISTINCT 计数。 | COUNT(DISTINCT dwd.enterprise_industry.industry_chain) |  |  |
| 6 | `M_ENT_KEY_TOTAL` | T1 | 重点企业总数 | STAT | 按专利数/技术交易额双阈值识别重点企业，去重统计目标企业数量。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 7 | `M_ENT_NEW_COUNT_Y` | T1 | 历年新增企业数 | STAT | 按注册年份分组的新登记企业数。从dwd_org_base_info取incorporation_date，按YEAR分组COUNT(DISTINCT org_id)。 | COUNT(DISTINCT org_id) GROUP BY YEAR(incorporation_date)，并计算累计 cumulative_count |  |  |
| 8 | `M_ENT_PAINPOINT_COUNT` | T1 | 痛难点总数 | MODEL | Q018 基线（2026-08-11 临时默认闭合）：诊断维度固定为技术研发/市场拓展/融资/管理四维。命中规则：研发投入同比下降→技术；营收同比下降→市场；融资轮次停滞→融资；管理维无稳定时序则 insufficient 暂不判断。计数为命中痛难点条数（可按企业去重扩展）。 | COUNT(pain_issues) WHERE dimension IN (technology,market,finance,management) AND data_status!='insufficient' |  |  |
| 9 | `M_ENT_SUPPLY_CHAIN_RISK` | T1 | 断链风险等级 | MODEL | 对企业供应链因内外部因素导致中断的可能性及其影响程度的综合评价等级。 | 供应链韧性指数 = 加权汇总(资金关系/供需稳固/产品流动/绩效波动)，映射断链风险等级(低/中/高)。 |  |  |
| 10 | `M_ENT_TECH_POWER_SCORE` | T1 | 技术力得分 | MODEL | 企业技术力评估的综合得分，满分0-100分，综合反映企业在技术人才、技术创新、技术转化、技术合作、技术投入五个维度的综合水平。采用加权平均。 | 五维加权平均：技术人才(development_employee/employees_number) + 技术创新(有效发明专利数/专利占比/新增申请) + 技术转化(新产品销售收入占比/技术合同成交额) + 技术合作(产学研项目数/外部专 |  |  |
| 11 | `M_ENT_TYPE_COUNT` | T1 | 各类型企业数 | STAT | 按企业类型（外资/高新/小微/上市/专精特新/小巨人）分组的企业计数。外企：org_type LIKE %外商%；上市：dwd_org_stock_base 去重；小微：scale_tag in(小型,微型)；高新/专精特新/小巨人：dwd_org_tech_tag.org_tag 筛选。 | 外企=COUNT(org_type LIKE %外商%)；上市=COUNT(DISTINCT dwd_org_stock_base)；高新/专精特新/小巨人=COUNT(DISTINCT org_id) FROM dwd_org_tech_ |  |  |
| 12 | `M_ENT_CITY_COMPARE_TOPIC` | T2 | 多城市企业群对标值 | MIXED | 统计窗口默认自然年。深圳企业群 vs 对照城市集合，输出平均技术力、平均商业力、企业密度等 城市聚合值。对照集合内部默认=05 seq 141 全国加权参照（Q-MO-ENT-06），不用 04 北上苏、 也不改挂 Q016 北上苏广。密度无独立核。城市聚合后再比；技术力/商业力派生自本页已 reuse 的 SCORE | pending_cosign: human:唐绍祖（未签） |  |  |
| 13 | `M_ENT_DOMAIN_DIST_TOPIC` | T2 | 企业领域分布 | STAT | 统计窗口默认自然年。对象=选定产业下名录去重。以年报/专利/产品映射到产业或技术领域后， 按 field_id 分组的企业去重数及该分布的同比增长率。领域分类临时默认与专题产业/技术领域 映射一致，不改挂展示 Q013。参与深度/多元化无独立核（ENT-B03），不另造 DEPTH ID。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 14 | `M_ENT_PAINPOINT_TOPIC` | T2 | 发展痛难点诊断 | MODEL | G3 Job。输出问题/瓶颈清单及建议报告（描述、成因、实践、方案）。 诊断维内部默认=05.3 `.5.3` 经营/盈利/效率/人才（Q-MO-ENT-09）， 因此不 reuse Q018 四维的 M_ENT_PAINPOINT_COUNT。分项维无独立 ID。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 15 | `M_ENT_REGIONAL_COUNT_TOPIC` | T2 | 区域企业数量规模占比 | STAT | 统计窗口默认自然年。对象=选定产业下名录去重。全国→省→市下钻，输出各区域 企业去重数、规模、占当期集合占比。三级地图可视化不进本核。规模口径见 Q-MO-ENT-02。 不消费展示 M_ENT_REGIONAL_COUNT（仅计数、无规模/占比面）。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 16 | `M_ENT_SUPPLY_STRUCT_TOPIC` | T2 | 供应链结构指标 | GRAPH | A 面 G1/G2（CUT-D6 不进 B 面）。对象=目标企业多级供应商/客户网络（Nebula 当前图）。 同核输出供应商数量、距离/稳定性、密度/紧密度、中心性，并支撑断链风险标注。 默认多级（非展示一级上游）。N<2 不计算密度。备份方案无核（ENT-B09），不另造 ID。 实体识别/关系抽取无独立统计核。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 17 | `M_ENT_SZ_LIST_TOPIC` | T2 | 深圳企业清单与链中角色 | STAT | 统计窗口默认自然年。选定产业链下深圳企业去重清单，并标注链中角色。 「深圳」内部默认=总部在深圳（与 M_ENT_SZ_COUNT 对象一致，见 Q-MO-ENT-05）； 角色依赖关系抽取（ENT-D14），不另造定位 ID，也不 reuse ODS 直取的 SZ_CHAIN_POSITION。 清单规模为同核 ST | pending_cosign: human:唐绍祖（未签） |  |  |
| 18 | `M_ENT_TYPE_DIST_TOPIC` | T2 | 重点企业类型分布 | STAT | 统计窗口默认自然年。对象=用户选定产业下企业名录去重。按类型标签分组输出 去重企业数、占当期集合占比、环比。类型字典内部默认=招标四类（外企/高企/小微/上市）， 见 Q-MO-ENT-01；不自动并入展示 Q010 的专精特新/小巨人。筛选壳本身不是本核。 重点企业门槛不另造 ID、不改挂 Q038。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 19 | `M_ENT_AGGLOMERATION_INDEX` | T3 | 集聚指数 | MODEL | 衡量企业在区域内空间集聚程度（区位熵/基尼系数）；formula 待 algorithm-agent，区划精度依赖 Q012。 | pending_algorithm（区位熵 LQ 或 基尼系数） |  |  |
| 20 | `M_ENT_ATTRACT_SCORE` | T3 | 招引推荐评分（demo路径） | GRAPH | ENT-DEEP-GAP-L01 demo 快路径：基于 enterprise_score 综合分 + tech_proxy + 风险扣减的招引推荐评分；与 M_ENT_ATTRACTION_INDEX（三维招引指数）并行，待 Q015 确认后合并。 | attract_score = w_tech*tech_proxy + w_growth*growth + w_regional*regional - risk_penalty; rank DESC |  |  |
| 21 | `M_ENT_AVG_RD_INVESTMENT` | T3 | 平均研发投入 | STAT | 企业平均研发投入额（单位：亿元）；统计窗口最新批次，对象范围为 rd_investment 非空企业，取算术平均。 | AVG(dwd.enterprise.rd_investment) |  |  |
| 22 | `M_ENT_CHAIN_COMPLETENESS` | T3 | 产业链完整度 | MODEL | 城市/区域覆盖的产业链环节占全链环节比例；源环节数据可得，需算法计算覆盖率。 | pending_algorithm（覆盖环节数 / 全链环节数 * 100） |  |  |
| 23 | `M_ENT_CITY_AVG_TECH_POWER` | T3 | 城市平均技术力 | MODEL | pending_data_lead(Q014)：城市内企业技术力评分均值；技术力权重口径同 Q014，城市集合参考 Q016。 | pending_algorithm（AVG(tech_score) GROUP BY city） |  |  |
| 24 | `M_ENT_CITY_DENSITY` | T3 | 企业密度 | MODEL | pending_data_lead(Q016)：对标城市企业密度；对标城市集合（默认北京/上海/苏州/广州）待甲方确认，formula 待算法实现。 | pending_algorithm（城市企业数 / 城市面积或单位GDP） |  |  |
| 25 | `M_ENT_COMPETITIVENESS_RANK` | T3 | 综合竞争力排名 | MODEL | 在同一产业、同一统计期内的可比企业集合内，按企业综合竞争力得分从高到低进行降序排名。 | 基于ads_ent_competitiveness_score表中score字段在同业分组内降序排名。 |  |  |
| 26 | `M_ENT_CORE_SUPPLIER_COUNT` | T3 | 核心供应商数 | MODEL | Q017 基线（2026-08-11 临时默认闭合）：直接一级供应商中，按投资关系金额 TOP5（无供应份额字段时的代理；可用 chain_score 辅证）计为核心供应商。 | COUNT(DISTINCT related_enterprise_id) WHERE relation_level=1 AND rank_by_invest_amount<=5 |  |  |
| 27 | `M_ENT_CULTIVATE_SCORE` | T3 | 培育推荐评分（demo路径） | GRAPH | ENT-DEEP-GAP-L01 demo 快路径：基于 enterprise_score 综合分 + 成长分 + 诊断短板恢复潜力的培育推荐评分；与 M_ENT_CULTIVATION_INDEX（三维培育指数）并行，待 Q015 确认后合并。 | cultivate_score = w_potential*score_total + w_growth*growth + w_recovery*(100-penalty); rank DESC |  |  |
| 28 | `M_ENT_DEV_HISTORY` | T3 | 企业发展历程 | MODEL | 企业历年财务、专利统计、重点资讯事件合并时间线；按年份倒序输出 timeline。 | timeline = merge(dwd.enterprise_finance_history, dwd.enterprise_patent_history, dwd.enterprise_news) ORDER BY year DESC |  |  |
| 29 | `M_ENT_DIVERSIFICATION_INDEX` | T3 | 多元化指数 | MODEL | pending_data_lead(Q013)：企业领域分布的多元化程度（领域分布熵）；权重与口径待确认，formula 待算法实现。 | pending_algorithm（领域分布熵 Shannon entropy） |  |  |
| 30 | `M_ENT_DOMAIN_COVERAGE_BREADTH` | T3 | 覆盖广度 | MODEL | pending_data_lead(Q013)：覆盖广度=覆盖领域数/产业领域全集，领域全集与权重口径待算法 lead + 甲方确认。 | pending_algorithm（覆盖领域数 / 产业领域全集） |  |  |
| 31 | `M_ENT_DOMAIN_COVERAGE_DEPTH` | T3 | 参与深度 | MODEL | pending_data_lead(Q013)：企业在所涉领域的产业链参与深度；以 chain_score 为基础结合产品/专利贡献加权，口径待确认。 | pending_algorithm（dwd_org_industry_chain_dtl.chain_score + 产品/专利贡献加权） |  |  |
| 32 | `M_ENT_DS_02_ENTITY_004` | T3 | [新增] 技术点影响力 | MODEL | 05 无技术点关联实体优先级专叶。关联强度排序不重复 missing。 禁止用 PATH 中心度/关键节点或 M_SVC_GRAPH_INFLUENCE 顶替。见 ENT-D04 / ENT-B03。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 33 | `M_ENT_DS_07_INDUSTRY_POTENTIAL_004` | T3 | 科学影响力评估 | MODEL | 算法库无产业科学影响力专叶。禁止 mapped 182 / 05 seq 149。禁止 also_in DS-01-FACTORS。见 POT-D04。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 34 | `M_ENT_DS_07_INDUSTRY_POTENTIAL_005` | T3 | 技术影响力评估 | MODEL | 算法库无产业技术影响力 / SEP 专叶。禁止 mapped 145 / 05 seq 150。禁止 also_in DS-01-FACTORS。见 POT-D05。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 35 | `M_ENT_DS_07_INDUSTRY_POTENTIAL_006` | T3 | 产业发展潜力综合评估 | MODEL | 对照 183 对不上（成果≠潜力五项）。禁止伪 mapped 183/135/186。禁止 mapped 05 seq 151。 不重列 TOPIC-TECH-05 潜力 Job。不 also_in 专题。见 POT-D06。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 36 | `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT` | T3 | 覆盖未来产业数 | MODEL | 当前数据实际覆盖的未来产业去重数；分母先按 5 个未来集群。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 37 | `M_ENT_GROWTH_POTENTIAL` | T3 | 成长潜力 | MODEL | pending_data_lead(Q015)：企业成长潜力评分（增速+技术壁垒+团队）；构成与权重依赖招引/培育口径，待甲方确认。 | pending_algorithm（营收/研发增速 + 技术壁垒 + 团队规模 加权） |  |  |
| 38 | `M_ENT_HIGH_TECH_COUNT` | T3 | 高企数量 | STAT | pending_data_lead(Q010)：高新技术企业判定规则待甲方确认；临时默认按资质/荣誉标签解析 is_high_tech=1 计数。 | pending_algorithm（解析 dwd_company_honor_tags/dwd_org_tag_info 高新技术企业标签后 COUNT） |  |  |
| 39 | `M_ENT_INDUSTRY_MATCH_SCORE` | T3 | 产业匹配度 | MODEL | pending_data_lead(Q015)：企业与目标产业链的匹配程度评分；以 chain_score 为基础，权重待确认。bid 名称为产业相关度，招引与培育共用。 | pending_algorithm（基于 dwd_org_industry_chain_dtl.chain_score 与目标产业相似度） |  |  |
| 40 | `M_ENT_INNOVATION_INDEX` | T3 | 创新能力指数 | MODEL | 企业创新能力评估的综合得分，满分0-100分，综合反映企业在创新投入、创新产出及可持续发展方面的综合水平。 | 三准则层加权汇总：创新投入(研发投入占比/技术人员占比) + 创新产出(专利申请数/专利质量/软著/获奖) + 可持续发展(总资产/营收/净利润/研发投入增长率) |  |  |
| 41 | `M_ENT_INNOVATIVE_COUNT` | T3 | 创新型企业数 | STAT | pending_data_lead(Q011)：创新型企业口径（=高企∪专精特新∪瞪羚∪独角兽？）待甲方确认；临时默认取四类资质标签并集去重计数。 | pending_algorithm（is_high_tech/is_little_giant/is_gazelle/is_unicorn 标签解析后取并集计数） |  |  |
| 42 | `M_ENT_KEY_NODE_COUNT` | T3 | 重点环节企业数 | GRAPH | 按产业链重点环节分组的企业去重数；对象范围 dwd.enterprise_industry，按 node 分组计数。 | COUNT(DISTINCT enterprise_id) GROUP BY dwd.enterprise_industry.industry_chain_node |  |  |
| 43 | `M_ENT_KEYPANO_DOMAIN_SUMMARY` | T3 | 领域摘要（当前链位） | MODEL | 当前链位下论文/专利关键词到产业领域/环节的映射结果及关联企业；依赖 Q013/Q047 映射规则。 | 关键词抽取 → 领域映射 → COUNT 分组; 证据来源: dwd_paper_keywords, dwd_patent_keywords |  |  |
| 44 | `M_ENT_KEYPANO_ENTERPRISE_LIST` | T3 | 企业清单（当前链位） | GRAPH | 当前链位下重点企业分页列表，含企业名称、资质标签、基础信息；依赖 Q038 识别阈值。 | SELECT enterprise_id, enterprise_name, honor_type_list, region_level JOIN chain_node_mapping WHERE chain_node=:node |  |  |
| 45 | `M_ENT_KEYPANO_MATCH_COUNT` | T3 | 匹配企业数 | GRAPH | 当前产业链+链位条件下命中重点企业去重计数；依赖 Q038 重点企业识别阈值。 | COUNT(DISTINCT enterprise_id) FILTER(industry_chain=:chain AND chain_node=:node AND is_published=1) |  |  |
| 46 | `M_ENT_KEYPANO_QUAL_DISTRIBUTION` | T3 | 整链资质分布 | STAT | 当前整条产业链四项资质×三个地域层级的绝对数量横向分组；依赖 Q010/Q047 口径。 | 4 qual_types × 3 region_levels grid: COUNT(DISTINCT enterprise_id) GROUP BY qual_type, region_level |  |  |
| 47 | `M_ENT_KEYPANO_REGIONAL_COUNT` | T3 | 覆盖区域数 | STAT | 当前产业链下至少命中1家企业的行政区域去重数（市/省/国家三级）；依赖 Q012 行政区划精度。 | COUNT(DISTINCT administrative_region) WHERE industry_chain=:chain |  |  |
| 48 | `M_ENT_KEYPANO_REGIONAL_DISTRIBUTION` | T3 | 区域分布 | STAT | 当前产业链下按行政区域分组的企业数量分布；依赖 Q012 行政区划精度。 | COUNT(DISTINCT enterprise_id) GROUP BY administrative_region WHERE industry_chain=:chain |  |  |
| 49 | `M_ENT_KEYPANO_TYPE_COUNT` | T3 | 覆盖企业类型数 | STAT | 当前结果集中至少命中1家企业的资质类型去重数；依赖 Q010 外企/高企/小微/上市口径。 | COUNT(DISTINCT honor_type) FROM current_result_set |  |  |
| 50 | `M_ENT_KEYPANO_TYPE_STRUCTURE` | T3 | 企业类型分布（当前链位） | GRAPH | 当前链位下按资质类型分组的企业数量分布；依赖 Q010 口径。 | COUNT(DISTINCT enterprise_id) GROUP BY honor_type FROM current_chain_node |  |  |
| 51 | `M_ENT_MARKET_SHARE` | T3 | 市场份额 | STAT | 企业在所属细分市场的营收占有率；ODS 要素库无市场规模/竞品数据，需额外采购市场调研数据。 | pending_algorithm（企业营收 / 细分市场总规模）——缺市场规模数据 |  |  |
| 52 | `M_ENT_NODE_CENTRALITY` | T3 | 供应链中心性 | GRAPH | 企业在供应链网络中靠近核心位置的程度，反映其在供应链中的影响力和控制力。 | 中心度 = deg(v) / (/V/ - 1)，deg(v)为企业直接连接的节点总数。需先建供应链网络图。 |  |  |
| 53 | `M_ENT_PAINPOINT_GAP` | T3 | 与行业最佳差距 | MODEL | Q018 基线（2026-08-11 临时默认闭合）：沿用企业诊断 A3 的产业链分组与 P25/P75 基线，展示企业值与基线的原始差值，不设硬阈值。 | gap = enterprise_value - industry_baseline(P25/P75 by A3 chain group) |  |  |
| 54 | `M_ENT_PAINPOINT_SEVERITY` | T3 | 痛难点严重度 | MODEL | Q018 基线（2026-08-11 临时默认闭合）：仅作阅读优先级，不转企业得分/排名。降幅 >30%=高 / 10%~30%=中 / <10%=低。 | severity := high if drop>0.30 else medium if drop>=0.10 else low |  |  |
| 55 | `M_ENT_PATENT_GRANT_COUNT` | T3 | 专利授权量 | STAT | 报告期内企业作为第一专利权人获得授权的专利件数，含发明、实用新型、外观设计三类。 | 从dwd_patent_legal筛选status为授权，关联dwd_patent匹配企业名，COUNT(DISTINCT patent_id) |  |  |
| 56 | `M_ENT_PATENT_TOTAL` | T3 | 专利总量 | STAT | 全部企业专利授权数之和；对象范围 dwd.enterprise 全量，patent_grant_count 为 ODS 预聚合值，按企业求和。 | SUM(dwd.enterprise.patent_grant_count) |  |  |
| 57 | `M_ENT_POLICY_MATCH_SCORE` | T3 | 政策匹配度 | MODEL | pending_data_lead(Q015)：企业与政策导向的匹配程度评分；需跨政策域数据，权重与口径待确认。招引与培育共用。 | pending_algorithm（企业属性 vs 政策标签匹配评分） |  |  |
| 58 | `M_ENT_PROFIT_MARGIN` | T3 | 利润率 | MODEL | 企业净利润占营收比例；源年报净利润+营收可得，需算法计算比值。 | pending_algorithm（net_profit / operating_revenue * 100） |  |  |
| 59 | `M_ENT_RD_INVESTMENT_RATIO` | T3 | 研发投入占比 | STAT | 企业研发投入占营收比例；源字段可得，需算法计算比值并处理空值/异常。 | pending_algorithm（rd_investment / revenue_latest * 100） |  |  |
| 60 | `M_ENT_RECOMMEND_COUNT` | T3 | 推荐企业数 | MODEL | pending_data_lead(Q015)：推荐指数≥阈值的企业去重数；阈值待甲方确认，计数本身为直接聚合。 | COUNT(DISTINCT enterprise_id) WHERE 推荐指数 >= :threshold |  |  |
| 61 | `M_ENT_REGIONAL_COUNT` | T3 | 区域企业数量 | STAT | pending_data_lead(Q012)：行政区划下钻精度（到市/到区县）待甲方确认，临时默认到市级；按 headquarters_city + 经纬度归集去重计数。 | COUNT(DISTINCT enterprise_id) GROUP BY dwd.enterprise.headquarters_city |  |  |
| 62 | `M_ENT_REGIONAL_DENSITY` | T3 | 区域企业密度 | MODEL | pending_data_lead(Q012)：单位区域面积或单位 GDP 的企业数；区划精度待甲方确认。formula 待算法实现。 | pending_algorithm（区域企业数 / 区域面积 或 / 单位GDP） |  |  |
| 63 | `M_ENT_RELATION_STRENGTH` | T3 | 关系强度 | MODEL | Q017 基线（2026-08-11 临时默认闭合）：以投资金额分档代理关系强度——>1亿=强 / 1000万~1亿=中 / <1000万=弱；有 chain_score 时可作辅证。 | bucket(invest_amount): strong/>1e8/ mid/[1e7,1e8)/ weak/<1e7 |  |  |
| 64 | `M_ENT_RESEARCHER_COUNT` | T3 | 全球企业科研人数 | MODEL | 企业内科研人员数全球合计；无源时展示数据待接入，禁止用从业人数冒充。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 65 | `M_ENT_REVENUE_GROWTH_RATE` | T3 | 营收增长率 | STAT | 企业相邻年度营收同比增长率；源年报逐年数据可得，需算法计算（本年−上年）/上年。 | pending_algorithm（(本年 operating_revenue − 上年) / 上年 * 100） |  |  |
| 66 | `M_ENT_REVENUE_LATEST` | T3 | 营收 | MODEL | 企业最新年度营业收入。从dwd_org_annual_financial_info取最新year的operating_revenue。 | SELECT operating_revenue FROM dwd_org_annual_financial_info WHERE org_id=? ORDER BY yearTime DESC LIMIT 1 |  |  |
| 67 | `M_ENT_SHORTBOARD_COUNT` | T3 | 短板指标数 | STAT | 在企业综合竞争力评价指标体系中，企业表现低于预设基准（同行业平均值）的指标个数。 | 将各指标实际值与同行业平均值逐一比较，低于基准的指标计为短板并统计总数。 |  |  |
| 68 | `M_ENT_STAR_ENTERPRISE_COUNT` | T3 | 明星企业数 | MODEL | 重点/明星企业去重计数，供初始态推荐池。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 69 | `M_ENT_SUPPLIER_COUNT` | T3 | 供应商数量 | STAT | Q017 基线（2026-08-11）：目标企业直接一级上游供应商关系去重数；对象范围 dwd.enterprise_supply_chain，按 relation_type=上游 且 relation_level=1 计数。 | COUNT(DISTINCT related_enterprise_id) WHERE relation_type='上游' |  |  |
| 70 | `M_ENT_SZ_CHAIN_POSITION` | T3 | 链中角色 | MODEL | 企业在产业链中的角色（上/中/下游、链主等）；直接取 ODS 产业链归属字段。 | dwd.enterprise_industry.industry_chain_role |  |  |
| 71 | `M_ENT_SZ_COUNT` | T3 | 深圳企业数 | STAT | 总部在深圳且属目标产业链的企业去重数；按 headquarters_city=深圳 + 产业链筛选 COUNT。 | COUNT(DISTINCT enterprise_id) WHERE headquarters_city='深圳' AND 产业链 IN(:chain) |  |  |
| 72 | `M_ENT_TECH_RANK` | T3 | 技术力排名 | MODEL | 企业按技术力综合评分降序排名；依赖 M_ENT_TECH_POWER_SCORE，排名范围由筛选条件决定。 | pending_algorithm（RANK() OVER ORDER BY tech_score DESC） |  |  |
| 73 | `M_ENT_TOTAL_COUNT` | T3 | 企业总数 | STAT | 在选定的未来产业范围内，按企业统一社会信用代码去重的企业数量。 | COUNT(DISTINCT credit_code WHERE 属于目标未来产业)；从 dwd_org_industry_tags 按 industry_name 正则匹配归类。 |  |  |
| 74 | `M_ENT_TYPE_MATCH_COUNT` | T3 | 匹配企业总数 | STAT | 按所选产业 + 企业类型筛选后命中的企业去重总数；统计窗口最新批次，筛选条件由前端传入。 | COUNT(DISTINCT enterprise_id) WHERE 产业 IN(:industry) AND 类型 IN(:type) |  |  |
| 75 | `M_ENT_TYPE_RATIO` | T3 | 类型占比 | STAT | 各企业类型数量占匹配企业总数的百分比；依赖 M_ENT_TYPE_COUNT 与 M_ENT_TYPE_MATCH_COUNT，类型口径同 Q010。 | M_ENT_TYPE_COUNT / M_ENT_TYPE_MATCH_COUNT * 100 |  |  |
| 76 | `M_ENT_BASE_97_4` | TTEMP | 重点资讯统计 | STAT | 按月统计重点资讯数量及环比增长率。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 77 | `M_ENT_DEEP_142_1` | TTEMP | 企业发展历程模型 | MODEL | 企业发展历程模型：对应算法库 SRS ALGO-ENT-DEEP-142，按企业深度分析需规开展评分/识别/推荐。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 78 | `M_ENT_GRAPH_108_1` | TTEMP | 企业实体识别构建 | GRAPH | 企业实体识别构建：对应算法库 SRS ALGO-ENT-GRAPH-108，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 79 | `M_ENT_GRAPH_109_1` | TTEMP | 企业实体关系抽取 | GRAPH | 企业实体关系抽取：对应算法库 SRS ALGO-ENT-GRAPH-109，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
