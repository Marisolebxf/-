# CHAIN · MySQL 存储

| 文档 | 内容 | S3 状态 |
|---|---|---|
| [`dwd-chain.md`](./dwd-chain.md) | 项目 DWD · v5 十四表 `industry_chain_*` | draft · 已灌清单 |
| [`ads.md`](./ads.md) | **ADS 契约面（必须）** · v1 八表（对齐 DWD v5） | draft · **已按 v5 重做设计** |
| [`dim.md`](./dim.md) | 码表 / 对照 | draft · 初填 |

库名约定：正式 `gkxlumenx_dwd` / `gkxlumenx_ads`；Demo 见 `etl/pipeline-demo-mock.md`。  
**细表不得仅因流图会签标 approved**（`DATA-CHAIN-STORAGE-S3-L01`）。  
**禁止**用供应方约定 ODS 四表（`dwd_industry_chain_*` 等）冒充本目录项目 DWD。
