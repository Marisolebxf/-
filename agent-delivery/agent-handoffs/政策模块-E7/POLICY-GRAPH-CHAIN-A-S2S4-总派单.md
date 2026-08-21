# A 段续 · 政策维存储 S2–S4（文档闭环）

> **管线**：[`POLICY-GRAPH-CHAIN-长任务总控.md`](./POLICY-GRAPH-CHAIN-长任务总控.md)  
> **叶**：`DATA-POLICY-STORAGE-S2-L01` → `S3-L01` → `S4-L01`  
> **执行 / 监管**：`human:淮政玮`  
> **claim**：`coordinator_dispatch` · `lock_hours=24`  
> **定义轨**：禁止 ponytail 强度行压文档；禁止改业务仓；**不灌数**；**不翻签** `POLICY-STORAGE-FLOW`。  
> **内容**：从 `政策域数据库设计(v1)` + 现网 `polan` as-built **搬树**；图谱落点改 `demo_gkx_chain`。

---

## `/goal` 头（S2）

```
/goal DATA-POLICY-STORAGE-S2-L01
角色：data-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：gkx-orchestration · origin/dev
图：必含 POLICY-STORAGE-FLOW（已 approved，本叶不改拓扑）
必读：storage/POLICY/01-data-flow.md · storage/SVC/etl/pipeline-demo-mock.md（同构指针）
禁止：灌数；写正式库；翻签流图；细表 approved。
```

S3 / S4 同头，只换 task-id。S3 图仍认同一 `POLICY-STORAGE-FLOW`。
