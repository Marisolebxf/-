-- Snapshot: SHOW CREATE TABLE on supplier inbound DB `gkx` (READ ONLY).
-- Host: 183.240.141.251:3318  database=gkx  (NOT demo_gkxlumenx_dwd, NOT gkxlumenx_dwd)
-- Task: DATA-CHAIN-INDANA-STORAGE-L01
-- These six tables are the inbound / 供应方 dwd_* 现表.
-- Project DWD physical names = strip the dwd_ prefix (industry_analysis_*).
-- Demo demo_gkxlumenx_dwd did NOT contain these tables on 2026-08-16 probe;
-- copy structure from this snapshot until Demo DWD SHOW CREATE is available.
-- Do NOT CREATE/ALTER gkxlumenx_dwd from this file.

USE `gkx`;

-- ===== gkx.dwd_industry_analysis_documents =====
CREATE TABLE `dwd_industry_analysis_documents` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `document_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件ID 唯一标识符',
  `format` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件格式',
  `update_date` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '最后一次更新日期',
  `creation_date` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件创建日期',
  `source_type_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '信息来源类型名称',
  `source_type_code` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '信息来源类型代码',
  `source_code` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '信息来源代码',
  `source_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '信息来源名称',
  `pages` int DEFAULT NULL COMMENT '报告页数',
  `size` bigint NOT NULL COMMENT '文件字节大小',
  `title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件标题',
  `body` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '正文',
  `abstract` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '文件摘要',
  `language` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '语言',
  `file_link` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '文件链接',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段，数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '技术字段，该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `operator_remarks` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，操作记录',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '逻辑删除标识，0未删除，1已删除',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段，逻辑删除标识，0新增，1更新',
  PRIMARY KEY (`pk_id`),
  UNIQUE KEY `uk_document_id` (`document_id`),
  KEY `idx_creation_date` (`creation_date`),
  KEY `idx_source_code` (`source_code`),
  KEY `idx_language` (`language`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文档信息';

-- ===== gkx.dwd_industry_analysis_companies =====
CREATE TABLE `dwd_industry_analysis_companies` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `document_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件ID 唯一标识符',
  `company_id` bigint DEFAULT NULL COMMENT '公司代码',
  `company_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '公司英文名称',
  `company_name_local` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '公司本地名称',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段，数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '技术字段，该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `operator_remarks` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，操作记录',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '逻辑删除标识，0未删除，1已删除',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段，逻辑删除标识，0新增，1更新',
  PRIMARY KEY (`pk_id`),
  UNIQUE KEY `uk_doc_company` (`document_id`,`company_id`),
  KEY `idx_document_id` (`document_id`),
  KEY `idx_company_id` (`company_id`),
  KEY `idx_company_name_local` (`company_name_local`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文档关联公司';

-- ===== gkx.dwd_industry_analysis_industries =====
CREATE TABLE `dwd_industry_analysis_industries` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `document_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件ID 唯一标识符',
  `industry_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '行业代码，如有',
  `industry_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '行业名称，如有',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段，数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '技术字段，该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `operator_remarks` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，操作记录',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '逻辑删除标识，0未删除，1已删除',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段，逻辑删除标识，0新增，1更新',
  PRIMARY KEY (`pk_id`),
  UNIQUE KEY `uk_doc_industry` (`document_id`,`industry_code`),
  KEY `idx_document_id` (`document_id`),
  KEY `idx_industry_code` (`industry_code`),
  KEY `idx_industry_name` (`industry_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3048 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文档关联行业';

-- ===== gkx.dwd_industry_analysis_topics =====
CREATE TABLE `dwd_industry_analysis_topics` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `document_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件ID 唯一标识符',
  `topic_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '主题名字',
  `topic_code` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '主题代码',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段，数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '技术字段，该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `operator_remarks` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，操作记录',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '逻辑删除标识，0未删除，1已删除',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段，逻辑删除标识，0新增，1更新',
  PRIMARY KEY (`pk_id`),
  UNIQUE KEY `uk_doc_topic` (`document_id`,`topic_code`),
  KEY `idx_document_id` (`document_id`),
  KEY `idx_topic_name` (`topic_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1053 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文档关联主题';

-- ===== gkx.dwd_industry_analysis_content_types =====
CREATE TABLE `dwd_industry_analysis_content_types` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `document_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件ID 唯一标识符',
  `name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '报告类型名称',
  `code` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '报告类型代码',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段，数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '技术字段，该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `operator_remarks` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，操作记录',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '逻辑删除标识，0未删除，1已删除',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段，逻辑删除标识，0新增，1更新',
  PRIMARY KEY (`pk_id`),
  UNIQUE KEY `uk_doc_code` (`document_id`,`code`),
  KEY `idx_document_id` (`document_id`),
  KEY `idx_code` (`code`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文档内容类型';

-- ===== gkx.dwd_industry_analysis_countries =====
CREATE TABLE `dwd_industry_analysis_countries` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `document_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件ID 唯一标识符',
  `country_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '国家代码',
  `country_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '国家名字',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段，数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '技术字段，该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `operator_remarks` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '技术字段，操作记录',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '逻辑删除标识，0未删除，1已删除',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段，逻辑删除标识，0新增，1更新',
  PRIMARY KEY (`pk_id`),
  UNIQUE KEY `uk_doc_country` (`document_id`,`country_code`),
  KEY `idx_document_id` (`document_id`),
  KEY `idx_country_code` (`country_code`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文档关联国家';
