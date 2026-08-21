# A 段总派单 · 政策维存储设计（投影 `demo_gkx_chain`）

> **管线**：[`POLICY-GRAPH-CHAIN-长任务总控.md`](./POLICY-GRAPH-CHAIN-长任务总控.md)  
> **本段唯一 leaf**：`DATA-POLICY-STORAGE-S1-L01`  
> **执行**：`human:淮政玮` 本人认领并会签 · **不经李伟**  
> **claim**：`pull` · `lock_hours=24`  
> **定义轨**：禁止 `/goal` 强度行压文档；禁止改 `demo-algo-*` / `lumen-*` 代码。

---

## `/goal` 头（粘贴给 data-agent）

```
/goal DATA-POLICY-STORAGE-S1-L01
角色：data-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：gkx-orchestration · origin/dev
图：必含 POLICY-STORAGE-FLOW；CHAIN-STORAGE-FLOW 仅增量补丁（政策挂接边）
必读：
- agent-delivery/长任务执行规约.md
- agent-delivery/agent-handoffs/政策模块-E7/POLICY-GRAPH-CHAIN-长任务总控.md
- agent-delivery/data/data-design/storage/README.md（决策 #7 一张 G）
- agent-delivery/data/data-design/storage/CHAIN/01-data-flow.md
- agent-delivery/diagram-as-contract.md
- agent-delivery/graph-engine.md §3.1
- repos/demo-algo-science/chainan/graph/nebula_schema.py（已有 Tag/Edge，禁止另起第二套本体）
架构铁律：图谱=Nebula；Java 不写 nGQL；Demo 只写 demo_*；禁止第二张 G。
禁止：DROP SPACE demo_gkx_chain；写入 gkx_chain；CREATE SPACE gkx_policy 作目标态；细表自填 approved。
```

---

## 已拍板

| 项 | 值 |
|---|---|
| Demo space | `demo_gkx_chain` |
| 正式 space | `gkx_chain`（本管线禁写） |
| as-built | `gkx_policy` 虚线 |
| MySQL | `demo_gkxlumenx_{ods,dwd,ads}` |
| 挂接原则 | 政策作为七要素挂到产业链底图；跨域 DWD 主键对齐 |
| CHAIN 已有 Tag | `chain` / `segment` / `enterprise` / `institution` |
| CHAIN 已有 Edge | `belongs_to` / `participates` / `supplies` / `depends_on` |
| 流图会签 | POLICY · `human:淮政玮` · 2026-08-21 **approved**（不经李伟） |
| data-agent 监管 | `human:淮政玮`（本叶本人执行） |

现网事实（勿当目标态）：政策页读 ADS `policy_graph_node/edge`；`polan` Nebula 关闭。

---

## 本叶交付

1. 新建 `agent-delivery/data/data-design/storage/POLICY/`（同构 CHAIN：README / 00-context / 01-data-flow）。  
2. `POLICY-STORAGE-FLOW`：ODS→DWD→ADS 实线；Python→`demo_gkx_chain` 实线（投影）；`gkx_policy` 虚线；Java 只读 ADS。四列表必填。  
3. 点边映射表：今日 polan（policy/industry/tech/… + support/apply_to/…）如何挂到一张 G；缺项 **draft**。  
4. 修订 `storage/README.md`：POLICY 域入口；政策模块 L2 认 `POLICY-STORAGE-FLOW` + 挂 `CHAIN-STORAGE-FLOW`。  
5. `CHAIN/01-data-flow.md` 增量：政策挂接边 + `amendment_note`；**不改** §1 已签主拓扑含义。  
6. 旧 `政策域数据库设计(v1)` 文首过期，回链本树。  
7. handoff：`agent-handoffs/政策模块-E7/DATA-POLICY-STORAGE-S1-L01.md`。

下游 `POLICY-NEBULA-PROJECT-CHAIN-L01` **已放行 ready**（流图会签通过）。

---

## 架构铁律自检（handoff 必勾）

1. 算法只在 Python  
2. 调用链前端→Java→Python（本 Demo 算法库允许前端→网关→Python，不在本叶改）  
3. 图谱 Nebula，禁 Neo4j  
4. 一张 G = `demo_gkx_chain`  
5. 不写正式库  
6. D12 本叶不碰 lumen 前端调 demo 服务  
