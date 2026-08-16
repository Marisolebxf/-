# MySQL DWD · 行业分析标准明细（CHAIN 切片）

```yaml
---
doc_id: CHAIN-STORE-DWD-INDANA
element: CHAIN
role: store-mysql
status: draft
version: "2026-08-16"
updated: "2026-08-16"
engine: mysql
task: DATA-CHAIN-INDANA-STORAGE-L01
as_built_source: storage/CHAIN/etl/gkx_industry_analysis_show_create.sql
---
```

> **落点**：`storage/CHAIN`（与产业链同 workbook 的「行业分析」切片）。**禁止**写入 `storage/ENT` / `dwd-entity`。  
> **库**：正式 `gkxlumenx_dwd`；Demo `demo_gkxlumenx_dwd`（口误 `gkxlumnex` 一律纠正为此名）。  
> **结构**：复制入站现表 `dwd_industry_analysis_*`（列名/类型/主键/索引语义）；**仅改表名去 `dwd_`** → `industry_analysis_*`。禁止改成素表 `documents` / `companies` 等。  
> **DDL 快照**：[`../../etl/gkx_industry_analysis_show_create.sql`](../../etl/gkx_industry_analysis_show_create.sql)（三方 `gkx` live）→ 去前缀稿 [`../../etl/demo_gkxlumenx_dwd_industry_analysis_show_create.sql`](../../etl/demo_gkxlumenx_dwd_industry_analysis_show_create.sql)。**本叶不对 `gkxlumenx_dwd` APPLY。**  
> **细表保持 `draft`**。`01-data-flow.md` 主图仍为 `human:李伟` 已会签 approved，本切片未翻签。

## 1. 写读

| 写 | 读 |
|---|---|
| 模拟 GDF / ETL（入站 `dwd_industry_analysis_*` → 本层 `industry_analysis_*`） | **Python / 算法**（企业图谱抽边读正文表及关联五表）；**Java 不扫 DWD** |

图谱抽边后续叶（`ENT-YIJI-INFER-LLM`）读 **DWD `industry_analysis_documents`**（及五张关联表），**不是** Java ADS。本叶不写推理代码。

## 2. 六表清单（一张不漏）

| # | 项目 DWD | 入站现表（Demo/供应方） | 中文 | 一行语义 |
|---|---|---|---|---|
| 1 | `industry_analysis_documents` | `dwd_industry_analysis_documents` | 文档信息 | 研报/资讯正文与元数据；业务键 `document_id` |
| 2 | `industry_analysis_companies` | `dwd_industry_analysis_companies` | 文档关联公司 | 文档 ↔ 公司 |
| 3 | `industry_analysis_industries` | `dwd_industry_analysis_industries` | 文档关联行业 | 文档 ↔ 行业 |
| 4 | `industry_analysis_topics` | `dwd_industry_analysis_topics` | 文档关联主题 | 文档 ↔ 主题 |
| 5 | `industry_analysis_content_types` | `dwd_industry_analysis_content_types` | 文档内容类型 | 文档 ↔ 报告类型 |
| 6 | `industry_analysis_countries` | `dwd_industry_analysis_countries` | 文档关联国家 | 文档 ↔ 国家 |

物理主键现表均为 `pk_id`；`document_id` 在主表 UNIQUE，在五从表与业务码组成 UNIQUE。取数 `is_deleted=0`。

字段级摘要见 [`../../sources/inventory-industry-analysis.md`](../../sources/inventory-industry-analysis.md)。

## 3. 与产业链 DWD / ADS 的边界

| 对象 | 关系 |
|---|---|
| [`dwd-chain.md`](./dwd-chain.md) v5 `industry_chain_*` 十四表 | **并列切片**，不互相冒充 |
| CHAIN ADS v2 十表 | 行业分析**正文不并入** ADS v2；见 [`ads.md`](./ads.md) 指针 |
| `dwd_industry_chain_news_info` | **禁止**冒充文档表 |
| ENT `dwd-entity` `enterprise_*` | **禁止**把本六表塞进企业工商店面 |

## 4. 禁止

- 第二套 schema / `storage/CHAIN-demo` 平行树  
- 把要素库英表 `documents` 当项目 DWD 物理名  
- 用 `gkx-mysql-raw` as-built 压过现表 DDL 改列名  
- 细表标 `approved`（须 `human:李伟` 会签增量）  
- 本叶对正式 `gkxlumenx_dwd` `CREATE`/`ALTER`  
- 本叶改 `demo-algo-ent-analysis` 推理代码 / 启动图边 LLM / 建 `ods_news_event`
