# QA-KJZTFWSFK-RUNNER-APIVIEW-L01

| 项 | 值 |
|---|---|
| 角色 | agent:qa-agent |
| 监管 | human:黄敬洲 |
| 认领 | coordinator_dispatch（MCP `task-claim` 未写入 `claim_type` 字段，记在本表与任务 note） |
| ponytail | full |
| 日期 | 2026-10-22 |

## 范围与实现

按 `algo-lib-api-case-playbook.md` §S2 把算法库 runner 从专题入口拆开。

- 专题仍走 `run-scripts.mjs`：登录、`ensureReviewOff`、基址拼接保持原样。
- 算法库走 `run-apiview.mjs`。无头默认开启。
- `/login` 用 `ALGO_LOGIN_USER` / `ALGO_LOGIN_PASSWORD` 点「进入算法库」。不关内部评审。
- `goto` 目标 `#/path` 或 `/path` 拼成 `{base_url}#/path`，`base_url` 必须含 `/dma/algovwz/`。
- 动作：`algo_tab`、`algo_pick`、`algo_fill`、`algo_run`。`chainId` 走级联。
- `algo_run` 写 `scripts/{id}/exchange.txt`（path、params、response）。返回为空则该条不得 pass。
- 读册、断言、每步截图、`result.yaml` / `steps.md` 在 `runner-core.mjs`，两个入口都用。

未做：金样 yaml、联调台试跑、用例册回填。

## 偏离

开工时曾把算法库做成 `run-scripts.mjs` 里的 profile。随后按入口隔离改成 `run-apiview.mjs`，专题文件收回原行为，只把读册和结果文件抽到 `runner-core.mjs`。`claim_type` 没进 registry 字段，是 MCP `task-claim` 没有这个参数。

## 产物清单

- `agent-delivery/qa/as-built/tools/run-apiview.mjs`
- `agent-delivery/qa/as-built/tools/apiview-session.mjs`
- `agent-delivery/qa/as-built/tools/runner-core.mjs`（专题入口改为引用它）
- 索引与 playbook 成熟度改成「runner 已落地，金样未开」

## 验收证据

- `node apiview-session.mjs` → `apiview-session ok`
- `node run-apiview.mjs <临时目录> --check`：1 条脚本，assert 编译错误 0
- 缺 `ALGO_LOGIN_*`、`base_url` 不含 `/dma/algovwz/`：`run-apiview.mjs` 退出码 2，未开浏览器
- 专题 `node run-scripts.mjs .../industry-center/overview --check`：17 条，assert 编译错误 0（不读算法库环境变量）
- 未对 `https://edu.itic-sci.com/dma/algovwz/` 试跑

## 架构合规自检

- 算法仍只在 Python，本单不写算法 ✅
- 调用链未改，runner 只驱动联调台页面 ✅
- 未使用 Neo4j ✅
- 未改业务可观测埋点 ✅
- 未 push，未改 CI ✅
- 未把 demo 并进 lumen ✅
- 未写对象存储桶 ✅
- 未让 lumen 前端调用 demo 服务 ✅

## Cost 回填

- actual_tokens: 未从计费接口读取
- model_used: grok-4.7
- actual_cost: 0
- cost_warn: green
