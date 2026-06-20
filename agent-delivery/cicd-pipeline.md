# CI/CD 与 K8s 发布规范（Agent 强制执行）

> **铁律**：每个 leaf 任务完成 = 代码已 **push GitLab** + **Pipeline 绿** + **K8s dev 部署成功** + **冒烟/接口测试通过**。
> 仅本地改完不 push 视为 **未完成**。

---

## 1. 标准闭环（每个 Agent 必须走）

```mermaid
flowchart LR
  A[本地修改+自测] --> B[git commit]
  B --> C[git push 远程分支]
  C --> D[GitLab CI Pipeline]
  D --> E[Harbor 镜像]
  E --> F[K8s dev 滚动发布]
  F --> G[qa 冒烟/接口/E2E]
  G --> H[handoff + 更新 task-registry]
```

| 步骤 | 要求 |
|------|------|
| 分支 | 功能在 `dev` 或 `feat/{task-id}`；合并目标 `dev` → `main` |
| Commit | 消息含 task-id，如 `feat(E-INNOV-M1-L03): 移植 gkxlumen-innov` |
| Push | `git push -u origin <branch>`，禁止只留本地 |
| Pipeline | 等待 GitLab CI 全部 required job 通过（可用 `glab`/`curl` API 轮询） |
| Deploy | `main` 推 dev 命名空间；`release/*` → uat（manual）；tag → prod（manual） |
| 测试 | 对 **K8s 上运行的服务** 测，不只 localhost |

---

## 2. 基础设施（已存在）

| 项 | 值 |
|----|-----|
| GitLab | https://gitlab.htmisoft.net/SZCGKX |
| Harbor | harbor.htmisoft.net/gkx |
| Runner | tag=`rag`，shell executor（htsvr036） |
| K8s 集群 | kubeconfig 存 GitLab 组变量 `KUBECONFIG_B64` |
| dev 命名空间 | `dev` |
| 前端 dev 访问 | http://192.168.88.50:30891（gkx-lumen-pc）、http://192.168.88.50:30892（gkx-lumen-topic） |

组级 CI 变量（SZCGKX）：`HARBOR_*`、`KUBECONFIG_B64`（已配置，agent 勿写入仓库）。

---

## 3. 各仓 CI/CD 现状

| 仓库 | .gitlab-ci.yml | 镜像名 | K8s 部署方式 | main→dev |
|------|----------------|--------|-------------|----------|
| `innov-algo-demo` | ✅ | gkx-innov-py | helm innov-py 热更新 | manual deploy job |
| `gkx_lumen_fronted_pc` | ✅ | gkx-lumen-pc | 独立 Deployment NodePort 30891 | **自动** deploy:k8s |
| `gkx_lumen_fronted_topic` / `lumen-ui-science-topic` | ✅ | gkx-lumen-topic | 独立 Deployment NodePort 30892 | **自动** deploy:k8s |
| `gkx_service_demo` | ✅ | gkx-* 多服务 | helm gkx-platform | manual helm:deploy |
| `gkx_lumen_backend` | ❌ **待建** | gkxlumen-* | 待从 demo 复制 helm + CI | — |
| `ent-analysis-demo` | ✅ | 见仓内 CI | 见仓内 | 见仓内 |

**缺口**：`gkx_lumen_backend` 尚无 CI — 首 Epic 需在 L03 前从 `gkx_service_demo` 移植 `.gitlab-ci.yml` + `helm/`，并改模块名为 gkxlumen-*。

---

## 4. Pipeline 阶段（对齐 demo 仓）

### Java（gkx_lumen_backend）

```
build (mvn verify) → test (surefire) → package (docker) → scan (trivy) → deploy (helm/kubectl)
```

### Python（innov-algo-demo）

```
test (py:smoke) → package (py:image) → deploy (deploy:innov-py → dev)
```

### 前端（gkx_lumen_fronted_pc）

```
build (npm run build) → package (frontend:image) → deploy (deploy:k8s → dev 自动)
```

---

## 5. Agent 派单附加指令（写入每个 /goal）

```
完成代码后必须：
1. git add / commit / push 到对应仓库远程分支
2. 等待 GitLab Pipeline 成功（附 pipeline URL 到 handoff）
3. 确认 K8s dev 滚动完成（kubectl rollout status 或 CI deploy job 绿）
4. 对 dev 环境执行本任务 DoD 中的测试项
5. handoff 填写：commit SHA、pipeline ID、部署 namespace、测试 URL/命令
```

---

## 6. K8s 测试入口（E-INNOV-M1）

| 被测服务 | dev 验证方式 |
|---------|-------------|
| Python innov-py | `/internal/status`；**Tempo** 中 `service.name` 对应 OTEL_SERVICE_NAME |
| Java gkxlumen-innov | 网关 `/innov/v1/*`；响应头 **traceparent** / **X-Trace-Id** |
| 前端 lumen-pc | :30891；错误拦截器输出 traceId + Grafana 深链（若已配 VITE_GRAFANA_*） |
| 前端 lumen-topic | :30892；占位首页 + observability 冒烟 |

可观测性规范见 `observability.md`。

---

## 7. 失败处理

| 情况 | 动作 |
|------|------|
| Pipeline 红 | agent 读 job log，修复后新 commit push，直到绿 |
| deploy job manual 未点 | coordinator 或 integration-agent 在 GitLab 触发 deploy |
| K8s rollout 失败 | `kubectl describe pod` + 修镜像/配置 + 重跑 pipeline |
| 测试失败 | 开新 commit 修复，禁止标记 task done |

---

## 8. 禁止事项

- 禁止 `--no-verify` 跳过 hook（除非 hook 明确阻塞且 handoff 说明）
- 禁止 force push `main`/`dev`
- 禁止把 Harbor 密码、kubeconfig 写入代码库
- 禁止「本地验证通过」但不 push 就关 task
