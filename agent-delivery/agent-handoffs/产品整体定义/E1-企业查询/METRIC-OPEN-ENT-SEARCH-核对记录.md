# METRIC-OPEN-ENT-SEARCH-核对记录
# ENT-MOD-SEARCH-METRIC-OPEN-L01 — 企业查询指标语义与 ODS/DWD 缺口核对

> **任务**：ENT-MOD-SEARCH-METRIC-OPEN-L01
> **角色**：algorithm-agent + data-agent 双 Agent
> **监管人**：human:唐绍祖（§1.4.1 临时语义 Owner）
> **日期**：2026-07-22
> **上游**：ENT-MOD-SEARCH-PACK-L01 ✅ done

---

## §1 适用性结论（Track-MS #4/#5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡（MetricSpecCard） | ✅ 已闭合 | 12 个 metric 中 11 个已映射, 1 个待 Q019 闭合 |
| #5 开放项（PendingBadge + Popover） | ✅ 已闭合 | Q033~Q037 已登记; ≥2 条 pending_hint 达字段级粒度 |
| PDR-05 自检 | ✅ 通过 | IA ↔ USM ↔ TRACE 一致 |
| PDR-06 自检 | ✅ 通过 | metric ↔ definition ↔ source_tables 一致 |
| #5 开放项更正（2026-08-05） | ✅ 已闭合 | Q037=空态推荐≤30 条（非明星定义）；明星定义改挂 Q041/Q048 |
| 算法共签（方案 B） | human:唐绍祖 | 2026-08-05 | ✅ 已签署（Q037 错挂已更正） |
| 口径主责（方案 B） | human:王惠 | — | ⏳ 待王惠口径会签 |

## §2 检索指标口径摘要（algorithm-agent）

### 2.1 列表卡片 KPI（检索结果展示）

| metric_id | 中文名 | 定义 | 公式 | 源表 | 状态 |
|-----------|--------|------|------|------|------|
| M_ENT_TECH_POWER_SCORE | 技术力评分 | 企业技术力五维加权评分，按 enterprise_code 展示 | tech_power_weights(talent,innovation,transfer,cooperation,investment) | ads.enterprise_score | 🔧 algorithm 已实现 |
| M_ENT_PATENT_TOTAL | 专利总数 | 企业专利总申请数（含发明/实用/外观） | COUNT(DISTINCT patent_id) | dwd.enterprise_patent_info | ✅ 有源 |
| M_ENT_HIGH_TECH_COUNT | 高企数量 | 高新技术企业认定数（按年度） | COUNT(DISTINCT enterprise_id WHERE is_high_tech=1) | dwd.enterprise_honor_tags | ⚠️ Q011 口径待确认 |
| M_ENT_BUSINESS_POWER_SCORE | 商业力评分 | 企业商业力六维加权评分 | biz_power_weights(market,product,brand,cooperation,chain_coverage,chain_keynode) | ads.enterprise_score | 🔧 algorithm 已实现 |
| M_ENT_COMPETITIVENESS_SCORE | 综合竞争力 | 企业综合竞争力三域评分 | DOMAIN_WEIGHTS(innov=0.40,operate=0.40,growth=0.20) | ads.enterprise_score | 🔧 algorithm 已实现 |
| M_ENT_DOMAIN_COVERAGE_BREADTH | 领域覆盖面 | 企业产业/技术标签覆盖领域数 | COUNT(DISTINCT industry_tag) | dwd.enterprise_industry_tags | 🔧 formula 待注册 |
| M_ENT_SUPPLY_CHAIN_RISK | 供应链风险 | 企业供应链风险总评分 | SUM(risk_weight * risk_score) | ads.realdata_enterprise_risk | 🔧 algorithm 已实现 |
| M_ENT_STAR_ENTERPRISE_COUNT | 明星企业数 | 深圳明星企业按条件筛选计数 | COUNT(DISTINCT enterprise_id) FILTER(is_star) | dwd.enterprise_honor_tags | ⚠️ Q041/Q048 口径待确认 |

### 2.2 检索交互口径

| 开放项 | 说明 | 临时默认 |
|--------|------|---------|
| Q033 | 智能搜索多字段匹配范围 | 企业名称 + USCC + 产业/技术标签, 非 NL/LLM |
| Q034 | 排序字段与默认排序 | 默认按竞争力降序; 排序选项: 竞争力/专利/营收/成立时间 |
| Q035 | 导出上限 | ≤1000 条, CSV 格式, 含当前可见列 |
| Q036 | 高级筛选字段范围 | 字段库简化版, 无 AND/OR 嵌套; 每次增删按配置重新查询 |
| Q037 | 空态推荐默认展示重点/明星企业列表 ≤30 条，不按用户行为个性化 | 搜索结果为空时展示固定重点/明星企业列表 ≤30 条 |
| Q041 | 明星企业定义：固定明星企业表；基础指标我方出数；CMS 人工维护视频/团队/介绍 | 暂取资质标签 is_star=true; 待甲方确认正式口径（详见 Q041 客户决策清单） |
| Q048 | E-34 明星企业候选名单、发布准入、sort_order、入选标准 | 待 ENT-MOD-STAR-PACK-L01 闭合后对齐名单与 sort_order |

## §3 指标 × 贴源矩阵（data-agent）

> 2026-08-05 更正：原矩阵仅 5 行，现补齐至 9 条与 catalog 完全对齐。

| metric_id | mapping_status | ODS | DWD | ADS | pending_ref | pending_hint |
|-----------|---------------|-----|-----|-----|-------------|-------------|
| M_ENT_TECH_POWER_SCORE | 🔧 | dwd_org_tag_info,dwd_org_annual_financial_info | dwd.enterprise | ads.enterprise_score | Q014 | 技术力五维中有部分维度(transfer,cooperation)当前 ODS 无直接字段, 使用资质标签代理。详见 cfg_metric Q014。 |
| M_ENT_PATENT_TOTAL | ✅ | dwd_patent_info | dwd.enterprise_patent_info | — | — | 数据可用。源自企业专利信息表, 按 enterprise_id 聚合。 |
| M_ENT_HIGH_TECH_COUNT | ⚠️ | dwd_org_honor_info | dwd.enterprise_honor_tags | — | Q011 | 高企口径待甲方确认(是否包含过期认定)。当前取 is_high_tech=true 的标签记录, 按 enterprise_id 去重。 |
| M_ENT_BUSINESS_POWER_SCORE | 🔧 | dwd_org_tag_info,dwd_org_annual_financial_info | dwd.enterprise | ads.enterprise_score | Q014 | 商业力六维加权评分。市场维度份额数据依赖 M_ENT_MARKET_SHARE, wave0 暂以营收替代。正式评分需甲方确认权重分配方案(Q014)。 |
| M_ENT_COMPETITIVENESS_SCORE | 🔧 | dwd_org_tag_info,dwd_org_annual_financial_info | dwd.enterprise | ads.enterprise_score | Q014 | 综合竞争力评分=创新能力(40%)+经营能力(40%)+成长能力(20%)。正式数据需甲方确认三域权重与评分标准(Q014)。 |
| M_ENT_DOMAIN_COVERAGE_BREADTH | 🔧 | dwd_enterprise_industry_tags | dwd.enterprise_industry_tags | — | Q013 | 领域覆盖面统计企业所属产业/技术标签的去重覆盖数。当前 ODS 层标签分类体系与业务口径是否一致待甲方确认(Q013)。 |
| M_ENT_SUPPLY_CHAIN_RISK | 🔧 | dwd_org_credit_info,dwd_org_penalty_info | dwd.enterprise_risk_events | ads.realdata_enterprise_risk | Q017 | 供应链风险评分由失信(3.0)+异常(1.5)+处罚(1.0)三类事件加权 min-max 归一化。正式阈值与等级划分(Q017)需甲方确认。 |
| M_ENT_MARKET_SHARE | ❌ | — | — | — | Q019 | 市场份额数据无第三方采购, wave0 暂不展示该指标。指标卡片置灰并显示"数据筹备中"。 |
| M_ENT_STAR_ENTERPRISE_COUNT | ⚠️ | dwd_org_honor_info | dwd.enterprise_honor_tags | — | Q041/Q048 | 明星企业定义待甲方确认。当前临时取资质标签含"市/区明星企业"标记的企业。正式口径见 Q041（明星定义）与 Q048（候选名单/sort_order）。 |

## §4 开放项闭合表

| 编号 | metric_id | 当前状态 | 依据 | 待闭合动作 |
|------|-----------|---------|------|-----------|
| Q010 | — | 🟡 团队临时默认 | PDR 纪要 | 甲方确认企业画像指标范围 |
| Q011 | M_ENT_HIGH_TECH_COUNT | 🟡 团队临时默认 | PDR 纪要 | 甲方确认高企口径及有效期 |
| Q013 | M_ENT_DOMAIN_COVERAGE_BREADTH | 🟡 团队临时默认 | PDR 纪要 | 甲方确认领域覆盖分类体系 |
| Q017 | M_ENT_SUPPLY_CHAIN_RISK | 🟢 临时默认闭合（2026-08-11） | E-28 PACK | 监管人指示按临时默认升格基线；cfg_metric + FE 镜像已落地 |
| Q019 | M_ENT_MARKET_SHARE | ❌ 正式数据无源 | K-O7/GAP-SOURCE-01 | 待甲方确认是否采购第三方数据 |
| Q033 | 检索能力 | 🟡 团队临时默认 | Decision 042~083 | 待甲方确认智能搜索范围 |
| Q034 | 排序/结果展示 | 🟡 团队临时默认 | — | 待甲方确认默认排序与双视图需求 |
| Q035 | 导出上限 | 🟡 团队临时默认 | — | 待甲方确认导出条数上限 |
| Q036 | 高筛字段 | 🟡 团队临时默认 | — | 待甲方确认字段库版本 |
| Q037 | 空态推荐（≤30 条） | 🟡 团队临时默认 | 客户决策清单 | 待甲方确认空态推荐展示条数与是否个性化 |
| Q041 | M_ENT_STAR_ENTERPRISE_COUNT | 🟡 团队临时默认 | 客户决策清单 · 明星企业定义 | 待甲方确认明星企业正式定义（固定明星企业表 + CMS + 基础指标） |
| Q048 | M_ENT_STAR_ENTERPRISE_COUNT | 🟡 团队临时默认 | 客户决策清单 · 明星名单/sort_order | 待 ENT-MOD-STAR-PACK-L01 闭合后对齐候选名单与 sort_order |

## §5 PDR-05/06 自检清单

| 检查项 | 结果 | 备注 |
|--------|------|------|
| PDR-05: IA ↔ USM ↔ TRACE 一致性 | ✅ | 16 leaves 全部映射 |
| PDR-05: wireframe 覆盖度 | ✅ | 各 USM 均有 wireframe 对应 |
| PDR-06: metric ↔ definition 一致性 | ✅ | cfg_metric 12/11 已映射 |
| PDR-06: source_tables 完整度 | ⚠️ | 1 个 metric (M_ENT_MARKET_SHARE) 无源 |
| PDR-06: pending_hint ≥80 字 | ✅ | ≥2 条达标 |

## §6 语义会签

> 2026-08-05 更新：按方案 B §1.4.2 双签格式重写。

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 算法共签 | human:唐绍祖 | 2026-08-05 | ✅ 已签署（Q037 错挂已更正；§3 矩阵补齐至 9 条与 catalog 对齐） |
| 口径主责 | human:王惠 | — | ⏳ 待王惠口径会签（方案 B 铁律，缺一不可） |
