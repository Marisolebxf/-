# MySQL DWD · 服务机构（圈定 hang，不是机构主体）

```yaml
---
doc_id: SVC-STORE-DWD
element: SVC
role: store-mysql
status: draft
version: "2026-08-19"
updated: "2026-08-19"
engine: mysql
s3_task: DATA-SVC-STORAGE-S3-L02
---
```

> **库名**：正式 `gkxlumenx_dwd`（本总控零写）；Demo **`demo_gkxlumenx_dwd`**。  
> **映射**：[`../../etl/ods-to-dwd-mapping.md`](../../etl/ods-to-dwd-mapping.md)。  
> **DDL**：[`ddl-demo-empty.sql`](./ddl-demo-empty.sql)。  
> **status=draft**。流图会签 **不算** 本文件 approved。

机构**主体属性**权威在 ENT / ODS 贴源。本层只保留「哪些 `org_id` 被圈进服务机构池」以及图/事件 hang。

## 1. 边界

| 含 | 不含 |
|---|---|
| 圈定结果、图 hang、投融资事件 hang | ODS 主表全列；`svc_org_base`；`enterprise_*` |
| | ADS 指标/模型结果 → [`ads.md`](./ads.md) |

统一约定：主键 `id BIGINT AUTO_INCREMENT`；机构键 **`org_id` VARCHAR(64)**（与 ODS/ENT 同一键）。

## 2. 表清单

| # | 表（`demo_gkxlumenx_dwd`） | 用途 | 关键键 |
|---:|---|---|---|
| 1 | `svc_org_circle` | 圈定池：规则命中的服务机构 | `org_id` UK |
| 2 | `svc_org_graph_hang` | 投影到一张 G 的 hang 记录 | `org_id` + `node_id`；`space_name`=`demo_gkx_chain` |
| 3 | `svc_org_finance_event` | 投融资事件 hang（A3 原料；可 0 行） | `org_id` + `event_id` |

### 2.1 `svc_org_circle`

| 列 | 说明 |
|---|---|
| `org_id` | hang；禁止再存一套工商主数据 |
| `rule_version` | Demo 默认 `svc_rule_demo_kw_v1.1`（规则 A） |
| `hit_fields` | 命中的 ODS 列名 JSON |
| `service_type_candidate` | 六类候选，待核验 |
| `pending_client_confirm` | 默认 1（Q-SVC-010） |

### 2.2 `svc_org_graph_hang`

只记录 MySQL 侧 hang。Nebula 写入见 [`../nebula/graph-svc.md`](../nebula/graph-svc.md)。禁 `gkx_service`。

### 2.3 `svc_org_finance_event`

源：`demo_gkxlumenx_ods.dwd_org_financing_info` / `dwd_org_invest_info`。列名见 [`../../etl/ods-to-dwd-mapping.md`](../../etl/ods-to-dwd-mapping.md) §3。Q-SVC-006：可空表。`event_type` ∈ {`FINANCING`,`INVEST`}。

## 3. 读写（阶段 F）

| 写 | 读 |
|---|---|
| `demo-algo-ent-analysis`（F-SEED / F-ALGO；本单不跑） | 算法写 ADS / 图；**Java 禁扫 DWD** |

## 4. 禁止

- 38 列 `service_org` / `svc_org_base` 主体  
- 以 `gkx-mysql-raw` as-built 倒逼本层  
- 未评审标 `approved`  
- 本文件粘贴替代 [`ddl-demo-empty.sql`](./ddl-demo-empty.sql) 的第二套 DDL
