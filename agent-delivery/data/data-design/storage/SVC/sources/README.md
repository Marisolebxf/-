# SVC · 第三方 / ODS 入站

> 表级清单：[`inventory.md`](./inventory.md)（**S2** `DATA-SVC-STORAGE-S2-L01` · 2026-08-14）。  
> 流图：[`../01-data-flow.md`](../01-data-flow.md) · 上下文：[`../00-context.md`](../00-context.md)

## 结构真源（勿混淆）

| 用途 | 路径 | 地位 |
|---|---|---|
| **三方 ODS 权威唯一真源** | `agent-delivery/data/third-party-source/doc/`（xlsx） | 权威裁决；Demo 建表 / Mapping **一律对齐** |
| **优先读取面** | `…/doc/md-extract/` | **自 Excel 抽取**；默认先读这里 |
| 本域优先 Sheet | `版权人才、企业机构、政策数据汇总表` · **国内机构要素库** | 日常 CSV：`doc/md-extract/_csv/版权人才、企业机构、政策数据汇总表__国内机构要素库.csv` |
| 现网探测 / 对账 | `third-party-source/gkx-mysql-raw/`（含 L01 实查备忘） | **禁止**作 ODS 建表真源 |

## 与 ENT 边界

- 机构主表 `dwd_org_base_info` 等 **ENT 已按同一文档**列入 `storage/ENT/sources/inventory.md`。  
- SVC **不**另建一套主表；S2 在 `demo_gkxlumenx_ods` **复用并对列**（含文档承诺的 `industry*`，见 OPEN-SVC-FLOW-08 / Q-SVC-009）。  
- 本域增量清单（圈定结果、关系）属项目 DWD，不是第三套机构 ODS。

Demo 灌数主路径：[`../etl/pipeline-demo-mock.md`](../etl/pipeline-demo-mock.md)。
