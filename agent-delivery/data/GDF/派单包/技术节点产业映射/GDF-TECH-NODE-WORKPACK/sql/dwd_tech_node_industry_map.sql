-- SYSINT-06-20-L01
-- 产线映射表。表名沿用中台 dwd_tech_node_industry_map，落在 gkxlumenx_dwd。
-- 本文件只给建表语句。不要在 demo_gkxlumenx_* 执行，不要另开库。
-- 脚本不建表。表不存在时脚本退出码 4。

CREATE TABLE IF NOT EXISTS `gkxlumenx_dwd`.`dwd_tech_node_industry_map` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `technology_node_id` VARCHAR(64) NOT NULL,
  `name_zh` VARCHAR(200) NOT NULL,
  `name_en` VARCHAR(200) NULL,
  `data_version` VARCHAR(64) NULL,
  `synced_at` DATETIME NOT NULL,
  `node_id` VARCHAR(64) NULL,
  `node_name` VARCHAR(200) NULL,
  `industry_id` VARCHAR(64) NULL,
  `industry_name` VARCHAR(200) NULL,
  `cluster_id` VARCHAR(64) NULL,
  `cluster_name` VARCHAR(200) NULL,
  `model_name` VARCHAR(128) NULL,
  `linked_at` DATETIME NULL,
  `fail_reason` VARCHAR(500) NULL,
  PRIMARY KEY (`id`),
  KEY `idx_technology_node` (`technology_node_id`),
  KEY `idx_node` (`node_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
