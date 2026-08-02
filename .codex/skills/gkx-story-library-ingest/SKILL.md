---
name: gkx-story-library-ingest
description: Use after Gate-1 PDR (PDR-G1 / PDR-G1-RECLOSE) completes for a module — extract USM user stories into user-story-library.yaml and propose story-driven implementation leaves into story-impl-proposals.yaml without merging task-registry.
---

# GKX 门1 → 用户故事入库 + 实现拆单提案

门 1 PDR **完整闭合**（或 Track-L **通过**）后执行。不伪造会签；不自动 merge `task-registry`；不把实现 leaf 标 `ready`。

## 触发条件

满足任一即可开工：

1. Registry 任务 `*-PDR-G1` 或 `*-PDR-G1-RECLOSE` 已 `done`
2. 存在 `PM-PDR-{模块}-评审纪要.md`，结论含 Track-MS「完整闭合」或 Track-L「通过」
3. 人类明确要求对某模块跑「故事入库 / 故事拆单提案」

未闭合 → **停止**，只报告缺什么。

## 标准顺序

1. 确认模块标识（USM 目录名，如 `E1-企业查询`；或 slug `SEARCH`）
2. 读 `agent-delivery/story-impl-templates.yaml#module_map`，确认映射
3. 跑流水线（推荐）：

```bash
node scripts/pdr-gate1-story-pipeline.mjs --module {MODULE}
# 仅预览：
node scripts/pdr-gate1-story-pipeline.mjs --module {MODULE} --dry-run
```

分步等价：

```bash
node scripts/extract-user-stories.mjs --module {MODULE} --write
node scripts/suggest-story-impl-tasks.mjs write --module {MODULE}
```

4. 检查输出：
   - `agent-delivery/user-story-library.yaml` — 该模块故事 `status` 至少为 `defined`
   - `agent-delivery/story-impl-proposals.yaml` — `story_impl_leaf` / `story_theme_plan`
5. （推荐）投影飞书待审建单：

```bash
node scripts/suggest-story-impl-tasks.mjs project-feishu --status proposed
```

6. 写短 handoff（可选）：`agent-handoffs/.../STORY-INGEST-{模块}.md`
7. **向用户报备**：飞书「建单已采纳」才会 merge registry（backlog）；**禁止**本 skill 直接标 `ready`

## 飞书档 C（与缺口建单共用）

| 派单门控 | 动作 |
|----------|------|
| 待审建单 | 故事 leaf 草案已投影 |
| 建单已采纳 | `gap_proposal_accept` → 监测缺 `*-DG-G3` 则自动创建给淮政玮（ready+待确认）→ merge + backlog |
| 建单已驳回 | `gap_proposal_reject` → 提案 rejected |
| 已确认 | 既有 leaf 解锁 ready（门3 后，非本 skill） |

本地等价：`merge --ids … --approved-by human:郭万迎`（同样会 auto-ensure DG）。

## 调度智能体（coordinator）衔接

门1 入库完成后，coordinator 应：

1. `node scripts/suggest-story-impl-tasks.mjs scan --module {MODULE}`
2. 按 Theme（每包 ≤ `theme_size`，默认 3）整理 Sprint 草案话术
3. 将可粘贴 leaf 交给 PM（`yaml` 子命令）；入库后仍为 `backlog`
4. 门 3 `DG-G3` done 后走既有 `impl-gate3-unlock` + confirm → `ready`

## 禁止

- 自动 merge / push `task-registry.yaml`
- 门1 后把实现 leaf 标 `ready` 或派开发开工
- 从 Demo / 常识发明故事角色或正文（真源仍是 USM）
- 跳过「无正文」WARN 不报给人

## 相关真源

| 文件 | 用途 |
|------|------|
| `scripts/extract-user-stories.mjs` | USM → 故事库 |
| `scripts/suggest-story-impl-tasks.mjs` | 故事 → 拆单提案 |
| `scripts/pdr-gate1-story-pipeline.mjs` | 一门双做 |
| `agent-delivery/story-impl-templates.yaml` | 模块映射 + leaf 模板 |
| `agent-delivery/dispatch-rules.yaml#post_done_hooks` | PDR done 后钩子说明 |
| `产品定义评审规程.md` §5.3 | 门1 后续：故事入库 |
| `产品实现规程.md` §2.3 | 门1 草案 vs 门3 开工 |
| `task-creation-guide.md` §16 | 建单边界 |
