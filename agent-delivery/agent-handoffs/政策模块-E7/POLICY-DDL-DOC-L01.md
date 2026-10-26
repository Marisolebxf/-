# POLICY-DDL-DOC-L01

- 任务：把现网 demo 列结构写成带注释的 CREATE，收进 ads.md 与 dwd.md
- 状态：文档已落盘（tech_task，本叶不改 registry）
- claimed_by：`agent:data-agent`
- supervised_by：`human:淮政玮`
- ponytail: off（文档叶不压完整性）

## 范围

只补 `ads.md` / `dwd.md` 里在册表的带注释 CREATE。在两份文件的现文上追加或补注释，没有改 `policy_base_info` 的 37 列清单，没有改库，没有把旧稿 v1 的 `smallint` / `decimal(6,2)` / 二级索引写回去。未 commit、未 push。口令未写入任何文件。

结构对照 2026-10-26 `10.50.11.76` 的 `SHOW CREATE TABLE`。15 张 ADS 表现网表级和字符列都是 `utf8mb4_unicode_ci`；文档按规约写成 `utf8mb4` / `utf8mb4_0900_ai_ci`。列、类型、空值、默认值、索引与现网一致。不写 `AUTO_INCREMENT` 当前值。这 15 张现网都只有主键 `id`。

## 产物清单

- `agent-delivery/data/data-design/storage/POLICY/stores/mysql/ads.md`  
  文末新增「建表语句」。15 张：指标 9（`policy_level_dist`、`policy_type_dist`、`policy_timeseries`、`policy_national_dist`、`policy_sz_dist`、`policy_focus`、`policy_intensity`、`policy_effect`、`policy_metric_timeseries`）+ 图 2（`policy_graph_node`、`policy_graph_edge`）+ `policy_entity` + 文本 3（`policy_text_parse`、`policy_match`、`policy_simulate`）。库名 `demo_gkxlumenx_ads`。`policy_industry_rel` 仍只指向 `dwd.md`，这里不另写 CREATE。
- `agent-delivery/data/data-design/storage/POLICY/stores/mysql/dwd.md`  
  `policy_industry_rel` 原 CREATE 补上 `id` / `create_time` / `update_time` 注释，并写明 `policy_id` 列排序规则收到 `utf8mb4_0900_ai_ci`（现网该列是 `utf8mb4_general_ci`）。列集未另起。  
  新增 `policy_text_parse` 说明和 CREATE，库名 `demo_gkxlumenx_dwd`。
- 本 handoff。

## 对不上注释的列

注释写「现网 demo 有此列，口径待补」。对得上的用 `ads.md` 已有中文用途，或旧稿 v1 §3 里列名仍在、现网取值也对得上的 COMMENT。`policy_industry_rel` 用该节已有中文，没有待补列。

| 表 | 待补列 |
|---|---|
| `policy_level_dist` | `id`，`create_time` |
| `policy_type_dist` | `id`，`stat_date`，`policy_type`，`policy_count`，`create_time` |
| `policy_timeseries` | `id`，`create_time` |
| `policy_national_dist` | `id`，`stat_date`，`province_name`，`policy_count`，`create_time` |
| `policy_sz_dist` | `id`，`stat_date`，`policy_count`，`center_lng`，`center_lat`，`create_time` |
| `policy_focus` | `id`，`region_code`，`create_time` |
| `policy_intensity` | `id`，`scope_name`，`create_time` |
| `policy_effect` | `id`，`scope_type`，`scope_code`，`scope_name`，`metric_id`，`create_time` |
| `policy_metric_timeseries` | `id`，`stat_date`，`create_time` |
| `policy_graph_node` | `id`，`node_key`，`node_type`，`name`，`weight`，`props`，`create_time` |
| `policy_graph_edge` | `id`，`src_key`，`dst_key`，`relation_type`，`weight`，`props`，`create_time` |
| `policy_entity` | `id`，`policy_id`，`entity_name`，`attributes`，`confidence`，`model_version`，`create_time` |
| `policy_text_parse`（ADS 与 DWD 同一列集） | `id`，`policy_id`，`title`，`metric_id`，`create_time`，`update_time` |
| `policy_match` | `id`，`subject_type`，`subject_id`，`subject_name`，`policy_id`，`policy_title`，`rank_no`，`metric_id`，`create_time` |
| `policy_simulate` | `id`，`scenario_id`，`scope_type`，`scope_code`，`params`，`delta_rate`，`explanation`，`metric_id`，`create_time` |

三处是文档口径和现网取值对不上，所以不沿用旧文：

- `policy_type_dist.policy_type`：`ads.md` 写 QPOL-01 科创/行业/园区/招商/人才，旧稿写产业/人才/企业扶持。现网是公示公告、政策文件-*、规范性文件-*、政策解读等。
- `policy_effect.scope_type`：旧稿写 region/industry/policy。现网是 `region_effect`、`region_gap`、`region_layout`、`ds_guide`、`ds_guard`。
- `policy_effect.metric_id`：旧稿和展示窗口把 `IMPLEMENTATION_EFFECT` 放在这张表。现网该列是 `M_POLICY_EFFECT_SCORE`、`M_POLICY_SHORTBOARD_COUNT`、`M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DS_07_POLICY_GUARD_001`、`M_POLICY_DS_07_POLICY_GUARD_008`。`M_POLICY_IMPLEMENTATION_EFFECT` 在 `policy_metric_timeseries`。

其余待补列是 `ads.md` 和旧稿都没有这列的中文。图镜像只写了表级用途，列没有单独口径。

`ext` 仍是现网 `longtext`。注释用旧稿公共列「JSON 扩展」（现网内容是 JSON 文本），没有把类型改回 JSON。

## 现网缺口（不挡本叶）

`demo_gkxlumenx_dwd.policy_text_parse` 不存在，`gkxlumenx_dwd` 也没有。同名表现网只在 `demo_gkxlumenx_ads` 和 `gkxlumenx_ads`。DWD 的 CREATE 列照 `demo_gkxlumenx_ads.policy_text_parse`，库名按总控写成 `demo_gkxlumenx_dwd`。本叶不建表。

`policy_industry_rel.is_deleted` 现网印成 `DEFAULT '0'`，文档保持原来的 `DEFAULT 0`，语义相同，没有另起列集。

## 架构合规

1. 算法只在 Python：本叶只有文档 CREATE，没有算法。✅
2. 调用链前端 → Java → Python：没有改调用链。✅
3. 图谱 NebulaGraph：没有改图库；图镜像只补 MySQL 文档。✅
4. 可观测性：文档叶，没有运行时代码。✅
5. CI/CD：未 commit、未 push，没有业务流水线。✅
6. demo 不 merge 进 lumen：只改编排仓文档。✅
7. 共享聚合、Java 只读 ADS：没有改 Java。✅
8. 标准表先行：CREATE 写入 `ads.md` / `dwd.md`；没有改库，没有写 ODS 或供应库 `gkx`。✅
9. D8 前端规范：不涉及页面。✅
10. D9 血缘：保留 `metric_id` 列；对不上的口径不编造。✅
11. D10 交互规范：不涉及交互。✅
12. D12 demo / lumen 隔离：文档库名是 `demo_gkxlumenx_*`，没有把 demo 服务写进 lumen。✅
13. D14 对象存储：不涉及。✅

`policy_base_info` 的 37 列清单未改。

## cost

- actual_tokens: 未单列
- model_used: grok-4.7
- actual_cost: 0
- cost_warn: green

## 联调

会签通过。
