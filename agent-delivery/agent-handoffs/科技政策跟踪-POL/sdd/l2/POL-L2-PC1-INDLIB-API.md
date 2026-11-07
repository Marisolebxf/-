# POL-L2-PC1-INDLIB-API · 规划指标库搭建 · 后台接口设计

- 任务：`POL-L2-PC1-INDLIB-API` · 2026-11-08 · `agent:api-agent` · 监管：`human:淮政玮`
- 上游：INDLIB-ARCH；总控 §1.2 · SRS：**605**
- 偏离：契约清单仍写 501；本分册按 ARCH 读 `gapfill_policy_indicator_lib`，成功空态。

## 1. 公开资源

`GET /display/v1/policy/governance/indicator-library` — 同步。不 501。

| 参数语义 | 必选 | 作用 |
|---|---|---|
| 维度 | 否 | 扶持力度/适用范围/实施时效/申请条件 四闭集 |
| 政策 id（`policyId`） | 否；**演示默认一条可演**（可与 603/604 共用选中） | 拣该政策条目 |

## 2. 内部委托

display → element 只读 `gkxlumenx_gapfill.gapfill_policy_indicator_lib`。不挂注册 `M_POLICY_*` 顶条目。不进异步。

## 3. 明确不做

不写字段表；不新造 metric；接口不直接返回 mock 数组。
