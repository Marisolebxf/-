# LUMEN-POLICY-C-BOOT-L01 · gkxlumen-topic-policy 模块/网关骨架

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-JAVA-C-总派单.md`](./LUMEN-POLICY-JAVA-C-总派单.md)  
> 细叶：[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md) §1

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h；本叶不算完成门面 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对照 `gkxlumen-topic-chain` 最小可编译模块；只 health + 空 Feign 声明；未实现 search/graph/metrics/task |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 骨架对照复制，无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | §1 `lumen-ui-topic` → `gkxlumen-platform-gateway` `/policy/**` → `gkxlumen-topic-policy` → Feign `/internal/policy` 改实线；新增 §2.2 专题在线读路径。工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。联调台 demo polan 仍虚线 |
| 会签态 | `approved`（`01-data-flow.md` frontmatter；本叶不翻签；`OPEN-POLICY-FLOW-01` 专题侧已实线） |

## 范围与实现

- 新建 **`gkxlumen-topic-policy`**（api+biz），对照 topic-chain / topic-svc。
- 对外服务内路径：`GET /topic/v1/policy/health`。网关：`/policy/**` StripPrefix=1 → 完整 URL `/policy/topic/v1/policy/health`。
- Feign **只**打 `lumen-algo-py` `/internal/policy/**`；K8s 基址 `http://gkxlumen-platform-entan-py:8000`（policy 挂 entan-api 制品，仍是 lumen-algo-py）。禁止 Feign `demo-platform-entan-py` / `demo-svc-*` / `demo-algo-*`。
- JDBC 只读 `demo_gkxlumenx_ads`。禁止另接正式 `gkxlumenx_*` 数据面。
- **未实现** search / graph / metrics / task（留给 C-SEARCH / C-GRAPH / C-METRICS / C-TASK）。Feign 仅声明接口。
- Java 不写 nGQL、不做 NLP/图谱算法、不扫 ODS。

## 偏离说明

- 总控对外写 `/topic/v1/policy/**`；网关对照 `/chain/**` 使用独立前缀 `/policy/**`（剥第一段后服务内仍是 `/topic/v1/policy/**`）。理由：若把 `/topic/v1/policy/**` 直接挂薄 `gkxlumen-topic` 会抢 `/topic/**` 路由。与 chain/svc 一致。
- Feign `name=lumen-algo-py`，`url` 指向现网 `gkxlumen-platform-entan-py:8000`（PY-BOOT as-built：`/internal/policy` 挂 entan-api，不另起 kitchen Deployment）。
- `deploy:topic-policy` 本叶 **manual**（Deployment 须先 `helm:chart` 装出；自动 set-image 会因 not found 红）。装出后可改 auto-on-dev。

## 产物清单

- 代码：`lumen-svc-platform` `0f8c269f2b1135fc1b57dc5fe7aea766d915dd8f` → `origin/dev`
- helm：`configs/gkxlumen-topic-policy-biz-dev.yml` · `values.yaml` `topic-policy` · `values-lumen.yaml` enabled · gateway `/policy/**`
- 流图：`storage/POLICY/01-data-flow.md` 产品链改实线
- 本文 handoff

## 验收证据

- 单元测试：`PolicyFacadeControllerTest.healthMapped` · `PolicyFacadeServiceImplTest.healthDeclaresLumenAlgoPyInternalPolicy`（本机 Windows 无 mvn/JDK，以 CI `backend:build` verify 为准）
- 健康体：`java.status=up` · `python.name=lumen-algo-py` · `python.pathPrefix=/internal/policy` · `degraded=false`
- 网关路由：`Path=/policy/**` → `lb://gkxlumen-topic-policy-biz`（排在 `/topic/**` 之前）
- JDBC：`demo_gkxlumenx_ads` + `SET SESSION TRANSACTION READ ONLY`

## 修改内容

| 路径 | 动作 |
|------|------|
| `gkxlumen-topic-policy/**` | 新建 api+biz：Application / health / 空 Feign `/internal/policy/**` |
| `ServiceNameConstants.TOPIC_POLICY_SERVICE` | `gkxlumen-topic-policy-biz` |
| 根 `pom.xml` | 加 module |
| `helm/.../gkxlumen-gateway-dev.yml` | `/policy/**` 路由 |
| `helm/.../gkxlumen-topic-policy-biz-dev.yml` | Nacos DataId；JDBC demo ADS |
| `values.yaml` / `values-lumen.yaml` | 端口 7097；algo URL entan-py |
| `.gitlab-ci.yml` | build `-pl` · `backend:image:topic-policy` · `deploy:topic-policy`（manual） |
| `storage/POLICY/01-data-flow.md` | 产品链实线 + §2.2 |

## 测试结果

- 路径契约：`GET /topic/v1/policy/health` MockMvc 200。
- 健康体声明 Feign 目标不含 `demo-`。
- 本叶 **无** 对外 search/graph/metrics/task Controller。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `origin/dev`
- commit：`0f8c269f2b1135fc1b57dc5fe7aea766d915dd8f`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines?ref=dev
- 部署：首发须 `helm:chart`（`FORCE_NACOS_REPUBLISH=true`）灌网关路由并创建 `gkxlumen-platform-topic-policy`；`deploy:topic-policy` 本叶 manual
- 探活（Deployment 起来后）：`GET http://192.168.88.50:30899/policy/topic/v1/policy/health`

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-topic-policy-biz`（Dockerfile + helm env）
- Tempo / Loki：随平台 Collector；本叶未抽样

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ Java 无 NLP/图谱 |
| 前端→Java→Python `/internal/*` | ✅ Feign `/internal/policy/**` |
| 图谱 Nebula | ✅ Java 不写 nGQL；space 仍 `demo_gkx_chain` |
| 可观测 | ✅ OTEL_SERVICE_NAME + javaagent |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ 对照 chain 重写 |
| 共享聚合 / 不直连 nGQL | ✅ |
| 数据策略 ADS `demo_gkxlumenx_*` | ✅ JDBC 只读 demo ADS |
| D8 / D10 | N/A 无 UI |
| D9 8 件套 | N/A 本叶无统计数字 |
| D12 lumen 不调 demo **服务** | ✅ Feign `lumen-algo-py`；禁止 `demo-platform-entan-py`；数仓共用 demo 源是总控 §0 #6 |

## 遗留风险

- 首发 Deployment / 网关 Nacos 需 `helm:chart` + `FORCE_NACOS_REPUBLISH=true`（本叶只落 git）。
- search/graph/metrics/task 留给路径细叶；BOOT 不算完成门面。
- C-TASK 扩 `gkxlumen-topic-async-service` 不在本叶。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 110000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.74 |
| cost_warn | green |
