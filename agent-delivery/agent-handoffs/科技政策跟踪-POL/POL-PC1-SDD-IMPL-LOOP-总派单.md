# POL-PC1 · 智能政策库构建 · 段总派单（厚包）

总控：`POL-PC1-SDD-IMPL-LOOP-长任务总控.md`。监管 `human:淮政玮`。`claim_type=coordinator_dispatch`。强度：定义叶 ponytail off；实现叶 ponytail full。

必读：总控全文（含 §1.2 政策选择）、说明书 PC-1、`sdd/调用链与边界.md`、`sdd/契约输入清单.md` 治理三行、四份 `POL-L2-PC1-*-ARCH.md`、SRS `政策数据治理.md`。

`/goal` 头（各叶替换角色与 task-id）：

```text
/goal {agent}
身份：按 registry agent。只做本叶 DoD。
强度：ponytail off（定义）或 full（实现）
监管人：human:淮政玮
总控：agent-handoffs/科技政策跟踪-POL/POL-PC1-SDD-IMPL-LOOP-长任务总控.md
仓：见本叶 registry.repo。定义叶不改 lumen/demo 业务代码。实现叶 push origin/dev；前端本管线完工即推。
```

共同禁令：浏览器不打 `/topic/v1/policy`；不重开 GDF；不新造 `metric_id`；不改 D4 为 live；604/605 只写 `gkxlumenx_gapfill`；token / 口令不进 git；政策选择候选不硬编码。

## S0 会签代签

四份 ARCH 已落盘且 ≥ integration。授权人代签四角色收口：在 `sdd/l2/会签/` 落四角色各一页（可薄），note 写「授权人代签 · 总控会签 A」，状态 → `ready_to_sign` → `done`（`actor=human:淮政玮`）。不挡 S1 起草。

## S1 二级三单（每叶并行 API∥METRIC∥DATA）

| 叶 | ARCH | API | METRIC | DATA |
|---|---|---|---|---|
| 602 CLEAN | 已有 | `POL-L2-PC1-CLEAN-API` | `…-METRIC` | `…-DATA` |
| 603 STRUCT | 已有 | `…-STRUCT-API` | … | … |
| 604 LINEAGE | 已有 | `…-LINEAGE-API` | … | … |
| 605 INDLIB | 已有 | `…-INDLIB-API` | … | … |

DoD 要点：路径/同步/501 或读 gapfill；`policyId` 可选过滤（总控 §1.2）；只汇入 `BE-POL-CONTRACT-01`；指标只挂说明书已有 id 或明确不挂；DATA 写清读哪些表 / gapfill DDL 边界。

## S2 实现（会签收口后）

| 能力 | 建议叶（可复用已有 backlog） | 仓 |
|---|---|---|
| results 门面（602/603 + policyId 明细） | 新建或并入既有 display policy 门面叶 | lumen-svc-platform |
| lineage-index + indicator-library 门面 | 同上 | lumen-svc-platform |
| gapfill 建表灌数 | `POL-L2-PC1-LINEAGE-GAPFILL-L01` / `…-INDLIB-GAPFILL-L01` | 编排+执行环境 |
| FE 政策选择 + 接线 | 在 `FE-POL-04A` 后续或本管线 FE 叶 | lumen-ui-science-pc；完工即推 |

## S3 / S4 用例与 LOOP

开发负责人补四份合规演示用例可演行（须含选定政策）。覆盖无空行后自动建 `POL-L2-PC1-{CLEAN|STRUCT|LINEAGE|INDLIB}-DEMO-ACCEPT-LOOP`，按总控 LOOP 收口跑。

## S5 段 E

总控 §4 金路径。只认 K8s 已发布前端。
