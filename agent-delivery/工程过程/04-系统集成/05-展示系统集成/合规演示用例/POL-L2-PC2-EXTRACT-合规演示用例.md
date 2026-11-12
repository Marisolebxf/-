# POL-L2-PC2-EXTRACT · 关键指标自动提取 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 智能政策拆解
- 需规序号：608
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2 PC-2
- 日期：2026-11-13（PARSE-4JOB-FDE 卡3=A 写 structured_elements）
- 调度核对：见文末

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 608 关键指标自动提取 | 智能政策拆解 · 指标 Tab + 页头力度指数 | 政策 18363390 | 点「拆解」；本叶盯 `policy_parse_metric` | POST /display/v1/policy/evaluation/jobs | {"sub_type":"policy_parse_metric","params":{"policy_id":"18363390"},"force":true} | 指标 Tab 见量化项列表或诚实空态；页头「力度指数」有数或「—」。写回 `structured_elements.metrics` + `intensity`。不新表 | 可演（部署后） |

## 一条主路径

1. 选定 18363390，点「拆解」。
2. 指标 Tab / 力度指数随本 Job 成功亮起；失败保持「—」，不造假分。

## 调度核对

需规 608 一行可演。
