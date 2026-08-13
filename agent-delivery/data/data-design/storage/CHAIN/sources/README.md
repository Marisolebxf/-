# CHAIN · 第三方 / ODS 入站

产业链依赖的供应表清单见 [`inventory.md`](./inventory.md)（S1 已钉真源与四表名；**S2 充实字段级说明**）。

## 结构真源（勿混淆）

| 用途 | 路径 | 地位 |
|---|---|---|
| **三方 ODS 权威唯一真源** | `agent-delivery/data/third-party-source/doc/`（xlsx） | 权威裁决；Demo 建表 / Mapping **一律对齐** |
| **优先读取面** | `…/doc/md-extract/` | **自 Excel 抽取**；默认先读这里（含「产业链要素库」） |
| 现网探测 / 对账 | `third-party-source/gkx-mysql-raw/` | **禁止**作 ODS 建表真源 |

Demo 灌数主路径：[`../etl/pipeline-demo-mock.md`](../etl/pipeline-demo-mock.md)。
