# CHAIN · ODS 表级清单（骨架）

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

> **S1**：锁定真源 + 表名。**S2**：补字段/类型/可空与建表证据。  
> Sheet：`市场研究（金融、宏观行业、行业分析、产业链）数据汇总表` → **产业链要素库**。  
> CSV：`doc/md-extract/_csv/市场研究（金融、宏观行业、行业分析、产业链）数据汇总表__产业链要素库.csv`

| # | 约定表名（英文） | 中文 | 角色 | Demo 库 | 备注 |
|---|---|---|---|---|---|
| 1 | `dwd_industry_chain_info` | 产业链图谱 | 约定 ODS | `demo_gkxlumenx_ods` | 供应方命名含 `dwd_`；**非**项目 DWD |
| 2 | `dwd_org_industry_tags` | 产业关联企业信息 | 约定 ODS | 同上 | |
| 3 | `dwd_org_industry_product_tags` | 产业链关联产品信息 | 约定 ODS | 同上 | |
| 4 | `dwd_industry_chain_news_info` | 产业动态资讯 | 约定 ODS | 同上 | |

**禁止**：以 `gkx-mysql-raw` as-built 改写上表；写入正式 `gkxlumenx_ods`。
