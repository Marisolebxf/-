# ALGO-LIB-T0X-REGISTER-L01 · T0-X 会前 — 分析清单指标注册进 metrics/registry

> 定义任务。`D1=draft`，`algorithm_type=UNKNOWN`。**未**把 A1 表2 / 赋号建议类型当已签。**未**改存量口径/公式/源表。**未**改 A2 `missing→mapped`。**未**把 `TEMP_*` 写入 seed `metric_id`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·YAML 身份注册） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶写 registry YAML，未走 Headroom。 |

## 范围与实现

前置：`ALGO-LIB-T0X-L01` 会前分析清单、`TOPIC-ALGO-GAP-L02` / `DS-ALGO-GAP-L02` 覆盖表、A1 `TEMP_ALGO_*` 90 条。按对人说明四批写入 `cfg_metric-*-seed.yaml` + `metric-readiness-matrix-*.yaml`。

| 动作 | 条数 |
|------|------|
| 新注册（去重后） | **215**（CHAIN 39 / ENT 12 / INNOV 39 / ORG 10 / POLICY 13 / SVC 41 / SYNTH 25 / TALENT 19 / TECH 17） |
| reuse 跳过（已在 seed，不改口径） | **20**（F−L 已有号 5 + C 轨已在 seed 15） |
| F−L 闸门 | **77 / 77** `getMetric` → `found.seed=true`（72 新号 + 5 reuse） |
| A1 `TEMP_ALGO_*` → 正式 `M_*` | **90**（禁止 TEMP 当 seed id） |
| 新建矩阵 | `metric-readiness-matrix-POLICY.yaml`（POLICY 矩阵此前不存在） |

批次对照：

| 批 | 内容 | 落地 |
|----|------|------|
| A | F−L 72 无号赋正式号并入 seed/矩阵 | ✅；5 条已在 seed 只 reuse |
| B | 已有号未入 seed：专题 mapped 49 + 展示 mapped 3 + `M_ENT_KEY_TOTAL` | ✅；`M_ENT_KEY_TOTAL` 矩阵 D1 `missing→draft`，`d1_pending_ref=Q038`；未改 D2/D3/D4 |
| C | mapped 无号：专题 53 / 展示 113 | ✅ 按 A1 叶赋号或 reuse，与 D 去重后计入 215 |
| D | A1 表2 的 90 条 TEMP 先赋正式号再注册 | ✅ `TEMP_ALGO_ALGO-{DOM}-{KIND}-{N}_{seq}` → `M_{DOM}_{KIND}_{N}_{seq}`；`SYNTH-SYNTH` → `M_SYNTH_{n}_{seq}` |

F−L 已在 seed 的 5 条（未改口径）：`M_CHAIN_PRODUCT_COUNT` / `M_CHAIN_PATENT_COUNT` / `M_POLICY_INDUSTRY_FIT` / `M_SYNTH_ELEM_CONTRIB` / `M_SYNTH_COLLAB_OUTPUT_CORR`。

新条约定：`formula=pending_cosign: human:唐绍祖（未签）`，无 Q 则 `d1_pending_ref=GAP-ALGO-TYPE-UNSIGNED`。YAML 用 `metric-registry-lib.mjs` 子集语法（dash 缩进、flow 列表、`>` 口径），不用 PyYAML dump。已在矩阵的行只补 seed，不改原 D2/D3/D4。

机器清单与闸门表：

- `metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-new-ids.md`
- `metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-t0x-gate.md`
- `metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-plan.json`
- 写入脚本：`…-apply.py`；验收：`node …-verify.mjs`

## DoD 对照

| 项 | 结果 |
|----|------|
| F−L 77 行均有正式 `metric_id` 且 `found.seed=true` | ✅ `verify.mjs`：`fl=77` / `fl_seed=77` / `fail=0` |
| F∩L mapped 已有号未入 seed 的注册完；已在 seed 的不改 definition/formula/source/type | ✅ 专题 49 + 展示 3 + `M_ENT_KEY_TOTAL`；存量 ENT/CHAIN/POLICY/SYNTH/SVC seed body hash 校验通过 |
| mapped 无号赋正式号或 reuse；90 条 TEMP 先赋正式号；禁 TEMP 当 seed id | ✅ |
| D1=draft；algorithm_type=UNKNOWN；禁 suggested/A1 type 当已签；禁 D1=aligned；禁 A2 missing→mapped | ✅ |
| 子集语法；矩阵 `lifecycle_stage=open`；不把 D2/D3/D4 改绿；pending_ref 挂已有 Q 或 `GAP-ALGO-TYPE-UNSIGNED` | ✅ `M_ENT_KEY_TOTAL` 挂 Q038 |
| 注册清单 + T0-X 复会闸门表；handoff 含新号/跳过 | ✅ |
| 不写业务代码；不开 OPEN 贴源 / GDF / T0-X 四桶 | ✅ |

## 偏离说明

- **域前缀误挂（闸门仍绿）**：`DS-07-INDUSTRY-POTENTIAL-00{4,5,6}` 因 `POTENTIAL` 含子串 `ENT` 写成 `M_ENT_DS_07_INDUSTRY_POTENTIAL_*`，进企业域 seed。T0-X `getMetric` 可解析。后续可改挂 INNOV/TECH，本叶不改号以免闸门表漂移。
- `DS-02-ENTITY-004` → `M_ENT_DS_02_ENTITY_004`（`ENTITY` 含 `ENT`）；技术点影响力语义上更偏 TECH/INNOV，同样可解析、未改号。
- 新建 `metric-readiness-matrix-POLICY.yaml`；`metrics/registry/README.md` 与 `metrics/README.md` 现网矩阵列表已加 POLICY。
- 无独立 Question 的 draft 挂 `GAP-ALGO-TYPE-UNSIGNED`，不是新的甲方口径题。
- 本会话未要求 commit / push。

## 产物清单

- `metrics/registry/cfg_metric-{CHAIN,ENT,INNOV,ORG,POLICY,SVC,SYNTH,TALENT,TECH}-seed.yaml`（追加新身份）
- `metrics/registry/metric-readiness-matrix-{同上}.yaml`（POLICY 为新建）
- `metrics/registry/README.md`、`metrics/README.md`（现网矩阵含 POLICY）
- `metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-apply.py`
- `metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-dump-catalog.mjs`
- `metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-plan.json`
- `metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-new-ids.md`
- `metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-t0x-gate.md`
- `metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-verify.mjs`
- `metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-patch-key-total.py`

## 验收证据

- `node agent-delivery/metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-verify.mjs` → `{ "checked": 86, "fail": 0, "fl": 77, "fl_seed": 77 }`（含 `M_ENT_KEY_TOTAL` D1=draft 补丁后复跑）。
- 假 ID `M_CHAIN_REG_COMMERCIALIZE` 不存在；真源 `M_CHAIN_REG_COMMERCIALIZATION` 在 seed。
- CI/CD：定义资产，`cicd: skip`。本会话未 push。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 不写算法实现 |
| 2 调用链 | ✅ 不越层 |
| 3 NebulaGraph | ✅ 不引入 Neo4j |
| 4 可观测性 | N/A |
| 5 CI/CD | ✅ skip |
| 6 demo2 merge | ✅ 不 merge lumen |
| 7 共享聚合 | ✅ 只改编排仓身份 YAML |
| 8 数据策略 | ✅ pending_ods，不伪 full |
| 9 D8 | N/A |
| 10 D9 | ✅ draft + UNKNOWN，不标 aligned |
| 11 D10 | N/A |
| 12 D12 | ✅ 不调 demo 服务 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 150000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 2.5 |
| cost_warn | green |

## 会签

| 角色 | 结论 |
|------|------|
| 身份 Owner `human:淮政玮` | 待签收。身份注册完成；类型/公式仍 pending 唐绍祖 |
| 公式 / 类型 `human:唐绍祖` | 不在本叶；走 A1 会签后 `ALGO-LIB-SEED-TYPE-L01` / T0-X 复会 |

## 遗留风险

- 建议类型仍只在赋号卡 / A1 表2，seed 为 UNKNOWN。
- 3 条 F−L 产业潜力指标域前缀误挂 ENT（见偏离）；不影响会前 `getMetric`。
- OPEN / 贴源 / GDF / 四桶不在本叶。
- 无 Q 的 draft 用 `GAP-ALGO-TYPE-UNSIGNED`，未写入客户决策清单正文。

## CI/CD（必填）

- 分支：`dev`（编排仓，本会话未要求 push）
- commit：待你确认后提交
- pipeline URL / ID：N/A
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：`node agent-delivery/metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-verify.mjs` → F−L 77 全绿
