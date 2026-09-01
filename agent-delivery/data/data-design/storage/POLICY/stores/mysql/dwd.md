# POLICY · DWD

```yaml
---
doc_id: POLICY-STORE-MYSQL-DWD
element: POLICY
role: store-mysql
status: draft
version: "2026-08-21"
updated: 2026-08-21
engine: mysql
task_id: DATA-POLICY-STORAGE-S3-L01
---
```

> **贴源结构**：[`../../sources/ods-ddl.md`](../../sources/ods-ddl.md)。  
> **落库名**：`demo_gkxlumenx_dwd.policy_base_info`。主键 `policy_id` ← ODS `id`。  
> 对照：[`../../etl/ods-to-dwd-mapping.md`](../../etl/ods-to-dwd-mapping.md)。本叶不 APPLY。  
> 勿把 `gkx.dwd_policy_base` 当项目 DWD 表名。旧稿 v1 37 列 **过期**。

项目 DWD 列以能承接贴源为准：`status` 用有效/失效文案；`rank`/`type`/`province|city|district`/`policy_support` JSON 必须能落到库，禁止再压成旧 smallint `level`。国际行同表 + 平面标记。

## as-built 列清单（回源 `polan/common/db.py`）

单表 `policy_base_info`，国内与国际政策同表。按用途分群：

| 群 | 列 |
|---|---|
| 主键与租户 | `id`(pk) · `tenant_id` · **`policy_id`**（业务主键 ← ODS `id`） |
| 基本信息 | `title` · `issued_number` · `publish_organization` · `url` · `source` |
| 时间 | `publish_date` · `implementation_date` · `expire_date` · `publish_year` |
| 分类与状态 | `status` · `level` · `region` · `sci_tech_attribute` |
| 正文与摘要 | `abstract` · `content` · `keywords` |
| 深度文本字段 | `elements` · `keypoints` · `factors` · `pedigree` · `related_entities`(json) |
| 执行口径 | `application_conditions` · `execution_cycle` · `execution_entity` |
| 其他 | `gis_location` · `attachment` |
| 审计 | `create_time` · `update_time` · `is_deleted` |
| 扩展位 | `ext1`–`ext5` |

要点：

1. **深度文本五列是算法链的燃料**，不是装饰：`related_entities`(json) 供 RE 抽四类边，`pedigree` 供 `cite` 上位政策解析，`factors` 进 `support` 边 props，`keywords` / `keypoints` 供 NER 与 D1 解析。清洗时不得丢弃或截断。
2. **`ext1` 当前承载政策类型**（`M_POLICY_TYPE_DIST` 读它），属 QPOL-01 临时口径；甲方确认类别体系后应迁至正名列，届时本表与 `policy_type_dist` 同步改。
3. **`ext5` 是产业回落位**：`related_entities.industry` 为空时用它兜底建 `support` / `apply_to` 边。
4. `is_deleted=0` 是全部下游算法的统一过滤条件。
5. 国际政策不另建表，靠 `source` + 平面标记切片；国际专有列（`organ` / `country` / `geo_region` / `language` / `doc_type` 等）进扩展位，映射见 [`../../etl/ods-to-dwd-mapping.md`](../../etl/ods-to-dwd-mapping.md)。
