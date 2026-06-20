# DevOps handoff · E-PLATFORM-P0-L00 专题前端仓

| 项 | 值 |
|---|---|
| 任务 | E-PLATFORM-P0-L00 |
| Epic | E-PLATFORM-P0 |
| 角色 | devops-agent |
| 仓 | `lumen-ui-science-topic`（老 `gkx_lumen_fronted_topic`） |
| 分支 | `feat/E-PLATFORM-P0-L00`（与 `main` 同内容） |
| Commit | `4b9e6604b1a28aa836801cde6df4bc52e3f83f0b` |
| 日期 | 2026-06-20 |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 证据 |
|--------|------|------|
| 仓存在（GitLab gkx-lumen 组） | ✅ | https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-science-topic |
| 保留 observability.ts、request 拦截器、网关代理 | ✅ | `src/utils/observability.ts`、`src/utils/request.ts`、`k8s/lumen-topic.yaml` `/api/` → gateway |
| `.gitlab-ci.yml` frontend:build + deploy:k8s（30892） | ✅ | 仓内 CI + `k8s/lumen-topic.yaml` nodePort 30892 |
| push → build 绿 | ✅ | Pipeline #4117 `frontend:build` success、`frontend:image` success |
| dev rollout + :30892 占位首页 | ❌ | `deploy:k8s` failed（见阻塞项） |
| 更新 repo-registry / paths / cicd-pipeline（去 interim） | ✅ | 编排仓本 handoff 同期提交 |

## GitLab / CI

| 项 | 值 |
|----|-----|
| GitLab URL | https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-science-topic |
| Project ID | 232 |
| Pipeline | https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-science-topic/-/pipelines/4117 |
| 镜像 | `harbor.htmisoft.net/gkx/gkx-lumen-topic:4b9e6604` |
| deploy namespace | `dev`（目标） |
| dev URL | http://192.168.88.50:30892 |

### Pipeline job 结果

| Job | 状态 |
|-----|------|
| `frontend:build` | ✅ success |
| `frontend:image` | ✅ success（首次 TLS 抖动失败后 retry 通过） |
| `deploy:k8s` | ❌ failed |
| `trivy:frontend` | skipped（deploy 失败） |

## 产物清单

### lumen-ui-science-topic

| 路径 | 说明 |
|------|------|
| `.gitlab-ci.yml` | frontend:build → frontend:image → deploy:k8s |
| `k8s/lumen-topic.yaml` | Deployment + Service NodePort **30892** + nginx 网关代理 |
| `docker/Dockerfile` | nginx 静态资源镜像 |
| `src/utils/observability.ts` | traceId / Grafana 深链 |
| `src/utils/request.ts` | axios 拦截器 + trace 日志 |
| `src/views/HomeView.vue` | Wave 0 占位首页 |
| `vite.config.ts` | dev 网关 proxy |

### gkx-orchestration

| 路径 | 说明 |
|------|------|
| `agent-delivery/repo-registry.yaml` | migration_map + ui_topic 去 interim |
| `agent-delivery/paths.yaml` | `lumen-ui-science-topic` 路径 |
| `agent-delivery/cicd-pipeline.md` | topic CI 现状更新 |

## 架构合规自检

| # | 项 | 结果 |
|---|-----|------|
| 1 | 算法只在 Python | ✅ 前端仓无算法 |
| 2 | 调用链 | ✅ 仅经 `/api` 代理 Java 网关；专题调 topic/metrics |
| 4 | observability.ts | ✅ 保留 |
| 6 | demo2 禁止 merge lumen | ✅ 从 pc 模板 fork，未 merge demo2 |
| 8 | D8 Arco 栈 | ✅ Vue3 + Arco + Vite（与 pc 一致） |

## 阻塞项

1. **K8s API 不可达（deploy:k8s）**
   - Job log：`The connection to the server 192.168.88.50:6443 was refused`
   - 组变量 `KUBECONFIG_B64` 指向的 API Server 当前拒绝连接；需 infra/coordinator 恢复集群或更新 kubeconfig 后 **retry pipeline #4117** 或重跑 `deploy:k8s`。
2. **:30892 未验证**
   - 依赖 deploy 成功；agent 侧 curl 内网 IP 超时（可能不在同一 VPN）。
3. **下游**
   - `E-PLATFORM-P0-L02` / 专题页 frontend-agent 可基于本仓 `feat/E-PLATFORM-P0-L00` 开发；生产 dev 冒烟待 deploy 绿后由 qa 补测。

## 接力清单

| 下游 | 动作 |
|------|------|
| **integration-agent / infra** | 修复 K8s API；确认 `harbor-pull` Secret 在 dev ns；retry deploy |
| **frontend-agent** | `/topic/**` 页面开发；禁止 merge demo-ui-topic 到 lumen |
| **coordinator** | K8s 恢复后标记本任务 done；回填 task-registry pipeline 字段 |

## Cost（占位）

| estimated_tokens | actual_tokens | model_used | actual_cost | cost_warn |
|------------------|---------------|------------|-------------|-----------|
| 200_000 | 0 | claude-sonnet-4.5 | 0.0 | green |
