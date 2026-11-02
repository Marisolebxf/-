# 服务机构维存储 · 上下文与铁律

```yaml
---
doc_id: SVC-STORAGE-CONTEXT
element: SVC
role: context
status: draft
version: "2026-11-02"
updated: 2026-11-02
signoff_owner: human:淮政玮
task_id: ARCH-SVC-STORAGE-S1-L02
---
```

> **本单不建表、不灌数、不写 DDL。** 流图会签见 [`01-data-flow.md`](./01-data-flow.md)（`signoff_status=approved` · Owner `human:淮政玮` · 2026-08-19）。

## 1. Data Product 边界

- **域**：服务机构维（SVC / 科技专题 · 产业服务链分析相关存储）
- **内**：圈定后的服务机构 DWD/ADS、模型回写表、图谱 hang（同一张 `demo_gkx_chain`）、本域 MinIO 对象前缀
- **外**：功能设计 / USM / 50100 页面实现；机构**主体属性**权威在 ENT，本域不平行建 `svc_org_base`
- **阶段 F（本总控）写库**：`demo-algo-ent-analysis`（50100「产业服务算法库」灌数据/运行触发）
- **阶段 F 不碰**：`lumen-topic-py` / `lumen-algo-py` / `lumen-svc-platform` / `lumen-ui-topic`（留给下一份 P 总控）

## 2. 铁律（存储视角）

1. **阶段 F 算法台**：50100 → `demo-algo-ent-analysis` `/entan/internal/svc/*` → 只写 `demo_gkxlumenx_*`。这是联调台惯例（同 ENT 算法库），**不是**产品调用链。
2. **阶段 P（未授权，图中虚线）**：前端 → Java → Python `/internal/*`；Java **只读 ADS**；不扫 ODS/DWD；不直连 nGQL。D12：lumen 不调 `demo-*`。
3. 图谱 = **NebulaGraph** 一张 G：Demo `demo_gkx_chain`（决策 #7）。禁止 Neo4j；禁止平行 `gkx_service` space。
4. 关系库 = **MySQL**；禁止 PostgreSQL 叙述。
5. 主体 hang ENT `org_id`；禁复制 `dwd_org_base_info` 全列；禁 `SELECT enterprise_*` 当服务机构主路径。
6. 圈定 Demo 临时规则 `svc_rule_demo_kw_v1`；Q-SVC-010 🟡 不伪闭合 live。
7. 三方源变更不传导 ADS 契约面（D7）。

## 3. 与 ENT / CHAIN

| 关系 | 约定 |
|------|------|
| ENT | 机构主数据权威；SVC 只 hang `org_id` |
| CHAIN | `storage/CHAIN` / `gkxlumen-topic-chain` / `industry-center` **不动** |
| 图 | 服务机构节点/边投影进同一张 `demo_gkx_chain`，不另起 SVC 图 |

## 4. Demo / Mock

- **灌数真源**：只认 50100「基础指标」灌数据按钮（`append`/`replace`）；CLI/`svcseed` 为同一引擎。
- **主路径**：共用已有 `demo_gkxlumenx_ods`（不新建 ODS 实例、不 DROP 约定 33 表）→ 模拟 GDF → SVC DWD → ADS / 图 hang。
- **fixture 24 家**旁路，不得当退出门。
- **结构**与正式共用 `stores/`（S3 draft · `DATA-SVC-STORAGE-S3-L02`）。

## 5. 下一步

1. [`01-data-flow.md`](./01-data-flow.md) 已由 **`human:淮政玮` 会签**（2026-08-19 `approved`）  
2. S2 指针 + S3 细表 draft 已落盘。  
3. **S4 入口已加回**（`DATA-SVC-STORAGE-S4-L02`）。**缺口文档已补**（`DATA-SVC-STORAGE-GAP-L02`：列对照 / 词表 / MinIO / 矩阵血缘）。  
4. F-SEED / F-ALGO 已在 50100 出数。F-GATE 切法 A 见 [`formula-freeze-cut-a.md`](./formula-freeze-cut-a.md)。**不开 50892 / P 总控**，不重签本会签流图。

## 6. 2026-11-02 现网对照（不改上面的铁律）

铁律仍是设计边界。现网已经长出设计当时写成「阶段 F 不碰」的读路径和旁路。事实写在 [`02-asbuilt-process-chain.md`](./02-asbuilt-process-chain.md)，这里只钉和本节冲突的四点：

| 本节原文 | 2026-11-02 看到的 |
|---|---|
| 阶段 F 不碰 `lumen-topic-py` / `lumen-algo-py` / `lumen-svc-platform` / `lumen-ui-topic` | `lumen-topic-py` 只读 `demo_gkxlumenx_*`。`lumen-svc-platform` 的内容运营写 `gkxlumenx_cms`，不写 ADS。ES 同步在 `lumen-etl-es-py`（不在这四仓名单里），别名 `gkx_svc_org` 已有 43296 篇 |
| 灌数真源只认 50100 按钮 | 同一引擎还有 `POST /internal/svc/run-pipeline` 与 `python -m entan.svcseed`。L01 核对到的批次没有单独证明来自按钮。仓库里未见定时任务 |
| 主路径写成 ODS → 模拟 GDF → DWD → ADS / 图 | demo 上是 Python 直接写。GDF 作业未建。图谱和十模型不是同一次 pipeline |
| 只写 `demo_gkxlumenx_*` | 代码仍拒绝写正式 DWD/ADS。正式库同名表已建且 0 行。谁建的，未闭合 |

图库行数未闭合。正式库 0 行不是产线已跑通。  
