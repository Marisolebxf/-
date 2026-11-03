# POL-L2-DS10-SENT-IMPL-PY · 科创政策全景 · 政策舆情评估 · 效果与匹配 Job

> 格式参考 `正式文件/` 与 `templates/`；内容按本次实测与代码实写。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时任务已是 `in_progress`。本单不改 `task-registry.yaml`，不把任务标 `done`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只加两个 sub_type 的调用与只读查询。未改 `effect.py` / `match.py` 公式，未跳过已签收的查表口径。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶是短实现，未走 Headroom 压缩。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `POL-L2-DS10-SENT-ARCH-SEQ` |
| 图 diff | 未改图。实现已签收边：209 `effect.run` 后读 `ads.policy_effect`（`region_effect`）与 `policy_metric_timeseries`（`M_POLICY_IMPLEMENTATION_EFFECT`）；212 `match.run` 后读 `ads.policy_match`。禁止事项未变：不重写公式、不写死分数、不挂 `/v1/policy`。 |
| 会签态 | `draft`（源 ARCH 文首无 frontmatter，原文自记 `draft`；2026-11-03 `human:淮政玮` 已签收该架构叶） |
| 说明 | 本叶不改 Mermaid。 |

## 问题清单

- Java `PolicyAnalysisTypes` 白名单仍只有时序 / 区域 / 深圳 / 焦点。本单范围不含 `gkxlumen-topic-policy`，也未改 async 白名单。浏览器要打到这两个 sub_type，还要另单放行 Java。
- `api/policy_routes.py` 的 jobs 注释仍写「禁止在线直调 eval.*.run()」。路由文件不在本单范围，实际入口已走 `execute_policy_job` 的签收例外。

## 修改内容

- `JOB_SUB_TYPES` 增加 `policy_effect`、`policy_match`。别名只加 `policy:effect`、`policy:match`。裸名 `effect` / `match` 不收录。
- 这两个 sub_type 不做产业 VID 格式校验，也不走深圳三维的产业 / 技术领域二选一。其余 sub_type 仍走原校验。
- `policy_effect`：调用已有 `polan.eval.effect.run`，再查 `ads.policy_effect`（`scope_type=region_effect`）和 `ads.policy_metric_timeseries`（`metric_id=M_POLICY_IMPLEMENTATION_EFFECT`）。查到的行放进 `result`。两表都空则两个列表都空。
- `policy_match`：调用已有 `polan.text.match.run`，再查 `ads.policy_match`。带 `subject_id` / `subject_type` 时按主体过滤。无行则 `result` 为 `[]`。
- 查询失败原样抛出，不用写死 JSON 顶上。未改 `effect.py`、`match.py`、`lumen_algo_service/main.py`。

## 测试结果

- `python -m pytest tests/test_policy_job.py -q --tb=short`
- 24 passed，1 warning（StarletteDeprecationWarning，既有 TestClient）。
- 新断言：未知 sub_type 拒绝；裸 `effect` / `match` 拒绝；`policy_focus` 非法产业 VID 仍拒绝；`policy_shenzhen` 产业与技术同时出现仍拒绝；`policy_effect` 不带产业 VID 可执行，非法 VID 加技术领域也不被二选一拦住；表空则空；查询异常不回写死结果。未连真库。

## 遗留风险

- `run()` 自己会连库写表。单测把 `run` 和 `connect` 换成桩。线上空表取决于 `run()` 实际写入，本单没有灌数。
- 效果结果是 `{policy_effect, policy_metric_timeseries}` 两个列表；匹配结果是列表。字段名未另做契约单。
- 任务状态仍由注册表维持，本单未改为 `done`。

## CI/CD（必填）

- 分支：`dev`
- commit：`b4a414e08889f757d4a82ae3e8b155e93a4b1b83`
- pipeline URL / ID：已推 `origin/dev`（`3827118..b4a414e`）。本单未查 pipeline。
- 部署 namespace / 镜像 tag：未部署
- K8s rollout：未触发
- dev 测试 URL / 命令与结果：本地 `pytest tests/test_policy_job.py`，24 passed

## 可观测性（建议）

- OTEL_SERVICE_NAME：未新加埋点。Job 仍走既有入口。
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `lumen-algo-py` `vendor/entan-py/polan/job.py`
- `lumen-algo-py` `tests/test_policy_job.py`
- 未纳入提交：仓内已有的 `scripts/mysql/gapfill_policy_*.sql`、`scripts/seed_gapfill_policy_*.py`、`scripts/run_policy_sent_mock_ads.py`（他人未提交文件）
