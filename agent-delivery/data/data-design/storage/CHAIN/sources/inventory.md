# CHAIN · ODS 表级清单

```yaml
---
doc_id: CHAIN-SOURCE-INVENTORY
element: CHAIN
role: source
status: draft
version: "2026-08-13"
updated: 2026-08-13
---
```

> **真源**：权威 `third-party-source/doc/` xlsx；日常读 `doc/md-extract/`。  
> Sheet：`市场研究（金融、宏观行业、行业分析、产业链）数据汇总表` → **产业链要素库**。  
> CSV：`doc/md-extract/_csv/市场研究（金融、宏观行业、行业分析、产业链）数据汇总表__产业链要素库.csv`  
> **禁止**：以 `gkx-mysql-raw` as-built 改写本清单；默认写入正式 `gkxlumenx_ods`。  
> **并列切片**（不要并进本表）：行业分析六表见 [`inventory-industry-analysis.md`](./inventory-industry-analysis.md)。

## 约定四表（角色 = ODS）

供应方表名带 `dwd_`，**不是**项目 v5 DWD（`industry_chain_*` 14 表）。

| # | 约定表名 | 中文 | Demo 库 | 业务键（文档「是否为主键」） | 字段数 |
|---|---|---|---|---|---|
| 1 | `dwd_industry_chain_info` | 产业链图谱 | `demo_gkxlumenx_ods` | `industry_link_code` | 8 |
| 2 | `dwd_org_industry_tags` | 产业关联企业信息 | 同上 | `credit_code` | 6 |
| 3 | `dwd_org_industry_product_tags` | 产业链关联产品信息 | 同上 | `credit_code` | 9 |
| 4 | `dwd_industry_chain_news_info` | 产业动态资讯 | 同上 | `id` | 7 |

> **资讯使用（2026-08-25）**：表 4 **不可用**（合规交付、无实用价值）。产业/行业资讯改用 [`inventory-industry-analysis.md`](./inventory-industry-analysis.md) 与企业要闻 `dwd_org_important_news_info`。本清单仍保留表名，只作对照，禁止 Mapping。

Demo DDL 另加 `_demo_id` BIGINT AUTO_INCREMENT 作物理主键；业务键建 `KEY`。

## 字段摘要（Demo MySQL 类型）

生成器：`repos/demo-algo-ent-analysis/scripts/run_chain_ods.py`（复用 `entan/llm_ods`）。超长「字符」→ TEXT；「数字」→ DECIMAL。

### `dwd_industry_chain_info`

| 英文字段 | 中文 | MySQL | 业务键 |
|---|---|---|---|
| industry_code | 产业链编码 | VARCHAR(255) | |
| industry_name | 产业链名称 | VARCHAR(255) | |
| industry_link_code | 节点代码 | VARCHAR(255) NOT NULL | ✓ |
| industry_link_name | 节点名称 | VARCHAR(255) | |
| level | 节点层级 | DECIMAL(20,0) | |
| parent_code | 父级节点代码 | VARCHAR(255) | |
| parent_name | 父级节点名称 | VARCHAR(255) | |
| node_company_count | 节点企业数量 | DECIMAL(20,0) | |

### `dwd_org_industry_tags`

| 英文字段 | 中文 | MySQL | 业务键 |
|---|---|---|---|
| industry_code | 产业链编码 | TEXT | |
| industry_name | 产业链名称 | TEXT | |
| industry_link_code | 节点代码 | TEXT | |
| industry_link_name | 节点名称 | TEXT | |
| company_name | 企业名称 | VARCHAR(500) | |
| credit_code | 统一社会信用代码 | VARCHAR(255) NOT NULL | ✓ |

### `dwd_org_industry_product_tags`

| 英文字段 | 中文 | MySQL | 业务键 |
|---|---|---|---|
| industry_code | 产业链编码 | TEXT | |
| industry_name | 产业链名称 | TEXT | |
| industry_link_code | 节点代码 | TEXT | |
| industry_link_name | 节点名称 | TEXT | |
| id | 企业ID | DECIMAL(20,4) | |
| company_name | 企业名称 | VARCHAR(500) | |
| credit_code | 统一社会信用代码 | VARCHAR(255) NOT NULL | ✓ |
| product_name | 产品名称 | TEXT | |
| product_top5 | TOP5产品技术词 | TEXT | |

### `dwd_industry_chain_news_info`

| 英文字段 | 中文 | MySQL | 业务键 |
|---|---|---|---|
| industry_code | 产业链编码 | TEXT | |
| industry_name | 产业链名称 | TEXT | |
| id | 资讯id | VARCHAR(255) NOT NULL | ✓ |
| title | 标题 | VARCHAR(255) | |
| publish_date | 发布时间 | DATE | |
| abstract | 摘要 | TEXT | |
| source | 来源 | VARCHAR(500) | |

## 建表产物

| 项 | 路径 |
|---|---|
| DDL（已生成） | [`../etl/demo_gkxlumenx_ods_chain_tables.sql`](../etl/demo_gkxlumenx_ods_chain_tables.sql) |
| 脚本 | `${GKX_ROOT}/repos/demo-algo-ent-analysis/scripts/run_chain_ods.py` |
| 自检 | `python scripts/run_chain_ods.py --self-check` |
| 直连建表 | `python scripts/run_chain_ods.py --apply`（需可达 `demo` MySQL） |
| **在线 vs 三方四表差异** | [`md-extract-vs-live-ods-diff.md`](./md-extract-vs-live-ods-diff.md) |

## 开放项

| ID | 说明 | 状态 |
|---|---|---|
| OPEN-CHAIN-S2-01 | 经 `ENTAN_MYSQL_HOST=111.198.38.90` `PORT=34306` 对 `demo_gkxlumenx_ods` `--apply` 成功；证据 `repos/demo-algo-ent-analysis/out/chain_demo_ods_show_create.sql` | **关闭** |
| OPEN-CHAIN-S2-02 | 产品表 `id` 文档类型为「数字」→ DECIMAL；若供应方实为字符 ID，待样本确认后改映射 | 开放 |
