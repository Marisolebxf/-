# LUMEN-CHAIN-JAVA-FACADE-L01 · 产业链 Java 查询/门户/发布快照门面

> 格式参考 `templates/handoff-template.md`；内容按本单 as-built。  
> **不做**：Job / async-service（`LUMEN-CHAIN-JAVA-JOB-L01`）、lumen-algo-py、前端、CMS/OPS 写侧。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | registry 已 claimed + in_progress；lock 24h。本单完工转 **integration**，不标 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单 `/goal` 一致。未用 YAGNI 跳过调用链（前端→Java→Python `/internal`）、可观测（Java Agent + `OTEL_SERVICE_NAME`）、D9（指标走 `gkxlumen-metrics` catalog，chain 不手写就绪度改绿）。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | C 总派单 / ABCD 总控 / PY-SEARCH / PY-SYNC / Demo `industrySearchModel.ts` / enterprise 切法均精读，未用 compress 代替。 |

## 范围与实现

新建独立微服务 **`gkxlumen-topic-chain`**（api+biz），切法对齐 `gkxlumen-topic-enterprise`：Controller → Service → Feign Python `/internal/v1/chain/**`。无 ES 客户端、无 13 旧 GET、不复制 `demo-svc-platform` `gkx-innov` ChainController。企业 `/topic/v1/search/meta/chains` 仍是高筛字典，不是产业查询。

Java 原样透传 Python 裸 JSON（`R.ok(map)`）。KPI `value=null`（Q056/QC07）不补假数；`created_task` 不改成 true。不签发 Job snapshot。

### 对外路径表（语义锁定，as-built 写死）

| 语义 | 服务内 | 网关完整路径 | Feign Python |
|---|---|---|---|
| health | `GET /topic/v1/industry/health` | `GET /chain/topic/v1/industry/health` | `GET /internal/v1/chain/health` |
| search GET | `GET /topic/v1/industry/search` | `GET /chain/topic/v1/industry/search` | `GET /internal/v1/chain/search` |
| search POST | `POST /topic/v1/industry/search` | `POST /chain/topic/v1/industry/search` | `POST /internal/v1/chain/search` |
| overview | `GET /topic/v1/industry/overview` | `GET /chain/topic/v1/industry/overview` | `GET /internal/v1/chain/sync/kpi` |
| overview KPI | `GET /topic/v1/industry/overview/kpi` | `GET /chain/topic/v1/industry/overview/kpi` | `GET /internal/v1/chain/sync/kpi` |
| overview news | `GET /topic/v1/industry/overview/news` | `GET /chain/topic/v1/industry/overview/news` | `GET /internal/v1/chain/sync/news` |
| panorama snapshot | `GET /topic/v1/industry/panorama/snapshot` | `GET /chain/topic/v1/industry/panorama/snapshot` | `GET /internal/v1/chain/sync/snapshot` |
| catalog | `GET /topic/v1/industry/catalog` | `GET /chain/topic/v1/industry/catalog` | `GET /internal/v1/chain/sync/objects` |

SEARCH `mode`：`smart` / `industry` / `advanced`。记录字段对齐 Demo `IndustrySearchRecord`（Java 不改写命中逻辑）。

网关：`Path=/chain/**` → `lb://gkxlumen-topic-chain-biz`；`GkxlumenRequestGlobalFilter` StripPrefix=1。禁止再 Strip 到 innov `/v1/industry`。禁止把产业查询塞进 `/topic/**` 薄模块或企业模块。

## 偏离说明（as-built）

| 项 | 派单 | As-built | 理由 |
|---|---|---|---|
| 网关前缀 | `/topic/v1/industry/**` → chain | `/chain/**` 剥 `chain` 后落到服务内 `/topic/v1/industry/**` | `/topic/**` 已挂薄 `gkxlumen-topic`；与 enterprise `/enterprise/**` 同构 |
| overview | ADS 只读 + 必要 Feign | **全部 Feign SYNC**（kpi/news）；Demo ADS 仅 JDBC 探活（`SET SESSION TRANSACTION READ ONLY`） | 查询目录权威仍是 Python SEARCH/objects；Java 不扫 DWD/ADS 作第二查询路径 |
| panorama snapshot | ADS `graph_snapshot` | Feign SYNC snapshot | 与 Job Result 分 API；写快照是 JOB/Python 的事 |
| gkxlumen-boot | 一并挂上 | 单体 **未列入**；模块 POM 有 `cloud`/`boot` profile | 对齐 `topic-enterprise` / `topic-async-service`；生产走独立进程 7095 |
| 集群端到端 curl | 能联调则经 Java curl 一次 Python | 契约/MockMvc **7/7 绿**；集群 `lumen-platform-algo-py` 镜像仍 `55bc548d`（OpenAPI 无 `/internal/v1/chain/**`） | 本单不改 Python、不擅自 set image；B 代码真源 `03c6c58` 待 rollout |

## 产物清单

| 产物 | 路径（相对 `lumen-svc-platform/`） |
|---|---|
| 模块 | `gkxlumen-topic-chain/`（api+biz） |
| 启动类 | `…-biz/…/GkxlumenTopicChainApplication.java`（`@EnableOpenApi("chain")`） |
| Controller | `…/controller/IndustryFacadeController.java` |
| Service | `IndustryFacadeService` + `impl/IndustryFacadeServiceImpl` |
| Feign Python | `…/feign/RemoteChainPythonClient.java`（直连 `algo-base-url`） |
| 对外 Feign | `…-api/…/feign/RemoteTopicChainService.java` |
| DTO | `IndustrySearchRequest` / `IndustrySearchCondition` / `IndustrySyncQuery` |
| Nacos | `helm/gkxlumen-platform/configs/gkxlumen-topic-chain-biz-dev.yml` |
| 网关 | `helm/gkxlumen-platform/configs/gkxlumen-gateway-dev.yml` `Path=/chain/**` |
| Helm | `values.yaml` `topic-chain`（7095）+ `values-lumen.yaml` enabled |
| CI | `.gitlab-ci.yml`：`-pl`、artifact、`backend:image:topic-chain`、`deploy:topic-chain`、`helm:deploy` needs |
| 常量 | `ServiceNameConstants.TOPIC_CHAIN_SERVICE` |
| 本 handoff | `agent-delivery/agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-JAVA-FACADE-L01.md` |

未改：`lumen-algo-py`、`gkxlumen-topic-async-service`、前端仓、`gkxlumen-metrics`（catalog 既有）。

## 验收证据

| 项 | 结果 |
|---|---|
| Maven 测试 | ✅ `mvn -pl gkxlumen-topic-chain/gkxlumen-topic-chain-biz -am test` **BUILD SUCCESS**；Tests run: **7**，Failures: 0（Controller MockMvc 2 + Service 5） |
| 三种 SEARCH mode | ✅ smart / industry / advanced 转发覆盖 |
| Q056/QC07 null | ✅ 单测断言 `value=null` 原样、`created_task=false` |
| 422 不造假 KPI | ✅ Feign 422 → `R.failed`，data=null |
| 无 ES / 无 13 GET / 无 nGQL | ✅ pom 无 ES 依赖；Feign 仅 `/internal/v1/chain/**` |
| Nacos algo-base-url | ✅ `http://lumen-platform-algo-py:8000`（禁止 innov-py / demo-algo-science） |
| Demo ADS 只读 | ✅ `demo_gkxlumenx_ads` + `connection-init-sqls: SET SESSION TRANSACTION READ ONLY` |
| 可观测 | ✅ Dockerfile `JAVA_TOOL_OPTIONS` Java Agent；`OTEL_SERVICE_NAME=gkxlumen-topic-chain-biz` |
| 集群 Java→Python curl | ⏳ 开放项：等 lumen-algo-py 含 SEARCH+SYNC 的镜像 rollout + 本服务 CI deploy |

## 架构合规自检（十条）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ Java 只 Feign 透传 |
| 2 | 前端 → Java REST → Python `/internal/*` | ✅ 无前端直连；无 `/gdf/tasks` |
| 3 | 图谱 NebulaGraph；禁止 Neo4j | ✅ 未引入 Neo4j；不直连 nGQL |
| 4 | 可观测：Java Agent | ✅ OTel agent + `OTEL_SERVICE_NAME` |
| 5 | CI/CD push → Pipeline 绿 → K8s | ✅ 已挂 image/deploy/helm；push `origin/dev` 后走既有 Pipeline |
| 6 | demo2 不 merge lumen | ✅ 仅 lumen-svc-platform + 编排仓 handoff |
| 7 | 共享聚合；Java 不写算法、不直连 nGQL、只读 ADS | ✅ ADS 只读探活；查询权威 Python |
| 8 | 数据策略：ADS 先行 / Mock | ✅ 联调 Demo ADS；不写正式库 |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 | ✅ 指标走既有 `gkxlumen-metrics` catalog；chain 不手写就绪度、不改绿 |

## CI/CD

- 分支：`lumen-svc-platform` `dev`（禁止 main、禁止 force）
- commit：`lumen-svc-platform` `83422eef8a69bf180e90c2d97693f479b97203a2`（`feat(topic-chain): add industry search/overview/snapshot facade [agent:api-agent]`）
- pipeline：push `origin/dev` 触发；手动 `deploy:topic-chain` 或 `helm:deploy`
- 部署：ns=`dev`；镜像 `gkxlumen-topic-chain`；端口 **7095**
- 网关 NodePort：`http://192.168.88.50:30899/chain/topic/v1/industry/health`（服务 rollout 后）
- K8s rollout：本单提交后由 CI；Python chain 路由待镜像升级

## 可观测性

- `OTEL_SERVICE_NAME`：`gkxlumen-topic-chain-biz`
- Micrometer tracing：与其它微服务一致 `management.tracing.enabled: false`（走 Java Agent）
- Tempo / Loki：沿用平台 Collector

## 遗留风险 / 开放项

1. **Python 镜像滞后**：集群 `lumen-platform-algo-py` 仍旧镜像，OpenAPI 无 `/internal/v1/chain/**`。端到端 curl 待 B 镜像 rollout 后补（本单不改 Python）。
2. **Nacos 配置生效**：`configs/gkxlumen-topic-chain-biz-dev.yml` 随 helm `nacos-config-init` Glob 发布；需一次 helm/nacos-init 或等价 publish。
3. **JOB 单**：`LUMEN-CHAIN-JAVA-JOB-L01` 扩展 async-service；本门面不签发 `result_snapshot_id`。
4. 前端 `lumen-ui-topic` 对接另单；完整网关路径以本表 `/chain/topic/v1/industry/**` 为准。

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 220000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.19 |
| cost_warn | green |

口径：api-agent 默认 in/out=**80/20**，按 budget-estimate Sonnet 4.5 价表（$3 / $15 per 1M）折算（Grok 无独立价行）。`source: session_estimate`。公式：`220000×0.8×3/1e6 + 220000×0.2×15/1e6 = 1.188 ≈ 1.19`。单任务 <$5。

## 联调确认

**联调通过 / 联调确认**：Java 契约层 MockMvc + Service 单测 7/7 绿；三种 SEARCH mode 转发正确；SYNC KPI null 与 `created_task=false` 原样透传；snapshot 与 Job Result 分 API。集群经网关 Java→Python 端到端 curl **待** lumen-algo-py SEARCH+SYNC 镜像 rollout 后补，不在本单造假数。本 agent **不**把任务标 `done`（feature → `integration`）。
