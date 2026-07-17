# DevOps handoff：DEVOPS-TOPIC-PY-CICD-L01

- **时间**：2026-07-17
- **执行**：`agent:devops-agent` · **监管**：`human:淮政玮`
- **仓库**：
  - `demo-svc-topic-py` @ `1c1b8b0`（dev）
  - `demo-svc-platform` @ `6259144`（dev，helm searchPy）
- **产物**：
  - `.gitlab-ci.yml`（py:smoke → py:image → deploy:search-py）
  - `docker/Dockerfile.search`（python-algo-base + opentelemetry-instrument）
  - `k8s/dev-search-py.yaml`（bootstrap）
  - `docs/DEPLOY-K8S.md`
  - helm：`templates/search-py.yaml` + `values.yaml#searchPy` + `values-demo.yaml`
- **CI**：https://gitlab.htmisoft.net/gkx-lumen/demo-svc-topic-py/-/pipelines/4335 （success）
- **镜像**：`harbor.htmisoft.net/gkx/gkx-search-service:1c1b8b0b`
- **K8s**：`dev` / Deployment `demo-platform-search-py`（bootstrap apply 后 rollout 成功）
- **冒烟**：in-pod `GET /healthz` → `{"status":"ok","service":"gkx-search-service","mock_enabled":true}`
- **NodePort**：`30805`（bootstrap / values）
- **OTel**：镜像 ENTRYPOINT `opentelemetry-instrument`；env 指向 collector
- **资源**：requests 100m/256Mi · limits 1CPU/1Gi
- **回滚**：`kubectl -n dev rollout undo deployment/demo-platform-search-py`
- **范围**：仅 search；ai/analytics/graph 未构建
- **后续**：正式态建议在 platform 执行 `helm upgrade` 启用 searchPy，与 bootstrap 标签对齐后改走纯 set image

## 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ |
| 2 | 调用链 /internal/* | ✅ 前缀 `/internal/gkx-search/**` |
| 3 | NebulaGraph | ✅ 配置保留；本任务未改图谱 |
| 4 | OTel | ✅ instrument + OTEL_* |
| 5 | CI Pipeline 绿 | ✅ #4335 |
| 6 | demo 仓策略 | ✅ 推 origin/dev |
| 7 | Java 不写算法 / 不直连 nGQL | ✅ N/A 本仓 Python |
| 8 | secret 不入 git | ✅ 沿用 CI 变量 / 既有集群 secret |
| 9–10 | Design/血缘 | ✅ N/A 本任务运维 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 120000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.70 |
| cost_warn | green |
