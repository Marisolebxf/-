# POLICY · stores 索引

```yaml
---
doc_id: POLICY-STORES-INDEX
element: POLICY
role: store-mysql
status: draft
version: "2026-08-21"
updated: 2026-08-21
s3_task: DATA-POLICY-STORAGE-S3-L01
---
```

> **S3**：项目侧细表清单。一律 **draft**。禁止仅因 S1 流图会签标 `approved`。  
> **冲突**：以本树为准。贴源结构 [`../sources/ods-ddl.md`](../sources/ods-ddl.md)。旧 v1 仅历史（含独立 `gkx_policy` DDL）。

| 子目录 | 文档 | 状态 |
|---|---|---|
| [`mysql/dwd.md`](./mysql/dwd.md) | `policy_base_info` + `policy_industry_rel`（产业关联，逻辑删除） | draft |
| [`mysql/ads.md`](./mysql/ads.md) | ADS **16 张**：指标 9 + 图镜像 2 + NER 1 + 文本 3 + `policy_industry_rel` 镜像 | draft |
| [`nebula/`](./nebula.md) | hang **`demo_gkx_chain` only** | draft |
| [`elasticsearch/`](./elasticsearch.md) | 本管线不施工独立索引 | draft 指针 |
| 窗口对照 | [`../windows/display-ds10-12.md`](../windows/display-ds10-12.md) | draft |

库名：Demo `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`。引擎：**MySQL 8 only**。禁止 `dwd.` / `ads.` PG schema 叙述当建库名。
