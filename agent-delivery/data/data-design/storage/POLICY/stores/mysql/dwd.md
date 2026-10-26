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
> **落库名**：`demo_gkxlumenx_dwd.policy_base_info`。结构真源是下面的 CREATE。技术主键是 `id`。`policy_id` 是业务键，来自 ODS `id`，不是主键。  
> 对照：[`../../etl/ods-to-dwd-mapping.md`](../../etl/ods-to-dwd-mapping.md)。本节不执行 DDL。  
> 勿把 `gkx.dwd_policy_base` 当项目 DWD 表名。旧稿 v1 的 37 列，以及本节原先的 as-built 37 列清单，都不再是这张表的结构真源。

## `policy_base_info`

本节是 `policy_base_info` 的结构真源。目标列集取派单包 [`policy_base_info-MySQL.md`](../../../../../GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/10-DWD-MySQL-DDL/policy_base_info-MySQL.md) 的 CREATE。库名写 `demo_gkxlumenx_dwd`；产线同表只换库名 `gkxlumenx_dwd`。表和全部字符列是 `utf8mb4` / `utf8mb4_0900_ai_ci`。列注释只沿用派单包里已有的注释。不写 `AUTO_INCREMENT` 当前值。

原先 as-built 37 列清单不再是这张表的结构真源，也不写回产线。`gis_location`、`related_entities`、`factors`、`elements`、`ext1`–`ext5` 不在目标列里。禁止直接改名：`ext1` 不是 `policy_type`，`level` 不是 `rank`，`region` 拼串不是 `province` / `city` / `district`。

`content`、`policy_support`、`keywords`、`keypoints`、`pedigree` 清洗时不得截断。`is_deleted=0` 仍是下游过滤条件。`is_history` 为 NULL 时视为当前，取数不过滤。国内与国际同表，平面看 `source_plane`。

2026-10-26 现网：`demo_gkxlumenx_dwd.policy_base_info` 与 `gkxlumenx_dwd.policy_base_info` 都已是上面这份 CREATE，表级 `utf8mb4_0900_ai_ci`。demo 20,000 行的 `source_plane` 整批为 `domestic`（human:淮政玮 选定，不从地区或旧列推导）。产线 0 行。旧 37 列留在 `demo_gkxlumenx_dwd.policy_base_info_pre_20261026`，不作为结构真源，也不写回产线。交叉表和行回填见 `POLICY-DDL-BASE-SPEC-L06`。

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`policy_base_info` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '技术主键',
  `policy_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '业务主键 ← ODS id',
  `source_plane` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'domestic | global',
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '政策标题',
  `issued_number` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '文号',
  `publish_organization` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '发文机构',
  `publish_date` date DEFAULT NULL COMMENT '发文日期',
  `publish_year` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '发布年原文',
  `implementation_date` date DEFAULT NULL COMMENT '实施日期',
  `expire_date` date DEFAULT NULL COMMENT '失效日期',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '有效/失效原文',
  `rank` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '国家级/省级/市级/区县级原文',
  `policy_type` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '国内 type / 国际 category 原文',
  `topic` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '国际专题',
  `province` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `district` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `region` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '国际实施区域',
  `country` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '国际国家',
  `geo_region` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '宏观地理区',
  `disclosure_date` date DEFAULT NULL,
  `abstract` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `keywords` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `pedigree` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '引用政策原文',
  `theme` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `keypoints` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `policy_support` json DEFAULT NULL,
  `source` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `appendix_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `appendix_link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `language` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `report_number` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `project_id` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `security_class` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `version_type` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `volume_no` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `doc_type` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `etl_batch_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ods_updated_time` datetime DEFAULT NULL,
  `is_deleted` smallint NOT NULL DEFAULT 0,
  `is_history` int DEFAULT NULL COMMENT '0当前，1历史；NULL视为当前。取数不过滤',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_policy_plane_id` (`source_plane`, `policy_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='政策主表（国内+国际同表）';
```

## 政策–产业关联：`policy_industry_rel`

本节是 `policy_industry_rel` 的结构真源。上文 `policy_base_info` 的 as-built 37 列清单不是这张关联表的依据。

落库名 `demo_gkxlumenx_dwd.policy_industry_rel`。产业抽取（按钮与跑批）先写本表，再按 `policy_id` 把该政策的行同步到 ADS 同名表。不 `UPDATE` 主表 `related_entities`。算法侧增量与「已抽过」仍读本表。

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`policy_industry_rel` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `policy_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '对应 policy_base_info.policy_id',
  `industry_name` varchar(200) NOT NULL DEFAULT '' COMMENT '产业名',
  `industry_link_code` varchar(128) NOT NULL DEFAULT '' COMMENT 'chain: / segment:；仅名称时为空串',
  `is_deleted` tinyint NOT NULL DEFAULT 0 COMMENT '0 有效，1 逻辑删除',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '写入时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '最近一次同步时间',
  PRIMARY KEY (`id`),
  KEY `idx_policy_industry_rel_pid` (`policy_id`, `is_deleted`),
  KEY `idx_policy_industry_rel_code` (`industry_link_code`, `is_deleted`, `policy_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='政策–产业关联。抽取写入，不回写主表';
```

`policy_id` 列排序规则收到 `utf8mb4_0900_ai_ci`。现网 `demo_gkxlumenx_dwd.policy_industry_rel.policy_id` 是 `utf8mb4_general_ci`，表级已经是 `utf8mb4_0900_ai_ci`。上面的 CREATE 在该列写明这一套，不另起列集。本叶不改库。

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

## 政策文本解析：`policy_text_parse`

总控要求本表在 DWD 有说明和建表语句。现网 `demo_gkxlumenx_dwd` 没有 `policy_text_parse`，同名表只在 `demo_gkxlumenx_ads`。下面的 CREATE 库名写 `demo_gkxlumenx_dwd`；列、类型、空值、默认值、索引与 2026-10-26 现网 `demo_gkxlumenx_ads.policy_text_parse` 一致。字符集 `utf8mb4`，排序规则 `utf8mb4_0900_ai_ci`（现网 ADS 该表是 `utf8mb4_unicode_ci`）。不写 `AUTO_INCREMENT` 当前值。本叶不建表。

用途与 [`ads.md`](./ads.md) 相同：D1 政策文本解析，摘要 + 结构化要素 + 自动标签。列注释口径同 ADS 那份 CREATE。

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`policy_text_parse` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `policy_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `title` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `summary` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '摘要',
  `structured_elements` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '结构化要素',
  `auto_tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '自动标签',
  `model_version` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '规则基线产物须在 UI 标注模型版本',
  `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='D1 政策文本解析：摘要 + 结构化要素 + 自动标签';
```

