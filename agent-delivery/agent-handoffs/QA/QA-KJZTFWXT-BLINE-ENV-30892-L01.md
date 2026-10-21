# QA-KJZTFWXT-BLINE-ENV-30892-L01 · 专题 B 线测试环境改到 30892

> **状态**：已提交  
> **执行**：agent:qa-agent  
> **监管**：human:黄敬洲  
> **日期**：2026-10-21

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:黄敬洲` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 环境地址替换，不改业务代码 |

## 范围与实现

专题 B 线现行测试环境改为 `http://10.50.69.111:30892/`（无 `/tts/svcz` 前缀）。

已改：用例编制说明（`case-rework-playbook.md`、`_case.md`）、脚本编制说明（`script-backfill-playbook.md`、`script-batch-run-playbook.md`、`_script.md`）、规约与总索引（`func-test-playbook-index.md`、`catalog/KJZTFWXT.yaml`、`catalog/index.yaml` 专题行、`qa/README.md`、`as-built/README.md`、`perf-baseline.md`）、提示词（`_result.md`、`_submit.md`、企业查询/重点类型 `gold.md`）、39 本用例册环境行、脚本 `fixtures` 的 `base_url` 与脚本里的完整旧地址、`run-scripts.mjs` 默认地址。

未改：`retro/` 里标明记录当时的旧地址；`runs/` 历史证据（已按原跑次还原，不入库）；算法库 `edu.itic-sci.com/dma/algovwz/`；脚本 `as_built_note` 里对当时 edu 现场的观察句。

## 偏离

`QA-KJZTFWXT-BLINE-SCRIPT-REWRITE-L01` 的 DoD 仍写试跑环境 `http://10.50.69.111:30888/`。现行指针以本单为准。

## 遗留

无。历史 `runs/` 目录名未改。
