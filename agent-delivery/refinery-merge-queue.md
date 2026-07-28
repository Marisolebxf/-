# Refinery 合并队列（B5 评估与脚手架 · 2026-07-28）

> **状态**：评估 + 策略脚手架，**未**接入 git hook / 强制串行 push  
> **关联**：Gastown Refinery · `orchestration-maturity-and-roadmap.md` Phase 3/远期 · 公约 §4.2 lumen `dev` 直推  
> **决策**：本项目长期默认 **主工作区 + push `origin/dev`**；Refinery 仅在同仓多 agent 高频 push reject 时启用

---

## 1. 问题

多 agent 同时 `git push origin/dev` → 互相 reject → `pull --rebase` 竞态。  
Gastown **Refinery** = 按仓串行化合并/推送队列。

## 2. 与本项目策略的关系

| 策略 | 说明 |
|------|------|
| 默认 | 无 Refinery；push reject → `pull --rebase` 再推（公约 §4.3） |
| Convoy（B3） | **源头减冲突**（同文件集串行），优先于合并队列 |
| Refinery | **汇聚层**兜底；仅当 Convoy 无法覆盖（跨 leaf 无 touched_files / 热文件）时启用 |

**结论（2026-07-28）**：先落地 B3 Convoy 自动检测；Refinery 保持可选。不自研完整合并机器人，不强制改 git hook。

## 3. 若启用时的最小模型

```text
agent 完成 → enqueue(repo, task_id, branch|HEAD) → Refinery worker 串行：
  fetch → rebase origin/dev → push → mark released → 通知下一笔
```

字段见 `refinery-queue.yaml`。

## 4. MVP 命令（脚手架）

```powershell
# 入队（记录意图，不执行 git）
node scripts/refinery-enqueue.mjs --repo lumen-svc-platform --task ENT-X --dry-run
node scripts/refinery-enqueue.mjs --repo lumen-svc-platform --task ENT-X

# 查看队列
node scripts/refinery-enqueue.mjs --list
```

**不做**：自动 rebase/push、改远程保护规则、替代 GitLab MR。

## 5. 启用门槛（全部满足才升格实现）

1. 同一 `lumen-*` 仓一周内 push reject ≥ 5 次且可归因多 agent  
2. B3 Convoy 已强制（新 leaf 必填 `touched_files`）仍无法压冲突  
3. PM + 架构师双签（涉及推送纪律变更）

## 6. 与 ORCH-L03 关系

ORCH-L03（coordinator 循环）选型：**Path A light** = `coordinator-loop.mjs`（不接 Cursor SDK）。  
Refinery 不阻塞 ORCH-L03；属推送层正交能力。
