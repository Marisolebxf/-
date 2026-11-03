# DR-RES-C3-L01 · 科技数据资源主题视窗只读接口

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
| 说明 | 只做主题视窗这一个对外 GET。SQL 复用 element 已有的 `{ads}` 与 `ElementDao.listOrEmpty`，没有新数据源、没有新 Maven 依赖。未用 YAGNI 跳过调用链、信封或空库键。未做 application/dataset，未改总体视窗和接入视窗的响应形状。 |

## 路径

| 面 | 路径 |
|---|---|
| 展示服务 | `GET /v1/data-ops/theme/dataset` |
| 网关 | `GET /display/v1/data-ops/theme/dataset`（`/display/**` StripPrefix=1，沿用已有放行 `/v1/data-ops/**`） |
| element 内部 | `GET /v1/element/data-ops/theme-rows`（`@Inner`，Feign `@NoToken`） |

成功体是 PigX `R`：`code=0`，`msg=ok`，`data` 才是数据集。空表同样 `code=0`，数组 `[]`，数字 `0`，`recordCountLabel` / `storageLabel` 为 `"0"`，对象键仍在。element 返回 `code!=0` 或 Feign 失败时，展示侧 `code!=0`，`data` 为 null，不把故障伪装成空数据集。

## 读了哪些表

库只经 `gkxlumen.element.ads-db`（默认 `demo_gkxlumenx_ads`）。只读，无 INSERT/UPDATE/DELETE。mock 行取最新 `calc_batch_id` 且前缀 `mock_`。列目录取最新 `calc_batch_id` 且前缀 `snap_`。

| 表 | 用途 |
|---|---|
| `gapfill_dr_theme_library` | `themeDatabases`；`themeDatabaseCount` = 行数；`tableCount` = `table_count` 之和；`recordCountLabel` = `record_yi` 之和；`storageLabel` = `storage_tb` 之和 |
| `gapfill_dr_theme_column` | `themeDatabases[].tableSchemas`。只这一张 |
| `gapfill_dr_graph_node` | `datasetRelationData.nodes`，`graph_code=theme_relation` |
| `gapfill_dr_resource_link` | `datasetRelationData.links`，`graph_code=theme_relation` |
| `gapfill_dr_column_catalog` | `columnCatalog`，`origin=snap`。不并进 `tableSchemas` |

四个总数在展示侧按读到的主题库行汇总，没有写死，也没有另存一份总数。

## data 顶层键

齐。`DataResourcesThemeDataset` 的 6 个键都在，并多出契约允许的 `columnCatalog`：

`themeDatabaseCount`、`tableCount`、`recordCountLabel`、`storageLabel`、`themeDatabases`、`datasetRelationData`、`columnCatalog`。

`recordCountLabel`、`storageLabel` 是纯数字字符串，不带「亿条」「TB」。`themeDatabases[]` 与接入视窗同一套卡片字段，`origin=mock`。`datasetRelationData` 根和每个点、边为 `origin=mock`。`columnCatalog` 为 `{ origin: "snap", rows: [...] }`，行内是 `tableName`、`columnName`、`ordinal`、`dataType`、`columnComment`，行上不再加 `origin`。

## 已知空数

- `themeDatabases` 的 `publishTime`、`updateTime`、`partition`、`contactPerson`、`collectTime`、`dataStructure` 表上没有列，写空串。`records`、`size` 是 `record_yi`、`storage_tb` 的数字字符串。
- 关系图节点按契约只有 `id`、`name`、`category`、`desc`、`size`。名称和类别取行上的 `name`、`category`。节点表上的 `color` 不写入响应，避免多出类型没有的键，也没有另做调色板。
- `columnCatalog.rows` 的子键沿 `gapfill_dr_column_catalog` 的列，留在该对象内。现有页面忽略这个键。

## 测试

- `DataResourcesThemeAssemblerTest`：空包 7 个根键都在，标签为 `"0"`；总数等于行汇总；`tableSchemas` 只有主题字段行；`doi` 只出现在 `columnCatalog`。
- `DataResourcesThemeControllerTest`：element `code=0` 时空包仍成功且键在；Feign 失败或 element `code!=0` 时展示侧 `code!=0` 且 `data` 为 null。
- `DataResourceThemeControllerTest`：5 条 SQL 都走 `{ads}.gapfill_dr_*`，四条绑定 `mock_`，列目录绑定 `snap_`，两条 `graph_code=theme_relation`，无写语句，列目录 SQL 不含主题字段表。
- 本机没有 `java` / `mvn`，按派单未跑编译。编译交给 GitLab CI。

## CI/CD

- 分支：`dev`
- 实现 commit：`70c0b36e2f3bc8c3f18a8e44f3a9381f0ef64a88`
- Feign 方法 `dataOpsThemeRows` 已在并行提交 `896956ecbcfa65cdd6062862c3feb2b5f366fbd6` 里（该提交带上了当时工作区中的这一方法）。本叶其余代码在 `70c0b36`
- 推送：成功。`896956e..70c0b36` 已在 `origin/dev`
- pipeline / K8s：本叶未盯流水线

## 涉及文件

- `gkxlumen-display/.../controller/DataResourcesThemeController.java`
- `gkxlumen-display/.../service/DataResourcesThemeAssembler.java`
- `gkxlumen-display/.../feign/RemoteElementClient.java`（只加 `theme-rows`；该方法随 `896956e` 先到 `origin/dev`）
- `gkxlumen-element/.../controller/DataResourceThemeController.java`
- 三个测试类

未改总体视窗、接入视窗的组装与 SQL。未改 `application-local.yml` 与 helm：`/v1/data-ops/**` 已放行。未提交 `gkx-orchestration`，未改 task-registry。
