-- DR-RES-MOCK-DDL-L01
-- 只建表，不灌业务行。可重复执行。
-- 库只允许 demo_gkxlumenx_ads。表名一律 gapfill_dr_。
-- 禁止：INSERT / UPDATE / DELETE / DROP / TRUNCATE；禁止 gkxlumenx_ads、ODS、DWD、久新、gkxlumenx_gapfill。
-- 每张表：id、calc_batch_id、generated_at、fill_method。
-- calc_batch_id 由灌数叶填写，前缀 mock_ 或 snap_。fill_method 首批为 manual。
-- gapfill_dr_block_json.block_code 不在本叶插行。
-- gapfill_dr_column_catalog 只建列，不写现网 131 列快照。

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_type_slice` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `slice_kind` VARCHAR(32) NOT NULL COMMENT 'structure / theme',
  `name` VARCHAR(128) NOT NULL,
  `value` BIGINT NOT NULL,
  `color` VARCHAR(32) NULL,
  `avg_quality` DECIMAL(6,2) NULL,
  `heat` VARCHAR(32) NULL,
  `lifecycle` VARCHAR(32) NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='类型分布、主题分布；累计调用的类型拆分';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_source_channel` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `channel_group` VARCHAR(32) NOT NULL COMMENT 'srs_source / org_activity',
  `channel_code` VARCHAR(64) NOT NULL,
  `channel_name` VARCHAR(128) NOT NULL,
  `stat_month` VARCHAR(16) NOT NULL,
  `volume` BIGINT NULL,
  `item_count` BIGINT NULL,
  `share_pct` DECIMAL(8,2) NULL,
  `change_pct` DECIMAL(8,2) NULL,
  `trend` VARCHAR(32) NULL,
  `reliability` DECIMAL(6,2) NULL,
  `avg_quality` DECIMAL(6,2) NULL,
  `color` VARCHAR(32) NULL,
  `activity` DECIMAL(10,2) NULL,
  `status` VARCHAR(32) NULL,
  `sample_tags` JSON NULL,
  `reliability_hint` VARCHAR(512) NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='来源分布、来源分析、活跃度、结构趋势';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_catalog_item` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `list_code` VARCHAR(32) NOT NULL COMMENT 'overview_source / access_source / access_detail',
  `name` VARCHAR(256) NOT NULL COMMENT '名称',
  `source_name` VARCHAR(256) NULL COMMENT '来源',
  `item_type` VARCHAR(64) NULL COMMENT '类型',
  `channel_name` VARCHAR(64) NULL COMMENT '渠道',
  `domain_name` VARCHAR(64) NULL COMMENT '领域',
  `collect_time` VARCHAR(32) NULL COMMENT '采集时间',
  `quality_score` DECIMAL(6,2) NULL COMMENT '质量分',
  `reliability` VARCHAR(64) NULL COMMENT '可靠度',
  `related_project` VARCHAR(256) NULL COMMENT '关联项目',
  `volume_label` VARCHAR(64) NULL COMMENT '体量',
  `tags` JSON NULL COMMENT '标签',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='三个明细列表';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_ingest_task` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `ingest_method` VARCHAR(64) NOT NULL COMMENT 'API接口、文件传输、数据库同步、人工录入、物联网采集',
  `status` VARCHAR(32) NOT NULL COMMENT 'done / running / pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='接入完成度';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_collection_fact` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `grain` VARCHAR(16) NOT NULL COMMENT 'year / month / week / day',
  `period_label` VARCHAR(32) NOT NULL,
  `metric` VARCHAR(32) NOT NULL COMMENT 'added / updated / volume',
  `ingest_method` VARCHAR(64) NULL,
  `channel_name` VARCHAR(128) NULL,
  `table_name` VARCHAR(128) NULL,
  `biz_type` VARCHAR(64) NULL,
  `row_count` BIGINT NULL,
  `size_label` VARCHAR(64) NULL,
  `update_cycle` VARCHAR(32) NULL,
  `status` VARCHAR(32) NULL,
  `anomaly_type` VARCHAR(64) NULL,
  `anomaly_note` VARCHAR(512) NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='年度接入、接入趋势、渠道归集、历史记录、更新周期、历史仪表盘';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_theme_library` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `name` VARCHAR(256) NOT NULL COMMENT '主题库卡片名称，第 5 节 themeDatabases 必需',
  `category` VARCHAR(64) NULL,
  `resource_type` VARCHAR(64) NULL,
  `tags` JSON NULL,
  `table_count` INT NULL,
  `record_yi` DECIMAL(12,4) NULL COMMENT '记录数，单位亿，供汇总',
  `storage_tb` DECIMAL(12,4) NULL COMMENT '存储量，单位 TB，供汇总',
  `quality` DECIMAL(6,2) NULL,
  `source_name` VARCHAR(256) NULL,
  `region` VARCHAR(64) NULL,
  `update_freq` VARCHAR(32) NULL,
  `related_project` VARCHAR(256) NULL,
  `description` VARCHAR(1024) NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='themeDatabases；主题页四个总数由行汇总';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_theme_column` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `theme_id` BIGINT NOT NULL COMMENT '指向 gapfill_dr_theme_library.id',
  `table_name` VARCHAR(128) NOT NULL,
  `table_comment` VARCHAR(256) NULL,
  `field_name` VARCHAR(128) NOT NULL,
  `field_type` VARCHAR(64) NULL,
  `meaning` VARCHAR(512) NULL,
  `required_flag` TINYINT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='themeDatabases[].tableSchemas';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_quality_issue` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `name` VARCHAR(256) NOT NULL,
  `table_name` VARCHAR(128) NULL,
  `issue_type` VARCHAR(64) NULL,
  `category` VARCHAR(64) NULL,
  `data_cluster` VARCHAR(64) NULL,
  `level` VARCHAR(32) NULL,
  `status` VARCHAR(32) NULL,
  `found_at` VARCHAR(32) NULL,
  `ingest_method` VARCHAR(64) NULL,
  `detail` VARCHAR(1024) NULL,
  `suggestion` VARCHAR(512) NULL,
  `color` VARCHAR(32) NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='问题列表；统计由行计数';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_usage_subject` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `subject_type` VARCHAR(32) NOT NULL COMMENT 'app_subject / asset / supplier / demander / business / region',
  `name` VARCHAR(256) NOT NULL COMMENT '名称',
  `department` VARCHAR(128) NULL COMMENT '部门',
  `region_name` VARCHAR(64) NULL COMMENT '区域',
  `call_count` BIGINT NULL COMMENT '调用次数',
  `user_count` BIGINT NULL COMMENT '用户数',
  `share_pct` DECIMAL(8,2) NULL COMMENT '占比',
  `growth_pct` DECIMAL(8,2) NULL COMMENT '增速',
  `theme_name` VARCHAR(128) NULL COMMENT '主题',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='应用主体、排行、供应方、需求方、业务应用、区域分组';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_usage_series` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `series_code` VARCHAR(32) NOT NULL COMMENT 'usage_call / usage_detail / theme_call / supplier_call / demander_call / business_call / cumulative',
  `series_name` VARCHAR(128) NULL,
  `period_label` VARCHAR(32) NOT NULL,
  `sort_no` INT NOT NULL,
  `call_count` BIGINT NULL,
  `user_count` BIGINT NULL,
  `cumulative_count` BIGINT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='各条调用趋势';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_call_event` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `event_kind` VARCHAR(32) NOT NULL COMMENT 'app_log / supplier_detail / column_usage / user_track',
  `subject_name` VARCHAR(256) NULL COMMENT '主体',
  `department` VARCHAR(128) NULL COMMENT '部门',
  `app_name` VARCHAR(256) NULL COMMENT '应用',
  `theme_name` VARCHAR(128) NULL COMMENT '主题',
  `api_name` VARCHAR(256) NULL COMMENT '接口',
  `event_time` VARCHAR(32) NULL COMMENT '时间',
  `call_count` BIGINT NULL COMMENT '次数',
  `result_text` VARCHAR(64) NULL COMMENT '结果',
  `field_name` VARCHAR(128) NULL COMMENT '字段名',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='调用日志、字段使用、用户追踪';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_api_probe` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `metric_code` VARCHAR(64) NOT NULL,
  `label` VARCHAR(128) NOT NULL,
  `value_num` DECIMAL(18,4) NULL,
  `status` VARCHAR(32) NULL,
  `probed_at` DATETIME NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='resourceUsageStats、interfaceStatusMetrics';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_graph_node` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `graph_code` VARCHAR(32) NOT NULL COMMENT 'overview_kg / theme_relation',
  `node_id` VARCHAR(64) NOT NULL,
  `name` VARCHAR(256) NOT NULL,
  `category` VARCHAR(64) NULL,
  `category_key` VARCHAR(64) NULL,
  `color` VARCHAR(32) NULL,
  `size` INT NULL,
  `desc_text` VARCHAR(1024) NULL,
  `record_label` VARCHAR(64) NULL COMMENT '记录量',
  `quality` DECIMAL(6,2) NULL COMMENT '质量',
  `source_name` VARCHAR(256) NULL COMMENT '来源',
  `user_label` VARCHAR(64) NULL COMMENT '用户',
  `call_label` VARCHAR(64) NULL COMMENT '调用',
  `related_nodes` JSON NULL COMMENT '关联节点',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='两张关系图的点';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_resource_link` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `graph_code` VARCHAR(32) NOT NULL,
  `src_id` VARCHAR(64) NOT NULL,
  `dst_id` VARCHAR(64) NOT NULL,
  `relation` VARCHAR(64) NULL,
  `strength` DECIMAL(8,4) NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='两张关系图的边';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_block_json` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `block_code` VARCHAR(32) NOT NULL COMMENT 'overview_classify / semantic_theme / partition / big_data_center；本叶不插行',
  `payload_json` JSON NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='不能由行汇总出来的整块';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_entity_year` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `entity_type` VARCHAR(32) NOT NULL,
  `stat_year` SMALLINT NOT NULL,
  `row_count` BIGINT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='entityStock 快照。Java 能直连久新时不读这张表';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`gapfill_dr_column_catalog` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `calc_batch_id` VARCHAR(64) NOT NULL,
  `generated_at` DATETIME NOT NULL,
  `fill_method` VARCHAR(32) NOT NULL,
  `table_name` VARCHAR(128) NOT NULL,
  `column_name` VARCHAR(128) NOT NULL,
  `ordinal` INT NOT NULL,
  `data_type` VARCHAR(64) NULL,
  `column_comment` VARCHAR(512) NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='columnCatalog 快照。禁止手填字段名；现网 131 列由灌数叶写入';
