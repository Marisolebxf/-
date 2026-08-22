# MySQL DIM · 服务机构码表 / 对照

```yaml
---
doc_id: SVC-STORE-DIM
element: SVC
role: store-mysql
status: draft
version: "2026-08-19"
updated: "2026-08-19"
engine: mysql
s3_task: DATA-SVC-STORAGE-S3-L02
---
```

> 本文件只列清单。**不**为本域新建行政区划码表（与 ENT 共用）。  
> 六类枚举可落注释 / CHECK，不强制单独物理表（ponytail lite）。

## 表 / 对象

| 对象 | 库（常见） | 用途 | 指针 |
|---|---|---|---|
| `cfg_metric` / lineage | `gkxlumenx_cfg` | D9 八件套 · `M_SVC_*` | `metrics/registry/metric-readiness-matrix-SVC.yaml`（过渡）；正式 seed 待 METRIC-OPEN |
| 六类 `service_type` | 枚举，非平行主体 | 1 FINANCE / 2 IP / 3 HR / 4 MKT / 5 CONSULT / 6 INNOV | 候选写入 `svc_org_circle.service_type_candidate`；词表 [`../../seeds/svc_rule_demo_kw_v1.md`](../../seeds/svc_rule_demo_kw_v1.md)；待核验 |
| 行政区划 | 平台 / ENT DIM | A2/A5/A6 切片 | ODS `province`/`city`/`area`；深圳分布用 `area` |

## 读写

数据任务维护；F-SEED 只读枚举。禁止业务 API 在请求路径改词典语义。Q-SVC-010 关键词词典属规则配置，不是 DIM 物理表。
