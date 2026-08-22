# METRIC-SEED-REGISTER-L01 · OPEN 新号身份注册进 seed

> 定义任务。`D1=draft`，`algorithm_type=UNKNOWN`。**未**把赋号建议类型当已签。**未**改存量口径/公式/源表。**未**改 A2 missing。

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

前置 `METRIC-ID-ASSIGN-L01` 已签收。按 `id-assign/*.yaml` 把**新建** `M_*` 写入 `cfg_metric-{域}-seed.yaml` + 对应就绪度矩阵。

| 动作 | 条数 |
|------|------|
| 新注册（含 B 轨 reuse 但 seed 缺失的 `M_SVC_ORG_TECH_SCORE`） | **156** |
| 已在 seed 的 reuse，跳过、不改口径 | 5：`M_ENT_TECH_POWER_SCORE` / `M_ENT_BUSINESS_POWER_SCORE` / `M_ENT_ATTRACTION_INDEX` / `M_ENT_CULTIVATION_INDEX` / `M_ENT_COMPETITIVENESS_SCORE` |
| ZHIKU 非红 `ZHIKU-S*` 保持赋号卡前缀，不入 seed | 25 |
| 四枚 🔴 demo_lock 不注册 | 4 |

分域新注册：INNOV 99 · TECH 22 · TALENT 13 · ORG 12 · ENT 7 · SVC 2 · COMMON 1。

机器清单：`metrics/request/_work/METRIC-SEED-REGISTER-L01-new-ids.md`。

`scripts/lib/metric-registry-lib.mjs` 抽检：新号 `found.seed+matrix`、`algorithm_type=UNKNOWN`、`d1=draft`、`lifecycle_stage=open`；`ZHIKU-S1-TASK-TOTAL` 不在 catalog。

## DoD 对照

| 项 | 结果 |
|----|------|
| 新建 M_* 进 seed；reuse 不改 definition/formula/source/type | ✅ ENT 存量 60 条 hash 未变 |
| D1=draft；algorithm_type=UNKNOWN；禁止 suggested 当已签 | ✅ |
| d1_pending_ref 挂 Q-MO-* / Q072+；无 Q 则 `GAP-ALGO-TYPE-UNSIGNED` | ✅ |
| 矩阵 lifecycle_stage=open；不改 D2/D3/D4 为绿 | ✅ pending / pending_ods / mock |
| ZHIKU 非红不发明 M_ZHIKU_*；四红不注册 | ✅ |
| 与 A1 并行只新增行 | ✅ 未改 CHAIN/POLICY/SYNTH/TNIE 口径 |
| A2 missing 不改 mapped；禁止 D1=aligned | ✅ |
| handoff 含新注册清单与 reuse 跳过清单 | ✅ 本文件 + new-ids.md |

## 偏离说明

- 新建域 seed：INNOV / TECH / ORG / TALENT / COMMON；SVC seed **仅 2 条** OPEN 身份，B 轨 29 条 `calc-logic/SVC/` **未**全量灌入。
- 无独立 Question 的 draft 挂 `GAP-ALGO-TYPE-UNSIGNED`（公式/类型未签），不是新的甲方口径题。
- YAML 按 `metric-registry-lib.mjs` 子集语法写（dash 缩进、flow 列表、`>` 口径），不用 PyYAML 默认 dump（该 dump 机器解析器读不到）。

## 产物清单

- `metrics/registry/cfg_metric-{INNOV,TECH,ORG,TALENT,COMMON,SVC}-seed.yaml`（新建）
- `metrics/registry/cfg_metric-ENT-seed.yaml`（+7）
- `metrics/registry/metric-readiness-matrix-{INNOV,TECH,ORG,TALENT,COMMON}.yaml`（新建）
- `metrics/registry/metric-readiness-matrix-ENT.yaml`（+7）
- `metrics/registry/metric-readiness-matrix-SVC.yaml`（+2）
- `metrics/registry/README.md`、`metrics/README.md`（现网域列表）
- `metrics/request/_work/METRIC-SEED-REGISTER-L01-new-ids.md`
- `metrics/request/_work/seed_register_open_ids.py`（可重跑检查）

## 验收证据

- 库解析：ENT 67/67、INNOV 99/99、TECH 22/22、ORG 12/12、TALENT 13/13、SVC 2/2、COMMON 1/1。
- CI/CD：定义资产，`cicd: skip`。

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
| actual_tokens | 80000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.0 |
| cost_warn | green |

## 会签

| 角色 | 结论 |
|------|------|
| 身份 Owner `human:淮政玮` | 身份注册完成；类型/公式仍 pending 唐绍祖 |
| 公式 / 类型 `human:唐绍祖` | 不在本叶；走 A1 会签后 `ALGO-LIB-SEED-TYPE-L01` |

## 遗留风险

- 建议类型仍只在赋号卡，seed 为 UNKNOWN。
- OPEN 新号多数不在算法库 97 叶，A1 ODS 表不会自动覆盖它们。
- 无 Q 的 draft 用 `GAP-ALGO-TYPE-UNSIGNED`，未写入客户决策清单正文。

## CI/CD（必填）

- 分支：`dev`（编排仓，本会话未要求 push）
- commit：待你确认后提交
- pipeline URL / ID：N/A
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：`node` + `metric-registry-lib.mjs getMetric` 抽检通过
