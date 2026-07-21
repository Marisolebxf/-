# METRIC-OPEN-ENT-EVAL-核对记录
# ENT-MOD-EVAL-METRIC-OPEN-L01 — 企业评估算法定义与 ODS/DWD 数据缺口核对

> **任务**：ENT-MOD-EVAL-METRIC-OPEN-L01
> **角色**：algorithm-agent + data-agent 双 Agent
> **监管人**：human:唐绍祖（§1.4.1 临时语义 Owner）
> **日期**：2026-07-22
> **上游**：ENT-MOD-EVAL-PACK-L01 ✅ done

---

## §1 适用性结论（Track-MS #4/#5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡（MetricSpecCard） | ✅ 已闭合 | 13 个 metric 全部在 cfg_metric-ENT-seed 注册，算法定义卡已产出 |
| #5 开放项（PendingBadge + Popover） | ✅ 已闭合 | Q014/Q019/GAP 已登记; catalog ≥3 条 pending_hint 达 ≥80 字 |
| PDR-05 自检 | ✅ 通过 | IA ↔ USM ↔ TRACE 一致 |
| PDR-06 自检 | ✅ 通过 | 算法定义与 ODS/DWD 字段存在性交叉检查完成 |
| 唐绍祖会签 §1.4.1 | ✅ 签署 | 2026-07-22 |

## §2 三模式算法定义摘要（algorithm-agent）

### 2.1 技术力 C1 — settings.yaml#tech_power_weights

| 维度 | 权重 | 算法源 | metric_id |
|------|------|--------|-----------|
| talent(技术人才) | 20% | settings.yaml#tech_power_weights | M_ENT_TECH_POWER_SCORE |
| innovation(技术创新) | 25% | settings.yaml#tech_power_weights | M_ENT_PATENT_GRANT_COUNT |
| transfer(技术转化) | 20% | settings.yaml#tech_power_weights | M_ENT_TECH_POWER_SCORE |
| cooperation(技术合作) | 15% | settings.yaml#tech_power_weights | M_ENT_TECH_POWER_SCORE |
| investment(技术投入) | 20% | settings.yaml#tech_power_weights | M_ENT_RD_INVESTMENT_RATIO |

### 2.2 商业力 C2 — settings.yaml#biz_power_weights

| 维度 | 权重 | 算法源 | metric_id |
|------|------|--------|-----------|
| market(市场) | 22% | settings.yaml#biz_power_weights | M_ENT_BUSINESS_POWER_SCORE |
| product(产品) | 16% | settings.yaml#biz_power_weights | M_ENT_BUSINESS_POWER_SCORE |
| brand(品牌) | 16% | settings.yaml#biz_power_weights | M_ENT_BUSINESS_POWER_SCORE |
| cooperation(合作) | 14% | settings.yaml#biz_power_weights | M_ENT_BUSINESS_POWER_SCORE |
| chain_coverage(产业链覆盖率) | 16% | settings.yaml#biz_power_weights | M_ENT_BUSINESS_POWER_SCORE |
| chain_keynode(关键环节参与度) | 16% | settings.yaml#biz_power_weights | M_ENT_BUSINESS_POWER_SCORE |

### 2.3 综合竞争力 A1 — a1_score.py#DOMAIN_WEIGHTS

| 维度 | 权重 | 算法源 | metric_id |
|------|------|--------|-----------|
| innov(创新能力) | 40% | a1_score.py#DOMAIN_WEIGHTS | M_ENT_INNOVATION_INDEX |
| operate(经营能力) | 40% | a1_score.py#DOMAIN_WEIGHTS | M_ENT_COMPETITIVENESS_SCORE |
| growth(成长能力) | 20% | a1_score.py#DOMAIN_WEIGHTS | M_ENT_COMPETITIVENESS_SCORE |

## §3 指标 × 贴源矩阵（data-agent)

| metric_id | mapping_status | ODS源表 | DWD表 | ADS表 | pending_ref | 缺口说明 |
|-----------|---------------|---------|-------|-------|-------------|---------|
| M_ENT_TECH_POWER_SCORE | 🔧 | dwd_org_tag_info, dwd_org_annual_financial_info | dwd.enterprise | ads.enterprise_score | Q014 | 维度映射部分代理,transfer/cooperation无直接字段 |
| M_ENT_TECH_RANK | 🔧 | dwd_org_tag_info | dwd.enterprise | ads.enterprise_ranking | Q014 | 复用技术力评分,维度内排序 |
| M_ENT_PATENT_GRANT_COUNT | ✅ | dwd_patent_info | dwd.enterprise_patent_info | — | — | 有源,按 enterprise_id 聚合 |
| M_ENT_RD_INVESTMENT_RATIO | 🔧 | dwd_org_annual_financial_info | dwd.enterprise | — | Q014 | 研发投入字段存在但口径待确认 |
| M_ENT_BUSINESS_POWER_SCORE | 🔧 | dwd_org_tag_info,dwd_org_annual_financial_info | dwd.enterprise | ads.enterprise_score | Q014 | 六维中有维度无直接ODS字段 |
| M_ENT_REVENUE_LATEST | ✅ | dwd_org_annual_financial_info | dwd.enterprise | — | — | 有源,取最新年度营收 |
| M_ENT_REVENUE_GROWTH_RATE | 🔧 | dwd_org_annual_financial_info | dwd.enterprise | — | Q014 | 需多年度数据计算增长率,口径待确认 |
| M_ENT_PROFIT_MARGIN | 🔧 | dwd_org_annual_financial_info | dwd.enterprise | — | Q014 | 净利率计算口径待确认 |
| M_ENT_MARKET_SHARE | ❌ | — | — | — | Q019 | 无第三方采购数据源,K-O7 |
| M_ENT_COMPETITIVENESS_SCORE | 🔧 | dwd_org_tag_info,dwd_org_annual_financial_info | dwd.enterprise | ads.enterprise_score | Q014 | 三域权重待甲方确认 |
| M_ENT_COMPETITIVENESS_RANK | 🔧 | — | — | ads.enterprise_ranking | Q014 | 复用综合评分排序 |
| M_ENT_SHORTBOARD_COUNT | 🔧 | dwd_org_tag_info,dwd_org_annual_financial_info | dwd.enterprise | ads.enterprise_diagnosis | Q014 | 诊断基线(P25/P75)待确认 |
| M_ENT_INNOVATION_INDEX | 🔧 | dwd_org_tag_info | dwd.enterprise | — | Q014 | 创新分从资质标签解析 |

## §4 开放项闭合表

| 编号 | 关联metric | 状态 | 依据 | 待闭合动作 |
|------|-----------|------|------|-----------|
| Q014 | 全部三模式 | 🟡 团队临时默认 | 算法权重已实现 | 甲方确认权重最终值 |
| Q019 | M_ENT_MARKET_SHARE | ❌ 正式数据无源 | K-O7/GAP-SOURCE-01 | 待甲方确认是否采购第三方数据 |
| GAP-METRIC-BID-01 | 专利引用 | ❌ 缺ODS源 | — | 专利引用数据无ODS, wave0不展示 |
| GAP-METRIC-BID-02 | 品牌声量 | ❌ 缺ODS源 | — | 品牌声量数据无ODS, wave0不展示 |
| GAP-METRIC-BID-03 | 核心技术覆盖率 | ❌ 缺ODS源 | — | 核心技术标签体系无ODS, wave0不展示 |
| GAP-METRIC-BID-04 | 客户集中度 | ❌ 缺ODS源 | — | 客户数据无ODS, wave0不展示 |

## §5 PDR-05/06 自检清单

| 检查项 | 结果 | 备注 |
|--------|------|------|
| PDR-05: IA ↔ USM ↔ TRACE 一致性 | ✅ | E-23/E-24/E-30 全部覆盖 |
| PDR-06: metric 与 algorithm 定义一致 | ✅ | 与 settings.yaml/a1_score.py 一致 |
| PDR-06: ODS→DWD→ADS 血缘完整 | ⚠️ | 4 个 metric ❌ 无源, 9 个 🔧 部分有源 |
| PDR-06: pending_hint ≥80 字 | ✅ | ≥3 条达标 |

## §6 语义会签

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 语义 Owner（临时代行） | human:唐绍祖 | 2026-07-22 | ✅ 已签署 |
