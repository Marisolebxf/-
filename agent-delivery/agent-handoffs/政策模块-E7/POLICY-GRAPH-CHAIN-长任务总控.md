# 政策图谱投影一张 G · 长任务总控（无人值守）

> **日期**：2026-08-21  
> **授权**：`human:淮政玮`（本管线监管人；后续认领 **不必再问**）  
> **目标**：政策入图投影进 Nebula **`demo_gkx_chain`**（一张 G）；停用 `gkx_policy` 作目标态；现网 ADS 镜像仅作读兜底。  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)  
> **触发**：2026-08-21 政策算法库 Tempo 抽样（`e0901e8c…` / `605f71cd…`）证明 `/v1/policy/graph` 只读 `demo_gkxlumenx_ads.policy_graph_*`，无 Nebula span；`polan` 默认 `space=gkx_policy` 且 `enabled:false`。

| 段 | 仓 | 分支 | 任务 | 状态门 |
|----|-----|------|------|--------|
| **A 存储 S1** | `gkx-orchestration` | `origin/dev` | `DATA-POLICY-STORAGE-S1-L01` | **done** |
| **A 存储 S2–S4** | `gkx-orchestration` | `origin/dev` | `DATA-POLICY-STORAGE-S2/S3/S4-L01` | **done** · 文档闭环（不灌数） |
| **B 算法投影** | `demo-algo-ent-analysis` | `origin/dev` | `POLICY-NEBULA-PROJECT-CHAIN-L01` | **done** · `human:淮政玮` 签收 · 实调 `source=nebula` |

厚包：A [`POLICY-GRAPH-CHAIN-A-总派单.md`](./POLICY-GRAPH-CHAIN-A-总派单.md) · A 续 [`POLICY-GRAPH-CHAIN-A-S2S4-总派单.md`](./POLICY-GRAPH-CHAIN-A-S2S4-总派单.md) · B [`POLICY-GRAPH-CHAIN-B-总派单.md`](./POLICY-GRAPH-CHAIN-B-总派单.md)

---

## 1. 无人值守规则（违反才停）

1. **监管已授权**：本管线政策叶一律 `supervised_by=human:淮政玮`（含 B 叶）。A 叶本人认领；B 叶 `claimed_by=agent:algorithm-agent`。`coordinator_dispatch`。锁 **24h**。  
2. **已拍板不回问**：
   - Demo 图库物理落点 = **`demo_gkx_chain`**
   - 正式图库 = **`gkx_chain`**（本管线 **禁止写入**）
   - `gkx_policy` = Wave1 as-built，图画虚线，**不是**目标态
   - MySQL 联调 = `demo_gkxlumenx_*`；禁止无闸门写 `gkxlumenx_*`
   - 调用链保持：前端 → 网关 `gkx-policy` → `demo-platform-entan-py`（`polan`）
   - 一张 G：产业链底图 + 七要素挂接；**禁止**第二套政策本体 space
3. **QC / 甲方 🟡**：挂接 Tag 缺口标 draft，不停工等纪要。  
4. **结构歧义**（新 Tag/Edge、改 VID 规则、DROP SPACE）：该叶 `blocked` + 升级 **`human:淮政玮`**（本管线不经李伟会签）。  
5. **缺数据**：A 未绿不得灌 Nebula；B 读空则空图 + 角标。  
6. git：编排仓 / demo 仓推 `origin/dev`；禁止 force；commit `[agent:<role>]`。  
7. 每叶 handoff + cost 四字段。定义叶 `ponytail: N/A`。coding 叶必含 `ponytail: full`。  
8. `ready_to_sign→done` 可积压。禁止把签收插进主链。

授权句：**后续认领不必再问。**

---

## 2. 依赖（联调闸门）

```text
POLICY-PROTO-L01 (done)
        │
        ▼
DATA-POLICY-STORAGE-S1-L01  ──A S1 流图（**done**）
        │
        ▼
DATA-POLICY-STORAGE-S2-L01 ──S3-L01 ──S4-L01  ──A 存储走程（文档闭环；不灌数）
        │  联调闸门：handoff + ≥ integration（不挡 B：B 已抢跑）
        ▼
POLICY-NEBULA-PROJECT-CHAIN-L01  ──B polan 投影
```

废作施工（不要派、不要当依赖）：

- `E-E7-POLICY-M1-L02` DoD 中的「space `gkx_policy` 为目标态」——历史 as-built，**不得**作为本管线验收。
- `POLICY-PROTO-L04` 的「无 Nebula 走 PG/SQLite」——允许作读兜底，**不允许**继续把独立 `gkx_policy` 当写入目标。

---

## 3. 开工顺序

1. Coordinator 建 A 叶 + 厚包。  
2. S1 已 **done**。S2–S4 文档闭环（本轮走程）。  
3. B 已派 `agent:algorithm-agent`（监管 `human:淮政玮`）；同仓不另派 coding。  
4. 卡住只允许：Nebula `demo_gkx_chain` 不可 USE、正式库误写风险、结构升级项。

---

## 4. 金路径（本管线不派段 E）

本管线止于 Demo 算法入图。B 叶自证：

| # | 期望（未发生=红） | 允许的空态 |
|---|-------------------|------------|
| 1 | Tempo：`GET /policy/v1/policy/graph` → `gkx-entan-py` 后出现对 `demo_gkx_chain` 的图访问，或 API `source=nebula` 且 SQL 不再是唯一路径 | Nebula 宕机时 `source` 诚实为 mysql/ads 镜像，**禁止**标 nebula |
| 2 | nGQL / loader 日志 space=`demo_gkx_chain` | 无 |
| 3 | 无 `CREATE SPACE gkx_policy` / 无写 `gkx_chain` | 无 |
