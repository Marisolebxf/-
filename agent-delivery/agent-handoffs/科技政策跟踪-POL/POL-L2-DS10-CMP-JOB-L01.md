# POL-L2-DS10-CMP-JOB-L01 · 科创政策全景 · 力度 Job

> 格式参考 `正式文件/` 与 `templates/`；内容按本次实测与代码实写。

ponytail: full

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时任务已是 `in_progress`。本单不改任务状态，不把任务标 `done`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只在已有 Job 白名单上加 `policy_intensity`，调用已有 `polan.eval.intensity.run` 后再读表。未抄 `intensity.py`，未在路由里打分，未新造 `metric_id`，未改 D4。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶是短实现，未走 Headroom 压缩。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `POL-L2-DS10-CMP-ARCH-SEQ` |
| 图 diff | 未改图。实现已签收边：214 / 218 的 `sub_type=policy_intensity` 调 `polan.eval.intensity.run`，再读 `ads.policy_intensity`。禁止事项未变：不抄公式、不返回演示分、不改 D4、display 不直打这条内部路径。 |
| 会签态 | `draft`（源 ARCH 文首无 frontmatter，原文自记 `draft`；2026-11-03 `human:淮政玮` 已签收该架构叶） |
| 说明 | 本叶不改 Mermaid。 |

## 问题清单

- Java 适配器白名单是 `POL-L2-DS10-CMP-BE-L01`。本单不改 Java。
- 216 的支持力度仍走 `stats` 同步读，不进这条 Job。
- `run()` 抛错时不读表，避免把上一轮分数当成这次结果。查询失败仍原样抛出。

## 修改内容

- `resolve_sub_type` 的白名单 `JOB_SUB_TYPES` 增加 `policy_intensity`。别名只加 `policy:intensity`。裸名 `intensity` 仍拒绝，拒绝方式与原来一样：`PolicyJobRejected` / `INPUT_SCHEMA_INVALID`，HTTP 400。
- `policy_intensity` 与效果、匹配一样不做产业 VID 校验，也不走产业 / 技术领域二选一。
- 新增 `_policy_intensity_rows`：调用已有 `polan.eval.intensity.run`，再 `SELECT * FROM ads.policy_intensity`。带 `policy_ids` / `items` 时按政策 `scope_code` 滤；带 `regions` 时按省级 `scope_code` 或 `scope_name` 滤。都没给则读整表。
- `execute_policy_job` 为该 `sub_type` 增加分支。`harness_mode=intensity_ads`，`result` 是行列表。不走 `harness.dispatch`，不在路由里打分。
- `run()` 抛错，或查到 0 行：`accepted=true`，`result=[]`，`n=0`。不补 0，不补演示分。HTTP 仍是 202。

## 测试结果

- `python -m pytest tests/test_policy_job.py -q --tb=short`
- 25 passed，1 warning（StarletteDeprecationWarning，既有 TestClient）。
- 新断言：未知 `sub_type` 与裸 `intensity` 拒绝；`policy_intensity` 调到 `run()` 并带回表行；别名 `policy:intensity` 在非法产业 VID 下仍执行；表空则 `result=[]`；`run()` 缺维抛错则空且不再读表；HTTP 未知类型 400、空表 202。未连真库。

## 遗留风险

- `run()` 自己会连库写 `ads.policy_intensity`。单测把 `run` 和 `connect` 换成桩。线上有没有行取决于 `run()` 实际写入。
- 结果是行列表，字段沿用表列。未另做契约单，未改 D4。
- 任务状态仍是 `in_progress`。

## CI/CD（必填）

- 分支：`dev`
- commit：`bce912217e83af29d35c9ba5618164927f9907ab`
- pipeline URL / ID：已推 `origin/dev`（`40d84e2..bce9122`）。本单未查 pipeline。
- 部署 namespace / 镜像 tag：未部署
- K8s rollout：未触发
- dev 测试 URL / 命令与结果：本地 `pytest tests/test_policy_job.py`，25 passed

## 可观测性（建议）

- OTEL_SERVICE_NAME：未新加埋点。Job 仍走既有入口。`run()` 写不出时打一条 warning。
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `lumen-algo-py` `vendor/entan-py/polan/job.py`
- `lumen-algo-py` `tests/test_policy_job.py`
- 未改：`scripts/seed_gapfill_policy_cmp.py`、`scripts/mysql/gapfill_policy_cmp.sql`，也未改 `intensity.py`、Java。
