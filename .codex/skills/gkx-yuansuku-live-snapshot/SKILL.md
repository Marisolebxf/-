---
name: gkx-yuansuku-live-snapshot
description: >-
  Runs the full 20-要素库 Excel vs live MySQL gkx row-count and schema-diff
  snapshot (gen_schema_diff_report.py), writes a dated summary against the
  last in-repo report, and updates 加工/README.md. Use when the user says
  执行一次快照, 跑行数报告, 要素库对照, gen_schema_diff_report, or
  数据源表及行数报告. Not for enterprise Wave A 40-table probes
  (LIVE-DWD-ENTERPRISE) or TOPIC-METRIC coverage.
---

# 全要素库 live 快照

真源与 Cursor 同文：`.cursor/skills/gkx-yuansuku-live-snapshot/SKILL.md`。改技能先改那边。

执行脚本与 Excel 在 `agent-delivery/data/third-party-source/gkx-mysql-raw/加工/`。日常：`python gen_schema_diff_report.py`。环比只用仓内上一份行数报告；未点名不 commit。
