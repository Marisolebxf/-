# CHAIN · 第三方 / ODS 入站

产业链依赖的供应表清单见 [`inventory.md`](./inventory.md)。  
在线约定 vs 三方真实四表差异（S2 副产品）：[`md-extract-vs-live-ods-diff.md`](./md-extract-vs-live-ods-diff.md)。

## 结构真源（勿混淆）

| 用途 | 路径 | 地位 |
|---|---|---|
| **三方 ODS 权威唯一真源** | `agent-delivery/data/third-party-source/doc/`（xlsx） | 权威裁决；Demo 建表 / Mapping **一律对齐** |
| **优先读取面** | `…/doc/md-extract/` | **自 Excel 抽取**；默认先读这里（含「产业链要素库」） |
| 现网探测 / 对账 | `third-party-source/gkx-mysql-raw/`（`gkx` 四同名表） | **禁止**作 ODS 建表真源；差异见上 |
