# 企业 DWD 四类分类表（DOC 工作稿）

> **核验**：2026-09-03 `information_schema` via `gkxlumenx-dwd-public`  
> **库**：`gkxlumenx_dwd`（正式）· `demo_gkxlumenx_dwd`（对照，同一套 ADD）  
> **规则**：Q-WP3-29。`id` 忽略。demo 不当真源。

## 1. 改名（跟正式库）

| 表 | 设计/demo 名 | 正式库名 | ETL |
|----|--------------|----------|-----|
| `enterprise_bid` | `announcement_title` / `project_name` | `bid_title` | 读 `bid_title`，ES 仍写 `announcement_title` |
| `enterprise_bid` | `announcement_date` | `event_date` | 读 `event_date`，ES 仍写 `announcement_date` |
| `enterprise_bid` | `winning_amount` | `bid_amount` | 读 `bid_amount` |
| `enterprise_news` | `news_title` | `title` | 读 `title` |
| `enterprise_news` | `news_date` | `publish_time` | 读 `publish_time` |
| `enterprise_news` | `news_content` | `summary` | 读 `summary`（全文） |
| `enterprise_invest` | `inv_name` | `inv_org_name` | 读 `inv_org_name` |
| `enterprise_invest` | `investment_amount` / `investment_ratio` | `invest_amount` / `invest_ratio` | 已改读 |
| `enterprise_finance_history` | （设计用 `total_profit` 双写 ES `pure_profit`） | `net_profit` | ES `pure_profit` ← `net_profit` |

## 2. 设计有、正式从未有 → ADD（两库同一套；旧同义列不 DROP）

| 表 | ADD | 备注 |
|----|-----|------|
| `enterprise_extra` | `stock_noun` `listed_status` `capital_currency_code` `registration_org` `postal_code` `start_date` `end_date` | 正式缺；**demo 已有**，正式 ADD |
| `enterprise_finance_history` | `main_business_revenue` `total_profit` `total_fixed_assets` | 正式缺；**demo 已有** |
| `enterprise_finance_history` | `net_profit` | **正式已有**；**demo 缺** → demo ADD |
| `enterprise_news` | `original_url` | 正式缺；demo 已有 |
| `enterprise_bid` | `project_no` | 正式缺；demo 已有 |
| `enterprise_patent_detail` | v3.1 宽列（`title_zh` / `abstract_zh` / `publication_*` / `grant_*` / `ipc_main` / `cpc_main` / 引用数等） | 现网 `patent_name`/`publish_date`/`ipc_code` 不 DROP |
| `enterprise_patent_history` | `patent_invention_count` `latest_patent_date` `latest_grant_date` | Q-WP3-28 |
| `enterprise_executive` | `data_source`（正式） / `gender`（demo） | 正式有 `gender` 无 `data_source`；demo 相反。**两库互相 ADD，不 DROP** |

## 3. 正式有、设计 8-12 写丢 → 回写设计稿

正式 `enterprise_base` 已有（7-29 ETL 用过或现网在）：  
`enterprise_name_short` `headquarters_*` `is_foreign` `is_high_tech` `is_sme` `is_little_giant` `little_giant_level` `is_gazelle` `is_unicorn` `revenue_latest` `revenue_year` `revenue_growth_rate` `net_profit` `profit_margin` `gross_margin` `market_share` `brand_score` `customer_concentration` 专利/研发宽列等。

**禁止 DROP。** DOC 回写 v3.1。

## 4. 待核（7-29 SELECT 没写到、又不能证明是后加）

`brand_score` `customer_concentration` `market_share` `core_tech_coverage` `tech_transaction_amount` 等 KPI 宽列：正式在、设计无。按 (3)/(4) **保留并回写**，本叶不猜口径、不洗。

## 5. 灌数仓 `demo-algo-science`

只做旧表名 → `demo_gkxlumenx_*` 库表映射（`innov/common/tables.py`），**无工商列名硬编码**。本管线 **不改** 该仓。DDL 把 demo DWD 列补到与正式同一套后，灌数仍只认表名。

## 6. 拟 ALTER（给 DDL 叶）

对 **`gkxlumenx_dwd` 与 `demo_gkxlumenx_dwd`**：缺哪列 ADD 哪列；已有则跳过；禁止 DROP。

执行前再 `SHOW CREATE` 快照。
