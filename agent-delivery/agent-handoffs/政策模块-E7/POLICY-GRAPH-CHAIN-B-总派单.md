# B 段总派单 · 政策图谱投影 `demo_gkx_chain`

> **管线**：[`POLICY-GRAPH-CHAIN-长任务总控.md`](./POLICY-GRAPH-CHAIN-长任务总控.md)  
> **本段唯一 leaf**：`POLICY-NEBULA-PROJECT-CHAIN-L01`  
> **执行**：`agent:algorithm-agent` · 监管 **`human:淮政玮`**  
> **claim**：`coordinator_dispatch` · `lock_hours=24`  
> **前序**：`DATA-POLICY-STORAGE-S1-L01` **done**（`human:淮政玮` 签收；流图不经李伟）

---

## `/goal` 头（粘贴给 algorithm-agent）

```
/goal POLICY-NEBULA-PROJECT-CHAIN-L01
角色：algorithm-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：demo-algo-ent-analysis · origin/dev
强度：ponytail full
图：必含 POLICY-STORAGE-FLOW（已 approved）；按 §3 施工范围写 demo_gkx_chain
上下文：headroom 推荐（K8s/Tempo 日志可长）
必读：
- agent-delivery/长任务执行规约.md
- agent-delivery/agent-handoffs/政策模块-E7/POLICY-GRAPH-CHAIN-长任务总控.md
- agent-delivery/data/data-design/storage/POLICY/01-data-flow.md（POLICY-STORAGE-FLOW · approved）
- agent-delivery/graph-engine.md
- repos/demo-algo-science/chainan/graph/nebula_schema.py（已有 Tag/Edge，禁止另起第二套本体）
架构铁律：图谱=Nebula；算法只在 Python；Demo 只写 demo_*；禁止第二张 G；Java 不写 nGQL。
禁止：DROP SPACE demo_gkx_chain；写入 gkx_chain；CREATE SPACE gkx_policy 作目标态；tech/talent 本波 CREATE TAG；ADS 全表扫却 source=nebula。
```

---

## 已拍板（S1 会签）

| 项 | 值 |
|---|---|
| Demo space | **仅** `demo_gkx_chain` |
| 正式 space | `gkx_chain`（禁写） |
| as-built | `gkx_policy` 虚线；禁止当目标写入 |
| 本波 Tag | `CREATE TAG IF NOT EXISTS policy`；hang 已有 `chain`/`segment`/`enterprise`/`institution` |
| 本波 Edge | `CREATE EDGE IF NOT EXISTS`：`support` / `apply_to` / `regulate` / `cite` |
| 不上图 | `tech` / `talent` |
| VID | 政策点 `pol:{policy_id}`；`vid_length=80` |
| 读路径 | Nebula 优先；失败诚实兜底 ADS `policy_graph_*` |
| 调用链 | 前端 → 网关 `gkx-policy` → `gkx-entan-py` `polan`（本叶不改 Java/前端） |

---

## 本叶交付

1. `polan` Nebula 默认 space = `demo_gkx_chain`；K8s 打开 Nebula（hosts 走现网 `192.168.88.43:9669` 惯例）。  
2. loader：按映射 UPSERT 点边；`IF NOT EXISTS` 增量 DDL，**禁止 DROP SPACE**。  
3. `/v1/policy/graph`：Nebula 可用时 `source=nebula`；不可用时 `mysql`/`ads`，禁止撒谎。  
4. Tempo-Demo 抽样或 nGQL 证据：访问 `demo_gkx_chain`。  
5. handoff：`agent-handoffs/政策模块-E7/POLICY-NEBULA-PROJECT-CHAIN-L01.md`（`ponytail: full` + cost 四字段 + `diagram_id=POLICY-STORAGE-FLOW`）。  
6. push `origin/dev`；commit `[agent:algorithm-agent]`。

---

## 架构铁律自检（handoff 必勾）

1. 算法只在 Python  
2. 本 Demo 算法库允许前端→网关→Python  
3. 图谱 Nebula，禁 Neo4j  
4. 一张 G = `demo_gkx_chain`  
5. 不写正式库 / 不写 `gkx_chain`  
6. D12 不让 lumen 调 demo 服务当正式链  
7. 可观测：trace 可证图访问或诚实兜底  
