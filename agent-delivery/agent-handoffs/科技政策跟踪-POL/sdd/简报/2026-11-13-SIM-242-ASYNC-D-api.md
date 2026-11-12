# POL-L2-DS12-SIM-242-ASYNC · D 波 · Java 白名单切片

- 总单：`POL-L2-DS12-SIM-242-ASYNC-L01`
- 角色：`agent:api-agent`
- 日期：2026-11-13

## 交付

| 层 | 变更 |
|---|---|
| Java async | `PolicyAnalysisTypes.SIM_INTERPRET`（`policy_sim_interpret`）进 CANONICAL / WHITELIST；`skipsIndustryVidXor=true`（同 238） |
| Java display | `PolicyEvaluationService.JOB_SUB_TYPES` 放行，evaluation/jobs 可透传 async |
| 单测 | `PolicyAnalysisTypesTest` 十四键 + skips/canonical；`PolicyAnalysisAdapterImplTest` 注册含新键 |
| 明确不做 | 未改 `simulation/jobs` 读面；未动解读报告 element 查询 |

## 自检

- 本机无 `mvn`/`java`，未跑本地 surefire；改动同构 `policy_sim_focus`（`6f939423`），断言覆盖键存在。
- CI / 有 JDK 环境：`-Dtest=PolicyAnalysisTypesTest,PolicyAnalysisAdapterImplTest`
