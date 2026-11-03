# DR-RES-C2-L01 · 科技数据资源接入视窗只读接口

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
| 说明 | 只做接入视窗这一个对外 GET。SQL 复用 element 已有的 `{ads}` 与 `ElementDao.listOrEmpty`，没有新数据源、没有新 Maven 依赖。未用 YAGNI 跳过调用链、信封或空库键。未做 theme/dataset、application/dataset，未改总体视窗响应形状。 |

## 路径

| 面 | 路径 |
|---|---|
| 展示服务 | `GET /v1/data-ops/access/dataset` |
| 网关 | `GET /display/v1/data-ops/access/dataset`（`/display/**` StripPrefix=1，沿用已有放行 `/v1/data-ops/**`） |
| element 内部 | `GET /v1/element/data-ops/access-rows`（`@Inner`，Feign `@NoToken`） |

成功体是 PigX `R`：`code=0`，`msg=ok`，`data` 才是数据集。空表同样 `code=0`，数组 `[]`，对象键仍在。element 返回 `code!=0` 或 Feign 失败时，展示侧 `code!=0`，`data` 为 null，不把故障伪装成空数据集。

## 读了哪些表

库只经 `gkxlumen.element.ads-db`（默认 `demo_gkxlumenx_ads`）。只读，无 INSERT/UPDATE/DELETE。八条 SQL 都取最新 `calc_batch_id` 且前缀 `mock_`。

| 表 | 用途 |
|---|---|
| `gapfill_dr_collection_fact` | 接入趋势（`added` / `updated`）、渠道分时、分业务、带表名的历史明细、`update_cycle` |
| `gapfill_dr_ingest_task` | 完成率按 `ingest_method` × `status` 计数；待处理任务 = `pending` |
| `gapfill_dr_quality_issue` | 问题列表；类别、数据群、类型、等级、渠道、月份由行计数。颜色用行上的 `color` |
| `gapfill_dr_source_channel` | `channel_group=srs_source` 的最新月，作渠道汇总 |
| `gapfill_dr_catalog_item` | `list_code=access_source` 的明细 |
| `gapfill_dr_block_json` | `block_code=partition` |
| `gapfill_dr_theme_library` | `themeDatabases` 卡片 |
| `gapfill_dr_theme_column` | `themeDatabases[].tableSchemas` |

未读：`gapfill_dr_type_slice`、`gapfill_dr_usage_*`、`gapfill_dr_call_event`、`gapfill_dr_api_probe`、`gapfill_dr_graph_node`、`gapfill_dr_resource_link`、`gapfill_dr_entity_year`、`gapfill_dr_column_catalog`。

完成率的 `total` / `completed` / `inProgress` / `pending`、问题统计六个数组、历史看板的 `summary` 和 `trend`，都是读到的行当场汇总，没有另存一份总数。

## data 顶层键

齐。`DataResourcesAccessDataset` 的 11 个键都在：

`accessKPIs`、`resourceAccessTrend`、`accessCompletionData`、`accessSourceAnalysis`、`problemResources`、`problemResourceStats`、`partitionData`、`themeDatabases`、`historyAccessRecords`、`historyAccessDashboard`、`updateCycleStats`。

本月接入、问题、任务三条来源都没有行时，`accessKPIs` 为 `[]`，不造 `key`。有任一侧行时给出三项，`origin=mock`。`resourceAccessTrend` 的 `months`、`datasets` 是月度副本。`byTime.series` 空库仍有 `科研院所`、`企业`、`第三方平台`。分区 `typeDist` 空缺时补 `结构化`、`非结构化`、`半结构化`、`实时流`，值为 0。

## 已知空数

- `accessKPIs` 的涨跌只在能比相邻两期时才有。待处理任务没有历史期，不写 `trend` / `change`。
- 趋势序列名用指标列 `added`、`updated`，顺序固定为新增在前、更新在后。页面图按下标取这两条。
- `byBizType` 的三个渠道键只累加 `channel_name` 命中的行。渠道为空的业务行三个键为 0，不把 `row_count` 摊进任一渠道。
- 渠道汇总的 `bizTypes` 用 `sample_tags`。这是来源渠道上唯一的字符串数组。
- `themeDatabases` 的 `publishTime`、`updateTime`、`partition`、`contactPerson`、`collectTime`、`dataStructure` 表上没有列，写空串。`records`、`size` 是 `record_yi`、`storage_tb` 的数字字符串。
- 历史明细的 `updateTime` 没有列，写空串。异常类型和更新状态的 `color` 写空串：`collection_fact` 没有颜色列。名称用 `status`、`anomaly_type` 原文。
- `updateCycleStats.avgCycle` 取该渠道 `update_cycle` 出现最多的值；次数相同保留行序上先出现的那个。`successRate` 和 `trend` 按 `status=success` 从这些行算出。

## 测试

- `DataResourcesAccessAssemblerTest`：空包 11 个根键都在；完成率、问题数、历史看板等于行数，不读单独的总数字段；颜色取问题行；分区补四个 `typeDist` 键且区域项没有 `topResource`。
- `DataResourcesAccessControllerTest`：element `code=0` 时空包仍成功且键在；Feign 失败或 element `code!=0` 时展示侧 `code!=0` 且 `data` 为 null。
- `DataResourceAccessControllerTest`：8 条 SQL 都走 `{ads}.gapfill_dr_*`，绑定 `mock_`，无写语句，不含实体年。
- 本机没有 `java` / `mvn`，按派单未跑编译。编译交给 GitLab CI。

## CI/CD

- 分支：`dev`
- 实现 commit：`5944f1363620e2504c8841ec8f4c6272abafebfa`
- 推送：成功。远端当时已有 `e298d0e`，`git pull --no-rebase origin dev` 后合并提交 `ae65afe810b10c88a3f69ed08b12de89b0ea8a9a` 已在 `origin/dev`
- pipeline / K8s：本叶未盯流水线

## 涉及文件

- `gkxlumen-display/.../controller/DataResourcesAccessController.java`
- `gkxlumen-display/.../service/DataResourcesAccessAssembler.java`
- `gkxlumen-display/.../feign/RemoteElementClient.java`（只加 access-rows）
- `gkxlumen-element/.../controller/DataResourceAccessController.java`
- 三个测试类

未改总体视窗的组装与 SQL。未改 `application-local.yml` 与 helm：`/v1/data-ops/**` 已放行。
