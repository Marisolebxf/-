# POL-DISPLAY · 长任务总控（调研 → 系统详细设计）

> **日期**：2026-11-03  
> **授权人**：`human:淮政玮`（本管线 `supervised_by`）  
> **授权句**：后续认领不必再问。2026-11-03 追加：详设段编排完成后直接确认并执行，中途不再问，直到调研定稿和详设说明书都落盘。  
> **目标**：写完科技政策跟踪的存量调研定稿，再写系统详细设计说明书。不写 API-POL，不改业务仓。  
> **模式**：长任务。规约：`agent-delivery/长任务执行规约.md`  
> **锁**：`lock_hours=24`。`claim_type=coordinator_dispatch`。`claimed_by=agent:arch-agent`。

聊天里的「按此编排写总控，后续认领不必再问」即本授权。2026-11-03 追加「详设长任务编排后直接确认并执行，中途不再问，直到完成」。本文件落盘后，本管线后续叶不再逐叶问聊天。详设三叶已在本文件确认，不再另请确认。

## 1. 已拍板

| 项 | 结论 |
|---|---|
| 仓 | 只写 `gkx-orchestration`。禁止改 `lumen-*` / `demo-*` |
| 分支 | 编排仓 `origin/dev`。子智能体不 commit、不 push |
| 调用链 | 展示对外只走 `/display/v1/policy/**`。禁止把 `E-E7-POLICY-M1-L06` 写成实现路径 |
| 契约边界 | `BE-POL-CONTRACT-01` 只出 API-POL。本管线不写 OpenAPI 字段表 |
| 废作 | 不新建第二套 `FE-POL-*`。不重开政策 GDF 包。不把门户扶持十条写成展示页任务 |
| 升级人 | 结构歧义（新表、改主键）`blocked` 并升级 `human:李伟`。口径 🟡 照实记录，不停工 |
| 签收 | `ready_to_sign→done` 只由 `human:淮政玮`。签收可积压，不挡下一叶 |

本管线是文档，没有段 E，没有金路径。不派 QA。

## 2. 叶表

| 顺序 | 任务 | 状态门 | 产物 |
|---|---|---|---|
| 1 并行 | `POL-DISPLAY-SURVEY-DS10-L01` | 无前置 | `survey/DS-10.md` |
| 1 并行 | `POL-DISPLAY-SURVEY-DS11-L01` | 无前置 | `survey/DS-11.md` |
| 1 并行 | `POL-DISPLAY-SURVEY-DS12-L01` | 无前置 | `survey/DS-12.md` |
| 1 并行 | `POL-DISPLAY-SURVEY-PC-L01` | 无前置 | `survey/PC.md` |
| 2 | `POL-DISPLAY-SURVEY-L01` | 四叶都有 handoff | 定稿 `工程过程/04-系统集成/05-展示系统集成/对照-科技政策跟踪-存量任务与依赖.md` |
| 3 并行 | `POL-DISPLAY-SDD-CHAIN-L01` | 调研父单 handoff 已落盘（不等签收） | `sdd/调用链与边界.md` |
| 3 并行 | `POL-DISPLAY-SDD-METRIC-L01` | 同上 | `sdd/指标与501.md` |
| 3 并行 | `POL-DISPLAY-SDD-INPUT-L01` | 同上 | `sdd/契约输入清单.md` |
| 4 | `POL-DISPLAY-SDD-L01` | 详设三叶都有 handoff | `sdd/科技政策跟踪-系统详细设计说明书.md` |

详设三叶已建，状态 backlog。调研父单 handoff 一落盘，本会话直接认领并派写，不再问。三叶未齐时不写说明书正文。

注册表现有父单的 `depends_on` 不能改写。解锁以本表为准。调研父单 `depends_on` 仍为空。详设三叶的 `depends_on` 指向 `POL-DISPLAY-SURVEY-L01`，只表示顺序，不等该单变成 done。

## 3. 子智能体纪律

- 只写本叶产物和本叶 handoff：调研写 `survey/{叶}.md`，详设写 `sdd/{叶}.md`，handoff 写 `agent-handoffs/科技政策跟踪-POL/{task-id}.md`。
- 不改 `WBS.md`、`task-registry.yaml`、别人的分册。
- 指标走 metric-registry MCP，任务走 task-registry MCP。禁止为查询去读 seed / 矩阵 / `task-registry.yaml`。
- 判定只允许三档：可接统计读面、模型未注册则 501、跨项索引。D4 全是 mock 时，可接统计读面仍标 mock，不写成已上线。
- 找不到的任务或指标写「未见」，不编造。

厚包：调研 `POL-DISPLAY-SURVEY-总派单.md`；详设 `POL-DISPLAY-SDD-总派单.md`。
