# LUMEN-POLICY-PY-SEARCH-FILTER-L01 · 政策检索高级筛选参数

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)
> 派单：[`LUMEN-POLICY-ADV-FILTER-派单说明.md`](./LUMEN-POLICY-ADV-FILTER-派单说明.md) 第 1 节
> 条数材料：[`产业检索政策条数-20261024.md`](../../qa/test-cases/SDWJSF-KJZTFWSFK/policy-政策分析/产业检索政策条数-20261024.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工前已由 coordinator 认领并置 `in_progress`。本叶不改任务状态、不 commit、不 push。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 筛选落在已有 `search_policies` 的 SQL 上，不新造检索器。未改 `eval/`、`models/`、打分函数、算子 `run()`。未用 YAGNI 跳过调用链与 handoff。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只扩查询参数，无大日志要压缩。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 未改图、未改工厂边。检索仍只读 DWD `policy_base_info` 与 ADS `policy_industry_rel`。选项接口另只读同库 `level` / `status` / `ext1` 去重，以及 DWD `industry_chain_node`（链节点名单，不是政策工厂写入）。 |
| 会签态 | `approved`（`storage/POLICY/01-data-flow.md` frontmatter：`status: approved`，`signoff_by: human:淮政玮`，`signoff_at: 2026-08-21`；本叶不翻签） |
| 说明 | Java 仍只打 `/internal/policy/**`。本叶不让 Java 直连 MySQL。 |

## 范围与实现

`GET /internal/policy/search` 的 SQL 在 `polan.search.search_policies`（`industry_rel_exists` / 新增 `industry_code_exists`）。路由只收参。

无新参数时，关键词、文号、单值级别 / 类型 / 地区 / 机关、`industry_vid` 等值关联与现在一致。

| 参数 | 行为 |
|------|------|
| `publish_year_from` / `publish_year_to` | `publish_year` 闭区间。空端不加条件。非四位数字 → HTTP 400 |
| `level` / `status` | 可重复。`CAST(列 AS CHAR) =` ，同字段或者 |
| `policy_type` | 可重复。仍筛 `ext1` LIKE，同字段或者 |
| `region` / `ministry` | 可重复。仍是 LIKE，同字段或者 |
| `industry_code` | 可重复，INB 码（大小写折成大写）。一条 EXISTS：`industry_link_code = chain:{码}` 或者 `LIKE segment:{码}%`。多个码是或者。主表查询，一条政策一次。`CL-*` 与非 INB → HTTP 400，不进关键词 |
| `industry_vid` | 保持等值，与 `industry_code` 同时出现时并且 |
| 未知查询字段 | `honesty.ignored_fields`。不拼进 `keyword`。`support_strength` 走这条 |

`honesty.ignored_fields` 始终返回；没有未知字段时是 `[]`。

`GET /internal/policy/search/options?industry_code=`

- `level` / `status`：`policy_base_info` 去重（`CAST AS CHAR`）
- `policy_type`：`ext1` 去重（与检索同一列）
- `nodes`：`industry_chain_node` 中 `chain_id` 等于该 INB 码的 `node_code` + `node_name`。不传码则 `nodes=[]`
- 不写死「已发布 / 公示公告 / 基础软件」等词表。`CL-*` 同样 400

不做：支持强度筛选、分析配置、门户、算子 `run()`、Java 直连 MySQL。

## 偏离说明

- 政策类型列是 `ext1`，库里没有名为 `policy_type` 的列。选项与筛选都读 `ext1`。
- 实库 `status` 去重目前只有 `"1"`，不是手写的「已发布 / 即将失效 / 已撤销」。
- 节点选项读的是产业链 DWD `industry_chain_node`，不是 `policy_industry_rel`。关联表只有已经挂上政策的节点名。

## 修改内容

- `vendor/entan-py/polan/search.py`：年份、多选或者、INB 码 EXISTS、`ignored_fields`、`list_search_options`
- `vendor/entan-py/api/policy_routes.py`：`GET /internal/policy/search` 收新参数与未知字段；`GET /internal/policy/search/options`
- `tests/test_policy_search_filter.py`：不连库的自检

## 测试结果

自检（不连库）：

```text
python -m pytest tests/test_policy_search_filter.py -q --tb=line
```

11 passed。断言：`chain:` 等值 + `segment:` 前缀、多个 INB 一条 EXISTS、`CL-*` HTTP 400、缺新参数时关键词 SQL 不变、重复参数或者、年份闭区间与空端、`support_strength` 在 `ignored_fields` 且不进 LIKE、选项 SQL 读库不去写死词表。

同仓检索回归：`test_search_industry_uses_rel_equality`、`test_search_empty_and_hit_not_5xx`、`test_search_http_stubbed_hit_and_empty`、`test_not_v1_mock_topic_path`、`test_internal_metrics_graph_symmetry` 通过。`industry_vid` 仍是等值，WHERE 里没有 LIKE。

实库（`demo_gkxlumenx_*`，2026-10-24 本机）：

| 调用 | 结果 |
|------|------|
| `industry_code=INB170106` | `total=17`，当页 17 条且 `policy_id` 不重复。与条数材料「软件与信息服务」17 条一致 |
| `industry_vid=chain:INB170106`（仅等值） | `total=9` |
| 只挂 `segment:INB170106*`、没有 `chain:INB170106` 的政策 | 8 条，全部出现在上面的 17 条里（例 `18318873`） |
| `list_search_options(INB170106)` | level `1/2/3/4`，status `1`，policy_type 13 个（来自 `ext1`），节点 6 个：`INB17010601` 基础软件 … `INB17010606` 低代码平台 |
| 只传 `ignored_fields=["support_strength"]` | 与无筛选的 `total` 同为 20000，没有被当成关键词 |

库测已跑，不是「未跑」。

## 问题清单

- 无。`status` 实库只有 `"1"` 是数据现状，不是本叶缺口。

## 遗留风险

- 全量 `tests/test_policy_job.py` 里 `test_job_timeseries_returns_board_not_harness_focus` 在本机连上库时 `M_POLICY_TOTAL_COUNT` 为 4 而不是 2：时序板在带 `industry_vid` 时会把库内政策并进夹具。本叶未改时序与算子。
- 未 commit / 未 push，CI 与 K8s 未跑。Java 透传与查询页不在本叶。

## CI/CD（必填）

- 分支：`lumen-algo-py` `dev`（本地工作区）
- commit：无（派单要求停在本地）
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：未发布
- dev 测试 URL / 命令与结果：见上节 pytest 与实库调用

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 polan，本叶未加新服务名
- traceId（dev 抽样）：无
- Tempo / Loki：无新埋点；检索失败仍走原有 warning 日志

## 涉及文件

- `repos/lumen-algo-py/vendor/entan-py/polan/search.py`
- `repos/lumen-algo-py/vendor/entan-py/api/policy_routes.py`
- `repos/lumen-algo-py/tests/test_policy_search_filter.py`
