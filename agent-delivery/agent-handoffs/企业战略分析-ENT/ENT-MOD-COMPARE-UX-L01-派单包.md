# 派单包：ENT-MOD-COMPARE-UX-L01

- **派单方**：coordinator
- **时间**：2026-07-21
- **执行 Agent**：`ux-agent`
- **监管人**：human:高颖
- **Sprint**：2026-W30 stretch
- **上游**：`ENT-MOD-COMPARE-PACK-L01` ✅ done（2026-07-21 四件套 alignment 闭合）

## 1. 目标

产出对比篮 **UX 交互规格**，闭合 `ENT-MOD-COMPARE-V1-HIFI`（review）的 UX 真源缺口，覆盖：

- 单用户单篮（50 家）、全局去重加入态
- **稳定纵向工作区**：筛选顶固定、列表内滚、操作栏底固定（DIFF-08）
- **发起分析** →「选择分析任务」浮层（3+2 分组，选后不跳转，确认后 handoff）
- **return_context_id** 往返恢复 vs 新进入仅恢复篮内容
- 空篮 **不做推荐**；招引/培育候选即时动作
- GAP-IMPL-01~03 交互降级与 ⚠️ 占位（口径未定不阻塞线框）

## 2. 输入真源

| 文件 | 用途 |
|------|------|
| `ENT-COMPARE/IA-*.md`、`USM-*.md`、`Wireframe-*.md` | PACK 四件套 |
| `TRACE-ENT-COMPARE.yaml` | `interaction_contract` / `analysis_types` / `dispatch_state` |
| `repos/demo-ui-topic/docs/ia/enterprise/ENT-compare-basket-product-design.md` | 早期 PM 草案（须与 PACK 差异表对齐） |
| `PM-PDR-ENT-COMPARE-评审纪要.md` | Decision 088、Δ-C2 长卡片批量上限 |
| `交付覆盖/ENT-COMPARE/evidence/*.png` | Demo 已验证交互证据 |
| `UX-UE 通用交互组件规范.md` §19 | 走查清单 |

## 3. 交付物

**主产出**（二选一 + handoff 声明真源）：

- `agent-handoffs/产品整体定义/ENT-COMPARE/UX-SPEC-ENT-COMPARE.md`（**推荐**），或
- 升版 `ENT-compare-basket-product-design.md` 并标注与 IA 导航位置差异（PACK 已将对比篮置于重点企业分析之后）

**须含**：

| 章节 | 内容 |
|------|------|
| 主路径 | 加入 → 篮内筛选（名称+类型）→ 勾选 → 发起分析 → 目标模块 |
| 异常路径 | 超 50 批量溢出、权限不足、对象失效交集、return_context 失效 |
| 空篮 | 进企业查询；**禁止**推荐列表（DIFF-04） |
| 文案统一 | 筛选恢复用「重置」；取消勾选「取消选择」；清空篮需确认 |
| 跨模块 | `CompareBasketHandoffBar` / 返回对比篮 / `analysis_type` 路由表 |
| Arco 边界 | 浮层、固定底栏、列表虚拟滚动（D10） |
| 字段表 | Wireframe 列与 TRACE `card_visible_fields` 一致；统计列 **metric_id=N/A** 注明 |

## 4. Definition of Done

1. UX 规格与 IA / Wireframe / TRACE **故事 US-ENT-CMP-01~05** 一致
2. `interaction_contract` 全量映射（含 `analysis_entry` 与 `candidate_actions`）
3. GAP-IMPL-01~03 均有交互处理说明（🟡 可 PendingBadge 占位）
4. handoff：`ENT-MOD-COMPARE-UX-L01.md`
5. 高颖 review ✅
6. **不**改 demo 代码（V1-HIFI 已在 review；代码对齐属 V2）

## 5. 下游

| 任务 | 关系 |
|------|------|
| `ENT-MOD-COMPARE-V1-HIFI` | **直接依赖** 本任务（补 UX 真源后可闭合 review） |
| `ENT-MOD-COMPARE-METRIC-OPEN-L01` | 并行，不阻塞 |

## 6. 认领话术

```text
/goal ENT-MOD-COMPARE-UX-L01
监管：human:高颖
交付 UX-SPEC-ENT-COMPARE.md；对齐 Decision 088、3+2 分析任务浮层与 return_context 往返
```
