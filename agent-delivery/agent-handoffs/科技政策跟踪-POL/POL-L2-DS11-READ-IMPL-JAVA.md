# POL-L2-DS11-READ-IMPL-JAVA · 政策分析评价 · 结果解读报告多维展示 · 展示读面

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 从 ready 认领。本单不把任务标 done |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 展示只转发到已有 element 与 topic-async。未直连 Python，未直连库，未新造前端页 |

## 范围与实现

浏览器只打 `/display/v1/policy/evaluation/**`。

- `GET /counts`：display 调 element，只读 `{ads}.policy_effect` 且 `scope_type=region_gap` 的 `shortboard_cnt`。无行则 `records` 空，不造 0，不调用 `gap.run`，不读机遇
- `GET /shells`：element 只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。无表或无行则空列表。不返回视频、动画、PDF、模板字节。GET 不插入
- `POST /jobs`：display 委托 `POST /topic/v1/analysis/tasks`。白名单增加 `policy_focus_ads`、`policy_text_parse`，这两个不走产业 VID XOR、不收 items。既有 `policy_focus` 仍走 harness。`policy_effect`、`policy_match`、`policy_intensity` 仍可转发

## 偏离

| 偏离 | 理由 | as-built |
|------|------|----------|
| 合并远端时白名单已有 `policy_intensity` | 力度是别的叶子已放行的转发键 | 保留力度，并加上焦点与摘要两个读表键 |

## 产物清单

- `gkxlumen-display` `PolicyEvaluationController` / `PolicyEvaluationService`
- `gkxlumen-element` `PolicyGapfillController` 的 counts、shells
- `PolicyAnalysisTypes` 与 `PolicyAnalysisAdapterImpl` 的两个新键
- 本 handoff

## 验收证据

`mvn -pl gkxlumen-display,gkxlumen-element,gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz -am -Dtest=PolicyAnalysisTypesTest,PolicyAnalysisAdapterImplTest,PolicyGapfillEvaluationTest,PolicyEvaluationServiceTest test`

2026-11-03 结果：`PolicyAnalysisAdapterImplTest` 11、`PolicyAnalysisTypesTest` 4、`PolicyEvaluationServiceTest` 7、`PolicyGapfillEvaluationTest` 1，全部通过。BUILD SUCCESS。

## 架构合规自检

- ✅ 调用链：浏览器 → display `/display/v1/policy/**` → element 只读，或 → topic-async → Python `/internal/policy/jobs/execute`。Java 不算分
- ✅ 未把浏览器指到 `/v1/policy`，未调用 demo 服务
- ✅ 图谱：未写 nGQL
- ✅ 可观测：沿既有 Feign 与任务入口，未拆埋点
- ✅ D8 / D10：本单无页面
- ✅ D9：不改 D4，不新造 `metric_id`
- ✅ D12：改动在 `lumen-svc-platform`
- ✅ D14：不写对象存储，shells 不返回媒体字节
- ✅ D16：shells 只读已有 `gapfill_policy_eval_shell`，GET 不插入
- ✅ D17：未改锁定算法闭包
- ✅ D18：有表则查表。无行则空，接口不返回写死 mock

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 30000 |
| model_used | grok-4.7 |
| actual_cost | 0.16 |
| cost_warn | green |
| user_story | US-DS-POL-05 |

## CI/CD

- 分支：`lumen-svc-platform` 的 `dev`
- commit：`490071b` 读面，`814d8df` 合并远端并保留力度，`30a3192` 评价任务白名单补回 `policy_intensity`
- pipeline：本单推 `origin/dev` 后未查 Pipeline
- 部署：未单独 rollout

## 未做的事

- 未做展示页，未标 done
- 未联调线上库。单测用桩
