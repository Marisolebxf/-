# LUMEN-POLICY-C-GRAPH-L01 · GET /topic/v1/policy/graph 只读

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-JAVA-C-总派单.md`](./LUMEN-POLICY-JAVA-C-总派单.md)  
> 细叶：[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md) §1  
> 前序：[`LUMEN-POLICY-C-SEARCH-L01.md`](./LUMEN-POLICY-C-SEARCH-L01.md) · [`LUMEN-POLICY-PY-JOB-L01.md`](./LUMEN-POLICY-PY-JOB-L01.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h；本叶只做 graph 只读，不做 metrics/task |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对照 C-SEARCH：Controller 薄转发 + Feign 透传 Map 查询参数 + 拆 Python `{code,msg,data}`；`source` 走 `copyMap` 原样上送，禁止改成 nebula；未新建 DTO；未改 helm；未实现 metrics/task；未暴露 hang/ner/intra |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 门面透传，无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | §2.2 补 graph 只读边：Java Feign `GET /internal/policy/graph`（center/steps/limit 透传）→ polan 优先 Nebula `demo_gkx_chain`，失败 ADS `policy_graph_*` 且 `source≠nebula`。工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。 |
| 会签态 | `approved`（`01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

- 对外：`GET /topic/v1/policy/graph`。网关仍 `/policy/**`（BOOT）。查询参数 `center/steps/limit` 原样透传。
- Feign 只打 `lumen-algo-py`：`GET /internal/policy/graph`。基址 `http://gkxlumen-platform-entan-py:8000`。
- `source` 诚实：Python Nebula 失败返回 `mysql`/`ads` 等；Java `copyMap` 原样上送，禁止改成 `nebula`。Feign 挂时 Java 填 `source=unavailable`，仍不是 nebula。
- 空态 / 下游失败：HTTP 200 + 空 `nodes`/`edges` + `honesty.empty` + `fabricated=false`；Feign 挂 `degraded=true`。禁止 5xx 填假数、禁止 fixture。
- **禁止**把 `POST /v1/policy/graph/hang` / ner / intra 暴露给专题前端（Controller 无 POST；Feign 无 hang 路径）。写 hang 留算法库联调台。
- Java 不写 nGQL/NLP；禁止 Feign `demo-*`。JDBC 仍 `demo_gkxlumenx_*`。本叶无 metrics/task。

## 偏离说明

- Python 图谱 `source` 在 `data` 顶层（非 honesty 内）；Java 透传顶层 `source`，Feign 失败才补 honesty + `source=unavailable`。
- 本机 Windows 无 JDK/mvn；单测以 CI `backend:build` verify 为准（同 SEARCH/BOOT）。
- 未改 helm（BOOT 已挂 `/policy/**`、algo URL）。K8s 首发仍须遗留 `helm:chart`，本叶不挡编码。

## 产物清单

- 代码：`lumen-svc-platform` `36e5a7237f1cb901bd25639aab0b1e42704cc60a` → `origin/dev`
- 流图：`storage/POLICY/01-data-flow.md` §2.2 graph 读边
- 本文 handoff

## 验收证据

- 单元测试：`PolicyFacadeControllerTest` graph 命中 / 空态 / hang 404；`PolicyFacadeServiceImplTest` 透传、Python `source=mysql` 不被改写、Feign 失败 `source≠nebula`、Feign path `/internal/policy/graph` 且无 hang
- 对外：`GET /topic/v1/policy/graph`
- Feign：`GET /internal/policy/graph` · name=`lumen-algo-py`
- source 诚实：Python 回 `mysql` → Java 仍 `mysql`；Feign 挂 → `unavailable`，均 ≠ nebula
- 空态：`nodes=[]` / `edges=[]` + `fabricated=false`；下游挂 `degraded=true`，`R.code=0`

## 修改内容

| 路径 | 动作 |
|------|------|
| `PolicyFacadeController` | 加 `GET /graph`（静态段优先于 `/{id}`）；无 POST hang |
| `PolicyFacadeService` + `Impl` | 透传 Python data；`source` copyMap 不改写；Feign 失败诚实空 |
| `RemotePolicyPythonClient` | graph 改为 `@RequestParam Map` 透传；不声明 hang/ner/intra |
| `RemoteTopicPolicyService` | 对外 Feign 补 graph |
| `PolicyFacadeControllerTest` / `PolicyFacadeServiceImplTest` | MockMvc graph、Feign path、source 不改写、hang 未映射 |
| `storage/POLICY/01-data-flow.md` | §2.2 graph 读边 |

## 测试结果

- MockMvc：`GET /topic/v1/policy/graph` 命中透传 nodes/source；空态 nodes/edges 空且 source=mysql 不被改成 nebula。
- MockMvc：`POST /topic/v1/policy/graph/hang` 与 `POST /v1/policy/graph/hang` 均 404。
- Feign 注解：`name=lumen-algo-py`，path `/internal/policy/graph`，url/path 不含 `demo-`、不含 hang、不含 `/graph/` 写子路径。
- Service：Python `source=mysql` 原样上送；Feign 失败 `source=unavailable` 且 `honesty.fabricated=false`。
- 本机无 JDK，未跑 `mvn test`；以 CI `backend:build` 为准。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `origin/dev`
- commit：`36e5a7237f1cb901bd25639aab0b1e42704cc60a`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines?ref=dev
- 部署：不改 helm；首发 Deployment 仍须 `helm:chart`（遗留，不挡编码）；`deploy:topic-policy` 仍 BOOT 的 manual
- 探活：`GET http://10.50.69.111:30899/policy/topic/v1/policy/graph`（Deployment 起来后）

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-topic-policy-biz`（BOOT 已挂）
- Tempo / Loki：随平台 Collector；本叶未抽样

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ Java 无 NLP/图谱/nGQL |
| 前端→Java→Python `/internal/*` | ✅ Feign `/internal/policy/graph` |
| 图谱 Nebula | ✅ 只读 Feign；失败 source 诚实，不假标 nebula |
| 可观测 | ✅ 复用 BOOT OTEL |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ 对照 SEARCH 重写 |
| 共享聚合 / 不直连 nGQL | ✅ |
| 数据策略 ADS `demo_gkxlumenx_*` | ✅ JDBC 未改 |
| D8 / D10 | N/A 无 UI |
| D9 8 件套 | N/A 本叶无统计数字 |
| D12 lumen 不调 demo **服务** | ✅ Feign `lumen-algo-py`；禁止 `demo-*`；数仓共用 demo 源是总控 §0 #6 |

## 遗留风险

- K8s 首发仍须 `helm:chart`；本叶未部署验证现网 graph。
- Nebula 空/失败返回 `source≠nebula`，前端 D 叶按空态或 ADS 镜像渲染。
- metrics/task 留给 C-METRICS / C-TASK。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 88000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.59 |
| cost_warn | green |
