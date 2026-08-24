# 重判明细 · SYNTH（46 条）

| # | metric_id | 分组 | 中文名 | 现type | definition | formula | 新判type | 理由 |
|---|---|---|---|---|---|---|---|---|
| 1 | `M_SYNTH_COLLAB_CENTRALITY` | T3 | 协同网络中心度 | GRAPH | draft(Q-SYNTH-C-01)：在所选目标区域与时间窗口形成的协同网络中，衡量企业、科研机构和人才节点连接其他创新主体并产生辐射影响的相对程度；正式采用度中心性、介数中心性或其他算法及区域聚合方法待确认。 | pending_algorithm（节点度中心性 degree/(N-1)；正式算法待 Q-SYNTH-C-01 闭合） |  |  |
| 2 | `M_SYNTH_COLLAB_COMPLETENESS` | T3 | 协同网络完整度 | MODEL | draft(Q-SYNTH-C-01)：在所选目标区域、对比范围与时间窗口内，衡量纳入分析的企业、科研机构和人才等有效创新主体被有效合作关系覆盖的全面程度；正式主体全集、关系有效性、去重规则和分母均待算法定义卡确认。 | pending_algorithm（已建立有效合作关系的主体数 / 纳入分析的有效主体总数 × 100%；正式分母待 Q-SYNTH-C-01 闭合） |  |  |
| 3 | `M_SYNTH_COLLAB_DENSITY` | T3 | 协同网络密度 | GRAPH | draft(Q-SYNTH-C-01)：在所选目标区域与时间窗口形成的创新主体网络中，以实际有效合作连接相对于理论可连接关系的程度反映整体合作紧密度；正式图类型、方向性、重复边合并与边权处理规则待确认。 | pending_algorithm（无向简单图 2E/[N×(N-1)]；正式图模型待 Q-SYNTH-C-01 闭合） |  |  |
| 4 | `M_SYNTH_COLLAB_INDEX` | T3 | 区域创新协同指数 | MODEL | missing(Q-SYNTH-C-02)：将网络完整度、中心度和密度三项指标标准化、综合加权并结合历史数据校准后形成的区域创新合作综合结果，用于横向区域对比和纵向趋势分析；正式标准化方法、权重、校准窗口与集群/孤立判据待确认。禁止以密度×强度冒充正式公式。 | pending_algorithm（三指标归一化后加权合成；权重/校准待 Q-SYNTH-C-02 闭合） |  |  |
| 5 | `M_SYNTH_COLLAB_OUTPUT_CORR` | T3 | 协同—创新产出关联结果 | MODEL | missing(Q-SYNTH-C-03)：在明确的区域样本、时间窗口与产出指标口径下，衡量协同网络指标或协同指数与联合发明专利数等创新产出之间的统计关联程度；相关方法、滞后窗口、显著性和最小样本数均待确认。 | pending_algorithm（Pearson/Spearman 相关；方法/样本门槛待 Q-SYNTH-C-03 闭合） |  |  |
| 6 | `M_SYNTH_COLLAB_RELATION_INPUT` | T3 | 协同关系输入统计 | STAT | draft(Q-SYNTH-C-01)：按联合专利、合作项目、人才流动等关系类型，对完成主体匹配、事件去重和有效性校验的合作事件或网络边进行分类统计，作为协同网络建模的可追溯输入。 | COUNT(DISTINCT relation_event_id) GROUP BY relation_type, region, window |  |  |
| 7 | `M_SYNTH_DS_21_GRAPH_ANALYSIS_005` | T3 | 自动模式识别 | MODEL | 05 无模式识别专叶。禁止改挂 116(5)/PATH 中心度。无 also_in。见 GA-D05。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 8 | `M_SYNTH_DS_21_GRAPH_ANALYSIS_006` | T3 | 预测分析 | MODEL | 05 无展示侧预测专叶。禁止 mapped 182–191 / DS-09。禁止静默假网。见 GA-D06。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 9 | `M_SYNTH_DS_21_GRAPH_ANALYSIS_007` | T3 | 分类与聚类 | MODEL | 05 无分类聚类专叶。禁止 mapped 116(4)。见 GA-D07。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 10 | `M_SYNTH_DS_21_GRAPH_ANALYSIS_008` | T3 | 智能推荐 | MODEL | 05 无展示侧推荐专叶。禁止硬挂招入 164。无 also_in 专题 7 条。见 GA-D08。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 11 | `M_SYNTH_DS_23_GRAPH_ALGO_001` | T3 | 多种路径搜索算法支持 | GRAPH | 专用最短路族，05 无专叶。禁止 mapped 116。501 ≠ 库已覆盖。见 DS23-D01。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 12 | `M_SYNTH_DS_23_GRAPH_ALGO_002` | T3 | 最优路径发现与展示 | GRAPH | 专用最短路且无叶。可视化并入本行。禁止 mapped 116。见 DS23-D02。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 13 | `M_SYNTH_DS_23_GRAPH_ALGO_006` | T3 | 度中心性计算与展示 | GRAPH | 05 无度中心性专叶。禁止 116(5)/M_SVC_GRAPH_CENTRALITY。禁止 also_in DS-02-PATH。见 DS23-D06 / DS23-B01。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 14 | `M_SYNTH_DS_23_GRAPH_ALGO_007` | T3 | 紧密中心性计算与展示 | GRAPH | 05 无专叶。禁止 mapped 116。禁止 also_in DS-02-PATH。见 DS23-D07 / DS23-B02。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 15 | `M_SYNTH_DS_23_GRAPH_ALGO_008` | T3 | 中介中心性计算与展示 | GRAPH | 05 无专叶。禁止 also_in DS-02-PATH。见 DS23-D08 / DS23-B03。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 16 | `M_SYNTH_DS_23_GRAPH_ALGO_009` | T3 | PageRank算法计算与展示 | GRAPH | 05 无 PageRank 专叶。不是 IDE。见 DS23-D09 / DS23-B04。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 17 | `M_SYNTH_DS_23_GRAPH_ALGO_011` | T3 | 多种社群发现算法支持 | GRAPH | 05 无社群专叶。116 无社群。501 ≠ 库已覆盖。见 DS23-D11。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 18 | `M_SYNTH_DS_23_GRAPH_ALGO_012` | T3 | 社群结构自动识别 | GRAPH | 要社群划分结果且无专叶。禁止 also_in DS-02-PATH。见 DS23-D12。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 19 | `M_SYNTH_DS_23_GRAPH_ALGO_013` | T3 | 社群属性与特征分析 | GRAPH | 05 无社群特征专叶。核心节点对象不同，禁止 also_in DS-02-PATH。见 DS23-D13。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 20 | `M_SYNTH_DS_23_GRAPH_ALGO_014` | T3 | 社群动态演化追踪 | GRAPH | 05 无动态社群专叶。禁止 mapped seq 132。禁止改挂 DS-27。见 DS23-D14。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 21 | `M_SYNTH_ELEM_CONTRIB` | T3 | 要素贡献度与影响路径 | GRAPH | missing(Q-SYNTH-E-02)：各创新要素对特定产业发展及创新成果的贡献度量化与影响路径识别；算法细则（关联分析方法、贡献度计算模型）待算法定义卡确认。演示态仅展示要素规模占比推导，不作因果结论。 | pending_algorithm（贡献度量化 + 影响路径识别；方法待 Q-SYNTH-E-02 闭合） |  |  |
| 22 | `M_SYNTH_ELEM_DOMAIN_INDEX` | T3 | 区域创新要素领域指数 | MODEL | missing(Q-SYNTH-E-01)：基于产业领域覆盖广度、技术领域应用深度、创新产出强度等维度的领域综合评价指数。算法库 §10.8。 | pending_algorithm（领域维度加权 + 归一化；权重待 Q-SYNTH-E-01 闭合） |  |  |
| 23 | `M_SYNTH_ELEM_INDEX` | T3 | 区域创新要素指数（综合） | MODEL | missing(Q-SYNTH-02)：综合类型/层次/领域三维评价结果的区域创新要素综合指数；正式合成公式、三维权重与归一化基准待算法定义卡确认。临时默认为三维等权合成。 | pending_algorithm（三维加权合成；权重/公式待 Q-SYNTH-02 闭合） |  |  |
| 24 | `M_SYNTH_ELEM_INDICATOR` | T3 | 要素分项指标值与得分 | MODEL | draft(Q-SYNTH-02)：类型/层次/领域三维下各分项要素指标的原始值与归一化得分；正式分项指标池以算法库 §10.6-10.9 为准，待算法定义卡确认完整清单。 | pending_algorithm（分项指标采集 + 归一化评分） |  |  |
| 25 | `M_SYNTH_ELEM_LEVEL_INDEX` | T3 | 区域创新要素层次指数 | MODEL | missing(Q-SYNTH-E-01)：基于七要素结构（人才结构/企业结构/政策结构/服务机构结构/科研机构结构/资金结构/空间结构）的层次综合评价指数，衡量创新体系成熟度与均衡度。算法库 §10.7。 | pending_algorithm（结构维度加权 + 达标判定；权重/阈值待 Q-SYNTH-E-01 闭合） |  |  |
| 26 | `M_SYNTH_ELEM_LEVEL_SCORE` | T3 | 七大结构层次评价 | MODEL | draft(Q-SYNTH-E-01)：七要素各自结构层次的达标评价结果（成熟度/均衡度/达标）；评价方法与阈值待算法定义卡确认。 | pending_algorithm（结构达标判定 + 层次评分） |  |  |
| 27 | `M_SYNTH_ELEM_RANK` | T3 | 对比范围要素综合排名 | MODEL | missing(Q-SYNTH-02)：目标区域在所选对比范围内的要素综合指数排名；排名基于 M_SYNTH_ELEM_INDEX 计算结果排序，指数公式未定前排名禁止对外决策展示。 | RANK(M_SYNTH_ELEM_INDEX) OVER (ORDER BY index DESC) — 依赖指数公式闭合 |  |  |
| 28 | `M_SYNTH_ELEM_TYPE_INDEX` | T3 | 区域创新要素类型指数 | MODEL | missing(Q-SYNTH-E-01)：基于七要素（人才/企业/政策/服务机构/科研机构/资金/空间）配置水平的类型综合评价指数；正式指标体系、阈值与权重待算法定义卡确认。算法库 §10.6。 | pending_algorithm（七要素加权 + 归一化；权重待 Q-SYNTH-E-01 闭合） |  |  |
| 29 | `M_SYNTH_ELEM_TYPE_SCORE` | T3 | 七要素类型维得分 | MODEL | draft(Q-SYNTH-E-01)：创新人才/企业/政策/服务机构/科研机构/资金/空间七类要素各自的类型维量化评分；评分基于规模、质量、活跃度等维度，正式指标池与权重待确认。 | pending_algorithm（各要素类型维加权评分；权重待 Q-SYNTH-E-01 闭合） |  |  |
| 30 | `M_SYNTH_ELEM_WEIGHT` | T3 | 类型/层次/领域权重分布 | STAT | missing(Q-SYNTH-E-01)：类型/层次/领域三维在要素综合指数合成中的权重分配；正式权重合计规则、阈值来源与产品展示口径待算法 Lead + 语义 Owner 确认。临时展示默认等权 + ⚠️ 待甲方确认。 | pending_algorithm（三维权重分配待 Q-SYNTH-E-01 闭合） |  |  |
| 31 | `M_SYNTH_VIT_DIM_SCORE` | T3 | 四维单维评分 | MODEL | draft(Q-SYNTH-V-01)：科技/产业/人才/政策四个一级维度的单维评分；评分方法为各维度内分项指标加权求和后归一化，权重合计规则与阈值来源待确认。临时展示默认权重表 + ⚠️ 待甲方确认。 | pending_algorithm（维度内加权求和 + 归一化；权重待 Q-SYNTH-V-01 闭合） |  |  |
| 32 | `M_SYNTH_VIT_INDEX` | T3 | 区域创新活力指数 | MODEL | pending_algorithm(Q-SYNTH-01)：基于科技、产业、人才、政策四维指标加权求和合成的区域创新活力综合指数；正式维度权重、阈值来源与归一化基准待算法定义卡确认。临时默认为四维等权 + 对比集合内最大值归一。 | pending_algorithm（四维加权求和；权重/归一化基准待 Q-SYNTH-01 闭合） |  |  |
| 33 | `M_SYNTH_VIT_INDICATOR` | T3 | 活力分项指标值与得分 | MODEL | draft(Q-SYNTH-01)：四维下各分项指标的原始值与归一化得分；分项指标清单以算法库 §10.5 指标体系构建为准（专利成果质量、产业发展水平、人才结构优劣、政策支持力度等），正式指标池待算法定义卡确认。 | pending_algorithm（分项指标值采集 + 归一化评分） |  |  |
| 34 | `M_SYNTH_VIT_RANK` | T3 | 对比范围活力排名 | MODEL | missing(Q-SYNTH-01)：目标区域在所选对比范围（默认全国重点城市）内的活力指数排名；排名基于 M_SYNTH_VIT_INDEX 计算结果排序，但指数公式未定前排名禁止对外决策展示。 | RANK(M_SYNTH_VIT_INDEX) OVER (ORDER BY index DESC) — 依赖指数公式闭合 |  |  |
| 35 | `M_SYNTH_VIT_WEIGHT` | T3 | 维度权重分布 | STAT | missing(Q-SYNTH-V-01)：科技/产业/人才/政策四维在活力指数合成中的权重分配；正式权重合计规则、阈值来源与产品侧计算方法展示口径待算法 Lead + 语义 Owner 确认。临时展示默认等权（各 25%）+ ⚠️ 待甲方确认。 | pending_algorithm（权重分配方案待 Q-SYNTH-V-01 闭合） |  |  |
| 36 | `M_SYNTH_182_1` | TTEMP | 区域科技创新成果综合评价模型 | MIXED | 区域科技创新成果综合评价模型：对应算法库 SRS ALGO-SYNTH-SYNTH-182，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 37 | `M_SYNTH_183_1` | TTEMP | 区域产业创新成果综合评价模型 | MIXED | 区域产业创新成果综合评价模型：对应算法库 SRS ALGO-SYNTH-SYNTH-183，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 38 | `M_SYNTH_184_1` | TTEMP | 区域产业创新人才综合评价模型 | MIXED | 区域产业创新人才综合评价模型：对应算法库 SRS ALGO-SYNTH-SYNTH-184，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 39 | `M_SYNTH_185_1` | TTEMP | 区域产业创新政策综合评价模型 | MIXED | 区域产业创新政策综合评价模型：对应算法库 SRS ALGO-SYNTH-SYNTH-185，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 40 | `M_SYNTH_186_1` | TTEMP | 区域创新活力综合分析模型 | MIXED | 区域创新活力综合分析模型：对应算法库 SRS ALGO-SYNTH-SYNTH-186，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 41 | `M_SYNTH_187_1` | TTEMP | 区域创新要素类型综合评价模型 | MIXED | 区域创新要素类型综合评价模型：对应算法库 SRS ALGO-SYNTH-SYNTH-187，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 42 | `M_SYNTH_188_1` | TTEMP | 区域创新要素层次综合评价模型 | MIXED | 区域创新要素层次综合评价模型：对应算法库 SRS ALGO-SYNTH-SYNTH-188，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 43 | `M_SYNTH_189_1` | TTEMP | 区域创新要素领域综合评价模型 | MIXED | 区域创新要素领域综合评价模型：对应算法库 SRS ALGO-SYNTH-SYNTH-189，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 44 | `M_SYNTH_190_1` | TTEMP | 区域创新要素综合分析模型 | MIXED | 区域创新要素综合分析模型：对应算法库 SRS ALGO-SYNTH-SYNTH-190，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 45 | `M_SYNTH_191_1` | TTEMP | 区域创新协同分析模型 | MIXED | 区域创新协同分析模型：对应算法库 SRS ALGO-SYNTH-SYNTH-191，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 46 | `M_SYNTH_GRAPHAPI_116_1` | TTEMP | 产业全要素图谱API服务开发 | third_party | 产业全要素图谱API服务开发：对应算法库 SRS ALGO-SYNTH-GRAPHAPI-116，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
