# QA-KJZTFWSFK-SCRIPT-CHAIN-BASIC-L02

| 项 | 值 |
|---|---|
| 角色 | agent:qa-agent（父控派单 + 验收） |
| 监管 | human:黄敬洲 |
| 认领 | coordinator_dispatch（MCP `task-claim` 未写入 `claim_type` 字段，记在本表与任务 note） |
| ponytail | full |
| 日期 | 2026-10-23 |

## 范围与实现

按 `algo-lib-api-case-playbook.md` §S2 补齐 `chain.basic` 调用类脚本 **FUNC-00003、00005～00023**（共 20 条），对照金样 FUNC-00002 / FUNC-00004 形态；用例册仅回填「自动化用例ID」；`coverage.md` 补全 25 条映射。

- 子 agent 执行写 yaml；父控不写 yaml，仅调度与验收。
- 金样五条（FUNC-00001、00002、00004、00024、00025）断言未改；`index.yaml` 的 `gold` / `all` 仍为原五条。
- `fixtures/testdata.yaml` 的 `base_url` 仍为 `https://edu.itic-sci.com/dma/algovwz/`。
- 未试跑浏览器、未写 `runs/`。

## 偏离

无。`index.yaml` 的 `all` 仍只列金样五条（铺开前口径）；任务指定 `--check` 命令仅编译 index 内 5 条，父控另对新增 20 条逐条 `--only` 自检 assert 编译均为 0。

## 产物清单

- `agent-delivery/qa/as-built/scripts/SDWJSF-KJZTFWSFK/basic/chain-basic/cases/FUNC-00003.yaml`
- `agent-delivery/qa/as-built/scripts/SDWJSF-KJZTFWSFK/basic/chain-basic/cases/FUNC-00005.yaml`～`FUNC-00023.yaml`（共 20 个新增）
- `agent-delivery/qa/as-built/scripts/SDWJSF-KJZTFWSFK/basic/chain-basic/coverage.md`
- `agent-delivery/qa/test-cases/SDWJSF-KJZTFWSFK/basic-基础指标/CHAINBASIC-产业链基础指标/FUNC-产业链基础指标-用例.md`（自动化用例ID 列）

## 验收证据

- `cd agent-delivery/qa/as-built/tools && node run-apiview.mjs ../scripts/SDWJSF-KJZTFWSFK/basic/chain-basic --check` → **5 条脚本，assert 编译错误 0 处**
- 新增 20 条逐条 `--only FUNC-00xxx --check` → 各 **编译错误 0**
- cases 目录共 25 条 yaml；无 `allow_skip`；新增条均为 `tier: A`
- `git diff` 金样五条 yaml 为空

## 架构合规（D1–D12）

| 铁律 | 结论 |
|------|------|
| 未读 lumen-algo-py / demo-algo-* | ✅ |
| 未浏览器试跑 / 未改专题脚本 | ✅ |
| 编排仓 QA 资产，无越层调用 | ✅ |
| 未提交 runs/、.env | ✅ |

## cost

| 字段 | 值 |
|------|-----|
| model_used | Composer（本会话） |
| actual_tokens | （未精确计量） |
| actual_cost | 0 |
| cost_warn | green |
