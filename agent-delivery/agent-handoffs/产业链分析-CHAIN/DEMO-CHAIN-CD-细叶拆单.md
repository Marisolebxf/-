# 产业链 C/D 细叶拆单（一接口 / 一故事）

> **日期**：2026-08-18  
> **拍板**：聊天「C 段一接口一叶；D 段按页面功能或用户故事拆叶」  
> **规约**：`长任务执行规约.md` v1.11 §5  
> **总控**：[`DEMO-CHAIN-ABCD-长任务总控.md`](./DEMO-CHAIN-ABCD-长任务总控.md)  
> **监管**：`human:淮政玮` · `claim_type=coordinator_dispatch` · lock 24h  
> **状态**：细叶入库 **`backlog`**，解锁仍走联调闸门 + confirm；**禁止**本包直接标 `ready`

旧厚包 **不删、不重做**：`LUMEN-CHAIN-JAVA-FACADE-L01` / `JAVA-JOB-L01` / `FE-ENTRY-L01` / `FE-WORKSPACE-L01` / `FE-SEARCH-SKIN-L01` / `FE-SEARCH-LAYOUT-L01` 仅作 **骨架 fan-in**。新施工真源 = 本表细叶。同仓仍 **同时只派一张** coding 单。段 E 仍在全部 **P0 故事叶** 满足联调闸门后一次冒烟，禁止逐叶 QA。

废作施工（勿派、勿当依赖）：`CHAIN-API-L01` 旧 13 GET · `CHAIN-FE-L03` CP1–CP6 · `US-CHAIN-TOPIC-02~17`（已迁出）。

---

## 0. 切法

| 段 | 一叶 = | 不算一叶 |
|----|--------|----------|
| **C** | 一条对外 REST **路径**（同一 path 的 GET+POST 可同叶） | 一个 `analysisType` 键、一次 Feign、一次网关改写 |
| **D** | 一条 **实施权威** USM 故事；外加共享壳 2 叶 | 废止父故事；只改 Hero/页底；ENTRY 整包 |

每张 D 叶 `/goal` 必贴手册 §9.0c + `fe-replica-visual-dod.md`。handoff 无 V1–V7 → `needs-revision`。

---

## 1. 段 C · 一 REST 路径一叶

仓：`lumen-svc-platform` · `origin/dev` · `api-agent` · Epic `E-CHAIN-PROTOTYPE`  
网关前缀：`/chain/topic/v1/industry/**`（门面）· `/topicAsync/topic/v1/analysis/**`（Job）

骨架 fan-in：`LUMEN-CHAIN-JAVA-FACADE-L01`（模块/网关）· `LUMEN-CHAIN-JAVA-JOB-L01`（async 托管）。细叶 DoD = **该路径契约对齐 Demo 字段 + 联调 curl + 不造假**；已有代码可收口，禁止另起第二套 Controller。

### 1.1 查询门面

| ID | 方法 · 路径 | 依赖（联调闸门） | DoD 要点 |
|----|-------------|------------------|----------|
| `LUMEN-CHAIN-JAVA-API-SEARCH-L01` | GET+POST `/topic/v1/industry/search` | `DEMO-CHAIN-PY-SEARCH-L01` | 三 mode；`IndustrySearchRecord`；无数诚实空；无 ES |
| `LUMEN-CHAIN-JAVA-API-OVERVIEW-L01` | GET `/topic/v1/industry/overview` | `DEMO-CHAIN-PY-SYNC-L01` | 总览壳；不造假 KPI |
| `LUMEN-CHAIN-JAVA-API-OVERVIEW-KPI-L01` | GET `/topic/v1/industry/overview/kpi` | `DEMO-CHAIN-PY-METRIC-L01` | 8 件套走 metrics catalog；Q056 空 |
| `LUMEN-CHAIN-JAVA-API-OVERVIEW-NEWS-L01` | GET `/topic/v1/industry/overview/news` | `DEMO-CHAIN-PY-SYNC-L01` | 资讯列表头；介绍/历程不冒充 |
| `LUMEN-CHAIN-JAVA-API-SNAPSHOT-L01` | GET `/topic/v1/industry/panorama/snapshot` | `DEMO-CHAIN-PY-SYNC-L01` | 与 Job Result **分 API**；默认秒开 |
| `LUMEN-CHAIN-JAVA-API-CATALOG-L01` | GET `/topic/v1/industry/catalog` | `DEMO-CHAIN-PY-SYNC-L01` | 对象 Select；产业/链身份 |

Health 不单独成叶，随 SEARCH 自检。

### 1.2 Job 门面

| ID | 方法 · 路径 | 依赖 | DoD 要点 |
|----|-------------|------|----------|
| `LUMEN-CHAIN-JAVA-API-TASK-CREATE-L01` | POST `/topic/v1/analysis/tasks` | `DEMO-CHAIN-PY-JOB-RUNTIME-L01` + `JAVA-JOB-L01` | 冻 input snapshot；Feign Execute；白名单 `chain:*`；Java 签发 `result_snapshot_id` |
| `LUMEN-CHAIN-JAVA-API-TASK-GET-L01` | GET `/topic/v1/analysis/tasks/{id}` | CREATE | 过程态；禁止自动当已查看 |
| `LUMEN-CHAIN-JAVA-API-TASK-RESULT-L01` | GET `/topic/v1/analysis/tasks/{id}/result` | CREATE + `PY-JOB-KEY-LINK-L01` | **不**改 `viewed`；wait_view 由前端点 |
| `LUMEN-CHAIN-JAVA-API-TASK-EVENTS-L01` | GET `/topic/v1/analysis/tasks/{id}/events` | CREATE | 过程节点；不另起表 |

`analysisType`（key_link / cycle / …）是 CREATE 的请求字段，**不**再按键拆 Java 叶。

---

## 2. 段 D · 一实施权威故事一叶

仓：`lumen-ui-topic` · `origin/dev` · `frontend-agent`  
复刻源：`repos/demo-ui-topic/src/app/pages/industry-center/**`  
只调 Java。骨架 fan-in：`FE-ENTRY-L01` / `FE-WORKSPACE-L01`。

### 2.1 共享壳（先于故事叶）

| ID | 一句话 | 依赖 |
|----|--------|------|
| `LUMEN-CHAIN-FE-SHELL-L01` | 侧栏「产业链分析」整组 + 路由 + `menu:chain:*` + 页根 `#D8E7FC` | `JAVA-API-SEARCH` + `JAVA-API-CATALOG`（闸门） |
| `LUMEN-CHAIN-FE-WAITVIEW-L01` | 过程壳 + succeeded 后必须点「查看分析结果」；对齐 Demo `industryAnalysisShell` | `JAVA-API-TASK-GET` + `JAVA-API-TASK-RESULT` |

### 2.2 查询 / 总览

| ID | 故事 | 路由 | 依赖 |
|----|------|------|------|
| `LUMEN-CHAIN-FE-US-TOPIC-01` | `US-CHAIN-TOPIC-01` 发现并保存兼容对象 | `/industry-center/search` | SHELL + `JAVA-API-SEARCH` |
| `LUMEN-CHAIN-FE-US-OV-01` | `US-CHAIN-OV-01` 切换 L0 产业 | `/industry-center/overview` | SHELL + OVERVIEW |
| `LUMEN-CHAIN-FE-US-OV-02` | `US-CHAIN-OV-02` L1 子链结构 | 同上 | OV-01 |
| `LUMEN-CHAIN-FE-US-OV-03` | `US-CHAIN-OV-03` 简介与企业列表 | 同上 | OV-01 |
| `LUMEN-CHAIN-FE-US-OV-05` | `US-CHAIN-OV-05` 产业资讯 | 同上 | `JAVA-API-OVERVIEW-NEWS` |
| `LUMEN-CHAIN-FE-US-OV-06` | `US-CHAIN-OV-06` 整链概况 | 同上 | `JAVA-API-OVERVIEW-KPI` |
| `LUMEN-CHAIN-FE-US-OV-07` | `US-CHAIN-OV-07` 空间布局 | 同上 | OV-01 |
| `LUMEN-CHAIN-FE-US-OV-08` | `US-CHAIN-OV-08` 发展阶段 | 同上 | OV-06 |
| `LUMEN-CHAIN-FE-US-OV-09` | `US-CHAIN-OV-09` 深圳产业现状 | 同上 | OV-01 |
| `LUMEN-CHAIN-FE-US-OV-10` | `US-CHAIN-OV-10` 加入分析对象集合 | 同上 | TOPIC-01 |

`US-CHAIN-OV-04` **废止**，不建叶。

### 2.3 全景

| ID | 故事 | 依赖 |
|----|------|------|
| `LUMEN-CHAIN-FE-US-PANORAMA-01` | `US-CHAIN-PANORAMA-01` 确认对象；默认秒开无「开始分析」 | SHELL + `JAVA-API-SNAPSHOT` |
| `LUMEN-CHAIN-FE-US-PANORAMA-02` | `US-CHAIN-PANORAMA-02` 浏览完整结构 | PANORAMA-01 |
| `LUMEN-CHAIN-FE-US-PANORAMA-03` | `US-CHAIN-PANORAMA-03` 下钻节点详情 | PANORAMA-02 |
| `LUMEN-CHAIN-FE-US-PANORAMA-04` | `US-CHAIN-PANORAMA-04` 双快照演进（无证据则诚实 Pending，不伪差异） | PANORAMA-02 |

改条件 Job 走 WAITVIEW + `JAVA-API-TASK-CREATE`（`chain:panorama:graph`）。

### 2.4 诊断（页 `/industry-center/diagnosis`）

| ID | 故事 |
|----|------|
| `LUMEN-CHAIN-FE-US-DIAG-01` | `US-CHAIN-DIAG-01` 提交周期 |
| `LUMEN-CHAIN-FE-US-DIAG-02` | `US-CHAIN-DIAG-02` 阅读周期结果 |
| `LUMEN-CHAIN-FE-US-DIAG-03` | `US-CHAIN-DIAG-03` 提交关键环节 |
| `LUMEN-CHAIN-FE-US-DIAG-04` | `US-CHAIN-DIAG-04` 关键环节结果 |
| `LUMEN-CHAIN-FE-US-DIAG-05` | `US-CHAIN-DIAG-05` 提交瓶颈 |
| `LUMEN-CHAIN-FE-US-DIAG-06` | `US-CHAIN-DIAG-06` 瓶颈结果 |
| `LUMEN-CHAIN-FE-US-DIAG-07` | `US-CHAIN-DIAG-07` 恢复诊断记录 |

配置叶依赖 WAITVIEW + CREATE；结果叶依赖对应配置叶 + TASK-RESULT。

### 2.5 区域 / 深圳

| ID | 故事 | 路由 |
|----|------|------|
| `LUMEN-CHAIN-FE-US-REG-01`～`05` | `US-CHAIN-REG-01`～`05` | `/industry-center/regional` |
| `LUMEN-CHAIN-FE-US-SZ-01`～`05` | `US-CHAIN-SZ-01`～`05` | `/industry-center/shenzhen` |

SZ-03 负例：无有效对比结果禁止空跑发展（金路径 #5）。

### 2.6 记录 / 报告 / OPS

| ID | 故事 | 优先级 |
|----|------|--------|
| `LUMEN-CHAIN-FE-US-TOPIC-18` | `US-CHAIN-TOPIC-18` 跟踪/撤回排队任务 | P0 |
| `LUMEN-CHAIN-FE-US-TOPIC-19` | `US-CHAIN-TOPIC-19` 分析记录与复制配置 | P0 |
| `LUMEN-CHAIN-FE-US-TOPIC-20` | `US-CHAIN-TOPIC-20` 报告阅读 | **P1**（不挡 E） |
| `LUMEN-CHAIN-FE-US-OPS-SHELL` | OPS 维护 **壳**（`US-CHAIN-OPS-*` 写侧不做） | **P1** |

---

## 3. DAG（联调闸门，不等 `done`）

coordinator 过夜循环见规约 **§9.1**（五闸）。本表只给依赖箭头。

```text
B SEARCH/SYNC/METRIC/RUNTIME
  → C API 细叶（同仓串行：SEARCH → OVERVIEW* → SNAPSHOT → CATALOG
       → TASK-CREATE → GET → RESULT → EVENTS）
  → D SHELL
  → D TOPIC-01（金路径 #1）→ D OV-*（OV 内按表箭头；OV-01/06 = 金路径 #2）
  → D WAITVIEW
  → D PANORAMA-01（金路径 #3）…04
  → D DIAG-01…07 / REG-01…05 / SZ-01…05（同仓排队；配置→结果；DIAG-03/04=#4 · SZ-03=#5）
  → D TOPIC-18/19
  → 闸4：SHELL+WAITVIEW+全部 P0 D 叶 ≥ pending_test
  → 重开 E0 → E1（金路径仍总控 §4 五条；禁止逐叶 QA；旧 E ready_to_sign 不算）
```

---

## 4. `/goal` 头

```text
/goal
仓库：按本叶 repo · origin/dev
监管：human:淮政玮 · coordinator_dispatch · lock 24h
强度：ponytail full
必读：DEMO-CHAIN-CD-细叶拆单.md · 本叶故事/路径 USM · Design.md §14
禁止：直连 Python；另起更简 UI；手写就绪度改绿；派废止父故事；把厚包 ENTRY/FACADE 当本叶 DoD。
```

D 叶追加：

```text
复刻：语义+布局。必读 templates/fe-replica-visual-dod.md。
禁止：两套互斥 display 叠同一节点；只改页底/Hero 宣称完成。
```
