# 603-STRUCT-FDE · 波次 D · frontend-agent

总单：`POL-L2-PC1-STRUCT-FDE-L01`。会签已闭合（1A/2A/3A）。  
你是 frontend-agent。仓：`lumen-ui-science-pc`。强度：ponytail full。

## 真源（只读）

- 说明书「#### 603」+ 线框 `603-STRUCT-FDE-线框.md`（`vFDE-603-2026-11-10`）
- 异议闭合 `603-STRUCT-FDE-C-异议闭合.md`
- 读法 `603-STRUCT-FDE-B-读法方案.md`（定档中）
- 中台对照（勿改）：`demo-ui-system-test` ClausePage「抽取条款」→ `structurePolicyClauses`

## 必改

1. 条件栏标签「演示政策」→「政策选择」；下拉可关键字检索（`allow-search` 已有则核验可用）
2. **同一行**按钮「结构化抽取」
3. 门控：`hasClauses`/已结构化才加载下方业务摘要；未结构化不加载，引导先抽
4. 按钮：未选禁用；未结构化可点；已结构化**仍可点（2A）**；进行中禁用不可第二遍；失败保留上次成功摘要 + 提示
5. 调用：`POST /display/v1/policy/parse/clauses`（body `policy_id`），成功后再拉 `governance/results?policyId=`；禁直连 Python、禁打开中台
6. 两表：`fetchGovernanceLive` 合并 `policyPcSeed.structureTaxonomy` / `fieldMappings`，不得空；Wave0 须 Mock/评审可辨识（角标或文案）
7. **603-qry-1 本波不验收**：页内快速检索不作为本单 DoD，可不改或保持 empty

## 不做

- 不改 Java/Python/Storage；不改 `demo-*`；不 push 除非监管人当次说「推」
- 前端仓默认人工确认后推（`fe-manual-confirm-push`）

## 自检

`pnpm type-check`（或仓规约等价）绿；改动摘要写清。完工后停本地，等用户确认再 push。

## 回复（8 行内）

改了哪些文件；抽取 API 路径；两表如何灌 seed；自检结果；是否已 commit（可本地 commit，勿 push）。
