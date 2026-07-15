-- ============================================================================
-- Isolated sandbox: third-party MySQL schema dump for database `gkx`
-- Source: user paste (Navicat/DBeaver style `-- gkx.<table> definition`)
-- Purpose: structure analysis ONLY — do NOT load into demo_gdf_data /
--          algo POC (117.50...) / production ADS pipelines.
-- Extracted-from-transcript: 1f32dbcf-d513-40f5-821f-ee2c7be0473f
-- ============================================================================

-- gkx.dwd_author_affiliation definition

CREATE TABLE `dwd_author_affiliation` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `auid` bigint NOT NULL COMMENT '作者ID',
  `affiliation_id` bigint DEFAULT NULL COMMENT '机构ID',
  `afid` bigint DEFAULT NULL COMMENT '机构显示ID',
  `affiliation_id_parent` bigint DEFAULT NULL COMMENT '父机构ID',
  `preferred_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构标准名称',
  `afdispname` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构显示名称',
  `sort_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构排序名称',
  `address_part` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '详细地址',
  `city` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '城市',
  `state` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '州/省份',
  `country` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '国家',
  `country_tag` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '国家编码',
  `postal_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '邮政编码',
  `type_afid` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构类型：dept/parent',
  `relationship` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '关系：author/derived',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1648 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='作者-机构关联表';

-- gkx.dwd_author_en_paper_rel definition

CREATE TABLE `dwd_author_en_paper_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `author_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者记录的业务唯一标识。',
  `paper_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `paper_doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_daepr_author_id_paper_id` (`author_id`,`paper_id`) USING BTREE,
  KEY `idx_daepr_author_id` (`author_id`) USING BTREE,
  KEY `idx_daepr_paper_id` (`paper_id`) USING BTREE,
  KEY `idx_daepr_paper_doi` (`paper_doi`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='科技人才-外文论文关联表';

-- gkx.dwd_author_en_project_rel definition

CREATE TABLE `dwd_author_en_project_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `author_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者记录的业务唯一标识。',
  `project_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '项目记录的唯一主键标识。',
  `project_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '项目在管理系统中的编号。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_daepr_author_id_project_id` (`author_id`,`project_id`) USING BTREE,
  KEY `idx_daepr_author_id` (`author_id`) USING BTREE,
  KEY `idx_daepr_project_id` (`project_id`) USING BTREE,
  KEY `idx_daepr_project_number` (`project_number`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='科技人才-国外项目关联表';

-- gkx.dwd_author_en_report_rel definition

CREATE TABLE `dwd_author_en_report_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `author_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者记录的业务唯一标识。',
  `report_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '外文报告记录的唯一主键标识。',
  `report_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '报告在来源系统或机构中的编号。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_daerr_author_id_report_id` (`author_id`,`report_id`) USING BTREE,
  KEY `idx_daerr_author_id` (`author_id`) USING BTREE,
  KEY `idx_daerr_report_id` (`report_id`) USING BTREE,
  KEY `idx_daerr_report_number` (`report_number`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='科技人才-外文报告关联表';

-- gkx.dwd_author_foreign_org_base_info_rel definition

CREATE TABLE `dwd_author_foreign_org_base_info_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `author_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者记录的业务唯一标识。',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构身份唯一id，用于关联其它表。',
  `base_external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构外部唯一标识',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_dafobir_author_id_org_id` (`author_id`,`org_id`) USING BTREE,
  KEY `idx_dafobir_author_id` (`author_id`) USING BTREE,
  KEY `idx_dafobir_org_id` (`org_id`(191)) USING BTREE,
  KEY `idx_dafobir_base_external_id` (`base_external_id`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='科技人才-国外机构关联表';

-- gkx.dwd_author_global_patent_rel definition

CREATE TABLE `dwd_author_global_patent_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `author_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者记录的业务唯一标识。',
  `patent_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利记录唯一标识，用于关联专利明细。',
  `publication_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利公开或公告时使用的文献编号。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_dagpr_author_id_patent_id` (`author_id`,`patent_id`) USING BTREE,
  KEY `idx_dagpr_author_id` (`author_id`) USING BTREE,
  KEY `idx_dagpr_patent_id` (`patent_id`) USING BTREE,
  KEY `idx_dagpr_publication_number` (`publication_number`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='科技人才-全球专利关联表';

-- gkx.dwd_author_info definition

CREATE TABLE `dwd_author_info` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `auid` bigint NOT NULL COMMENT '作者唯一ID',
  `orcid` varchar(64) DEFAULT NULL COMMENT 'ORCID 标识',
  `orcid_matching_type` varchar(64) DEFAULT NULL COMMENT 'ORCID匹配类型',
  `given_name` varchar(255) DEFAULT NULL COMMENT '名',
  `surname` varchar(255) DEFAULT NULL COMMENT '姓',
  `indexed_name` varchar(255) DEFAULT NULL COMMENT '索引名称',
  `initials` varchar(32) DEFAULT NULL COMMENT '姓名缩写',
  `alias_status` varchar(32) DEFAULT NULL COMMENT '别名状态',
  `name_variants` varchar(500) DEFAULT NULL COMMENT '姓名别名列表（逗号分隔）',
  `history_ids` varchar(500) DEFAULT NULL COMMENT '历史ID列表（逗号分隔）',
  `email` varchar(255) DEFAULT NULL COMMENT '邮箱',
  `email_type` varchar(32) DEFAULT NULL COMMENT '邮箱类型',
  `asjc_list` varchar(500) DEFAULT NULL COMMENT 'ASJC学科代码列表，逗号分隔',
  `asjc_freq_list` varchar(500) DEFAULT NULL COMMENT 'ASJC频次列表，逗号分隔',
  `subjabbr_list` varchar(500) DEFAULT NULL COMMENT '学科缩写列表，逗号分隔',
  `subjabbr_freq_list` varchar(500) DEFAULT NULL COMMENT '学科缩写频次，逗号分隔',
  `n_affiliation_current` int DEFAULT '0' COMMENT '当前机构数量',
  `current_affiliations` varchar(500) DEFAULT NULL COMMENT '当前有效机构ID列表，逗号分隔',
  `current_affiliations_parent` varchar(500) DEFAULT NULL COMMENT '父机构ID列表，逗号分隔',
  `corrupt_xml` tinyint DEFAULT '0' COMMENT 'XML文件是否损坏（1=损坏，0=正常）',
  `xmlsize` int DEFAULT NULL COMMENT 'XML文件大小',
  `datetime_max` varchar(32) DEFAULT NULL COMMENT '数据最新日期',
  `suppress` tinyint DEFAULT '0' COMMENT '是否隐藏',
  `type` varchar(32) DEFAULT NULL COMMENT '作者类型',
  `curated` tinyint DEFAULT '0' COMMENT '是否经过人工校准',
  `curtype` varchar(255) DEFAULT NULL COMMENT '校准类型',
  `cur_source` varchar(255) DEFAULT NULL COMMENT '校准来源',
  `cur_timestamp` varchar(255) DEFAULT NULL COMMENT '校准时间戳',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_auid` (`auid`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Scopus作者元数据表';

-- gkx.dwd_author_org_base_info_rel definition

CREATE TABLE `dwd_author_org_base_info_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `author_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者记录的业务唯一标识。',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构身份唯一id，用于关联其它表。',
  `base_external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构外部唯一标识',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_daobir_author_id_org_id` (`author_id`,`org_id`) USING BTREE,
  KEY `idx_daobir_author_id` (`author_id`) USING BTREE,
  KEY `idx_daobir_org_id` (`org_id`(191)) USING BTREE,
  KEY `idx_daobir_base_external_id` (`base_external_id`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='科技人才-国内机构关联表';

-- gkx.dwd_author_zh_paper_rel definition

CREATE TABLE `dwd_author_zh_paper_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `author_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者记录的业务唯一标识。',
  `paper_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `paper_doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_dazpr_author_id_paper_id` (`author_id`,`paper_id`) USING BTREE,
  KEY `idx_dazpr_author_id` (`author_id`) USING BTREE,
  KEY `idx_dazpr_paper_id` (`paper_id`) USING BTREE,
  KEY `idx_dazpr_paper_doi` (`paper_doi`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='科技人才-中文论文关联表';

-- gkx.dwd_author_zh_project_rel definition

CREATE TABLE `dwd_author_zh_project_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `author_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者记录的业务唯一标识。',
  `project_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '项目记录的唯一主键标识。',
  `project_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '项目在管理系统中的编号。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_dazpr_author_id_project_id` (`author_id`,`project_id`) USING BTREE,
  KEY `idx_dazpr_author_id` (`author_id`) USING BTREE,
  KEY `idx_dazpr_project_id` (`project_id`) USING BTREE,
  KEY `idx_dazpr_project_number` (`project_number`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='科技人才-国内项目关联表';

-- gkx.dwd_author_zh_report_rel definition

CREATE TABLE `dwd_author_zh_report_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `author_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者记录的业务唯一标识。',
  `report_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '中文报告记录的唯一主键标识。',
  `report_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '报告在来源系统或机构中的编号。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_dazrr_author_id_report_id` (`author_id`,`report_id`) USING BTREE,
  KEY `idx_dazrr_author_id` (`author_id`) USING BTREE,
  KEY `idx_dazrr_report_id` (`report_id`) USING BTREE,
  KEY `idx_dazrr_report_number` (`report_number`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='科技人才-中文报告关联表';

-- gkx.dwd_calculation definition

CREATE TABLE `dwd_calculation` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分子理论计算的内部或来源库唯一标识',
  `molecular_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '化合物、材料或分子的标准英文名称',
  `reference` json DEFAULT NULL COMMENT '支持该条记录的论文、数据库页面或 DOI 等来源信息',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_calculation_molecular_name` (`molecular_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='分子理论计算';

-- gkx.dwd_clinical definition

CREATE TABLE `dwd_clinical` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '疾病或适应症在来源库中的唯一标识',
  `disease_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药物、试验或临床信息关联的疾病名称',
  `phenotype_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '临床表型在标准术语库中的唯一标识',
  `phenotype_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '疾病相关的临床表现、症状或表型名称',
  `associated_gene` json DEFAULT NULL COMMENT '与疾病、表型或多组学结果相关的基因名称',
  `references` json DEFAULT NULL COMMENT '支持该条记录的论文、数据库页面或 DOI 等来源信息',
  `disease_category` json DEFAULT NULL COMMENT '疾病在 ICD、肿瘤分类或其他标准体系中的层级分类',
  `symptoms` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '疾病或临床表型相关的主要症状',
  `related_disease` json DEFAULT NULL COMMENT '与当前疾病存在继发、共病、遗传或机制关联的疾病',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_clinical_disease_name` (`disease_name`) USING BTREE,
  KEY `idx_dwd_clinical_phenotype_id` (`phenotype_id`) USING BTREE,
  KEY `idx_dwd_clinical_phenotype_name` (`phenotype_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='临床信息表';

-- gkx.dwd_clinical_trial definition

CREATE TABLE `dwd_clinical_trial` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '临床试验信息的内部或来源库唯一标识',
  `trial_sponsor` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '临床试验登记记录中的研究标题',
  `disease_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药物、试验或临床信息关联的疾病名称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='临床试验信息表';

-- gkx.dwd_company definition

CREATE TABLE `dwd_company` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品企业对应的内部或来源库唯一标识',
  `firm_name` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品企业、生产企业或许可持有人名称',
  `address` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业注册地址、生产地址或经营地址',
  `duns_number` json DEFAULT NULL COMMENT '企业的 D-U-N-S 编码，用于企业识别和外部数据关联',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='药品企业表';

-- gkx.dwd_company_base definition

CREATE TABLE `dwd_company_base` (
  `id` bigint NOT NULL COMMENT '企业id',
  `name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业名称',
  `english_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业英文名称',
  `registration_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册号',
  `organization_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '组织机构号',
  `credit_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统一信用代码',
  `first_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业类型',
  `registered_capital` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册资本',
  `registered_add` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册地址',
  `scope` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '经营范围',
  `start_date` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '营业期限开始日期',
  `end_date` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '营业期限终止日期',
  `reg_organization` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '登记机关',
  `legal_representative` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '法人姓名',
  `legal_rep_type` int DEFAULT NULL COMMENT '法人类型',
  `approval_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '核准日期',
  `establish_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '成立日期',
  `cancel_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注销日期',
  `status_std` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业状态',
  `display` int DEFAULT NULL COMMENT '企业状态(1:正常存续, 2:注销,3:非工商主体,7:搬迁,8:停业,9:清算,10:其他)',
  `reg_capital_std` decimal(18,6) DEFAULT NULL COMMENT '注册资本金额',
  `unit` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册资本单位',
  `currency` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册资本币种',
  `real_capital` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '实缴资本',
  `real_capital_std` decimal(18,6) DEFAULT NULL COMMENT '实缴资本金额',
  `cancel_reason` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注销原因',
  `ori_reg_city` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册地所在市',
  `ori_reg_district` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册的所在区',
  `ori_reg_province` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册地所在省',
  `reg_xy` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '经度',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='基础信息';

-- gkx.dwd_company_basic_tags definition

CREATE TABLE `dwd_company_basic_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `business_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '业务类型',
  `capital_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业性质',
  `scale_tag` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业规模标签',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='基础属性标签';

-- gkx.dwd_company_branch definition

CREATE TABLE `dwd_company_branch` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `branch_id` bigint DEFAULT NULL COMMENT '分支机构的主体唯一键',
  `branch_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分支机构名称',
  `branch_reg_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分支机构注册号',
  `branch_credit_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分支机构统一信用代码',
  `branch_establish_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分支机构成立日期',
  `branch_company_status` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登记状态',
  `branch_cancel_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '注销日期',
  `is_history` int DEFAULT NULL COMMENT '使用标记(0: 非历史， 1：历史 )',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='分支机构';

-- gkx.dwd_company_brief_tags definition

CREATE TABLE `dwd_company_brief_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `brief` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公司简介摘要',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='企业简介';

-- gkx.dwd_company_change definition

CREATE TABLE `dwd_company_change` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `before` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更前内容',
  `after` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更后内容',
  `date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更日期',
  `change_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更类型(法定代表人变更, 主要人员变更, 经营范围变更, 注册资本变更, 股东信息变更, address, business, lp)',
  `change_type_std` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更类型(法定代表人变更, 主要人员变更, 经营范围变更, 注册资本变更, 股东信息变更)',
  `change_type_detail` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更类型详情',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='工商变更';

-- gkx.dwd_company_contact_tags definition

CREATE TABLE `dwd_company_contact_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `contact` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '联系人信息（联系人姓名，联系方式，类型，信息来源，更新日期，原始链接）',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='企业联系方式';

-- gkx.dwd_company_diy_tags definition

CREATE TABLE `dwd_company_diy_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `diy_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '特色资质标签',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='特色资质标签';

-- gkx.dwd_company_history_name definition

CREATE TABLE `dwd_company_history_name` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `history_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '曾用名',
  `start_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '名称开始使用日期',
  `end_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '名称结束使用日期',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='曾用名';

-- gkx.dwd_company_honor_tags definition

CREATE TABLE `dwd_company_honor_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `association_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '协会标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `award_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '荣誉奖项标签（奖项编码，奖项类型，奖项等级，级别，获奖日期，颁发单位，奖项全称，获奖年份）',
  `certification` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '资质认证（证书名称，证书编号，资质编码，获证年份，级别，状态，有效期起，有效期止，发证日期，发证机构）',
  `city_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '市级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `district_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '区县级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `national_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '国家级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `nonpublic_tags` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '私有标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `park_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '园区级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `permission` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '备案许可（许可事项名称，许可证号，许可类型编码，许可年份，管理层级，状态，有效期起，有效期止，发证日期，审批机关，许可生产范围）',
  `province_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '省级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `rank_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '榜单标签（标签名称，标签编码，年份，级别，具体名次，发布日期，发布机构）',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='企业荣誉标签';

-- gkx.dwd_company_industry_tags definition

CREATE TABLE `dwd_company_industry_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `industry_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业标签（产业编码，产业名称，置信度，环节[环节编码，环节名称，级别，置信度]）',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='产业标签';

-- gkx.dwd_company_license definition

CREATE TABLE `dwd_company_license` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '许可证名称',
  `license_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '许可文件编号',
  `scope` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '许可内容',
  `start_date` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '有效期自',
  `end_date` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '有效期至',
  `organization` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '许可机关',
  `is_history` int DEFAULT NULL COMMENT '状态（0: 有效， 1: 历史）',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='行政许可';

-- gkx.dwd_company_location_tags definition

CREATE TABLE `dwd_company_location_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `reg_province` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '省',
  `reg_city` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '市',
  `reg_district` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '区',
  `reg_xy` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '坐标',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='所在行政区';

-- gkx.dwd_company_nei_code definition

CREATE TABLE `dwd_company_nei_code` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `industry` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '最深一级的行业名称',
  `industry_l1_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '一级行业编码',
  `industry_l1_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '一级行业名称',
  `industry_l2_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '二级行业编码',
  `industry_l2_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '二级行业名称',
  `industry_l3_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '三级行业编码',
  `industry_l3_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '三级行业名称',
  `industry_l4_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '四级行业编码',
  `industry_l4_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '四级行业名称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='国民行业经济分类';

-- gkx.dwd_company_recruit definition

CREATE TABLE `dwd_company_recruit` (
  `id` bigint DEFAULT NULL COMMENT '关联企业基础表主键ID',
  `source_id` varchar(56) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '招聘事件ID',
  `company_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公司名称',
  `city` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '所在城市',
  `district` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '所在区',
  `title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '招聘职称',
  `salary` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '工资',
  `first_class` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '一级分类',
  `second_class` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '二级分类',
  `third_class` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '三级分类',
  `address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '工作地址',
  `start_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '招聘开始日期',
  `end_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '招聘截止日期',
  `education` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '教育',
  `recruit_number` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '招聘人数',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '职位描述',
  `experience` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '经验',
  `type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '招聘类别',
  `company_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公司地址',
  `url_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '外网链接',
  `source` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源：赶集，58....',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`source_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='招聘';

-- gkx.dwd_company_reg_cap_change definition

CREATE TABLE `dwd_company_reg_cap_change` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更类型',
  `date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更日期',
  `before` decimal(18,6) NOT NULL DEFAULT '0.000000' COMMENT '变更前注册资本',
  `after` decimal(18,6) NOT NULL DEFAULT '0.000000' COMMENT '变更后注册资本',
  `unit` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '单位',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='注册资本变更';

-- gkx.dwd_company_shareholder definition

CREATE TABLE `dwd_company_shareholder` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `investor_id` bigint DEFAULT NULL COMMENT '股东id',
  `investor_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '股东名称',
  `investor_type` int NOT NULL DEFAULT '0' COMMENT '股东类型(0:企业,1:个人,2:其他,3:港企,4:事业单位,5:政府机关,6:社会组织,7:工会,8:律师事务所)',
  `investor_detail_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '股东类型',
  `amount` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '投资金额',
  `amount_std` decimal(18,6) NOT NULL DEFAULT '0.000000' COMMENT '投资金额标准化（万元人民币）',
  `share_ratio` decimal(18,6) NOT NULL DEFAULT '0.000000' COMMENT '持股比例',
  `subscribed` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '认缴资金,认缴日期,认缴形式',
  `contributed` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '实缴金额,实缴日期,实缴形式',
  `stock_realcapital` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '实缴出资额',
  `country` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '股东国别',
  `include_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '股东进入日期',
  `remove_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '股东退出日期',
  `is_history` int NOT NULL DEFAULT '0' COMMENT '是否历史股东，0：当前股东，1：历史股东',
  `name_source` int NOT NULL DEFAULT '0' COMMENT '股东来源，0：官网同步，1：变更记录解析，2：其他源补充',
  `stock_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '股东类型',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='股东信息';

-- gkx.dwd_company_staff definition

CREATE TABLE `dwd_company_staff` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `staff_id` bigint NOT NULL DEFAULT '0' COMMENT '主要人员是机构时，该机构的company_id',
  `staff_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '清洗后主要人员名称',
  `staff_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '职位',
  `person_type` int NOT NULL DEFAULT '0' COMMENT 'employee_name类型，1：自然人，0：机构，2：非自然人非机构',
  `start_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主要人员任职开始日期',
  `end_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主要人员任职截止日期',
  `is_history` int NOT NULL DEFAULT '0' COMMENT '是否历史主要人员，0：当前主要人员，1：历史主要人员',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='任职人员';

-- gkx.dwd_company_transition_clean definition

CREATE TABLE `dwd_company_transition_clean` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业名称',
  `before` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '清洗后变更前地址',
  `after` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '清洗后变更后地址',
  `date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更日期',
  `type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更类型',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='注册地址变更';

-- gkx.dwd_crystal_structure definition

CREATE TABLE `dwd_crystal_structure` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '晶体结构与性质的内部或来源库唯一标识',
  `formula` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '分子或晶体的化学组成式',
  `diffraction_radiation_type` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '晶体结构测定使用的 X 射线或中子衍射辐射类型',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='晶体结构与性质';

-- gkx.dwd_deal definition

CREATE TABLE `dwd_deal` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药物交易的内部或来源库唯一标识',
  `drug_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '交易涉及的药品、候选药物或管线资产名称',
  `licensor` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '在药物交易中授出研发、生产或商业化权益的公司',
  `licensee` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '在药物交易中获得相关权益的公司',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_deal_drug_name` (`drug_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='药物交易';

-- gkx.dwd_drug definition

CREATE TABLE `dwd_drug` (
  `application_number` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药品在监管机构申请或批准体系中的编号，用于关联审评、批准和标签信息',
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品记录的内部或来源库唯一标识，用于去重和跨表关联',
  `drug_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药物安全、交易或试验记录中涉及的药品名称',
  `brand_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药品上市销售时使用的品牌名称',
  `generic_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药品非专利通用名称或国际通用名称',
  `active_ingredients` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药品中具有治疗作用的主要成分，可包含一个或多个成分',
  `route` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药品进入人体的给药方式，如口服、注射、皮下等',
  `dosage_form` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药品制剂形态，如片剂、胶囊、注射液等',
  `application_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '监管申请类别，如 NDA、ANDA、BLA 等',
  `sponsor_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '提交药品申请或持有上市许可的机构全称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_drug_application_number` (`application_number`) USING BTREE,
  KEY `idx_dwd_drug_drug_name` (`drug_name`) USING BTREE,
  KEY `idx_dwd_drug_brand_name` (`brand_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='药品信息表';

-- gkx.dwd_drug_profile definition

CREATE TABLE `dwd_drug_profile` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药物档案的内部或来源库唯一标识',
  `brand_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品上市销售时使用的品牌名称',
  `indications_and_usage` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '药品标签中关于适应症、适用人群和使用场景的说明',
  `mechanism_of_action` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '药物发挥治疗作用的生物学或药理学机制',
  `substance_name` json DEFAULT NULL COMMENT '药品中具有治疗作用的主要成分，可包含一个或多个成分',
  `contraindications` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '不应使用该药物的疾病、状态或用药条件',
  `warnings_and_cautions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '药品标签中的重要风险、警示和用药注意事项',
  `adverse_reactions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '临床试验或上市后报告中记录的药物不良反应',
  `dosage_and_administration` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '药品推荐给药剂量、频率、调整方式和用药方法',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_drug_profile_brand_name` (`brand_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='药物档案表';

-- gkx.dwd_drug_substance definition

CREATE TABLE `dwd_drug_substance` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '化合物性质与信息的内部或来源库唯一标识',
  `molecular_name` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '化合物、材料或分子的标准英文名称',
  `formula` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分子或晶体的化学组成式',
  `in_chi_key` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'InChI 的固定长度哈希标识，用于化合物快速匹配和去重',
  `in_chi` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '化合物的 IUPAC 国际化学标识符',
  `std_smiles` varchar(4000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '化合物标准化后的 SMILES 结构表示',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_drug_substance_molecular_name` (`molecular_name`(191)) USING BTREE,
  KEY `idx_dwd_drug_substance_in_chi_key` (`in_chi_key`) USING BTREE,
  KEY `idx_dwd_drug_substance_in_chi` (`in_chi`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='化合物性质与信息';

-- gkx.dwd_en_author definition

CREATE TABLE `dwd_en_author` (
  `paper_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `author_sequence` int NOT NULL DEFAULT '0' COMMENT '作者在文献中的顺序。',
  `author_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者的唯一主键 id',
  `en_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者的英文名称',
  `zh_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者中文名',
  `email` json NOT NULL COMMENT '文献作者email',
  `correspond` tinyint NOT NULL DEFAULT '0' COMMENT '是否为通讯作者',
  `institution` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '作者所属机构或单位的名称。',
  `affiliation` json NOT NULL COMMENT '文献作者地址',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '来源贴源库表名',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`paper_id`,`author_sequence`) USING BTREE,
  KEY `idx_dwd_en_author_author_id` (`author_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文文献作者详情信息';

-- gkx.dwd_en_author_bak_20260710 definition

CREATE TABLE `dwd_en_author_bak_20260710` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献作者的唯一主键 id',
  `paper_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献记录的唯一主键标识。',
  `en_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献作者的英文名称',
  `zh_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献作者中文名',
  `affiliation` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '文献作者地址',
  `email` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '文献作者email',
  `correspond` tinyint DEFAULT NULL COMMENT '是否为通讯作者。否=0，是=1，未知=Null',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-英文文献作者详情信息';

-- gkx.dwd_en_journal definition

CREATE TABLE `dwd_en_journal` (
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '期刊、会议或预印本记录的唯一标识。',
  `publication_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标识出版载体的类型，如期刊、会议或预印本等。',
  `country` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊、会议或出版机构所属的国家或地区。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊、顶会或预印本平台的英文名称。',
  `name_abbr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊、会议或预印本名称的简称或缩写。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊、顶会或预印本平台的中文名称。',
  `issn_print` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国际标准连续出版物编号。纸印出版 issn',
  `issn_online` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国际标准连续出版物编号。在网发行 issn',
  `jn_official` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '期刊官方网站地址。',
  `en_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '期刊、会议或预印本平台的英文简介或说明。',
  `establish_time` int NOT NULL DEFAULT '0' COMMENT '期刊首次创办或发行的时间。',
  `annual_publication` int NOT NULL DEFAULT '0' COMMENT '期刊或会议每年发表文章的数量。',
  `review` tinyint NOT NULL DEFAULT '0' COMMENT '标识该期刊是否为综述类期刊。',
  `impact_factor` double NOT NULL DEFAULT '0' COMMENT '期刊或会议的影响力评价指标。',
  `jcr_zone` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊在 JCR 等评价体系中的分区信息。',
  `review_period` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊从投稿到审稿完成的平均周期。',
  `self_rate` double NOT NULL DEFAULT '0' COMMENT '期刊文献中自我引用所占的比例。',
  `top` tinyint NOT NULL DEFAULT '0' COMMENT '标识期刊或会议是否为所在领域的顶级刊物。',
  `warning` tinyint NOT NULL DEFAULT '0' COMMENT '标识期刊是否处于预警状态。',
  `is_sci` tinyint NOT NULL DEFAULT '0' COMMENT '标识期刊是否被 SCI 收录。',
  `publish_period` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的出版频率或发行周期。',
  `layout_cost` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊发表论文所需的版面费用。',
  `paper_nums` int NOT NULL DEFAULT '0' COMMENT '期刊、会议或平台已发表论文的数量。',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '来源贴源库表名',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`publication_id`) USING BTREE,
  KEY `idx_dwd_en_journal_en_name` (`en_name`(191)) USING BTREE,
  KEY `idx_dwd_en_journal_name_abbr` (`name_abbr`(191)) USING BTREE,
  KEY `idx_dwd_en_journal_zh_name` (`zh_name`(191)) USING BTREE,
  KEY `idx_dwd_en_journal_issn_print` (`issn_print`) USING BTREE,
  KEY `idx_dwd_en_journal_issn_online` (`issn_online`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文期刊详情信息';

-- gkx.dwd_en_journal_bak_20260710 definition

CREATE TABLE `dwd_en_journal_bak_20260710` (
  `id` bigint NOT NULL COMMENT '期刊、会议或预印本记录的唯一标识。',
  `issn` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊的国际标准连续出版物编号。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊、顶会或预印本平台的中文名称。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊、顶会或预印本平台的英文名称。',
  `name_abbr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊、会议或预印本名称的简称或缩写。',
  `publication_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标识出版载体的类型，如期刊、会议或预印本等。journal，conference',
  `en_description` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '期刊、会议或预印本平台的英文简介或说明。',
  `establish_time` int DEFAULT NULL COMMENT '期刊首次创办或发行的时间。',
  `language` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献或期刊出版使用的语言类型。',
  `country` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊、会议或出版机构所属的国家或地区。',
  `eissn` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊电子版的国际标准连续出版物编号。',
  `annual_publication` int DEFAULT NULL COMMENT '期刊或会议每年发表文章的数量。',
  `review` tinyint DEFAULT NULL COMMENT '标识该期刊是否为综述类期刊。否=0，是=1，未知=2',
  `impact_factor` decimal(20,10) DEFAULT NULL COMMENT '期刊或会议的影响力评价指标。',
  `jcr_zone` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊在 JCR 等评价体系中的分区信息。Q1,Q2,Q3,Q4',
  `open_access` tinyint DEFAULT NULL COMMENT '标识期刊或论文是否为开放获取。否=0，是=1，未知=2',
  `review_period` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊从投稿到审稿完成的平均周期。',
  `scope` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊或会议所属的大类学科领域。',
  `sub_scope` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊或会议所属的细分学科主题。',
  `self_rate` decimal(20,10) DEFAULT NULL COMMENT '期刊文献中自我引用所占的比例。',
  `top` tinyint DEFAULT NULL COMMENT '标识期刊或会议是否为所在领域的顶级刊物。否=0，是=1',
  `warning` tinyint DEFAULT NULL COMMENT '标识期刊是否处于预警状态。否=0，是=1，未知=Null',
  `is_sci` tinyint DEFAULT NULL COMMENT '标识期刊是否被 SCI 收录。否=0，是=1，未知=Null',
  `publish_period` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊的出版频率或发行周期。',
  `jn_official` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '期刊官方网站地址。',
  `layout_cost` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊发表论文所需的版面费用。',
  `paper_nums` int DEFAULT NULL COMMENT '期刊、会议或平台已发表论文的数量。',
  `updated_time` datetime NOT NULL COMMENT '该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-英文期刊详情信息';

-- gkx.dwd_en_paper definition

CREATE TABLE `dwd_en_paper` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的英文标题名称。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的中文标题名称。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '关联出版物的id，用于获取期刊详情信息',
  `paper_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献所属出版物的章节名称，栏目等。',
  `publication_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标识出版载体的类型，如期刊、会议或预印本等。',
  `publication_en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊、顶会或预印本平台的英文名称。',
  `issn_print` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国际标准连续出版物编号。纸印出版 issn',
  `issn_online` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国际标准连续出版物编号。在网发行 issn',
  `volume` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献发表所在期刊的卷号。',
  `issue` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献发表所在期刊的期号。',
  `first_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文在期刊中的起始页码。',
  `last_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文在期刊中的结束页码。',
  `cover_year_start` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献正式发表的年份。',
  `cover_date_start` date NOT NULL DEFAULT '1970-01-01' COMMENT '文献正式发表的时间。',
  `language` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献或期刊出版使用的语言类型。',
  `abstract_available` tinyint NOT NULL DEFAULT '0' COMMENT '摘要是否可用。',
  `open_access` tinyint NOT NULL DEFAULT '0' COMMENT '标识期刊或论文是否为开放获取。',
  `paper_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献在官网或来源平台中的访问链接。',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '来源贴源库表名',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_en_paper_doi` (`doi`(191)) USING BTREE,
  KEY `idx_dwd_en_paper_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_dwd_en_paper_paper_type` (`paper_type`(191)) USING BTREE,
  KEY `idx_dep_publication_en_name` (`publication_en_name`(191)) USING BTREE,
  KEY `idx_dwd_en_paper_issn_print` (`issn_print`) USING BTREE,
  KEY `idx_dwd_en_paper_issn_online` (`issn_online`) USING BTREE,
  KEY `idx_dep_cover_year_start` (`cover_year_start`) USING BTREE,
  KEY `idx_dep_cover_date_start` (`cover_date_start`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文详情信息';

-- gkx.dwd_en_paper_abstract definition

CREATE TABLE `dwd_en_paper_abstract` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `abstract_sequence` int NOT NULL DEFAULT '0' COMMENT '同一文献多个摘要的顺序号',
  `language` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献或期刊出版使用的语言类型。',
  `original_abstract` tinyint NOT NULL DEFAULT '0' COMMENT '是否为原始摘要。',
  `en_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献内容的英文摘要信息。',
  `zh_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献内容的中文摘要信息。',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '来源贴源库表名',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`,`abstract_sequence`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文摘要信息';

-- gkx.dwd_en_paper_bak_20260710 definition

CREATE TABLE `dwd_en_paper_bak_20260710` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献记录的唯一主键标识。',
  `publisher` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献或期刊所属的出版商信息。',
  `publication_id` bigint NOT NULL COMMENT '关联出版物的id，用于获取期刊详情信息',
  `paper_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献所属出版物的章节名称，栏目等。',
  `paper_url` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '文献在官网或来源平台中的访问链接。',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '论文的唯一标识编码。',
  `cover_date_start` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献正式发表的时间。',
  `funds` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '支持该论文研究的基金或资助项目信息。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献的英文标题名称。',
  `en_abstract` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '文献内容的英文摘要信息。',
  `keywords` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '描述论文主题内容的关键词。',
  `volume` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献发表所在期刊的卷号。',
  `issue` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献发表所在期刊的期号。',
  `first_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '论文在期刊中的起始页码。',
  `last_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '论文在期刊中的结束页码。',
  `reference_nums` int DEFAULT NULL COMMENT '论文参考文献的总数量。',
  `reference_content` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '论文所引用参考文献的具体内容。',
  `citation_nums` int DEFAULT NULL COMMENT '论文被其他文献引用的数量。',
  `citation_content` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '引用该论文的相关文献信息。',
  `relevant` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '与当前文献内容或主题相关的文献信息。',
  `authors` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '论文作者的结构化id列表。',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_dwd_en_paper_doi` (`doi`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-英文论文详情信息';

-- gkx.dwd_en_paper_citation definition

CREATE TABLE `dwd_en_paper_citation` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '关联出版物的id，用于获取期刊详情信息',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '引用文献的英文标题名称。',
  `publication_en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献出版物的英文名称。',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '来源贴源库表名',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_depc_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_dwd_en_paper_citation_doi` (`doi`(191)) USING BTREE,
  KEY `idx_depc_publication_en_name` (`publication_en_name`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文引用文献信息';

-- gkx.dwd_en_paper_cited_by definition

CREATE TABLE `dwd_en_paper_cited_by` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `paper_eid` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '被引文献EID（指向dwd_paper_info_qh.eid）',
  `citing_eid` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '引用文献EID',
  `citing_year` int DEFAULT NULL COMMENT '引用文献发表年份',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_citation` (`paper_eid`,`citing_eid`)
) ENGINE=InnoDB AUTO_INCREMENT=228219 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='爱思唯尔外文论文引用关系表';

-- gkx.dwd_en_paper_classification definition

CREATE TABLE `dwd_en_paper_classification` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `scope` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊或会议所属的大类学科领域。',
  `sub_scope` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊或会议所属的细分学科主题。',
  `keywords` json NOT NULL COMMENT '描述论文主题内容的关键词。',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '来源贴源库表名',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `created_time_2` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在要素库中的创建时间。',
  `updated_time_2` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条数据最近一次更新的时间。',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文分类信息';

-- gkx.dwd_en_paper_funding definition

CREATE TABLE `dwd_en_paper_funding` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `funds` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '支持该论文研究的基金或资助项目信息。',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '来源贴源库表名',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文基金信息';

-- gkx.dwd_en_paper_info definition

CREATE TABLE `dwd_en_paper_info` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键ID',
  `eid` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Scopus文献唯一标识',
  `doi` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文献数字对象唯一标识符',
  `online_status` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文献在线状态',
  `pui` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '出版商唯一标识',
  `sdfullavail` tinyint DEFAULT '0' COMMENT '全文可获取状态，0-不可获取，1-可获取',
  `issn` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '期刊国际标准刊号',
  `volume` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '期刊卷号',
  `issue` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '期刊期号',
  `first_page` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文献起始页码',
  `last_page` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文献结束页码',
  `sort_year` int DEFAULT NULL COMMENT '数据排序年份',
  `sort_yyyymm` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据排序年月',
  `pub_year` int DEFAULT NULL COMMENT '文献正式出版年份',
  `timestamp` datetime DEFAULT NULL COMMENT '文献数据更新时间戳',
  `orig_load_date` date DEFAULT NULL COMMENT '数据原始入库日期',
  `datesort` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '日期排序字符串',
  `indexeddate` datetime DEFAULT NULL COMMENT 'Scopus索引收录时间',
  `absavail` tinyint DEFAULT '0' COMMENT '摘要可获取状态，0-不可获取，1-可获取',
  `suppressdummy` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'no' COMMENT '是否隐藏虚拟数据',
  `srctype` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文献来源类型，j-期刊',
  `subj_area` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文献所属学科领域，多学科逗号分隔',
  `srctitle` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '期刊来源全称',
  `country` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文献所属国家',
  `language` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文献语种',
  `is_open_access` tinyint DEFAULT '0' COMMENT '是否开放获取，0-否，1-是',
  `oa_article_status` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '开放获取状态描述',
  `doctype` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文献文档类型',
  `group_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文献分组ID',
  `author_count` int DEFAULT '0' COMMENT '文献作者总数量',
  `author_list` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '作者完整信息列表，多作者分号分隔，含姓名、职称、作者ID等',
  `author_surname` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '第一作者姓氏',
  `author_initials` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '第一作者首字母缩写',
  `author_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '作者唯一标识',
  `title` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文献中文/英文标题',
  `source_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '期刊来源唯一ID',
  `source_title_abbrev` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '期刊来源简称',
  `asjc_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'ASJC学科分类编码，多编码逗号分隔',
  `cited_by_count` int DEFAULT '0' COMMENT '被引用次数',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '数据入库时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_eid` (`eid`)
) ENGINE=InnoDB AUTO_INCREMENT=10101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='爱思唯尔外文文献基础信息';

-- gkx.dwd_en_paper_reference definition

CREATE TABLE `dwd_en_paper_reference` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '关联出版物的id，用于获取期刊详情信息',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献的英文标题名称。',
  `publication_en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献出版物的英文名称。',
  `cover_year_start` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献正式发表的年份。',
  `volume` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献发表所在期刊的卷号。',
  `issue` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献发表所在期刊的期号。',
  `first_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献在期刊中的起始页码。',
  `last_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献在期刊中的结束页码。',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '来源贴源库表名',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_depr_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_dwd_en_paper_reference_doi` (`doi`(191)) USING BTREE,
  KEY `idx_depr_publication_en_name` (`publication_en_name`(191)) USING BTREE,
  KEY `idx_depr_cover_year_start` (`cover_year_start`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文参考文献信息';

-- gkx.dwd_en_paper_related definition

CREATE TABLE `dwd_en_paper_related` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `relevant` json NOT NULL COMMENT '与当前文献内容或主题相关的文献信息。',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '相关文献的英文标题名称。',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '来源贴源库表名',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id_2` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `relevant_2` json NOT NULL COMMENT '与当前文献内容或主题相关的文献信息。',
  `doi_2` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `en_name_2` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '相关文献的英文标题名称。',
  `data_source_2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '来源贴源库表名',
  `created_time_2` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在要素库中的创建时间。',
  `updated_time_2` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条数据最近一次更新的时间。',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_en_paper_related_doi` (`doi`(191)) USING BTREE,
  KEY `idx_depr_logic_id` (`logic_id`) USING BTREE,
  KEY `idx_dwd_en_paper_related_id_2` (`id_2`) USING BTREE,
  KEY `idx_dwd_en_paper_related_doi_2` (`doi_2`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文关联文献信息';

-- gkx.dwd_en_paper_title definition

CREATE TABLE `dwd_en_paper_title` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `title_sequence` int NOT NULL DEFAULT '0' COMMENT '同一文献多个标题的顺序号。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的英文标题名称。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的中文标题名称。',
  `language_code` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题的语言代码。',
  `language` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题的语言类型。',
  `original_title` tinyint NOT NULL DEFAULT '0' COMMENT '是否为原始标题。',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '来源贴源库表名',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`,`title_sequence`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文标题信息';

-- gkx.dwd_event definition

CREATE TABLE `dwd_event` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '会展的内部或来源库唯一标识',
  `event_name` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '医药或生命科学相关会议、展会名称',
  `organizer` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '会议或展会的主办机构',
  `start_date` date DEFAULT NULL COMMENT '会议或展会开始日期',
  `end_date` date DEFAULT NULL COMMENT '会议或展会结束日期',
  `event_url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '会议或展会官网或详情页 URL',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='会展';

-- gkx.dwd_forg_agg_identifier definition

CREATE TABLE `dwd_forg_agg_identifier` (
  `ename_en` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业英文名称',
  `code_category` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '代码大类',
  `code_subcategory` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '代码小类',
  `code_cn_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '代码中文名称',
  `code_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '代码名称',
  `code_value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '代码值'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外企业代码表';

-- gkx.dwd_forg_base_info definition

CREATE TABLE `dwd_forg_base_info` (
  `ename_en` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业英文名称',
  `ename_local` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业名称（本地语种）',
  `ename_pv` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '曾用名',
  `ipo_status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业状态',
  `employees_num` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '员工人数',
  `start_year` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '成立年份',
  `start_date` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '成立日期',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '国家或地区',
  `reg_city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '城市',
  `address1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '地址第1行',
  `address2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '地址第2行',
  `address3` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '地址第3行',
  `address4` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '地址第4行'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外企业基本信息表';

-- gkx.dwd_forg_beneficiary_info definition

CREATE TABLE `dwd_forg_beneficiary_info` (
  `ename_en` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业英文名称',
  `bo_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '受益人名称',
  `bo_gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '受益人性别',
  `bo_birthdate` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '受益人出生日期',
  `bo_country_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '受益人所在国家代码',
  `bo_manager` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '受益人是否同时是管理层',
  `path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '路径'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外企业受益人表';

-- gkx.dwd_forg_contact definition

CREATE TABLE `dwd_forg_contact` (
  `ename_en` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业英文名称',
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '电话',
  `domain` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '域名',
  `website` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '网址',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '邮箱'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外企业联系方式表';

-- gkx.dwd_forg_executive_info definition

CREATE TABLE `dwd_forg_executive_info` (
  `ename_en` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业英文名称',
  `executives_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '高管名称',
  `dm_age` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '高管年龄',
  `dm_sex` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '高管性别',
  `executives_position` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '高管职位',
  `dm_birthdate` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '高管出生日期',
  `dm_nationalities` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '高管国籍',
  `dm_biography` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '高管履历'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外企业高管表';

-- gkx.dwd_forg_industry definition

CREATE TABLE `dwd_forg_industry` (
  `ename_en` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业英文名称',
  `industry_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '行业分类标准',
  `industry_level` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '行业分类层级',
  `industry_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '行业代码',
  `industry_label_cn` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '行业描述'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外企业行业分类表';

-- gkx.dwd_forg_investment definition

CREATE TABLE `dwd_forg_investment` (
  `ename_en` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业英文名称',
  `invested_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '子公司名称',
  `invested_eid` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '子公司国家代码',
  `direct_pct` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '直接持股比例（%）',
  `total_pct` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '总持股比例（%）'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外企业子公司情况表';

-- gkx.dwd_forg_profile definition

CREATE TABLE `dwd_forg_profile` (
  `ename_en` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业英文名称',
  `business_desc` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '业务简介',
  `products_services` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '主要产品与服务'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外企业简介表';

-- gkx.dwd_forg_shareholder definition

CREATE TABLE `dwd_forg_shareholder` (
  `ename_en` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业英文名称',
  `sh_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '股东名称',
  `sh_entity_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '股东类型',
  `sh_country_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '股东所在国家代码',
  `sh_direct_pct` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '股东直接持股比例（%）',
  `sh_total_pct` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '股东总持股比例（%）'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外企业股东表';

-- gkx.dwd_forg_ultimate_control definition

CREATE TABLE `dwd_forg_ultimate_control` (
  `ename_en` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业英文名称',
  `entity_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '实控人名称',
  `entity_country_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '实控人国家代码',
  `direct_pct` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '实控人直接持股比例（%）',
  `total_pct` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '实控人总持股比例（%）'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外企业实控人表';

-- gkx.dwd_hycy_aquaculture_veterinary_drugs_enterprise_list definition

CREATE TABLE `dwd_hycy_aquaculture_veterinary_drugs_enterprise_list` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：企业名称+通用名+规格+批准文号，连接字符：-，md5',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业的中文名称；',
  `common_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '通用名',
  `specifications` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '规格型号',
  `trade_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '商品名',
  `approval_number` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '批准文号',
  `approval_date` date DEFAULT NULL COMMENT '批准日期',
  `validity_period` date DEFAULT NULL COMMENT '有效期至',
  `failure_reason` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '失效原因',
  `change_situation` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '变更情况',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_水产养殖用兽药名录';

-- gkx.dwd_hycy_aquatic_new_species definition

CREATE TABLE `dwd_hycy_aquatic_new_species` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：品种登记号+品种名称+育种单位，连接字符：-，md5',
  `reg_no` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '品种登记号',
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '品种名称',
  `breeding_unit` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '育种单位',
  `stat_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '年份时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_水产新品种认定情况及育种单位统计表';

-- gkx.dwd_hycy_china_classification_society_marine_product_list definition

CREATE TABLE `dwd_hycy_china_classification_society_marine_product_list` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：证书编号+工作类型+有效期至+产品名称+工厂名称，连接字符：-，md5',
  `certificate_number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件编号',
  `work_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '工作类型',
  `validity_period` date DEFAULT NULL COMMENT '有效期至',
  `product_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品名称',
  `factory_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '工厂名称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_中国船级社船用产品目录';

-- gkx.dwd_hycy_china_mainland_submarine_cable definition

CREATE TABLE `dwd_hycy_china_mainland_submarine_cable` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则:城市名称+光缆名称+带宽+长度+起始地区，连接字符：-，md5',
  `province_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `province_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `cable_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '光缆名称',
  `bandwidth` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '带宽',
  `length` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '长度',
  `origin_region` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '起始地区',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_中国大陆地区海底光缆情况';

-- gkx.dwd_hycy_china_major_city_lng_receiving_capacity definition

CREATE TABLE `dwd_hycy_china_major_city_lng_receiving_capacity` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则:城市名称+统计时间，连接字符：-，md5',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '存在非大陆城市',
  `receipt_capacity` int NOT NULL DEFAULT '0' COMMENT '接收能力',
  `receipt_unit` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '接收单位',
  `rank` int DEFAULT NULL COMMENT '排名',
  `lng_receipt_station` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'LNG接收站',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统计时间',
  `update_frequency` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '更新频次',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_中国主要城市LNG接收能力';

-- gkx.dwd_hycy_china_ocean_large_model definition

CREATE TABLE `dwd_hycy_china_ocean_large_model` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则:大模型名称，连接字符：-，md5',
  `model_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '大模型名称',
  `research_entity_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '或归属单位',
  `research_entity_city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主体所在城市',
  `domain_oriented` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '面向领域',
  `features_progress` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技术特点与进展',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_国内海洋大模型情况';

-- gkx.dwd_hycy_china_offshore_field definition

CREATE TABLE `dwd_hycy_china_offshore_field` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则:油田名称+运营主体名称，连接字符：-，md5',
  `oilfield_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '油田名称',
  `operator_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '运营主体名称',
  `reserves` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '储量',
  `production_scale` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '油当量',
  `geological_features` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '地质特点',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统计时间',
  `update_frequency` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '指标更新频次，年更、季更等',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_中国海上油气田信息';

-- gkx.dwd_hycy_china_offshore_production definition

CREATE TABLE `dwd_hycy_china_offshore_production` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则:年份，连接字符：-，md5',
  `year` int NOT NULL DEFAULT '0' COMMENT '年份',
  `oil_output` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '单位:万吨',
  `gas_output` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '单位:亿立方米',
  `oil_gas_total_output` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '油当量,单位:万吨',
  `update_frequency` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '更新频次',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_中国海洋油气田产量情况';

-- gkx.dwd_hycy_china_offshore_production_growth definition

CREATE TABLE `dwd_hycy_china_offshore_production_growth` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则:油田名称+统计时间，连接字符：-，md5',
  `rank` int NOT NULL DEFAULT '0' COMMENT '排名',
  `oilfield_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '油田名称',
  `oge` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT '油气当量',
  `oge_unit` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '油气单位',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统计时间',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '备注',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_中国海洋油气产量增长情况';

-- gkx.dwd_hycy_csad_ship definition

CREATE TABLE `dwd_hycy_csad_ship` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：船检登记号，连接字符：-，md5',
  `ship_registration_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '船检登记号',
  `ship_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '船名',
  `haihe_river_ship` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '海河船',
  `gross_tonnage` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '总吨位',
  `ship_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '船舶类型',
  `ship_owner` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '船舶所有人',
  `ship_operator` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '船舶经营人',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_CSAD船舶';

-- gkx.dwd_hycy_enterprise_indicators definition

CREATE TABLE `dwd_hycy_enterprise_indicators` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：标准指标名称+企业名称+统计时间，连接字符：-，md5',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业名称',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '指标统计时间',
  `update_frequency` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '指标更新频次，年更、季更等',
  `index_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标准指标名称',
  `data` decimal(18,2) DEFAULT NULL COMMENT '标准数值',
  `unit` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标准单位',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_企业指标表';

-- gkx.dwd_hycy_gas_supply definition

CREATE TABLE `dwd_hycy_gas_supply` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：城市名称+气源名称，连接字符：-，md5',
  `province_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `province_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `gas_source_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '气源名称',
  `gas_source_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '气源类型',
  `gas_source_origin` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '气源来源',
  `ownership_structure` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '股权结构',
  `tank_capacity` decimal(38,20) DEFAULT NULL COMMENT '储罐规模',
  `tank_capacity_unit` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '储罐规模单位',
  `annual_supply_capacity` decimal(38,20) DEFAULT NULL COMMENT '年供应能力',
  `annual_supply_capacity_unit` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '年供应能力单位',
  `is_lng_refill_capability` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '是否具备LNG补液功能',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_天然气供应信息表';

-- gkx.dwd_hycy_global_alternative_marine_fuel_market_demand_scale definition

CREATE TABLE `dwd_hycy_global_alternative_marine_fuel_market_demand_scale` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：燃料类别+年份，连接字符：-，md5',
  `fuel_category` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '燃料类别',
  `year` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '年份',
  `market_demand` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '市场需求',
  `market_scale` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '市场规模',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_船用替代燃料全球市场需求及规模预测';

-- gkx.dwd_hycy_global_cruise_capacity_distribution definition

CREATE TABLE `dwd_hycy_global_cruise_capacity_distribution` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：指标名称+船型+船龄范围+统计时间，连接字符：-，md5',
  `ship_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '船型',
  `ship_age_range` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '船龄范围',
  `index_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '指标名称',
  `data` decimal(18,2) DEFAULT NULL COMMENT '标准数值',
  `unit` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标准单位',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '统计时间',
  `update_frequency` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '指标更新频次，年更、季更等',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_全球邮轮运力分布';

-- gkx.dwd_hycy_green_fuel_enterprise definition

CREATE TABLE `dwd_hycy_green_fuel_enterprise` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：城市名称+产业链环节，连接字符：-，md5',
  `province_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `province_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `industry_chain_link` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业链环节',
  `enterprise_name` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业名称',
  `core_product_service` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '优势产品或服务',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_绿色燃料加注产业信息表';

-- gkx.dwd_hycy_index definition

CREATE TABLE `dwd_hycy_index` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：级别+区域+省份+城市+区县+经济区+统计时间+标准指标名称+采集来源，连接字符：-，md5',
  `level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '指标的空间级别',
  `region` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '全球、重点国家等',
  `province` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '省份',
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '城市',
  `district` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '区县',
  `other_region` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '长三角、珠三角等经济区',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统计时间',
  `scope` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '年度、季度、月度等周期',
  `index_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '标准指标名称',
  `data` decimal(18,2) DEFAULT NULL COMMENT '标准数值',
  `unit` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标准单位',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_指标库';

-- gkx.dwd_hycy_industry definition

CREATE TABLE `dwd_hycy_industry` (
  `id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：类型、产业编码、环节编码',
  `record_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '实体类型',
  `industry_chain_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业链ID',
  `entity_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '实体ID',
  `industry_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业编码',
  `industry_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业名称',
  `link_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '环节编码',
  `link_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '环节名称',
  `chain_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '挂链时间',
  `chain_operator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '挂链人',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='上链结果表';

-- gkx.dwd_hycy_international_shipping_agency_enterprises_registration definition

CREATE TABLE `dwd_hycy_international_shipping_agency_enterprises_registration` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：国际船舶代理企业名称+备案回执文号+备案年份，连接字符：-，md5',
  `number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '序号',
  `international_ship_agent_enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业工商注册的名称',
  `registered_address` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册地址',
  `record_receipt_number` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '备案回执文号',
  `annual_filing` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '备案年份',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_国际船舶代理企业备案表';

-- gkx.dwd_hycy_international_shipping_certificate_effective_enterprise definition

CREATE TABLE `dwd_hycy_international_shipping_certificate_effective_enterprise` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：证书编号+企业中文名称，连接字符：-，md5',
  `number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '序号',
  `certificate_number` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '证件编号',
  `enterprise_chinese_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业的中文名称；',
  `enterprise_english_name` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '生产企业的英文名称；',
  `registered_address` varchar(600) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册地址',
  `business_line` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '业务种类',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_国际班轮运输经营资格登记证有效企业';

-- gkx.dwd_hycy_leading_maritime_capitals definition

CREATE TABLE `dwd_hycy_leading_maritime_capitals` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：榜单名称+一级指标+二级指标+统计时间+城市名称，连接字符：-，md5',
  `rank_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '榜单名称',
  `first_level_index` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '一级指标',
  `second_level_index` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '二级指标',
  `rank` int NOT NULL DEFAULT '0' COMMENT '排名',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '统计时间',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '城市名称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_世界领先海事之都报告城市数据';

-- gkx.dwd_hycy_marine_alternative_fuel_cost definition

CREATE TABLE `dwd_hycy_marine_alternative_fuel_cost` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：燃料类别+燃料类型+生产路线+当前生产成本+远期生产成本，连接字符：-，md5',
  `fuel_category` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '燃料类别',
  `fuel_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '燃料类型',
  `production_route` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '生产路线',
  `current_production_cost` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '当前生产成本',
  `future_production_cost` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '远期生产成本',
  `cost_currency` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '成本货币单位',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_船用替代燃料生产成本对比表';

-- gkx.dwd_hycy_marine_energy_industry_carrier definition

CREATE TABLE `dwd_hycy_marine_energy_industry_carrier` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：创新载体名称+载体类型+级别，连接字符：-，md5',
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '创新载体名称',
  `category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '载体类型',
  `level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '级别',
  `charge_authority` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '主管部门',
  `support_unit_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '依托单位名称',
  `support_unit_flag` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业;科研机构;高校',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '立项年度',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_海洋能源创新平台载体名单';

-- gkx.dwd_hycy_marine_forecast_data definition

CREATE TABLE `dwd_hycy_marine_forecast_data` (
  `id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：区域、分析时间、预报时间、浪高、分析内容',
  `analysis_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分析类型',
  `region` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '区域',
  `analysis_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '分析时间',
  `forecast_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '预报时间',
  `wave_height` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '浪高',
  `weather_condition` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '天气状况',
  `analysis_content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分析内容',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋分析预报数据';

-- gkx.dwd_hycy_marine_observation_data definition

CREATE TABLE `dwd_hycy_marine_observation_data` (
  `id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：站点名称、观测时间、水温、盐度、风速、风向、PH值',
  `data_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '实测数据类型',
  `station_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '站点名称',
  `longitude` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '经度',
  `latitude` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '纬度',
  `observation_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '观测时间',
  `water_temp` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '水温',
  `salinity` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '盐度',
  `wind_speed` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '风速',
  `wind_direction` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '风向',
  `ph_value` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT 'pH值',
  `dissolved_oxygen` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '溶解氧',
  `species_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '生物名称',
  `quantity` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '数量',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋实测数据';

-- gkx.dwd_hycy_marine_remote_sensing_data definition

CREATE TABLE `dwd_hycy_marine_remote_sensing_data` (
  `id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：卫星名称、拍摄时间、区域、分辨率、影像地址',
  `remote_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '遥感类型',
  `satellite_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '卫星名称',
  `capture_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '拍摄时间',
  `region` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '区域',
  `resolution` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分辨率',
  `image_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '影像地址',
  `data_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据说明',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋地理遥感数据';

-- gkx.dwd_hycy_methanol_production_cost_trend_prediction definition

CREATE TABLE `dwd_hycy_methanol_production_cost_trend_prediction` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：一级分类+二级分类+当前生产成本+远期生产成本，连接字符：-，md5',
  `first_level` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技术路线的分类',
  `second_level` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技术路线的分类',
  `current_production_cost` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '当前生产成本',
  `forward_production_cost` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '远期生产成本',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_甲醇生产成本及趋势预测';

-- gkx.dwd_hycy_nvocc_operator_list definition

CREATE TABLE `dwd_hycy_nvocc_operator_list` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：企业中文名称+企业英文名称，连接字符：-，md5',
  `enterprise_chinese_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业的中文名称；',
  `enterprise_english_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业英文名称',
  `enterprise_english_short_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业英文简称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_无船承运业务经营者名录';

-- gkx.dwd_hycy_offshore_fishing_company_evaluation definition

CREATE TABLE `dwd_hycy_offshore_fishing_company_evaluation` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：指标类别+一级指标+二级指标+三级指标，连接字符：-，md5',
  `category` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '指标类别',
  `first_index` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '一级指标',
  `sec_index` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '二级指标',
  `third_index` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '三级指标',
  `score` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '分',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '备注说明',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_全国远洋渔业企业履约评估表';

-- gkx.dwd_hycy_pelagic_fishery_enterprise_eval_results definition

CREATE TABLE `dwd_hycy_pelagic_fishery_enterprise_eval_results` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：企业名称，连接字符：-，md5',
  `number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '序号',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业的中文名称；',
  `score` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT '得分',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_远洋渔业企业履约评估结果';

-- gkx.dwd_hycy_port_operation_license_form definition

CREATE TABLE `dwd_hycy_port_operation_license_form` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：企业名称+证书编号+证件起始日期+证件终止日期+证件有效期，连接字符：-，md5',
  `number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '序号',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业工商注册的名称',
  `legal_representative` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '法定代表人',
  `certificate_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件名称',
  `certificate_number` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '证件编号',
  `issuing_authority` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '发证机关',
  `registered_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册地址',
  `operating_area` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '经营地域',
  `business_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '经营业务类型',
  `business_place` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '经营场所所在港区',
  `dangerous_goods_operation_certificate` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '港口危险货物作业附证',
  `dangerous_goods_operation` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '从事危险货物港口作业情况',
  `certificate_start_date` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件起始日期',
  `certificate_end_date` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件终止日期',
  `certificate_validity_period` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件有效期',
  `certificate_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件状态',
  `remark` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '备注说明',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_港口经营许可表';

-- gkx.dwd_hycy_shanghai_domestic_water_transport_directory definition

CREATE TABLE `dwd_hycy_shanghai_domestic_water_transport_directory` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：证书编号+企业名称，连接字符：-，md5',
  `certificate_number` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件编号',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业的中文名称；',
  `main_business_passenger_transport` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '主营旅客运输',
  `main_business_freight_transport` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '主营货物运输',
  `certificate_validity_period` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件有效期',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_上海市国内水路运输经营名录';

-- gkx.dwd_hycy_ship_management_enterprise_trustee_ship definition

CREATE TABLE `dwd_hycy_ship_management_enterprise_trustee_ship` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：企业名称+代管类型，连接字符：-，md5',
  `province_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `province_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业名称',
  `trustee_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '代管类型',
  `is_water_transport_qualification` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '是否同时具有水路运输经营资格',
  `is_international_ship_management` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '是否兼营国际船舶管理',
  `is_domestic_ship_management` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '是否兼营国内船舶管理',
  `trustee_ship_count` int DEFAULT NULL COMMENT '代管船舶数量',
  `total_tonnage` decimal(18,2) DEFAULT NULL COMMENT '总吨合计',
  `business_scope` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '经营范围',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_船舶管理企业代管船舶表';

-- gkx.dwd_hycy_shipping_capacity definition

CREATE TABLE `dwd_hycy_shipping_capacity` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：统计类型+统计时间+更新频次+企业名称+船舶类型，连接字符：-，md5',
  `province_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `province_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `statistical_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统计类型',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业名称',
  `enterprise_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业类型',
  `vessel_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '船舶类型',
  `vessels` int NOT NULL DEFAULT '0' COMMENT '船舶总数',
  `hong_kong_macao_vessels` int NOT NULL DEFAULT '0' COMMENT '港澳通航船舶数量',
  `inland_vessels` int NOT NULL DEFAULT '0' COMMENT '内陆通航船舶数量',
  `international_vessels` int NOT NULL DEFAULT '0' COMMENT '国际通航船舶数量',
  `passenger_capacity` int NOT NULL DEFAULT '0' COMMENT '客位数',
  `gross_tonnage` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT '总吨数',
  `deadweight_tonnage` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT '载重吨',
  `teu_capacity` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT 'TEU',
  `cubic_meter_capacity` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT '立方米',
  `car_capacity` int NOT NULL DEFAULT '0' COMMENT '车位',
  `statistical_date` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统计时间',
  `update_frequency` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '更新频次',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_航运运力表';

-- gkx.dwd_hycy_submarine_cable_distribution definition

CREATE TABLE `dwd_hycy_submarine_cable_distribution` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：类别+区域，连接字符：-，md5',
  `category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '类别',
  `region` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '区域',
  `submarine_cable` int DEFAULT NULL COMMENT '海底光缆条数',
  `connection_point` int DEFAULT NULL COMMENT '链接点个数',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_海底光缆分布';

-- gkx.dwd_hycy_sz_maritime_law_attorneys definition

CREATE TABLE `dwd_hycy_sz_maritime_law_attorneys` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：年份+姓名+所属律师事务所+执业证号，连接字符：-，md5',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '年份',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '姓名',
  `gender` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '性别',
  `region` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '区域',
  `law_firm` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '所属律师事务所',
  `licensed_category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '执业类别',
  `licensed_no` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '执业证号',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_深圳海事海商律所及执业律师';

-- gkx.dwd_industry_chain_info definition

CREATE TABLE `dwd_industry_chain_info` (
  `chain_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '产业链代码',
  `chain_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '产业链名称',
  `node_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '节点代码',
  `node_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '节点名称',
  `node_type` int DEFAULT NULL COMMENT '节点类型',
  `level` int DEFAULT NULL COMMENT '节点层级',
  `node_seq` int DEFAULT NULL COMMENT '节点序号',
  `parent_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '父级节点代码',
  `parent_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '父级节点名称',
  `node_imp_level` int DEFAULT NULL COMMENT '节点重要性等级',
  `downstream_lin` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '下游节点代码',
  `node_stage` int DEFAULT NULL COMMENT '节点环节',
  `node_path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '节点路径',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='产业链图谱';

-- gkx.dwd_industry_chain_news_info definition

CREATE TABLE `dwd_industry_chain_news_info` (
  `chain_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '产业链代码',
  `chain_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '产业链名称',
  `news_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '资讯id',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '标题',
  `relaese_date` date DEFAULT NULL COMMENT '发布时间',
  `summary` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '摘要',
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '来源',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='产业动态资讯';

-- gkx.dwd_industry_code definition

CREATE TABLE `dwd_industry_code` (
  `id` bigint DEFAULT NULL COMMENT 'id',
  `code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '环节编码',
  `name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '环节名称',
  `parent_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '父级编码',
  `industry_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业编码',
  `industry_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业名称',
  `level` int NOT NULL DEFAULT '0' COMMENT '级别',
  `definition` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '定义',
  `is_key_link` int NOT NULL DEFAULT '0' COMMENT '是否为关键环节',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='产业链';

-- gkx.dwd_information definition

CREATE TABLE `dwd_information` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '医疗资讯的内部或来源库唯一标识',
  `information_title` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '医疗资讯的标题',
  `information_time` date DEFAULT NULL COMMENT '医疗资讯正式发布的日期或时间',
  `information_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '医疗资讯正文或摘要内容',
  `information_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '医疗资讯来源页面的 URL',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='医疗资讯';

-- gkx.dwd_job definition

CREATE TABLE `dwd_job` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '招聘的内部或来源库唯一标识',
  `job_title` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '招聘岗位名称',
  `company_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '发布岗位的公司或机构名称',
  `job_description` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '岗位职责、任职要求或工作内容摘要',
  `job_url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '招聘岗位详情页 URL',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='招聘';

-- gkx.dwd_market definition

CREATE TABLE `dwd_market` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品市场对应的内部或来源库唯一标识',
  `market_name` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品市场对应的国家、地区、治疗领域或细分市场名称',
  `market_share` decimal(18,6) NOT NULL DEFAULT '0.000000' COMMENT '目标药品、品类或仿制药在指定市场中的占比',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='药品市场表';

-- gkx.dwd_material_virtual_structure definition

CREATE TABLE `dwd_material_virtual_structure` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '材料虚拟结构的内部或来源库唯一标识',
  `material_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '材料或晶体结构的名称',
  `formula` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '材料的化学组成式',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_material_virtual_structure_material_name` (`material_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='材料虚拟结构';

-- gkx.dwd_medical_device definition

CREATE TABLE `dwd_medical_device` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '医疗器械记录的唯一标识或来源库编码',
  `device_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '医疗器械产品名称',
  `device_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '医疗器械的类别、用途或产品类型',
  `device_id_issuing_agency` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '器械标识或编码的发行机构',
  `brand_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '医疗器械或产品使用的品牌名称',
  `company_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '医疗器械生产企业或注册企业名称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_medical_device_device_name` (`device_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='医疗器械表';

-- gkx.dwd_molecular_spectrum definition

CREATE TABLE `dwd_molecular_spectrum` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '唯一标识',
  `substance_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联到物质信息表的物质ID，用于将谱图归属到具体物质',
  `en_name` varchar(4000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '化合物、材料或分子的标准英文名称',
  `formula` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分子、化合物或晶体的化学组成式',
  `ms_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '质谱数据级别，如 MS1 或 MS2',
  `ion_mode` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '质谱采集的离子极性模式，如正离子或负离子',
  `ionization` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '质谱电离方法，如 ESI、APCI、EI 等',
  `collision_energy` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'MS/MS 碎裂过程使用的碰撞能设置',
  `precursor_mz` decimal(18,6) DEFAULT NULL COMMENT 'MS/MS 采集时被选择碎裂的前体离子 m/z',
  `precursor_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '前体离子的加合物或离子形式',
  `peaks` json DEFAULT NULL COMMENT '谱图峰数据列表，通常包含 m/z、强度和相对强度',
  `mass_to_charge_ratio` json DEFAULT NULL COMMENT '谱峰或离子的 m/z 数值',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_molecular_spectrum_substance_id` (`substance_id`) USING BTREE,
  KEY `idx_dwd_molecular_spectrum_en_name` (`en_name`(191)) USING BTREE,
  KEY `idx_dwd_molecular_spectrum_formula` (`formula`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='分子谱图';

-- gkx.dwd_multi_omics definition

CREATE TABLE `dwd_multi_omics` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '多组学数据的内部或来源库唯一标识',
  `data_category` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '多组学数据的大类，如突变、表达、甲基化、蛋白组等',
  `data_type` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '多组学数据的细分类型或文件类型',
  `repository` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '多组学数据来源平台或数据库名称',
  `experimental_strategy` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '产生该组学数据的实验或测序策略',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='多组学表';

-- gkx.dwd_org_annual_financial_info definition

CREATE TABLE `dwd_org_annual_financial_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `year` bigint NOT NULL COMMENT '年报年度',
  `total_assets` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '资产总额',
  `total_liabilities` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '负债总额',
  `operating_revenue` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '营业收入',
  `main_business_revenue` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '主营业务收入',
  `total_profit` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '利润总额',
  `pure_profit` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '净利润',
  `total_tax_paid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '纳税总额',
  `owners_equity` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '所有者权益合计',
  `employees_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '从业人数',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_annual_financial_info_org_id_year` (`org_id`,`year`) USING BTREE,
  KEY `idx_dwd_org_annual_financial_info_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_annual_financial_info_org_id` (`org_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='年报财务信息';

-- gkx.dwd_org_annual_financial_info_bak_20260710 definition

CREATE TABLE `dwd_org_annual_financial_info_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `year` int DEFAULT NULL COMMENT '年报年度',
  `total_assets` double DEFAULT NULL COMMENT '资产总额',
  `total_fixed_assets` double DEFAULT NULL COMMENT '固定资产总额',
  `total_liabilities` double DEFAULT NULL COMMENT '负债总额',
  `operating_revenue` double DEFAULT NULL COMMENT '营业收入',
  `main_business_revenue` double DEFAULT NULL COMMENT '主营业务收入',
  `total_profit` double DEFAULT NULL COMMENT '利润总额',
  `pure_profit` double DEFAULT NULL COMMENT '净利润',
  `total_tax_paid` double DEFAULT NULL COMMENT '纳税总额',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构年报财务信息';

-- gkx.dwd_org_bankruptcy_public_cases definition

CREATE TABLE `dwd_org_bankruptcy_public_cases` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '案号',
  `case_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案件类型',
  `handling_court` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '经办法院',
  `applicant_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '申请人信息',
  `respondent_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '被申请人信息',
  `admin_org` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '管理人机构',
  `admin_org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '管理人机构id',
  `admin_principal` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '管理人主要负责人',
  `public_date` date DEFAULT NULL COMMENT '公开时间',
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '链接',
  `history_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '历史状态',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_bankruptcy_public_cases_case_no_handling_court` (`case_no`,`handling_court`) USING BTREE,
  KEY `idx_dwd_org_bankruptcy_public_cases_admin_org_id` (`admin_org_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='破产案件';

-- gkx.dwd_org_bankruptcy_public_cases_bak_20260710 definition

CREATE TABLE `dwd_org_bankruptcy_public_cases_bak_20260710` (
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案号',
  `case_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案件类型',
  `handling_court` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '经办法院',
  `applicant_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '申请人信息',
  `respondent_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '被申请人信息',
  `admin_org` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '管理人机构',
  `admin_org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '管理人机构id',
  `admin_principal` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '管理人主要负责人',
  `public_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公开时间',
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '链接',
  `is_deleted` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否删除',
  `history_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '历史状态',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='破产案件表';

-- gkx.dwd_org_bankruptcy_public_cases_list definition

CREATE TABLE `dwd_org_bankruptcy_public_cases_list` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `bankruptcy_party_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '破产案件当事人记录唯一标识id。',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案号',
  `related_person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '相关人名称',
  `party_role_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人角色类型',
  `party_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人类型',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `public_date` date DEFAULT NULL COMMENT '公开时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_bankruptcy_public_cases_list_bankruptcy_party_id` (`bankruptcy_party_id`) USING BTREE,
  KEY `idx_dwd_org_bankruptcy_public_cases_list_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_bankruptcy_public_cases_list_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='破产案件当事人';

-- gkx.dwd_org_bankruptcy_public_cases_list_bak_20260710 definition

CREATE TABLE `dwd_org_bankruptcy_public_cases_list_bak_20260710` (
  `bankruptcy_party_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '唯一索引id',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案号',
  `related_person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '相关人名称',
  `party_role_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人角色类型',
  `party_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人类型',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `public_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公开时间',
  `is_deleted` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否删除',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='破产案件当事人表';

-- gkx.dwd_org_base_info_en_paper_rel definition

CREATE TABLE `dwd_org_base_info_en_paper_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构身份唯一id，用于关联其它表。',
  `base_external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构外部唯一标识',
  `paper_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `paper_doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_dobiepr_org_id_paper_id` (`org_id`,`paper_id`) USING BTREE,
  KEY `idx_dobiepr_org_id` (`org_id`(191)) USING BTREE,
  KEY `idx_dobiepr_base_external_id` (`base_external_id`(191)) USING BTREE,
  KEY `idx_dobiepr_paper_id` (`paper_id`) USING BTREE,
  KEY `idx_dobiepr_paper_doi` (`paper_doi`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内机构-外文论文关联表';

-- gkx.dwd_org_base_info_financing_meta_rel definition

CREATE TABLE `dwd_org_base_info_financing_meta_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构身份唯一id，用于关联其它表。',
  `base_external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构外部唯一标识',
  `metadata_id` int NOT NULL DEFAULT '0' COMMENT '金融元数据唯一标识。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_dobifmr_org_id_metadata_id` (`org_id`,`metadata_id`) USING BTREE,
  KEY `idx_dobifmr_org_id` (`org_id`(191)) USING BTREE,
  KEY `idx_dobifmr_base_external_id` (`base_external_id`(191)) USING BTREE,
  KEY `idx_dobifmr_metadata_id` (`metadata_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内机构-金融数据关联表';

-- gkx.dwd_org_base_info_financing_metadata_rel definition

CREATE TABLE `dwd_org_base_info_financing_metadata_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联id',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '机构身份唯一id，用于关联其它表',
  `base_external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '机构社会信用代码',
  `metadata_id` bigint NOT NULL COMMENT '数列的唯一标识符',
  `business_data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据来源',
  `source_created_user` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '创建人',
  `source_updated_user` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '更新人',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`,`org_id`) USING BTREE,
  KEY `idx_dwd_org_base_info_financing_metadata_rel_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_base_info_financing_metadata_rel_base_external_id` (`base_external_id`) USING BTREE,
  KEY `idx_dwd_org_base_info_financing_metadata_rel_metadata_id` (`metadata_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='国内机构-金融数据关联表';

-- gkx.dwd_org_base_info_patent_rel definition

CREATE TABLE `dwd_org_base_info_patent_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构身份唯一id，用于关联其它表。',
  `base_external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构外部唯一标识',
  `patent_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利记录唯一标识，用于关联专利明细。',
  `publication_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利公开或公告时使用的文献编号。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_dobiopr_org_id_patent_id` (`org_id`,`patent_id`) USING BTREE,
  KEY `idx_dobiopr_org_id` (`org_id`(191)) USING BTREE,
  KEY `idx_dobiopr_base_external_id` (`base_external_id`(191)) USING BTREE,
  KEY `idx_dobiopr_patent_id` (`patent_id`) USING BTREE,
  KEY `idx_dobiopr_publication_number` (`publication_number`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内机构-专利关联表';

-- gkx.dwd_org_base_info_zh_policies_rel definition

CREATE TABLE `dwd_org_base_info_zh_policies_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构身份唯一id，用于关联其它表。',
  `base_external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构外部唯一标识',
  `policies_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '国内政策表的唯一主键标识。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_dobizpol_org_id_policies_id` (`org_id`,`policies_id`) USING BTREE,
  KEY `idx_dobizpol_org_id` (`org_id`(191)) USING BTREE,
  KEY `idx_dobizpol_base_external_id` (`base_external_id`(191)) USING BTREE,
  KEY `idx_dobizpol_policies_id` (`policies_id`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内机构-国内政策关联表';

-- gkx.dwd_org_base_info_zh_project_rel definition

CREATE TABLE `dwd_org_base_info_zh_project_rel` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联id',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构身份唯一id，用于关联其它表。',
  `base_external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '机构外部唯一标识',
  `project_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '项目记录的唯一主键标识。',
  `project_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '项目在管理系统中的编号。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_dobizpr_org_id_project_id` (`org_id`,`project_id`) USING BTREE,
  KEY `idx_dobizpr_org_id` (`org_id`(191)) USING BTREE,
  KEY `idx_dobizpr_base_external_id` (`base_external_id`(191)) USING BTREE,
  KEY `idx_dobizpr_project_id` (`project_id`) USING BTREE,
  KEY `idx_dobizpr_project_number` (`project_number`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内机构-国内项目关联表';

-- gkx.dwd_org_bid_info definition

CREATE TABLE `dwd_org_bid_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `tender_org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `tender_name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '采购单位名称',
  `tender_external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '采购单位统一社会信用代码',
  `winner_org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `winner_name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '中标单位名称',
  `winner_external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '中标单位统一社会信用代码',
  `announcement_title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '公告标题',
  `announcement_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '中标成交信息',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_bid_info_tender_winner_title` (`tender_org_id`,`winner_org_id`,`announcement_title`(191)) USING BTREE,
  KEY `idx_dwd_org_bid_info_tender_external_id` (`tender_external_id`) USING BTREE,
  KEY `idx_dwd_org_bid_info_winner_external_id` (`winner_external_id`) USING BTREE,
  KEY `idx_dwd_org_bid_info_tender_org_id` (`tender_org_id`) USING BTREE,
  KEY `idx_dwd_org_bid_info_winner_org_id` (`winner_org_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内机构招投标事件';

-- gkx.dwd_org_bid_info_bak_20260710 definition

CREATE TABLE `dwd_org_bid_info_bak_20260710` (
  `tender_org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '采购单位id',
  `tender_name_cn` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '采购单位名称',
  `tender_social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '采购单位统一社会信用代码',
  `winner_org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '中标单位id',
  `winner_name_cn` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '中标单位名称',
  `winner_social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '中标单位统一社会信用代码',
  `announcement_title` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '公告标题',
  `announcement_content` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '中标成交信息',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构招投标事件';

-- gkx.dwd_org_change_record_info definition

CREATE TABLE `dwd_org_change_record_info` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `update_content` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '变更类型',
  `current_name` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '变更前内容',
  `update_name` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '变更后内容',
  `update_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '变更日期',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构工商变更信息';

-- gkx.dwd_org_changerecord_info definition

CREATE TABLE `dwd_org_changerecord_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `update_content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '变更类型',
  `current_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '变更前内容',
  `update_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '变更后内容',
  `update_date` date NOT NULL COMMENT '变更日期',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_changerecord_info_org_id_update_date_content` (`org_id`,`update_date`,`update_content`) USING BTREE,
  KEY `idx_dwd_org_changerecord_info_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_changerecord_info_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_changerecord_info_update_date` (`update_date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='工商变更信息';

-- gkx.dwd_org_company_abnormal definition

CREATE TABLE `dwd_org_company_abnormal` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `abnormal_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '经营异常记录唯一标识id。',
  `abn_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '列入原因',
  `abn_date` date DEFAULT NULL COMMENT '列入时间',
  `abn_org` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '列入机关',
  `remove_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '移除原因',
  `remove_date` date DEFAULT NULL COMMENT '移除时间',
  `remove_org` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '移除机关',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标记',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '状态',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_company_abnormal_abnormal_id` (`abnormal_id`) USING BTREE,
  KEY `idx_dwd_org_company_abnormal_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_company_abnormal_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='经营异常';

-- gkx.dwd_org_company_abnormal_bak_20260710 definition

CREATE TABLE `dwd_org_company_abnormal_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `abnormal_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '经营异常记录id',
  `abn_reason` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '列入原因',
  `abn_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '列入时间',
  `abn_org` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '列入机关',
  `remove_reason` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '移除原因',
  `remove_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '移除时间',
  `remove_org` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '移除机关',
  `use_flag` int DEFAULT NULL COMMENT '使用标记',
  `status_code` int DEFAULT NULL COMMENT '状态',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构经营异常事件';

-- gkx.dwd_org_company_chattel definition

CREATE TABLE `dwd_org_company_chattel` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `reg_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '登记编号',
  `reg_date` date DEFAULT NULL COMMENT '登记日期',
  `reg_org` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '登记机关',
  `guarantee_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '被担保债权种类',
  `guarantee_amount` decimal(20,2) DEFAULT NULL COMMENT '被担保债权数额',
  `guarantee_scope` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '担保范围',
  `public_date` date DEFAULT NULL COMMENT '公示日期',
  `debt_term` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '债务人履行债务的期限',
  `debt_remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '主债权信息备注',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '状态',
  `cancel_date` date DEFAULT NULL COMMENT '注销日期',
  `cancel_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '注销原因',
  `status_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '状态代码',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标记',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_company_chattel_reg_no` (`reg_no`) USING BTREE,
  KEY `idx_dwd_org_company_chattel_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_company_chattel_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='动产抵押';

-- gkx.dwd_org_company_chattel_bak_20260710 definition

CREATE TABLE `dwd_org_company_chattel_bak_20260710` (
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `reg_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '登记编号',
  `reg_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '登记日期',
  `reg_org` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '登记机关',
  `guarantee_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '被担保债权种类',
  `guarantee_amount` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '被担保债权数额',
  `guarantee_scope` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '担保范围',
  `public_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公示日期',
  `debt_term` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '债务人履行债务的期限',
  `debt_remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '主债权信息备注',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '状态',
  `cancel_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '注销日期',
  `cancel_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '注销原因',
  `status_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '状态代码',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用标记',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='动产抵押表';

-- gkx.dwd_org_company_illegal definition

CREATE TABLE `dwd_org_company_illegal` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `sv_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '严重违法记录唯一标识id。',
  `category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '类别',
  `abn_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '列入原因',
  `abn_date` date DEFAULT NULL COMMENT '列入时间',
  `abn_org` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '列入机关',
  `remove_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '移除原因',
  `remove_date` date DEFAULT NULL COMMENT '移除时间',
  `remove_org` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '移除机关',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '状态',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标记',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_company_illegal_sv_id` (`sv_id`) USING BTREE,
  KEY `idx_dwd_org_company_illegal_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_company_illegal_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='严重违法';

-- gkx.dwd_org_company_illegal_bak_20260710 definition

CREATE TABLE `dwd_org_company_illegal_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `sv_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '严重违法记录id',
  `category` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '类别',
  `abn_reason` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '列入原因',
  `abn_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '列入时间',
  `abn_org` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '列入机关',
  `remove_reason` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '移除原因',
  `remove_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '移除时间',
  `remove_org` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '移除机关',
  `status` int DEFAULT NULL COMMENT '状态',
  `use_flag` int DEFAULT NULL COMMENT '使用标记',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构严重违法';

-- gkx.dwd_org_company_justice definition

CREATE TABLE `dwd_org_company_justice` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `judicial_assist_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '司法协助记录唯一标识id。',
  `executed_person` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '被执行人',
  `equity_amount` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '股权数额',
  `exec_court` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '执行法院',
  `exec_notice_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '执行通知书文号',
  `type_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '类型|状态',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标记',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '状态',
  `executed_person_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '被执行人类型',
  `executed_company_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '被执行人的company_id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_company_justice_judicial_assist_id` (`judicial_assist_id`) USING BTREE,
  KEY `idx_dwd_org_company_justice_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_company_justice_executed_company_id` (`executed_company_id`) USING BTREE,
  KEY `idx_dwd_org_company_justice_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='股权冻结';

-- gkx.dwd_org_company_justice_bak_20260710 definition

CREATE TABLE `dwd_org_company_justice_bak_20260710` (
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `judicial_assist_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '司法协助记录id',
  `executed_person` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '被执行人',
  `equity_amount` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '股权数额',
  `exec_court` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '执行法院',
  `exec_notice_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '执行通知书文号',
  `type_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '类型|状态',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用标记',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '状态',
  `executed_person_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '被执行人类型',
  `executed_company_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '被执行人的company_id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='股权冻结表';

-- gkx.dwd_org_company_pledge definition

CREATE TABLE `dwd_org_company_pledge` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `pledge_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '股权出质记录唯一标识id。',
  `reg_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '登记编号',
  `pledgor` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '出质人',
  `pledgor_id_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '出质人证件号码',
  `pledgee` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '质权人',
  `pledgee_id_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '质权人证件号码',
  `equity_amount` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '出质股权数额',
  `pledge_reg_date` date DEFAULT NULL COMMENT '股权出质设立登记日期',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '状态',
  `public_date` date DEFAULT NULL COMMENT '公示日期',
  `cancel_date` date DEFAULT NULL COMMENT '注销日期',
  `cancel_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '注销原因',
  `invalid_date` date DEFAULT NULL COMMENT '失效时间',
  `invalid_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '失效原因',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标记',
  `status_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '状态代码',
  `province_abbr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '省份简称',
  `pledgor_company_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构出质人的company_id',
  `pledgor_company_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构出质人名称',
  `pledgor_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构出质人统一社会信用代码',
  `pledgor_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '出质人类型',
  `pledgee_company_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构质权人的company_id',
  `pledgee_company_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构质权人名称',
  `pledgee_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构质权人统一社会信用代码',
  `pledgee_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '质权人类型',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_company_pledge_pledge_id` (`pledge_id`) USING BTREE,
  KEY `idx_dwd_org_company_pledge_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_company_pledge_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_company_pledge_pledgor_company_id` (`pledgor_company_id`) USING BTREE,
  KEY `idx_dwd_org_company_pledge_pledgor_credit_code` (`pledgor_credit_code`) USING BTREE,
  KEY `idx_dwd_org_company_pledge_pledgee_company_id` (`pledgee_company_id`) USING BTREE,
  KEY `idx_dwd_org_company_pledge_pledgee_credit_code` (`pledgee_credit_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='股权出质';

-- gkx.dwd_org_company_pledge_bak_20260710 definition

CREATE TABLE `dwd_org_company_pledge_bak_20260710` (
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `pledge_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '股权出质记录id',
  `reg_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '登记编号',
  `pledgor` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '出质人',
  `pledgor_id_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '出质人证件号码',
  `pledgee` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '质权人',
  `pledgee_id_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '质权人证件号码',
  `equity_amount` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '出质股权数额',
  `pledge_reg_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '股权出质设立登记日期',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '状态',
  `public_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公示日期',
  `cancel_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '注销日期',
  `cancel_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '注销原因',
  `invalid_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '失效时间',
  `invalid_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '失效原因',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用标记',
  `status_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '状态代码',
  `province_abbr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '省份简称',
  `pledgor_company_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构出质人的company_id',
  `pledgor_company_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构出质人名称',
  `pledgor_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构出质人统一社会信用代码',
  `pledgor_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '出质人类型',
  `pledgee_company_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构质权人的company_id',
  `pledgee_company_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构质权人名称',
  `pledgee_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构质权人统一社会信用代码',
  `pledgee_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '质权人类型',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='股权出质表';

-- gkx.dwd_org_company_punish definition

CREATE TABLE `dwd_org_company_punish` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `penalty_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '行政处罚记录唯一标识id。',
  `decision_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '决定书文号',
  `violation_type` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '违法行为类型',
  `penalty_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '行政处罚内容',
  `decision_org` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '决定机关',
  `penalty_date` date DEFAULT NULL COMMENT '处罚决定日期',
  `public_date` date DEFAULT NULL COMMENT '公示日期',
  `penalty_basis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '处罚依据',
  `violation_fact` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '主要违法事实',
  `penalty_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '处罚种类',
  `fine_amount` decimal(20,2) DEFAULT NULL COMMENT '罚款金额',
  `confiscate_amount` decimal(20,2) DEFAULT NULL COMMENT '没收金额',
  `license_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '暂扣或吊销证照名称及编号',
  `validity_period` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '处罚有效期',
  `public_deadline` date DEFAULT NULL COMMENT '公示截止日期',
  `remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '备注',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标记',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '状态',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_company_punish_penalty_id` (`penalty_id`) USING BTREE,
  KEY `idx_dwd_org_company_punish_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_company_punish_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='行政处罚';

-- gkx.dwd_org_company_punish_bak_20260710 definition

CREATE TABLE `dwd_org_company_punish_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `penalty_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '行政处罚记录id',
  `decision_no` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '决定书文号',
  `violation_type` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '违法行为类型',
  `penalty_content` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '行政处罚内容',
  `decision_org` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '决定机关',
  `penalty_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '处罚决定日期',
  `public_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '公示日期',
  `penalty_basis` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '处罚依据',
  `violation_fact` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '主要违法事实',
  `penalty_type` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '处罚种类',
  `fine_amount` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '罚款金额',
  `confiscate_amount` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '没收金额',
  `license_info` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '暂扣或吊销证照名称及编号',
  `validity_period` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '处罚有效期',
  `public_deadline` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '公示截止日期',
  `remark` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '备注',
  `use_flag` int DEFAULT NULL COMMENT '使用标记',
  `status_code` int DEFAULT NULL COMMENT '状态代码',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构行政处罚记录';

-- gkx.dwd_org_executive_info definition

CREATE TABLE `dwd_org_executive_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `executives_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '高管姓名',
  `executives_position` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '职位名称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_executive_info_org_id_executives_name_execut_c813fe12` (`org_id`,`executives_name`,`executives_position`) USING BTREE,
  KEY `idx_dwd_org_executive_info_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_executive_info_org_id` (`org_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内机构高管信息';

-- gkx.dwd_org_executive_info_bak_20260710 definition

CREATE TABLE `dwd_org_executive_info_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `executives_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '高管姓名',
  `executives_position` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '职位名称',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构高管信息';

-- gkx.dwd_org_financing_info definition

CREATE TABLE `dwd_org_financing_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `funding_round` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '融资轮次',
  `funding_amount` decimal(20,2) DEFAULT NULL COMMENT '获投金额(元)',
  `funding_currency_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '金额币种',
  `post_valuation` decimal(20,2) DEFAULT NULL COMMENT '投后估值',
  `completion_date` date DEFAULT NULL COMMENT '融资完成时间',
  `investors_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '投资方列表',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_financing_info_org_id_completion_date_round` (`org_id`,`completion_date`,`funding_round`) USING BTREE,
  KEY `idx_dwd_org_financing_info_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内机构融资事件';

-- gkx.dwd_org_financing_info_bak_20260710 definition

CREATE TABLE `dwd_org_financing_info_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `funding_round` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '融资轮次',
  `funding_amount` bigint DEFAULT NULL COMMENT '获投金额',
  `funding_currency_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '金额币种',
  `post_valuation` bigint DEFAULT NULL COMMENT '投后估值',
  `completion_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '融资完成时间',
  `investors_name` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '投资方列表',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构融资事件';

-- gkx.dwd_org_hels_info definition

CREATE TABLE `dwd_org_hels_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `org_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '高校/科研机构名称(中文)',
  `org_name_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '高校/科研机构名称(英文)',
  `org_desc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '高校/科研机构描述',
  `est_year` date DEFAULT NULL COMMENT '建立时间',
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '地址(国家、区域、城市)',
  `addr_lng` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '地址对应经度',
  `addr_lat` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '地址对应维度',
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '地址所在省',
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '地址所在市',
  `univ_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '高校类型',
  `web_link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '官方网址',
  `postal_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '邮政编码',
  `email` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '电子邮箱',
  `contact_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '联系电话',
  `fax_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '传真号码',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_hels_info_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_hels_info_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='高校/科研机构信息';

-- gkx.dwd_org_hels_info_bak_20260710 definition

CREATE TABLE `dwd_org_hels_info_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '高校id',
  `name_cn` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `org_name` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '高校/科研机构名称(中文)',
  `org_name_en` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '高校/科研机构名称(英文)',
  `org_desc` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '高校/科研机构描述',
  `address` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '地址(国家、区域、城市)',
  `addr_lng` double DEFAULT NULL COMMENT '地址对应经度',
  `addr_lat` double DEFAULT NULL COMMENT '地址对应维度',
  `province` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '地址所在省',
  `city` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '地址所在市',
  `univ_type` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '高校类型',
  `web_link` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '官方网址',
  `postal_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '邮政编码',
  `contact_number` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '联系电话',
  `email` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '电子邮箱',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据高校与科研机构信息';

-- gkx.dwd_org_important_news_info definition

CREATE TABLE `dwd_org_important_news_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `news_title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '资讯标题',
  `news_date` date DEFAULT NULL COMMENT '资讯日期',
  `news_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '资讯内容',
  `original_textlink` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '咨询原文链接',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_important_news_info_org_id_news_date_title` (`org_id`,`news_date`,`news_title`(191)) USING BTREE,
  KEY `idx_dwd_org_important_news_info_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内机构重点资讯';

-- gkx.dwd_org_important_news_info_bak_20260710 definition

CREATE TABLE `dwd_org_important_news_info_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `news_title` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '资讯标题',
  `news_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '资讯日期',
  `news_content` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '资讯内容',
  `original_textlink` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '咨询原文链接',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构重点资讯';

-- gkx.dwd_org_industry_chain_dtl definition

CREATE TABLE `dwd_org_industry_chain_dtl` (
  `chain_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '产业链代码',
  `chain_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '产业链名称',
  `node_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '节点代码',
  `node_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '节点名称',
  `antitypic` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业id',
  `credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `chain_score` decimal(20,2) DEFAULT NULL COMMENT '产业链评分',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='产业关联企业信息';

-- gkx.dwd_org_industry_chain_pat_dtl definition

CREATE TABLE `dwd_org_industry_chain_pat_dtl` (
  `chain_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '产业链代码',
  `chain_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '产业链名称',
  `node_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '节点代码',
  `node_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '节点名称',
  `apno` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '申请号',
  `apdt` date DEFAULT NULL COMMENT '申请日',
  `pat_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '专利名称',
  `pn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公布(公告)号',
  `pbdt` date DEFAULT NULL COMMENT '公布(公告)日',
  `current_assign` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '申请(专利权)人',
  `inventors` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '发明(设计)人',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='产业链关联专利信息';

-- gkx.dwd_org_industry_chain_prod_dtl definition

CREATE TABLE `dwd_org_industry_chain_prod_dtl` (
  `chain_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '产业链代码',
  `chain_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '产业链名称',
  `antitypic` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业id',
  `company_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业名称',
  `credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `tech_product` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '主营产品名称',
  `tech_product_s` int DEFAULT NULL COMMENT '主营产品排序',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='产业链企业关联产品信息';

-- gkx.dwd_org_innovation_carrier definition

CREATE TABLE `dwd_org_innovation_carrier` (
  `carrier_type` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '载体/平台/中心类型',
  `carrier_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '载体/平台/中心名称',
  `carrier_level` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '载体/平台/中心级别',
  `create_year` int DEFAULT NULL COMMENT '组建/认定/立项年份',
  `area` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '载体/平台/中心所在地区',
  `area_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '所在地区行政区划代码',
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `org_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '关联单位名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `announcement` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '公告名称',
  `publish_org` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '发布单位',
  `publish_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '发布日期',
  `source_url` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '来源链接'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构创新载体信息';

-- gkx.dwd_org_invest_info definition

CREATE TABLE `dwd_org_invest_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `inv_org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `inv_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '被投资企业名称',
  `inv_external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '被投资企业统一社会信用代码',
  `investment_amount` decimal(20,2) DEFAULT NULL COMMENT '投资金额(元)',
  `investment_ratio` decimal(20,2) DEFAULT NULL COMMENT '股权占比(%)',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_invest_info_org_id_inv_org_id` (`org_id`,`inv_org_id`) USING BTREE,
  KEY `idx_dwd_org_invest_info_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_invest_info_inv_external_id` (`inv_external_id`) USING BTREE,
  KEY `idx_dwd_org_invest_info_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_invest_info_inv_org_id` (`inv_org_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='投资事件';

-- gkx.dwd_org_invest_info_bak_20260710 definition

CREATE TABLE `dwd_org_invest_info_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `inv_org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '被投企业id',
  `inv_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '被投资企业名称',
  `inv_social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '被投资企业统一社会信用代码',
  `investment_amount` double DEFAULT NULL COMMENT '投资金额(元)',
  `investment_ratio` double DEFAULT NULL COMMENT '股权占比(%)',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构投资事件';

-- gkx.dwd_org_merger_acquisition_info definition

CREATE TABLE `dwd_org_merger_acquisition_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `acquiring_org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `acquiring_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '发起收购企业名称',
  `acquired_org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `acquired_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '被收购企业名称',
  `ma_amount` decimal(20,2) DEFAULT NULL COMMENT '并购金额(元)',
  `currency_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '并购金额币种',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  KEY `idx_dwd_org_merger_acquisition_info_org_pair` (`acquiring_org_id`,`acquired_org_id`) USING BTREE,
  KEY `idx_dwd_org_merger_acquisition_info_acquiring_org_id` (`acquiring_org_id`) USING BTREE,
  KEY `idx_dwd_org_merger_acquisition_info_acquired_org_id` (`acquired_org_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='并购事件';

-- gkx.dwd_org_merger_acquisition_info_bak_20260710 definition

CREATE TABLE `dwd_org_merger_acquisition_info_bak_20260710` (
  `event_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '公告日期',
  `ma_amount` double DEFAULT NULL COMMENT '交易金额',
  `currency_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '币种',
  `acquiring_org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '发起收购企业id',
  `acquiring_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '发起收购企业名称',
  `acquired_org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '被收购企业id',
  `acquired_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '被收购企业',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构并购事件';

-- gkx.dwd_org_opt_judicial_case definition

CREATE TABLE `dwd_org_opt_judicial_case` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `company_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '企业登记名称。',
  `reg_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '注册号',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `case_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '司法案件记录唯一标识id。',
  `case_title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '案件标题',
  `case_type_tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案件类型标签',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案号',
  `case_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案由',
  `case_role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案件身份',
  `current_procedure` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当前审理程序',
  `procedure_date` date DEFAULT NULL COMMENT '当前审理程序日期',
  `data_use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据使用标识',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_opt_judicial_case_case_id` (`case_id`) USING BTREE,
  KEY `idx_dwd_org_opt_judicial_case_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_opt_judicial_case_org_id` (`org_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='司法案件';

-- gkx.dwd_org_opt_judicial_case_bak_20260710 definition

CREATE TABLE `dwd_org_opt_judicial_case_bak_20260710` (
  `company_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '企业名称',
  `reg_no` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '注册号',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `case_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '司法案件唯一标识',
  `case_title` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '案件标题',
  `case_type_tag` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '案件类型标签',
  `case_no` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '案号',
  `case_cause` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '案由',
  `case_role` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '案件身份',
  `current_procedure` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '当前审理程序',
  `procedure_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '当前审理程序日期',
  `data_use_flag` int DEFAULT NULL COMMENT '数据使用标识',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构司法案件事件';

-- gkx.dwd_org_org_product_info definition

CREATE TABLE `dwd_org_org_product_info` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `industry_class` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '公司行业分类',
  `main_activities` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '公司经营范围',
  `description` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '业务描述',
  `main_prod` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '主要产品',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构经营信息';

-- gkx.dwd_org_product_info definition

CREATE TABLE `dwd_org_product_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `industry_class` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '公司行业分类',
  `main_activities` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '公司经营范围',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '业务描述',
  `main_prod` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '主要产品',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_product_info_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_product_info_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内机构经营信息';

-- gkx.dwd_org_recruit_info definition

CREATE TABLE `dwd_org_recruit_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `job_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '岗位',
  `job_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '工作描述',
  `work_place` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '工作地点',
  `release_date` date DEFAULT NULL COMMENT '发布日期',
  `hiring_number` bigint DEFAULT NULL COMMENT '招聘人数',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_recruit_info_org_id_release_date_job_title` (`org_id`,`release_date`,`job_title`) USING BTREE,
  KEY `idx_dwd_org_recruit_info_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='招聘信息';

-- gkx.dwd_org_recruit_info_bak_20260710 definition

CREATE TABLE `dwd_org_recruit_info_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `job_title` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '岗位',
  `job_description` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '工作描述',
  `work_place` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '工作地点',
  `release_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '发布日期',
  `hiring_number` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '招聘人数',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据招聘信息';

-- gkx.dwd_org_reg_info definition

CREATE TABLE `dwd_org_reg_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '所在省份',
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '所在城市',
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '公司地址',
  `addr_lng` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '地址对应经度',
  `addr_lat` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '地址对应维度',
  `postal_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '邮政编码',
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '联系电话',
  `email` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '电子邮箱',
  `lerep` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法人名字',
  `org_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构类型',
  `org_size` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '企业规模',
  `registration_org` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '登记机关',
  `incorporation_year` bigint DEFAULT NULL COMMENT '成立年份',
  `incorporation_date` date DEFAULT NULL COMMENT '成立日期',
  `start_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '经营期限自',
  `end_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '经营期限至',
  `listing_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '上市状态',
  `listing_date` date DEFAULT NULL COMMENT '上市日期',
  `registered_capital_value` decimal(20,2) DEFAULT NULL COMMENT '注册资本(本币元)',
  `capital_currency_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '资本货币代码',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_reg_info_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_reg_info_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='机构基本信息';

-- gkx.dwd_org_reg_info_bak_20260710 definition

CREATE TABLE `dwd_org_reg_info_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `province` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '所在省份',
  `city` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '所在城市',
  `address` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '公司地址',
  `addr_lng` double DEFAULT NULL COMMENT '地址经度',
  `addr_lat` double DEFAULT NULL COMMENT '地址纬度',
  `postal_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '邮编',
  `lerep` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '法人代表',
  `registration_org` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '登记机关',
  `incorporation_year` int DEFAULT NULL COMMENT '成立年',
  `incorporation_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '成立日期',
  `start_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '经营期限自',
  `end_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '经营期限至',
  `listing_status` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '上市状态',
  `listing_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '上市日期',
  `registered_capital_value` double DEFAULT NULL COMMENT '注册资本金',
  `capital_currency_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '资本货币代码',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构基本信息';

-- gkx.dwd_org_risk_court_announcement definition

CREATE TABLE `dwd_org_risk_court_announcement` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `notice_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '法院公告唯一标识id。',
  `notice_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公告号',
  `notice_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公告名称',
  `notice_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公告类型',
  `notice_type_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公告类型名称',
  `notice_date` date DEFAULT NULL COMMENT '公告日期',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案号',
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '标题',
  `notice_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '公告内容',
  `court_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法院名称',
  `handle_level` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '处理等级',
  `handle_level_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '处理等级名称',
  `judge` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法官',
  `judge_phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法官电话',
  `mobile_phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '手机号',
  `plaintiff` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '原告',
  `party` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人',
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '省份',
  `case_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案由',
  `notice_year` bigint DEFAULT NULL COMMENT '公告年份',
  `publish_date` date DEFAULT NULL COMMENT '公告刊登日期',
  `publish_page_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公告刊登版面页码',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标志',
  `original_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '原始连接URL',
  `content_md5` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公告内容的md5值',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否不展示',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_risk_court_announcement_notice_id` (`notice_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='法院公告';

-- gkx.dwd_org_risk_court_announcement_bak_20260710 definition

CREATE TABLE `dwd_org_risk_court_announcement_bak_20260710` (
  `notice_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告id',
  `notice_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告号',
  `notice_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告名称',
  `notice_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告类型',
  `notice_type_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告类型名称',
  `notice_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告日期',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案号',
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '标题',
  `notice_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '公告内容',
  `court_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '法院名称',
  `handle_level` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '处理等级',
  `handle_level_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '处理等级名称',
  `judge` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '法官',
  `judge_phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '法官电话',
  `mobile_phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '手机号',
  `plaintiff` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '原告',
  `party` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人',
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '省份',
  `case_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案由',
  `notice_year` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告年份',
  `publish_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告刊登日期',
  `publish_page_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告刊登版面页码',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用标志',
  `original_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '原始连接URL',
  `content_md5` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告内容的md5值',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否不展示',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='法院公告表';

-- gkx.dwd_org_risk_court_announcement_list definition

CREATE TABLE `dwd_org_risk_court_announcement_list` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `notice_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '法院公告唯一标识id，关联法院公告表。',
  `party_identity` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人身份',
  `party_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人类型',
  `party_role_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人角色类型',
  `related_person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '相关人名称',
  `publish_date` date DEFAULT NULL COMMENT '公告刊登日期',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标志',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否不展示',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_risk_court_announcement_list_notice_id_relat_4d75ee48` (`notice_id`,`related_person_name`) USING BTREE,
  KEY `idx_dwd_org_risk_court_announcement_list_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_risk_court_announcement_list_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_risk_court_announcement_list_notice_id` (`notice_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='法院公告当事人';

-- gkx.dwd_org_risk_court_announcement_list_bak_20260710 definition

CREATE TABLE `dwd_org_risk_court_announcement_list_bak_20260710` (
  `notice_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告id',
  `party_identity` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人身份',
  `party_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人类型',
  `party_role_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人角色类型',
  `related_person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '相关人名称',
  `publish_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告刊登日期',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用标志',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否不展示',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='法院公告当事人表';

-- gkx.dwd_org_risk_court_filed_case definition

CREATE TABLE `dwd_org_risk_court_filed_case` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `case_unique_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '案件唯一标识id。',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案号',
  `norm_case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '归一化案号',
  `case_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案由',
  `trial_procedure` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '审理程序',
  `case_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案件状态',
  `norm_case_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '归一化后案件状态',
  `filing_date` date DEFAULT NULL COMMENT '立案日期',
  `closing_date` date DEFAULT NULL COMMENT '结案日期',
  `hearing_date` date DEFAULT NULL COMMENT '开庭日期',
  `court_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法院',
  `undertaking_dept` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '承办部门',
  `judge` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法官',
  `assistant_judge` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '助理法官',
  `party_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '当事人信息',
  `court_province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法院所在省',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标志',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_risk_court_filed_case_case_unique_id` (`case_unique_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='法院立案';

-- gkx.dwd_org_risk_court_filed_case_bak_20260710 definition

CREATE TABLE `dwd_org_risk_court_filed_case_bak_20260710` (
  `case_unique_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案件唯一id',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案号',
  `norm_case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '归一化案号',
  `case_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案由',
  `trial_procedure` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '审理程序',
  `case_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案件状态',
  `norm_case_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '归一化后案件状态',
  `filing_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '立案日期',
  `closing_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '结案日期',
  `hearing_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '开庭日期',
  `court_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '法院',
  `undertaking_dept` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '承办部门',
  `judge` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '法官',
  `assistant_judge` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '助理法官',
  `party_info` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人信息',
  `court_province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '法院所在省',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用标志',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='法院立案表';

-- gkx.dwd_org_risk_court_filed_case_litigant definition

CREATE TABLE `dwd_org_risk_court_filed_case_litigant` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `case_unique_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '案件唯一标识id，关联法院立案表。',
  `filing_date` date DEFAULT NULL COMMENT '立案日期',
  `party_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '当事人名称',
  `party_role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人角色',
  `classified_org_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '归类后企业类型',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标志',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_risk_court_filed_case_litigant_case_unique_i_78e449c4` (`case_unique_id`,`party_name`) USING BTREE,
  KEY `idx_dwd_org_risk_court_filed_case_litigant_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_risk_court_filed_case_litigant_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_risk_court_filed_case_litigant_case_unique_id` (`case_unique_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='法院立案当事人';

-- gkx.dwd_org_risk_court_filed_case_litigant_bak_20260710 definition

CREATE TABLE `dwd_org_risk_court_filed_case_litigant_bak_20260710` (
  `case_unique_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案件唯一id',
  `filing_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '立案日期',
  `party_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人名称',
  `party_role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人角色',
  `classified_org_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '归类后企业类型',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用标志',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='法院立案当事人表';

-- gkx.dwd_org_risk_court_notice definition

CREATE TABLE `dwd_org_risk_court_notice` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `notice_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '开庭公告唯一标识id。',
  `court_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法院',
  `courtroom` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法庭',
  `undertaking_dept` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '承办部门',
  `hearing_date` date DEFAULT NULL COMMENT '开庭日期',
  `scheduling_date` date DEFAULT NULL COMMENT '排期日期',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案号',
  `case_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案由',
  `case_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案件类型',
  `jurisdiction_area` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案件管辖区域',
  `plaintiff_appellant` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '原告上诉人',
  `defendant_appellee` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '被告被上诉人',
  `party` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人',
  `presiding_judge` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '审判长主审人',
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '标题',
  `notice_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '公告内容',
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '省份',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标志',
  `original_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '原始连接URL',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否不展示',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_risk_court_notice_notice_id` (`notice_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='开庭公告';

-- gkx.dwd_org_risk_court_notice_bak_20260710 definition

CREATE TABLE `dwd_org_risk_court_notice_bak_20260710` (
  `notice_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告id',
  `court_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '法院',
  `courtroom` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '法庭',
  `undertaking_dept` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '承办部门',
  `hearing_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '开庭日期',
  `scheduling_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '排期日期',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案号',
  `case_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案由',
  `case_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案件类型',
  `jurisdiction_area` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案件管辖区域',
  `plaintiff_appellant` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '原告上诉人',
  `defendant_appellee` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '被告被上诉人',
  `party` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人',
  `presiding_judge` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '审判长主审人',
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '标题',
  `notice_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '公告内容',
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '省份',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用标志',
  `original_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '原始连接URL',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否不展示',
  `data_source_2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源（重复字段，已重命名避免冲突）',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='开庭公告表';

-- gkx.dwd_org_risk_court_notice_list definition

CREATE TABLE `dwd_org_risk_court_notice_list` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `notice_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '开庭公告唯一标识id，关联开庭公告表。',
  `party_role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人角色',
  `party_role_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人角色类型',
  `party_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人类型',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `related_person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '相关人名称',
  `hearing_date` date DEFAULT NULL COMMENT '开庭日期',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标志',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否不展示',
  `case_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案由',
  `reserve_field` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '预留字段',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_risk_court_notice_list_notice_id_related_person_name` (`notice_id`,`related_person_name`) USING BTREE,
  KEY `idx_dwd_org_risk_court_notice_list_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_risk_court_notice_list_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_risk_court_notice_list_notice_id` (`notice_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='开庭公告当事人';

-- gkx.dwd_org_risk_court_notice_list_bak_20260710 definition

CREATE TABLE `dwd_org_risk_court_notice_list_bak_20260710` (
  `notice_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告id',
  `party_role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人角色',
  `party_role_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人角色类型',
  `party_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人类型',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `related_person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '相关人名称',
  `hearing_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '开庭日期',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用标志',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否不展示',
  `case_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案由',
  `reserve_field` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '预留字段',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='开庭公告当事人表';

-- gkx.dwd_org_risk_lawsuit definition

CREATE TABLE `dwd_org_risk_lawsuit` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `judgment_doc_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '裁判文书网文书唯一标识id。',
  `defendant` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '被告',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案号',
  `case_type_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案件类型编码',
  `case_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案件类型',
  `doc_type_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文书类型编码',
  `doc_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文书类型',
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '省份',
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '地市',
  `district` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '区县',
  `main_doc_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '主表docid',
  `court_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法院名称',
  `trial_procedure` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '审理程序名称',
  `judgment_year` bigint DEFAULT NULL COMMENT '裁判年份',
  `judgment_date` date DEFAULT NULL COMMENT '裁判日期',
  `case_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案由',
  `doc_title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '文书标题',
  `doc_full_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '文书全文',
  `publish_date` date DEFAULT NULL COMMENT '公布日期',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标志',
  `original_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '原始连接URL',
  `plaintiff` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '原告',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否不展示',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_risk_lawsuit_judgment_doc_id` (`judgment_doc_id`) USING BTREE,
  KEY `idx_dwd_org_risk_lawsuit_main_doc_id` (`main_doc_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='裁判文书';

-- gkx.dwd_org_risk_lawsuit_bak_20260710 definition

CREATE TABLE `dwd_org_risk_lawsuit_bak_20260710` (
  `judgment_doc_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '裁判文书网文书id',
  `defendant` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '被告',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案号',
  `case_type_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案件类型编码',
  `case_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案件类型',
  `doc_type_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文书类型编码',
  `doc_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文书类型',
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '省份',
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '地市',
  `district` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '区县',
  `main_doc_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '主表docid',
  `court_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '法院名称',
  `trial_procedure` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '审理程序名称',
  `judgment_year` int DEFAULT NULL COMMENT '裁判年份',
  `judgment_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '裁判日期',
  `case_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案由',
  `doc_title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '文书标题',
  `doc_full_text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '文书全文',
  `publish_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公布日期',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用标志',
  `original_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '原始连接URL',
  `plaintiff` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '原告',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否不展示',
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='裁判文书';

-- gkx.dwd_org_risk_lawsuit_list definition

CREATE TABLE `dwd_org_risk_lawsuit_list` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `main_doc_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主表docid，关联裁判文书表。',
  `party_identity` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人身份',
  `party_role_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人角色类型',
  `party_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '当事人类型',
  `related_person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '相关人名称',
  `doc_publish_date` date DEFAULT NULL COMMENT '文书公布日期',
  `case_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案由',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标志',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否不展示',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_risk_lawsuit_list_main_doc_id_related_person_name` (`main_doc_id`,`related_person_name`) USING BTREE,
  KEY `idx_dwd_org_risk_lawsuit_list_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_risk_lawsuit_list_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_risk_lawsuit_list_main_doc_id` (`main_doc_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='裁判文书当事人';

-- gkx.dwd_org_risk_lawsuit_list_bak_20260710 definition

CREATE TABLE `dwd_org_risk_lawsuit_list_bak_20260710` (
  `main_doc_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '主表docid',
  `party_identity` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人身份',
  `party_role_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人角色类型',
  `party_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当事人类型',
  `related_person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '相关人名称',
  `doc_publish_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文书公布日期',
  `case_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案由',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用标志',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否不展示',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='裁判文书当事人表';

-- gkx.dwd_org_risk_shixin definition

CREATE TABLE `dwd_org_risk_shixin` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `dishonest_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '失信被执行人记录唯一标识id。',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `official_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '官网id',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '案号',
  `dishonest_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '失信人名称',
  `gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '性别',
  `age` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '年龄',
  `credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一信用代码',
  `reg_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '企业注册号',
  `display_id_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '展示用证件号码',
  `legal_person` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法定代表人或负责人',
  `exec_court` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '执行法院',
  `province_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '省份id。',
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '省份',
  `dishonest_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '失信人类型',
  `exec_basis_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '执行依据文号',
  `exec_basis_org` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '做出执行依据单位',
  `legal_obligation` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '生效法律文书确定的义务',
  `fulfillment_status` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '被执行人的履行情况',
  `dishonest_behavior` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '失信被执行人行为具体情形',
  `publish_date` date DEFAULT NULL COMMENT '发布时间',
  `filing_date` date DEFAULT NULL COMMENT '立案时间',
  `exec_part` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '执行部分',
  `unexec_part` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '未执行部分',
  `is_history` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否历史数据',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标记',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否不展示',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_risk_shixin_dishonest_id` (`dishonest_id`) USING BTREE,
  KEY `idx_dwd_org_risk_shixin_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_risk_shixin_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_risk_shixin_official_id` (`official_id`) USING BTREE,
  KEY `idx_dwd_org_risk_shixin_province_id` (`province_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='失信被执行人';

-- gkx.dwd_org_risk_shixin_bak_20260710 definition

CREATE TABLE `dwd_org_risk_shixin_bak_20260710` (
  `dishonest_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '失信被执行人id',
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `official_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '官网id',
  `case_no` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '案号',
  `dishonest_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '失信人名称',
  `gender` int DEFAULT NULL COMMENT '性别',
  `age` int DEFAULT NULL COMMENT '年龄',
  `reg_no` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '企业注册号',
  `display_id_no` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '展示用证件号码',
  `legal_person` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '法定代表人或负责人',
  `exec_court` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '执行法院',
  `province_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '省份id',
  `province` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '省份',
  `dishonest_type` int DEFAULT NULL COMMENT '失信人类型',
  `exec_basis_no` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '执行依据文号',
  `exec_basis_org` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '做出执行依据单位',
  `legal_obligation` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '生效法律文书确定的义务',
  `fulfillment_status` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '被执行人的履行情况',
  `dishonest_behavior` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '失信被执行人行为具体情形',
  `publish_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '发布时间',
  `filing_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '立案时间',
  `exec_part` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '执行部分',
  `unexec_part` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '未执行部分',
  `is_history` int DEFAULT NULL COMMENT '是否历史数据',
  `use_flag` int DEFAULT NULL COMMENT '使用标记',
  `is_hidden` int DEFAULT NULL COMMENT '是否不展示',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构失信被执行人记录';

-- gkx.dwd_org_risk_tax_punish definition

CREATE TABLE `dwd_org_risk_tax_punish` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `taxpayer_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '纳税人登记名称。',
  `tax_vio_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '税收违法记录唯一标识id。',
  `report_period` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案件上报期',
  `taxpayer_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '纳税人识别码',
  `org_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '组织机构代码',
  `reg_address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '注册地址',
  `publish_date` date DEFAULT NULL COMMENT '发布日期',
  `legal_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法定代表人或者负责人姓名',
  `legal_gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法定代表人或者负责人性别',
  `legal_id_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法定代表人或者负责人证件类型',
  `legal_id_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法定代表人或者负责人证件号码',
  `finance_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '负有直接责任的财务负责人姓名',
  `finance_gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '负有直接责任的财务负责人性别',
  `finance_id_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '负有直接责任的财务负责人证件类型',
  `finance_id_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '负有直接责任的财务负责人证件号码',
  `agency_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '负有直接责任的中介机构信息及其从业人员信息',
  `case_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案件性质',
  `illegal_fact` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '主要违法事实',
  `punish_basis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '相关法律依据及税务处理处罚情况',
  `tax_authority` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '所属税务机关',
  `original_link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '数据原始连接',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标志',
  `original_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '原始数据来源',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `is_history` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否历史记录，0正常；1历史。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_risk_tax_punish_tax_vio_id` (`tax_vio_id`) USING BTREE,
  KEY `idx_dwd_org_risk_tax_punish_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_risk_tax_punish_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='税收违法';

-- gkx.dwd_org_risk_tax_punish_bak_20260710 definition

CREATE TABLE `dwd_org_risk_tax_punish_bak_20260710` (
  `taxpayer_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '纳税人名称',
  `tax_vio_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '税收违法id',
  `report_period` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '案件上报期',
  `taxpayer_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '纳税人识别码',
  `org_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '组织机构代码',
  `reg_address` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '注册地址',
  `publish_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '发布日期',
  `legal_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '法定代表人或者负责人姓名',
  `legal_gender` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '法定代表人或者负责人性别',
  `legal_id_type` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '法定代表人或者负责人证件类型',
  `legal_id_no` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '法定代表人或者负责人证件号码',
  `case_type` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '案件性质',
  `illegal_fact` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '主要违法事实',
  `punish_basis` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '相关法律依据及税务处理处罚情况',
  `tax_authority` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '所属税务机关',
  `original_link` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据原始连接',
  `use_flag` int DEFAULT NULL COMMENT '使用标志',
  `original_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '原始数据来源',
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `is_history` int DEFAULT NULL COMMENT '是否历史',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构税收违法';

-- gkx.dwd_org_risk_xianxiao definition

CREATE TABLE `dwd_org_risk_xianxiao` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `xhfgk_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '限制高消费官网/平台原始id。',
  `rhc_person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '限制高消费人员名称',
  `filing_date` date DEFAULT NULL COMMENT '立案时间',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '案号',
  `gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '性别',
  `company_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '企业信息',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `company_cert_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '企业证件号',
  `xhfgk_doc_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '限制高消费令文件url',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标记',
  `is_history` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否是历史限制高消费',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_risk_xianxiao_xhfgk_id` (`xhfgk_id`) USING BTREE,
  KEY `idx_dwd_org_risk_xianxiao_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_risk_xianxiao_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='限制高消费';

-- gkx.dwd_org_risk_xianxiao_bak_20260710 definition

CREATE TABLE `dwd_org_risk_xianxiao_bak_20260710` (
  `xhfgk_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '限制高消费官网id',
  `rhc_person_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '限制高消费人员名称',
  `filing_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '立案时间',
  `case_no` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '案号',
  `gender` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '性别',
  `company_info` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '企业信息',
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `company_cert_no` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '企业证件号',
  `xhfgk_doc_url` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '限制高消费令文件url',
  `use_flag` int DEFAULT NULL COMMENT '使用标记',
  `is_history` int DEFAULT NULL COMMENT '是否是历史限制高消费',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海机构限制高消费记录';

-- gkx.dwd_org_risk_zhixing definition

CREATE TABLE `dwd_org_risk_zhixing` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `exec_person_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '被执行人记录唯一标识id。',
  `exec_person_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '被执行人类型',
  `exec_person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '被执行人名称',
  `gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '性别',
  `id_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '证件号码',
  `exec_court` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '执行法院',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '案号',
  `exec_basis_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '执行依据文号',
  `exec_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '执行状态',
  `exec_target` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '执行标的',
  `web_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '执行信息公开网id',
  `filing_date` date DEFAULT NULL COMMENT '立案时间',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标记',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否不展示',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_risk_zhixing_exec_person_id` (`exec_person_id`) USING BTREE,
  KEY `idx_dwd_org_risk_zhixing_exec_basis_no` (`exec_basis_no`) USING BTREE,
  KEY `idx_dwd_org_risk_zhixing_web_id` (`web_id`) USING BTREE,
  KEY `idx_dwd_org_risk_zhixing_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_risk_zhixing_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='被执行人';

-- gkx.dwd_org_risk_zhixing_bak_20260710 definition

CREATE TABLE `dwd_org_risk_zhixing_bak_20260710` (
  `exec_person_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '唯一索引id',
  `exec_person_type` int DEFAULT NULL COMMENT '被执行人类型',
  `exec_person_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '被执行人名称',
  `gender` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '性别',
  `id_no` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '证件号码',
  `exec_court` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '执行法院',
  `case_no` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '案号',
  `exec_basis_no` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '执行依据文号',
  `exec_status` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '执行状态',
  `exec_target` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '执行标的',
  `web_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '执行信息公开网id',
  `filing_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '立案时间',
  `use_flag` int DEFAULT NULL COMMENT '使用标记',
  `is_hidden` int DEFAULT NULL COMMENT '是否不展示',
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构被执行人记录';

-- gkx.dwd_org_risk_zhongben definition

CREATE TABLE `dwd_org_risk_zhongben` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `official_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '官网id',
  `executed_person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '被执行人姓名名称',
  `gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '性别',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '案号',
  `executed_person_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '被执行人类型',
  `id_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '证件号码',
  `exec_court` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '执行法院',
  `filing_date` date DEFAULT NULL COMMENT '立案日期',
  `termination_date` date DEFAULT NULL COMMENT '终本日期',
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '地址',
  `exec_target_amount` decimal(20,2) DEFAULT NULL COMMENT '执行标的金额',
  `unfulfilled_amount` decimal(20,2) DEFAULT NULL COMMENT '未履行标的金额',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `data_use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据使用标记',
  `is_history` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否是历史数据',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否不展示',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_risk_zhongben_official_id` (`official_id`) USING BTREE,
  KEY `idx_dwd_org_risk_zhongben_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_risk_zhongben_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='终本案件';

-- gkx.dwd_org_risk_zhongben_bak_20260710 definition

CREATE TABLE `dwd_org_risk_zhongben_bak_20260710` (
  `official_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '官网id',
  `executed_person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '被执行人姓名名称',
  `gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '性别',
  `case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '案号',
  `executed_person_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '被执行人类型',
  `id_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '证件号码',
  `exec_court` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '执行法院',
  `filing_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '立案日期',
  `termination_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '终本日期',
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '地址',
  `exec_target_amount` decimal(20,2) DEFAULT NULL COMMENT '执行标的金额',
  `unfulfilled_amount` decimal(20,2) DEFAULT NULL COMMENT '未履行标的金额',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源zxgk',
  `data_use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据使用标记',
  `is_history` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否是历史数据',
  `is_hidden` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否不展示',
  `data_source2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='终本案件表';

-- gkx.dwd_org_shareholder_info definition

CREATE TABLE `dwd_org_shareholder_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `inv_org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `owners_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '股东名称',
  `owners_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '股东类型',
  `ownership_percentage` decimal(20,2) DEFAULT NULL COMMENT '所有权占比(%)',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_shareholder_info_org_id_inv_org_id` (`org_id`,`inv_org_id`) USING BTREE,
  KEY `idx_dwd_org_shareholder_info_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_shareholder_info_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_shareholder_info_inv_org_id` (`inv_org_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内机构股东信息';

-- gkx.dwd_org_shareholder_info_bak_20260710 definition

CREATE TABLE `dwd_org_shareholder_info_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `inv_org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '股东id',
  `owners_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '股东名称',
  `owners_type` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '股东类型',
  `ownership_percentage` double DEFAULT NULL COMMENT '所有权占比(%)',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构股东信息';

-- gkx.dwd_org_stock_base definition

CREATE TABLE `dwd_org_stock_base` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `stock_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '股票代码',
  `stock_noun` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '股票简称',
  `stock_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '上市板块',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `listed_date` date DEFAULT NULL COMMENT '上市日期',
  `listed_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '上市状态',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_stock_base_stock_code` (`stock_code`) USING BTREE,
  KEY `idx_dwd_org_stock_base_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_stock_base_external_id` (`external_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='上市企业基本信息';

-- gkx.dwd_org_stock_base_bak_20260710 definition

CREATE TABLE `dwd_org_stock_base_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `stock_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '股票代码',
  `stock_noun` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '股票简称',
  `stock_type` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '上市板块',
  `listed_date` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '上市日期',
  `listed_status` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '上市状态',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据上市企业基本信息';

-- gkx.dwd_org_stock_finance_info definition

CREATE TABLE `dwd_org_stock_finance_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `stock_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '股票代码',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `occur_period` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '数据期',
  `total_assets` decimal(20,2) DEFAULT NULL COMMENT '资产总额(元)',
  `fixed_assets` decimal(20,2) DEFAULT NULL COMMENT '固定资产总额(元)',
  `total_liabilities` decimal(20,2) DEFAULT NULL COMMENT '负债总额(元)',
  `operating_revenue` decimal(20,2) DEFAULT NULL COMMENT '营业收入(元)',
  `main_business_revenue` decimal(20,2) DEFAULT NULL COMMENT '主营业务收入(元)',
  `total_profit` decimal(20,2) DEFAULT NULL COMMENT '利润总额(元)',
  `pure_profit` decimal(20,2) DEFAULT NULL COMMENT '净利润(元)',
  `total_tax_paid` decimal(20,2) DEFAULT NULL COMMENT '纳税总额(元)',
  `oper_cash_flow` decimal(20,2) DEFAULT NULL COMMENT '经营活动现金流(元)',
  `owners_equity` decimal(20,2) DEFAULT NULL COMMENT '所有者权益合计(元)',
  `employees_number` bigint DEFAULT NULL COMMENT '从业人数',
  `research_development_amount` decimal(20,2) DEFAULT NULL COMMENT '研发投入金额(元)',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_stock_finance_info_org_id_occur_period` (`org_id`,`occur_period`) USING BTREE,
  KEY `idx_dwd_org_stock_finance_info_stock_code` (`stock_code`) USING BTREE,
  KEY `idx_dwd_org_stock_finance_info_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_stock_finance_info_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_stock_finance_info_occur_period` (`occur_period`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='上市企业主要财务指标';

-- gkx.dwd_org_stock_finance_info_bak_20260710 definition

CREATE TABLE `dwd_org_stock_finance_info_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `stock_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '股票代码',
  `occur_period` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据期',
  `total_assets` decimal(20,2) DEFAULT NULL COMMENT '资产总额(元)',
  `fixed_assets` decimal(20,2) DEFAULT NULL COMMENT '固定资产总额(元)',
  `total_liabilities` decimal(20,2) DEFAULT NULL COMMENT '负债总额(元)',
  `operating_revenue` decimal(20,2) DEFAULT NULL COMMENT '营业收入(元)',
  `gross_revenue` decimal(20,2) DEFAULT NULL COMMENT '营业总收入(元)',
  `main_business_revenue` decimal(20,2) DEFAULT NULL COMMENT '主营业务收入(元)',
  `total_profit` decimal(20,2) DEFAULT NULL COMMENT '利润总额(元)',
  `pure_profit` decimal(20,2) DEFAULT NULL COMMENT '净利润(元)',
  `total_tax_paid` decimal(20,2) DEFAULT NULL COMMENT '纳税总额(元)',
  `oper_cash_flow` decimal(20,2) DEFAULT NULL COMMENT '经营活动现金流(元)',
  `owners_equity` decimal(20,2) DEFAULT NULL COMMENT '所有者权益合计(元)',
  `employees_number` int DEFAULT NULL COMMENT '从业人数',
  `research_development_amount` decimal(20,2) DEFAULT NULL COMMENT '研发投入金额(元)',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据上市企业主要财务指标';

-- gkx.dwd_org_tag_info definition

CREATE TABLE `dwd_org_tag_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构身份唯一id，用于关联其它表。',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `org_tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '企业标签',
  `tag_level` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '级别',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_tag_info_org_id_org_tag` (`org_id`,`org_tag`) USING BTREE,
  KEY `idx_dwd_org_tag_info_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_tag_info_org_id` (`org_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='机构标签表';

-- gkx.dwd_org_tag_info_bak_20260710 definition

CREATE TABLE `dwd_org_tag_info_bak_20260710` (
  `org_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `org_tag` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '企业标签',
  `tag_level` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '级别',
  `data_source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '创建时间',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='前海数据机构标签表';

-- gkx.dwd_org_tb_judicial_sale definition

CREATE TABLE `dwd_org_tb_judicial_sale` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `notice_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '公告名',
  `asset_disposal_unit` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '资产处置单位',
  `notice_time` date DEFAULT NULL COMMENT '公告时间',
  `notice_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '司法拍卖公告唯一标识id。',
  `source_website` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '来源网站',
  `notice_content_path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '公告内容存储路径',
  `auction_start_date` date DEFAULT NULL COMMENT '拍卖开始日期',
  `auction_end_date` date DEFAULT NULL COMMENT '拍卖截止日期',
  `original_link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '原始链接',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标志',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_tb_judicial_sale_notice_id` (`notice_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='司法拍卖';

-- gkx.dwd_org_tb_judicial_sale_bak_20260710 definition

CREATE TABLE `dwd_org_tb_judicial_sale_bak_20260710` (
  `notice_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '公告名',
  `asset_disposal_unit` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '资产处置单位',
  `notice_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告时间',
  `notice_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告id',
  `source_website` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '来源网站',
  `notice_content_path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '公告内容存储路径',
  `auction_start_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '拍卖开始日期',
  `auction_end_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '拍卖截止日期',
  `original_link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '原始链接',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用标志',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='司法拍卖表';

-- gkx.dwd_org_tb_judicial_sale_info_company definition

CREATE TABLE `dwd_org_tb_judicial_sale_info_company` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `notice_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '司法拍卖公告唯一标识id，关联司法拍卖表。',
  `related_company` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '相关公司',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '机构名称',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标记',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_org_tb_judicial_sale_info_company_notice_id_rela_8757ed55` (`notice_id`,`related_company`) USING BTREE,
  KEY `idx_dwd_org_tb_judicial_sale_info_company_org_id` (`org_id`) USING BTREE,
  KEY `idx_dwd_org_tb_judicial_sale_info_company_external_id` (`external_id`) USING BTREE,
  KEY `idx_dwd_org_tb_judicial_sale_info_company_notice_id` (`notice_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='司法拍卖当事人';

-- gkx.dwd_org_tb_judicial_sale_info_company_bak_20260710 definition

CREATE TABLE `dwd_org_tb_judicial_sale_info_company_bak_20260710` (
  `notice_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告id',
  `related_company` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '相关公司',
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `name_cn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构名称',
  `social_credit_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `use_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用标记',
  `data_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='司法拍卖当事人表';

-- gkx.dwd_patent definition

CREATE TABLE `dwd_patent` (
  `patent_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利记录唯一标识，与 DOCDB 兼容，用于关联各专利要素分表。',
  `publication_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利公开或公告时使用的文献编号。',
  `application_kind` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利申请类型代码，用于区分发明、实用新型、PCT、外观设计等申请类别。',
  `country_code` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利公开或公告文献对应的国家、地区或组织代码。',
  `country` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利所属或发布的国家名称。',
  `publication_reference` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利公开或公告文献的种类代码。',
  `publication_reference_2` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '专利公开或公告发布的具体日期，格式为YYYY-MM-DD。',
  `publication_reference_3` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利公开或公告发布日期对应的年份，格式为YYYY。',
  `publication_reference_4` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利公开或公告发布日期对应的年月，格式为YYYY-MM。',
  `application_reference` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利申请提交时使用的申请编号。',
  `application_reference_2` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '受理专利申请的国家、地区或组织代码。',
  `application_reference_3` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '专利申请提交的具体日期，格式为YYYY-MM-DD。',
  `application_reference_4` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利申请提交日期对应的年份，格式为YYYY。',
  `application_reference_5` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利申请提交日期对应的年月，格式为YYYY-MM。',
  `pct_or_regional_filing_data` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'PCT 国际专利申请的申请编号。',
  `pct_or_regional_filing_data_2` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT 'PCT 国际申请提交的日期。',
  `pct_or_regional_publishing_data` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'PCT 国际申请对应的公布号。',
  `pct_or_regional_pub_data_2` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT 'PCT 国际申请公开发布的日期。',
  `priority_filings` int NOT NULL DEFAULT '0' COMMENT '同一专利下多条优先权信息的排列序号。',
  `priority_filings_2` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权语言',
  `priority_filings_3` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权申请的申请号。',
  `priority_filings_4` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权申请的公布号。',
  `priority_filings_5` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权对应的国家、地区或组织代码。',
  `priority_filings_6` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权申请的具体日期。',
  `priority_filings_7` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权申请日期对应的年份。',
  `priority_filings_8` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权申请的类型代码。',
  `priority_filings_9` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权申请的具体标题。',
  `applicants` bigint NOT NULL DEFAULT '0' COMMENT '原始申请人在申请人列表中的排列序号。',
  `applicants_2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利申请文件记载的原始申请人或权利人名称。',
  `assignees` bigint NOT NULL DEFAULT '0' COMMENT '当前申请人或专利权人在权利人列表中的排列序号。',
  `assignees_2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前有效的申请人、受让人或专利权人名称。',
  `inventors` bigint NOT NULL DEFAULT '0' COMMENT '发明人在发明人列表中的排列序号。',
  `inventors_2` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '专利发明人的姓名或信息列表。',
  `first_applicant_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '原始申请人列表中的第一位申请人名称。',
  `first_current_assignee_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前申请人或专利权人列表中的第一位主体名称。',
  `first_inventor_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '发明人列表中的第一位发明人名称。',
  `classification_ipcr` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利的主要 IPCR/IPC 分类号。',
  `classification_ipcr_2` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利的附加 IPCR/IPC 分类号。',
  `classification_cpc` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利的主要 CPC 分类号。',
  `classification_cpc_2` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利的附加 CPC 分类号。',
  `keywords` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '描述专利主题内容的关键词。',
  `claims_localized` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '专利权利要求书的文本内容。',
  `description_localized` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '专利说明书的正文内容。',
  `figures` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '专利附图或图示相关信息。',
  `language` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利原始文本使用的语言。',
  `granted_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利获得授权后的授权编号。',
  `spif_application_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'SPIF 标准化后的专利申请号。',
  `spif_publication_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'SPIF 标准化后的专利公布号。',
  `prior_art_year` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '相关现有技术对应的年份。',
  `prior_art_date` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '相关现有技术对应的具体日期。',
  `relevants` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '与当前专利主题或技术内容相关的专利信息。',
  `db_source` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '该条专利要素数据的来源贴源库。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的最近更新时间。',
  `citation_nums` bigint NOT NULL DEFAULT '0' COMMENT '该专利引用的专利文献数量。',
  `patent_citations` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的其他专利信息。',
  `patent_citations_2` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '当前专利引用的专利文献日期。',
  `patent_citations_3` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的专利文献所属国家、地区或组织代码。',
  `patent_citations_4` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的专利文献种类代码。',
  `cited_by_nums` bigint NOT NULL DEFAULT '0' COMMENT '当前专利被其他专利引用的数量。',
  `cited_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '被引专利公开号',
  `cited_by_2` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '引用当前专利的专利文献日期。',
  `cited_by_3` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的专利文献所属国家、地区或组织代码。',
  `cited_by_4` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的专利文献种类代码。',
  `non_patent_citations_nums` bigint NOT NULL DEFAULT '0' COMMENT '当前专利引用的非专利文献数量。',
  `non_patent_citations` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的非专利文献数量。',
  `non_patent_citations_2` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的非专利文献日期。',
  `dates_of_public_availability` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '专利授权公告或授权公开的具体日期，格式为YYYY-MM-DD。',
  `dates_of_public_availability_2` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利授权公告或授权公开日期对应的年份，格式为YYYY。',
  `dates_of_public_availability_3` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利授权公告或授权公开日期对应的年月，格式为YYYY-MM。',
  `status` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利当前所处的法律状态。',
  `anticipated_expiration` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '专利预计到期的具体日期。',
  `expiration_year` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利预计或实际到期日期对应的年份。',
  `family_citations` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '同一专利家族内部的引用信息。',
  `cited_by_family` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '同一专利家族内部的被引用信息。',
  `other_versions` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '当前专利的其他公开、公告或授权版本信息。',
  `worldwides` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '当前专利在全球范围内的同族专利信息。',
  `simple_family` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '简单同族成员的文献号。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`patent_id`) USING BTREE,
  KEY `idx_dp_publication_number` (`publication_number`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='专利信息表';

-- gkx.dwd_patent_abstract definition

CREATE TABLE `dwd_patent_abstract` (
  `patent_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联 dwd_patent.patent_id 的专利唯一标识，用于连接主表与各要素分表。',
  `abstract_localized` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '专利文献原始语种对应的摘要内容。',
  `abstract_localized_2` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '专利英文摘要文本。',
  `db_source` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '该条专利要素数据的来源贴源库。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的最近更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`patent_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='专利摘要信息表';

-- gkx.dwd_patent_family definition

CREATE TABLE `dwd_patent_family` (
  `patent_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联 dwd_patent.patent_id 的专利唯一标识，用于连接主表与各要素分表。',
  `simple_family` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '简单同族或专利家族的唯一编号。',
  `simple_family_2` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '简单同族成员所属国家、地区或组织代码。',
  `simple_family_3` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '简单同族成员公开或公告文献的种类代码。',
  `db_source` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '该条专利要素数据的来源贴源库。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的最近更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`patent_id`) USING BTREE,
  KEY `idx_dpf_simple_family` (`simple_family`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='专利家族信息表';

-- gkx.dwd_patent_legal definition

CREATE TABLE `dwd_patent_legal` (
  `patent_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联 dwd_patent.patent_id 的专利唯一标识，用于连接主表与各要素分表。',
  `legal_events` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '专利生命周期中的法律状态变更事件。',
  `patent_legal_prs_data` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'PRS 法律状态事件发生日期。',
  `patent_legal_prs_data_2` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'PRS 法律状态事件代码。',
  `patent_legal_prs_data_3` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '法律状态事件所属分类的说明。',
  `db_source` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '该条专利要素数据的来源贴源库。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的最近更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`patent_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='法律状态信息表';

-- gkx.dwd_patent_title definition

CREATE TABLE `dwd_patent_title` (
  `patent_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联 dwd_patent.patent_id 的专利唯一标识，用于连接主表与各要素分表。',
  `title_localized` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利文献原始语种对应的标题内容。',
  `title_localized_2` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利英文标题文本。',
  `db_source` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '该条专利要素数据的来源贴源库。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的最近更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`patent_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='专利标题信息表';

-- gkx.dwd_protein definition

CREATE TABLE `dwd_protein` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '蛋白质对应的内部或来源库唯一标识',
  `protein_name` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '蛋白质的标准名称或推荐名称',
  `uniprot_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '蛋白质在 UniProt 数据库中的唯一编号',
  `gene_names` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '编码该蛋白的基因符号或别名',
  `protein_length` int DEFAULT NULL COMMENT '蛋白质氨基酸序列长度',
  `sequence` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '蛋白质的一字母氨基酸序列',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_protein_protein_name` (`protein_name`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='蛋白质表';

-- gkx.dwd_quantum_chain_link definition

CREATE TABLE `dwd_quantum_chain_link` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '表主键，唯一标识每条上链结果记录',
  `entity_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '上链实体的类型',
  `industry_chain_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '所属产业链的唯一标识ID',
  `entity_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '上链实体的唯一标识ID，与对应业务表的主键关联',
  `industry_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子产业的标准产业分类编码',
  `industry_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业编码对应的产业名称',
  `link_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业链环节的标准编码',
  `link_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '环节编码对应的产业链环节名称',
  `link_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '实体完成产业链挂链的时间',
  `link_operator` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '执行挂链操作的操作人员账号/姓名',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='上链结果表';

-- gkx.dwd_quantum_frontier_talent definition

CREATE TABLE `dwd_quantum_frontier_talent` (
  `id` bigint NOT NULL COMMENT '表主键，唯一标识每条人才记录',
  `person_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子领域人才的公开姓名',
  `organization_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '人才所属的科研机构、高校或企业名称',
  `research_direction` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '人才在量子领域的核心研究方向',
  `major_achievements` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '人才公开发表的核心论文、主持的重点科研项目等成果',
  `publish_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条人才信息的首次发布时间',
  `source_update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条人才信息的最新更新时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='量子前沿人才';

-- gkx.dwd_quantum_market_scale definition

CREATE TABLE `dwd_quantum_market_scale` (
  `id` bigint NOT NULL COMMENT '表主键，唯一标识每条市场规模记录',
  `stat_year` int NOT NULL DEFAULT '0' COMMENT '市场规模数据对应的统计年份',
  `region` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '市场规模数据对应的地理区域',
  `sub_field` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子产业的细分赛道领域',
  `market_size_100m` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '对应细分领域的市场规模，单位为亿元',
  `growth_rate` decimal(5,2) NOT NULL DEFAULT '0.00' COMMENT '市场规模的同比增长率，单位为%',
  `report_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该市场数据所属报告的发布时间',
  `source_update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条市场数据的最新更新时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='量子市场规模';

-- gkx.dwd_quantum_product definition

CREATE TABLE `dwd_quantum_product` (
  `id` bigint NOT NULL COMMENT '表主键，唯一标识每条产品记录',
  `product_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子相关产品的正式名称',
  `product_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子产品的分类类型',
  `company_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品所属的研发/生产企业全称',
  `credit_code` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业的统一社会信用代码',
  `product_parameters` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品的核心技术参数、规格指标',
  `application_scenario` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品的主要落地应用场景',
  `publish_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条产品信息的首次发布时间',
  `source_update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条产品信息的最新更新时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='量子产品信息';

-- gkx.dwd_quantum_rd_progress definition

CREATE TABLE `dwd_quantum_rd_progress` (
  `id` bigint NOT NULL COMMENT '表主键，唯一标识每条研发进展记录',
  `project_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子研发项目的正式名称',
  `organization_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目的核心承担研发单位名称',
  `credit_code` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '承担单位为企业时的统一社会信用代码',
  `rd_direction` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目的核心研发技术方向',
  `rd_stage` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目当前所处的研发阶段',
  `progress_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目当前的整体研发进展情况说明',
  `key_breakthrough` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目研发过程中取得的核心技术突破、创新成果',
  `publish_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条研发进展信息的首次发布时间',
  `source_update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条研发进展信息的最新更新时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='量子研发进展';

-- gkx.dwd_quantum_tech_trend definition

CREATE TABLE `dwd_quantum_tech_trend` (
  `id` bigint NOT NULL COMMENT '表主键，唯一标识每条技术趋势记录',
  `technology_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子相关技术的标准名称',
  `technology_category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技术的分类属性',
  `technology_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '该量子技术的核心原理、技术特点、核心能力说明',
  `maturity_stage` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技术当前的成熟度阶段',
  `application_prospect` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '该技术未来的落地应用场景、市场潜力、发展前景分析',
  `main_orgs` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '该技术的核心研发机构、头部企业',
  `publish_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条技术趋势信息的首次发布时间',
  `source_update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条技术趋势信息的最新更新时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='量子技术趋势';

-- gkx.dwd_react_detail definition

CREATE TABLE `dwd_react_detail` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '化学反应记录的唯一标识',
  `step_count` int DEFAULT NULL COMMENT '反应路线包含的步骤数量',
  `reactants` json DEFAULT NULL COMMENT '参与反应的起始物、试剂或底物集合',
  `products` json DEFAULT NULL COMMENT '反应生成物或目标产物集合',
  `yield_value` json DEFAULT NULL COMMENT '目标产物的反应收率',
  `catalyst` json DEFAULT NULL COMMENT '反应中使用的催化剂或关键促进剂',
  `temperature` int DEFAULT NULL COMMENT '反应温度的数值部分',
  `temperature_unit` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '反应温度使用的计量单位',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='化学反应信息表';

-- gkx.dwd_rel_project_paper definition

CREATE TABLE `dwd_rel_project_paper` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `id` bigint NOT NULL COMMENT '关联表主键ID。',
  `project_source` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目所属来源库，用于区分国内项目与国外项目。',
  `project_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目记录ID。',
  `paper_source` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '论文所属来源库，用于区分中文论文与外文论文。',
  `paper_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '论文记录ID。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_rel_project_paper_id` (`id`) USING BTREE,
  UNIQUE KEY `uk_dwd_rel_project_paper_biz` (`project_source`,`project_id`,`paper_source`,`paper_id`) USING BTREE,
  KEY `idx_dwd_rel_project_paper_project_source` (`project_source`) USING BTREE,
  KEY `idx_dwd_rel_project_paper_project_id` (`project_id`) USING BTREE,
  KEY `idx_dwd_rel_project_paper_paper_source` (`paper_source`) USING BTREE,
  KEY `idx_dwd_rel_project_paper_paper_id` (`paper_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='项目-论文关联表';

-- gkx.dwd_rel_project_patent definition

CREATE TABLE `dwd_rel_project_patent` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `id` bigint NOT NULL COMMENT '关联表主键ID。',
  `project_source` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目所属来源库，用于区分国内项目与国外项目。',
  `project_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目记录ID。',
  `patent_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '专利记录ID。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_rel_project_patent_id` (`id`) USING BTREE,
  UNIQUE KEY `uk_dwd_rel_project_patent_biz` (`project_source`,`project_id`,`patent_id`) USING BTREE,
  KEY `idx_dwd_rel_project_patent_project_source` (`project_source`) USING BTREE,
  KEY `idx_dwd_rel_project_patent_project_id` (`project_id`) USING BTREE,
  KEY `idx_dwd_rel_project_patent_patent_id` (`patent_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='项目-专利关联表';

-- gkx.dwd_rel_project_scholar definition

CREATE TABLE `dwd_rel_project_scholar` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `id` bigint NOT NULL COMMENT '关联表主键ID。',
  `project_source` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目所属来源库，用于区分国内项目与国外项目。',
  `project_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目记录ID。',
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '算法绑定后的学者ID。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_rel_project_scholar_id` (`id`) USING BTREE,
  UNIQUE KEY `uk_dwd_rel_project_scholar_biz` (`project_source`,`project_id`,`scholar_id`) USING BTREE,
  KEY `idx_dwd_rel_project_scholar_project_source` (`project_source`) USING BTREE,
  KEY `idx_dwd_rel_project_scholar_project_id` (`project_id`) USING BTREE,
  KEY `idx_dwd_rel_project_scholar_scholar_id` (`scholar_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='项目-人才关联表';

-- gkx.dwd_rel_reaction_substance definition

CREATE TABLE `dwd_rel_reaction_substance` (
  `id` bigint NOT NULL COMMENT '反应-物质关联记录主键',
  `reaction_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联化学反应信息表的反应ID',
  `substance_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联物质信息表的物质ID',
  `substance_role` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '物质在反应中的角色',
  `source_field` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '关系来源于反应表中的哪个字段',
  `yield_value` decimal(18,6) DEFAULT NULL COMMENT '当角色为产物时记录对应产率数值',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`,`reaction_id`) USING BTREE,
  KEY `idx_dwd_rel_reaction_substance_reaction_id` (`reaction_id`) USING BTREE,
  KEY `idx_dwd_rel_reaction_substance_substance_id` (`substance_id`) USING BTREE,
  KEY `idx_dwd_rel_reaction_substance_substance_role` (`substance_role`) USING BTREE,
  KEY `idx_dwd_rel_reaction_substance_source_field` (`source_field`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='反应-物质关联表';

-- gkx.dwd_rel_report_paper definition

CREATE TABLE `dwd_rel_report_paper` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `id` bigint NOT NULL COMMENT '关联表主键ID。',
  `report_source` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '报告所属来源库，用于区分中文报告与外文报告。',
  `report_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '报告记录ID。',
  `paper_source` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '论文所属来源库，用于区分中文论文与外文论文。',
  `paper_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '论文记录ID。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_rel_report_paper_id` (`id`) USING BTREE,
  UNIQUE KEY `uk_dwd_rel_report_paper_biz` (`report_source`,`report_id`,`paper_source`,`paper_id`) USING BTREE,
  KEY `idx_dwd_rel_report_paper_report_source` (`report_source`) USING BTREE,
  KEY `idx_dwd_rel_report_paper_report_id` (`report_id`) USING BTREE,
  KEY `idx_dwd_rel_report_paper_paper_source` (`paper_source`) USING BTREE,
  KEY `idx_dwd_rel_report_paper_paper_id` (`paper_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='报告-论文关联表';

-- gkx.dwd_rel_report_project definition

CREATE TABLE `dwd_rel_report_project` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `id` bigint NOT NULL COMMENT '关联表主键ID。',
  `report_source` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '报告所属来源库，用于区分中文报告与外文报告。',
  `report_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '报告记录ID。',
  `project_source` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目所属来源库，用于区分国内项目与国外项目。',
  `project_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目记录ID。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_rel_report_project_id` (`id`) USING BTREE,
  UNIQUE KEY `uk_dwd_rel_report_project_biz` (`report_source`,`report_id`,`project_source`,`project_id`) USING BTREE,
  KEY `idx_dwd_rel_report_project_report_source` (`report_source`) USING BTREE,
  KEY `idx_dwd_rel_report_project_report_id` (`report_id`) USING BTREE,
  KEY `idx_dwd_rel_report_project_project_source` (`project_source`) USING BTREE,
  KEY `idx_dwd_rel_report_project_project_id` (`project_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='报告-项目关联表';

-- gkx.dwd_rel_report_scholar definition

CREATE TABLE `dwd_rel_report_scholar` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `id` bigint NOT NULL COMMENT '关联表主键ID。',
  `report_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '报告记录ID。',
  `report_source` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '报告所属来源库，用于区分中文报告与外文报告。',
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '算法绑定后的学者ID。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_rel_report_scholar_id` (`id`) USING BTREE,
  UNIQUE KEY `uk_dwd_rel_report_scholar_biz` (`report_source`,`report_id`,`scholar_id`) USING BTREE,
  KEY `idx_dwd_rel_report_scholar_report_id` (`report_id`) USING BTREE,
  KEY `idx_dwd_rel_report_scholar_report_source` (`report_source`) USING BTREE,
  KEY `idx_dwd_rel_report_scholar_scholar_id` (`scholar_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='报告-人才关联表';

-- gkx.dwd_rel_substance_paper definition

CREATE TABLE `dwd_rel_substance_paper` (
  `id` bigint NOT NULL COMMENT '论文信息关联表ID',
  `substance_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分子或物质记录的唯一标识',
  `paper_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '论文记录ID',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`,`substance_id`) USING BTREE,
  KEY `idx_dwd_rel_substance_paper_substance_id` (`substance_id`) USING BTREE,
  KEY `idx_dwd_rel_substance_paper_paper_id` (`paper_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='物质-论文关联表';

-- gkx.dwd_rel_substance_patent definition

CREATE TABLE `dwd_rel_substance_patent` (
  `id` bigint NOT NULL COMMENT '专利信息关联表ID',
  `substance_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分子或物质记录的唯一标识',
  `patent_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '与 DOCDB 兼容的专利记录唯一标识',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`,`substance_id`) USING BTREE,
  KEY `idx_dwd_substance_patent_substance_id` (`substance_id`) USING BTREE,
  KEY `idx_dwd_substance_patent_patent_id` (`patent_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='物质-专利关联表';

-- gkx.dwd_safety definition

CREATE TABLE `dwd_safety` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品安全记录的内部或来源库唯一标识',
  `receivedate` date DEFAULT NULL COMMENT '药物不良事件报告在 FAERS 等安全数据库中的接收日期',
  `drug_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药物安全、交易或试验记录中涉及的药品名称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_safety_drug_name` (`drug_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='药物安全表';

-- gkx.dwd_scholar definition

CREATE TABLE `dwd_scholar` (
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者记录的业务唯一标识。',
  `name_en` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者的英文姓名。',
  `name_zh` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者的中文姓名。',
  `avatar` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者头像图片的访问链接。',
  `scholar_org_name_en` varchar(4096) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者所属机构的英文名称。',
  `scholar_org_name_zh` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者所属机构的中文名称。',
  `bio` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者的个人或学术简介信息。',
  `bio_zh` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者的中文个人或学术简介信息。',
  `work_experience_en` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者英文工作经历信息。',
  `work_experience_zh` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者中文工作经历信息。',
  `education_background_en` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者的英文教育经历信息。',
  `education_background_zh` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者的中文教育经历信息。',
  `paper_nums` int NOT NULL DEFAULT '0' COMMENT '学者已发表论文的数量。',
  `citation_nums` int NOT NULL DEFAULT '0' COMMENT '学者论文被引用的总次数。',
  `h_index` int NOT NULL DEFAULT '0' COMMENT '衡量学者学术影响力的 H 指数。',
  `status` int NOT NULL DEFAULT '0' COMMENT '记录状态，0 表示无效，1 表示有效。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录最后更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`scholar_id`) USING BTREE,
  KEY `idx_dwd_scholar_name_en` (`name_en`) USING BTREE,
  KEY `idx_dwd_scholar_name_zh` (`name_zh`) USING BTREE,
  KEY `idx_ds_scholar_org_name_en` (`scholar_org_name_en`(191)) USING BTREE,
  KEY `idx_ds_scholar_org_name_zh` (`scholar_org_name_zh`(191)) USING BTREE,
  KEY `idx_dwd_scholar_paper_nums` (`paper_nums`) USING BTREE,
  KEY `idx_dwd_scholar_citation_nums` (`citation_nums`) USING BTREE,
  KEY `idx_dwd_scholar_create_time` (`create_time`) USING BTREE,
  KEY `idx_dwd_scholar_update_time` (`update_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='学者';

-- gkx.dwd_scholar_bak_20260710 definition

CREATE TABLE `dwd_scholar_bak_20260710` (
  `id` bigint NOT NULL COMMENT '主键',
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者id',
  `name_en` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '英文姓名',
  `name_zh` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '中文姓名',
  `avatar` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '头像',
  `scholar_org_name_en` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '英文机构',
  `scholar_org_name_zh` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '' COMMENT '中文机构',
  `scholar_org_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '所属机构id，学者所属机构id',
  `bio` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '个人简介/学术简介，学者的个人或学术简介信息',
  `bio_zh` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '个人简介/学术简介（中文），学者的中文个人或学术简介信息',
  `work_experience_en` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '工作经历英文（包含机构和职务）',
  `work_experience_zh` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '工作经历中文（包含机构和职务）',
  `education_background_en` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '教育背景（英文），学者的英文教育经历信息',
  `education_background_zh` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '教育背景（中文），学者的中文教育经历信息',
  `paper_nums` int NOT NULL DEFAULT '0' COMMENT '论文数量',
  `citation_nums` int NOT NULL DEFAULT '0' COMMENT '被引数量',
  `h_index` int NOT NULL DEFAULT '0' COMMENT 'H指数',
  `status` int NOT NULL DEFAULT '1' COMMENT '状态：0:无效,1:有效',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-学者表';

-- gkx.dwd_scholar_coauthor definition

CREATE TABLE `dwd_scholar_coauthor` (
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前学者记录的业务唯一标识。',
  `co_scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '合作学者记录的业务唯一标识。',
  `co_scholar_name_en` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '合作学者的英文姓名。',
  `co_scholar_name_zh` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '合作学者的中文姓名。',
  `co_scholar_avatar` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '合作学者头像图片的访问链接。',
  `co_scholar_org_name_en` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '合作学者所属机构的英文名称。',
  `co_scholar_org_name_zh` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '合作学者所属机构的中文名称。',
  `co_paper_count` int NOT NULL DEFAULT '0' COMMENT '与该学者合作发表的论文数量。',
  `status` int NOT NULL DEFAULT '0' COMMENT '记录状态，0 表示无效，1 表示有效。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录最后更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`scholar_id`,`co_scholar_id`) USING BTREE,
  KEY `idx_dsc_co_scholar_name_en` (`co_scholar_name_en`(191)) USING BTREE,
  KEY `idx_dsc_co_scholar_name_zh` (`co_scholar_name_zh`) USING BTREE,
  KEY `idx_dwd_scholar_coauthor_status` (`status`) USING BTREE,
  KEY `idx_dsc_update_time` (`update_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='学者合作者关系';

-- gkx.dwd_scholar_coauthor_bak_20260710 definition

CREATE TABLE `dwd_scholar_coauthor_bak_20260710` (
  `id` bigint NOT NULL COMMENT '自增主键ID',
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者ID，当前学者记录的业务唯一标识',
  `co_scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '合作学者ID，合作学者记录的业务唯一标识',
  `co_scholar_name_en` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '合作学者英文名',
  `co_scholar_name_zh` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '合作学者中文名',
  `co_scholar_avatar` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '合作学者头像URL',
  `co_scholar_org_name_en` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '合作学者所属机构英文名',
  `co_scholar_org_name_zh` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '合作学者所属机构中文名',
  `co_scholar_org_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '合作学者所属机构ID',
  `co_paper_count` int NOT NULL DEFAULT '0' COMMENT '合作论文数量',
  `status` int NOT NULL DEFAULT '1' COMMENT '状态：0:无效,1:有效',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-学者合作者关系表';

-- gkx.dwd_scholar_paper_relation definition

CREATE TABLE `dwd_scholar_paper_relation` (
  `paper_id` int NOT NULL DEFAULT '0' COMMENT '论文记录的唯一标识。',
  `year` int NOT NULL DEFAULT '0' COMMENT '论文发表年份。',
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者记录的业务唯一标识。',
  `citations` int NOT NULL DEFAULT '0' COMMENT '论文被引用次数。',
  `publish_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '论文发布时间。',
  `status` int NOT NULL DEFAULT '0' COMMENT '记录状态，0 表示无效，1 表示有效。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录最后更新时间。',
  `publication_id` int NOT NULL DEFAULT '0' COMMENT '期刊或会议记录的唯一标识。',
  `related_paper_id` int NOT NULL DEFAULT '0' COMMENT '关联论文库的唯一标识。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`scholar_id`,`paper_id`) USING BTREE,
  KEY `idx_dspr_citations` (`citations`) USING BTREE,
  KEY `idx_dspr_publish_time` (`publish_time`) USING BTREE,
  KEY `idx_dspr_create_time` (`create_time`) USING BTREE,
  KEY `idx_dspr_update_time` (`update_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='学者论文关系';

-- gkx.dwd_scholar_paper_relation_bak_20260710 definition

CREATE TABLE `dwd_scholar_paper_relation_bak_20260710` (
  `id` bigint NOT NULL COMMENT '主键',
  `paper_id` bigint NOT NULL DEFAULT '0' COMMENT '论文id',
  `related_paper_id` bigint DEFAULT NULL COMMENT '关联论文库的唯一标识',
  `year` bigint NOT NULL DEFAULT '0' COMMENT '论文发表年份',
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者id',
  `citations` int NOT NULL DEFAULT '0' COMMENT '被引用次数',
  `publish_time` datetime DEFAULT NULL COMMENT '发布时间',
  `status` int NOT NULL DEFAULT '1' COMMENT '状态：0:无效,1:有效',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '期刊id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-学者论文关系表';

-- gkx.dwd_scholar_papers definition

CREATE TABLE `dwd_scholar_papers` (
  `paper_id` bigint NOT NULL DEFAULT '0' COMMENT '论文记录的唯一标识，依据人才质量核验字段补充。',
  `zh_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的中文标题名称。',
  `en_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的英文标题名称。',
  `authors` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '论文作者的姓名或信息列表。',
  `paper_url` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文原始来源页面的访问链接。',
  `cover_date_start` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '论文正式发表或出版的时间。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录最后更新时间。',
  `status` int NOT NULL DEFAULT '0' COMMENT '记录状态，0 表示无效，1 表示有效。',
  `zh_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '论文内容的中文摘要信息。',
  `en_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '论文内容的英文摘要信息。',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的 DOI 唯一识别号。',
  `publication_en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文发表所在期刊或会议的英文名称。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`paper_id`) USING BTREE,
  KEY `idx_dwd_scholar_papers_en_name` (`en_name`(191)) USING BTREE,
  KEY `idx_dsp_cover_date_start` (`cover_date_start`) USING BTREE,
  KEY `idx_dsp_create_time` (`create_time`) USING BTREE,
  KEY `idx_dsp_update_time` (`update_time`) USING BTREE,
  KEY `idx_dwd_scholar_papers_doi` (`doi`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='论文信息';

-- gkx.dwd_scholar_papers_bak_20260710 definition

CREATE TABLE `dwd_scholar_papers_bak_20260710` (
  `id` bigint NOT NULL,
  `zh_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '中文题目',
  `en_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '英文题目',
  `authors` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '作者列表',
  `paper_url` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文原始链接',
  `cover_date_start` datetime DEFAULT NULL COMMENT '发表时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '记录最后更新时间',
  `status` tinyint DEFAULT '1' COMMENT '状态：0:无效,1:有效',
  `zh_abstract` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '中文摘要',
  `en_abstract` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '英文摘要',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `publication_en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '期刊/会议英文名',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-论文信息表';

-- gkx.dwd_scholar_research_direction definition

CREATE TABLE `dwd_scholar_research_direction` (
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联学者记录的业务唯一标识。',
  `fields` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者研究方向，来源于表1字段。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录最后更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`scholar_id`) USING BTREE,
  KEY `idx_dsrd_create_time` (`create_time`) USING BTREE,
  KEY `idx_dsrd_update_time` (`update_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='学者研究方向';

-- gkx.dwd_scholar_research_direction_bak_20260710 definition

CREATE TABLE `dwd_scholar_research_direction_bak_20260710` (
  `id` bigint NOT NULL COMMENT '逻辑ID',
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者ID',
  `fields` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '研究方向',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_scholar_id` (`scholar_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-学者研究方向表';

-- gkx.dwd_scholar_talent_flag definition

CREATE TABLE `dwd_scholar_talent_flag` (
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联学者记录的业务唯一标识。',
  `academician` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标识学者是否为院士，来源于表1字段。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录最后更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`scholar_id`) USING BTREE,
  KEY `idx_dstf_academician` (`academician`) USING BTREE,
  KEY `idx_dstf_create_time` (`create_time`) USING BTREE,
  KEY `idx_dstf_update_time` (`update_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='学者人才标识';

-- gkx.dwd_scholar_talent_flag_bak_20260710 definition

CREATE TABLE `dwd_scholar_talent_flag_bak_20260710` (
  `id` bigint NOT NULL COMMENT '逻辑ID',
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者ID',
  `academician` int NOT NULL DEFAULT '0' COMMENT '是否为院士：0:否,1:是',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_scholar_id` (`scholar_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-学者人才标签表';

-- gkx.dwd_series_metadata definition

CREATE TABLE `dwd_series_metadata` (
  `metadata_id` bigint NOT NULL COMMENT '数列的唯一标识符',
  `metadata_name` varchar(1600) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列名称',
  `metadata_indicators` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '指标',
  `metadata_unit_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数列单位ID',
  `metadata_unit_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数列单位名称',
  `metadata_country_id` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列国家ID',
  `metadata_country_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列国家名称',
  `metadata_frequency_id` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列频率ID',
  `metadata_frequency_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列频率名称',
  `metadata_status_id` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列状态ID',
  `metadata_status_name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列状态名称',
  `metadata_source_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据来源ID',
  `metadata_source_name` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据来源名称',
  `metadata_startdate` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '第一个时间点的日期',
  `metadata_enddate` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '最后时间点的日期',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`metadata_id`) USING BTREE,
  KEY `idx_dwd_series_metadata_metadata_name` (`metadata_name`(191)) USING BTREE,
  KEY `idx_dwd_series_metadata_metadata_unit_name` (`metadata_unit_name`) USING BTREE,
  KEY `idx_dwd_series_metadata_metadata_country_name` (`metadata_country_name`) USING BTREE,
  KEY `idx_dwd_series_metadata_metadata_frequency_name` (`metadata_frequency_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='序列元数据';

-- gkx.dwd_series_timepoints definition

CREATE TABLE `dwd_series_timepoints` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '业务侧生成主键',
  `timepoints_value` decimal(18,6) NOT NULL DEFAULT '0.000000' COMMENT '数据时间点值',
  `timepoints_date` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据时间点日期',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_series_timepoints_timepoints_value` (`timepoints_value`) USING BTREE,
  KEY `idx_dwd_series_timepoints_timepoints_date` (`timepoints_date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='序列时间点';

-- gkx.dwd_similar_substance definition

CREATE TABLE `dwd_similar_substance` (
  `similar_substance_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '相似物质记录的唯一标识',
  `en_name` varchar(4000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '物质的英文名称或标准名称',
  `cas_registry_id` json DEFAULT NULL COMMENT '化学物质的 CAS Registry Number',
  `formula` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '分子、化合物或晶体的化学组成式',
  `similar_paper_count` int DEFAULT NULL COMMENT '与相似分子相关的论文数量',
  `similar_publication_count` int DEFAULT NULL COMMENT '与相似分子相关的专利或公开文献数量',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`similar_substance_id`) USING BTREE,
  KEY `idx_dwd_similar_substance_en_name` (`en_name`(191)) USING BTREE,
  KEY `idx_dwd_similar_substance_formula` (`formula`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='结构相近的其他分子';

-- gkx.dwd_small_molecule_screening definition

CREATE TABLE `dwd_small_molecule_screening` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '小分子活性与筛选的内部或来源库唯一标识',
  `molecular_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '化合物、材料或分子的标准英文名称',
  `reference` json DEFAULT NULL COMMENT '支持该条记录的论文、数据库页面或 DOI 等来源信息',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_small_molecule_screening_molecular_name` (`molecular_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='小分子活性与筛选';

-- gkx.dwd_substance definition

CREATE TABLE `dwd_substance` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分子或物质记录的唯一标识',
  `en_name` varchar(4000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '物质的英文名称或标准名称',
  `cas_registry_id` json DEFAULT NULL COMMENT '化学物质的 CAS Registry Number',
  `formula` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '分子、化合物或晶体的化学组成式',
  `synonym` json DEFAULT NULL COMMENT '化合物或物质的别名、商品名或历史名称',
  `chemical_type` json DEFAULT NULL COMMENT '物质的化学类别或结构分类',
  `weight` decimal(18,6) DEFAULT NULL COMMENT '化合物的相对分子质量',
  `iupac_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '化合物的系统性 IUPAC 名称',
  `std_smiles` varchar(4000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '包含立体化学信息的 SMILES 表示',
  `in_chi_key` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'InChI 的固定长度哈希标识，用于化合物快速匹配和去重',
  `in_chi` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '化合物的 IUPAC 国际化学标识符',
  `heavy_atom_count` int DEFAULT NULL COMMENT '分子中非氢原子的数量',
  `total_formal_charge` int DEFAULT NULL COMMENT '分子的总形式电荷',
  `complexity` int DEFAULT NULL COMMENT '基于结构特征计算的分子复杂度指标',
  `isotope_atom_count` int DEFAULT NULL COMMENT '分子中同位素标记原子的数量',
  `atom_chiral_count` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '分子中已明确和未明确构型的原子手性中心数量',
  `bond_chiral_count` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '分子中已明确和未明确构型的立体键数量',
  `covalent_unit_count` int DEFAULT NULL COMMENT '分子结构中通过共价键连接形成的独立结构单元数量',
  `xlogp` decimal(18,6) DEFAULT NULL COMMENT '化合物的 LogP，用于表征亲脂性',
  `hydrogen_bond_donor_count` int DEFAULT NULL COMMENT '分子中可作为氢键供体的原子或基团数量',
  `hydrogen_bond_acceptor_count` int DEFAULT NULL COMMENT '分子中可作为氢键受体的原子或基团数量',
  `rotatable_bond_count` int DEFAULT NULL COMMENT '分子中可自由旋转的单键数量',
  `tpsa` decimal(18,6) DEFAULT NULL COMMENT '分子的拓扑极性表面积，用于评估吸收和渗透性',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_substance_en_name` (`en_name`(191)) USING BTREE,
  KEY `idx_dwd_substance_formula` (`formula`(191)) USING BTREE,
  KEY `idx_dwd_substance_iupac_name` (`iupac_name`(191)) USING BTREE,
  KEY `idx_dwd_substance_std_smiles` (`std_smiles`(191)) USING BTREE,
  KEY `idx_dwd_substance_in_chi_key` (`in_chi_key`) USING BTREE,
  KEY `idx_dwd_substance_in_chi` (`in_chi`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='物质信息表';

-- gkx.dwd_zck_intl_policy definition

CREATE TABLE `dwd_zck_intl_policy` (
  `policy_record_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '唯一ID',
  `original_title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '标题原文',
  `translated_title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '标题译文',
  `original_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '正文原文',
  `translated_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '正文译文',
  `original_summary` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '摘要原文',
  `media_region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '所属区域',
  `publish_date_raw` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '发布时间',
  `media_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '媒体名称',
  `source_url` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'url链接',
  `language_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '语种',
  `media_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '媒体类型',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`policy_record_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='国际政策信息表';

-- gkx.dwd_zck_policy definition

CREATE TABLE `dwd_zck_policy` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '唯一ID',
  `datatype` tinyint NOT NULL COMMENT '数据类型（政策/解读）',
  `docstatus` tinyint NOT NULL COMMENT '政策的发布状态（20-已发布，30-已撤销）',
  `title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '标题（纯文本）',
  `titlena` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '标题（富文本）',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '内容（纯文本）',
  `contentNa` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '内容（富文本）',
  `url` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '原文链接地址',
  `issueno` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '发文字号',
  `indexno` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '索引号',
  `sitename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '站点名称',
  `crtime` date NOT NULL COMMENT '成文日期',
  `pubtime` date NOT NULL COMMENT '发文日期（发布日期）',
  `pubyear` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '发布年份',
  `area` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '发布单位的所属地区',
  `policylevel` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '政策层级（国家级/省级/市级/区县级）',
  `region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '政策地区',
  `attachments` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '政策附件文件的链接',
  `keywords` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '政策内容关键词',
  `abs` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '正文摘要',
  `maelements` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '对政策背景、指导思想等政策内容进行标准化拆解与提炼',
  `ma_keypoints` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '从政策全文中摘录、提炼章节标题、工作原则、发展现状、重点任务、细分产业、问题研判等内容。',
  `allfactors` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '含扶持分类、扶持门槛扶持力度。目的是提取政策中各类扶持、补助、优惠、激励类内容需满足的条件和对应的扶持信息',
  `complextaginfojson` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '政策所有的标签（json格式）',
  `pedigree` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '政策的上位政策和下位政策',
  `ma_contenttypenew` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '用于区分政策文件的性质、发文类别、公文体裁，是政务数据基础分类字段',
  `pubdeptname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '发布单位名称',
  `topic_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '政策主题分类',
  `expiration_date` date NOT NULL COMMENT '失效日期',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_zck_policy_id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内政策信息表';

-- gkx.dwd_zh_author definition

CREATE TABLE `dwd_zh_author` (
  `paper_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `author_sequence` int NOT NULL DEFAULT '0' COMMENT '作者在文献中的顺序。',
  `author_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者的唯一主键 id',
  `en_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者的英文名称',
  `zh_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者中文名',
  `email` json NOT NULL COMMENT '文献作者email',
  `is_correspond` tinyint NOT NULL DEFAULT '0' COMMENT '是否为通讯作者：否=0，是=1，未知为空。',
  `institution` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '作者所属机构或单位的名称。',
  `affiliation` json NOT NULL COMMENT '文献作者地址',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`paper_id`,`author_sequence`) USING BTREE,
  KEY `idx_dwd_zh_author_author_id` (`author_id`) USING BTREE,
  KEY `idx_dza_author_en_name` (`en_name`) USING BTREE,
  KEY `idx_dza_author_zh_name` (`zh_name`) USING BTREE,
  KEY `idx_dza_institution` (`institution`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文文献作者详情信息';

-- gkx.dwd_zh_author_bak_20260710 definition

CREATE TABLE `dwd_zh_author_bak_20260710` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献作者的唯一主键 id',
  `paper_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献记录的唯一主键标识。',
  `en_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献作者的英文名称',
  `zh_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献作者中文名',
  `affiliation` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '文献作者地址',
  `email` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '文献作者email',
  `correspond` tinyint DEFAULT NULL COMMENT '是否为通讯作者',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-中文文献作者详情信息';

-- gkx.dwd_zh_journal definition

CREATE TABLE `dwd_zh_journal` (
  `paper_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '期刊记录的唯一标识。',
  `publication_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '出版物类别，例如期刊，会议等',
  `country` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊所属或出版所在国家/地区代码或名称。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的中文名称。',
  `name_abbr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊名称的简称或缩写。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的英文名称。',
  `iscn` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国内统一刊号。',
  `issn` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国际标准连续出版物编号。',
  `eissn` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊电子版的国际标准连续出版物编号。',
  `founding_time` int NOT NULL DEFAULT '0' COMMENT '期刊首次创办或发行的时间。',
  `jn_official` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '期刊官方网站地址。',
  `zh_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '期刊的中文简介或说明。',
  `format` tinytext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '期刊的版面开本规格。',
  `postal_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊邮政发行使用的代号。',
  `chief_editor` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊当前或记录中的主编信息。',
  `organizer` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '负责主办该期刊的单位名称。',
  `publisher_place` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊出版发行的地点。',
  `award` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '期刊获得的奖项或荣誉信息。',
  `cite_nums` int NOT NULL DEFAULT '0' COMMENT '期刊或文献的累计被引用次数。',
  `annual_publication` int NOT NULL DEFAULT '0' COMMENT '期刊每年发表文章的数量。',
  `is_review` tinyint NOT NULL DEFAULT '0' COMMENT '是否为综述性期刊：否=0，是=1，未知=2。',
  `impact_factor` double NOT NULL DEFAULT '0' COMMENT '期刊的影响因子指标。',
  `sub_quartile` tinyint NOT NULL DEFAULT '0' COMMENT '期刊在相关评价体系中的分区信息。Subject Quartile in Category分区',
  `classify_list` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献或期刊对应的学科分类编号。',
  `is_warning` tinyint NOT NULL DEFAULT '0' COMMENT '是否预警：否=0，是=1，未知为空。',
  `is_sci` tinyint NOT NULL DEFAULT '0' COMMENT '标识期刊是否被 SCI 收录。',
  `publication_cycle` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的出版频率或发行周期。',
  `paper_nums` int NOT NULL DEFAULT '0' COMMENT '期刊已发表论文的数量。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`publication_id`) USING BTREE,
  KEY `idx_dwd_zh_journal_paper_id` (`paper_id`) USING BTREE,
  KEY `idx_dwd_zh_journal_zh_name` (`zh_name`(191)) USING BTREE,
  KEY `idx_dwd_zh_journal_name_abbr` (`name_abbr`(191)) USING BTREE,
  KEY `idx_dwd_zh_journal_en_name` (`en_name`(191)) USING BTREE,
  KEY `idx_dwd_zh_journal_iscn` (`iscn`) USING BTREE,
  KEY `idx_dwd_zh_journal_issn` (`issn`) USING BTREE,
  KEY `idx_dwd_zh_journal_eissn` (`eissn`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文期刊详情信息';

-- gkx.dwd_zh_journal_bak_20260710 definition

CREATE TABLE `dwd_zh_journal_bak_20260710` (
  `id` bigint NOT NULL COMMENT '期刊记录的唯一标识。',
  `iscn` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊的国内统一刊号。',
  `issn` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊的国际标准连续出版物编号。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊的中文名称。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊的英文名称。',
  `publication_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '出版物类别，例如期刊，会议等',
  `name_abbr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊名称的简称或缩写。',
  `country` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊所属或出版所在的国家。',
  `zh_description` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '期刊的中文简介或说明。',
  `format` varchar(63) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊的版面开本规格。',
  `founding_time` int DEFAULT NULL COMMENT '期刊首次创办或发行的时间。',
  `language_classify` tinyint DEFAULT NULL COMMENT '期刊出版使用的语言类型。',
  `eissn` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊电子版的国际标准连续出版物编号。',
  `jn_official` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '期刊官方网站地址。',
  `postal_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊邮政发行使用的代号。',
  `chief_editor` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊当前或记录中的主编信息。',
  `organizer` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '负责主办该期刊的单位名称。',
  `publisher_place` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊出版发行的地点。',
  `publication_cycle` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊的出版频率或发行周期。',
  `award` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '期刊获得的奖项或荣誉信息。',
  `cite_nums` int DEFAULT NULL COMMENT '期刊或文献的累计被引用次数。',
  `paper_nums` int DEFAULT NULL COMMENT '期刊已发表论文的数量。',
  `review` tinyint DEFAULT NULL COMMENT '标识该期刊是否为综述类期刊。',
  `annual_publication` int DEFAULT NULL COMMENT '期刊每年发表文章的数量。',
  `impact_factor` decimal(20,10) DEFAULT NULL COMMENT '期刊的影响因子指标。',
  `open_access` tinyint DEFAULT NULL COMMENT '标识期刊或论文是否为开放获取。',
  `scope` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊所属的大类学科领域。',
  `scope_zone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '期刊所属的细分学科领域。',
  `warning` tinyint DEFAULT NULL COMMENT '标识期刊是否处于预警状态。',
  `is_sci` tinyint DEFAULT NULL COMMENT '标识期刊是否被 SCI 收录。',
  `sub_quartile` tinyint DEFAULT NULL COMMENT '期刊在相关评价体系中的分区信息。',
  `classify_list` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '文献或期刊对应的学科分类编号。',
  `updated_time` datetime NOT NULL COMMENT '该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-中文期刊详情信息';

-- gkx.dwd_zh_paper definition

CREATE TABLE `dwd_zh_paper` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `doi` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的英文标题名称。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的中文标题名称。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '关联出版物的id，用于获取期刊详情信息',
  `paper_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献所属出版物的章节名称，栏目等。',
  `publication_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '出版物类别，例如期刊，会议等',
  `publication_zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的中文名称。',
  `issn` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国际标准连续出版物编号。',
  `volume` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献发表所在期刊的卷号。',
  `issue` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献发表所在期刊的期号。',
  `first_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文在期刊中的起始页码。',
  `last_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文在期刊中的结束页码。',
  `cover_year_start` date NOT NULL DEFAULT '1970-01-01' COMMENT '文献正式发表年份，按年份日期存储。',
  `cover_date_start` date NOT NULL DEFAULT '1970-01-01' COMMENT '文献正式发表的日期。',
  `language_classify` tinyint NOT NULL DEFAULT '0' COMMENT '文献语言类型：英文=0，中文=1，中英文=2。',
  `abstract_available` tinyint NOT NULL DEFAULT '0' COMMENT '摘要是否可用：否=0，是=1。',
  `open_access` tinyint NOT NULL DEFAULT '0' COMMENT '标识期刊或论文是否为开放获取。',
  `paper_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献数据的原始来源地址。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_zh_paper_doi` (`doi`(191)) USING BTREE,
  KEY `idx_dwd_zh_paper_en_name` (`en_name`(191)) USING BTREE,
  KEY `idx_dwd_zh_paper_zh_name` (`zh_name`(191)) USING BTREE,
  KEY `idx_dwd_zh_paper_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_dzp_publication_zh_name` (`publication_zh_name`(191)) USING BTREE,
  KEY `idx_dzp_pub_year_type` (`publication_id`,`cover_year_start`,`paper_type`) USING BTREE,
  KEY `idx_dzp_year_open` (`cover_year_start`,`open_access`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文详情信息';

-- gkx.dwd_zh_paper_abstract definition

CREATE TABLE `dwd_zh_paper_abstract` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `abstract_sequence` int NOT NULL DEFAULT '0' COMMENT '同一文献多个摘要的顺序号',
  `language_code` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '摘要语言代码。',
  `original_abstract` tinyint NOT NULL DEFAULT '0' COMMENT '是否为原始摘要：否=0，是=1，未知=2。',
  `en_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献内容的英文摘要信息。',
  `zh_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献内容的中文摘要信息。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`,`abstract_sequence`) USING BTREE,
  KEY `idx_dzpa_abstract_sequence` (`abstract_sequence`) USING BTREE,
  KEY `idx_dzpa_language_code` (`language_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文摘要信息';

-- gkx.dwd_zh_paper_bak_20260710 definition

CREATE TABLE `dwd_zh_paper_bak_20260710` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献记录的唯一主键标识。',
  `paper_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献所属出版物的章节名称，栏目等。',
  `publication_id` bigint NOT NULL COMMENT '关联出版物的id，用于获取期刊详情信息',
  `paper_url` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '文献数据的原始来源地址。',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '论文的唯一标识编码。',
  `cover_date_start` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献正式发表的日期。',
  `ch_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献的中文标题名称。',
  `ch_abstract` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '文献内容的中文摘要信息。',
  `keywords` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '描述论文主题内容的关键词。',
  `volume` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献发表所在期刊的卷号。',
  `issue` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文献发表所在期刊的期号。',
  `first_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '论文在期刊中的起始页码。',
  `last_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '论文在期刊中的结束页码。',
  `reference_nums` int DEFAULT NULL COMMENT '论文参考文献的总数量。',
  `reference_content` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '论文所引用参考文献的具体内容。',
  `citation_nums` int DEFAULT NULL COMMENT '论文被其他文献引用的数量。',
  `citation_content` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '引用该论文的相关文献信息。',
  `relevant` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '与当前文献内容或主题相关的文献信息。',
  `authors` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '论文作者的结构化id列表。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-中文论文详情信息';

-- gkx.dwd_zh_paper_citation definition

CREATE TABLE `dwd_zh_paper_citation` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '关联出版物的id，用于获取期刊详情信息',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '引用文献的中文标题名称。',
  `publication_zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献出版物的中文名称。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dzpc_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_dwd_zh_paper_citation_doi` (`doi`(191)) USING BTREE,
  KEY `idx_dzpc_publication_zh_name` (`publication_zh_name`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文引用文献信息';

-- gkx.dwd_zh_paper_classification definition

CREATE TABLE `dwd_zh_paper_classification` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `scope` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊所属的大类学科领域。',
  `scope_zone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊所属的细分学科领域。',
  `keywords` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '描述论文主题内容的关键词。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文分类信息';

-- gkx.dwd_zh_paper_reference definition

CREATE TABLE `dwd_zh_paper_reference` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '关联出版物的id，用于获取期刊详情信息',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献的中文标题名称。',
  `publication_zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献出版物的中文名称。',
  `cover_year_start` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献正式发表的年份。',
  `volume` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献发表所在期刊的卷号。',
  `issue` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献发表所在期刊的期号。',
  `first_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献在期刊中的起始页码。',
  `last_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献在期刊中的结束页码。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dzpr_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_dwd_zh_paper_reference_doi` (`doi`(191)) USING BTREE,
  KEY `idx_dzpr_publication_zh_name` (`publication_zh_name`(191)) USING BTREE,
  KEY `idx_dzpr_cover_year_start` (`cover_year_start`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文参考文献信息';

-- gkx.dwd_zh_paper_related definition

CREATE TABLE `dwd_zh_paper_related` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `relevant` json NOT NULL COMMENT '与当前文献内容或主题相关的文献信息。',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '相关文献的中文标题名称。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id_2` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `relevant_2` json NOT NULL COMMENT '与当前文献内容或主题相关的文献信息。',
  `doi_2` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `zh_name_2` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '相关文献的英文标题名称。',
  `data_source_2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '来源贴源库表名',
  `created_time_2` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在要素库中的创建时间。',
  `updated_time_2` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条数据最近一次更新的时间。',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_dwd_zh_paper_related_doi` (`doi`(191)) USING BTREE,
  KEY `idx_dzpr_logic_id` (`logic_id`) USING BTREE,
  KEY `idx_dwd_zh_paper_related_id_2` (`id_2`) USING BTREE,
  KEY `idx_dwd_zh_paper_related_doi_2` (`doi_2`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文关联文献信息';

-- gkx.dwd_zh_paper_title definition

CREATE TABLE `dwd_zh_paper_title` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `title_sequence` int NOT NULL DEFAULT '0' COMMENT '同一文献多个标题的顺序号。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的英文标题名称。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的中文标题名称。',
  `language_code` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题的语言代码。',
  `original_title` tinyint NOT NULL DEFAULT '0' COMMENT '是否为原始标题：否=0，是=1，未知=2。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`,`title_sequence`) USING BTREE,
  KEY `idx_dzpt_title_sequence` (`title_sequence`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文标题信息';

-- gkx.dwd_zh_project definition

CREATE TABLE `dwd_zh_project` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目记录的唯一主键标识。',
  `project_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目在管理系统中的编号。',
  `title` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目的名称或标题。',
  `project_source` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目所属的资助来源或立项来源。',
  `funded_institution` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '获得项目资助的机构名称。',
  `project_level` enum('国家级','省级','市级','县级','其他') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目所属的级别或层次。',
  `funded_amount` decimal(18,2) DEFAULT NULL COMMENT '项目获得的资助经费金额，单位为万元。',
  `discipline` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目所属的学科领域。',
  `discipline_code` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目所属学科的分类代码。',
  `fund_category` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目对应的基金或资助类别。',
  `funded_province` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目受资助机构所在的省份。',
  `participating_institution` json DEFAULT NULL COMMENT '参与项目研究或实施的机构信息。',
  `approval_year` int DEFAULT NULL COMMENT '项目获批立项的年份。',
  `approval_time` date DEFAULT NULL COMMENT '项目正式获批立项的时间。',
  `research_period` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目计划开展研究的时间期限。',
  `project_host` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目的主要负责人或主持人。',
  `participants` json DEFAULT NULL COMMENT '参与项目研究或实施的人员信息。',
  `keywords` json DEFAULT NULL COMMENT '描述项目研究主题的关键词。',
  `abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '项目申请书或标书中的摘要内容。',
  `final_report_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '项目结题报告中的摘要内容。',
  `project_page_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '项目详情页面的访问链接。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_zh_project_id` (`id`) USING BTREE,
  KEY `idx_dwd_zh_project_project_number` (`project_number`) USING BTREE,
  KEY `idx_dwd_zh_project_discipline_code` (`discipline_code`) USING BTREE,
  KEY `idx_dwd_zh_project_approval_year` (`approval_year`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内项目信息表';

-- gkx.dwd_zh_project_output definition

CREATE TABLE `dwd_zh_project_output` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目记录的唯一主键标识。',
  `total_outputs` int DEFAULT NULL COMMENT '项目产生的成果总数量。',
  `journal_articles_count` int DEFAULT NULL COMMENT '项目产出的期刊论文数量。',
  `conference_papers_count` int DEFAULT NULL COMMENT '项目产出的会议论文数量。',
  `degree_papers_count` int DEFAULT NULL COMMENT '项目产出的学位论文数量。',
  `patents_count` int DEFAULT NULL COMMENT '项目产出的专利数量。',
  `clinical_trials_count` int DEFAULT NULL COMMENT '项目产出的临床试验数量。',
  `books_count` int DEFAULT NULL COMMENT '项目产出的图书或专著数量。',
  `products_count` int DEFAULT NULL COMMENT '项目产出的产品数量。',
  `awards_count` int DEFAULT NULL COMMENT '项目获得的奖项数量。',
  `reports_count` int DEFAULT NULL COMMENT '项目产出的报告数量。',
  `other_outputs_count` int DEFAULT NULL COMMENT '项目产生的其他成果数量。',
  `output_journal_articles` json DEFAULT NULL COMMENT '项目产出的期刊文章内容',
  `output_patents` json DEFAULT NULL COMMENT '项目产出专利标题',
  `output_conference_papers` json DEFAULT NULL COMMENT '项目产出会议论文标题',
  `output_degree_papers` json DEFAULT NULL COMMENT '项目产出学位论文标题',
  `output_clinical_trials` json DEFAULT NULL COMMENT '项目产出临床试验标题',
  `output_books` json DEFAULT NULL COMMENT '项目产出图书专著标题',
  `output_products` json DEFAULT NULL COMMENT '项目产出产品标题',
  `output_awards` json DEFAULT NULL COMMENT '项目产出奖项标题',
  `output_reports` json DEFAULT NULL COMMENT '项目产出报告标题',
  `output_other` json DEFAULT NULL COMMENT '项目其他产出标题',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_zh_project_output_id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内项目-产出信息';

-- gkx.dwd_zh_report definition

CREATE TABLE `dwd_zh_report` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `report_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '中文报告记录的唯一主键标识。',
  `report_category` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标识报告所属的类别。',
  `title_cn` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '报告的中文标题名称。',
  `authors` json DEFAULT NULL COMMENT '报告作者的姓名或信息列表。',
  `organization` json DEFAULT NULL COMMENT '作者所属单位或报告完成单位名称。',
  `abstract_cn` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '报告内容的中文摘要信息。',
  `keywords_cn` json DEFAULT NULL COMMENT '描述报告主题内容的中文关键词。',
  `report_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标识报告的具体类型。',
  `page_count` int DEFAULT NULL COMMENT '报告全文的总页数。',
  `preparation_time` date DEFAULT NULL COMMENT '报告编制完成或形成的时间。',
  `approval_year` int DEFAULT NULL COMMENT '报告相关项目获批立项的年份。',
  `related_literature` json DEFAULT NULL COMMENT '与当前报告内容相关的文献信息。',
  `related_scholars` json DEFAULT NULL COMMENT '与当前报告主题相关的学者信息。',
  `related_institutions` json DEFAULT NULL COMMENT '与当前报告主题相关的机构信息。',
  `related_projects` json DEFAULT NULL COMMENT '与当前报告内容相关的项目信息。',
  `source_org` json DEFAULT NULL COMMENT '报告数据或内容的来源机构。',
  `visibility_scope` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '报告可被访问或查看的范围。',
  `project_annual_number` int DEFAULT NULL COMMENT '项目按年度管理的编号标识。',
  `contact_phone` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '报告相关联系人或单位的联系电话。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_dwd_zh_report_report_id` (`report_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文科技报告信息表';

-- gkx.ods_calculation definition

CREATE TABLE `ods_calculation` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分子理论计算的内部或来源库唯一标识',
  `molecular_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '化合物、材料或分子的标准英文名称',
  `reference` json DEFAULT NULL COMMENT '支持该条记录的论文、数据库页面或 DOI 等来源信息',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_calculation_molecular_name` (`molecular_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='分子理论计算';

-- gkx.ods_clinical definition

CREATE TABLE `ods_clinical` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '疾病或适应症在来源库中的唯一标识',
  `disease_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药物、试验或临床信息关联的疾病名称',
  `phenotype_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '临床表型在标准术语库中的唯一标识',
  `phenotype_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '疾病相关的临床表现、症状或表型名称',
  `associated_gene` json DEFAULT NULL COMMENT '与疾病、表型或多组学结果相关的基因名称',
  `references` json DEFAULT NULL COMMENT '支持该条记录的论文、数据库页面或 DOI 等来源信息',
  `disease_category` json DEFAULT NULL COMMENT '疾病在 ICD、肿瘤分类或其他标准体系中的层级分类',
  `symptoms` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '疾病或临床表型相关的主要症状',
  `related_disease` json DEFAULT NULL COMMENT '与当前疾病存在继发、共病、遗传或机制关联的疾病',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_clinical_disease_name` (`disease_name`) USING BTREE,
  KEY `idx_ods_clinical_phenotype_id` (`phenotype_id`) USING BTREE,
  KEY `idx_ods_clinical_phenotype_name` (`phenotype_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='临床信息表';

-- gkx.ods_clinical_trial definition

CREATE TABLE `ods_clinical_trial` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '临床试验信息的内部或来源库唯一标识',
  `trial_sponsor` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '临床试验登记记录中的研究标题',
  `disease_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药物、试验或临床信息关联的疾病名称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='临床试验信息表';

-- gkx.ods_company definition

CREATE TABLE `ods_company` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品企业对应的内部或来源库唯一标识',
  `firm_name` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品企业、生产企业或许可持有人名称',
  `address` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业注册地址、生产地址或经营地址',
  `duns_number` json DEFAULT NULL COMMENT '企业的 D-U-N-S 编码，用于企业识别和外部数据关联',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='药品企业表';

-- gkx.ods_company_base definition

CREATE TABLE `ods_company_base` (
  `id` bigint NOT NULL COMMENT '企业id',
  `name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业名称',
  `english_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业英文名称',
  `registration_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册号',
  `organization_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '组织机构号',
  `credit_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统一信用代码',
  `first_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业类型',
  `registered_capital` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册资本',
  `registered_add` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册地址',
  `scope` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '经营范围',
  `start_date` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '营业期限开始日期',
  `end_date` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '营业期限终止日期',
  `reg_organization` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '登记机关',
  `legal_representative` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '法人姓名',
  `legal_rep_type` int DEFAULT NULL COMMENT '法人类型',
  `approval_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '核准日期',
  `establish_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '成立日期',
  `cancel_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注销日期',
  `status_std` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业状态',
  `display` int DEFAULT NULL COMMENT '企业状态(1:正常存续, 2:注销,3:非工商主体,7:搬迁,8:停业,9:清算,10:其他)',
  `reg_capital_std` decimal(18,6) DEFAULT NULL COMMENT '注册资本金额',
  `unit` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册资本单位',
  `currency` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册资本币种',
  `real_capital` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '实缴资本',
  `real_capital_std` decimal(18,6) DEFAULT NULL COMMENT '实缴资本金额',
  `cancel_reason` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注销原因',
  `ori_reg_city` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册地所在市',
  `ori_reg_district` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册的所在区',
  `ori_reg_province` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册地所在省',
  `reg_xy` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '经度',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='基础信息';

-- gkx.ods_company_basic_tags definition

CREATE TABLE `ods_company_basic_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `business_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '业务类型',
  `capital_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业性质',
  `scale_tag` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业规模标签',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='基础属性标签';

-- gkx.ods_company_branch definition

CREATE TABLE `ods_company_branch` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `branch_id` bigint DEFAULT NULL COMMENT '分支机构的主体唯一键',
  `branch_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分支机构名称',
  `branch_reg_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分支机构注册号',
  `branch_credit_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分支机构统一信用代码',
  `branch_establish_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分支机构成立日期',
  `branch_company_status` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登记状态',
  `branch_cancel_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '注销日期',
  `is_history` int DEFAULT NULL COMMENT '使用标记(0: 非历史， 1：历史 )',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='分支机构';

-- gkx.ods_company_brief_tags definition

CREATE TABLE `ods_company_brief_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `brief` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公司简介摘要',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='企业简介';

-- gkx.ods_company_change definition

CREATE TABLE `ods_company_change` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `before` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更前内容',
  `after` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更后内容',
  `date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更日期',
  `change_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更类型(法定代表人变更, 主要人员变更, 经营范围变更, 注册资本变更, 股东信息变更, address, business, lp)',
  `change_type_std` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更类型(法定代表人变更, 主要人员变更, 经营范围变更, 注册资本变更, 股东信息变更)',
  `change_type_detail` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更类型详情',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='工商变更';

-- gkx.ods_company_contact_tags definition

CREATE TABLE `ods_company_contact_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `contact` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '联系人信息（联系人姓名，联系方式，类型，信息来源，更新日期，原始链接）',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='企业联系方式';

-- gkx.ods_company_diy_tags definition

CREATE TABLE `ods_company_diy_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `diy_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '特色资质标签',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='特色资质标签';

-- gkx.ods_company_history_name definition

CREATE TABLE `ods_company_history_name` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `history_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '曾用名',
  `start_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '名称开始使用日期',
  `end_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '名称结束使用日期',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='曾用名';

-- gkx.ods_company_honor_tags definition

CREATE TABLE `ods_company_honor_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `association_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '协会标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `award_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '荣誉奖项标签（奖项编码，奖项类型，奖项等级，级别，获奖日期，颁发单位，奖项全称，获奖年份）',
  `certification` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '资质认证（证书名称，证书编号，资质编码，获证年份，级别，状态，有效期起，有效期止，发证日期，发证机构）',
  `city_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '市级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `district_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '区县级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `national_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '国家级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `nonpublic_tags` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '私有标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `park_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '园区级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `permission` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '备案许可（许可事项名称，许可证号，许可类型编码，许可年份，管理层级，状态，有效期起，有效期止，发证日期，审批机关，许可生产范围）',
  `province_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '省级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `rank_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '榜单标签（标签名称，标签编码，年份，级别，具体名次，发布日期，发布机构）',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='企业荣誉标签';

-- gkx.ods_company_industry_tags definition

CREATE TABLE `ods_company_industry_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `industry_tag` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业标签（产业编码，产业名称，置信度，环节[环节编码，环节名称，级别，置信度]）',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='产业标签';

-- gkx.ods_company_license definition

CREATE TABLE `ods_company_license` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '许可证名称',
  `license_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '许可文件编号',
  `scope` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '许可内容',
  `start_date` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '有效期自',
  `end_date` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '有效期至',
  `organization` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '许可机关',
  `is_history` int DEFAULT NULL COMMENT '状态（0: 有效， 1: 历史）',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='行政许可';

-- gkx.ods_company_location_tags definition

CREATE TABLE `ods_company_location_tags` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `reg_province` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '省',
  `reg_city` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '市',
  `reg_district` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '区',
  `reg_xy` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '坐标',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='所在行政区';

-- gkx.ods_company_nei_code definition

CREATE TABLE `ods_company_nei_code` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `industry` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '最深一级的行业名称',
  `industry_l1_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '一级行业编码',
  `industry_l1_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '一级行业名称',
  `industry_l2_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '二级行业编码',
  `industry_l2_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '二级行业名称',
  `industry_l3_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '三级行业编码',
  `industry_l3_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '三级行业名称',
  `industry_l4_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '四级行业编码',
  `industry_l4_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '四级行业名称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='国民行业经济分类';

-- gkx.ods_company_recruit definition

CREATE TABLE `ods_company_recruit` (
  `id` bigint DEFAULT NULL COMMENT '关联企业基础表主键ID',
  `source_id` varchar(56) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '招聘事件ID',
  `company_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公司名称',
  `city` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '所在城市',
  `district` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '所在区',
  `title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '招聘职称',
  `salary` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '工资',
  `first_class` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '一级分类',
  `second_class` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '二级分类',
  `third_class` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '三级分类',
  `address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '工作地址',
  `start_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '招聘开始日期',
  `end_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '招聘截止日期',
  `education` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '教育',
  `recruit_number` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '招聘人数',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '职位描述',
  `experience` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '经验',
  `type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '招聘类别',
  `company_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公司地址',
  `url_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '外网链接',
  `source` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源：赶集，58....',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`source_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='招聘';

-- gkx.ods_company_reg_cap_change definition

CREATE TABLE `ods_company_reg_cap_change` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更类型',
  `date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更日期',
  `before` decimal(18,6) NOT NULL DEFAULT '0.000000' COMMENT '变更前注册资本',
  `after` decimal(18,6) NOT NULL DEFAULT '0.000000' COMMENT '变更后注册资本',
  `unit` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '单位',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='注册资本变更';

-- gkx.ods_company_shareholder definition

CREATE TABLE `ods_company_shareholder` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `investor_id` bigint DEFAULT NULL COMMENT '股东id',
  `investor_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '股东名称',
  `investor_type` int NOT NULL DEFAULT '0' COMMENT '股东类型(0:企业,1:个人,2:其他,3:港企,4:事业单位,5:政府机关,6:社会组织,7:工会,8:律师事务所)',
  `investor_detail_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '股东类型',
  `amount` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '投资金额',
  `amount_std` decimal(18,6) NOT NULL DEFAULT '0.000000' COMMENT '投资金额标准化（万元人民币）',
  `share_ratio` decimal(18,6) NOT NULL DEFAULT '0.000000' COMMENT '持股比例',
  `subscribed` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '认缴资金,认缴日期,认缴形式',
  `contributed` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '实缴金额,实缴日期,实缴形式',
  `stock_realcapital` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '实缴出资额',
  `country` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '股东国别',
  `include_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '股东进入日期',
  `remove_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '股东退出日期',
  `is_history` int NOT NULL DEFAULT '0' COMMENT '是否历史股东，0：当前股东，1：历史股东',
  `name_source` int NOT NULL DEFAULT '0' COMMENT '股东来源，0：官网同步，1：变更记录解析，2：其他源补充',
  `stock_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '股东类型',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='股东信息';

-- gkx.ods_company_staff definition

CREATE TABLE `ods_company_staff` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `staff_id` bigint NOT NULL DEFAULT '0' COMMENT '主要人员是机构时，该机构的company_id',
  `staff_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '清洗后主要人员名称',
  `staff_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '职位',
  `person_type` int NOT NULL DEFAULT '0' COMMENT 'employee_name类型，1：自然人，0：机构，2：非自然人非机构',
  `start_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主要人员任职开始日期',
  `end_date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主要人员任职截止日期',
  `is_history` int NOT NULL DEFAULT '0' COMMENT '是否历史主要人员，0：当前主要人员，1：历史主要人员',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='任职人员';

-- gkx.ods_company_transition_clean definition

CREATE TABLE `ods_company_transition_clean` (
  `id` bigint NOT NULL COMMENT '关联企业基础表主键ID',
  `name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业名称',
  `before` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '清洗后变更前地址',
  `after` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '清洗后变更后地址',
  `date` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更日期',
  `type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '变更类型',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='注册地址变更';

-- gkx.ods_crystal_structure definition

CREATE TABLE `ods_crystal_structure` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '晶体结构与性质的内部或来源库唯一标识',
  `formula` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '分子或晶体的化学组成式',
  `diffraction_radiation_type` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '晶体结构测定使用的 X 射线或中子衍射辐射类型',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='晶体结构与性质';

-- gkx.ods_deal definition

CREATE TABLE `ods_deal` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药物交易的内部或来源库唯一标识',
  `drug_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '交易涉及的药品、候选药物或管线资产名称',
  `licensor` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '在药物交易中授出研发、生产或商业化权益的公司',
  `licensee` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '在药物交易中获得相关权益的公司',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_deal_drug_name` (`drug_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='药物交易';

-- gkx.ods_drug definition

CREATE TABLE `ods_drug` (
  `application_number` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药品在监管机构申请或批准体系中的编号，用于关联审评、批准和标签信息',
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品记录的内部或来源库唯一标识，用于去重和跨表关联',
  `drug_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药物安全、交易或试验记录中涉及的药品名称',
  `brand_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药品上市销售时使用的品牌名称',
  `generic_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药品非专利通用名称或国际通用名称',
  `active_ingredients` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药品中具有治疗作用的主要成分，可包含一个或多个成分',
  `route` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药品进入人体的给药方式，如口服、注射、皮下等',
  `dosage_form` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药品制剂形态，如片剂、胶囊、注射液等',
  `application_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '监管申请类别，如 NDA、ANDA、BLA 等',
  `sponsor_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '提交药品申请或持有上市许可的机构全称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_drug_application_number` (`application_number`) USING BTREE,
  KEY `idx_ods_drug_drug_name` (`drug_name`) USING BTREE,
  KEY `idx_ods_drug_brand_name` (`brand_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='药品信息表';

-- gkx.ods_drug_profile definition

CREATE TABLE `ods_drug_profile` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药物档案的内部或来源库唯一标识',
  `brand_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品上市销售时使用的品牌名称',
  `indications_and_usage` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '药品标签中关于适应症、适用人群和使用场景的说明',
  `mechanism_of_action` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '药物发挥治疗作用的生物学或药理学机制',
  `substance_name` json DEFAULT NULL COMMENT '药品中具有治疗作用的主要成分，可包含一个或多个成分',
  `contraindications` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '不应使用该药物的疾病、状态或用药条件',
  `warnings_and_cautions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '药品标签中的重要风险、警示和用药注意事项',
  `adverse_reactions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '临床试验或上市后报告中记录的药物不良反应',
  `dosage_and_administration` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '药品推荐给药剂量、频率、调整方式和用药方法',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_drug_profile_brand_name` (`brand_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='药物档案表';

-- gkx.ods_drug_substance definition

CREATE TABLE `ods_drug_substance` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '化合物性质与信息的内部或来源库唯一标识',
  `molecular_name` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '化合物、材料或分子的标准英文名称',
  `formula` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分子或晶体的化学组成式',
  `in_chi_key` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'InChI 的固定长度哈希标识，用于化合物快速匹配和去重',
  `in_chi` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '化合物的 IUPAC 国际化学标识符',
  `std_smiles` varchar(4000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '化合物标准化后的 SMILES 结构表示',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_drug_substance_molecular_name` (`molecular_name`(191)) USING BTREE,
  KEY `idx_ods_drug_substance_in_chi_key` (`in_chi_key`) USING BTREE,
  KEY `idx_ods_drug_substance_in_chi` (`in_chi`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='化合物性质与信息';

-- gkx.ods_en_author definition

CREATE TABLE `ods_en_author` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `paper_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `author_sequence` int NOT NULL DEFAULT '0' COMMENT '作者在文献中的顺序。',
  `author_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者的唯一主键 id',
  `en_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者的英文名称',
  `zh_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者中文名',
  `orcid` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '作者ORCID。',
  `author_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '作者类型，如机构作者等。',
  `surname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '作者姓。',
  `given_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '作者名。',
  `initials` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '作者姓名首字母。',
  `preferred_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '作者首选姓名。',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者email',
  `correspond` tinyint NOT NULL DEFAULT '0' COMMENT '是否为通讯作者',
  `institution` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '作者所属机构或单位的名称。',
  `affiliation` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者地址',
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者单位所在城市。',
  `state` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者单位所在州或省。',
  `postal_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者单位邮政编码。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`,`author_sequence`) USING BTREE,
  KEY `idx_ods_en_author_paper_id` (`paper_id`) USING BTREE,
  KEY `idx_ods_en_author_author_id` (`author_id`) USING BTREE,
  KEY `idx_ods_en_author_orcid` (`orcid`) USING BTREE,
  KEY `idx_ods_en_author_surname` (`surname`(191)) USING BTREE,
  KEY `idx_ods_en_author_given_name` (`given_name`(191)) USING BTREE,
  KEY `idx_ods_en_author_preferred_name` (`preferred_name`(191)) USING BTREE,
  KEY `idx_ods_en_author_city` (`city`(191)) USING BTREE,
  KEY `idx_ods_en_author_state` (`state`(191)) USING BTREE,
  KEY `idx_ods_en_author_postal_code` (`postal_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文文献作者详情信息';

-- gkx.ods_en_journal definition

CREATE TABLE `ods_en_journal` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `paper_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '期刊、会议或预印本记录的唯一标识。',
  `publication_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标识出版载体的类型，如期刊、会议或预印本等。',
  `publisher_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊出版商名称',
  `correspond_method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '通讯方式',
  `country` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊、会议或出版机构所属的国家或地区。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊、顶会或预印本平台的英文名称。',
  `name_abbr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊、会议或预印本名称的简称或缩写。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊、顶会或预印本平台的中文名称。',
  `issn_print` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国际标准连续出版物编号。纸印出版 issn',
  `issn_online` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国际标准连续出版物编号。在网发行 issn',
  `jn_official` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '期刊官方网站地址。',
  `en_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '期刊、会议或预印本平台的英文简介或说明。',
  `zh_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '期刊描述，中文描述',
  `establish_time` int NOT NULL DEFAULT '0' COMMENT '期刊首次创办或发行的时间。',
  `annual_publication` int NOT NULL DEFAULT '0' COMMENT '期刊或会议每年发表文章的数量。',
  `review` tinyint NOT NULL DEFAULT '0' COMMENT '标识该期刊是否为综述类期刊。',
  `impact_factor` double NOT NULL DEFAULT '0' COMMENT '期刊或会议的影响力评价指标。',
  `jcr_zone` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊在 JCR 等评价体系中的分区信息。',
  `quartile` tinyint NOT NULL DEFAULT '0' COMMENT '中国科学院期刊分区',
  `review_period` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊从投稿到审稿完成的平均周期。',
  `self_rate` double NOT NULL DEFAULT '0' COMMENT '期刊文献中自我引用所占的比例。',
  `jci` double NOT NULL DEFAULT '0' COMMENT 'JCI期刊引文指标',
  `oa_quote_rate` double NOT NULL DEFAULT '0' COMMENT '期刊OA文献被引用占比',
  `article_rate` double NOT NULL DEFAULT '0' COMMENT '期刊的研究性文章占比',
  `correct_rate` double NOT NULL DEFAULT '0' COMMENT '期刊出版后修正文章占比',
  `revoke_rate` double NOT NULL DEFAULT '0' COMMENT '期刊文献撤稿占比',
  `top` tinyint NOT NULL DEFAULT '0' COMMENT '标识期刊或会议是否为所在领域的顶级刊物。',
  `warning` tinyint NOT NULL DEFAULT '0' COMMENT '标识期刊是否处于预警状态。',
  `is_sci` tinyint NOT NULL DEFAULT '0' COMMENT '标识期刊是否被 SCI 收录。',
  `publish_period` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的出版频率或发行周期。',
  `layout_cost` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊发表论文所需的版面费用。',
  `paper_nums` int NOT NULL DEFAULT '0' COMMENT '期刊、会议或平台已发表论文的数量。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE,
  KEY `idx_ods_en_journal_paper_id` (`paper_id`) USING BTREE,
  KEY `idx_oej_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_ods_en_journal_en_name` (`en_name`(191)) USING BTREE,
  KEY `idx_ods_en_journal_name_abbr` (`name_abbr`(191)) USING BTREE,
  KEY `idx_ods_en_journal_zh_name` (`zh_name`(191)) USING BTREE,
  KEY `idx_ods_en_journal_issn_print` (`issn_print`) USING BTREE,
  KEY `idx_ods_en_journal_issn_online` (`issn_online`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文期刊详情信息';

-- gkx.ods_en_journal_bak_20260710 definition

CREATE TABLE `ods_en_journal_bak_20260710` (
  `F_ID` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_PaperID` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_Title` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_title_alternative` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_abbrev_title` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_author` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_author_alternative` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_affiliation` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_affiliation_alternative` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_Abstract` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_Abstract_alternative` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_Keyword` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_Keyword_alternative` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_Language` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_Other_language` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_year` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_volume` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_issue` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_Paper_type` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_Classification` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_DOI` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_Start_page` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_End_page` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_page` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_Total_page_number` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_Journal` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_Journal_alternative` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_journal_abbrev` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_journal_id` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_ISSNp` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_ISSNe` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_DateReceived` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_DateSubmitted` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_DatePublish` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_DateRevision` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_Updatedtime` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_Content` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_Subject` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_column` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_column_alternative` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_AbstractUrl` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_FulltextUrl` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_PaperUrlContent` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_issue_url` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_journal_url` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `yn_free` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_Fund` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_Fundid` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_Fundaffiliation` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_refrences` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_publiser` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_batchid` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `F_article_id` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='万方外文期刊信息';

-- gkx.ods_en_paper definition

CREATE TABLE `ods_en_paper` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `pmid` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'PubMed标识符。',
  `online_status` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献在线可用状态。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的英文标题名称。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的中文标题名称。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '关联出版物的id，用于获取期刊详情信息',
  `paper_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献所属出版物的章节名称，栏目等。',
  `publication_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标识出版载体的类型，如期刊、会议或预印本等。',
  `publication_en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊、顶会或预印本平台的英文名称。',
  `issn_print` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国际标准连续出版物编号。纸印出版 issn',
  `issn_online` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国际标准连续出版物编号。在网发行 issn',
  `volume` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献发表所在期刊的卷号。',
  `issue` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献发表所在期刊的期号。',
  `first_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文在期刊中的起始页码。',
  `last_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文在期刊中的结束页码。',
  `cover_year_start` date NOT NULL DEFAULT '1970-01-01' COMMENT '文献正式发表的年份。',
  `cover_date_start` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献正式发表的时间。',
  `language` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献或期刊出版使用的语言类型。',
  `abstract_available` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '摘要是否可用。',
  `open_access` tinyint NOT NULL DEFAULT '0' COMMENT '标识期刊或论文是否为开放获取。',
  `paper_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献在官网或来源平台中的访问链接。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_en_paper_doi` (`doi`(191)) USING BTREE,
  KEY `idx_ods_en_paper_pmid` (`pmid`) USING BTREE,
  KEY `idx_ods_en_paper_online_status` (`online_status`) USING BTREE,
  KEY `idx_ods_en_paper_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_ods_en_paper_paper_type` (`paper_type`(191)) USING BTREE,
  KEY `idx_oep_publication_en_name` (`publication_en_name`(191)) USING BTREE,
  KEY `idx_ods_en_paper_issn_print` (`issn_print`) USING BTREE,
  KEY `idx_ods_en_paper_issn_online` (`issn_online`) USING BTREE,
  KEY `idx_oep_cover_year_start` (`cover_year_start`) USING BTREE,
  KEY `idx_oep_cover_date_start` (`cover_date_start`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文详情信息';

-- gkx.ods_en_paper_abstract definition

CREATE TABLE `ods_en_paper_abstract` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `abstract_sequence` int NOT NULL DEFAULT '0' COMMENT '同一文献多个摘要的顺序号',
  `language` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献或期刊出版使用的语言类型。',
  `original_abstract` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '是否为原始摘要。',
  `en_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献内容的英文摘要信息。',
  `zh_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献内容的中文摘要信息。',
  `abstract_source` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '摘要来源。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`,`abstract_sequence`) USING BTREE,
  KEY `idx_ods_en_paper_abstract_id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文摘要信息';

-- gkx.ods_en_paper_citation definition

CREATE TABLE `ods_en_paper_citation` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '关联出版物的id，用于获取期刊详情信息',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '引用文献的英文标题名称。',
  `publication_en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献出版物的英文名称。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE,
  KEY `idx_ods_en_paper_citation_id` (`id`) USING BTREE,
  KEY `idx_oepc_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_ods_en_paper_citation_doi` (`doi`(191)) USING BTREE,
  KEY `idx_oepc_publication_en_name` (`publication_en_name`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文引用文献信息';

-- gkx.ods_en_paper_classification definition

CREATE TABLE `ods_en_paper_classification` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `scope` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊或会议所属的大类学科领域。',
  `sub_scope` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊或会议所属的细分学科主题。',
  `keywords` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '描述论文主题内容的关键词。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE,
  KEY `idx_oepc_id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文分类信息';

-- gkx.ods_en_paper_funding definition

CREATE TABLE `ods_en_paper_funding` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `funds` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '支持该论文研究的基金或资助项目信息。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE,
  KEY `idx_ods_en_paper_funding_id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文基金信息';

-- gkx.ods_en_paper_reference definition

CREATE TABLE `ods_en_paper_reference` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '关联出版物的id，用于获取期刊详情信息',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献的英文标题名称。',
  `publication_en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献出版物的英文名称。',
  `cover_year_start` date NOT NULL DEFAULT '1970-01-01' COMMENT '文献正式发表的年份。',
  `volume` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献发表所在期刊的卷号。',
  `issue` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献发表所在期刊的期号。',
  `first_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献在期刊中的起始页码。',
  `last_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献在期刊中的结束页码。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE,
  KEY `idx_ods_en_paper_reference_id` (`id`) USING BTREE,
  KEY `idx_oepr_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_ods_en_paper_reference_doi` (`doi`(191)) USING BTREE,
  KEY `idx_oepr_publication_en_name` (`publication_en_name`(191)) USING BTREE,
  KEY `idx_oepr_cover_year_start` (`cover_year_start`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文参考文献信息';

-- gkx.ods_en_paper_related definition

CREATE TABLE `ods_en_paper_related` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `relevant` json NOT NULL COMMENT '与当前文献内容或主题相关的文献信息。',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '相关文献的英文标题名称。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE,
  KEY `idx_ods_en_paper_related_id` (`id`) USING BTREE,
  KEY `idx_ods_en_paper_related_doi` (`doi`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文关联文献信息';

-- gkx.ods_en_paper_title definition

CREATE TABLE `ods_en_paper_title` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `title_sequence` int NOT NULL DEFAULT '0' COMMENT '同一文献多个标题的顺序号。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的英文标题名称。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的中文标题名称。',
  `language_code` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题的语言代码。',
  `language` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题的语言类型。',
  `original_title` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '是否为原始标题。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`,`title_sequence`) USING BTREE,
  KEY `idx_ods_en_paper_title_id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='英文论文标题信息';

-- gkx.ods_en_policy definition

CREATE TABLE `ods_en_policy` (
  `IR_URLTITLE` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_URLTITLE` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `FY_URLTITLE` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `IR_URLTIME` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `IR_SITENAME` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_MEDIA_PRODUCT_NAME` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `IR_CONTENT` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `SY_CONTENT` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `FY_CONTENT` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `IR_ABSTRACT` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `SY_ABSTRACT` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `IR_URLNAME` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `IR_URLDATE` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `IR_ATTACHMENT` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `IR_AUTHORS` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `IR_CHANNEL` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `IR_LANGUAGE` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `IR_URLCONTENT` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `SY_AREA_LIST` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_AREA_LIST_CODE` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_KEYWORDS` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_MEDIA_AREA` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_MEDIA_AREA_CODE` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_MEDIA_DIRECT_UNIT` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_MEDIA_INDUSTRY` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_MEDIA_RANK_CODE` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_MEDIA_TAG` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_MEDIA_TYPE1` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_MEDIA_TYPE2` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_MEDIA_TYPE3` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SY_NAME` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='拓尔思国外政策信息';

-- gkx.ods_en_project definition

CREATE TABLE `ods_en_project` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主键',
  `project_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目编号',
  `title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目名称',
  `project_source` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目来源',
  `funded_institution` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '依托单位',
  `project_level` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目级别',
  `funded_amount` decimal(12,2) DEFAULT NULL COMMENT '资助金额',
  `discipline` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '学科',
  `discipline_code` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '学科代码',
  `fund_category` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '基金类别',
  `funded_province` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '资助省份',
  `participating_institution` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '参与单位',
  `approval_year` date DEFAULT NULL COMMENT '批准年度',
  `approval_time` date DEFAULT NULL COMMENT '批准日期',
  `research_period` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '研究周期',
  `project_host` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目负责人',
  `participants` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '参与人员',
  `keywords` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '关键词',
  `abstract` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '项目摘要',
  `project_page_url` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目详情页',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-国外项目信息表';

-- gkx.ods_en_project_output definition

CREATE TABLE `ods_en_project_output` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'UUID主键',
  `total_outputs` int DEFAULT NULL COMMENT '项目总产出数量',
  `journal_articles_count` int DEFAULT NULL COMMENT '期刊文章数量',
  `conference_papers_count` int DEFAULT NULL COMMENT '会议论文数量',
  `books_count` int DEFAULT NULL COMMENT '图书专著数量',
  `degree_papers_count` int DEFAULT NULL COMMENT '学位论文数量',
  `patents_count` int DEFAULT NULL COMMENT '专利数量',
  `clinical_trials_count` int DEFAULT NULL COMMENT '临床试验数量',
  `products_count` int DEFAULT NULL COMMENT '产品数量',
  `awards_count` int DEFAULT NULL COMMENT '奖项数量',
  `reports_count` int DEFAULT NULL COMMENT '报告数量',
  `other_outputs_count` int DEFAULT NULL COMMENT '其他产出数量',
  `output_journal_articles` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '期刊文章',
  `output_conference_papers` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '会议论文',
  `output_books` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '图书专著',
  `output_degree_papers` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '学位论文',
  `output_patents` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '专利',
  `output_clinical_trials` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '临床试验',
  `output_products` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '产品',
  `output_awards` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '奖项',
  `output_reports` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '报告',
  `output_other` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '其他成果',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-国外项目产出信息表';

-- gkx.ods_en_report definition

CREATE TABLE `ods_en_report` (
  `Identifier_ID` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Report_Num` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Title_Title` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `Title_AlterNativeTitle` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `Creator_Creator` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `Creator_AlterNativeCreator` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `Creator_Org` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `Creator_AlterNativeOrg` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `Date_Issued` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Description_Abstract` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `Description_AlternativeAbstract` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `Subject_Keywords` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `Subject_AlternativeKeywords` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `Subject_CLC` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `Subject_SelfFL` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `Report_Source` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Language_Language` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Place_Counry` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Source_Page` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Source_PageCount` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Yn_publition` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Report_Type` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Publisher_Publisher` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `f_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Date_Download` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `DataLink` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `Collection_Number` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Document_Type` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Sponsor` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `IS_OA` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_Publish_Date` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `F_FulltextUrl` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='万方外文报告信息';

-- gkx.ods_event definition

CREATE TABLE `ods_event` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '会展的内部或来源库唯一标识',
  `event_name` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '医药或生命科学相关会议、展会名称',
  `organizer` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '会议或展会的主办机构',
  `start_date` date DEFAULT NULL COMMENT '会议或展会开始日期',
  `end_date` date DEFAULT NULL COMMENT '会议或展会结束日期',
  `event_url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '会议或展会官网或详情页 URL',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='会展';

-- gkx.ods_hels_info definition

CREATE TABLE `ods_hels_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `ztwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主体唯一键',
  `lx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '类型',
  `xxmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '学校名称',
  `xxbsm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '学校标识码',
  `zgbm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '主管部门',
  `bxcc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '办学层次',
  `tyshxydm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `ywm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '英文名',
  `xxdz` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '学校地址',
  `szsh` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '所在省',
  `szs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '所在市',
  `szq` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '所在区',
  `gw` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '官网',
  `dh` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '电话',
  `yx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '邮箱',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_hels_info_ztwyj` (`ztwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='高校信息表';

-- gkx.ods_hycy_aquaculture_veterinary_drugs_enterprise_list definition

CREATE TABLE `ods_hycy_aquaculture_veterinary_drugs_enterprise_list` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：企业名称+通用名+规格+批准文号，连接字符：-，md5',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业的中文名称；',
  `common_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '通用名',
  `specifications` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '规格型号',
  `trade_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '商品名',
  `approval_number` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '批准文号',
  `approval_date` date DEFAULT NULL COMMENT '批准日期',
  `validity_period` date DEFAULT NULL COMMENT '有效期至',
  `failure_reason` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '失效原因',
  `change_situation` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '变更情况',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_水产养殖用兽药名录';

-- gkx.ods_hycy_aquatic_new_species definition

CREATE TABLE `ods_hycy_aquatic_new_species` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：品种登记号+品种名称+育种单位，连接字符：-，md5',
  `reg_no` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '品种登记号',
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '品种名称',
  `breeding_unit` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '育种单位',
  `stat_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '年份时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_水产新品种认定情况及育种单位统计表';

-- gkx.ods_hycy_china_classification_society_marine_product_list definition

CREATE TABLE `ods_hycy_china_classification_society_marine_product_list` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：证书编号+工作类型+有效期至+产品名称+工厂名称，连接字符：-，md5',
  `certificate_number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件编号',
  `work_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '工作类型',
  `validity_period` date DEFAULT NULL COMMENT '有效期至',
  `product_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品名称',
  `factory_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '工厂名称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_中国船级社船用产品目录';

-- gkx.ods_hycy_china_mainland_submarine_cable definition

CREATE TABLE `ods_hycy_china_mainland_submarine_cable` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则:城市名称+光缆名称+带宽+长度+起始地区，连接字符：-，md5',
  `province_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `province_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `cable_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '光缆名称',
  `bandwidth` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '带宽',
  `length` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '长度',
  `origin_region` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '起始地区',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_中国大陆地区海底光缆情况';

-- gkx.ods_hycy_china_major_city_lng_receiving_capacity definition

CREATE TABLE `ods_hycy_china_major_city_lng_receiving_capacity` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则:城市名称+统计时间，连接字符：-，md5',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '存在非大陆城市',
  `receipt_capacity` int NOT NULL DEFAULT '0' COMMENT '接收能力',
  `receipt_unit` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '接收单位',
  `rank` int DEFAULT NULL COMMENT '排名',
  `lng_receipt_station` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'LNG接收站',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统计时间',
  `update_frequency` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '更新频次',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_中国主要城市LNG接收能力';

-- gkx.ods_hycy_china_ocean_large_model definition

CREATE TABLE `ods_hycy_china_ocean_large_model` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则:大模型名称，连接字符：-，md5',
  `model_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '大模型名称',
  `research_entity_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '或归属单位',
  `research_entity_city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主体所在城市',
  `domain_oriented` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '面向领域',
  `features_progress` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技术特点与进展',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_国内海洋大模型情况';

-- gkx.ods_hycy_china_offshore_field definition

CREATE TABLE `ods_hycy_china_offshore_field` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则:油田名称+运营主体名称，连接字符：-，md5',
  `oilfield_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '油田名称',
  `operator_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '运营主体名称',
  `reserves` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '储量',
  `production_scale` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '油当量',
  `geological_features` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '地质特点',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统计时间',
  `update_frequency` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '指标更新频次，年更、季更等',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_中国海上油气田信息';

-- gkx.ods_hycy_china_offshore_production definition

CREATE TABLE `ods_hycy_china_offshore_production` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则:年份，连接字符：-，md5',
  `year` int NOT NULL DEFAULT '0' COMMENT '年份',
  `oil_output` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '单位:万吨',
  `gas_output` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '单位:亿立方米',
  `oil_gas_total_output` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '油当量,单位:万吨',
  `update_frequency` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '更新频次',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_中国海洋油气田产量情况';

-- gkx.ods_hycy_china_offshore_production_growth definition

CREATE TABLE `ods_hycy_china_offshore_production_growth` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则:油田名称+统计时间，连接字符：-，md5',
  `rank` int NOT NULL DEFAULT '0' COMMENT '排名',
  `oilfield_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '油田名称',
  `oge` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT '油气当量',
  `oge_unit` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '油气单位',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统计时间',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '备注',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_中国海洋油气产量增长情况';

-- gkx.ods_hycy_csad_ship definition

CREATE TABLE `ods_hycy_csad_ship` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：船检登记号，连接字符：-，md5',
  `ship_registration_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '船检登记号',
  `ship_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '船名',
  `haihe_river_ship` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '海河船',
  `gross_tonnage` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '总吨位',
  `ship_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '船舶类型',
  `ship_owner` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '船舶所有人',
  `ship_operator` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '船舶经营人',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_CSAD船舶';

-- gkx.ods_hycy_enterprise_indicators definition

CREATE TABLE `ods_hycy_enterprise_indicators` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：标准指标名称+企业名称+统计时间，连接字符：-，md5',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业名称',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '指标统计时间',
  `update_frequency` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '指标更新频次，年更、季更等',
  `index_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标准指标名称',
  `data` decimal(18,2) DEFAULT NULL COMMENT '标准数值',
  `unit` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标准单位',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_企业指标表';

-- gkx.ods_hycy_gas_supply definition

CREATE TABLE `ods_hycy_gas_supply` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：城市名称+气源名称，连接字符：-，md5',
  `province_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `province_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `gas_source_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '气源名称',
  `gas_source_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '气源类型',
  `gas_source_origin` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '气源来源',
  `ownership_structure` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '股权结构',
  `tank_capacity` decimal(38,20) DEFAULT NULL COMMENT '储罐规模',
  `tank_capacity_unit` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '储罐规模单位',
  `annual_supply_capacity` decimal(38,20) DEFAULT NULL COMMENT '年供应能力',
  `annual_supply_capacity_unit` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '年供应能力单位',
  `is_lng_refill_capability` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '是否具备LNG补液功能',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_天然气供应信息表';

-- gkx.ods_hycy_global_alternative_marine_fuel_market_demand_scale definition

CREATE TABLE `ods_hycy_global_alternative_marine_fuel_market_demand_scale` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：燃料类别+年份，连接字符：-，md5',
  `fuel_category` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '燃料类别',
  `year` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '年份',
  `market_demand` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '市场需求',
  `market_scale` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '市场规模',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_船用替代燃料全球市场需求及规模预测';

-- gkx.ods_hycy_global_cruise_capacity_distribution definition

CREATE TABLE `ods_hycy_global_cruise_capacity_distribution` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：指标名称+船型+船龄范围+统计时间，连接字符：-，md5',
  `ship_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '船型',
  `ship_age_range` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '船龄范围',
  `index_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '指标名称',
  `data` decimal(18,2) DEFAULT NULL COMMENT '标准数值',
  `unit` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标准单位',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '统计时间',
  `update_frequency` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '指标更新频次，年更、季更等',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_全球邮轮运力分布';

-- gkx.ods_hycy_green_fuel_enterprise definition

CREATE TABLE `ods_hycy_green_fuel_enterprise` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：城市名称+产业链环节，连接字符：-，md5',
  `province_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `province_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `industry_chain_link` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业链环节',
  `enterprise_name` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业名称',
  `core_product_service` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '优势产品或服务',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_绿色燃料加注产业信息表';

-- gkx.ods_hycy_index definition

CREATE TABLE `ods_hycy_index` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：级别+区域+省份+城市+区县+经济区+统计时间+标准指标名称+采集来源，连接字符：-，md5',
  `level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '指标的空间级别',
  `region` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '全球、重点国家等',
  `province` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '省份',
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '城市',
  `district` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '区县',
  `other_region` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '长三角、珠三角等经济区',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统计时间',
  `scope` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '年度、季度、月度等周期',
  `index_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '标准指标名称',
  `data` decimal(18,2) DEFAULT NULL COMMENT '标准数值',
  `unit` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标准单位',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_指标库';

-- gkx.ods_hycy_industry definition

CREATE TABLE `ods_hycy_industry` (
  `id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：类型、产业编码、环节编码',
  `record_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '实体类型',
  `industry_chain_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业链ID',
  `entity_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '实体ID',
  `industry_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业编码',
  `industry_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业名称',
  `link_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '环节编码',
  `link_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '环节名称',
  `chain_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '挂链时间',
  `chain_operator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '挂链人',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='上链结果表';

-- gkx.ods_hycy_international_shipping_agency_enterprises_registration definition

CREATE TABLE `ods_hycy_international_shipping_agency_enterprises_registration` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：国际船舶代理企业名称+备案回执文号+备案年份，连接字符：-，md5',
  `number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '序号',
  `international_ship_agent_enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业工商注册的名称',
  `registered_address` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册地址',
  `record_receipt_number` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '备案回执文号',
  `annual_filing` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '备案年份',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_国际船舶代理企业备案表';

-- gkx.ods_hycy_international_shipping_certificate_effective_enterprise definition

CREATE TABLE `ods_hycy_international_shipping_certificate_effective_enterprise` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：证书编号+企业中文名称，连接字符：-，md5',
  `number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '序号',
  `certificate_number` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '证件编号',
  `enterprise_chinese_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业的中文名称；',
  `enterprise_english_name` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '生产企业的英文名称；',
  `registered_address` varchar(600) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册地址',
  `business_line` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '业务种类',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_国际班轮运输经营资格登记证有效企业';

-- gkx.ods_hycy_leading_maritime_capitals definition

CREATE TABLE `ods_hycy_leading_maritime_capitals` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：榜单名称+一级指标+二级指标+统计时间+城市名称，连接字符：-，md5',
  `rank_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '榜单名称',
  `first_level_index` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '一级指标',
  `second_level_index` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '二级指标',
  `rank` int NOT NULL DEFAULT '0' COMMENT '排名',
  `statistical_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '统计时间',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '城市名称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_世界领先海事之都报告城市数据';

-- gkx.ods_hycy_marine_alternative_fuel_cost definition

CREATE TABLE `ods_hycy_marine_alternative_fuel_cost` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：燃料类别+燃料类型+生产路线+当前生产成本+远期生产成本，连接字符：-，md5',
  `fuel_category` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '燃料类别',
  `fuel_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '燃料类型',
  `production_route` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '生产路线',
  `current_production_cost` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '当前生产成本',
  `future_production_cost` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '远期生产成本',
  `cost_currency` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '成本货币单位',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_船用替代燃料生产成本对比表';

-- gkx.ods_hycy_marine_energy_industry_carrier definition

CREATE TABLE `ods_hycy_marine_energy_industry_carrier` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：创新载体名称+载体类型+级别，连接字符：-，md5',
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '创新载体名称',
  `category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '载体类型',
  `level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '级别',
  `charge_authority` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '主管部门',
  `support_unit_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '依托单位名称',
  `support_unit_flag` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业;科研机构;高校',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '立项年度',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_海洋能源创新平台载体名单';

-- gkx.ods_hycy_marine_forecast_data definition

CREATE TABLE `ods_hycy_marine_forecast_data` (
  `id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：区域、分析时间、预报时间、浪高、分析内容',
  `analysis_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分析类型',
  `region` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '区域',
  `analysis_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '分析时间',
  `forecast_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '预报时间',
  `wave_height` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '浪高',
  `weather_condition` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '天气状况',
  `analysis_content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分析内容',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋分析预报数据';

-- gkx.ods_hycy_marine_observation_data definition

CREATE TABLE `ods_hycy_marine_observation_data` (
  `id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：站点名称、观测时间、水温、盐度、风速、风向、PH值',
  `data_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '实测数据类型',
  `station_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '站点名称',
  `longitude` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '经度',
  `latitude` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '纬度',
  `observation_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '观测时间',
  `water_temp` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '水温',
  `salinity` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '盐度',
  `wind_speed` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '风速',
  `wind_direction` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '风向',
  `ph_value` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT 'pH值',
  `dissolved_oxygen` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '溶解氧',
  `species_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '生物名称',
  `quantity` decimal(38,20) NOT NULL DEFAULT '0.00000000000000000000' COMMENT '数量',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋实测数据';

-- gkx.ods_hycy_marine_remote_sensing_data definition

CREATE TABLE `ods_hycy_marine_remote_sensing_data` (
  `id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：卫星名称、拍摄时间、区域、分辨率、影像地址',
  `remote_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '遥感类型',
  `satellite_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '卫星名称',
  `capture_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '拍摄时间',
  `region` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '区域',
  `resolution` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分辨率',
  `image_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '影像地址',
  `data_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据说明',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋地理遥感数据';

-- gkx.ods_hycy_methanol_production_cost_trend_prediction definition

CREATE TABLE `ods_hycy_methanol_production_cost_trend_prediction` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：一级分类+二级分类+当前生产成本+远期生产成本，连接字符：-，md5',
  `first_level` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技术路线的分类',
  `second_level` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技术路线的分类',
  `current_production_cost` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '当前生产成本',
  `forward_production_cost` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '远期生产成本',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_甲醇生产成本及趋势预测';

-- gkx.ods_hycy_nvocc_operator_list definition

CREATE TABLE `ods_hycy_nvocc_operator_list` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：企业中文名称+企业英文名称，连接字符：-，md5',
  `enterprise_chinese_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业的中文名称；',
  `enterprise_english_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业英文名称',
  `enterprise_english_short_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业英文简称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_无船承运业务经营者名录';

-- gkx.ods_hycy_offshore_fishing_company_evaluation definition

CREATE TABLE `ods_hycy_offshore_fishing_company_evaluation` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：指标类别+一级指标+二级指标+三级指标，连接字符：-，md5',
  `category` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '指标类别',
  `first_index` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '一级指标',
  `sec_index` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '二级指标',
  `third_index` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '三级指标',
  `score` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '分',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '备注说明',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_全国远洋渔业企业履约评估表';

-- gkx.ods_hycy_pelagic_fishery_enterprise_eval_results definition

CREATE TABLE `ods_hycy_pelagic_fishery_enterprise_eval_results` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：企业名称，连接字符：-，md5',
  `number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '序号',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业的中文名称；',
  `score` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT '得分',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_远洋渔业企业履约评估结果';

-- gkx.ods_hycy_port_operation_license_form definition

CREATE TABLE `ods_hycy_port_operation_license_form` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：企业名称+证书编号+证件起始日期+证件终止日期+证件有效期，连接字符：-，md5',
  `number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '序号',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业工商注册的名称',
  `legal_representative` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '法定代表人',
  `certificate_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件名称',
  `certificate_number` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '证件编号',
  `issuing_authority` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '发证机关',
  `registered_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '注册地址',
  `operating_area` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '经营地域',
  `business_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '经营业务类型',
  `business_place` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '经营场所所在港区',
  `dangerous_goods_operation_certificate` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '港口危险货物作业附证',
  `dangerous_goods_operation` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '从事危险货物港口作业情况',
  `certificate_start_date` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件起始日期',
  `certificate_end_date` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件终止日期',
  `certificate_validity_period` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件有效期',
  `certificate_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件状态',
  `remark` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '备注说明',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_港口经营许可表';

-- gkx.ods_hycy_shanghai_domestic_water_transport_directory definition

CREATE TABLE `ods_hycy_shanghai_domestic_water_transport_directory` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：证书编号+企业名称，连接字符：-，md5',
  `certificate_number` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件编号',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业的中文名称；',
  `main_business_passenger_transport` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '主营旅客运输',
  `main_business_freight_transport` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '主营货物运输',
  `certificate_validity_period` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '证件有效期',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_上海市国内水路运输经营名录';

-- gkx.ods_hycy_ship_management_enterprise_trustee_ship definition

CREATE TABLE `ods_hycy_ship_management_enterprise_trustee_ship` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：企业名称+代管类型，连接字符：-，md5',
  `province_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `province_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业名称',
  `trustee_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '代管类型',
  `is_water_transport_qualification` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '是否同时具有水路运输经营资格',
  `is_international_ship_management` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '是否兼营国际船舶管理',
  `is_domestic_ship_management` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '是否兼营国内船舶管理',
  `trustee_ship_count` int DEFAULT NULL COMMENT '代管船舶数量',
  `total_tonnage` decimal(18,2) DEFAULT NULL COMMENT '总吨合计',
  `business_scope` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '经营范围',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_船舶管理企业代管船舶表';

-- gkx.ods_hycy_shipping_capacity definition

CREATE TABLE `ods_hycy_shipping_capacity` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：统计类型+统计时间+更新频次+企业名称+船舶类型，连接字符：-，md5',
  `province_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `province_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联【公共码表.行政区域代码表】',
  `statistical_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统计类型',
  `enterprise_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业名称',
  `enterprise_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '企业类型',
  `vessel_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '船舶类型',
  `vessels` int NOT NULL DEFAULT '0' COMMENT '船舶总数',
  `hong_kong_macao_vessels` int NOT NULL DEFAULT '0' COMMENT '港澳通航船舶数量',
  `inland_vessels` int NOT NULL DEFAULT '0' COMMENT '内陆通航船舶数量',
  `international_vessels` int NOT NULL DEFAULT '0' COMMENT '国际通航船舶数量',
  `passenger_capacity` int NOT NULL DEFAULT '0' COMMENT '客位数',
  `gross_tonnage` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT '总吨数',
  `deadweight_tonnage` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT '载重吨',
  `teu_capacity` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT 'TEU',
  `cubic_meter_capacity` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT '立方米',
  `car_capacity` int NOT NULL DEFAULT '0' COMMENT '车位',
  `statistical_date` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '统计时间',
  `update_frequency` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '更新频次',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_航运运力表';

-- gkx.ods_hycy_submarine_cable_distribution definition

CREATE TABLE `ods_hycy_submarine_cable_distribution` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：类别+区域，连接字符：-，md5',
  `category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '类别',
  `region` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '区域',
  `submarine_cable` int DEFAULT NULL COMMENT '海底光缆条数',
  `connection_point` int DEFAULT NULL COMMENT '链接点个数',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_海底光缆分布';

-- gkx.ods_hycy_sz_maritime_law_attorneys definition

CREATE TABLE `ods_hycy_sz_maritime_law_attorneys` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键规则：年份+姓名+所属律师事务所+执业证号，连接字符：-，md5',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '年份',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '姓名',
  `gender` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '性别',
  `region` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '区域',
  `law_firm` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '所属律师事务所',
  `licensed_category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '执业类别',
  `licensed_no` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '执业证号',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='海洋产业_深圳海事海商律所及执业律师';

-- gkx.ods_industry_analysis_news definition

CREATE TABLE `ods_industry_analysis_news` (
  `id` int DEFAULT NULL COMMENT '唯一标识',
  `format` varchar(10) DEFAULT NULL COMMENT '文件格式',
  `creation_date` varchar(50) DEFAULT NULL COMMENT '创建日期',
  `companies` text COMMENT '关联企业列表',
  `country_codes` varchar(500) DEFAULT NULL COMMENT '国家代码',
  `topics` text COMMENT '主题信息',
  `source_type_code` varchar(50) DEFAULT NULL COMMENT '数据源类型代码',
  `source_type_name` varchar(500) DEFAULT NULL COMMENT '数据源类型名称',
  `document_source_code` varchar(50) DEFAULT NULL COMMENT '数据源代码',
  `document_source_name` varchar(500) DEFAULT NULL COMMENT '数据源名称',
  `content_types` text COMMENT '内容类型',
  `industries` text COMMENT '涉及产业列表',
  `pages` int DEFAULT NULL COMMENT '页数',
  `title` varchar(1000) DEFAULT NULL COMMENT '标题',
  `abstract` text COMMENT '摘要',
  `language` varchar(50) DEFAULT NULL COMMENT '语言'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='行业分析-科技新闻';

-- gkx.ods_industry_code definition

CREATE TABLE `ods_industry_code` (
  `id` bigint DEFAULT NULL COMMENT 'id',
  `code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '环节编码',
  `name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '环节名称',
  `parent_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '父级编码',
  `industry_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业编码',
  `industry_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业名称',
  `level` int NOT NULL DEFAULT '0' COMMENT '级别',
  `definition` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '定义',
  `is_key_link` int NOT NULL DEFAULT '0' COMMENT '是否为关键环节',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='产业链';

-- gkx.ods_information definition

CREATE TABLE `ods_information` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '医疗资讯的内部或来源库唯一标识',
  `information_title` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '医疗资讯的标题',
  `information_time` date DEFAULT NULL COMMENT '医疗资讯正式发布的日期或时间',
  `information_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '医疗资讯正文或摘要内容',
  `information_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '医疗资讯来源页面的 URL',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='医疗资讯';

-- gkx.ods_job definition

CREATE TABLE `ods_job` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '招聘的内部或来源库唯一标识',
  `job_title` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '招聘岗位名称',
  `company_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '发布岗位的公司或机构名称',
  `job_description` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '岗位职责、任职要求或工作内容摘要',
  `job_url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '招聘岗位详情页 URL',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='招聘';

-- gkx.ods_market definition

CREATE TABLE `ods_market` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品市场对应的内部或来源库唯一标识',
  `market_name` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品市场对应的国家、地区、治疗领域或细分市场名称',
  `market_share` decimal(18,6) NOT NULL DEFAULT '0.000000' COMMENT '目标药品、品类或仿制药在指定市场中的占比',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='药品市场表';

-- gkx.ods_material_virtual_structure definition

CREATE TABLE `ods_material_virtual_structure` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '材料虚拟结构的内部或来源库唯一标识',
  `material_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '材料或晶体结构的名称',
  `formula` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '材料的化学组成式',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='材料虚拟结构';

-- gkx.ods_medical_device definition

CREATE TABLE `ods_medical_device` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '医疗器械记录的唯一标识或来源库编码',
  `device_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '医疗器械产品名称',
  `device_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '医疗器械的类别、用途或产品类型',
  `device_id_issuing_agency` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '器械标识或编码的发行机构',
  `brand_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '医疗器械或产品使用的品牌名称',
  `company_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '医疗器械生产企业或注册企业名称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_medical_device_device_name` (`device_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='医疗器械表';

-- gkx.ods_molecular_spectrum definition

CREATE TABLE `ods_molecular_spectrum` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '唯一标识',
  `substance_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联到物质信息表的物质ID，用于将谱图归属到具体物质',
  `en_name` varchar(4000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '化合物、材料或分子的标准英文名称',
  `formula` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分子、化合物或晶体的化学组成式',
  `ms_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '质谱数据级别，如 MS1 或 MS2',
  `ion_mode` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '质谱采集的离子极性模式，如正离子或负离子',
  `ionization` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '质谱电离方法，如 ESI、APCI、EI 等',
  `collision_energy` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'MS/MS 碎裂过程使用的碰撞能设置',
  `precursor_mz` decimal(18,6) DEFAULT NULL COMMENT 'MS/MS 采集时被选择碎裂的前体离子 m/z',
  `precursor_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '前体离子的加合物或离子形式',
  `peaks` json DEFAULT NULL COMMENT '谱图峰数据列表，通常包含 m/z、强度和相对强度',
  `mass_to_charge_ratio` json DEFAULT NULL COMMENT '谱峰或离子的 m/z 数值',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_molecular_spectrum_substance_id` (`substance_id`) USING BTREE,
  KEY `idx_ods_molecular_spectrum_en_name` (`en_name`(191)) USING BTREE,
  KEY `idx_ods_molecular_spectrum_formula` (`formula`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='分子谱图';

-- gkx.ods_multi_omics definition

CREATE TABLE `ods_multi_omics` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '多组学数据的内部或来源库唯一标识',
  `data_category` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '多组学数据的大类，如突变、表达、甲基化、蛋白组等',
  `data_type` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '多组学数据的细分类型或文件类型',
  `repository` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '多组学数据来源平台或数据库名称',
  `experimental_strategy` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '产生该组学数据的实验或测序策略',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='多组学表';

-- gkx.ods_news_base definition

CREATE TABLE `ods_news_base` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `yqwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '舆情唯一键',
  `fbsj` date DEFAULT NULL COMMENT '发布时间',
  `lymc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '来源名称',
  `lx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '类型',
  `bt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标题',
  `lylj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '来源链接',
  `zy` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '摘要',
  `xgqyxx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '相关企业信息',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_news_base_yqwyj` (`yqwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='舆情表';

-- gkx.ods_org_annual_report_asset definition

CREATE TABLE `ods_org_annual_report_asset` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `ztwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主体唯一键',
  `nbnf` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '年报年份',
  `zcze` int DEFAULT NULL COMMENT '资产总额',
  `syzqyhj` int DEFAULT NULL COMMENT '所有者权益合计',
  `xsze` int DEFAULT NULL COMMENT '销售总额(营业总收入)',
  `lrze` int DEFAULT NULL COMMENT '利润总额',
  `zyywsr` int DEFAULT NULL COMMENT '主营业务收入',
  `jlr` int DEFAULT NULL COMMENT '净利润',
  `nsze` int DEFAULT NULL COMMENT '纳税总额',
  `fzze` int DEFAULT NULL COMMENT '负债总额',
  `hdzffczjbz` int DEFAULT NULL COMMENT '获得政府扶持资金、补助',
  `jrdk` int DEFAULT NULL COMMENT '金融贷款',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_annual_report_asset_ztwyj_nbnf` (`ztwyj`,`nbnf`) USING BTREE,
  KEY `idx_ods_org_annual_report_asset_ztwyj` (`ztwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='企业年报资产信息';

-- gkx.ods_org_annual_report_base definition

CREATE TABLE `ods_org_annual_report_base` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `ztwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主体唯一键',
  `tyshxydm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `ztmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '主体名称',
  `zch` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '注册号',
  `nbnf` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '年报年份',
  `jyzmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '经营者名称',
  `jyzt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '经营状态',
  `txdz` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '通讯地址',
  `qyzyywhd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '企业主营业务活动',
  `lxdh` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '联系电话',
  `lxyx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '联系邮箱',
  `yzbm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '邮政编码',
  `cyers` int DEFAULT NULL COMMENT '从业人数',
  `nxcyrs` int DEFAULT NULL COMMENT '女性从业人数',
  `cyrs` int DEFAULT NULL COMMENT '成员人数',
  `cyrsznmrs` int DEFAULT NULL COMMENT '成员人数中农民人数',
  `bndxzcyrs` int DEFAULT NULL COMMENT '本年度新增成员人数',
  `bndtccyrs` int DEFAULT NULL COMMENT '本年度退出成员人数',
  `qykgqk` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '企业控股情况',
  `sfytzhgmqtgsgq` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否有投资或购买其他公司股权',
  `sfydwtgdbxx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否有对外提供担保信息',
  `yxzrgsbndsffsgqzr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '有限责任公司本年度是否发生股权转让',
  `csqymc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '从属企业名称',
  `sfywzhwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '是否有网站或网点',
  `nbtbsj` date DEFAULT NULL COMMENT '年报填报时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_annual_report_base_ztwyj_nbnf` (`ztwyj`,`nbnf`) USING BTREE,
  KEY `idx_ods_org_annual_report_base_ztwyj` (`ztwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='年报基本信息';

-- gkx.ods_org_balance_sheet definition

CREATE TABLE `ods_org_balance_sheet` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `ztmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '主体名称',
  `ztwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主体唯一键',
  `gsjc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公司简称',
  `zzjgdm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '组织机构代码',
  `fbrq` date DEFAULT NULL COMMENT '发布日期',
  `jzrq` date DEFAULT NULL COMMENT '截止日期',
  `bblx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '报表类型',
  `hjnd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '会计年度',
  `bgqlx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '报告期类型',
  `sjzt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '审计状态',
  `bz` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '币种',
  `hbzj` int DEFAULT NULL COMMENT '货币资金',
  `jsbfj` int DEFAULT NULL COMMENT '结算备付金',
  `cczj` int DEFAULT NULL COMMENT '拆出资金',
  `jyxjrzc` int DEFAULT NULL COMMENT '交易性金融资产',
  `ysjrzc` int DEFAULT NULL COMMENT '衍生金融资产',
  `yspj` int DEFAULT NULL COMMENT '应收票据',
  `yszk` int DEFAULT NULL COMMENT '应收账款',
  `yfkx` int DEFAULT NULL COMMENT '预付款项',
  `ysbf` int DEFAULT NULL COMMENT '应收保费',
  `ysfbzk` int DEFAULT NULL COMMENT '应收分保账款',
  `ysfbhtzbj` int DEFAULT NULL COMMENT '应收分保合同准备金',
  `yslx` int DEFAULT NULL COMMENT '应收利息',
  `ysgl` int DEFAULT NULL COMMENT '应收股利',
  `qtysk` int DEFAULT NULL COMMENT '其他应收款',
  `ysckts` int DEFAULT NULL COMMENT '应收出口退税',
  `ysbtk` int DEFAULT NULL COMMENT '应收补贴款',
  `ysbzj` int DEFAULT NULL COMMENT '应收保证金',
  `nbysk` int DEFAULT NULL COMMENT '内部应收款',
  `mrfsjrzc` int DEFAULT NULL COMMENT '买入返售金融资产',
  `ch` int DEFAULT NULL COMMENT '存货',
  `hfwcydsdzc` int DEFAULT NULL COMMENT '划分为持有待售的资产',
  `dtfy` int DEFAULT NULL COMMENT '待摊费用',
  `dclldzcsy` int DEFAULT NULL COMMENT '待处理流动资产损益',
  `ynndqdfldzc` int DEFAULT NULL COMMENT '一年内到期的非流动资产',
  `qtldzc` int DEFAULT NULL COMMENT '其他流动资产',
  `ldzchj` int DEFAULT NULL COMMENT '流动资产合计',
  `ffdkjdk` int DEFAULT NULL COMMENT '发放贷款及垫款',
  `kgcsjrzc` int DEFAULT NULL COMMENT '可供出售金融资产',
  `zqtz` int DEFAULT NULL COMMENT '债权投资',
  `zqysk` int DEFAULT NULL COMMENT '长期应收款',
  `zqgqtz` int DEFAULT NULL COMMENT '长期股权投资',
  `qtcqtz` int DEFAULT NULL COMMENT '其他长期投资',
  `tzxfdc` int DEFAULT NULL COMMENT '投资性房地产',
  `gdzcyz` int DEFAULT NULL COMMENT '固定资产原值',
  `ljzj` int DEFAULT NULL COMMENT '累计折旧',
  `gdzcjz` int DEFAULT NULL COMMENT '固定资产净值',
  `gdzcjzzb` int DEFAULT NULL COMMENT '固定资产减值准备',
  `gdzcje` int DEFAULT NULL COMMENT '固定资产净额',
  `zjgc` int DEFAULT NULL COMMENT '在建工程',
  `gcwz` int DEFAULT NULL COMMENT '工程物资',
  `gdzcql` int DEFAULT NULL COMMENT '固定资产清理',
  `scxswzc` int DEFAULT NULL COMMENT '生产性生物资产',
  `gyxswzc` int DEFAULT NULL COMMENT '公益性生物资产',
  `yqzc` int DEFAULT NULL COMMENT '油气资产',
  `wxzc` int DEFAULT NULL COMMENT '无形资产',
  `kfzc` int DEFAULT NULL COMMENT '开发支出',
  `sy` int DEFAULT NULL COMMENT '商誉',
  `zqdtfy` int DEFAULT NULL COMMENT '长期待摊费用',
  `gqfzltq` int DEFAULT NULL COMMENT '股权分置流通权',
  `dysdszc` int DEFAULT NULL COMMENT '递延所得税资产',
  `qtfldzc` int DEFAULT NULL COMMENT '其他非流动资产',
  `fldzchj` int DEFAULT NULL COMMENT '非流动资产合计',
  `zczj` int DEFAULT NULL COMMENT '资产总计',
  `dqjk` int DEFAULT NULL COMMENT '短期借款',
  `xzyyxjk` int DEFAULT NULL COMMENT '向中央银行借款',
  `xsckjtycf` int DEFAULT NULL COMMENT '吸收存款及同业存放',
  `crzj` int DEFAULT NULL COMMENT '拆入资金',
  `jyxjrfz` int DEFAULT NULL COMMENT '交易性金融负债',
  `ysjrfz` int DEFAULT NULL COMMENT '衍生金融负债',
  `yfpj` int DEFAULT NULL COMMENT '应付票据',
  `yfzk` int DEFAULT NULL COMMENT '应付账款',
  `yskx` int DEFAULT NULL COMMENT '预收款项',
  `mchgjrzck` int DEFAULT NULL COMMENT '卖出回购金融资产款',
  `yfsxfjyj` int DEFAULT NULL COMMENT '应付手续费及佣金',
  `yfzgxc` int DEFAULT NULL COMMENT '应付职工薪酬',
  `yjsf` int DEFAULT NULL COMMENT '应交税费',
  `yflx` int DEFAULT NULL COMMENT '应付利息',
  `yfgl` int DEFAULT NULL COMMENT '应付股利',
  `qtyjk` int DEFAULT NULL COMMENT '其他应交款',
  `yfbzj` int DEFAULT NULL COMMENT '应付保证金',
  `nbyfk` int DEFAULT NULL COMMENT '内部应付款',
  `qtyfk` int DEFAULT NULL COMMENT '其他应付款',
  `ytfy` int DEFAULT NULL COMMENT '预提费用',
  `yjldfz` int DEFAULT NULL COMMENT '预计流动负债',
  `yffbzk` int DEFAULT NULL COMMENT '应付分保账款',
  `bxhtzbj` int DEFAULT NULL COMMENT '保险合同准备金',
  `dlmmzqk` int DEFAULT NULL COMMENT '代理买卖证券款',
  `dlcxzqk` int DEFAULT NULL COMMENT '代理承销证券款',
  `gjpzjs` int DEFAULT NULL COMMENT '国际票证结算',
  `gnpzjs` int DEFAULT NULL COMMENT '国内票证结算',
  `ynnddysy` int DEFAULT NULL COMMENT '一年内的递延收益',
  `yfdqzq` int DEFAULT NULL COMMENT '应付短期债券',
  `hfwcydsdfz` int DEFAULT NULL COMMENT '划分为持有待售的负债',
  `ynndqdfldfz` int DEFAULT NULL COMMENT '一年内到期的非流动负债',
  `qtldfz` int DEFAULT NULL COMMENT '其他流动负债',
  `ldfzhj` int DEFAULT NULL COMMENT '流动负债合计',
  `zqjk` int DEFAULT NULL COMMENT '长期借款',
  `zqyfzgxc` int DEFAULT NULL COMMENT '长期应付职工薪酬',
  `yfzq` int DEFAULT NULL COMMENT '应付债券',
  `yxg` int DEFAULT NULL COMMENT '优先股',
  `yxz` int DEFAULT NULL COMMENT '永续债',
  `zqyfk` int DEFAULT NULL COMMENT '长期应付款',
  `zxyfk` int DEFAULT NULL COMMENT '专项应付款',
  `yjfldfz` int DEFAULT NULL COMMENT '预计非流动负债',
  `zqdysy` int DEFAULT NULL COMMENT '长期递延收益',
  `dysdsfz` int DEFAULT NULL COMMENT '递延所得税负债',
  `qtfldfz` int DEFAULT NULL COMMENT '其他非流动负债',
  `fldfzhj` int DEFAULT NULL COMMENT '非流动负债合计',
  `fzhj` int DEFAULT NULL COMMENT '负债合计',
  `sszbhgb` int DEFAULT NULL COMMENT '实收资本(或股本)',
  `qtqygj` int DEFAULT NULL COMMENT '其他权益工具',
  `zbgj` int DEFAULT NULL COMMENT '资本公积',
  `kcg` int DEFAULT NULL COMMENT '库存股',
  `qtzhsy` int DEFAULT NULL COMMENT '其他综合收益',
  `zxcb` int DEFAULT NULL COMMENT '专项储备',
  `yygj` int DEFAULT NULL COMMENT '盈余公积',
  `ybfxzb` int DEFAULT NULL COMMENT '一般风险准备',
  `wqddtzss` int DEFAULT NULL COMMENT '未确定的投资损失',
  `wfplr` int DEFAULT NULL COMMENT '未分配利润',
  `nfpxjgl` int DEFAULT NULL COMMENT '拟分配现金股利',
  `wbbbzsce` int DEFAULT NULL COMMENT '外币报表折算差额',
  `gsymgsgdqyhj` int DEFAULT NULL COMMENT '归属于母公司股东权益合计',
  `ssgdqy` int DEFAULT NULL COMMENT '少数股东权益',
  `syzqyhgdqhj` int DEFAULT NULL COMMENT '所有者权益(或股东权益)合计',
  `fzhsyzqyhgdqyzj` int DEFAULT NULL COMMENT '负债和所有者权益(或股东权益)总计',
  `dbzrpczbj` int DEFAULT NULL COMMENT '担保责任赔偿准备金',
  `yspjjyszk` int DEFAULT NULL COMMENT '应收票据及应收账款',
  `htzc` int DEFAULT NULL COMMENT '合同资产',
  `qtzqtz` int DEFAULT NULL COMMENT '其他债权投资',
  `qtqygjtz` int DEFAULT NULL COMMENT '其他权益工具投资',
  `qtfldjrzc` int DEFAULT NULL COMMENT '其他非流动金融资产',
  `yfpjjyfzk` int DEFAULT NULL COMMENT '应付票据及应付账款',
  `htfz` int DEFAULT NULL COMMENT '合同负债',
  `ygyjzjlqqbdjrqtzhsydjrzc` int DEFAULT NULL COMMENT '以公允价值计量且其变动计入其他综合收益的金融资产',
  `ytycbjldjrzc` int DEFAULT NULL COMMENT '以摊余成本计量的金融资产',
  `qtyskhj` int DEFAULT NULL COMMENT '其他应收款合计',
  `qtyfkhj` int DEFAULT NULL COMMENT '其他应付款合计',
  `gdzcjqlhj` int DEFAULT NULL COMMENT '固定资产及清理合计',
  `zjgchj` int DEFAULT NULL COMMENT '在建工程合计',
  `zqyfkhj` int DEFAULT NULL COMMENT '长期应付款合计',
  `yskxrz` int DEFAULT NULL COMMENT '应收款项融资',
  `syqzc` int DEFAULT NULL COMMENT '使用权资产',
  `zlfz` int DEFAULT NULL COMMENT '租赁负债',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_balance_sheet_ztwyj` (`ztwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='资产负债表';

-- gkx.ods_org_base_info definition

CREATE TABLE `ods_org_base_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `ztwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主体唯一键',
  `tyshxydm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '统一社会信用代码',
  `ztmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '主体名称',
  `bzztmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标准主体名称',
  `fddbr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法定代表人',
  `frtx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法人头衔',
  `djzt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '登记状态',
  `glhddjzt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '归类后的登记状态',
  `clrq` date DEFAULT NULL COMMENT '成立日期',
  `lx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '类型',
  `glhdztlx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '归类后的主体类型',
  `zczb` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '注册资本',
  `bz` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '币种',
  `jyqxz` date DEFAULT NULL COMMENT '经营期限自',
  `jyqxzh` date DEFAULT NULL COMMENT '经营期限至',
  `djdz` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '登记地址',
  `jyfw` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '经营范围',
  `hzrq` date DEFAULT NULL COMMENT '核准日期',
  `zch` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '注册号',
  `zzjgdm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '组织机构代码',
  `ywmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '英文名称',
  `djjg` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '登记机关',
  `sjzb` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '实缴资本',
  `sfjc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '省份简称',
  `sf` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '省份',
  `shjxzqhdm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '省级行政区划代码',
  `cs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '城市',
  `sjxzqhdm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '市级行政区划代码',
  `qx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '区县',
  `xjxzqhdm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '县级行政区划代码',
  `jwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '经纬度',
  `bdjwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '百度经纬度',
  `zxrq` date DEFAULT NULL COMMENT '注销日期',
  `zxyy` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '注销原因',
  `dxrq` date DEFAULT NULL COMMENT '吊销日期',
  `sszt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '上市状态',
  `sszqlx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '上市证券类型',
  `ssdm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '上市代码',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_base_info_ztwyj` (`ztwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内机构基本信息';

-- gkx.ods_org_bid_base definition

CREATE TABLE `ods_org_bid_base` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `wyzjid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '唯一主键id',
  `zhbdw` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '招标单位',
  `gglx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公告类型',
  `ggzlx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公告子类型',
  `ggbt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公告标题',
  `xmbh` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目编号',
  `zbje` int DEFAULT NULL COMMENT '招标金额 （为0 表示 空）',
  `fbsj` date DEFAULT NULL COMMENT '发布时间',
  `sf` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '省份',
  `cs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '城市',
  `cgfs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '采购方式',
  `zbbdw` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '招标标的物',
  `ztbxy` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '招投标行业',
  `zbdljg` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '招标代理机构',
  `zbdw` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '中标单位',
  `zjxz` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '专家小组',
  `kbsj` date DEFAULT NULL COMMENT '开标时间',
  `hqbsjzrq` date DEFAULT NULL COMMENT '获取标书截止日期',
  `tbjzrq` date DEFAULT NULL COMMENT '投标截止日期',
  `sybs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标识，0有效，10废弃删除',
  `bgsj` date DEFAULT NULL COMMENT '变更时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_bid_base_wyzjid` (`wyzjid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='招投标基本信息';

-- gkx.ods_org_bid_notice definition

CREATE TABLE `ods_org_bid_notice` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `wyzjid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '唯一主键id',
  `ggzwnr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公告正文内容',
  `zwxxcclj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '正文信息存储路径',
  `wzlj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '网站链接',
  `sybs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标识，0有效，10废弃删除',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_bid_notice_wyzjid` (`wyzjid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='招投标公告内容';

-- gkx.ods_org_bid_relation definition

CREATE TABLE `ods_org_bid_relation` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `wyzjid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '唯一主键id',
  `xgfztglwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '相关方主体关联唯一键',
  `xgfmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '相关方名称',
  `xglx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '相关类型，0：采购人，1：代理机构，2：中标单位，3：参与方',
  `xgftyshxydm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '相关方统一社会信用代码',
  `zbje` int DEFAULT NULL COMMENT '中标金额',
  `xgflxr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '相关方联系人',
  `xgflxfs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '相关方联系方式',
  `xgflxdz` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '相关方联系地址',
  `sybs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标识，0有效，10废弃删除',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_bid_relation_wyzjid` (`wyzjid`) USING BTREE,
  KEY `idx_ods_org_bid_relation_xgfztglwyj` (`xgfztglwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='招投标相关方';

-- gkx.ods_org_cashflow_statement definition

CREATE TABLE `ods_org_cashflow_statement` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `ztmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '主体名称',
  `ztwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主体唯一键',
  `gsjc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公司简称',
  `zzjgdm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '组织机构代码',
  `fbrq` date DEFAULT NULL COMMENT '发布日期',
  `bbqsrq` date DEFAULT NULL COMMENT '报表起始日期',
  `jzrq` date DEFAULT NULL COMMENT '截止日期',
  `bblx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '报表类型',
  `hjnd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '会计年度',
  `bgqlx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '报告期类型',
  `sjzt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '审计状态',
  `bz` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '币种',
  `xssptglwsddxj` int DEFAULT NULL COMMENT '销售商品、提供劳务收到的现金',
  `khckhtycfkxjzje` int DEFAULT NULL COMMENT '客户存款和同业存放款项净增加额',
  `xzyyxjkjzje` int DEFAULT NULL COMMENT '向中央银行借款净增加额',
  `xqtjrjgcrzjjzje` int DEFAULT NULL COMMENT '向其他金融机构拆入资金净增加额',
  `sdybxhtbfqddxj` int DEFAULT NULL COMMENT '收到原保险合同保费取得的现金',
  `sdzbxywxjje` int DEFAULT NULL COMMENT '收到再保险业务现金净额',
  `bhcjjtzkjzje` int DEFAULT NULL COMMENT '保户储金及投资款净增加额',
  `czjyxjrzcjzje` int DEFAULT NULL COMMENT '处置交易性金融资产净增加额',
  `sqlxsxfjyjdxj` int DEFAULT NULL COMMENT '收取利息、手续费及佣金的现金',
  `crzjjzje` int DEFAULT NULL COMMENT '拆入资金净增加额',
  `hgywzjjzje` int DEFAULT NULL COMMENT '回购业务资金净增加额',
  `sddsffh` int DEFAULT NULL COMMENT '收到的税费返还',
  `sddqtyjyhdygdxj` int DEFAULT NULL COMMENT '收到的其他与经营活动有关的现金',
  `jyhdxjlrxj` int DEFAULT NULL COMMENT '经营活动现金流入小计',
  `gmspjslwzfdxj` int DEFAULT NULL COMMENT '购买商品、接受劳务支付的现金',
  `khdkjdkjzje` int DEFAULT NULL COMMENT '客户贷款及垫款净增加额',
  `cfzyyxhtykxjzje` int DEFAULT NULL COMMENT '存放中央银行和同业款项净增加额',
  `zfybxhtpfkxdxj` int DEFAULT NULL COMMENT '支付原保险合同赔付款项的现金',
  `zflxsxfjyjdxj` int DEFAULT NULL COMMENT '支付利息、手续费及佣金的现金',
  `zfbdhldxj` int DEFAULT NULL COMMENT '支付保单红利的现金',
  `zfgzgyjwzgzfdxj` int DEFAULT NULL COMMENT '支付给职工以及为职工支付的现金',
  `zfdgxsf` int DEFAULT NULL COMMENT '支付的各项税费',
  `zfdqtyjyhdygdxj` int DEFAULT NULL COMMENT '支付的其他与经营活动有关的现金',
  `jyhdxjlcxj` int DEFAULT NULL COMMENT '经营活动现金流出小计',
  `jyhdcsdxjllje` int DEFAULT NULL COMMENT '经营活动产生的现金流量净额',
  `shtzssddxj` int DEFAULT NULL COMMENT '收回投资所收到的现金',
  `qdtzsysddxj` int DEFAULT NULL COMMENT '取得投资收益收到的现金',
  `czgdzcwxzchqtzqzcsshdxjje` int DEFAULT NULL COMMENT '处置固定资产、无形资产和其他长期资产所收回的现金净额',
  `czzgsjqtyydwsddxjje` int DEFAULT NULL COMMENT '处置子公司及其他营业单位收到的现金净额',
  `sddqtytzhdygdxj` int DEFAULT NULL COMMENT '收到的其他与投资活动有关的现金',
  `jszyhdqckssddxj` int DEFAULT NULL COMMENT '减少质押和定期存款所收到的现金',
  `tzhdxjlrxj` int DEFAULT NULL COMMENT '投资活动现金流入小计',
  `gjgdzcwxzchqtzqzcszfdxj` int DEFAULT NULL COMMENT '购建固定资产、无形资产和其他长期资产所支付的现金',
  `tzszfdxj` int DEFAULT NULL COMMENT '投资所支付的现金',
  `zydkjzje` int DEFAULT NULL COMMENT '质押贷款净增加额',
  `qdzgsjqtyydwzfdxjje` int DEFAULT NULL COMMENT '取得子公司及其他营业单位支付的现金净额',
  `zfdqtytzhdygdxj` int DEFAULT NULL COMMENT '支付的其他与投资活动有关的现金',
  `zjzyhdqckszfdxj` int DEFAULT NULL COMMENT '增加质押和定期存款所支付的现金',
  `tzhdxjlcxj` int DEFAULT NULL COMMENT '投资活动现金流出小计',
  `tzhdcsdxjllje` int DEFAULT NULL COMMENT '投资活动产生的现金流量净额',
  `xstzsddxj` int DEFAULT NULL COMMENT '吸收投资收到的现金',
  `qdjksddxj` int DEFAULT NULL COMMENT '取得借款收到的现金',
  `fxzqsddxj` int DEFAULT NULL COMMENT '发行债券收到的现金',
  `sdqtyczhdygdxj` int DEFAULT NULL COMMENT '收到其他与筹资活动有关的现金',
  `czhdxjlrxj` int DEFAULT NULL COMMENT '筹资活动现金流入小计',
  `chzwzfdxj` int DEFAULT NULL COMMENT '偿还债务支付的现金',
  `zfqtyczhdygdxj` int DEFAULT NULL COMMENT '支付其他与筹资活动有关的现金',
  `czhdxjlcxj` int DEFAULT NULL COMMENT '筹资活动现金流出小计',
  `czhdcsdxjllje` int DEFAULT NULL COMMENT '筹资活动产生的现金流量净额',
  `hlbddxjjxjdjwdyx` int DEFAULT NULL COMMENT '汇率变动对现金及现金等价物的影响',
  `xjjxjdjwjzje` int DEFAULT NULL COMMENT '现金及现金等价物净增加额',
  `qcxjjxjdjwye` int DEFAULT NULL COMMENT '期初现金及现金等价物余额',
  `qmxjjxjdjwye` int DEFAULT NULL COMMENT '期末现金及现金等价物余额',
  `jlr` int DEFAULT NULL COMMENT '净利润',
  `ssgdqy` int DEFAULT NULL COMMENT '少数股东权益',
  `wqrdtzss` int DEFAULT NULL COMMENT '未确认的投资损失',
  `zcjzzb` int DEFAULT NULL COMMENT '资产减值准备',
  `gdzczjyqzczhscxwzzj` int DEFAULT NULL COMMENT '固定资产折旧、油气资产折耗、生产性物资折旧',
  `tzxfdczjtx` int DEFAULT NULL COMMENT '投资性房地产折旧、摊销',
  `wxzctx` int DEFAULT NULL COMMENT '无形资产摊销',
  `zqdtfytx` int DEFAULT NULL COMMENT '长期待摊费用摊销',
  `dtfydjs` int DEFAULT NULL COMMENT '待摊费用的减少',
  `ytfydzj` int DEFAULT NULL COMMENT '预提费用的增加',
  `czgdzcwxzchqtzqzcdss` int DEFAULT NULL COMMENT '处置固定资产、无形资产和其他长期资产的损失',
  `gdzcbfss` int DEFAULT NULL COMMENT '固定资产报废损失',
  `gyjzbdss` int DEFAULT NULL COMMENT '公允价值变动损失',
  `dysyzj` int DEFAULT NULL COMMENT '递延收益增加',
  `yjfz` int DEFAULT NULL COMMENT '预计负债',
  `cwfy` int DEFAULT NULL COMMENT '财务费用',
  `tzss` int DEFAULT NULL COMMENT '投资损失',
  `dysdszcjs` int DEFAULT NULL COMMENT '递延所得税资产减少',
  `dysdsfzzj` int DEFAULT NULL COMMENT '递延所得税负债增加',
  `chdjs` int DEFAULT NULL COMMENT '存货的减少',
  `jyxysxmdjs` int DEFAULT NULL COMMENT '经营性应收项目的减少',
  `jyxyfxmdzj` int DEFAULT NULL COMMENT '经营性应付项目的增加',
  `qt` int DEFAULT NULL COMMENT '其他',
  `jyhdcsxjllje` int DEFAULT NULL COMMENT '经营活动产生现金流量净额',
  `zwzwzb` int DEFAULT NULL COMMENT '债务转为资本',
  `ynndqdkzhgszq` int DEFAULT NULL COMMENT '一年内到期的可转换公司债券',
  `rzzrgdzc` int DEFAULT NULL COMMENT '融资租入固定资产',
  `xjdqmye` int DEFAULT NULL COMMENT '现金的期末余额',
  `xjdqcye` int DEFAULT NULL COMMENT '现金的期初余额',
  `xjdjwdqmye` int DEFAULT NULL COMMENT '现金等价物的期末余额',
  `xjdjwdqcye` int DEFAULT NULL COMMENT '现金等价物的期初余额',
  `xjjxjdjwdjzje` int DEFAULT NULL COMMENT '现金及现金等价物的净增加额',
  `xyjzss` int DEFAULT NULL COMMENT '信用减值损失(附表)',
  `czkgcsjrzcjzje` int DEFAULT NULL COMMENT '处置可供出售金融资产净增加额(投资流入)',
  `syqzczj` int DEFAULT NULL COMMENT '使用权资产折旧',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_cashflow_statement_ztwyj` (`ztwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='现金流量表';

-- gkx.ods_org_change definition

CREATE TABLE `ods_org_change` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `ztwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主体唯一键',
  `bgrq` date DEFAULT NULL COMMENT '变更日期',
  `bglx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '变更类型',
  `bgsx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '变更事项',
  `bgqnr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '变更前内容',
  `bghnr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '变更后内容',
  `bgjl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '变更记录',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_change_ztwyj` (`ztwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='工商变更表';

-- gkx.ods_org_employee definition

CREATE TABLE `ods_org_employee` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `ztwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主体唯一键',
  `yszyrymc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '原始主要人员名称',
  `zyry` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '主要人员（清洗后）',
  `zw` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '职位',
  `zyryrzzt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '主要人员任职状态',
  `zyryrzksrq` date DEFAULT NULL COMMENT '主要人员任职开始日期',
  `zyryrzjzrq` date DEFAULT NULL COMMENT '主要人员任职截止日期',
  `fddbrlx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法定代表人类型',
  `zyryly` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '主要人员来源',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_employee_ztwyj` (`ztwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='主要人员';

-- gkx.ods_org_employment definition

CREATE TABLE `ods_org_employment` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `gsmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公司名称',
  `ztwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主体唯一键',
  `zwmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '职位名称',
  `zwms` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '职位描述',
  `rzyq` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '任职要求',
  `dq` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '地区',
  `bgdz` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '办公地址',
  `xsqj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '薪水区间',
  `fldy` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '福利待遇',
  `gzjy` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '工作经验',
  `jycd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '教育程度',
  `zprs` int DEFAULT NULL COMMENT '招聘人数',
  `lyzddm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '来源站点代码',
  `zwlj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '职位链接',
  `fbsj` date DEFAULT NULL COMMENT '发布时间',
  `hrsczxsj` date DEFAULT NULL COMMENT 'HR上次在线时间',
  `zwszsh` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '职位所在省',
  `zwszs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '职位所在市',
  `zwszq` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '职位所在区',
  `sybs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '使用标识（0有效，10废弃删除）',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_employment_ztwyj` (`ztwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='招聘信息表';

-- gkx.ods_org_financing definition

CREATE TABLE `ods_org_financing` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `gsm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公司名',
  `rzrq` date DEFAULT NULL COMMENT '融资日期',
  `lc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '轮次',
  `bzhhdcylc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标准化后的参与轮次',
  `tzje` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '投资金额',
  `tzjeg` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '投资金额(估)',
  `thgz` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '投后估值',
  `bz` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '币种',
  `bltzrjg` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '本轮投资人（机构）',
  `bltzrjgid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '本轮投资人（机构）id',
  `bdrq` date DEFAULT NULL COMMENT '报道日期',
  `xwbt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '新闻标题',
  `xwurl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '新闻url',
  `rzjlwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '融资记录唯一键',
  `dyztwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '对应主体唯一键',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_financing_rzjlwyj_dyztwyj` (`rzjlwyj`,`dyztwyj`) USING BTREE,
  KEY `idx_ods_org_financing_rzjlwyj` (`rzjlwyj`) USING BTREE,
  KEY `idx_ods_org_financing_dyztwyj` (`dyztwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='企业融资';

-- gkx.ods_org_income_statement definition

CREATE TABLE `ods_org_income_statement` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `ztmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '主体名称',
  `ztwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主体唯一键',
  `gsjc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公司简称',
  `zzjgdm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '组织机构代码',
  `fbrq` date DEFAULT NULL COMMENT '发布日期',
  `bbqsrq` date DEFAULT NULL COMMENT '报表起始日期',
  `jzrq` date DEFAULT NULL COMMENT '截止日期',
  `bblx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '报表类型',
  `hjnd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '会计年度',
  `bgqlx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '报告期类型',
  `sjzt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '审计状态',
  `bz` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '币种',
  `yyzsr` int DEFAULT NULL COMMENT '营业总收入',
  `yysr` int DEFAULT NULL COMMENT '营业收入',
  `lxsr` int DEFAULT NULL COMMENT '利息收入',
  `yzbf` int DEFAULT NULL COMMENT '已赚保费',
  `sxfjyjsr` int DEFAULT NULL COMMENT '手续费及佣金收入',
  `fdcxssr` int DEFAULT NULL COMMENT '房地产销售收入',
  `qtywsr` int DEFAULT NULL COMMENT '其他业务收入',
  `yyzcb` int DEFAULT NULL COMMENT '营业总成本',
  `yycb` int DEFAULT NULL COMMENT '营业成本',
  `lxzc` int DEFAULT NULL COMMENT '利息支出',
  `sxfjyjzc` int DEFAULT NULL COMMENT '手续费及佣金支出',
  `fdcxscb` int DEFAULT NULL COMMENT '房地产销售成本',
  `yffy` int DEFAULT NULL COMMENT '研发费用',
  `tbj` int DEFAULT NULL COMMENT '退保金',
  `pfzcje` int DEFAULT NULL COMMENT '赔付支出净额',
  `tqbxhtzbjje` int DEFAULT NULL COMMENT '提取保险合同准备金净额',
  `bdhlzc` int DEFAULT NULL COMMENT '保单红利支出',
  `fbfy` int DEFAULT NULL COMMENT '分保费用',
  `qtywcb` int DEFAULT NULL COMMENT '其他业务成本',
  `yysjjfj` int DEFAULT NULL COMMENT '营业税金及附加',
  `xsfy` int DEFAULT NULL COMMENT '销售费用',
  `glfy` int DEFAULT NULL COMMENT '管理费用',
  `cwfy` int DEFAULT NULL COMMENT '财务费用',
  `zcjzss` int DEFAULT NULL COMMENT '资产减值损失',
  `gyjzbdsy` int DEFAULT NULL COMMENT '公允价值变动收益',
  `tzsy` int DEFAULT NULL COMMENT '投资收益',
  `hdsy` int DEFAULT NULL COMMENT '汇兑收益',
  `qhsy` int DEFAULT NULL COMMENT '期货损益',
  `tgsy` int DEFAULT NULL COMMENT '托管收益',
  `btsr` int DEFAULT NULL COMMENT '补贴收入',
  `qtywlr` int DEFAULT NULL COMMENT '其他业务利润',
  `yylr` int DEFAULT NULL COMMENT '营业利润',
  `yywsr` int DEFAULT NULL COMMENT '营业外收入',
  `yywzc` int DEFAULT NULL COMMENT '营业外支出',
  `fldzcczss` int DEFAULT NULL COMMENT '非流动资产处置损失',
  `lrze` int DEFAULT NULL COMMENT '利润总额',
  `sdsfy` int DEFAULT NULL COMMENT '所得税费用',
  `wqrtzss` int DEFAULT NULL COMMENT '未确认投资损失',
  `jlr` int DEFAULT NULL COMMENT '净利润',
  `gsymgssyzdjlr` int DEFAULT NULL COMMENT '归属于母公司所有者的净利润',
  `bhbfzhbqsxjlr` int DEFAULT NULL COMMENT '被合并方在合并前实现净利润',
  `ssgdsy` int DEFAULT NULL COMMENT '少数股东损益',
  `jbmgsy` int DEFAULT NULL COMMENT '基本每股收益',
  `xsmgsy` int DEFAULT NULL COMMENT '稀释每股收益',
  `qtzhsy` int DEFAULT NULL COMMENT '其他综合收益',
  `gsymgssyzdqtzhsy` int DEFAULT NULL COMMENT '归属于母公司所有者的其他综合收益',
  `gsyssgddqtzhsy` int DEFAULT NULL COMMENT '归属于少数股东的其他综合收益',
  `zhsyze` int DEFAULT NULL COMMENT '综合收益总额',
  `gsymgssyzdzhsyze` int DEFAULT NULL COMMENT '归属于母公司所有者的综合收益总额',
  `gsyssgddzhsyze` int DEFAULT NULL COMMENT '归属于少数股东的综合收益总额',
  `zyywsr` int DEFAULT NULL COMMENT '主营业务收入',
  `zyywcb` int DEFAULT NULL COMMENT '主营业务成本',
  `ncwfplr` int DEFAULT NULL COMMENT '年初未分配利润',
  `jszczbjsdwfplr` int DEFAULT NULL COMMENT '减少注册资本减少的未分配利润',
  `qtysdz` int DEFAULT NULL COMMENT '其他因素调整',
  `kgfpdlr` int DEFAULT NULL COMMENT '可供分配的利润',
  `tqfdyygj` int DEFAULT NULL COMMENT '提取法定盈余公积',
  `tqfdgyj` int DEFAULT NULL COMMENT '提取法定公益金',
  `tqzbgjj` int DEFAULT NULL COMMENT '提取资本公积金',
  `tqzgjfjj` int DEFAULT NULL COMMENT '提取职工奖福基金',
  `tqcbjj` int DEFAULT NULL COMMENT '提取储备基金',
  `tqqyfzjj` int DEFAULT NULL COMMENT '提取企业发展基金',
  `lrghtz` int DEFAULT NULL COMMENT '利润归还投资',
  `bcldzb` int DEFAULT NULL COMMENT '补充流动资本',
  `kggdfpdlr` int DEFAULT NULL COMMENT '可供股东分配的利润',
  `yfyxggl` int DEFAULT NULL COMMENT '应付优先股股利',
  `tqryyygj` int DEFAULT NULL COMMENT '提取任意盈余公积',
  `yfptggl` int DEFAULT NULL COMMENT '应付普通股股利',
  `zzzbgbdptggl` int DEFAULT NULL COMMENT '转作资本股本的普通股股利',
  `wfplr` int DEFAULT NULL COMMENT '未分配利润',
  `fldzcczld` int DEFAULT NULL COMMENT '非流动资产处置利得',
  `yhbnzfljsydqtzhsy` int DEFAULT NULL COMMENT '以后不能重分类进损益的其他综合收益',
  `zxjlsdsyjhjfzhjzcdbd` int DEFAULT NULL COMMENT '重新计量设定受益计划净负债或净资产的变动',
  `qyfxzbtzdwbnzfljsydqtzhsyzxydfe` int DEFAULT NULL COMMENT '权益法下在被投资单位不能重分类进损益的其他综合收益中享有的份额',
  `yhjzfljsydqtzhsy` int DEFAULT NULL COMMENT '以后将重分类进损益的其他综合收益',
  `qyfxzbtzdwyhjzfljsydqtzhsyzxydfe` int DEFAULT NULL COMMENT '权益法下在被投资单位以后将重分类进损益的其他综合收益中享有的份额',
  `kgcsjrzcgyjzbdsy` int DEFAULT NULL COMMENT '可供出售金融资产公允价值变动损益',
  `cyzdqtzzflwkgcsjrzcsy` int DEFAULT NULL COMMENT '持有至到期投资重分类为可供出售金融资产损益',
  `xjlltqsydyxbf` int DEFAULT NULL COMMENT '现金流量套期损益的有效部分',
  `wbcwbbzsce` int DEFAULT NULL COMMENT '外币财务报表折算差额',
  `qt` int DEFAULT NULL COMMENT '其他',
  `zcczsy` int DEFAULT NULL COMMENT '资产处置收益',
  `qtsy` int DEFAULT NULL COMMENT '其他收益',
  `cxjyjlr` int DEFAULT NULL COMMENT '持续经营净利润',
  `zzjyjlr` int DEFAULT NULL COMMENT '终止经营净利润',
  `lxfy` int DEFAULT NULL COMMENT '利息费用',
  `lxsryycb` int DEFAULT NULL COMMENT '利息收入(营业成本)',
  `xyjzss` int DEFAULT NULL COMMENT '信用减值损失',
  `jcktqsy` int DEFAULT NULL COMMENT '净敞口套期收益',
  `qtqygjtzgyjzbd` int DEFAULT NULL COMMENT '其他权益工具投资公允价值变动',
  `qyzsxyfxgyjzbd` int DEFAULT NULL COMMENT '企业自身信用风险公允价值变动',
  `qtzqtzgyjzbd` int DEFAULT NULL COMMENT '其他债权投资公允价值变动',
  `jrzczfljrqtzhsydje` int DEFAULT NULL COMMENT '金融资产重分类计入其他综合收益的金额',
  `qtzqtzxyjzzb` int DEFAULT NULL COMMENT '其他债权投资信用减值准备',
  `qtgdfp` int DEFAULT NULL COMMENT '其他(股东分配)',
  `xjlltqcb` int DEFAULT NULL COMMENT '现金流量套期储备',
  `tqybfxzbkfplr` int DEFAULT NULL COMMENT '提取一般风险准备(可分配利润)',
  `ytycbjldjrzczzqrcsdsy` int DEFAULT NULL COMMENT '以摊余成本计量的金融资产终止确认产生的收益',
  `yfyxzlx` int DEFAULT NULL COMMENT '应付永续债利息',
  `zcjzssyylr` int DEFAULT NULL COMMENT '资产减值损失(营业利润)',
  `xyjzssyylr` int DEFAULT NULL COMMENT '信用减值损失(营业利润)',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_income_statement_ztwyj` (`ztwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='利润表';

-- gkx.ods_org_innovation definition

CREATE TABLE `ods_org_innovation` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `ztlx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '载体类型',
  `ztmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '载体名称',
  `ztjb` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '载体级别',
  `qtgjytyydw` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '牵头/共建/依托/运营单位',
  `rdpzdw` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '认定/批准单位',
  `rdjlnf` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '认定/建立年份',
  `ztszdq` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '载体所在地区',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='企业创新载体';

-- gkx.ods_org_news definition

CREATE TABLE `ods_org_news` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `ztwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主体唯一键',
  `yqwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '舆情唯一键',
  `gsqc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '公司全称',
  `gpdm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '股票代码',
  `qgsx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '情感属性',
  `qgzyd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '情感重要度',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_news_ztwyj_yqwyj` (`ztwyj`,`yqwyj`) USING BTREE,
  KEY `idx_ods_org_news_ztwyj` (`ztwyj`) USING BTREE,
  KEY `idx_ods_org_news_yqwyj` (`yqwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='企业舆情信息';

-- gkx.ods_org_shareholder definition

CREATE TABLE `ods_org_shareholder` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `ztwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主体唯一键',
  `gdssgsmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '股东所属公司名称',
  `ysgdmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '原始股东名称',
  `qxhdgdmc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '清洗后的股东名称',
  `gdwyj` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '股东唯一键',
  `gdjrrq` date DEFAULT NULL COMMENT '股东进入日期',
  `gdtcrq` date DEFAULT NULL COMMENT '股东退出日期',
  `gdlx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '股东类型',
  `gdzjlx` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '股东证件类型',
  `gdzjhm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '股东证件号码',
  `yjcze` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '应缴出资额',
  `yjczesz` int DEFAULT NULL COMMENT '应缴出资额数值（量纲-万）',
  `rjczjl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '认缴出资记录',
  `czbl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '出资比例',
  `cgs` int DEFAULT NULL COMMENT '持股数',
  `sjcze` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '实缴出资额',
  `sjczesz` int DEFAULT NULL COMMENT '实缴出资额数值',
  `sjczjl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '实缴出资记录',
  `gdly` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '股东来源',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_org_shareholder_gdwyj_ztwyj` (`gdwyj`,`ztwyj`) USING BTREE,
  KEY `idx_ods_org_shareholder_ztwyj` (`ztwyj`) USING BTREE,
  KEY `idx_ods_org_shareholder_gdwyj` (`gdwyj`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='股东信息';

-- gkx.ods_patent definition

CREATE TABLE `ods_patent` (
  `patent_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利记录唯一标识，与 DOCDB 兼容，用于关联各专利要素分表。',
  `publication_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利公开或公告时使用的文献编号。',
  `application_kind` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利申请类型代码，用于区分发明、实用新型、PCT、外观设计等申请类别。',
  `country_code_country` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利公开或公告文献对应的国家、地区或组织代码。',
  `country` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利所属或发布的国家名称。',
  `publication_reference_kind` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利公开或公告文献的种类代码。',
  `publication_reference_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '专利公开或公告发布的具体日期，格式为YYYY-MM-DD。',
  `publication_reference_year` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利公开或公告发布日期对应的年份，格式为YYYY。',
  `publication_reference_month` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利公开或公告发布日期对应的年月，格式为YYYY-MM。',
  `application_reference_apno` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利申请提交时使用的申请编号。',
  `application_reference_country` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '受理专利申请的国家、地区或组织代码。',
  `application_reference_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '专利申请提交的具体日期，格式为YYYY-MM-DD。',
  `application_reference_year` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利申请提交日期对应的年份，格式为YYYY。',
  `application_reference_month` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利申请提交日期对应的年月，格式为YYYY-MM。',
  `pct_or_reg_filing_data_doc_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'PCT 国际专利申请的申请编号。',
  `pct_or_regional_filing_data_date` date NOT NULL DEFAULT '1970-01-01' COMMENT 'PCT 国际申请提交的日期。',
  `pct_or_reg_pub_data_doc_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'PCT 国际申请对应的公布号。',
  `pct_or_regional_pub_data_date` date NOT NULL DEFAULT '1970-01-01' COMMENT 'PCT 国际申请公开发布的日期。',
  `priority_filings_sequence` int NOT NULL DEFAULT '0' COMMENT '同一专利下多条优先权信息的排列序号。',
  `priority_filings_language` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权语言',
  `priority_filings_app_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权申请的申请号。',
  `priority_filings_pub_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权申请的公布号。',
  `priority_filings_country` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权对应的国家、地区或组织代码。',
  `priority_filings_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权申请的具体日期。',
  `priority_filings_year` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权申请日期对应的年份。',
  `priority_filings_patent_type` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权申请的类型代码。',
  `priority_filings_title` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利优先权申请的具体标题。',
  `applicants_sequence` bigint NOT NULL DEFAULT '0' COMMENT '原始申请人在申请人列表中的排列序号。',
  `applicants_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利申请文件记载的原始申请人或权利人名称。',
  `assignees_sequence` bigint NOT NULL DEFAULT '0' COMMENT '当前申请人或专利权人在权利人列表中的排列序号。',
  `assignees_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前有效的申请人、受让人或专利权人名称。',
  `inventors_sequence` bigint NOT NULL DEFAULT '0' COMMENT '发明人在发明人列表中的排列序号。',
  `inventors_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利发明人的姓名或信息列表。',
  `first_applicant_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '原始申请人列表中的第一位申请人名称。',
  `first_current_assignee_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前申请人或专利权人列表中的第一位主体名称。',
  `first_inventor_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '发明人列表中的第一位发明人名称。',
  `classification_ipcr_main` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利的主要 IPCR/IPC 分类号。',
  `classification_ipcr_further` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利的附加 IPCR/IPC 分类号。',
  `classification_cpc_main` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利的主要 CPC 分类号。',
  `classification_cpc_further` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利的附加 CPC 分类号。',
  `keywords` json NOT NULL COMMENT '描述专利主题内容的关键词。',
  `claims_localized` json NOT NULL COMMENT '专利权利要求书的文本内容。',
  `description_localized` json NOT NULL COMMENT '专利说明书的正文内容。',
  `figures` json NOT NULL COMMENT '专利附图或图示相关信息。',
  `language` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利原始文本使用的语言。',
  `granted_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利获得授权后的授权编号。',
  `spif_application_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'SPIF 标准化后的专利申请号。',
  `spif_publication_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'SPIF 标准化后的专利公布号。',
  `prior_art_year` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '相关现有技术对应的年份。',
  `prior_art_date` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '相关现有技术对应的具体日期。现有技术日期是指该专利的技术在专利申请日前已经公开、发表、使用或被公众知晓的时间，可以用来判断专利新颖性和创造性',
  `relevants` json NOT NULL COMMENT '与当前专利主题或技术内容相关的专利信息。相关专利是内容推荐逻辑，相似专利，不一定是同族专利',
  `db_source` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '该条专利要素数据的来源贴源库。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的最近更新时间。',
  `citation_nums` bigint NOT NULL DEFAULT '0' COMMENT '该专利引用的专利文献数量。',
  `patent_citations_pub_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的其他专利信息。',
  `patent_citations_pub_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '当前专利引用的专利文献日期。',
  `patent_citations_country` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的专利文献所属国家、地区或组织代码。',
  `patent_citations_kind` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的专利文献种类代码。',
  `cited_by_nums` bigint NOT NULL DEFAULT '0' COMMENT '当前专利被其他专利引用的数量。',
  `cited_by_publication_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '被引专利公开号',
  `cited_by_publication_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '引用当前专利的专利文献日期。',
  `cited_by_country` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的专利文献所属国家、地区或组织代码。',
  `cited_by_kind` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的专利文献种类代码。',
  `non_patent_citations_nums` bigint NOT NULL DEFAULT '0' COMMENT '当前专利引用的非专利文献数量。',
  `non_patent_cites_non_patent_cite` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的非专利文献数量。',
  `non_patent_cites_non_patent_ci_2` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前专利引用的非专利文献日期。',
  `dates_of_public_availability_pri` date NOT NULL DEFAULT '1970-01-01' COMMENT '专利授权公告或授权公开的具体日期，格式为YYYY-MM-DD。',
  `dates_of_public_availability_yea` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利授权公告或授权公开日期对应的年份，格式为YYYY。',
  `dates_of_public_availability_mon` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利授权公告或授权公开日期对应的年月，格式为YYYY-MM。',
  `status` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利当前所处的法律状态。',
  `anticipated_expiration` date NOT NULL DEFAULT '1970-01-01' COMMENT '专利预计到期的具体日期。',
  `expiration_year` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利预计或实际到期日期对应的年份。',
  `family_citations` json NOT NULL COMMENT '同一专利家族内部的引用信息。',
  `cited_by_family` json NOT NULL COMMENT '同一专利家族内部的被引用信息。',
  `other_versions` json NOT NULL COMMENT '当前专利的其他公开、公告或授权版本信息。其他版本是专利的其他公开/审查版本，比如公开版本、授权版本、修改版本、不同语言版本',
  `worldwides` json NOT NULL COMMENT '当前专利在全球范围内的同族专利信息。',
  `simple_family_doc_number` json NOT NULL COMMENT '简单同族成员的文献号。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`patent_id`) USING BTREE,
  KEY `idx_op_publication_number` (`publication_number`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='专利信息表';

-- gkx.ods_patent_abstract definition

CREATE TABLE `ods_patent_abstract` (
  `patent_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联 dwd_patent.patent_id 的专利唯一标识，用于连接主表与各要素分表。',
  `abstract_localized_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '专利文献原始语种对应的摘要内容。',
  `abstract_localized_text_lang_en` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '专利英文摘要文本。',
  `db_source` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '该条专利要素数据的来源贴源库。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的最近更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`patent_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='专利摘要信息表';

-- gkx.ods_patent_bak_20260710 definition

CREATE TABLE `ods_patent_bak_20260710` (
  `id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '专利公布号(与DOCDB兼容)',
  `publication_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '专利公布号',
  `pct_publication_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'pct公开号',
  `application_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '专利申请号',
  `country_code` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '国家代码',
  `kind_code` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '种类代码',
  `application_kind` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '应用程序类型',
  `application_number_formatted` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '格式化的申请号',
  `pct_number` varchar(17) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'PCT编号',
  `family_id` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '家庭ID',
  `spif_publication_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'SPIF标准发布编号',
  `spif_application_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'SPIF标准申请号',
  `title_localized` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '标题',
  `abstract_localized` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '摘要',
  `claims_localized` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '权利要求',
  `claims_localized_html` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '权利要求html',
  `description_localized` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '说明书',
  `description_localized_html` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '说明书html',
  `publication_year` int DEFAULT NULL COMMENT '发布年份',
  `filing_year` int DEFAULT NULL COMMENT '申请年份',
  `grant_year` int DEFAULT NULL COMMENT '授予年份',
  `priority_year` int DEFAULT NULL COMMENT '优先权年',
  `expiration_year` int DEFAULT NULL COMMENT '失效年',
  `citation_nums` int DEFAULT NULL COMMENT '专利引用数量',
  `cited_by_nums` int DEFAULT NULL COMMENT '专利施引数量',
  `publication_date` date DEFAULT NULL COMMENT '发布日期',
  `filing_date` date DEFAULT NULL COMMENT '申请日期',
  `grant_date` date DEFAULT NULL COMMENT '授予日期',
  `priority_date` date DEFAULT NULL COMMENT '优先权日',
  `priority_claim` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '本出版物',
  `inventor` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '发明人',
  `inventor_harmonized` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '发明者信息',
  `assignee` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '受让人/申请人',
  `current_assignee` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '当前受让人/申请人',
  `assignee_harmonized` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '受让人/申请人信息',
  `examiner` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '审查员信息',
  `uspc` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '美国专利',
  `ipc` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '国际专利分类',
  `cpc` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '合作专利分类',
  `fi` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT 'FI分类',
  `fterm` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT 'fterm分类',
  `locarno` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT 'Locarno分类',
  `citation` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '出版物引用',
  `parent` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '父申请',
  `child` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '子申请',
  `entity_status` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '美国专利商标局实体状态',
  `art_unit` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '美国专利商标局艺术单位',
  `status` varchar(55) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '专利状态',
  `figures` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '专利图',
  `pdf_url` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '专利文件链接',
  `patent_citations` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '专利引用',
  `family_citations` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '家族内引用',
  `cited_by` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '被引用',
  `cited_by_family` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '家庭内被引用',
  `events` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '事件',
  `non_patent_citations` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '非专利引用',
  `legal_events` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '法律事件',
  `anticipated_expiration` date DEFAULT NULL COMMENT '预计到期日',
  `language` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '原文语言',
  `relevants` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '相关专利',
  `priority_filings` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '优先权信息',
  `precis_graph` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '摘要图AI生成OSS链接',
  `targets` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '靶点',
  `keywords` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '关键词',
  `concepts` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '概念',
  `definitions` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '定义',
  `worldwides` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '全球专利',
  `docdb_family` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '家族专利',
  `prior_art_date` date DEFAULT NULL COMMENT 'Prior art date',
  `prior_art_year` int DEFAULT NULL COMMENT 'Prior art year',
  `country` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '国家',
  `other_versions` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '其他版本',
  `external_links` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '外部链接',
  `landscapes` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '技术领域分类',
  `dwpi_basic` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'DWPI基本专利，指第一个输入到DWPI数据库的同族专利成员',
  `dwpi_family` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT 'DWPI同族公开号',
  `main_family` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '同族专利公开号',
  `complete_family` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '拓展同族公开号',
  `legal_status` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '法律状态',
  `transferor` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '转让人',
  `transfer_count` int DEFAULT NULL COMMENT '转让次数',
  `transfer_price` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '转让价格',
  `transfer_record` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '转让时间序列',
  `license_type` int DEFAULT NULL COMMENT '许可类型，如独占许可、排他许可、普通许可等许可方式',
  `license_country` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '许可地国家，专利许可在哪些国家或地区有效',
  `license_price` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '许可费用',
  `examination_detail` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '审察详细信息',
  `technical_abstract` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '技术摘要',
  `page_count` int DEFAULT NULL COMMENT '文献页数',
  `subject_classification` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '学科分类',
  `dwpi_classification` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT 'DWPI分类',
  `dwpi_title` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT 'DWPI标题',
  `dwpi_priority_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'DWPI优先权号',
  `dwpi_priority_country` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'DWPI优先权国别',
  `dwpi_assignee` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT 'DWPI专利权人',
  `dwpi_inventor` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT 'DWPI发明人',
  `inpadoc_family_id` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'INPADOC同族编号',
  `independent_claims_localized` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '独立权利要求',
  `independent_claims_localized_html` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '独立权利要求html',
  `problem_sum` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '技术问题',
  `method_sum` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '技术手段',
  `benefit_sum` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '技术功效',
  `current_assignee_harmonized` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '当前受让人/申请人信息',
  `current_inventor` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '当前发明人',
  `current_inventor_harmonized` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '当前发明者信息',
  `agent` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '代理人',
  `current_agent` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '当前代理人',
  `agency` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '代理机构',
  `current_agency` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '当前代理机构',
  `assistant_examiner` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '助理审查员信息',
  `priority_country` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '优先权国家/地区',
  `epds` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'EP指定国家/地区',
  `business_information` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '工商信息',
  `first_publication_date` date DEFAULT NULL COMMENT '首次公开日',
  `examine_date` date DEFAULT NULL COMMENT '实质审查生效日',
  `pct_entry_date` date DEFAULT NULL COMMENT 'PCT进入国家阶段日',
  `legal_status_date` date DEFAULT NULL COMMENT '法律状态更新日',
  `earliest_priority_date` date DEFAULT NULL COMMENT '最早优先权日',
  `gbc` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '国民经济行业分类号',
  `adc` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '应用领域分类',
  `ttc` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '技术主题分类',
  `seic` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '战略新兴产业分类',
  `cite_category` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '引用类别',
  `epds_count` int DEFAULT NULL COMMENT 'EP指定国家/地区数量',
  `up_status` int DEFAULT NULL COMMENT '欧洲统一法院状态',
  `epds_legal_status` int DEFAULT NULL COMMENT 'EP指定国家/地区法律状态',
  `patent_value` int DEFAULT NULL COMMENT '专利价值(美元)',
  `gov` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '政府利益',
  `examine_period` int DEFAULT NULL COMMENT '审查时长',
  `sep` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '标准专利',
  `award` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '奖励',
  `sub_case` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '分案',
  `priority_country_count` int DEFAULT NULL COMMENT '优先权国家/地区个数',
  `case_number` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '案件号',
  `court` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '审查法院',
  `judge` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '审判员',
  `chief_judge` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '审判长',
  `plaintiff` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '原告',
  `defendant` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '被告',
  `case_filing_date` date DEFAULT NULL COMMENT '立案日期',
  `verdict_date` date DEFAULT NULL COMMENT '裁判日期',
  `hearing_date` date DEFAULT NULL COMMENT '听证日期',
  `trial_grade` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '审理程序',
  `case` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '案件',
  `case_close_date` date DEFAULT NULL COMMENT '结案日期',
  `outcome` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '案件结果',
  `litigation_count` int DEFAULT NULL COMMENT '诉讼次数',
  `case_doc_type` int DEFAULT NULL COMMENT '文书类型',
  `court_grade` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '法院级别',
  `verdict` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '判决结果',
  `party` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '当事人',
  `amount_plaintiff` int DEFAULT NULL COMMENT '申请赔偿总额',
  `damages_amount` int DEFAULT NULL COMMENT '判赔总额',
  `case_filing_year` int DEFAULT NULL COMMENT '立案年份',
  `litigation_product` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '涉及产品',
  `licensor` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '许可人',
  `licensee` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '被许可人',
  `license_number` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '许可合同备案号',
  `exclusivity` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '许可排他性',
  `license_effective_date` date DEFAULT NULL COMMENT '许可生效日',
  `license_count` int DEFAULT NULL COMMENT '许可次数',
  `transfer` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '权利转移',
  `review_invalid_applicant` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '复审/无效请求人',
  `review_invalid_decision_number` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '决定号',
  `review_invalid_commission_number` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '委内编号',
  `review_invalid_decision_date` date DEFAULT NULL COMMENT '决定/发文日',
  `review_invalid_decision_type` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '决定类型',
  `review_invalid_decision` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '决定',
  `review_invalid_decision_point` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '决定要点',
  `review_invalid_decision_case_mainpoint` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '案由',
  `review_invalid_legal_basis` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '法律依据',
  `review_invalid_fulltext` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '复审/无效全文',
  `invalid_count` int DEFAULT NULL COMMENT '无效次数',
  `pledgor` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '质押人',
  `pledgee` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '质权人',
  `pledgeno` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '质押登记号',
  `pledge` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '质押信息',
  `summarize` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '总结',
  `spare_zero` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '备用0',
  `spare_one` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '备用1',
  `spare_two` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '备用2',
  `spare_three` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '备用3',
  `spare_four` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '备用4',
  `spare_five` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '备用5',
  `spare_six` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '备用6',
  `spare_seven` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '备用7',
  `spare_eight` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备用8',
  `spare_nine` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备用9',
  `spare_ten` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备用10',
  `state` tinyint DEFAULT '1' COMMENT '逻辑删除(1:存在，0:不存在)',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-专利信息表';

-- gkx.ods_patent_biblio definition

CREATE TABLE `ods_patent_biblio` (
  `patent_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利主键ID',
  `pn` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利公开(公告)号',
  `exdt` int DEFAULT NULL COMMENT '智慧芽专利预估到期日',
  `parties` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '当事人信息(申请人、发明人等)',
  `abstracts` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '摘要信息',
  `patent_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '专利类型',
  `invention_title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '标题信息',
  `priority_claims` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '优先权信息',
  `reference_cited` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '应用专利信息',
  `related_documents` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '分案申请、继续申请信息',
  `classification_data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '分类数据',
  `application_reference` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '申请信息',
  `publication_reference` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '公开信息',
  `pct_or_regional_filing_data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'PCT申请信息',
  `dates_of_public_availability` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '授权信息',
  `pct_or_regional_publishing_data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'PCT公开信息',
  PRIMARY KEY (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='全球专利-著录项目';

-- gkx.ods_patent_cited definition

CREATE TABLE `ods_patent_cited` (
  `patent_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利主键ID',
  `pn` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利公开(公告)号',
  `patent_cited` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '被引用详情',
  PRIMARY KEY (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='全球专利-专利被引用';

-- gkx.ods_patent_claims definition

CREATE TABLE `ods_patent_claims` (
  `patent_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利主键ID',
  `pn` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利公开(公告)号',
  `claims` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '权利要求信息',
  `claim_count` int DEFAULT NULL COMMENT '权利要求统计',
  PRIMARY KEY (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='全球专利-权利要求';

-- gkx.ods_patent_description definition

CREATE TABLE `ods_patent_description` (
  `patent_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利主键ID',
  `pn` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利公开(公告)号',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '说明书信息',
  PRIMARY KEY (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='全球专利-说明书';

-- gkx.ods_patent_drawing definition

CREATE TABLE `ods_patent_drawing` (
  `patent_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利主键ID',
  `pn` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利公开(公告)号',
  `abstract_drawing` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '摘要附图信息',
  PRIMARY KEY (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='全球专利-摘要附图';

-- gkx.ods_patent_family definition

CREATE TABLE `ods_patent_family` (
  `patent_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联 dwd_patent.patent_id 的专利唯一标识，用于连接主表与各要素分表。',
  `simple_family_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '简单同族或专利家族的唯一编号。',
  `simple_family_country` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '简单同族成员所属国家、地区或组织代码。',
  `simple_family_kind` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '简单同族成员公开或公告文献的种类代码。',
  `db_source` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '该条专利要素数据的来源贴源库。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的最近更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`patent_id`) USING BTREE,
  KEY `idx_opf_simple_family_id` (`simple_family_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='专利家族信息表';

-- gkx.ods_patent_family_bak_20260710 definition

CREATE TABLE `ods_patent_family_bak_20260710` (
  `patent_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利主键ID',
  `pn` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利公开(公告)号',
  `patent_family` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '专利家族信息',
  PRIMARY KEY (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='全球专利-专利家族';

-- gkx.ods_patent_info definition

CREATE TABLE `ods_patent_info` (
  `lngid` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `media_c` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `years` int DEFAULT NULL,
  `title_c` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `title_e` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `keyword_c` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `keyword_e` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `remark_c` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `remark_e` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `class` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `firstclass` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `beginpage` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `endpage` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `jumppage` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `pagecount` int DEFAULT NULL,
  `showwriter` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `author_e` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `showorgan` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `intpdf` int DEFAULT NULL,
  `country` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `language` int DEFAULT NULL,
  `type` int DEFAULT NULL,
  `classtypes` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `showclasstypes` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `fulltextaddress` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `zlmaintype` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zlapplicantaddr` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `zlprovincecode` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zlapplicationnum` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zlapplicationdata` int DEFAULT NULL,
  `zlopendata` int DEFAULT NULL,
  `zlpriority` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `zlprioritynumber` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zlmainclassnum` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zlclassnum` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zlinternationalpub` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zlinternationalapp` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zlcomeindata` int DEFAULT NULL,
  `zlsovereignty` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `zlagents` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zlagency` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zllegalstatus` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zlthesissize` int DEFAULT NULL,
  `zlaccdate` int DEFAULT NULL,
  `zlpatentstate` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='维普专利信息';

-- gkx.ods_patent_legal definition

CREATE TABLE `ods_patent_legal` (
  `patent_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联 dwd_patent.patent_id 的专利唯一标识，用于连接主表与各要素分表。',
  `patent_legal` json NOT NULL COMMENT '专利生命周期中的法律状态变更事件。',
  `patent_legal_event_date` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'PRS 法律状态事件发生日期。',
  `patent_legal_event_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'PRS 法律状态事件代码。',
  `patent_legal_patent_legal_prs_da` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '法律状态事件所属分类的说明。',
  `db_source` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '该条专利要素数据的来源贴源库。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的最近更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`patent_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='法律状态信息表';

-- gkx.ods_patent_legal_status definition

CREATE TABLE `ods_patent_legal_status` (
  `patent_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利主键ID',
  `pn` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专利公开(公告)号',
  `legal_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '法定日期',
  `patent_legal` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '法律状态详情',
  PRIMARY KEY (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='全球专利-法律状态';

-- gkx.ods_patent_title definition

CREATE TABLE `ods_patent_title` (
  `patent_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联 dwd_patent.patent_id 的专利唯一标识，用于连接主表与各要素分表。',
  `title_localized_text` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利文献原始语种对应的标题内容。',
  `title_localized_text_lang_en` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '专利英文标题文本。',
  `db_source` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '该条专利要素数据的来源贴源库。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条记录在专利要素库中的最近更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`patent_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='专利标题信息表';

-- gkx.ods_protein definition

CREATE TABLE `ods_protein` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '蛋白质对应的内部或来源库唯一标识',
  `protein_name` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '蛋白质的标准名称或推荐名称',
  `uniprot_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '蛋白质在 UniProt 数据库中的唯一编号',
  `gene_names` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '编码该蛋白的基因符号或别名',
  `protein_length` int DEFAULT NULL COMMENT '蛋白质氨基酸序列长度',
  `sequence` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '蛋白质的一字母氨基酸序列',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_protein_protein_name` (`protein_name`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='蛋白质表';

-- gkx.ods_quantum_chain_link definition

CREATE TABLE `ods_quantum_chain_link` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '表主键，唯一标识每条上链结果记录',
  `entity_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '上链实体的类型',
  `industry_chain_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '所属产业链的唯一标识ID',
  `entity_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '上链实体的唯一标识ID，与对应业务表的主键关联',
  `industry_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子产业的标准产业分类编码',
  `industry_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业编码对应的产业名称',
  `link_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业链环节的标准编码',
  `link_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '环节编码对应的产业链环节名称',
  `link_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '实体完成产业链挂链的时间',
  `link_operator` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '执行挂链操作的操作人员账号/姓名',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='上链结果表';

-- gkx.ods_quantum_frontier_talent definition

CREATE TABLE `ods_quantum_frontier_talent` (
  `id` bigint NOT NULL COMMENT '表主键，唯一标识每条人才记录',
  `person_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子领域人才的公开姓名',
  `organization_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '人才所属的科研机构、高校或企业名称',
  `research_direction` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '人才在量子领域的核心研究方向',
  `major_achievements` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '人才公开发表的核心论文、主持的重点科研项目等成果',
  `publish_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条人才信息的首次发布时间',
  `source_update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条人才信息的最新更新时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='量子前沿人才';

-- gkx.ods_quantum_market_scale definition

CREATE TABLE `ods_quantum_market_scale` (
  `id` bigint NOT NULL COMMENT '表主键，唯一标识每条市场规模记录',
  `stat_year` int NOT NULL DEFAULT '0' COMMENT '市场规模数据对应的统计年份',
  `region` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '市场规模数据对应的地理区域',
  `sub_field` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子产业的细分赛道领域',
  `market_size_100m` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '对应细分领域的市场规模，单位为亿元',
  `growth_rate` decimal(5,2) NOT NULL DEFAULT '0.00' COMMENT '市场规模的同比增长率，单位为%',
  `report_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该市场数据所属报告的发布时间',
  `source_update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条市场数据的最新更新时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='量子市场规模';

-- gkx.ods_quantum_product definition

CREATE TABLE `ods_quantum_product` (
  `id` bigint NOT NULL COMMENT '表主键，唯一标识每条产品记录',
  `product_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子相关产品的正式名称',
  `product_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子产品的分类类型',
  `company_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品所属的研发/生产企业全称',
  `credit_code` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '企业的统一社会信用代码',
  `product_parameters` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品的核心技术参数、规格指标',
  `application_scenario` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品的主要落地应用场景',
  `publish_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条产品信息的首次发布时间',
  `source_update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条产品信息的最新更新时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='量子产品信息';

-- gkx.ods_quantum_rd_progress definition

CREATE TABLE `ods_quantum_rd_progress` (
  `id` bigint NOT NULL COMMENT '表主键，唯一标识每条研发进展记录',
  `project_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子研发项目的正式名称',
  `organization_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目的核心承担研发单位名称',
  `credit_code` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '承担单位为企业时的统一社会信用代码',
  `rd_direction` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目的核心研发技术方向',
  `rd_stage` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目当前所处的研发阶段',
  `progress_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目当前的整体研发进展情况说明',
  `key_breakthrough` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目研发过程中取得的核心技术突破、创新成果',
  `publish_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条研发进展信息的首次发布时间',
  `source_update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条研发进展信息的最新更新时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='量子研发进展';

-- gkx.ods_quantum_tech_trend definition

CREATE TABLE `ods_quantum_tech_trend` (
  `id` bigint NOT NULL COMMENT '表主键，唯一标识每条技术趋势记录',
  `technology_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '量子相关技术的标准名称',
  `technology_category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技术的分类属性',
  `technology_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '该量子技术的核心原理、技术特点、核心能力说明',
  `maturity_stage` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技术当前的成熟度阶段',
  `application_prospect` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '该技术未来的落地应用场景、市场潜力、发展前景分析',
  `main_orgs` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '该技术的核心研发机构、头部企业',
  `publish_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条技术趋势信息的首次发布时间',
  `source_update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '该条技术趋势信息的最新更新时间',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='量子技术趋势';

-- gkx.ods_react_detail definition

CREATE TABLE `ods_react_detail` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '化学反应记录的唯一标识',
  `step_count` int DEFAULT NULL COMMENT '反应路线包含的步骤数量',
  `reactants` json DEFAULT NULL COMMENT '参与反应的起始物、试剂或底物集合',
  `products` json DEFAULT NULL COMMENT '反应生成物或目标产物集合',
  `yield_value` json DEFAULT NULL COMMENT '目标产物的反应收率',
  `catalyst` json DEFAULT NULL COMMENT '反应中使用的催化剂或关键促进剂',
  `temperature` int DEFAULT NULL COMMENT '反应温度的数值部分',
  `temperature_unit` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '反应温度使用的计量单位',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='化学反应信息表';

-- gkx.ods_rel_reaction_substance definition

CREATE TABLE `ods_rel_reaction_substance` (
  `id` bigint NOT NULL COMMENT '反应-物质关联记录主键',
  `reaction_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联化学反应信息表的反应ID',
  `substance_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联物质信息表的物质ID',
  `substance_role` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '物质在反应中的角色',
  `source_field` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '关系来源于反应表中的哪个字段',
  `yield_value` decimal(18,6) DEFAULT NULL COMMENT '当角色为产物时记录对应产率数值',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`,`reaction_id`) USING BTREE,
  KEY `idx_ods_rel_reaction_substance_reaction_id` (`reaction_id`) USING BTREE,
  KEY `idx_ods_rel_reaction_substance_substance_id` (`substance_id`) USING BTREE,
  KEY `idx_ods_rel_reaction_substance_substance_role` (`substance_role`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='反应-物质关联表';

-- gkx.ods_safety definition

CREATE TABLE `ods_safety` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '药品安全记录的内部或来源库唯一标识',
  `receivedate` date DEFAULT NULL COMMENT '药物不良事件报告在 FAERS 等安全数据库中的接收日期',
  `drug_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '药物安全、交易或试验记录中涉及的药品名称',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_safety_drug_name` (`drug_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='药物安全表';

-- gkx.ods_scholar definition

CREATE TABLE `ods_scholar` (
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者记录的业务唯一标识。',
  `name_en` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者的英文姓名。',
  `name_zh` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者的中文姓名。',
  `avatar` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者头像图片的访问链接。',
  `scholar_org_name_en` varchar(4096) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者所属机构的英文名称。',
  `scholar_org_name_zh` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者所属机构的中文名称。',
  `bio` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者的个人或学术简介信息。',
  `bio_zh` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者的中文个人或学术简介信息。',
  `work_experience_en` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者英文工作经历信息。',
  `work_experience_zh` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者中文工作经历信息。',
  `education_background_en` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者的英文教育经历信息。',
  `education_background_zh` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者的中文教育经历信息。',
  `paper_nums` int NOT NULL DEFAULT '0' COMMENT '学者已发表论文的数量。',
  `citation_nums` int NOT NULL DEFAULT '0' COMMENT '学者论文被引用的总次数。',
  `h_index` int NOT NULL DEFAULT '0' COMMENT '衡量学者学术影响力的 H 指数。',
  `status` int NOT NULL DEFAULT '0' COMMENT '记录状态，0 表示无效，1 表示有效。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录最后更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`scholar_id`) USING BTREE,
  KEY `idx_ods_scholar_name_en` (`name_en`) USING BTREE,
  KEY `idx_ods_scholar_name_zh` (`name_zh`) USING BTREE,
  KEY `idx_os_scholar_org_name_en` (`scholar_org_name_en`(191)) USING BTREE,
  KEY `idx_os_scholar_org_name_zh` (`scholar_org_name_zh`(191)) USING BTREE,
  KEY `idx_ods_scholar_paper_nums` (`paper_nums`) USING BTREE,
  KEY `idx_ods_scholar_citation_nums` (`citation_nums`) USING BTREE,
  KEY `idx_ods_scholar_create_time` (`create_time`) USING BTREE,
  KEY `idx_ods_scholar_update_time` (`update_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='学者';

-- gkx.ods_scholar_coauthor definition

CREATE TABLE `ods_scholar_coauthor` (
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '当前学者记录的业务唯一标识。',
  `co_scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '合作学者记录的业务唯一标识。',
  `co_scholar_name_en` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '合作学者的英文姓名。',
  `co_scholar_name_zh` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '合作学者的中文姓名。',
  `co_scholar_avatar` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '合作学者头像图片的访问链接。',
  `co_scholar_org_name_en` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '合作学者所属机构的英文名称。',
  `co_scholar_org_name_zh` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '合作学者所属机构的中文名称。',
  `co_scholar_org_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '合作学者所属机构的业务唯一标识。',
  `co_paper_count` int NOT NULL DEFAULT '0' COMMENT '与该学者合作发表的论文数量。',
  `status` int NOT NULL DEFAULT '0' COMMENT '记录状态，0 表示无效，1 表示有效。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录最后更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`scholar_id`,`co_scholar_id`) USING BTREE,
  KEY `idx_osc_co_scholar_name_en` (`co_scholar_name_en`(191)) USING BTREE,
  KEY `idx_osc_co_scholar_name_zh` (`co_scholar_name_zh`) USING BTREE,
  KEY `idx_ods_scholar_coauthor_status` (`status`) USING BTREE,
  KEY `idx_osc_update_time` (`update_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='学者合作者关系';

-- gkx.ods_scholar_paper_relation definition

CREATE TABLE `ods_scholar_paper_relation` (
  `paper_id` int NOT NULL DEFAULT '0' COMMENT '论文记录的唯一标识。',
  `year` int NOT NULL DEFAULT '0' COMMENT '论文发表年份。',
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '学者记录的业务唯一标识。',
  `citations` int NOT NULL DEFAULT '0' COMMENT '论文被引用次数。',
  `publish_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '论文发布时间。',
  `status` int NOT NULL DEFAULT '0' COMMENT '记录状态，0 表示无效，1 表示有效。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录最后更新时间。',
  `publication_id` int NOT NULL DEFAULT '0' COMMENT '期刊或会议记录的唯一标识。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`scholar_id`,`paper_id`) USING BTREE,
  KEY `idx_ospr_citations` (`citations`) USING BTREE,
  KEY `idx_ospr_publish_time` (`publish_time`) USING BTREE,
  KEY `idx_ospr_create_time` (`create_time`) USING BTREE,
  KEY `idx_ospr_update_time` (`update_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='学者论文关系';

-- gkx.ods_scholar_papers definition

CREATE TABLE `ods_scholar_papers` (
  `paper_id` bigint NOT NULL DEFAULT '0' COMMENT '论文记录的唯一标识，依据人才数据核验对象补充。',
  `zh_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的中文标题名称。',
  `en_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的英文标题名称。',
  `authors` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '论文作者的姓名或信息列表。',
  `paper_url` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文原始来源页面的访问链接。',
  `cover_date_start` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '论文正式发表或出版的时间。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录最后更新时间。',
  `status` int NOT NULL DEFAULT '0' COMMENT '记录状态，0 表示无效，1 表示有效。',
  `zh_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '论文内容的中文摘要信息。',
  `en_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '论文内容的英文摘要信息。',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的 DOI 唯一识别号。',
  `publication_en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文发表所在期刊或会议的英文名称。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`paper_id`) USING BTREE,
  KEY `idx_ods_scholar_papers_en_name` (`en_name`(191)) USING BTREE,
  KEY `idx_osp_cover_date_start` (`cover_date_start`) USING BTREE,
  KEY `idx_osp_create_time` (`create_time`) USING BTREE,
  KEY `idx_osp_update_time` (`update_time`) USING BTREE,
  KEY `idx_ods_scholar_papers_doi` (`doi`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='论文信息';

-- gkx.ods_scholar_research_direction definition

CREATE TABLE `ods_scholar_research_direction` (
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联学者记录的业务唯一标识。',
  `fields` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '学者研究方向，来源于表1字段。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录最后更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`scholar_id`) USING BTREE,
  KEY `idx_osrd_create_time` (`create_time`) USING BTREE,
  KEY `idx_osrd_update_time` (`update_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='学者研究方向';

-- gkx.ods_scholar_talent_flag definition

CREATE TABLE `ods_scholar_talent_flag` (
  `scholar_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '关联学者记录的业务唯一标识。',
  `academician` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标识学者是否为院士，来源于表1字段。',
  `create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录创建时间。',
  `update_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '记录最后更新时间。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`scholar_id`) USING BTREE,
  KEY `idx_ostf_academician` (`academician`) USING BTREE,
  KEY `idx_ostf_create_time` (`create_time`) USING BTREE,
  KEY `idx_ostf_update_time` (`update_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='学者人才标识';

-- gkx.ods_series_metadata definition

CREATE TABLE `ods_series_metadata` (
  `metadata_id` bigint NOT NULL COMMENT '数列的唯一标识符',
  `metadata_name` varchar(1600) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列名称',
  `metadata_indicators` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '指标',
  `metadata_unit_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数列单位ID',
  `metadata_unit_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数列单位名称',
  `metadata_country_id` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列国家ID',
  `metadata_country_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列国家名称',
  `metadata_frequency_id` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列频率ID',
  `metadata_frequency_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列频率名称',
  `metadata_status_id` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列状态ID',
  `metadata_status_name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数列状态名称',
  `metadata_source_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据来源ID',
  `metadata_source_name` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据来源名称',
  `metadata_startdate` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '第一个时间点的日期',
  `metadata_enddate` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '最后时间点的日期',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`metadata_id`) USING BTREE,
  KEY `idx_ods_series_metadata_metadata_name` (`metadata_name`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='序列元数据';

-- gkx.ods_series_timepoints definition

CREATE TABLE `ods_series_timepoints` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '业务侧生成主键',
  `timepoints_value` decimal(18,6) NOT NULL DEFAULT '0.000000' COMMENT '数据时间点值',
  `timepoints_date` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据时间点日期',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_series_timepoints_timepoints_value` (`timepoints_value`) USING BTREE,
  KEY `idx_ods_series_timepoints_timepoints_date` (`timepoints_date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='序列时间点';

-- gkx.ods_similar_substance definition

CREATE TABLE `ods_similar_substance` (
  `similar_substance_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '相似物质记录的唯一标识',
  `en_name` varchar(4000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '物质的英文名称或标准名称',
  `cas_registry_id` json DEFAULT NULL COMMENT '化学物质的 CAS Registry Number',
  `formula` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分子、化合物或晶体的化学组成式',
  `similar_paper_count` int NOT NULL DEFAULT '0' COMMENT '与相似分子相关的论文数量',
  `similar_publication_count` int NOT NULL DEFAULT '0' COMMENT '与相似分子相关的专利或公开文献数量',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`similar_substance_id`) USING BTREE,
  KEY `idx_ods_similar_substance_en_name` (`en_name`(191)) USING BTREE,
  KEY `idx_ods_similar_substance_formula` (`formula`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='结构相近的其他分子';

-- gkx.ods_small_molecule_screening definition

CREATE TABLE `ods_small_molecule_screening` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '小分子活性与筛选的内部或来源库唯一标识',
  `molecular_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '化合物、材料或分子的标准英文名称',
  `reference` json DEFAULT NULL COMMENT '支持该条记录的论文、数据库页面或 DOI 等来源信息',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_small_molecule_screening_molecular_name` (`molecular_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='小分子活性与筛选';

-- gkx.ods_substance definition

CREATE TABLE `ods_substance` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分子或物质记录的唯一标识',
  `en_name` varchar(4000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '物质的英文名称或标准名称',
  `cas_registry_id` json DEFAULT NULL COMMENT '化学物质的 CAS Registry Number',
  `formula` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '分子、化合物或晶体的化学组成式',
  `synonym` json DEFAULT NULL COMMENT '化合物或物质的别名、商品名或历史名称',
  `chemical_type` json DEFAULT NULL COMMENT '物质的化学类别或结构分类',
  `weight` decimal(18,6) DEFAULT NULL COMMENT '化合物的相对分子质量',
  `iupac_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '化合物的系统性 IUPAC 名称',
  `std_smiles` varchar(4000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '包含立体化学信息的 SMILES 表示',
  `in_chi_key` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'InChI 的固定长度哈希标识，用于化合物快速匹配和去重',
  `in_chi` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '化合物的 IUPAC 国际化学标识符',
  `heavy_atom_count` int DEFAULT NULL COMMENT '分子中非氢原子的数量',
  `total_formal_charge` int DEFAULT NULL COMMENT '分子的总形式电荷',
  `complexity` int DEFAULT NULL COMMENT '基于结构特征计算的分子复杂度指标',
  `isotope_atom_count` int DEFAULT NULL COMMENT '分子中同位素标记原子的数量',
  `atom_chiral_count` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '分子中已明确和未明确构型的原子手性中心数量',
  `bond_chiral_count` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '分子中已明确和未明确构型的立体键数量',
  `covalent_unit_count` int DEFAULT NULL COMMENT '分子结构中通过共价键连接形成的独立结构单元数量',
  `xlogp` decimal(18,6) DEFAULT NULL COMMENT '化合物的 LogP，用于表征亲脂性',
  `hydrogen_bond_donor_count` int DEFAULT NULL COMMENT '分子中可作为氢键供体的原子或基团数量',
  `hydrogen_bond_acceptor_count` int DEFAULT NULL COMMENT '分子中可作为氢键受体的原子或基团数量',
  `rotatable_bond_count` int DEFAULT NULL COMMENT '分子中可自由旋转的单键数量',
  `tpsa` decimal(18,6) DEFAULT NULL COMMENT '分子的拓扑极性表面积，用于评估吸收和渗透性',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_substance_en_name` (`en_name`(191)) USING BTREE,
  KEY `idx_ods_substance_formula` (`formula`(191)) USING BTREE,
  KEY `idx_ods_substance_iupac_name` (`iupac_name`(191)) USING BTREE,
  KEY `idx_ods_substance_std_smiles` (`std_smiles`(191)) USING BTREE,
  KEY `idx_ods_substance_in_chi_key` (`in_chi_key`) USING BTREE,
  KEY `idx_ods_substance_in_chi` (`in_chi`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='物质信息表';

-- gkx.ods_zck_intl_policy definition

CREATE TABLE `ods_zck_intl_policy` (
  `policy_record_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '唯一ID',
  `original_title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标题原文',
  `translated_title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标题译文',
  `original_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '正文原文',
  `translated_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '正文译文',
  `original_summary` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '摘要原文',
  `media_region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '所属区域',
  `publish_date_raw` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '发布时间',
  `media_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '媒体名称',
  `source_url` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'url链接',
  `language_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '语种',
  `media_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '媒体类型',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`policy_record_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='国际政策信息表';

-- gkx.ods_zck_intl_policy_fill definition

CREATE TABLE `ods_zck_intl_policy_fill` (
  `policy_record_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '唯一ID',
  `original_title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标题原文',
  `original_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '正文原文',
  `original_summary` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '摘要原文',
  `media_region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '所属区域',
  `publish_date_raw` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '发布时间',
  `media_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '媒体名称',
  `source_url` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'url链接',
  `language_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '语种',
  `media_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '媒体类型',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`policy_record_id`) USING BTREE,
  KEY `idx_ods_zck_intl_policy_fill_ir_urldate` (`publish_date_raw`) USING BTREE,
  KEY `idx_ods_zck_intl_policy_fill_sy_media_product_name` (`media_name`) USING BTREE,
  KEY `idx_ods_zck_intl_policy_fill_ir_urlname` (`source_url`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='国际政策信息增补表';

-- gkx.ods_zck_policy definition

CREATE TABLE `ods_zck_policy` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '唯一ID',
  `datatype` tinyint DEFAULT NULL COMMENT '数据类型（政策/解读）',
  `docstatus` tinyint DEFAULT NULL COMMENT '政策的发布状态（20-已发布，30-已撤销）',
  `title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标题（纯文本）',
  `titlena` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标题（富文本）',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '内容（纯文本）',
  `contentNa` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '内容（富文本）',
  `url` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '原文链接地址',
  `issueno` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '发文字号',
  `indexno` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '索引号',
  `sitename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '站点名称',
  `crtime` date DEFAULT NULL COMMENT '成文日期',
  `pubtime` date DEFAULT NULL COMMENT '发文日期（发布日期）',
  `pubyear` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '发布年份',
  `area` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '发布单位的所属地区',
  `policylevel` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '政策层级（国家级/省级/市级/区县级）',
  `region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '政策地区',
  `attachments` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '政策附件文件的链接',
  `keywords` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '政策内容关键词',
  `abs` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '正文摘要',
  `maelements` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '对政策背景、指导思想等政策内容进行标准化拆解与提炼',
  `ma_keypoints` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '从政策全文中摘录、提炼章节标题、工作原则、发展现状、重点任务、细分产业、问题研判等内容。',
  `allfactors` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '含扶持分类、扶持门槛扶持力度。目的是提取政策中各类扶持、补助、优惠、激励类内容需满足的条件和对应的扶持信息',
  `complextaginfojson` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '政策所有的标签（json格式）',
  `pedigree` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '政策的上位政策和下位政策',
  `ma_contenttypenew` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用于区分政策文件的性质、发文类别、公文体裁，是政务数据基础分类字段',
  `pubdeptname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '发布单位名称',
  `topic_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '政策主题分类',
  `expiration_date` date DEFAULT NULL COMMENT '失效日期',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_zck_policy_id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内政策信息表';

-- gkx.ods_zck_policy_fill definition

CREATE TABLE `ods_zck_policy_fill` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '唯一ID',
  `title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标题（纯文本）',
  `contentNa` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '内容（富文本）',
  `url` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '原文链接地址',
  `sitename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '站点名称',
  `pubtime` date DEFAULT NULL COMMENT '发文日期（发布日期）',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_zck_policy_fill_id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内政策信息增补表';

-- gkx.ods_zh_journal definition

CREATE TABLE `ods_zh_journal` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '期刊记录的唯一标识。',
  `publication_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '出版物类别，例如期刊，会议等',
  `country` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊所属或出版所在的国家。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的中文名称。',
  `name_abbr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊名称的简称或缩写。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的英文名称。',
  `iscn` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国内统一刊号。',
  `issn` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国际标准连续出版物编号。',
  `eissn` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊电子版的国际标准连续出版物编号。',
  `founding_time` int NOT NULL DEFAULT '0' COMMENT '期刊首次创办或发行的时间。',
  `jn_official` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '期刊官方网站地址。',
  `zh_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '期刊的中文简介或说明。',
  `format` tinytext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '期刊的版面开本规格。',
  `postal_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊邮政发行使用的代号。',
  `chief_editor` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊当前或记录中的主编信息。',
  `organizer` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '负责主办该期刊的单位名称。',
  `publisher_place` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊出版发行的地点。',
  `award` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '期刊获得的奖项或荣誉信息。',
  `cite_nums` int NOT NULL DEFAULT '0' COMMENT '期刊或文献的累计被引用次数。',
  `annual_publication` int NOT NULL DEFAULT '0' COMMENT '期刊每年发表文章的数量。',
  `review` tinyint NOT NULL DEFAULT '0' COMMENT '标识该期刊是否为综述类期刊。',
  `impact_factor` double NOT NULL DEFAULT '0' COMMENT '期刊的影响因子指标。',
  `sub_quartile` tinyint NOT NULL DEFAULT '0' COMMENT '期刊在相关评价体系中的分区信息。Subject Quartile in Category分区',
  `classify_list` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献或期刊对应的学科分类编号。',
  `warning` tinyint NOT NULL DEFAULT '0' COMMENT '标识期刊是否处于预警状态。',
  `is_sci` tinyint NOT NULL DEFAULT '0' COMMENT '标识期刊是否被 SCI 收录。',
  `publication_cycle` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的出版频率或发行周期。',
  `paper_nums` int NOT NULL DEFAULT '0' COMMENT '期刊已发表论文的数量。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE,
  KEY `idx_ods_zh_journal_id` (`id`) USING BTREE,
  KEY `idx_ozj_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_ods_zh_journal_zh_name` (`zh_name`(191)) USING BTREE,
  KEY `idx_ods_zh_journal_name_abbr` (`name_abbr`(191)) USING BTREE,
  KEY `idx_ods_zh_journal_en_name` (`en_name`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文期刊详情信息';

-- gkx.ods_zh_journal_bak_20260710 definition

CREATE TABLE `ods_zh_journal_bak_20260710` (
  `lngid` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `media_c` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `media_e` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `gch` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `gch5` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `years` int DEFAULT NULL,
  `vol` int DEFAULT NULL,
  `num` int DEFAULT NULL,
  `title_c` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `title_e` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `keyword_c` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `keyword_e` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `remark_c` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `remark_e` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `firstclass` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `class` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `beginpage` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `endpage` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `jumppage` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `pagecount` int DEFAULT NULL,
  `firstwriter` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `showwriter` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `firstorgan` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `showorgan` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `showwriter_e` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `showorgan_e` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `author_e` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `publishdate` int DEFAULT NULL,
  `doi` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `intpdf` int DEFAULT NULL,
  `pdfsize` int DEFAULT NULL,
  `range` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `language` int DEFAULT NULL,
  `type` int DEFAULT NULL,
  `issn` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `cnno` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `classtypes` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `showclasstypes` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `subject_edu` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `corr_author` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `fulltextaddress` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='维普中文报告信息';

-- gkx.ods_zh_paper definition

CREATE TABLE `ods_zh_paper` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的英文标题名称。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的中文标题名称。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '关联出版物的id，用于获取期刊详情信息',
  `paper_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献所属出版物的章节名称，栏目等。',
  `publication_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '出版物类别，例如期刊，会议等',
  `publication_zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的中文名称。',
  `issn` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊的国际标准连续出版物编号。',
  `volume` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献发表所在期刊的卷号。',
  `issue` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献发表所在期刊的期号。',
  `directory_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '目录',
  `page_range` tinytext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '页码内容',
  `first_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文在期刊中的起始页码。',
  `last_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文在期刊中的结束页码。',
  `cover_year_start` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献正式发表的日期。',
  `cover_date_start` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献正式发表的日期。',
  `online_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文网上可见时间',
  `language_classify` tinyint NOT NULL DEFAULT '0' COMMENT '期刊出版使用的语言类型。',
  `abstract_available` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '摘要是否可用。',
  `open_access` tinyint NOT NULL DEFAULT '0' COMMENT '标识期刊或论文是否为开放获取。',
  `paper_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献数据的原始来源地址。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_ods_zh_paper_doi` (`doi`(191)) USING BTREE,
  KEY `idx_ods_zh_paper_en_name` (`en_name`(191)) USING BTREE,
  KEY `idx_ods_zh_paper_zh_name` (`zh_name`(191)) USING BTREE,
  KEY `idx_ods_zh_paper_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_ozp_publication_zh_name` (`publication_zh_name`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文详情信息';

-- gkx.ods_zh_paper_abstract definition

CREATE TABLE `ods_zh_paper_abstract` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `abstract_sequence` int NOT NULL DEFAULT '0' COMMENT '同一文献多个摘要的顺序号',
  `language` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献或期刊出版使用的语言类型。',
  `original_abstract` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '是否为原始摘要。',
  `en_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献内容的英文摘要信息。',
  `zh_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '文献内容的中文摘要信息。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`,`abstract_sequence`) USING BTREE,
  KEY `idx_ods_zh_paper_abstract_id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文摘要信息';

-- gkx.ods_zh_paper_author definition

CREATE TABLE `ods_zh_paper_author` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `author_sequence` int NOT NULL DEFAULT '0' COMMENT '作者在文献中的顺序。',
  `author_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者的唯一主键 id',
  `author_en_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者的英文名称',
  `author_zh_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献作者中文名',
  `email` json NOT NULL COMMENT '文献作者email',
  `correspond` tinyint NOT NULL DEFAULT '0' COMMENT '是否为通讯作者',
  `institution` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '作者所属机构或单位的名称。',
  `affiliation` json NOT NULL COMMENT '文献作者地址',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`,`author_sequence`) USING BTREE,
  KEY `idx_ods_zh_paper_author_id` (`id`) USING BTREE,
  KEY `idx_ozpa_author_id` (`author_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文文献作者详情信息';

-- gkx.ods_zh_paper_citation definition

CREATE TABLE `ods_zh_paper_citation` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '关联出版物的id，用于获取期刊详情信息',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '引用文献的中文标题名称。',
  `publication_zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献出版物的中文名称。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE,
  KEY `idx_ods_zh_paper_citation_id` (`id`) USING BTREE,
  KEY `idx_ozpc_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_ods_zh_paper_citation_doi` (`doi`(191)) USING BTREE,
  KEY `idx_ozpc_publication_zh_name` (`publication_zh_name`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文引用文献信息';

-- gkx.ods_zh_paper_classification definition

CREATE TABLE `ods_zh_paper_classification` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `scope` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊所属的大类学科领域。',
  `scope_zone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '期刊所属的细分学科领域。',
  `col_113` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '描述论文主题内容的关键词。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE,
  KEY `idx_ozpc_id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文分类信息';

-- gkx.ods_zh_paper_reference definition

CREATE TABLE `ods_zh_paper_reference` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `publication_id` bigint NOT NULL DEFAULT '0' COMMENT '关联出版物的id，用于获取期刊详情信息',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献的中文标题名称。',
  `publication_zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献出版物的中文名称。',
  `cover_year_start` date NOT NULL DEFAULT '1970-01-01' COMMENT '文献正式发表的年份。',
  `volume` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献发表所在期刊的卷号。',
  `issue` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献发表所在期刊的期号。',
  `first_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献在期刊中的起始页码。',
  `last_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '参考文献在期刊中的结束页码。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE,
  KEY `idx_ods_zh_paper_reference_id` (`id`) USING BTREE,
  KEY `idx_ozpr_publication_id` (`publication_id`) USING BTREE,
  KEY `idx_ods_zh_paper_reference_doi` (`doi`(191)) USING BTREE,
  KEY `idx_ozpr_publication_zh_name` (`publication_zh_name`(191)) USING BTREE,
  KEY `idx_ozpr_cover_year_start` (`cover_year_start`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文参考文献信息';

-- gkx.ods_zh_paper_related definition

CREATE TABLE `ods_zh_paper_related` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `relevant` json NOT NULL COMMENT '与当前文献内容或主题相关的文献信息。',
  `doi` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '论文的唯一标识编码。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '相关文献的英文标题名称。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`) USING BTREE,
  KEY `idx_ods_zh_paper_related_id` (`id`) USING BTREE,
  KEY `idx_ods_zh_paper_related_doi` (`doi`(191)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文关联文献信息';

-- gkx.ods_zh_paper_title definition

CREATE TABLE `ods_zh_paper_title` (
  `logic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题信息表逻辑主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献记录的唯一主键标识。',
  `title_sequence` int NOT NULL DEFAULT '0' COMMENT '同一文献多个标题的顺序号。',
  `en_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的英文标题名称。',
  `zh_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '文献的中文标题名称。',
  `language_code` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题的语言代码。',
  `language` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '标题的语言类型。',
  `original_title` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '是否为原始标题。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`logic_id`,`title_sequence`) USING BTREE,
  KEY `idx_ods_zh_paper_title_id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文论文标题信息';

-- gkx.ods_zh_policy definition

CREATE TABLE `ods_zh_policy` (
  `id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '唯一id',
  `data_type` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据类型',
  `status` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '政策状态（已发布、已撤销）',
  `title` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '标题（纯文本）',
  `title_na` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '标题（富文本）',
  `content` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '内容',
  `url` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '原文链接地址',
  `issue_no` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '发文字号',
  `index_no` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '索引号',
  `site_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '站点名称',
  `create_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '成文日期',
  `publish_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '发文日期',
  `publish_year` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '发布年份',
  `area` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '地区',
  `area_code` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '地区编码',
  `policy_level` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '政策层级',
  `region` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '完整地区',
  `platform` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '数据来源平台',
  `attachments` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '附件',
  `keywords` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '关键词',
  `abstracts` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '摘要',
  `elements` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '主旨要素',
  `keypoints` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '政策要点',
  `allfactors` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '扶持要素',
  `tags` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '标签集',
  `pedigree` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '政策谱系',
  `content_type` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '内容分类',
  `publish_department` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '发文机构',
  `region_origin` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '地区原始信息',
  `updated_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '更新时间',
  `industry` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '产业分类'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='拓尔思6月政策样例数据';

-- gkx.ods_zh_project definition

CREATE TABLE `ods_zh_project` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目记录的唯一主键标识。',
  `project_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目在管理系统中的编号。',
  `title` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目的名称或标题。',
  `project_source` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目所属的资助来源或立项来源。',
  `funded_institution` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '获得项目资助的机构名称。',
  `project_level` enum('国家级','省级','市级','县级','其他') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目所属的级别或层次。',
  `funded_amount` decimal(18,2) DEFAULT NULL COMMENT '项目获得的资助经费金额，单位为万元。',
  `discipline` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目所属的学科领域。',
  `discipline_code` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目所属学科的分类代码。',
  `fund_category` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目对应的基金或资助类别。',
  `funded_province` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目受资助机构所在的省份。',
  `participating_institution` json DEFAULT NULL COMMENT '参与项目研究或实施的机构信息。',
  `approval_year` int DEFAULT NULL COMMENT '项目获批立项的年份。',
  `approval_time` date DEFAULT NULL COMMENT '项目正式获批立项的时间。',
  `research_period` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目计划开展研究的时间期限。',
  `project_host` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目的主要负责人或主持人。',
  `participants` json DEFAULT NULL COMMENT '参与项目研究或实施的人员信息。',
  `keywords` json DEFAULT NULL COMMENT '描述项目研究主题的关键词。',
  `abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '项目申请书或标书中的摘要内容。',
  `final_report_abstract` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '项目结题报告中的摘要内容。',
  `project_page_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '项目详情页面的访问链接。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_zh_project_id` (`id`) USING BTREE,
  KEY `idx_ods_zh_project_project_number` (`project_number`) USING BTREE,
  KEY `idx_ods_zh_project_discipline_code` (`discipline_code`) USING BTREE,
  KEY `idx_ods_zh_project_approval_year` (`approval_year`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内项目信息表';

-- gkx.ods_zh_project_bak_20260710 definition

CREATE TABLE `ods_zh_project_bak_20260710` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '主键',
  `project_number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目编号',
  `title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目名称',
  `project_source` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目来源',
  `funded_institution` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '依托单位',
  `project_level` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目级别',
  `funded_amount` decimal(12,2) DEFAULT NULL COMMENT '资助金额',
  `discipline` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '学科',
  `discipline_code` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '学科代码',
  `fund_category` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '基金类别',
  `funded_province` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '资助省份',
  `participating_institution` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '参与单位',
  `approval_year` date DEFAULT NULL COMMENT '批准年度',
  `approval_time` date DEFAULT NULL COMMENT '批准日期',
  `research_period` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '研究周期',
  `project_host` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目负责人',
  `participants` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '参与人员',
  `keywords` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '关键词',
  `abstract` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '项目摘要',
  `final_report_abstract` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '结题摘要',
  `project_page_url` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目详情页',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-国内项目信息表';

-- gkx.ods_zh_project_output definition

CREATE TABLE `ods_zh_project_output` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '项目记录的唯一主键标识。',
  `total_outputs` int DEFAULT NULL COMMENT '项目产生的成果总数量。',
  `journal_articles_count` int DEFAULT NULL COMMENT '项目产出的期刊论文数量。',
  `conference_papers_count` int DEFAULT NULL COMMENT '项目产出的会议论文数量。',
  `degree_papers_count` int DEFAULT NULL COMMENT '项目产出的学位论文数量。',
  `patents_count` int DEFAULT NULL COMMENT '项目产出的专利数量。',
  `clinical_trials_count` int DEFAULT NULL COMMENT '项目产出的临床试验数量。',
  `books_count` int DEFAULT NULL COMMENT '项目产出的图书或专著数量。',
  `products_count` int DEFAULT NULL COMMENT '项目产出的产品数量。',
  `awards_count` int DEFAULT NULL COMMENT '项目获得的奖项数量。',
  `reports_count` int DEFAULT NULL COMMENT '项目产出的报告数量。',
  `other_outputs_count` int DEFAULT NULL COMMENT '项目产生的其他成果数量。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL COMMENT '逻辑删除标识，0未删除，1已删除',
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_zh_project_output_id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='国内项目-产出信息';

-- gkx.ods_zh_project_output_bak_20260710 definition

CREATE TABLE `ods_zh_project_output_bak_20260710` (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'UUID主键',
  `total_outputs` int DEFAULT NULL COMMENT '项目总产出数量',
  `journal_articles_count` int DEFAULT NULL COMMENT '期刊文章数量',
  `conference_papers_count` int DEFAULT NULL COMMENT '会议论文数量',
  `books_count` int DEFAULT NULL COMMENT '图书专著数量',
  `degree_papers_count` int DEFAULT NULL COMMENT '学位论文数量',
  `patents_count` int DEFAULT NULL COMMENT '专利数量',
  `clinical_trials_count` int DEFAULT NULL COMMENT '临床试验数量',
  `products_count` int DEFAULT NULL COMMENT '产品数量',
  `awards_count` int DEFAULT NULL COMMENT '奖项数量',
  `reports_count` int DEFAULT NULL COMMENT '报告数量',
  `other_outputs_count` int DEFAULT NULL COMMENT '其他产出数量',
  `output_journal_articles` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '期刊文章',
  `output_conference_papers` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '会议论文',
  `output_books` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '图书专著',
  `output_degree_papers` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '学位论文',
  `output_patents` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '专利',
  `output_clinical_trials` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '临床试验',
  `output_products` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '产品',
  `output_awards` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '奖项',
  `output_reports` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '报告',
  `output_other` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '其他成果',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='深势-国内项目产出信息表';

-- gkx.ods_zh_report definition

CREATE TABLE `ods_zh_report` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'MySQL自增主键',
  `report_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '中文报告记录的唯一主键标识。',
  `report_category` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标识报告所属的类别。',
  `title_cn` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '报告的中文标题名称。',
  `authors` text COLLATE utf8mb4_bin COMMENT '报告作者的姓名或信息列表。',
  `organization` text COLLATE utf8mb4_bin COMMENT '作者所属单位或报告完成单位名称。',
  `abstract_cn` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '报告内容的中文摘要信息。',
  `keywords_cn` text COLLATE utf8mb4_bin COMMENT '描述报告主题内容的中文关键词。',
  `report_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标识报告的具体类型。',
  `page_count` int DEFAULT NULL COMMENT '报告全文的总页数。',
  `preparation_time` date DEFAULT NULL COMMENT '报告编制完成或形成的时间。',
  `approval_year` int DEFAULT NULL COMMENT '报告相关项目获批立项的年份。',
  `related_literature` text COLLATE utf8mb4_bin COMMENT '与当前报告内容相关的文献信息。',
  `related_scholars` text COLLATE utf8mb4_bin COMMENT '与当前报告主题相关的学者信息。',
  `related_institutions` text COLLATE utf8mb4_bin COMMENT '与当前报告主题相关的机构信息。',
  `related_projects` text COLLATE utf8mb4_bin COMMENT '与当前报告内容相关的项目信息。',
  `source_org` text COLLATE utf8mb4_bin COMMENT '报告数据或内容的来源机构。',
  `visibility_scope` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '报告可被访问或查看的范围。',
  `project_annual_number` int DEFAULT NULL COMMENT '项目按年度管理的编号标识。',
  `contact_phone` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '报告相关联系人或单位的联系电话。',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '该条数据最近一次更新的时间',
  `creater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据新增操作员',
  `updater` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据更新操作员',
  `table_data_source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '技术字段，数据来源',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '逻辑删除标识，0未删除，1已删除',
  `source_url` varchar(128) COLLATE utf8mb4_bin DEFAULT NULL,
  `scholar_id` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `org_id` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `paper_id` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `project_id` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `file_path` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`pk_id`) USING BTREE,
  UNIQUE KEY `uk_ods_zh_report_report_id` (`report_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='中文科技报告信息表';

-- gkx.ods_zh_report_bak_20260710 definition

CREATE TABLE `ods_zh_report_bak_20260710` (
  `title` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `alternativeTitle` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `creator` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `creatOrorganization` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `prepareOrganization` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `publicScope` int DEFAULT NULL,
  `publicDate` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `delaypubliclyYears` int DEFAULT NULL,
  `note` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `abstractCn` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `proposalDate` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `downtime` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `keywordsCn` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `keywordsEn` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `abstractEn` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `projectName` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `projectSubjectName` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `competentOrg` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `responsiblePerson` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `startDate` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `endDate` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `linkmanName` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `linkmanEmail` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `lnkmanPhone` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `linkmanAddresss` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `fieldId` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `classification` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `kjbgType` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `ID` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='万方中文报告信息';

-- gkx.ods_zh_report_org definition

CREATE TABLE `ods_zh_report_org` (
  `org_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '机构id',
  `org_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '机构名称',
  `org_xydm` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '统一社会信用代码'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='中文科技报告机构信息';

-- gkx.ods_zh_report_paper definition

CREATE TABLE `ods_zh_report_paper` (
  `paper_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '论文id',
  `paper_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '论文标题',
  `paper_doi` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'doi编号',
  `report_source` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '报告来源',
  `report_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '报告id',
  `paper_source` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '论文来源'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='中文科技报告关联论文信息';

-- gkx.ods_zh_report_project definition

CREATE TABLE `ods_zh_report_project` (
  `project_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '项目id',
  `project_name` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '项目名称',
  `project_subject` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '项目主题',
  `project_type` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '项目类型',
  `project_number` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '项目编号',
  `report_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '报告id',
  `project_source` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '项目来源'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='中文科技报告关联项目信息';

-- gkx.ods_zh_report_scholar definition

CREATE TABLE `ods_zh_report_scholar` (
  `scholar_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '学者id',
  `scholar_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '学者名字',
  `scholar_unit` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '学者所属机构',
  `scholar_project` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '参与项目类型',
  `report_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '报告id',
  `report_source` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '报告来源'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='中文科技报告关联学者信息';