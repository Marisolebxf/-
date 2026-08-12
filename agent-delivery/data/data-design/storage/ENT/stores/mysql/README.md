# ENT · MySQL 存储

| 文档 | 内容 | S3 状态 |
|---|---|---|
| [`dwd-entity.md`](./dwd-entity.md) | 工商/实体 DWD | draft · 已灌清单（真源工商 v3.1） |
| [`dwd-risk.md`](./dwd-risk.md) | 风险 DWD | draft · 已灌清单（真源模块 v3.0） |
| [`dwd-aggregate.md`](./dwd-aggregate.md) | 预聚合 / 指标汇总 | draft · 已灌清单（真源指标 v3.1 + v3.0 补充） |
| [`ads.md`](./ads.md) | **ADS 契约面（必须）** | draft · 已灌算法结果表清单 |
| [`dim.md`](./dim.md) | 码表 | draft · 初填 |

库名约定：正式 `gkxlumenx_dwd` / `gkxlumenx_ads`（及 cfg）；Demo 见 `etl/pipeline-demo-mock.md`。引擎：**MySQL 8 only**。  
**细表不得仅因流图会签标 approved**（`DATA-ENT-STORAGE-S3-L01`）。
