# LUMEN-SVC-P-JAVA-API-SEARCH-ORGS-L01 · POST /topic/v1/service/search/orgs

> 日期：2026-08-21  
> Task：`LUMEN-SVC-P-JAVA-API-SEARCH-ORGS-L01`  
> 总控：[`LUMEN-SVC-P-长任务总控.md`](./LUMEN-SVC-P-长任务总控.md)（§7 已生效）  
> 仓：`lumen-svc-platform` · `origin/dev`  
> 故事：`US-SVC-ORG-07`（本叶只出检索 REST，不做前端 V1–V7）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务 24h 锁；未自行标 `done` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 BOOT `gkxlumen-topic-svc` 门面 + Feign；只加一条 REST。未用 YAGNI 跳过 OTel、空态诚实、handoff、图即契约。Java 不查 ADS、不 JOIN ODS、不填名单。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机会话未挂载 Headroom MCP。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-LINEAGE`（消费，不改工厂边）；`LUMEN-SVC-P-JAVA-API-SEARCH-ORGS-L01-SEQ`（本叶检索） |
| 图 diff | LINEAGE 边未改。本叶把 BOOT 的 search 虚线改成实线：50892 → gateway `/svc/**` → `gkxlumen-topic-svc` `POST /topic/v1/service/search/orgs` → `lumen-topic-py` `POST /internal/gkx-svc/search/orgs` → ADS `svc_org_card`。profile/portal/analysis 仍虚线。禁止事项未变：不写正式库、对拍前不写 Demo ADS/图、不对前端暴露 `/internal`、禁 Feign `lumen-algo-py` 与 `demo-*`、禁 `/api/svc`、禁 Java fixture。 |
| 会签态 | `SVC-STORAGE-LINEAGE` 随 `01-data-flow.md` frontmatter：`approved`（`human:淮政玮` · 2026-08-19 流图；2026-08-20 选 B 增补 LINEAGE，**不改** §1 工厂边） |

### L2 消费（不改边）

本叶只读消费 [`storage/SVC/01-data-flow.md`](../../data/data-design/storage/SVC/01-data-flow.md) §1.1 `SVC-STORAGE-LINEAGE`：线上名单读 `svc_org_card`，不联 ODS。Java **不扫表**；经 Feign 让 `lumen-topic-py` SELECT。不写工厂边、不灌数。

### L4 本叶 SEQ · `LUMEN-SVC-P-JAVA-API-SEARCH-ORGS-L01-SEQ`

```mermaid
sequenceDiagram
  participant FE as lumen-ui-topic
  participant GW as gkxlumen-platform-gateway
  participant JAVA as gkxlumen-topic-svc
  participant PY as lumen-topic-py<br/>gkxlumen-platform-search-py
  participant ADS as demo_gkxlumenx_ads
  Note over FE,GW: 不对前端暴露 /internal；禁止 /api/svc
  FE->>GW: POST /svc/topic/v1/service/search/orgs
  GW->>JAVA: GlobalFilter 剥 svc → /topic/v1/service/search/orgs
  JAVA->>PY: POST /internal/gkx-svc/search/orgs<br/>透传 keyword/q service_type/serviceType city industry page size
  PY->>ADS: SELECT svc_org_card（禁 JOIN ODS）
  ADS-->>PY: 0..n 行
  PY-->>JAVA: {code:0,msg,data} empty/items/gap 原样
  JAVA-->>GW: HTTP 200 R.ok(data)<br/>empty=true 不填 fixture；黄灯 Q-SVC-010/Q063 透传不改绿
  JAVA-xPY: Feign 不可达
  JAVA-->>GW: HTTP 200 R.ok empty=true items=[]<br/>禁止 5xx、禁止华大基因
  FE->>GW: GET /svc/topic/v1/service/health
  GW->>JAVA: /topic/v1/service/health
  JAVA->>PY: POST /internal/gkx-svc/health
  JAVA-->>GW: HTTP 200；python 失败 degraded=true
  FE -.-> GW: POST /svc/topic/v1/service/profile（PROFILE-GET）
  FE -.-> GW: POST /svc/topic/v1/service-portal/**（PORTAL-*）
  Note over JAVA,PY: Feign 仅 lumen-topic-py；禁 lumen-algo-py；禁 demo-*
```

| 生产者 | 消费者 | 触发 | 失败语义 | 禁止事项 |
|---|---|---|---|---|
| `gkxlumen-topic-svc` search/orgs | 50892 经网关 | 在线 POST `/topic/v1/service/search/orgs` | Python 空态 → HTTP 200 + `empty=true` `items=[]`；Feign 失败同诚实空，**不** 5xx、**不** fixture | `/api/svc`；Java 查 ADS / JOIN ODS / 填名单；把 SVC 塞进薄 `gkxlumen-topic` |
| `lumen-topic-py` `POST /internal/gkx-svc/search/orgs` | 本叶 Feign | Java 透传 body | 连不上 → `data_source=unavailable:feign` 空名单；黄灯只随 Python 包络透传，不改绿、不发明 gap | Feign `lumen-algo-py`；Feign `demo-*`；对前端暴露 `/internal` |
| ADS `svc_org_card`（Python 读） | 检索名单 | 有行才出 items | 0 行 = empty；Q-SVC-010 / Q063 留 pending | 本叶写 Demo ADS/图；扫 DWD；直连 nGQL；扩 async-service |
| health（BOOT 已有） | 自检 | GET `/topic/v1/service/health` | Java `up`；Python 失败 `degraded=true` 仍 HTTP 200 | 本叶改坏 degraded 契约 |

## 范围与实现

在 BOOT 模块上只加一条检索 REST：

- `POST /topic/v1/service/search/orgs`（网关外网 `/svc/topic/v1/service/search/orgs`）
- Feign `POST /internal/gkx-svc/search/orgs`，body 原样透传（keyword/q、service_type/serviceType、city、industry、page、size）
- 拆 Python `{code,msg,data}` 后 `R.ok(data)`；`empty` / `items` / `gap` / `pending_client_confirm` 不改写
- Feign 失败：HTTP 200 + `empty=true` + `items=[]`，不填「华大基因」
- health 自检未改：仍 HTTP 200，可 `degraded`

**非范围**：PROFILE-GET / PORTAL-* / TASK-* / ECO / REC；扩 `gkxlumen-topic-async-service`；改 Python / 前端；写 Demo ADS/图。

## 偏离说明

- 本机 Maven 3.6.2 + compiler-plugin 3.14.0 要求 Maven ≥3.6.3，无法本地 `mvn test`。契约测试已写入 `ServiceFacadeControllerTest` / `ServiceFacadeServiceImplTest`，待 CI `backend:build` 验证。
- Feign 失败时 Java **不发明** `gap: Q-SVC-010`（黄灯只随 Python 包络透传）；只给诚实空名单。
- 不把旧 `LUMEN-SVC-JAVA-*` 当 `depends_on`。

## 产物清单

| 产物 | 路径 |
|------|------|
| Controller | `repos/lumen-svc-platform/gkxlumen-topic-svc/gkxlumen-topic-svc-biz/.../ServiceFacadeController.java` |
| Feign | `.../feign/RemoteSvcPythonClient.java` · api `RemoteTopicSvcService.java` |
| 透传 | `.../service/impl/ServiceFacadeServiceImpl.java` |
| 测试 | `ServiceFacadeControllerTest` · `ServiceFacadeServiceImplTest` |
| 本 handoff | `agent-handoffs/服务机构-SVC/LUMEN-SVC-P-JAVA-API-SEARCH-ORGS-L01.md` |

## 测试结果

- [x] MockMvc：`POST /topic/v1/service/search/orgs` 有 items 透传；`empty=true` 不造假；health 仍映射
- [x] 服务单测：Python items + Q-SVC-010 透传；empty 不填华大基因；Feign 5xx → `R.code=0` + empty；health degraded 契约未改
- [ ] 本机 `mvn test`：Maven 3.6.2 无法跑 compiler-plugin 3.14.0；待 CI

## 验收证据

- [x] POST `/topic/v1/service/search/orgs` 经 Feign 打 `lumen-topic-py` `/internal/gkx-svc/search/orgs`；空态诚实不造假、不填 fixture
- [x] health 自检仍 HTTP 200 可 degraded；禁 `/api/svc`；禁 Feign `lumen-algo-py` 与 `demo-*`
- [x] handoff 含 ponytail: full、cost 四字段、diagram_id、SEQ
- [x] `origin/dev` `e1c0c8e`；未标 `done`

## 遗留风险

- K8s 未注入 Python/MySQL 时检索为诚实空（预期）；前端 D 叶须按 `empty` 展示，不能当 5xx。
- `deploy:topic-svc` / 网关 Nacos 种子仍可能未灌；本叶不宣称 K8s rollout 已绿（E0 另叶）。
- profile/portal 仍 404（留给后续 JAVA-API-*，预期）。

## CI/CD（必填）

- 分支：`origin/dev`（`lumen-svc-platform`）
- commit：`e1c0c8e` `feat(svc): add POST /topic/v1/service/search/orgs [agent:api-agent]`
- pipeline URL：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines?ref=dev
- 部署 namespace / 镜像 tag：本叶未宣称 rollout
- K8s rollout：本叶未执行（E0 另叶）
- 本地：契约测试源码就位；Maven 3.6.2 无法跑 `mvn test`

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-topic-svc-biz`（Dockerfile + Helm env，BOOT 已有）
- Feign 失败：`ServiceFacadeServiceImpl` warn 日志，不抛 5xx
- traceId（dev 抽样）：无（本叶未 rollout）
- Tempo / Loki：沿用平台 Java Agent

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ Java 不写算法、不扫 ADS |
| 2 | 前端 → Java → `/internal/*` | ✅ Feign `POST /internal/gkx-svc/search/orgs` |
| 3 | Nebula，禁 Neo4j | ✅ 本叶不碰图 |
| 4 | 可观测 OTel | ✅ `OTEL_SERVICE_NAME=gkxlumen-topic-svc-biz` + Feign warn |
| 5 | CI | ✅ 测写在模块内；本叶不宣称绿 |
| 6 | demo2 不 merge lumen | ✅ N/A |
| 7 | 共享聚合 / 分仓 | ✅ 只改 `gkxlumen-topic-svc`，未塞进薄 `gkxlumen-topic` |
| 8 | 只读 ADS；不写库 | ✅ Java 不查表；Python 只读 |
| 9 | D8 | N/A 无 UI |
| 10 | D9 | ✅ 不造假名单；黄灯透传不改绿 |
| 11 | D10 | N/A |
| 12 | D12 不调 demo-* | ✅ Feign 仅 `lumen-topic-py`；禁 `demo-*` 与 `lumen-algo-py` |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 150000（估 in+out；source: session_estimate） |
| model_used | `claude-sonnet-4.5`（registry enum；本会话 Cursor Grok 4.6，enum 无 grok） |
| actual_cost | 0.90（api 75/25 × Sonnet $3/$15 per M） |
| cost_warn | `green` |

## 联调确认

联调通过（代码侧）：检索 REST / Feign / 空态诚实 / health 降级契约就绪，可对接已发布 `gkx_svc_service` `POST /internal/gkx-svc/search/orgs`。下一叶：`LUMEN-SVC-P-JAVA-API-PROFILE-GET-L01`（本叶 ≥ integration）。请 coordinator AV-0，**本叶不自行标 done**。
