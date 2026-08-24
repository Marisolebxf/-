# ALGO-LIB-SEED-TYPE-L01 · A1 会签后回填 seed — algorithm_type 与已签 formula

> 定义任务。把 A1 表2 ∩ seed 的 **10 条 `M_ENT_*`** 的 `algorithm_type` 回填进 seed。`formula` 保留 seed 现有（监管人决策 keep_detail）。`M_ENT_KEY_TOTAL` 不在 seed，跳过。**未**改 definition/源表/源系统/更新频率，**未**把赋号卡 `suggested_unsigned` 当已签，**未**改 A2 missing。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:唐绍祖` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off` |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶回填 seed YAML，未走 Headroom。 |

## 范围与实现

按 `metric_id` 精确相交 A1 表2 ∩ seed。表2 共 101 条 = **11 条正式 `M_*`**（全企业域）+ 90 条 `TEMP_ALGO_*`。

- **回填 10 条**（`algorithm_type` 仅，formula 保留）：

| metric_id | algorithm_type |
|---|---|
| `M_ENT_TYPE_COUNT` | `STAT` |
| `M_ENT_DOMAIN_COVERAGE_COUNT` | `STAT` |
| `M_ENT_NEW_COUNT_Y` | `STAT` |
| `M_ENT_COMPETITIVENESS_SCORE` | `MODEL` |
| `M_ENT_PAINPOINT_COUNT` | `MODEL` |
| `M_ENT_SUPPLY_CHAIN_RISK` | `MODEL` |
| `M_ENT_TECH_POWER_SCORE` | `MODEL` |
| `M_ENT_BUSINESS_POWER_SCORE` | `MODEL` |
| `M_ENT_ATTRACTION_INDEX` | `MODEL` |
| `M_ENT_CULTIVATION_INDEX` | `MODEL` |

- **跳过 1 条**：`M_ENT_KEY_TOTAL` — `found.seed=false`，`d1=missing`，`d1_pending_ref=Q038`，`d1_note="未入 cfg_metric-ENT-seed，待王惠正式化"`。不在 seed，本叶不代注册。
- **skip 90 条** `TEMP_ALGO_*`：未入 seed，不发明 `M_*` 写入。

写入方式：`metric-registry-lib.mjs` 子集语法，在 `formula:` 后插 `algorithm_type:` 行，**保留 CRLF + BOM**，避免整文件行尾改写。

## DoD 对照

| 项 | 结果 |
|----|------|
| 仅回填已签 algorithm_type/formula；未签不写 | ✅ 只写表2 已签的 10 条 type |
| 回填 cfg_metric-{域}-seed.yaml 对应行；不把 suggested 当已签 | ✅ ENT seed +10 行；未动赋号卡 |
| MODEL/GRAPH 步骤留定义卡/表2，不冒充 8 件套缺项 | ✅ 只写 type，不写 steps |
| D1 仅 9 项齐才 aligned；否则 draft；禁 UNKNOWN 派实现单 | ✅ 10 条 D1 仍 draft，未动 |
| 不改存量口径 definition/源表 | ✅ 仅 +10 行 algorithm_type |
| data-agent 协作枚举/缩进校验；handoff 含回填清单 | ✅ 库解析 67/67；回填清单见 `_work/` |
| 不写业务代码；不把 A2 missing 改 mapped | ✅ 定义叶，无代码 |

## 偏离说明

1. **`M_ENT_KEY_TOTAL` 不在 seed**（`found.seed=false` / `d1=missing` / `Q038` /「待王惠正式化」）。按监管人 `skip10` 决策跳过，不代注册、不代写类型/公式。**需淮政玮确认**：是否待王惠正式化后由 data-agent 注册，再走一次回填。
2. **formula 保留 seed 现有（keep_detail）**：给人说明字面要求「写表2 公式」，但表2 MODEL 公式是空泛骨架 `MODEL(特征标准化 + 指标聚合 + 模型评分)`，覆盖会丢维度细节；而 seed 现有 formula 本身即「命名维度、不写权重」的合规骨架（技术力五维 / 竞争力四维 / 断链韧性四因子等），符合「不编权重」铁律且更详细。监管人决策保留 seed formula、只补 `algorithm_type`。
3. **矩阵 `lifecycle_stage` 未动**：DoD 未要求；给人说明对矩阵仅「允许」`open/identified → formula_signed` 未「强制」。本叶不改 D2/D3/D4、不标 `kit_complete`。

## 产物清单

- `metrics/registry/cfg_metric-ENT-seed.yaml`（+10 行 `algorithm_type`）
- `metrics/request/_work/ALGO-LIB-SEED-TYPE-L01-backfill.md`（回填清单，含 skip 90 全列表）

## 验收证据

- `metric-registry-lib.mjs` 解析：ENT seed `declared_total=67` vs `parsed=67`（YAML 无损坏）。
- `metric-summary`（domain=ENT）`by_algorithm_type`：`UNKNOWN=78, STAT=3, MODEL=7`，与回填 10 条完全一致。
- `metric-get` 抽检 4 条：`M_ENT_TYPE_COUNT=STAT`、`M_ENT_TECH_POWER_SCORE=MODEL`、`M_ENT_ATTRACTION_INDEX=MODEL`、`M_ENT_CULTIVATION_INDEX=MODEL`，`algorithm_type_inferred` 已消失（字段真实写入），formula 原样。
- `git diff`：`1 file changed, 10 insertions(+)`，仅 10 行 `+    algorithm_type: ...`，无 CRLF/BOM 污染。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 不写算法实现 |
| 2 调用链 | ✅ 不越层 |
| 3 NebulaGraph | ✅ 不引入 Neo4j |
| 4 可观测性 | N/A |
| 5 CI/CD | ✅ skip |
| 6 demo2 merge | ✅ 不 merge lumen |
| 7 共享聚合 | ✅ 只改编排仓 seed YAML |
| 8 数据策略 | ✅ 不伪 full |
| 9 D8 | N/A |
| 10 D9 | ✅ draft + type，不标 aligned |
| 11 D10 | N/A |
| 12 D12 | ✅ 不调 demo 服务 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 待回填（本会话未统计，由监管人补） |
| model_used | 待回填 |
| actual_cost | 待回填 |
| cost_warn | green |

## 会签

| 角色 | 结论 |
|------|------|
| 状态 | `ready_to_sign`（registry 同步，`ready → claimed → ready_to_sign`，**未**置 `done`） |
| 公式 / 类型 `human:唐绍祖` | 本叶执行，已回填 10 条 algorithm_type 并抽检；formula 保留 seed 现有（keep_detail） |
| 身份 Owner / 签收 `human:淮政玮` | 待签收；`M_ENT_KEY_TOTAL` 不在 seed 需确认 |

## 遗留风险

- `M_ENT_KEY_TOTAL` 未注册进 seed，Q038 待王惠正式化；其 `algorithm_type=STAT` 已在表2 签收，但 seed 未落，后续需补注册 + 回填。
- 10 条 MODEL 的 formula 仍为骨架（命名维度、无权重），`D1` 仍 `draft`，未达 `aligned`。
- 其余 OPEN 新号（INNOV/TECH/ORG/TALENT 等）`algorithm_type` 仍 `UNKNOWN`，等后续 OPEN 贴源叶。

## CI/CD（必填）

- 分支：`dev`（编排仓，本会话未要求 push）
- commit：待你确认后提交
- pipeline URL / ID：N/A
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：MCP `metric-get` / `metric-summary` + `metric-registry-lib.mjs` 解析抽检通过
