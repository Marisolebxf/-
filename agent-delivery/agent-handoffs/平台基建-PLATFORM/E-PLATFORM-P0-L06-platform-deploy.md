# DevOps handoff · E-PLATFORM-P0-L06 平台服务 K8s 工程化部署

| 项 | 值 |
|---|---|
| 任务 | E-PLATFORM-P0-L06 |
| Epic | E-PLATFORM-P0 |
| 角色 | devops-agent |
| 仓库 | `lumen-svc-platform`（backend.lumen） |
| 分支 | `feat/E-PLATFORM-P0-L06` |
| 日期 | 2026-06-20 |
| PM waiver | **v2** — 禁止等待 K8s rollout / curl / Tempo / Harbor 镜像就绪 |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 说明 |
|--------|------|------|
| Helm 启用 innov + metrics + topic | ✅ | `values-lumen.yaml` 三项 `enabled: true` |
| CI build/image/deploy 占位 | ✅ | `.gitlab-ci.yml` 扩展 6 模块 build + 3 镜像 job + 3 单服务 deploy |
| gkxlumen-innov 纳入 reactor | ✅ | `pom.xml` + 自 `feat/E-INNOV-M1-L03` 引入模块 |
| OTEL_SERVICE_NAME helm env | ✅ | `values.yaml` innov/metrics/topic |
| 部署清单文档 | ✅ | `docs/PLATFORM-DEPLOY-CHECKLIST.md` |
| metrics + topic 镜像推 Harbor | ⏸️ **DEFERRED P0-L08** | CI job 已就位，未触发 pipeline |
| dev rollout 成功 | ⏸️ **DEFERRED P0-L08** | 未 kubectl apply / helm:deploy |
| GET /metrics/v1/catalog 可达 | ⏸️ **DEFERRED P0-L08** | 未 curl |
| GET /topic/v1/health 可达 | ⏸️ **DEFERRED P0-L08** | 未 curl |
| Tempo 可见 metrics/topic trace | ⏸️ **DEFERRED P0-L08** | 未查 Tempo |

## 产物清单

| 路径 | 说明 |
|------|------|
| `helm/gkxlumen-platform/values-lumen.yaml` | dev 最小集：gateway/auth/upms + **innov/metrics/topic** |
| `helm/gkxlumen-platform/values.yaml` | OTEL env 补全 innov/metrics |
| `.gitlab-ci.yml` | `backend:build` 含 6 模块；`backend:image:{innov,metrics,topic}`；`deploy:{innov,metrics,topic}` |
| `pom.xml` | `<module>gkxlumen-innov</module>` |
| `gkxlumen-innov/**` | 自 L03 分支引入（与 L05 metrics/topic 同分支聚合） |
| `helm/gkxlumen-platform/DEPLOY-LUMEN.md` | 部署前置 / CI 阶段 / 验证清单（D1–D6 defer 标注） |

## Helm 启用摘要

```yaml
microservices:
  gateway: { enabled: true }
  auth:    { enabled: true }
  upms:    { enabled: true }
  innov:   { enabled: true }   # 7090 · /innov/**
  metrics: { enabled: true }   # 7091 · /metrics/**
  topic:   { enabled: true }   # 7092 · /topic/**
```

网关路由已在 `configs/gkxlumen-gateway-dev.yml` 预置。

## CI 新增 Job

| Job | 镜像 |
|-----|------|
| `backend:image:innov` | `harbor.htmisoft.net/gkx/gkxlumen-innov` |
| `backend:image:metrics` | `harbor.htmisoft.net/gkx/gkxlumen-metrics` |
| `backend:image:topic` | `harbor.htmisoft.net/gkx/gkxlumen-topic` |
| `deploy:innov` / `deploy:metrics` / `deploy:topic` | 单 Deployment 热更新（manual） |

`helm:deploy` needs 已包含上述 image job（仍 manual，不自动 rollout）。

## 架构合规自检

| 铁律 | 状态 |
|------|------|
| D2 调用链 前端→Java→Python | ✅ Helm 仅部署 Java 层；Python innovPy 仍 disabled |
| D4 可观测性 OTel | ✅ OTEL_SERVICE_NAME 三服务 + JavaAgent Dockerfile |
| D6 demo2 只读 merge | ✅ 仅 lumen 正式仓 |
| D7 方案 A 共享聚合 | ✅ metrics + topic 同 chart 启用 |

## 验收证据

| 项 | 结果 |
|----|------|
| 本地 helm lint | **未跑**（runner 环境；CI `helm:lint` 待 push 后触发） |
| GitLab pipeline | **未等待**（PM waiver v2） |
| K8s rollout | **DEFERRED P0-L08** |
| curl 冒烟 | **DEFERRED P0-L08** |
| Tempo | **DEFERRED P0-L08** |

## 接力（P0-L08 补验）

1. 合并 `feat/E-PLATFORM-P0-L06` → `main`（或 dev 集成分支）
2. 触发 Pipeline：`backend:build` → `backend:image:*` → manual `helm:deploy`
3. 执行 `docs/PLATFORM-DEPLOY-CHECKLIST.md` §5 D1–D6
4. coordinator P0-L08 里程碑签收

## cost

| estimated_tokens | actual_tokens | model_used | actual_cost | cost_warn |
|------------------|---------------|------------|-------------|-----------|
| 200_000 | 120_000 | claude-sonnet-4.5 | 0.24 | green |

## git

- 分支：`feat/E-PLATFORM-P0-L06`
- commit：见 push 后 SHA
- push：`origin/feat/E-PLATFORM-P0-L06`

---

*handoff · devops-agent · E-PLATFORM-P0-L06*
