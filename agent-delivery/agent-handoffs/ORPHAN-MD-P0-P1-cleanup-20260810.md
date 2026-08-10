# ORPHAN-MD-P0-P1 — 孤立/误放 Markdown 清理 handoff

> 任务：仓根冗余 MD P0+P1 清理（coordinator 调度执行）  
> 日期：2026-08-10  
> 执行：`agent:coordinator`  
> 分支：`cursor/orphan-md-p0-p1-3405`  
> 监管：用户确认「执行 P0+P1」

## 1. 范围与实现

### P0（删除/跳转）

| 动作 | 路径 | 说明 |
|---|---|---|
| 删除 | `agent-handoffs/TOPIC-SVCCHAIN-ALIGN-L01.md` | 与 `agent-delivery/agent-handoffs/` 下同文件字节级重复 |
| 删除 | `agent-handoffs/TOPIC-SVCCHAIN-ALIGN-L02.md` | 同上 |
| 改为跳转页 | `team-onboarding.md`（仓根） | 真源保持 `agent-delivery/team-onboarding.md` |

### P1（迁入公约路径）

| 动作 | 原路径 | 新路径 |
|---|---|---|
| 迁移 | `agent-handoffs/FE-DISPLAY-KG-SERVICE-ALIGN-L01.md` + evidence | `agent-delivery/agent-handoffs/` + `evidence/` |
| 迁移 | `agent-handoffs/FE-DISPLAY-SVC-ECO-ALIGN-L01.md` + evidence | 同上 |
| 迁移 | `agent-handoffs/CHAIN-INST-DATA-ANALYSIS-L01.md` | `agent-delivery/agent-handoffs/产业链分析-CHAIN/` |

同步更新：`docs/符合度评估-科技知识图谱-服务展示.md`、`docs/符合度评估-科技服务全景-科技创新生态服务.md`、两份 FE-DISPLAY handoff 内证据路径、CHAIN-INST handoff 自指路径。

## 2. 未改

- **未改** `task-registry.yaml`（公约要求走 MCP；当前环境无 task-registry MCP）。registry 既有 `agent-handoffs/...` 简写与迁入后的 `agent-delivery/agent-handoffs/...` 约定一致。
- **未做** P2 归档（过程备忘 / SYNTH-REGION / superpowers scratch）。
- 数据设计稿 `agent-delivery/data/data-design/产业链/CHAIN-INST-DATA-ANALYSIS-L01.md` 保留（与 handoff 不同内容）。

## 3. 验收证据

- 仓根 `agent-handoffs/` 目录已清空移除
- TOPIC 真源仍在 `agent-delivery/agent-handoffs/TOPIC-SVCCHAIN-ALIGN-L0{1,2}.md`
- FE-DISPLAY evidence PNG 7 张位于 `agent-delivery/agent-handoffs/evidence/`
- 仓根 `team-onboarding.md` 为跳转页

## 4. 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1–5 算法/调用链/图谱/可观测/CI | N/A（仅文档路径） |
| 6 demo2 merge | N/A |
| 7 共享聚合 | N/A |
| 8 数据策略 | N/A |
| 9 D8 Design | N/A |
| 10 D9 血缘 | N/A |
| 11 D10 交互 | N/A |
| handoff 路径公约 | ✅ 收口到 `agent-delivery/agent-handoffs/` |

## 5. cost（本 chore）

| 字段 | 值 |
|---|---|
| actual_tokens | n/a（coordinator 清理会话，未挂 registry task） |
| model_used | cursor-grok-4.5-high-fast |
| actual_cost | n/a |
| cost_warn | false |

ponytail: off（coordinator 文档收口，不以缩代码为目标）
