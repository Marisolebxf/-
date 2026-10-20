-- ============================================================
-- ODS 贴源表建表脚本 · 补遗 5 张（v3.1.6 自查发现漏建）
-- 目标库：gkxlumenx_ods @ 10.50.11.76:3306
-- 结构真源：三方源库 gkx @ 183.240.141.251:3318（information_schema 实测 2026-10-20）
-- 背景：02 v3.1.6 清单复核发现首批建表漏列本 5 张（招投标 2 张 + 国外 3 张）
-- 生成：agent:data 协助 徐滕强 · 2026-10-20
-- ============================================================

-- 1. 招投标采购代理出库（42,033 行）
CREATE TABLE IF NOT EXISTS `dwd_bid_purchase_agency_out` (
  `dwd_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'dwd_id',
  `u_id` varchar(255) NOT NULL COMMENT '公告唯一标识id',
  `company_id` varchar(255) NOT NULL COMMENT '机构id',
  `company_name` varchar(255) DEFAULT NULL COMMENT '机构名称',
  `credit_no` varchar(255) DEFAULT NULL COMMENT '统一社会信用代码',
  `project_number` varchar(255) DEFAULT NULL COMMENT '项目编号',
  `project_name` text COMMENT '项目名称',
  `relate_type` double DEFAULT NULL COMMENT '枚举判断',
  `data_source` varchar(255) NOT NULL COMMENT '数据来源',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段：创建时间',
  `updated_time` datetime NOT NULL COMMENT '技术字段：更新时间',
  `creater` varchar(100) DEFAULT NULL COMMENT '技术字段：新增操作员',
  `updater` varchar(100) DEFAULT NULL COMMENT '技术字段：更新操作员',
  `table_data_source` varchar(100) DEFAULT NULL COMMENT '技术字段：数据来源',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0未删除,1已删除',
  `operator_remarks` varchar(100) DEFAULT NULL COMMENT '技术字段：操作备注',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0新增,1修改,2补齐',
  PRIMARY KEY (`dwd_id`),
  KEY `idx_bpao_u_id` (`u_id`),
  KEY `idx_bpao_company_name` (`company_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='招投标采购代理出库表（同名同构镜像 gkx）';

-- 2. 招投标标的物出库（41,187 行）
CREATE TABLE IF NOT EXISTS `dwd_bid_target_item_out` (
  `dwd_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'dwd_id',
  `u_id` varchar(255) NOT NULL COMMENT '公告唯一标识id',
  `project_number` text COMMENT '项目编号',
  `project_name` text COMMENT '项目名称',
  `amount_unit` varchar(255) DEFAULT NULL COMMENT '金额单位',
  `bid_item_name` text COMMENT '招标项目名称',
  `bid_section_number` varchar(255) DEFAULT NULL COMMENT '标段编号',
  `brand` varchar(255) DEFAULT NULL COMMENT '品牌',
  `model` varchar(255) DEFAULT NULL COMMENT '型号',
  `project_content` varchar(255) DEFAULT NULL COMMENT '项目内容',
  `quantity` double DEFAULT NULL COMMENT '数量',
  `service_content` text COMMENT '服务内容',
  `standard_product_name` varchar(255) DEFAULT NULL COMMENT '标准产品名称',
  `target_item_name` text COMMENT '标的物名称',
  `target_item_type` varchar(255) DEFAULT NULL COMMENT '标的物类型',
  `unit_price_amount` double DEFAULT NULL COMMENT '单价金额',
  `data_source` varchar(255) NOT NULL COMMENT '数据来源',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段：创建时间',
  `updated_time` datetime NOT NULL COMMENT '技术字段：更新时间',
  `creater` varchar(100) DEFAULT NULL COMMENT '技术字段：新增操作员',
  `updater` varchar(100) DEFAULT NULL COMMENT '技术字段：更新操作员',
  `table_data_source` varchar(100) DEFAULT NULL COMMENT '技术字段：数据来源',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0未删除,1已删除',
  `operator_remarks` varchar(100) DEFAULT NULL COMMENT '技术字段：操作备注',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0新增,1修改,2补齐',
  PRIMARY KEY (`dwd_id`),
  UNIQUE KEY `uk_u_id` (`u_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='招投标标的物出库表（同名同构镜像 gkx）';

-- 3. 国外高管（19,920 行）
CREATE TABLE IF NOT EXISTS `dwd_forg_executive_info` (
  `dwd_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'dwd_id',
  `org_id` varchar(64) DEFAULT NULL COMMENT '机构id',
  `executives_name` varchar(98) DEFAULT NULL COMMENT '高管姓名',
  `executives_position` varchar(114) DEFAULT NULL COMMENT '高管职位',
  `org_name` varchar(254) DEFAULT NULL COMMENT '机构名称',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `source_table` varchar(64) DEFAULT NULL COMMENT '数据来源表',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段：创建时间',
  `updated_time` datetime NOT NULL COMMENT '技术字段：更新时间',
  `creater` varchar(100) DEFAULT NULL COMMENT '技术字段：新增操作员',
  `updater` varchar(100) DEFAULT NULL COMMENT '技术字段：更新操作员',
  `table_data_source` varchar(100) DEFAULT NULL COMMENT '技术字段：数据来源',
  `operator_remarks` varchar(100) DEFAULT NULL COMMENT '技术字段：操作备注',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0未删除,1已删除',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0新增,1修改,2补齐',
  PRIMARY KEY (`dwd_id`),
  KEY `idx_fei_org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外高管信息（同名同构镜像 gkx）';

-- 4. 国外经营/产品（19,823 行）
CREATE TABLE IF NOT EXISTS `dwd_forg_product_info` (
  `dwd_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'dwd_id',
  `org_id` varchar(64) DEFAULT NULL COMMENT '机构id',
  `org_name` varchar(254) DEFAULT NULL COMMENT '机构名称',
  `description` mediumtext COMMENT '描述',
  `main_products` mediumtext COMMENT '主要产品',
  `main_activities` mediumtext COMMENT '公司主营业务',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `source_table` varchar(64) DEFAULT NULL COMMENT '数据来源表',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段：创建时间',
  `updated_time` datetime NOT NULL COMMENT '技术字段：更新时间',
  `creater` varchar(100) DEFAULT NULL COMMENT '技术字段：新增操作员',
  `updater` varchar(100) DEFAULT NULL COMMENT '技术字段：更新操作员',
  `table_data_source` varchar(100) DEFAULT NULL COMMENT '技术字段：数据来源',
  `operator_remarks` varchar(100) DEFAULT NULL COMMENT '技术字段：操作备注',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0未删除,1已删除',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0新增,1修改,2补齐',
  PRIMARY KEY (`dwd_id`),
  KEY `idx_fpi_org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外经营/产品信息（同名同构镜像 gkx）';

-- 5. 国外股东（39,494 行）
CREATE TABLE IF NOT EXISTS `dwd_forg_shareholder_info` (
  `dwd_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'dwd_id',
  `org_id` varchar(64) DEFAULT NULL COMMENT '机构id',
  `owners_id` varchar(72) DEFAULT NULL COMMENT '股东id',
  `org_name` varchar(154) DEFAULT NULL COMMENT '机构名称',
  `owners_name` varchar(180) DEFAULT NULL COMMENT '股东名称',
  `ownership_percentage` decimal(20,2) DEFAULT NULL COMMENT '股东直接持股比例(%)',
  `owners_country_code` varchar(64) DEFAULT NULL COMMENT '股东国家代码',
  `owners_country` varchar(64) DEFAULT NULL COMMENT '股东国家',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `source_table` varchar(64) DEFAULT NULL COMMENT '数据来源表',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段：创建时间',
  `updated_time` datetime NOT NULL COMMENT '技术字段：更新时间',
  `creater` varchar(100) DEFAULT NULL COMMENT '技术字段：新增操作员',
  `updater` varchar(100) DEFAULT NULL COMMENT '技术字段：更新操作员',
  `table_data_source` varchar(100) DEFAULT NULL COMMENT '技术字段：数据来源',
  `operator_remarks` varchar(100) DEFAULT NULL COMMENT '技术字段：操作备注',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0未删除,1已删除',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0新增,1修改,2补齐',
  PRIMARY KEY (`dwd_id`),
  KEY `idx_fsi_org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外股东信息（同名同构镜像 gkx）';
