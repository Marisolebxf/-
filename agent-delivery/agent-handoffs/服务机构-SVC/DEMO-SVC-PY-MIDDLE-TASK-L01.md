# DEMO-SVC-PY-MIDDLE-TASK-L01 · 产业服务链 B — 任务/callback 适配

> 日期：2026-08-17  
> Task：`DEMO-SVC-PY-MIDDLE-TASK-L01`  
> 总控：`DEMO-SVC-ABCD-长任务总控.md`（已授权 · human:侯佳伟）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 内存任务表 + 映射 svcan 样板；明确不签发 snapshot |

## 范围与实现

- `POST /internal/gkx-svc/analysis/tasks/create`（Java 必填 `task_id`）→ 调 `lumen-algo-py` `/internal/v1/svcan/sample/shortboard`
- `POST /internal/gkx-svc/analysis/tasks/status`
- `POST /internal/gkx-svc/analysis/callback`（若带 snapshot id 则 **忽略**，`snapshot_ignored=true`）
- **非范围**：Java async Job 真源、正式持久化任务表

## 偏离说明

- 与 BOOT/SEARCH 同分支 `feat/svc-middle-boot`（`origin/dev` 受保护）；MR：https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/merge_requests/1

## 产物清单

| 产物 | 路径 |
|------|------|
| task views | `repos/lumen-topic-py/gkx_svc_service/views/task.py` |
| 测试 | `repos/lumen-topic-py/tests/test_gkx_svc_boot.py` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DEMO-SVC-PY-MIDDLE-TASK-L01.md` |

## 验收证据

- [x] create/status/callback 包络可调；`result_snapshot_id` 恒为 null
- [x] algo 不可达时 status=failed 诚实失败（本机无 algo 时 create→failed 可接受）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 2 | 调用链 | ✅ 中层→algo /internal |
| Job 真源 | 不自签 snapshot | ✅ |
| D12 | lumen-topic-py | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~2.5 万 |
| actual_cost | 估 <$1.5 |
| cost_warn | false |

## 联调确认

联调通过：任务 create/status/callback 可映射 algo 且不签发 snapshot。下一叶：`LUMEN-SVC-JAVA-JOB-L01`（等 FACADE）。
