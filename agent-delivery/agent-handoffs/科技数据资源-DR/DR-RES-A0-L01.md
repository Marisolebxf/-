# DR-RES-A0-L01 · 久新现网列复核

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| 状态 | 已是 `in_progress`。本叶不改登记表，不标 `done` |

ponytail: off

## 范围

核对久新库 `gkx_technology_analysis_dev` 里方案第 2 节真查用的列，只覆盖这两块：

1. `entityStock`：`ads_paper_profile.publication_year`；`ads_patent_profile.application_year`、`ads_patent_profile.publication_year`；`ads_project_profile.start_year`。
2. `columnCatalog`：上述三张表 `SHOW FULL COLUMNS` 能拿到的全部列。

不建表、不灌数、不改方案、不改 WBS、不改总控、不改契约。

实体存量不写进页面「资源总量」和年度接入。`SHOW COLUMNS` 不写进 `themeDatabases.tableSchemas`。

## 证据

现网复核，不是只凭 2026-10-22 清单。

| 项 | 值 |
|---|---|
| 时间 | 2026-11-03 |
| 实例 | `47.93.119.170:29030`，`version_comment` = `doris version doris-4.1.0-rc03-5960d4cea0e` |
| 库 | `gkx_technology_analysis_dev` |
| 账号 | `test2`（只读）。密码未写入本文 |
| 语句 | `SELECT @@version_comment`；`SHOW FULL COLUMNS FROM ads_paper_profile`；`SHOW FULL COLUMNS FROM ads_patent_profile`；`SHOW FULL COLUMNS FROM ads_project_profile` |
| 对照 | `agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/字段清单.csv`（调研日 2026-10-22，schema 5.11.0） |

年份列与方案第 2 节一致，没有旧名换成新名：

| 表 | 方案列名 | 现网 | 类型 | 可空 | 现网序号 | 2026-10-22 序号 |
|---|---|---|---|---|---:|---:|
| `ads_paper_profile` | `publication_year` | 仍在 | `smallint` | NO | 12 | 9 |
| `ads_patent_profile` | `application_year` | 仍在 | `smallint` | YES | 22 | 22 |
| `ads_patent_profile` | `publication_year` | 仍在 | `smallint` | NO | 23 | 23 |
| `ads_project_profile` | `start_year` | 仍在 | `smallint` | YES | 29 | 22 |

全列：论文 38、专利 45、项目 48，合计 131。逐列在 `DR-RES-A0-矩阵.md`。

## 偏离

年份列无偏离。方案第 2 节四个列名可以照用。第 4 节我方表 `gapfill_dr_entity_year`、`gapfill_dr_column_catalog` 的列名也不用改。本叶没有改方案文件。

相对 2026-10-22 字段清单，现网没有消失的列，也没有改名。多了 10 列，只进 `columnCatalog`：

| 表 | 清单列数 | 现网列数 | 新增列名 |
|---|---:|---:|---|
| `ads_paper_profile` | 35 | 38 | `abstract_zh`、`abstract_en`、`abstract_original` |
| `ads_patent_profile` | 45 | 45 | 无 |
| `ads_project_profile` | 41 | 48 | `amount_cny`、`amount_cny_exchange_rate`、`amount_cny_exchange_rate_date`、`amount_cny_exchange_rate_source`、`amount_cny_normalization_status`、`amount_cny_conversion_policy`、`amount_cny_value_type` |

论文 `publication_year` 序号从 9 变成 12，项目 `start_year` 序号从 22 变成 29，都是前面插入新列，列名未变。后续 `columnCatalog` 按现网 131 列做快照，不要按清单的 35/45/41 截断。

现网还有方案没用的年份列，不拿来做 `entityStock`：专利 `grant_year`；项目 `end_year`、`observed_start_year`、`effective_start_year`。

## 架构合规

只读。对久新只执行了上面的 `SELECT` 和 `SHOW FULL COLUMNS`。没有写入久新，没有写入 ODS、DWD、ADS、`gkxlumenx_gapfill`，没有建表，没有灌数。

未 commit，未 push。

## 产物

- `agent-delivery/agent-handoffs/科技数据资源-DR/DR-RES-A0-L01.md`
- `agent-delivery/agent-handoffs/科技数据资源-DR/DR-RES-A0-矩阵.md`
