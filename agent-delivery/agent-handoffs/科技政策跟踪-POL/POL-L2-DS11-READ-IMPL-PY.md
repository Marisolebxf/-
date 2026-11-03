# POL-L2-DS11-READ-IMPL-PY · 政策分析评价 · 结果解读报告多维展示 · 焦点与摘要 Job

> 格式参考 `正式文件/` 与 `templates/`；内容按本次实测与代码实写。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 从 `ready` 认领，锁定 24 小时。本单不改 `task-registry.yaml`，不把任务标 `done`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只在已有 Job 白名单上加两个读表键。未改 `focus.py`，未调用会清空整表的文本解析，未跳过已签收的查表口径。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶是短实现，未走 Headroom 压缩。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `POL-L2-DS11-READ-ARCH-SEQ` |
| 图 diff | 未改图。实现已签收边：`policy_focus_ads` 调用 `polan.eval.focus.run` 后读 `ads.policy_focus`（`policy_id` 非空）；`policy_text_parse` 只读 `ads.policy_text_parse.summary`。禁止事项未变：不改删除范围，不在请求里调用文本解析，不把展示打到 `/v1/policy`。 |
| 会签态 | `draft`（源 ARCH 文首无 frontmatter，原文自记 `draft`；2026-11-03 `human:淮政玮` 已签收该架构叶） |
| 说明 | 本叶不改 Mermaid。 |

## 问题清单

- 无。Java 白名单不在本单。浏览器要打到这两个 sub_type，仍要另单放行展示侧。

## 修改内容

- `JOB_SUB_TYPES` 增加 `policy_focus_ads`、`policy_text_parse`。未删除已有键。合并时保留远端已有的 `policy_intensity`。
- 这两个新键与 `policy_effect` 一样，不做产业 VID 校验，不收 items。别名未改：`focus` / `policy:focus` 仍是 `policy_focus`。
- `policy_focus` 仍走 `harness.dispatch`，仍把 items 交给 harness。没有改成 `focus.run`。
- `policy_focus_ads`：调用已有 `polan.eval.focus.run`，再 `SELECT focus_score, ext FROM ads.policy_focus WHERE policy_id IS NOT NULL`。`title`、`explanation` 从 `ext` 读出。不改 `focus.py`，不扩大 DELETE，不调 `focus-one`。无行则 `result` 为 `[]`。
- `policy_text_parse`：只 `SELECT summary FROM ads.policy_text_parse`。这次请求不调用 `polan.text.parse.run`。无行则 `result` 为 `[]`。查询失败原样抛出，不返回写死段落。

## 测试结果

- `python -m pytest tests/test_policy_job.py -q --tb=line`
- 合并远端 `policy_intensity` 后：36 passed，2 warnings（Starlette/FastAPI 既有弃用警告）。
- 新用例 `test_focus_ads_and_text_parse_read_ads`：`policy_focus` 仍进 harness 且不调用 `focus.run`；`policy_focus_ads` 不要求合法产业 VID，读出 `focus_score` 与 `ext` 里的标题和说明；两表空则空；`policy_text_parse` 不调用文本解析；查询异常不回写死摘要。未连真库。

## 遗留风险

- `focus.run()` 自己会连库，并按原范围删除 `policy_id` 非空行再写入。单测把 `run` 和 `connect` 换成桩。线上有没有行取决于这次 `run()` 实际写入，本单没有灌数。
- 焦点结果是 `{focus_score, title, explanation}` 列表；摘要结果是 `{summary}` 列表。字段名未另做契约单。
- 展示 URL 仍不应指到 `/v1/policy`。本单未改 Java、未改 D4、未新造 `metric_id`。
- 任务状态仍由注册表维持，本单未改为 `done`。

## CI/CD（必填）

- 分支：`dev`
- commit：`177b80c7669b267b5fe8acab7e0c93c4c39bce4e`（焦点与摘要 Job）；已含在 `origin/dev` 尖端 `2d912496b74750e3402b9d5867ea48d19e7e23c6`
- pipeline URL / ID：已在 `origin/dev`。本单未查 pipeline。
- 部署 namespace / 镜像 tag：未部署
- K8s rollout：未触发
- dev 测试 URL / 命令与结果：本地 `pytest tests/test_policy_job.py`，36 passed

## 可观测性（建议）

- OTEL_SERVICE_NAME：未新加埋点。Job 仍走既有入口。
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `lumen-algo-py` `vendor/entan-py/polan/job.py`
- `lumen-algo-py` `tests/test_policy_job.py`
- 未纳入本单提交：仓内他人的 `k8s/README.md`、`gapfill_policy_eval_shell` 灌数脚本。远端已有的 `policy_intensity` 与解读壳灌数提交保持原样。

## 架构合规自检

- ✅ 算法只在 Python。本单只改 `lumen-algo-py` 的 Job。Java 未写算法。
- ✅ 调用链仍是前端 → Java → `POST /internal/policy/jobs/execute`。未把展示浏览器指到 `/v1/policy`。
- ✅ 图谱仍是 Nebula 协议。本单不写 nGQL，不读图。
- ✅ 可观测沿既有 Job 入口。未新造观测点，也未拆掉既有埋点。
- ✅ 已推 `origin/dev`，未 force。本单未查 Pipeline。
- ✅ 未把 demo 合并进 lumen。
- ✅ 未另造一套展示直连 Python 的路径。
- ✅ 焦点与摘要都读已有 ADS。无行则空，不在接口里返回写死指数或段落。
- ✅ D8：本单无页面。
- ✅ D9：不改 D4，不新造 `metric_id`。`M_POLICY_FOCUS_INDEX` 与 `M_POLICY_DS_11_POLICY_EVAL_012` 仍是读面身份。
- ✅ D10：本单无交互页。
- ✅ D12：改动在 `lumen-algo-py`。未调用 `demo-*` 服务。
- ✅ D14：未写对象存储，未新造桶。
- ✅ D16：未建 `gapfill_` 表，未改 `job.py` 以外去建缺项表。
- ✅ D17：未改 `focus.py`，未改锁定算法闭包，未复用锁定 URL 做另一套公式。
- ✅ D18：有表则查表。`policy_focus_ads` 先调用已有 `focus.run` 再查 `ads.policy_focus`。`policy_text_parse` 只查 `ads.policy_text_parse.summary`。无行则空。

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 20000 |
| model_used | grok-4.7 |
| actual_cost | 0.11 |
| cost_warn | green |
| user_story | US-DS-POL-05 |
