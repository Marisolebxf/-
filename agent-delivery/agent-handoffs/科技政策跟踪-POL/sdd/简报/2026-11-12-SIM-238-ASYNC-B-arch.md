# POL-L2-DS12-SIM-238-ASYNC · B 波次 · arch

- 总单：`POL-L2-DS12-SIM-238-ASYNC-L01`
- 日期：2026-11-12
- 档位：**重**
- 输入：A product；计划同构 237 C

## 1. 定档与层清单

| 层 | 动作 |
|---|---|
| Python | 新 `polan.sim_focus_job`；`JOB_SUB_TYPES` 加 `policy_sim_focus` |
| topic-async | `PolicyAnalysisTypes.SIM_FOCUS`；`skipsIndustryVidXor`；校验 `policy_id` |
| display | `PolicyEvaluationService.JOB_SUB_TYPES` 收新键；FE 经 `evaluation/jobs` 建任务 |
| element | **不改** SELECT；任务成功后 FE 仍 `jobs·重点可视化` 只读 gapfill |
| FE | 检索 + 按钮建任务 + loading + 读回画图 |
| gapfill | 单政策 DELETE+INSERT 或按 group upsert 重点行；**禁** TRUNCATE/整表清空 |

## 2. 读法 / 写法

```text
浏览器 → POST /display/v1/policy/evaluation/jobs
  { sub_type: policy_sim_focus, params: { policy_id }, analysis_fp }
  → topic-async → POST /internal/policy/jobs/execute
  → sim_focus_job：读 DWD 正文 → LLM → upsert gapfill 重点四行
  → 终态 success
浏览器 → POST /display/v1/policy/simulation/jobs { kind: 重点可视化, policy_id }
  → element 只读 gapfill → 导图/柱图
```

只读 `jobs·重点可视化` **并存**（读已有行 / 当天复用）；真算只走 evaluation/jobs。

## 3. 契约钉死

- Job 键：`policy_sim_focus`（全名，无裸别名）
- 入参：`params.policy_id`（必填）；`force=true` 可重算
- 出参：result 含 `generated` / `policy_id` / 行摘要；权威数据在 gapfill
- 柱图列：仍 `score_value`；不新 metric_id；不挂焦点指数

## 4. 不做

浏览器直连 Python；demo 服务；239–242 本单扩真算；`polan.text.parse.run` 式整表清空。

## 5. B 波收口

→ C 轻会签 + D 实现。
