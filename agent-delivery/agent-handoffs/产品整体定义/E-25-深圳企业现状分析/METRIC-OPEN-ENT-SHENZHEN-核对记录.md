# METRIC-OPEN-ENT-SHENZHEN-核对记录
# ENT-MOD-SHENZHEN-METRIC-OPEN-L01 — 深圳企业介绍指标语义与 ODS/DWD 缺口核对

> **任务**：ENT-MOD-SHENZHEN-METRIC-OPEN-L01
> **角色**：algorithm-agent + data-agent 双 Agent
> **监管人**：human:唐绍祖（§1.4.1 临时语义 Owner）
> **日期**：2026-07-29
> **上游**：ENT-MOD-SHENZHEN-PACK-L01 ✅ done
> **模块**：深圳企业现状分析（E-25 / E-35）
> **区别于 KEYPANO/STAR**：本模块存在真实算法指标（非 CMS 驱动），需要逐条核对算法公式与数据血缘

---

## §1 适用性结论（Track-MS #4/#5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡（MetricSpecCard） | ⚠️ 部分闭合 | 7 个 metric 中 3 个已映射、3 个映射但公式待算法确认、1 个正式 metric_id 未登记 |
| #5 开放项（PendingBadge + Popover） | ⚠️ 部分闭合 | Q014/Q016/GAP-SZSTATUS-* 已登记；catalog 7 条 pending_hint 均 ≥80 字 |
| PDR-05 自检 | ✅ 通过 | IA ↔ USM ↔ TRACE 一致 |
| PDR-06 自检 | ⚠️ 通过 | metric ↔ definition ↔ source_tables 交叉检查完成；3 个指标缺少完整算法公式 |
| 唐绍祖会签 §1.4.1 | ⏳ 待签署 | — |

> **关键判断**：本模块的 7 个指标中，有 3 个（M_ENT_SZ_COUNT、M_ENT_SZ_CHAIN_POSITION、M_ENT_KEY_NODE_COUNT）属于"统计型指标"（离源数据近，算法逻辑简单），已具备闭合条件。其余 4 个指标必须在 Q014（技术力/商业力公式）、Q016（对标城市集合）和链数据基础设施就绪后才能从 🔧 升级为 ✅。当前阶段如实记录 4 个开放项，不伪闭合。

---

## §2 深圳企业现状分析指标口径摘要（algorithm-agent）

### 2.1 产业链定位视图指标（view=chain-position）

| metric_id | 中文名 | 定义 | 公式 | 源表 | 状态 |
|-----------|--------|------|------|------|------|
| M_ENT_SZ_COUNT | 深圳企业数 | 总部在深圳且属目标产业链的企业去重数 | COUNT(DISTINCT enterprise_id) WHERE headquarters_city='深圳' AND 产业链 IN(:chain) | dwd.enterprise_base + dwd.enterprise_industry_tags | ✅ 已登记，统计型 |
| M_ENT_SZ_CHAIN_POSITION | 链中角色 | 企业在产业链中的角色（上/中/下游、链主等），取 ODS 产业链归属字段 | dwd.enterprise_industry.industry_chain_role | dwd.enterprise_industry ← ods | ✅ 已登记，直接映射 |
| M_ENT_KEY_NODE_COUNT | 重点环节企业数 | 按产业链重点环节分组的企业去重数 | COUNT(DISTINCT enterprise_id) GROUP BY industry_chain_node | dwd.enterprise_industry | ✅ 已登记，统计型 |
| M_ENT_CHAIN_COMPLETENESS | 产业链完整度 | 城市/区域覆盖的产业链环节占全链环节比例 | 覆盖环节数 / 全链环节数 × 100（公式待算法确认：环节全集定义、覆盖判定规则、权重方案均未闭合） | dwd.enterprise_industry + dwd_industry_chain_info | 🔧 formula 待算法确认 |

### 2.2 多城市横向对标视图指标（view=city-benchmark）

| metric_id | 中文名 | 定义 | 公式 | 源表 | 状态 |
|-----------|--------|------|------|------|------|
| M_ENT_CITY_AVG_TECH_POWER | 城市平均技术力 | 城市内企业技术力评分均值；技术力权重口径同 Q014，城市集合参考 Q016 | AVG(tech_score) GROUP BY city（派生自 M_ENT_TECH_POWER_SCORE） | ads.enterprise_score + dwd.enterprise_base.headquarters_city | 🔧 Q014 未闭合 |
| GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER | 城市平均商业力 | Bid 明确要求但 cfg_metric-ENT-seed 未注册独立 metric_id；不得以综合竞争力或单一营收指标替代 | 待 Q014 闭合后按商业力六维均值计算 | 待映射 | ❌ metric_id 未登记 |
| M_ENT_CITY_DENSITY | 企业密度 | 对标城市企业密度；对标城市集合（临时默认北京/上海/苏州/广州）待 Q016 确认 | 城市企业数 / 分母（分母不能默认面积或 GDP，待数据侧确认标准化基数） | dwd.enterprise_base.headquarters_city + 城市基础维表（待补） | 🔧 分母未确认 |

### 2.3 数据依赖与算法边界

| 依赖项 | 影响指标 | 说明 |
|--------|---------|------|
| Q014（技术力/商业力指标库构成及默认权重） | M_ENT_CITY_AVG_TECH_POWER, GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER | 城市平均技术力/商业力均派生自单企业评分 → 城市 GROUP BY 聚合；Q014 未闭合则城市评分公式无锚点，不可包装为正式算法结论 |
| Q016（多城市对标默认城市集合） | M_ENT_CITY_DENSITY, M_ENT_CITY_AVG_TECH_POWER, M_ENT_CHAIN_COMPLETENESS | 对标城市集合影响所有需跨城市比较的指标计算范围；临时集合北京/上海/苏州/广州仅作为产品临时值 |
| 产业链环节全集与覆盖判定规则 | M_ENT_CHAIN_COMPLETENESS | 完整度需要：产业链环节全集 → 深圳企业覆盖的环节 → 覆盖判定阈值（有 1 家即覆盖 vs 需要 N 家以上），当前均未定义 |
| 城市基础维表 | M_ENT_CITY_DENSITY | 密度计算需要城市面积或标准化基数（如单位 GDP、建成区面积等），当前无对应维表 |
| 全国参照聚合 | 所有城市指标 | 全国参照需对 dwd.enterprise_base 做全量聚合（非按城市筛选），该聚合逻辑尚未实现 |

---

## §3 指标 × 贴源矩阵（data-agent）

| metric_id | mapping_status | ODS源表 | DWD表 | ADS表 | pending_ref | pending_hint |
|-----------|---------------|---------|-------|-------|-------------|-------------|
| M_ENT_SZ_COUNT | ✅ | dwd_org_reg_info, dwd_org_industry_chain_dtl | dwd.enterprise_base, dwd.enterprise_industry_tags | — | — | 数据可用。按 headquarters_city='深圳' + 产业链筛选 COUNT(DISTINCT enterprise_id)。当前为 Mock 数据（batch=mock_20260618），待真实数据灌入后验证过滤条件准确性。 |
| M_ENT_SZ_CHAIN_POSITION | ✅ | dwd_org_industry_chain_dtl, dwd_industry_chain_info | dwd.enterprise_industry | — | — | 直接取 dwd.enterprise_industry.industry_chain_role 字段。缺失角色时业务态显示"暂未标注"，不得依据企业名称推断。当前为 Mock 数据（batch=mock_20260618），正式数据需确认字段映射完整性。 |
| M_ENT_KEY_NODE_COUNT | ✅ | dwd_org_industry_chain_dtl, dwd_industry_chain_info | dwd.enterprise_industry | — | — | 数据可用。按 dwd.enterprise_industry.industry_chain_node 分组 COUNT(DISTINCT enterprise_id)。当前为 Mock 数据（batch=mock_20260618），正式数据需确认重点环节的"重点"判定口径（由算法/业务定义还是直接取数据字段）。 |
| M_ENT_CITY_AVG_TECH_POWER | 🔧 | dwd_org_tag_info, dwd_org_annual_financial_info | dwd.enterprise_base (headquarters_city) | ads.enterprise_score (score_innov, score_total) | Q014, Q016 | 城市平均技术力需先有企业级技术力评分（M_ENT_TECH_POWER_SCORE），再按 headquarters_city GROUP BY 取 AVG。技术力评分依赖 Q014 闭合（5 维权重及部分维度代理方案确认），城市集合依赖 Q016（对标城市列表确认）。当前 ads.enterprise_score.score_total 可作为临时近似但不等同于正式技术力评分。 |
| GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER | ❌ | — | — | — | Q014 | Bid 要求城市平均商业力对标，但 cfg_metric-ENT-seed 未注册独立 metric_id（GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER）。登记前业务模式显示正常不可用态，不得用综合竞争力 M_ENT_COMPETITIVENESS_SCORE 或单一营收指标替代。商业力六维公式同样依赖 Q014 闭合。待何老师确认后由 data-agent 新增 metric_id 并完成映射。 |
| M_ENT_CITY_DENSITY | 🔧 | dwd_org_reg_info | dwd.enterprise_base (headquarters_city, enterprise_id) | — | Q016, GAP-SZSTATUS-DENSITY-DENOMINATOR | 企业密度 = 城市内企业数 / 标准化分母。分子可用 COUNT(DISTINCT enterprise_id) GROUP BY headquarters_city。分母未确认：不能默认取城市面积（各城市面积不可比）或 GDP（经济总量不等于企业密度基准）。需数据侧提供城市基础维表（如建成区面积、单位 GDP 企业密度、常住人口等），由甲方确认分母方案。 |
| M_ENT_CHAIN_COMPLETENESS | 🔧 | dwd_org_industry_chain_dtl, dwd_industry_chain_info | dwd.enterprise_industry | — | GAP-SZSTATUS-CHAIN-COMPLETENESS-FORMULA | 产业链完整度 = 覆盖环节数 / 全链环节数。三个未闭合点：(1) 环节全集以 dwd_industry_chain_info 为准还是以甲方产业链定义为准；(2) 覆盖判定：有 1 家深圳企业即覆盖 vs 需要 N 家以上；(3) 是否需要按环节重要性加权（链主环节权重 > 普通环节）。公式待算法确认（owner: 唐绍祖），Demo 可展示固定样例形态但不作为正式生态完整性结论。 |

---

## §4 开放项闭合表

| 编号 | 关联 metric | 当前状态 | 依据 | 待闭合动作 |
|------|-----------|---------|------|-----------|
| Q014 | M_ENT_CITY_AVG_TECH_POWER, GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER | 🟡 团队临时默认 | PDR 纪要 / settings.yaml 权重已实现 | 甲方确认技术力五维、商业力六维的最终权重及部分维度代理方案 |
| Q016 | M_ENT_CITY_DENSITY, M_ENT_CITY_AVG_TECH_POWER, M_ENT_CHAIN_COMPLETENESS | 🟡 团队临时默认 | PDR 纪要 / Q016 topic | 甲方确认多城市对标默认集合（当前临时：北京/上海/苏州/广州） |
| GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER | GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER | ❌ metric_id 未登记 | Bid 需求 / IA-ENT-SZSTATUS §7 | 何老师确认后 data-agent 在 cfg_metric-ENT-seed 注册独立 metric_id 并映射到商业力六维评分均值 |
| GAP-SZSTATUS-DENSITY-DENOMINATOR | M_ENT_CITY_DENSITY | ❌ 分母未确认 | IA-ENT-SZSTATUS §7 | 甲方/数据侧确认企业密度分母（建成区面积/单位 GDP/常住人口 等），并提供城市基础维表 |
| GAP-SZSTATUS-CHAIN-COMPLETENESS-FORMULA | M_ENT_CHAIN_COMPLETENESS | ❌ 公式待算法 | IA-ENT-SZSTATUS §7 / TRACE 开放项 | 唐绍祖确认环节全集来源、覆盖判定规则及环节加权方案 |
| GAP-SZSTATUS-NATIONAL-AGGREGATION | M_ENT_CITY_AVG_TECH_POWER, M_ENT_CITY_DENSITY, M_ENT_CHAIN_COMPLETENESS | 🆕 全国参照聚合未实现 | IA-ENT-SZSTATUS §7 "全国参照使用相同指标的全国聚合结果" | 数据侧实现全国维度 GROUP BY 聚合逻辑（非按城市筛选，而是全量汇总），作为多城市标对中的固定参照基线 |

---

## §5 PDR-05/06 自检清单

| 检查项 | 结果 | 备注 |
|--------|------|------|
| PDR-05: IA ↔ USM ↔ TRACE 一致性 | ✅ | E-25/E-35 两个模块全部覆盖；IA §7 指标与 TRACE metric_semantics 字段一致 |
| PDR-05: wireframe 覆盖度 | ✅ | 两个视图均覆盖全部指标；评审挂点与 Wireframe review_trace_contract 一致 |
| PDR-06: metric ↔ definition 一致性 | ✅ | 7 个 metric 中 6 个已在 cfg_metric-ENT-seed 注册，1 个（GAP）待登记 |
| PDR-06: source_tables 完整度 | ⚠️ | 4 个 metric 完全有源（3✅ + 1🔧）; 1 个 metric 映射待映射（GAP）; 2 个 metric（DENSITY/COMPLETENESS）部分有源但关键字段缺失 |
| PDR-06: ODS→DWD→ADS 血缘完整 | ⚠️ | M_ENT_SZ_COUNT/SZ_CHAIN_POSITION/KEY_NODE_COUNT 血缘完整；其余 4 个有数据缺口 |
| PDR-06: pending_hint ≥80 字 | ✅ | 7 条全部达标（catalog 验证通过） |
| PDR-06: 全国参照聚合 | ⚠️ | 全国参照聚合逻辑未实现，标为 GAP-SZSTATUS-NATIONAL-AGGREGATION |

---

## §6 语义会签

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 语义 Owner（临时代行） | human:唐绍祖 | 2026-07-29 | ⏳ 待签署 |

---

## §7 与其他模块的关键差异

本模块与企业评估（ENT-MOD-EVAL-METRIC-OPEN-L01）有本质不同：

| 对比维度 | 企业评估（E-23/E-24/E-30） | 深圳企业现状分析（E-25/E-35） |
|---------|--------------------------|---------------------------|
| 指标体系性质 | 单企业维度评分（技术力/商业力/竞争力） | 城市级别聚合指标（均值/密度/完整度） |
| 数据血缘路径 | ODS → DWD → ads.enterprise_score（单企业行） | ODS → DWD → ads.enterprise_score → 城市 GROUP BY 再聚合 |
| 算法复杂度 | 五维/六维加权评分 + min-max 归一化 | 部分为统计型（COUNT/AVG），部分依赖链数据基础设施 |
| 核心阻塞项 | Q014（权重确认）、Q019（市场份额无源） | Q014/Q016（权重+城市集）、链数据基础设施（环节全集/角色字段）、全国聚合 |
| 当前可展示程度 | 9/13 个指标可用 Mock 数据展示交互 | 3/7 个指标可展示、4/7 个指标数据/公式未就绪 |

核心特征：深圳企业现状分析继承了企业评估的 Q014 依赖（城市均值派生于单企业评分），但额外增加了"产业维度"（链角色、链完整度、链环节分布）和"空间维度"（城市密度、全国参照）的聚合需求，这要求链数据基础设施和城市维表先到位，算法才能基于准确的数据底座实现城市级指标。
