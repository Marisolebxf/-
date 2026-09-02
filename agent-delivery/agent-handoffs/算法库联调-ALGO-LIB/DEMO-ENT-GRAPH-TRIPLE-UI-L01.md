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
| 图 diff | 新增目标态：灌数零图谱 → A NER 企业点 → B `cooperate` / `invest` / `parent_sub`（投资源 = DWD `enterprise_invest`）→ C 产业/技术/人才/政策/科研/服务 hang（一企可多产业；他域只 FETCH）；space 目标 `demo_gkx_chain`；禁止灌数调用 `entity.run` / `load_nebula_safe` / yiji persist |
| 会签态 | 存储拓扑 `01-data-flow.md` 仍为 `approved`；本图为步1 **DEMO** 口径稿 |

---

## 数据设计（步1 · agent:data-agent · 2026-09-01）

**步1 按任务 DoD 收口为 DEMO 链。** Python = `demo-algo-ent-analysis`（进程 `demo-platform-entan-py`）；Java = `demo-svc-platform`。正式 `lumen-topic-py` / `lumen-algo-py` **不在本叶**。实现对照 `pipeline-to-nebula.md` 文首「审核定稿」+ §17–§18。

### 范围与实现（对照 SRS 108 / 109）

| 项 | 企业实体识别构建 | 企业实体关系抽取 |
|---|---|---|
| seq | **108** | **109** |
| metric_id | `M_ENT_GRAPH_108_1` | `M_ENT_GRAPH_109_1` |
| 本步落点 | 档 **A** `ENT_NER_ORG`：企业点 + 属性 NER | 档 **B** 合作/投资/归属；档 **C** 跨域六类 |
| 原文要点 | 工商/新闻/财报/招聘；名称/类型/行业/地理 + 营收/员工/高管/融资/市值/产品/技术 | 合作、投资、归属、产业所属、技术应用、人才关系、政策适用、科研合作、服务提供 |
| 本波诚实 | 属性不上图；融资额/市值/员工总数/班子缺列 → `empty_field` | **投资上图**（`enterprise_invest`，两端须在 `enterprise_base`）；股东 ODS 本波不画；政策适用无企业→政策边 → 挂不上（行保留）；无稳定 ID 不上图；禁止名称猜 VID |

档 **D** = 只读 `GET /v1/entan/graph`，不写库。Space = **`demo_gkx_chain`**（禁止 `gkx_enterprise` / 继续把 `demo_entan` 当目标）。as-built space 仍是 `entan` + `FIXED_STRING(64)`，见 `OPEN-ENT-GRAPH-VID`。

真源（只写编排仓，未改业务代码）：

`agent-delivery/data/data-design/storage/ENT/etl/pipeline-to-nebula.md` §1–§20（§1–§9 as-built，§10–§20 与政策同构）。

### 关系 × op_id × I/O 摘要

| op_id | 档 | HTTP | 输入要点 | 输出要点 | 本波 |
|---|---|---|---|---|---|
| `ENT_NER_ORG` | A | `POST /v1/entan/graph/ner` → `/internal/entan/graph/ner` | `scope=one\|batch`；`org_id` 或 filter；`mode=rule\|llm`；`dry_run` | `written_nodes`（`ent:`）；`skipped` 四码；`source`/`model_version`/`calc_batch_id` | 企业点上图；属性只进 `entity_recognition` |
| `ENT_RE_COOP` | B | `POST /v1/entan/graph/intra` | 同上 + 白名单 `[cooperate]` | `written_edges` cooperate；对端无 ID → `no_stable_id` | 两端 `ent:` |
| `ENT_RE_INVEST` | B | 同上 | 白名单含 `invest`；源 DWD `enterprise_invest`（`org_id`→`inv_org_id`） | 两端 `ent:` | **上图**；对端不在主表 → `no_stable_id` |
| `ENT_RE_BELONG` | B | 同上 | 白名单含 `parent_sub` | 母→子 | 两端 `ent:` |
| `ENT_RE_INDUSTRY` | C | `POST /v1/entan/graph/hang` | 必须带 `op_id` 或白名单；`dest_types` | hang 前 `FETCH` `chain:`/`segment:`；**一企多行各挂一条** | 禁止 `ind:{名}`；禁止「一企一节点」 |
| `ENT_RE_TECH` | C | 同上 | 白名单含 `produces` | 已有技术点才写 | 无专题库 ID → 不上图 |
| `ENT_RE_TALENT` | C | 同上 | `talent_coop` | 稳定人才 ID | 名称 → `no_stable_id` |
| `ENT_RE_POLICY` | C | 同上 | 政策适用 | 默认 skipped | **不上图** `OPEN-ENT-GRAPH-POLICY` |
| `ENT_RE_RESEARCH` | C | 同上 | `research_coop` | `FETCH` `inst:` | 名称键废除 |
| `ENT_RE_SERVICE` | C | 同上 | `service_provide` | `FETCH` `inst:` | 同上 |
| `ENT_GRAPH_BROWSE` | D | `GET /v1/entan/graph` | 只读 | 不写 ADS/Nebula | 现网 `/v1/graph/*` 可并存只读 |

加性（非需规最低集）：`ENT_RE_SUPPLY` / `supply`。禁止用供应链顶替投资。

公共：`dry_run` 不写 ADS/Nebula；同 `calc_batch_id`+主键可重跑覆盖；LLM 只在 `mode=llm`，无 Key 回退规则且 `llm_fallback=true`。`skipped.reason` ∈ `empty_field` / `no_stable_id` / `not_in_wave` / `vid_too_long`。需规边×终点全表见 §17.3，**无静默删行**。

Java（步3 才编码）：抄政策 `31582b9e`；网关在 `/entan/**` 之前插 graph 路由 → `gkx-innov` → Feign **`demo-platform-entan-py:8000`** `/internal/entan/graph*`；禁止 innov-py；禁止 catch-all 直连 Python 写图。lumen 不打 demo（D12），正式链另叶。

### 灌数剥离清单（文件 / 函数级）

步2 必须从灌数路径摘掉（checklist）。路径在 `demo-algo-ent-analysis`：灌数要摘图；`/internal/entan/graph*` 也在本仓实现。

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
| 图 `/internal` 落点 | ✅ 本叶 Demo：`demo-algo-ent-analysis` / `demo-platform-entan-py`；正式 lumen 链不在本叶 |
| 综合叶 | ✅ 未建、未开工 |

### Cost（估算 · 非 console 实测）

计价代理：`budget-estimate.md` §1.2 Sonnet 4.5（$3 / $15 per MTok），data/doc 默认 in/out ≈ 85/15。`source: session_estimate`。

| 字段 | 值 |
|------|-----|
| actual_tokens | 360000 |
| model_used | grok-4.6 |
| actual_cost | 1.73 |
| cost_warn | green |

未超 $5 黄线。coordinator 收单时回填 registry。

### 步2 开工门

**步1 文档齐（对照任务 DoD / 厚包 §0.5：demo 链）。** 步2 只改 `demo-algo-ent-analysis`：出 `/v1` + `/internal/entan/graph*`，并从灌数路径摘 B/B+/M。不改图谱菜单 Vue、不改 Java、不开综合叶、不改 `lumen-*`。步3 闸门 = demo `/internal/entan/graph*` 已齐才能写 `demo-svc-platform` Feign。`claimed_by` 切 `agent:algorithm-agent` 后再开步2。

### 开放项

- `OPEN-ENT-GRAPH-VID`：as-built `entan`/64 vs 目标 `demo_gkx_chain`/80
- `OPEN-ENT-GRAPH-INVEST`：as-built 无 `invest` Edge；目标增量补 Edge + 吃 DWD `enterprise_invest`（**不是**「无投资表」）
- `OPEN-ENT-GRAPH-SHAREHOLDER`：股东仅 ODS，本波不画
- `OPEN-ENT-GRAPH-POLICY`：政策适用无源
- `OPEN-ENT-GRAPH-NAMEVID`：名称当 VID
- L6 链指须徐滕强拍板，默认关闭
- 正式 lumen 图谱链（`lumen-ui-*` → `gkxlumen-*` → `lumen-topic-py` / `lumen-algo-py`）**另叶**，本叶不建
- `pipeline-demo-mock.md` §4 仍写 `demo_entan`：剥代码后再另单改该稿；**本文件对应 §18 已是剥离真源**
- 综合叶等本叶四步完

---

## CI/CD（本步）

- 分支：`dev`（编排仓 `gkx-orchestration`）
- commit：`a269c583` `docs(ent): GRAPH-TRIPLE 步1 按六条审核+demo链收口 [agent:data-agent]`
- pipeline / K8s：文档仓无业务 rollout
- 验证：未跑灌数、未连 Nebula 写库、未建 Python 服务

## 涉及文件

- `agent-delivery/data/data-design/storage/ENT/etl/pipeline-to-nebula.md`（整文件 §1–§20）
- `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/DEMO-ENT-GRAPH-TRIPLE-UI-L01.md`（本文件）

---

## 算法实现（步2 · agent:algorithm-agent · 2026-09-01）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| ponytail | `full` |
| diagram_id | `ENT-GRAPH-TRIPLE`（沿用步1，本步不改图） |

**范围**：只改 `demo-algo-ent-analysis`。不改 Vue / Java / lumen-*。不开综合叶。

### 实现

| 项 | 落点 |
|---|---|
| 灌数剥离 | `scripts/run_all.py` `build_steps` 删除 B / B+ / M；删除 `load_nebula_safe` / `init_membership_safe` 函数体。`POST /internal/run-pipeline` 经 `run_all.run` 不再建图 |
| A/B/C 核 | `entan/graph/ops.py`：`ENT_NER_ORG` / intra 四 op / hang 六 op；space=`demo_gkx_chain`；VID=`ent:{org_id}` 超长 `vid_too_long`（禁止 MD5 截断） |
| 投资 | `facts.iter_invest` + `fetch_tables` 读 DWD `enterprise_invest`（`org_id`→`inv_org_id`）；两端须在 `enterprise_base` |
| HTTP | `api/entan_graph_routes.py` 成对 `/v1` + `/internal/entan/graph{,/ner,/intra,/hang,/ops/{op_id}}`；`main.py` include |
| 加性 | `ENT_RE_SUPPLY` 须显式白名单，不顶替投资 |
| C hang | 必须 `op_id` 或白名单；产业只写 `industry_belong`（不双写 `located_in`）；他域只 FETCH；政策 `OPEN-ENT-GRAPH-POLICY`；技术无 DWD 稳定 ID 表 → `no_stable_id` 不上图；禁止名称猜 VID |
| invest 边类型 | 写入路径 **不** `CREATE EDGE`。事先 DDL：`scripts/nebula_ddl_invest.ngql`（只 `USE demo_gkx_chain` + `CREATE EDGE IF NOT EXISTS invest`）。未 APPLY 则投资只记 ADS、不上图 |
| 读图 D | `GET /v1/entan/graph` + `/internal/entan/graph`，优先 `USE demo_gkx_chain`，失败回退 ADS |

### 灌数剥离证据（grep）

对 `scripts/run_all.py`、`api/main.py`、`entan/llm_ods/`、`entan/basic/` 检索 `entity.run` / `load_nebula_safe` / `init_membership_safe` / `yiji_run(apply=True` / `nebula_loader.run`：**无命中**。`entity.py` / `yiji_sim.persist` / `nebula_loader` 仍保留作图谱菜单核，不进 `build_steps`。`llm_ods/demo_graph.py` 仍是独立 `seed_demo_graph` 脚本，不是 `run-pipeline`。

### 口头收口（监管人徐滕强 2026-09-01）

1–6、8 已过。7 技术无稳定 ID → `no_stable_id`：**行**。9 现网 APPLY `invest` DDL：本机无 graphd 外网，**先不执行**；脚本仍在仓内。

### 验收

- 单测 `tests/test_entan_graph_ops.py`：parse 拒空过滤 / 仅 `year`（enterprise_base 无年字段，不得当全表扫描门）/ 空白名单；vid 80 不截断；`iter_invest` 缺 `inv_org_id` / 对端不在主表不上图；`build_steps` 无 B/B+/M。本机 `.venv` 无 pytest，用 `python -c` 跑通
- 未对现网 Python 进程做 `dry_run` curl（本步未起服务、未改 K8s）。步3 网关插完再经 Java 打 `/internal/entan/graph*`
- 算法仓 commit：`ce86666`（`origin/dev`）

### 架构合规

| 铁律 | 本步 |
|---|---|
| 算法只在 Python | ✅ `/internal/entan/graph*` |
| 调用链 | ✅ 只出 Python；Java 步3 |
| Nebula `demo_gkx_chain` | ✅ 拒绝 `entan`/`demo_entan`；invest 边须事先 DDL，写入不改 schema；不 `DROP SPACE` / 不灌数 `ensure_schema` |
| D12 | ✅ 未改 lumen-*；未把 Feign 写成 innov-py |
| 灌数零图谱 | ✅ |
| 综合叶 | ✅ 未开 |

### Cost（估算 · 非 console 实测）

| 字段 | 值 |
|------|-----|
| actual_tokens | 180000 |
| model_used | grok-4.6 |
| actual_cost | 0.86 |
| cost_warn | green |

### 步3 开工门

`/v1` + `/internal/entan/graph*` 已在算法仓代码齐。步3 只改 `demo-svc-platform`：抄政策 `31582b9e`，网关在 `/entan/**` 之前插 graph → Feign `http://demo-platform-entan-py:8000` `/internal/entan/graph*`。

---

## Java 门面（步3 · agent:api-agent · 2026-09-01）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:徐滕强` |
| ponytail | `full` |
| diagram_id | `ENT-GRAPH-TRIPLE`（本步不改图） |

**范围**：只改 `demo-svc-platform`。不改 Vue / lumen-* / Python。不开综合叶。业务路径对齐政策，实现不必逐文件相同。

### 实现

| 项 | 落点 |
|---|---|
| 抄样板 | 政策 `31582b9e` + 产服 `gkx-svc-graph`（同仓 `/entan/**` 前插法） |
| Java 门面 | `gkx-innov/.../entan/EntanGraph{Controller,Service,AlgoClient,Properties}` |
| 对外路径 | `GET/POST /v1/entan/graph*` 与 `/internal/entan/graph*` 成对 |
| Feign | `name=entan-algo` → `${gkx.innov.entan.algo-base-url}` → **只** `/internal/entan/graph*` |
| K8s 基址 | `INNOV_ENTAN_ALGO_BASE_URL=http://demo-platform-entan-py:8000`；禁止 innov-py |
| 网关 | `gkx-entan-graph` `order: -10`，Path=`/entan/v1/entan/graph*` + `/entan/internal/entan/graph*`，插在 catch-all `/entan/**` **之前**；**不配** `StripPrefix`（与政策/产服一致，全局过滤器已剥 `/entan`，再剥会 404） |
| 透传边界 | body/query 原样；不做 NLP / nGQL / 边名改写；上游挂了返回 `{code:1,data:null}` |

### 验收

- 单测 `EntanGraphServiceTest`：Feign 抛错时 `code=1`、`data=null`。本机 `mvn test` 未跑通：nexus 无 `gkx-common-bom:5.12.0`
- 本机未对现网 gateway 做 curl（未部署）。步4 UI 须打 `/entan/v1/entan/graph*`，禁止直连 Python 写图
- 算法仓步2已推 `ce86666`。本步 Java `7394467`（rebase 后以 `origin/dev` HEAD 为准）

### 架构合规

| 铁律 | 本步 |
|---|---|
| 调用链 前端→Java→Python `/internal/*` | ✅ |
| Feign 禁止 innov-py | ✅ `demo-platform-entan-py:8000` |
| 网关禁止 catch-all 直连写图 | ✅ `gkx-entan-graph` 在 `/entan/**` 前 |
| D12 / 综合叶 | ✅ 未改 lumen-*；未开 COMP 叶 |
