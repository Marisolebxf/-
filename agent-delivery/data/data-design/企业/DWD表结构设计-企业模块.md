# 科技专题-企业模块 DWD 表结构设计

> 版本：v2.6 | 日期：2026-07-14 | 作者：[agent:data-agent]
> 范围：科技专题服务系统 - 企业检索 + 企业详情模块
> 数据库：PostgreSQL | Schema：dwd
> 约定：所有表统一 id BIGSERIAL 自增主键 + create_time + update_time
> 数据量级：企业主表约 2 亿行，司法/招投标等明细表亿级以上
>
> **变更记录**
>
> | 版本 | 日期 | 变更说明 |
> | ---- | ---- | ---- |
> | v2.0 | 2026-07-07 | 初版 DWD 表结构设计（41 张表） |
> | v2.1 | 2026-07-13 | 补充 ES 索引所需字段：enterprise_extra 补 12 字段、enterprise_score 补 2 字段、enterprise_finance_history 补 3 字段、新建 enterprise_history_name 表、enterprise_industry_chain 补 is_chain_leader 字段 |
> | v2.2 | 2026-07-13 | 新建 enterprise_industry_summary 产业维度统计汇总表（第 43 张），支撑企业整体概况 KPI/对比/趋势；引入 chain_code='ALL' 八大未来产业去重汇总语义 |
> | v2.3 | 2026-07-13 | 新建 enterprise_stat_summary（通用统计汇总表，第 44 张）+ enterprise_type_scale_stats（类型×规模×区域交叉统计表，第 45 张），支撑"重点企业介绍"模块的 KPI 卡片/产业统计/资质统计/类型×规模交叉统计 |
> | v2.4 | 2026-07-13 | 新建 enterprise_star 明星企业预定义表（第 46 张）；tag_dict 追加 key_enterprise/star_enterprise 标签；enterprise_stat_summary 追加 star_enterprise_node/star_enterprise_district 两种 stat_type |
> | v2.5 | 2026-07-13 | 新建 shenzhen_enterprise_summary 深圳企业统计汇总表（第 47 张），支撑"深圳企业介绍"模块的 KPI/产业分布/历年累计增长趋势；不走通用 enterprise_stat_summary，单独建表 |
> | v2.6 | 2026-07-14 | 新建 code_region 行政地区码表（第 48 张，完整导入非ETL）；tag_dict 追加上市/小巨人/链主龙头标签 |

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
| 企业详情-曾用名     | 企业历史名称变更记录                | enterprise_history_name     | dwd_company_history_name                  |


**不做 DWD 表的模块**：技术力/商业力/竞争力得分（算法产物归 ADS）、企业合作关系（依赖 NER 无数据源）、供应链关系（同上）、母子公司（可从 ODS 临时查询）。

---

## 3. DWD 表总览（48 张表）

### 3.1 企业基本信息（3 张）


| #   | 表名                      | 字段数 | 更新频率 | 说明                                   |
| --- | ----------------------- | --- | ---- | ------------------------------------ |
| 1   | enterprise_base         | 19  | 年更   | 检索列表页高频字段（名称/代码/行业/地区/成立/状态/上市标志/资本） |
| 2   | enterprise_extra        | 28  | 年更   | 详情页低频字段（英文名/实缴/经营范围/地址/经纬度/上市详情/联系方式/主营业务/曾用名相关）     |
| 3   | enterprise_history_name | 8   | 季更   | 企业曾用名（来源：dwd_company_history_name）    |


**拆分理由**：2亿行主表，列表页只查 base（19 字段窄表），详情页按需 JOIN extra。避免列表查询扫描含 TEXT 大字段（business_scope 等）的宽行。

### 3.2 企业画像（6 张）


| #   | 表名                          | 字段数 | 更新频率 | 说明                      |
| --- | --------------------------- | --- | ---- | ----------------------- |
| 3   | tag_dict                    | 10  | 极低频  | 标签字典（通用，资质/荣誉/规模/产业/特色） |
| 4   | enterprise_tag              | 7   | 季更   | 企业-标签关联（多对多）            |
| 5   | enterprise_finance_history  | 18  | 年追加  | 历年财务（画像页取最新年份，趋势图取全部） |
| 6   | enterprise_patent_history   | 12  | 年追加  | 历年专利统计（画像页取最新年份或SUM全部，趋势图取全部） |
| 7   | enterprise_patent_detail    | 28  | 日追加  | 专利明细（详情页知识产权Tab走PG查询，不走ES） |
| 8   | enterprise_executive        | 7   | 季更   | 高管信息（详情页主要团队Tab） |


### 3.3 企业明细（6 张）


| #   | 表名                           | 字段数 | 更新频率 | 说明                       |
| --- | ---------------------------- | --- | ---- | ------------------------ |
| 9   | enterprise_bid               | 16  | 日追加  | 招投标记录                    |
| 10  | enterprise_news              | 12  | 日追加  | 新闻资讯                     |
| 11  | enterprise_industry_chain    | 12  | 季更   | 产业链归属（含是否链主标志）                    |
| 12  | enterprise_financing         | 11  | 日追加  | 融资事件（详情页融资历程）            |
| 13  | enterprise_innovation_carrier | 13  | 季更   | 创新载体（详情页资质荣誉Tab）         |
| 14  | enterprise_invest            | 11  | 季更   | 对外投资（详情页供应链关系Tab）        |


### 3.4 企业评分（1 张，ADS 层）


| #   | 表名              | 字段数 | 更新频率 | 说明                                    |
| --- | ---------------- | --- | ---- | ------------------------------------- |
| 15  | enterprise_score | 12  | 按算法  | ADS 层评分（竞争力分/技术力/商业力/规模/链位/风险等级），算法产出后 ETL 写入 |

### 3.4b 区域统计汇总（3 张）

| #   | 表名                          | 字段数 | 更新频率 | 说明                                          |
| --- | ----------------------------- | ------ | -------- | --------------------------------------------- |
| 16  | enterprise_region_summary     | 12     | 日更     | 区域企业汇总（企业总数/新增/活跃/产值），支撑 KPI 卡片 + 区域热力 |
| 17  | enterprise_industry_distribution | 8   | 日更     | 区域产业分布（按产业链统计企业数），支撑产业分布饼图       |
| 18  | enterprise_growth_trend       | 8      | 日更     | 区域增长趋势（按月统计新增企业数），支撑增长趋势柱状图     |

### 3.4c 产业维度统计汇总（1 张）

| #   | 表名                          | 字段数 | 更新频率 | 说明                                          |
| --- | ----------------------------- | ------ | -------- | --------------------------------------------- |
| 19  | enterprise_industry_summary   | 11     | 日更     | 产业维度汇总（按 chain_code×stat_year 预聚合），支撑企业整体概况 KPI/对比/趋势；chain_code='ALL' 为八大未来产业去重汇总 |

### 3.4d 重点企业统计汇总（2 张）

| #   | 表名                          | 字段数 | 更新频率 | 说明                                          |
| --- | ----------------------------- | ------ | -------- | --------------------------------------------- |
| 20  | enterprise_stat_summary       | 9      | 日更     | 通用统计汇总（按 stat_type×dim_code×stat_year 预聚合），通过 stat_type 区分重点企业按产业/环节/行政区、资质类型、产业企业总数等口径 |
| 21  | enterprise_type_scale_stats   | 11     | 日更     | 类型×规模×区域交叉统计（按 company_type×enterprise_scale×region 预聚合），支撑重点企业介绍-类型×国/省/市规模 |


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


### 4.2 dwd.enterprise_extra（企业扩展信息，28 字段）

**原型图位置**：企业详情-基本信息卡（详情页才展示的低频字段）
**更新频率**：年更
**ODS 来源**：`dwd_company_base`、`dwd_org_stock_base`、`dwd_company_location_tags`、`dwd_org_reg_info`、`dwd_org_org_product_info`


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
| 13  | contact_phone        | varchar(50)   | 是   | 联系电话        | dwd_org_reg_info.phone                   |
| 14  | contact_email        | varchar(100)  | 是   | 联系邮箱        | dwd_org_reg_info.email                   |
| 15  | main_activities      | text          | 是   | 主营业务范围      | dwd_org_org_product_info.main_activities |
| 16  | main_prod            | text          | 是   | 主要产品        | dwd_org_org_product_info.main_prod       |
| 17  | description          | text          | 是   | 企业简介        | dwd_org_org_product_info.description     |
| 18  | stock_noun           | varchar(50)   | 是   | 股票简称        | dwd_org_stock_base.stock_noun            |
| 19  | listed_status        | varchar(20)   | 是   | 上市状态（已上市/退市） | dwd_org_stock_base.listed_status         |
| 20  | capital_currency_code | varchar(20)  | 是   | 注册资本币种代码    | dwd_org_reg_info.capital_currency_code   |
| 21  | registration_org     | varchar(100)  | 是   | 登记机关        | dwd_org_reg_info.registration_org        |
| 22  | postal_code          | varchar(20)   | 是   | 邮编          | dwd_org_reg_info.postal_code             |
| 23  | start_date           | varchar(50)   | 是   | 经营起始日期（ODS为VARCHAR，ETL清洗后转date） | dwd_org_reg_info.start_date              |
| 24  | end_date             | varchar(50)   | 是   | 经营截止日期（ODS为VARCHAR，ETL清洗后转date） | dwd_org_reg_info.end_date                |
| 25  | data_source          | varchar(100)  | 是   | 数据来源        | -                                        |
| 26  | create_time          | timestamp     | 否   | 记录创建时间      | 系统填充                                     |
| 27  | update_time          | timestamp     | 否   | 记录更新时间（ETL） | 系统填充                                     |
| 28  | _（含 id 共 28 个字段，#13-#24 为 v2.1 新增）_ | | | | |


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

### 4.5 dwd.enterprise_finance_history（企业财务历史，18 字段）

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
| 12 | main_business_revenue | numeric(20,2) | 是 | 主营业务收入（元） | dwd_org_annual_financial_info.main_business_revenue |
| 13 | total_profit | numeric(20,2) | 是 | 利润总额（元） | dwd_org_annual_financial_info.total_profit |
| 14 | total_fixed_assets | numeric(20,2) | 是 | 固定资产合计（元） | dwd_org_annual_financial_info.fixed_assets |
| 15 | data_source | varchar(50) | 是 | 数据来源（annual/stock） | - |
| 16 | create_time | timestamp | 否 | 记录创建时间 | 系统填充 |
| 17 | update_time | timestamp | 否 | 记录更新时间（ETL） | 系统填充 |

> 注：#12-#14 为 v2.1 新增字段，金额单位为元（与 ODS 源保持一致），区别于 #4-#9 的万元口径。

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


### 4.11 dwd.enterprise_industry_chain（企业产业链归属，12 字段）

**原型图位置**：企业详情-产业链位置
**更新频率**：季更
**ODS 来源**：`dwd_org_industry_chain_dtl`
**唯一约束**：(org_id, chain_code, node_id)

| # | 字段名 | 类型 | 可空 | 备注 | ODS 来源 |
|---|--------|------|------|------|----------|
| 1 | id | bigserial | 否 | 自增主键 | - |
| 2 | org_id | varchar(64) | 否 | 机构id | dwd_org_industry_chain_dtl.org_id |
| 3 | enterprise_code | varchar(64) | 是 | 统一社会信用代码 | dwd_org_industry_chain_dtl.credit_code |
| 4 | chain_code | varchar(64) | 否 | 产业链编码 | dwd_org_industry_chain_dtl.chain_code |
| 5 | chain_name | varchar(255) | 否 | 产业链名称 | dwd_org_industry_chain_dtl.chain_name |
| 6 | node_id | varchar(64) | 是 | 产业链环节id | dwd_org_industry_chain_dtl.node_id |
| 7 | node_name | varchar(255) | 是 | 环节名称 | dwd_org_industry_chain_dtl.node_name |
| 8 | node_stage | varchar(20) | 是 | 环节（上游/中游/下游） | dwd_org_industry_chain_dtl.node_stage |
| 9 | chain_score | numeric(10,2) | 是 | 产业链评分 | dwd_org_industry_chain_dtl.chain_score |
| 10 | is_chain_leader | boolean | 否 | 是否产业链链主（待业务确认判定规则，默认FALSE） | 待业务确认 |
| 11 | create_time | timestamp | 否 | 记录创建时间 | 系统填充 |
| 12 | update_time | timestamp | 否 | 记录更新时间（ETL） | 系统填充 |

**设计说明**：`is_chain_leader` 为 v2.1 新增字段，用于标识企业是否为某产业链的链主企业。判定规则待业务确认（可能基于企业规模、产业链位置评分、市场份额等维度综合判定），表结构先建好，默认值为 FALSE，待业务确认后由 ETL 或算法服务回填。

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

### 4.15 dwd.enterprise_score（企业评分，12 字段，ADS 层）

**原型图位置**：搜索结果卡片（竞争力分排序）、高级筛选（规模/风险等级）、卡片展示（链位文本）、企业画像页技术力/商业力分解
**更新频率**：按算法产出周期（暂定季更，算法就绪后 ETL 写入）
**数据来源**：算法侧（ai-service）计算产出，ETL 搬入此表
**唯一约束**：(org_id)

| # | 字段名 | 类型 | 可空 | 备注 |
|---|--------|------|------|------|
| 1 | id | bigserial | 否 | 自增主键 |
| 2 | org_id | varchar(64) | 否 | 机构id |
| 3 | competitiveness_score | numeric(6,2) | 是 | 综合竞争力评分（0-100） |
| 4 | tech_score | numeric(6,2) | 是 | 技术力评分（算法产出，来源：算法服务，暂无数据） |
| 5 | business_score | numeric(6,2) | 是 | 商业力评分（算法产出，来源：算法服务，暂无数据） |
| 6 | enterprise_scale | varchar(20) | 是 | 企业规模（大型/中型/小型/微型/规上） |
| 7 | chain_position_text | varchar(255) | 是 | 产业链位置文本（如"设计层 · 上游EDA"） |
| 8 | risk_level | varchar(20) | 是 | 风险等级（无风险/低风险/中风险/高风险） |
| 9 | score_version | varchar(20) | 是 | 评分模型版本 |
| 10 | score_date | date | 是 | 评分计算日期 |
| 11 | create_time | timestamp | 否 | 记录创建时间 |
| 12 | update_time | timestamp | 否 | 记录更新时间（ETL） |

**设计说明**：此表属 ADS 层，算法侧尚未实现。表结构先建好，算法就绪后 ETL 直接写入。`tech_score` / `business_score` 为 v2.1 新增，由算法服务产出，当前无数据，表结构先建好等算法侧写入。ES 同步时从此表读取 `competitiveness_score` / `enterprise_scale` / `chain_position_text` / `risk_level` 写入 ES 顶层字段。算法就绪前这些字段为空，不影响 ES 索引正常使用。

### 4.16 dwd.enterprise_history_name（企业曾用名，8 字段）

**原型图位置**：企业详情-基本信息卡（曾用名展示）+ 企业检索（按曾用名检索）
**更新频率**：季更
**ODS 来源**：`dwd_company_history_name`
**唯一约束**：无（同一企业可有多个曾用名，同一曾用名可跨企业）

| # | 字段名 | 类型 | 可空 | 备注 | ODS 来源 |
|---|--------|------|------|------|----------|
| 1 | id | bigserial | 否 | 自增主键 | - |
| 2 | org_id | varchar(64) | 否 | 企业唯一标识（32位MD5） | dwd_company_history_name.org_id |
| 3 | history_name | varchar(255) | 否 | 曾用名 | dwd_company_history_name.history_name |
| 4 | start_date | varchar(50) | 是 | 曾用名起始日期（ODS为VARCHAR） | dwd_company_history_name.start_date |
| 5 | end_date | varchar(50) | 是 | 曾用名结束日期（ODS为VARCHAR） | dwd_company_history_name.end_date |
| 6 | source | varchar(50) | 是 | 数据来源 | dwd_company_history_name.source |
| 7 | create_time | timestamp | 否 | 记录创建时间 | 系统填充 |
| 8 | update_time | timestamp | 否 | 记录更新时间（ETL） | 系统填充 |

**设计说明**：此表为 v2.1 新增。ODS 源表 `dwd_company_history_name` 记录企业名称变更历史，一家企业可能多次更名，因此为一对多关系。`start_date` / `end_date` 在 ODS 中为 VARCHAR（日期格式可能不统一），DWD 保持 VARCHAR，ETL 清洗后再转 date。索引 `(org_id)` 支持详情页按企业查曾用名列表，索引 `(history_name)` 支持按曾用名检索企业。同时灌入 ES `history_names` 字段支持曾用名检索。

---

## 5. 区域统计汇总表（3 张，支撑门户首页"企业发展概况"）

### 5.0 设计思路

原型图「1.1 企业发展概况」页面（`/development/overview`）需要展示：

1. **KPI 卡片（4 张）**：企业总数、新增企业、活跃企业、产值规模
2. **图表：产业分布**（饼图，按产业链统计深圳企业数占比）
3. **图表：增长趋势**（近 12 月柱状图，按月统计新增企业数）
4. **图表：区域热力**（区县网格，按深圳各区统计企业数）

2 亿企业下直接对 `enterprise_base` 做 count / group by 性能不可接受。采用**离线预计算方案**：ETL 每日凌晨从 `enterprise_base` + `enterprise_finance_history` + `enterprise_industry_chain` 聚合写入汇总表，接口只读汇总表。

**表数选择：3 张表**

| 表名 | 粒度 | 用途 | 预估行数 |
|------|------|------|---------|
| enterprise_region_summary | region_id × stat_date | KPI 卡片 + 区域热力 | ~几千（城市+区县×日期） |
| enterprise_industry_distribution | region_id × chain_code × stat_date | 产业分布饼图 | ~几千 |
| enterprise_growth_trend | region_id × stat_year × stat_month × stat_date | 增长趋势柱状图 | ~几万 |

**为什么不合并为 1 张表**：产业分布是一对多（N 个产业链）、增长趋势是一对多（12 个月），维度不同，合并会导致大量空值或 dim_type 笛卡尔积。

**为什么区域热力不单独建表**：区域热力本质是"按区县统计企业数"，和 KPI 卡片的 `enterprise_total` 是同一个指标，只是粒度从 city 下钻到 district。`enterprise_region_summary` 同时存 city 和 district 级别的行，区域热力查询时按 `region_type=district` + `parent_region_id=深圳` 过滤即可。

---

### 5.1 dwd.enterprise_region_summary（区域企业汇总统计，12 字段）

**原型图位置**：1.1 企业发展概况 → KPI 卡片（4 张）+ 区域热力图
**更新频率**：日更（每日凌晨 ETL 跑批）
**数据来源**：`enterprise_base` + `enterprise_finance_history`
**唯一约束**：(region_id, region_type, stat_date)

| # | 字段名 | 类型 | 可空 | 备注 |
|---|--------|------|------|------|
| 1 | id | bigserial | 否 | 自增主键 |
| 2 | region_id | varchar(20) | 否 | 区域编码（如深圳市 440300） |
| 3 | region_name | varchar(100) | 否 | 区域名称（如深圳市/南山区） |
| 4 | region_type | varchar(20) | 否 | 区域级别（city/district） |
| 5 | parent_region_id | varchar(20) | 是 | 父级区域编码（区县填所属城市编码） |
| 6 | stat_date | date | 否 | 统计日期（ETL 跑批日期） |
| 7 | enterprise_total | integer | 否 | 企业总数（该区域在营企业数） |
| 8 | new_enterprise_count | integer | 否 | 新增企业数（最近一周成立） |
| 9 | active_enterprise_count | integer | 否 | 活跃企业数（business_status=1） |
| 10 | total_revenue | numeric(18,2) | 是 | 产值规模（最新年度营收之和，万元） |
| 11 | create_time | timestamp | 否 | 记录创建时间 |
| 12 | update_time | timestamp | 否 | 记录更新时间（ETL） |

**ETL 统计逻辑**：

```sql
-- KPI：企业总数（city 级别）
INSERT INTO dwd.enterprise_region_summary (region_id, region_name, region_type, parent_region_id, stat_date, enterprise_total, new_enterprise_count, active_enterprise_count, total_revenue)
SELECT
    city AS region_id,
    city AS region_name,
    'city' AS region_type,
    NULL AS parent_region_id,
    CURRENT_DATE AS stat_date,
    COUNT(*) AS enterprise_total,
    COUNT(*) FILTER (WHERE registration_date >= CURRENT_DATE - INTERVAL '7 days') AS new_enterprise_count,
    COUNT(*) FILTER (WHERE business_status = '1') AS active_enterprise_count,
    NULL AS total_revenue  -- 下面单独更新
FROM dwd.enterprise_base
WHERE city IS NOT NULL
GROUP BY city;

-- KPI：产值规模（从 enterprise_finance_history 取最新年份营收求和）
UPDATE dwd.enterprise_region_summary s
SET total_revenue = sub.total_revenue
FROM (
    SELECT b.city AS region_id, SUM(f.revenue) AS total_revenue
    FROM dwd.enterprise_finance_history f
    JOIN dwd.enterprise_base b ON b.org_id = f.org_id
    WHERE f.data_year = (SELECT MAX(data_year) FROM dwd.enterprise_finance_history)
      AND b.city IS NOT NULL
    GROUP BY b.city
) sub
WHERE s.region_id = sub.region_id AND s.stat_date = CURRENT_DATE AND s.region_type = 'city';

-- 区域热力（district 级别，只统计 enterprise_total）
INSERT INTO dwd.enterprise_region_summary (region_id, region_name, region_type, parent_region_id, stat_date, enterprise_total)
SELECT
    district AS region_id,
    district AS region_name,
    'district' AS region_type,
    city AS parent_region_id,
    CURRENT_DATE AS stat_date,
    COUNT(*) AS enterprise_total
FROM dwd.enterprise_base
WHERE district IS NOT NULL AND city IS NOT NULL
GROUP BY district, city;
```

---

### 5.2 dwd.enterprise_industry_distribution（区域产业分布统计，8 字段）

**原型图位置**：1.1 企业发展概况 → 产业分布饼图
**更新频率**：日更
**数据来源**：`enterprise_base` JOIN `enterprise_industry_chain`
**唯一约束**：(region_id, chain_code, stat_date)

| # | 字段名 | 类型 | 可空 | 备注 |
|---|--------|------|------|------|
| 1 | id | bigserial | 否 | 自增主键 |
| 2 | region_id | varchar(20) | 否 | 区域编码 |
| 3 | chain_code | varchar(64) | 否 | 产业链编码 |
| 4 | chain_name | varchar(255) | 否 | 产业链名称 |
| 5 | enterprise_count | integer | 否 | 该产业链下企业数 |
| 6 | stat_date | date | 否 | 统计日期 |
| 7 | create_time | timestamp | 否 | 记录创建时间 |
| 8 | update_time | timestamp | 否 | 记录更新时间（ETL） |

**ETL 统计逻辑**：

```sql
INSERT INTO dwd.enterprise_industry_distribution (region_id, chain_code, chain_name, enterprise_count, stat_date)
SELECT
    b.city AS region_id,
    ic.chain_code,
    ic.chain_name,
    COUNT(DISTINCT b.org_id) AS enterprise_count,
    CURRENT_DATE AS stat_date
FROM dwd.enterprise_base b
JOIN dwd.enterprise_industry_chain ic ON ic.org_id = b.org_id
WHERE b.city IS NOT NULL
GROUP BY b.city, ic.chain_code, ic.chain_name;
```

---

### 5.3 dwd.enterprise_growth_trend（区域企业增长趋势，8 字段）

**原型图位置**：1.1 企业发展概况 → 增长趋势柱状图（近 12 月）
**更新频率**：日更
**数据来源**：`enterprise_base`（按 `registration_date` 聚合）
**唯一约束**：(region_id, stat_year, stat_month, stat_date)

| # | 字段名 | 类型 | 可空 | 备注 |
|---|--------|------|------|------|
| 1 | id | bigserial | 否 | 自增主键 |
| 2 | region_id | varchar(20) | 否 | 区域编码 |
| 3 | stat_year | integer | 否 | 统计年份 |
| 4 | stat_month | integer | 否 | 统计月份（1-12） |
| 5 | new_enterprise_count | integer | 否 | 当月新增企业数 |
| 6 | stat_date | date | 否 | 统计日期 |
| 7 | create_time | timestamp | 否 | 记录创建时间 |
| 8 | update_time | timestamp | 否 | 记录更新时间（ETL） |

**ETL 统计逻辑**：

```sql
INSERT INTO dwd.enterprise_growth_trend (region_id, stat_year, stat_month, new_enterprise_count, stat_date)
SELECT
    city AS region_id,
    EXTRACT(YEAR FROM registration_date)::INTEGER AS stat_year,
    EXTRACT(MONTH FROM registration_date)::INTEGER AS stat_month,
    COUNT(*) AS new_enterprise_count,
    CURRENT_DATE AS stat_date
FROM dwd.enterprise_base
WHERE city IS NOT NULL AND registration_date IS NOT NULL
  AND registration_date >= CURRENT_DATE - INTERVAL '13 months'
GROUP BY city, stat_year, stat_month;
```

---

### 5.4 dwd.enterprise_industry_summary（产业维度统计汇总，11 字段）

**原型图位置**：企业整体概况 → KPI 卡片（八大未来产业企业总数/科研人数总数/产业覆盖）+ 八大未来产业企业数量对比柱状图 + 选中产业历年企业数量趋势折线图
**更新频率**：日更（每日凌晨 ETL 跑批）
**数据来源**：`enterprise_base` JOIN `enterprise_industry_chain` + `enterprise_finance_history`（科研人数）+ `enterprise_tag`（高企数）+ `enterprise_patent_history`（专利数）
**唯一约束**：(chain_code, stat_year, stat_date)

| # | 字段名 | 类型 | 可空 | 备注 |
|---|--------|------|------|------|
| 1 | id | bigserial | 否 | 自增主键 |
| 2 | chain_code | varchar(64) | 否 | 产业链编码；'ALL' 表示八大未来产业去重汇总行，其余为具体产业编码（如 IC001/BIO01） |
| 3 | chain_name | varchar(255) | 否 | 产业链名称；'ALL' 时填'八大未来产业'，其余为具体产业名 |
| 4 | stat_year | integer | 否 | 统计年份（0=全部年份累计汇总，2024/2025/2026=当年新增数） |
| 5 | enterprise_count | integer | 否 | 该产业企业数；chain_code='ALL' 时为八大未来产业 DISTINCT org_id 去重总数 |
| 6 | research_staff_total | integer | 否 | 该产业科研人数总数；chain_code='ALL' 时为去重企业科研人数之和 |
| 7 | patent_total | integer | 否 | 该产业专利总量 |
| 8 | high_tech_count | integer | 否 | 该产业高新技术企业数 |
| 9 | stat_date | date | 否 | 统计日期（ETL 跑批日期） |
| 10 | create_time | timestamp | 否 | 记录创建时间 |
| 11 | update_time | timestamp | 否 | 记录更新时间（ETL） |

**⚠️ chain_code='ALL' 去重汇总语义（核心设计点）**

原型图"八大未来产业企业总数"是一个**去重总数**——一家企业可能同时属于集成电路和人工智能，按产业分别统计后直接相加会重复计数。因此 ETL 需要产出一行 `chain_code='ALL'` 的汇总行：

- **chain_code='ALL' 的行**：ETL 先对八大未来产业覆盖的所有企业做 `DISTINCT org_id` 去重，再 `COUNT`。科研人数同理对去重后的企业集合做 `SUM(employees_number)`。
- **chain_code='IC001' 等具体产业的行**：直接 `COUNT(DISTINCT org_id) WHERE chain_code='IC001'`，不做跨产业去重。因此各产业企业数之和 ≥ 'ALL' 行的企业数。
- **stat_year=0**：全部年份的累计汇总（KPI 卡片 + 对比柱状图用）。
- **stat_year>0**：当年新增的企业数（历年趋势折线图用）。

**ETL 统计逻辑**：

```sql
-- 1. 各产业汇总行（chain_code ≠ 'ALL'，stat_year=0 为全部年份累计）
INSERT INTO dwd.enterprise_industry_summary (chain_code, chain_name, stat_year, enterprise_count, research_staff_total, patent_total, high_tech_count, stat_date)
SELECT
    ic.chain_code,
    ic.chain_name,
    0 AS stat_year,
    COUNT(DISTINCT b.org_id) AS enterprise_count,
    COALESCE(SUM(f.employees_number), 0) AS research_staff_total,
    COALESCE(SUM(p.patent_apply_count), 0) AS patent_total,
    COUNT(DISTINCT CASE WHEN t.tag_code='high_tech' THEN b.org_id END) AS high_tech_count,
    CURRENT_DATE AS stat_date
FROM dwd.enterprise_industry_chain ic
JOIN dwd.enterprise_base b ON b.org_id = ic.org_id
LEFT JOIN dwd.enterprise_finance_history f ON f.org_id = b.org_id
    AND f.data_year = (SELECT MAX(data_year) FROM dwd.enterprise_finance_history)
LEFT JOIN dwd.enterprise_patent_history p ON p.org_id = b.org_id
LEFT JOIN dwd.enterprise_tag t ON t.org_id = b.org_id AND t.tag_code='high_tech'
WHERE ic.chain_code IN ('IC001','BIO01','AI001','NEV01','COM01','SOFT01','MAT01','ROB01')
GROUP BY ic.chain_code, ic.chain_name;

-- 2. 八大未来产业去重汇总行（chain_code='ALL'，stat_year=0）
INSERT INTO dwd.enterprise_industry_summary (chain_code, chain_name, stat_year, enterprise_count, research_staff_total, patent_total, high_tech_count, stat_date)
SELECT
    'ALL' AS chain_code,
    '八大未来产业' AS chain_name,
    0 AS stat_year,
    COUNT(DISTINCT b.org_id) AS enterprise_count,                       -- 去重总数
    COALESCE(SUM(distinct_emp.employees_number), 0) AS research_staff_total,  -- 去重企业科研人数之和
    COALESCE(SUM(distinct_pat.patent_apply_count), 0) AS patent_total,
    COUNT(DISTINCT CASE WHEN t.tag_code='high_tech' THEN b.org_id END) AS high_tech_count,
    CURRENT_DATE AS stat_date
FROM dwd.enterprise_industry_chain ic
JOIN dwd.enterprise_base b ON b.org_id = ic.org_id
LEFT JOIN LATERAL (
    SELECT employees_number FROM dwd.enterprise_finance_history f
    WHERE f.org_id = b.org_id
      AND f.data_year = (SELECT MAX(data_year) FROM dwd.enterprise_finance_history)
    LIMIT 1
) distinct_emp ON TRUE
LEFT JOIN LATERAL (
    SELECT COALESCE(SUM(patent_apply_count),0) AS patent_apply_count
    FROM dwd.enterprise_patent_history p WHERE p.org_id = b.org_id
) distinct_pat ON TRUE
LEFT JOIN dwd.enterprise_tag t ON t.org_id = b.org_id AND t.tag_code='high_tech'
WHERE ic.chain_code IN ('IC001','BIO01','AI001','NEV01','COM01','SOFT01','MAT01','ROB01');

-- 3. 历年趋势行（stat_year > 0，按 chain_code × 年份）
INSERT INTO dwd.enterprise_industry_summary (chain_code, chain_name, stat_year, enterprise_count, research_staff_total, patent_total, high_tech_count, stat_date)
SELECT
    ic.chain_code,
    ic.chain_name,
    EXTRACT(YEAR FROM b.registration_date)::INTEGER AS stat_year,
    COUNT(DISTINCT b.org_id) AS enterprise_count,
    0 AS research_staff_total,  -- 趋势行只关心企业数，其余指标留 0
    0 AS patent_total,
    0 AS high_tech_count,
    CURRENT_DATE AS stat_date
FROM dwd.enterprise_industry_chain ic
JOIN dwd.enterprise_base b ON b.org_id = ic.org_id
WHERE ic.chain_code IN ('IC001','BIO01','AI001','NEV01','COM01','SOFT01','MAT01','ROB01')
  AND b.registration_date IS NOT NULL
GROUP BY ic.chain_code, ic.chain_name, EXTRACT(YEAR FROM b.registration_date);
```

**接口查询示例**：

```sql
-- KPI 卡片（去重总数）
SELECT enterprise_count, research_staff_total, patent_total, high_tech_count
FROM dwd.enterprise_industry_summary
WHERE chain_code='ALL' AND stat_year=0
  AND stat_date=(SELECT MAX(stat_date) FROM dwd.enterprise_industry_summary);

-- 对比柱状图（各产业，不去重）
SELECT chain_code, chain_name, enterprise_count
FROM dwd.enterprise_industry_summary
WHERE chain_code!='ALL' AND stat_year=0
  AND stat_date=(SELECT MAX(stat_date) FROM dwd.enterprise_industry_summary)
ORDER BY enterprise_count DESC;

-- 历年趋势（选中产业）
SELECT stat_year, enterprise_count
FROM dwd.enterprise_industry_summary
WHERE chain_code=%s AND stat_year>0
  AND stat_date=(SELECT MAX(stat_date) FROM dwd.enterprise_industry_summary WHERE chain_code=%s)
ORDER BY stat_year ASC;
```

**与现有 3 张统计表的关系**：

| 表 | 维度 | 用途 | 与 enterprise_industry_summary 的关系 |
|---|---|---|---|
| enterprise_region_summary | region_id × stat_date | 区域 KPI + 热力 | 维度不同（区域 vs 产业），互不重叠 |
| enterprise_industry_distribution | region_id × chain_code × stat_date | 区域内产业分布饼图 | 本表多了 region_id 维度，但只有 enterprise_count；industry_summary 无 region 维度但有多个指标 + 'ALL' 汇总行 |
| enterprise_growth_trend | region_id × year × month × stat_date | 区域增长趋势 | 维度不同（区域×月 vs 产业×年），互不重叠 |
| enterprise_industry_summary | chain_code × stat_year × stat_date | 产业维度 KPI/对比/趋势 | 新增，专门支撑"企业整体概况"页面的产业维度统计 |

**设计说明**：
- 不复用 `enterprise_industry_distribution`：该表按 region×chain 维度，只有 enterprise_count，无科研人数/专利/高企等指标，且无 'ALL' 去重汇总行。新建独立表避免改已有表的语义。
- `research_staff_total` 科研人数来源暂定为 `enterprise_finance_history.employees_number`，口径待甲方确认（🟡 待确认项）。

---

## 6. 司法风险模块设计（18 张明细 + 字典 + 统计）

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

## 7. 需上游排查的数据缺口汇总

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
| 10  | 经营起止日期为 VARCHAR    | enterprise_extra           | v2.1 新增 start_date / end_date，ODS 为 VARCHAR，DWD 保持 VARCHAR，ETL 清洗后转 date |
| 11  | 曾用名起止日期为 VARCHAR   | enterprise_history_name    | v2.1 新增表，start_date / end_date ODS 为 VARCHAR，DWD 保持 VARCHAR，ETL 清洗后转 date |

> **注**：6 类司法案件详情表不含 org_id 是设计预期行为，非数据缺口。org_id 在当事人关联表中，查询时 JOIN 即可。唯一风险是当事人名称无法映射到 org_id，属于数据质量问题。

### 6.3 v2.1 新增待业务确认项（🟡 需甲方拍板）

| # | 待确认项 | 涉及 DWD 表 | 说明 | 临时默认值 |
| --- | --- | --- | --- | --- |
| 12 | 产业链链主判定规则 | enterprise_industry_chain | v2.1 新增 `is_chain_leader` 字段，需业务确认判定规则（可能基于企业规模/产业链位置评分/市场份额等维度综合判定）。UI 上暂不加 ⚠️ 角标（字段默认 FALSE 不展示） | FALSE |
| 13 | 技术力/商业力评分口径 | enterprise_score | v2.1 新增 `tech_score` / `business_score` 字段，由算法服务产出，当前无数据。算法就绪后由算法侧定义评分口径 | 空 |


---

## 7b. 重点企业统计汇总表设计（2 张）

> v2.3 新增，支撑"科技专题-重点企业介绍"模块。两张表均为日更 ETL 预聚合表，Python 服务（gkx-search-service）通过 `/api/gkx-search/key-enterprise/*` 接口查询。

### 7b.1 dwd.enterprise_stat_summary（通用统计汇总表，9 字段）

**原型图位置**：重点企业介绍 - KPI 卡片 / 产业统计 / 资质统计
**更新频率**：日更
**ODS 来源**：`enterprise_base` + `enterprise_tag` + `enterprise_industry_chain`（ETL 聚合）

通过 `stat_type` 区分统计口径，一张表支撑重点企业介绍的多个统计场景，避免为每个统计场景各建一张表。

| #   | 字段名       | 类型           | 可空 | 备注                                                                  |
| --- | ------------ | -------------- | ---- | --------------------------------------------------------------------- |
| 1   | id           | bigserial      | 否   | 自增主键                                                               |
| 2   | stat_type    | varchar(50)    | 否   | 统计类型编码（见下方枚举）                                              |
| 3   | dim_code     | varchar(100)   | 否   | 维度编码（语义随 stat_type 变化）                                       |
| 4   | dim_name     | varchar(255)   | 否   | 维度名称（人类可读）                                                     |
| 5   | stat_year    | integer        | 否   | 统计年份（0=全部年份累计，>0=当年）                                     |
| 6   | stat_value   | integer        | 否   | 统计值（企业数）                                                        |
| 7   | stat_date    | date           | 否   | 统计日期（ETL 跑批日期，取最新日期）                                     |
| 8   | create_time  | timestamp      | 否   | 记录创建时间                                                           |
| 9   | update_time  | timestamp      | 否   | 记录更新时间（ETL）                                                    |

**唯一约束**：(stat_type, dim_code, stat_year, stat_date)

**stat_type 枚举值说明**：

| stat_type | 含义 | dim_code 语义 | dim_name 语义 | 支撑接口 |
| --- | --- | --- | --- | --- |
| `key_enterprise_chain` | 重点企业按产业统计 | chain_code（如 IC9901） | chain_name（如 低空经济） | chain-subject-stats |
| `key_enterprise_node` | 重点企业按产业链环节统计 | chain_code:node_id（如 IC9901:NODE_FLY_CTRL） | chain_name:node_name（如 低空经济:飞控系统） | KPI 卡片-覆盖环节数 |
| `key_enterprise_district` | 重点企业按行政区统计 | province_code:city_code（如 440000:440300） | province:city（如 广东省:深圳市） | KPI 卡片-覆盖行政区数 |
| `qualification_count` | 资质类型企业数 | tag_code（如 high_tech） | tag_name（如 高新技术企业） | qualification-summary |
| `industry_enterprise_count` | 产业企业总数（含非重点） | chain_code | chain_name | 产业统计对比 |

**ETL 逻辑**：

```sql
-- key_enterprise_chain：重点企业按产业统计（tags_flat 含 key_enterprise 的企业，按产业分组）
INSERT INTO dwd.enterprise_stat_summary (stat_type, dim_code, dim_name, stat_year, stat_value, stat_date)
SELECT 'key_enterprise_chain', ic.chain_code, ic.chain_name, 0,
       COUNT(DISTINCT b.org_id), CURRENT_DATE
FROM dwd.enterprise_base b
JOIN dwd.enterprise_industry_chain ic ON ic.org_id = b.org_id
JOIN dwd.enterprise_tag t ON t.org_id = b.org_id AND t.tag_code = 'key_enterprise'
GROUP BY ic.chain_code, ic.chain_name;

-- key_enterprise_node：重点企业按产业链环节统计
INSERT INTO dwd.enterprise_stat_summary (stat_type, dim_code, dim_name, stat_year, stat_value, stat_date)
SELECT 'key_enterprise_node',
       ic.chain_code || ':' || ic.node_id,
       ic.chain_name || ':' || COALESCE(ic.node_name, ''),
       0, COUNT(DISTINCT b.org_id), CURRENT_DATE
FROM dwd.enterprise_base b
JOIN dwd.enterprise_industry_chain ic ON ic.org_id = b.org_id
JOIN dwd.enterprise_tag t ON t.org_id = b.org_id AND t.tag_code = 'key_enterprise'
GROUP BY ic.chain_code, ic.node_id, ic.chain_name, ic.node_name;

-- key_enterprise_district：重点企业按行政区统计
INSERT INTO dwd.enterprise_stat_summary (stat_type, dim_code, dim_name, stat_year, stat_value, stat_date)
SELECT 'key_enterprise_district',
       COALESCE(b.province_code,'') || ':' || COALESCE(b.city_code,''),
       COALESCE(b.province,'') || ':' || COALESCE(b.city,''),
       0, COUNT(DISTINCT b.org_id), CURRENT_DATE
FROM dwd.enterprise_base b
JOIN dwd.enterprise_tag t ON t.org_id = b.org_id AND t.tag_code = 'key_enterprise'
GROUP BY b.province_code, b.city_code, b.province, b.city;

-- qualification_count：资质类型企业数（按 tag_code 统计）
INSERT INTO dwd.enterprise_stat_summary (stat_type, dim_code, dim_name, stat_year, stat_value, stat_date)
SELECT 'qualification_count', t.tag_code, d.tag_name, 0,
       COUNT(DISTINCT t.org_id), CURRENT_DATE
FROM dwd.enterprise_tag t
JOIN dwd.tag_dict d ON d.tag_code = t.tag_code
WHERE t.tag_code IN ('high_tech','little_giant','gazelle','unicorn')
GROUP BY t.tag_code, d.tag_name;

-- industry_enterprise_count：产业企业总数（含非重点）
INSERT INTO dwd.enterprise_stat_summary (stat_type, dim_code, dim_name, stat_year, stat_value, stat_date)
SELECT 'industry_enterprise_count', ic.chain_code, ic.chain_name, 0,
       COUNT(DISTINCT b.org_id), CURRENT_DATE
FROM dwd.enterprise_base b
JOIN dwd.enterprise_industry_chain ic ON ic.org_id = b.org_id
GROUP BY ic.chain_code, ic.chain_name;
```

**接口查询示例**：

```sql
-- KPI 卡片：覆盖产业链环节数（key_enterprise_node 的 dim_code 去重数）
SELECT COUNT(DISTINCT dim_code) FROM dwd.enterprise_stat_summary
WHERE stat_type='key_enterprise_node' AND stat_year=0
  AND stat_date=(SELECT MAX(stat_date) FROM dwd.enterprise_stat_summary WHERE stat_type='key_enterprise_node');

-- KPI 卡片：覆盖行政区数（key_enterprise_district 的行数）
SELECT COUNT(*) FROM dwd.enterprise_stat_summary
WHERE stat_type='key_enterprise_district' AND stat_year=0
  AND stat_date=(SELECT MAX(stat_date) FROM dwd.enterprise_stat_summary WHERE stat_type='key_enterprise_district');

-- 产业统计（重点企业按产业）
SELECT dim_code AS chain_code, dim_name AS chain_name, stat_value AS key_enterprise_count
FROM dwd.enterprise_stat_summary
WHERE stat_type='key_enterprise_chain' AND stat_year=0
  AND stat_date=(SELECT MAX(stat_date) FROM dwd.enterprise_stat_summary WHERE stat_type='key_enterprise_chain')
ORDER BY stat_value DESC;

-- 资质统计
SELECT dim_code AS tag_code, dim_name AS tag_name, stat_value AS enterprise_count
FROM dwd.enterprise_stat_summary
WHERE stat_type='qualification_count' AND stat_year=0
  AND stat_date=(SELECT MAX(stat_date) FROM dwd.enterprise_stat_summary WHERE stat_type='qualification_count')
ORDER BY stat_value DESC;
```

### 7b.2 dwd.enterprise_type_scale_stats（类型×规模×区域 交叉统计表，11 字段）

**原型图位置**：重点企业介绍 - 类型×规模交叉统计（按国/省/市维度切换）
**更新频率**：日更
**ODS 来源**：`enterprise_base`（ETL 聚合）

按 `company_type × enterprise_scale × region` 三维度预聚合，支撑"企业类型×规模"交叉统计图表，可按国家级/省级/市级切换区域维度。

| #   | 字段名           | 类型           | 可空 | 备注                                                                  |
| --- | ---------------- | -------------- | ---- | --------------------------------------------------------------------- |
| 1   | id               | bigserial      | 否   | 自增主键                                                               |
| 2   | company_type     | varchar(100)   | 否   | 企业类型（有限责任公司/股份有限公司/外商投资/国有企业/民营企业）            |
| 3   | enterprise_scale | varchar(20)    | 否   | 企业规模（大型/中型/小型/微型/规上）                                     |
| 4   | region_level     | varchar(20)    | 否   | 区域级别（national/province/city）                                      |
| 5   | region_code      | varchar(20)    | 否   | 区域编码（national=CN / 省份编码 / 城市编码）                            |
| 6   | region_name      | varchar(100)   | 否   | 区域名称（全国 / 广东省 / 深圳市）                                       |
| 7   | enterprise_count | integer        | 否   | 该类型×规模×区域下的企业数                                               |
| 8   | stat_date        | date           | 否   | 统计日期（ETL 跑批日期，取最新日期）                                     |
| 9   | create_time      | timestamp      | 否   | 记录创建时间                                                           |
| 10  | update_time      | timestamp      | 否   | 记录更新时间（ETL）                                                    |

**唯一约束**：(company_type, enterprise_scale, region_level, region_code, stat_date)

**ETL 逻辑**：

```sql
-- national：全国汇总
INSERT INTO dwd.enterprise_type_scale_stats
(company_type, enterprise_scale, region_level, region_code, region_name, enterprise_count, stat_date)
SELECT b.enterprise_type, b.org_size, 'national', 'CN', '全国',
       COUNT(*), CURRENT_DATE
FROM dwd.enterprise_base b
WHERE b.enterprise_type IS NOT NULL AND b.org_size IS NOT NULL
GROUP BY b.enterprise_type, b.org_size;

-- province：按省汇总
INSERT INTO dwd.enterprise_type_scale_stats
(company_type, enterprise_scale, region_level, region_code, region_name, enterprise_count, stat_date)
SELECT b.enterprise_type, b.org_size, 'province', b.province_code, b.province,
       COUNT(*), CURRENT_DATE
FROM dwd.enterprise_base b
WHERE b.enterprise_type IS NOT NULL AND b.org_size IS NOT NULL AND b.province_code IS NOT NULL
GROUP BY b.enterprise_type, b.org_size, b.province_code, b.province;

-- city：按市汇总
INSERT INTO dwd.enterprise_type_scale_stats
(company_type, enterprise_scale, region_level, region_code, region_name, enterprise_count, stat_date)
SELECT b.enterprise_type, b.org_size, 'city', b.city_code, b.city,
       COUNT(*), CURRENT_DATE
FROM dwd.enterprise_base b
WHERE b.enterprise_type IS NOT NULL AND b.org_size IS NOT NULL AND b.city_code IS NOT NULL
GROUP BY b.enterprise_type, b.org_size, b.city_code, b.city;
```

**接口查询示例**：

```sql
-- 类型×规模交叉统计（按 region_level 切换国/省/市）
SELECT company_type, enterprise_scale, region_code, region_name, enterprise_count
FROM dwd.enterprise_type_scale_stats
WHERE region_level = %s
  AND stat_date = (SELECT MAX(stat_date) FROM dwd.enterprise_type_scale_stats WHERE region_level = %s)
ORDER BY company_type, enterprise_scale;
```

**设计说明**：
- `enterprise_stat_summary` 用 `stat_type` 区分口径，避免为重点企业介绍的每个统计场景各建一张表，降低表数量维护成本。
- `enterprise_type_scale_stats` 独立建表是因为其维度（company_type × enterprise_scale × region）与 `enterprise_stat_summary` 的单维度模型不匹配（三维度交叉），强行塞进 stat_summary 会导致 dim_code 拼接过长且语义不清。
- 两张表均为日更 ETL，取数据时 `stat_date = (SELECT MAX(stat_date) ...)` 取最新跑批日期。

---

## 8. 后续工作

1. **本文档定稿后** → DDL 已就绪，导入 dwd schema
2. **DDL 入库后** → 评估 ES 索引设计是否需要调整（字段名/来源对齐）
3. **ES 定稿后** → 继续 Python 代码开发（enterprise_profile.py 的 PG 查询逻辑改为查独立表）
4. **ETL 开发**（data-agent 职责）：ODS → DWD 的数据加载脚本
5. **v2.1 新增字段 ETL**：enterprise_extra 补 12 字段、enterprise_finance_history 补 3 字段、enterprise_history_name 新表的 ODS→DWD 加载脚本
6. **算法侧对接**：tech_score / business_score 评分产出后写入 enterprise_score 表
7. **业务确认**：is_chain_leader 链主判定规则（🟡 待甲方确认）
8. **v2.2 新增**：enterprise_industry_summary ETL 脚本（含 chain_code='ALL' 去重汇总逻辑）；research_staff_total 科研人口径待甲方确认（🟡）
9. **v2.3 新增**：enterprise_stat_summary + enterprise_type_scale_stats ETL 脚本（含 5 种 stat_type 口径 + 3 级 region 聚合）；重点企业判定规则（key_enterprise 标签）待业务确认（🟡）
10. **v2.4 新增**：enterprise_star 明星企业预定义表的入选规则待业务确认（🟡）；enterprise_stat_summary 追加 star_enterprise_node/star_enterprise_district 两种 stat_type 的 ETL 脚本
11. **v2.5 新增**：shenzhen_enterprise_summary ETL 脚本（含 4 种 stat_type 口径：enterprise_total/key_enterprise_total/industry_distribution/yearly_growth）；历年累计增长趋势若 ES 性能不够则改用预聚合


---

## 9. 明星企业预定义表（v2.4 新增）

> v2.4 新增，支撑"科技专题-明星企业介绍"模块。明星企业为人工/业务预定义清单，ETL 读取此表给对应企业打 `star_enterprise` 标签写入 ES tags_flat，后续查询通过标签检索。

### 9.1 enterprise_star

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | BIGSERIAL | PK | 自增主键 |
| org_id | VARCHAR(64) | NOT NULL, UNIQUE | 企业ID |
| enterprise_name | VARCHAR(255) | NOT NULL | 企业名称（冗余） |
| star_type | VARCHAR(50) | | 明星类型（待业务定义） |
| star_level | VARCHAR(50) | | 明星级别（待业务定义） |
| description | TEXT | | 明星企业简介 |
| sort_order | INTEGER | NOT NULL DEFAULT 0 | 排序序号 |
| is_active | BOOLEAN | NOT NULL DEFAULT TRUE | 是否生效 |
| create_time | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 记录创建时间 |
| update_time | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 记录更新时间 |

**设计说明**：
- 明星企业为预定义清单，不依赖算法计算，由业务/运营人工维护。
- ETL 逻辑：每日扫描 `enterprise_star WHERE is_active=TRUE`，给对应 `org_id` 的企业打 `star_enterprise` 标签写入 `enterprise_tag` 表 + ES `tags_flat`。
- `star_type` / `star_level` 字段待业务确认入选规则后补充具体值域（🟡）。
- 表结构待定，业务确认明星企业入选规则后可能追加字段。

### 9.2 enterprise_stat_summary 新增 stat_type

v2.4 在 `enterprise_stat_summary` 通用统计表中追加 2 种 stat_type，复用同一张表：

| stat_type | 含义 | dim_code | dim_name | 服务于 |
|---|---|---|---|---|
| `star_enterprise_node` | 明星企业按产业链环节统计 | chain_code:node_id | chain_name:node_name | 明星企业 KPI-覆盖环节数 |
| `star_enterprise_district` | 明星企业按行政区统计 | province_code:city_code | province:city | 明星企业 KPI-覆盖行政区数 |
| `patent_valid_count` | 有效专利数按产业统计 | chain_code | chain_name | 高级筛选-有效专利数按产业聚合 |
| `high_value_patent_count` | 高价值专利数按产业统计 | chain_code | chain_name | 高级筛选-高价值专利数按产业聚合 |

**ETL 逻辑**：与 key_enterprise_node / key_enterprise_district 相同，仅将 tag_code 从 `key_enterprise` 改为 `star_enterprise`。


---

## 10. 深圳企业统计汇总表（v2.5 新增）

> v2.5 新增，支撑"科技专题-深圳企业介绍"模块。深圳统计单独建表，不走通用 `enterprise_stat_summary`（用户明确要求）：region_id 维度固定为 440300（深圳市），统计口径独立，避免与通用统计表口径混淆。

### 10.1 shenzhen_enterprise_summary

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | BIGSERIAL | PK | 自增主键 |
| stat_type | VARCHAR(50) | NOT NULL | 统计类型编码 |
| dim_code | VARCHAR(100) | NOT NULL | 维度编码（语义随 stat_type 变化） |
| dim_name | VARCHAR(255) | NOT NULL | 维度名称（人类可读） |
| stat_year | INTEGER | NOT NULL DEFAULT 0 | 统计年份（0=累计；yearly_growth 时为具体年份） |
| stat_value | INTEGER | NOT NULL DEFAULT 0 | 统计值（企业数） |
| stat_date | DATE | NOT NULL | 统计日期（ETL 跑批日期，取最新日期） |
| create_time | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 记录创建时间 |
| update_time | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 记录更新时间（ETL） |

**唯一约束**：(stat_type, dim_code, stat_year, stat_date)

### 10.2 stat_type 枚举

| stat_type | 含义 | dim_code | dim_name | stat_year | 服务于 |
|---|---|---|---|---|---|
| `enterprise_total` | 深圳企业总数 | `440300` | `深圳市` | 0 | 深圳 KPI 卡片-企业总数 |
| `key_enterprise_total` | 深圳重点企业总数 | `440300` | `深圳市` | 0 | 深圳 KPI 卡片-重点企业数 |
| `industry_distribution` | 深圳企业按产业分布 | chain_code | chain_name | 0 | 深圳产业分布统计 |
| `yearly_growth` | 深圳企业历年累计增长 | `440300` | `深圳市` | 年份（如 2024） | 深圳历年累计增长趋势 |

### 10.3 设计说明

- **为何单独建表**：深圳企业介绍的统计维度（region_id 固定 440300）与通用 `enterprise_stat_summary` 的多维度模型不完全契合。深圳历年累计增长趋势（yearly_growth）是按成立时间累计统计，与 stat_summary 的"全量统计"语义不同。用户明确要求深圳统计单独建表，避免口径混淆。
- **历年累计趋势口径**：`yearly_growth` 的 `stat_value` 为"该年及之前成立的企业累计数"，即 2024 年 = 成立日期 ≤ 2024-12-31 的企业数。ETL 每年补一行，保证逐年递增。
- **重点企业清单不走此表**：重点企业平铺列表走 ES 实时查询（filter region_id=440300 + tags_flat contains key_enterprise），不走 DWD 统计表。
- **历年趋势优先用此表**：若 DWD `yearly_growth` 有数据则取预聚合值；若无则回退 ES 实时聚合（date_range aggregation on incorporation_date, filter region_id=440300）。考虑 2 亿企业量级，ES 性能不够时优先用预聚合。

### 10.4 ETL 逻辑

```sql
-- 1. enterprise_total：深圳企业总数
INSERT INTO dwd.shenzhen_enterprise_summary
(stat_type, dim_code, dim_name, stat_year, stat_value, stat_date)
SELECT 'enterprise_total', '440300', '深圳市', 0, COUNT(*), CURRENT_DATE
FROM dwd.enterprise_base
WHERE region_id = '440300';

-- 2. key_enterprise_total：深圳重点企业总数
INSERT INTO dwd.shenzhen_enterprise_summary
(stat_type, dim_code, dim_name, stat_year, stat_value, stat_date)
SELECT 'key_enterprise_total', '440300', '深圳市', 0, COUNT(DISTINCT t.org_id), CURRENT_DATE
FROM dwd.enterprise_tag t
JOIN dwd.enterprise_base b ON t.org_id = b.org_id
WHERE t.tag_code = 'key_enterprise' AND b.region_id = '440300';

-- 3. industry_distribution：按产业统计深圳企业数
INSERT INTO dwd.shenzhen_enterprise_summary
(stat_type, dim_code, dim_name, stat_year, stat_value, stat_date)
SELECT 'industry_distribution', c.chain_code, c.chain_name, 0,
       COUNT(DISTINCT b.org_id), CURRENT_DATE
FROM dwd.enterprise_base b
JOIN dwd.enterprise_industry_chain c ON b.org_id = c.org_id
WHERE b.region_id = '440300'
GROUP BY c.chain_code, c.chain_name;

-- 4. yearly_growth：历年累计增长（2024 年 = 成立日期 ≤ 2024-12-31 的企业累计数）
INSERT INTO dwd.shenzhen_enterprise_summary
(stat_type, dim_code, dim_name, stat_year, stat_value, stat_date)
SELECT 'yearly_growth', '440300', '深圳市', y.year_val,
       COUNT(*) FILTER (WHERE b.registration_date <= (y.year_val || '-12-31')::date),
       CURRENT_DATE
FROM dwd.enterprise_base b, generate_series(2015, EXTRACT(YEAR FROM CURRENT_DATE)::int) AS y(year_val)
WHERE b.region_id = '440300'
GROUP BY y.year_val;
```

### 10.5 接口查询示例

```sql
-- KPI：深圳企业总数 + 重点企业总数
SELECT stat_type, stat_value FROM dwd.shenzhen_enterprise_summary
WHERE stat_type IN ('enterprise_total', 'key_enterprise_total')
  AND stat_date = (SELECT MAX(stat_date) FROM dwd.shenzhen_enterprise_summary);

-- 产业分布
SELECT dim_code AS chain_code, dim_name AS chain_name, stat_value AS enterprise_count
FROM dwd.shenzhen_enterprise_summary
WHERE stat_type = 'industry_distribution'
  AND stat_date = (SELECT MAX(stat_date) FROM dwd.shenzhen_enterprise_summary WHERE stat_type = 'industry_distribution')
ORDER BY stat_value DESC;

-- 历年累计增长趋势
SELECT stat_year, stat_value AS cumulative_count
FROM dwd.shenzhen_enterprise_summary
WHERE stat_type = 'yearly_growth'
  AND stat_date = (SELECT MAX(stat_date) FROM dwd.shenzhen_enterprise_summary WHERE stat_type = 'yearly_growth')
ORDER BY stat_year ASC;
```

