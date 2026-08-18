# 产业服务链 C/D 细叶拆单（一接口 / 一故事）

> **日期**：2026-08-18  
> **拍板**：与产业链同切法（规约 v1.11）  
> **总控**：[`DEMO-SVC-ABCD-长任务总控.md`](./DEMO-SVC-ABCD-长任务总控.md)  
> **监管**：`human:侯佳伟` · lock 24h  
> **状态**：细叶 **`backlog`**；旧厚包仅骨架 fan-in

旧厚包不删：`LUMEN-SVC-JAVA-FACADE-L01` / `JAVA-JOB-L01` / `FE-ENTRY-L01` / `FE-WORKSPACE-L01` / `FE-ENTRY-VISUAL-C1` / `FE-WORKSPACE-VISUAL-C1` / `FE-SEARCH-REPLICA-C2`。新施工真源 = 本表。禁止再用「轻量表格」关闭 V1–V7。

---

## 1. 段 C · 一 REST 路径一叶

仓：`lumen-svc-platform` · 网关 `/svc/topic/v1/service|service-portal/**` + `/topicAsync/topic/v1/analysis/**`

### 已有路径（收口 + 字段对齐 Demo）

| ID | 方法 · 路径 | 依赖 |
|----|-------------|------|
| `LUMEN-SVC-JAVA-API-SEARCH-ORGS-L01` | POST `/topic/v1/service/search/orgs` | `DEMO-SVC-PY-MIDDLE-SEARCH-L01` |
| `LUMEN-SVC-JAVA-API-PROFILE-GET-L01` | POST `/topic/v1/service/profile/get` | SEARCH-ORGS |
| `LUMEN-SVC-JAVA-API-PORTAL-OVERVIEW-L01` | POST `/topic/v1/service-portal/overview` | MIDDLE-SEARCH |
| `LUMEN-SVC-JAVA-API-PORTAL-RANKING-L01` | POST `/topic/v1/service-portal/ranking` | PORTAL-OVERVIEW |
| `LUMEN-SVC-JAVA-API-TASK-CREATE-L01` | POST `/topic/v1/analysis/tasks` | `JAVA-JOB-L01` + `PY-MIDDLE-TASK` + `PY-SVCAN-BOOT` |
| `LUMEN-SVC-JAVA-API-TASK-GET-L01` | GET `/topic/v1/analysis/tasks/{id}` | CREATE |
| `LUMEN-SVC-JAVA-API-TASK-RESULT-L01` | GET `/topic/v1/analysis/tasks/{id}/result` | CREATE |
| `LUMEN-SVC-JAVA-API-TASK-EVENTS-L01` | GET `/topic/v1/analysis/tasks/{id}/events` | CREATE |

Health 随 SEARCH-ORGS 自检。

### 缺口路径（USM 需要、现网尚无独立 REST → 仍一叶）

| ID | 拟路径 | 故事 |
|----|--------|------|
| `LUMEN-SVC-JAVA-API-PORTAL-INDUSTRY-L01` | portal 产业分布 | `US-SVC-PT-02` |
| `LUMEN-SVC-JAVA-API-PORTAL-REGION-L01` | portal 区域分布 | `US-SVC-PT-03` |
| `LUMEN-SVC-JAVA-API-PORTAL-SZ-L01` | portal 深圳统计 | `US-SVC-PT-05` |
| `LUMEN-SVC-JAVA-API-PORTAL-KEYORG-L01` | 重点机构介绍 | `US-SVC-PT-06` |
| `LUMEN-SVC-JAVA-API-ECO-GRAPH-L01` | 生态图谱读面 | `US-SVC-ECO-01` |
| `LUMEN-SVC-JAVA-API-REC-LIST-L01` | 招引/培育名单 | `US-SVC-REC-02/04` |

若总控授权「先复用 overview section、不新建 path」，该叶 DoD 改为 **文档化降级 + 前端诚实空**，仍单独验收，禁止 silently 并进 OVERVIEW 厚包。

Job `analysisType` 白名单（shortboard 等）留在 CREATE 叶，不按键拆 Java。

---

## 2. 段 D · 一 USM 故事一叶

仓：`lumen-ui-topic` · 复刻 `demo-ui-topic` `service-portal/*` + `service-center/*`  
壳：`LUMEN-SVC-FE-SHELL-L01`（侧栏/路由/`menu:svc:*`）· `LUMEN-SVC-FE-WAITVIEW-L01`

### 门户 `US-SVC-PT-*`

| ID | 故事 | 路由（拟定） |
|----|------|----------------|
| `LUMEN-SVC-FE-US-PT-01` | `US-SVC-PT-01` 全球概况 | `/service-portal/overview` |
| `LUMEN-SVC-FE-US-PT-02` | `US-SVC-PT-02` 产业分布 | `/service-portal/industry-distribution` |
| `LUMEN-SVC-FE-US-PT-03` | `US-SVC-PT-03` 区域分布 | `/service-portal/region-map` |
| `LUMEN-SVC-FE-US-PT-04` | `US-SVC-PT-04` 技术力 Top30 | `/service-portal/capability-rank` |
| `LUMEN-SVC-FE-US-PT-05` | `US-SVC-PT-05` 深圳统计 | `/service-portal/shenzhen` |
| `LUMEN-SVC-FE-US-PT-06` | `US-SVC-PT-06` 重点机构介绍 | 门户内抽屉/页 |

### 查询 / 分析 / 对比篮 `US-SVC-ORG-*`

| ID | 故事 | 路由 |
|----|------|------|
| `LUMEN-SVC-FE-US-ORG-07` | `US-SVC-ORG-07` 检索（Workbench 完整复刻） | `/service-center/search` |
| `LUMEN-SVC-FE-US-ORG-08` | `US-SVC-ORG-08` 对比篮 | 篮面板 |
| `LUMEN-SVC-FE-US-ORG-01` | `US-SVC-ORG-01` 组装分析对象集 | 分析工作区 |
| `LUMEN-SVC-FE-US-ORG-02` | `US-SVC-ORG-02` 领域覆盖 | 同上 |
| `LUMEN-SVC-FE-US-ORG-03` | `US-SVC-ORG-03` 画像下钻 | `?org=` + 抽屉 |
| `LUMEN-SVC-FE-US-ORG-04` | `US-SVC-ORG-04` 新增趋势 | 分析工作区 |
| `LUMEN-SVC-FE-US-ORG-05` | `US-SVC-ORG-05` 市场热度 | 同上 |
| `LUMEN-SVC-FE-US-ORG-06` | `US-SVC-ORG-06` 技术力评估 | 同上 |

ORG-07 DoD **必须**过 V1–V7 + ElementSearchWorkbench 三段；`SEARCH-REPLICA-C2` 只作对照，不能代替本叶签收。

### 生态 / 招引

| ID | 故事 |
|----|------|
| `LUMEN-SVC-FE-US-ECO-01`～`06` | `US-SVC-ECO-01`～`06` |
| `LUMEN-SVC-FE-US-REC-01`～`04` | `US-SVC-REC-01`～`04` |

---

## 3. DAG

coordinator 过夜循环见规约 **§9.1**。与 CHAIN 抢 `lumen-ui-topic`，默认 CHAIN 先。

```text
B MIDDLE-SEARCH / TASK / SVCAN
  → C 已有路径细叶（同仓串行）→ C 缺口路径叶
  → D SHELL → PT-01（金路径 #1）∥ ORG-07（金路径 #2，V1–V7）
  → D WAITVIEW → ORG-01/02（金路径 #3）→ ECO-01（#4）→ REC-02（#5）
  → 其余 P0
  → 闸4：SHELL+WAITVIEW+全部 P0 D 叶 ≥ pending_test → 重开 E0 → E1
```

E1 金路径 = 总控 §4 真实 `US-SVC-*`。旧 E1「能出记录或诚实空」作废。
