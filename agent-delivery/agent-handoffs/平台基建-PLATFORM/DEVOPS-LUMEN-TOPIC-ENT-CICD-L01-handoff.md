# DEVOPS-LUMEN-TOPIC-ENT-CICD-L01 handoff

> **状态**：`done`（2026-07-31 human:淮政玮 清理 A 组验收关单）  
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
| 业务接入 commit | `8af9759` |
| Nacos init 修复 | `ce17d59`（探活）→ `0714332`（v3 admin publish） |
| Pipeline | https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/4344 |
| helm:deploy | job [#17684](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/17684) **success** |
| K8s | `gkxlumen-platform-topic-enterprise` Ready；镜像 `gkxlumen-topic-enterprise:07143322` |
| Gateway | Nacos `gkxlumen-gateway-dev.yml` 已含 `gkxlumen-topic-enterprise` 路由 |

### 附带修复（as-built）

Nacos 3.x 导致原 `nacos-config-init` hook 卡死（`/v1/console/health/readiness` → 410；v1 publish 不可靠）。  
已改为：控制台根路径探活 + login + `/v3/admin/cs/config` 发布。

## 4. 使用方式

1. 业务发版：点 `deploy:topic-enterprise` / `deploy:topic` / `deploy:innov` / `deploy:metrics`  
2. 底座或 chart 变更：点 `helm:deploy`  
3. Python 下游默认 `http://demo-platform-search-py:8080`（同 ns）

## 5. Cost（估算）

| 字段 | 值 |
|------|-----|
| actual_tokens | 160_000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 1.10 |
| cost_warn | green |
