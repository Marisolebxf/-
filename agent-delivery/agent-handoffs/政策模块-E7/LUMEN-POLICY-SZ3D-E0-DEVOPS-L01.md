# LUMEN-POLICY-SZ3D-E0-DEVOPS-L01 · 深圳政策现状点名发布

> 只核对本管线三仓在 K8s `dev` 的发布。未改业务代码，未改时序 / 区域对比发布范围，未领 E1。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 总控写 E0 依赖 D ≥ `pending_test`。D 停在 `integration`（`5a41dee`），未写「联调通过」。用户本轮要求继续推进，故只做发布核对。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 发布核对，没有业务代码改动，也没有新依赖。 |

## 点名结果

| 服务 | 镜像 | 包含的业务提交 | 证据 |
|------|------|----------------|------|
| `gkxlumen-platform-entan-py` | `gkxlumen-entan-py-api:80f6ed1b` | `7a6f6b24` 是其祖先 | pipeline [2964](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/pipelines/2964) job `deploy:entan-api` 成功。rollout 成功。pod `gkxlumen-platform-entan-py-d5547958f-47kkd` 健康检查 `{"status":"ok"}` |
| `gkxlumen-platform-topic-policy` | `gkxlumen-topic-policy:017671c3` | `982e038` 是其祖先 | pipeline [2963](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/2963) job `deploy:topic-policy` 成功，rollout 成功 |
| `gkxlumen-platform-topic-async-service` | `gkxlumen-topic-async-service:017671c3` | 同上 | 同 pipeline job `deploy:topic-async-service` 成功，rollout 成功 |
| `gkx-lumen-topic` | `gkx-lumen-topic:5a41dee5` | 即 D 叶提交 | pipeline [2968](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-topic/-/pipelines/2968) job `deploy:k8s` 成功，rollout 成功 |

`80f6ed1b`、`017671c3` 是同日模型 Secret 发布提交，业务提交已在其历史上。本轮没有重跑失败的 deploy。

## 已发布前端

- URL：http://10.50.69.111:30892
- `GET /` 返回 200，`Last-Modified: Sun, 25 Oct 2026 07:52:22 GMT`，与 `deploy:k8s` 滚动时间一致。
- 入口脚本 `assets/index-DI4-umAs.js` 加载 `PolicyAnalysisConfigPage-B0ScG1SE.js`。该包含 `data-testid=policy-sz3d-fixed-cards` 与 `data-dim=support|fit|effect`，页摘要为「三张固定卡 + wait_view + 结果板。开始分析只看锚点，不出综合分。」
- Deployment 名是 `gkx-lumen-topic`，NodePort 30892。原型专题前端是 30888。本 URL 不是 `demo-ui-topic`。
- 未在已发布站登录，也未点击开始分析。五条金路径留给 E1。

## 库

本轮 deploy 只 `kubectl set image`，没有改数据源。仓内现行配置仍是：

- 政策读数：`vendor/entan-py/conf/settings_policy.yaml` 的 `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`
- Java 政策服务样例：`gkxlumen-topic-policy-biz-dev.yml` 的 `demo_gkxlumenx_ads`
- 异步任务库样例仍是 `gkxlumenx_topic_enterprise`，这是任务库，不是政策数仓，本轮未改

node01 上的 `kubectl` 打到 Jenkins 登录页，没有从 Pod 环境变量再读一次库名。

## 架构合规

| 铁律 | 结果 |
|------|------|
| 发布目标是 lumen，不是 demo Ingress | ✅ 30892 / `gkx-lumen-topic` |
| 政策数仓不改到正式 `gkxlumenx_*` | ✅ 本轮未改配置；样例仍是 `demo_gkxlumenx_*` |
| 不改时序 / 区域对比发布范围 | ✅ 只核对 entan-api、topic-policy、topic-async、专题前端 |
| 不用 localhost 当发布证据 | ✅ |

## 遗留

- D 仍是 `integration`。这里不补「联调通过」。
- E1 `LUMEN-POLICY-SZ3D-E1-QA-L01` 仍是 backlog。
- `deploy:entan-worker` 不是这条政策执行链（Java 调 entan-api `/internal/policy/jobs/execute`）。worker 未作为本叶门禁。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 20000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |
| 说明 | source: session_estimate。按本叶登记估算 20000，比例沿用 C 叶 60000 token ≈ $0.12。 |
