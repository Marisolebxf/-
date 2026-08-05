# METRIC-OPEN-ENT-KEYPANO-核对记录
# ENT-MOD-KEYPANO-METRIC-OPEN-L01 — 重点企业概览指标语义与 ODS/DWD 缺口核对

> **任务**：ENT-MOD-KEYPANO-METRIC-OPEN-L01
> **角色**：algorithm-agent + data-agent 双 Agent
> **监管人**：human:唐绍祖（§1.4.1 临时语义 Owner）
> **日期**：2026-07-29
> **上游**：ENT-MOD-KEYPANO-PACK-L01 ✅ done
> **范围**：E-33 重点企业概览（门户展示层，不计算新算法，消费其他模块结果）

---

## §1 适用性结论（Track-MS #4/#5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡（MetricSpecCard） | ✅ 已闭合 | 8 个 metric 中 6 个已映射至 ODS/DWD/ADS, 2 个需 Q047 闭合 |
| #5 开放项（PendingBadge + Popover） | ✅ 已闭合 | Q010/Q012/Q013/Q038/Q047 已登记; ≥2 条 pending_hint 达字段级粒度 |
| PDR-05 自检 | ✅ 通过 | IA ↔ USM ↔ TRACE 一致 |
| PDR-06 自检 | ✅ 通过 | metric ↔ definition ↔ source_tables 一致 |
| 算法共签（方案 B） | human:唐绍祖 | 2026-08-05 | ✅ 已签署（8 条 M_ENT_KEYPANO_* seed 已补登 cfg_metric-ENT-seed.yaml） |
| 口径主责（方案 B） | human:王惠 | — | ⏳ 待王惠口径会签 |

**核心判定**：KEYPANO 是门户概览页面，消费企业查询、企业画像、企业评估等模块的已计算结果。模块自身不产生新算法——所有指标均为对已入库数据的聚合、分组和展示。因此 6/8 指标 🔧（公式已注册，数据 agent 需建立 ADS 聚合层），2/8 ⚠️（领域映射口径依赖 Q013/Q047 闭合）。

## §2 指标口径摘要（algorithm-agent）

### 2.1 核心概览 KPI

| metric_id | 中文名 | 定义 | 公式 | 源表 | 状态 |
|-----------|--------|------|------|------|------|
| M_ENT_KEYPANO_MATCH_COUNT | 匹配企业数 | 当前产业链 + 链位条件下命中重点企业去重计数 | COUNT(DISTINCT enterprise_id) FILTER(industry_chain=:chain AND chain_node=:node AND is_published=1) | dwd.enterprise_base, E-37 CMS 发布状态 | 🔧 依赖 ADS 聚合 + CMS 发布标记 |
| M_ENT_KEYPANO_TYPE_COUNT | 覆盖企业类型数 | 当前结果集中至少命中 1 家企业的资质类型去重数 | COUNT(DISTINCT honor_type) FROM current_result_set | dwd.enterprise_honor_tags | 🔧 依赖 ADS 分组结果; ⚠️ Q010 外企/高企/小微/上市精确口径 |
| M_ENT_KEYPANO_REGIONAL_COUNT | 覆盖区域数 | 当前产业链下至少命中 1 家企业的行政区域去重数（市/省/国家三级） | COUNT(DISTINCT administrative_region) FROM dwd.enterprise_base WHERE industry_chain=:chain | dwd.enterprise_base | 🔧 依赖 ADS 按产业链预聚合 |
| M_ENT_KEYPANO_QUAL_DISTRIBUTION | 整链资质分布 | 当前整条产业链四项资质（外企/国高企/小微/上市）× 三个地域层级（深圳市/广东省/全国）的绝对数量横向分组条形图 | 4 qual_types × 3 region_levels grid: COUNT(DISTINCT enterprise_id) GROUP BY qual_type, region_level | dwd.enterprise_honor_tags + dwd.enterprise_base.region_level | 🔧 依赖 ADS 构建交叉分组聚合表; ⚠️ Q010/Q047 口径 |

### 2.2 展示结构指标

| metric_id | 中文名 | 定义 | 公式 | 源表 | 状态 |
|-----------|--------|------|------|------|------|
| M_ENT_KEYPANO_TYPE_STRUCTURE | 企业类型分布（当前链位） | 当前链位下按资质类型分组的企业数量分布，用于类型结构图 | COUNT(DISTINCT enterprise_id) GROUP BY honor_type FROM current_chain_node | dwd.enterprise_honor_tags | 🔧 依赖 ADS 按链位分组 |
| M_ENT_KEYPANO_REGIONAL_DISTRIBUTION | 区域分布 | 当前产业链下按行政区域分组的企业数量分布，用于空间分布视图 | COUNT(DISTINCT enterprise_id) GROUP BY administrative_region FROM dwd.enterprise_base WHERE industry_chain=:chain | dwd.enterprise_base | 🔧 依赖 ADS 按产业链 + 区域分组 |
| M_ENT_KEYPANO_ENTERPRISE_LIST | 企业清单（当前链位） | 当前链位下重点企业分页列表，含企业名称、资质标签、基础信息 | SELECT enterprise_id, enterprise_name, honor_type_list, region_level FROM enterprise_base/honor_tags JOIN chain_node_mapping WHERE chain_node=:node | dwd.enterprise_base + dwd.enterprise_honor_tags + 产业链映射表 | 🔧 依赖 ADS 构建 JOIN 视图; ⚠️ 企业识别阈值 Q038 |
| M_ENT_KEYPANO_DOMAIN_SUMMARY | 领域摘要（当前链位） | 当前链位下论文/专利关键词到产业领域/环节的映射结果及关联企业 | 关键词抽取 → 领域映射 → COUNT 分组; 证据来源: dwd_paper_keywords, dwd_patent_keywords | dwd.paper_info + dwd.patent_info + 领域映射规则表 | ⚠️ 领域映射规则依赖 Q013/Q047 闭合; 关键词抽取算法独立于 KEYPANO |

## §3 指标 × 贴源矩阵（data-agent）

| metric_id | mapping_status | ODS | DWD | ADS | pending_ref | pending_hint |
|-----------|---------------|-----|-----|-----|-------------|-------------|
| M_ENT_KEYPANO_MATCH_COUNT | 🔧 | ods_enterprise_info | dwd.enterprise_base | ads.enterprise_keypano_chain_node_summary | Q038 | 匹配企业数依赖重点企业识别阈值（Q038 未闭合）。当前临时方案以专利数≥3 且 CMS 已发布作为识别规则。产业链→企业映射需要 ADS 层预计算。详见 cfg_metric Q038。 |
| M_ENT_KEYPANO_TYPE_COUNT | 🔧 | ods_organization_honor | dwd.enterprise_honor_tags | ads.enterprise_keypano_qual_summary | Q010 | 外企/高企/小微/上市四类口径的精确判定规则待甲方确认（Q010）。当前复用 E-32/E-33 系统通用资质荣誉枚举，取 honor_type 标签值匹配计数。多标签企业允许多次出现，统计值不可直接相加为企业总数。 |
| M_ENT_KEYPANO_QUAL_DISTRIBUTION | 🔧 | ods_organization_honor | dwd.enterprise_honor_tags | ads.enterprise_keypano_chain_qual_matrix | Q010, Q047 | 整链资质分布需构建 4(资质类型)×3(地域层级)交叉分组矩阵。地域层级取完整嵌套口径（深圳市/广东省/全国各自独立计数，非增量叠加）。资质口径依赖 Q010，正式 metric_id 与地域聚合规则由 Q047 管理。 |
| M_ENT_KEYPANO_TYPE_STRUCTURE | 🔧 | ods_organization_honor | dwd.enterprise_honor_tags | ads.enterprise_keypano_node_type | Q010 | 当前链位类型结构按 honor_type 分组计数。同一企业可命中多个资质标签，占比计算不得将多标签企业误解为互斥分类，「主导类型占比」在多标签口径下存在无决策价值的100%风险。IA §5.1 已明确顶部不展示主导类型占比，仅保留在当前区域类型结构中。 |
| M_ENT_KEYPANO_REGIONAL_COUNT | 🔧 | ods_enterprise_info | dwd.enterprise_base | ads.enterprise_keypano_chain_region_summary | Q012 | 行政区域覆盖数按产业链+区域层级聚合。Q012 行政区划下钻精度与密度分母未定，当前取 Bid 明确的国家/省/市三级。市级到区县仅为地图展示深化（product_interpretation），不新增区县分析指标层。 |
| M_ENT_KEYPANO_REGIONAL_DISTRIBUTION | 🔧 | ods_enterprise_info | dwd.enterprise_base | ads.enterprise_keypano_chain_region_detail | Q012 | 区域分布按行政区域分组展示企业数量。密度/集聚指数因 Q012 公式未定暂不纳入 KEYPANO 展示，仅表达绝对数量。区域企业规模和区域占比（GAP-KEYENT-REGIONAL-SCALE/RATIO）因无正式 metric_id 暂缺，业务模式省略或显示正常不可用态。 |
| M_ENT_KEYPANO_ENTERPRISE_LIST | 🔧 | ods_enterprise_info | dwd.enterprise_base + dwd.enterprise_honor_tags | ads.enterprise_keypano_node_enterprise_list | Q038, Q039 | 企业清单需 JOIN enterprise_base + honor_tags + CMS 发布状态。重点企业识别阈值依赖 Q038（当前临时取专利数阈值初版）。前端不计算评分/排名/推荐。企业档案来自 E-37 CMS 已发布内容，未发布行显示"档案待维护"。 |
| M_ENT_KEYPANO_DOMAIN_SUMMARY | ⚠️ | ods_paper_keywords, ods_patent_keywords | dwd.paper_info, dwd.patent_info | — | Q013, Q047 | 领域摘要的关键词→产业领域→环节→链位映射规则需 Q013 闭合领域分类体系 + Q047 闭合正式映射口径。当前 DEMO 阶段以论文/专利关键词与领域名称的模糊匹配代理，评审模式标记待确认。业务模式不展示依赖 Q013 的覆盖广度/参与深度/多元化指数。 |

## §4 开放项闭合表

| 编号 | metric_id | 当前状态 | 依据 | 待闭合动作 |
|------|-----------|---------|------|-----------|
| Q010 | M_ENT_KEYPANO_TYPE_COUNT, M_ENT_KEYPANO_QUAL_DISTRIBUTION, M_ENT_KEYPANO_TYPE_STRUCTURE | 🟡 团队临时默认 | PDR 纪要; IA-KEYENT §5.1 | 甲方确认外企/高企/小微/上市精确判定规则及有效期 |
| Q012 | M_ENT_KEYPANO_REGIONAL_COUNT, M_ENT_KEYPANO_REGIONAL_DISTRIBUTION | 🟡 团队临时默认 | PDR 纪要; IA-KEYENT §5.1 | 甲方确认行政区划下钻精度、密度分母及集聚指数公式 |
| Q013 | M_ENT_KEYPANO_DOMAIN_SUMMARY | 🟡 团队临时默认 | PDR 纪要; IA-KEYENT §5.5 | 甲方+算法确认领域覆盖分类体系、覆盖广度/深度/多元化计算口径 |
| Q038 | M_ENT_KEYPANO_MATCH_COUNT, M_ENT_KEYPANO_ENTERPRISE_LIST | 🟡 算法临时默认 | TRACE-ENT-KEYPANO; IA-KEYENT §9 | 算法确认重点企业识别阈值；当前临时方案不包装为推荐排名 |
| Q039 | M_ENT_KEYPANO_ENTERPRISE_LIST | 🟡 文案对齐中 | TRACE-ENT-KEYPANO; IA-KEYENT §5.4 | 高颖确认评审模式重点企业口径说明与算法描述一致 |
| Q047 | M_ENT_KEYPANO_QUAL_DISTRIBUTION, M_ENT_KEYPANO_DOMAIN_SUMMARY | ❌ 正式指标口径待定 | USM-ENT-KEYPANO §8; TRACE-ENT-KEYPANO open_question_ids | 何老师确认正式 metric_id、地域层级聚合口径与关键词→产业链映射规则 |
| GAP-KEYPANO-REGIONAL-SCALE | M_ENT_KEYPANO_REGIONAL_DISTRIBUTION | ❌ 正式数据无源 | IA-KEYENT §7; TRACE-ENT-KEYENT explicit_metric_gaps | 区域企业规模分布尚无正式 metric_id；正式注册前业务模式省略或显示正常不可用态 |
| GAP-KEYPANO-REGIONAL-RATIO | M_ENT_KEYPANO_REGIONAL_DISTRIBUTION | ❌ 正式数据无源 | IA-KEYENT §7; TRACE-ENT-KEYENT explicit_metric_gaps | 区域企业占比无源且不得用高企占比替代；正式展示前注册独立 metric_id |
| GAP-KEYPANO-CHAIN-MAPPING | M_ENT_KEYPANO_ALL | 🟡 数据适配中 | IA-ENT-KEYPANO §8 | 产业链→企业映射表、链位→企业关联关系需数据 agent 构建 ADS 层预计算视图 |

## §5 PDR-05/06 自检清单

| 检查项 | 结果 | 备注 |
|--------|------|------|
| PDR-05: IA ↔ USM ↔ TRACE 一致性 | ✅ | E-33 三项原始功能 5 user stories 全部映射至 8 metric |
| PDR-05: wireframe 覆盖度 | ✅ | 各 USM 均有 wireframe 对应（F-KEYPANO-00～04） |
| PDR-06: metric ↔ definition 一致性 | ✅ | 8/8 metric 已注册 definition 与 formula |
| PDR-06: source_tables 完整度 | ⚠️ | 2 个 metric (DOMAIN_SUMMARY, QUAL_DISTRIBUTION 地域维度) 部分依赖待闭合规则 |
| PDR-06: pending_hint ≥80 字 | ✅ | ≥3 条达标 |
| PDR-06: KEYPANO 不计算新算法 | ✅ | 全部指标为聚合/分组/JOIN 消费，不产生算法模型 |
| PDR-06: 整链资质分布使用完整嵌套口径 | ✅ | 深圳市/广东省/全国各自独立计数，非增量堆叠 |

## §6 语义会签

> 2026-08-05 更新：按方案 B §1.4.2 双签格式重写。

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 算法共签 | human:唐绍祖 | 2026-08-05 | ✅ 已签署（8 条 M_ENT_KEYPANO_* seed 已补登；defer 已闭合） |
| 口径主责 | human:王惠 | — | ⏳ 待王惠口径会签（方案 B 铁律，缺一不可） |

---

## §A 附记：KEYPANO 消费链路

KEYPANO 作为门户概览，不计算新算法，其数据链路如下：

| 消费来源 | 消费内容 | 本模块职责 | 不可承担 |
|---------|---------|-----------|---------|
| 企业识别（Q038） | 重点企业名单 | 展示已识别企业 | 不调整识别阈值或排名规则 |
| 企业查询模块 | 企业基础信息、资质标签 | JOIN enterprise_base + honor_tags 构建视图 | 不复制查询筛选逻辑 |
| E-37 CMS | 已发布企业档案 | CMS 未发布行显示"档案待维护" | 不编辑/审核/发布 |
| 论文/专利数据 | 关键词映射证据 | 展示数据 agent 预计算领域映射结果 | 不运行 NLP 抽取算法 |
| 产业链管理 | 产业链→链位结构 | 展示映射关系 | 不编辑产业链拓扑 |
| 企业评估/风险模块 | 评分、评级 | 不消费（KEYPANO 不展示评分/风险/排名/推荐） | 不暴露算法参数 |

## §7 KEYPANO 指标 seed 补登说明（2026-08-05）

> 淮政玮 2026-08-03 签收检查指出：cfg_metric 无 M_ENT_KEYPANO_*。
> 2026-08-05 已补登 8 条 seed 至 cfg_metric-ENT-seed.yaml（total_metrics 52→60）。

**已补登 8 条**：
1. M_ENT_KEYPANO_MATCH_COUNT（🔧 Q038）
2. M_ENT_KEYPANO_TYPE_COUNT（🔧 Q010）
3. M_ENT_KEYPANO_REGIONAL_COUNT（🔧 Q012）
4. M_ENT_KEYPANO_QUAL_DISTRIBUTION（🔧 Q010/Q047）
5. M_ENT_KEYPANO_TYPE_STRUCTURE（🔧 Q010）
6. M_ENT_KEYPANO_REGIONAL_DISTRIBUTION（🔧 Q012）
7. M_ENT_KEYPANO_ENTERPRISE_LIST（🔧 Q038/Q039）
8. M_ENT_KEYPANO_DOMAIN_SUMMARY（⚠️ Q013/Q047）

**说明**：KEYPANO 为门户概览消费模块，不计算新算法。8 条 seed 均为聚合/分组/JOIN 公式，mapping_status 按核对记录 §3 矩阵如实标注（7 条 🔧 + 1 条 ⚠️）。Q010/Q012/Q013/Q038/Q039/Q047 未闭合前 formula 为临时口径，待甲方确认后终值化。