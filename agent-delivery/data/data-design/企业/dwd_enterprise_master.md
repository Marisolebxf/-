# DWD 表设计契约 — 企业主表（dwd_enterprise_master）

> **用途**：项目自研 DWD 企业主表的设计真源。架构师按业务需求填此契约；**不与甲方 ODS（供应库 `dwd_*`）一一对应**。
> **阶段**：Phase 1（现在 ~ 2026-08-20，ODS 未稳定）— 只治理项目 DWD 设计；Phase 2（8/20 后）由 GDF 对照本契约的 `ods_mapping_expectation` 做映射。
> **权威规约**：`agent-delivery/data-lineage-policy.md` §2.2
> **连接真源**（只读 ODS）：`agent-delivery/data/third-party-source/gkx-mysql-raw/CONNECTION.md`（密码禁止写入本文件）
> **维护**：lineage-subcoord（Phase 1）主导；architect-agent 审设计；data-agent 建表时遵循。
> **任务来源**：ENT-LINEAGE-DWD-CONTRACT-L01

---

## 表头元数据

```yaml
table: dwd_enterprise_master       # 项目自研 DWD 表名（勿照抄供应库表名）
layer: DWD
element: ENT
design_owner: architect
design_phase: phase1
ods_dependency: none               # Phase 1 固定 none；Phase 2 映射完成后可改为 mapped
related_metrics:
  - M_ENT_SZ_COUNT
  - M_ENT_SZ_CHAIN_POSITION
  - M_ENT_KEY_NODE_COUNT
  - M_ENT_CITY_AVG_TECH_POWER
  - M_ENT_CITY_DENSITY
  - M_ENT_CHAIN_COMPLETENESS
  - M_ENT_TECH_POWER_SCORE
  - M_ENT_BUSINESS_POWER_SCORE
  - M_ENT_COMPETITIVENESS_SCORE
  - M_ENT_COMPETITIVENESS_RANK
  - M_ENT_TOTAL_COUNT
  - M_ENT_INNOVATIVE_COUNT
  - M_ENT_PATENT_TOTAL
bid_refs:
  - "§1.1.1.2.4.2.1"          # 企业搜索
  - "§1.1.1.2.4.2.2"          # 企业评估
  - "§1.1.1.2.4.2.3"          # 风险洞察
  - "§1.1.1.2.4.2.4"          # 引育推荐
  - "§1.1.1.2.4.2.3.5"        # 深圳企业现状分析
acceptance_units: [E-20, E-23, E-24, E-25, E-30, E-35]
status: draft                      # draft | review | approved
updated: "2026-08-10"
```

### 业务说明

| 项 | 内容 |
|----|------|
| 中文表名 | 企业主表（双源归一） |
| 一句话用途 | 支撑企业搜索(E-20)、企业评估(E-23/E-24/E-30)、风险洞察(E-25)、引育推荐(E-35)、深圳企业现状分析(E-25)的企业级基础数据 |
| 粒度 | 一企业一行 |
| 主键 | `id`（BIGINT 自增代理键） |
| 业务键 | `enterprise_code`（统一社会信用代码；跨表/跨图谱稳定键） |
| 与供应库关系 | **非一一对应**。供应库 `dwd_*` = 本项目 ODS；本表为项目自研 DWD，由架构师按 SEARCH/EVAL/RISK/RECRUIT 需求设计字段集。双源归一：`dwd_org_reg_info`（机构口径）+ `dwd_company_base`（工商口径），以 `external_id = credit_code` 归一。 |

---

## 字段定义

> `confidence`：`high`=语义明确、易映射；`medium`=可能有命名差异；`low`=供应侧可能缺失（Phase 2 重点核对）
>
> 字段分 6 组：①主键与归一 ②基础信息 ③行业与地域 ④财务与研发 ⑤专利与知识产权 ⑥算法评分字段。覆盖 SEARCH/EVAL/RISK/RECRUIT 已用到的全部核心字段。

### ① 主键与归一字段

```yaml
fields:
  - name: id
    type: bigint
    nullable: false
    business_def: 代理主键，序列自增
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "供应侧主表代理键或可推导唯一键"
      confidence: high
      note: ""

  - name: enterprise_code
    type: varchar(64)
    nullable: false
    business_def: 业务主键（统一社会信用代码）；双源归一键 = COALESCE(dwd_org_reg_info.external_id, dwd_company_base.credit_code)
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_reg_info.external_id / dwd_company_base.credit_code"
      confidence: high
      note: "机构口径为主、工商口径补全（FULL JOIN ON external_id = credit_code）"

  - name: enterprise_name
    type: varchar(255)
    nullable: false
    business_def: 企业全称
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_reg_info.name_cn / dwd_company_base.name"
      confidence: high
      note: ""

  - name: enterprise_name_short
    type: varchar(100)
    nullable: true
    business_def: 企业简称（要素库无，需 NLP 抽取或截取）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "无直接来源；从 enterprise_name 提取或人工维护"
      confidence: low
      note: "Phase 2 需人工补录或 NLP 抽取"
```

### ② 基础信息字段

```yaml
  - name: legal_representative
    type: varchar(100)
    nullable: true
    business_def: 法定代表人
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_reg_info.lerep / dwd_company_base.legal_representative"
      confidence: high
      note: ""

  - name: registered_capital
    type: decimal(20,4)
    nullable: true
    business_def: 注册资本（万元）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_reg_info.registered_capital_value/10000 / dwd_company_base.reg_capital_std"
      confidence: high
      note: "SEARCH 用于企业规模分档；EVAL 用于数据质量检查"

  - name: registration_date
    type: date
    nullable: true
    business_def: 成立日期
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_reg_info.incorporation_date / dwd_company_base.establish_date"
      confidence: high
      note: ""

  - name: business_status
    type: varchar(20)
    nullable: true
    business_def: 经营状态（存续/注销/吊销等）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_company_base.status_std"
      confidence: high
      note: ""

  - name: enterprise_type
    type: varchar(50)
    nullable: true
    business_def: 企业类型（三级分类）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_company_base.first_type/second_type/detail_type"
      confidence: high
      note: "用于高企/专精特新/外资等分类判定（Q010）"

  - name: business_scope
    type: text
    nullable: true
    business_def: 经营范围
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_org_product_info.main_activities / dwd_company_base.scope"
      confidence: high
      note: ""
```

### ③ 行业与地域字段

```yaml
  - name: industry_category
    type: varchar(100)
    nullable: true
    business_def: 所属行业名称
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_org_product_info.industry_class / dwd_company_nei_code.industry_l1_name"
      confidence: high
      note: "SEARCH 筛选条件；EVAL 行业基准分组；RISK 产业链归属"

  - name: industry_code
    type: varchar(20)
    nullable: true
    business_def: 行业代码（国民经济行业分类）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_company_nei_code.industry_l1_code"
      confidence: high
      note: ""

  - name: headquarters_city
    type: varchar(100)
    nullable: true
    business_def: 总部城市
    metric_ref: M_ENT_SZ_COUNT
    ods_mapping_expectation:
      expected_from: "dwd_org_reg_info.city / dwd_company_location_tags.reg_city"
      confidence: high
      note: "SEARCH 城市筛选；SHENZHEN M_ENT_SZ_COUNT 过滤条件；EVAL/RISK/RECRUIT 企业画像"

  - name: headquarters_district
    type: varchar(100)
    nullable: true
    business_def: 总部区县
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_company_base.ori_reg_district / dwd_company_location_tags.reg_district"
      confidence: high
      note: ""

  - name: headquarters_province
    type: varchar(100)
    nullable: true
    business_def: 总部省份
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_reg_info.province / dwd_company_base.ori_reg_province"
      confidence: high
      note: ""

  - name: headquarters_lng
    type: decimal(12,7)
    nullable: true
    business_def: 经度
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_reg_info.addr_lng / dwd_company_location_tags.reg_xy"
      confidence: medium
      note: "可能需解析 reg_xy 字段（格式 lng,lat）"

  - name: headquarters_lat
    type: decimal(12,7)
    nullable: true
    business_def: 纬度
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_reg_info.addr_lat"
      confidence: medium
      note: "可能需解析 reg_xy 字段"
```
### ④ 财务与研发字段

```yaml
  - name: revenue_latest
    type: decimal(20,4)
    nullable: true
    business_def: 最新年营收（万元）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_annual_financial_info.operating_revenue（最新 year）"
      confidence: high
      note: "EVAL business_power 市场维度；RECRUIT attraction/cultivation 成长性输入"

  - name: revenue_year
    type: int
    nullable: true
    business_def: 营收对应年份
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_annual_financial_info.year"
      confidence: high
      note: ""

  - name: revenue_growth_rate
    type: decimal(10,4)
    nullable: true
    business_def: 营收增长率（%）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "相邻年 dwd_org_annual_financial_info.operating_revenue 计算"
      confidence: medium
      note: "需 ETL 计算派生；EVAL business_power 成长性输入；RECRUIT attraction/cultivation"

  - name: net_profit
    type: decimal(20,4)
    nullable: true
    business_def: 净利润（万元）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_annual_financial_info.pure_profit"
      confidence: high
      note: ""

  - name: profit_margin
    type: decimal(10,4)
    nullable: true
    business_def: 利润率（%）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "净利润/营收 计算"
      confidence: medium
      note: "需 ETL 计算派生"

  - name: gross_margin
    type: decimal(10,4)
    nullable: true
    business_def: 毛利率（%）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "年报缺毛利明细；上市企业可从 dwd_org_stock_finance_info 推算"
      confidence: low
      note: "非上市企业大概率无来源；EVAL business_power 市场维度输入"

  - name: rd_staff_count
    type: int
    nullable: true
    business_def: 研发人数
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_annual_financial_info.employees_number（为从业人数，口径待确认 Q019）"
      confidence: medium
      note: "EVAL tech_power 人才维度输入"

  - name: rd_staff_ratio
    type: decimal(10,4)
    nullable: true
    business_def: 研发人数占比
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "rd_staff_count / 总员工数 计算"
      confidence: low
      note: "需 ETL 计算派生；总员工数口径待确认"

  - name: rd_investment
    type: decimal(20,4)
    nullable: true
    business_def: 研发投入（万元）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_stock_finance_info.research_development_amount（上市可得）"
      confidence: medium
      note: "非上市企业大概率无来源；EVAL tech_power 投入维度输入"

  - name: rd_investment_ratio
    type: decimal(10,4)
    nullable: true
    business_def: 研发投入占比（%）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "rd_investment / revenue_latest 计算"
      confidence: low
      note: "需 ETL 计算派生"
```

### ⑤ 专利与知识产权字段

```yaml
  - name: patent_apply_count
    type: int
    nullable: true
    business_def: 累计专利申请数
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_industry_chain_pat_dtl / dwd_patent 聚合"
      confidence: high
      note: ""

  - name: patent_grant_count
    type: int
    nullable: true
    business_def: 累计专利授权数
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_rd_achiev_info(inv+util+des 预聚合)"
      confidence: high
      note: "EVAL tech_power 创新维度核心输入；SEARCH 排序权重；RECRUIT attraction 画像"

  - name: patent_valid_count
    type: int
    nullable: true
    business_def: 有效专利数
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_patent_legal 法律状态计算"
      confidence: medium
      note: "需 ETL 计算派生"

  - name: patent_invention_count
    type: int
    nullable: true
    business_def: 发明专利授权数
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_rd_achiev_info.inv_pat_auth_num"
      confidence: high
      note: "EVAL tech_power 创新维度加权输入"

  - name: patent_citation_count
    type: int
    nullable: true
    business_def: 专利被引数
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_patent_cited 聚合"
      confidence: high
      note: ""
```

### ⑥ 算法评分字段（🔧 待 algorithm-agent）

```yaml
  - name: tech_score
    type: decimal(10,4)
    nullable: true
    business_def: 技术力评分（算法模型 ENT_WEIGHTED_SCORE 五维加权）
    metric_ref: M_ENT_TECH_POWER_SCORE
    ods_mapping_expectation:
      expected_from: "算法侧产出（dwd_org_rd_achiev_info + dwd_org_annual_financial_info + dwd_org_tag_info 五维计算）"
      confidence: medium
      note: "Q014 权重未闭合；M_ENT_CITY_AVG_TECH_POWER 派生于本字段按 city AVG"

  - name: business_score
    type: decimal(10,4)
    nullable: true
    business_def: 商业力评分（算法模型 ENT_WEIGHTED_SCORE 六维加权）
    metric_ref: M_ENT_BUSINESS_POWER_SCORE
    ods_mapping_expectation:
      expected_from: "算法侧产出（revenue + market_share + gross_margin + brand_score + chain_coverage + chain_keynode 六维计算）"
      confidence: low
      note: "Q014 权重未闭合；market_share/brand_score 供应侧可能缺失"

  - name: competitiveness_score
    type: decimal(10,4)
    nullable: true
    business_def: 综合竞争力评分（tech_score * W1 + business_score * W2）
    metric_ref: M_ENT_COMPETITIVENESS_SCORE
    ods_mapping_expectation:
      expected_from: "算法侧产出（派生自 tech_score + business_score）"
      confidence: medium
      note: "Q014 权重未闭合"

  - name: risk_level
    type: varchar(20)
    nullable: true
    business_def: 风险等级（经营异常/处罚/失信/被执行等综合判定）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_risk_* (20+张风险表) 综合计算"
      confidence: low
      note: "RISK 模块核心字段；供应侧风险表结构待 Phase 2 核对"

  - name: is_high_tech
    type: tinyint
    nullable: true
    business_def: 是否高新技术企业
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_org_tag_info.org_tag / dwd_company_honor_tags.national_tag 解析"
      confidence: medium
      note: "Q010 口径待确认；需标签解析规则"

  - name: is_little_giant
    type: tinyint
    nullable: true
    business_def: 是否专精特新
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_company_honor_tags 解析"
      confidence: medium
      note: "需标签解析规则"

  - name: is_gazelle
    type: tinyint
    nullable: true
    business_def: 是否瞪羚企业
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_company_honor_tags 解析"
      confidence: medium
      note: "需标签解析规则"

  - name: is_unicorn
    type: tinyint
    nullable: true
    business_def: 是否独角兽
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "dwd_company_honor_tags 解析"
      confidence: medium
      note: "需标签解析规则"
```
---

## 字段一览（给人读的表）

| # | 字段名 | 类型 | 可空 | 业务定义 | metric_ref | confidence | expected_from |
|---|--------|------|------|----------|------------|------------|---------------|
| 1 | id | bigint | 否 | 代理主键 | — | high | 供应侧主表代理键 |
| 2 | enterprise_code | varchar(64) | 否 | 统一社会信用代码 | — | high | external_id / credit_code |
| 3 | enterprise_name | varchar(255) | 否 | 企业全称 | — | high | name_cn / name |
| 4 | enterprise_name_short | varchar(100) | 是 | 企业简称 | — | low | 无直接来源 |
| 5 | legal_representative | varchar(100) | 是 | 法定代表人 | — | high | lerep / legal_representative |
| 6 | registered_capital | decimal(20,4) | 是 | 注册资本(万元) | — | high | registered_capital_value / reg_capital_std |
| 7 | registration_date | date | 是 | 成立日期 | — | high | incorporation_date / establish_date |
| 8 | business_status | varchar(20) | 是 | 经营状态 | — | high | status_std |
| 9 | enterprise_type | varchar(50) | 是 | 企业类型(三级) | — | high | first/second/detail_type |
| 10 | business_scope | text | 是 | 经营范围 | — | high | main_activities / scope |
| 11 | industry_category | varchar(100) | 是 | 所属行业名称 | — | high | industry_class / industry_l1_name |
| 12 | industry_code | varchar(20) | 是 | 行业代码 | — | high | industry_l1_code |
| 13 | headquarters_city | varchar(100) | 是 | 总部城市 | M_ENT_SZ_COUNT | high | city / reg_city |
| 14 | headquarters_district | varchar(100) | 是 | 总部区县 | — | high | ori_reg_district / reg_district |
| 15 | headquarters_province | varchar(100) | 是 | 总部省份 | — | high | province / ori_reg_province |
| 16 | headquarters_lng | decimal(12,7) | 是 | 经度 | — | medium | addr_lng / reg_xy |
| 17 | headquarters_lat | decimal(12,7) | 是 | 纬度 | — | medium | addr_lat / reg_xy |
| 18 | revenue_latest | decimal(20,4) | 是 | 最新年营收(万元) | — | high | operating_revenue |
| 19 | revenue_year | int | 是 | 营收对应年份 | — | high | year |
| 20 | revenue_growth_rate | decimal(10,4) | 是 | 营收增长率(%) | — | medium | 相邻年计算 |
| 21 | net_profit | decimal(20,4) | 是 | 净利润(万元) | — | high | pure_profit |
| 22 | profit_margin | decimal(10,4) | 是 | 利润率(%) | — | medium | 净利润/营收计算 |
| 23 | gross_margin | decimal(10,4) | 是 | 毛利率(%) | — | low | 上市可推算 |
| 24 | rd_staff_count | int | 是 | 研发人数 | — | medium | employees_number(Q019) |
| 25 | rd_staff_ratio | decimal(10,4) | 是 | 研发人数占比 | — | low | 计算 |
| 26 | rd_investment | decimal(20,4) | 是 | 研发投入(万元) | — | medium | research_development_amount |
| 27 | rd_investment_ratio | decimal(10,4) | 是 | 研发投入占比(%) | — | low | 计算 |
| 28 | patent_apply_count | int | 是 | 累计专利申请数 | — | high | dwd_patent 聚合 |
| 29 | patent_grant_count | int | 是 | 累计专利授权数 | — | high | inv+util+des 预聚合 |
| 30 | patent_valid_count | int | 是 | 有效专利数 | — | medium | dwd_patent_legal 计算 |
| 31 | patent_invention_count | int | 是 | 发明专利授权数 | — | high | inv_pat_auth_num |
| 32 | patent_citation_count | int | 是 | 专利被引数 | — | high | dwd_patent_cited 聚合 |
| 33 | tech_score | decimal(10,4) | 是 | 技术力评分 | M_ENT_TECH_POWER_SCORE | medium | 算法侧产出 |
| 34 | business_score | decimal(10,4) | 是 | 商业力评分 | M_ENT_BUSINESS_POWER_SCORE | low | 算法侧产出 |
| 35 | competitiveness_score | decimal(10,4) | 是 | 综合竞争力评分 | M_ENT_COMPETITIVENESS_SCORE | medium | 算法侧产出 |
| 36 | risk_level | varchar(20) | 是 | 风险等级 | — | low | dwd_org_risk_* 综合 |
| 37 | is_high_tech | tinyint | 是 | 是否高新技术企业 | — | medium | org_tag / honor_tags 解析 |
| 38 | is_little_giant | tinyint | 是 | 是否专精特新 | — | medium | honor_tags 解析 |
| 39 | is_gazelle | tinyint | 是 | 是否瞪羚 | — | medium | honor_tags 解析 |
| 40 | is_unicorn | tinyint | 是 | 是否独角兽 | — | medium | honor_tags 解析 |

---

## SEARCH/EVAL/RISK/RECRUIT 核心字段覆盖对照表

| 模块 | 核心字段 | 本表字段 | 说明 |
|------|---------|---------|------|
| **SEARCH** (E-20) | enterprise_name | enterprise_name | 搜索关键词匹配 |
| | industry_category | industry_category | 行业筛选 |
| | headquarters_city | headquarters_city | 城市筛选 |
| | registered_capital | registered_capital | 规模分档 |
| | patent_grant_count | patent_grant_count | 排序权重 |
| | registration_date | registration_date | 成立时间筛选 |
| **EVAL** (E-23/E-24/E-30) | enterprise_code | enterprise_code | 企业标识 |
| | headquarters_city | headquarters_city | 画像展示 |
| | revenue_latest | revenue_latest | 商业力-市场维度 |
| | revenue_growth_rate | revenue_growth_rate | 商业力-成长性 |
| | rd_investment | rd_investment | 技术力-投入维度 |
| | rd_staff_count | rd_staff_count | 技术力-人才维度 |
| | patent_grant_count | patent_grant_count | 技术力-创新维度 |
| | patent_invention_count | patent_invention_count | 技术力-创新加权 |
| | gross_margin | gross_margin | 商业力-市场维度 |
| | market_share | (未入本表) | ❌ 无来源(K-O7)，需采购 |
| | tech_score | tech_score | 算法评分产出 |
| | business_score | business_score | 算法评分产出 |
| | competitiveness_score | competitiveness_score | 算法评分产出 |
| **RISK** (E-25) | risk_level | risk_level | 风险等级 |
| | enterprise_supply_chain.* | (见 dwd_enterprise_supply_chain 契约，待建) | 供应链关系数据另表 |
| **RECRUIT** (E-35) | enterprise_code | enterprise_code | 企业标识 |
| | revenue_latest | revenue_latest | 招引价值-成长性 |
| | revenue_growth_rate | revenue_growth_rate | 招引价值-成长性 |
| | headquarters_city | headquarters_city | 画像 |
| | industry_category | industry_category | 产业链匹配 |
| | is_high_tech | is_high_tech | 招引标签 |
| | is_little_giant | is_little_giant | 招引标签 |

> **未覆盖字段说明**：`market_share`（市场份额）和 `brand_score`（品牌声量）在供应库无来源（K-O7），需采购市调数据，不在本表 Phase 1 契约范围。`enterprise_supply_chain`（供应链上下游关系）为独立 DWD 表，将另建 `dwd_enterprise_supply_chain.md` 契约。

---

## Phase 2 映射验收清单（8/20 后勾选）

- [ ] GDF 已为本表产出 ODS→项目 DWD 字段级 mapping
- [ ] lineage-subcoord 已验证完整度
- [ ] 引用本表的全部 metric：`mapping_status` 已从 `⏳` 升级为 `✅` 或 `❌`
- [ ] 若有 `❌`：已登记 `data-gap-catalog.yaml` + `客户决策清单跟踪表.md`（🟡）
- [ ] UI 已移除本表相关指标的 ⏳ OdsPendingBadge（或转为 ⚠️）

---

## 变更记录

| 日期 | 变更 | 作者 |
|------|------|------|
| 2026-08-10 | 初版：40 字段（6 组），覆盖 SEARCH/EVAL/RISK/RECRUIT 核心字段；Phase 1 契约，ods_mapping_expectation 全覆盖 | data-agent / lineage-subcoord（任务 ENT-LINEAGE-DWD-CONTRACT-L01） |