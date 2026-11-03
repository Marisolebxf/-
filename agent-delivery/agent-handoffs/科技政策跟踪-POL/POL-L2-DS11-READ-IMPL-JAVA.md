# POL-L2-DS11-READ-IMPL-JAVA · 政策分析评价 · 结果解读读面

ponytail: full

## 任务认领

| 字段 | 值 |
|---|---|
| id | `POL-L2-DS11-READ-IMPL-JAVA` |
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| lock_hours | 24 |
| user_story | `US-DS-POL-05` |
| 开工状态 | 认领时为 `ready`，随后改为 `in_progress` |
| 说明 | 不改 `task-registry.yaml`。不标 `done` / `ready_to_sign` |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 沿用全景控制器的 Feign 与 element 已有 `JdbcTemplate`。不加 Maven 依赖。未跳过调用链、空态和单测 |

## 范围

设计只读：`sdd/l2/POL-L2-DS11-READ-API.md`、`POL-L2-DS11-READ-ARCH.md`、`POL-L2-DS11-READ-DATA.md`。未改 VIZ、PLAN、WBS。

浏览器打 `/display/v1/policy/evaluation/**`。网关 `StripPrefix=1` 后，`gkxlumen-display` 内路径是 `/v1/policy/evaluation/**`，与全景控制器同一习惯。

| 公开资源 | 实现 |
|---|---|
| `GET /display/v1/policy/evaluation/counts` | display → `gkxlumen-element`。只读 `{ads}.policy_effect`，`scope_type=region_gap`，列 `shortboard_cnt`。无行则 `records` 为空，不造 0，不调用 `gap.run`。页上没有机遇读面，本单不新造 |
| `GET /display/v1/policy/evaluation/shells` | element 只读 `{gapfill}.gapfill_policy_eval_shell`。表不存在或无行返回空列表。不插入，不写死句子。不返回视频、动画、PDF、模板字节 |
| `POST /display/v1/policy/evaluation/jobs` | display → `gkxlumen-topic-async-service` 已有 `POST /topic/v1/analysis/tasks`。白名单在既有政策键上增加 `policy_focus_ads`、`policy_text_parse`。这两个跳过产业 VID XOR，不要求 `items`。`policy_focus` 的 items / 产业 / 正文校验和 harness 路径保持原样。`policy_effect`、`policy_match` 仍在，且不改成必须带 `items`。本资源没有收成只接受这两个新键。合并远端时保留已有的 `policy_intensity` |

切条件不建任务：只有 `POST jobs` 调异步创建。Job 失败只返回任务错误，随后再读 counts、shells 仍走各自的只读，不会被这次失败清空。

Java 不写算法、不写 nGQL、不调 `demo-*`、不直连 Python。展示侧不补 `analysis_fp`，不补 `items`。

## 修改内容

仓 `lumen-svc-platform`，分支 `dev`，已在 `origin/dev`。未 force。

| commit | 说明 |
|---|---|
| `490071b3b201d6887564706a5a6a4a0844345af5` | 接上 counts、shells、jobs，白名单增加两个读表键 |
| `814d8dfab3dbe5ceac8c400bea84ba149b885001` | `git pull --no-rebase` 合入远端。保留 `policy_intensity` 与比对读面，同时留下本单的评价读面 |
| `30a3192bbe12faa557ff394e8713f9b536204fda` | 评价 jobs 继续放行已有的 `policy_intensity` |

- `gkxlumen-display`：`PolicyEvaluationController`、`PolicyEvaluationService`、`RemoteElementClient` 两条只读。jobs 复用 `RemoteTopicAsyncClient.create`
- `gkxlumen-element`：`PolicyGapfillController` 增加 `GET /evaluation/counts`、`GET /evaluation/shells`。沿用 `ElementDao.listOrEmpty`
- `gkxlumen-topic-async-service`：`PolicyAnalysisTypes` 增加 `policy_focus_ads`、`policy_text_parse`，并保留远端的 `policy_intensity`。`skipsIndustryVidXor` 对效果、匹配、力度、展示焦点、摘要为真。`policy_focus` 不跳过

规范键共九个：时序、区域、深圳、焦点、效果、匹配、力度、展示焦点、摘要。

## 测试结果

未跑全仓 `mvn`。Maven 3.9.9，JDK 为 JetBrains JBR 21（编译目标仍是 release 17）。`-Dmaven.build.cache.enabled=false`。

```
mvn -pl gkxlumen-display,gkxlumen-element,gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz -am -Dtest=PolicyAnalysisTypesTest,PolicyAnalysisAdapterImplTest,PolicyEvaluationServiceTest,PolicyGapfillEvaluationTest,PolicyGapfillControllerTest test
```

| 测试类 | 结果 |
|---|---|
| `PolicyAnalysisTypesTest` | 4 tests，0 failures |
| `PolicyAnalysisAdapterImplTest` | 11 tests，0 failures |
| `PolicyEvaluationServiceTest` | 7 tests，0 failures |
| `PolicyGapfillEvaluationTest` | 1 test，0 failures |
| `PolicyGapfillControllerTest` | 6 tests，0 failures |

`BUILD SUCCESS`。评价单测覆盖：空计数不变成 0、响应里没有机遇字段、读面不调异步创建、未知 `sub_type` 不建任务、任务失败后 counts / shells 仍可再读、两个新键不要求 items、既有焦点仍走 items / harness。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ Java 只做白名单与转发，不写 `focus.run` / `parse.run` |
| 调用链 前端 → Java REST → Python `/internal/*` | ✅ jobs 经 topic-async 已有适配器。counts / shells 只到 element |
| 图谱 Nebula，Java 不写 nGQL | ✅ 本单无图查询 |
| 可观测 | ✅ 新接口落在已有 display / element / topic-async 进程，未绕开 Java Agent |
| CI/CD | ✅ 已推 `origin/dev`，未 force。本会话未打开 pipeline 页面 |
| demo 不 merge 进 lumen | ✅ 只改 `lumen-svc-platform` |
| 前端只调 Java，Java 不直连算法库 | ✅ display 只 Feign `gkxlumen-element` 与 `gkxlumen-topic-async-service` |
| 读 ADS，缺项走 gapfill | ✅ counts 读 `ads.policy_effect`；shells 只读 `gkxlumenx_gapfill` |
| D8 前端规范 | ✅ 本单无页面 |
| D9 指标与空态 | ✅ 不新造 `metric_id`，无行不造 0，不把 mock 写成已上线 |
| D10 交互规范 | ✅ 本单无交互页。切条件不建任务 |
| D12 不调 demo-* | ✅ Feign 名称为 `gkxlumen-*` |
| D14 对象存储 | ✅ 不写桶，不返回模板或 PDF 字节 |
| D16 gapfill | ✅ 只读 `gapfill_policy_eval_shell`，不插入，不写 ODS / DWD / ADS |
| D17 合规算法闭包 | ✅ 未改锁定算法，未改合规展示名 |
| D18 不在接口写死 mock | ✅ 无行是空列表。Job 失败不清空 counts 和 shells |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 30000 |
| model_used | grok-4.7 |
| actual_cost | 0.16 |
| cost_warn | green |
| user_story | `US-DS-POL-05` |

## 遗留

- 异步创建仍要合法 `analysis_fp`。display 不补指纹。
- `policy_focus_ads`、`policy_text_parse` 的 Python 分支不在本单。若下游还不认识这两个键，任务失败，counts 与 shells 保持各自只读。
- 壳表未建时 shells 是空列表。本单不建表、不灌数。
