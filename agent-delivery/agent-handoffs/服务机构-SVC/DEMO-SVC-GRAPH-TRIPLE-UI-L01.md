# DEMO-SVC-GRAPH-TRIPLE-UI-L01 · 产业服务图谱三元组闭环

> 叶内四步：步1 data-agent → 步2 algorithm-agent → 步3 api-agent → 步4 frontend-agent。本文按步追加，不覆盖他人段落。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent`（本步 1/4；步 2/3/4 由 coordinator 切换） |
| supervised_by | `human:侯佳伟`（全程不准改） |
| claim_type | `coordinator_dispatch` |
| 说明 | 厚包 `COORD-GRAPH-TRIPLE-UI-DISPATCH-20260831.md` §0 §3 §7.0。本工作区 MCP `task-get` **未找到**该 ID（五叶 GRAPH-TRIPLE 均 0 命中）；**未改** `task-registry.yaml`。请 coordinator 补建单后补认领。 |

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
| diagram_id | `SVC-GRAPH-TRIPLE` |
| 图 diff | 新增目标态：灌数零图谱 → A NER 机构点 → B `participates`（服务-服务）→ C 跨域七类；tech/talent 标不上图；政策默认不造反向；禁止灌数调用 `run_graph` / `_upsert_participates` |
| 会签态 | 存储拓扑 `01-data-flow.md` 仍为 `approved`（本叶未改会签边）；本图为步1 契约稿（draft 实现，步2 按图编码） |

---

## 数据设计（步1 · agent:data-agent · 2026-09-01）

**步1 完成，步2 可开工（文档门）。** 无文档阻塞。步2 不得在文档不齐前提前写接口；实现必须对照 `pipeline-to-nebula.md` §17–§18。

**请 `human:侯佳伟` 开步2**：派 `algorithm-agent`，`claimed_by=agent:algorithm-agent`，`supervised_by` 仍为 `human:侯佳伟`。厚包 `/goal` 见 COORD §7.2，`{HARD}` = 服务灌数禁 hang、禁写 Nebula。

### 范围与实现（对照 SRS 112 / 113）

| 项 | 服务机构实体识别构建 | 服务机构实体关系抽取 |
|---|---|---|
| seq | **112** | **113** |
| metric_id | `M_SVC_GRAPH_112_1`（设计占位；本会话 metric-registry 未挂） | `M_SVC_GRAPH_113_1` |
| 本步落点 | 档 **A** `SVC_NER_ORG`：机构点 + 属性 | 档 **B** 服务-服务 `participates`；档 **C** 跨域七类 |
| 原文要点 | 规则+词典；名称/类型/人数/规模/地理位置 | 对接产业/技术/企业/人才/政策/科研/政府；服务机构-产业/技术/企业等 |
| 本波诚实 | 属性只进 `svc_org_card` | tech/talent **本波不上图**；无稳定 ID 不上图；禁止名称猜 VID；政策默认不造 inst→pol 反向 |

档 **D** = 只读 `GET /v1/svc/graph`，不写库。Space = **`demo_gkx_chain`**（禁止 `gkx_service`）。

A/B/C/D = **A 机构；B 服务-服务；C 跨域七类；D 浏览**。

真源（只写编排仓，未改业务代码）：

`agent-delivery/data/data-design/storage/SVC/etl/pipeline-to-nebula.md`（及 SVC/storage README 指针）。

### 关系 × op_id × I/O 摘要

| op_id | 档 | HTTP | 输入要点 | 输出要点 | 本波 |
|---|---|---|---|---|---|
| `SVC_NER_ORG` | A | `POST /v1/svc/graph/ner` → `/internal/svc/graph/ner` | `scope=one\|batch`；`id=org_id` 或 filter；`mode=rule\|llm`；`dry_run` | `written_nodes`（institution）；`skipped` 四码 | 机构点上图；属性只进 card |
| `SVC_RE_SVC_SVC` | B | `POST /v1/svc/graph/intra` | 同上 + `relation_whitelist=[participates]` | `written_edges` participates | 两端本批服务 VID |
| `SVC_RE_INDUSTRY` | C | `POST /v1/svc/graph/hang` | 必须带 `op_id` 或白名单；`dest_types` | hang 前 `FETCH` | 产业 `belongs_to`；无码 `no_stable_id` |
| `SVC_RE_TECH` | C | 同上 | 白名单含 tech | skipped `not_in_wave` | **不上图** |
| `SVC_RE_ENTERPRISE` | C | 同上 | | `FETCH` `ent:` | 上图 |
| `SVC_RE_GOV` | C | 同上 | | `FETCH` `inst:` | 上图 |
| `SVC_RE_TALENT` | C | 同上 | | skipped `not_in_wave` | **不上图** |
| `SVC_RE_POLICY` | C | 同上 | | 默认不写反向 | 消费政策 `apply_to` |
| `SVC_RE_RESEARCH` | C | 同上 | | `FETCH` `inst:` | 上图 |
| `SVC_GRAPH_BROWSE` | D | `GET /v1/svc/graph` | 只读 | 不写 ADS/Nebula | 现网查询保留 |

公共：`dry_run` 不写 hang/Nebula；同 `calc_batch_id`+主键可重跑覆盖；LLM 只在 `mode=llm`，无 Key 回退且 `llm_fallback=true`。`skipped.reason` ∈ `empty_field` / `no_stable_id` / `not_in_wave` / `vid_too_long`。七类 + B 全表见 §17.3，**无静默删行**。

现网 API 挂 `/entan/internal/svc/*` → **entan-py**（与政策/企业同进程）。步3 Feign 禁止指 innov-py。

### 灌数剥离清单（文件 / 函数 / 按钮级）

精读结论：`run_seed` **今天已不写 Nebula、不写 `svc_org_graph_hang`**。步2 仍须 grep 钉死，并摘十模型顺带写图。

| 文件 | 符号 | 步2 |
|---|---|---|
| `entan/svcseed.py` | `run_seed` / `_truncate_seed` | 保持零图写；禁止改成清/写 hang |
| `entan/svcseed.py` | `_hang_finance` | **保留**（A3，不是图 hang） |
| `api/svc_routes.py` | `run_svc_pipeline` / `POST …/run-pipeline` | 只留 seed |
| `api/svc_routes.py` | `run_svc_graph` / `POST …/run-graph` | 禁止被灌数调用；收成 A |
| `api/svc_routes.py` | `run_svc_models` | ADS 可留；**摘** hang.peers + nGQL |
| `entan/svcgraph.py` | `run_graph` / `_upsert_nebula` | 禁止进 pipeline |
| `entan/svcmodels.py` | `_upsert_participates` / UPDATE hang.peers | 迁 B |
| `BasicPage.vue` | 「灌数据」`onSeed` | 保持只调 pipeline；禁止会建图 |
| `GraphView.vue` | 「投影到图谱」/「跑十模型」 | 不是灌数；步4 收成 A/B；步2 灌数页不得调 |
| `01-data-flow` / `pipeline-demo-mock` | 仍画灌数→NEB | **§18 才是剥离真源**；不改会签边 |

灌数只留：ODS→circle/card/finance_event + 可选基础指标。重灌后图空或旧图不被灌数填满 = 预期。

### 架构合规自检

| 铁律 | 本步 |
|---|---|
| 算法只在 Python | ✅ 契约写 Python `/internal`；Java 只转发 |
| 调用链 前端→Java→Python `/internal/*` | ✅ §17.1 HTTP 表；现网 as-built 仍直连 `/entan/**`，步3 插 Java |
| 图谱 Nebula `demo_gkx_chain` | ✅ 禁止 `gkx_service` |
| D12 | ✅ 本步只改编排仓文档；未改 `demo-ui-*` / `lumen-ui-*` / `demo-algo-*` 代码 |
| 不灌数 / 不 APPLY DDL | ✅ |
| P0 灌数剥离 | ✅ 清单已落 §18；实现属步2 |

### Cost（估算 · 非 console 实测）

计价代理：`budget-estimate.md` §1.2 Sonnet 4.5（$3 / $15 per MTok），data/doc 默认 in/out ≈ 85/15。`source: session_estimate`。

| 字段 | 值 |
|---|---|
| actual_tokens | 240000 |
| model_used | grok-4.6 |
| actual_cost | 1.15 |
| cost_warn | green |

未超 $5 黄线。coordinator 收单时回填 registry（本步 **未** 调 MCP 改状态：任务 ID 未入库）。

### 步2 开工门

**PASS（文档）。** 已含：op_id I/O、边×终点全表、灌数剥离文件/函数/按钮级清单、`diagram_id=SVC-GRAPH-TRIPLE`。

步2 打开条件：本文件 + `pipeline-to-nebula.md` 已 `origin/dev`。步2 只改 `demo-algo-ent-analysis`；不改图谱菜单 Vue。

### 开放项

- `OPEN-SVC-GRAPH-01`：tech / talent 本波不上图
- `OPEN-SVC-GRAPH-02`：`institution:` vs `inst:` VID
- Q062 边类型；Q-SVC-010 圈定待核验
- 十模型同城同环节造边 = 代理，须迁 B 并标 `proxy`
- `01-data-flow` 灌数→NEB：另单会签
- registry 缺本叶 ID：请 coordinator 补建

---

## 算法实现（步2 · agent:algorithm-agent · 2026-09-01）

**步2 完成，步3 可开工（`/internal` 门）。** 请 `human:侯佳伟` 开步3：派 `api-agent`，`claimed_by=agent:api-agent`，`supervised_by` 仍为 `human:侯佳伟`。厚包 `/goal` 见 COORD §7.3。Java 插在 `/entan/**` catch-all **之前**，Feign 必须指 **entan-py**（禁止 innov-py）。

`task-get DEMO-SVC-GRAPH-TRIPLE-UI-L01` 仍 **未找到**；**未改** `task-registry.yaml`。本步 `claimed_by` 语义 = `agent:algorithm-agent`。

### 范围与实现

| 档 | op_id | Python | 写什么 |
|---|---|---|---|
| A | `SVC_NER_ORG` | `POST /internal/svc/graph/ner`（兼 `/v1`） | hang UPSERT（按 `org_id`，不 DELETE 全表）+ `INSERT VERTEX institution` |
| B | `SVC_RE_SVC_SVC` | `POST /internal/svc/graph/intra` | hang.ext.peers + `INSERT EDGE participates`；talent_flow/competition → `not_in_wave` |
| C | 七个 `SVC_RE_*` | `POST /internal/svc/graph/hang`（须 `op_id` 或白名单） | `FETCH PROP ON *` 后 `belongs_to` / `participates`；tech/talent / 政策默认反向 → `not_in_wave` |
| D | `SVC_GRAPH_BROWSE` | `GET /internal/svc/graph`（兼现网 `/v1`） | 不写库 |
| 可选 | 同上 | `POST /internal/svc/graph/ops/{op_id}` | 与 ner/intra/hang 并存 |

实现核：`entan/svcgraph_ops.py`（对标 `polan/graph/ops.py`）。旧 `POST /internal/svc/run-graph` 收成 A 档 `filter.all=true`。十模型 `run_models` **已摘** hang.peers 与 nGQL，只留 ADS 分表。`run_seed` / `run-pipeline` 保持零图。`_hang_finance` 注释写明「不是 graph hang」。未改 GraphView / apiview / Vue。

I/O：`scope=one|batch`、`filter.all` 才扫全库、空 `relation_whitelist` 拒绝、`dry_run` 不写、`mode=llm` 无 Key → `llm_fallback=true`。`skipped.reason` 仅四码。`space=demo_gkx_chain`，`vid_scheme=institution`（`OPEN-SVC-GRAPH-02`）。禁止名称猜 VID；禁止 `CREATE SPACE/EDGE`。

### 灌数剥离 grep（步2 过关）

在 `demo-algo-ent-analysis` 对 `run_seed` / `_truncate_seed` / `_write_circle_card` / `_write_metrics` / `run_svc_pipeline` / `svc_run_pipeline` 源码检索，命中均为 **0**：

`run_graph` / `_upsert_nebula` / `upsert_participates` / `_upsert_participates` / `INSERT VERTEX` / `INSERT EDGE` / `svc_org_graph_hang`

`run_models` 源码同上四项写符号 **0**。`.gitlab-ci.yml` 无 seed 后串联 `run-graph` / `run_graph`。

自检：`python -m entan.svcgraph_ops` → `svc graph ops self_check OK`；`entan.svcgraph --check` / `svcmodels --check` / `svcseed --check` 绿。

### `/internal` curl 样例（步3 对照）

前缀现网为 `/entan`（直打 entan-py）。`dry_run` 可先打。

```http
POST /entan/internal/svc/graph/ner
{"scope":"one","id":"<org_id>","mode":"rule","dry_run":true}

POST /entan/internal/svc/graph/intra
{"scope":"batch","filter":{"all":true},"relation_whitelist":["participates"],"mode":"rule","dry_run":true}

POST /entan/internal/svc/graph/hang
{"op_id":"SVC_RE_INDUSTRY","scope":"one","id":"<org_id>","mode":"rule","dry_run":true}

POST /entan/internal/svc/graph/hang
{"op_id":"SVC_RE_TECH","scope":"one","id":"<org_id>","mode":"rule"}

GET /entan/internal/svc/graph
```

C 空白名单 / 无 `op_id` → HTTP 包络 `code=1`。`SVC_RE_TECH` 出参必有 `skipped.reason=not_in_wave`。

### 架构合规自检

| 铁律 | 本步 |
|---|---|
| 算法只在 Python | ✅ A/B/C 在 `entan/svcgraph_ops.py` |
| 调用链 前端→Java→Python `/internal/*` | ✅ 已出 `/internal` 成对；Java 留步3 |
| 图谱 Nebula `demo_gkx_chain` | ✅ 禁 `gkx_service`；不 CREATE SPACE |
| 可观测 | ✅ span `svc.graph.write`（无 OTel 时 no-op） |
| D12 | ✅ 只改 `demo-algo-ent-analysis`；未改 lumen / Vue |
| P0 灌数剥离 | ✅ grep 零命中；十模型不再写图 |

### Ponytail / Cost

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| actual_tokens | 180000 |
| model_used | grok-4.6 |
| actual_cost | 0.86 |
| cost_warn | green |

### 开放项（步2 不挡步3）

- registry 仍缺本叶 ID
- C 多数无稳定码 → `no_stable_id`（诚实跳过，不猜 VID）
- `OPEN-SVC-GRAPH-02` VID 前缀仍 as-built `institution:`
- 步4 才改 GraphView 按钮与灌数文案

---

## CI/CD（步1）

- 分支：`dev`（编排仓 `gkx-orchestration`）
- commit：`63dedf1a`（`docs(svc): 112/113 pipeline-to-nebula 步1 契约 [agent:data-agent]`）
- pipeline / K8s：文档仓无业务 rollout
- 验证：未跑灌数、未连 Nebula 写库

## 涉及文件

- `agent-delivery/data/data-design/storage/SVC/etl/pipeline-to-nebula.md`（新建）
- `agent-delivery/data/data-design/storage/SVC/etl/README.md`
- `agent-delivery/data/data-design/storage/SVC/etl/pipeline-demo-mock.md`（指针债说明）
- `agent-delivery/data/data-design/storage/SVC/README.md`
- `agent-delivery/data/data-design/storage/SVC/CHANGELOG.md`
- `agent-delivery/data/data-design/storage/SVC/stores/nebula/graph-svc.md`
- `agent-delivery/data/data-design/storage/SVC/stores/nebula/README.md`
- `agent-delivery/data/data-design/storage/README.md`
- `agent-delivery/agent-handoffs/服务机构-SVC/DEMO-SVC-GRAPH-TRIPLE-UI-L01.md`（本文件）

## CI/CD（步2）

- 仓：`demo-algo-ent-analysis` `origin/dev`
- commit：`e5960ab`（`feat(svc): 图谱 A/B/C /internal 并从灌数/十模型剥离 [agent:algorithm-agent]`）
- 验证：`python -m entan.svcgraph_ops` 绿；灌数入口 grep 写图符号 0
