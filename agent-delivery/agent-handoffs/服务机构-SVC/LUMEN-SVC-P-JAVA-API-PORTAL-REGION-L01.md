# LUMEN-SVC-P-JAVA-API-PORTAL-REGION-L01 · POST /topic/v1/service-portal/region-map

> 日期：2026-08-21  
> Task：`LUMEN-SVC-P-JAVA-API-PORTAL-REGION-L01`  
> 总控：[`LUMEN-SVC-P-长任务总控.md`](./LUMEN-SVC-P-长任务总控.md)（§7 已生效）  
> 仓：`lumen-svc-platform` · `origin/dev`  
> 故事：`US-SVC-PT-03`（本叶只出门户区域分布 REST，不做 50892 前端）

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
| 说明 | 复用 INDUSTRY 的 `gkxlumen-topic-svc` 门面 + Feign；只加一条 REST。未用 YAGNI 跳过 OTel、空态诚实、handoff、图即契约、D9。Java 不查 ADS、不把省名复制成国别、不用 0 冒充全球分布、不填 Demo 区级假点。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机会话未挂载 Headroom MCP。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-LINEAGE`（消费，不改工厂边）；`LUMEN-SVC-P-JAVA-API-PORTAL-REGION-L01-SEQ`（本叶区域分布） |
| 图 diff | LINEAGE 边未改。本叶把 INDUSTRY SEQ 的 portal region 虚线改成实线：50892 → gateway `/svc/**` → `gkxlumen-topic-svc` `POST /topic/v1/service-portal/region-map` → `lumen-topic-py` `POST /internal/gkx-svc/portal/region-map` → ADS `svc_region_dist`（`M_SVC_ORG_CNT`；有 country 才出 global，否则只出 province）。sz/keyorg 仍虚线。禁止事项未变：不写正式库、对拍前不写 Demo ADS/图、不对前端暴露 `/internal`、禁 Feign `lumen-algo-py` 与 `demo-*`、禁 `/api/svc`、禁 Java fixture、禁用 0 冒充全球分布、禁 Demo 区级假点。 |
| 会签态 | `SVC-STORAGE-LINEAGE` 随 `01-data-flow.md` frontmatter：`approved`（`human:淮政玮` · 2026-08-19 流图；2026-08-20 选 B 增补 LINEAGE，**不改** §1 工厂边） |

### L2 消费（不改边）

本叶只读消费 [`storage/SVC/01-data-flow.md`](../../data/data-design/storage/SVC/01-data-flow.md) §1.1 `SVC-STORAGE-LINEAGE`：线上区域分布读 ADS 指标四表 A1–A6 的 `region_dist`（`M_SVC_ORG_CNT`），不联 ODS。Java **不扫表**；经 Feign 让 `lumen-topic-py` SELECT。无 country 行则 `global=[]` `geo_level_used=province`；缺行则省/全球列表皆空。不写工厂边、不灌数。

### L4 本叶 SEQ · `LUMEN-SVC-P-JAVA-API-PORTAL-REGION-L01-SEQ`

```mermaid
sequenceDiagram
  participant FE as lumen-ui-topic
  participant GW as gkxlumen-platform-gateway
  participant JAVA as gkxlumen-topic-svc
  participant PY as lumen-topic-py<br/>gkxlumen-platform-search-py
  participant ADS as demo_gkxlumenx_ads
  Note over FE,GW: 不对前端暴露 /internal；禁止 /api/svc
  FE->>GW: POST /svc/topic/v1/service-portal/region-map
  GW->>JAVA: GlobalFilter 剥 svc → /topic/v1/service-portal/region-map
  JAVA->>PY: POST /internal/gkx-svc/portal/region-map<br/>透传 body
  PY->>ADS: SELECT svc_region_dist M_SVC_ORG_CNT geo_level=province
  PY->>ADS: SELECT svc_region_dist M_SVC_ORG_CNT geo_level=country
  alt 有 country 行
    ADS-->>PY: china + global
    PY-->>JAVA: {code:0,msg,data} geo_level_used=country；黄灯 Q-SVC-010 原样
    JAVA-->>GW: HTTP 200 R.ok(data) 原样上送，不改绿、不补 0
  else 无 country 有省
    ADS-->>PY: 仅 province
    PY-->>JAVA: china=省列表 global=[] geo_level_used=province
    JAVA-->>GW: HTTP 200 只出省，禁止把省名复制成国别
  else 缺行 / empty
    ADS-->>PY: 无 region_dist 行
    PY-->>JAVA: empty=true china=[] global=[]
    JAVA-->>GW: HTTP 200 诚实空列表<br/>禁止用 0 冒充全球分布、禁止 Demo 区级假点
  end
  JAVA-xPY: Feign 不可达
  JAVA-->>GW: HTTP 200 R.ok empty=true china=[] global=[] geo_level_used=province<br/>禁止 5xx、禁止 fixture、禁止 30999
  FE->>GW: POST /svc/topic/v1/service-portal/overview
  GW->>JAVA: /topic/v1/service-portal/overview（本叶不改契约）
  FE->>GW: POST /svc/topic/v1/service-portal/ranking
  GW->>JAVA: /topic/v1/service-portal/ranking（本叶不改契约）
  FE->>GW: POST /svc/topic/v1/service-portal/industry-distribution
  GW->>JAVA: /topic/v1/service-portal/industry-distribution（本叶不改契约）
  FE->>GW: POST /svc/topic/v1/service/search/orgs
  GW->>JAVA: /topic/v1/service/search/orgs（本叶不改契约）
  FE->>GW: POST /svc/topic/v1/service/profile/get
  GW->>JAVA: /topic/v1/service/profile/get（本叶不改契约）
  FE->>GW: GET /svc/topic/v1/service/health
  GW->>JAVA: /topic/v1/service/health
  JAVA->>PY: POST /internal/gkx-svc/health
  JAVA-->>GW: HTTP 200；python 失败 degraded=true
  FE -.-> GW: POST /svc/topic/v1/service-portal/shenzhen（PORTAL-SZ）
  FE -.-> GW: POST /svc/topic/v1/service-portal/key-orgs（PORTAL-KEYORG）
  Note over JAVA,PY: Feign 仅 lumen-topic-py；禁 lumen-algo-py；禁 demo-*
```

| 生产者 | 消费者 | 触发 | 失败语义 | 禁止事项 |
|---|---|---|---|---|
| `gkxlumen-topic-svc` portal/region-map | 50892 经网关 | 在线 POST `/topic/v1/service-portal/region-map` | Python 空列表 → HTTP 200 `china=[]` `global=[]` `empty=true`；无 country → 只出省；Feign 失败同左，**不** 5xx、**不** fixture、**不** `count=0` 冒充全球分布 | `/api/svc`；Java 查 ADS / 填国别 / 填 Demo 区级点；把 SVC 塞进薄 `gkxlumen-topic` |
| `lumen-topic-py` `POST /internal/gkx-svc/portal/region-map` | 本叶 Feign | Java 透传 body | 连不上 → 诚实空 china/global；有行则黄灯原样透传，不改绿 | Feign `lumen-algo-py`；Feign `demo-*`；对前端暴露 `/internal`；30999 常量填数；把省名复制成国别 |
| ADS `svc_region_dist`（Python 读） | 门户区域分布 | 有 country 才出 global；否则只出 province | 缺行 = 空列表，不用 0 冒充全球分布 | 本叶写 Demo ADS/图；扫 DWD；直连 nGQL；扩 async-service |
| overview + ranking + industry-distribution + search/orgs + profile/get + health（已有） | 自检 | 本叶不改 | empty / kpi omit / items=[] / by_service_type=[] / data=null / degraded 契约保持 | 本叶改坏 overview KPI、ranking items、industry 六类、search empty、profile null 或 health degraded |

## 范围与实现

在 INDUSTRY 模块上只加一条门户区域分布 REST：

- `POST /topic/v1/service-portal/region-map`（网关外网 `/svc/topic/v1/service-portal/region-map`）
- Feign `POST /internal/gkx-svc/portal/region-map`，body 原样透传
- 拆 Python `{code,msg,data}` 后 `R.ok(data)`；`china` / `global` / `geo_level_used` / `empty` / `gap` / `pending_client_confirm` 不改写；无 country 不把省名复制成国别
- Feign 失败：HTTP 200 + `empty=true` + `china=[]` + `global=[]` + `geo_level_used=province`，不填「南山区」、不用 30999、不发明 `gap`
- overview、ranking、industry-distribution、search/orgs、profile/get、health 未改

**非范围**：PORTAL-SZ / KEYORG；ECO-GRAPH；REC-LIST；TASK-* / CHAIN / async-service；改 Python / 前端；写 Demo ADS/图。

## 偏离说明

- PATH 上默认 `mvn` 仍是 3.6.2（compiler-plugin 3.14.0 要求 ≥3.6.3）。本叶用本机 `D:\temp\apache-maven-3.9.9` + Zulu 17 跑通模块单测。
- Feign 失败时 Java **不发明** `gap: Q-SVC-010`（黄灯只随 Python 包络透传）；只给诚实空 `china=[]` `global=[]`。
- 不把旧 `LUMEN-SVC-JAVA-*` 当 `depends_on`。

## 产物清单

| 产物 | 路径 |
|------|------|
| Controller | `repos/lumen-svc-platform/gkxlumen-topic-svc/gkxlumen-topic-svc-biz/.../ServicePortalFacadeController.java` |
| Feign | `.../feign/RemoteSvcPythonClient.java` · api `RemoteTopicSvcService.java` |
| 透传 | `.../service/impl/ServiceFacadeServiceImpl.java` |
| 测试 | `ServiceFacadeControllerTest` · `ServiceFacadeServiceImplTest` |
| 本 handoff | `agent-handoffs/服务机构-SVC/LUMEN-SVC-P-JAVA-API-PORTAL-REGION-L01.md` |

## 测试结果

- [x] MockMvc：`POST /topic/v1/service-portal/region-map` 有省/国透传；无 country 只出省；empty 不造 `count=0` 全球分布、不造南山区假点；Feign 失败不造假；overview、ranking、industry-distribution、search/orgs、profile/get 与 health 仍映射
- [x] 服务单测：Python china+global + Q-SVC-010 透传不改绿；无 country `global=[]` `geo_level_used=province`；empty 不填华大基因/南山区；Feign 5xx → `R.code=0` + `china=[]` `global=[]`；overview omit、ranking items、industry 六类、search empty、profile null 与 health degraded 契约未改
- [x] 本机 `mvn`（3.9.9 + Zulu 17）：`ServiceFacadeControllerTest` 19 · `ServiceFacadeServiceImplTest` 24，合计 43 Tests run, Failures: 0

## 验收证据

- [x] POST `/topic/v1/service-portal/region-map` 经 Feign 打 `lumen-topic-py` `/internal/gkx-svc/portal/region-map`；无 country 只出省、缺行诚实空、禁止用 0 冒充全球分布、禁止 Demo 区级假点、禁止 fixture
- [x] 禁 `/api/svc`；禁 Feign `lumen-algo-py` 与 `demo-*`；不改坏 overview/ranking/industry 契约
- [x] handoff 含 ponytail: full、cost 四字段、diagram_id、SEQ
- [x] `origin/dev` `6e5a4e7`；未标 `done`

## 遗留风险

- K8s 未注入 Python/MySQL 时区域分布为 `empty` / 空省空全球（预期）；前端 D 叶须按空态展示，不能当 5xx，不能自行补 0 或区级点。
- `deploy:topic-svc` / 网关 Nacos 种子仍可能未灌；本叶不宣称 K8s rollout 已绿（E0 另叶）。
- sz/keyorg 仍 404（留给后续 PORTAL-* 叶，预期）。

## CI/CD（必填）

- 分支：`origin/dev`（`lumen-svc-platform`）
- commit：`6e5a4e7` `feat(svc): add POST /topic/v1/service-portal/region-map [agent:api-agent]`
- pipeline URL：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines?ref=dev
- 部署 namespace / 镜像 tag：本叶未宣称 rollout
- K8s rollout：本叶未执行（E0 另叶）
- 本地：Maven 3.9.9 + Zulu 17，`Tests run: 43, Failures: 0`

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-topic-svc-biz`（Dockerfile + Helm env，BOOT 已有）
- Feign 失败：`ServiceFacadeServiceImpl` warn 日志，不抛 5xx
- traceId（dev 抽样）：无（本叶未 rollout）
- Tempo / Loki：沿用平台 Java Agent

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ Java 不写算法、不扫 ADS |
| 2 | 前端 → Java → `/internal/*` | ✅ Feign `POST /internal/gkx-svc/portal/region-map` |
| 3 | Nebula，禁 Neo4j | ✅ 本叶不碰图 |
| 4 | 可观测 OTel | ✅ `OTEL_SERVICE_NAME=gkxlumen-topic-svc-biz` + Feign warn |
| 5 | CI | ✅ 测写在模块内；本叶不宣称绿 |
| 6 | demo2 不 merge lumen | ✅ N/A |
| 7 | 共享聚合 / 分仓 | ✅ 只改 `gkxlumen-topic-svc`，未塞进薄 `gkxlumen-topic` |
| 8 | 只读 ADS；不写库 | ✅ Java 不查表；Python 只读 |
| 9 | D8 | N/A 无 UI |
| 10 | D9 | ✅ 不造假全球分布；无 country 只出省；缺行空列表；黄灯透传不改绿 |
| 11 | D10 | N/A |
| 12 | D12 不调 demo-* | ✅ Feign 仅 `lumen-topic-py`；禁 `demo-*` 与 `lumen-algo-py` |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 158000（估 in+out；source: session_estimate） |
| model_used | `claude-sonnet-4.5`（registry enum；本会话 Cursor Grok 4.6，enum 无 grok） |
| actual_cost | 0.95（api 75/25 × Sonnet $3/$15 per M） |
| cost_warn | `green` |

## 联调确认

联调通过（代码侧）：区域分布 REST / Feign / 无 country 只出省 / 缺行诚实空列表 / overview·ranking·industry·search·profile·health 契约未改，可对接已发布 `gkx_svc_service` `POST /internal/gkx-svc/portal/region-map`。下一叶：`LUMEN-SVC-P-JAVA-API-PORTAL-SZ-L01`（或按 DAG）。请 coordinator AV-0，**本叶不自行标 done**。
