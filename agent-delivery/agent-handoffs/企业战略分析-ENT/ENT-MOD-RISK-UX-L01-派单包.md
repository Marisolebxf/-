# 派单包：ENT-MOD-RISK-UX-L01

- **派单方**：coordinator（补生成 · webhook confirm 未落盘 git）
- **时间**：2026-07-21
- **执行 Agent**：`ux-agent`
- **监管人**：human:高颖
- **Sprint**：2026-W30 stretch
- **上游**：`ENT-MOD-RISK-PACK-L01` ✅ done（五步线框预览已确认，作 V1 首轮输入）
- **confirm**：`dispatch_confirmed_by=human:唐绍祖` · trigger=`def-pack-unlock-mo-ux`

## 1. 目标

产出风险洞察 **UX 交互深化规格**，闭合 `GAP-RISK-V1` 中的 UX 真源缺口，覆盖两种分析模式：

- **供应链关系分析**（图谱 / 节点 / 断链风险 / 报告）
- **企业发展痛难点识别**（四维诊断 / 差距 / 报告）

以及与企业评估一致的：对象带入、任务配置、分析执行、结果查看、报告输出、历史与个人资产中心。

## 2. 输入真源

| 文件 | 用途 |
|------|------|
| `E-28_E-29-风险洞察/IA-ENT-RISK.md` | 信息架构 |
| `USM-ENT-RISK.md` | 用户故事 US-ENT-RISK-* |
| `Wireframe-ENT-RISK.md` | 线框帧 F-RISK-* |
| `TRACE-ENT-RISK.yaml` | 故事 / metric / Q017·Q018 / 架构约束 |
| `UX-UE 通用交互组件规范.md` §19 | 走查清单 |
| `Design.md` | 视觉 token（本任务不改视觉体系） |

## 3. 交付物

**主产出**（推荐路径）：

- `agent-handoffs/产品整体定义/E-28_E-29-风险洞察/UX-SPEC-ENT-RISK.md`

**须含**：

| 章节 | 内容 |
|------|------|
| 主路径 | 对象带入 → 模式选择（供应链 / 痛难点）→ 配置 → 执行 → 结果 → 报告 |
| 异常路径 | 无对象、超限、无数据、错误、无权限、低可信、口径待确认 |
| Q017/Q018 | 字段旁 ⚠️ PendingBadge；交互降级说明（不伪闭合） |
| 跨模块 | 对比篮 handoff（供应链关系 / 发展痛难点）；与评估共享交互对齐 DEC-RISK-SHARED-INTERACTION |
| 图谱 | Nebula 只读展示约束；禁止前端算官方风险/中心性 |
| Arco 边界 | Drawer / Modal / 空态 / 加载（D10） |
| 字段表 | Wireframe 列与 TRACE metric 对齐；统计列带 `metric_id` |

## 4. Definition of Done

1. UX 规格与 IA / USM / Wireframe / TRACE **故事 US-ENT-RISK-*** 一致
2. 两种模式主路径 + 关键异常态均有交互说明
3. Q017/Q018 / GAP-RISK-* 均有 ⚠️ 占位与降级路径（🟡 可）
4. handoff：`ENT-MOD-RISK-UX-L01.md`
5. 高颖 review ✅
6. **不**改 demo 代码（属 `ENT-MOD-RISK-V1-HIFI`）

## 5. 下游

| 任务 | 关系 |
|------|------|
| `ENT-MOD-RISK-V1-HIFI` | **直接消费** 本任务 UX 规格作首轮会签输入 |
| `ENT-MOD-RISK-METRIC-OPEN-L01` | 并行；字段 ⓘ 文案可后挂 catalog |
| `ENT-MOD-RISK-PDR-G1` | 依赖 V1-HIFI + PACK；本任务支撑 UX 闭合证据 |

## 6. 认领话术

```text
/goal ENT-MOD-RISK-UX-L01
监管：human:高颖
交付 UX-SPEC-ENT-RISK.md；对齐供应链/痛难点双模式、共享交互与 Q017/Q018 降级
先读：IA/USM/Wireframe/TRACE-ENT-RISK、UX-UE 通用交互组件规范 §19
```
