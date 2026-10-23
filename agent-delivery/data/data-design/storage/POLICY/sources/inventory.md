# 政策维 ODS 表级清单

```yaml
---
doc_id: POLICY-SOURCE-INVENTORY
element: POLICY
role: source
status: draft
version: "2026-08-21"
updated: 2026-10-23
task_id: DATA-POLICY-STORAGE-S2-L01
---
```

> **结构真源**：汇总表「国内政策要素库」「国外政策要素库」（各 35 列）。DDL 落点 [`ods-ddl.md`](./ods-ddl.md)。  
> 三方只读 ODS 固定 `gkx.dwd_policy_base`（国内）、`gkx.dwd_global_policy_base`（海外）。表名带 `dwd_`，对本项目仍是 **ODS**。业务键是 `id`，`t_id` 只做分片。  
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
| `dwd_policy_base` | 国内政策 | ODS 只读 | → 项目 DWD `policy_base_info` |
| `dwd_global_policy_base` | 海外政策 | ODS 只读 | 入同一张 DWD；专有列见下 |

国内 35 列：`t_id,id,title,publish_code,ministry,publish_date,publish_year,implementation_date,expire_date,status,rank,type,province,city,district,abstract,keywords,content,link,quote_policy,theme,keypoints,policy_support,source,appendix_name,appendix_link,is_history,created_time,updated_time,creater,updater,table_data_source,operator_remarks,is_deleted,insert_remark`。  
海外 35 列：`t_id,id,title,abstract,organ,year,publish_date,disclosure_date,category,content,region,link,language,source,geo_region,appendix_name,appendix_link,country,report_number,topic,theme,project_id,security_class,version_type,volume_no,doc_type,is_history,created_time,updated_time,creater,updater,table_data_source,operator_remarks,is_deleted,insert_remark`。  
产业/企业 hang 用跨域主键，对不齐不上图。

**展示窗口不另建 ODS。** 类别读 `type`/`category`，层级读 `rank`，海外读 `country`（QPOL-01）。抓取网站 ≠ 增表。
