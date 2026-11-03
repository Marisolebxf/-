# POL-L2-DS10-SENT-IMPL-JAVA · 科创政策全景 · 政策舆情评估 · 展示与缺项读面

ponytail: full

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时已是 `in_progress`。本单不改 `task-registry.yaml`，不标 done |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 沿用 display 已有 Feign 与 element 已有 JdbcTemplate。不新加 Maven 依赖。未跳过调用链、空态和单测 |

## 范围

科创政策全景 · 政策舆情评估。SRS 207–212。用户故事 `US-DS-POL-03`。

浏览器只打 `/display/v1/policy/panorama/**`（网关 StripPrefix=1 后服务内是 `/v1/policy/panorama/**`）。未改 `gkxlumen-topic-policy`。Java 不写算法、不写 nGQL、不调 `demo-*`、不直连 Python。

| 公开资源 | 实现 |
|---|---|
| `POST /display/v1/policy/panorama/jobs` | display → `gkxlumen-topic-async-service` `POST /topic/v1/analysis/tasks`。只接受 `policy_effect`、`policy_match`。其它 sub_type 不建任务 |
| `GET .../stats` | display → topic-policy `metrics`，再取 `indicators`。无数据为空对象，不补 0 |
| `GET .../search` | display → topic-policy `search`。查询参数原样转发 |
| `GET .../{id}/detail` | display → topic-policy `docs/{id}`。不走 `/{id}` 兜底 |
| `GET .../feedback` | display → element 只读 `gkxlumenx_gapfill.gapfill_policy_audience_feedback` |
| `GET .../assessment-report` | display → element 只读 `gkxlumenx_gapfill.gapfill_policy_assessment_report` |
| 208 | 未新开资源 |

切条件不会建 job：只有 `POST jobs` 调异步创建。Job 失败只返回任务错误，不调用、不清空 stats / search / detail。

`policy_effect`、`policy_match` 已进入 `PolicyAnalysisTypes.CANONICAL`。这两个跳过产业 VID XOR；时序、区域、深圳、焦点仍走原校验。未注册 `policy_shard`。

缺项表未建或没有行时 `records` 为空列表。GET 不建表、不插入、不写死 mock。`score` 保持空，不用 0 占位。

## 修改内容

仓 `lumen-svc-platform`，commit `6e7f7f4934817d07345d57a4d103b9f38cbca63d`，已推 `origin/dev`。

- `gkxlumen-display`：`PolicyPanoramaController`、`PolicyPanoramaService`、`RemoteTopicPolicyClient`、`RemoteTopicAsyncClient`，并在 `RemoteElementClient` 增加两条只读
- `gkxlumen-element`：`PolicyGapfillController`；`ElementDao.listOrEmpty` 读 `{gapfill}`，失败返回空列表；`application.yml` 增加 `gkxlumen.element.gapfill-db`
- `gkxlumen-topic-async-service`：`PolicyAnalysisTypes`、`PolicyAnalysisAdapterImpl`、`PolicyAnalysisTypesTest`

## 测试结果

未跑全仓 `mvn`。JDK 17.0.16，Maven 3.9.9，`-Dmaven.build.cache.enabled=false`。

| 模块 | 命令焦点 | 结果 |
|---|---|---|
| topic-async-service-biz | `PolicyAnalysisTypesTest` + `PolicyAnalysisAdapterImplTest` | 13 tests，0 failures |
| gkxlumen-element | `ElementDaoGapfillTest` + `EnterprisePointsAssemblerTest` | 8 tests，0 failures |
| gkxlumen-display | `PolicyPanoramaServiceTest` | 2 tests，0 failures |

`ElementDaoGapfillTest` 断言：表不可读时 SQL 已落到 `gkxlumenx_gapfill`，返回空列表；`score` 为 null 时不改成 0。

## 架构合规

| 铁律 | 结果 |
|---|---|
| 调用链 前端 → Java → Python `/internal/*` | jobs 经 topic-async 已有 `PolicyAnalysisAdapterImpl`。display 不直连 Python |
| 不改 topic-policy | 未改该模块任何文件 |
| Java 不写算法、不写 nGQL、不调 demo-* | 是 |
| 无行不造 0、不返回 501 | 读面失败或无行是空对象 / 空列表 |
| D12 | display 只调 `gkxlumen-topic-policy-biz`、`gkxlumen-topic-async-service-biz`、`gkxlumen-element` |
| D9 / D4 | 本单不改指标、不把 mock 写成已上线 |

## CI/CD

- 分支：`dev`
- commit：`6e7f7f4934817d07345d57a4d103b9f38cbca63d`
- push：`origin/dev` 成功（`e443c41..6e7f7f4`）。未 force
- pipeline：本会话未查 GitLab pipeline 页面
- K8s rollout：未在本会话确认

## 遗留

- 政策 Job 仍走已有指纹门：请求里没有合法 `analysis_fp` 时，异步服务拒绝创建，display 不补指纹。
- Java 白名单收规范名 `policy_effect`、`policy_match`。未加 Python 别名 `policy:effect`、`policy:match`。展示入口只转发这两个规范名。
- 缺项表的建表和灌数仍在 `POL-L2-DS10-SENT-MOCK-210` / `211`。表未建时接口是空列表。
- 208 没有新资源。本单不把第 7 项子图接到新路径。
- 成本未单独计量。不标 done。
