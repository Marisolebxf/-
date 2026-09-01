# 政策维（POLICY）存储设计 — 入口

> **读我**：政策维存储现行入口。图谱 **投影进一张 G**（`demo_gkx_chain`），**禁止**把 `gkx_policy` 当目标态。  
> **规范**：[`../README.md`](../README.md)（决策 #7）  
> **流图**：[`01-data-flow.md`](./01-data-flow.md) · `diagram_id=POLICY-STORAGE-FLOW` · **approved** · `human:淮政玮` · 2026-08-21（不经李伟）  
> **阶段**：S1–S4 **文档闭环**（细表 draft · **未灌数**）· 监管 `human:淮政玮`

```yaml
---
doc_id: POLICY-STORAGE-INDEX
element: POLICY
role: index
status: draft
version: "2026-08-21"
updated: 2026-08-21
task_id: DATA-POLICY-STORAGE-S1-L01
---
```

## 读序（强制）

1. [`00-context.md`](./00-context.md)  
2. [`01-data-flow.md`](./01-data-flow.md) — **L2 approved**；细表不得标 approved  
3. [`sources/inventory.md`](./sources/inventory.md) + [`sources/ods-ddl.md`](./sources/ods-ddl.md)（贴源结构真源）  
4. [`etl/README.md`](./etl/README.md) — **ETL 管道索引**（含各管道 as-built / draft / not-built 状态）  
5. [`seeds/README.md`](./seeds/README.md)  
6. [`stores/`](./stores/README.md) — **draft**  
7. [`windows/display-ds10-12.md`](./windows/display-ds10-12.md) — 展示 DS10-12 窗口对照  
8. 旧稿 [`../../政策/政策域数据库设计(v1).md`](../../政策/政策域数据库设计(v1).md) **过期**

## 已锁定（本叶）

| 项 | 值 |
|---|---|
| Demo Nebula | **仅** `demo_gkx_chain` |
| 正式 Nebula | `gkx_chain`（本管线禁写） |
| as-built | `gkx_policy` 虚线；禁止 CREATE/DROP 作目标态 |
| MySQL Demo | `demo_gkxlumenx_{ods,dwd,ads}` |
| RDBMS | 仅 MySQL |
| 写图仓 | `demo-algo-ent-analysis` `polan`（`POLICY-NEBULA-PROJECT-CHAIN-L01`） |
| 细表 | **draft**（文档闭环 ≠ 灌数 / ≠ approved） |

## 任务

| 阶段 | Task | 状态 |
|---|---|---|
| S1 | `DATA-POLICY-STORAGE-S1-L01` | **ready_to_sign** · 待 `human:淮政玮` 签收 |
| S2 | `DATA-POLICY-STORAGE-S2-L01` | **ready_to_sign** · 待 `human:淮政玮` 签收 |
| S3 | `DATA-POLICY-STORAGE-S3-L01` | **ready_to_sign** · stores draft · 待签收 |
| S4 | `DATA-POLICY-STORAGE-S4-L01` | **ready_to_sign** · 文档闭环 ≠ 灌数 · 待签收 |
| B | `POLICY-NEBULA-PROJECT-CHAIN-L01` | **done** · `human:淮政玮` 签收 |
