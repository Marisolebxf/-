# as-built/tools

辅助 node 脚本，以及业务仓 e2e spec **指针**。Playwright 可读的 yaml 过程在上一级 `scripts/{系统}/{模块}/{功能}/`。

金样阶段用 Playwright MCP + yaml，不在此放 spec。

稳定后可把 `lumen-ui-topic/e2e/` 中对应测试记在下表，并回填用例「自动化用例ID」。

| spec | 覆盖 | 说明 |
|------|------|------|
| e2e/chain-gold.spec.ts | 产业链金路径 | 段 E；环境默认 30892，与本线 50892 不同 |
| `check-run-consistency.py` | run 四方一致性机检（X5） | `python3 check-run-consistency.py <run-dir> [<scripts-dir>]`；run 落盘后必跑 |
| `survey-page.mjs` | **无头实勘探针**（可并行） | `node survey-page.mjs --path '/…' --out ../scripts/…/fixtures/scout`；可选 `--click '对比篮'`；产出 scout.json/md + page.png。禁止当 runner，不写 `runs/` |
| `gap-func-vs-scripts.py` | FUNC↔脚本缺口；`--write` 附带 health+**queue** | `python3 gap-func-vs-scripts.py --system KJZTFWXT --write` → `gap`/`health`/`queue`；编排 `../script-backfill-playbook.md` |
| `health-cases.py` | 半成品 / index 漂移（gap 盲区） | 单独 `--write` 或由 gap `--write` 自动调用 |
| `run-scripts.mjs` | cases-v1 机跑 | `node run-scripts.mjs <功能目录> [--run-dir …] [--only id1,id2]`；默认平铺 `runs/{日}-50892-{功能}-…`。**同波次**应 `--run-dir runs/{日}-50892-{wave}/{功能名}`（见 `schema.md` §4.2），禁止多功能共用一个 run-dir（P0-01 撞名） |
| `aggregate-wave-results.py` | 波次 → Excel | `python3 aggregate-wave-results.py --wave ../runs/{wave} --write` → `results.xlsx`；编排见 `../script-batch-run-playbook.md` |
