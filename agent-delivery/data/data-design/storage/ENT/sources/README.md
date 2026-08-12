# ENT · 第三方 / ODS 入站

企业维依赖的供应表清单见 [`inventory.md`](./inventory.md)（**S2 已初填**）。

## 结构真源（勿混淆）

| 用途 | 路径 | 地位 |
|---|---|---|
| **三方 ODS 标准与唯一真源** | `agent-delivery/data/third-party-source/doc/`（xlsx） | 权威裁决；Demo Mock、正式贴源、Mapping **一律对齐** |
| **优先读取面** | `…/doc/md-extract/` | **自 Excel 抽取**；人 / agent / 程序 **默认先读这里** |
| GDF 施工枚举 | `data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/02-WaveA-贴源表清单.yaml` | **镜像 / 派单用**；漂移时回写对齐 `doc/`，不得反向覆盖 |
| 现网探测 / 对账 | `third-party-source/gkx-mysql-raw/` | 供应进度与差异；**禁止**作 ODS 建表真源 |

连接与凭证：见 `third-party-source/`（勿复制密码）。  
Demo 灌数主路径：[`../etl/pipeline-demo-mock.md`](../etl/pipeline-demo-mock.md)。
