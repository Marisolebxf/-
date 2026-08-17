# MySQL ADS · 服务机构契约面（字段级 draft）

```yaml
---
doc_id: SVC-STORE-ADS
element: SVC
role: store-mysql
status: draft
version: "2026-08-17"
updated: "2026-08-17"
engine: mysql
s3_task: DATA-SVC-STORAGE-S3-L01
structure_task: DATA-SVC-STORAGE-DDL-L01
---
```

> **排除数据口径是否拍板**；只定 **Java 只读契约表结构**。指标公式 / 权重另轨 METRIC-OPEN。  
> **库**：`gkxlumenx_ads` / Demo `demo_gkxlumenx_ads`。  
> **ADS 单轨决议（结构）**：本域以 **`svc_*` 十表** 为契约清单真源；**不**与平台 `ads_metric_timeseries` 双写。若平台通用表已存在同语义，由 ETL **投影写入 `svc_*`**，Java 只读 `svc_*`。

## 1. 写读

| 写 | 读 |
|---|---|
| Python / 指标引擎 / 模型后处理 | **Java 只读** |

## 2. 跨模块联动键（结构钉死）

| 契约 | 键 / 约定 |
|---|---|
| 下钻画像 / 门户进分析 | 查询参数 `org_id`（= DWD/ENT `org_id`）；卡片带 `service_org_code` |
| 对比篮 `service_org` 类型 | 入篮主键 = `service_org_code`；展示名 = `name_cn`；回链 `org_id` |
| 招引外部机构（可无库内圈定） | `svc_rec_ranking.candidate_key` 可非 `service_org_code`；`in_pool` 标记是否已在 DWD 池 |

## 3. 表与关键列（draft）

公共列约定：`id BIGINT AI`；`as_of_date DATE`；`batch_id VARCHAR(64)`；`created_at`/`updated_at DATETIME(3)`。

### 3.1 `svc_metric_fact`

| 列 | 说明 |
|---|---|
| `metric_id` | 如 `M_SVC_ORG_CNT` |
| `dim_json` | 切片 JSON（type/region/year…）或拆维表（后续可演化） |
| `value_num` | 数值 |
| `value_text` | 枚举/文本值 |
| `unit` | 单位 |

**键**：`UNIQUE(metric_id, as_of_date, batch_id, dim_json(191))`（落地可改为维列哈希）。

### 3.2 `svc_metric_series`

| 列 | 说明 |
|---|---|
| `metric_id` | |
| `period` | `YYYY` / `YYYY-MM` |
| `dim_json` | |
| `value_num` | |

**键**：`UNIQUE(metric_id, period, dim_json(191), batch_id)`。

### 3.3 `svc_metric_dist`

| 列 | 说明 |
|---|---|
| `metric_id` | 如六类分布 |
| `bucket_code` | 分档/类型码 |
| `bucket_name` | |
| `value_num` | 计数或占比分子 |
| `share` | 占比可选 |

### 3.4 `svc_region_dist`

| 列 | 说明 |
|---|---|
| `metric_id` | |
| `region_level` | country/province/city/district |
| `region_code` | |
| `region_name` | |
| `value_num` | |

### 3.5 `svc_org_profile_card`

| 列 | 说明 |
|---|---|
| `service_org_code` | UK |
| `org_id` | 下钻键 |
| `name_cn` | |
| `service_type_primary` | |
| `city` / `district` | |
| `verification_status` | 透出待核验 |
| `tech_score` | 可选冗余 |
| `ext_json` | 短扩展，禁塞全量工商 |

### 3.6 `svc_tech_power_score`

| 列 | 说明 |
|---|---|
| `service_org_code` | |
| `service_type` | 六类维度 |
| `score` | |
| `model_id` | |
| `model_version` | |

**键**：`UNIQUE(service_org_code, service_type, model_id, model_version, as_of_date)`。

### 3.7 `svc_chain_gap_score`

| 列 | 说明 |
|---|---|
| `chain_stage_code` | |
| `gap_type` | weak/blank/bottleneck… |
| `score` | |
| `model_version` | |

### 3.8 `svc_rec_ranking`

| 列 | 说明 |
|---|---|
| `list_type` | `ATTRACT` / `CULTIVATE` |
| `industry_direction` | 用户设定产业方向码 |
| `rank_no` | |
| `candidate_key` | 候选稳定键 |
| `service_org_code` | 可空（外部机构） |
| `org_id` | 可空 |
| `in_pool` | 0/1 是否在 DWD 圈定池 |
| `score` | |
| `reason_text` | |
| `model_version` | |

**键**：`UNIQUE(list_type, industry_direction, model_version, as_of_date, candidate_key)`。

### 3.9 `svc_narrative`

| 列 | 说明 |
|---|---|
| `scope_key` | 页面/对象键 |
| `title` | |
| `body` | 短结论；非 CMS 长文 |

### 3.10 `svc_graph_snapshot`

| 列 | 说明 |
|---|---|
| `snapshot_id` | UK |
| `publish_status` | draft/published |
| `payload_ref` | 对象存储键或内联限长 JSON 指针 |

## 4. 禁止

- Java 写 ADS；DWD 冒充 ADS  
- 与平台通用指标表双写双权威  
- 未结构会签标 `approved`  
