# POL-L2-DS12-SIM-238-ASYNC · D 波次 · 实现

- 总单：`POL-L2-DS12-SIM-238-ASYNC-L01`

## 交付

| 层 | 变更 |
|---|---|
| Python | `polan/sim_focus_job.py`；`job.py` 注册 `policy_sim_focus` |
| Java | `PolicyAnalysisTypes.SIM_FOCUS`；evaluation jobs 白名单；adapter/types 单测 |
| FE | 检索选策 +「可视化展示」→ 建任务 → 读回画导图/柱图；业务态文案 |

## 自检

- `python -m polan.sim_focus_job` → `sim_focus_job self-check ok`
- FE-POL-03A focus 相关断言（exportHtmlDoc 既有红不属本单）
