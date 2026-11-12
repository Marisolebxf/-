# POL-L2-DS10-CMP-213-ANALYSIS-FDE · 213-3 变化统计分析说明（LLM→gapfill→读面）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:fullstack-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |

## 修改内容

- 废止 COVER-FDE「213 非独立分析列」；回写 ARCH/API/DATA/说明书：配对级 `analysis_text`。
- 新表 `gkxlumenx_gapfill.gapfill_policy_version_analysis`；seed 预灌合规样本 `18363390` / `2022-04-06`↔`2022-06-15`。
- Python：`polan/version_analysis.py` + `POST /internal/policy/version-analysis/enrich`；synth 写 diff 后挂 enrich；panorama 按钮同写分析行。
- Java element：`version-diff` 同次透传顶层 `analysis_text`；display 原样转发。
- FE live：`VersionCompareModal` 补齐「变化统计与分析」块（Tag + 分析文 / 空态）。
- 合规用例 213 行补形态期望与冻结文案。
- 线上库已建表并插入可演分析行（本机 pymysql → `10.50.11.76`）。

## 测试结果

- `python scripts/seed_gapfill_policy_cmp.py --check` → ok（含 analysis 1 行）
- `python -m polan.version_analysis_selfcheck` → ok
- `node --experimental-strip-types src/views/policy/panorama/FE-POL-CMP-LIVE.test.mjs` → 全绿
- `pnpm type-check`（lumen-ui-science-pc）→ exit 0
- 线上：`SELECT` 确认 `18363390` 分析行存在

## 遗留风险

- Java / algo / FE 需 push → CI → K8s rollout 后，§6.5 冒烟才验通读面透传；前端仓待人工确认推送。
- 分析表未部署旧 element 时，`version-diff` catch 后 `analysis_text=null`，Tag 仍可用。

## CI/CD

- 分支：各仓 `dev`（待 commit/push）
- pipeline / rollout：本会话未等 CI
- 前端：停在本地，待确认推送

## 涉及文件

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-CMP-{ARCH,API,DATA}.md`
- `agent-delivery/.../合规演示用例/POL-L2-DS10-CMP-合规演示用例.md`
- `lumen-algo-py`：`polan/version_analysis.py`、`policy_routes.py`、`synth.py`、`panorama.py`、`seed_gapfill_policy_cmp.py`
- `lumen-svc-platform`：`PolicyGapfillController.java`、`PolicyPanoramaService.java`
- `lumen-ui-science-pc`：`VersionCompareModal.vue`、`compareLive.ts`、`FE-POL-CMP-LIVE.test.mjs`
