# ENT-PY-RECOMMEND-TASK

> 2026-08-21 按规范补回：原关单在 `ENT-PY-ANALYSIS-完工.md`，AV 扫不到本 ID。只拆引育适配叶；联调证据未闭合。未改 `ENT-MOD-RECRUIT-*` 产品定义。

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
| 说明 | 4 端点 + 权重校验；不管候选池 CRUD |

## 范围与实现

`POST /internal/gkx-ai/recommend/**` 四端点（body 传参）：

| 路径 | 作用 |
|------|------|
| `/tasks` | 创建；`sub_type`=`attraction`\|`cultivation`；`selection_mode`=`filter`\|`candidate_workbench` |
| `/tasks/status` | 不返回 pending |
| `/tasks/result` | 招引/培育两套结果 |
| `/tasks/cancel` | 透传算法 |

`filter` 传筛选快照；`candidate_workbench` 传 `enterprise_codes[]`。权重合计必须 100。Java `task_id`/`callback_url` 原样下传。无 `/tasks/history`。

现仓：`demo-svc-topic-py` 与 `lumen-topic-py` 的 `gkx_ai_service/views/recommend.py`。

## 产物清单

| 文件 | 作用 |
|------|------|
| `gkx_ai_service/views/recommend.py` | 4 端点 + 权重 |
| `gkx_ai_service/science_client.py` | 推荐异步客户端 |
| `tests/test_analysis_tasks.py` | 关单含推荐 create→status |
| 派单包 | `ENT-PY-RECOMMEND-TASK-派单包.md` |
| 合并关单 | `ENT-PY-ANALYSIS-完工.md` |

## 偏离说明

| 项 | 说明 |
|----|------|
| 招引/培育不拆两套 URL | 与 ARCH v3：同一 `talent_recommend` + `sub_type` |
| 候选池 CRUD | 不在 Python（对比篮模块） |
| science 真实任务 | 关单待联调 |
| 注释 `tasks/{id}` | 过时；路由为 `/tasks/status` |

## 验收证据

关单 2026-07-28：`tests/test_analysis_tasks.py` 20 passed（含推荐 create→status）。D-30：camelCase 入参拒绝。

**无 2026-08 Java 门面 + 算法真实任务联调记录。**

## 架构合规自检

| # | 铁律 | 合规 | 说明 |
|---|------|------|------|
| 1 | 算法只在 Python | ✅ | 适配转发，不算分 |
| 2 | `/internal/*` | ✅ | `/internal/gkx-ai/recommend/*` |
| 3 | Nebula | ✅ | 不直连图 |
| 4 | 可观测 | ✅ | |
| 5 | CI/CD | ✅ | 关单待补 pipeline |
| 6 | demo≠lumen merge | ✅ | |
| 7 | Java 不写算法 | ✅ | |
| 8 | Mock 先行 | ✅ | |
| 9 | D8 | ✅ | 无 UI |
| 10 | D9 | ✅ | 不伪 live 推荐分 |
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

依赖 CALLBACK + 算法框；权重与 selectionMode 需 Java 契约对齐后才能做联调探针。
