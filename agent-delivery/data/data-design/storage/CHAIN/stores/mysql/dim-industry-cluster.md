# DIM · 产业集群（展示目录 → L0 映射）

```yaml
---
doc_id: CHAIN-STORE-DIM-INDUSTRY-CLUSTER
element: CHAIN
role: store-mysql
status: draft
version: "2026-08-17"
updated: "2026-08-17"
engine: mysql
policy_version: sz-10+5-2026
decision_ref: Q068
task_brief: agent-handoffs/产业链分析-CHAIN/CHAIN-INDUSTRY-CLUSTER-全站改-任务说明书.md
---
```

> **本文件是产业集群存储真源。** 查表、编码、种子映射只认这里。  
> 字段级 DDL / 灌种 SQL：`data/ddl/gkxlumenx_dim_industry_cluster.sql`（波次 B）。  
> Java 契约：`agent-handoffs/产业链分析-CHAIN/API-CHAIN-INDUSTRY-CLUSTER.md`。  
> 不改 `industry_chain`。不翻签 `01-data-flow.md`。  
> 口径未获甲方书面确认前按团队默认跑，UI 标 ⚠️，见 `客户决策清单跟踪表.md` **Q068**。

## 1. 锁死的事

领导看的目录，和供应商给的产业，不是同一套东西。全站对外只说 **15 个产业集群**；查数时翻译成当时挂上的真实 L0。目录稳，映射可以变。

| 锁 | 值 |
|---|---|
| 对外目录 | 固定 15（10 战新 + 5 未来），编码自编 |
| 映射目标 | 只挂 `industry_chain.chain_tier='L0'` 的 `industry_id`（INB，Q053） |
| 基数 | 集群 → L0 为 **1:N**，允许 **0**；本轮不挂 L1 |
| 空态 | 枚举仍在；映射 0 条则「无相关产业数据」，去要数，不藏、不造假 |
| 共用 | 企业 / 产业链 / 展示 / 政策 / 服务链读同一份 |
| 库 | `gkxlumenx_dim`（Demo：`demo_gkxlumenx_dim`） |
| 表 | `industry_cluster`（15 行）+ `industry_cluster_map` |
| 图谱 | 第一期不投影；查图前先展开成 L0 |
| 禁止 | 改 `industry_chain` 加列；复活旧 `CH00x`；写入 `gkxlumenx_cfg`（算法配置库） |

## 2. 谁写谁读

| 对象 | 写 | 读 |
|---|---|---|
| `industry_cluster` / `_map` | 维护页经 Java 管理接口；Demo 种子 | 全站查询只读；ETL **不写** |
| `industry_chain` L0 | 仅 ETL | 映射目标必须已存在；业务查询不扫 DWD，查数走 ADS |

查询约定：界面用 `cluster_id`；出数把映射展开成 `industry_id[]` 再打现有 ADS。空数组走空态。

## 3. 15 个编码（团队默认）

政策版：`sz-10+5-2026`。名称来自 2026-08-17 内部讨论（淮政玮转述深圳 3.0）。

| cluster_id | 组 | 名称 | 括号说明（展示可用，不另编码） |
|---|---|---|---|
| `CL-SEI-01` | 战新 | 新一代信息技术 | — |
| `CL-SEI-02` | 战新 | 生物产业 | — |
| `CL-SEI-03` | 战新 | 新能源 | — |
| `CL-SEI-04` | 战新 | 新材料 | — |
| `CL-SEI-05` | 战新 | 高端装备 | — |
| `CL-SEI-06` | 战新 | 智能网联新能源汽车 | — |
| `CL-SEI-07` | 战新 | 绿色环保 | — |
| `CL-SEI-08` | 战新 | 低空经济与空天 | — |
| `CL-SEI-09` | 战新 | 传统与创意产业 | — |
| `CL-SEI-10` | 战新 | 海洋产业 | — |
| `CL-FUT-01` | 未来 | 未来制造 | 智能机器人 |
| `CL-FUT-02` | 未来 | 未来信息 | 光载信息、AI 底层生态 |
| `CL-FUT-03` | 未来 | 未来能源 | — |
| `CL-FUT-04` | 未来 | 未来空间 | — |
| `CL-FUT-05` | 未来 | 未来健康 | 合成生物、细胞基因、脑机工程 |

排序：先 10 个战新，再 5 个未来，与上表顺序一致。

## 4. 种子映射（团队默认 · 对现网三方 DWD L0）

L0 清单来自 `demo_gkxlumenx_dwd.industry_chain`（`chain_tier='L0'`，现网 12 条：`INB12xx` / `INB13xx` / `INB15xx` / `INB25xx`）。旧 3.0 mock 的 `INB17xx` / `INB18xx` **不再挂**。本轮仍 **不挂 L1**。

**2026-09-02 监管人确认共享**：`CL-FUT-02` 与 `CL-SEI-01` 共享软件/AI；`CL-FUT-04` 与 `CL-SEI-08` 共享低空经济。其余无现网 L0 的集群保持空态。口径仍 **Q068 🟡**。

| cluster_id | 挂上的 L0（industry_id = 名称） | 状态 |
|---|---|---|
| `CL-SEI-01` | `INB1303` 集成电路；`INB1323` 传感器；`INB1309` 人工智能；`INB1333` 智能终端；`INB1306` 软件与信息服务 | mapped |
| `CL-SEI-02` | `INB2503` 生物医药 | mapped |
| `CL-SEI-03` | — | pending_vendor |
| `CL-SEI-04` | — | pending_vendor |
| `CL-SEI-05` | — | pending_vendor |
| `CL-SEI-06` | `INB1209` 智能网联汽车 | mapped |
| `CL-SEI-07` | — | pending_vendor |
| `CL-SEI-08` | `INB1236` 低空经济 | mapped |
| `CL-SEI-09` | `INB1502` 数字创意 | mapped |
| `CL-SEI-10` | — | pending_vendor |
| `CL-FUT-01` | `INB1204` 机器人；`INB1354` 具身智能 | mapped |
| `CL-FUT-02` | `INB1306` 软件与信息服务；`INB1309` 人工智能（共享 SEI-01） | mapped |
| `CL-FUT-03` | — | pending_vendor |
| `CL-FUT-04` | `INB1236` 低空经济（共享 SEI-08） | mapped |
| `CL-FUT-05` | `INB2505` 合成生物 | mapped |

映射行 15、去重 L0 12。领导改关注点 = 改本表有效映射，不改 §3 的 15 行。正式 `gkxlumenx_dim` 勿用本种子覆盖。

## 5. 选择器（对账，不在本树实现）

现网已批：`DEC-CHAIN-PORTAL-OVERVIEW-L0-L1-20260806` 顶部直接选 L0。  
本次全站改：先选集群，再选该集群下的 L0；无 L0 时停在空态。  
须由体验 Owner 修订该 DEC 后，前端才能改选择器。本文件只锁数据侧：下拉源 = §3，查询键 = §4 展开结果。
