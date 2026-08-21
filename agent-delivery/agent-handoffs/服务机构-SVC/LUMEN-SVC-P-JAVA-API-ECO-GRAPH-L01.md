# LUMEN-SVC-P-JAVA-API-ECO-GRAPH-L01 · POST /topic/v1/service/eco-graph

> 日期：2026-08-21  
> Task：`LUMEN-SVC-P-JAVA-API-ECO-GRAPH-L01`  
> 总控：[`LUMEN-SVC-P-长任务总控.md`](./LUMEN-SVC-P-长任务总控.md)（§7 已生效）  
> 仓：`lumen-svc-platform` · `origin/dev`  
> 故事：`US-SVC-ECO-01`（本叶只出生态图谱读面 REST，不做前端、不改 Python）

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
| 说明 | 复用已有 `gkxlumen-topic-svc` 查询门面 + Feign，只加一条 REST。未用 YAGNI 跳过 OTel、空态诚实、handoff、图即契约、D9。Java 不查 ADS、不写 nGQL、不重算密度、不发明边类型、不填迈瑞/华为 fixture。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机会话未挂载 Headroom MCP。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-LINEAGE`（消费，不改工厂边）；`LUMEN-SVC-P-JAVA-API-ECO-GRAPH-L01-SEQ`（本叶生态图谱） |
| 图 diff | LINEAGE 边未改。本叶把 SZ SEQ 的 eco-graph 虚线改成实线：50892 → gateway `/svc/**` → `gkxlumen-topic-svc` `POST /topic/v1/service/eco-graph` → `lumen-topic-py` `POST /internal/gkx-svc/eco/graph`（body 含双滤镜 `filter=orgs\|orgs_and_actors`）→ Python 读 `demo_gkx_chain` hang。REC-LIST 仍虚线。禁止事项未变：不写正式库、对拍前不写 Demo ADS/图、不对前端暴露 `/internal`、禁 Feign `lumen-algo-py` 与 `demo-*`、禁 `/api/svc`、禁 Java fixture / 迈瑞华为 / 30999 填点、禁轻量表格冒充图谱、禁用生态密度覆盖子网列名。 |
| 会签态 | `SVC-STORAGE-LINEAGE` 随 `01-data-flow.md` frontmatter：`approved`（`human:淮政玮` · 2026-08-19 流图；2026-08-20 选 B 增补 LINEAGE，**不改** §1 工厂边） |

### L2 消费（不改边）

本叶只读消费 [`storage/SVC/01-data-flow.md`](../../data/data-design/storage/SVC/01-data-flow.md) §1.1 `SVC-STORAGE-LINEAGE`：生态图谱读 Demo `demo_gkx_chain` 一张 hang（切法 A 双滤镜）；Java **不扫表、不写 nGQL**；经 Feign 让 `lumen-topic-py` 出 `nodes`/`edges` + 子网密度 `subnet_density` 与生态密度 `eco_density` **并排**。缺图 / hang 无对端则 `nodes=[]` `edges=[]` `empty=true`。不写工厂边、不灌数。

### L4 本叶 SEQ · `LUMEN-SVC-P-JAVA-API-ECO-GRAPH-L01-SEQ`

```mermaid
sequenceDiagram
  participant FE as lumen-ui-topic
  participant GW as gkxlumen-platform-gateway
  participant JAVA as gkxlumen-topic-svc
  participant PY as lumen-topic-py<br/>gkxlumen-platform-search-py
  participant G as demo_gkx_chain
  Note over FE,GW: 不对前端暴露 /internal；禁止 /api/svc
  FE->>GW: POST /svc/topic/v1/service/eco-graph<br/>filter=orgs|orgs_and_actors
  GW->>JAVA: GlobalFilter 剥 svc → /topic/v1/service/eco-graph
  JAVA->>PY: POST /internal/gkx-svc/eco/graph<br/>透传 body（含 filter）
  PY->>G: 读 hang；滤镜只滤显示，不换空间
  alt 有点/边
    G-->>PY: nodes/edges
    PY-->>JAVA: {code:0,msg,data} 黄灯 Q062/Q-SVCCHAIN-03/Q-SVC-010 原样<br/>subnet_density 与 eco_density 并排
    JAVA-->>GW: HTTP 200 R.ok(data) 原样上送，不改绿、不重算密度
  else 缺图 / hang 无对端
    G-->>PY: 无对端或不画
    PY-->>JAVA: empty=true nodes=[] edges=[]
    JAVA-->>GW: HTTP 200 诚实空图<br/>禁止迈瑞华为 fixture、禁止 30999、禁止轻量表格冒充图谱
  end
  JAVA-xPY: Feign 不可达
  JAVA-->>GW: HTTP 200 R.ok empty=true nodes=[] edges=[] section=eco_graph<br/>禁止 5xx、禁止 fixture、禁止发明 gap、禁止用 0 冒充有图
  FE->>GW: POST /svc/topic/v1/service/search/orgs
  GW->>JAVA: /topic/v1/service/search/orgs（本叶不改契约）
  FE->>GW: POST /svc/topic/v1/service/profile/get
  GW->>JAVA: /topic/v1/service/profile/get（本叶不改契约）
  FE->>GW: GET /svc/topic/v1/service/health
  GW->>JAVA: /topic/v1/service/health
  JAVA->>PY: POST /internal/gkx-svc/health
  JAVA-->>GW: HTTP 200；python 失败 degraded=true
  FE->>GW: POST /svc/topic/v1/service-portal/key-orgs
  GW->>JAVA: /topic/v1/service-portal/key-orgs（本叶不改契约）
  FE -.-> GW: POST /svc/topic/v1/service/rec-list（REC-LIST）
  Note over JAVA,PY: Feign 仅 lumen-topic-py；禁 lumen-algo-py；禁 demo-*
  Note over JAVA,G: Java 不直连 Nebula；N&lt;2 密度记 0 由 Python 出
```

| 生产者 | 消费者 | 触发 | 失败语义 | 禁止事项 |
|---|---|---|---|---|
| `gkxlumen-topic-svc` eco-graph | 50892 经网关 | 在线 POST `/topic/v1/service/eco-graph` | Python 空 → HTTP 200 `empty=true` `nodes=[]` `edges=[]`；Feign 失败同左，**不** 5xx、**不** fixture、**不** 迈瑞华为、**不** 发明密度 0 | `/api/svc`；Java 查 ADS / 写 nGQL / 重算密度 / 填点；把 SVC 塞进薄 `gkxlumen-topic`；用生态密度覆盖子网列名 |
| `lumen-topic-py` `POST /internal/gkx-svc/eco/graph` | 本叶 Feign | Java 透传 body（`filter`） | 连不上 → 诚实空图；有图则黄灯 Q062 / Q-SVCCHAIN-03 / Q-SVC-010 原样透传，不改绿 | Feign `lumen-algo-py`；Feign `demo-*`；对前端暴露 `/internal`；30999 常量填点；轻量表格 JSON 冒充图谱 |
| Nebula `demo_gkx_chain` hang（Python 读） | 生态图谱 | 同一 hang 双滤镜；对端不在 hang 则不画 | hang 无对端 = 空画，不用迈瑞华为冒充关联主体 | 本叶写 Demo ADS/图；直连 nGQL；扩 async-service / CHAIN analysisType |
| search/orgs + profile/get + health + portal/*（已有） | 自检 | 本叶不改 | empty / items=[] / data=null / degraded 契约保持 | 本叶改坏 search empty、profile null、health degraded 或 portal 契约 |

## 范围与实现

在 SZ 查询门面只加一条生态图谱 REST：

- `POST /topic/v1/service/eco-graph`（网关外网 `/svc/topic/v1/service/eco-graph`）
- Feign `POST /internal/gkx-svc/eco/graph`，body 原样透传（建议 `filter=orgs|orgs_and_actors`）
- 拆 Python `{code,msg,data}` 后 `R.ok(data)`；`nodes` / `edges` / `subnet_density` / `eco_density` / `empty` / `gap` / `pending_client_confirm` 不改写；不改绿
- Feign 失败：HTTP 200 + `empty=true` + `nodes=[]` + `edges=[]` + `section=eco_graph`，不填迈瑞/华为、不用 30999、不发明 `gap`、不发明密度 0、不给 `items` 表
- search/orgs、profile/get、health、portal/* 未改

**非范围**：REC-LIST；TASK-* / CHAIN / async-service；改 Python / 前端；写 Demo ADS/图。

## 偏离说明

- PATH 上默认 `mvn` 仍是 3.6.2（compiler-plugin 3.14.0 要求 ≥3.6.3）。本叶用本机 `D:\temp\apache-maven-3.9.9` + Zulu 17 跑通模块单测。
- Feign 失败时 Java **不发明** `gap: Q062` / `Q-SVCCHAIN-03` / `Q-SVC-010`（黄灯只随 Python 包络透传）；只给诚实空图。
- 并行叶 `LUMEN-SVC-P-PY-MIDDLE-ECO-L01` 未在本叶改 Python；Python 未上线时 Feign 失败 = HTTP 200 诚实空图（与门户叶一致）。
- 不把旧 `LUMEN-SVC-JAVA-*` 当 `depends_on`。

## 产物清单

| 产物 | 路径 |
|------|-----|
| Controller | `repos/lumen-svc-platform/gkxlumen-topic-svc/gkxlumen-topic-svc-biz/.../ServiceFacadeController.java` |
| Feign | `.../feign/RemoteSvcPythonClient.java` · api `RemoteTopicSvcService.java` |
| 透传 | `.../service/impl/ServiceFacadeServiceImpl.java` |
| 测试 | `ServiceFacadeControllerTest` · `ServiceFacadeServiceImplTest` |
| 本 handoff | `agent-handoffs/服务机构-SVC/LUMEN-SVC-P-JAVA-API-ECO-GRAPH-L01.md` |

## 测试结果

- [x] MockMvc：`POST /topic/v1/service/eco-graph` 透传双滤镜 + nodes/edges + `subnet_density`/`eco_density` 并排；empty 不造迈瑞华为、不给 items 表；Feign 失败不造假密度；search/orgs、profile/get、health 与 portal/* 仍映射
- [x] 服务单测：Python 双滤镜 body 原样透传；Q062 / Q-SVCCHAIN-03 / Q-SVC-010 透传不改绿；empty 不填迈瑞华为；Feign 5xx → `R.code=0` + `nodes=[]` `edges=[]` 无 gap、无密度 0；已有门户/检索契约未改
- [x] 本机 `mvn`（3.9.9 + Zulu 17）：`ServiceFacadeControllerTest` 29 · `ServiceFacadeServiceImplTest` 34，合计 63 Tests run, Failures: 0

## 验收证据

- [x] POST `/topic/v1/service/eco-graph` 经 Feign 打 `lumen-topic-py` `/internal/gkx-svc/eco/graph`；双滤镜字段透传；缺图/hang 无对端诚实空，禁迈瑞华为 fixture，禁轻量表格冒充图谱
- [x] 禁 `/api/svc`；禁 Feign `lumen-algo-py` 与 `demo-*`；Java 不写 nGQL；不改 portal/search/profile/CHAIN 契约
- [x] handoff 含 ponytail: full、cost 四字段、diagram_id、SEQ
- [x] `origin/dev` `5331c0e`；未标 `done`

## 遗留风险

- K8s 未注入 Python/Nebula 或并行 `PY-MIDDLE-ECO` 未上线时图谱为 `empty` / 空 `nodes`/`edges`（预期）；前端 D 叶须按空态展示，不能当 5xx，不能自行补迈瑞华为。
- `deploy:topic-svc` / 网关 Nacos 种子仍可能未灌；本叶不宣称 K8s rollout 已绿（E0 另叶）。
- REC-LIST 仍未出门面（留给后续叶，预期）。

## CI/CD（必填）

- 分支：`origin/dev`（`lumen-svc-platform`）
- commit：`5331c0e` `feat(svc): add POST /topic/v1/service/eco-graph [agent:api-agent]`
- pipeline URL：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines?ref=dev
- 部署 namespace / 镜像 tag：本叶未宣称 rollout
- K8s rollout：本叶未执行（E0 另叶）
- 本地：Maven 3.9.9 + Zulu 17，`Tests run: 63, Failures: 0`

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-topic-svc-biz`（Dockerfile + Helm env，BOOT 已有）
- Feign 失败：`ServiceFacadeServiceImpl` warn 日志 `svc eco-graph python unavailable`，不抛 5xx
- traceId（dev 抽样）：无（本叶未 rollout）
- Tempo / Loki：沿用平台 Java Agent

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ Java 不写算法、不扫 ADS、不重算密度、不发明边类型 |
| 2 | 前端 → Java → `/internal/*` | ✅ Feign `POST /internal/gkx-svc/eco/graph` |
| 3 | Nebula，禁 Neo4j | ✅ Java 不连图；只声明消费 `demo_gkx_chain` |
| 4 | 可观测 OTel | ✅ `OTEL_SERVICE_NAME=gkxlumen-topic-svc-biz` + Feign warn |
| 5 | CI | ✅ 测写在模块内；本叶不宣称绿 |
| 6 | demo2 不 merge lumen | ✅ N/A |
| 7 | 共享聚合 / 分仓 | ✅ 只改 `gkxlumen-topic-svc`，未塞进薄 `gkxlumen-topic` |
| 8 | 只读 ADS；不写库 | ✅ Java 不查表；Python 只读 |
| 9 | D8 | N/A 无 UI |
| 10 | D9 | ✅ 不造假图；缺图 `nodes=[]`；黄灯 Q062 / Q-SVCCHAIN-03 / Q-SVC-010 透传不改绿；双密度并排 |
| 11 | D10 | N/A |
| 12 | D12 不调 demo-* | ✅ Feign 仅 `lumen-topic-py`；禁 `demo-*` 与 `lumen-algo-py` |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 120000（估 in+out；source: session_estimate） |
| model_used | `claude-sonnet-4.5`（registry enum；本会话 Cursor Grok 4.6，enum 无 grok） |
| actual_cost | 0.72（api 75/25 × Sonnet $3/$15 per M） |
| cost_warn | `green` |

## 联调确认

联调通过（代码侧）：生态图谱 REST / Feign / 双滤镜字段透传 / nodes·edges + 双密度并排 / 缺图诚实空 / search·profile·health·portal 契约未改，可对接即将发布的 `gkx_svc_service` `POST /internal/gkx-svc/eco/graph`。下一叶：按 DAG（REC-LIST 或对应 D 叶）。请 coordinator AV-0，**本叶不自行标 done**。
