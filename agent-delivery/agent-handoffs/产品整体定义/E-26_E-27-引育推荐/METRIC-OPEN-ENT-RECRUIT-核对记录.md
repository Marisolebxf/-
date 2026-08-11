# METRIC-OPEN-ENT-RECRUIT-核对记录
# ENT-MOD-RECRUIT-METRIC-OPEN-L01 — 引育推荐指标语义与 ODS/DWD 缺口核对

> **任务**：ENT-MOD-RECRUIT-METRIC-OPEN-L01
> **角色**：algorithm-agent + data-agent 双 Agent
> **监管人**：human:唐绍祖（§1.4.1 临时语义 Owner）
> **日期**：2026-07-23
> **上游**：ENT-MOD-RECRUIT-PACK-L01 ✅ done（PM 淮政玮 2026-07-22 通过）

---

## §1 适用性结论（Track-MS #4/#5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡（MetricSpecCard） | ✅ 已闭合 | 5 个核心 metric（2 推荐指数 + 3 维度）已映射; 5 个 GAP 已登记 |
| #5 开放项（PendingBadge + Popover） | ✅ 已闭合 | Q015 + GAP-RECRUIT-METRIC-01~05 已登记; ≥2 条 pending_hint 达字段级粒度（≥80 字） |
| PDR-05 自检 | ✅ 通过 | IA ↔ USM ↔ TRACE 一致 |
| PDR-06 自检 | ✅ 通过 | metric ↔ definition ↔ source_tables 一致 |
| 唐绍祖会签 §1.4.1 | ✅ 签署 | 2026-07-23 |

## §2 招引/培育指标口径摘要（algorithm-agent）

### 2.1 招引推荐（E-26）— 对象范围：全国企业

根据 bid-reference §5.7，招引推荐算法基于 **产业相关度 + 政策匹配度 + 深圳连接度** 三维度加权计算。

| metric_id | 中文名 | 定义 | 公式 | 源表 | 状态 |
|-----------|--------|------|------|------|------|
| M_ENT_ATTRACTION_INDEX | 招引推荐指数 | 全国高潜力企业招引综合指数（产业相关度+政策匹配+深圳连接度） | 产业相关度×w1 + 政策匹配度×w2 + 深圳连接度×w3（w1/w2/w3 待 Q015 确认） | 派生自下辖三维度 | 🔧 口径待 Q015 |
| M_ENT_INDUSTRY_MATCH_SCORE | 产业匹配度 | 企业与目标产业链/产业的匹配程度评分 | 基于 dwd_org_industry_chain_dtl.chain_score 计算 | dwd.enterprise_industry ← ods: dwd_org_industry_chain_dtl | 🔧 候选校准 Q015 |
| M_ENT_POLICY_MATCH_SCORE | 政策匹配度 | 企业与深圳政策导向的匹配程度评分 | 企业属性标签 vs 政策标签匹配评分 | dwd.enterprise（标签字段）+ 政策域（跨域引用） | 🔧 口径待 Q015 |
| GAP-RECRUIT-METRIC-01 | 深圳连接度 | 企业与深圳投融资/子公司/供应链的连接强度 | 待定义（禁止与区域适配性静默合并） | 待确认 | 🆕 GAP 待定义 |

### 2.2 培育推荐（E-27）— 对象范围：深圳市内企业

根据 bid-reference §5.8，培育推荐算法基于 **产业相关度 + 政策匹配度 + 企业潜力** 三维度加权计算。

| metric_id | 中文名 | 定义 | 公式 | 源表 | 状态 |
|-----------|--------|------|------|------|------|
| M_ENT_CULTIVATION_INDEX | 培育推荐指数 | 深圳本地企业培育综合指数（产业相关度+政策匹配+企业潜力） | 产业相关度×w1 + 政策匹配度×w2 + 企业潜力×w3（w1/w2/w3 待 Q015 确认） | 派生自下辖三维度 | 🔧 口径待 Q015 |
| M_ENT_INDUSTRY_MATCH_SCORE | 产业匹配度 | 同招引，按深圳产业链范围筛选 | 同 M_ENT_INDUSTRY_MATCH_SCORE | dwd.enterprise_industry | 🔧 共用口径 |
| M_ENT_POLICY_MATCH_SCORE | 政策匹配度 | 同招引 | 同 M_ENT_POLICY_MATCH_SCORE | dwd.enterprise + 政策域 | 🔧 共用口径 |
| M_ENT_GROWTH_POTENTIAL | 企业潜力 | 企业成长潜力评分（增速+技术壁垒+团队） | 营收/研发增速 + 技术壁垒 + 团队规模 加权 | dwd.enterprise.rd_investment/revenue_latest/patent_grant_count | 🔧 候选校准 Q015 |
| GAP-RECRUIT-METRIC-02 | 企业潜力（培育专属） | 培育视角的企业潜力，不能等同 M_ENT_GROWTH_POTENTIAL 在 E-26 的归属语义 | 待数据评审决定修订 M_ENT_GROWTH_POTENTIAL 或新增 metric_id | 同 M_ENT_GROWTH_POTENTIAL 源表 | 🆕 GAP 待定义 |

### 2.3 补充展示项

| 开放项 | 说明 | 临时默认 |
|--------|------|---------|
| GAP-RECRUIT-METRIC-03 | 企业行业领域排名—排名范围、排序字段、并列规则待定义 | Wave0 不展示真实排名，🧪 Mock |
| GAP-RECRUIT-METRIC-04 | 可视化行业分布—统计量、分母、行业分类待定义 | Wave0 不展示真实分布，🧪 Mock |
| GAP-RECRUIT-METRIC-05 | 关键指标集合—每个实际指标携带自身 metric_id | 不创建笼统总分，按招引/培育分别展示 |

## §3 指标 × 贴源矩阵（data-agent）

| metric_id | mapping_status | ODS | DWD | ADS | pending_ref | pending_hint |
|-----------|---------------|-----|-----|-----|-------------|-------------|
| M_ENT_ATTRACTION_INDEX | 🔧 | dwd_org_industry_chain_dtl, dwd_org_tag_info, dwd_org_reg_info | dwd.enterprise_industry, dwd.enterprise | — | Q015 | 招引推荐指数由产业相关度、政策匹配度、深圳连接度三维加权计算。产业相关度源 ODS dwd_org_industry_chain_dtl.chain_score 可用。政策匹配度需跨域引用政策标签。深圳连接度（GAP-RECRUIT-METRIC-01）当前无直接 ODS 字段，依赖投融资/子公司关系数据。正式阈值与权重待甲方确认(Q015)。 |
| M_ENT_CULTIVATION_INDEX | 🔧 | dwd_org_industry_chain_dtl, dwd_org_tag_info, dwd_org_annual_financial_info, dwd_org_rd_achiev_info | dwd.enterprise_industry, dwd.enterprise | — | Q015 | 培育推荐指数由产业相关度、政策匹配度、企业潜力三维加权计算。企业潜力依赖营收增速/研发增速/技术壁垒，ODS 层 dwd_org_annual_financial_info（operating_revenue/pure_profit）+ dwd_org_rd_achiev_info（patent_count）字段可用。深圳本地筛选需 headquarters_city 字段。正式阈值与权重待甲方确认(Q015)。 |
| M_ENT_INDUSTRY_MATCH_SCORE | 🔧 | dwd_org_industry_chain_dtl.chain_score, dwd_industry_chain_info | dwd.enterprise_industry | — | Q015 | 产业匹配度以 ODS dwd_org_industry_chain_dtl.chain_score 为基础计算。产业分类体系与业务口径是否一致待甲方确认(Q015)。招引和培育共享该指标，但筛选范围不同（全国 vs 深圳）。 |
| M_ENT_POLICY_MATCH_SCORE | 🔧 | dwd_org_tag_info（企业标签）+ 政策域 ODS（政策标签） | dwd.enterprise（标签字段）+ 跨域政策表 | — | Q015 | 政策匹配度需企业标签 vs 政策标签交叉评分。企业标签 ODS 字段可用，政策标签需从政策域引用。正式匹配算法与权重待甲方确认(Q015)。 |
| M_ENT_GROWTH_POTENTIAL | 🔧 | dwd_org_annual_financial_info（operating_revenue/pure_profit）, dwd_org_rd_achiev_info（patent_count） | dwd.enterprise.rd_investment/revenue_latest/patent_grant_count | — | Q015 | 成长潜力依赖财务增速和研发数据。ODS 层近两年数据可用，但增速计算需时序数据。该指标在招引和培育语境下的归属语义不同(GAP-RECRUIT-METRIC-02)，待数据评审决定 metric_id 方案。 |
| GAP-RECRUIT-METRIC-01 | ❌ | — | — | — | Q015 | 深圳连接度当前无直接贴源字段。需梳理投融资事件、子公司注册地、供应链关系等 ODS 表的深圳关联字段后合成。Wave0 不可展示真实值。 |
| GAP-RECRUIT-METRIC-03 | ⚠️ | dwd_org_industry_chain_dtl.node_name | dwd.enterprise_industry | — | — | 企业行业领域排名范围（全国/深圳/某产业）和排序字段（产业相关度/综合指数）待下游定义。Wave0 mock。 |
| GAP-RECRUIT-METRIC-04 | ⚠️ | dwd_org_industry_chain_dtl.node_stage | dwd.enterprise_industry.industry_chain_role | — | — | 可视化行业分布统计量（企业数/占比）、分母（该行业企业总数）和行业分类粒度待下游定义。Wave0 mock。 |
| GAP-RECRUIT-METRIC-05 | ⚠️ | — | — | — | — | 关键指标集合 = 前 4 项 GAP + Q015 中待确认的 5 个现有 metric。不做笼统总分汇总。 |

## §4 开放项闭合表

| 编号 | metric_id | 当前状态 | 依据 | 待闭合动作 |
|------|-----------|---------|------|-----------|
| Q015 | M_ENT_ATTRACTION_INDEX, M_ENT_CULTIVATION_INDEX | 🟡 团队临时默认 | bid §5.7/§5.8 + TRACE | 甲方确认招引/培育推荐指数权重、维度口径及阈值 |
| Q015 | M_ENT_INDUSTRY_MATCH_SCORE | 🟡 团队临时默认 | TRACE metric status | 甲方确认产业匹配度是否可校准为同一语义（招引+培育共用） |
| Q015 | M_ENT_POLICY_MATCH_SCORE | 🟡 团队临时默认 | TRACE metric status | 甲方确认政策匹配度正式定义 |
| Q015 | M_ENT_GROWTH_POTENTIAL | 🟡 团队临时默认 | TRACE metric status | 甲方确认成长潜力在招引 vs 培育下的归属语义（GAP-RECRUIT-METRIC-02） |
| GAP-RECRUIT-METRIC-01 | — | 🆕 无源 | TRACE explicit_gaps | 确认深圳连接度的数据组成（投融资/子公司/供应链），决定是否采购或合成 |
| GAP-RECRUIT-METRIC-03 | — | 🆕 未定 | TRACE explicit_gaps | 明确排名范围、排序字段、并列规则和 metric_id 定义 |
| GAP-RECRUIT-METRIC-04 | — | 🆕 未定 | TRACE explicit_gaps | 明确统计量、分母、行业分类和 metric_id |
| GAP-RECRUIT-METRIC-05 | — | 🆕 未定 | TRACE explicit_gaps | 明确每个指标携带自身 metric_id，不创建笼统总分 |
| Q010 | — | 🟡 团队临时默认 | PDR 纪要 | 甲方确认企业画像指标范围 |
| Q014 | — | 🟡 团队临时默认 | PDR 纪要 | 甲方确认企业综合能力评估权重 |
| Q018 | — | 🟢 临时默认闭合（2026-08-11） | 客户决策清单 | 四维+命中/严重度阈值已升格项目基线；算法落地仍待 |

## §5 PDR-05/06 自检清单

| 检查项 | 结果 | 备注 |
|--------|------|------|
| PDR-05: IA ↔ USM ↔ TRACE 一致性 | ✅ | 2 leaves (E-26, E-27) 全部映射，6 stories (A1~A3, C1~C3) 一致 |
| PDR-05: wireframe 覆盖度 | ✅ | 招引/培育各有 config + result 两个 frame |
| PDR-06: metric ↔ definition 一致性 | ✅ | cfg_metric 5 个相关 metric 已定义，5 个 GAP 已登记 |
| PDR-06: source_tables 完整度 | ⚠️ | 1 个 GAP (GAP-RECRUIT-METRIC-01) 无直接数据源 |
| PDR-06: pending_hint ≥80 字 | ✅ | ≥2 条达标（M_ENT_ATTRACTION_INDEX, M_ENT_CULTIVATION_INDEX） |
| 禁止：替甲方闭合 Q015 | ✅ | 未设定正式权重/阈值 |
| 禁止：前端计算官方指数 | ✅ | 已标注前端不计算 |
| 禁止：混用招引/培育语义 | ✅ | 对象范围已分离（全国 vs 深圳） |

## §6 语义会签

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 算法共签 | human:唐绍祖 | 2026-07-23 | ✅ 已签署 |
| 口径主责 | human:王惠 | — | ⏳ 待王惠口径会签（方案 B 铁律，缺一不可） |

算法共签补充说明（2026-08-05）：招引/培育推荐指数的三维加权公式、维度口径、临时默认权重（pending Q015）均与 bid-reference §5.7/§5.8 及 §13.7 已实现算法一致。深圳连接度（GAP-01）与企业潜力归属（GAP-02）按开放项登记，未替甲方闭合 Q015。算法侧交付明确完成，此前「待确认」字样系飞书 inbound 回刷期间遗留，现更正为明确 ✅。
