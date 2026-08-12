# DATA-CHAIN-STORAGE-S4-L01 · 派单说明

> **日期**：2026-08-12  
> **Task ID**：`DATA-CHAIN-STORAGE-S4-L01`（registry · **backlog** · 依赖 S3）  
> **派单人**：`human:淮政玮`  
> **监管**：`human:李伟`  
> **执行 Agent**：`data-agent` · 协作 `architect-agent`  
> **前置**：`DATA-CHAIN-STORAGE-S3-L01` = **done** 后升 **ready**  
> **阶段**：产业链存储 **S4**  
> **强度**：ponytail **lite**

---

## 1. 目标

旧路径 **`data-design/产业链/`** 增加 stub / 导航，强制指向 **`storage/CHAIN`**；不删旧 DDL 正文（供外链）。

参照：`DATA-ENT-STORAGE-S4-L01`（企业维 stub 做法）。

---

## 2. DoD

- [ ] `data-design/产业链/README.md`（或等价）→ 现行入口 = `storage/CHAIN`  
- [ ] 主要旧稿文首横幅：冲突以 storage/CHAIN 为准  
- [ ] CHANGELOG  
- [ ] handoff：`…/DATA-CHAIN-STORAGE-S4-L01.md` · 李伟确认  

---

## 3. 禁止

- 删除旧 DDL 大稿正文（除非另有归档任务）  
- 在本单重开 stores 结构评审升 approved（另开）  

---

## 4. 认领话术（S3 done 后）

```text
认领 DATA-CHAIN-STORAGE-S4-L01
claimed_by=agent:data-agent（或 human:李伟）
supervised_by=human:李伟
claim_type=pull
强度：ponytail lite
```

---

**汇总**：[`CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md`](./CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md)
