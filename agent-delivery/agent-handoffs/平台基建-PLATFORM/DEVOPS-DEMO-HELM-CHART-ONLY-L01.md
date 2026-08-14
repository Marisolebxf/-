# DEVOPS-DEMO-HELM-CHART-ONLY-L01 · chart-only 部署 + upgrade 不重发 Nacos

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 21827 只关 etlEsPy 仍全量打 Java TAG；新 upms CrashLoop。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 新手动 job + hook 开关；不改 Java、不灌口令。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | CI/helm 开关。 |

## 问题清单

- `helm:deploy` `needs` 7 个 Java 镜像，并把 `global.imageTag` 打成当前 SHA。
- Nacos hook 每次 upgrade 重发 chart configs，可能盖掉现网数据源。
- CUTOVER 现网 ETL 已卸；21827 卡在 `--wait` / 重试。

## 修改内容

- 新增手动 job `helm:chart`：只 `needs: helm:lint`，`HELM_CHART_ONLY=true`
- `k8s-deploy.sh`：chart-only 走 `--reuse-values`，不 `--set global.imageTag`
- `nacosConfigInit.runOnUpgrade: false`：upgrade 默认不跑 post-upgrade hook

## 测试结果

- 待 21827 结束后点 **helm:chart**（不要再点 helm:deploy）。未结束时点会撞 pending-upgrade。

## 遗留风险

- 现网 crashloop 的新 upms RS 本叶不删，等 21827 结束再看。
- 需要把 chart configs 再灌进 Nacos 时设 `nacosConfigInit.runOnUpgrade=true`。
- lumen chart 未改（本叶只动 demo）。

## CI/CD（必填）

- 分支：`demo-svc-platform` `origin/dev`
- commit：`bbac3b6`
- 部署：21827 结束后点 `helm:chart`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 | N/A（CI/helm 操作面） |
| 算法只在 Python | ✅ 未改算法 |
| 禁止把口令写入新文档 | ✅ |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 22000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.18 |
| cost_warn | green |
