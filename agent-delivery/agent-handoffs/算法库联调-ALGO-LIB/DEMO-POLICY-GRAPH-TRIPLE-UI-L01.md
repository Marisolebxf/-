# DEMO-POLICY-GRAPH-TRIPLE-UI-L01 · 政策图谱三元组闭环

> 叶内三步：P-1 data-agent → P-2 algorithm-agent → P-3 frontend-agent。本文按步追加，不覆盖他人段落。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent`（本步 P-1；步 2/3 由 coordinator 切换） |
| supervised_by | `human:淮政玮`（全程不准改） |
| claim_type | `coordinator_dispatch` |
| 说明 | 厚包 `COORD-GRAPH-TRIPLE-UI-DISPATCH-20260831.md` §9；监管人已授权全链路 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 文档完整性优先；未用 YAGNI 裁掉接口表 / 过程图 / 边×终点矩阵。本步不改 UI，D8/D9/D10 由 P-3 落地。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求 SRS 与现网 pipeline 读原文，禁止 compress 代替精读。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-GRAPH-TRIPLE` |
| 图 diff | 新增目标态：灌数零图谱 → A NER 政策点 → B `cite` → C `support`/`apply_to`/`regulate` hang；tech/talent 标不上图；禁止灌数调用 `graph.run` / `nebula_loader` |
| 会签态 | 存储拓扑 `01-data-flow.md` 仍为 `approved`；本图为 P-1 契约稿（draft 实现，P-2 按图编码） |

---

## 数据设计（P-1 · agent:data-agent · 2026-08-31）

**P-1 完成，P-2 可开工。** 无文档阻塞。P-2 不得在文档不齐前提前写接口；实现必须对照 `pipeline-to-nebula.md` §17–§18。

### 范围与实现（对照 SRS 106 / 107）

| 项 | 政策实体识别构建 | 政策实体关系抽取 |
|---|---|---|
| seq | **106** | **107** |
| metric_id | `M_POLICY_GRAPH_106_1` | `M_POLICY_GRAPH_107_1` |
| 本步落点 | 档 **A** `POLICY_NER_POLICY`：政策点 + 属性 NER | 档 **B** `cite`；档 **C** `support` / `apply_to` / `regulate` |
| 原文要点 | 规则+词典识别名称/级别/类型/地点/时间；维护增删改 | NLP+规则；扶持/适用/监管；对接产业、技术、企业、人才、科研机构、服务机构 |
| 本波诚实 | 属性不上图 | tech/talent **本波不上图**（`OPEN-POLICY-GRAPH-01`）；无稳定 ID 不上图；禁止名称猜 VID |

档 **D** = 只读 `GET /v1/policy/graph`，不写库。Space = **`demo_gkx_chain`**（禁止 `gkx_policy` 第二空间）。产业 as-built 可同时 `support`+`apply_to`。

真源（只写编排仓，未改业务代码）：

`agent-delivery/data/data-design/storage/POLICY/etl/pipeline-to-nebula.md` §17–§20（§1–§16 语义保留）。

### 关系 × op_id × I/O 摘要

| op_id | 档 | HTTP | 输入要点 | 输出要点 | 本波 |
|---|---|---|---|---|---|
| `POLICY_NER_POLICY` | A | `POST /v1/policy/graph/ner` → `/internal/policy/graph/ner` | `scope=one\|batch`；`id` 或 filter；`mode=rule\|llm`；`dry_run` | `written_nodes`（`pol:`）；`skipped` 四码；`source`/`model_version`/`calc_batch_id` | 政策点上图；属性只进 `policy_entity` |
| `POLICY_RE_CITE` | B | `POST /v1/policy/graph/intra` | 同上 + `relation_whitelist=[cite]` | `written_edges` cite；悬挂 pid → `no_stable_id` | 两端本批 `pol:` |
| `POLICY_RE_SUPPORT` | C | `POST /v1/policy/graph/hang` | 必须带 `op_id` 或白名单；`dest_types` | hang 前 `FETCH`；无 ID 不上图 | 产业/企业上图；**技术/人才不上图** |
| `POLICY_RE_APPLY_TO` | C | 同上 | 白名单含 `apply_to` | 同 hang 契约 | 产业/服务机构上图；技术不上图 |
| `POLICY_RE_REGULATE` | C | 同上 | 白名单含 `regulate` | 同 hang 契约 | 科研/实施 `inst:`；实施 vs 监管现网一条 |
| `POLICY_GRAPH_BROWSE` | D | `GET /v1/policy/graph` | 只读 | 不写 ADS/Nebula | 现网查询保留 |

公共：`dry_run` 不写 ADS/Nebula；同 `calc_batch_id`+主键可重跑覆盖；LLM 只在 `mode=llm`，无 Key 回退规则且 `llm_fallback=true`。`skipped.reason` ∈ `empty_field` / `no_stable_id` / `not_in_wave` / `vid_too_long`。需规 3×6 边×终点 + `cite` 全表见 §17.3，**无静默删行**。

### 灌数剥离清单（文件 / 函数级）

P-2 必须从灌数路径摘掉（checklist）：

| 文件 | 符号 |
|---|---|
| `scripts/run_all_policy.py` | import `entity as graph`；`build_steps` 的 `graph.run`；`load_nebula_safe()` → `nebula_loader.run()` |
| `polan/graph/entity.py` | `run()` 禁止被灌数调用（可留作 A/B/C 核） |
| `polan/graph/nebula_loader.py` | `ensure_schema` / `run` / `_load_nodes` / `_load_edges` 禁止进 `run_all` / `run-pipeline` |
| `api/policy_routes.py` | `run_policy_pipeline()` 经 `build_steps` 间接触发；`POST /internal/policy/run-pipeline` |
| `polan/mockgen/incr.py` | `clear_policy_nebula()`（`DELETE VERTEX`）；`reload_from_ods()` 内对该函数的调用 |
| `polan/mockgen/generate.py` | `mode=reload` 清 Nebula 文案与分支 |
| `demo-ui-system-test/.../policy/pages/BasicPage.vue` | 「灌数据」`onSeed`；`seedFlow`「B 政策图谱」；reload「清 DWD + Nebula」 |
| `demo-ui-system-test/.../api/policy/index.ts` | `runPipeline` 注释中的 Nebula 副作用 |

灌数只留：三方/Mock → ODS → DWD（+ 可选 `basic.indicators`）。CLI `python -m polan.graph.entity` / `nebula_loader` 不得进灌数 runbook。重灌后图空或旧图不被灌数填满 = 预期。

### 架构合规自检

| 铁律 | 本步 |
|---|---|
| 算法只在 Python | ✅ 契约写 Python `/internal`；Java 只转发 |
| 调用链 前端→Java→Python `/internal/*` | ✅ §17.1 HTTP 表 |
| 图谱 Nebula `demo_gkx_chain` | ✅ 禁止 `gkx_policy` 第二空间 |
| D12 | ✅ 本步只改编排仓文档；未改 `demo-ui-*` / `lumen-ui-*`；未改 `demo-algo-*` 代码 |
| 不灌数 / 不 APPLY DDL | ✅ |
| P0 灌数剥离 | ✅ 清单已落 §18；实现属 P-2 |

### Cost（估算 · 非 console 实测）

计价代理：`budget-estimate.md` §1.2 Sonnet 4.5（$3 / $15 per MTok），data/doc 默认 in/out ≈ 85/15。`source: session_estimate`。

| 字段 | 值 |
|---|---|
| actual_tokens | 220000 |
| model_used | grok-4.6 |
| actual_cost | 1.06 |
| cost_warn | green |

未超 $5 黄线。coordinator 收单时回填 registry（本步 **未** 调 MCP 改状态）。

### P-2 开工门

**PASS。** 文档已含：op_id I/O、边×终点全表、灌数剥离文件级清单、`diagram_id=POLICY-GRAPH-TRIPLE`。

P-2 打开条件（coordinator 核）：本文件 + `pipeline-to-nebula.md` 已 `origin/dev`。P-2 只改 `demo-algo-ent-analysis`（及 Java 转发预留，可不改）；不改图谱菜单 Vue。

### 开放项

- `OPEN-POLICY-GRAPH-01`：tech / talent 本波不上图
- `OPEN-POLICY-GRAPH-03`：S3 边 DDL vs as-built `(weight, props)`
- 实施主体 vs 监管机构揉成一条 `regulate`（`QPOL-02` / 唐绍祖会签）
- L6 名称链指须淮政玮拍板，默认关闭
- `pipeline-demo-mock.md` 15 步全景仍含 B/B+：P-2 剥代码后再另单改该稿（本 P-1 真源是 `pipeline-to-nebula.md` §18）

---

## CI/CD（本步）

- 分支：`dev`（编排仓 `gkx-orchestration`）
- commit：见 git log（本步提交后回填 hash）
- pipeline / K8s：文档仓无业务 rollout
- 验证：未跑灌数、未连 Nebula 写库

## 涉及文件

- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-to-nebula.md`（§17–§20 + 文首指针）
- `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/DEMO-POLICY-GRAPH-TRIPLE-UI-L01.md`（本文件）

---

## 算法（P-2 · agent:algorithm-agent · 2026-08-31）

**P-2 完成，P-3 可开工。** 灌数路径零图谱调用；A/B/C 接口可 curl。未改 GraphView / apiview catalog / 任何 Vue。

### 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| ponytail | `full`（未用 YAGNI 跳过可观测 span、I/O 四码、灌数剥离） |
| diagram_id | `POLICY-GRAPH-TRIPLE` |
| headroom | `skip`（契约与现网代码按原文精读） |

### 范围（对照 §17 op_id）

| op_id | 档 | HTTP | 实现 |
|---|---|---|---|
| `POLICY_NER_POLICY` | A | `POST /v1/policy/graph/ner` + `/internal/policy/graph/ner` | `polan.graph.ops.execute`；政策点 `pol:` + `policy_entity`；属性不上图 |
| `POLICY_RE_CITE` | B | `POST /v1/policy/graph/intra` + `/internal/.../intra` | pedigree `上位政策:pid`；不在本批 → `no_stable_id` |
| `POLICY_RE_SUPPORT` | C | `POST /v1/policy/graph/hang`（`op_id` 或白名单） | FETCH `chain:`/`segment:`/`ent:`；tech/talent → `not_in_wave` |
| `POLICY_RE_APPLY_TO` | C | 同上 | 产业 + 服务 `inst:`；产业可与 support 同时落边 |
| `POLICY_RE_REGULATE` | C | 同上 | FETCH `inst:`；实施/监管仍一条 |
| `POLICY_GRAPH_BROWSE` | D | `GET /v1/policy/graph` | 现网保留，本步未改 |

并存：`POST /v1|/internal/policy/graph/ops/{op_id}`。`dry_run` 不写 ADS/Nebula。`mode=llm` 无 Key → `mode_effective=rule`、`llm_fallback=true`。C 档未 FETCH 命中 → `no_stable_id`，禁止名称猜 VID。Space = `demo_gkx_chain`。

灌数剥离：`run_all_policy.build_steps` 删除 B/`graph.run` 与 B+/`load_nebula_safe`；`reload_from_ods` 去掉 `clear_policy_nebula`；`run-pipeline` 仍灌 ODS→DWD（+基础指标/深度/文本），不再建图。

### 灌数剥离 grep 证据

仓：`demo-algo-ent-analysis` @ `a23ff8a7`。模式：`entity.run|nebula_loader|ensure_schema|INSERT VERTEX|INSERT EDGE|clear_policy_nebula|graph.run`

```text
Select-String -Path "scripts\run_all_policy.py" -Pattern "entity\.run|nebula_loader|ensure_schema|INSERT VERTEX|INSERT EDGE|clear_policy_nebula|graph\.run"
→ hits=0

Select-String -Path "polan\mockgen\generate.py" -Pattern <同上>
→ hits=0

Select-String -Path "polan\mockgen\incr.py" -Pattern <同上>
→ hits=0

Select-String -Path "api\policy_routes.py" -Pattern <同上>
→ hits=0
```

函数级：`inspect.getsource(reload_from_ods / run_policy_pipeline / policy_run_pipeline)` 对上列符号 **FORBIDDEN=False**。`build_steps` 不再含「B 政策实体识别」/「B+ 政策图谱投影」。

自检：`python -m polan.graph.ops` → `policy graph ops self_check OK ner_nodes=1`（sqlite；dry_run 不写库；llm 无 Key 回退；cite 本批可写；tech/talent=`not_in_wave`；无 Nebula 时 hang=`no_stable_id`）。

### curl 样例（路径与 JSON 真实；未对 live 执行）

```bash
curl -s -X POST http://127.0.0.1:8000/internal/policy/graph/ner \
  -H "Content-Type: application/json" \
  -d "{\"op_id\":\"POLICY_NER_POLICY\",\"scope\":\"one\",\"id\":\"POLA\",\"mode\":\"rule\",\"dry_run\":true}"

curl -s -X POST http://127.0.0.1:8000/v1/policy/graph/ner \
  -H "Content-Type: application/json" \
  -d "{\"scope\":\"batch\",\"filter\":{\"all\":true},\"mode\":\"llm\",\"dry_run\":false}"

curl -s -X POST http://127.0.0.1:8000/internal/policy/graph/intra \
  -H "Content-Type: application/json" \
  -d "{\"op_id\":\"POLICY_RE_CITE\",\"scope\":\"batch\",\"filter\":{\"policy_ids\":[\"POLA\",\"POLB\"]},\"relation_whitelist\":[\"cite\"],\"mode\":\"rule\",\"dry_run\":true}"

curl -s -X POST http://127.0.0.1:8000/internal/policy/graph/hang \
  -H "Content-Type: application/json" \
  -d "{\"op_id\":\"POLICY_RE_SUPPORT\",\"scope\":\"one\",\"id\":\"POLA\",\"mode\":\"rule\",\"relation_whitelist\":[\"support\"],\"dry_run\":true}"

curl -s -X POST http://127.0.0.1:8000/v1/policy/graph/hang \
  -H "Content-Type: application/json" \
  -d "{\"op_id\":\"POLICY_RE_APPLY_TO\",\"scope\":\"one\",\"id\":\"POLA\",\"relation_whitelist\":[\"apply_to\",\"support\"],\"mode\":\"rule\",\"dry_run\":false}"

curl -s -X POST http://127.0.0.1:8000/internal/policy/graph/ops/POLICY_RE_REGULATE \
  -H "Content-Type: application/json" \
  -d "{\"scope\":\"one\",\"id\":\"POLA\",\"mode\":\"rule\",\"dry_run\":true}"
```

公共出参字段：`written_nodes[]` / `written_edges[]` / `skipped[]`（四码）/ `source` / `model_version` / `calc_batch_id` / `mode_effective` / `llm_fallback` / `space=demo_gkx_chain`。

### 架构合规自检

| 铁律 | 本步 |
|---|---|
| 算法只在 Python | ✅ `polan/graph/ops.py`；Java 未改、不写 NLP |
| 调用链 前端→Java→Python `/internal/*` | ✅ 对外 `/v1` 与内部 `/internal` 成对 |
| 图谱 Nebula `demo_gkx_chain` | ✅ `space` 恒该值；禁止名称猜 VID |
| 可观测 | ✅ `opentelemetry` span `policy.graph.write`（仓内已有 OTel，无新依赖） |
| 未改 UI / apiview | ✅ 无 Vue、无 catalog |
| D12 | ✅ 只改 `demo-algo-ent-analysis`；未打 lumen 前端 |
| P0 灌数剥离 | ✅ grep 空命中 |

### Cost（估算 · 非 console 实测）

计价代理：`budget-estimate.md` §1.2 Sonnet 4.5（$3 / $15 per MTok），algorithm 默认 in/out ≈ 85/15。`source: session_estimate`。

| 字段 | 值 |
|------|-----|
| actual_tokens | 350000 |
| model_used | grok-4.6 |
| actual_cost | 1.68 |
| cost_warn | green |

未超 $5 黄线。本步 **未** 调 MCP 改任务状态。

### P-3 开工门

**PASS。** 接口齐、灌数零图调用、文档 `diagram_id=POLICY-GRAPH-TRIPLE`。P-3 只改 `demo-ui-system-test` / `lumen-ui-algo-apiview`：灌数文案去建图、图谱菜单 A/B/C/D、apiview 按 op_id。

### 开放项

- `OPEN-POLICY-GRAPH-01`：tech / talent 本波不上图（接口已 `not_in_wave`）
- `OPEN-POLICY-GRAPH-03`：边 DDL vs as-built `(weight, props)`
- L6 名称链指默认关闭
- `pipeline-demo-mock.md` 15 步全景仍含 B/B+：代码已剥，该稿由 data/doc 另单改
- UI「灌数据」文案仍可能写建图（P-3）；后端已做到即使点灌数据也不再建图

### CI/CD（本步）

- 仓 / 分支：`demo-algo-ent-analysis` `origin/dev`
- commit：`a23ff8a71c7db9169f9f81ce5e2c088db84bdaaf`
- 已 `git push origin dev`（非 force）
- 验证：`python -m polan.graph.ops` 自检绿；未对 live Nebula 写库

### 涉及文件（算法仓）

- `scripts/run_all_policy.py`
- `api/policy_routes.py`
- `polan/graph/ops.py`（新）
- `polan/graph/entity.py`
- `polan/graph/nebula_loader.py`
- `polan/graph/__init__.py`
- `polan/mockgen/incr.py`
- `polan/mockgen/generate.py`
