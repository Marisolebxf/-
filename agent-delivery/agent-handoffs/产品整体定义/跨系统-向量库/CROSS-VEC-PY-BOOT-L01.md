# CROSS-VEC-PY-BOOT-L01 · lumen-algo-py-api CrashLoop — Docker 未 COPY polan

> 事故：`lumen-platform-algo-py` 滚 `f07f8754` / `e5b06525` CrashLoopBackOff，exit 1，`ModuleNotFoundError: No module named 'polan'`，healthz connection refused。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 已 claimed；开工转 `in_progress`；lock 24h；bugfix，AV-0 目标 `pending_test` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只补 `Dockerfile.api` 一行 COPY；未改 Python 业务、未删 enrich 路由、未新 pip、未扩 worker。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 单仓 Docker 一行修，本机未挂 Headroom |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（镜像打包漏 COPY，不改调用链图） |
| 图 diff | 无。运行时仍是 `main:app` → industry / jobs → `polan.graph.entity` |
| 会签态 | N/A |

## 范围与实现

**根因**：`docker/Dockerfile.api` 只 COPY `lumen_common` / `lumen_algo_service` / `conf`。`main.py` 顶层 import `industry` / `industry_jobs` / `policy_industry` → `industry_embed.py` / `industry_enrich.py` 顶层 `from polan.graph.entity import …`。`policy/_ensure_polan_on_path()` 找 `/app/vendor/entan-py/polan/harness` 与 `/app/polan/harness`，镜像两处都没有。本机 pytest 绿是因为工作区有 `vendor/entan-py`。

**做**：

1. `Dockerfile.api` 增加 `COPY vendor/entan-py/polan/ ./polan/`（落到 `/app/polan`，命中 path 钩子第二候选；WORKDIR `/app` 也让 `from polan…` 直接可解析）。
2. `lumen_algo_worker` 现无 `industry_embed` / `industry_enrich` / `industry_job` import，**不扩** `Dockerfile.worker`（其已有 harness/focus_one 切片，够当前 worker）。
3. 一条 runnable check：`tests/test_docker_api_copies_polan.py` 读 Dockerfile 断言含 `COPY vendor/entan-py/polan/`。

**不做**：改 Python 业务逻辑、删 enrich 路由、新 pip、改 `.gitignore` / `requirements.txt`、扩 worker graph COPY。

## 偏离

无。对照 `Dockerfile.entan-api` 整份 `COPY vendor/entan-py/polan ./polan`，本叶 api 镜像同落 `/app/polan`。

## 产物清单

- `lumen-algo-py/docker/Dockerfile.api`（+1 COPY）
- `lumen-algo-py/tests/test_docker_api_copies_polan.py`
- 本 handoff

## 验收证据

- `python -m pytest tests/test_docker_api_copies_polan.py -q` → **1 passed**
- worker：`rg` `lumen_algo_worker` 无 industry_embed / industry_enrich / industry_job，未改 `Dockerfile.worker`

### 人怎么确认下一轮 `k8s:deploy`

1. 新 ReplicaSet 镜像 tag = 本叶 SHA（见 CI/CD），旧 `7bcbf7f446` 可退。
2. `lumen-platform-algo-py` 新 Pod **Ready**，不再 CrashLoopBackOff / exit 1。
3. 日志不再出现 `ModuleNotFoundError: No module named 'polan'`。
4. `healthz` 可达（不再 connection refused）。

## 遗留风险

- worker 若日后顶层 import `industry_embed` / enrich，现有切片 COPY 仍缺 `polan/graph/`；到那时再整份 COPY 或补 `graph/`。
- 本机无 Docker，未本地 `docker build` 验 import；锁在 Dockerfile 的 COPY 行 + pytest 读文件。

## CI/CD（必填）

- 分支：`lumen-algo-py` `origin/dev`（先 `git pull --ff-only`，基线 `f07f875`）
- commit：**`b82b3f3`** `fix(docker): COPY vendor polan into api image [agent:algorithm-agent]`
- pipeline：push 触发 GitLab CI → `k8s:deploy`
- K8s rollout：等人确认新 Pod Ready（本叶不标已上线）
- dev 测试：本机 pytest 1 passed；未本机构镜像

## 可观测性（建议）

- 未改 OTEL / `observability.ts`；原 CrashLoop 使 healthz 起不来，修后探针应恢复。

## 涉及文件

- `lumen-algo-py/docker/Dockerfile.api`
- `lumen-algo-py/tests/test_docker_api_copies_polan.py`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python `/internal/*` | ✅ 未改路由 / 算法 |
| 调用链不可越层 | ✅ 未改 Java / 前端 |
| 图谱仅 Nebula | ✅ 未改图引擎 |
| 可观测 | ✅ 未拆 instrument ENTRYPOINT |
| CI/CD | ✅ push `origin/dev`，未 force |
| D12 | ✅ 未调 `demo-*` |
| 数据策略 | ✅ 未改 ADS / 业务逻辑 |
| Java 不写算法 | ✅ 零 Java |
| D8 / D9 / D10 | N/A |
| 未新 pip | ✅ |
| 未改 `.gitignore` / `requirements.txt` | ✅ |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 48000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.29 |
| cost_warn | green |

口径：algorithm 默认 75/25；B 档 `$3/$15` per 1M；`48000×0.75×3/1e6 + 48000×0.25×15/1e6 = 0.288` → 0.29。
