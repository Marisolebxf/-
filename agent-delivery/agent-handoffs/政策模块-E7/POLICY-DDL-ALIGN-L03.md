# POLICY-DDL-ALIGN-L03

- 任务：按 POLICY-DDL-IMPACT-L02 的拟 ALTER 对齐政策 ADS 字符集与列注释
- 状态：in_progress（本叶不改 task-registry）
- 执行：agent:data-agent
- 监管人：human:淮政玮
- 日期：2026-10-26
- ponytail: full
- 依据：`agent-delivery/agent-handoffs/政策模块-E7/POLICY-DDL-IMPACT-L02.md`
- 列注释来源：已提交的 `agent-delivery/data/data-design/storage/POLICY/stores/mysql/ads.md`（工作区与 HEAD 一致，`dc566597`）

服务器 `10.50.11.76:3306`，版本 8.0.39。先改 `demo_gkxlumenx_*`，再改 `gkxlumenx_*`。清单内语句全部成功，没有失败。口令未写入本文件。

联调通过。

## 做法

- demo `demo_gkxlumenx_ads` 15 张：`CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci`，再按 ads.md 补列注释。列类型、空值、默认值、`EXTRA` 不动。
- 产线 `gkxlumenx_ads` 12 张：不 `CONVERT`、不加列，只补与 ads.md 一致的列注释。
- 产线缺列只加这三句，字符集显式 `utf8mb4` / `utf8mb4_0900_ai_ci`，然后补这三张的列注释。`update_time` 是 `datetime NULL DEFAULT CURRENT_TIMESTAMP`，没有 `ON UPDATE`。
- 只改 demo 两库 `policy_industry_rel.policy_id`，保持 `varchar(128) NOT NULL`，排序规则改为 `utf8mb4_0900_ai_ci` 并写上注释。产线两库已对齐，未执行。

列注释语句的列定义取自当时的 `SHOW CREATE TABLE`，只追加 `COMMENT`。注释正文与 ads.md 逐列核对。每条语句前后核对 `COLUMN_TYPE`、空值、默认值、`EXTRA`、字符集、`COUNT(*)`、`AUTO_INCREMENT`、索引签名。`CONVERT` 只改排序规则。不一致会中止，本次全部通过。

产线这 12 张以及三张里原有的 `longtext`，表级已经是 `utf8mb4_0900_ai_ci`，`SHOW CREATE` 在列排序规则与表默认相同时省略了 `CHARACTER SET` 子句，所以注释语句里这些列写成 `longtext COMMENT '...'`。改后 `information_schema` 仍是 `utf8mb4` / `utf8mb4_0900_ai_ci`。新加的 `metric_id` 在 `SHOW CREATE` 里仍带显式字符集。

每次连接在 ALTER 之前设置了会话参数，不是表结构变更：`SET NAMES utf8mb4`；`net_read_timeout` / `net_write_timeout` = 3600；`lock_wait_timeout` = 1800；`innodb_lock_wait_timeout` = 600；`wait_timeout` / `interactive_timeout` = 28800；`group_concat_max_len` = 102400。

未改 `policy_base_info`（含排序规则和列集）。未 `DROP`。未改主键。未加删索引。未写 `gkxlumenx_ods` 或供应库 `gkx`。未在 DWD 新建 `policy_text_parse`。未重建 `v_cms_pol`。未把 demo 的 `utf8mb4_unicode_ci` 抄到产线。

## 改前快照

2026-10-26 18:16:00。行数 = `information_schema.TABLES.TABLE_ROWS`（InnoDB 统计估计，不是 `COUNT(*)`）。列数 = `information_schema.COLUMNS` 行数。表排序规则 = `TABLE_COLLATION`。非 0900 字符列 = `COLLATION_NAME` 非空且不是 `utf8mb4_0900_ai_ci` 的列数。

`demo_gkxlumenx_dwd.policy_entity` 与 `gkxlumenx_dwd.policy_entity` 因快照按表名过滤被读出，本叶未对它们执行 ALTER，仅作对照。

### demo_gkxlumenx_ads

| 表 | 行数 | 列数 | 表排序规则 | 非 0900 字符列 |
| --- | ---: | ---: | --- | ---: |
| `policy_effect` | 155 | 12 | `utf8mb4_unicode_ci` | 6 |
| `policy_entity` | 134511 | 10 | `utf8mb4_unicode_ci` | 7 |
| `policy_focus` | 19554 | 10 | `utf8mb4_unicode_ci` | 5 |
| `policy_graph_edge` | 0 | 8 | `utf8mb4_unicode_ci` | 5 |
| `policy_graph_node` | 20038 | 8 | `utf8mb4_unicode_ci` | 5 |
| `policy_industry_rel` | 322 | 7 | `utf8mb4_0900_ai_ci` | 1 |
| `policy_intensity` | 19630 | 12 | `utf8mb4_unicode_ci` | 6 |
| `policy_level_dist` | 6 | 11 | `utf8mb4_unicode_ci` | 3 |
| `policy_match` | 144 | 13 | `utf8mb4_unicode_ci` | 9 |
| `policy_metric_timeseries` | 93 | 11 | `utf8mb4_unicode_ci` | 6 |
| `policy_national_dist` | 31 | 12 | `utf8mb4_unicode_ci` | 5 |
| `policy_simulate` | 36 | 14 | `utf8mb4_unicode_ci` | 9 |
| `policy_sz_dist` | 5 | 12 | `utf8mb4_unicode_ci` | 5 |
| `policy_text_parse` | 18468 | 11 | `utf8mb4_unicode_ci` | 8 |
| `policy_timeseries` | 46 | 10 | `utf8mb4_unicode_ci` | 5 |
| `policy_type_dist` | 14 | 10 | `utf8mb4_unicode_ci` | 4 |

### demo_gkxlumenx_dwd

| 表 | 行数 | 列数 | 表排序规则 | 非 0900 字符列 |
| --- | ---: | ---: | --- | ---: |
| `policy_entity`（未改） | 0 | 19 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_industry_rel` | 322 | 7 | `utf8mb4_0900_ai_ci` | 1 |

### gkxlumenx_ads

| 表 | 行数 | 列数 | 表排序规则 | 非 0900 字符列 |
| --- | ---: | ---: | --- | ---: |
| `policy_effect` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_entity` | 0 | 10 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_focus` | 0 | 10 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_graph_edge` | 0 | 8 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_graph_node` | 0 | 8 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_industry_rel`（未改） | 0 | 7 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_intensity` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_level_dist` | 0 | 11 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_match` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_metric_timeseries` | 0 | 11 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_national_dist` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_simulate` | 0 | 13 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_sz_dist` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_text_parse` | 0 | 9 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_timeseries` | 0 | 10 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_type_dist` | 0 | 10 | `utf8mb4_0900_ai_ci` | 0 |

### gkxlumenx_dwd

| 表 | 行数 | 列数 | 表排序规则 | 非 0900 字符列 |
| --- | ---: | ---: | --- | ---: |
| `policy_entity`（未改） | 0 | 19 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_industry_rel`（未改） | 0 | 7 | `utf8mb4_0900_ai_ci` | 0 |

demo 15 张改前 `COUNT(*)`（与上表估计行数分开）：`policy_level_dist` 6，`policy_type_dist` 14，`policy_timeseries` 46，`policy_national_dist` 31，`policy_sz_dist` 5，`policy_focus` 20031，`policy_intensity` 20031，`policy_effect` 155，`policy_metric_timeseries` 93，`policy_graph_node` 20001，`policy_graph_edge` 0，`policy_entity` 135945，`policy_text_parse` 20000，`policy_match` 144，`policy_simulate` 36。改后 `COUNT(*)` 与这些数字相同。`policy_entity` 的 `TABLE_ROWS` 估计仍是 134511。

## 实际执行的语句

下面 `--` 行是清单标注，没有单独送给服务器。标注下一句才是执行的 ALTER。顺序：demo 15 张 CONVERT 后补注释，demo 两库 `policy_industry_rel`，产线 12 张只补注释，产线 3 张先加列再补注释。

```sql
-- CONVERT demo_gkxlumenx_ads.policy_level_dist
ALTER TABLE demo_gkxlumenx_ads.policy_level_dist CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_level_dist
ALTER TABLE demo_gkxlumenx_ads.policy_level_dist
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `stat_date` date DEFAULT NULL COMMENT '统计日期/批次快照日',
  MODIFY COLUMN `level` bigint DEFAULT NULL COMMENT '层级 1国家/2省/3市/4区县；NULL=全量汇总行',
  MODIFY COLUMN `policy_count` bigint DEFAULT NULL COMMENT '政策去重数',
  MODIFY COLUMN `ratio` decimal(38,10) DEFAULT NULL COMMENT '占比%',
  MODIFY COLUMN `valid_count` bigint DEFAULT NULL COMMENT '有效政策数（M_POLICY_VALIDITY_RATE 分子）',
  MODIFY COLUMN `validity_rate` decimal(38,10) DEFAULT NULL COMMENT '政策时效=有效/总数%',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_LEVEL_DIST/M_POLICY_TOTAL_COUNT/M_POLICY_VALIDITY_RATE',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_type_dist
ALTER TABLE demo_gkxlumenx_ads.policy_type_dist CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_type_dist
ALTER TABLE demo_gkxlumenx_ads.policy_type_dist
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `stat_date` date DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_count` bigint DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `ratio` decimal(38,10) DEFAULT NULL COMMENT '占比%',
  MODIFY COLUMN `yoy` decimal(38,10) DEFAULT NULL COMMENT '同比增长率%',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_TYPE_DIST',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_timeseries
ALTER TABLE demo_gkxlumenx_ads.policy_timeseries CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_timeseries
ALTER TABLE demo_gkxlumenx_ads.policy_timeseries
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `period_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'Y/Q/M 粒度',
  MODIFY COLUMN `period_key` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '如 2025 / 2025Q1 / 2025-03',
  MODIFY COLUMN `publish_count` bigint DEFAULT NULL COMMENT '发布量',
  MODIFY COLUMN `growth_rate` decimal(38,10) DEFAULT NULL COMMENT '环比增长率%',
  MODIFY COLUMN `continuity_rate` decimal(38,10) DEFAULT NULL COMMENT '连续性指标%',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_TIMESERIES',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_national_dist
ALTER TABLE demo_gkxlumenx_ads.policy_national_dist CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_national_dist
ALTER TABLE demo_gkxlumenx_ads.policy_national_dist
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `stat_date` date DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `province_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '省级区划码 <- dim_region',
  MODIFY COLUMN `province_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_count` bigint DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `yoy` decimal(38,10) DEFAULT NULL COMMENT '同比增长率%',
  MODIFY COLUMN `center_lng` decimal(38,10) DEFAULT NULL COMMENT '省中心经度(地图渲染)',
  MODIFY COLUMN `center_lat` decimal(38,10) DEFAULT NULL COMMENT '省中心纬度',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_NATIONAL_DIST',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_sz_dist
ALTER TABLE demo_gkxlumenx_ads.policy_sz_dist CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_sz_dist
ALTER TABLE demo_gkxlumenx_ads.policy_sz_dist
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `stat_date` date DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `district_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '深圳区县区划码 <- dim_region',
  MODIFY COLUMN `district_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '福田/南山/宝安/龙岗…',
  MODIFY COLUMN `policy_count` bigint DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `yoy` decimal(38,10) DEFAULT NULL COMMENT '增长趋势%',
  MODIFY COLUMN `center_lng` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `center_lat` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_SZ_DIST',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_focus
ALTER TABLE demo_gkxlumenx_ads.policy_focus CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_focus
ALTER TABLE demo_gkxlumenx_ads.policy_focus
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '单政策粒度；NULL=区域/产业汇总',
  MODIFY COLUMN `region_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `focus_score` decimal(38,10) DEFAULT NULL COMMENT '政策焦点指数（QPOL-02）',
  MODIFY COLUMN `opportunity_cnt` bigint DEFAULT NULL COMMENT '政策机遇数（QPOL-02）',
  MODIFY COLUMN `relation_degree` decimal(38,10) DEFAULT NULL COMMENT '政策关联度（QPOL-03，图谱度中心性）',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_FOCUS_INDEX/M_POLICY_OPPORTUNITY_COUNT/M_POLICY_RELATION_DEGREE',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_intensity
ALTER TABLE demo_gkxlumenx_ads.policy_intensity CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_intensity
ALTER TABLE demo_gkxlumenx_ads.policy_intensity
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scope_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'province/city/policy 粒度',
  MODIFY COLUMN `scope_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '区划码或 policy_id',
  MODIFY COLUMN `scope_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `intensity_index` decimal(38,10) DEFAULT NULL COMMENT '政策力度指数（QPOL-02）',
  MODIFY COLUMN `intensity_score` decimal(38,10) DEFAULT NULL COMMENT '单政策力度评分（QPOL-02）',
  MODIFY COLUMN `industry_coverage` decimal(38,10) DEFAULT NULL COMMENT '产业覆盖度%',
  MODIFY COLUMN `rank_no` bigint DEFAULT NULL COMMENT '力度排行',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_INTENSITY_INDEX/M_POLICY_INTENSITY_SCORE/M_POLICY_INDUSTRY_COVERAGE',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_effect
ALTER TABLE demo_gkxlumenx_ads.policy_effect CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_effect
ALTER TABLE demo_gkxlumenx_ads.policy_effect
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scope_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scope_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scope_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `effect_score` decimal(38,10) DEFAULT NULL COMMENT '政策效果评分（QPOL-02，含待采购输入）',
  MODIFY COLUMN `shortboard_cnt` bigint DEFAULT NULL COMMENT '政策短板数（QPOL-02）',
  MODIFY COLUMN `layout_rec_cnt` bigint DEFAULT NULL COMMENT '政策布局建议数（QPOL-02）',
  MODIFY COLUMN `impl_effect` decimal(38,10) DEFAULT NULL COMMENT '落地实效性（QPOL-02，含待采购输入）',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_metric_timeseries
ALTER TABLE demo_gkxlumenx_ads.policy_metric_timeseries CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_metric_timeseries
ALTER TABLE demo_gkxlumenx_ads.policy_metric_timeseries
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_SUPPORT_STRENGTH/M_POLICY_INDUSTRY_FIT/M_POLICY_IMPLEMENTATION_EFFECT 等',
  MODIFY COLUMN `region_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '区域/对标地区',
  MODIFY COLUMN `industry_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '目标产业(三维框架)',
  MODIFY COLUMN `stat_date` date DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `metric_value` decimal(38,10) DEFAULT NULL COMMENT '指标值',
  MODIFY COLUMN `yoy` decimal(38,10) DEFAULT NULL COMMENT '同比%',
  MODIFY COLUMN `dim_key` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '维度键(支持力度/产业适配/落地实效)',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_graph_node
ALTER TABLE demo_gkxlumenx_ads.policy_graph_node CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_graph_node
ALTER TABLE demo_gkxlumenx_ads.policy_graph_node
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `node_key` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `node_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `weight` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `props` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_graph_edge
ALTER TABLE demo_gkxlumenx_ads.policy_graph_edge CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_graph_edge
ALTER TABLE demo_gkxlumenx_ads.policy_graph_edge
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `src_key` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `dst_key` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `relation_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `weight` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `props` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_entity
ALTER TABLE demo_gkxlumenx_ads.policy_entity CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_entity
ALTER TABLE demo_gkxlumenx_ads.policy_entity
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `entity_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '取值 policy/level/type/org/region/time/keyword/industry/enterprise/talent/service',
  MODIFY COLUMN `entity_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `attributes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `source_field` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '该实体从 DWD 哪一列抽出，D9 字段级血缘',
  MODIFY COLUMN `confidence` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `model_version` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_text_parse
ALTER TABLE demo_gkxlumenx_ads.policy_text_parse CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_text_parse
ALTER TABLE demo_gkxlumenx_ads.policy_text_parse
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `title` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `summary` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '摘要',
  MODIFY COLUMN `structured_elements` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '结构化要素',
  MODIFY COLUMN `auto_tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '自动标签',
  MODIFY COLUMN `model_version` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '规则基线产物须在 UI 标注模型版本',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_match
ALTER TABLE demo_gkxlumenx_ads.policy_match CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_match
ALTER TABLE demo_gkxlumenx_ads.policy_match
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `subject_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `subject_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `subject_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_title` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `match_score` decimal(38,10) DEFAULT NULL COMMENT '匹配打分',
  MODIFY COLUMN `match_reasons` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '匹配理由',
  MODIFY COLUMN `rank_no` bigint DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `model_version` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '规则基线产物须在 UI 标注模型版本',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- CONVERT demo_gkxlumenx_ads.policy_simulate
ALTER TABLE demo_gkxlumenx_ads.policy_simulate CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- COMMENT demo_gkxlumenx_ads.policy_simulate
ALTER TABLE demo_gkxlumenx_ads.policy_simulate
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scenario_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scope_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scope_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `params` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `baseline_value` decimal(38,10) DEFAULT NULL COMMENT '基线',
  MODIFY COLUMN `simulated_value` decimal(38,10) DEFAULT NULL COMMENT '仿真值',
  MODIFY COLUMN `delta_rate` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `curve` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '曲线',
  MODIFY COLUMN `explanation` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `model_version` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '规则基线产物须在 UI 标注模型版本',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- MODIFY policy_id demo_gkxlumenx_ads.policy_industry_rel
ALTER TABLE demo_gkxlumenx_ads.policy_industry_rel MODIFY COLUMN policy_id varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '对应 policy_base_info.policy_id';

-- MODIFY policy_id demo_gkxlumenx_dwd.policy_industry_rel
ALTER TABLE demo_gkxlumenx_dwd.policy_industry_rel MODIFY COLUMN policy_id varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '对应 policy_base_info.policy_id';

-- COMMENT gkxlumenx_ads.policy_level_dist
ALTER TABLE gkxlumenx_ads.policy_level_dist
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `stat_date` date DEFAULT NULL COMMENT '统计日期/批次快照日',
  MODIFY COLUMN `level` bigint DEFAULT NULL COMMENT '层级 1国家/2省/3市/4区县；NULL=全量汇总行',
  MODIFY COLUMN `policy_count` bigint DEFAULT NULL COMMENT '政策去重数',
  MODIFY COLUMN `ratio` decimal(38,10) DEFAULT NULL COMMENT '占比%',
  MODIFY COLUMN `valid_count` bigint DEFAULT NULL COMMENT '有效政策数（M_POLICY_VALIDITY_RATE 分子）',
  MODIFY COLUMN `validity_rate` decimal(38,10) DEFAULT NULL COMMENT '政策时效=有效/总数%',
  MODIFY COLUMN `metric_id` longtext COMMENT 'M_POLICY_LEVEL_DIST/M_POLICY_TOTAL_COUNT/M_POLICY_VALIDITY_RATE',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- COMMENT gkxlumenx_ads.policy_type_dist
ALTER TABLE gkxlumenx_ads.policy_type_dist
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `stat_date` date DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_type` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_count` bigint DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `ratio` decimal(38,10) DEFAULT NULL COMMENT '占比%',
  MODIFY COLUMN `yoy` decimal(38,10) DEFAULT NULL COMMENT '同比增长率%',
  MODIFY COLUMN `metric_id` longtext COMMENT 'M_POLICY_TYPE_DIST',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- COMMENT gkxlumenx_ads.policy_timeseries
ALTER TABLE gkxlumenx_ads.policy_timeseries
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `period_type` longtext COMMENT 'Y/Q/M 粒度',
  MODIFY COLUMN `period_key` longtext COMMENT '如 2025 / 2025Q1 / 2025-03',
  MODIFY COLUMN `publish_count` bigint DEFAULT NULL COMMENT '发布量',
  MODIFY COLUMN `growth_rate` decimal(38,10) DEFAULT NULL COMMENT '环比增长率%',
  MODIFY COLUMN `continuity_rate` decimal(38,10) DEFAULT NULL COMMENT '连续性指标%',
  MODIFY COLUMN `metric_id` longtext COMMENT 'M_POLICY_TIMESERIES',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- COMMENT gkxlumenx_ads.policy_national_dist
ALTER TABLE gkxlumenx_ads.policy_national_dist
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `stat_date` date DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `province_code` longtext COMMENT '省级区划码 <- dim_region',
  MODIFY COLUMN `province_name` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_count` bigint DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `yoy` decimal(38,10) DEFAULT NULL COMMENT '同比增长率%',
  MODIFY COLUMN `center_lng` decimal(38,10) DEFAULT NULL COMMENT '省中心经度(地图渲染)',
  MODIFY COLUMN `center_lat` decimal(38,10) DEFAULT NULL COMMENT '省中心纬度',
  MODIFY COLUMN `metric_id` longtext COMMENT 'M_POLICY_NATIONAL_DIST',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- COMMENT gkxlumenx_ads.policy_sz_dist
ALTER TABLE gkxlumenx_ads.policy_sz_dist
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `stat_date` date DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `district_code` longtext COMMENT '深圳区县区划码 <- dim_region',
  MODIFY COLUMN `district_name` longtext COMMENT '福田/南山/宝安/龙岗…',
  MODIFY COLUMN `policy_count` bigint DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `yoy` decimal(38,10) DEFAULT NULL COMMENT '增长趋势%',
  MODIFY COLUMN `center_lng` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `center_lat` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `metric_id` longtext COMMENT 'M_POLICY_SZ_DIST',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- COMMENT gkxlumenx_ads.policy_focus
ALTER TABLE gkxlumenx_ads.policy_focus
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_id` longtext COMMENT '单政策粒度；NULL=区域/产业汇总',
  MODIFY COLUMN `region_code` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `focus_score` decimal(38,10) DEFAULT NULL COMMENT '政策焦点指数（QPOL-02）',
  MODIFY COLUMN `opportunity_cnt` bigint DEFAULT NULL COMMENT '政策机遇数（QPOL-02）',
  MODIFY COLUMN `relation_degree` decimal(38,10) DEFAULT NULL COMMENT '政策关联度（QPOL-03，图谱度中心性）',
  MODIFY COLUMN `metric_id` longtext COMMENT 'M_POLICY_FOCUS_INDEX/M_POLICY_OPPORTUNITY_COUNT/M_POLICY_RELATION_DEGREE',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- COMMENT gkxlumenx_ads.policy_intensity
ALTER TABLE gkxlumenx_ads.policy_intensity
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scope_type` longtext COMMENT 'province/city/policy 粒度',
  MODIFY COLUMN `scope_code` longtext COMMENT '区划码或 policy_id',
  MODIFY COLUMN `scope_name` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `intensity_index` decimal(38,10) DEFAULT NULL COMMENT '政策力度指数（QPOL-02）',
  MODIFY COLUMN `intensity_score` decimal(38,10) DEFAULT NULL COMMENT '单政策力度评分（QPOL-02）',
  MODIFY COLUMN `industry_coverage` decimal(38,10) DEFAULT NULL COMMENT '产业覆盖度%',
  MODIFY COLUMN `rank_no` bigint DEFAULT NULL COMMENT '力度排行',
  MODIFY COLUMN `metric_id` longtext COMMENT 'M_POLICY_INTENSITY_INDEX/M_POLICY_INTENSITY_SCORE/M_POLICY_INDUSTRY_COVERAGE',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- COMMENT gkxlumenx_ads.policy_effect
ALTER TABLE gkxlumenx_ads.policy_effect
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scope_type` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scope_code` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scope_name` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `effect_score` decimal(38,10) DEFAULT NULL COMMENT '政策效果评分（QPOL-02，含待采购输入）',
  MODIFY COLUMN `shortboard_cnt` bigint DEFAULT NULL COMMENT '政策短板数（QPOL-02）',
  MODIFY COLUMN `layout_rec_cnt` bigint DEFAULT NULL COMMENT '政策布局建议数（QPOL-02）',
  MODIFY COLUMN `impl_effect` decimal(38,10) DEFAULT NULL COMMENT '落地实效性（QPOL-02，含待采购输入）',
  MODIFY COLUMN `metric_id` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- COMMENT gkxlumenx_ads.policy_metric_timeseries
ALTER TABLE gkxlumenx_ads.policy_metric_timeseries
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `metric_id` longtext COMMENT 'M_POLICY_SUPPORT_STRENGTH/M_POLICY_INDUSTRY_FIT/M_POLICY_IMPLEMENTATION_EFFECT 等',
  MODIFY COLUMN `region_code` longtext COMMENT '区域/对标地区',
  MODIFY COLUMN `industry_code` longtext COMMENT '目标产业(三维框架)',
  MODIFY COLUMN `stat_date` date DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `metric_value` decimal(38,10) DEFAULT NULL COMMENT '指标值',
  MODIFY COLUMN `yoy` decimal(38,10) DEFAULT NULL COMMENT '同比%',
  MODIFY COLUMN `dim_key` longtext COMMENT '维度键(支持力度/产业适配/落地实效)',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `ext` longtext COMMENT 'JSON 扩展',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- COMMENT gkxlumenx_ads.policy_graph_node
ALTER TABLE gkxlumenx_ads.policy_graph_node
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `node_key` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `node_type` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `name` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `weight` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `props` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- COMMENT gkxlumenx_ads.policy_graph_edge
ALTER TABLE gkxlumenx_ads.policy_graph_edge
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `src_key` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `dst_key` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `relation_type` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `weight` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `props` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- COMMENT gkxlumenx_ads.policy_entity
ALTER TABLE gkxlumenx_ads.policy_entity
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_id` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `entity_type` longtext COMMENT '取值 policy/level/type/org/region/time/keyword/industry/enterprise/talent/service',
  MODIFY COLUMN `entity_name` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `attributes` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `source_field` longtext COMMENT '该实体从 DWD 哪一列抽出，D9 字段级血缘',
  MODIFY COLUMN `confidence` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `model_version` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- ADD gkxlumenx_ads.policy_match
ALTER TABLE gkxlumenx_ads.policy_match ADD COLUMN metric_id longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL AFTER model_version;

-- COMMENT gkxlumenx_ads.policy_match
ALTER TABLE gkxlumenx_ads.policy_match
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `subject_type` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `subject_id` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `subject_name` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_id` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_title` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `match_score` decimal(38,10) DEFAULT NULL COMMENT '匹配打分',
  MODIFY COLUMN `match_reasons` longtext COMMENT '匹配理由',
  MODIFY COLUMN `rank_no` bigint DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `model_version` longtext COMMENT '规则基线产物须在 UI 标注模型版本',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- ADD gkxlumenx_ads.policy_simulate
ALTER TABLE gkxlumenx_ads.policy_simulate ADD COLUMN metric_id longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL AFTER model_version;

-- COMMENT gkxlumenx_ads.policy_simulate
ALTER TABLE gkxlumenx_ads.policy_simulate
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scenario_id` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scope_type` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `scope_code` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `params` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `baseline_value` decimal(38,10) DEFAULT NULL COMMENT '基线',
  MODIFY COLUMN `simulated_value` decimal(38,10) DEFAULT NULL COMMENT '仿真值',
  MODIFY COLUMN `delta_rate` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `curve` longtext COMMENT '曲线',
  MODIFY COLUMN `explanation` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `model_version` longtext COMMENT '规则基线产物须在 UI 标注模型版本',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';

-- ADD gkxlumenx_ads.policy_text_parse
ALTER TABLE gkxlumenx_ads.policy_text_parse ADD COLUMN metric_id longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL AFTER model_version, ADD COLUMN update_time datetime NULL DEFAULT CURRENT_TIMESTAMP AFTER create_time;

-- COMMENT gkxlumenx_ads.policy_text_parse
ALTER TABLE gkxlumenx_ads.policy_text_parse
  MODIFY COLUMN `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `policy_id` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `title` longtext COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `summary` longtext COMMENT '摘要',
  MODIFY COLUMN `structured_elements` longtext COMMENT '结构化要素',
  MODIFY COLUMN `auto_tags` longtext COMMENT '自动标签',
  MODIFY COLUMN `model_version` longtext COMMENT '规则基线产物须在 UI 标注模型版本',
  MODIFY COLUMN `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `calc_batch_id` longtext COMMENT 'mock_ 前缀区分 Mock',
  MODIFY COLUMN `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  MODIFY COLUMN `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补';
```

## 改后快照

2026-10-26 18:34:04。口径与改前相同。

### demo_gkxlumenx_ads

| 表 | 行数 | 列数 | 表排序规则 | 非 0900 字符列 |
| --- | ---: | ---: | --- | ---: |
| `policy_effect` | 155 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_entity` | 134511 | 10 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_focus` | 19554 | 10 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_graph_edge` | 0 | 8 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_graph_node` | 20038 | 8 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_industry_rel` | 322 | 7 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_intensity` | 19630 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_level_dist` | 6 | 11 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_match` | 144 | 13 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_metric_timeseries` | 93 | 11 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_national_dist` | 31 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_simulate` | 36 | 14 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_sz_dist` | 5 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_text_parse` | 18468 | 11 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_timeseries` | 46 | 10 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_type_dist` | 14 | 10 | `utf8mb4_0900_ai_ci` | 0 |

### demo_gkxlumenx_dwd

| 表 | 行数 | 列数 | 表排序规则 | 非 0900 字符列 |
| --- | ---: | ---: | --- | ---: |
| `policy_entity`（未改） | 0 | 19 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_industry_rel` | 322 | 7 | `utf8mb4_0900_ai_ci` | 0 |

### gkxlumenx_ads

| 表 | 行数 | 列数 | 表排序规则 | 非 0900 字符列 |
| --- | ---: | ---: | --- | ---: |
| `policy_effect` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_entity` | 0 | 10 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_focus` | 0 | 10 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_graph_edge` | 0 | 8 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_graph_node` | 0 | 8 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_industry_rel`（未改） | 0 | 7 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_intensity` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_level_dist` | 0 | 11 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_match` | 0 | 13 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_metric_timeseries` | 0 | 11 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_national_dist` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_simulate` | 0 | 14 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_sz_dist` | 0 | 12 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_text_parse` | 0 | 11 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_timeseries` | 0 | 10 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_type_dist` | 0 | 10 | `utf8mb4_0900_ai_ci` | 0 |

### gkxlumenx_dwd

| 表 | 行数 | 列数 | 表排序规则 | 非 0900 字符列 |
| --- | ---: | ---: | --- | ---: |
| `policy_entity`（未改） | 0 | 19 | `utf8mb4_0900_ai_ci` | 0 |
| `policy_industry_rel`（未改） | 0 | 7 | `utf8mb4_0900_ai_ci` | 0 |

产线 `policy_match` 列数 12→13，`policy_simulate` 13→14，`policy_text_parse` 9→11。`policy_text_parse.update_time` 改后为 `datetime`、可空、默认 `CURRENT_TIMESTAMP`、`EXTRA=DEFAULT_GENERATED`，没有 `ON UPDATE`。`metric_id` 为 `longtext`、可空、字符集 `utf8mb4`、排序规则 `utf8mb4_0900_ai_ci`。demo 两库 `policy_id` 仍是 `varchar(128) NOT NULL`，排序规则变为 `utf8mb4_0900_ai_ci`，注释为「对应 policy_base_info.policy_id」。

## 架构合规

- D1–D4：未改算法、未改 Java、未改调用链、未改 Nebula、未改可观测埋点。✅
- D5：无代码提交，无 pipeline。✅
- D6 / D12：demo 与产线库按清单分别 ALTER，没有把 demo 仓 merge 进 lumen，也没有让 lumen 调用 demo 服务。✅
- D8 / D10：未改前端。✅
- D9：列注释只采用已提交 ads.md 的正文，未新写口径。✅
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
