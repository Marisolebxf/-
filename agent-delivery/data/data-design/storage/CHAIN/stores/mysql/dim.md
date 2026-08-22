# MySQL DIM · 产业链码表 / 对照

```yaml
---
doc_id: CHAIN-STORE-DIM
element: CHAIN
role: store-mysql
status: draft
version: "2026-08-17"
updated: "2026-08-17"
engine: mysql
s3_task: DATA-CHAIN-STORAGE-S3-L01
---
```

> 码表可落 `gkxlumenx_dwd` / `gkxlumenx_cfg` / `demo_*`；**结构共用**。本文件只列清单。

## 表清单（初填）

| 表 / 对象 | 库（常见） | 用途 | 指针 |
|---|---|---|---|
| `cfg_metric` / lineage | `gkxlumenx_cfg` | D9 八件套 · `M_CHAIN_*` | `metrics/registry/cfg_metric-CHAIN-seed.yaml` |
| INB ↔ 国标/别名对照（若落地） | 待定 | API 展示国标时读对照；DWD 主键仍 INB | `DEC-CHAIN-Q053-CODE-NORMALIZATION-20260807.md` |
| 资讯 `IC*` ↔ `INB*` 对照 | 待定 | 资讯挂链（OPEN-CHAIN-DIFF-03） | `sources/md-extract-vs-live-ods-diff.md` |
| 行政区划码表 | 以平台 DIM 为准 | 区域切片 | 与 ENT `dim.md` 共用；路径待核验 |
| `industry_cluster` | `gkxlumenx_dim`（Demo：`demo_gkxlumenx_dim`） | 固定 15 个产业集群（展示目录） | [`dim-industry-cluster.md`](./dim-industry-cluster.md) · DDL `data/ddl/gkxlumenx_dim_industry_cluster.sql` |
| `industry_cluster_map` | 同上 | 集群 1:N → L0 `industry_id` | 同上 |

## 读写

数据任务维护；服务/ETL 只读。禁止业务 API 在请求路径动态改字典语义。

例外：`industry_cluster` / `industry_cluster_map` 由维护页经 Java 管理接口改映射（领导关注点会变）；**查询接口只读**。不进 `gkxlumenx_cfg`。细则见 [`dim-industry-cluster.md`](./dim-industry-cluster.md)。
