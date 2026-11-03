# DR-RES-MOCK-DDL-L01 · 科技数据资源 gapfill 建表

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 已认领，开工时已是 `in_progress` |
| 状态 | 仍是 `in_progress`。本叶不改登记表，不标 `done` |

ponytail: full

## 库与结果

| 项 | 值 |
|---|---|
| 目标库 | `demo_gkxlumenx_ads` |
| 实例 | `10.50.11.76:3306`（账号取自 `lumen-svc-platform` 的 `gkxlumen-element` `application-local.yml`，用户名 `gkxlumenx`。密码未写入本文、未写入 SQL） |
| 是否已在库里建成 | **否** |
| 行数是否为 0 | **未核对**。表没建成，没有执行 `COUNT(*)`。SQL 文件里没有 `INSERT`，本叶没有写入任何业务行 |
| 卡点 | 本机连接 `10.50.11.76:3306` 超时。`errno` 2003，`Can't connect to MySQL server on '10.50.11.76' (timed out)`。SSH 执行器返回未连接，没有改从别的机器执行，也没有改去别的库 |

未写入正式库 `gkxlumenx_ads`、ODS、DWD、久新、库 `gkxlumenx_gapfill`。

## 表清单

方案第 4 节 17 张，语句均为 `CREATE TABLE IF NOT EXISTS`，限定在 `` `demo_gkxlumenx_ads` ``。每张表都有 `id`、`calc_batch_id`、`generated_at`、`fill_method`。`gapfill_dr_block_json.block_code` 没有插行。`gapfill_dr_column_catalog` 只建列，不写现网 131 列。年份列名未改：`gapfill_dr_entity_year.stat_year`。

| 表 | 关键列 |
|---|---|
| `gapfill_dr_type_slice` | `slice_kind`、`name`、`value`、`color`、`avg_quality`、`heat`、`lifecycle` |
| `gapfill_dr_source_channel` | `channel_group`、`channel_code`、`channel_name`、`stat_month`、`volume`、`item_count`、`share_pct`、`change_pct`、`trend`、`reliability`、`avg_quality`、`color`、`activity`、`status`、`sample_tags`、`reliability_hint` |
| `gapfill_dr_catalog_item` | `list_code`、`name`、`source_name`、`item_type`、`channel_name`、`domain_name`、`collect_time`、`quality_score`、`reliability`、`related_project`、`volume_label`、`tags` |
| `gapfill_dr_ingest_task` | `ingest_method`、`status` |
| `gapfill_dr_collection_fact` | `grain`、`period_label`、`metric`、`ingest_method`、`channel_name`、`table_name`、`biz_type`、`row_count`、`size_label`、`update_cycle`、`status`、`anomaly_type`、`anomaly_note` |
| `gapfill_dr_theme_library` | `name`、`category`、`resource_type`、`tags`、`table_count`、`record_yi`、`storage_tb`、`quality`、`source_name`、`region`、`update_freq`、`related_project`、`description` |
| `gapfill_dr_theme_column` | `theme_id`、`table_name`、`table_comment`、`field_name`、`field_type`、`meaning`、`required_flag` |
| `gapfill_dr_quality_issue` | `name`、`table_name`、`issue_type`、`category`、`data_cluster`、`level`、`status`、`found_at`、`ingest_method`、`detail`、`suggestion`、`color` |
| `gapfill_dr_usage_subject` | `subject_type`、`name`、`department`、`region_name`、`call_count`、`user_count`、`share_pct`、`growth_pct`、`theme_name` |
| `gapfill_dr_usage_series` | `series_code`、`series_name`、`period_label`、`sort_no`、`call_count`、`user_count`、`cumulative_count` |
| `gapfill_dr_call_event` | `event_kind`、`subject_name`、`department`、`app_name`、`theme_name`、`api_name`、`event_time`、`call_count`、`result_text`、`field_name` |
| `gapfill_dr_api_probe` | `metric_code`、`label`、`value_num`、`status`、`probed_at` |
| `gapfill_dr_graph_node` | `graph_code`、`node_id`、`name`、`category`、`category_key`、`color`、`size`、`desc_text`、`record_label`、`quality`、`source_name`、`user_label`、`call_label`、`related_nodes` |
| `gapfill_dr_resource_link` | `graph_code`、`src_id`、`dst_id`、`relation`、`strength` |
| `gapfill_dr_block_json` | `block_code`、`payload_json` |
| `gapfill_dr_entity_year` | `entity_type`、`stat_year`、`row_count` |
| `gapfill_dr_column_catalog` | `table_name`、`column_name`、`ordinal`、`data_type`、`column_comment` |

中文关键列落成的列名：目录明细的名称/来源/类型/渠道/领域/采集时间/质量分/可靠度/关联项目/体量/标签；调用主体的名称/部门/区域/调用次数/用户数/占比/增速/主题；调用事件的主体/部门/应用/主题/接口/时间/次数/结果/字段名；图节点详情的记录量/质量/来源/用户/调用/关联节点。

## 偏离

`gapfill_dr_theme_library` 比方案第 4 节多一列 `name`。第 5 节 `themeDatabases` 卡片要有名称，第 4 节卡片列没有写这一列。没有另建业务表。

没有改方案第 5 节，没有改契约，没有改 `DR-RES-A0-L01.md`。

## 架构合规

| 铁律 | 结果 |
|---|---|
| 只写验收库 `demo_gkxlumenx_ads`，表名 `gapfill_dr_` | SQL 已限定该库。本机没连上，库上没有执行成功 |
| 不写正式 `gkxlumenx_ads`、ODS、DWD、久新、`gkxlumenx_gapfill` | 未写 |
| D18 | 本叶只准备 mock 空表 DDL，不在接口里返回写死 mock，也没有灌行 |
| 算法 / 调用链 / 可观测 | 本叶无代码 |

## CI/CD

- 分支：`dev`（工作区）
- commit：无。未 commit，未 push
- pipeline / K8s：无

## 产物

- `agent-delivery/agent-handoffs/科技数据资源-DR/DR-RES-MOCK-DDL-L01.sql`
- `agent-delivery/agent-handoffs/科技数据资源-DR/DR-RES-MOCK-DDL-L01.md`

连上 `10.50.11.76:3306` 之后，对 `demo_gkxlumenx_ads` 执行该 SQL，再用只读语句列出 `gapfill_dr_%` 并 `COUNT(*)`。本叶没有做这一步。
