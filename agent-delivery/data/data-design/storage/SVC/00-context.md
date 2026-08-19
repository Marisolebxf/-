# 服务机构维存储 · 上下文与铁律

```yaml
---
doc_id: SVC-STORAGE-CONTEXT
element: SVC
role: context
status: draft
version: "2026-08-19"
updated: 2026-08-19
signoff_owner: human:淮政玮
task_id: ARCH-SVC-STORAGE-S1-L02
---
```

> **本单不建表、不灌数、不写 DDL。** 流图会签见 [`01-data-flow.md`](./01-data-flow.md)（`signoff_status=pending` · Owner `human:淮政玮`）。

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
- **结构**与正式共用未来 `stores/`（S3）；本单不写细表。

## 5. 下一步

1. [`01-data-flow.md`](./01-data-flow.md) 待 **`human:淮政玮` 会签**  
2. 会签 `approved` 后才开 S2（sources/etl）/ S3（细表）/ F-SEED  
