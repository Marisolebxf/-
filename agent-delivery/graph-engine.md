# 知识图谱引擎规范（NebulaGraph · 开发必遵）

> **原则**：七要素支持层及 innov 图谱 **统一使用 NebulaGraph**，**禁止** 新引入 Neo4j 运行时。
> **Demo 真源**：`E:\gkx_src\ent-analysis-demo`（已接入 dev Nebula；`gkx_demo_ui` GraphView 已联调）。
> **dev 环境**：graphd `192.168.88.43:9669`（见 ent-analysis `conf/settings.yaml`）。

---

## 1. 为何 NebulaGraph

| 项 | 说明 |
|----|------|
| 环境 | 开发/联调 Nebula 已部署，可直接 `USE space` |
| Demo 验证 | ent-analysis：灌数 → `/v1/graph` 子图 → 前端 `source:"nebula"` |
| 正式路线 | lumen 全要素图谱、innov P5 落图均对齐 Nebula，不再规划 Neo4j |

---

## 2. Demo 参考实现（ent-analysis-demo）

| 模块 | 路径 | 职责 |
|------|------|------|
| 配置 | `conf/settings.yaml` → `nebula:` | hosts、space、partition、vid_length |
| 客户端 | `entan/common/nebula.py` | 连接池、`available()`、nGQL、`backend()` |
| 灌数 | `entan/graph/nebula_loader.py` | Tag/Edge schema、PG→Nebula 全量/重建 |
| 查询 | `entan/graph/nebula_query.py` | `subgraph()`、`find_path()` 多跳子图 |
| 增量 | `entan/graph/incremental.py` | 增量 upsert |
| API | `api/main.py` → `/v1/graph` | 优先 Nebula，不可用回退 PG 镜像 |
| 流水线 | `scripts/run_all.py` → `load_nebula_safe` | 灌数失败告警不阻断 |
| 前端 | `gkx_demo_ui/.../GraphView.vue` | 展示 `source: nebula \| pg` |

**API 响应约定**（所有图谱 REST **必须** 带 `source` 字段）：

```json
{
  "nodes": [],
  "edges": [],
  "source": "nebula"
}
```

`source` 取值：`nebula` | `pg`（PG 兜底）| `error`。

---

## 3. lumen 平台约定

### 3.1 Space 规划（按要素/业务域）

| Space | 用途 | 状态 |
|-------|------|------|
| `entan` | 企业分析 demo / E1 企业图谱 | demo 已有 |
| `gkx_policy` | E7 政策要素图谱 | Wave1 待建 |
| `gkx_innov` | innov P5 创新落图 | 待从 networkx 迁移 |
| `gkx_topic` | 七要素全量汇总（可选二期） | 待规划 |

### 3.2 环境变量（K8s / 本地）

```text
GKX_NEBULA_HOSTS=192.168.88.43:9669
GKX_NEBULA_USER=root
GKX_NEBULA_PASSWORD=
GKX_NEBULA_SPACE=gkx_policy          # 按服务/要素切换
GKX_GRAPH_BACKEND=nebula             # nebula | pg
```

各 Python 仓可保留服务前缀（如 `ENTAN_NEBULA_*`），语义与 `GKX_NEBULA_*` 一致。

### 3.3 Python 依赖

```text
nebula3-python>=3.4,<3.9
```

启动仍用 `opentelemetry-instrument`（见 `observability.md`）。

### 3.4 Java 层

- **禁止** 在 Java 内嵌 Cypher/nGQL 直连图库（除极少数运维工具）。
- Java `gkxlumen-topic` 通过 Feign 调 Python `/internal/graph/*` 或已有 `/v1/graph` 形态。
- 响应头继续回传 `traceparent` / `X-Trace-Id`。

### 3.5 PG 兜底

与 demo 一致：Nebula 不可用时读 PG 镜像（1 跳简化子图），保证页面可演示；handoff 须注明当前 `source`。

---

## 4. innov-algo-demo 迁移说明

| 现状 | 目标 |
|------|------|
| P5 使用 networkx 内存图 + dwm 快照 | 正式化写入 **NebulaGraph** space `gkx_innov` |
| README 仍写 Neo4j | 实现与文档改为 Nebula；参考 ent-analysis `nebula_loader` |

---

## 5. Agent 纪律

| Agent | 要求 |
|-------|------|
| **algorithm-agent** | 新图谱代码用 nebula3-python + nGQL；复用 loader/query 模式 |
| **api-agent** | REST 返回含 `source`；不新增 Neo4j 驱动依赖 |
| **devops-agent** | Helm/CI 注入 `GKX_NEBULA_*`；dev 集群 graphd 可达 |
| **frontend-agent** | 图谱组件展示数据源标签（参考 GraphView.vue） |
| **qa-agent** | 验收：`source:"nebula"` 且 dev 子图节点 > 0 |

---

## 6. 禁止项

- 新业务 Pod / 新 Epic 引入 Neo4j 驱动或 Neo4j 专用 Helm chart
- 概要设计原文中的「Neo4j」在 **lumen 实现** 时一律按本文 NebulaGraph 落地（设计文档未改版前以本规范为准）

---

## 7. 关联任务

| 任务 | 内容 |
|------|------|
| E-PLATFORM-P0-L03 | 平台图谱引擎脚手架（Nebula） |
| E-E7-POLICY-M1-L02 | 政策子图灌入 `gkx_policy` |
| E-INNOV-M1 后续 / innov P5 | networkx → Nebula `gkx_innov` |

---

## 8. 关联文档

| 文档 | 说明 |
|------|------|
| `agent-delivery/数据库设计.md` | RDBMS schema 总纲；`graph_node`/`graph_edge` PG 镜像 |
| `ent-analysis-demo/scripts/schema_ads.sql` | 图谱 PG 镜像 DDL 样例 |
