# POL-MOCK-BTN-C02 · 对比读口

> 2026-11-09。只加 `POST /display/v1/policy/compare/jobs`。不改任务状态，不开始 C03，不改前端，不改 Nacos。

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
| 说明 | 照 C01 的分层走 display → `RemoteElementClient` → element GET → `gkxlumenx_gapfill` 的三张缺项表。未用 YAGNI 跳过调用链。失败日志打当前 OTel traceId。未改图、未改前端、未造 0。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无。本单不改存储流图 |
| 图 diff | 无 |
| 会签态 | 未改图，不抄会签态 |
| 说明 | 表结构沿用 A01 已落盘的 `stores/mysql/gapfill.md`。业务键：610 是 `policy_id_a` + `policy_id_b` + `relation_name`；611 是 `chart_kind` + `policy_id_a` + `policy_id_b` + `item_name`；613 是 `policy_id_a` + `policy_id_b` + `summary_kind` |

## 问题清单

- 八张新表在 A01 执行后行数是 0。本读口无行时对应组是空列表，不造 0。灌数是 B 段，本单不写。
- 612 不建表。请求里的枚举和 `policy_id` 只当过滤条件，响应里没有配置体。
- 对比页统计仍走已有 `GET compare/stats`，本资源不读全景分布，也不写件数。

## 修改内容

调用链：浏览器 `POST /display/v1/policy/compare/jobs` → 网关已有 `Path=/display/**`（GlobalFilter 剥第一段）→ `gkxlumen-display` `POST /v1/policy/compare/jobs` → Feign `GET /v1/element/policy/compare` → `gkxlumen-element` 只读 `{gapfill}.gapfill_policy_xcmp`、`gapfill_policy_xcmp_viz`、`gapfill_policy_xcmp_summary`。

display 不写 mock、不连 Python、不写 nGQL、不直连库。未知枚举不查对应表。Feign 整次失败时三组都是空列表，HTTP 仍成功，不返回 501。单表读失败由 element `listOrEmpty` 把该组收成空列表，同一次响应里其它组仍返回。

### 怎么调

```http
POST /display/v1/policy/compare/jobs
Content-Type: application/json

{}
```

或带过滤：

```json
{"policy_id":"<演示库政策键>","relation_name":"共性","chart_kind":"柱","summary_kind":"核心结论"}
```

空体、空对象、或只给 `policy_id` 时按条件读三张表。空白字符串当没传。

### 请求字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `policy_id` | 否 | 三张表都用。命中 `policy_id_a` 或 `policy_id_b` 都算，条件是 `(policy_id_a = ? OR policy_id_b = ?)` |
| `relation_name` | 否 | 只过滤 610。闭集：共性、差异、互补、冲突。不在闭集则不查 `gapfill_policy_xcmp`，`xcmp` 为空列表 |
| `chart_kind` | 否 | 只过滤 611。闭集：对比表、柱、雷达。不在闭集则不查 `gapfill_policy_xcmp_viz`，`viz` 为空列表 |
| `summary_kind` | 否 | 只过滤 613。闭集：对比摘要、核心结论。不在闭集则不查 `gapfill_policy_xcmp_summary`，`summary` 为空列表 |

612 没有表，也没有响应字段。上面三个枚举和 `policy_id` 就是可选过滤。其它键忽略，不落库。

### 响应字段

外层是平台 `R`：`code`（成功为 0）、`msg`、`data`。`data` 只有三组，没有 `total`、`count`、`records`、`config`。

| 组 | 表 | 无行时 |
|----|----|--------|
| `xcmp` | `gapfill_policy_xcmp`（610） | `[]` |
| `viz` | `gapfill_policy_xcmp_viz`（611） | `[]` |
| `summary` | `gapfill_policy_xcmp_summary`（613） | `[]` |

组的值就是行列表，不是再包一层 `records`。不是数字 0。

`xcmp[]` 列名由 element 转成 camelCase：

| 字段 | 表列 | 说明 |
|------|------|------|
| `id` | `id` | 自增主键 |
| `policyIdA` | `policy_id_a` | 字典序较小的政策业务键 |
| `policyIdB` | `policy_id_b` | 字典序较大的政策业务键 |
| `relationName` | `relation_name` | 共性、差异、互补、冲突 |
| `bodyText` | `body_text` | 一句中文 |
| `isMock` | `is_mock` | 缺项标记 |
| `metricId` | `metric_id` | 可空，本表不新造指标 |
| `gapItem` | `gap_item` | 缺口项 |
| `fillMethod` | `fill_method` | 写入方式 |
| `gapfillBatchId` | `gapfill_batch_id` | 批次 |
| `generatedAt` | `generated_at` | 生成时间 |

`viz[]` 在同样的公共列之外是 `chartKind`、`policyIdA`、`policyIdB`、`itemName`、`compareValue`。`compareValue` 来自 `compare_value`，是对照数，不是新指标，也不当件数。

`summary[]` 在同样的公共列之外是 `policyIdA`、`policyIdB`、`summaryKind`、`bodyText`。`summaryKind` 是对比摘要或核心结论。

无行、未知枚举、读失败时：`code=0`，对应组为 `[]`。

element 对内是 `GET /v1/element/policy/compare`，查询参数同名 `policy_id`、`relation_name`、`chart_kind`、`summary_kind`，`@Inner` + Feign `@NoToken`。排序：

- 610：`policy_id_a`，`policy_id_b`，关系闭集，`id`
- 611：图种闭集，`policy_id_a`，`policy_id_b`，`item_name`，`id`
- 613：`policy_id_a`，`policy_id_b`，摘要闭集，`id`

语句只有 `SELECT`，没有 `COUNT`、`INSERT`、`UPDATE`、`DELETE`。库名占位符是 `{gapfill}`。

## 测试结果

2026-11-09 本机（JDK 17.0.20.1，Maven 3.9.9，build cache 关闭）：

```text
mvn -pl gkxlumen-display,gkxlumen-element -am test "-Dtest=PolicyCompareServiceTest,PolicyCompareReadControllerTest" "-Dsurefire.failIfNoSpecifiedTests=false" "-Dmaven.build.cache.enabled=false"
```

- `PolicyCompareServiceTest`：Tests run: 5, Failures: 0, Errors: 0
- `PolicyCompareReadControllerTest`：Tests run: 6, Failures: 0, Errors: 0
- BUILD SUCCESS（20:30:59 +08:00）

覆盖：路径只有 `/jobs`；空体和空对象仍调 element；三组列表且不含 `total` / `count` / `config` / `records`；按政策与三个枚举过滤；未知关系丢掉该组，图种位置若不是列表则该组为空；Feign 失败三组仍是空列表；SQL 只打三张 `gapfill_policy_xcmp*`；未知枚举不发对应 `SELECT`；一行落到对应组；一组空列表不清掉其它组。

## 遗留风险

- 三张表仍是空的。展示在 B 段写入之前读到的是空列表。这是允许的空态。
- 前端对比页接这条读口不在本单。
- 研报 `report/jobs` 是 C03，本单未做。
- 612 没有保存入口。本资源只消费当次请求里的过滤条件。

## CI/CD（必填）

- 分支：`dev` → `origin/dev`
- lumen-svc-platform 功能提交：`911dd666200b42dee50afa4169c7ed0b36e21501`
- lumen-svc-platform 推送：`33b22eb..911dd66`，`dev -> dev`。推送尖端与功能提交相同
- gkx-orchestration：本 handoff 这一次提交（推送后以 `git log -1` 为准）
- pipeline：提交后由远端 CI 触发。此处未等、未抄运行结果
- 部署：push `origin/dev` 后由现有 CI 出 display / element 镜像。本单不设 `FORCE_NACOS_REPUBLISH`
- K8s rollout：未在本机等待
- dev 调用：`POST /display/v1/policy/compare/jobs`。网关已有 `id: gkxlumen-display`、`Path=/display/**`，剥第一段后命中 `/v1/policy/compare/jobs`。不需要新网关路由，未改 Nacos

## 可观测性

- display、element 现有 Java Agent 会给这次 HTTP 和 Feign 调用建 span
- Feign 失败日志：`policy compare jobs feign status={} traceId={}`。traceId 取 `Span.current()`，无有效 span 时记 `no-trace`
- element `listOrEmpty` 读表失败已有 warn，并返回空列表。失败的那一组是空列表，其它组仍在同一次响应里

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 调用链 前端 → Java → element，不越层到 Python | 符合。display 只调 `RemoteElementClient` |
| Java 不做 NLP / 不写 nGQL | 符合。只读缺项表 |
| D16 缺项只读 `gkxlumenx_gapfill.gapfill_*` | 符合。SQL 使用 `{gapfill}` |
| D18 接口不返回写死 mock，无行不造 0 | 符合。三组是列表，无计数字段 |
| 不改 Nacos / 不整批重发 | 符合。未改 helm 配置，未发 dataId |
| D12 不把 demo 并进 lumen | 符合。只改 `lumen-svc-platform` |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 220000（估算，含本会话上下文，非控制台精确值） |
| model_used | `grok-4.7` |
| actual_cost | 0.75（按本单量级估算，美元） |
| cost_warn | `green` |

## 涉及文件

- `repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/PolicyCompareController.java`
- `repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/service/PolicyCompareService.java`
- `repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/feign/RemoteElementClient.java`
- `repos/lumen-svc-platform/gkxlumen-display/src/test/java/com/topcomm/gkxlumen/display/service/PolicyCompareServiceTest.java`
- `repos/lumen-svc-platform/gkxlumen-element/src/main/java/com/topcomm/gkxlumen/element/controller/PolicyCompareReadController.java`
- `repos/lumen-svc-platform/gkxlumen-element/src/test/java/com/topcomm/gkxlumen/element/controller/PolicyCompareReadControllerTest.java`
- 本 handoff
