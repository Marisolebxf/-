> **【包内复制件】** 语句从 [`dwd-svc.md`](../../../../data-design/storage/SVC/stores/mysql/dwd-svc.md) §2.4 和 [`ads.md`](../../../../data-design/storage/SVC/stores/mysql/ads.md) §2.1 复制。这两处与 [`ddl-demo-empty.sql`](../../../../data-design/storage/SVC/stores/mysql/ddl-demo-empty.sql) 同文。库名改成 `gkxlumenx_dwd` / `gkxlumenx_ads`。  
> **目标库**：MySQL 8 · 正式库。禁止在库名以 `demo_` 开头的库执行。  
> **不执行**：2026-11-02 正式库这些表已经在。本文件不 DROP、不重建。缺表时才用下面的语句建。

# 服务机构表结构（MySQL）

> 本包作业只写：`svc_org_circle`、`svc_org_finance_event`、`svc_org_card`、四张基础指标表。  
> `svc_org_graph_hang` 和五张模型表正式库已有。本包不写。模型表不附 CREATE。

`org_id` 使用 `utf8mb4_general_ci`，与企业 hang 键一致。表默认排序规则同为 `utf8mb4_general_ci`。

`svc_org_circle.rule_version` 的默认值是源 SQL 里的 `svc_rule_demo_kw_v1`。作业写入的是 `svc_rule_demo_kw_v1.1`，不改这个默认值。

## 1. 表清单

| 层 | 表 | 本包作业 |
|----|----|----------|
| DWD | `svc_org_circle` | 写 |
| DWD | `svc_org_finance_event` | 写 |
| DWD | `svc_org_graph_hang` | 不写。CREATE 附上，供缺表对照 |
| ADS | `svc_org_card` | 写 |
| ADS | `svc_metric_fact` | 写。A5 |
| ADS | `svc_metric_series` | 写。A3、A4 |
| ADS | `svc_metric_dist` | 写。A1 |
| ADS | `svc_region_dist` | 写。A2、A6 |

五张模型表 `svc_chain_gap`、`svc_relation_chain`、`svc_tech_power_score`、`svc_attraction_recommend`、`svc_cultivation_recommend` 不在上表。正式库已有，列与源 SQL 一致。本包不建、不写。

## 2. 本包写入的表

### 2.1 `svc_org_circle`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| org_id | VARCHAR(64) | 否 | hang 键。`utf8mb4_general_ci` |
| rule_version | VARCHAR(32) | 否 | 默认 `svc_rule_demo_kw_v1` |
| hit_fields | JSON | 是 | 命中的源列名 |
| service_type_candidate | VARCHAR(32) | 是 | 六类候选 |
| pending_client_confirm | TINYINT(1) | 否 | 默认 1 |
| etl_batch_id | VARCHAR(64) | 是 | 批次号 |
| ext | JSON | 是 | 可空；本批不因整表回退写入（Q9 已取消） |
| created_time / updated_time | DATETIME | 否 | 创建 / 更新时间 |

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_dwd`.`svc_org_circle` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'hang ODS/ENT 同一机构键，不复制主体',
  `rule_version` VARCHAR(32) NOT NULL DEFAULT 'svc_rule_demo_kw_v1',
  `hit_fields` JSON NULL COMMENT '命中的 ODS 列名',
  `service_type_candidate` VARCHAR(32) NULL COMMENT '六类候选，待核验',
  `pending_client_confirm` TINYINT(1) NOT NULL DEFAULT 1,
  `etl_batch_id` VARCHAR(64) NULL,
  `ext` JSON NULL,
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_org_circle_org` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='SVC 圈定池 hang org_id；禁止平行 svc_org_base';
```

### 2.2 `svc_org_finance_event`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| org_id | VARCHAR(64) | 否 | hang 键 |
| event_id | VARCHAR(64) | 否 | 复合键 md5（见 `08`§3）；**表唯一键** |
| event_type | VARCHAR(16) | 否 | `FINANCING` / `INVEST` |
| amount | DECIMAL(20,2) | 是 | 金额，元 |
| event_date | DATE | 是 | 融资用完成日。投资为空 |
| etl_batch_id | VARCHAR(64) | 是 | 批次号 |
| ext | JSON | 是 | 融资轮次、投资方等 |
| created_time / updated_time | DATETIME | 否 | 创建 / 更新时间 |

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_dwd`.`svc_org_finance_event` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `event_id` VARCHAR(64) NOT NULL,
  `event_type` VARCHAR(16) NOT NULL COMMENT 'FINANCING / INVEST',
  `amount` DECIMAL(20,2) NULL,
  `event_date` DATE NULL,
  `etl_batch_id` VARCHAR(64) NULL,
  `ext` JSON NULL,
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_finance_event` (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='投融资事件 hang；event_id=复合键md5；Q-SVC-006 允许 0 行';
```

> **正式库已有表（Q11）**：同意 GDF 按现存物理表接管。唯一键若仍是 `(org_id, event_id, event_type)`，开工前 ALTER 为 `UNIQUE(event_id)`，不 DROP 表、不加业务列。demo / 正式库列集已核对一致（2026-11-04）。

### 2.3 `svc_org_card`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| org_id | VARCHAR(64) | 否 | 圈定机构 |
| name_cn | VARCHAR(255) | 是 | 名称 |
| province / city / area | VARCHAR(64) | 是 | 省 / 市 / 区县 |
| industry | VARCHAR(128) | 是 | 行业。无列则空 |
| org_size | VARCHAR(32) | 是 | 规模原文 |
| employees_number | INT | 是 | 年报人数 |
| operating_revenue | DECIMAL(20,2) | 是 | 年报营收 |
| service_type_candidate | VARCHAR(32) | 是 | 来自圈定池 |
| pending_client_confirm | TINYINT(1) | 否 | 默认 1 |
| etl_batch_id | VARCHAR(64) | 是 | 批次号 |
| ext | JSON | 是 | |
| update_time | DATETIME | 否 | 更新时间 |

源 SQL 这一张写成 `COLLATE utf8mb4_general_ci`，少了等号。现网表是 `utf8mb4_general_ci`。下面按现网和其他表写成 `COLLATE=`。

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_ads`.`svc_org_card` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name_cn` VARCHAR(255) NULL COMMENT '展示投影 ODS name_cn',
  `province` VARCHAR(64) NULL,
  `city` VARCHAR(64) NULL,
  `area` VARCHAR(64) NULL COMMENT '区县；ODS area；无 district 回退',
  `industry` VARCHAR(128) NULL COMMENT '展示投影 ODS industry；无列则空',
  `org_size` VARCHAR(32) NULL COMMENT '投影 ODS org_size；禁止当分档',
  `employees_number` INT NULL COMMENT '投影年报 employees_number',
  `operating_revenue` DECIMAL(20,2) NULL COMMENT '投影年报 operating_revenue',
  `service_type_candidate` VARCHAR(32) NULL COMMENT '来自 svc_org_circle',
  `pending_client_confirm` TINYINT(1) NOT NULL DEFAULT 1,
  `etl_batch_id` VARCHAR(64) NULL,
  `ext` JSON NULL,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_org_card_org` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='名单/详情卡面；线上不联 ODS；禁当 svc_org_base';
```

### 2.4 `svc_metric_fact`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| metric_id | VARCHAR(64) | 否 | `M_SVC_*` |
| period | VARCHAR(16) | 是 | 期间 |
| slice_key | VARCHAR(128) | 是 | 切片 |
| value | DECIMAL(20,4) | 是 | 值 |
| yoy | DECIMAL(10,4) | 是 | 同比 |
| etl_batch_id | VARCHAR(64) | 是 | 批次号 |
| ext | JSON | 是 | |
| update_time | DATETIME | 否 | 更新时间 |

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_ads`.`svc_metric_fact` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `metric_id` VARCHAR(64) NOT NULL COMMENT 'M_SVC_*',
  `period` VARCHAR(16) NULL,
  `slice_key` VARCHAR(128) NULL,
  `value` DECIMAL(20,4) NULL,
  `yoy` DECIMAL(10,4) NULL,
  `etl_batch_id` VARCHAR(64) NULL,
  `ext` JSON NULL,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_metric_fact` (`metric_id`, `period`, `slice_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='A1-A6 卡片快照';
```

### 2.5 `svc_metric_series`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| metric_id | VARCHAR(64) | 否 | A3 / A4 |
| period | VARCHAR(16) | 否 | 年 |
| value | DECIMAL(20,4) | 是 | 值 |
| etl_batch_id | VARCHAR(64) | 是 | 批次号 |
| ext | JSON | 是 | |
| update_time | DATETIME | 否 | 更新时间 |

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_ads`.`svc_metric_series` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `metric_id` VARCHAR(64) NOT NULL COMMENT 'M_SVC_INVEST_Y / M_SVC_NEW_CNT',
  `period` VARCHAR(16) NOT NULL,
  `value` DECIMAL(20,4) NULL,
  `etl_batch_id` VARCHAR(64) NULL,
  `ext` JSON NULL,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_metric_series` (`metric_id`, `period`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='A3/A4 时序';
```

### 2.6 `svc_metric_dist`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| metric_id | VARCHAR(64) | 否 | 默认 `M_SVC_INDUSTRY_LAYOUT` |
| category | VARCHAR(128) | 否 | 分类 |
| value | DECIMAL(20,4) | 是 | 机构数 |
| etl_batch_id | VARCHAR(64) | 是 | 批次号 |
| ext | JSON | 是 | |
| update_time | DATETIME | 否 | 更新时间 |

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_ads`.`svc_metric_dist` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `metric_id` VARCHAR(64) NOT NULL DEFAULT 'M_SVC_INDUSTRY_LAYOUT',
  `category` VARCHAR(128) NOT NULL,
  `value` DECIMAL(20,4) NULL,
  `etl_batch_id` VARCHAR(64) NULL,
  `ext` JSON NULL,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_metric_dist` (`metric_id`, `category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='A1 产业布局分布';
```

### 2.7 `svc_region_dist`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| metric_id | VARCHAR(64) | 否 | A2 或 A6 |
| geo_level | VARCHAR(32) | 否 | `province` / `sz_district` |
| region_name | VARCHAR(128) | 否 | 地区名 |
| org_count | INT | 是 | 机构数 |
| etl_batch_id | VARCHAR(64) | 是 | 批次号 |
| ext | JSON | 是 | |
| update_time | DATETIME | 否 | 更新时间 |

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_ads`.`svc_region_dist` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `metric_id` VARCHAR(64) NOT NULL COMMENT 'M_SVC_ORG_CNT / M_SVC_SZ_DISTRICT',
  `geo_level` VARCHAR(32) NOT NULL COMMENT 'country / province / sz_district',
  `region_name` VARCHAR(128) NOT NULL,
  `org_count` INT NULL,
  `etl_batch_id` VARCHAR(64) NULL,
  `ext` JSON NULL,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_region_dist` (`metric_id`, `geo_level`, `region_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='A2 分布 / A6 深圳各区';
```

## 3. 正式库已有、本包不写

### 3.1 `svc_org_graph_hang`

默认 `space_name` 仍是源 SQL 的 `demo_gkx_chain`。本包不改这个默认值，也不写这张表。

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| org_id | VARCHAR(64) | 否 | hang 键 |
| node_id | VARCHAR(80) | 否 | Nebula vid |
| space_name | VARCHAR(64) | 否 | 默认 `demo_gkx_chain` |
| tag_name | VARCHAR(32) | 是 | 建议 `institution` |
| etl_batch_id | VARCHAR(64) | 是 | 批次号 |
| ext | JSON | 是 | |
| created_time / updated_time | DATETIME | 否 | 创建 / 更新时间 |

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_dwd`.`svc_org_graph_hang` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `node_id` VARCHAR(80) NOT NULL COMMENT 'Nebula vid；与 org_id 对齐 hang',
  `space_name` VARCHAR(64) NOT NULL DEFAULT 'demo_gkx_chain',
  `tag_name` VARCHAR(32) NULL COMMENT '建议复用 institution；不新建 space',
  `etl_batch_id` VARCHAR(64) NULL,
  `ext` JSON NULL,
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_graph_hang` (`org_id`, `space_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='SVC hang 一张 G demo_gkx_chain；禁 gkx_service';
```

## 4. 自检（2026-11-02）

`check_gdf_ddl.py --dimension svc` 退出码 0。未执行建表，未改库。

| 核对 | 结果 |
|------|------|
| 本文件 8 张表 | 与 `dwd-svc.md` §2.4、`ads.md` §2.1 一致。库名按所在库替换 |
| `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads` | 这 8 张表的列、注释、索引、排序规则与上述语句一致 |
| `gkxlumenx_dwd` / `gkxlumenx_ads` | 同上 |
| 卡面排序规则 | 源 SQL 写成 `COLLATE=utf8mb4_general_ci`，与 demo 和正式库一致 |
| 五张模型表 | 不在本包，也不在上述两节。本次对照不含它们 |

通过。
