# 重判明细 · TECH（39 条）

| # | metric_id | 分组 | 中文名 | 现type | definition | formula | 新判type | 理由 |
|---|---|---|---|---|---|---|---|---|
| 1 | `M_TECH_COMPOSITE_SCORE` | T2 | 评估综合得分 | COMPUTE | 对该技术多项评价指标加权后的综合评价结果，供本页读面与下钻报告展示。本页只读 ADS 已落库字段，不跑综合评价 Job，不把 seq 182–191 抄成我方公式。分项与权重未冻。不是专题深圳潜力与阶段综合评估。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 2 | `M_TECH_CONVERT_BOTTLENECK` | T2 | 技术转化瓶颈识别 | third_party | 输入 technology_id，标识转化堵点并给出原因与改进建议（清单/报告）。 流程图/时间轴为同叶流程面，无独立统计核。不是历程 CMS。 实现类 G3 Job（05 seq 136）；专家知识库步骤未签，不伪展开归因公式。 禁止 M_CHAIN_BOTTLENECK_COUNT 及产业链瓶颈族。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 3 | `M_TECH_EDGE_STRENGTH` | T2 | 技术–技术关联强度 | GRAPH | 技术点之间边权重（半成品本五级只消费技术–技术边）。对象=技术–技术边；窗口=当前图快照。 实体–技术点排序强度归 M_TECH_ENTITY_TOP5，不进本号。禁止 seq 116 / M_SVC_GRAPH_*。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 4 | `M_TECH_ENTITY_INFLUENCE` | T2 | 技术点影响力 / 实体优先级 | MODEL | 按影响力等指标自动排序、优先展示重要实体（xlsx 行 19）。 关联强度排序已由 M_TECH_ENTITY_TOP5 覆盖，本号不重复边权 Top-K。 05 无「技术点关联实体优先级」专叶 → A2 missing 保持。赋号 ≠ mapped。 禁止伪公式、禁止 PATH 中心度改挂、禁止 M_SVC_GRAP | pending_cosign: human:唐绍祖（未签） |  |  |
| 5 | `M_TECH_ENTITY_REL` | T2 | 实体关联关系网 | GRAPH | 以连线或网络图展示与当前技术点相关的实体之间关联。消费 seq 105 关系面，不另开模型。 禁止 seq 116；禁止用 PATH 关键路径顶替。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 6 | `M_TECH_ENTITY_TOP5` | T2 | 根节点 Top5 关键实体与关联强度 | GRAPH | 按已有 105 边权截取与当前根技术点关联的 Top5 实体（人/机构/论文/专利）， 卡片含名称、类型、关联强度。不另造排序模型。维护面候选同源不同面，见 TEMP_DS02_MENT_REC_TOP 复用本号。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 7 | `M_TECH_GRAPH_STRUCT` | T2 | 技术点网图结构 | GRAPH | 当前 Nebula A 面技术点子图（entity_type=technology）上，按已有技术点计算技术–技术关联， 生成可视化图谱结构。对象=技术点主键去重；边=技术–技术；窗口=当前图快照。 层级/类型配色与布局是图壳，不另开 ID。禁止用 M_CHAIN_NODE_COUNT / EDGE_COUNT 顶替。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 8 | `M_TECH_HEAT_INDEX` | T2 | 技术热点热度指数 | third_party | 对象为已对齐技术点。对文献/频次做聚类对齐后，输出该点热度指数、增长曲线与热点报告， 并区分短期热点与长期趋势（同核切片，不另造 ID）。页上不做 NER（建图面抽点）。 实现类 G3 Job（05 seq 134）；不伪展开热度公式。 不 reuse DS-02（TECHGRAPH 热度不进该页）。 不 reuse  | pending_cosign: human:唐绍祖（未签） |  |  |
| 9 | `M_TECH_HEAT_QUERY` | T2 | 查询结果·技术热度 | STAT | 对当前查询结果集中的技术术语/主题做词频统计，以热力图或词云呈现热点。 默认分母=结果集内 term 频次 TF，不做全域 DF（Q-MO-QUERY-03）。 词云/热力图是可视化形态，不另造 ID。不是 05 技术链热点识别 seq 134， 不 mapped 图谱API seq 116，不 reuse M_CHA | pending_cosign: human:唐绍祖（未签） |  |  |
| 10 | `M_TECH_INVEST_AMOUNT` | T2 | 技术投资额 | STAT | 选定时间窗内对该技术的资金投入合计（政府专项与社会资本合计；不含技术交易额、不含产业链企业营收合计）。本页气泡大小或地理「投资分布」读 ADS 字段。无窗口/对象歧义到需单独 Q。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 11 | `M_TECH_LIFE_STAGE` | T2 | 技术发展阶段 | MODEL | 单一技术所处生命周期阶段（内部默认分档：萌芽 / 成长 / 成熟；是否含衰退待算法卡）。作为本页气泡图另一位置维。对照 05 seq 137。与专题 TEMP_TOPIC_TECH_STAGE 默认同口径同号（本页读 ADS，专题跑 Job 写同一结果）；禁止产业链阶段号。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 12 | `M_TECH_MATURITY_LEVEL` | T2 | 技术成熟度 | MODEL | 单一技术从概念到应用转化的成熟水平（连续或分档），作为本页气泡图位置维之一。对象=技术点，不是产业链环节。对照 05 seq 137 成熟度输入；实现类不伪展开。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 13 | `M_TECH_OUTPUT_SCALE` | T2 | 技术规模 | STAT | 选定时间窗内该技术的成果与应用体量（内部默认不含资金投入——投入走 M_TECH_INVEST_AMOUNT）。ADS 读面计数/加总。禁止用论文量、专利量或技术交易额冒充「技术规模」专名。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 14 | `M_TECH_PAPER_PATENT_CNT` | T2 | 技术点论文量 / 专利量 | STAT | 对象为已对齐技术点（entity_type=technology，按 technology_id）。 统计窗口默认累计全量；页上年份筛选为交互壳，不另开 ID。 计量为该点关联论文去重数量与关联专利去重数量（材料+清单上的计数面）。 去重：COUNT(DISTINCT paper_id) / COUNT(DISTINC | pending_cosign: human:唐绍祖（未签） |  |  |
| 15 | `M_TECH_PATH_CENTRALITY` | T2 | 中心度 | GRAPH | 节点在技术点网中的核心程度；作为关键节点识别输入（xlsx 行 17）。 对象=技术点节点；窗口=当前图快照。偏 GRAPH（度/介数/PageRank 公式未签，不拆子号）。 禁止 mapped seq 116；禁止消费 M_SVC_GRAPH_CENTRALITY / M_SYNTH_COLLAB_CENTRALI | pending_cosign: human:唐绍祖（未签） |  |  |
| 16 | `M_TECH_PATH_KEYNODE` | T2 | 关键节点重要性 | GRAPH | 按中心度、影响力自动识别关键节点并特殊样式标记（xlsx 行 20）。放大/变色/图标是同一结果的前端壳。 禁止改挂 seq 131 深圳链；禁止 M_CHAIN_KEY_NODE_COUNT。05 无专叶 → missing 保持；赋号 ≠ mapped。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 17 | `M_TECH_PATH_PRIORITY` | T2 | 节点优先级 / 重要度 | GRAPH | 图谱节点关键程度，用于识别核心节点（xlsx 行 22）。与 KEYNODE 同识别族、半成品分行： 本号默认=重要度级别（可供筛选）；KEYNODE 默认=识别结果+样式。筛选交互壳不另开 ID。 missing 保持；赋号 ≠ mapped。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 18 | `M_TECH_POTENTIAL_SCORE` | T2 | 技术产业化潜力评分 | third_party | 按 technology_id 输出产业化潜力综合分；多技术雷达/排名/对比报告为同核对比面，不另造 ID。 特征含论文量/专利量（本页 M_TECH_PAPER_PATENT_CNT 作输入材料，不把本分改挂为 STAT）+ A 面子图结构。 实现类 G3 Job（05 seq 135）；禁止把「科研/转化/市场三维 | pending_cosign: human:唐绍祖（未签） |  |  |
| 19 | `M_TECH_REL_STRENGTH` | T2 | 技术关联强度 | GRAPH | 技术–技术边上的关联紧密程度，编码为本页弦线图线粗。影响路径=弦上关系流向可视化，不是 DS-02 关键路径，不是中心度 KPI。边权内部默认随 05 seq 105 关系抽取。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 20 | `M_TECH_STAGE_JUDGE` | T2 | 技术阶段判定 | third_party | 输出选定技术点所处阶段及简要说明（状态、关键瓶颈、发展潜力）。 用户参数嵌入提示词后重跑为同核定制面，不另造 ID。 实现类 G3 Job + LLM 未注册 501（TECH-B03）；不伪展开阶段公式；禁止联网检索散文冒充已注册模型。 禁止 M_CHAIN_PHASE_DETERMINATION / M_CHAIN | pending_cosign: human:唐绍祖（未签） |  |  |
| 21 | `M_TECH_SZ_ASSESS` | T2 | 深圳技术潜力与阶段综合评估 | third_party | 基于深圳切片输出潜力评分、发展阶段、优劣势与建议（问题/机遇/布局/细分同层 Job，不另造 ID）。 潜力/阶段计算复用 M_TECH_POTENTIAL_SCORE / M_TECH_STAGE_JUDGE 的核，不发明第二套公式； 本号是深圳综合评估包（独立消费面），不是那两条的地理过滤别名——见 Q-MO-TE | pending_cosign: human:唐绍祖（未签） |  |  |
| 22 | `M_TECH_TOPIC_HEAT` | T2 | 技术话题热度 | MODEL | 在用户选定时间窗内，按技术领域关键词/主题聚合的关注度与活跃程度；对象为技术话题（非单一技术点、非产业链热点领域）。本页热力图只读 ADS 已落库结果，对照算法库 05 seq 134，不在本页跑专题 Job、不伪展开热度公式。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 23 | `M_TECH_DS_07_TECH_INNOV_002` | T3 | 专利质量评估 | MODEL | 05 无专利质量专叶。禁止硬挂 182/186、禁止兄弟 seq 150、禁止 M_CHAIN_HIGH_VALUE_RATIO。见 TINN-D02。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 24 | `M_TECH_DS_07_TECH_INNOV_004` | T3 | 技术创新力综合评估 | MODEL | 禁止硬挂 182/186/190。自定义权重不另开 n/a_ops。见 TINN-D04。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 25 | `M_TECH_DS_07_TECH_INNOV_006` | T3 | 技术创新趋势预测 | MODEL | 禁止 mapped 134/132。禁止改挂 xlsx 行71。见 TINN-D06。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 26 | `M_TECH_BASE_96_1` | TTEMP | 技术基础指标模型构建 | third_party | 技术基础指标模型构建：对应算法库 SRS ALGO-TECH-BASE-96，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 27 | `M_TECH_DEEP_130_1` | TTEMP | 全景技术链模型 | third_party | 全景技术链模型：对应算法库 SRS ALGO-TECH-DEEP-130，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 28 | `M_TECH_DEEP_131_1` | TTEMP | 深圳技术链模型 | third_party | 深圳技术链模型：对应算法库 SRS ALGO-TECH-DEEP-131，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 29 | `M_TECH_DEEP_132_1` | TTEMP | 技术发展历程模型 | third_party | 技术发展历程模型：对应算法库 SRS ALGO-TECH-DEEP-132，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 30 | `M_TECH_DEEP_133_1` | TTEMP | 深圳细分领域分布模型 | third_party | 深圳细分领域分布模型：对应算法库 SRS ALGO-TECH-DEEP-133，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 31 | `M_TECH_DEEP_134_1` | TTEMP | 技术前沿热点领域识别模型 | third_party | 技术前沿热点领域识别模型：对应算法库 SRS ALGO-TECH-DEEP-134，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 32 | `M_TECH_DEEP_135_1` | TTEMP | 技术产业化潜力识别模型 | third_party | 技术产业化潜力识别模型：对应算法库 SRS ALGO-TECH-DEEP-135，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 33 | `M_TECH_DEEP_136_1` | TTEMP | 技术转化瓶颈堵点原因识别模型 | third_party | 技术转化瓶颈堵点原因识别模型：对应算法库 SRS ALGO-TECH-DEEP-136，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 34 | `M_TECH_DEEP_137_1` | TTEMP | 技术阶段分析模型 | third_party | 技术阶段分析模型：对应算法库 SRS ALGO-TECH-DEEP-137，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 35 | `M_TECH_DEEP_138_1` | TTEMP | 深圳技术发展问题识别模型 | third_party | 深圳技术发展问题识别模型：对应算法库 SRS ALGO-TECH-DEEP-138，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 36 | `M_TECH_DEEP_139_1` | TTEMP | 深圳技术发展机遇识别模型 | third_party | 深圳技术发展机遇识别模型：对应算法库 SRS ALGO-TECH-DEEP-139，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 37 | `M_TECH_DEEP_140_1` | TTEMP | 深圳技术发展重点布局领域推荐模型 | third_party | 深圳技术发展重点布局领域推荐模型：对应算法库 SRS ALGO-TECH-DEEP-140，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 38 | `M_TECH_GRAPH_104_1` | TTEMP | 技术实体识别构建 | third_party | 技术实体识别构建：对应算法库 SRS ALGO-TECH-GRAPH-104，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 39 | `M_TECH_GRAPH_105_1` | TTEMP | 技术实体关系抽取 | third_party | 技术实体关系抽取：对应算法库 SRS ALGO-TECH-GRAPH-105，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
