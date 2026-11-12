# POL-L2-DS10-TREND-KEYFIELD · 长任务总控

> **日期**：2026-11-12  
> **授权人**：`human:淮政玮`（本管线 `supervised_by`）  
> **授权句**：后续认领不必再问。  
> **目标**：序号 205「影响评估」「深度分析报告」补强为弹窗进度条 + 结果展示 + situation/report 真 PDF/Word 导出。  
> **模式**：长任务 FDE。规约：`agent-delivery/长任务执行规约.md` + `产品实现规程.md` §4.2  
> **锁**：`lock_hours=24`。`claim_type=coordinator_dispatch`。  
> **强度**：ponytail full

聊天确认的计划 `205重点领域FDE` 即本授权。

## 1. 已拍板

| 项 | 结论 |
|---|---|
| 范围 | 仅 205 影响评估 + 深度分析报告交互与导出；不改热点主路径、stats 趋势/地域 |
| 档位 | **中档** |
| 进度 | 弹窗分阶段进度条；底层仍同步读 gapfill（不进 Python、不建真算 Job） |
| 导出 | 两入口完成后均可 PDF/Word；对齐 217：`situation/report` → OpenHTMLtoPDF |
| 仓 | 编排说明书/四单/用例 + `lumen-ui-science-pc` |
| 分支 | `origin/dev`；前端 push 仍待当次「推」 |
| 签收 | `ready_to_sign→done` 只由 `human:淮政玮` |

## 2. DAG

| 波次 | 叶 | 产物 |
|---|---|---|
| 总单 | `POL-L2-DS10-TREND-KEYFIELD-FDE-L01` | 本总控 + 各波次 handoff/简报 |
| A | product | 界面必见 / 状态 / 影响清单；说明书 205 |
| B | arch | TREND-ARCH/API 中档回写 |
| C | 会签 | 四单对抗闭合简报 |
| D | frontend（+必要时 api 无改） | `KeyFieldAnalysisPanel` |
| E | qa | TREND 用例形态 + §6.5；段 E 冒烟 |

## 3. 纪律

- 界面禁止 gapfill / Job / 算法黑话。
- 禁止 `trackingExport` 打印另存冒充 PDF。
- 不新造 `metric_id`；D4 仍 mock。
- 长任务循环内 coordinator 可调动 qa（不等黄敬洲）。
