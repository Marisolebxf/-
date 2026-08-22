# METRIC-ID-ASSIGN-L01 · OPEN TEMP_* 赋正式 metric_id

> 定义任务。公式 / `algorithm_type` **未签**（`human:唐绍祖`，8/25 前不派本包）。本叶 **不写 seed**。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 口径 / 8 件套身份 / 适用性主责。Wave A+B 叶级智能体合流后由本父单收口。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶为 YAML 赋号草稿合流，未走 Headroom。 |

## 范围与实现

对照 loop：`agent-handoffs/算法库联调-ALGO-LIB/METRIC-ID-ASSIGN-LOOP-循环工程.md`；状态 `METRIC-ID-ASSIGN-LOOP-state.yaml` `current: complete`。

| Wave | 叶 | 结果 |
|------|----|------|
| A | 专题 ENT/TECH/ORG/TALENT/QUERY + DS-01…05 | 赋号草稿齐 |
| B | DS-06…09 + ZHIKU 非红 | 赋号草稿齐 |
| Skip | SVCCHAIN | 已是 `M_SVC_*`，不重赋 |

条目 **192**（含 ZHIKU 25 非红 `ZHIKU-S*` + 四枚 demo_lock）。Question **84** 条（Q072–Q155，全 🟡，已对照客户决策清单 §2.aj）。算法轨包：`metrics/request/_work/METRIC-ID-ASSIGN-handoff-to-algo.md`。

`TEMP_*` 不再当页面终态：叶级 `id-assign/{TASK_ID}.yaml` + 核对记录 §赋号表 + 机器卡 `demands` 已换正式草稿 `M_*`（或 reuse）。

## DoD 对照

| 项 | 结果 |
|----|------|
| 含 TEMP_* 的 OPEN 叶均有正式 M_* 或 reuse 对照表 | ✅ 叶级 yaml + §赋号表 |
| 每条带 algorithm_type_suggested（unsigned） | ✅ `suggested_unsigned`；未写入 seed |
| 歧义口径进 METRIC-SEMANTIC-QUESTIONS.md 为黄 | ✅ 84 条，不升 🟢 |
| 不写 seed 口径/公式/源表 | ✅ 本叶未改 `metrics/registry/` |
| 汇编算法轨交接清单 | ✅ `METRIC-ID-ASSIGN-handoff-to-algo.md` |
| TEMP_* 不再当页面终态 | ✅ 身份草稿已是 `M_*` / reuse / `ZHIKU-S*` |

## 偏离说明

- 类型与公式仍未签：本叶 DoD 允许；交给 `ALGO-LIB-SEED-TYPE-L01`（须 A1 会签后）与唐绍祖 A1 窗口。
- ZHIKU 非红保持 `ZHIKU-S*` 前缀，禁止发明 `M_ZHIKU_*`；四枚 🔴 不转正。
- 身份注册进 seed **不在本叶**：`METRIC-SEED-REGISTER-L01`。

## 产物清单

- `metrics/request/_work/id-assign/*.yaml`（15 叶；SVCCHAIN skip）
- `metrics/request/_work/METRIC-SEMANTIC-QUESTIONS.md`
- `metrics/request/_work/METRIC-ID-ASSIGN-handoff-to-algo.md`
- `metrics/request/_work/METRIC-ID-ASSIGN-LOOP-state.yaml`
- 本 handoff

## 验收证据

- Loop `current: complete`；父单 note 已记 Wave A+B 齐。
- CI/CD：定义资产，`cicd: skip`。
- 未改业务仓代码。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 本叶不写算法 |
| 2 调用链 前端→Java→Python `/internal/*` | ✅ 不越层 |
| 3 图谱 NebulaGraph | ✅ 不引入 Neo4j |
| 4 可观测性 | N/A 无运行时 |
| 5 CI/CD | ✅ 定义叶 skip |
| 6 demo2 只读 merge | ✅ 不 merge lumen |
| 7 共享聚合核心 | ✅ 前端不直连算法 |
| 8 数据策略 ADS / Mock | ✅ 不伪 D1=aligned |
| 9 D8 Design | N/A 无 UI |
| 10 D9 8 件套 | ✅ 只赋身份草稿；类型 `UNKNOWN`/未签；不标 aligned |
| 11 D10 交互 | N/A |
| 12 D12 demo/lumen 隔离 | ✅ 不调 demo 服务 |

## 会签

| 角色 | 结论 |
|------|------|
| 语义 Owner `human:淮政玮` | **会签通过**：赋号草稿收口，TEMP 非终态，不写 seed |
| 公式 / 类型 `human:唐绍祖` | 不在本叶；8/25 前优先 A1 |

## 遗留风险

- 建议类型不得当作已签。
- A2 库 missing 不因有号改 mapped。
- OPEN 16 叶仍 `integration`，本父单签收不等于 OPEN 会签完成。

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 95000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.2 |
| cost_warn | green |

## CI/CD（必填）

- 分支：`dev`（编排仓）
- commit：本 handoff 随编排仓提交（若本会话提交）
- pipeline URL / ID：N/A（定义）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A
