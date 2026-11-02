# NebulaGraph · 服务机构 hang（一张 G）

```yaml
---
doc_id: SVC-STORE-NEBULA
element: SVC
role: store-nebula
status: draft
version: "2026-08-19"
updated: "2026-11-02"
engine: nebula
s3_task: DATA-SVC-STORAGE-S3-L02
---
```

> **引擎**：仅 NebulaGraph；**禁止 Neo4j**；阶段 P：**Java 禁直连 nGQL**。  
> **一张 G（决策 #7）**：Demo **`demo_gkx_chain`**；正式 `gkx_chain`。服务机构**投影进这张底图**，不另起 space。  
> MySQL hang 记录：[`../mysql/dwd-svc.md`](../mysql/dwd-svc.md) `svc_org_graph_hang`。  
> **112/113 写入契约（步1）**：[`../../etl/pipeline-to-nebula.md`](../../etl/pipeline-to-nebula.md)（`diagram_id=SVC-GRAPH-TRIPLE`）。灌数路径**禁止**写本 hang / nGQL。

## 1. Space

| 属性 | 值 |
|---|---|
| Demo | **`demo_gkx_chain`**（写死） |
| 正式 | `gkx_chain`（本总控不写） |
| 禁止 | `gkx_service` / 第二张七要素图 |

## 2. Hang 约定

| 项 | 口径 |
|---|---|
| 机构键 | **`org_id`**（与 ODS / `svc_org_circle` 同一键） |
| 图键 | **`node_id`**；与 `org_id` 对齐 hang（决策 #7） |
| Tag | 建议复用底图 `institution`；若需区分，用属性 `role=service`，**不新建 space** |
| Edge | F-ALGO 再钉关系边类型（Q062）；本单不发明第二套边真源 |

图谱菜单（50100）写 hang，**不是**十模型。十模型结果回 ADS；必要时可加边，仍在 `demo_gkx_chain`。

2026-11-02：`demo_gkxlumenx_dwd.svc_org_graph_hang` 43296 行，space `demo_gkx_chain`，Tag `institution`，VID `institution:{org_id}`。ext 中 33861 行是机构到机构的 `participates`（`mapped_from=cooperation`）。`belongs_to` 与 `service_provide` 在这份 ext 里是 0。`service_provide` 不在本域允许边里，企业合作代码另写、点类型是 `service`。正式库 hang 0 行。graphd 超时，图库点数未闭合。不能把 hang 行数写成 Nebula 已写入。`gkxlumenx` 侧的图由 GDF 直写也不在范围内：GDF 不直写图库。

## 3. 读写（阶段 F）

| 写 | 读 |
|---|---|
| `demo-algo-ent-analysis`（F-ALGO；本单不跑） | 50100 图谱菜单；阶段 P 经 Java→Python |

失败：图可降级；**ADS 仍为指标权威**（流图 §1）。

## 4. 禁止

Neo4j；Java 直连；新建 `gkx_service`；把 ENT/CHAIN/SVC 建成三张图再「二期合并」；细表仅因流图会签标 approved。
