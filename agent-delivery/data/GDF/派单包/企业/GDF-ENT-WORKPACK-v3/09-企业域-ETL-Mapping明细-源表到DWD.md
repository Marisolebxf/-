> **【GDF-ENT-WORKPACK-v3.1.5 · Mapping 施工真源】** 日期 2026-10-19。加工逻辑补遗见 CHANGELOG v3.1.5 与本文件对应小节。列契约以 `00` §8 / §9 为准。  
> 基线来源：`agent-delivery/data/data-design/企业/企业域-ETL-Mapping明细-源表到DWD.md`（v1.2）；本包按监管人确认增加财务万元门禁、live 核验和港澳台本期范围。  
> 旧短版 `09-企业维-ODS到DWD-Mapping说明-v4.md` **仅作导读**，字段级施工 **只认本文件**。  
> **复核范围（诚实）**：只复核 `00` §8 已拍板项。其余 **继承 v1.2，未逐字段复验**。正式库已 ADD 的列按列洗。GDF 不写 demo。禁止假装 49 张表已对完。

---
# 企业域 ETL Mapping 明细 — 源表到 DWD

> **版本**：v3.1（继承 v1.2；复核范围见上文；列名跟正式库）
> **日期**：2026-09-03
> **范围**：GDF 三方源表（`dwd_org_*` / `dwd_patent*`）→ 项目 DWD（`gkxlumenx_dwd.enterprise_*` / `risk_*`）的字段级映射
> **配套文档**：`企业域-数据ETL流转架构.md`（架构总纲）、`DWD表结构设计-企业工商表-MySQL-v3.1.md`（目标表 DDL）
> **目标库**：`gkxlumenx_dwd`（MySQL `10.50.11.76:3306`，见 `03`）。**禁止**写 `demo_gkxlumenx_*`。  
> **交付对象**：GDF 三方 ETL 团队

---

## 1. 映射分类说明

| 类型 | 说明 | 示例 |
|---|---|---|
| **直接映射** | 源表字段直接写入目标表对应字段，仅做类型/命名转换。源列**不必同名**，以要素库/live 注释意义为准（Q-WP3-24）；禁止猜口径 | `org_id → org_id`、`capital_currency → capital_currency_code` |
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

2026-09-02 live 核验：`dwd_org_industry_chain_dtl` 在 `gkx` 及当前可见 schema 中不存在，不能作为本期施工输入。先用 `dwd_org_industry_tags.credit_code` 关联 `enterprise_base.enterprise_code` 获取 `org_id`，并映射其产业 / 环节字段；同时继续向供应方索取或核实 `chain_dtl` 实名。`industry_tags` 不含 `chain_score` / `segment_key`，对应目标字段保持 NULL，禁止伪造。产品标签走同口径：`dwd_org_industry_product_tags.credit_code` → `enterprise_industry_product`（§3.19）。

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
| 18 | `dwd_org_tech_tag`（旧名 tag_info） | `enterprise_tag` | 直接映射 |
| 19 | `dwd_org_subsidiary_info` | `enterprise_parent_subsidiary` | 直接映射（子=`org_id`，母=`parent_*`；§3.10） |
| 20 | `dwd_org_recruit_info` | `enterprise_recruit` | 招聘信息（新建表） |

### 2.2 关联映射（9 条）

| # | 源表 | 目标表 | 关联逻辑 |
|---|---|---|---|
| 1 | `dwd_org_changerecord_info` | `enterprise_history_name` | 仅取 `update_content` 含"名称"的行，`current_name` → `history_name` |
| 2 | `dwd_org_stock_finance_info` | `enterprise_finance_history`（补充） | 按业务含义选取字段，`occur_period` 解析为 `data_year` |
| 3 | `dwd_org_shareholder_info` | `enterprise_shareholder` | 2026-09-02 改口：新建股东表；**禁止**再写入 `enterprise_supply_chain` |
| 4 | `dwd_bid_win_candidate_out` | `enterprise_bid` | 通过 `org_id` 直接关联（源表已有 org_id） |
| 5 | `dwd_bid_base_out` | `enterprise_bid`（公告信息补充） | 通过 `u_id` 关联中标表 |
| 6 | `dwd_patent` + applicants/assignees 分表 | `enterprise_patent_detail` + `enterprise_patent_org_rel` | 所有申请人/权利人名称精确匹配企业主档；关系表保留角色与顺序 |
| 7 | （空）`dwd_org_industry_chain_pat_dtl` | `enterprise_chain_patent` | **本期不洗（Q-WP3-19）**：源表现网不存在；禁止用 `dwd_patent` + IPC 硬推 |
| 8 | `dwd_org_industry_tags` | `enterprise_industry_chain` | `credit_code` → JOIN `enterprise_base.enterprise_code` → `org_id`；产业/环节字段直接映射 |
| 9 | `dwd_org_industry_product_tags` | `enterprise_industry_product` | `credit_code` → JOIN `enterprise_base.enterprise_code` → `org_id`；列表字段取首元素（§3.19） |

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
| `dwd_org_merger_acquisition_info`（并购事件） | **Q-WP3-21 可贴源不洗（B）**：目标无并购 DWD；Wave A `mirror_only`。当事人表不贴。禁止洗进 invest/supply_chain |
| `dwd_bid_purchase_agency_out` / `dwd_bid_target_item_out` | 采购代理/标的物不在企业域范围 |
| `dwd_org_innovation_carrier` → `enterprise_innovation_carrier` | **2026-09-02 确认本期不做**：live `gkx` 无源；`02` 已剔除。ES 模块保留但不触发 |
| （无源）→ `enterprise_cooperation` | **2026-09-02 确认本期不做（A）**：live `gkx` / ODS 无合作关系源表。图谱合作类 op 不触发 |
| `fund_project` → `enterprise_fund_project` | **2026-09-02 确认本期不做（A）**：现网无该源表；`dwd_fund_*` 是基金不是科研立项，禁止顶替 |
| `dwd_org_sc_info` → `enterprise_supply_chain` | **2026-09-02 本期不做（A）+ 潜在可能（Q-WP3-18）**：live≈1716 行，两端企业+信用代码。要素库 CSV 无此表，`type` 1/2 无值域。**不贴不洗**；确认前禁止当供应边 |
| `dwd_org_industry_chain_pat_dtl` → `enterprise_chain_patent` | **2026-09-02 本期不做（A，Q-WP3-19）**：live / 要素库均无此表。禁止 `dwd_patent.ipc` 硬挂产业链。明细 / `patent_org_rel` / 按年计数照旧 |

### 2.5 国外机构映射（6 条）

| # | 源表 | 目标表 | 说明 |
|---:|---|---|---|
| 1 | `dwd_forg_base_info` | `enterprise_forg_base` + `enterprise_forg_extra` | 主数据拆分 |
| 2 | `dwd_forg_product_info` | `enterprise_forg_extra` | 经营/产品/描述 |
| 3 | `dwd_forg_executive_info` | `enterprise_forg_executive` | 高管信息 |
| 4 | `dwd_forg_shareholder_info` | `enterprise_forg_invest` | **Q-WP3-20 维持（A）**：现网无国外投资表；股东当投资写入本表 |
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
| `industry_l4_code` | `industry_code` | 直接 | 取 4 位 L4。禁止 `LEFT(industry_l4_code,2)`。L4 为空则 `industry_code` 为 NULL |
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

**Q-WP3-24 B**：正式库缺的 7 列只 ADD 再洗。源列**不必同名**，以要素库/live 注释意义为准（`capital_currency`→`capital_currency_code`，`listing_status`→`listed_status`）。禁止把无关列当同义。demo 已有这 7 列则跳过 ADD。

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
| `operating_revenue` | `revenue` | 条件转换 | 营业收入；目标统一万元，按下方门禁换算。**禁止**与主营收入合成一列（Q-WP3-22：源两列都有） |
| `main_business_revenue` | `main_business_revenue` | 条件转换 | 主营业务收入；目标统一万元。正式库缺列则 ADD，禁止写进 `revenue` |
| `total_profit` | `total_profit` | 条件转换 | 利润总额；目标统一万元。正式库缺列则 ADD |
| `pure_profit` | `net_profit` | 条件转换 | 净利润；目标统一万元。正式库已有 `net_profit`，升为设计列，禁止另 ADD `pure_profit` |
| `fixed_assets` | `total_fixed_assets` | 条件转换 | 固定资产总额。源表无 `total_fixed_assets`，只取 `fixed_assets`。目标统一万元，按下方门禁换算 |
| `total_assets` | `total_assets` | 条件转换 | 年末资产总额；目标统一万元，按下方门禁换算 |
| `total_liabilities` | `total_liabilities` | 条件转换 | 年末负债总额；目标统一万元，按下方门禁换算 |
| `data_source` | `data_source` | 直接 | |

> **财务单位门禁（2026-09-02 `human:徐滕强` 确认；2026-10-19 补成可执行规则）**：目标统一为**万元**。源注释或单位列明确为元时该列 ÷10000；明确为万元时原值写入。`dwd_org_annual_financial_info` 同一金额列里元和万元并存，且 `data_source` 不能把行分开时：**该金额单元格写 NULL，行进治理清单**（带 org_id、year、列名、原值）。禁止整表 ÷10000，禁止用数值大小猜单位。其他列照常洗，不因此停整包。

### 3.4 `dwd_org_stock_finance_info` → `enterprise_finance_history`（补充）

上市企业财务指标有更丰富的字段（净利润、研发投入、从业人数等），按目标表已有字段选取补充：

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `org_id` | `org_id` | 直接 | |
| `occur_period` | `data_year` | 转换 | 如 "2023-12-31" → 2023 |
| `operating_revenue` | `revenue` | 转换 | ÷10000（元→万元）。禁止与主营收入合成 |
| `main_business_revenue` | `main_business_revenue` | 转换 | ÷10000 |
| `total_profit` | `total_profit` | 转换 | ÷10000 |
| `pure_profit` | `net_profit` | 转换 | ÷10000；净利润 |
| `fixed_assets` | `total_fixed_assets` | 转换 | ÷10000 |
| `total_assets` | `total_assets` | 转换 | 年末资产总额；÷10000（元→万元） |
| `total_liabilities` | `total_liabilities` | 转换 | 年末负债总额；÷10000（元→万元） |
| `data_source` | `data_source` | 直接 | |

> Q-WP3-22：净利润进 `net_profit`。研发投入等其余源字段仍不进国内目标表。`total_assets` / `total_liabilities` 为年末时点存量，ES 取最新一年，不与收入逐年同维。

### 3.5 `dwd_org_important_news_info` → `enterprise_news`

**Q-WP3-25 C（2026-09-02 `human:徐滕强`）**：正式库用现网列。有同义就不 ADD 设计同义列。`summary` **就是资讯全文**，不是短摘要。

| 源字段 | 目标字段（正式库） | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `org_id` | `org_id` | 直接 | |
| `name_cn` | `enterprise_name` | 直接 | |
| `news_title` | `title` | 直接 | 意义=标题；不 ADD `news_title` |
| `news_date` | `publish_time` | 转换 | 意义=发布日；现网 datetime，日期补 00:00:00 |
| `news_content` | `summary` | 直接 | **全文**进 `summary` |
| `original_textlink` | `original_url` | 直接 | 现网无同义列，**只 ADD** 这一列 |

禁止 ADD `news_title` / `news_date` / `news_content` 与现网列双写。demo 已有设计列可并存，产线只认上表。`lumen-etl-es-py` `news.py` 已改读 `title`/`publish_time`/`summary`（`DATA-ENT-DWD-ALIGN-ETL-L01`）；ES params 键名不动。

### 3.6 `dwd_org_changerecord_info` → `enterprise_history_name`（关联映射）

**仅取变更类型含"名称"的行**：

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `org_id` | `org_id` | 直接 | |
| `current_name` | `history_name` | 直接 | 变更前内容 = 曾用名 |
| `update_date` | `start_date` | 直接 | 变更日期 = 曾用名起始 |
| `update_name` | — | 不映射 | 变更后内容 = 现用名（已在 base 表） |

过滤条件：`WHERE update_content LIKE '%名称%'`

ES：`former_names` **本期要灌**（Q-WP3-14），整组替换；`DATA-ENT-ES-FORMER-L01` 已写模块。表 success 后按 `12`/`15` 触发；未跑 sync ≠ 代码未上。

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

**Q-WP3-27 A（2026-09-02）**：被投企业键只认 `inv_org_id`（32 位）。源 `inv_external_id` 是被投**信用代码**（18 位），**不 ADD、不洗、不写进任何 org_id**。正式库用现网列名。

| 源字段 | 目标字段（正式库） | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `org_id` | `org_id` | 直接 | 投资方 |
| `inv_org_id` | `inv_org_id` | 直接 | 被投 `org_id`；禁止用信用代码顶 |
| `inv_name` | `inv_org_name` | 直接 | 被投名称；不 ADD `inv_name` |
| `investment_amount` | `invest_amount` | 条件转换 | 源注释元；目标按万元门禁 |
| `investment_ratio` | `invest_ratio` | 直接 | 股权占比 |
| `inv_external_id` | — | 不映射 | 信用代码，本期不落 |
| `data_source` | — | 不映射 | 正式库无此列，不 ADD |
| `updated_time` | — | 不映射 | **禁止**当 `event_date` |

### 3.9 `dwd_org_tech_tag` → `enterprise_tag`（旧名 `dwd_org_tag_info` 现网不存在）

2026-09-02 监管人确认：供应方工作簿与 live `gkx` 均为 `dwd_org_tech_tag`（约 20 万行）。**与下文 v1.2 设想的 tag_info 列不完全同构**：live 有 `org_id`/`org_tag`/`data_source`/`created_time`/`updated_time`/`is_deleted` + 技术列；**无** `name_cn`/`external_id`/`tag_level`/`tag_value`。`org_tag` 现网是中文名称（如「高新技术企业」），不是 `high_tech` 码。码对照仍走 `ENT-P0-7`。`tag_dict` 未就绪时：`tag_code` 与 `tag_name` 都落 `org_tag` 原文，`tag_category` 写 NULL。禁止编造码，禁止因字典为空整表不洗。过滤 `is_deleted = 0`。

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `org_id` | `org_id` | 直接 | |
| `org_tag` | `tag_code` | 直接 | 标签编码 |
| `org_tag` | `tag_name` | 直接 | 与 `tag_code` 同为中文原值。`tag_dict` 有命中行时再改用字典名，未命中保持原文 |
| `org_tag` → JOIN `gkxlumenx_dwd.tag_dict` | `tag_category` | 字典反查 | 字典无行或未命中则 NULL |
| `tag_level` | — | 不映射 | 目标 `enterprise_tag` 无 `tag_level` 字段；`tag_dict.tag_level` 已按 `tag_code` 维护 |
| `tag_value` | — | 待细化 | 普通标签默认 NULL；荣誉/级别类标签的展示值后续按规则生成 |
| `created_time` | `create_time` | 直接 | 创建时间 |
| `updated_time` | `update_time` | 直接 | 更新时间 |
| — | `tag_score` | 源无 | 默认 NULL；后续如需评分来源再回填 |
| — | `id` | 自增 | bigint AUTO_INCREMENT |
| `name_cn` / `external_id` | — | 不映射 | 目标表无对应字段 |
| `is_deleted` | — | 不映射 | 仅作为过滤条件 |

### 3.10 `dwd_org_subsidiary_info` → `enterprise_parent_subsidiary`

2026-09-02 确认（Q-WP3-13）：用国内子公司表，**不做**分支机构、**不掺** `dwd_agg_subsidiary_info`（`eid` 不是 `org_id`）。  
源口径：`org_id`/`name_cn` = 母公司，`sub_org_id`/`sub_name_cn` = 子公司。DWD 行主体是**子公司**（图谱点），母写在 `parent_*`。旧稿把子字段写成了母字段，已纠正。

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `sub_org_id` | `org_id` | 直接 | 子公司；空则跳过该行，禁止造 ID |
| `org_id` | `parent_org_id` | 直接 | 母公司 |
| `name_cn` | `parent_enterprise_name` | 直接 | 母公司名称 |
| `sub_name_cn` / `sub_external_id` | — | 不映射 | 子名称/信用代码不落本表（子主体已在 `enterprise_base`） |
| 源无 | `ownership_ratio` / `subsidiary_count` | — | NULL，禁止伪造 |

两端 `org_id` 都应能在 `enterprise_base` 找到；对端缺失记拒绝清单，不上图。表 success 后触发 `ENT_RE_BELONG`；国内无母子 ES 模块。

### 3.11 `dwd_org_shareholder_info` → `enterprise_shareholder`（新建，Q-WP3-17）

旧稿把股东洗进 `enterprise_supply_chain` 当「投资方」，**作废**。对外投资只认 `dwd_org_invest_info` → `enterprise_invest`。

| 源字段 | 目标字段 | 转换逻辑 |
|---|---|---|
| `org_id` | `org_id` | 被持股企业；空则跳过 |
| `name_cn` | `enterprise_name` | 直接 |
| `external_id` | `enterprise_code` | 直接，可空 |
| `inv_org_id` | `shareholder_org_id` | 有值才写；空（自然人/未关联）保持 NULL，**禁止造 ID** |
| `owners_name` | `shareholder_name` | 必填；空则跳过该行 |
| `owners_type` | `shareholder_type` | **原文照写**（自然人股东/企业法人/…），禁止改写成「投资方」 |
| `ownership_percentage` | `ownership_percentage` | 直接，单位 % |
| `data_source` / `table_data_source` | `data_source` | 优先 `data_source` |
| `creater` / `updater` / `dwd_id` | — | 不映射 |
| `is_deleted` | — | 仅过滤 `=0` |

ES / 图谱本期不上。供应链模块不得再读股东源。

### 3.20 `enterprise_supply_chain`（本期不洗，Q-WP3-18）

目标表还要 `relation_type`（supplier/customer）、`relation_strength`、`is_core_supplier`、`risk_level`。现网没有能填这些列的**已确认**三方事实。

**潜在可能（未确认，禁止施工）：** `dwd_org_sc_info`

| 观察 | 缺口 |
|------|------|
| 表注释「产业供应链信息」；≈1716 行 | 要素库 CSV/xlsx **未收录**，无字段描述/值域 |
| `company_name`+`credit_code` ↔ `name`+`code`（`code` 全 18 位） | 业务列无注释 |
| `type` 只有 `1` / `2` | **不能**猜成供应商/客户 |

其余仍禁止顶替：股东走 `enterprise_shareholder`，投资走 `enterprise_invest`，正式库 169 行 `ORG*` mock 不当源。

本期不贴不洗。不触发 ES `supply_chain`、不上图 `ENT_RE_SUPPLY`。供应方书面确认 `type` 前不升格为 Mapping 源。

### 3.12 招投标 → `enterprise_bid`

**Q-WP3-26（2026-09-02 `human:徐滕强`）**：正式库用现网列。有同义就洗进现网；**项目编号必须洗**（标讯关键字段），现网无列则 **只 ADD `project_no`**。公告类型是招投标公告属性，现网没有对应列 → **不映射，`bid_type` 空着**，禁止塞进 `bid_type`。

主路径：`dwd_bid_win_candidate_out` 按 `org_id` 落企业；用 `u_id` 关联 `dwd_bid_base_out` 取公告标题/发布日/项目编号。

| 源 | 目标（正式库） | 转换 |
|---|---|---|
| `win.org_id` | `org_id` | 直接 |
| `base.title`，关联不上再用 `win.project_name` | `bid_title` | **不拼接** `bid_item_name` |
| `win.amount` | `bid_amount` | 见下表。未知单位不停整包：金额写 NULL，行进治理清单 |
| `base.publish_time` | `event_date` | 公告发布日 |
| `base.project_number`，空则 `win.project_number` | `project_no` | **必洗**；只 ADD 此列 |
| `win.name_cn` | — | 现网无 `enterprise_name`，有 `org_id` 本期不 ADD、不落 |
| `base.announcement_type` / `relate_type` / `role` | — | **不映射**；`bid_type` 保持空 |
| `tender_org_*` | `tender_org_id` / `tender_org_name` | 源有才写；没有空着 |

`amount_unit` 换算（目标万元）：

| 源 `amount_unit` | `bid_amount` |
|---|---|
| `元` / `人民币` / `CNY` / `RMB`（大小写不敏感） | `amount ÷ 10000` |
| `万元` | 原值 |
| 空、含 `/` 的单价（元/人/天、元/kg、元/平方米等）、外币（美元、USD、欧元等） | NULL，该行其他列照洗，金额进治理清单 |

禁止按汇率把外币折成人民币。禁止 ADD `announcement_title` / `announcement_date` / `winning_amount` / `project_name` / `role` 与现网列双写。`lumen-etl-es-py` `bid.py` 已改读 `bid_title`/`event_date`/`bid_amount`（`DATA-ENT-DWD-ALIGN-ETL-L01`）；ES 仍写 `announcement_title`/`announcement_date`。`project_no` **正式库已 ADD**，必洗。

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
| 源无 | `status` | 源表无 `status`，写 NULL |
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
| 源无 | `status` | 源表无 `status`，写 NULL |
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
| 源无 | `status` | 源表无 `status`，写 NULL |
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
| 源无 | `is_history` | 源表无 `is_history` 列，默认 0 |
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
| 源无 | `is_history` | 源表无 `is_history` 列，默认 0 |
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
| 源无 | `case_id` | `LEFT(SHA2(CONCAT(IFNULL(case_no,''),'|',IFNULL(handling_court,'')),256),64)`。`case_no` 与 `handling_court` 都空则丢行进治理清单。不使用 `bankruptcy_party_id` |
| 源无 | `id` | 自增主键 |
| `pk_id` / `applicant_info` / `respondent_info` / `admin_org` / `admin_org_id` / `admin_principal` / `link` / `history_status` | — | 不映射 |
| `creater` / `updater` / `table_data_source` / `is_deleted` | — | 不映射；`is_deleted` 仅作为过滤条件 |

#### 3.13.9 `dwd_org_bankruptcy_public_cases_list` → `risk_bankruptcy_party`

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `org_id` | `org_id` | 直接复用 |
| `related_person_name` | `party_name` | 当事人名称 |
| `party_role_type` | `party_role` | 原值写入。空或 NULL 则该当事人行不入库，进治理清单；案件主表照洗 |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `case_id` | 目标 NOT NULL；源表无 `case_id`，需按 `case_no` 关联主表复用/生成 `risk_bankruptcy.case_id`，不得使用 `bankruptcy_party_id` |
| 源无 | `is_history` | 源表无字段且无可推导业务字段，默认 0 |
| 源无 | `id` | 自增主键 |
| `pk_id` / `bankruptcy_party_id` / `case_no` / `party_type` / `name_cn` / `external_id` / `public_date` | — | 不映射 |
| `creater` / `updater` / `table_data_source` / `is_deleted` | — | 不映射；`is_deleted` 仅作为过滤条件 |

### 3.14 专利映射（关联映射）

#### 3.14.1 `dwd_patent` → `enterprise_patent_detail`

**Q-WP3-23**：正式库专利宽列 **已 ADD**。现网同义列 `patent_name` / `publish_date` / `ipc_code` **不 DROP**。按宽列+窄列并存洗。禁止写不存在的源列 `ipc` / `cpc` / `citation_nums`。

目标仍是“企业 × 专利”一行：同一专利命中多个企业时，每个 `org_id` 各写一行；`enterprise_patent_org_rel` 另存角色与顺序（Q-WP3-04 不变）。

**关联逻辑**：申请人/当前权利人完整名单名称 → 精确 JOIN `dwd_org_base_info.name_cn` → 获取企业主档既有 `org_id`。未命中不得生成新 ID。

Wave A 贴 `dwd_patent` / `dwd_patent_applicants` / `dwd_patent_assignees`。宽列 ADD 后，`dwd_patent_title` / `abstract` / `legal` / `cited` **允许贴**，写入设计列（`title_zh` / `abstract_zh` 等）；`patent_name` 可与 `title_zh` 同义回填，不另造标题口径。禁止直连 live `gkx` 越层。

正式库现网列：`org_id` / `patent_id` / `patent_name` / `patent_type` / `filing_date` / `publish_date` / `legal_status` / `ipc_code`。旧列保留不 DROP。

| 源字段 | 目标字段（正式库窄表） | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `dwd_patent.pn` | `patent_id` | 直接 | 专利记录唯一标识 |
| `dwd_patent.kind` | `patent_type` | 直接 | 类型代码 |
| `dwd_patent.apdt` | `filing_date` | 转换 | 申请日；源注释 YYYYMMDD |
| `dwd_patent.pbdt` | `publish_date` | 转换 | 公开日；现网该列为 varchar，按源日期写入，禁止改成 date 覆盖 |
| `dwd_patent.main_classification_ipcr` | `ipc_code` | 直接 | IPC 主分类号。**禁止**写不存在的 `dwd_patent.ipc` |
| `enterprise_patent_org_rel` | `org_id` | 关联 | 对该专利每个已命中企业各写一条 detail；按 `(org_id, patent_id)` 幂等 |

`dwd_patent` **无** `ipc` / `cpc` 列，有 `main_classification_ipcr` / `main_classification_cpc`；`citation_nums` **不存在**，是 `reference_cited_count`。宽列已 ADD：`ipc_code`/`ipc_main`←`main_classification_ipcr`，`cpc_main`←`main_classification_cpc`，`citation_count`←`reference_cited_count`。禁止把源列名 `reference_cited_count` 写成目标列。`cited_by_count` 源表无对应列，写 NULL。禁止按旧列名 `ipc`/`cpc`/`citation_nums` 施工。

#### 3.14.1.1 申请人 / 权利人 → `enterprise_patent_org_rel`

| 源 | 角色 | 目标映射 |
|---|---|---|
| `dwd_patent_applicants(patent_id, sequence, name)` | `APPLICANT` | `name = dwd_org_base_info.name_cn` 精确唯一命中后写 `org_id` |
| `dwd_patent_assignees(patent_id, sequence, name)` | `ASSIGNEE` | 同上 |
| `dwd_patent.first_applicant_name` | `APPLICANT` | 仅在 applicants 分表无对应行时作为 `sequence=1` 回退 |
| `dwd_patent.first_current_assignee_name` | `ASSIGNEE` | 仅在 assignees 分表无对应行时作为 `sequence=1` 回退 |

- 目标字段：`patent_id`、匹配所得 `org_id`、固定 `party_role`、源 `sequence`、源 `name → source_name`、`match_type='EXACT_NAME'`。
- 未命中名称写 GDF 拒绝 / 待治理清单，至少包含 `patent_id`、role、sequence、source_name、batch_ts；禁止模糊匹配、禁止去「有限公司」后缀、禁止用 `dim_org_alias` 自动入库。
- 2026-09-02「精确匹配覆盖 3161 件 / 1533 家」只作当时样本，**不作验收线**。未命中比例不设上限，未命中进清单。

#### 3.14.2 `dwd_patent` → `enterprise_patent_history`（指标表）

**Q-WP3-28**：`patent_invention_count` / `latest_patent_date` / `latest_grant_date` **正式库已 ADD**。计数列能从明细算出则洗（申请/授权/有效/引用/发明），不编。这是计数覆盖，不是指标 8 件套计算。

```sql
SELECT
    org_id,
    YEAR(filing_date) AS data_year,
    COUNT(*) AS patent_apply_count
FROM enterprise_patent_detail
WHERE filing_date IS NOT NULL
GROUP BY org_id, YEAR(filing_date)
```

#### 3.14.3 `enterprise_chain_patent`（本期不洗，Q-WP3-19）

设计源是 **`dwd_org_industry_chain_pat_dtl`**（链 × 环节专利明细，行上已有 `chain_code` / `node_id`），不是 `dwd_patent`。

2026-09-02：live `gkx` 与要素库 CSV/xlsx **均无** `pat_dtl`。旧稿「`dwd_patent.ipc` → IPC 对照表」**作废**——专利表无 `ipc` 列，对照表也不存在，禁止硬推。

本期不贴不洗。`enterprise_chain_patent` 保持空表。专利明细 / `patent_org_rel` / `enterprise_patent_history` 不受影响。表到位后再按源表字段直映，未命中企业不造 `org_id`。

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
| `table_data_source` | `data_source` | 源列名是 `table_data_source`，不是 `source_table` |
| `created_time` | `create_time` | 源列名是 `created_time`，不是 `create_time` |
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

#### 3.15.5 `dwd_forg_shareholder_info` → `enterprise_forg_invest`（Q-WP3-20 维持）

2026-09-02 确认（A）：现网只有这张国外股权表，**没有**国外对外投资表。继续洗进 `enterprise_forg_invest`。已知口径=股东当投资，不另建 `enterprise_forg_shareholder`，不跟国内 Q-WP3-17 对齐拆表。

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
| `hiring_number` | `hiring_number` | `CAST(hiring_number AS CHAR)` 写入 `varchar(64)`。源列是 bigint，转失败则 NULL |
| `table_data_source` | `data_source` | 源 DDL 字段名 `table_data_source`，按业务 `data_source` 落库 |
| `created_time` | `create_time` | 创建时间 |
| `updated_time` | `update_time` | 更新时间 |
| 源无 | `id` | 自增主键 |
| `pk_id` / `creater` / `updater` | — | 不映射 |
| `is_deleted` | — | 不映射；仅作为过滤条件 |

ES / 图谱：**本期不上**（Q-WP3-15）。业务无按招聘检索；只洗 MySQL 备查。

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

### 3.19 `dwd_org_industry_product_tags` → `enterprise_industry_product`（本期洗）

2026-09-02 确认（Q-WP3-12）。live `gkx` 约 8000 行。`industry_*` / `product_*` 存的是 Python 列表字面量（如 `['INB1333','INB1306']`），不是标准 JSON。

| 源字段 | 目标字段 | 转换逻辑/说明 |
|---|---|---|
| `credit_code` | `enterprise_code` | 直接；并 JOIN `enterprise_base.enterprise_code` 取 `org_id` |
| 关联所得 | `org_id` | 仅唯一命中；未命中 NULL + 拒绝清单。**禁止**把源 `company_id` 当 `org_id` |
| `company_name` | `enterprise_name` | 直接 |
| `industry_code` | `chain_code` | 解析列表，**取第一个**；`[]` / 空 → NULL |
| `industry_name` | `chain_name` | 同上取第一个 |
| `industry_link_code` | `node_id` | 同上取第一个 |
| `industry_link_name` | `node_name` | 同上取第一个 |
| `product_name` | `product_name` | 列表展开后用顿号拼接全文（目标是 text） |
| `product_top5` | — | 目标无列，不落、不加列 |
| `company_id` / `dwd_id` / `id` / `creater` / `updater` | — | 不映射 |
| 源无 | `data_source` | 写源表名 `dwd_org_industry_product_tags` |

ES / 图谱本波无下游；只洗 MySQL DWD。

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
| 4 | 标签源表 | 源是 `gkx.dwd_org_tech_tag`，不是 `dwd_org_tag_info` | ✅ `tag_code`/`tag_name` 落 `org_tag` 中文原文；`tag_dict` 空则 `tag_category` 为 NULL。禁止编造码 |
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
