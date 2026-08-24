# ALGO-LIB-SEED-TYPE-L01 · §2.1 重判修正清单

> 由 `algorithm-agent` 按《给人说明-指标与算法工作类型与流程梳理.md》§2.1 枚举表，对 522 条已回填指标中 T2+T3（431 条）逐条重判。
> T1（11）+ TTEMP（90）= 101 条 A1 表2 已签，**一律保持不动**。
> 共修正 **94** 条，已回填进 seed。

## 一、判断标准（§2.1 轴 A 映射）

| algorithm.type | 计算本质信号 | 本次重判应用 |
|---|---|---|
| STAT | 计数 COUNT/SUM/AVG/MAX/GROUP BY/DISTINCT、占比 A/B、环比、排名 RANK、简单取数 SELECT | 把「XX数/占比/排名/取最新值」从 MODEL 改回 |
| COMPUTE | 有公式无模型：纯加权 w1+w2+w3、标准化、阈值分档、固定指数公式(HHI/熵/区位熵) | 把「纯加权指数/评分」从 MODEL 改回 |
| MODEL | 评分模型(多维+归一化/等级/排名)、预测、聚类、匹配适配、识别/抽取(NLP)、推荐 | 保留真模型 |
| GRAPH | 中心性、路径、子图、边权、实体识别/关系抽取 | 补「关键节点重要性/网络密度」等图算法 |
| MIXED | 上列多类组合(如贡献度模型+影响路径) | 补「多维排名/竞争情报比对/贡献度+路径」 |
| third_party | 外采 API / G3 Job / LLM | 未改动 |

## 二、改动分布

| from→to | 条数 | 说明 |
|---|---|---|
| MODEL→STAT | 49 | 计数/占比/排名/取数被误判为模型 |
| MODEL→COMPUTE | 30 | 纯加权指数/评分 → 加权计算 |
| STAT→COMPUTE | 3 | 加权被误判为占比 |
| MODEL→GRAPH | 3 | 关键节点重要性 = 图算法 |
| GRAPH→STAT | 3 | SELECT/COUNT 被误判为图 |
| MODEL→MIXED | 2 | 多维排名/竞争情报比对 |
| GRAPH→COMPUTE | 2 | 招引/培育评分 demo 路径 |
| GRAPH→MIXED | 1 | 贡献度 + 影响路径 |
| COMPUTE→STAT | 1 | 归一化+COUNT 本质计数 |

## 三、逐条清单

### CHAIN（31 条）

| # | metric_id | from | to | 理由 |
|---|---|---|---|---|
| 1 | `M_CHAIN_ACADEMIC_COOP_SCORE` | MODEL | COMPUTE | 纯加权合成 联合专利*w1+项目*w2+人才*w3，无评分/预测/聚类模型 |
| 2 | `M_CHAIN_ACADEMIC_POWER` | MODEL | COMPUTE | 纯加权 专利密度*w1+论文密度*w2+高校数量*w3 |
| 3 | `M_CHAIN_BOTTLENECK_SEVERITY` | MODEL | STAT | MAX(severity_score) 简单取最大值聚合，非评分模型 |
| 4 | `M_CHAIN_CHOKE_LINK_COUNT` | MODEL | STAT | 瓶颈∧severity=高 的子集计数（⊆瓶颈数） |
| 5 | `M_CHAIN_COMPLETENESS_SCORE` | MODEL | COMPUTE | 覆盖环节数/全链环节数*100*修正因子 = 占比×加权 |
| 6 | `M_CHAIN_CONCENTRATION_INDEX` | STAT | COMPUTE | HHI=SUM(份额^2) 集中度固定指数公式，非简单计数 |
| 7 | `M_CHAIN_ENTERPRISE_POWER` | MODEL | COMPUTE | AVG(chain_score)*加权因子 |
| 8 | `M_CHAIN_HOT_NEWS_COUNT` | MODEL | STAT | COUNT(DISTINCT news_id) WHERE heat_score>=80 阈值计数 |
| 9 | `M_CHAIN_HOTSPOT_COUNT` | MODEL | COMPUTE | 加权 w1+w2+w3>=阈值 的加权阈值筛选 |
| 10 | `M_CHAIN_HOTSPOT_SCORE` | MODEL | COMPUTE | 纯加权 w1+w2+w3+w4 |
| 11 | `M_CHAIN_INTERNATIONALIZATION_INDEX` | STAT | COMPUTE | 海外占比*w1+海外专利占比*w2+进出口*w3 加权，非纯占比 |
| 12 | `M_CHAIN_LAYOUT_PRIORITY_SCORE` | MODEL | COMPUTE | 纯加权 战略*w1+缺口*w2+前景*w3+可行*w4 |
| 13 | `M_CHAIN_LAYOUT_RECOMMEND_COUNT` | MODEL | STAT | COUNT(DISTINCT chain_id) WHERE 评分>=阈值 阈值计数 |
| 14 | `M_CHAIN_REG_FINANCING` | MODEL | STAT | 融资事件数（计数） |
| 15 | `M_CHAIN_REG_PAPERS` | MODEL | STAT | 高校论文产出（计数） |
| 16 | `M_CHAIN_REG_PATENT` | MODEL | STAT | 产业相关专利（计数） |
| 17 | `M_CHAIN_REG_POLICY_COVERAGE` | MODEL | STAT | 政策覆盖率（占比） |
| 18 | `M_CHAIN_REG_RESEARCH_ORG` | MODEL | STAT | 科研机构规模/密度（计数） |
| 19 | `M_CHAIN_REG_REVENUE` | MODEL | STAT | 营收规模（SUM 聚合） |
| 20 | `M_CHAIN_REG_SERVICE_ORG` | MODEL | STAT | 服务机构（计数） |
| 21 | `M_CHAIN_REG_TALENT_STRUCTURE` | MODEL | STAT | 人才结构（分布统计） |
| 22 | `M_CHAIN_REGION_INDEX` | MODEL | COMPUTE | 三维加权 enterprise*W1+academic*W2+support*W3 |
| 23 | `M_CHAIN_STRATEGIC_IMPORTANCE` | MODEL | COMPUTE | 纯加权 壁垒*w1+集中度*w2+国产化*w3+政策*w4 |
| 24 | `M_CHAIN_SUPPORT_POWER` | MODEL | COMPUTE | 纯加权 政策*w1+机构密度*w2+基础设施*w3 |
| 25 | `M_CHAIN_SZ_ADVANTAGE_RANK` | MODEL | STAT | RANK() OVER ORDER BY 评分 排名（§2.1 STAT 含排名） |
| 26 | `M_CHAIN_SZ_ADVANTAGE_SCORE` | MODEL | COMPUTE | 纯加权 密度*w1+实力*w2+科研*w3+政策*w4 |
| 27 | `M_CHAIN_SZ_COMPLETENESS` | MODEL | STAT | 深圳覆盖环节数/全链环节数*100 占比 |
| 28 | `M_CHAIN_SZ_KEY_NODE_COVERAGE` | MODEL | STAT | 覆盖关键环节数/全链关键环节数*100 占比 |
| 29 | `M_CHAIN_SZ_OPPORTUNITY_SCORE` | MODEL | COMPUTE | 纯加权 缺口*w1+匹配度*w2+政策*w3 |
| 30 | `M_CHAIN_TECH_MATURITY_SCORE` | MODEL | COMPUTE | 纯加权 专利年龄*w1+增长率*w2+覆盖度*w3 |
| 31 | `M_CHAIN_TREND_INDEX` | MODEL | COMPUTE | 纯加权 企业增速*w1+专利增速*w2+热度*w3+投融资*w4 |

### INNOV（4 条）

| # | metric_id | from | to | 理由 |
|---|---|---|---|---|
| 1 | `M_INNOV_DS_02_PATH_002` | MODEL | GRAPH | 关键节点重要性=图节点重要性(PageRank/中心性)，非评分模型 |
| 2 | `M_INNOV_DS_02_PATH_003` | MODEL | GRAPH | 节点优先级/重要度=图节点重要度，同 002 识别族 |
| 3 | `M_INNOV_DS_04_CARRIER_RANK_002` | MODEL | MIXED | 多维度排名展示，对齐同语义赋号卡 M_INNOV_CARRIER_RANK_GLOBAL=MIXED |
| 4 | `M_INNOV_DS_09_RESEARCH_004` | MODEL | MIXED | 多企业竞争情报比对，对齐同语义赋号卡 M_INNOV_RES_CI_COMPARE=MIXED |

### ENT（28 条）

| # | metric_id | from | to | 理由 |
|---|---|---|---|---|
| 1 | `M_ENT_AGGLOMERATION_INDEX` | MODEL | COMPUTE | 区位熵/基尼系数固定指数公式 |
| 2 | `M_ENT_ATTRACT_SCORE` | GRAPH | COMPUTE | 线性加权 w_tech*proxy+w_growth*growth+...-risk 评分合成，非图 |
| 3 | `M_ENT_CULTIVATE_SCORE` | GRAPH | COMPUTE | 线性加权评分合成，非图 |
| 4 | `M_ENT_DIVERSIFICATION_INDEX` | MODEL | COMPUTE | Shannon 熵固定公式 |
| 5 | `M_ENT_DOMAIN_COVERAGE_DEPTH` | MODEL | COMPUTE | chain_score+产品/专利贡献加权 |
| 6 | `M_ENT_GROWTH_POTENTIAL` | MODEL | COMPUTE | 营收/研发增速+技术壁垒+团队规模加权 |
| 7 | `M_ENT_PAINPOINT_GAP` | MODEL | COMPUTE | 企业值-行业基线 差值计算，无模型 |
| 8 | `M_ENT_PAINPOINT_SEVERITY` | MODEL | COMPUTE | 降幅>30%/10-30%/<10% 阈值分档 |
| 9 | `M_ENT_RELATION_STRENGTH` | MODEL | COMPUTE | 投资金额 >1e8/[1e7,1e8)/<1e7 阈值分档 |
| 10 | `M_ENT_CHAIN_COMPLETENESS` | MODEL | STAT | 覆盖环节数/全链环节数*100 占比 |
| 11 | `M_ENT_CITY_AVG_TECH_POWER` | MODEL | STAT | AVG(tech_score) GROUP BY city 聚合 |
| 12 | `M_ENT_CITY_DENSITY` | MODEL | STAT | 企业数/面积或GDP 密度比值 |
| 13 | `M_ENT_COMPETITIVENESS_RANK` | MODEL | STAT | 按 score 降序排名（§2.1 STAT 含排名） |
| 14 | `M_ENT_CORE_SUPPLIER_COUNT` | MODEL | STAT | COUNT(DISTINCT) WHERE rank<=5 计数 |
| 15 | `M_ENT_DEV_HISTORY` | MODEL | STAT | 财务/专利/资讯 merge 时间线，数据整合非模型 |
| 16 | `M_ENT_DOMAIN_COVERAGE_BREADTH` | MODEL | STAT | 覆盖领域数/产业领域全集 占比 |
| 17 | `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT` | MODEL | STAT | 未来产业去重计数 |
| 18 | `M_ENT_KEYPANO_ENTERPRISE_LIST` | GRAPH | STAT | SELECT...JOIN...WHERE 查询列表，非图算法 |
| 19 | `M_ENT_KEYPANO_MATCH_COUNT` | GRAPH | STAT | COUNT(DISTINCT) FILTER 计数 |
| 20 | `M_ENT_KEYPANO_TYPE_STRUCTURE` | GRAPH | STAT | COUNT GROUP BY honor_type 分组计数 |
| 21 | `M_ENT_PROFIT_MARGIN` | MODEL | STAT | 净利润/营收*100 占比 |
| 22 | `M_ENT_RECOMMEND_COUNT` | MODEL | STAT | COUNT(DISTINCT) WHERE 指数>=阈值 计数 |
| 23 | `M_ENT_REGIONAL_DENSITY` | MODEL | STAT | 企业数/面积 密度比值 |
| 24 | `M_ENT_RESEARCHER_COUNT` | MODEL | STAT | 科研人员数合计 计数 |
| 25 | `M_ENT_REVENUE_LATEST` | MODEL | STAT | SELECT...ORDER BY...LIMIT 1 取最新值 |
| 26 | `M_ENT_STAR_ENTERPRISE_COUNT` | MODEL | STAT | 明星企业去重计数 |
| 27 | `M_ENT_SZ_CHAIN_POSITION` | MODEL | STAT | 直接取 ODS 产业链归属字段，无计算 |
| 28 | `M_ENT_TECH_RANK` | MODEL | STAT | RANK() OVER ORDER BY tech_score 排名 |

### SYNTH（5 条）

| # | metric_id | from | to | 理由 |
|---|---|---|---|---|
| 1 | `M_SYNTH_COLLAB_COMPLETENESS` | MODEL | STAT | 已建关系主体数/有效主体总数×100% 占比 |
| 2 | `M_SYNTH_ELEM_CONTRIB` | GRAPH | MIXED | 贡献度量化(关联分析模型)+影响路径识别(图) 组合 |
| 3 | `M_SYNTH_ELEM_INDEX` | MODEL | COMPUTE | 类型/层次/领域三维等权合成，无归一化/判定 |
| 4 | `M_SYNTH_ELEM_RANK` | MODEL | STAT | RANK(ELEM_INDEX) 排名（§2.1 STAT 含排名） |
| 5 | `M_SYNTH_VIT_RANK` | MODEL | STAT | RANK(VIT_INDEX) 排名 |

### SVC（15 条）

| # | metric_id | from | to | 理由 |
|---|---|---|---|---|
| 1 | `M_SVC_CHAIN_SEGMENT_AVG_DEPTH` | MODEL | STAT | 环节内机构服务深度均值 AVG |
| 2 | `M_SVC_CHAIN_SEGMENT_ORG_COUNT` | MODEL | STAT | 某环节服务机构去重计数 |
| 3 | `M_SVC_GRAPH_DENSITY` | MODEL | GRAPH | 可见子网无向密度 2E/[N(N-1)] 图算法 |
| 4 | `M_SVC_ORG_COVERAGE_BREADTH` | MODEL | STAT | 有服务记录的产业领域去重计数 |
| 5 | `M_SVC_ORG_NEW_COUNT` | MODEL | STAT | 按年新增机构计数 |
| 6 | `M_SVC_ORG_SELECTED_COUNT` | MODEL | STAT | 已确认集合机构计数 |
| 7 | `M_SVC_PT_CHAIN_NODE_ORG` | MODEL | STAT | 各服务链环节机构计数 |
| 8 | `M_SVC_PT_REGION_ORG` | MODEL | STAT | 区域机构计数 |
| 9 | `M_SVC_PT_SZ_TYPE_DIST` | MODEL | STAT | 深圳机构 OrgType 分布计数 |
| 10 | `M_SVC_REC_CANDIDATE_CNT` | MODEL | STAT | 候选机构数量计数 |
| 11 | `M_SVC_SZ_CHAIN_COMPLETENESS` | MODEL | STAT | 服务链完整度=覆盖占比 |
| 12 | `M_SVC_SZ_COMPARE_METRIC` | MODEL | STAT | 深圳/全国/北上广各对比指标取值读数 |
| 13 | `M_SVC_REC_ATTRACT_SCORE` | MODEL | COMPUTE | 四指标加权综合得分 |
| 14 | `M_SVC_REC_CULTIVATE_SCORE` | MODEL | COMPUTE | 四维度加权综合得分 |
| 15 | `M_SVC_SZ_TIER` | MODEL | COMPUTE | 深圳相对一线城市梯队分档（阈值分档） |

### POLICY（10 条）

| # | metric_id | from | to | 理由 |
|---|---|---|---|---|
| 1 | `M_POLICY_EFFECT_SCORE` | MODEL | COMPUTE | 执行效果*w1+社会经济*w2+环境影响*w3 纯加权 |
| 2 | `M_POLICY_FOCUS_INDEX` | MODEL | COMPUTE | 焦点维度指标体系加权打分 |
| 3 | `M_POLICY_IMPLEMENTATION_EFFECT` | MODEL | COMPUTE | 落地执行率+受益覆盖+反馈满意度加权 |
| 4 | `M_POLICY_INTENSITY_INDEX` | MODEL | COMPUTE | 补贴*w1+税收*w2+数量*w3+周期*w4 纯加权 |
| 5 | `M_POLICY_INTENSITY_SCORE` | MODEL | COMPUTE | 效果*w1+覆盖*w2+成本*w3 纯加权 |
| 6 | `M_POLICY_SUPPORT_STRENGTH` | STAT | COMPUTE | 扶持力度档位*w1+层级*w2+数量*w3 加权，非纯占比 |
| 7 | `M_POLICY_LAYOUT_REC_COUNT` | MODEL | STAT | COUNT(建议 WHERE 优先级>=阈值) 阈值计数 |
| 8 | `M_POLICY_OPPORTUNITY_COUNT` | MODEL | STAT | COUNT(政策 WHERE 阈值) 阈值计数 |
| 9 | `M_POLICY_SHORTBOARD_COUNT` | MODEL | STAT | COUNT(短板 WHERE 评估值<阈值) 阈值计数 |
| 10 | `M_POLICY_TYPE_DIST` | COMPUTE | STAT | COUNT(DISTINCT policy_id) GROUP BY type 分组计数 |

### TNIE（1 条）

| # | metric_id | from | to | 理由 |
|---|---|---|---|---|
| 1 | `M_TNIE_EVENT_COUNT` | MODEL | STAT | len(response.events) 数组长度计数，抽取是前置 LLM 而非本指标 |

## 四、需淮政玮/唐绍祖确认的决策点

1. **COMPUTE 边界（本次最大变化，30 条 MODEL→COMPUTE）**：§2.1 把「加权、标准化、阈值」明确归 COMPUTE（有公式但无模型）。因此把「纯加权合成指数」（如 `科研实力指数 = 专利密度*w1+论文密度*w2+高校*w3`）从 MODEL 改回 COMPUTE。
   - 区分标尺：**纯线性加权（w1+w2+w3，无归一化/等级/排名/主成分）→ COMPUTE；含归一化/等级/排名/主成分/预测/聚类 → MODEL**。
   - 佐证：赋号卡 `M_ORG_ATTENTION_TREND` 也明确「指数合成（无训练）→ COMPUTE」；A1 表2 的正式 M_ENT_* 多维加权（如 `COMPETITIVENESS_SCORE` 四维加权+极值归一化）仍是 MODEL。
   - 注意：A1 已签的 101 条（含 TTEMP 90 + T1 11）**未动**，其中若存在「无归一化的纯加权」被判 MODEL（如 `M_ENT_TECH_POWER_SCORE` 五维加权平均）属 A1 历史口径，不在本次重判范围，可另议。

2. **排名归 STAT**：§2.1 明确 STAT 含「排名」，故 `RANK() OVER ORDER BY` 类（如 `M_ENT_TECH_RANK`、`M_SYNTH_ELEM_RANK`）从 MODEL 改 STAT。

3. **关键节点重要性/节点优先级 → GRAPH**：属图节点重要性（PageRank/中心性），非评分模型，从 MODEL 改 GRAPH。

## 五、淮政玮终签（2026-08-25）

1. **范围**：522 条全部纳入，本叶签 `done`。
2. **差 1 条**：`M_ENT_KEY_TOTAL`（重点企业总数）。它在签收草表里算 **T3 #108**（计入 156+276=432），重判时被标成 **T1 #6 冻结**（T1 写成 11=原 10 条+本条），所以重判分母写成 431。类型仍是 `STAT`，只是分组双计，不是漏回填。
3. **COMPUTE 新口径**（淮政玮）：加权合成若子指标本身是评价模型产出（如专利密度、论文密度、评分、壁垒），归 **MODEL**，不归 COMPUTE。示例：`科研实力指数 = 专利密度*w1+论文密度*w2+高校*w3` → MODEL。
4. **已回退**：上表 30 条 `MODEL→COMPUTE` 已全部改回 `MODEL`（`rejudge/_apply_compute_to_model_rollback.mjs --apply`）。种子侧现分布：`STAT=164, MODEL=228, GRAPH=53, COMPUTE=7, MIXED=33, third_party=47`。
5. **仍留 COMPUTE 的 7 条**（非这 30 条，未动）：`M_CHAIN_CONCENTRATION_INDEX`（HHI）、`M_CHAIN_INTERNATIONALIZATION_INDEX`、`M_ENT_ATTRACT_SCORE`、`M_ENT_CULTIVATE_SCORE`、`M_ORG_ATTENTION_TREND`、`M_POLICY_SUPPORT_STRENGTH`、`M_TECH_COMPOSITE_SCORE`。根目录 `_seed_*.mjs` 先不整理。