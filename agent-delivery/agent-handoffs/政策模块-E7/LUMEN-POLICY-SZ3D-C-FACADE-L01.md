# LUMEN-POLICY-SZ3D-C-FACADE-L01 · 深圳政策现状 Java 透传

> 设计：`05.6.2-深圳政策现状分析.md`，总控，B 叶 handoff 字段样例。只改 Java。未改前端，未领 D/E。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 编码中途会话中断，本会话补跑测试、提交并推送。任务未改 done。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用时序任务的快照签发路径。新增一个透传类，不加依赖。Java 不写分数、不调模型。 |

## 修改内容

- `policy_shenzhen` / `policy_sz_3d` / `policy:recommendation:policy_sz_3d` 成功回包时，`result_payload` 保存 Python 结果板。信封上的 `harness_mode` / `sub_type` / `shards` 若结果板没有，补进同一份 payload。
- 顶层 `composite`、`selected_indicators`、`weights`（34/33/33）从响应和输入快照去掉。卡内 `cards.support.weights`（0.5/0.5，`pending_ref=QPOL-02`）保留。
- `frozen_cards` 只冻三张卡的可算状态：支持力度另冻条数、层级均值、档位。档位 `value` 保持 null，不写成 0。
- `strategies[].conclusion` 原样保存。报告第 5 章用同一句。无卡时章节为「本结果没有可写的优化建议」。
- 报告六章写在快照 `report_chapters`，模板号 `POL-SZ-3D-PDF-v1`。没有报告渲染器，Java 不调模型。null 印成「—」或「不可算」。
- `GET indicators?kind=all` 仍透传 level/type/timeseries/national/sz。若 Python 带回 `items`，删掉，不组装二级目录。
- Java 快照号仍是 `res-{taskId}`，`viewed=false`，`totalNodes=1`。不用 Python 的 `result_snapshot_id`。

## 字段表

| Python 键 | Java `result_payload` | 快照额外字段 |
|-----------|----------------------|--------------|
| `harness_mode` / `sub_type` / `shards` / `mode` | 原样 | — |
| `cards.support` 分数、名次、条数、层级均值、`tier`、`notes`、卡内 `weights` | 原样，`tier.value` 保持 null | `frozen_cards.support`：`computable`、`policy_count`、`level_mean`、`tier` |
| `cards.fit` | 原样，无命中则 `score` 保持 null | `frozen_cards.fit`：`computable`、`score`、`hit_count` |
| `cards.effect` | 原样，`computable=false` 与 `reason` | `frozen_cards.effect`：`computable`、`reason`。章节只写「不可算」 |
| `strategies[]` | `id` / `title` / `dimension` / `priority` / `conclusion` 不改 | `report_chapters`「优化建议」用同一 `conclusion` |
| `narration` / `honesty` | 原样，不二次润色 | — |
| 顶层 `composite` / `selected_indicators` / `weights` | 删除 | 输入快照同样删除 |
| Python `result_snapshot_id` | 不写入响应 | Java 另签 `result_snapshot_id=res-{taskId}` |
| `indicators?kind=all` 的 `items` | 删除 | 分布五段保留 |

## 测试结果

在 `lumen-svc-platform`，Maven 3.9.9，关闭构建缓存：

```text
mvn -pl gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz,gkxlumen-topic-policy/gkxlumen-topic-policy-biz -am test "-Dtest=PolicyShenzhenSnapshotTest,PolicyAnalysisTypesTest,AnalysisTaskServiceImplPolicyJobTest,PolicyFacadeServiceImplTest" "-Dsurefire.failIfNoSpecifiedTests=false" "-Dmaven.build.cache.enabled=false"
```

- `gkxlumen-topic-async-service-biz`：13 passed（含政策任务 7、类型 4、深圳快照 2）
- `gkxlumen-topic-policy-biz`：`PolicyFacadeServiceImplTest` 26 passed

覆盖：档位不是 0、无综合分、结论不改、无建议卡用规则句、`kind=all` 去掉 `items` 且保留分布。

## CI/CD

- 分支：`lumen-svc-platform` `origin/dev`
- commit：`982e038d0893b4da3dd55c3b87141e9ddaf10353`
- 部署：本叶不点部署

## 遗留

- 未连真库，未点发布。前端三张卡、发布和 QA 不在本叶。
- 任务保持联调前状态由 coordinator 推进。本 handoff 不写「联调通过」。

## 涉及文件

- `repos/lumen-svc-platform/gkxlumen-topic-async-service/.../PolicyShenzhenSnapshot.java`
- `repos/lumen-svc-platform/gkxlumen-topic-async-service/.../AnalysisTaskServiceImpl.java`
- `repos/lumen-svc-platform/gkxlumen-topic-async-service/.../PolicyAnalysisTypes.java`
- `repos/lumen-svc-platform/gkxlumen-topic-policy/.../PolicyFacadeServiceImpl.java`
- 对应三份测试

## 架构合规

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ Java 只透传 |
| 前端 → Java → `/internal/*` | ✅ |
| 不把 null 档位写成 0、不补综合分 | ✅ |
| 不调模型、不改 `conclusion` | ✅ |
| 快照由 Java 签发 | ✅ |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 60000 |
| model_used | grok-4.7 |
| actual_cost | 0.12 |
| cost_warn | green |
| 说明 | source: session_estimate。沿用 B 叶 60000 token ≈ $0.12。无 Console 的 in/out 分离值。 |
