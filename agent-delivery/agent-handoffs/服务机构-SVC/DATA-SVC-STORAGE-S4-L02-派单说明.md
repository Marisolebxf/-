# DATA-SVC-STORAGE-S4-L02 · 派单说明（阶段 F · README 入口）

> **日期**：2026-08-19  
> **Task ID**：`DATA-SVC-STORAGE-S4-L02`  
> **总控**：[`DEMO-SVC-REOPEN-长任务总控.md`](./DEMO-SVC-REOPEN-长任务总控.md)（已授权 · 范围仅阶段 F）  
> **前置（联调闸门）**：`DATA-SVC-STORAGE-S3-L02` handoff + `integration`（不等看板 `done`）  
> **流图**：[`storage/SVC/01-data-flow.md`](../../data/data-design/storage/SVC/01-data-flow.md) **`signoff_status=approved`** · `human:淮政玮` · 2026-08-19  
> **淮总会签口径**：细表**不得**标 `approved`；S4 = 入口 / 文档闭环，**不等于**灌数；**F-SEED 另开叶**  
> **派单**：`agent:coordinator-agent` · `claim_type=coordinator_dispatch`  
> **监管 / 模块负责**：`human:侯佳伟`  
> **看板签收**：`human:淮政玮`  
> **执行**：`data-agent`  
> **task_type**：`definition` · 强度：**ponytail lite**  
> **锁**：24h  

旧叶 `DATA-SVC-STORAGE-S4-L01` = **废作对照**（本地 stub、未 push）。禁止 `depends_on` 旧 L01。

---

## 1. 这张单是什么 / 不是什么

**是**：把 `storage/README.md` 的 SVC 行标成 **S1–S4 文档闭环**；旧路径 `data-design/服务机构/` stub 指向 `storage/SVC`；inventory 标明本波谁读；记下 F-SEED 前必补。

**不是**：细表 `approved`、50100 灌数、F-SEED 叶、A1–A6 全列对照、六类词表、`pipeline-to-minio.md`、改 lumen 四仓、改 CHAIN。

---

## 2. `/goal`

```
任务：DATA-SVC-STORAGE-S4-L02
监管：human:侯佳伟
认领：coordinator_dispatch · 24h
总控：agent-handoffs/服务机构-SVC/DEMO-SVC-REOPEN-长任务总控.md
厚包：agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-S4-L02-派单说明.md
强度：ponytail lite

做：storage/README + SVC/README 文档闭环；旧路径 stub；inventory 本波读法；F-SEED 前必补清单。
不做：approved、F-SEED、50100 灌数、列对照、词表、lumen 四仓、CHAIN。

禁止 force。commit [agent:data-agent]。
```
