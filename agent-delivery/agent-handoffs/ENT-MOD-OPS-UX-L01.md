# handoff：ENT-MOD-OPS-UX-L01（重跑）

- **时间**：2026-07-24
- **角色**：`[agent:ux-agent]` · 监管 `human:淮政玮`
- **状态**：`review`（待体验 Owner 高颖抽检后由 coordinator 转 done）
- **说明**：本轮按用户指令重跑；**未改** `task-registry.yaml`；仅改 UX-SPEC + 本 handoff

## 范围与实现

对照 `企业维护管理-能力全清单.md` §F，将 UX-SPEC 从「三分区」升版为**全量 15 项左侧分组导航**交互契约：

| 分组 | 项数 | tab 覆盖 |
| --- | --- | --- |
| 内容运营 | 5 | `portal` / `entity` / `entity_dynamics` / `expert_knowledge` / `visualization` |
| 图谱运营 | 4 | `lifecycle` / `relation_lifecycle` / `entity_attrs` / `graph_draw` |
| 分析配置 | 6 | `fields_metrics` / `model_rules` / `data_batch` / `report_templates` / `perm_mask` / `audit` |

交付要点：

- 纠正 0.1「禁止应用 OPS 六分区」表述 → C1–C6 **必须可导航占位**
- 可演示项（portal / entity / entity_dynamics / lifecycle）：主路径、空态、禁止行为（ODS 不覆盖）
- 占位项 11 个：可导航、招标锚点、`本轮骨架/占位` Tag、不可从菜单消失
- 相对旧版三分区 UX-SPEC 差异表 D1–D12
- D10 §19 走查勾选（13 项）

**未做**：原型/业务代码；Wireframe/USM/TRACE；task-registry；git commit；替甲方关闭 🟡 项。

## 偏离说明

- **有意范围纠正（非偏离招标）**：相对本任务首跑 handoff「禁六分区」，按全清单 0.2 与监管指令改为全量 15 项；分析配置以占位交互契约交付，不等于完整配置台。
- **相对 Wireframe 0.1**：Wireframe 仍可能写三分区壳；本 SPEC 以全清单 §F 为导航真源，差异表已标明；不覆盖改写 Wireframe（PACK 并行）。

## 产物清单

1. `agent-handoffs/产品整体定义/ENT-OPS-维护管理/UX-SPEC-ENT-OPS.md`（**v0.2**）
2. `agent-handoffs/ENT-MOD-OPS-UX-L01.md`（本文件）

## 验收证据

- 15 项 tab id 与全清单一致，覆盖核对表 §15 = **15/15**
- 可演示 4 项含主路径/空态/禁止（含 ODS 不覆盖）
- 占位 11 项含通用契约 §2 + 分述 §7
- 差异表 D1–D12；§19 勾选见 UX-SPEC §11
- 边界：未改 demo 代码、未改 registry、未 commit

## D10 §19 勾选摘要

| 结果 | 项 |
| --- | --- |
| ✅ | 组件归类、状态完整性、键盘可达、筛选一致、联动可解释、权限明确、异常可恢复、空态可行动、抽屉宽度、遮罩策略、无障碍、Arco 一致性 |
| N/A / ✅ | 导出可信：可演示路径本轮无导出；`report_templates` 占位已写边界 |

## 架构合规自检（公约 §2 摘要）

| # | 项 | 结果 |
| --- | --- | --- |
| 1–3 | 算法/调用链/图谱 | ✅ 设计文档无越层实现 |
| 5 | CI/CD | ✅ skip_design_only |
| 6 | demo 不 merge lumen | ✅ 未改 demo |
| 9–11 | Design / D9 / D10 | ✅ 无壳层 KPI；§19 已勾选；交互对齐 D10 |

## cost（四字段）

| 字段 | 值 |
| --- | --- |
| `actual_tokens` | 55000 |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | 0.36 |
| `cost_warn` | green |

> 口径：估算 in+out（含重跑精读全清单/IA/旧 SPEC/D10）；价表按同类任务惯例回填，待 coordinator 验收时可按 console 精校。

## 残留风险

1. **PACK 文档不同步**：IA/Wireframe 0.1 仍含「三分区 / 禁六分区」语句；HIFI 若只读 Wireframe 会回退——需 PACK 对齐全清单 §F，或 HIFI 明确以 UX-SPEC 0.2 + 全清单为准。
2. **A3 从主体拆出**：旧主体锚点「动态与区域」与独立 `entity_dynamics` 并存期可能双入口文案不一致；实现须按 SPEC 主体瘦身 + 链出。
3. **占位与可演示感知**：评审时需强调 C1–C6 / A4–A5 / B2–B4 为骨架，避免被误认为完整配置台已交付。
4. **开放项 🟡**：Q-OPS-02 写侧归属、Q041/Q048/Q049 明星深圳字段仍待甲方确认；UI 保留 ⚠。

## 下一步

1. 高颖抽检 UX-SPEC v0.2 → coordinator 转 `done`
2. PACK 修订 IA/Wireframe 导航表述（若尚未完成）
3. `ENT-MOD-OPS-V1-HIFI` 按差异表 D1–D12 落地左导航 15 项
4. 开放项仍由 PM 推进客户决策清单（不在本任务关闭）
