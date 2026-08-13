# MySQL DIM · 产业链码表 / 对照

```yaml
---
doc_id: CHAIN-STORE-DIM
element: CHAIN
role: store-mysql
status: draft
version: "2026-08-13"
updated: "2026-08-13"
engine: mysql
s3_task: DATA-CHAIN-STORAGE-S3-L01
---
```

> 码表可落 `gkxlumenx_dwd` / `gkxlumenx_cfg` / `demo_*`；**结构共用**。本文件只列清单。

## 表清单（初填）

| 表 / 对象 | 库（常见） | 用途 | 指针 |
|---|---|---|---|
| `cfg_metric` / lineage | `gkxlumenx_cfg` | D9 八件套 · `M_CHAIN_*` | `metrics/cfg_metric-CHAIN-seed.yaml` |
| INB ↔ 国标/别名对照（若落地） | 待定 | API 展示国标时读对照；DWD 主键仍 INB | `DEC-CHAIN-Q053-CODE-NORMALIZATION-20260807.md` |
| 资讯 `IC*` ↔ `INB*` 对照 | 待定 | 资讯挂链（OPEN-CHAIN-DIFF-03） | `sources/md-extract-vs-live-ods-diff.md` |
| 行政区划码表 | 以平台 DIM 为准 | 区域切片 | 与 ENT `dim.md` 共用；路径待核验 |

## 读写

数据任务维护；服务/ETL 只读。禁止业务 API 在请求路径动态改字典语义。
