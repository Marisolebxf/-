# DEVOPS-DEMO-HELM-CHART-PIN-PY-L01 · 派单包

> 执行角色：`devops-agent`（花名册无 `ops-agent`）  
> 监管：默认 `human:徐滕强`（`dispatch-rules#agent_supervisors`）；前序同类 helm 单也可用 `human:淮政玮`  
> 仓：`${GKX_ROOT}/repos/demo-svc-platform` · 推 `origin/dev`  
> 强度：`ponytail full`

## 背景

`helm:chart`（`HELM_CHART_ONLY=true`）已保证不 `--set global.imageTag`，Java 不会被打成当前 Java SHA。  
Python 侧 `values.yaml` 写死 `image.tag: latest`，算法仓用 `kubectl set image` 热更 **不写回 Helm values**。随后 `helm:chart` 按 chart 把现网 SHA **收成旧 `:latest`**。政策 `sync-ods` 404 即此因。

前序：`DEVOPS-DEMO-HELM-CHART-ONLY-L01`（done，只保 Java）。本叶补 Python。  
lumen 钉 SHA 是另一条路（`DEVOPS-LUMEN-INNOV-ENTAN-PIN-SHA-L01`）；**本叶不要把 demo values 写成死 SHA**，要 **chart-only 读现网再 `--set` 钉回去**。

## 推荐改法

只改 `scripts/k8s-deploy.sh` 的 `HELM_CHART_ONLY` 分支（可顺带改 `.gitlab-ci.yml` 注释）。

`helm upgrade` 前：对下表 Deployment `kubectl get ... -o jsonpath='{.spec.template.spec.containers[0].image}'`，解析 `:` 后 tag（或 digest），`--set {key}.image.tag=$tag`。  
Deployment 不存在 → skip，不要 `--set latest`。

不要改 `helm:deploy`。不要点 `helm:deploy` 验收。

## 高风险（必须钉）：CI `set image` + `tag: latest` + demo 开着

| Helm key | Deployment（release=`demo-platform`） | 镜像 | 热更 job | 源仓 |
|---|---|---|---|---|
| `entanPy` | `demo-platform-entan-py` | `gkx-entan-py-api` | `deploy:entan-py-api` | demo-algo-ent-analysis |
| `entanPyWorker` | `demo-platform-entan-py-worker` | `gkx-entan-py-worker` | `deploy:entan-py-worker` | 同上 |
| `innovPy` | `demo-platform-innov-py` | `gkx-innov-py` | `deploy:innov-py` | demo-algo-science |
| `searchPy` | `demo-platform-search-py` | `gkx-search-service` | `deploy:search-py` | demo-svc-topic-py |
| `aiPy` | `demo-platform-ai-py` | `gkx-ai-service` | `deploy:ai-py` | 同上 |
| `workerPy` | `demo-platform-worker-py` | `gkx-ai-worker` | `deploy:worker-py` | 同上 |

## 次要 / 不在本叶强钉

| 对象 | 说明 |
|---|---|
| `demoPy` / `gkx-demo-py` | values 也是 `latest`，无独立热更 job；建议一并钉（有 Deployment 就钉） |
| `etlEsPy` | `values-demo.yaml` **关闭**，现网不应有 |
| `frontend` / `gkx-demo-ui` | demo overlay **关闭**，前端各仓独立 yaml |
| Java（gateway/auth/upms/demo-a/demo-b-biz/innov） | 走 `global.imageTag`；chart-only **不** `--set`，不会打成 `latest`。若 `helm:deploy` 后又点过 `deploy:gateway` 等，chart-only 会收回**上次 helm SHA**（不是 latest）。本叶不强求钉 Java |
| 基础设施（mysql/redis/nacos/otel/tempo/loki） | 版本 tag，不是算法热更路径 |

`rollme: {{ randAlphaNum 5 }}` 仍会让 Python Pod 重启；本叶目标是 **镜像 tag 不回 latest**，不强制去掉 rollme。

## 验收

1. 脚本在 `HELM_CHART_ONLY` 打印将 `--set` 的 6 组 tag  
2. 在 dev 跑一次 `helm:chart` 后：`kubectl -n dev get deploy demo-platform-entan-py -o jsonpath='{.spec.template.spec.containers[0].image}'` 仍是 upgrade 前 SHA  
3. 不把 `values.yaml` 的 `tag: latest` 改成某个死 SHA  
4. handoff：`agent-handoffs/平台基建-PLATFORM/DEVOPS-DEMO-HELM-CHART-PIN-PY-L01.md`，含 `ponytail: full`

## 铁律

- 调用链 / Nebula / 可观测不改  
- 禁止 `helm:deploy`（会编 7 个 Java）  
- 禁止 force push  
- commit 带 `[agent:devops-agent]`
