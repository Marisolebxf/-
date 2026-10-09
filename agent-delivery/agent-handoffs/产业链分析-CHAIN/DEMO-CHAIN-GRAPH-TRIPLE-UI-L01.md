# DEMO-CHAIN-GRAPH-TRIPLE-UI-L01 · 产业链图谱三元组闭环

> 叶内四步：步1 data-agent → 步2 algorithm-agent → 步3 api-agent → 步4 frontend-agent。本文按步追加，不覆盖他人段落。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent`（本步 4/4；步1/2/3 曾为 data-agent / algorithm-agent / api-agent） |
| supervised_by | `human:李伟`（全程不准改） |
| claim_type | `coordinator_dispatch` |
| 说明 | 厚包 `COORD-GRAPH-TRIPLE-UI-DISPATCH-20260831.md` §0 §0.5 §7.0。本步会话未挂 `task-registry` MCP，未直接读取/修改 `task-registry.yaml`，按派单要求只在本文手工回填 cost。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 文档完整性优先；未用 YAGNI 裁掉接口表 / 过程图 / 边×终点矩阵 / 灌数剥离函数级清单。本步不改 UI，D8/D9/D10 由步4 落地。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求 SRS 与现网 pipeline 读原文，禁止 compress 代替精读。本会话未挂 headroom MCP。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `CHAIN-GRAPH-TRIPLE` |
| 图 diff | 新增目标态：灌数零图谱 → A `chain`/`segment` → B `belongs_to`/`depends_on`（`supplies` 本波不上图）→ C 产业-六主体（tech/talent 不上图；政策 FETCH `pol:`）→ D 双全景只读；禁止灌数 `project_safe` / `CLEAR SPACE` / 顺带 hang |
| 会签态 | 存储拓扑 `01-data-flow.md` 仍为 `approved`（本叶未改会签边）；本图为步1 契约稿（draft 实现，步2 按图编码） |

---

## 数据设计（步1 · agent:data-agent · 2026-09-01）

**步1 文档门已齐，步2 可按文档开工。** 实现必须对照 `storage/CHAIN/etl/pipeline-to-nebula.md` §17–§18。

**请 `human:李伟` 开步2**：派 `algorithm-agent`，`claimed_by=agent:algorithm-agent`，`supervised_by` 仍为 `human:李伟`。厚包 `/goal` 见 COORD §7.2，`{HARD}` = 链灌数禁 Nebula 投影、禁顺带 hang。

飞书 `im-send` 因登记表无此 `task_id` 会拒发；本段即通知真源。

### 范围与实现（对照 SRS 102 / 103）

| 项 | 产业实体识别构建 | 产业实体关系抽取 |
|---|---|---|
| seq | **102** | **103** |
| metric_id | `M_CHAIN_GRAPH_102_1`（设计占位；本会话 metric-registry 未挂） | `M_CHAIN_GRAPH_103_1` |
| 本步落点 | 档 **A** `CHAIN_NER_INDUSTRY`：产业 + 环节 | 档 **B** 链内边；档 **C** 产业-六主体 |
| 原文要点 | 规则+词典；名称/类型/行业/地理位置；属性周期更新 | 产业-技术/企业/人才/科研/服务/政策 |
| 本波诚实 | 属性走 ADS，不另建属性 Tag | tech/talent **本波不上图**；无稳定 ID 不上图；禁止名称猜 VID；C 档 FETCH，禁止再造 `ent:`/`inst:` 点 |

档 **D** = 只读全景 + 专题全景拼装，不写库。Space = **`demo_gkx_chain`**。

A/B/C/D = **A 产业/环节；B 链内边；C 产业-六主体；D 双全景**。

真源（只写编排仓，未改业务代码）：

`agent-delivery/data/data-design/storage/CHAIN/etl/pipeline-to-nebula.md`

### 关系 × op_id × I/O 摘要

| op_id | 档 | HTTP | 输入要点 | 输出要点 | 本波 |
|---|---|---|---|---|---|
| `CHAIN_NER_INDUSTRY` | A | `POST /v1/chain/graph/ner` → `/internal/chain/graph/ner` | `scope=one\|batch`；`id=chain_id`；`mode`；`dry_run` | `written_nodes` chain/segment；`skipped` 四码 | 上图 |
| `CHAIN_RE_BELONGS_TO` | B | `POST /v1/chain/graph/intra` | `relation_whitelist` | `belongs_to` | 上图 |
| `CHAIN_RE_DEPENDS_ON` | B | 同上 | 同上 | `depends_on` | 上图 |
| `CHAIN_RE_SUPPLIES` | B | 同上 | 同上 | skipped | **无源不上图** |
| `CHAIN_RE_INDUSTRY_ENTERPRISE` | C | `POST /v1/chain/graph/hang` | 必须带 `op_id`；`dest_types` | `FETCH` `ent:` | 上图 |
| `CHAIN_RE_INDUSTRY_RESEARCH` | C | 同上 | | `FETCH` `inst:` | 上图 |
| `CHAIN_RE_INDUSTRY_SERVICE` | C | 同上 | | `FETCH` `inst:` | 上图 |
| `CHAIN_RE_INDUSTRY_TECH` | C | 同上 | | `not_in_wave` | **不上图** |
| `CHAIN_RE_INDUSTRY_TALENT` | C | 同上 | | `not_in_wave` | **不上图** |
| `CHAIN_RE_INDUSTRY_POLICY` | C | 同上 | | `FETCH` `pol:` | 有点才上图 |
| `CHAIN_GRAPH_PANORAMA` | D | `GET /v1/chain/{id}/panorama` | 只读 | 不写库 | 现网可读 Nebula/ADS |
| `CHAIN_GRAPH_TOPIC_PANORAMA` | D | 页拼装 list+panorama | 只读 | 不写库 | 无第二写接口 |

公共：`dry_run` 不写 Nebula；同 `calc_batch_id`+主键可重跑覆盖；LLM 只在 `mode=llm`，无 Key 回退。`skipped.reason` ∈ `empty_field` / `no_stable_id` / `not_in_wave` / `vid_too_long`。六主体 + 链内边全表见 §17.3，**无静默删行**。

步3 Feign **`demo-platform-innov-py`**（禁止指 entan-py）。Java 在已有 `ChainAlgoClient` 上补写入 `/internal`。

### 灌数剥离清单（文件 / 函数 / 按钮级）

精读结论：主路径 **`run_seed` 末步仍调用 `project_safe` → `project_nebula` → `project_from_dwd`**（replace 会 `CLEAR SPACE`）。这是步2 必须摘掉的核心。

| 文件 | 符号 | 步2 |
|---|---|---|
| `chainan/llm_ods/seed.py` | `project_safe(...)` | **删除** |
| `chainan/llm_ods/project.py` | `project_nebula` / `project_safe` | 禁止进灌数 |
| `chainan/graph/nebula_project.py` | `project_from_dwd` / `CLEAR SPACE` | 仅 A/B/C；C 改 FETCH |
| `chainan/graph/nebula_schema.py` | `init_schema_from_code` | 禁止进灌数 |
| `scripts/run_all.py` | `run_chain` / `_seed_step` | grep 零投影 |
| `api/main.py` | `POST /internal/run-chain-pipeline` | 保留灌数，零图 |
| `run_ent_chain_hang.py` | hang | **禁止**灌数顺带调用 |
| `BasicPage.vue` | 「追加/重建灌数」+ Nebula 文案 | 步4 去文案；步2 先断后端 |

灌数只留：ODS→DWD→可选 ADS。重灌后图空或旧图不被灌数填满 = 预期。

### 架构合规自检

| 铁律 | 本步 |
|---|---|
| 算法只在 Python | ✅ 契约写 Python `/internal`；Java 只转发 |
| 调用链 前端→Java→Python `/internal/*` | ✅ §17.1 HTTP 表；现网 as-built 灌数仍直打 innov-py `/internal`，步3 插 Java 写图路由 |
| 图谱 Nebula `demo_gkx_chain` | ✅ 禁止第二 space |
| D12 | ✅ 本步只改编排仓文档；未改 `demo-ui-*` / `lumen-ui-*` / `demo-algo-*` 代码 |
| 不灌数 / 不 APPLY DDL | ✅ |
| P0 灌数剥离 | ✅ 清单已落 §18；实现属步2 |
| 不顺带 hang | ✅ §18 #11 |

### Cost（估算 · 非 console 实测）

计价代理：`budget-estimate.md` §1.2 Sonnet 4.5（$3 / $15 per MTok），data/doc 默认 in/out ≈ 85/15。`source: session_estimate`。长会话含多次 MCP/冲突排查。

| 字段 | 值 |
|------|-----|
| actual_tokens | 320000 |
| model_used | grok-4.6 |
| actual_cost | 1.54 |
| cost_warn | green |

registry 四字段待建单后 `task-update-fields`。

### 偏离说明

- 注册表无此叶：与 SVC 步1 同处理——文档先 push，认领后补。
- 未改 `01-data-flow.md` / `pipeline-demo-sim-process.md`（会签边与范围）；剥离真源以本管道 §18 为准。
- `CHAIN_GRAPH_TOPIC_PANORAMA` 现网无独立 GET，标为 UI 拼装，禁止步1 发明写接口。

### 产物清单

- `agent-delivery/data/data-design/storage/CHAIN/etl/pipeline-to-nebula.md`
- 本 handoff

### 验收证据

- 编排仓 `origin/dev` push（本步 commit）
- 未改 demo/lumen 业务代码
- 未灌数、未 APPLY DDL

---

## 算法实现（步2 · agent:algorithm-agent · 2026-09-01）

**步2 `/internal` 门已齐，步3 可按文档开 api-agent。** `supervised_by` 仍为 `human:李伟`。Feign 下游 **`demo-platform-innov-py:8000`**，禁止 entan-py。

### 范围

| 项 | 落点 |
|---|---|
| 仓 | `demo-algo-science`（未改 demo-ui / lumen-ui / lumen-svc） |
| 灌数剥离 | `run_seed` 不再调 `project_safe`；`run-chain-pipeline` 只灌 ODS→DWD→ADS；legacy 去掉 `chain_graph.run` / `run_sz` |
| A | `POST /internal/chain/graph/ner`（兼 `/v1/chain/graph/ner`）`CHAIN_NER_INDUSTRY` |
| B | `POST /internal/chain/graph/intra` · belongs_to / depends_on；`CHAIN_RE_SUPPLIES` 本波 `empty_field` |
| C | `POST /internal/chain/graph/hang` · 企业/科研/服务 **FETCH** 后 `participates`；tech/talent `not_in_wave`；政策 FETCH `pol:` |
| D | 现网 `GET /v1/chain/{id}/panorama` + 新增 `GET /internal/chain/{id}/panorama` 只读 |
| 可选 | `POST /internal/chain/graph/ops/{op_id}` |
| space | `demo_gkx_chain` |
| diagram_id | `CHAIN-GRAPH-TRIPLE`（实现对照步1 mermaid，未加边） |

`graph-schema-init` **仍独立**，不进灌数。`project_from_dwd` 留核给图谱菜单/测试，灌数入口 grep 不到。

### grep 证据（灌数入口）

对 `chainan/llm_ods/seed.py`、`scripts/run_all.py`、`api/main.py` 的 `_run_chain_pipeline`：

| 符号 | seed.py | run_all.py 主路径 | `_run_chain_pipeline` |
|---|---|---|---|
| `project_safe` / `project_nebula` / `project_from_dwd` | 无 | 无 | 无 |
| `CLEAR SPACE` / `INSERT VERTEX` / `run_ent_chain_hang` | 无 | 无 | 无 |
| `init_schema_from_code` | 无 | 无 | 无（仅 `/internal/graph-schema-init`） |

单测：`python -m pytest tests/test_chain_graph_ops.py tests/test_chain_nebula_schema.py -q` → **16 passed**。

### /internal 样例

```http
POST /internal/chain/graph/ner
{"op_id":"CHAIN_NER_INDUSTRY","scope":"one","id":"INB13","mode":"rule","dry_run":true}

POST /internal/chain/graph/intra
{"op_id":"CHAIN_RE_BELONGS_TO","scope":"one","id":"INB13","relation_whitelist":["belongs_to"],"dry_run":true}

POST /internal/chain/graph/hang
{"op_id":"CHAIN_RE_INDUSTRY_ENTERPRISE","scope":"one","id":"INB13","mode":"rule","dry_run":true}

POST /internal/chain/graph/hang
{"op_id":"CHAIN_RE_INDUSTRY_TECH","scope":"one","id":"INB13"}
```

`mode=llm` 无 Key → `mode_effective=rule`，`llm_fallback=true`。`skipped.reason` 仅四码。C 档 FETCH 未命中 → `no_stable_id`，**不** `INSERT VERTEX enterprise|institution`。

本会话未对 K8s :8000 做 live curl（无本机 innov-py 探活）；契约由 FakeSess 单测覆盖。步3 经网关 curl。

### 架构合规

| 铁律 | 本步 |
|---|---|
| 算法只在 Python `/internal` | ✅ |
| 灌数零图谱 | ✅ |
| Nebula `demo_gkx_chain` | ✅ 未第二 space |
| Java 不写 NLP / nGQL | ✅ 留给步3 |
| D12 | ✅ 未改 lumen；未打 demo UI |
| C 档 FETCH | ✅ 禁止造 ent:/inst: |

### Ponytail / 图 / Cost

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| diagram_id | `CHAIN-GRAPH-TRIPLE` |
| headroom | skip（本会话未挂） |
| actual_tokens | 180000 |
| model_used | grok-4.6 |
| actual_cost | 0.86 |
| cost_warn | green |
| source | session_estimate |

registry 本 ID MCP 仍可能 not found，**未**手改 `task-registry.yaml`。

### 请 `human:李伟` 开步3

派 **api-agent**：在 `demo-svc-platform` 抄政策 `31582b9e`，`ChainAlgoClient` 补写入 `/internal/chain/graph*`，Feign **`http://demo-platform-innov-py:8000`**，网关 graph 路由插在 catch-all **之前**，勿让 `/chain/internal` 直连抢走写图。

---

## Java 转发（步3 · agent:api-agent · 2026-09-01）

**步3 Java / 网关门已齐，步4 可接线。** `supervised_by` 仍为 `human:李伟`，`claim_type=coordinator_dispatch`。本会话动态工具未发现 `task-registry` / `task-get`，未直接修改 `task-registry.yaml`；cost 先回填本文。

### 范围与实现

| 项 | 落点 |
|---|---|
| Java REST | `POST /v1/chain/graph/ner\|intra\|hang`、`POST /v1/chain/graph/ops/{op_id}`、`GET /v1/chain/{chainId}/panorama` |
| 兼容入口 | `/internal/chain/graph/*` 与 `/internal/chain/{chainId}/panorama` 同样先进入 Java |
| Feign | 已有 `ChainAlgoClient` 新增 `/internal/chain/graph/ner\|intra\|hang\|ops/{op_id}` 与只读 panorama |
| 下游 | `INNOV_CHAIN_ALGO_BASE_URL=http://demo-platform-innov-py:8000`；`application-dev.yml` 与 Helm `values.yaml` 均已存在该值，禁止 entan-py |
| 网关 | 新增 `gkx-chain-graph`（`order: -10`），位于 `gkx-chain-internal` 的 `/chain/internal/**` catch-all **之前**；指标、灌数、状态、模型注册仍走原 catch-all |
| OpenAPI | `openapi-chain-graph-v1.yaml` + Controller `@Operation`；`x-diagram-id=CHAIN-GRAPH-TRIPLE` |
| 可观测 | 复用 Java Agent 对 Feign 的 W3C `traceparent` 自动注入；失败日志标签固定为 `[chain-graph]` |

Java 只转发 `Map<String,Object>`；非空 body 保持同一对象传给 Feign，不做 NER/RE、不改边名、不拼 nGQL。写入 op_id 全覆盖：

`CHAIN_NER_INDUSTRY`、`CHAIN_RE_BELONGS_TO`、`CHAIN_RE_DEPENDS_ON`、`CHAIN_RE_SUPPLIES`、`CHAIN_RE_INDUSTRY_ENTERPRISE`、`CHAIN_RE_INDUSTRY_RESEARCH`、`CHAIN_RE_INDUSTRY_SERVICE`、`CHAIN_RE_INDUSTRY_TECH`、`CHAIN_RE_INDUSTRY_TALENT`、`CHAIN_RE_INDUSTRY_POLICY`。

D panorama 透传 Python `/internal/chain/{chainId}/panorama`，只读、不写库。

### 经网关 curl（不是直打 :8000）

开发网关根：`http://192.168.88.50:30889`。

```bash
curl -X POST "http://192.168.88.50:30889/chain/v1/chain/graph/ner" \
  -H "Content-Type: application/json" \
  -H "X-Trace-Id: chain-step3-f6ce03c" \
  -d '{"op_id":"CHAIN_NER_INDUSTRY","scope":"one","id":"INB13","mode":"rule","dry_run":true}'

curl "http://192.168.88.50:30889/chain/v1/chain/INB13/panorama" \
  -H "X-Trace-Id: chain-step3-f6ce03c"
```

本机两次实际执行均在 15 秒后连接超时（`curl: (28)`），与同日 SVC 叶记录的该网关不可达现象一致；不伪称 K8s live 已验证。远端 `origin/dev` 已确认指向 `f6ce03c8be63c2534aa3a8ca1c5ce5daf42c70dd`。

### 验收证据

- Java 17 编译 + JUnit 5：`ChainGraphServiceTest` **4 passed**，覆盖 ner/intra/hang 原 Map、10 个 op_id、panorama、精确 `{op_id}` 路径与上游失败包络。
- YAML：Python `yaml.safe_load` 成功解析网关与 OpenAPI，并断言 `x-diagram-id=CHAIN-GRAPH-TRIPLE`。
- IDE lint：本步 6 个改动文件无诊断。
- `git diff --check`：通过。
- Helm CLI：本机未安装，未伪称 `helm lint` 通过。

### 架构合规

| 铁律 | 本步 |
|---|---|
| 前端 → Java REST → Python `/internal/*` | ✅ graph 具体路由抢在 `/chain/internal/**` 前 |
| 算法只在 Python | ✅ Java 仅 Controller / Service / Feign 透传 |
| Java 禁止直连 nGQL | ✅ 无 Nebula 客户端、无 nGQL |
| Feign Pod | ✅ `demo-platform-innov-py:8000`；未指向 entan-py |
| 不改整域灌数/指标 | ✅ catch-all 保留；仅 graph 与 panorama 具体 Path 走 Java |
| D12 | ✅ 仅 demo 服务仓；无 lumen → demo 调用 |
| 未改 Vue / 未发明边 | ✅ |

### Ponytail / Cost

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 复用已有 `ChainAlgoClient`、现有 Feign URL 与 Java Agent；未增加依赖或算法抽象；未裁掉 OpenAPI、中文 Javadoc、可观测和测试 |
| actual_tokens | 120000 |
| model_used | Auto |
| actual_cost | 0.58 |
| cost_warn | green |
| source | session_estimate |

### 产物与推送

- 仓：`demo-svc-platform` `origin/dev`
- commit：`f6ce03c`（`feat(chain): 图谱 A/B/C/D 经 Java 转发 internal [agent:api-agent]`）
- 文件：`ChainAlgoClient`、`ChainGraphController`、`ChainGraphService`、OpenAPI、单测、`gkx-gateway-dev.yml`

### 请 `human:李伟` 开步4

请派 `frontend-agent` 接图谱菜单 A/B/C/D 与 apiview；`supervised_by` 保持 `human:李伟`。前端必须只调用网关 `/chain/v1/chain/graph*` / panorama，不得直打 Python `:8000`。

---

## 前端接线（步4 · agent:frontend-agent · 2026-09-01）

**步4 已完成，`DEMO-CHAIN-GRAPH-TRIPLE-UI-L01` 四步齐。** `supervised_by=human:李伟`、`claim_type=coordinator_dispatch` 未变；未改数据口径、算法、Java、Feign、`01-data-flow.md`。

### 范围与实现

| 能力 | `demo-ui-system-test` | `lumen-ui-algo-apiview` |
|---|---|---|
| A 产业/环节 | 两个范围路由共用 `ChainGraphWorkbench`，执行 `CHAIN_NER_INDUSTRY` | 两页 `chain-graph-composite` 均可选并执行该 `op_id` |
| B 链内边 | `belongs_to` / `depends_on` / `supplies` 逐项执行；`supplies` 明示本波不上图 | 三个 `op_id` 全部列入 catalog 选择器与契约测试 |
| C 产业-六主体 | 企业/科研/服务/技术/人才/政策六项齐；tech/talent 明示本波不上图，政策明示 FETCH 到才上图 | 六个 `op_id` 全部可测，不发明新边 |
| D 双全景 | 复用原 `PanoramaGraph` / `TopicPanoramaPage` 浏览区，不再新建图组件 | 两页都走 `GET /chain/v1/chain/{chainId}/panorama`；复用本仓 G6 `GraphPanel` |
| 图例/血缘 | 步1 §17.3 **11 行**全表；统计数旁复用 `MetricHint` | 同一 11 行表；复用 `@/review/MetricMarker`，mount 为 102/103/节点数 |

`diagram_id=CHAIN-GRAPH-TRIPLE`；source/space 均标识为 `demo_gkx_chain`；示例只用稳定 `chain_id=INB13`，图谱页已移除 `gkx_policy` 与 `n-up-1` / `t-1` 等假图数据。

### 复刻五列对照

| 维度 | 联调台 `/chain/panorama` | 联调台 `/chain/topic-panorama` | APIView 两页 | 结论 |
|---|---|---|---|---|
| 布局 | A/B/C/D Tab + 条件区 + 结果区 + 三元组表 | 同一四档壳内保留专题双全景工作区 | 同一 composite 覆盖写入、浏览、结果、图例 | ✅ 非占位、非只改 Hero |
| 交互 | one/batch、rule/llm、dry_run、稳定 ID 校验、错误 trace | 切档不自动写图；原「开始分析」与条件脏状态保留 | 每个 op_id 可选可执行；D 只读；失败可见 | ✅ |
| 样式 | 复用 `--sci-*`、Element Plus、原页图表 | 复用原专题页与兄弟页 token | Arco + 既有 composite / G6 图谱皮肤 | ✅ 未另起 UI 栈 |
| 评审 | 复用既有 `MetricHint`，不自造 ⓘ | 同左 | 只从 `@/review/MetricMarker` 挂点 | ✅ D9 追溯入口齐 |
| Mock 开关 | 页面无 `MOCK_*`、无 fixture；只调 Java 网关 | 同左 | `runChainEndpoint` 服从全局 `USE_MOCK` / `useCompMock`；关闭后只打 Java | ✅ 不回落 fixture |

### 灌数剥离与 Java 网关证据

- `BasicPage.vue` 的追加/重建卡片、`seedFlow`、`seedNotes`、`ElMessageBox` 已删除 ES / Nebula 投影、整图重灌、补图等承诺；确认框明确“本操作不执行图谱写入”。
- 删除前端 `initChainGraphSchema` 内部入口；`runChainPipeline` / `fetchChainStatus` 仍只用于灌数与状态。
- 图谱写入按钮只挂在 `/chain/panorama`、`/chain/topic-panorama` 的 A/B/C 档；D 档只读。
- 联调台调用 `POST /chain/v1/chain/graph/ner|intra|hang`；APIView 调用 `POST /chain/v1/chain/graph/ops/{op_id}`；双全景调用 `GET /chain/v1/chain/{chainId}/panorama`。
- 目录测试断言两页路径均不含 `/internal/`、`:8000`；浏览器未写入 demo 服务名。链路保持 **前端 → Java REST → Python `/internal/*`**。
- 两仓继续复用中央 request/observability：联调台错误态显示 `traceId`；APIView 保存执行结果、耗时与 trace。

### V1–V7 / R1–R5 / W1–W4

| 项 | 结果 | 证据 |
|---|---|---|
| V1–V7 | N/A | 本叶是全景工作区/API 调试页，不是检索 Hub；未新增检索卡、推荐卡或搜索 Hero。 |
| R1 布局 | ✅ | 两个范围路由均有 A/B/C/D、条件、结果、图例；D 内保留原完整工作区。 |
| R2 交互 | ✅ | 空/加载/失败/结果可见；稳定 ID 校验；切档不自动写入；专题条件脏状态保留。 |
| R3 样式 | ✅ | 联调台复用 `--sci-*` / Element Plus；APIView 复用 Arco composite 与本仓 G6。 |
| R4 评审 | ✅ | APIView 统计数只挂 `@/review/MetricMarker`；联调台复用既有 `MetricHint`。 |
| R5 Mock | ✅ | 无页内 `MOCK_*` / `@/mock/**` / Demo fixture；全局 Mock 关闭后只走 Java 实包。 |
| W1 | ✅ | 配置区、执行结果、D 浏览板、§17.3 表齐；APIView 执行记录复用 `algoResults`。 |
| W2 | ✅ | APIView 复用本仓 `GraphPanel`（AntV G6）；联调台 D 档复用既有图谱页。 |
| W3 | N/A | 本叶无报告阅读范围，未新建报告页。 |
| W4 | ✅ | A/B/C 仅点击执行；专题 D 挂载只预选条件，不请求 panorama，须点击「开始分析」。 |

### 验收证据

| 仓 | commit / push | 检查 |
|---|---|---|
| `demo-ui-system-test` | `bb0b7e8` + `29bda97` → `origin/dev` | 契约自检 ✅；专题挂载零自动 panorama 请求扫描 ✅；`npm run build` ✅（3755 modules） |
| `lumen-ui-algo-apiview` | `6045fc7` → `origin/dev` | `catalog.test.mjs` ✅（21/21）；`npm run lint` ✅；`npm run build` ✅ |

APIView 构建机 Node 为 20.18.0，Vite 提示推荐升级至 20.19+，但 type-check 与生产构建均成功；大 chunk 为既有告警，未借本叶修改构建配置。

### 架构合规

| 铁律 | 本步 |
|---|---|
| 前端 → Java → Python `/internal/*` | ✅ 浏览器只调用 `/chain/v1/chain/**` |
| 算法只在 Python / Java 零计算 | ✅ 本步未改算法或 Java |
| Nebula | ✅ 只标识 `demo_gkx_chain`；未引入第二 space |
| D8 / D10 | ✅ 复用仓内组件、token、键盘可达 Tab/表单、加载/失败/空态 |
| D9 | ✅ 统计数旁复用既有血缘组件，102/103 与节点数 mount 齐 |
| 可观测 | ✅ 中央 request + traceId/ErrorBanner/执行结果记录 |
| D12 | ✅ APIView 只写 `/chain` 网关前缀，不写 demo 服务名或 Python 端口 |
| 灌数零图 | ✅ UI 文案与调用均剥离；图操作只在 A/B/C |
| 不发明边 / 缺口诚实 | ✅ supplies/tech/talent 保留并明示不上图；政策 FETCH 到才上图 |

### Ponytail / Cost

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 两路由共用一个 `ChainGraphWorkbench`；APIView 两页共用一个 `ChainGraphPanel` 和一个 ops 契约形状；复用现有 G6、血缘、request、错误态，无新增依赖。 |
| actual_tokens | 220000 |
| model_used | Auto |
| actual_cost | 1.06 |
| cost_warn | green |
| source | session_estimate |

四步估算合计：`actual_tokens=840000`，`actual_cost=$4.04`，低于 $10 复盘阈值。registry MCP 本会话不可用，未自建单、未直接改注册表。

### 通知 `human:李伟`

本叶四步齐：步1 数据契约、步2 Python 图操作与灌数剥离、步3 Java/网关转发、步4 双前端四档与 op_id 测试均已提交；请按上述 commit、测试与路径证据签收。

---

## 联调确认（human:李伟 · 2026-09-07）

**联调通过。** 监管人李伟口头确认 A/B/C/D/E 联调台可点验。

| 项 | 结果 |
|---|---|
| D 产业自身浏览 | 出图 |
| E 全景浏览 | 出图；`source=ads` 可截断抽样；检索企业（如信用代码）命中后高亮挂边，产业/环节骨架保留 |
| 部署 | `gkx-demo-ui:b57859df`；`gkx-innov-py:5bde498b` |
| UI 收口 commit | `demo-ui-system-test` `b57859d`（E `active` 走 slot props，修复父级无法 inject 子 provide） |
| 未改口径 | 有检索词时仍保留全链骨架 + 命中主体，不是 ego 邻域 |

后续：`pending_test` 等 QA。

