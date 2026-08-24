# 重判明细 · SVC（43 条）

| # | metric_id | 分组 | 中文名 | 现type | definition | formula | 新判type | 理由 |
|---|---|---|---|---|---|---|---|---|
| 1 | `M_SVC_ORG_TECH_SCORE` | T2 | 服务机构影响力 | MODEL | 服务机构的科技服务供给、资源连接、生态支撑。本页不新编 ID：reuse B 轨已有 M_SVC_ORG_TECH_SCORE（seq 179 技术力）。 seed 尚未登记（MCP miss），A2-GAP-algo-catalog 已列。口径差（影响力叙事 vs 技术力指数）见 Q-MO-DS01-04，默认仍 r | pending_cosign: human:唐绍祖（未签） |  |  |
| 2 | `M_SVC_TYPE_DIST_QUERY` | T2 | 查询结果·服务类型分布 | STAT | 对当前查询结果集中的服务机构（org_id 去重）按主数据服务/机构类型字段计数， 反映服务生态多样性。类型字典默认=结果集内 svc_type/org_type（Q-MO-QUERY-04）。 不是产业服务深度分析，禁止消费 SVCCHAIN-* / M_SVC_ORG_CNT（全球按国家规模核）。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 3 | `M_SVC_CHAIN_BOTTLENECK` | T3 | 瓶颈堵点判定 | MODEL | 薄弱环节 / 服务空白 / 资源瓶颈标注 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 4 | `M_SVC_CHAIN_SEGMENT_AVG_DEPTH` | T3 | 环节平均服务深度 | MODEL | 环节内机构服务深度均值 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 5 | `M_SVC_CHAIN_SEGMENT_ORG_COUNT` | T3 | 环节服务机构数 | MODEL | 当前产业下某环节在库服务机构去重数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 6 | `M_SVC_GRAPH_CENTRALITY` | T3 | 节点度中心性 | GRAPH | 可见子网内节点连接数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 7 | `M_SVC_GRAPH_DENSITY` | T3 | 服务网络密度 | MODEL | 当前可见子网无向密度 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 8 | `M_SVC_GRAPH_INFLUENCE` | T3 | 生态影响力评分 | MODEL | 服务网络影响力合成分 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 9 | `M_SVC_ORG_COVERAGE_BREADTH` | T3 | 服务广度 | MODEL | 机构有服务记录的产业领域去重数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 10 | `M_SVC_ORG_COVERAGE_DEPTH` | T3 | 服务深度得分 | MODEL | 机构在单一产业领域的服务深度 0–100 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 11 | `M_SVC_ORG_MARKET_HEAT` | T3 | 市场热度评级 | MODEL | 由趋势斜率/波动得到的热度研判 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 12 | `M_SVC_ORG_NEW_COUNT` | T3 | 年度新增服务机构数 | MODEL | 选定领域按年新增服务机构数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 13 | `M_SVC_ORG_SELECTED_COUNT` | T3 | 当前分析机构数 | MODEL | 用户已确认分析集合的机构数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 14 | `M_SVC_ORG_TOTAL` | T3 | 入库服务机构总数 | STAT | 专题库内服务机构去重总数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 15 | `M_SVC_PT_CHAIN_NODE_ORG` | T3 | 产业链节点服务机构数 | MODEL | 选定产业下各服务链环节的机构数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 16 | `M_SVC_PT_GLOBAL_SCALE_DIST` | T3 | 全球服务机构规模分布 | STAT | <50 / 50-200 / 200-500 / >500 人分档机构数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 17 | `M_SVC_PT_GLOBAL_TOTAL` | T3 | 全球服务机构总数 | STAT | 全球口径服务机构去重总数（含历年） 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 18 | `M_SVC_PT_GLOBAL_TYPE_DIST` | T3 | 全球服务机构类型分布 | STAT | 高校/科研院所/企业三类数量与占比 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 19 | `M_SVC_PT_KEYORG_SCALE` | T3 | 重点机构规模档案值 | STAT | 档案字段直读，非计算指标 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 20 | `M_SVC_PT_REGION_ORG` | T3 | 区域服务机构数 | MODEL | 全球=国家/地区；全国=省级 的机构数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 21 | `M_SVC_PT_SZ_FIELD_DIST` | T3 | 深圳机构产业领域分布 | STAT | 深圳机构在领域与六环节上的分布 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 22 | `M_SVC_PT_SZ_REGION_ORG` | T3 | 深圳机构区域分布 | STAT | 深圳十区机构数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 23 | `M_SVC_PT_SZ_TOTAL` | T3 | 深圳产业服务机构数量 | STAT | 城市=深圳 的机构去重数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 24 | `M_SVC_PT_SZ_TYPE_DIST` | T3 | 深圳机构类型统计 | MODEL | 深圳口径 OrgType 分布 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 25 | `M_SVC_REC_ATTRACT_SCORE` | T3 | 招引综合评分 | MODEL | 外部候选机构按招引模型四指标加权的综合得分 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 26 | `M_SVC_REC_CANDIDATE_CNT` | T3 | 候选机构数 | MODEL | 当前产业方向与筛选范围内参与名单计算的候选机构数量 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 27 | `M_SVC_REC_CULTIVATE_SCORE` | T3 | 培育综合评分 | MODEL | 深圳本土在库机构按培育模型四维度加权的综合得分 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 28 | `M_SVC_SZ_CHAIN_COMPLETENESS` | T3 | 服务链完整度 | MODEL | 统一框架下服务链完整程度 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 29 | `M_SVC_SZ_COMPARE_METRIC` | T3 | 城市对比指标值 | MODEL | 选定产业下深圳/全国平均/北上广各对比指标取值 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 30 | `M_SVC_SZ_TIER` | T3 | 深圳梯队位置 | MODEL | 可比指标下深圳相对一线城市的梯队分档 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 31 | `M_SVC_BASE_101_1` | TTEMP | 服务机构基础指标模型构建 | STAT | 服务机构基础指标模型构建：对应算法库 SRS ALGO-SVC-BASE-101，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 32 | `M_SVC_DEEP_172_1` | TTEMP | 服务链短板分析模型 | MODEL | 服务链短板分析模型：对应算法库 SRS ALGO-SVC-DEEP-172，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 33 | `M_SVC_DEEP_173_1` | TTEMP | 服务关系链模型 | MODEL | 服务关系链模型：对应算法库 SRS ALGO-SVC-DEEP-173，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 34 | `M_SVC_DEEP_174_1` | TTEMP | 金融服务机构技术力评价模型 | MODEL | 金融服务机构技术力评价模型：对应算法库 SRS ALGO-SVC-DEEP-174，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 35 | `M_SVC_DEEP_175_1` | TTEMP | 知识产权服务机构技术力评价模型 | MODEL | 知识产权服务机构技术力评价模型：对应算法库 SRS ALGO-SVC-DEEP-175，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 36 | `M_SVC_DEEP_176_1` | TTEMP | 人力资源服务机构技术力评价模型 | MODEL | 人力资源服务机构技术力评价模型：对应算法库 SRS ALGO-SVC-DEEP-176，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 37 | `M_SVC_DEEP_177_1` | TTEMP | 市场营销服务机构技术力评价模型 | MODEL | 市场营销服务机构技术力评价模型：对应算法库 SRS ALGO-SVC-DEEP-177，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 38 | `M_SVC_DEEP_178_1` | TTEMP | 咨询服务机构技术力评价模型 | MODEL | 咨询服务机构技术力评价模型：对应算法库 SRS ALGO-SVC-DEEP-178，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 39 | `M_SVC_DEEP_179_1` | TTEMP | 科技创新服务机构技术力评价模型 | MODEL | 科技创新服务机构技术力评价模型：对应算法库 SRS ALGO-SVC-DEEP-179，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 40 | `M_SVC_DEEP_180_1` | TTEMP | 服务机构引入推荐模型 | MODEL | 服务机构引入推荐模型：对应算法库 SRS ALGO-SVC-DEEP-180，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 41 | `M_SVC_DEEP_181_1` | TTEMP | 服务机构培育推荐模型 | MODEL | 服务机构培育推荐模型：对应算法库 SRS ALGO-SVC-DEEP-181，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 42 | `M_SVC_GRAPH_112_1` | TTEMP | 服务机构实体识别构建 | GRAPH | 服务机构实体识别构建：对应算法库 SRS ALGO-SVC-GRAPH-112，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
| 43 | `M_SVC_GRAPH_113_1` | TTEMP | 服务机构实体关系抽取 | GRAPH | 服务机构实体关系抽取：对应算法库 SRS ALGO-SVC-GRAPH-113，统计窗口与对象范围以需规文本为准。 | pending_cosign: human:唐绍祖（未签） |  |  |
