# POL-L2-DS12-JOBS-IMPL-JAVA · 政策效果推演 jobs

ponytail: full

## 任务认领

| 字段 | 值 |
|---|---|
| id | `POL-L2-DS12-JOBS-IMPL-JAVA` |
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| 说明 | 只写本地 commit。未 `git push`。不改 `task-registry.yaml`，不标 `done` / `ready_to_sign` |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 沿用展示侧 Feign 与 element `ElementDao.listOrEmpty`。不加依赖，不建第二套任务入口。未跳过调用链、空态和单测 |

## 路径

浏览器 `POST /display/v1/policy/simulation/jobs`。网关 `StripPrefix=1` 后，`gkxlumen-display` 映射是 `/v1/policy/simulation` + `POST /jobs`。展示侧不连库、不调 Python、不转发 `gkxlumen-topic-async-service`。只读走 `gkxlumen-element` `GET /v1/element/policy/simulation`（`@Inner`，Feign `@NoToken`）。

240 政策关联没有这条资源，也没有单独路径。请求体字段是 `kind` 与蛇形过滤项。单独的 `sub_type` 不会建任务。

## 种类对照

一次请求一种类。表空、无行、种类对不上、条件不齐：HTTP 成功，`records` 为空，不返回 501。查询异常走 `listOrEmpty`，同样空列表。不插入、不更新、不删除。

| 请求 `kind` | 表 | `row_kind` / 条件 | 顺序 |
|---|---|---|---|
| 未出台仿真 | `{gapfill}.gapfill_policy_sim_forecast` | `未出台仿真`。`policy_type`、`coverage_scope`、`support_intensity`、`implement_time` 至少给一个；给了才等值过滤。四个都空则不扫全表 | `id` |
| 新出台预测 | 同上 | `新出台预测`。必须有 `policy_id` | `id` |
| 区域空间 | 同上 | `区域空间`。必须有 `region_name`；`policy_type` 只在传入时过滤。不补全国行 | `id` |
| 多维评估 | `{gapfill}.gapfill_policy_sim_result` | `多维评估`。不按政策过滤 | 经济、社会、环境、创新，再按 `id` |
| 利益攸关方 | `{gapfill}.gapfill_policy_sim_stakeholder` | 行种类是 `参与意见`。请求种类不是「参与意见」。无 `policy_id` 列。列含 `actor_role`、`channel_name`、`opinion_text`、`opinion_at` | `opinion_at`，再 `id` |
| 文本解析 | `{ads}.policy_text_parse` | 按 `policy_id`。返回 `title`、`summary`、`auto_tags`、`structured_elements`。去掉 JSON 里的 `clauses`、`clause_meta`，行仍返回。不查不存在的 `metric_id`。不调 `polan.text.parse.run`，不走 `parse/jobs` | `id` |
| 重点可视化 | result | `重点`。必须有 `policy_id` | 政策目标、支持领域、实施路径、资金安排，再按 `id` |
| 影响范围 | result | `影响范围`。必须有 `policy_id` | `id` |
| 路径预测 | result | `路径环节`。必须有 `policy_id` | 政策发布、申报受理、评审评估、资金拨付、效果评估，再按 `id` |
| 解读报告 | result | `解读段落`。必须有 `policy_id`。只回 `section_name` / `body_text` 等结果列，不含文件列 | 政策背景、主要内容、预期效果、实施建议，再按 `id` |
| 政策关联、参与意见，以及其他未知种类 | 不查表 | `records` 为空 | — |

`{gapfill}`、`{ads}` 仍由 element 配置替换，不写死 `gkxlumenx_ads`。

## 修改内容

仓 `lumen-svc-platform`，分支 `dev`。

| commit | 说明 |
|---|---|
| `78aab79a6cf7165f1afdb2a889f6c6d12a2c325e` | 唯一公开入口 `POST /display/v1/policy/simulation/jobs` |

- `gkxlumen-display`：`PolicySimulationController`、`PolicySimulationService`；`RemoteElementClient.policySimulation`
- `gkxlumen-element`：`PolicySimulationReadController`
- 未改 `PolicyEvaluationService.JOB_SUB_TYPES`，未改 `PolicyAnalysisTypes`

## 测试结果

Maven 3.9.9，JDK 为 JetBrains JBR 21。`-Dmaven.build.cache.enabled=false`。

```
mvn -pl gkxlumen-element,gkxlumen-display -Dtest=PolicySimulationReadControllerTest,PolicySimulationServiceTest -DfailIfNoTests=false -Dmaven.build.cache.enabled=false test
```

| 测试类 | 结果 |
|---|---|
| `PolicySimulationServiceTest` | 3 tests，0 failures |
| `PolicySimulationReadControllerTest` | 5 tests，0 failures |

`BUILD SUCCESS`。覆盖：未知种类（含请求种类「参与意见」和「政策关联」）不查预估表；未出台四个参数都空不扫全表；文本解析去掉条款键但保留该行；利益攸关方读 stakeholder 且绑定 `参与意见`；解读报告只读段落正文；展示侧只有 `POST /jobs`；读失败仍是成功空列表。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ Java 只读表，不跑解析或仿真 |
| 调用链 前端 → Java REST → Python `/internal/*` | ✅ 本接口是同步读表，display 只 Feign element，不越层调 Python |
| 图谱 Nebula，Java 不写 nGQL | ✅ 无图查询 |
| 可观测 | ✅ 落在已有 display / element 进程 |
| CI/CD | 未推送。本会话没有 pipeline |
| demo 不 merge 进 lumen | ✅ 只改 `lumen-svc-platform` |
| 前端只调 Java | ✅ 公开入口只有 display jobs |
| 读 ADS，缺项走 gapfill | ✅ 文本解析读 `{ads}.policy_text_parse`；其余读 gapfill 三张表 |
| D9 | ✅ 不新造 `metric_id`，不改 D4。无行是空列表 |
| D12 不调 demo-* | ✅ Feign 名称为 `gkxlumen-element` |
| D16 | ✅ 只读 gapfill，不插入 |
| D18 | ✅ 不在接口里写死 mock 行 |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 40000 |
| model_used | grok-4.7 |
| actual_cost | 0.20 |
| cost_warn | green |

## 遗留

- 表未建或无行时接口返回空列表。本单不建表、不灌数。

## 总控推送

2026-11-06 三仓都落地后推 `lumen-svc-platform` `origin/dev`。提交 `78aab79a6cf7165f1afdb2a889f6c6d12a2c325e` 已在远端。
