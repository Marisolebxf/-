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

- `python -m polan.sim_focus_job` → `sim_focus_job self-check ok`
- FE-POL-03A 48 项全绿（含 focus 真算断言；export 断言已对齐 `exportPolicyReport`）
- `pnpm type-check` 绿

## 遗留风险

- FE 未 push 前线上无检索/真算按钮
- 无 LLM 密钥时 generated=0，读面仍可依赖预灌 18363390
- 237 ASYNC 仍独立进行；本单不阻塞

## CI/CD

- algo `28d6e6f` / Java `6f93942` / orch `2cb7c2a15` → `origin/dev`
- FE 本地 `2bd5aec`（ahead），待人工确认「推」

## 涉及文件

- `polan/sim_focus_job.py`、`polan/job.py`
- `PolicyAnalysisTypes.java`、`PolicyEvaluationService.java`
- `InterpretWorkbench.vue`、`policy.ts` types
- 说明书 / SIM ARCH·API / 合规用例 / 简报 A–E
