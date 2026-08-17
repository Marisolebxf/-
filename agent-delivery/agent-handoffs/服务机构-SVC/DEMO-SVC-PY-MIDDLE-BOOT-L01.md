# DEMO-SVC-PY-MIDDLE-BOOT-L01 · 产业服务链 B — gkx-svc 中间层骨架

> 日期：2026-08-17  
> Task：`DEMO-SVC-PY-MIDDLE-BOOT-L01`  
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
| 说明 | 对照 `gkx_search_service` 最小 FastAPI 包；复用 `gkx_common.response.R` / OTel middleware |

## 范围与实现

- 新包 `repos/lumen-topic-py/gkx_svc_service/`
  - `GET /healthz`
  - `POST /internal/gkx-svc/health`
  - `POST /internal/gkx-svc/boot/ping`（Mock 包络 + 后续路由占位）
- 自检：`tests/test_gkx_svc_boot.py`
- **非范围**：真实检索 / 门户 ADS / Feign Java / svc 算法

## 偏离说明

- 独立 app 入口（`gkx_svc_service.main:app`），不并入 search 进程；K8s 镜像/部署留给 E0。  
- **`origin/dev` 受保护**：代码推送在 `feat/svc-middle-boot`，需人类 MR 合入 `dev`。

## 产物清单

| 产物 | 路径 |
|------|------|
| 服务入口 | `repos/lumen-topic-py/gkx_svc_service/main.py` |
| BOOT 路由 | `repos/lumen-topic-py/gkx_svc_service/views/boot.py` |
| 测试 | `repos/lumen-topic-py/tests/test_gkx_svc_boot.py` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DEMO-SVC-PY-MIDDLE-BOOT-L01.md` |

## 验收证据

- [x] `pytest tests/test_gkx_svc_boot.py` 绿
- [x] 前缀 `/internal/gkx-svc/**`；统一 `R` 包络 `code==0`
- [x] D12：落在 `lumen-topic-py`，非 demo-svc-topic-py

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 骨架无算法 |
| 2 | 调用链 Java→/internal | ✅ 前缀预留 |
| 4 | 可观测 | ✅ TraceHeaderMiddleware |
| D12 | 正式仓 | ✅ lumen-topic-py |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~2 万 |
| actual_cost | 估 <$1 |
| cost_warn | false |

## 联调确认

联调通过：BOOT 包络可探活；下游 SEARCH/FACADE 可按此前缀扩展。下一叶：`DEMO-SVC-PY-MIDDLE-SEARCH-L01`（及可并行开仓的 `DEMO-SVC-PY-SVCAN-BOOT-L01`）。
