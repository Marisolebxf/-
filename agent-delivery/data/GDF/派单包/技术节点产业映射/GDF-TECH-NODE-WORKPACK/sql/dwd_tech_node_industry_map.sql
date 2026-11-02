-- SYSINT-06-20-L01
-- 产线映射表。表名沿用中台 dwd_tech_node_industry_map，落在 gkxlumenx_dwd。
-- 本文件只给建表语句。不要在 demo_gkxlumenx_* 执行，不要另开库。
-- 脚本不建表。表不存在时脚本退出码 4。
-- 同步只填 technology_node_id、名称、版本和 synced_at，node_id 为空。
-- 关联后再写产业节点。同一技术节点挂多个集群时各写一行，所以主键是 id。

CREATE TABLE IF NOT EXISTS `gkxlumenx_dwd`.`dwd_tech_node_industry_map` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '自增主键。同一技术节点多集群时一行一个集群',
  `technology_node_id` VARCHAR(64) NOT NULL COMMENT '久新 ads_technology_profile.technology_node_id',
  `name_zh` VARCHAR(200) NOT NULL COMMENT '中文名，来自 technology_name_zh。空则存空串，不抄英文',
  `name_en` VARCHAR(200) NULL COMMENT '英文名，来自 technology_name_en',
  `data_version` VARCHAR(64) NULL COMMENT '久新 data_version',
  `synced_at` DATETIME NOT NULL COMMENT '本侧最近一次同步时间',
  `node_id` VARCHAR(64) NULL COMMENT '本侧产业节点。未关联为空',
  `node_name` VARCHAR(200) NULL COMMENT '产业节点名称',
  `industry_id` VARCHAR(64) NULL COMMENT '产业 id',
  `industry_name` VARCHAR(200) NULL COMMENT '产业名称',
  `cluster_id` VARCHAR(64) NULL COMMENT '集群 id，取 CL-*',
  `cluster_name` VARCHAR(200) NULL COMMENT '集群名称',
  `model_name` VARCHAR(128) NULL COMMENT '关联时的向量模型版本。未关联为空',
  `linked_at` DATETIME NULL COMMENT '关联写入时间。未关联为空',
  `fail_reason` VARCHAR(500) NULL COMMENT '该批关联失败原因。只写在本批尚未关联的行上',
  PRIMARY KEY (`id`),
  KEY `idx_technology_node` (`technology_node_id`),
  KEY `idx_node` (`node_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='技术节点与产业节点映射。先同步目录，再人工触发关联';
