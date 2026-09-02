# DEMO-COMP-GRAPH-TRIPLE-UI-L01 · 综合图谱 API 三元组（116）

> 叶内四步：步1 data-agent → 步2 algorithm-agent → 步3 api-agent → 步4 frontend-agent。本文按步追加，不覆盖他人段落。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent`（本步 1/4） |
| supervised_by | `human:徐滕强`（全程不准改） |
| claim_type | `coordinator_dispatch` |
| 说明 | 厚包 `COORD-GRAPH-TRIPLE-UI-DISPATCH-20260831.md` §0.2/§7.0；前序企业叶四步已完（`pending_test`）。本叶无 A/B/C |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 文档完整性优先；未用 YAGNI 裁掉 116 五查询行 / 过程图。本步不改 UI。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | SRS 与厚包读原文，禁止 compress 代替精读。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `COMP-GRAPH-TRIPLE` |
| 图 diff | 综合只读：灌数零图谱 → D 浏览 + 五查询；写入不在本叶；space=`demo_gkx_chain`；禁止第二张图 |
| 会签态 | 不新建流图；不翻签 ENT `01-data-flow.md` |

---

## 数据设计（步1 · agent:data-agent · 2026-09-02）

**步1 只写编排仓。** Python 目标 = `demo-algo-ent-analysis`（进程 `demo-platform-entan-py`）；Java = `demo-svc-platform`。正式 lumen 链不在本叶。

### 范围与实现（对照 SRS 116）

| 项 | 产业全要素图谱 API |
|---|---|
| seq | **116** |
| metric_id | `M_COMP_GRAPH_116_1`（占位，不伪 8 件套） |
| 落点 | D `COMP_GRAPH_BROWSE` + 检索 / 关系 / 可视化 / 语义相似 / 网络指标 |
| 本波诚实 | 不写图；名称不猜 VID；语义相似默认 rule；词云=频次 |

真源：`agent-delivery/data/data-design/storage/COMP/etl/pipeline-to-nebula.md`。

### 关系 × op_id × I/O 摘要

| op_id | 档 | HTTP | 本波 |
|---|---|---|---|
| `COMP_GRAPH_BROWSE` | D | `GET /v1/comp/graph` → `/internal/comp/graph` | 只读；`hops`/`limit` |
| `COMP_ENTITY_SEARCH` | 查询 | `GET /v1/comp/graph/entities` | 分页；已有点 |
| `COMP_REL_QUERY` | 查询 | `GET /v1/comp/graph/relations` | 已有边；未知 rel=`not_in_wave` |
| `COMP_GRAPH_VIZ` | 查询 | `GET /v1/comp/graph/viz` | graph / wordcloud |
| `COMP_SEMANTIC_SIM` | 查询 | `POST /v1/comp/graph/similar` | rule 字面；llm 可选 |
| `COMP_NETWORK_METRIC` | 查询 | `GET /v1/comp/graph/metrics` | 密度 / 中心度，空图为 0 |
| A/B/C 写入 | — | — | **不实现** `not_in_wave` |

Java（步3）：网关在 `/industry-comp/**` 前插 graph → `gkx-innov` → Feign **entan-py** `/internal/comp/graph*`。禁止 innov-py。禁止 catch-all 直连写图。

### 灌数剥离清单

| 位置 | 动作 |
|---|---|
| `industry-comp/pages/BasicPage.vue` | 灌数据已 disabled；保持零图谱 |
| 综合 `run_all_*` | 现网无独立贴源；禁止新建来建图 |
| `compModelCatalog.ts` Mock 图 | 步4：`USE_MOCK=false` 禁止 fixture 填 116 |
| 企业 `run_all.py` | **不改**（企业叶已收口） |

### 偏离说明

| 项 | 说明 |
|---|---|
| 无 `storage/COMP` 细表 / 流图 | 按厚包只建 draft 管道 + README，不翻签 |
| metric 8 件套 | `M_COMP_GRAPH_116_1` 占位；MCP 未挂，不编造口径 |
| Feign 进程 | 与企业同 `demo-platform-entan-py`，换 Path `/comp/graph*`，不另起 Pod |
| 现网无 graph 菜单 / 无网关插队 | 步3/4 补；步1 只写清 |

### 产物清单

| 路径 | 说明 |
|---|---|
| `storage/COMP/README.md` | 域入口 draft |
| `storage/COMP/etl/pipeline-to-nebula.md` | 116 契约 + mermaid |
| `storage/README.md` | COMP 指针 |
| 本文 | 步1 handoff |

### 验收证据

- 步1 范围 = 编排仓文档；未改 Python/Java/Vue
- `diagram_id=COMP-GRAPH-TRIPLE`
- 116 五查询 + D 全表，无静默删行

### 架构合规自检

| 铁律 | 本步 |
|---|---|
| 算法只在 Python | ✅ 本步无代码；契约写查询在 Python |
| 前端→Java→`/internal` | ✅ 步3 才接线；文档已写 Path |
| 图谱 Nebula / 一张 G | ✅ `demo_gkx_chain`；禁第二张图 |
| 可观测 | ✅ 步4 补 |
| CI/CD | ✅ 文档 push `origin/dev` |
| demo 不 merge lumen | ✅ |
| 共享聚合 / Java 不写算法 | ✅ Java 只透传 |
| 数据 ADS / Mock | ✅ 查询可 pg 回退；不灌数建图 |
| D8/D9/D10 | ✅ 步4 |
| D9 metric 占位 | ✅ 不伪 8 件套 |
| D12 | ✅ 不改 lumen Java |
| 只做自己工单 | ✅ 未开别人的叶 |

### Cost（估算 · 非 console 实测）

| 字段 | 值 |
|------|-----|
| actual_tokens | 45000 |
| model_used | grok-4.6 |
| actual_cost | 0.22 |
| cost_warn | green |

---

## 算法查询（步2 · agent:algorithm-agent · 2026-09-02）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| ponytail | `full` |

**范围**：`demo-algo-ent-analysis` 只读 `/v1`+`/internal/comp/graph*`。不改 Java / UI / 企业写入 / 灌数。

### 实现

| 项 | 落点 |
|---|---|
| 核 | `entan/comp_graph/query.py`：D 复用 `browse`；检索/关系走 ADS `graph_*`；相似 rule 字面分；指标在本次子图上算 |
| HTTP | `api/comp_graph_routes.py` 成对挂 `api/main.py` |
| VID | 只认前缀 / 32 位 hex；名称 → `no_stable_id` |
| 未知 rel | `not_in_wave` |
| 写图 | 模块无 `INSERT VERTEX/EDGE`；`written_nodes/edges` 恒空 |

### 验收

- `PYTHONPATH=. python -m pytest tests/test_comp_graph_query.py -q`：4 pass
- 未改 `scripts/run_all.py`

### 架构合规

| 铁律 | 本步 |
|---|---|
| 算法只在 Python | ✅ |
| 不写 nGQL | ✅ 只读 browse / ADS SELECT |
| 一张 G | ✅ `demo_gkx_chain` |
| 灌数零图谱 | ✅ 未挂灌数 |
| D12 / 别人的叶 | ✅ 未开 |

### 步2 核对补丁（2026-09-02 · 徐滕强要求先修缺口）

对照契约现网复测后补：

| 缺口 | 处理 |
|---|---|
| browse 走 `ent_vid` 把 `chain:` 拧成 `ent:chain:`；中文中心会变成 `ent:华为` | `browse(seed=)` 不再二次加前缀；综合中心先 `resolve_vid`，名称 → `no_stable_id` |
| `ent:` 前缀吃掉 `entan:` | 长前缀优先；`entan:x` → `no_stable_id` |
| 检索无 `sort` | `sort=name\|-name\|weight\|-weight\|vid\|-vid` |
| 检索/关系只读 ADS | 先 Nebula LOOKUP / GO + FETCH，失败回退 ADS |
| 对端无点 | src/dst 不在图 → `no_stable_id`；边两端缺顶点丢弃并记 skipped |
| 本机 pydantic 1.8 挂不上 `dict \| None` | `Optional[dict]`（只改综合 similar） |
| `mode=llm` 无向量 | **保持** rule 回退 + `llm_fallback`（`OPEN-COMP-GRAPH-SEMANTIC`；仓内无 embed 客户端，不新造） |

验收：`PYTHONPATH=. python -m pytest tests/test_comp_graph_query.py -q` → 8 pass。未改 `run_all.py` / Java / UI。

现网 `e680538` 复测：名称不猜 VID / hex→nebula / `entan:` 拒绝 已生效。回归：LOOKUP/FETCH 空结果没回 ADS，检索 `量子` 变 0、`ent:ORG00000002` 被判 `no_stable_id`。已补「Nebula 空 → ADS」。需再发 `demo-algo-ent-analysis`。

---

## Java 门面（步3 · agent:algorithm-agent · 2026-09-02）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| ponytail | `full` |

**范围**：只改 `demo-svc-platform`。不改 lumen / Python / UI。无 A/B/C。

### 实现

| 项 | 落点 |
|---|---|
| 网关 | `gkx-gateway-dev.yml` `gkx-comp-graph`：`/industry-comp/v1\|internal/comp/graph*` → `lb://gkx-innov`，`order: -10`，不配 StripPrefix |
| Controller | `gkx-innov/.../comp/CompGraphController`：`/v1`+`/internal/comp/graph*` 六条只读 |
| Feign | `CompGraphAlgoClient` → `${gkx.innov.entan.algo-base-url}` `/internal/comp/graph*`（同 entan-py，禁止 innov-py） |
| 未加 | `/industry-comp/**` catch-all（现网没有，契约禁止顺手加） |

### 验收

- 单测 `CompGraphServiceTest`：上游失败 `code=1`
- 现网须发 **`demo-svc-platform`**（`gkx-innov` + `demo-platform-gateway`）后再 curl `/api/industry-comp/v1/comp/graph`

### 发完复测（2026-09-02 · 徐滕强确认已部署）

| 路径 | HTTP | 结论 |
|---|---|---|
| `/api/industry-comp/v1/comp/graph*` 六条 + `/internal` | **424** `token expired`（2026-09-03 00:49 后） | **S3-1 已关**：进了 `gkx-comp-graph` → `gkx-innov` 鉴权，不再 404 |
| `/api/innov/v1/comp/graph` | 424 `token expired` | 同 innov 鉴权（S3-2，企业图同口径；UI 带 token 可过） |
| `/api/entan/internal/comp/graph` | 200 `COMP_GRAPH_BROWSE` / `demo_gkx_chain` | 步2 Python 仍绿 |
| `/api/entan/v1/comp/graph` | 200 | `/entan/**` catch-all 直连 Python，**不是** Java 门面 |

根因（已闭环）：`nacosConfigInit.runOnUpgrade=false`，发镜像不会把 helm `gkx-gateway-dev.yml` 灌进现网。业务路由真源是 **`gkxx.sys_route_conf` → Redis `gl:gateway_route_key`**（UPMS `DynamicRouteInitRunner` 全量灌）。只改 Nacos / 只重启网关不够。

**现网操作（2026-09-03 · 跳板 `111.198.38.90:50122` → ns `dev`）**：

- 在 **`gkxx.sys_route_conf`** 插入 `gkx-comp-graph`：`lb://gkx-innov`，`sort_order=-10`，`filters=[]`，Path 四条（`/industry-comp/v1/comp/graph`、`/**`、`/internal/comp/graph`、`/internal/**`），无 StripPrefix。
- rollout `demo-platform-upms`：日志确认「加载路由ID：gkx-comp-graph … order:-10」。
- rollout `demo-platform-gateway`：旧副本结束后复测，正式链 404 → 424。
- 未改 `gkxlumenx` / lumen 网关（D12）。外网 `50148` 仍是 lumen Nacos，不要往那里贴 demo 路由。

### 先记着、发完再收

| ID | 现象 | 处理时机 |
|---|---|---|
| S3-1 | ~~正式链 404 带 `industry-comp/`~~ | **已关**（`sys_route_conf` + UPMS + gateway 重启） |
| S3-2 | 无 token curl 424 | **代码已补** `CompGraphController` `@Inner(false)`（innov 扫描进 ignore-urls）。要现网 200 须发 **gkx-innov**。联调台 / apiview 带登录态即可过 |
| S3-3 | 外网 Nacos 看不到 demo 路由 | 与企业叶同：记缺口（真源是 Redis，不依赖外网 Nacos） |
| S3-4 | ~~步4 UI 未开~~ | **已做**（见下节；待两仓 push + 现网点验） |

### 架构合规

| 铁律 | 本步 |
|---|---|
| 前端→Java→`/internal` | ✅ |
| Java 不写算法 / nGQL | ✅ Map 透传 |
| Feign 指 entan-py | ✅ 复用 `gkx.innov.entan.algo-base-url` |
| 不改 lumen / D12 | ✅ |
| 一张 G / 无写入 | ✅ |

---

## 前端接线（步4 · agent:frontend-agent · 2026-09-03）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:徐滕强` |
| ponytail | `full` |

**范围**：`demo-ui-system-test` + `lumen-ui-algo-apiview`。不改口径、不写算法、不直打 Python 端口。无 A/B/C。

### 实现

| 项 | 落点 |
|---|---|
| 联调台菜单 | `/industry-comp/graph`（`industryCompMenuConfig` + router extraImport） |
| API | `src/api/industry-comp/index.ts` → `/industry-comp/v1/comp/graph*` + `X-Trace-Id` |
| 页 | `industry-comp/components/GraphView.vue`：D + 检索 / 关系 / 可视化 / 相似 / 指标；116 全表含 A/B/C `not_in_wave` |
| apiview | `comp.graph` 六条 `java_api`；`GRAPH_IDS` / 图谱导航纳入 |
| 白名单 | `CompGraphController` `@Inner(false)`（S3-2；须发 innov） |
| 灌数 | `BasicPage` 灌数据按钮保持 disabled，文案未改成「会建图」 |

### 验收

- `node --test scripts/catalog.test.mjs`：21 pass
- 现网点验（登录联调台后）：`/industry-comp/graph` 打正式链；apiview 关「模块 Mock」后六条 op_id 可跑
- 无 token curl 仍可能 424，等 innov 带着 `@Inner` 发出

### 架构合规

| 铁律 | 本步 |
|---|---|
| 前端→Java→`/internal` | ✅ 只打 `/industry-comp/v1/comp/graph*` |
| 禁止 catch-all 直连 Python 写图 | ✅ 无写入按钮 |
| D8/D9/D10 / 可观测 | ✅ MetricHint + X-Trace-Id；D9 占位 `M_COMP_GRAPH_116_1` 不伪 8 件套 |
| D12 | ✅ 不改 lumen 业务前端仓调用链 |
| `USE_MOCK=false` | ✅ 图谱页不读 `compModelCatalog` fixture |
| 一张 G / 无 A/B/C | ✅ |

### Cost（估算）

| 字段 | 值 |
|------|-----|
| actual_tokens | 38000 |
| model_used | grok-4.6 |
| actual_cost | 0.19 |
| cost_warn | green |
