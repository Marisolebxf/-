-- SHOW CREATE @ demo_gkxlumenx_ods · DATA-SVC-STORAGE-S2-L01
-- host via ENTAN_MYSQL_* · zero write to gkxlumenx_ods

-- === dwd_org_base_info ===
CREATE TABLE `dwd_org_base_info` (
  `_demo_id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name_cn` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `external_id` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `province` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `city` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `area` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `address` text COLLATE utf8mb4_general_ci,
  `addr_lng` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `addr_lat` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `postal_code` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` text COLLATE utf8mb4_general_ci,
  `lerep` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `reg_status` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `registration_org` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `incorporation_year` decimal(20,0) DEFAULT NULL,
  `incorporation_date` date DEFAULT NULL,
  `start_date` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `end_date` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `org_type` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `listing_status` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `listing_date` date DEFAULT NULL,
  `registered_capital_value` decimal(20,2) DEFAULT NULL,
  `capital_currency` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `industry` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `industry_l1_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `industry_l1_code` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `industry_l2_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `industry_l2_code` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `industry_l3_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `industry_l3_code` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `industry_l4_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `industry_l4_code` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone_num` text COLLATE utf8mb4_general_ci,
  `org_size` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `data_source` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`_demo_id`),
  KEY `idx_org_id` (`org_id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- === dwd_org_org_product_info ===
CREATE TABLE `dwd_org_org_product_info` (
  `_demo_id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name_cn` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `external_id` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `main_activities` text COLLATE utf8mb4_general_ci,
  `description` text COLLATE utf8mb4_general_ci,
  `main_prod` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `data_source` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`_demo_id`),
  KEY `idx_org_id` (`org_id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- === dwd_org_tech_tag ===
CREATE TABLE `dwd_org_tech_tag` (
  `_demo_id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `org_tag` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `data_source` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`_demo_id`),
  KEY `idx_org_id` (`org_id`)
) ENGINE=InnoDB AUTO_INCREMENT=139 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- === dwd_org_shareholder_info ===
CREATE TABLE `dwd_org_shareholder_info` (
  `_demo_id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name_cn` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `external_id` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `inv_org_id` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `owners_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `owners_type` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ownership_percentage` decimal(20,2) DEFAULT NULL,
  `data_source` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`_demo_id`),
  KEY `idx_org_id` (`org_id`)
) ENGINE=InnoDB AUTO_INCREMENT=271 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
