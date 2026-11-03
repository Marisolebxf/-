# POL-DISPLAY 详设段 · 总派单

总控：`POL-DISPLAY-长任务总控.md`。监管 `human:淮政玮`。执行 `agent:arch-agent`。强度：ponytail off（定义任务，不缩文档）。

本段已确认。调研父单 `POL-DISPLAY-SURVEY-L01` 的 handoff 落盘后直接认领三叶，不再问。三叶可同时写。每叶只写自己的两个文件。父单 `POL-DISPLAY-SDD-L01` 等三叶 handoff 齐后合成说明书，三叶自己不写说明书正文。

必读（三叶通用）：

- `agent-delivery/agent-handoffs/产品整体定义/科技信息展示系统-完整详细设计/05-功能-科技政策跟踪.md`
- `agent-delivery/ARCH-DISPLAY-01.md`
- 调研定稿 `agent-delivery/工程过程/04-系统集成/05-展示系统集成/对照-科技政策跟踪-存量任务与依赖.md`
- 四册 `agent-delivery/agent-handoffs/科技政策跟踪-POL/survey/`

`/goal` 头（三叶通用，替换叶名与路径）：

```text
/goal arch-agent
身份：架构师。只写本叶文档。
强度：ponytail off
监管人：human:淮政玮
总控：agent-handoffs/科技政策跟踪-POL/POL-DISPLAY-长任务总控.md
仓：gkx-orchestration。不 commit，不 push，不改注册表，不改 WBS，不改 lumen/demo。
```

共同禁令：不写 OpenAPI 字段表、DTO、枚举。不把 `E-E7-POLICY-M1-L06` 写成展示实现路径。同一算法可以复用，URL 不复用 `/topic/v1/policy`。不新建 `FE-POL-*`，不重开政策 GDF 包。指标和任务只引用调研定稿里已出现的编号；调研写「未见」的，详设也写「未见」。

## 调用链与边界

任务 `POL-DISPLAY-SDD-CHAIN-L01`。产物 `sdd/调用链与边界.md`。

写清：前端 → `gkxlumen-display` 的 `/display/v1/policy/**` → Python `/internal/*`。哪些区块同步读 ADS，哪些走 Job。书面裁定 L06 不是展示实现路径。写清与专题政策、门户政策扶持、第 6 项 GDF、第 7 项读图的边界，这些范围不新开实现任务。

## 指标与 501

任务 `POL-DISPLAY-SDD-METRIC-L01`。产物 `sdd/指标与501.md`。

按页（全景、评价、推演、治理、拆解、对比、研报）列出展示区块、`metric_id`、`algorithm_type`、D4、判定。判定只沿用调研三档。可接统计读面且 D4=mock 的，写明真路径接上前数值仍是 mock。MODEL 和未注册的推演、解析、研报写 501 与空态。推演与布局推荐继续分键。

## 契约输入清单

任务 `POL-DISPLAY-SDD-INPUT-L01`。产物 `sdd/契约输入清单.md`。

这是交给 `BE-POL-CONTRACT-01` 的输入，不是契约本身。只列：资源路径、同步或 Job、成功时读什么、501 时页面空态、明确不做的字段表。不展开请求体和响应体。
