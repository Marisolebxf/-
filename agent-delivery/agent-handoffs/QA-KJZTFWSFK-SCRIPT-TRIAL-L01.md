# QA-KJZTFWSFK-SCRIPT-TRIAL-L01

| 项 | 值 |
|---|---|
| 角色 | agent:qa-agent |
| 监管 | human:黄敬洲 |
| 认领 | coordinator_dispatch（MCP `task-claim` 未写入 `claim_type` 字段，记在任务 note） |
| ponytail | full |
| 日期 | 2026-10-22 |

## 范围与实现

无头试跑 `chain.basic` 金样五条。环境 `https://edu.itic-sci.com/dma/algovwz/`。口令只读 `agent-delivery/qa/as-built/tools/.env.local` 的 `ALGO_LOGIN_USER` / `ALGO_LOGIN_PASSWORD`，未写入仓库。

最终一轮（`runs/金样-algovwz-chain-basic`）：**pass 3 / fail 2 / blocked 0**，约 23 秒。

- FUNC-00002、FUNC-00024、FUNC-00025 通过。
- FUNC-00001 失败：返回有 `chain_id`、`chain_name`、`description`，没有文档示例里的 `cluster_name`、`map_status`。口径以文档示例为准，断言不改。
- FUNC-00004 失败：`chainId` 已清空，画面仍有 `total_revenue`，没有缺参说明。文档将该字段标为必填，实现未校验则本条保持失败。未标必填的字段才把留空理解为查全部。

点击优化（写在 runner，不改用例册）：

- 接口下拉只点已打开弹层里的 `.arco-select-option`，并滚进 200px 列表。不整页 `getByText`。
- `chainId` 点 `.chain-cascader .arco-select-view`，搜索后点 `.arco-radio`。tag 已是目标 id 则跳过。没有 `.arco-cascader-view`。
- 登录看 `.login-card`，不看地址里有没有 `/login`。同一 hash 再次 `goto` 时刷新页面。
- 临时用 `INB170202`（高端医疗器械）跑过 FUNC-00002，级联点中，tag 为该 id。跑完已改回 `INB1701`，名称表未保留该 id。

未做：铺第二页，改 00001/00004 断言充绿，提交这次改动。

## 偏离

调用类 `exchange.txt` 的 `request_url` 这次是「无」，`response` 抄的是画面 JSON，不是新截到的 HTTP 正文。返回非空，所以没有因空响应记通过。FUNC-00004 画面上的 1 条结果与刚跑过的 FUNC-00002 相同，不能当成「空 chainId 返回了 26 条」。

## 产物清单

- `agent-delivery/qa/as-built/tools/apiview-session.mjs`
- `agent-delivery/qa/as-built/tools/run-apiview.mjs`
- `agent-delivery/qa/as-built/scripts/SDWJSF-KJZTFWSFK/basic/chain-basic/`
- `agent-delivery/qa/algo-lib-api-case-playbook.md` §S2「点击从源码定」
- `agent-delivery/qa/algo-lib-playbook-index.md` S2 行
- `runs/金样-algovwz-chain-basic/`（gitignore，不提交）

## 验收证据

- 最终命令：`node run-apiview.mjs ../scripts/SDWJSF-KJZTFWSFK/basic/chain-basic --only FUNC-00001,FUNC-00002,FUNC-00004,FUNC-00024,FUNC-00025 --run-dir ../runs/金样-algovwz-chain-basic`
- 结果：pass 3 / fail 2 / blocked 0。三条调用类都有 `exchange.txt`，`response` 非空。
- `node apiview-session.mjs` → `apiview-session ok`
- `--check`：5 条脚本，assert 编译错误 0
- 口令未出现在 yaml、playbook、handoff

## 架构合规自检

- 算法仍只在 Python，本单只改测试 runner 和脚本 ✅
- 调用链未改，脚本只操作联调台页面 ✅
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
