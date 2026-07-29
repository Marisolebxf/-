-- 行政地区码表（企业所属地区全国树）
-- 目标：MySQL gkxlumenx_dim.code_region
-- 源：PostgreSQL dim.admin_division（PG 无独立 code_region 表）
-- 迁移日：2026-07-29
-- 映射：admin_code→code, COALESCE(parent_code,'0')→parent, name→name/fulltitle,
--       level→level(字符串), CONCAT(lng,lat)→lnglat

CREATE TABLE IF NOT EXISTS `gkxlumenx_dim`.`code_region` (
  `code` varchar(20) NOT NULL COMMENT '行政区划代码',
  `parent` varchar(20) NOT NULL DEFAULT '0' COMMENT '父级代码，顶级为 0',
  `name` varchar(128) NOT NULL COMMENT '名称',
  `level` varchar(8) NOT NULL COMMENT '层级：1国家/省 2市 3区县（字符串，对齐接口）',
  `fulltitle` varchar(256) DEFAULT NULL COMMENT '全称',
  `zipcode` varchar(16) DEFAULT NULL COMMENT '邮编',
  `lnglat` varchar(64) DEFAULT NULL COMMENT '经度,纬度',
  `tel` varchar(16) DEFAULT NULL COMMENT '区号',
  `area` decimal(12,2) DEFAULT NULL COMMENT '面积',
  `people` decimal(12,2) DEFAULT NULL COMMENT '人口（万）',
  PRIMARY KEY (`code`),
  KEY `idx_code_region_parent` (`parent`),
  KEY `idx_code_region_level` (`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='行政地区码表（企业所属地区树；源 PG dim.admin_division）';
