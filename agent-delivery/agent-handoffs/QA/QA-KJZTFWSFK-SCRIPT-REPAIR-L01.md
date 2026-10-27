# QA-KJZTFWSFK-SCRIPT-REPAIR-L01 · 算法库脚本修订（中途）

> **状态**：进行中，本次只落盘已改文件  
> **执行**：agent:qa-agent  
> **监管**：human:黄敬洲  
> **日期**：2026-10-27

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:黄敬洲` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改已命中的脚本和对应用例行 |

## 范围

算法库 `SDWJSF/KJZTFWSFK` 脚本修订还没做完。这次提交的是换电脑前工作区里已经改好的部分。

已落盘的改动：

- `target` 写成未加引号的 `#/...` 时补上双引号，路径不改。
- `set` 里测试步骤没有的入参（主要是多写的 `chainId`）删掉，并删掉只为它写的产业链标签断言。
- 用例册里同一行的「测试内容」去掉步骤里没有的 `chainId`。
- 政策基础指标 kind 选项改成联调台下拉的中文标签。

续跑只读这两份父控，不要另写提示词：

- `agent-delivery/qa/as-built/prompts/algo-lib-script-repair-parent.md`
- `agent-delivery/qa/as-built/prompts/algo-lib-expect-timeout-recheck-parent.md`

## 未完成

两类都还要继续扫。队列和结论账本在 `as-built/runs/`，不入库。本单保持 `in_progress`，不要改成 `ready_to_sign`。
