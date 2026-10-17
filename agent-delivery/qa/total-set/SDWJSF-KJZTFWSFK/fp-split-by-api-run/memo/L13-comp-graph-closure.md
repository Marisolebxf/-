# L13 产业全要素图谱 API 封闭清单（`comp.graph`）

**2026-10-17 更正**：L13 六级 =「产业全要素图谱API服务开发」，仅挂 **`comp.graph`**（与 apiview「产业全要素图谱 API」下拉一致）。  
旧版 `L13-graph-endpoint-closure.md`（chain/entan/policy/svc 30 endpoint）**作废**；构建类契约见 L05–L12 方案 A 分挂。

| endpoint_id | title | METHOD | path | catalog_status |
|---|---|---|---|---|
| `comp.graph.browse` | D 浏览 COMP_GRAPH_BROWSE | GET | `/industry-comp/v1/comp/graph` | live |
| `comp.graph.entities` | 实体检索 COMP_ENTITY_SEARCH | GET | `/industry-comp/v1/comp/graph/entities` | live |
| `comp.graph.relations` | 关系查询 COMP_REL_QUERY | GET | `/industry-comp/v1/comp/graph/relations` | live |
| `comp.graph.viz` | 可视化 COMP_GRAPH_VIZ | GET | `/industry-comp/v1/comp/graph/viz` | live |
| `comp.graph.similar` | 语义相似 COMP_SEMANTIC_SIM | POST | `/industry-comp/v1/comp/graph/similar` | live |
| `comp.graph.metrics` | 网络指标 COMP_NETWORK_METRIC | GET | `/industry-comp/v1/comp/graph/metrics` | live |

真源：`lumen-ui-algo-apiview/src/catalog/comp.json` · 页 `comp.graph`。

## L05–L12 构建页分挂（方案 A · 3c）

| 六级 | 主挂 endpoint（全库 field 行归属） |
|---|---|
| L05 | `chain.panorama.ops` |
| L06 | req_only（写入契约见 L05） |
| L07 | `policy.graph.ner`、`policy.graph.main` |
| L08 | `policy.graph.intra`、`policy.graph.hang-*` |
| L09 | `entan.graph.ner`、`entan.graph.main` |
| L10 | `entan.graph.intra-*`、`entan.graph.hang-*` |
| L11 | `svc.graph.ner`、`svc.graph.main` |
| L12 | `svc.graph.intra`、`svc.graph.hang-*` |
| L14 | `chain.panorama.main`（ops 不在 L14，见 L05） |
