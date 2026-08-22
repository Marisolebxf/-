# METRIC 赋号包 · 交给算法轨（类型/公式均未签）

> **日期**：2026-08-22  
> **语义 Owner**：`human:淮政玮`  
> **公式 / `algorithm_type` 会签**：`human:唐绍祖`（**未签**；8/25 前不派本包开工，A1 `ALGO-LIB-METRIC-DEPS-L01` 优先）  
> **状态**：`algorithm_type_suggested` = `suggested_unsigned`。唐绍祖可改类型。  
> **禁止**：把本表写入 seed 当已签；标 `D1=aligned`；把 A2 库 `missing` 改 mapped。  
> **不替代** A1 97 叶。

条目 **192**（含 ZHIKU 非红 `ZHIKU-S*` 与四枚 demo_lock）。Question 见 `METRIC-SEMANTIC-QUESTIONS.md`（84 条，Q072+）。

| 叶 | temp / 旧号 | metric_id | 中文名 | reuse_of | 建议类型 | 建议理由 | 口径默认（摘要） | pending_ref |
|----|-------------|-----------|--------|----------|----------|----------|------------------|-------------|
| TOPIC-ENT | TEMP_TOPIC_ENT_TYPE_DIST | M_ENT_TYPE_DIST_TOPIC | 重点企业类型分布 | — | STAT | 名录去重分组计数、占比与环比，无训练 | 统计窗口默认自然年。对象=用户选定产业下企业名录去重。按类型标签分组输出 去重企业数、占当期集合占比、环比。类型字典内部默认=招标四类（外企/高企/小微/上市）， 见 Q-MO-ENT-01；不自动并… | Q-MO-ENT-01 |
| TOPIC-ENT | TEMP_TOPIC_ENT_REGIONAL_COUNT | M_ENT_REGIONAL_COUNT_TOPIC | 区域企业数量规模占比 | — | STAT | 按行政区 GROUP BY 的计数/规模/占比，无模型 | 统计窗口默认自然年。对象=选定产业下名录去重。全国→省→市下钻，输出各区域 企业去重数、规模、占当期集合占比。三级地图可视化不进本核。规模口径见 Q-MO-ENT-02。 不消费展示 M_ENT_RE… | Q-MO-ENT-02 |
| TOPIC-ENT | TEMP_TOPIC_ENT_DOMAIN_DIST | M_ENT_DOMAIN_DIST_TOPIC | 企业领域分布 | — | STAT | 领域分组计数与简单增长率，无训练 | 统计窗口默认自然年。对象=选定产业下名录去重。以年报/专利/产品映射到产业或技术领域后， 按 field_id 分组的企业去重数及该分布的同比增长率。领域分类临时默认与专题产业/技术领域 映射一致，不… | — |
| TOPIC-ENT | TEMP_TOPIC_ENT_TECH_SCORE | M_ENT_TECH_POWER_SCORE | 企业技术力指数 | M_ENT_TECH_POWER_SCORE | MODEL | 多维赋权合成技术力得分，无训练也按评分指数走 MODEL | 内部默认采用 05.3 `.5.5` 五维（技术人才/技术创新/技术转化/技术合作/技术投入） 加权合成 0–100，与 seed M_ENT_TECH_POWER_SCORE 同口径，故 reuse… | Q-MO-ENT-03 |
| TOPIC-ENT | TEMP_TOPIC_ENT_BIZ_SCORE | M_ENT_BUSINESS_POWER_SCORE | 企业商业力指数 | M_ENT_BUSINESS_POWER_SCORE | MODEL | 多维商业力综合评分 | 内部默认采用 05.3 `.5.6` 六维（市场/产品/品牌/技术合作/产业链覆盖/关键环节参与） 合成 0–100，与 seed 同口径，reuse。PCA vs 加权属公式未签，不另造 ID。 0… | Q-MO-ENT-04 |
| TOPIC-ENT | TEMP_TOPIC_ENT_SZ_LIST | M_ENT_SZ_LIST_TOPIC | 深圳企业清单与链中角色 | — | STAT | 清单去重计数加角色标注，角色抽取是基建不是本核算法类型 | 统计窗口默认自然年。选定产业链下深圳企业去重清单，并标注链中角色。 「深圳」内部默认=总部在深圳（与 M_ENT_SZ_COUNT 对象一致，见 Q-MO-ENT-05）； 角色依赖关系抽取（ENT-… | Q-MO-ENT-05 |
| TOPIC-ENT | TEMP_TOPIC_ENT_CITY_COMPARE | M_ENT_CITY_COMPARE_TOPIC | 多城市企业群对标值 | — | MIXED | 平均技术力/商业力派生 MODEL 分，密度为 STAT，捆在一条 ID 拆不开 | 统计窗口默认自然年。深圳企业群 vs 对照城市集合，输出平均技术力、平均商业力、企业密度等 城市聚合值。对照集合内部默认=05 seq 141 全国加权参照（Q-MO-ENT-06），不用 04 北上… | Q-MO-ENT-06 |
| TOPIC-ENT | TEMP_TOPIC_ENT_ATTRACT_SCORE | M_ENT_ATTRACTION_INDEX | 招引推荐指数 | M_ENT_ATTRACTION_INDEX | MODEL | 招引综合评分 Job，不是图算 | G3 Job。内部默认 05.3 `.5.7` 三维（产业相关度/政策匹配度/深圳连接度）综合分， 对象=全国库中与深圳重点产业契合的外部企业；与 seed ATTRACTION_INDEX 同口径，… | Q-MO-ENT-07 |
| TOPIC-ENT | TEMP_TOPIC_ENT_CULTIVATE_SCORE | M_ENT_CULTIVATION_INDEX | 培育推荐指数 | M_ENT_CULTIVATION_INDEX | MODEL | 培育综合评分 Job | G3 Job。内部默认 05.3 `.5.8` 三维（产业相关度/政策匹配度/企业潜力），对象=深圳本地高潜力企业； 与 seed CULTIVATION_INDEX 同口径，reuse。名单规模同核… | Q-MO-ENT-08 |
| TOPIC-ENT | TEMP_TOPIC_ENT_SUPPLY_STRUCT | M_ENT_SUPPLY_STRUCT_TOPIC | 供应链结构指标 | — | GRAPH | 中心性/密度/多级关系均在供应链子图上算 | A 面 G1/G2（CUT-D6 不进 B 面）。对象=目标企业多级供应商/客户网络（Nebula 当前图）。 同核输出供应商数量、距离/稳定性、密度/紧密度、中心性，并支撑断链风险标注。 默认多级（… | — |
| TOPIC-ENT | TEMP_TOPIC_ENT_PAINPOINT | M_ENT_PAINPOINT_TOPIC | 发展痛难点诊断 | — | MODEL | 痛难点识别与报告生成，非计数 | G3 Job。输出问题/瓶颈清单及建议报告（描述、成因、实践、方案）。 诊断维内部默认=05.3 `.5.3` 经营/盈利/效率/人才（Q-MO-ENT-09）， 因此不 reuse Q018 四维的… | Q-MO-ENT-09 |
| TOPIC-ENT | TEMP_TOPIC_ENT_COMPETITIVENESS | M_ENT_COMPETITIVENESS_SCORE | 综合竞争力指数 | M_ENT_COMPETITIVENESS_SCORE | MODEL | 多维赋权综合得分 | 内部默认 05.3 `.5.1` 固定四维（规模/财务/人力/市场）加权 0–100，可与全国对比； 与 seed COMPETITIVENESS_SCORE 同口径，reuse。雷达/排名/短板为同… | Q-MO-ENT-10 |
| TOPIC-TECH | TEMP_TOPIC_TECH_PAPER_PATENT_CNT | M_TECH_PAPER_PATENT_CNT | 技术点论文量 / 专利量 | — | STAT | 名录去重计数，无加权或模型 | 对象为已对齐技术点（entity_type=technology，按 technology_id）。 统计窗口默认累计全量；页上年份筛选为交互壳，不另开 ID。 计量为该点关联论文去重数量与关联专利去… | — |
| TOPIC-TECH | TEMP_TOPIC_TECH_HEAT_INDEX | M_TECH_HEAT_INDEX | 技术热点热度指数 | — | third_party | 九新/实现类 G3 Job（聚类热度），不伪展开我方公式 | 对象为已对齐技术点。对文献/频次做聚类对齐后，输出该点热度指数、增长曲线与热点报告， 并区分短期热点与长期趋势（同核切片，不另造 ID）。页上不做 NER（建图面抽点）。 实现类 G3 Job（05 … | Q-MO-TECH-02 |
| TOPIC-TECH | TEMP_TOPIC_TECH_POTENTIAL_SCORE | M_TECH_POTENTIAL_SCORE | 技术产业化潜力评分 | — | third_party | 九新/实现类潜力评分 Job，不伪展开 | 按 technology_id 输出产业化潜力综合分；多技术雷达/排名/对比报告为同核对比面，不另造 ID。 特征含论文量/专利量（本页 M_TECH_PAPER_PATENT_CNT 作输入材料，不… | Q-MO-TECH-02 |
| TOPIC-TECH | TEMP_TOPIC_TECH_STAGE | M_TECH_STAGE_JUDGE | 技术阶段判定 | — | third_party | 九新/实现类阶段 Job（含未注册 LLM），不伪展开 | 输出选定技术点所处阶段及简要说明（状态、关键瓶颈、发展潜力）。 用户参数嵌入提示词后重跑为同核定制面，不另造 ID。 实现类 G3 Job + LLM 未注册 501（TECH-B03）；不伪展开阶段… | Q-MO-TECH-02 |
| TOPIC-TECH | TEMP_TOPIC_TECH_SZ_ASSESS | M_TECH_SZ_ASSESS | 深圳技术潜力与阶段综合评估 | — | third_party | 九新/实现类深圳综合 Job 包，不伪展开 | 基于深圳切片输出潜力评分、发展阶段、优劣势与建议（问题/机遇/布局/细分同层 Job，不另造 ID）。 潜力/阶段计算复用 M_TECH_POTENTIAL_SCORE / M_TECH_STAGE_… | Q-MO-TECH-01 |
| TOPIC-TECH | TEMP_TOPIC_TECH_BOTTLENECK | M_TECH_CONVERT_BOTTLENECK | 技术转化瓶颈识别 | — | third_party | 九新/实现类瓶颈归因 Job，不伪展开 | 输入 technology_id，标识转化堵点并给出原因与改进建议（清单/报告）。 流程图/时间轴为同叶流程面，无独立统计核。不是历程 CMS。 实现类 G3 Job（05 seq 136）；专家知识… | Q-MO-TECH-02 |
| TOPIC-ORG | TEMP_TOPIC_ORG_INDUSTRY_COVER | M_ORG_INDUSTRY_COVER | 科研机构产业领域覆盖 | — | STAT | 领域去重计数与简单趋势，无训练、无加权指数 | 选定专题科研机构集合（名录去重）在统计窗口（默认自然年）内参与的产业链领域去重个数， 及该覆盖数的同比/环比趋势。对象不含产业服务链「服务机构」。 R-19「各领域参与度」无独立核，不另造 DEPTH… | — |
| TOPIC-ORG | TEMP_TOPIC_ORG_TECH_LAYOUT | M_ORG_TECH_LAYOUT | 科研机构技术领域布局 | — | STAT | 布局为分布计数/占比；综合实力若独立成核则另议（Q-MO-ORG-03） | 所选科研机构在核心学科 / 前沿方向 / 产业技术链上的布局分布（机构×领域计数或占比）。 统计窗口默认自然年；对象=专题科研机构名录去重。 seq 149「各领域科技综合实力」默认并入本核展示面、不… | Q-MO-ORG-03 |
| TOPIC-ORG | TEMP_TOPIC_ORG_NEW_TREND | M_ORG_NEW_TREND | 新增科研机构趋势 | — | STAT | 名录去重计数的时间序列 | 选定产业或技术领域内，统计窗口（默认自然年）内首次进入该范围科研机构名录的机构 去重计数随时间变化。对象仅专题科研机构。禁止因 05 seq 99(4) 混写「服务机构」而改挂 M_SVC_NEW_C… | Q-MO-ORG-01 |
| TOPIC-ORG | TEMP_TOPIC_ORG_ATTENTION | M_ORG_ATTENTION_TREND | 科研关注度 | — | COMPUTE | 由新增数+增速合成关注度，无训练；不是单纯计数 | 由同一选定范围下的新增科研机构数量及其增长速率合成的领域科研关注度趋势（SRS 04 seq 65）。 05 无关注度专叶，与新增动态同叶消费。非检索热度、非政策关注度。 OPEN Round 4 草… | Q-MO-ORG-02 |
| TOPIC-ORG | TEMP_TOPIC_ORG_SZ_STATUS | M_ORG_SZ_STATUS | 深圳科研机构现状解读 | — | MIXED | 报告核混合计数表现与定性解读，拆不开一条纯 STAT/MODEL | 深圳科研机构在选定产业下的优势与不足解读报告，突出关键指标表现。 范围=深圳×选定产业×专题科研机构名录。不重复计算优势专叶与痛难点专叶的覆盖。 评价框架配置壳不是本核。禁止用 M_CHAIN_SZ_… | Q-MO-ORG-04 |
| TOPIC-ORG | TEMP_TOPIC_ORG_COLLAB_CHAIN | M_ORG_COLLAB_CHAIN | 科研合作关系链条 | — | GRAPH | 合作网络、强度、核心节点属图计算 | 以论文、专利等合作记录构建的科研机构合作网络（G1 A 面当前图 / Nebula）， 展示合作强度、合作类型与核心节点。对象=专题科研机构。 不是产业服务图谱，不是区域创新协同指数。强度/类型/中心… | Q-MO-ORG-05 |
| TOPIC-ORG | TEMP_TOPIC_ORG_TECH_SCORE | M_ORG_TECH_SCORE | 科研机构技术力评价与对比 | — | MODEL | 页上是可配置多维评分/对比/排名；实现类 third_party 不改变建议类型 | 用户从技术力指标库多选并设权后，对各专题科研机构计算的技术力得分， 支撑雷达/条形对比与综合排名。05 十叶无专叶，差集 third_party（【算法补】），公式不展开。 禁止改挂服务机构或企业技术… | Q-MO-ORG-06 |
| TOPIC-ORG | TEMP_TOPIC_ORG_ATTRACT_SCORE | M_ORG_ATTRACT_SCORE | 科研机构招引推荐指数 | — | MODEL | 招引优先级评分为适配/评分模型 | 对候选科研机构多维评估后的招引优先级得分；建议名单规模为同核计数展示面，不另造 CNT ID。 G3 Job。内部默认维取 05.4 seq 154（学术影响力 / 科技成果 / 团队实力）。 禁止改… | Q-MO-ORG-07 |
| TOPIC-ORG | TEMP_TOPIC_ORG_CULTIVATE_SCORE | M_ORG_CULTIVATE_SCORE | 科研机构扶持推荐指数 | — | MODEL | 扶持优先级评分为适配/评分模型 | 对深圳本地科研机构评估后的培育/扶持优先级得分及建议名单规模。 「一院一策」为文本，无独立 ID。G3 Job。 内部默认维取 05.4 seq 155（成果 / 经费效率 / 人才结构）。 禁止改挂… | Q-MO-ORG-07 |
| TOPIC-ORG | TEMP_TOPIC_ORG_SZ_ADVANTAGE | M_ORG_SZ_ADVANTAGE | 深圳科研机构优势 | — | MODEL | 相对对照集合的优势识别属评价/模型产出 | 选定产业下深圳科研机构相对全国（或对照集合）的优势分析报告。G3 Job。 内部默认维取 05.4 seq 151（成果 / 经费 / 人才）。指标选择壳不是本核。 不与现状解读核重复算覆盖。 | Q-MO-ORG-08 |
| TOPIC-ORG | TEMP_TOPIC_ORG_PAINPOINT | M_ORG_SZ_PAINPOINT | 深圳科研机构痛难点 | — | MODEL | 痛难点识别属评价/模型产出 | 识别深圳科研机构在选定产业下的痛难点，并给出改进建议与分析报告。G3 Job。 内部默认维取 05.4 seq 152（项目 / 转化 / 人才 / 产业合作）。 禁止用企业痛点 M_ENT_PAIN… | Q-MO-ORG-09 |
| TOPIC-TALENT | TEMP_TOPIC_TALENT_REGIONAL_DIST | M_TALENT_REGIONAL_DIST | 重点人才区域分布 | — | STAT | 名录去重后的地理分布计数与对照，第三方不展开伪 COUNT | 用户选定产业或技术领域下，对重点人才（第三方名录、人才实体去重）按地理单元计数， 并支持多领域并列对照。内部默认：当前快照；地理粒度=国家与省级并列（全球库含境外）； 重点人才集合见 Q-MO-TAL… | Q-MO-TALENT-10 |
| TOPIC-TALENT | TEMP_TOPIC_TALENT_ORG_DIST | M_TALENT_ORG_DIST | 重点人才机构分布 | — | STAT | 前 N 机构人才数与占比，第三方不展开 | 内部默认取招标 04：在高校/院所/企业等类型（用户可筛）下，按人才所属机构聚合， 输出该产业或技术领域内人才最集中的前 N 家机构及其人才数量与占比（名录去重、当前快照）。 05「省/国家拥有的人才… | Q-MO-TALENT-01 |
| TOPIC-TALENT | TEMP_TOPIC_TALENT_SUPPLY | M_TALENT_SUPPLY_STRUCT | 人才供给情况 | — | STAT | 历年序列与存量结构计数，第三方不展开 | 特定领域人才供给的历年变化 + 当前存量结构。内部默认：历年序列用自然年、 学士/硕士/博士毕业数量（05）；存量结构以学历为主；职称/年龄不单列 ID（Q-MO-TALENT-02）。 对象=名录去… | Q-MO-TALENT-02 |
| TOPIC-TALENT | TEMP_TOPIC_TALENT_RELATION | M_TALENT_RELATION_NET | 重点人才关系链结构 | — | GRAPH | 多元关系网络图统计，非 Job、非轨迹 | 论文/专利/组织/项目多源融合后的合作、引用等多元关系网络（节点/边规模等图统计）， 支撑最短路径与节点洞察呈现。G1 当前图（Nebula）。内部默认：路径长度与节点画像不单列 ID （Q-MO-T… | Q-MO-TALENT-08 |
| TOPIC-TALENT | TEMP_TOPIC_TALENT_SZ_STATUS | M_TALENT_SZ_STATUS | 深圳人才现状与优劣势 | — | MIXED | 计数对比与优劣势评价拆不开一条 ID；第三方不展开伪加权 | 统一评价框架下深圳 vs 全国/重点城市的人才横向对比，含计数面（.1）与优劣势/短板面（.7.4）， 一条 MIXED 核不拆（Q-MO-TALENT-07）。供需平衡归 M_TALENT_SZ_S… | Q-MO-TALENT-07 |
| TOPIC-TALENT | TEMP_TOPIC_TALENT_ACADEMIC_SCORE | M_TALENT_ACADEMIC_SCORE | 人才学术力指数 | — | MODEL | 可配权综合评分与排名，禁止伪展开 H 指数 | 用户可组合指标与权重后的人才学术力综合评分、排名与名单对比。内部默认：一条综合指数； 分项维名跟 05（成果数量/学术影响力/专业技能）；04 H 指数/被引/期刊/合作广度作第三方内部特征， 不展开… | Q-MO-TALENT-03 |
| TOPIC-TALENT | TEMP_TOPIC_TALENT_INDUSTRY_SCORE | M_TALENT_INDUSTRY_SCORE | 人才产业力指数 | — | MODEL | 个人产业转化贡献综合评分，第三方不展开 | 特定产业领域内人才个人产业转化贡献的综合评分与排名。内部默认取 04：专利转化/项目/商业化（对象=人）。 05 企业侧「人才综合实力（影响力/产业覆盖/媒体知名度）」不作为本 ID 主口径（Q-MO… | Q-MO-TALENT-04 |
| TOPIC-TALENT | TEMP_TOPIC_TALENT_ATTRACT_SCORE | M_TALENT_ATTRACT_SCORE | 引入人才推荐指数 | — | MODEL | 招引综合推荐分（Job），第三方不展开加权 | 全球库中与深圳产业发展方向契合的外部人才综合推荐分（G3 Job，非 G1 图算）。 名单规模为同核 STAT 面（共 N 人），不另造 CNT ID。分项维与推荐理由不单列（Q-MO-TALENT-… | Q-MO-TALENT-06 |
| TOPIC-TALENT | TEMP_TOPIC_TALENT_CULTIVATE_SCORE | M_TALENT_CULTIVATE_SCORE | 培育人才推荐指数 | — | MODEL | 培育综合推荐分（Job），第三方不展开 | 高成长潜力人才综合培育推荐分 + 建议名单规模（G3 Job）。培育方向建议为文本，无独立 ID。 分项维不单列（Q-MO-TALENT-06）。禁止 M_SVC_REC_* / M_ENT_CULT… | Q-MO-TALENT-06 |
| TOPIC-TALENT | TEMP_TOPIC_TALENT_UNIV_NEW | M_TALENT_UNIV_NEW | 高校新培育人才 | — | MODEL | 高校新增人才识别与趋势模型叶；预测不进本核 | 目标技术领域高校新增人才培养识别、培养趋势、学科/技术方向与校际对比（05 `.7.3`，自然年）。 04 三句（3–5 年毕业生预测、新专业/研究中心、校企合作）不纳入本核、不另发明 ID（Q-MO… | Q-MO-TALENT-05 |
| TOPIC-TALENT | TEMP_TOPIC_TALENT_SZ_SUPPLY_DEMAND | M_TALENT_SZ_SUPPLY_DEMAND | 深圳人才供需评价 | — | MODEL | 供需评价指数（非算术差），第三方不展开 | 特定产业/技术领域深圳人才供需平衡（缺口或盈余）及趋势。内部默认：第三方供需评价指数， 禁止伪展开「供给−需求」算术（Q-MO-TALENT-09）。与 M_TALENT_SZ_STATUS 分核。 … | Q-MO-TALENT-09 |
| TOPIC-TALENT | TEMP_TOPIC_TALENT_FLOW | M_TALENT_FLOW_TRACK | 人才流动追踪 | — | GRAPH | 关系+时间上的流入流出留存，非轨迹引擎 | 区域/行业人才流入、流出、留存的时间序列（自然年）。用关系边+时间属性；禁止 GIS 轨迹引擎。 三面共一条 ID，不拆。04 未单列流动页不影响本核。可与展示 DS-14 迁徙同源，不改挂、不消费展… | — |
| TOPIC-QUERY | TEMP_TOPIC_QUERY_TALENT_STRUCT | M_TALENT_STRUCT_QUERY | 查询结果·人才结构 | — | STAT | 结果集内去重计数与占比，规则匹配字段类型 | 对当前查询命中结果集中的人才实体（talent_id 去重）按结构分箱统计人数与占比， 匹配推荐饼图/柱状。统计窗口=当次查询结果集，不是自然年全量名录、不是 05 人才 13 叶。 默认分箱=最高学… | Q-MO-QUERY-01 |
| TOPIC-QUERY | TEMP_TOPIC_QUERY_ORG_PERF | M_ORG_PERF_QUERY | 查询结果·科研机构绩效 | — | STAT | 结果集内论文数字段聚合，非加权指数 | 对当前查询命中结果集中的科研机构（org_id 去重）按绩效核做推荐聚合，匹配饼图/柱状。 默认核=结果集内关联论文数 COUNT，可按 org_type 分组（Q-MO-QUERY-02）。 不是 … | Q-MO-QUERY-02 |
| TOPIC-QUERY | TEMP_TOPIC_QUERY_TECH_HEAT | M_TECH_HEAT_QUERY | 查询结果·技术热度 | — | STAT | 结果集内词频计数；非 05 热点 Job/模型 | 对当前查询结果集中的技术术语/主题做词频统计，以热力图或词云呈现热点。 默认分母=结果集内 term 频次 TF，不做全域 DF（Q-MO-QUERY-03）。 词云/热力图是可视化形态，不另造 ID… | Q-MO-QUERY-03 |
| TOPIC-QUERY | TEMP_TOPIC_QUERY_SVC_DIVERSITY | M_SVC_TYPE_DIST_QUERY | 查询结果·服务类型分布 | — | STAT | 类型分组计数，反映分布而非门户规模 | 对当前查询结果集中的服务机构（org_id 去重）按主数据服务/机构类型字段计数， 反映服务生态多样性。类型字典默认=结果集内 svc_type/org_type（Q-MO-QUERY-04）。 不是… | Q-MO-QUERY-04 |
| TOPIC-QUERY | TEMP_TOPIC_QUERY_INFO_TREND | M_COMMON_INFO_TREND_QUERY | 查询结果·资讯传播趋势 | — | STAT | 时间桶条数计数；非情感/趋势指数 | 对当前查询结果集中的资讯按发布时间自然月桶计数，呈现传播趋势（Q-MO-QUERY-05）。 ELEMENT=COMMON（资讯非七要素助记码）。不是链域全量 M_CHAIN_NEWS_COUNT /… | Q-MO-QUERY-05 |
| DS-01 | TEMP_DS01_FACT_COUNT | M_INNOV_FACTOR_COUNT | 科创要素数量统计 | — | STAT | 名录去重计数 | 选定范围（区域/时间窗/图层过滤）下科创要素去重存量。对象默认含论文、专利、人才、企业、科研机构、服务机构； 会议/期刊/项目/成果无基础指标叶则走 ADS 列表计数，不另造 CNT ID（Q-MO-… | Q-MO-DS01-01 |
| DS-01 | TEMP_DS01_FACT_DIST | M_INNOV_FACTOR_DIST | 科创要素分布比例 | — | STAT | 分类占比 | 当期集合内对象在切面中的占比。默认切面=要素分类（factor_type）；可切区域、层级。 占比=该类计数/当期集合。第三方维不展开。无独立身份歧义，不另造 Q。 | — |
| DS-01 | TEMP_DS01_FACT_GROWTH | M_INNOV_FACTOR_GROWTH | 科创要素增长趋势 | — | STAT | 历史同比/环比，无训练 | 选定要素类型在历史窗口上的增长率与趋势曲线。默认可切日/周/月/季/年，主展示年同比； 环比公式未签。预测不混入本条（见 M_INNOV_FACTOR_FORECAST）。第三方基础指标含环比叙事不展… | — |
| DS-01 | TEMP_DS01_FACT_INFLUENCE_DEGREE | M_INNOV_FACTOR_EDGE_WEIGHT | 要素间影响程度 | — | GRAPH | 关系权重/网络边权 | 科创要素实体间关系权重 / 网络边权，衡量相互作用强弱。对照 seq 116 关系权重。 禁止 M_SYNTH_ELEM_CONTRIB / seq 187 七要素作用强度顶替；禁止改挂 M_SVC_… | — |
| DS-01 | TEMP_DS01_FACT_ASSOC | M_INNOV_FACTOR_RELATION | 要素关联关系 | — | GRAPH | 关系查询 API，非计数核 | 要素间关系查询与可视化结果（边集合/是否存在关系），不是协同指数。 图失败不挡 KPI。禁止 M_SYNTH_COLLAB_* / M_SVC_GRAPH_* 改挂。 | — |
| DS-01 | TEMP_DS01_FACT_SCHOLAR | M_INNOV_SCHOLAR_INFLUENCE | 专家学者影响力 | — | MODEL | 学术力评分，非简单计数 | 专家学者在学术活动/成果/合作网络中的影响程度。内部默认取第三方学术力（seq 162）且不展开公式； 半成品 H 指数/引用/论文数为叙事维，不进本 ID 公式（Q-MO-DS01-02）。 禁止 … | Q-MO-DS01-02 |
| DS-01 | TEMP_DS01_FACT_CONF | M_INNOV_CONFERENCE_INFLUENCE | 会议影响力 | — | MODEL | 热度综合分，非单一计数 | 科技会议的影响程度。内部默认以会议热度为主、投稿数/参与人数为辅的综合分；公式未签。 05 无会议评价专叶，库缺口保持 missing。禁止伪热度公式进 seed。 | — |
| DS-01 | TEMP_DS01_FACT_ORG | M_INNOV_ORG_INFLUENCE | 科研机构影响力 | — | MODEL | 综合科研实力评分 | 科研机构在产出/合作/领域布局上的影响程度。内部默认对照 seq 99 综合科研实力，第三方不展开。 禁止用 M_SVC_ORG_TECH_SCORE 顶替（服务机构 ≠ 科研机构）；禁止 TOPIC… | — |
| DS-01 | TEMP_DS01_FACT_ENT | M_INNOV_ENTERPRISE_INFLUENCE | 企业影响力 | — | MODEL | 企业技术力类评分，禁止改挂 M_ENT_* | 企业作为科创要素在科技创新、成果转化、产业带动上的影响程度。对照 seq 145 技术力（辅 146/97），第三方不展开。 禁止消费展示企业包 M_ENT_*（含 M_ENT_TECH_POWER_… | — |
| DS-01 | TEMP_DS01_FACT_SVC | M_SVC_ORG_TECH_SCORE | 服务机构影响力 | M_SVC_ORG_TECH_SCORE | MODEL | 服务机构技术力评价（B 轨已用 MODEL 取向） | 服务机构的科技服务供给、资源连接、生态支撑。本页不新编 ID：reuse B 轨已有 M_SVC_ORG_TECH_SCORE（seq 179 技术力）。 seed 尚未登记（MCP miss），A2… | Q-MO-DS01-04 |
| DS-01 | TEMP_DS01_FACT_PROJECT | M_INNOV_PROJECT_INFLUENCE | 项目（含课题）影响力 | — | MODEL | 项目效果综合评价 | 科技项目（默认含课题，Q-MO-DS01-03）在数量/资助金额/实施效果上的影响程度。 05 无项目评价专叶，库缺口保持 missing。seq 145 仅把项目库当企业技术力输入，不是本核。 | Q-MO-DS01-03 |
| DS-01 | TEMP_DS01_FACT_PAPER | M_INNOV_PAPER_INFLUENCE | 论文影响力 | — | STAT | 被引/IF 取值或计数，本页不训练 | 论文被引次数 / 影响因子（seq 96 第三方不展开）。国际合作论文比例无专核，挂本条叙事、不另造 ID（SD-FACT-03）。 不是论文篇数（篇数归 M_INNOV_FACTOR_COUNT）。 | — |
| DS-01 | TEMP_DS01_FACT_PATENT | M_INNOV_PATENT_INFLUENCE | 专利影响力 | — | MODEL | 被引与 SEP 综合，非专利件数 | 专利实体影响力。内部默认一条 ID：被引为主、标准必要专利（SEP）数量为辅子项（Q-MO-DS01-05）。 05 无被引/SEP 专叶，库缺口保持 missing。禁止 M_CHAIN_PATEN… | Q-MO-DS01-05 |
| DS-01 | TEMP_DS01_FACT_JOURNAL | M_INNOV_JOURNAL_INFLUENCE | 期刊影响力 | — | MODEL | 期刊评价综合分 | 期刊影响因子/发文量/高被引论文数综合。05 无期刊评价专叶，库缺口保持 missing。 seq 96 影响因子仅为机构筛选输入，不是本核。 | — |
| DS-01 | TEMP_DS01_FACT_CLUSTER | M_INNOV_FACTOR_CLUSTER | 要素聚类 | — | MODEL | 聚类 | 将相似科创要素自动分类归纳的聚类结果（簇标签/簇规模）。库无专叶，保持 missing。 禁止把 seq 96 区域论文「数据处理/聚类分析」一句写成 mapped。 | — |
| DS-01 | TEMP_DS01_FACT_FORECAST | M_INNOV_FACTOR_FORECAST | 监测趋势预测 | — | MODEL | 时序预测 | 基于历史序列预测特定科创要素未来趋势（点预测/区间未签）。库无要素实体时序预测专叶，保持 missing。 禁止 M_SYNTH_ELEM_INDEX 及综合 182/186/189/190 区域指数… | — |
| DS-01 | TEMP_DS01_FACT_ANOMALY | M_INNOV_FACTOR_ANOMALY | 监测异常点识别 | — | MODEL | 异常检测 | 自动识别标记科创要素监测序列上的异常点与突变点。库无监测异常检测专叶，保持 missing。 清洗阶段「异常值剔除」不是本核。 | — |
| DS-01 | TEMP_DS01_EVT_ATTENTION | M_INNOV_EVENT_ATTENTION | 事件关注度 | — | MODEL | 关注度挖掘分，非 CMS 手工、非计数 | 科技事件被关注和讨论的程度，作为重要性分级输入。内部默认=传播/讨论热度，非资讯条数（Q-MO-DS01-06）。 05 无专叶，库缺口保持 missing。禁止 M_CHAIN_NEWS_COUNT… | Q-MO-DS01-06 |
| DS-01 | TEMP_DS01_EVT_INFLUENCE | M_INNOV_EVENT_INFLUENCE | 事件影响力 | — | MODEL | 事件影响强度评分 | 科技事件对行业、区域或舆情的影响强度，作为分级输入。内部默认三角综合、权重未签（Q-MO-DS01-07）。 禁止把要素影响力九子项算进本页。库缺口保持 missing。 | Q-MO-DS01-07 |
| DS-01 | TEMP_DS01_EVT_IMPORTANCE | M_INNOV_EVENT_IMPORTANCE | 事件重要性等级 | — | MODEL | 自动分级模型 | 基于关注度与影响力自动计算高/中/低，供筛选排序并随动态更新。阈值未签（Q-MO-DS01-08）。 SRS L6-2 点名自动分级 → 差集 missing，不是 CMS 手工打标。禁止路径模型重大… | Q-MO-DS01-08 |
| DS-02 | TEMP_DS02_TECH_GRAPH | M_TECH_GRAPH_STRUCT | 技术点网图结构 | — | GRAPH | 子图构图与结构读取，不是名录计数 | 当前 Nebula A 面技术点子图（entity_type=technology）上，按已有技术点计算技术–技术关联， 生成可视化图谱结构。对象=技术点主键去重；边=技术–技术；窗口=当前图快照。 … | — |
| DS-02 | TEMP_DS02_TECH_EDGE_STRENGTH | M_TECH_EDGE_STRENGTH | 技术–技术关联强度 | — | GRAPH | 边权是图属性，不是加权指数合成 | 技术点之间边权重（半成品本五级只消费技术–技术边）。对象=技术–技术边；窗口=当前图快照。 实体–技术点排序强度归 M_TECH_ENTITY_TOP5，不进本号。禁止 seq 116 / M_SVC… | — |
| DS-02 | TEMP_DS02_ENT_TOP5 | M_TECH_ENTITY_TOP5 | 根节点 Top5 关键实体与关联强度 | — | GRAPH | Top-K 截取边权，不是独立评分模型 | 按已有 105 边权截取与当前根技术点关联的 Top5 实体（人/机构/论文/专利）， 卡片含名称、类型、关联强度。不另造排序模型。维护面候选同源不同面，见 TEMP_DS02_MENT_REC_TO… | Q-MO-DS02-01 |
| DS-02 | TEMP_DS02_ENT_PAPER_PATENT | M_TECH_PAPER_PATENT_CNT | 论文量 / 专利量 | M_TECH_PAPER_PATENT_CNT | STAT | COUNT DISTINCT 材料计数 | 技术点对齐的论文去重数量、专利去重数量（材料计数，不进点类型）。 展示页按图谱当前根节点对齐；专题页按选定 technology_id 对齐。窗口=当前库快照全量（无自然年声明则不加时间窗）。 本页是… | Q-MO-DS02-04 |
| DS-02 | TEMP_DS02_ENT_REL | M_TECH_ENTITY_REL | 实体关联关系网 | — | GRAPH | 关系子图读取，不是路径识别 | 以连线或网络图展示与当前技术点相关的实体之间关联。消费 seq 105 关系面，不另开模型。 禁止 seq 116；禁止用 PATH 关键路径顶替。 | — |
| DS-02 | TEMP_DS02_ENT_INFLUENCE | M_TECH_ENTITY_INFLUENCE | 技术点影响力 / 实体优先级 | — | MODEL | 影响力/优先级是评分排序，不是边权截取 | 按影响力等指标自动排序、优先展示重要实体（xlsx 行 19）。 关联强度排序已由 M_TECH_ENTITY_TOP5 覆盖，本号不重复边权 Top-K。 05 无「技术点关联实体优先级」专叶 → … | Q-MO-DS02-03 |
| DS-02 | TEMP_DS02_PATH_CENTRALITY | M_TECH_PATH_CENTRALITY | 中心度 | — | GRAPH | 路径中心性偏 GRAPH，不是综合维工作台或供应链中心性 | 节点在技术点网中的核心程度；作为关键节点识别输入（xlsx 行 17）。 对象=技术点节点；窗口=当前图快照。偏 GRAPH（度/介数/PageRank 公式未签，不拆子号）。 禁止 mapped s… | — |
| DS-02 | TEMP_DS02_PATH_KEYNODE | M_TECH_PATH_KEYNODE | 关键节点重要性 | — | GRAPH | 图上关键节点识别与标记，不是产业链关键环节计数 | 按中心度、影响力自动识别关键节点并特殊样式标记（xlsx 行 20）。放大/变色/图标是同一结果的前端壳。 禁止改挂 seq 131 深圳链；禁止 M_CHAIN_KEY_NODE_COUNT。05 … | Q-MO-DS02-02 |
| DS-02 | TEMP_DS02_PATH_PRIORITY | M_TECH_PATH_PRIORITY | 节点优先级 / 重要度 | — | GRAPH | 图节点重要度，与 KEYNODE 分行但同属图识别族 | 图谱节点关键程度，用于识别核心节点（xlsx 行 22）。与 KEYNODE 同识别族、半成品分行： 本号默认=重要度级别（可供筛选）；KEYNODE 默认=识别结果+样式。筛选交互壳不另开 ID。 … | Q-MO-DS02-02 |
| DS-02 | TEMP_DS02_MENT_REC_TOP | M_TECH_ENTITY_TOP5 | 关键实体推荐列表 | M_TECH_ENTITY_TOP5 | GRAPH | 与读面 Top5 同核（边权 Top-K），不是独立推荐模型 | 维护面：按 105 边权截取与当前技术领域相关的 Top 人/机构/论文/专利候选（名称、类型、关联强度）。 与读面 Top5 同源不同面（侧栏 vs 维护候选），policy §3.4 不因展示位置… | Q-MO-DS02-01 |
| DS-03 | TEMP_DS03_TOPIC_HEAT | M_TECH_TOPIC_HEAT | 技术话题热度 | — | MODEL | 关注度/活跃程度评分；差集 third_party·seq 134，本页不计算、不伪展开 | 在用户选定时间窗内，按技术领域关键词/主题聚合的关注度与活跃程度；对象为技术话题（非单一技术点、非产业链热点领域）。本页热力图只读 ADS 已落库结果，对照算法库 05 seq 134，不在本页跑专题… | Q-MO-DS03-02 |
| DS-03 | TEMP_DS03_TECH_MATURITY | M_TECH_MATURITY_LEVEL | 技术成熟度 | — | MODEL | 成熟水平评分/分档；差集 third_party·seq 137，禁产业链成熟度号 | 单一技术从概念到应用转化的成熟水平（连续或分档），作为本页气泡图位置维之一。对象=技术点，不是产业链环节。对照 05 seq 137 成熟度输入；实现类不伪展开。 | Q-MO-DS03-05 |
| DS-03 | TEMP_DS03_TECH_STAGE | M_TECH_LIFE_STAGE | 技术发展阶段 | — | MODEL | 生命周期阶段判定；差集 third_party·seq 137，禁 CHAIN 阶段号 | 单一技术所处生命周期阶段（内部默认分档：萌芽 / 成长 / 成熟；是否含衰退待算法卡）。作为本页气泡图另一位置维。对照 05 seq 137。与专题 TEMP_TOPIC_TECH_STAGE 默认同… | Q-MO-DS03-03 |
| DS-03 | TEMP_DS03_TECH_SCALE | M_TECH_OUTPUT_SCALE | 技术规模 | — | STAT | ADS 读面体量计数/加总；seq 96 无专名 | 选定时间窗内该技术的成果与应用体量（内部默认不含资金投入——投入走 M_TECH_INVEST_AMOUNT）。ADS 读面计数/加总。禁止用论文量、专利量或技术交易额冒充「技术规模」专名。 | Q-MO-DS03-01 |
| DS-03 | TEMP_DS03_INVESTMENT | M_TECH_INVEST_AMOUNT | 技术投资额 | — | STAT | ADS 资金加总；交易额≠投资额，禁 M_CHAIN_MARKET_SIZE | 选定时间窗内对该技术的资金投入合计（政府专项与社会资本合计；不含技术交易额、不含产业链企业营收合计）。本页气泡大小或地理「投资分布」读 ADS 字段。无窗口/对象歧义到需单独 Q。 | — |
| DS-03 | TEMP_DS03_REL_STRENGTH | M_TECH_REL_STRENGTH | 技术关联强度 | — | GRAPH | 边权重/关系抽取；禁中心度与综合要素贡献改挂 | 技术–技术边上的关联紧密程度，编码为本页弦线图线粗。影响路径=弦上关系流向可视化，不是 DS-02 关键路径，不是中心度 KPI。边权内部默认随 05 seq 105 关系抽取。 | Q-MO-DS03-06 |
| DS-03 | TEMP_DS03_COMPOSITE_SCORE | M_TECH_COMPOSITE_SCORE | 评估综合得分 | — | COMPUTE | 多项加权合成（无训练）；OPEN 草稿曾写 STAT（读面），本 loop 按加权核改建议 COMPUTE，未签 | 对该技术多项评价指标加权后的综合评价结果，供本页读面与下钻报告展示。本页只读 ADS 已落库字段，不跑综合评价 Job，不把 seq 182–191 抄成我方公式。分项与权重未冻。不是专题深圳潜力与阶… | Q-MO-DS03-04 |
| DS-04 | TEMP_DS04_ACHIEVE_VALUE | M_INNOV_ACHIEVE_VALUE | 创新价值 | — | MODEL | 成果条目多维价值评分，非计数 | 统计对象=全球创新成果清单条目（专利/论文/资讯/机构/企业动态等，名录去重以 innov 主键为准）； 产出技术价值、应用价值与潜在影响力的综合分值，供列表排序、分档与重点突出阈值。 窗口=自然年（… | — |
| DS-04 | TEMP_DS04_MONITOR_DISCOVERY | M_INNOV_POINT_DISCOVERY | 创新点发现 | — | MODEL | 自动识别创新点，属模型产出 | 从全球创新监测对象中用模型自动识别「创新点」，产出识别列表与详情。 对象≠技术链热点领域（seq 134）、≠区域综合评价（182–191）、≠ OVERVIEW 成果条目。 | — |
| DS-04 | TEMP_DS04_MONITOR_VALUE | M_INNOV_POINT_VALUE | 创新点价值评估 | — | MODEL | 对发现结果打分，属模型产出 | 对已发现的创新点做价值评估，产出评估分值与价值分析报告。 对象=创新点（依赖 M_INNOV_POINT_DISCOVERY），≠ OVERVIEW 成果清单创新价值。 不得把 501 当成本条已覆盖… | — |
| DS-04 | TEMP_DS04_RT_KPI_BOARD | M_INNOV_KPI_BOARD | 全球创新实时看板指标 | — | STAT | 看板字段计数与比率聚合 | 按专利数量、论文引用率、投资金额等类别切换的全球创新看板计数/比率； 柱/折/饼/热力为同一套数的读面。V1 读 innov/ADS 聚合，不是 05 seq 96 论文/专利公式， 不是 M_CHA… | — |
| DS-04 | TEMP_DS04_RT_IMPACT_SCORE | M_INNOV_IMPACT_SCORE | 创新影响分数 | — | MODEL | 实体节点影响赋分，非图中心性本身 | 对领域知识图谱实体节点做创新影响赋分，展示分数与排名。 不是网络密度/中心度（seq 116（5）），不是服务链图指标，禁止 M_SVC_GRAPH_* / DS-02-PATH 顶替。 | — |
| DS-04 | TEMP_DS04_RT_IMPACT_FORECAST | M_INNOV_IMPACT_FORECAST | 创新影响预测 | — | MODEL | 影响与贡献度预测，属模型；501 仅为实现通道 | 基于图谱与影响分数，预测科技创新对领域创新的积极影响及贡献度（含趋势）。 招标父句「趋势预测和判断」落本叶。实现通道可 501 / pending；未注册不改变差集 missing。 建议类型 MOD… | — |
| DS-04 | TEMP_DS04_CITY_MONITOR | M_INNOV_CITY_MONITOR_GLOBAL | 城市创新数据监控 | — | STAT | 城市看板字段展示与计数 | 全球主要城市的创新基金/投资规模、机构与企业投入、创新成果等看板详情（innov/ADS 读面）。 不是 186「实时监控」，不是湾区 DS-05 / 深圳 DS-06-CITY。 | — |
| DS-04 | TEMP_DS04_CITY_RANK | M_INNOV_CITY_RANK_GLOBAL | 城市创新能力排名 | — | MIXED | 指数合成加排序拆不开一条时标 MIXED | 全球主要城市创新能力名次（可查看计算方法）。对象=城市，宇宙=全球。 对照 05 seq 186 指数排序仅作库叶映射，本页不跑专题 SYNTH Job。 与 M_SYNTH_VIT_RANK（区域创… | Q-MO-DS04-04 |
| DS-04 | TEMP_DS04_CITY_BENCHMARK | M_INNOV_CITY_BENCHMARK_GLOBAL | 城市对标分析 | — | MIXED | 横向对比与单维评分组合 | 多城对比。内部默认：读面标签用招标三维（投入/产出/环境），计算底物跟 186 四维 （科技/产业/人才/政策），不另开三维公式、不改挂 M_SYNTH_VIT_*。见 Q-MO-DS04-01。 | Q-MO-DS04-01 |
| DS-04 | TEMP_DS04_CITY_FACTOR | M_INNOV_CITY_FACTOR_GLOBAL | 城市创新能力要素表现 | — | MIXED | 多要素维评分且与展示标签不完全同构 | 各城在要素维上的量化表现。内部默认：招标例示人才/资金/政策为展示标签， 计算跟 seq 187 要素维，不伪展开为七条 ID，不改挂 M_SYNTH_ELEM_TYPE_SCORE / CONTRI… | Q-MO-DS04-02 |
| DS-04 | TEMP_DS04_CITY_TALENT_INDEX | M_INNOV_CITY_TALENT_INDEX_GLOBAL | 人才创新指数 | — | third_party | 智库外采封装读数，本页不合成（OPEN 曾写 STAT，类型未签） | 综合反映人才在创新活动中的贡献度、影响力与活跃度；调用系统=新型高端智库 / 科技人才智慧服务。 对象=全球城市语境下的人才指数封装读数。不挂 seq 184；不复用 DS-06 深圳重点人才指数。 … | Q-MO-DS04-05 |
| DS-04 | TEMP_DS04_CARRIER_INDEX | M_INNOV_CARRIER_INDEX_GLOBAL | 创新载体创新能力指数 | — | MODEL | 载体综合指数由模型合成 | 对象=创新载体（企业/机构），宇宙=全球。按各载体创新成果数据计算的综合指数（资源/产出/能力）， 可查看方法与权重。不是城市排名，不是 DS-06 深圳载体价值排名，禁止 M_SVC_ORG_TEC… | — |
| DS-04 | TEMP_DS04_CARRIER_RANK | M_INNOV_CARRIER_RANK_GLOBAL | 创新载体多维度排名 | — | MIXED | 同一指数上的三维度名次拆不开时标 MIXED | 总体 / 领域 / 地区三维度名次，依赖同一载体指数。内部默认一条 ID，筛选壳 n/a_ops。 禁止用 CITY 城市排名或 DS-06-CARRIER 顶替。见 Q-MO-DS04-03。 | Q-MO-DS04-03 |
| DS-05 | TEMP_DS05_GBA_FACTOR_STAT | M_INNOV_GBA_FACTOR_STAT | 湾区创新能力因素统计 | — | STAT | 名录/ADS 分组计数与结构占比，无识别模型 | 统计窗口自然年。对象=粤港澳大湾区规划 11 城（广州、深圳、珠海、佛山、惠州、东莞、中山、江门、肇庆、香港、澳门） 合计及分城。对创新资源 / 机构 / 机制 / 环境等促成因素做 COUNT/SU… | — |
| DS-05 | TEMP_DS05_GBA_SWOT_STRENGTH | M_INNOV_GBA_SWOT_STRENGTH | 湾区创新能力优势因素 | — | MODEL | 优势因素识别与影响程度，非简单计数 | 在选定湾区范围下识别 Strengths，给出因素清单、具体表现与影响程度（seq 100）。 禁止把 seq 186/188 区域指数优劣清单当 SWOT。库无 SWOT 专叶 → A 类 miss… | — |
| DS-05 | TEMP_DS05_GBA_SWOT_WEAKNESS | M_INNOV_GBA_SWOT_WEAKNESS | 湾区创新能力短板因素 | — | MODEL | 短板识别+建议，非计数 | 识别 Weaknesses，含表现与改进建议（seq 101）。禁改挂 M_CHAIN_BOTTLENECK_* / M_SVC_CHAIN_BOTTLENECK。 改进建议不改挂 05 seq 14… | — |
| DS-05 | TEMP_DS05_GBA_SWOT_OPPORTUNITY | M_INNOV_GBA_SWOT_OPPORTUNITY | 湾区创新能力机会因素 | — | MODEL | 机会象限识别，库无现成公式 | 识别 Opportunities（政策支持 / 市场需求 / 技术突破 / 国际合作等）及利用建议（seq 102）。 05 综合叶不输出 Opportunities 象限。库 missing 保持。 | — |
| DS-05 | TEMP_DS05_GBA_SWOT_THREAT | M_INNOV_GBA_SWOT_THREAT | 湾区创新能力威胁因素 | — | MODEL | 威胁象限识别 | 识别 Threats（竞争加剧 / 技术壁垒 / 政策变化 / 环境风险等）及应对策略（seq 103）。 禁改挂 M_CHAIN_TECH_BARRIER_*。库 missing 保持。 | — |
| DS-05 | TEMP_DS05_GBA_OUTPUT_VALUE | M_INNOV_GBA_OUTPUT_VALUE | 创新产值 | — | STAT | 产值求和 | 湾区范围内创新活动经济产出规模（seq 106 目录；xlsx 49）。窗口自然年；对象=11 城合计及分城。 内部默认=高技术产业（制造业）增加值（Q-MO-DS05-04）。禁止 mapped 0… | Q-MO-DS05-04 |
| DS-05 | TEMP_DS05_GBA_INNOV_RATIO | M_INNOV_GBA_INNOV_RATIO | 创新比例 | — | STAT | 占比=分子/分母，无训练 | 创新相关量在总体中的占比（xlsx 50）。窗口自然年；对象=11 城。 内部默认分子=创新产值（与 M_INNOV_GBA_OUTPUT_VALUE 同核），分母=区域生产总值（Q-MO-DS05-… | Q-MO-DS05-01 |
| DS-05 | TEMP_DS05_GBA_INVEST | M_INNOV_GBA_INVEST | 创新投入 | — | STAT | 经费求和 | 湾区创新资金投入规模（xlsx 51）。窗口自然年；对象=11 城合计及分城。 内部默认=研究与试验发展（R&D）经费内部支出，不含人力折合全时当量（Q-MO-DS05-05）。 | Q-MO-DS05-05 |
| DS-05 | TEMP_DS05_GBA_TECH_CONTRACT | M_INNOV_GBA_TECH_CONTRACT | 创新技术合同交易额 | — | STAT | 成交金额求和 | 期内技术合同成交金额合计（xlsx 52）。窗口自然年；对象=登记地或履行地落在湾区 11 城的合同，去重合同号。 不含未成交意向。 | — |
| DS-05 | TEMP_DS05_GBA_PATENT_PAPER | M_INNOV_GBA_PATENT_PAPER | 专利及论文数量 | — | STAT | 专利与论文件数加总 | 目录成员「专利及论文数量」（seq 106）；与授权量分列。窗口自然年；对象=申请人/第一完成单位在湾区 11 城。 内部默认加总 COUNT(专利)+COUNT(论文)；授权量走 M_INNOV_G… | Q-MO-DS05-03 |
| DS-05 | TEMP_DS05_GBA_PATENT_GRANT | M_INNOV_GBA_PATENT_GRANT | 专利授权量 | — | STAT | 授权专利去重计数 | 期内授权专利件数（xlsx 53），含发明/实用新型/外观，按专利号去重。窗口自然年；专利权人地址或第一专利权人在湾区 11 城。 不是企业第一专利权人口径（≠ M_ENT_PATENT_GRANT_… | — |
| DS-05 | TEMP_DS05_GBA_HOTSPOT | M_INNOV_GBA_HOTSPOT | 湾区创新热点区域 | — | MODEL | 空间聚类/密度识别 | 自动识别并标注大湾区内创新热点；读面给出创新密度与主要创新类型（seq 92）。密度与类型共核，不另造 CNT ID。 不是专题技术前沿领域（05 seq 134），不是区域综合评价（182–191）… | — |
| DS-05 | TEMP_DS05_GBA_CAPACITY_INDEX | M_INNOV_GBA_CAPACITY_INDEX | 粤港澳大湾区创新能力指标 | — | MODEL | 对上区域创新活力综合分析模型（seq 186）读面，不是无模型加权壳 | 对湾区创新资源/机构/机制/环境综合分析得到的总指数（seq 94；xlsx 45）。对象=湾区（xlsx 45 误写「城市」不改对象）。 实现对上 05 seq 186 展示读面，不跑 SYNTH-… | Q-MO-DS05-02 |
| DS-05 | TEMP_DS05_GBA_RES_INDEX | M_INNOV_GBA_RES_INDEX | 创新资源指数 | — | MODEL | 同核 186 子维评分 | 总指数子指标「创新资源」（xlsx 44 / seq 96）。随 186 单维评分路径读面，标签「资源」≠ 186「科技」维（Q-MO-DS05-02）。 禁止 reuse M_SYNTH_VIT_D… | Q-MO-DS05-02 |
| DS-05 | TEMP_DS05_GBA_ORG_INDEX | M_INNOV_GBA_ORG_INDEX | 创新机构指数 | — | MODEL | 同核 186 子维评分 | 总指数子指标「创新机构」（xlsx 42）。同核 186 读面。禁止 reuse M_SYNTH_VIT_DIM_SCORE / INDICATOR。 | Q-MO-DS05-02 |
| DS-05 | TEMP_DS05_GBA_MECH_INDEX | M_INNOV_GBA_MECH_INDEX | 创新机制指数 | — | MODEL | 同核 186 子维评分 | 总指数子指标「创新机制」（xlsx 41）。同核 186 读面。禁止 reuse M_SYNTH_VIT_*。 | Q-MO-DS05-02 |
| DS-05 | TEMP_DS05_GBA_ENV_INDEX | M_INNOV_GBA_ENV_INDEX | 创新环境指数 | — | MODEL | 同核 186 子维评分 | 总指数子指标「创新环境」（xlsx 43）。同核 186 读面。禁止 reuse M_SYNTH_VIT_*。 | Q-MO-DS05-02 |
| DS-05 | TEMP_DS05_GBA_SUBINDEX_CONTRIB | M_INNOV_GBA_SUBINDEX_CONTRIB | 子指标贡献度 | — | MODEL | 同核 186 权重/贡献分解 | 四子对总指数的贡献（xlsx 48）。随 186 权重分布读面。禁止 reuse M_SYNTH_VIT_WEIGHT（四维权重）与 M_SYNTH_ELEM_CONTRIB（要素对产业的贡献路径，口… | Q-MO-DS05-02 |
| DS-06 | TEMP_DS06_CITY_COMPARE | M_INNOV_CITY_COMPARE_SZ | 深圳科技发展指标对比 | — | MIXED | 横向对比与 186 单维评分组合，拆不开一条 | 对象=深圳市与选定对标城市（国内主要城市 + 国际创新城市），不是载体、不是湾区 11 城、不是专题 SYNTH 对比集合。 窗口=自然年（内部默认）。产出横向对比与单维/分项评分。 内部默认：计算底… | Q-MO-DS06-01 |
| DS-06 | TEMP_DS06_CITY_RANK | M_INNOV_CITY_RANK_SZ | 深圳城市科技发展排名 | — | MIXED | 名次依赖综合指数排序，与指数读面同核但分条 | 深圳在综合科技发展指数上的全国或全球名次。对象=城市；宇宙=深圳 vs 对标，不是全球城市创新能力榜。 窗口=自然年。排序底物=本页 M_INNOV_CITY_INDEX_SZ（186 活力指数读面）… | — |
| DS-06 | TEMP_DS06_CITY_INDEX | M_INNOV_CITY_INDEX_SZ | 深圳创新能力指数 | — | MIXED | 随 186 综合指数读面（加权合成 + 展示维），公式未签 | 衡量深圳在创新资源、创新主体、创新环境等方面综合水平的指数值；本页排名底物。 对象=深圳（可并列对标城指数值）。窗口=自然年。随 186 活力指数读面，不跑专题 Job。 不是 CARRIER 行56… | — |
| DS-06 | TEMP_DS06_CITY_COMPETE | M_INNOV_CITY_COMPETE_SZ | 深圳科技竞争力 | — | MIXED | 优劣/潜力/水平分析与 186 报告读面组合，四子项不拆号 | 对深圳市科技竞争力的分析读面：优势领域、薄弱环节、发展潜力、发展水平。四子项共核一条 ID，不拆四号（Q-MO-DS06-03）。 对照 seq 186「优势与短板分析报告」+ 模型目的「发展潜力」。… | Q-MO-DS06-03 |
| DS-06 | TEMP_DS06_CITY_TALENT_INDEX | M_INNOV_CITY_TALENT_INDEX_SZ | 深圳重点人才指数 | — | third_party | 智库外采封装读数，本页不合成（OPEN 曾写 STAT，类型未签） | 综合反映深圳重点人才质量、活跃度与贡献度。调用系统=新型高端智库 / 科技人才智慧服务；本页只读封装数，不在 display 合成。 对象=深圳重点人才（不是 186 人才维评分，不是 seq 130… | Q-MO-DS06-02 |
| DS-06 | TEMP_DS06_CITY_TREND | M_INNOV_CITY_TREND_SZ | 深圳与对标城市趋势 | — | MIXED | 历史序列与未冻预测共核，拆不开一条 | 深圳与对标城市科技发展指标的历史变化趋势和未来预测，共核一条 ID（内部默认不拆 HIST/FORECAST）。 05 seq 186 已列区域趋势分析/趋势预测 → 差集 mapped 保持。预测算… | — |
| DS-06 | TEMP_DS06_CARRIER_VALUE_RANK | M_INNOV_CARRIER_VALUE_RANK_SZ | 深圳创新载体创新价值排名 | — | MODEL | 载体创新价值由模型合成后排序，非计数 | 对象=深圳创新载体（高校 / 研究机构 / 企业 / 工作室），不是城市、不是区域、不是全球载体榜。 按各深圳载体创新成果等数据计算的创新价值名次，供识别高价值载体；详情页与筛选键「创新价值」、对比视… | — |
| DS-06 | TEMP_DS06_IND_KPI_BOARD | M_INNOV_KPI_BOARD_SZ | 深圳科技发展指标看板 | — | STAT | 看板字段计数与比率聚合 | 从论文、期刊、专利、专家学者、会议、组织机构、课题、项目、资金、政策、基础设施等维度切换查看的深圳科技发展指标计数/比率； 图表（柱/折/饼/雷达）、字面时序、字面多指标/多时段对比、详情口径为同一套… | — |
| DS-06 | TEMP_DS06_DOMAIN_KPI | M_INNOV_DOMAIN_KPI_SZ | 深圳科技领域明细指标 | — | STAT | 分领域计数/金额聚合 | 各科技领域的企业数量、专利数量、研发投入、人才数量（分领域 ADS 明细表）。四字段不拆正式 M_*。 对象=深圳市各科技领域，不是 INDICATOR 十一维，不是 182–185 区域综合评价，不… | — |
| DS-07 | TEMP_DS07_SCI_PAPER | M_INNOV_SCI_PAPER | 科学论文数量 | — | STAT | 论文去重计数与历史分布 | 特定领域科学论文发表数量；按年/季/月、研究机构、地域看分布与历史变化（柱/折）。 对象≠专利计数。本条「趋势」=已落库计数的历史图表，不是 seq 139 预测。 只消费 05 seq 96 论文项… | — |
| DS-07 | TEMP_DS07_SCI_CENTRALITY | M_INNOV_SCI_CENTRALITY | 科学网络中心性 | — | MIXED | 三类中心性（GRAPH）与排名读面同核拆不开 | 科学合作网络中学者、研究机构的度中心性、接近中心性、中介中心性 + 网络图谱与中心性排名。 对照 116（5）中心度 +（3）可视化 +（2）人物关系。104/105 无中心性计算 → 不对上。 三类… | Q-MO-DS07-02 |
| DS-07 | TEMP_DS07_SCI_FRONTIER | M_INNOV_SCI_FRONTIER | 科学研究前沿性 | — | MODEL | 前沿/热点识别评分；第三方不展开、不改挂专题热度号 | 文献计量与引文网络识别领域研究前沿/热点；主题时间演变与空间分布。 对照 seq 134 实现类（TOPIC-TECH-05 同叶 third_party），本页不跑专题 Job、不伪展开公式。 96… | — |
| DS-07 | TEMP_DS07_SCI_FORECAST | M_INNOV_SCI_FORECAST | 科学创造力趋势预测 | — | MODEL | 时序预测+区间，非历史折线 | 基于历史与算法模型预测特定领域科学创造力未来趋势，展示预测结果与置信区间。 05 无专叶。详设 04 **未**给本页 501。赋号 ≠ 覆盖证明；差集 **missing 保持**。 禁止 also… | — |
| DS-07 | TEMP_DS07_TINN_PATENT_COUNT | M_INNOV_TINN_PATENT_COUNT | 专利数量 | — | STAT | 专利去重计数与分布 | 特定领域专利申请和授权数量；按时间、技术类别、地域、申请人分布；柱/折看变化。 对照 96（5）（6）（7）。默认一条 ID、申请/授权为切片（Q-MO-DS07-03 / TINN-B03）。 **… | Q-MO-DS07-03 |
| DS-07 | TEMP_DS07_TINN_PATENT_QUALITY | M_INNOV_TINN_PATENT_QUALITY | 专利质量 | — | MODEL | 单件专利质量评分，非件数 | 引文 / 权利要求 / 家族专利分析；被引次数、权利要求数量、家族规模的分布与排名，识别高质量专利。 05 无专叶。禁止 96（8）领先机构 / 182 高价值专利分项 / 186 专利成果质量顶替。… | — |
| DS-07 | TEMP_DS07_TINN_MARKET | M_INNOV_TINN_MARKET | 技术市场潜力 | — | MODEL | 市场活动潜力评分；第三方不展开、不改挂专题潜力号 | 基于专利转让、许可、诉讼等市场活动，看市场活跃度、技术成熟度、商业化前景。 对照 seq 135 实现类（专题已 third_party 同叶）；本页不跑 TOPIC-TECH Job、不伪展开三维加… | — |
| DS-07 | TEMP_DS07_TINN_COMPOSITE | M_INNOV_TINN_COMPOSITE | 技术创新力综合评估 | — | MODEL | 多维加权综合分，权重未签 | 将本页规模/质量/潜力等按用户自定义权重计算综合得分。05 无「技术创新力综合」专叶。 自定义权重是交互壳，不另开 n/a_ops。禁止硬挂 182（会吞 SCI-CREATE）/ 186 / 190… | — |
| DS-07 | TEMP_DS07_TINN_FORECAST | M_INNOV_TINN_FORECAST | 技术创新趋势预测 | — | MODEL | 时序预测+区间；501 未注册不得当 mapped | 基于历史与算法模型预测特定领域技术创新力趋势 + 置信区间。 详设「趋势预测可 501」= **实现通道**，未注册；**501 pending 不是覆盖证明**，差集 **missing 保持**，… | — |
| DS-07 | TEMP_DS07_POT_INPUT | M_INNOV_POT_INPUT | 产业投入 | — | STAT | ADS 金额/强度聚合，无训练 | 特定产业内企业研发投入、固定资产投资、人才投入；按规模/地域/时间看结构与趋势。ADS 统计读面。 禁止 mapped 05 seq 146 企业商业力 / 187 资金要素。禁止 reuse M_C… | — |
| DS-07 | TEMP_DS07_POT_MATURITY | M_INNOV_POT_MATURITY | 技术产品成熟度 | — | MODEL | 成熟度曲线评估；第三方不展开、不改挂链/专题阶段号 | 技术生命周期 / 市场渗透率，评估产业内技术或产品成熟度；成熟度曲线。 对照 seq 137 实现类（TOPIC-TECH-05 同叶 third_party）；本页不跑专题 Job。 禁止 B 轨成… | — |
| DS-07 | TEMP_DS07_POT_OUTPUT | M_INNOV_POT_OUTPUT | 产业产值 | — | STAT | ADS 产值/增加值聚合 | 特定产业总产值、增加值、利润；按时间/地域/企业类型看趋势。ADS 经济统计读面。 禁止 mapped 05 seq 148。禁止 reuse M_CHAIN_REG_REVENUE / MARKET… | — |
| DS-07 | TEMP_DS07_POT_SCI_INFL | M_INNOV_POT_SCI_INFL | 产业科学影响力 | — | MODEL | 产业科学影响力评分，非论文篇数 | 基于论文引用、国际合作评估**产业**科学影响力；被引次数、国际合作论文比例的分布与排名。 05 无专叶。182「学术影响力」是区域科技成果分项，对象不符。禁止 also_in DS-01-FACTO… | — |
| DS-07 | TEMP_DS07_POT_TECH_INFL | M_INNOV_POT_TECH_INFL | 产业技术影响力 | — | MODEL | 产业技术影响力评分，非单件专利质量 | 基于专利引用、技术标准评估**产业**技术影响力；专利被引、标准必要专利数量分布与排名。 05 无专叶。企业技术力 seq 145 对象=企业。≠ TINN 专利质量（单件 vs 产业）。 禁止 re… | — |
| DS-07 | TEMP_DS07_POT_COMPOSITE | M_INNOV_POT_COMPOSITE | 产业发展潜力综合评估 | — | MODEL | 五项加权综合分，权重未签 | 将投入/成熟度/产值/科学影响力/技术影响力按自定义权重计算综合得分与排名。 对照 183：成果三维（产品服务/企业/服务机构）≠ 本页潜力五项，对象不对 → **对不上**。 禁止伪 mapped … | — |
| DS-07 | TEMP_DS07_PG_GUIDE | M_INNOV_PG_GUIDE | 发展战略引导力 | — | MODEL | 引导力三性评分，公式未签 | 收集领域发展战略规划、产业政策文件，评估战略规划的前瞻性、系统性、针对性； 查看关键内容、实施路径、预期目标。政策 9 叶无引导力专叶。三性默认一条 ID（Q-MO-DS07-05 / PG-B03）… | Q-MO-DS07-05 |
| DS-07 | TEMP_DS07_PG_INTENSITY | M_INNOV_PG_INTENSITY | 政策扶持力度 | — | MIXED | 广度+深度合成力度读面，对照 167 不展开 | 评估政策扶持的广度与深度。对照 05 seq 167 力度指数（覆盖≈广度，效果/成本≈深度）。 默认一条 MIXED（Q-MO-DS07-04）。xlsx 行85「资金支持强度」归 FUND，不把 … | Q-MO-DS07-04 |
| DS-07 | TEMP_DS07_PG_COUNT_DIST | M_INNOV_PG_COUNT_DIST | 政策数量类型与覆盖分布 | — | STAT | 件数/类型/覆盖分布计数 | 政策数量、类型、覆盖面；按财税/人才/金融、时间、地域看分布。对照 seq 100 基础指标。 覆盖面≠产业适配（不重列 E7 missing 的 M_POLICY_INDUSTRY_FIT）。 禁止… | Q-MO-DS07-01 |
| DS-07 | TEMP_DS07_PG_FUND | M_INNOV_PG_FUND | 经费支持 | — | STAT | ADS 经费金额聚合 | 科研经费、产业基金、补贴资金；按来源/方向/时间看结构与趋势。原文是计数可视化，未点名评估模型。 05 力度成本维≠经费台账。禁止 missing「库无经费叶」。禁止 mapped 167/185。 … | Q-MO-DS07-01 |
| DS-07 | TEMP_DS07_PG_PROJECT | M_INNOV_PG_PROJECT | 项目支持 | — | STAT | ADS 项目件数与资助额聚合 | 科技项目、产业项目数量与资助金额分布。原文并列的「实施效果」当**项目记录字段**，不是 seq 156 政策效果模型（PG-B06）。 禁止 mapped 168 / 科研机构 155。禁止 reu… | Q-MO-DS07-01 |
| DS-07 | TEMP_DS07_PG_EFFECT | M_INNOV_PG_EFFECT | 政策实施效果 | — | MIXED | 前后对比读面与 168 效果指数同核拆不开 | 基于实施后数据变化评估实际效果；实施前后关键指标对比。对照 seq 168。半成品行66「政策效果评估值」同核。 默认一条 MIXED（Q-MO-DS07-06）。E7 已 mapped 同叶 → 不… | Q-MO-DS07-06 |
| DS-07 | TEMP_DS07_PG_COMPOSITE | M_INNOV_PG_COMPOSITE | 政策与条件保障力综合评估 | — | MODEL | 保障力五项加权综合分，权重未签 | 将引导力、扶持力度、经费、项目、效果按自定义权重计算综合得分与排名。 政策 9 叶无保障力综合专叶。185=区域政策创新成果指数（数量/类型/效果），对象不符。 禁止 mapped 167/168/1… | Q-MO-DS07-01 |
| DS-08 | TEMP_DS08_RANK_SCORE | M_INNOV_SCIINDEX_RANK_SCORE | 科技成果综合得分与名次 | — | STAT | 页上对已发布分值排序/名次差，不在本页做加权合成 | 展示科技成果综合排名榜单：前 N 名、综合得分、较上一期升降。 分类切面（领域/成果类型/机构类型/地域）、历史名次曲线、多成果对比均消费同一套已落库分值/名次 （注释 TEMP_RANK_SCORE… | Q-TINDEX-01 |
| DS-08 | TEMP_DS08_TINDEX_VALUE | M_INNOV_SCIINDEX_VALUE | 科技指数值（含区域分布读数） | — | STAT | 页上读已发布指数，不在本页做指数合成 | 已发布「科技指数」数值本身；GIS 热力/区域图（seq 165 / xlsx 92–93）落同一读数 （注释 TEMP_TINDEX_VALUE 不是额外 ID）。对象=指数空间切面，不是 186 … | Q-MO-DS08-01 |
| DS-08 | TEMP_DS08_VIZ_INFLUENCE | M_INNOV_SCIINDEX_INFLUENCE | 科技影响力趋势 | — | STAT | ADS 时序聚合，页上无训练、无预警模型 | 科技影响力随时间的折线/面积读数（xlsx 91）；可按时间范围、领域切换，支持多指标并排。 原文=字面读 ADS 时序，未点名预测模型。影响力统称口径见 Q069 / Q071（待登，不另开 A）。… | Q069 |
| DS-08 | TEMP_DS08_VIZ_HINDEX | M_INNOV_EXPERT_HINDEX | 专家H指数排行 | — | third_party | 外采专家 H 指数只读，本页不自算 Hirsch | 柱/雷达展示专家 H 指数排行；可按学科/机构/地域筛选。对象=专家，不是 RANK 科技成果榜。 对照 05 seq 162 人才学术力分项含 H。实现类 third_party，禁止伪展开 Hir… | Q-MO-DS08-02 |
| DS-08 | TEMP_DS08_VIZ_ACTIVITY | M_INNOV_EXPERT_ACTIVITY | 专家科研活跃度 | — | third_party | 外采成果数量/动态只读，本页不自算活跃度合成 | 热力/时间轴展示专家科研活跃读面。内部默认分子=论文数量（对照 162 成果数量/动态更新）； 项目数/学术活动参与度 05 无专核 → VIZ-B02 叙事，不另开 A、不进本公式（Q-MO-DS0… | Q-MO-DS08-03 |
| DS-09 | TEMP_DS09_COMP_HEAT | M_INNOV_PLAN_HEAT | 热度指数 | — | MIXED | 134 外采/实现类热度核 + 规划页周期/列表切片拆不开一条 | 热门技术领域在当前周期内的受关注程度与活跃水平。宿主=综合发展规划「全球热点技术捕捉」 （自动识别热门领域 + 热点列表）。对象=技术领域，不是论文/专利条目计数，也不是专题页单一 technolog… | — |
| DS-09 | TEMP_DS09_COMP_GROWTH | M_INNOV_PLAN_GROWTH | 增长速度 | — | MIXED | 随 134 趋势读面，非单纯计数、非本页预警模型 | 热门技术领域的发展速度与增长变化。⊂ 134 研究热度/趋势读面。宿主仍是 seq 178，不是独立 A、不是 seq 184 预警。 专题 M_TECH_HEAT_INDEX 把增长曲线作同核切片不… | — |
| DS-09 | TEMP_DS09_COMP_LOCAL_ADV | M_INNOV_PLAN_LOCAL_ADV | 本地科技创新特色与优势 | — | MODEL | 本地优势识别与全球对比，非计数 | 本地优势领域、创新资源分布，及与全球水平对比。对象=规划页「本地」区域（Q-MO-DS09-01：用户选定规划区域， 未选时内部默认深圳）。不是深圳城市竞争力拆项（xlsx 60–63 / DS-06… | Q-MO-DS09-01 |
| DS-09 | TEMP_DS09_COMP_TALENT_FLOW | M_INNOV_PLAN_TALENT_FLOW | 科技人才流动（产业界↔学术界） | — | MODEL | 产学流动趋势与预警，非区域迁徙图统计 | 核心技术人才在产业界和学术界之间的流动趋势 + 预警。对象≠ M_TALENT_FLOW_TRACK（专题：区域/行业流入流出留存，GRAPH）， ≠ 人才 05 seq 157（社交/招聘区域或行业… | Q-MO-DS09-02 |
| DS-09 | TEMP_DS09_COMP_DIRECTION_ALERT | M_INNOV_PLAN_DIRECTION_ALERT | 潜在科技发展方向预警 | — | MODEL | 多源方向预警属模型；501 仅为实现通道 | 结合论文、专利、项目、人才、产业和政策多源，对潜在科技发展方向持续监测与预警。 招标父句「潜在的科技发展方向预警」收口本叶。对象≠ 134 已识别热点的趋势预测，≠ M_INNOV_IMPACT_FO… | — |
| DS-09 | TEMP_DS09_RES_OVERLAP | M_INNOV_RES_OVERLAP | 研究领域重叠度 | — | MODEL | 两企研究领域重叠计算，非图相似度 API、非区域协同指数 | 基于企业－专家－学术文献－研究关键词知识图谱，衡量两家企业在研究领域上的重叠程度，产出计算结果与可视化。 对象≠ 05 seq 191 区域创新协同（完整度/中心度/密度），≠ 116 两实体通用语义… | — |
| DS-09 | TEMP_DS09_RES_GRADE | M_INNOV_RES_GRADE | 研究领域等级划分 | — | MODEL | 重叠度分档模型，阈值参数面不另造 ID | 对重叠度做量化等级划分；可查看标准与结果，支持自定义阈值。阈值是同一缺口的参数面，不另开 missing。 与 M_INNOV_RES_CI_LEVEL 同族不同核（Q-MO-DS09-03 默认分两… | Q-MO-DS09-03 |
| DS-09 | TEMP_DS09_RES_CI_LEVEL | M_INNOV_RES_CI_LEVEL | 竞争情报等级 | — | MODEL | 竞争情报强弱评分/分档，非简单计数 | 半成品独立主项：用量化指标对重叠度划分等级，反映企业间竞争情报强弱（等级/分值）。 与 GRADE 同族，比对交互归 M_INNOV_RES_CI_COMPARE。覆盖判定跟算法缺口，不改 other… | Q-MO-DS09-03 |
| DS-09 | TEMP_DS09_RES_CI_COMPARE | M_INNOV_RES_CI_COMPARE | 多企业竞争情报比对 | — | MIXED | 情报等级读数 + 竞争矩阵/定位图拆不开一条 | 比对多家企业竞争情报等级，产出竞争矩阵与战略定位图。企业维 11 叶均对不上该输出 （141=深圳 vs 全国竞争力；145 对标=技术力；146 跨企业=商业力）。 禁止 M_CHAIN_COMPE… | — |
| DS-09 | TEMP_DS09_KEYD_SPATIAL | M_INNOV_KEYD_SPATIAL | 空间密度与集聚度 | — | STAT | GIS/ADS 密度与集聚读数，无识别模型 | 创新资源在地理空间上的分布密集程度与集聚水平（xlsx 100/101 共核，不拆两条）。 宿主=区域科技创新空间布局分析。对象=GIS 地理密度，不是协同网络密度（seq 191）， 不是 M_EN… | — |
| DS-09 | TEMP_DS09_KEYD_COMPETITIVENESS | M_INNOV_KEYD_COMPETITIVENESS | 区域科技创新竞争力水平 | — | MIXED | 186 读面分值 + 指标体系/对标拆不开；权重未签 | 规划页区域对象的竞争力水平分值（xlsx 102）+ 指标体系/对标。对照 05 综合 186 活力指数/单维评分（语义，不是展示序号 186）。 与 SYNTH-VITALITY / DS-04-C… | Q-MO-DS09-04 |
| DS-09 | TEMP_DS09_KEYD_POTENTIAL | M_INNOV_KEYD_POTENTIAL | 区域科技创新发展潜力 | — | MIXED | 同核 186 潜力面 + 规划页读面切片 | 同上叶的发展潜力评分（xlsx 103；186 正文含发展潜力）。对象=区域，不是某项技术的产业化潜力 （M_TECH_POTENTIAL_SCORE / 技术链 135），不是 DS-07 产业发展… | Q-MO-DS09-04 |
| DS-09 | TEMP_DS09_KEYD_LAND | M_INNOV_KEYD_LAND | 土地创新产出效益与利用效率 | — | STAT | GIS/ADS 用地效益与效率读数 | 土地利用类型上的创新产出效益（xlsx 104）与土地利用效率（xlsx 105）共核，不拆两条。 宿主=土地用途与效益分析。对象=GIS 用地/产出图层，不是要素类型综合评价（综合 187）。 GI… | — |
| ZHIKU | ZHIKU-S1-TASK-TOTAL | ZHIKU-S1-TASK-TOTAL | 我的报告任务总数 | — | STAT | 任务去重计数 | 当前账号下创建的全部报告创作任务数。内部默认：研究/战略/洞察三态合计； 去重=report_task_id；窗口=当前快照。对象=current_user，不是租户全量。 ELEMENT 说明=CO… | — |
| ZHIKU | ZHIKU-S1-TASK-PENDING-REVIEW | ZHIKU-S1-TASK-PENDING-REVIEW | 待发布审核任务数 | — | STAT | 状态过滤计数 | 当前账号下状态=待发布审核的报告任务数。内部默认：status=pending_review 且 owner=current_user。 禁止与全库审核队列混计。 | — |
| ZHIKU | ZHIKU-S1-CASE-TOTAL | ZHIKU-S1-CASE-TOTAL | 案例广场案例总数 | — | STAT | 公开案例去重计数 | 案例广场当前可检索展示的战略咨询成果案例总数。内部默认：visibility=public； 去重=strategy_case_id；当前快照。 | — |
| ZHIKU | ZHIKU-S1-INSIGHT-TOTAL | ZHIKU-S1-INSIGHT-TOTAL | 洞察报告库报告总数 | — | STAT | 公开报告去重计数 | 洞察报告库当前可检索展示的洞察报告总数。内部默认：visibility=public； 去重=insight_report_id。 | — |
| ZHIKU | ZHIKU-S1-MATERIAL-TOTAL | ZHIKU-S1-MATERIAL-TOTAL | 我的素材库文件总数 | — | STAT | 解析完成文件计数 | 当前账号素材库中已上传并完成解析的素材文件数。内部默认：owner=current_user 且 parse_status=done。 | — |
| ZHIKU | ZHIKU-S2-ENTITY-TOTAL | ZHIKU-S2-ENTITY-TOTAL | 科技实体清单总数 | — | STAT | 筛选命中去重计数 | 当前筛选条件下命中的科技实体总数。内部默认：filter_match=true；去重=tech_entity_id；当前快照。 不是 DS-01 科创要素存量，禁止改挂 M_INNOV_FACTOR_… | — |
| ZHIKU | ZHIKU-S2-TREND-TECH-TOTAL | ZHIKU-S2-TREND-TECH-TOTAL | 技术趋势分析·技术总量 | — | STAT | 技术条目去重计数 | 技术趋势分析页宏观统计卡片覆盖的技术条目总数。内部默认：distinct tech_id；当前分析任务结果集。 禁止 reuse M_CHAIN_HOTSPOT_COUNT / DS-02 技术全景 … | — |
| ZHIKU | ZHIKU-S2-TECHSYS-TOTAL | ZHIKU-S2-TECHSYS-TOTAL | 技术体系总数 | — | STAT | 技术体系去重计数 | 当前账号可见的技术体系（树）总数。内部默认：visibility=current_scope；去重=tech_system_id。 树节点展开不另造 ID。 | — |
| ZHIKU | ZHIKU-S2-PAPER-TOTAL | ZHIKU-S2-PAPER-TOTAL | 论文分析总览·论文总数 | — | STAT | 已收录论文去重计数 | 论文分析总览页当前统计口径下的学术论文总数。内部默认：indexed=true；去重=paper_id。 禁止 reuse M_CHAIN_ACADEMIC_POWER（链科研实力指数）。 | — |
| ZHIKU | ZHIKU-S2-PROJECT-TOTAL | ZHIKU-S2-PROJECT-TOTAL | 科研项目统计·项目总数 | — | STAT | 在册项目去重计数 | 科研项目统计分析仪表盘当前口径下的项目总数。内部默认：status!=archived；去重=research_project_id。 | — |
| ZHIKU | ZHIKU-S2-NETWORK-NODE-TOTAL | ZHIKU-S2-NETWORK-NODE-TOTAL | 社会网络分析·节点总数 | — | GRAPH | 关系网分析结果的节点规模，不是普通名录计数 | 社会网络可视化当前分析结果的节点（实体）总数。内部默认：当前图结果 distinct node_id； 边数/社区数/中心性不另造 ID（Q-MO-ZHIKU-03）。禁止 mapped 图谱 API… | Q-MO-ZHIKU-03 |
| ZHIKU | ZHIKU-S3-CLUSTER-TOTAL | ZHIKU-S3-CLUSTER-TOTAL | 聚类分析·簇总数 | — | STAT | 聚类结果簇计数，模型不进本 ID | 当前聚类任务结果中生成的簇（分组）总数。内部默认：distinct cluster_id。 本 ID 只计簇数；聚类模型本身不进本核、禁止另造 ZHIKU-S*。 | — |
| ZHIKU | ZHIKU-S3-HOTSPOT-TOTAL | ZHIKU-S3-HOTSPOT-TOTAL | 技术热点·热点词总数 | — | STAT | 热点词条去重计数，不是链域热点评分 | 当前统计周期内识别出的技术热点词条总数。内部默认：自然日窗口；distinct hotspot_term。 禁止 reuse M_CHAIN_HOTSPOT_COUNT / M_CHAIN_HOTSP… | — |
| ZHIKU | ZHIKU-S3-ALERT-PENDING | ZHIKU-S3-ALERT-PENDING | 动态预警·未处理预警数 | — | STAT | 未处理事件计数 | 状态为未处理的技术动态预警事件数。内部默认：status=pending；去重=tech_alert_id。 | — |
| ZHIKU | ZHIKU-S3-DELPHI-COMPLETION | ZHIKU-S3-DELPHI-COMPLETION | 德尔菲问卷·完成率 | — | STAT | 回收人数比邀请人数 | 当前问卷的专家回收完成率。内部默认：submitted 人数 / invited 人数；当前问卷一张。 分母=已邀请专家，不是注册用户全量。 | — |
| ZHIKU | ZHIKU-S3-ROADMAP-PROJECT-TOTAL | ZHIKU-S3-ROADMAP-PROJECT-TOTAL | 技术发展路线·在建项目数 | — | STAT | 在建路线图项目计数 | 当前技术发展路线图中状态为在建的路线图项目总数。内部默认：status=in_progress； 去重=roadmap_project_id。禁止 reuse M_CHAIN_DEVELOPMENT_… | — |
| ZHIKU | ZHIKU-S4-TALENT-INFLUENCE-SCORE | ZHIKU-S4-TALENT-INFLUENCE-SCORE | 人才关联信息·成果影响力/贡献度得分 | — | COMPUTE | 五维等权合成，无训练 | 学者成果影响力雷达图综合得分。内部默认：被引/合作广度/产出速度/新颖度/权威度五维等权求和（无训练）。 对象=智库人才画像中的学者，不是区域人才支撑指数。 禁止与 🔴 ZHIKU-S4-TALENT… | — |
| ZHIKU | ZHIKU-S4-TALENT-GROWTH-INDEX | ZHIKU-S4-TALENT-GROWTH-INDEX | 人才行为信息·成长指数 | — | COMPUTE | 产出趋势加权指数，无训练 | 学者科研成长轨迹综合指数。内部默认：累计产出趋势加权（无训练）；窗口跟更新频率=月。 禁止 reuse M_ENT_GROWTH_POTENTIAL（企业成长潜力）；禁止并入 DS-13～16。 | — |
| ZHIKU | ZHIKU-S4-TALENT-DOMAIN-NODE-TOTAL | ZHIKU-S4-TALENT-DOMAIN-NODE-TOTAL | 人才库-领域分类·节点总数 | — | STAT | 分类树节点计数 | 九大类人才分类树当前展开范围内的节点（含子类/叶子）总数。内部默认：distinct node_id。 分类树壳不进本 ID。禁止发明 H 指数；禁止并入 DS-13～16。 | — |
| ZHIKU | ZHIKU-S4-TALENT-MAP-DIST-TOTAL | ZHIKU-S4-TALENT-MAP-DIST-TOTAL | 人才地图·分布总数 | — | STAT | 地图命中点去重计数 | 当前地图视图筛选条件下命中的地理分布点总数。内部默认：distinct point_id（人/机构可同点，不拆核；Q-MO-ZHIKU-02）。 禁止并入 DS-13～16 GIS/引进 Job；禁止… | Q-MO-ZHIKU-02 |
| ZHIKU | ZHIKU-S5-ISSUE-TOTAL | ZHIKU-S5-ISSUE-TOTAL | 基础研究问题清单·问题总数 | — | STAT | 已发布问题去重计数 | 基础研究问题清单中已识别/在线发布的问题总数。内部默认：status=published；去重=basic_research_issue_id。 | — |
| ZHIKU | ZHIKU-S5-ISSUE-HEAT-SCORE | ZHIKU-S5-ISSUE-HEAT-SCORE | 问题发展趋势·研究热度/潜力评估得分 | — | MODEL | 热度与潜力评估，不是简单计数 | 单个基础研究问题的研究热度与潜力量化得分。内部默认：一条综合核，热度与潜力不拆新 ZHIKU-S*（Q-MO-ZHIKU-01）。 公式未签；禁止伪展开「时序+文献+成果」为已签模型。 | Q-MO-ZHIKU-01 |
| ZHIKU | ZHIKU-S5-COMPETITION-INDEX | ZHIKU-S5-COMPETITION-INDEX | 竞争格局报告·区域对比指数 | — | COMPUTE | 四维等权区域对比指数，无训练 | 国际/国家/深圳市三层次的研究热度/前沿引领性/投资力度/研究主体总量综合对比指数。 内部默认：四维等权合成（无训练），不另造分项 ID。权重待确认走已有 Q-ZHIKU-04，不新开 Q-MO、不升… | Q-ZHIKU-04 |
| ZHIKU | ZHIKU-S5-DEPLOY-TOTAL | ZHIKU-S5-DEPLOY-TOTAL | 深圳市基础研究部署清单·清单总数 | — | STAT | 部署条目去重计数 | 深圳市基础研究部署清单当前收录的部署条目总数。内部默认：city=深圳；去重=deploy_item_id。 | — |
| ZHIKU | ZHIKU-S5-ORG-CAPABILITY-SCORE | ZHIKU-S5-ORG-CAPABILITY-SCORE | 组织实施分析·核心能力/资源保障得分 | — | COMPUTE | 五维等权合成，无训练 | 学科覆盖/人才品质/机构资源/经费投入/管理机制五维核心能力量化得分。 内部默认：等权求和（无训练）；不另造分项 ID。禁止改挂 M_SVC_ORG_*。 | — |
| ZHIKU | ZHIKU-S3-TREND-FORECAST | ZHIKU-S3-TREND-FORECAST 🔒红 | 发展趋势·预测区间 | — | demo_lock | demo_lock；不赋正式号、不建议生产类型 | 前端演示态趋势外推区间（非算法产出）。保持 🔴；禁止转正、禁止赋正式 M_*、禁止改 mapped、 禁止当生产预测核。差集保持 n/a_ops。 | — |
| ZHIKU | ZHIKU-S4-TALENT-INDEX-SCORE | ZHIKU-S4-TALENT-INDEX-SCORE 🔒红 | 人才指数·综合得分 | — | demo_lock | demo_lock；算法未落地，不赋正式号 | 区域/产业人才支撑能力综合指数（演示态，算法定义卡未落地，§2 序号 76）。 保持 🔴；禁止转正、禁止发明 M_TINDEX_* / M_ZHIKU_* 替换、禁止改 mapped。 与非红 ZHI… | Q-ZHIKU-04 |
| ZHIKU | ZHIKU-S4-TALENT-COCKPIT-ALERT | ZHIKU-S4-TALENT-COCKPIT-ALERT 🔒红 | 人才驾驶舱·统计卡+趋势预测 | — | demo_lock | demo_lock；预测禁止转正，本叶不拆号 | 驾驶舱统计卡 + 趋势预测时间轴。预测部分非算法产出。本叶整枚保持 🔴； 统计卡不在本叶转 🟡；禁止拆新 ZHIKU-S*；禁止并入 DS-13～16。 | — |
| ZHIKU | ZHIKU-S5-EVAL-SCORE | ZHIKU-S5-EVAL-SCORE 🔒红 | 基础研究成果评估·四维量化得分 | — | demo_lock | demo_lock；算法未落地，不赋正式号 | 应用性/理论价值性/创新性/学术影响力四维量化综合评价（演示态，算法定义卡未落地，§2 序号 87）。 保持 🔴；禁止转正、禁止赋正式 M_*、禁止改 mapped。相关债 Q-ZHIKU-04 保持… | Q-ZHIKU-04 |

## 会签时请注意

- 同口径只保留一套 ID（policy §3.4）。已共享：`M_TECH_PAPER_PATENT_CNT`（TOPIC-TECH ↔ DS-02）。
- 专题企业 5 条 reuse 展示 `M_ENT_*`；其余 `VARIANT=TOPIC`。禁止整页改挂 60 个展示 ENT ID。
- 城市/湾区/深圳读面 mapped 186 **不等于** reuse `M_SYNTH_VIT_*`。
- 预测/预警可有正式号 + 建议 MODEL，**501 pending 不是覆盖证明**，差集 missing 保持。
- ZHIKU 四枚红锁不得转正；禁止发明 `M_ZHIKU_*`。

