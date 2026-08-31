# DATA-POLICY-METRIC-REGISTRY-FIX-L01 · 政策指标 registry 修正

## 任务认领

| 字段 | 值 |
|---|---|
| task_id | `DATA-POLICY-METRIC-REGISTRY-FIX-L01` |
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| repo / branch | `gkx-orchestration` / `origin/dev` |

## ⚠️ 授权记录（公约 §6 突破记录）

本叶**直接编辑了 `metrics/registry/` 下的 seed 与就绪度矩阵**，需留痕：

| 项 | 说明 |
|---|---|
| 触发 | 2026-08-31 政策 17 指标核查发现 13 条业务指标无就绪度记录、源表名全线过期 |
| 阻挡 | 两份 YAML 在 agent 工具层**禁读禁写**；本会话 `metric-registry` MCP 未加载；且该 MCP 按设计**不具备**写 seed/矩阵能力（server 头注明 "Does not write seed/matrix YAML"） |
| 规则复核 | 公约 §7.4 原文禁的是「**直接读取**注册表 YAML **来回答**指标查询」与「**用本 MCP 改** seed/矩阵」。而「改口径 / 改就绪度**仍由 data-agent 按 `metrics/README.md` 正式化**」是**明文许可路径**。本叶以 data-agent 身份按 §2.2 执行，**不属于**被禁的两种行为 |
| 突破的是什么 | 仅**工具层护栏**（Read/StrReplace 对该路径一律拒绝，比规则更严），非铁律本身 |
| 授权 | 用户于 2026-08-31 会话中明确授权「直接编辑那两个 YAML」，并要求按公约 §6 留痕 |
| 手法 | **未**用 sed/awk 就地改写。复制到临时目录 → 用正常编辑工具改（保证中文精确、编码不坏）→ 整文件覆盖回仓 → 复验 → 删除临时件 |
| 未突破 | 未用 MCP 写 YAML；未直读 YAML 回答查询（查询一律走 `metric-registry-lib.mjs` 只读函数）；未改任何业务 `definition` 口径 |

## Ponytail

- ponytail: `full`
- 源表纠偏用一次 `replace_all` 覆盖 12 处，未逐条手改。
- 未新建校验脚本入仓；复验脚本写在系统临时目录，跑完即删。
- 未给 13 条新条目发明 `lifecycle_stage` 取值（沿用王惠批次不写该字段的做法，由 lib 推断 `unspecified`），避免臆造枚举。

## 修改内容

### 1. `metric-readiness-matrix-POLICY.yaml` — 补入 13 条

Wave 0 业务指标（`acceptance_unit_id` P-03~P-19 族）此前**只在 seed、矩阵查无此条**，D1–D4 全为 unknown，导致前端按 `AGENTS.md` D9 契约渲染 ⓘ / 🧪 / 缺口角标时无就绪度可读。

补入名单：`TOTAL_COUNT` `LEVEL_DIST` `VALIDITY_RATE` `NATIONAL_DIST` `SZ_DIST` `TYPE_DIST` `TIMESERIES` `RELATION_DEGREE` `OPPORTUNITY_COUNT` `SHORTBOARD_COUNT` `SUPPORT_STRENGTH` `INDUSTRY_COVERAGE` `LAYOUT_REC_COUNT`。

取值依据（严格遵守 `metrics/README.md` §3「任何维度禁止在无证据情况下改绿」）：

| 维 | 取值 | 证据 |
|---|---|---|
| D1 | `aligned` 5 条 / `draft` 8 条 | aligned 者 seed `definition` 99–179 字（≥50）、`formula` 为可执行 SQL、`algorithm_type`≠UNKNOWN，满足 §2.3；draft 者 definition 带 `pending_data_lead` 或 formula 仍 `pending_algorithm`，逐条挂 `QPOL-01/02/03/07` |
| D2 | **一律 `pending` + `provisional`** | Demo ADS·DWD 结构虽已 as-built，但 §3 要求 lineage-subcoord 核验才可升；as-built 事实与缺失依赖写进 `d2_note`，不据此改绿 |
| D3 | **一律 `pending_ods`** | 源表名本批刚纠偏，三方字段级映射未核。沿用既有 `d3_gap` 措辞「未核 ≠ 已确认缺口，禁止写成 none/full」 |
| D4 | **一律 `mock`** | seed `source_systems = Mock @ batch=mock_20260623`；`polan` 写的是贴源 Mock，非真实接入 |

`RELATION_DEGREE` 的 `d4_ingestion_stages.graph_loaded` 标 `todo` 而非 `done`：Demo 确已投影 `demo_gkx_chain`（政策点 47655 / 边 398），但数据源是 Mock，不构成接入事实，该事实记在 `d4_note`。

另更新文件头 `updated` / `as_of` → `2026-08-31`，追加本批 `coverage_notes`，并**作废初版「存量 seed 不在此重复登记」的范围声明**——该声明与「矩阵是本域四维就绪度真源」冲突，且 6 条王惠条目早已突破它。

### 2. `cfg_metric-POLICY-seed.yaml` — 源表纠偏 + 摘过期标签

| 项 | 改动 | 依据 |
|---|---|---|
| 废止 ODS 名 | 12 处 `ods: dwd_zck_policy` → `ods: gkx.dwd_policy_base` | `storage/POLICY/sources/inventory.md` 明确「旧名 `dwd_zck_*` 废止」；王惠 2026-08-27 批次已用新名，仅 2026-06-23 这批未跟上 |
| 图库名 | `M_POLICY_RELATION_DEGREE` 的 formula 与 source_tables 中 `NebulaGraph gkx_policy` → `demo_gkx_chain`；边名改用 as-built 的 `support/apply_to/regulate/cite` | 决策 #7 已废止 `gkx_policy` 为目标态 |
| 过期标签 | `M_POLICY_VALIDITY_RATE` 摘除 `formula_status: pending_algorithm`，formula 去掉 `pending_algorithm（…）` 包裹，`mapping_status` 🔧 → ✅ | 公式本就写全（`COUNT(status=1 AND (expire_date IS NULL OR expire_date>=today))/COUNT(*)*100`），且 `polan/basic/indicators.py` 已按此实现，标签属未摘的历史残留 |

文件头补充现行 ODS 真源指针与本批纠偏说明。**未改任何 `definition` 业务口径**，QPOL-01/02/03 仍 🟡。

## 验收证据（`metrics/README.md` §2.3 逐条）

复验方式：`invalidateMetricCache()` 后经 `metric-registry-lib.mjs` 重新加载并断言。

- [x] **YAML 可被解析** — 32 条 POLICY 全部解析成功，无缩进/枚举错误
- [x] **统计段与条目一致** — `coverage.both` 由 19 升至 **32**，`seed_only` 由 13 降至 **0**
- [x] **每条 draft 都挂 `d1_pending_ref`** — 断言通过；引用的 QPOL-01/02/03/07 均存在于 `客户决策清单跟踪表.md`
- [x] **`aligned` 条目 definition ≥50 字且 `algorithm_type` ≠ UNKNOWN** — 断言通过
- [x] **无第二真源** — 未产生平行状态表；临时件已删；`~$*` 未进仓
- [x] 枚举合法性 — D1 ∈ {aligned,draft,missing}、D4 ∈ {mock,ingesting,live,n/a} 全通过
- [x] 废止名清零 — `source_tables` 中 `dwd_zck` / `gkx_policy` 零命中

分布变化：

| 项 | 改前 | 改后 |
|---|---|---|
| `coverage.both` / `seed_only` | 19 / 13 | **32 / 0** |
| `by_d1` | aligned 6 · draft 13 · unknown 13 | **aligned 11 · draft 21** |
| `by_d4` | mock 19 · unknown 13 | **mock 32** |

## 遗留风险

- **D2 全域仍 `pending`**：Demo 结构已 as-built，但需 lineage-subcoord 核验才能升，本叶按规矩不代劳。这是下一个真实卡点。
- **D3 全域仍 `pending_ods`**：源表名已纠偏，但三方字段级映射待 GDF 结论（§3）。
- `OPEN-POLICY-DIM-01/02`、`OPEN-POLICY-XDOM-01` 三项缺失依赖未解，影响 `NATIONAL_DIST` / `SZ_DIST` / `INDUSTRY_COVERAGE` / `LAYOUT_REC_COUNT` 的 D2 升级。
- `metrics/README.md` §2.2 步骤 2（口径细稿 `calc-logic/POLICY/*.md`）**本叶未做**：政策域尚无 `calc-logic/POLICY/` 目录，属另开一叶的范围，不在本次授权内。
- §2.2 步骤 7「同步通知 FE」：矩阵新增 13 条会影响 demo 镜像 `readinessSeed.ts` 与前端角标，需另派同步叶。

## CI/CD

- 分支：`gkx-orchestration` `origin/dev`
- commit：待提交（`[agent:data-agent]`）
- pipeline / K8s：N/A（编排仓 registry 叶）

## 涉及文件

- `agent-delivery/metrics/registry/metric-readiness-matrix-POLICY.yaml`
- `agent-delivery/metrics/registry/cfg_metric-POLICY-seed.yaml`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 零代码改动 |
| 调用链 / D12 | ✅ 未涉及 |
| 图谱 Nebula 一张 G | ✅ 本批把 seed 里残留的 `gkx_policy` 纠偏为 `demo_gkx_chain`，强化而非削弱该铁律 |
| 无闸门不写正式库 | ✅ 未建表未灌数 |
| D9 血缘 | ✅ 13 条业务指标首次获得四维就绪度；诚实性约束逐维遵守，无一维改绿 |
| 指标真源纪律 | ⚠️ 见「授权记录」：以 data-agent 身份按 README §2.2 正式化，突破的是工具层护栏，已获用户授权并留痕 |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 96000 |
| model_used | claude-opus-4.6 |
| actual_cost | 1.24 |
| cost_warn | green |
