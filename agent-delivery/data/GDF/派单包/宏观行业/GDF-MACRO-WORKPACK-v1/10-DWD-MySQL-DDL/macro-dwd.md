# 宏观行业 DWD 建表（草稿 · 六张）

> **日期**：2026-11-09 · **状态**：草稿（`OPEN-MACRO-05`）。库 `gkxlumenx_dwd`，MySQL 8。  
> 列与 09 §3 一一对应。**未对产线库核差集**（`OPEN-MACRO-06`）。已有表只 ADD COLUMN，不 DROP、不改 UK。  
> 本文档的 DDL **未在任何库上执行过**；语法按 MySQL 8 写，GDF 执行前自检。

公共治理列（六张表都有）：`etl_batch_id` / `ods_updated_time` / `created_time` / `updated_time`。

## 1. `macro_index_data`（事实）

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_dwd`.`macro_index_data` (
  `id`                 bigint        NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `index_code`         varchar(50)   NOT NULL COMMENT '指标代码，关联 macro_index_attribute.index_code',
  `occur_period`       int           NOT NULL COMMENT '数据期 YYYYMM',
  `area_code`          varchar(32)   NOT NULL COMMENT '事实所属区划键。长度 2/3/4/12 混存（国家码/省码/市码/区县码），原文，禁止转 int',
  `area_code_type`     int           NOT NULL COMMENT '区划类型。1 行政区；3 园区（实测仅长沙）；4 未定义（含义待供应方澄清，OPEN-MACRO-01）。v1 ADS 只取 1',
  `dim_cal`            varchar(32)   NOT NULL COMMENT '计算类型代码 HB/TB/JDZ，关联 macro_index_cal.dim_cal',
  `dim_dur`            varchar(32)   NOT NULL COMMENT '时间特征代码 QM/DJ/DNLJ/DY/ZC/LSLJ/NC，关联 macro_index_dur.dim_dur',
  `index_value`        decimal(38,8)          DEFAULT NULL COMMENT '指标值，保留 8 位小数',
  `unit_use`           varchar(50)            DEFAULT NULL COMMENT '该行数值的真实单位（元/% 等）。TB 行为 %。不要用 macro_index_attribute.unit_use（恒为元）',
  `occur_period_t`     varchar(20)            DEFAULT NULL COMMENT '数据期首日，原文如 2018-06-01',
  `occur_period_year`  int                    DEFAULT NULL COMMENT '数据期年',
  `occur_period_month` int                    DEFAULT NULL COMMENT '数据期月',
  `label`              int                    DEFAULT NULL COMMENT '1 宏观 / 2 中观；实测全为 1',
  `source_code`        varchar(100)           DEFAULT NULL COMMENT '来源代码 LBS/NATIONALSTAT/GACC/worldbank，关联 macro_source_code',
  `src_rid`            int                    DEFAULT NULL COMMENT '供应方 rid',
  `src_update_time`    datetime               DEFAULT NULL COMMENT '供应方业务「数据更新时间」',
  `area_resolve`       varchar(32)   NOT NULL DEFAULT 'unresolved' COMMENT '区划反解类别：city_by_city_code/municipality_by_province_code/district_by_area_code/unresolved，规则见包 04 §3.2',
  `city_code`          varchar(50)            DEFAULT NULL COMMENT '反解出的 12 位市码；unresolved 为 NULL',
  `city_name`          varchar(150)           DEFAULT NULL COMMENT '反解出的城市名',
  `province_code`      varchar(50)            DEFAULT NULL COMMENT '反解出的省码',
  `is_deleted`         tinyint       NOT NULL DEFAULT 0 COMMENT '源逻辑删除标识，原样；应用侧自行 is_deleted=0',
  `etl_batch_id`       varchar(64)            DEFAULT NULL COMMENT 'ETL 批次',
  `ods_updated_time`   datetime               DEFAULT NULL COMMENT 'ODS updated_time（增量水位）',
  `created_time`       datetime      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'DWD 写入时间',
  `updated_time`       datetime      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'DWD 更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_macro_fact` (`index_code`, `occur_period`, `area_code`, `area_code_type`, `dim_cal`, `dim_dur`),
  KEY `idx_macro_city` (`city_code`, `area_code_type`, `index_code`, `dim_cal`, `dim_dur`, `occur_period`),
  KEY `idx_macro_resolve` (`area_resolve`, `area_code_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='宏观行业事实。来源 gkx.dwd_macro_index_data；加区划反解派生列';
```

## 2. `macro_admin_area`（区划维度）

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_dwd`.`macro_admin_area` (
  `id`               bigint       NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `cur_code`         varchar(50)  NOT NULL COMMENT '本行区域编码（唯一）',
  `cur_name`         varchar(150)          DEFAULT NULL COMMENT '本行区域名称',
  `parent_code`      varchar(50)           DEFAULT NULL COMMENT '父级区域编码',
  `country_code`     varchar(50)           DEFAULT NULL COMMENT '国家编码，如 0086，禁止转 int',
  `country_name`     varchar(150)          DEFAULT NULL COMMENT '国家名称',
  `province_code`    varchar(50)           DEFAULT NULL COMMENT '省码',
  `province_name`    varchar(150)          DEFAULT NULL COMMENT '省名',
  `city_code`        varchar(50)           DEFAULT NULL COMMENT '市码（12 位）',
  `city_name`        varchar(150)          DEFAULT NULL COMMENT '市名',
  `area_code`        varchar(50)           DEFAULT NULL COMMENT '区县编码。注意：不是 macro_index_data.area_code 的同义列',
  `area_name`        varchar(150)          DEFAULT NULL COMMENT '区县名称',
  `street_code`      varchar(50)           DEFAULT NULL COMMENT '街道编码',
  `street_name`      varchar(150)          DEFAULT NULL COMMENT '街道名称',
  `community_code`   varchar(50)           DEFAULT NULL COMMENT '社区编码',
  `community_name`   varchar(150)          DEFAULT NULL COMMENT '社区名称',
  `cur_level`        int                   DEFAULT NULL COMMENT '1 国家/2 省/3 市/4 区县/5 街道/6 社区',
  `qh_base_id`       int                   DEFAULT NULL COMMENT '供应方基础区域 ID',
  `source_code`      varchar(255)          DEFAULT NULL COMMENT '来源代码',
  `src_rid`          int                   DEFAULT NULL COMMENT '供应方 rid',
  `src_update_time`  datetime              DEFAULT NULL COMMENT '供应方业务更新时间',
  `is_deleted`       tinyint      NOT NULL DEFAULT 0 COMMENT '源逻辑删除标识，原样',
  `etl_batch_id`     varchar(64)           DEFAULT NULL COMMENT 'ETL 批次',
  `ods_updated_time` datetime              DEFAULT NULL COMMENT 'ODS updated_time',
  `created_time`     datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'DWD 写入时间',
  `updated_time`     datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'DWD 更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_macro_area_cur` (`cur_code`),
  KEY `idx_macro_area_city` (`city_code`),
  KEY `idx_macro_area_prov` (`province_code`),
  KEY `idx_macro_area_dist` (`area_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='宏观行业区划维度。来源 gkx.dwd_dim_admin_area；仅用于区划反解，四个政策城市无自己的 cur_code 行';
```

## 3. `macro_index_attribute`（指标属性维度）

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_dwd`.`macro_index_attribute` (
  `id`               bigint       NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `index_code`       varchar(255) NOT NULL COMMENT '指标代码（唯一）',
  `index_name`       varchar(255)          DEFAULT NULL COMMENT '指标名称',
  `unit_show`        varchar(255)          DEFAULT NULL COMMENT '推荐展示单位，如 元,千元,万元,亿元',
  `unit_use`         varchar(255)          DEFAULT NULL COMMENT '库存单位，恒为「元」。不是行单位；行真实单位以 macro_index_data.unit_use 为准',
  `data_freq`        varchar(50)           DEFAULT NULL COMMENT '公布频率：月度/季度/年度',
  `time_attr_tag`    varchar(50)           DEFAULT NULL COMMENT '时间属性标签，允许空',
  `src_rid`          int                   DEFAULT NULL COMMENT '供应方 rid',
  `src_create_time`  datetime              DEFAULT NULL COMMENT '供应方指标创建时间',
  `is_deleted`       tinyint      NOT NULL DEFAULT 0 COMMENT '源逻辑删除标识，原样',
  `etl_batch_id`     varchar(64)           DEFAULT NULL COMMENT 'ETL 批次',
  `ods_updated_time` datetime              DEFAULT NULL COMMENT 'ODS updated_time',
  `created_time`     datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'DWD 写入时间',
  `updated_time`     datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'DWD 更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_macro_attr_code` (`index_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='宏观行业指标属性维度。来源 gkx.dwd_dim_index_attribute';
```

## 4. `macro_index_cal`（计算维度）

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_dwd`.`macro_index_cal` (
  `id`               bigint       NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `dim_cal`          varchar(50)  NOT NULL COMMENT '计算维度代码 HB/TB/JDZ（唯一）',
  `dim_cal_name`     varchar(150)          DEFAULT NULL COMMENT '名称，如 可比同比增长(%)',
  `dim_cal_desc`     varchar(255)          DEFAULT NULL COMMENT '解释',
  `src_rid`          int                   DEFAULT NULL COMMENT '供应方 rid',
  `src_create_time`  datetime              DEFAULT NULL COMMENT '供应方创建时间',
  `is_deleted`       tinyint      NOT NULL DEFAULT 0 COMMENT '源逻辑删除标识，原样',
  `etl_batch_id`     varchar(64)           DEFAULT NULL COMMENT 'ETL 批次',
  `ods_updated_time` datetime              DEFAULT NULL COMMENT 'ODS updated_time',
  `created_time`     datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'DWD 写入时间',
  `updated_time`     datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'DWD 更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_macro_cal` (`dim_cal`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='宏观行业计算维度。来源 gkx.dwd_dim_index_cal';
```

## 5. `macro_index_dur`（时间维度）

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_dwd`.`macro_index_dur` (
  `id`               bigint       NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `dim_dur`          varchar(50)  NOT NULL COMMENT '时间维度代码 QM/DJ/DNLJ/DY/ZC/LSLJ/NC（唯一）',
  `dim_dur_name`     varchar(50)           DEFAULT NULL COMMENT '名称，如 当年累计',
  `dim_dur_desc`     varchar(255)          DEFAULT NULL COMMENT '解释',
  `src_rid`          int                   DEFAULT NULL COMMENT '供应方 rid',
  `src_create_time`  datetime              DEFAULT NULL COMMENT '供应方创建时间',
  `is_deleted`       tinyint      NOT NULL DEFAULT 0 COMMENT '源逻辑删除标识，原样',
  `etl_batch_id`     varchar(64)           DEFAULT NULL COMMENT 'ETL 批次',
  `ods_updated_time` datetime              DEFAULT NULL COMMENT 'ODS updated_time',
  `created_time`     datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'DWD 写入时间',
  `updated_time`     datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'DWD 更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_macro_dur` (`dim_dur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='宏观行业时间维度。来源 gkx.dwd_dim_index_dur';
```

## 6. `macro_source_code`（来源维度）

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_dwd`.`macro_source_code` (
  `id`               bigint       NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `source_code`      varchar(100) NOT NULL COMMENT '来源代码 GACC/worldbank/LBS/NATIONALSTAT（唯一）',
  `source_name`      varchar(255)          DEFAULT NULL COMMENT '来源名称',
  `src_rid`          int                   DEFAULT NULL COMMENT '供应方 rid',
  `src_create_time`  datetime              DEFAULT NULL COMMENT '供应方创建时间',
  `is_deleted`       tinyint      NOT NULL DEFAULT 0 COMMENT '源逻辑删除标识，原样',
  `etl_batch_id`     varchar(64)           DEFAULT NULL COMMENT 'ETL 批次',
  `ods_updated_time` datetime              DEFAULT NULL COMMENT 'ODS updated_time',
  `created_time`     datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'DWD 写入时间',
  `updated_time`     datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'DWD 更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_macro_source` (`source_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='宏观行业来源维度。来源 gkx.dwd_dim_source_code';
```
