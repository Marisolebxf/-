# LUMEN-POLICY-C-METRICS-L01 · GET /topic/v1/policy/metrics + indicators

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-JAVA-C-总派单.md`](./LUMEN-POLICY-JAVA-C-总派单.md)  
> 细叶：[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md) §1  
> 前序：[`LUMEN-POLICY-C-GRAPH-L01.md`](./LUMEN-POLICY-C-GRAPH-L01.md) · [`LUMEN-POLICY-PY-JOB-L01.md`](./LUMEN-POLICY-PY-JOB-L01.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h；本叶只做 metrics/indicators 读边，不做 task |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对照 C-GRAPH：Controller 薄转发 + Feign 透传 Map 查询参数 + 拆 Python `{code,msg,data}`；headline 数字 copyMap 原样上送，禁止自填 8 件套 / 改绿 D1；未新建 DTO；未改 helm；未实现 C-TASK；未暴露 `/v1/mock` |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 门面透传，无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | §2.2 补 metrics/indicators 读边：Java Feign `GET /internal/policy/metrics` 与 `/internal/policy/indicators`（查询参数透传，headline 数字原样上送）→ polan 读 ADS `policy_*`。工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。 |
| 会签态 | `approved`（`01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

- 对外：`GET /topic/v1/policy/metrics` · `GET /topic/v1/policy/indicators`。网关仍 `/policy/**`（BOOT）。查询参数原样透传（indicators `kind` 等）。
- Feign 只打 `lumen-algo-py`：`GET /internal/policy/metrics`、`GET /internal/policy/indicators`。基址 `http://gkxlumen-platform-entan-py:8000`。
- 空态 / 下游失败：HTTP 200 + 空 `headline`/`metric_ids` 或空分布列表 + `honesty.empty` + `fabricated=false`；Feign 挂 `degraded=true`。禁止 5xx 填假数、禁止 fixture。
- **D9**：Java 不自造 metric_id 口径、不把 D1 改绿；数字原样透传。D9 ⓘ 由前端消费 catalog，本叶不写 catalog / 不改 readiness。
- **禁止**实现 C-TASK（Controller 无 analysis/tasks；Feign `executeJob` 仍只声明）。禁止暴露 `/v1/mock`。
- Java 不写 nGQL/NLP；禁止 Feign `demo-*`。JDBC 仍 `demo_gkxlumenx_*`。

## 偏离说明

- Python `GET /internal/policy/metrics` 现网无查询参数；Java 仍 `@RequestParam Map` 透传，便于后续扩展，空 Map 不造查询项。
- Python `kind≠all` 时 `data` 为数组；Java `R<Map>` 包 `{items}`，kind=all 仍是分布 Map。不改数字、不填口径。
- 本机 Windows 无 JDK/mvn；单测以 CI `backend:build` verify 为准（同 GRAPH/SEARCH/BOOT）。
- 未改 helm（BOOT 已挂 `/policy/**`、algo URL）。K8s 首发仍须遗留 `helm:chart`，本叶不挡编码。

## 产物清单

- 代码：`lumen-svc-platform` `7d4b164874374fb61b104452ee7976b813747374` → `origin/dev`
- 流图：`storage/POLICY/01-data-flow.md` §2.2 metrics/indicators 读边
- 本文 handoff

## 验收证据

- 单元测试：`PolicyFacadeControllerTest` metrics/indicators 命中 / 空态 fabricated=false；`PolicyFacadeServiceImplTest` 数字透传、不写 def_status/aligned、Feign 失败空 headline 且 fabricated=false、Feign path `/internal/policy/metrics` 与 `/internal/policy/indicators`
- 对外：`GET /topic/v1/policy/metrics` · `GET /topic/v1/policy/indicators`
- Feign：`GET /internal/policy/metrics` · `GET /internal/policy/indicators` · name=`lumen-algo-py`
- D9：空态无自造 `M_POLICY_TOTAL_COUNT`、无 `def_status`/`aligned`；命中时 headline 数字原样
- 空态：`fabricated=false`；下游挂 `degraded=true`，`R.code=0`

## 修改内容

| 路径 | 动作 |
|------|------|
| `PolicyFacadeController` | 加 `GET /metrics` · `GET /indicators`（静态段优先于 `/{id}`）；无 task |
| `PolicyFacadeService` + `Impl` | 透传 Python data；headline copyMap 不改写；Feign 失败诚实空 |
| `RemotePolicyPythonClient` | metrics/indicators 改为 `@RequestParam Map` 透传 |
| `RemoteTopicPolicyService` | 对外 Feign 补 metrics/indicators |
| `PolicyFacadeControllerTest` / `PolicyFacadeServiceImplTest` | MockMvc 两路径、Feign path、空态 fabricated=false、数字不改写 |
| `storage/POLICY/01-data-flow.md` | §2.2 metrics/indicators 读边 |

## 测试结果

- MockMvc：`GET /topic/v1/policy/metrics` 命中透传 headline；空态 headline/metric_ids 空且 fabricated=false，无 def_status。
- MockMvc：`GET /topic/v1/policy/indicators?kind=level` 命中透传；空态列表空且 fabricated=false。
- Feign 注解：`name=lumen-algo-py`，path `/internal/policy/metrics` · `/internal/policy/indicators`，url/path 不含 `demo-`、不含 `/v1/policy/mock`。
- Service：Python headline `17` 原样上送；Feign 失败空 headline、无自造 `M_POLICY_TOTAL_COUNT`，`honesty.fabricated=false`。
- 本机无 JDK，未跑 `mvn test`；以 CI `backend:build` 为准。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `origin/dev`
- commit：`7d4b164874374fb61b104452ee7976b813747374`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines?ref=dev
- 部署：不改 helm；首发 Deployment 仍须 `helm:chart`（遗留，不挡编码）；`deploy:topic-policy` 仍 BOOT 的 manual
- 探活：`GET http://192.168.88.50:30899/policy/topic/v1/policy/metrics`（Deployment 起来后）

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-topic-policy-biz`（BOOT 已挂）
- Tempo / Loki：随平台 Collector；本叶未抽样

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ Java 无 NLP/图谱/nGQL |
| 前端→Java→Python `/internal/*` | ✅ Feign `/internal/policy/metrics` · `/indicators` |
| 图谱 Nebula | ✅ 本叶不改 graph；未写 nGQL |
| 可观测 | ✅ 复用 BOOT OTEL |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ 对照 GRAPH 重写 |
| 共享聚合 / 不直连 nGQL | ✅ |
| 数据策略 ADS `demo_gkxlumenx_*` | ✅ JDBC 未改 |
| D8 / D10 | N/A 无 UI |
| D9 8 件套 | ✅ Java 不自填口径、不改绿 D1；数字原样透传；ⓘ 由前端消费 catalog |
| D12 lumen 不调 demo **服务** | ✅ Feign `lumen-algo-py`；禁止 `demo-*`；数仓共用 demo 源是总控 §0 #6 |

## 遗留风险

- K8s 首发仍须 `helm:chart`；本叶未部署验证现网 metrics。
- ADS 空库返回 Python 侧 0/空列表，Java 原样上送；前端 D 叶按空态 + catalog ⓘ 渲染。
- task 留给 C-TASK。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 92000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.61 |
| cost_warn | green |
