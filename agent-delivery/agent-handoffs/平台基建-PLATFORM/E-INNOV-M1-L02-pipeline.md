# E-INNOV-M1-L02 · innov-algo-demo（Python）跑通 P1–P4 流水线，innov 库 ADS 有数据

> agent: algorithm-agent · 2026-06-20

## 问题清单

- `demo-algo-science` 原为空仓，需从 `SZCGKX/innov-algo-demo` bootstrap。
- 本机（Windows 开发机）无法直连 MySQL `10.50.11.76:3306`（连接超时），流水线数据验证需在集群内或内网执行。
- GitLab Runner（tag `rag`）`py:smoke` 每次需 docker 内全量 `pip install`（含 scipy/OTel），耗时长；Pipeline #4121 在日志已输出 `SMOKE-OK` 后 job 仍 hung，已手动 cancel 并重触发 #4126。
- SSH MCP（K8s 节点）连接失败，无法从 agent 环境直接 `kubectl port-forward` 验证 dev `/internal/status` 与 Tempo。

## 修改内容

### Bootstrap（innov-algo-demo → demo-algo-science）

- 从 `https://gitlab.htmisoft.net/SZCGKX/innov-algo-demo.git` main 导入完整 P1–P9 流水线代码。
- 分支：`feat/E-INNOV-M1-L02`；首 commit 推送至 `gkx-lumen/demo-algo-science`。

### OTel 对齐 observability.md

| 项 | 实现 |
|----|------|
| 依赖 | `opentelemetry-distro`、`exporter-otlp-proto-http`、`instrumentation-fastapi/logging` |
| Dockerfile | `ENTRYPOINT ["opentelemetry-instrument"]` + `OTEL_SERVICE_NAME=gkx-innov-py` + Collector `:4318` |
| 日志 | `api/logging_config.py` JSON + `otelTraceID`/`otel_trace_id` 双字段 |
| 响应头 | `api/otel_middleware.py` 回传 `traceparent` + `X-Trace-Id` |

### /internal/status 增强

- 返回 `pipelines`（P1–P9 done/pending/running）与 `p1_p4_complete` 布尔值。
- 依据 `dim_org_master`、`dwd_event_std.produce_mode`（rule/nlp）、`ads_innovation_event` 等表行数推断完成态。

### CI 适配

- `py:image` / `deploy:innov-py` 增加 `feat/E-INNOV-M1-L02` 分支规则（dev 命名空间自动 deploy）。

## 测试结果

| 项 | 结果 | 证据 |
|----|------|------|
| 本地 import 冒烟 | ✅ `LOCAL-SMOKE-OK` | 全模块 `import` 通过（`OTEL_TRACES_EXPORTER=none`） |
| `scripts/run_all.py` 幂等 | ⏳ 待内网 MySQL | 本机连接 `10.50.11.76` 超时 |
| `ads_innovation_event` > 0 | ⏳ 待集群跑流水线 | Pod 启动 `INNOV_RUN_ON_START=1` 自动触发 |
| GET `/internal/status` P1–P4 | ⏳ 待集群验证 | API 已实现 `pipelines` + `p1_p4_complete` |
| CI `py:smoke` | 🟡 运行中 | Pipeline #4126 job log 正在 pip install |
| CI `py:image` | ⏳ 等待 smoke | — |
| `deploy:innov-py` dev rollout | ⏳ 等待 image | 依赖 `gkx-gkx-platform-innov-py` Deployment 已存在（demo-svc-platform helm） |
| dev `/internal/status` | ⏳ 阻塞 | 本机无法达 K8s 内网；SSH MCP 不可用 |
| Tempo `gkx-innov-py` trace | ⏳ 阻塞 | 需 deploy 完成后抽样 |

## 遗留风险

- **P5 仍为 networkx 内存图**（非 NebulaGraph），与 `graph-engine.md` 过渡说明一致，不在本 leaf 范围。
- CI Runner 慢/ hung 风险：建议 devops 为 `py:smoke` 预构建含依赖的 CI 基础镜像，或缓存 pip wheel。
- `deploy:innov-py` 前提：`gkx_service_demo` / `demo-svc-platform` helm 已创建 `gkx-gkx-platform-innov-py`；若 L02b 未完成，deploy 可能报 Deployment not found。

## CI/CD（必填）

| 字段 | 值 |
|------|-----|
| **branch** | `feat/E-INNOV-M1-L02` |
| **commit_sha** | `e9788ac0f74f914fc36dbdd1fe2258d2325fa33d` |
| **pipeline_url** | https://gitlab.htmisoft.net/gkx-lumen/demo-algo-science/-/pipelines/4126 （重跑；首跑 #4121 已 cancel） |
| **deploy_namespace** | `dev`（待 deploy job 完成） |
| **image_tag** | `e9788ac0`（`harbor.htmisoft.net/gkx/gkx-innov-py:e9788ac0`，待 py:image 成功） |
| **K8s rollout** | ⏳ 待 `deploy:innov-py` |
| **dev 测试** | 集群内：`kubectl -n dev port-forward svc/gkx-gkx-platform-innov-py 8000:8000` → `curl localhost:8000/internal/status` |

### test_result 摘要

```text
本地：LOCAL-SMOKE-OK（import 全模块）
CI #4126：py:smoke running（docker pip install 中）
CI #4121：py:smoke 日志 SMOKE-OK 后 runner hung → canceled
MySQL 流水线：本机 10.50.11.76:3306 超时，未执行 run_all.py
```

### trace_id_sample

```text
待 dev deploy 后执行：
  curl -sD - http://<innov-py>/healthz | grep -i traceparent
预期 OTEL_SERVICE_NAME=gkx-innov-py，Tempo 可搜 service.name
```

## 可观测性

- **OTEL_SERVICE_NAME**：`gkx-innov-py`（Dockerfile ENV）
- **OTLP**：`http://gkx-otel-collector:4318`（http/protobuf）
- **traceId（dev 抽样）**：待 deploy 后补录
- **Tempo / Loki**：待验证

## 架构合规自检

| 铁律 | 状态 |
|------|------|
| 算法只在 Python | ✅ |
| 仅 `/internal/*` 内部 API | ✅ |
| 禁止 Neo4j（P5 networkx 过渡） | ✅（已知缺口，Epic 后续） |
| OTel instrument + traceparent | ✅（代码/Dockerfile） |
| Java 不写 ADS | ✅（本任务不涉及 Java） |
| demo2 不 merge lumen | ✅ |

## 涉及文件

- `F:\gkx-lumen\repos\demo-algo-science\`（全仓 bootstrap）
- 关键：`docker/Dockerfile`、`api/main.py`、`api/otel_middleware.py`、`api/logging_config.py`、`requirements.txt`、`.gitlab-ci.yml`

## Cost 回填

| 字段 | 值 |
|------|-----|
| estimated_tokens | 800_000 |
| actual_tokens | 420_000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 3.20 |
| cost_warn | green |

## 阻塞项（需协调）

1. **本机网络**：无法达 `10.50.11.76` MySQL 与 K8s dev 网段 → 流水线数据与 `/internal/status` 验证需在内网/集群执行。
2. **CI Runner**：`py:smoke` 耗时长且 #4121 hung；#4126 重跑中，需 devops 关注 runner 健康。
3. **Deploy 前置**：`gkx-gkx-platform-innov-py` Deployment 需由 `demo-svc-platform` helm 或 L02b 创建。
4. **SSH MCP**：连接 K8s 节点失败，agent 无法代执行 `kubectl` 验证。

## 建议下一任务

- coordinator：Pipeline #4126 绿后确认 `deploy:innov-py` rollout → 补录 `trace_id_sample` → 本 task 升 `done`
- **L03** api-agent：待 L02 数据就绪后移植 `gkxlumen-innov`
