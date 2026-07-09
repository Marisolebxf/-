# 科技专题-企业模块 DWD 表结构设计

> 版本：v2.0 | 日期：2026-07-07 | 作者：[agent:data-agent]
> 范围：科技专题服务系统 - 企业检索 + 企业详情模块
> 数据库：PostgreSQL | Schema：dwd
> 约定：所有表统一 id BIGSERIAL 自增主键 + create_time + update_time
> 数据量级：企业主表约 2 亿行，司法/招投标等明细表亿级以上

## 1. 设计方法

从原型图企业模块的业务页面出发，明确每个页面/模块需要展示什么数据，再对照 ODS 实际表结构，推导出 DWD 应该有哪些表、哪些字段。

推导链路：**原型图页面 → 展示字段 → ODS 来源 → DWD 表**

### 1.1 企业标识体系

ODS 存在两套企业标识体系，DWD 统一以 `org_id` 为业务主键：


| 体系    | 主键                    | 来源表                          | 统一信用代码字段      |
| ----- | --------------------- | ---------------------------- | ------------- |
| 机构口径  | `org_id` (VARCHAR)    | `dwd_org_reg_info`           | `external_id` |
| 工商口径  | `id` (DOUBLE)         | `dwd_company_base`           | `credit_code` |
| 产业链口径 | `antitypic` (VARCHAR) | `dwd_org_industry_chain_dtl` | `credit_code` |


ETL 时通过 `external_id` ↔ `credit_code` 做跨体系归一。

### 1.2 评分类字段归属

原型图企业画像页有技术力分解、商业力分解、竞争力得分等模块。这些是算法产物，不属于 DWD 层，放在 ADS 层由算法服务计算。DWD 只保留可计算原始指标（专利数、研发投入等）。

### 1.3 2亿数据量级下的表设计原则


| 原则        | 说明                                               |
| --------- | ------------------------------------------------ |
| 主表拆分      | 检索列表页高频字段 vs 详情页低频字段拆开，避免列表查询扫描宽行                |
| 明细表独立     | 司法 18 类各有独立表，避免合并宽表导致十亿级行膨胀                      |
| 预聚合统计     | 风险统计走预聚合表，不扫十亿级明细表做 COUNT                        |
| org_id 索引 | 所有明细表以 `(org_id, event_date DESC)` 建索引，服务详情页分页查询 |


---

## 2. 原型图页面 → DWD 表推导


| 原型图页面/模块   | 展示内容                      | 对应 DWD 表                    | ODS 来源                                   |
| ---------- | ------------------------- | --------------------------- | ---------------------------------------- |
| 企业检索列表     | 工商基本信息、行业、地区、上市标志         | enterprise_base             | dwd_org_reg_info                         |
| 企业详情-基本信息  | 英文名、实缴资本、经营范围、地址、经纬度、上市详情 | enterprise_extra            | dwd_company_base, dwd_org_stock_base     |
| 企业检索筛选-标签  | 高企/专精特新/瞪羚等资质标签           | tag_dict + enterprise_tag   | dwd_org_tag_info, dwd_company_honor_tags |
| 企业画像-财务指标  | 最新营收、净利润、总资产等             | enterprise_finance_history  | dwd_org_annual_financial_info            |
| 企业画像-财务趋势  | 历年营收/利润趋势图                | enterprise_finance_history  | 同上                                       |
| 企业画像-技术创新  | 专利累计统计                    | enterprise_patent_history   | dwd_patent, dwd_patent_legal             |
| 企业画像-专利趋势  | 历年专利趋势图                   | enterprise_patent_history   | 同上                                       |
| 企业详情-招投标   | 招投标记录列表                   | enterprise_bid              | dwd_org_bid_info                         |
| 企业详情-司法风险  | 18类司法风险各自列表 + 统计计数        | risk_*（18张）+ risk_summary   | 18张司法风险表                                 |
| 企业详情-新闻资讯  | 企业相关资讯列表                  | enterprise_news             | dwd_org_important_news_info              |
| 企业详情-产业链位置 | 所属产业链、环节                  | enterprise_industry_chain   | dwd_org_industry_chain_dtl               |


**不做 DWD 表的模块**：技术力/商业力/竞争力得分（算法产物归 ADS）、企业合作关系（依赖 NER 无数据源）、供应链关系（同上）、母子公司（可从 ODS 临时查询）。

---

## 3. DWD 表总览（41 张表）

### 3.1 企业基本信息（2 张）


| #   | 表名               | 字段数 | 更新频率 | 说明                                   |
| --- | ---------------- | --- | ---- | ------------------------------------ |
| 1   | enterprise_base  | 19  | 年更   | 检索列表页高频字段（名称/代码/行业/地区/成立/状态/上市标志/资本） |
| 2   | enterprise_extra | 16  | 年更   | 详情页低频字段（英文名/实缴/经营范围/地址/经纬度/上市详情）     |


**拆分理由**：2亿行主表，列表页只查 base（19 字段窄表），详情页按需 JOIN extra。避免列表查询扫描含 TEXT 大字段（business_scope 等）的宽行。

### 3.2 企业画像（6 张）


| #   | 表名                          | 字段数 | 更新频率 | 说明                      |
| --- | --------------------------- | --- | ---- | ----------------------- |
| 3   | tag_dict                    | 10  | 极低频  | 标签字典（通用，资质/荣誉/规模/产业/特色） |
| 4   | enterprise_tag              | 7   | 季更   | 企业-标签关联（多对多）            |
| 5   | enterprise_finance_history  | 15  | 年追加  | 历年财务（画像页取最新年份，趋势图取全部） |
| 6   | enterprise_patent_history   | 12  | 年追加  | 历年专利统计（画像页取最新年份或SUM全部，趋势图取全部） |
| 7   | enterprise_patent_detail    | 28  | 日追加  | 专利明细（详情页知识产权Tab走PG查询，不走ES） |
| 8   | enterprise_executive        | 7   | 季更   | 高管信息（详情页主要团队Tab） |


### 3.3 企业明细（6 张）


| #   | 表名                           | 字段数 | 更新频率 | 说明                       |
| --- | ---------------------------- | --- | ---- | ------------------------ |
| 9   | enterprise_bid               | 16  | 日追加  | 招投标记录                    |
| 10  | enterprise_news              | 12  | 日追加  | 新闻资讯                     |
| 11  | enterprise_industry_chain    | 11  | 季更   | 产业链归属                    |
| 12  | enterprise_financing         | 11  | 日追加  | 融资事件（详情页融资历程）            |
| 13  | enterprise_innovation_carrier | 13  | 季更   | 创新载体（详情页资质荣誉Tab）         |
| 14  | enterprise_invest            | 11  | 季更   | 对外投资（详情页供应链关系Tab）        |


### 3.4 企业评分（1 张，ADS 层）


| #   | 表名              | 字段数 | 更新频率 | 说明                                    |
| --- | ---------------- | --- | ---- | ------------------------------------- |
| 15  | enterprise_score | 10  | 按算法  | ADS 层评分（竞争力分/规模/链位/风险等级），算法产出后 ETL 写入 |


### 3.5 司法风险（26 张）


| #   | 表名                              | 字段数 | 更新频率 | 说明                         | ODS 来源                                    |
| --- | ------------------------------- | --- | ---- | -------------------------- | ----------------------------------------- |
| 16  | risk_type_dict                  | 10  | 极低频  | 风险类型字典（通用）                 | -                                         |
| 17  | enterprise_risk_summary         | 9   | 日更   | 风险统计汇总（org_id × risk_type） | 各明细表预聚合                                   |
| 18  | risk_judicial_case              | 16  | 日追加  | 司法案件                       | dwd_org_opt_judicial_case                 |
| 19  | risk_dishonest                  | 16  | 日追加  | 失信被执行人                     | dwd_org_risk_shixin                       |
| 20  | risk_executed                   | 16  | 日追加  | 被执行人                       | dwd_org_risk_zhixing                      |
| 21  | risk_limit_high                 | 16  | 日追加  | 限制高消费                      | dwd_org_risk_xianxiao                     |
| 22  | risk_lawsuit                    | 14  | 日追加  | 裁判文书-案件详情                  | dwd_org_risk_lawsuit                      |
| 23  | risk_lawsuit_party              | 7   | 日追加  | 裁判文书-当事人关联                 | dwd_org_risk_lawsuit_list                 |
| 24  | risk_court_filed                | 15  | 日追加  | 法院立案-案件详情                  | dwd_org_risk_court_filed_case             |
| 25  | risk_court_filed_party          | 7   | 日追加  | 法院立案-当事人关联                 | dwd_org_risk_court_filed_litigant         |
| 26  | risk_court_notice               | 13  | 日追加  | 开庭公告-案件详情                  | dwd_org_risk_court_notice                 |
| 27  | risk_court_notice_party         | 7   | 日追加  | 开庭公告-当事人关联                 | dwd_org_risk_court_notice_list            |
| 28  | risk_court_announcement         | 14  | 日追加  | 法院公告-案件详情                  | dwd_org_risk_court_announcement           |
| 29  | risk_court_announcement_party   | 7   | 日追加  | 法院公告-当事人关联                 | dwd_org_risk_court_announcement_list      |
| 30  | risk_equity_freeze              | 16  | 日追加  | 股权冻结                       | dwd_org_company_justice                   |
| 31  | risk_equity_pledge              | 16  | 日追加  | 股权出质                       | dwd_org_company_pledge                    |
| 32  | risk_zhongben                   | 16  | 日追加  | 终本案件                       | dwd_org_risk_zhongben                     |
| 33  | risk_chattel_mortgage           | 17  | 日追加  | 动产抵押                       | dwd_org_company_chattel                   |
| 34  | risk_judicial_sale              | 16  | 日追加  | 司法拍卖-案件详情                  | dwd_org_tb_judicial_sale                  |
| 35  | risk_judicial_sale_party        | 7   | 日追加  | 司法拍卖-当事人关联                 | dwd_org_tb_judicial_sale_info_company     |
| 36  | risk_bankruptcy                 | 12  | 日追加  | 破产案件-案件详情                  | dwd_org_bankruptcy_public_cases           |
| 37  | risk_bankruptcy_party           | 7   | 日追加  | 破产案件-当事人关联                 | dwd_org_bankruptcy_public_cases_list      |
| 38  | risk_abnormal                   | 15  | 日追加  | 经营异常                       | dwd_org_company_abnormal                  |
| 39  | risk_punishment                 | 17  | 日追加  | 行政处罚                       | dwd_org_company_punish                    |
| 40  | risk_illegal                    | 15  | 日追加  | 严重违法                       | dwd_org_company_illegal                   |
| 41  | risk_tax_punish                 | 15  | 日追加  | 税收违法                       | dwd_org_risk_tax_punish                   |


**拆分理由**：2亿企业下司法明细总量可能达十亿级。合并为一张宽表会导致：

1. 单表行数爆炸，VACUUM 和索引膨胀严重
2. 查某类风险时扫描全表（即使有 risk_type 索引，回表代价也高）
3. 各类风险字段差异大，合并后大量 NULL 列浪费存储

拆为 24 张独立明细表后，每张表行数可控。其中：
- **12 张单企业维度表**：按 `(org_id, event_date DESC)` 索引精准命中
- **6 类 × 2 = 12 张案件+当事人拆分表**：案件详情表不冗余存储，当事人关联表通过 `org_id` 索引命中后 JOIN 详情表

**通用统计表设计**：

- `risk_type_dict`：风险类型字典，统一注册所有风险类型（含 risk_type 编码、中文名、大类、ODS 来源表、事件日期字段名）
- `enterprise_risk_summary`：按 `org_id × risk_type` 预聚合，存 total_count / current_count / history_count / latest_date。检索页筛选风险等级、详情页展示风险计数都查这张表，不扫明细。

---

## 4. 逐表字段设计

### 4.1 dwd.enterprise_base（企业核心信息，19 字段）

**原型图位置**：企业检索列表（名称/行业/地区/上市/成立年份筛选+排序）
**更新频率**：年更
**ODS 来源**：`dwd_org_reg_info`（主）、`dwd_company_base`（补全企业类型）


| #   | 字段名                  | 类型            | 可空  | 备注            | ODS 来源                                                 |
| --- | -------------------- | ------------- | --- | ------------- | ------------------------------------------------------ |
| 1   | id                   | bigserial     | 否   | 自增主键          | -                                                      |
| 2   | org_id               | varchar(64)   | 否   | 机构id（业务主键，唯一） | dwd_org_reg_info.org_id                                |
| 3   | enterprise_code      | varchar(64)   | 否   | 统一社会信用代码      | dwd_org_reg_info.external_id                           |
| 4   | enterprise_name      | varchar(255)  | 否   | 企业全称          | dwd_org_reg_info.name_cn                               |
| 5   | legal_representative | varchar(100)  | 是   | 法定代表人         | dwd_org_reg_info.lerep                                 |
| 6   | registration_date    | date          | 是   | 成立日期          | dwd_org_reg_info.incorporation_date                    |
| 7   | business_status      | varchar(20)   | 是   | 经营状态          | dwd_company_base.status_std                            |
| 8   | enterprise_type      | varchar(100)  | 是   | 企业类型          | dwd_company_base.first_type/second_type                |
| 9   | industry_category    | varchar(100)  | 是   | 所属行业          | dwd_org_org_product_info.industry_class                |
| 10  | industry_code        | varchar(20)   | 是   | 行业代码          | dwd_company_nei_code.industry_l1_code                  |
| 11  | province             | varchar(50)   | 是   | 省份            | dwd_org_reg_info.province                              |
| 12  | city                 | varchar(50)   | 是   | 城市            | dwd_org_reg_info.city                                  |
| 13  | district             | varchar(50)   | 是   | 区县            | dwd_company_base.ori_reg_district                      |
| 14  | registered_capital   | numeric(18,2) | 是   | 注册资本（万元）      | dwd_org_reg_info.registered_capital_value（元→万元 /10000） |
| 15  | is_listed            | smallint      | 是   | 是否上市（0否/1是）   | dwd_org_stock_base 存在记录则=1                             |
| 16  | org_size             | varchar(20)   | 是   | 企业规模          | dwd_org_reg_info.org_size                              |
| 17  | data_source          | varchar(100)  | 是   | 数据来源          | 各源表 data_source                                        |
| 18  | create_time          | timestamp     | 否   | 记录创建时间        | 系统填充                                                   |
| 19  | update_time          | timestamp     | 否   | 记录更新时间（ETL）   | 系统填充                                                   |


### 4.2 dwd.enterprise_extra（企业扩展信息，16 字段）

**原型图位置**：企业详情-基本信息卡（详情页才展示的低频字段）
**更新频率**：年更
**ODS 来源**：`dwd_company_base`、`dwd_org_stock_base`、`dwd_company_location_tags`


| #   | 字段名                  | 类型            | 可空  | 备注          | ODS 来源                                   |
| --- | -------------------- | ------------- | --- | ----------- | ---------------------------------------- |
| 1   | id                   | bigserial     | 否   | 自增主键        | -                                        |
| 2   | org_id               | varchar(64)   | 否   | 机构id（唯一）    | -                                        |
| 3   | enterprise_name_en   | varchar(255)  | 是   | 英文名称        | dwd_company_base.english_name            |
| 4   | paid_in_capital      | numeric(18,2) | 是   | 实缴资本（万元）    | dwd_company_base.real_capital_std        |
| 5   | business_scope       | text          | 是   | 经营范围        | dwd_org_org_product_info.main_activities |
| 6   | registered_address   | varchar(500)  | 是   | 注册地址        | dwd_org_reg_info.address                 |
| 7   | headquarters_address | varchar(500)  | 是   | 总部详细地址      | 同 registered_address                     |
| 8   | lng                  | numeric(10,6) | 是   | 经度          | dwd_org_reg_info.addr_lng                |
| 9   | lat                  | numeric(10,6) | 是   | 纬度          | dwd_org_reg_info.addr_lat                |
| 10  | listed_market        | varchar(50)   | 是   | 上市板块        | dwd_org_stock_base.stock_type            |
| 11  | listed_code          | varchar(20)   | 是   | 股票代码        | dwd_org_stock_base.stock_code            |
| 12  | listed_date          | date          | 是   | 上市日期        | dwd_org_stock_base.listed_date           |
| 13  | data_source          | varchar(100)  | 是   | 数据来源        | -                                        |
| 14  | create_time          | timestamp     | 否   | 记录创建时间      | 系统填充                                     |
| 15  | update_time          | timestamp     | 否   | 记录更新时间（ETL） | 系统填充                                     |


**与 base 的关系**：一对一，通过 org_id 关联。列表页只查 base，详情页 JOIN extra。

### 4.3 dwd.tag_dict（标签字典表，10 字段）

**原型图位置**：企业检索筛选-标签 facets（标签选项来源）+ 企业画像-资质标签展示
**更新频率**：极低频（新增标签类型才更新）
**ODS 来源**：ETL 从 `dwd_org_tag_info.org_tag`、`dwd_company_honor_tags.`*、`dwd_company_diy_tags.diy_tag` 动态发现后追加


| #   | 字段名          | 类型           | 可空  | 备注                                                             |
| --- | ------------ | ------------ | --- | -------------------------------------------------------------- |
| 1   | id           | bigserial    | 否   | 自增主键                                                           |
| 2   | tag_code     | varchar(100) | 否   | 标签编码（唯一，如 high_tech / little_giant / gazelle）                  |
| 3   | tag_name     | varchar(255) | 否   | 标签中文名称                                                         |
| 4   | tag_category | varchar(50)  | 否   | 标签大类（qualification资质 / honor荣誉 / scale规模 / industry产业 / diy特色） |
| 5   | tag_level    | varchar(50)  | 是   | 标签级别（national / province / city / district，荣誉类适用）              |
| 6   | ods_source   | varchar(255) | 是   | ODS 来源表名                                                       |
| 7   | sort_order   | integer      | 是   | 排序序号                                                           |
| 8   | is_active    | smallint     | 否   | 是否启用（0/1）                                                      |
| 9   | create_time  | timestamp    | 否   | 记录创建时间                                                         |
| 10  | update_time  | timestamp    | 否   | 记录更新时间                                                         |


**设计说明**：已预置 11 条常见标签（高企/专精特新/瞪羚/独角兽/小微/外资/国家级荣誉/省级荣誉/市级荣誉/区县级荣誉/资质认证）。其余标签由 ETL 从 ODS 动态发现后追加。新增标签类型不需要改表结构，只加字典记录。

### 4.4 dwd.enterprise_tag（企业-标签关联表，7 字段）

**原型图位置**：企业检索筛选-标签 facets + 企业画像-资质标签展示
**更新频率**：季更
**ODS 来源**：`dwd_org_tag_info`（一行一标签，直接映射）、`dwd_company_honor_tags`（JSON 解析展开）、`dwd_company_basic_tags`、`dwd_company_diy_tags`


| #   | 字段名         | 类型           | 可空  | 备注                                |
| --- | ----------- | ------------ | --- | --------------------------------- |
| 1   | id          | bigserial    | 否   | 自增主键                              |
| 2   | org_id      | varchar(64)  | 否   | 机构id                              |
| 3   | tag_code    | varchar(100) | 否   | 标签编码（关联 tag_dict）                 |
| 4   | tag_value   | varchar(500) | 是   | 标签值/明细（如专精特新级别"国家级"、荣誉标签具体名称，可为空） |
| 5   | create_time | timestamp    | 否   | 记录创建时间                            |
| 6   | update_time | timestamp    | 否   | 记录更新时间（ETL）                       |


**唯一约束**：(org_id, tag_code, tag_value) — 同一企业同一标签同一值只有一条。

**设计说明**：

- 多对多模型：一家企业可有多个标签，一个标签可关联多家企业
- 检索页按 `tag_code` 筛选（如筛选"高企"，JOIN enterprise_tag WHERE tag_code='high_tech'）
- 详情页按 `org_id` 查全部标签（SELECT * FROM enterprise_tag WHERE org_id=?）
- `tag_value` 存标签明细（如专精特新的级别"国家级"/"省级"，荣誉标签的具体名称"2024年度优秀企业"），布尔型标签（如 high_tech）此字段留空
- 相比原 `enterprise_qualification` 方案：不需要加新标签就改表结构，标签可索引可聚合，JSON 大字段消除

### 4.5 dwd.enterprise_finance_history（企业财务历史，15 字段）

**原型图位置**：企业画像-财务指标卡片（取最新年份）+ 财务趋势图（取全部年份）
**更新频率**：年追加
**ODS 来源**：`dwd_org_annual_financial_info`（年报，VARCHAR 需转换）、`dwd_org_stock_finance_info`（上市财务，DOUBLE）
**唯一约束**：(org_id, data_year, data_source)

| # | 字段名 | 类型 | 可空 | 备注 | ODS 来源 |
|---|--------|------|------|------|----------|
| 1 | id | bigserial | 否 | 自增主键 | - |
| 2 | org_id | varchar(64) | 否 | 机构id | - |
| 3 | data_year | integer | 否 | 数据年份 | annual.year / stock.occur_period 提取年 |
| 4 | revenue | numeric(18,2) | 是 | 营收（万元） | annual.operating_revenue 或 stock.operating_revenue（元→万元 /10000） |
| 5 | net_profit | numeric(18,2) | 是 | 净利润（万元） | annual.pure_profit 或 stock.pure_profit |
| 6 | total_assets | numeric(18,2) | 是 | 总资产（万元） | annual.total_assets 或 stock.total_assets |
| 7 | total_liabilities | numeric(18,2) | 是 | 总负债（万元） | annual.total_liabilities 或 stock.total_liabilities |
| 8 | total_tax | numeric(18,2) | 是 | 纳税总额（万元） | annual.total_tax_paid |
| 9 | rd_investment | numeric(18,2) | 是 | 研发投入（万元） | stock.research_development_amount |
| 10 | employees_number | integer | 是 | 从业人数 | annual.employees_number（VARCHAR 转 int） |
| 11 | owners_equity | numeric(18,2) | 是 | 所有者权益（万元） | annual.owners_equity |
| 12 | data_source | varchar(50) | 是 | 数据来源（annual/stock） | - |
| 13 | create_time | timestamp | 否 | 记录创建时间 | 系统填充 |
| 14 | update_time | timestamp | 否 | 记录更新时间（ETL） | 系统填充 |

**设计说明**：不单独建快照表。画像页财务指标卡片直接从 history 取最新年份：

```sql
SELECT * FROM dwd.enterprise_finance_history
WHERE org_id = ? ORDER BY data_year DESC LIMIT 1;
```

`(org_id, data_year)` 有唯一约束 + 索引，2亿企业下也是毫秒级查询。趋势图取全部年份。上市企业优先取 stock 来源（字段为 DOUBLE 更规范），非上市取 annual（VARCHAR 需 CAST）。


### 4.6 dwd.enterprise_patent_history（企业专利历史，12 字段）

**原型图位置**：企业画像-技术创新模块（专利累计统计卡片，取最新年份或 SUM 全部）+ 专利趋势图（取全部年份）
**更新频率**：年追加
**ODS 来源**：`dwd_patent`、`dwd_patent_legal`、`dwd_patent_cited`
**唯一约束**：(org_id, data_year)

| # | 字段名 | 类型 | 可空 | 备注 | ODS 来源 |
|---|--------|------|------|------|----------|
| 1 | id | bigserial | 否 | 自增主键 | - |
| 2 | org_id | varchar(64) | 否 | 机构id | - |
| 3 | data_year | integer | 否 | 数据年份 | dwd_patent 申请日期提取年 |
| 4 | patent_apply_count | integer | 是 | 当年申请数 | dwd_patent 按年 COUNT |
| 5 | patent_grant_count | integer | 是 | 当年授权数 | dwd_patent_legal 按年 COUNT |
| 6 | patent_valid_count | integer | 是 | 当年有效数 | dwd_patent_legal 按年 |
| 7 | patent_invention_count | integer | 是 | 当年发明专利数 | dwd_patent application_kind 过滤 |
| 8 | patent_citation_count | integer | 是 | 当年被引次数 | dwd_patent_cited 按年 |
| 9 | latest_patent_date | date | 是 | 当年最新专利申请日期 | dwd_patent.application_reference_3 |
| 10 | latest_grant_date | date | 是 | 当年最新授权日期 | dwd_patent_legal.dates_of_public_availability |
| 11 | create_time | timestamp | 否 | 记录创建时间 | 系统填充 |
| 12 | update_time | timestamp | 否 | 记录更新时间（ETL） | 系统填充 |

**设计说明**：不单独建汇总表。画像页专利卡片从 history 取最新年份或 SUM 全部年份：

```sql
-- 累计总数：SUM 全部年份（专利历史一般10-20年，代价很小）
SELECT SUM(patent_apply_count), SUM(patent_grant_count), SUM(patent_invention_count)
FROM dwd.enterprise_patent_history WHERE org_id = ?;

-- 最新日期：取最新年份的 latest_patent_date / latest_grant_date
SELECT latest_patent_date, latest_grant_date FROM dwd.enterprise_patent_history
WHERE org_id = ? ORDER BY data_year DESC LIMIT 1;
```

趋势图取全部年份。`(org_id, data_year)` 有唯一约束 + 索引。

**⚠️ 实体归一前置**：`dwd_patent` 无 org_id，只有申请人文本，需建机构名→org_id 映射表。

### 4.7 dwd.enterprise_patent_detail（企业专利明细，28 字段）

**原型图位置**：企业详情页-知识产权 Tab（专利明细列表，走 PG 查询不走 ES）
**更新频率**：日追加
**ODS 来源**：`dwd_patent`（主表）+ `dwd_patent_title`（标题）+ `dwd_patent_abstract`（摘要）+ `dwd_patent_cited`（引用关系）
**唯一约束**：(org_id, patent_id)

| # | 字段名 | 类型 | 可空 | 备注 | ODS 来源 |
|---|--------|------|------|------|----------|
| 1 | id | bigserial | 否 | 自增主键 | - |
| 2 | org_id | varchar(64) | 否 | 机构id（ETL通过申请人名称映射） | 映射表 |
| 3 | patent_id | varchar(64) | 否 | 专利id | dwd_patent.patent_id |
| 4 | publication_number | varchar(64) | 是 | 专利公布号 | dwd_patent.publication_number |
| 5 | title_zh | varchar(1024) | 是 | 中文标题 | dwd_patent_title.title_zh |
| 6 | title_en | varchar(1024) | 是 | 英文标题 | dwd_patent_title.title_localized_2 |
| 7 | abstract_zh | text | 是 | 中文摘要 | dwd_patent_abstract |
| 8 | patent_type | varchar(10) | 是 | 申请类型（A=发明/U=实用/F=外观/W=PCT） | dwd_patent.application_kind |
| 9 | country | varchar(20) | 是 | 国家 | dwd_patent.country |
| 10 | filing_date | date | 是 | 申请日期 | dwd_patent.application_reference_3 |
| 11 | filing_year | integer | 是 | 申请年份 | dwd_patent.application_reference_4 |
| 12 | publication_date | date | 是 | 公开日期 | dwd_patent.publication_reference_2 |
| 13 | publication_year | integer | 是 | 公开年份 | dwd_patent.publication_reference_3 |
| 14 | grant_date | date | 是 | 授权日期 | ETL推导 |
| 15 | grant_year | integer | 是 | 授权年份 | ETL推导 |
| 16 | grant_number | varchar(64) | 是 | 授权号 | dwd_patent.granted_number |
| 17 | ipc_main | varchar(32) | 是 | IPC主分类号 | dwd_patent.classification_ipcr |
| 18 | cpc_main | varchar(32) | 是 | CPC主分类号 | dwd_patent.classification_cpc |
| 19 | inventor | varchar(500) | 是 | 发明人 | dwd_patent.inventors_2 |
| 20 | applicant_name | varchar(255) | 是 | 原始申请人名称 | dwd_patent.applicants_2 |
| 21 | assignee_name | varchar(255) | 是 | 当前专利权人名称 | dwd_patent.assignees_2 |
| 22 | legal_status | varchar(50) | 是 | 法律状态（有效/无效/审查中） | ETL推导 |
| 23 | citation_count | integer | 是 | 引用专利数量 | dwd_patent_cited.reference_cited |
| 24 | cited_by_count | integer | 是 | 被引数量 | dwd_patent_cited.cited_by_nums |
| 25 | detail_json | text | 是 | ODS原始完整记录（JSON） | dwd_patent全字段 |
| 26 | data_source | varchar(100) | 是 | 数据来源 | dwd_patent.db_source |
| 27 | create_time | timestamp | 否 | 记录创建时间 | 系统填充 |
| 28 | update_time | timestamp | 否 | 记录更新时间（ETL） | 系统填充 |

**设计说明**：专利明细走 PG 查询，不灌入 ES。详情页知识产权 Tab 按 `org_id` 分页查询，按 `filing_date DESC` 排序：

```sql
SELECT patent_id, publication_number, title_zh, patent_type, filing_date,
       grant_date, legal_status, ipc_main, inventor, cited_by_count
FROM dwd.enterprise_patent_detail
WHERE org_id = ?
ORDER BY filing_date DESC
LIMIT 20 OFFSET ?;
```

索引 `(org_id, filing_date DESC)` 支持分页倒序查询。大企业可能几万条专利，PG 分页 + 索引效率可接受。

**⚠️ 实体归一前置**：同 patent_history，ODS `dwd_patent` 无 org_id，ETL 需通过 `assignees_2`/`applicants_2` 名称映射到 org_id。

### 4.8 dwd.enterprise_executive（企业高管信息，7 字段）

**原型图位置**：企业详情页-主要团队 Tab（姓名/职务表格）
**更新频率**：季更
**ODS 来源**：`dwd_org_executive_info`
**唯一约束**：(org_id, executive_name, position)

| # | 字段名 | 类型 | 可空 | 备注 | ODS 来源 |
|---|--------|------|------|------|----------|
| 1 | id | bigserial | 否 | 自增主键 | - |
| 2 | org_id | varchar(64) | 否 | 机构id | dwd_org_executive_info.org_id |
| 3 | executive_name | varchar(255) | 否 | 高管姓名 | executives_name |
| 4 | position | varchar(255) | 是 | 职位名称 | executives_position |
| 5 | data_source | varchar(100) | 是 | 数据来源 | data_source |
| 6 | create_time | timestamp | 否 | 记录创建时间 | 系统填充 |
| 7 | update_time | timestamp | 否 | 记录更新时间（ETL） | 系统填充 |

**设计说明**：ODS 源表已含 org_id，ETL 直接搬即可。数据量小（一家企业 5-30 人），同时灌入 ES `executives` nested。

### 4.9 dwd.enterprise_bid（企业招投标明细，16 字段）

**原型图位置**：企业详情-招投标记录列表
**更新频率**：日追加
**ODS 来源**：`dwd_org_bid_info`


| #   | 字段名                  | 类型            | 可空  | 备注             | ODS 来源               |
| --- | -------------------- | ------------- | --- | -------------- | -------------------- |
| 1   | id                   | bigserial     | 否   | 自增主键           | -                    |
| 2   | org_id               | varchar(64)   | 否   | 关联企业id（中标方）    | winner_org_id        |
| 3   | enterprise_name      | varchar(255)  | 是   | 中标企业名称         | winner_name_cn       |
| 4   | tender_org_id        | varchar(64)   | 是   | 采购单位id         | tender_org_id        |
| 5   | tender_name          | varchar(255)  | 是   | 采购单位名称         | tender_name_cn       |
| 6   | role                 | varchar(20)   | 是   | 本企业角色（中标方/采购方） | -                    |
| 7   | announcement_title   | text          | 是   | 公告标题           | announcement_title   |
| 8   | announcement_content | text          | 是   | 中标成交信息         | announcement_content |
| 9   | announcement_date    | date          | 是   | 公告日期           | ⚠️ ODS 无此字段          |
| 10  | winning_amount       | numeric(18,2) | 是   | 中标金额（万元）       | ⚠️ ODS 无此字段          |
| 11  | project_name         | varchar(500)  | 是   | 项目名称           | ⚠️ ODS 无此字段          |
| 12  | project_no           | varchar(100)  | 是   | 项目编号           | ⚠️ ODS 无此字段          |
| 13  | data_source          | varchar(100)  | 是   | 数据来源           | data_source          |
| 14  | create_time          | timestamp     | 否   | 记录创建时间         | -                    |
| 15  | update_time          | timestamp     | 否   | 记录更新时间（ETL）    | -                    |


### 4.10 dwd.enterprise_news（企业新闻资讯，12 字段）

**原型图位置**：企业详情-新闻资讯列表
**更新频率**：日追加
**ODS 来源**：`dwd_org_important_news_info`


| #   | 字段名                 | 类型           | 可空  | 备注              |
| --- | ------------------- | ------------ | --- | --------------- |
| 1   | id                  | bigserial    | 否   | 自增主键            |
| 2   | org_id              | varchar(64)  | 否   | 关联企业id          |
| 3   | enterprise_name     | varchar(255) | 是   | 企业名称            |
| 4   | news_title          | text         | 是   | 资讯标题            |
| 5   | news_date           | date         | 是   | 资讯日期            |
| 6   | news_content        | text         | 是   | 资讯内容            |
| 7   | original_url        | text         | 是   | 原文链接            |
| 8   | data_source         | varchar(100) | 是   | 数据来源            |
| 9   | source_created_time | timestamp    | 是   | ODS原始入库时间（业务字段） |
| 10  | create_time         | timestamp    | 否   | 记录创建时间          |
| 11  | update_time         | timestamp    | 否   | 记录更新时间（ETL）     |


### 4.11 dwd.enterprise_industry_chain（企业产业链归属，11 字段）

**原型图位置**：企业详情-产业链位置
**更新频率**：季更
**唯一约束**：(org_id, chain_code, node_id)

字段：id / org_id / enterprise_code / chain_code / chain_name / node_id / node_name / node_stage（上游/中游/下游）/ chain_score / create_time / update_time

### 4.12 dwd.enterprise_financing（企业融资事件，11 字段）

**原型图位置**：企业详情页-融资历程
**更新频率**：日追加
**ODS 来源**：`dwd_org_financing_info`
**唯一约束**：无（同一企业可多轮融资，同轮次可多次）

| # | 字段名 | 类型 | 可空 | 备注 | ODS 来源 |
|---|--------|------|------|------|----------|
| 1 | id | bigserial | 否 | 自增主键 | - |
| 2 | org_id | varchar(64) | 否 | 机构id | org_id |
| 3 | funding_round | varchar(255) | 是 | 融资轮次（天使轮/A轮/B轮等） | funding_round |
| 4 | funding_amount | numeric(18,2) | 是 | 获投金额（元） | funding_amount |
| 5 | funding_currency_code | varchar(20) | 是 | 币种 | funding_currency_code |
| 6 | post_valuation | numeric(18,2) | 是 | 投后估值（元） | post_valuation |
| 7 | completion_date | date | 是 | 融资完成时间 | completion_date |
| 8 | investors_name | text | 是 | 投资方列表（逗号分隔） | investors_name |
| 9 | data_source | varchar(100) | 是 | 数据来源 | data_source |
| 10 | create_time | timestamp | 否 | 记录创建时间 | 系统填充 |
| 11 | update_time | timestamp | 否 | 记录更新时间（ETL） | 系统填充 |

**设计说明**：ODS 源表已含 org_id，ETL 直接搬。数据量中等（1-30条/企业），同时灌入 ES `financings` nested。

### 4.13 dwd.enterprise_innovation_carrier（企业创新载体，13 字段）

**原型图位置**：企业详情页-资质荣誉 Tab（创新载体部分）
**更新频率**：季更
**ODS 来源**：`dwd_innovation_carrier`
**唯一约束**：(org_id, carrier_name, carrier_type)

| # | 字段名 | 类型 | 可空 | 备注 | ODS 来源 |
|---|--------|------|------|------|----------|
| 1 | id | bigserial | 否 | 自增主键 | - |
| 2 | org_id | varchar(64) | 否 | 机构id | org_id |
| 3 | carrier_type | varchar(255) | 是 | 载体类型（重点实验室/工程中心等） | carrier_type |
| 4 | carrier_name | varchar(500) | 是 | 载体名称 | carrier_name |
| 5 | carrier_level | varchar(50) | 是 | 级别（国家级/省级/市级） | carrier_level |
| 6 | establish_year | varchar(20) | 是 | 组建/认定年份 | establish_year |
| 7 | region | varchar(255) | 是 | 所在地区 | region |
| 8 | publish_org | varchar(500) | 是 | 发布单位 | publish_org |
| 9 | publish_date | varchar(20) | 是 | 发布日期 | publish_date |
| 10 | source_url | text | 是 | 来源链接 | source_url |
| 11 | create_time | timestamp | 否 | 记录创建时间 | 系统填充 |
| 12 | update_time | timestamp | 否 | 记录更新时间（ETL） | 系统填充 |

**设计说明**：ODS 源表已含 org_id（可空，ETL 需过滤无 org_id 的记录）。数据量小（1-20条/企业），同时灌入 ES `innovation_carriers` nested。ODS 的 `publish_date` 为 VARCHAR，DWD 保持原样不做类型转换。

### 4.14 dwd.enterprise_invest（企业对外投资，11 字段）

**原型图位置**：企业详情页-供应链关系 Tab（投资方→被投企业关系）
**更新频率**：季更
**ODS 来源**：`dwd_org_invest_info`
**唯一约束**：(org_id, inv_org_id)

| # | 字段名 | 类型 | 可空 | 备注 | ODS 来源 |
|---|--------|------|------|------|----------|
| 1 | id | bigserial | 否 | 自增主键 | - |
| 2 | org_id | varchar(64) | 否 | 投资方机构id | org_id |
| 3 | inv_org_id | varchar(64) | 是 | 被投企业id | inv_org_id |
| 4 | inv_name | varchar(255) | 是 | 被投资企业名称 | inv_name |
| 5 | inv_external_id | varchar(64) | 是 | 被投企业信用代码 | inv_external_id |
| 6 | investment_amount | numeric(18,2) | 是 | 投资金额（元） | investment_amount |
| 7 | investment_ratio | numeric(8,4) | 是 | 股权占比（%） | investment_ratio |
| 8 | data_source | varchar(100) | 是 | 数据来源 | data_source |
| 9 | create_time | timestamp | 否 | 记录创建时间 | 系统填充 |
| 10 | update_time | timestamp | 否 | 记录更新时间（ETL） | 系统填充 |

**设计说明**：ODS 源表已含 org_id 和 inv_org_id，ETL 直接搬。同时灌入 ES `supply_chain_relations` nested（relation_type="投资方"）。反向查询（谁投资了我）通过 `inv_org_id` 索引实现。

### 4.15 dwd.enterprise_score（企业评分，10 字段，ADS 层）

**原型图位置**：搜索结果卡片（竞争力分排序）、高级筛选（规模/风险等级）、卡片展示（链位文本）
**更新频率**：按算法产出周期（暂定季更，算法就绪后 ETL 写入）
**数据来源**：算法侧（ai-service）计算产出，ETL 搬入此表
**唯一约束**：(org_id)

| # | 字段名 | 类型 | 可空 | 备注 |
|---|--------|------|------|------|
| 1 | id | bigserial | 否 | 自增主键 |
| 2 | org_id | varchar(64) | 否 | 机构id |
| 3 | competitiveness_score | numeric(6,2) | 是 | 综合竞争力评分（0-100） |
| 4 | enterprise_scale | varchar(20) | 是 | 企业规模（大型/中型/小型/微型/规上） |
| 5 | chain_position_text | varchar(255) | 是 | 产业链位置文本（如"设计层 · 上游EDA"） |
| 6 | risk_level | varchar(20) | 是 | 风险等级（无风险/低风险/中风险/高风险） |
| 7 | score_version | varchar(20) | 是 | 评分模型版本 |
| 8 | score_date | date | 是 | 评分计算日期 |
| 9 | create_time | timestamp | 否 | 记录创建时间 |
| 10 | update_time | timestamp | 否 | 记录更新时间（ETL） |

**设计说明**：此表属 ADS 层，算法侧尚未实现。表结构先建好，算法就绪后 ETL 直接写入。ES 同步时从此表读取 `competitiveness_score` / `enterprise_scale` / `chain_position_text` / `risk_level` 写入 ES 顶层字段。算法就绪前这些字段为空，不影响 ES 索引正常使用。

---

## 5. 司法风险模块设计（18 张明细 + 字典 + 统计）

### 5.1 设计思路

原型图企业详情页「司法风险」模块需要：

1. **风险概览**：展示各类风险的当前/历史计数（如失信 3 条、被执行 5 条）
2. **风险明细列表**：点击某类风险后展示该类型的详细记录列表（分页）

2亿企业下司法明细可能达十亿级，如果合并为一张宽表：

- 单表行数爆炸，VACUUM 和索引膨胀严重
- 查某类风险时即使有 risk_type 索引，回表代价也高
- 各类风险字段差异大，合并后大量 NULL 列浪费存储

**方案**：18 类完全独立表 + 通用字典 + 预聚合统计表

### 5.2 dwd.risk_type_dict（风险类型字典，10 字段）

通用字典表，统一注册所有风险类型。ETL 和查询都通过 risk_type 编码关联。


| 字段名              | 类型           | 备注                                          |
| ---------------- | ------------ | ------------------------------------------- |
| id               | bigserial    | 自增主键                                        |
| risk_type        | varchar(50)  | 风险类型编码（唯一），如 dishonest / executed / lawsuit |
| risk_category    | varchar(50)  | 风险大类（judicial司法 / risk经营风险 / penalty处罚）     |
| risk_name        | varchar(100) | 风险类型中文名称                                    |
| ods_source_table | varchar(255) | ODS 来源表名                                    |
| event_date_field | varchar(100) | 事件日期取值字段名（如 filing_date / publish_date）     |
| sort_order       | integer      | 排序序号                                        |
| is_active        | smallint     | 是否启用（0/1）                                   |
| create_time      | timestamp    | 记录创建时间                                      |
| update_time      | timestamp    | 记录更新时间                                      |


已预置 18 条字典数据（见 DDL INSERT 语句）。

### 5.3 dwd.enterprise_risk_summary（企业风险统计汇总，9 字段）

按 `org_id × risk_type` 预聚合。检索页风险筛选、详情页风险计数都查这张表。


| 字段名           | 类型          | 备注                  |
| ------------- | ----------- | ------------------- |
| id            | bigserial   | 自增主键                |
| org_id        | varchar(64) | 机构id                |
| risk_type     | varchar(50) | 风险类型（关联字典表）         |
| total_count   | integer     | 该类型风险总数             |
| current_count | integer     | 当前有效数（is_history=0） |
| history_count | integer     | 历史数（is_history=1）   |
| latest_date   | date        | 最近一次事件日期            |
| create_time   | timestamp   | 记录创建时间              |
| update_time   | timestamp   | 记录更新时间              |


**唯一约束**：(org_id, risk_type)

### 5.4 司法明细表（24 张：12 张单企业维度 + 6 类×2 拆分表）

司法明细表分两类：

**A 类：单企业维度表（12 张）**

ODS 源表本身一行一企业一事件，`org_id` 直接在主表里，不存在多当事人问题。设计原则：
- `id` 自增主键 + `org_id` 关联企业 + `create_time` / `update_time`
- 只提取该类型**核心展示字段**（案号、日期、法院、金额等）
- `detail_json`（TEXT）存 ODS 原始完整记录，供详情页展开
- `is_history`（SMALLINT）标记当前/历史
- 索引统一为 `(org_id, event_date DESC)` 支持分页倒序查询

| 表名                      | risk_type          | 核心字段                                                                                         | 事件日期            | 特殊说明                     |
| ----------------------- | ------------------ | -------------------------------------------------------------------------------------------- | --------------- | ------------------------ |
| risk_judicial_case      | judicial_case      | case_id/case_no/case_title/case_cause/case_role/procedure                                    | procedure_date  | -                        |
| risk_dishonest          | dishonest          | dishonest_id/case_no/exec_court/legal_obligation/fulfillment_status                          | publish_date    | -                        |
| risk_executed           | executed           | exec_person_id/case_no/exec_court/exec_status/exec_target                                    | filing_date     | exec_target 为 VARCHAR 文本 |
| risk_limit_high         | limit_high         | xhfgk_id/rhc_person_name/case_no/doc_url                                                     | filing_date     | -                        |
| risk_equity_freeze      | equity_freeze      | judicial_assist_id/executed_person/equity_amount/exec_court/status                           | ⚠️无日期           | ODS 无日期字段                |
| risk_equity_pledge      | equity_pledge      | pledge_id/reg_no/pledgor/pledgee/equity_amount/pledge_reg_date/status                        | pledge_reg_date | equity_amount 为 VARCHAR  |
| risk_zhongben           | zhongben           | case_no/exec_court/filing_date/termination_date/exec_target_amount/unfulfilled_amount        | filing_date     | 金额字段最完整                  |
| risk_chattel_mortgage   | chattel_mortgage   | reg_no/reg_date/reg_org/guarantee_type/guarantee_amount/guarantee_scope/public_date          | reg_date        | -                        |
| risk_abnormal           | abnormal           | abnormal_id/abn_date/remove_date/reason                                                      | abn_date        | -                        |
| risk_punishment         | punishment         | penalty_id/decision_no/penalty_date/public_date/fine_amount/confiscate_amount/penalty_reason | penalty_date    | 金额字段完整                   |
| risk_illegal            | illegal            | sv_id/abn_date/remove_date/reason                                                            | abn_date        | -                        |
| risk_tax_punish         | tax_punish         | tax_vio_id/case_no/publish_date/tax_vio_type                                                 | publish_date    | ⚠️无罚款金额                  |

**B 类：案件详情 + 当事人关联拆分表（6 类 × 2 = 12 张）**

ODS 源表是"主表 + 当事人子表"结构，一个案件对应多个企业当事人（原告/被告等角色不同）。如果像 A 类那样把详情和关联塞在同一张表里，会导致**同一案件详情被冗余存储多份**（N 个当事人就存 N 份详情），在亿级数据下浪费严重。

因此拆为两张表：
- **案件详情表**（`risk_*`）：一行一个案件，案件唯一 ID 做唯一约束，**不含 org_id**
- **当事人关联表**（`risk_*_party`）：一行一个当事人，`org_id` + 案件 ID + `party_role`

查询时 JOIN 两表：`SELECT d.* FROM risk_lawsuit d JOIN risk_lawsuit_party p ON d.judgment_doc_id = p.judgment_doc_id WHERE p.org_id = ?`

| 案件详情表                     | 当事人关联表                              | risk_type          | 案件唯一 ID          | 核心字段（详情表）                                                                        | 事件日期            |
| --------------------------- | -------------------------------------- | ------------------ | ---------------- | ------------------------------------------------------------------------------- | --------------- |
| risk_lawsuit                | risk_lawsuit_party                     | lawsuit            | judgment_doc_id  | case_no/case_type/court_name/trial_procedure/judgment_date/publish_date/case_cause/doc_title | judgment_date   |
| risk_court_filed            | risk_court_filed_party                 | court_filed        | case_unique_id   | case_no/case_cause/trial_procedure/case_status/filing_date/closing_date/hearing_date/court_name | filing_date     |
| risk_court_notice           | risk_court_notice_party                | court_notice       | notice_id        | case_no/case_cause/court_name/hearing_date                                       | hearing_date    |
| risk_court_announcement     | risk_court_announcement_party          | court_announcement | notice_id        | notice_name/notice_type/case_no/court_name/notice_date/publish_date              | publish_date    |
| risk_judicial_sale          | risk_judicial_sale_party               | judicial_sale      | notice_id        | notice_name/asset_disposal_unit/notice_time/auction_start_date/auction_end_date/source_website/original_link | notice_time     |
| risk_bankruptcy             | risk_bankruptcy_party                  | bankruptcy         | case_no          | case_type/handling_court/public_date                                             | public_date     |

**当事人关联表通用字段**：`id` / 案件唯一 ID / `org_id` / `party_role`（原告/被告/申请人/被申请人等）/ `is_history` / `create_time` / `update_time`


---

## 6. 需上游排查的数据缺口汇总

### 6.1 需上游补充数据的（ODS 源表本身缺字段，ETL 无法凭空生成）

| #   | 缺失字段/问题         | 涉及 DWD 表       | 业务必要性         | 建议                                           |
| --- | --------------- | --------------- | ------------- | -------------------------------------------- |
| 1   | 招投标缺公告日期        | enterprise_bid  | **高**（列表排序必需） | 请上游确认 dwd_org_bid_info 能否补 announcement_date |
| 2   | 招投标缺中标金额        | enterprise_bid  | 中（可选展示）       | 如无金额数据，留空                                    |
| 3   | 招投标缺项目名称        | enterprise_bid  | 中             | 如有请提供                                        |
| 4   | 股权冻结表无日期字段      | risk_equity_freeze | 中（时间排序）       | 确认 dwd_org_company_justice 有无日期字段            |
| 5   | 税收违法无罚款金额       | risk_tax_punish | 低             | fine 字段留空                                    |

### 6.2 ETL 处理可解决的（数据存在，需格式转换/清洗/映射）

| #   | 问题                 | 涉及 DWD 表                  | ETL 处理方式                                    |
| --- | ------------------ | -------------------------- | -------------------------------------------- |
| 6   | 年报财务金额为 VARCHAR    | enterprise_finance_history | ETL 时 CAST 为 NUMERIC，清洗"万元"等文本和异常值           |
| 7   | 执行标的为 VARCHAR 文本   | risk_executed              | DWD 保持 VARCHAR 或 ETL 抽取数值部分                  |
| 8   | 股权数额为 VARCHAR 文本   | risk_equity_freeze         | 同上                                           |
| 9   | 专利表无 org_id        | enterprise_patent_history  | ETL 建机构名→org_id 映射（⚠️需确认 ODS 是否有企业基本信息表可关联） |

> **注**：6 类司法案件详情表不含 org_id 是设计预期行为，非数据缺口。org_id 在当事人关联表中，查询时 JOIN 即可。唯一风险是当事人名称无法映射到 org_id，属于数据质量问题。


---

## 7. 后续工作

1. **本文档定稿后** → DDL 已就绪，导入 dwd schema
2. **DDL 入库后** → 评估 ES 索引设计是否需要调整（字段名/来源对齐）
3. **ES 定稿后** → 继续 Python 代码开发（enterprise_profile.py 的 PG 查询逻辑改为查独立表）
4. **ETL 开发**（data-agent 职责）：ODS → DWD 的数据加载脚本

