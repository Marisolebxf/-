# coordinator 自动派单（运维手册 · 非全员）

> **全员可读版本**：[`自动派单与确认规约.md`](自动派单与确认规约.md)

监听 task done → 提议 unlock（pending）→ **confirm（必填 --approved-by）** → ready + 派单包  
门 3 DG-G3 done → 实现轨 **pending（impl-gate3-unlock）** → confirm → ready

## 命令

```powershell
node scripts/coordinator-dispatch.mjs list
node scripts/coordinator-dispatch.mjs confirm --all --approved-by human:郭万迎
node scripts/coordinator-dispatch.mjs scan --cause-task ENT-MOD-COMPARE-PACK-L01 --dry-run
```

## 真源

- `dispatch-rules.yaml` — 规则 + `confirm_policy`
- `pending-dispatch.yaml` — 待确认队列
- `team-roster.yaml` — confirm 审批人校验

## 停机

`dispatch-queue.yaml#coordinator_halt.active: true`
