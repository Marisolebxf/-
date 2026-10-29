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
| C | `lumen-svc-platform` | 骨架 `FACADE/JOB`；施工真源 **一 REST 路径一叶**（[`DEMO-CHAIN-CD-细叶拆单.md`](./DEMO-CHAIN-CD-细叶拆单.md)） | 2026-08-18 改切法；厚包不删；对应 B 读面 / Runtime 满足联调闸门 |
| D | `lumen-ui-topic` | 骨架 `ENTRY/WORKSPACE/SKIN/LAYOUT`；施工真源 **一实施权威故事一叶**（同上拆单） | 五维 + V1–V7 钉在故事叶；废止 `US-CHAIN-TOPIC-02~17`；不等人审截图 |
| E | devops + qa | `LUMEN-CHAIN-E-DEVOPS-L01` · `LUMEN-CHAIN-E-QA-SMOKE-L01` · **`LUMEN-CHAIN-E-CI-PLAYWRIGHT-L01`** | E0/E1 已 `ready_to_sign`（不标 done）。金路径默认走 GitLab `e2e:chain-gold`。前端 http://10.50.69.111:30892 |

厚包：A 派单说明 · [B 总派单](./DEMO-CHAIN-PY-B-总派单.md) · [C 总派单](./DEMO-CHAIN-JAVA-C-总派单.md) · [D 总派单](./DEMO-CHAIN-FE-D-总派单.md) · **[C/D 细叶拆单](./DEMO-CHAIN-CD-细叶拆单.md)** · [E 总派单](./DEMO-CHAIN-E-总派单.md)

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
9. **段 E**：禁止逐叶 QA；只认 K8s 已发布前端；QA 不改代码；**期望未发生必红**；红了先失败分类 C1–C6；C1 由 coordinator 派修（分诊助手无提交权）。C1 后 **点名自动 deploy**：Python api+worker、Java topic-chain + async-service；deploy 绿 = E0，随后 **`e2e:chain-gold` 自动复测**（规约 §11.5.2）；CI 红才派 qa-agent 抄 trace；**禁止**等聊天「已经滚了」、**禁止**等黄敬洲领取；innov/entan/`helm:deploy` 不搭车。

锁：长任务 `lock_hours=24`。lease 过期则同一监管人重新认领继续，不要改设计。

---

## 2. 依赖（联调闸门升 ready，不等签收 `done`）

施工 DAG 以 [`DEMO-CHAIN-CD-细叶拆单.md`](./DEMO-CHAIN-CD-细叶拆单.md) §3 为准。下面是 coordinator **段 D loop**（规约 §9.1）。旧 ENTRY→WORKSPACE→SKIN→E **作废**。

```text
A SEED → A JOB-MOCK
  → B SHARED → METRIC / GRAPH / SEARCH / RUNTIME / NER(P1)
       METRIC → SYNC
       RUNTIME+METRIC → KEY-LINK → 其余 Job / REPORT(P1)
       RUNTIME+GRAPH+SYNC → PANORAMA
  → C 路径细叶（同仓串行；FACADE/JOB 仅骨架）
  → D 内循环（规约 §9.1；lumen-ui-topic 一次一张）
       SHELL ← C SEARCH + CATALOG
       TOPIC-01 ← SHELL + SEARCH          ← 金路径 #1
       OV-01/06 ← SHELL + OVERVIEW/KPI    ← 金路径 #2
       WAITVIEW ← C TASK-GET + RESULT
       PANORAMA-01 ← SHELL + SNAPSHOT     ← 金路径 #3
       DIAG-03/04 ← WAITVIEW + CREATE     ← 金路径 #4
       SZ-03 ← WAITVIEW                   ← 金路径 #5
       其余 P0 故事叶（OV/PANORAMA/DIAG/REG/SZ/TOPIC-18/19）
       P1 TOPIC-20 / OPS-SHELL（不挡 E）
  → 闸4：SHELL+WAITVIEW+全部 P0 故事叶 ≥ pending_test
  → 重开 E0（本轮 deploy）→ E1（金路径 §4）
```

**禁选下一张**：`FE-ENTRY` / `FE-WORKSPACE` / `SEARCH-SKIN` / `SEARCH-LAYOUT` / `FE-REPLICA-FIX` / 旧 `CHAIN-FE-L03`。  
**旧 E0/E1 已 `ready_to_sign` ≠ 本轮 D 完成**，P0 故事叶齐后必须重开。

废作施工（不要派、不要当依赖）：`CHAIN-ALGO-L01` · `CHAIN-API-L01` 旧 13 透传 · `CHAIN-FE-L03` 旧 CP1–CP6 · `US-CHAIN-TOPIC-02~17`。

---

## 3. 开工顺序（执行 agent 照此，不必问）

1. 认领并做完 **A SEED**；MOCK 撑不住 Job 时立刻做 **`DEMO-CHAIN-UI-SEED-JOB-MOCK-L01`**（2026-08-14 已开）。  
2. A done → 认领 **B SHARED**，再按 B 总派单并行许可范围内做 SEARCH/METRIC/GRAPH/RUNTIME（同仓 Convoy 则串行，先 SHARED）。  
3. C 按 **一 REST 路径一叶**（拆单 §1）同仓串行；**不要**再派 FACADE/JOB 当完成叶。SEARCH 路径叶闸门后即可穿插 D SHELL（规约 §9.1 闸1）。  
4. C 按 **一 REST 路径一叶**（拆单 §1）同仓串行。D **禁止**再派 ENTRY/WORKSPACE/SKIN/LAYOUT/REPLICA-FIX 当完成叶。  
5. D 按规约 **§9.1**：先对应 C 路径叶闸门 → SHELL → 金路径故事优先 → 其余 P0 → P1。查询页无 V1–V7、工作区无 W1–W3 → 同一叶 `needs-revision`，不开补单当过。  
6. 闸4 触发后 **重开 E0 → E1**（§4）。现网 E0/E1 `ready_to_sign` 只证明旧厚包接线，不证明故事复刻。失败用缺陷包驱动 coordinator 派修；C1 push 后等 **点名 deploy job 绿** =E0，再等同轮 **`e2e:chain-gold`**。

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
