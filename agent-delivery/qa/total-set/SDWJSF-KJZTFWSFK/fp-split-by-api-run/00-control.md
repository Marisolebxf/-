# 功能点拆分循环 · 控制面（by-api v0.2）

- **方法**：`by-api` v0.2（字段级；对外唯一交付合表）
- **任务（拟）**：`QA-KJZTFWALGO-FP-BY-API-L01`（MCP 待补建）
- **工作单元**：六级（一条六级 = 一个子 agent）
- **原则**：`../科技专题服务算法库-功能点拆分原则-by-api.md`（**0.2.1**；L01 金样若仍为旧表头须按 3.1 重写）
- **旧稿**：`../fp-split-by-api-run-v0-202609/` 只读，禁止回填
- **接口快照**：`_catalog-snapshot.md`
- **挂接**：`_l6-to-catalog-map.yaml`（4A / 双金样）
- **孤儿**：`catalog-orphan-registry.yaml`（5b，不交付）
- **编排真源**：[`fp-split-by-api-playbook.md`](../fp-split-by-api-playbook.md) · 总索引 [`qa/algo-lib-playbook-index.md`](../../../algo-lib-playbook-index.md)
- **队列**：`01-task-list.md`（60 六级 × 子 agent）

## 当前

| 项 | 值 |
|---|---|
| 阶段 | **复核中（不进 F4）** · L13/L05–L14 已改写；**自动门禁已绿**（`memo/audit-parent-run-20261017.md`） |
| 金样闸门 | L01 已签收；**L13 须按 `comp.graph` 重新人签收**（旧 30-endpoint 作废） |
| F3 进度 | **60/60** done |
| 合表 | 未开始；目标 `…功能点拆分-by-api_v1.xlsx` + GKX 扩展列（12a） |
| 校验 | **父控 2026-10-17**：`scripts/audit_l6_catalog_binding.py` → **0 blocking**；人检 L13 + 文档 drift 见 audit memo |

## 停机条件

- L01、L13 未过人确认，不派全量 58
- 写不出不同验收就不拆；契约不全先补 catalog（8a）
- 不得覆盖 `…功能点拆分_v1.xlsx` / `_v2.xlsx`；不得改 `fp-split-run/work/`

## 循环步骤

1. 读原则 0.2、本文件、`_l6-to-catalog-map.yaml`
2. 按闸门派 `prompts/Lxx.md` → `work/Lxx.md` + `review/Lxx.md`
3. 登记 5b 孤儿到 `catalog-orphan-registry.yaml`
4. 60/60 + 校验绿 → 合表
