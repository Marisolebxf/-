# fin-ads-draft · 金融 ADS 建表草稿

> **同步副本，未建表。** 结构真源已入 `storage/FIN/stores/mysql/ads.md`（GDF-FIN-STORAGE-DDL-L01），改列须两边同改。 口径与取数 SQL 见 [12-ADS后加工-金融.md](../12-ADS后加工-金融.md)。  
> 库 `gkxlumenx_ads`。字符集 `utf8mb4_0900_ai_ci`。列风格对齐现有政策 ADS（`id` 自增 + `calc_batch_id` + `ext` + `create_time`），但**不带 `metric_id` 列**：本包不替任何指标定 `metric_id`（12 §1）。  
> 每批「同 `stat_date` 先删后插」放在一个事务里，可重跑。

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_ads`.`ads_fin_industrial_fund_summary` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `stat_date` date NOT NULL COMMENT '统计批次日',
  `reg_region_l1` varchar(64) DEFAULT NULL COMMENT '注册地一级：fin_industrial_fund.reg_region 按 - 切第一段；空则 NULL',
  `fund_type` varchar(255) DEFAULT NULL COMMENT '基金类型',
  `est_year` int DEFAULT NULL COMMENT '成立年（est_date）',
  `fund_cnt` int NOT NULL COMMENT '产业基金数（按 industrial_fund_id 去重）',
  `state_owned_fund_cnt` int NOT NULL COMMENT '国资背景=是 的基金数',
  `reg_capital_wan_sum` decimal(24,4) DEFAULT NULL COMMENT '可解析注册资本合计（万元人民币）；全不可解析为 NULL',
  `reg_capital_parsed_cnt` int NOT NULL COMMENT '注册资本可解析的基金数',
  `reg_capital_parse_rate` decimal(8,4) DEFAULT NULL COMMENT '可解析率 = parsed_cnt / fund_cnt',
  `gp_rel_cnt` int DEFAULT NULL COMMENT '基金-GP 关系条数（非去重 GP 数）',
  `lp_rel_cnt` int DEFAULT NULL COMMENT '基金-LP 关系条数（非去重 LP 数）',
  `lp_sub_capital_sum` decimal(24,2) DEFAULT NULL COMMENT 'LP 认缴金额合计；单位未确认（OPEN-FIN-03）',
  `cum_inv_amount_sum` decimal(24,2) DEFAULT NULL COMMENT '基金级累计投资金额合计；单位未确认（OPEN-FIN-03）；基金级，非项目级',
  `calc_batch_id` varchar(64) DEFAULT NULL COMMENT '计算批次',
  `ext` json DEFAULT NULL COMMENT 'JSON 扩展',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '写入时间',
  PRIMARY KEY (`id`),
  KEY `idx_stat_region` (`stat_date`,`reg_region_l1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='产业基金汇总（地区×类型×成立年）';
```

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_ads`.`ads_fin_bond_issue_summary` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `stat_date` date NOT NULL COMMENT '统计批次日',
  `issue_year` int DEFAULT NULL COMMENT '发行年（issue_date）',
  `bond_class` varchar(32) NOT NULL COMMENT 'SCI_TECH_INNO / HIGH_TECH_INDUSTRY',
  `issuer_type` varchar(255) DEFAULT NULL COMMENT '发行人类型',
  `bond_cnt` int NOT NULL COMMENT '债券数（按 bond_class+bond_code 去重）',
  `issuer_cnt` int NOT NULL COMMENT '发行人数（按 issuer 名称去重）',
  `issue_amount_yi_sum` decimal(24,4) DEFAULT NULL COMMENT '发行总额合计（亿）；源为空的不计入',
  `coupon_rate_avg` decimal(12,4) DEFAULT NULL COMMENT '当期票面利率简单平均（%），非规模加权',
  `calc_batch_id` varchar(64) DEFAULT NULL COMMENT '计算批次',
  `ext` json DEFAULT NULL COMMENT 'JSON 扩展',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '写入时间',
  PRIMARY KEY (`id`),
  KEY `idx_stat_year` (`stat_date`,`issue_year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='科创债/高新债发行汇总（发行年×类别×发行人类型）';
```

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_ads`.`ads_fin_listed_company_snapshot` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `stat_date` date NOT NULL COMMENT '统计批次日',
  `org_id` varchar(255) NOT NULL COMMENT '机构ID（供应方 org_id）',
  `org_name_cn` varchar(500) DEFAULT NULL COMMENT '机构名称；取 fin_corp_basic，缺则取 fin_security.issuer_name',
  `reg_region` varchar(255) DEFAULT NULL COMMENT '注册国家或地区',
  `sec_id` varchar(255) NOT NULL COMMENT '代表证券ID（取数规则见 12 §2.3，OPEN-FIN-09）',
  `sec_code` varchar(255) DEFAULT NULL COMMENT '证券代码',
  `td_mkt` varchar(255) DEFAULT NULL COMMENT '交易市场',
  `valuation_dt` date DEFAULT NULL COMMENT '估值日期（该证券最新一天）',
  `pe_ttm_ed` decimal(20,4) DEFAULT NULL COMMENT '市盈率 PE(TTM)',
  `pb_mrq` decimal(20,4) DEFAULT NULL COMMENT '市净率 PB(MRQ)',
  `ps_ttm_ed` decimal(20,4) DEFAULT NULL COMMENT '市销率 PS(TTM)',
  `pcf_ttm_ed` decimal(20,4) DEFAULT NULL COMMENT '市现率 PCF',
  `tmv_rmb` decimal(20,4) DEFAULT NULL COMMENT '总市值（人民币）',
  `sw_l1_code` varchar(255) DEFAULT NULL COMMENT '申万一级行业代码（industry_level=1 暂定，OPEN-FIN-11）',
  `sw_l1_name` varchar(255) DEFAULT NULL COMMENT '申万一级行业名称',
  `crsc_l1_code` varchar(255) DEFAULT NULL COMMENT '证监会一级行业代码（同上）',
  `crsc_l1_name` varchar(255) DEFAULT NULL COMMENT '证监会一级行业名称',
  `citic_l1_code` varchar(255) DEFAULT NULL COMMENT '中信一级行业代码（同上）',
  `citic_l1_name` varchar(255) DEFAULT NULL COMMENT '中信一级行业名称',
  `calc_batch_id` varchar(64) DEFAULT NULL COMMENT '计算批次',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '写入时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_stat_org` (`stat_date`,`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='A股上市公司金融快照（最新估值+一级行业）；v1 仅 market=CN';
```

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_ads`.`ads_fin_main_biz_latest` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `stat_date` date NOT NULL COMMENT '统计批次日',
  `org_id` varchar(255) NOT NULL COMMENT '机构ID',
  `dim_type` varchar(16) NOT NULL COMMENT 'INDUSTRY / PRODUCT / AREA',
  `dim_name` varchar(255) NOT NULL COMMENT '维度名称',
  `occur_period` varchar(255) NOT NULL COMMENT '该机构该维度的最新报告期（字符串最大值，OPEN-FIN-04）',
  `core_biz_income` decimal(20,4) DEFAULT NULL COMMENT '主营业务收入（万元）',
  `core_biz_income_prop` decimal(20,4) DEFAULT NULL COMMENT '收入占比（%）',
  `core_biz_cost` decimal(20,4) DEFAULT NULL COMMENT '主营业务成本（万元）',
  `gross_margin` decimal(20,4) DEFAULT NULL COMMENT '毛利率（%）',
  `calc_batch_id` varchar(64) DEFAULT NULL COMMENT '计算批次',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '写入时间',
  PRIMARY KEY (`id`),
  KEY `idx_stat_org` (`stat_date`,`org_id`,`dim_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='主营业务构成最新报告期（行业/产品/地区）';
```
