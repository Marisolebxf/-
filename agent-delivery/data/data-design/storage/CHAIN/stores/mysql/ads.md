# MySQL ADS · 产业链契约面

```yaml
---
doc_id: CHAIN-STORE-ADS
element: CHAIN
role: store-mysql
status: draft
version: "2026-08-13"
updated: "2026-08-13"
engine: mysql
s3_task: DATA-CHAIN-STORAGE-S3-L01
as_built_source: data-design/产业链/产业链-ADS表设计-业务需求驱动(v1).md
---
```

> **必须文档**。Java 业务 API **只读**本层；**禁止** Java 写 ADS / 扫 DWD。  
> **DDL / 字段真源**：[`产业链-ADS表设计-业务需求驱动(v1).md`](../../../../产业链/产业链-ADS表设计-业务需求驱动(v1).md)（**勿在本文件粘贴全 DDL**）。  
> **库名**：正式 `gkxlumenx_ads`；Demo `demo_gkxlumenx_ads`。  
> **对齐**：DWD v5 §2.2 / §2.5；指标 `M_CHAIN_*` ← `cfg_metric-CHAIN-seed.yaml`。  
> **废止当真源**：`DATA-CHAIN-db-design.md` 旧十一张 `chain_*`（仅对照，见 ADS v1 §0 / §6）。

## 1. 写读矩阵

| 写 | 读 |
|---|---|
| Python / 指标引擎 / 模型后处理；Demo 见 [`../../etl/pipeline-demo-mock.md`](../../etl/pipeline-demo-mock.md) | **Java 只读**；前端不直连 |

## 2. 表清单（v1 · 8 张）

| # | 表（`gkxlumenx_ads`） | 用途 |
|---|---|---|
| 1 | `industry_chain_metric_fact` | 指标快照（卡片 KPI / 排名 / 占比） |
| 2 | `industry_chain_metric_series` | 指标时序（趋势图） |
| 3 | `industry_chain_region_scorecard` | 区域对比 / 综合评价 |
| 4 | `industry_chain_topn` | TopN 列表 |
| 5 | `industry_chain_conclusion` | 产品化结论头 |
| 6 | `industry_chain_narrative` | 长文本解释 / 报告摘要 |
| 7 | `industry_chain_graph_snapshot` | 图谱结构快照元数据 |
| 8 | `industry_chain_graph_diff` | 演进 diff |

字段、唯一键、旧表映射、开放项 → **真源文档 §3–§8**。

## 3. 与 DWD / CMS / Nebula

| 层 | 关系 |
|---|---|
| DWD | 明细与原子模型结果；ADS 经 `run_id`/`result_id` 回链 |
| CMS | 产业介绍 / 发展历程 **不进** ADS narrative |
| Nebula | 在线图谱查询；ADS 快照非永久边真源 |

## 4. 禁止

- 沿用或平行维护旧 `chain_overview` 等十一表作正式契约  
- 前端/Java 写 ADS  
- 细表仅因流图会签标 `approved`  
- 把 DWD 明细表伪装成 ADS
