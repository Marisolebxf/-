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
---
```

> **必须文档**。Java 业务 API **只读**本层；**禁止** Java 写 ADS / 扫 DWD。  
> **库名**：正式 `gkxlumenx_ads`；Demo `demo_gkxlumenx_ads`。  
> **status=draft**。细 DDL 外链；本文件列契约表清单。  
> 指标 8 件套真源：`metrics/cfg_metric-CHAIN-seed.yaml`（本文件不替代 D9）。

## 1. 写读矩阵

| 写 | 读 |
|---|---|
| Python / 工厂；Demo：模拟 GDF 或旁路（[`../../etl/pipeline-mock-to-ads.md`](../../etl/pipeline-mock-to-ads.md)） | **Java 只读**；前端不直连 |

## 2. 规划表清单（as-built 设计指针）

> 表名沿用 [`DATA-CHAIN-db-design.md`](../../../../../agent-handoffs/产业链分析-CHAIN/DATA-CHAIN-db-design.md) §5 的 `chain_*` 契约面（历史 PG 方言）；**现网落地须 MySQL 化**，列名核验见开放项。  
> v5 §2.2：市场规模默认 = 链下企业年报营收加总 → ADS（`M_CHAIN_MARKET_SIZE`），**不**进 DWD `market_observation`。

| 表（目标 `gkxlumenx_ads`） | 用途摘要 | 指针 |
|---|---|---|
| `chain_overview` | 概览 KPI（企业数/机构数等） | DATA-CHAIN-db-design §5.1 |
| `chain_panorama` | 全景节点/边计数与 G6 快照字段 | 同上；图真源仍 Nebula/DWD 关系表 |
| `chain_cycle` | 周期阶段 | 同上 |
| `chain_region_index` | 区域指数 | 同上 |
| `chain_key_node` | 关键节点汇总 | 同上 |
| `chain_bottleneck` | 瓶颈汇总 | 同上；诊断细粒度见 DWD model_result |
| `chain_shenzhen` | 深圳切片完备度等 | 同上 |
| `chain_market` | 市场规模/增速（平台默认口径） | v5 §2.2 + db-design |
| `chain_investment` | 投融资汇总 | 同上 |
| `chain_news_stat` | 资讯统计 | 同上 |
| `chain_competitiveness` | 竞争力指数 | 同上 |

图谱结构快照 / 演进 diff 查询面：按 v5 落 ADS（`snapshot_id` + 引用）；**永久边真源**仍为 DWD 三张 `*_rel`，禁止 ADS 另建永久边库。

## 3. 与 DWD 关系

- 明细与关系在 [`dwd-chain.md`](./dwd-chain.md)。  
- ADS **不**复制三方 ODS 字段进契约面。  
- 页面结论 / TopN / 自然语言建议进 ADS 或业务库，须可回链 `run_id` / `calc_batch_id`（v5 §2.5）。

## 4. 禁止

- 前端/Java 造假写 ADS  
- `demo_ads_*` 第二套契约结构  
- 把 DWD 明细表伪装成对外 ADS  
- 细表标 `approved`（须单独评审）
