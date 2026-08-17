# DEMO-SVC-PY-SVCAN-BOOT-L01 · 产业服务链 B — svcan 启动与样板键

> 日期：2026-08-17  
> Task：`DEMO-SVC-PY-SVCAN-BOOT-L01`  
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
| 说明 | 对照 chain router 最小挂载；样板键 mock，不写正式库 |

## 范围与实现

- `GET /internal/v1/svcan/health`
- `POST /internal/v1/svcan/sample/shortboard`（短板样板键 `svcan.shortboard.v0`）
- 挂入 `lumen_algo_service.main`
- **非范围**：真实短板算法、Nebula、Job 全链路、中间层 TASK 适配

## 偏离说明

无。

## 产物清单

| 产物 | 路径 |
|------|------|
| views | `repos/lumen-algo-py/lumen_algo_service/views/svcan.py` |
| 测试 | `repos/lumen-algo-py/tests/test_svcan_boot.py` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DEMO-SVC-PY-SVCAN-BOOT-L01.md` |

## 验收证据

- [x] TestClient health + sample shortboard 绿
- [x] mock+GAP 诚实

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法在 Python | ✅ |
| 2 | 经 /internal | ✅ |
| D12 | lumen-algo-py | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~1.5 万 |
| actual_cost | 估 <$1 |
| cost_warn | false |

## 联调确认

联调通过：svcan 可启动且样板键可调。下一依赖：`DEMO-SVC-PY-MIDDLE-TASK-L01` / `LUMEN-SVC-JAVA-JOB-L01`。
