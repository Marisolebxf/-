# FIN · DWD（契约面）

```yaml
---
doc_id: FIN-STORE-MYSQL-DWD
element: FIN
role: store-mysql
status: draft
version: "2026-11-09"
updated: 2026-11-09
engine: mysql
task_id: GDF-FIN-STORAGE-DDL-L01
---
```

> 金融数据域 DWD，共 11 张。库名按 `mysql-ddl-convention.md` §1 写 `demo_gkxlumenx_dwd`；产线 `gkxlumenx_dwd` 只换库名。派单包副本写 `gkxlumenx_dwd`（GDF 只写正式库），自检不比库名。结构真源自 2026-11-09 起在本文件；派单包 `GDF-FIN-WORKPACK-v1/10-DWD-MySQL-DDL/fin-dwd-draft.md` 改为同步副本（OPEN-FIN-01 闭合）。字符集 `utf8mb4_0900_ai_ci`（`../../../mysql-ddl-convention.md` §2）。
> 现网状态：`demo_gkxlumenx_dwd` / `gkxlumenx_dwd` 均未建，建表归 GDF；未建前库核对不通过。
> 禁止：把供应方 `dwd_*` 当项目 DWD 建表；为凑表数灌假数据。

## DDL

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`fin_corp_basic` (
  `src_dwd_id` bigint NOT NULL COMMENT '供应方 dwd_id（追溯）',
  `org_id` varchar(255) NOT NULL COMMENT '机构ID（供应方 org_id，原样；与 enterprise_base.org_id 对照见 09 §4）',
  `org_name_cn` varchar(500) NULL COMMENT '机构名称（中文）',
  `org_name_en` varchar(500) NULL COMMENT '机构名称（英文）',
  `reg_region` varchar(255) NULL COMMENT '注册国家或地区',
  `established_date` date NULL COMMENT '成立日期',
  `business_reg_num` varchar(255) NULL COMMENT '工商登记号',
  `etl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'GDF 写入时间',
  PRIMARY KEY (`src_dwd_id`),
  KEY `idx_org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='上市公司基本资料（沪深港美）';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`fin_security` (
  `src_dwd_id` bigint NOT NULL COMMENT '供应方 dwd_id（追溯）',
  `sec_id` varchar(255) NOT NULL COMMENT '证券ID（供应方 sec_id）',
  `sec_code` varchar(255) NULL COMMENT '证券代码',
  `sec_full_name` varchar(500) NULL COMMENT '证券全称',
  `sec_full_name_en` varchar(500) NULL COMMENT '证券英文全称',
  `sec_type` varchar(255) NULL COMMENT '证券类别',
  `td_mkt` varchar(255) NULL COMMENT '交易市场',
  `td_currency_name` varchar(255) NULL COMMENT '交易货币名称',
  `listed_board_name` varchar(255) NULL COMMENT '上市板名称',
  `listed_status` varchar(255) NULL COMMENT '上市状态',
  `is_listing` smallint NULL COMMENT '是否上市 0否1是',
  `is_delisted` smallint NULL COMMENT '是否摘牌 0否1是',
  `listed_date` date NULL COMMENT '上市日期',
  `stop_listing_date` date NULL COMMENT '终止上市日期',
  `org_id` varchar(255) NULL COMMENT '机构ID',
  `sec_issuer_id` varchar(255) NULL COMMENT '证券发行主体ID（基金/指数/期货用）',
  `issue_org_id` varchar(255) NULL COMMENT '发行机构ID',
  `bond_code` varchar(255) NULL COMMENT '债券关联代码（关联 fin_bond.bond_code）',
  `issuer_name` varchar(255) NULL COMMENT '公司名称',
  `credit_code` varchar(255) NULL COMMENT '统一社会信用代码',
  `etl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'GDF 写入时间',
  PRIMARY KEY (`src_dwd_id`),
  KEY `idx_sec_id` (`sec_id`),
  KEY `idx_sec_code` (`sec_code`),
  KEY `idx_org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='证券基本资料';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`fin_industrial_fund` (
  `src_dwd_id` bigint NOT NULL COMMENT '供应方 dwd_id（追溯）',
  `industrial_fund_id` varchar(255) NOT NULL COMMENT '产业基金ID',
  `fund_short_name` varchar(255) NULL COMMENT '基金简称',
  `fund_name` varchar(255) NULL COMMENT '基金名称',
  `reg_region` varchar(255) NULL COMMENT '注册地区（原样，形如 天津市-西青区）',
  `est_date` date NULL COMMENT '成立日期',
  `fund_type` varchar(255) NULL COMMENT '基金类型',
  `currency_ctgry` varchar(255) NULL COMMENT '投资币种',
  `capital_source` varchar(255) NULL COMMENT '资本来源',
  `fund_year` int NULL COMMENT '基金存续年限',
  `state_owned` varchar(255) NULL COMMENT '国资背景',
  `reg_status` varchar(255) NULL COMMENT '设立状态',
  `proposed_reg_date` date NULL COMMENT '拟设立时间',
  `reg_address` text NULL COMMENT '注册地址',
  `reg_capital_raw` varchar(255) NULL COMMENT '注册资本原文（含单位）',
  `reg_capital_wan` decimal(20,4) NULL COMMENT '注册资本（万元人民币）：仅 元/万元/亿元 可解析；含外币或解析失败为 NULL，不写 0、不换汇',
  `real_capital_raw` varchar(255) NULL COMMENT '实缴资本原文',
  `credit_code` varchar(255) NULL COMMENT '统一社会信用代码',
  `est_status` varchar(255) NULL COMMENT '经营状态',
  `etl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'GDF 写入时间',
  PRIMARY KEY (`src_dwd_id`),
  KEY `idx_industrial_fund_id` (`industrial_fund_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='产业基金基本信息';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`fin_industrial_fund_gp` (
  `src_dwd_id` bigint NOT NULL COMMENT '供应方 dwd_id（追溯）',
  `industrial_fund_id` varchar(255) NOT NULL COMMENT '产业基金ID',
  `gp_org_id` varchar(255) NOT NULL COMMENT 'GP机构ID',
  `gp_org_name` varchar(255) NULL COMMENT 'GP名称全称',
  `brand_institution_name` varchar(255) NULL COMMENT '归属品牌机构名称（简称）',
  `brand_institution_tag` varchar(255) NULL COMMENT '归属品牌机构标签',
  `brand_institution_region` varchar(255) NULL COMMENT '归属品牌机构总部地区',
  `brand_institution_type` varchar(255) NULL COMMENT '归属品牌机构类型',
  `etl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'GDF 写入时间',
  PRIMARY KEY (`src_dwd_id`),
  KEY `idx_industrial_fund_id` (`industrial_fund_id`),
  KEY `idx_gp_org_id` (`gp_org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='产业基金管理机构（GP）';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`fin_industrial_fund_lp` (
  `src_dwd_id` bigint NOT NULL COMMENT '供应方 dwd_id（追溯）',
  `industrial_fund_id` varchar(255) NOT NULL COMMENT '产业基金ID',
  `lp_org_id` varchar(255) NOT NULL COMMENT 'LP机构ID',
  `lp_org_name` varchar(255) NULL COMMENT 'LP机构全称',
  `lp_org_type` text NULL COMMENT 'LP类型',
  `lp_state_owned` varchar(255) NULL COMMENT 'LP是否国资背景',
  `state_lp_sub_ratio` decimal(20,2) NULL COMMENT '国资LP认缴比例（源列 solp_rub_ratio）',
  `lp_region_name` varchar(255) NULL COMMENT 'LP所在地区',
  `lp_first_inv_date` date NULL COMMENT 'LP首次出资时间',
  `sub_capital` decimal(20,2) NULL COMMENT 'LP认缴金额（单位待供应方确认 OPEN-FIN-03，原样）',
  `lp_inv_ratio` decimal(20,2) NULL COMMENT 'LP出资比例',
  `lp_real_capital` decimal(20,2) NULL COMMENT 'LP实缴金额（单位同上）',
  `lp_brand_institution` varchar(255) NULL COMMENT 'LP归属品牌',
  `is_lp_exited` varchar(255) NULL COMMENT 'LP是否退出',
  `etl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'GDF 写入时间',
  PRIMARY KEY (`src_dwd_id`),
  KEY `idx_industrial_fund_id` (`industrial_fund_id`),
  KEY `idx_lp_org_id` (`lp_org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='产业基金LP信息';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`fin_industrial_fund_strategy` (
  `src_dwd_id` bigint NOT NULL COMMENT '供应方 dwd_id（追溯）',
  `industrial_fund_id` varchar(255) NOT NULL COMMENT '产业基金ID',
  `inv_field` text NULL COMMENT '投资领域（多值，源内以换行分隔，原样不拆）',
  `inv_round` varchar(255) NULL COMMENT '投资轮次',
  `inv_industry` varchar(255) NULL COMMENT '投资行业',
  `strategy_desc` text NULL COMMENT '策略描述',
  `etl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'GDF 写入时间',
  PRIMARY KEY (`src_dwd_id`),
  KEY `idx_industrial_fund_id` (`industrial_fund_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='产业基金投资策略';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`fin_industrial_fund_inv_summary` (
  `src_dwd_id` bigint NOT NULL COMMENT '供应方 dwd_id（追溯）',
  `industrial_fund_id` varchar(255) NOT NULL COMMENT '产业基金ID',
  `latest_inv_date` date NULL COMMENT '最新投资时间',
  `inv_event_count` int NULL COMMENT '投资事件数量',
  `total_inv_companies_count` int NULL COMMENT '投资企业总数',
  `cum_inv_amount` decimal(20,2) NULL COMMENT '累计投资金额（单位待确认 OPEN-FIN-03，原样）',
  `listed_companies_count` int NULL COMMENT '投后企业上市数量',
  `etl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'GDF 写入时间',
  PRIMARY KEY (`src_dwd_id`),
  KEY `idx_industrial_fund_id` (`industrial_fund_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='产业基金投资汇总（基金级，非项目级）';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`fin_bond` (
  `src_dwd_id` bigint NOT NULL COMMENT '供应方 dwd_id（追溯）',
  `src_table` varchar(64) NOT NULL COMMENT '来源物理表',
  `bond_class` varchar(32) NOT NULL COMMENT '债券类别：SCI_TECH_INNO / HIGH_TECH_INDUSTRY',
  `bond_code` varchar(255) NOT NULL COMMENT '债券代码',
  `bond_name` varchar(255) NULL COMMENT '债券名称',
  `issue_amount_yi` decimal(20,4) NULL COMMENT '发行总额（亿）；源为 -- 的不写 0',
  `issue_term_years` decimal(20,4) NULL COMMENT '发行期限（年）；仅高新债有',
  `issue_price` decimal(20,4) NULL COMMENT '发行价格；仅高新债有',
  `current_coupon_rate` decimal(20,4) NULL COMMENT '当期票面利率（%）',
  `interest_rate_type` varchar(255) NULL COMMENT '利率类型；仅高新债有',
  `payment_frequency` varchar(255) NULL COMMENT '付息频率',
  `issue_date` date NULL COMMENT '发行日期',
  `maturity_date` date NULL COMMENT '到期日期',
  `latest_bond_rating` varchar(255) NULL COMMENT '最新债项评级',
  `latest_issuer_rating` varchar(255) NULL COMMENT '最新主体信用评级',
  `issue_issuer_rating` varchar(255) NULL COMMENT '发行时主体评级',
  `gics_l1` varchar(255) NULL COMMENT 'GICS一级行业',
  `gics_l2` varchar(255) NULL COMMENT 'GICS二级行业',
  `gics_l3` varchar(255) NULL COMMENT 'GICS三级行业',
  `gics_l4` varchar(255) NULL COMMENT 'GICS四级行业',
  `issuer` varchar(255) NULL COMMENT '发行人',
  `issuer_type` varchar(255) NULL COMMENT '发行人类型',
  `trading_market` varchar(255) NULL COMMENT '交易市场',
  `etl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'GDF 写入时间',
  PRIMARY KEY (`src_table`,`src_dwd_id`),
  KEY `idx_bond_code` (`bond_code`),
  KEY `idx_issuer` (`issuer`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='科创债 / 高新技术产业债';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`fin_industry_class_his` (
  `src_dwd_id` bigint NOT NULL COMMENT '供应方 dwd_id（追溯）',
  `src_table` varchar(64) NOT NULL COMMENT '来源物理表',
  `class_system` varchar(16) NOT NULL COMMENT '分类体系：SW_CN / CRSC_CN / CITIC_CN / SW_HK',
  `org_id` varchar(255) NOT NULL COMMENT '机构ID',
  `org_name` varchar(255) NULL COMMENT '公司名称',
  `credit_code` varchar(255) NULL COMMENT '统一社会信用代码',
  `industry_type` varchar(255) NULL COMMENT '行业类别',
  `industry_level` int NULL COMMENT '行业级别',
  `inclusion_date` date NULL COMMENT '纳入日期',
  `eliminate_date` date NULL COMMENT '剔除日期',
  `industry_code` varchar(255) NULL COMMENT '行业代码',
  `industry_name` varchar(255) NULL COMMENT '行业名称',
  `is_latest` smallint NULL COMMENT '最新标志 1最新；港股申万源无此列→NULL，ADS 以 eliminate_date IS NULL 判最新',
  `etl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'GDF 写入时间',
  PRIMARY KEY (`src_table`,`src_dwd_id`),
  KEY `idx_org_id` (`org_id`),
  KEY `idx_class_system` (`class_system`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='上市公司行业分类全量（申万/证监会/中信/港股申万）';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`fin_main_biz_composition` (
  `src_dwd_id` bigint NOT NULL COMMENT '供应方 dwd_id（追溯）',
  `src_table` varchar(64) NOT NULL COMMENT '来源物理表',
  `dim_type` varchar(16) NOT NULL COMMENT '构成维度：INDUSTRY / PRODUCT / AREA',
  `dim_name` varchar(255) NOT NULL COMMENT '维度名称（行业名/产品名/地区名）',
  `org_id` varchar(255) NOT NULL COMMENT '机构ID',
  `credit_code` varchar(255) NULL COMMENT '统一社会信用代码',
  `stock_code` varchar(255) NULL COMMENT '股票代码',
  `stock_name` varchar(255) NULL COMMENT '代码简称',
  `occur_period` varchar(255) NOT NULL COMMENT '报告期（源样例 202603，原样字符串；OPEN-FIN-04）',
  `core_biz_income` decimal(20,4) NULL COMMENT '主营业务收入（万元）',
  `core_biz_income_prop` decimal(20,4) NULL COMMENT '主营业务收入占比（%）',
  `core_biz_income_gr` decimal(20,4) NULL COMMENT '主营业务收入增长率（%）',
  `core_biz_cost` decimal(20,4) NULL COMMENT '主营业务成本（万元）',
  `core_biz_cost_prop` decimal(20,4) NULL COMMENT '主营业务成本占比（%）',
  `core_biz_cost_gr` decimal(20,4) NULL COMMENT '主营业务成本增长率（%）',
  `core_biz_profit` decimal(20,4) NULL COMMENT '主营业务利润（万元）',
  `core_biz_profit_prop` decimal(20,4) NULL COMMENT '主营业务利润占比（%）',
  `gross_margin` decimal(20,4) NULL COMMENT '毛利率（%）',
  `gross_margin_change` decimal(20,4) NULL COMMENT '毛利率变动',
  `csrc_industry` varchar(255) NULL COMMENT '行业_证监会（新）',
  `shenwan_industry` varchar(255) NULL COMMENT '行业_申万',
  `etl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'GDF 写入时间',
  PRIMARY KEY (`src_table`,`src_dwd_id`),
  KEY `idx_org_id` (`org_id`),
  KEY `idx_dim_type` (`dim_type`),
  KEY `idx_occur_period` (`occur_period`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='沪深上市企业主营业务构成（行业/产品/地区）';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`fin_valuation_daily` (
  `src_dwd_id` bigint NOT NULL COMMENT '供应方 dwd_id（追溯）',
  `src_table` varchar(64) NOT NULL COMMENT '来源物理表',
  `market` varchar(8) NOT NULL COMMENT '市场：CN / HK / US',
  `sec_id` varchar(255) NOT NULL COMMENT '证券ID（关联 fin_security.sec_id）',
  `dt` date NOT NULL COMMENT '日期',
  `pe_ttm_ed` decimal(20,4) NULL COMMENT '市盈率 PE(TTM)',
  `pb_mrq` decimal(20,4) NULL COMMENT '市净率 PB(MRQ)',
  `pcf_ttm_ed` decimal(20,4) NULL COMMENT '市现率 PCF(经营现金流TTM)',
  `ps_ttm_ed` decimal(20,4) NULL COMMENT '市销率 PS(TTM)',
  `tmv_rmb` decimal(20,4) NULL COMMENT '总市值（人民币）',
  `cir_tmv` decimal(20,4) NULL COMMENT '流通市值；仅 A 股有',
  `tmv_hkd` decimal(20,4) NULL COMMENT '总市值（港币）；A 股无',
  `tmv_usd` decimal(20,4) NULL COMMENT '总市值（美元）；A 股无',
  `org_id` varchar(255) NULL COMMENT '机构ID；仅港股源有',
  `org_name` varchar(255) NULL COMMENT '公司名称；仅港股源有',
  `etl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'GDF 写入时间',
  PRIMARY KEY (`src_table`,`src_dwd_id`),
  KEY `idx_sec_id` (`sec_id`),
  KEY `idx_dt` (`dt`),
  KEY `idx_market` (`market`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='股票估值指标日表（A股/港股/美股）';
```
