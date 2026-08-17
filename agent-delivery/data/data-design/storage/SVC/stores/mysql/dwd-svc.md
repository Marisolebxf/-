# MySQL DWD · 服务机构项目明细（字段级 draft）

```yaml
---
doc_id: SVC-STORE-DWD
element: SVC
role: store-mysql
status: draft
version: "2026-08-17"
updated: "2026-08-17"
engine: mysql
s3_task: DATA-SVC-STORAGE-S3-L01
structure_task: DATA-SVC-STORAGE-DDL-L01
as_built_source: data-design/服务机构/服务机构域数据库设计(v1).md（对照 only）
---
```

> **本版范围**：**排除数据如何灌入 / 准入规则是否批准**；只定**表结构**（列、键、索引意图），便于后续联调。  
> **库**：正式 `gkxlumenx_dwd`；Demo `demo_gkxlumenx_dwd`。  
> **细表保持 `draft`**；圈定结果默认 `verification_status=pending_client_confirm`（结构字段预留，**不等于** Q-SVC-010 已关闭）。  
> **禁止**复制 ENT `enterprise_*` / ODS `dwd_org_base_info` 全量工商列。  
> DDL 快照（可选）：[`../../etl/demo_gkxlumenx_dwd_svc_tables.sql`](../../etl/demo_gkxlumenx_dwd_svc_tables.sql)（**不对正式库 APPLY**）。

## 0. 结构原则（排除数据影响）

| 原则 | 说明 |
|---|---|
| 身份回链 | 只用 `org_id` + `external_id`（及派生 `service_org_code`）回 ENT/ODS；详情不落本域 |
| 一企多标签 | 标签不挤在主表多列，走 `service_org_type_tag` |
| 规则可追溯 | `rule_version` / `tag_rule_version` 列预留；规则正文另轨 |
| 待核验可表达 | `verification_status` 枚举列；live 晋升是流程，不是缺列 |

## 1. 写读

| 写 | 读 |
|---|---|
| Python 圈定 ETL / 模拟 GDF | Python / algorithm；**Java 不扫 DWD** |

## 2. 表清单

| # | 表 | 一行语义 | 待核验语义 |
|---|---|---|---|
| 1 | `service_org` | 圈定结果名单 | 行级 `verification_status` |
| 2 | `service_org_type_tag` | 六类标签候选（一对多） | 行级可标 pending |
| 3 | `service_org_chain_rel` | 机构↔服务链环节 | 结构可定；环节码字典见 dim |
| 4 | `service_org_org_rel` | 机构↔机构（可选） | — |
| 5 | `service_org_financing` | 圈定池投融资切片 | — |

## 3. 字段级（draft）

> 类型为 MySQL 意图；落地可微调长度。`id` = BIGINT AUTO_INCREMENT PK。时间列统一 `DATETIME(3)`。

### 3.1 `service_org`

| 列 | 类型意图 | 空 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | N | 物理主键 |
| `service_org_code` | VARCHAR(64) | N | 业务键；优先 `external_id`，否则 `svc:{org_id}` |
| `org_id` | VARCHAR(64) | N | 回链 ODS/ENT |
| `external_id` | VARCHAR(64) | Y | 统一社会信用代码 |
| `name_cn` | VARCHAR(255) | Y | 列表展示冗余名 |
| `service_type_primary` | VARCHAR(32) | Y | 主类候选码（见 dim 六类）；可空 |
| `rule_version` | VARCHAR(32) | N | 圈定规则版本号 |
| `verification_status` | VARCHAR(32) | N | 默认 `pending_client_confirm` |
| `is_shenzhen` | TINYINT | Y | 0/1 |
| `province` | VARCHAR(64) | Y | 冗余切片 |
| `city` | VARCHAR(64) | Y | |
| `district` | VARCHAR(64) | Y | 深圳分布等 |
| `is_deleted` | TINYINT | N | 默认 0 |
| `batch_id` | VARCHAR(64) | Y | 灌数/圈定批次 |
| `created_at` | DATETIME(3) | N | |
| `updated_at` | DATETIME(3) | N | |

**键 / 索引**：`UNIQUE(service_org_code)`；`KEY(org_id)`；`KEY(external_id)`；`KEY(verification_status, is_deleted)`；`KEY(city, district)`。

### 3.2 `service_org_type_tag`

| 列 | 类型意图 | 空 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | N | |
| `service_org_code` | VARCHAR(64) | N | FK 逻辑 → `service_org` |
| `service_type` | VARCHAR(32) | N | 六类码（dim） |
| `tag_rule_version` | VARCHAR(32) | N | 打标规则版本 |
| `confidence` | DECIMAL(5,4) | Y | 可选 0~1 |
| `verification_status` | VARCHAR(32) | N | 默认 pending |
| `is_primary` | TINYINT | N | 是否与主表 primary 对齐；默认 0 |
| `created_at` | DATETIME(3) | N | |
| `updated_at` | DATETIME(3) | N | |

**键**：`UNIQUE(service_org_code, service_type, tag_rule_version)`；`KEY(service_type)`。

### 3.3 `service_org_chain_rel`

| 列 | 类型意图 | 空 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | N | |
| `service_org_code` | VARCHAR(64) | N | |
| `chain_stage_code` | VARCHAR(64) | N | 服务链环节码（**字典来源 = E7/ECO `CHAIN_STAGES`，见 dim**） |
| `chain_stage_name` | VARCHAR(128) | Y | 冗余名 |
| `rel_type` | VARCHAR(32) | N | 默认 `SERVES` |
| `weight` | DECIMAL(10,4) | Y | 可选 |
| `created_at` | DATETIME(3) | N | |

**键**：`UNIQUE(service_org_code, chain_stage_code, rel_type)`。  
**禁止**：复制 CHAIN `industry_chain_node` 全模型。

### 3.4 `service_org_org_rel`（可选）

| 列 | 类型意图 | 空 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | N | |
| `src_service_org_code` | VARCHAR(64) | N | |
| `dst_service_org_code` | VARCHAR(64) | Y | 对方若在池内 |
| `dst_org_id` | VARCHAR(64) | Y | 对方仅有企业键时 |
| `rel_type` | VARCHAR(32) | N | `COOP` / `INVEST` / … |
| `created_at` | DATETIME(3) | N | |

**键**：`KEY(src_service_org_code, rel_type)`。

### 3.5 `service_org_financing`

| 列 | 类型意图 | 空 | 说明 |
|---|---|---|---|
| `id` | BIGINT AI | N | |
| `service_org_code` | VARCHAR(64) | N | 必须已在圈定池 |
| `event_type` | VARCHAR(16) | N | `FINANCING` / `INVEST` |
| `amount` | DECIMAL(20,2) | Y | |
| `currency` | VARCHAR(8) | Y | |
| `completion_date` | DATE | Y | |
| `counterparty_name` | VARCHAR(255) | Y | |
| `source_ods_table` | VARCHAR(64) | Y | 溯源表名 |
| `source_ods_key` | VARCHAR(64) | Y | 溯源键 |
| `created_at` | DATETIME(3) | N | |

**键**：`KEY(service_org_code, completion_date)`；`KEY(event_type)`。

## 4. 与 ENT / 旧稿

| 对象 | 关系 |
|---|---|
| ENT `enterprise_*` | 只读键；禁止把工商全列拷入 `service_org` |
| ODS `dwd_org_*` | 约定贴源；角色不是本域 DWD |
| v1 38 字段稿 | **对照**；本版刻意瘦身为键+本域属性 |

## 5. 禁止

- 细表标 `approved` / live（须另开结构会签 + Q-SVC-010 决策后）  
- 本叶对正式 `gkxlumenx_dwd` 默认 APPLY  
- 用数据是否灌满否定本结构草案  
