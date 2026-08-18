# 产业服务链（SVC）A–E · 长任务总控（已授权）

> **日期**：2026-08-17  
> **授权**：`human:侯佳伟`（本管线监管人；后续认领 **不必再问**）  
> **确认**：2026-08-17 聊天「全部同意」§0 八项  
> **目标**：Demo 库可测的产业服务链闭环：灌数 → 中间层/算法 Python → Java → `lumen-ui-topic` → **段 E 已发布冒烟**  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)  
> **对标**：产业链 [`DEMO-CHAIN-ABCD-长任务总控.md`](../产业链分析-CHAIN/DEMO-CHAIN-ABCD-长任务总控.md)  
> **存储前置**：`storage/SVC` S1–S4 文档已本地交；**段 A 退出门 = `DEMO-SVC-A-RECLOSE-L01`**。旧 `DEMO-SVC-SEED-*` 不得单独给 C 开闸。细表 draft；Q-SVC-010 诚实降级不伪闭合

| 段 | 仓 | 任务 | 状态门 |
|----|-----|------|--------|
| A | `demo-algo-ent-analysis`（+ 可选 `demo-algo-science`） | `DEMO-SVC-SEED-ODS-L01` · `DEMO-SVC-SEED-MOCK-L01` · **退出门 `DEMO-SVC-A-RECLOSE-L01`** | Demo 库可测：建表/种子/MOCK + `pipeline-demo-mock` 可复跑；禁正式库 |
| B | `lumen-topic-py` + `lumen-algo-py` | `DEMO-SVC-PY-MIDDLE-BOOT-L01` · `DEMO-SVC-PY-MIDDLE-SEARCH-L01` · `DEMO-SVC-PY-MIDDLE-TASK-L01` · `DEMO-SVC-PY-SVCAN-BOOT-L01` | A 联调闸门后；同仓 Convoy 串行 |
| C | `lumen-svc-platform` | 骨架 `FACADE/JOB`（**新建 gkxlumen-topic-svc** / 扩 async-service）；施工 **一 REST 路径一叶**（[`DEMO-SVC-CD-细叶拆单.md`](./DEMO-SVC-CD-细叶拆单.md)） | 2026-08-18 改切法；厚包不删 |
| D | `lumen-ui-topic` | 骨架 ENTRY/WORKSPACE/视觉补单 **废作铺齐**；施工 **一 USM 故事一叶**（同上） | 五维 + V1–V7 钉在故事叶；只调 Java；同仓串行 |
| E | devops + qa + CI | `LUMEN-SVC-E-DEVOPS-L01` · `LUMEN-SVC-E-QA-SMOKE-L01` | 只认已发布前端；金路径 §4 |

厚包：[A](./DEMO-SVC-A-总派单.md) · [B](./DEMO-SVC-PY-B-总派单.md) · [C](./DEMO-SVC-JAVA-C-总派单.md) · [D](./DEMO-SVC-FE-D-总派单.md) · **[C/D 细叶拆单](./DEMO-SVC-CD-细叶拆单.md)** · [E](./DEMO-SVC-E-总派单.md)

---

## 0. 已确认拍板（2026-08-17 · human:侯佳伟）

| # | 议题 | 决定 |
|---|------|------|
| 1 | Java 查询门面 | **新建 `gkxlumen-topic-svc`**（api+biz） |
| 2 | Java 异步 Job | **扩展 `gkxlumen-topic-async-service`** |
| 3 | 对外 REST | `/topic/v1/service/**` + `/topic/v1/service-portal/**` → `gkxlumen-topic-svc` |
| 4 | 中间层 | **`lumen-topic-py`** · `/internal/gkx-svc/**`（禁正式 Feign demo-svc-topic-py） |
| 5 | 算法 | **`lumen-algo-py`** · `svcan/`；Java 不直连 |
| 6 | 段 A | 主 `demo-algo-ent-analysis`；只写 `demo_gkxlumenx_*` |
| 7 | 监管 | `supervised_by=human:侯佳伟` |
| 8 | 金路径 | §4 占位 5 条；CI 暂拟 `e2e:svc-gold`（可后补） |

---

## 1. 无人值守规则（违反才停）

1. **监管已授权**：`supervised_by=human:侯佳伟`，`claim_type=coordinator_dispatch`，`lock_hours=24`。升 ready 后直接认领，不要等聊天确认。  
2. **已拍板不回问**：§0 八项 + 调用链/库/废作（§2）。  
3. **QC / 甲方 🟡 / Q-SVC-010**：诚实降级（空值、角标、待核验），**不**停工等纪要。  
4. **结构歧义**：`blocked` + 升级 `human:李伟`；同段其它叶继续。  
5. **缺数据**：不得写正式 `gkxlumenx_*`；读空则空态。  
6. git：lumen / orchestration / demo-algo-ent-analysis → `origin/dev`；禁止 force；commit `[agent:<role>]`。  
7. 每叶 handoff + `ponytail: full`（定义/文档 leaf 可 lite）+ cost 四字段。签收可积压。  
8. **段 E**：禁止逐叶 QA；只认 K8s 已发布前端；QA 不改代码；期望未发生必红；失败分类后 C1 派修。

---

## 2. 已拍板（执行勿问）

1. 调用链：`前端 → Java(gkxlumen-topic-svc) → lumen-topic-py /internal/gkx-svc/** →（按需）lumen-algo-py/svcan → ADS/Nebula`  
2. Java 不写算法、不直连 nGQL、不 Feign 算法仓；Job 真源在 async-service。  
3. 库：只写 `demo_gkxlumenx_*`；结构真源 `storage/SVC/stores/*`。  
4. 废作：旧透传门面、Java→algo 直连、第二套机构主表、L01 当建表真源、正式 Feign demo-svc-topic-py。  

---

## 3. 依赖（联调闸门，不等签收 done）

施工 DAG 以 [`DEMO-SVC-CD-细叶拆单.md`](./DEMO-SVC-CD-细叶拆单.md) §3 为准。段 D loop = 规约 §9.1。旧 ENTRY→WORKSPACE→E **作废**。

```text
A SEED → A MOCK → **A RECLOSE（退出门，C 只认这一叶）**
  → B MIDDLE-BOOT → MIDDLE-SEARCH → MIDDLE-TASK
       + SVCAN-BOOT（可与 MIDDLE 并行开仓，同仓仍串行）
  → C 路径细叶（已有路径收口 → 缺口路径；FACADE/JOB 仅骨架）
  → D 内循环（与 CHAIN 抢 lumen-ui-topic，默认 CHAIN 先）
       SHELL ← C SEARCH-ORGS
       PT-01 ← SHELL + PORTAL-OVERVIEW     ← 金路径 #1
       ORG-07 ← SHELL + SEARCH-ORGS        ← 金路径 #2（V1–V7 必过）
       WAITVIEW ← C TASK-GET + RESULT
       ORG-01/02 ← WAITVIEW + CREATE       ← 金路径 #3
       ECO-01 ← WAITVIEW + ECO-GRAPH       ← 金路径 #4
       REC-02 ← WAITVIEW + REC-LIST        ← 金路径 #5
       其余 P0（PT-02…06 / ORG-03…08 / ECO-02…06 / REC-01/03/04）
  → 闸4：SHELL+WAITVIEW+全部 P0 故事叶 ≥ pending_test
  → 重开 E0 → E1（金路径必须真实 US-SVC-*，见 §4）
```

**禁选下一张**：`FE-ENTRY` / `FE-WORKSPACE` / `ENTRY-VISUAL-C1` / `WORKSPACE-VISUAL-C1` / `SEARCH-REPLICA-C2`。  
**现网 E1 `ready_to_sign` ≠ 本轮 D 完成**（当时期望是占位「能出记录或诚实空」）。

---

## 4. 金路径（E1 · 真实故事 ID · 2026-08-18）

> 旧占位「能出记录或诚实空」作废。重开 E1 必须按下表；未发生期望必红。

| # | 故事 ID | 已发布路由（拟定） | 期望（未发生=红） | 允许空态 |
|---|---------|-------------------|-------------------|----------|
| 1 | `US-SVC-PT-01` | `/service-portal/overview` | 经 Java 拉全球概况；不造假 KPI | 无数可见空态 |
| 2 | `US-SVC-ORG-07` | `/service-center/search` | Workbench 三段可走；能出记录 | 三模式均无命中时可诚实空（可见空态，非 5xx） |
| 3 | `US-SVC-ORG-02` | 机构分析工作区 | 配置→生成→过程→succeeded 后 wait_view 点查看结果 | **无。** Job failed / 未 succeeded ≠ 空态 |
| 4 | `US-SVC-ECO-01` | 生态图谱 | 经 Java 出图或可见空；禁止轻量表格冒充图谱 | 无数可见空态 |
| 5 | `US-SVC-REC-02` | 招引名单 | 名单可走通或诚实拦截 | 按故事写明的拦截/空名单 |

E0 点名：`lumen-ui-topic` · `gkxlumen-topic-svc` · `gkxlumen-topic-async-service` · `lumen-topic-py` · `lumen-algo-py`。库：`demo_gkxlumenx_*`。D12：前端不得打 `demo-*` 服务。

**已发布前端外网基址（E1）**：http://111.198.38.90:50892/ （内网 NodePort `192.168.88.50:30892` 对本机可能不可达，以本外网为准）。

---

## 5. 授权

> **授权**：`human:侯佳伟`  
> **日期**：2026-08-17  
> **授权句**：后续认领 **不必再问**。

---

## 6. 变更记录

| 日期 | 说明 |
|------|------|
| 2026-08-17 | 初稿草案 |
| 2026-08-17 | 侯佳伟确认 §0 全部同意；升已授权；建叶 + 厚包 |
| 2026-08-17 | E0 ready_to_sign；E1 blocked(C2 网络)；FE 视觉不符原型 → 增 `LUMEN-SVC-FE-ENTRY-VISUAL-C1` / `LUMEN-SVC-FE-WORKSPACE-VISUAL-C1`，先修 ENTRY |
| 2026-08-17 | **人令**：正式 FE 须按 `demo-ui-topic` 已评审原型复刻（语义+布局+卡片内部）；禁止功能壳/轻量表格宣称完成；V1–V7 不过不收 |
| 2026-08-17 | FE 视觉 C1：ENTRY+WORKSPACE → integration；修 SearchHub 皮肤选择器 + SPA 路由 404（`6d413fa`）。E1 仍 blocked(C2)。**长任务未结束** |
| 2026-08-17 | E1 外网基址改为 http://111.198.38.90:50892/ ；查询未完整复刻 → 开 `LUMEN-SVC-FE-SEARCH-REPLICA-C2`；E1 解阻重测 |
| 2026-08-17 | SEARCH-REPLICA-C2 → integration（Workbench+Recent+结果卡密度+?org=；`5213cff`）；外网待部署后再验 |
| 2026-08-17 | E1 外网：SPA 绿、`/api/svc/**` **404** → 开 `LUMEN-SVC-E-DEVOPS-GATEWAY-SVC-C1`（Nacos/gateway 路由未生效） |
| 2026-08-17 | 澄清：网关已通；根因 search-py 未挂 `/internal/gkx-svc` → `85a8fd9` + play `deploy:search-py` 22467；外网 health/overview **code=0**；E1 解阻复测 |
| 2026-08-17 | **外网复测**：`/api/svc` 已通（405/剥前缀）；health body=`detail Not Found` → 根因转 **search-py 未挂 gkx-svc**；`lumen-topic-py` `85a8fd9` 同进程挂载，等 image/deploy |
| 2026-08-17 | **E1 联调通过**：五条金路径绿（SPA+#1/#2 `/svc` code=0+#3/#5 壳+#4 async 诚实拦截）；`LUMEN-SVC-E-QA-SMOKE-L01` → `ready_to_sign` |
| 2026-08-18 | **切法变更**：C 一 REST 路径一叶、D 一 USM 故事一叶；见 `DEMO-SVC-CD-细叶拆单.md`；旧厚包仅骨架 |
| 2026-08-18 | **D loop**：规约 §9.1；总控 §3 废 ENTRY→E；§4 金路径改为真实 `US-SVC-*`；旧 E1 不算本轮完成 |
| 2026-08-18 | **段 A 重跑**：`DEMO-SVC-A-RECLOSE-L01` 为退出门；旧 SEED-* → `needs-revision`；C 不得在 RECLOSE 前开闸 |
