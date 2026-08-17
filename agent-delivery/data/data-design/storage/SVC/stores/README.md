# SVC · stores 索引

```yaml
---
doc_id: SVC-STORES-INDEX
element: SVC
role: store-mysql
status: draft
version: "2026-08-14"
updated: 2026-08-14
s3_task: DATA-SVC-STORAGE-S3-L01
---
```

> **S3 已灌清单**（`DATA-SVC-STORAGE-S3-L01`）。细表保持 **draft**。  
> **禁止**仅因 S1 流图会签标 `approved`。  
> **禁止**在此复制 ENT 机构主表 DDL。  
> **冲突裁决**：以本树叙述为准；旧 `服务机构域数据库设计(v1).md` 仅对照（S4 stub）。  
> **Q-SVC-010**：圈定结果相关表 **不得**标 live 契约。

| 子目录 | 文档 | 状态 |
|---|---|---|
| [`mysql/`](./mysql/) | [`dwd-svc.md`](./mysql/dwd-svc.md) · [`ads.md`](./mysql/ads.md)（**必含**）· [`dim.md`](./mysql/dim.md) | draft · S3 清单 |
| [`elasticsearch/`](./elasticsearch/) | [`index-svc.md`](./elasticsearch/index-svc.md) · [`sync.md`](./elasticsearch/sync.md) | draft |
| [`nebula/`](./nebula/) | [`graph-svc.md`](./nebula/graph-svc.md) | draft；禁复制 CHAIN 模型 |

### 共用 vs 本域（一句话）

| | |
|---|---|
| **ENT 共用** | 机构主体键与属性权威在 ENT / 约定 ODS；本域只存 `org_id`/`external_id` 回链 |
| **本域独有** | `service_org*` 圈定与关系、本域 ADS `svc_*`、ES `gkx_svc_*`、Nebula `gkx_svc` |

库名：正式 `gkxlumenx_dwd` / `gkxlumenx_ads`；Demo `demo_gkxlumenx_dwd` / `_ads`（见 [`../etl/pipeline-demo-mock.md`](../etl/pipeline-demo-mock.md)）。引擎：**MySQL 8 only**（RDB）。
