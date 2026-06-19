# 可观测性规范（全栈 · 开发必遵）

> **原则**：所有 lumen 正式开发 **必须** 继承 demo 仓已验证的 OTel 方案；新功能不得破坏「指标 → 链路 → 日志」三联查。
> **Demo 真源**：`E:\gkx_src\gkx_service_demo`（Java + Helm 基础设施）、`gkx_demo_python`（Python）、`gkx_demo_ui` / `gkx_lumen_fronted_pc`（前端深链）。
> **图谱引擎**：NebulaGraph（`ent-analysis-demo`）；见 `graph-engine.md`。

---

## 1. 目标架构（与 demo 一致）

```text
Java 微服务 (Spring Boot)
  ↓
OTel JavaAgent
  - 自动埋点（HTTP / DB / Redis / Feign 等）
  - 注入日志上下文（trace_id / span_id）
  - 网关回传 trace 到响应头（traceparent / X-Trace-Id）
  ↓ OTLP HTTP (:4318)
OTel Collector（统一接收）
  ├─ Trace  → Tempo
  ├─ Metric → Prometheus
  └─ Log    → Loki
  ↓
Grafana（指标 → 链路 → 日志 三联查）

Python 算法服务 (FastAPI / uvicorn)
  ↓
opentelemetry-instrument（零代码，对标 Java -javaagent）
  ↓ 同一 Collector（OTLP HTTP）
  └─ 同上 Tempo / Prometheus / Loki / Grafana

前端 (Vue)
  ↓
observability.ts
  - parseTraceparent / extractTraceId
  - buildTempoExploreUrl / buildLokiExploreUrl
  - VITE_GRAFANA_* 环境变量
  ↓
axios 拦截器：错误提示附 traceId + 可选 Grafana 深链
```

详细方案文档（demo 仓，移植 lumen 时随代码一并参考）：

| 文档 | 路径 |
|------|------|
| 总体方案 | `gkx_service_demo/OTEL_OBSERVABILITY_PLAN.md` |
| Java 接入 | `gkx_service_demo/OTEL_APP_DEV_IMPLEMENTATION.md` |
| 运维交付 | `gkx_service_demo/OTEL_INFRA_OPS_HANDOFF.md` |
| Python 示例 | `gkx_demo_python/README.md` |

---

## 2. Java（gkx_lumen_backend / gkxlumen-*）

### 2.1 必做项（从 gkx_service_demo 复制）

| 项 | Demo 参考 |
|----|-----------|
| JavaAgent 制品 | `scripts/download-otel-agent.sh` + `docker/otel/opentelemetry-javaagent.jar` |
| Dockerfile | `-javaagent:/otel/opentelemetry-javaagent.jar` |
| CI | `.gitlab-ci.yml` package 前执行 `download-otel-agent.sh` |
| 环境变量 | `OTEL_EXPORTER_OTLP_ENDPOINT=http://…:4318`（Collector Gateway） |
| | `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf` |
| | `OTEL_TRACES/METRICS/LOGS_EXPORTER=otlp` |
| | `OTEL_SERVICE_NAME=<spring.application.name>` |
| 网关 | `GkxRequestGlobalFilter` 回传 `traceparent` + `X-Trace-Id` |
| | `Access-Control-Expose-Headers` 放行上述头（前端可读） |
| 日志 | JSON 结构化，含 `trace_id` / `span_id` |

### 2.2 禁止

- Micrometer Tracing 与 JavaAgent **双导出**（见 `OTEL_APP_DEV_IMPLEMENTATION.md` §7）
- 业务 Pod 直连 Tempo / Prometheus / Loki
- 新微服务镜像 **不带** JavaAgent

### 2.3 Helm / K8s

基础设施 chart 参考 `gkx_service_demo/helm/gkx-platform`：

- `otel-collector.yaml`、`tempo.yaml`、Loki、MinIO bucket
- 各 Deployment 注入 `OTEL_*` env（values.yaml 中 `otelCollector` 段）

---

## 3. Python（innov-algo-demo → lumen 正式化时必补）

**现状**：`innov-algo-demo` Dockerfile 仍为裸 `uvicorn`，**需对齐** `gkx_demo_python`。

### 3.1 必做项

| 项 | 参考 `gkx_demo_python` |
|----|------------------------|
| 依赖 | `opentelemetry-distro`、`exporter-otlp-proto-http`、fastapi/logging instrumentation |
| 启动 | `ENTRYPOINT ["opentelemetry-instrument", "uvicorn", …]` |
| 环境变量 | 与 Java 相同 Collector endpoint（`:4318` HTTP） |
| 日志 | `logging_config.py` JSON + `otelTraceID` / `otel_trace_id` 双字段兼容 |
| 响应头 | 中间件回传 `traceparent` + `X-Trace-Id`（见 `api.py`） |
| 本地测试 | `OTEL_TRACES_EXPORTER=none` 可关上报（见 `test/test_api.py`） |

### 3.2 禁止

- 生产路径下裸 `uvicorn` 无 OTel 包装
- 业务代码重复手动埋点整套 HTTP（Agent 已覆盖的不要再包一层）

---

## 4. 前端（gkx_lumen_fronted_pc / mobile）

### 4.1 必做项

| 项 | 参考 |
|----|------|
| 工具模块 | `src/utils/observability.ts` |
| 请求拦截 | `src/utils/request.ts` 中 `extractTraceId`，错误信息附 traceId |
| 环境变量 | `VITE_GRAFANA_BASE_URL`、`VITE_GRAFANA_TEMPO_DS`、`VITE_GRAFANA_LOKI_DS` |
| 降级 | 未配置 Grafana URL 时深链返回 null，不阻塞业务 |

`gkx_lumen_fronted_pc` **已具备** observability.ts；新页面/新 API 错误处理 **必须** 沿用该模式。

### 4.2 联调验收

1. 触发一次失败请求，浏览器 Network 可见 `traceparent` / `X-Trace-Id`
2. 控制台或 UI 可复制 traceId
3. Grafana Tempo Explore 能搜到完整链路（Java → Python 跨服务若已调用）

---

## 5. Agent 开发纪律

| Agent | 可观测性要求 |
|-------|-------------|
| **api-agent** | 新 Java 模块：Dockerfile + OTEL env + 网关头；不引入双导出 |
| **algorithm-agent** | Python 服务：`opentelemetry-instrument` + 响应头；对齐 gkx_demo_python |
| **frontend-agent** | 新 API 走 request 拦截器；保留 traceId 展示/深链 |
| **devops-agent** | Helm/CI 含 otel agent 下载、Collector 路由、OTEL_* 注入 |
| **integration-agent** | 跨服务调用后 Tempo 可见连续 trace |
| **qa-agent** | 验收项含：Tempo 有 span、Loki 可按 traceId 搜日志 |

每个 handoff **建议** 增加：

```markdown
## 可观测性
- service.name：
- 抽样 traceId（dev 实测）：
- Tempo 链路：有 / 无
- Loki 日志关联：有 / 无
```

---

## 6. 与 CI/CD 的关系

- Java CI **package 阶段** 必须能拿到 `opentelemetry-javaagent.jar`（见 `gkx_service_demo/.gitlab-ci.yml`）
- 部署 dev 后，**DoD 之一**：在 Grafana 能看到新服务名的 trace（非仅 localhost 日志）

---

## 7. 待办（已知缺口）

| 项 | 状态 | 负责 Epic |
|----|------|-----------|
| `innov-algo-demo` 加 OTel instrument | 待做 | E-INNOV-M1 或 L02 子项 |
| `innov-algo-demo` P5 networkx → NebulaGraph | 待做 | graph-engine.md §4 |
| `gkx_lumen_backend` 移植 JavaAgent + Helm OTEL | 待做 | E-INNOV-M1-L02b |
| `gkxlumen-innov` 注册 `OTEL_SERVICE_NAME=gkxlumen-innov` | 待做 | L03 |

---

## 8. 环境变量速查（dev 默认）

```text
OTEL_EXPORTER_OTLP_ENDPOINT=http://gkx-otel-collector:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_TRACES_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
OTEL_METRIC_EXPORT_INTERVAL=60000
OTEL_PYTHON_LOG_CORRELATION=true   # Python only
```

Grafana（前端 `.env.development`）：

```text
VITE_GRAFANA_BASE_URL=http://192.168.88.34:3000
VITE_GRAFANA_TEMPO_DS=Tempo
VITE_GRAFANA_LOKI_DS=Loki
```
