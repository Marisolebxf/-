# ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01 · 派单说明

> **日期**：2026-08-12  
> **Task ID**：`ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01`（registry · **ready**）  
> **派单人**：`human:淮政玮`  
> **监管 / 会签 Owner**：`human:李伟`（认领时 `supervised_by=human:李伟`）  
> **执行 Agent**：`architect-agent`（主）· 协作 `data-agent`  
> **仓**：`gkx-orchestration`  
> **阶段**：产业链存储 **S1**  
> **强度**：ponytail **off**（definition / 会签）

---

## 1. 目标（一句话）

按企业维已跑通的规范，新建 **`storage/CHAIN/`**，完成 **`01-data-flow.md` 架构师会签**，放行 S2。

---

## 2. 必读（按序）

| 序 | 路径 |
|---:|---|
| 1 | `data-design/storage/README.md`（规范；决策 #1–#6） |
| 2 | `data-design/storage/ENT/`（**模板**：目录与读序，非业务照抄） |
| 3 | `architecture-baseline.md`（ADS / 调用链 / Nebula / 工厂） |
| 4 | `agent-handoffs/产业链分析-CHAIN/DATA-CHAIN-db-design.md` |
| 5 | `data-design/产业链/产业链域数据库设计(v1).md` |
| 6 | `storage/platform/minio.md`（平台正文，本域只引用） |

---

## 3. 交付（DoD）

### A. 目录骨架

- [ ] `storage/CHAIN/README.md` · `00-context.md` · `01-data-flow.md` · `CHANGELOG.md`
- [ ] 占位：`sources/` `etl/` `seeds/` `stores/{mysql,elasticsearch,nebula}/`
- [ ] 必要时轻改 `storage/README.md`：范围从「仅 ENT」扩到「多维 · 先 ENT+CHAIN」

### B. 流图会签

- [ ] 三张 Mermaid：批处理主链 / 在线读 / 对象产物  
- [ ] 表：触发 / 失败语义 / 禁止事项（对齐基线）  
- [ ] Demo 主路径口径可参照 ENT §7（LLM→约定 ODS→模拟 GDF）；ODS 真源 = `doc/` + **优先 `md-extract` 产业链要素库**  
- [ ] 开放项 `OPEN-CHAIN-FLOW-*`（调度/MinIO 域前缀/告警等）  
- [ ] frontmatter：`signoff_by: human:李伟` · `status: approved`（或驳回原因）

### C. Handoff

- [ ] `agent-handoffs/产业链分析-CHAIN/ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01.md`
- [ ] 明确放行/暂缓 S2；**未会签前 stores 细表不得 approved**

---

## 4. 禁止

- 功能设计 / Wireframe 进本树  
- PostgreSQL / Neo4j  
- 以 `gkx-mysql-raw` 当 ODS 建表真源  
- 把 ENT 企业表清单原样贴成产业链 stores  

---

## 5. 与存量关系

| 存量 | 关系 |
|---|---|
| `CHAIN-DATA-L01` / `DATA-CHAIN-db-design.md` | **输入**；不替代本树；冲突以会签后 `storage/CHAIN` 为准 |
| `CHAIN-INST-DATA-ANALYSIS-L01` | 数据源分析可引用；本单不吞并 |

---

## 6. 认领话术

```text
认领 ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01
claimed_by=agent:architect-agent（或 human:李伟）
supervised_by=human:李伟
claim_type=pull
强度：ponytail off
目标：新建 storage/CHAIN + 01-data-flow 会签
```

---

**汇总**：[`CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md`](./CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md)
