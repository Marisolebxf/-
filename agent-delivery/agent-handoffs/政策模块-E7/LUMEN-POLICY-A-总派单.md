# A 段总派单 · 政策专题退出门

> **管线**：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> **本段**：不重做 S1–S4。只做 Demo 库可测退出门。  
> **执行**：`agent:data-agent`（可选 algorithm 补 MOCK）· 监管 `human:淮政玮`

## `/goal` 头

```
/goal DEMO-POLICY-A-RECLOSE-L01
角色：data-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：demo-algo-ent-analysis · origin/dev
强度：ponytail full
图：必含 POLICY-STORAGE-FLOW（不翻签；本叶不改拓扑）
必读：LUMEN-POLICY-ABCDE-长任务总控.md · storage/POLICY/01-data-flow.md
架构铁律：lumen 数仓 = demo 源，只写 demo_gkxlumenx_*；禁止正式 gkxlumenx_* 数据面；图谱一张 G demo_gkx_chain。
```

## 已拍板

- ODS/DWD/ADS 已有政策灌数路径（`polan` `run_sync` / `ods_to_dwd`）。本叶验收「可复跑 + 样本可挂图」，不新开工厂。lumen 读的也是这套 `demo_gkxlumenx_*`。
- 样本锚：政策 `21259543` 须能挂 `chain:INB170101`（或同等图上链码）。
- MOCK 叶仅当 Job 缺底数；标 mock + GAP。

## DoD（退出门）

1. `demo_gkxlumenx_ods` / `_dwd.policy_base_info` / ADS `policy_*` 行数与复跑命令写入 handoff。  
2. 至少 1 条政策 `related_entities.industry` 含图上 `industry_link_code`。  
3. 禁止写正式 `gkxlumenx_*` 数据面 / 三方 `gkx`。lumen 现网数仓就是 demo 源，本叶不换仓。  
4. handoff + cost 四字段 + `ponytail: full`。
