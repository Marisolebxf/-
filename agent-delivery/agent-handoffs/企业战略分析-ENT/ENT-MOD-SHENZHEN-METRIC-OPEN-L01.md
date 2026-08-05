# ENT-MOD-SHENZHEN-METRIC-OPEN-L01 — 任务完成说明
# 深圳企业介绍 — 指标语义与 ODS/DWD 缺口核对（METRIC-OPEN）

> **任务**：ENT-MOD-SHENZHEN-METRIC-OPEN-L01
> **角色**：algorithm-agent + data-agent 双 Agent
> **监管人**：human:唐绍祖（§1.4.1 临时语义 Owner）
> **日期**：2026-07-29
> **产出**：以下 3 件套

---

## 1. 任务概述

根据 PM 淮政玮 2026-07-28 PACK 通过后派单，完成 Track-MS 五件套 **#4 指标语义 + #5 开放项** 闭合：

- **深圳企业现状分析（E-25）** — 产业链定位 + 多城市横向对标的指标体系与数据缺口
- **深圳企业介绍（E-35）** — 门户深圳企业展示的统计指标口径（本任务侧重 E-25 算法指标；E-35 为 CMS 驱动，指标待 Q049 闭合）

上游依赖 **ENT-MOD-SHENZHEN-PACK-L01** ✅ done。本模块是四个 Track-MS 模块中唯一需要真实算法计算指标的模块（区别于 KEYPANO/STAR 的 CMS 驱动模式）。

## 2. 产出清单

| # | 产出文件 | 路径 |
|---|---------|------|
| 1 | METRIC-OPEN 核对记录 | `agent-handoffs/产品整体定义/E-25-深圳企业现状分析/METRIC-OPEN-ENT-SHENZHEN-核对记录.md` |
| 2 | 数据缺口目录 | `agent-handoffs/产品整体定义/E-25-深圳企业现状分析/ENT-SHENZHEN-data-gap-catalog.yaml` |
| 3 | 本 handoff 文档 | `agent-handoffs/企业战略分析-ENT/ENT-MOD-SHENZHEN-METRIC-OPEN-L01.md` |

## 3. 指标核对结论

### 3.1 核对范围

本次核对的 7 个指标覆盖两个产品视图：

| 视图 | 指标数 | 说明 |
|------|--------|------|
| 产业链定位（view=chain-position） | 4 个 | 深圳企业数量、链角色、环节分布、产业链完整度 |
| 多城市横向对标（view=city-benchmark） | 4 个 | 平均技术力、平均商业力、企业密度、产业链完整度（与前视图共用） |

其中 M_ENT_CHAIN_COMPLETENESS 在两个视图中均被引用。

### 3.2 algorithm-agent 侧

| 指标 | metric_id | mapping_status | 阻塞项 |
|------|-----------|---------------|--------|
| 深圳企业数 | M_ENT_SZ_COUNT | ✅ 已登记 | 无（统计型指标，已具备闭合条件） |
| 链中角色 | M_ENT_SZ_CHAIN_POSITION | ✅ 已登记 | 无（直接映射字段，已具备闭合条件） |
| 重点环节企业数 | M_ENT_KEY_NODE_COUNT | ✅ 已登记 | 无（统计型指标，已具备闭合条件） |
| 城市平均技术力 | M_ENT_CITY_AVG_TECH_POWER | 🔧 | Q014 未闭合（技术力公式待确认） |
| 城市平均商业力 | GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER | ❌ metric_id 未登记 | Q014 + 需先由何老师注册 metric_id |
| 企业密度 | M_ENT_CITY_DENSITY | 🔧 | Q016（对标城市）+ GAP-SZSTATUS-DENSITY-DENOMINATOR（分母未确认） |
| 产业链完整度 | M_ENT_CHAIN_COMPLETENESS | 🔧 | GAP-SZSTATUS-CHAIN-COMPLETENESS-FORMULA（公式待算法定义） |

**核心判断**：3 个统计型指标（M_ENT_SZ_COUNT、M_ENT_SZ_CHAIN_POSITION、M_ENT_KEY_NODE_COUNT）已具备闭合条件——它们离源数据近，公式单纯（COUNT / 直接取字段），不依赖未闭合的 Q 项或链数据基础设施。其余 4 个指标存在真实依赖（Q014 技术力公式、链数据环节全集、城市维表、全国聚合逻辑），不能伪闭合。与 ENT-MOD-EVAL-METRIC-OPEN-L01 的不同之处在于：深圳模块多了"产业维度" + "空间维度"的二级聚合需求，本模块待闭合项 = EVAL 模块待闭合项（Q014）+ 本模块独有待闭合项（链数据、城市维表、全国聚合）。

### 3.3 data-agent 侧

**数据可用性摘要**：
- ✅ 可用且闭合：M_ENT_SZ_COUNT、M_ENT_SZ_CHAIN_POSITION、M_ENT_KEY_NODE_COUNT（均源自 dwd.enterprise_base + dwd.enterprise_industry 体系，当前为 Mock 数据 batch=mock_20260618）
- 🔧 formula 待算法：M_ENT_CITY_AVG_TECH_POWER、M_ENT_CITY_DENSITY、M_ENT_CHAIN_COMPLETENESS（有 DWD/ADS 源表但公式未闭合）
- ❌ 无源：GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER（不是数据无源，是 metric_id 未注册，语义上等于"正式指标不存在"）

**关键数据基础设施缺口**：

| 缺口项 | 影响指标 | 严重程度 |
|--------|---------|---------|
| 产业链环节全集与覆盖判定规则 | M_ENT_CHAIN_COMPLETENESS | 🔴 阻塞算法实现 |
| 城市基础维表（面积/人口/GDP 等标准化基数） | M_ENT_CITY_DENSITY | 🔴 阻塞分母计算 |
| 全国参照聚合逻辑 | M_ENT_CITY_AVG_TECH_POWER, M_ENT_CITY_DENSITY, M_ENT_CHAIN_COMPLETENESS | 🟡 阻塞对标基准 |
| 商业力 metric_id 注册 | GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER | 🔴 阻塞任何后续工作 |

### 3.4 开放项跟踪

| 编号 | 主题 | 状态 | Owner |
|------|------|------|-------|
| Q014 | 技术力与商业力指标库构成及默认权重 | 🟡 待甲方确认 | human:何老师 |
| Q016 | 多城市对标默认城市集合 | 🟡 待甲方确认 | human:何老师 |
| GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER | 城市平均商业力 metric_id 登记 | 🆕 待注册 | human:何老师 → data-agent |
| GAP-SZSTATUS-DENSITY-DENOMINATOR | 企业密度分母确认 + 城市维表提供 | 🆕 待数据侧 | human:辜少彬 |
| GAP-SZSTATUS-CHAIN-COMPLETENESS-FORMULA | 产业链完整度环节全集/覆盖判定/权重方案 | 🆕 待算法 | human:唐绍祖 |
| GAP-SZSTATUS-NATIONAL-AGGREGATION | 全国参照聚合逻辑实现 | 🆕 待数据侧 | human:辜少彬 |

## 4. 与 ENT-MOD-EVAL-METRIC-OPEN-L01 的差异与继承

本模块不是独立的模块算法体系，而是继承企业评估模块（EVAL）的单企业评分能力再做城市级聚合。因此：

| 依赖来源 | 继承内容 | 新增内容 |
|---------|---------|---------|
| ENT-MOD-EVAL-METRIC-OPEN-L01 §2 | 技术力 C1 五维（talent/innovation/transfer/cooperation/investment）、商业力 C2 六维（market/product/brand/cooperation/chain_coverage/chain_keynode） | 城市 GROUP BY + AVG 聚合 |
| ENT-MOD-EVAL-METRIC-OPEN-L01 §3 | ODS/DWD/ADS 血缘：ads.enterprise_score 作为企业级评分源 | dwd_industry_chain_info 作为链环节全集源；城市基础维表作为密度分母源 |
| ENT-MOD-EVAL-METRIC-OPEN-L01 §4 | Q014（权重确认）为本模块必备前置 | Q016（城市集合）、链环节属性定义、全国聚合 |
| IA-ENT-SZSTATUS §7 | 指标命名与产品契约 | 产业链维度、商业力独立 metric_id、密度分母拒绝面积/GDP 默认 |

> **继承关系简图**：
> ```
> ENT-MOD-EVAL-METRIC-OPEN-L01（13 metrics, Q014/Q019）
>   │  产出: ads.enterprise_score（企业级技术力/商业力/竞争力评分）
>   │
>   ▼
> ENT-MOD-SHENZHEN-METRIC-OPEN-L01（7 metrics, Q014/Q016 + 4 GAP）
>   │  输入: ads.enterprise_score（企业级评分）
>   │  产出: 城市级 AVG（tech/biz power）+ 城市计数（density/completeness/count）
> ```
>
> **Q014 闭合后，ETS 模块可用的计算路径**：
> 1. 技术力 C1 企业级评分（已有算法）→ 按 city GROUP BY AVG → 城市平均技术力
> 2. 商业力 C2 企业级评分（已有算法）→ 按 city GROUP BY AVG → 城市平均商业力
> 3. 企业密度 → 分子（城市企业 COUNT）+ 分母（待提供）
> 4. 完整度 → 链环节全集（待提供）+ 深圳覆盖环节（已有 dwd）

## 5. 禁止项合规

- ✅ **未替甲方闭合 Q014/Q016**：权重/阈值/城市集合停留 pending 状态
- ✅ **GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER 未擅自造 metric_id**：如实登记为未注册缺口
- ✅ **密度分母未自行选定**：明确拒绝默认面积或 GDP，等待甲方/数据侧确认标准化基数
- ✅ **完整度公式未虚构**：三个未闭合点（环节全集/覆盖判定/权重）均在核对记录中完整记录
- ✅ **数据库报告/bat**：未改动（本任务为 agent-delivery 文档产出，不涉及数据库操作）
- ✅ **未混淆统计型指标与算法型指标**：3 个 COUNT/直接映射型已闭合，4 个算法依赖型如实标记 🔧/❌

## 6. 后续动作

1. 唐绍祖签署本 handoff，标志 METRIC-OPEN 交付完成
2. 推动甲方/何老师闭合 Q014（技术力/商业力权重终值）— 此为本模块最大阻塞项，闭合后 4 个 🔧 指标中可解除 2 个（tech/biz power avg）
3. 推动何老师确认 GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER metric_id 注册方案
4. 推动数据侧辜少彬提供城市基础维表并确认密度分母方案
5. 唐绍祖确认产业链完整度公式（GAP-SZSTATUS-CHAIN-COMPLETENESS-FORMULA）
6. 推动数据侧实现全国参照聚合逻辑（GAP-SZSTATUS-NATIONAL-AGGREGATION）
7. Q016 闭合前，多城市对标使用临时默认集合进行前端交互开发

## 7. 架构合规自检

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 仅改动 agent-delivery 文档，未动 demo 页面 | ✅ |
| 2 | metric 口径引用 PDR/Decision/IA，非新拍板 | ✅ |
| 3 | pending_hint ≥80 字（7 条全部达标） | ✅ |
| 4 | 唐绍祖 §1.4.1 会签 | ✅（2026-08-05 补签，见 §9） |
| 5 | cost 四字段已填写 | ✅ |

## 8. Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 150_000 |
| actual_tokens | 98_000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.61 |
| cost_warn | green |

## 9. 语义双签（方案 B · 2026-08-05 补签）

> 方案 B §1.4.2：口径主责 human:王惠；算法共签 human:唐绍祖

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 算法共签 | human:唐绍祖 | 2026-08-05 | ✅ 算法侧交付完成：7 指标 mapping_status 评估、3 统计型闭合、4 算法依赖型如实标记、GAP-CHAIN-COMPLETENESS-FORMULA 待算法确认 |
| 口径主责 | human:王惠 | — | ⏳ 待王惠口径会签（方案 B 铁律，缺一不可） |

算法共签说明：深圳企业现状分析 7 个指标的 mapping_status、数据缺口登记、开放项纪律（Q014/Q016 不伪闭合）均与 bid-reference 及 EVAL METRIC-OPEN 产出一致。3 个统计型指标（SZ_COUNT/SZ_CHAIN_POSITION/KEY_NODE_COUNT）离源数据近、公式单纯，已具备闭合条件。4 个算法依赖型指标如实标记待闭合项，未替甲方闭合 Q014/Q016。
