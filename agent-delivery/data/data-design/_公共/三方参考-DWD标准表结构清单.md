# DWD 标准表结构清单

> **【禁止施工 · 非项目 DWD 真源】**  
> 本文是历史 **PostgreSQL** 库 `demo_gdf_data` / schema `dwd` 的 9 表摘录（含宽表 `enterprise`），**不得**用于国科信正式库建表或 ALTER。  
> **现行建表真源（GDF）**：[`../../GDF/派单包/企业/GDF-ENT-WORKPACK-v2/10-DWD-MySQL-DDL/`](../../GDF/派单包/企业/GDF-ENT-WORKPACK-v2/10-DWD-MySQL-DDL/)  
> **仓内 as-built**：[`../企业/DWD表结构设计-企业工商表-MySQL-v3.1.md`](../企业/DWD表结构设计-企业工商表-MySQL-v3.1.md) · [`../企业/DWD表结构设计-企业模块-MySQL-v3.0.md`](../企业/DWD表结构设计-企业模块-MySQL-v3.0.md) · [`../企业/DWD表结构设计-企业指标汇总表-MySQL-v3.1.md`](../企业/DWD表结构设计-企业指标汇总表-MySQL-v3.1.md)  
> 旧表名对照见 WORKPACK-v2 的 `11-作废与误源对照.md`。

---

**数据库**: 192.168.88.64:15554 / demo_gdf_data（历史参考，非目标）  
**Schema**: dwd  
**表数量**: 9

## 表目录

| # | 表名 | 字段数 | 说明 |
|---|------|--------|------|
| 1 | enterprise | 65 | 企业主表（含基本信息、财务指标、技术指标、评分） |
| 2 | enterprise_business_tag | 7 | 企业业务标签 |
| 3 | enterprise_cooperation | 10 | 企业合作关系 |
| 4 | enterprise_finance_history | 13 | 企业财务历史数据 |
| 5 | enterprise_industry | 8 | 企业产业链归属 |
| 6 | enterprise_parent_subsidiary | 8 | 企业母子公司关系 |
| 7 | enterprise_patent_history | 9 | 企业专利历史数据 |
| 8 | enterprise_supply_chain | 9 | 企业供应链关系 |
| 9 | policy_base_info | 37 | 政策基础信息 |

## 表字段详情

### enterprise

**说明**: 企业主表（含基本信息、财务指标、技术指标、评分）

| # | 字段名 | 数据类型 | 可空 | 备注 |
|---|--------|---------|------|------|
| 1 | id | bigint | 否 | 自增主键 |
| 2 | enterprise_code | character varying(64) | 否 | 统一社会信用代码 |
| 3 | enterprise_name | character varying(255) | 否 | 企业全称 |
| 4 | enterprise_name_short | character varying(100) | 是 | 企业简称 |
| 5 | enterprise_name_en | character varying(255) | 是 | 英文名称 |
| 6 | legal_representative | character varying(100) | 是 | 法定代表人 |
| 7 | registered_capital | numeric | 是 | 注册资本（万元） |
| 8 | paid_in_capital | numeric | 是 | 实缴资本（万元） |
| 9 | registration_date | date | 是 | 成立日期 |
| 10 | business_status | character varying(20) | 是 | 经营状态（在营/吊销/注销/迁出） |
| 11 | enterprise_type | character varying(50) | 是 | 企业类型 |
| 12 | industry_category | character varying(100) | 是 | 所属行业 |
| 13 | industry_code | character varying(20) | 是 | 行业代码 |
| 14 | business_scope | text | 是 | 经营范围 |
| 15 | registered_address | character varying(500) | 是 | 注册地址 |
| 16 | headquarters_city | character varying(100) | 是 | 总部城市 |
| 17 | headquarters_district | character varying(100) | 是 | 总部所在区县 |
| 18 | headquarters_address | character varying(500) | 是 | 总部详细地址 |
| 19 | headquarters_lng | numeric | 是 | 总部经度 |
| 20 | headquarters_lat | numeric | 是 | 总部纬度 |
| 21 | is_listed | smallint | 是 | 是否上市（0否/1是） |
| 22 | listed_market | character varying(50) | 是 | 上市板块 |
| 23 | listed_code | character varying(20) | 是 | 股票代码 |
| 24 | is_foreign | smallint | 是 | 是否外资企业（0否/1是） |
| 25 | is_high_tech | smallint | 是 | 是否高新技术企业（0否/1是） |
| 26 | is_sme | smallint | 是 | 是否小微企业（0否/1是） |
| 27 | is_little_giant | smallint | 是 | 是否专精特新（0否/1是） |
| 28 | little_giant_level | character varying(20) | 是 | 专精特新级别 |
| 29 | is_gazelle | smallint | 是 | 是否瞪羚企业（0否/1是） |
| 30 | is_unicorn | smallint | 是 | 是否独角兽企业（0否/1是） |
| 31 | revenue_latest | numeric | 是 | 最新年营收（万元） |
| 32 | revenue_year | integer | 是 | 营收对应年份 |
| 33 | revenue_growth_rate | numeric | 是 | 营收增长率（%） |
| 34 | net_profit | numeric | 是 | 净利润（万元） |
| 35 | profit_margin | numeric | 是 | 利润率（%） |
| 36 | gross_margin | numeric | 是 | 毛利率（%） |
| 37 | market_share | numeric | 是 | 市场份额（%） |
| 38 | brand_score | numeric | 是 | 品牌声量评分 |
| 39 | customer_concentration | numeric | 是 | 客户集中度（%） |
| 40 | patent_apply_count | integer | 是 | 专利申请数量（累计） |
| 41 | patent_grant_count | integer | 是 | 专利授权数量（累计） |
| 42 | patent_valid_count | integer | 是 | 有效专利数量 |
| 43 | patent_invention_count | integer | 是 | 发明专利数量 |
| 44 | patent_citation_count | integer | 是 | 专利引用次数 |
| 45 | rd_staff_count | integer | 是 | 研发人员数量 |
| 46 | rd_staff_ratio | numeric | 是 | 研发人员占比（%） |
| 47 | rd_investment | numeric | 是 | 研发投入金额（万元） |
| 48 | rd_investment_ratio | numeric | 是 | 研发投入占比（%） |
| 49 | core_tech_coverage | numeric | 是 | 核心技术覆盖度评分 |
| 50 | tech_score | numeric | 是 | 技术力综合得分（0-100） |
| 51 | business_score | numeric | 是 | 商业力综合得分（0-100） |
| 52 | competitiveness_score | numeric | 是 | 综合竞争力得分（0-100） |
| 53 | innovation_index | numeric | 是 | 创新活力指数 |
| 54 | introduction_value | character varying(20) | 是 | 招引价值等级（A/B/C/D） |
| 55 | cultivation_priority | character varying(20) | 是 | 培育优先级（高/中/低） |
| 56 | risk_level | character varying(20) | 是 | 风险等级（低/中/高） |
| 57 | data_source | character varying(100) | 是 | 数据来源 |
| 58 | data_source_url | character varying(500) | 是 | 原始数据URL |
| 59 | data_collect_time | timestamp without time zone | 是 | 数据采集时间 |
| 60 | data_update_time | timestamp without time zone | 是 | 数据更新时间 |
| 61 | data_completeness | numeric | 是 | 数据完整度（0-1） |
| 62 | data_confidence | numeric | 是 | 数据置信度（0-1） |
| 63 | audit_status | character varying(20) | 是 | 人工审核状态 |
| 64 | create_time | timestamp without time zone | 否 | 记录创建时间 |
| 65 | update_time | timestamp without time zone | 否 | 记录更新时间 |

### enterprise_business_tag

**说明**: 企业业务标签

| # | 字段名 | 数据类型 | 可空 | 备注 |
|---|--------|---------|------|------|
| 1 | id | bigint | 否 | 自增主键 |
| 2 | enterprise_id | bigint | 否 | 企业ID |
| 3 | tag_type | character varying(50) | 否 | 标签类型 |
| 4 | tag_name | character varying(100) | 否 | 标签名称 |
| 5 | tag_score | numeric | 是 | 标签关联度评分 |
| 6 | create_time | timestamp without time zone | 否 | 创建时间 |
| 7 | update_time | timestamp without time zone | 否 | 更新时间 |

### enterprise_cooperation

**说明**: 企业合作关系

| # | 字段名 | 数据类型 | 可空 | 备注 |
|---|--------|---------|------|------|
| 1 | id | bigint | 否 | 自增主键 |
| 2 | enterprise_id | bigint | 否 | 企业ID |
| 3 | partner_type | character varying(50) | 否 | 合作方类型 |
| 4 | partner_id | bigint | 是 | 合作方ID |
| 5 | partner_name | character varying(255) | 是 | 合作方名称 |
| 6 | cooperation_type | character varying(50) | 是 | 合作类型 |
| 7 | project_count | integer | 是 | 合作项目数量 |
| 8 | patent_count | integer | 是 | 联合专利数量 |
| 9 | create_time | timestamp without time zone | 否 | 创建时间 |
| 10 | update_time | timestamp without time zone | 否 | 更新时间 |

### enterprise_finance_history

**说明**: 企业财务历史数据

| # | 字段名 | 数据类型 | 可空 | 备注 |
|---|--------|---------|------|------|
| 1 | id | bigint | 否 | 自增主键 |
| 2 | enterprise_id | bigint | 否 | 企业ID |
| 3 | data_year | integer | 否 | 数据年份 |
| 4 | revenue | numeric | 是 | 营收(万元) |
| 5 | revenue_growth_rate | numeric | 是 | 营收增长率(%) |
| 6 | net_profit | numeric | 是 | 净利润(万元) |
| 7 | profit_margin | numeric | 是 | 利润率(%) |
| 8 | gross_margin | numeric | 是 | 毛利率(%) |
| 9 | rd_investment | numeric | 是 | 研发投入(万元) |
| 10 | rd_investment_ratio | numeric | 是 | 研发投入占比(%) |
| 11 | rd_staff_count | integer | 是 | 研发人员数量 |
| 12 | create_time | timestamp without time zone | 否 | 创建时间 |
| 13 | update_time | timestamp without time zone | 否 | 更新时间 |

### enterprise_industry

**说明**: 企业产业链归属

| # | 字段名 | 数据类型 | 可空 | 备注 |
|---|--------|---------|------|------|
| 1 | id | bigint | 否 | 自增主键 |
| 2 | enterprise_id | bigint | 否 | 企业ID |
| 3 | industry_chain | character varying(100) | 否 | 产业链名称 |
| 4 | industry_chain_node | character varying(100) | 是 | 产业链环节 |
| 5 | industry_chain_role | character varying(50) | 是 | 产业链角色 |
| 6 | participation_depth | numeric | 是 | 参与深度评分 |
| 7 | create_time | timestamp without time zone | 否 | 创建时间 |
| 8 | update_time | timestamp without time zone | 否 | 更新时间 |

### enterprise_parent_subsidiary

**说明**: 企业母子公司关系

| # | 字段名 | 数据类型 | 可空 | 备注 |
|---|--------|---------|------|------|
| 1 | id | bigint | 否 | 自增主键 |
| 2 | enterprise_id | bigint | 否 | 本企业ID |
| 3 | parent_enterprise_id | bigint | 是 | 母公司ID |
| 4 | parent_enterprise_name | character varying(255) | 是 | 母公司名称 |
| 5 | ownership_ratio | numeric | 是 | 控股比例(%) |
| 6 | subsidiary_count | integer | 是 | 子公司数量 |
| 7 | create_time | timestamp without time zone | 否 | 创建时间 |
| 8 | update_time | timestamp without time zone | 否 | 更新时间 |

### enterprise_patent_history

**说明**: 企业专利历史数据

| # | 字段名 | 数据类型 | 可空 | 备注 |
|---|--------|---------|------|------|
| 1 | id | bigint | 否 | 自增主键 |
| 2 | enterprise_id | bigint | 否 | 企业ID |
| 3 | data_year | integer | 否 | 数据年份 |
| 4 | patent_apply_count | integer | 是 | 当年专利申请数 |
| 5 | patent_grant_count | integer | 是 | 当年专利授权数 |
| 6 | patent_valid_count | integer | 是 | 当年有效专利数 |
| 7 | patent_citation_count | integer | 是 | 当年专利引用次数 |
| 8 | create_time | timestamp without time zone | 否 | 创建时间 |
| 9 | update_time | timestamp without time zone | 否 | 更新时间 |

### enterprise_supply_chain

**说明**: 企业供应链关系

| # | 字段名 | 数据类型 | 可空 | 备注 |
|---|--------|---------|------|------|
| 1 | id | bigint | 否 | 自增主键 |
| 2 | enterprise_id | bigint | 否 | 本企业ID |
| 3 | related_enterprise_id | bigint | 否 | 关联企业ID |
| 4 | relation_type | character varying(50) | 否 | 关系类型 |
| 5 | relation_strength | numeric | 是 | 关系强度评分 |
| 6 | is_core_supplier | smallint | 是 | 是否核心供应商 |
| 7 | risk_level | character varying(20) | 是 | 断链风险等级 |
| 8 | create_time | timestamp without time zone | 否 | 创建时间 |
| 9 | update_time | timestamp without time zone | 否 | 更新时间 |

### policy_base_info

**说明**: 政策基础信息

| # | 字段名 | 数据类型 | 可空 | 备注 |
|---|--------|---------|------|------|
| 1 | id | bigint | 否 | 主键ID |
| 2 | tenant_id | bigint | 否 | 租户ID |
| 3 | policy_id | character varying(64) | 否 | 政策唯一标识（业务主键，如UUID或业务编码） |
| 4 | title | character varying(500) | 否 | 政策标题 |
| 5 | issued_number | character varying(200) | 是 | 政策文号 |
| 6 | publish_organization | character varying(300) | 否 | 发布机构 |
| 7 | publish_date | date | 否 | 发布日期 |
| 8 | implementation_date | date | 是 | 实施日期 |
| 9 | expire_date | date | 是 | 失效日期 |
| 10 | status | smallint | 否 | 政策状态（1-有效，2-失效，3-修订中，4-即将生效） |
| 11 | publish_year | integer | 否 | 发布年份（冗余字段，便于统计） |
| 12 | level | smallint | 否 | 政策层级（1-国家，2-省级，3-市级，4-区级） |
| 13 | region | character varying(200) | 否 | 政策地区（省/市/区名称，多个用逗号分隔） |
| 14 | abstract | text | 是 | 政策摘要 |
| 15 | keywords | character varying(1000) | 是 | 关键词（多个用逗号分隔） |
| 16 | content | text | 是 | 政策正文内容（全文） |
| 17 | url | character varying(1000) | 是 | 原文链接 |
| 18 | pedigree | text | 是 | 政策谱系/引用政策（JSON格式存储关联政策ID列表） |
| 19 | elements | text | 是 | 政策主旨要素（JSON格式存储结构化要素） |
| 20 | keypoints | text | 是 | 政策要点（JSON格式存储要点列表） |
| 21 | factors | text | 是 | 政策扶持要素（JSON格式存储扶持要素结构化数据） |
| 22 | source | character varying(200) | 否 | 数据来源（如：政府官网、第三方平台） |
| 23 | gis_location | character varying(100) | 是 | 政策发布地GIS坐标（经纬度，格式：lng,lat） |
| 24 | attachment | text | 是 | 附件信息（JSON格式存储附件名称、URL列表） |
| 25 | sci_tech_attribute | smallint | 是 | 科创属性（0-非科创，1-科创政策，2-强科创关联） |
| 26 | application_conditions | text | 是 | 申报条件（结构化文本） |
| 27 | execution_cycle | character varying(200) | 是 | 执行周期（如：2024-01-01 至 2026-12-31） |
| 28 | execution_entity | character varying(300) | 是 | 执行主体（负责政策执行的机构） |
| 29 | related_entities | text | 是 | 关联实体（JSON格式存储关联的产业、企业、人才、科研机构等实体标识） |
| 30 | create_time | timestamp without time zone | 否 | 创建时间 |
| 31 | update_time | timestamp without time zone | 否 | 更新时间 |
| 32 | is_deleted | smallint | 否 | 逻辑删除标记（0-未删除，1-已删除） |
| 33 | ext1 | character varying(500) | 是 | 扩展字段1 |
| 34 | ext2 | character varying(500) | 是 | 扩展字段2 |
| 35 | ext3 | character varying(500) | 是 | 扩展字段3 |
| 36 | ext4 | character varying(500) | 是 | 扩展字段4 |
| 37 | ext5 | character varying(500) | 是 | 扩展字段5 |

