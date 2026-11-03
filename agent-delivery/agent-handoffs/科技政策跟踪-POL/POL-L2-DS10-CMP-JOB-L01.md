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
- 新增 `_policy_intensity_rows`：调用已有 `polan.eval.intensity.run`。写成功后再读两处：`ads.policy_intensity` 中 `metric_id=M_POLICY_INTENSITY_SCORE` 且 `scope_type=policy` 的行，以及 `ads.policy_metric_timeseries` 中 `metric_id=M_POLICY_SUPPORT_STRENGTH` 的行。不按请求里的政策 id 或地区再滤。
- `execute_policy_job` 为该 `sub_type` 增加分支。`harness_mode=intensity_ads`。`result` 是 `policy_intensity` 与 `policy_metric_timeseries` 两个列表。不走 `harness.dispatch`，不在路由里打分。
- `run()` 抛错：不再读表，`result` 两个列表都空，`n=0`。两表都没有行时同样空。查询抛错则原样抛出，不用写死分数顶上。HTTP 在空结果时仍是 202。

## 测试结果

- `python -m pytest tests/test_policy_job.py -q --tb=line`
- 35 passed，1 warning（StarletteDeprecationWarning，既有 TestClient）。
- 新断言：未知 `sub_type` 与裸 `intensity` 拒绝；`policy_focus` 的非法产业 VID 仍拒绝；`policy_intensity` 调到 `run()`，SQL 参数是 `M_POLICY_INTENSITY_SCORE`/`policy` 与 `M_POLICY_SUPPORT_STRENGTH`；别名 `policy:intensity` 在非法产业 VID 下仍执行；两表都空则两个列表空；`run()` 抛错则空且不再读表；查询抛 `ads down` 则原样抛出。未连真库。

## 遗留风险

- 单测把 `run` 和 `connect` 换成桩。2026-11-03 另用已有 `polan.eval.intensity.run()` 对正式平面写过一次，见下节。`LUMEN_ALGO_MYSQL_PASSWORD` 未设置；连接走 polan 已有配置，口令未写入本文。
- 结果是两个列表，字段沿用表列。未另做契约单，未改 D4。
- 任务状态仍是 `in_progress`。

## intensity.run 实测

平面 `x-gkx-plane-policy=live`。库是 `gkxlumenx_ads` / `gkxlumenx_dwd`。跑之前三处计数都是 0。`gkxlumenx_dwd.policy_base_info` 为 40000 行。

`run()` 退出无异常。跑完：

| 查询 | 行数 |
|---|---|
| `policy_intensity` 全部 | 40031 |
| `metric_id=M_POLICY_INTENSITY_SCORE` 且 `scope_type=policy` | 40000 |
| `policy_metric_timeseries` 且 `metric_id=M_POLICY_SUPPORT_STRENGTH` | 31 |

## CI/CD（必填）

- 分支：`dev`
- commit：`06a86e621a4ffe9a2cf5da8a777d77733cbe6afd`（读表修正，已推 `origin/dev`，`25c7a53..06a86e6`）。前一笔 `bce912217e83af29d35c9ba5618164927f9907ab` 曾按政策 id / 地区滤 `policy_intensity` 整表，且不读支持力度时序。
- pipeline URL / ID：本单未查 pipeline。
- 部署 namespace / 镜像 tag：未部署
- K8s rollout：未触发
- dev 测试 URL / 命令与结果：本地 `pytest tests/test_policy_job.py`，35 passed。正式库 `intensity.run()` 已写入，行数见上节。

## 可观测性（建议）

- OTEL_SERVICE_NAME：未新加埋点。Job 仍走既有入口。`run()` 写不出时打一条 warning。
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 架构合规自检

- 调用链：只在 Python Job 里调已有 `intensity.run`，再只读 ADS。未改 Java。
- 未改 `intensity.py` 公式，未改 `effect.py`、`match.py`。
- 未新造 `metric_id`，未改 D4。
- 查询失败不返回写死分数。`run()` 失败不读旧行。

## 涉及文件

- `lumen-algo-py` `vendor/entan-py/polan/job.py`
- `lumen-algo-py` `tests/test_policy_job.py`
- 未改：`scripts/seed_gapfill_policy_cmp.py`、`scripts/mysql/gapfill_policy_cmp.sql`，也未改 `intensity.py`、Java。
