# DEVOPS-LUMEN-HELM-CHART-ONLY-L01 · lumen 增加 helm:chart

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 对照 demo `DEVOPS-DEMO-HELM-CHART-ONLY-L01`。长任务不必再问。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 新手动 job + hook 开关；不改 Java、不灌口令。未点 `helm:deploy`。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | CI/helm 开关。 |

## 问题清单

- lumen `helm:deploy` `needs` 一批 Java 镜像，并把 `global.imageTag` 打成当前 SHA，全量滚动。
- 只改 chart/values（ETL 钉 SHA、关开关）时没有 chart-only 入口。
- Nacos hook 每次 upgrade 默认 `post-upgrade`，可能盖掉现网配置。

## 修改内容

- 新增手动 job `helm:chart`：只 `needs: helm:lint`，`HELM_CHART_ONLY=true`
- `k8s-deploy.sh`：chart-only 走 `--reuse-values`，不 `--set global.imageTag`，不 `--wait`；仍保活现网 ETL SHA
- `nacosConfigInit.runOnUpgrade: false`：upgrade 默认不跑 post-upgrade hook
- `.helm_kube` 抽出给 `helm:deploy` / `helm:chart` 共用

## 测试结果

- 代码已推 `origin/dev` `149c2db`
- **请点 lumen-svc-platform pipeline 的 `helm:chart`**，不要点 `helm:deploy`
- 验收：release 升 rev、`STATUS=deployed`；Java `global.imageTag` 不变；ETL 仍 `lumen-etl-es-py:2ac38573`；无新的 `nacos-config-init` Job

## 遗留风险

- `helm:chart` 是 manual，FULL_PIPELINE 不会自动跑它。
- 需要把 chart configs 再灌进 Nacos 时设 `nacosConfigInit.runOnUpgrade=true` 再点 `helm:chart` 或 `helm:deploy`。
- `topic-chain` / `topic-async-service` 在 origin/dev 仍自动 `deploy:*`（与本叶无关）。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `origin/dev`
- commit：`149c2db`
- pipeline：push 后出现；**只点 `helm:chart`**
- 部署 namespace：`dev`
- K8s rollout：待 `helm:chart` 绿

## 可观测性（建议）

- 未改 OTel

## 涉及文件

- `lumen-svc-platform/.gitlab-ci.yml`
- `lumen-svc-platform/scripts/k8s-deploy.sh`
- `lumen-svc-platform/helm/gkxlumen-platform/values.yaml`
- `lumen-svc-platform/helm/gkxlumen-platform/templates/nacos-config-init.yaml`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 | ✅ 未把正式链指回 demo |
| 算法只在 Python | ✅ 未改算法 |
| 调用链 FE→Java→Python | ✅ 未改 |
| 禁止把口令写入新文档 | ✅ |
| D8/D9/D10 | N/A |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 24000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.20 |
| cost_warn | green |
