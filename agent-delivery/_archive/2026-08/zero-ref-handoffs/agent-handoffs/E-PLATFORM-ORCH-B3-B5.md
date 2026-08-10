# Handoff · E-PLATFORM-ORCH B3 / B4 / B5

**日期**：2026-07-28  
**作者**：`[agent:architect]`  
**范围**：编排成熟度 B 线 — Convoy 自动检测、coordinator 自治循环（轻量）、Refinery 评估脚手架

## 1. 实现对照

| 项 | 原编号 | 交付 | 自动化边界 |
|----|--------|------|------------|
| B3 | 原 B6 | `touched_files` + `detect-convoy-conflicts.mjs` + `convoy-lib.mjs` | 硬冲突门禁；软警告（`agent-delivery` 豁免） |
| B4 | 原 B4 | `coordinator-loop.mjs` Path A light | lease→ready→convoy→空位→scan；**不**接 Cursor SDK、不 auto-confirm |
| B5 | 原 B7 | `refinery-merge-queue.md` + `refinery-queue.yaml` + `refinery-enqueue.mjs` | `enabled: false`；仅 soft-record，不 git push |

## 2. 产物清单

- `scripts/lib/convoy-lib.mjs`
- `scripts/detect-convoy-conflicts.mjs`
- `scripts/coordinator-loop.mjs`
- `scripts/refinery-enqueue.mjs`
- `agent-delivery/refinery-merge-queue.md` / `refinery-queue.yaml`
- `task-registry.yaml#graph_engineering_policy`（`convoy_auto` / `coordinator_loop` / `refinery`）
- 手册 §14.3 / §14.4 / §16.5–16.6；`coordinator.mdc`；`templates/task-leaf-template.yaml`；`scripts/README.md`

## 3. 验收证据（本地冒烟 2026-07-28）

```text
node scripts/detect-convoy-conflicts.mjs     → hard=0（soft 主要为代码仓缺 touched_files）
node scripts/coordinator-loop.mjs --skip-scan --limit 3 → 输出派单建议包
node scripts/refinery-enqueue.mjs --list     → enabled=false, queues={}
```

## 4. 偏离 / 决策

- **B4 不接 Cursor SDK**：无人监管烧 token 风险；符合公约「决策不外包」→ Path A light。
- **B5 不启用自动合并**：先靠 B3 减冲突；启用门槛见 `refinery-merge-queue.md` §5（需 PM+架构师双签）。
- 同批 `task-registry` 含过期 lease 清理（若干 claimed→ready / HIFI→done），与 B3–B5 工具同仓变更。

## 5. 架构合规自检（§2）

1–10：本批仅编排资产与 Node 脚本，不改业务调用链 / 图谱 / 前端栈 → ✅ 不适用或未违反。

## 6. 下一步

1. 人审后 `git commit`（本 handoff 写入时可能尚未 commit）
2. 新 leaf 填 `touched_files`；站会用 `coordinator-loop.mjs`
3. ORCH-L02/L03 状态升格由 PM/coordinator 按 DoD 另办
4. Refinery 真启用前双签
