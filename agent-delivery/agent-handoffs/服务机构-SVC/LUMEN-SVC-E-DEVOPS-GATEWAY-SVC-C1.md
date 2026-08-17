# LUMEN-SVC-E-DEVOPS-GATEWAY-SVC-C1 · 外网 `/api/svc/**` 网关路由修复

> 日期：2026-08-17  
> Task：`LUMEN-SVC-E-DEVOPS-GATEWAY-SVC-C1`  
> 总控：[`DEMO-SVC-ABCD-长任务总控.md`](./DEMO-SVC-ABCD-长任务总控.md)  
> E1 证据：[`LUMEN-SVC-E-QA-SMOKE-L01.md`](./LUMEN-SVC-E-QA-SMOKE-L01.md)  
> 协作：`algorithm-agent` 已挂载 search-py `/internal/gkx-svc/**`（`85a8fd9`/`b2cd5c11`）；本单 devops 收口验证 + Nacos 热更钩子

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权「不必再问」；lock 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 Nacos 热更钩子与外网验收；未另起路由体系 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 外网 curl + GitLab CI play；本机无集群 kubeconfig |

## 根因（E1 404）

两层叠加：

1. **网关 / Nacos 路由（E1 主诉）**  
   - QA：`/api/svc/topic/v1/**` → HTTP 404，`No static resource svc/topic/v1/...`，无 `X-Trace-Id`  
   - 仓内 seed 已有 `Path=/svc/**` → `lb://gkxlumen-topic-svc-biz`  
   - **`nacosConfigInit.runOnUpgrade` 默认 `false`**：普通 `helm:chart` **不**重灌直播 Nacos  
   - nginx `^~/api/` → gateway 正常（对照 `/api/chain/.../health` 绿）

2. **下游 Python（网关通后次生）**  
   - 一度 HTTP 200 + `X-Trace-Id`，body `{"detail":"Not Found"}`（Feign → FastAPI 404）  
   - search-py 未挂载 `/internal/gkx-svc/**`（已由 algorithm 修 + `deploy:search-py` 22467）

## 修复动作

| # | 动作 | 证据 |
|---|------|------|
| 1 | `FORCE_NACOS_REPUBLISH` → `nacosConfigInit.runOnUpgrade=true` | `lumen-svc-platform` `fdd07c7` |
| 2 | `helm:chart` 透传变量 | 同 commit |
| 3 | values-lumen 注释 `/svc/**` | 同 commit |
| 4 | push `origin/dev` · pipeline [5142](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5142) | sha `fdd07c70` |
| 5 | play `helm:chart` **22486** `FORCE_NACOS_REPUBLISH=true` | success；Job `nacos-config-init` Completed |
| 6 | `deploy:search-py` **22467** | `gkxlumen-search-service:b2cd5c11` rollout 绿 |

## 验证（外网 · 无 auth）

基址：`http://111.198.38.90:50892/`

```text
GET  /api/svc/topic/v1/service/health
  → HTTP 200 + X-Trace-Id
  → {"code":0,"ok":true,"data":{"status":"ok","service":"gkx-svc-service",...}}

POST /api/svc/topic/v1/service-portal/overview  body={}
  → HTTP 200 code=0（mock KPI + gap Q-SVC-010）

POST /api/svc/topic/v1/service/search/orgs  body={"page":1,"size":5}
  → HTTP 200 code=0 total=3
```

**DoD 满足**：外网 `/api/svc/topic/v1/**` 不再 404；命中 topic-svc（有 `X-Trace-Id`）；E1 可解阻复测。

## 联调确认

联调通过：外网 `/api/svc` health/overview/search 均 HTTP 200 + `code=0` + `X-Trace-Id`；E1 网关 404 阻塞解除。

## CI/CD

| 项 | 值 |
|----|-----|
| 分支 | `dev` |
| commit | `fdd07c7` `[agent:devops-agent]` |
| pipeline | https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5142 |
| helm:chart | https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/22486 |
| search-py | https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/jobs/22467 |
| 本机 | 无 kubeconfig；以外网 50892 为准 |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~8 万 |
| actual_cost | 估 <$5 |
| cost_warn | false |

## 架构合规

| 铁律 | 结果 |
|------|------|
| 调用链 | ✅ nginx→gateway→topic-svc→search-py `/internal/gkx-svc` |
| D12 | ✅ 无 demo-* |
| StripPrefix | ✅ 路由未再加 StripPrefix |
| 可观测 | ✅ `X-Trace-Id` / `traceparent` |

## 遗留

- E1 QA 复测金路径；本单不替 QA 写「五条全绿」。
