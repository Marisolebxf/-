# 产业链 ADS 表设计（对齐 DWD v5）

| 属性 | 内容 |
|------|------|
| 文档编号 | DATA-CHAIN-ADS-v1 |
| 版本 | v1.0.0-draft |
| 状态 | **Draft**（待李伟 / 架构 / 数据 Lead 会签） |
| 作者 | agent:data-agent · 监管 human:李伟 |
| 创建日期 | 2026-08-13 |
| 任务 | `DATA-CHAIN-STORAGE-S3-L01` 补齐 · v5 后续步骤 #6 |
| 引擎 | **MySQL 8** · 库 `gkxlumenx_ads` / Demo `demo_gkxlumenx_ads` |
| 上游 DWD | [`产业链-DWD表设计-业务需求驱动(v5).md`](./产业链-DWD表设计-业务需求驱动(v5).md) |
| 指标 | `metrics/cfg_metric-CHAIN-seed.yaml`（`M_CHAIN_*`） |
| storage 入口 | [`storage/CHAIN/stores/mysql/ads.md`](../storage/CHAIN/stores/mysql/ads.md) |

---

## 0. 相对旧稿的裁决

| 旧稿 | 本设计 |
|---|---|
| `DATA-CHAIN-db-design.md` §5 十一张 `ads.chain_*`（PG） | **废作 ADS 真源**；仅历史对照 |
| S3 初灌沿用旧十一表名 | **以本文 8 张表为准** 重写 `stores/mysql/ads.md` |
| DWM | **不设**；链路仅 ODS → DWD → ADS（v5） |

本设计**不**从旧十一表「改名平移」，而是按 v5 §2.2 / §2.5 **按查询形态**切表。

---

## 1. 分层边界（摘自 v5，ADS 必守）

### 1.1 ADS 承载

- 企业数 / 机构数 / 人才数等**聚合**；
- **平台默认市场规模** `M_CHAIN_MARKET_SIZE`（Σ 链下企业年报营收，仅企业）；
- 区域分布、同比/环比/增长率/占比/排名；
- 页面卡片与趋势查询结构；
- 区域对比与综合评价结果；
- 机遇 / 布局 / 跃升等**产品结论**；
- 瓶颈解决方案、政策建议、报告摘要、页面解释（自然语言）；
- **图谱结构快照与演进 diff 查询面**（元数据 + 引用；边真源仍在 DWD `*_rel`）。

### 1.2 不进 ADS

| 内容 | 去向 |
|---|---|
| 链/节点/关系明细 | DWD `industry_chain_*` |
| 模型单次原子评分/标签 | DWD `industry_chain_model_result_detail` |
| 产业介绍 / 发展历程正文 | **CMS** |
| 永久图谱边 | Nebula（由 DWD 投影）；禁止 ADS 另建永久边表 |

### 1.3 追溯铁律（v5 §2.5）

凡来自模型二次加工的 ADS 行，必须能回链：

`calc_batch_id` · `run_id` · `result_id`（可空）· `metric_id` · `metric_version`

---

## 2. 命名与公共列

- 库已是 `gkxlumenx_ads`，表名**不**加 `ads_` 前缀；统一 `industry_chain_*`（与 DWD 同域前缀，靠库名分层）。
- 物理主键：`id BIGINT AUTO_INCREMENT`。
- 业务对象键：与 DWD/Q053 对齐 — `industry_id` / `chain_id` / `node_id`（INB）。
- 公共治理（建议）：`calc_batch_id`、`data_version`、`created_time`、`updated_time`、`is_deleted`（默认查询 `is_deleted=0`）。

### 2.1 对象粒度约定

| `object_type` | `object_id` 含义 |
|---|---|
| `industry` | L0 `industry_id` |
| `chain` | `chain_id` |
| `node` | `node_id`（常配 `chain_id`） |
| `region` | 区划码（配 `industry_id`/`chain_id`） |
| `event` | 资讯/投融资等事件 id |
| `relation` | DWD 关系 id（少用于 ADS） |

---

## 3. 表总览（8 张）

| # | 表名 | 一句话 | 主要消费 |
|---|---|---|---|
| 1 | `industry_chain_metric_fact` | 指标快照事实（卡片 KPI / 排名 / 占比） | 总览、深圳切片、统计条 |
| 2 | `industry_chain_metric_series` | 指标时序点（趋势图） | 趋势、同比序列 |
| 3 | `industry_chain_region_scorecard` | 区域对比 / 综合评价行 | 区域评价页 |
| 4 | `industry_chain_topn` | TopN 列表行 | 排行、重点企业/节点 |
| 5 | `industry_chain_conclusion` | 产品化结论头（推荐/方案类） | 诊断、跃升、布局 |
| 6 | `industry_chain_narrative` | 长文本解释 / 报告摘要 | 详情解读、报告 |
| 7 | `industry_chain_graph_snapshot` | 图谱结构快照元数据 | 全景图只读快照 |
| 8 | `industry_chain_graph_diff` | 演进 diff 条目 | 全景演进 |

> 旧十一表能力映射见 §6；**禁止**再平行维护 `chain_overview` 等第二套契约。

---

## 4. 表结构（字段级）

### 4.1 `industry_chain_metric_fact`

**用途**：某一对象、某一指标、某一统计期的**当前/批次快照**（含可选同比环比、排名）。覆盖绝大多数 `M_CHAIN_*` 卡片值。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | 物理主键 |
| `industry_id` | VARCHAR(64) | 否 | L0；门户选择器常用 |
| `chain_id` | VARCHAR(64) | 否 | 子链；与 industry 至少填一 |
| `node_id` | VARCHAR(64) | 否 | 节点级指标时用 |
| `object_type` | VARCHAR(32) | 是 | 见 §2.1 |
| `object_id` | VARCHAR(64) | 是 | |
| `region_code` | VARCHAR(32) | 否 | `ALL`/国/省/市/区；默认 `ALL` |
| `metric_id` | VARCHAR(64) | 是 | `M_CHAIN_*`，须已在 cfg_metric |
| `metric_version` | VARCHAR(32) | 是 | 口径版本 |
| `stat_period_type` | VARCHAR(16) | 是 | `day`/`month`/`quarter`/`year`/`snapshot` |
| `stat_period` | VARCHAR(32) | 是 | 如 `2025` / `2025-Q1` / `2025-08-13` |
| `metric_value` | DECIMAL(24,6) | 否 | 主值 |
| `value_unit` | VARCHAR(32) | 否 | 展示单位提示（换算可在 API） |
| `yoy` | DECIMAL(12,6) | 否 | 同比 |
| `mom` | DECIMAL(12,6) | 否 | 环比 |
| `ratio` | DECIMAL(12,6) | 否 | 占比 |
| `rank_no` | INT | 否 | 排名 |
| `rank_total` | INT | 否 | 排名分母 |
| `run_id` | VARCHAR(64) | 否 | 模型派生时必填 |
| `result_id` | VARCHAR(64) | 否 | 回链 DWD 原子结果 |
| `calc_batch_id` | VARCHAR(64) | 是 | |
| `ext_json` | JSON | 否 | 少量扩展，禁止塞页面整包 |
| `is_deleted` | SMALLINT | 是 | 默认 0 |
| `created_time` / `updated_time` | DATETIME | 是 | |

**唯一键（建议）**：`UK(object_type, object_id, region_code, metric_id, metric_version, stat_period_type, stat_period, calc_batch_id)`  
**策略**：同业务键新批次 Upsert 或按 batch 追加后由发布指针切换（发布策略 OPEN）。

**典型 metric**：`M_CHAIN_ENTERPRISE_COUNT`、`M_CHAIN_MARKET_SIZE`、`M_CHAIN_NODE_COUNT`、`M_CHAIN_SZ_*`、`M_CHAIN_NEWS_COUNT` 等。

---

### 4.2 `industry_chain_metric_series`

**用途**：趋势图点列；与 fact 分离，避免大序列撑爆卡片行。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `industry_id` / `chain_id` / `node_id` | VARCHAR(64) | 否 | 同 fact |
| `object_type` / `object_id` | VARCHAR(64) | 是 | |
| `region_code` | VARCHAR(32) | 否 | 默认 `ALL` |
| `metric_id` / `metric_version` | VARCHAR(64)/32 | 是 | |
| `stat_period_type` | VARCHAR(16) | 是 | |
| `stat_period` | VARCHAR(32) | 是 | 序列上的一个点 |
| `metric_value` | DECIMAL(24,6) | 否 | |
| `yoy` / `mom` | DECIMAL(12,6) | 否 | |
| `calc_batch_id` | VARCHAR(64) | 是 | |
| `run_id` / `result_id` | VARCHAR(64) | 否 | |
| `is_deleted` | SMALLINT | 是 | |
| `created_time` / `updated_time` | DATETIME | 是 | |

**唯一键**：`UK(object_type, object_id, region_code, metric_id, metric_version, stat_period_type, stat_period, calc_batch_id)`

---

### 4.3 `industry_chain_region_scorecard`

**用途**：区域对比 /「四力」或综合评价一行一区域（可含多 score 列或 JSON 分项）。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `industry_id` / `chain_id` | VARCHAR(64) | 否 | 至少一 |
| `region_code` | VARCHAR(32) | 是 | |
| `region_name` | VARCHAR(128) | 否 | 冗余展示名 |
| `stat_period_type` / `stat_period` | VARCHAR | 是 | |
| `score_total` | DECIMAL(12,6) | 否 | 综合分 |
| `score_enterprise` | DECIMAL(12,6) | 否 | 分项示例 |
| `score_innovation` | DECIMAL(12,6) | 否 | |
| `score_capital` | DECIMAL(12,6) | 否 | |
| `score_support` | DECIMAL(12,6) | 否 | |
| `rank_no` | INT | 否 | |
| `dimension_json` | JSON | 否 | 扩展分项，避免频繁加列 |
| `metric_id` | VARCHAR(64) | 否 | 主综合分对应 metric（如有） |
| `metric_version` | VARCHAR(32) | 否 | |
| `run_id` / `result_id` / `calc_batch_id` | VARCHAR(64) | 批次必填 | |
| `is_deleted` / 时间戳 | | 是 | |

分项枚举与模型卡对齐前，`dimension_json` 为过渡；定稿后可升正式列（OPEN）。

---

### 4.4 `industry_chain_topn`

**用途**：跨对象 TopN（重点企业、关键节点、热点资讯等），属 v5 明确不进 DWD 的二次排序。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `industry_id` / `chain_id` | VARCHAR(64) | 否 | 列表所属分析对象 |
| `list_code` | VARCHAR(64) | 是 | 如 `key_enterprise` / `key_node` / `hot_news` |
| `rank_no` | INT | 是 | |
| `item_type` | VARCHAR(32) | 是 | `enterprise` / `node` / `news` / … |
| `item_id` | VARCHAR(64) | 是 | 平台主体 id 或事件 id |
| `item_name` | VARCHAR(512) | 否 | 展示冗余 |
| `score` | DECIMAL(24,6) | 否 | |
| `metric_id` / `metric_version` | VARCHAR | 否 | 排序依据指标 |
| `stat_period_type` / `stat_period` | VARCHAR | 是 | |
| `payload_json` | JSON | 否 | 列表行扩展字段 |
| `run_id` / `result_id` / `calc_batch_id` | | 批次必填 | |
| `is_deleted` / 时间戳 | | 是 | |

**唯一键**：`UK(list_code, industry_id, chain_id, stat_period, rank_no, calc_batch_id)`（空键用哨兵 `*`）。

---

### 4.5 `industry_chain_conclusion`

**用途**：产品化结论头：「推荐/不推荐」「重点招商」「跃升路径条目」等；**不含**大段正文（正文在 narrative）。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `conclusion_id` | VARCHAR(64) | 是 | 业务键 UK |
| `industry_id` / `chain_id` / `node_id` | VARCHAR(64) | 否 | |
| `conclusion_type` | VARCHAR(64) | 是 | `opportunity` / `layout` / `upgrade` / `bottleneck_solution` / `policy_advice` / … |
| `conclusion_code` | VARCHAR(64) | 否 | 配置库编码 |
| `title` | VARCHAR(512) | 是 | 短标题 |
| `priority_level` | VARCHAR(32) | 否 | 产品优先级（≠ DWD 原子 priority 直出） |
| `status` | VARCHAR(32) | 是 | `published` / `draft` / `retracted` |
| `run_id` / `result_id` | VARCHAR(64) | 否 | 须能追溯原子结果 |
| `metric_id` / `metric_version` | VARCHAR | 否 | |
| `calc_batch_id` | VARCHAR(64) | 是 | |
| `evidence_ref` | VARCHAR(512) | 否 | |
| `ext_json` | JSON | 否 | |
| `is_deleted` / 时间戳 | | 是 | |

---

### 4.6 `industry_chain_narrative`

**用途**：自然语言段落、报告摘要、页面解释；通过 `conclusion_id` 或直接挂对象。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `narrative_id` | VARCHAR(64) | 是 | UK |
| `conclusion_id` | VARCHAR(64) | 否 | FK 逻辑关联 conclusion |
| `industry_id` / `chain_id` / `node_id` | VARCHAR(64) | 否 | |
| `narrative_type` | VARCHAR(64) | 是 | `page_explain` / `report_summary` / `solution_body` / … |
| `locale` | VARCHAR(16) | 是 | 默认 `zh-CN` |
| `title` | VARCHAR(512) | 否 | |
| `body_text` | MEDIUMTEXT | 是 | |
| `body_format` | VARCHAR(16) | 是 | `plain` / `markdown` |
| `run_id` / `result_id` / `calc_batch_id` | | 批次必填 | |
| `is_deleted` / 时间戳 | | 是 | |

**禁止**把 CMS 产业介绍/历程正文同步进本表。

---

### 4.7 `industry_chain_graph_snapshot`

**用途**：某一分析对象在某时刻的**图结构只读快照**元数据（Q062）；nodes/edges **引用** MinIO/对象存储或压缩 JSON，**不**作为永久边真源。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `snapshot_id` | VARCHAR(64) | 是 | UK |
| `industry_id` / `chain_id` | VARCHAR(64) | 否 | 至少一 |
| `valid_at` | DATETIME | 是 | 快照业务时间 |
| `node_count` / `edge_count` | INT | 否 | 冗余计数（可与 metric_fact 对账） |
| `nodes_ref` | VARCHAR(512) | 否 | 对象存储路径或内容哈希 |
| `edges_ref` | VARCHAR(512) | 否 | |
| `payload_json` | JSON | 否 | 小图可内嵌；大图必须走 ref |
| `source_space` | VARCHAR(64) | 否 | Nebula space 名 |
| `calc_batch_id` | VARCHAR(64) | 是 | |
| `run_id` | VARCHAR(64) | 否 | |
| `is_deleted` / 时间戳 | | 是 | |

DWD `node_rel` / `entity_rel` 仍为关系权威；本表只服务「当时看见的图」。

---

### 4.8 `industry_chain_graph_diff`

**用途**：两次快照间的演进条目（新增/退出/关系变化等）。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | 是 | |
| `diff_id` | VARCHAR(64) | 是 | UK |
| `from_snapshot_id` | VARCHAR(64) | 是 | |
| `to_snapshot_id` | VARCHAR(64) | 是 | |
| `industry_id` / `chain_id` | VARCHAR(64) | 否 | |
| `change_type` | VARCHAR(32) | 是 | `node_add` / `node_exit` / `edge_change` / `entity_change` / … |
| `subject_type` / `subject_id` | VARCHAR(64) | 是 | |
| `detail_json` | JSON | 否 | |
| `calc_batch_id` | VARCHAR(64) | 是 | |
| `is_deleted` / 时间戳 | | 是 | |

---

## 5. `M_CHAIN_*` → 表落点（摘要）

| 形态 | 落表 | 示例 metric |
|---|---|---|
| 单值卡片 / 排名 / 占比 | `metric_fact` | ENTERPRISE_COUNT、MARKET_SIZE、SZ_*、NODE_COUNT |
| 时间序列 | `metric_series` | MARKET_SIZE 逐年、NEWS_COUNT 月序 |
| 区域评价矩阵 | `region_scorecard` | REGION_INDEX、竞争力分项 |
| TopN | `topn` | 关键节点列表、热点资讯 |
| 产品结论 | `conclusion` + 可选 `narrative` | 机遇/布局/瓶颈方案 |
| 图快照 / 演进 | `graph_snapshot` / `graph_diff` | NODE_COUNT/EDGE_COUNT 可与 fact 对账 |

未在 cfg_metric 登记或 `metric_version` 不匹配的写入必须拒绝（同 v5 DWD 门禁精神）。

---

## 6. 旧十一表 → 新八表

| 旧 `chain_*` | 新落点 |
|---|---|
| `chain_overview` | `metric_fact`（多 metric 行） |
| `chain_panorama` | `graph_snapshot` + `metric_fact`(NODE/EDGE_COUNT) |
| `chain_cycle` / `stage` | `metric_fact`（CYCLE_STAGE 等）± `conclusion` |
| `chain_region_index` | `region_scorecard` |
| `chain_key_node` | `metric_fact` + `topn` |
| `chain_bottleneck` | `conclusion` + `narrative`（原子分仍在 DWD model_result） |
| `chain_shenzhen` | `metric_fact`（SZ_*） |
| `chain_market` | `metric_fact` / `metric_series`（MARKET_SIZE/GROWTH） |
| `chain_investment` | `metric_fact`（INVEST_*） |
| `chain_news_stat` | `metric_fact` / `metric_series` |
| `chain_competitiveness` | `region_scorecard` 或 `metric_fact` |

---

## 7. 读写与发布

| 写 | 读 |
|---|---|
| Python（模拟 GDF / 指标引擎 / 模型后处理） | **Java 只读**；前端不直连 |

建议：`calc_batch_id` 计算完成后写 `published` 指针表或配置（OPEN：是否单独立 `industry_chain_ads_release`）；默认 API 只读已发布批次。

---

## 8. 开放项

| ID | 内容 | Owner |
|---|---|---|
| OPEN-CHAIN-ADS-01 | 本设计会签（李伟 + 架构 + 数据 Lead） | 监管人 |
| OPEN-CHAIN-ADS-02 | 发布指针表是否单建 | architect |
| OPEN-CHAIN-ADS-03 | region_scorecard 分项枚举冻结 | 算法 / 产品 |
| OPEN-CHAIN-ADS-04 | graph payload 内嵌阈值 vs 仅 MinIO ref | data |
| OPEN-CHAIN-ADS-05 | Demo 库按本文 DDL 建表 | data（联调触发） |
| OPEN-CHAIN-ADS-06 | 旧 innov/PG `chain_*` 下线计划 | data / devops |

---

## 9. 后续

1. 会签通过后：输出 MySQL DDL 脚本 → `demo_gkxlumenx_ads` / 正式库。  
2. 更新 Java API 契约与 metric 投影，**停止**引用旧十一表。  
3. stores 细表评审通过前保持 `draft`（≠ 流图会签 approved）。
