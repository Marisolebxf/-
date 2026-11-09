# SYNTH 合规演示用例 · 活力叶细化（CASE-VIT-01～16）

- **日期**：2026-11-07
- **任务 ID**：`SYNTH-DEMO-CASE-M1-CASES-L01`（长任务 `SYNTH-DEMO-CASE-CTL-L01` 段 M1b；doc-agent 人格）
- **上游输入**：`00-用例总册.md`（M1a，CASE-VIT-01～16 编号/条件/入口真源）；`data-survey-20261107.md`（M2 实库调研，2026-11-07）
- **铁律**：
  1. 编号不变（16 条 CASE-VIT-01～16，与总册一一对应），不新增/改名/删除；
  2. 期望分支与代码一致：404 = `IntelBatchSnapshotNotFound`（前端进 no_batch 引导「开始分析」）；`legacy_unknown` / `WEIGHT_PROFILE_INVALID` 等 reason/错误码逐字保留；
  3. 过渡标识三件套（`is_mock=1`）随数值出现；禁止编造数值、禁止把 mock 写成真值；
  4. **M3 以本册为准**：凡标注**（对照M2修正）**的条目，为总册期望与 M2 实库事实矛盾/细化后的修正版，M3 判定按本册口径执行（修正索引见文末附录 A）。

---

## 0. 本叶 M2 数据事实速览（细化期望的事实依据）

| # | 事实 | 出处 | 对用例的影响 |
|---|---|---|---|
| F1 | 活力 ADS 全部表 `window_label` 仅「最近3年」；1y/5y = **0 行** | M2 §0.2 / §1.1 / G-01 | 非默认窗用例（VIT-04/05/09）期望收敛为 **404/引导开始分析**，不承诺出数 |
| F2 | `synth_vit_trend` 表**不存在**；趋势 = `synth_vit_index` 同键 2022/2023 历史年行（批 `mock_20261107_vit_trend_*`，`is_mock=1`） | M2 §1.6 | 趋势/报告用例（VIT-14/16）依赖表按 `synth_vit_index.year` 写 |
| F3 | 深圳行双批次冗余：通用 seed + 档位 seed 并存（index/weight/dim_score/indicator）；快照读取必须按 `calc_batch_created_at` 取最新（最新批 `mock_20261106_vit_seed_equal` 等） | M2 §0.5 / D-02 | 秒开用例（VIT-01/02/03/12）期望补「按最新批次取数」断言 |
| F4 | `synth_vit_dim_score` / `synth_vit_indicator` 非深圳行 `region_name` 全部误标「深圳」（`region_code` 正确） | M2 §0.5 / D-01 | 换城用例（VIT-06/07/08）补城市名展示风险注记 |
| F5 | `synth_vit_rank` 仅深圳市上下文 24 行（4 rank_city × 3 档 × 2 批次；深圳 rank1·is_current=1） | M2 §1.5 / G-02 | 排名用例（VIT-13）按深圳上下文书写；非深圳上下文 0 行为空态分支 |
| F6 | 活力 gapfill 三表各 4 行（四城 × 2024；无 region_code/window_label 列，键=`city`+`year`，批 `mock_20261107_vit_gapfill_seed`） | M2 §1.7 | 分项表三分项 `confidence=gapfill`（VIT-01/14） |
| F7 | 全表 `is_mock=1` 占比 100%；`calc_status` 全部 `succeeded` | M2 §0.3 | 所有出数用例必带 🧪 mock 标识 |
| F8 | 权重档行：INDEX_MAIN / EQUAL / WEIGHT_MAIN 三档齐（四城）；`TEMP_*` 档 0 行 | M2 §1.2 / G-03 | legacy 反例仅 `legacy_unknown` 存量任务路径（VIT-10）；非法档走参数校验（VIT-11） |

---

## CASE-VIT-01 · 活力默认三元组秒开（INDEX_MAIN）

| 项 | 内容 |
|---|---|
| 用例名 | 活力默认三元组秒开（深圳 × 全国重点城市 × 最近3年 × INDEX_MAIN） |
| 需规叶 | 133 指标体系构建 / 134 综合评价模型 / 135 指数计算与可视化（需规 seq 133–135，Excel 行 136–138） |

**前置条件**
- `demo_gkxlumenx_ads` 活力四表（index/dim_score/weight/indicator）最近3年有深圳行（M2 F1/F7：全库仅最近3年窗，`is_mock=1` 100%）；
- 活力 gapfill 三表各 4 行在库（M2 §1.7）；
- 排名表深圳市上下文 24 行在库（M2 §1.5）；
- 临时权重口径属 🟡 待甲方确认（Q-SYNTH-01 / Q-SYNTH-V-01 / Q-SYNTH-V-02），页面 ⚠️ 角标策略已启用。

**操作步骤**
1. 打开 `/intelligence/vitality`；
2. 确认 URL 为 `?region=深圳&compare=全国重点城市&window=3y&weight_profile=INDEX_MAIN`（默认三元组，无 URL 时按 `SYNTH_DEFAULTS` 补齐）；
3. 不点击任何按钮，等待结果区渲染（instant 分支，不建任务、不进过程页）。

**期望结果**
- 秒开 200：活力指数仪表 + 四维柱状 + 权重环 + 分项表 + 排名榜 + 优势短板全部渲染；回显档 = **INDEX_MAIN**（沿用响应内 `weight_profile`，禁前端自标）；
- 结果元信息显示「预计算结果 · 跑批于 …」；
- 所有 mock 行带 🧪 标识（`is_mock=1`）；⚠️ 临时权重「待甲方确认」角标出现（Q-SYNTH-01/V-01/V-02 🟡）；
- 分项表 `ind-newprod` / `ind-talent-cnt` / `ind-pol-effect` 三分项 `confidence=gapfill`（gapfill 三表覆盖，M2 F6）；
- （对照M2修正）**快照读取按最新批次**：深圳 2024 存在通用 seed + 档位 seed 双批次并存，快照必须按 `calc_batch_created_at` 取最新（`mock_20261106_vit_seed_index_main` 系），页面不得出现同键双值（M2 D-02）。
- **404 分支（单独列）**：若快照服务返回 404（`IntelBatchSnapshotNotFound`）→ 页面进 no_batch 态，显式引导「开始分析」，不静默空白、不 fixture 填数。

**数据依赖**
- `demo_gkxlumenx_ads.synth_vit_index`（region_code=深圳市 × window_label=最近3年 × weight_profile_code=INDEX_MAIN；全表 39 行、is_mock=1 39/39；最新批 `mock_20261106_vit_seed_equal` 系档位批，深圳 2024 双批次并存）——M2 §1.1 / D-02；
- `synth_vit_dim_score` / `synth_vit_weight` / `synth_vit_indicator` / `synth_vit_rank` 同上键（dim_score 96 行、weight 60 行、indicator 288 行、rank 24 行；全部 is_mock=1）——M2 §1.2–1.5；
- `gapfill_synth_new_product_sales_ratio` / `gapfill_synth_rd_employee` / `gapfill_synth_policy_effect`（各 4 行，city=深圳市 × year=2024，批 `mock_20261107_vit_gapfill_seed`）——M2 §1.7；
- metric_id：`M_SYNTH_VIT_INDEX` 等活力面（界面 ⓘ 触发）。

**演示备注**：能演示出结果——全部为 mock 过渡态，带 🧪 与 ⚠️ 标识演示；双批次冗余已由最新批口径消除。

---

## CASE-VIT-02 · 等权档 EQUAL 快照秒开

| 项 | 内容 |
|---|---|
| 用例名 | 权重档切「等权档」（EQUAL）快照秒开 |
| 需规叶 | 134 综合评价模型（加权融合单一指数）/ 135 指数可视化 |

**前置条件**
- `synth_vit_*` 存在 `weight_profile_code='EQUAL'` 行（M2 F8：四城三档齐；深圳 EQUAL 最新档位批 `mock_20261106_vit_seed_equal`）；
- 先完成 CASE-VIT-01（默认秒开态在场）。

**操作步骤**
1. 在 CASE-VIT-01 结果页定位条件栏权重档下拉；
2. 选择「等权档」→ URL 变为 `?region=深圳&compare=全国重点城市&window=3y&weight_profile=EQUAL`；
3. 等待结果区刷新（不点击「开始分析」）。

**期望结果**
- 该档最近成功快照秒开；index/dim/weight/rank 四表同码 EQUAL；权重环显示 25%×4；
- 与 CASE-VIT-01（INDEX_MAIN）数值不同（四段指纹 `region|compare|window|weight_profile` 断言，两档互不复用）；
- 换档不自动建任务（快照命中直接显示）；`is_mock=1` 🧪；⚠️ 角标沿用；
- （对照M2修正）快照按最新批次取（EQUAL 档位批 `mock_20261106_vit_seed_equal`，非通用 seed 批，M2 D-02）。
- **404 分支（单独列）**：EQUAL 档无快照 → no_batch 引导「开始分析」。

**数据依赖**
- `ads.synth_vit_index` / `synth_vit_weight`（weight_profile_code='EQUAL'；全表仅最近3年窗，M2 §1.1/§1.2）；
- `synth_vit_dim_score` / `synth_vit_rank` 同码行（M2 §1.3/§1.5）。

**演示备注**：能演示出结果（mock 过渡态）；两档数值差异可现场对比展示。

---

## CASE-VIT-03 · 权重主档 WEIGHT_MAIN URL 直达

| 项 | 内容 |
|---|---|
| 用例名 | 登记档 WEIGHT_MAIN URL 直达演示（页面下拉未露出） |
| 需规叶 | 134 综合评价模型（三档权重） |

**前置条件**
- `synth_vit_*` 存在 `weight_profile_code='WEIGHT_MAIN'` 行（M2 F8；登记档 seed 已灌）；
- 页面下拉仅露出 INDEX_MAIN / EQUAL 两档（`WEIGHT_MAIN` 为 URL 直达演示档）。

**操作步骤**
1. 浏览器地址栏直达 `/intelligence/vitality?region=深圳&compare=全国重点城市&window=3y&weight_profile=WEIGHT_MAIN`；
2. 等待结果区渲染；
3. 核对权重环数值与回显档。

**期望结果**
- 登记档快照秒开；权重环 = 0.30 / 0.35 / 0.20 / 0.15；回显档 = 权重主档（WEIGHT_MAIN）；
- 与 INDEX_MAIN / EQUAL 数值均不同；`is_mock=1` 🧪；
- （对照M2修正）快照按最新批次取（档位批 `mock_20261106_vit_seed_weight_main` 系，M2 D-02）。
- **404 分支（单独列）**：该档无快照 → no_batch 引导「开始分析」。
- 该档不是 legacy 档：不得出现 `legacy_unknown` 拦截。

**数据依赖**
- `ads.synth_vit_index` / `synth_vit_weight`（weight_profile_code='WEIGHT_MAIN'；M2 §1.1/§1.2，全表仅最近3年窗）。

**演示备注**：能演示出结果（登记档过渡态）；演示时强调「页面未露出、URL 直达可达」的登记档语义。

---

## CASE-VIT-04 · 深圳 × 最近1年（非默认窗 → 404/引导开始分析）

| 项 | 内容 |
|---|---|
| 用例名 | 非默认窗（最近1年）待分析态引导 + 显式开始分析 |
| 需规叶 | 135 指数计算与可视化（灵活选择时间窗、实时计算） |

**前置条件**
- 活力 ADS 全部表**无「最近1年」行**（M2 F1/G-01：1y/5y = 0 行）；
- 无该窗预置快照；任务中心无同四段指纹当天成功任务。

**操作步骤**
1. 从默认秒开态把时间窗切「最近1年」→ URL 变 `?region=深圳&compare=全国重点城市&window=1y&weight_profile=INDEX_MAIN`；
2. **不点击任何按钮**，观察结果区态（应出现待分析态与「开始分析」按钮）；
3. 点击「开始分析」→ 进入任务过程页（五阶段活力文案）；
4. 任务完成后点击「查看分析结果」进入任务结果态（V4）。

**期望结果**（对照M2修正）
- **主期望 = 404/引导分支**：切窗后无该窗快照 → 快照接口 404（`IntelBatchSnapshotNotFound`）→ 页面进 no_batch/config 待分析态，显式引导「开始分析」；**切条件不自动建任务**（Q-ANALYSIS-01）；
- **不承诺出数**：总册原期望「完成绑定任务快照出数」按 M2 G-01 收敛——活力 ADS 全表无 1y 行，任务链实算在该窗预期为诚实空值/失败分支，**不得伪装该窗出数、不补 0**；任务若成功返回，结果内空值字段按 null+reason 诚实展示；
- 任务过程页五阶段活力文案正常；同四段指纹当天复用单飞（同条件二次进入直接恢复任务）。

**数据依赖**
- `ads.synth_vit_index` 等 window_label='最近1年' → **0 行（M2 §1.1 G-01，本用例空态依据）**；
- 任务链表（#102–#105，非 ADS，M2 未覆盖）。

**演示备注**：演示诚实空态/拦截——404 → 引导开始分析是本条核心；任务提交后的空值/失败为诚实分支，不是演示事故。

> **（2026-11-08 更新：已闭合——见 SYNTH-DEMO-ACCEPT-LOOP.md R3）** 1y 窗已出数（200，`snap:mock_20261106_vit_seed_index_main_1y`），matrix 判定改 supported；本节 404/引导期望为当时的诚实分支，保留作历史记录。

---

## CASE-VIT-05 · 深圳 × 最近5年（非默认窗 → 404/引导开始分析）

| 项 | 内容 |
|---|---|
| 用例名 | 非默认窗（最近5年）待分析态引导 + 显式开始分析 |
| 需规叶 | 135 指数计算与可视化 |

**前置条件**：同 CASE-VIT-04（5y 窗 ADS 0 行，M2 G-01）。

**操作步骤**
1. 时间窗切「最近5年」→ URL 变 `?region=深圳&compare=全国重点城市&window=5y&weight_profile=INDEX_MAIN`；
2. 观察结果区待分析态；3. 点击「开始分析」；4. （延伸）完成/失败后查看对应态。

**期望结果**（对照M2修正）
- 同 CASE-VIT-04 结构：404（`IntelBatchSnapshotNotFound`）→ no_batch/config 引导；显式开始分析；
- ADS 无 5y 行 → 任务实算预期诚实空值/失败，不伪造出数、不补 0；
- 趋势点位按任务实算批（若有）；无非默认预填数据。

**数据依赖**
- `ads.synth_vit_*` window_label='最近5年' → 0 行（M2 §1.1 G-01）。

**演示备注**：演示诚实空态/拦截；本任务亦是 CASE-VIT-15（失败分支）的推荐触发路径。

> **（2026-11-08 更新：已闭合——见 SYNTH-DEMO-ACCEPT-LOOP.md R3）** 5y 窗已出数（200，`snap:mock_20261106_vit_seed_index_main_5y`），matrix 判定改 supported；其失败态触发器语义随之失效（见 VIT-15 注记）。

---

## CASE-VIT-06 · 广州 × 最近3年（换城任务实算）

| 项 | 内容 |
|---|---|
| 用例名 | 区域切广州 → 显式开始分析 → 任务实算 |
| 需规叶 | 135 指数计算与可视化（灵活选择区域、实时计算） |

**前置条件**
- `synth_vit_*` 广州 × 最近3年行在库（M2 §1.1：广州 index 9 行 = 3 年 × 3 档；is_mock=1 100%）；
- instant 秒开仅默认三元组（深圳×3y）→ 换城必回 config 待分析态（`vitalityResultSource` 分支）。

**操作步骤**
1. 从默认秒开态把区域切「广州」→ URL 变 `?region=广州&compare=全国重点城市&window=3y&weight_profile=INDEX_MAIN`；
2. 观察结果区：回 config 待分析态（不自动建任务）；
3. 点击「开始分析」→ 任务过程页（五阶段活力文案）；
4. 完成后点击「查看分析结果」→ 任务结果态。

**期望结果**
- config 待分析态 → 显式开始分析 → 任务实算广州结果；排名榜含广州行；回显条件与冻结四段指纹一致（region=广州）；
- 完成不自动跳（须手动点「查看分析结果」）；`is_mock=1` 🧪；
- （对照M2修正）**城市名展示风险**：`synth_vit_dim_score` / `synth_vit_indicator` 非深圳行 `region_name` 误标「深圳」（`region_code` 正确，M2 D-01）——若页面任何位置出现来自数据行的城市名，可能串显「深圳」；城市名应以条件栏/ctx.region 为准；该缺陷登记 M4 修复（seed UPDATE 可修），演示时不作为数据错误讲解口径。
- **失败分支（单独列）**：任务失败 → 过程页失败阶段 +「重新尝试」（见 CASE-VIT-15）。

**数据依赖**
- `ads.synth_vit_index` / `dim_score` / `weight` / `indicator` / `rank`（region_code=广州 × 最近3年；index 9 行等；全部 is_mock=1）——M2 §1.1–1.5；
- ⚠️ dim_score/indicator 广州行 region_name 误标「深圳」（M2 D-01）。

**演示备注**：能演示出结果（任务实算过渡态）；城市名以条件栏为准，若串名按 D-01 缺陷口径说明。

---

## CASE-VIT-07 · 东莞 × 最近3年（换城任务实算）

| 项 | 内容 |
|---|---|
| 用例名 | 区域切东莞 → 显式开始分析 → 任务实算 |
| 需规叶 | 135 指数计算与可视化 |

**前置条件**
- 东莞 × 最近3年行在库（M2 §1.1：东莞 index 9 行；is_mock=1 100%）。

**操作步骤**
1. 区域切「东莞」→ URL 变 `?region=东莞&compare=全国重点城市&window=3y&weight_profile=INDEX_MAIN`；
2. 观察回 config 待分析态；3. 点击「开始分析」；4. 完成后「查看分析结果」。

**期望结果**
- 任务实算东莞结果；排名榜含东莞行（rank_city=东莞）；完成不自动跳；`is_mock=1` 🧪；
- （对照M2修正）D-01 城市名展示风险同 CASE-VIT-06（`synth_vit_dim_score` / `synth_vit_indicator` 东莞行 region_name 误标「深圳」，城市名以条件栏为准）；
- **失败分支（单独列）**：任务失败 → 过程页失败阶段 +「重新尝试」，`failed` 批不被读取（同 CASE-VIT-15）。

**数据依赖**
- `ads.synth_vit_*`（region_code=东莞 × 最近3年；is_mock=1 100%）——M2 §1.1–1.5。

**演示备注**：能演示出结果（任务实算过渡态）；城市名以条件栏为准。

---

## CASE-VIT-08 · 惠州 × 最近3年（换城任务实算）

| 项 | 内容 |
|---|---|
| 用例名 | 区域切惠州 → 显式开始分析 → 任务实算 |
| 需规叶 | 135 指数计算与可视化 |

**前置条件**
- 惠州 × 最近3年行在库（M2 §1.1：惠州 index 9 行；is_mock=1 100%）。

**操作步骤**
1. 区域切「惠州」→ URL 变 `?region=惠州&compare=全国重点城市&window=3y&weight_profile=INDEX_MAIN`；
2. 观察回 config 待分析态；3. 点击「开始分析」；4. 完成后「查看分析结果」。

**期望结果**
- 任务实算惠州结果；排名榜含惠州行；完成不自动跳；`is_mock=1` 🧪；
- （对照M2修正）D-01 城市名展示风险同 CASE-VIT-06（惠州行 region_name 误标「深圳」，城市名以条件栏为准）；
- **失败分支（单独列）**：任务失败 → 过程页失败阶段 +「重新尝试」，`failed` 批不被读取（同 CASE-VIT-15）。

**数据依赖**
- `ads.synth_vit_*`（region_code=惠州 × 最近3年；is_mock=1 100%）——M2 §1.1–1.5。

**演示备注**：能演示出结果（任务实算过渡态）；城市名以条件栏为准。

---

## CASE-VIT-09 · 广州 × 最近5年（改窗+改区组合 → 404/引导）

| 项 | 内容 |
|---|---|
| 用例名 | 条件组合改窗+改区（广州 × 最近5年）待分析态引导 |
| 需规叶 | 135 指数计算与可视化（组合条件） |

**前置条件**
- 广州 × 最近5年 ADS **0 行**（M2 F1/G-01：全部城市 1y/5y 均无行）；
- 无该组合快照与预填。

**操作步骤**
1. 条件栏先切区域「广州」，再切时间窗「最近5年」→ URL 变 `?region=广州&compare=全国重点城市&window=5y&weight_profile=INDEX_MAIN`；
2. 观察结果区待分析态；3. 点击「开始分析」。

**期望结果**（对照M2修正）
- **主期望 = 404/引导分支**：无快照（`IntelBatchSnapshotNotFound`）→ no_batch/config 待分析态 → 显式「开始分析」；
- 总册原期望「非默认组合任务实算；同指纹当天复用单飞」按 M2 G-01 收敛：ADS 无该组合行 → 实算预期诚实空值/失败，**不承诺出数、不补 0**；
- 同指纹当天复用单飞机制仍成立（同条件二次进入直接恢复任务，无论成败）。

**数据依赖**
- `ads.synth_vit_*`（region_code=广州 × window_label='最近5年'）→ 0 行（M2 §1.1 G-01）。

**演示备注**：演示诚实空态/拦截——组合条件不预填、不自动起任务是本条核心。

> **（2026-11-08 更新：已闭合——见 SYNTH-DEMO-ACCEPT-LOOP.md R3）** 广州 5y 已出数（200，四城三窗全通），matrix 判定改 supported。

---

## CASE-VIT-10 · legacy_unknown 复用拦截（反例）

| 项 | 内容 |
|---|---|
| 用例名 | 历史旧三段任务 `legacy_unknown` 拦截（禁自动复用） |
| 需规叶 | 134 综合评价模型（任务指纹与档位识别） |

**前置条件**
- 任务中心存在历史旧三段指纹任务（冻结 params 无权重档 / `methodVersion` 信息，无法确认档位）；
- ⚠️ 任务中心为 Java 任务表（非 ADS），M2 未覆盖该表——演示前需人工确认存量旧任务在库；若无存量，本条登记「演示前置缺失」。

**操作步骤**
1. 打开工作台「分析记录」Tab（V15，leaf=vitality）；
2. 选择一条历史旧任务打开其结果（可展示）；
3. 回工作台，把条件设为与旧任务同 region/compare/window、权重档 INDEX_MAIN（或缺省）；
4. 观察结果源是否自动复用/当天单飞命中旧任务。

**期望结果**
- **`legacy_unknown` 拦截**（reason 值逐字保留）：旧任务历史结果可展示，但新 INDEX_MAIN 请求（含缺省归一）**禁止自动复用/当天单飞命中**，必须重新分析；
- 页面不得把旧任务当 INDEX_MAIN 档展示（不「顺手翻绿」、不改名 reason）；
- `legacy_unknown` 任务永不参与自动复用（总控 §1.4）。

**数据依赖**
- #103/#105 存量任务行（冻结 params 权重不可识别；非 ADS 表，M2 未覆盖）；
- 对照 `ads.synth_vit_*` 无对应 profile 批（旧任务产出行不参与新档快照选择，M2 F8：库内仅三正档）。

**演示备注**：演示拦截反例——依赖一条存量旧任务；若库中无旧任务，先如实登记缺失再演示或跳过。

---

## CASE-VIT-11 · 非法权重档 400 拦截（反例）

| 项 | 内容 |
|---|---|
| 用例名 | 非法权重档参数（`weight_profile=FOO`）400 拦截 |
| 需规叶 | 134 综合评价模型（参数校验边界） |

**前置条件**：无数据前置（参数校验分支，不触库写入）。

**操作步骤**
1. 浏览器地址栏直达 `/intelligence/vitality?region=深圳&compare=全国重点城市&window=3y&weight_profile=FOO`；
2. 观察结果区错误文案与网络面板状态码。

**期望结果**
- **400 拦截**：错误码 `WEIGHT_PROFILE_INVALID` → errorText 逐字「权重档参数非法（合法值 INDEX_MAIN / WEIGHT_MAIN / EQUAL）」；
- 不默改档位、不静默回落 INDEX_MAIN；不写任何表；`TEMP_*` 等未登记档同此拦截（库内 `TEMP_*` 0 行，M2 G-03）。

**数据依赖**
- 无表依赖（前端/接口参数校验分支）；对照 `ads.synth_vit_index.weight_profile_code` 枚举（M2：库内仅 INDEX_MAIN/EQUAL/WEIGHT_MAIN 三值）。

**演示备注**：演示拦截（可演示，零数据依赖，任意时候可跑）。

---

## CASE-VIT-12 · INDEX_MAIN ↔ EQUAL 换档不复用他档

| 项 | 内容 |
|---|---|
| 用例名 | 权重换档不复用他档任务/快照（四段指纹断言） |
| 需规叶 | 134 综合评价模型 |

**前置条件**
- 两档行并存（M2 F8：深圳 INDEX_MAIN / EQUAL 档位批均在库且为最新批）；
- 先以 EQUAL 档获得一次快照/任务（见 CASE-VIT-02）。

**操作步骤**
1. 在 EQUAL 档结果态（VIT-02）把权重档切回「INDEX_MAIN」→ URL 变 `weight_profile=INDEX_MAIN`；
2. 观察结果恢复来源（快照 or 本档任务）；3. 核对两档结果并存情况。

**期望结果**
- 换档**不复用**他档任务/快照（四段指纹 `region|compare|window|weight_profile` 断言生效）；
- INDEX_MAIN 命中本档快照/本档任务；两档结果并存互不覆盖；
- 回显档 = 实际计算档；`is_mock=1` 🧪；
- （对照M2修正）两档各按最新批次取数（深圳双批次冗余下取档位最新批，M2 D-02）。
- **404 分支（单独列）**：切回档无快照且无本档任务 → no_batch 引导「开始分析」。

**数据依赖**
- `ads.synth_vit_index` / `synth_vit_weight`（INDEX_MAIN 与 EQUAL 两 profile 行并存；M2 §1.1/§1.2）。

**演示备注**：能演示出结果；重点讲「档位隔离」语义。

---

## CASE-VIT-13 · 排名榜查看 + 点击切区（回 config）

| 项 | 内容 |
|---|---|
| 用例名 | 排名卡查看 + 点击「广州」切区回待分析态 |
| 需规叶 | 135 指数计算与可视化（排名） |

**前置条件**
- CASE-VIT-01 秒开态在场；
- `synth_vit_rank` 深圳市上下文 24 行（M2 F5：4 个 rank_city × 3 档 × 2 批次；深圳 rank1·is_current=1）。

**操作步骤**
1. 在 VIT-01 结果页定位排名卡（`vit-rank-card`）；
2. 核对当前区域（深圳）高亮「当前」标识与排序；
3. 点击排名行「广州」；
4. 观察 URL 与结果区状态变化。

**期望结果**
- 当前区域高亮「当前」（is_current=1 对应行）；排序与指数一致（深圳 rank1 → 广州 rank2 → 东莞 rank3 → 惠州 rank4）；
- 点击「广州」→ 回 config 待重分析态（不自动建任务、不串数据）；
- `is_mock=1` 🧪；
- **空态分支（单独列）**：若接口按 region 上下文查询 rank 表，非深圳上下文为 0 行（M2 G-02）——本用例为深圳上下文不受影响；东莞/广州/惠州上下文的排名视图预期 0 行诚实空态，不补 0。

**数据依赖**
- `ads.synth_vit_rank`（仅 region_code=深圳市 上下文 24 行；rank_city_code=广州 行存在）——M2 §1.5 / G-02。

**演示备注**：能演示出结果；点击切区后回到待分析态是预期行为，不是卡死。

---

## CASE-VIT-14 · 生成分析报告（报告页 + PDF）

| 项 | 内容 |
|---|---|
| 用例名 | 生成活力分析报告并下载 PDF |
| 需规叶 | 135 指数计算与可视化（结果输出） |

**前置条件**
- CASE-VIT-01 快照在场（instant 态带 snapshotId）或一条成功任务（任务态带父任务）。

**操作步骤**
1. 在 VIT-01 结果页点击「生成分析报告」→ 进入 `/intelligence/vitality/report`；
2. 核对报告段（四维/趋势/优劣）与标识；
3. 点击下载 PDF，本地打开核对；
4. （反分支）在无快照条件（如最近1年）下观察报告入口。

**期望结果**
- 任务态：带父任务建报告产物任务后进报告页；instant 态：带 snapshotId 直读快照；
- 报告页含四维/趋势/优劣段（`is_mock=1` 标识沿用至报告）；
- （对照M2修正）趋势段含 2022/2023「演示历史」年度行——趋势数据源 = `synth_vit_index` 历史年批（`mock_20261107_vit_trend_*`），**`synth_vit_trend` 表不存在**（M2 §1.6），依赖表名以本条为准；
- **快照缺失分支（单独列）**：无快照时报告入口禁用并说明，不伪造数据段、不生成空白 PDF 冒充。

**数据依赖**
- 消费 CASE-VIT-01 快照（活力四表最新批）；
- `ads.synth_vit_index`（year=2022/2023 历史年行，`is_mock=1`，「演示历史」）——M2 §1.1 / §1.6。

**演示备注**：能演示出结果；报告为 mock 过渡态，讲解时带 🧪 口径。

---

## CASE-VIT-15 · 任务失败分支（过程页失败态）

| 项 | 内容 |
|---|---|
| 用例名 | 任务过程页失败阶段 + 「重新尝试」 |
| 需规叶 | 135 指数计算与可视化（异常路径） |

**前置条件**
- 需要一条可复现/存量失败任务；（对照M2修正）**推荐触发路径 = CASE-VIT-05 的最近5年任务**：该窗 ADS 0 行（G-01），任务链实算预期失败，可作为本用例的确定性触发器；存量失败任务亦可（任务中心表非 ADS，M2 未覆盖）。

**操作步骤**
1. 按 CASE-VIT-05 步骤提交深圳 × 最近5年任务；
2. 在任务过程页等待至失败阶段（或从「分析记录」打开历史失败任务）；
3. 观察过程页失败文案、错误编号与按钮；
4. 点击「重新尝试」观察新任务受理。

**期望结果**
- 过程页失败阶段 + 错误编号（`errorMsg`）+「重新尝试」按钮；
- `failed` 批**不被结果源读取**（只认 succeeded）；不伪装秒开、不把失败批当结果展示；
- 重新尝试建立新任务（同四段指纹）。

**数据依赖**
- 任务表状态（#104 轮询；非 ADS，M2 未覆盖）；
- `ads.synth_vit_*` 无 failed 行读取语义（M2 §0.3：全库 calc_status 均 succeeded，失败态只存在于任务链）。

**演示备注**：演示诚实失败态——失败文案与「重新尝试」是预期交互，不是演示事故。

> **（2026-11-08 更新：已闭合——见 SYNTH-DEMO-ACCEPT-LOOP.md R3）** 5y/1y 均已出数，原「5y 空窗任务失败」触发路径失效——失败态改为**可选演示**（任务链失败态需另造触发，过程页行为），默认轮次不安排；matrix 判定改 supported。

---

## CASE-VIT-16 · 趋势卡查看（演示历史年度行）

| 项 | 内容 |
|---|---|
| 用例名 | 趋势图查看（2022–2024 + 「演示历史」标识） |
| 需规叶 | 135 指数计算与可视化（趋势） |

**前置条件**
- CASE-VIT-01 秒开态在场；
- `synth_vit_index` 2022/2023/2024 年行在库（M2 §1.1：2022:12 / 2023:12 / 2024:15，深圳 2024 双批次并存）。

**操作步骤**
1. 在 VIT-01 结果页定位趋势卡（`trendOption`）；
2. 读取年度点（2022/2023/2024）与同比值；
3. 核对「演示历史」标识与过渡行标注。

**期望结果**
- 统计年度 2022–2024：当前批 2024 + 过渡历史 2022/2023（历史年批 `mock_20261107_vit_trend_*`，`is_mock=1`，标「演示历史」）；
- 同比取最近两个年度点（2023 → 2024）计算；
- （对照M2修正）深圳 2024 双批次冗余：趋势点按 `year` 去重取最新行（`calc_batch_created_at` 最新，M2 D-02）；依赖表 = `synth_vit_index`（`synth_vit_trend` 不存在，M2 §1.6）；
- **无可比期分支（单独列）**：无可比年度时显示「暂无可比期」，不补 0、不画伪线。

**数据依赖**
- `ads.synth_vit_index`（year 列去重取最新行；2022/2023 历史批 + 2024 最新批；is_mock=1 100%）——M2 §1.1 / §1.6 / D-02。

**演示备注**：能演示出结果（趋势为 mock 演示历史）；讲解时明确「演示历史」为过渡演示数据。

---

## 附录 A · 对照 M2 修正索引（M3 以本册为准）

| CASE | 修正要点 | M2 依据 |
|---|---|---|
| CASE-VIT-01/02/03/12 | 快照读取按最新批次断言（深圳双批次冗余不得双值） | D-02 |
| CASE-VIT-04/05/09 | 非默认窗期望收敛为「404/引导开始分析」，不承诺出数（ADS 1y/5y = 0 行） | §0.2 / G-01 |
| CASE-VIT-06/07/08 | 补城市名展示风险注记（dim_score/indicator 非深圳行 region_name 误标「深圳」，城市名以条件栏为准） | D-01 |
| CASE-VIT-13 | 补非深圳上下文排名 0 行空态分支 | §1.5 / G-02 |
| CASE-VIT-14 | 趋势依赖表修正为 `synth_vit_index` 历史年行（`synth_vit_trend` 表不存在） | §1.6 |
| CASE-VIT-15 | 明确以 5y 空窗任务为失败触发路径 | G-01 |
| CASE-VIT-16 | 趋势按 year 去重取最新行 + 依赖表名修正 | §1.1 / §1.6 / D-02 |

## 附录 B · 本叶复核

- CASE 计数：**16 条**（CASE-VIT-01～16，与总册一致，零增删）；
- 每条含：用例名+需规叶 / 前置条件 / 操作步骤 / 期望结果（含 404/空态/失败分支与过渡标识）/ 数据依赖（含 M2 实际状态）/ 演示备注 六要素；
- reason 值保留清单：`IntelBatchSnapshotNotFound` / `legacy_unknown` / `WEIGHT_PROFILE_INVALID`（本叶涉及）。
