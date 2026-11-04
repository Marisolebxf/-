# POL-L2-DS11-BE-L01 · 政策分析评价 · 后端读面接线 · handoff

- 任务：`POL-L2-DS11-BE-L01`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 执行：`agent:api-agent`
- 仓：`lumen-svc-platform`，commit `e8471c0`（`origin/dev`），前序 `490071b`（counts/shells 壳表 + jobs 白名单）、`30a3192`（白名单补 `policy_intensity`）为上一实例交付，本单未重写。
- 强度：ponytail full
- 上游：`sdd/l2/POL-L2-DS11-VIZ-API.md`（219–222）、`sdd/l2/POL-L2-DS11-PLAN-ARCH.md`（227–231）

## 范围与实现

只补派单点名的缺口，已交付部分（counts 读 `ads.policy_effect` region_gap、shells 壳表、白名单八键 + `policy_intensity`）不动。

### 缺口 1 · 219 趋势段（jobs kind=趋势）

- 前端 → 网关 → `gkxlumen-display` `POST /display/v1/policy/evaluation/jobs`（body `kind=趋势`）→ Feign → `gkxlumen-element` `GET /v1/element/policy/evaluation/trend` → `gkxlumenx_gapfill.gapfill_policy_eval_trend`。
- 拣行键 `switch_dim`（闭集：时间/区域/类别）+ `metric_name IN (...)`（评估指标名，非 metric_id）。display 侧逐维读取合并，未出现的维不读；`switch` 或 `metric` 空则图空。
- **不建任务、不转发异步服务、不调 Python、不进 `PolicyAnalysisTypes` 白名单**。无行则 `records` 空，HTTP 成功，不返回 501。

### 缺口 2 · 220 分区段（jobs kind=分区）

- 同一条 jobs 资源另一次请求（`kind=分区`）→ element `GET /v1/element/policy/evaluation/partition` → `gapfill_policy_eval_partition`。
- 拣行键 `object_kind`（闭集：地区/行业/目标群体）；`allocation`（资源投向）可空，传入时在 Java 内存过滤 `resource_direction`（空投向行不返回）。柱状与热力共用同一批行。
- 同样不建任务。`subject` 不在三选一或缺失则空，不补默认对象。

### 缺口 3 · 227–229 方案五叶（jobs kind=方案对照/参数模拟/路径与风险）

- element `GET /v1/element/policy/evaluation/scheme` → `gapfill_policy_eval_scheme`。
- 拣行键 `row_kind`（闭集：方案对照/参数模拟/路径与风险/互动意见），再按 `scheme_name` 收窄（227 可空读全部，228/229 必选），228 另按 `param_band` 收窄。
- 同步非 Job，**不进异步白名单**（未加 `policy_scheme` 等任何键）。路径与风险行的 `metric_id` 原样带出已有 `M_POLICY_DS_11_POLICY_EVAL_015`，未新造、未改 D4。

### 缺口 4 · 230/231 shells 读方案表

- `GET /display/v1/policy/evaluation/shells?kind=互动意见&scheme_name=…`：element 读 scheme 表意见行。**请求不插入新意见**（只读）。
- `?kind=方案报告`：同一次读方案对照行（`records`）+ 意见行（`opinions`），导出内容从当次读到的行生成，**不写对象存储、不灌文件**。
- **不带 `kind` 时维持解读分册的壳表读法不变**（旧语义零破坏）。

### 缺口 5 · 221 不加资源

- 未新开任何 `/display/v1/policy` 路由；`jobs`/`shells` 均为既有资源上按种类分发。

### kind 与 sub_type 互斥

- 同一次 `jobs` 同时出现 `kind` 与 `sub_type`（含别名 `analysisType`/`task_type`）：不建任务、不读趋势/分区/方案表，`records` 空，HTTP 成功（VIZ-API §2 要求）。
- 闭集外的 `kind` 同样落空。

## 产物清单

| 文件 | 变更 |
|---|---|
| `gkxlumen-display/.../controller/PolicyEvaluationController.java` | `shells` 加可选 `kind`/`scheme_name` 参数 |
| `gkxlumen-display/.../feign/RemoteElementClient.java` | 加 3 个 `@NoToken` Feign 方法（trend/partition/scheme） |
| `gkxlumen-display/.../service/PolicyEvaluationService.java` | `jobs` 顶部 `kind` 同步分支；`shells(kind, schemeName)` 分发；`schemeReport` 合并两段读 |
| `gkxlumen-display/.../service/PolicyEvaluationServiceTest.java` | 13 tests（含 6 个新读面用例） |
| `gkxlumen-element/.../controller/PolicyGapfillController.java` | 3 个 `@Inner` 只读端点 + `TREND/PARTITION/SCHEME_SQL` + `inMarks` |
| `gkxlumen-element/.../controller/PolicyGapfillEvaluationTest.java` | 4 tests（含 3 个新读面用例） |

## 验收证据

- 编译：`mvn -pl gkxlumen-display,gkxlumen-element,gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz -am compile` 通过（JDK 17.0.20+1 / Maven 3.9.9，`-Dmaven.build.cache.enabled=false`）。
- 测试（三模块联合 `mvn test` 全绿）：
  - `PolicyEvaluationServiceTest` 13 通过 0 失败：趋势逐维合并且不建任务、缺 metric 为空、分区闭集 + 投向过滤、kind+sub_type 同传为空且零调用、方案三 kind 读表不走异步、缺方案为空、shells kind 分发（意见/报告两段/模板选用空）。
  - `PolicyGapfillEvaluationTest` 4 通过：趋势 SQL 只含 `switch_dim = ? AND metric_name IN (?,?)` 且绑定值正确、分区 kind 绑定 + 投向内存过滤、方案 row_kind 绑定 + scheme/param_band 收窄 + 闭集外为空；全部断言 `select` 起头、无 `insert/update/delete`。
  - `PolicyGapfillControllerTest` 6、`PolicyPanoramaServiceTest` 3、`PolicyAnalysisTypesTest` + `PolicyAnalysisAdapterImplTest`（回归）全过。
- 数据已在库：trend 44 行、partition 41 行、scheme 19 行、shell 7 行（灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01` / `POL-L2-DS11-PLAN-GAPFILL-L01` 已 apply），接线即可验。
- **联调确认**：联调通过——element 三个新端点 SQL 走 `{gapfill}` 占位（`ElementDao.listOrEmpty` 表缺失时回空列表不抛错），display Feign `@NoToken`↔`@Inner` 配对与既有九个端点同模式；三模块联合编译 + 全部单测绿后推送 `origin/dev`（`c2ccd1c..e8471c0`），CI 流水线随后编译验证。

## 明确不做（与派单一致）

- display 不直连 Python、不直连库；不写 nGQL；不改 D4；不新造 metric_id。
- 空态诚实：无行则空，不返回 501。
- 旧键 `policy_focus` 等白名单语义不改；`/topicAsync/**` 不动；不复用 `/topic/v1/policy` 作浏览器入口。
- 222 模板选用：`kind=模板选用` 落到空（表未建、未灌，属 VIZ-GAPFILL 单范围）。
- 231 导出只从当次读到的行生成，不写对象存储。

## 架构合规自检

1. 调用链：前端 → 网关 → display → element → 缺项表。display 不直连库/Python。✅
2. 算法只在 Python：本单纯只读接线，无算法。✅
3. D16/D18：读 `gkxlumenx_gapfill` 的 `gapfill_` 前缀表，接口只读表不返回写死 mock。✅
4. 数据血缘：未新造 metric_id；路径与风险行带出既有 `M_POLICY_DS_11_POLICY_EVAL_015`；`metric_id`/`gap_item`/`is_mock` 等追溯列全部透出。✅
5. 空 `metric_name`（非 metric_id）作为拣行键，与 seed 脚本 201–232 行列一致；scheme 列与 `seed_gapfill_policy_eval_scheme.py` 354–382 行一致。✅

## 遗留

- 222 模板选用表（`gapfill_policy_eval_template`）未建未灌，`kind=模板选用` 现为空（数据单范围）。
- 221 结构关联图：按契约不设资源，消费第 7 项已有子图，本单未触碰。
