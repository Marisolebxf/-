# API-DEMO-INNOV-ADS-ISOLATE-L01 · 派单条

> 长任务总控：[`D12-LUMEN-INNOV-ENTAN-长任务总控.md`](./D12-LUMEN-INNOV-ENTAN-长任务总控.md)  
> 强度：ponytail full。仓：`demo-svc-platform`。监管：`human:淮政玮`。

## /goal

你是经验丰富的 api-agent。闭合 D12：demo 创新监测 Java **不再读正式 `gkxlumenx_ads`**。  
强度：ponytail full。  
必读：本派单条 + 总控 + `architecture-baseline.md` 数据面 as-built。  
禁止：改 lumen Java/SQL；GDF 全量迁数；把 lumen JDBC 改成 `gkxlumenx_ads`。

## 已拍板

- 全拆：demo 不读写正式 ADS；cfg 可共享。
- demo SQL 保持 2B 逻辑名 `gkxlumenx_ads.*`，运行时 DataPlane 改写到 `demo_gkxlumenx_*`。
- demo ADS 缺表时允许 **一次性 snapshot**（`CREATE TABLE LIKE` + `INSERT SELECT`），不是 GDF、不是持续跨库读。

## DoD

见 registry `API-DEMO-INNOV-ADS-ISOLATE-L01`。
