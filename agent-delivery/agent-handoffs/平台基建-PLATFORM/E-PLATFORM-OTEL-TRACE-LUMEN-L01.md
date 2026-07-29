# Handoff · E-PLATFORM-OTEL-TRACE-LUMEN-L01  
# lumen 网关 / 展示 PC 对齐 system-test 的 trace-id 串联

| 项 | 值 |
|---|---|
| 任务 | `E-PLATFORM-OTEL-TRACE-LUMEN-L01` |
| Epic | `E-PLATFORM` |
| 角色 | `agent:api-agent` + `agent:frontend-agent` |
| 监管 | `human:淮政玮` |
| 日期 | 2026-07-30 |
| 状态 | `review`（代码已 push；**CI/CD 与 Tempo 三联查由监管人执行**） |
| 规范真源 | `agent-delivery/observability.md` · demo `GkxRequestGlobalFilter` · `demo-ui-system-test` 首页 |

---

## 1. 交付结论

将 system-test「功能 Demo」的跨语言 trace 契约移植到 lumen 正式链路（以科技新闻抽取为试点验收面）：

| 层 | 变更 | Commit |
|----|------|--------|
| **网关** `gkxlumen-gateway` | `GkxlumenRequestGlobalFilter` 回传 `traceparent` + `X-Trace-Id`，并合并 `Access-Control-Expose-Headers`（对齐 demo） | `lumen-svc-platform` **`9eadddd`** |
| **innov** `TechNewsExtractService` | extract / entity-extract 入口 `log.info` 打印 `Span.current()` traceId | 同上 **`9eadddd`** |
| **展示 PC** | `request.ts` 成功/失败挂不可枚举 `__traceId`；tech-news 页展示 traceId + Tempo/Loki 深链；生产关 Mock 登录（`VITE_ENABLE_MOCK_AUTH=false`） | `lumen-ui-science-pc` **`cdba193`** |

依赖：`opentelemetry-api:1.51.0`（`provided`，与 JavaAgent 一致）已写入 gateway / innov `pom.xml`。

---

## 2. 目标调用链（对齐 system-test）

```text
FE (lumen-ui-science-pc)
  → Gateway (StripPrefix + OTel server span + 响应头回传)
  → gkxlumen-innov (RestTemplate；Agent 注入出站 traceparent)
  → demo-algo-science (opentelemetry-instrument + TraceHeaderMiddleware)
```

验收时同一 `traceId` 应在 Tempo 中覆盖：`gkxlumen-gateway` → `gkxlumen-innov` → Python service（`OTEL_SERVICE_NAME` 以 K8s 为准）。

---

## 3. 产物清单

| 路径 | 说明 |
|------|------|
| `gkxlumen-gateway/.../GkxlumenRequestGlobalFilter.java` | trace 响应头注入 |
| `gkxlumen-gateway/pom.xml` | otel-api provided |
| `gkxlumen-innov/.../TechNewsExtractService.java` | 抽取路径日志含 traceId |
| `gkxlumen-innov/pom.xml` | otel-api provided |
| `lumen-ui-science-pc/src/utils/request.ts` | `__traceId` 约定 |
| `lumen-ui-science-pc/src/views/tech-news/index.vue` | UI 展示 + 深链 |
| `lumen-ui-science-pc/.env.production` | `VITE_ENABLE_MOCK_AUTH=false` |

---

## 4. 监管人待执行（CI/CD + 验收）

1. 跑通 / 确认 Pipeline：
   - UI：`https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-science-pc/-/pipelines`（sha `cdba193`）
   - SVC：`https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines`（sha `9eadddd`，需 gateway + innov 镜像滚动）
2. **真登录**（勿再用 `admin-mock-token`）后打开科技新闻复核页，点「抽取」
3. Network：响应头含 `traceparent`、`X-Trace-Id`
4. 页面可复制 traceId；Tempo / Loki 深链可开
5. Tempo：同一 trace 含 gateway → innov → Python 三段

### 已知前置问题（不在本单扩白名单）

- 关 Mock 后若未真登录，抽取仍会 **424 / 用户凭证已过期**
- Mock token 误带 `Authorization` 的处理方式：见后续任务 **`FE-SCIENCE-PC-TOKEN-ALIGN-L01`**（对齐 `lumen-ui-topic` 的 `shouldAttachBearerToken`）

### Grafana 数据源（2026-07-30 补齐）

| 名称 | URL | 说明 |
|------|-----|------|
| `Tempo` | `http://192.168.88.50:30201` | **lumen** 主源（已从 demo 切过来） |
| `Loki` | `http://192.168.88.50:30311` | **lumen** 主源 |
| `Tempo-Lumen` / `Loki-Lumen` | 同上 | 别名，与主源等价 |
| `Tempo-Demo` | `http://192.168.88.50:30200` | **demo** / system-test |
| `Loki-Demo` | `http://192.168.88.50:30310` | **demo** / system-test |

science-pc：`VITE_GRAFANA_TEMPO_DS=Tempo` / `Loki`。system-test：`Tempo-Demo` / `Loki-Demo`。Explore 选对应源即可。

---

## 5. 架构合规自检

| 铁律 | 状态 |
|------|------|
| D1 算法只在 Python | ✅ 未改算法 |
| D2 调用链 FE→Java→Python | ✅ |
| D4 可观测性 | ✅ 网关头 + FE `__traceId` + innov 日志；Tempo 待监管人补验 |
| D5 CI/CD | 🟡 监管人执行中 |
| D8 Design.md | N/A（可观测基建） |
| D9 血缘 | N/A |

---

## 6. Cost（估）

| 字段 | 值 |
|------|-----|
| `model_used` | cursor-grok-4.5 |
| `actual_tokens` | ~120000（估） |
| `actual_cost` | ~0.80 |
| `cost_warn` | green |

---

## 7. 下一任务

- **`FE-SCIENCE-PC-TOKEN-ALIGN-L01`**：参考 `lumen-ui-topic` token 处理，修复 science-pc 在 Mock/真网关混用下误带 Bearer 导致 424 的问题。
