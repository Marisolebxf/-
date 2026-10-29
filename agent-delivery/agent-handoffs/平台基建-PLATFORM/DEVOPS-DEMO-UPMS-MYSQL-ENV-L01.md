# DEVOPS-DEMO-UPMS-MYSQL-ENV-L01 · upms 注入 MYSQL_PASSWORD

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 21879 `deploy:upms` 红。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只给 upms 补两个 env，口令走已有 Secret。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 两行 env。 |

## 问题清单

- 21879：`kubectl set image ...:a0a554ff` 成功，`rollout status --timeout=5m` 超时。
- 新副本 CrashLoop：连 `gkxx` 被拒。Nacos `gkx-upms-biz-dev.yml` 是 `${MYSQL_PASSWORD}` 占位，Pod 未注入该变量，走了 chart 占位默认值。
- `deploy:upms` 只换镜像，补不了 env。不要再点它。

## 修改内容

- `values.yaml` `microservices.upms.env`：`MYSQL_USERNAME=root`，`MYSQL_PASSWORD` from `demo-platform-mysql` / `mysql-root-password`
- 现网已 patch 同两项，等新副本 Ready 后用 **helm:chart** 把 release 对齐（不要 helm:deploy）

## 测试结果

- `helm:chart` **21920 绿**（18s，`34860e8`）
- 现网 **rev 29 deployed**；`demo-platform-upms-6668f87896` **1/1 Running**；旧副本 Terminating
- Deployment env 含 `MYSQL_USERNAME` / `MYSQL_PASSWORD`（Secret）；`etlEsPy.enabled=false`；`imageTag=08f6ca9e`

## 遗留风险

- 若 Secret 里的口令与 10.50.11.76 `gkxx` 仍不一致，新副本还会拒。那时要改 Secret / `mysql.rootPassword`，不要把口令写进 Nacos 文档。

## CI/CD（必填）

- 分支：`demo-svc-platform` `origin/dev`
- commit：`34860e8`
- 部署：点 **helm:chart**，不要点 `deploy:upms`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 口令不进新文档 | ✅ Secret 引用 |
| D12 | N/A |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 14000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.12 |
| cost_warn | green |
