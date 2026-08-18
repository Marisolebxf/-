# 产业集群全站改 · 任务说明书

> **角色**：FDE 闭环（不是架构方案、不是 PRD、不是某一端实现）  
> **日期**：2026-08-17  
> **来源**：同日内部讨论（徐滕强 / 李伟 / 淮政玮）  
> **执行 / 监管**：`human:李伟`（本单由李伟创建并闭环）  
> **存储真源**：[`storage/CHAIN/stores/mysql/dim-industry-cluster.md`](../../data/data-design/storage/CHAIN/stores/mysql/dim-industry-cluster.md)  
> **口径跟踪**：`客户决策清单跟踪表.md` **Q068**（🟡 团队默认）  
> **实施方案（改前范围）**：[`CHAIN-INDUSTRY-CLUSTER-全站改-实施方案.md`](./CHAIN-INDUSTRY-CLUSTER-全站改-实施方案.md)  
> **registry（2026-08-17 淮政玮）**：**只建 1 条** — `CHAIN-INDUSTRY-CLUSTER-SUPP-L01`「产业集群功能设计和实现的补充任务」。由 `human:李伟` 创建并认领。A–E 是本单内执行波次，不拆成 10 个 registry ID。设计过程溯源 = 本说明书 + 实施方案 + `dim-industry-cluster.md` + Q068。  
> **进度**：2026-08-17 已 `in_progress`；波次 A+B+C 已齐；**系统和算法（联调台）已开**；DEC 高颖已补签；波次 D lumen 未开。

## 0. 建单字段（李伟创建时照填）

| 字段 | 值 |
|---|---|
| id | `CHAIN-INDUSTRY-CLUSTER-SUPP-L01` |
| title | 产业集群功能设计和实现的补充任务 |
| status | `ready`（无前置依赖） |
| agent | `coordinator-agent`（单内按波次调 product / data / api / frontend） |
| epic | `E-CHAIN-PROTOTYPE` |
| repo | `gkx-orchestration` |
| delivery_phase | `crosscut` |
| task_type | `feature` |
| effort_points | `13` |
| difficulty | `XL` |
| estimated_tokens | `200000` |
| priority | `P0` |
| collaborators | `product-agent`, `data-agent`, `api-agent`, `frontend-agent` |
| design_refs | `agent-delivery/data/data-design/storage/CHAIN/stores/mysql/dim-industry-cluster.md`；本文；`CHAIN-INDUSTRY-CLUSTER-全站改-实施方案.md`；Q068 |
| definition_of_done | 见下 |

DoD（建单至少这 4 条）：

1. 企业 / 产业链 / 展示 / **政策 / 服务链**同一份 15 个产业集群（10+5），编码与 storage §3 一致。
2. 查询经映射展开为 L0 `industry_id[]`；无映射走空态，不造假。
3. 维护页可改映射；五件套 / demo / lumen 与 storage 同一目录，无现行「八大下拉」。
4. handoff 回链本说明书 + 实施方案 + `dim-industry-cluster.md`，可溯源整段设计。

认领（你创建后自己填）：`claimed_by=human:李伟`，`supervised_by=human:李伟`，`claim_type=pull`。

## 1. 这件事做成什么样

全站对外只说 15 个产业集群；点进去查的是当前映射到的真实 L0。目录不跟供应商改名，映射可以跟领导关注点改。

四条都成立才算完：

1. 企业、产业链、展示、政策、服务链打开，看到同一份 15 个名字。
2. 点进去，查的是映射后的真实 L0；映射改了，菜单还是这 15 个。
3. 有名无数据的产业仍在列表里，空态说清楚。
4. 以后目录再改一版，运营改映射，三个前端不用改名单。

只建了表、只加了菜单、只改了一个端，都不算完。

## 2. 方案已锁（不要再争）

| 项 | 锁定 |
|---|---|
| 目录 | 15 个，编码见 storage §3 |
| 映射 | 1:N 到 L0，允许 0；先不挂 L1 |
| 现有 12 条怎么挂 | storage §4 种子（团队默认） |
| 库表 | `gkxlumenx_dim.industry_cluster` + `industry_cluster_map` |
| 不做什么 | 不改 DWD 主表；不用旧 `CH00x`；不进 `gkxlumenx_cfg`；第一期不上图谱 |
| 调用 | 下拉读集群；出数展开 `industry_id[]` 再打 ADS |

选择器从「直接选 L0」改为「先集群、再 L0」——数据侧已锁，**产品 DEC 高颖已补签**（见 §4）。

## 3. 单内执行顺序（不是 10 条 registry）

细范围、防漏清单见实施方案 §2 / §4。registry 只有本补充任务一条；下面是单内波次，方便并行、也方便以后对照 handoff 溯源。

| 波次 | 本单内做什么 | 并行 |
|---|---|---|
| A | 产品五件套 E2 + E-31～E-35 + DEC | 可同时改两包 |
| B | dim 建表 → Java 集群 API → Demo 种子 | 建表后才能出接口 |
| C | demo-ui-topic / demo-ui-science / 后台维护 | 三端同时，一起收 |
| D | lumen-ui-topic / lumen-ui-science-pc 复刻 | 只复刻 C |
| E | 三端对账 | 收口 |

## 4. 还要人点头的（不挡团队默认开工）

| 谁 | 点什么 |
|---|---|
| 淮政玮 | 本文 + storage 是否可以按此全站改 |
| 高颖 | 修订 `DEC-CHAIN-PORTAL-OVERVIEW-L0-L1-20260806`：顶部改为先集群、再 L0。**2026-08-17 已补签** |
| PM | Q068 进甲方议程；招标 20+8 / 产品八大与 10+5 的对外说法 |
| coordinator | 只建 `CHAIN-INDUSTRY-CLUSTER-SUPP-L01`；未建本单前禁止改业务仓 |

同一 L0 是否允许挂多个集群：本轮种子 **不允许**。以后要交叉归属，只加映射行，不改 15 个编码。

## 5. 禁止

- 各端自己写一份 15 个名字或继续写死八大。
- 把 `cluster_id` 写进 DWD / ADS 主键。
- 为「看起来有数」给未映射集群造假 L0。
- 用本次改动翻签已会签的 `01-data-flow.md`。
- 未建 registry 叶就改 `lumen-*` / `demo-*` 业务代码。
