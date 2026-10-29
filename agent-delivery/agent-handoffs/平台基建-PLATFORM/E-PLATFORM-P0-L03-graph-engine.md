# Algorithm handoff · E-PLATFORM-P0-L03 图谱引擎 NebulaGraph

| 项 | 值 |
|---|---|
| 任务 | E-PLATFORM-P0-L03 |
| Epic | E-PLATFORM-P0 |
| 角色 | algorithm-agent |
| 仓 | `F:/gkx-lumen/repos/demo-algo-ent-analysis` |
| 分支 | `feat/E-PLATFORM-P0-L03` |
| Bootstrap 源 | `https://gitlab.htmisoft.net/SZCGKX/ent-analysis-demo.git` |
| 日期 | 2026-06-20 |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 产物 |
|--------|------|------|
| 对齐 ent-analysis-demo nebula_loader / nebula_query / nebula.py | ✅ | `entan/common/nebula.py`、`entan/graph/nebula_loader.py`、`entan/graph/nebula_query.py`（自 demo bootstrap） |
| dev graphd 10.50.75.136:9669；space schema 文档化 | ✅ | `conf/settings.yaml` + `docs/nebula-space-schema.md` |
| POST `/internal/graph/subgraph` → nodes/edges + source:nebula | ✅ | `api/main.py` |
| PG 兜底 source:pg | ✅ | Nebula 不可用或 backend=pg 时读 `ads.graph_node/edge` |
| opentelemetry-instrument + OTLP :4318 | ✅ | `docker/Dockerfile`、`api/otel_middleware.py`、`api/logging_config.py`、`requirements.txt` |
| push → py:smoke 绿 | 🟡 | 本地 `SMOKE-OK`；待 push 后 GitLab CI 确认 |

## 产物清单

### demo-algo-ent-analysis（bootstrap + 增量）

| 路径 | 说明 |
|------|------|
| `entan/common/nebula.py` | Nebula 连接池；支持 `GKX_NEBULA_*` / `ENTAN_NEBULA_*` |
| `entan/graph/nebula_loader.py` | Tag/Edge schema + PG→Nebula 灌数 |
| `entan/graph/nebula_query.py` | `subgraph()` / `find_path()` |
| `api/main.py` | `POST /internal/graph/subgraph` + 保留 `/v1/graph` |
| `api/otel_middleware.py` | traceparent / X-Trace-Id 响应头 |
| `api/logging_config.py` | JSON 日志 + OTel trace 关联 |
| `docs/nebula-space-schema.md` | space `entan` Tag/Edge 文档 |
| `docker/Dockerfile` | `opentelemetry-instrument` + OTLP env |
| `.gitlab-ci.yml` | `py:smoke`；feat 分支可 package |

### 内部 API 契约

**POST** `/internal/graph/subgraph`

```json
// 请求
{
  "center": 10,
  "center_ids": [10, 20],
  "centers": "10,20",
  "steps": 1,
  "limit": 80
}

// 响应（无 code 包络，供 Java Feign）
{
  "nodes": [...],
  "edges": [...],
  "source": "nebula",
  "centers": [10],
  "steps": 1
}
```

`source`：`nebula` | `pg`

## Nebula 环境

| 项 | 值 |
|----|-----|
| graphd | `10.50.75.136:9669` |
| space | `entan` |
| user | `root` / 空密码 |

```text
GKX_NEBULA_HOSTS=10.50.75.136:9669
GKX_NEBULA_SPACE=entan
GKX_GRAPH_BACKEND=nebula
```

灌数：`python -m entan.graph.nebula_loader` 或流水线 `load_nebula_safe`

## 可观测性

- service.name：`gkx-entan-py`（`OTEL_SERVICE_NAME`）
- 启动：`opentelemetry-instrument uvicorn api.main:app`
- Collector：`OTEL_EXPORTER_OTLP_ENDPOINT=http://gkx-otel-collector:4318`
- 响应头：`traceparent`、`X-Trace-Id`
- 本地 agent 环境：Nebula/PG 外网不可达，未采 dev traceId

## 架构合规自检（§2 十条）

| # | 项 | 结果 |
|---|-----|------|
| 1 | 算法只在 Python | ✅ nGQL 仅在 Python |
| 2 | 调用链 | ✅ `/internal/*` 供 Java Feign |
| 3 | NebulaGraph | ✅ nebula3-python；禁 Neo4j |
| 4 | 可观测性 | ✅ OTel instrument + middleware |
| 5 | CI/CD | 🟡 push 后待 py:smoke 绿 |
| 8 | PG 兜底 + source 字段 | ✅ |
| 10 | D9 血缘 | N/A（图谱节点 props 沿用 demo PG 镜像） |

## Convoy 隔离

- **ENT-PY-ALGO**：P0-L04（model registry）排在本任务之后，勿并行改同仓同文件
- P0-L04 预期改：`cfg_model_registry`、GET `/internal/models/registry`（与图谱模块无重叠）

## 阻塞项

| 项 | 说明 | Owner |
|----|------|-------|
| 本地 Nebula 连通 | agent 执行环境无法访问 `10.50.75.136:9669`（超时）；dev K8s / 内网需验收 `source:nebula` | devops / qa |
| CI py:smoke | 待 `feat/E-PLATFORM-P0-L03` push 后 GitLab _runner 确认 | coordinator |
| entan-py Deployment | 镜像 build 依赖 helm 已创建 `gkx-gkx-platform-entan-py`（deploy job） | devops P0-L06 |

## 接力清单

| 下游 | 动作 |
|------|------|
| **algorithm-agent P0-L04** | `cfg_model_registry` + GET `/internal/models/registry` |
| **api-agent P0-L05** | gkxlumen-topic Feign 调 `/internal/graph/subgraph` |
| **qa-agent** | dev 子图 `source:nebula` 且 nodes > 0 |
| **devops-agent P0-L06** | entan-py 镜像 rollout + Tempo trace |

## cost

| 字段 | 值 |
|------|-----|
| model_used | claude-sonnet-4.5 |
| actual_tokens | （session 回填） |
| actual_cost | （session 回填） |
| cost_warn | green |
