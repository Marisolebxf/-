# DATA-SVC-STORAGE-S4-L01 · 派单说明

> **日期**：2026-08-14  
> **Task ID**：`DATA-SVC-STORAGE-S4-L01`（**本地执行** · 依赖 S3 本地签收放行）  
> **派单人**：`human:淮政玮` / **本地开跑**：`human:侯佳伟`（2026-08-17）  
> **监管**：`human:侯佳伟`  
> **执行 Agent**：`agent:data-agent`  
> **前置**：S3 Owner 本地放行（本会话随「进行本地 S4」一并视为确认）  
> **强度**：ponytail **lite**  
> **Git**：**不 commit / 不 push**  
> **汇总**：[`SVC-STORAGE-S1-S4-DISPATCH-2026-08-14.md`](./SVC-STORAGE-S1-S4-DISPATCH-2026-08-14.md)

---

## 1. 目标

旧路径 **`data-design/服务机构/`** 增加 stub / 导航，强制指向 **`storage/SVC`**；不删旧稿正文（供对照）。

参照：`DATA-ENT-STORAGE-S4-L01` · `DATA-CHAIN-STORAGE-S4-L01`。

---

## 2. DoD

- [ ] `data-design/服务机构/README.md`（新建或改）：现行入口 = `storage/SVC`  
- [ ] `服务机构域数据库设计(v1).md` 文首横幅：冲突以 storage/SVC 为准  
- [ ] `SVC-DATA-ANALYSIS-L01-数据分析报告.md` 文首横幅：**legacy 分析纪要，非 ODS/stores 真源**；开放项仍指向决策清单 §2.ae  
- [ ] `storage/SVC/CHANGELOG.md` 记 S4  
- [ ] handoff：`agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-S4-L01.md`  

---

## 3. 禁止

- 删除旧分析报告 / v1 库设计正文（除非另有归档任务）  
- 在本单重开 stores 结构评审升 approved（另开）  
- 把 L01 结论改写成现行建表真源  

---

## 4. 认领话术（S3 done 后）

```text
认领 DATA-SVC-STORAGE-S4-L01
claimed_by=agent:data-agent（或 human:{Owner}）
supervised_by=human:{Owner}
claim_type=pull
强度：ponytail lite
```
