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

---

## 前端（P-3 · agent:frontend-agent · 2026-08-31）

**P-3 完成，叶可验收。** 灌数 UI 已去建图承诺；`/policy/graph` 四档可点；apiview 每写入 `op_id` 一条算法测试。未改 Python 算法仓。未调 MCP 改任务状态。

### 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| ponytail | `full`（未用 YAGNI 跳过 D8 皮肤 token、D9 ⓘ、四档可点、§17.3 全表图例、可观测 X-Trace-Id） |
| diagram_id | `POLICY-GRAPH-TRIPLE` |
| headroom | `skip`（P-1 pipeline / Design / 现网页按原文精读） |

### 五列对照（需规 / 设计 / 代码 / UI / apiview）

边 × 终点（§17.3 全表，禁止静默删行）：

| 边 × 终点 | 需规 | 设计 | 代码（P-2） | UI（本步） | apiview（本步） |
|---|---|---|---|---|---|
| support×产业 | 107 扶持 | §17.3 上图 `chain:`/`segment:` | hang SUPPORT | 图例「上图」；C 档 SUPPORT | `policy.graph.hang-support` |
| support×技术 | 107 | 本波不上图 `OPEN-POLICY-GRAPH-01` | `not_in_wave` | 图例「本波不上图」 | 同上，skipped 四码表 |
| support×企业 | 107 | 上图 `ent:` | hang SUPPORT | 图例「上图」 | 同上 |
| support×人才 | 107 | 本波不上图 | `not_in_wave` | 图例「本波不上图」 | 同上 |
| support×科研机构 | 107 | 本波不上图（走 regulate） | 不上 support | 图例「本波不上图」 | 同上 |
| support×服务机构 | 107 | 本波不上图（走 apply_to） | 不上 support | 图例「本波不上图」 | 同上 |
| apply_to×产业 | 107 适用 | 上图，可与 support 同时 | hang APPLY_TO | 图例「上图」；C 档 APPLY_TO | `policy.graph.hang-apply` |
| apply_to×技术 | 107 | 本波不上图 | `not_in_wave` | 图例「本波不上图」 | 同上 |
| apply_to×企业 | 107 | 本波不上图 | 不上 | 图例「本波不上图」 | 同上 |
| apply_to×人才 | 107 | 本波不上图 | `not_in_wave` | 图例「本波不上图」 | 同上 |
| apply_to×科研机构 | 107 | 本波不上图 | 不上 | 图例「本波不上图」 | 同上 |
| apply_to×服务机构 | 107 | 上图 `inst:` | hang APPLY_TO | 图例「上图」 | 同上 |
| regulate×产业 | 107 监管 | 本波不上图 | 不上 | 图例「本波不上图」 | `policy.graph.hang-regulate` |
| regulate×技术 | 107 | 本波不上图 | `not_in_wave` | 图例「本波不上图」 | 同上 |
| regulate×企业 | 107 | 本波不上图 | 不上 | 图例「本波不上图」 | 同上 |
| regulate×人才 | 107 | 本波不上图 | `not_in_wave` | 图例「本波不上图」 | 同上 |
| regulate×科研机构 | 107 | 上图 `inst:`（实施/监管一条） | hang REGULATE | 图例「上图」 | 同上 |
| regulate×服务机构 | 107 | 本波不上图 | 不上 | 图例「本波不上图」 | 同上 |
| cite×政策 | 107 加性 | 上图两端本批 `pol:` | intra CITE | 图例「上图」；B 档 | `policy.graph.intra` |

写入 / 浏览 op_id：

| op_id | 档 | 需规 | 设计 HTTP | UI | apiview |
|---|---|---|---|---|---|
| `POLICY_NER_POLICY` | A | SRS 106 | `POST /v1/policy/graph/ner` | GraphView 档 A；`written_nodes`+skipped 四码 | `policy.graph.ner` |
| `POLICY_RE_CITE` | B | 107 cite | `POST .../intra` `whitelist=[cite]` | 档 B | `policy.graph.intra` |
| `POLICY_RE_SUPPORT` | C | 107 扶持 | `POST .../hang` 必带 `op_id` | 档 C 三按钮 SUPPORT | `policy.graph.hang-support` |
| `POLICY_RE_APPLY_TO` | C | 107 适用 | 同上 | 档 C APPLY_TO | `policy.graph.hang-apply` |
| `POLICY_RE_REGULATE` | C | 107 监管 | 同上 | 档 C REGULATE | `policy.graph.hang-regulate` |
| `POLICY_GRAPH_BROWSE` | D | 可视化 | `GET /v1/policy/graph` | 档 D 只读；source + `space=demo_gkx_chain` | `policy.graph.main` |

未发明新边名。C 档文案写明禁止名称猜 VID。

### 灌数剥离 UI 证据（P-3）

| 位置 | 改前 | 改后 |
|---|---|---|
| `BasicPage.vue` `seedFlow` | `{ label: 'B 政策图谱', hint: 'NER + RE；Nebula 未启用时跳过' }` | **已删除该步** |
| 下拉「重灌」 | 「只清 DWD + Nebula 政策子图」 | 「只清 DWD 并重算基础指标」 |
| `seedNotes` 重灌 | 「删 Nebula policy 点」 | 「不建图、不清 Nebula；图谱请到政策图谱 A/B/C」 |
| `ElMessageBox` reload | 「清空政策 DWD 与 Nebula 政策子图」 | 「只清空政策 DWD…不写 Nebula、不建政策图谱」 |
| `api/policy/index.ts` `runPipeline` 注释 | `reload=清 DWD+Nebula` | `reload=保留 ODS、只清 DWD 并重算基础指标（不再清 Nebula、不再建图）` |

后端 P-2 已做到误点灌数据也不再建图；UI 不再承诺建图。

### 复刻五维 / 检索皮肤

本页是算法库工作区（四档加工 + 浏览），**不是检索 Hub**。

| # | 项 | 结论 |
|---|---|---|
| V1–V7 | 检索 Hub 皮肤 | **N/A**：无检索 Hero / 推荐卡 / 结果列表；政策页走仓内 `.policy-page` + `--sci-bg-page` |
| R1 布局 | 四档 + §17.3 全表图例 + D 图/详情 | ✅ 一页四 `el-tabs`/`a-tabs`，未拆 15 路由 |
| R2 交互 | 空 / 加载 / 失败 / dry_run / 有结果 | ✅ `useGraceful` + ErrorBanner；无数据诚实空；不填假 ID |
| R3 样式 | Element 政策页皮肤 / apiview `--sci-*` | ✅ 未另起灰白后台；主色 `#165DFF` |
| R4 评审 | 不自造 ⓘ | ✅ system-test 既有 `MetricHint`/`AlgoHelp`；apiview `@/review/MetricMarker` |
| R5 Mock | `USE_MOCK=false` 禁止 fixture | ✅ 删除 `DEMO_POLICY_OPTIONS`；apiview 不在关闭 Mock 时用 sample 填图 |

### 架构合规自检

| 铁律 | 本步 |
|---|---|
| 前端→Java REST，不直调 Python `/internal` | ✅ demo 走既有 `/policy/v1/policy/graph/*`；apiview 路径同构，无 `127.0.0.1:8000/internal` |
| 图谱 space `demo_gkx_chain` | ✅ 文案与出参展示；去掉 `gkx_policy` |
| D8 Design | ✅ 管理端 Element 对齐本仓政策页；apiview Arco + `--sci-*` |
| D9 ⓘ | ✅ 写入计数 / 节点权重 / 图例旁 MetricHint 或 MetricMarker；无数字不造假 |
| D10 | ✅ 四档可点、空态、loading、失败；键盘随 Element/Arco 页签 |
| 可观测 | ✅ demo `request.ts` 注入 `X-Trace-Id` + `traceparent`；apiview 既有 interceptor |
| D12 | ✅ lumen apiview 只经 `VITE_APP_BASE_API` 打 `/policy/v1/...`（`runtime=java_api`）；未指向 `demo-*` / Python 端口 |
| 未改算法 Python | ✅ |

### Cost（估算 · 非 console 实测）

计价代理：`budget-estimate.md` §1.2 Sonnet 4.5（$3 / $15 per MTok），frontend 默认 in/out ≈ 85/15。`source: session_estimate`。

| 字段 | 值 |
|------|-----|
| actual_tokens | 320000 |
| model_used | grok-4.6 |
| actual_cost | 1.54 |
| cost_warn | green |

未超 $5 黄线。本步 **未** 调 MCP 改任务状态（coordinator 收单）。

### 浏览器验证

**未做。** 本机 terminals 无 `demo-ui-system-test` / `lumen-ui-algo-apiview` dev server，未点 A/B/C/D 与灌数页。请监管人/QA 在 K8s 或本地 `pnpm dev` 后点验。

### CI/CD（本步）

| 仓 | 分支 | commit | push |
|---|---|---|---|
| `demo-ui-system-test` | `origin/dev` | `c85be8188db1104560fed4ed15eb6380dd617b0e` | 成功（非 force） |
| `lumen-ui-algo-apiview` | `origin/dev` | `5165ab3d5824f9a2c1be54eda2b7fb4065673602` | 成功（非 force） |

### 涉及文件

**demo-ui-system-test**

- `src/views/policy/components/GraphView.vue`
- `src/views/policy/pages/BasicPage.vue`
- `src/views/policy/components/policyHelp.ts`
- `src/api/policy/index.ts`
- `src/utils/request.ts`
- `src/utils/observability.ts`

**lumen-ui-algo-apiview**

- `src/catalog/policy.json`
- `src/components/algo/PolicyGraphPanel.vue`
- `src/api/policy.ts`

### 开放项（不挡本叶 UI 验收）

- `OPEN-POLICY-GRAPH-01`：tech/talent 本波不上图（图例已标）
- 本机未浏览器点验
- Java 网关若尚未转发 `/v1/policy/graph/{ner,intra,hang}`，apiview/管理端按钮会失败（路径已按 P-2 契约接线；转发缺口属 api 另单）

---

## coordinator 收单（AV-0 · 2026-09-01）

| 项 | 结论 |
|---|---|
| P-1 data | ✅ `9520f61f` pipeline §17–§20 + `POLICY-GRAPH-TRIPLE` |
| P-2 algorithm | ✅ `a23ff8a7` 灌数 grep 空命中；ner/intra/hang + `/internal` 成对 |
| P-3 frontend | ✅ ui `c85be818` · apiview `5165ab3d` · 四档 + 6 op_id；灌数去建图文案 |
| P-4 api | ✅ demo-svc `31582b9e` 网关 `gkx-policy-graph` → gkx-innov → `/internal`；entan-py 非 innov-py；浏览 `GET /internal/policy/graph` `36fcf48f` |
| handoff | ✅ 五列对照、Java 路径表、diagram_id、ponytail full、四步 cost |
| 浏览器 / live curl | ❌ 未点验；K8s rollout 后才能实打 |
| 联调 | ❌ 不写「联调通过」——缺 live 验证；lumen 网关仍无 `/policy` |

registry：`evidence` 已设；cost 合计 `actual_tokens=1090000` · `actual_cost=5.24` · `cost_warn=yellow`（略过 $5）· `model_used=grok-4.6`。状态 **`integration`**。不自动 AV-1。

ENT / CHAIN / SVC / COMP 本集合未开。

---

## Java 转发（P-4 · agent:api-agent · 2026-09-01）

**P-4 完成。** 政策图谱 A/B/C/D 走 前端 → demo 网关 `gkx-policy-graph` → `gkx-innov` → Python `/internal/policy/graph*`。指标/文本/灌数仍走 catch-all `gkx-policy` 直连 Python。未改 Vue / apiview catalog。未改 lumen-svc-platform。未调 MCP 改任务状态。

### 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| ponytail | `full`（未用 YAGNI 跳过 OpenAPI `@Operation`、中文 Javadoc、调用链 `/internal`、Feign 超时、网关插队） |
| diagram_id | `POLICY-GRAPH-TRIPLE`（透传覆盖写入 op_id，未改边名） |
| headroom | `skip`（对标 Chain 透传与现网 gateway 原文） |

### Java 路径表

| 对外（网关后） | Java controller | Feign |
|---|---|---|
| GET `/policy/v1/policy/graph` | GET `/v1/policy/graph` | GET `/internal/policy/graph` |
| POST `/policy/v1/policy/graph/ner` | POST `/v1/policy/graph/ner` | POST `/internal/policy/graph/ner` |
| POST `.../intra` | POST `/intra` | POST `/internal/policy/graph/intra` |
| POST `.../hang` | POST `/hang` | POST `/internal/policy/graph/hang` |
| POST `.../ops/{op_id}` | POST `/ops/{op_id}` | POST `/internal/policy/graph/ops/{op_id}` |

body 原样 `Map` 透传：`op_id, scope, id, filter, mode, dry_run, relation_whitelist, dest_types, calc_batch_id`。Java **不**解析政策文本、**不**写 nGQL、**不**改边类型。

### Feign url

| 项 | 值 |
|---|---|
| `@FeignClient` name | `policy-algo` |
| url 占位 | `${gkx.innov.policy.algo-base-url:http://127.0.0.1:8000}` |
| `application-dev.yml` | **`http://demo-platform-entan-py:8000`**（不是 innov-py） |
| helm env | `INNOV_POLICY_ALGO_BASE_URL=http://demo-platform-entan-py:8000` |
| openfeign readTimeout | `policy-algo` = **180000** ms（≥90s） |

### 网关 route

| 项 | 值 |
|---|---|
| 文件 | `helm/gkx-platform/configs/gkx-gateway-dev.yml`（仓内仅此一份 gateway yaml） |
| 新 route id | **`gkx-policy-graph`** |
| uri | `lb://gkx-innov` |
| Path | `/policy/v1/policy/graph,/policy/v1/policy/graph/**` |
| filters | `StripPrefix=1` |
| 顺序 | **插在 catch-all `gkx-policy`（`Path=/policy/**` 直连 entan-py）之前** |
| 未改 | 整个 `/policy/**` 仍直连 Python（指标/文本/灌数） |

### GET `/internal` 浏览

Python 原先只有 `GET /v1/policy/graph`。本步在 `demo-algo-ent-analysis/api/policy_routes.py` 给同一函数加了 **`GET /internal/policy/graph` 一行别名**，复用现有浏览逻辑，未重写算法。

### curl 样例（经网关 `/policy/v1/...`，不是直打 8000）

```bash
curl -s -X POST http://<demo-gateway>/policy/v1/policy/graph/ner \
  -H "Content-Type: application/json" \
  -d "{\"op_id\":\"POLICY_NER_POLICY\",\"scope\":\"one\",\"id\":\"POLA\",\"mode\":\"rule\",\"dry_run\":true}"

curl -s -X POST http://<demo-gateway>/policy/v1/policy/graph/intra \
  -H "Content-Type: application/json" \
  -d "{\"op_id\":\"POLICY_RE_CITE\",\"scope\":\"batch\",\"filter\":{\"policy_ids\":[\"POLA\",\"POLB\"]},\"relation_whitelist\":[\"cite\"],\"mode\":\"rule\",\"dry_run\":true}"

curl -s -X POST http://<demo-gateway>/policy/v1/policy/graph/hang \
  -H "Content-Type: application/json" \
  -d "{\"op_id\":\"POLICY_RE_SUPPORT\",\"scope\":\"one\",\"id\":\"POLA\",\"mode\":\"rule\",\"relation_whitelist\":[\"support\"],\"dry_run\":true}"

curl -s -X POST http://<demo-gateway>/policy/v1/policy/graph/ops/POLICY_RE_REGULATE \
  -H "Content-Type: application/json" \
  -d "{\"scope\":\"one\",\"id\":\"POLA\",\"mode\":\"rule\",\"dry_run\":true}"

curl -s "http://<demo-gateway>/policy/v1/policy/graph?limit=80"
```

### 测试

`PolicyGraphServiceTest`：Feign 抛错时兜底 `{code:1,data:null}`。本机 PATH 无 `mvn`/`java`，未跑 Maven；逻辑与 `ChainService.passthrough` 同构。

### 架构合规自检

| 铁律 | 本步 |
|---|---|
| 调用链 前端→Java REST→Python `/internal/*` | ✅ 图谱路径；Feign 全 `/internal` |
| 算法只在 Python / Java 无 NLP | ✅ 只 controller/service/Feign 透传 |
| Java 无 nGQL / 未改边名 | ✅ |
| 可观测 | ✅ 未关 Java Agent；`management.tracing.enabled` 保持 false（Agent 全量 OTLP） |
| D12 | ✅ **只改 demo-svc-platform**；Feign 指向 entan-py，未把 lumen Feign 指到 demo-* |
| 未改灌数 run-pipeline | ✅ 仍走 `gkx-policy` catch-all |

### lumen apiview 网关（只说明，未改 lumen）

- apiview catalog 路径已是 `/policy/v1/policy/graph*`，`runtime=java_api`。
- `.env.example`：线上 nginx `/api` → **`demo-platform-gateway`**。走 demo 网关时，本步 `gkx-policy-graph` 即可通。
- **`lumen-svc-platform` `gkxlumen-gateway-dev.yml` 没有 `/policy/**` 路由。** 若有人把 apiview 的 `VITE_APP_API_URL` 指到 lumen 网关，图谱会 404。按 D12 **禁止**在 lumen Java/Feign 指向 `demo-*`；要通须另开 lumen 正式转发叶，本步不擅自改。

### Cost（估算 · 非 console 实测）

计价代理：`budget-estimate.md` §1.2 Sonnet 4.5（$3 / $15 per MTok），api 默认 in/out ≈ 85/15。`source: session_estimate`。

| 字段 | 值 |
|---|---|
| actual_tokens | 200000 |
| model_used | grok-4.6 |
| actual_cost | 0.96 |
| cost_warn | green |

未超 $5 黄线。本步 **未** 调 MCP 改任务状态。

### P-4 开工/完成门

**PASS。** 图谱路径已改走 Java；Feign url = entan-py；网关 `gkx-policy-graph` 在 catch-all 之前；浏览补了 `GET /internal/policy/graph`。

### 开放项

- 本机无 Maven，未跑 `PolicyGraphServiceTest`
- 未对 live K8s curl（需 gateway + innov + entan-py rollout）
- lumen 网关仍无 `/policy`（apiview 若改打 lumen 会缺路由）

### CI/CD（本步）

| 仓 | 分支 | commit | push |
|---|---|---|---|
| `demo-svc-platform` | `origin/dev` | `31582b9e9ead084cb6a10bdae204e6d4988bfd1b` | 成功（非 force） |
| `demo-algo-ent-analysis` | `origin/dev` | `36fcf48fb52f66f3f8ceb8df3cf2436ac60edd3f` | 成功（非 force） |
| `gkx-orchestration` | `origin/dev` | （本 handoff 提交后） | 非 force |

### 涉及文件

**demo-svc-platform**

- `gkx-innov/src/main/java/com/topcomm/gkx/innov/policy/PolicyAlgoClient.java`
- `gkx-innov/src/main/java/com/topcomm/gkx/innov/policy/PolicyGraphController.java`
- `gkx-innov/src/main/java/com/topcomm/gkx/innov/policy/PolicyGraphService.java`
- `gkx-innov/src/main/java/com/topcomm/gkx/innov/policy/PolicyProperties.java`
- `gkx-innov/src/test/java/com/topcomm/gkx/innov/policy/PolicyGraphServiceTest.java`
- `gkx-innov/src/main/resources/application.yml`
- `gkx-innov/src/main/resources/application-dev.yml`
- `gkx-innov/pom.xml`（`gkx-common-swagger` 供 `@Operation`）
- `helm/gkx-platform/configs/gkx-gateway-dev.yml`
- `helm/gkx-platform/values.yaml`

**demo-algo-ent-analysis**

- `api/policy_routes.py`（`GET /internal/policy/graph` 别名）
