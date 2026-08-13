# CHAIN · stores 索引

```yaml
---
doc_id: CHAIN-STORES-INDEX
element: CHAIN
role: store-mysql
status: draft
version: "2026-08-13"
updated: 2026-08-13
s3_task: DATA-CHAIN-STORAGE-S3-L01
---
```

> **S3**：项目侧 as-built / 设计真源清单灌入；细表保持 **draft**。  
> **禁止**仅因 S1 流图会签标 `approved`。  
> **冲突裁决**：以本树叙述为准；DWD 以 v5 `industry_chain_*` 为准；旧 `DATA-CHAIN-db-design`（PG / 8 表）仅对照。

| 子目录 | 文档 | 状态 |
|---|---|---|
| [`mysql/`](./mysql/) | DWD / **ADS（必含）** / DIM | draft · S3 已灌清单 |
| [`elasticsearch/`](./elasticsearch/) | 检索索引 + sync | draft · S3 指针 |
| [`nebula/`](./nebula/) | 图谱 space / tag / edge | draft · S3 指针 |

库名：正式 `gkxlumenx_dwd` / `gkxlumenx_ads`；Demo `demo_gkxlumenx_dwd` / `_ads`（见 [`../etl/pipeline-demo-mock.md`](../etl/pipeline-demo-mock.md)）。引擎：**MySQL 8 only**（RDB）。
