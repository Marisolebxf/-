# POL-L2-DS12-SIM-238-ASYNC-L01 · 238 异步真算 FDE

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:product-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |

## 修改内容

- A/B/C：界面必见、ARCH/API/`policy_sim_focus`、轻会签
- D：`polan.sim_focus_job` LLM 抽四组+upsert；Java 白名单；FE 检索+建任务+读回画图
- E：合规用例真算路径

## 测试结果

- `python -m polan.sim_focus_job` self-check（仓内 vendor）
- FE-POL-03A：focus 相关断言（exportHtmlDoc 既有红不属本单）
- `pnpm type-check`（science-pc）

## 遗留风险

- FE 未 push 前线上无检索/真算按钮
- 无 LLM 密钥时 generated=0，读面仍可依赖预灌 18363390
- 237 ASYNC 仍独立进行；本单不阻塞

## CI/CD

- algo / Java / orchestration：本 handoff 同批 push `origin/dev`
- FE：本地 commit，待「推」

## 涉及文件

- `polan/sim_focus_job.py`、`polan/job.py`
- `PolicyAnalysisTypes.java`、`PolicyEvaluationService.java`
- `InterpretWorkbench.vue`、`policy.ts` types
- 说明书 / SIM ARCH·API / 合规用例 / 简报 A–E
