# Archive — 仓根 `p2a-session/`（Codex 过程会话）

> 归档日：2026-08-22  
> 来源：仓根 `gkx-orchestration/p2a-session/`（2026-07-15 随 `1802a64e` 入库，时间戳停在 2026-08-05）  
> 方式：`git mv`（保留历史），非删除  
> **不是** `agent-handoffs/产品整体定义/p2a-session/`——那份仍是企业深化规格/决策日志真源，8/10 归档已排除，本次不动。

## 为什么归档而不是留在仓根

仓根 `p2a-session/` 是 Codex Plan-to-Act 会话工作区，不是产品定义包、也不是 Skill 真源。继续放在仓根会与 `产品整体定义/p2a-session/` 撞名，后续检索会把过程稿当成现行稿。

## 两摊内容与现行落点

| 归档子目录 | 原路径 | 性质 | 现行真源 | 处理 |
|---|---|---|---|---|
| `definition-to-demo/` | 仓根 4 份 PLAN/DECISIONS/FINAL_PLAN/OPEN_QUESTIONS | 拟建个人 Skill `$gkx-definition-to-demo`（任意模块定义包 → Demo 覆盖契约） | `.codex/skills/gkx-product-definition-review/` + `产品定义评审规程.md`；E-34 覆盖证据在 `agent-handoffs/交付覆盖/ENT-STAR/` | 未落地为独立 Skill；能力被后续规程/Skill 吸收。过程稿归档，不复活。 |
| `e34-star-enterprise-selector/` | 仓根嵌套会话 | E-34 明星企业 0..N 名单、选择器、URL `enterprise_code`、0/1/N 空态等已确认决策 | `agent-handoffs/产品整体定义/E-31-企业发展/E-34-明星企业介绍/`（IA/TRACE/USM/Wireframe）；Q048 仍在客户决策清单 🟡 | 决策已写入四件套。会话稿仅作纸面追溯。 |

## 仍有效的纸面指针

- `agent-handoffs/交付覆盖/ENT-STAR/source-manifest.yaml` → `decision_session` 已改为本目录 `e34-star-enterprise-selector/FINAL_PLAN.md`
- `ENT-EVAL` 的 `forbidden_sources: p2a-session` 仍表示「禁止用会话稿当评估模块真源」，语义不变

## 不要做的事

- 不要在仓根重建此目录当产品文档。
- 不要从本归档把 `$gkx-definition-to-demo` 再做成第二套规程；要改评审流程，改 `gkx-product-definition-review`。
- 不要把 `产品整体定义/p2a-session/` 一并搬进来——那份仍被 `task-registry`、TRACE、PDR 纪要引用。
