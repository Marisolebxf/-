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
as_built_source: data-design/产业链/产业链-ADS表设计-原型与Handoff驱动(v2).md
---
```

> **必须文档**。Java 业务 API **只读**本层；**禁止** Java 写 ADS / 扫 DWD。  
> **DDL / 字段真源**：[`产业链-ADS表设计-原型与Handoff驱动(v2).md`](../../../../产业链/产业链-ADS表设计-原型与Handoff驱动(v2).md)（**勿在本文件粘贴全 DDL**）。  
> **库名**：正式 `gkxlumenx_ads`；Demo `demo_gkxlumenx_ads`。  
> **对齐**：DWD v5；指标 `M_CHAIN_*` ← `cfg_metric-CHAIN-seed.yaml`；全景发布态对齐 DEC-CHAIN-PANORAMA-STATUS-COMPARE。  
> **对照（非真源）**：[`产业链-ADS表设计-业务需求驱动(v1).md`](../../../../产业链/产业链-ADS表设计-业务需求驱动(v1).md)（8 表旧稿）。  
> **废止当真源**：`DATA-CHAIN-db-design.md` 旧十一张 `chain_*`。

## 1. 写读矩阵

| 写 | 读 |
|---|---|
| Python / 指标引擎 / 发布作业 / 模型后处理；Demo 见 [`../../etl/pipeline-demo-mock.md`](../../etl/pipeline-demo-mock.md) | **Java 只读**；前端不直连 |

**边界（v2）**：七键「生成分析」正式结果包 → Analysis Job Snapshot（**禁止**与全景 `graph_snapshot` 混表）；产业介绍 / 发展历程 → CMS；在线图谱遍历 → Nebula。  
**行业分析正文不并入**本文件 v2 十表。企业图谱抽边读 **DWD** [`industry_analysis_documents`](./dwd-industry-analysis.md)（及关联五表），不是 Java ADS。

## 2. 表清单（v2 · 10 张物理表）

| # | 表（`gkxlumenx_ads`） | 用途 |
|---|---|---|
| 1 | `industry_chain_metric_fact` | 指标快照（卡片 KPI / 排名 / 占比 / 枚举阶段） |
| 2 | `industry_chain_metric_series` | 指标时序（趋势图） |
| 3 | `industry_chain_metric_dist` | 分布型指标（类型占比、分档计数） |
| 4 | `industry_chain_region_dist` | 区域分布行（地图/列表） |
| 5 | `industry_chain_region_scorecard` | 区域评价 / 四力矩阵行 |
| 6 | `industry_chain_topn` | TopN 列表行 |
| 7 | `industry_chain_conclusion` | 产品化结论头 |
| 8 | `industry_chain_narrative` | 长文本解释（非 CMS） |
| 9 | `industry_chain_graph_snapshot` | 全景**发布**快照 |
| 10 | `industry_chain_graph_diff` | 演进 / 状态对比 diff |

相对 v1 增量：`metric_dist`、`region_dist`；强化 `graph_snapshot` / `graph_diff`（`publish_status` 等）。

字段、唯一键、`M_CHAIN_*` 映射、开放项 → **真源文档 §3–§9**。

## 3. 与 DWD / CMS / Nebula / Job

| 层 | 关系 |
|---|---|
| DWD | 明细与原子模型结果；ADS 经 `run_id`/`result_id` 回链 |
| CMS | 产业介绍 / 发展历程 **不进** ADS narrative |
| Nebula | 在线图谱查询；历史对比走 ADS 发布快照 |
| Job Snapshot | 七键正式结果权威；可投影进 conclusion/scorecard（规则见 OPEN-CHAIN-ADS-V2-05） |

## 4. 禁止

- 沿用或平行维护旧 `chain_overview` 等十一表作正式契约  
- 以 v1 八表稿覆盖本文件真源指针  
- 前端/Java 写 ADS  
- 细表仅因流图会签标 `approved`  
- 把 DWD 明细表伪装成 ADS  
- Job Result 与全景发布快照混表  
