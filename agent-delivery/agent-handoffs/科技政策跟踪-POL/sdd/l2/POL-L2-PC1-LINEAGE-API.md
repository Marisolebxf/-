# POL-L2-PC1-LINEAGE-API · 溯源索引构建 · 后台接口设计

- 任务：`POL-L2-PC1-LINEAGE-API` · 2026-11-08 · `agent:api-agent` · 监管：`human:淮政玮`
- 上游：LINEAGE-ARCH；总控 §1.2 · SRS：**604**
- 偏离：契约清单/`指标与501` 仍写 501；本分册按 ARCH 迁移读 `gapfill_policy_lineage_index`，HTTP 成功空态，不 501 充当功能。不回头改那些文件。

## 1. 公开资源

`GET /display/v1/policy/governance/lineage-index` — 同步。不进异步。不返回 501（无行则空列表）。

| 参数语义 | 必选 | 作用 |
|---|---|---|
| 政策 id（`policyId`） | 否；**核增演示默认一条可演** | 按政策拣索引行 |
| 条款号 | 否 | 按条款拣关联 |
| 结论键 | 否 | 按结论拣原文/条款依据 |

## 2. 内部委托

display → element 只读 `gkxlumenx_gapfill.gapfill_policy_lineage_index`。不直连 Python；不读研报 617 表；不写 nGQL。

## 3. 明确不做

不写字段表；不新造 metric；接口不直接返回 mock 行（行须在表内）。
