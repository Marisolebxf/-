# DR-RES-C4-L01 · 科技数据资源应用视窗只读接口

| 字段 | 值 |
|---|---|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 状态 | 仍是 `in_progress`。本叶不改登记表，不标 `done` |
| 仓 | `lumen-svc-platform`，分支 `dev` |
| ponytail | `full` |

ponytail: full

只做应用视窗这一个对外 GET。SQL 复用 element 已有的 `{ads}` 与 `ElementDao.listOrEmpty`，没有新数据源、没有新 Maven 依赖。未用 YAGNI 跳过调用链、信封或空库键。未改总体、接入、主题三个 dataset 的响应形状。

## 路径

| 面 | 路径 |
|---|---|
| 展示服务 | `GET /v1/data-ops/application/dataset` |
| 网关 | `GET /display/v1/data-ops/application/dataset`（`/display/**` StripPrefix=1，沿用已有放行 `/v1/data-ops/**`） |
| element 内部 | `GET /v1/element/data-ops/application-rows`（`@Inner`，Feign `@NoToken`） |

成功体是 PigX `R`：`code=0`，`msg=ok`，`data` 才是数据集。空表同样 `code=0`，数组 `[]`，数字 `0`，对象键仍在。element 返回 `code!=0` 或 Feign 失败时，展示侧 `code!=0`，`data` 为 null，不把故障伪装成空数据集。

页面实时监控用本响应的 `usageCallTrend`（`dates`、`calls`、`users`）在浏览器里走表。没有另做轮询接口，没有告警字段。

## 读了哪些表

库只经 `gkxlumen.element.ads-db`（默认 `demo_gkxlumenx_ads`）。只读，无 INSERT/UPDATE/DELETE。mock 行取最新 `calc_batch_id` 且前缀 `mock_`。

| 表 | 用途 |
|---|---|
| `gapfill_dr_usage_subject` | `asset` → `assetRanking`；`supplier` → `supplierStats` 并参与 `supplierRegionGroups`；`region` → 区域分组的调用量；`demander` → `demanderStats`；`business` → `businessApplicationStats` 与部门分组。应用系统数 = 业务行 `user_count` 之和 |
| `gapfill_dr_usage_series` | `usage_call` → `usageCallTrend`，最近一期 `call_count` 为资产调用总量；`usage_detail` → `usageDetailTrend`；`theme_call` / `supplier_call` / `demander_call` / `business_call` → 四条多线趋势。`themeCallBasicInfo` 用 `theme_call` 最近一段 |
| `gapfill_dr_call_event` | `supplier_detail` → `supplierCallDetails`，月份去重排序为 `supplierCallPeriods`；`app_log` → `businessApplicationCallLogs`，并给主题基本信息补接口名和业务系统；`column_usage` → `dataUsageDetails`；`user_track` → `callUserTracking` |

未读 `gapfill_dr_collection_fact`：方案第 5.4 节本页 KPI 只有调用总量和应用系统数，归集量不进 `applicationKPIs`。未读 `gapfill_dr_entity_year`，响应里没有 `entityStock`。未读 `gapfill_dr_api_probe`，不造告警。

调用总量没有序列时，改为资产行 `call_count` 之和；资产行也没有时，改为 `app_subject` 之和。名称取行上的 `name` / `series_name` / `subject_name` / `theme_name` / `app_name` / `field_name`。这三张表没有颜色列，响应不另做调色板。

## data 顶层键

齐。`DataResourcesApplicationDataset` 的 19 个键都在：

`applicationKPIs`、`usageCallTrend`、`assetRanking`、`supplierStats`、`supplierRegionGroups`、`supplierCallDetails`、`supplierCallPeriods`、`demanderStats`、`businessApplicationStats`、`businessApplicationDeptGroups`、`businessApplicationCallLogs`、`dataUsageDetails`、`usageDetailTrend`、`themeCallTrend`、`themeCallBasicInfo`、`supplierCallTrend`、`demanderCallTrend`、`businessCallTrend`、`callUserTracking`。

`usageCallTrend` 含 `dates`、`calls`、`users`。空库这三者和 `usageDetailTrend` 的 `months`/`calls`、四条多线趋势的 `months`/`datasets` 都是 `[]`。`applicationKPIs` 种子没有 `key`，响应不造 `key`。有行时 KPI 与列表带 `origin=mock`，趋势对象根上也写 `origin=mock`。

## 已知空数

表上没有的字符串留空，数字留 0，不把别的列改名填进去：

- 资产排行的 `dataType`、`appSubject`、`deployLocation`、`usageCycle`、`businessType`、`usageUnit`、`lastActiveDate` 为空串，`businessModules` 为 `[]`。`category` 用行上的 `theme_name`。
- 供应方 `resourceCount` 为 0。区域分组的 `resourceCount` 以及部门下的 `resourceCount` 为 0。有 `region` 行时，区域 `totalCalls` 用该行，不加总供应方。
- 供应明细 `businessType`、需求方 `businessType`/`projectTeam`、业务应用 `businessType`/`status` 为空串。需求方 `activeDays`、`avgDaily` 为 0。
- 调用日志 `resource` 为空串，`durationMs` 为 0。用户、结果、应用名、时间用事件行上的列。
- 字段使用 `tableName`、`columnType`、`columnDesc` 为空串，`subscriberCount` 为 0。`columnName` 用 `field_name`。
- 主题基本信息 `callFreq` 为空串。`callTime` 是该序列最近一期的 `period_label`。`callInterface`、`businessSystems` 来自同一主题的 `app_log`。
- 用户追踪 `userId` 用行 `id`，`ipAddress` 为空串。不编 `u001` 或 IP。

## 测试

- `DataResourcesApplicationAssemblerTest`：空包 19 个根键都在，`usageCallTrend` 三数组为空，无 `entityStock`。有行时调用总量取 `usage_call` 最近一期并算涨跌，应用系统数为业务行 `user_count` 之和，区域调用量不被供应方加总盖掉。没有序列时调用总量回退到资产行之和。
- `DataResourcesApplicationControllerTest`：element `code=0` 时空包仍成功且键在；Feign 失败或 element `code!=0` 时展示侧 `code!=0` 且 `data` 为 null。
- `DataResourceApplicationControllerTest`：3 条 SQL 都走 `{ads}.gapfill_dr_*`，绑定 `mock_`，无写语句，不含 `entity_year`、`collection_fact`、`api_probe`。
- 本机没有 `java` / `mvn`，按派单未跑编译。编译交给 GitLab CI。

## CI/CD

- 分支：`dev`
- 实现 commit：`3c5d8d6ca17d80133845cdbc135b4505f576f4c6`
- 推送：成功。`70abaa7..3c5d8d6` 已在 `origin/dev`
- pipeline / K8s：本叶未盯流水线

## 涉及文件

- `gkxlumen-display/.../controller/DataResourcesApplicationController.java`
- `gkxlumen-display/.../service/DataResourcesApplicationAssembler.java`
- `gkxlumen-display/.../feign/RemoteElementClient.java`（只加 `application-rows`）
- `gkxlumen-element/.../controller/DataResourceApplicationController.java`
- 三个测试类

未改总体、接入、主题视窗的组装与 SQL。未改 `application-local.yml` 与 helm：`/v1/data-ops/**` 已放行。未提交 `gkx-orchestration`，未改 task-registry。
