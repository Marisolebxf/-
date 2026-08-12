# ENT · 第三方 / ODS 入站

企业维依赖的供应表清单见 [`inventory.md`](./inventory.md)（**S2 已初填**）。

## 结构真源（两层，勿混淆）

| 用途 | 真源 | 说明 |
|---|---|---|
| **Demo / 约定口径（优先）** | `agent-delivery/data/third-party-source/doc/` + `md-extract/` | LLM Mock 建 ODS、内部全链路以此为准 |
| 现网探测 / 对账 | `third-party-source/gkx-mysql-raw/` | 供应进度与差异；**不得**单独作为 Demo ODS 建表真源 |

连接与凭证：见 `third-party-source/`（勿复制密码）。  
Demo 灌数主路径：[`../etl/pipeline-demo-mock.md`](../etl/pipeline-demo-mock.md)。  
GDF Wave A 枚举：`data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/02-WaveA-贴源表清单.yaml`。
