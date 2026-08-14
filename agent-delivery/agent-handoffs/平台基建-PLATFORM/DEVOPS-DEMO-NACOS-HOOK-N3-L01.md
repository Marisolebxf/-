# DEVOPS-DEMO-NACOS-HOOK-N3-L01 · demo nacos hook 对齐 Nacos 3

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（长任务总控） |
| 说明 | job 21724 红：hook 探 `/v1/console/health/readiness` → 410。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对照复制 lumen 已绿脚本，不另发明探活。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 单文件 hook。 |

## 问题清单

- Nacos 3：`/nacos/v1/console/health/readiness` = **410 Gone**；`/` 与 `/actuator/health` = 200。
- demo hook 60×5s 空转，Job `OnFailure` 重启，helm `--wait 10m` 必红。下午 rev 19–24 同一错误。
- lumen 模板已改为探 `$NACOS_BASE/` + v3 Admin publish，所以 lumen `helm:deploy` 能绿。
- values 曾写「hook 失败不阻塞主部署」，与 `--wait` 不符。

## 修改内容

- `helm/gkx-platform/templates/nacos-config-init.yaml`：探活 `/`（200/302）；login；`v3/admin/core/namespace`；`v3/admin/cs/config`。
- `values.yaml`：补 `username`/`password`；注释改为 hook **会**挡住 `--wait`。

## 测试结果

- 模板无 `console/health/readiness`；含 `v3/admin/cs/config`。
- 现网 innov 仍是 `6f73df72` + `demo_gkxlumenx_ads`（21724 失败未回滚掉 jar）。

## 遗留风险

- 需再点一次 **demo-svc-platform `helm:deploy`**（commit `08f6ca9`）验证 hook 绿。release 现为 **failed rev 24**，脚本会先清 pending/failed。
- 不要在 08f6ca9 绿之前重复点 6f73df7 那条旧 pipeline。

## CI/CD（必填）

- 分支：`origin/dev`
- commit：`08f6ca9`
- 部署：ns=`dev` release `demo-platform`；点 `helm:deploy`
- K8s rollout：待本叶 pipeline

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 | N/A（CI hook） |
| 不改 lumen | ✅ 只改 demo chart |
| D8/D9/D10 | N/A |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 22000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.2 |
| cost_warn | green |
