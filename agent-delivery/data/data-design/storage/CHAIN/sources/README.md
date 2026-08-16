# CHAIN · 第三方 / ODS 入站

同 workbook「市场研究（金融、宏观行业、行业分析、产业链）数据汇总表」拆两张清单，**禁止糊成一张无分层表**：

| 切片 | 文档 | Sheet |
|---|---|---|
| 产业链要素库（四表） | [`inventory.md`](./inventory.md) | 产业链要素库 |
| 行业分析要素库（六表） | [`inventory-industry-analysis.md`](./inventory-industry-analysis.md) | 行业分析要素库 |

在线约定 vs 三方真实**产业链**四表差异（S2 副产品）：[`md-extract-vs-live-ods-diff.md`](./md-extract-vs-live-ods-diff.md)。  
行业分析入站现表 live `SHOW CREATE`：[`../etl/gkx_industry_analysis_show_create.sql`](../etl/gkx_industry_analysis_show_create.sql)（`DATA-CHAIN-INDANA-STORAGE-L01`）。

## 结构真源（勿混淆）

| 用途 | 路径 | 地位 |
|---|---|---|
| **三方 ODS 权威唯一真源** | `agent-delivery/data/third-party-source/doc/`（xlsx） | 权威裁决；Demo 建表 / Mapping **一律对齐** |
| **优先读取面** | `…/doc/md-extract/` | **自 Excel 抽取**；默认先读这里（含「产业链要素库」） |
| 现网探测 / 对账 | `third-party-source/gkx-mysql-raw/`（`gkx` 四同名表） | **禁止**作 ODS 建表真源；差异见上 |
