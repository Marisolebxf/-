# DATA-CHAIN-STORAGE-S3-L01 · 派单说明

> **日期**：2026-08-12  
> **Task ID**：`DATA-CHAIN-STORAGE-S3-L01`（registry · **backlog** · 依赖 S2）  
> **派单人**：`human:淮政玮`  
> **监管**：`human:李伟`  
> **执行 Agent**：`data-agent` · 协作 `architect-agent`  
> **前置**：`DATA-CHAIN-STORAGE-S2-L01` = **done** 后升 **ready**  
> **阶段**：产业链存储 **S3**  
> **强度**：ponytail **lite**

---

## 1. 目标

向 `storage/CHAIN/stores/*` 灌入 **as-built 清单**（MySQL 含 **ADS 必含** · ES · Nebula），细表保持 **draft**，放行 S4。

---

## 2. 必读

| 序 | 路径 |
|---:|---|
| 1 | `storage/CHAIN/01-data-flow.md`（流图会签 ≠ 细表 approved） |
| 2 | `storage/ENT/stores/`（目录模板） |
| 3 | `DATA-CHAIN-db-design.md` + `data-design/产业链/*` DWD 稿 |
| 4 | S2 handoff |

---

## 3. DoD

- [ ] `stores/mysql/{dwd-*,ads,dim}.md` + README 状态列  
- [ ] `stores/elasticsearch/*` · `stores/nebula/*`  
- [ ] 真源外链清晰；冲突以 `storage/CHAIN` 叙述为准  
- [ ] 若 Demo 联调需要：在 **`demo_gkxlumenx_dwd` / `_ads`** 补齐本域缺表（结构对齐本树 stores / DATA-CHAIN-db-design；**不是**用正式库 as-built 覆盖在线 ODS 约定）  
- [ ] **禁止**仅因 S1 会签把细表改 `approved`  
- [ ] handoff · 李伟确认 · 放行 S4  

---

## 4. 认领话术（S2 done 后）

```text
认领 DATA-CHAIN-STORAGE-S3-L01
claimed_by=agent:data-agent（或 human:李伟）
supervised_by=human:李伟
claim_type=pull
强度：ponytail lite
```

---

**汇总**：[`CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md`](./CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md)
