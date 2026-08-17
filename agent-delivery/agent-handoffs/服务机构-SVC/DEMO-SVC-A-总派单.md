# 段 A · SVC Demo 灌数总派单

> **监管**：`human:侯佳伟` · 总控已授权不必再问  
> **仓**：`demo-algo-ent-analysis`（主）· 可选 `demo-algo-science`  
> **分支**：`origin/dev` · **强度**：ponytail **full**  
> **总控**：[DEMO-SVC-ABCD-长任务总控.md](./DEMO-SVC-ABCD-长任务总控.md)

## 铁律

- 只写 `demo_gkxlumenx_*`；禁正式 `gkxlumenx_*`  
- 结构真源 `storage/SVC`；复用 ENT 机构主表，禁第二套  
- Q-SVC-010：圈定结果标待核验  

## 叶

| ID | 一句话 DoD |
|----|------------|
| `DEMO-SVC-SEED-ODS-L01` | Demo ODS 核对/补列齐；本域 DWD/ADS 可按 DDL 草稿建表（Owner 指示 APPLY） |
| `DEMO-SVC-SEED-MOCK-L01` | 最小种子/MOCK 撑住后续查询与 Job 用例；标 mock+GAP |

## /goal 头

```
任务：{ID}
仓：demo-algo-ent-analysis · origin/dev
监管：human:侯佳伟 · claim_type=coordinator_dispatch · lock 24h
强度：ponytail full
必读：DEMO-SVC-ABCD-长任务总控.md · 本总派单 · storage/SVC/**
```
