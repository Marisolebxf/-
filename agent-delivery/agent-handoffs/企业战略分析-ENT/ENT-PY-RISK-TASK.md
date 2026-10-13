# ENT-PY-RISK-TASK

> 2026-08-21 按规范补回：原关单在 `ENT-PY-ANALYSIS-完工.md`，AV 扫不到本 ID。只拆风险适配叶；联调证据未闭合。产品定义文档只读，未改 `ENT-MOD-RISK-*`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:徐滕强` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 2026-07-24 认领；2026-07-28 随分析编排层关单 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 4 端点适配；不写算法、不建 Python 任务史 |

## 范围与实现

`POST /internal/gkx-ai/risk/**` 四端点（body 传 `task_id`，无路径参数）：

| 路径 | 作用 |
|------|------|
| `/tasks` | 创建；`sub_type`=`supply_chain` \| `pain_points` |
| `/tasks/status` | 状态；不返回 pending，映射 running |
| `/tasks/result` | 结果；供应链允许最多 3 级图谱快照，大结果可 `resultUrl` |
| `/tasks/cancel` | 取消透传算法 |

约束：Java `task_id` / `callback_url` 原样下传；Python 不自造 taskId；无 `/tasks/history`；不直连前端。

现仓路由仍在 `demo-svc-topic-py` 与 `lumen-topic-py` 的 `gkx_ai_service/views/risk.py`（`@router.post("/tasks")` 等四条）。

## 产物清单

| 文件 | 作用 |
|------|------|
| `gkx_ai_service/views/risk.py` | 4 端点 |
| `gkx_ai_service/science_client.py` | 风险异步任务客户端（Mock+占位） |
| `tests/test_analysis_tasks.py` | 关单含风险 create→status |
| 派单包 | `ENT-PY-RISK-TASK-派单包.md` |
| 合并关单 | `ENT-PY-ANALYSIS-完工.md` |

## 偏离说明

| 项 | 说明 |
|----|------|
| 与 CALLBACK/EVAL/RECOMMEND 共仓关单 | 本次拆文件，不改代码 |
| science `/gdf/tasks/create-and-start` | 关单待联调 |
| 无正式任务历史 | 符合 DoD：真源在 Java |
| 模块注释仍写 `tasks/{id}/status` | 过时；实际路由为 `/tasks/status` + body |

## 验收证据

关单 2026-07-28：`tests/test_analysis_tasks.py` 20 passed（评估/风险/推荐共享）。风险路径：create→status。`py_compile` 通过。

**无 science 真实任务 + Java 门面 2026-08 联调记录。**

## 架构合规自检

| # | 铁律 | 合规 | 说明 |
|---|------|------|------|
| 1 | 算法只在 Python | ✅ | 本叶 HTTP 调算法/Mock，不在 Java 算 |
| 2 | `/internal/*` | ✅ | `/internal/gkx-ai/risk/*` |
| 3 | Nebula | ✅ | 图谱快照由算法回传，本叶不直连 nGQL |
| 4 | 可观测 | ✅ | 公共 observability |
| 5 | CI/CD | ✅ | 关单待补 pipeline |
| 6 | demo≠lumen merge | ✅ | |
| 7 | Java 不写算法 | ✅ | |
| 8 | Mock 先行 | ✅ | |
| 9 | D8 | ✅ | 无 UI |
| 10 | D9 | ✅ | 不伪造风险指标 live |
| 11 | D10 | ✅ | 无 UI |
| 12 | D12 | ✅ | 不以 demo 冒充 lumen 联调 |

## Cost 回填

四叶合并关单共用：

| 字段 | 值 |
|------|-----|
| actual_tokens | 350000 |
| model_used | zs-glm-5.2 |
| actual_cost | 8 |
| cost_warn | green |

## 遗留风险

依赖 CALLBACK 与算法异步框；正式门面 INT 见下方 2026-08-21 节，状态保持 integration。

## 2026-08-21 正式门面 INT

`POST /topicAsync/topic/v1/analysis/tasks` `risk_insight` 可建单（须 64 位 `analysis_fp`）。`RISK-20260821-001` supply_chain、`RISK-20260821-002` pain_points 均 `failed`：`创建下游任务失败：DWD enterprise_base 未找到企业`（ES org 不在算法 DWD）。不进入下一步。

记录：`qa/test-records/KJZTFWXT/R0/INT-分析任务中心联调-记录-20260821.md`
