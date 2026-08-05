# POLICY-UX-L01 · 政策维度 E7 + DS-10/12 UX 交互深化

> **状态**：in_progress（文档交付完成，待会签/AV）  
> **监管人**：human:高颖  
> **执行**：agent:ux-agent  
> **日期**：2026-08-05  
> **四件套基线**：E7 v1.4.3 · DS10-12 v1.0

## 1. 范围与实现

| DoD | 产物 | 状态 |
| --- | --- | --- |
| UX-SPEC-E7-政策分析.md | `产品整体定义/E7-政策分析/UX-SPEC-E7-政策分析.md` v1.0 · `ready_for_v1` | ✅ |
| UX-SPEC-DS10-12-科技政策跟踪.md（含三屏差异） | `产品整体定义/DS10-12-科技政策跟踪/UX-SPEC-DS10-12-科技政策跟踪.md` v1.0 · `ready_for_v1` | ✅ |

对照 bid：

- 专题 E7：`§1.1.1.2.4.2.6` + 门户 P-17~22 + 维护 OPS 复用  
- 展示 DS：`§1.1.1.1.4.2` + 核增四叶子；与专题 `/policy/*` 分轨写明

## 2. 偏离说明

- Wireframe-E7 清单含 F-POL-PORTAL / F-POL-OPS，正文细则以 TRACE 门户/OPS 合同补齐进 UX-SPEC（未改产品范围）。
- DS 契约 `screen_tier` 按校验器取 `medium_1440_1920`；小屏/大屏差异写在 §8（Track-L 独立视觉）。
- TRACE 中部分 Gap 原含 `v1_hifi_round1` 且 `blocks_v1: false`；UX 契约按校验器改为不阻断 hifi 的下游阶段，V1 处理仍为 deterministic_demo_contract。

## 3. 产物清单

- `UX-SPEC-E7-政策分析.md`（12 节 + `ux_spec_contract`）
- `UX-SPEC-DS10-12-科技政策跟踪.md`（12 节 + 三屏旅程）
- 本 handoff

## 4. 验收证据

```bash
python3 ~/.codex/skills/gkx-ux-specification/scripts/validate_ux_spec.py \
  agent-delivery/agent-handoffs/产品整体定义/E7-政策分析/UX-SPEC-E7-政策分析.md
# UX_SPEC_OK

python3 ~/.codex/skills/gkx-ux-specification/scripts/validate_ux_spec.py \
  agent-delivery/agent-handoffs/产品整体定义/DS10-12-科技政策跟踪/UX-SPEC-DS10-12-科技政策跟踪.md
# UX_SPEC_OK
```

覆盖摘要：

| 包 | 故事 | Frame | 旅程 | blocks_v1 |
| --- | --- | --- | --- | --- |
| E7 | 9 | 9 | 4 | 无 |
| DS10-12 | 11 | 10 | 5 | 无 |

## 5. 架构合规自检

| # | 铁律 | 结论 |
| --- | --- | --- |
| 1 | 算法只在 Python | ✅ 规格禁止前端直连算法 |
| 2 | 前端→Java→Python | ✅ 图谱/仿真经 API |
| 3 | Nebula 非 Neo4j | ✅ 展示禁止浏览器直连 |
| 4 | 可观测 | ⚪ 定义阶段不适用页面埋点落地 |
| 5 | CI/CD | ⚪ 文档任务 |
| 6 | demo2 不 merge lumen | ✅ 未改业务仓 |
| 7 | 共享聚合核心 | ✅ E7 复用篮/任务/报告壳 |
| 8 | ADS/Mock | ✅ Mock/Pending 挂载 |
| 9 | Design.md / Arco | ✅ 中屏；大屏 Track-L 分轨 |
| 10 | D9 血缘 | ✅ metric_id 投影；无矩阵不伪填 D1–D4 |
| 11 | D10 交互规范 | ✅ 键盘/焦点/ARIA/状态 |

## 6. Demo 激活说明

- 两份 UX-SPEC 均为 `ready_for_v1`，**允许**进入 V1 高保真首轮设计/Demo 编排（`gkx-definition-to-demo`）。
- E7 依赖共享对比篮政策 Tab 可操作态（GAP-E7-05 实现对齐）。
- 本 handoff **不**自动改 registry 为 integration；需监管人确认后由 coordinator 推进。

## 7. Cost 回填（估算）

| 字段 | 值 |
| --- | --- |
| actual_tokens | 95000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 2.8 |
| cost_warn | green |
