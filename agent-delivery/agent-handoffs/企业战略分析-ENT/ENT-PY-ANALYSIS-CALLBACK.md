# ENT-PY-ANALYSIS-CALLBACK

> 2026-08-21 按规范补回：原关单写在 `ENT-PY-ANALYSIS-完工.md`（四叶合并，H1 不含本 task-id），AV 扫不到。本文件只拆本叶；Java/算法联调证据未闭合。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:徐滕强` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 2026-07-24 认领；2026-07-28 data-agent 关单 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 适配层最小实现；未用 YAGNI 跳过 OTel / `/internal` 调用链 |

## 范围与实现

在检索 Python 仓 `gkx_ai_service` 增加算法 Webhook 中转：`POST /internal/gkx-ai/analysis/callback`。

| 项 | as-built |
|----|----------|
| 校验 | `analysis_type` / `task_id` / `event` / `status` |
| 分发 | `enterprise_eval`→Java `.../callback/eval`；`risk_insight`→`.../risk`；`talent_recommend`→`.../recommend` |
| Java URL | `java_callback` 配置/环境变量，禁止硬编码主机 |
| pending | 映射 running，不透传 Java |
| 业务 JSON | 透明中转，不解析多态结果、不写 Java 任务表 |
| D-31 五事件 | `step_started` / `step_completed` 同步转发；`task_completed` 投 MQ；`task_failed` / `task_cancelled` 同步 |
| 幂等 | `task_id+event+node_index` LRU 5000 |
| D-33 | MQ 不可用则同步降级转发（无 result_url） |

对照：`ENT-PY-ANALYSIS-CALLBACK-派单包.md`、`ARCH-ANALYSIS-TASK-设计方案.md` v3.4、`gkx_ai_service/views/callback.py`。

## 产物清单

| 文件 | 作用 |
|------|------|
| `gkx_ai_service/views/callback.py` | 回调路由 + 五事件 + LRU |
| `gkx_ai_service/mq_producer.py` | `task_completed` 投递 |
| `gkx_ai_worker/` | 消费 → camelCase → MinIO → 转发 Java |
| `tests/test_analysis_callback.py` | 关单 16 例 |
| 合并关单 | `ENT-PY-ANALYSIS-完工.md` §回调部分 |

仓：关单日 `demo-svc-topic-py`；同路径现亦在 `lumen-topic-py`（`@router.post("/callback")`）。本叶证据以 2026-07-28 关单为准。

## 偏离说明

| 项 | 说明 |
|----|------|
| 四叶一份 完工.md | 文件名不含本 ID，本次拆出 |
| RabbitMQ/MinIO | 关单：基础设施待部署，Worker 可本地文件兜底 |
| Java callback | 关单明确「接收端待联调」 |
| 算法 `/gdf/tasks/create-and-start` | 关单待对接，非本叶假绿 |

## 验收证据

关单 2026-07-28：

```
tests/test_analysis_callback.py — 16 passed
```

覆盖五事件、缺字段、pending→running、幂等、MQ 降级。Mock 下服务可起（8081）。**无 2026-08 正式 Java 门面联调记录。**

## 架构合规自检

| # | 铁律 | 合规 | 说明 |
|---|------|------|------|
| 1 | 算法只在 Python | ✅ | 本叶只中转，不写评分 |
| 2 | 前端→Java→Python `/internal/*` | ✅ | 回调入口 `/internal/gkx-ai/analysis/callback` |
| 3 | NebulaGraph | ✅ | 不涉及 |
| 4 | 可观测 | ✅ | `gkx_common.observability` |
| 5 | CI/CD | ✅ | 关单待补 pipeline，不伪绿 |
| 6 | demo 不 merge lumen | ✅ | 后迁 lumen-topic-py 是后续工作 |
| 7 | Java 不写算法 | ✅ | 本叶不解析业务结果 |
| 8 | Mock 先行 | ✅ | 单测 Mock |
| 9 | D8 | ✅ | 无 UI |
| 10 | D9 | ✅ | 不造指标 |
| 11 | D10 | ✅ | 无 UI |
| 12 | D12 | ✅ | 不把 demo 端口当 lumen 联调证据 |

## Cost 回填

四叶合并关单共用（CALLBACK/EVAL/RISK/RECOMMEND）：

| 字段 | 值 |
|------|-----|
| actual_tokens | 350000 |
| model_used | zs-glm-5.2 |
| actual_cost | 8 |
| cost_warn | green |

## 遗留风险

Java 三回调 URL、entan/science 异步任务、MQ/MinIO 未在本叶闭合。2026-08-21 正式门面未观察到 step 回写。

## 2026-08-21 正式门面 INT

评估/风险在「创建下游任务失败」处结束，无节点进度。引育 `REC-20260821-002` running>60s 时 `currentNodeName` 一直为 null，随后 Java cancel 为 `cancelled`。**不能**据此证明 `POST /internal/gkx-ai/analysis/callback` → Java `#110–112`。状态保持 integration。

记录：`qa/test-records/KJZTFWXT/ANALYSIS/INT-分析任务中心联调-记录-20260821.md`
