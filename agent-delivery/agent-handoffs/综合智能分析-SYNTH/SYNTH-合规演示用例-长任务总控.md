# SYNTH 合规演示用例整理 + 数据条件填充 · 长任务总控（无人值守）

> **日期**：2026-11-07
> **授权人**：`human:徐滕强`（本管线监管人；用户本轮原话「创建一个长任务……执行时可自行分解为多个子智能体并行完成」= 总控一次授权，**后续认领不必再问**）
> **规约**：`agent-delivery/长任务执行规约.md`；`claim_type=coordinator_dispatch`；`lock_hours=24`
> **一句话目标**：按最新规程（功能合规过渡口径）整理综合智能分析全部子模块（活力/要素/协同，需规 133–141 九叶）的**合规演示用例**，形成 LOOP 执行编排计划；调研当前 demo 库数据情况，**逐条**为用例填充可支持的输入/选择条件；数据无法支持的明确缺口（GAP/CLOSED 引用），不遗漏、不造假。

---

## 0. 术语与最新规程口径（执行 agent 必读）

| 术语 | 本管线含义 | 真源 |
|---|---|---|
| 合规演示用例 | 在功能合规过渡口径下可演示、可追溯的最小操作序列：**输入条件 → 触发动作 → 期望结果（含过渡标识）**。数值可来自 `is_mock=1` / `pending_registration` / `gapfill_transitional`，但**必须带标识**，不得当正式业务结论 | `sdd/功能合规过渡设计-137与C05.md`、`sdd/reconciliation/需规功能一致性审计-20261107.md`、`sdd/reconciliation/九叶功能覆盖矩阵.md` v1.1.0 |
| 输入/选择条件 | 页面条件栏三元组 `region × compare × window`（活力另含 `weight_profile`）+ 叶内局部筛选（要素三透镜/全景分类、协同产业/关系类型/图谱截断、任务键 6 个 analysisType） | `lumen-ui-topic/src/composables/useSynthCtx.ts`（条件枚举唯一真源） |
| 数据情况调研 | demo 库 `demo_gkxlumenx_ads` / `demo_gkxlumenx_ai` 中 SYNTH 相关表逐表行数、城市×窗口覆盖、批次状态 | 本总控 §3 调研清单 |
| 明确缺口 | 条件×指标组合无数据行支撑的用例 → 引用既有缺口真源（`SYNTH-*-data-gap-catalog.yaml`、`Q-SYNTH-*`、GAP-*），**不新造缺口编号**；确属新缺口才登记并注明 | 各叶 data-gap-catalog + 客户决策清单跟踪表 |

**禁止**：为凑用例编造数值；把 mock 行写成真值；把 135 区县粒度缺口"顺手"用深圳数据顶替；在前端硬编码缺口文案。

---

## 1. 已拍板（执行 agent 不回问）

1. **模块范围** = 综合智能分析三叶全部子模块：活力（133–135）、要素（136–138）、协同（139–141）。SYNC 三册 L2 + 总册为设计真源。
2. **条件枚举**（写死，与代码一致，禁止另选）：
   - `region`：深圳 / 广州 / 东莞 / 惠州（`REGION_OPTIONS`）
   - `compare`：全国重点城市（唯一 `COMPARE_OPTIONS`）
   - `window`：最近1年 / 最近3年 / 最近5年（URL 码 `1y|3y|5y`）
   - 活力 `weight_profile`：`INDEX_MAIN`（默认）/ `EQUAL`；legacy 档 `WEIGHT_MAIN`/`TEMP_*` 仅作反例用例（`legacy_unknown` 禁复用）
   - 默认三元组（秒开）：深圳 × 全国重点城市 × 最近3年
3. **用例覆盖矩阵基准** = 4 城市 × 3 窗 × 3 叶（活力再 × 2 权重档 + 2 反例档）× 叶内关键动作。默认三元组必有快照（404 分支也要有用例）；非默认组合按数据实际情况标注「可演示 / 缺口」。
4. **数据调研范围** = §3 清单所列表；demo 库连接：`10.50.11.76`，库 `demo_gkxlumenx_ads` / `demo_gkxlumenx_ai`（账号走 `LUMEN_ALGO_MYSQL_*` / 既有 database-mcp 分组，只读）。**禁止**写任何正式 `gkxlumenx_*`。
5. **过渡标识三件套**必须出现在每条用例的期望结果里（如适用）：`is_mock=1`、`metric_status=pending_registration`（137 四维）、`dataSource=gapfill_transitional`（C-05 回退）。
6. **缺口处理**：引用既有 `SYNTH-{VITALITY|ELEMENT|COLLAB}-data-gap-catalog.yaml` 与客户决策清单 `Q-SYNTH-*`；新缺口登记进 M4 汇总表并交叉引用，不重复建编号。
7. **产物落点**：`agent-delivery/agent-handoffs/综合智能分析-SYNTH/合规演示用例/`（新目录）：`00-用例总册.md`、`vitality-cases.md`、`element-cases.md`、`collab-cases.md`、`data-survey-20261107.md`、`condition-fill-matrix.yaml`、`gap-summary.md`、`LOOP-执行编排计划.md`。
8. **cicd: skip**（纯编排仓文档）；不改 `metrics/registry/` seed；不改业务仓代码。
9. **升级人**：结构歧义 / 甲方口径 → `human:李伟`；业务用例期望改动 → 本总控授权人。
10. 签收：coordinator 推进至 `ready_to_sign` 积压不挡主链；`ready_to_sign→done` 由 `human:淮政玮` 签收（公约 §7.2 闸门，definition 类无豁免；总控授权不可替代）。

---

## 2. 段 / 叶表（M0–M5）

| 段 | task-id | agent | 仓 | 产物 | 依赖门 |
|---|---|---|---|---|---|
| M0 | `SYNTH-DEMO-CASE-CTL-L01` | coordinator-agent | gkx-orchestration | 本总控 + 建单 + registry push | — |
| M1a | `SYNTH-DEMO-CASE-M1-USM-L01` | product-agent | gkx-orchestration | `00-用例总册.md`：三叶 USM 动作清单 × 条件枚举矩阵（逐条编号 CASE-VIT-*/ELEM-*/COLLAB-*） | M0 |
| M1b | `SYNTH-DEMO-CASE-M1-CASES-L01` | doc-agent | gkx-orchestration | 三份 `*-cases.md`：每条用例 = 条件 + 步骤 + 期望（含过渡标识）+ 数据依赖表/接口 + 缺口占位 | M1a |
| M2 | `SYNTH-DEMO-CASE-M2-DB-L01` | data-agent | gkx-orchestration | `data-survey-20261107.md`：§3 清单逐表行数/城市×窗覆盖/批次状态/`is_mock` 比例 | M0（与 M1 并行） |
| M3 | `SYNTH-DEMO-CASE-M3-FILL-L01` | data-agent | gkx-orchestration | `condition-fill-matrix.yaml`：CASE × 条件 → `supported`（引表+行数）/ `gap`（引缺口）逐条判定，**不遗漏一条** | M1b + M2 |
| M4 | `SYNTH-DEMO-CASE-M4-GAP-L01` | doc-agent | gkx-orchestration | `gap-summary.md`：缺口归并（既有引用 vs 新登记）+ 修复建议 + 责任方 | M3 |
| M5 | `SYNTH-DEMO-CASE-M5-ORCH-L01` | architect（agent:arch-agent） | gkx-orchestration | `LOOP-执行编排计划.md`：演示执行 LOOP（轮次/顺序/每轮用例集/判定与退出条件），标注哪些轮依赖哪些表数据、gap 轮降级策略 | M1b + M3 |

DAG：

```text
M0 ─┬─ M1a → M1b ─┬─ M3 → ┬─ M4
    └─ M2 ────────┘       └─ M5
```

M1 与 M2 可并行；同仓无代码冲突（各写各文件）。

## 3. 数据调研清单（M2 必须逐表覆盖）

库：`demo_gkxlumenx_ads`（gapfill 输入本期也落此库）+ `demo_gkxlumenx_ai`（137 四维）。

| 库.表 | 用途 | 关键维度 |
|---|---|---|
| `synth_vit_index` | 活力指数 | region × window × weight_profile × year × batch |
| `synth_vit_dim_score` / `synth_vit_weight` | 四维分/权重 | 同上 |
| `synth_vit_indicator` | 活力分项 | region × window；注意 gapfill 三表（newprod/rd/pol）覆盖键 |
| `synth_vit_rank` / `synth_vit_trend` | 排名/趋势 | region × window |
| `gapfill_synth_new_product_sales_ratio` / `gapfill_synth_rd_employee` / `gapfill_synth_policy_effect` | 活力缺项输入 | region × 2024 |
| ADS `synth_elem_*`（index/type_score/level_score/domain_score/indicator/contrib/rank） | 要素 | region × window × 类型/层次/领域 |
| `demo_gkxlumenx_ai.synth_elem_four_dim_score` | 137 四维过渡 | region × compare × window × dim（48 行） |
| `gapfill_synth_collab_relation_year` | C-05 关系年化 | region × relation_type × year（35 行） |
| `gapfill_synth_collab_output_year` | C-05 产出序列 | region × year（20 行） |
| `gapfill_synth_collab_isolate_year` | 孤立主体 | region × entity（8 行） |
| `synth_collab_node` / `synth_collab_edge` / `synth_collab_network_stat` / `synth_collab_relation_input` / `synth_collab_index` / `synth_collab_output_corr` / `synth_collab_batch_meta` | 协同 ADS 面 | region × window × batch |
| DWD 汇聚源（要素全景 136 用） | `ElementPanoramaPanel` 数据面 | 只查行数与分类计数，不展开明细 |

每表输出：总行数、按 region（×window）分布、最新 `calc_batch_id` + `calc_status`、`is_mock=1` 行数、覆盖缺口（哪城哪窗 0 行）。

## 4. 用例编号规范（M1a 定稿，M1b/M3 消费）

- `CASE-VIT-<序2位>`（活力 133–135，含权重档与 legacy 反例）
- `CASE-ELEM-<序2位>`（要素 136–138，三透镜 + 四维 + 贡献）
- `CASE-COLLAB-<序2位>`（协同 139–141，图谱/网络/相关性/报告/策略）
- 每条必填：`条件(region|compare|window[|weight_profile])` / `入口(路由+动作)` / `期望结果(含过渡标识与 404/空态分支)` / `数据依赖(表.metric_id)` / `数据判定`（M3 填 `supported|partial|gap`，partial=主结果可出但子区块降级，引缺口）
- 数量基准：活力 ≥14（4城×3窗含默认秒开 404 分支 + 2 档位 + 2 反例）、要素 ≥12、协同 ≥15（含坏快照 batch_meta_missing、产业筛选、报告 PDF、LLM 降级）。**宁多勿漏**；M3 对每条逐格填。

## 5. 无人值守规则

1. 已拍板不回问；结构歧义该叶 blocked + 升级李伟，同段其它叶继续。
2. 只读 demo 库；MCP 建单/改状态后立即 commit + push registry（多会话保护）。
3. 每叶 handoff：`agent-handoffs/综合智能分析-SYNTH/SYNTH-DEMO-CASE-*.md`，含 `ponytail:` 行 + cost 四字段 + 架构合规自检。
4. 前端仓铁律不触发（本管线零业务仓改动）；编排仓 commit 带 `[agent:<role>]`，origin/dev 直推。
5. 数据库只读查询失败 2 次 → 该表记 `调查受阻` 继续下一张，不空转；SSH/K8s 不需要，禁止为查库开探活。
6. cost：单叶 >$10 停叶复盘 / >$20 hard stop。

## 6. 段完成定义

- M1b 完成时：三份 cases 文件用例总数 ≥ §4 基准，且每条都有数据依赖行（待 M3 判定）。
- M3 完成时：`condition-fill-matrix.yaml` 覆盖 M1b 全部 CASE 编号，零缺格；`supported` 必须带表名+行数证据，`gap` 必须带缺口引用。
- M5 完成时：LOOP 计划每轮都有「用例集 / 前置数据 / 判定 / 退出」，gap 用例有降级路径，且与 M4 缺口表交叉引用一致。
- 总验收（M0 关单前）：M4 缺口数 = M3 gap 数；无一条用例既无 supported 又无 gap 标注。
