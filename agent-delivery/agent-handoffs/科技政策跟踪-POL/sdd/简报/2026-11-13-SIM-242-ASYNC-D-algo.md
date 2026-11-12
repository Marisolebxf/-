# POL-L2-DS12-SIM-242-ASYNC · D 波次 · algo

- 总单：`POL-L2-DS12-SIM-242-ASYNC-L01`
- 日期：2026-11-13
- 身份：algorithm-agent
- 方案钉：`2026-11-13-SIM-242-LLM-ASYNC-ARCH方案.md` §5
- 对照：`polan.sim_focus_job`（238）

## 交付

| 项 | 值 |
|---|---|
| 仓 | `lumen-algo-py` `origin/dev` |
| commit | `bf0a440f4d0afdcaf8b6fe58f179a6ae10842004` |
| 入口 | `run_sim_interpret(payload)` |
| Job 键 | `policy_sim_interpret`（`polan/job.py` 已注册，`_NO_INDUSTRY_XOR`） |
| 自检 | `python -m polan.sim_interpret_job` → **绿** |

## 行为摘要

1. 读 DWD `title/abstract/content`；可选拼 `ads.policy_text_parse` + gapfill 影响/路径摘要（限长，无行不挡）。
2. LLM → JSON 四段（政策背景/主要内容/预期效果/实施建议）→ 校验；≥1 段非空才写库。
3. 单政策 `DELETE row_kind=解读段落` + `INSERT`；禁整表；无密钥 `degraded=true`、`generated=0` 不造假行。
4. `force`：有行且 `force≠true` 短路返回已有计数（`skipped=true`）；重算必 `force=true`。

## 文件

- 新建 `vendor/entan-py/polan/sim_interpret_job.py`
- 改 `vendor/entan-py/polan/job.py`（白名单 + 分支镜像 focus）

## 下一跳

D 波剩余：Java 白名单 `PolicyAnalysisTypes` + FE create/进度/force/读回。
