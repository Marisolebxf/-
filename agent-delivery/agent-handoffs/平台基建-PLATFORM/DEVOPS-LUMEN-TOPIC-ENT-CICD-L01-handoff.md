# DEVOPS-LUMEN-TOPIC-ENT-CICD-L01 handoff

> **状态**：待 coordinator 验收 → `done`  
> **执行**：agent:devops-agent · **监管**：human:淮政玮  
> **日期**：2026-07-17

---

## 1. 范围

把 **业务常发** 服务 `gkxlumen-topic-enterprise` 接入 CI/Helm 热更新；图 2 `deploy:*` 顺序改为业务优先。

## 2. 产物

| 项 | 说明 |
|----|------|
| Dockerfile | `gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz/Dockerfile`（端口 7093，OTel） |
| CI | `backend:build` 含模块；`backend:image:topic-enterprise`；`deploy:topic-enterprise` |
| Helm | `values.yaml` + `values-lumen` 启用 `topic-enterprise` |
| Gateway | `gkxlumen-gateway-dev.yml` 企业路径优先于通用 `/topic/**` |
| 文档 | `DEPLOY-LUMEN.md` 业务常发 vs helm 分层 |

## 3. 证据

| 项 | 值 |
|----|-----|
| commit | `8af9759`（origin/dev） |
| Pipeline | https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/4342 |

## 4. 使用方式

1. Pipeline package 绿后，**首次**点 `helm:deploy`（创建 `gkxlumen-platform-topic-enterprise`）  
2. 之后业务发版：点 `deploy:topic-enterprise` / `deploy:topic` 等即可  
3. Python 下游默认 `http://demo-platform-search-py:8080`（同 ns）

## 5. Cost（估算）

| 字段 | 值 |
|------|-----|
| actual_tokens | 90_000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.60 |
| cost_warn | green |
