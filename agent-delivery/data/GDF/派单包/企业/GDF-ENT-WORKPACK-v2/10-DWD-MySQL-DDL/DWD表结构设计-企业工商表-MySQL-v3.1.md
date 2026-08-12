> **【GDF-ENT-WORKPACK-v2.0 冻结快照】** 日期 2026-08-13。投递给 GDF 的建表真源副本。  
> 仓内维护路径：`agent-delivery/data/data-design/企业/` 同名文件。DDL 变更须升工作包版本后重发本快照。  
> 目标库：MySQL 8 · `gkxlumenx_dwd`。禁止 PostgreSQL / `demo_gdf_data`。

---
# DWD 表结构设计—企业工商表—MySQL v3.1

> **现行存储入口（S4）**：[`../storage/ENT/stores/mysql/dwd-entity.md`](../storage/ENT/stores/mysql/dwd-entity.md) · 总览 [`../storage/ENT/README.md`](../storage/ENT/README.md)  
> 本文保留为 **as-built DDL 细表真源**（stores 外链至此；勿把本文件当导航首页）。

> 冻结库：`gkxlumenx_dwd`
> 冻结日期：2026-08-12
> 范围：企业工商/实体明细表（`enterprise_*`，排除指标预聚合与 `__pre_v3`）
> 指标/KPI 预聚合见：`DWD表结构设计-企业指标汇总表-MySQL-v3.1.md`
> 业务字段：保持现网 as-built；与 Excel《机构要素库》差异另评
> 统一主键：`id bigint NOT NULL AUTO_INCREMENT PRIMARY KEY`

## 1. 结构变更记录

| 表名 | 变更 |
|---|---|
| `enterprise_base` | 新增 `id bigint AUTO_INCREMENT PRIMARY KEY` |
| `enterprise_bid` | 新增 `id bigint AUTO_INCREMENT PRIMARY KEY` |
| `enterprise_executive` | 新增 `id bigint AUTO_INCREMENT PRIMARY KEY` |
| `enterprise_extra` | 新增 `id bigint AUTO_INCREMENT PRIMARY KEY` |
| `enterprise_finance_history` | 新增 `id bigint AUTO_INCREMENT PRIMARY KEY` |
| `enterprise_fund_project` | 空表原 `id varchar(64)` → `bigint AUTO_INCREMENT` |
| `enterprise_industry_chain` | 新增 `id bigint AUTO_INCREMENT PRIMARY KEY` |
| `enterprise_news` | 新增 `id bigint AUTO_INCREMENT PRIMARY KEY` |

> 注：`enterprise_risk_summary` 的 id 变更归指标汇总文档（该表属预聚合计数）。

2026-08-12 纠偏：

- 删除 0 行孤立表 `enterprise_base2`。
- `enterprise_industry_chain` 新增可空 `org_id varchar(64)` 与索引
  `idx_enterprise_industry_chain_org_id`。现有 20,000 行因
  `enterprise_base.enterprise_code` 全部为空，无法权威回填，当前 `org_id` 全部保持
  `NULL`；禁止按信用代码自行生成第三方 `org_id`。
- `enterprise_financing` 保持现行
  `finance_round / amount / currency / investors / event_date` 契约。ES ETL、统计与种子任务直接依赖这些字段，算法侧已做别名兼容，本次不改名。

## 2. 工商/实体表明细清单

| # | 表名 | 估算行数 | id bigint AI | 创建时间 | 更新时间 |
|---:|---|---:|---|---|---|
| 1 | `enterprise_base` | 20000 | ✅ | `create_time` | `update_time` |
| 2 | `enterprise_bid` | 20000 | ✅ | ❌ | ❌ |
| 3 | `enterprise_chain_patent` | 0 | ✅ | `create_time` | `update_time` |
| 4 | `enterprise_cooperation` | 22350 | ✅ | `create_time` | `update_time` |
| 5 | `enterprise_executive` | 20000 | ✅ | ❌ | ❌ |
| 6 | `enterprise_extra` | 20000 | ✅ | ❌ | ❌ |
| 7 | `enterprise_finance_history` | 5352 | ✅ | ❌ | ❌ |
| 8 | `enterprise_financing` | 11230 | ✅ | `create_time` | `update_time` |
| 9 | `enterprise_fund_project` | 0 | ✅ | `create_time` | `update_time` |
| 10 | `enterprise_history_name` | 78 | ✅ | `create_time` | `update_time` |
| 11 | `enterprise_industry_chain` | 20000 | ✅ | ❌ | ❌ |
| 12 | `enterprise_industry_product` | 0 | ✅ | `create_time` | `update_time` |
| 13 | `enterprise_innovation_carrier` | 3088 | ✅ | `create_time` | `update_time` |
| 14 | `enterprise_invest` | 9865 | ✅ | `create_time` | `update_time` |
| 15 | `enterprise_news` | 19983 | ✅ | ❌ | ❌ |
| 16 | `enterprise_parent_subsidiary` | 21 | ✅ | `create_time` | `update_time` |
| 17 | `enterprise_patent_detail` | 460 | ✅ | `create_time` | `update_time` |
| 18 | `enterprise_patent_history` | 50099 | ✅ | `create_time` | `update_time` |
| 19 | `enterprise_supply_chain` | 32972 | ✅ | `create_time` | `update_time` |
| 20 | `enterprise_tag` | 21658 | ✅ | `create_time` | `update_time` |

## 3. 现网 as-built DDL

### 3.1 `enterprise_base`

```sql
CREATE TABLE `enterprise_base` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT '业务主键',
  `enterprise_code` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `enterprise_name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '企业名称',
  `legal_representative` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '法定代表人',
  `registration_date` date DEFAULT NULL COMMENT '成立日期',
  `business_status` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '经营状态',
  `enterprise_type` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业类型',
  `industry_category` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '行业分类',
  `industry_code` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '行业代码',
  `province` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '省份',
  `city` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '地市',
  `district` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '区县',
  `registered_capital` decimal(20,4) DEFAULT NULL COMMENT '注册资本(万元)',
  `is_listed` tinyint(1) DEFAULT NULL COMMENT '是否上市',
  `org_size` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业规模',
  `data_source` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='企业主数据输出';
```

### 3.2 `enterprise_bid`

```sql
CREATE TABLE `enterprise_bid` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `enterprise_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构名称',
  `announcement_title` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公告标题',
  `announcement_date` timestamp NULL DEFAULT NULL COMMENT '公告日期',
  `project_name` text COLLATE utf8mb4_general_ci COMMENT '项目名称',
  `project_no` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '项目编号',
  `winning_amount` double DEFAULT NULL COMMENT '中标金额',
  `role` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '角色(中标/采购)',
  `tender_org_id` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '采购方机构ID',
  `tender_org_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '采购方机构名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='企业招投标输出';
```

### 3.3 `enterprise_chain_patent`

```sql
CREATE TABLE `enterprise_chain_patent` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `org_id` varchar(64) DEFAULT NULL COMMENT '机构id（ETL通过current_assign映射enterprise_base）',
  `chain_code` varchar(255) DEFAULT NULL COMMENT '产业链编码（如 IC0007）',
  `chain_name` varchar(255) DEFAULT NULL COMMENT '产业链名称（如 集成电路）',
  `node_id` varchar(255) DEFAULT NULL COMMENT '产业链环节编码（如 IC0007004）',
  `node_name` varchar(255) DEFAULT NULL COMMENT '产业链环节名称（如 半导体材料）',
  `patent_no` varchar(255) DEFAULT NULL COMMENT '申请号（apno）',
  `patent_pub_no` varchar(255) DEFAULT NULL COMMENT '公开号（pn）',
  `patent_name` varchar(500) DEFAULT NULL COMMENT '专利名称',
  `filing_date` date DEFAULT NULL COMMENT '申请日（apdt）',
  `publish_date` date DEFAULT NULL COMMENT '公开日（pbdt）',
  `assignee` text COMMENT '当前专利权人（current_assign）',
  `inventors` text COMMENT '发明人',
  `data_source` varchar(255) DEFAULT NULL COMMENT '数据来源',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间（ETL）',
  PRIMARY KEY (`id`),
  KEY `idx_org_id` (`org_id`),
  KEY `idx_chain_code` (`chain_code`),
  KEY `idx_node_id` (`node_id`),
  KEY `idx_patent_no` (`patent_no`),
  KEY `idx_filing_date` (`filing_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='产业链维度专利明细（来源：ODS dwd_org_industry_chain_pat_dtl）';
```

### 3.4 `enterprise_cooperation`

```sql
CREATE TABLE `enterprise_cooperation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) NOT NULL,
  `partner_type` varchar(50) NOT NULL,
  `partner_org_id` varchar(64) DEFAULT NULL,
  `partner_name` varchar(255) DEFAULT NULL,
  `cooperation_type` varchar(50) DEFAULT NULL,
  `project_count` int DEFAULT NULL,
  `patent_count` int DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_cooperation` (`org_id`,`partner_org_id`,`cooperation_type`),
  KEY `idx_coop_org` (`org_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24550 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='entan 图谱输入：企业合作关系';
```

### 3.5 `enterprise_executive`

```sql
CREATE TABLE `enterprise_executive` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `executive_name` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '高管姓名',
  `position` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '职位名称',
  `data_source` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='企业高管信息输出';
```

### 3.6 `enterprise_extra`

```sql
CREATE TABLE `enterprise_extra` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '业务主键',
  `enterprise_name_en` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业英文名称',
  `paid_in_capital` decimal(20,4) DEFAULT NULL COMMENT '实缴资本',
  `business_scope` text COLLATE utf8mb4_general_ci COMMENT '经营范围',
  `registered_address` varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '注册地址',
  `headquarters_address` varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '总部地址',
  `lng` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '经度',
  `lat` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '纬度',
  `listed_market` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '上市板块',
  `listed_code` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '股票代码',
  `listed_date` date DEFAULT NULL COMMENT '上市日期',
  `contact_phone` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '联系电话',
  `contact_email` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '联系邮箱',
  `main_activities` text COLLATE utf8mb4_general_ci COMMENT '主要经营活动',
  `main_prod` text COLLATE utf8mb4_general_ci COMMENT '主要产品',
  `description` text COLLATE utf8mb4_general_ci COMMENT '企业描述',
  `stock_noun` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '股票简称',
  `listed_status` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '上市状态描述',
  `capital_currency_code` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '币种代码',
  `registration_org` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '登记机关',
  `postal_code` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '邮政编码',
  `start_date` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '营业期限自',
  `end_date` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '营业期限至',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='企业扩展表输出';
```

### 3.7 `enterprise_finance_history`

```sql
CREATE TABLE `enterprise_finance_history` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `data_year` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据年度',
  `revenue` decimal(20,4) DEFAULT NULL COMMENT '营业收入(万元)',
  `main_business_revenue` decimal(20,4) DEFAULT NULL COMMENT '主营业务收入(万元)',
  `total_profit` decimal(20,4) DEFAULT NULL COMMENT '利润总额(万元)',
  `total_fixed_assets` decimal(20,4) DEFAULT NULL COMMENT '固定资产总额(万元)',
  `data_source` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源标识',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5353 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='企业财务历史输出';
```

### 3.8 `enterprise_financing`

```sql
CREATE TABLE `enterprise_financing` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) NOT NULL,
  `finance_round` varchar(30) DEFAULT NULL,
  `amount` decimal(20,2) DEFAULT NULL,
  `currency` varchar(20) DEFAULT NULL,
  `investors` varchar(500) DEFAULT NULL,
  `event_date` date DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_financing` (`org_id`,`event_date`,`finance_round`),
  KEY `idx_fin_org` (`org_id`,`event_date`)
) ENGINE=InnoDB AUTO_INCREMENT=13913 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='企业融资事件（canonical §4.12）';
```

### 3.9 `enterprise_fund_project`

```sql
CREATE TABLE `enterprise_fund_project` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) DEFAULT NULL COMMENT '机构id（ETL通过ODS org_id映射）',
  `project_name` varchar(512) DEFAULT NULL COMMENT '项目名称',
  `fund_amount` decimal(20,2) DEFAULT NULL COMMENT '资助金额（元）',
  `domain_code` varchar(64) DEFAULT NULL COMMENT '领域代码（D-IC/D-BIO/D-AI/D-NE/D-QI/D-AS）',
  `approve_date` datetime DEFAULT NULL COMMENT '批准日期',
  `data_source` varchar(100) DEFAULT NULL COMMENT '数据来源',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间（ETL）',
  PRIMARY KEY (`id`),
  KEY `idx_org_id` (`org_id`),
  KEY `idx_domain` (`domain_code`),
  KEY `idx_approve_date` (`approve_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='企业领域科研项目（来源：ODS fund_project）';
```

### 3.10 `enterprise_history_name`

```sql
CREATE TABLE `enterprise_history_name` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) NOT NULL,
  `history_name` varchar(255) NOT NULL,
  `start_date` varchar(50) DEFAULT NULL,
  `end_date` varchar(50) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_history_name` (`org_id`,`history_name`,`start_date`),
  KEY `idx_hist_org` (`org_id`),
  KEY `idx_hist_name` (`history_name`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='企业曾用名（canonical §4.16）';
```

### 3.11 `enterprise_industry_chain`

```sql
CREATE TABLE `enterprise_industry_chain` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) DEFAULT NULL COMMENT '机构id；待权威信用代码映射后回填',
  `enterprise_code` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '统一社会信用代码',
  `chain_code` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '产业链代码',
  `chain_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '产业链名称',
  `node_id` varchar(3000) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '节点代码',
  `node_name` varchar(2000) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '节点名称',
  `node_stage` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '节点环节/层级',
  `is_chain_leader` tinyint(1) DEFAULT NULL COMMENT '是否链主',
  `chain_score` decimal(10,2) DEFAULT NULL COMMENT '产业链评分',
  PRIMARY KEY (`id`),
  KEY `idx_enterprise_industry_chain_org_id` (`org_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='企业产业链关联输出';
```

### 3.12 `enterprise_industry_product`

```sql
CREATE TABLE `enterprise_industry_product` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `org_id` varchar(64) DEFAULT NULL COMMENT '机构id（ETL通过credit_code映射enterprise_base）',
  `enterprise_code` varchar(64) DEFAULT NULL COMMENT '统一社会信用代码',
  `enterprise_name` varchar(500) DEFAULT NULL COMMENT '企业名称',
  `chain_code` varchar(255) DEFAULT NULL COMMENT '产业链编码（JSON展开后取第一个）',
  `chain_name` varchar(255) DEFAULT NULL COMMENT '产业链名称',
  `node_id` varchar(255) DEFAULT NULL COMMENT '产业链环节编码',
  `node_name` varchar(255) DEFAULT NULL COMMENT '产业链环节名称',
  `product_name` text COMMENT '产品名称（JSON展开后）',
  `data_source` varchar(100) DEFAULT NULL COMMENT '数据来源',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间（ETL）',
  PRIMARY KEY (`id`),
  KEY `idx_org_id` (`org_id`),
  KEY `idx_enterprise_code` (`enterprise_code`),
  KEY `idx_chain_code` (`chain_code`),
  KEY `idx_node_id` (`node_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='企业产业链产品标签（来源：ODS dwd_org_industry_product_tags）';
```

### 3.13 `enterprise_innovation_carrier`

```sql
CREATE TABLE `enterprise_innovation_carrier` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) NOT NULL,
  `carrier_name` varchar(255) NOT NULL,
  `carrier_type` varchar(50) DEFAULT NULL,
  `carrier_level` varchar(30) DEFAULT NULL,
  `publish_date` varchar(50) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_carrier` (`org_id`,`carrier_name`,`carrier_type`)
) ENGINE=InnoDB AUTO_INCREMENT=3717 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='企业创新载体（canonical §4.13）';
```

### 3.15 `enterprise_invest`

```sql
CREATE TABLE `enterprise_invest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) NOT NULL,
  `inv_org_id` varchar(64) NOT NULL,
  `inv_name` varchar(255) DEFAULT NULL,
  `inv_external_id` varchar(64) DEFAULT NULL,
  `investment_amount` decimal(20,2) DEFAULT NULL,
  `investment_ratio` decimal(10,4) DEFAULT NULL,
  `data_source` varchar(100) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_invest_org_inv_org` (`org_id`,`inv_org_id`),
  KEY `idx_invest_inv_org` (`inv_org_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10852 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 3.16 `enterprise_news`

```sql
CREATE TABLE `enterprise_news` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构id',
  `enterprise_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业名称',
  `news_title` text COLLATE utf8mb4_general_ci COMMENT '新闻标题',
  `news_date` date DEFAULT NULL COMMENT '新闻日期',
  `news_content` text COLLATE utf8mb4_general_ci COMMENT '新闻内容',
  `original_url` varchar(1024) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '原文链接',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19984 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='企业资讯输出';
```

### 3.17 `enterprise_parent_subsidiary`

```sql
CREATE TABLE `enterprise_parent_subsidiary` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) NOT NULL,
  `parent_org_id` varchar(64) DEFAULT NULL,
  `parent_enterprise_name` varchar(255) DEFAULT NULL,
  `ownership_ratio` decimal(10,4) DEFAULT NULL,
  `subsidiary_count` int DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_parent_subsidiary` (`org_id`,`parent_org_id`),
  KEY `idx_ps_org` (`org_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='entan 图谱输入：母子公司关系';
```

### 3.18 `enterprise_patent_detail`

```sql
CREATE TABLE `enterprise_patent_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) NOT NULL,
  `patent_id` varchar(64) NOT NULL,
  `publication_number` varchar(64) DEFAULT NULL,
  `title_zh` varchar(1024) DEFAULT NULL,
  `title_en` varchar(1024) DEFAULT NULL,
  `abstract_zh` text,
  `patent_type` varchar(20) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `filing_date` date DEFAULT NULL,
  `filing_year` int DEFAULT NULL,
  `publication_date` date DEFAULT NULL,
  `publication_year` int DEFAULT NULL,
  `grant_date` date DEFAULT NULL,
  `grant_year` int DEFAULT NULL,
  `grant_number` varchar(64) DEFAULT NULL,
  `ipc_main` varchar(64) DEFAULT NULL,
  `cpc_main` varchar(64) DEFAULT NULL,
  `inventor` varchar(500) DEFAULT NULL,
  `applicant_name` varchar(255) DEFAULT NULL,
  `assignee_name` varchar(255) DEFAULT NULL,
  `legal_status` varchar(50) DEFAULT NULL,
  `citation_count` bigint DEFAULT NULL,
  `cited_by_count` bigint DEFAULT NULL,
  `detail_json` text,
  `data_source` varchar(100) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_patent_org_patent` (`org_id`,`patent_id`),
  KEY `idx_patent_id` (`patent_id`),
  KEY `idx_patent_org_filing` (`org_id`,`filing_date`)
) ENGINE=InnoDB AUTO_INCREMENT=461 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 3.19 `enterprise_patent_history`

```sql
CREATE TABLE `enterprise_patent_history` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) NOT NULL,
  `data_year` int NOT NULL,
  `patent_apply_count` bigint DEFAULT NULL,
  `patent_grant_count` bigint DEFAULT NULL,
  `patent_valid_count` bigint DEFAULT NULL,
  `patent_invention_count` bigint DEFAULT NULL,
  `patent_citation_count` bigint DEFAULT NULL,
  `latest_patent_date` date DEFAULT NULL,
  `latest_grant_date` date DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_patent_history_org_year` (`org_id`,`data_year`)
) ENGINE=InnoDB AUTO_INCREMENT=66306 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 3.20 `enterprise_supply_chain`

```sql
CREATE TABLE `enterprise_supply_chain` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) NOT NULL,
  `related_org_id` varchar(64) NOT NULL,
  `relation_type` varchar(50) NOT NULL,
  `relation_strength` decimal(10,3) DEFAULT NULL,
  `is_core_supplier` smallint DEFAULT NULL,
  `risk_level` varchar(20) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_supply_chain` (`org_id`,`related_org_id`,`relation_type`),
  KEY `idx_supply_org` (`org_id`)
) ENGINE=InnoDB AUTO_INCREMENT=36205 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='entan 图谱输入：供应链关系';
```

### 3.21 `enterprise_tag`

```sql
CREATE TABLE `enterprise_tag` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) NOT NULL,
  `tag_code` varchar(50) NOT NULL,
  `tag_value` varchar(100) DEFAULT NULL,
  `tag_name` varchar(100) DEFAULT NULL,
  `tag_category` varchar(50) DEFAULT NULL,
  `tag_score` decimal(10,2) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ent_tag` (`org_id`,`tag_code`,`tag_value`),
  KEY `idx_tag_code` (`tag_code`)
) ENGINE=InnoDB AUTO_INCREMENT=50268 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='企业-标签关联（canonical §4.4）';
```

## 4. 不在本文档的表

| 类别 | 去向 |
|---|---|
| 从旧版文档摘出的指标/预聚合汇总（区域/产业/重点企业/深圳/风险汇总） | `DWD表结构设计-企业指标汇总表-MySQL-v3.1.md` |
| v3.0 后新增汇总表（`enterprise_distribution`、`sz_city_benchmark`） | `DWD表结构设计-企业模块-MySQL-v3.0.md` |
| 风险明细 `risk_*`、专利/投资等 v3.0 已冻结表 | `DWD表结构设计-企业模块-MySQL-v3.0.md` |
| `__pre_v3` 备份表 | 不纳入正式契约 |

## 5. 验收

- 复核时间：2026-08-12。
- 工商/实体正式表：20 张；全部 `id bigint AI PK`。
- `enterprise_base2` 已删除；`enterprise_industry_chain.org_id` 为已知数据映射阻塞，保持可空且不得伪造。
- 融资字段保持现行 ETL 契约；与 Excel 对齐仍另开任务。

## 6. 国外机构表（`enterprise_forg_*`）

> 新增日期：2026-08-12
> 数据库：`gkxlumenx_dwd`
> 设计原则：字段命名和业务含义对齐国内 `enterprise_*` 表；org_id 复用源表，不重新生成
> 源表：`dwd_forg_base_info` / `dwd_forg_product_info` / `dwd_forg_executive_info` / `dwd_forg_shareholder_info` / `dwd_foreign_org_annual_financial_info` / `dwd_agg_subsidiary_info`

### 6.0 国外机构表清单

| # | 表名 | 对应国内表 | 源表 | 说明 |
|---:|---|---|---|---|
| 1 | `enterprise_forg_base` | `enterprise_base` + `enterprise_extra`(部分) | `dwd_forg_base_info` | 国外机构主数据 |
| 2 | `enterprise_forg_extra` | `enterprise_extra`(部分) | `dwd_forg_product_info` | 经营/产品/描述 |
| 3 | `enterprise_forg_executive` | `enterprise_executive` | `dwd_forg_executive_info` | 高管信息 |
| 4 | `enterprise_forg_finance_history` | `enterprise_finance_history` | `dwd_foreign_org_annual_financial_info` | 财务历史 |
| 5 | `enterprise_forg_invest` | `enterprise_invest` | `dwd_forg_shareholder_info` | 股东/投资 |
| 6 | `enterprise_forg_parent_subsidiary` | `enterprise_parent_subsidiary` | `dwd_agg_subsidiary_info` | 母子公司 |

### 6.1 `enterprise_forg_base`

```sql
CREATE TABLE `enterprise_forg_base` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT '机构ID',
  `enterprise_code` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当地官方注册码',
  `enterprise_name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '机构名称（英文）',
  `name_alias` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构本地名称',
  `country_code` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '国家代码',
  `country_name` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '国家名称',
  `state` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '所在州/省',
  `city` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '所在城市',
  `address` varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '公司地址',
  `postal_code` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '邮政编码',
  `phone` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '联系电话',
  `email` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '电子邮箱',
  `enterprise_type` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '企业类型',
  `registration_date` date DEFAULT NULL COMMENT '成立日期',
  `incorporation_year` int DEFAULT NULL COMMENT '成立年份',
  `registration_org` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '注册机构',
  `is_listed` tinyint(1) DEFAULT NULL COMMENT '是否上市',
  `stock_code` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '上市股票代码',
  `registered_capital` decimal(20,4) DEFAULT NULL COMMENT '注册资本',
  `capital_currency_code` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '注册资本货币代码',
  `industry_code` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '行业代码',
  `industry_type` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '行业分类标准（如NAICS）',
  `data_source` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_forg_org_id` (`org_id`),
  KEY `idx_forg_country` (`country_code`),
  KEY `idx_forg_name` (`enterprise_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外机构主数据';
```

### 6.2 `enterprise_forg_extra`

```sql
CREATE TABLE `enterprise_forg_extra` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT '机构ID',
  `main_activities` text COLLATE utf8mb4_general_ci COMMENT '主要经营活动',
  `main_prod` text COLLATE utf8mb4_general_ci COMMENT '主要产品',
  `description` text COLLATE utf8mb4_general_ci COMMENT '企业描述',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_forg_extra_org` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外机构扩展信息';
```

### 6.3 `enterprise_forg_executive`

```sql
CREATE TABLE `enterprise_forg_executive` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT '机构ID',
  `executive_name` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '高管姓名',
  `position` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '职位名称',
  `data_source` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_forg_exec_org` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外机构高管信息';
```

### 6.4 `enterprise_forg_finance_history`

```sql
CREATE TABLE `enterprise_forg_finance_history` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT '机构ID',
  `data_year` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据年度',
  `occur_period` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '报表数据期',
  `total_assets` decimal(20,4) DEFAULT NULL COMMENT '资产总额',
  `fixed_assets` decimal(20,4) DEFAULT NULL COMMENT '固定资产净额',
  `total_liabilities` decimal(20,4) DEFAULT NULL COMMENT '负债总额',
  `operating_revenue` decimal(20,4) DEFAULT NULL COMMENT '营业收入',
  `main_business_revenue` decimal(20,4) DEFAULT NULL COMMENT '主营业务收入',
  `total_profit` decimal(20,4) DEFAULT NULL COMMENT '利润总额',
  `pure_profit` decimal(20,4) DEFAULT NULL COMMENT '净利润',
  `total_tax_paid` decimal(20,4) DEFAULT NULL COMMENT '纳税总额',
  `employees_number` int DEFAULT NULL COMMENT '从业人数',
  `research_development_amount` decimal(20,4) DEFAULT NULL COMMENT '研发投入金额',
  `data_source` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_forg_fin_org` (`org_id`, `data_year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外机构财务历史';
```

> **字段对比国内 `enterprise_finance_history`**：国内表只有 8 个字段（revenue/main_business_revenue/total_profit/total_fixed_assets + 基础字段），国外表保留了更多财务字段（total_assets/total_liabilities/pure_profit/employees_number 等），因为国外源表 `dwd_foreign_org_annual_financial_info` 有 21 个字段，字段更丰富。

### 6.5 `enterprise_forg_invest`

```sql
CREATE TABLE `enterprise_forg_invest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT '机构ID',
  `inv_org_id` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '股东/被投机构ID',
  `inv_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '股东/被投机构名称',
  `inv_country_code` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '股东所在国家代码',
  `ownership_percentage` decimal(10,4) DEFAULT NULL COMMENT '持股比例(%)',
  `data_source` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数据来源',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_forg_invest` (`org_id`, `inv_org_id`),
  KEY `idx_forg_invest_inv` (`inv_org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外机构股东/投资信息';
```

> **字段对比国内 `enterprise_invest`**：国外表多了 `inv_country_code`（股东所在国家代码），因为国外股东可能来自不同国家；少了 `investment_amount`（投资金额）和 `investment_ratio`（股权占比），改为 `ownership_percentage`（持股比例），因为源表 `dwd_forg_shareholder_info` 只有持股比例字段。

### 6.6 `enterprise_forg_parent_subsidiary`

```sql
CREATE TABLE `enterprise_forg_parent_subsidiary` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT '母公司机构ID',
  `sub_org_id` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '子公司机构ID',
  `sub_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '子公司名称',
  `sub_country_code` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '子公司所在国家代码',
  `sub_country_name` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '子公司所在国家名称',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_forg_ps` (`org_id`, `sub_org_id`),
  KEY `idx_forg_ps_org` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='国外机构母子公司关系';
```

> **字段对比国内 `enterprise_parent_subsidiary`**：国外表多了 `sub_country_code` / `sub_country_name`（子公司所在国家），因为国外子公司可能在不同国家；少了 `ownership_ratio`（持股比例）和 `subsidiary_count`（子公司数量），因为源表 `dwd_agg_subsidiary_info` 没有这些字段。
