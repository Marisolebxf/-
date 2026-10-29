# 政策分析（E7 专题）A–E · 长任务总控（无人值守）

> **日期**：2026-09-02  
> **授权**：`human:淮政玮`（本管线监管人；后续认领 **不必再问**）  
> **目标**：Demo 库可测的**科技专题政策分析**闭环：可复跑灌数闸门 → `lumen-algo-py` polan `/internal` → Java `gkxlumen-topic-policy` → `lumen-ui-topic` `/policy/*` → **段 E 已发布冒烟**  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md) v1.13  
> **对标**：产业链 [`DEMO-CHAIN-ABCD-长任务总控.md`](../产业链分析-CHAIN/DEMO-CHAIN-ABCD-长任务总控.md)  
> **存储真源**：[`storage/POLICY/01-data-flow.md`](../../data/data-design/storage/POLICY/01-data-flow.md)（`POLICY-STORAGE-FLOW` 已签）  
> **图谱窄管线**：[`POLICY-GRAPH-CHAIN-长任务总控.md`](./POLICY-GRAPH-CHAIN-长任务总控.md) **仍然有效且 B 已 done**。本文件是专题产品链，**不重做** S1–S4、**不重做** `demo_gkx_chain` 投影设计。  
> **执行 agent 按本文件已拍板项继续**，禁止把「等用户」当默认阻塞。

| 段 | 仓 | 分支 | 任务（骨架 ID，MCP 建单后施工） | 状态门 |
|----|-----|------|------|--------|
| A | `demo-algo-ent-analysis` | `origin/dev` | `DEMO-POLICY-A-RECLOSE-L01`（退出门；可选 `DEMO-POLICY-SEED-MOCK-L01`） | 不重做 S1–S4。退出门 = Demo 库可测 + 至少 1 条可挂图产业的政策样本。C **只认** RECLOSE ≥ integration |
| B | `lumen-algo-py` | `origin/dev` | `LUMEN-POLICY-PY-BOOT-L01` → SHARED → **HARNESS** → METRIC / GRAPH / RUNTIME / 分析 Job | A 联调闸门后；对照 `demo-algo-ent-analysis/polan` **迁入** `vendor/polan`（禁止 git merge）。**算子方法冻结**；专题 Job 只加 harness 包装（§0 #13）。同仓串行 |
| C | `lumen-svc-platform` | `origin/dev` | 骨架 `FACADE/JOB`；施工 **一 REST 路径一叶**（[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md)） | 新建 **`gkxlumen-topic-policy`**；Job 扩 `gkxlumen-topic-async-service`；禁止 Feign `demo-platform-entan-py` |
| D | `lumen-ui-topic` | `origin/dev` | 共享壳一叶 + **一实施权威故事一叶**（同上拆单） | 复刻 `demo-ui-topic` 五维；只调 Java；同仓串行。**禁止**改 `lumen-ui-science-*` |
| E | devops + qa | K8s `dev` | `LUMEN-POLICY-E-DEVOPS-L01` · `LUMEN-POLICY-E-QA-SMOKE-L01` | D 闸4 后；只认已发布前端 `http://10.50.69.111:30892`；金路径 §4 |

厚包：A [`LUMEN-POLICY-A-总派单.md`](./LUMEN-POLICY-A-总派单.md) · B [`LUMEN-POLICY-PY-B-总派单.md`](./LUMEN-POLICY-PY-B-总派单.md) · C [`LUMEN-POLICY-JAVA-C-总派单.md`](./LUMEN-POLICY-JAVA-C-总派单.md) · D [`LUMEN-POLICY-FE-D-总派单.md`](./LUMEN-POLICY-FE-D-总派单.md) · **[C/D 细叶拆单](./LUMEN-POLICY-CD-细叶拆单.md)** · E [`LUMEN-POLICY-E-总派单.md`](./LUMEN-POLICY-E-总派单.md)  
金路径：本文件 §4 · 缺陷包：[`long-task-e-defect-pack.md`](../../templates/long-task-e-defect-pack.md)  
复刻：[`fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)

> **与算法库联调台隔离**：`demo-ui-system-test` `/policy`、`/entan/mock` 等 **不是** 本管线段 D。Mock CRUD 留在联调台，禁止做成专题 C 路径。

---

## 0. 已拍板（落盘即生效 · 执行勿问）

| # | 议题 | 决定 |
|---|------|------|
| 1 | 轨道 | **专题正式链**。D12：`lumen-ui-topic` 只经 `gkxlumen-platform-gateway` 调 `gkxlumen-*`。禁止 lumen 调任何 `demo-*` 服务 |
| 2 | Java 查询门面 | **新建 `gkxlumen-topic-policy`**（api+biz）。对外 REST **`/topic/v1/policy/**`** |
| 3 | Java 异步 Job | **扩展 `gkxlumen-topic-async-service`**（政策分析 task_type）；Python **不自签** `result_snapshot_id` |
| 4 | 算法 | **`lumen-algo-py/vendor/polan`** · `/internal/policy/**`。Java 不直连 nGQL、不写算法。现网 polan **只对照、算子方法冻结**（§0 #13） |
| 5 | 中间检索 | 政策文档查询经 Java → polan `/internal`（或已有 ADS 读面）。**禁止**正式 Feign `demo-platform-entan-py` / `demo-svc-topic-py` |
| 6 | 数仓 | **lumen 项目当前数仓 = demo 数据源。** 数据面 ODS/DWD/ADS 一律 **`demo_gkxlumenx_*`**（与现网 polan / CHAIN 同一套）。禁止为「上 lumen」另接 `gkxlumenx_*` 数据面、禁止把 helm JDBC 改成正式前缀仓。Java 应用表（任务/快照）能落 demo 前缀则落 demo 前缀；不得借机新建正式数仓 |
| 7 | 图谱 | 一张 G = **`demo_gkx_chain`**。禁 `CREATE SPACE gkx_policy` 作目标态；禁写正式 `gkx_chain`。投影 B 叶 `POLICY-NEBULA-PROJECT-CHAIN-L01` 已 done，本管线 B 只迁代码+让 Java 走 `/internal` |
| 8 | 产业挂接 VID | **只用图上链码**（例 `chain:INB170101` 半导体与集成电路）。禁止把三方 ODS 树码（例 `INB1303`）或产业**名称**当 VID。标题兜底对图上链名已在 demo polan 落地，迁入时保留 |
| 9 | 产业锚点 | Q068：15 个产业集群；查询粒度 = 集群 + 可选 L0；无映射 `grain=empty`，禁止把 `CL-*` 当 `industry_id` 打 ADS |
| 10 | 对象流 | 三项分析**主路径 = 配置页内直选**：先选产业集群（产业 map 表），再选该 map 下 **L0 产业**（单次恰好 1 个）。对比篮产业 Tab **仅可选预填，不强制**。无政策文档 Tab。产业 XOR 技术领域。政策查询只核对语料，不入篮、不发起分析。**2026-09-02 `human:淮政玮` 人审修正**：不再要求从对比篮选 |
| 11 | 监管 | `supervised_by=human:淮政玮`，`claim_type=coordinator_dispatch`，`lock_hours=24` |
| 12 | 金路径 / CI | §4 五条 P0；CI 名 **`e2e:policy-gold`**（可后补；未绿前 E1 用手跑已发布 URL） |
| 13 | B 算子 + harness | **对照已有算子 demo，禁止改算子方法。** 真源：`demo-algo-ent-analysis/polan`（`eval/` `basic/` `graph/` `text/` `models/`）+ 算法库联调台已跑通的政策算子。迁入后公式/签名/返回语义保持原样。专题场景（时序 / 区域对比 / 深圳三维 / 单条焦点）在 **harness 层**按用量包装：小结果集同步直调；中等 `ThreadPool` 分片；大结果集走 `lumen_algo_worker` 多任务 claim + **子任务/子 agent** 分片聚合。大数据只允许 harness 做分片、限流、流式读、连接池；**禁止**为「跑得动」去改 `run()` / 打分函数 / 抽词函数。灌数批处理仍可调用原 `run()` 入口，与 demo 一致 |

---

## 1. 无人值守规则（违反才停）

1. **监管已授权**：`supervised_by=human:淮政玮`，`claim_type=coordinator_dispatch`。升 ready 后直接认领开工，不要等聊天确认。  
2. **已拍板不回问**：§0 十三项 + 调用链/废作（§2）。  
3. **QC / 甲方 🟡（QPOL-01～07）**：诚实降级（空值、ⓘ、PendingBadge、⚠️ 待甲方确认），**不**停工等纪要，**不**把口径改绿。  
4. **结构歧义**（新表/改主键/新 Tag·Edge/DROP SPACE）：该叶 `blocked` + 升级 **`human:李伟`**；产业码对照表另开，**不挡**已拍板的图上码挂接。同段其它叶继续。  
5. **缺数据**：不得写正式数仓；读空则可见空态 + 角标。段 A MOCK 只为撑起 Job 用例（标 mock + GAP），不算正式真源。lumen 代码连的就是 `demo_gkxlumenx_*`，不要问「正式仓 JDBC 配哪」。  
6. **不要问**选仓、选引擎、要不要做某 Bid 叶子、要不要等门 3。故事拆单 `POLICY-MOD-E7-*` 保持 `proposed`，**禁止** merge 后标 ready。本管线 **另建** `DEMO-POLICY-*` / `LUMEN-POLICY-*` 叶。  
7. git：lumen / orchestration / `demo-algo-ent-analysis` 推 `origin/dev`；禁止 force；commit `[agent:<role>]`。  
8. 每叶 handoff + `ponytail: full`（定义/文档叶 `N/A`）+ cost 四字段。`ready_to_sign→done` 可积压。  
9. **段 E**：禁止逐叶 QA；只认 K8s 已发布前端；QA 不改代码；**期望未发生必红**；红了先失败分类 C1–C6；C1 由 coordinator 派修（分诊助手无提交权）。C1 后点名 deploy 绿 = E0，随后 `e2e:policy-gold`（或手跑 §4）；CI 红才派 qa-agent 抄 trace。禁止等聊天「已经滚了」、禁止等黄敬洲领取。  
10. **同仓 Convoy**：`lumen-algo-py` / `lumen-svc-platform` / `lumen-ui-topic` **同时只派一张** coding 单。与 CHAIN/ENT/SVC 抢 `lumen-ui-topic` 时，本管线排队，不插队。

锁：`lock_hours=24`。lease 过期则同一监管人续领，不改设计。

---

## 2. 调用链与废作

### 2.0 数仓（执行勿问）

**现在 lumen 仓连的就是 demo 数据源**，不是另一套管线。

| 层 | 本管线 | 禁止 |
|----|--------|------|
| ODS / DWD / ADS | `demo_gkxlumenx_ods` / `_dwd` / `_ads` | `gkxlumenx_ods` 等正式前缀数据面 |
| 图 | `demo_gkx_chain` | 正式 `gkx_chain`；独立 `gkx_policy` |
| 三方源 | 只读对照，不直连当 ADS | 无闸门写 `gkx` |
| Java 任务表 | 跟现网 async：能 demo 前缀则 demo 前缀 | 为政策新建正式数仓 |

D12 禁的是 lumen **调 demo 服务**；**数仓共用 demo_gkxlumenx_*** 是现状，本管线保持。

### 2.1 目标调用链（实线）

```text
lumen-ui-topic /policy/* 、/policy-portal/*
        → gkxlumen-platform-gateway
        → Java gkxlumen-topic-policy  /topic/v1/policy/**
        →（分析 Job）gkxlumen-topic-async-service
        → Python lumen-algo-py  /internal/policy/**
        → 只读 ADS demo_gkxlumenx_ads.policy_*
        → 图  demo_gkx_chain（失败诚实兜底 ADS，source 不得假标 nebula）
```

Java 不写 nGQL、不扫 ODS 做算法。前端不直连 Python / Nebula。数仓见 §2.0（lumen 连 `demo_gkxlumenx_*`）。图即契约：C/D 施工须把 `POLICY-STORAGE-FLOW` 产品链从虚线改实线（`OPEN-POLICY-FLOW-01`）。

### 2.2 废作施工（不要派、不要当依赖）

| ID / 路径 | 原因 |
|-----------|------|
| `E-E7-POLICY-M1-L02` DoD「space `gkx_policy` 为目标态」 | 历史 as-built；投影已改一张 G |
| `E-E7-POLICY-M1-L03`～`L07` | 旧要素 M1 切法；能力吸收进本管线 B/C/D 细叶 |
| `POLICY-PROTO-L04`「无 Nebula 走 PG/SQLite」 | 允许读兜底，不允许当写入目标 |
| `sip-POLICY-MOD-E7-*` / `POLICY-MOD-E7-DG-G3` | 门 1 提案；未 merge、无门 3；不得当施工单、不得标 ready |
| 展示 `DS10-12-*` / `DS10-12-V1-HIFI-L01` | **另一系统**，本管线不接 |
| `demo-ui-system-test` 政策 Mock CRUD 当专题 API | 联调台专用 |
| Java Feign `demo-platform-entan-py` / `demo-svc-platform` | D12 |
| lumen 前端 `VITE_*` 直连 demo nginx / Python | D12 |
| `CREATE SPACE gkx_policy` / 写 `gkx_chain` / DROP `demo_gkx_chain` | 一张 G |
| 用 ODS `INB1303` 或中文名当图 VID | 挂不上 |
| 段 D：`FE-ENTRY` / `FE-WORKSPACE` / 只改 Hero 当完成 | 规约 §9.1 |
| 对比篮「政策文档 Tab」；查询「深度分析」直达 | DEC-E7 已废 |
| 给 lumen-* helm 另配正式 `gkxlumenx_*` 数据面「因为是 lumen 项目」 | 现网 lumen 数仓 = demo 源；§0 #6 |
| 专题 Job 一次 `load` 全表 4 万+ 政策再在算子里循环 | 大数据走 harness 分片多次调用已有入口（如 `focus_one`） |
| 给 lumen-* helm 另配正式 `gkxlumenx_*` 数据面「因为是 lumen 项目」 | 现网 lumen 数仓 = demo 源；§0 #6 |

---

## 3. 依赖（联调闸门，不等签收 `done`）

```text
[已完成，不重做]
  DATA-POLICY-STORAGE-S1～S4  done
  POLICY-NEBULA-PROJECT-CHAIN-L01  done（demo polan → demo_gkx_chain）
  POLICY-PACK / UX / METRIC-OPEN / PDR-G1-INGEST  done（定义门）

A RECLOSE ──可选 MOCK
  → B PY-BOOT（迁 polan，算子原样）→ SHARED
       → **HARNESS**（场景包装：线程池 / worker 子任务；不改算子）
       → METRIC / GRAPH / SEARCH-READ
       → RUNTIME → 分析 Job（时序 / 区域对比 / 深圳三维；只调 harness）
  → C 路径细叶（同仓串行；FACADE/JOB 仅骨架）
       SEARCH → GRAPH → METRICS → TASK-CREATE/GET/RESULT
  → D 内循环（规约 §9.1；lumen-ui-topic 一次一张）
       SHELL ← C SEARCH + 对比篮产业 Tab 已有（复用 ENT-COMPARE）
       POL-01c 查询 ← SHELL                         ← 金路径 #1
       POL-01/05 配置页集群→L0（篮可选预填）← SHELL ← 金路径 #2
       POL-01-SCOPE 人审修正（不强制篮）← POL-01    ← 金路径 #2 补叶
       WAITVIEW ← C TASK-GET + RESULT
       POL-02 时序 ← WAITVIEW + CREATE              ← 金路径 #3
       POL-03 区域对比 ← WAITVIEW                   ← 金路径 #4
       POL-04 深圳三维 ← WAITVIEW                   ← 金路径 #5
       POL-08 门户（P1，不挡 E）
       POL-06 任务浮层（复用 SystemTaskLayer，不复制队列）
       POL-07 报告 / POL-09 OPS（P1，不挡 E）
  → 闸4：SHELL + WAITVIEW + 金路径 #1～#5 故事叶 ≥ pending_test
  → E0（本轮 deploy）→ E1（§4）
```

**禁选下一张**：`FE-ENTRY` / `FE-WORKSPACE` / `SEARCH-SKIN` 当完成叶；旧 `E-E7-POLICY-M1-L0*`。

卡住只允许：真环境不通、正式库误写风险、李伟结构项、E 超 3 轮 / cost 硬闸。

---

## 4. 金路径（段 E1 · 只点 K8s dev 已发布前端）

已发布前端：`http://10.50.69.111:30892`。环境禁止 localhost。QA **不改代码**。

I2-12：切条件 **不**自动起任务；条件栏「开始分析」；同用户同条件只允许一条在跑；当天已成功直接打开结果；「重新分析」可强制重跑。

**期望未发生必红**。空态只有写进本行才算过。Job 未 `succeeded`（含 freeze failed）→ 红，不得以过程页报失败改判 PASS。

| # | 故事 ID | 已发布路由 | 期望（未发生=红） | 允许的空态 |
|---|---------|------------|-------------------|------------|
| 1 | `US-E7-POL-01c` | `/policy/search` | 智能检索或高级筛选能出政策卡；**无**「加入对比篮」「深度分析」 | 无命中可见空态，非 5xx |
| 2 | `US-E7-POL-01` + `US-E7-POL-05` | `/policy/overview`（区域对比 `/policy/analysis`、深圳 `/policy/recommendation` 同配置页） | 先选**集群**（产业 map）再选该 map 下 **L0 产业** 恰好 1 个；**不强制**对比篮。篮带入仅可选预填（可显示「来自对比篮」）。经 Java，不直连 Python | 未选集群/L0 或无映射时禁止空跑；**不得**把「去产业查询入篮」当唯一入口 |
| 3 | `US-E7-POL-02` + `US-E7-POL-06` | `/policy/overview` | 配置锚点（1 产业 XOR ≥1 技术领域）→「开始分析」→ 过程页 → **succeeded 后** wait_view 点查看结果；禁止自动跳结果 | **无。** Job failed ≠ 空态 |
| 4 | `US-E7-POL-03` | `/policy/analysis` | 同上闭环出区域对比矩阵/雷达（经 Java） | 无数则结果页可见空态+角标；**未 succeeded 仍红** |
| 5 | `US-E7-POL-04` | `/policy/recommendation` | 三维框架可提交评估任务并出不可变结果；一级权重合计 100% | QPOL-02 权重口径 ⚠️ 可带角标，但任务须跑通 |

P1 不挡闭环：门户 `/policy-portal/overview`（`US-E7-POL-08`）、报告 HTML→PDF（`US-E7-POL-07`）、维护 `/policy/maintenance`（`US-E7-POL-09`）。

E0 点名服务（发布未绿则 E1 不开）：`lumen-ui-topic` · `gkxlumen-topic-policy` · `gkxlumen-topic-async-service` · `lumen-algo-py`（polan worker/api）。**数仓 = demo 源** `demo_gkxlumenx_*`（lumen 现网如此，勿改正式前缀）。D12：前端不得打到 `demo-*` **服务**（数仓共用 demo 不违反 D12）。

---

## 5. 开工顺序（执行 agent 照此，不必问）

1. Coordinator **MCP 建单** A 退出门 `DEMO-POLICY-A-RECLOSE-L01`（及可选 MOCK），升 ready，认领，派 data/algorithm。  
2. A 达联调闸门 → 建并派 **B PY-BOOT**（算子原样迁入）→ SHARED → **HARNESS**（场景包装）→ 读面/图 → Runtime → Job（Job 只调 harness）。  
3. C **一 REST 路径一叶**；BOOT/FACADE 只骨架。SEARCH 路径闸门后可穿插 D SHELL。  
4. D 按 §3：SHELL → 金路径故事优先 → P1。查询页无 V1–V7、工作区无 W1–W3 → 同一叶 `needs-revision`。  
5. 闸4 → **重开 E0 → E1**。失败用缺陷包驱动修；C1 push 后等点名 deploy 绿 =E0。

本总控不替代各叶 DoD。第一张业务仓 commit 之前，对应 leaf 必须已在 registry 且已认领。

---

## 6. 开放项（不挡主链）

| ID | 项 | 处理 |
|----|----|------|
| QPOL-01～07 | 甲方口径仍 🟡 | UI 角标；不改绿 |
| OPEN-POLICY-GRAPH-01 | tech/talent 上图 | 本管线不上图 |
| OPEN-POLICY-DIM-01/02 · XDOM-01 | 维表缺口 | 诚实降级；补对象另单 |
| 两套 INB 对照表 | ODS 树 vs 图上树 | 本管线只用图上码；对照表另开 |
| 门 3 `POLICY-MOD-E7-DG-G3` | 未建 | 不挡本管线另建实施叶 |
| `e2e:policy-gold` | CI 后补 | 未绿前 E1 手跑已发布 URL |

授权句：**后续认领不必再问。**
