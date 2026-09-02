> **【GDF-ENT-WORKPACK-v3.0 · Mapping 施工真源】** 日期 2026-09-02。  
> 基线来源：`agent-delivery/data/data-design/企业/企业域-ETL-Mapping明细-源表到DWD.md`（v1.2）；本包按监管人确认增加财务万元门禁、live 核验和港澳台本期范围。  
> 旧短版 `09-企业维-ODS到DWD-Mapping说明-v4.md` **仅作导读**，字段级施工 **只认本文件**。  
> **本叶复核范围（诚实）**：只复核 `00` §8 七项（财务万元、`chain_dtl`/`industry_tags`、融资表在 `gkx`、专利多角色+`patent_org_rel`、`05` 重出、OPEN-FLOW 独立、港澳台+`region_id`）。其余字段映射 **继承 v1.2，未逐字段复验**；与 live 冲突以 `13` ADD-不-DROP 为准，禁止假装 48 张表已对完。

---
# 企业域 ETL Mapping 明细 — 源表到 DWD

> **版本**：v3.0（继承 v1.2；复核范围见上文）
> **日期**：2026-09-02
> **范围**：GDF 三方源表（`dwd_org_*` / `dwd_patent*`）→ 项目 DWD（`gkxlumenx_dwd.enterprise_*` / `risk_*`）的字段级映射
> **配套文档**：`企业域-数据ETL流转架构.md`（架构总纲）、`DWD表结构设计-企业工商表-MySQL-v3.1.md`（目标表 DDL）
> **目标库**：`gkxlumenx_dwd`（MySQL 8.0，192.168.88.43:3306）
> **交付对象**：GDF 三方 ETL 团队

---

## 1. 映射分类说明

| 类型 | 说明 | 示例 |
|---|---|---|
| **直接映射** | 源表字段直接写入目标表对应字段，仅做类型/命名转换 | `org_id → org_id`、`name_cn → enterprise_name` |
| **关联映射** | 需要通过企业名/信用代码关联其他表获取字段（如 org_id） | 专利 `current_assignee` → 关联 `enterprise_base.enterprise_name` → 获取 `org_id` |
| **指标表** | 需要通过 SQL 聚合计算（COUNT/SUM）生成 | 按 `org_id + risk_type` 聚合各风险表 COUNT → `enterprise_risk_summary` |

### 1.1 org_id 复用规则

**源表的 `org_id` 直接复用为目标表的 `org_id`**，不重新生成。三方源表 `dwd_org_*` 里的 `org_id` 字段就是项目 DWD 需要的业务主键。

### 1.2 企业名关联规则

专利源没有企业 `org_id`，需要将所有企业角色名称与机构主档精确匹配：

- 首位名称：`dwd_patent.first_applicant_name` / `first_current_assignee_name`
- 完整名单：`dwd_patent_applicants.name` / `dwd_patent_assignees.name`（按 `patent_id + sequence`）
- 国内：名称 → JOIN `dwd_org_base_info.name_cn` → 取得**既有** `org_id`
- 国外：名称 → JOIN 国外机构主档名称 → 取得**既有** `org_id`
- 一件专利可对应多个企业，写 `enterprise_patent_org_rel`，保存角色和顺序；未命中名称进入待治理清单，禁止生成新 `org_id`

### 1.3 产业链 org_id 关联

2026-09-02 live 核验：`dwd_org_industry_chain_dtl` 在 `gkx` 及当前可见 schema 中不存在，不能作为本期施工输入。先用 `dwd_org_industry_tags.credit_code` 关联 `enterprise_base.enterprise_code` 获取 `org_id`，并映射其产业 / 环节字段；同时继续向供应方索取或核实 `chain_dtl` 实名。`industry_tags` 不含 `chain_score` / `segment_key`，对应目标字段保持 NULL，禁止伪造。

### 1.4 国内外机构分库分索引

**DWD 分两套表**：国内 `enterprise_*`（现有 21 张，含新增 `enterprise_recruit`）+ 国外 `enterprise_forg_*`（新建）。org_id 不会冲突。

**ES 分两个索引 + 同一个别名**：

```
别名 gkx_enterprise
  ├── gkx_enterprise_v1        (国内 2500 万，IK 分词)
  └── gkx_enterprise_global_v1 (国外 3000 万，standard 分词)
```

- mapping 结构完全一致（字段名/类型/nested 相同），只是分词器不同
- 查询代码走别名，ES 自动 fan-out 到两个索引
- 用户选择"美国+中国"地区范围时，按 `country_code` 做 `terms` 过滤
- 国内由 ETL 统一写 `country_code = CHN`，并继续使用 `region_id`；国外索引填各自国家代码
- `region_scope` 表已有全球/国家体系（`global` → `global-all` → G20 国家，`bind_country_code` = ISO alpha-3）

### 1.5 name_en 字段说明

ES mapping 新增 `name_en` 字段（text + standard 分词 + keyword 子字段），用于国外机构名称搜索：

| 索引 | `name_cn` | `name_en` |
|---|---|---|
| cn（国内） | 中文名（IK + 拼音 + suggest） | 英文名或 NULL（来自 `enterprise_extra.enterprise_name_en`） |
| global（国外） | 本地名称/别名（standard，可能含中文/日文/韩文） | 英文名（standard，主名称） |

搜索时 `name_cn` 和 `name_en` 是 OR 关系——keyword 搜索同时匹配两个字段，任一命中即可。

---

## 2. 源表 → 目标表对应总览

### 2.1 直接映射（20 条）

| # | 源表 | 目标表 | 说明 |
|---|---|---|---|
| 1 | `dwd_org_base_info` | `enterprise_base` + `enterprise_extra` | 37 字段拆分到两张表 |
| 2 | `dwd_org_executive_info` | `enterprise_executive` | 直接映射 |
| 3 | `dwd_org_org_product_info` | `enterprise_extra`（部分字段） | 经营范围/产品/描述补充到 extra |
| 4 | `dwd_org_annual_financial_info` | `enterprise_finance_history` | 期间指标 + 年末存量 assets/liabilities |
| 5 | `dwd_org_important_news_info` | `enterprise_news` | 直接映射 |
| 6 | `dwd_org_stock_base` | `enterprise_extra`（上市字段）+ `enterprise_base`（is_listed） | 上市信息合并 |
| 7 | `dwd_org_company_abnormal` | `risk_abnormal` | 直接映射 |
| 8 | `dwd_org_company_punish` | `risk_punishment` | 直接映射 |
| 9 | `dwd_org_company_illegal` | `risk_illegal` | 直接映射 |
| 10 | `dwd_org_risk_tax_punish` | `risk_tax_punish` | 直接映射 |
| 11 | `dwd_org_opt_judicial_case` | `risk_judicial_case` | 直接映射 |
| 12 | `dwd_org_risk_shixin` | `risk_dishonest` | 直接映射 |
| 13 | `dwd_org_risk_zhixing` | `risk_executed` | 直接映射 |
| 14 | `dwd_org_bankruptcy_public_cases` | `risk_bankruptcy` | 直接映射 |
| 15 | `dwd_org_bankruptcy_public_cases_list` | `risk_bankruptcy_party` | 直接映射 |
| 16 | `dwd_org_financing_info` | `enterprise_financing` | 直接映射 |
| 17 | `dwd_org_invest_info` | `enterprise_invest` | 直接映射 |
| 18 | `dwd_org_tag_info` | `enterprise_tag` | 直接映射 |
| 19 | `dwd_org_subsidiary_info` | `enterprise_parent_subsidiary` | 直接映射 |
| 20 | `dwd_org_recruit_info` | `enterprise_recruit` | 招聘信息（新建表） |

### 2.2 关联映射（8 条）

| # | 源表 | 目标表 | 关联逻辑 |
|---|---|---|---|
| 1 | `dwd_org_changerecord_info` | `enterprise_history_name` | 仅取 `update_content` 含"名称"的行，`current_name` → `history_name` |
| 2 | `dwd_org_stock_finance_info` | `enterprise_finance_history`（补充） | 按业务含义选取字段，`occur_period` 解析为 `data_year` |
| 3 | `dwd_org_shareholder_info` | `enterprise_supply_chain`（投资方部分） | `owners_name` → `related_name`，`inv_org_id` → `related_org_id` |
| 4 | `dwd_bid_win_candidate_out` | `enterprise_bid` | 通过 `org_id` 直接关联（源表已有 org_id） |
| 5 | `dwd_bid_base_out` | `enterprise_bid`（公告信息补充） | 通过 `u_id` 关联中标表 |
| 6 | `dwd_patent` + applicants/assignees 分表 | `enterprise_patent_detail` + `enterprise_patent_org_rel` | 所有申请人/权利人名称精确匹配企业主档；关系表保留角色与顺序 |
| 7 | `dwd_patent` | `enterprise_chain_patent` | IPC → 产业链映射 + `assignee` → `org_id` |
| 8 | `dwd_org_industry_tags` | `enterprise_industry_chain` | `credit_code` → JOIN `enterprise_base.enterprise_code` → `org_id`；产业/环节字段直接映射 |

### 2.3 指标表（4 条）

| # | 源 | 目标表 | 聚合逻辑 |
|---|---|---|---|
| 1 | `dwd_patent` | `enterprise_patent_history` | 按 `org_id + filing_year` 聚合 COUNT |
| 2 | 多张 `risk_*` 表 | `enterprise_risk_summary` | 按 `org_id + risk_type` 聚合 COUNT |
| 3 | `enterprise_base` | `enterprise_region_summary` | 按 `region_id + stat_date` 聚合 COUNT |
| 4 | `enterprise_base` + `enterprise_industry_chain` | `enterprise_industry_summary` | 按 `chain_code + stat_year` 聚合 |

### 2.4 暂不映射（4 条）

| 源表 | 原因 |
|---|---|
| `dwd_org_heis_info`（高校基本信息） | 非企业域范围 |
| `dwd_research_institute_base_info`（科研机构） | 非企业域范围 |
| `dwd_org_merger_acquisition_info`（并购事件） | 目标侧暂无并购表 |
| `dwd_bid_purchase_agency_out` / `dwd_bid_target_item_out` | 采购代理/标的物不在企业域范围 |

### 2.5 国外机构映射（6 条）

| # | 源表 | 目标表 | 说明 |
|---:|---|---|---|
| 1 | `dwd_forg_base_info` | `enterprise_forg_base` + `enterprise_forg_extra` | 主数据拆分 |
| 2 | `dwd_forg_product_info` | `enterprise_forg_extra` | 经营/产品/描述 |
| 3 | `dwd_forg_executive_info` | `enterprise_forg_executive` | 高管信息 |
| 4 | `dwd_forg_shareholder_info` | `enterprise_forg_invest` | 股东/投资 |
| 5 | `dwd_foreign_org_annual_financial_info` | `enterprise_forg_finance_history` | 财务历史 |
| 6 | `dwd_forg_subsidiary_info` | `enterprise_forg_parent_subsidiary` | 母子公司 |

---

## 3. 逐表字段映射明细

### 3.1 `dwd_org_base_info` → `enterprise_base` + `enterprise_extra`

源表 37 字段拆分到两张目标表。

#### 3.1.1 → `enterprise_base`（工商基础信息，21 字段）

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `org_id` | `org_id` | 直接 | 复用源 org_id |
| `external_id` | `enterprise_code` | 直接 | 统一社会信用代码 |
| `name_cn` | `enterprise_name` | 直接 | 企业名称 |
| `lerep` | `legal_representative` | 直接 | 法定代表人 |
| `incorporation_date` | `registration_date` | 直接 | 成立日期 |
| `reg_status` | `business_status` | 直接 | 经营状态 |
| `org_type` | `enterprise_type` | 直接 | 企业类型 |
| `industry_l4_name` | `industry_category` | 直接 | 取最深级行业名称 |
| `industry_l4_code` | `industry_code` | 直接 | 取最深级行业编码 |
| `province` | `province` | 直接 | 省份 |
| `city` | `city` | 直接 | 地市 |
| `area` | `district` | 直接 | 区县 |
| `province` + `city` + `area` | `region_id` | 维表绑定 | 关联 `gkxlumenx_dim.code_region` 取 6 位国标行政区划码；无法唯一绑定则 NULL + 待治理 |
| `registered_capital_value` | `registered_capital` | 直接 | 注册资本（万元；源表是元，需 ÷10000） |
| `listing_status` | `is_listed` | 转换 | 文本"上市"→1，其他→0/NULL |
| `org_size` | `org_size` | 直接 | 企业规模 |
| `data_source` | `data_source` | 直接 | 数据来源 |
| `created_time` | `create_time` | 直接 | 创建时间 |
| `updated_time` | `update_time` | 直接 | 更新时间 |
| — | `id` | 自增 | bigint AUTO_INCREMENT |
| `industry` | — | 不映射 | 用 industry_l4_name 替代 |

> ⚠️ **注册资本单位**：源表 `registered_capital_value` 单位是"元"，目标表 `registered_capital` 注释是"万元"。映射时需 ÷10000。

#### 3.1.2 → `enterprise_extra`（企业扩展信息，19 字段）

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `org_id` | `org_id` | 直接 | 复用源 org_id |
| `address` | `registered_address` | 直接 | 注册地址 |
| `addr_lng` | `lng` | 直接 | 经度 |
| `addr_lat` | `lat` | 直接 | 纬度 |
| `postal_code` | `postal_code` | 直接 | 邮政编码 |
| `email` | `contact_email` | 直接 | 电子邮箱 |
| `phone_num` | `contact_phone` | 直接 | 联系电话 |
| `registration_org` | `registration_org` | 直接 | 登记机关 |
| `start_date` | `start_date` | 直接 | 经营期限自 |
| `end_date` | `end_date` | 直接 | 经营期限至 |
| `capital_currency` | `capital_currency_code` | 直接 | 币种 |
| `incorporation_year` | — | 不映射 | 可从 registration_date 推导 |
| `listing_status` | `listed_status` | 直接 | 上市状态描述 |
| `listing_date` | `listed_date` | 直接 | 上市日期 |
| `dwd_org_stock_base.stock_code` | `listed_code` | 关联 | 从上市表补充 |
| `dwd_org_stock_base.stock_noun` | `stock_noun` | 关联 | 从上市表补充 |
| `dwd_org_stock_base.stock_type` | `listed_market` | 关联 | 从上市表补充（上市板块） |
| `dwd_org_org_product_info.main_activities` | `main_activities` | 关联 | 从经营信息表补充 |
| `dwd_org_org_product_info.main_prod` | `main_prod` | 关联 | 从经营信息表补充 |
| `dwd_org_org_product_info.description` | `description` | 关联 | 从经营信息表补充 |

### 3.2 `dwd_org_executive_info` → `enterprise_executive`

| 源字段 | 目标字段 | 映射类型 |
|---|---|---|
| `org_id` | `org_id` | 直接 |
| `executives_name` | `executive_name` | 直接 |
| `executives_position` | `position` | 直接 |
| `data_source` | `data_source` | 直接 |

### 3.3 `dwd_org_annual_financial_info` → `enterprise_finance_history`

源表含 `total_assets` / `total_liabilities`。目标表期间指标 + 年末时点存量；存量不与收入同维解读，供 ES 取最新一年。

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `org_id` | `org_id` | 直接 | |
| `year` | `data_year` | 直接 | 年报年度 |
| `operating_revenue` | `revenue` | 条件转换 | 营业收入；目标统一万元，按下方门禁换算 |
| `main_business_revenue` | `main_business_revenue` | 条件转换 | 主营业务收入；目标统一万元，按下方门禁换算 |
| `total_profit` | `total_profit` | 条件转换 | 利润总额；目标统一万元，按下方门禁换算 |
| `total_fixed_assets` / `fixed_assets` | `total_fixed_assets` | 条件转换 | 固定资产总额；目标统一万元，按下方门禁换算 |
| `total_assets` | `total_assets` | 条件转换 | 年末资产总额；目标统一万元，按下方门禁换算 |
| `total_liabilities` | `total_liabilities` | 条件转换 | 年末负债总额；目标统一万元，按下方门禁换算 |
| `data_source` | `data_source` | 直接 | |

> **财务单位门禁（2026-09-02 `human:徐滕强` 确认）**：目标统一为**万元**。GDF 在配置转换前必须核对 live 字段注释、原始值文本和代表性样本并在验收表留证；源明确为元时 ÷10000，源明确为万元时原值写入。仅凭数值大小无法判定单位时立即报阻塞，禁止猜单位或直接写入。

### 3.4 `dwd_org_stock_finance_info` → `enterprise_finance_history`（补充）

上市企业财务指标有更丰富的字段（净利润、研发投入、从业人数等），按目标表已有字段选取补充：

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `org_id` | `org_id` | 直接 | |
| `occur_period` | `data_year` | 转换 | 如 "2023-12-31" → 2023 |
| `operating_revenue` | `revenue` | 转换 | ÷10000（元→万元） |
| `main_business_revenue` | `main_business_revenue` | 转换 | ÷10000 |
| `total_profit` | `total_profit` | 转换 | ÷10000 |
| `fixed_assets` | `total_fixed_assets` | 转换 | ÷10000 |
| `total_assets` | `total_assets` | 转换 | 年末资产总额；÷10000（元→万元） |
| `total_liabilities` | `total_liabilities` | 转换 | 年末负债总额；÷10000（元→万元） |
| `data_source` | `data_source` | 直接 | |

> 净利润 / 研发投入等其余源字段仍不进国内目标表。`total_assets` / `total_liabilities` 为年末时点存量，ES 取最新一年，不与收入逐年同维。

### 3.5 `dwd_org_important_news_info` → `enterprise_news`

| 源字段 | 目标字段 | 映射类型 |
|---|---|---|
| `org_id` | `org_id` | 直接 |
| `name_cn` | `enterprise_name` | 直接 |
| `news_title` | `news_title` | 直接 |
| `news_date` | `news_date` | 直接 |
| `news_content` | `news_content` | 直接 |
| `original_textlink` | `original_url` | 直接 |

### 3.6 `dwd_org_changerecord_info` → `enterprise_history_name`（关联映射）

**仅取变更类型含"名称"的行**：

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `org_id` | `org_id` | 直接 | |
| `current_name` | `history_name` | 直接 | 变更前内容 = 曾用名 |
| `update_date` | `start_date` | 直接 | 变更日期 = 曾用名起始 |
| `update_name` | — | 不映射 | 变更后内容 = 现用名（已在 base 表） |

过滤条件：`WHERE update_content LIKE '%名称%'`

### 3.7 `dwd_org_financing_info` → `enterprise_financing`

| 源字段 | 目标字段 | 映射类型 |
|---|---|---|
| `org_id` | `org_id` | 直接 |
| `funding_round` | `finance_round` | 直接 |
| `funding_amount` | `amount` | 直接 |
| `funding_currency_code` | `currency` | 直接 |
| `investors_name` | `investors` | 直接 |
| `completion_date` | `event_date` | 直接 |

### 3.8 `dwd_org_invest_info` → `enterprise_invest`

| 源字段 | 目标字段 | 映射类型 |
|---|---|---|
| `org_id` | `org_id` | 直接 |
| `inv_org_id` | `inv_org_id` | 直接 |
| `inv_name` | `inv_name` | 直接 |
| `inv_external_id` | `inv_external_id` | 直接 |
| `investment_amount` | `investment_amount` | 直接 |
| `investment_ratio` | `investment_ratio` | 直接 |
| `data_source` | `data_source` | 直接 |

### 3.9 `dwd_org_tag_info` → `enterprise_tag`

源表以实际 live DDL `gkxlumenx_ods.dwd_org_tag_info` 为准，字段含 `org_id` / `name_cn` / `external_id` / `org_tag` / `tag_level` / `created_time` / `updated_time` / `is_deleted` 等；过滤 `is_deleted = 0` 才入 DWD。

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `org_id` | `org_id` | 直接 | |
| `org_tag` | `tag_code` | 直接 | 标签编码 |
| `org_tag` → JOIN `gkxlumenx_dwd.tag_dict` | `tag_name` | 字典反查 | 按 `tag_dict.tag_code = org_tag` 取 `tag_name` |
| `org_tag` → JOIN `gkxlumenx_dwd.tag_dict` | `tag_category` | 字典反查 | 按 `tag_dict.tag_code = org_tag` 取 `tag_category` |
| `tag_level` | — | 不映射 | 目标 `enterprise_tag` 无 `tag_level` 字段；`tag_dict.tag_level` 已按 `tag_code` 维护 |
| `tag_value` | — | 待细化 | 普通标签默认 NULL；荣誉/级别类标签的展示值后续按规则生成 |
| `created_time` | `create_time` | 直接 | 创建时间 |
| `updated_time` | `update_time` | 直接 | 更新时间 |
| — | `tag_score` | 源无 | 默认 NULL；后续如需评分来源再回填 |
| — | `id` | 自增 | bigint AUTO_INCREMENT |
| `name_cn` / `external_id` | — | 不映射 | 目标表无对应字段 |
| `is_deleted` | — | 不映射 | 仅作为过滤条件 |

### 3.10 `dwd_org_subsidiary_info` → `enterprise_parent_subsidiary`

| 源字段 | 目标字段 | 映射类型 |
|---|---|---|
| `org_id` | `org_id` | 直接（母公司） |
| `sub_org_id` | `parent_org_id` | 直接 |
| `sub_name_cn` | `parent_enterprise_name` | 直接 |

### 3.11 `dwd_org_shareholder_info` → `enterprise_supply_chain`（投资方部分）

股东信息映射为供应链关系中的投资方关系：

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `org_id` | `org_id` | 直接 | 被投资企业 |
| `inv_org_id` | `related_org_id` | 直接 | 股东/投资方 |
| `owners_name` | — | 不映射 | 目标表无 name 字段 |
| `owners_type` | `relation_type` | 转换 | 股东类型 → 关系类型 |
| `ownership_percentage` | `relation_strength` | 转换 | 占比 → 关系强度 |

### 3.12 `dwd_bid_win_candidate_out` → `enterprise_bid`

| 源字段 | 目标字段 | 映射类型 |
|---|---|---|
| `org_id` | `org_id` | 直接 |
| `name_cn` | `enterprise_name` | 直接 |
| `project_name` | `announcement_title` | 直接（映射为公告标题） |
| `external_id` | — | 不映射 |
| `bid_item_name` | — | 补充到公告标题 |

### 3.13 风险类表字段级映射（9 张）

> 公共规则：
> - 过滤条件：`is_deleted = 0` 才入 DWD。
> - 企业名称：`name_cn` → `org_name`；司法案件源表用 `company_name`，同样映射为 `org_name`。
> - 时间字段：`created_time` → `create_time`；`updated_time` → `update_time`。
> - 业务 ID：源表已有的 `case_id` / `abnormal_id` / `penalty_id` / `sv_id` / `tax_vio_id` / `dishonest_id` / `exec_person_id` 直接复用；源表无唯一业务 ID 的目标 NOT NULL 字段按下方说明生成或待三方确认。
> - `is_history`：能由业务字段推导的写推导规则；无法推导的默认 0，并在转换说明注明。

#### 3.13.1 `dwd_org_company_abnormal` → `risk_abnormal`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `abnormal_id` | `case_id` | 直接复用业务 ID |
| `org_id` | `org_id` | 直接复用 |
| `name_cn` | `org_name` | 机构名称 |
| `abn_reason` | `reason` | 列入原因 |
| `abn_org` | `decision_org` | 列入机关 |
| `abn_date` | `abn_date` | 列入时间 |
| `remove_date` | `remove_date` | 移出时间 |
| `status` | `status` | 状态 |
| `remove_date` | `is_history` | 推导：`remove_date IS NOT NULL` → 1，否则 0 |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `id` | 自增主键 |
| `pk_id` / `external_id` / `remove_reason` / `remove_org` / `use_flag` | — | 不映射 |
| `creater` / `updater` / `table_data_source` / `is_deleted` | — | 不映射；`is_deleted` 仅作为过滤条件 |

#### 3.13.2 `dwd_org_company_punish` → `risk_punishment`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `penalty_id` | `case_id` | 直接复用业务 ID |
| `org_id` | `org_id` | 直接复用 |
| `name_cn` | `org_name` | 机构名称 |
| `decision_no` | `doc_no` | 决定书文号 |
| `violation_fact` | `reason` | 主要违法事实；如业务要求合并违法行为类型/处罚内容，需另行确认 |
| `fine_amount` | `fine_amount` | 罚款金额 |
| `confiscate_amount` | `confiscate_amount` | 没收金额 |
| `decision_org` | `decision_org` | 决定机关 |
| `penalty_date` | `penalty_date` | 处罚决定日期 |
| `public_date` | `public_date` | 公示日期 |
| `status` | `status` | 状态 |
| 源无 | `is_history` | 源表无字段且无可推导业务字段，默认 0 |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `id` | 自增主键 |
| `pk_id` / `external_id` / `violation_type` / `penalty_content` / `penalty_basis` / `penalty_type` / `license_info` / `validity_period` / `public_deadline` / `remark` / `use_flag` | — | 不映射 |
| `creater` / `updater` / `table_data_source` / `is_deleted` | — | 不映射；`is_deleted` 仅作为过滤条件 |

#### 3.13.3 `dwd_org_company_illegal` → `risk_illegal`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `sv_id` | `case_id` | 直接复用业务 ID |
| `org_id` | `org_id` | 直接复用 |
| `name_cn` | `org_name` | 机构名称 |
| `abn_reason` | `reason` | 列入原因 |
| `abn_org` | `decision_org` | 列入机关 |
| `abn_date` | `abn_date` | 列入时间 |
| `remove_date` | `remove_date` | 移出时间 |
| `status` | `status` | 状态 |
| `remove_date` | `is_history` | 推导：`remove_date IS NOT NULL` → 1，否则 0 |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `id` | 自增主键 |
| `pk_id` / `external_id` / `category` / `remove_reason` / `remove_org` / `use_flag` | — | 不映射 |
| `creater` / `updater` / `table_data_source` / `is_deleted` | — | 不映射；`is_deleted` 仅作为过滤条件 |

#### 3.13.4 `dwd_org_risk_tax_punish` → `risk_tax_punish`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `tax_vio_id` | `case_id` | 直接复用业务 ID |
| `org_id` | `org_id` | 直接复用 |
| `illegal_fact` | `reason` | 主要违法事实 |
| `case_type` | `tax_vio_type` | 案件性质 → 税收违法类型，语义待字典确认 |
| `publish_date` | `publish_date` | 发布日期 |
| `is_history` | `is_history` | 源 varchar `0/1` → tinyint |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `case_no` | 默认 NULL |
| 源无 | `amount` | 默认 NULL（源表无罚款金额） |
| 源无 | `status` | 默认 NULL |
| 源无 | `id` | 自增主键 |
| `pk_id` / `taxpayer_name` / `name_cn` / `external_id` / `report_period` / `taxpayer_id` / `org_code` / `reg_address` / `legal_name` / `legal_gender` / `legal_id_type` / `legal_id_no` / `finance_name` / `finance_gender` / `finance_id_type` / `finance_id_no` / `agency_info` / `punish_basis` / `tax_authority` / `original_link` / `use_flag` / `original_source` | — | 不映射 |
| `creater` / `updater` / `table_data_source` / `is_deleted` | — | 不映射；`is_deleted` 仅作为过滤条件 |

#### 3.13.5 `dwd_org_opt_judicial_case` → `risk_judicial_case`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `case_id` | `case_id` | 直接复用业务 ID |
| `org_id` | `org_id` | 直接复用 |
| `company_name` | `org_name` | 企业登记名称 |
| `case_no` | `case_no` | 案号 |
| `case_title` | `case_title` | 案件标题 |
| `case_type_tag` | `case_type_tag` | 案件类型标签 |
| `case_role` | `case_role` | 案件身份 |
| `case_cause` | `case_cause` | 案由 |
| `current_procedure` | `current_procedure` | 当前审理程序 |
| `procedure_date` | `procedure_date` | 当前审理程序日期 |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `amount` / `court` / `event_date` / `status` | 默认 NULL |
| 源无 | `is_history` | 源表无字段且无可推导业务字段，默认 0 |
| 源无 | `id` | 自增主键 |
| `pk_id` / `reg_no` / `external_id` / `data_use_flag` | — | 不映射 |
| `creater` / `updater` / `table_data_source` / `is_deleted` | — | 不映射；`is_deleted` 仅作为过滤条件 |

#### 3.13.6 `dwd_org_risk_shixin` → `risk_dishonest`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `dishonest_id` | `dishonest_id` | 直接复用业务 ID |
| `org_id` | `org_id` | 直接复用 |
| `name_cn` | `org_name` | 机构名称 |
| `case_no` | `case_no` | 案号 |
| `dishonest_behavior` | `dishonest_behavior` | 失信行为 |
| `exec_court` | `exec_court` | 执行法院 |
| `filing_date` | `filing_date` | 立案时间 |
| `fulfillment_status` | `fulfillment_status` | 履行情况 |
| `legal_obligation` | `legal_obligation` | 法定义务 |
| `publish_date` | `publish_date` | 发布时间 |
| `is_history` | `is_history` | 源 varchar `0/1` → tinyint |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `case_title` / `amount` / `court` / `event_date` / `status` | 默认 NULL |
| 源无 | `id` | 自增主键 |
| `pk_id` / `external_id` / `official_id` / `dishonest_name` / `gender` / `age` / `credit_code` / `reg_no` / `display_id_no` / `legal_person` / `province_id` / `province` / `dishonest_type` / `exec_basis_no` / `exec_basis_org` / `exec_part` / `unexec_part` / `use_flag` / `is_hidden` | — | 不映射 |
| `creater` / `updater` / `table_data_source` / `is_deleted` | — | 不映射；`is_deleted` 仅作为过滤条件 |

#### 3.13.7 `dwd_org_risk_zhixing` → `risk_executed`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `exec_person_id` | `exec_person_id` | 直接复用业务 ID |
| `org_id` | `org_id` | 直接复用 |
| `name_cn` | `org_name` | 机构名称 |
| `case_no` | `case_no` | 案号 |
| `exec_court` | `exec_court` | 执行法院 |
| `exec_status` | `exec_status` | 执行状态 |
| `exec_target` | `exec_target` | 执行标的 |
| `filing_date` | `filing_date` | 立案时间 |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `case_title` / `amount` / `court` / `event_date` / `status` | 默认 NULL；`status` 不映射 `exec_status`，避免与 `exec_status` 语义混淆 |
| 源无 | `is_history` | 源表无字段且无可推导业务字段，默认 0 |
| 源无 | `id` | 自增主键 |
| `pk_id` / `exec_person_type` / `exec_person_name` / `gender` / `id_no` / `exec_basis_no` / `web_id` / `external_id` / `use_flag` / `is_hidden` | — | 不映射 |
| `creater` / `updater` / `table_data_source` / `is_deleted` | — | 不映射；`is_deleted` 仅作为过滤条件 |

#### 3.13.8 `dwd_org_bankruptcy_public_cases` → `risk_bankruptcy`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `case_no` | `case_no` | 案号 |
| `case_type` | `case_type` | 案件类型 |
| `handling_court` | `court` | 经办法院 |
| `public_date` | `public_date` | 公开时间 |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `case_id` | 目标 NOT NULL；源表无 `case_id`，建议按源唯一键 `case_no + handling_court` 生成稳定业务 ID，需与三方确认 |
| 源无 | `id` | 自增主键 |
| `pk_id` / `applicant_info` / `respondent_info` / `admin_org` / `admin_org_id` / `admin_principal` / `link` / `history_status` | — | 不映射 |
| `creater` / `updater` / `table_data_source` / `is_deleted` | — | 不映射；`is_deleted` 仅作为过滤条件 |

#### 3.13.9 `dwd_org_bankruptcy_public_cases_list` → `risk_bankruptcy_party`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `org_id` | `org_id` | 直接复用 |
| `related_person_name` | `party_name` | 当事人名称 |
| `party_role_type` | `party_role` | 当事人角色类型；语义待字典确认；源字段可空，目标 NOT NULL，空值处理待确认 |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `case_id` | 目标 NOT NULL；源表无 `case_id`，需按 `case_no` 关联主表复用/生成 `risk_bankruptcy.case_id`，不得使用 `bankruptcy_party_id` |
| 源无 | `is_history` | 源表无字段且无可推导业务字段，默认 0 |
| 源无 | `id` | 自增主键 |
| `pk_id` / `bankruptcy_party_id` / `case_no` / `party_type` / `name_cn` / `external_id` / `public_date` | — | 不映射 |
| `creater` / `updater` / `table_data_source` / `is_deleted` | — | 不映射；`is_deleted` 仅作为过滤条件 |

### 3.14 专利映射（关联映射）

#### 3.14.1 `dwd_patent` → `enterprise_patent_detail`

专利源表由主表及申请人、权利人、引用、标题、摘要、法律状态等子表组成。目标 `enterprise_patent_detail` 保存“企业 × 专利”宽表事实：同一专利命中多个企业时，每个 `org_id` 各写一行；`enterprise_patent_org_rel` 另存角色与顺序。

**关联逻辑**：申请人/当前权利人完整名单名称 → 精确 JOIN `dwd_org_base_info.name_cn` → 获取企业主档既有 `org_id`。未命中不得生成新 ID。

| 源字段（专利子表） | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `dwd_patent.pn` | `patent_id` | 直接 | 专利公布号作为业务 ID |
| `dwd_patent.publication_number` | `publication_number` | 直接 | |
| `dwd_patent_title.titles` | `title_zh` | 直接 | 原文标题 |
| `dwd_patent_title.title_en` | `title_en` | 直接 | 英文标题 |
| `dwd_patent_abstract.abstracts` | `abstract_zh` | 直接 | 原文摘要 |
| `dwd_patent.kind` | `patent_type` | 直接 | 专利类型 |
| `dwd_patent.country` | `country` | 直接 | 国家 |
| `dwd_patent.apdt` | `filing_date` | 直接 | 申请日期 |
| `dwd_patent.apdt_year` | `filing_year` | 直接 | 申请年份 |
| `dwd_patent.pbdt` | `publication_date` | 直接 | 公开日期 |
| `dwd_patent.pbdt_year` | `publication_year` | 直接 | 公开年份 |
| `dwd_patent_legal.isdt` | `grant_date` | 直接 | 授权日期 |
| `dwd_patent_legal.isdt_year` | `grant_year` | 直接 | 授权年份 |
| `dwd_patent.ipc` | `ipc_main` | 直接 | IPC 主分类号 |
| `dwd_patent.cpc` | `cpc_main` | 直接 | CPC 主分类号 |
| `dwd_patent.first_inventor_name` | `inventor` | 直接 | 第一发明人；发明人是自然人，不参与企业 org_id 匹配 |
| `dwd_patent.first_applicant_name` | `applicant_name` | 直接 | 第一原始申请人名称 |
| `dwd_patent.first_current_assignee_name` | `assignee_name` | 直接 | 第一当前权利人名称 |
| `dwd_patent_legal.status` | `legal_status` | 直接 | 法律状态 |
| `dwd_patent_cited.citation_nums` | `citation_count` | 直接 | 引用数 |
| `dwd_patent_cited.cited_by_nums` | `cited_by_count` | 直接 | 被引数 |
| `enterprise_patent_org_rel` | `org_id` | 关联 | 对该专利每个已命中企业各写一条 detail；按 `(org_id, patent_id)` 幂等 |

#### 3.14.1.1 申请人 / 权利人 → `enterprise_patent_org_rel`

| 源 | 角色 | 目标映射 |
|---|---|---|
| `dwd_patent_applicants(patent_id, sequence, name)` | `APPLICANT` | `name = dwd_org_base_info.name_cn` 精确唯一命中后写 `org_id` |
| `dwd_patent_assignees(patent_id, sequence, name)` | `ASSIGNEE` | 同上 |
| `dwd_patent.first_applicant_name` | `APPLICANT` | 仅在 applicants 分表无对应行时作为 `sequence=1` 回退 |
| `dwd_patent.first_current_assignee_name` | `ASSIGNEE` | 仅在 assignees 分表无对应行时作为 `sequence=1` 回退 |

- 目标字段：`patent_id`、匹配所得 `org_id`、固定 `party_role`、源 `sequence`、源 `name → source_name`、`match_type='EXACT_NAME'`。
- 未命中名称写 GDF 拒绝 / 待治理清单，至少包含 `patent_id`、role、sequence、source_name、batch_ts；禁止模糊匹配自动入库。
- 2026-09-02 live 基线：联合主表两个首位名称及 applicants/assignees 全量名称，精确匹配覆盖 3161 件专利、1533 家企业。

#### 3.14.2 `dwd_patent` → `enterprise_patent_history`（指标表）

按 `org_id + filing_year` 聚合统计：

```sql
SELECT
    org_id,
    filing_year AS data_year,
    COUNT(*) AS patent_apply_count,
    COUNT(CASE WHEN grant_date IS NOT NULL THEN 1 END) AS patent_grant_count,
    COUNT(CASE WHEN legal_status = '有效' THEN 1 END) AS patent_valid_count,
    SUM(citation_count) AS patent_citation_count,
    MAX(filing_date) AS latest_patent_date,
    MAX(grant_date) AS latest_grant_date
FROM enterprise_patent_detail
GROUP BY org_id, filing_year
```

#### 3.14.3 `dwd_patent` → `enterprise_chain_patent`（关联映射）

通过 IPC 分类号映射到产业链环节，同时关联企业获取 org_id：

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `dwd_patent.ipc` | `chain_code` / `node_id` | 关联 | IPC → 产业链映射表 |
| `dwd_patent.pn` | `patent_no` | 直接 | |
| `dwd_patent_title.titles` | `patent_name` | 直接 | |
| `dwd_patent.apdt` | `filing_date` | 直接 | |
| `dwd_patent.first_current_assignee_name` | `assignee` | 直接 | 第一当前专利权人 |
| `enterprise_patent_org_rel` | `org_id` | 关联 | 取已精确匹配的企业关系；一专利多企业可生成多条链专利关系 |

### 3.15 国外机构字段级映射

> 源字段以 md-extract 国外机构要素库及 live ODS DDL 为准（源表位于 `gkxlumenx_ods`）；目标 DDL 以 `DWD表结构设计-企业工商表-MySQL-v3.1.md` §6 为准。
> 公共规则：`org_id` 直接复用；`created_time`/`updated_time` → `create_time`/`update_time`；目标表有 `data_source` 时，源 `source_table` 或 `table_data_source` 按来源落库。

#### 3.15.1 `dwd_forg_base_info` → `enterprise_forg_base`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `org_id` | `org_id` | 直接复用 |
| `name_en` | `enterprise_name` | 机构英文名称 |
| `name_alias` | `name_alias` | 机构本地名称 |
| `country_code` | `country_code` | 国家代码 |
| `country` | `country_name` | 国家名称 |
| `external_id` | `enterprise_code` | 当地官方注册码 |
| `state` | `state` | 所在州/省 |
| `city` | `city` | 所在城市 |
| `address` | `address` | 公司地址 |
| `postal_code` | `postal_code` | 邮政编码 |
| `phone` | `phone` | 联系电话 |
| `email` | `email` | 电子邮箱 |
| `company_type` | `enterprise_type` | 企业类型 |
| `incorporation_date` | `registration_date` | 成立日期 |
| `incorporation_year` | `incorporation_year` | 成立年份 |
| `listing_status` | `is_listed` | 1 → 1，其他 → 0/NULL |
| `stock_code` | `stock_code` | 上市股票代码 |
| `registered_capital_value` | `registered_capital` | 单位待源表字段确认，本版不做换算 |
| `registered_capital_currency_code` | `capital_currency_code` | 注册资本货币代码 |
| `industry_code` | `industry_code` | 行业代码 |
| `industry_type` | `industry_type` | 行业分类标准 |
| `registration_org` | `registration_org` | 注册机构/登记机关 |
| `source_table` | `data_source` | 数据来源表名 |
| `create_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `id` | 自增主键 |

#### 3.15.2 `dwd_forg_base_info` → `enterprise_forg_extra`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `org_id` | `org_id` | 先写机构 ID；`main_activities`/`main_prod`/`description` 由 `dwd_forg_product_info` 补充 |

#### 3.15.3 `dwd_forg_product_info` → `enterprise_forg_extra`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `org_id` | `org_id` | 直接复用 |
| `main_activities` | `main_activities` | 公司主营业务 |
| `main_products` | `main_prod` | 主要产品 |
| `description` | `description` | 企业简介 |
| `create_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 设计映射；现网 `enterprise_forg_extra` 已补 `update_time`，按该字段增量同步 |
| 源无 | `id` | 自增主键 |
| `org_name` / `source_table` / `table_data_source` | — | 不映射；目标 `enterprise_forg_extra` 无 `data_source` 字段 |

#### 3.15.4 `dwd_forg_executive_info` → `enterprise_forg_executive`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `org_id` | `org_id` | 直接复用 |
| `executives_name` | `executive_name` | 高管姓名 |
| `executives_position` | `position` | 职位名称 |
| `source_table` | `data_source` | 数据来源表名 |
| `create_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `id` | 自增主键 |
| `org_name` | — | 不映射 |

#### 3.15.5 `dwd_forg_shareholder_info` → `enterprise_forg_invest`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `org_id` | `org_id` | 直接复用 |
| `owners_id` | `inv_org_id` | 股东/被投机构 ID |
| `owners_name` | `inv_name` | 股东/被投机构名称 |
| `owners_country_code` | `inv_country_code` | 股东所在国家代码 |
| `ownership_percentage` | `ownership_percentage` | 持股比例（%） |
| `source_table` | `data_source` | 数据来源表名 |
| `create_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `id` | 自增主键 |
| `org_name` / `owners_country` | — | 不映射 |

#### 3.15.6 `dwd_foreign_org_annual_financial_info` → `enterprise_forg_finance_history`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `org_id` | `org_id` | 直接复用 |
| `occur_period` | `occur_period` | 报表数据期 |
| `occur_period` | `data_year` | 推导：日期/`YYYYMM` 取前 4 位；格式异常则 NULL |
| `total_assets` | `total_assets` | 资产总额 |
| `fixed_assets` | `fixed_assets` | 固定资产净额 |
| `total_liabilities` | `total_liabilities` | 负债总额 |
| `operating_revenue` | `operating_revenue` | 营业收入 |
| `total_profit` | `total_profit` | 利润总额 |
| `pure_profit` | `pure_profit` | 净利润 |
| `total_tax_paid` | `total_tax_paid` | 纳税总额 |
| `employees_number` | `employees_number` | 从业人数 |
| `research_development_amount` | `research_development_amount` | 研发投入金额 |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| `source_table` | `data_source` | 数据来源表名 |
| 源无 | `main_business_revenue` | 默认 NULL |
| 源无 | `id` | 自增主键 |
| `qymc` / `create_time`（重复） | — | 不映射 |
| `profit_after_tax` / `oper_cash_flow` / `owners_equity` | — | 不映射；目标表暂无税后利润/经营现金流/所有者权益字段 |

> **财务单位（2026-09-02 `human:徐滕强` 确认）**：国外财务目标同样统一为**万元**。GDF 须按 live 字段注释、原始值文本和样本判定后换算；单位无法证实时阻塞，不得按源值盲写。

#### 3.15.7 `dwd_forg_subsidiary_info` → `enterprise_forg_parent_subsidiary`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `org_id` | `org_id` | 直接复用（母公司） |
| `affiliate` | `sub_org_id` | 子公司机构 ID |
| `affiliates_name` | `sub_name` | 子公司名称 |
| `affiliates_country_code` | `sub_country_code` | 子公司所在国家代码 |
| `affiliates_country` | `sub_country_name` | 子公司所在国家名称 |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `id` | 自增主键 |
| `pk_id` / `affiliates_company_id` / `creater` / `updater` | — | 不映射；目标表暂无对应字段 |
| `is_deleted` | — | 不映射；仅作为过滤条件，`is_deleted = 0` 才入 DWD |
| `table_data_source` | — | 不映射；目标 `enterprise_forg_parent_subsidiary` 现网无 `data_source` 列，ES 侧保持空，不伪造数据 |

> ⚠️ 已按 live 表 `gkxlumenx_ods.dwd_forg_subsidiary_info` 回填字段映射；该表当前为 0 行，后续数据灌入后再校验样例。

### 3.16 `dwd_org_recruit_info` → `enterprise_recruit`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `org_id` | `org_id` | 直接复用 |
| `name_cn` | `enterprise_name` | 机构名称 |
| `external_id` | `enterprise_code` | 统一社会信用代码 |
| `job_title` | `job_title` | 岗位 |
| `job_description` | `job_description` | 工作描述 |
| `work_place` | `work_place` | 工作地点 |
| `release_date` | `release_date` | 发布日期 |
| `hiring_number` | `hiring_number` | 源 DDL 为 bigint，但样例可能为“若干”，目标用 varchar(64) 更稳妥 |
| `table_data_source` | `data_source` | 源 DDL 字段名 `table_data_source`，按业务 `data_source` 落库 |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `id` | 自增主键 |
| `pk_id` / `creater` / `updater` | — | 不映射 |
| `is_deleted` | — | 不映射；仅作为过滤条件 |

### 3.17 `dwd_org_industry_tags` → `enterprise_industry_chain`（本期可覆盖字段）

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `credit_code` | `enterprise_code` | 直接；并关联 `enterprise_base.enterprise_code` 获取 `org_id` |
| 关联所得 | `org_id` | 仅唯一命中时写入；未命中保持 NULL 并进拒绝清单 |
| `industry_code` | `chain_code` | 直接 |
| `industry_name` | `chain_name` | 直接 |
| `industry_link_code` | `node_id` | 直接 |
| `industry_link_name` | `node_name` | 直接 |
| 源无 | `node_stage` / `is_chain_leader` / `chain_score` | NULL；禁止伪造 |
| `created_time` | `create_time` | 直接 |
| `updated_time` | `update_time` | 直接 |

> `dwd_org_industry_chain_dtl` 继续作为供应方待核实表，不进入 Wave A 施工清单；若后续到表，再按变更单补 `chain_score` 等增量字段，不覆盖本期已洗结果。

### 3.18 港澳台企业 → `enterprise_base`（本期纳入）

| 来源 | `org_id` | `enterprise_code` | `enterprise_name` | `region_id` | 地区文本 |
|---|---|---|---|---|---|
| `dwd_special_hongkong_company` | `org_id` | `company_code`（可空） | `name_cn` | `810000` | `province='香港特别行政区'` |
| `dwd_special_taiwan_company` | `org_id` | `company_code`（可空） | `COALESCE(n_company_name, company_name)` | `710000` | `province='台湾省'` |
| `dwd_special_aomen_company` | `org_id` | `company_code`（可空） | `org_loc_name` | `820000` | `province='澳门特别行政区'` |

- `enterprise_code` 已恢复为可空契约；不得将香港商业登记号、台湾统一编号、澳门商业登记号伪装成大陆统一社会信用代码以满足非空约束。保留原值时仍须通过 `data_source` 标明来源。
- `region_id` 是项目派生企业粒度字段：港澳台按来源表确定地区，不依赖信用代码；其余国内企业按省/市/区关联行政区划维表。
- 源 `org_id` 直接复用。2026-09-02 live：香港 / 台湾各 40000 行均有 `org_id`；澳门 792 行仅 396 行有 `org_id`。澳门缺失 `org_id` 的 396 行只保留 ODS 并进待治理清单，禁止生成新 ID。
- 其他可对应字段按语义映射：成立日期 → `registration_date`，状态 → `business_status`，类型 → `enterprise_type`，法定代表人（台湾）→ `legal_representative`。资本值统一为万单位并保留币种证据，单位 / 币种无法确认时不写金额。

---

## 4. 指标表聚合逻辑

### 4.1 `enterprise_risk_summary`

```sql
-- 从各风险明细表聚合，按 org_id + risk_type 统计
INSERT INTO enterprise_risk_summary (org_id, risk_type, total_count, current_count, history_count, latest_date)
SELECT org_id, 'judicial_case', COUNT(*),
       SUM(CASE WHEN is_history = 0 THEN 1 ELSE 0 END),
       SUM(CASE WHEN is_history = 1 THEN 1 ELSE 0 END),
       MAX(event_date)
FROM risk_judicial_case
GROUP BY org_id
-- 其余 risk_* 表同理，每张表一条 INSERT...SELECT
```

### 4.2 `enterprise_region_summary`

```sql
-- 从 enterprise_base 按区域聚合
SELECT
    region_id, region_name, region_type, parent_region_id, CURRENT_DATE AS stat_date,
    COUNT(*) AS enterprise_total,
    SUM(CASE WHEN DATE(registration_date) = CURRENT_DATE THEN 1 ELSE 0 END) AS new_enterprise_count,
    SUM(CASE WHEN business_status = '在营' THEN 1 ELSE 0 END) AS active_enterprise_count
FROM enterprise_base
GROUP BY region_id, region_type
```

### 4.3 `enterprise_industry_summary`

```sql
-- 从 enterprise_industry_chain 按产业链聚合
SELECT
    chain_code, chain_name, stat_year, CURRENT_DATE AS stat_date,
    COUNT(DISTINCT org_id) AS enterprise_count
FROM enterprise_industry_chain eic
JOIN enterprise_base eb ON eic.org_id = eb.org_id
GROUP BY chain_code, chain_name, stat_year
```

---

## 5. 需要确认的问题

| # | 问题 | 影响 | 建议 |
|---|---|---|---|
| 1 | 招聘信息目标侧无对应表 | 招聘数据无法入库 | ✅ 已确认新建 `enterprise_recruit`，映射见 §3.16 |
| 2 | 注册资本单位：源表"元" vs 目标表"万元" | 金额错误 | ✅ 已确认目标统一万元，源 `registered_capital_value` ÷10000 |
| 3 | `dwd_org_annual_financial_info` 字段名未带单位；`dwd_org_stock_finance_info` 明确带(元) | 单位误判会造成 10000 倍错误 | ✅ 目标统一万元；GDF 实查字段注释/原始值/样本后换算，无法判定则阻塞 |
| 4 | 实际 live 表为 `gkxlumenx_ods.dwd_org_tag_info`，原文档误写 `dwd_org_tech_tag` | 源表名不一致 | ✅ 已修正；现成口径为 `org_tag → tag_code`，`tag_name/tag_category` 按 `gkxlumenx_dwd.tag_dict` 反查；`tag_level` 保留在 `tag_dict`，不直接映射到 `enterprise_tag` |
| 5 | 专利无企业 `org_id` / 信用代码，且一件专利可有多个申请人/权利人 | 单一 detail.org_id 无法表达完整关系 | ✅ 新增 `enterprise_patent_org_rel`；主表首位名称 + applicants/assignees 分表全量精确匹配企业主档，未命中进治理清单、不造 ID |
| 6 | `enterprise_industry_chain.enterprise_code` 当前全为空 | 无法通过信用代码关联 org_id | ⏳ 已知数据阻塞，本期不解决 |
| 7 | 风险表字段级映射未逐字段对照 | 可能有字段名/类型不一致 | ✅ 已完成，见 §3.13 |
| 8 | 港澳台企业映射目标 | 数据覆盖范围 | ✅ 本期写国内 `enterprise_base`；恢复 `region_id`，enterprise_code 可空；港/台/澳分别绑定 810000/710000/820000，澳门缺 org_id 行只留 ODS |
| 9 | 国外财务字段未标注单位 | 金额口径错误 | ✅ 目标统一万元；GDF 实查单位后换算，无法判定则阻塞 |
| 10 | `name_alias` 可能是中文/本地名称 | ES 名称检索语义 | ✅ 已确认：国内 `enterprise_name → name_cn`、`enterprise_name_en/name_alias → name_en`；国外 `enterprise_name → name_en`、`name_alias → name_cn` |
| 11 | 国外 `industry_type` 是分类标准（如 NAICS），不是行业名称 | ES 行业名称检索 | ✅ 本期 ES `industry_class_name` 先置空，后续行业字典反查再回填 |

---

## 6. 版本历史

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.2 | 2026-08-12 | 按 live ODS 修正国外来源表/字段，补充母子公司字段级映射与问题清单 |
| v1.1 | 2026-08-12 | 新增招聘/国外机构映射；补全风险表字段级映射；修正标签源表为 `dwd_org_tag_info`；更新问题清单 |
| v1.0 | 2026-08-12 | 首版：源表到 DWD 的表级+字段级映射明细 |
