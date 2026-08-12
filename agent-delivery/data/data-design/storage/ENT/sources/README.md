# ENT · 第三方 / ODS 入站

企业维依赖的供应表清单见 [`inventory.md`](./inventory.md)。

## 结构真源（两层，勿混淆）

| 用途 | 真源 | 说明 |
|---|---|---|
| **Demo / 约定口径（优先）** | 与三方约定的**在线文档**表结构 | LLM Mock 建 ODS、内部全链路以此为准；屏蔽现网三方进度导致的结构漂移 |
| 现网探测 / 对账 | `agent-delivery/data/third-party-source/` live 探测 | 用于供应进度、差异报告；**不得**单独作为 Demo ODS 建表真源 |

连接与凭证：见 `third-party-source/`（勿在本目录复制密码或全量 DDL）。  
Demo 灌数主路径：[`../etl/pipeline-demo-mock.md`](../etl/pipeline-demo-mock.md)。
