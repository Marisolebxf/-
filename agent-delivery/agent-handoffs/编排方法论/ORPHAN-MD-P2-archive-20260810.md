# ORPHAN-MD-P2 — C+E36 归档 handoff

> 日期：2026-08-10  
> 执行：`agent:coordinator`  
> 分支：`cursor/orphan-md-p0-p1-3405`  
> 用户确认：执行 P2：C+E36，排除 README/定义 DEC/p2a

## 1. 范围

| 桶 | 数量 | 落点 |
|---|---|---|
| C process-notes | 10 | `agent-delivery/_archive/2026-08/process-notes/` |
| C drafts-and-scratch | 4 | `.../drafts-and-scratch/` |
| E zero-ref-handoffs | 34（原 36 去掉 2 份 p2a） | `.../zero-ref-handoffs/` |
| **合计** | **48** | `git mv`，保留历史 |

### 排除（未动）

- 各目录 `README.md`
- 产品定义包内 `DEC-*` / `FUNC-DESIGN-*` / `INDEX-*` 等
- `产品整体定义/p2a-session/**`（含 `PLAN.md` / `OPEN_QUESTIONS.md`）
- `docs/superpowers/specs/2026-07-29-ent-v2-*`（仍被 sprint 引用）
- `SYNTH-REGION` 废止包（本次未纳入确认范围）

## 2. 索引

总说明：`agent-delivery/_archive/2026-08/README.md`

镜像规则：归档路径 = `_archive/2026-08/<bucket>/` + 原路径去掉 `agent-delivery/` 前缀（`docs/` 原样挂在 bucket 下）。

## 3. registry 注意

本次**未改** `task-registry.yaml`（无 task-registry MCP）。  
已知可能仍被 registry 简写点到的归档文件：

- `ENT-JAVA-ANALYSIS-ASSET-STREAM-FIX.md` → 现位于 `_archive/2026-08/zero-ref-handoffs/agent-handoffs/企业战略分析-ENT/`

后续用 MCP `task-update-fields` 把相关 `evidence`/`handoff` 改到 archive 路径，或标 superseded。

## 4. 架构合规

仅文档搬迁；D8/D9/D10/调用链 N/A。handoff 公约路径：活跃稿仍在 `agent-delivery/agent-handoffs/`，过程稿进 `_archive/`。

## 5. cost

| 字段 | 值 |
|---|---|
| actual_tokens | n/a（未挂 registry task） |
| model_used | cursor-grok-4.5-high-fast |
| actual_cost | n/a |
| cost_warn | false |

ponytail: off（coordinator 文档收口）
