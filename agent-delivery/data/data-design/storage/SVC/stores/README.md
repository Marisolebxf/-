# SVC · stores 索引

```yaml
---
doc_id: SVC-STORES-INDEX
element: SVC
role: store-mysql
status: draft
version: "2026-08-19"
updated: 2026-08-19
s3_task: DATA-SVC-STORAGE-S3-L02
---
```

> **S3**：项目侧细表清单 + Demo 空表 CREATE；一律 **draft**。  
> **禁止**仅因 S1 流图会签标 `approved`。  
> **冲突裁决**：以本树为准。旧 `服务机构域数据库设计(v1).md`（`gkx_dwd.service_org` / `gkx_service`）仅历史对照。

| 子目录 | 文档 | 状态 |
|---|---|---|
| [`mysql/`](./mysql/) | DWD 圈定 hang / **ADS（必含 A1–A6 + 十模型）** / DIM / 空表 DDL | draft |
| [`elasticsearch/`](./elasticsearch/) | 本总控不施工独立索引；不挡 F | draft 指针 |
| [`nebula/`](./nebula/) | hang **`demo_gkx_chain` only** | draft |

库名：正式 `gkxlumenx_dwd` / `gkxlumenx_ads`（本总控**零写入**）；Demo `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`。引擎：**MySQL 8 only**。
