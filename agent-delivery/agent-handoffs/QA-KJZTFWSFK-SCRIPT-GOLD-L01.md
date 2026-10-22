# QA-KJZTFWSFK-SCRIPT-GOLD-L01

| 项 | 值 |
|---|---|
| 角色 | agent:qa-agent |
| 监管 | human:黄敬洲 |
| 认领 | coordinator_dispatch（MCP `task-claim` 未写入 `claim_type` 字段） |
| ponytail | full |
| 日期 | 2026-10-22 |

## 范围与实现

按 `algo-lib-api-case-playbook.md` §S2 写 `chain.basic` 金样五条，给 `run-apiview.mjs` 用。

- FUNC-00001 无参列表，FUNC-00002 填 chainId=INB1701、statYear=2025，FUNC-00004 省略 chainId。
- FUNC-00024 / FUNC-00025 是页面清单，不用 `algo_*`，不点「执行接口」。
- 五条用例只回填了「自动化用例ID」。
- `node run-apiview.mjs .../chain-basic --check`：5 条，编译错误 0。

未做：联调台试跑，其余 20 条脚本，其它 catalog 页。

## 偏离

runner 单 `QA-KJZTFWSFK-RUNNER-APIVIEW-L01` 仍是待签收，代码已在 `origin/dev`。本单不挂 `depends_on`，否则建不成 ready。

## 产物清单

- `agent-delivery/qa/as-built/scripts/SDWJSF-KJZTFWSFK/basic/chain-basic/`
- `FUNC-产业链基础指标-用例.md` 五条自动化用例ID
- playbook §S2 与索引 S2 行改为金样已写、试跑未开

## 验收证据

- `--check` 完成：5 条脚本，assert 编译错误 0
- 未对 `https://edu.itic-sci.com/dma/algovwz/` 试跑

## 架构合规自检

- 算法仍只在 Python，本单只写脚本 ✅
- 调用链未改，脚本只描述联调台页面操作 ✅
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
