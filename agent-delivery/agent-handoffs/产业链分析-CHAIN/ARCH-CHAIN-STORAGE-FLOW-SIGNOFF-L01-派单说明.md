# ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01 · 派单说明

> **日期**：2026-08-12（2026-08-13 补：下游建表真源）  
> **Task ID**：`ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01`（registry · **ready**）  
> **派单人**：`human:淮政玮`  
> **监管 / 会签 Owner**：`human:李伟`  
> **执行**：`architect-agent` 或 `human:李伟`  
> **强度**：ponytail **off**

---

## 1. 目标

新建 `storage/CHAIN/`，完成 `01-data-flow.md` 会签，**明确 ODS 建表真源 = 三方在线文档**，放行 S2（由李伟按文档在 `demo_*` 建表）。

---

## 2. 必读

| 序 | 路径 |
|---:|---|
| 1 | `storage/README.md` · `storage/ENT/`（模板） |
| 2 | `architecture-baseline.md` |
| 3 | `DATA-CHAIN-db-design.md`（输入，冲突以本树会签为准） |
| 4 | **`third-party-source/doc/md-extract/`** · 产业链要素库（及权威 xlsx） |
| 5 | ENT 参照：`pipeline-demo-mock.md`（demo_* 隔离已落地） |

---

## 3. DoD

- [ ] `storage/CHAIN` 骨架 + `01-data-flow` 三图与失败语义  
- [ ] 流图/文中写死：Demo ODS **表名字段 = doc/md-extract**；落 **`demo_gkxlumenx_ods`**（禁止正式 ODS）  
- [ ] 开放项 `OPEN-CHAIN-FLOW-*`；`signoff_by: human:李伟`  
- [ ] handoff 放行 S2：**S2 必须按在线文档建表**（不只写文档清单）

---

## 4. 禁止

- 以 live as-built 当 ODS 真源  
- 本单可不执行 DDL（DDL 在 S2），但不得写「等现网表结构」替代在线文档  

---

## 5. 认领

```text
认领 ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01
claimed_by=human:李伟（或 agent:architect-agent）
supervised_by=human:李伟
强度：ponytail off
```

**汇总**：[`CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md`](./CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md)
