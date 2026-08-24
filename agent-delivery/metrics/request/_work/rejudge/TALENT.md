# 重判明细 · TALENT（32 条）

| # | metric_id | 分组 | 中文名 | 现type | definition | formula | 新判type | 理由 |
|---|---|---|---|---|---|---|---|---|
| 1 | `M_TALENT_ACADEMIC_SCORE` | T2 | 人才学术力指数 | MODEL | 用户可组合指标与权重后的人才学术力综合评分、排名与名单对比。内部默认：一条综合指数； 分项维名跟 05（成果数量/学术影响力/专业技能）；04 H 指数/被引/期刊/合作广度作第三方内部特征， 不展开公式、不单列 ID（Q-MO-TALENT-03）。禁止 M_CHAIN_ACADEMIC_POWER / M_SYNT | pending_cosign: human:唐绍祖（未签） |  |  |
| 2 | `M_TALENT_ATTRACT_SCORE` | T2 | 引入人才推荐指数 | MODEL | 全球库中与深圳产业发展方向契合的外部人才综合推荐分（G3 Job，非 G1 图算）。 名单规模为同核 STAT 面（共 N 人），不另造 CNT ID。分项维与推荐理由不单列（Q-MO-TALENT-06）。 可与 DS-16 复用本核，不改挂展示页、不消费展示 OPEN。 禁止 M_SVC_REC_* / M_ENT | pending_cosign: human:唐绍祖（未签） |  |  |
| 3 | `M_TALENT_CULTIVATE_SCORE` | T2 | 培育人才推荐指数 | MODEL | 高成长潜力人才综合培育推荐分 + 建议名单规模（G3 Job）。培育方向建议为文本，无独立 ID。 分项维不单列（Q-MO-TALENT-06）。禁止 M_SVC_REC_* / M_ENT_CULTIVATE_SCORE / M_ENT_CULTIVATION_INDEX。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 4 | `M_TALENT_FLOW_TRACK` | T2 | 人才流动追踪 | GRAPH | 区域/行业人才流入、流出、留存的时间序列（自然年）。用关系边+时间属性；禁止 GIS 轨迹引擎。 三面共一条 ID，不拆。04 未单列流动页不影响本核。可与展示 DS-14 迁徙同源，不改挂、不消费展示 OPEN。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 5 | `M_TALENT_INDUSTRY_SCORE` | T2 | 人才产业力指数 | MODEL | 特定产业领域内人才个人产业转化贡献的综合评分与排名。内部默认取 04：专利转化/项目/商业化（对象=人）。 05 企业侧「人才综合实力（影响力/产业覆盖/媒体知名度）」不作为本 ID 主口径（Q-MO-TALENT-04）。 禁止伪展开转化率；禁止改挂企业指标。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 6 | `M_TALENT_ORG_DIST` | T2 | 重点人才机构分布 | STAT | 内部默认取招标 04：在高校/院所/企业等类型（用户可筛）下，按人才所属机构聚合， 输出该产业或技术领域内人才最集中的前 N 家机构及其人才数量与占比（名录去重、当前快照）。 05「省/国家拥有的人才机构数」不作为本 ID 主口径（Q-MO-TALENT-01）。 不发明机构数/占比分项 ID。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 7 | `M_TALENT_REGIONAL_DIST` | T2 | 重点人才区域分布 | STAT | 用户选定产业或技术领域下，对重点人才（第三方名录、人才实体去重）按地理单元计数， 并支持多领域并列对照。内部默认：当前快照；地理粒度=国家与省级并列（全球库含境外）； 重点人才集合见 Q-MO-TALENT-10。地图可视化与筛选壳不进本 ID。 禁止复用 M_CHAIN_REG_TALENT_STRUCTURE /  | pending_cosign: human:唐绍祖（未签） |  |  |
| 8 | `M_TALENT_RELATION_NET` | T2 | 重点人才关系链结构 | GRAPH | 论文/专利/组织/项目多源融合后的合作、引用等多元关系网络（节点/边规模等图统计）， 支撑最短路径与节点洞察呈现。G1 当前图（Nebula）。内部默认：路径长度与节点画像不单列 ID （Q-MO-TALENT-08）。可与展示 DS-15 同源，不改挂、不消费展示 OPEN。可视化拖拽不进本 ID。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 9 | `M_TALENT_STRUCT_QUERY` | T2 | 查询结果·人才结构 | STAT | 对当前查询命中结果集中的人才实体（talent_id 去重）按结构分箱统计人数与占比， 匹配推荐饼图/柱状。统计窗口=当次查询结果集，不是自然年全量名录、不是 05 人才 13 叶。 默认分箱=最高学历；职称/年龄为同一 ID 下可切换维（Q-MO-QUERY-01）。 禁止消费 TOPIC-TALENT-05 / 综 | pending_cosign: human:唐绍祖（未签） |  |  |
| 10 | `M_TALENT_SUPPLY_STRUCT` | T2 | 人才供给情况 | STAT | 特定领域人才供给的历年变化 + 当前存量结构。内部默认：历年序列用自然年、 学士/硕士/博士毕业数量（05）；存量结构以学历为主；职称/年龄不单列 ID（Q-MO-TALENT-02）。 对象=名录去重人才。领域过滤不另造 ID。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 11 | `M_TALENT_SZ_STATUS` | T2 | 深圳人才现状与优劣势 | MIXED | 统一评价框架下深圳 vs 全国/重点城市的人才横向对比，含计数面（.1）与优劣势/短板面（.7.4）， 一条 MIXED 核不拆（Q-MO-TALENT-07）。供需平衡归 M_TALENT_SZ_SUPPLY_DEMAND。 报告导出壳不进本 ID。禁止 M_CHAIN_SZ_TALENT。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 12 | `M_TALENT_SZ_SUPPLY_DEMAND` | T2 | 深圳人才供需评价 | MODEL | 特定产业/技术领域深圳人才供需平衡（缺口或盈余）及趋势。内部默认：第三方供需评价指数， 禁止伪展开「供给−需求」算术（Q-MO-TALENT-09）。与 M_TALENT_SZ_STATUS 分核。 结构化报告壳不进本 ID。禁止 M_CHAIN_BOTTLENECK_TALENT。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 13 | `M_TALENT_UNIV_NEW` | T2 | 高校新培育人才 | MODEL | 目标技术领域高校新增人才培养识别、培养趋势、学科/技术方向与校际对比（05 `.7.3`，自然年）。 04 三句（3–5 年毕业生预测、新专业/研究中心、校企合作）不纳入本核、不另发明 ID（Q-MO-TALENT-05）。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 14 | `M_TALENT_DS_16_TALENT_RECRUIT_005` | T3 | 沟通障碍智能检测 | MODEL | 原文要模型，不是尽调字段。禁止改挂 164/501。无 also_in。不发明 M_*。见 REC-D05。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 15 | `M_TALENT_DS_16_TALENT_RECRUIT_006` | T3 | 文化融合风险评估 | MODEL | 原文要模型。禁止改挂 164。无 also_in。见 REC-D06。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 16 | `M_TALENT_DS_16_TALENT_RECRUIT_007` | T3 | 国际流动壁垒分析 | MODEL | 禁止按号挂 111。157 不顶替。无 also_in。见 REC-D07。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 17 | `M_TALENT_DS_16_TALENT_RECRUIT_010` | T3 | 引进阻力量化评分 | MODEL | 禁止改挂 164 招引推荐指数。501 ≠ 覆盖。智库标法不冲掉 A。无 also_in。见 REC-D10。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 18 | `M_TALENT_DS_16_TALENT_RECRUIT_013` | T3 | 高精度成本模型构建 | MODEL | 禁止改挂 164。智库标法不冲掉 A。无 also_in。不发明 M_*。见 REC-D13。 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 19 | `M_TALENT_DS_16_TALENT_RECRUIT_025` | T3 | 团队组合与协同分析 | MODEL | 对不上 164/165。禁止 160 顶替。禁止按号挂 165。无 also_in。不发明 M_*。见 REC-D25。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 20 | `M_TALENT_BASE_98_1` | TTEMP | 人才基础指标模型构建 | third_party | 人才基础指标模型构建：对应算法库 SRS ALGO-TALENT-BASE-98，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 21 | `M_TALENT_DEEP_156_1` | TTEMP | 重点人才识别模型 | third_party | 重点人才识别模型：对应算法库 SRS ALGO-TALENT-DEEP-156，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 22 | `M_TALENT_DEEP_157_1` | TTEMP | 人才流动追踪模型 | third_party | 人才流动追踪模型：对应算法库 SRS ALGO-TALENT-DEEP-157，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 23 | `M_TALENT_DEEP_158_1` | TTEMP | 高校学院新培育人才模型 | third_party | 高校学院新培育人才模型：对应算法库 SRS ALGO-TALENT-DEEP-158，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 24 | `M_TALENT_DEEP_159_1` | TTEMP | 深圳重点人才优势和短板分析模型 | third_party | 深圳重点人才优势和短板分析模型：对应算法库 SRS ALGO-TALENT-DEEP-159，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 25 | `M_TALENT_DEEP_160_1` | TTEMP | 人才关系链模型 | third_party | 人才关系链模型：对应算法库 SRS ALGO-TALENT-DEEP-160，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 26 | `M_TALENT_DEEP_161_1` | TTEMP | 人才供需分析评价模型 | third_party | 人才供需分析评价模型：对应算法库 SRS ALGO-TALENT-DEEP-161，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 27 | `M_TALENT_DEEP_162_1` | TTEMP | 人才学术力评估模型 | third_party | 人才学术力评估模型：对应算法库 SRS ALGO-TALENT-DEEP-162，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 28 | `M_TALENT_DEEP_163_1` | TTEMP | 人才产业力评估模型 | third_party | 人才产业力评估模型：对应算法库 SRS ALGO-TALENT-DEEP-163，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 29 | `M_TALENT_DEEP_164_1` | TTEMP | 招入人才推荐模型 | third_party | 招入人才推荐模型：对应算法库 SRS ALGO-TALENT-DEEP-164，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 30 | `M_TALENT_DEEP_165_1` | TTEMP | 培育人才布局模型 | third_party | 培育人才布局模型：对应算法库 SRS ALGO-TALENT-DEEP-165，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 31 | `M_TALENT_GRAPH_110_1` | TTEMP | 人才实体识别构建 | third_party | 人才实体识别构建：对应算法库 SRS ALGO-TALENT-GRAPH-110，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 32 | `M_TALENT_GRAPH_111_1` | TTEMP | 人才实体关系抽取 | third_party | 人才实体关系抽取：对应算法库 SRS ALGO-TALENT-GRAPH-111，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
