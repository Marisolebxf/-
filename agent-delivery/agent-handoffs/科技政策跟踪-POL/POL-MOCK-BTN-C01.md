# POL-MOCK-BTN-C01 · 拆解语义读口

> 2026-11-09。只加 `POST /display/v1/policy/parse/jobs`。不改任务状态，不开始 C02/C03，不改前端，不改 Nacos。

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
| 说明 | 照 `simulation/jobs` 走 display → `RemoteElementClient` → element GET → `gkxlumenx_gapfill.gapfill_policy_semantic`。未用 YAGNI 跳过调用链。失败日志打当前 OTel traceId。未改图、未改前端、未造 0。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无。本单不改存储流图 |
| 图 diff | 无 |
| 会签态 | 未改图，不抄会签态 |
| 说明 | 表结构沿用 A01 已落盘的 `stores/mysql/gapfill.md` |

## 问题清单

- 八张新表在 A01 执行后行数是 0。本读口无行时 `records` 为空列表，不造 0。灌数是 B 段，本单不写。
- 607、608 的条款树和 609 的子图不在这条资源上。本单没有 `parse/clauses`。

## 修改内容

调用链：浏览器 `POST /display/v1/policy/parse/jobs` → 网关已有 `Path=/display/**`（GlobalFilter 剥第一段）→ `gkxlumen-display` `POST /v1/policy/parse/jobs` → Feign `GET /v1/element/policy/parse` → `gkxlumen-element` 只读 `{gapfill}.gapfill_policy_semantic`。

display 不写 mock、不连 Python、不写 nGQL、不直连库。未知 `facet_name` 不查表。Feign 失败返回空列表，HTTP 仍成功，不返回 501。

### 怎么调

```http
POST /display/v1/policy/parse/jobs
Content-Type: application/json

{}
```

或带过滤：

```json
{"policy_id":"<演示库政策键>","facet_name":"主旨"}
```

`facet_name` 闭集：主旨、适用场景、约束、条款分类。空体或只给 `policy_id` 时按条件读表。空白字符串当没传。

### 请求字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `policy_id` | 否 | 等值过滤。不传则不按政策收窄 |
| `facet_name` | 否 | 等值过滤。不在闭集则不查表，`records` 为空 |

### 响应字段

外层是平台 `R`：`code`（成功为 0）、`msg`、`data`。`data` 只有 `records`，没有 `total` / `count`。

`records[]` 来自缺项表，列名由 element 转成 camelCase：

| 字段 | 表列 | 说明 |
|------|------|------|
| `id` | `id` | 自增主键 |
| `policyId` | `policy_id` | 政策业务键 |
| `facetName` | `facet_name` | 主旨、适用场景、约束、条款分类 |
| `bodyText` | `body_text` | 一句中文 |
| `isMock` | `is_mock` | 缺项标记 |
| `metricId` | `metric_id` | 可空，本表不新造指标 |
| `gapItem` | `gap_item` | 缺口项 |
| `fillMethod` | `fill_method` | 写入方式 |
| `gapfillBatchId` | `gapfill_batch_id` | 批次 |
| `generatedAt` | `generated_at` | 生成时间 |

无行、未知侧面、读失败时：`code=0`，`data.records=[]`。

element 对内是 `GET /v1/element/policy/parse`，查询参数同名 `policy_id`、`facet_name`，`@Inner` + Feign `@NoToken`。排序：`policy_id`，再按侧面闭集，再 `id`。语句只有 `SELECT`，没有 `COUNT`、`INSERT`、`UPDATE`、`DELETE`。

## 测试结果

2026-11-09 本机（JDK 17，Maven 3.9.9，build cache 关闭）：

```text
mvn -pl gkxlumen-display,gkxlumen-element -am test "-Dtest=PolicyParseServiceTest,PolicyParseReadControllerTest" "-Dsurefire.failIfNoSpecifiedTests=false" "-Dmaven.build.cache.enabled=false"
```

- `PolicyParseServiceTest`：Tests run: 5, Failures: 0, Errors: 0
- `PolicyParseReadControllerTest`：Tests run: 4, Failures: 0, Errors: 0
- BUILD SUCCESS（20:12:46 +08:00）

覆盖：路径只有 `/jobs`；空体仍调 element；按政策与侧面过滤；未知侧面不查表；Feign 失败仍是空列表；SQL 只打 `gapfill_policy_semantic`；响应不含 `total`/`count`。

## 遗留风险

- 表仍是空的。展示在 B 段写入之前读到的是空列表。这是允许的空态，不是失败。
- 前端拆解页接这条读口不在本单。
- 对比 `compare/jobs`、研报 `report/jobs` 是 C02、C03，本单未做。

## CI/CD（必填）

- 分支：`dev` → `origin/dev`
- lumen-svc-platform 功能提交：`dd8585a968a33423a66936264e54c477ceea3630`
- lumen-svc-platform 推送尖端（含与远端 dev 的 merge）：`33b22eb7d455c5b0f444217e67e1727c5b95aeb5`
- gkx-orchestration：本 handoff 这一次提交（推送后以 `git log -1` 为准）
- pipeline：提交后由远端 CI 触发。此处未等、未抄运行结果
- 部署：push `origin/dev` 后由现有 CI 出 display / element 镜像。本单不设 `FORCE_NACOS_REPUBLISH`
- K8s rollout：未在本机等待
- dev 调用：`POST /display/v1/policy/parse/jobs`。网关已有 `id: gkxlumen-display`、`Path=/display/**`，剥第一段后命中 `/v1/policy/parse/jobs`。不需要新网关路由，未改 Nacos

## 可观测性

- display、element 现有 Java Agent 会给这次 HTTP 和 Feign 调用建 span
- Feign 失败日志：`policy parse jobs feign status={} traceId={}`。traceId 取 `Span.current()`，无有效 span 时记 `no-trace`
- element `listOrEmpty` 读表失败已有 warn，并返回空列表

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 调用链 前端 → Java → element，不越层到 Python | 符合。display 只调 `RemoteElementClient` |
| Java 不做 NLP / 不写 nGQL | 符合。只读缺项表 |
| D16 缺项只读 `gkxlumenx_gapfill.gapfill_*` | 符合。SQL 使用 `{gapfill}` |
| D18 接口不返回写死 mock，无行不造 0 | 符合。`records` 为空列表，无计数字段 |
| 不改 Nacos / 不整批重发 | 符合。未改 helm 配置，未发 dataId |
| D12 不把 demo 并进 lumen | 符合。只改 `lumen-svc-platform` |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 250000（估算，含本会话上下文，非控制台精确值） |
| model_used | `grok-4.7` |
| actual_cost | 0.80（按本单量级估算，美元） |
| cost_warn | `green` |

## 涉及文件

- `repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/PolicyParseController.java`
- `repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/service/PolicyParseService.java`
- `repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/feign/RemoteElementClient.java`
- `repos/lumen-svc-platform/gkxlumen-display/src/test/java/com/topcomm/gkxlumen/display/service/PolicyParseServiceTest.java`
- `repos/lumen-svc-platform/gkxlumen-element/src/main/java/com/topcomm/gkxlumen/element/controller/PolicyParseReadController.java`
- `repos/lumen-svc-platform/gkxlumen-element/src/test/java/com/topcomm/gkxlumen/element/controller/PolicyParseReadControllerTest.java`
- 本 handoff
