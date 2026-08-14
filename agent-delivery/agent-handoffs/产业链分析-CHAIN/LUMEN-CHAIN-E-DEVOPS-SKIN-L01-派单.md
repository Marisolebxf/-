# LUMEN-CHAIN-E-DEVOPS-SKIN-L01 · 派单条

> **日期**：2026-08-14  
> **监管**：`human:淮政玮`（不必再问）  
> **执行**：`devops-agent`  
> **原因**：`LUMEN-CHAIN-FE-SEARCH-SKIN-L01` 已 push `lumen-ui-topic` `ee3ff6f`。当前集群镜像仍是 `gkx-lumen-topic:b0032e17`，已发布页看不到 Hero/页底。

## 范围

只确认 **`lumen-ui-topic` → deploy `gkx-lumen-topic`** 吃到 `ee3ff6f`（或其后 SHA）并 rollout 健康。

- **不要**改 helm / CI / 业务代码。  
- **不要**重滚 Java / Python（除非镜像仍停在旧 tag 且必须等 pipeline）。  
- 禁止 localhost。  
- D12：确认仍走 `gkxlumen-platform-gateway`，未指向 `demo-*`。

## 步骤

1. 查 GitLab `gkx-lumen/lumen-ui-topic` 对 `ee3ff6f` 的 Pipeline（`cicd-pipeline.md`：push `dev` 应自动 `deploy:k8s`）。未绿则 `blocked` 写 job 名，不要手改 yaml。  
2. `kubectl -n dev`：`gkx-lumen-topic` image tag 含 `ee3ff6f`（或更新）；`rollout status` 1/1。  
3. `curl -I http://192.168.88.50:30892` → 200。  
4. 静态资源或 HTML 能证明新包（可选：搜 `industry-search-page` / 对比旧 `b0032e17`）。  
5. handoff 本 ID；tech_task 转 ready_to_sign，**不标 done**。

## `/goal`

```text
/goal
你是 devops-agent。task-id：LUMEN-CHAIN-E-DEVOPS-SKIN-L01
监管：human:淮政玮
强度：ponytail full
仓：不改业务代码。只等/核 lumen-ui-topic Pipeline + K8s gkx-lumen-topic 镜像 ≥ ee3ff6f。
必读：本条 · LUMEN-CHAIN-E-DEVOPS-L01.md · cicd-pipeline.md
禁止：改 helm 凑发布；localhost；打到 demo-*；问用户。
写 handoff agent-delivery/agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-E-DEVOPS-SKIN-L01.md
```
