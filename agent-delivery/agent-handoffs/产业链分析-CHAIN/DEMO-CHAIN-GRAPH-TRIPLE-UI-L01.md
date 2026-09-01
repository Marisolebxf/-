# DEMO-CHAIN-GRAPH-TRIPLE-UI-L01 · 产业链图谱三元组闭环

> 叶内四步：步1 data-agent → 步2 algorithm-agent → 步3 api-agent → 步4 frontend-agent。本文按步追加，不覆盖他人段落。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent`（本步 1/4；步 2/3/4 由 coordinator 切换） |
| supervised_by | `human:李伟`（全程不准改） |
| claim_type | `coordinator_dispatch` |
| 说明 | 厚包 `COORD-GRAPH-TRIPLE-UI-DISPATCH-20260831.md` §0 §3 §7.0。`origin/dev` 拉取后 MCP `task-get` **仍未找到**该 ID（GRAPH-TRIPLE 查询 0 命中）；**未改** `task-registry.yaml`。请 coordinator 补建单后补认领 / cost 回填。 |

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
