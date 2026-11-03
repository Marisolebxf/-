-- SVC Demo 空表 CREATE（DATA-SVC-STORAGE-S3-L02）
-- 目标库：仅 demo_gkxlumenx_dwd / demo_gkxlumenx_ads
-- 禁止：DROP demo_gkxlumenx_ods 约定 33 表；新建 ODS 实例；写正式 gkxlumenx_*
-- 本文件不灌数。F-SEED 首刀执行本脚本后，再按 50100 按钮灌数。
-- 建库不在本文件：须先跑 demo-algo-ent-analysis/scripts/mysql/create_demo_dbs.sql。
-- 细表 status=draft。org_id collation 与 ENT hang 对齐 utf8mb4_general_ci。

-- ---------------------------------------------------------------------------
-- DWD（库须已存在；建库见 demo-algo-ent-analysis/scripts/mysql/create_demo_dbs.sql）
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`svc_org_circle` (
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

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`svc_org_graph_hang` (
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

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`svc_org_finance_event` (
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
  UNIQUE KEY `uk_svc_finance_event` (`org_id`, `event_id`, `event_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='投融资事件 hang；Q-SVC-006 允许 0 行';

-- ---------------------------------------------------------------------------
-- ADS（库须已存在；建库见 demo-algo-ent-analysis/scripts/mysql/create_demo_dbs.sql）
-- ---------------------------------------------------------------------------
-- 名单卡面（DATA-SVC-STORAGE-CARD-L02 · 淮政玮选 B）。不是 svc_org_base。
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`svc_org_card` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name_cn` VARCHAR(255) NULL COMMENT '展示投影 ODS name_cn',
  `province` VARCHAR(64) NULL,
  `city` VARCHAR(64) NULL,
  `area` VARCHAR(64) NULL COMMENT '区县；优先 ODS area，live 仅 district 则写入本列',
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

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`svc_metric_fact` (
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

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`svc_metric_series` (
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

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`svc_metric_dist` (
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

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`svc_region_dist` (
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

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`svc_chain_gap` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `stage_code` VARCHAR(64) NOT NULL,
  `stage_name` VARCHAR(128) NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `org_count_in_stage` INT NULL,
  `avg_depth` DECIMAL(10,4) NULL,
  `runtime_flag` VARCHAR(16) NULL COMMENT 'Q-SVCCHAIN-03: blank / weak / bottleneck',
  `q061_score` DECIMAL(10,4) NULL COMMENT '对照列，不参与运行时',
  `q061_pending_client` TINYINT(1) NOT NULL DEFAULT 1,
  `gap_items` JSON NULL,
  `calc_batch_id` VARCHAR(64) NULL,
  `model_version` VARCHAR(64) NULL,
  `weights` JSON NULL,
  `ext` JSON NULL,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_chain_gap` (`stage_code`, `calc_batch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='SVC_SERVICE_CHAIN_GAP；运行时 Q-SVCCHAIN-03';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`svc_relation_chain` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `density` DECIMAL(10,6) NULL,
  `centrality` DECIMAL(10,6) NULL,
  `hop_level` INT NULL,
  `calc_batch_id` VARCHAR(64) NULL,
  `model_version` VARCHAR(64) NULL,
  `weights` JSON NULL,
  `ext` JSON NULL,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_svc_rel_batch` (`calc_batch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='SVC_SERVICE_RELATION_CHAIN；Q062';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`svc_tech_power_score` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model_id` VARCHAR(64) NOT NULL COMMENT 'SVC_*_TECH_POWER ×6',
  `service_type` VARCHAR(32) NULL,
  `score` DECIMAL(10,4) NULL,
  `dimension_scores` JSON NULL COMMENT 'Q060 五维等权',
  `calc_batch_id` VARCHAR(64) NULL,
  `model_version` VARCHAR(64) NULL,
  `weights` JSON NULL,
  `ext` JSON NULL,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_tech_power` (`org_id`, `model_id`, `calc_batch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='六类技术力；Q060';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`svc_attraction_recommend` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `attraction_index` DECIMAL(10,4) NULL,
  `dimension_scores` JSON NULL,
  `priority_level` VARCHAR(16) NULL,
  `rank_no` INT NULL,
  `recommend_reason` TEXT NULL,
  `calc_batch_id` VARCHAR(64) NULL,
  `model_version` VARCHAR(64) NULL,
  `weights` JSON NULL,
  `ext` JSON NULL,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_attract` (`org_id`, `calc_batch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='SVC_ATTRACTION_RECOMMEND；Q063';

CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`svc_cultivation_recommend` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cultivation_index` DECIMAL(10,4) NULL,
  `dimension_scores` JSON NULL,
  `growth_stage` VARCHAR(32) NULL,
  `priority_level` VARCHAR(16) NULL,
  `advice` TEXT NULL,
  `calc_batch_id` VARCHAR(64) NULL,
  `model_version` VARCHAR(64) NULL,
  `weights` JSON NULL,
  `ext` JSON NULL,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_svc_cult` (`org_id`, `calc_batch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='SVC_CULTIVATION_RECOMMEND；Q063';
