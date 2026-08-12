# 10-DWD-MySQL-DDL — 建表 / ALTER 唯一真源

> **工作包**：GDF-ENT-WORKPACK-v2.0  
> **冻结日期**：2026-08-13  
> **目标库**：MySQL 8 · **`gkxlumenx_dwd`**（正式库；**不是** `demo_gkxlumenx_dwd`，也不是 PG `demo_gdf_data`）  
> **仓内真源**（本侧维护）：`agent-delivery/data/data-design/企业/` 下同名三份设计稿；本目录为 **投递给 GDF 的冻结快照**。DDL 变更须升工作包版本后重发。

## 铁律

1. 引擎 **仅 MySQL**；禁止 PostgreSQL / schema `dwd` / `demo_gdf_data`。  
2. 技术主键统一 `id bigint NOT NULL AUTO_INCREMENT`。  
3. 企业关联键优先 **`org_id`**（风险域 `org_id` 列 collation = `utf8mb4_general_ci`，与 `enterprise_base` 对齐，防 1267）。  
4. **禁止**建宽表 `enterprise`；主数据表是 **`enterprise_base`**。  
5. **禁止**在信用代码为空时自行生成第三方 `org_id` 回填。  
6. 细节字段 / CREATE 语句以本目录三份快照正文为准；本 README 只给总览。

## 快照文件

| 文件 | 范围 |
|------|------|
| [DWD表结构设计-企业工商表-MySQL-v3.1.md](./DWD表结构设计-企业工商表-MySQL-v3.1.md) | 工商/实体 `enterprise_*` 明细 |
| [DWD表结构设计-企业模块-MySQL-v3.0.md](./DWD表结构设计-企业模块-MySQL-v3.0.md) | 风险 `risk_*` + party + 部分复核表 |
| [DWD表结构设计-企业指标汇总表-MySQL-v3.1.md](./DWD表结构设计-企业指标汇总表-MySQL-v3.1.md) | 指标/预聚合表 |

## A. 工商 / 实体明细（来自工商 v3.1）

| # | 表名 | 关联键摘要 |
|---:|------|------------|
| 1 | `enterprise_base` | `org_id` UK 语义；`enterprise_code` |
| 2 | `enterprise_extra` | `org_id` |
| 3 | `enterprise_executive` | `org_id` |
| 4 | `enterprise_bid` | `org_id` |
| 5 | `enterprise_news` | `org_id` |
| 6 | `enterprise_finance_history` | `org_id` |
| 7 | `enterprise_financing` | `org_id`；字段契约 `finance_round` / `amount` / `currency` / `investors` / `event_date` |
| 8 | `enterprise_industry_chain` | `org_id`（可空历史债：现网可能全 NULL，禁止自造 org_id 回填） |
| 9 | `enterprise_tag` | `org_id` |
| 10 | `enterprise_invest` | `org_id` |
| 11 | `enterprise_supply_chain` | `org_id` |
| 12 | `enterprise_cooperation` | `org_id` |
| 13 | `enterprise_innovation_carrier` | `org_id` |
| 14 | `enterprise_parent_subsidiary` | `org_id` |
| 15 | `enterprise_history_name` | `org_id` |
| 16 | `enterprise_patent_detail` | `org_id` + `patent_id` |
| 17 | `enterprise_patent_history` | `org_id` |
| 18 | `enterprise_fund_project` | `org_id` |
| 19 | `enterprise_chain_patent` | `org_id`（可空表） |
| 20 | `enterprise_industry_product` | `org_id`（可空表） |

纠偏备忘（须写入迁移说明）：

- 已删除孤立表 `enterprise_base2`（勿再建）。  
- `enterprise_industry_chain` 须有可空 `org_id varchar(64)` 及索引；历史行可暂 NULL。  
- `enterprise_financing` **保持**现行字段名，勿改成另一套融资列名。

## B. 风险明细（来自模块 MySQL-v3.0）

**风险主表（18）**

`risk_judicial_case` · `risk_dishonest` · `risk_executed` · `risk_limit_high` · `risk_lawsuit` · `risk_court_filed` · `risk_court_notice` · `risk_court_announcement` · `risk_equity_freeze` · `risk_equity_pledge` · `risk_zhongben` · `risk_chattel_mortgage` · `risk_judicial_sale` · `risk_bankruptcy` · `risk_abnormal` · `risk_punishment` · `risk_illegal` · `risk_tax_punish`

**party 表（6）**

`risk_lawsuit_party` · `risk_court_filed_party` · `risk_court_notice_party` · `risk_court_announcement_party` · `risk_judicial_sale_party` · `risk_bankruptcy_party`

字段级 DDL 见模块快照正文；本波 Mapping 可施工子集见 `09` §5。

## C. 指标 / 预聚合（来自指标汇总 v3.1 + 模块补充）

| 表名 | 说明 |
|------|------|
| `enterprise_region_summary` | 区域 KPI |
| `enterprise_industry_distribution` | 区内产业分布 |
| `enterprise_growth_trend` | 月度增长 |
| `enterprise_industry_summary` | 产业 KPI |
| `enterprise_stat_summary` | 通用单维统计 |
| `enterprise_type_scale_stats` | 三维交叉 |
| `shenzhen_enterprise_summary` | 深圳专题 |
| `enterprise_risk_summary` | `org_id × risk_type` 长表 |
| `enterprise_org_type` | 机构类型 |
| `enterprise_distribution` | 见模块 v3.0 |
| `sz_city_benchmark` | 见模块 v3.0 |

**勿当本层 DWD 汇总建表**：`enterprise_score`（ADS）、`enterprise_star`（配置）。

## D. 验收（GDF 自检）

- [ ] `SHOW TABLES` / 信息_schema 与上表差集已列出并处理  
- [ ] 无宽表 `enterprise`、无 `enterprise_base2`、无 PG 类型残留  
- [ ] `enterprise_base.org_id` 与风险表 `org_id` JOIN 无 1267  
- [ ] 变更已回写本侧（飞书 + 迁移说明）
