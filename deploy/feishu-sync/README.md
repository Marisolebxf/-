# gkx-feishu-sync · K8s 部署（Webhook + 看板同步 Cron）

> 运维手册：[`agent-delivery/feishu/feishu-bitable-webhook-handler.md`](../../agent-delivery/feishu/feishu-bitable-webhook-handler.md)  
> RFC：[`agent-delivery/RFC/RFC-003-feishu-bitable-webhook.md`](../../agent-delivery/RFC/RFC-003-feishu-bitable-webhook.md)

## 做什么？

| 组件 | K8s 资源 | 替代 |
|------|----------|------|
| Webhook 入站 | `Deployment` + `Service` | 本机 `start-feishu-bitable-webhook.ps1` |
| 双向 sync + outbound 投影 | `CronJob` `gkx-feishu-sync-board-watch`（高峰 15min / 夜间 2h） | 投影机 `register-board-sync-watch` |
| Mayor 派单建议 + 门控 IM（A3） | `CronJob` `gkx-feishu-sync-coordinator-loop`（工作时段每 2h） | 本机 `register-coordinator-loop-watch` |
| 公网回调 | `Service` NodePort **30894** 或 Ingress path | 内网穿透 / 防火墙 DNAT |

```text
飞书拖状态 → webhook：看板字段 inbound 已关（skipped）；dispatch_confirm 等门控 action 仍可用
Cron board-watch → outbound only（默认 **全部 Sprint**；无 record_id 则 CREATE 并回写）
  → 投影前刷新用户故事库：`extract-user-stories --write` + `check-story-coverage --write`
  → 投影看板出站：指标对象（sync-feishu-metric-board）+ A1 算法库叶子（sync-feishu-algo-leaf-board）+ A2 页面差集（sync-feishu-algo-gap-board）+ 指标算法WBS（sync-feishu-wbs-board）+ 甲方决策清单 + 上线前必办 + 用户故事库（均非致命）
  → git push → dispatch scan
  高峰 08:30–01:00 每 15min；其余 03:00/05:00/07:00 每 2h
  逃生阀：`feishu-bitable-cron-sync.mjs --current-sprint-only`
Cron coordinator-loop → git pull → `--propose-dispatch`（pending + 派单门控待确认 + IM→淮政玮）→ git-push-registry
  08/10/12/14/16/18/20（Asia/Shanghai）；淮政玮改「已确认」→ webhook dispatch_confirm → 可派
  默认不 apply-leases；关 propose：COORDINATOR_LOOP_PROPOSE_DISPATCH=0
```

## 前置

- 基础镜像：**`harbor.test.com/zp-tts/node:22.12.0-alpine`**（须先推入 Harbor 项目 `zp-tts`；纯 Node + git/bash，无 PowerShell）
- namespace `zhipu-tts`
- Harbor pull secret `harbor-pull`（须在 `zhipu-tts` 创建，指向 `harbor.test.com`）
- GitLab Deploy Token / PAT：`read_repository` + `write_repository`（push registry YAML + `pending-dispatch.yaml` + confirm 产生的 `*派单包.md`）
- **访问**：`Service` 类型 **NodePort 30894**（节点 `10.50.192.46` / `10.50.69.111` / `10.50.75.136`）；外网 `111.198.38.90:12287` 若仍映射，DNAT 目标须改为新集群节点的 30894
- **可选** Ingress 域名 + TLS（与 NodePort 二选一或并存）

## 1. CI/CD（推荐）

仓库根目录 `.gitlab-ci.yml`（仅 **dev** 分支触发）：

| Job | 阶段 | 说明 |
|-----|------|------|
| `feishu-sync:smoke` | test | Node `--check` 核心脚本 |
| `feishu-sync:image` | package | 构建并推送 `harbor.test.com/zp-tts/gkx-feishu-sync:{sha}` + `:latest` |
| `deploy:feishu-sync` | deploy | `kubectl apply` Deployment/Service/CronJob；默认 **manual** |

**首次发布**：Secret 预置后，GitLab → CI/CD → Run pipeline → 分支 `dev` → 变量 `FULL_PIPELINE=true` → 跑完 package 后点 **deploy:feishu-sync**。

**路径过滤**：仅 `deploy/feishu-sync/`、飞书/dispatch 相关 `scripts/`、以及 `agent-delivery` 里飞书/派单配置 YAML 变更时才会触发 pipeline；改 `task-registry.yaml`、handoff、无关 RFC 等 **不会** 重新 build/deploy。强制发布：Run pipeline 设 `FULL_PIPELINE=true`。

**组级变量**（已配置）：`HARBOR_*`、`KUBECONFIG_B64`。  
**可选**：`FEISHU_INGRESS_HOST` + `FEISHU_TLS_SECRET` 让 deploy 一并 apply Ingress。

## 2. 本地手动构建镜像

```bash
cd gkx-orchestration
docker build -f deploy/feishu-sync/Dockerfile -t harbor.test.com/zp-tts/gkx-feishu-sync:latest .
docker push harbor.test.com/zp-tts/gkx-feishu-sync:latest
```

## 3. Secret（首次 deploy 前必做）

**报错 `secret/gkx-feishu-sync not found`** = 本步未做。命名空间用 `zhipu-tts`，应用 Secret 需一次性写入。

### 方式 A（推荐 · 本机有 `.env`）

```bash
cd gkx-orchestration
chmod +x scripts/k8s-apply-feishu-sync-secret.sh
./scripts/k8s-apply-feishu-sync-secret.sh
# 会从 .env 读 FEISHU_* / GKX_GITLAB_TOKEN；目标命名空间没有 harbor-pull 时从 zhipu-tts 复制（通常需先在该命名空间创建）
```

### 方式 B（GitLab 组变量 · CI 自动 bootstrap）

在 GitLab **gkx-lumen 组** CI/CD Variables 增加（Masked）：

| 变量 | 说明 |
|------|------|
| `FEISHU_APP_ID` | 飞书应用 |
| `FEISHU_APP_SECRET` | 飞书应用 |
| `FEISHU_BITABLE_WEBHOOK_SECRET` | 与飞书自动化 Header 一致 |
| `GKX_GITLAB_TOKEN` | push task-registry 用 PAT |

重跑 **deploy:feishu-sync** 即可自动 `kubectl apply` Secret。

### 方式 C（手工 yaml）

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
kubectl apply -f deploy/feishu-sync/k8s/cronjob-coordinator-loop.yaml
# 或一键：./scripts/k8s-deploy-feishu-sync.sh
```

### 4.1 Mayor Cron（A3）运维

| 项 | 说明 |
|----|------|
| 资源名 | `cronjob/gkx-feishu-sync-coordinator-loop` |
| 节奏 | 每小时 tick；门控仅 **08/10/12/14/16/18/20**（上海时区）真正跑 |
| 默认 | `COORDINATOR_LOOP_APPLY_LEASES=0` → 不回收 lease |
| 派单门控 | `COORDINATOR_LOOP_PROPOSE_DISPATCH=1`（默认）→ 可派 ready 写入 `pending-dispatch` + 飞书「派单门控=待确认」+ **IM 通知淮政玮**；随后 `git-push-registry` |
| 看结果 | `kubectl -n zhipu-tts logs job/...`（Job 内 `_tmp` 不持久） |

**淮政玮确认闭环**（复用自动化 B，不走 inbound）：

1. Mayor Cron / `--propose-dispatch` → 看板列「派单门控」= 待确认、确认人=@淮政玮，并私信
2. 淮政玮把「派单门控」改为 **已确认**
3. 飞书自动化 POST `action=dispatch_confirm` + `approved_by: human:淮政玮`
4. webhook → `confirmPending` → 任务可派

应用需开通 **IM 发消息**权限；否则日志 `notify: FAIL`，门控列仍会写。关 IM：`COORDINATOR_LOOP_NO_NOTIFY=1`。关 propose：`COORDINATOR_LOOP_PROPOSE_DISPATCH=0`。

```bash
# 立刻手跑一枪（绕过门控）
kubectl -n zhipu-tts create job --from=cronjob/gkx-feishu-sync-coordinator-loop mayor-manual-1
kubectl -n zhipu-tts logs -f job/mayor-manual-1

# 开启 lease 回收（改 CronJob env 后下次 tick 生效；会 git push）
kubectl -n zhipu-tts set env cronjob/gkx-feishu-sync-coordinator-loop \
  COORDINATOR_LOOP_APPLY_LEASES=1
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
kubectl -n zhipu-tts get pods -l app=gkx-feishu-sync
kubectl -n zhipu-tts get svc gkx-feishu-sync
# 期望：TYPE=NodePort  PORT(S)=8787:30894/TCP

curl -sS "http://192.168.88.50:30894/health"
curl -sS "http://192.168.88.50:30894/internal/feishu-bitable/webhook" \
  -H "Content-Type: application/json" \
  -H "X-GKX-Webhook-Secret: ***" \
  -d '{"type":"url_verification","challenge":"ok"}'
# 期望：{"challenge":"ok"}

kubectl -n zhipu-tts logs deploy/gkx-feishu-sync -f

kubectl -n zhipu-tts create job --from=cronjob/gkx-feishu-sync-board-watch manual-sync-1
kubectl -n zhipu-tts logs job/manual-sync-1
```

## 7. 退役投影机

K8s Cron + Webhook 稳定运行 **1～2 个 Sprint** 后：

```powershell
# Windows 投影机
.\scripts\register-board-sync-watch.ps1 -Unregister
```

## 8. 配置真源

- `agent-delivery/feishu/feishu-bitable.yaml#webhook` — `auto_git_push: true`
- Secret 环境变量覆盖 `.env` 本地值
