# 政策维 ODS 表级清单

```yaml
---
doc_id: POLICY-SOURCE-INVENTORY
element: POLICY
role: source
status: draft
version: "2026-08-21"
updated: 2026-08-21
task_id: DATA-POLICY-STORAGE-S2-L01
---
```

> **结构真源**：[`ods-ddl.md`](./ods-ddl.md)（DDL 赢口径文档）。  
> 供应库 **`gkx`**：`dwd_policy_base` / `dwd_global_policy_base`。表名带 `dwd_`，对本项目仍是 **ODS**。  
> 旧名 `dwd_zck_*` **废止**。Demo 镜像：`demo_gkxlumenx_ods` 同 DDL、同表名。不写正式 `gkx`。  
> 列对照：[`../etl/ods-to-dwd-mapping.md`](../etl/ods-to-dwd-mapping.md)。  
> **禁止**：本叶灌数。

## 目标库

| 层 | 库名 | 说明 |
|---|---|---|
| 三方供应（只读对照） | `gkx` | `dwd_policy_base` / `dwd_global_policy_base` |
| Demo ODS | `demo_gkxlumenx_ods` | 同构贴源表名；与 ENT/CHAIN 共用实例 |
| 项目 DWD | `demo_gkxlumenx_dwd` | **`policy_base_info`**（勿与供应表 `dwd_policy_base` 混名） |
| 正式 ODS | `gkxlumenx_ods` | **本管线零写入** |

## 本域主读（P0）

| 约定表名 | 中文 | 角色 | 下游 |
|---|---|---|---|
| `dwd_policy_base` | 国内政策 | ODS 贴源 | → 项目 DWD `policy_base_info` |
| `dwd_global_policy_base` | 国际政策 | ODS 贴源 | 入 DWD：国际切片 + `source`；专有列进 ext |

国内关键列：`id,title,publish_code,ministry,publish_date,status,rank,type,province,city,district,quote_policy,theme,keypoints,policy_support(json)`。  
国际关键列：`id,title,organ,year,publish_date,category,country,region,geo_region,language,topic,theme,doc_type`。  
产业/企业 hang 用跨域主键，对不齐不上图。

**展示窗口不另建 ODS。** 类别读 `type`/`category`，层级读 `rank`，海外读 `country`（QPOL-01）。抓取网站 ≠ 增表。
