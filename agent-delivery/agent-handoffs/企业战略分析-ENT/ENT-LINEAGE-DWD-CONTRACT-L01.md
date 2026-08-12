# ENT-LINEAGE-DWD-CONTRACT-L01 — 任务完成说明
# 企业维度 — 项目自研 DWD 契约样板（主表 + 指标支撑字段）

> **任务**：ENT-LINEAGE-DWD-CONTRACT-L01
> **角色**：data-agent / lineage-subcoord（唐绍祖认领推进）
> **监管人**：human:王惠（口径主责）/ human:唐绍祖（算法共签）
> **日期**：2026-08-10（初版，唐绍祖认领并完成 DWD 契约落盘）
> **产出**：1 张企业主表 DWD 契约（40 字段 / 6 组 / 全量 ods_mapping_expectation）

---

## 1. 任务概述

根据 task-registry.yaml 中 ENT-LINEAGE-DWD-CONTRACT-L01 的派单说明（方案 B / Phase 1），完成项目自研 DWD 企业主表契约样板的设计与落盘。

本任务是 ENT 域数据血缘治理的基础设施任务，产出物为设计契约文档，不涉及代码或数据库操作。Phase 1（~2026-08-20，ODS 未稳定）只治理项目 DWD 设计；Phase 2（8/20 后）由 GDF 对照本契约的 ods_mapping_expectation 做 ODS→DWD 字段级映射。

### 1.1 任务基本信息

| 项 | 内容 |
|----|------|
| 任务编码 | ENT-LINEAGE-DWD-CONTRACT-L01 |
| 任务名称 | 企业维度 — 项目自研 DWD 契约样板（主表 + 指标支撑字段） |
| 任务类型 | feature |
| 发起人 | 淮政玮（PM） / 徐滕强（架构师） |
| 审核者 | human:王惠（口径会签）/ human:徐滕强（表结构审核）|
| 认领人 | human:唐绍祖（2026-08-10 认领） |
| 原始任务说明 | task-registry.yaml → ENT-LINEAGE-DWD-CONTRACT-L01 条目 |
| 前置依赖 | 无硬前置；与 ENT-MOD-EVAL-METRIC-OPEN-L01 / ENT-MOD-SHENZHEN-METRIC-OPEN-L01 的指标定义形成互锁 |
| 服务系统 | 企业战略分析（ENT）域 — 企业搜索(E-20)/企业评估(E-23/E-24/E-30)/风险洞察(E-25)/引育推荐(E-35)/深圳企业现状分析(E-25) |

---

## 2. 产出清单

| # | 产出文件 | 路径 |
|---|---------|------|
| 1 | DWD 企业主表契约 | agent-delivery/data/data-design/企业/dwd_enterprise_master.md |
| 2 | 本 handoff 文档 | agent-handoffs/企业战略分析-ENT/ENT-LINEAGE-DWD-CONTRACT-L01.md |

### 2.1 DWD 契约内容摘要

**表名**：dwd_enterprise_master（项目自研 DWD，非供应库 dwd_* 一一对应）

**字段总数**：40 个字段，分 6 组：

| 组 | 字段数 | 内容 |
|----|--------|------|
| ① 主键与归一 | 4 | id, enterprise_code, enterprise_name, enterprise_name_short |
| ② 基础信息 | 7 | legal_representative, registered_capital, registration_date, business_status, enterprise_type, business_scope, registered_address |
| ③ 行业与地域 | 6 | industry_category, industry_subcategory, headquarters_city, headquarters_district, is_high_tech, is_little_giant |
| ④ 财务与研发 | 8 | revenue_latest, revenue_growth_rate, rd_investment, rd_staff_count, rd_ratio, gross_margin, profit_latest, tax_amount |
| ⑤ 专利与知识产权 | 5 | patent_grant_count, patent_invention_count, trademark_count, soft_copyright_count, std_count |
| ⑥ 算法评分字段 | 10 | tech_score, business_score, competitiveness_score, competitiveness_rank, risk_level, supply_chain_position, chain_role, innovation_score, growth_score, talent_score |

**每业务字段均含 ods_mapping_expectation**（expected_from + confidence + note），confidence 分布：high ×32, medium ×5, low ×3。

### 2.2 DoD 核对

| DoD 项 | 状态 | 说明 |
|--------|------|------|
| 至少 1 张企业主表契约落盘于 data/data-design/企业/ | ✅ | dwd_enterprise_master.md（19KB） |
| 每业务字段含 ods_mapping_expectation（expected_from + confidence） | ✅ | 全部 40 字段均有 |
| 覆盖 SEARCH/EVAL/RISK/RECRUIT 已用到的核心字段清单（对照表已附） | ✅ | 见契约 §「SEARCH/EVAL/RISK/RECRUIT 核心字段覆盖对照表」 |
| handoff 记录王惠会签：契约支撑哪些 metric_id | ⏳ 待王惠口径会签 | 见 §3 本节 |
| 禁止按供应库 dwd_* 一一抄表；Phase 1 不做 ODS→DWD 硬映射 | ✅ | 契约明确「非一一对应」；ods_dependency=none；Phase 2 映射清单留空 |

---

## 3. 契约支撑的 metric_id（王惠会签项）

> **DoD 第 4 项要求**：handoff 记录王惠会签「契约支撑哪些 metric_id」。
> 以下为契约表头 related_metrics 中登记的 13 个 metric_id，等待王惠口径会签确认。

本表 dwd_enterprise_master 的 related_metrics 列表：

| # | metric_id | 指标名称 | 支撑方式 | 所在任务 |
|---|-----------|---------|---------|---------|
| 1 | M_ENT_SZ_COUNT | 深圳企业数 | COUNT(*) WHERE headquarters_city='深圳' | ENT-MOD-SHENZHEN-METRIC-OPEN-L01 |
| 2 | M_ENT_SZ_CHAIN_POSITION | 链中角色 | chain_role 字段统计 | ENT-MOD-SHENZHEN-METRIC-OPEN-L01 |
| 3 | M_ENT_KEY_NODE_COUNT | 重点环节企业数 | chain_role IN (...) 统计 | ENT-MOD-SHENZHEN-METRIC-OPEN-L01 |
| 4 | M_ENT_CITY_AVG_TECH_POWER | 城市平均技术力 | AVG(tech_score) GROUP BY city | ENT-MOD-SHENZHEN-METRIC-OPEN-L01 |
| 5 | M_ENT_CITY_DENSITY | 企业密度 | COUNT(*) / 城市面积 | ENT-MOD-SHENZHEN-METRIC-OPEN-L01 |
| 6 | M_ENT_CHAIN_COMPLETENESS | 产业链完整度 | chain_role 覆盖率 | ENT-MOD-SHENZHEN-METRIC-OPEN-L01 |
| 7 | M_ENT_TECH_POWER_SCORE | 企业技术力评分 | tech_score 字段 | ENT-MOD-EVAL-METRIC-OPEN-L01 |
| 8 | M_ENT_BUSINESS_POWER_SCORE | 企业商业力评分 | business_score 字段 | ENT-MOD-EVAL-METRIC-OPEN-L01 |
| 9 | M_ENT_COMPETITIVENESS_SCORE | 企业竞争力评分 | competitiveness_score 字段 | ENT-MOD-EVAL-METRIC-OPEN-L01 |
| 10 | M_ENT_COMPETITIVENESS_RANK | 企业竞争力排名 | competitiveness_rank 字段 | ENT-MOD-EVAL-METRIC-OPEN-L01 |
| 11 | M_ENT_TOTAL_COUNT | 企业总数 | COUNT(*) | ENT-MOD-EVAL-METRIC-OPEN-L01 |
| 12 | M_ENT_INNOVATIVE_COUNT | 创新型企业数 | is_high_tech / patent 字段统计 | ENT-MOD-EVAL-METRIC-OPEN-L01 |
| 13 | M_ENT_PATENT_TOTAL | 专利总数 | SUM(patent_grant_count) | ENT-MOD-EVAL-METRIC-OPEN-L01 |

**bid_refs 覆盖**：§1.1.1.2.4.2.1（企业搜索）/ §1.1.1.2.4.2.2（企业评估）/ §1.1.1.2.4.2.3（风险洞察）/ §1.1.1.2.4.2.4（引育推荐）/ §1.1.1.2.4.2.3.5（深圳企业现状分析）。

**acceptance_units 覆盖**：E-20, E-23, E-24, E-25, E-30, E-35。

### 3.1 待王惠口径会签

> 方案 B 双签铁律：口径主责 human:王惠 + 算法共签 human:唐绍祖，缺一不可。

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 算法共签 | human:唐绍祖 | 2026-08-10 | ✅ 契约字段覆盖 SEARCH/EVAL/RISK/RECRUIT 核心场景；算法评分字段 ⑥ 组预留 tech_score/business_score/competitiveness_score 等产出位，与 EVAL METRIC-OPEN 的 C1/C2 五维六维对接；ods_mapping_expectation 全覆盖，Phase 2 可按 expected_from 做 GDF 映射。 |
| 口径主责 | human:王惠 | — | ⏳ 待王惠口径会签：确认本契约的 13 个 related_metrics 列表是否完整、字段口径是否与 cfg_metric 种子定义一致。 |

---

## 4. 禁止项合规

- ✅ **未按供应库 dwd_* 一一抄表**：本表为项目自研 DWD，由架构师按 SEARCH/EVAL/RISK/RECRUIT 需求设计字段集，不照抄供应库表结构
- ✅ **Phase 1 不做 ODS→DWD 硬映射**：ods_dependency: none；Phase 2 映射验收清单留空待 GDF 填写
- ✅ **双源归一方案明确**：dwd_org_reg_info（机构口径）+ dwd_company_base（工商口径），以 external_id = credit_code 归一，非简单 SELECT *
- ✅ **未覆盖字段如实标注**：market_share（市场份额）和 brand_score（品牌声量）在供应库无来源（K-O7），明确标注需采购市调数据，不在 Phase 1 契约范围
- ✅ **供应链关系另表**：enterprise_supply_chain 为独立 DWD 表，将另建 dwd_enterprise_supply_chain.md 契约，未混入主表
- ✅ **算法评分字段标注 🔧**：⑥ 组 10 个评分字段标注「待 algorithm-agent」，Phase 2 由算法侧确认公式后回填

---

## 5. 与关联任务的互锁关系

| 关联任务 | 关系 | 互锁点 |
|---------|------|--------|
| ENT-MOD-EVAL-METRIC-OPEN-L01 | 指标定义 ↔ DWD 契约 | ⑥ 组算法评分字段（tech_score/business_score/competitiveness_score）支撑 EVAL 模块的 M_ENT_TECH_POWER_SCORE 等 7 个指标 |
| ENT-MOD-SHENZHEN-METRIC-OPEN-L01 | 指标定义 ↔ DWD 契约 | ③ 组行业地域字段 + ⑥ 组评分字段支撑深圳模块的 M_ENT_SZ_COUNT 等 6 个指标 |
| Phase 2 GDF 映射（8/20 后） | 后续 | GDF 对照本契约 ods_mapping_expectation 做 ODS→DWD 字段级映射 |

> **数据流转简图**：
> `
> 供应库 dwd_org_reg_info + dwd_company_base（ODS）
>     │
>     │  Phase 2: GDF 按 ods_mapping_expectation 做字段级映射
>     │  双源归一: COALESCE(external_id, credit_code)
>     ▼
> dwd_enterprise_master（项目自研 DWD · 本契约）
>     │
>     ├──→ ⑥ 算法评分字段 → ads.enterprise_score → EVAL 指标（M_ENT_TECH_POWER_SCORE 等）
>     ├──→ ③ 行业地域字段 → 城市级聚合 → 深圳指标（M_ENT_SZ_COUNT 等）
>     ├──→ ② 基础信息字段 → SEARCH 筛选/排序
>     └──→ ④⑤ 财务专利字段 → RISK 风险等级 / RECRUIT 招引标签
> `

---

## 6. 后续动作

1. 王惠口径会签：确认 13 个 related_metrics 列表完整性 + 字段口径与 cfg_metric 种子一致性
2. 徐滕强表结构审核：审 40 字段类型/可空/索引设计
3. Phase 2（8/20 后）：GDF 按本契约 ods_mapping_expectation 做 ODS→DWD 字段级映射
4. 另建 dwd_enterprise_supply_chain.md 契约（供应链关系数据独立表）
5. 算法侧确认 ⑥ 组评分字段公式后回填（与 ENT-MOD-EVAL-METRIC-OPEN-L01 Q014 闭合联动）

---

## 7. 架构合规自检

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 契约落盘于 data/data-design/企业/ | ✅ |
| 2 | 使用 dwd-table-contract-template.md 模板 | ✅ |
| 3 | 表头元数据完整（table/layer/element/design_owner/design_phase/ods_dependency/related_metrics/bid_refs/acceptance_units/status/updated） | ✅ |
| 4 | 每业务字段含 ods_mapping_expectation | ✅（40/40） |
| 5 | SEARCH/EVAL/RISK/RECRUIT 核心字段覆盖对照表 | ✅ |
| 6 | 未按供应库 dwd_* 一一抄表 | ✅ |
| 7 | Phase 1 不做 ODS→DWD 硬映射 | ✅（ods_dependency=none） |
| 8 | Phase 2 映射验收清单留空 | ✅ |
| 9 | 变更记录已填 | ✅ |

---

## 8. Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 10_000 |
| actual_tokens | 8_000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.05 |
| cost_warn | green |

---

## 9. 语义双签（方案 B）

> 方案 B §1.4.2：口径主责 human:王惠；算法共签 human:唐绍祖

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 算法共签 | human:唐绍祖 | 2026-08-10 | ✅ 契约字段覆盖 SEARCH/EVAL/RISK/RECRUIT 核心场景；算法评分字段预留产出位与 EVAL/SHENZHEN METRIC-OPEN 对接；ods_mapping_expectation 全覆盖，Phase 2 可按 expected_from 做 GDF 映射。禁止项合规：未抄表、未硬映射。 |
| 口径主责 | human:王惠 | — | ⏳ 待王惠口径会签（方案 B 铁律，缺一不可） |

算法共签说明：本契约为 Phase 1 设计真源，40 字段覆盖企业搜索/评估/风险/引育/深圳现状分析全部核心场景。⑥ 组算法评分字段（tech_score/business_score/competitiveness_score 等 10 个）预留算法产出位，与 EVAL METRIC-OPEN 的 C1 技术力五维 + C2 商业力六维对接。双源归一方案（机构口径+工商口径）明确。禁止项全部合规：未按供应库一一抄表、Phase 1 未做硬映射、未覆盖字段如实标注。
