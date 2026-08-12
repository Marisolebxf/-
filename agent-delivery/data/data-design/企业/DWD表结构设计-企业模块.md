# DWD 表结构设计 — 企业模块（已归档）

> **状态**：历史稿（PostgreSQL `dwd` 大稿 v2.6）已迁出，**不再作为落库 DDL 真源**。  
> **归档位置**：`agent-delivery/_archive/2026-08/data-design-企业-legacy/DWD表结构设计-企业模块.md`  
> **近副本**：同目录 `DWD表结构设计-企业模块-old.md`（亦已归档）

## 请改用（MySQL 现网）

| 文档 | 用途 |
|---|---|
| [`DWD表结构设计-企业模块-MySQL-v3.0.md`](./DWD表结构设计-企业模块-MySQL-v3.0.md) | 风险 24 表 + 已复核非风险 / API 兼容 / 迁移 as-built |
| [`DWD表结构设计-企业工商表-MySQL-v3.1.md`](./DWD表结构设计-企业工商表-MySQL-v3.1.md) | 工商/实体 `enterprise_*` 现网 as-built（含 `enterprise_base`） |
| [`DWD表结构设计-企业指标汇总表-MySQL-v3.1.md`](./DWD表结构设计-企业指标汇总表-MySQL-v3.1.md) | KPI / 预聚合汇总（含 `enterprise_risk_summary`） |

字段语义若需对照旧 PG 叙述，只读归档件；改表以 MySQL 三份为准。
