# ALGO-LIB-SEED-TYPE-L01 · 签收草表（最新库 522 条）

> 基于 `acc16b1` 补库后的最新 seed（557 条 / in_seed 532 / 已回填 10 / 待签 522）。
> 供 `human:唐绍祖` 统签。**建议 type 仅供参考，请逐条或批量确认，签完我回填。**
> 回填规则：`API` → seed `third_party`；`D1` 保持 `draft`；`MODEL/GRAPH/MIXED` 的 steps 不回填。

## 统计

| 分组 | 建议依据 | 条数 |
|---|---|---|
| T2 赋号卡建议 | id-assign 赋号卡 suggested_unsigned | 156 |
| T-TEMP A1 已签沿用 | A1 表2 TEMP_ALGO → 正式号 已签 type | 90 |
| T3 机器初判 | 旧初判 0 + 新初判 276 | 276 |
| **合计待签** | | **522** |

## T2 · 赋号卡建议（156 条）

| # | metric_id | domain | 中文名 | 建议 type | 确认 type |
|---|---|---|---|---|---|
| 1 | `M_COMMON_INFO_TREND_QUERY` | COMMON | 查询结果·资讯传播趋势 | STAT |  |
| 2 | `M_ENT_CITY_COMPARE_TOPIC` | ENT | 多城市企业群对标值 | MIXED |  |
| 3 | `M_ENT_DOMAIN_DIST_TOPIC` | ENT | 企业领域分布 | STAT |  |
| 4 | `M_ENT_PAINPOINT_TOPIC` | ENT | 发展痛难点诊断 | MODEL |  |
| 5 | `M_ENT_REGIONAL_COUNT_TOPIC` | ENT | 区域企业数量规模占比 | STAT |  |
| 6 | `M_ENT_SUPPLY_STRUCT_TOPIC` | ENT | 供应链结构指标 | GRAPH |  |
| 7 | `M_ENT_SZ_LIST_TOPIC` | ENT | 深圳企业清单与链中角色 | STAT |  |
| 8 | `M_ENT_TYPE_DIST_TOPIC` | ENT | 重点企业类型分布 | STAT |  |
| 9 | `M_INNOV_ACHIEVE_VALUE` | INNOV | 创新价值 | MODEL |  |
| 10 | `M_INNOV_CARRIER_INDEX_GLOBAL` | INNOV | 创新载体创新能力指数 | MODEL |  |
| 11 | `M_INNOV_CARRIER_RANK_GLOBAL` | INNOV | 创新载体多维度排名 | MIXED |  |
| 12 | `M_INNOV_CARRIER_VALUE_RANK_SZ` | INNOV | 深圳创新载体创新价值排名 | MODEL |  |
| 13 | `M_INNOV_CITY_BENCHMARK_GLOBAL` | INNOV | 城市对标分析 | MIXED |  |
| 14 | `M_INNOV_CITY_COMPARE_SZ` | INNOV | 深圳科技发展指标对比 | MIXED |  |
| 15 | `M_INNOV_CITY_COMPETE_SZ` | INNOV | 深圳科技竞争力 | MIXED |  |
| 16 | `M_INNOV_CITY_FACTOR_GLOBAL` | INNOV | 城市创新能力要素表现 | MIXED |  |
| 17 | `M_INNOV_CITY_INDEX_SZ` | INNOV | 深圳创新能力指数 | MIXED |  |
| 18 | `M_INNOV_CITY_MONITOR_GLOBAL` | INNOV | 城市创新数据监控 | STAT |  |
| 19 | `M_INNOV_CITY_RANK_GLOBAL` | INNOV | 城市创新能力排名 | MIXED |  |
| 20 | `M_INNOV_CITY_RANK_SZ` | INNOV | 深圳城市科技发展排名 | MIXED |  |
| 21 | `M_INNOV_CITY_TALENT_INDEX_GLOBAL` | INNOV | 人才创新指数 | third_party |  |
| 22 | `M_INNOV_CITY_TALENT_INDEX_SZ` | INNOV | 深圳重点人才指数 | third_party |  |
| 23 | `M_INNOV_CITY_TREND_SZ` | INNOV | 深圳与对标城市趋势 | MIXED |  |
| 24 | `M_INNOV_CONFERENCE_INFLUENCE` | INNOV | 会议影响力 | MODEL |  |
| 25 | `M_INNOV_DOMAIN_KPI_SZ` | INNOV | 深圳科技领域明细指标 | STAT |  |
| 26 | `M_INNOV_ENTERPRISE_INFLUENCE` | INNOV | 企业影响力 | MODEL |  |
| 27 | `M_INNOV_EVENT_ATTENTION` | INNOV | 事件关注度 | MODEL |  |
| 28 | `M_INNOV_EVENT_IMPORTANCE` | INNOV | 事件重要性等级 | MODEL |  |
| 29 | `M_INNOV_EVENT_INFLUENCE` | INNOV | 事件影响力 | MODEL |  |
| 30 | `M_INNOV_EXPERT_ACTIVITY` | INNOV | 专家科研活跃度 | third_party |  |
| 31 | `M_INNOV_EXPERT_HINDEX` | INNOV | 专家H指数排行 | third_party |  |
| 32 | `M_INNOV_FACTOR_ANOMALY` | INNOV | 监测异常点识别 | MODEL |  |
| 33 | `M_INNOV_FACTOR_CLUSTER` | INNOV | 要素聚类 | MODEL |  |
| 34 | `M_INNOV_FACTOR_COUNT` | INNOV | 科创要素数量统计 | STAT |  |
| 35 | `M_INNOV_FACTOR_DIST` | INNOV | 科创要素分布比例 | STAT |  |
| 36 | `M_INNOV_FACTOR_EDGE_WEIGHT` | INNOV | 要素间影响程度 | GRAPH |  |
| 37 | `M_INNOV_FACTOR_FORECAST` | INNOV | 监测趋势预测 | MODEL |  |
| 38 | `M_INNOV_FACTOR_GROWTH` | INNOV | 科创要素增长趋势 | STAT |  |
| 39 | `M_INNOV_FACTOR_RELATION` | INNOV | 要素关联关系 | GRAPH |  |
| 40 | `M_INNOV_GBA_CAPACITY_INDEX` | INNOV | 粤港澳大湾区创新能力指标 | MODEL |  |
| 41 | `M_INNOV_GBA_ENV_INDEX` | INNOV | 创新环境指数 | MODEL |  |
| 42 | `M_INNOV_GBA_FACTOR_STAT` | INNOV | 湾区创新能力因素统计 | STAT |  |
| 43 | `M_INNOV_GBA_HOTSPOT` | INNOV | 湾区创新热点区域 | MODEL |  |
| 44 | `M_INNOV_GBA_INNOV_RATIO` | INNOV | 创新比例 | STAT |  |
| 45 | `M_INNOV_GBA_INVEST` | INNOV | 创新投入 | STAT |  |
| 46 | `M_INNOV_GBA_MECH_INDEX` | INNOV | 创新机制指数 | MODEL |  |
| 47 | `M_INNOV_GBA_ORG_INDEX` | INNOV | 创新机构指数 | MODEL |  |
| 48 | `M_INNOV_GBA_OUTPUT_VALUE` | INNOV | 创新产值 | STAT |  |
| 49 | `M_INNOV_GBA_PATENT_GRANT` | INNOV | 专利授权量 | STAT |  |
| 50 | `M_INNOV_GBA_PATENT_PAPER` | INNOV | 专利及论文数量 | STAT |  |
| 51 | `M_INNOV_GBA_RES_INDEX` | INNOV | 创新资源指数 | MODEL |  |
| 52 | `M_INNOV_GBA_SUBINDEX_CONTRIB` | INNOV | 子指标贡献度 | MODEL |  |
| 53 | `M_INNOV_GBA_SWOT_OPPORTUNITY` | INNOV | 湾区创新能力机会因素 | MODEL |  |
| 54 | `M_INNOV_GBA_SWOT_STRENGTH` | INNOV | 湾区创新能力优势因素 | MODEL |  |
| 55 | `M_INNOV_GBA_SWOT_THREAT` | INNOV | 湾区创新能力威胁因素 | MODEL |  |
| 56 | `M_INNOV_GBA_SWOT_WEAKNESS` | INNOV | 湾区创新能力短板因素 | MODEL |  |
| 57 | `M_INNOV_GBA_TECH_CONTRACT` | INNOV | 创新技术合同交易额 | STAT |  |
| 58 | `M_INNOV_IMPACT_FORECAST` | INNOV | 创新影响预测 | MODEL |  |
| 59 | `M_INNOV_IMPACT_SCORE` | INNOV | 创新影响分数 | MODEL |  |
| 60 | `M_INNOV_JOURNAL_INFLUENCE` | INNOV | 期刊影响力 | MODEL |  |
| 61 | `M_INNOV_KEYD_COMPETITIVENESS` | INNOV | 区域科技创新竞争力水平 | MIXED |  |
| 62 | `M_INNOV_KEYD_LAND` | INNOV | 土地创新产出效益与利用效率 | STAT |  |
| 63 | `M_INNOV_KEYD_POTENTIAL` | INNOV | 区域科技创新发展潜力 | MIXED |  |
| 64 | `M_INNOV_KEYD_SPATIAL` | INNOV | 空间密度与集聚度 | STAT |  |
| 65 | `M_INNOV_KPI_BOARD` | INNOV | 全球创新实时看板指标 | STAT |  |
| 66 | `M_INNOV_KPI_BOARD_SZ` | INNOV | 深圳科技发展指标看板 | STAT |  |
| 67 | `M_INNOV_ORG_INFLUENCE` | INNOV | 科研机构影响力 | MODEL |  |
| 68 | `M_INNOV_PAPER_INFLUENCE` | INNOV | 论文影响力 | STAT |  |
| 69 | `M_INNOV_PATENT_INFLUENCE` | INNOV | 专利影响力 | MODEL |  |
| 70 | `M_INNOV_PG_COMPOSITE` | INNOV | 政策与条件保障力综合评估 | MODEL |  |
| 71 | `M_INNOV_PG_COUNT_DIST` | INNOV | 政策数量类型与覆盖分布 | STAT |  |
| 72 | `M_INNOV_PG_EFFECT` | INNOV | 政策实施效果 | MIXED |  |
| 73 | `M_INNOV_PG_FUND` | INNOV | 经费支持 | STAT |  |
| 74 | `M_INNOV_PG_GUIDE` | INNOV | 发展战略引导力 | MODEL |  |
| 75 | `M_INNOV_PG_INTENSITY` | INNOV | 政策扶持力度 | MIXED |  |
| 76 | `M_INNOV_PG_PROJECT` | INNOV | 项目支持 | STAT |  |
| 77 | `M_INNOV_PLAN_DIRECTION_ALERT` | INNOV | 潜在科技发展方向预警 | MODEL |  |
| 78 | `M_INNOV_PLAN_GROWTH` | INNOV | 增长速度 | MIXED |  |
| 79 | `M_INNOV_PLAN_HEAT` | INNOV | 热度指数 | MIXED |  |
| 80 | `M_INNOV_PLAN_LOCAL_ADV` | INNOV | 本地科技创新特色与优势 | MODEL |  |
| 81 | `M_INNOV_PLAN_TALENT_FLOW` | INNOV | 科技人才流动（产业界↔学术界） | MODEL |  |
| 82 | `M_INNOV_POINT_DISCOVERY` | INNOV | 创新点发现 | MODEL |  |
| 83 | `M_INNOV_POINT_VALUE` | INNOV | 创新点价值评估 | MODEL |  |
| 84 | `M_INNOV_POT_COMPOSITE` | INNOV | 产业发展潜力综合评估 | MODEL |  |
| 85 | `M_INNOV_POT_INPUT` | INNOV | 产业投入 | STAT |  |
| 86 | `M_INNOV_POT_MATURITY` | INNOV | 技术产品成熟度 | MODEL |  |
| 87 | `M_INNOV_POT_OUTPUT` | INNOV | 产业产值 | STAT |  |
| 88 | `M_INNOV_POT_SCI_INFL` | INNOV | 产业科学影响力 | MODEL |  |
| 89 | `M_INNOV_POT_TECH_INFL` | INNOV | 产业技术影响力 | MODEL |  |
| 90 | `M_INNOV_PROJECT_INFLUENCE` | INNOV | 项目（含课题）影响力 | MODEL |  |
| 91 | `M_INNOV_RES_CI_COMPARE` | INNOV | 多企业竞争情报比对 | MIXED |  |
| 92 | `M_INNOV_RES_CI_LEVEL` | INNOV | 竞争情报等级 | MODEL |  |
| 93 | `M_INNOV_RES_GRADE` | INNOV | 研究领域等级划分 | MODEL |  |
| 94 | `M_INNOV_RES_OVERLAP` | INNOV | 研究领域重叠度 | MODEL |  |
| 95 | `M_INNOV_SCHOLAR_INFLUENCE` | INNOV | 专家学者影响力 | MODEL |  |
| 96 | `M_INNOV_SCI_CENTRALITY` | INNOV | 科学网络中心性 | MIXED |  |
| 97 | `M_INNOV_SCI_FORECAST` | INNOV | 科学创造力趋势预测 | MODEL |  |
| 98 | `M_INNOV_SCI_FRONTIER` | INNOV | 科学研究前沿性 | MODEL |  |
| 99 | `M_INNOV_SCI_PAPER` | INNOV | 科学论文数量 | STAT |  |
| 100 | `M_INNOV_SCIINDEX_INFLUENCE` | INNOV | 科技影响力趋势 | STAT |  |
| 101 | `M_INNOV_SCIINDEX_RANK_SCORE` | INNOV | 科技成果综合得分与名次 | STAT |  |
| 102 | `M_INNOV_SCIINDEX_VALUE` | INNOV | 科技指数值（含区域分布读数） | STAT |  |
| 103 | `M_INNOV_TINN_COMPOSITE` | INNOV | 技术创新力综合评估 | MODEL |  |
| 104 | `M_INNOV_TINN_FORECAST` | INNOV | 技术创新趋势预测 | MODEL |  |
| 105 | `M_INNOV_TINN_MARKET` | INNOV | 技术市场潜力 | MODEL |  |
| 106 | `M_INNOV_TINN_PATENT_COUNT` | INNOV | 专利数量 | STAT |  |
| 107 | `M_INNOV_TINN_PATENT_QUALITY` | INNOV | 专利质量 | MODEL |  |
| 108 | `M_ORG_ATTENTION_TREND` | ORG | 科研关注度 | COMPUTE |  |
| 109 | `M_ORG_ATTRACT_SCORE` | ORG | 科研机构招引推荐指数 | MODEL |  |
| 110 | `M_ORG_COLLAB_CHAIN` | ORG | 科研合作关系链条 | GRAPH |  |
| 111 | `M_ORG_CULTIVATE_SCORE` | ORG | 科研机构扶持推荐指数 | MODEL |  |
| 112 | `M_ORG_INDUSTRY_COVER` | ORG | 科研机构产业领域覆盖 | STAT |  |
| 113 | `M_ORG_NEW_TREND` | ORG | 新增科研机构趋势 | STAT |  |
| 114 | `M_ORG_PERF_QUERY` | ORG | 查询结果·科研机构绩效 | STAT |  |
| 115 | `M_ORG_SZ_ADVANTAGE` | ORG | 深圳科研机构优势 | MODEL |  |
| 116 | `M_ORG_SZ_PAINPOINT` | ORG | 深圳科研机构痛难点 | MODEL |  |
| 117 | `M_ORG_SZ_STATUS` | ORG | 深圳科研机构现状解读 | MIXED |  |
| 118 | `M_ORG_TECH_LAYOUT` | ORG | 科研机构技术领域布局 | STAT |  |
| 119 | `M_ORG_TECH_SCORE` | ORG | 科研机构技术力评价与对比 | MODEL |  |
| 120 | `M_SVC_ORG_TECH_SCORE` | SVC | 服务机构影响力 | MODEL |  |
| 121 | `M_SVC_TYPE_DIST_QUERY` | SVC | 查询结果·服务类型分布 | STAT |  |
| 122 | `M_TALENT_ACADEMIC_SCORE` | TALENT | 人才学术力指数 | MODEL |  |
| 123 | `M_TALENT_ATTRACT_SCORE` | TALENT | 引入人才推荐指数 | MODEL |  |
| 124 | `M_TALENT_CULTIVATE_SCORE` | TALENT | 培育人才推荐指数 | MODEL |  |
| 125 | `M_TALENT_FLOW_TRACK` | TALENT | 人才流动追踪 | GRAPH |  |
| 126 | `M_TALENT_INDUSTRY_SCORE` | TALENT | 人才产业力指数 | MODEL |  |
| 127 | `M_TALENT_ORG_DIST` | TALENT | 重点人才机构分布 | STAT |  |
| 128 | `M_TALENT_REGIONAL_DIST` | TALENT | 重点人才区域分布 | STAT |  |
| 129 | `M_TALENT_RELATION_NET` | TALENT | 重点人才关系链结构 | GRAPH |  |
| 130 | `M_TALENT_STRUCT_QUERY` | TALENT | 查询结果·人才结构 | STAT |  |
| 131 | `M_TALENT_SUPPLY_STRUCT` | TALENT | 人才供给情况 | STAT |  |
| 132 | `M_TALENT_SZ_STATUS` | TALENT | 深圳人才现状与优劣势 | MIXED |  |
| 133 | `M_TALENT_SZ_SUPPLY_DEMAND` | TALENT | 深圳人才供需评价 | MODEL |  |
| 134 | `M_TALENT_UNIV_NEW` | TALENT | 高校新培育人才 | MODEL |  |
| 135 | `M_TECH_COMPOSITE_SCORE` | TECH | 评估综合得分 | COMPUTE |  |
| 136 | `M_TECH_CONVERT_BOTTLENECK` | TECH | 技术转化瓶颈识别 | third_party |  |
| 137 | `M_TECH_EDGE_STRENGTH` | TECH | 技术–技术关联强度 | GRAPH |  |
| 138 | `M_TECH_ENTITY_INFLUENCE` | TECH | 技术点影响力 / 实体优先级 | MODEL |  |
| 139 | `M_TECH_ENTITY_REL` | TECH | 实体关联关系网 | GRAPH |  |
| 140 | `M_TECH_ENTITY_TOP5` | TECH | 根节点 Top5 关键实体与关联强度 | GRAPH |  |
| 141 | `M_TECH_GRAPH_STRUCT` | TECH | 技术点网图结构 | GRAPH |  |
| 142 | `M_TECH_HEAT_INDEX` | TECH | 技术热点热度指数 | third_party |  |
| 143 | `M_TECH_HEAT_QUERY` | TECH | 查询结果·技术热度 | STAT |  |
| 144 | `M_TECH_INVEST_AMOUNT` | TECH | 技术投资额 | STAT |  |
| 145 | `M_TECH_LIFE_STAGE` | TECH | 技术发展阶段 | MODEL |  |
| 146 | `M_TECH_MATURITY_LEVEL` | TECH | 技术成熟度 | MODEL |  |
| 147 | `M_TECH_OUTPUT_SCALE` | TECH | 技术规模 | STAT |  |
| 148 | `M_TECH_PAPER_PATENT_CNT` | TECH | 技术点论文量 / 专利量 | STAT |  |
| 149 | `M_TECH_PATH_CENTRALITY` | TECH | 中心度 | GRAPH |  |
| 150 | `M_TECH_PATH_KEYNODE` | TECH | 关键节点重要性 | GRAPH |  |
| 151 | `M_TECH_PATH_PRIORITY` | TECH | 节点优先级 / 重要度 | GRAPH |  |
| 152 | `M_TECH_POTENTIAL_SCORE` | TECH | 技术产业化潜力评分 | third_party |  |
| 153 | `M_TECH_REL_STRENGTH` | TECH | 技术关联强度 | GRAPH |  |
| 154 | `M_TECH_STAGE_JUDGE` | TECH | 技术阶段判定 | third_party |  |
| 155 | `M_TECH_SZ_ASSESS` | TECH | 深圳技术潜力与阶段综合评估 | third_party |  |
| 156 | `M_TECH_TOPIC_HEAT` | TECH | 技术话题热度 | MODEL |  |

## T-TEMP · A1 已签 type 沿用（90 条）

| # | metric_id | domain | 中文名 | 建议 type | 确认 type |
|---|---|---|---|---|---|
| 1 | `M_CHAIN_BASE_95_1` | CHAIN | 产业链基础指标模型构建 | STAT |  |
| 2 | `M_CHAIN_DEEP_117_1` | CHAIN | 产业链全景模型构建 | MODEL |  |
| 3 | `M_CHAIN_DEEP_118_1` | CHAIN | 深圳产业链模型构建 | MODEL |  |
| 4 | `M_CHAIN_DEEP_119_1` | CHAIN | 产业发展路线历程模型 | MODEL |  |
| 5 | `M_CHAIN_DEEP_120_1` | CHAIN | 产业热点领域识别模型 | MODEL |  |
| 6 | `M_CHAIN_DEEP_121_1` | CHAIN | 深圳产业优势识别模型 | MODEL |  |
| 7 | `M_CHAIN_DEEP_122_1` | CHAIN | 产业周期分析模型 | MODEL |  |
| 8 | `M_CHAIN_DEEP_123_1` | CHAIN | 产业阶段分析模型 | MODEL |  |
| 9 | `M_CHAIN_DEEP_124_1` | CHAIN | 产业链关键环节识别模型 | MODEL |  |
| 10 | `M_CHAIN_DEEP_125_1` | CHAIN | 产业瓶颈堵点识别模型 | MODEL |  |
| 11 | `M_CHAIN_DEEP_126_1` | CHAIN | 区域产业指数模型 | MODEL |  |
| 12 | `M_CHAIN_DEEP_127_1` | CHAIN | 深圳问题识别模型 | MODEL |  |
| 13 | `M_CHAIN_DEEP_128_1` | CHAIN | 深圳机遇分析模型 | MODEL |  |
| 14 | `M_CHAIN_DEEP_129_1` | CHAIN | 重点布局产业推荐模型 | MODEL |  |
| 15 | `M_CHAIN_GRAPH_102_1` | CHAIN | 产业实体识别构建 | GRAPH |  |
| 16 | `M_CHAIN_GRAPH_103_1` | CHAIN | 产业实体关系抽取 | GRAPH |  |
| 17 | `M_ENT_BASE_97_4` | ENT | 重点资讯统计 | STAT |  |
| 18 | `M_ENT_DEEP_142_1` | ENT | 企业发展历程模型 | MODEL |  |
| 19 | `M_ENT_GRAPH_108_1` | ENT | 企业实体识别构建 | GRAPH |  |
| 20 | `M_ENT_GRAPH_109_1` | ENT | 企业实体关系抽取 | GRAPH |  |
| 21 | `M_ORG_BASE_99_1` | ORG | 科研机构基础指标模型构建 | third_party |  |
| 22 | `M_ORG_DEEP_149_1` | ORG | 科研机构重点技术领域布局模型 | third_party |  |
| 23 | `M_ORG_DEEP_150_1` | ORG | 科研机构发展历程模型 | third_party |  |
| 24 | `M_ORG_DEEP_151_1` | ORG | 深圳科研机构优势分析模型 | third_party |  |
| 25 | `M_ORG_DEEP_152_1` | ORG | 深圳科研机构痛难点识别模型 | third_party |  |
| 26 | `M_ORG_DEEP_153_1` | ORG | 科研合作关系链条模型 | third_party |  |
| 27 | `M_ORG_DEEP_154_1` | ORG | 科研机构引入推荐模型 | third_party |  |
| 28 | `M_ORG_DEEP_155_1` | ORG | 科研机构扶持推荐模型 | third_party |  |
| 29 | `M_ORG_GRAPH_114_1` | ORG | 科研机构实体识别构建 | third_party |  |
| 30 | `M_ORG_GRAPH_115_1` | ORG | 科研机构实体关系抽取 | third_party |  |
| 31 | `M_POLICY_BASE_100_1` | POLICY | 政策基础指标模型构建 | STAT |  |
| 32 | `M_POLICY_DEEP_166_1` | POLICY | 政策焦点识别模型 | MODEL |  |
| 33 | `M_POLICY_DEEP_167_1` | POLICY | 政策力度评估模型 | MODEL |  |
| 34 | `M_POLICY_DEEP_168_1` | POLICY | 政策效果评估模型 | MODEL |  |
| 35 | `M_POLICY_DEEP_169_1` | POLICY | 政策短板识别模型 | MODEL |  |
| 36 | `M_POLICY_DEEP_170_1` | POLICY | 政策机遇识别模型 | MODEL |  |
| 37 | `M_POLICY_DEEP_171_1` | POLICY | 政策布局推荐模型 | MODEL |  |
| 38 | `M_POLICY_GRAPH_106_1` | POLICY | 政策实体识别构建 | GRAPH |  |
| 39 | `M_POLICY_GRAPH_107_1` | POLICY | 政策实体关系抽取 | GRAPH |  |
| 40 | `M_SVC_BASE_101_1` | SVC | 服务机构基础指标模型构建 | STAT |  |
| 41 | `M_SVC_DEEP_172_1` | SVC | 服务链短板分析模型 | MODEL |  |
| 42 | `M_SVC_DEEP_173_1` | SVC | 服务关系链模型 | MODEL |  |
| 43 | `M_SVC_DEEP_174_1` | SVC | 金融服务机构技术力评价模型 | MODEL |  |
| 44 | `M_SVC_DEEP_175_1` | SVC | 知识产权服务机构技术力评价模型 | MODEL |  |
| 45 | `M_SVC_DEEP_176_1` | SVC | 人力资源服务机构技术力评价模型 | MODEL |  |
| 46 | `M_SVC_DEEP_177_1` | SVC | 市场营销服务机构技术力评价模型 | MODEL |  |
| 47 | `M_SVC_DEEP_178_1` | SVC | 咨询服务机构技术力评价模型 | MODEL |  |
| 48 | `M_SVC_DEEP_179_1` | SVC | 科技创新服务机构技术力评价模型 | MODEL |  |
| 49 | `M_SVC_DEEP_180_1` | SVC | 服务机构引入推荐模型 | MODEL |  |
| 50 | `M_SVC_DEEP_181_1` | SVC | 服务机构培育推荐模型 | MODEL |  |
| 51 | `M_SVC_GRAPH_112_1` | SVC | 服务机构实体识别构建 | GRAPH |  |
| 52 | `M_SVC_GRAPH_113_1` | SVC | 服务机构实体关系抽取 | GRAPH |  |
| 53 | `M_SYNTH_182_1` | SYNTH | 区域科技创新成果综合评价模型 | MIXED |  |
| 54 | `M_SYNTH_183_1` | SYNTH | 区域产业创新成果综合评价模型 | MIXED |  |
| 55 | `M_SYNTH_184_1` | SYNTH | 区域产业创新人才综合评价模型 | MIXED |  |
| 56 | `M_SYNTH_185_1` | SYNTH | 区域产业创新政策综合评价模型 | MIXED |  |
| 57 | `M_SYNTH_186_1` | SYNTH | 区域创新活力综合分析模型 | MIXED |  |
| 58 | `M_SYNTH_187_1` | SYNTH | 区域创新要素类型综合评价模型 | MIXED |  |
| 59 | `M_SYNTH_188_1` | SYNTH | 区域创新要素层次综合评价模型 | MIXED |  |
| 60 | `M_SYNTH_189_1` | SYNTH | 区域创新要素领域综合评价模型 | MIXED |  |
| 61 | `M_SYNTH_190_1` | SYNTH | 区域创新要素综合分析模型 | MIXED |  |
| 62 | `M_SYNTH_191_1` | SYNTH | 区域创新协同分析模型 | MIXED |  |
| 63 | `M_SYNTH_GRAPHAPI_116_1` | SYNTH | 产业全要素图谱API服务开发 | third_party |  |
| 64 | `M_TALENT_BASE_98_1` | TALENT | 人才基础指标模型构建 | third_party |  |
| 65 | `M_TALENT_DEEP_156_1` | TALENT | 重点人才识别模型 | third_party |  |
| 66 | `M_TALENT_DEEP_157_1` | TALENT | 人才流动追踪模型 | third_party |  |
| 67 | `M_TALENT_DEEP_158_1` | TALENT | 高校学院新培育人才模型 | third_party |  |
| 68 | `M_TALENT_DEEP_159_1` | TALENT | 深圳重点人才优势和短板分析模型 | third_party |  |
| 69 | `M_TALENT_DEEP_160_1` | TALENT | 人才关系链模型 | third_party |  |
| 70 | `M_TALENT_DEEP_161_1` | TALENT | 人才供需分析评价模型 | third_party |  |
| 71 | `M_TALENT_DEEP_162_1` | TALENT | 人才学术力评估模型 | third_party |  |
| 72 | `M_TALENT_DEEP_163_1` | TALENT | 人才产业力评估模型 | third_party |  |
| 73 | `M_TALENT_DEEP_164_1` | TALENT | 招入人才推荐模型 | third_party |  |
| 74 | `M_TALENT_DEEP_165_1` | TALENT | 培育人才布局模型 | third_party |  |
| 75 | `M_TALENT_GRAPH_110_1` | TALENT | 人才实体识别构建 | third_party |  |
| 76 | `M_TALENT_GRAPH_111_1` | TALENT | 人才实体关系抽取 | third_party |  |
| 77 | `M_TECH_BASE_96_1` | TECH | 技术基础指标模型构建 | third_party |  |
| 78 | `M_TECH_DEEP_130_1` | TECH | 全景技术链模型 | third_party |  |
| 79 | `M_TECH_DEEP_131_1` | TECH | 深圳技术链模型 | third_party |  |
| 80 | `M_TECH_DEEP_132_1` | TECH | 技术发展历程模型 | third_party |  |
| 81 | `M_TECH_DEEP_133_1` | TECH | 深圳细分领域分布模型 | third_party |  |
| 82 | `M_TECH_DEEP_134_1` | TECH | 技术前沿热点领域识别模型 | third_party |  |
| 83 | `M_TECH_DEEP_135_1` | TECH | 技术产业化潜力识别模型 | third_party |  |
| 84 | `M_TECH_DEEP_136_1` | TECH | 技术转化瓶颈堵点原因识别模型 | third_party |  |
| 85 | `M_TECH_DEEP_137_1` | TECH | 技术阶段分析模型 | third_party |  |
| 86 | `M_TECH_DEEP_138_1` | TECH | 深圳技术发展问题识别模型 | third_party |  |
| 87 | `M_TECH_DEEP_139_1` | TECH | 深圳技术发展机遇识别模型 | third_party |  |
| 88 | `M_TECH_DEEP_140_1` | TECH | 深圳技术发展重点布局领域推荐模型 | third_party |  |
| 89 | `M_TECH_GRAPH_104_1` | TECH | 技术实体识别构建 | third_party |  |
| 90 | `M_TECH_GRAPH_105_1` | TECH | 技术实体关系抽取 | third_party |  |

## T3 · 机器初判（276 条）

| # | metric_id | domain | 中文名 | formula(截断) | 建议 type | 确认 type |
|---|---|---|---|---|---|---|
| 1 | `M_CHAIN_ACADEMIC_COOP_SCORE` | CHAIN | 产学研合作强度 | pending_algorithm（联合专利数*w1+联合项目数*w2+人才流动*w3） | MODEL |  |
| 2 | `M_CHAIN_ACADEMIC_POWER` | CHAIN | 科研实力指数 | pending_algorithm（专利密度*w1 + 论文密度*w2 + 高校数量*w3） | MODEL |  |
| 3 | `M_CHAIN_BOTTLENECK_COUNT` | CHAIN | 瓶颈堵点数 | COUNT(DISTINCT id) FROM dwd.industry_bottleneck | STAT |  |
| 4 | `M_CHAIN_BOTTLENECK_SEVERITY` | CHAIN | 瓶颈严重度 | pending_algorithm（MAX(severity_score) FROM dwd.industry_bott | MODEL |  |
| 5 | `M_CHAIN_BOTTLENECK_TYPE_DIST` | CHAIN | 瓶颈类型分布 | COUNT(*) GROUP BY bottleneck_type FROM dwd.industry_bottlene | STAT |  |
| 6 | `M_CHAIN_BREAK_RISK_COUNT` | CHAIN | 产业链断链风险数 | pending_algorithm（供应链节点中心性+替代性+地域集中度综合判定） | GRAPH |  |
| 7 | `M_CHAIN_CHOKE_LINK_COUNT` | CHAIN | 卡脖子环节数 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 8 | `M_CHAIN_COMPETITIVENESS_INDEX` | CHAIN | 区域竞争力指数 | pending_algorithm（M_CHAIN_REGION_INDEX + 排名归一化 + 趋势因子） | MODEL |  |
| 9 | `M_CHAIN_COMPLETENESS_SCORE` | CHAIN | 产业链完整度评分 | pending_algorithm（覆盖环节数/全链环节数*100 * 企业分布均匀度修正因子） | MODEL |  |
| 10 | `M_CHAIN_CONCENTRATION_INDEX` | CHAIN | 产业集中度 | pending_algorithm（HHI = SUM(企业市场份额^2) 或 CR_N = TopN企业市场份额之和） | STAT |  |
| 11 | `M_CHAIN_CYCLE_STAGE` | CHAIN | 周期阶段 | pending_algorithm（基于企业增速/专利增速/投融资趋势/市场集中度的周期判定模型 CHAIN_CYCLE | MODEL |  |
| 12 | `M_CHAIN_DEVELOPMENT_MILESTONE_COUNT` | CHAIN | 发展里程碑数 | pending_algorithm（基于 dwd.industry_chain_news + 政策事件 NLP 提取里程 | MODEL |  |
| 13 | `M_CHAIN_DOWNSTREAM_COUNT` | CHAIN | 下游环节数 | COUNT(DISTINCT node_name) WHERE chain_stage='downstream' | GRAPH |  |
| 14 | `M_CHAIN_EDGE_COUNT` | CHAIN | 产业链边数 | pending_algorithm（NebulaGraph gkx_chain 边统计） | GRAPH |  |
| 15 | `M_CHAIN_ENTERPRISE_COUNT` | CHAIN | 产业链关联企业数 | COUNT(DISTINCT dwd.industry_chain_enterprise.enterprise_code | STAT |  |
| 16 | `M_CHAIN_ENTERPRISE_NEW_COUNT` | CHAIN | 新增关联企业数 | COUNT(DISTINCT enterprise_code) GROUP BY YEAR(首次关联时间) | STAT |  |
| 17 | `M_CHAIN_ENTERPRISE_POWER` | CHAIN | 企业实力指数 | pending_algorithm（AVG(chain_score) * 企业规模/资质加权因子） | MODEL |  |
| 18 | `M_CHAIN_GLOBAL_CASE_MATCH` | CHAIN | 全球成功案例匹配 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 19 | `M_CHAIN_GLOBAL_REGION_COUNT` | CHAIN | 全球分布区域数 | COUNT(DISTINCT region_code) WHERE scope='global' | STAT |  |
| 20 | `M_CHAIN_HIGH_VALUE_RATIO` | CHAIN | 高价值环节占比 | pending_algorithm（高价值环节数 / 全部环节数 * 100） | STAT |  |
| 21 | `M_CHAIN_HOT_NEWS_COUNT` | CHAIN | 热门资讯数 | COUNT(DISTINCT news_id) WHERE heat_score >= 80 | MODEL |  |
| 22 | `M_CHAIN_HOTSPOT_COUNT` | CHAIN | 热点领域数 | pending_algorithm（企业增速*w1+投融资热度*w2+专利密度*w3 >= 阈值） | MODEL |  |
| 23 | `M_CHAIN_HOTSPOT_SCORE` | CHAIN | 热点评分 | pending_algorithm（企业增速*w1+投融资热度*w2+专利密度*w3+资讯热度*w4） | MODEL |  |
| 24 | `M_CHAIN_INSTITUTION_COUNT` | CHAIN | 产业链关联机构数 | COUNT(DISTINCT enterprise_name) WHERE org_type='机构' | STAT |  |
| 25 | `M_CHAIN_INTERNATIONALIZATION_INDEX` | CHAIN | 产业链国际化程度 | pending_algorithm（海外企业占比*w1+海外专利占比*w2+进出口数据*w3） | STAT |  |
| 26 | `M_CHAIN_INVEST_COUNT` | CHAIN | 投融资事件数 | COUNT(DISTINCT news_id) WHERE news_type='financing' | STAT |  |
| 27 | `M_CHAIN_INVEST_TOTAL` | CHAIN | 投融资总额 | pending_algorithm（NLP抽取融资金额 / 采购数据聚合） | MODEL |  |
| 28 | `M_CHAIN_KEY_NODE_COUNT` | CHAIN | 关键环节数 | COUNT(DISTINCT node_name) WHERE is_key_node=1 | GRAPH |  |
| 29 | `M_CHAIN_LAYOUT_PRIORITY_SCORE` | CHAIN | 布局优先级评分 | pending_algorithm（战略重要性*w1+深圳缺口*w2+市场前景*w3+技术可行*w4） | MODEL |  |
| 30 | `M_CHAIN_LAYOUT_RECOMMEND_COUNT` | CHAIN | 重点布局推荐数 | COUNT(DISTINCT chain_id) WHERE 布局优先级评分 >= 阈值 | MODEL |  |
| 31 | `M_CHAIN_LINK_HEALTH` | CHAIN | 环节健康度 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 32 | `M_CHAIN_MARKET_GROWTH` | CHAIN | 市场增长率 | (M_CHAIN_MARKET_SIZE(y)-M_CHAIN_MARKET_SIZE(y-1))/NULLIF(M_C | STAT |  |
| 33 | `M_CHAIN_MARKET_SIZE` | CHAIN | 市场规模 | SUM(ent_annual_revenue) WHERE enterprise_code IN (SELECT ent | STAT |  |
| 34 | `M_CHAIN_MIDSTREAM_COUNT` | CHAIN | 中游环节数 | COUNT(DISTINCT node_name) WHERE chain_stage='midstream' | GRAPH |  |
| 35 | `M_CHAIN_NATIONAL_REGION_COUNT` | CHAIN | 全国分布区域数 | COUNT(DISTINCT headquarters_city) WHERE scope='national' | STAT |  |
| 36 | `M_CHAIN_NEWS_COUNT` | CHAIN | 动态资讯数 | COUNT(DISTINCT dwd.industry_chain_news.news_id) | STAT |  |
| 37 | `M_CHAIN_NEWS_SENTIMENT_RATIO` | CHAIN | 资讯正面情感占比 | pending_algorithm（COUNT(sentiment='positive') / COUNT(*) * 1 | STAT |  |
| 38 | `M_CHAIN_NODE_COUNT` | CHAIN | 产业链节点数 | pending_algorithm（NebulaGraph gkx_chain LOOKUP COUNT） | GRAPH |  |
| 39 | `M_CHAIN_PATENT_COUNT` | CHAIN | 产业链关联专利数 | COUNT(DISTINCT dwd.industry_chain_patent.patent_id) | STAT |  |
| 40 | `M_CHAIN_PHASE_DETERMINATION` | CHAIN | 阶段判定 | pending_algorithm（基于环节数据的分阶段判定模型） | MODEL |  |
| 41 | `M_CHAIN_POLICY_MATCH_SCORE` | CHAIN | 产业政策匹配度 | pending_algorithm（产业链标签 vs 政策标签匹配评分） | MODEL |  |
| 42 | `M_CHAIN_PRODUCT_COUNT` | CHAIN | 产业链关联产品数 | COUNT(DISTINCT dwd.industry_chain_product.product_id) | STAT |  |
| 43 | `M_CHAIN_REG_COMMERCIALIZATION` | CHAIN | 企业商业化能力 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 44 | `M_CHAIN_REG_COMP_ACADEMIC` | CHAIN | 学术生态 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 45 | `M_CHAIN_REG_COMP_ENTERPRISE` | CHAIN | 企业能力 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 46 | `M_CHAIN_REG_COMP_SUPPORT` | CHAIN | 配套生态力 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 47 | `M_CHAIN_REG_ECOSYSTEM` | CHAIN | 配套生态 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 48 | `M_CHAIN_REG_FINANCING` | CHAIN | 融资事件 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 49 | `M_CHAIN_REG_PAPERS` | CHAIN | 高校论文 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 50 | `M_CHAIN_REG_PATENT` | CHAIN | 专利 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 51 | `M_CHAIN_REG_POLICY_COVERAGE` | CHAIN | 政策覆盖率 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 52 | `M_CHAIN_REG_RESEARCH_ORG` | CHAIN | 科研机构 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 53 | `M_CHAIN_REG_REVENUE` | CHAIN | 营收 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 54 | `M_CHAIN_REG_SERVICE_ORG` | CHAIN | 服务机构 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 55 | `M_CHAIN_REG_TALENT_STRUCTURE` | CHAIN | 人才结构 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 56 | `M_CHAIN_REG_TECH_BARRIER` | CHAIN | 技术壁垒 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 57 | `M_CHAIN_REG_TECH_MATURITY` | CHAIN | 技术成熟度 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 58 | `M_CHAIN_REGION_INDEX` | CHAIN | 区域产业综合指数 | pending_algorithm（enterprise_power_score*W1 + academic_power | MODEL |  |
| 59 | `M_CHAIN_STAGE_SCORE` | CHAIN | 周期阶段评分 | pending_algorithm（CHAIN_CYCLE 模型置信度输出） | MODEL |  |
| 60 | `M_CHAIN_STRATEGIC_IMPORTANCE` | CHAIN | 战略重要性评分 | pending_algorithm（技术壁垒*w1+市场集中度*w2+国产化率*w3+政策导向*w4） | MODEL |  |
| 61 | `M_CHAIN_SUPPLY_RELATION_COUNT` | CHAIN | 供应链关系数 | pending_algorithm（NebulaGraph gkx_chain supplies 边 COUNT） | GRAPH |  |
| 62 | `M_CHAIN_SUPPORT_POWER` | CHAIN | 配套支撑指数 | pending_algorithm（政策匹配度*w1 + 服务机构密度*w2 + 基础设施*w3） | MODEL |  |
| 63 | `M_CHAIN_SZ_ADVANTAGE_RANK` | CHAIN | 深圳优势排名 | pending_algorithm（RANK() OVER ORDER BY 优势评分 DESC） | MODEL |  |
| 64 | `M_CHAIN_SZ_ADVANTAGE_SCORE` | CHAIN | 深圳优势评分 | pending_algorithm（深圳产业密度*w1+企业实力*w2+科研实力*w3+政策支撑*w4） | MODEL |  |
| 65 | `M_CHAIN_SZ_COMPLETENESS` | CHAIN | 深圳产业链完整度 | pending_algorithm（深圳覆盖环节数 / 全链环节数 * 100） | MODEL |  |
| 66 | `M_CHAIN_SZ_ENTERPRISE` | CHAIN | 对比四维-企业 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 67 | `M_CHAIN_SZ_ENTERPRISE_COUNT` | CHAIN | 深圳产业链企业数 | COUNT(DISTINCT enterprise_code) WHERE headquarters_city='深圳' | STAT |  |
| 68 | `M_CHAIN_SZ_ENTERPRISE_RATIO` | CHAIN | 深圳产业链企业占比 | M_CHAIN_SZ_ENTERPRISE_COUNT / M_CHAIN_ENTERPRISE_COUNT * 100 | STAT |  |
| 69 | `M_CHAIN_SZ_INSTITUTION_COUNT` | CHAIN | 深圳产业链机构数 | COUNT(DISTINCT enterprise_name) WHERE headquarters_city='深圳' | STAT |  |
| 70 | `M_CHAIN_SZ_KEY_NODE_COUNT` | CHAIN | 深圳关键环节覆盖数 | COUNT(DISTINCT node_name) WHERE is_key_node=1 AND headquarte | GRAPH |  |
| 71 | `M_CHAIN_SZ_KEY_NODE_COVERAGE` | CHAIN | 深圳关键环节覆盖率 | pending_algorithm（深圳覆盖关键环节数 / 全链关键环节数 * 100） | MODEL |  |
| 72 | `M_CHAIN_SZ_OPPORTUNITY_COUNT` | CHAIN | 深圳产业机遇数 | pending_algorithm（基于产业缺口+深圳优势匹配的机遇识别模型） | MODEL |  |
| 73 | `M_CHAIN_SZ_OPPORTUNITY_SCORE` | CHAIN | 深圳产业机遇评分 | pending_algorithm（产业缺口*w1+深圳匹配度*w2+政策机遇*w3） | MODEL |  |
| 74 | `M_CHAIN_SZ_PATENT` | CHAIN | 对比四维-专利 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 75 | `M_CHAIN_SZ_POLICY` | CHAIN | 对比四维-政策 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 76 | `M_CHAIN_SZ_PROBLEM_COUNT` | CHAIN | 深圳产业问题数 | COUNT(DISTINCT id) FROM dwd.industry_bottleneck WHERE region | STAT |  |
| 77 | `M_CHAIN_SZ_REGION_COUNT` | CHAIN | 深圳产业分布区域数 | COUNT(DISTINCT headquarters_district) WHERE headquarters_cit | STAT |  |
| 78 | `M_CHAIN_SZ_TALENT` | CHAIN | 对比四维-人才 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 79 | `M_CHAIN_TECH_MATURITY_SCORE` | CHAIN | 技术成熟度评分 | pending_algorithm（专利平均年龄*w1+专利增长率*w2+技术覆盖度*w3） | MODEL |  |
| 80 | `M_CHAIN_TECH_POWER` | CHAIN | 技术力 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 81 | `M_CHAIN_TOTAL_COUNT` | CHAIN | 产业链总数 | COUNT(DISTINCT dwd.industry_chain.chain_id) | STAT |  |
| 82 | `M_CHAIN_TREND_INDEX` | CHAIN | 产业链变化趋势指数 | pending_algorithm（企业增速*w1+专利增速*w2+资讯热度变化*w3+投融资变化*w4） | MODEL |  |
| 83 | `M_CHAIN_UPSTREAM_COUNT` | CHAIN | 上游环节数 | COUNT(DISTINCT node_name) WHERE chain_stage='upstream' | GRAPH |  |
| 84 | `M_ENT_AGGLOMERATION_INDEX` | ENT | 集聚指数 | pending_algorithm（区位熵 LQ 或 基尼系数） | MODEL |  |
| 85 | `M_ENT_ATTRACT_SCORE` | ENT | 招引推荐评分（demo路径） | attract_score = w_tech*tech_proxy + w_growth*growth + w_regi | GRAPH |  |
| 86 | `M_ENT_AVG_RD_INVESTMENT` | ENT | 平均研发投入 | AVG(dwd.enterprise.rd_investment) | STAT |  |
| 87 | `M_ENT_CHAIN_COMPLETENESS` | ENT | 产业链完整度 | pending_algorithm（覆盖环节数 / 全链环节数 * 100） | MODEL |  |
| 88 | `M_ENT_CITY_AVG_TECH_POWER` | ENT | 城市平均技术力 | pending_algorithm（AVG(tech_score) GROUP BY city） | MODEL |  |
| 89 | `M_ENT_CITY_DENSITY` | ENT | 企业密度 | pending_algorithm（城市企业数 / 城市面积或单位GDP） | MODEL |  |
| 90 | `M_ENT_COMPETITIVENESS_RANK` | ENT | 综合竞争力排名 | 基于ads_ent_competitiveness_score表中score字段在同业分组内降序排名。 | MODEL |  |
| 91 | `M_ENT_CORE_SUPPLIER_COUNT` | ENT | 核心供应商数 | COUNT(DISTINCT related_enterprise_id) WHERE relation_level=1 | MODEL |  |
| 92 | `M_ENT_CULTIVATE_SCORE` | ENT | 培育推荐评分（demo路径） | cultivate_score = w_potential*score_total + w_growth*growth  | GRAPH |  |
| 93 | `M_ENT_DEV_HISTORY` | ENT | 企业发展历程 | timeline = merge(dwd.enterprise_finance_history, dwd.enterpr | MODEL |  |
| 94 | `M_ENT_DIVERSIFICATION_INDEX` | ENT | 多元化指数 | pending_algorithm（领域分布熵 Shannon entropy） | MODEL |  |
| 95 | `M_ENT_DOMAIN_COVERAGE_BREADTH` | ENT | 覆盖广度 | pending_algorithm（覆盖领域数 / 产业领域全集） | MODEL |  |
| 96 | `M_ENT_DOMAIN_COVERAGE_DEPTH` | ENT | 参与深度 | pending_algorithm（dwd_org_industry_chain_dtl.chain_score + 产 | MODEL |  |
| 97 | `M_ENT_DS_02_ENTITY_004` | ENT | [新增] 技术点影响力 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 98 | `M_ENT_DS_07_INDUSTRY_POTENTIAL_004` | ENT | 科学影响力评估 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 99 | `M_ENT_DS_07_INDUSTRY_POTENTIAL_005` | ENT | 技术影响力评估 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 100 | `M_ENT_DS_07_INDUSTRY_POTENTIAL_006` | ENT | 产业发展潜力综合评估 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 101 | `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT` | ENT | 覆盖未来产业数 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 102 | `M_ENT_GROWTH_POTENTIAL` | ENT | 成长潜力 | pending_algorithm（营收/研发增速 + 技术壁垒 + 团队规模 加权） | MODEL |  |
| 103 | `M_ENT_HIGH_TECH_COUNT` | ENT | 高企数量 | pending_algorithm（解析 dwd_company_honor_tags/dwd_org_tag_info | STAT |  |
| 104 | `M_ENT_INDUSTRY_MATCH_SCORE` | ENT | 产业匹配度 | pending_algorithm（基于 dwd_org_industry_chain_dtl.chain_score  | MODEL |  |
| 105 | `M_ENT_INNOVATION_INDEX` | ENT | 创新能力指数 | 三准则层加权汇总：创新投入(研发投入占比/技术人员占比) + 创新产出(专利申请数/专利质量/软著/获奖) + 可持续发 | MODEL |  |
| 106 | `M_ENT_INNOVATIVE_COUNT` | ENT | 创新型企业数 | pending_algorithm（is_high_tech/is_little_giant/is_gazelle/is | STAT |  |
| 107 | `M_ENT_KEY_NODE_COUNT` | ENT | 重点环节企业数 | COUNT(DISTINCT enterprise_id) GROUP BY dwd.enterprise_indust | GRAPH |  |
| 108 | `M_ENT_KEY_TOTAL` | ENT | 重点企业总数 | pending_cosign: human:唐绍祖（未签） | STAT |  |
| 109 | `M_ENT_KEYPANO_DOMAIN_SUMMARY` | ENT | 领域摘要（当前链位） | 关键词抽取 → 领域映射 → COUNT 分组; 证据来源: dwd_paper_keywords, dwd_paten | MODEL |  |
| 110 | `M_ENT_KEYPANO_ENTERPRISE_LIST` | ENT | 企业清单（当前链位） | SELECT enterprise_id, enterprise_name, honor_type_list, regi | GRAPH |  |
| 111 | `M_ENT_KEYPANO_MATCH_COUNT` | ENT | 匹配企业数 | COUNT(DISTINCT enterprise_id) FILTER(industry_chain=:chain A | GRAPH |  |
| 112 | `M_ENT_KEYPANO_QUAL_DISTRIBUTION` | ENT | 整链资质分布 | 4 qual_types × 3 region_levels grid: COUNT(DISTINCT enterpri | STAT |  |
| 113 | `M_ENT_KEYPANO_REGIONAL_COUNT` | ENT | 覆盖区域数 | COUNT(DISTINCT administrative_region) WHERE industry_chain=: | STAT |  |
| 114 | `M_ENT_KEYPANO_REGIONAL_DISTRIBUTION` | ENT | 区域分布 | COUNT(DISTINCT enterprise_id) GROUP BY administrative_region | STAT |  |
| 115 | `M_ENT_KEYPANO_TYPE_COUNT` | ENT | 覆盖企业类型数 | COUNT(DISTINCT honor_type) FROM current_result_set | STAT |  |
| 116 | `M_ENT_KEYPANO_TYPE_STRUCTURE` | ENT | 企业类型分布（当前链位） | COUNT(DISTINCT enterprise_id) GROUP BY honor_type FROM curre | GRAPH |  |
| 117 | `M_ENT_MARKET_SHARE` | ENT | 市场份额 | pending_algorithm（企业营收 / 细分市场总规模）——缺市场规模数据 | STAT |  |
| 118 | `M_ENT_NODE_CENTRALITY` | ENT | 供应链中心性 | 中心度 = deg(v) / (/V/ - 1)，deg(v)为企业直接连接的节点总数。需先建供应链网络图。 | GRAPH |  |
| 119 | `M_ENT_PAINPOINT_GAP` | ENT | 与行业最佳差距 | gap = enterprise_value - industry_baseline(P25/P75 by A3 cha | MODEL |  |
| 120 | `M_ENT_PAINPOINT_SEVERITY` | ENT | 痛难点严重度 | severity := high if drop>0.30 else medium if drop>=0.10 else | MODEL |  |
| 121 | `M_ENT_PATENT_GRANT_COUNT` | ENT | 专利授权量 | 从dwd_patent_legal筛选status为授权，关联dwd_patent匹配企业名，COUNT(DISTINC | STAT |  |
| 122 | `M_ENT_PATENT_TOTAL` | ENT | 专利总量 | SUM(dwd.enterprise.patent_grant_count) | STAT |  |
| 123 | `M_ENT_POLICY_MATCH_SCORE` | ENT | 政策匹配度 | pending_algorithm（企业属性 vs 政策标签匹配评分） | MODEL |  |
| 124 | `M_ENT_PROFIT_MARGIN` | ENT | 利润率 | pending_algorithm（net_profit / operating_revenue * 100） | MODEL |  |
| 125 | `M_ENT_RD_INVESTMENT_RATIO` | ENT | 研发投入占比 | pending_algorithm（rd_investment / revenue_latest * 100） | STAT |  |
| 126 | `M_ENT_RECOMMEND_COUNT` | ENT | 推荐企业数 | COUNT(DISTINCT enterprise_id) WHERE 推荐指数 >= :threshold | MODEL |  |
| 127 | `M_ENT_REGIONAL_COUNT` | ENT | 区域企业数量 | COUNT(DISTINCT enterprise_id) GROUP BY dwd.enterprise.headqu | STAT |  |
| 128 | `M_ENT_REGIONAL_DENSITY` | ENT | 区域企业密度 | pending_algorithm（区域企业数 / 区域面积 或 / 单位GDP） | MODEL |  |
| 129 | `M_ENT_RELATION_STRENGTH` | ENT | 关系强度 | bucket(invest_amount): strong/>1e8/ mid/[1e7,1e8)/ weak/<1e7 | MODEL |  |
| 130 | `M_ENT_RESEARCHER_COUNT` | ENT | 全球企业科研人数 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 131 | `M_ENT_REVENUE_GROWTH_RATE` | ENT | 营收增长率 | pending_algorithm（(本年 operating_revenue − 上年) / 上年 * 100） | STAT |  |
| 132 | `M_ENT_REVENUE_LATEST` | ENT | 营收 | SELECT operating_revenue FROM dwd_org_annual_financial_info  | MODEL |  |
| 133 | `M_ENT_SHORTBOARD_COUNT` | ENT | 短板指标数 | 将各指标实际值与同行业平均值逐一比较，低于基准的指标计为短板并统计总数。 | STAT |  |
| 134 | `M_ENT_STAR_ENTERPRISE_COUNT` | ENT | 明星企业数 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 135 | `M_ENT_SUPPLIER_COUNT` | ENT | 供应商数量 | COUNT(DISTINCT related_enterprise_id) WHERE relation_type='上 | STAT |  |
| 136 | `M_ENT_SZ_CHAIN_POSITION` | ENT | 链中角色 | dwd.enterprise_industry.industry_chain_role | MODEL |  |
| 137 | `M_ENT_SZ_COUNT` | ENT | 深圳企业数 | COUNT(DISTINCT enterprise_id) WHERE headquarters_city='深圳' A | STAT |  |
| 138 | `M_ENT_TECH_RANK` | ENT | 技术力排名 | pending_algorithm（RANK() OVER ORDER BY tech_score DESC） | MODEL |  |
| 139 | `M_ENT_TOTAL_COUNT` | ENT | 企业总数 | COUNT(DISTINCT credit_code WHERE 属于目标未来产业)；从 dwd_org_industr | STAT |  |
| 140 | `M_ENT_TYPE_MATCH_COUNT` | ENT | 匹配企业总数 | COUNT(DISTINCT enterprise_id) WHERE 产业 IN(:industry) AND 类型  | STAT |  |
| 141 | `M_ENT_TYPE_RATIO` | ENT | 类型占比 | M_ENT_TYPE_COUNT / M_ENT_TYPE_MATCH_COUNT * 100 | STAT |  |
| 142 | `M_INNOV_DS_01_EVENTS_001` | INNOV | 事件关注度 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 143 | `M_INNOV_DS_01_EVENTS_002` | INNOV | 事件影响力 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 144 | `M_INNOV_DS_01_EVENTS_003` | INNOV | 重要性等级 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 145 | `M_INNOV_DS_02_PATH_001` | INNOV | 中心度 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 146 | `M_INNOV_DS_02_PATH_002` | INNOV | 关键节点重要性 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 147 | `M_INNOV_DS_02_PATH_003` | INNOV | 节点优先级/重要度 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 148 | `M_INNOV_DS_04_ACHIEVE_OVERVIEW_001` | INNOV | 创新价值 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 149 | `M_INNOV_DS_04_CARRIER_RANK_001` | INNOV | 创新能力指数 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 150 | `M_INNOV_DS_04_CARRIER_RANK_002` | INNOV | 多维度排名展示 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 151 | `M_INNOV_DS_04_MONITOR_001` | INNOV | 创新点发现 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 152 | `M_INNOV_DS_04_MONITOR_002` | INNOV | 创新价值评估 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 153 | `M_INNOV_DS_04_REALTIME_004` | INNOV | 创新影响分数 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 154 | `M_INNOV_DS_04_REALTIME_005` | INNOV | 创新影响预测 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 155 | `M_INNOV_DS_05_GBA_ACHIEVE_004` | INNOV | 创新热点区域识别 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 156 | `M_INNOV_DS_05_GBA_ANALYSIS_003` | INNOV | 优势因素分析 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 157 | `M_INNOV_DS_05_GBA_ANALYSIS_004` | INNOV | 短板因素分析 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 158 | `M_INNOV_DS_05_GBA_ANALYSIS_005` | INNOV | 机会因素分析 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 159 | `M_INNOV_DS_05_GBA_ANALYSIS_006` | INNOV | 威胁因素分析 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 160 | `M_INNOV_DS_06_CARRIER_003` | INNOV | 创新价值排名 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 161 | `M_INNOV_DS_07_SCI_CREATE_004` | INNOV | 科学创造力趋势预测 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 162 | `M_INNOV_DS_09_COMPREHENSIVE_005` | INNOV | 本地特色与优势分析 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 163 | `M_INNOV_DS_09_COMPREHENSIVE_006` | INNOV | 科技人才流动监控 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 164 | `M_INNOV_DS_09_COMPREHENSIVE_008` | INNOV | 潜在科技发展方向预警 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 165 | `M_INNOV_DS_09_RESEARCH_001` | INNOV | 研究领域重叠度 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 166 | `M_INNOV_DS_09_RESEARCH_002` | INNOV | 研究领域等级划分 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 167 | `M_INNOV_DS_09_RESEARCH_003` | INNOV | 竞争情报等级 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 168 | `M_INNOV_DS_09_RESEARCH_004` | INNOV | 多企业竞争情报比对 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 169 | `M_INNOV_DS_25_SOFTSCI_012` | INNOV | 影响力评价与应用反馈 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 170 | `M_INNOV_DS_26_ECO_012` | INNOV | 协同绩效与影响力智能评估 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 171 | `M_INNOV_DS_27_SPATIO_003` | INNOV | 热点区域自动识别与预警 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 172 | `M_INNOV_DS_27_SPATIO_012` | INNOV | 主题演化路径与创新前沿发现 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 173 | `M_INNOV_DS_29_INCUBATOR_006` | INNOV | 影响力评价 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 174 | `M_INNOV_DS_FACTORS_008` | INNOV | 要素影响力 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 175 | `M_INNOV_DS_FACTORS_012` | INNOV | 要素影响力 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 176 | `M_INNOV_DS_FACTORS_014` | INNOV | 要素影响力 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 177 | `M_INNOV_DS_FACTORS_015` | INNOV | 要素影响力 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 178 | `M_INNOV_DS_FACTORS_016` | INNOV | 要素聚类分析 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 179 | `M_INNOV_DS_FACTORS_018` | INNOV | 监测趋势预测 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 180 | `M_INNOV_DS_FACTORS_019` | INNOV | 监测异常点识别 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 181 | `M_POLICY_DS_07_POLICY_GUARD_001` | POLICY | 发展战略引导力评估 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 182 | `M_POLICY_DS_07_POLICY_GUARD_008` | POLICY | 政策与条件保障力综合评估 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 183 | `M_POLICY_DS_11_POLICY_EVAL_012` | POLICY | 智能摘要与结论推送 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 184 | `M_POLICY_DS_11_POLICY_EVAL_015` | POLICY | 实施路径与风险辅助 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 185 | `M_POLICY_EFFECT_SCORE` | POLICY | 政策效果评分 | pending_algorithm（执行效果*w1 + 社会经济效应*w2 + 环境影响*w3；关键输入待采购，权重待  | MODEL |  |
| 186 | `M_POLICY_FOCUS_INDEX` | POLICY | 政策焦点指数 | pending_algorithm（焦点维度指标体系加权打分，维度/阈值待 QPOL-02） | MODEL |  |
| 187 | `M_POLICY_IMPLEMENTATION_EFFECT` | POLICY | 落地实效性 | pending_algorithm（落地执行率 + 受益覆盖 + 反馈满意度加权；关键输入待采购，权重待 QPOL-02 | MODEL |  |
| 188 | `M_POLICY_INDUSTRY_COVERAGE` | POLICY | 政策产业覆盖度 | pending_algorithm（DISTINCT 覆盖产业节点数 / 产业链全节点数 * 100） | STAT |  |
| 189 | `M_POLICY_INDUSTRY_FIT` | POLICY | 产业适配性 | pending_algorithm（政策标签 vs 产业需求标签相似度加权，匹配规则待 QPOL-03） | MODEL |  |
| 190 | `M_POLICY_INTENSITY_INDEX` | POLICY | 政策力度指数 | pending_algorithm（补贴*w1 + 税收优惠*w2 + 政策数量*w3 + 执行周期*w4，权重待 QP | MODEL |  |
| 191 | `M_POLICY_INTENSITY_SCORE` | POLICY | 政策力度评分 | pending_algorithm（效果维度*w1 + 覆盖维度*w2 + 成本维度*w3，权重待 QPOL-02） | MODEL |  |
| 192 | `M_POLICY_LAYOUT_REC_COUNT` | POLICY | 政策布局建议数 | pending_algorithm（COUNT(布局建议 WHERE 优先级评分 >= 阈值)，融合机遇/短板/专家策略 | MODEL |  |
| 193 | `M_POLICY_LEVEL_DIST` | POLICY | 政策级别分布 | COUNT(DISTINCT policy_id) GROUP BY dwd.policy_base_info.leve | STAT |  |
| 194 | `M_POLICY_NATIONAL_DIST` | POLICY | 全国政策分布 | COUNT(DISTINCT policy_id) GROUP BY province(dwd.policy_base_ | STAT |  |
| 195 | `M_POLICY_OPPORTUNITY_COUNT` | POLICY | 政策机遇数 | pending_algorithm（COUNT(政策 WHERE 关注度/影响力/稳定性 >= 阈值)，维度/阈值待 Q | MODEL |  |
| 196 | `M_POLICY_RELATION_DEGREE` | POLICY | 政策关联度 | pending_algorithm（NebulaGraph gkx_policy 加权度中心性：扶持/适用/监管/引用  | GRAPH |  |
| 197 | `M_POLICY_SHORTBOARD_COUNT` | POLICY | 政策短板数 | pending_algorithm（COUNT(短板维度 WHERE 评估值 < 阈值)，维度/阈值待 QPOL-02） | MODEL |  |
| 198 | `M_POLICY_SUPPORT_STRENGTH` | POLICY | 支持力度 | pending_algorithm（扶持力度档位*w1 + 政策层级权重*w2 + 政策数量*w3，权重待 QPOL-0 | STAT |  |
| 199 | `M_POLICY_SZ_DIST` | POLICY | 深圳政策分布 | COUNT(DISTINCT policy_id) WHERE region LIKE '%深圳%' GROUP BY  | STAT |  |
| 200 | `M_POLICY_TIMESERIES` | POLICY | 政策时序指标 | 发布量=COUNT(DISTINCT policy_id) GROUP BY 期；增长率/连续性 pending_alg | STAT |  |
| 201 | `M_POLICY_TOTAL_COUNT` | POLICY | 政策总数 | COUNT(DISTINCT dwd.policy_base_info.policy_id) | STAT |  |
| 202 | `M_POLICY_TYPE_DIST` | POLICY | 政策类型分布 | pending_algorithm（解析 topic_type/ma_contenttypenew/complextag | COMPUTE |  |
| 203 | `M_POLICY_VALIDITY_RATE` | POLICY | 政策时效 | pending_algorithm（COUNT(status=1 AND (expire_date IS NULL OR | STAT |  |
| 204 | `M_SVC_CHAIN_BOTTLENECK` | SVC | 瓶颈堵点判定 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 205 | `M_SVC_CHAIN_SEGMENT_AVG_DEPTH` | SVC | 环节平均服务深度 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 206 | `M_SVC_CHAIN_SEGMENT_ORG_COUNT` | SVC | 环节服务机构数 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 207 | `M_SVC_GRAPH_CENTRALITY` | SVC | 节点度中心性 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 208 | `M_SVC_GRAPH_DENSITY` | SVC | 服务网络密度 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 209 | `M_SVC_GRAPH_INFLUENCE` | SVC | 生态影响力评分 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 210 | `M_SVC_ORG_COVERAGE_BREADTH` | SVC | 服务广度 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 211 | `M_SVC_ORG_COVERAGE_DEPTH` | SVC | 服务深度得分 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 212 | `M_SVC_ORG_MARKET_HEAT` | SVC | 市场热度评级 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 213 | `M_SVC_ORG_NEW_COUNT` | SVC | 年度新增服务机构数 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 214 | `M_SVC_ORG_SELECTED_COUNT` | SVC | 当前分析机构数 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 215 | `M_SVC_ORG_TOTAL` | SVC | 入库服务机构总数 | pending_cosign: human:唐绍祖（未签） | STAT |  |
| 216 | `M_SVC_PT_CHAIN_NODE_ORG` | SVC | 产业链节点服务机构数 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 217 | `M_SVC_PT_GLOBAL_SCALE_DIST` | SVC | 全球服务机构规模分布 | pending_cosign: human:唐绍祖（未签） | STAT |  |
| 218 | `M_SVC_PT_GLOBAL_TOTAL` | SVC | 全球服务机构总数 | pending_cosign: human:唐绍祖（未签） | STAT |  |
| 219 | `M_SVC_PT_GLOBAL_TYPE_DIST` | SVC | 全球服务机构类型分布 | pending_cosign: human:唐绍祖（未签） | STAT |  |
| 220 | `M_SVC_PT_KEYORG_SCALE` | SVC | 重点机构规模档案值 | pending_cosign: human:唐绍祖（未签） | STAT |  |
| 221 | `M_SVC_PT_REGION_ORG` | SVC | 区域服务机构数 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 222 | `M_SVC_PT_SZ_FIELD_DIST` | SVC | 深圳机构产业领域分布 | pending_cosign: human:唐绍祖（未签） | STAT |  |
| 223 | `M_SVC_PT_SZ_REGION_ORG` | SVC | 深圳机构区域分布 | pending_cosign: human:唐绍祖（未签） | STAT |  |
| 224 | `M_SVC_PT_SZ_TOTAL` | SVC | 深圳产业服务机构数量 | pending_cosign: human:唐绍祖（未签） | STAT |  |
| 225 | `M_SVC_PT_SZ_TYPE_DIST` | SVC | 深圳机构类型统计 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 226 | `M_SVC_REC_ATTRACT_SCORE` | SVC | 招引综合评分 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 227 | `M_SVC_REC_CANDIDATE_CNT` | SVC | 候选机构数 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 228 | `M_SVC_REC_CULTIVATE_SCORE` | SVC | 培育综合评分 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 229 | `M_SVC_SZ_CHAIN_COMPLETENESS` | SVC | 服务链完整度 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 230 | `M_SVC_SZ_COMPARE_METRIC` | SVC | 城市对比指标值 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 231 | `M_SVC_SZ_TIER` | SVC | 深圳梯队位置 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 232 | `M_SYNTH_COLLAB_CENTRALITY` | SYNTH | 协同网络中心度 | pending_algorithm（节点度中心性 degree/(N-1)；正式算法待 Q-SYNTH-C-01 闭合） | GRAPH |  |
| 233 | `M_SYNTH_COLLAB_COMPLETENESS` | SYNTH | 协同网络完整度 | pending_algorithm（已建立有效合作关系的主体数 / 纳入分析的有效主体总数 × 100%；正式分母待 Q | MODEL |  |
| 234 | `M_SYNTH_COLLAB_DENSITY` | SYNTH | 协同网络密度 | pending_algorithm（无向简单图 2E/[N×(N-1)]；正式图模型待 Q-SYNTH-C-01 闭合） | GRAPH |  |
| 235 | `M_SYNTH_COLLAB_INDEX` | SYNTH | 区域创新协同指数 | pending_algorithm（三指标归一化后加权合成；权重/校准待 Q-SYNTH-C-02 闭合） | MODEL |  |
| 236 | `M_SYNTH_COLLAB_OUTPUT_CORR` | SYNTH | 协同—创新产出关联结果 | pending_algorithm（Pearson/Spearman 相关；方法/样本门槛待 Q-SYNTH-C-03  | MODEL |  |
| 237 | `M_SYNTH_COLLAB_RELATION_INPUT` | SYNTH | 协同关系输入统计 | COUNT(DISTINCT relation_event_id) GROUP BY relation_type, re | STAT |  |
| 238 | `M_SYNTH_DS_21_GRAPH_ANALYSIS_005` | SYNTH | 自动模式识别 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 239 | `M_SYNTH_DS_21_GRAPH_ANALYSIS_006` | SYNTH | 预测分析 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 240 | `M_SYNTH_DS_21_GRAPH_ANALYSIS_007` | SYNTH | 分类与聚类 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 241 | `M_SYNTH_DS_21_GRAPH_ANALYSIS_008` | SYNTH | 智能推荐 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 242 | `M_SYNTH_DS_23_GRAPH_ALGO_001` | SYNTH | 多种路径搜索算法支持 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 243 | `M_SYNTH_DS_23_GRAPH_ALGO_002` | SYNTH | 最优路径发现与展示 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 244 | `M_SYNTH_DS_23_GRAPH_ALGO_006` | SYNTH | 度中心性计算与展示 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 245 | `M_SYNTH_DS_23_GRAPH_ALGO_007` | SYNTH | 紧密中心性计算与展示 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 246 | `M_SYNTH_DS_23_GRAPH_ALGO_008` | SYNTH | 中介中心性计算与展示 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 247 | `M_SYNTH_DS_23_GRAPH_ALGO_009` | SYNTH | PageRank算法计算与展示 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 248 | `M_SYNTH_DS_23_GRAPH_ALGO_011` | SYNTH | 多种社群发现算法支持 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 249 | `M_SYNTH_DS_23_GRAPH_ALGO_012` | SYNTH | 社群结构自动识别 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 250 | `M_SYNTH_DS_23_GRAPH_ALGO_013` | SYNTH | 社群属性与特征分析 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 251 | `M_SYNTH_DS_23_GRAPH_ALGO_014` | SYNTH | 社群动态演化追踪 | pending_cosign: human:唐绍祖（未签） | GRAPH |  |
| 252 | `M_SYNTH_ELEM_CONTRIB` | SYNTH | 要素贡献度与影响路径 | pending_algorithm（贡献度量化 + 影响路径识别；方法待 Q-SYNTH-E-02 闭合） | GRAPH |  |
| 253 | `M_SYNTH_ELEM_DOMAIN_INDEX` | SYNTH | 区域创新要素领域指数 | pending_algorithm（领域维度加权 + 归一化；权重待 Q-SYNTH-E-01 闭合） | MODEL |  |
| 254 | `M_SYNTH_ELEM_INDEX` | SYNTH | 区域创新要素指数（综合） | pending_algorithm（三维加权合成；权重/公式待 Q-SYNTH-02 闭合） | MODEL |  |
| 255 | `M_SYNTH_ELEM_INDICATOR` | SYNTH | 要素分项指标值与得分 | pending_algorithm（分项指标采集 + 归一化评分） | MODEL |  |
| 256 | `M_SYNTH_ELEM_LEVEL_INDEX` | SYNTH | 区域创新要素层次指数 | pending_algorithm（结构维度加权 + 达标判定；权重/阈值待 Q-SYNTH-E-01 闭合） | MODEL |  |
| 257 | `M_SYNTH_ELEM_LEVEL_SCORE` | SYNTH | 七大结构层次评价 | pending_algorithm（结构达标判定 + 层次评分） | MODEL |  |
| 258 | `M_SYNTH_ELEM_RANK` | SYNTH | 对比范围要素综合排名 | RANK(M_SYNTH_ELEM_INDEX) OVER (ORDER BY index DESC) — 依赖指数公式 | MODEL |  |
| 259 | `M_SYNTH_ELEM_TYPE_INDEX` | SYNTH | 区域创新要素类型指数 | pending_algorithm（七要素加权 + 归一化；权重待 Q-SYNTH-E-01 闭合） | MODEL |  |
| 260 | `M_SYNTH_ELEM_TYPE_SCORE` | SYNTH | 七要素类型维得分 | pending_algorithm（各要素类型维加权评分；权重待 Q-SYNTH-E-01 闭合） | MODEL |  |
| 261 | `M_SYNTH_ELEM_WEIGHT` | SYNTH | 类型/层次/领域权重分布 | pending_algorithm（三维权重分配待 Q-SYNTH-E-01 闭合） | STAT |  |
| 262 | `M_SYNTH_VIT_DIM_SCORE` | SYNTH | 四维单维评分 | pending_algorithm（维度内加权求和 + 归一化；权重待 Q-SYNTH-V-01 闭合） | MODEL |  |
| 263 | `M_SYNTH_VIT_INDEX` | SYNTH | 区域创新活力指数 | pending_algorithm（四维加权求和；权重/归一化基准待 Q-SYNTH-01 闭合） | MODEL |  |
| 264 | `M_SYNTH_VIT_INDICATOR` | SYNTH | 活力分项指标值与得分 | pending_algorithm（分项指标值采集 + 归一化评分） | MODEL |  |
| 265 | `M_SYNTH_VIT_RANK` | SYNTH | 对比范围活力排名 | RANK(M_SYNTH_VIT_INDEX) OVER (ORDER BY index DESC) — 依赖指数公式闭 | MODEL |  |
| 266 | `M_SYNTH_VIT_WEIGHT` | SYNTH | 维度权重分布 | pending_algorithm（权重分配方案待 Q-SYNTH-V-01 闭合） | STAT |  |
| 267 | `M_TALENT_DS_16_TALENT_RECRUIT_005` | TALENT | 沟通障碍智能检测 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 268 | `M_TALENT_DS_16_TALENT_RECRUIT_006` | TALENT | 文化融合风险评估 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 269 | `M_TALENT_DS_16_TALENT_RECRUIT_007` | TALENT | 国际流动壁垒分析 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 270 | `M_TALENT_DS_16_TALENT_RECRUIT_010` | TALENT | 引进阻力量化评分 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 271 | `M_TALENT_DS_16_TALENT_RECRUIT_013` | TALENT | 高精度成本模型构建 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 272 | `M_TALENT_DS_16_TALENT_RECRUIT_025` | TALENT | 团队组合与协同分析 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 273 | `M_TECH_DS_07_TECH_INNOV_002` | TECH | 专利质量评估 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 274 | `M_TECH_DS_07_TECH_INNOV_004` | TECH | 技术创新力综合评估 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 275 | `M_TECH_DS_07_TECH_INNOV_006` | TECH | 技术创新趋势预测 | pending_cosign: human:唐绍祖（未签） | MODEL |  |
| 276 | `M_TNIE_EVENT_COUNT` | TNIE | 抽取事件条数 | len(response.events) | MODEL |  |
