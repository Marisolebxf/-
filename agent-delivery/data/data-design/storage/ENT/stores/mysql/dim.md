# MySQL DIM · 企业维码表 / 字典

```yaml
---
doc_id: ENT-STORE-DIM
element: ENT
role: store-mysql
status: draft
version: "2026-08-12"
updated: "2026-08-12"
engine: mysql
s3_task: DATA-ENT-STORAGE-S3-L01
---
```

> 码表可落在 `gkxlumenx_dwd` / `gkxlumenx_cfg` 等；**结构共用**，Demo 用 `demo_*` 实例。  
> 细 DDL 外链现网/仓内 SQL，本文件只列清单。

## 表清单（已知 as-built）

| 表 | 库（常见） | 用途 | 指针 |
|---|---|---|---|
| `tag_dict` | `gkxlumenx_dwd` | 标签字典 | `demo-algo-ent-analysis/scripts/mysql/schema_mysql.sql` |
| `cfg_model_registry`（及 cfg_*） | `gkxlumenx_cfg` | 模型注册（含图 space 名等） | `scripts/schema_cfg.sql` · registry |
| 行政区划码表（如 `code_region` / region_scope） | 以现网为准 | 区域过滤 | 待核验后补路径；缺失则 OPEN |

## 读写

数据任务维护；服务/ETL 只读。禁止业务 API 在请求路径动态改字典语义。
