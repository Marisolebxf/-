# Elasticsearch · 服务机构（指针 · 不挡 F）

```yaml
---
doc_id: SVC-STORE-ES
element: SVC
role: store-elasticsearch
status: draft
version: "2026-08-19"
updated: "2026-11-02"
engine: elasticsearch
s3_task: DATA-SVC-STORAGE-S3-L02
---
```

> **本总控（阶段 F）不施工独立 SVC 索引。** 底座退出门认 50100 + Demo ADS/图，不认 ES。  
> OPEN-SVC-FLOW-04（同步失败 SLA）保持开放，不阻塞本单。

| 项 | 约定 |
|---|---|
| 阶段 F | 不新建 `svc_*` 索引；不挡 F-SEED / F-ALGO |
| 阶段 P（未授权） | 若检索需要，跟 ENT 企业索引策略对齐，另单 |
| 权威 | 指标以 ADS 为准；ES 失败不得冒充灌完 |

禁止前端直连 ES。禁止用 ES 替代 `svc_org_circle` / ADS 契约表。

## 2026-11-02 现网（阶段 F「不建索引」已被后来的同步作业打破）

上面的阶段 F 约定仍然是当时的退出门：底座不认 ES。现网已经有索引，不能再写成「没有 SVC 索引」：

| 项 | 2026-11-02 |
|---|---|
| 作业 | `lumen-etl-es-py` 的 `service_org`。`POST /internal/etl/indexes/svc-org` 后 `POST /internal/etl/svc-org`。仓库里未见定时任务 |
| 别名 | `gkx_svc_org` → `gkx_svc_org_v1`，文档 43296 |
| 水位 | `gkxlumenx_cfg.es_sync_watermark`，`module_name=svc_org_card`，仅一条，`last_sync_time=2026-10-20 14:23:49`，`last_sync_count=43296` |
| 源 | 配置默认 `demo_gkxlumenx_*` 的 card / circle / `svc_tech_power_score`，以及 `dwd_org_industry_tags`、`enterprise_patent_history`。没有 `svc_org_tech` / `svc_org_tags` / `svc_org_patent` 这三张表 |
| 对不上的地方 | 正式库卡面 0 行，解释不了 43296 篇。当时进程环境变量未见，未闭合。卡面 2026-10-22 还有更新，没有第二条水位 |

指标权威仍是 ADS。ES 有文档不等于产线 ADS 已灌完。
