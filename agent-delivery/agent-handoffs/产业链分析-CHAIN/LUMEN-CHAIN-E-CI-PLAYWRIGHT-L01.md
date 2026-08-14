# LUMEN-CHAIN-E-CI-PLAYWRIGHT-L01 · 产业链金路径进 GitLab Playwright

> 格式参考 `templates/handoff-template.md`。2026-08-14 `human:淮政玮` 拍板：段 E 金路径进 GitLab Playwright。本单不改业务 Vue。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权不必再问；lock 24h。tech_task 完工转 **ready_to_sign**，不标 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | `@playwright/test` 只进 `e2e/` 子包，不进根 `package.json`（避免拖慢 `frontend:build`）。未扩成全量 USM / 视觉回归。未用 YAGNI 跳过 D12 / wait_view / 期望未发生必红。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | CI YAML + 五条规格，未挂载 compress。 |

## 问题清单

- Runner 若拉不到 `mcr.microsoft.com/playwright:v1.51.0-jammy` → **C2**。把镜像推进 Harbor 后改 CI 变量 `PLAYWRIGHT_IMAGE`。
- `lumen-ui-topic` 须放行 inbound job token（`gkx-lumen/lumen-algo-py`、`gkx-lumen/lumen-svc-platform`），否则跨仓 trigger 403 → **C2**。
- 首轮 `e2e:chain-gold` 绿否以 push 后 GitLab 为准；本 handoff 提交时尚未等 Pipeline。

## 修改内容

- `lumen-ui-topic/e2e/`：独立 Playwright 1.51，总控 §4 五条；`E2E_BASE_URL` 禁止 localhost。
- `lumen-ui-topic/.gitlab-ci.yml`：stage `e2e`，`deploy:k8s` 绿后 `e2e:chain-gold`；`CHAIN_GOLD_ONLY=true` 跳过 build/image/deploy/trivy。
- `lumen-algo-py`：`deploy:api` + `deploy:worker` 绿后 trigger `gkx-lumen/lumen-ui-topic` `e2e:chain-gold`。
- `lumen-svc-platform`：`deploy:topic-chain` + `deploy:topic-async-service` 绿后同样 trigger。
- 规约 **v1.8**：删「金路径不进 GitLab Playwright」；CI 绿 = 本轮 E1/复测；QA 子智能体改为抄 trace / 失败分类兜底。

复测失败故事：父 Pipeline 变量 `CHAIN_GOLD_GREP=#4` 或 `CHAIN_GOLD_STORY=4`。

## 测试结果

- 用例文件：`e2e/chain-gold.spec.ts`（#1 检索同类型锁 · #2 总览经 Java · #3 全景默认无「开始分析」· #4 wait_view · #5 深圳发展负例）。
- 本机未在 Windows 跑 Playwright（Runner 是 Linux docker）；以 GitLab job 为证据。
- 联调确认：规约与三仓 CI 已对齐；**等** `e2e:chain-gold` 首跑。

## 遗留风险

1. mcr 镜像 / job token 放行见问题清单（失败分类 **C2**，不派业务修）。
2. #4 会真 Create Job（约 6–10s）；Job failed 按规约 §11.3 **必红**。
3. 未把 A–D feature 标 done。

## CI/CD（必填）

- 分支：三业务仓 `origin/dev`；编排仓 `origin/dev`
- commit：
  - `lumen-ui-topic` `8e779d5`
  - `lumen-algo-py` `41ce60d`
  - `lumen-svc-platform` `e831a69`
  - 编排仓 `cd3d54d`
- pipeline：
  - https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines
  - https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/pipelines
  - https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines
- 部署 namespace：`dev`（topic 本次 CI YAML 会再滚一次 `deploy:k8s`，随后跑 `e2e:chain-gold`）
- K8s URL：http://192.168.88.50:30892
- 金路径 job：`e2e:chain-gold`（首跑进行中，未在本 handoff 内等绿）

## 可观测性（建议）

- 失败时 Playwright trace 在 job artifact（`e2e/test-results`）；QA 再抄页面 `X-Trace-Id` → Tempo `http://192.168.88.50:30201`

## 涉及文件

- `${GKX_ROOT}/repos/lumen-ui-topic/e2e/*` · `.gitlab-ci.yml` · `.gitignore`
- `${GKX_ROOT}/repos/lumen-algo-py/.gitlab-ci.yml`
- `${GKX_ROOT}/repos/lumen-svc-platform/.gitlab-ci.yml`
- `agent-delivery/长任务执行规约.md` v1.8 及总控 / cicd / 手册 / 公约 / coordinator·qa·devops mdc

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未改算法 |
| 2 调用链 前端→Java→Python `/internal/*` | ✅ 金路径只点已发布前端，经 `/api/` |
| 3 图谱 Nebula | N/A |
| 4 可观测 | ✅ 失败走 artifact + Tempo；未删埋点 |
| 5 CI/CD | ✅ 金路径进 GitLab；`cicd: skip` 不适用 |
| 6 demo2 merge | ✅ 未 merge demo |
| 7 共享聚合核心 | N/A |
| 8 数据策略 ADS | ✅ 仍读已发布链路 / `demo_gkxlumenx_*` |
| 9 D8 Design | ✅ 未改 UI |
| 10 D9 血缘 | ✅ 未删 ⓘ |
| 11 D10 交互 | ✅ wait_view / 混选锁 / 深圳负例写入断言 |
| 12 D12 demo/lumen 隔离 | ✅ spec 拦截 `/api/*` 打到 `demo-*` |

## cost 四字段（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 待回填（本会话） |
| model_used | Cursor Grok 4.6 |
| actual_cost | 待回填 |
| cost_warn | green（估 < $10） |
