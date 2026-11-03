# MySQL DWD · 服务机构（圈定 hang，不是机构主体）

```yaml
---
doc_id: SVC-STORE-DWD
element: SVC
role: store-mysql
status: draft
version: "2026-08-19"
updated: "2026-11-02"
engine: mysql
s3_task: DATA-SVC-STORAGE-S3-L02
---
```

> **库名**：正式 `gkxlumenx_dwd`（本总控零写；2026-11-02 同名三表已建且 0 行）；Demo **`demo_gkxlumenx_dwd`**（circle 43296、finance_event 15755、graph_hang 43296）。图库行数未闭合。见 [`../../02-asbuilt-process-chain.md`](../../02-asbuilt-process-chain.md)。  
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

### 2.4 建表语句

与 [`ddl-demo-empty.sql`](./ddl-demo-empty.sql) 同文。库名 `demo_gkxlumenx_dwd`。派单包只换库名。

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`svc_org_circle` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'hang ODS/ENT 同一机构键，不复制主体',
  `rule_version` VARCHAR(32) NOT NULL DEFAULT 'svc_rule_demo_kw_v1',
  `hit_fields` JSON NULL COMMENT '命中的 ODS 列名',
  `service_type_candidate` VARCHAR(32) NULL COMMENT '六类候选，待核验',
  `pending_client_confirm` TINYINT(1) NOT NULL DEFAULT 1,
  `etl_batch_id` VARCHAR(64) NULL,
  `ext` JSON NULL,
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_org_circle_org` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='SVC 圈定池 hang org_id；禁止平行 svc_org_base';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`svc_org_graph_hang` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `node_id` VARCHAR(80) NOT NULL COMMENT 'Nebula vid；与 org_id 对齐 hang',
  `space_name` VARCHAR(64) NOT NULL DEFAULT 'demo_gkx_chain',
  `tag_name` VARCHAR(32) NULL COMMENT '建议复用 institution；不新建 space',
  `etl_batch_id` VARCHAR(64) NULL,
  `ext` JSON NULL,
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_graph_hang` (`org_id`, `space_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='SVC hang 一张 G demo_gkx_chain；禁 gkx_service';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`svc_org_finance_event` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `event_id` VARCHAR(64) NOT NULL,
  `event_type` VARCHAR(16) NOT NULL COMMENT 'FINANCING / INVEST',
  `amount` DECIMAL(20,2) NULL,
  `event_date` DATE NULL,
  `etl_batch_id` VARCHAR(64) NULL,
  `ext` JSON NULL,
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_finance_event` (`org_id`, `event_id`, `event_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='投融资事件 hang；Q-SVC-006 允许 0 行';
```

## 3. 读写（阶段 F）

| 写 | 读 |
|---|---|
| `demo-algo-ent-analysis`（F-SEED / F-ALGO）。2026-11-02 demo 已有行；本文件仍不执行灌数 | 算法写 ADS / 图；**Java 禁扫 DWD**。专题 `lumen-topic-py` 现网会读 demo DWD/ADS，不写 |

## 4. 禁止

- 38 列 `service_org` / `svc_org_base` 主体  
- 以 `gkx-mysql-raw` as-built 倒逼本层  
- 未评审标 `approved`  
- 在 §2.4 与 [`ddl-demo-empty.sql`](./ddl-demo-empty.sql) 之外再写一套列
