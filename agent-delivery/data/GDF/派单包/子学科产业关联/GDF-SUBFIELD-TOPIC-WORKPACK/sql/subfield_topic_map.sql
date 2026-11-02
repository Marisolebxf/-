-- SYSINT-06-19-L01
-- 产线映射表。表名沿用中台 subfield_topic_map，落在 gkxlumenx_dim。
-- 本文件只给建表语句。不要在 demo_gkxlumenx_* 执行，不要另开库。
-- 脚本不建表。表不存在时脚本退出码 4。
-- 排在技术节点产业映射之后。同步只填 subfield_id、中文名、版本和 synced_at，node_id 为空。
-- 关联后再写产业节点。同一子学科挂多个集群时各写一行，所以主键是 id。

CREATE TABLE IF NOT EXISTS `gkxlumenx_dim`.`subfield_topic_map` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '自增主键。同一子学科多集群时一行一个集群',
  `subfield_id` VARCHAR(64) NOT NULL COMMENT '子学科 id，来自本侧 SUBFIELD_CATALOG',
  `name_zh` VARCHAR(200) NOT NULL COMMENT '中文名。本表没有英文字段',
  `data_version` VARCHAR(64) NULL COMMENT '目录数据版本',
  `synced_at` DATETIME NOT NULL COMMENT '本侧最近一次同步时间',
  `node_id` VARCHAR(64) NULL COMMENT '本侧产业节点。未关联为空',
  `node_name` VARCHAR(200) NULL COMMENT '产业节点名称',
  `industry_id` VARCHAR(64) NULL COMMENT '产业 id',
  `industry_name` VARCHAR(200) NULL COMMENT '产业名称',
  `cluster_id` VARCHAR(64) NULL COMMENT '集群 id，取 CL-*',
  `cluster_name` VARCHAR(200) NULL COMMENT '集群名称',
  `model_name` VARCHAR(128) NULL COMMENT '关联时的模型名。未关联为空',
  `linked_at` DATETIME NULL COMMENT '关联写入时间。未关联为空',
  `fail_reason` VARCHAR(500) NULL COMMENT '该批关联失败原因。只写在本批尚未关联的行上',
  PRIMARY KEY (`id`),
  KEY `idx_subfield` (`subfield_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='子学科与产业节点映射。先同步目录，再人工触发关联';
