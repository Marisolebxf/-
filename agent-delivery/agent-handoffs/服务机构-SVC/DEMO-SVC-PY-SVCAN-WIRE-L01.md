# DEMO-SVC-PY-SVCAN-WIRE-L01 · topic-py 按 analysis_key 调 svcan /analyze

> 日期：2026-08-18  
> Task：`DEMO-SVC-PY-SVCAN-WIRE-L01`  
> 总控：`DEMO-SVC-FULL-底座后全量-长任务总控.md` / `DEMO-SVC-GATE1-全量派单.md`（已授权 · human:侯佳伟）  
> 上游：`DEMO-SVC-PY-SVCAN-MODELS-L01`（`10ece36` · algo `/analyze` + 八叶子）

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
| 说明 | 只改 task 路由解析 + 单测 mock httpx；不新依赖；未知键诚实 422，禁止静默 shortboard |

## 范围与实现

仓：`repos/lumen-topic-py` · `gkx_svc_service/views/task.py`

| 项 | 行为 |
|----|------|
| 解析 | `analysis_key` / `analysisKey` → `svcan.{leaf}.v0`；或 `analysisType`=`svc:analysis:{leaf}`；或裸 `leaf` |
| 调用 | `POST {_algo_base}/internal/v1/svcan/analyze` body=`{analysis_key, leaf, params}` |
| 未知键 | `Rerr` code=422 + `supported_keys` / `supported_types`；**不**默认 shortboard |
| 成功/失败 | 仍写内存 task：`succeeded`+result / `failed`+error；`result_snapshot_id` 恒 `None` |
| callback | 契约不变；仍丢弃 snapshot |

八叶子：`org_coverage` `org_trend` `tech_power` `shortboard` `graph` `shenzhen` `attract` `cultivate`。

## 偏离说明

- 本机无法直连 K8s NodePort / 集群 DNS 做外网 create 冒烟；证据以 pytest + GitLab deploy 为准。  
- Job 全链路（Java async → Feign create）需登录态，未在本叶伪造 token。

## 产物清单

| 产物 | 路径 |
|------|------|
| 路由 | `gkx_svc_service/views/task.py` |
| 单测 | `tests/test_gkx_svc_boot.py`（含 analyze 路由 / 未知键 / analysisType） |
| 本 handoff | `agent-handoffs/服务机构-SVC/DEMO-SVC-PY-SVCAN-WIRE-L01.md` |

## 验收证据

- [x] 不再写死 `/sample/shortboard`；`tech_power` 等走 `/analyze`  
- [x] 未知 / 缺 key → code=422 诚实错误  
- [x] `py -3 -m pytest tests/test_gkx_svc_boot.py` → **16 passed**  
- [x] commit `73492fe` push `origin/dev`  
- [x] pipeline [5197](https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5197)；play `deploy:search-py` **22740 success**  
- [x] 上游 algo：pipeline [5195](https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/pipelines/5195) `deploy:api` **22729** / `deploy:worker` **22730** success（`10ece36`，`/analyze` 已在线）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 2 | FE→Java→topic-py→algo `/internal/*`；Java 不直连 algo | ✅ |
| 1 | 算法只在 Python（algo） | ✅ |
| D12 | 不 Feign demo-* | ✅ |
| snapshot | 中间层不签发 | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~4.5 万 |
| actual_cost | 估 <$3 |
| cost_warn | false |

## CI/CD

- 分支：`dev`
- commit：`73492fe6b248186ca6b83159be19dd9638591f77`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5197
- job：`deploy:search-py` https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/jobs/22740 **success**
- algo（依赖）：https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/pipelines/5195 · `deploy:api`/`deploy:worker` 已绿

## 开放项

1. **`LUMEN-SVC-FE-ANALYSIS-FULL-L01`**：FE 八叶接线 — **不认领**。  
2. 带鉴权的 Job create E2E（Java → Feign → 本层 → algo）留给 QA / 联调闸门。

## 联调确认

联调通过（中间层）：按 `analysis_key`/`analysisType` 调 `/analyze`；未知键 422；create/status/callback 包络与 snapshot 铁律保持；search-py 已热更。下一闸：带用户态 Job 八叶抽样 + FE。
