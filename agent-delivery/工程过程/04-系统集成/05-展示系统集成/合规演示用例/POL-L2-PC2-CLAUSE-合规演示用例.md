# POL-L2-PC2-CLAUSE · 条款精细化拆解 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 智能政策拆解
- 需规序号：607
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2 PC-2
- 日期：2026-11-13（PARSE-4JOB-FDE 卡2=A；原稿同步 GET 口径废止）
- 调度核对：见文末

拆解页一点拆解走 async `policy_parse_clause`（worker 内复用 enrich）。治理 603 仍可直调同步 `parse/clauses`，本叶不测治理页。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 607 条款精细化拆解 | 智能政策拆解 · 条款 Tab | 政策 18363390 | 点「拆解」并行四 Job；本叶盯 `policy_parse_clause` | POST /display/v1/policy/evaluation/jobs | {"sub_type":"policy_parse_clause","params":{"policy_id":"18363390"},"force":true} | 须见条款树（章节/条目）或诚实空态；写回 `structured_elements.clauses`。不因本叶失败清空语义 Tab | 可演（部署后） |

## 一条主路径

1. 选定 18363390，点「拆解」。
2. 条款 Tab 出现树或空态说明；不直调 `parse/clauses`（拆解页路径）。

## 调度核对

需规 607 一行可演。
