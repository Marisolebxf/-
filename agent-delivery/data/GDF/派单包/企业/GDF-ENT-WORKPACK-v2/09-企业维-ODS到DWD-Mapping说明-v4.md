# 企业维 ODS → 项目 DWD Mapping 说明（v4）

> **版本**：v4（2026-08-13）— **WORKPACK-v2 正式 Mapping 输入**（字段矩阵继承 v3 + DDL 纠偏）  
> **读者**：GDF 产线（配置 Mapping / ETL）；本侧 data-agent / 架构师  
> **ODS 层**：`gkxlumenx_ods`（Wave A 贴源后的承诺表）  
> **DWD 层**：MySQL **`gkxlumenx_dwd`**（**建表 / 列结构只认本包 [`10-DWD-MySQL-DDL/`](10-DWD-MySQL-DDL/)**：工商 v3.1 + 风险/模块 v3.0 + 指标 v3.1）  
> **承诺表真源**：`third-party-source/doc/`（`md-extract`）  
> **作废施工**：Mapping v2/v3 单独文件、WORKPACK-v1 错误 DWD 指针、PG `demo_gdf_data`、宽表 `enterprise`、`三方参考-DWD标准表结构清单`

---

## 相对 v3 的 DDL 差集（必读）

| # | 项 | 要求 |
|---|-----|------|
| 1 | 建表真源 | 只认 `10/`；**禁止**再打开旧 `DWD表结构设计-企业模块.md`（PG）或三方参考 9 表清单 |
| 2 | 企业主表 | **`enterprise_base`**，不是宽表 `enterprise` |
| 3 | 主键 | 目标表 `id bigint AUTO_INCREMENT`（见 `10/`） |
| 4 | `enterprise_industry_chain.org_id` | 列须存在且可空；现网历史行可全 NULL；**禁止**按空信用代码自造 org_id 回填 |
| 5 | `enterprise_financing` | 保持 `finance_round` / `amount` / `currency` / `investors` / `event_date` 契约，勿另起列名 |
| 6 | `enterprise_base2` | **勿建**；已删除孤立表 |
| 7 | 风险 `org_id` collation | `utf8mb4_general_ci`，与 `enterprise_base.org_id` 一致 |
| 8 | 目标库 | 正式 `gkxlumenx_dwd`；**不写** `demo_gkxlumenx_*` |

字段映射表（下文 §2–§7）与 v3 相同，施工时列名以 **`10/` 快照 + 贴源后 ODS DDL** 为准微调。

---

## 0. 图例与施工顺序

| 标记 | 含义 |
|------|------|
| ✅ | 直接映射（取值或简单类型转换） |
| 🔧 | 需计算 / 多源合并 / 单位换算 / 枚举规则 |
| ⚠️ | 待确认（字段语义或业务规则） |
| ❌ | 本波承诺表无源（缺口；勿硬编） |
| 🟦 | 系统填充（主键序列、ETL 时间戳等） |

**建议 ETL 顺序（本包）**

1. `enterprise_base` ← `dwd_org_base_info`（+ stock 推导上市）  
2. `enterprise_extra` ← base_info + product + stock  
3. `enterprise_finance_history` ← annual + stock_finance  
4. `enterprise_executive` / `enterprise_news`  
5. `enterprise_bid` ← `dwd_bid_*_out`  
6. `enterprise_industry_chain` ← `dwd_org_industry_tags` + `dwd_industry_chain_info`（+ product_tags）  
7. `risk_*`（承诺子集）  
8. 港澳台 / 高校 / 科研（落点见 §6，契约待补则先贴源不洗）  

**过滤**：源侧默认 `is_deleted = 0`（有该列时）。

---

## 1. 表级总览（本波可施工）

| # | 项目 DWD 表 | 承诺 ODS 主源 | 覆盖 | 说明 |
|---|-------------|---------------|------|------|
| 1 | enterprise_base | dwd_org_base_info | 高 | 主数据；**不用** reg_info / company_base |
| 2 | enterprise_extra | dwd_org_base_info + org_product + stock_base | 中 | 部分原 company_* 字段 ❌ |
| 3 | enterprise_finance_history | annual_financial + stock_finance | 高 | |
| 4 | enterprise_executive | dwd_org_executive_info | 高 | |
| 5 | enterprise_news | dwd_org_important_news_info | 高 | |
| 6 | enterprise_bid | dwd_bid_base_out + win/agency/target | 中 | 替代 org_bid_info |
| 7 | enterprise_industry_chain | dwd_org_industry_tags + industry_chain_info | 中 | 替代 chain_dtl；字段名以贴源 DDL 为准 |
| 8 | risk_abnormal 等（§5） | 承诺风险子集 | 中 | 非 live 全套司法 |
| — | enterprise_tag / history_name / patent_* / financing / invest / carrier | — | ❌/另波 | 本波不施工或缺口 |

---

## 2. enterprise_base（← dwd_org_base_info）

目标库：`gkxlumenx_dwd.enterprise_base`（DDL 见 `10/` 工商 v3.1；源表名已按承诺纠正）

| # | DWD 字段 | 映射 | 承诺 ODS | 逻辑/备注 |
|---|----------|------|----------|-----------|
| 1 | id | 🟦 | — | 自增 |
| 2 | org_id | ✅ | dwd_org_base_info.org_id | 业务主键 |
| 3 | enterprise_code | ✅ | external_id | 统一社会信用代码 |
| 4 | enterprise_name | ✅ | name_cn | |
| 5 | legal_representative | ✅ | lerep | |
| 6 | registration_date | ✅ | incorporation_date | |
| 7 | business_status | 🔧 | reg_status | 枚举归一（在营/注销等）规则启动会确认 |
| 8 | enterprise_type | ✅ | org_type | 原 company_base.first_type ❌ 改用 org_type |
| 9 | industry_category | ✅ | industry 或 industry_l1_name | 优先最深一级 industry，空则 l1_name |
| 10 | industry_code | ✅ | industry_l1_code | |
| 11 | province | ✅ | province | |
| 12 | city | ✅ | city | |
| 13 | district | ✅ | area | 承诺字段名 area |
| 14 | registered_capital | 🔧 | registered_capital_value | **元→万元**（/10000）；注意币种 capital_currency |
| 15 | is_listed | 🔧 | listing_status 或 JOIN stock_base | listing_status 非空/已上市→1；或存在 stock_base 行→1 |
| 16 | org_size | ❌ | — | 承诺 base_info **无** org_size；暂空或二期 |
| 17 | data_source | ✅ | data_source | |
| 18–19 | create_time / update_time | 🟦 | — | ETL 填充（勿直接当业务展示） |

---

## 3. enterprise_extra

| # | DWD 字段 | 映射 | 承诺 ODS | 备注 |
|---|----------|------|----------|------|
| 2 | org_id | ✅ | 同 base | |
| 3 | enterprise_name_en | ❌/⚠️ | special_* / heis.name_en | 大陆主体承诺 base 无 english_name；港澳台/高校可补 |
| 4 | paid_in_capital | ❌ | — | 原 company_base；本波无源 |
| 5 | business_scope | ✅ | dwd_org_org_product_info.main_activities | |
| 6 | registered_address | ✅ | dwd_org_base_info.address | |
| 7 | headquarters_address | 🔧 | address | 默认同注册地址 |
| 8–9 | lng / lat | ✅ | addr_lng / addr_lat | |
| 10–12 | listed_market / listed_code / listed_date | ✅ | stock_base.stock_type / stock_code / listed_date | |
| 13 | contact_phone | ✅ | base_info.phone_num | |
| 14 | contact_email | ✅ | base_info.email | |
| 15–17 | main_activities / main_prod / description | ✅ | org_product_info 同名字段 | |
| 18–19 | stock_noun / listed_status | ✅ | stock_base | |
| 20 | capital_currency_code | ✅ | base_info.capital_currency | 字段名以 DDL 为准 |
| 21 | registration_org | ✅ | registration_org | |
| 22 | postal_code | ✅ | postal_code | |
| 23–24 | start_date / end_date | ✅ | start_date / end_date | 建议清洗为 date |
| 其余系统列 | 🟦 | — | | |

---

## 4. 明细表（高覆盖）

### 4.1 enterprise_finance_history

| DWD 字段 | 映射 | ODS |
|----------|------|-----|
| org_id | ✅ | annual.org_id / stock.org_id |
| data_year | 🔧 | annual.year；stock.occur_period 抽年 |
| revenue 等（万元口径） | 🔧 | operating_revenue 等，**元→万元**（设计 §4.5） |
| main_business_revenue / total_profit / total_fixed_assets | ✅ | annual 对应字段（元口径，见设计注） |
| data_source | 🔧 | `annual` / `stock`；上市优先 stock |

### 4.2 enterprise_executive

| DWD | 映射 | ODS |
|-----|------|-----|
| org_id | ✅ | org_id |
| executive_name | ✅ | executives_name |
| position | ✅ | executives_position |
| data_source | ✅ | data_source |

### 4.3 enterprise_news

| DWD | 映射 | ODS |
|-----|------|-----|
| org_id | ✅ | org_id |
| enterprise_name | ✅ | name_cn |
| news_title / news_date / news_content | ✅ | 同名 |
| original_url | ✅ | original_textlink |

### 4.4 enterprise_bid（← dwd_bid_*_out）

以 `dwd_bid_base_out` 为主，用 `u_id` / `project_number` 关联 win_candidate / purchase_agency / target_item。

| DWD | 映射 | ODS（承诺） |
|-----|------|-------------|
| org_id | 🔧 | win_candidate.org_id 或 base 中标主体字段（以 DDL 为准） |
| enterprise_name | 🔧 | win_candidate.name_cn |
| announcement_title | ✅ | base_out.title |
| announcement_date | 🔧 | base_out.publish_time → date |
| project_name / project_no | ✅ | project_name / project_number |
| winning_amount | 🔧 | target_item 金额字段（单位换算） |
| role | 🔧 | 按主体是中标/采购推导 |
| tender_* | 🔧 | purchase_agency 或 base 采购方字段 |

> 旧设计写 `dwd_org_bid_info.*` **全部作废**，以贴源后四表 DDL 为准微调列名。

### 4.5 enterprise_industry_chain

承诺侧为企业关联表 **`dwd_org_industry_tags`** + 图谱 **`dwd_industry_chain_info`**（另有 product_tags），**不是** `dwd_org_industry_chain_dtl`。

| DWD | 映射 | 说明 |
|-----|------|------|
| org_id / enterprise_code | ✅/🔧 | tags 表 org_id、信用代码列（贴源后确认列名）；**DWD 侧 `org_id` 可空**，禁止自造 org_id |
| chain_code / chain_name | 🔧 | tags JOIN chain_info |
| node_id / node_name / node_stage | 🔧 | 以 tags/product_tags 实际列名为准 |
| is_chain_leader | ⚠️ | 业务规则未定，默认 false |
| chain_score | ⚠️ | 有则映射，无则空 |

---

## 5. 风险表（承诺子集 → risk_*）

| 项目 DWD | 承诺 ODS | 映射 |
|----------|----------|------|
| risk_abnormal | dwd_org_company_abnormal | ✅ 明细直搬（列对齐 DDL） |
| risk_punishment | dwd_org_company_punish | ✅ |
| risk_illegal | dwd_org_company_illegal | ✅ |
| risk_tax_punish | dwd_org_risk_tax_punish | ✅ |
| risk_judicial_case | dwd_org_opt_judicial_case | ✅ |
| risk_dishonest | dwd_org_risk_shixin | ✅ |
| risk_executed | dwd_org_risk_zhixing | ✅ |
| risk_bankruptcy / _party | bankruptcy_public_cases / _list | ✅ |
| enterprise_risk_summary | 上列预聚合 | 🔧 |
| 其余 risk_*（lawsuit/court/pledge…） | — | ❌ 本波不做 |

---

## 6. 本波贴源但不强制洗入核心 enterprise_* 的表

| 承诺 ODS | 建议 |
|----------|------|
| dwd_special_hongkong/taiwan/aomen_company | 先 ODS 验收；DWD 落点待契约（可扩展 enterprise_* 或独立表） |
| dwd_org_heis_info / dwd_research_institute_base_info | 机构扩展；可补 name_en 等 |
| dwd_forg_* / dwd_foreign_org_annual_financial_info | 海外；DWD 契约确认后另作业 |
| dwd_org_changerecord_info / dwd_org_recruit_info | 变更/招聘；无对应核心 enterprise 主路径则 ODS 保留 |
| dwd_industry_chain_news_info | 产业资讯；可进资讯域或暂留 ODS |

---

## 7. 明确缺口（❌ / 另波）

| 项目 DWD / 能力 | 原因 |
|-----------------|------|
| enterprise_history_name | 依赖量子 company_history_name，本波不贴 |
| enterprise_tag / 荣誉资质 facets | 承诺无 org_tag_info / company_*_tags |
| enterprise_patent_* | 专利在另一工作簿，另波 |
| enterprise_financing / invest / innovation_carrier | 承诺国内机构 Sheet 未列 |
| org_size、实缴资本等 | 承诺字段缺失 |

缺口须在 UI/指标侧保留 ⏳/⚠️，**禁止**用假枚举填满。

---

## 8. GDF 交付物（Mapping / ETL）

1. 按本文件配置的字段级 Mapping（中台可导出配置截图或作业清单）  
2. ETL 作业：依赖顺序符合 §0；失败可重跑；按 org_id 幂等  
3. 调度：建议 **Wave A P0 镜像成功 → 触发 §1 表 1–7**；风险 P1 可随后  
4. 抽样对账：每张 DWD 表 ≥20 条 org_id 与 ODS 一致  
5. 列名以 **贴源后** `gkxlumenx_ods` 实际 DDL 微调时，回写差异表给本侧  

---

## 9. 参考路径

| 材料 | 路径 |
|------|------|
| 本说明（工作包） | `GDF/派单包/企业/GDF-ENT-WORKPACK-v2/09-企业维-ODS到DWD-Mapping说明-v4.md` |
| DWD 建表快照 | 本包 `10-DWD-MySQL-DDL/` |
| 作废对照 | 本包 `11-作废与误源对照.md` |
| Mapping 目录历史副本 | `GDF/Mapping/企业/企业相关-ODS到DWD字段映射分析报告(v3).md`（**勿单独施工**；以本 `09` v4 为准） |
| 承诺字段 CSV | `third-party-source/doc/md-extract/_csv/` |
| Wave A 表清单 | `02-WaveA-贴源表清单.yaml` |
