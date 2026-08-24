# 重判明细 · ORG（22 条）

| # | metric_id | 分组 | 中文名 | 现type | definition | formula | 新判type | 理由 |
|---|---|---|---|---|---|---|---|---|
| 1 | `M_ORG_ATTENTION_TREND` | T2 | 科研关注度 | COMPUTE | 由同一选定范围下的新增科研机构数量及其增长速率合成的领域科研关注度趋势（SRS 04 seq 65）。 05 无关注度专叶，与新增动态同叶消费。非检索热度、非政策关注度。 OPEN Round 4 草稿曾标 STAT；本 loop 按「指数合成（无训练）」改为建议 COMPUTE。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 2 | `M_ORG_ATTRACT_SCORE` | T2 | 科研机构招引推荐指数 | MODEL | 对候选科研机构多维评估后的招引优先级得分；建议名单规模为同核计数展示面，不另造 CNT ID。 G3 Job。内部默认维取 05.4 seq 154（学术影响力 / 科技成果 / 团队实力）。 禁止改挂企业招引或服务机构招引 ID。推荐理由文本无独立 ID。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 3 | `M_ORG_COLLAB_CHAIN` | T2 | 科研合作关系链条 | GRAPH | 以论文、专利等合作记录构建的科研机构合作网络（G1 A 面当前图 / Nebula）， 展示合作强度、合作类型与核心节点。对象=专题科研机构。 不是产业服务图谱，不是区域创新协同指数。强度/类型/中心性默认作为本核展示面，不拆子 ID。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 4 | `M_ORG_CULTIVATE_SCORE` | T2 | 科研机构扶持推荐指数 | MODEL | 对深圳本地科研机构评估后的培育/扶持优先级得分及建议名单规模。 「一院一策」为文本，无独立 ID。G3 Job。 内部默认维取 05.4 seq 155（成果 / 经费效率 / 人才结构）。 禁止改挂企业培育或服务机构扶持 ID。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 5 | `M_ORG_INDUSTRY_COVER` | T2 | 科研机构产业领域覆盖 | STAT | 选定专题科研机构集合（名录去重）在统计窗口（默认自然年）内参与的产业链领域去重个数， 及该覆盖数的同比/环比趋势。对象不含产业服务链「服务机构」。 R-19「各领域参与度」无独立核，不另造 DEPTH ID。筛选壳本身不是本核。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 6 | `M_ORG_NEW_TREND` | T2 | 新增科研机构趋势 | STAT | 选定产业或技术领域内，统计窗口（默认自然年）内首次进入该范围科研机构名录的机构 去重计数随时间变化。对象仅专题科研机构。禁止因 05 seq 99(4) 混写「服务机构」而改挂 M_SVC_NEW_CNT / M_SVC_ORG_NEW_COUNT。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 7 | `M_ORG_PERF_QUERY` | T2 | 查询结果·科研机构绩效 | STAT | 对当前查询命中结果集中的科研机构（org_id 去重）按绩效核做推荐聚合，匹配饼图/柱状。 默认核=结果集内关联论文数 COUNT，可按 org_type 分组（Q-MO-QUERY-02）。 不是 05 科研机构 10 叶模型输出，禁止消费 TOPIC-ORG-05 / M_SVC_ORG_* / SVCCHAIN。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 8 | `M_ORG_SZ_ADVANTAGE` | T2 | 深圳科研机构优势 | MODEL | 选定产业下深圳科研机构相对全国（或对照集合）的优势分析报告。G3 Job。 内部默认维取 05.4 seq 151（成果 / 经费 / 人才）。指标选择壳不是本核。 不与现状解读核重复算覆盖。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 9 | `M_ORG_SZ_PAINPOINT` | T2 | 深圳科研机构痛难点 | MODEL | 识别深圳科研机构在选定产业下的痛难点，并给出改进建议与分析报告。G3 Job。 内部默认维取 05.4 seq 152（项目 / 转化 / 人才 / 产业合作）。 禁止用企业痛点 M_ENT_PAINPOINT_* 或服务机构口径顶替。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 10 | `M_ORG_SZ_STATUS` | T2 | 深圳科研机构现状解读 | MIXED | 深圳科研机构在选定产业下的优势与不足解读报告，突出关键指标表现。 范围=深圳×选定产业×专题科研机构名录。不重复计算优势专叶与痛难点专叶的覆盖。 评价框架配置壳不是本核。禁止用 M_CHAIN_SZ_INSTITUTION_COUNT 顶替。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 11 | `M_ORG_TECH_LAYOUT` | T2 | 科研机构技术领域布局 | STAT | 所选科研机构在核心学科 / 前沿方向 / 产业技术链上的布局分布（机构×领域计数或占比）。 统计窗口默认自然年；对象=专题科研机构名录去重。 seq 149「各领域科技综合实力」默认并入本核展示面、不另造 ID，且不得冒充可配置多机构技术力。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 12 | `M_ORG_TECH_SCORE` | T2 | 科研机构技术力评价与对比 | MODEL | 用户从技术力指标库多选并设权后，对各专题科研机构计算的技术力得分， 支撑雷达/条形对比与综合排名。05 十叶无专叶，差集 third_party（【算法补】），公式不展开。 禁止改挂服务机构或企业技术力；禁止用综合科研实力或领域科技综合实力冒充本核。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 13 | `M_ORG_BASE_99_1` | TTEMP | 科研机构基础指标模型构建 | third_party | 科研机构基础指标模型构建：对应算法库 SRS ALGO-ORG-BASE-99，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 14 | `M_ORG_DEEP_149_1` | TTEMP | 科研机构重点技术领域布局模型 | third_party | 科研机构重点技术领域布局模型：对应算法库 SRS ALGO-ORG-DEEP-149，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 15 | `M_ORG_DEEP_150_1` | TTEMP | 科研机构发展历程模型 | third_party | 科研机构发展历程模型：对应算法库 SRS ALGO-ORG-DEEP-150，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 16 | `M_ORG_DEEP_151_1` | TTEMP | 深圳科研机构优势分析模型 | third_party | 深圳科研机构优势分析模型：对应算法库 SRS ALGO-ORG-DEEP-151，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 17 | `M_ORG_DEEP_152_1` | TTEMP | 深圳科研机构痛难点识别模型 | third_party | 深圳科研机构痛难点识别模型：对应算法库 SRS ALGO-ORG-DEEP-152，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 18 | `M_ORG_DEEP_153_1` | TTEMP | 科研合作关系链条模型 | third_party | 科研合作关系链条模型：对应算法库 SRS ALGO-ORG-DEEP-153，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 19 | `M_ORG_DEEP_154_1` | TTEMP | 科研机构引入推荐模型 | third_party | 科研机构引入推荐模型：对应算法库 SRS ALGO-ORG-DEEP-154，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 20 | `M_ORG_DEEP_155_1` | TTEMP | 科研机构扶持推荐模型 | third_party | 科研机构扶持推荐模型：对应算法库 SRS ALGO-ORG-DEEP-155，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 21 | `M_ORG_GRAPH_114_1` | TTEMP | 科研机构实体识别构建 | third_party | 科研机构实体识别构建：对应算法库 SRS ALGO-ORG-GRAPH-114，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 22 | `M_ORG_GRAPH_115_1` | TTEMP | 科研机构实体关系抽取 | third_party | 科研机构实体关系抽取：对应算法库 SRS ALGO-ORG-GRAPH-115，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
