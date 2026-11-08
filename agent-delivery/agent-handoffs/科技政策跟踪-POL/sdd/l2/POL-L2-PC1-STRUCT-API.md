# POL-L2-PC1-STRUCT-API · 政策库结构化 · 后台接口设计

- 任务：`POL-L2-PC1-STRUCT-API` · 日期：2026-11-08 · 监管：`human:淮政玮` · `agent:api-agent`
- 上游：`POL-L2-PC1-STRUCT-ARCH.md`；总控 §1.2 · SRS：**603**
- 强度：ponytail off。汇入 `BE-POL-CONTRACT-01`，不写实现代码。

## 1. 公开资源

与 602 共用：`GET /display/v1/policy/governance/results`（同步，不 501）。本分册只定**结构化区块** + **单政策结构化摘要**（核增演示主点）。

| 参数语义 | 必选 | 作用 |
|---|---|---|
| 标签筛选 | 否 | 结构化概览按 `auto_tags` 拣 |
| 政策 id（`policyId`） | 否；**演示默认一条可演** | 总控 §1.2。返回该政策结构化摘要；不改标签体系树/字段映射总表的全库读法 |

## 2. 内部委托

`gkxlumen-display` → `gkxlumen-element` 只读 `gkxlumenx_ads.policy_text_parse`、`policy_industry_rel`、`gkxlumenx_dwd.policy_base_info` / `script_state`（批次时间）。不进异步，不打 `/topic/v1/policy`。

区块：

1. **库级**：结构化政策数、覆盖率（有条款政策数÷主表数）、标签分布、最新结构化批次。  
2. **单政策摘要**（有 `policyId`）：是否已有条款行、`auto_tags`、关键标准字段取值概要、更新时间。**不是**拆解页条款树（607/608）。无行则摘要空。

## 3. 明确不做

不拆第三条资源；不写字段表；不新造 metric；不允许接口直接返回 mock 覆盖率。
