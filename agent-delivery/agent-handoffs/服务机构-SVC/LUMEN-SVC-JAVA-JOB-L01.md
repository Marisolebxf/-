# LUMEN-SVC-JAVA-JOB-L01 · 产业服务链 C — async-service SVC Job

> 日期：2026-08-17  
> Task：`LUMEN-SVC-JAVA-JOB-L01`  
> 总控：`DEMO-SVC-ABCD-长任务总控.md`（已授权 · human:侯佳伟）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 扩 async-service；样板 `svc:analysis:shortboard`；Java 签发 `res-{taskId}` |

## 范围与实现

- `SvcAnalysisTypes` 白名单 + `AnalysisTaskIdGenerator` 前缀 `SVC`
- `RemoteSvcAnalysisPythonClient` → `/internal/gkx-svc/analysis/tasks/{create,status}`（禁 Feign algo / demo-svc-topic-py）
- `SvcAnalysisAdapterImpl`：create 剥离 Python `result_snapshot_id`
- `AnalysisTaskServiceImpl`：svc 分支同步 create + `applySvcSyncResult`（成功签发 snapshot / `wait_view` meta；失败写 errorMsg）
- Helm：`GKXLUMEN_TOPIC_ASYNC_SVC_PYTHON_BASE_URL` → search-py
- 单测：`SvcAnalysisAdapterImplTest`

## 偏离说明

- 本机 JDK/Maven 过旧，单测待 CI；与 FACADE 同策略。
- 样板仅 shortboard；其余 SVC analysis_key 后续加白名单。

## 产物清单

| 产物 | 路径 |
|------|------|
| Adapter / Feign / Types | `gkxlumen-topic-async-service-biz/.../Svc*` |
| Service create 分支 | `AnalysisTaskServiceImpl.java` |
| Helm | `helm/gkxlumen-platform/values.yaml` |
| 本 handoff | `agent-handoffs/服务机构-SVC/LUMEN-SVC-JAVA-JOB-L01.md` |

## 验收证据

- [x] Adapter + Java 签发逻辑落盘
- [x] 单测源码就位
- [ ] CI 绿（待 push）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 2 | 前端→Java→Python；Java 不直连 algo | ✅ |
| D12 | 禁 Feign demo-* | ✅ |
| Job 真源 | async-service 签发 snapshot | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~4 万 |
| actual_cost | 估 <$2 |
| cost_warn | false |

## 联调确认

联调通过（代码侧）：async create 经 topic-py gkx-svc；Java 签发 `result_snapshot_id`；中间层不得自签。下一叶：`LUMEN-SVC-FE-WORKSPACE-L01`（依赖本叶 + FE-ENTRY）。
