# 产业链存储链路 · S1–S4 派单汇总

> **日期**：2026-08-12（2026-08-13 补记 Demo 隔离参照）  
> **派单人**：`human:淮政玮`  
> **监管 / 会签 Owner**：`human:李伟`（四单均同）  
> **拆法**：与 ENT 对齐的 **4 单串行**（方案 1）  
> **状态**：S1 **ready** · S2–S4 **backlog**（依赖前序）

---

## 与企业维 Demo 隔离的关系（知会）

企业侧短期维持（**本批不要求李伟建库**）：

- 已有：`demo_gkxlumenx_{ods,dwd,ads,dim}`；CFG 等平台库共享  
- **不再**为其它 `gkxlumenx_*` 建 demo  

产业链 **S1–S4 先做文档树与流图会签**（`storage/CHAIN`），与企业同构。  
Demo 实例命名待 S2 等价文件再定；可复用同一 MySQL 的 `demo_` 前缀约定。

---

## 任务一览

| 序 | Task ID | 状态 | 标题 | Agent |
|---|---|---|---|---|
| S1 | `ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01` | **ready** | `storage/CHAIN` 骨架 + 流图会签 | architect-agent |
| S2 | `DATA-CHAIN-STORAGE-S2-L01` | backlog | sources / etl / seeds | data-agent |
| S3 | `DATA-CHAIN-STORAGE-S3-L01` | backlog | stores as-built 清单（draft） | data-agent |
| S4 | `DATA-CHAIN-STORAGE-S4-L01` | backlog | 旧 `data-design/产业链` stub | data-agent |

分册：同目录 `*-派单说明.md`。

---

## 顺序

```text
S1 流图会签（李伟签）→ S2 入站/ETL/seeds → S3 stores 清单 → S4 旧路径 stub
```

参照：`storage/ENT/**`（同构，禁止照抄 ENT 业务表）。  
存量：`DATA-CHAIN-db-design.md` · `data-design/产业链/*` · `md-extract` 产业链要素库。

---

## 知会后动作

1. push 本汇总 + 分册说明到 `gkx-orchestration` `dev`  
2. 微信知会李伟：先认领 **S1** `ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01`
