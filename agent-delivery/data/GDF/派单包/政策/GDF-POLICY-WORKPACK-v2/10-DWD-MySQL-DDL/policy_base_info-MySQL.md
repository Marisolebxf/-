# `policy_base_info` 产线目标列（POLICY v1.0 冻结）

> **库**：`gkxlumenx_dwd` · MySQL 8  
> **日期**：2026-09-01  
> **用途**：GDF Wave B APPLY / ALTER 差集。字段语义以本包 09 为准。  
> **不是**：Demo as-built、旧 v1 37 列。

若库中尚无此表：按下列 DDL 建。  
若仅有 Demo as-built：按差集 **加列**（`source_plane` / `rank` / `policy_type` / 省市区 / `policy_support` / 国际专有列），**不要**按旧 37 列重建后丢新列。

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

目标索引：单列 `policy_id` 的普通索引 `idx_pid`，不是唯一键。上面的唯一键仍是 `(source_plane, policy_id)`。加索引的语句在 `sql/update_round1.sql`。这列不清重，不删行。本仓不代跑。

## 与 Demo as-built 的差集（诚实）

| Demo as-built（`stores/mysql/dwd.md`） | 产线 |
|---|---|
| 无 `source_plane` | **必有** |
| `level` / `region` 拼串 / `ext1` 当类型 | 改用 `rank` + 省市区 + `policy_type` |
| `gis_location` / `sci_tech_attribute` | **不要求**建；禁止假填 |
| `related_entities` / `factors` / `elements` | 算法链燃料，**本包不写**（无 ODS 列） |
| `ext1`–`ext5` | 本包不写正名数据 |
| 无 `is_history` | **必有**。源列原样映射；`NULL` 视为当前 |

`content` / `policy_support` / `keywords` / `keypoints` / `pedigree` 清洗时不得截断。
