# gkx-feishu-sync · K8s 部署（Webhook + 看板同步 Cron）

> 运维手册：[`agent-delivery/feishu-bitable-webhook-handler.md`](../../agent-delivery/feishu-bitable-webhook-handler.md)  
> RFC：[`agent-delivery/RFC/RFC-003-feishu-bitable-webhook.md`](../../agent-delivery/RFC/RFC-003-feishu-bitable-webhook.md)

## 做什么？

| 组件 | K8s 资源 | 替代 |
|------|----------|------|
| Webhook 入站 | `Deployment` + `Service` | 本机 `start-feishu-bitable-webhook.ps1` |
| 双向 sync + outbound 投影 | `CronJob`（30min，`feishu-bitable-cron-sync.mjs`） | 投影机 `register-board-sync-watch` |
| 公网回调 | `Ingress` 新增 path | 内网穿透 |

```text
飞书拖状态 → POST https://{已有域名}/internal/feishu-bitable/webhook
Cron 每 30min → feishu-bitable-cron-sync → registry↔飞书 → git push → dispatch scan
```

## 前置

- 基础镜像：**`harbor.htmisoft.net/hub/node:22.12.0-alpine`**（纯 Node + git/bash，无 PowerShell）
- namespace `gkx-dev`（或与 lumen dev 一致）
- Harbor pull secret `harbor-pull`（与 `lumen-svc-platform` helm 相同）
- GitLab Deploy Token / PAT：`read_repository` + `write_repository`（push `task-registry.yaml`）
- **已有 Ingress 域名 + TLS**（本 chart 只加 path，不新建域名）

## 1. CI/CD（推荐）

仓库根目录 `.gitlab-ci.yml`（仅 **dev** 分支触发）：

| Job | 阶段 | 说明 |
|-----|------|------|
| `feishu-sync:smoke` | test | Node `--check` 核心脚本 |
| `feishu-sync:image` | package | 构建并推送 `harbor.htmisoft.net/gkx/gkx-feishu-sync:{sha}` + `:latest` |
| `deploy:feishu-sync` | deploy | `kubectl apply` Deployment/Service/CronJob；默认 **manual** |

**首次发布**：Secret 预置后，GitLab → CI/CD → Run pipeline → 分支 `dev` → 变量 `FULL_PIPELINE=true` → 跑完 package 后点 **deploy:feishu-sync**。

**路径过滤**：仅 `deploy/feishu-sync/`、飞书/dispatch 相关 `scripts/`、以及 `agent-delivery` 里飞书/派单配置 YAML 变更时才会触发 pipeline；改 `task-registry.yaml`、handoff、无关 RFC 等 **不会** 重新 build/deploy。强制发布：Run pipeline 设 `FULL_PIPELINE=true`。

**组级变量**（已配置）：`HARBOR_*`、`KUBECONFIG_B64`。  
**可选**：`FEISHU_INGRESS_HOST` + `FEISHU_TLS_SECRET` 让 deploy 一并 apply Ingress。

## 2. 本地手动构建镜像

```bash
cd gkx-orchestration
docker build -f deploy/feishu-sync/Dockerfile -t harbor.htmisoft.net/gkx/gkx-feishu-sync:latest .
docker push harbor.htmisoft.net/gkx/gkx-feishu-sync:latest
```

## 3. Secret

```bash
cp deploy/feishu-sync/k8s/secret.example.yaml deploy/feishu-sync/k8s/secret.yaml
# 编辑 secret.yaml 填 FEISHU_* / GKX_GITLAB_TOKEN / FEISHU_BITABLE_WEBHOOK_SECRET
kubectl apply -f deploy/feishu-sync/k8s/secret.yaml
```

## 4. 部署工作负载

```bash
kubectl apply -f deploy/feishu-sync/k8s/deployment.yaml
kubectl apply -f deploy/feishu-sync/k8s/service.yaml
kubectl apply -f deploy/feishu-sync/k8s/cronjob.yaml
```

## 5. 挂到已有 Ingress 域名

**方式 A（推荐）**：独立 Ingress 只加 path（与现有 lumen Ingress 同 host 共存）

```bash
# 编辑 deploy/feishu-sync/k8s/ingress-path.yaml：
#   __INGRESS_HOST__     → 例如 skxdemo.unicomcn.tech（你们实际 dev 域名）
#   __TLS_SECRET_NAME__  → 该 host 已在用的 tls secret 名

kubectl apply -f deploy/feishu-sync/k8s/ingress-path.yaml
```

**方式 B**：在现有 Helm `values-dev.yaml` 的 `ingress.hosts[].paths` 追加：

```yaml
- path: /internal/feishu-bitable
  pathType: Prefix
  backend: feishu-sync   # 需自行加 Service 名 gkx-feishu-sync:8787
```

飞书 Bitable 自动化 URL：

```text
https://{你的Ingress域名}/internal/feishu-bitable/webhook
Header: X-GKX-Webhook-Secret: <FEISHU_BITABLE_WEBHOOK_SECRET>
Body: {"record_id":"{{record_id}}","app_token":"...","table_id":"..."}
```

## 6. 验收

```bash
kubectl -n gkx-dev get pods -l app=gkx-feishu-sync
kubectl -n gkx-dev logs deploy/gkx-feishu-sync -f

curl -sS "https://{域名}/internal/feishu-bitable/webhook" \
  -H "Content-Type: application/json" \
  -H "X-GKX-Webhook-Secret: ***" \
  -d '{"type":"url_verification","challenge":"ok"}'
# 期望：{"challenge":"ok"}

kubectl -n gkx-dev create job --from=cronjob/gkx-feishu-sync-board-watch manual-sync-1
kubectl -n gkx-dev logs job/manual-sync-1
```

## 7. 退役投影机

K8s Cron + Webhook 稳定运行 **1～2 个 Sprint** 后：

```powershell
# Windows 投影机
.\scripts\register-board-sync-watch.ps1 -Unregister
```

## 8. 配置真源

- `agent-delivery/feishu-bitable.yaml#webhook` — `auto_git_push: true`
- Secret 环境变量覆盖 `.env` 本地值
