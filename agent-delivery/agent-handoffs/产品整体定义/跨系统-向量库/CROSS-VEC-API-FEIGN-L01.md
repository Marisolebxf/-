# CROSS-VEC-API-FEIGN-L01 · 产业锚点向量 Java Feign 门面（embed/rebuild + embed/search）

> 派单包 `派单/CROSS-VEC-API-FEIGN-L01-派单包.md`；总控 §0 #1 #6 #16 #17 / §4 第 5 行；上游契约 `CROSS-VEC-PY-INDEX-L01.md` §下游契约。
> **本叶最重要的三条**：①Java **零算法**，两条路径只是 Feign 转发，Java 侧连一次字符串切分都没做；②**未就绪一律 501 + honesty**，把 Python 的 503 / `degraded=true` / 连不上 / 体不合契约全部向上暴露，禁止 200 空成功；③**没有新建 Feign client / 配置类 / 模块**，复用存量 `RemoteChainPythonClient` + `ChainPythonFeignConfig`（同一个 `lumen-algo-py` 基址与超时），本叶净增一个 DTO 文件。
> `jobs/enrich` 门面**不在本叶**（= `CROSS-VEC-API-JOB-L01`，另依赖 JOB-A），本叶零代码涉及。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控段 C；lock 24h；接单时已 claimed + in_progress |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 停在阶梯第 2 级「已存在就复用」：**没有**新 Feign client、**没有**新 `*PythonFeignConfig`、**没有**新 controller / service / 模块。两条 `@PostMapping` 挂在存量 `IndustryFacadeController`（同前缀 `/topic/v1/industry`），两个 Feign 方法挂在存量 `RemoteChainPythonClient`（同 `lumen-algo-py` 基址 `gkxlumen.topic.chain.algo-base-url`、同 `ChainPythonFeignConfig` 重试/超时）。honesty 结构沿用仓内 `PolicyFacadeServiceImpl` 的既有键（`empty/source/engine/error/fabricated`），不另造一套词汇。**零新 Maven 依赖**、零 helm 改动（网关 `/chain/**` 已是前缀通配）。净增文件 1 个（`IndustryEmbedSearchRequest`），主代码净增约 100 行。未用 YAGNI 跳过：honesty / 501 硬闸、D12 校验、输入校验、可观测（沿用现有 `TraceHeaderMiddleware` 侧的 trace 透传 + 新增 `log.warn` 记未就绪原因）、handoff。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 单仓单叶，本机未挂 Headroom |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `02-概要设计.md` **§2 调用链**（另对照 §1.1 建库/消费切面） |
| 图 diff | **新增一条实线**：`前端 → 网关(/chain/**) → gkxlumen-topic-chain-biz(/topic/v1/industry/embed/*) → lumen-algo-py(/internal/industry/embed/*)`，即把 §2 里 Java→Python 那段在向量面落实。**没有**新增 `Java → Milvus 19530` 的边（该边只存在于 Python 侧，本叶未碰）；**没有**新增 `Java → jobs/enrich` 的边（留给 API-JOB）。禁止事项无变化：Java 不签发 VID、不产 `industry_link_code`。节点名沿用仓名 `gkxlumen-topic-chain-biz`。 |
| 会签态 | `v0.3-draft`（抄源文件 frontmatter，未自填绿） |

## 范围与实现

**做**：Java 侧产业锚点向量门面，两条对外 REST，只 Feign 转发，未就绪 501 + honesty。

### 1. 对外 REST 路径（全文）

| 服务内路径（`gkxlumen-topic-chain-biz`） | 网关路径 | 方法 | 转发到 |
|---|---|---|---|
| `/topic/v1/industry/embed/rebuild` | `/chain/topic/v1/industry/embed/rebuild` | `POST` | `lumen-algo-py` `POST /internal/industry/embed/rebuild` |
| `/topic/v1/industry/embed/search` | `/chain/topic/v1/industry/embed/search` | `POST` | `lumen-algo-py` `POST /internal/industry/embed/search` |

- 所属模块：**`gkxlumen-topic-chain`**（`-biz` 放 controller/service/feign，`-api` 放 DTO）。选它是因为产业锚点即产业链对象，存量 `IndustryFacadeController`／`RemoteChainPythonClient` 已指向同一个 `lumen-algo-py`，无需第二套寻址。
- 网关**无需新增路由**：`configs/gkxlumen-gateway-dev.yml` 已有 `Path=/chain/**` → `lb://gkxlumen-topic-chain-biz`（GlobalFilter 统一剥第一段），新子路径自动覆盖。`db/9x_gkxlumenx_sys_route_conf_topic_chain.sql` 同为 `/chain/**`，不用改。
- 鉴权注解沿用同类 `@Inner(value = false)`（对外可调，与 `search` / `meta` 一致）。

### 2. 请求 / 响应契约

`embed/rebuild` 请求：**无 body**（Java 固定给 Python 发 `{}`）。

`embed/search` 请求（`IndustryEmbedSearchRequest`，白名单）：

```json
{ "query": "集成电路", "topK": 2, "kinds": ["chain"], "minScore": 0.2 }
```

- Java 映射为 Python 的 snake_case（`topK→top_k`、`minScore→min_score`），**留空的字段不传**，由 Python 用它自己的默认值（`top_k=8`、两类 kinds、`min_score=0.0`）——Java 不复制一份默认值口径。
- **故意不接受 `collection`**：Milvus 库名是内部实现，不给前端指定（D12 + 总控 §0 #16）。因此 Python 侧前缀守卫的 **422 在本门面不可达**，Java 不需要也没有翻译 422。

就绪时（HTTP 200）：`R.ok(data)`，`data` = Python `data` **原样**，即 `items[{vid,name,kind,industry_code,score}]` / `source` / `model_version` / `index_version` / `degraded=false` / `collection` / `store` / `trace_id`。Java **不改 `score`、不拼 `chain:` 码、不补 `industry_link_code`、不重排序、不合并同名**。

### 3. 501 判定（未就绪）与响应体

判定集中在 `IndustryFacadeServiceImpl#embedCall`（两条路径共用一处），命中任一条即 `R.failed` + honesty，控制器统一映 **HTTP 501 NOT_IMPLEMENTED**：

| honesty.engine | 判定来源 |
|---|---|
| `not_ready:python_503` | Python 返回 **HTTP 503**（引擎不可用 / 词表为空，Python 侧 `code=1` + `degraded=true`） |
| `not_ready:python_http_{status}` | Python 其它非 2xx（如网关 504） |
| `not_ready:unreachable` | Feign 连接失败 / 超时（`FeignException.status() <= 0`） |
| `not_ready:call_failed` | 其它 `RuntimeException`（编解码等），异常堆栈进 Java 日志 |
| `not_ready:python_code_{n}` | HTTP 200 但包络 `code≠0`（防御性，现网不应发生） |
| `not_ready:degraded` | HTTP 200 且 `code=0`，但 `data.degraded=true`（内存回退 / 索引不可信）——**总控硬闸要的那条**，不吞成成功 |
| `not_ready:empty_body` | 空体 |
| `not_ready:malformed` | 体里没有 `data` 对象 |

501 响应体：

```json
{
  "code": 1,
  "msg": "industry embed not ready: python_503",
  "data": {
    "items": [],
    "indexed": 0,
    "source": "industry_embed",
    "degraded": true,
    "honesty": {
      "empty": true,
      "source": "unavailable",
      "engine": "not_ready:python_503",
      "upstream": "lumen-algo-py /internal/industry/embed/search",
      "error": true,
      "fabricated": false
    }
  }
}
```

- 未就绪体**不带任何 Python 返回的候选**：`degraded=true` 时 Python 仍可能给出内存回退命中的 VID，那批 VID 半可信，顺 501 漏出去就等于变相假数据。诊断细节走 `log.warn("industry embed {} not ready: {}", op, reason)`。
- `query` 为空/空白 → **HTTP 400** + `R.failed("query must not be blank")`（信任边界校验，不伪装成「未就绪」）。

**不做**（按派单逐条确认未越界）：`jobs/enrich` 门面（= `CROSS-VEC-API-JOB-L01`，本叶零代码，仅在 controller javadoc 写了一句「不在本模块」）、Java 直连 `192.168.88.43:19530` / 引 Milvus SDK（零依赖变更，全仓 `pom.xml` 未动）、Java 做 embedding / 分词 / 打分 / 二次排序、改前端、改 Python、改 helm/values、把 503/degraded 翻成 200。

## 偏离

| # | 偏离 | 理由 / as-built |
|---|------|-----------------|
| 1 | 未新建独立 Feign client（如 `RemoteIndustryEmbedClient`）与配置类，两个方法挂进存量 `RemoteChainPythonClient` | 目标服务、基址属性（`gkxlumen.topic.chain.algo-base-url`）、重试/超时（`ChainPythonFeignConfig`：连 5s / 读 30s / IO 重试 1 次）完全相同，新建等于把同一个 `lumen-algo-py` 寻址抄第二遍，并多一处 helm/Nacos 要维护。已在该接口 javadoc 写明它现在同时承载 `/internal/v1/chain/**` 与 `/internal/industry/embed/**`（后者无 `/v1`）。rebuild 实测约 4 秒 / 1516 条（PY-INDEX 证据 3），30s 读超时够用。 |
| 2 | 返回类型用 `ResponseEntity<R<Map<String,Object>>>`，不是同文件其它方法的裸 `R<...>` | 501 是**硬要求**，`R` 只能带业务 `code`、带不动 HTTP 状态。仓内已有同类写法（`AnalysisTaskController` 用 `ResponseEntity.status(...)`）。状态判定只有一处：controller 私有 `readiness()`，`R.isOk()` → 200，否则 501。 |
| 3 | 未就绪时 Java 返回的 `data` 里同时有 `items:[]` 和 `indexed:0`（rebuild 其实没有 items、search 其实没有 indexed） | 两条路径共用一个诚实空体，少一套分支；两个值都是「空/零」，读到哪个都不会被误当成功（同时有 `code=1` + HTTP 501 + `honesty.error=true`）。 |
| 4 | `min_score` / `top_k` / `kinds` 缺省时不下传，而不是在 Java 填默认值 | 默认值口径属 Python + VEC-Q2，Java 抄一份就会在改模型/阈值时两边漂移。 |
| 5 | 本机无法执行 `mvn` / `spring-javaformat:apply`，编译与测试证据取自 GitLab CI；dev 上因此留下 3 条红/半红流水线 | 开发机（Windows）**未装 JDK 与 Maven**（`Get-Command mvn/java` 均无、无 `.m2`、无 `mvnw`），SSH MCP 本次会话不可用（`ssh_connect` 返回 `Connection closed` / `Not connected`），故无法本地跑。改用 CI 的 `maven:3.9.6-eclipse-temurin-17` 跑 `mvn clean verify`（编译 + surefire 一起过），逐轮红→修→绿，见 §验收证据 1。代价是把 4 次编译反馈留在了 dev 流水线上（每轮约 70 秒 runner 时间），已升级为开放项 C。格式按 spring-javaformat 约定手工对齐（tab 缩进、import 顺序、行宽 ≤120，已用脚本核过新增行无超长）；仓内 `spring-javaformat-maven-plugin` 未绑 `validate` 执行，不会因此红。 |

## 产物清单

- `gkxlumen-topic-chain/gkxlumen-topic-chain-api/.../api/dto/IndustryEmbedSearchRequest.java`（新增，唯一新文件）
- `gkxlumen-topic-chain/gkxlumen-topic-chain-biz/.../feign/RemoteChainPythonClient.java`（+2 方法）
- `gkxlumen-topic-chain/gkxlumen-topic-chain-biz/.../service/IndustryFacadeService.java`（+2 方法）
- `gkxlumen-topic-chain/gkxlumen-topic-chain-biz/.../service/impl/IndustryFacadeServiceImpl.java`（+`embedRebuild` / `embedSearch` / `embedCall` / `feignReason` / `notReady`）
- `gkxlumen-topic-chain/gkxlumen-topic-chain-biz/.../controller/IndustryFacadeController.java`（+2 `@PostMapping` + `readiness`）
- `gkxlumen-topic-chain/gkxlumen-topic-chain-biz/src/test/.../service/impl/IndustryFacadeServiceImplTest.java`（+2 用例）
- `gkxlumen-topic-chain/gkxlumen-topic-chain-biz/src/test/.../controller/IndustryFacadeControllerTest.java`（+1 用例）
- 本 handoff

未产出（有意）：无 helm/values 改动、无 `pom.xml` 改动、无网关路由改动、无 SQL 改动。

## 验收证据

### 1. 编译 + 单测（GitLab CI，`mvn -B -ntp clean verify`，temurin-17）

四轮，前三轮红/半红全部出在**我自己新加的测试代码**上，主代码 5 个文件从第一轮起就编译通过。如实记录，不把红说成黄：

| pipeline | commit | backend:build | 结论 |
|---|---|---|---|
| [6083](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/6083) | `cf9f3d9` | ❌ failed | 主代码编译通过；测试用了包私有的 `FeignException.errorExecuting` → `testCompile` 报「is not public in feign.FeignException」 |
| [6085](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/6085) | `5492682` | ❌ failed | 编译全绿；`IndustryFacadeServiceImplTest` NPE（Mockito 抛 mock 出来的 Throwable 时 `Arrays.asList(getStackTrace())` 吃到 null） |
| [6087](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/6087) | `36b22ab` | ⚠️ success **但不算数** | 退出码绿，可 chain-biz 只统计到 **4** 个用例：日志里有 `[WARNING] ForkStarter IOException: java.util.NoSuchElementException`，surefire fork 在 `IndustryFacadeServiceImplTest` 中途死掉，两个测试类的结果**没被计入**。根因是 Mockito 陷阱：`when(mock.call())` 会**真的调一次** mock，对已用 `thenThrow` 打过桩的方法再打桩时直接在 `when()` 里抛异常。**没拿这轮当验收证据** |
| [6091](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/6091) | **`b662a9f`** | ✅ **passed（真绿）** | 改用 `doThrow` / `doReturn` + 真实 `FeignException` 子类（不再 mock Throwable）；chain-biz **Tests run: 13, Failures: 0, Errors: 0**，无 ForkStarter 告警，四个测试类全部计入 |

chain 模块测试明细（第四轮，6091）：

```text
IndustryFacadeControllerTest      Tests run: 3   （含 embedReadyIs200AndNotReadyIs501）
IndustryChainUxControllerTest     Tests run: 1
IndustryFacadeServiceImplTest     Tests run: 8   （含新增 2 例）
IndustryFacadeAnalysisDimsTest    Tests run: 1
[INFO] Results: Tests run: 13, Failures: 0, Errors: 0, Skipped: 0
```

全 reactor `backend:build` 绿（upms / innov / metrics / topic-enterprise 111 / topic-svc 80 / topic-policy 28 等既有用例未被破坏）。

新增用例断言什么：

| 用例 | 断言 |
|------|------|
| `embedSearchForwardsWhitelistAndPassesItemsThrough` | Python `data` 原样上送（`vid=chain:INB1303`、`score=1.0` 未被改写、item 里**没有** `industry_link_code`）；下传 payload **精确等于** `{query, top_k, kinds}` → 证明白名单生效、**没有** `collection`、也没给 `min_score` 塞默认值 |
| `embedNotReadyOnPython503TimeoutCallFailureDegradedAndMalformed` | 五种未就绪各自的 `honesty.engine`：`python_503` / `python_http_504` / `call_failed` / `degraded`（HTTP 200 + `degraded=true` + `store=memory` 也必须判未就绪）/ `malformed`；每种都 `code=1`、`items=[]`、`indexed=0`、`fabricated=false` |
| `embedReadyIs200AndNotReadyIs501`（controller） | 路径契约 + 状态码：`/topic/v1/industry/embed/search` 就绪 200；`/embed/rebuild` 未就绪 **501** 且体内 `honesty.engine=not_ready:python_503`、`items` 空；`query` 空 → **400** |

未被单测覆盖的 3 个判定分支（如实列出）：`not_ready:unreachable`（`FeignException.status() <= 0`）、`not_ready:python_code_{n}`、`not_ready:empty_body`。前者要造 status ≤0 的 Feign 异常，只能 mock Throwable 或调 protected 构造器（正是 6085/6087 两轮红的来源），代价大于收益；三条分支各 2–3 行、与已覆盖分支共用同一个 `notReady()` 出口，按代码走查确认。

CI 日志留下了未就绪日志，证明 honesty 判定真的跑到了：

```text
WARN ...IndustryFacadeServiceImpl -- industry embed search not ready: python_503
WARN ...IndustryFacadeServiceImpl -- industry embed rebuild not ready: python_http_504
WARN ...IndustryFacadeServiceImpl -- industry embed rebuild call failed
      java.lang.IllegalStateException: decode boom
```

### 2. 未做的事的证明

- 全仓 `pom.xml` 零改动 → 未引 Milvus SDK / 任何新依赖；`git show --stat` 仅 chain 模块 7 个文件。
- 新增代码内无 `19530` / `Milvus` 客户端调用、无 `industry_link_code` 赋值、无 `chain:` 字符串拼接（`chain:INB1303` 只作为测试断言里的**期望值**出现，不是 Java 生成的）。
- 无 `jobs/enrich` 路径字样（仅 controller javadoc 一句「不在本模块」说明）。
- 未改 `helm/` 任何文件：devops 前序 `bea173e` 只动了 `entanPy.env`（政策/企业 Python），与本叶无关；chain 模块的 Python 寻址 `configs/gkxlumen-topic-chain-biz-dev.yml` 早已是 `GKXLUMEN_TOPIC_CHAIN_ALGO_BASE_URL:http://lumen-platform-algo-py:8000`，**本来就指向 lumen-algo-py**，不需要新增变量。

### 3. 尚未验证（诚实标注）

- **未在 K8s dev 上 curl 过这两条路径**：本轮 `backend:build` 绿后镜像/部署阶段按 CI 规则触发（topic-chain 在 dev 自动部署清单内），但提交时刻未点名 rollout 完成，也未跑真实 HTTP。段 E 由 coordinator 点名。
- 因此「Python 就绪时 200 透传」目前只有单测（mock Feign）覆盖，未有 Java→Python 的真实回环证据；Python 侧真实返回已由 PY-INDEX 在现网实测（其 §验收证据 4）。这条差距写进 §遗留风险。

## 问题清单 / 开放项（升级给 `human:淮政玮`）

| # | 事项 | 谁做 | 状态 |
|---|------|------|------|
| A | **rebuild 该不该对外开**：现在 `@Inner(value=false)` 与 `search` 一致，即网关可达。整库重建是写操作（drop+create+insert），生产上更该只给运维 / CHAIN-HOOK 内网调。是否收成 `@Inner(true)` 或加权限位，请架构拍板 | 架构 + 淮政玮 | 🟡 |
| B | **`degraded=true` 一律 501 的口径**：内存回退时 Python 其实能返回可用的命中（只是不持久化）。本叶按总控硬闸判未就绪 → 前端只会看到 501。若产品希望「降级可用但打角标」，需要改成 200 + `degraded` 透传 + 前端 MockBadge，属口径变更 | 产品 + 架构 | 🟡 |
| C | **本机无 Java 工具链**：开发机没有 JDK/Maven，Java 叶目前只能靠 CI 验证，每轮反馈约 70 秒且会占用 runner。建议给 api 侧开发机装 temurin-17 + maven，或提供可 SSH 的构建机 | 运维 + 淮政玮 | 🟡 |
| D | 承接 PY-INDEX 开放项 D：没有「当前索引版本」查询接口，Java 门面也就无法给前端提供 `industry_index_version`（`search` 只能回传命中行的版本）。若前端要展示索引新鲜度，需 Python 补 `GET .../status` 再加一条 Feign | coordinator 决定要不要建叶 | 🟡 |

## 修改内容

| 文件 | 改了什么 |
|------|----------|
| `api/.../dto/IndustryEmbedSearchRequest.java` | 新增。`query` / `topK` / `kinds` / `minScore` 四字段 + `@Schema`；注释写明**故意不含** `collection` |
| `biz/.../feign/RemoteChainPythonClient.java` | +`industryEmbedRebuild(Map)` / `industryEmbedSearch(Map)`，路径写死 `/internal/industry/embed/{rebuild,search}`（无 `/v1`）；类 javadoc 补「Java 不 embed / 不直连 Milvus」 |
| `biz/.../service/IndustryFacadeService.java` | +`embedRebuild()` / `embedSearch(req)` 声明，javadoc 写明未就绪由控制器映 501 |
| `biz/.../service/impl/IndustryFacadeServiceImpl.java` | +`embedRebuild` / `embedSearch`（白名单 payload 映 snake_case）、`embedCall`（唯一就绪判定）、`feignReason`（status≤0 与 503 分开）、`notReady`（honesty 体 + `log.warn`）；类加 `@Slf4j` |
| `biz/.../controller/IndustryFacadeController.java` | +`POST /embed/rebuild` / `POST /embed/search`（`ResponseEntity<R<...>>`）、`readiness()`（`isOk` → 200，否则 501）、`query` 空 → 400；类 javadoc 补 embed 说明与「jobs/enrich 不在本模块」 |
| `biz/src/test/.../IndustryFacadeServiceImplTest.java` | +2 例（白名单透传 / 五种未就绪判定）；换桩统一用 `doThrow` / `doReturn`，不 mock Throwable |
| `biz/src/test/.../IndustryFacadeControllerTest.java` | +1 例（路径 + 200/501/400 状态契约） |

## 测试结果

- CI `mvn clean verify`（pipeline **6091** / `b662a9f`）：`gkxlumen-topic-chain-biz` **13 passed, 0 failed, 0 error**；全 reactor `backend:build` **passed**（未破坏 upms / innov / metrics / topic-* 等既有模块用例）。
- 中间轮次 6087 虽然退出码绿，但 surefire fork 崩了、chain 只计入 4 个用例，**不作为验收证据**（见 §验收证据 1）。
- 本地 `mvn` **无法执行**（开发机无 JDK/Maven，见 §偏离 5），故没有本地测试结果可贴——不编造。
- 未跑集成/端到端：Java→Python 真实回环留给段 E / coordinator 点名（见 §验收证据 3）。

## 遗留风险

- **本叶没有任何真实 Java→Python 调用证据**：单测里 Feign 是 mock。若 Python 的包络在现网与 handoff 契约有偏差（例如 `data` 不是对象），本门面会判 `not_ready:malformed` 报 501 —— 这是设计上的诚实失败，不是静默降级，但排障时要先看 `honesty.engine`。
- **向量语义能力仍为 0**（承接 PY-INDEX 偏离 2）：本门面原样透传 `score`。任何调用方（含 API-JOB / POLICY-SEARCH）**必须**按总控 §0 #17 拿 top-k 候选再过 `match_industry_anchors` 二次对码，禁止采 top1 当定码。Java 侧没有、也不会加这个二次对码（那是算法，属 Python）。
- `rebuild` 目前网关可达（开放项 A）。在收紧之前，误调只会触发 Python 侧整库重建（幂等、约 4 秒），不会破坏别的 collection（Python 前缀守卫在），但会顶掉 `index_version`。
- 30s 读超时是按现网 1516 条锚点（约 4 秒）定的。词表规模若涨一个量级，`rebuild` 可能超时被判 `not_ready:unreachable` —— 那时应把 rebuild 改成异步任务（走 async-service），而不是无脑调大超时。
- 未加 OTel 自定义 span；trace 透传沿用仓内既有 Feign / 网关链路，Python 返回的 `trace_id` 在就绪响应里原样带回。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `origin/dev`（先 `git pull --ff-only` = Already up to date，未 force；前序 devops `bea173e` 已在本地基线上）
- commit：**`b662a9f`**（`feat` 主提交 `cf9f3d9` + 三个测试修复 `5492682` / `36b22ab` / `b662a9f`，全部带 `[agent:api-agent]`；无 force、无 amend 已推提交）
- pipeline URL / ID：**6091** https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/6091（前三轮 6083 / 6085 / 6087 见 §验收证据 1）
- 部署 namespace / 镜像 tag：`dev`；`gkxlumen-topic-chain-biz` 镜像由 CI 打 tag（topic-chain 属 `origin/dev` 自动部署清单）
- K8s rollout：**未在本叶点名验证**（提交时刻 backend:build 刚绿，image/deploy 阶段随后跑）。段 E 由 coordinator 点名 CI `deploy:topic-chain` 绿
- dev 测试 URL / 命令与结果（待 rollout 后由 coordinator / QA 点）：

```bash
# 未就绪路径（Python 不通 / degraded 时应得 501，且体内 honesty.engine 指明来源）
curl -i -X POST "https://{gateway}/chain/topic/v1/industry/embed/search" \
  -H "Authorization: Bearer {token}" -H "Content-Type: application/json" \
  -d '{"query":"集成电路","topK":2}'

# 就绪路径（Python live 时应得 200 + items[].vid 为图上码）
curl -s -X POST "https://{gateway}/chain/topic/v1/industry/embed/rebuild" \
  -H "Authorization: Bearer {token}"
```

## 可观测性（建议）

- OTEL_SERVICE_NAME：未改（`gkxlumen-topic-chain-biz`）
- traceId（dev 抽样）：**无**（本叶未在 dev 跑过真实请求，不编造 traceId）。就绪响应里 Python 的 `trace_id` 原样透传
- Tempo / Loki：无新增埋点；新增一条结构化 `WARN industry embed {op} not ready: {reason}`，可直接按 `not_ready:` 前缀在 Loki 聚合 501 原因分布

## 涉及文件

- `lumen-svc-platform/gkxlumen-topic-chain/gkxlumen-topic-chain-api/src/main/java/com/topcomm/gkxlumen/topic/chain/api/dto/IndustryEmbedSearchRequest.java`
- `lumen-svc-platform/gkxlumen-topic-chain/gkxlumen-topic-chain-biz/src/main/java/com/topcomm/gkxlumen/topic/chain/feign/RemoteChainPythonClient.java`
- `lumen-svc-platform/gkxlumen-topic-chain/gkxlumen-topic-chain-biz/src/main/java/com/topcomm/gkxlumen/topic/chain/service/IndustryFacadeService.java`
- `lumen-svc-platform/gkxlumen-topic-chain/gkxlumen-topic-chain-biz/src/main/java/com/topcomm/gkxlumen/topic/chain/service/impl/IndustryFacadeServiceImpl.java`
- `lumen-svc-platform/gkxlumen-topic-chain/gkxlumen-topic-chain-biz/src/main/java/com/topcomm/gkxlumen/topic/chain/controller/IndustryFacadeController.java`
- `lumen-svc-platform/gkxlumen-topic-chain/gkxlumen-topic-chain-biz/src/test/java/com/topcomm/gkxlumen/topic/chain/service/impl/IndustryFacadeServiceImplTest.java`
- `lumen-svc-platform/gkxlumen-topic-chain/gkxlumen-topic-chain-biz/src/test/java/com/topcomm/gkxlumen/topic/chain/controller/IndustryFacadeControllerTest.java`
- 本 handoff

## 下游契约（给 `CROSS-VEC-API-JOB-L01` / 前端 / POLICY-SEARCH）

| 项 | 值 |
|----|-----|
| 对外路径 | `POST /chain/topic/v1/industry/embed/rebuild`、`POST /chain/topic/v1/industry/embed/search`（服务内 `/topic/v1/industry/embed/*`） |
| search 请求 | `{query（必填）, topK?, kinds?, minScore?}`；**不接受 `collection`** |
| 成功响应 | `R.ok(data)`，`data` = Python `data` 原样（含 `items` / `model_version` / `index_version` / `store` / `trace_id`） |
| 未就绪 | HTTP **501** + `code=1` + `data.honesty.engine=not_ready:*`（8 种来源见 §范围与实现 3），`items` 恒空 |
| 参数非法 | `query` 空 → HTTP **400** |
| 红线 | `score` **不是** `industry_link_code`；本门面不产 VID、不定码。API-JOB 必须走「top-k 候选 → `match_industry_anchors` 二次对码」（总控 §0 #17） |
| API-JOB 关系 | 本叶**只交** rebuild/search 门面。`jobs/enrich` 门面在 `CROSS-VEC-API-JOB-L01`，它还要等 JOB-A 定义 Python 侧 `jobs/enrich` 契约；届时**建议同样挂进 `RemoteChainPythonClient`** 复用寻址，honesty/501 判定可直接复用 `embedCall` 的模式（若语义相同可提取，本叶按 YAGNI 未预留抽象） |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python（D1） | ✅ Java 只有 Feign 转发 + 状态映射；无 embedding / 分词 / 打分 / 排序；无 NLP 依赖 |
| 调用链不可越层 | ✅ 前端 → 网关 `/chain/**` → `gkxlumen-topic-chain-biz` → Python `/internal/industry/embed/*`；前端不直连 Python，Java 不直连 Milvus 19530 |
| 图谱仅 Nebula | ✅ 未碰 `9669`、未写 nGQL；Java 不签发 / 不加工 VID |
| 可观测 | ✅ 沿用既有 Feign / 网关链路与 `OTEL_SERVICE_NAME`；新增未就绪 `WARN` 结构化日志；未把连接串写进日志 |
| CI/CD | ✅ push `origin/dev`，未 force；3 个 commit 均带 `[agent:api-agent]`；`backend:build` 绿（pipeline 6086） |
| demo2 只读 / **D12** | ✅ 未改任何 `demo-*` 仓、未 merge；下游只有 `lumen-algo-py`（`GKXLUMEN_TOPIC_CHAIN_ALGO_BASE_URL` → `lumen-platform-algo-py:8000`），**无** `demo-svc-platform` / `demo-algo-*` / `demo-platform-*` 回落；未向前端暴露 Milvus IP 或 collection 名 |
| 数据策略 | ✅ Java 不读写 ADS/DWD/Milvus，本叶零 SQL、零 nGQL |
| D8 / D10 | N/A（无 UI） |
| D9 数据血缘 | N/A（本叶不产界面统计指标；`model_version` / `index_version` 由 Python 提供并原样透传，可追溯） |
| 密钥不入 git | ✅ 无新增凭据；Python 基址走 env / Nacos |
| 硬闸：禁止 200 假 VID | ✅ `degraded=true`、503、连不上、体不合契约一律 501，未就绪体不带任何候选（单测 `embedNotReadyOnPython503TimeoutCallFailureDegradedAndMalformed` + `embedReadyIs200AndNotReadyIs501` 守住） |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 132000 |
| model_used | claude-opus-5-thinking |
| actual_cost | 0.79 |
| cost_warn | green |

口径：coding 默认 75/25 读写比；B 档 `$3/$15` per 1M；`132000×0.75×3/1e6 + 132000×0.25×15/1e6 = 0.79`。
