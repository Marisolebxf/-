# 三页面（M4/M5/M6）久新取数判定表

> **日期**：2026-10-29　**实测库**：久新 Doris `gkx_technology_analysis_dev`
> **边界**：地域范围 / 维度定义 / 页面结构**一律以展示系统（需规 + 原型）为准**，久新只作数据源配合

## 0. 边界（human 2026-10-29 核定）

1. 地域范围、维度定义、页面结构**以展示系统为准**，不因久新数据结构而改。
2. 久新是**数据源之一**，配合展示取数；缺数出空态 + `emptyReason`，**不补 0、不编口径**。
3. **不修改页面结构与样式**。

## 1. 地域覆盖实测

| 层级 | 维表 | 指标表实测 | 结论 |
|---|---|---|---|
| **COUNTRY** | 232 | **216 国 / 年**（2024） | ✅ M4 全球可用 |
| **CITY** | 19729 | 17 万行 | ✅ M5 / M6 可用 |
| **DISTRICT** | 9（恰为深圳 9 区） | **0 行** | ❌ M6 区级**无数据**，只能空态 |

### 湾区 11 城逐城实测（展示系统口径：简称）

| 城市 | 久新精确名 | 状态 | 数据年份 |
|---|---|---|---|
| 广州 | 广州市 | ✅ | 2000–2026（27 行） |
| 深圳 | 深圳 | ✅ | 2000–2026（27 行） |
| 东莞 | 东莞市 | ✅ | 2000–2026（27 行） |
| 珠海 | 珠海市 | ✅ | 2001–2026（25 行） |
| 佛山 | 佛山市 | ✅ | 2000–2026（25 行） |
| 江门 | 江门 | ✅ | 2001–2026（17 行） |
| 惠州 | 惠州 | ✅ | 2002–2026（16 行） |
| 肇庆 | 肇庆市 | ✅ | 2004–2026（16 行） |
| **中山** | 中山市 | ❌ **no_data** | 实体存在，指标表 0 行 |
| **香港** | — | ❌ **no_source** | 维表无此实体 |
| **澳门** | — | ❌ **no_source** | 维表无此实体 |

**8 / 11 城有数据，3 城空态。**

## 2. 两个必须记住的坑

### 坑 1：中山同名污染（**禁用模糊匹配**）

库中 CITY 级同时存在三个实体：

| 实体 | 指标表行数 | 说明 |
|---|---|---|
| 中山市 | **0** | 本体，无数据 |
| 中山 | **0** | 同名 |
| **中山村** | **16** | **是村，不是市** |

若用 `LIKE '中山%'`，会把**村的数据当中山市出数**。因此城市名**必须精确映射**，实现见
`geo_indicator.py` 的 `SHOW_TO_JIUXIN_CITY`。

### 坑 2：国家级中文名为空

国家级 `name_zh` **215/216 为 NULL**，只有 `name_en` 有值。取国家名必须
`COALESCE(name_zh, name_en)`，否则 216 国只会被识别成 2 个。

## 3. 可用指标（`ads_geo_yearly_metrics`，30 字段）

| 组 | 字段 |
|---|---|
| 论文 | `paper_count` · `paper_fractional_count` · `cited_by_count` · `citation_count` |
| 项目 | `project_count` · `project_fractional_count` · `direct_project_count` · `inferred_project_count` |
| 人才 | `talent_count` · `talent_participation_count` · `new_talent_count` · `inbound/outbound_talent_count` |
| 机构 | `institution_count` · `paper_active_institution_count` · `project_start_institution_count` · `new_institution_count` |
| 流动 | `mobility_event_count` |

**自带质量信号**（对应契约 `asOf` 与角标就绪度）：
`metrics_as_of_date`（实测 **2026-09-18**）、`location_resolved_ratio`、
`*_coverage_status`（5 组）、`metric_definition_version`。

## 4. 15 个端点判定

| # | 端点 | 久新能否补 | 判定 |
|---|---|---|---|
| 1 | M4 achievements | ⚠️ 部分 | 落点可用 COUNTRY 级；成果实体待验证 |
| 2 | M4 realtime | ✅ **能补** | 年度序列 + 216 国五维 |
| 3 | M4 carriers | ❌ 不能 | 载体是 innov 概念，久新无 |
| 4 | M4 alerts | ❌ 不能 | 久新无预警 |
| 5 | M4 cities | ✅ **能补** | 216 国 × 五维 |
| 6 | M5 achievements | ⚠️ 部分 | 仅 8 城有落点 |
| 7 | M5 capability | ✅ **能补** | 四维可映射 + 历史序列 |
| 8 | M5 swot | ❌ 不能 | 纯算法，久新无 |
| 9 | M5 indicators | ⚠️ 部分 | 6 指标中仅论文有源；专利不可靠；**产值/投入/技术合同久新也没有** |
| 10 | M5 alerts | ❌ 不能 | — |
| 11 | M6 carriers | ⚠️ 部分 | 载体本身无，`talents` 可用 `talent_count` 补 |
| 12 | M6 indicator-systems | ❌ 不能 | 依赖算法侧 |
| 13 | M6 field-distribution | ⏸ **待拍板** | 口径映射见 `SITUATION-IM-DOMAIN-MAPPING-DRAFT.md` |
| 14 | M6 city-benchmark | ✅ **能补** | CITY 级四维 + 人才流动 |
| 15 | M6 operation-timeline | ❌ 不能 | — |

**能补（5）**：M4 realtime / M4 cities / M5 capability / M6 city-benchmark / M6 carriers 的 talents
**补不了（6）**：carriers(M4) / alerts(M4,M5) / swot / indicator-systems / operation-timeline —— 均为 innov 或算法概念
**久新自身也没有**：创新产值、创新投入、创新比例、技术合同（统计年鉴口径）

## 5. 已实装接口

`lumen-topic-py` · `gkx_show_service/views/geo_indicator.py`

| 接口 | 用途 |
|---|---|
| `POST /internal/gkx-show/geo/metrics` | 通用地域取数：`scope`(gba/global/custom) × `groups`(五组) × 年度区间，返回 items + **missing** + `as_of` |
| `POST /internal/gkx-show/geo/coverage` | 覆盖自检：展示系统名单中哪些有源、哪些空态 |

**冒烟结果（2026-10-29）**

| 场景 | 结果 |
|---|---|
| 湾区覆盖自检 | total=11, available=8，香港/澳门 `no_source`、中山 `no_data` |
| 湾区 2024 论文 | 8 城出数，例 广州 31788 / 深圳 17596；`as_of=2026-09-18` |
| 中山防污染 | items 0 条、missing 1 条 ✅ 未误取「中山村」 |
| 全球 2024 | 216 国 ✅（修复 `name_en` 回退后） |
| 人才+机构 | 广州 talent=10672 / inst=183 ✅ |
| 只读防护 | `DROP TABLE` 被拦截 ✅ |

## 6. 待拍板

1. **M6 八大产业 ↔ 久新集群映射**（见 `SITUATION-IM-DOMAIN-MAPPING-DRAFT.md`）。未定前 M6 领域分布保持空态。
2. **M6 区级筛选**：久新 DISTRICT 指标表 0 行，契约 §4.7 亦只到市本级 → 空态，不得谎称支持。
3. **M5 缺 3 城**（中山、香港、澳门）：页面按展示系统仍画 11 城，久新侧这 3 城出空态 + 原因。
