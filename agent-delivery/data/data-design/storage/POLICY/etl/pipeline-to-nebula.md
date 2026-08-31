# 管道 · → Nebula（政策投影一张 G）

```yaml
---
doc_id: POLICY-ETL-TO-NEBULA
element: POLICY
role: etl
status: as-built
version: "2026-08-31"
updated: 2026-08-31
task_id: DATA-POLICY-STORAGE-NEBULA-ETL-L01
asbuilt_from: POLICY-NEBULA-PROJECT-CHAIN-L01
---
```

> **本文件是 as-built 回填**，不是待施工设计。投影已由 B 叶落地并 `done`（commit `32124a0`，`demo-algo-ent-analysis` `origin/dev`）。
> 拓扑真源 [`../01-data-flow.md`](../01-data-flow.md) §3（**approved**）· 细表指针 [`../stores/nebula.md`](../stores/nebula.md)（draft）。
> 本叶只写文档：**不改代码、不 APPLY DDL、不灌数**。

## 1. 意图

政策点与政策边**增量投影**进产业链一张 G。`chain` / `segment` / `enterprise` / `institution` 复用 CHAIN 既有顶点，政策侧不复制底图本体、不另建 space。

## 2. 入口与源

| 项 | 值 |
|---|---|
| 仓 / 模块 | `demo-algo-ent-analysis` · `polan/graph/nebula_loader.py` |
| 入口 | `run()`；`python -m polan.graph.nebula_loader` |
| 源表 | `{ads}.policy_graph_node` · `{ads}.policy_graph_edge`（Demo = `demo_gkxlumenx_ads`） |
| 目标 | Nebula space **`demo_gkx_chain`** |
| 读路径 | `polan/graph/nebula_query.py` → `/v1/policy/graph` |

源是 **ADS 镜像**，不是 DWD 直读。镜像两表同时是 Nebula 不可用时的读兜底（见 [`../stores/mysql/ads.md`](../stores/mysql/ads.md)）。

## 3. Space 与 VID 约束（代码强制）

`polan/common/nebula.py` 把一张 G 写死为常量并在 `conf()` 校验，配置成别的 space 直接抛错：

| 项 | 值 | 违反后果 |
|---|---|---|
| space | 仅 `demo_gkx_chain` | `RuntimeError: 政策投影拒绝非一张 G space` |
| vid_length | 必须 `80` | `RuntimeError` |
| 正式图库 | `gkx_chain` | 本管线零写入 |
| 废作 | `gkx_policy` | 代码中无 `CREATE SPACE` / `DROP SPACE` |

VID：政策 `pol:{policy_id}`；既有实体沿用 `chain:` / `segment:` / `ent:` / `inst:` 前缀。超 80 字符的候选 VID 丢弃不投。

## 4. Schema 增量（`ensure_schema()`）

在**已存在**的 space 内 `USE` 后补增量，只 `IF NOT EXISTS`，随后 `DESCRIBE` 轮询至就绪（超时 40s 抛错）：

```ngql
CREATE TAG  IF NOT EXISTS policy   (name string, weight double, props string)
CREATE EDGE IF NOT EXISTS support  (weight double, props string)
CREATE EDGE IF NOT EXISTS apply_to (weight double, props string)
CREATE EDGE IF NOT EXISTS regulate (weight double, props string)
CREATE EDGE IF NOT EXISTS cite     (weight double, props string)
```

> ⚠️ **与 S3 文档不一致（待裁决）**：[`../stores/nebula.md`](../stores/nebula.md) 把四类边写成 `support(weight, factor_type, src_table)` / `apply_to(weight, src_table)` / `regulate(weight, src_table)` / `cite(relation, weight)`，与上表 as-built 的统一 `(weight double, props string)` 对不上。现网以 as-built 为准；S3 细表是否跟改属结构项，按 `01-data-flow.md` `OPEN-POLICY-GRAPH-03` 升级 `human:淮政玮`，**不在本叶静默改 S3**。

## 5. 挂接解析（对不齐则不上图）

既有实体必须经 `FETCH PROP ON *` 证明顶点真实存在才挂边，解析不到就计数跳过，**不按名称猜测**：

| 源 `node_type` | 取值字段（`props`） | 目标前缀 |
|---|---|---|
| `policy` | `node_key` | `pol:` |
| `industry` | `industry_link_code` | `chain:` / `segment:` |
| `enterprise` | `org_id` → `enterprise_code` → `entity_id` | `ent:` |
| `org` / `service` | `org_id` → `institution_id` → `entity_id` | `inst:` |
| 其余（含 `tech` / `talent`） | — | 本波不上图（`OPEN-POLICY-GRAPH-01`） |

`relation_type` 不在四类边内的一律跳过计数。边两端任一顶点未解析则整条丢弃。

## 6. 写入与幂等

`INSERT VERTEX` / `INSERT EDGE` 分类型批量提交，`chunk=100`。同 VID 重跑覆盖，可重复执行；本管线不做删除，**不清空既有底图**。

## 7. fail-soft 与开关

`available()` 轻量探活（未启用或 `USE` 失败即 False）。不可用时 `run_all` 跳过投影、`/v1/policy/graph` 回退 ADS/MySQL/SQLite 镜像，并把 `source` 诚实标成实际后端——**只有真实 nGQL 成功才返回 `source=nebula`**。

| 环境变量 | 作用 | 回退键 |
|---|---|---|
| `POLAN_NEBULA_ENABLED` | 投影/读图总开关 | settings `nebula.enabled` |
| `POLAN_NEBULA_HOSTS` | 图库地址 | `GKX_NEBULA_HOSTS` |
| `POLAN_NEBULA_USER` / `_PASSWORD` | 凭据 | `GKX_NEBULA_*` |
| `POLAN_NEBULA_SPACE` | space（只接受 `demo_gkx_chain`） | `GKX_NEBULA_SPACE` |
| `POLAN_GRAPH_BACKEND` | 读路径后端 `nebula` \| `pg` | `GKX_GRAPH_BACKEND` |

`POLAN_*` 与同 Pod 的 `ENTAN_NEBULA_SPACE=demo_entan` 隔离，避免共用 `GKX_NEBULA_SPACE` 串库。

## 8. 首轮实投影基线（2026-08-21）

| 项 | 值 |
|---|---|
| space | `demo_gkx_chain` |
| policy 顶点 | `47655` |
| 政策边 | `398` |
| 跳过 | industry `850` · enterprise `20` · org `574` · service `3` · talent `5` |
| 实调 | `GET /v1/policy/graph?limit=3` → 200，`source=nebula`，`nodes=24` `edges=22` |

跳过量大的原因：ADS 镜像 `props` 里多数产业/企业/机构缺稳定 ID，符合"对不齐则不上图"。**这是缺口不是故障**，改善路径见 `OPEN-POLICY-GRAPH-01`。

## 9. 禁止

Neo4j；Java 直连 nGQL；`CREATE SPACE gkx_policy`；写 `gkx_chain`；`DROP SPACE demo_gkx_chain`；新建 `org` / `industry` / `tech` / `talent` Tag；用名称相似度伪造挂接边。
