-- ============================================================
-- 要素库建表语句 (MySQL 8.0)
-- 来源: 数据需求分析/db 下各汇总表中以"要素库"结尾的 Sheet
-- 规则: 字符集 utf8mb4；表名统一以 dwd_ 开头；长 VARCHAR/TEXT 索引用前缀(255)；
--       JSON 列不建索引；列注释截断至 1000 字符；缺英文名的表/字段用拼音
-- 更新(基于新增文件): 中文论文/外文论文采用「数据库设计及数据质量核验方案」精化设计(19表);
--       人才重构为 6 表; 国内政策更新为 29 字段(dwd_zck_policy); 国内机构 reg_info 增 org_type、
--       删 rd_achiev_info; 新增维度/样例表 dwd_forg_industry_scope/dwd_innovation_carrier/dwd_macro_region_category
-- ============================================================
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------------------------------------
-- 表: dwd_series_metadata  (序列元数据)
-- 来源文件: 市场研究（金融、宏观行业、行业分析、产业链）数据汇总表v0601.xlsx | Sheet: 金融要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_series_metadata`;
CREATE TABLE `dwd_series_metadata` (
  `metadata_id` INT NOT NULL COMMENT '数列ID；数列的唯一标识符',
  `metadata_name` VARCHAR(1600) NOT NULL COMMENT '数列名称',
  `metadata_indicators` JSON NULL COMMENT '指标',
  `metadata_unit_id` VARCHAR(255) NULL COMMENT '单位ID；数列单位ID',
  `metadata_unit_name` VARCHAR(100) NULL COMMENT '单位名称；数列单位名称',
  `metadata_country_id` VARCHAR(2) NOT NULL COMMENT '国家ID；数列国家ID',
  `metadata_country_name` VARCHAR(100) NOT NULL COMMENT '国家名称；数列国家名称',
  `metadata_frequency_id` VARCHAR(1) NOT NULL COMMENT '频率ID；数列频率ID；值域: D - Daily W - Weekly M - Monthly Q - Quarterly H - Semi-annual Y - Annual Z - Quinquennially T - Decadal',
  `metadata_frequency_name` VARCHAR(50) NOT NULL COMMENT '频率名称；数列频率名称',
  `metadata_status_id` VARCHAR(1) NOT NULL COMMENT '状态ID；数列状态ID；值域: T - Active C - Discontinued B - Rebased',
  `metadata_status_name` VARCHAR(45) NOT NULL COMMENT '状态名称；数列状态名称',
  `metadata_source_id` VARCHAR(20) NULL COMMENT '来源ID；数据来源ID',
  `metadata_source_name` VARCHAR(400) NULL COMMENT '来源名称；数据来源名称',
  `metadata_startDate` VARCHAR(10) NOT NULL COMMENT '开始日期；第一个时间点的日期',
  `metadata_endDate` VARCHAR(10) NOT NULL COMMENT '最后日期；最后时间点的日期',
  KEY `idx_dwd_series_metadata_metadata_id` (`metadata_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='序列元数据';

-- ----------------------------------------------------------
-- 表: dwd_series_timepoints  (序列时间点)
-- 来源文件: 市场研究（金融、宏观行业、行业分析、产业链）数据汇总表v0601.xlsx | Sheet: 金融要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_series_timepoints`;
CREATE TABLE `dwd_series_timepoints` (
  `timePoints_value` DOUBLE NOT NULL COMMENT '时间点值；数据时间点值',
  `timePoints_date` VARCHAR(10) NOT NULL COMMENT '时间点日期；数据时间点日期'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='序列时间点';

-- ----------------------------------------------------------
-- 表: dwd_macro_index_data  (数据表)
-- 来源文件: 市场研究（金融、宏观行业、行业分析、产业链）数据汇总表v0601.xlsx | Sheet: 宏观行业要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_macro_index_data`;
CREATE TABLE `dwd_macro_index_data` (
  `rid` BIGINT NOT NULL COMMENT '主键 ID',
  `index_code` VARCHAR(50) NOT NULL COMMENT '指标代码',
  `occur_period` BIGINT NOT NULL COMMENT '数据期',
  `area_code` VARCHAR(32) NOT NULL COMMENT '区划代码',
  `dim_cal` VARCHAR(32) NOT NULL COMMENT '计算类型',
  `dim_dur` VARCHAR(32) NOT NULL COMMENT '时间特征',
  `index_value` DOUBLE NOT NULL COMMENT '值',
  `unit_use` VARCHAR(50) NOT NULL COMMENT '单位',
  `update_time` DATETIME NOT NULL COMMENT '数据更新时间',
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='数据表';

-- ----------------------------------------------------------
-- 表: dwd_document_metadata  (文档元数据)
-- 来源文件: 市场研究（金融、宏观行业、行业分析、产业链）数据汇总表v0601.xlsx | Sheet: 行业分析要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_document_metadata`;
CREATE TABLE `dwd_document_metadata` (
  `id` VARCHAR(255) NOT NULL COMMENT '文件ID；文件ID 唯一标识符',
  `format` VARCHAR(255) NOT NULL COMMENT '文件格式',
  `creationDate` VARCHAR(255) NOT NULL COMMENT '文件日期；文件创建日期',
  `companies_id` INT NULL COMMENT '公司代码',
  `companies_name` VARCHAR(255) NULL COMMENT '公司英文名称',
  `countryCodes` JSON NULL COMMENT '国家；国家代码',
  `topics_name` VARCHAR(255) NULL COMMENT '主题名字',
  `topics_code` VARCHAR(255) NULL COMMENT '主题代码',
  `sourceType_name` VARCHAR(255) NULL COMMENT '源类型名字；信息来源类型名称',
  `sourceType_code` VARCHAR(8) NULL COMMENT '源类型代码；信息来源类型代码',
  `documentSource_name` VARCHAR(255) NOT NULL COMMENT '数据源名字；信息来源名称',
  `documentSource_code` VARCHAR(24) NOT NULL COMMENT '数据源代码；信息来源代码',
  `contentTypes_name` VARCHAR(255) NULL COMMENT '报告类型名字；报告类型名称',
  `contentTypes_code` VARCHAR(8) NULL COMMENT '报告类型代码；值域: TA - Analysis/ Research TF - Financials and Annual Reports TV - Survey/Polls TJ - Analytical Commentary TC - Company official documents TN - News',
  `industries_code` VARCHAR(50) NULL COMMENT '行业代码；行业代码，如有',
  `industries_name` VARCHAR(255) NULL COMMENT '行业名称；行业名称，如有',
  `pages` INT NULL COMMENT '页数；报告页数',
  `title` VARCHAR(255) NOT NULL COMMENT '标题；文件标题',
  `body` VARCHAR(255) NULL COMMENT '正文',
  `abstract` VARCHAR(255) NULL COMMENT '文件摘要',
  `language` VARCHAR(2) NOT NULL COMMENT '语言；值域: en -English fr -French es -Spanish bg -Bulgarian ru -Russian pt -Portuguese zh -Chinese cs -Czech sk -Slovak hu -Hungarian id -Indonesian ro -Romanian ar -Arabic pl -Polish th -Thai tr -Turkish',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='文档元数据';

-- ----------------------------------------------------------
-- 表: dwd_industry_chain_info  (产业链图谱)
-- 来源文件: 市场研究（金融、宏观行业、行业分析、产业链）数据汇总表v0601.xlsx | Sheet: 产业链要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_industry_chain_info`;
CREATE TABLE `dwd_industry_chain_info` (
  `chain_code` VARCHAR(255) NOT NULL COMMENT '产业链代码；产业链唯一id，用于关联其它表。',
  `chain_name` VARCHAR(255) NOT NULL COMMENT '产业链名称',
  `node_id` VARCHAR(255) NOT NULL COMMENT '节点代码；产业链节点唯一id，用于关联其它表。',
  `node_name` VARCHAR(255) NOT NULL COMMENT '节点名称',
  `node_type` DOUBLE NOT NULL COMMENT '节点类型；1-大类节点：为构建图谱结构设置的虚拟节点，不直接关联企业，可通过其下属业务节点间接关联企业。 2-业务节点：具备实际业务含义的节点，在数据处理环节直接关联企业。 3 展示节点：与产业链相关性极弱，仅做图谱关系展示，不关联企业。；值域: 1,2，3',
  `level` DOUBLE NOT NULL COMMENT '节点层级；产业链节点分类层级中，节点所处层级。；值域: 1,2,3,4,5',
  `node_seq` DOUBLE NULL COMMENT '节点序号；同一父级节点下的子节点排序参考值。；值域: 1至20',
  `parent_id` VARCHAR(255) NULL COMMENT '父级节点代码；产业链节点唯一id，用于关联其它表。',
  `parent_name` VARCHAR(255) NULL COMMENT '父级节点名称',
  `node_imp_level` DOUBLE NULL COMMENT '节点重要性等级；产业链节点在整个产业链体系中重要性。1为重要性最高，5为重要性最低。仅适用于节点类型为2的业务节点。；值域: 1,2,3,4,5',
  `downstream_link_code` VARCHAR(255) NULL COMMENT '下游节点代码；产业链节点唯一id，用于关联其它表。',
  `node_stage` DOUBLE NULL COMMENT '节点环节；适用于上中下游型产业链，1-上游，2-中游，3-下游。；值域: 1,2,3',
  `node_path` TEXT NULL COMMENT '节点路径',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_industry_chain_i_chain_code` (`chain_code`),
  KEY `idx_dwd_industry_chain_i_node_id` (`node_id`),
  KEY `idx_dwd_industry_chain_i_node_imp_level` (`node_imp_level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='产业链图谱';

-- ----------------------------------------------------------
-- 表: dwd_org_industry_chain_dtl  (产业关联企业信息)
-- 来源文件: 市场研究（金融、宏观行业、行业分析、产业链）数据汇总表v0601.xlsx | Sheet: 产业链要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_industry_chain_dtl`;
CREATE TABLE `dwd_org_industry_chain_dtl` (
  `chain_code` VARCHAR(255) NOT NULL COMMENT '产业链代码；产业链唯一id，用于关联其它表。',
  `chain_name` VARCHAR(255) NOT NULL COMMENT '产业链名称',
  `node_id` VARCHAR(255) NOT NULL COMMENT '节点代码；产业链节点唯一id，用于关联其它表。',
  `node_name` VARCHAR(255) NOT NULL COMMENT '节点名称',
  `antitypic` VARCHAR(255) NOT NULL COMMENT '企业id；企业身份唯一id，用于关联其它表。',
  `credit_code` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `chain_score` DOUBLE NULL COMMENT '产业链评分',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_industry_cha_chain_code` (`chain_code`),
  KEY `idx_dwd_org_industry_cha_node_id` (`node_id`),
  KEY `idx_dwd_org_industry_cha_antitypic` (`antitypic`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='产业关联企业信息';

-- ----------------------------------------------------------
-- 表: dwd_org_industry_chain_prod_dtl  (产业链企业关联产品信息)
-- 来源文件: 市场研究（金融、宏观行业、行业分析、产业链）数据汇总表v0601.xlsx | Sheet: 产业链要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_industry_chain_prod_dtl`;
CREATE TABLE `dwd_org_industry_chain_prod_dtl` (
  `chain_code` VARCHAR(255) NOT NULL COMMENT '产业链代码；产业链唯一id，用于关联其它表。',
  `chain_name` VARCHAR(255) NOT NULL COMMENT '产业链名称',
  `antitypic` VARCHAR(255) NOT NULL COMMENT '企业id；企业身份唯一id，用于关联其它表。',
  `company_name` VARCHAR(500) NULL COMMENT '企业名称',
  `credit_code` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `tech_product` VARCHAR(255) NOT NULL COMMENT '主营产品名称',
  `tech_product_seq` DOUBLE NULL COMMENT '主营产品排序',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_industry_cha_chain_code` (`chain_code`),
  KEY `idx_dwd_org_industry_cha_antitypic` (`antitypic`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='产业链企业关联产品信息';

-- ----------------------------------------------------------
-- 表: dwd_org_industry_chain_pat_dtl  (产业链关联专利信息)
-- 来源文件: 市场研究（金融、宏观行业、行业分析、产业链）数据汇总表v0601.xlsx | Sheet: 产业链要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_industry_chain_pat_dtl`;
CREATE TABLE `dwd_org_industry_chain_pat_dtl` (
  `chain_code` VARCHAR(255) NOT NULL COMMENT '产业链代码；产业链唯一id，用于关联其它表。',
  `chain_name` VARCHAR(255) NOT NULL COMMENT '产业链名称',
  `node_id` VARCHAR(255) NOT NULL COMMENT '节点代码；产业链节点唯一id，用于关联其它表。',
  `node_name` VARCHAR(255) NOT NULL COMMENT '节点名称',
  `apno` VARCHAR(255) NOT NULL COMMENT '申请号；专利唯一id，用于关联专利对应企业信息。',
  `apdt` DATE NULL COMMENT '申请日',
  `pat_name` VARCHAR(500) NULL COMMENT '专利名称',
  `pn` VARCHAR(255) NULL COMMENT '公布(公告)号',
  `pbdt` DATE NULL COMMENT '公布(公告)日',
  `current_assignee` TEXT NULL COMMENT '申请(专利权)人',
  `inventors` TEXT NULL COMMENT '发明(设计)人',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_industry_cha_chain_code` (`chain_code`),
  KEY `idx_dwd_org_industry_cha_node_id` (`node_id`),
  KEY `idx_dwd_org_industry_cha_node_name` (`node_name`),
  KEY `idx_dwd_org_industry_cha_apno` (`apno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='产业链关联专利信息';

-- ----------------------------------------------------------
-- 表: dwd_industry_chain_news_info  (产业动态资讯)
-- 来源文件: 市场研究（金融、宏观行业、行业分析、产业链）数据汇总表v0601.xlsx | Sheet: 产业链要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_industry_chain_news_info`;
CREATE TABLE `dwd_industry_chain_news_info` (
  `chain_code` VARCHAR(255) NOT NULL COMMENT '产业链代码；产业链唯一id，用于关联其它表。',
  `chain_name` VARCHAR(255) NOT NULL COMMENT '产业链名称',
  `news_id` VARCHAR(255) NOT NULL COMMENT '资讯id；资讯唯一id',
  `title` VARCHAR(255) NULL COMMENT '标题',
  `relaese_date` DATE NULL COMMENT '发布时间',
  `summary` TEXT NULL COMMENT '摘要',
  `source` VARCHAR(255) NULL COMMENT '来源',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_industry_chain_n_chain_code` (`chain_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='产业动态资讯';

-- ----------------------------------------------------------
-- 表: dwd_org_reg_info  (机构基本信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_reg_info`;
CREATE TABLE `dwd_org_reg_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `org_type` VARCHAR(255) NULL COMMENT '机构类型',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `province` VARCHAR(255) NULL COMMENT '所在省份',
  `city` VARCHAR(255) NULL COMMENT '所在城市',
  `address` TEXT NULL COMMENT '公司地址',
  `addr_lng` VARCHAR(255) NULL COMMENT '地址对应经度',
  `addr_lat` VARCHAR(255) NULL COMMENT '地址对应维度',
  `postal_code` VARCHAR(255) NULL COMMENT '邮政编码',
  `phone` VARCHAR(255) NULL COMMENT '联系电话',
  `email` TEXT NULL COMMENT '电子邮箱',
  `lerep` VARCHAR(255) NULL COMMENT '法人名字',
  `org_size` VARCHAR(255) NULL COMMENT '企业规模',
  `registration_org` VARCHAR(255) NULL COMMENT '登记机关',
  `incorporation_year` DOUBLE NULL COMMENT '成立年份',
  `incorporation_date` DATE NULL COMMENT '成立日期',
  `start_date` VARCHAR(255) NULL COMMENT '经营期限自',
  `end_date` VARCHAR(255) NULL COMMENT '经营期限至',
  `listing_status` VARCHAR(255) NULL COMMENT '上市状态',
  `listing_date` DATE NULL COMMENT '上市日期',
  `registered_capital_value` DOUBLE NULL COMMENT '注册资本(本币元)',
  `capital_currency_code` VARCHAR(255) NULL COMMENT '资本货币代码；值域: qhdata_standard.dim_currency_code；货币代码映射对应的货币名称。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_reg_info_org_id` (`org_id`),
  KEY `idx_dwd_org_reg_info_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='机构基本信息';

-- ----------------------------------------------------------
-- 表: dwd_org_shareholder_info  (股东信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_shareholder_info`;
CREATE TABLE `dwd_org_shareholder_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `inv_org_id` VARCHAR(255) NULL COMMENT '股东id；机构身份唯一id，用于关联其它表。',
  `owners_name` VARCHAR(255) NOT NULL COMMENT '股东名称',
  `owners_type` VARCHAR(255) NULL COMMENT '股东类型',
  `ownership_percentage` DOUBLE NULL COMMENT '所有权占比(%)',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_shareholder__org_id` (`org_id`),
  KEY `idx_dwd_org_shareholder__external_id` (`external_id`),
  KEY `idx_dwd_org_shareholder__inv_org_id` (`inv_org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='股东信息';

-- ----------------------------------------------------------
-- 表: dwd_org_executive_info  (高管信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_executive_info`;
CREATE TABLE `dwd_org_executive_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `executives_name` VARCHAR(255) NOT NULL COMMENT '高管姓名',
  `executives_position` VARCHAR(255) NULL COMMENT '职位名称',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_executive_in_org_id` (`org_id`),
  KEY `idx_dwd_org_executive_in_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='高管信息';

-- ----------------------------------------------------------
-- 表: dwd_org_org_product_info  (经营信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_org_product_info`;
CREATE TABLE `dwd_org_org_product_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `industry_class` VARCHAR(255) NOT NULL COMMENT '公司行业分类；值域: qhdata_standard.map_industry_code_2017；行业代码映射行业门类名称、大类名称、中类名称、小类名称。',
  `main_activities` TEXT NULL COMMENT '公司经营范围',
  `description` TEXT NULL COMMENT '业务描述',
  `main_prod` VARCHAR(255) NULL COMMENT '主要产品',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_org_product__org_id` (`org_id`),
  KEY `idx_dwd_org_org_product__external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='经营信息';

-- ----------------------------------------------------------
-- 表: dwd_org_annual_financial_info  (年报财务信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_annual_financial_info`;
CREATE TABLE `dwd_org_annual_financial_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `year` DOUBLE NOT NULL COMMENT '年报年度',
  `total_assets` VARCHAR(255) NULL COMMENT '资产总额',
  `total_liabilities` VARCHAR(255) NULL COMMENT '负债总额',
  `operating_revenue` VARCHAR(255) NULL COMMENT '营业收入',
  `main_business_revenue` VARCHAR(255) NULL COMMENT '主营业务收入',
  `total_profit` VARCHAR(255) NULL COMMENT '利润总额',
  `pure_profit` VARCHAR(255) NULL COMMENT '净利润',
  `total_tax_paid` VARCHAR(255) NULL COMMENT '纳税总额',
  `owners_equity` VARCHAR(255) NULL COMMENT '所有者权益合计',
  `employees_number` VARCHAR(255) NULL COMMENT '从业人数',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_annual_finan_org_id` (`org_id`),
  KEY `idx_dwd_org_annual_finan_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='年报财务信息';

-- ----------------------------------------------------------
-- 表: dwd_org_important_news_info  (重点资讯)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_important_news_info`;
CREATE TABLE `dwd_org_important_news_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `news_title` TEXT NULL COMMENT '资讯标题',
  `news_date` DATE NULL COMMENT '资讯日期',
  `news_content` TEXT NULL COMMENT '资讯内容',
  `original_textlink` TEXT NULL COMMENT '咨询原文链接',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_important_ne_org_id` (`org_id`),
  KEY `idx_dwd_org_important_ne_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点资讯';

-- ----------------------------------------------------------
-- 表: dwd_org_changerecord_info  (工商变更信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_changerecord_info`;
CREATE TABLE `dwd_org_changerecord_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `update_content` VARCHAR(255) NOT NULL COMMENT '变更类型',
  `current_name` TEXT NULL COMMENT '变更前内容',
  `update_name` TEXT NULL COMMENT '变更后内容',
  `update_date` DATE NOT NULL COMMENT '变更日期',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_changerecord_org_id` (`org_id`),
  KEY `idx_dwd_org_changerecord_external_id` (`external_id`),
  KEY `idx_dwd_org_changerecord_update_date` (`update_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='工商变更信息';

-- ----------------------------------------------------------
-- 表: dwd_org_merger_acquisition_info  (并购事件)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_merger_acquisition_info`;
CREATE TABLE `dwd_org_merger_acquisition_info` (
  `acquiring_org_id` VARCHAR(255) NOT NULL COMMENT '发起收购企业id；机构身份唯一id，用于关联其它表。',
  `acquiring_name` VARCHAR(255) NOT NULL COMMENT '发起收购企业名称',
  `acquired_org_id` VARCHAR(255) NOT NULL COMMENT '被收购企业id；机构身份唯一id，用于关联其它表。',
  `acquired_name` VARCHAR(255) NOT NULL COMMENT '被收购企业名称',
  `ma_amount` DOUBLE NULL COMMENT '并购金额(元)',
  `currency_code` VARCHAR(255) NULL COMMENT '并购金额币种；值域: qhdata_standard.dim_currency_code；货币代码映射对应的货币名称。',
  KEY `idx_dwd_org_merger_acqui_acquiring_org_id` (`acquiring_org_id`),
  KEY `idx_dwd_org_merger_acqui_acquired_org_id` (`acquired_org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='并购事件';

-- ----------------------------------------------------------
-- 表: dwd_org_financing_info  (融资事件)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_financing_info`;
CREATE TABLE `dwd_org_financing_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `funding_round` VARCHAR(255) NULL COMMENT '融资轮次',
  `funding_amount` DOUBLE NULL COMMENT '获投金额(元)',
  `funding_currency_code` VARCHAR(255) NULL COMMENT '金额币种',
  `post_valuation` DOUBLE NULL COMMENT '投后估值',
  `completion_date` DATE NULL COMMENT '融资完成时间',
  `investors_name` TEXT NOT NULL COMMENT '投资方列表',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_financing_in_org_id` (`org_id`),
  KEY `idx_dwd_org_financing_in_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='融资事件';

-- ----------------------------------------------------------
-- 表: dwd_org_invest_info  (投资事件)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_invest_info`;
CREATE TABLE `dwd_org_invest_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `inv_org_id` VARCHAR(255) NOT NULL COMMENT '被投企业id；机构身份唯一id，用于关联其它表。',
  `inv_name` VARCHAR(255) NOT NULL COMMENT '被投资企业名称',
  `inv_external_id` VARCHAR(255) NULL COMMENT '被投资企业统一社会信用代码',
  `investment_amount` DOUBLE NULL COMMENT '投资金额(元)',
  `investment_ratio` DOUBLE NULL COMMENT '股权占比(%)',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_invest_info_org_id` (`org_id`),
  KEY `idx_dwd_org_invest_info_external_id` (`external_id`),
  KEY `idx_dwd_org_invest_info_inv_org_id` (`inv_org_id`),
  KEY `idx_dwd_org_invest_info_inv_external_id` (`inv_external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='投资事件';

-- ----------------------------------------------------------
-- 表: dwd_org_bid_info  (招投标事件)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_bid_info`;
CREATE TABLE `dwd_org_bid_info` (
  `tender_org_id` VARCHAR(255) NOT NULL COMMENT '采购单位id；机构身份唯一id，用于关联其它表。',
  `tender_name_cn` VARCHAR(255) NOT NULL COMMENT '采购单位名称',
  `tender_external_id` VARCHAR(255) NULL COMMENT '采购单位统一社会信用代码',
  `winner_org_id` VARCHAR(255) NOT NULL COMMENT '中标单位id；机构身份唯一id，用于关联其它表。',
  `winner_name_cn` VARCHAR(255) NOT NULL COMMENT '中标单位名称',
  `winner_external_id` VARCHAR(255) NULL COMMENT '中标单位统一社会信用代码',
  `announcement_title` TEXT NULL COMMENT '公告标题',
  `announcement_content` TEXT NULL COMMENT '中标成交信息',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_bid_info_tender_org_id` (`tender_org_id`),
  KEY `idx_dwd_org_bid_info_tender_external_id` (`tender_external_id`),
  KEY `idx_dwd_org_bid_info_winner_org_id` (`winner_org_id`),
  KEY `idx_dwd_org_bid_info_winner_external_id` (`winner_external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='招投标事件';

-- ----------------------------------------------------------
-- 表: dwd_org_recruit_info  (招聘信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_recruit_info`;
CREATE TABLE `dwd_org_recruit_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `job_title` VARCHAR(255) NULL COMMENT '岗位',
  `job_description` TEXT NULL COMMENT '工作描述',
  `work_place` TEXT NULL COMMENT '工作地点',
  `release_date` DATE NULL COMMENT '发布日期',
  `hiring_number` DOUBLE NULL COMMENT '招聘人数',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_recruit_info_org_id` (`org_id`),
  KEY `idx_dwd_org_recruit_info_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='招聘信息';

-- ----------------------------------------------------------
-- 表: dwd_org_hels_info  (高校/科研机构信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_hels_info`;
CREATE TABLE `dwd_org_hels_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '高校id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `org_name` VARCHAR(255) NOT NULL COMMENT '高校/科研机构名称(中文)',
  `org_name_en` VARCHAR(255) NULL COMMENT '高校/科研机构名称(英文)',
  `org_desc` TEXT NULL COMMENT '高校/科研机构描述',
  `est_year` DATE NULL COMMENT '建立时间',
  `address` TEXT NULL COMMENT '地址(国家、区域、城市)',
  `addr_lng` VARCHAR(255) NULL COMMENT '地址对应经度',
  `addr_lat` VARCHAR(255) NULL COMMENT '地址对应维度',
  `province` VARCHAR(255) NULL COMMENT '地址所在省',
  `city` VARCHAR(255) NULL COMMENT '地址所在市',
  `univ_type` VARCHAR(255) NULL COMMENT '高校类型',
  `web_link` TEXT NULL COMMENT '官方网址',
  `postal_code` VARCHAR(255) NULL COMMENT '邮政编码',
  `email` TEXT NULL COMMENT '电子邮箱',
  `contact_number` VARCHAR(255) NULL COMMENT '联系电话',
  `fax_number` VARCHAR(255) NULL COMMENT '传真号码',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_hels_info_org_id` (`org_id`),
  KEY `idx_dwd_org_hels_info_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='高校/科研机构信息';

-- ----------------------------------------------------------
-- 表: dwd_org_tag_info  (机构标签表)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_tag_info`;
CREATE TABLE `dwd_org_tag_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `org_tag` VARCHAR(255) NOT NULL COMMENT '企业标签',
  `tag_level` VARCHAR(255) NOT NULL COMMENT '级别',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_tag_info_org_id` (`org_id`),
  KEY `idx_dwd_org_tag_info_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='机构标签表';

-- ----------------------------------------------------------
-- 表: dwd_org_stock_base  (上市企业基本信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_stock_base`;
CREATE TABLE `dwd_org_stock_base` (
  `stock_code` VARCHAR(255) NOT NULL COMMENT '股票代码',
  `stock_noun` VARCHAR(255) NULL COMMENT '股票简称',
  `stock_type` VARCHAR(255) NULL COMMENT '上市板块',
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `listed_date` DATE NULL COMMENT '上市日期',
  `listed_status` VARCHAR(255) NULL COMMENT '上市状态',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_stock_base_stock_code` (`stock_code`),
  KEY `idx_dwd_org_stock_base_org_id` (`org_id`),
  KEY `idx_dwd_org_stock_base_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='上市企业基本信息';

-- ----------------------------------------------------------
-- 表: dwd_org_stock_finance_info  (上市企业主要财务指标)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_stock_finance_info`;
CREATE TABLE `dwd_org_stock_finance_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id；机构身份唯一id，用于关联其它表。',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `stock_code` VARCHAR(255) NOT NULL COMMENT '股票代码',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `occur_period` VARCHAR(255) NOT NULL COMMENT '数据期',
  `total_assets` DOUBLE NULL COMMENT '资产总额(元)',
  `fixed_assets` DOUBLE NULL COMMENT '固定资产总额(元)',
  `total_liabilities` DOUBLE NULL COMMENT '负债总额(元)',
  `operating_revenue` DOUBLE NULL COMMENT '营业收入(元)',
  `main_business_revenue` DOUBLE NULL COMMENT '主营业务收入(元)',
  `total_profit` DOUBLE NULL COMMENT '利润总额(元)',
  `pure_profit` DOUBLE NULL COMMENT '净利润(元)',
  `total_tax_paid` DOUBLE NULL COMMENT '纳税总额(元)',
  `oper_cash_flow` DOUBLE NULL COMMENT '经营活动现金流(元)',
  `owners_equity` DOUBLE NULL COMMENT '所有者权益合计(元)',
  `employees_number` DOUBLE NULL COMMENT '从业人数',
  `research_development_amount` DOUBLE NULL COMMENT '研发投入金额(元)',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_stock_financ_org_id` (`org_id`),
  KEY `idx_dwd_org_stock_financ_stock_code` (`stock_code`),
  KEY `idx_dwd_org_stock_financ_external_id` (`external_id`),
  KEY `idx_dwd_org_stock_financ_occur_period` (`occur_period`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='上市企业主要财务指标';

-- ----------------------------------------------------------
-- 表: dwd_org_company_abnormal  (经营异常)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_company_abnormal`;
CREATE TABLE `dwd_org_company_abnormal` (
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `abnormal_id` VARCHAR(255) NOT NULL COMMENT '经营异常记录id；经营异常记录唯一标识id。',
  `abn_reason` TEXT NULL COMMENT '列入原因',
  `abn_date` DATE NULL COMMENT '列入时间',
  `abn_org` VARCHAR(255) NULL COMMENT '列入机关',
  `remove_reason` TEXT NULL COMMENT '移除原因',
  `remove_date` DATE NULL COMMENT '移除时间',
  `remove_org` VARCHAR(255) NULL COMMENT '移除机关',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标记',
  `status` VARCHAR(255) NULL COMMENT '状态',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；值域: 否',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；值域: 否',
  KEY `idx_dwd_org_company_abno_org_id` (`org_id`),
  KEY `idx_dwd_org_company_abno_external_id` (`external_id`),
  KEY `idx_dwd_org_company_abno_abnormal_id` (`abnormal_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='经营异常';

-- ----------------------------------------------------------
-- 表: dwd_org_company_punish  (行政处罚)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_company_punish`;
CREATE TABLE `dwd_org_company_punish` (
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `penalty_id` VARCHAR(255) NOT NULL COMMENT '行政处罚记录id；行政处罚记录唯一标识id。',
  `decision_no` VARCHAR(255) NULL COMMENT '决定书文号',
  `violation_type` TEXT NULL COMMENT '违法行为类型',
  `penalty_content` TEXT NULL COMMENT '行政处罚内容',
  `decision_org` VARCHAR(255) NULL COMMENT '决定机关',
  `penalty_date` DATE NULL COMMENT '处罚决定日期',
  `public_date` DATE NULL COMMENT '公示日期',
  `penalty_basis` TEXT NULL COMMENT '处罚依据',
  `violation_fact` TEXT NULL COMMENT '主要违法事实',
  `penalty_type` VARCHAR(255) NULL COMMENT '处罚种类',
  `fine_amount` DOUBLE NULL COMMENT '罚款金额',
  `confiscate_amount` DOUBLE NULL COMMENT '没收金额',
  `license_info` TEXT NULL COMMENT '暂扣或吊销证照名称及编号',
  `validity_period` VARCHAR(255) NULL COMMENT '处罚有效期',
  `public_deadline` DATE NULL COMMENT '公示截止日期',
  `remark` TEXT NULL COMMENT '备注',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标记',
  `status` VARCHAR(255) NULL COMMENT '状态',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_company_puni_org_id` (`org_id`),
  KEY `idx_dwd_org_company_puni_external_id` (`external_id`),
  KEY `idx_dwd_org_company_puni_penalty_id` (`penalty_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='行政处罚';

-- ----------------------------------------------------------
-- 表: dwd_org_company_illegal  (严重违法)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_company_illegal`;
CREATE TABLE `dwd_org_company_illegal` (
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `sv_id` VARCHAR(255) NOT NULL COMMENT '严重违法记录id；严重违法记录唯一标识id。',
  `category` VARCHAR(255) NULL COMMENT '类别',
  `abn_reason` TEXT NULL COMMENT '列入原因',
  `abn_date` DATE NULL COMMENT '列入时间',
  `abn_org` VARCHAR(255) NULL COMMENT '列入机关',
  `remove_reason` TEXT NULL COMMENT '移除原因',
  `remove_date` DATE NULL COMMENT '移除时间',
  `remove_org` VARCHAR(255) NULL COMMENT '移除机关',
  `status` VARCHAR(255) NULL COMMENT '状态',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标记',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_company_ille_org_id` (`org_id`),
  KEY `idx_dwd_org_company_ille_external_id` (`external_id`),
  KEY `idx_dwd_org_company_ille_sv_id` (`sv_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='严重违法';

-- ----------------------------------------------------------
-- 表: dwd_org_risk_tax_punish  (税收违法)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_risk_tax_punish`;
CREATE TABLE `dwd_org_risk_tax_punish` (
  `taxpayer_name` VARCHAR(255) NOT NULL COMMENT '纳税人名称；纳税人登记名称。',
  `tax_vio_id` VARCHAR(255) NOT NULL COMMENT '唯一索引id；税收违法记录唯一标识id。',
  `report_period` VARCHAR(255) NULL COMMENT '案件上报期',
  `taxpayer_id` VARCHAR(255) NULL COMMENT '纳税人识别码',
  `org_code` VARCHAR(255) NULL COMMENT '组织机构代码',
  `reg_address` TEXT NULL COMMENT '注册地址',
  `publish_date` DATE NULL COMMENT '发布日期',
  `legal_name` VARCHAR(255) NULL COMMENT '法定代表人或者负责人姓名',
  `legal_gender` VARCHAR(255) NULL COMMENT '法定代表人或者负责人性别',
  `legal_id_type` VARCHAR(255) NULL COMMENT '法定代表人或者负责人证件类型',
  `legal_id_no` VARCHAR(255) NULL COMMENT '法定代表人或者负责人证件号码',
  `finance_name` VARCHAR(255) NULL COMMENT '负有直接责任的财务负责人姓名',
  `finance_gender` VARCHAR(255) NULL COMMENT '负有直接责任的财务负责人性别',
  `finance_id_type` VARCHAR(255) NULL COMMENT '负有直接责任的财务负责人证件类型',
  `finance_id_no` VARCHAR(255) NULL COMMENT '负有直接责任的财务负责人证件号码',
  `agency_info` TEXT NULL COMMENT '负有直接责任的中介机构信息及其从业人员信息',
  `case_type` VARCHAR(255) NULL COMMENT '案件性质',
  `illegal_fact` TEXT NULL COMMENT '主要违法事实',
  `punish_basis` TEXT NULL COMMENT '相关法律依据及税务处理处罚情况',
  `tax_authority` VARCHAR(255) NULL COMMENT '所属税务机关',
  `original_link` TEXT NULL COMMENT '数据原始连接',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标志',
  `original_source` VARCHAR(255) NULL COMMENT '原始数据来源',
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `is_history` VARCHAR(255) NULL COMMENT '是否历史；是否历史记录，0正常；1历史。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_risk_tax_pun_tax_vio_id` (`tax_vio_id`),
  KEY `idx_dwd_org_risk_tax_pun_org_id` (`org_id`),
  KEY `idx_dwd_org_risk_tax_pun_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='税收违法';

-- ----------------------------------------------------------
-- 表: dwd_org_opt_judicial_case  (司法案件)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_opt_judicial_case`;
CREATE TABLE `dwd_org_opt_judicial_case` (
  `company_name` VARCHAR(255) NOT NULL COMMENT '企业名称；企业登记名称。',
  `reg_no` VARCHAR(255) NULL COMMENT '注册号',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `case_id` VARCHAR(255) NOT NULL COMMENT '司法案件唯一标识；司法案件记录唯一标识id。',
  `case_title` TEXT NULL COMMENT '案件标题',
  `case_type_tag` VARCHAR(255) NULL COMMENT '案件类型标签',
  `case_no` VARCHAR(255) NULL COMMENT '案号',
  `case_cause` VARCHAR(255) NULL COMMENT '案由',
  `case_role` VARCHAR(255) NULL COMMENT '案件身份',
  `current_procedure` VARCHAR(255) NULL COMMENT '当前审理程序',
  `procedure_date` DATE NULL COMMENT '当前审理程序日期',
  `data_use_flag` VARCHAR(255) NULL COMMENT '数据使用标识',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_opt_judicial_external_id` (`external_id`),
  KEY `idx_dwd_org_opt_judicial_org_id` (`org_id`),
  KEY `idx_dwd_org_opt_judicial_case_id` (`case_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='司法案件';

-- ----------------------------------------------------------
-- 表: dwd_org_risk_shixin  (失信被执行人)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_risk_shixin`;
CREATE TABLE `dwd_org_risk_shixin` (
  `dishonest_id` VARCHAR(255) NULL COMMENT '失信被执行人id；失信被执行人记录唯一标识id。',
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `official_id` VARCHAR(255) NULL COMMENT '官网id',
  `case_no` VARCHAR(255) NOT NULL COMMENT '案号',
  `dishonest_name` VARCHAR(255) NULL COMMENT '失信人名称',
  `gender` VARCHAR(255) NULL COMMENT '性别',
  `age` VARCHAR(255) NULL COMMENT '年龄',
  `credit_code` VARCHAR(255) NULL COMMENT '统一信用代码',
  `reg_no` VARCHAR(255) NULL COMMENT '企业注册号',
  `display_id_no` VARCHAR(255) NULL COMMENT '展示用证件号码',
  `legal_person` VARCHAR(255) NULL COMMENT '法定代表人或负责人',
  `exec_court` VARCHAR(255) NULL COMMENT '执行法院',
  `province_id` VARCHAR(255) NULL COMMENT '省份id；省份id。',
  `province` VARCHAR(255) NULL COMMENT '省份',
  `dishonest_type` VARCHAR(255) NULL COMMENT '失信人类型',
  `exec_basis_no` VARCHAR(255) NULL COMMENT '执行依据文号',
  `exec_basis_org` VARCHAR(255) NULL COMMENT '做出执行依据单位',
  `legal_obligation` TEXT NULL COMMENT '生效法律文书确定的义务',
  `fulfillment_status` TEXT NULL COMMENT '被执行人的履行情况',
  `dishonest_behavior` TEXT NULL COMMENT '失信被执行人行为具体情形',
  `publish_date` DATE NULL COMMENT '发布时间',
  `filing_date` DATE NULL COMMENT '立案时间',
  `exec_part` VARCHAR(255) NULL COMMENT '执行部分',
  `unexec_part` VARCHAR(255) NULL COMMENT '未执行部分',
  `is_history` VARCHAR(255) NULL COMMENT '是否历史数据',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标记',
  `is_hidden` VARCHAR(255) NULL COMMENT '是否不展示',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_risk_shixin_dishonest_id` (`dishonest_id`),
  KEY `idx_dwd_org_risk_shixin_org_id` (`org_id`),
  KEY `idx_dwd_org_risk_shixin_external_id` (`external_id`),
  KEY `idx_dwd_org_risk_shixin_official_id` (`official_id`),
  KEY `idx_dwd_org_risk_shixin_province_id` (`province_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='失信被执行人';

-- ----------------------------------------------------------
-- 表: dwd_org_risk_zhixing  (被执行人)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_risk_zhixing`;
CREATE TABLE `dwd_org_risk_zhixing` (
  `exec_person_id` VARCHAR(255) NOT NULL COMMENT '唯一索引id；被执行人记录唯一标识id。',
  `exec_person_type` VARCHAR(255) NULL COMMENT '被执行人类型',
  `exec_person_name` VARCHAR(255) NULL COMMENT '被执行人名称',
  `gender` VARCHAR(255) NULL COMMENT '性别',
  `id_no` VARCHAR(255) NULL COMMENT '证件号码',
  `exec_court` VARCHAR(255) NULL COMMENT '执行法院',
  `case_no` VARCHAR(255) NULL COMMENT '案号',
  `exec_basis_no` VARCHAR(255) NULL COMMENT '执行依据文号',
  `exec_status` VARCHAR(255) NULL COMMENT '执行状态',
  `exec_target` VARCHAR(255) NULL COMMENT '执行标的',
  `web_id` VARCHAR(255) NULL COMMENT '执行信息公开网id',
  `filing_date` DATE NULL COMMENT '立案时间',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标记',
  `is_hidden` VARCHAR(255) NULL COMMENT '是否不展示',
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_risk_zhixing_exec_person_id` (`exec_person_id`),
  KEY `idx_dwd_org_risk_zhixing_exec_basis_no` (`exec_basis_no`),
  KEY `idx_dwd_org_risk_zhixing_web_id` (`web_id`),
  KEY `idx_dwd_org_risk_zhixing_org_id` (`org_id`),
  KEY `idx_dwd_org_risk_zhixing_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='被执行人';

-- ----------------------------------------------------------
-- 表: dwd_org_risk_xianxiao  (限制高消费)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_risk_xianxiao`;
CREATE TABLE `dwd_org_risk_xianxiao` (
  `xhfgk_id` VARCHAR(255) NULL COMMENT '限制高消费官网id；限制高消费官网/平台原始id。',
  `rhc_person_name` VARCHAR(255) NOT NULL COMMENT '限制高消费人员名称',
  `filing_date` DATE NULL COMMENT '立案时间',
  `case_no` VARCHAR(255) NOT NULL COMMENT '案号',
  `gender` VARCHAR(255) NULL COMMENT '性别',
  `company_info` TEXT NULL COMMENT '企业信息',
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `company_cert_no` VARCHAR(255) NULL COMMENT '企业证件号',
  `xhfgk_doc_url` TEXT NULL COMMENT '限制高消费令文件url',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标记',
  `is_history` VARCHAR(255) NULL COMMENT '是否是历史限制高消费',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_risk_xianxia_xhfgk_id` (`xhfgk_id`),
  KEY `idx_dwd_org_risk_xianxia_org_id` (`org_id`),
  KEY `idx_dwd_org_risk_xianxia_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='限制高消费';

-- ----------------------------------------------------------
-- 表: dwd_org_risk_lawsuit  (裁判文书)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_risk_lawsuit`;
CREATE TABLE `dwd_org_risk_lawsuit` (
  `judgment_doc_id` VARCHAR(255) NOT NULL COMMENT '裁判文书网文书id；裁判文书网文书唯一标识id。',
  `defendant` VARCHAR(255) NULL COMMENT '被告',
  `case_no` VARCHAR(255) NULL COMMENT '案号',
  `case_type_code` VARCHAR(255) NULL COMMENT '案件类型编码',
  `case_type` VARCHAR(255) NULL COMMENT '案件类型',
  `doc_type_code` VARCHAR(255) NULL COMMENT '文书类型编码',
  `doc_type` VARCHAR(255) NULL COMMENT '文书类型',
  `province` VARCHAR(255) NULL COMMENT '省份',
  `city` VARCHAR(255) NULL COMMENT '地市',
  `district` VARCHAR(255) NULL COMMENT '区县',
  `main_doc_id` VARCHAR(255) NULL COMMENT '主表docid',
  `court_name` VARCHAR(255) NULL COMMENT '法院名称',
  `trial_procedure` VARCHAR(255) NULL COMMENT '审理程序名称',
  `judgment_year` DOUBLE NULL COMMENT '裁判年份',
  `judgment_date` DATE NULL COMMENT '裁判日期',
  `case_cause` VARCHAR(255) NULL COMMENT '案由',
  `doc_title` TEXT NULL COMMENT '文书标题',
  `doc_full_text` TEXT NULL COMMENT '文书全文',
  `publish_date` DATE NULL COMMENT '公布日期',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标志',
  `original_url` TEXT NULL COMMENT '原始连接URL',
  `plaintiff` VARCHAR(255) NULL COMMENT '原告',
  `is_hidden` VARCHAR(255) NULL COMMENT '是否不展示',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_risk_lawsuit_judgment_doc_id` (`judgment_doc_id`),
  KEY `idx_dwd_org_risk_lawsuit_main_doc_id` (`main_doc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='裁判文书';

-- ----------------------------------------------------------
-- 表: dwd_org_risk_court_filed_case  (法院立案)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_risk_court_filed_case`;
CREATE TABLE `dwd_org_risk_court_filed_case` (
  `case_unique_id` VARCHAR(255) NOT NULL COMMENT '案件唯一id；案件唯一标识id。',
  `case_no` VARCHAR(255) NULL COMMENT '案号',
  `norm_case_no` VARCHAR(255) NULL COMMENT '归一化案号',
  `case_cause` VARCHAR(255) NULL COMMENT '案由',
  `trial_procedure` VARCHAR(255) NULL COMMENT '审理程序',
  `case_status` VARCHAR(255) NULL COMMENT '案件状态',
  `norm_case_status` VARCHAR(255) NULL COMMENT '归一化后案件状态',
  `filing_date` DATE NULL COMMENT '立案日期',
  `closing_date` DATE NULL COMMENT '结案日期',
  `hearing_date` DATE NULL COMMENT '开庭日期',
  `court_name` VARCHAR(255) NULL COMMENT '法院',
  `undertaking_dept` VARCHAR(255) NULL COMMENT '承办部门',
  `judge` VARCHAR(255) NULL COMMENT '法官',
  `assistant_judge` VARCHAR(255) NULL COMMENT '助理法官',
  `party_info` TEXT NULL COMMENT '当事人信息',
  `court_province` VARCHAR(255) NULL COMMENT '法院所在省',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标志',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_risk_court_f_case_unique_id` (`case_unique_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='法院立案';

-- ----------------------------------------------------------
-- 表: dwd_org_risk_lawsuit_list  (裁判文书当事人)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_risk_lawsuit_list`;
CREATE TABLE `dwd_org_risk_lawsuit_list` (
  `main_doc_id` VARCHAR(255) NOT NULL COMMENT '主表docid；主表docid，关联裁判文书表。',
  `party_identity` VARCHAR(255) NULL COMMENT '当事人身份',
  `party_role_type` VARCHAR(255) NULL COMMENT '当事人角色类型',
  `party_type` VARCHAR(255) NULL COMMENT '当事人类型',
  `related_person_name` VARCHAR(255) NULL COMMENT '相关人名称',
  `doc_publish_date` DATE NULL COMMENT '文书公布日期',
  `case_cause` VARCHAR(255) NULL COMMENT '案由',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标志',
  `is_hidden` VARCHAR(255) NULL COMMENT '是否不展示',
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_risk_lawsuit_main_doc_id` (`main_doc_id`),
  KEY `idx_dwd_org_risk_lawsuit_org_id` (`org_id`),
  KEY `idx_dwd_org_risk_lawsuit_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='裁判文书当事人';

-- ----------------------------------------------------------
-- 表: dwd_org_risk_court_filed_case_litigant  (法院立案当事人)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_risk_court_filed_case_litigant`;
CREATE TABLE `dwd_org_risk_court_filed_case_litigant` (
  `case_unique_id` VARCHAR(255) NOT NULL COMMENT '案件唯一id；案件唯一标识id，关联法院立案表。',
  `filing_date` DATE NULL COMMENT '立案日期',
  `party_name` VARCHAR(255) NULL COMMENT '当事人名称',
  `party_role` VARCHAR(255) NULL COMMENT '当事人角色',
  `classified_org_type` VARCHAR(255) NULL COMMENT '归类后企业类型',
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标志',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_risk_court_f_case_unique_id` (`case_unique_id`),
  KEY `idx_dwd_org_risk_court_f_org_id` (`org_id`),
  KEY `idx_dwd_org_risk_court_f_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='法院立案当事人';

-- ----------------------------------------------------------
-- 表: dwd_org_risk_court_notice  (开庭公告)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_risk_court_notice`;
CREATE TABLE `dwd_org_risk_court_notice` (
  `notice_id` VARCHAR(255) NOT NULL COMMENT '公告id；开庭公告唯一标识id。',
  `court_name` VARCHAR(255) NULL COMMENT '法院',
  `courtroom` VARCHAR(255) NULL COMMENT '法庭',
  `undertaking_dept` VARCHAR(255) NULL COMMENT '承办部门',
  `hearing_date` DATE NULL COMMENT '开庭日期',
  `scheduling_date` DATE NULL COMMENT '排期日期',
  `case_no` VARCHAR(255) NULL COMMENT '案号',
  `case_cause` VARCHAR(255) NULL COMMENT '案由',
  `case_type` VARCHAR(255) NULL COMMENT '案件类型',
  `jurisdiction_area` VARCHAR(255) NULL COMMENT '案件管辖区域',
  `plaintiff_appellant` VARCHAR(255) NULL COMMENT '原告上诉人',
  `defendant_appellee` VARCHAR(255) NULL COMMENT '被告被上诉人',
  `party` VARCHAR(255) NULL COMMENT '当事人',
  `presiding_judge` VARCHAR(255) NULL COMMENT '审判长主审人',
  `title` TEXT NULL COMMENT '标题',
  `notice_content` TEXT NULL COMMENT '公告内容',
  `province` VARCHAR(255) NULL COMMENT '省份',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标志',
  `original_url` TEXT NULL COMMENT '原始连接URL',
  `is_hidden` VARCHAR(255) NULL COMMENT '是否不展示',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_risk_court_n_notice_id` (`notice_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='开庭公告';

-- ----------------------------------------------------------
-- 表: dwd_org_risk_court_notice_list  (开庭公告当事人)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_risk_court_notice_list`;
CREATE TABLE `dwd_org_risk_court_notice_list` (
  `notice_id` VARCHAR(255) NOT NULL COMMENT '公告id；开庭公告唯一标识id，关联开庭公告表。',
  `party_role` VARCHAR(255) NULL COMMENT '当事人角色',
  `party_role_type` VARCHAR(255) NULL COMMENT '当事人角色类型',
  `party_type` VARCHAR(255) NULL COMMENT '当事人类型',
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `related_person_name` VARCHAR(255) NULL COMMENT '相关人名称',
  `hearing_date` DATE NULL COMMENT '开庭日期',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标志',
  `is_hidden` VARCHAR(255) NULL COMMENT '是否不展示',
  `case_cause` VARCHAR(255) NULL COMMENT '案由',
  `reserve_field` VARCHAR(255) NULL COMMENT '预留字段',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_risk_court_n_notice_id` (`notice_id`),
  KEY `idx_dwd_org_risk_court_n_org_id` (`org_id`),
  KEY `idx_dwd_org_risk_court_n_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='开庭公告当事人';

-- ----------------------------------------------------------
-- 表: dwd_org_risk_court_announcement  (法院公告)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_risk_court_announcement`;
CREATE TABLE `dwd_org_risk_court_announcement` (
  `notice_id` VARCHAR(255) NOT NULL COMMENT '公告id；法院公告唯一标识id。',
  `notice_no` VARCHAR(255) NULL COMMENT '公告号',
  `notice_name` VARCHAR(255) NULL COMMENT '公告名称',
  `notice_type` VARCHAR(255) NULL COMMENT '公告类型',
  `notice_type_name` VARCHAR(255) NULL COMMENT '公告类型名称',
  `notice_date` DATE NULL COMMENT '公告日期',
  `case_no` VARCHAR(255) NULL COMMENT '案号',
  `title` TEXT NULL COMMENT '标题',
  `notice_content` TEXT NULL COMMENT '公告内容',
  `court_name` VARCHAR(255) NULL COMMENT '法院名称',
  `handle_level` VARCHAR(255) NULL COMMENT '处理等级',
  `handle_level_name` VARCHAR(255) NULL COMMENT '处理等级名称',
  `judge` VARCHAR(255) NULL COMMENT '法官',
  `judge_phone` VARCHAR(255) NULL COMMENT '法官电话',
  `mobile_phone` VARCHAR(255) NULL COMMENT '手机号',
  `plaintiff` VARCHAR(255) NULL COMMENT '原告',
  `party` VARCHAR(255) NULL COMMENT '当事人',
  `province` VARCHAR(255) NULL COMMENT '省份',
  `case_cause` VARCHAR(255) NULL COMMENT '案由',
  `notice_year` DOUBLE NULL COMMENT '公告年份',
  `publish_date` DATE NULL COMMENT '公告刊登日期',
  `publish_page_no` VARCHAR(255) NULL COMMENT '公告刊登版面页码',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标志',
  `original_url` TEXT NULL COMMENT '原始连接URL',
  `content_md5` VARCHAR(255) NULL COMMENT '公告内容的md5值',
  `is_hidden` VARCHAR(255) NULL COMMENT '是否不展示',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_risk_court_a_notice_id` (`notice_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='法院公告';

-- ----------------------------------------------------------
-- 表: dwd_org_risk_court_announcement_list  (法院公告当事人)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_risk_court_announcement_list`;
CREATE TABLE `dwd_org_risk_court_announcement_list` (
  `notice_id` VARCHAR(255) NOT NULL COMMENT '公告id；法院公告唯一标识id，关联法院公告表。',
  `party_identity` VARCHAR(255) NULL COMMENT '当事人身份',
  `party_type` VARCHAR(255) NULL COMMENT '当事人类型',
  `party_role_type` VARCHAR(255) NULL COMMENT '当事人角色类型',
  `related_person_name` VARCHAR(255) NULL COMMENT '相关人名称',
  `publish_date` DATE NULL COMMENT '公告刊登日期',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标志',
  `is_hidden` VARCHAR(255) NULL COMMENT '是否不展示',
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_risk_court_a_notice_id` (`notice_id`),
  KEY `idx_dwd_org_risk_court_a_org_id` (`org_id`),
  KEY `idx_dwd_org_risk_court_a_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='法院公告当事人';

-- ----------------------------------------------------------
-- 表: dwd_org_company_justice  (股权冻结)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_company_justice`;
CREATE TABLE `dwd_org_company_justice` (
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `judicial_assist_id` VARCHAR(255) NOT NULL COMMENT '司法协助记录id；司法协助记录唯一标识id。',
  `executed_person` VARCHAR(255) NULL COMMENT '被执行人',
  `equity_amount` VARCHAR(255) NULL COMMENT '股权数额',
  `exec_court` VARCHAR(255) NULL COMMENT '执行法院',
  `exec_notice_no` VARCHAR(255) NULL COMMENT '执行通知书文号',
  `type_status` VARCHAR(255) NULL COMMENT '类型|状态',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标记',
  `status` VARCHAR(255) NULL COMMENT '状态',
  `executed_person_type` VARCHAR(255) NULL COMMENT '被执行人类型',
  `executed_company_id` VARCHAR(255) NULL COMMENT '被执行人的company_id',
  `name_cn` VARCHAR(255) NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_company_just_org_id` (`org_id`),
  KEY `idx_dwd_org_company_just_judicial_assist_id` (`judicial_assist_id`),
  KEY `idx_dwd_org_company_just_executed_company_id` (`executed_company_id`),
  KEY `idx_dwd_org_company_just_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='股权冻结';

-- ----------------------------------------------------------
-- 表: dwd_org_company_pledge  (股权出质)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_company_pledge`;
CREATE TABLE `dwd_org_company_pledge` (
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `pledge_id` VARCHAR(255) NOT NULL COMMENT '股权出质记录id；股权出质记录唯一标识id。',
  `reg_no` VARCHAR(255) NULL COMMENT '登记编号',
  `pledgor` VARCHAR(255) NULL COMMENT '出质人',
  `pledgor_id_no` VARCHAR(255) NULL COMMENT '出质人证件号码',
  `pledgee` VARCHAR(255) NULL COMMENT '质权人',
  `pledgee_id_no` VARCHAR(255) NULL COMMENT '质权人证件号码',
  `equity_amount` VARCHAR(255) NULL COMMENT '出质股权数额',
  `pledge_reg_date` DATE NULL COMMENT '股权出质设立登记日期',
  `status` VARCHAR(255) NULL COMMENT '状态',
  `public_date` DATE NULL COMMENT '公示日期',
  `cancel_date` DATE NULL COMMENT '注销日期',
  `cancel_reason` TEXT NULL COMMENT '注销原因',
  `invalid_date` DATE NULL COMMENT '失效时间',
  `invalid_reason` TEXT NULL COMMENT '失效原因',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标记',
  `status_code` VARCHAR(255) NULL COMMENT '状态代码',
  `province_abbr` VARCHAR(255) NULL COMMENT '省份简称',
  `pledgor_company_id` VARCHAR(255) NULL COMMENT '机构出质人的company_id',
  `pledgor_company_name` VARCHAR(255) NULL COMMENT '机构出质人名称',
  `pledgor_credit_code` VARCHAR(255) NULL COMMENT '机构出质人统一社会信用代码',
  `pledgor_type` VARCHAR(255) NULL COMMENT '出质人类型',
  `pledgee_company_id` VARCHAR(255) NULL COMMENT '机构质权人的company_id',
  `pledgee_company_name` VARCHAR(255) NULL COMMENT '机构质权人名称',
  `pledgee_credit_code` VARCHAR(255) NULL COMMENT '机构质权人统一社会信用代码',
  `pledgee_type` VARCHAR(255) NULL COMMENT '质权人类型',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_company_pled_org_id` (`org_id`),
  KEY `idx_dwd_org_company_pled_external_id` (`external_id`),
  KEY `idx_dwd_org_company_pled_pledge_id` (`pledge_id`),
  KEY `idx_dwd_org_company_pled_pledgor_company_id` (`pledgor_company_id`),
  KEY `idx_dwd_org_company_pled_pledgor_credit_code` (`pledgor_credit_code`),
  KEY `idx_dwd_org_company_pled_pledgee_company_id` (`pledgee_company_id`),
  KEY `idx_dwd_org_company_pled_pledgee_credit_code` (`pledgee_credit_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='股权出质';

-- ----------------------------------------------------------
-- 表: dwd_org_risk_zhongben  (终本案件)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_risk_zhongben`;
CREATE TABLE `dwd_org_risk_zhongben` (
  `official_id` VARCHAR(255) NULL COMMENT '官网id',
  `executed_person_name` VARCHAR(255) NULL COMMENT '被执行人姓名名称',
  `gender` VARCHAR(255) NULL COMMENT '性别',
  `case_no` VARCHAR(255) NOT NULL COMMENT '案号',
  `executed_person_type` VARCHAR(255) NULL COMMENT '被执行人类型',
  `id_no` VARCHAR(255) NULL COMMENT '证件号码',
  `exec_court` VARCHAR(255) NULL COMMENT '执行法院',
  `filing_date` DATE NULL COMMENT '立案日期',
  `termination_date` DATE NULL COMMENT '终本日期',
  `address` TEXT NULL COMMENT '地址',
  `exec_target_amount` DOUBLE NULL COMMENT '执行标的金额',
  `unfulfilled_amount` DOUBLE NULL COMMENT '未履行标的金额',
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `data_use_flag` VARCHAR(255) NULL COMMENT '数据使用标记',
  `is_history` VARCHAR(255) NULL COMMENT '是否是历史数据',
  `is_hidden` VARCHAR(255) NULL COMMENT '是否不展示',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_risk_zhongbe_official_id` (`official_id`),
  KEY `idx_dwd_org_risk_zhongbe_org_id` (`org_id`),
  KEY `idx_dwd_org_risk_zhongbe_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='终本案件';

-- ----------------------------------------------------------
-- 表: dwd_org_company_chattel  (动产抵押)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_company_chattel`;
CREATE TABLE `dwd_org_company_chattel` (
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `reg_no` VARCHAR(255) NULL COMMENT '登记编号',
  `reg_date` DATE NULL COMMENT '登记日期',
  `reg_org` VARCHAR(255) NULL COMMENT '登记机关',
  `guarantee_type` VARCHAR(255) NULL COMMENT '被担保债权种类',
  `guarantee_amount` DOUBLE NULL COMMENT '被担保债权数额',
  `guarantee_scope` TEXT NULL COMMENT '担保范围',
  `public_date` DATE NULL COMMENT '公示日期',
  `debt_term` VARCHAR(255) NULL COMMENT '债务人履行债务的期限',
  `debt_remark` TEXT NULL COMMENT '主债权信息备注',
  `status` VARCHAR(255) NULL COMMENT '状态',
  `cancel_date` DATE NULL COMMENT '注销日期',
  `cancel_reason` TEXT NULL COMMENT '注销原因',
  `status_code` VARCHAR(255) NULL COMMENT '状态代码',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标记',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_company_chat_org_id` (`org_id`),
  KEY `idx_dwd_org_company_chat_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='动产抵押';

-- ----------------------------------------------------------
-- 表: dwd_org_tb_judicial_sale  (司法拍卖)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_tb_judicial_sale`;
CREATE TABLE `dwd_org_tb_judicial_sale` (
  `notice_name` TEXT NULL COMMENT '公告名',
  `asset_disposal_unit` VARCHAR(255) NULL COMMENT '资产处置单位',
  `notice_time` DATETIME NULL COMMENT '公告时间',
  `notice_id` VARCHAR(255) NOT NULL COMMENT '公告id；司法拍卖公告唯一标识id。',
  `source_website` VARCHAR(255) NULL COMMENT '来源网站',
  `notice_content_path` TEXT NULL COMMENT '公告内容存储路径',
  `auction_start_date` DATE NULL COMMENT '拍卖开始日期',
  `auction_end_date` DATE NULL COMMENT '拍卖截止日期',
  `original_link` TEXT NULL COMMENT '原始链接',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标志',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_tb_judicial__notice_id` (`notice_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='司法拍卖';

-- ----------------------------------------------------------
-- 表: dwd_org_tb_judicial_sale_info_company  (司法拍卖当事人)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_tb_judicial_sale_info_company`;
CREATE TABLE `dwd_org_tb_judicial_sale_info_company` (
  `notice_id` VARCHAR(255) NOT NULL COMMENT '公告id；司法拍卖公告唯一标识id，关联司法拍卖表。',
  `related_company` VARCHAR(255) NULL COMMENT '相关公司',
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `use_flag` VARCHAR(255) NULL COMMENT '使用标记',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_tb_judicial__notice_id` (`notice_id`),
  KEY `idx_dwd_org_tb_judicial__org_id` (`org_id`),
  KEY `idx_dwd_org_tb_judicial__external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='司法拍卖当事人';

-- ----------------------------------------------------------
-- 表: dwd_org_bankruptcy_public_cases  (破产案件)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_bankruptcy_public_cases`;
CREATE TABLE `dwd_org_bankruptcy_public_cases` (
  `case_no` VARCHAR(255) NOT NULL COMMENT '案号',
  `case_type` VARCHAR(255) NULL COMMENT '案件类型',
  `handling_court` VARCHAR(255) NULL COMMENT '经办法院',
  `applicant_info` TEXT NULL COMMENT '申请人信息',
  `respondent_info` TEXT NULL COMMENT '被申请人信息',
  `admin_org` VARCHAR(255) NULL COMMENT '管理人机构',
  `admin_org_id` VARCHAR(255) NULL COMMENT '管理人机构id',
  `admin_principal` VARCHAR(255) NULL COMMENT '管理人主要负责人',
  `public_date` DATE NULL COMMENT '公开时间',
  `link` TEXT NULL COMMENT '链接',
  `is_deleted` VARCHAR(255) NULL COMMENT '是否删除',
  `history_status` VARCHAR(255) NULL COMMENT '历史状态',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_bankruptcy_p_admin_org_id` (`admin_org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='破产案件';

-- ----------------------------------------------------------
-- 表: dwd_org_bankruptcy_public_cases_list  (破产案件当事人)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国内机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_org_bankruptcy_public_cases_list`;
CREATE TABLE `dwd_org_bankruptcy_public_cases_list` (
  `bankruptcy_party_id` VARCHAR(255) NOT NULL COMMENT '唯一索引id；破产案件当事人记录唯一标识id。',
  `case_no` VARCHAR(255) NULL COMMENT '案号',
  `related_person_name` VARCHAR(255) NULL COMMENT '相关人名称',
  `party_role_type` VARCHAR(255) NULL COMMENT '当事人角色类型',
  `party_type` VARCHAR(255) NULL COMMENT '当事人类型',
  `org_id` VARCHAR(255) NULL COMMENT '机构id',
  `name_cn` VARCHAR(255) NULL COMMENT '机构名称',
  `external_id` VARCHAR(255) NULL COMMENT '统一社会信用代码',
  `public_date` DATE NULL COMMENT '公开时间',
  `is_deleted` VARCHAR(255) NULL COMMENT '是否删除',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  `created_time` DATETIME NOT NULL COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间',
  KEY `idx_dwd_org_bankruptcy_p_bankruptcy_party_id` (`bankruptcy_party_id`),
  KEY `idx_dwd_org_bankruptcy_p_org_id` (`org_id`),
  KEY `idx_dwd_org_bankruptcy_p_external_id` (`external_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='破产案件当事人';

-- ----------------------------------------------------------
-- 表: dwd_forg_base_info  (海外机构基本信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国外机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_forg_base_info`;
CREATE TABLE `dwd_forg_base_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id',
  `name_en` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `name_alias` VARCHAR(255) NULL COMMENT '机构本地名称',
  `country_code` VARCHAR(255) NULL COMMENT '国家代码',
  `country` VARCHAR(255) NULL COMMENT '国家',
  `external_id` VARCHAR(255) NULL COMMENT '当地官方唯一注册码',
  `city` VARCHAR(255) NULL COMMENT '所在城市',
  `address` TEXT NULL COMMENT '公司地址',
  `postal_code` VARCHAR(255) NULL COMMENT '邮政编码（无数据）',
  `phone` VARCHAR(255) NULL COMMENT '联系电话',
  `email` VARCHAR(255) NULL COMMENT '电子邮箱',
  `company_type` VARCHAR(255) NULL COMMENT '企业类型',
  `registration_org` VARCHAR(255) NULL COMMENT '注册机构（无数据）',
  `incorporation_year` DOUBLE NULL COMMENT '成立年份',
  `incorporation_date` DATE NULL COMMENT '成立日期/注册日期/核准日期',
  `listing_status` VARCHAR(255) NULL COMMENT '上市状态',
  `registered_capital_value` DOUBLE NULL COMMENT '注册资本',
  `registered_capital_currency_code` VARCHAR(255) NULL COMMENT '注册资本货币代码',
  `industry_class` VARCHAR(255) NULL COMMENT '公司行业分类',
  `industry_type` VARCHAR(255) NULL COMMENT '行业分类标准（新增字段）'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海外机构基本信息';

-- ----------------------------------------------------------
-- 表: dwd_forg_shareholder_info  (海外机构股东股权关联信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国外机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_forg_shareholder_info`;
CREATE TABLE `dwd_forg_shareholder_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id',
  `owners_name` VARCHAR(255) NULL COMMENT '股东名称',
  `ownership_percentage` DOUBLE NULL COMMENT '股权占比(%)',
  `owners_country_code` VARCHAR(255) NULL COMMENT '股东所在国家代码',
  `owners_country` VARCHAR(255) NULL COMMENT '股东所在国家'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海外机构股东股权关联信息';

-- ----------------------------------------------------------
-- 表: dwd_forg_subsidiary_info  (海外机构子公司股权关联信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国外机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_forg_subsidiary_info`;
CREATE TABLE `dwd_forg_subsidiary_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id',
  `affiliate` VARCHAR(255) NULL COMMENT '子公司id',
  `affiliates_name` VARCHAR(255) NULL COMMENT '子公司名称',
  `affiliates_country_code` VARCHAR(255) NULL COMMENT '子公司国家代码',
  `affiliates_country` VARCHAR(255) NULL COMMENT '子公司国家',
  `affiliates_company_id` VARCHAR(255) NULL COMMENT '子公司唯一注册码'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海外机构子公司股权关联信息';

-- ----------------------------------------------------------
-- 表: dwd_forg_executive_info  (海外机构高管信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国外机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_forg_executive_info`;
CREATE TABLE `dwd_forg_executive_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id',
  `executives_name` VARCHAR(255) NULL COMMENT '高管姓名',
  `executives_position` VARCHAR(255) NULL COMMENT '职位名称',
  `dm_birthdate` DATE NULL COMMENT '高管出生日期(新增字段)',
  `dm_nationalities` VARCHAR(255) NULL COMMENT '高管国籍(新增字段)',
  `dm_biography` VARCHAR(255) NULL COMMENT '高管履历(新增字段)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海外机构高管信息';

-- ----------------------------------------------------------
-- 表: dwd_forg_product_info  (海外机构公司经营信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国外机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_forg_product_info`;
CREATE TABLE `dwd_forg_product_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id',
  `description` VARCHAR(255) NULL COMMENT '业务描述',
  `main_products` VARCHAR(255) NULL COMMENT '主要产品'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海外机构公司经营信息';

-- ----------------------------------------------------------
-- 表: dwd_forg_beneficiary_info  (海外机构受益人信息（新增表）)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国外机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_forg_beneficiary_info`;
CREATE TABLE `dwd_forg_beneficiary_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id',
  `bo_name` VARCHAR(255) NULL COMMENT '受益人名称',
  `bo_gender` VARCHAR(255) NULL COMMENT '受益人性别',
  `bo_birthdate` DATE NULL COMMENT '受益人出生日期',
  `bo_country_code` VARCHAR(255) NULL COMMENT '受益人所在国家代码',
  `path` VARCHAR(255) NULL COMMENT '受益人关系路径',
  `bo_manager` VARCHAR(255) NULL COMMENT '受益人是否同时是管理层',
  `total_percent` DOUBLE NULL COMMENT '总持股比例',
  `direct_percent` DOUBLE NULL COMMENT '直接持股比例',
  `indirect_percent` DOUBLE NULL COMMENT '间接持股比例'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海外机构受益人信息（新增表）';

-- ----------------------------------------------------------
-- 表: dwd_forg_act_contro_info  (海外机构实控人信息（新增表）)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国外机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_forg_act_contro_info`;
CREATE TABLE `dwd_forg_act_contro_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id',
  `country_code` VARCHAR(255) NULL COMMENT '企业国家代码',
  `entity_eid` VARCHAR(255) NULL COMMENT '实控人ID',
  `entity_name` VARCHAR(255) NULL COMMENT '实控人名称',
  `entity_type` VARCHAR(255) NULL COMMENT '实控人类型',
  `entity_country_code` VARCHAR(255) NULL COMMENT '实控人国家代码',
  `direct_pct` VARCHAR(255) NULL COMMENT '直接持股比例',
  `total_pct` VARCHAR(255) NULL COMMENT '总持股比例',
  `direct_pct_num` DOUBLE NULL COMMENT '直接持股比例数值',
  `total_pct_num` DOUBLE NULL COMMENT '总持股比例数值',
  `path` VARCHAR(255) NULL COMMENT '路径'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海外机构实控人信息（新增表）';

-- ----------------------------------------------------------
-- 表: dwd_forg_stock_fin_info  (海外上市企业财务信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国外机构要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_forg_stock_fin_info`;
CREATE TABLE `dwd_forg_stock_fin_info` (
  `org_id` VARCHAR(255) NOT NULL COMMENT '机构id',
  `occur_period` DATE NULL COMMENT '报告期',
  `total_assets` DOUBLE NULL COMMENT '资产总额',
  `fixed_assets` DOUBLE NULL COMMENT '固定资产总额',
  `total_liabilities` DOUBLE NULL COMMENT '负债总额',
  `operating_revenue` DOUBLE NULL COMMENT '营业收入',
  `main_business_revenue` DOUBLE NULL COMMENT '主营业务收入',
  `total_profit` DOUBLE NULL COMMENT '利润总额',
  `pure_profit` DOUBLE NULL COMMENT '净利润',
  `total_tax_paid` DOUBLE NULL COMMENT '企业所得税',
  `oper_cash_flow` DOUBLE NULL COMMENT '经营活动现金流',
  `owners_equity` DOUBLE NULL COMMENT '所有者权益合计',
  `employees_number` DOUBLE NULL COMMENT '从业人数',
  `research_development_amount` DOUBLE NULL COMMENT '研发投入金额',
  `research_development_employees_number` DOUBLE NULL COMMENT '研发人员数（无数据）'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海外上市企业财务信息';

-- ----------------------------------------------------------
-- 表: dwd_scholar  (学者)
-- 来源文件: 版权人才、企业机构、政策数据汇总表(含行业范围).xlsx | Sheet: 人才要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_scholar`;
CREATE TABLE `dwd_scholar` (
  `scholar_id` VARCHAR(32) NOT NULL COMMENT '学者ID；学者记录的业务唯一标识。',
  `name_en` VARCHAR(128) NOT NULL COMMENT '英文姓名；学者的英文姓名。',
  `name_zh` VARCHAR(128) NOT NULL COMMENT '中文姓名；学者的中文姓名。',
  `avatar` VARCHAR(256) NOT NULL COMMENT '头像；学者头像图片的访问链接。',
  `scholar_org_name_en` TEXT NULL COMMENT '英文机构；学者所属机构的英文名称。',
  `scholar_org_name_zh` VARCHAR(1024) NULL COMMENT '中文机构；学者所属机构的中文名称。',
  `bio` LONGTEXT NULL COMMENT '个人简介/学术简介；学者的个人或学术简介信息。',
  `bio_zh` LONGTEXT NULL COMMENT '个人简介/学术简介（中文）；学者的中文个人或学术简介信息。',
  `work_experience_en` LONGTEXT NULL COMMENT '工作经历英文（包含机构和职务）；学者英文工作经历信息。',
  `work_experience_zh` LONGTEXT NULL COMMENT '工作经历中文（包含机构和职务）；学者中文工作经历信息。',
  `education_background_en` LONGTEXT NULL COMMENT '教育背景（英文）；学者的英文教育经历信息。',
  `education_background_zh` LONGTEXT NULL COMMENT '教育背景（中文）；学者的中文教育经历信息。',
  `paper_nums` INT NOT NULL COMMENT '论文数量；学者已发表论文的数量。',
  `citation_nums` INT NOT NULL COMMENT '被引数量；学者论文被引用的总次数。',
  `h_index` INT NOT NULL COMMENT 'H指数；衡量学者学术影响力的 H 指数。',
  `status` INT NOT NULL COMMENT '状态；记录状态，0 表示无效，1 表示有效。；值域: 0，1',
  `create_time` DATETIME NOT NULL COMMENT '创建时间；记录创建时间。',
  `update_time` DATETIME NOT NULL COMMENT '更新时间；记录最后更新时间。',
  PRIMARY KEY (`scholar_id`),
  KEY `idx_dwd_scholar_name_en` (`name_en`),
  KEY `idx_dwd_scholar_name_zh` (`name_zh`),
  KEY `idx_dwd_scholar_scholar_org_name_en` (`scholar_org_name_en`(255)),
  KEY `idx_dwd_scholar_scholar_org_name_zh` (`scholar_org_name_zh`(255)),
  KEY `idx_dwd_scholar_paper_nums` (`paper_nums`),
  KEY `idx_dwd_scholar_citation_nums` (`citation_nums`),
  KEY `idx_dwd_scholar_create_time` (`create_time`),
  KEY `idx_dwd_scholar_update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='学者';

-- ----------------------------------------------------------
-- 表: dwd_scholar_talent_flag  (学者人才标识)
-- 来源文件: 版权人才、企业机构、政策数据汇总表(含行业范围).xlsx | Sheet: 人才要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_scholar_talent_flag`;
CREATE TABLE `dwd_scholar_talent_flag` (
  `scholar_id` VARCHAR(32) NOT NULL COMMENT '学者ID；关联学者记录的业务唯一标识。',
  `academician` VARCHAR(128) NOT NULL COMMENT '是否为院士；标识学者是否为院士，来源于表1字段。；值域: 是/否',
  `create_time` DATETIME NOT NULL COMMENT '创建时间；记录创建时间。',
  `update_time` DATETIME NOT NULL COMMENT '更新时间；记录最后更新时间。',
  PRIMARY KEY (`scholar_id`),
  KEY `idx_dwd_scholar_talent_f_academician` (`academician`),
  KEY `idx_dwd_scholar_talent_f_create_time` (`create_time`),
  KEY `idx_dwd_scholar_talent_f_update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='学者人才标识';

-- ----------------------------------------------------------
-- 表: dwd_scholar_research_direction  (学者研究方向)
-- 来源文件: 版权人才、企业机构、政策数据汇总表(含行业范围).xlsx | Sheet: 人才要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_scholar_research_direction`;
CREATE TABLE `dwd_scholar_research_direction` (
  `scholar_id` VARCHAR(32) NOT NULL COMMENT '学者ID；关联学者记录的业务唯一标识。',
  `fields` TEXT NULL COMMENT '研究方向；学者研究方向，来源于表1字段。',
  `create_time` DATETIME NOT NULL COMMENT '创建时间；记录创建时间。',
  `update_time` DATETIME NOT NULL COMMENT '更新时间；记录最后更新时间。',
  PRIMARY KEY (`scholar_id`),
  KEY `idx_dwd_scholar_research_create_time` (`create_time`),
  KEY `idx_dwd_scholar_research_update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='学者研究方向';

-- ----------------------------------------------------------
-- 表: dwd_scholar_paper_relation  (学者论文关系)
-- 来源文件: 版权人才、企业机构、政策数据汇总表(含行业范围).xlsx | Sheet: 人才要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_scholar_paper_relation`;
CREATE TABLE `dwd_scholar_paper_relation` (
  `paper_id` VARCHAR(8) NOT NULL COMMENT '论文ID；论文记录的唯一标识。',
  `year` VARCHAR(8) NOT NULL COMMENT '论文发表年份；论文发表年份。',
  `scholar_id` VARCHAR(32) NOT NULL COMMENT '学者ID；学者记录的业务唯一标识。',
  `citations` INT NOT NULL COMMENT '被引用次数；论文被引用次数。',
  `publish_time` DATE NULL COMMENT '发布时间；论文发布时间。',
  `status` INT NOT NULL COMMENT '状态；记录状态，0 表示无效，1 表示有效。；值域: 0，1',
  `create_time` DATETIME NOT NULL COMMENT '创建时间；记录创建时间。',
  `update_time` DATETIME NOT NULL COMMENT '更新时间；记录最后更新时间。',
  `publication_id` VARCHAR(8) NOT NULL COMMENT '期刊ID；期刊或会议记录的唯一标识。',
  `related_paper_id` BIGINT NOT NULL COMMENT '关联论文库ID；关联论文库的唯一标识。',
  PRIMARY KEY (`scholar_id`),
  KEY `idx_dwd_scholar_paper_re_paper_id` (`paper_id`),
  KEY `idx_dwd_scholar_paper_re_citations` (`citations`),
  KEY `idx_dwd_scholar_paper_re_publish_time` (`publish_time`),
  KEY `idx_dwd_scholar_paper_re_create_time` (`create_time`),
  KEY `idx_dwd_scholar_paper_re_update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='学者论文关系';

-- ----------------------------------------------------------
-- 表: dwd_scholar_papers  (论文信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表(含行业范围).xlsx | Sheet: 人才要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_scholar_papers`;
CREATE TABLE `dwd_scholar_papers` (
  `zh_name` VARCHAR(500) NOT NULL COMMENT '中文题目；论文的中文标题名称。',
  `en_name` VARCHAR(500) NOT NULL COMMENT '英文题目；论文的英文标题名称。',
  `authors` TEXT NULL COMMENT '作者列表；论文作者的姓名或信息列表。',
  `paper_url` VARCHAR(1024) NOT NULL COMMENT '论文原始链接；论文原始来源页面的访问链接。',
  `cover_date_start` DATE NULL COMMENT '发表时间；论文正式发表或出版的时间。',
  `create_time` DATETIME NULL COMMENT '创建时间；记录创建时间。',
  `update_time` DATETIME NULL COMMENT '更新时间；记录最后更新时间。',
  `status` INT NULL COMMENT '状态；记录状态，0 表示无效，1 表示有效。；值域: 0，1',
  `zh_abstract` TEXT NULL COMMENT '中文摘要；论文内容的中文摘要信息。',
  `en_abstract` TEXT NULL COMMENT '英文摘要；论文内容的英文摘要信息。',
  `doi` VARCHAR(512) NOT NULL COMMENT 'DOI；论文的 DOI 唯一识别号。',
  `publication_en_name` VARCHAR(1024) NOT NULL COMMENT '期刊/会议英文名；论文发表所在期刊或会议的英文名称。',
  KEY `idx_dwd_scholar_papers_en_name` (`en_name`(255)),
  KEY `idx_dwd_scholar_papers_cover_date_start` (`cover_date_start`),
  KEY `idx_dwd_scholar_papers_create_time` (`create_time`),
  KEY `idx_dwd_scholar_papers_update_time` (`update_time`),
  KEY `idx_dwd_scholar_papers_doi` (`doi`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='论文信息';

-- ----------------------------------------------------------
-- 表: dwd_scholar_coauthor  (学者合作者关系)
-- 来源文件: 版权人才、企业机构、政策数据汇总表(含行业范围).xlsx | Sheet: 人才要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_scholar_coauthor`;
CREATE TABLE `dwd_scholar_coauthor` (
  `scholar_id` VARCHAR(32) NOT NULL COMMENT '学者ID；当前学者记录的业务唯一标识。',
  `co_scholar_id` VARCHAR(32) NOT NULL COMMENT '合作学者ID；合作学者记录的业务唯一标识。',
  `co_scholar_name_en` VARCHAR(256) NULL COMMENT '合作学者英文名；合作学者的英文姓名。',
  `co_scholar_name_zh` VARCHAR(128) NULL COMMENT '合作学者中文名；合作学者的中文姓名。',
  `co_scholar_avatar` VARCHAR(512) NULL COMMENT '合作学者头像URL；合作学者头像图片的访问链接。',
  `co_scholar_org_name_en` TEXT NULL COMMENT '合作学者所属机构英文名；合作学者所属机构的英文名称。',
  `co_scholar_org_name_zh` VARCHAR(1024) NULL COMMENT '合作学者所属机构中文名；合作学者所属机构的中文名称。',
  `co_paper_count` INT NOT NULL COMMENT '合作论文数量；与该学者合作发表的论文数量。',
  `status` INT NOT NULL COMMENT '状态；记录状态，0 表示无效，1 表示有效。；值域: 0，1',
  `create_time` DATETIME NOT NULL COMMENT '创建时间；记录创建时间。',
  `update_time` DATETIME NOT NULL COMMENT '更新时间；记录最后更新时间。',
  PRIMARY KEY (`scholar_id`),
  KEY `idx_dwd_scholar_coauthor_co_scholar_id` (`co_scholar_id`),
  KEY `idx_dwd_scholar_coauthor_co_scholar_name_en` (`co_scholar_name_en`(255)),
  KEY `idx_dwd_scholar_coauthor_co_scholar_name_zh` (`co_scholar_name_zh`),
  KEY `idx_dwd_scholar_coauthor_status` (`status`),
  KEY `idx_dwd_scholar_coauthor_update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='学者合作者关系';

-- ----------------------------------------------------------
-- 表: dwd_zck_policy  (国内政策信息表)
-- 来源文件: 版权人才、企业机构、政策数据汇总表(含行业范围).xlsx | Sheet: 国内政策要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zck_policy`;
CREATE TABLE `dwd_zck_policy` (
  `id` VARCHAR(255) NULL COMMENT '唯一ID',
  `datatype` VARCHAR(2) NOT NULL COMMENT '数据类型；数据类型（政策/解读）',
  `docstatus` VARCHAR(2) NOT NULL COMMENT '状态（20-已发布，30-已撤销）；政策的发布状态（20-已发布，30-已撤销）',
  `title` VARCHAR(1000) NOT NULL COMMENT '标题（纯文本）',
  `titlena` VARCHAR(1000) NOT NULL COMMENT '标题（富文本）',
  `content` VARCHAR(2000) NOT NULL COMMENT '内容（纯文本）',
  `contentNa` VARCHAR(2000) NOT NULL COMMENT '内容（富文本）',
  `url` VARCHAR(1000) NOT NULL COMMENT '原文链接地址',
  `issueno` VARCHAR(255) NOT NULL COMMENT '发文字号',
  `indexno` VARCHAR(255) NOT NULL COMMENT '索引号',
  `sitename` VARCHAR(255) NOT NULL COMMENT '站点名称',
  `crtime` VARCHAR(10) NOT NULL COMMENT '成文日期；值域: 格式：2023-11-09',
  `pubtime` VARCHAR(10) NOT NULL COMMENT '发文日期（发布日期）；值域: 格式：2023-11-09',
  `pubyear` VARCHAR(4) NOT NULL COMMENT '发布年份',
  `area` VARCHAR(255) NOT NULL COMMENT '地区；发布单位的所属地区',
  `policylevel` VARCHAR(255) NOT NULL COMMENT '政策层级；政策层级（国家级/省级/市级/区县级）；值域: 国家级、省级、市级、区县级',
  `region` VARCHAR(255) NOT NULL COMMENT '政策地区',
  `attachments` VARCHAR(2000) NOT NULL COMMENT '附件信息；政策附件文件的链接',
  `keywords` VARCHAR(1000) NOT NULL COMMENT '关键词；政策内容关键词',
  `abs` VARCHAR(2000) NOT NULL COMMENT '摘要；正文摘要',
  `maelements` VARCHAR(2000) NOT NULL COMMENT '政策主旨要素；对政策背景、指导思想等政策内容进行标准化拆解与提炼',
  `ma_keypoints` VARCHAR(2000) NOT NULL COMMENT '政策要点；从政策全文中摘录、提炼章节标题、工作原则、发展现状、重点任务、细分产业、问题研判等内容。',
  `allfactors` VARCHAR(2000) NOT NULL COMMENT '政策扶持要素；含扶持分类、扶持门槛扶持力度。目的是提取政策中各类扶持、补助、优惠、激励类内容需满足的条件和对应的扶持信息',
  `complextaginfojson` VARCHAR(2000) NOT NULL COMMENT '标签集；政策所有的标签（json格式）',
  `pedigree` VARCHAR(2000) NOT NULL COMMENT '政策谱系；政策的上位政策和下位政策',
  `ma_contenttypenew` VARCHAR(255) NOT NULL COMMENT '文件类型；用于区分政策文件的性质、发文类别、公文体裁，是政务数据基础分类字段；值域: 纲要、规划、发展愿景、行动计划、实施方案、工作方案、指导意见、若干措施、实施细则、扶持计划、规定、法律法规、条例 、管理办法、要求、申报指南、 项目征集、资质认定、揭榜挂帅 、批复公示、通知公告、征求意见稿、决定、函',
  `pubdeptname` VARCHAR(255) NOT NULL COMMENT '发布单位名称',
  `topic_type` VARCHAR(255) NOT NULL COMMENT '主题分类；政策主题分类',
  `expiration_date` VARCHAR(10) NOT NULL COMMENT '失效日期',
  KEY `idx_dwd_zck_policy_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国内政策信息表';

-- ----------------------------------------------------------
-- 表: dwd_zck_intl_policy  (国际政策信息)
-- 来源文件: 版权人才、企业机构、政策数据汇总表v0601.xlsx | Sheet: 国外政策要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zck_intl_policy`;
CREATE TABLE `dwd_zck_intl_policy` (
  `id` VARCHAR(255) NOT NULL COMMENT '唯一id',
  `title` VARCHAR(1000) NOT NULL COMMENT '标题原文',
  `translate_title` VARCHAR(1000) NOT NULL COMMENT '标题译文',
  `abstract` VARCHAR(2000) NOT NULL COMMENT '摘要原文',
  `content` TEXT NOT NULL COMMENT '正文原文',
  `translate_content` TEXT NOT NULL COMMENT '正文译文',
  `media_product_name` VARCHAR(255) NOT NULL COMMENT '媒体名称',
  `media_type` VARCHAR(255) NOT NULL COMMENT '媒体类型',
  `release_year` VARCHAR(255) NOT NULL COMMENT '年份',
  `release_date` VARCHAR(255) NOT NULL COMMENT '发布日期',
  `media_area` VARCHAR(255) NOT NULL COMMENT '所属区域',
  `url_link` VARCHAR(1000) NOT NULL COMMENT 'url链接',
  `language` VARCHAR(255) NOT NULL COMMENT '语种',
  `class` VARCHAR(255) NOT NULL COMMENT '内容分类',
  `class_no` VARCHAR(255) NOT NULL COMMENT '分类号',
  `source` VARCHAR(255) NOT NULL COMMENT '数据来源',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国际政策信息';

-- ----------------------------------------------------------
-- 表: dwd_drug  (药品信息表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_drug`;
CREATE TABLE `dwd_drug` (
  `application_number` VARCHAR(32) NULL COMMENT '药品申请号；药品在监管机构申请或批准体系中的编号，用于关联审评、批准和标签信息。',
  `id` VARCHAR(32) NOT NULL COMMENT '药物ID；药品记录的内部或来源库唯一标识，用于去重和跨表关联。',
  `drug_name` VARCHAR(255) NOT NULL COMMENT '药物名称；药物安全、交易或试验记录中涉及的药品名称。',
  `brand_name` VARCHAR(255) NULL COMMENT '商品名；药品上市销售时使用的品牌名称。',
  `generic_name` VARCHAR(255) NULL COMMENT '通用名；药品非专利通用名称或国际通用名称。',
  `active_ingredients` VARCHAR(255) NULL COMMENT '活性成分；药品中具有治疗作用的主要成分，可包含一个或多个成分。',
  `route` VARCHAR(255) NULL COMMENT '给药途径；药品进入人体的给药方式，如口服、注射、皮下等。；值域: [AURICULAR (OTIC)，BUCCAL，CONJUNCTIVAL，CUTANEOUS，DENTAL，ELECTRO-OSMOSIS，ENDOCERVICAL，ENDOSINUSIAL，ENDOTRACHEAL，ENTERAL，EPIDURAL，EXTRA-AMNIOTIC，EXTRACORPOREAL，HEMODIALYSIS，INFILTRATION，INTERSTITIAL，INTRA-ABDOMINAL，INTRA-AMNIOTIC，INTRA-ARTERIAL，INTRA-ARTICULAR，INTRABILIARY，INTRABRONCHIAL，INTRABURSAL，INTRACAMERAL，INTRACANALICULAR，INTRACARDIAC，INTRACARTILAGINOUS，INTRACAUDAL，INTRACAVERNOUS，INTRACAVITARY，INTRACEREBRAL，INTRACISTERNAL，INTRACORNEAL，INTRACORONAL, DENTAL，INTRACORONARY，INTRACORPORUS CAVERNOSUM，INTRACRANIAL，INTRADERMAL，INTRADISCAL，INTRADUCTAL，INTRADUODENAL，INTRADURAL，INTRAEPICARDIAL，INTRAEPIDERMAL，INTRAESOPHAGEAL，INTRAGASTRIC，INTRAGINGIVAL，INTRAHEPATIC，INTRAILEAL，INTRALESIONAL，INTRALINGUAL，INTRALUMINAL，INTRALYMPHATIC，INTRAMAMMARY，INTRAMEDULLARY，INTRAMENINGEAL，INTRAMUSCULAR，INTRANODAL，INTRAOCULAR，INTRAOMENTUM，INTRAOVARIAN，INTRAPERICARDIAL，INTRAPERITONEAL，INTRAPLEURAL，INTRAPROSTATIC，INTRAPULMONARY，INTRARUMINAL，INTRASINAL，INTRASPINAL，INTRASYNOVIAL，INTR…',
  `dosage_form` VARCHAR(128) NULL COMMENT '剂型；药品制剂形态，如片剂、胶囊、注射液等。；值域: [AEROSOL，AEROSOL, FOAM，AEROSOL, METERED，AEROSOL, POWDER，AEROSOL, SPRAY，BAR, CHEWABLE，BEAD，CAPSULE，CAPSULE, COATED，CAPSULE, COATED PELLETS，CAPSULE, COATED, EXTENDED RELEASE，CAPSULE, DELAYED RELEASE，CAPSULE, DELAYED RELEASE PELLETS，CAPSULE, EXTENDED RELEASE，CAPSULE, FILM COATED, EXTENDED RELEASE，CAPSULE, GELATIN COATED，CAPSULE, LIQUID FILLED，CELLULAR SHEET，CHEWABLE GEL，CLOTH，CONCENTRATE，CREAM，CREAM, AUGMENTED，CRYSTAL，DISC，DOUCHE，DRESSING，DRUG-ELUTING CONTACT LENS，ELIXIR，EMULSION，ENEMA，EXTRACT，FIBER, EXTENDED RELEASE，FILM，FILM, EXTENDED RELEASE，FILM, SOLUBLE，FOR SOLUTION，FOR SUSPENSION，FOR SUSPENSION, EXTENDED RELEASE，GAS，GEL，GEL, DENTIFRICE，GEL, METERED，GLOBULE，GRANULE，GRANULE, DELAYED RELEASE，GRANULE, EFFERVESCENT，GRANULE, FOR SOLUTION，GRANULE, FOR SUSPENSION，GRANULE, FOR SUSPENSION, EXTENDED RELEASE，GUM, CHEWING，IMPLANT，INHALANT，INJECTABLE FOAM，INJECTABLE, LIPOSOMAL，INJECTION，INJECTION, EMULSION，INJECTION, LIPID COMPLEX，INJECTION, POWDER, FOR SOLUTION，INJECT…',
  `application_type` VARCHAR(32) NULL COMMENT '申请类型；监管申请类别，如 NDA、ANDA、BLA 等。；值域: [ANADA，ANDA，Approved Drug Product Manufactured Under Contract，BLA，Bulk ingredient，Bulk Ingredient For Animal Drug Compounding，Bulk Ingredient For Human Prescription Compounding，Conditional NADA，Cosmetic，Dietary Supplement，Drug for Further Processing，Emergency Use Authorization，Exempt device，Export only，Humanitarian Device Exemption，IND，Medical Food，Legally Marketed Unapproved New Animal Drugs for Minor Species，Multi-Market Approved Product，NADA，NDA，NDA authorized generic，OTC Monograph Drug，OTC Monograph Drug Product Manufactured Under Contract，Outsourcing Facility Compounded Human Drug Product (Exempt From Approval Requirements)，Outsourcing Facility Compounded Human Drug Product (Not Marketed - Not Distributed)，Premarket Application，Premarket Notification，SIP Approved Drug，Unapproved drug for use in drug shortage，Unapproved drug other，Unapproved Drug Product Manufactured Under Contract，Unapproved homeopathic，Unapproved medical gas]',
  `sponsor_name` VARCHAR(255) NULL COMMENT '申请机构全称；提交药品申请或持有上市许可的机构全称。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_drug_application_number` (`application_number`),
  KEY `idx_dwd_drug_drug_name` (`drug_name`),
  KEY `idx_dwd_drug_brand_name` (`brand_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='药品信息表';

-- ----------------------------------------------------------
-- 表: dwd_medical_device  (医疗器械表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_medical_device`;
CREATE TABLE `dwd_medical_device` (
  `id` VARCHAR(32) NOT NULL COMMENT '器械ID；医疗器械记录的唯一标识或来源库编码。',
  `device_name` VARCHAR(255) NOT NULL COMMENT '器械名称；医疗器械产品名称。',
  `device_type` VARCHAR(32) NULL COMMENT '器械类型；医疗器械的类别、用途或产品类型。',
  `device_id_issuing_agency` VARCHAR(255) NULL COMMENT '发行机构；器械标识或编码的发行机构。；值域: [GS1，HIBCC，ICCBBA]',
  `brand_name` VARCHAR(255) NULL COMMENT '品牌名称；医疗器械或产品使用的品牌名称。',
  `company_name` VARCHAR(255) NULL COMMENT '生产商名称；医疗器械生产企业或注册企业名称。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_medical_device_device_name` (`device_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='医疗器械表';

-- ----------------------------------------------------------
-- 表: dwd_clinical  (临床信息表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_clinical`;
CREATE TABLE `dwd_clinical` (
  `id` VARCHAR(32) NOT NULL COMMENT '治疗疾病ID；疾病或适应症在来源库中的唯一标识。',
  `disease_name` VARCHAR(255) NOT NULL COMMENT '治疗疾病名称；药物、试验或临床信息关联的疾病名称。',
  `phenotype_id` VARCHAR(32) NOT NULL COMMENT '临床表型ID；临床表型在标准术语库中的唯一标识。',
  `phenotype_name` VARCHAR(255) NOT NULL COMMENT '临床表型；疾病相关的临床表现、症状或表型名称。',
  `associated_gene` JSON NULL COMMENT '关联基因；与疾病、表型或多组学结果相关的基因名称。',
  `references` JSON NULL COMMENT '参考文献；支持该条记录的论文、数据库页面或 DOI 等来源信息。',
  `disease_category` JSON NULL COMMENT '疾病分类；疾病在 ICD、肿瘤分类或其他标准体系中的层级分类。',
  `symptoms` VARCHAR(512) NULL COMMENT '症状；疾病或临床表型相关的主要症状。',
  `related_disease` JSON NULL COMMENT '相关疾病；与当前疾病存在继发、共病、遗传或机制关联的疾病。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_clinical_disease_name` (`disease_name`),
  KEY `idx_dwd_clinical_phenotype_id` (`phenotype_id`),
  KEY `idx_dwd_clinical_phenotype_name` (`phenotype_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='临床信息表';

-- ----------------------------------------------------------
-- 表: dwd_market  (药品市场表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_market`;
CREATE TABLE `dwd_market` (
  `id` VARCHAR(32) NOT NULL COMMENT '市场id；药品市场对应的内部或来源库唯一标识。',
  `market_name` VARCHAR(512) NOT NULL COMMENT '市场名称；药品市场对应的国家、地区、治疗领域或细分市场名称。',
  `market_share` DOUBLE NOT NULL COMMENT '市场份额；目标药品、品类或仿制药在指定市场中的占比。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='药品市场表';

-- ----------------------------------------------------------
-- 表: dwd_company  (药品企业表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company`;
CREATE TABLE `dwd_company` (
  `id` VARCHAR(32) NOT NULL COMMENT '企业id；药品企业对应的内部或来源库唯一标识。',
  `firm_name` VARCHAR(512) NOT NULL COMMENT '企业名称；药品企业、生产企业或许可持有人名称。',
  `address` VARCHAR(1024) NOT NULL COMMENT '详细地址；企业注册地址、生产地址或经营地址。',
  `duns_number` JSON NULL COMMENT '邓白氏编码；企业的 D-U-N-S 编码，用于企业识别和外部数据关联。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='药品企业表';

-- ----------------------------------------------------------
-- 表: dwd_protein  (蛋白质表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_protein`;
CREATE TABLE `dwd_protein` (
  `id` VARCHAR(32) NOT NULL COMMENT '蛋白id；蛋白质对应的内部或来源库唯一标识。',
  `protein_name` VARCHAR(512) NOT NULL COMMENT '蛋白名称；蛋白质的标准名称或推荐名称。',
  `uniprot_id` VARCHAR(32) NOT NULL COMMENT 'UniProt 蛋白 ID；蛋白质在 UniProt 数据库中的唯一编号。',
  `gene_names` VARCHAR(255) NOT NULL COMMENT '基因名称；编码该蛋白的基因符号或别名。',
  `protein_length` INT NULL COMMENT '蛋白长度；蛋白质氨基酸序列长度。',
  `sequence` VARCHAR(1024) NULL COMMENT '氨基酸序列；蛋白质的一字母氨基酸序列。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_protein_protein_name` (`protein_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='蛋白质表';

-- ----------------------------------------------------------
-- 表: dwd_multi_omics  (多组学表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_multi_omics`;
CREATE TABLE `dwd_multi_omics` (
  `id` VARCHAR(32) NOT NULL COMMENT '组学id；多组学数据的内部或来源库唯一标识。',
  `data_category` VARCHAR(128) NULL COMMENT '数据类别；多组学数据的大类，如突变、表达、甲基化、蛋白组等。',
  `data_type` VARCHAR(128) NULL COMMENT '数据子类型；多组学数据的细分类型或文件类型。',
  `repository` VARCHAR(128) NULL COMMENT '来源库；多组学数据来源平台或数据库名称。',
  `experimental_strategy` VARCHAR(1024) NULL COMMENT '实验策略；产生该组学数据的实验或测序策略。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='多组学表';

-- ----------------------------------------------------------
-- 表: dwd_drug_profile  (药物档案表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_drug_profile`;
CREATE TABLE `dwd_drug_profile` (
  `id` VARCHAR(32) NOT NULL COMMENT '药物档案id；药物档案的内部或来源库唯一标识。',
  `brand_name` VARCHAR(255) NOT NULL COMMENT '商品名；药品上市销售时使用的品牌名称。',
  `indications_and_usage` LONGTEXT NOT NULL COMMENT '药物适应症和使用说明；药品标签中关于适应症、适用人群和使用场景的说明。',
  `mechanism_of_action` LONGTEXT NULL COMMENT '作用机制；药物发挥治疗作用的生物学或药理学机制。',
  `substance_name` JSON NULL COMMENT '活性成分；药品中具有治疗作用的主要成分，可包含一个或多个成分。',
  `contraindications` LONGTEXT NULL COMMENT '禁忌症；不应使用该药物的疾病、状态或用药条件。',
  `warnings_and_cautions` LONGTEXT NULL COMMENT '警示与注意事项；药品标签中的重要风险、警示和用药注意事项。',
  `adverse_reactions` LONGTEXT NULL COMMENT '不良反应；临床试验或上市后报告中记录的药物不良反应。',
  `dosage_and_administration` LONGTEXT NULL COMMENT '用法用量；药品推荐给药剂量、频率、调整方式和用药方法。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_drug_profile_brand_name` (`brand_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='药物档案表';

-- ----------------------------------------------------------
-- 表: dwd_safety  (药物安全表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_safety`;
CREATE TABLE `dwd_safety` (
  `id` VARCHAR(32) NOT NULL COMMENT '药物安全记录ID；药品安全记录的内部或来源库唯一标识。',
  `receivedate` DATE NULL COMMENT 'FEMA 接收日期；药物不良事件报告在 FAERS 等安全数据库中的接收日期。',
  `drug_name` VARCHAR(255) NULL COMMENT '药物名称；药物安全、交易或试验记录中涉及的药品名称。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_safety_drug_name` (`drug_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='药物安全表';

-- ----------------------------------------------------------
-- 表: dwd_clinical_trial  (临床试验信息表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_clinical_trial`;
CREATE TABLE `dwd_clinical_trial` (
  `id` VARCHAR(32) NOT NULL COMMENT '临床试验信息id；临床试验信息的内部或来源库唯一标识。',
  `trial_sponsor` VARCHAR(512) NULL COMMENT '临床试验标题；临床试验登记记录中的研究标题。',
  `disease_name` VARCHAR(255) NULL COMMENT '治疗疾病名称；药物、试验或临床信息关联的疾病名称。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='临床试验信息表';

-- ----------------------------------------------------------
-- 表: dwd_deal  (药物交易)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_deal`;
CREATE TABLE `dwd_deal` (
  `id` VARCHAR(32) NOT NULL COMMENT '药品交易id；药物交易的内部或来源库唯一标识。',
  `drug_name` VARCHAR(255) NULL COMMENT '药品名称；交易涉及的药品、候选药物或管线资产名称。',
  `licensor` VARCHAR(128) NULL COMMENT '授权方；在药物交易中授出研发、生产或商业化权益的公司。',
  `licensee` VARCHAR(128) NULL COMMENT '被授权方；在药物交易中获得相关权益的公司。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_deal_drug_name` (`drug_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='药物交易';

-- ----------------------------------------------------------
-- 表: dwd_drug_substance  (化合物性质与信息)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_drug_substance`;
CREATE TABLE `dwd_drug_substance` (
  `id` VARCHAR(32) NOT NULL COMMENT '化合物性质与信息id；化合物性质与信息的内部或来源库唯一标识。',
  `molecular_name` VARCHAR(512) NOT NULL COMMENT '分子名；化合物、材料或分子的标准英文名称。',
  `formula` VARCHAR(255) NOT NULL COMMENT '分子式；分子或晶体的化学组成式。',
  `in_chi_key` VARCHAR(64) NULL COMMENT 'InChIKey；InChI 的固定长度哈希标识，用于化合物快速匹配和去重。',
  `in_chi` TEXT NULL COMMENT 'InChI；化合物的 IUPAC 国际化学标识符。',
  `std_smiles` VARCHAR(4000) NULL COMMENT '标准smiles；化合物标准化后的 SMILES 结构表示。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_drug_substance_molecular_name` (`molecular_name`),
  KEY `idx_dwd_drug_substance_in_chi_key` (`in_chi_key`),
  KEY `idx_dwd_drug_substance_in_chi` (`in_chi`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='化合物性质与信息';

-- ----------------------------------------------------------
-- 表: dwd_crystal_structure  (晶体结构与性质)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_crystal_structure`;
CREATE TABLE `dwd_crystal_structure` (
  `id` VARCHAR(32) NOT NULL COMMENT '晶体结构与性质id；晶体结构与性质的内部或来源库唯一标识。',
  `formula` VARCHAR(100) NULL COMMENT '分子式；分子或晶体的化学组成式。',
  `diffraction_radiation_type` VARCHAR(128) NULL COMMENT '衍射辐射类型；晶体结构测定使用的 X 射线或中子衍射辐射类型。；值域: [CuKα，MoKα，AgKα，neutron，synchrotron，white-beam, CuKα1，CuKα2，CuK-L2,3，CoKα，CrKα，FeKα，synchrotron radiation，monochromatic synchrotron]',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='晶体结构与性质';

-- ----------------------------------------------------------
-- 表: dwd_calculation  (分子理论计算)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_calculation`;
CREATE TABLE `dwd_calculation` (
  `id` VARCHAR(32) NOT NULL COMMENT '分子理论计算id；分子理论计算的内部或来源库唯一标识。',
  `molecular_name` VARCHAR(255) NULL COMMENT '分子名；化合物、材料或分子的标准英文名称。',
  `reference` JSON NULL COMMENT '参考文献；支持该条记录的论文、数据库页面或 DOI 等来源信息。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_calculation_molecular_name` (`molecular_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='分子理论计算';

-- ----------------------------------------------------------
-- 表: dwd_material_virtual_structure  (材料虚拟结构)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_material_virtual_structure`;
CREATE TABLE `dwd_material_virtual_structure` (
  `id` VARCHAR(32) NOT NULL COMMENT '材料虚拟结构id；材料虚拟结构的内部或来源库唯一标识。',
  `material_name` VARCHAR(255) NULL COMMENT '材料名称；材料或晶体结构的名称。',
  `formula` VARCHAR(100) NULL COMMENT '化学式；材料的化学组成式。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='材料虚拟结构';

-- ----------------------------------------------------------
-- 表: dwd_small_molecule_screening  (小分子活性与筛选)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_small_molecule_screening`;
CREATE TABLE `dwd_small_molecule_screening` (
  `id` VARCHAR(32) NOT NULL COMMENT '小分子活性与筛选id；小分子活性与筛选的内部或来源库唯一标识。',
  `molecular_name` VARCHAR(255) NULL COMMENT '分子名；化合物、材料或分子的标准英文名称。',
  `reference` JSON NULL COMMENT '参考文献；支持该条记录的论文、数据库页面或 DOI 等来源信息。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_small_molecule_s_molecular_name` (`molecular_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='小分子活性与筛选';

-- ----------------------------------------------------------
-- 表: dwd_information  (医疗资讯)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_information`;
CREATE TABLE `dwd_information` (
  `id` VARCHAR(32) NOT NULL COMMENT '医疗资讯id；医疗资讯的内部或来源库唯一标识。',
  `information_title` VARCHAR(1024) NULL COMMENT '标题；医疗资讯的标题。',
  `information_time` DATE NULL COMMENT '发布时间；医疗资讯正式发布的日期或时间。',
  `information_content` TEXT NULL COMMENT '内容；医疗资讯正文或摘要内容。',
  `information_url` VARCHAR(255) NULL COMMENT '原文链接；医疗资讯来源页面的 URL。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='医疗资讯';

-- ----------------------------------------------------------
-- 表: dwd_job  (招聘)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_job`;
CREATE TABLE `dwd_job` (
  `id` VARCHAR(32) NOT NULL COMMENT '招聘id；招聘的内部或来源库唯一标识。',
  `job_title` VARCHAR(128) NULL COMMENT '职位名称；招聘岗位名称。',
  `company_name` VARCHAR(255) NULL COMMENT '公司名称；发布岗位的公司或机构名称。',
  `job_description` VARCHAR(512) NULL COMMENT '职位描述；岗位职责、任职要求或工作内容摘要。',
  `job_url` VARCHAR(512) NULL COMMENT '职位链接；招聘岗位详情页 URL。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='招聘';

-- ----------------------------------------------------------
-- 表: dwd_event  (会展)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 医药专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_event`;
CREATE TABLE `dwd_event` (
  `id` VARCHAR(32) NOT NULL COMMENT '会展id；会展的内部或来源库唯一标识。',
  `event_name` VARCHAR(512) NULL COMMENT '会展名称；医药或生命科学相关会议、展会名称。',
  `organizer` VARCHAR(255) NULL COMMENT '主办方；会议或展会的主办机构。',
  `start_date` DATE NULL COMMENT '开始日期；会议或展会开始日期。',
  `end_date` DATE NULL COMMENT '结束日期；会议或展会结束日期。',
  `event_url` VARCHAR(512) NULL COMMENT '会展链接；会议或展会官网或详情页 URL。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='会展';

-- ----------------------------------------------------------
-- 表: dwd_substance  (物质信息表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 化学专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_substance`;
CREATE TABLE `dwd_substance` (
  `id` VARCHAR(32) NOT NULL COMMENT '分子ID；分子或物质记录的唯一标识。',
  `en_name` VARCHAR(4000) NOT NULL COMMENT '物质名；物质的英文名称或标准名称。',
  `cas_registry_id` JSON NULL COMMENT 'CAS号；化学物质的 CAS Registry Number。',
  `formula` VARCHAR(512) NULL COMMENT '分子式；分子、化合物或晶体的化学组成式。',
  `synonym` JSON NULL COMMENT '同义词；化合物或物质的别名、商品名或历史名称。',
  `chemical_type` JSON NULL COMMENT '化学类型分类；物质的化学类别或结构分类。',
  `weight` DOUBLE NULL COMMENT '分子量；化合物的相对分子质量。',
  `iupac_name` TEXT NULL COMMENT 'IUPAC命名；化合物的系统性 IUPAC 名称。',
  `std_smiles` VARCHAR(4000) NULL COMMENT '分子标准SMILES表示；包含立体化学信息的 SMILES 表示。',
  `in_chi_key` VARCHAR(64) NULL COMMENT 'InChIKey；InChI 的固定长度哈希标识，用于化合物快速匹配和去重。',
  `in_chi` TEXT NULL COMMENT 'InChI；化合物的 IUPAC 国际化学标识符。',
  `heavy_atom_count` INT NULL COMMENT '重原子数；分子中非氢原子的数量。',
  `total_formal_charge` INT NULL COMMENT '形式电荷；分子的总形式电荷。',
  `complexity` INT NULL COMMENT '分子复杂度；基于结构特征计算的分子复杂度指标。',
  `isotope_atom_count` INT NULL COMMENT '同位素原子数；分子中同位素标记原子的数量。',
  `atom_chiral_count` VARCHAR(32) NULL COMMENT '手性中心 （明确/未明确）；分子中已明确和未明确构型的原子手性中心数量。',
  `bond_chiral_count` VARCHAR(32) NULL COMMENT '立体键数量（明确/未明确）；分子中已明确和未明确构型的立体键数量。',
  `covalent_unit_count` INT NULL COMMENT '共价单位数；分子结构中通过共价键连接形成的独立结构单元数量。',
  `xlogp` DOUBLE NULL COMMENT '脂水分配系数；化合物的 LogP，用于表征亲脂性。',
  `hydrogen_bond_donor_count` INT NULL COMMENT '氢键供体数；分子中可作为氢键供体的原子或基团数量。',
  `hydrogen_bond_acceptor_count` INT NULL COMMENT '氢键受体数；分子中可作为氢键受体的原子或基团数量。',
  `rotatable_bond_count` INT NULL COMMENT '可旋转键数；分子中可自由旋转的单键数量。',
  `tpsa` DOUBLE NULL COMMENT '极性表面积；分子的拓扑极性表面积，用于评估吸收和渗透性。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_substance_en_name` (`en_name`(255)),
  KEY `idx_dwd_substance_formula` (`formula`),
  KEY `idx_dwd_substance_iupac_name` (`iupac_name`(255)),
  KEY `idx_dwd_substance_std_smiles` (`std_smiles`(255)),
  KEY `idx_dwd_substance_in_chi_key` (`in_chi_key`),
  KEY `idx_dwd_substance_in_chi` (`in_chi`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='物质信息表';

-- ----------------------------------------------------------
-- 表: dwd_react_detail  (化学反应信息表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 化学专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_react_detail`;
CREATE TABLE `dwd_react_detail` (
  `id` VARCHAR(32) NOT NULL COMMENT '反应ID；化学反应记录的唯一标识。',
  `step_count` INT NULL COMMENT '反应步数；反应路线包含的步骤数量。',
  `reactants` JSON NULL COMMENT '反应物集合；参与反应的起始物、试剂或底物集合。',
  `products` JSON NULL COMMENT '产物集合；反应生成物或目标产物集合。',
  `yield_value` JSON NULL COMMENT '产率；目标产物的反应收率。',
  `catalyst` JSON NULL COMMENT '催化剂；反应中使用的催化剂或关键促进剂。',
  `temperature` INT NULL COMMENT '温度数值；反应温度的数值部分。',
  `temperature_unit` VARCHAR(32) NULL COMMENT '温度单位；反应温度使用的计量单位。；值域: °C',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='化学反应信息表';

-- ----------------------------------------------------------
-- 表: dwd_rel_reaction_substance  (反应-物质关联表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 化学专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_rel_reaction_substance`;
CREATE TABLE `dwd_rel_reaction_substance` (
  `id` BIGINT NOT NULL COMMENT '关联表ID；反应-物质关联记录主键。',
  `reaction_id` VARCHAR(32) NOT NULL COMMENT '反应ID；关联化学反应信息表的反应ID。',
  `substance_id` VARCHAR(32) NOT NULL COMMENT '物质ID；关联物质信息表的物质ID。',
  `substance_role` VARCHAR(32) NOT NULL COMMENT '物质角色；物质在反应中的角色。；值域: reactant/product/catalyst/solvent/reagent',
  `source_field` VARCHAR(32) NULL COMMENT '来源字段；关系来源于反应表中的哪个字段。；值域: reactants/products/catalyst/yield_value',
  `yield_value` DOUBLE NULL COMMENT '产率；当角色为产物时记录对应产率数值。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_rel_reaction_sub_reaction_id` (`reaction_id`),
  KEY `idx_dwd_rel_reaction_sub_substance_id` (`substance_id`),
  KEY `idx_dwd_rel_reaction_sub_substance_role` (`substance_role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='反应-物质关联表';

-- ----------------------------------------------------------
-- 表: dwd_molecular_spectrum  (分子谱图)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 化学专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_molecular_spectrum`;
CREATE TABLE `dwd_molecular_spectrum` (
  `id` VARCHAR(32) NOT NULL COMMENT '分子谱图id；唯一标识',
  `substance_id` VARCHAR(32) NOT NULL COMMENT '物质ID；关联到物质信息表的物质ID，用于将谱图归属到具体物质。',
  `en_name` VARCHAR(4000) NOT NULL COMMENT '分子名；化合物、材料或分子的标准英文名称。',
  `formula` VARCHAR(512) NOT NULL COMMENT '分子式；分子、化合物或晶体的化学组成式。',
  `ms_type` VARCHAR(32) NULL COMMENT '质谱级别；质谱数据级别，如 MS1 或 MS2。',
  `ion_mode` VARCHAR(32) NULL COMMENT '离子模式；质谱采集的离子极性模式，如正离子或负离子。',
  `ionization` VARCHAR(32) NULL COMMENT '电离方式；质谱电离方法，如 ESI、APCI、EI 等。',
  `collision_energy` VARCHAR(32) NULL COMMENT '碰撞能；MS/MS 碎裂过程使用的碰撞能设置。',
  `precursor_mz` DOUBLE NULL COMMENT '前体离子质荷比；MS/MS 采集时被选择碎裂的前体离子 m/z。',
  `precursor_type` VARCHAR(32) NULL COMMENT '前体离子类型；前体离子的加合物或离子形式。',
  `peaks` JSON NULL COMMENT '谱峰列表；谱图峰数据列表，通常包含 m/z、强度和相对强度。',
  `mass_to_charge_ratio` JSON NULL COMMENT '质荷比；谱峰或离子的 m/z 数值。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_molecular_spectr_substance_id` (`substance_id`),
  KEY `idx_dwd_molecular_spectr_en_name` (`en_name`(255)),
  KEY `idx_dwd_molecular_spectr_formula` (`formula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='分子谱图';

-- ----------------------------------------------------------
-- 表: dwd_similar_substance  (结构相近的其他分子)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 化学专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_similar_substance`;
CREATE TABLE `dwd_similar_substance` (
  `similar_substance_id` VARCHAR(32) NOT NULL COMMENT '相似物质ID；相似物质记录的唯一标识。',
  `en_name` VARCHAR(4000) NULL COMMENT '物质名；物质的英文名称或标准名称。',
  `cas_registry_id` JSON NULL COMMENT 'CAS号；化学物质的 CAS Registry Number。',
  `formula` VARCHAR(512) NULL COMMENT '分子式；分子、化合物或晶体的化学组成式。',
  `similar_paper_count` INT NULL COMMENT '相关论文数量；与相似分子相关的论文数量。',
  `similar_publication_count` INT NULL COMMENT '相关专利数量；与相似分子相关的专利或公开文献数量。',
  KEY `idx_dwd_similar_substanc_similar_substance_id` (`similar_substance_id`),
  KEY `idx_dwd_similar_substanc_en_name` (`en_name`(255)),
  KEY `idx_dwd_similar_substanc_formula` (`formula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='结构相近的其他分子';

-- ----------------------------------------------------------
-- 表: dwd_rel_substance_paper  (物质-论文关联表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 化学专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_rel_substance_paper`;
CREATE TABLE `dwd_rel_substance_paper` (
  `id` BIGINT NOT NULL COMMENT '论文信息关联表ID',
  `substance_id` VARCHAR(32) NOT NULL COMMENT '物质ID；分子或物质记录的唯一标识。',
  `paper_id` VARCHAR(64) NOT NULL COMMENT '论文id；论文记录ID。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_rel_substance_pa_substance_id` (`substance_id`),
  KEY `idx_dwd_rel_substance_pa_paper_id` (`paper_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='物质-论文关联表';

-- ----------------------------------------------------------
-- 表: dwd_ods_substance_patent  (物质-专利关联表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 化学专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_ods_substance_patent`;
CREATE TABLE `dwd_ods_substance_patent` (
  `id` BIGINT NOT NULL COMMENT '专利信息关联表ID',
  `substance_id` VARCHAR(32) NOT NULL COMMENT '物质ID；分子或物质记录的唯一标识。',
  `patent_id` VARCHAR(20) NOT NULL COMMENT '专利id(与DOCDB兼容)；与 DOCDB 兼容的专利记录唯一标识。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_ods_substance_pa_substance_id` (`substance_id`),
  KEY `idx_dwd_ods_substance_pa_patent_id` (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='物质-专利关联表';

-- ----------------------------------------------------------
-- 表: dwd_hycy_index  (海洋产业_指标库)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_index`;
CREATE TABLE `dwd_hycy_index` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `level` VARCHAR(255) NULL COMMENT '级别',
  `region` VARCHAR(255) NULL COMMENT '区域',
  `province` VARCHAR(255) NULL COMMENT '省份',
  `city` VARCHAR(255) NULL COMMENT '城市',
  `district` VARCHAR(255) NULL COMMENT '区县',
  `other_region` VARCHAR(255) NULL COMMENT '经济区',
  `statistical_date` VARCHAR(255) NULL COMMENT '统计时间',
  `scope` VARCHAR(255) NULL COMMENT '更新频次',
  `index_name` VARCHAR(255) NULL COMMENT '标准指标名称',
  `data` DOUBLE NULL COMMENT '标准数值',
  `unit` VARCHAR(255) NULL COMMENT '标准单位',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_指标库';

-- ----------------------------------------------------------
-- 表: dwd_hycy_aquatic_new_species  (海洋产业_水产新品种认定情况及育种单位统计表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_aquatic_new_species`;
CREATE TABLE `dwd_hycy_aquatic_new_species` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `reg_no` VARCHAR(255) NULL COMMENT '品种登记号',
  `name` VARCHAR(255) NULL COMMENT '品种名称',
  `breeding_unit` VARCHAR(255) NULL COMMENT '育种单位',
  `stat_date` VARCHAR(255) NULL COMMENT '时间',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_水产新品种认定情况及育种单位统计表';

-- ----------------------------------------------------------
-- 表: dwd_hycy_marine_energy_industry_carrier  (海洋产业_海洋能源创新平台载体名单)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_marine_energy_industry_carrier`;
CREATE TABLE `dwd_hycy_marine_energy_industry_carrier` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `name` VARCHAR(255) NULL COMMENT '创新载体名称',
  `category` VARCHAR(255) NULL COMMENT '载体类型',
  `level` VARCHAR(255) NULL COMMENT '级别',
  `charge_authority` VARCHAR(255) NULL COMMENT '主管部门',
  `support_unit_name` VARCHAR(255) NULL COMMENT '依托单位名称',
  `support_unit_flag` VARCHAR(255) NULL COMMENT '依托单位标识',
  `year` VARCHAR(255) NULL COMMENT '立项年度',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_海洋能源创新平台载体名单';

-- ----------------------------------------------------------
-- 表: dwd_hycy_offshore_fishing_company_evaluation  (海洋产业_全国远洋渔业企业履约评估表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_offshore_fishing_company_evaluation`;
CREATE TABLE `dwd_hycy_offshore_fishing_company_evaluation` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `category` VARCHAR(255) NULL COMMENT '指标类别',
  `first_index` VARCHAR(255) NULL COMMENT '一级指标',
  `sec_index` VARCHAR(255) NULL COMMENT '二级指标',
  `third_index` VARCHAR(255) NULL COMMENT '三级指标',
  `score` VARCHAR(255) NULL COMMENT '分',
  `remark` VARCHAR(255) NULL COMMENT '备注',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_全国远洋渔业企业履约评估表';

-- ----------------------------------------------------------
-- 表: dwd_hycy_sz_maritime_law_attorneys  (海洋产业_深圳海事海商律所及执业律师)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_sz_maritime_law_attorneys`;
CREATE TABLE `dwd_hycy_sz_maritime_law_attorneys` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `year` VARCHAR(255) NULL COMMENT '年份',
  `name` VARCHAR(255) NULL COMMENT '姓名',
  `gender` VARCHAR(255) NULL COMMENT '性别',
  `region` VARCHAR(255) NULL COMMENT '区域',
  `law_firm` VARCHAR(255) NULL COMMENT '所属律师事务所',
  `licensed_category` VARCHAR(255) NULL COMMENT '执业类别',
  `licensed_no` VARCHAR(255) NULL COMMENT '执业证号',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_深圳海事海商律所及执业律师';

-- ----------------------------------------------------------
-- 表: dwd_hycy_port_operation_license_form  (海洋产业_港口经营许可表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_port_operation_license_form`;
CREATE TABLE `dwd_hycy_port_operation_license_form` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `number` VARCHAR(255) NULL COMMENT '序号',
  `enterprise_name` VARCHAR(255) NULL COMMENT '企业名称',
  `legal_representative` VARCHAR(255) NULL COMMENT '法定代表人',
  `certificate_name` VARCHAR(255) NULL COMMENT '证件名称',
  `certificate_number` VARCHAR(255) NULL COMMENT '证件编号',
  `issuing_authority` VARCHAR(255) NULL COMMENT '发证机关',
  `registered_address` VARCHAR(255) NULL COMMENT '注册地址',
  `operating_area` VARCHAR(255) NULL COMMENT '经营地域',
  `business_type` VARCHAR(255) NULL COMMENT '经营业务类型',
  `business_place` VARCHAR(255) NULL COMMENT '经营场所所在港区',
  `dangerous_goods_operation_certificate` VARCHAR(255) NULL COMMENT '港口危险货物作业附证',
  `dangerous_goods_operation` VARCHAR(255) NULL COMMENT '从事危险货物港口作业情况',
  `certificate_start_date` VARCHAR(255) NULL COMMENT '证件起始日期',
  `certificate_end_date` VARCHAR(255) NULL COMMENT '证件终止日期',
  `certificate_validity_period` VARCHAR(255) NULL COMMENT '证件有效期',
  `certificate_status` VARCHAR(255) NULL COMMENT '证件状态',
  `remark` VARCHAR(255) NULL COMMENT '备注',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_港口经营许可表';

-- ----------------------------------------------------------
-- 表: dwd_hycy_international_shipping_certificate_effective_enterprise  (海洋产业_国际班轮运输经营资格登记证有效企业)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_international_shipping_certificate_effective_enterprise`;
CREATE TABLE `dwd_hycy_international_shipping_certificate_effective_enterprise` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `number` VARCHAR(255) NULL COMMENT '序号',
  `certificate_number` VARCHAR(255) NULL COMMENT '证件编号',
  `enterprise_chinese_name` VARCHAR(255) NULL COMMENT '企业中文名称',
  `enterprise_english_name` VARCHAR(255) NULL COMMENT '企业英文名称',
  `registered_address` VARCHAR(255) NULL COMMENT '注册地址',
  `business_line` VARCHAR(255) NULL COMMENT '业务种类',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_国际班轮运输经营资格登记证有效企业';

-- ----------------------------------------------------------
-- 表: dwd_hycy_shanghai_domestic_water_transportation_trading_director  (海洋产业_上海市国内水路运输经营名录)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_shanghai_domestic_water_transportation_trading_director`;
CREATE TABLE `dwd_hycy_shanghai_domestic_water_transportation_trading_director` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `certificate_number` VARCHAR(255) NULL COMMENT '证件编号',
  `enterprise_name` VARCHAR(255) NULL COMMENT '企业名称',
  `main_business_passenger_transport` VARCHAR(255) NULL COMMENT '主营旅客运输',
  `main_business_freight_transport` VARCHAR(255) NULL COMMENT '主营货物运输',
  `certificate_validity_period` VARCHAR(255) NULL COMMENT '证件有效期',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_上海市国内水路运输经营名录';

-- ----------------------------------------------------------
-- 表: dwd_hycy_international_shipping_agency_enterprises_registration  (海洋产业_国际船舶代理企业备案表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_international_shipping_agency_enterprises_registration`;
CREATE TABLE `dwd_hycy_international_shipping_agency_enterprises_registration` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `number` VARCHAR(255) NULL COMMENT '序号',
  `international_ship_agent_enterprise_name` VARCHAR(255) NULL COMMENT '国际船舶代理企业名称',
  `registered_address` VARCHAR(255) NULL COMMENT '注册地址',
  `record_receipt_number` VARCHAR(255) NULL COMMENT '备案回执文号',
  `annual_filing` VARCHAR(255) NULL COMMENT '备案年份',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_国际船舶代理企业备案表';

-- ----------------------------------------------------------
-- 表: dwd_hycy_pelagic_fishery_enterprises_performance_evaluation_resu  (海洋产业_远洋渔业企业履约评估结果)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_pelagic_fishery_enterprises_performance_evaluation_resu`;
CREATE TABLE `dwd_hycy_pelagic_fishery_enterprises_performance_evaluation_resu` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `number` VARCHAR(255) NULL COMMENT '序号',
  `enterprise_name` VARCHAR(255) NULL COMMENT '企业名称',
  `score` DOUBLE NULL COMMENT '得分',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_远洋渔业企业履约评估结果';

-- ----------------------------------------------------------
-- 表: dwd_hycy_aquaculture_veterinary_drugs_enterprise_list  (海洋产业_水产养殖用兽药名录)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_aquaculture_veterinary_drugs_enterprise_list`;
CREATE TABLE `dwd_hycy_aquaculture_veterinary_drugs_enterprise_list` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `enterprise_name` VARCHAR(255) NULL COMMENT '企业名称',
  `common_name` VARCHAR(255) NULL COMMENT '通用名',
  `specifications` VARCHAR(255) NULL COMMENT '规格',
  `trade_name` VARCHAR(255) NULL COMMENT '商品名',
  `approval_number` VARCHAR(255) NULL COMMENT '批准文号',
  `approval_date` DATE NULL COMMENT '批准日期',
  `validity_period` DATE NULL COMMENT '有效期至',
  `failure_reason` VARCHAR(255) NULL COMMENT '失效原因',
  `change_situation` VARCHAR(255) NULL COMMENT '变更情况',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_水产养殖用兽药名录';

-- ----------------------------------------------------------
-- 表: dwd_hycy_nvocc_operator_list  (海洋产业_无船承运业务经营者名录)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_nvocc_operator_list`;
CREATE TABLE `dwd_hycy_nvocc_operator_list` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `enterprise_chinese_name` VARCHAR(255) NULL COMMENT '企业中文名称',
  `enterprise_english_name` VARCHAR(255) NULL COMMENT '企业英文名称',
  `enterprise_english_short_name` VARCHAR(255) NULL COMMENT '企业英文简称',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_无船承运业务经营者名录';

-- ----------------------------------------------------------
-- 表: dwd_hycy_china_classification_society_marine_product_list  (海洋产业_中国船级社船用产品目录)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_china_classification_society_marine_product_list`;
CREATE TABLE `dwd_hycy_china_classification_society_marine_product_list` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `certificate_number` VARCHAR(255) NULL COMMENT '证件编号',
  `work_type` VARCHAR(255) NULL COMMENT '工作类型',
  `validity_period` DATE NULL COMMENT '有效期至',
  `product_name` VARCHAR(255) NULL COMMENT '产品名称',
  `factory_name` VARCHAR(255) NULL COMMENT '工厂名称',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_中国船级社船用产品目录';

-- ----------------------------------------------------------
-- 表: dwd_hycy_csad_ship  (海洋产业_CSAD船舶)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_csad_ship`;
CREATE TABLE `dwd_hycy_csad_ship` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `ship_registration_no` VARCHAR(255) NULL COMMENT '船检登记号',
  `ship_name` VARCHAR(255) NULL COMMENT '船名',
  `haihe_river_ship` VARCHAR(255) NULL COMMENT '海河船',
  `gross_tonnage` VARCHAR(255) NULL COMMENT '总吨位',
  `ship_type` VARCHAR(255) NULL COMMENT '船舶类型',
  `ship_owner` VARCHAR(255) NULL COMMENT '船舶所有人',
  `ship_operator` VARCHAR(255) NULL COMMENT '船舶经营人',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_CSAD船舶';

-- ----------------------------------------------------------
-- 表: dwd_hycy_enterprise_indicators  (海洋产业_企业指标表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_enterprise_indicators`;
CREATE TABLE `dwd_hycy_enterprise_indicators` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `enterprise_name` VARCHAR(255) NULL COMMENT '企业名称',
  `statistical_date` VARCHAR(255) NULL COMMENT '统计时间',
  `update_frequency` VARCHAR(255) NULL COMMENT '更新频次',
  `index_name` VARCHAR(255) NULL COMMENT '标准指标名称',
  `data` DOUBLE NULL COMMENT '标准数值',
  `unit` VARCHAR(255) NULL COMMENT '标准单位',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_企业指标表';

-- ----------------------------------------------------------
-- 表: dwd_hycy_global_cruise_capacity_distribution  (海洋产业_全球邮轮运力分布)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_global_cruise_capacity_distribution`;
CREATE TABLE `dwd_hycy_global_cruise_capacity_distribution` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `ship_type` VARCHAR(255) NULL COMMENT '船型',
  `ship_age_range` VARCHAR(255) NULL COMMENT '船龄范围',
  `index_name` VARCHAR(255) NULL COMMENT '指标名称',
  `data` DOUBLE NULL COMMENT '标准数值',
  `unit` VARCHAR(255) NULL COMMENT '标准单位',
  `statistical_date` VARCHAR(255) NULL COMMENT '统计时间',
  `update_frequency` VARCHAR(255) NULL COMMENT '更新频次',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_全球邮轮运力分布';

-- ----------------------------------------------------------
-- 表: dwd_hycy_china_offshore_field  (海洋产业_中国海上油气田信息)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_china_offshore_field`;
CREATE TABLE `dwd_hycy_china_offshore_field` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `oilfield_name` VARCHAR(255) NULL COMMENT '油田名称',
  `operator_name` VARCHAR(255) NULL COMMENT '运营主体名称',
  `reserves` VARCHAR(255) NULL COMMENT '储量',
  `production_scale` VARCHAR(255) NULL COMMENT '产量规模',
  `geological_features` VARCHAR(255) NULL COMMENT '地质特点',
  `statistical_date` VARCHAR(255) NULL COMMENT '统计时间',
  `update_frequency` VARCHAR(255) NULL COMMENT '更新频次',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_中国海上油气田信息';

-- ----------------------------------------------------------
-- 表: dwd_hycy_china_major_city_lng_receiving_capacity  (海洋产业_中国主要城市LNG接收能力)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_china_major_city_lng_receiving_capacity`;
CREATE TABLE `dwd_hycy_china_major_city_lng_receiving_capacity` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `city_name` VARCHAR(255) NULL COMMENT '城市名称',
  `receipt_capacity` DOUBLE NULL COMMENT '接收能力',
  `receipt_unit` VARCHAR(255) NULL COMMENT '接收单位',
  `rank` DOUBLE NULL COMMENT '排名',
  `lng_receipt_station` VARCHAR(255) NULL COMMENT 'LNG接收站',
  `statistical_date` VARCHAR(255) NULL COMMENT '统计时间',
  `update_frequency` VARCHAR(255) NULL COMMENT '更新频次',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_中国主要城市LNG接收能力';

-- ----------------------------------------------------------
-- 表: dwd_hycy_china_offshore_production_growth  (海洋产业_中国海洋油气产量增长情况)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_china_offshore_production_growth`;
CREATE TABLE `dwd_hycy_china_offshore_production_growth` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `rank` DOUBLE NULL COMMENT '排名',
  `oilfield_name` VARCHAR(255) NULL COMMENT '油田名称',
  `oge` DOUBLE NULL COMMENT '油气当量',
  `oge_unit` VARCHAR(255) NULL COMMENT '油气单位',
  `statistical_date` VARCHAR(255) NULL COMMENT '统计时间',
  `remark` VARCHAR(255) NULL COMMENT '备注',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_中国海洋油气产量增长情况';

-- ----------------------------------------------------------
-- 表: dwd_hycy_china_offshore_production  (海洋产业_中国海洋油气田产量情况)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_china_offshore_production`;
CREATE TABLE `dwd_hycy_china_offshore_production` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `year` DOUBLE NULL COMMENT '年份',
  `oil_output` VARCHAR(255) NULL COMMENT '海洋原油产量',
  `gas_output` VARCHAR(255) NULL COMMENT '海洋天然气产量',
  `oil_gas_total_output` VARCHAR(255) NULL COMMENT '海洋油气总产量',
  `update_frequency` VARCHAR(255) NULL COMMENT '更新频次',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_中国海洋油气田产量情况';

-- ----------------------------------------------------------
-- 表: dwd_hycy_leading_maritime_capitals  (海洋产业_世界领先海事之都报告城市数据)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_leading_maritime_capitals`;
CREATE TABLE `dwd_hycy_leading_maritime_capitals` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `rank_name` VARCHAR(255) NULL COMMENT '榜单名称',
  `first_level_index` VARCHAR(255) NULL COMMENT '一级指标',
  `second_level_index` VARCHAR(255) NULL COMMENT '二级指标',
  `rank` DOUBLE NULL COMMENT '排名',
  `statistical_date` VARCHAR(255) NULL COMMENT '统计时间',
  `city_name` VARCHAR(255) NULL COMMENT '城市名称',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_世界领先海事之都报告城市数据';

-- ----------------------------------------------------------
-- 表: dwd_hycy_submarine_cable_distribution  (海洋产业_海底光缆分布)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_submarine_cable_distribution`;
CREATE TABLE `dwd_hycy_submarine_cable_distribution` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `category` VARCHAR(255) NULL COMMENT '类别',
  `region` VARCHAR(255) NULL COMMENT '区域',
  `submarine_cable` DOUBLE NULL COMMENT '海底光缆条数',
  `connection_point` DOUBLE NULL COMMENT '链接点个数',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_海底光缆分布';

-- ----------------------------------------------------------
-- 表: dwd_hycy_china_ocean_large_model  (海洋产业_国内海洋大模型情况)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_china_ocean_large_model`;
CREATE TABLE `dwd_hycy_china_ocean_large_model` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `model_name` VARCHAR(255) NULL COMMENT '大模型名称',
  `research_entity_name` VARCHAR(255) NULL COMMENT '研发主体名称',
  `research_entity_city` VARCHAR(255) NULL COMMENT '主体所在城市',
  `domain_oriented` VARCHAR(255) NULL COMMENT '面向领域',
  `features_progress` VARCHAR(255) NULL COMMENT '技术特点与进展',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_国内海洋大模型情况';

-- ----------------------------------------------------------
-- 表: dwd_hycy_china_mainland_submarine_cable  (海洋产业_中国大陆地区海底光缆情况)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_china_mainland_submarine_cable`;
CREATE TABLE `dwd_hycy_china_mainland_submarine_cable` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `province_code` VARCHAR(255) NULL COMMENT '省份代码',
  `province_name` VARCHAR(255) NULL COMMENT '省份名称',
  `city_code` VARCHAR(255) NULL COMMENT '城市代码',
  `city_name` VARCHAR(255) NULL COMMENT '城市名称',
  `cable_name` VARCHAR(255) NULL COMMENT '光缆名称',
  `bandwidth` VARCHAR(255) NULL COMMENT '带宽',
  `length` VARCHAR(255) NULL COMMENT '长度',
  `origin_region` VARCHAR(255) NULL COMMENT '起始地区',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_中国大陆地区海底光缆情况';

-- ----------------------------------------------------------
-- 表: dwd_hycy_methanol_production_cost_trend_prediction  (海洋产业_甲醇生产成本及趋势预测)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_methanol_production_cost_trend_prediction`;
CREATE TABLE `dwd_hycy_methanol_production_cost_trend_prediction` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `first_level` VARCHAR(255) NULL COMMENT '一级分类',
  `second_level` VARCHAR(255) NULL COMMENT '二级分类',
  `current_production_cost` VARCHAR(255) NULL COMMENT '当前生产成本',
  `forward_production_cost` VARCHAR(255) NULL COMMENT '远期生产成本',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_甲醇生产成本及趋势预测';

-- ----------------------------------------------------------
-- 表: dwd_hycy_ship_management_enterprise_trustee_ship  (海洋产业_船舶管理企业代管船舶表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_ship_management_enterprise_trustee_ship`;
CREATE TABLE `dwd_hycy_ship_management_enterprise_trustee_ship` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `province_code` VARCHAR(255) NULL COMMENT '省份代码',
  `province_name` VARCHAR(255) NULL COMMENT '省份名称',
  `city_code` VARCHAR(255) NULL COMMENT '城市代码',
  `city_name` VARCHAR(255) NULL COMMENT '城市名称',
  `enterprise_name` VARCHAR(255) NULL COMMENT '企业名称',
  `trustee_type` VARCHAR(255) NULL COMMENT '代管类型',
  `is_water_transport_qualification` VARCHAR(255) NULL COMMENT '是否同时具有水路运输经营资格',
  `is_international_ship_management` VARCHAR(255) NULL COMMENT '是否兼营国际船舶管理',
  `is_domestic_ship_management` VARCHAR(255) NULL COMMENT '是否兼营国内船舶管理',
  `trustee_ship_count` DOUBLE NULL COMMENT '代管船舶数量',
  `total_tonnage` DOUBLE NULL COMMENT '总吨合计',
  `business_scope` VARCHAR(255) NULL COMMENT '经营范围',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_船舶管理企业代管船舶表';

-- ----------------------------------------------------------
-- 表: dwd_hycy_gas_supply  (海洋产业_天然气供应信息表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_gas_supply`;
CREATE TABLE `dwd_hycy_gas_supply` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `province_code` VARCHAR(255) NULL COMMENT '省份代码',
  `province_name` VARCHAR(255) NULL COMMENT '省份名称',
  `city_code` VARCHAR(255) NULL COMMENT '城市代码',
  `city_name` VARCHAR(255) NULL COMMENT '城市名称',
  `gas_source_name` VARCHAR(255) NULL COMMENT '气源名称',
  `gas_source_type` VARCHAR(255) NULL COMMENT '气源类型',
  `gas_source_origin` VARCHAR(255) NULL COMMENT '气源来源',
  `ownership_structure` VARCHAR(255) NULL COMMENT '股权结构',
  `tank_capacity` DOUBLE NULL COMMENT '储罐规模',
  `tank_capacity_unit` VARCHAR(255) NULL COMMENT '储罐规模单位',
  `annual_supply_capacity` DOUBLE NULL COMMENT '年供应能力',
  `annual_supply_capacity_unit` VARCHAR(255) NULL COMMENT '年供应能力单位',
  `is_lng_refill_capability` VARCHAR(255) NULL COMMENT '是否具备LNG补液功能',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_天然气供应信息表';

-- ----------------------------------------------------------
-- 表: dwd_hycy_green_fuel_enterprise  (海洋产业_绿色燃料加注产业信息表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_green_fuel_enterprise`;
CREATE TABLE `dwd_hycy_green_fuel_enterprise` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `province_code` VARCHAR(255) NULL COMMENT '省份代码',
  `province_name` VARCHAR(255) NULL COMMENT '省份名称',
  `city_code` VARCHAR(255) NULL COMMENT '城市代码',
  `city_name` VARCHAR(255) NULL COMMENT '城市名称',
  `industry_chain_link` VARCHAR(255) NULL COMMENT '产业链环节',
  `enterprise_name` VARCHAR(255) NULL COMMENT '企业名称',
  `core_product_service` VARCHAR(255) NULL COMMENT '优势产品或服务',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_绿色燃料加注产业信息表';

-- ----------------------------------------------------------
-- 表: dwd_hycy_shipping_capacity  (海洋产业_航运运力表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_shipping_capacity`;
CREATE TABLE `dwd_hycy_shipping_capacity` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `province_code` VARCHAR(255) NULL COMMENT '省份代码',
  `province_name` VARCHAR(255) NULL COMMENT '省份名称',
  `city_code` VARCHAR(255) NULL COMMENT '城市代码',
  `city_name` VARCHAR(255) NULL COMMENT '城市名称',
  `statistical_type` VARCHAR(255) NULL COMMENT '统计类型',
  `enterprise_name` VARCHAR(255) NULL COMMENT '企业名称',
  `enterprise_type` VARCHAR(255) NULL COMMENT '企业类型',
  `vessel_type` VARCHAR(255) NULL COMMENT '船舶类型',
  `vessels` DOUBLE NULL COMMENT '船舶总数',
  `hong_kong_macao_vessels` DOUBLE NULL COMMENT '港澳通航船舶数量',
  `inland_vessels` DOUBLE NULL COMMENT '内陆通航船舶数量',
  `international_vessels` DOUBLE NULL COMMENT '国际通航船舶数量',
  `passenger_capacity` DOUBLE NULL COMMENT '客位数',
  `gross_tonnage` DOUBLE NULL COMMENT '总吨数',
  `deadweight_tonnage` DOUBLE NULL COMMENT '载重吨',
  `teu_capacity` DOUBLE NULL COMMENT 'TEU',
  `cubic_meter_capacity` DOUBLE NULL COMMENT '立方米',
  `car_capacity` DOUBLE NULL COMMENT '车位',
  `statistical_date` VARCHAR(255) NULL COMMENT '统计时间',
  `update_frequency` VARCHAR(255) NULL COMMENT '更新频次',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_航运运力表';

-- ----------------------------------------------------------
-- 表: dwd_hycy_marine_alternative_fuel_cost  (海洋产业_船用替代燃料生产成本对比表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_marine_alternative_fuel_cost`;
CREATE TABLE `dwd_hycy_marine_alternative_fuel_cost` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `fuel_category` VARCHAR(255) NULL COMMENT '燃料类别',
  `fuel_type` VARCHAR(255) NULL COMMENT '燃料类型',
  `production_route` VARCHAR(255) NULL COMMENT '生产路线',
  `current_production_cost` VARCHAR(255) NULL COMMENT '当前生产成本',
  `future_production_cost` VARCHAR(255) NULL COMMENT '远期生产成本',
  `cost_currency` VARCHAR(255) NULL COMMENT '成本货币单位',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_船用替代燃料生产成本对比表';

-- ----------------------------------------------------------
-- 表: dwd_hycy_global_alternative_marine_fuel_market_demand_scale  (海洋产业_船用替代燃料全球市场需求及规模预测)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hycy_global_alternative_marine_fuel_market_demand_scale`;
CREATE TABLE `dwd_hycy_global_alternative_marine_fuel_market_demand_scale` (
  `logic_id` VARCHAR(255) NOT NULL COMMENT '逻辑主键',
  `fuel_category` VARCHAR(255) NULL COMMENT '燃料类别',
  `year` VARCHAR(255) NULL COMMENT '年份',
  `market_demand` VARCHAR(255) NULL COMMENT '市场需求',
  `market_scale` VARCHAR(255) NULL COMMENT '市场规模',
  PRIMARY KEY (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋产业_船用替代燃料全球市场需求及规模预测';

-- ----------------------------------------------------------
-- 表: dwd_hai_yang_shi_ce_shu_ju  (海洋实测数据)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hai_yang_shi_ce_shu_ju`;
CREATE TABLE `dwd_hai_yang_shi_ce_shu_ju` (
  `zhu_jian` VARCHAR(255) NOT NULL COMMENT '主键',
  `shui_wen_qi_xiang_sheng_wu_hua_xue` VARCHAR(255) NULL COMMENT '水文/气象/生物/化学',
  `zhan_dian_ming_cheng` VARCHAR(255) NULL COMMENT '站点名称',
  `jing_du` DOUBLE NULL COMMENT '经度',
  `wei_du` DOUBLE NULL COMMENT '纬度',
  `guan_ce_shi_jian` DATETIME NULL COMMENT '观测时间',
  `shui_wen` DOUBLE NULL COMMENT '水温',
  `yan_du` DOUBLE NULL COMMENT '盐度',
  `feng_su` DOUBLE NULL COMMENT '风速',
  `feng_xiang` VARCHAR(255) NULL COMMENT '风向',
  `pH_zhi` DOUBLE NULL COMMENT 'pH值',
  `rong_jie_yang` DOUBLE NULL COMMENT '溶解氧',
  `sheng_wu_ming_cheng` VARCHAR(255) NULL COMMENT '生物名称',
  `shu_liang` INT NULL COMMENT '数量',
  `geng_xin_shi_jian` DATETIME NULL COMMENT '更新时间',
  PRIMARY KEY (`zhu_jian`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋实测数据';

-- ----------------------------------------------------------
-- 表: dwd_hai_yang_fen_xi_yu_bao_shu_ju  (海洋分析预报数据)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hai_yang_fen_xi_yu_bao_shu_ju`;
CREATE TABLE `dwd_hai_yang_fen_xi_yu_bao_shu_ju` (
  `zhu_jian` VARCHAR(255) NOT NULL COMMENT '主键',
  `shi_kuang_fen_xi_tong_ji_fen_xi` VARCHAR(255) NULL COMMENT '实况分析/统计分析',
  `qu_yu` VARCHAR(255) NULL COMMENT '区域',
  `fen_xi_shi_jian` DATETIME NULL COMMENT '分析时间',
  `yu_bao_shi_jian` DATETIME NULL COMMENT '预报时间',
  `lang_gao` DOUBLE NULL COMMENT '浪高',
  `tian_qi_zhuang_kuang` VARCHAR(255) NULL COMMENT '天气状况',
  `fen_xi_nei_rong` VARCHAR(255) NULL COMMENT '分析内容',
  `geng_xin_shi_jian` DATETIME NULL COMMENT '更新时间',
  PRIMARY KEY (`zhu_jian`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋分析预报数据';

-- ----------------------------------------------------------
-- 表: dwd_hai_yang_di_li_yao_gan_shu_ju  (海洋地理遥感数据)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_hai_yang_di_li_yao_gan_shu_ju`;
CREATE TABLE `dwd_hai_yang_di_li_yao_gan_shu_ju` (
  `zhu_jian` VARCHAR(255) NOT NULL COMMENT '主键',
  `jin_hai_yao_gan_bei_bing_yang_yao_gan_shi_liang_di_tu` VARCHAR(255) NULL COMMENT '近海遥感/北冰洋遥感/矢量地图',
  `wei_xing_ming_cheng` VARCHAR(255) NULL COMMENT '卫星名称',
  `pai_she_shi_jian` DATETIME NULL COMMENT '拍摄时间',
  `qu_yu` VARCHAR(255) NULL COMMENT '区域',
  `fen_bian_lv` VARCHAR(255) NULL COMMENT '分辨率',
  `ying_xiang_di_zhi` VARCHAR(255) NULL COMMENT '影像地址',
  `shu_ju_shuo_ming` VARCHAR(255) NULL COMMENT '数据说明',
  `geng_xin_shi_jian` DATETIME NULL COMMENT '更新时间',
  PRIMARY KEY (`zhu_jian`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海洋地理遥感数据';

-- ----------------------------------------------------------
-- 表: dwd_shang_lian_jie_guo_biao  (上链结果表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 海洋专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_shang_lian_jie_guo_biao`;
CREATE TABLE `dwd_shang_lian_jie_guo_biao` (
  `zhu_jian` INT NOT NULL COMMENT '主键',
  `lei_xing` VARCHAR(255) NULL COMMENT '类型；001：企业、002：专利、等等',
  `chan_ye_lian_ID` INT NULL COMMENT '产业链ID',
  `shi_ti_ID` INT NULL COMMENT '实体ID',
  `chan_ye_bian_ma` VARCHAR(255) NULL COMMENT '产业编码',
  `chan_ye_ming_cheng` VARCHAR(255) NULL COMMENT '产业名称',
  `huan_jie_bian_ma` VARCHAR(255) NULL COMMENT '环节编码',
  `huan_jie_ming_cheng` VARCHAR(255) NULL COMMENT '环节名称',
  `gua_lian_shi_jian` DATETIME NULL COMMENT '挂链时间',
  `gua_lian_ren` VARCHAR(255) NULL COMMENT '挂链人',
  PRIMARY KEY (`zhu_jian`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='上链结果表';

-- ----------------------------------------------------------
-- 表: dwd_industry_code  (产业链)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_industry_code`;
CREATE TABLE `dwd_industry_code` (
  `id` DOUBLE NOT NULL COMMENT 'id',
  `code` VARCHAR(255) NULL COMMENT '环节编码',
  `name` VARCHAR(255) NULL COMMENT '环节名称',
  `parent_code` VARCHAR(255) NULL COMMENT '父级编码',
  `industry_code` VARCHAR(255) NULL COMMENT '产业编码',
  `industry_name` VARCHAR(255) NULL COMMENT '产业名称',
  `level` DOUBLE NULL COMMENT '级别',
  `definition` VARCHAR(255) NULL COMMENT '定义',
  `is_key_link` DOUBLE NULL COMMENT '是否为关键环节',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='产业链';

-- ----------------------------------------------------------
-- 表: dwd_company_base  (基础信息)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_base`;
CREATE TABLE `dwd_company_base` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `name` VARCHAR(255) NULL COMMENT '企业名称',
  `source_id` VARCHAR(255) NULL COMMENT '来源编码',
  `english_name` VARCHAR(255) NULL COMMENT '企业英文名称',
  `registration_code` VARCHAR(255) NULL COMMENT '注册号',
  `organization_code` VARCHAR(255) NULL COMMENT '组织机构号',
  `credit_code` VARCHAR(255) NULL COMMENT '统一信用代码',
  `first_type` VARCHAR(255) NULL COMMENT '标准化后的企业类型',
  `second_type` VARCHAR(255) NULL COMMENT '标准化后的企业类型',
  `detail_type` VARCHAR(255) NULL COMMENT '标准化后的企业类型',
  `registered_capital` VARCHAR(255) NULL COMMENT '注册资本',
  `registered_add` VARCHAR(255) NULL COMMENT '注册地址',
  `scope` VARCHAR(255) NULL COMMENT '经营范围',
  `start_date` VARCHAR(255) NULL COMMENT '营业期限开始日期',
  `end_date` VARCHAR(255) NULL COMMENT '营业期限终止日期',
  `reg_organization` VARCHAR(255) NULL COMMENT '登记机关',
  `legal_representative` VARCHAR(255) NULL COMMENT '法人姓名',
  `legal_rep_type` DOUBLE NULL COMMENT '法人类型',
  `approval_date` VARCHAR(255) NULL COMMENT '核准日期',
  `establish_date` VARCHAR(255) NULL COMMENT '成立日期',
  `cancel_date` VARCHAR(255) NULL COMMENT '注销日期',
  `status_std` VARCHAR(255) NULL COMMENT '企业状态',
  `display` DOUBLE NULL COMMENT '企业状态',
  `reg_capital_std` DOUBLE NULL COMMENT '注册资本金额',
  `unit` VARCHAR(255) NULL COMMENT '注册资本单位',
  `currency` VARCHAR(255) NULL COMMENT '注册资本币种',
  `real_capital` VARCHAR(255) NULL COMMENT '实缴资本',
  `real_capital_std` DOUBLE NULL COMMENT '实缴资本金额',
  `cancel_reason` VARCHAR(255) NULL COMMENT '注销原因',
  `ori_reg_city` VARCHAR(255) NULL COMMENT '注册地所在市',
  `ori_reg_district` VARCHAR(255) NULL COMMENT '注册的所在区',
  `ori_reg_province` VARCHAR(255) NULL COMMENT '注册地所在省',
  `reg_xy` VARCHAR(255) NULL COMMENT '经度',
  `is_deleted` DOUBLE NULL COMMENT '使用标记',
  `create_time` DATE NULL COMMENT '创建时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='基础信息';

-- ----------------------------------------------------------
-- 表: dwd_company_branch  (分支机构)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_branch`;
CREATE TABLE `dwd_company_branch` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `source_id` VARCHAR(255) NULL COMMENT '唯一键',
  `branch_id` DOUBLE NULL COMMENT '分支机构的主体唯一键',
  `branch_name` VARCHAR(255) NULL COMMENT '分支机构名称',
  `branch_reg_code` VARCHAR(255) NULL COMMENT '分支机构注册号',
  `branch_credit_code` VARCHAR(255) NULL COMMENT '分支机构统一信用代码',
  `branch_establish_date` VARCHAR(255) NULL COMMENT '分支机构成立日期',
  `branch_company_status` VARCHAR(255) NULL COMMENT '登记状态',
  `branch_cancel_date` VARCHAR(255) NULL COMMENT '注销日期',
  `is_history` DOUBLE NULL COMMENT '使用标记',
  `is_deleted` DOUBLE NULL COMMENT '使用标记',
  `create_time` DATE NULL COMMENT '入库时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='分支机构';

-- ----------------------------------------------------------
-- 表: dwd_company_change  (工商变更)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_change`;
CREATE TABLE `dwd_company_change` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `source_id` VARCHAR(255) NULL COMMENT '唯一键',
  `before` VARCHAR(255) NULL COMMENT '变更前内容',
  `after` VARCHAR(255) NULL COMMENT '变更后内容',
  `date` VARCHAR(255) NULL COMMENT '变更日期',
  `change_type` VARCHAR(255) NULL COMMENT '变更类型(法定代表人变更, 主要人员变更, 经营范围变更, 注册资本变更, 股东信息变更, address, business, lp)',
  `change_type_std` VARCHAR(255) NULL COMMENT '变更类型(法定代表人变更, 主要人员变更, 经营范围变更, 注册资本变更, 股东信息变更)',
  `change_type_detail` VARCHAR(255) NULL COMMENT '变更类型详情',
  `is_deleted` DOUBLE NULL COMMENT '使用标记',
  `create_time` DATE NULL COMMENT '入库时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='工商变更';

-- ----------------------------------------------------------
-- 表: dwd_company_history_name  (曾用名)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_history_name`;
CREATE TABLE `dwd_company_history_name` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `source_id` VARCHAR(255) NULL COMMENT '唯一键',
  `history_name` VARCHAR(255) NULL COMMENT '曾用名',
  `start_date` VARCHAR(255) NULL COMMENT '名称开始使用日期',
  `end_date` VARCHAR(255) NULL COMMENT '名称结束使用日期',
  `is_deleted` DOUBLE NULL COMMENT '使用标记',
  `create_time` DATE NULL COMMENT '创建时间',
  `update_time` DATE NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='曾用名';

-- ----------------------------------------------------------
-- 表: dwd_company_license  (行政许可)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_license`;
CREATE TABLE `dwd_company_license` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `source_id` VARCHAR(255) NULL COMMENT '唯一键',
  `name` VARCHAR(255) NULL COMMENT '许可证名称',
  `license_code` VARCHAR(255) NULL COMMENT '许可文件编号',
  `scope` VARCHAR(255) NULL COMMENT '许可内容',
  `start_date` VARCHAR(255) NULL COMMENT '有效期自',
  `end_date` VARCHAR(255) NULL COMMENT '有效期至',
  `organization` VARCHAR(255) NULL COMMENT '许可机关',
  `is_history` DOUBLE NULL COMMENT '状态',
  `is_deleted` DOUBLE NULL COMMENT '使用标记',
  `create_time` DATE NULL COMMENT '入库时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='行政许可';

-- ----------------------------------------------------------
-- 表: dwd_company_nei_code  (国民行业经济分类)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_nei_code`;
CREATE TABLE `dwd_company_nei_code` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `source_id` VARCHAR(255) NULL COMMENT '唯一键',
  `industry` VARCHAR(255) NULL COMMENT '最深一级的行业名称',
  `industry_l1_code` VARCHAR(255) NULL COMMENT '一级行业编码',
  `industry_l1_name` VARCHAR(255) NULL COMMENT '一级行业名称',
  `industry_l2_code` VARCHAR(255) NULL COMMENT '二级行业编码',
  `industry_l2_name` VARCHAR(255) NULL COMMENT '二级行业名称',
  `industry_l3_code` VARCHAR(255) NULL COMMENT '三级行业编码',
  `industry_l3_name` VARCHAR(255) NULL COMMENT '三级行业名称',
  `industry_l4_code` VARCHAR(255) NULL COMMENT '四级行业编码',
  `industry_l4_name` VARCHAR(255) NULL COMMENT '四级行业名称',
  `is_deleted` DOUBLE NULL COMMENT '使用标记',
  `create_time` DATE NULL COMMENT '入库时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国民行业经济分类';

-- ----------------------------------------------------------
-- 表: dwd_company_reg_cap_change  (注册资本变更)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_reg_cap_change`;
CREATE TABLE `dwd_company_reg_cap_change` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `source_id` VARCHAR(255) NULL COMMENT '唯一键',
  `type` VARCHAR(255) NULL COMMENT '变更类型',
  `date` VARCHAR(255) NULL COMMENT '变更日期',
  `before` DOUBLE NULL COMMENT '变更前注册资本',
  `after` DOUBLE NULL COMMENT '变更后注册资本',
  `unit` VARCHAR(255) NULL COMMENT '单位',
  `is_deleted` DOUBLE NULL COMMENT '是否删除',
  `create_time` DATE NULL COMMENT '创建时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='注册资本变更';

-- ----------------------------------------------------------
-- 表: dwd_company_shareholder  (股东信息)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_shareholder`;
CREATE TABLE `dwd_company_shareholder` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `source_id` VARCHAR(255) NULL COMMENT '唯一键',
  `investor_id` DOUBLE NULL COMMENT '股东id',
  `investor_name` VARCHAR(255) NULL COMMENT '股东名称',
  `investor_type` DOUBLE NULL COMMENT '股东类型',
  `investor_detail_type` VARCHAR(255) NULL COMMENT '股东类型',
  `amount` VARCHAR(255) NULL COMMENT '投资金额',
  `amount_std` DOUBLE NULL COMMENT '投资金额标准化（万元人民币）',
  `share_ratio` DOUBLE NULL COMMENT '持股比例',
  `subscribed` VARCHAR(255) NULL COMMENT '认缴资金,认缴日期,认缴形式',
  `contributed` VARCHAR(255) NULL COMMENT '实缴金额,实缴日期,实缴形式',
  `stock_realcapital` VARCHAR(255) NULL COMMENT '实缴出资额',
  `country` VARCHAR(255) NULL COMMENT '股东国别',
  `include_date` VARCHAR(255) NULL COMMENT '股东进入日期',
  `remove_date` VARCHAR(255) NULL COMMENT '股东退出日期',
  `is_history` DOUBLE NULL COMMENT '是否历史股东',
  `name_source` DOUBLE NULL COMMENT '股东来源',
  `stock_type` VARCHAR(255) NULL COMMENT '股东类型',
  `is_deleted` DOUBLE NULL COMMENT '使用标记',
  `create_time` DATE NULL COMMENT '创建时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='股东信息';

-- ----------------------------------------------------------
-- 表: dwd_company_staff  (任职人员)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_staff`;
CREATE TABLE `dwd_company_staff` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `source_id` VARCHAR(255) NULL COMMENT '唯一键',
  `staff_id` DOUBLE NULL COMMENT '主要人员是机构时，该机构的company_id',
  `staff_name` VARCHAR(255) NULL COMMENT '清洗后主要人员名称',
  `staff_type` VARCHAR(255) NULL COMMENT '职位',
  `person_type` DOUBLE NULL COMMENT 'employee_name类型',
  `start_date` VARCHAR(255) NULL COMMENT '主要人员任职开始日期',
  `end_date` VARCHAR(255) NULL COMMENT '主要人员任职截止日期',
  `is_history` DOUBLE NULL COMMENT '是否历史主要人员',
  `is_deleted` DOUBLE NULL COMMENT '使用标记',
  `create_time` DATE NULL COMMENT '入库时间',
  `update_time` DATE NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='任职人员';

-- ----------------------------------------------------------
-- 表: dwd_company_transition_clean  (注册地址变更)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_transition_clean`;
CREATE TABLE `dwd_company_transition_clean` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `source_id` VARCHAR(255) NULL COMMENT '',
  `name` VARCHAR(255) NULL COMMENT '企业名称',
  `before` VARCHAR(255) NULL COMMENT '清洗后变更前地址',
  `after` VARCHAR(255) NULL COMMENT '清洗后变更后地址',
  `date` VARCHAR(255) NULL COMMENT '变更日期',
  `type` VARCHAR(255) NULL COMMENT '变更类型',
  `is_deleted` DOUBLE NULL COMMENT '是否删除',
  `create_time` DATE NULL COMMENT '创建时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='注册地址变更';

-- ----------------------------------------------------------
-- 表: dwd_company_basic_tags  (基础属性标签)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_basic_tags`;
CREATE TABLE `dwd_company_basic_tags` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `business_type` VARCHAR(255) NULL COMMENT '业务类型',
  `capital_type` VARCHAR(255) NULL COMMENT '企业性质',
  `scale_tag` VARCHAR(255) NULL COMMENT '企业规模标签',
  `is_deleted` DOUBLE NULL COMMENT '使用标记',
  `create_time` DATE NULL COMMENT '创建时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='基础属性标签';

-- ----------------------------------------------------------
-- 表: dwd_company_brief_tags  (企业简介)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_brief_tags`;
CREATE TABLE `dwd_company_brief_tags` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `brief` VARCHAR(255) NULL COMMENT '公司简介摘要',
  `is_deleted` DOUBLE NULL COMMENT '使用标记',
  `create_time` DATE NULL COMMENT '创建时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='企业简介';

-- ----------------------------------------------------------
-- 表: dwd_company_location_tags  (所在行政区)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_location_tags`;
CREATE TABLE `dwd_company_location_tags` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `reg_province` VARCHAR(255) NULL COMMENT '省',
  `reg_city` VARCHAR(255) NULL COMMENT '市',
  `reg_district` VARCHAR(255) NULL COMMENT '区',
  `reg_xy` VARCHAR(255) NULL COMMENT '坐标',
  `is_deleted` DOUBLE NULL COMMENT '是否删除',
  `create_time` DATE NULL COMMENT '入库时间',
  `update_time` DATE NULL COMMENT '数据更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='所在行政区';

-- ----------------------------------------------------------
-- 表: dwd_company_contact_tags  (企业联系方式)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_contact_tags`;
CREATE TABLE `dwd_company_contact_tags` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `contact` VARCHAR(255) NULL COMMENT '联系人信息（联系人姓名，联系方式，类型，信息来源，更新日期，原始链接）',
  `is_deleted` DOUBLE NULL COMMENT '是否删除',
  `create_time` DATE NULL COMMENT '创建时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='企业联系方式';

-- ----------------------------------------------------------
-- 表: dwd_company_recruit  (招聘)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_recruit`;
CREATE TABLE `dwd_company_recruit` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `source_id` VARCHAR(255) NULL COMMENT '招聘事件ID',
  `company_name` VARCHAR(255) NULL COMMENT '公司名称',
  `city` VARCHAR(255) NULL COMMENT '所在城市',
  `district` VARCHAR(255) NULL COMMENT '所在区',
  `title` VARCHAR(255) NULL COMMENT '招聘职称',
  `salary` VARCHAR(255) NULL COMMENT '工资',
  `first_class` VARCHAR(255) NULL COMMENT '一级分类',
  `second_class` VARCHAR(255) NULL COMMENT '二级分类',
  `third_class` VARCHAR(255) NULL COMMENT '三级分类',
  `address` VARCHAR(255) NULL COMMENT '工作地址',
  `start_date` DATE NULL COMMENT '招聘开始日期',
  `end_date` VARCHAR(255) NULL COMMENT '招聘截止日期',
  `education` VARCHAR(255) NULL COMMENT '教育',
  `recruit_number` VARCHAR(255) NULL COMMENT '招聘人数',
  `description` VARCHAR(255) NULL COMMENT '职位描述',
  `experience` VARCHAR(255) NULL COMMENT '经验',
  `type` VARCHAR(255) NULL COMMENT '招聘类别',
  `company_address` VARCHAR(255) NULL COMMENT '公司地址',
  `url_Path` VARCHAR(255) NULL COMMENT '外网链接',
  `source` VARCHAR(255) NULL COMMENT '来源',
  `is_deleted` DOUBLE NULL COMMENT '使用标记',
  `create_time` DATE NULL COMMENT '创建时间',
  `update_time` DATE NULL COMMENT '更改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='招聘';

-- ----------------------------------------------------------
-- 表: dwd_company_industry_tags  (产业标签)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_industry_tags`;
CREATE TABLE `dwd_company_industry_tags` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `industry_tag` VARCHAR(255) NULL COMMENT '产业标签（产业编码，产业名称，置信度，环节[环节编码，环节名称，级别，置信度]）',
  `is_deleted` DOUBLE NULL COMMENT '是否删除',
  `create_time` DATE NULL COMMENT '创建时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='产业标签';

-- ----------------------------------------------------------
-- 表: dwd_company_diy_tags  (特色资质标签)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_diy_tags`;
CREATE TABLE `dwd_company_diy_tags` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `diy_tag` VARCHAR(255) NULL COMMENT '特色资质标签',
  `is_deleted` DOUBLE NULL COMMENT '使用标记',
  `create_time` DATE NULL COMMENT '创建时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='特色资质标签';

-- ----------------------------------------------------------
-- 表: dwd_company_honor_tags  (企业荣誉标签)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_company_honor_tags`;
CREATE TABLE `dwd_company_honor_tags` (
  `id` DOUBLE NOT NULL COMMENT '企业id',
  `association_tag` VARCHAR(255) NULL COMMENT '协会标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `award_tag` VARCHAR(255) NULL COMMENT '荣誉奖项标签（奖项编码，奖项类型，奖项等级，级别，获奖日期，颁发单位，奖项全称，获奖年份）',
  `certification` VARCHAR(255) NULL COMMENT '资质认证（证书名称，证书编号，资质编码，获证年份，级别，状态，有效期起，有效期止，发证日期，发证机构）',
  `city_tag` VARCHAR(255) NULL COMMENT '市级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `district_tag` VARCHAR(255) NULL COMMENT '区县级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `national_tag` VARCHAR(255) NULL COMMENT '国家级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `nonpublic_tags` VARCHAR(255) NULL COMMENT '',
  `park_tag` VARCHAR(255) NULL COMMENT '园区级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `permission` VARCHAR(255) NULL COMMENT '备案许可（许可事项名称，许可证号，许可类型编码，许可年份，管理层级，状态，有效期起，有效期止，发证日期，审批机关，许可生产范围）',
  `province_tag` VARCHAR(255) NULL COMMENT '省级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构）',
  `rank_tag` VARCHAR(255) NULL COMMENT '榜单标签（标签名称，标签编码，年份，级别，具体名次，发布日期，发布机构）',
  `is_deleted` DOUBLE NULL COMMENT '是否删除',
  `create_time` DATE NULL COMMENT '创建时间',
  `update_time` DATE NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='企业荣誉标签';

-- ----------------------------------------------------------
-- 表: dwd_liang_zi_qian_yan_ren_cai  (量子前沿人才)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_liang_zi_qian_yan_ren_cai`;
CREATE TABLE `dwd_liang_zi_qian_yan_ren_cai` (
  `zhu_jian` DOUBLE NOT NULL COMMENT '主键',
  `xing_ming_gong_kai` VARCHAR(255) NULL COMMENT '姓名（公开）',
  `suo_shu_ji_gou` VARCHAR(255) NULL COMMENT '所属机构',
  `yan_jiu_fang_xiang` VARCHAR(255) NULL COMMENT '研究方向',
  `zhu_yao_cheng_guo_gong_kai_lun_wen_xiang_mu` VARCHAR(255) NULL COMMENT '主要成果（公开论文/项目）',
  `fa_bu_shi_jian` DATE NULL COMMENT '发布时间',
  `geng_xin_shi_jian` DATE NULL COMMENT '更新时间',
  PRIMARY KEY (`zhu_jian`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='量子前沿人才';

-- ----------------------------------------------------------
-- 表: dwd_liang_zi_chan_pin_xin_xi  (量子产品信息)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_liang_zi_chan_pin_xin_xi`;
CREATE TABLE `dwd_liang_zi_chan_pin_xin_xi` (
  `zhu_jian` DOUBLE NOT NULL COMMENT '主键',
  `chan_pin_ming_cheng` VARCHAR(255) NULL COMMENT '产品名称',
  `chan_pin_lei_xing` VARCHAR(255) NULL COMMENT '产品类型',
  `qi_ye_ming_cheng` VARCHAR(255) NULL COMMENT '企业名称',
  `tong_yi_xin_yong_dai_ma` VARCHAR(255) NULL COMMENT '统一信用代码',
  `chan_pin_can_shu` VARCHAR(255) NULL COMMENT '产品参数',
  `ying_yong_chang_jing` VARCHAR(255) NULL COMMENT '应用场景',
  `fa_bu_shi_jian` DATE NULL COMMENT '发布时间',
  `geng_xin_shi_jian` DATE NULL COMMENT '更新时间',
  PRIMARY KEY (`zhu_jian`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='量子产品信息';

-- ----------------------------------------------------------
-- 表: dwd_liang_zi_yan_fa_jin_zhan  (量子研发进展)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_liang_zi_yan_fa_jin_zhan`;
CREATE TABLE `dwd_liang_zi_yan_fa_jin_zhan` (
  `zhu_jian` DOUBLE NOT NULL COMMENT '主键',
  `xiang_mu_ming_cheng` VARCHAR(255) NULL COMMENT '项目名称',
  `cheng_dan_dan_wei` VARCHAR(255) NULL COMMENT '承担单位',
  `qi_ye_xin_yong_dai_ma` VARCHAR(255) NULL COMMENT '企业信用代码',
  `yan_fa_fang_xiang` VARCHAR(255) NULL COMMENT '研发方向',
  `ji_chu_yan_jiu_gong_cheng_hua_chan_ye_hua` VARCHAR(255) NULL COMMENT '基础研究/工程化/产业化',
  `jin_zhan_miao_shu` VARCHAR(255) NULL COMMENT '进展描述',
  `guan_jian_tu_po` VARCHAR(255) NULL COMMENT '关键突破',
  `fa_bu_shi_jian` DATE NULL COMMENT '发布时间',
  `geng_xin_shi_jian` DATE NULL COMMENT '更新时间',
  PRIMARY KEY (`zhu_jian`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='量子研发进展';

-- ----------------------------------------------------------
-- 表: dwd_liang_zi_shi_chang_gui_mo  (量子市场规模)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_liang_zi_shi_chang_gui_mo`;
CREATE TABLE `dwd_liang_zi_shi_chang_gui_mo` (
  `zhu_jian` DOUBLE NOT NULL COMMENT '主键',
  `nian_fen` DOUBLE NULL COMMENT '年份',
  `qu_yu` VARCHAR(255) NULL COMMENT '区域',
  `xi_fen_ling_yu` VARCHAR(255) NULL COMMENT '细分领域',
  `shi_chang_gui_mo_yi_yuan` DOUBLE NULL COMMENT '市场规模（亿元）',
  `zeng_zhang_lv` DOUBLE NULL COMMENT '增长率',
  `bao_gao_shi_jian` DATE NULL COMMENT '报告时间',
  `geng_xin_shi_jian` DATE NULL COMMENT '更新时间',
  PRIMARY KEY (`zhu_jian`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='量子市场规模';

-- ----------------------------------------------------------
-- 表: dwd_liang_zi_ji_shu_qu_shi  (量子技术趋势)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_liang_zi_ji_shu_qu_shi`;
CREATE TABLE `dwd_liang_zi_ji_shu_qu_shi` (
  `zhu_jian` DOUBLE NOT NULL COMMENT '主键',
  `ji_shu_ming_cheng` VARCHAR(255) NULL COMMENT '技术名称',
  `ying_jian_ruan_jian_suan_fa_ying_yong` VARCHAR(255) NULL COMMENT '硬件/软件/算法/应用',
  `ji_shu_shuo_ming` VARCHAR(255) NULL COMMENT '技术说明',
  `shi_yan_shi_gong_cheng_hua_shang_yong` VARCHAR(255) NULL COMMENT '实验室/工程化/商用',
  `ying_yong_qian_jing` VARCHAR(255) NULL COMMENT '应用前景',
  `zhu_yao_ji_gou_qi_ye` VARCHAR(255) NULL COMMENT '主要机构/企业',
  `fa_bu_shi_jian` DATE NULL COMMENT '发布时间',
  `geng_xin_shi_jian` DATE NULL COMMENT '更新时间',
  PRIMARY KEY (`zhu_jian`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='量子技术趋势';

-- ----------------------------------------------------------
-- 表: dwd_shang_lian_jie_guo_biao_2  (上链结果表)
-- 来源文件: 行业专题数据汇总表v0601.xlsx | Sheet: 量子专题要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_shang_lian_jie_guo_biao_2`;
CREATE TABLE `dwd_shang_lian_jie_guo_biao_2` (
  `zhu_jian` VARCHAR(255) NOT NULL COMMENT '主键',
  `lei_xing` VARCHAR(255) NULL COMMENT '类型',
  `chan_ye_lian_ID` VARCHAR(255) NULL COMMENT '产业链ID',
  `shi_ti_ID` VARCHAR(255) NULL COMMENT '实体ID',
  `chan_ye_bian_ma` VARCHAR(255) NULL COMMENT '产业编码',
  `chan_ye_ming_cheng` VARCHAR(255) NULL COMMENT '产业名称',
  `huan_jie_bian_ma` VARCHAR(255) NULL COMMENT '环节编码',
  `huan_jie_ming_cheng` VARCHAR(255) NULL COMMENT '环节名称',
  `gua_lian_shi_jian` DATE NULL COMMENT '挂链时间',
  `gua_lian_ren` VARCHAR(255) NULL COMMENT '挂链人',
  PRIMARY KEY (`zhu_jian`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='上链结果表';

-- ----------------------------------------------------------
-- 表: dwd_zh_paper  (中文论文详情信息)
-- 来源文件: 中文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zh_paper`;
CREATE TABLE `dwd_zh_paper` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `doi` VARCHAR(512) NULL COMMENT '论文唯一识别号；论文的唯一标识编码。',
  `en_name` VARCHAR(1024) NULL COMMENT '文献英文题名；文献的英文标题名称。',
  `zh_name` VARCHAR(1024) NULL COMMENT '文献中文题名；文献的中文标题名称。',
  `publication_id` BIGINT NOT NULL COMMENT '关联出版物信息；关联出版物的id，用于获取期刊详情信息',
  `paper_type` VARCHAR(255) NULL COMMENT '文献类型；文献所属出版物的章节名称，栏目等。',
  `publication_type` VARCHAR(255) NULL COMMENT '出版刊物类型；出版物类别，例如期刊，会议等；值域: journal，conference',
  `publication_zh_name` VARCHAR(1024) NULL COMMENT '出版物中文名；期刊的中文名称。',
  `issn` VARCHAR(16) NULL COMMENT 'ISSN；期刊的国际标准连续出版物编号。',
  `volume` VARCHAR(128) NULL COMMENT '文献所在期刊的卷号；文献发表所在期刊的卷号。',
  `issue` VARCHAR(128) NULL COMMENT '文献所在期刊的期号；文献发表所在期刊的期号。',
  `first_page` VARCHAR(255) NULL COMMENT '论文在期刊的首页-页码；论文在期刊中的起始页码。',
  `last_page` VARCHAR(255) NULL COMMENT '论文在期刊的末尾页-页码；论文在期刊中的结束页码。',
  `cover_year_start` VARCHAR(4) NULL COMMENT '文献发表年份；文献正式发表的日期。',
  `cover_date_start` VARCHAR(255) NULL COMMENT '文献发表日期；文献正式发表的日期。',
  `language_classify` TINYINT NULL COMMENT '语言；期刊出版使用的语言类型。；值域: 英文=0 ，中文=1，中英文=2',
  `abstract_available` VARCHAR(1) NULL COMMENT '摘要是否可用；摘要是否可用。；值域: 否=0，是=1',
  `open_access` TINYINT NULL COMMENT '是否OA；标识期刊或论文是否为开放获取。；值域: 否=0，是=1，未知=2',
  `paper_url` TEXT NULL COMMENT '数据来源链接；文献数据的原始来源地址。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_zh_paper_doi` (`doi`(255)),
  KEY `idx_dwd_zh_paper_en_name` (`en_name`(255)),
  KEY `idx_dwd_zh_paper_zh_name` (`zh_name`(255)),
  KEY `idx_dwd_zh_paper_publication_id` (`publication_id`),
  KEY `idx_dwd_zh_paper_publication_zh_name` (`publication_zh_name`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='中文论文详情信息';

-- ----------------------------------------------------------
-- 表: dwd_zh_paper_title  (中文论文标题信息)
-- 来源文件: 中文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zh_paper_title`;
CREATE TABLE `dwd_zh_paper_title` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `title_sequence` INT NOT NULL COMMENT '标题序号；同一文献多个标题的顺序号。',
  `en_name` VARCHAR(1024) NULL COMMENT '文献英文名；文献的英文标题名称。',
  `zh_name` VARCHAR(1024) NULL COMMENT '文献中文名；文献的中文标题名称。',
  `language_code` VARCHAR(12) NULL COMMENT '语言代码；标题的语言代码。',
  `language` VARCHAR(255) NULL COMMENT '语种；标题的语言类型。',
  `original_title` VARCHAR(1) NULL COMMENT '是否原始标题；是否为原始标题。；值域: 否=0，是=1，未知=2',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_zh_paper_title_title_sequence` (`title_sequence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='中文论文标题信息';

-- ----------------------------------------------------------
-- 表: dwd_zh_paper_abstract  (中文论文摘要信息)
-- 来源文件: 中文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zh_paper_abstract`;
CREATE TABLE `dwd_zh_paper_abstract` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `abstract_sequence` INT NOT NULL COMMENT '摘要序号；同一文献多个摘要的顺序号',
  `language` VARCHAR(255) NULL COMMENT '语种；文献或期刊出版使用的语言类型。',
  `original_abstract` VARCHAR(1) NOT NULL COMMENT '是否原始摘要；是否为原始摘要。；值域: 否=0，是=1，未知=2',
  `en_abstract` LONGTEXT NULL COMMENT '摘要 英文；文献内容的英文摘要信息。',
  `zh_abstract` LONGTEXT NULL COMMENT '摘要 中文；文献内容的中文摘要信息。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_zh_paper_abstrac_abstract_sequence` (`abstract_sequence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='中文论文摘要信息';

-- ----------------------------------------------------------
-- 表: dwd_zh_author  (中文文献作者详情信息)
-- 来源文件: 中文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zh_author`;
CREATE TABLE `dwd_zh_author` (
  `paper_id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `author_sequence` INT NOT NULL COMMENT '作者顺序；作者在文献中的顺序。',
  `author_id` VARCHAR(32) NOT NULL COMMENT '文献作者 id；文献作者的唯一主键 id',
  `en_name` VARCHAR(255) NOT NULL COMMENT '文献作者英文名；文献作者的英文名称',
  `zh_name` VARCHAR(255) NULL COMMENT '文献作者中文名',
  `email` JSON NULL COMMENT '文献作者email',
  `correspond` TINYINT NULL COMMENT '是否为通讯作者；值域: 否=0，是=1，未知=Null',
  `institution` TEXT NULL COMMENT '作者单位名称；作者所属机构或单位的名称。',
  `affiliation` JSON NULL COMMENT '文献作者地址',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`paper_id`),
  KEY `idx_dwd_zh_author_author_sequence` (`author_sequence`),
  KEY `idx_dwd_zh_author_author_id` (`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='中文文献作者详情信息';

-- ----------------------------------------------------------
-- 表: dwd_zh_journal  (中文期刊详情信息)
-- 来源文件: 中文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zh_journal`;
CREATE TABLE `dwd_zh_journal` (
  `paper_id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `publication_id` BIGINT NOT NULL COMMENT '期刊id；期刊记录的唯一标识。',
  `publication_type` VARCHAR(255) NULL COMMENT '出版刊物类别；出版物类别，例如期刊，会议等；值域: journal，conference',
  `country` VARCHAR(255) NULL COMMENT '国家；期刊所属或出版所在的国家。',
  `zh_name` VARCHAR(1024) NULL COMMENT '期刊名（中文）；期刊的中文名称。',
  `name_abbr` VARCHAR(255) NULL COMMENT '简称；期刊名称的简称或缩写。',
  `en_name` VARCHAR(1024) NULL COMMENT '期刊名（英文）；期刊的英文名称。',
  `iscn` VARCHAR(16) NULL COMMENT '国内刊号；期刊的国内统一刊号。',
  `issn` VARCHAR(16) NULL COMMENT 'ISSN；期刊的国际标准连续出版物编号。',
  `eissn` VARCHAR(16) NULL COMMENT 'EISSN；期刊电子版的国际标准连续出版物编号。',
  `founding_time` INT NULL COMMENT '创刊时间；期刊首次创办或发行的时间。',
  `jn_official` TEXT NULL COMMENT '期刊官网；期刊官方网站地址。',
  `zh_description` TEXT NULL COMMENT '期刊描述；期刊的中文简介或说明。',
  `format` VARCHAR(255) NULL COMMENT '开本；期刊的版面开本规格。',
  `postal_code` VARCHAR(32) NULL COMMENT '邮发代号；期刊邮政发行使用的代号。',
  `chief_editor` VARCHAR(128) NULL COMMENT '主编；期刊当前或记录中的主编信息。',
  `organizer` VARCHAR(1024) NULL COMMENT '主办单位；负责主办该期刊的单位名称。',
  `publisher_place` VARCHAR(64) NULL COMMENT '出版地；期刊出版发行的地点。',
  `award` TEXT NULL COMMENT '获奖情况；期刊获得的奖项或荣誉信息。',
  `cite_nums` INT NULL COMMENT '被引用量；期刊或文献的累计被引用次数。',
  `annual_publication` INT NULL COMMENT '年文章数；期刊每年发表文章的数量。',
  `review` TINYINT NULL COMMENT '是否为综述性期刊；标识该期刊是否为综述类期刊。；值域: 否=0，是=1，未知=2',
  `impact_factor` DOUBLE NULL COMMENT '影响指数；期刊的影响因子指标。',
  `sub_quartile` TINYINT NULL COMMENT '分区；期刊在相关评价体系中的分区信息。Subject Quartile in Category分区；值域: 1为一区，2为二区，3为三区，4为四区，9表示未知',
  `classify_list` TEXT NULL COMMENT '分类号；文献或期刊对应的学科分类编号。',
  `warning` TINYINT NULL COMMENT '是否预警；标识期刊是否处于预警状态。；值域: 否=0，是=1，未知=Null',
  `is_sci` TINYINT NULL COMMENT '是否SCI；标识期刊是否被 SCI 收录。；值域: 否=0，是=1，未知=Null',
  `publication_cycle` VARCHAR(64) NULL COMMENT '出版周期；期刊的出版频率或发行周期。',
  `paper_nums` INT NULL COMMENT '出版论文量；期刊已发表论文的数量。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`paper_id`),
  KEY `idx_dwd_zh_journal_publication_id` (`publication_id`),
  KEY `idx_dwd_zh_journal_zh_name` (`zh_name`(255)),
  KEY `idx_dwd_zh_journal_name_abbr` (`name_abbr`),
  KEY `idx_dwd_zh_journal_en_name` (`en_name`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='中文期刊详情信息';

-- ----------------------------------------------------------
-- 表: dwd_zh_paper_reference  (中文论文参考文献信息)
-- 来源文件: 中文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zh_paper_reference`;
CREATE TABLE `dwd_zh_paper_reference` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `publication_id` BIGINT NOT NULL COMMENT '关联出版物信息；关联出版物的id，用于获取期刊详情信息',
  `doi` VARCHAR(512) NOT NULL COMMENT '参考文献唯一识别号；论文的唯一标识编码。',
  `zh_name` VARCHAR(1024) NULL COMMENT '参考文献中文名；参考文献的中文标题名称。',
  `publication_zh_name` VARCHAR(1024) NULL COMMENT '参考文献出版物中文名；参考文献出版物的中文名称。',
  `cover_year_start` VARCHAR(4) NULL COMMENT '参考文献发表年份；文献正式发表的年份。',
  `volume` VARCHAR(128) NULL COMMENT '参考文献所在期刊的卷号；参考文献发表所在期刊的卷号。',
  `issue` VARCHAR(128) NULL COMMENT '参考文献所在期刊的期号；参考文献发表所在期刊的期号。',
  `first_page` VARCHAR(255) NULL COMMENT '参考文献在期刊的首页-页码；参考文献在期刊中的起始页码。',
  `last_page` VARCHAR(255) NULL COMMENT '参考文献在期刊的末尾页-页码；参考文献在期刊中的结束页码。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_zh_paper_referen_publication_id` (`publication_id`),
  KEY `idx_dwd_zh_paper_referen_doi` (`doi`(255)),
  KEY `idx_dwd_zh_paper_referen_publication_zh_name` (`publication_zh_name`(255)),
  KEY `idx_dwd_zh_paper_referen_cover_year_start` (`cover_year_start`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='中文论文参考文献信息';

-- ----------------------------------------------------------
-- 表: dwd_zh_paper_citation  (中文论文引用文献信息)
-- 来源文件: 中文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zh_paper_citation`;
CREATE TABLE `dwd_zh_paper_citation` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `publication_id` BIGINT NOT NULL COMMENT '关联出版物信息；关联出版物的id，用于获取期刊详情信息',
  `doi` VARCHAR(512) NOT NULL COMMENT '引用文献唯一识别号；论文的唯一标识编码。',
  `zh_name` VARCHAR(1024) NULL COMMENT '引用文献中文名；引用文献的中文标题名称。',
  `publication_zh_name` VARCHAR(1024) NULL COMMENT '引用文献出版物中文名；参考文献出版物的中文名称。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_zh_paper_citatio_publication_id` (`publication_id`),
  KEY `idx_dwd_zh_paper_citatio_doi` (`doi`(255)),
  KEY `idx_dwd_zh_paper_citatio_publication_zh_name` (`publication_zh_name`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='中文论文引用文献信息';

-- ----------------------------------------------------------
-- 表: dwd_zh_paper_classification  (中文论文分类信息)
-- 来源文件: 中文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zh_paper_classification`;
CREATE TABLE `dwd_zh_paper_classification` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `scope` VARCHAR(20) NULL COMMENT '大类学科分类；期刊所属的大类学科领域。；值域: 材料科学 地球科学 工程技术 管理学 化学 环境科学与生态学 计算机科学 教育学 经济学 历史学 农林科学 社会学 生物学 数学 文学 物理与天体物理 心理学 医学 艺术学 哲学 综合性期刊',
  `scope_zone` VARCHAR(20) NULL COMMENT '小类学科分类；期刊所属的细分学科领域。；值域: 政治学、法学（法律）、国际关系…… JCR小类254',
  `keywords` LONGTEXT NULL COMMENT '论文关键字；描述论文主题内容的关键词。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='中文论文分类信息';

-- ----------------------------------------------------------
-- 表: dwd_zh_paper_related  (中文论文关联文献信息)
-- 来源文件: 中文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zh_paper_related`;
CREATE TABLE `dwd_zh_paper_related` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `relevant` JSON NULL COMMENT '相关文献；与当前文献内容或主题相关的文献信息。',
  `doi` VARCHAR(512) NOT NULL COMMENT '相关文献文献唯一识别号；论文的唯一标识编码。',
  `zh_name` VARCHAR(1024) NULL COMMENT '相关文献中文名；相关文献的中文标题名称。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  `logic_id` VARCHAR(128) NOT NULL COMMENT '逻辑主键；标题信息表逻辑主键',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_zh_paper_related_doi` (`doi`(255)),
  KEY `idx_dwd_zh_paper_related_logic_id` (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='中文论文关联文献信息';

-- ----------------------------------------------------------
-- 表: dwd_en_paper  (英文论文详情信息)
-- 来源文件: 外文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_en_paper`;
CREATE TABLE `dwd_en_paper` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `doi` VARCHAR(512) NOT NULL COMMENT '论文唯一识别号；论文的唯一标识编码。',
  `en_name` VARCHAR(1024) NULL COMMENT '文献英文名；文献的英文标题名称。',
  `zh_name` VARCHAR(1024) NULL COMMENT '文献中文名；文献的中文标题名称。',
  `publication_id` BIGINT NOT NULL COMMENT '关联出版物信息；关联出版物的id，用于获取期刊详情信息',
  `paper_type` VARCHAR(255) NULL COMMENT '文献类型；文献所属出版物的章节名称，栏目等。',
  `publication_type` VARCHAR(255) NULL COMMENT '出版刊物类型；标识出版载体的类型，如期刊、会议或预印本等。；值域: journal，conference',
  `publication_en_name` VARCHAR(1024) NULL COMMENT '出版物英文名；期刊、顶会或预印本平台的英文名称。',
  `issn_print` VARCHAR(16) NULL COMMENT 'ISSN；期刊的国际标准连续出版物编号。纸印出版 issn',
  `issn_online` VARCHAR(16) NULL COMMENT 'EISSN；期刊的国际标准连续出版物编号。在网发行 issn',
  `volume` VARCHAR(128) NULL COMMENT '文献所在期刊的卷号；文献发表所在期刊的卷号。',
  `issue` VARCHAR(128) NULL COMMENT '文献所在期刊的期号；文献发表所在期刊的期号。',
  `first_page` VARCHAR(255) NULL COMMENT '论文在期刊的首页-页码；论文在期刊中的起始页码。',
  `last_page` VARCHAR(255) NULL COMMENT '论文在期刊的末尾页-页码；论文在期刊中的结束页码。',
  `cover_year_start` VARCHAR(4) NULL COMMENT '文献发表年份；文献正式发表的年份。',
  `cover_date_start` DATE NULL COMMENT '文献发表时间；文献正式发表的时间。',
  `language` VARCHAR(255) NULL COMMENT '语种；文献或期刊出版使用的语言类型。',
  `abstract_available` TINYINT NULL COMMENT '摘要是否可用；摘要是否可用。；值域: 否=0，是=1',
  `open_access` TINYINT NULL COMMENT '是否OA；标识期刊或论文是否为开放获取。；值域: 否=0，是=1，未知=2',
  `paper_url` TEXT NULL COMMENT '文献官网链接；文献在官网或来源平台中的访问链接。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_en_paper_doi` (`doi`(255)),
  KEY `idx_dwd_en_paper_publication_id` (`publication_id`),
  KEY `idx_dwd_en_paper_paper_type` (`paper_type`),
  KEY `idx_dwd_en_paper_publication_en_name` (`publication_en_name`(255)),
  KEY `idx_dwd_en_paper_issn_print` (`issn_print`),
  KEY `idx_dwd_en_paper_issn_online` (`issn_online`),
  KEY `idx_dwd_en_paper_cover_year_start` (`cover_year_start`),
  KEY `idx_dwd_en_paper_cover_date_start` (`cover_date_start`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='英文论文详情信息';

-- ----------------------------------------------------------
-- 表: dwd_en_paper_title  (英文论文标题信息)
-- 来源文件: 外文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_en_paper_title`;
CREATE TABLE `dwd_en_paper_title` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `title_sequence` INT NOT NULL COMMENT '标题序号；同一文献多个标题的顺序号。',
  `en_name` VARCHAR(1024) NULL COMMENT '文献英文名；文献的英文标题名称。',
  `zh_name` VARCHAR(1024) NULL COMMENT '文献中文名；文献的中文标题名称。',
  `language_code` VARCHAR(12) NULL COMMENT '语言代码；标题的语言代码。',
  `language` VARCHAR(255) NULL COMMENT '语种；标题的语言类型。',
  `original_title` TINYINT NULL COMMENT '是否原始标题；是否为原始标题。；值域: 否=0，是=1，未知=2',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_en_paper_title_title_sequence` (`title_sequence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='英文论文标题信息';

-- ----------------------------------------------------------
-- 表: dwd_en_paper_abstract  (英文论文摘要信息)
-- 来源文件: 外文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_en_paper_abstract`;
CREATE TABLE `dwd_en_paper_abstract` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `abstract_sequence` INT NOT NULL COMMENT '摘要序号；同一文献多个摘要的顺序号',
  `language` VARCHAR(255) NULL COMMENT '语种；文献或期刊出版使用的语言类型。',
  `original_abstract` TINYINT NOT NULL COMMENT '是否原始摘要；是否为原始摘要。；值域: 否=0，是=1，未知=2',
  `en_abstract` LONGTEXT NULL COMMENT '摘要 英文；文献内容的英文摘要信息。',
  `zh_abstract` LONGTEXT NULL COMMENT '摘要 中文；文献内容的中文摘要信息。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_en_paper_abstrac_abstract_sequence` (`abstract_sequence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='英文论文摘要信息';

-- ----------------------------------------------------------
-- 表: dwd_en_author  (英文文献作者详情信息)
-- 来源文件: 外文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_en_author`;
CREATE TABLE `dwd_en_author` (
  `paper_id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `author_sequence` INT NOT NULL COMMENT '作者顺序；作者在文献中的顺序。',
  `author_id` VARCHAR(32) NOT NULL COMMENT '文献作者 id；文献作者的唯一主键 id',
  `en_name` VARCHAR(255) NOT NULL COMMENT '文献作者英文名；文献作者的英文名称',
  `zh_name` VARCHAR(255) NULL COMMENT '文献作者中文名',
  `email` JSON NULL COMMENT '文献作者email',
  `correspond` TINYINT NULL COMMENT '是否为通讯作者；值域: 否=0，是=1，未知=Null',
  `institution` TEXT NULL COMMENT '作者单位名称；作者所属机构或单位的名称。',
  `affiliation` JSON NULL COMMENT '文献作者地址',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`paper_id`),
  KEY `idx_dwd_en_author_author_sequence` (`author_sequence`),
  KEY `idx_dwd_en_author_author_id` (`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='英文文献作者详情信息';

-- ----------------------------------------------------------
-- 表: dwd_en_journal  (英文期刊详情信息)
-- 来源文件: 外文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_en_journal`;
CREATE TABLE `dwd_en_journal` (
  `publication_id` BIGINT NOT NULL COMMENT '期刊id；期刊、会议或预印本记录的唯一标识。',
  `publication_type` VARCHAR(255) NULL COMMENT '出版刊物类型；标识出版载体的类型，如期刊、会议或预印本等。；值域: journal，conference',
  `country` VARCHAR(255) NULL COMMENT '出版国家/地区；期刊、会议或出版机构所属的国家或地区。',
  `en_name` VARCHAR(1024) NULL COMMENT '期刊名/顶会/预印本名（英文）；期刊、顶会或预印本平台的英文名称。',
  `name_abbr` VARCHAR(255) NULL COMMENT '简称；期刊、会议或预印本名称的简称或缩写。',
  `zh_name` VARCHAR(1024) NULL COMMENT '期刊/顶会/预印本名（中文）；期刊、顶会或预印本平台的中文名称。',
  `issn_print` VARCHAR(16) NULL COMMENT 'ISSN；期刊的国际标准连续出版物编号。纸印出版 issn',
  `issn_online` VARCHAR(16) NULL COMMENT 'EISSN；期刊的国际标准连续出版物编号。在网发行 issn',
  `jn_official` TEXT NULL COMMENT '期刊官网；期刊官方网站地址。',
  `en_description` TEXT NULL COMMENT '期刊描述；期刊、会议或预印本平台的英文简介或说明。',
  `establish_time` INT NULL COMMENT '创刊时间；期刊首次创办或发行的时间。',
  `annual_publication` INT NULL COMMENT '年文量数；期刊或会议每年发表文章的数量。',
  `review` TINYINT NULL COMMENT '是否为综述性期刊；标识该期刊是否为综述类期刊。；值域: 否=0，是=1，未知=2',
  `impact_factor` DOUBLE NULL COMMENT '影响指数；期刊或会议的影响力评价指标。',
  `jcr_zone` VARCHAR(2) NULL COMMENT '分区；期刊在 JCR 等评价体系中的分区信息。；值域: Q1,Q2,Q3,Q4',
  `review_period` VARCHAR(255) NULL COMMENT '平均审稿周期；期刊从投稿到审稿完成的平均周期。',
  `self_rate` DOUBLE NULL COMMENT '自引率；期刊文献中自我引用所占的比例。',
  `top` TINYINT NULL COMMENT '是否顶刊；标识期刊或会议是否为所在领域的顶级刊物。；值域: 否=0，是=1',
  `warning` TINYINT NULL COMMENT '是否预警；标识期刊是否处于预警状态。；值域: 否=0，是=1，未知=Null',
  `is_sci` TINYINT NULL COMMENT '是否SCI；标识期刊是否被 SCI 收录。；值域: 否=0，是=1，未知=Null',
  `publish_period` VARCHAR(64) NULL COMMENT '出版周期；期刊的出版频率或发行周期。',
  `layout_cost` VARCHAR(15) NULL COMMENT '版面费；期刊发表论文所需的版面费用。',
  `paper_nums` INT NULL COMMENT '出版论文量；期刊、会议或平台已发表论文的数量。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  KEY `idx_dwd_en_journal_publication_id` (`publication_id`),
  KEY `idx_dwd_en_journal_en_name` (`en_name`(255)),
  KEY `idx_dwd_en_journal_name_abbr` (`name_abbr`),
  KEY `idx_dwd_en_journal_zh_name` (`zh_name`(255)),
  KEY `idx_dwd_en_journal_issn_print` (`issn_print`),
  KEY `idx_dwd_en_journal_issn_online` (`issn_online`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='英文期刊详情信息';

-- ----------------------------------------------------------
-- 表: dwd_en_paper_reference  (英文论文参考文献信息)
-- 来源文件: 外文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_en_paper_reference`;
CREATE TABLE `dwd_en_paper_reference` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `publication_id` BIGINT NOT NULL COMMENT '关联出版物信息；关联出版物的id，用于获取期刊详情信息',
  `doi` VARCHAR(512) NOT NULL COMMENT '参考文献唯一识别号；论文的唯一标识编码。',
  `en_name` VARCHAR(1024) NULL COMMENT '参考文献英文名；参考文献的英文标题名称。',
  `publication_en_name` VARCHAR(1024) NULL COMMENT '参考文献出版物英文名；参考文献出版物的英文名称。',
  `cover_year_start` VARCHAR(4) NULL COMMENT '文献发表年份；文献正式发表的年份。',
  `volume` VARCHAR(128) NULL COMMENT '参考文献所在期刊的卷号；参考文献发表所在期刊的卷号。',
  `issue` VARCHAR(128) NULL COMMENT '参考文献所在期刊的期号；参考文献发表所在期刊的期号。',
  `first_page` VARCHAR(255) NULL COMMENT '参考文献在期刊的首页-页码；参考文献在期刊中的起始页码。',
  `last_page` VARCHAR(255) NULL COMMENT '参考文献在期刊的末尾页-页码；参考文献在期刊中的结束页码。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_en_paper_referen_publication_id` (`publication_id`),
  KEY `idx_dwd_en_paper_referen_doi` (`doi`(255)),
  KEY `idx_dwd_en_paper_referen_publication_en_name` (`publication_en_name`(255)),
  KEY `idx_dwd_en_paper_referen_cover_year_start` (`cover_year_start`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='英文论文参考文献信息';

-- ----------------------------------------------------------
-- 表: dwd_en_paper_citation  (英文论文引用文献信息)
-- 来源文件: 外文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_en_paper_citation`;
CREATE TABLE `dwd_en_paper_citation` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `publication_id` BIGINT NOT NULL COMMENT '关联出版物信息；关联出版物的id，用于获取期刊详情信息',
  `doi` VARCHAR(512) NOT NULL COMMENT '引用文献唯一识别号；论文的唯一标识编码。',
  `en_name` VARCHAR(1024) NULL COMMENT '引用文献英文名；引用文献的英文标题名称。',
  `publication_en_name` VARCHAR(1024) NULL COMMENT '引用文献出版物英文名；参考文献出版物的英文名称。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_en_paper_citatio_publication_id` (`publication_id`),
  KEY `idx_dwd_en_paper_citatio_doi` (`doi`(255)),
  KEY `idx_dwd_en_paper_citatio_publication_en_name` (`publication_en_name`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='英文论文引用文献信息';

-- ----------------------------------------------------------
-- 表: dwd_en_paper_funding  (英文论文基金信息)
-- 来源文件: 外文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_en_paper_funding`;
CREATE TABLE `dwd_en_paper_funding` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `funds` LONGTEXT NULL COMMENT '基金；支持该论文研究的基金或资助项目信息。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='英文论文基金信息';

-- ----------------------------------------------------------
-- 表: dwd_en_paper_classification  (英文论文分类信息)
-- 来源文件: 外文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_en_paper_classification`;
CREATE TABLE `dwd_en_paper_classification` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `scope` VARCHAR(20) NULL COMMENT '大类学科领域；期刊或会议所属的大类学科领域。；值域: 材料科学 地球科学 工程技术 管理学 化学 环境科学与生态学 计算机科学 教育学 经济学 历史学 农林科学 社会学 生物学 数学 文学 物理与天体物理 心...',
  `sub_scope` VARCHAR(20) NULL COMMENT '小类学科主题；期刊或会议所属的细分学科主题。；值域: 政治学、法学（法律）、国际关系…… JCR小类254',
  `keywords` JSON NULL COMMENT '论文关键词；描述论文主题内容的关键词。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='英文论文分类信息';

-- ----------------------------------------------------------
-- 表: dwd_en_paper_related  (英文论文关联文献信息)
-- 来源文件: 外文论文-数据库设计及数据质量核验方案.xlsx | Sheet: 要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_en_paper_related`;
CREATE TABLE `dwd_en_paper_related` (
  `id` VARCHAR(64) NOT NULL COMMENT '文献id；文献记录的唯一主键标识。',
  `relevant` JSON NULL COMMENT '相关文献；与当前文献内容或主题相关的文献信息。',
  `doi` VARCHAR(512) NOT NULL COMMENT '相关文献文献唯一识别号；论文的唯一标识编码。',
  `en_name` VARCHAR(1024) NULL COMMENT '相关文献英文名；相关文献的英文标题名称。',
  `data_source` VARCHAR(255) NOT NULL COMMENT '数据来源；来源贴源库表名',
  `created_time` DATETIME NOT NULL COMMENT '创建时间；数据在要素库中的创建时间。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  `logic_id` VARCHAR(128) NOT NULL COMMENT '逻辑主键；标题信息表逻辑主键',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_en_paper_related_doi` (`doi`(255)),
  KEY `idx_dwd_en_paper_related_logic_id` (`logic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='英文论文关联文献信息';

-- ----------------------------------------------------------
-- 表: dwd_patent  (专利信息表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 全球专利要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_patent`;
CREATE TABLE `dwd_patent` (
  `id` BIGINT NOT NULL COMMENT '逻辑id；专利信息表的行级逻辑主键，用于唯一标识该分表中的一条记录。',
  `patent_id` VARCHAR(64) NOT NULL COMMENT '专利id；专利记录唯一标识，与 DOCDB 兼容，用于关联各专利要素分表。',
  `publication_number` VARCHAR(64) NOT NULL COMMENT '专利公布号；专利公开或公告时使用的文献编号。',
  `application_kind` VARCHAR(1) NULL COMMENT '专利申请类型；专利申请类型代码，用于区分发明、实用新型、PCT、外观设计等申请类别。；值域: A=专利；U=实用；P=临时；W= PCT；F=设计；T=翻译',
  `country_code` VARCHAR(8) NULL COMMENT '国家代码；专利公开或公告文献对应的国家、地区或组织代码。；值域: country_code数据字典表',
  `country` VARCHAR(20) NULL COMMENT '国家；专利所属或发布的国家名称。；值域: country_code数据字典表',
  `publication_reference` VARCHAR(16) NULL COMMENT '发布文献种类代码；专利公开或公告文献的种类代码。；值域: A=专利；U=实用；P=临时；W= PCT；F=设计；T=翻译',
  `publication_reference_2` VARCHAR(10) NULL COMMENT '发布日期；专利公开或公告发布的具体日期，格式为YYYY-MM-DD。',
  `publication_reference_3` VARCHAR(4) NULL COMMENT '发布年份；专利公开或公告发布日期对应的年份，格式为YYYY。',
  `publication_reference_4` VARCHAR(7) NULL COMMENT '发布年月；专利公开或公告发布日期对应的年月，格式为YYYY-MM。',
  `application_reference` VARCHAR(64) NULL COMMENT '专利申请号；专利申请提交时使用的申请编号。',
  `application_reference_2` VARCHAR(8) NULL COMMENT '申请受理局代码；受理专利申请的国家、地区或组织代码。；值域: country_code数据字典表',
  `application_reference_3` VARCHAR(10) NULL COMMENT '申请日期；专利申请提交的具体日期，格式为YYYY-MM-DD。',
  `application_reference_4` VARCHAR(4) NULL COMMENT '申请年份；专利申请提交日期对应的年份，格式为YYYY。',
  `application_reference_5` VARCHAR(7) NULL COMMENT '申请年月；专利申请提交日期对应的年月，格式为YYYY-MM。',
  `pct_or_regional_filing_data` VARCHAR(64) NULL COMMENT 'PCT申请号；PCT 国际专利申请的申请编号。',
  `pct_or_regional_filing_data_2` VARCHAR(10) NULL COMMENT 'PCT国际申请日期；PCT 国际申请提交的日期。',
  `pct_or_regional_filing_data_3` VARCHAR(10) NULL COMMENT 'PCT进入国家阶段日期；PCT 申请进入国家、地区或组织阶段的日期。',
  `pct_or_regional_publishing_data` VARCHAR(64) NULL COMMENT 'PCT国际公布号；PCT 国际申请对应的公布号。',
  `pct_or_regional_publishing_data_2` VARCHAR(10) NULL COMMENT 'PCT国际公布日期；PCT 国际申请公开发布的日期。',
  `priority_filings` INT NULL COMMENT '优先权序号；同一专利下多条优先权信息的排列序号。',
  `priority_filings_2` INT NULL COMMENT '优先权语言；专利优先权语言',
  `priority_filings_3` VARCHAR(64) NULL COMMENT '优先权申请号；专利优先权申请的申请号。',
  `priority_filings_4` VARCHAR(64) NULL COMMENT '优先权公布号；专利优先权申请的公布号。',
  `priority_filings_5` VARCHAR(8) NULL COMMENT '优先权所属国家/地区/组织代码；专利优先权对应的国家、地区或组织代码。',
  `priority_filings_6` VARCHAR(10) NULL COMMENT '优先权日期；专利优先权申请的具体日期。',
  `priority_filings_7` VARCHAR(4) NULL COMMENT '优先权年份；专利优先权申请日期对应的年份。',
  `priority_filings_8` VARCHAR(16) NULL COMMENT '优先权申请类型代码；专利优先权申请的类型代码。',
  `priority_filings_9` VARCHAR(255) NULL COMMENT '优先权标题；专利优先权申请的具体标题。',
  `applicants` INT NULL COMMENT '原始申请人序号；原始申请人在申请人列表中的排列序号。',
  `applicants_2` VARCHAR(255) NULL COMMENT '原始申请人名称；专利申请文件记载的原始申请人或权利人名称。',
  `assignees` INT NULL COMMENT '当前申请人/专利权人序号；当前申请人或专利权人在权利人列表中的排列序号。',
  `assignees_2` VARCHAR(255) NULL COMMENT '当前申请人/专利权人名称；当前有效的申请人、受让人或专利权人名称。',
  `inventors` INT NULL COMMENT '发明人序号；发明人在发明人列表中的排列序号。',
  `inventors_2` VARCHAR(255) NULL COMMENT '发明人；专利发明人的姓名或信息列表。',
  `first_applicant_name` VARCHAR(255) NULL COMMENT '第一原始申请人；原始申请人列表中的第一位申请人名称。',
  `first_current_assignee_name` VARCHAR(255) NULL COMMENT '第一当前申请人/专利权人；当前申请人或专利权人列表中的第一位主体名称。',
  `first_inventor_name` VARCHAR(255) NULL COMMENT '第一发明人；发明人列表中的第一位发明人名称。',
  `classification_ipcr` VARCHAR(32) NULL COMMENT 'IPCR/IPC主分类号；专利的主要 IPCR/IPC 分类号。；值域: ipc字典表',
  `classification_ipcr_2` VARCHAR(32) NULL COMMENT 'IPCR/IPC附加分类号；专利的附加 IPCR/IPC 分类号。；值域: ipc字典表',
  `classification_ipcr_3` VARCHAR(1) NULL COMMENT 'IPCR/IPC主分类部；主要 IPCR/IPC 分类号对应的部。；值域: ipc字典表',
  `classification_ipcr_4` VARCHAR(2) NULL COMMENT 'IPCR/IPC主分类大类；主要 IPCR/IPC 分类号对应的大类。；值域: ipc字典表',
  `classification_ipcr_5` VARCHAR(1) NULL COMMENT 'IPCR/IPC主分类小类；主要 IPCR/IPC 分类号对应的小类。；值域: ipc字典表',
  `classification_ipcr_6` VARCHAR(4) NULL COMMENT 'IPCR/IPC主分类大组；主要 IPCR/IPC 分类号对应的大组。；值域: ipc字典表',
  `classification_ipcr_7` VARCHAR(8) NULL COMMENT 'IPCR/IPC主分类小组；主要 IPCR/IPC 分类号对应的小组。；值域: ipc字典表',
  `classification_ipcr_8` VARCHAR(1) NULL COMMENT 'IPCR/IPC附加分类部；附加 IPCR/IPC 分类号对应的部。；值域: ipc字典表',
  `classification_ipcr_9` VARCHAR(2) NULL COMMENT 'IPCR/IPC附加分类大类；附加 IPCR/IPC 分类号对应的大类。；值域: ipc字典表',
  `classification_ipcr_10` VARCHAR(1) NULL COMMENT 'IPCR/IPC附加分类小类；附加 IPCR/IPC 分类号对应的小类。；值域: ipc字典表',
  `classification_ipcr_11` VARCHAR(4) NULL COMMENT 'IPCR/IPC附加分类大组；附加 IPCR/IPC 分类号对应的大组。；值域: ipc字典表',
  `classification_ipcr_12` VARCHAR(8) NULL COMMENT 'IPCR/IPC附加分类小组；附加 IPCR/IPC 分类号对应的小组。；值域: ipc字典表',
  `classification_cpc` VARCHAR(32) NULL COMMENT 'CPC主分类号；专利的主要 CPC 分类号。；值域: cpc字典表',
  `classification_cpc_2` VARCHAR(32) NULL COMMENT 'CPC附加分类号；专利的附加 CPC 分类号。；值域: cpc字典表',
  `classification_cpc_3` VARCHAR(1) NULL COMMENT 'CPC主分类部；主要 CPC 分类号对应的部。；值域: cpc字典表',
  `classification_cpc_4` VARCHAR(2) NULL COMMENT 'CPC主分类大类；主要 CPC 分类号对应的大类。；值域: cpc字典表',
  `classification_cpc_5` VARCHAR(1) NULL COMMENT 'CPC主分类小类；主要 CPC 分类号对应的小类。；值域: cpc字典表',
  `classification_cpc_6` VARCHAR(4) NULL COMMENT 'CPC主分类大组；主要 CPC 分类号对应的大组。；值域: cpc字典表',
  `classification_cpc_7` VARCHAR(8) NULL COMMENT 'CPC主分类小组；主要 CPC 分类号对应的小组。；值域: cpc字典表',
  `classification_cpc_8` VARCHAR(1) NULL COMMENT 'CPC附加分类部；附加 CPC 分类号对应的部。；值域: cpc字典表',
  `classification_cpc_9` VARCHAR(2) NULL COMMENT 'CPC附加分类大类；附加 CPC 分类号对应的大类。；值域: cpc字典表',
  `classification_cpc_10` VARCHAR(1) NULL COMMENT 'CPC附加分类小类；附加 CPC 分类号对应的小类。；值域: cpc字典表',
  `classification_cpc_11` VARCHAR(4) NULL COMMENT 'CPC附加分类大组；附加 CPC 分类号对应的大组。；值域: cpc字典表',
  `classification_cpc_12` VARCHAR(8) NULL COMMENT 'CPC附加分类小组；附加 CPC 分类号对应的小组。；值域: cpc字典表',
  `keywords` JSON NULL COMMENT '关键词；描述专利主题内容的关键词。',
  `claims_localized` JSON NULL COMMENT '权利要求；专利权利要求书的文本内容。',
  `description_localized` JSON NULL COMMENT '说明书；专利说明书的正文内容。',
  `figures` JSON NULL COMMENT '专利图；专利附图或图示相关信息。',
  `language` VARCHAR(16) NULL COMMENT '原文语言；专利原始文本使用的语言。',
  `granted_number` VARCHAR(64) NULL COMMENT '授权号；专利获得授权后的授权编号。',
  `spif_application_number` VARCHAR(64) NULL COMMENT 'SPIF标准申请号；SPIF 标准化后的专利申请号。',
  `spif_publication_number` VARCHAR(64) NULL COMMENT 'SPIF标准公布号；SPIF 标准化后的专利公布号。',
  `prior_art_year` VARCHAR(4) NULL COMMENT '现有技术年份；相关现有技术对应的年份。',
  `prior_art_date` VARCHAR(10) NULL COMMENT '现有技术日期；相关现有技术对应的具体日期。',
  `relevants` JSON NULL COMMENT '相关专利；与当前专利主题或技术内容相关的专利信息。',
  `db_source` VARCHAR(64) NOT NULL COMMENT '数据库来源；该条专利要素数据的来源贴源库。',
  `create_time` DATETIME NOT NULL COMMENT '创建时间；该条记录在专利要素库中的创建时间。',
  `update_time` DATETIME NOT NULL COMMENT '更新时间；该条记录在专利要素库中的最近更新时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_patent_patent_id` (`patent_id`),
  KEY `idx_dwd_patent_publication_number` (`publication_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='专利信息表';

-- ----------------------------------------------------------
-- 表: dwd_patent_cited  (专利引用关系表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 全球专利要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_patent_cited`;
CREATE TABLE `dwd_patent_cited` (
  `id` BIGINT NOT NULL COMMENT '逻辑id；专利信息表的行级逻辑主键，用于唯一标识该分表中的一条记录。',
  `patent_id` VARCHAR(64) NOT NULL COMMENT '专利id；专利记录唯一标识，与 DOCDB 兼容，用于关联各专利要素分表。',
  `reference_cited` INT NULL COMMENT '引用专利数量；该专利引用的专利文献数量。',
  `cited_by_nums` INT NULL COMMENT '专利被引数量；当前专利被其他专利引用的数量。',
  `reference_cited_2` VARCHAR(10) NULL COMMENT '被引专利日期；引用当前专利的专利文献日期。',
  `reference_cited_3` VARCHAR(10) NULL COMMENT '引用专利日期；当前专利引用的专利文献日期。',
  `reference_cited_4` INT NULL COMMENT '非专利文献引用数量；当前专利引用的非专利文献数量。',
  `reference_cited_5` VARCHAR(10) NULL COMMENT '非专利文献引用日期；当前专利引用的非专利文献日期。',
  `reference_cited_6` VARCHAR(8) NULL COMMENT '引用专利国家/地区/组织代码；当前专利引用的专利文献所属国家、地区或组织代码。；值域: country_code数据字典表',
  `reference_cited_7` VARCHAR(20) NULL COMMENT '引用专利所属国家/地区；当前专利引用的专利文献所属国家或地区。；值域: country_code数据字典表',
  `reference_cited_8` VARCHAR(16) NULL COMMENT '引用专利文献种类代码；当前专利引用的专利文献种类代码。',
  `cited_by` JSON NULL COMMENT '被引用；引用当前专利的其他专利信息。',
  `patent_citations` JSON NULL COMMENT '专利引用；当前专利引用的其他专利信息。',
  `non_patent_citations` JSON NULL COMMENT '非专利引用；当前专利引用的非专利文献信息。',
  `db_source` VARCHAR(64) NOT NULL COMMENT '数据库来源；该条专利要素数据的来源贴源库。',
  `create_time` DATETIME NOT NULL COMMENT '创建时间；该条记录在专利要素库中的创建时间。',
  `update_time` DATETIME NOT NULL COMMENT '更新时间；该条记录在专利要素库中的最近更新时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_patent_cited_patent_id` (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='专利引用关系表';

-- ----------------------------------------------------------
-- 表: dwd_patent_title  (专利标题信息表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 全球专利要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_patent_title`;
CREATE TABLE `dwd_patent_title` (
  `id` BIGINT NOT NULL COMMENT '逻辑id；专利标题信息表的行级逻辑主键，用于唯一标识该分表中的一条记录。',
  `patent_id` VARCHAR(64) NOT NULL COMMENT '专利id；关联 dwd_patent.patent_id 的专利唯一标识，用于连接主表与各要素分表。',
  `title_localized` VARCHAR(1024) NULL COMMENT '原文标题；专利文献原始语种对应的标题内容。',
  `title_localized_2` VARCHAR(1024) NULL COMMENT '英文标题；专利英文标题文本。',
  `title_zh` VARCHAR(1024) NULL COMMENT '中文翻译标题；专利标题的中文翻译文本。',
  `db_source` VARCHAR(64) NOT NULL COMMENT '数据库来源；该条专利要素数据的来源贴源库。',
  `create_time` DATETIME NOT NULL COMMENT '创建时间；该条记录在专利要素库中的创建时间。',
  `update_time` DATETIME NOT NULL COMMENT '更新时间；该条记录在专利要素库中的最近更新时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_patent_title_patent_id` (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='专利标题信息表';

-- ----------------------------------------------------------
-- 表: dwd_patent_abstract  (专利摘要信息表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 全球专利要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_patent_abstract`;
CREATE TABLE `dwd_patent_abstract` (
  `id` BIGINT NOT NULL COMMENT '逻辑id；专利摘要信息表的行级逻辑主键，用于唯一标识该分表中的一条记录。',
  `patent_id` VARCHAR(64) NOT NULL COMMENT '专利id；关联 dwd_patent.patent_id 的专利唯一标识，用于连接主表与各要素分表。',
  `abstract_localized` TEXT NULL COMMENT '原文摘要；专利文献原始语种对应的摘要内容。',
  `abstract_localized_2` TEXT NULL COMMENT '英文摘要；专利英文摘要文本。',
  `abstract_zh` TEXT NULL COMMENT '中文翻译摘要；专利摘要的中文翻译文本。',
  `db_source` VARCHAR(64) NOT NULL COMMENT '数据库来源；该条专利要素数据的来源贴源库。',
  `create_time` DATETIME NOT NULL COMMENT '创建时间；该条记录在专利要素库中的创建时间。',
  `update_time` DATETIME NOT NULL COMMENT '更新时间；该条记录在专利要素库中的最近更新时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_patent_abstract_patent_id` (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='专利摘要信息表';

-- ----------------------------------------------------------
-- 表: dwd_patent_legal  (法律状态信息表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 全球专利要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_patent_legal`;
CREATE TABLE `dwd_patent_legal` (
  `id` BIGINT NOT NULL COMMENT '逻辑id；法律状态信息表的行级逻辑主键，用于唯一标识该分表中的一条记录。',
  `patent_id` VARCHAR(64) NOT NULL COMMENT '专利id；关联 dwd_patent.patent_id 的专利唯一标识，用于连接主表与各要素分表。',
  `dates_of_public_availability` VARCHAR(10) NULL COMMENT '授权日期；专利授权公告或授权公开的具体日期，格式为YYYY-MM-DD。',
  `dates_of_public_availability_2` VARCHAR(4) NULL COMMENT '授权年份；专利授权公告或授权公开日期对应的年份，格式为YYYY。',
  `dates_of_public_availability_3` VARCHAR(7) NULL COMMENT '授权年月；专利授权公告或授权公开日期对应的年月，格式为YYYY-MM。',
  `status` VARCHAR(64) NULL COMMENT '专利状态；专利当前所处的法律状态。',
  `legal_events` JSON NULL COMMENT '法律事件；专利生命周期中的法律状态变更事件。',
  `patent_legal_prs_data` VARCHAR(10) NULL COMMENT 'PRS法律状态日期；PRS 法律状态事件发生日期。',
  `patent_legal_prs_data_2` VARCHAR(16) NULL COMMENT 'PRS法律状态代码；PRS 法律状态事件代码。',
  `patent_legal_prs_data_3` VARCHAR(255) NULL COMMENT 'PRS法律状态说明；PRS 法律状态事件代码对应的说明。',
  `patent_legal_prs_data_4` VARCHAR(64) NULL COMMENT '法律状态分类说明；法律状态事件所属分类的说明。',
  `anticipated_expiration` VARCHAR(10) NULL COMMENT '预计到期日；专利预计到期的具体日期。',
  `expiration_year` VARCHAR(4) NULL COMMENT '到期年份；专利预计或实际到期日期对应的年份。',
  `db_source` VARCHAR(64) NOT NULL COMMENT '数据库来源；该条专利要素数据的来源贴源库。',
  `create_time` DATETIME NOT NULL COMMENT '创建时间；该条记录在专利要素库中的创建时间。',
  `update_time` DATETIME NOT NULL COMMENT '更新时间；该条记录在专利要素库中的最近更新时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_patent_legal_patent_id` (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='法律状态信息表';

-- ----------------------------------------------------------
-- 表: dwd_patent_transfer  (专利转移信息表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 全球专利要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_patent_transfer`;
CREATE TABLE `dwd_patent_transfer` (
  `id` BIGINT NOT NULL COMMENT '逻辑id；专利转移信息表的行级逻辑主键，用于唯一标识该分表中的一条记录。',
  `patent_id` VARCHAR(64) NOT NULL COMMENT '专利id；关联 dwd_patent.patent_id 的专利唯一标识，用于连接主表与各要素分表。',
  `country` VARCHAR(8) NULL COMMENT '转移国家/地区/组织代码；发生专利权利转移的国家、地区或组织代码。',
  `transfer_effective_date` VARCHAR(10) NULL COMMENT '转移生效日期；专利权利转移的生效日期。',
  `transferor_sequence` INT NULL COMMENT '转移前权利人序号；转移前权利人在权利转移记录中的排列序号。',
  `transferor_name` VARCHAR(255) NULL COMMENT '转移前权利人名称；权利转移发生前的权利人名称。',
  `transferee_sequence` INT NULL COMMENT '转移后权利人序号；转移后权利人在权利转移记录中的排列序号。',
  `transferee_name` VARCHAR(255) NULL COMMENT '转移后权利人名称；权利转移发生后的权利人名称。',
  `db_source` VARCHAR(64) NOT NULL COMMENT '数据库来源；该条专利要素数据的来源数据库或来源系统。',
  `create_time` DATETIME NOT NULL COMMENT '创建时间；该条记录在专利要素库中的创建时间。',
  `update_time` DATETIME NOT NULL COMMENT '更新时间；该条记录在专利要素库中的最近更新时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_patent_transfer_patent_id` (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='专利转移信息表';

-- ----------------------------------------------------------
-- 表: dwd_patent_family  (专利家族信息表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 全球专利要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_patent_family`;
CREATE TABLE `dwd_patent_family` (
  `id` BIGINT NOT NULL COMMENT '逻辑id；专利家族信息表的行级逻辑主键，用于唯一标识该分表中的一条记录。',
  `patent_id` VARCHAR(64) NOT NULL COMMENT '专利id；关联 dwd_patent.patent_id 的专利唯一标识，用于连接主表与各要素分表。',
  `simple_family` VARCHAR(20) NULL COMMENT '专利家族ID；简单同族或专利家族的唯一编号。',
  `simple_family_2` JSON NULL COMMENT '专利家族；简单同族成员的文献号。',
  `simple_family_3` INT NULL COMMENT '家族成员序号；同一专利家族中成员记录的排列序号。',
  `simple_family_4` VARCHAR(8) NULL COMMENT '家族成员所属国家/地区/组织代码；简单同族成员所属国家、地区或组织代码。',
  `simple_family_5` VARCHAR(16) NULL COMMENT '家族成员文献种类代码；简单同族成员公开或公告文献的种类代码。',
  `family_citations` JSON NULL COMMENT '家族内引用；同一专利家族内部的引用信息。',
  `cited_by_family` JSON NULL COMMENT '家族内被引用；同一专利家族内部的被引用信息。',
  `other_versions` JSON NULL COMMENT '其他版本；当前专利的其他公开、公告或授权版本信息。',
  `worldwides` JSON NULL COMMENT '全球同族专利；当前专利在全球范围内的同族专利信息。',
  `db_source` VARCHAR(64) NOT NULL COMMENT '数据库来源；该条专利要素数据的来源贴源库。',
  `create_time` DATETIME NOT NULL COMMENT '创建时间；该条记录在专利要素库中的创建时间。',
  `update_time` DATETIME NOT NULL COMMENT '更新时间；该条记录在专利要素库中的最近更新时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_patent_family_patent_id` (`patent_id`),
  KEY `idx_dwd_patent_family_simple_family` (`simple_family`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='专利家族信息表';

-- ----------------------------------------------------------
-- 表: dwd_zh_project  (国内项目信息表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 国内项目要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zh_project`;
CREATE TABLE `dwd_zh_project` (
  `id` VARCHAR(64) NOT NULL COMMENT '项目索引；项目记录的唯一主键标识。',
  `project_number` VARCHAR(64) NULL COMMENT '项目编号；项目在管理系统中的编号。',
  `title` VARCHAR(512) NULL COMMENT '项目名称；项目的名称或标题。',
  `project_source` VARCHAR(64) NULL COMMENT '项目来源；项目所属的资助来源或立项来源。',
  `funded_institution` VARCHAR(128) NULL COMMENT '项目受资助机构；获得项目资助的机构名称。',
  `project_level` VARCHAR(255) NULL COMMENT '项目级别；项目所属的级别或层次。；值域: 国家级 省级 市级 县级 其他',
  `funded_amount` DECIMAL(20,4) NULL COMMENT '受资助金额；项目获得的资助经费金额，单位为万元。',
  `discipline` VARCHAR(256) NULL COMMENT '学科；项目所属的学科领域。；值域: 学科分类',
  `discipline_code` VARCHAR(256) NULL COMMENT '学科代码；项目所属学科的分类代码。；值域: 学科分类代码',
  `fund_category` VARCHAR(64) NULL COMMENT '基金类别；项目对应的基金或资助类别。；值域: 基金类别',
  `funded_province` VARCHAR(32) NULL COMMENT '项目受资助省；项目受资助机构所在的省份。；值域: 资助省',
  `participating_institution` JSON NULL COMMENT '参与机构；参与项目研究或实施的机构信息。',
  `approval_year` INT NULL COMMENT '立项年度；项目获批立项的年份。',
  `approval_time` DATE NULL COMMENT '立项时间；项目正式获批立项的时间。',
  `research_period` VARCHAR(64) NULL COMMENT '研究期限；项目计划开展研究的时间期限。',
  `project_host` VARCHAR(16) NULL COMMENT '项目主持人；项目的主要负责人或主持人。',
  `participants` JSON NULL COMMENT '参与者；参与项目研究或实施的人员信息。',
  `keywords` JSON NULL COMMENT '关键词；描述项目研究主题的关键词。',
  `abstract` LONGTEXT NULL COMMENT '项目标书摘要；项目申请书或标书中的摘要内容。',
  `final_report_abstract` LONGTEXT NULL COMMENT '项目结题摘要；项目结题报告中的摘要内容。',
  `project_page_url` TEXT NULL COMMENT '项目页面 URL；项目详情页面的访问链接。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_zh_project_project_number` (`project_number`),
  KEY `idx_dwd_zh_project_discipline_code` (`discipline_code`),
  KEY `idx_dwd_zh_project_approval_year` (`approval_year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国内项目信息表';

-- ----------------------------------------------------------
-- 表: dwd_zh_project_output  (国内项目-产出信息)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 国内项目要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zh_project_output`;
CREATE TABLE `dwd_zh_project_output` (
  `id` VARCHAR(64) NOT NULL COMMENT '项目索引；项目记录的唯一主键标识。',
  `total_outputs` INT NULL COMMENT '项目总产出数量；项目产生的成果总数量。',
  `journal_articles_count` INT NULL COMMENT '期刊文章数量；项目产出的期刊论文数量。',
  `conference_papers_count` INT NULL COMMENT '会议论文数量；项目产出的会议论文数量。',
  `degree_papers_count` INT NULL COMMENT '学位论文数量；项目产出的学位论文数量。',
  `patents_count` INT NULL COMMENT '专利数量；项目产出的专利数量。',
  `clinical_trials_count` INT NULL COMMENT '临床试验数量；项目产出的临床试验数量。',
  `books_count` INT NULL COMMENT '图书专著数量；项目产出的图书或专著数量。',
  `products_count` INT NULL COMMENT '产品数量；项目产出的产品数量。',
  `awards_count` INT NULL COMMENT '奖项数量；项目获得的奖项数量。',
  `reports_count` INT NULL COMMENT '报告数量；项目产出的报告数量。',
  `other_outputs_count` INT NULL COMMENT '其他产出数量；项目产生的其他成果数量。',
  `output_article_type` VARCHAR(32) NULL COMMENT '产出类型；项目产出成果的类型。；值域: journal: 期刊文章 conference_paper: 会议论文 degree_paper: 学位论文 patent: 专利 clinical_trial: 临床试验 book: 图书专著 product: 产品 awards: 奖项 report: 报告',
  `output_article_title` VARCHAR(256) NULL COMMENT '产出文章标题；项目产出文章的标题名称。',
  `output_article_authors` JSON NULL COMMENT '产出文章作者；项目产出文章的作者信息。',
  `output_article_journal` VARCHAR(256) NULL COMMENT '产出文章期刊；项目产出文章发表所在的期刊。',
  `output_article_year` INT NULL COMMENT '产出文章发表年份；项目产出文章的发表年份。',
  `output_article_issue` VARCHAR(16) NULL COMMENT '产出文章期数；项目产出文章所在期刊的期号。',
  `output_article_keywords` JSON NULL COMMENT '产出文章关键词；项目产出文章的关键词信息。',
  `output_article_abstract` LONGTEXT NULL COMMENT '产出文章摘要；项目产出文章的摘要内容。',
  `output_article_source_url` TEXT NULL COMMENT '产出文章来源 URL；项目产出文章来源页面的访问链接。',
  `output_patent_title` VARCHAR(256) NULL COMMENT '产出专利标题；项目产出专利的标题名称。',
  `output_patent_inventor` JSON NULL COMMENT '产出专利发明人；项目产出专利的发明人信息。',
  `output_patent_number` VARCHAR(20) NULL COMMENT '产出专利号；项目产出专利的编号。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国内项目-产出信息';

-- ----------------------------------------------------------
-- 表: dwd_rel_project_scholar  (项目-人才关联表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 国内项目要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_rel_project_scholar`;
CREATE TABLE `dwd_rel_project_scholar` (
  `id` BIGINT NOT NULL COMMENT '关联ID；关联表主键ID。',
  `project_source` VARCHAR(32) NOT NULL COMMENT '项目来源；项目所属来源库，用于区分国内项目与国外项目。；值域: zh_project/en_project',
  `project_id` VARCHAR(64) NOT NULL COMMENT '项目ID；项目记录ID。',
  `scholar_id` VARCHAR(32) NOT NULL COMMENT '学者ID；算法绑定后的学者ID。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_rel_project_scho_project_source` (`project_source`),
  KEY `idx_dwd_rel_project_scho_project_id` (`project_id`),
  KEY `idx_dwd_rel_project_scho_scholar_id` (`scholar_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='项目-人才关联表';

-- ----------------------------------------------------------
-- 表: dwd_rel_project_paper  (项目-论文关联表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 国内项目要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_rel_project_paper`;
CREATE TABLE `dwd_rel_project_paper` (
  `id` BIGINT NOT NULL COMMENT '关联ID；关联表主键ID。',
  `project_source` VARCHAR(32) NOT NULL COMMENT '项目来源；项目所属来源库，用于区分国内项目与国外项目。；值域: zh_project/en_project',
  `project_id` VARCHAR(64) NOT NULL COMMENT '项目ID；项目记录ID。',
  `paper_source` VARCHAR(32) NOT NULL COMMENT '论文来源；论文所属来源库，用于区分中文论文与外文论文。；值域: zh_paper/en_paper',
  `paper_id` VARCHAR(64) NOT NULL COMMENT '论文ID；论文记录ID。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_rel_project_pape_project_source` (`project_source`),
  KEY `idx_dwd_rel_project_pape_project_id` (`project_id`),
  KEY `idx_dwd_rel_project_pape_paper_source` (`paper_source`),
  KEY `idx_dwd_rel_project_pape_paper_id` (`paper_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='项目-论文关联表';

-- ----------------------------------------------------------
-- 表: dwd_rel_project_patent  (项目-专利关联表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 国内项目要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_rel_project_patent`;
CREATE TABLE `dwd_rel_project_patent` (
  `id` BIGINT NOT NULL COMMENT '关联ID；关联表主键ID。',
  `project_source` VARCHAR(32) NOT NULL COMMENT '项目来源；项目所属来源库，用于区分国内项目与国外项目。；值域: zh_project/en_project',
  `project_id` VARCHAR(64) NOT NULL COMMENT '项目ID；项目记录ID。',
  `patent_id` VARCHAR(20) NOT NULL COMMENT '专利ID；专利记录ID。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_rel_project_pate_project_source` (`project_source`),
  KEY `idx_dwd_rel_project_pate_project_id` (`project_id`),
  KEY `idx_dwd_rel_project_pate_patent_id` (`patent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='项目-专利关联表';

-- ----------------------------------------------------------
-- 表: dwd_en_project  (国外项目信息表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 国外项目要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_en_project`;
CREATE TABLE `dwd_en_project` (
  `project_id` VARCHAR(64) NOT NULL COMMENT '项目索引；项目记录的唯一主键标识。',
  `project_number` VARCHAR(32) NULL COMMENT '项目编号；项目在管理系统中的编号。',
  `title` VARCHAR(512) NULL COMMENT '项目名称；项目的名称或标题。',
  `project_source` VARCHAR(64) NULL COMMENT '项目来源；项目所属的资助来源或立项来源。',
  `funded_institution` VARCHAR(128) NULL COMMENT '项目受资助机构；获得项目资助的机构名称。',
  `project_level` VARCHAR(255) NULL COMMENT '项目级别；项目所属的级别或层次。；值域: 国家级 州级 市级 县级 其他',
  `funded_amount` DECIMAL(20,4) NULL COMMENT '受资助金额；项目获得的资助经费金额，单位为美元。',
  `discipline` VARCHAR(256) NULL COMMENT '学科；项目所属的学科领域。',
  `discipline_code` VARCHAR(256) NULL COMMENT '学科代码；项目所属学科的分类代码。',
  `fund_category` VARCHAR(64) NULL COMMENT '基金类别；项目对应的基金或资助类别。；值域: BOA/Task Order Continuing grant Contract Contract Interagency Agreement Contract-BOA/Task Order Cooperative Agreement Fellowship Fellowship Award Fixed Amount Award Fixed Price Award GAA Interagency Agreement Intergovernmental Personnel Award Personnel Agreement Standard Grant',
  `funded_province` VARCHAR(32) NULL COMMENT '项目受资助地区；项目受资助机构所在的地区信息。',
  `participating_institution` JSON NULL COMMENT '参与机构；参与项目研究或实施的机构信息。',
  `approval_year` INT NULL COMMENT '立项年度；项目获批立项的年份。',
  `approval_time` DATE NULL COMMENT '立项时间；项目正式获批立项的时间。',
  `research_period` VARCHAR(64) NULL COMMENT '研究期限；项目计划开展研究的时间期限。',
  `project_host` VARCHAR(64) NULL COMMENT '项目主持人；项目的主要负责人或主持人。',
  `participants` JSON NULL COMMENT '参与者；参与项目研究或实施的人员信息。',
  `keywords` JSON NULL COMMENT '关键词；描述项目研究主题的关键词。',
  `abstract` LONGTEXT NULL COMMENT '项目标书摘要；项目申请书或标书中的摘要内容。',
  `final_report_abstract` LONGTEXT NULL COMMENT '项目结题摘要；项目结题报告中的摘要内容。',
  `project_page_url` TEXT NULL COMMENT '项目页面 URL；项目详情页面的访问链接。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  KEY `idx_dwd_en_project_project_id` (`project_id`),
  KEY `idx_dwd_en_project_project_number` (`project_number`),
  KEY `idx_dwd_en_project_discipline_code` (`discipline_code`),
  KEY `idx_dwd_en_project_approval_year` (`approval_year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外项目信息表';

-- ----------------------------------------------------------
-- 表: dwd_en_project_output  (国外项目-产出信息)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 国外项目要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_en_project_output`;
CREATE TABLE `dwd_en_project_output` (
  `id` VARCHAR(64) NOT NULL COMMENT '项目索引；项目记录的唯一主键标识。',
  `total_outputs` INT NULL COMMENT '项目总产出数量；项目产生的成果总数量。',
  `journal_articles_count` INT NULL COMMENT '期刊文章数量；项目产出的期刊论文数量。',
  `conference_papers_count` INT NULL COMMENT '会议论文数量；项目产出的会议论文数量。',
  `degree_papers_count` INT NULL COMMENT '学位论文数量；项目产出的学位论文数量。',
  `patents_count` INT NULL COMMENT '专利数量；项目产出的专利数量。',
  `clinical_trials_count` INT NULL COMMENT '临床试验数量；项目产出的临床试验数量。',
  `books_count` INT NULL COMMENT '图书专著数量；项目产出的图书或专著数量。',
  `products_count` INT NULL COMMENT '产品数量；项目产出的产品数量。',
  `awards_count` INT NULL COMMENT '奖项数量；项目获得的奖项数量。',
  `reports_count` INT NULL COMMENT '报告数量；项目产出的报告数量。',
  `other_outputs_count` INT NULL COMMENT '其他产出数量；项目产生的其他成果数量。',
  `output_article_type` VARCHAR(32) NULL COMMENT '产出类型；项目产出文章所属的类型。；值域: journal: 期刊文章 conference_paper: 会议论文 degree_paper: 学位论文 patent: 专利 clinical_trial: 临床试验 book: 图书专著 product: 产品 awards: 奖项 report: 报告',
  `output_article_title` VARCHAR(256) NULL COMMENT '产出文章标题；项目产出文章的标题名称。',
  `output_article_authors` JSON NULL COMMENT '产出文章作者；项目产出文章的作者信息。',
  `output_article_journal` VARCHAR(256) NULL COMMENT '产出文章期刊；项目产出文章发表所在的期刊。',
  `output_article_year` INT NULL COMMENT '产出文章发表年份；项目产出文章的发表年份。',
  `output_article_issue` VARCHAR(16) NULL COMMENT '产出文章期数；项目产出文章所在期刊的期号。',
  `output_article_keywords` JSON NULL COMMENT '产出文章关键词；项目产出文章的关键词信息。',
  `output_article_abstract` LONGTEXT NULL COMMENT '产出文章摘要；项目产出文章的摘要内容。',
  `output_article_source_url` TEXT NULL COMMENT '产出文章来源 URL；项目产出文章来源页面的访问链接。',
  `output_patent_title` VARCHAR(256) NULL COMMENT '产出专利标题；项目产出专利的标题名称。',
  `output_patent_inventor` JSON NULL COMMENT '产出专利发明人；项目产出专利的发明人信息。',
  `output_patent_number` VARCHAR(20) NULL COMMENT '产出专利号；项目产出专利的编号。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外项目-产出信息';

-- ----------------------------------------------------------
-- 表: dwd_zh_report  (中文科技报告信息表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 中文报告要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_zh_report`;
CREATE TABLE `dwd_zh_report` (
  `report_id` VARCHAR(64) NOT NULL COMMENT '中文报告id；中文报告记录的唯一主键标识。',
  `report_category` VARCHAR(64) NULL COMMENT '报告类别；标识报告所属的类别。',
  `title_cn` VARCHAR(512) NULL COMMENT '中文题名；报告的中文标题名称。',
  `authors` JSON NULL COMMENT '作者；报告作者的姓名或信息列表。',
  `organization` JSON NULL COMMENT '作者单位/完成单位；作者所属单位或报告完成单位名称。',
  `abstract_cn` LONGTEXT NULL COMMENT '中文摘要；报告内容的中文摘要信息。',
  `keywords_cn` JSON NULL COMMENT '中文关键词；描述报告主题内容的中文关键词。',
  `report_type` VARCHAR(32) NULL COMMENT '报告类型；标识报告的具体类型。；值域: 最终报告 进展报告 专题报告 年度报告 中期报告 立项报告 奖励报告 验收报告 其他',
  `page_count` INT NULL COMMENT '全文页数；报告全文的总页数。',
  `preparation_time` DATE NULL COMMENT '编制时间；报告编制完成或形成的时间。',
  `approval_year` INT NULL COMMENT '立项批准年；报告相关项目获批立项的年份。',
  `related_literature` JSON NULL COMMENT '相关文献；与当前报告内容相关的文献信息。',
  `related_scholars` JSON NULL COMMENT '相关学者；与当前报告主题相关的学者信息。',
  `related_institutions` JSON NULL COMMENT '相关机构；与当前报告主题相关的机构信息。',
  `related_projects` JSON NULL COMMENT '相关项目；与当前报告内容相关的项目信息。',
  `source_org` JSON NULL COMMENT '报告来源；报告数据或内容的来源机构。',
  `visibility_scope` VARCHAR(16) NULL COMMENT '可见范围；报告可被访问或查看的范围。；值域: 公开 延期公开(x)年 未知',
  `project_annual_number` INT NULL COMMENT '项目年度编号；项目按年度管理的编号标识。',
  `contact_phone` VARCHAR(64) NULL COMMENT '联系电话；报告相关联系人或单位的联系电话。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  KEY `idx_dwd_zh_report_report_id` (`report_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='中文科技报告信息表';

-- ----------------------------------------------------------
-- 表: dwd_rel_report_scholar  (报告-人才关联表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 中文报告要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_rel_report_scholar`;
CREATE TABLE `dwd_rel_report_scholar` (
  `id` BIGINT NOT NULL COMMENT '关联ID；关联表主键ID。',
  `report_id` VARCHAR(64) NOT NULL COMMENT '报告ID；报告记录ID。',
  `report_source` VARCHAR(32) NOT NULL COMMENT '报告来源；报告所属来源库，用于区分中文报告与外文报告。；值域: zh_report/en_report',
  `scholar_id` VARCHAR(32) NOT NULL COMMENT '学者ID；算法绑定后的学者ID。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_rel_report_schol_report_id` (`report_id`),
  KEY `idx_dwd_rel_report_schol_report_source` (`report_source`),
  KEY `idx_dwd_rel_report_schol_scholar_id` (`scholar_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='报告-人才关联表';

-- ----------------------------------------------------------
-- 表: dwd_rel_report_paper  (报告-论文关联表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 中文报告要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_rel_report_paper`;
CREATE TABLE `dwd_rel_report_paper` (
  `id` BIGINT NOT NULL COMMENT '关联ID；关联表主键ID。',
  `report_source` VARCHAR(32) NOT NULL COMMENT '报告来源；报告所属来源库，用于区分中文报告与外文报告。；值域: zh_report/en_report',
  `report_id` VARCHAR(64) NOT NULL COMMENT '报告ID；报告记录ID。',
  `paper_source` VARCHAR(32) NOT NULL COMMENT '论文来源；论文所属来源库，用于区分中文论文与外文论文。；值域: zh_paper/en_paper',
  `paper_id` VARCHAR(64) NOT NULL COMMENT '论文ID；论文记录ID。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_rel_report_paper_report_source` (`report_source`),
  KEY `idx_dwd_rel_report_paper_report_id` (`report_id`),
  KEY `idx_dwd_rel_report_paper_paper_source` (`paper_source`),
  KEY `idx_dwd_rel_report_paper_paper_id` (`paper_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='报告-论文关联表';

-- ----------------------------------------------------------
-- 表: dwd_rel_report_project  (报告-项目关联表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 中文报告要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_rel_report_project`;
CREATE TABLE `dwd_rel_report_project` (
  `id` BIGINT NOT NULL COMMENT '关联ID；关联表主键ID。',
  `report_source` VARCHAR(32) NOT NULL COMMENT '报告来源；报告所属来源库，用于区分中文报告与外文报告。；值域: zh_report/en_report',
  `report_id` VARCHAR(64) NOT NULL COMMENT '报告ID；报告记录ID。',
  `project_source` VARCHAR(32) NOT NULL COMMENT '项目来源；项目所属来源库，用于区分国内项目与国外项目。；值域: zh_project/en_project',
  `project_id` VARCHAR(64) NOT NULL COMMENT '项目ID；项目记录ID。',
  PRIMARY KEY (`id`),
  KEY `idx_dwd_rel_report_proje_report_source` (`report_source`),
  KEY `idx_dwd_rel_report_proje_report_id` (`report_id`),
  KEY `idx_dwd_rel_report_proje_project_source` (`project_source`),
  KEY `idx_dwd_rel_report_proje_project_id` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='报告-项目关联表';

-- ----------------------------------------------------------
-- 表: dwd_en_report  (外文科技报告信息表)
-- 来源文件: 论文、专利、项目、报告数据汇总表v0601.xlsx | Sheet: 外文报告要素库
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_en_report`;
CREATE TABLE `dwd_en_report` (
  `report_id` VARCHAR(64) NOT NULL COMMENT '外文报告id；外文报告记录的唯一主键标识。',
  `report_number` VARCHAR(64) NULL COMMENT '报告编号；报告在来源系统或机构中的编号。',
  `title_en` VARCHAR(512) NULL COMMENT '英文题名；报告的英文标题名称。',
  `publication_date` INT NULL COMMENT '发布时间；报告正式发布或公开的时间。',
  `authors` JSON NULL COMMENT '作者；报告作者的姓名或信息列表。',
  `corporate_author` JSON NULL COMMENT '团体作者；以机构或团体名义署名的作者信息。',
  `source_agency` VARCHAR(64) NULL COMMENT '来源机构；报告发布或提供的来源机构。',
  `abstract_en` LONGTEXT NULL COMMENT '英文摘要；报告内容的英文摘要信息。',
  `keywords_en` JSON NULL COMMENT '英文关键词；描述报告主题内容的英文关键词。',
  `page_count` INT NULL COMMENT '全文页数；报告全文的总页数。',
  `document_type` VARCHAR(64) NULL COMMENT '文档类型；标识报告文档所属的类型。',
  `contract_number` VARCHAR(32) NULL COMMENT '合同编号；报告相关项目或任务对应的合同编号。',
  `related_literature` JSON NULL COMMENT '相关文献；与当前报告内容相关的文献信息。',
  `related_scholars` JSON NULL COMMENT '相关学者；与当前报告主题相关的学者信息。',
  `updated_time` DATETIME NOT NULL COMMENT '更新时间；该条数据最近一次更新的时间。',
  KEY `idx_dwd_en_report_report_id` (`report_id`),
  KEY `idx_dwd_en_report_report_number` (`report_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='外文科技报告信息表';

SET FOREIGN_KEY_CHECKS = 1;

/* ===== 维度/样例表（基于新增文件） ===== */

-- ----------------------------------------------------------
-- 表: dwd_forg_industry_scope  (海外机构行业范围)
-- 来源文件: 版权人才、企业机构、政策数据汇总表(含行业范围).xlsx | Sheet: 国外机构行业范围
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_forg_industry_scope`;
CREATE TABLE `dwd_forg_industry_scope` (
  `classification_standard` VARCHAR(64) NULL COMMENT '分类标准',
  `classification_standard_desc` VARCHAR(255) NULL COMMENT '分类标准描述',
  `l1_code` VARCHAR(32) NULL COMMENT '一级分类编码',
  `l2_code` VARCHAR(32) NULL COMMENT '二级分类编码',
  `l1_desc` VARCHAR(255) NULL COMMENT '一级分类描述',
  `l2_desc` VARCHAR(255) NULL COMMENT '二级分类描述',
  `is_required` VARCHAR(10) NULL COMMENT '是否需要',
  KEY `idx_dwd_forg_industry_sc_classification_standard` (`classification_standard`),
  KEY `idx_dwd_forg_industry_sc_l1_code` (`l1_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='海外机构行业范围';

-- ----------------------------------------------------------
-- 表: dwd_innovation_carrier  (创新载体(平台/中心))
-- 来源文件: 创新载体(平台中心)_样例数据_202606041527.xlsx | Sheet: Sheet1
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_innovation_carrier`;
CREATE TABLE `dwd_innovation_carrier` (
  `carrier_type` VARCHAR(255) NULL COMMENT '载体/平台/中心类型',
  `carrier_name` VARCHAR(500) NULL COMMENT '载体/平台/中心名称',
  `carrier_level` VARCHAR(50) NULL COMMENT '载体/平台/中心级别',
  `establish_year` VARCHAR(20) NULL COMMENT '组建/认定/立项年份',
  `region` VARCHAR(255) NULL COMMENT '载体/平台/中心所在地区',
  `region_code` VARCHAR(20) NULL COMMENT '所在地区行政区划代码',
  `org_id` VARCHAR(64) NULL COMMENT '机构id；关联单位的机构唯一标识',
  `org_name` VARCHAR(500) NULL COMMENT '关联单位名称',
  `credit_code` VARCHAR(64) NULL COMMENT '统一社会信用代码',
  `announcement_title` VARCHAR(500) NULL COMMENT '公告名称',
  `publish_org` VARCHAR(500) NULL COMMENT '发布单位',
  `publish_date` VARCHAR(20) NULL COMMENT '发布日期',
  `source_url` VARCHAR(1000) NULL COMMENT '来源链接',
  KEY `idx_dwd_innovation_carri_org_id` (`org_id`),
  KEY `idx_dwd_innovation_carri_credit_code` (`credit_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='创新载体(平台/中心)';

-- ----------------------------------------------------------
-- 表: dwd_macro_region_category  (宏观地区分类(重点城市))
-- 来源文件: 重点城市梳理-6.4(2).xlsx | Sheet: 宏观地区分类
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `dwd_macro_region_category`;
CREATE TABLE `dwd_macro_region_category` (
  `seq_no` INT NULL COMMENT '序号',
  `city_name` VARCHAR(255) NULL COMMENT '城市名称',
  `region_tag` VARCHAR(100) NULL COMMENT '地区标签',
  `pan_yrd_city` VARCHAR(255) NULL COMMENT '泛长三角城市(41个)',
  `yrd_core_city` VARCHAR(255) NULL COMMENT '长三角中心区(27个)',
  `prd_city` VARCHAR(255) NULL COMMENT '珠三角城市(9个)',
  `chengyu_city` VARCHAR(255) NULL COMMENT '成渝城市(重庆1市+四川15市,16个)',
  `jingjinji_tech_city` VARCHAR(255) NULL COMMENT '津京冀等重点科创城市(13个)',
  `separate_plan_city` VARCHAR(255) NULL COMMENT '计划单列市(5个)',
  `provincial_capital_city` VARCHAR(255) NULL COMMENT '省会城市(27个)',
  `sub_provincial_capital_city` VARCHAR(255) NULL COMMENT '副省会城市(15个)',
  `bsgs_city_district` VARCHAR(255) NULL COMMENT '北上广深及区县(58个)',
  `g20_country` VARCHAR(255) NULL COMMENT 'G20国家(21个)',
  KEY `idx_dwd_macro_region_cat_city_name` (`city_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='宏观地区分类(重点城市)';

