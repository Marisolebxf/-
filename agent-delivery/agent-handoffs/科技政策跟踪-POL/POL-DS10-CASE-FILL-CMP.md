# POL-DS10-CASE-FILL-CMP · 政策重点比对合规演示用例

ponytail: N/A（文档）

监管人 `human:淮政玮`。任务已在 `in_progress`。本叶只写用例和本 handoff。

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `N/A`（文档） |
| 说明 | 未改业务代码。没有用 YAGNI 跳过架构读面。 |

## 查了哪些表

查库时间 2026-11-07 16:01:36。主机 `10.50.11.76`，用户 `gkxlumenx`。只读 SELECT。口令未写入本文件，未打印。

展示代码：`PolicyPanoramaService` 把 `stats` 的比对块、`version-diff`、`benchmark-report`、详情附带列交给 `gkxlumen-element` 的 `PolicyGapfillController`。`stats` 头条走专题 `metrics`。element 配置缺项库 `gkxlumenx_gapfill`，ADS `demo_gkxlumenx_ads`。正文在目录有行时读 `demo_gkxlumenx_dwd.policy_base_info`（本次未删除行 20008）。

| 表 | 本次行数 | 用途 |
|---|---|---|
| `gkxlumenx_gapfill.gapfill_policy_version_diff` | 5 | 213 |
| `gkxlumenx_gapfill.gapfill_policy_detail_compare` | 4 | 214 条件与材料 |
| `demo_gkxlumenx_dwd.policy_base_info` | 未删除 20008；四条比对键都在 | 213/214 正文 |
| `demo_gkxlumenx_ads.policy_intensity` | 政策力度 20008；省级 31，`intensity_index` 均非空 | 214/216/218 |
| `gkxlumenx_gapfill.gapfill_policy_impl_dept` | 6 | 215 |
| `demo_gkxlumenx_ads.policy_level_dist` | 头条行 `policy_count=20000` | 215 总数 |
| `demo_gkxlumenx_ads.policy_metric_timeseries` | `M_POLICY_SUPPORT_STRENGTH` 31 行 | 216 |
| `gkxlumenx_gapfill.gapfill_policy_benchmark_report` | 6 | 217 |

`POST /display/v1/policy/panorama/jobs` 的 `policy_intensity` 会先 `intensity.run()` 再读 `policy_intensity` 与支持力度时序。本叶未提交该请求，未执行 `--apply`。

## 每条结论与原句出处

| 序号 | 数据情况 | 输入 | 原句出处 |
|---|---|---|---|
| 213 | 可演 | 政策 `18363390`，时点 `2022-04-06` 与 `2022-06-15` | `gapfill_policy_version_diff.summary_text` 三句（新增、修改、删除）。正文标题与发布日在 `policy_base_info.title`、`publish_date` |
| 214 | 可演 | `18363390`、`18407696` | 条件与材料：`gapfill_policy_detail_compare.apply_condition`、`apply_material`。申报时间、受理部门：`policy_base_info.publish_date`、`publish_organization`。`policy_type` 为 NULL，产业类别空。力度分：`policy_intensity.intensity_score` 当前 `20.0000000000`。GET detail 不带出分数；「计算支持力度」未提交 |
| 215 | 可演 | 北京市科学技术委员会、广东省科学技术厅；请求 `kind=all` | 部门行：`gapfill_policy_impl_dept` 的 `item_count`、`list_title` 等 6 行。总数 20000：`policy_level_dist.policy_count` |
| 216 | 可演 | 国内先进地区；北京市、广东省；支持力度 | 对象：`policy_intensity.scope_name` / `scope_code`（`110000`、`440000`）。力度：`policy_metric_timeseries.metric_value` `58.0000000000`，`stat_date` `2026-11-05`，`dim_key` 支持力度 |
| 217 | 可演 | 北京市、广东省；支持力度 | `gapfill_policy_benchmark_report` 的 `difference_text`、`pros_cons_text`、`suggestion_text`、`report_body`。接口是全景 `benchmark-report`。研报 jobs 不在本叶 |
| 218 | 可演 | 地区视角；北京市、广东省 | `policy_intensity.intensity_index`、`industry_coverage`、`rank_no`（北京 `864.1800000000` / `27.8800000000` / 2，广东 `741.5100000000` / `35.7700000000` / 3）。填写时未提交 jobs |

可演 6 行，覆盖不到 0 行。

## 产物

- `agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-CMP-合规演示用例.md`
- 本 handoff

未改索引、未改其他用例、未改 `task-registry.yaml`、未改业务仓、未 commit、未 push。
