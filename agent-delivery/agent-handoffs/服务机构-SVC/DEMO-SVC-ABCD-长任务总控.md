# 产业服务链（SVC）A–E · 长任务总控（草案 · 待确认）

> **日期**：2026-08-17  
> **状态**：**DRAFT** — **未授权过夜**。须 `human:侯佳伟` 确认下方「待确认拍板项」后，再写授权句「后续认领不必再问」。  
> **目标（拟定）**：Demo 库可测的产业服务链闭环：灌数 → 中间层/算法 Python → Java → `lumen-ui-topic` → 段 E 已发布冒烟  
> **模式**：长任务（规约：[`长任务执行规约.md`](../../长任务执行规约.md)）  
> **对标**：产业链 [`DEMO-CHAIN-ABCD-长任务总控.md`](../产业链分析-CHAIN/DEMO-CHAIN-ABCD-长任务总控.md)（**同构切法**）  
> **存储前置**：`storage/SVC` S1–S4 已入库（2026-08-17）；细表仍 draft；Q-SVC-010 诚实降级不伪闭合

---

## 0. 待你确认（拍板前禁止建 A–E registry 叶 / 禁止过夜）

| # | 议题 | **建议方案（对齐 CHAIN）** | 你的确认 |
|---|------|---------------------------|----------|
| 1 | **Java 查询门面微服务名** | 新建 **`gkxlumen-topic-svc`**（api+biz），切法对齐 `gkxlumen-topic-chain` / `gkxlumen-topic-enterprise`；**不**塞进裸 `gkxlumen-topic` | ☐ 同意 / ☐ 改名：________ |
| 2 | **Java 异步 Job** | **扩展**现有 **`gkxlumen-topic-async-service`**（加 SVC adapter，对标 CHAIN KeyLink 等）；**不**另起 Job 微服务 | ☐ 同意 / ☐ 另议 |
| 3 | **对外 REST 前缀** | `/topic/v1/service/**` + `/topic/v1/service-portal/**`（IA 已有）；网关路由到 `gkxlumen-topic-svc` | ☐ 同意 / ☐ 改 |
| 4 | **业务中间层 Python** | **`lumen-topic-py`** · `/internal/gkx-svc/**`（D12）；禁止正式链路 Feign `demo-svc-topic-py` | ☐ 同意 |
| 5 | **算法 Python** | **`lumen-algo-py`** · `svcan/`；Java **不**直连算法 | ☐ 同意 |
| 6 | **段 A 灌数仓** | 主：`demo-algo-ent-analysis`（ODS 核对/补列已有）+ 必要时 `demo-algo-science` 灌数入口；只写 `demo_gkxlumenx_*` | ☐ 同意 / ☐ 改 |
| 7 | **监管 / 授权人** | 建议本管线 `supervised_by=human:侯佳伟`（或改淮政玮） | ☐ 侯佳伟 / ☐ 淮政玮 / ☐ 其他 |
| 8 | **金路径条数** | 先从 E7 USM 抽 **5–8** 条（门户/查询/分析/生态/招引各至少可测）写入 §4；CI 名暂拟 `e2e:svc-gold`（可后补） | ☐ 同意先占位 |

确认方式：在本文件改 ☐→☑，或聊天回复「确认总控 §0 全部同意 / 第 x 条改成 …」。  
**确认前**：可继续补厚包草稿；**不得** MCP 批量建编码叶、不得写授权过夜句。

---

## 1. 段表（拟定 · 同构 CHAIN）

| 段 | 仓 | 分支 | 任务形态（拟定 ID） | 状态门 |
|----|-----|------|---------------------|--------|
| A | `demo-algo-ent-analysis`（+ 可选 `demo-algo-science`） | `origin/dev` | `DEMO-SVC-SEED-ODS-L01` · `DEMO-SVC-SEED-MOCK-L01` | Demo 建表/种子/MOCK；禁正式库 |
| B | `lumen-topic-py` + `lumen-algo-py` | `origin/dev` | `DEMO-SVC-PY-MIDDLE-*` · `DEMO-SVC-PY-SVCAN-*` | A 联调闸门后；同仓 Convoy 串行 |
| C | `lumen-svc-platform` | `origin/dev` | `LUMEN-SVC-JAVA-FACADE-L01`（**新建 gkxlumen-topic-svc**）· `LUMEN-SVC-JAVA-JOB-L01`（扩 async-service） | 对标 CHAIN FACADE/JOB |
| D | `lumen-ui-topic` | `origin/dev` | `LUMEN-SVC-FE-ENTRY-L01` · `LUMEN-SVC-FE-WORKSPACE-L01` | 复刻 `demo-ui-topic` service-*；只调 Java |
| E | devops + qa + CI | K8s `dev` | `LUMEN-SVC-E-DEVOPS-L01` · `LUMEN-SVC-E-QA-SMOKE-L01` | 只认已发布前端；金路径写 §4 |

厚包（确认后补齐）：A 派单 · B 总派单 · C 总派单 · D 总派单 · E 总派单

---

## 2. 已拍板（草案默认；与 §0 冲突以你确认为准）

1. 调用链：`前端 → Java(gkxlumen-topic-svc) → lumen-topic-py /internal/gkx-svc/** →（按需）lumen-algo-py/svcan → ADS/Nebula`  
2. Java 不写算法、不直连 nGQL、不 Feign 算法仓；Job 真源在 Java async-service。  
3. 库：只写 `demo_gkxlumenx_*`；结构真源 `storage/SVC/stores/*`（draft 可联调，标待核验）。  
4. Q-SVC-010 / 六类：Mock + ⚠️「待核验」；禁止伪闭合 live。  
5. 废作：旧 13 透传式门面、Java→algo 直连、第二套机构主表、把 L01 当建表真源。  
6. git：lumen / orchestration / demo-algo-ent-analysis → `origin/dev`；禁止 force；commit `[agent:<role>]`。  
7. 锁：确认授权后 `lock_hours=24`，`claim_type=coordinator_dispatch`。

---

## 3. 依赖（联调闸门，不等签收 done）

```text
A SEED → A MOCK
  → B MIDDLE-BOOT → SEARCH/PORTAL 读面 → TASK 适配
       + SVCAN-BOOT → gap/graph/tech/recommend（按数据就绪）
  → C FACADE（等 MIDDLE 读面）→ C JOB（等 TASK + 样板算法键）
  → D ENTRY → D WORKSPACE
  → E0 发布门 → E1 金路径
```

---

## 4. 金路径（占位 · 确认后从 E7 USM 填满）

| # | 故事 ID（待填） | 已发布路由（拟定） | 期望（未发生=红） | 允许空态 |
|---|-----------------|-------------------|-------------------|----------|
| 1 | US-SVCCHAIN-… | `/service-portal/overview` | 门户可开；经 Java；不造假 KPI | 无数可见空态 |
| 2 | … | `/service-center/…` 查询 | 三模式之一能出记录或诚实空 | 可空 |
| 3 | … | 机构分析 | 经 Java 拉分析壳 | 可空 + 待核验角标 |
| 4 | … | 生态/短板或图谱 | 任务流到可解释终态 | 按故事写明 |
| 5 | … | 招引或培育 | 名单/预检可走通或诚实拦截 | 按故事写明 |

E0 点名服务（拟定）：`lumen-ui-topic` · `gkxlumen-topic-svc` · `gkxlumen-topic-async-service` · `lumen-topic-py` · `lumen-algo-py`。

---

## 5. 授权区（确认 §0 后再填）

> **授权**：`human:________`  
> **日期**：________  
> **授权句**：后续认领 **不必再问**。（未填 = 不得过夜长任务）

---

## 6. 变更记录

| 日期 | 说明 |
|------|------|
| 2026-08-17 | 初稿：对标 CHAIN；Java 建议 `gkxlumen-topic-svc` + 扩 async-service；待侯佳伟确认 §0 |
