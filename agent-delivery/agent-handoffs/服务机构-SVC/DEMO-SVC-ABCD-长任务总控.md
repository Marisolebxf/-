# 产业服务链（SVC）A–E · 长任务总控（已授权）

> **日期**：2026-08-17  
> **授权**：`human:侯佳伟`（本管线监管人；后续认领 **不必再问**）  
> **确认**：2026-08-17 聊天「全部同意」§0 八项  
> **目标**：Demo 库可测的产业服务链闭环：灌数 → 中间层/算法 Python → Java → `lumen-ui-topic` → **段 E 已发布冒烟**  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)  
> **对标**：产业链 [`DEMO-CHAIN-ABCD-长任务总控.md`](../产业链分析-CHAIN/DEMO-CHAIN-ABCD-长任务总控.md)  
> **存储前置**：`storage/SVC` S1–S4 已入库；细表 draft；Q-SVC-010 诚实降级不伪闭合

| 段 | 仓 | 任务 | 状态门 |
|----|-----|------|--------|
| A | `demo-algo-ent-analysis`（+ 可选 `demo-algo-science`） | `DEMO-SVC-SEED-ODS-L01` · `DEMO-SVC-SEED-MOCK-L01` | Demo 建表/种子/MOCK；禁正式库 |
| B | `lumen-topic-py` + `lumen-algo-py` | `DEMO-SVC-PY-MIDDLE-BOOT-L01` · `DEMO-SVC-PY-MIDDLE-SEARCH-L01` · `DEMO-SVC-PY-MIDDLE-TASK-L01` · `DEMO-SVC-PY-SVCAN-BOOT-L01` | A 联调闸门后；同仓 Convoy 串行 |
| C | `lumen-svc-platform` | `LUMEN-SVC-JAVA-FACADE-L01`（**新建 gkxlumen-topic-svc**）· `LUMEN-SVC-JAVA-JOB-L01`（扩 async-service） | 对标 CHAIN FACADE/JOB |
| D | `lumen-ui-topic` | `LUMEN-SVC-FE-ENTRY-L01` · `LUMEN-SVC-FE-WORKSPACE-L01` | 复刻 `demo-ui-topic` service-*；只调 Java |
| E | devops + qa + CI | `LUMEN-SVC-E-DEVOPS-L01` · `LUMEN-SVC-E-QA-SMOKE-L01` | 只认已发布前端；金路径 §4 |

厚包：[A](./DEMO-SVC-A-总派单.md) · [B](./DEMO-SVC-PY-B-总派单.md) · [C](./DEMO-SVC-JAVA-C-总派单.md) · [D](./DEMO-SVC-FE-D-总派单.md) · [E](./DEMO-SVC-E-总派单.md)

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

```text
A SEED → A MOCK
  → B MIDDLE-BOOT → MIDDLE-SEARCH → MIDDLE-TASK
       + SVCAN-BOOT（可与 MIDDLE 并行开仓，同仓仍串行）
  → C FACADE（等 MIDDLE-SEARCH）→ C JOB（等 MIDDLE-TASK + SVCAN-BOOT）
  → D ENTRY（等 C FACADE）→ D WORKSPACE（等 C JOB + D ENTRY）
  → E0 发布门 → E1 金路径
```

---

## 4. 金路径（占位 · 实施中对照 E7 USM 补故事 ID）

| # | 故事 ID | 已发布路由（拟定） | 期望（未发生=红） | 允许空态 |
|---|---------|-------------------|-------------------|----------|
| 1 | （E7 PORTAL） | `/service-portal/overview` | 门户可开；经 Java；不造假 KPI | 无数可见空态 |
| 2 | （E7 查询） | service-center 查询 | 能出记录或诚实空；不 5xx | 可空 |
| 3 | （E7 分析） | 机构分析工作区 | 经 Java 拉分析壳 | 可空 + 待核验角标 |
| 4 | （E7 生态） | 生态短板或图谱 | 任务流到可解释终态 | 按故事写明 |
| 5 | （E7 招引/培育） | 招引或培育 | 名单/预检可走通或诚实拦截 | 按故事写明 |

E0 点名：`lumen-ui-topic` · `gkxlumen-topic-svc` · `gkxlumen-topic-async-service` · `lumen-topic-py` · `lumen-algo-py`。库：`demo_gkxlumenx_*`。D12：前端不得打 `demo-*` 服务。

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
