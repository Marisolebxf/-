# 金融域 ETL Mapping 明细 — 源表到 DWD

> **版本**：v1.0（2026-11-09）  
> **范围**：金融要素库 → 项目 DWD（`gkxlumenx_dwd.fin_*`）字段级映射。**v1 只覆盖 P0 / P1 共 19 张源表 → 11 张目标表**；P2 / 0 行表本期只贴不洗，分期见 `00` §3  
> **源**：`gkxlumenx_ods` 同名贴源表（Wave A 由 `gkx.dwd_*` 镜像，已按 `is_deleted = 0` 过滤）  
> **目标库**：`gkxlumenx_dwd`（MySQL）。建表草稿见 [10-DWD-MySQL-DDL/fin-dwd-draft.md](10-DWD-MySQL-DDL/fin-dwd-draft.md)  
> **交付对象**：GDF 产线  
> **结构真源声明**：源表列以 **live `gkx`** 为准。本文 §3 与 [09a](09a-源表业务列清单-金融31表.md) 取自 20261109 行数报告（Excel 抽取），两者不一致时以 live 为准并在回签登记（`00` §0.3）。  
> **自检**：§3.4 起的矩阵由 `script/gen_fin_pack.py` 生成；该脚本 `--check` 会核对每个引用的源列都在报告列清单里。

---

## 0. 本期边界

| 做 | 不做 |
|---|---|
| P0 9 张、P1 10 张源表按 §3 洗入 11 张 `fin_*` 目标表 | P2 日行情 / 期权 / 外汇 6 张、公募基金 0 行 3 张：只贴不洗 |
| 保留供应方 `org_id` / `sec_id` 原值；追溯列 `src_dwd_id`（联合表加 `src_table`） | 自造 `org_id`；用信用代码当 `org_id`；因 JOIN 不上而丢行 |
| 默认 `is_deleted = 0`（Wave A 已过滤，Wave B 不再重复判断） | 按业务口径删行、去重（重复只在验收登记，见 OPEN-FIN-02） |
| 解析不了的值写 `NULL` | 把 `--`、空串、解析失败写成 `0` |
| 外币金额原样保留，不换汇 | 汇率折算 |

**不与下列包混表**：

| 包 | 关系 |
|---|---|
| `GDF-ENT-WORKPACK-v4` | `dwd_org_financing_info` / `dwd_org_invest_info` 的贴源与洗入 `enterprise_financing` / `enterprise_invest` **归企业包**；`dwd_org_merger_acquisition_info` 企业包维持只贴不洗。本包不重复配这三张的贴源作业，也不另洗一份 |
| `GDF-MACRO-WORKPACK-v1` | `dwd_foreign_exchange_info`（外汇）虽属金融要素库，但本包 v1 只贴不洗，不抢宏观包口径。宏观六表归 MACRO 包，不进本包 |
| `GDF-CHAIN-WORKPACK-v2` | 链树、分析六表、产业资讯不进本包 |
| `GDF-SVC-WORKPACK` | 服务机构后加工读 ODS 的融资 / 投资表，与本包无写冲突 |

---

## 1. 映射分类

| 类型 | 说明 |
|---|---|
| **直接** | 源列写入同义目标列，类型按目标列定义转换 |
| **字面量** | 联合表用来区分来源的常量列（`src_table` / `class_system` / `dim_type` / `market` / `bond_class`） |
| **缺列** | 该源表没有此列，目标写 `NULL` |
| **派生** | `reg_capital_wan`，规则见 §3.3 |

联合表规则：`UNION ALL`，不去重；主键 `(src_table, src_dwd_id)`。

---

## 2. 源表 → 目标表总览（v1）

| # | 目标表 | 分期 | 源表（`gkxlumenx_ods`） | 源行数（20261109） |
|---|---|---|---|---:|
| 1 | `fin_corp_basic` | P0 | `dwd_corp_basic_info` | 20,000 |
| 2 | `fin_security` | P0 | `dwd_sec_basic_info` | 1,242,959 |
| 3 | `fin_industrial_fund` | P0 | `dwd_industrial_fund_basic_info` | 10,891 |
| 4 | `fin_industrial_fund_gp` | P0 | `dwd_industrial_fund_management_institution` | 10,943 |
| 5 | `fin_industrial_fund_lp` | P0 | `dwd_industrial_fund_lp_info` | 20,000 |
| 6 | `fin_industrial_fund_strategy` | P0 | `dwd_industrial_fund_investment_strategy` | 10,891 |
| 7 | `fin_industrial_fund_inv_summary` | P0 | `dwd_industrial_fund_investment_project_info` | 10,891 |
| 8 | `fin_bond` | P0 | `dwd_sci_tech_inno_bonds` + `dwd_high_tech_industry_bonds` | 3,894 + 72 |
| 9 | `fin_industry_class_his` | P1 | `dwd_corp_his_sw_ic` + `_crsc_ic` + `_citic_ic` + `dwd_hk_corp_his_sw_ic` | 78,034 + 32,472 + 26,367 + 2,849 |
| 10 | `fin_main_biz_composition` | P1 | `dwd_main_business_composition_industry` + `_prod` + `_area` | 295,641 + 610,840 + 464,011 |
| 11 | `fin_valuation_daily` | P1 | `dwd_astock_val_indicators` + `dwd_hk_stock_val_indicators` + `dwd_us_stock_val_ind` | 3,221,732 + 39,910 + 1,749 |

> 行数是行数报告的快照，只用于验收对数，不当目标行数承诺。`dwd_corp_basic_info` 与 `dwd_industrial_fund_lp_info` 恰为 20,000，疑似供应方限量，见 OPEN-FIN-10。

---

## 3. 字段映射

### 3.1 每张目标表都有的列

| 列 | 类型 | 说明 |
|---|---|---|
| `src_dwd_id` | bigint NOT NULL | 供应方 `dwd_id`，追溯用，不当业务键 |
| `src_table` | varchar(64) NOT NULL | 仅联合表。来源物理表名 |
| `etl_time` | datetime | GDF 写入时间，默认 `CURRENT_TIMESTAMP` |

### 3.2 不映射的源列

| 源列 | 原因 |
|---|---|
| `t_id` | Excel 多出，live 库无 |
| `dwd_id` | 只进 `src_dwd_id` |
| `created_time` / `updated_time` / `creater` / `updater` / `table_data_source` / `operator_remarks` / `is_deleted` / `insert_remark` | 供应方技术字段，只作审计，不当业务口径 |
| `data_source` | 供应方来源描述，本期不进 DWD；追溯靠 `src_table` + `src_dwd_id` |

### 3.3 `reg_capital_wan` 解析规则（产业基金注册资本）

`dwd_industrial_fund_basic_info.reg_capital` 是带单位的字符串（样例 `30000.00万元`）。

| 原文形态 | `reg_capital_wan`（万元人民币） |
|---|---|
| `<数字>万元`、`<数字>万元人民币` | 数字原值 |
| `<数字>亿元`、`<数字>亿元人民币` | 数字 × 10000 |
| `<数字>元` | 数字 ÷ 10000 |
| 含美元 / 港元 / 欧元等外币、`/`、空串、其他 | `NULL`（不换汇，不写 0） |

数字允许千分位逗号。可执行断言在 `script/gen_fin_pack.py` 的 `parse_wan` / `_self_check_rules`。已有指标调研记录该列可解析率约 58.57%（`M_INNOV_PG_FUND` 调研），验收时以实测为准，登记 `reg_capital_wan IS NULL` 占比。

<!-- BEGIN GEN §3 -->
### 3.4 `fin_corp_basic` · 上市公司基本资料（沪深港美）（P0）

源：`dwd_corp_basic_info`（1:1）

| 目标列 | 类型 | 说明 | `corp_basic_info` |
|---|---|---|---|
| `src_dwd_id` | bigint NOT NULL | 供应方 dwd_id（追溯） | `dwd_id` |
| `org_id` | varchar(255) NOT NULL | 机构ID（供应方 org_id，原样；与 enterprise_base.org_id 对照见 09 §4） | `org_id` |
| `org_name_cn` | varchar(500) NULL | 机构名称（中文） | `org_name_cn` |
| `org_name_en` | varchar(500) NULL | 机构名称（英文） | `org_name_en` |
| `reg_region` | varchar(255) NULL | 注册国家或地区 | `reg_region` |
| `established_date` | date NULL | 成立日期 | `established_date` |
| `business_reg_num` | varchar(255) NULL | 工商登记号 | `business_reg_num` |
| `etl_time` | datetime | GDF 写入时间（默认 CURRENT_TIMESTAMP） | — |

键：PK=(`src_dwd_id`)；普通索引 `org_id`。业务自然键是否唯一以验收抽检为准（OPEN-FIN-02）。

### 3.5 `fin_security` · 证券基本资料（P0）

源：`dwd_sec_basic_info`（1:1）

| 目标列 | 类型 | 说明 | `sec_basic_info` |
|---|---|---|---|
| `src_dwd_id` | bigint NOT NULL | 供应方 dwd_id（追溯） | `dwd_id` |
| `sec_id` | varchar(255) NOT NULL | 证券ID（供应方 sec_id） | `sec_id` |
| `sec_code` | varchar(255) NULL | 证券代码 | `sec_code` |
| `sec_full_name` | varchar(500) NULL | 证券全称 | `sec_full_name` |
| `sec_full_name_en` | varchar(500) NULL | 证券英文全称 | `sec_full_name_en` |
| `sec_type` | varchar(255) NULL | 证券类别 | `sec_type` |
| `td_mkt` | varchar(255) NULL | 交易市场 | `td_mkt` |
| `td_currency_name` | varchar(255) NULL | 交易货币名称 | `td_currency_name` |
| `listed_board_name` | varchar(255) NULL | 上市板名称 | `listed_board_name` |
| `listed_status` | varchar(255) NULL | 上市状态 | `listed_status` |
| `is_listing` | smallint NULL | 是否上市 0否1是 | `is_listing` |
| `is_delisted` | smallint NULL | 是否摘牌 0否1是 | `is_delisted` |
| `listed_date` | date NULL | 上市日期 | `listed_date` |
| `stop_listing_date` | date NULL | 终止上市日期 | `stop_listing_date` |
| `org_id` | varchar(255) NULL | 机构ID | `org_id` |
| `sec_issuer_id` | varchar(255) NULL | 证券发行主体ID（基金/指数/期货用） | `sec_issuer_id` |
| `issue_org_id` | varchar(255) NULL | 发行机构ID | `issue_org_id` |
| `bond_code` | varchar(255) NULL | 债券关联代码（关联 fin_bond.bond_code） | `bond_code` |
| `issuer_name` | varchar(255) NULL | 公司名称 | `name_cn` |
| `credit_code` | varchar(255) NULL | 统一社会信用代码 | `external_id` |
| `etl_time` | datetime | GDF 写入时间（默认 CURRENT_TIMESTAMP） | — |

键：PK=(`src_dwd_id`)；普通索引 `sec_id`、`sec_code`、`org_id`。业务自然键是否唯一以验收抽检为准（OPEN-FIN-02）。

### 3.6 `fin_industrial_fund` · 产业基金基本信息（P0）

源：`dwd_industrial_fund_basic_info`（1:1）

| 目标列 | 类型 | 说明 | `industrial_fund_basic_info` |
|---|---|---|---|
| `src_dwd_id` | bigint NOT NULL | 供应方 dwd_id（追溯） | `dwd_id` |
| `industrial_fund_id` | varchar(255) NOT NULL | 产业基金ID | `industrial_fund_id` |
| `fund_short_name` | varchar(255) NULL | 基金简称 | `industrial_fund_short_name` |
| `fund_name` | varchar(255) NULL | 基金名称 | `industrial_fund_name` |
| `reg_region` | varchar(255) NULL | 注册地区（原样，形如 天津市-西青区） | `reg_region` |
| `est_date` | date NULL | 成立日期 | `est_date` |
| `fund_type` | varchar(255) NULL | 基金类型 | `industrial_fund_type` |
| `currency_ctgry` | varchar(255) NULL | 投资币种 | `currency_ctgry` |
| `capital_source` | varchar(255) NULL | 资本来源 | `capital_source` |
| `fund_year` | int NULL | 基金存续年限 | `industrial_fund_year` |
| `state_owned` | varchar(255) NULL | 国资背景 | `state_owned` |
| `reg_status` | varchar(255) NULL | 设立状态 | `reg_status` |
| `proposed_reg_date` | date NULL | 拟设立时间 | `proposed_reg_date` |
| `reg_address` | text NULL | 注册地址 | `reg_address` |
| `reg_capital_raw` | varchar(255) NULL | 注册资本原文（含单位） | `reg_capital` |
| `reg_capital_wan` | decimal(20,4) NULL | 注册资本（万元人民币）：仅 元/万元/亿元 可解析；含外币或解析失败为 NULL，不写 0、不换汇 | `parse_wan(reg_capital)`（规则见 §3.3） |
| `real_capital_raw` | varchar(255) NULL | 实缴资本原文 | `real_capital` |
| `credit_code` | varchar(255) NULL | 统一社会信用代码 | `external_id` |
| `est_status` | varchar(255) NULL | 经营状态 | `est_status` |
| `etl_time` | datetime | GDF 写入时间（默认 CURRENT_TIMESTAMP） | — |

键：PK=(`src_dwd_id`)；普通索引 `industrial_fund_id`。业务自然键是否唯一以验收抽检为准（OPEN-FIN-02）。

### 3.7 `fin_industrial_fund_gp` · 产业基金管理机构（GP）（P0）

源：`dwd_industrial_fund_management_institution`（1:1）

| 目标列 | 类型 | 说明 | `industrial_fund_management_institution` |
|---|---|---|---|
| `src_dwd_id` | bigint NOT NULL | 供应方 dwd_id（追溯） | `dwd_id` |
| `industrial_fund_id` | varchar(255) NOT NULL | 产业基金ID | `industrial_fund_id` |
| `gp_org_id` | varchar(255) NOT NULL | GP机构ID | `gp_org_id` |
| `gp_org_name` | varchar(255) NULL | GP名称全称 | `gp_org_name` |
| `brand_institution_name` | varchar(255) NULL | 归属品牌机构名称（简称） | `brand_institution_name` |
| `brand_institution_tag` | varchar(255) NULL | 归属品牌机构标签 | `brand_institution_tag` |
| `brand_institution_region` | varchar(255) NULL | 归属品牌机构总部地区 | `brand_institution_region` |
| `brand_institution_type` | varchar(255) NULL | 归属品牌机构类型 | `brand_institution_type` |
| `etl_time` | datetime | GDF 写入时间（默认 CURRENT_TIMESTAMP） | — |

键：PK=(`src_dwd_id`)；普通索引 `industrial_fund_id`、`gp_org_id`。业务自然键是否唯一以验收抽检为准（OPEN-FIN-02）。

### 3.8 `fin_industrial_fund_lp` · 产业基金LP信息（P0）

源：`dwd_industrial_fund_lp_info`（1:1）

| 目标列 | 类型 | 说明 | `industrial_fund_lp_info` |
|---|---|---|---|
| `src_dwd_id` | bigint NOT NULL | 供应方 dwd_id（追溯） | `dwd_id` |
| `industrial_fund_id` | varchar(255) NOT NULL | 产业基金ID | `industrial_fund_id` |
| `lp_org_id` | varchar(255) NOT NULL | LP机构ID | `lp_org_id` |
| `lp_org_name` | varchar(255) NULL | LP机构全称 | `lp_org_name` |
| `lp_org_type` | text NULL | LP类型 | `lp_org_type` |
| `lp_state_owned` | varchar(255) NULL | LP是否国资背景 | `lp_state_owned` |
| `state_lp_sub_ratio` | decimal(20,2) NULL | 国资LP认缴比例（源列 solp_rub_ratio） | `solp_rub_ratio` |
| `lp_region_name` | varchar(255) NULL | LP所在地区 | `lp_region_name` |
| `lp_first_inv_date` | date NULL | LP首次出资时间 | `lp_first_inv_date` |
| `sub_capital` | decimal(20,2) NULL | LP认缴金额（单位待供应方确认 OPEN-FIN-03，原样） | `sub_capital` |
| `lp_inv_ratio` | decimal(20,2) NULL | LP出资比例 | `lp_inv_ratio` |
| `lp_real_capital` | decimal(20,2) NULL | LP实缴金额（单位同上） | `lp_real_capital` |
| `lp_brand_institution` | varchar(255) NULL | LP归属品牌 | `lp_brand_institution` |
| `is_lp_exited` | varchar(255) NULL | LP是否退出 | `is_lp_exited` |
| `etl_time` | datetime | GDF 写入时间（默认 CURRENT_TIMESTAMP） | — |

键：PK=(`src_dwd_id`)；普通索引 `industrial_fund_id`、`lp_org_id`。业务自然键是否唯一以验收抽检为准（OPEN-FIN-02）。

### 3.9 `fin_industrial_fund_strategy` · 产业基金投资策略（P0）

源：`dwd_industrial_fund_investment_strategy`（1:1）

| 目标列 | 类型 | 说明 | `industrial_fund_investment_strategy` |
|---|---|---|---|
| `src_dwd_id` | bigint NOT NULL | 供应方 dwd_id（追溯） | `dwd_id` |
| `industrial_fund_id` | varchar(255) NOT NULL | 产业基金ID | `industrial_fund_id` |
| `inv_field` | text NULL | 投资领域（多值，源内以换行分隔，原样不拆） | `inv_field` |
| `inv_round` | varchar(255) NULL | 投资轮次 | `inv_round` |
| `inv_industry` | varchar(255) NULL | 投资行业 | `inv_industry` |
| `strategy_desc` | text NULL | 策略描述 | `strategy_desc` |
| `etl_time` | datetime | GDF 写入时间（默认 CURRENT_TIMESTAMP） | — |

键：PK=(`src_dwd_id`)；普通索引 `industrial_fund_id`。业务自然键是否唯一以验收抽检为准（OPEN-FIN-02）。

### 3.10 `fin_industrial_fund_inv_summary` · 产业基金投资汇总（基金级，非项目级）（P0）

源：`dwd_industrial_fund_investment_project_info`（1:1）

| 目标列 | 类型 | 说明 | `industrial_fund_investment_project_info` |
|---|---|---|---|
| `src_dwd_id` | bigint NOT NULL | 供应方 dwd_id（追溯） | `dwd_id` |
| `industrial_fund_id` | varchar(255) NOT NULL | 产业基金ID | `industrial_fund_id` |
| `latest_inv_date` | date NULL | 最新投资时间 | `latest_inv_date` |
| `inv_event_count` | int NULL | 投资事件数量 | `inv_event_count` |
| `total_inv_companies_count` | int NULL | 投资企业总数 | `total_inv_companies_count` |
| `cum_inv_amount` | decimal(20,2) NULL | 累计投资金额（单位待确认 OPEN-FIN-03，原样） | `cum_inv_amount` |
| `listed_companies_count` | int NULL | 投后企业上市数量 | `listed_companies_count` |
| `etl_time` | datetime | GDF 写入时间（默认 CURRENT_TIMESTAMP） | — |

键：PK=(`src_dwd_id`)；普通索引 `industrial_fund_id`。业务自然键是否唯一以验收抽检为准（OPEN-FIN-02）。

### 3.11 `fin_bond` · 科创债 / 高新技术产业债（P0）

源：`dwd_sci_tech_inno_bonds`、`dwd_high_tech_industry_bonds`（UNION ALL，`src_table` 区分来源）

| 目标列 | 类型 | 说明 | `sci_tech_inno_bonds` | `high_tech_industry_bonds` |
|---|---|---|---|---|
| `src_dwd_id` | bigint NOT NULL | 供应方 dwd_id（追溯） | `dwd_id` | `dwd_id` |
| `src_table` | varchar(64) NOT NULL | 来源物理表 | 字面量 'dwd_sci_tech_inno_bonds' | 字面量 'dwd_high_tech_industry_bonds' |
| `bond_class` | varchar(32) NOT NULL | 债券类别：SCI_TECH_INNO / HIGH_TECH_INDUSTRY | 字面量 'SCI_TECH_INNO' | 字面量 'HIGH_TECH_INDUSTRY' |
| `bond_code` | varchar(255) NOT NULL | 债券代码 | `bond_code` | `bond_code` |
| `bond_name` | varchar(255) NULL | 债券名称 | `bond_name` | `bond_name` |
| `issue_amount_yi` | decimal(20,4) NULL | 发行总额（亿）；源为 -- 的不写 0 | `issue_amount` | `issue_amount` |
| `issue_term_years` | decimal(20,4) NULL | 发行期限（年）；仅高新债有 | —（该源无此列→NULL） | `issue_term_years` |
| `issue_price` | decimal(20,4) NULL | 发行价格；仅高新债有 | —（该源无此列→NULL） | `issue_price` |
| `current_coupon_rate` | decimal(20,4) NULL | 当期票面利率（%） | `current_coupon_rate` | `current_coupon_rate` |
| `interest_rate_type` | varchar(255) NULL | 利率类型；仅高新债有 | —（该源无此列→NULL） | `interest_rate_type` |
| `payment_frequency` | varchar(255) NULL | 付息频率 | `payment_frequency` | `payment_frequency` |
| `issue_date` | date NULL | 发行日期 | `issue_date` | `issue_date` |
| `maturity_date` | date NULL | 到期日期 | `maturity_date` | `maturity_date` |
| `latest_bond_rating` | varchar(255) NULL | 最新债项评级 | `latest_bond_rating` | `latest_bond_rating` |
| `latest_issuer_rating` | varchar(255) NULL | 最新主体信用评级 | `latest_issuer_rating` | `latest_issuer_rating` |
| `issue_issuer_rating` | varchar(255) NULL | 发行时主体评级 | `issue_issuer_rating` | `issue_issuer_rating` |
| `gics_l1` | varchar(255) NULL | GICS一级行业 | `gics_sector` | `gics_c_name` |
| `gics_l2` | varchar(255) NULL | GICS二级行业 | `gics_industry_group` | `gics_l_name` |
| `gics_l3` | varchar(255) NULL | GICS三级行业 | `gics_industry` | `gics_m_name` |
| `gics_l4` | varchar(255) NULL | GICS四级行业 | `gics_sub_industry` | `gics_s_name` |
| `issuer` | varchar(255) NULL | 发行人 | `issuer` | `issuer` |
| `issuer_type` | varchar(255) NULL | 发行人类型 | `issuer_type` | `issuer_type` |
| `trading_market` | varchar(255) NULL | 交易市场 | `trading_market` | `trading_market` |
| `etl_time` | datetime | GDF 写入时间（默认 CURRENT_TIMESTAMP） | — | — |

键：PK=(`src_table`,`src_dwd_id`)；普通索引 `bond_code`、`issuer`。业务自然键是否唯一以验收抽检为准（OPEN-FIN-02）。

### 3.12 `fin_industry_class_his` · 上市公司行业分类全量（申万/证监会/中信/港股申万）（P1）

源：`dwd_corp_his_sw_ic`、`dwd_corp_his_crsc_ic`、`dwd_corp_his_citic_ic`、`dwd_hk_corp_his_sw_ic`（UNION ALL，`src_table` 区分来源）

| 目标列 | 类型 | 说明 | `corp_his_sw_ic` | `corp_his_crsc_ic` | `corp_his_citic_ic` | `hk_corp_his_sw_ic` |
|---|---|---|---|---|---|---|
| `src_dwd_id` | bigint NOT NULL | 供应方 dwd_id（追溯） | `dwd_id` | `dwd_id` | `dwd_id` | `dwd_id` |
| `src_table` | varchar(64) NOT NULL | 来源物理表 | 字面量 'dwd_corp_his_sw_ic' | 字面量 'dwd_corp_his_crsc_ic' | 字面量 'dwd_corp_his_citic_ic' | 字面量 'dwd_hk_corp_his_sw_ic' |
| `class_system` | varchar(16) NOT NULL | 分类体系：SW_CN / CRSC_CN / CITIC_CN / SW_HK | 字面量 'SW_CN' | 字面量 'CRSC_CN' | 字面量 'CITIC_CN' | 字面量 'SW_HK' |
| `org_id` | varchar(255) NOT NULL | 机构ID | `org_id` | `org_id` | `org_id` | `org_id` |
| `org_name` | varchar(255) NULL | 公司名称 | `name_cn` | `name_cn` | `name_cn` | `name_cn` |
| `credit_code` | varchar(255) NULL | 统一社会信用代码 | `external_id` | `external_id` | `external_id` | `external_id` |
| `industry_type` | varchar(255) NULL | 行业类别 | `industry_type` | `industry_type` | `industry_type` | `industry_type` |
| `industry_level` | int NULL | 行业级别 | `industry_level` | `industry_level` | `industry_level` | `industry_level` |
| `inclusion_date` | date NULL | 纳入日期 | `inclusion_date` | `inclusion_date` | `inclusion_date` | `inclusion_date` |
| `eliminate_date` | date NULL | 剔除日期 | `eliminate_date` | `eliminate_date` | `eliminate_date` | `eliminate_date` |
| `industry_code` | varchar(255) NULL | 行业代码 | `industry_code` | `industry_code` | `industry_code` | `industry_code` |
| `industry_name` | varchar(255) NULL | 行业名称 | `industry_name` | `industry_name` | `industry_name` | `industry_name` |
| `is_latest` | smallint NULL | 最新标志 1最新；港股申万源无此列→NULL，ADS 以 eliminate_date IS NULL 判最新 | `lastest_symbol` | `lastest_symbol` | `lastest_symbol` | —（该源无此列→NULL） |
| `etl_time` | datetime | GDF 写入时间（默认 CURRENT_TIMESTAMP） | — | — | — | — |

键：PK=(`src_table`,`src_dwd_id`)；普通索引 `org_id`、`class_system`。业务自然键是否唯一以验收抽检为准（OPEN-FIN-02）。

### 3.13 `fin_main_biz_composition` · 沪深上市企业主营业务构成（行业/产品/地区）（P1）

源：`dwd_main_business_composition_industry`、`dwd_main_business_composition_prod`、`dwd_main_business_composition_area`（UNION ALL，`src_table` 区分来源）

| 目标列 | 类型 | 说明 | `main_business_composition_industry` | `main_business_composition_prod` | `main_business_composition_area` |
|---|---|---|---|---|---|
| `src_dwd_id` | bigint NOT NULL | 供应方 dwd_id（追溯） | `dwd_id` | `dwd_id` | `dwd_id` |
| `src_table` | varchar(64) NOT NULL | 来源物理表 | 字面量 'dwd_main_business_composition_industry' | 字面量 'dwd_main_business_composition_prod' | 字面量 'dwd_main_business_composition_area' |
| `dim_type` | varchar(16) NOT NULL | 构成维度：INDUSTRY / PRODUCT / AREA | 字面量 'INDUSTRY' | 字面量 'PRODUCT' | 字面量 'AREA' |
| `dim_name` | varchar(255) NOT NULL | 维度名称（行业名/产品名/地区名） | `industry_name` | `prod_name` | `area_name` |
| `org_id` | varchar(255) NOT NULL | 机构ID | `org_id` | `org_id` | `org_id` |
| `credit_code` | varchar(255) NULL | 统一社会信用代码 | `external_id` | `external_id` | `external_id` |
| `stock_code` | varchar(255) NULL | 股票代码 | `stock_code` | `stock_code` | `stock_code` |
| `stock_name` | varchar(255) NULL | 代码简称 | `stock_noun` | `stock_noun` | `stock_noun` |
| `occur_period` | varchar(255) NOT NULL | 报告期（源样例 202603，原样字符串；OPEN-FIN-04） | `occur_period` | `occur_period` | `occur_period` |
| `core_biz_income` | decimal(20,4) NULL | 主营业务收入（万元） | `core_biz_income` | `core_biz_income` | `core_biz_income` |
| `core_biz_income_prop` | decimal(20,4) NULL | 主营业务收入占比（%） | `core_biz_income_prop` | `core_biz_income_prop` | `core_biz_income_prop` |
| `core_biz_income_gr` | decimal(20,4) NULL | 主营业务收入增长率（%） | `core_biz_income_gr` | `core_biz_income_gr` | `core_biz_income_gr` |
| `core_biz_cost` | decimal(20,4) NULL | 主营业务成本（万元） | `core_biz_cost` | `core_biz_cost` | `core_biz_cost` |
| `core_biz_cost_prop` | decimal(20,4) NULL | 主营业务成本占比（%） | `core_biz_cost_prop` | `core_biz_cost_prop` | `core_biz_cost_prop` |
| `core_biz_cost_gr` | decimal(20,4) NULL | 主营业务成本增长率（%） | `core_biz_cost_gr` | `core_biz_cost_gr` | `core_biz_cost_gr` |
| `core_biz_profit` | decimal(20,4) NULL | 主营业务利润（万元） | `core_biz_profit` | `core_biz_profit` | `core_biz_profit` |
| `core_biz_profit_prop` | decimal(20,4) NULL | 主营业务利润占比（%） | `core_biz_profit_prop` | `core_biz_profit_prop` | `core_biz_profit_prop` |
| `gross_margin` | decimal(20,4) NULL | 毛利率（%） | `gross_margin` | `gross_margin` | `gross_margin` |
| `gross_margin_change` | decimal(20,4) NULL | 毛利率变动 | `gross_margin_change` | `gross_margin_change` | `gross_margin_change` |
| `csrc_industry` | varchar(255) NULL | 行业_证监会（新） | `csrc_industry` | `csrc_industry` | `csrc_industry` |
| `shenwan_industry` | varchar(255) NULL | 行业_申万 | `shenwan_industry` | `shenwan_industry` | `shenwan_industry` |
| `etl_time` | datetime | GDF 写入时间（默认 CURRENT_TIMESTAMP） | — | — | — |

键：PK=(`src_table`,`src_dwd_id`)；普通索引 `org_id`、`dim_type`、`occur_period`。业务自然键是否唯一以验收抽检为准（OPEN-FIN-02）。

### 3.14 `fin_valuation_daily` · 股票估值指标日表（A股/港股/美股）（P1）

源：`dwd_astock_val_indicators`、`dwd_hk_stock_val_indicators`、`dwd_us_stock_val_ind`（UNION ALL，`src_table` 区分来源）

| 目标列 | 类型 | 说明 | `astock_val_indicators` | `hk_stock_val_indicators` | `us_stock_val_ind` |
|---|---|---|---|---|---|
| `src_dwd_id` | bigint NOT NULL | 供应方 dwd_id（追溯） | `dwd_id` | `dwd_id` | `dwd_id` |
| `src_table` | varchar(64) NOT NULL | 来源物理表 | 字面量 'dwd_astock_val_indicators' | 字面量 'dwd_hk_stock_val_indicators' | 字面量 'dwd_us_stock_val_ind' |
| `market` | varchar(8) NOT NULL | 市场：CN / HK / US | 字面量 'CN' | 字面量 'HK' | 字面量 'US' |
| `sec_id` | varchar(255) NOT NULL | 证券ID（关联 fin_security.sec_id） | `sec_id` | `sec_id` | `sec_id` |
| `dt` | date NOT NULL | 日期 | `dt` | `dt` | `dt` |
| `pe_ttm_ed` | decimal(20,4) NULL | 市盈率 PE(TTM) | `pe_ttm_ed` | `pe_ttm_ed` | `pe_ttm_ed` |
| `pb_mrq` | decimal(20,4) NULL | 市净率 PB(MRQ) | `pb_mrq` | `pb_mrq` | `pb_mrq` |
| `pcf_ttm_ed` | decimal(20,4) NULL | 市现率 PCF(经营现金流TTM) | `pcf_ttm_ed` | `pcf_ttm_ed` | `pcf_ttm_ed` |
| `ps_ttm_ed` | decimal(20,4) NULL | 市销率 PS(TTM) | `ps_ttm_ed` | `ps_ttm_ed` | `ps_ttm_ed` |
| `tmv_rmb` | decimal(20,4) NULL | 总市值（人民币） | `tmv_rmb` | `tmv_rmb` | `tmv_rmb` |
| `cir_tmv` | decimal(20,4) NULL | 流通市值；仅 A 股有 | `cir_tmv` | —（该源无此列→NULL） | —（该源无此列→NULL） |
| `tmv_hkd` | decimal(20,4) NULL | 总市值（港币）；A 股无 | —（该源无此列→NULL） | `tmv_hkd` | `tmv_hkd` |
| `tmv_usd` | decimal(20,4) NULL | 总市值（美元）；A 股无 | —（该源无此列→NULL） | `tmv_usd` | `tmv_usd` |
| `org_id` | varchar(255) NULL | 机构ID；仅港股源有 | —（该源无此列→NULL） | `org_id` | —（该源无此列→NULL） |
| `org_name` | varchar(255) NULL | 公司名称；仅港股源有 | —（该源无此列→NULL） | `name_cn` | —（该源无此列→NULL） |
| `etl_time` | datetime | GDF 写入时间（默认 CURRENT_TIMESTAMP） | — | — | — |

键：PK=(`src_table`,`src_dwd_id`)；普通索引 `sec_id`、`dt`、`market`。业务自然键是否唯一以验收抽检为准（OPEN-FIN-02）。

<!-- END GEN §3 -->

---

## 4. `org_id` 与企业主档的关系

金融表的 `org_id` 是供应方机构 ID，原样落库。

| 场景 | 处理 |
|---|---|
| 上市公司 `org_id` 能在 `enterprise_base.org_id` 找到 | 后加工（`12`）可 JOIN 打通；本包 Wave B **不做**这个 JOIN |
| 找不到（港美股、基金管理人等） | 照常落库，**不丢行**，ADS 里按需标记 |
| 港股 / 美股 `org_id` 形态（样例 `T000163343`）与国内 32 位 hash 不同 | 原样保留，不转换 |

企业包未就绪不阻塞本包任何一张 `fin_*`。

---

## 5. 本期不洗清单

| 源表 | 原因 |
|---|---|
| `dwd_ls_stock_daily_quotation`（4,420,724）、`dwd_hk_sec_daily_quotation`（786,781）、`dwd_us_sec_daily_quotation`（1,194） | 日行情大表，当前没有消费方指标。v1.1 视需求再出明细（`00` §3） |
| `dwd_option_daily_quotation`、`dwd_option_basic_info`、`dwd_foreign_exchange_info` | 同上；外汇另与 MACRO 包口径对齐后再议 |
| `dwd_fund_basic_info`、`dwd_fund_equity_sector_allocation`、`dwd_fund_bond_allocation` | live 0 行；供应方补数前不洗。`M_INNOV_PG_FUND` 调研已确认补贴资助类也无表，禁止拿项目资助额冒充 |
| `dwd_org_financing_info`、`dwd_org_invest_info`、`dwd_org_merger_acquisition_info` | 归 ENT-v4（见 §0） |
| 任何 `*_bak_*` | 供应方备份，不贴不洗 |

---

## 6. 开放项

| 编号 | 问题 | 默认处理 | 谁关 |
|---|---|---|---|
| OPEN-FIN-02 | 自然键（`org_id` / `sec_id` / `industrial_fund_id` / `bond_code` 等）在源内是否唯一 | 不去重，主键用 `src_dwd_id`；验收登记各表自然键重复数 | GDF 回签 + data-agent |
| OPEN-FIN-03 | `fin_industrial_fund_lp.sub_capital` / `lp_real_capital`、`fin_industrial_fund_inv_summary.cum_inv_amount` 的金额单位 | 原样保留，不换算；ADS 汇总时标 `unit_unconfirmed` | 供应方答复 |
| OPEN-FIN-04 | `occur_period` 在 Excel 标「日期」，样例 `202603` | 用 varchar 原样落，不转 date | 供应方答复 |
| OPEN-FIN-05 | live 结构与行数报告是否一致（`t_id`、`dwd_corp_basic_info` 16 列、`funding_amount` 类型等） | 以 live 为准 | GDF 开工前核对 |

OPEN-FIN-01 / 06 ~ 10 见 `00` §7。

---

## 7. 验收抽检（Wave B）

1. 每张目标表 ≥20 条抽样，附源行对照（`src_dwd_id` 可回查）。
2. 行数对账：非联合表 `目标行数 = 源 ODS 行数`；联合表 `目标行数 = Σ 各源 ODS 行数`。差异必须有书面原因，不得靠丢行对齐。
3. `fin_industrial_fund.reg_capital_wan` 解析成功数 / 失败数；失败里外币行数。
4. 联合表每个字面量（`src_table` / `class_system` / `dim_type` / `market` / `bond_class`）都有行。
5. 自然键重复数（OPEN-FIN-02）。
6. 禁止出现把 `--` 或空串写成 0 的数值列。
