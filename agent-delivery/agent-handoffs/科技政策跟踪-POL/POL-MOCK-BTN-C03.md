# POL-MOCK-BTN-C03 · 研报读口

> 2026-11-09。只加 `POST /display/v1/policy/report/jobs`。不改任务状态，不另开接口，不改前端，不改 Nacos。C 段到此结束。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时已是 `in_progress`。本单不改任务状态，不调用 task-registry。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 照 C02 的分层走 display → `RemoteElementClient` → element GET → `gkxlumenx_gapfill` 的四张缺项表。未用 YAGNI 跳过调用链。失败日志打当前 OTel traceId。未改图、未改前端、未造 0。 |

ponytail: full

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无。本单不改存储流图 |
| 图 diff | 无 |
| 会签态 | 未改图，不抄会签态 |
| 说明 | 表结构沿用 A01 已落盘的 `stores/mysql/gapfill.md`。业务键：614 是 `policy_id` + `aspect_name`；615 是 `policy_id` + `insight_kind`；616 与 618 是 `policy_id` + `section_name`；617 是 `policy_id` + `direction_name` + `conclusion_key` |

## 问题清单

- 八张新表在 A01 执行后行数是 0。本读口无行时对应组是空列表，不造 0。灌数是 B 段，本单不写。
- 618 不建文件表，不生成 PDF / Word。正文只在 `body` 列表。
- 不读全景对标报告（`gapfill_policy_benchmark_report`），不读推演解读报告（`gapfill_policy_sim_result` 的解读段落，也不读 `gapfill_policy_assessment_report`）。

## 修改内容

调用链：浏览器 `POST /display/v1/policy/report/jobs` → 网关已有 `Path=/display/**`（GlobalFilter 剥第一段）→ `gkxlumen-display` `POST /v1/policy/report/jobs` → Feign `GET /v1/element/policy/report` → `gkxlumen-element` 只读 `{gapfill}.gapfill_policy_report_analysis`、`gapfill_policy_report_insight`、`gapfill_policy_report_body`、`gapfill_policy_report_trace`。

display 不写 mock、不连 Python、不写 nGQL、不直连库。未知枚举不查对应表。Feign 整次失败时四组都是空列表，HTTP 仍成功，不返回 501。单表读失败由 element `listOrEmpty` 把该组收成空列表，同一次响应里其它组仍返回。

### 怎么调

```http
POST /display/v1/policy/report/jobs
Content-Type: application/json

{}
```

或带过滤：

```json
{"policy_id":"<演示库政策键>","aspect_name":"实施效果","insight_kind":"观点","direction_name":"结论到原文"}
```

空体、空对象、或只给 `policy_id` 时按条件读四张表。空白字符串当没传。

### 请求字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `policy_id` | 否 | 四张表都用。条件是 `policy_id = ?` |
| `aspect_name` | 否 | 只过滤 614。闭集：实施效果、经济社会、产业影响、趋势。不在闭集则不查 `gapfill_policy_report_analysis`，`analysis` 为空列表 |
| `insight_kind` | 否 | 只过滤 615。闭集：观点、建议、风险、机遇。不在闭集则不查 `gapfill_policy_report_insight`，`insight` 为空列表 |
| `direction_name` | 否 | 只过滤 617。闭集：结论到原文、原文到结论。不在闭集则不查 `gapfill_policy_report_trace`，`trace` 为空列表 |

616 / 618 的 `section_name` 不是闭集，不作为请求枚举。正文表始终按 `policy_id` 读取。其它键忽略，不落库。

### 响应字段

外层是平台 `R`：`code`（成功为 0）、`msg`、`data`。`data` 只有四组，没有 `total`、`count`、`records`、`config`、`pdf`、`word`。

| 组 | 表 | 无行时 |
|----|----|--------|
| `analysis` | `gapfill_policy_report_analysis`（614） | `[]` |
| `insight` | `gapfill_policy_report_insight`（615） | `[]` |
| `body` | `gapfill_policy_report_body`（616，618 只读同一张） | `[]` |
| `trace` | `gapfill_policy_report_trace`（617） | `[]` |

组的值就是行列表，不是再包一层 `records`。不是数字 0。618 不单独生成文件，正文在 `body[].bodyText`。

`analysis[]` 列名由 element 转成 camelCase：

| 字段 | 表列 | 说明 |
|------|------|------|
| `id` | `id` | 自增主键 |
| `policyId` | `policy_id` | 政策业务键 |
| `aspectName` | `aspect_name` | 实施效果、经济社会、产业影响、趋势 |
| `conclusionText` | `conclusion_text` | 一句结论 |
| `isMock` | `is_mock` | 缺项标记 |
| `metricId` | `metric_id` | 可空，本表不新造指标 |
| `gapItem` | `gap_item` | 缺口项 |
| `fillMethod` | `fill_method` | 写入方式 |
| `gapfillBatchId` | `gapfill_batch_id` | 批次 |
| `generatedAt` | `generated_at` | 生成时间 |

`insight[]` 在同样的公共列之外是 `insightKind`、`bodyText`。`insightKind` 是观点、建议、风险、机遇。

`body[]` 在同样的公共列之外是 `sectionName`、`bodyText`。`sectionName` 是模块名。`bodyText` 是正文，616 与 618 都读这一列。

`trace[]` 在同样的公共列之外是 `directionName`、`conclusionKey`、`conclusionText`、`sourceExcerpt`。`directionName` 是结论到原文或原文到结论。

无行、未知枚举、读失败时：`code=0`，对应组为 `[]`。

element 对内是 `GET /v1/element/policy/report`，查询参数同名 `policy_id`、`aspect_name`、`insight_kind`、`direction_name`，`@Inner` + Feign `@NoToken`。排序：

- 614：`policy_id`，分析面闭集，`id`
- 615：`policy_id`，洞察闭集，`id`
- 616 / 618：`policy_id`，`section_name`，`id`
- 617：`policy_id`，方向闭集，`conclusion_key`，`id`

语句只有 `SELECT`，没有 `COUNT`、`INSERT`、`UPDATE`、`DELETE`。库名占位符是 `{gapfill}`。

## 测试结果

2026-11-09 本机（JDK 17.0.20.1，Maven 3.9.9，build cache 关闭）：

```text
mvn -pl gkxlumen-display,gkxlumen-element -am test "-Dtest=PolicyReportServiceTest,PolicyReportReadControllerTest" "-Dsurefire.failIfNoSpecifiedTests=false" "-Dmaven.build.cache.enabled=false"
```

- `PolicyReportServiceTest`：Tests run: 5, Failures: 0, Errors: 0
- `PolicyReportReadControllerTest`：Tests run: 6, Failures: 0, Errors: 0
- BUILD SUCCESS（20:41:19 +08:00）

覆盖：路径只有 `/jobs`；空体和空对象仍调 element；四组列表且不含 `total` / `count` / `config` / `records` / `pdf` / `word`；按政策与三个枚举过滤；未知分析面丢掉该组，洞察位置若不是列表则该组为空，正文仍在 `body`；Feign 失败四组仍是空列表；SQL 只打四张 `gapfill_policy_report_*`，不打对标报告、评估报告、推演结果、对比表、治理溯源；未知枚举不发对应 `SELECT`，三个枚举都不在闭集时只查正文表；一行落到对应组；一组空列表不清掉其它组。

## 遗留风险

- 四张表仍是空的。展示在 B 段写入之前读到的是空列表。这是允许的空态。
- 前端研报页接这条读口不在本单。
- C 段三张读口已齐。本单不再开新接口。
- 618 没有导出文件。要 PDF / Word 时页面只能用当次读到的正文，本资源不写文件。

## CI/CD（必填）

- 分支：`dev` → `origin/dev`
- lumen-svc-platform 功能提交：`ce55c8d118b4d3788ded87bb1ec229e1b6dda73f`
- lumen-svc-platform 推送：`93a47fe..ce55c8d`，`dev -> dev`。推送尖端与功能提交相同
- gkx-orchestration：本 handoff 这一次提交（推送后以 `git log -1` 为准）
- pipeline：提交后由远端 CI 触发。此处未等、未抄运行结果
- 部署：push `origin/dev` 后由现有 CI 出 display / element 镜像。本单不设 `FORCE_NACOS_REPUBLISH`
- K8s rollout：未在本机等待
- dev 调用：`POST /display/v1/policy/report/jobs`。网关已有 `id: gkxlumen-display`、`Path=/display/**`，剥第一段后命中 `/v1/policy/report/jobs`。不需要新网关路由，未改 Nacos

## 可观测性

- display、element 现有 Java Agent 会给这次 HTTP 和 Feign 调用建 span
- Feign 失败日志：`policy report jobs feign status={} traceId={}`。traceId 取 `Span.current()`，无有效 span 时记 `no-trace`
- element `listOrEmpty` 读表失败已有 warn，并返回空列表。失败的那一组是空列表，其它组仍在同一次响应里

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 调用链 前端 → Java → element，不越层到 Python | 符合。display 只调 `RemoteElementClient` |
| Java 不做 NLP / 不写 nGQL | 符合。只读缺项表 |
| D16 缺项只读 `gkxlumenx_gapfill.gapfill_*` | 符合。SQL 使用 `{gapfill}` |
| D18 接口不返回写死 mock，无行不造 0 | 符合。四组是列表，无计数字段 |
| 不改 Nacos / 不整批重发 | 符合。未改 helm 配置，未发 dataId |
| D12 不把 demo 并进 lumen | 符合。只改 `lumen-svc-platform` |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 190000（估算，含本会话上下文，非控制台精确值） |
| model_used | `grok-4.7` |
| actual_cost | 0.65（按本单量级估算，美元） |
| cost_warn | `green` |

## 涉及文件

- `repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/PolicyReportController.java`
- `repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/service/PolicyReportService.java`
- `repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/feign/RemoteElementClient.java`
- `repos/lumen-svc-platform/gkxlumen-display/src/test/java/com/topcomm/gkxlumen/display/service/PolicyReportServiceTest.java`
- `repos/lumen-svc-platform/gkxlumen-element/src/main/java/com/topcomm/gkxlumen/element/controller/PolicyReportReadController.java`
- `repos/lumen-svc-platform/gkxlumen-element/src/test/java/com/topcomm/gkxlumen/element/controller/PolicyReportReadControllerTest.java`
- 本 handoff
