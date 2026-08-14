# 产业链 A–E · 长任务总控（无人值守）

> **日期**：2026-08-14  
> **授权**：`human:淮政玮`（本管线监管人；后续认领 **不必再问**）  
> **目标**：Demo 库可测的产业链专题闭环：灌数 → Python → Java → `lumen-ui-topic` → **段 E 已发布冒烟**  
> **模式**：长任务。方法已升格为 [`长任务执行规约.md`](../../长任务执行规约.md)；**本文件只保留本管线拍板项与 DAG**。  
> 每段少单、厚包、依赖按联调闸门解锁；执行 agent **按本文件已拍板项继续**，禁止把「等用户」当默认阻塞。

| 段 | 仓 | 任务 | 状态门 |
|---|---|---|---|
| A | `demo-algo-science` | `DEMO-CHAIN-UI-SEED-ODS-L01` · **`DEMO-CHAIN-UI-SEED-JOB-MOCK-L01`**（LLM MOCK 补区域/周期） | L01 联调闸门已过；MOCK 补单 2026-08-14 开 |
| B | `lumen-algo-py` | `DEMO-CHAIN-PY-*`（14） | A 满足 **联调闸门**（handoff + `integration`/`pending_test`）后 SHARED 升 ready |
| C | `lumen-svc-platform` | `LUMEN-CHAIN-JAVA-FACADE-L01` · `LUMEN-CHAIN-JAVA-JOB-L01` | 对应 B 读面 / Runtime+样板键 满足联调闸门 |
| D | `lumen-ui-topic` | `LUMEN-CHAIN-FE-ENTRY-L01` · `LUMEN-CHAIN-FE-WORKSPACE-L01` · **`LUMEN-CHAIN-FE-SEARCH-SKIN-L01`**（视觉补单） | 对应 C 满足联调闸门；皮肤单在 ENTRY 联调闸门后 |
| E | devops + qa | `LUMEN-CHAIN-E-DEVOPS-L01` · `LUMEN-CHAIN-E-QA-SMOKE-L01` | **2026-08-14 无人值守完成**：E0/E1 均 `ready_to_sign`（不标 done）。前端 http://192.168.88.50:30892；五条金路径 ALL_PASS |

厚包：A 派单说明 · [B 总派单](./DEMO-CHAIN-PY-B-总派单.md) · [C 总派单](./DEMO-CHAIN-JAVA-C-总派单.md) · [D 总派单](./DEMO-CHAIN-FE-D-总派单.md) · [E 总派单](./DEMO-CHAIN-E-总派单.md)

---

## 1. 无人值守规则（违反才停）

1. **监管已授权**：`supervised_by=human:淮政玮`，`claim_type=coordinator_dispatch`。升 ready 后直接认领开工，不要等聊天确认。  
2. **已拍板不回问**：查询走 MySQL；功能对齐已评审 `demo-ui-topic`；B=`lumen-algo-py`；C=`lumen-svc-platform`；D=`lumen-ui-topic`；Job 真源 Java；Python 不自签 `result_snapshot_id`。  
3. **QC / PDR / 甲方 🟡**：诚实降级（空值、角标、Q056），**不**停工等纪要。  
4. **结构歧义**（新表/改主键/新 ES）：`blocked` + 升级 `human:李伟`，**同段其它不依赖该点的工作继续**。  
5. **缺数据**：不得写正式库、不得用旧 `chain_*` 冒充。**禁止造假市场/投融资（Q056/QC07）**。2026-08-14 淮政玮拍板：段 A **LLM MOCK 必须撑起后续 Job 用例**（区域四力底分、周期主序列等）；标 mock + GAP，不算正式真源。缺这类 MOCK 导致 Job `BASE_SCORE_MISSING` ≠ 允许的诚实空态。  
6. **不要问用户选仓/选引擎/要不要做某 Bid 叶子**。八项不合并；OPS 维护只复刻 Demo 壳。  
7. git：lumen 仓只推 `origin/dev`；demo-algo-science 按 A 包。禁止 force。commit `[agent:<role>]`。  
8. 每单仍写 handoff + `ponytail: full` + cost 四字段。coordinator/AV 按状态机推进，不把「等淮政玮看一眼」插进 A→E 主链（签收 `ready_to_sign→done` 除外，可积压）。  
9. **段 E**：禁止逐叶 QA；只认 K8s 已发布前端；QA 不改代码；**期望未发生必红**；红了先失败分类 C1–C6；C1 由 coordinator 派修（分诊助手无提交权）。C1 后 `lumen-algo-py` **api+worker 自动 deploy**，deploy 绿 = E0，coordinator 自动只复测（规约 §11.5.2）；**禁止**等聊天「已经滚了」；innov/entan 不搭车。

锁：长任务 `lock_hours=24`。lease 过期则同一监管人重新认领继续，不要改设计。

---

## 2. 依赖（联调闸门升 ready，不等签收 `done`）

```text
A SEED → A JOB-MOCK（区域 scorecard + 周期序列）
  → B SHARED → METRIC / GRAPH / SEARCH / RUNTIME / NER(P1)
       METRIC → SYNC
       RUNTIME+METRIC → KEY-LINK → 其余 Job / REPORT(P1)
       RUNTIME+GRAPH+SYNC → PANORAMA
  → C FACADE（等 SEARCH + SYNC）
  → C JOB（等 RUNTIME + KEY-LINK）
  → D ENTRY（等 C FACADE）
  → D WORKSPACE（等 C JOB + D ENTRY）
  → D SEARCH-SKIN（Hero/页底）→ D SEARCH-LAYOUT（推荐卡横排）
  → E0 发布门 → E1 金路径冒烟（失败 → 缺陷包修单 → 点名 deploy 绿=E0 → 只复测）
```

旧单废作施工（不要派、不要当依赖）：`CHAIN-ALGO-L01` · `CHAIN-API-L01` 旧 13 透传 · `CHAIN-FE-L03` 旧 CP1–CP6。

---

## 3. 开工顺序（执行 agent 照此，不必问）

1. 认领并做完 **A SEED**；MOCK 撑不住 Job 时立刻做 **`DEMO-CHAIN-UI-SEED-JOB-MOCK-L01`**（2026-08-14 已开）。  
2. A done → 认领 **B SHARED**，再按 B 总派单并行许可范围内做 SEARCH/METRIC/GRAPH/RUNTIME（同仓 Convoy 则串行，先 SHARED）。  
3. SEARCH+SYNC done → **C FACADE**。KEY-LINK done → **C JOB**。  
4. C FACADE 联调闸门 → **D ENTRY**。C JOB + D ENTRY 联调闸门 → **D WORKSPACE**。ENTRY 联调闸门后可并行 **`LUMEN-CHAIN-FE-SEARCH-SKIN-L01`**（视觉补单）。  
5. D WORKSPACE 联调闸门 → **`LUMEN-CHAIN-E-DEVOPS-L01`** → **`LUMEN-CHAIN-E-QA-SMOKE-L01`**（§4）。失败用缺陷包驱动 coordinator 派修；C1 push 后等 **api+worker deploy job 绿**（=E0，不必问人），再只复测失败故事。SEARCH-SKIN push 后若要已发布页见新皮肤，再跑一次 E0（不重开功能冒烟，除非皮肤修动了金路径 DOM）。

本总控不替代各段 DoD。卡住只允许：真环境不通、正式库误写风险、李伟结构项、E 超 3 轮 / cost 硬闸。

---

## 4. 段 E · 金路径（只点 K8s dev 已发布前端）

规约：[`长任务执行规约.md`](../../长任务执行规约.md) §11。QA **不改代码**。环境禁止 localhost。缺陷包：[`long-task-e-defect-pack.md`](../../templates/long-task-e-defect-pack.md)。

实施权威故事以拆分后的 USM 为准（不要再用已迁移的 `US-CHAIN-TOPIC-02~17` 当施工）。

**期望未发生必红**（2026-08-14 拍板，规约 §11.3）：下表「期望」没发生 → FAIL。空态仅当该行写明。#4 Job 未到 succeeded（含 `freeze` failed）→ 红，不得以过程页报失败改判 PASS。  
**失败分类**（规约 §11.4）：#4 `freeze` failed = **C1**（不是 C3）。C1 才派修；C2 只重开 E0；C3 记缺口；C5 李伟。

| # | 故事 ID | 路由 | 期望（未发生=红） | 允许的空态 |
|---|---------|------|-------------------|------------|
| 1 | `US-CHAIN-TOPIC-01` | `/industry-center/search` | 三模式之一能出记录；入篮同类型锁 | 三模式均无命中时可诚实空（可见空态，非 5xx） |
| 2 | `US-CHAIN-OV-01` / `US-CHAIN-OV-06` | `/industry-center/overview` | 经 Java 拉总览；不造假 KPI | 无数则可见空态 |
| 3 | `US-CHAIN-PANORAMA-01` | `/industry-center/panorama` | 默认 **无 task 秒开**发布快照；改条件才出现「开始分析」 | 快照节点可空，但须是已发布 snapshot 而非卡过程页 |
| 4 | `US-CHAIN-DIAG-03` → `US-CHAIN-DIAG-04` | `/industry-center/diagnosis`（key_link） | 配置→生成→过程→**succeeded 后 wait_view 点查看结果**；禁止自动跳结果 | **无。** Job failed / 未 succeeded ≠ 空态 |
| 5 | `US-CHAIN-SZ-03` 负例 | `/industry-center/shenzhen` | **无有效对比结果时禁止提交/空跑发展分析** | 本条是负例，拦截成功即过 |

P1 不挡闭环：区域两键、报告 `US-CHAIN-TOPIC-20`、OPS 写侧、其余诊断键。

E0 点名服务（发布未绿则 E1 不开）：`lumen-ui-topic` · `lumen-svc-platform`（chain 门面 + async-service）· `lumen-algo-py`。库：`demo_gkxlumenx_*`。D12：前端不得打到 `demo-*` 服务。
