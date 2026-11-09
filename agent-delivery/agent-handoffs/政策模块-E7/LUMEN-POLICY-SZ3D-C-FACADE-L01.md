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
| `cards.effect` | 原样，`computable=false` 与 `reason`；`ext` 原样透传（见下「落地实效宏观代理 ext」，POL-EFFECT-MACRO-JAVA-L01） | `frozen_cards.effect`：`computable`、`reason`；可算时加 `score`；有 `ext` 时加 `ext` 口径子集。章节：可算印「分数」，否则「不可算」，宏观代理再附口径句与 `proxy_notes` |
| `strategies[]` | `id` / `title` / `dimension` / `priority` / `conclusion` 不改 | `report_chapters`「优化建议」用同一 `conclusion` |
| `narration` / `honesty` | 原样，不二次润色 | — |
| 顶层 `composite` / `selected_indicators` / `weights` | 删除 | 输入快照同样删除 |
| Python `result_snapshot_id` | 不写入响应 | Java 另签 `result_snapshot_id=res-{taskId}` |
| `indicators?kind=all` 的 `items` | 删除 | 分布五段保留 |

## 落地实效宏观代理 ext（POL-EFFECT-MACRO-JAVA-L01 补，契约说明）

`result_payload.cards.effect` 由 Python 产出，Java **整块原样透传，不改分、不补键、不写 0**。`ext` 键定义真源 = `POL-EFFECT-MACRO-ALGO-L01.md`：

| 键 | 说明 | 冻结进 `frozen_cards.effect.ext` |
|----|------|:--:|
| `caliber` | `macro_outcome_proxy`（宏观结果面代理，**不是**正本三维） | ✅ |
| `whitelist_version` | 如 `macro-eff-v1` | ✅ |
| `window` / `dim` | 期次窗口 / 维度说明 | ✅ |
| `indicator_count` / `indicator_used` | 参与指标数与清单 | ✅ |
| `period_used` | 每城每指标实际取用期次（各城不对齐，**不得宣称同期**） | ✅ |
| `source_tables` | 实际读取的源表 | ✅ |
| `proxy_notes` | 剔除/期次不齐等诚实说明（字符串数组） | ✅ |
| `track_a_status` / `track_a_*` | 正本三维诊断，只作诊断，不混入分数 | `track_a_status` ✅，其余只在结果板 |
| `city_scores` / `area_key` | 四城对比分 / 区划键 | ❌（体积大，仅结果板） |

空值规则：
- `computable=false`：无 `score` 键或 `score=null`；`frozen_cards.effect` 不写 `score`；章节「落地实效」= 「不可算」+ `reason`，**不印 0**。
- `computable=true`：`score` 为 Python 原值。最低城截面分可为**真 0**，章节照印「分数 0」（旧逻辑把 0 当不可算，已改为只看 `computable` + 数值性）。
- `ext` 缺失（旧 Python / 正本三维路径）：行为与改动前一致。
- 带 `caliber=macro_outcome_proxy` 时，章节与 `policy:report:export` 的「落地实效性」块追加「口径 宏观结果面代理（待甲方确认）」与每条 `proxy_notes`。FE 角标语义（⚠️ 待甲方确认）仍归 D 段。

样例（`result_payload.cards.effect`）：

```json
{"metric_id":"M_POLICY_IMPLEMENTATION_EFFECT","computable":true,"score":78.5836,
 "ext":{"caliber":"macro_outcome_proxy","whitelist_version":"macro-eff-v1","window":"202101~各城最新",
  "indicator_count":7,"period_used":{"深圳":{"gmjj_gnmy_01":202509}},"source_tables":["gkx.dwd_macro_index_data"],
  "city_scores":{"深圳":78.5836,"广州":41.1010,"北京":48.5023,"上海":30.3062},
  "proxy_notes":["各城最新期次不对齐，非同期比较"],"track_a_status":"not_computable"}}
```

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
