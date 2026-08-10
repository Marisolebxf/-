# QA 企业分析三链路 E2E（2026-08-10）— 问题分流

> 角色：`[agent:qa-agent]`  
> 样本：`EVAL/RISK/REC-20260810-002/003`  
> 主流程：**创建 / 节点进度回调 / 终态回调均已闭环**（CFG `callback_attempts`≈事件×1）  
> **本期验收范围（2026-08-10 收口）**：只验 **功能是否通畅**、**结构是否完整**；**评分效果暂不测**。

## 分流结论

| 问题 | 是否本期范围 | 归属 | 动作 |
|------|--------------|------|------|
| 创建→进度→终态回调闭环 | ✅ 功能通畅 | — | 已通过 |
| 结果指针 / `/asset` 可读 / JSON 顶层字段 | ✅ 结构完整 | — | `/asset` 已通；引育 `taskId=""` 见下 |
| 引育 `/asset` 中 `taskId=""` | ✅ 结构完整 | Python + 算法 | **Python 已改**；算法工单 `ENT-ALGO-REC-TASKID-BACKFILL-FIX` |
| 供应链 1 节点 0 边 | ❌ 现网 Mock/关系数据不全 | — | **不建单**；已从 registry 删除 | 
| 评估三维全 50.0 / 低可信 | ❌ 评分效果 | — | **不建单**；已从 registry 删除 |
| SSE 与 status 鉴权不一致 | ❌ 本期不管 | — | **不建单**；已从 registry 删除 |
| `/result` 无业务体易踩坑 | ❌ 本期不管 | — | **不建单**；已从 registry 删除 |
| `/asset` 空 `{}` | ✅ 结构/下载 | Java（旧单） | `ENT-JAVA-ANALYSIS-ASSET-STREAM-FIX` — **复测已不复现** |

## Python 已改（data-agent 范围）

- 仓：`demo-svc-topic-py`
- 文件：`gkx_ai_worker/consumer.py`（`_backfill_result_task_id` + `upload_result` 写 MinIO 前补空 `task_id`）
- 测试：`tests/test_result_delivery.py` 增补回填用例
- 说明：算法注释写明「由调用方回填」；Worker 是 Java 可见 JSON 的最后一跳，必须落真实 taskId。算法源头工单仍保留，避免只靠防御。

## 新建 / 调整工单

**ready（本期相关，仍保留）**
1. `ENT-ALGO-REC-TASKID-BACKFILL-FIX` → algorithm-agent / `lumen-algo-py`

**已从 registry 删除（不应建单 / 本期不管）**
- ~~`ENT-ALGO-EVAL-COMPETITIVENESS-FLAT-SCORE`~~（评分效果）
- ~~`ENT-ALGO-RISK-SUPPLY-CHAIN-EMPTY-GRAPH`~~（Mock/关系数据不全）
- ~~`ENT-JAVA-ANALYSIS-SSE-AUTH-ALIGN`~~（SSE 鉴权，非主流程）
- ~~`ENT-JAVA-ANALYSIS-RESULT-CONTRACT-CLARIFY`~~（`/result` 契约，非主流程）

## 未单独立单

- 节点进度「跳号」：CFG attempts 满次数，属节点切换过快 + 仅 latest 状态；非回调失败。若产品要逐步条，另开增强单即可。
