# 待确认语义列表（METRIC 赋号 loop）

> **工作底稿真源**（本 loop）。客户决策清单对照列 = `qid`（Q072+）。  
> **监管**：`human:淮政玮`（内部默认）。**不升 🟢**（甲方未签）。  
> **公式 / 类型**：建议类型在赋号卡；本表只收 **口径歧义**。

| 状态 | 含义 |
|------|------|
| 🟡 | 已选内部默认，待甲方 |
| ⚪ | 撤销 / 与已有 Q 合并 |

## 登记表（Wave A+B · 84 条 · 2026-08-22 合流）

客户决策清单 §2.aj 已对照 `qid`。详情仍以本表 + 叶级 yaml 为准。

| qid | local_id | 标题 | 来源叶 | metric_id | 选项（摘要） | 内部默认 | 推理依据 | 状态 |
|-----|----------|------|--------|-----------|--------------|----------|----------|------|
| Q072 | Q-MO-ENT-01 | 专题企业类型字典 | TOPIC-ENT-METRIC-OPEN-L01 | M_ENT_TYPE_DIST_TOPIC | A:招标四类（外企/高企/小微/上市）；多标签允许重复计入类型、占比分母仍为企业去重数 · B:并入展示 Q010 六类（再加专精特新/小巨人），并 reuse M_ENT_TYP… · C:类型完全由用户筛选壳传入，本 ID 只做「当前勾选集合」分布 | A | SRS 04 seq 40 明文四类。seed TYPE_COUNT 定义为六类，OPEN 已写「类型字典≠展示 Q010」。 选定产业分布… | 🟡 |
| Q073 | Q-MO-ENT-02 | 区域「规模」口径 | TOPIC-ENT-METRIC-OPEN-L01 | M_ENT_REGIONAL_COUNT_TOPIC | A:数量=企业去重数；规模=该区域企业最新营收合计（缺失则规模面空，不伪造）；占比=区域… · B:规模=从业人员合计 · C:规模与数量同义，只出企业数+占比（实质 reuse M_ENT_REGIONAL_C… | A | seq 41 把数量、规模、占比并列，规模不能默认同义于企业数。营收是 ADS 最近的规模代理； 展示 REGIONAL_COUNT 无规模… | 🟡 |
| Q074 | Q-MO-ENT-03 | 技术力维名（04 指标库 vs 05 五维） | TOPIC-ENT-METRIC-OPEN-L01 | M_ENT_TECH_POWER_SCORE | A:05.3 `.5.5` 五维（人才/创新/转化/合作/投入），reuse M_ENT… · B:SRS 04 seq 43 指标库（专利/引用/研发人员/核心技术覆盖），改挂新号 … | A | 本页算法真源是 05.3 `.5.5` / seq 145，seed 五维与之逐条相同，policy §3.4 同口径须 reuse。 04… | 🟡 |
| Q075 | Q-MO-ENT-04 | 商业力维名（04 vs 05 六维） | TOPIC-ENT-METRIC-OPEN-L01 | M_ENT_BUSINESS_POWER_SCORE | A:05.3 `.5.6` 六维（市场/产品/品牌/技术合作/链覆盖/关键环节），reu… · B:SRS 04 seq 45（营收/利润率/客户集中/品牌声量），改挂新号 M_ENT… | A | 本页算法真源 `.5.6` / seq 146，seed 六维相同。04 的客户集中/品牌声量展示侧无 ODS。 PCA vs 加权留给唐绍… | 🟡 |
| Q076 | Q-MO-ENT-05 | 「深圳相关企业」对象范围 | TOPIC-ENT-METRIC-OPEN-L01 | M_ENT_SZ_LIST_TOPIC | A:总部在深圳（headquarters_city=深圳）且属选定产业链 · B:总部或分支/经营地在深圳 · C:只计数，reuse M_ENT_SZ_COUNT，角色另挂 SZ_CHAIN_POS… | A | 「相关」字面可含分支，但可落地对象与 seed SZ_COUNT 一致=总部在深圳。 本核仍是清单+抽取角色，不是单纯 COUNT，也不 r… | 🟡 |
| Q077 | Q-MO-ENT-06 | 多城市对标对照集合 | TOPIC-ENT-METRIC-OPEN-L01 | M_ENT_CITY_COMPARE_TOPIC | A:05 seq 141 全国加权参照（深圳 vs 全国聚合） · B:SRS 04 seq 48 北京/上海/苏州 · C:改挂展示 Q016 临时集（北京/上海/苏州/广州）并拆 reuse CITY_AV… | A | 本页竞争力/对标算法叶是 seq 141，OPEN 已对照 04 北上苏 vs 05 全国加权。 展示拆成均技术力/密度/未注册均商业力，且… | 🟡 |
| Q078 | Q-MO-ENT-07 | 招引三维名称 | TOPIC-ENT-METRIC-OPEN-L01 | M_ENT_ATTRACTION_INDEX | A:05.3 `.5.7` 产业相关/政策匹配/深圳连接，reuse M_ENT_ATT… · B:SRS 04 seq 49 技术匹配/成长性/区域适配，改挂新号 M_ENT_ATT… · C:reuse demo 快路径 M_ENT_ATTRACT_SCORE | A | 本页 Job 真源 `.5.7` / seq 147，seed INDEX 三维逐条相同。demo ATTRACT_SCORE 是并行快路径… | 🟡 |
| Q079 | Q-MO-ENT-08 | 培育三维名称 | TOPIC-ENT-METRIC-OPEN-L01 | M_ENT_CULTIVATION_INDEX | A:05.3 `.5.8` 产业相关/政策匹配/企业潜力，reuse M_ENT_CUL… · B:SRS 04 seq 51 技术壁垒/市场增速/团队背景，改挂新号 M_ENT_CU… | A | 本页 Job 真源 `.5.8` / seq 148，seed INDEX 三维相同。不 reuse demo CULTIVATE_SCOR… | 🟡 |
| Q080 | Q-MO-ENT-09 | 痛难点诊断维 | TOPIC-ENT-METRIC-OPEN-L01 | M_ENT_PAINPOINT_TOPIC | A:05.3 `.5.3` 经营/盈利/效率/人才，新号 M_ENT_PAINPOINT… · B:SRS 04 seq 55 / Q018 研发/市场/融资/管理，改 reuse M… | A | 本页 Job 真源 seq 143 / `.5.3`。Q018 四维是展示诊断核，OPEN 禁止改挂。 若甲方确认 04=05 同维，再改 … | 🟡 |
| Q081 | Q-MO-ENT-10 | 竞争力评估框架 | TOPIC-ENT-METRIC-OPEN-L01 | M_ENT_COMPETITIVENESS_SCORE | A:05.3 `.5.1` 固定四维（规模/财务/人力/市场），reuse M_ENT_… · B:SRS 04 seq 57 用户自选框架（保持无核，本 ID 只作容器） · C:改挂产业链 M_CHAIN_COMPETITIVENESS_INDEX | A | 自选框架无核（ENT-B11），不能当正式身份。seed 四维与 05 固定框架相同，§3.4 须 reuse。 CHAIN 指数是区域产业… | 🟡 |
| Q082 | Q-MO-TECH-01 |  | TOPIC-TECH-METRIC-OPEN-L01 |  | A:独立号 M_TECH_SZ_ASSESS（深圳综合评估包） · B:不另开号，只消费潜力分 + 阶段判定的深圳地理切片 | A | 检索：OPEN §3.5 写明潜力/阶段计算复用 §3.3/§3.4 核、不发明第二套公式，同时又把 seq 133/138/139/140… | 🟡 |
| Q083 | Q-MO-TECH-02 |  | TOPIC-TECH-METRIC-OPEN-L01 |  | A:third_party（九新/实现类 G3 Job，不伪展开公式） · B:MODEL（页上在算评分/聚类/判定/归因） · C:MIXED（类型轴 + 交付轴拆不开） | A | 检索：OPEN §2 草稿曾写 MODEL；差集与 algo-catalog default_hint 写 third_party； LOO… | 🟡 |
| Q084 | Q-MO-ORG-01 | 新增科研机构的「新增」判定 | TOPIC-ORG-METRIC-OPEN-L01 | M_ORG_NEW_TREND | A:统计窗口内首次进入「选定产业/技术领域 × 专题科研机构名录」的机构去重计数 · B:窗口内新注册 / 新成立的科研机构（不论是否首次进入本页选定范围） · C:窗口内新入库要素库的科研机构（与业务首次出现可能不一致） | A | 05 基础指标(4)与 04 seq 64 都是「选定领域内新增科研机构数量趋势」，语义落在当前筛选范围而非全市新注册。 要素库入库时点与业… | 🟡 |
| Q085 | Q-MO-ORG-02 | 科研关注度是否独立核及合成方式 | TOPIC-ORG-METRIC-OPEN-L01 | M_ORG_ATTENTION_TREND | A:独立 ID；由新增数量+增长速率合成关注度趋势（04 seq 65）；05 未单列专… · B:不独立；仅作为 M_ORG_NEW_TREND 的衍生展示面，作废本 ID · C:独立 ID，但改用检索热度 / 文献关注等非新增口径 | A | TORG-B02：04 要新增数+增速得到关注度，05 未单列。OPEN 已判 mapped 而非 missing。 独立 ID 才能回指 … | 🟡 |
| Q086 | Q-MO-ORG-03 | 布局叶「领域科技综合实力」是否并入布局核 | TOPIC-ORG-METRIC-OPEN-L01 | M_ORG_TECH_LAYOUT | A:并入 M_ORG_TECH_LAYOUT 展示面，不另造 ID；布局核保持分布 ST… · B:另造独立 COMPUTE/MODEL ID（领域科技综合实力） · C:改挂或并入 M_ORG_TECH_SCORE（可配置技术力） | A | TORG-B08：seq 149 输出含「各领域科技综合实力」但 OPEN 明确不另造 ID、不得冒充 §3.7 技术力。 C 违反 tec… | 🟡 |
| Q087 | Q-MO-ORG-04 | 深圳现状解读与优势/痛点专叶是否重复覆盖 | TOPIC-ORG-METRIC-OPEN-L01 | M_ORG_SZ_STATUS, M_ORG_SZ_ADVANTAGE, M_ORG_SZ_PAINPOINT | A:现状解读为独立 MIXED 报告核；优势/痛点专叶另算，本核不重复算覆盖 · B:现状解读只是优势+痛点的容器，废弃 M_ORG_SZ_STATUS · C:三核都算覆盖，允许同一结论在三处重复计数 | A | 04 seq 67 要「优势与不足报告」；05 另有 seq 151/152 专叶。OPEN §3.4 已写专叶不在本条重复算覆盖。 B 会… | 🟡 |
| Q088 | Q-MO-ORG-05 | 合作强度 / 类型 / 核心节点是否拆子 ID | TOPIC-ORG-METRIC-OPEN-L01 | M_ORG_COLLAB_CHAIN | A:一条 GRAPH ID 覆盖网络及强度/类型/核心节点展示面 · B:拆成强度 / 类型 / 中心性三条子 ID | A | TORG-B05：分项无正式 ID。招标叶子是「合作关系链」一条。拆子项会扩出机器卡 11 条，本 loop 不扩。 禁止改挂 M_SYNT… | 🟡 |
| Q089 | Q-MO-ORG-06 | 可配置技术力 vs 综合科研实力 vs 领域科技综合实力 | TOPIC-ORG-METRIC-OPEN-L01 | M_ORG_TECH_SCORE | A:本 ID=用户可配置多机构技术力对比（【算法补】）；综合科研实力非十招标独立叶不另造… · B:用基础指标「综合科研实力」冒充本核 · C:改挂 M_SVC_ORG_TECH_SCORE 或 M_ENT_TECH_POWER… | A | TORG-B03/B07 与 tech_power_ruling：05 无技术力专叶但 ④ 仍出卡；禁止 mapped 到 seq 99(3… | 🟡 |
| Q090 | Q-MO-ORG-07 | 招引 / 扶持推荐指数分项维名（04 vs 05 vs catalog R-*） | TOPIC-ORG-METRIC-OPEN-L01 | M_ORG_ATTRACT_SCORE, M_ORG_CULTIVATE_SCORE | A:内部默认跟 05.4 算法叶——招引 seq 154（学术影响力/科技成果/团队实力… · B:跟 SRS 04 招引维 / 培育维（用户可选指标集） · C:跟 catalog R-16（产业关联/区域互补/科研实力/政策契合）与 R-17（… | A | TORG-B04：三套维名未冻。实现路径已映射 05 `.6.6`/`.6.7`，先跟算法叶才能联调； 04/R-* 差异保留 🟡。名单规模… | 🟡 |
| Q091 | Q-MO-ORG-08 | 深圳科研机构优势对标维 | TOPIC-ORG-METRIC-OPEN-L01 | M_ORG_SZ_ADVANTAGE | A:05.4 seq 151（成果 / 经费 / 人才） · B:04 seq 80 用户自选指标 · C:catalog R-13（成果 / 创新 / 学术影响力 / 合作活跃度） | A | TORG-B09：维名 04≠05≠R-13。与招引/扶持同一策略——先跟已映射算法叶，用户自选是配置壳（n/a_ops）。 | 🟡 |
| Q092 | Q-MO-ORG-09 | 深圳科研机构痛难点诊断维 | TOPIC-ORG-METRIC-OPEN-L01 | M_ORG_SZ_PAINPOINT | A:05.4 seq 152（项目 / 转化 / 人才 / 产业合作） · B:04 seq 82 用户自选业务指标 · C:catalog R-14（投入/转化/人才引进/国际合作）或 R-28（转化率低、人… | A | TORG-B10：维名 04≠05≠R-14/R-28。默认跟已映射痛点模型叶。禁止企业痛点 ID 顶替。 | 🟡 |
| Q093 | Q-MO-TALENT-01 | 机构分布主口径：前 N 机构人才数 vs 区域机构数 | TOPIC-TALENT-METRIC-OPEN-L01 | M_TALENT_ORG_DIST | A:前 N 家机构的人才数量与占比（SRS 04 seq 86–87） · B:每个省/国家拥有的人才机构数（05 seq 98（2）正文） | A | 招标叶子与 04 用户故事是「机构→人才数排名」；05 标题仍是机构分布，正文偏区域机构计数属叙述漂移。 内部默认跟 04，05 机构计数不… | 🟡 |
| Q094 | Q-MO-TALENT-02 | 供给结构维：学历毕业序列 vs 职称/年龄存量 | TOPIC-TALENT-METRIC-OPEN-L01 | M_TALENT_SUPPLY_STRUCT | A:历年学士/硕士/博士毕业数量 + 存量以学历为主（05） · B:存量必须含学历/职称/年龄三切（04 seq 89） | A | 05 有可对上的学位毕业核；04 职称/年龄无专核。不发明职称/年龄结构 ID。历年窗口=自然年（常识，不另开 Q）。 | 🟡 |
| Q095 | Q-MO-TALENT-03 | 学术力分项维名与是否单列 | TOPIC-TALENT-METRIC-OPEN-L01 | M_TALENT_ACADEMIC_SCORE | A:一条综合指数；分项跟 05（成果数量/学术影响力/专业技能），04 H 指数等不展开… · B:按 04 被引/H 指数/期刊影响力/合作广度单列分项 ID | A | 页面核是综合评分+排名；禁止伪展开 H 指数公式。04 分项作第三方内部特征。 | 🟡 |
| Q096 | Q-MO-TALENT-04 | 产业力对象：个人转化贡献 vs 企业人才综合实力 | TOPIC-TALENT-METRIC-OPEN-L01 | M_TALENT_INDUSTRY_SCORE | A:人才个人专利转化/项目/商业化贡献（04；对象=人） · B:企业侧人才综合实力（影响力/产业覆盖/媒体知名度）（05 seq 163） | A | 招标叶子是「人才产业力」，对象是人不是企业。05 企业侧表述视为实现侧特征漂移，不改挂企业指标、不发明转化率 ID。 | 🟡 |
| Q097 | Q-MO-TALENT-05 | 高校新培育是否包含预测/新兴/校企专核 | TOPIC-TALENT-METRIC-OPEN-L01 | M_TALENT_UNIV_NEW | A:仅 05：新增识别、培养趋势、学科/技术方向、校际对比 · B:必须含 04 三句：3–5 年毕业生预测、新专业/研究中心、校企合作（并单列） | A | 产品叶已对上 `.7.3`。04 三句 05 未单列专核；不另开 A 类、不发明预测/新兴/校企 ID。 | 🟡 |
| Q098 | Q-MO-TALENT-06 | 引入/培育分项维与建议文本是否单列 ID | TOPIC-TALENT-METRIC-OPEN-L01 | M_TALENT_ATTRACT_SCORE, M_TALENT_CULTIVATE_SCORE | A:各一条综合指数；名单规模同核 STAT 面；分项与建议文本不单列 · B:招引四维、培育四维及推荐理由/培育建议各自正式 ID | A | OPEN 已禁止发明匹配度/潜力分项。Job 核是综合分。不消费 M_SVC_REC_* / 企业招引培育指数。 | 🟡 |
| Q099 | Q-MO-TALENT-07 | 深圳现状是否拆成计数 + 优劣势两条 ID | TOPIC-TALENT-METRIC-OPEN-L01 | M_TALENT_SZ_STATUS | A:一条 MIXED（计数对比 + 优劣势/短板）；供需仍走独立 ID · B:拆成现状计数 ID 与优劣势评价 ID | A | 05.5 把深圳现状收口到 `.1`+`.7.4` 同一招标叶子；MIXED 且拆不开时本 loop 要求进 Question。 供需已有 … | 🟡 |
| Q100 | Q-MO-TALENT-08 | 关系链路径/节点画像是否单列 ID | TOPIC-TALENT-METRIC-OPEN-L01 | M_TALENT_RELATION_NET | A:一条网络结构 ID；最短路径与节点画像为呈现，不单列 · B:路径长度、节点画像各自正式 ID | A | OPEN 禁止发明路径类 ID。G1 核是网络结构；可视化/画像是呈现。不改挂 DS-15。 | 🟡 |
| Q101 | Q-MO-TALENT-09 | 深圳供需：第三方评价指数 vs 供给减需求算术 | TOPIC-TALENT-METRIC-OPEN-L01 | M_TALENT_SZ_SUPPLY_DEMAND | A:第三方供需评价指数（缺口/盈余及趋势），不展开算术差 · B:显式「供给−需求」或预测缺口公式 | A | 05 是供需评价指数；04「供给与需求预测算缺口」若展开成算术差即伪公式。实现类 third_party。 禁止 M_CHAIN_BOTTL… | 🟡 |
| Q102 | Q-MO-TALENT-10 | 「重点人才」分析对象如何圈定 | TOPIC-TALENT-METRIC-OPEN-L01 | M_TALENT_REGIONAL_DIST, M_TALENT_ORG_DIST, M_TALENT_RELATION_NET | A:第三方名录/标签圈定的分析对象集（识别 `.7.1` 仅前置，不单列 ID） · B:必须先跑重点人才识别模型，以其产出集为唯一对象 | A | `.7.1` 非十一招标页、④ 无独立核。区域/机构/关系链的对象默认=名录去重重点人才标签， 识别能力保持 mapped 前置。不发明识别… | 🟡 |
| Q103 | Q-MO-QUERY-01 | 查询结果·人才结构的分箱字典 | TOPIC-QUERY-METRIC-OPEN-L01 | M_TALENT_STRUCT_QUERY | A:仅最高学历 · B:仅职称 · C:仅年龄段 · D:学历为主分箱，职称/年龄为同一 ID 下可切换维 | D |  | 🟡 |
| Q104 | Q-MO-QUERY-02 | 查询结果·科研机构「绩效」核 | TOPIC-QUERY-METRIC-OPEN-L01 | M_ORG_PERF_QUERY | A:结果集内关联论文数 COUNT · B:项目数 · C:经费 · D:加权综合（论文/项目/经费） | A |  | 🟡 |
| Q105 | Q-MO-QUERY-03 | 查询结果·技术热度的分母 | TOPIC-QUERY-METRIC-OPEN-L01 | M_TECH_HEAT_QUERY | A:当前结果集内 term 频次 TF · B:相对查询前全域 DF · C:套用技术链全量热点指数（seq 134 / 链域热点分） | A |  | 🟡 |
| Q106 | Q-MO-QUERY-04 | 查询结果·服务类型字典 | TOPIC-QUERY-METRIC-OPEN-L01 | M_SVC_TYPE_DIST_QUERY | A:结果集内服务机构主数据 svc_type / org_type · B:服务产品类型 · C:与 SVCCHAIN 门户类型码对齐 | A |  | 🟡 |
| Q107 | Q-MO-QUERY-05 | 查询结果·资讯传播趋势的时间桶 | TOPIC-QUERY-METRIC-OPEN-L01 | M_COMMON_INFO_TREND_QUERY | A:自然月 × 资讯条数 COUNT · B:自然年 · C:近 12 个月滚动窗口 · D:关键词权重而非条数 | A |  | 🟡 |
| Q108 | Q-MO-DS01-01 | 要素数量统计是否计入会议/期刊/项目/成果 | DS-01-METRIC-OPEN-L01 | M_INNOV_FACTOR_COUNT | A:计入；无基础指标叶走 ADS 列表计数，不另造 CNT ID · B:不计入主核；仅论文/专利/人才/企业/科研机构/服务机构 · C:四类各造独立 COUNT ID | A | OPEN 已裁定会议/期刊/项目/成果无专叶 → ADS 计数，不改 missing、不膨胀 ID。 检索：pages/DS-01-FACT… | 🟡 |
| Q109 | Q-MO-DS01-02 | 专家学者影响力取第三方学术力还是 H 指数族 | DS-01-METRIC-OPEN-L01 | M_INNOV_SCHOLAR_INFLUENCE | A:第三方学术力（seq 162）不展开；H 指数/引用/论文数为叙事 · B:半成品 H 指数/引用/论文数加权（需公式会签） · C:改挂专题 M_CHAIN_ACADEMIC_POWER | A | 库已列学术力叶 → mapped + 第三方不展开。C 被 OPEN 禁止（链学术力 ≠ 本页学者影响力）。 检索：srs/05 seq 1… | 🟡 |
| Q110 | Q-MO-DS01-03 | 课题是否并入项目影响力对象 | DS-01-METRIC-OPEN-L01 | M_INNOV_PROJECT_INFLUENCE | A:课题并入项目，一条 ID · B:课题与项目拆两条 ID | A | SRS 02 / 半成品将课题并入项目；05 两者皆无评价专叶。拆条会双 missing。待甲方确认机构三拆的另一半不在本 Q（ORG/EN… | 🟡 |
| Q111 | Q-MO-DS01-04 | 服务机构影响力是否等同 B 轨技术力 | DS-01-METRIC-OPEN-L01 | M_SVC_ORG_TECH_SCORE | A:reuse M_SVC_ORG_TECH_SCORE，不新编 · B:口径不同，另造 M_INNOV_SVC_INFLUENCE（可能与 B 轨冲撞） | A | 用户协议 + OPEN impl 指针明确 reuse、不新编冲撞。seed MCP miss、B 轨 catalog 已列。 叙事（供给/… | 🟡 |
| Q112 | Q-MO-DS01-05 | 专利影响力被引与 SEP 一条还是两条 | DS-01-METRIC-OPEN-L01 | M_INNOV_PATENT_INFLUENCE | A:一条 ID；被引为主、SEP 为辅子项 · B:拆 M_INNOV_PATENT_CITE 与 M_INNOV_PATENT_SEP | A | 半成品同一行并列被引/SEP；05 两者皆无专叶。拆条膨胀且同缺库。禁止用 M_CHAIN_PATENT_COUNT 顶替件数。 | 🟡 |
| Q113 | Q-MO-DS01-06 | 事件关注度口径 | DS-01-METRIC-OPEN-L01 | M_INNOV_EVENT_ATTENTION | A:传播/讨论热度（被关注和讨论的程度） · B:资讯/新闻条数 · C:CMS 阅读量 | A | 半成品「需确认」+ 调用系统=深度挖掘。B 会撞 M_CHAIN_NEWS_COUNT（禁止顶替）。C 是运营壳，不是自动分级输入。 | 🟡 |
| Q114 | Q-MO-DS01-07 | 事件影响力对象范围 | DS-01-METRIC-OPEN-L01 | M_INNOV_EVENT_INFLUENCE | A:行业+区域+舆情综合，权重待公式会签 · B:仅行业 · C:并入要素影响力九子项 | A | OPEN 口径已写三角。C 被禁止。演示「影响力分值」未签，默认综合以免漏对象。 | 🟡 |
| Q115 | Q-MO-DS01-08 | 事件重要性分级如何切高/中/低 | DS-01-METRIC-OPEN-L01 | M_INNOV_EVENT_IMPORTANCE | A:由关注度+影响力自动分级，阈值待唐绍祖签 · B:CMS 手工打标 | A | SRS L6-2 点名自动计算；差集 missing 正因要模型而非手工。B 会把本核打成 other_system，与需规不符。 | 🟡 |
| Q116 | Q-MO-DS02-01 |  | DS-02-METRIC-OPEN-L01 |  | A:同一 ID（同源不同面） · B:维护面另号 VARIANT=MAINTAIN | A |  | 🟡 |
| Q117 | Q-MO-DS02-02 |  | DS-02-METRIC-OPEN-L01 |  | A:分行两号（KEYNODE=识别+样式；PRIORITY=重要度级别） · B:合并为一号 | A |  | 🟡 |
| Q118 | Q-MO-DS02-03 |  | DS-02-METRIC-OPEN-L01 |  | A:一条 MODEL（xlsx 行 19 合并；边权排序已由 TOP5 覆盖） · B:拆成节点影响力 + 实体优先级两号 | A |  | 🟡 |
| Q119 | Q-MO-DS02-04 |  | DS-02-METRIC-OPEN-L01 |  | A:一条 ID、两个 COUNT 面（与 TOPIC-TECH TEMP 同结构） · B:拆 M_TECH_PAPER_CNT + M_TECH_PATENT_CNT | A |  | 🟡 |
| Q120 | Q-MO-DS02-05 |  | DS-02-METRIC-OPEN-L01 |  | A:共享（同口径：technology 对齐 COUNT DISTINCT） · B:展示另号 VARIANT=DISPLAY | A |  | 🟡 |
| Q121 | Q-MO-DS03-01 | 技术规模（气泡大小）统计的是成果体量、应用规模还是投入？ | DS-03-METRIC-OPEN-L01 | M_TECH_OUTPUT_SCALE | A:成果体量（论文/专利/标准等产出去重计数） · B:应用规模（落地项目/产品数） · C:投入规模（与投资额合并为同一号） · D:成果与应用的综合体量（不含资金） | D | OPEN 口径并列「成果/投入/应用」，但投资额已独立赋号；又禁止用论文量/专利量冒充「技术规模」专名。 故默认成果+应用综合体量，论文/专… | 🟡 |
| Q122 | Q-MO-DS03-02 | 本页「技术话题热度」是否与专题「技术热点热度指数」同口径？ | DS-03-METRIC-OPEN-L01 | M_TECH_TOPIC_HEAT | A:同口径，复用专题热度即将赋的正式号 · B:不同口径，本页独立 M_TECH_TOPIC_HEAT（话题/关键词热力读面） | B | 专题=已对齐技术点的热度指数 Job（增长曲线/热点报告）；本页=按技术领域关键词/主题聚合的热力图。 OPEN 双方互不改挂。同 seq … | 🟡 |
| Q123 | Q-MO-DS03-03 | 本页「技术发展阶段」是否与专题「技术阶段判定」同口径同号？ | DS-03-METRIC-OPEN-L01 | M_TECH_LIFE_STAGE | A:同口径同号 M_TECH_LIFE_STAGE（本页读 ADS，专题跑 Job） · B:不同口径；专题保留 Job 判定说明+LLM，本页另号只作家气泡分档 | A | 同 05 seq 137 核、同一技术对象的生命周期阶段。policy §3.4 禁止同口径两套 ID。 本页气泡位置维与专题阶段输出是同一… | 🟡 |
| Q124 | Q-MO-DS03-04 | 评估综合得分的分项构成与权重以哪套为准？ | DS-03-METRIC-OPEN-L01 | M_TECH_COMPOSITE_SCORE | A:只读 ADS 已落库加权总分，权重不在本页展开 · B:本页按综合评估 seq 182–191 展开分项公式 · C:与专题深圳潜力与阶段综合评估同号 | A | OPEN 禁止把 seq 182–191 抄成我方公式，本页不跑综合评价 Job。 专题 SZ_ASSESS 是深圳切片上的潜力+阶段 Jo… | 🟡 |
| Q125 | Q-MO-DS03-05 | 技术成熟度与技术发展阶段是否同一标尺？ | DS-03-METRIC-OPEN-L01 | M_TECH_MATURITY_LEVEL | A:两轴独立（成熟水平 vs 生命周期阶段），保留两号 · B:同一标尺，只保留一号 | A | 本页气泡图同时用成熟度与阶段编码位置二维；OPEN 已拆两条 TEMP。 萌芽/成长/成熟看起来像成熟度，但是阶段枚举，不是成熟水平连续分。 | 🟡 |
| Q126 | Q-MO-DS03-06 | 技术关联强度的边权如何取？ | DS-03-METRIC-OPEN-L01 | M_TECH_REL_STRENGTH | A:05 seq 105 关系抽取边权重 · B:共现次数 · C:引用/依赖边计数 · D:节点中心度 | A | OPEN 写明边权随 seq 105 关系抽取，弦线粗细；影响路径≠ DS-02-PATH。 中心度是另一指标，且禁止改挂 M_SYNTH_… | 🟡 |
| Q127 | Q-MO-DS04-01 | 城市对标维：招标三维 vs 186 四维 | DS-04-METRIC-OPEN-L01 | M_INNOV_CITY_BENCHMARK_GLOBAL | A:计算维用招标三维（投入/产出/环境），另写三维公式 · B:读面标签用招标三维，计算底物跟 186 四维（科技/产业/人才/政策） · C:两套并存、拆两条 ID | B | A2 CITY-B03 已记三维≠四维为语义债、不另开 A；差集已 mapped 186。 禁止发明三维 M_*，禁止改挂 M_SYNTH_… | 🟡 |
| Q128 | Q-MO-DS04-02 | 城市创新能力要素集合 | DS-04-METRIC-OPEN-L01 | M_INNOV_CITY_FACTOR_GLOBAL | A:只算招标例示三要素（人才/资金/政策），或拆成三条 ID · B:例示三要素为展示标签，计算跟 seq 187 要素维，一条 ID · C:复用 M_SYNTH_ELEM_TYPE_SCORE（七要素类型维得分） | B | 例示 ⊂ 七要素；OPEN 禁止改挂 M_SYNTH_ELEM_* / CONTRIB。 本页是全球城市读面，与专题 SYNTH-ELEME… | 🟡 |
| Q129 | Q-MO-DS04-03 | 载体多维排名是否按维拆 ID | DS-04-METRIC-OPEN-L01 | M_INNOV_CARRIER_RANK_GLOBAL | A:一条 MIXED（总体/领域/地区名次，依赖同一指数） · B:拆 OVERALL / DOMAIN / REGION 三条 RANK | A | OPEN 只给一条 TEMP_DS04_CARRIER_RANK；筛选壳已 N/A（n/a_ops）。 名次依赖 M_INNOV_CARRI… | 🟡 |
| Q130 | Q-MO-DS04-04 | 城市创新能力排名是否拆指数值 + 名次；能否复用 SYNTH / DS-06 | DS-04-METRIC-OPEN-L01 | M_INNOV_CITY_RANK_GLOBAL | A:一条 MIXED（名次为主、计算方法可查看） · B:拆 INDEX + RANK 两条 · C:复用 M_SYNTH_VIT_INDEX + M_SYNTH_VIT_RANK，或复… | A | DS-04 OPEN 未单列 CITY_INDEX。M_SYNTH_VIT_RANK 口径=区域创新活力四维指数在对比范围内的排序 （依赖 … | 🟡 |
| Q131 | Q-MO-DS04-05 | 人才创新指数是否与智库 seq 184 / DS-06 深圳重点人才指数同产品 | DS-04-METRIC-OPEN-L01 | M_INNOV_CITY_TALENT_INDEX_GLOBAL | A:本页全球封装独立 ID · B:与 DS-06 深圳重点人才指数同产品、复用同一 ID · C:挂 seq 184 / 改 mapped | A | 对象=全球城市语境下人才贡献/影响/活跃度封装读数；DS-06 是深圳重点人才质量/活跃/贡献。 OPEN 禁止 mapped 184。内部… | 🟡 |
| Q132 | Q-MO-DS05-01 | 湾区「创新比例」分子分母 | DS-05-METRIC-OPEN-L01 | M_INNOV_GBA_INNOV_RATIO | A:分子=创新产值（与 M_INNOV_GBA_OUTPUT_VALUE 同核）；分母=… · B:分子=创新投入（与 M_INNOV_GBA_INVEST 同核）；分母=全社会固定资… · C:分子=高技术产业增加值；分母=工业增加值 | A | 目录把产值、投入、比例并列，比例更像产出结构而非投入强度。与产值同核可避免第三套未冻口径。 窗口默认自然年、对象 11 城（常识，不另开 Q… | 🟡 |
| Q133 | Q-MO-DS05-02 | 招标四因子 vs seq 186 四维（CAPACITY 子指标身份） | DS-05-METRIC-OPEN-L01 | M_INNOV_GBA_CAPACITY_INDEX, M_INNOV_GBA_RES_INDEX, M_INNOV_GBA_ORG_INDEX, M_INNOV_GBA_MECH_INDEX, M_INNOV_GBA_ENV_INDEX, M_INNOV_GBA_SUBINDEX_CONTRIB | A:本页正式身份用招标四因子（资源/机构/机制/环境）。186 仅作计算路径对照（map… · B:子指标改挂 186 四维名称，本页四因子只作展示别名 · C:认为四因子与四维逐条同口径，reuse M_SYNTH_VIT_INDEX / DI… | A | 用户铁律：CAPACITY 可 mapped 186，禁止改挂 M_SYNTH_VIT_*，除非口径逐条相同。 getMetric：M_SY… | 🟡 |
| Q134 | Q-MO-DS05-03 | 「专利及论文数量」加总规则 | DS-05-METRIC-OPEN-L01 | M_INNOV_GBA_PATENT_PAPER | A:加总 COUNT(专利)+COUNT(论文)；授权量走独立 M_INNOV_GBA_… · B:专利只计申请量，论文单独分列（本 ID 只保留加总展示，后台两列） · C:本 ID 只计专利，论文另开 ID（将废弃加总名） | A | 目录原文是一个成员名「专利及论文数量」，与「专利授权量」分列。半成品无行。 加总保一个 ID；授权量独立避免申请/授权双计。论文默认科技论文… | 🟡 |
| Q135 | Q-MO-DS05-04 | 「创新产值」统计对象 | DS-05-METRIC-OPEN-L01 | M_INNOV_GBA_OUTPUT_VALUE | A:高技术产业（制造业）增加值 · B:新产品销售收入 / 新产品产值 · C:全口径「创新活动」经济产出（需甲方给名录） | A | OPEN 只写「区域创新活动经济产出规模」，未冻。湾区监测常用高技术产业增加值，可统计、可分城。 C 无现成名录，不作默认。 | 🟡 |
| Q136 | Q-MO-DS05-05 | 「创新投入」统计对象 | DS-05-METRIC-OPEN-L01 | M_INNOV_GBA_INVEST | A:R&D 经费内部支出（不含人力折合全时当量） · B:R&D 经费 + 科技拨款等全口径资金 · C:资金与 R&D 人员全时当量合成投入强度指数 | A | OPEN 写「资金/资源/研发投入强度」三者并列。默认取可加总的 R&D 经费，强度（占比）若需要走比例 ID 而非本号。 C 会把本 ST… | 🟡 |
| Q137 | Q-MO-DS06-01 | 城际对比维：招标分项 vs 186 四维 | DS-06-METRIC-OPEN-L01 | M_INNOV_CITY_COMPARE_SZ | A:计算维用招标分项（研发投入 / 专利数量 / 高新技术企业数量 / 创新人才），另写… · B:读面标签用招标分项，计算底物跟 186 四维（科技/产业/人才/政策），一条 ID · C:复用 M_SYNTH_VIT_INDICATOR 或 M_INNOV_CITY_BE… | B | OPEN 已记招标分项 ≠ 186 四维为 SZCITY-B03，不另开 A、不发明分项 M_*。差集已 mapped 186。 本页是深圳… | 🟡 |
| Q138 | Q-MO-DS06-02 | 深圳重点人才指数是否与智库 seq 184 / DS-04 全球人才创新指数同产品 | DS-06-METRIC-OPEN-L01 | M_INNOV_CITY_TALENT_INDEX_SZ | A:本页深圳封装独立 ID；类型建议 third_party · B:与 DS-04 M_INNOV_CITY_TALENT_INDEX_GLOBAL 同… · C:挂 seq 184 / 改 mapped | A | 对象=深圳重点人才质量/活跃/贡献；DS-04 是全球城市语境下人才贡献/影响/活跃度。 OPEN 禁止 mapped 184；差集 oth… | 🟡 |
| Q139 | Q-MO-DS06-03 | 深圳科技竞争力四子项是否拆 ID；能否套用湾区 SWOT | DS-06-METRIC-OPEN-L01 | M_INNOV_CITY_COMPETE_SZ | A:一条 MIXED（优势领域 / 薄弱环节 / 发展潜力 / 发展水平共核） · B:拆四条 ID · C:复用 DS-05 M_INNOV_GBA_SWOT_* 四象限 | A | OPEN 只给一条 TEMP_DS06_CITY_COMPETE；xlsx 行60–63 为同叶四子项。 湾区 SWOT 对象=11 城象限… | 🟡 |
| Q140 | Q-MO-DS07-01 | POLICY-GUARD 七条 ELEMENT 用 INNOV 还是 POLICY？ | DS-07-METRIC-OPEN-L01 | M_INNOV_PG_COUNT_DIST | A:全部用 INNOV（M_INNOV_PG_*），与 E7 M_POLICY_* 分域 · B:政策评估核改用 POLICY 域新号（仍禁止改挂已有 M_POLICY_*） · C:改挂 E7 TRACE 的 M_POLICY_INTENSITY_* / IMPLE… | A | 本页是评估四力·政策与条件保障力展示指标，不是 E7 政策工作台、不是 DS-10/11/12。 用户协议：ELEMENT 默认 INNOV… | 🟡 |
| Q141 | Q-MO-DS07-02 | 科学网络三类中心性一条 MIXED 还是拆三条 GRAPH？ | DS-07-METRIC-OPEN-L01 | M_INNOV_SCI_CENTRALITY | A:一条 MIXED（度/接近/中介 + 图谱 + 排名） · B:拆 DEGREE / CLOSENESS / BETWEENNESS 三条 GRAP… · C:改挂 M_TECH_PATH_CENTRALITY 或 M_SYNTH_COLLAB… | A | OPEN 只给一条 TEMP；对照 116 中心度排序。拆条膨胀且同 mapped。 C：路径关键节点 / 协同生态网 ≠ 科学合作网，OP… | 🟡 |
| Q142 | Q-MO-DS07-03 | 专利数量是否拆申请 / 授权两条？ | DS-07-METRIC-OPEN-L01 | M_INNOV_TINN_PATENT_COUNT | A:一条 STAT；申请与授权为切片 · B:拆 APPLY 与 GRANT 两条 · C:改挂 M_CHAIN_PATENT_COUNT / M_INNOV_GBA_PATE… | A | 招标「申请和授权」vs 96「申请成功」已记 TINN-B03，不另开 A 类。拆条双 mapped 叙事。 C 对象=链关联专利或湾区授权… | 🟡 |
| Q143 | Q-MO-DS07-04 | 扶持力度广度 / 深度是否拆号？ | DS-07-METRIC-OPEN-L01 | M_INNOV_PG_INTENSITY | A:一条 MIXED（广度≈覆盖，深度≈效果/成本，对照 167） · B:拆 BREADTH 与 DEPTH 两条 · C:改挂 M_POLICY_INTENSITY_INDEX / SUPPORT_STRE… | A | OPEN 一条 TEMP 覆盖广度与深度；资金支持强度归 FUND。C 是 E7 TRACE，禁止改挂、无 also_in。 | 🟡 |
| Q144 | Q-MO-DS07-05 | 引导力三性是否拆号？ | DS-07-METRIC-OPEN-L01 | M_INNOV_PG_GUIDE | A:一条 MODEL（前瞻性/系统性/针对性综合分） · B:三性拆三条 · C:发明 M_POLICY_GUIDE_* 并改挂政策 OPEN | A | 政策 9 叶无引导力专叶；PG-B03 已记三性口径未冻。拆条三 missing。C 被 OPEN / 本 loop 禁止。 | 🟡 |
| Q145 | Q-MO-DS07-06 | 政策实施效果前后对比与 168 指数是否一条？ | DS-07-METRIC-OPEN-L01 | M_INNOV_PG_EFFECT | A:一条 MIXED（前后对比读面 + 168 效果指数） · B:拆前后对比 STAT 与效果指数 MODEL · C:改挂 M_POLICY_IMPLEMENTATION_EFFECT / EFFECT… | A | 半成品行66 与 seq 168 同核。E7 已 mapped 同叶 → 不重列、不改挂 TRACE。 项目记录上的「实施效果」字段归 M_… | 🟡 |
| Q146 | Q-MO-DS08-01 | 科技指数值是一条 ID（区域为切面）还是拆全国/区域两号 | DS-08-METRIC-OPEN-L01 | M_INNOV_SCIINDEX_VALUE | A:一条 ID；全国单值与 GIS 区域热力是同一读数的空间切面 · B:拆全国值与区域值两条 ID | A | OPEN 已收口 xlsx 92/93 + seq 165 落同一 TEMP_DS08_TINDEX_VALUE。 拆条会把注释 TEMP_… | 🟡 |
| Q147 | Q-MO-DS08-02 | 专家H指数数据源：外采只读 vs 本页自算 Hirsch | DS-08-METRIC-OPEN-L01 | M_INNOV_EXPERT_HINDEX | A:第三方外采只读（seq 162 学术力分项含 H），不展开 Hirsch · B:本页按 Hirsch 公式自算（需公式会签） · C:改挂 M_CHAIN_ACADEMIC_POWER · D:reuse DS-01 M_INNOV_SCHOLAR_INFLUENCE | A | OPEN 明确 third_party、禁止伪展开 Hirsch。C 被用户铁律禁止（链科研实力 ≠ 本页 H 排行）。 D 不可：DS-0… | 🟡 |
| Q148 | Q-MO-DS08-03 | 专家科研活跃度分子 | DS-08-METRIC-OPEN-L01 | M_INNOV_EXPERT_ACTIVITY | A:论文数量（对照 162 成果数量/动态）；项目/学术活动为叙事不进公式 · B:论文+项目数+学术活动参与度加权（需公式会签） · C:改挂人才流动 / mapped 157 | A | OPEN：论文数量等科研活跃读面；项目/学术活动 05 无专核 → VIZ-B02，不另开 A。 C 被禁止。不改挂 M_CHAIN_ACA… | 🟡 |
| Q149 | Q-MO-DS09-01 | 规划页「本地」范围 | DS-09-METRIC-OPEN-L01 | M_INNOV_PLAN_LOCAL_ADV | A:固定深圳本市 · B:用户选定规划区域；未选时内部默认深圳 · C:粤港澳大湾区 11 城（与 DS-05 同宇宙） | B | OPEN 口径是规划页「本地」特色与优势，不是 DS-06 深圳城市竞争力拆项，也不是湾区创新能力因素。 固定深圳会把未选区域的规划页读面锁… | 🟡 |
| Q150 | Q-MO-DS09-02 | 产业界↔学术界流动如何判定 | DS-09-METRIC-OPEN-L01 | M_INNOV_PLAN_TALENT_FLOW | A:以任职单位类型为主（企业 vs 高校/院所）；论文署名与项目承担单位只作叙事、不进公… · B:任职 + 论文署名单位 + 项目承担单位三源并集进公式 · C:复用 M_TALENT_FLOW_TRACK（区域/行业流入流出留存） | A | 招标对象是产业界和学术界之间的流动 + 预警，不是专题人才区域迁徙。 C 口径不同且用户禁止改挂专题人才 ID。B 公式未签、易把 157 … | 🟡 |
| Q151 | Q-MO-DS09-03 | 重叠度等级 vs 竞争情报等级是否同核 | DS-09-METRIC-OPEN-L01 | M_INNOV_RES_GRADE, M_INNOV_RES_CI_LEVEL | A:两条 ID（GRADE=重叠度分档；CI_LEVEL=情报强弱分值） · B:合并为一条，等级/分值只是读面 · C:复用企业竞争力/技术力/商业力分档（141/145/146） | A | OPEN 已分两条 TEMP，半成品把竞争情报等级列为独立主项。C 被 RESEARCH 禁 mapped。 比对交互仍归 M_INNOV_… | 🟡 |
| Q152 | Q-MO-DS09-04 | 规划页「区域竞争力/潜力」vs 186「创新活力」vs SYNTH-VITALITY | DS-09-METRIC-OPEN-L01 | M_INNOV_KEYD_COMPETITIVENESS, M_INNOV_KEYD_POTENTIAL | A:独立两条 INNOV 号；186 只作语义读面对照；不改挂 SYNTH / 不 re… · B:复用 M_SYNTH_VIT_INDEX / DIM_SCORE（或 GBA/CIT… · C:竞争力与潜力再合并为一条 | A | KEYD-B03 已记「竞争力水平」≠「区域创新活力」。对象=规划页区域，不是专题 Job 对比城市、不是湾区 11 城、不是全球城市。 用… | 🟡 |
| Q153 | Q-MO-ZHIKU-01 | 问题热度与潜力是否拆核 | ZHIKU-METRIC-OPEN-L01 | ZHIKU-S5-ISSUE-HEAT-SCORE | A:一条综合核（热度+潜力），不拆新 ZHIKU-S* · B:热度、潜力分列两条 ID | A | 卡面原文用「研究热度/潜力」斜杠并列。本 loop 禁止发明新 ZHIKU-S* / M_*， 内部默认一条 MODEL 核；拆条留给甲方，… | 🟡 |
| Q154 | Q-MO-ZHIKU-02 | 人才地图分布计数对象 | ZHIKU-METRIC-OPEN-L01 | ZHIKU-S4-TALENT-MAP-DIST-TOTAL | A:当前视图命中的 geo point 去重（人/机构可同点） · B:人才点与机构点分核 | A | 原文「人才/机构地理分布点」。分核需第二号，本叶禁止发明。默认计点不计人/机构分列。 禁止并入 DS-13～16 GIS。 | 🟡 |
| Q155 | Q-MO-ZHIKU-03 | 社会网络节点总数是否含边/社区 | ZHIKU-METRIC-OPEN-L01 | ZHIKU-S2-NETWORK-NODE-TOTAL | A:只计当前结果 distinct node_id；边/社区/中心性不另造 ID · B:节点、边、社区分列 | A | 卡面核是「节点（实体）总数」。边/社区分列需新号，本叶禁止发明。禁止 mapped 图谱 API 116。 | 🟡 |

## 叶级文件

路径：`metrics/request/_work/id-assign/{TASK_ID}-questions.yaml`。

## 共享号（非 Question）

- `M_TECH_PAPER_PATENT_CNT`：TOPIC-TECH 与 DS-02 同口径共享；两边均非 seed reuse。

