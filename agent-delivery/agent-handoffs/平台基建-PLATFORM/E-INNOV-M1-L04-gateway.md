# Gateway handoff · E-INNOV-M1-L04 `/innov/**` 路由 + Helm 启用

| 项 | 值 |
|---|---|
| 任务 | E-INNOV-M1-L04 |
| Epic | E-INNOV-M1 |
| 角色 | integration-agent |
| 仓 | `F:/gkx-lumen/repos/lumen-svc-platform` |
| 分支 | `feat/E-INNOV-M1-L04` |
| 基线 | `feat/E-INNOV-M1-L03`（含 L02b Helm/网关种子） |
| 日期 | 2026-06-20 |
| Pipeline | **deferred** — 见 `PIPELINE-WAIVER-2026-06-20.md` v2 |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 说明 |
|--------|------|------|
| gkxlumen-gateway 路由含 `gkxlumen-innov` `/innov/**` | ✅ | `helm/gkxlumen-platform/configs/gkxlumen-gateway-dev.yml`：`Path=/innov/**` → `lb://gkxlumen-innov`，`StripPrefix=1` |
| helm 启用 `microservices.innov` | ✅ | `values-lumen.yaml` → `innov: { enabled: true }`；`values.yaml` 保留完整 env（含 `OTEL_SERVICE_NAME=gkxlumen-innov`、innov 库连接） |
| helm/kubectl dev rollout | 🟡 **deferred** | PM waiver v2：不阻塞本任务签收 |
| curl `/innov/v1/meta/data-status` code=0 | 🟡 **deferred** | 待 devops/qa 补验（需镜像 `gkxlumen-innov` + rollout 后） |

## 路由契约

| 外部（经网关） | 内部（gkxlumen-innov） | 说明 |
|----------------|------------------------|------|
| `GET /innov/v1/meta/data-status` | `GET /v1/meta/data-status` | StripPrefix=1 剥 `/innov` |
| `GET /innov/v1/events` | `GET /v1/events` | M1 事件 API（L05 qa 全套测试） |

Nacos 服务名：`gkxlumen-innov`（与 `SPRING_APPLICATION_NAME` / gateway `lb://` 一致）。

## 产物清单

| 路径 | 说明 |
|------|------|
| `helm/gkxlumen-platform/configs/gkxlumen-gateway-dev.yml` | 网关路由（L02b 已有，本任务确认） |
| `helm/gkxlumen-platform/values-lumen.yaml` | dev 最小集启用 innov |
| `helm/gkxlumen-platform/values.yaml` | innov 微服务默认值（L03 含 OTEL + MySQL env） |
| `gkxlumen-innov/**` | Java 业务模块（L03 移植，本分支继承） |

## Helm 部署命令（补验用）

```bash
helm upgrade --install gkxlumen ./helm/gkxlumen-platform \
  -n dev --create-namespace \
  -f ./helm/gkxlumen-platform/values-lumen.yaml
```

补验 curl（waiver 关闭后）：

```bash
curl -s "http://<dev-gateway>/innov/v1/meta/data-status" | jq .code
# 期望：0
```

## 架构合规自检

| 铁律 | 状态 |
|------|------|
| D1 算法只在 Python | ✅ 网关仅转发至 Java innov 服务 |
| D2 调用链 前端→Java→Python | ✅ 本任务仅 Java 网关层 |
| D3 NebulaGraph | N/A |
| D4 可观测性 OTel | ✅ innov helm env 含 `OTEL_SERVICE_NAME` |
| D5 CI/CD | 🟡 rollout/curl deferred |
| D6 demo2 只读 merge | ✅ 仅 lumen 正式仓 |

## 测试结果

| 项 | 结果 |
|----|------|
| `helm template … -f values-lumen.yaml` | ✅ 渲染 innov Deployment/Service + gateway 路由 |
| K8s dev rollout | **跳过**（PM waiver v2） |
| curl 冒烟 | **跳过**（PM waiver v2） |

## 遗留与下一任务

- **L05** qa-agent：`/innov/v1/**` 全套 API 测试（依赖 L04 路由 + 可选 rollout）
- **补验** devops-agent：`backend:image:innov` 入 CI、`helm:deploy` 后 rollout + curl
- **CI 缺口**：`.gitlab-ci.yml` 尚未含 `gkxlumen-innov` build/image job（waiver 期间不阻塞）

## Commit

- 分支：`feat/E-INNOV-M1-L04`
- message：`[agent:integration-agent] E-INNOV-M1-L04 enable innov in helm + gateway route`

---

*handoff · integration-agent · E-INNOV-M1-L04*
