---
name: ponytail-help
description: >
  Show GKX ponytail command/mode cheat sheet. Trigger: /ponytail-help,
  "ponytail help", "ponytail 怎么用". One-shot; do not change mode or write code.
---

# Ponytail-help（GKX）

Display this card. Do **not** change mode, write files, or code.

Full doc: `agent-delivery/ponytail-usage.md`

## Cursor（本团队主战场）

斜杠 `/ponytail` **无插件档**；规则默认 **full**。对话话术：

| 意图 | 怎么说 |
|------|--------|
| 标准 | `按 ponytail full` |
| 轻度 | `按 ponytail lite` |
| 极限 | `按 ponytail ultra`（慎用） |
| 关闭 | `本次关闭 ponytail` / `normal mode` |
| 审查 | `ponytail-review`（只出删除清单） |
| 帮助 | `ponytail-help`（本卡） |

Skills：`.cursor/skills/ponytail` · `ponytail-review` · `ponytail-help`

## 档位

- **full**（默认）：懒阶梯强制，最短有效 diff  
- **lite**：照做 + 一行更懒替代  
- **ultra**：先质疑范围，优先删  
- **off**：不压代码量；铁律仍在  

## GKX 护栏

不得用 YAGNI 跳过：调用链 / Nebula / 可观测 / D8·D9·D10 / handoff / demo→lumen 对齐。

适用：coding agent。不适用：PM / product / coordinator / architect / doc / ux（完整性优先）。
