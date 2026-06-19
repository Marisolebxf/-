# 企业相关 ODS → DWD 字段映射分析报告（v2）

> 生成时间: 2026-06-02 ｜ 版本: v2（ODS 数据源切换为三方「要素库」）
> 分析范围: **企业 / 机构相关** 数据域

---

## 1. 背景与版本变更

本报告分析三方采购数据源（ODS 层）能否满足本项目自建 **DWD 企业标准表** 的字段填充需求。

| 项 | v1 | v2（本报告） |
|----|----|----|
| ODS 来源 | PostgreSQL `demo_gdf_data.ods`（`poc_tb_*` 70 张示例表） | 三方「要素库」`db/要素库建表语句.sql`（186 张表，企业/机构相关 74 张） |
| ODS 命名 | 拼音字段名（如 `qi_ye_ming_cheng`） | 规范英文字段名（如 `name_cn`、`credit_code`），且**字段已带中文注释** |
| DWD 目标 | 9 张标准表（不变） | 同 v1，企业相关 8 张：见 `DWD标准表结构清单.md` |
| 数据丰富度 | 工商/年报/专利/股东/投资/社保/产业链 | 在 v1 基础上**新增**：经纬度、上市信息、专利预聚合统计、专利引用、研发投入、企业资质标签、产业链上中下游环节、海外机构/受益人/实控人 等 |

> 命名澄清：要素库 SQL 中的 `dwd_xxx` 是数据供应方命名习惯，其业务定位为**三方数据源 = 本系统 ODS（贴源层）**；本报告右侧 `dwd.enterprise*` 才是本项目自建的 DWD 标准明细层。

**映射状态图例**：
- ✅**直接映射**：ODS 有对应字段，可直接取值或简单类型/枚举转换
- 🔧**需计算/算法**：有数据源但需聚合、公式推导、规则判定或算法模型
- ⚠️**待确认/质量待验**：需进一步探查或字段语义需业务确认
- ❌**无来源**：要素库中无相关数据，需额外采购或暂置空
- 🟦**系统/预留**：主键、时间戳、扩展位等由系统自动填充

## 2. 企业相关 ODS 源表概况

企业/机构相关 ODS 表共 **74 张**，分布于 4 个 Sheet：

| 数据子域 | 来源 Sheet | 表数 | 代表表 |
|----------|-----------|------|--------|
| 国内机构（工商/财务/经营/风险/司法） | 国内机构要素库 | 41 | `dwd_org_reg_info` 机构基本信息、`dwd_org_annual_financial_info` 年报财务、`dwd_org_stock_base/finance_info` 上市信息、`dwd_org_rd_achiev_info` 研发成果产出、`dwd_org_shareholder_info` 股东、`dwd_org_invest_info` 投资、各类风险/司法表 |
| 国外机构 | 国外机构要素库 | 8 | `dwd_forg_base_info` 海外机构基本信息、`dwd_forg_shareholder_info` 股东、`dwd_forg_subsidiary_info` 子公司、`dwd_forg_stock_fin_info` 海外上市财务 |
| 企业工商通用 | 量子专题要素库 | 20 | `dwd_company_base` 基础信息、`dwd_company_shareholder` 股东、`dwd_company_*_tags` 各类标签、`dwd_industry_code` 产业链编码 |
| 产业链 | 产业链要素库 | 5 | `dwd_industry_chain_info` 产业链图谱、`dwd_org_industry_chain_dtl` 产业关联企业、`dwd_org_industry_chain_prod_dtl` 关联产品、`dwd_org_industry_chain_pat_dtl` 关联专利 |

**核心企业主数据来源（双源并存，需做实体归一）**：

| 来源 | 企业主键 | 关联键 | 特点 |
|------|---------|--------|------|
| `dwd_org_reg_info`（国内机构） | `org_id` | `external_id`（统一社会信用代码） | 字段规范、含经纬度/上市状态，机构口径 |
| `dwd_company_base`（量子专题通用工商） | `id` | `credit_code`（统一信用代码） | 通用工商口径，含实缴资本/企业类型细分 |

> 建议以**统一社会信用代码**（`external_id` / `credit_code`）作为企业实体归一主键，将两套源数据 merge 后加载 `dwd.enterprise`。

## 3. DWD 企业标准表概览

| # | DWD 表 | 字段数 | 说明 | 主要 ODS 来源（v2） |
|---|--------|--------|------|---------------------|
| 1 | enterprise | 65 | 企业主表 | `dwd_org_reg_info`、`dwd_company_base`、`dwd_org_org_product_info`、`dwd_org_annual_financial_info`、`dwd_org_stock_base/finance_info`、`dwd_org_rd_achiev_info`、`dwd_company_*_tags`、`dwd_org_tag_info` |
| 2 | enterprise_finance_history | 13 | 企业财务历史 | `dwd_org_annual_financial_info`、`dwd_org_stock_finance_info` |
| 3 | enterprise_patent_history | 9 | 企业专利历史 | `dwd_org_rd_achiev_info`、`dwd_patent`、`dwd_patent_legal`、`dwd_patent_cited`、`dwd_org_industry_chain_pat_dtl` |
| 4 | enterprise_parent_subsidiary | 8 | 母子公司关系 | `dwd_org_shareholder_info`、`dwd_org_invest_info`、`dwd_company_shareholder`、`dwd_company_branch` |
| 5 | enterprise_supply_chain | 9 | 供应链关系 | `dwd_industry_chain_info`、`dwd_org_industry_chain_dtl` |
| 6 | enterprise_industry | 8 | 产业链归属 | `dwd_org_industry_chain_dtl`、`dwd_industry_chain_info`、`dwd_company_industry_tags` |
| 7 | enterprise_cooperation | 10 | 合作关系 | `dwd_org_industry_chain_pat_dtl`、`dwd_zh_paper/dwd_en_paper`、`dwd_rel_project_*` |
| 8 | enterprise_business_tag | 7 | 业务标签 | `dwd_org_tag_info`、`dwd_company_basic_tags/diy_tags/honor_tags/industry_tags` |

## 4. 映射覆盖率总览

| DWD 表 | 总字段 | ✅直接 | 🔧需计算 | ⚠️待确认 | ❌无来源 | 🟦系统/预留 | 覆盖率* |
|--------|--------|--------|---------|---------|---------|------------|--------|
| enterprise | 65 | 30 | 24 | 3 | 3 | 5 | 90.0% |
| enterprise_finance_history | 13 | 5 | 3 | 2 | 0 | 3 | 80.0% |
| enterprise_patent_history | 9 | 5 | 1 | 0 | 0 | 3 | 100.0% |
| enterprise_parent_subsidiary | 8 | 4 | 1 | 0 | 0 | 3 | 100.0% |
| enterprise_supply_chain | 9 | 2 | 4 | 0 | 0 | 3 | 100.0% |
| enterprise_industry | 8 | 4 | 1 | 0 | 0 | 3 | 100.0% |
| enterprise_cooperation | 10 | 1 | 6 | 0 | 0 | 3 | 100.0% |
| enterprise_business_tag | 7 | 2 | 2 | 0 | 0 | 3 | 100.0% |
| **合计** | **129** | **53** | **42** | **5** | **3** | **26** | **92.2%** |

> *覆盖率 = (✅直接 + 🔧需计算) / (总字段 − 系统/预留)。
> 相比 v1（覆盖率 76.2%、直接映射率 40%），v2 覆盖率提升至 **92.2%**、直接映射率提升至 **51.5%**，主要得益于要素库新增的经纬度、上市信息、专利预聚合、研发投入、企业资质标签、产业链环节等数据。

## 5. 逐表字段映射详情

### 5.1 dwd.enterprise（企业主表，65 字段）

**ODS 来源**: `dwd_org_reg_info`、`dwd_company_base`、`dwd_org_org_product_info`、`dwd_company_nei_code`、`dwd_org_annual_financial_info`、`dwd_org_stock_base`、`dwd_org_stock_finance_info`、`dwd_org_rd_achiev_info`、`dwd_org_tag_info`、`dwd_company_*_tags`、`dwd_company_location_tags`

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增主键 |
| 2 | enterprise_code | varchar(64) | ✅直接 | `dwd_org_reg_info.external_id` / `dwd_company_base.credit_code` | 统一社会信用代码，作实体归一主键 |
| 3 | enterprise_name | varchar(255) | ✅直接 | `dwd_org_reg_info.name_cn` / `dwd_company_base.name` | 直接取值 |
| 4 | enterprise_name_short | varchar(100) | ⚠️待确认 | - | 要素库无简称字段，需从全称 NLP 抽取/截取 |
| 5 | enterprise_name_en | varchar(255) | ✅直接 | `dwd_company_base.english_name` / `dwd_org_hels_info.org_name_en` | **v2 新增可得**（v1 待确认） |
| 6 | legal_representative | varchar(100) | ✅直接 | `dwd_org_reg_info.lerep` / `dwd_company_base.legal_representative` | 法定代表人 |
| 7 | registered_capital | numeric | ✅直接 | `dwd_org_reg_info.registered_capital_value`(本币元，需 /10000 转万元) / `dwd_company_base.reg_capital_std` | 注意单位换算 |
| 8 | paid_in_capital | numeric | ✅直接 | `dwd_company_base.real_capital_std` | **v2 新增可得**（实缴资本，v1 待确认） |
| 9 | registration_date | date | ✅直接 | `dwd_org_reg_info.incorporation_date` / `dwd_company_base.establish_date` | 成立日期 |
| 10 | business_status | varchar(20) | ✅直接 | `dwd_company_base.status_std` / `dwd_org_reg_info`（经营期限推断） | 经营状态/枚举映射 |
| 11 | enterprise_type | varchar(50) | ✅直接 | `dwd_company_base.first_type/second_type/detail_type` | 企业类型（三级细分） |
| 12 | industry_category | varchar(100) | ✅直接 | `dwd_org_org_product_info.industry_class` / `dwd_company_nei_code.industry_l1_name` | 所属行业名称 |
| 13 | industry_code | varchar(20) | ✅直接 | `dwd_company_nei_code.industry_l1_code`（及 l2~l4） | 行业代码 |
| 14 | business_scope | text | ✅直接 | `dwd_org_org_product_info.main_activities` / `dwd_company_base.scope` | 经营范围 |
| 15 | registered_address | varchar(500) | ✅直接 | `dwd_org_reg_info.address` / `dwd_company_base.registered_add` | 注册地址 |
| 16 | headquarters_city | varchar(100) | ✅直接 | `dwd_org_reg_info.city` / `dwd_company_base.ori_reg_city` / `dwd_company_location_tags.reg_city` | 总部城市 |
| 17 | headquarters_district | varchar(100) | ✅直接 | `dwd_company_base.ori_reg_district` / `dwd_company_location_tags.reg_district` | 总部区县 |
| 18 | headquarters_address | varchar(500) | ✅直接 | 同 `registered_address` | DWD 设计中总部地址=注册地址 |
| 19 | headquarters_lng | numeric | ✅直接 | `dwd_org_reg_info.addr_lng` / `dwd_company_location_tags.reg_xy` | **v2 新增直接可得**（v1 需调地理编码 API） |
| 20 | headquarters_lat | numeric | ✅直接 | `dwd_org_reg_info.addr_lat` / `dwd_company_location_tags.reg_xy` | **v2 新增直接可得** |
| 21 | is_listed | smallint | 🔧需计算 | `dwd_org_reg_info.listing_status` / 存在 `dwd_org_stock_base` 记录则=1 | 规则判定 |
| 22 | listed_market | varchar(50) | ✅直接 | `dwd_org_stock_base.stock_type` | **v2 新增可得**（上市板块，v1 无来源） |
| 23 | listed_code | varchar(20) | ✅直接 | `dwd_org_stock_base.stock_code` | **v2 新增可得**（股票代码，v1 无来源） |
| 24 | is_foreign | smallint | 🔧需计算 | `dwd_company_base.first_type`（判断含"外资"）/ 关联 `dwd_forg_base_info` | 规则判定 |
| 25 | is_high_tech | smallint | 🔧需计算 | `dwd_org_tag_info.org_tag` / `dwd_company_honor_tags.national_tag`（解析"高新技术企业"标签） | **v2 由资质标签解析**（v1 无来源） |
| 26 | is_sme | smallint | 🔧需计算 | `dwd_company_basic_tags.scale_tag`（企业规模标签）/ 年报人数+营收规则 | 规则判定 |
| 27 | is_little_giant | smallint | 🔧需计算 | `dwd_org_tag_info` / `dwd_company_honor_tags`（解析"专精特新"标签） | **v2 由资质标签解析**（v1 无来源） |
| 28 | little_giant_level | varchar(20) | 🔧需计算 | `dwd_company_honor_tags.national_tag/province_tag`（解析级别） | 标签解析 |
| 29 | is_gazelle | smallint | 🔧需计算 | `dwd_org_tag_info` / `dwd_company_honor_tags`（解析"瞪羚"标签） | **v2 由资质标签解析** |
| 30 | is_unicorn | smallint | 🔧需计算 | `dwd_org_tag_info` / `dwd_company_honor_tags`（解析"独角兽"标签） | **v2 由资质标签解析** |
| 31 | revenue_latest | numeric | ✅直接 | `dwd_org_annual_financial_info.operating_revenue`(取最新 year) / `dwd_org_stock_finance_info.operating_revenue` | 最新年营收 |
| 32 | revenue_year | integer | ✅直接 | `dwd_org_annual_financial_info.year` | 营收对应年份 |
| 33 | revenue_growth_rate | numeric | 🔧需计算 | `dwd_org_annual_financial_info`（相邻年） | (本年−上年)/上年×100 |
| 34 | net_profit | numeric | ✅直接 | `dwd_org_annual_financial_info.pure_profit` / `dwd_org_stock_finance_info.pure_profit` | 净利润 |
| 35 | profit_margin | numeric | 🔧需计算 | 净利润/营收×100 | 字段间计算 |
| 36 | gross_margin | numeric | ⚠️待确认 | `dwd_org_annual_financial_info`（无毛利明细） | 年报缺毛利数据，需采购或置空 |
| 37 | market_share | numeric | ❌无来源 | - | 需市场调研数据 |
| 38 | brand_score | numeric | ❌无来源 | - | 可基于 `dwd_org_important_news_info` 资讯声量做算法，否则无来源 |
| 39 | customer_concentration | numeric | ❌无来源 | - | 需企业客户明细 |
| 40 | patent_apply_count | integer | ✅直接 | `dwd_org_industry_chain_pat_dtl` / `dwd_patent` 按企业聚合 COUNT | 累计专利申请数 |
| 41 | patent_grant_count | integer | ✅直接 | `dwd_org_rd_achiev_info`(inv_pat_auth_num+util_pat_auth_num+des_pat_auth_num 已预聚合) | **v2 预聚合直接可得** |
| 42 | patent_valid_count | integer | 🔧需计算 | `dwd_patent_legal`（按法律状态计算有效专利） | 需法律状态+日期逻辑 |
| 43 | patent_invention_count | integer | ✅直接 | `dwd_org_rd_achiev_info.inv_pat_auth_num` | **v2 新增直接可得**（发明专利授权数） |
| 44 | patent_citation_count | integer | ✅直接 | `dwd_patent_cited` 按企业聚合 | **v2 新增可得**（专利引用，v1 无来源） |
| 45 | rd_staff_count | integer | ⚠️待确认 | `dwd_org_annual_financial_info.employees_number`(从业人数，非研发人数) | 缺研发人数口径，需确认 |
| 46 | rd_staff_ratio | numeric | 🔧需计算 | rd_staff_count / 总员工数 | 依赖研发人数 |
| 47 | rd_investment | numeric | ✅直接 | `dwd_org_stock_finance_info.research_development_amount` | **v2 上市企业可得**（非上市仍缺，v1 待确认） |
| 48 | rd_investment_ratio | numeric | 🔧需计算 | rd_investment / revenue×100 | 字段间计算 |
| 49 | core_tech_coverage | numeric | 🔧算法 | 多表综合（专利+论文+技术领域） | 算法模型 |
| 50 | tech_score | numeric | 🔧算法 | 多表综合 | 技术力加权评分模型 |
| 51 | business_score | numeric | 🔧算法 | 多表综合 | 商业力加权评分模型 |
| 52 | competitiveness_score | numeric | 🔧算法 | tech_score×W1+business_score×W2 | 综合竞争力评分 |
| 53 | innovation_index | numeric | 🔧算法 | 多表综合 | 创新活力指数 |
| 54 | introduction_value | varchar(20) | 🔧算法 | competitiveness_score→等级 | 规则引擎 A/B/C/D |
| 55 | cultivation_priority | varchar(20) | 🔧算法 | 多维度综合 | 规则引擎 |
| 56 | risk_level | varchar(20) | 🔧算法 | 经营异常/行政处罚/严重违法/税收违法/失信/被执行/限高/裁判文书/股权冻结质押/破产 等风险表综合 | **v2 风险源极丰富**，可做规则评分 |
| 57 | data_source | varchar(100) | ✅直接 | 各表 `data_source` 字段 | 标记数据源 |
| 58 | data_source_url | varchar(500) | 🔧需计算 | `dwd_org_important_news_info.original_textlink` 等 / ETL 记录 | 部分可得 |
| 59 | data_collect_time | timestamp | ✅直接 | 各表 `created_time` | ODS 入库时间 |
| 60 | data_update_time | timestamp | 🟦系统 | - | ETL 执行时间 |
| 61 | data_completeness | numeric | 🔧需计算 | 本行字段 | 非空字段数/总字段数 |
| 62 | data_confidence | numeric | 🔧需计算 | 多源一致性 | 数据置信度评分 |
| 63 | audit_status | varchar(20) | 🟦系统 | - | 默认"待审核" |
| 64 | create_time | timestamp | 🟦系统 | - | ETL 写入时间 |
| 65 | update_time | timestamp | 🟦系统 | - | ETL 更新时间 |

### 5.2 dwd.enterprise_finance_history（企业财务历史，13 字段）

**ODS 来源**: `dwd_org_annual_financial_info`（年报财务，逐年）、`dwd_org_stock_finance_info`（上市财务，逐期）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增 |
| 2 | enterprise_id | bigint | ✅直接 | 经 `external_id` 关联 `dwd.enterprise.id` | 外键关联 |
| 3 | data_year | integer | ✅直接 | `dwd_org_annual_financial_info.year` / `dwd_org_stock_finance_info.occur_period` | 数据年份 |
| 4 | revenue | numeric | ✅直接 | `dwd_org_annual_financial_info.operating_revenue` | 营收（注意源为字符串，需转 numeric） |
| 5 | revenue_growth_rate | numeric | 🔧需计算 | 相邻年营收 | (本年−上年)/上年×100 |
| 6 | net_profit | numeric | ✅直接 | `dwd_org_annual_financial_info.pure_profit` | 净利润 |
| 7 | profit_margin | numeric | 🔧需计算 | net_profit/revenue×100 | 字段间计算 |
| 8 | gross_margin | numeric | ⚠️待确认 | 年报无毛利明细 | 需采购或置空 |
| 9 | rd_investment | numeric | ✅直接 | `dwd_org_stock_finance_info.research_development_amount` | **v2 上市企业可得**，非上市缺 |
| 10 | rd_investment_ratio | numeric | 🔧需计算 | rd_investment/revenue×100 | 依赖 rd_investment |
| 11 | rd_staff_count | integer | ⚠️待确认 | `employees_number`（从业人数，非研发人数） | 口径需确认 |
| 12 | create_time | timestamp | 🟦系统 | - | ETL 写入 |
| 13 | update_time | timestamp | 🟦系统 | - | ETL 更新 |

### 5.3 dwd.enterprise_patent_history（企业专利历史，9 字段）

**ODS 来源**: `dwd_patent`（专利信息表，76 字段）、`dwd_patent_legal`（法律状态）、`dwd_patent_cited`（引用关系）、`dwd_org_industry_chain_pat_dtl`（产业链关联专利）、`dwd_org_rd_achiev_info`（研发成果累计统计）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增 |
| 2 | enterprise_id | bigint | ✅直接 | 经 `external_id`/申请人关联 | 外键关联，需专利申请人→企业归一 |
| 3 | data_year | integer | ✅直接 | `dwd_patent`(申请年) / `dwd_org_industry_chain_pat_dtl.apdt` 提取年 | 从申请日提取 |
| 4 | patent_apply_count | integer | ✅直接 | `dwd_patent` / `dwd_org_industry_chain_pat_dtl` 按年 COUNT | 按年聚合 |
| 5 | patent_grant_count | integer | ✅直接 | `dwd_patent_legal`(状态=授权) 按年聚合 | 按年+状态聚合 |
| 6 | patent_valid_count | integer | 🔧需计算 | `dwd_patent_legal` | 有效期内专利计算 |
| 7 | patent_citation_count | integer | ✅直接 | `dwd_patent_cited` 按企业+年聚合 | **v2 新增可得**（v1 无来源） |
| 8 | create_time | timestamp | 🟦系统 | - | ETL 写入 |
| 9 | update_time | timestamp | 🟦系统 | - | ETL 更新 |

> 说明：`dwd_org_rd_achiev_info` 提供的是**累计授权数**（非按年），可用于 `dwd.enterprise` 汇总字段；按年明细需从 `dwd_patent` 系列表聚合。

### 5.4 dwd.enterprise_parent_subsidiary（母子公司关系，8 字段）

**ODS 来源**: `dwd_org_shareholder_info`（股东）、`dwd_org_invest_info`（对外投资）、`dwd_company_shareholder`、`dwd_company_branch`（分支机构）、`dwd_forg_shareholder_info/subsidiary_info`（海外）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增 |
| 2 | enterprise_id | bigint | ✅直接 | 经 `org_id`/`external_id` 关联 | 外键关联 |
| 3 | parent_enterprise_id | bigint | ✅直接 | `dwd_org_shareholder_info.inv_org_id` / `dwd_company_shareholder.investor_id` | 股东为法人时关联其企业 |
| 4 | parent_enterprise_name | varchar(255) | ✅直接 | `dwd_org_shareholder_info.owners_name` / `dwd_company_shareholder.investor_name` | 股东名称 |
| 5 | ownership_ratio | numeric | ✅直接 | `dwd_org_shareholder_info.ownership_percentage` / `dwd_company_shareholder.share_ratio` | 持股比例 |
| 6 | subsidiary_count | integer | 🔧需计算 | `dwd_org_invest_info` / `dwd_company_branch` 按企业 COUNT | 对外投资/分支机构计数 |
| 7 | create_time | timestamp | 🟦系统 | - | ETL 写入 |
| 8 | update_time | timestamp | 🟦系统 | - | ETL 更新 |

### 5.5 dwd.enterprise_supply_chain（供应链关系，9 字段）

**ODS 来源**: `dwd_industry_chain_info`（产业链图谱，含上中下游环节）、`dwd_org_industry_chain_dtl`（产业关联企业，含产业链评分）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增 |
| 2 | enterprise_id | bigint | ✅直接 | `dwd_org_industry_chain_dtl.antitypic/credit_code` 关联 | 外键关联 |
| 3 | related_enterprise_id | bigint | 🔧需计算 | `dwd_org_industry_chain_dtl` 同链上下游节点企业 | 经 `dwd_industry_chain_info.downstream_link_code` 推导上下游企业对 |
| 4 | relation_type | varchar(50) | ✅直接 | `dwd_industry_chain_info.node_stage`(1上游/2中游/3下游) | **v2 新增可得**（上下游环节） |
| 5 | relation_strength | numeric | 🔧需计算 | `dwd_org_industry_chain_dtl.chain_score` 作基础 | 结合共现频次算法 |
| 6 | is_core_supplier | smallint | 🔧需计算 | chain_score 阈值判定 | 规则判定 |
| 7 | risk_level | varchar(20) | 🔧算法 | 供应链网络+风险表综合 | 断链风险评估算法 |
| 8 | create_time | timestamp | 🟦系统 | - | ETL 写入 |
| 9 | update_time | timestamp | 🟦系统 | - | ETL 更新 |

### 5.6 dwd.enterprise_industry（产业链归属，8 字段）

**ODS 来源**: `dwd_org_industry_chain_dtl`（产业关联企业）、`dwd_industry_chain_info`（产业链图谱）、`dwd_company_industry_tags`（产业标签）、`dwd_industry_code`（产业链编码）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增 |
| 2 | enterprise_id | bigint | ✅直接 | `dwd_org_industry_chain_dtl.credit_code` 关联 | 外键关联 |
| 3 | industry_chain | varchar(100) | ✅直接 | `dwd_org_industry_chain_dtl.chain_name` / `dwd_industry_chain_info.chain_name` | 产业链名称 |
| 4 | industry_chain_node | varchar(100) | ✅直接 | `dwd_org_industry_chain_dtl.node_name` | **v2 直接可得**（v1 间接） |
| 5 | industry_chain_role | varchar(50) | ✅直接 | `dwd_industry_chain_info.node_stage`(上游/中游/下游) | **v2 直接可得**（v1 待确认） |
| 6 | participation_depth | numeric | 🔧需计算 | `dwd_org_industry_chain_dtl.chain_score` 作基础 | 结合产品/专利贡献度算法 |
| 7 | create_time | timestamp | 🟦系统 | - | ETL 写入 |
| 8 | update_time | timestamp | 🟦系统 | - | ETL 更新 |

> 补充：`dwd_company_industry_tags.industry_tag` 内含「产业编码/名称/置信度/环节」结构化标签，可作为产业链归属的二级来源；`dwd_org_industry_chain_prod_dtl` 提供企业主营产品，可辅助参与度评估。

### 5.7 dwd.enterprise_cooperation（合作关系，10 字段）

**ODS 来源**: `dwd_org_industry_chain_pat_dtl`（含联合申请人/发明人）、`dwd_zh_paper/dwd_en_paper`（论文合著）、`dwd_rel_project_scholar/paper/patent`（项目关联）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增 |
| 2 | enterprise_id | bigint | ✅直接 | 经申请人/署名机构关联 | 外键关联 |
| 3 | partner_type | varchar(50) | 🔧需推导 | 从合作来源推断（企业/高校/科研机构） | 实体类型识别 |
| 4 | partner_id | bigint | 🔧需推导 | 实体识别后关联 | NER+实体链接 |
| 5 | partner_name | varchar(255) | 🔧需推导 | `dwd_org_industry_chain_pat_dtl.current_assignee`(多申请人) / 论文合著机构 | 抽取联合方 |
| 6 | cooperation_type | varchar(50) | 🔧需推导 | 按来源分类（联合专利/论文/项目） | 规则判定 |
| 7 | project_count | integer | 🔧需计算 | `dwd_rel_project_*` 联合项目计数 | 依赖实体识别 |
| 8 | patent_count | integer | 🔧需计算 | `dwd_org_industry_chain_pat_dtl` 联合专利计数 | 解析多申请人 |
| 9 | create_time | timestamp | 🟦系统 | - | ETL 写入 |
| 10 | update_time | timestamp | 🟦系统 | - | ETL 更新 |

### 5.8 dwd.enterprise_business_tag（业务标签，7 字段）

**ODS 来源**: `dwd_org_tag_info`（机构标签）、`dwd_company_basic_tags`（基础属性）、`dwd_company_diy_tags`（特色资质）、`dwd_company_honor_tags`（荣誉标签）、`dwd_company_industry_tags`（产业标签）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增 |
| 2 | enterprise_id | bigint | ✅直接 | 经 `id`/`external_id` 关联 | 外键关联 |
| 3 | tag_type | varchar(50) | 🔧需计算 | 按来源表分类（基础属性/资质/荣誉/产业） | 结构化标签拆解归类 |
| 4 | tag_name | varchar(100) | ✅直接 | `dwd_org_tag_info.org_tag` / `dwd_company_diy_tags.diy_tag` / `dwd_company_honor_tags.*` | **v2 直接可得**（v1 需 NLP 生成） |
| 5 | tag_score | numeric | 🔧需计算 | `dwd_company_honor_tags`/`industry_tags` 内置置信度 / 算法 | 标签关联度评分 |
| 6 | create_time | timestamp | 🟦系统 | - | ETL 写入 |
| 7 | update_time | timestamp | 🟦系统 | - | ETL 更新 |

## 6. v1 → v2 关键改善对照

| DWD 字段 | v1 状态 | v2 状态 | 改善原因（要素库新增） |
|----------|---------|---------|------------------------|
| enterprise.headquarters_lng/lat | 🔧 地理编码 | ✅ 直接 | `dwd_org_reg_info.addr_lng/addr_lat`、`dwd_company_location_tags.reg_xy` |
| enterprise.listed_market/listed_code | ❌ 无来源 | ✅ 直接 | `dwd_org_stock_base.stock_type/stock_code` |
| enterprise.enterprise_name_en | ⚠️ 待确认 | ✅ 直接 | `dwd_company_base.english_name` |
| enterprise.paid_in_capital | ⚠️ 待确认 | ✅ 直接 | `dwd_company_base.real_capital_std` |
| enterprise.patent_grant/invention_count | 🔧 条件聚合 | ✅ 预聚合 | `dwd_org_rd_achiev_info`（已按企业汇总授权/发明数） |
| enterprise.patent_citation_count | ❌ 无来源 | ✅ 直接 | `dwd_patent_cited` 专利引用关系表 |
| enterprise.rd_investment | ⚠️ 待确认 | ✅（上市） | `dwd_org_stock_finance_info.research_development_amount` |
| enterprise.is_high_tech/little_giant/gazelle/unicorn | ❌ 无来源 | 🔧 标签解析 | `dwd_org_tag_info`、`dwd_company_honor_tags` 资质/荣誉标签 |
| enterprise_industry.industry_chain_node/role | ⚠️ 待确认 | ✅ 直接 | `dwd_org_industry_chain_dtl.node_name`、`dwd_industry_chain_info.node_stage` |
| enterprise_business_tag.tag_name | 🔧 NLP生成 | ✅ 直接 | 结构化标签表（`dwd_*_tags`） |
| enterprise.risk_level | 🔧 风险模型(数据缺) | 🔧 风险模型(数据足) | 新增 20+ 张风险/司法表（处罚/失信/被执行/裁判文书等） |

## 7. 数据缺口与风险

### 7.1 仍无来源的字段（需额外采购或暂置空）

| DWD 表 | 字段 | 说明 | 建议 |
|--------|------|------|------|
| enterprise | market_share | 市场份额 | 采购行业研究/市调数据 |
| enterprise | brand_score | 品牌声量评分 | 可基于 `dwd_org_important_news_info` 资讯做算法，或采购品牌评估 |
| enterprise | customer_concentration | 客户集中度 | 需企业客户明细，暂缺 |

### 7.2 待确认/质量待验字段

| DWD 表 | 字段 | 问题 | 处理建议 |
|--------|------|------|----------|
| enterprise | enterprise_name_short | 无简称字段 | NLP 抽取或从全称规则截取 |
| enterprise / finance | gross_margin | 年报无毛利明细 | 上市财务可推算（营收−营业成本），非上市置空 |
| enterprise / finance | rd_staff_count | `employees_number` 为从业人数，非研发人数 | 与供方确认是否有研发人数字段 |

### 7.3 实体归一风险（v2 新增重点）

- 企业主数据存在**双源**（`dwd_org_reg_info` 机构口径 vs `dwd_company_base` 工商口径），需以统一社会信用代码做去重合并，避免 `dwd.enterprise` 出现重复主体。
- 专利/论文/项目中的企业以名称或申请人字符串出现，需做**机构名→统一社会信用代码**的标准化映射后，才能关联到 `dwd.enterprise`。
- 国内（`dwd_org_*`/`dwd_company_*`）与国外（`dwd_forg_*`）机构主键体系不同，跨境母子公司关系需单独处理。

## 8. ETL 实施建议

```
Phase 1（直接映射加载，1-2周）
├── dwd.enterprise: 工商基本(双源合并去重)+经纬度+上市信息+英文名+实缴资本  约 30 字段
├── dwd.enterprise_finance_history: 年报/上市财务逐年加载
├── dwd.enterprise_patent_history: 专利申请/授权/引用按年聚合
├── dwd.enterprise_parent_subsidiary: 股东/投资/分支关系
├── dwd.enterprise_industry: 产业链归属(含节点/上中下游)
└── dwd.enterprise_business_tag: 结构化标签拆解加载

Phase 2（计算型字段，2-3周）
├── 增长率/利润率/研发投入占比 数值计算
├── is_listed/is_foreign/is_sme 规则判定
├── is_high_tech/little_giant/gazelle/unicorn 资质标签解析
├── 专利有效数(法律状态) 条件聚合
└── 供应链上下游企业对 + relation_strength(chain_score)

Phase 3（算法模型，3-4周）
├── tech/business/competitiveness/innovation 评分模型
├── risk_level 风险评分(利用丰富风险表)
├── 合作关系实体识别(联合专利/论文)
└── 产业链参与度/标签置信度评分

Phase 4（数据补充采购）
└── 市场份额/品牌/客户集中度/毛利/研发人数 等剩余缺口
```

**示例 ETL（enterprise 主表，双源合并）**：

```sql
-- 以统一社会信用代码为归一键，机构口径为主、工商口径补全
INSERT INTO dwd.enterprise (
  enterprise_code, enterprise_name, enterprise_name_en, legal_representative,
  registered_capital, paid_in_capital, registration_date, business_status,
  enterprise_type, registered_address, headquarters_city, headquarters_district,
  headquarters_lng, headquarters_lat, data_source
)
SELECT
  COALESCE(o.external_id, c.credit_code)                     AS enterprise_code,
  COALESCE(o.name_cn, c.name)                                AS enterprise_name,
  c.english_name                                             AS enterprise_name_en,
  COALESCE(o.lerep, c.legal_representative)                  AS legal_representative,
  COALESCE(o.registered_capital_value/10000, c.reg_capital_std) AS registered_capital,
  c.real_capital_std                                         AS paid_in_capital,
  COALESCE(o.incorporation_date, CAST(c.establish_date AS date)) AS registration_date,
  c.status_std                                               AS business_status,
  c.first_type                                               AS enterprise_type,
  COALESCE(o.address, c.registered_add)                      AS registered_address,
  COALESCE(o.city, c.ori_reg_city)                           AS headquarters_city,
  c.ori_reg_district                                         AS headquarters_district,
  CAST(o.addr_lng AS numeric)                                AS headquarters_lng,
  CAST(o.addr_lat AS numeric)                                AS headquarters_lat,
  o.data_source
FROM ods.dwd_org_reg_info o
FULL JOIN ods.dwd_company_base c
       ON o.external_id = c.credit_code;
```

## 9. 综合结论

| 评估维度 | v1 满足度 | v2 满足度 | 说明 |
|----------|-----------|-----------|------|
| 企业工商基础信息 | 100% | 100% | 双源，字段更细（企业类型三级、实缴资本） |
| 企业地理位置 | 50%(需地理编码) | 100% | 经纬度直接提供 |
| 企业上市信息 | 0% | 90% | 板块/代码/上市财务齐全 |
| 企业财务数据 | 70% | 85% | 新增上市财务+研发投入，缺毛利/非上市研发投入 |
| 企业专利数据 | 80% | 100% | 预聚合统计+引用关系齐全 |
| 企业股权/投资关系 | 90% | 100% | 国内外股东/投资/子公司齐全 |
| 企业产业链归属 | 60% | 100% | 节点/上中下游/评分齐全 |
| 企业供应链关系 | 50% | 85% | 产业链图谱完整，关系强度需算法 |
| 企业资质标签 | 0% | 70% | 由资质/荣誉标签解析（高新/专精特新等） |
| 企业评分/合作关系 | 10-20% | 20%(算法) | 仍依赖算法模型，但底层数据更充分 |

**关键结论**：

1. **覆盖率大幅提升**：企业相关 DWD 字段覆盖率由 v1 的 76.2% 提升至 **92.2%**，直接映射率由 40% 提升至 **51.5%**。
2. **多项 v1 缺口被填补**：经纬度、上市信息、专利引用、研发投入、企业英文名、实缴资本、产业链环节、企业资质标签等，由要素库直接或半直接提供。
3. **核心待办从"缺数据"转为"做加工"**：剩余字段集中在评分类（tech/business/competitiveness）、合作关系推导、风险评级等**算法层**，底层数据已基本就绪。
4. **新增重点风险=实体归一**：双源企业主数据 + 专利/论文机构名标准化，是 v2 ETL 的首要工程难点。
5. **仍需采购的少量字段**：市场份额、品牌评分、客户集中度、毛利明细、研发人数。

---

*报告生成时间: 2026-06-02 ｜ ODS 数据源: db/要素库建表语句.sql（企业相关 74 张表）｜ DWD 目标: dwd 企业相关 8 张标准表*
