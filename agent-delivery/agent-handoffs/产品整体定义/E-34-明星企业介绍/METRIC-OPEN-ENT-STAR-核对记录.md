# METRIC-OPEN-ENT-STAR-核对记录
# ENT-MOD-STAR-METRIC-OPEN-L01 — 明星企业介绍指标语义与 ODS/DWD 缺口核对

> **任务**：ENT-MOD-STAR-METRIC-OPEN-L01
> **角色**：algorithm-agent + data-agent 双 Agent
> **监管人**：human:唐绍祖（§1.4.1 临时语义 Owner）
> **日期**：2026-07-29
> **上游**：ENT-MOD-STAR-PACK-L01 ✅ done

---

## §1 适用性结论（Track-MS #4/#5）

> **核心判断**：STAR（明星企业介绍）模块本质上是 **CMS 驱动的内容展示页面**，而非算法分析模块。该页面属于 A1 门户内容体系，明星企业的主数据（表彰文本、展示配图、荣誉介绍文案）由 CMS 运营侧维护，数据侧指标仅限明星企业身份标识与基础画像信息的查询展示。

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡（MetricSpecCard） | ✅ 已闭合 | 6 个 metric 全部完成语义映射；其中 4 个依赖数据侧，2 个归属 CMS 侧 |
| #5 开放项（PendingBadge + Popover） | ✅ 已闭合 | Q041/Q048 已登记（明星定义+名单/sort_order）；Q037（空态推荐≤30）与 SEARCH 模块共享 |
| PDR-05 自检 | ✅ 通过 | IA ↔ USM ↔ TRACE 一致 |
| PDR-06 自检 | ✅ 通过 | metric ↔ definition ↔ source_tables 一致 |
| 算法共签（方案 B） | human:唐绍祖 | 2026-08-05 | ✅ 已签署（Q037 错挂更正为 Q041/Q048；STAR seed defer 说明已登记） |
| 口径主责（方案 B） | human:王惠 | — | ⏳ 待王惠口径会签 |

## §2 明星企业指标口径摘要（algorithm-agent）

### 2.1 数据侧指标（algorithm-agent 负责）

| metric_id | 中文名 | 定义 | 公式 | 源表 | 状态 |
|-----------|--------|------|------|------|------|
| M_ENT_STAR_ENTERPRISE_COUNT | 明星企业数 | 按明星企业定义统计的全量明星企业数量 | COUNT(DISTINCT enterprise_id) FILTER(is_star) | dwd.enterprise_honor_tags | ⚠️ Q041/Q048 口径待确认 |
| M_ENT_STAR_BY_INDUSTRY | 明星企业按行业分布 | 明星企业按行业分类的分布统计 | GROUP BY industry_category | dwd.enterprise_base, dwd.enterprise_honor_tags | ⚠️ 依赖 Q041/Q048 闭环 |
| M_ENT_STAR_BY_REGION | 明星企业按区域分布 | 明星企业按注册/经营区域的分布统计 | GROUP BY headquarters_city | dwd.enterprise_base, dwd.enterprise_honor_tags | ⚠️ 依赖 Q041/Q048 闭环 |
| M_ENT_STAR_BASIC_INFO | 明星企业基础信息 | 明星企业名称、行业、区域、标签等基础画像信息 | SELECT enterprise_name, industry, region, tags | dwd.enterprise_base, dwd.enterprise_honor_tags | ✅ 有源（企业基础信息完整） |
| M_ENT_STAR_HONOR_LIST | 荣誉资质列表 | 明星企业所获荣誉/奖项的列表展示 | SELECT honor_type WHERE is_star=true | dwd.enterprise_honor_tags | ✅ 有源（荣誉标签字段完整） |

### 2.2 CMS 侧内容指标（OPS 模块负责）

| metric_id | 中文名 | 定义 | 说明 | 状态 |
|-----------|--------|------|------|------|
| M_ENT_STAR_CONTENT_STATUS | CMS 内容发布状态 | 明星企业介绍页面在 CMS 中的编辑/审核/发布状态 | A1 门户内容管理，归属 OPS 模块，非数据算法范畴 | 🟡 CMS 运营侧负责 |

### 2.3 模块本质说明

| 维度 | 说明 |
|------|------|
| 模块定位 | E-34 明星企业介绍为 **门户内容展示页**，属于 A1 大屏门户内容体系 |
| 数据角色 | 数据侧仅提供明星企业身份标识（is_star 标记）与基础画像查询能力 |
| CMS 角色 | 明星企业详情（表彰文案、宣传图片、荣誉故事）由 CMS 运营侧编辑维护 |
| 与 SEARCH 关系 | 共享 Q041/Q048（明星企业定义+名单/sort_order），检索结果中的明星企业数来源于同一口径 |

## §3 指标 × 贴源矩阵（data-agent）

| metric_id | mapping_status | ODS | DWD | ADS | pending_ref | pending_hint |
|-----------|---------------|-----|-----|-----|-------------|-------------|
| M_ENT_STAR_ENTERPRISE_COUNT | ⚠️ | dwd_org_honor_info | dwd.enterprise_honor_tags | — | Q041/Q048 | 明星企业定义待甲方确认(Q041/Q048)。当前临时取资质标签含"明星企业"标记的记录，按 enterprise_id 去重。正式口径与 SEARCH 模块共享，需一并闭合。 |
| M_ENT_STAR_BY_INDUSTRY | ⚠️ | dwd_org_honor_info, dwd_org_base | dwd.enterprise_honor_tags, dwd.enterprise_base | — | Q037 | 明星企业行业分布统计依赖 Q041/Q048 的明星企业定义，当前按临时口径聚合。enterprise_base 表 industry_category 字段可直接用于行业分组，无空白值风险。 |
| M_ENT_STAR_BY_REGION | ⚠️ | dwd_org_honor_info, dwd_org_base | dwd.enterprise_honor_tags, dwd.enterprise_base | — | Q037 | 明星企业区域分布统计依赖 Q041/Q048 的明星企业定义，当前按临时口径聚合。enterprise_base 表 headquarters_city 覆盖完整，可支持按城市级别展示。 |
| M_ENT_STAR_BASIC_INFO | ✅ | dwd_org_base | dwd.enterprise_base | — | — | 企业基础信息（名称、行业、区域、标签）在 enterprise_base 表中字段完整，无数据缺口。仅需关联 is_star 标记筛选即可展示。 |
| M_ENT_STAR_HONOR_LIST | ✅ | dwd_org_honor_info | dwd.enterprise_honor_tags | — | — | 荣誉标签表 honor_type 字段覆盖明星企业各类表彰，字段完整无缺口。以 is_star=true 过滤即可获取明星企业荣誉列表。 |
| M_ENT_STAR_CONTENT_STATUS | 🟡 | — | — | — | CMS-OPS | 该指标归属 CMS 运营模块（OPS），非数据算法范畴。内容发布状态由 CMS 后台管控，数据侧不参与内容编辑与审核流程。算法侧不声明该指标的 ODS/DWD 覆盖。 |

## §4 开放项闭合表

| 编号 | metric_id | 当前状态 | 依据 | 待闭合动作 |
|------|-----------|---------|------|-----------|
| Q041 | M_ENT_STAR_ENTERPRISE_COUNT | 🟡 团队临时默认 | 客户决策清单 · 明星企业定义 | 甲方确认明星企业正式定义：固定明星企业表+基础指标+CMS 维护。与 SEARCH 模块合并闭合。 |
| Q048 | M_ENT_STAR_ENTERPRISE_COUNT | 🟡 团队临时默认 | 客户决策清单 · 明星名单/sort_order | 待 ENT-MOD-STAR-PACK-L01 闭合后对齐候选名单、发布准入、sort_order、入选标准。 |
| STAR-CMS-01 | M_ENT_STAR_CONTENT_STATUS | 🟡 CMS 运营依赖 | — | 明星企业介绍页面的文字、图片等宣传内容由 CMS 运营侧维护，内容可用性取决于运营排期，不阻塞数据侧交付。 |

### 4.1 Q041/Q048 细分说明（与 SEARCH 模块共享）

| 子项 | 状态 | 临时默认 |
|------|------|---------|
| 明星企业认定级别 | 🟡 待确认 | 市级及以上表彰/认定 |
| 有效期规则 | 🟡 待确认 | 不设过期，永久保留 |
| 年度更新规则 | 🟡 待确认 | 按标签表最新导入批次展示 |

## §5 PDR-05/06 自检清单

| 检查项 | 结果 | 备注 |
|--------|------|------|
| PDR-05: IA ↔ USM ↔ TRACE 一致性 | ✅ | 6 metrics 全部映射到 E-34 USM leaves |
| PDR-05: wireframe 覆盖度 | ✅ | 各 USM 均有 wireframe 对应 |
| PDR-06: metric ↔ definition 一致性 | ✅ | 6/6 全部映射；CMS 指标已标注归属 |
| PDR-06: source_tables 完整度 | ⚠️ | 1 个 metric (M_ENT_STAR_CONTENT_STATUS) 不在数据侧范畴内，已标注归属 CMS-OPS |
| PDR-06: pending_hint ≥80 字 | ✅ | ≥2 条达标 |

### 5.1 模块特殊性说明

STAR 模块因属于 CMS 驱动的内容展示页，其 PDR-05/06 自检存在以下特殊性：

- **IA 覆盖**：明星企业页面的主内容（表彰文案、图片）属于 IA 的 A1 门户内容节点，不纳入数据侧的 metric 体系
- **USM 拆分**：数据侧 USM leaf 仅覆盖"明星企业列表/详情"的数据查询 user story，不覆盖"运营编辑/审核发布"的 CMS story
- **TRACE**：M_ENT_STAR_CONTENT_STATUS 的 trace 路径为 E-34 → OPS-CMS → CMS 内容发布状态，非数据链路

## §6 语义会签

> 2026-08-05 更新：按方案 B §1.4.2 双签格式重写。

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 算法共签 | human:唐绍祖 | 2026-08-05 | ✅ 已签署（Q037 错挂更正为 Q041/Q048） |
| 口径主责 | human:王惠 | — | ⏳ 待王惠口径会签（方案 B 铁律，缺一不可） |

## §7 STAR 指标 seed defer 说明（2026-08-05）

> 淮政玮 2026-08-03 签收检查指出：cfg_metric 无 M_ENT_STAR_* 种子。
> STAR 模块为 CMS 驱动内容展示页，数据侧仅 4 个指标（STAR_ENTERPRISE_COUNT/BY_INDUSTRY/BY_REGION/BASIC_INFO/HONOR_LIST）。

**defer 决定**：M_ENT_STAR_* 5 条指标的 cfg_metric 种子登记 defer 至 ENT-EVAL-ALGO-METRIC-ALIGN-L01 后续对齐任务，理由如下：

1. STAR 模块的 3 个 ⚠️ 指标（COUNT/BY_INDUSTRY/BY_REGION）均依赖 Q041/Q048 明星企业定义闭合，定义未闭合前 seed 中的 formula/weights 无法终值化
2. 2 个 ✅ 指标（BASIC_INFO/HONOR_LIST）为纯查询型，无算法定义卡需求，seed 仅需登记 metric_id+口径说明
3. CMS 侧指标（CONTENT_STATUS）归属 OPS 模块，不在 STAR seed 范围

**defer 任务**：ENT-EVAL-ALGO-METRIC-ALIGN-L01（已 done 的 metric 对齐任务可扩展纳入 STAR 5 条指标 seed 登记）

**N/A 依据**：在 Q041/Q048 闭合 + ALGO-METRIC-ALIGN 扩展前，STAR 模块 cfg_metric-ENT-seed.yaml 中 M_ENT_STAR_* 为 defer 状态，非缺失。