# 10-DWD-MySQL-DDL — 建表 / ALTER 唯一真源

> **工作包**：GDF-ENT-WORKPACK-v2.1  
> **冻结日期**：2026-08-13  
> **目标库**：MySQL 8 · **`gkxlumenx_dwd`**（正式库；**不是** `demo_gkxlumenx_dwd`，也不是 PG `demo_gdf_data`）  
> **仓内真源**：`agent-delivery/data/data-design/企业/` 下同名三份设计稿；本目录为冻结快照。  
> **Mapping**：字段级见本包 `09-企业域-ETL-Mapping明细-源表到DWD.md`

## 铁律

1. 引擎 **仅 MySQL**；禁止 PostgreSQL / schema `dwd` / `demo_gdf_data`。  
2. 技术主键统一 `id bigint NOT NULL AUTO_INCREMENT`。  
3. 企业关联键优先 **`org_id`**（风险域 `org_id` 列 collation = `utf8mb4_general_ci`）。  
4. **禁止**建宽表 `enterprise`；主数据表是 **`enterprise_base`**。  
5. **禁止**在信用代码为空时自行生成第三方 `org_id`。  
6. 细节字段以本目录三份快照正文为准。

## 快照文件

| 文件 | 范围 |
|------|------|
| [DWD表结构设计-企业工商表-MySQL-v3.1.md](./DWD表结构设计-企业工商表-MySQL-v3.1.md) | 工商/实体 + **`enterprise_recruit`** + **`enterprise_forg_*`** |
| [DWD表结构设计-企业模块-MySQL-v3.0.md](./DWD表结构设计-企业模块-MySQL-v3.0.md) | 风险 `risk_*` + party |
| [DWD表结构设计-企业指标汇总表-MySQL-v3.1.md](./DWD表结构设计-企业指标汇总表-MySQL-v3.1.md) | 指标/预聚合 |

## A. 工商 / 实体明细（国内）

| # | 表名 | 关联键摘要 |
|---:|------|------------|
| 1–20 | 见工商 v3.1 §2（`enterprise_base` … `enterprise_industry_product`） | 多为 `org_id` |
| 21 | **`enterprise_recruit`**（v2.1 强调） | `org_id`；UK `(org_id, release_date, job_title)` |

纠偏备忘：勿建 `enterprise_base2`；`enterprise_industry_chain.org_id` 可空；`enterprise_financing` 保持 `finance_round/amount/currency/investors/event_date`。

## B. 国外机构（`enterprise_forg_*` · 工商 v3.1 §6）

| # | 表名 | 源表（Mapping） |
|---:|------|-----------------|
| 1 | `enterprise_forg_base` | `dwd_forg_base_info` |
| 2 | `enterprise_forg_extra` | base + `dwd_forg_product_info` |
| 3 | `enterprise_forg_executive` | `dwd_forg_executive_info` |
| 4 | `enterprise_forg_finance_history` | `dwd_foreign_org_annual_financial_info` |
| 5 | `enterprise_forg_invest` | `dwd_forg_shareholder_info` |
| 6 | `enterprise_forg_parent_subsidiary` | `dwd_forg_subsidiary_info` |

## C. 风险明细（模块 MySQL-v3.0）

主表 18 + party 6（清单同 v2.0）。字段级见 Mapping 明细 §3.13。

## D. 指标 / 预聚合

同 v2.0（`enterprise_region_summary` … `sz_city_benchmark`）。聚合逻辑见 Mapping 明细 §4。  
**勿建**：`enterprise_score`（ADS）、`enterprise_star`（配置）。

## E. 验收（GDF 自检）

- [ ] 含 `enterprise_recruit`、六张 `enterprise_forg_*`  
- [ ] 无宽表 `enterprise`、无 `enterprise_base2`  
- [ ] 风险 `org_id` JOIN `enterprise_base` 无 1267  
