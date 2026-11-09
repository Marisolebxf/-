# MACRO · MySQL ADS

> **状态**：draft · 2026-11-09 `GDF-MACRO-STORAGE-DDL-L01`（`OPEN-MACRO-05`）。  
> **结构真源**：本文件。CREATE 逐字复制自派单包 `GDF-MACRO-WORKPACK-v1/12-DWD后加工-城市截面ADS与实效代理附录.md` §2，仅库名写 `demo_gkxlumenx_ads`（产线 `gkxlumenx_ads`）。  
> 灌数 SQL（②a）与血缘占位见派单包 12 §3–§4，本文件不复制。派生物，整体重建。

## 1. `macro_city_section`

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`macro_city_section` (
  `id`              bigint       NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `city_code`       varchar(50)  NOT NULL COMMENT '12 位市码（反解得到）',
  `city_name`       varchar(150)          DEFAULT NULL COMMENT '城市名',
  `province_code`   varchar(50)           DEFAULT NULL COMMENT '省码',
  `fact_area_code`  varchar(32)  NOT NULL COMMENT '事实表原 area_code（直辖市为 2 位省码，其他为 12 位市码）',
  `area_code_type`  int          NOT NULL COMMENT '区划类型，本表恒为 1',
  `area_resolve`    varchar(32)  NOT NULL COMMENT 'city_by_city_code / municipality_by_province_code',
  `index_code`      varchar(50)  NOT NULL COMMENT '指标代码',
  `index_name`      varchar(255)          DEFAULT NULL COMMENT '指标名称（macro_index_attribute）',
  `data_freq`       varchar(50)           DEFAULT NULL COMMENT '指标公布频率',
  `dim_cal`         varchar(32)  NOT NULL COMMENT '计算类型代码 HB/TB/JDZ',
  `dim_cal_name`    varchar(150)          DEFAULT NULL COMMENT '计算类型名称',
  `dim_dur`         varchar(32)  NOT NULL COMMENT '时间特征代码',
  `dim_dur_name`    varchar(50)           DEFAULT NULL COMMENT '时间特征名称',
  `occur_period`    int          NOT NULL COMMENT '该序列最新一期（非空值）YYYYMM。各城各指标不对齐',
  `index_value`     decimal(38,8)         DEFAULT NULL COMMENT '最新一期的值，原值不裁剪',
  `unit_use`        varchar(50)           DEFAULT NULL COMMENT '该行真实单位（来自事实表，非属性表）',
  `source_code`     varchar(100)          DEFAULT NULL COMMENT '来源代码',
  `series_points`   int          NOT NULL COMMENT '该序列（非空、未删）的数据点数。很稀，样本期常为 1–6',
  `etl_batch_id`    varchar(64)           DEFAULT NULL COMMENT 'ETL 批次',
  `created_time`    datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '写入时间',
  `updated_time`    datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_macro_city_section` (`fact_area_code`, `area_code_type`, `index_code`, `dim_cal`, `dim_dur`),
  KEY `idx_macro_section_city` (`city_code`, `index_code`, `dim_cal`, `dim_dur`),
  KEY `idx_macro_section_idx` (`index_code`, `dim_cal`, `dim_dur`, `occur_period`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='城市宏观截面（②a）。来源 gkxlumenx_dwd.macro_index_data 聚合；只读给展示/专题；整体重建';
```

