# MySQL DWD · 产业链标准明细（v5）

```yaml
---
doc_id: CHAIN-STORE-DWD
element: CHAIN
role: store-mysql
status: draft
version: "2026-08-13"
updated: "2026-08-13"
engine: mysql
s3_task: DATA-CHAIN-STORAGE-S3-L01
as_built_source: data-design/产业链/产业链-DWD表设计-业务需求驱动(v5).md
---
```

> **DDL / 字段真源**：[`产业链-DWD表设计-业务需求驱动(v5).md`](../../../../产业链/产业链-DWD表设计-业务需求驱动(v5).md)（**勿在本文件粘贴全 DDL**）。  
> **库**：正式 `gkxlumenx_dwd`；Demo `demo_gkxlumenx_dwd`。表名 **无** `dwd_` 前缀，统一 `industry_chain_*`。  
> **对照（勿当真源）**：[`DATA-CHAIN-db-design.md`](../../../../../agent-handoffs/产业链分析-CHAIN/DATA-CHAIN-db-design.md) 旧 PG/8 表稿。  
> **ODS 入站**：供应方四表见 [`../../sources/inventory.md`](../../sources/inventory.md)；映射见 Step2 复核报告。

## 1. 写读

| 写 | 读 |
|---|---|
| Python ETL / 模拟 GDF（[`../../etl/pipeline-ods-to-dwd.md`](../../etl/pipeline-ods-to-dwd.md)） | Python / algorithm；**Java 不扫 DWD 对外** |

## 2. 表清单（v5 · 14 张）

| # | 表 | 中文 | 一行语义 |
|---|---|---|---|
| 1 | `industry_chain` | 产业链标准信息 | L0 产业与 L1+ 子链名录（`industry_id`/`chain_tier`） |
| 2 | `industry_chain_node` | 节点信息 | 链内标准节点 |
| 3 | `industry_chain_node_rel` | 节点关系 | 上下游/供需等结构边 |
| 4 | `industry_chain_entity_rel` | 实体关系 | 链/节点 ↔ 企业等外部实体 |
| 5 | `industry_chain_market_observation` | 市场指标观测 | 外部导入原子观测；**平台市场规模不进本表** |
| 6 | `industry_chain_investment_event` | 投融资事件 | 资本事件主数据 |
| 7 | `industry_chain_investment_participant` | 投融资参与方扩展 | 金额等扩展；角色在 event_entity_rel |
| 8 | `industry_chain_news_event` | 资讯事件 | 产业资讯主数据 |
| 9 | `industry_chain_milestone_event` | 里程碑（可选） | 门户历程以 CMS 为准 |
| 10 | `industry_chain_event_entity_rel` | 事件实体关系 | 事件 ↔ 实体 |
| 11 | `industry_chain_event_metric_observation` | 事件指标观测 | 浏览/互动等时序 |
| 12 | `industry_chain_extraction_result` | 抽取结果 | NLP 实体/关系明细 |
| 13 | `industry_chain_model_run` | 模型运行 | 可复现运行记录 |
| 14 | `industry_chain_model_result_detail` | 模型结果明细 | 单次运行原子结果 |

主键口径：`chain_id` / `node_id` / `industry_id` = INB 升格（Q053）。

## 3. 冲突说明

| 旧稿 | 本树裁决 |
|---|---|
| DATA-CHAIN-db-design 8 张 / PG schema | **废作 DWD 真源**；仅历史对照 |
| 供应方 `dwd_industry_chain_info` 等 | **约定 ODS**，不是项目 DWD |

## 4. 禁止

- 把算法页面结论回写 DWD 形成双轨（见 v5 §2.5）  
- CMS「产业介绍/发展历程」长文双写 DWD  
- 细表标 `approved`（须单独结构评审）
