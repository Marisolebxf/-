# DR-RES-A0 列矩阵

复核日 2026-11-03。来源：久新 Doris `gkx_technology_analysis_dev` 现网 `SHOW FULL COLUMNS`。账号 `test2` 只读。密码不在本文。

实体存量不写进页面「资源总量」和年度接入。

`SHOW COLUMNS` 不写进 `themeDatabases.tableSchemas`。

`entityStock` 只用方案点名的四个年份列做按年存量。这四列同时也在 `SHOW COLUMNS` 结果里，所以落到写 `entityStock；columnCatalog`。其余列只进 `columnCatalog`。

旁边这些年份列现网有，但方案没有拿来做 `entityStock`，本矩阵不改口径：专利 `grant_year`；项目 `end_year`、`observed_start_year`、`effective_start_year`。`start_year_source`、`start_year_is_inferred` 也不是按年存量列。

## 年份列（entityStock）

与方案第 2 节一致。没有旧名换成新名。

| 表名 | 列名 | 类型 | 可空 | 现网序号 | 2026-10-22 序号 | 是否仍在 | 落到 |
|---|---|---|---|---:|---:|---|---|
| `ads_paper_profile` | `publication_year` | `smallint` | NO | 12 | 9 | 是 | entityStock；columnCatalog |
| `ads_patent_profile` | `application_year` | `smallint` | YES | 22 | 22 | 是 | entityStock；columnCatalog |
| `ads_patent_profile` | `publication_year` | `smallint` | NO | 23 | 23 | 是 | entityStock；columnCatalog |
| `ads_project_profile` | `start_year` | `smallint` | YES | 29 | 22 | 是 | entityStock；columnCatalog |

序号变化是因为前面插入了新列，列名没变。论文在 `publication_year` 前多了 3 个摘要列。项目在 `start_year` 前多了 7 个 `amount_cny*` 列。

## columnCatalog

三张表 `SHOW FULL COLUMNS` 全列，共 131。2026-10-22 字段清单里的列名全部仍在，没有改名、没有消失。标「现网新增」的 10 列是清单之后多出来的，同样只进 `columnCatalog`。

### ads_paper_profile（38 列）

| 表名 | 序号 | 列名 | 类型 | 可空 | 是否仍在 | 落到 |
|---|---:|---|---|---|---|---|
| `ads_paper_profile` | 1 | `paper_id` | `varchar(64)` | NO | 是 | columnCatalog |
| `ads_paper_profile` | 2 | `openalex_work_id` | `varchar(64)` | NO | 是 | columnCatalog |
| `ads_paper_profile` | 3 | `doi` | `varchar(512)` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 4 | `title` | `text` | NO | 是 | columnCatalog |
| `ads_paper_profile` | 5 | `title_zh` | `text` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 6 | `title_en` | `text` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 7 | `title_original` | `text` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 8 | `abstract_zh` | `text` | YES | 是（现网新增） | columnCatalog |
| `ads_paper_profile` | 9 | `abstract_en` | `text` | YES | 是（现网新增） | columnCatalog |
| `ads_paper_profile` | 10 | `abstract_original` | `text` | YES | 是（现网新增） | columnCatalog |
| `ads_paper_profile` | 11 | `publication_date` | `date` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 12 | `publication_year` | `smallint` | NO | 是 | entityStock；columnCatalog |
| `ads_paper_profile` | 13 | `paper_type` | `varchar(64)` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 14 | `language` | `varchar(32)` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 15 | `primary_topic_id` | `varchar(64)` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 16 | `openalex_primary_topic_id` | `varchar(64)` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 17 | `topic_ids` | `array<varchar(64)>` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 18 | `primary_source_id` | `varchar(64)` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 19 | `cited_by_count` | `bigint` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 20 | `fwci` | `decimal(14,6)` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 21 | `author_count` | `bigint` | NO | 是 | columnCatalog |
| `ads_paper_profile` | 22 | `institution_count` | `bigint` | NO | 是 | columnCatalog |
| `ads_paper_profile` | 23 | `is_open_access` | `tinyint` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 24 | `open_access_status` | `varchar(32)` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 25 | `open_access_url` | `text` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 26 | `landing_page_url` | `text` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 27 | `pdf_url` | `text` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 28 | `is_retracted` | `tinyint` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 29 | `is_paratext` | `tinyint` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 30 | `volume` | `varchar(128)` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 31 | `issue` | `varchar(128)` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 32 | `first_page` | `varchar(128)` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 33 | `last_page` | `varchar(128)` | YES | 是 | columnCatalog |
| `ads_paper_profile` | 34 | `data_sources` | `array<text>` | NO | 是 | columnCatalog |
| `ads_paper_profile` | 35 | `metrics_as_of_date` | `date` | NO | 是 | columnCatalog |
| `ads_paper_profile` | 36 | `metric_definition_version` | `varchar(64)` | NO | 是 | columnCatalog |
| `ads_paper_profile` | 37 | `data_version` | `bigint` | NO | 是 | columnCatalog |
| `ads_paper_profile` | 38 | `update_time` | `datetime(3)` | NO | 是 | columnCatalog |

### ads_patent_profile（45 列）

| 表名 | 序号 | 列名 | 类型 | 可空 | 是否仍在 | 落到 |
|---|---:|---|---|---|---|---|
| `ads_patent_profile` | 1 | `patent_id` | `varchar(64)` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 2 | `google_patent_publication_id` | `varchar(128)` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 3 | `publication_number` | `varchar(128)` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 4 | `application_number` | `varchar(128)` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 5 | `pct_number` | `varchar(128)` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 6 | `jurisdiction_code` | `varchar(16)` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 7 | `kind_code` | `varchar(32)` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 8 | `application_kind` | `varchar(64)` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 9 | `family_id` | `varchar(128)` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 10 | `title` | `text` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 11 | `title_zh` | `text` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 12 | `title_en` | `text` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 13 | `title_original` | `text` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 14 | `abstract_zh` | `text` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 15 | `abstract_en` | `text` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 16 | `abstract_original` | `text` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 17 | `language` | `varchar(32)` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 18 | `priority_date` | `date` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 19 | `filing_date` | `date` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 20 | `publication_date` | `date` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 21 | `grant_date` | `date` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 22 | `application_year` | `smallint` | YES | 是 | entityStock；columnCatalog |
| `ads_patent_profile` | 23 | `publication_year` | `smallint` | NO | 是 | entityStock；columnCatalog |
| `ads_patent_profile` | 24 | `grant_year` | `smallint` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 25 | `is_granted` | `tinyint` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 26 | `inventors` | `variant` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 27 | `inventor_count` | `int` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 28 | `assignees` | `variant` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 29 | `assignee_count` | `int` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 30 | `ipc_codes` | `array<text>` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 31 | `cpc_codes` | `array<text>` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 32 | `primary_ipc_code` | `varchar(64)` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 33 | `primary_cpc_code` | `varchar(64)` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 34 | `ipc_classifications` | `variant` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 35 | `cpc_classifications` | `variant` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 36 | `linked_talent_count` | `bigint` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 37 | `linked_institution_count` | `bigint` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 38 | `cited_paper_count` | `bigint` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 39 | `source_dataset` | `varchar(128)` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 40 | `source_batch` | `varchar(128)` | YES | 是 | columnCatalog |
| `ads_patent_profile` | 41 | `data_sources` | `array<text>` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 42 | `metrics_as_of_date` | `date` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 43 | `metric_definition_version` | `varchar(64)` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 44 | `data_version` | `bigint` | NO | 是 | columnCatalog |
| `ads_patent_profile` | 45 | `update_time` | `datetime(3)` | NO | 是 | columnCatalog |

### ads_project_profile（48 列）

| 表名 | 序号 | 列名 | 类型 | 可空 | 是否仍在 | 落到 |
|---|---:|---|---|---|---|---|
| `ads_project_profile` | 1 | `project_id` | `varchar(64)` | NO | 是 | columnCatalog |
| `ads_project_profile` | 2 | `openalex_grant_id` | `varchar(64)` | YES | 是 | columnCatalog |
| `ads_project_profile` | 3 | `name` | `text` | NO | 是 | columnCatalog |
| `ads_project_profile` | 4 | `name_zh` | `text` | YES | 是 | columnCatalog |
| `ads_project_profile` | 5 | `name_en` | `text` | YES | 是 | columnCatalog |
| `ads_project_profile` | 6 | `name_original` | `text` | YES | 是 | columnCatalog |
| `ads_project_profile` | 7 | `description` | `text` | YES | 是 | columnCatalog |
| `ads_project_profile` | 8 | `description_zh` | `text` | YES | 是 | columnCatalog |
| `ads_project_profile` | 9 | `description_en` | `text` | YES | 是 | columnCatalog |
| `ads_project_profile` | 10 | `openalex_funder_id` | `varchar(64)` | YES | 是 | columnCatalog |
| `ads_project_profile` | 11 | `funder_name` | `text` | YES | 是 | columnCatalog |
| `ads_project_profile` | 12 | `funder_ror` | `varchar(64)` | YES | 是 | columnCatalog |
| `ads_project_profile` | 13 | `funder_doi` | `varchar(256)` | YES | 是 | columnCatalog |
| `ads_project_profile` | 14 | `funder_project_id` | `text` | YES | 是 | columnCatalog |
| `ads_project_profile` | 15 | `amount` | `decimal(24,4)` | YES | 是 | columnCatalog |
| `ads_project_profile` | 16 | `currency` | `varchar(8)` | YES | 是 | columnCatalog |
| `ads_project_profile` | 17 | `amount_cny` | `decimal(24,4)` | YES | 是（现网新增） | columnCatalog |
| `ads_project_profile` | 18 | `amount_cny_exchange_rate` | `decimal(18,8)` | YES | 是（现网新增） | columnCatalog |
| `ads_project_profile` | 19 | `amount_cny_exchange_rate_date` | `date` | YES | 是（现网新增） | columnCatalog |
| `ads_project_profile` | 20 | `amount_cny_exchange_rate_source` | `varchar(64)` | YES | 是（现网新增） | columnCatalog |
| `ads_project_profile` | 21 | `amount_cny_normalization_status` | `varchar(40)` | YES | 是（现网新增） | columnCatalog |
| `ads_project_profile` | 22 | `amount_cny_conversion_policy` | `varchar(64)` | YES | 是（现网新增） | columnCatalog |
| `ads_project_profile` | 23 | `amount_cny_value_type` | `varchar(48)` | NO | 是（现网新增） | columnCatalog |
| `ads_project_profile` | 24 | `funding_type` | `varchar(128)` | YES | 是 | columnCatalog |
| `ads_project_profile` | 25 | `funder_scheme` | `varchar(256)` | YES | 是 | columnCatalog |
| `ads_project_profile` | 26 | `provenance` | `varchar(128)` | YES | 是 | columnCatalog |
| `ads_project_profile` | 27 | `start_date` | `date` | YES | 是 | columnCatalog |
| `ads_project_profile` | 28 | `end_date` | `date` | YES | 是 | columnCatalog |
| `ads_project_profile` | 29 | `start_year` | `smallint` | YES | 是 | entityStock；columnCatalog |
| `ads_project_profile` | 30 | `end_year` | `smallint` | YES | 是 | columnCatalog |
| `ads_project_profile` | 31 | `observed_start_year` | `smallint` | YES | 是 | columnCatalog |
| `ads_project_profile` | 32 | `effective_start_year` | `smallint` | YES | 是 | columnCatalog |
| `ads_project_profile` | 33 | `start_year_source` | `varchar(64)` | YES | 是 | columnCatalog |
| `ads_project_profile` | 34 | `start_year_is_inferred` | `boolean` | NO | 是 | columnCatalog |
| `ads_project_profile` | 35 | `doi` | `varchar(512)` | YES | 是 | columnCatalog |
| `ads_project_profile` | 36 | `landing_page_url` | `text` | YES | 是 | columnCatalog |
| `ads_project_profile` | 37 | `funded_paper_count` | `bigint` | NO | 是 | columnCatalog |
| `ads_project_profile` | 38 | `institution_count` | `bigint` | NO | 是 | columnCatalog |
| `ads_project_profile` | 39 | `talent_count` | `bigint` | NO | 是 | columnCatalog |
| `ads_project_profile` | 40 | `topic_count` | `bigint` | NO | 是 | columnCatalog |
| `ads_project_profile` | 41 | `primary_topic_id` | `varchar(64)` | YES | 是 | columnCatalog |
| `ads_project_profile` | 42 | `topic_ids` | `array<varchar(64)>` | YES | 是 | columnCatalog |
| `ads_project_profile` | 43 | `data_sources` | `array<text>` | YES | 是 | columnCatalog |
| `ads_project_profile` | 44 | `is_active` | `boolean` | NO | 是 | columnCatalog |
| `ads_project_profile` | 45 | `metrics_as_of_date` | `date` | YES | 是 | columnCatalog |
| `ads_project_profile` | 46 | `metric_definition_version` | `varchar(64)` | YES | 是 | columnCatalog |
| `ads_project_profile` | 47 | `data_version` | `bigint` | NO | 是 | columnCatalog |
| `ads_project_profile` | 48 | `update_time` | `datetime(3)` | NO | 是 | columnCatalog |
