# DEVOPS-LUMEN-PLATFORM-DEPLOY-FIX-L01 handoff

> **状态**：待 coordinator 验收 → `done`  
> **执行**：agent:devops-agent · **监管**：human:淮政玮  
> **日期**：2026-07-17

---

## 1. 范围与实现

修复 `lumen-svc-platform` `helm:deploy` 失败，且与同 ns=`dev` 的 **demo-platform** 隔离并存（不复用 demo NodePort/Secret）。

| 项 | demo-platform | gkxlumen-platform（本任务） |
|----|---------------|------------------------------|
| Tempo NodePort | 30200 | **30201** |
| Loki NodePort | 30310 | **30311** |
| MinIO Secret | `gkx-platform-minio` | **`gkxlumen-platform-minio`** |
| Nacos 镜像 | `gkx-register:c3c99e09` | **钉死** `gkx-register:c3c99e09`（勿套业务 commit SHA） |

代码改动（`lumen-svc-platform`）：

- `helm/gkxlumen-platform/values-lumen.yaml` — 隔离 NodePort / Secret / nacos tag
- `scripts/create-minio-secret.sh` — 默认 Secret 名改为 `gkxlumen-platform-minio`
- `helm/gkxlumen-platform/DEPLOY-LUMEN.md` — demo vs lumen 对照 + CI 触发说明修正

---

## 2. 验收证据（发布成功版 = 隔离修复，不含后续 Nacos 提交）

| 证据 | 值 |
|------|-----|
| Pipeline | [#4337](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/4337) |
| Job | `helm:deploy` **#17591 success** |
| Commit（集群 as-built） | **`ebe4684f`**（`Merge branch 'feat/DEVOPS-LUMEN-PLATFORM-DEPLOY-FIX-L01' into dev`） |
| Helm | `gkxlumen-platform` ns=`dev` **STATUS=deployed** revision=2 |
| 业务镜像 | `gkxlumen-{auth,gateway,innov,metrics,topic,upms}:ebe4684f` 均 Ready |
| 隔离核对 | demo Tempo/Loki 仍为 30200/30310；lumen 为 30201/30311 |

> **说明**：git `dev` 上另有后续提交 `a15130c`（Nacos v1 API 兼容 + `MYSQL_PASSWORD` 注入），**尚未**经 `helm:deploy` 发布到集群。当前线上 = **ebe4684**（用户确认的「发布成功 / 发布前版本」）。

---

## 3. 偏离 / 已知后续

1. **首次 install** 曾 `context deadline exceeded`（`upms` 缺 Nacos 灌入的 datasource）；运维侧临时 `kubectl set env` 注入 `SPRING_DATASOURCE_*` 后 `--wait` 通过。  
2. **`a15130c`** 已推 `dev`（chart 内修复 Nacos config-init 探活 + compatibility + MYSQL_PASSWORD），Pipeline [#4338](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/4338) 的 `helm:deploy` **仍为 manual**，默认不覆盖当前 `ebe4684` 运行态。  
3. 下次全量 `helm:deploy`（`a15130c` 或更新）前，建议确认 Nacos config-init 已能灌入 `gkxlumen-upms-biz-dev.yml`，避免再次依赖手工 env。

---

## 4. 架构合规自检（节选）

| # | 铁律 | 结果 |
|---|------|------|
| 调用链 | 前端→Java→Python | ✅ 未改 |
| Nebula / 算法边界 | — | ✅ 未触及 |
| CI/CD | push→Pipeline→K8s | ✅ #4337 helm:deploy 绿 |
| demo 隔离 | 不抢 demo NodePort/Secret | ✅ |
| 可观测 | OTel/Tempo/Loki 独立 NodePort | ✅ |

---

## 5. Cost（估算）

| 字段 | 值 |
|------|-----|
| `actual_tokens` | 180_000 |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | 1.20 |
| `cost_warn` | green |

---

*devops-agent · DEVOPS-LUMEN-PLATFORM-DEPLOY-FIX-L01 · 2026-07-17*
