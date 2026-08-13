# 产业链 ADS 表设计 — 原型与 Handoff 驱动（v2）

> **现行存储入口（S4）**：[`../storage/CHAIN/stores/mysql/ads.md`](../storage/CHAIN/stores/mysql/ads.md) · 总览 [`../storage/CHAIN/README.md`](../storage/CHAIN/README.md)  
> 本文为 **ADS 字段细表现行真源**（S3 指针已切）；导航首页走 `storage/CHAIN`。冲突以 `storage/CHAIN` 叙述为准。

| 属性 | 内容 |
|------|------|
| 文档编号 | DATA-CHAIN-ADS-v2 |
| 版本 | v2.0.0 |
| 状态 | **S3 现行真源**（团队认定 DWD+ADS 已定 · 2026-08-13）；多签纸面可补 OPEN-CHAIN-ADS-V2-01 |
| 作者 | architect-agent · 监管 human:李伟 |
| 创建日期 | 2026-08-13 |
| 引擎 | **MySQL 8** · 正式库 `gkxlumenx_ads` · Demo `demo_gkxlumenx_ads` |
| 上游 DWD | [`产业链-DWD表设计-业务需求驱动(v5).md`](./产业链-DWD表设计-业务需求驱动(v5).md) |
| 指标真源 | `agent-delivery/metrics/cfg_metric-CHAIN-seed.yaml`（60 × `M_CHAIN_*`） |
| 产品真源 | `agent-handoffs/产品整体定义/E2-产业链分析/**` 五件套 + DEC + DESIGN-LANDING |
| storage 指针 | **已更新** [`storage/CHAIN/stores/mysql/ads.md`](../storage/CHAIN/stores/mysql/ads.md)（S3 收口） |

> **与既有稿关系**：[`产业链-ADS表设计-业务需求驱动(v1).md`](./产业链-ADS表设计-业务需求驱动(v1).md) **保持不动**，仅作对照。  
> 本稿从 **原型 Wireframe / TRACE / DEC / Analysis Job Runtime / 全景状态对比 DEC** 反推 Java 只读契约面，不「改名平移」旧十一表，也不默认继承 v1 的字段定稿。

---

## 0. 设计目标与非目标

### 0.1 目标

1. 门户总览、专题全景、诊断/区域/深圳 **同步读路径**（`GET /v1/chain/**`）有明确 ADS 表。  
2. 60 条 `M_CHAIN_*` 均有落表形态（单值 / 序列 / 分布 / 矩阵）。  
3. 全景「状态对比 / 数据截至」有 **发布快照 + diff** 契约（对齐 `DEC-CHAIN-PANORAMA-STATUS-COMPARE-20260812`）。  
4. 与 **Analysis Job Result Snapshot**、**CMS**、**Nebula**、**DWD** 边界钉死，避免双真源。

### 0.2 非目标

| 不做 | 去向 |
|---|---|
| 链 / 节点 / 边 / 事件明细 | DWD `industry_chain_*` |
| 模型原子评分 / 标签 / 单对象排名 | DWD `industry_chain_model_result_detail` |
| 七键「生成分析」Input/Result 不可变包 | Job Snapshot Store（Runtime §8，**与全景发布快照分表**） |
| 产业介绍 / 发展历程正文 | CMS |
| 永久图谱边 / 在线图遍历 | NebulaGraph（由 DWD 投影） |
| 任务态 / 互斥 / Stage 事件 | `analysis_job*`（平台/业务库，非本稿指标 ADS） |

---

## 1. 三面读模型（先于表清单）

```text
┌─────────────────────────────── 前端 ───────────────────────────────┐
│  同步页（总览 KPI / 分布 / 资讯统计 / 全景当前态&对比）              │
│  生成分析页（配置→过程→显式查看结果）                              │
│  CMS 图文（介绍 / 历程）                                           │
└───────────────┬──────────────────────┬──────────────────┬─────────┘
                │                      │                  │
                ▼                      ▼                  ▼
         Java 只读 ADS          Java Job API         Java CMS API
         （本稿 9 张表）      Result Snapshot Store     （非 ADS）
                │                      │
                │                      │ 运行时可读 ADS 事实
                ▼                      ▼
         指标/TopN/结论/图发布包    Python Graph（只读 ADS + DWD）
```

| 面 | 典型页面 | 存储 |
|---|---|---|
| **A. 同步 ADS** | 总览概况/深圳现状 KPI、资讯统计、区域分布卡、全景发布态 | 本稿表 |
| **B. Job Snapshot** | 周期 / 关键 / 瓶颈 / 区域指数·竞争力 / 深圳对比·发展 | Runtime `analysis_snapshot`（input\|result） |
| **C. CMS** | 产业介绍、发展历程 | CMS |
| **D. Nebula** | 全景在线结构查询（非历史发布包） | Nebula；历史对比走 ADS 发布快照 |

**铁律（摘 DEC / Runtime）**

- Job Result Snapshot **禁止**与全景发布快照混表。  
- 前端 **禁止**自算正式 diff / 正式指数；正式值只读已发布 ADS 或已签发 Result Snapshot。  
- Java **禁止**写 ADS；写方 = Python / 指标引擎 / 发布作业。

---

## 2. 页面 × 数据面覆盖矩阵

> 依据：门户/专题 Wireframe、METRIC-OPEN 模块矩阵、ISOMORPH 七键、全景 DEC。

| 模块 / 路由（规范） | 主消费 | ADS 落表 | 非 ADS |
|---|---|---|---|
| 门户总览 · 整体概况 `/industry-center/overview` Tab 概况 | KPI 卡片、区域分布 | `metric_fact` + `metric_series` + `region_dist` | 介绍正文→CMS |
| 门户 · 产业资讯 | 计数 / 热度 / 情感占比 | `metric_fact` / `metric_series`；列表明细可走 ES/DWD 投影 API | 正文外链 |
| 门户 · 发展历程 | — | — | **CMS only** |
| 门户 · 深圳产业现状 | SZ_* KPI | `metric_fact` | — |
| 门户 · 全景（结构+简介） | 当前发布图 + 节点简介 | `graph_snapshot`（当前=最新 published）；节点简介属性以包内物化 / DWD 当前版 | 演进控件不在门户 |
| 专题全景 · 当前/演进/状态对比 | 发布包 + diff | `graph_snapshot` + `graph_diff` | 直播 DWD 须角标「含未发布」 |
| 诊断 · 周期 / 关键 / 瓶颈 | 生成分析结果 | 过程中可读 `metric_fact`；**成品**→ Job Result | 原子分→DWD |
| 区域 · 指数 / 竞争力 | 正式结果 | 可选沉淀 `region_scorecard` / `metric_fact` 供同步卡；**正式结果包**→ Job Result | WYSIWYG 预览不算正式 |
| 深圳 · 对比 / 发展 | 正式结果 | 同步 KPI→`metric_fact`；机遇/布局结论→`conclusion`+`narrative`；正式包→ Job Result | — |
| OPS 维护 | 配置/审核 | 不进本稿 | 业务库 / CMS |

---

## 3. 命名与公共约定

- 表名：**不加** `ads_` 前缀；统一 `industry_chain_*`（靠库名 `gkxlumenx_ads` 分层）。  
- 业务键：与 Q053 / DWD v5 一致 — `industry_id` / `chain_id` / `node_id` = INB 原文。  
- 物理主键：`id BIGINT AUTO_INCREMENT`。  
- 公共列：`calc_batch_id`、`data_version`、`is_deleted`、`created_time`、`updated_time`。  
- 模型派生行必须可回链：`run_id` · `result_id`（可空）· `metric_id` · `metric_version`。  
- `object_type`：`industry` | `chain` | `node` | `region` | `event`。

---

## 4. 表总览（9 张）

| # | 表名 | 一句话 | 主要消费 |
|---|---|---|---|
| 1 | `industry_chain_metric_fact` | 指标快照（卡片 KPI / 排名 / 占比 / 枚举阶段） | 总览、深圳、全景计数对账 |
| 2 | `industry_chain_metric_series` | 指标时序点 | 趋势图 |
| 3 | `industry_chain_metric_dist` | 分布型指标（类型占比、分档计数） | 瓶颈类型分布等 |
| 4 | `industry_chain_region_dist` | 区域分布行（地图/列表） | 整体概况地域卡 |
| 5 | `industry_chain_region_scorecard` | 区域评价 / 四力矩阵行 | 区域指数同步投影 |
| 6 | `industry_chain_topn` | TopN 列表行 | 关键节点、热点资讯、重点企业 |
| 7 | `industry_chain_conclusion` | 产品化结论头 | 机遇/布局/跃升/方案标题 |
| 8 | `industry_chain_narrative` | 长文本解释（非 CMS） | 方案正文、页面解读 |
| 9 | `industry_chain_graph_snapshot` + `industry_chain_graph_diff` | 全景**发布**快照与演进 diff | 专题全景状态对比 |

> 计数：快照与 diff 为配套 2 张物理表，契约上算一组；**物理共 10 张**，对外称「9 组能力 / 10 表」。为避免歧义，清单写清：

| 物理表 | |
|---|---|
| 1–8 | 上表 1–8 |
| 9 | `industry_chain_graph_snapshot` |
| 10 | `industry_chain_graph_diff` |

相对 v1 的增量意图（对照用，不修改 v1）：

- 新增 **`metric_dist`**：承接 `M_CHAIN_BOTTLENECK_TYPE_DIST` 等非标量。  
- 新增 **`region_dist`**：承接门户「全球/全国区域分布」行级数据（Wireframe F-CHAIN-OV-07）。  
- **强化** `graph_snapshot` / `graph_diff`：对齐全景 DEC（`publish_status`、`effective_at`、`layout_baseline_id`、`confirm_status`）。  
- **明确排除** Job Snapshot 表。

---

## 5. 表结构（字段级）

### 5.1 `industry_chain_metric_fact`

**用途**：对象 × 指标 × 统计期的发布快照。覆盖绝大多数标量 `M_CHAIN_*`。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `industry_id` | VARCHAR(64) | 否 | L0 |
| `chain_id` | VARCHAR(64) | 否 | 子链；与 industry 至少其一 |
| `node_id` | VARCHAR(64) | 否 | 节点级 |
| `object_type` | VARCHAR(32) | 是 | §3 |
| `object_id` | VARCHAR(64) | 是 | |
| `region_code` | VARCHAR(32) | 是 | 默认 `ALL` |
| `metric_id` | VARCHAR(64) | 是 | 须在 cfg_metric |
| `metric_version` | VARCHAR(32) | 是 | |
| `stat_period_type` | VARCHAR(16) | 是 | `day`/`month`/`quarter`/`year`/`snapshot` |
| `stat_period` | VARCHAR(32) | 是 | |
| `metric_value` | DECIMAL(24,6) | 否 | 数值主值 |
| `metric_label` | VARCHAR(128) | 否 | 枚举展示（如周期阶段名） |
| `value_unit` | VARCHAR(32) | 否 | |
| `yoy` / `mom` / `ratio` | DECIMAL(12,6) | 否 | |
| `rank_no` / `rank_total` | INT | 否 | |
| `run_id` / `result_id` | VARCHAR(64) | 否 | 模型派生必填 run_id |
| `calc_batch_id` | VARCHAR(64) | 是 | |
| `publish_status` | VARCHAR(16) | 是 | `draft`/`published`/`deprecated`；API 默认只读 published |
| `ext_json` | JSON | 否 | 禁止塞整页 payload |
| `is_deleted` | TINYINT | 是 | 默认 0 |
| `created_time` / `updated_time` | DATETIME | 是 | |

**UK**：`(object_type, object_id, region_code, metric_id, metric_version, stat_period_type, stat_period, calc_batch_id)`

**典型 metric**：`ENTERPRISE_COUNT`、`MARKET_SIZE`、`NODE_COUNT`、`EDGE_COUNT`、`CYCLE_STAGE`、`SZ_*`、`INVEST_*`、`NEWS_COUNT` 等。

---

### 5.2 `industry_chain_metric_series`

**用途**：趋势点列；与 fact 分离。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `industry_id` / `chain_id` / `node_id` | VARCHAR(64) | 否 | |
| `object_type` / `object_id` | | 是 | |
| `region_code` | VARCHAR(32) | 是 | 默认 `ALL` |
| `metric_id` / `metric_version` | | 是 | |
| `stat_period_type` / `stat_period` | | 是 | 序列上一点 |
| `metric_value` | DECIMAL(24,6) | 否 | |
| `yoy` / `mom` | DECIMAL(12,6) | 否 | |
| `calc_batch_id` / `run_id` / `result_id` | | 批次必填 | |
| `publish_status` | VARCHAR(16) | 是 | |
| `is_deleted` / 时间戳 | | 是 | |

**UK**：同 fact 形态（含 `calc_batch_id`）。

---

### 5.3 `industry_chain_metric_dist`

**用途**：一个指标拆多桶（类型分布、分档）。避免把分布硬塞 `metric_value` 单值。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `industry_id` / `chain_id` / `node_id` | VARCHAR(64) | 否 | |
| `object_type` / `object_id` | | 是 | |
| `region_code` | VARCHAR(32) | 是 | 默认 `ALL` |
| `metric_id` / `metric_version` | | 是 | 如 `M_CHAIN_BOTTLENECK_TYPE_DIST` |
| `stat_period_type` / `stat_period` | | 是 | |
| `bucket_code` | VARCHAR(64) | 是 | 如 `tech`/`talent`/`market`/`capital`/`policy` |
| `bucket_name` | VARCHAR(128) | 否 | |
| `bucket_value` | DECIMAL(24,6) | 否 | 计数或占比 |
| `bucket_ratio` | DECIMAL(12,6) | 否 | |
| `calc_batch_id` / `run_id` / `result_id` | | 批次必填 | |
| `publish_status` | VARCHAR(16) | 是 | |
| `is_deleted` / 时间戳 | | 是 | |

**UK**：`(object_type, object_id, region_code, metric_id, metric_version, stat_period, bucket_code, calc_batch_id)`

---

### 5.4 `industry_chain_region_dist`

**用途**：门户「区域分布地图/列表」（F-CHAIN-OV-07）：一行一区域的主体计数与可选指标。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `industry_id` / `chain_id` | VARCHAR(64) | 否 | 至少一 |
| `geo_scope` | VARCHAR(16) | 是 | `global` / `national` / `province` / `city` / `district` |
| `region_code` | VARCHAR(32) | 是 | |
| `region_name` | VARCHAR(128) | 否 | |
| `stat_period_type` / `stat_period` | | 是 | |
| `enterprise_count` | INT | 否 | 可与 fact 对账 |
| `institution_count` | INT | 否 | |
| `metric_payload` | JSON | 否 | 其它度量；正式 KPI 仍鼓励拆 fact |
| `calc_batch_id` | VARCHAR(64) | 是 | |
| `publish_status` | VARCHAR(16) | 是 | |
| `is_deleted` / 时间戳 | | 是 | |

**UK**：`(COALESCE(industry_id,'*'), COALESCE(chain_id,'*'), geo_scope, region_code, stat_period, calc_batch_id)`

---

### 5.5 `industry_chain_region_scorecard`

**用途**：区域产业评价「四力」行（对齐 QC05/QC11 临时命名：商业力/技术力/学术力/支撑力）。  
正式 Job 结果仍以 Result Snapshot 为准；本表供同步榜单/卡片投影。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `industry_id` / `chain_id` | VARCHAR(64) | 否 | 至少一 |
| `region_code` / `region_name` | | 是/否 | |
| `stat_period_type` / `stat_period` | | 是 | |
| `score_total` | DECIMAL(12,6) | 否 | ↔ `M_CHAIN_REGION_INDEX` |
| `score_commerce` | DECIMAL(12,6) | 否 | 商业力（临时名，QC11） |
| `score_tech` | DECIMAL(12,6) | 否 | 技术力 |
| `score_academic` | DECIMAL(12,6) | 否 | 学术力 |
| `score_support` | DECIMAL(12,6) | 否 | 支撑力 |
| `rank_no` | INT | 否 | |
| `dimension_json` | JSON | 否 | 12 叶子贡献等扩展 |
| `metric_id` / `metric_version` | | 否 | 主综合分 |
| `template_id` | VARCHAR(64) | 否 | 指数模板版本（区域评价） |
| `run_id` / `result_id` / `calc_batch_id` | | 批次必填 | |
| `publish_status` | VARCHAR(16) | 是 | |
| `is_deleted` / 时间戳 | | 是 | |

> 分项列名以 QC11 会签后冻结；未冻结前以 `dimension_json` 为准，列仅演示。

---

### 5.6 `industry_chain_topn`

**用途**：跨对象 TopN（关键节点列表、热点资讯、重点企业）。属 v5「不进 DWD」的二次排序。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `industry_id` / `chain_id` | VARCHAR(64) | 否 | 列表所属对象 |
| `list_code` | VARCHAR(64) | 是 | `key_node` / `hot_news` / `key_enterprise` / … |
| `rank_no` | INT | 是 | |
| `item_type` | VARCHAR(32) | 是 | `node` / `news` / `enterprise` / … |
| `item_id` | VARCHAR(64) | 是 | |
| `item_name` | VARCHAR(512) | 否 | |
| `score` | DECIMAL(24,6) | 否 | |
| `metric_id` / `metric_version` | | 否 | 排序依据 |
| `stat_period_type` / `stat_period` | | 是 | |
| `payload_json` | JSON | 否 | 行扩展 |
| `run_id` / `result_id` / `calc_batch_id` | | 批次必填 | |
| `publish_status` | VARCHAR(16) | 是 | |
| `is_deleted` / 时间戳 | | 是 | |

**UK**：`(list_code, industry_id, chain_id, stat_period, rank_no, calc_batch_id)`（空键哨兵 `*`）

---

### 5.7 `industry_chain_conclusion`

**用途**：产品结论头（推荐/机遇/布局/方案标题）。大段正文在 narrative。  
**不**替代七键 Job Result 全文；可用于门户/深圳同步展示条。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `conclusion_id` | VARCHAR(64) | 是 | 业务 UK |
| `industry_id` / `chain_id` / `node_id` | VARCHAR(64) | 否 | |
| `conclusion_type` | VARCHAR(64) | 是 | `opportunity` / `layout` / `upgrade` / `bottleneck_solution` / `policy_advice` / … |
| `conclusion_code` | VARCHAR(64) | 否 | |
| `title` | VARCHAR(512) | 是 | |
| `priority_level` | VARCHAR(32) | 否 | 产品优先级 |
| `status` | VARCHAR(32) | 是 | `published`/`draft`/`retracted` |
| `source_result_snapshot_id` | VARCHAR(64) | 否 | 若由某次 Job 投影而来 |
| `run_id` / `result_id` / `metric_id` / `metric_version` | | 否 | |
| `calc_batch_id` | VARCHAR(64) | 是 | |
| `evidence_ref` | VARCHAR(512) | 否 | |
| `ext_json` | JSON | 否 | |
| `is_deleted` / 时间戳 | | 是 | |

---

### 5.8 `industry_chain_narrative`

**用途**：自然语言段落（方案正文、页面解读、报告摘要片段）。  
**禁止**同步 CMS「产业介绍 / 发展历程」。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `narrative_id` | VARCHAR(64) | 是 | UK |
| `conclusion_id` | VARCHAR(64) | 否 | |
| `industry_id` / `chain_id` / `node_id` | VARCHAR(64) | 否 | |
| `narrative_type` | VARCHAR(64) | 是 | `page_explain` / `report_summary` / `solution_body` / … |
| `locale` | VARCHAR(16) | 是 | 默认 `zh-CN` |
| `title` | VARCHAR(512) | 否 | |
| `body_text` | MEDIUMTEXT | 是 | |
| `body_format` | VARCHAR(16) | 是 | `plain` / `markdown` |
| `source_result_snapshot_id` | VARCHAR(64) | 否 | |
| `run_id` / `result_id` / `calc_batch_id` | | 批次必填 | |
| `is_deleted` / 时间戳 | | 是 | |

---

### 5.9 `industry_chain_graph_snapshot`

**用途**：专题全景 **已发布** 结构包元数据 + 内容引用（DEC：V1=S1a 不可变整图 JSON）。  
默认「当前状态」= 该 `chain_id` 最新 `publish_status=published` 且未 deprecated 的包。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `snapshot_id` | VARCHAR(64) | 是 | UK |
| `industry_id` | VARCHAR(64) | 否 | |
| `chain_id` | VARCHAR(64) | 是 | V1 禁止跨链对比 |
| `effective_at` | DATETIME | 是 | 业务「数据截至」；≡ 发布裁切时刻 |
| `generated_at` | DATETIME | 是 | 作业生成时间 |
| `source_release_id` | VARCHAR(64) | 否 | 发布作业号 |
| `layout_baseline_id` | VARCHAR(64) | 是 | 对比对齐基线（DEC R6） |
| `publish_status` | VARCHAR(16) | 是 | `published` / `deprecated` |
| `schema_version` | VARCHAR(32) | 是 | 包结构版本 |
| `node_count` / `edge_count` | INT | 否 | 可与 metric_fact 对账 |
| `payload_ref` | VARCHAR(512) | 否 | MinIO 路径 / 内容哈希 |
| `payload_json` | JSON | 否 | V1 小图可内嵌；大图必须 ref；**须含节点属性+边+布局，禁止只存 ID 回查 SCD1 当前节点** |
| `nebula_space` | VARCHAR(64) | 否 | 来源 space 名（非真源） |
| `calc_batch_id` | VARCHAR(64) | 是 | |
| `is_deleted` / 时间戳 | | 是 | |

---

### 5.10 `industry_chain_graph_diff`

**用途**：两发布快照间的演进条目；前端不算正式 diff。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `diff_id` | VARCHAR(64) | 是 | UK |
| `from_snapshot_id` | VARCHAR(64) | 是 | 基准 |
| `to_snapshot_id` | VARCHAR(64) | 是 | 对比 |
| `industry_id` / `chain_id` | VARCHAR(64) | 否/是 | |
| `change_type` | VARCHAR(32) | 是 | V1：`node_add` / `node_exit` / `edge_change`；可选 `entity_change`；**禁止**无结构字段时标 `tech_replace` |
| `subject_type` / `subject_id` | VARCHAR(64) | 是 | |
| `confirm_status` | VARCHAR(16) | 是 | `pending` / `confirmed`；无证据不得 confirmed |
| `evidence_refs` | JSON | 否 | |
| `detail_json` | JSON | 否 | |
| `calc_batch_id` | VARCHAR(64) | 是 | |
| `is_deleted` / 时间戳 | | 是 | |

**策略**：默认预计算相邻 published；非相邻可现场算或提示（DEC R5）。

---

## 6. `M_CHAIN_*` → 落表（60 条）

| 形态 | 落表 | metric_id |
|---|---|---|
| 标量卡片 | `metric_fact` | `MARKET_SIZE` `MARKET_GROWTH` `ENTERPRISE_COUNT` `ENTERPRISE_NEW_COUNT` `INSTITUTION_COUNT` `INVEST_TOTAL` `INVEST_COUNT` `GLOBAL_REGION_COUNT` `NATIONAL_REGION_COUNT` `NEWS_COUNT` `HOT_NEWS_COUNT` `SZ_ENTERPRISE_COUNT` `SZ_INSTITUTION_COUNT` `SZ_REGION_COUNT` `TOTAL_COUNT` `NODE_COUNT` `EDGE_COUNT` `SZ_COMPLETENESS` `SZ_KEY_NODE_COVERAGE` `DEVELOPMENT_MILESTONE_COUNT` `HOTSPOT_COUNT` `HOTSPOT_SCORE` `SZ_ADVANTAGE_SCORE` `SZ_ADVANTAGE_RANK` `CYCLE_STAGE` `STAGE_SCORE` `PHASE_DETERMINATION` `KEY_NODE_COUNT` `HIGH_VALUE_RATIO` `STRATEGIC_IMPORTANCE` `BOTTLENECK_COUNT` `BOTTLENECK_SEVERITY` `REGION_INDEX` `ENTERPRISE_POWER` `ACADEMIC_POWER` `SUPPORT_POWER` `SZ_PROBLEM_COUNT` `SZ_OPPORTUNITY_COUNT` `SZ_OPPORTUNITY_SCORE` `LAYOUT_RECOMMEND_COUNT` `LAYOUT_PRIORITY_SCORE` `COMPETITIVENESS_INDEX` `PRODUCT_COUNT` `PATENT_COUNT` `UPSTREAM_COUNT` `MIDSTREAM_COUNT` `DOWNSTREAM_COUNT` `COMPLETENESS_SCORE` `SUPPLY_RELATION_COUNT` `CONCENTRATION_INDEX` `TECH_MATURITY_SCORE` `SZ_ENTERPRISE_RATIO` `SZ_KEY_NODE_COUNT` `BREAK_RISK_COUNT` `POLICY_MATCH_SCORE` `ACADEMIC_COOP_SCORE` `INTERNATIONALIZATION_INDEX` `NEWS_SENTIMENT_RATIO` `TREND_INDEX` |
| 分布 | `metric_dist` | `BOTTLENECK_TYPE_DIST` |
| 时序 | `metric_series` | 凡需趋势的上述 metric（至少 `MARKET_SIZE` `NEWS_COUNT` `TREND_INDEX` 等） |
| 区域矩阵 | `region_scorecard` | `REGION_INDEX` 及四力分项投影 |
| 区域分布行 | `region_dist` | 支撑 `GLOBAL_REGION_COUNT` / `NATIONAL_REGION_COUNT` 下钻 |
| TopN | `topn` | 关键节点/热点资讯等列表（metric 作排序依据） |
| 结论类计数 | `conclusion` + 可选 `metric_fact` | `SZ_OPPORTUNITY_*` `LAYOUT_*` 等可双写：计数在 fact，条目在 conclusion |

未登记 cfg_metric 或 `metric_version` 不匹配 → **拒绝写入**。

缺口行为（Pending）不改表结构：由 `CHAIN-data-gap-catalog.yaml` / Wave0 mock 策略处理（投融资 ❌、部分 🔧/⚠️）。

---

## 7. 与 Job Snapshot / DWD / CMS 对照

| 内容 | 本稿 ADS | Job Snapshot | DWD | CMS |
|---|---|---|---|---|
| KPI 卡片 | ✅ | 可读作输入 | 原料 | — |
| 关键/周期/瓶颈正式结果包 | 可选投影 conclusion | ✅ 权威 | 原子分 | — |
| 区域指数正式结果 | 可选 scorecard 投影 | ✅ 权威 | 原子分 | — |
| 全景发布态 / 状态对比 | ✅ snapshot+diff | ❌ 禁止混用 | 边账本 | — |
| 产业介绍 / 历程 | ❌ | ❌ | ❌ | ✅ |
| 节点当前属性 | 包内物化（历史） | — | ✅ 当前版 | — |

---

## 8. 读写与发布

| 写 | 读 |
|---|---|
| Python 指标引擎 / 发布作业 / 模型后处理投影 | **Java 只读**；前端不直连 |

- API 默认过滤：`publish_status='published'` 且 `is_deleted=0`。  
- 全景：`GET snapshots?chain_id=` 只返回 published；diff 按 base/compare `snapshot_id`。  
- 是否单建全局 `industry_chain_ads_release` 指针表 → OPEN-CHAIN-ADS-V2-02（可先用各表 `publish_status` + `calc_batch_id`）。

---

## 9. 开放项

| ID | 内容 | Owner |
|---|---|---|
| OPEN-CHAIN-ADS-V2-01 | 本稿纸面多签（李伟 + 架构 Lead + 数据 Lead）；**S3 指针已切，不挡 stub** | 监管人 |
| OPEN-CHAIN-ADS-V2-02 | 是否单建 release 指针表 | architect |
| OPEN-CHAIN-ADS-V2-03 | scorecard 四力列名随 QC11 冻结 | 产品 / 算法 |
| OPEN-CHAIN-ADS-V2-04 | graph payload 内嵌阈值 vs 仅 MinIO | data |
| OPEN-CHAIN-ADS-V2-05 | Job 结果是否投影进 conclusion/scorecard 的自动规则 | architect + algorithm |
| OPEN-CHAIN-ADS-V2-06 | Demo `demo_gkxlumenx_ads` DDL + seeds | data |
| OPEN-CHAIN-ADS-V2-07 | ~~与 v1 收敛改指针~~ **已关闭（S3）**：现行 = 本稿；v1 对照 | — |

---

## 10. 后续

1. ~~会签选定真源 → 更新 `ads.md`~~ **已做（S3）**：现行指针 = 本稿；v1 仅对照。  
2. 输出 MySQL DDL → Demo/正式库（OPEN-CHAIN-ADS-V2-06）。  
3. Java 同步 API 与全景三只读接口按本稿映射；七键仍走 Analysis Job Runtime。  
4. `stores/mysql/ads.md` 细表 frontmatter 仍可 `draft`，不以 S1 流图会签冒充结构 approved；纸面多签补 OPEN-CHAIN-ADS-V2-01。

---

## 11. 修订

| 版本 | 日期 | 说明 |
|---|---|---|
| v2.0.0-draft | 2026-08-13 | 新建：按原型/Handoff/DEC/Runtime 反推；不修改 v1 原文 |
| v2.0.0 | 2026-08-13 | S3 收口：定为 `storage/CHAIN/stores/mysql/ads.md` 现行真源；v1 对照 |
