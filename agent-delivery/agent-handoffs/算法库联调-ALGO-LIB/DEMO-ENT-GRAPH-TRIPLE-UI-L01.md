# DEMO-ENT-GRAPH-TRIPLE-UI-L01 · 企业图谱三元组闭环

> 叶内四步：步1 data-agent → 步2 algorithm-agent → 步3 api-agent → 步4 frontend-agent。本文按步追加，不覆盖他人段落。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent`（本步 1/4；步 2/3/4 由 coordinator 切换） |
| supervised_by | `human:徐滕强`（全程不准改） |
| claim_type | `coordinator_dispatch` |
| 说明 | 厚包 `COORD-GRAPH-TRIPLE-UI-DISPATCH-20260831.md` §0.5/§4/§7.0；综合叶 `DEMO-COMP-GRAPH-TRIPLE-UI-L01` 仍 backlog，本叶四步完再开 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 文档完整性优先；未用 YAGNI 裁掉接口表 / 过程图 / 边×终点矩阵。本步不改 UI，D8/D9/D10 由步4 落地。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求 SRS 与现网 pipeline 读原文，禁止 compress 代替精读。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `ENT-GRAPH-TRIPLE` |
| 图 diff | 新增目标态：灌数零图谱 → A NER 企业点 → B `cooperate`/`parent_sub`（`invest` 本波不上图）→ C 产业/技术/人才/政策/科研/服务 hang；space 目标 `demo_gkx_chain`；禁止灌数调用 `entity.run` / `load_nebula_safe` / yiji persist |
| 会签态 | 存储拓扑 `01-data-flow.md` 仍为 `approved`；本图为步1 契约稿（draft 实现，步2 按图编码） |

---

## 数据设计（步1 · agent:data-agent · 2026-09-01）

**步1 完成，步2 可开工。** 无文档阻塞。步2 不得在文档不齐前提前写接口；实现必须对照 `pipeline-to-nebula.md` §17–§18。

### 范围与实现（对照 SRS 108 / 109）

| 项 | 企业实体识别构建 | 企业实体关系抽取 |
|---|---|---|
| seq | **108** | **109** |
| metric_id | `M_ENT_GRAPH_108_1` | `M_ENT_GRAPH_109_1` |
| 本步落点 | 档 **A** `ENT_NER_ORG`：企业点 + 属性 NER | 档 **B** 合作/投资/归属；档 **C** 跨域六类 |
| 原文要点 | 工商/新闻/财报/招聘；名称/类型/行业/地理 + 营收/员工/高管/融资/市值/产品/技术 | 合作、投资、归属、产业所属、技术应用、人才关系、政策适用、科研合作、服务提供 |
| 本波诚实 | 属性不上图；融资额/市值/员工总数/班子缺列 → `empty_field` | 投资/政策适用 **本波不上图**（行保留）；无稳定 ID 不上图；禁止名称猜 VID |

档 **D** = 只读 `GET /v1/entan/graph`，不写库。Space = **`demo_gkx_chain`**（禁止 `gkx_enterprise` / 继续把 `demo_entan` 当目标）。as-built space 仍是 `entan` + `FIXED_STRING(64)`，见 `OPEN-ENT-GRAPH-VID`。

真源（只写编排仓，未改业务代码）：

`agent-delivery/data/data-design/storage/ENT/etl/pipeline-to-nebula.md` §1–§20（§1–§9 as-built，§10–§20 与政策同构）。

### 关系 × op_id × I/O 摘要

| op_id | 档 | HTTP | 输入要点 | 输出要点 | 本波 |
|---|---|---|---|---|---|
| `ENT_NER_ORG` | A | `POST /v1/entan/graph/ner` → `/internal/entan/graph/ner` | `scope=one\|batch`；`org_id` 或 filter；`mode=rule\|llm`；`dry_run` | `written_nodes`（`ent:`）；`skipped` 四码；`source`/`model_version`/`calc_batch_id` | 企业点上图；属性只进 `entity_recognition` |
| `ENT_RE_COOP` | B | `POST /v1/entan/graph/intra` | 同上 + 白名单 `[cooperate]` | `written_edges` cooperate；对端无 ID → `no_stable_id` | 两端 `ent:` |
| `ENT_RE_INVEST` | B | 同上 | 白名单含 `invest` | 默认 skipped | **不上图** `OPEN-ENT-GRAPH-INVEST` |
| `ENT_RE_BELONG` | B | 同上 | 白名单含 `parent_sub` | 母→子 | 两端 `ent:` |
| `ENT_RE_INDUSTRY` | C | `POST /v1/entan/graph/hang` | 必须带 `op_id` 或白名单；`dest_types` | hang 前 `FETCH` `chain:`/`segment:` | 禁止 `ind:{名}` |
| `ENT_RE_TECH` | C | 同上 | 白名单含 `produces` | 已有技术点才写 | 无专题库 ID → 不上图 |
| `ENT_RE_TALENT` | C | 同上 | `talent_coop` | 稳定人才 ID | 名称 → `no_stable_id` |
| `ENT_RE_POLICY` | C | 同上 | 政策适用 | 默认 skipped | **不上图** `OPEN-ENT-GRAPH-POLICY` |
| `ENT_RE_RESEARCH` | C | 同上 | `research_coop` | `FETCH` `inst:` | 名称键废除 |
| `ENT_RE_SERVICE` | C | 同上 | `service_provide` | `FETCH` `inst:` | 同上 |
| `ENT_GRAPH_BROWSE` | D | `GET /v1/entan/graph` | 只读 | 不写 ADS/Nebula | 现网 `/v1/graph/*` 可并存只读 |

加性（非需规最低集）：`ENT_RE_SUPPLY` / `supply`。禁止用供应链顶替投资。

公共：`dry_run` 不写 ADS/Nebula；同 `calc_batch_id`+主键可重跑覆盖；LLM 只在 `mode=llm`，无 Key 回退规则且 `llm_fallback=true`。`skipped.reason` ∈ `empty_field` / `no_stable_id` / `not_in_wave` / `vid_too_long`。需规边×终点全表见 §17.3，**无静默删行**。

Java（步3 才编码）：抄政策 `31582b9e`；网关在 `/entan/**` 之前插 graph 路由 → `gkx-innov` → Feign **`demo-platform-entan-py:8000`** `/internal/entan/graph*`；禁止 innov-py；禁止 catch-all 直连 Python 写图。

### 灌数剥离清单（文件 / 函数级）

步2 必须从灌数路径摘掉（checklist）：

| 文件 | 符号 |
|---|---|
| `scripts/run_all.py` | import `entity as b`；`build_steps` 的 `b.run`；`load_nebula_safe()`（yiji persist + `nebula_loader.run`）；`init_membership_safe` |
| `entan/graph/entity.py` | `run()` 禁止被灌数调用（可留作 A/B/C 核） |
| `entan/graph/nebula_loader.py` | `ensure_schema` / `run` / `_load_*` 禁止进 `run_all` / `run-pipeline` |
| `entan/graph/incremental.py` | 灌数不得 `init_membership` 顺带灌满图 |
| `entan/yiji_sim/pipeline.py` · `scripts/run_yiji_sim.py` | `--apply --persist` 写图从灌数摘掉 |
| `entan/llm_ods/demo_graph.py` · `scripts/seed_demo_graph.py` | `INSERT VERTEX/EDGE`、`demo_entan` 灌 `supply` |
| `scripts/run_ent_chain_hang.py` | MySQL 上链可留；nGQL 不得当灌数据建图 |
| `api/main.py` | `POST /internal/run-pipeline` 经 `build_steps` 间接触发；`POST /v1/graph/nodes|infer` 不得挂灌数 |
| `demo-ui-system-test/.../entan/pages/BasicPage.vue` | 「灌数据」`onSeed`；`seedFlow`「NER/RE 建图；Nebula 灌入；图谱成员初始化」 |

灌数只留：三方/Mock → ODS → DWD（+ 可选 `basic.indicators` / 技商力 / 深度只读图）。CLI `python -m entan.graph.entity` / `nebula_loader` 不得进灌数 runbook。重灌后图空或旧图不被灌数填满 = 预期。

### 架构合规自检

| 铁律 | 本步 |
|---|---|
| 算法只在 Python | ✅ 契约写 Python `/internal`；Java 只转发 |
| 调用链 前端→Java→Python `/internal/*` | ✅ §17.1 / §17.6 HTTP 表 |
| 图谱 Nebula `demo_gkx_chain` | ✅ 禁止 `gkx_enterprise` 第二空间；as-built `entan` 已标明不是目标 |
| D12 | ✅ 本步只改编排仓文档；未改 `demo-ui-*` / `lumen-ui-*`；未改 `demo-algo-*` 代码 |
| 不灌数 / 不 APPLY DDL | ✅ |
| P0 灌数剥离 | ✅ 清单已落 §18；实现属步2 |
| 企业 Feign = entan-py | ✅ 禁止 innov-py |
| 综合叶 | ✅ 未建、未开工 |

### Cost（估算 · 非 console 实测）

计价代理：`budget-estimate.md` §1.2 Sonnet 4.5（$3 / $15 per MTok），data/doc 默认 in/out ≈ 85/15。`source: session_estimate`。

| 字段 | 值 |
|------|-----|
| actual_tokens | 280000 |
| model_used | grok-4.6 |
| actual_cost | 1.34 |
| cost_warn | green |

未超 $5 黄线。coordinator 收单时回填 registry。

### 步2 开工门

**PASS。** 文档已含：op_id I/O、边×终点全表、灌数剥离文件级清单、`diagram_id=ENT-GRAPH-TRIPLE`。

步2 打开条件（coordinator 核）：本文件 + `pipeline-to-nebula.md` 已 `origin/dev`。步2 只改 `demo-algo-ent-analysis`；不改图谱菜单 Vue、不改 Java、不开综合叶。

### 开放项

- `OPEN-ENT-GRAPH-VID`：as-built `entan`/64 vs 目标 `demo_gkx_chain`/80
- `OPEN-ENT-GRAPH-INVEST`：投资无表无边
- `OPEN-ENT-GRAPH-POLICY`：政策适用无源
- `OPEN-ENT-GRAPH-NAMEVID`：名称当 VID
- L6 链指须徐滕强拍板，默认关闭
- `pipeline-demo-mock.md` §4 仍写 `demo_entan`：步2 剥代码后再另单改该稿；**本文件对应 §18 已是剥离真源**
- 综合叶等本叶四步完

---

## CI/CD（本步）

- 分支：`dev`（编排仓 `gkx-orchestration`）
- commit：见 git log（本步提交后回填 hash）
- pipeline / K8s：文档仓无业务 rollout
- 验证：未跑灌数、未连 Nebula 写库

## 涉及文件

- `agent-delivery/data/data-design/storage/ENT/etl/pipeline-to-nebula.md`（整文件 §1–§20）
- `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/DEMO-ENT-GRAPH-TRIPLE-UI-L01.md`（本文件）
