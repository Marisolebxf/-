# POLICY-DDL-IMPACT-L02

- 任务：扫描政策 ADS 表的写入方式，收窄两库对齐的 ALTER 清单
- 状态：in_progress（本叶不改 task-registry）
- 执行：agent:data-agent
- 监管人：human:淮政玮
- 日期：2026-10-26
- ponytail: off（只读扫描叶，用户指定 off）
- 厚包：`agent-delivery/agent-handoffs/政策模块-E7/POLICY-DDL-ALIGN-长任务总控.md` 第 2 节

只读 `10.50.11.76:3306` 的 `demo_gkxlumenx_ads`、`demo_gkxlumenx_dwd`、`gkxlumenx_ads`、`gkxlumenx_dwd`。行数是 `COUNT(*)`。列数、排序规则来自 `information_schema`。未执行 ALTER，未改算法，未改 Java。口令未写入本文件。

## 结论

拟 ALTER **没有超出**总控第 2 节的表和动作。相对第 2 节只做了收窄：两个产线库的 `policy_industry_rel` 已满足排序规则和 `dwd.md` 注释，不安排语句。`policy_base_info` 不在本叶。

按位置写入（`INSERT` 不写列名）**未发现**。ALIGN 不因此停工，不升级 human:李伟。

## 拟 ALTER 清单

清单以外的语句 ALIGN 不得执行。列类型、索引集合、`AUTO_INCREMENT` 当前值都不改。新增字符列显式 `utf8mb4` / `utf8mb4_0900_ai_ci`，不把 demo 上的 `utf8mb4_unicode_ci` 抄到产线。列注释正文以 DOC 联调闸门后的 `ads.md` / `dwd.md` 为准，本叶不新写口径。

共有列在 `demo_gkxlumenx_ads` 与 `gkxlumenx_ads` 之间，类型、空值、默认值、`EXTRA` 没有差异。唯一索引只有 `PRIMARY(id)`，`CONVERT` 不会撞字符列唯一键。

### 1. demo ADS 15 张：CONVERT + 列注释

库 `demo_gkxlumenx_ads`。表级与全部字符列现为 `utf8mb4_unicode_ci`，列注释为空。

`ALTER TABLE ... CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci`，再按 `ads.md` 补列注释。列类型不动。

| 群 | 表 |
| --- | --- |
| 指标 9 | `policy_level_dist`、`policy_type_dist`、`policy_timeseries`、`policy_national_dist`、`policy_sz_dist`、`policy_focus`、`policy_intensity`、`policy_effect`、`policy_metric_timeseries` |
| 图 2 | `policy_graph_node`、`policy_graph_edge` |
| 实体 | `policy_entity` |
| 文本 3 | `policy_text_parse`、`policy_match`、`policy_simulate` |

### 2. 产线 ADS 12 张：只补列注释

库 `gkxlumenx_ads`。表级已是 `utf8mb4_0900_ai_ci`，字符列已是该排序规则，列数与 demo 相同，行数为 0。不 `CONVERT`，不加列。

表：`policy_level_dist`、`policy_type_dist`、`policy_timeseries`、`policy_national_dist`、`policy_sz_dist`、`policy_focus`、`policy_intensity`、`policy_effect`、`policy_metric_timeseries`、`policy_graph_node`、`policy_graph_edge`、`policy_entity`。

### 3. 产线缺列：按 demo 列定义补齐，再补列注释

库 `gkxlumenx_ads`。这三张表现在也是 `utf8mb4_0900_ai_ci`，行数为 0。`AFTER` 只用来对齐 demo 的列顺序，不增加第 2 节以外的列。

`policy_match`（demo 13 列，产线 12 列）：

```sql
ALTER TABLE gkxlumenx_ads.policy_match
  ADD COLUMN metric_id longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL
  AFTER model_version;
```

`policy_simulate`（demo 14 列，产线 13 列）：

```sql
ALTER TABLE gkxlumenx_ads.policy_simulate
  ADD COLUMN metric_id longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL
  AFTER model_version;
```

`policy_text_parse`（demo 11 列，产线 9 列；demo 的 `update_time` 是 `datetime NULL DEFAULT CURRENT_TIMESTAMP`，没有 `ON UPDATE`）：

```sql
ALTER TABLE gkxlumenx_ads.policy_text_parse
  ADD COLUMN metric_id longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL
    AFTER model_version,
  ADD COLUMN update_time datetime NULL DEFAULT CURRENT_TIMESTAMP
    AFTER create_time;
```

### 4. `policy_industry_rel`：只改 demo 两库的 `policy_id`

四库表级都已是 `utf8mb4_0900_ai_ci`，列数都是 7，索引都是 `PRIMARY(id)`、`idx_policy_industry_rel_pid(policy_id, is_deleted)`、`idx_policy_industry_rel_code(industry_link_code, is_deleted, policy_id)`。表注释已是「政策–产业关联。抽取写入，不回写主表」。

demo 两库的 `policy_id` 是 `varchar(128) NOT NULL`、排序规则 `utf8mb4_general_ci`、注释为空。其余列注释已与 `dwd.md` 一致。

```sql
ALTER TABLE demo_gkxlumenx_ads.policy_industry_rel
  MODIFY COLUMN policy_id varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
  COMMENT '对应 policy_base_info.policy_id';

ALTER TABLE demo_gkxlumenx_dwd.policy_industry_rel
  MODIFY COLUMN policy_id varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
  COMMENT '对应 policy_base_info.policy_id';
```

产线 `gkxlumenx_ads.policy_industry_rel` 与 `gkxlumenx_dwd.policy_industry_rel` 的 `policy_id` 已是 `utf8mb4_0900_ai_ci`，注释已是「对应 policy_base_info.policy_id」。**收窄为不执行 ALTER。**

### 明确不在清单

- `policy_base_info`（含 `demo_gkxlumenx_dwd.policy_base_info`）
- `demo_gkxlumenx_dwd.policy_entity`、`gkxlumenx_dwd.policy_entity`：两库都在，各 19 列，表排序规则已是 `utf8mb4_0900_ai_ci`，字符列没有非 `0900`。`information_schema.TABLES.TABLE_ROWS` 统计值为 0。第 2 节没有这两张，本叶不 ALTER
- DROP、改列类型、改主键、加删索引、写 `gkxlumenx_ods` 或供应库 `gkx`

## 按位置 INSERT

检索仓：`repos/lumen-algo-py`、`repos/demo-algo-ent-analysis`、`repos/lumen-svc-platform`。

检索对象：指标 9 + 图 2 + `policy_entity` + 文本 3 + `policy_industry_rel`。

检索写法：`INSERT` / `REPLACE INTO`；`INSERT` 与 `VALUES` 之间没有列清单的语句。

**未发现**不写列名的按位置 INSERT。因此不升级 human:李伟，本叶不改算法。

抽到的写入都带列名，加可空列或带默认值的 `update_time` 不会改写这些语句的列位：

- `repos/lumen-algo-py/vendor/entan-py/polan/common/db.py` 与 `repos/demo-algo-ent-analysis/polan/common/db.py` 的 `insert()` 用字典键生成 `INSERT INTO 表 (列) VALUES (...)`
- 指标、图、`policy_entity`、文本 3 的落库都走这个 `insert()`（如 `polan/basic/indicators.py`、`polan/eval/*`、`polan/graph/ops.py`、`polan/text/parse.py`、`match.py`、`simulate.py`）
- `polan/industry_enrich.py` 写 `policy_industry_rel` 时列名是 `(id, policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)`。demo 仓同路径同写法
- 测试里的 `INSERT INTO ... policy_text_parse` / `policy_industry_rel` 也写了列名
- `lumen-svc-platform` 的 java/xml/sql 里，这些表名只出现在分析任务子类型（`policy_timeseries`、`policy_focus`），没有对应 INSERT
- Nebula 的 `INSERT VERTEX` / `INSERT EDGE` 不是这 16 张 MySQL 表

## 改前快照

查询日 2026-10-26。行数 = `COUNT(*)`。排序规则是表级 `TABLE_COLLATION`；「非 0900 字符列」是 `COLLATION_NAME` 不是 `utf8mb4_0900_ai_ci` 的列数。这些表的排序规则都属于 `utf8mb4`。

### demo_gkxlumenx_ads

| 表 | 行数 | 列数 | 表排序规则 | 非 0900 字符列 |
| --- | ---: | ---: | --- | ---: |
| `policy_level_dist` | 6 | 11 | `utf8mb4_unicode_ci` | 3 |
| `policy_type_dist` | 14 | 10 | `utf8mb4_unicode_ci` | 4 |
| `policy_timeseries` | 46 | 10 | `utf8mb4_unicode_ci` | 5 |
| `policy_national_dist` | 31 | 12 | `utf8mb4_unicode_ci` | 5 |
| `policy_sz_dist` | 5 | 12 | `utf8mb4_unicode_ci` | 5 |
| `policy_focus` | 20031 | 10 | `utf8mb4_unicode_ci` | 5 |
| `policy_intensity` | 20031 | 12 | `utf8mb4_unicode_ci` | 6 |
| `policy_effect` | 155 | 12 | `utf8mb4_unicode_ci` | 6 |
| `policy_metric_timeseries` | 93 | 11 | `utf8mb4_unicode_ci` | 6 |
| `policy_graph_node` | 20001 | 8 | `utf8mb4_unicode_ci` | 5 |
| `policy_graph_edge` | 0 | 8 | `utf8mb4_unicode_ci` | 5 |
| `policy_entity` | 135945 | 10 | `utf8mb4_unicode_ci` | 7 |
| `policy_text_parse` | 20000 | 11 | `utf8mb4_unicode_ci` | 8 |
| `policy_match` | 144 | 13 | `utf8mb4_unicode_ci` | 9 |
| `policy_simulate` | 36 | 14 | `utf8mb4_unicode_ci` | 9 |
| `policy_industry_rel` | 322 | 7 | `utf8mb4_0900_ai_ci` | 1（`policy_id` = `utf8mb4_general_ci`） |

### gkxlumenx_ads

产线这 16 张表行数都是 0，表排序规则都是 `utf8mb4_0900_ai_ci`，字符列没有非 `0900`。

| 表 | 行数 | 列数 | 表排序规则 | 非 0900 字符列 |
| --- | ---: | ---: | --- | ---: |
| `policy_level_dist` | 0 | 11 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_type_dist` | 0 | 10 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_timeseries` | 0 | 10 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_national_dist` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_sz_dist` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_focus` | 0 | 10 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_intensity` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_effect` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_metric_timeseries` | 0 | 11 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_graph_node` | 0 | 8 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_graph_edge` | 0 | 8 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_entity` | 0 | 10 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_text_parse` | 0 | 9 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_match` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_simulate` | 0 | 13 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_industry_rel` | 0 | 7 | `utf8mb4_0900_ai_ci` | 0 |

### policy_industry_rel（DWD）

| 库 | 行数 | 列数 | 表排序规则 | 非 0900 字符列 |
| --- | ---: | ---: | --- | --- |
| `demo_gkxlumenx_dwd` | 322 | 7 | `utf8mb4_0900_ai_ci` | 1（`policy_id` = `utf8mb4_general_ci`） |
| `gkxlumenx_dwd` | 0 | 7 | `utf8mb4_0900_ai_ci` | 0 |

demo ADS 上述 15 张（不含 `policy_industry_rel`）的列注释现为空。`policy_industry_rel` 除 demo 两库的 `policy_id` 外，列注释已与现行 `dwd.md` 的 CREATE 一致。

`CONVERT` 会重建 demo 上有数据的表。行数最多的是 `policy_entity` 135945、`policy_focus` / `policy_intensity` 各 20031、`policy_graph_node` 20001、`policy_text_parse` 20000。

## 架构合规

- D1–D12：本叶只读代码和库，不改调用链、不改算法、不改 Java、不 ALTER。✅
- D14：未涉及对象存储。✅
- 未写 ODS / 供应库 `gkx`，未碰 `policy_base_info`。✅
- 口令未写入本文件。✅

## cost

- actual_tokens: 未单列（随会话）
- model_used: grok-4.7
- actual_cost: 0
- cost_warn: green

## CI/CD

无代码变更，无 commit，无 pipeline。
