# CHAIN · 行业分析要素库清单（入站六表切片）

```yaml
---
doc_id: CHAIN-SOURCE-INVENTORY-INDANA
element: CHAIN
role: source
status: draft
version: "2026-08-16"
updated: 2026-08-16
task: DATA-CHAIN-INDANA-STORAGE-L01
---
```

> **切片**：与 [`inventory.md`](./inventory.md)（产业链四表）**同 workbook、不同 sheet**，禁止糊成一张无分层总表。  
> **真源分层**：权威 xlsx `third-party-source/doc/`；日常读 `doc/md-extract/`「行业分析要素库」。  
> **物理列**：以 Demo 现表 DDL 为准；Demo 未建前暂以三方 `gkx` live `SHOW CREATE`（[`../etl/gkx_industry_analysis_show_create.sql`](../etl/gkx_industry_analysis_show_create.sql)）。冲突时 **现表 DDL 赢**，CSV 只核漏列。  
> **资讯使用（2026-08-25）**：本六表 **可用**，作为行业/产业资讯与分析文档原料。  
> **禁止**：以 `gkx-mysql-raw` 沙箱旧稿改名；用 `dwd_industry_chain_news_info` 冒充文档表（该表合规交付、无实用价值）；把六表写入 `storage/ENT` / `dwd-entity`；默认写正式 `gkxlumenx_ods` / `gkxlumenx_dwd`。  
> 库名口误：文档一律写 `demo_gkxlumenx_dwd`（不是 `demo_gkxlumnex_dwd`）。

## 0. 三层命名（一张不漏）

| # | 要素库英表（CSV / md-extract，**对照用**） | 中文 | 入站 / Demo 现表（带 `dwd_`） | 项目 DWD 物理表（**仅去前缀**） |
|---|---|---|---|---|
| 1 | `documents` | 文档信息 | `dwd_industry_analysis_documents` | `industry_analysis_documents` |
| 2 | `companies` | 文档关联公司 | `dwd_industry_analysis_companies` | `industry_analysis_companies` |
| 3 | `industries` | 文档关联行业 | `dwd_industry_analysis_industries` | `industry_analysis_industries` |
| 4 | `topics` | 文档关联主题 | `dwd_industry_analysis_topics` | `industry_analysis_topics` |
| 5 | `content_types` | 文档内容类型 | `dwd_industry_analysis_content_types` | `industry_analysis_content_types` |
| 6 | `countries` | 文档关联国家 | `dwd_industry_analysis_countries` | `industry_analysis_countries` |

- CSV 英表 `documents` / `companies` / … **不是**项目 DWD 物理表名，也禁止改成素表名直接落库。  
- 入站角色 = 供应方 `dwd_*`（三方库 `gkx` 已存在这六张）。  
- 项目自建 DWD = 复制现表结构，**只改表名去 `dwd_`**。  
- 关联键：五张从表均以 `document_id` 挂主表；取数默认 `is_deleted=0`。

## 1. 现表落点（2026-08-16 抽检）

| 实例 | 六表 `dwd_industry_analysis_*` |
|---|---|
| 三方入站 `gkx` @ `183.240.141.251:3318` | **存在**（`SHOW CREATE` 已快照） |
| Demo `demo_gkxlumenx_dwd` @ `192.168.88.43:3306` | **不存在**（OPEN-CHAIN-INDANA-01） |
| 正式 `gkxlumenx_dwd` | **禁止本叶 CREATE/ALTER** |

CSV：`doc/md-extract/_csv/市场研究（金融、宏观行业、行业分析、产业链）数据汇总表__行业分析要素库.csv`

## 2. 字段摘要（物理列 = 现表；旁注 = CSV 中文）

生成器未建；列来自 `gkx` live。CSV 业务列**全部能对上**，无漏业务列。现表多出的技术列标「CSV 无」。

### `dwd_industry_analysis_documents` → 项目 `industry_analysis_documents`

| 现表列 | MySQL | 键 | CSV 中文 / 备注 |
|---|---|---|---|
| pk_id | BIGINT NOT NULL AUTO_INCREMENT | PRI | CSV 无（现表物理主键） |
| document_id | VARCHAR(100) NOT NULL | UNI `uk_document_id` | 文件ID（CSV 标主键） |
| format | VARCHAR(32) NOT NULL | | 文件格式 |
| update_date | VARCHAR(50) | | 更新日期 |
| creation_date | VARCHAR(50) NOT NULL | MUL | 文件日期 |
| source_type_name | VARCHAR(200) | | 源类型名字 |
| source_type_code | VARCHAR(8) | | 源类型代码 |
| source_code | VARCHAR(24) NOT NULL | MUL | 数据源代码 |
| source_name | VARCHAR(500) NOT NULL | | 数据源名字 |
| pages | INT | | 页数 |
| size | BIGINT NOT NULL | | 文件字节大小 |
| title | VARCHAR(1000) NOT NULL | | 标题 |
| body | MEDIUMTEXT | | 正文 |
| abstract | TEXT | | 文件摘要 |
| language | VARCHAR(50) NOT NULL | MUL | 语言（CSV 长度 2；现表 50 **现表赢**） |
| file_link | VARCHAR(1000) | | 文件链接 |
| created_time | DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP | | CSV 无 · 供应方技术字段 |
| updated_time | DATETIME | | CSV 无 |
| creater | VARCHAR(100) | | CSV 无 |
| updater | VARCHAR(100) | | CSV 无 |
| table_data_source | VARCHAR(100) | | CSV 无 |
| operator_remarks | VARCHAR(100) | | CSV 无 |
| is_deleted | SMALLINT NOT NULL DEFAULT 0 | | CSV 无 · 默认过滤 0 |
| insert_remark | SMALLINT NOT NULL DEFAULT 0 | | CSV 无 |

### `dwd_industry_analysis_companies` → 项目 `industry_analysis_companies`

| 现表列 | MySQL | 键 | CSV 中文 / 备注 |
|---|---|---|---|
| pk_id | BIGINT AI | PRI | CSV 无 |
| document_id | VARCHAR(100) NOT NULL | MUL + UK 组合 | 文件ID（CSV 标主键） |
| company_id | BIGINT | MUL + UK 组合 | 公司代码（CSV Integer；现表 bigint **现表赢**） |
| company_name | VARCHAR(500) | | 公司英文名称 |
| company_name_local | VARCHAR(500) | MUL | 公司本地名称 |
| （同主表 8 技术列） | | | CSV 无 |

UK：`uk_doc_company (document_id, company_id)`。

### `dwd_industry_analysis_industries` → 项目 `industry_analysis_industries`

| 现表列 | MySQL | 键 | CSV 中文 / 备注 |
|---|---|---|---|
| pk_id | BIGINT AI | PRI | CSV 无 |
| document_id | VARCHAR(100) NOT NULL | MUL + UK | 文件ID |
| industry_code | VARCHAR(50) | MUL + UK | 行业代码 |
| industry_name | VARCHAR(500) | MUL | 行业名称 |
| （8 技术列） | | | CSV 无 |

UK：`uk_doc_industry (document_id, industry_code)`。

### `dwd_industry_analysis_topics` → 项目 `industry_analysis_topics`

| 现表列 | MySQL | 键 | CSV 中文 / 备注 |
|---|---|---|---|
| pk_id | BIGINT AI | PRI | CSV 无 |
| document_id | VARCHAR(100) NOT NULL | MUL + UK | 文件ID |
| topic_name | VARCHAR(500) | MUL | 主题名字 |
| topic_code | VARCHAR(100) | UK 组合 | 主题代码 |
| （8 技术列） | | | CSV 无 |

UK：`uk_doc_topic (document_id, topic_code)`。

### `dwd_industry_analysis_content_types` → 项目 `industry_analysis_content_types`

| 现表列 | MySQL | 键 | CSV 中文 / 备注 |
|---|---|---|---|
| pk_id | BIGINT AI | PRI | CSV 无 |
| document_id | VARCHAR(100) NOT NULL | MUL + UK | 文件ID |
| name | VARCHAR(500) | MUL | 报告类型名字 |
| code | VARCHAR(8) | MUL + UK | 报告类型代码 |
| （8 技术列） | | | CSV 无 |

UK：`uk_doc_code (document_id, code)`。

### `dwd_industry_analysis_countries` → 项目 `industry_analysis_countries`

| 现表列 | MySQL | 键 | CSV 中文 / 备注 |
|---|---|---|---|
| pk_id | BIGINT AI | PRI | CSV 无 |
| document_id | VARCHAR(100) NOT NULL | MUL + UK | 文件ID |
| country_code | VARCHAR(50) | MUL + UK | 国家 |
| country_name | VARCHAR(200) | | 国家名字 |
| （8 技术列） | | | CSV 无 |

UK：`uk_doc_country (document_id, country_code)`。

## 3. 建表 / 快照产物

| 项 | 路径 |
|---|---|
| 三方 live `SHOW CREATE`（入站现表） | [`../etl/gkx_industry_analysis_show_create.sql`](../etl/gkx_industry_analysis_show_create.sql) |
| 项目 DWD 设计快照（去 `dwd_`，**未 APPLY**） | [`../etl/demo_gkxlumenx_dwd_industry_analysis_show_create.sql`](../etl/demo_gkxlumenx_dwd_industry_analysis_show_create.sql) |
| 店面 | [`../stores/mysql/dwd-industry-analysis.md`](../stores/mysql/dwd-industry-analysis.md) |

## 4. 开放项

| ID | 说明 | 状态 |
|---|---|---|
| OPEN-CHAIN-INDANA-01 | Demo `demo_gkxlumenx_dwd` 六张 `dwd_industry_analysis_*` 2026-08-16 抽检不存在；结构暂以 `gkx` live 复制；待 Demo 建表后补 Demo `SHOW CREATE` 并覆盖设计快照 | 开放 |
| OPEN-CHAIN-INDANA-02 | CSV 主键=业务 `document_id`；现表 PRI=`pk_id`。CSV 无 `pk_id` 与八技术列。**现表 DDL 赢** | 开放（已按现表收录，不改列） |
| OPEN-CHAIN-INDANA-03 | GDF 派单包现行仅 `派单包/企业/`，检索 `industry_analysis` / 六表无 Mapping 作业名，**禁止编造** | 开放 |
