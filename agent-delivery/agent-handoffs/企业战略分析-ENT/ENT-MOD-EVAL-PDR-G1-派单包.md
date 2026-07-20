# 派单包：ENT-MOD-EVAL-PDR-G1

- **派单方**：coordinator（human:淮政玮）
- **时间**：2026-07-20
- **执行 Agent**：`product-agent`
- **监管人**：human:高颖
- **PM 参与**：human:淮政玮（PACK-L01 已评审通过）
- **Sprint**：2026-W30（stretch）
- **Epic**：E-ENT-SCRUM-PDR
- **上游**：`ENT-MOD-EVAL-PACK-L01` ✅ done（2026-07-20 · 淮政玮）

## 1. 背景

企业评估模块（E-23 技术力 / E-24 商业力 / E-30 综合竞争力）门1产品定义包已完成四件套并经 PM 评审通过。本任务是 **Track-MS 门1 PDR 正式闭合**：产出 `PM-PDR-ENT-EVAL-评审纪要.md`，对照 PDR 检查清单逐条给结论。**metric 语义会签**：按 `产品定义评审规程.md` **§1.4.1**，**唐绍祖临时代行何老师**，签字等效。

## 2. 输入真源（必读）

| 用途 | 路径 |
|------|------|
| 四件套 | `agent-handoffs/产品整体定义/E-23_E-24_E-30-企业评估/` |
| PDR 规程 | `agent-delivery/产品定义评审规程.md` §5 |
| 参照纪要模板 | `agent-handoffs/企业战略分析-ENT/PM-PDR-ENT-COMPARE-评审纪要.md` |
| REQ 映射 | `TRACE-ENT-EVAL.yaml` |
| 指标 seed | `agent-delivery/metrics/cfg_metric-ENT-seed.yaml` |
| 客户决策表 | `agent-delivery/客户决策清单跟踪表.md` |
| PACK handoff | `agent-handoffs/企业战略分析-ENT/ENT-MOD-EVAL-PACK-L01.md` |

## 3. 范围

### 3.1 允许产出

- 新建 **`PM-PDR-ENT-EVAL-评审纪要.md`**（结构与 COMPARE 纪要一致：一页摘要、PDR 检查清单、讨论要点、开放项、门1结论）
- 必要时 **微调** 四件套中明显笔误（须 handoff 列出 diff；不大改语义）
- 更新 `TRACE-ENT-EVAL.yaml` 中 PDR 结论字段（若有规程要求）

### 3.2 禁止

- 宣告门1通过但开放项未登记 🟡
- 替甲方拍板指标口径（仍走客户决策清单）
- 跳过 metric 语义会签（须唐绍祖按 §1.4.1 会签，或何老师本人）
- 修改 demo-ui-topic / Java / 算法代码（指标对齐由 `ENT-EVAL-ALGO-METRIC-ALIGN-L01` 负责）

## 4. Definition of Done

1. **`PM-PDR-ENT-EVAL-评审纪要.md`** 存在且包含：
   - REQ-ENT-003 / 004 / 010 映射结论
   - PDR-01～PDR-14（或规程当前版）逐条 ✅ / 🟡 / ❌
   - 开放项同步至 `客户决策清单跟踪表.md`（新增或引用已有 Q 编号）
   - metric 语义卡：**唐绍祖会签（§1.4.1 临时代行）** / 或何老师本人 — 须明确标注
2. 门1结论：**通过（附 🟡）** 或 **有条件通过** — 须 PM 淮政玮 + 监管人高颖书面确认后 task → `review`
3. handoff：`agent-handoffs/企业战略分析-ENT/ENT-MOD-EVAL-PDR-G1.md`
4. registry `evidence` 指向纪要路径
5. cost 四字段回填

## 5. 架构与设计铁律（派单必读）

1. 算法只在 Python — 本任务不写 Java/算法
2. 调用链 — N/A（文档任务）
3. 图谱 NebulaGraph — N/A
4. 可观测性 — N/A
5. CI — `cicd: skip_design_only`
6. demo2 不 merge lumen — 仅 agent-delivery 文档
7. 数据血缘 — 纪要中每个统计指标须可追溯 metric_id 或 🟡 GAP
8. D8/D10 — 纪要引用 Design.md / UX 规范边界，不另起视觉栈

## 6. 认领话术（product-agent）

```
/goal ENT-MOD-EVAL-PDR-G1
监管人：human:高颖
请先读 ENT-MOD-EVAL-PDR-G1-派单包.md 与四件套，产出 PM-PDR-ENT-EVAL-评审纪要；提交 review 前请高颖 + 淮政玮确认门1结论表述。
```

## 7. 并行任务（勿混淆）

| 任务 | 负责人 | 关系 |
|------|--------|------|
| `ENT-EVAL-ALGO-METRIC-ALIGN-L01` | human:唐绍祖 | demo-ui-topic 指标/权重对齐；与 PDR 文档并行 |
| `ENT-JAVA-*` | 孔东/侯佳伟 | Java 门面；不阻塞 PDR |
