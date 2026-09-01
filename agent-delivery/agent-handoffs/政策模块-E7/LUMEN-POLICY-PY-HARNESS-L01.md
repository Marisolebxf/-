# LUMEN-POLICY-PY-HARNESS-L01 · 政策 harness 三种包装

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-PY-B-总派单.md`](./LUMEN-POLICY-PY-B-总派单.md)  
> 前序：[`LUMEN-POLICY-PY-BOOT-L01.md`](./LUMEN-POLICY-PY-BOOT-L01.md)（as-built `vendor/entan-py/polan`）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h；SHARED 缺口（policy task_type / runner）本叶一并补，不另开 SHARED 叶 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 新模块只加 `polan/harness/`，未改算子 `run()` / 打分 / 抽词；复用 `lumen_common.tasks` CAS，不自造 Redis 队列 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 新包装 + 假算子单测，无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。禁止事项补「专题 Job 一次 load 全表 4 万+须走 harness」。分析 Job 只调 harness，灌数仍可调原 `run()` |
| 会签态 | `approved`（`01-data-flow.md` frontmatter；本叶不翻签） |

## 偏离说明

- 总控路径写 `vendor/polan/harness/`；as-built 与 BOOT 同树，写在 `vendor/entan-py/polan/harness/`。
- SHARED 未单开：`analysis_type=policy` + 五个 `sub_type` 直接注册进 `lumen_common.tasks.lifecycle`，worker `Dockerfile.worker` COPY harness + `focus_one.py`。
- 大结果集 fan-in：父任务 CAS claim 子任务后可在本进程执行分片（避免占满 semaphore 死等）；他 worker 抢到则父任务等 `result()`。仍走 `TaskRepository.claim` pending→running，无 Redis 队列。

## 产物清单

- 代码：`lumen-algo-py` `10f58f57059aca9cdfa8ff770eaa7eafc8185913` → `origin/dev`
- harness：`vendor/entan-py/polan/harness/core.py`
- 入口：`run_sync` / `run_threadpool` / `run_worker_fanin`（另 `dispatch` 按用量选择）
- 流图：`storage/POLICY/01-data-flow.md` 禁止事项 + amendment_note（拓扑未改）
- 本文 handoff

## 验收证据

- `python -m pytest -q tests/test_policy_harness.py` → **10 passed**
- 全仓 `python -m pytest -q --ignore=vendor` → **311 passed, 1 skipped**
- 假算子桩覆盖三种包装；`focus_one.analyze` 真算子回归仍调原方法；`run_sync` 拒 >32 条；`run_threadpool` 拒 40000 条
- `CLAIM_ANALYSIS_TYPES` 含 `policy`；`TaskManager.create_and_start` 政策任务不要求 `enterprise_codes`
- eval/basic/graph/text/models 本叶 **无 diff**

## 范围与实现

- 小集合：`run_sync` 直调已有 `polan.eval.focus_one.analyze`（或注入 operator）。
- 中等：`run_threadpool` 按 `policy_id`（可换区域码 / 产业 VID）分片，默认 batch=32，超时可重试。
- 大结果集：`run_worker_fanin` 创建 `policy_shard` 子任务，CAS claim + fan-in。
- OTel tracer `gkx.polan.policy.harness`：外层 `policy.harness.{sync|threadpool|fanin}` + 每片 `policy.harness.shard`。算子内部未改。
- 灌数批处理仍走原 `eval/*.run()` / `load_policies`，本叶未碰。

## 修改内容

| 路径 | 动作 |
|------|------|
| `vendor/entan-py/polan/harness/` | 新增三种包装 |
| `lumen_common/tasks/lifecycle.py` | `policy` 类型 / `POLICY_NODES` / claim 列表 |
| `lumen_common/tasks/executor.py` | `_run_policy_node` 只调 harness |
| `lumen_common/tasks/manager.py` | 政策任务免企业码 |
| `lumen_common/algorithms/policy/` | 给 worker 补 `polan` sys.path |
| `docker/Dockerfile.worker` | COPY harness + `focus_one.py` |
| `tests/test_policy_harness.py` | 三种包装 + CAS + 真算子回归 |

## 测试结果

```text
python -m pytest -q tests/test_policy_harness.py
# 10 passed

python -m pytest -q -p no:cacheprovider --ignore=vendor
# 311 passed, 1 skipped in 234s
```

## CI/CD（必填）

- 分支：`lumen-algo-py` `origin/dev`
- commit：`10f58f57059aca9cdfa8ff770eaa7eafc8185913`
- pipeline：push 后 GitLab `dev`；`image:api` / `image:worker` 随 origin/dev 自动发；entan 制品仍 manual
- 部署：`lumen-platform-algo-py-worker` 吃到 policy runner；entan-api 镜像含 `polan/harness`（下次 entan 制品构建）
- 本叶未改 helm JDBC、未 CREATE SPACE、未写 `gkx_chain`

## 可观测性

- OTEL_SERVICE_NAME：worker `lumen-platform-algo-py-worker`；entan-api `gkxlumen-entan-py-api`
- harness span：`gkx.polan.policy.harness` / `policy.harness.sync|threadpool|fanin` + `policy.harness.shard`
- 算子内部 span 未改

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ |
| 前端→Java→Python `/internal/*` | ✅ 本叶不暴露 `/v1` 给专题 |
| 图谱 Nebula `demo_gkx_chain` | ✅ 未 CREATE `gkx_policy`、未写 `gkx_chain` |
| 可观测 | ✅ harness + 每片 span |
| CI/CD | ✅ 推 `origin/dev`；禁 force |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / Java 不直连 nGQL | ✅ |
| 数据策略 ADS `demo_gkxlumenx_*` | ✅ 未改正式 JDBC |
| D8 / D10 | N/A 无 UI |
| D9 8 件套 | N/A 本叶不改口径 |
| D12 lumen 不调 demo **服务** | ✅ |

## 遗留风险

- 分析 Job 叶须只调 harness，禁止直调 `eval.*.run()` 当在线路径。
- `lumen-algo-py-worker` 镜像需滚到本 SHA 后才能 claim `policy` 任务；entan 镜像需单独制品才带上 harness 供 `/internal` 进程 import。
- fan-in 子任务 `task_id` 形如 `{parent}:s{i}`，Java 侧勿与自签 snapshot 混淆。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 88000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.59 |
| cost_warn | green |
