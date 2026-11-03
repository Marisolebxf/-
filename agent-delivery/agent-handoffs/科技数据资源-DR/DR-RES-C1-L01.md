# DR-RES-C1-L01 · 科技数据资源总体视窗只读接口

| 字段 | 值 |
|---|---|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 状态 | 仍是 `in_progress`。本叶不改登记表，不标 `done` |
| 仓 | `lumen-svc-platform`，分支 `dev` |

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 只做总体视窗这一个 GET。SQL 复用 element 已有的 `{ads}` 与 `ElementDao.listOrEmpty`，没有新数据源、没有新 Maven 依赖。未用 YAGNI 跳过调用链、信封或空库键。 |

## 路径

| 面 | 路径 |
|---|---|
| 展示服务 | `GET /v1/data-ops/overview/dataset` |
| 网关 | `GET /display/v1/data-ops/overview/dataset`（`/display/**` StripPrefix=1） |
| element 内部 | `GET /v1/element/data-ops/overview-rows`（`@Inner`，Feign `@NoToken`） |

成功体是 PigX `R`：`code=0`，`msg=ok`，`data` 才是数据集。空表同样 `code=0`。element 不可达时展示侧 `code!=0`，不把故障伪装成空数据集。

## 读了哪些表

库只经 `gkxlumen.element.ads-db`（默认 `demo_gkxlumenx_ads`）。只读，无 INSERT/UPDATE/DELETE。mock 表取最新 `calc_batch_id` 且前缀 `mock_`；实体年只取前缀 `snap_`。

| 表 | 用途 |
|---|---|
| `gapfill_dr_type_slice` | 类型分布、主题分布、资源类型数、资源总量（structure 的 `value` 之和）、累计调用类型拆分 |
| `gapfill_dr_theme_library` | 主题库数量；覆盖 `bigDataCenterStats.overview` 的库数、表数、记录数、存储量 |
| `gapfill_dr_source_channel` | 来源分布、活跃度、来源分析的 `sourceTypes` / 结构趋势 / 相邻期占比 |
| `gapfill_dr_catalog_item` | `list_code=overview_source` 的明细；`list_code=access_detail` 的接入详情 |
| `gapfill_dr_api_probe` | `interfaceStatusMetrics` 与 `resourceUsageStats`（最新 `probed_at` 一组） |
| `gapfill_dr_graph_node` | `graph_code=overview_kg` 的点、分类、节点详情 |
| `gapfill_dr_resource_link` | `graph_code=overview_kg` 的边 |
| `gapfill_dr_block_json` | `overview_classify`、`semantic_theme`、`big_data_center` |
| `gapfill_dr_collection_fact` | `grain=year` 且渠道、表名、业务类型都空的 `volume` / `added`；同比在 Java 里算 |
| `gapfill_dr_usage_subject` | `subject_type=app_subject` |
| `gapfill_dr_usage_series` | `series_code=cumulative` |
| `gapfill_dr_entity_year` | `entityStock`，`origin=snap` |

未读：`gapfill_dr_theme_column`、`gapfill_dr_quality_issue`、`gapfill_dr_ingest_task`、`gapfill_dr_call_event`、`gapfill_dr_column_catalog`。未做 access / theme / application。

实体存量的 `rowCount` 不进入资源总量，也不进入年度接入的 `total`。

## data 顶层键

齐。类型上的 17 个键都在，并多出契约允许的 `entityStock`：

`overviewKPIs`、`resourceTypeDistribution`、`resourceThemeDistribution`、`resourceSourceDistribution`、`interfaceStatusMetrics`、`knowledgeGraphData`、`knowledgeGraphNodeDetails`、`knowledgeGraphCategories`、`resourceUsageStats`、`overviewAnnualAccessTrend`、`overviewSourceActivity`、`overviewSourceAnalysis`、`semanticThemeAggregation`、`resourceAccessDetailList`、`bigDataCenterStats`、`resourceAppSubjects`、`cumulativeCallAnalysis`、`entityStock`。

结构切片和主题库都没有行时，`overviewKPIs` 为 `[]`。有任一侧行时给出三项：资源类型数、资源总量（`key=total`，千分位）、主题库数量（`key=theme`）。颜色和名称用行上的列。`structureTrend.series` 在空库仍保留契约里的五个中文键，值来自行上的 `channel_name`。

## 已知空数

- `cumulativeCallAnalysis.summary.avgDaily`：累计序列没有日粒度，先为 `0`。
- `overviewSourceAnalysis.details[].reliabilityScore`：目录表没有这一列，先为 `0`。
- `resourceAppSubjects` 的 `subjectType`、`resourceType`、`purpose` 为空串，`isKeyUser` 为 `false`。表上只有名称、调用次数和占比。

## 测试

- `DataResourcesOverviewAssemblerTest`：空包根键齐、`entityStock.origin=snap`；资源总量等于 structure 之和，不包含实体存量 999；颜色取自行。
- `DataResourceOverviewControllerTest`：12 条 SQL 都走 `{ads}.gapfill_dr_*`，无 INSERT，实体年绑定 `snap_`，其余绑定 `mock_`。
- 未跑整仓 CI，未在浏览器点页面。

## CI/CD

- 分支：`dev`
- commit：`b0f8e65216327c4b3d8f7a3e1344b08d585bc411`
- 远程：该提交已在 `origin/dev`（`HEAD` 与 `origin/dev` 相同）
- pipeline / K8s：本叶未盯流水线

## 涉及文件

- `gkxlumen-display/.../controller/DataResourcesOverviewController.java`
- `gkxlumen-display/.../service/DataResourcesOverviewAssembler.java`
- `gkxlumen-display/.../feign/RemoteElementClient.java`（只加 overview-rows）
- `gkxlumen-display/src/main/resources/application-local.yml`（放行 `/v1/data-ops/**`）
- `helm/gkxlumen-platform/configs/gkxlumen-display-dev.yml`（同上）
- `gkxlumen-element/.../controller/DataResourceOverviewController.java`
- 两个测试类
