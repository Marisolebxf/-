# 管道 · DWD → ADS（产业链）

> S2 指针 · 细表 **S3** 写入 `stores/mysql/ads.md`

## 意图

DWD 聚合/宽表写入 ADS，供 Java 只读。Demo 落 `demo_gkxlumenx_ads`。

## 指针

| 项 | 路径 |
|---|---|
| 流图 | [`../01-data-flow.md`](../01-data-flow.md) |
| stores | [`../stores/README.md`](../stores/README.md)（S3） |
| ENT 参考 | [`../../ENT/etl/pipeline-dwd-to-ads.md`](../../ENT/etl/pipeline-dwd-to-ads.md) |
| Demo 全量重算 | `${GKX_ROOT}/repos/demo-algo-science/chainan/llm_ods/ads_v2.py`（两种 mode 都 TRUNCATE ADS） |

append / replace 都按**当前 DWD**重算 `industry_chain_metric_fact` 等 v2 同步面。不写 CMS 历程/介绍（`narrative`/`conclusion` 空表）；不把市场规模灌进 `market_observation`；QC07 `INVEST_COUNT` 不造假。
