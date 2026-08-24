# 派单包 · TOPIC-ALGO-GAP-L02

> **状态**：ready · **Agent**：`algorithm-agent` · **supervised_by**：`human:淮政玮`  
> **仓**：`gkx-orchestration` · **claim_type**：`pull`  
> **说明**：[`给人说明-A2-GAP-L02-2026-08-24.md`](./给人说明-A2-GAP-L02-2026-08-24.md)  
> **effort_points**：5 · **difficulty**：M  
> **下游**：本叶交齐后把 `DS-ALGO-GAP-L02` 从 backlog 升 ready。L01 冻结，不签成 A1 对照。

## 目标

用已 `done` 的 A1 表1/表2，回填专题差集 mapped 行的 A1 ID；missing 仅在 97 叶仍未覆盖时维持。新四人套文件名带 `L02`，不覆盖 L01。

## `/goal`

```text
/goal
task: TOPIC-ALGO-GAP-L02
agent: algorithm-agent
supervised_by: human:淮政玮
claim_type: pull
强度：ponytail off（定义·差集回填；禁止用 YAGNI 跳过对照清单与 handoff）。禁止用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律。
上下文：headroom 可选。A1 表2 / L01 yaml / schema 读原文，禁止 compress 代替精读。

先读 给人说明-A2-GAP-L02-2026-08-24.md。MCP 认领后再改文件。
对照 ALGO-LIB-METRIC-DEPS-L01 表1/表2 回填专题 mapped 的 A1 ID。
missing 旧=7，只在库确有覆盖时才改 mapped。禁止编造 M_*。禁止覆盖 L01 四人套。禁止回滚 OPEN 指针。
产物：metrics/request/专题系统/TOPIC-ALGO-GAP-L02.* + handoff。不要开工展示叶。
```
