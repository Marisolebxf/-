# `policy_base_info` 产线目标列（POLICY v1.0 冻结）

> **库**：`gkxlumenx_dwd` · MySQL 8  
> **日期**：2026-09-01  
> **用途**：GDF Wave B APPLY / ALTER 差集。字段语义以本包 09 为准。  
> **不是**：Demo as-built、旧 v1 37 列。

若库中尚无此表：按下列 DDL 建。  
若仅有 Demo as-built：按差集 **加列**（`source_plane` / `rank` / `policy_type` / 省市区 / `policy_support` / 国际专有列），**不要**按旧 37 列重建后丢新列。

```sql
CREATE TABLE IF NOT EXISTS `policy_base_info` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '技术主键',
  `policy_id` varchar(100) NOT NULL COMMENT '业务主键 ← ODS id',
  `source_plane` varchar(16) NOT NULL COMMENT 'domestic | global',
  `title` text NOT NULL COMMENT '政策标题',
  `issued_number` varchar(200) DEFAULT NULL COMMENT '文号',
  `publish_organization` text COMMENT '发文机构',
  `publish_date` date DEFAULT NULL COMMENT '发文日期',
  `publish_year` varchar(32) DEFAULT NULL COMMENT '发布年原文',
  `implementation_date` date DEFAULT NULL COMMENT '实施日期',
  `expire_date` date DEFAULT NULL COMMENT '失效日期',
  `status` varchar(20) DEFAULT NULL COMMENT '有效/失效原文',
  `rank` varchar(50) DEFAULT NULL COMMENT '国家级/省级/市级/区县级原文',
  `policy_type` varchar(200) DEFAULT NULL COMMENT '国内 type / 国际 category 原文',
  `topic` text COMMENT '国际专题',
  `province` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `region` text COMMENT '国际实施区域',
  `country` text COMMENT '国际国家',
  `geo_region` text COMMENT '宏观地理区',
  `disclosure_date` date DEFAULT NULL,
  `abstract` text,
  `keywords` text,
  `content` longtext,
  `url` text,
  `pedigree` text COMMENT '引用政策原文',
  `theme` text,
  `keypoints` varchar(1000) DEFAULT NULL,
  `policy_support` json DEFAULT NULL,
  `source` text,
  `appendix_name` text,
  `appendix_link` text,
  `language` text,
  `report_number` text,
  `project_id` varchar(500) DEFAULT NULL,
  `security_class` text,
  `version_type` text,
  `volume_no` text,
  `doc_type` varchar(64) DEFAULT NULL,
  `etl_batch_id` varchar(64) DEFAULT NULL,
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
