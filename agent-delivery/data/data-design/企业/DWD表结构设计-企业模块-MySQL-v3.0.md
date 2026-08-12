# 企业模块 DWD 表结构设计（MySQL v3.0 正式候选）

> **现行存储入口（S4）**：风险 [`../storage/ENT/stores/mysql/dwd-risk.md`](../storage/ENT/stores/mysql/dwd-risk.md) · 总览 [`../storage/ENT/README.md`](../storage/ENT/README.md)  
> 本文保留为 **风险 + 已复核非风险 as-built DDL 真源**（stores 外链至此）。

> 版本：v3.0-rc1（2026-08-03 首次迁移；2026-08-12 修复后现网复核见 §11.1）
> 日期：2026-08-03  
> 数据库：MySQL 8.0，库名 `gkxlumenx_dwd`  
> 范围：本轮人工逐表复核确认的 36 张表（12 张非风险表、18 张风险主表、6 张风险 party 表）  
> API 约束：Java 已接入的 API 路径、请求参数和响应结构完全不变；Python Repository 负责 DWD 字段到稳定 API 字段的兼容。

## 1. 权威决策来源与适用边界

1. 第一权威来源：`agent-delivery/agent-handoffs/FIX-TOPIC-SEARCH-PY-DWD-SCHEMA-REVIEW.md`。本文以其中每张表的“最终字段”、唯一键、事件日期以及第 7 节最新 Human 复核结论为准；第 7 节 Human 结论覆盖前文旧备注和冲突描述。
2. 字段语义历史参考（已归档）：`agent-delivery/_archive/2026-08/data-design-企业-legacy/DWD表结构设计-企业模块.md`（原 PG 大稿）。PostgreSQL schema、未复核表和冲突字段不进入本文正式范围；落库以本文 + 工商/指标 v3.1 为准。
3. 稳定接口字段参考：`demo-svc-topic-py/gkx_search_service/views/enterprise_risk.py`。该文件用于确认现有 API 字段名，不反向改变 Human 已确认的 DWD 最终字段。
4. 本文原始用途为定义候选目标结构；2026-08-03 经 human:徐滕强授权后执行首次迁移，2026-08-12 再次修复后 Python/Java API 契约仍未改变，as-built 见 §11 与 §11.1。

## 2. 命名、类型与约束规范

- 库名固定为 `gkxlumenx_dwd`；所有表名不带 `dwd_` 前缀。
- 主键 `id` 统一为 `BIGINT NOT NULL AUTO_INCREMENT`。
- 业务 ID、编码和状态文本使用 `VARCHAR`；长文本使用 `TEXT`。
- 金额使用 `DECIMAL(20,2)`；比例使用 `DECIMAL(10,4)`。
- 计数使用 `BIGINT`；年份、月份和排序序号使用 `INT`。
- 业务日期使用 `DATE`；`create_time`、`update_time` 使用 `DATETIME`。
- 历史和布尔状态使用 `TINYINT`，约定 `0=否/当前`、`1=是/历史`。
- 时间字段默认值统一为 `CURRENT_TIMESTAMP`，`update_time` 自动更新时间。
- 风险域企业关联键 `org_id` 固定使用 `utf8mb4_general_ci`，与
  `enterprise_base.org_id` 一致；该列级规则优先于风险表默认
  `utf8mb4_0900_ai_ci`，避免跨表 JOIN 出现 MySQL 1267。
- 复合唯一键严格采用复核后的完整维度；party 表按“案件 ID + 企业 + 当事人角色”去重。
- 直接关联企业的风险表在主表保存 `is_history`；经 party 关联企业的拆分案件在 party 表保存 `is_history`。
- 只有最终字段明确包含 `case_id` 的表使用 `case_id`；稳定 API 原生 ID 名称由 Python 映射。
- 所有 DDL 使用 `InnoDB`、`utf8mb4`、`utf8mb4_0900_ai_ci`。

## 3. 36 张表总览

| 类别 | 数量 | 表名 |
|---|---:|---|
| 非风险表 | 12 | `enterprise_patent_detail`, `enterprise_patent_history`, `enterprise_invest`, `enterprise_region_summary`, `enterprise_industry_distribution`, `enterprise_growth_trend`, `enterprise_industry_summary`, `enterprise_stat_summary`, `enterprise_type_scale_stats`, `shenzhen_enterprise_summary`, `enterprise_distribution`, `sz_city_benchmark` |
| 风险主表 | 18 | `risk_judicial_case`, `risk_dishonest`, `risk_executed`, `risk_limit_high`, `risk_lawsuit`, `risk_court_filed`, `risk_court_notice`, `risk_court_announcement`, `risk_equity_freeze`, `risk_equity_pledge`, `risk_zhongben`, `risk_chattel_mortgage`, `risk_judicial_sale`, `risk_bankruptcy`, `risk_abnormal`, `risk_punishment`, `risk_illegal`, `risk_tax_punish` |
| 风险 party 表 | 6 | `risk_lawsuit_party`, `risk_court_filed_party`, `risk_court_notice_party`, `risk_court_announcement_party`, `risk_judicial_sale_party`, `risk_bankruptcy_party` |

## 4. 非风险表字段字典与完整 DDL

### 4.1 `enterprise_patent_detail`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| org_id | VARCHAR(64) | 否 | 企业机构 ID |
| patent_id | VARCHAR(64) | 否 | 专利业务 ID |
| publication_number | VARCHAR(64) | 是 | 公布号 |
| title_zh / title_en | VARCHAR(1024) | 是 | 中文/英文标题 |
| abstract_zh | TEXT | 是 | 中文摘要 |
| patent_type / country | VARCHAR(20) | 是 | 专利类型/国家 |
| filing_date / publication_date / grant_date | DATE | 是 | 申请/公开/授权日期 |
| filing_year / publication_year / grant_year | INT | 是 | 申请/公开/授权年份 |
| grant_number | VARCHAR(64) | 是 | 授权号 |
| ipc_main / cpc_main | VARCHAR(64) | 是 | IPC/CPC 主分类号 |
| inventor | VARCHAR(500) | 是 | 发明人 |
| applicant_name / assignee_name | VARCHAR(255) | 是 | 申请人/当前权利人 |
| legal_status | VARCHAR(50) | 是 | 法律状态 |
| citation_count / cited_by_count | BIGINT | 是 | 引用数/被引数 |
| detail_json | TEXT | 是 | 原始详情 JSON |
| data_source | VARCHAR(100) | 是 | 数据来源 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`enterprise_patent_detail` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) NOT NULL,
  `patent_id` VARCHAR(64) NOT NULL,
  `publication_number` VARCHAR(64) NULL,
  `title_zh` VARCHAR(1024) NULL,
  `title_en` VARCHAR(1024) NULL,
  `abstract_zh` TEXT NULL,
  `patent_type` VARCHAR(20) NULL,
  `country` VARCHAR(20) NULL,
  `filing_date` DATE NULL,
  `filing_year` INT NULL,
  `publication_date` DATE NULL,
  `publication_year` INT NULL,
  `grant_date` DATE NULL,
  `grant_year` INT NULL,
  `grant_number` VARCHAR(64) NULL,
  `ipc_main` VARCHAR(64) NULL,
  `cpc_main` VARCHAR(64) NULL,
  `inventor` VARCHAR(500) NULL,
  `applicant_name` VARCHAR(255) NULL,
  `assignee_name` VARCHAR(255) NULL,
  `legal_status` VARCHAR(50) NULL,
  `citation_count` BIGINT NULL,
  `cited_by_count` BIGINT NULL,
  `detail_json` TEXT NULL,
  `data_source` VARCHAR(100) NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_patent_org_patent` (`org_id`, `patent_id`),
  KEY `idx_patent_id` (`patent_id`),
  KEY `idx_patent_org_filing` (`org_id`, `filing_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 4.2 `enterprise_patent_history`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| org_id | VARCHAR(64) | 否 | 企业机构 ID |
| data_year | INT | 否 | 数据年份 |
| patent_apply_count / patent_grant_count / patent_valid_count | BIGINT | 是 | 申请/授权/有效专利数 |
| patent_invention_count / patent_citation_count | BIGINT | 是 | 发明专利数/被引次数 |
| latest_patent_date / latest_grant_date | DATE | 是 | 最新申请/授权日期 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`enterprise_patent_history` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) NOT NULL,
  `data_year` INT NOT NULL,
  `patent_apply_count` BIGINT NULL,
  `patent_grant_count` BIGINT NULL,
  `patent_valid_count` BIGINT NULL,
  `patent_invention_count` BIGINT NULL,
  `patent_citation_count` BIGINT NULL,
  `latest_patent_date` DATE NULL,
  `latest_grant_date` DATE NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_patent_history_org_year` (`org_id`, `data_year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 4.3 `enterprise_invest`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| org_id | VARCHAR(64) | 否 | 投资方机构 ID |
| inv_org_id | VARCHAR(64) | 否 | 被投企业机构 ID |
| inv_name | VARCHAR(255) | 是 | 被投企业名称 |
| inv_external_id | VARCHAR(64) | 是 | 被投企业统一信用代码 |
| investment_amount | DECIMAL(20,2) | 是 | 投资金额 |
| investment_ratio | DECIMAL(10,4) | 是 | 投资比例 |
| data_source | VARCHAR(100) | 是 | 数据来源 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`enterprise_invest` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) NOT NULL,
  `inv_org_id` VARCHAR(64) NOT NULL,
  `inv_name` VARCHAR(255) NULL,
  `inv_external_id` VARCHAR(64) NULL,
  `investment_amount` DECIMAL(20,2) NULL,
  `investment_ratio` DECIMAL(10,4) NULL,
  `data_source` VARCHAR(100) NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_invest_org_inv_org` (`org_id`, `inv_org_id`),
  KEY `idx_invest_inv_org` (`inv_org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 4.4 `enterprise_region_summary`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| region_id | VARCHAR(20) | 否 | 区域编码 |
| region_name | VARCHAR(100) | 否 | 区域名称 |
| region_type | VARCHAR(20) | 否 | 区域级别 |
| parent_region_id | VARCHAR(20) | 是 | 父区域编码 |
| stat_date | DATE | 否 | 统计日期 |
| enterprise_total / new_enterprise_count / active_enterprise_count | BIGINT | 否 | 企业总数/新增数/活跃数 |
| total_revenue | DECIMAL(20,2) | 是 | 总营收 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`enterprise_region_summary` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `region_id` VARCHAR(20) NOT NULL,
  `region_name` VARCHAR(100) NOT NULL,
  `region_type` VARCHAR(20) NOT NULL,
  `parent_region_id` VARCHAR(20) NULL,
  `stat_date` DATE NOT NULL,
  `enterprise_total` BIGINT NOT NULL DEFAULT 0,
  `new_enterprise_count` BIGINT NOT NULL DEFAULT 0,
  `active_enterprise_count` BIGINT NOT NULL DEFAULT 0,
  `total_revenue` DECIMAL(20,2) NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_region_summary` (`region_id`, `region_type`, `stat_date`),
  KEY `idx_region_summary_parent` (`parent_region_id`, `region_type`, `stat_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 4.5 `enterprise_industry_distribution`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| region_id | VARCHAR(20) | 否 | 区域编码 |
| chain_code | VARCHAR(64) | 否 | 产业链编码 |
| chain_name | VARCHAR(255) | 否 | 产业链名称 |
| enterprise_count | BIGINT | 否 | 企业数 |
| stat_date | DATE | 否 | 统计日期 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`enterprise_industry_distribution` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `region_id` VARCHAR(20) NOT NULL,
  `chain_code` VARCHAR(64) NOT NULL,
  `chain_name` VARCHAR(255) NOT NULL,
  `enterprise_count` BIGINT NOT NULL DEFAULT 0,
  `stat_date` DATE NOT NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_industry_distribution` (`region_id`, `chain_code`, `stat_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 4.6 `enterprise_growth_trend`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| region_id | VARCHAR(20) | 否 | 区域编码 |
| stat_year / stat_month | INT | 否 | 统计年/月 |
| new_enterprise_count | BIGINT | 否 | 当月新增企业数 |
| stat_date | DATE | 否 | 统计日期 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`enterprise_growth_trend` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `region_id` VARCHAR(20) NOT NULL,
  `stat_year` INT NOT NULL,
  `stat_month` INT NOT NULL,
  `new_enterprise_count` BIGINT NOT NULL DEFAULT 0,
  `stat_date` DATE NOT NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_growth_trend` (`region_id`, `stat_year`, `stat_month`, `stat_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 4.7 `enterprise_industry_summary`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| chain_code / chain_name | VARCHAR(64) / VARCHAR(255) | 否 | 产业链编码/名称 |
| stat_year | INT | 否 | 统计年份 |
| enterprise_count / research_staff_total / patent_total / high_tech_count | BIGINT | 否 | 企业/科研人员/专利/高企数 |
| stat_date | DATE | 否 | 统计日期 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`enterprise_industry_summary` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `chain_code` VARCHAR(64) NOT NULL,
  `chain_name` VARCHAR(255) NOT NULL,
  `stat_year` INT NOT NULL,
  `enterprise_count` BIGINT NOT NULL DEFAULT 0,
  `research_staff_total` BIGINT NOT NULL DEFAULT 0,
  `patent_total` BIGINT NOT NULL DEFAULT 0,
  `high_tech_count` BIGINT NOT NULL DEFAULT 0,
  `stat_date` DATE NOT NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_industry_summary` (`chain_code`, `stat_year`, `stat_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 4.8 `enterprise_stat_summary`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| stat_type | VARCHAR(50) | 否 | 统计类型 |
| dim_code / dim_name | VARCHAR(100) / VARCHAR(255) | 否 | 维度编码/名称 |
| stat_year | INT | 否 | 统计年份 |
| stat_value | BIGINT | 否 | 统计值 |
| stat_date | DATE | 否 | 统计日期 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`enterprise_stat_summary` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `stat_type` VARCHAR(50) NOT NULL,
  `dim_code` VARCHAR(100) NOT NULL,
  `dim_name` VARCHAR(255) NOT NULL,
  `stat_year` INT NOT NULL,
  `stat_value` BIGINT NOT NULL DEFAULT 0,
  `stat_date` DATE NOT NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_stat_summary` (`stat_type`, `dim_code`, `stat_year`, `stat_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 4.9 `enterprise_type_scale_stats`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| company_type | VARCHAR(100) | 否 | 企业类型 |
| enterprise_scale | VARCHAR(20) | 否 | 企业规模 |
| region_level | VARCHAR(20) | 否 | 区域级别 |
| region_id | VARCHAR(20) | 否 | 区域编码；采用 Human 最终字段名 |
| region_name | VARCHAR(100) | 否 | 区域名称 |
| enterprise_count | BIGINT | 否 | 企业数 |
| stat_date | DATE | 否 | 统计日期 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`enterprise_type_scale_stats` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `company_type` VARCHAR(100) NOT NULL,
  `enterprise_scale` VARCHAR(20) NOT NULL,
  `region_level` VARCHAR(20) NOT NULL,
  `region_id` VARCHAR(20) NOT NULL,
  `region_name` VARCHAR(100) NOT NULL,
  `enterprise_count` BIGINT NOT NULL DEFAULT 0,
  `stat_date` DATE NOT NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_type_scale_stats` (`company_type`, `enterprise_scale`, `region_level`, `region_id`, `stat_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 4.10 `shenzhen_enterprise_summary`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| stat_type | VARCHAR(50) | 否 | 统计类型 |
| dim_code / dim_name | VARCHAR(100) / VARCHAR(255) | 否 | 维度编码/名称 |
| stat_year | INT | 否 | 统计年份 |
| stat_value | BIGINT | 否 | 统计值 |
| stat_date | DATE | 否 | 统计日期 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`shenzhen_enterprise_summary` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `stat_type` VARCHAR(50) NOT NULL,
  `dim_code` VARCHAR(100) NOT NULL,
  `dim_name` VARCHAR(255) NOT NULL,
  `stat_year` INT NOT NULL DEFAULT 0,
  `stat_value` BIGINT NOT NULL DEFAULT 0,
  `stat_date` DATE NOT NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_sz_summary` (`stat_type`, `dim_code`, `stat_year`, `stat_date`),
  KEY `idx_sz_summary_latest` (`stat_type`, `stat_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 4.11 `enterprise_distribution`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| dimension | VARCHAR(20) | 否 | 分布维度 |
| region_type | VARCHAR(20) | 否 | 区域类型 |
| parent_region_id | VARCHAR(20) | 是 | 父区域编码 |
| region_id / region_name | VARCHAR(20) / VARCHAR(100) | 否 | 区域编码/名称 |
| enterprise_count / new_enterprise_count | BIGINT | 否 | 企业总数/新增数 |
| stat_date | DATE | 否 | 统计日期 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`enterprise_distribution` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `dimension` VARCHAR(20) NOT NULL,
  `region_type` VARCHAR(20) NOT NULL DEFAULT 'standard',
  `parent_region_id` VARCHAR(20) NULL,
  `region_id` VARCHAR(20) NOT NULL,
  `region_name` VARCHAR(100) NOT NULL,
  `enterprise_count` BIGINT NOT NULL DEFAULT 0,
  `new_enterprise_count` BIGINT NOT NULL DEFAULT 0,
  `stat_date` DATE NOT NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ent_distribution` (`dimension`, `region_type`, `region_id`, `stat_date`),
  KEY `idx_ent_distribution_parent` (`dimension`, `region_type`, `parent_region_id`, `stat_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 4.12 `sz_city_benchmark`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| city_code / city_name | VARCHAR(20) / VARCHAR(100) | 否 | 城市编码/名称 |
| is_benchmark / is_national | TINYINT | 否 | 是否标杆/是否全国城市 |
| avg_tech_power / avg_business_power | DECIMAL(10,4) | 是 | 平均技术力/商业力 |
| enterprise_density / chain_completeness | DECIMAL(20,4) | 是 | 企业密度/产业链完整度 |
| key_node_count / sz_count | BIGINT | 是 | 关键节点数/深圳计数 |
| chain_position | VARCHAR(255) | 是 | 产业链位置 |
| sort_order | INT | 否 | 排序 |
| is_active | TINYINT | 否 | 是否启用 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`sz_city_benchmark` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `city_code` VARCHAR(20) NOT NULL,
  `city_name` VARCHAR(100) NOT NULL,
  `is_benchmark` TINYINT NOT NULL DEFAULT 0,
  `is_national` TINYINT NOT NULL DEFAULT 0,
  `avg_tech_power` DECIMAL(10,4) NULL,
  `avg_business_power` DECIMAL(10,4) NULL,
  `enterprise_density` DECIMAL(20,4) NULL,
  `chain_completeness` DECIMAL(20,4) NULL,
  `key_node_count` BIGINT NULL,
  `sz_count` BIGINT NULL,
  `chain_position` VARCHAR(255) NULL,
  `sort_order` INT NOT NULL DEFAULT 0,
  `is_active` TINYINT NOT NULL DEFAULT 1,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_city_benchmark_code` (`city_code`),
  KEY `idx_city_benchmark_active_sort` (`is_active`, `sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

现存表采用原结构重命名，不按上面 DDL 重建：

```sql
RENAME TABLE `gkxlumenx_dwd`.`dwd_sz_city_benchmark`
         TO `gkxlumenx_dwd`.`sz_city_benchmark`;
```

## 5. 风险表字段字典与完整 DDL

### 5.1 `risk_judicial_case`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| org_id / org_name | VARCHAR(64) / VARCHAR(255) | 否/是 | 企业 ID/名称 |
| case_id | VARCHAR(64) | 否 | 唯一业务 ID |
| case_no / case_title / case_type_tag | VARCHAR(255) | 是 | 案号/标题/案件类型标签 |
| amount | DECIMAL(20,2) | 是 | 涉案金额 |
| court / status / case_role / current_procedure | VARCHAR(255) | 是 | 法院/状态/角色/当前程序 |
| event_date / procedure_date | DATE | 是 | 旧事件日期/业务程序日期 |
| case_cause | VARCHAR(500) | 是 | 案由 |
| is_history | TINYINT | 否 | 历史标记 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_judicial_case` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `org_name` VARCHAR(255) NULL,
  `case_id` VARCHAR(64) NOT NULL,
  `case_no` VARCHAR(255) NULL,
  `case_title` VARCHAR(500) NULL,
  `case_type_tag` VARCHAR(100) NULL,
  `amount` DECIMAL(20,2) NULL,
  `court` VARCHAR(255) NULL,
  `event_date` DATE NULL,
  `status` VARCHAR(50) NULL,
  `case_role` VARCHAR(100) NULL,
  `case_cause` VARCHAR(500) NULL,
  `current_procedure` VARCHAR(100) NULL,
  `procedure_date` DATE NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_judicial_case_id` (`case_id`),
  KEY `idx_risk_judicial_case_org_date` (`org_id`, `procedure_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.2 `risk_dishonest`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| dishonest_id | VARCHAR(64) | 否 | 唯一业务 ID |
| org_id / org_name | VARCHAR(64) / VARCHAR(255) | 否/是 | 企业 ID/名称 |
| case_no / case_title | VARCHAR(255) / VARCHAR(500) | 是 | 案号/标题 |
| amount | DECIMAL(20,2) | 是 | 金额 |
| court / exec_court | VARCHAR(255) | 是 | 法院/执行法院 |
| event_date / filing_date / publish_date | DATE | 是 | 旧事件/立案/发布日期 |
| status / fulfillment_status | VARCHAR(100) | 是 | 状态/履行状态 |
| dishonest_behavior / legal_obligation | TEXT | 是 | 失信行为/法定义务 |
| is_history | TINYINT | 否 | 历史标记 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_dishonest` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `dishonest_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `org_name` VARCHAR(255) NULL,
  `case_no` VARCHAR(255) NULL,
  `case_title` VARCHAR(500) NULL,
  `amount` DECIMAL(20,2) NULL,
  `court` VARCHAR(255) NULL,
  `event_date` DATE NULL,
  `status` VARCHAR(50) NULL,
  `dishonest_behavior` TEXT NULL,
  `exec_court` VARCHAR(255) NULL,
  `filing_date` DATE NULL,
  `fulfillment_status` VARCHAR(100) NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `legal_obligation` TEXT NULL,
  `publish_date` DATE NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_dishonest_id` (`dishonest_id`),
  KEY `idx_risk_dishonest_org_date` (`org_id`, `publish_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.3 `risk_executed`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| org_id / org_name | VARCHAR(64) / VARCHAR(255) | 否/是 | 企业 ID/名称 |
| case_no / case_title / exec_person_id | VARCHAR(255) / VARCHAR(500) / VARCHAR(64) | 否/是/否 | 案号/标题/被执行人 ID |
| amount | DECIMAL(20,2) | 是 | 金额 |
| court / exec_court | VARCHAR(255) | 是 | 法院/执行法院 |
| event_date / filing_date | DATE | 是 | 旧事件/立案日期 |
| status / exec_status / exec_target | VARCHAR(100) | 是 | 状态/执行状态/执行标的 |
| is_history | TINYINT | 否 | 历史标记 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_executed` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `org_name` VARCHAR(255) NULL,
  `case_no` VARCHAR(255) NOT NULL,
  `case_title` VARCHAR(500) NULL,
  `amount` DECIMAL(20,2) NULL,
  `court` VARCHAR(255) NULL,
  `event_date` DATE NULL,
  `status` VARCHAR(50) NULL,
  `exec_court` VARCHAR(255) NULL,
  `exec_person_id` VARCHAR(64) NOT NULL,
  `exec_status` VARCHAR(100) NULL,
  `exec_target` VARCHAR(255) NULL,
  `filing_date` DATE NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_executed` (`org_id`, `case_no`, `exec_person_id`),
  KEY `idx_risk_executed_org_date` (`org_id`, `filing_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.4 `risk_limit_high`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| case_id | VARCHAR(64) | 否 | 写入原 `xhfgk_id`，唯一 |
| org_id / org_name | VARCHAR(64) / VARCHAR(255) | 否/是 | 企业 ID/名称 |
| case_no / case_title | VARCHAR(255) / VARCHAR(500) | 是 | 案号/标题 |
| court / person_name / status | VARCHAR(255) | 是 | 法院/限制对象/状态 |
| filing_date | DATE | 是 | 立案日期 |
| is_history | TINYINT | 否 | 历史标记 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_limit_high` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `org_name` VARCHAR(255) NULL,
  `case_no` VARCHAR(255) NULL,
  `case_title` VARCHAR(500) NULL,
  `court` VARCHAR(255) NULL,
  `person_name` VARCHAR(255) NULL,
  `filing_date` DATE NULL,
  `status` VARCHAR(50) NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_limit_high_case` (`case_id`),
  KEY `idx_risk_limit_high_org_date` (`org_id`, `filing_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.5 `risk_lawsuit` 与 `risk_lawsuit_party`

| 表 | 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|---|
| 主表 | id | BIGINT | 否 | 自增主键 |
| 主表 | case_id | VARCHAR(64) | 否 | 写入原 `judgment_doc_id`，唯一 |
| 主表 | case_no / case_type / case_title | VARCHAR(255) / VARCHAR(100) / VARCHAR(500) | 是 | 案号/类型/标题 |
| 主表 | judgment_date / publish_date | DATE | 是 | 判决/发布日期 |
| 主表 | case_reason / case_cause | VARCHAR(500) | 是 | 案件原因/案由 |
| 主表 | court | VARCHAR(255) | 是 | 法院 |
| 主表 | amount | DECIMAL(20,2) | 是 | 金额 |
| 主表 | create_time / update_time | DATETIME | 否 | 创建/更新时间 |
| party | id | BIGINT | 否 | 自增主键 |
| party | case_id / org_id | VARCHAR(64) | 否 | 案件/企业 ID |
| party | party_name / party_role | VARCHAR(255) / VARCHAR(100) | 是/否 | 当事人名称/角色 |
| party | is_history | TINYINT | 否 | 历史标记 |
| party | create_time | DATETIME | 否 | 创建时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_lawsuit` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `case_no` VARCHAR(255) NULL,
  `case_type` VARCHAR(100) NULL,
  `case_title` VARCHAR(500) NULL,
  `judgment_date` DATE NULL,
  `publish_date` DATE NULL,
  `case_reason` VARCHAR(500) NULL,
  `court` VARCHAR(255) NULL,
  `amount` DECIMAL(20,2) NULL,
  `case_cause` VARCHAR(500) NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_lawsuit_case` (`case_id`),
  KEY `idx_risk_lawsuit_date` (`judgment_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `gkxlumenx_dwd`.`risk_lawsuit_party` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `party_name` VARCHAR(255) NULL,
  `party_role` VARCHAR(100) NOT NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_lawsuit_party` (`case_id`, `org_id`, `party_role`),
  KEY `idx_risk_lawsuit_party_org` (`org_id`, `is_history`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.6 `risk_court_filed` 与 `risk_court_filed_party`

| 表 | 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|---|
| 主表 | id | BIGINT | 否 | 自增主键 |
| 主表 | case_id | VARCHAR(64) | 否 | 写入原 `case_unique_id`，唯一 |
| 主表 | case_no / case_title / court / case_status | VARCHAR(255) | 是 | 案号/标题/法院/状态 |
| 主表 | filing_date / closing_date / hearing_date | DATE | 是 | 立案/结案/开庭日期 |
| 主表 | create_time / update_time | DATETIME | 否 | 创建/更新时间 |
| party | id | BIGINT | 否 | 自增主键 |
| party | case_id / org_id | VARCHAR(64) | 否 | 案件/企业 ID |
| party | party_name / party_role | VARCHAR(255) / VARCHAR(100) | 是/否 | 当事人名称/角色 |
| party | is_history | TINYINT | 否 | 历史标记 |
| party | create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_court_filed` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `case_no` VARCHAR(255) NULL,
  `case_title` VARCHAR(500) NULL,
  `court` VARCHAR(255) NULL,
  `filing_date` DATE NULL,
  `case_status` VARCHAR(100) NULL,
  `closing_date` DATE NULL,
  `hearing_date` DATE NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_court_filed_case` (`case_id`),
  KEY `idx_risk_court_filed_date` (`filing_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `gkxlumenx_dwd`.`risk_court_filed_party` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `party_name` VARCHAR(255) NULL,
  `party_role` VARCHAR(100) NOT NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_court_filed_party` (`case_id`, `org_id`, `party_role`),
  KEY `idx_risk_court_filed_party_org` (`org_id`, `is_history`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.7 `risk_court_notice` 与 `risk_court_notice_party`

| 表 | 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|---|
| 主表 | id | BIGINT | 否 | 自增主键 |
| 主表 | case_id | VARCHAR(64) | 否 | 写入原 `notice_id`，唯一 |
| 主表 | case_no / court / case_cause / case_title | VARCHAR(255) / VARCHAR(255) / VARCHAR(500) / VARCHAR(500) | 是 | 案号/法院/案由/标题 |
| 主表 | hearing_date | DATE | 是 | 开庭日期 |
| 主表 | context | TEXT | 是 | 公告正文 |
| 主表 | create_time / update_time | DATETIME | 否 | 创建/更新时间 |
| party | id | BIGINT | 否 | 自增主键 |
| party | case_id / org_id | VARCHAR(64) | 否 | 案件/企业 ID |
| party | party_name / party_role | VARCHAR(255) / VARCHAR(100) | 是/否 | 当事人名称/角色 |
| party | is_history | TINYINT | 否 | 历史标记 |
| party | create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_court_notice` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `case_no` VARCHAR(255) NULL,
  `court` VARCHAR(255) NULL,
  `case_cause` VARCHAR(500) NULL,
  `hearing_date` DATE NULL,
  `case_title` VARCHAR(500) NULL,
  `context` TEXT NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_court_notice_case` (`case_id`),
  KEY `idx_risk_court_notice_date` (`hearing_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `gkxlumenx_dwd`.`risk_court_notice_party` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `party_name` VARCHAR(255) NULL,
  `party_role` VARCHAR(100) NOT NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_court_notice_party` (`case_id`, `org_id`, `party_role`),
  KEY `idx_risk_court_notice_party_org` (`org_id`, `is_history`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.8 `risk_court_announcement` 与 `risk_court_announcement_party`

| 表 | 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|---|
| 主表 | id | BIGINT | 否 | 自增主键 |
| 主表 | case_id | VARCHAR(64) | 否 | 写入原 `notice_id`，唯一 |
| 主表 | case_title | VARCHAR(500) | 是 | Python 映射为稳定 API `notice_name` |
| 主表 | context | TEXT | 是 | 公告正文，保留 |
| 主表 | case_no / notice_type / court | VARCHAR(255) | 是 | 案号/公告类型/法院 |
| 主表 | notice_date / publish_date | DATE | 是 | 公告/发布日期 |
| 主表 | create_time / update_time | DATETIME | 否 | 创建/更新时间 |
| party | id | BIGINT | 否 | 自增主键 |
| party | case_id / org_id | VARCHAR(64) | 否 | 案件/企业 ID |
| party | party_name / party_role | VARCHAR(255) / VARCHAR(100) | 是/否 | 当事人名称/角色 |
| party | is_history | TINYINT | 否 | 历史标记 |
| party | create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_court_announcement` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `case_title` VARCHAR(500) NULL,
  `context` TEXT NULL,
  `case_no` VARCHAR(255) NULL,
  `notice_type` VARCHAR(100) NULL,
  `court` VARCHAR(255) NULL,
  `notice_date` DATE NULL,
  `publish_date` DATE NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_court_announcement_case` (`case_id`),
  KEY `idx_risk_court_announcement_date` (`publish_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `gkxlumenx_dwd`.`risk_court_announcement_party` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `party_name` VARCHAR(255) NULL,
  `party_role` VARCHAR(100) NOT NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_court_announcement_party` (`case_id`, `org_id`, `party_role`),
  KEY `idx_risk_court_announcement_party_org` (`org_id`, `is_history`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.9 `risk_equity_freeze`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| case_id | VARCHAR(64) | 否 | 写入原 `judicial_assist_id`，唯一 |
| org_id / org_name | VARCHAR(64) / VARCHAR(255) | 否/是 | 企业 ID/名称 |
| case_no / executed_person | VARCHAR(255) | 是 | 案号/被执行人 |
| amount | DECIMAL(20,2) | 是 | 冻结股权数额 |
| court / status | VARCHAR(255) / VARCHAR(50) | 是 | 执行法院/状态 |
| event_date | DATE | 是 | 最终字段保留的事件日期；当前 API 不据此排序 |
| is_history | TINYINT | 否 | 历史标记 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_equity_freeze` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `org_name` VARCHAR(255) NULL,
  `case_no` VARCHAR(255) NULL,
  `executed_person` VARCHAR(255) NULL,
  `amount` DECIMAL(20,2) NULL,
  `court` VARCHAR(255) NULL,
  `event_date` DATE NULL,
  `status` VARCHAR(50) NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_equity_freeze_case` (`case_id`),
  KEY `idx_risk_equity_freeze_org` (`org_id`, `is_history`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.10 `risk_equity_pledge`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| case_id | VARCHAR(64) | 否 | 写入原 `pledge_id`，唯一 |
| org_id / org_name | VARCHAR(64) / VARCHAR(255) | 否/是 | 企业 ID/名称 |
| case_no / reg_no | VARCHAR(255) / VARCHAR(100) | 是 | 案号/登记编号 |
| amount / equity_amount | DECIMAL(20,2) | 是 | 金额/出质股权数额 |
| pledgor / pledgee | VARCHAR(255) | 是 | 出质人/质权人 |
| pledge_reg_date | DATE | 是 | 出质登记日期 |
| status | VARCHAR(50) | 是 | 状态 |
| is_history | TINYINT | 否 | 历史标记 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_equity_pledge` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `org_name` VARCHAR(255) NULL,
  `case_no` VARCHAR(255) NULL,
  `reg_no` VARCHAR(100) NULL,
  `amount` DECIMAL(20,2) NULL,
  `pledgor` VARCHAR(255) NULL,
  `pledgee` VARCHAR(255) NULL,
  `equity_amount` DECIMAL(20,2) NULL,
  `pledge_reg_date` DATE NULL,
  `status` VARCHAR(50) NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_equity_pledge_case` (`case_id`),
  KEY `idx_risk_equity_pledge_org_date` (`org_id`, `pledge_reg_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.11 `risk_zhongben`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| org_id / org_name | VARCHAR(64) / VARCHAR(255) | 否/是 | 企业 ID/名称 |
| case_no | VARCHAR(255) | 否 | 案号 |
| filing_date / termination_date | DATE | 是 | 立案/终本日期 |
| exec_target_amount / unfulfilled_amount | DECIMAL(20,2) | 是 | 执行标的/未履行金额 |
| court / status | VARCHAR(255) / VARCHAR(50) | 是 | 执行法院/状态 |
| is_history | TINYINT | 否 | 历史标记 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_zhongben` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `org_name` VARCHAR(255) NULL,
  `case_no` VARCHAR(255) NOT NULL,
  `filing_date` DATE NULL,
  `termination_date` DATE NULL,
  `exec_target_amount` DECIMAL(20,2) NULL,
  `court` VARCHAR(255) NULL,
  `unfulfilled_amount` DECIMAL(20,2) NULL,
  `status` VARCHAR(50) NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_zhongben` (`org_id`, `case_no`),
  KEY `idx_risk_zhongben_org_date` (`org_id`, `filing_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.12 `risk_chattel_mortgage`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| org_id / org_name | VARCHAR(64) / VARCHAR(255) | 否/是 | 企业 ID/名称 |
| reg_no | VARCHAR(100) | 否 | 登记编号 |
| amount / guarantee_amount | DECIMAL(20,2) | 是 | 金额/担保金额 |
| mortgagee / reg_org / guarantee_type / status | VARCHAR(255) | 是 | 抵押权人/登记机关/担保类型/状态 |
| reg_date / public_date | DATE | 是 | 登记/公示日期 |
| guarantee_scope | TEXT | 是 | 担保范围 |
| is_history | TINYINT | 否 | 历史标记 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_chattel_mortgage` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `org_name` VARCHAR(255) NULL,
  `reg_no` VARCHAR(100) NOT NULL,
  `amount` DECIMAL(20,2) NULL,
  `mortgagee` VARCHAR(255) NULL,
  `reg_date` DATE NULL,
  `reg_org` VARCHAR(255) NULL,
  `guarantee_type` VARCHAR(100) NULL,
  `guarantee_amount` DECIMAL(20,2) NULL,
  `status` VARCHAR(50) NULL,
  `guarantee_scope` TEXT NULL,
  `public_date` DATE NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_chattel_mortgage` (`org_id`, `reg_no`),
  KEY `idx_risk_chattel_org_date` (`org_id`, `reg_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.13 `risk_judicial_sale` 与 `risk_judicial_sale_party`

| 表 | 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|---|
| 主表 | id | BIGINT | 否 | 自增主键 |
| 主表 | case_id | VARCHAR(64) | 否 | 写入原 `notice_id`，唯一 |
| 主表 | case_no / asset_disposal_unit / court | VARCHAR(255) | 是 | 案号/处置单位/法院 |
| 主表 | notice_name / subject_matter | VARCHAR(500) | 是 | 公告名/拍卖标的 |
| 主表 | notice_time / auction_start_date / auction_end_date | DATE | 是 | 公告/拍卖起止日期 |
| 主表 | amount | DECIMAL(20,2) | 是 | 金额 |
| 主表 | create_time / update_time | DATETIME | 否 | 创建/更新时间 |
| party | id | BIGINT | 否 | 自增主键 |
| party | case_id / org_id | VARCHAR(64) | 否 | 案件/企业 ID |
| party | party_name / party_role | VARCHAR(255) / VARCHAR(100) | 是/否 | 当事人名称/角色 |
| party | is_history | TINYINT | 否 | 历史标记 |
| party | create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_judicial_sale` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `case_no` VARCHAR(255) NULL,
  `notice_name` VARCHAR(500) NULL,
  `notice_time` DATE NULL,
  `asset_disposal_unit` VARCHAR(255) NULL,
  `subject_matter` VARCHAR(500) NULL,
  `amount` DECIMAL(20,2) NULL,
  `court` VARCHAR(255) NULL,
  `auction_start_date` DATE NULL,
  `auction_end_date` DATE NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_judicial_sale_case` (`case_id`),
  KEY `idx_risk_judicial_sale_date` (`notice_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `gkxlumenx_dwd`.`risk_judicial_sale_party` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `party_name` VARCHAR(255) NULL,
  `party_role` VARCHAR(100) NOT NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_judicial_sale_party` (`case_id`, `org_id`, `party_role`),
  KEY `idx_risk_judicial_sale_party_org` (`org_id`, `is_history`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.14 `risk_bankruptcy` 与 `risk_bankruptcy_party`

| 表 | 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|---|
| 主表 | id | BIGINT | 否 | 自增主键 |
| 主表 | case_id | VARCHAR(64) | 否 | 案件唯一 ID |
| 主表 | case_no / case_type / court | VARCHAR(255) | 是 | 案号/类型/受理法院 |
| 主表 | public_date | DATE | 是 | 公示日期 |
| 主表 | create_time / update_time | DATETIME | 否 | 创建/更新时间 |
| party | id | BIGINT | 否 | 自增主键 |
| party | case_id / org_id | VARCHAR(64) | 否 | 案件/企业 ID |
| party | party_name / party_role | VARCHAR(255) / VARCHAR(100) | 是/否 | 当事人名称/角色 |
| party | is_history | TINYINT | 否 | 历史标记 |
| party | create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_bankruptcy` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `case_no` VARCHAR(255) NULL,
  `case_type` VARCHAR(100) NULL,
  `court` VARCHAR(255) NULL,
  `public_date` DATE NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_bankruptcy_case` (`case_id`),
  KEY `idx_risk_bankruptcy_date` (`public_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `gkxlumenx_dwd`.`risk_bankruptcy_party` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `party_name` VARCHAR(255) NULL,
  `party_role` VARCHAR(100) NOT NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_bankruptcy_party` (`case_id`, `org_id`, `party_role`),
  KEY `idx_risk_bankruptcy_party_org` (`org_id`, `is_history`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.15 `risk_abnormal`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| case_id | VARCHAR(64) | 否 | 写入原 `abnormal_id`，唯一 |
| org_id / org_name | VARCHAR(64) / VARCHAR(255) | 否/是 | 企业 ID/名称 |
| reason / decision_org / status | VARCHAR(500) / VARCHAR(255) / VARCHAR(50) | 是 | 原因/决定机关/状态 |
| abn_date / remove_date | DATE | 是 | 列入/移出日期 |
| is_history | TINYINT | 否 | 历史标记 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_abnormal` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `org_name` VARCHAR(255) NULL,
  `reason` VARCHAR(500) NULL,
  `decision_org` VARCHAR(255) NULL,
  `abn_date` DATE NULL,
  `remove_date` DATE NULL,
  `status` VARCHAR(50) NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_abnormal_case` (`case_id`),
  KEY `idx_risk_abnormal_org_date` (`org_id`, `abn_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.16 `risk_punishment`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| case_id | VARCHAR(64) | 否 | 写入原 `penalty_id` |
| org_id / org_name | VARCHAR(64) / VARCHAR(255) | 否/是 | 企业 ID/名称 |
| doc_no / decision_org / status | VARCHAR(255/255/50) | 是 | 文书号/决定机关/状态 |
| reason | TEXT | 是 | 处罚原因；源数据最长超过 500 字符，使用 TEXT 避免截断 |
| fine_amount / confiscate_amount | DECIMAL(20,2) | 是 | 罚款/没收金额 |
| penalty_date / public_date | DATE | 是 | 处罚/公示日期 |
| is_history | TINYINT | 否 | 历史标记 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_punishment` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `org_name` VARCHAR(255) NULL,
  `doc_no` VARCHAR(255) NULL,
  `reason` TEXT NULL,
  `fine_amount` DECIMAL(20,2) NULL,
  `confiscate_amount` DECIMAL(20,2) NULL,
  `decision_org` VARCHAR(255) NULL,
  `penalty_date` DATE NULL,
  `public_date` DATE NULL,
  `status` VARCHAR(50) NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_punishment` (`case_id`, `org_id`),
  KEY `idx_risk_punishment_org_date` (`org_id`, `penalty_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.17 `risk_illegal`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| case_id | VARCHAR(64) | 否 | 写入原 `sv_id`，唯一 |
| org_id / org_name | VARCHAR(64) / VARCHAR(255) | 否/是 | 企业 ID/名称 |
| reason / decision_org / status | VARCHAR(500) / VARCHAR(255) / VARCHAR(50) | 是 | 原因/决定机关/状态 |
| abn_date / remove_date | DATE | 是 | 列入/移出日期 |
| is_history | TINYINT | 否 | 历史标记 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_illegal` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `org_name` VARCHAR(255) NULL,
  `reason` VARCHAR(500) NULL,
  `decision_org` VARCHAR(255) NULL,
  `abn_date` DATE NULL,
  `remove_date` DATE NULL,
  `status` VARCHAR(50) NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_illegal_case` (`case_id`),
  KEY `idx_risk_illegal_org_date` (`org_id`, `abn_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 5.18 `risk_tax_punish`

| 字段 | MySQL 类型 | 可空 | 说明 |
|---|---|---|---|
| id | BIGINT | 否 | 自增主键 |
| case_id | VARCHAR(64) | 否 | 写入原 `tax_vio_id`，唯一 |
| org_id | VARCHAR(64) | 否 | 企业 ID |
| case_no | VARCHAR(255) | 是 | 案号 |
| reason / tax_vio_type / status | VARCHAR(500) / VARCHAR(100) / VARCHAR(50) | 是 | 原因/税收违法类型/状态 |
| amount | DECIMAL(20,2) | 是 | 金额 |
| publish_date | DATE | 是 | 发布日期 |
| is_history | TINYINT | 否 | 历史标记 |
| create_time / update_time | DATETIME | 否 | 创建/更新时间 |

```sql
CREATE TABLE `gkxlumenx_dwd`.`risk_tax_punish` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `case_id` VARCHAR(64) NOT NULL,
  `org_id` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `case_no` VARCHAR(255) NULL,
  `reason` VARCHAR(500) NULL,
  `amount` DECIMAL(20,2) NULL,
  `publish_date` DATE NULL,
  `tax_vio_type` VARCHAR(100) NULL,
  `status` VARCHAR(50) NULL,
  `is_history` TINYINT NOT NULL DEFAULT 0,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_risk_tax_punish_case` (`case_id`),
  KEY `idx_risk_tax_punish_org_date` (`org_id`, `publish_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

## 6. 风险表 Python 稳定 API 兼容映射

Python Repository 应在 SQL/Repository 层完成下表映射；Java API 契约不改。

| 风险表 | DWD → 稳定 API 映射 | 事件排序字段 | `is_history` 来源 |
|---|---|---|---|
| risk_judicial_case | `case_type_tag` 等字段直出 | `procedure_date` | 主表 |
| risk_dishonest | `dishonest_id` 等字段直出 | `publish_date` | 主表 |
| risk_executed | `exec_person_id` 等字段直出 | `filing_date` | 主表 |
| risk_limit_high | `case_id → xhfgk_id`; `person_name → rhc_person_name` | `filing_date` | 主表 |
| risk_lawsuit | `case_id → judgment_doc_id`; `court → court_name`; `case_title → doc_title` | `judgment_date` | party |
| risk_court_filed | `case_id → case_unique_id`; `court → court_name` | `filing_date` | party |
| risk_court_notice | `case_id → notice_id`; `court → court_name` | `hearing_date` | party |
| risk_court_announcement | `case_id → notice_id`; `case_title → notice_name`; `court → court_name` | `publish_date` | party |
| risk_equity_freeze | `case_id → judicial_assist_id`; `amount → equity_amount`; `court → exec_court` | 无，沿用稳定接口按 ID 的确定性顺序 | 主表 |
| risk_equity_pledge | `case_id → pledge_id`，其余稳定字段直出 | `pledge_reg_date` | 主表 |
| risk_zhongben | `court → exec_court`，其余稳定字段直出 | `filing_date` | 主表 |
| risk_chattel_mortgage | 稳定字段直出 | `reg_date` | 主表 |
| risk_judicial_sale | `case_id → notice_id` | `notice_time` | party |
| risk_bankruptcy | `court → handling_court`，`case_no` 等字段直出 | `public_date` | party |
| risk_abnormal | `case_id → abnormal_id` | `abn_date` | 主表 |
| risk_punishment | `case_id → penalty_id`; `doc_no → decision_no`; `reason → penalty_reason` | `penalty_date` | 主表 |
| risk_illegal | `case_id → sv_id` | `abn_date` | 主表 |
| risk_tax_punish | `case_id → tax_vio_id`; `tax_vio_type` 直出 | `publish_date` | 主表 |

拆分案件统一先由 party 表按 `org_id`、`is_history` 定位关联，再以 `case_id` JOIN 主表。返回结果中的 `is_history` 取 party 表值。`risk_lawsuit_party` 按 Human 最终字段仅有 `create_time`，其余五张 party 表同时包含 `update_time`。

## 7. 稳定 API 空字段返回规则

以下稳定 API 字段不进入最终 DWD。Python 必须保留字段名并显式返回 JSON `null`，不得删除字段、伪造值或改变响应结构：

| 风险接口 | 稳定 API 字段 | 返回规则 |
|---|---|---|
| risk_limit_high | `doc_url` | `null` |
| risk_lawsuit | `trial_procedure` | `null` |
| risk_court_filed | `case_cause` | `null` |
| risk_court_filed | `trial_procedure` | `null` |
| risk_equity_freeze | `type_status` | `null` |
| risk_judicial_sale | `source_website` | `null` |
| risk_judicial_sale | `original_link` | `null` |

数据库可空字段本身无值时，Python 同样按原字段名返回 `null`，不使用空字符串、`0` 或占位文本替代未知值。

## 8. 迁移说明

本文是目标结构正式候选，不直接执行任何数据库变更。现存表不能简单执行本文 `CREATE TABLE`；DBA 必须先对现库逐表做结构 diff，再生成经过评审的 `ALTER TABLE`、数据回填和索引切换脚本。缺表才可采用对应 `CREATE TABLE` DDL。

迁移必须满足：

1. 保持 Java 已接入的 API 路径、请求和响应结构不变。
2. Python Repository 在数据库切换前完成兼容映射，但实际代码变更不属于本文操作。
3. 字段改名、业务 ID 迁移和日期转换必须先回填、校验，再切换读路径；不得直接丢弃旧列。
4. 新唯一索引上线前必须完成重复数据审计；发现冲突由 DBA/数据负责人处理，不能依赖 `IGNORE` 静默丢数。
5. `is_history` 必须依据来源数据或明确规则回填；不得默认把全部历史记录标记为当前。
6. 拆分案件的主表与 party 表必须核对孤儿记录和一对多关系完整性。

## 9. 迁移执行清单（2026-08-03 前置计划，现已执行）

1. 在 `gkxlumenx_dwd` 对现存 36 张目标表做 `SHOW CREATE TABLE` 快照和数据量、重复键审计。
2. 为现存差异表生成逐表 `ALTER TABLE`，包括字段新增、改名、类型转换、默认值和索引调整；本文不自动执行。
3. 创建当前缺失的 `shenzhen_enterprise_summary`、`enterprise_distribution` 及其他经盘点确认缺失的目标表。
4. 执行并验证：
   `RENAME TABLE gkxlumenx_dwd.dwd_sz_city_benchmark TO gkxlumenx_dwd.sz_city_benchmark`。
5. 对 `risk_limit_high` 将原 `xhfgk_id` 回填至 `case_id`，确认非空和唯一后建立 `case_id` 唯一索引；最终目标表不保留 `xhfgk_id`。
6. 对 `risk_equity_freeze` 将原 `judicial_assist_id` 回填至 `case_id`，确认非空和唯一后建立 `case_id` 唯一索引；最终目标表不保留 `judicial_assist_id`。
7. 对其余最终字段含 `case_id` 的风险表，按本文兼容映射回填原业务 ID，并在删除/停用旧列前完成抽样和全量校验。
8. 为 6 组拆分案件迁移 party 关联，校验 `case_id + org_id + party_role` 重复、主表孤儿和 party 孤儿。
9. 回填直接关联企业风险主表的 `is_history`，回填 6 张 party 表的 `is_history`，并核对当前/历史计数。
10. 按各表业务日期字段完成 DATE 清洗与非法值隔离；`risk_equity_freeze` 当前无稳定排序日期口径，不自行推导。
11. 在线创建或切换所有唯一索引和查询索引，评估锁表窗口、回滚脚本和磁盘空间。
12. 完成迁移前后行数、唯一键、空值率、抽样字段映射和稳定 API 回归验证，并保留审计报告。

## 10. 自检清单

- [x] 正式范围恰为 36 张：12 张非风险表 + 18 张风险主表 + 6 张风险 party 表。
- [x] 未纳入旧设计中的其他未复核表。
- [x] 库名为 `gkxlumenx_dwd`，目标表名均无 `dwd_` 前缀。
- [x] 每张表均有字段字典和 MySQL 8 完整 DDL。
- [x] 统计表唯一键采用 Human 二次确认后的完整复合维度。
- [x] `risk_judicial_case` 使用 `case_type_tag`、`is_history`。
- [x] `risk_tax_punish` 使用 `tax_vio_type`。
- [x] `risk_limit_high` 只保留 `case_id`，由原 `xhfgk_id` 回填并映射回 API。
- [x] `risk_equity_freeze` 只保留 `case_id`，由原 `judicial_assist_id` 回填并映射回 API。
- [x] `risk_court_announcement.case_title` 映射稳定 API `notice_name`，`context` 保留。
- [x] 直接企业风险表的 `is_history` 在主表，拆分案件的 `is_history` 在 party 表。
- [x] 已列明稳定 API 空字段返回规则。
- [x] 原候选稿已明确迁移约束；后续经 human 授权改由 agent 直接执行，实际结果记录于 §11。

## 11. 2026-08-03 真实库 As-built

- 目标库：公网 MySQL `gkxlumenx_dwd`。
- 执行前已保留结构快照，并对 10 张有数据目标表完成结构+数据完整备份。
- 9 张有数据差异表采用目标暂存表迁移；字段映射后逐表核对迁移前后行数一致，再通过单条 `RENAME TABLE` 原子切换。
- 24 张风险表迁移前均为 0 行，按本文 DDL 建立目标结构后与非风险表一并原子切换。
- 已创建 `shenzhen_enterprise_summary`、`enterprise_distribution`。
- 已将 `dwd_sz_city_benchmark` 重命名为 `sz_city_benchmark`，保留原 8 行数据。
- 迁移结果：36/36 张目标表存在，暂存 `__v3` 表为 0；33 张原结构表保留为 `__pre_v3`，用于观察期内快速回退。
- 已完成关键风险 alias、party `case_id` JOIN、非风险查询的 SQL smoke test；应用/K8s 级联调仍需单独验收。
- `__pre_v3` 回退表的最终删除必须在观察窗口结束后由 human 确认，本次未删除。

### 11.1 2026-08-12 纠偏迁移 As-built

2026-08-11 数据重载后，4 张风险表被 ODS 原始结构覆盖，另生成 4 张带 `U+200B` 零宽字符的同名表；`risk_bankruptcy_party` 也被覆盖为 ODS 结构。§11 的“36/36 结构一致”仅代表 2026-08-03 当时状态，不能继续作为 2026-08-11 重载后的现网结论。

经 human:徐滕强授权，2026-08-12 执行
`agent-delivery/data/ddl/gkxlumenx_dwd_enterprise_schema_align_20260812.sql`：

- `risk_judicial_case`：规范结构 19,877 行。
- `risk_executed`：规范结构 20,000 行。
- `risk_bankruptcy`：规范主表 20,000 行。
- `risk_bankruptcy_party`：从 20,000 行原始数据中迁移 12,166 行；7,705 条无法关联主表、129 条违反目标唯一键的记录未强塞入规范表，全部仍保留在 `risk_bankruptcy_party__pre_fix_20260812`。
- `risk_abnormal`：规范结构 3,515 行；`is_history` 按 `remove_date` 是否存在确定。
- `risk_punishment`：规范结构 19,992 行；`reason` 使用 `TEXT`，避免 79 条超过 500 字符的源值被截断。
- `risk_illegal`：规范结构 887 行；`is_history` 按 `remove_date` 是否存在确定。
- `risk_tax_punish`：规范结构 10,959 行。
- `risk_dishonest[U+200B]` 为 0 行，已删除；其余 3 张有数据零宽字符表已改为显式 `__raw_u200b_20260812` 备份名。
- 现网正式表名已无 `U+200B`；所有迁移目标表均为 `id BIGINT AUTO_INCREMENT PRIMARY KEY`，必填键缺失数和目标唯一键重复数均为 0。
- 2026-08-12 再将全部含 `org_id` 的规范风险表及
  `enterprise_risk_summary.org_id` 统一为 `utf8mb4_general_ci`；
  与 `enterprise_base` 的直接 JOIN
  已通过，不再出现 `Illegal mix of collations`。
- 风险详情 API 仓契约测试 37/37 通过，算法 DWD 读取测试 7/7 通过，司法/执行/破产/风险汇总现网 SQL smoke test 均返回成功。

回退表 `__pre_fix_20260812` 与原始表 `__raw_u200b_20260812` 在观察期内不得删除；最终清理由 human 确认。
