# 企业维 · 未登记指标缺口清单

> **日期**：2026-08-03  
> **真源**：`metrics/metric-readiness-matrix-ENT.yaml`（v2 / L02）  
> **口径**：未入 `cfg_metric-ENT-seed.yaml` = 未登记；含 D1=`missing` 与「有拟用 ID 但未入种子」两类  
> **用途**：催促王惠正式化 + 唐绍祖 METRIC-OPEN 返工 / E-32 开工对照

---

## 0. 汇总

| 类别 | 条数 | 说明 |
|------|------|------|
| **A. D1=missing（严格未注册）** | **16** | UI 应红问号；d2~d4=n/a |
| **B. 拟用 ID 已写、未入 seed** | **13** | KEYPANO×8 + STAR×5（矩阵 draft，note 写明未入 seed） |
| **合计待入种子 / 待定 ID** | **29** | 不含已入 seed 仅口径 draft 的项 |

> 矩阵 footer：`missing 16` = RECRUIT GAP×4 + SHENZHEN GAP×1 + L02 未注册×11。  
> KEYPANO/STAR 另计为「未入 seed」但不标 missing（已有拟用 `M_ENT_*`）。

---

## 1. A 类 · D1=missing（16 条）

### 1.1 RECRUIT（E-26/E-27）· 4

| metric_id | 中文名 | 挂靠 | 催谁 |
|-----------|--------|------|------|
| `GAP-RECRUIT-METRIC-01` | 深圳连接度 | Q015 | 王惠定是否立正式 ID；唐绍祖算法合成方案 |
| `GAP-RECRUIT-METRIC-03` | 企业行业领域排名 | — | 下游定义是否独立 metric_id |
| `GAP-RECRUIT-METRIC-04` | 可视化行业分布 | — | 同上 |
| `GAP-RECRUIT-METRIC-05` | 关键指标集合 | — | UX 定义展示；不建笼统总分 |

### 1.2 SHENZHEN（E-25/E-35）· 1+2

| metric_id | 中文名 | 挂靠 | 催谁 |
|-----------|--------|------|------|
| `GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER` | 城市平均商业力 | Q014 | 何老师/王惠注册正式 ID；禁止用竞争力/营收替代 |
| `M_ENT_CITY_RANK` | 多城市对标排名 | Q016 | 王惠正式化（L02） |
| `M_ENT_STATE_OWNED_COUNT` | 国有企业数 | Q049 | 王惠；正式建议 `M_ENT_SZ_SOE_COUNT` |

### 1.3 OVERVIEW / E-31~E-33 相关（L02 · UI 已引用）· 6

| metric_id | 中文名 | 挂靠 | 催谁 |
|-----------|--------|------|------|
| `M_ENT_RESEARCHER_COUNT` | 企业科研人数 | TRACE-E31 | **E-32 METRIC-OPEN** + 王惠入种子 |
| `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT` | 覆盖未来产业数 | TRACE-E31 | 同上（截图 ⓘ 红叉即此条） |
| `M_ENT_KEY_TOTAL` | 重点企业总数 | Q038 | 王惠；禁复用 `M_ENT_TOTAL_COUNT` |
| `M_ENT_REGION_COVERAGE` | 区域覆盖数 | E-20 tab | 王惠定层级/分母 |
| `M_ENT_REGION_HOT_COUNT` | 热点区域数 | E-20 tab | 王惠定「热点」语义 |
| `M_ENT_CHAIN_STAGE_COVERAGE` | 产业链环节覆盖 | E-20 | 王惠：是否与 `M_ENT_CHAIN_COMPLETENESS` 合并 |

### 1.4 EVAL / STAR 补录（L02）· 3

| metric_id | 中文名 | 挂靠 | 催谁 |
|-----------|--------|------|------|
| `M_ENT_PATENT_VALID_COUNT` | 有效专利数 | — | 王惠；禁与 `PATENT_TOTAL`/`GRANT_COUNT` 别名合并 |
| `M_ENT_STAR_PATENT_COUNT` | 明星企业专利数 | Q048 | 王惠 + STAR METRIC-OPEN 返工 |
| `M_ENT_STAR_RD_RATIO` | 明星企业研发投入占比 | Q048 | 王惠；或对齐 `M_ENT_RD_INVESTMENT_RATIO`（待确认） |

---

## 2. B 类 · 拟用 ID 未入 `cfg_metric-ENT-seed`（13 条）

### 2.1 KEYPANO（E-33）· 8 · 归 Q047

| metric_id | 中文名 | pending |
|-----------|--------|---------|
| `M_ENT_KEYPANO_MATCH_COUNT` | 匹配企业数 | Q038 |
| `M_ENT_KEYPANO_TYPE_COUNT` | 覆盖企业类型数 | Q010 |
| `M_ENT_KEYPANO_QUAL_DISTRIBUTION` | 整链资质分布 | Q010 / Q047 |
| `M_ENT_KEYPANO_TYPE_STRUCTURE` | 企业类型分布 | Q010 |
| `M_ENT_KEYPANO_REGIONAL_COUNT` | 覆盖区域数 | Q012 |
| `M_ENT_KEYPANO_REGIONAL_DISTRIBUTION` | 区域分布 | Q012 |
| `M_ENT_KEYPANO_ENTERPRISE_LIST` | 企业清单 | Q038 |
| `M_ENT_KEYPANO_DOMAIN_SUMMARY` | 领域摘要 | Q013 / Q047 |

→ 催：**唐绍祖** KEYPANO METRIC-OPEN 返工落种子；**王惠** Q047 正式化。

### 2.2 STAR（E-34）· 5

| metric_id | 中文名 | pending |
|-----------|--------|---------|
| `M_ENT_STAR_ENTERPRISE_COUNT` | 明星企业数量 | Q037（注：与决策清单空态语义冲突，应拆清） |
| `M_ENT_STAR_BY_INDUSTRY` | 明星企业行业分布 | Q037→宜 Q041/Q048 |
| `M_ENT_STAR_BY_REGION` | 明星企业区域分布 | 同上 |
| `M_ENT_STAR_BASIC_INFO` | 明星企业基础画像 | —（口径清，只欠入种子） |
| `M_ENT_STAR_HONOR_LIST` | 明星企业荣誉清单 | —（同上） |

→ 催：**唐绍祖** STAR 返工入种子；**王惠** 正式化。

---

## 3. 相关但不算「未登记 ID」的缺口（备忘）

| 项 | 说明 |
|----|------|
| `GAP-RECRUIT-METRIC-02` | 培育「企业潜力」归属语义；挂在已有 `M_ENT_GROWTH_POTENTIAL` 上，非独立未注册 ID |
| `GAP-KEYPANO-REGIONAL-SCALE/RATIO` | KEYPANO 核对记录开放项；尚无正式 metric_id，矩阵挂在 REGIONAL_DISTRIBUTION 的 d3_gap |
| `GAP-SZSTATUS-DENSITY-DENOMINATOR` 等 | 公式/分母缺口；主 ID 已入 seed（如 `M_ENT_CITY_DENSITY`） |
| OPS 15 capability | CMS 能力非统计指标，不入本清单 |
| COMPARE | 派生容器无统计指标 |

---

## 4. 按催促对象折叠

| 对象 | 动作 | 条数焦点 |
|------|------|----------|
| **王惠** | 正式化入 `cfg_metric-ENT-seed` | A 类 16 + 审定 B 类 13 |
| **唐绍祖** | METRIC-OPEN 返工 / E-32 开工时写入种子或 GAP | KEYPANO 8、STAR 5+2、E-32 的 RESEARCHER/FUTURE_INDUSTRY、SHENZHEN 商业力 GAP |
| **何老师（名义）** | 城市平均商业力正式 ID | `GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER` |

---

## 5. 真源路径

- 矩阵：`agent-delivery/metrics/metric-readiness-matrix-ENT.yaml`
- 种子：`agent-delivery/metrics/cfg_metric-ENT-seed.yaml`
- 签收检查：`ENT-METRIC-OPEN-ready_to_sign-签收检查-2026-08-03.md`
