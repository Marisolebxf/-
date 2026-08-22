# calc-logic/ —— 口径计算逻辑 md（seed 的细稿）

seed yaml 只保留 8 件套摘要；完整口径（含子指标）在本目录 `{metric_id}.md`。

| 域 | 本目录 | 条数 | 说明 |
|----|--------|------|------|
| ENT | [`ENT/`](./ENT/) | 60 | 企业；2026-08-18 正式化 |
| CHAIN | [`CHAIN/`](./CHAIN/) | 63 | 产业链；2026-08-22 自 lumen-algo-py 汇总 |
| SVC | [`SVC/`](./SVC/) | 29 | 产业服务；2026-08-22 自 lumen-algo-py 汇总 |

入库过程件（指南 / 交接报告 / 批次 xlsx）在 [`../ingest/`](../ingest/)，不要和本目录混放。

新增域：建 `calc-logic/{域}/` + README 索引。Excel **活底稿**不进 git。
