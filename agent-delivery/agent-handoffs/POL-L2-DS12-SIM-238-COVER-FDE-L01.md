# POL-L2-DS12-SIM-238-COVER-FDE-L01 · 238 政策重点可视化 · 需规分句闭合 FDE

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

- **A–C**：产品读法 / ARCH·DATA 复用 `score_value` / 说明书 ####238 / 轻会签（见 `sdd/简报/2026-11-12-SIM-238-COVER-FDE-{A,B,C}-*.md`）
- **D**：样例 `18363390` 四组重点行灌分 88/82/75/80；FE `focusScoreBars` + `focusScoreOption` 读分画柱，禁 `namedScorePoints(detail_text)`；空态「暂无得分」
- **E**：合规用例 238 补导图+柱形态与样例分

## 测试结果

- `python scripts/seed_gapfill_policy_sim_result.py` → check ok
- `python scripts/patch_gapfill_policy_sim_focus_238_scores.py --apply` → after 四组分非空
- `node src/views/policy/simulation/simulationLive.test.mjs` → 绿
- `pnpm type-check`（lumen-ui-science-pc）→ 绿
- gateway jobs 无 token → 401（预期鉴权）；数据面已 UPDATE

## 遗留风险

- FE 改动待人工确认推送后才进 CI/K8s；推送前 live UI 柱图仍可能空（旧包）
- FE-POL-03A 既有 `exportHtmlDoc` 断言失败，与本单无关

## CI/CD

- 编排 / algo：本 handoff 同批 commit → `origin/dev`
- FE：`lumen-ui-science-pc` 本地 commit，**未 push**（fe-manual-confirm-push）
- pipeline / rollout：FE 推送后由 CI 触发

## 涉及文件

- `agent-delivery/工程过程/.../合规演示用例/POL-L2-DS12-SIM-合规演示用例.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/简报/2026-11-12-SIM-238-COVER-FDE-{A,B,C,D,E}-*.md`
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_sim_result.sql`
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_sim_result.py`
- `repos/lumen-algo-py/scripts/patch_gapfill_policy_sim_focus_238_scores.py`
- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/simulation.py`
- `repos/lumen-ui-science-pc/src/views/policy/simulation/{simulationLive.mjs,simulationLive.test.mjs,interpret/InterpretWorkbench.vue}`
