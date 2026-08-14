# 段 B · 产业链 Python（lumen-algo-py）总派单

> **日期**：2026-08-14  
> **派单人 / 监管**：`human:淮政玮`  
> **执行**：`algorithm-agent`  
> **仓**：`${GKX_ROOT}/repos/lumen-algo-py`（push **`origin/dev`**，禁止 `main`）  
> **Epic**：`E-CHAIN-PROTOTYPE` · Sprint `2026-W33`  
> **强度**：ponytail **full**  
> **本轮状态**：registry **backlog**（硬依赖段 A `DEMO-CHAIN-UI-SEED-ODS-L01` **done** 后才升 ready）  
> **薄条**：[`DEMO-CHAIN-PY-B-派单条.md`](./DEMO-CHAIN-PY-B-派单条.md)

段 C/D 见 [`DEMO-CHAIN-ABCD-长任务总控.md`](./DEMO-CHAIN-ABCD-长任务总控.md)。本文件只约束 Python；不要在本仓做 Java/前端。

---

## 0. 四段落点（已拍板）

| 段 | 仓 | 本轮 |
|---|---|---|
| A 存储 + MOCK | `demo-algo-science` + `demo_gkxlumenx_*` | 已建 `DEMO-CHAIN-UI-SEED-ODS-L01`（ready，未完工） |
| **B Python** | **`lumen-algo-py`** | **本文件** |
| C Java | `lumen-svc-platform` | 后拆；复用 `gkxlumen-topic-async-service` 做 Job Harness |
| D 前端 | `lumen-ui-topic` | 后拆；对齐已评审 `demo-ui-topic` |

废作施工：`CHAIN-ALGO-L01`、`demo-algo-science` `/v1/chain/**` 旧 13 GET、`demo-svc-platform` `gkx-innov` ChainController 1:1 透传、企业 `/topic/v1/search/meta/chains`（那是企业高筛字典）。

---

## 1. 架构裁决（冲突时执行 agent 不得自选）

1. **代码只写 `lumen-algo-py`**。禁止把 `demo-algo-science/chainan` 整包搬过来；可对照旧实现，按本仓 `lumen_algo_service` + `lumen_common` 结构新写。本仓 **不建 DWD/ADS 业务表**（表由段 A 在 Demo 库建）。
2. **联调库** = `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`（配置 `LUMEN_ALGO_MYSQL_*_DB`）。**禁止**无闸门写正式 `gkxlumenx_*`。缺 Demo 前缀直接拒绝（对齐 `assert_demo_*`）。
3. **产业查询走 MySQL 目录**（DWD `industry_chain` 等）。禁止为本页建 ES、禁止搬 `demo-svc-topic-py`。ES 仅 P1 资讯全文，不挡查询。
4. **功能对齐**已评审 `repos/demo-ui-topic/src/app/pages/industry-center/**`。冲突：该页 + 叶子五件套 > DESIGN-LANDING > 旧 13 GET / 旧 `CHAIN-IA.md`。
5. **八项 Bid 不合并**。七键各一 Graph；全景默认读 ADS `industry_chain_graph_snapshot` 秒开；改条件才 `chain:panorama:graph`（`DEC-CHAIN-PANORAMA-CONDITION-TASK-20260813` 修订 INDEX「全景不算 Job」）。
6. **Job 真源在 Java（段 C）**。Python 只做 Graph Runner：`Execute` + 回调 `ReportStage` / `Complete`。**禁止**自签 `result_snapshot_id`。**禁止**用本仓已有 `/gdf/tasks` + `lumen_analysis_task` 当七键/全景 Job 权威状态机（那是企业评估自管任务）。
7. 七键 Result **禁止**写入全景 `graph_snapshot`。介绍/历程走 **CMS**，不写 ADS narrative。
8. `M_CHAIN_MARKET_SIZE` 按 Q056 空值，禁止假市场。投融资禁止假值（QC07）。`chain_id` / `node_id` / `industry_id` = INB（Q053）。
9. 调用链：前端 → **Java** → Python **`/internal/*`**。本段可 curl Python 验收；禁止前端直连。图谱仅 **NebulaGraph**，禁止 Neo4j；Java 不直连 nGQL。
10. git：`origin/dev`；commit `[agent:algorithm-agent]`；禁止 force push。

---

## 2. 已评审 Demo → Python 能力

| Demo | 路由 / 键 | 本段交付 |
|---|---|---|
| `IndustrySearchPage` | `/industry-center/search` | SEARCH：`smart/industry/advanced`，记录对齐 `IndustrySearchRecord` |
| `IndustryOverviewPage` | 门户 | SYNC：ADS KPI；资讯可读 DWD `news_event`；介绍/历程不写 |
| `IndustryPanoramaPage` | `/industry-center/panorama` | SYNC 发布快照秒开；JOB-PANORAMA 改条件任务 |
| `IndustryDiagnosisPage` | cycle / key_link / bottleneck | 三键 Graph |
| `IndustryRegionalPage` | index / competitiveness | JOB-REGIONAL |
| `IndustryShenzhenPage` | comparison / development | JOB-SHENZHEN（发展依赖对比 Result） |
| `industryAnalysisShell` | wait_view | JOB-RUNTIME |

对象字段：`stableId`、`objectType`（industry / industry_chain）、`parentIndustryId`、`domain`、`aliases`、`tags`、`availability`。

---

## 3. 给段 C 的契约（B 先实现 Python 侧）

```text
lumen-ui-topic
  → lumen-svc-platform  /topic/v1/industry/** 与 /topic/v1/analysis-jobs
    → 只读 ADS
    → Feign /lumen-algo → lumen-algo-py /internal/v1/chain/**
```

| 逻辑 | Python（本段） | Java（段 C，后做） |
|---|---|---|
| 产业查询 | `GET/POST /internal/v1/chain/search` | `/topic/v1/industry/search` |
| 门户 / 发布快照 / 对象目录 | `/internal/v1/chain/sync/**` | 同步只读门面（建议新模块 `gkxlumen-topic-chain`） |
| 生成分析 | `POST /internal/v1/chain/jobs/execute`；回调 Stage/Complete | Create/互斥/Snapshot；复用 `gkxlumen-topic-async-service` |

路径落地以 OpenAPI 草稿为准（`CONTRACT-Java-Python-Analysis-Job-v0.md`）；前缀不得改成用户侧 `/v1/chain/{id}/cycle` 冒充 Job。

旧 `GET /v1/chain/**`：**不要**在 lumen-algo-py 复刻为产品面。

---

## 4. 任务清单与依赖

```text
A DEMO-CHAIN-UI-SEED-ODS-L01 (done)
  → SHARED
      → METRIC ─┐
      → GRAPH  ─┼→ SYNC
      → SEARCH  │
      → RUNTIME ─┬→ KEY-LINK（样板，先绿）
                 │     → BOTTLENECK / CYCLE / REGIONAL / SHENZHEN / REPORT
                 ├→ PANORAMA（还依赖 GRAPH + SYNC）
                 └→ NER-HOTSPOT（P1，仅 SHARED）
```

| ID | P | 一句话 | 依赖 | 点/难 |
|---|---|---|---|---|
| `DEMO-CHAIN-PY-SHARED-L01` | P0 | Demo 库闸门、DWD/ADS 只读、指标信封、`trace_id` | A | 5 / M |
| `DEMO-CHAIN-PY-METRIC-L01` | P0 | DWD→ADS v2 指标引擎；能算则算，不能则诚实空 | SHARED | 8 / L |
| `DEMO-CHAIN-PY-GRAPH-L01` | P0 | DWD rel → Nebula `demo_gkx_chain`；结构歧义升级李伟 | SHARED | 8 / L |
| `DEMO-CHAIN-PY-SEARCH-L01` | P0 | MySQL 产业查询，对齐 SearchPage | SHARED | 5 / M |
| `DEMO-CHAIN-PY-SYNC-L01` | P0 | 门户 KPI + 全景**已发布** snapshot/diff + Select 目录 | METRIC | 5 / M |
| `DEMO-CHAIN-PY-JOB-RUNTIME-L01` | P0 | Graph Runner Execute/Stage/Complete；不自签 snapshot | SHARED | 8 / L |
| `DEMO-CHAIN-PY-JOB-PANORAMA-L01` | P0 | `chain:panorama:graph`；成功则**发布**新 snapshot | RUNTIME+GRAPH+SYNC | 8 / L |
| `DEMO-CHAIN-PY-JOB-KEY-LINK-L01` | P0 | 样板键 `chain:diagnosis:key_link` | RUNTIME+METRIC | 13 / XL |
| `DEMO-CHAIN-PY-JOB-BOTTLENECK-L01` | P0 | `bottleneck`；GRAPH 待建则按 DESIGN-LANDING 补声明 | KEY-LINK | 8 / L |
| `DEMO-CHAIN-PY-JOB-CYCLE-L01` | P0 | `cycle`，对象 industry | KEY-LINK | 8 / L |
| `DEMO-CHAIN-PY-JOB-REGIONAL-L01` | P0 | `regional_index` + `regional_competitiveness` | KEY-LINK | 8 / L |
| `DEMO-CHAIN-PY-JOB-SHENZHEN-L01` | P0 | comparison → development（硬依赖对比 Result） | KEY-LINK | 13 / XL |
| `DEMO-CHAIN-PY-REPORT-L01` | P1 | 只读 Result → MinIO；禁止报告重跑分析 | KEY-LINK | 5 / M |
| `DEMO-CHAIN-PY-NER-HOTSPOT-L01` | P1 | 抽取落 DWD；热点不作为查询引擎 | SHARED | 5 / M |

建议包路径：`lumen_common/algorithms/chain/` · `lumen_algo_service/views/chain.py`（名称可在 SHARED 首单定，后续不得再拆第二套）。

---

## 5. 必读（禁止用压缩摘要代替精读）

| 序 | 路径 |
|---:|---|
| 1 | 本文件 + 派单条 |
| 2 | `lumen-algo-py/README.md`（不建业务表、dev 分支、`/lumen-algo`） |
| 3 | `storage/CHAIN/README.md` · `01-data-flow.md` · `stores/mysql/dwd-chain.md` · `stores/mysql/ads.md` · `stores/nebula/graph-chain.md` |
| 4 | DWD v5 · ADS v2 真源 md |
| 5 | `INDEX-DESIGN-LANDING-7-analysis.md` · Runtime · `CONTRACT-Java-Python-Analysis-Job-v0.md` · ISOMORPH |
| 6 | `DEC-CHAIN-PANORAMA-CONDITION-TASK-20260813.md` |
| 7 | Demo：`industrySearchModel.ts` / `industryAnalysisRegistry.ts` / 各 Page |
| 8 | `cfg_metric-CHAIN-seed.yaml` · `data-lineage-policy.md` |
| 9 | `architecture-baseline.md` |

Headroom：大 JSON/日志可 compress；上表全文禁止用摘要代替。

---

## 6. 各单 DoD 要点（registry 条目为验收真源）

- **SHARED**：配置只指向 `demo_*` 时可跑；指向正式库名拒绝；pytest 闸门；指标信封字段（metric_id + honesty/gap）有模块。
- **METRIC**：ADS v2 十表中指标相关表有写入路径；Q056 市场规模空；QC07 投融资不造假；`--self-check` 或 pytest 绿。
- **GRAPH**：Demo space 可投影；失败不假成功；无 Neo4j。
- **SEARCH**：三种 mode + 高筛字段能过滤 Demo 目录；响应可喂 `IndustrySearchRecord`；无 ES 依赖。
- **SYNC**：发布快照可读；与 Job Result 分表。
- **RUNTIME**：Execute 一次跑完 Graph；Stage 回调可测（mock Java）；Complete 只交 `result_payload`。
- **各 Job**：`task_type=chain:{module}:{key}`；`succeeded` 语义留给 Java wait_view；LLM 不改分数/布尔。
- **PANORAMA**：默认无 task 秒开走 SYNC；脏条件才建 `chain:panorama:graph`。
- 每单 handoff：`agent-handoffs/产业链分析-CHAIN/{id}.md`，含 `ponytail: full`、cost 四字段、架构合规。

---

## 7. `/goal` 模板（升 ready 后派单用）

```text
/goal
你是经验丰富、遵循业界最佳实践的算法工程师（algorithm-agent）。
任务：{TASK_ID} {标题}
仓库：${GKX_ROOT}/repos/lumen-algo-py（push origin/dev）
监管：human:淮政玮
强度：ponytail full（默认）。禁止用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律。
上下文：headroom 推荐。USM/TRACE/Wireframe/Design/Runtime/v5/v2 禁止 compress 代替精读。

必读：agent-handoffs/产业链分析-CHAIN/DEMO-CHAIN-PY-B-总派单.md
铁律：算法只 Python；前端→Java→/internal；Nebula 禁止 Neo4j；只写 demo_* 库；产业查询 MySQL 不走 ES；
对齐 demo-ui-topic industry-center；Job 不自签 result_snapshot_id；不用 /gdf/tasks 当 CHAIN Job 真源。
DoD：见 registry 该 ID。
完工写 handoff agent-handoffs/产业链分析-CHAIN/{TASK_ID}.md
```

认领：`claimed_by=agent:algorithm-agent` · `supervised_by=human:淮政玮` · `claim_type=pull`

---

## 8. 明确不做

CMS 介绍/历程；OPS 写侧；Java 门面与 Snapshot 库（段 C）；lumen 页（段 D）；为查询上 ES；在 `demo-algo-science` 继续加产业链产品 API。

---

## 9. 开放项（不挡建单）

| 项 | Owner |
|---|---|
| Nebula Tag/Edge 与 v5 命名终裁 | 李伟（GRAPH 单升级） |
| 部分键 GRAPH.md / Schema 仍待建 | 按 DESIGN-LANDING 在 Job 单内补声明 |
| PDR `CHAIN-MOD-PDR-G1` blocked | QC 🟡 诚实降级，不挡 Demo 联调 |
| 段 C 模块名 `gkxlumen-topic-chain` | 架构会签；B 不依赖模块名字符串 |

**派单完成条件**：本说明 + 派单条入仓 + 14 条 registry backlog。  
**本协调会话不写 Python 业务代码。**
