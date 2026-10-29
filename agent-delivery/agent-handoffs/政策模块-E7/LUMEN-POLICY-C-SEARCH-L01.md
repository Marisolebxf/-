# LUMEN-POLICY-C-SEARCH-L01 · GET /topic/v1/policy/search + 详情

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-JAVA-C-总派单.md`](./LUMEN-POLICY-JAVA-C-总派单.md)  
> 细叶：[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md) §1  
> 前序：[`LUMEN-POLICY-C-BOOT-L01.md`](./LUMEN-POLICY-C-BOOT-L01.md) · [`LUMEN-POLICY-PY-JOB-L01.md`](./LUMEN-POLICY-PY-JOB-L01.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h；本叶只做 search/详情，不做 graph/metrics/task |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对照 topic-chain / topic-svc search 门面：Controller 薄转发 + Feign 透传 Map 查询参数 + 拆 Python `{code,msg,data}`；未新建 DTO；未改 helm；未实现 graph/metrics/task |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 门面透传，无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | §2.2 补 search 读边：Java Feign `GET /internal/policy/search` · `/docs/{id}` → polan 读 DWD `policy_base_info`。工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。 |
| 会签态 | `approved`（`01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

- 对外：`GET /topic/v1/policy/search`；详情 `GET /topic/v1/policy/docs/{id}` 与兜底 `GET /topic/v1/policy/{id}`。网关仍 `/policy/**`（BOOT）。
- Feign 只打 `lumen-algo-py`：`GET /internal/policy/search`（查询参数原样透传）、`GET /internal/policy/docs/{id}`；另声明兜底 `GET /internal/policy/{id}`。基址 `http://gkxlumen-platform-entan-py:8000`。
- 空态 / 下游失败：HTTP 200 + `honesty.empty` + `fabricated=false`；Feign 挂 `degraded=true`。禁止 5xx 填假数、禁止 fixture、禁止 `/v1/policy/mock`。
- 查询不入对比篮、不发起分析。本叶无 graph/metrics/task。
- Java 不写 nGQL/NLP；禁止 Feign `demo-*`。JDBC 仍 `demo_gkxlumenx_*`。

## 偏离说明

- 详情同时挂 `/docs/{id}` 与 `/{id}`，与 PY-JOB 双路径对齐；服务实现只 Feign `/internal/policy/docs/{id}`（静态段优先，避免把 search 当 id）。
- 本机 Windows 无 JDK/mvn；单测以 CI `backend:build` verify 为准（同 BOOT）。
- 未改 helm（BOOT 已挂 `/policy/**`、algo URL）。K8s 首发仍须遗留 `helm:chart`，本叶不挡编码。

## 产物清单

- 代码：`lumen-svc-platform` `3a8d771679780ac4903eea14793cd1a1b9d80089` → `origin/dev`
- 流图：`storage/POLICY/01-data-flow.md` §2.2 search 读边
- 本文 handoff

## 验收证据

- 单元测试：`PolicyFacadeControllerTest` search 命中 / 空态 / docs；`PolicyFacadeServiceImplTest` 透传、空态、Feign 失败诚实降级、Feign path 不含 `demo-`
- 对外：`GET /topic/v1/policy/search` · `GET /topic/v1/policy/docs/{id}` · `GET /topic/v1/policy/{id}`
- Feign：`GET /internal/policy/search` · `GET /internal/policy/docs/{id}` · name=`lumen-algo-py`
- 空态：`items=[]` / `item=null` + `honesty.empty=true` + `fabricated=false`；下游挂 `degraded=true`，`R.code=0`

## 修改内容

| 路径 | 动作 |
|------|------|
| `PolicyFacadeController` | 加 search / docs / `{id}` |
| `PolicyFacadeService` + `Impl` | 透传 Python data；Feign 失败诚实空 |
| `RemotePolicyPythonClient` | search 改为 `@RequestParam Map` 透传；补 `GET /internal/policy/{id}` |
| `RemoteTopicPolicyService` | 对外 Feign 补 search/详情 |
| `PolicyFacadeControllerTest` / `PolicyFacadeServiceImplTest` | 命中、空态、Feign path |
| `storage/POLICY/01-data-flow.md` | §2.2 search 读边 |

## 测试结果

- MockMvc：`GET /topic/v1/policy/search` 命中透传 items；空态 `items` 空且无 mock/fixture。
- MockMvc：`GET /docs/{id}` 与 `GET /{id}` 映射同一详情。
- Feign 注解：`name=lumen-algo-py`，path `/internal/policy/**`，url/path 不含 `demo-`、不含 `/v1/policy/mock`。
- 本机无 JDK，未跑 `mvn test`；以 CI `backend:build` 为准。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `origin/dev`
- commit：`3a8d771679780ac4903eea14793cd1a1b9d80089`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines?ref=dev
- 部署：不改 helm；首发 Deployment 仍须 `helm:chart`（遗留，不挡编码）；`deploy:topic-policy` 仍 BOOT 的 manual
- 探活：`GET http://10.50.69.111:30899/policy/topic/v1/policy/search`（Deployment 起来后）

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-topic-policy-biz`（BOOT 已挂）
- Tempo / Loki：随平台 Collector；本叶未抽样

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ Java 无 NLP/图谱 |
| 前端→Java→Python `/internal/*` | ✅ Feign `/internal/policy/search` · `/docs/{id}` |
| 图谱 Nebula | ✅ 本叶不调 graph、不写 nGQL |
| 可观测 | ✅ 复用 BOOT OTEL |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ 对照 chain/svc 重写 |
| 共享聚合 / 不直连 nGQL | ✅ |
| 数据策略 ADS `demo_gkxlumenx_*` | ✅ JDBC 未改 |
| D8 / D10 | N/A 无 UI |
| D9 8 件套 | N/A 本叶无统计数字 |
| D12 lumen 不调 demo **服务** | ✅ Feign `lumen-algo-py`；禁止 `demo-*`；数仓共用 demo 源是总控 §0 #6 |

## 遗留风险

- K8s 首发仍须 `helm:chart`；本叶未部署验证现网 search。
- DWD 空库返回 `honesty.empty=true`，前端 D 叶按空态渲染。
- graph/metrics/task 留给 C-GRAPH / C-METRICS / C-TASK。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 98000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.66 |
| cost_warn | green |
