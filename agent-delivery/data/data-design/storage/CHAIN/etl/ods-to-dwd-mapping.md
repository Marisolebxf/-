# CHAIN · ODS 四表 → DWD v5 字段映射（Demo 模拟 GDF）

> **任务**：`DEMO-CHAIN-SIM-PROCESS-L01`  
> **ODS 列真源**：[`../sources/inventory.md`](../sources/inventory.md)  
> **DWD 列真源**：[`产业链-DWD表设计-业务需求驱动(v5).md`](../../../产业链/产业链-DWD表设计-业务需求驱动(v5).md) + Demo DDL `chainan/llm_ods/ddl.py`  
> **过程**：[`pipeline-demo-sim-process.md`](./pipeline-demo-sim-process.md)  
> **禁止**：新造 ODS/DWD 英文字段名；把本映射写成正式 GDF 已上线。  
> **正式 GDF Mapping（2026-09-01）**：`data-design/产业链/产业链域-ETL-Mapping明细-源表到DWD.md` + `GDF/派单包/产业链/GDF-CHAIN-WORKPACK-v1/`。本文只服务 Demo `gdf_sim`。

```yaml
---
doc_id: CHAIN-ETL-ODS-DWD-MAPPING
element: CHAIN
role: etl
status: draft
version: "2026-08-16"
updated: "2026-08-16"
task: DEMO-CHAIN-SIM-PROCESS-L01
---
```

图例：**直接** = ODS 列原值（可截断/类型转换）；**合成🧪** = Demo 规则生成，须 `source_system`/`ext` 可追溯；**n.a.** = 本 Demo 不写。  
公共治理列（`id`/`source_*`/`etl_batch_id`/`data_version`/`valid_*`/`is_deleted`/`created_time`/`updated_time`/`ext`）由 `_gov()` 系统生成，下表不逐列重复。

---

## 1. `dwd_industry_chain_info` → `industry_chain`（`level` ∈ {0,1}）

| ODS | DWD | 方式 |
|---|---|---|
| `industry_link_code` | `chain_id` / `chain_code` | 直接（Q053 INB） |
| `industry_code` | `industry_id`（L1）；L0 用 `industry_link_code` | 直接 |
| `industry_link_name`（空则 `industry_name`） | `chain_name` | 直接 |
| `parent_code` | `parent_chain_id`（L0=NULL） | 直接 |
| `level` | `chain_tier`=`L0`/`L1`；`chain_level`=0/1 | 直接派生 |
| — | `future_industry_flag` | 合成🧪：`industry_id` 前缀 `INB13`→1 |
| — | `status` | 合成🧪：`active` |
| `industry_name` / `parent_name` / `node_company_count` | — | **n.a.**（名称以 link 为准；企业数走 ADS） |
| — | `chain_short_name` / `chain_category` / `description` | **n.a.** |

`level`≥2 **不**进本表。

## 2. `dwd_industry_chain_info` → `industry_chain_node`（`level`≥2）

| ODS | DWD | 方式 |
|---|---|---|
| `industry_link_code` | `node_id` / `node_code` | 直接 |
| `parent_code` | `chain_id` | 直接（挂 L1） |
| `industry_link_name` | `node_name` / `description` | 直接 |
| `level` | `node_level` | 直接 |
| `industry_link_code` 末 2 位数字 | `sort_no`；`stage_code` upstream/midstream/downstream | 合成🧪 |
| — | `parent_node_id` | **n.a.**（现行写 NULL） |
| — | `node_type` / `importance_level` / `node_path` | **n.a.** |
| — | `status` | 合成🧪：`active` |
| `node_company_count` | — | **n.a.**（ADS） |

## 3. → `industry_chain_node_rel`

无 ODS 边表。同 `chain_id` 下按 `sort_no` 相邻 L2 生成 `relation_type=upstream`，`relation_id=node-rel:{chain}:{src}:{tgt}`。合成🧪。`confidence=0.8`。`relation_weight` / `evidence_ref` **n.a.**

## 4. `dwd_org_industry_tags` → `industry_chain_entity_rel`（企业）

| ODS | DWD | 方式 |
|---|---|---|
| `credit_code` | `entity_id`；`entity_type=enterprise` | 直接（语义交给并行叶，本叶不改） |
| `industry_link_code` | `node_id`；`chain_id`←`node[:9]` 或 `industry_code` | 直接+截取 |
| `company_name` | `ext.company_name` | 直接（进 JSON，非独立列） |
| — | `relation_type=belongs_to`；`role_type=participant`；`is_primary=1` | 合成🧪 |
| — | `relation_id=er:{node}:{credit}` | 合成🧪（≤64） |
| — | `ext.city` / `ext.district` | 合成🧪：`generate.credit_geo_map`（ODS **无** city 列） |

## 5. `dwd_org_industry_product_tags` → `industry_chain_entity_rel`（产品）

| ODS | DWD | 方式 |
|---|---|---|
| `credit_code` + `id` | `entity_id=p:{credit}:{id}` | 合成🧪（产品 UID 未冻） |
| `industry_link_code` | `node_id` / `chain_id` | 同 §4 |
| `product_name` / `product_top5` / `credit_code` | `ext.*` | 直接进 JSON |
| — | `entity_type=product`；`relation_type=produced_at` | 合成🧪 |
| `company_name` / `industry_name` | — | **n.a.**（可用 tags 侧名称） |

## 6. `dwd_industry_chain_news_info` → `industry_chain_news_event`

| ODS | DWD | 方式 |
|---|---|---|
| `id` | `source_news_id`；`event_id=news:{id}` | 直接+前缀 |
| `title` | `title`（截 500） | 直接 |
| `abstract` | `summary` | 直接 |
| `source` | `source_name` | 直接 |
| `publish_date` | `publish_time` | 直接；空则平台日 09:00 + `ext.publish_date_missing` |
| `industry_code` | `chain_id` | 直接（Demo 种子为 INB；live 供应方或为 IC* 需对照，见 Step2） |
| `industry_name` | — | **n.a.** |
| — | `news_type=market`；`news_dedup_key` | 合成🧪 fingerprint |
| — | `author_name` / `source_url` / `source_url_hash` / `node_id` / `region_code` | **n.a.** |

## 7. 合成🧪 投融资（无 ODS 四表列）

| DWD | 来源 | 方式 |
|---|---|---|
| `industry_chain_investment_event` | L0 × 6 条 mock | `source_system=mock`；`source_table=mock:synthetic_investment` |
| `industry_chain_investment_participant` | 同上 | `participation_amount` 规则值 |
| `event_entity_rel`（`event_kind=invest`） | tags `credit_code` 轮转 | `relation_type=financing_subject` |

正式路径（非本 Demo 四表）：`dwd_org_financing_info`（Q054 数据 0）。ADS 不写 `M_CHAIN_INVEST_COUNT`。

## 8. `event_entity_rel`（资讯向）

无 ODS「作者/发布企业」列。Demo：前 40 条 news × tags 轮转，`event_kind=news`，`relation_type=publisher`。合成🧪。

## 9. n.a. 五表 + 未写观测

| DWD | 为何 n.a. |
|---|---|
| `industry_chain_market_observation` | 平台市场规模=ADS←企业年报；外部观测 ODS 未到。`observation_id`/`metric_id`/`observation_value` 等 **不造** |
| `industry_chain_milestone_event` | 历程 CMS；四表无 `event_name`/`milestone_type`/`phase_*` |
| `industry_chain_event_metric_observation` | 无浏览/评论/转发 ODS；`map_event_metric_observation` 返回 `[]` |
| `industry_chain_extraction_result` | 不装 NLP 成功（`extraction_id`/`document_id`/`result_fingerprint` 不造） |
| `industry_chain_model_run` / `model_result_detail` | 不装模型成功（`run_id`/`result_id`/`severity_level` 不造） |

replace 时 `gdf_sim_gaps.apply_gaps` **TRUNCATE** 上表五张（防假结果残留）。
