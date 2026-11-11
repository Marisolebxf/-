# DevOps handoff：DEVOPS-LUMEN-OTEL-TEMPO-RECOVER-L01
- 时间：2026-11-12
- 监管人：human:淮政玮
- 仓库：lumen-svc-platform（helm/gkxlumen-platform）
- commit：`ca8e6cdd`（collector/Tempo 资源与限流）、`2459016b`（Tempo readinessProbe），均已推 `origin/dev`
- 镜像：未变（collector 0.126.0 / tempo 2.7.1）
- ponytail: full — 仅改 helm 模板 + values 默认值，不新增 chart/脚本/依赖；线上用 kubectl patch 对齐模板（release 无 otelCollector/tempo 覆盖值，下次 helm:chart 与此一致）
- cost：actual_tokens≈90000 / model_used=claude-sonnet / actual_cost≈$1.5 / cost_warn=false

## 根因
1. `otel-collector.yaml` 的 `memory_limiter.limit_mib` 硬编码 256（容器 limit 1Gi）：进程长期顶 soft/hard limit，持续 GC、拒收/丢 span，`gkxlumen-display` exporter 几乎全失败。
2. Tempo `limits.memory=1Gi`，2026-11-11T03:39Z 被 OOMKilled（restarts=5）；WAL 在容器可写层（重启即丢）；无 readinessProbe，重启后约 1 分钟内 `/ready`=503 期间 collector 照样导出 → 失败丢 span。

## 改动摘要
| 文件 | 改动 |
|---|---|
| `templates/otel-collector.yaml` | `limit_mib`/`spike_limit_mib` 改读 `.Values.otelCollector.memoryLimiter`（默认 1024/256） |
| `values.yaml` otelCollector | `memoryLimiter.limitMib=1024 spikeLimitMib=256`；resources req 512Mi / lim 1536Mi（limit_mib≈lim 的 2/3） |
| `values.yaml` tempo | req 768Mi / lim 2Gi；新增 `goMemLimit=1600MiB` |
| `templates/tempo.yaml` | env `GOMEMLIMIT`；`/tmp/tempo` 挂 emptyDir（WAL 随同 Pod 重启保留）；加 `/ready` readinessProbe |

demo 平面：未动 demo release（`demo-platform`，chart gkx-platform）；values.yaml 是 lumen chart 默认值，demo 若用同 chart 升级会带上新默认（更大 limit，无风险）。

## 线上操作（ns=zhipu-tts，经 SSH MCP 10.50.69.111）
- patch cm `gkxlumen-platform-otel-collector-config`（limit_mib 1024 + spike 256）、deploy collector/tempo resources、Tempo env/volume/readinessProbe，滚动重启；kubeconfig 副本已删。
- 未执行 helm upgrade、未碰 Nacos、未删任何资源。
- 注意：该 cm 为 CRLF 行尾，按行替换需正则兼容 `\r`。

## 验收证据
- Tempo lumen `:30202/ready` = 200（最终滚动后）；demo `:30200/ready` = 200
- `tempo_distributor_spans_received_total`：滚动后 1408→1865（25s）；最终 140→3346（30s，新 Pod 重新计数）
- 经网关 `:30895/actuator/health` 携带自生成 traceparent（网关响应头无 X-Trace-Id）：
  - `2e9c8ddfddb095a265a11df792220141` → `GET :30202/api/traces/<id>` = 200（含 gkxlumen-gateway）
  - `1d7713614b6d07f1b0051b6f07a95b0b`（Tempo 再次滚动后）= 200
- 内存：collector ≈102Mi/1536Mi，Tempo ≈68Mi/2Gi
- Loki 未专项验证。

## 残留风险
- 断窗期历史 trace（含 `e93ad7e945ad35dafc98e2dde08385b5`）无法找回。
- collector 最近 300 行日志仍有 16 行 `Dropping/Exporting failed/memory limit` 关键字匹配；因已删 kubeconfig 未细分，已知原因含 `prometheusremotewrite`（`prometheus.monitoring:9090` 写入失败，与 limiter 无关，需运维另查）。
- demo 平面 Tempo 也曾 restarts=9，同类 OOM 风险未处理（本任务范围外）。
- 下次 `helm:chart` 手动发布时应与线上一致；若 values-lumen 将来覆盖 resources，须同步 memoryLimiter。
- Tempo emptyDir WAL 仅在同 Pod 容器重启时保留，Pod 被重建仍会丢（无 PVC）。

## 架构合规自检
- 调用链/算法/Neo4j：不涉及 ✅；可观测：恢复 OTel→Tempo ✅；D12：lumen 未调 demo ✅；secret：无入 git ✅；FORCE_NACOS_REPUBLISH：未用 ✅；资源 req/limit：有 ✅
- 回滚：`kubectl -n zhipu-tts rollout undo deploy/gkxlumen-platform-tempo`（collector 同理，cm 需手改回 256）；仓库 `git revert 2459016b ca8e6cdd`
