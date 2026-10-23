# POLICY · DWD

```yaml
---
doc_id: POLICY-STORE-MYSQL-DWD
element: POLICY
role: store-mysql
status: draft
version: "2026-08-21"
updated: 2026-10-23
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

1. **深度文本列仍是企业 / 人才 / 机关 / 服务与谱系的燃料**：`related_entities` 的 `enterprise` / `talent` / `org` / `service` 供对应边，`pedigree` 供 `cite`，`factors` 进 `support` 边 props，`keywords` / `keypoints` 供 NER。清洗时不得丢弃或截断。
2. **`ext1` 当前承载政策类型**（`M_POLICY_TYPE_DIST` 读它），属 QPOL-01 临时口径；甲方确认类别体系后应迁至正名列，届时本表与 `policy_type_dist` 同步改。
3. **`related_entities.industry` 贴源后弃用**（2026-10-23）。贴源只把 `theme` 写入 `ext5`，不写这个键。产业抽取完成后再写，也**不**更新这里。`ext5` 只保留主题原文，不再充当产业关联的回落位。
4. `is_deleted=0` 是全部下游算法的统一过滤条件。
5. 国际政策不另建表，靠 `source` + 平面标记切片；国际专有列（`organ` / `country` / `geo_region` / `language` / `doc_type` 等）进扩展位，映射见 [`../../etl/ods-to-dwd-mapping.md`](../../etl/ods-to-dwd-mapping.md)。

## 政策–产业关联：`policy_industry_rel`

落库名 `demo_gkxlumenx_dwd.policy_industry_rel`。产业抽取（按钮与跑批）先写本表，再按 `policy_id` 把该政策的行同步到 ADS 同名表。不 `UPDATE` 主表 `related_entities`。算法侧增量与「已抽过」仍读本表。

| 列 | 含义 |
|---|---|
| `id` | 自增主键 |
| `policy_id` | 政策业务主键，对应 `policy_base_info.policy_id` |
| `industry_name` | 产业名 |
| `industry_link_code` | 产业链码（`chain:` / `segment:`）；只有名称时为空串 |
| `is_deleted` | `0` 有效，`1` 逻辑删除。再次抽取时，本次没有的有效行改为 `1`，不物理删除；同一链码再次出现则改回 `0` |
| `create_time` / `update_time` | 写入与最近一次同步时间 |

读有效关联：`is_deleted=0`。图谱产业边（`support` / `apply_to` → industry）以本表有效行为源，不再读 `related_entities.industry` 或 `ext5`。

索引：`(policy_id, is_deleted)` 给按政策读取、同步和增量跳过；`(industry_link_code, is_deleted, policy_id)` 给按链码查政策，末列 `policy_id` 让关联子查询不用回表。`is_deleted` 不做最左列。条件写 `is_deleted=0`，不用 `COALESCE`。

ADS 镜像见 [`ads.md`](./ads.md) 的 `policy_industry_rel`。同步发生在单次抽取提交内：删掉 ADS 里该 `policy_id` 的行，再按 DWD 当前行插入（`id`、`is_deleted` 一致）。Java 只读 ADS。
