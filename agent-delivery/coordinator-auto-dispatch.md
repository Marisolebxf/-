# coordinator 自动派单（运维手册 · 非全员）

> **全员可读版本**：[`自动派单与确认规约.md`](自动派单与确认规约.md)

监听 task done → 提议 unlock（pending）→ **confirm（必填 --approved-by）** → ready + 派单包  
门 3 DG-G3 done → 实现轨 **pending（impl-gate3-unlock）** → confirm → ready  
**缺 leaf 建单建议** → `suggest-registry-tasks.mjs` → `registry-gap-proposals.yaml`（PM 手工入库）  
**门1 故事入库 + 故事拆单提案** → `pdr-gate1-story-pipeline.mjs` → `user-story-library.yaml` + `story-impl-proposals.yaml`（**不** auto ready）

## 命令

```powershell
node scripts/coordinator-dispatch.mjs list
node scripts/coordinator-dispatch.mjs confirm --all --approved-by human:郭万迎
node scripts/coordinator-dispatch.mjs scan --cause-task ENT-MOD-COMPARE-PACK-L01 --dry-run
node scripts/coordinator-dispatch.mjs suggest-gaps [--module ENT-MOD-RISK]
node scripts/suggest-registry-tasks.mjs scan [--module PREFIX] [--phase definition|implementation]
node scripts/suggest-registry-tasks.mjs write [--module PREFIX] [--project-feishu]
node scripts/suggest-registry-tasks.mjs accept|reject|project-feishu [--approved-by human:真名]

# 门1 后（故事 + 拆单提案 + 飞书待审建单）
node scripts/pdr-gate1-story-pipeline.mjs --module E1-企业查询
node scripts/suggest-story-impl-tasks.mjs write --all --project-feishu
node scripts/suggest-story-impl-tasks.mjs project-feishu --status proposed [--dry-run]
node scripts/suggest-story-impl-tasks.mjs merge --ids sip-ENT-MOD-KEYPANO-API-CONTRACT-L01 --approved-by human:郭万迎
# ↑ merge/Webhook「建单已采纳」时：若 depends_on 缺 *-DG-G3，自动创建给淮政玮（ready + 待确认）
```

## 真源

- `dispatch-rules.yaml` — 规则 + `confirm_policy` + `post_done_hooks`
- `pending-dispatch.yaml` — 待确认 unlock 队列
- `registry-gap-templates.yaml` — 缺口检测模板
- `registry-gap-proposals.yaml` — 建单建议队列（`task-creation-guide.md` §13）
- `story-impl-templates.yaml` / `story-impl-proposals.yaml` — 故事驱动拆单（§16；飞书「待审建单→建单已采纳」同档 C）
- `scripts/lib/ensure-dg-gate3.mjs` — 建单已采纳时自动补门3给淮政玮
- `team-roster.yaml` — confirm 审批人校验

## 停机

`dispatch-queue.yaml#coordinator_halt.active: true`
