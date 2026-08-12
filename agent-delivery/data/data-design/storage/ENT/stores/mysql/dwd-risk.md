# MySQL DWD · 企业风险

```yaml
---
doc_id: ENT-STORE-DWD-RISK
element: ENT
role: store-mysql
status: draft
version: "2026-08-12"
updated: "2026-08-12"
engine: mysql
as_built_source: data-design/企业/DWD表结构设计-企业模块-MySQL-v3.0.md
s3_task: DATA-ENT-STORAGE-S3-L01
---
```

> **DDL / 字段真源**：[`DWD表结构设计-企业模块-MySQL-v3.0.md`](../../../企业/DWD表结构设计-企业模块-MySQL-v3.0.md)（风险主表 + party；§11 as-built）。  
> **库**：`gkxlumenx_dwd`。预聚合风险计数见 [`dwd-aggregate.md`](./dwd-aggregate.md) 的 `enterprise_risk_summary`。  
> **status=draft**（待单独结构评审）。

## 1. 范围

| 类别 | 数量 | 说明 |
|---|---:|---|
| 风险主表 | 18 | 司法/经营异常/处罚等明细 |
| 风险 party 表 | 6 | 案件多方；`is_history` 在 party |

`org_id` 列级 collation = `utf8mb4_general_ci`（与 `enterprise_base` JOIN，防 1267）。

## 2. 风险主表清单

`risk_judicial_case` · `risk_dishonest` · `risk_executed` · `risk_limit_high` · `risk_lawsuit` · `risk_court_filed` · `risk_court_notice` · `risk_court_announcement` · `risk_equity_freeze` · `risk_equity_pledge` · `risk_zhongben` · `risk_chattel_mortgage` · `risk_judicial_sale` · `risk_bankruptcy` · `risk_abnormal` · `risk_punishment` · `risk_illegal` · `risk_tax_punish`

## 3. party 表清单

`risk_lawsuit_party` · `risk_court_filed_party` · `risk_court_notice_party` · `risk_court_announcement_party` · `risk_judicial_sale_party` · `risk_bankruptcy_party`

## 4. 读写与 API

| 写 | 读 |
|---|---|
| GDF / ETL | 详情走 DWD；检索风险筛选优先用 `enterprise_risk_summary`；Python 映射稳定 API 字段（契约不变） |

**禁止**：Java 直扫风险明细拼契约面；ES 灌入全量司法 nested（见 ES 设计：只存 risk 计数/等级）。
