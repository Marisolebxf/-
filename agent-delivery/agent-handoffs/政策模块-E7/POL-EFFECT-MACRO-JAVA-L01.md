# POL-EFFECT-MACRO-JAVA-L01 · 落地实效宏观代理：Java 透传 cards.effect.ext

> 总控：[`POL-EFFECT-MACRO-长任务总控.md`](./POL-EFFECT-MACRO-长任务总控.md) §0.6 · 前序：[`POL-EFFECT-MACRO-ALGO-L01.md`](./POL-EFFECT-MACRO-ALGO-L01.md)（`cards.effect.ext` 键真源）· 契约：[`LUMEN-POLICY-SZ3D-C-FACADE-L01.md`](./LUMEN-POLICY-SZ3D-C-FACADE-L01.md)「落地实效宏观代理 ext」
> 日期：2026-11-09 · 类型：feature · Epic：`E-POLICY-PDR` · 故事：`US-E7-POL-04`

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 不新增类、不加依赖、不改 Python/前端。`businessResult` 本来就整块拷 `result`，`ext` 已能透传，只补确实丢信息的三处：快照冻结、章节、导出块。未跳过：诚实性（不写 0）、单测。`ponytail:` 上限：冻结键白名单写常量，Python 新增 ext 键需同步 `EFFECT_EXT_FROZEN_KEYS`（结果板本身不受影响，原样透传）。 |

## 范围与实现（对照 DoD）

| DoD | 实现 |
|---|---|
| 透传 `effect.ext`（caliber / whitelist_version / period_used / proxy_notes / track_a_* 等），Java 不改分、不写算法、不直连 gkx | `PolicyShenzhenSnapshot.businessResult` 整块拷 `result`，`cards.effect.ext` 原样进 `result_payload`（单测断言 `ext` 与输入 `equals`）。Java 未新增任何读库/算分逻辑。 |
| 快照冻结 | `frozen_cards.effect` 新增：可算时 `score`；有 `ext` 时 `ext` 口径子集（`caliber/whitelist_version/window/dim/indicator_count/indicator_used/period_used/source_tables/proxy_notes/track_a_status`）。`city_scores/area_key/track_a_score` 不冻（体积大，只在结果板）。 |
| 章节「落地实效」（快照 `report_chapters`） | 可算且 `score` 为数值 → 「分数 x」；否则「不可算」+ `reason`。宏观代理再附「口径 宏观结果面代理（待甲方确认）」与每条 `proxy_notes`。 |
| 导出块「落地实效性」（`PolicyBlockReportAssembler.shenzhen`） | 原先**硬编码「不可算」**，宏观代理上线后会与结果板矛盾；改为同一规则（可算印分，否则不可算）。 |
| 空实效不写 0 | 不可算：`frozen_cards.effect` 不写 `score` 键；章节不印分；`ext` 缺失时与改动前一致。**修了一处隐患**：旧 `realScore` 把 0 分当不可算，但宏观截面 min-max 下最低城的真分就是 0，旧逻辑会误印「不可算」；现在只看 `computable` + 数值性。 |
| OpenAPI/契约补字段说明 | 本仓无 `result_payload` 的 OpenAPI schema（`Map<String,Object>` 透传），契约真源在 `LUMEN-POLICY-SZ3D-C-FACADE-L01.md`，已增补「落地实效宏观代理 ext」章节（键表 + 空值规则 + 样例）与字段表 `cards.effect` 行。 |

## 偏离说明

- **未本地编译/跑 Maven**：本机无 JDK/Maven（PATH 与常见目录均未找到），测试未在本机执行，改动已逐行对照签名自查。须以 CI（`origin/dev` pipeline）为准，**若 CI 红由本叶修**。
- 未改 `AnalysisTaskServiceImpl`：入口 `isShenzhen → businessResult → freezeSnapshot` 无需改动。
- 未触达 D17 锁定闭包；`/internal/*` 路由与调用链不变。

## 样例 JSON（`result_payload.cards.effect`）

可算：

```json
{"metric_id":"M_POLICY_IMPLEMENTATION_EFFECT","computable":true,"score":78.5836,
 "ext":{"caliber":"macro_outcome_proxy","whitelist_version":"macro-eff-v1","window":"202101~各城最新",
  "indicator_count":7,"period_used":{"深圳":{"gmjj_gnmy_01":202509}},"source_tables":["gkx.dwd_macro_index_data"],
  "city_scores":{"深圳":78.5836,"广州":41.1010,"北京":48.5023,"上海":30.3062},
  "proxy_notes":["各城最新期次不对齐，非同期比较"],"track_a_status":"not_computable"}}
```

`frozen_cards.effect`（快照，同一任务）：

```json
{"computable":true,"reason":null,"score":78.5836,
 "ext":{"caliber":"macro_outcome_proxy","whitelist_version":"macro-eff-v1","window":"202101~各城最新",
  "indicator_count":7,"period_used":{"深圳":{"gmjj_gnmy_01":202509}},"source_tables":["gkx.dwd_macro_index_data"],
  "proxy_notes":["各城最新期次不对齐，非同期比较"],"track_a_status":"not_computable"}}
```

章节「落地实效」：`["分数 78.5836","口径 宏观结果面代理（待甲方确认）","各城最新期次不对齐，非同期比较"]`

宏观源不可达（不写 0）：

```json
{"metric_id":"M_POLICY_IMPLEMENTATION_EFFECT","computable":false,
 "reason":"宏观结果面代理暂不可用：宏观源不可达",
 "ext":{"caliber":"macro_outcome_proxy","whitelist_version":"macro-eff-v1","indicator_count":0,
  "proxy_notes":["宏观源读取失败：OperationalError"],"track_a_status":"not_computable"}}
```

章节：`["不可算","宏观结果面代理暂不可用：宏观源不可达","口径 宏观结果面代理（待甲方确认）","宏观源读取失败：OperationalError"]`；`frozen_cards.effect` 无 `score` 键。

## 测试结果

| 项 | 结果 |
|---|---|
| 新增 `PolicyShenzhenSnapshotTest.macroEffectExtPassesThroughAndFreezesCaliberWithoutInventingZero` | 已写（ext 原样透传 / 冻结子集不含 city_scores / 真 0 可印 / 不可算无 score 键与不印分）；**本机未跑**，待 CI |
| 新增 `PolicySvcReportModelTest.shenzhenReportPrintsMacroEffectScoreAndNotesButNotWhenUncomputable` | 同上 |
| 存量 `PolicyShenzhenSnapshotTest` / `AnalysisTaskServiceImplPolicyJobTest` | 断言「不可算」+reason 的路径行为不变（无 ext、score=0 且 `computable=false` 仍不可算），自查无回归；待 CI |

## 架构合规自检（00-team-constitution §2）

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ Java 只透传/冻结/拼文案，不算分 |
| 2 调用链 | ✅ 前端→Java→Python `/internal/*` 不变，Java 不直连 `gkx` |
| 3 Nebula | ✅ 不涉及 |
| 4 可观测 | ✅ 沿用既有任务链路与日志，无新增外部调用 |
| 5 CI/CD | ✅ push `origin/dev` |
| 6 demo2 只读 merge | ✅ 不涉及 |
| 7 共享聚合核心 | ✅ 不涉及 |
| 8 数据策略 | ✅ 不涉及，无落库 |
| 9 D8 | ✅ 未改前端 |
| 10 D9 | ✅ `metric_id` 不变；`whitelist_version/source_tables/caliber` 冻结供追溯；⚠️ 待确认角标语义交 D 段 |
| 11 D10 | ✅ 无交互改动 |
| 12 D12 | ✅ 不调用 demo-* |
| 13 D14 | ✅ 不涉及 |
| 14 D16 | ✅ 不写 gapfill |
| 15 D17 | ✅ 未触达锁定闭包 |
| 16 D18 | ✅ 无写死 mock |

## CI/CD

- 分支：`origin/dev`；commit：`lumen-svc-platform` `925df28`
- pipeline / K8s：随 push 触发，**未等待结果**；E0 由后续叶点名

## 涉及文件

- `lumen-svc-platform/.../support/analysis/PolicyShenzhenSnapshot.java`
- `lumen-svc-platform/.../service/impl/artifact/PolicyBlockReportAssembler.java`
- `lumen-svc-platform/.../test/.../PolicyShenzhenSnapshotTest.java`、`PolicySvcReportModelTest.java`
- `gkx-orchestration/.../LUMEN-POLICY-SZ3D-C-FACADE-L01.md`（契约增补）

## 下游放行建议

- **`POL-EFFECT-MACRO-FE-TOPIC-L01`（D）可开**，前提：CI 绿。FE 注意：
  - 读 `cards.effect.computable/score/reason/ext`；`score=0` 且 `computable=true` 是真 0，不要当空态；`computable=false` 不显示分。
  - `ext.caliber=macro_outcome_proxy` 须带 ⚠️「待甲方确认」；`period_used` 各城不对齐，不得写「同期」；展示 `proxy_notes`。
  - `city_scores` 只在结果板（`result_payload`），冻结快照里没有，对比城市用结果板读。
- E0 须 devops 确认 `lumen-algo-py` 可达 `gkx` 三方库（见 ALGO 遗留风险），否则金路径只会出现「宏观源不可达」空态。

## 问题清单 / 遗留风险

- 本机无 JDK/Maven，单测未本地执行；CI 为准。
- `EFFECT_EXT_FROZEN_KEYS` 为白名单，Python 将来新增 ext 键如需冻结需同步。
- 宏观源 20,000 行样本、各城期次不齐，跨城可比性有限（ALGO 已写 `proxy_notes`）。

## 成本（回填 registry）

| 字段 | 值 |
|---|---|
| actual_tokens | 约 90000 |
| model_used | claude-sonnet-5.5 |
| actual_cost | 0.6 |
| cost_warn | green |
