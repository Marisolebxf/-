# SYNTH 合规演示用例 · 要素叶细化（CASE-ELEM-01～14）

- **日期**：2026-11-07
- **任务 ID**：`SYNTH-DEMO-CASE-M1-CASES-L01`（长任务 `SYNTH-DEMO-CASE-CTL-L01` 段 M1b；doc-agent 人格）
- **上游输入**：`00-用例总册.md`（M1a，CASE-ELEM-01～14 编号/条件/入口真源）；`data-survey-20261107.md`（M2 实库调研，2026-11-07）
- **铁律**：
  1. 编号不变（14 条 CASE-ELEM-01～14，与总册一一对应），不新增/改名/删除；
  2. 期望分支与代码一致：404 = `IntelBatchSnapshotNotFound`（no_batch 引导「开始分析」）；`metric_not_registered` / `panorama_filtered_fetch_failed` 等 reason 值逐字保留；
  3. 137 四维必带 `pending_registration` + `is_mock=1`；禁止编造数值、禁止把 mock 写成真值；
  4. **M3 以本册为准**：凡标注**（对照M2修正）**的条目为总册期望与 M2 实库事实矛盾/细化后的修正版（修正索引见文末附录 A）。

---

## 0. 本叶 M2 数据事实速览（细化期望的事实依据）

| # | 事实 | 出处 | 对用例的影响 |
|---|---|---|---|
| F1 | 要素 ADS 全部表 `window_label` 仅「最近3年」；1y/5y = **0 行** | M2 §0.2 / §2.0 / G-01 | 非默认窗用例（ELEM-02/03）期望收敛为 **404/引导开始分析** |
| F2 | `ai.synth_elem_four_dim_score`（137 四维过渡）**三窗全齐**（48 行 = 4 城 × 3 窗 × 4 维），`metric_status=pending_registration` 全表，score 无 NULL，region_name 正确 | M2 §2.9 | 四维卡是**唯一全窗口数据面**；任务实算在 1y/5y 窗四维卡仍可出（过渡态） |
| F3 | 要素 ADS 最新批统一 `mock_20261105_elem_seed`（单批次，无深圳双批次冗余）；「双行构成」= 同数据复制到 4 个 region_code | M2 §2.0–2.8 | 要素面无 D-02 问题；但四城数值同源（D-03） |
| F4 | 除 `synth_elem_index`（名称正确）与 `synth_elem_rank`（仅深圳上下文）外，其余 7 表**非深圳行 `region_name` 全部误标「深圳」**（region_code 正确） | M2 §2.0 / D-01 | 换城用例（ELEM-04/05/06/07）补城市名展示风险注记 |
| F5 | `synth_elem_rank` 仅 4 行、仅深圳市上下文（4 个排名城市行） | M2 §2.7 / G-02 | 排名用例（ELEM-11）按深圳上下文书写；非深圳上下文 0 行空态 |
| F6 | `synth_elem_index` 四城值 = 同一目标值 ± 扰动（仅一个指数口径，非独立计算） | M2 §0.5 / D-03 | 排名/换城用例不得当真实城市差异结论 |
| F7 | 全景 136 = DWD 实时汇聚（装包内聚合，无 ADS 表）：`dwd_org_base_info`（is_deleted=0 约 18.9 万）/ `dwd_research_institute_base_info`（2,074）/ `dwd_scholar`（21,316）/ `dwd_org_financing_info`（25,654）；空间类=园区关键词约 128 行；**不按城市过滤（全域汇聚）**，3 秒超时降级 AR-8 | M2 §2.10 / G-08 | 全景计数城市维度不构成缺口；换城后全景数值不变 |
| F8 | `synth_elem_indicator` status 混合 `ok/mock/proxy/degenerate`；`synth_elem_contrib` 32 行（caliber_flag 24 NULL + 8 行 `B`） | M2 §2.5 / §2.6 | 分项/贡献用例的诚实状态断言 |
| F9 | 全表 `is_mock=1` 100%；`calc_status` 全部 `succeeded` | M2 §0.3 | 出数用例必带 🧪 |

---

## CASE-ELEM-01 · 要素默认三元组秒开

| 项 | 内容 |
|---|---|
| 用例名 | 要素默认三元组秒开（深圳 × 全国重点城市 × 最近3年） |
| 需规叶 | 136 要素数据汇聚 / 137 要素评价模型 / 138 要素影响关联（需规 seq 136–138，Excel 行 137–139） |

**前置条件**
- `demo_gkxlumenx_ads` 要素 ADS 八表最近3年有深圳行（M2 F1/F3：全库仅最近3年窗，最新批 `mock_20261105_elem_seed`）；
- `demo_gkxlumenx_ai.synth_elem_four_dim_score` 深圳 × 最近3年 4 行在库（M2 F2）；
- 136 全景 DWD 四源表有行（M2 F7）。

**操作步骤**
1. 打开 `/intelligence/elements`；
2. 确认 URL 为 `?region=深圳&compare=全国重点城市&window=3y`（默认三元组，无 URL 时按 `SYNTH_DEFAULTS` 补齐）；
3. 不点击任何按钮，等待结果区渲染（instant 分支）。

**期望结果**
- 200：全景卡 + 综合指数仪表 + 三透镜指数卡 + 四维卡 + 贡献路径 + 排名 + 趋势 + 优势短板全部渲染；「预计算结果 · 跑批于」；
- 所有 mock 行带 🧪（`is_mock=1`）；快照按最新批次 `mock_20261105_elem_seed` 取数；
- 四维卡带「功能合规过渡 · pending_registration」标识 + `is_mock=1`（`M_SYNTH_ELEM_FOUR_DIM_SCORE`）；
- （对照M2修正）综合指数与排名为同一目标值 ± 扰动的演示数值（M2 D-03）：可演示，但讲解口径明确「非独立真实城市差异」。
- **404 分支（单独列）**：快照 404（`IntelBatchSnapshotNotFound`）→ no_batch 引导「开始分析」，不 fixture 填数。

**数据依赖**
- `ads.synth_elem_index`（4 行，每城 1 行，region_name 正确）——M2 §2.1；
- `synth_elem_type_score`（56 行）/ `synth_elem_level_score`（56 行）/ `synth_elem_domain_score`（20 行）/ `synth_elem_indicator`（108 行）/ `synth_elem_weight`（12 行）/ `synth_elem_contrib`（32 行）——M2 §2.2–2.6/§2.8；
- `synth_elem_rank`（4 行，仅深圳上下文）——M2 §2.7；
- `ai.synth_elem_four_dim_score`（48 行；`metric_status=pending_registration`，批 `mock_20261106_four_dim_seed`）——M2 §2.9；
- metric_id：`M_SYNTH_ELEM_TYPE_*` / `M_SYNTH_ELEM_FOUR_DIM_SCORE` 等（界面 ⓘ 触发）。

**演示备注**：能演示出结果——全部 mock 过渡态带 🧪；指数与四维卡讲解按过渡口径。

---

## CASE-ELEM-02 · 深圳 × 最近1年（非默认窗 → 404/引导开始分析）

| 项 | 内容 |
|---|---|
| 用例名 | 非默认窗（最近1年）待分析态引导 + 显式开始分析 |
| 需规叶 | 136 要素数据汇聚（时间窗选择） |

**前置条件**
- 要素 ADS 八表**无「最近1年」行**（M2 F1/G-01）；
- 无该窗预置快照；任务中心无同三段指纹当天成功任务。

**操作步骤**
1. 从默认秒开态把时间窗切「最近1年」→ URL 变 `?region=深圳&compare=全国重点城市&window=1y`；
2. 不点击按钮，观察结果区待分析态与「开始分析」按钮；
3. 点击「开始分析」→ 任务过程页（五阶段**要素文案**）；
4. 完成后点击「查看分析结果」。

**期望结果**（对照M2修正）
- **主期望 = 404/引导分支**：切窗后无快照 → 404（`IntelBatchSnapshotNotFound`）→ no_batch/config 待分析态 → 显式引导「开始分析」；切条件不自动建任务（Q-ANALYSIS-01）；
- **不承诺出数**：总册原期望「完成绑定任务快照出数」按 M2 G-01 收敛——要素 ADS 无 1y 行，指数/透镜/排名等 ADS 面在该窗预期诚实空值；
- **四维例外**：`ai.synth_elem_four_dim_score` 是三窗全齐的唯一数据面（M2 F2）——任务若实算成功，四维卡在该窗**仍可出**（`pending_registration` + `is_mock=1` 过渡态）；其余 ADS 面空值诚实展示，不补 0；
- 同指纹当天复用单飞成立。

**数据依赖**
- `ads.synth_elem_*` window_label='最近1年' → **0 行（M2 §2.0 G-01，空态依据）**；
- `ai.synth_elem_four_dim_score`（window_label='最近1年' 16 行在库，M2 §2.9）；
- 任务链表（#102–#105，非 ADS，M2 未覆盖）。

**演示备注**：演示诚实空态/拦截——404 引导是核心；四维卡若出数为过渡态例外，讲解时点明。

> **（2026-11-08 更新：已闭合——见 SYNTH-DEMO-ACCEPT-LOOP.md R3）** 1y 窗已出数（200，`mock_20261107_elem_delivery_1y`），matrix 判定改 supported；本节 404/引导期望为当时的诚实分支，保留作历史记录。

---

## CASE-ELEM-03 · 深圳 × 最近5年（非默认窗 → 404/引导开始分析）

| 项 | 内容 |
|---|---|
| 用例名 | 非默认窗（最近5年）待分析态引导 + 显式开始分析 |
| 需规叶 | 136 要素数据汇聚 |

**前置条件**：同 CASE-ELEM-02（5y 窗要素 ADS 0 行；`ai.synth_elem_four_dim_score` 5y 16 行在库）。

**操作步骤**
1. 时间窗切「最近5年」→ URL 变 `?region=深圳&compare=全国重点城市&window=5y`；
2. 观察待分析态；3. 点击「开始分析」；4.（延伸）完成后查看任务结果态。

**期望结果**（对照M2修正）
- 同 CASE-ELEM-02 结构：404（`IntelBatchSnapshotNotFound`）→ no_batch/config 引导 → 显式开始分析；
- ADS 面无 5y 行 → 诚实空值不补 0；四维卡例外同 ELEM-02（过渡态可出）。

**数据依赖**
- `ads.synth_elem_*` window_label='最近5年' → 0 行（M2 G-01）；
- `ai.synth_elem_four_dim_score`（5y 16 行，M2 §2.9）。

**演示备注**：演示诚实空态/拦截；四维例外讲解口径同 ELEM-02。

> **（2026-11-08 更新：已闭合——见 SYNTH-DEMO-ACCEPT-LOOP.md R3）** 5y 窗已出数（200，`mock_20261107_elem_delivery_5y`），matrix 判定改 supported。

---

## CASE-ELEM-04 · 广州 × 最近3年（换城任务实算）

| 项 | 内容 |
|---|---|
| 用例名 | 区域切广州 → 显式开始分析 → 任务实算 |
| 需规叶 | 136 要素数据汇聚（灵活选择区域） |

**前置条件**
- 要素 ADS 广州 × 最近3年行在库（M2 §2.1–2.8：广州各表行齐，is_mock=1 100%）；
- instant 仅默认三元组 → 换城回 config 待分析态。

**操作步骤**
1. 区域切「广州」→ URL 变 `?region=广州&compare=全国重点城市&window=3y`；
2. 观察回 config 待分析态；3. 点击「开始分析」；4. 完成后「查看分析结果」。

**期望结果**
- config → 显式开始分析 → 任务实算广州结果；排名榜含广州行；冻结三段指纹一致；
- 完成不自动跳；`is_mock=1` 🧪；
- （对照M2修正）**城市名展示风险**：除 index/rank 外的要素 7 表非深圳行 `region_name` 误标「深圳」（region_code 正确，M2 D-01）——页面若展示数据行内城市名可能串显「深圳」，城市名以条件栏为准；缺陷登记 M4 修复，演示不作为数据错误讲解口径；
- （对照M2修正）广州指数值 = 同一目标值 ± 扰动（M2 D-03），不得当真实城市差异结论。
- **失败分支（单独列）**：任务失败 → 过程页失败阶段 +「重新尝试」，`failed` 批不被读取。

**数据依赖**
- `ads.synth_elem_*`（region_code=广州 × 最近3年）——M2 §2.1–2.8；
- ⚠️ 7 表广州行 region_name 误标（M2 D-01）；广州 index 行 region_name 正确（M2 §2.1）。

**演示备注**：能演示出结果（任务实算过渡态）；城市名以条件栏为准。

---

## CASE-ELEM-05 · 东莞 × 最近3年（换城任务实算）

| 项 | 内容 |
|---|---|
| 用例名 | 区域切东莞 → 显式开始分析 → 任务实算 |
| 需规叶 | 136 要素数据汇聚 |

**前置条件**
- 要素 ADS 东莞 × 最近3年行在库（M2 §2.1–2.8：东莞各表行齐，is_mock=1 100%）。

**操作步骤**
1. 区域切「东莞」→ URL 变 `?region=东莞&compare=全国重点城市&window=3y`；
2. 观察回 config 待分析态；3. 点击「开始分析」；4. 完成后「查看分析结果」。

**期望结果**
- config → 显式开始分析 → 任务实算东莞结果；完成不自动跳；`is_mock=1` 🧪；
- （对照M2修正）D-01 城市名展示风险与 D-03 数值口径同 CASE-ELEM-04（东莞行 region_name 误标「深圳」，城市名以条件栏为准；指数值同源 ± 扰动）；
- **失败分支（单独列）**：任务失败 → 过程页失败阶段 +「重新尝试」，`failed` 批不被读取。

**数据依赖**
- `ads.synth_elem_*`（region_code=东莞 × 最近3年；is_mock=1 100%）——M2 §2.1–2.8。

**演示备注**：能演示出结果；城市名以条件栏为准。

---

## CASE-ELEM-06 · 惠州 × 最近3年（换城任务实算）

| 项 | 内容 |
|---|---|
| 用例名 | 区域切惠州 → 显式开始分析 → 任务实算 |
| 需规叶 | 136 要素数据汇聚 |

**前置条件**
- 要素 ADS 惠州 × 最近3年行在库（M2 §2.1–2.8：惠州各表行齐，is_mock=1 100%）。

**操作步骤**
1. 区域切「惠州」→ URL 变 `?region=惠州&compare=全国重点城市&window=3y`；
2. 观察回 config 待分析态；3. 点击「开始分析」；4. 完成后「查看分析结果」。

**期望结果**
- config → 显式开始分析 → 任务实算惠州结果；完成不自动跳；`is_mock=1` 🧪；
- （对照M2修正）D-01 城市名展示风险与 D-03 数值口径同 CASE-ELEM-04（惠州行 region_name 误标「深圳」，城市名以条件栏为准；指数值同源 ± 扰动）；
- **失败分支（单独列）**：任务失败 → 过程页失败阶段 +「重新尝试」，`failed` 批不被读取。

**数据依赖**
- `ads.synth_elem_*`（region_code=惠州 × 最近3年；is_mock=1 100%）——M2 §2.1–2.8。

**演示备注**：能演示出结果；城市名以条件栏为准。

---

## CASE-ELEM-07 · 三透镜切换（type / level / domain）

| 项 | 内容 |
|---|---|
| 用例名 | 三透镜切换：类型·七要素表 / 层次·结构达标表 / 领域·覆盖表 |
| 需规叶 | 136 要素数据汇聚（分类结构） |

**前置条件**
- CASE-ELEM-01 秒开态在场（深圳 × 3y）；
- type_score 56 行（深圳 14 行 = 7 类型 T-ENT/T-FUN/T-POL/T-RSI/T-SPA/T-SRV/T-TAL × INDEX/SCORE 2 行）、level_score 56 行（7 层次 L-*）、domain_score 20 行（5 领域 D1-COV/D2-TEC/D3-OUT/D4-TAL/D5-ECO）、indicator 108 行（lens=type 68 + lens=domain 40；status 混合）。

**操作步骤**
1. 在 ELEM-01 结果页定位透镜切换器，点「类型」→ URL 变 `&lens=type`；核对类型·七要素表；
2. 点「层次」→ `&lens=level`；核对层次·结构达标表（成熟度/均衡度/达标 Tag）；
3. 点「领域」→ `&lens=domain`；核对领域·覆盖表（产业 × 技术 × 得分）。

**期望结果**
- 三透镜逐一切换渲染对应表；深圳上下文 region_name 无误标风险（M2 F4：误标仅非深圳行）；
- 分项表 status 诚实展示（`ok/mock/proxy/degenerate` 混合，M2 F8）——mock/proxy/degenerate 行不冒充 ok；
- 缺行 → null「暂无数据」，不补 0；
- `is_mock=1` 🧪。
- **空态分支（单独列）**：某透镜无对应行 → 该透镜表「暂无数据」+ 诚实 reason，不串用其他透镜数据。

**数据依赖**
- `ads.synth_elem_type_score`（INDEX/SCORE 两 metric 同表，56 行）/ `synth_elem_level_score`（56 行）/ `synth_elem_domain_score`（20 行）/ `synth_elem_indicator`（108 行，双透镜）——M2 §2.2–2.5。

**演示备注**：能演示出结果；重点讲「同一数据三个结构视角」与 status 诚实性。

---

## CASE-ELEM-08 · 137 四维打分卡（pending_registration 过渡）

| 项 | 内容 |
|---|---|
| 用例名 | 四维打分卡查看（规模/质量/结构/活跃度，pending_registration 过渡态） |
| 需规叶 | 137 要素评价模型（四维量化打分） |

**前置条件**
- CASE-ELEM-01 秒开态在场；
- `ai.synth_elem_four_dim_score` 深圳 × 全国重点城市 × 最近3年 4 行在库（scale/quality/structure/activity 各 1 行；score 无 NULL；批 `mock_20261106_four_dim_seed`；region_name 正确）。

**操作步骤**
1. 在 ELEM-01 结果页定位四维打分卡区（`evaluationDimensions`）；
2. 逐卡读取四维名称与分值；
3. 核对过渡标识与 ⓘ（`M_SYNTH_ELEM_FOUR_DIM_SCORE`）。

**期望结果**
- 四卡 scale / quality / structure / activity 有分值（48/48 无 NULL，M2 F2）；
- **必带「功能合规过渡 · pending_registration」标识 + `is_mock=1`**（页面与报告同段声明）；禁当正式结论；
- （对照M2修正）本表为**三窗全齐的唯一数据面**（M2 §2.9）：在最近1年/最近5年窗任务实算后四维卡同样可出（关联 CASE-ELEM-02/03）；region_name 无赋名缺陷；
- **缺表分支（单独列）**：过渡表无行时 → 四卡「暂无数据」+ `metric_not_registered`（reason 值逐字保留），不伪补四维分。

**数据依赖**
- `ai.synth_elem_four_dim_score`（48 行 seed；`metric_status=pending_registration`、`fill_method=demo_index_offset`）——M2 §2.9。

**演示备注**：能演示出结果（过渡态）——演示重点是「带标识的过渡结论」而非分值本身。

---

## CASE-ELEM-09 · 要素全景卡 + 分类筛选（E3/E4）

| 项 | 内容 |
|---|---|
| 用例名 | 要素全景卡查看 + 五类分类筛选（企业/机构/人才/资金/空间） |
| 需规叶 | 136 要素数据汇聚（全景库） |

**前置条件**
- CASE-ELEM-01 秒开态在场（默认三元组——**分类筛选仅默认条件可用**）；
- DWD 四源表有行（M2 F7：企业约 18.9 万 / 机构 2,074 / 人才 21,316 / 资金 25,654；空间类园区关键词约 128 行）。

**操作步骤**
1. 在 ELEM-01 结果页定位全景卡，读取五类计数 + TopN + total_count；
2. 依次点击「企业」「机构」「人才」「资金」「空间」分类筛选（real 模式带 `element_types` 重拉快照，锁 `snapshotId`）；
3. （反分支）切到非默认条件（如最近1年）观察筛选器；
4. （反分支）断网或上游超时再点筛选。

**期望结果**
- 五类计数 + TopN + total_count 渲染（真实 DWD 汇聚，无 ADS 表）；
- 逐类筛选带 `element_types` 重拉，锁 `snapshotId`；筛选后计数与 TopN 同步更新；
- **非默认条件筛选禁用**（`filterDisabled`）并提示「全景分类筛选仅系统默认条件可用；当前条件请先完成分析后再筛选」；
- 失败分支（单独列）：筛选重拉失败 → 诚实空态 + reason **`panorama_filtered_fetch_failed`** + 警告提示，不 500、不 fixture；
- 超时降级（AR-8，3 秒）→ `panoramaReason` 诚实空态；
- （对照M2修正）**全景为全域汇聚、不按城市过滤**（M2 G-08）：换城后全景计数不变属预期行为，城市维度不构成缺口；不得演示/承诺「按城市过滤的全景计数」。

**数据依赖**
- DWD 汇聚源（`demo_gkxlumenx_ods.dwd_org_base_info` / `dwd_research_institute_base_info` / `dwd_scholar` / `dwd_org_financing_info`；装包内实时聚合，无 ADS 表）——M2 §2.10。

**演示备注**：能演示出结果（全域口径）——计数是实时聚合的量大面宽数据，讲解时说明「全域汇聚」。

---

## CASE-ELEM-10 · 贡献路径查看（138，仅关联非因果）

| 项 | 内容 |
|---|---|
| 用例名 | 贡献路径查看（要素 → 对象 + 百分比） |
| 需规叶 | 138 要素影响关联（贡献度与影响路径） |

**前置条件**
- CASE-ELEM-01 秒开态在场；
- `synth_elem_contrib` 深圳 8 行在库（4 要素 ENT/FUN/RSI/TAL × 2 行；caliber_flag 6 NULL + 2 行 `B`）。

**操作步骤**
1. 在 ELEM-01 结果页定位贡献路径区（`contributions[]`）；
2. 逐行读取 element → target + 百分比；
3. 核对口径标注与 ⓘ（`M_SYNTH_ELEM_CONTRIB`）。

**期望结果**
- `contributions[]` 列表渲染（element → target + 百分比）；
- **仅关联表述、禁因果**（Q-SYNTH-E-02 🟡；文案不得出现「导致/因果」类表述）；
- caliber_flag `B` 行按 B 口径诚实标注（M2 F8）；
- `is_mock=1` 🧪。
- **空列表分支（单独列）**：无贡献行 → 诚实空态不填伪路径。

**数据依赖**
- `ads.synth_elem_contrib`（32 行；caliber_flag 24 NULL + 8 行 B）——M2 §2.6。

**演示备注**：能演示出结果；讲解口径强调「份额分解非因果」。

---

## CASE-ELEM-11 · 排名查看 + 点击切区（回 config）

| 项 | 内容 |
|---|---|
| 用例名 | 要素排名查看 + 点击「广州」切区回待分析态 |
| 需规叶 | 138 要素影响关联（排名参照） |

**前置条件**
- CASE-ELEM-01 秒开态在场；
- `synth_elem_rank` 深圳市上下文 4 行在库（4 个排名城市行，region_name 正确）。

**操作步骤**
1. 在 ELEM-01 结果页定位排名卡；
2. 核对当前区域「（当前）」标识与排序；
3. 点击排名行「广州」；4. 观察 URL 与结果区状态。

**期望结果**
- 当前区域「（当前）」标识；排序与综合指数一致；
- 点击「广州」→ 回 config 待重分析态（不自动建任务）；
- `is_mock=1` 🧪；（对照M2修正）四城排序值为同源 ± 扰动演示值（M2 D-03）。
- **空态分支（单独列）**：接口按 region 上下文查询时，非深圳上下文排名 0 行（M2 G-02）——东莞/广州/惠州上下文的排名视图为诚实空态，不补 0。

**数据依赖**
- `ads.synth_elem_rank`（仅 region_code=深圳市 上下文 4 行）——M2 §2.7 / G-02。

**演示备注**：能演示出结果；点击切区回待分析态是预期行为。

---

## CASE-ELEM-12 · 趋势查看（默认态诚实空态）

| 项 | 内容 |
|---|---|
| 用例名 | 要素趋势卡查看 |
| 需规叶 | 136 要素数据汇聚（趋势维度） |

**前置条件**
- CASE-ELEM-01 秒开态在场；
- `synth_elem_index` 深圳仅 1 行（最近3年当年行；**无 2022/2023 历史年行**——趋势历史种子仅活力侧补过，M2 §2.1）。

**操作步骤**
1. 在 ELEM-01 结果页定位趋势卡（trendOption）；
2. 观察趋势点与空态文案。

**期望结果**（对照M2修正）
- **主期望 = 诚实空态**：要素 ADS 无历史年行（`synth_elem_index` 每城仅 1 行当年行，M2 §2.1）→ 趋势卡显示「暂无数据」，不补 0、不画伪线；
- 总册原期望「趋势点按实算/预填批年度」按 M2 收敛：仅任务实算产生多年度点时才出趋势（当前 seed 无此批），默认秒开态不出趋势点；
- 与活力叶不同：**活力有 2022/2023 演示历史行，要素没有**——演示时不要把活力趋势口径套到要素叶。

**数据依赖**
- `ads.synth_elem_index`（4 行，每城 1 行，无历史年行）——M2 §2.1 / G-01。

**演示备注**：演示诚实空态——「暂无数据」是本条预期结果，不是演示事故；可对比活力叶趋势演示讲解差异。

> **（2026-11-08 更新：已闭合——见 SYNTH-DEMO-ACCEPT-LOOP.md R3/R2）** 要素历史年行已补（`mock_20261107_elem_hist_*`），趋势卡出数 [2022,2023,2024]，matrix 判定改 supported；本节「暂无数据」期望为当时的诚实分支，保留作历史记录。

---

## CASE-ELEM-13 · 生成分析报告（前端渲染 PDF）

| 项 | 内容 |
|---|---|
| 用例名 | 生成要素分析报告并下载 PDF |
| 需规叶 | 138 要素影响关联（结果输出） |

**前置条件**
- CASE-ELEM-01 快照在场（instant 带 snapshotId）或成功任务态。

**操作步骤**
1. 在 ELEM-01 结果页点击「生成分析报告」→ 进入要素报告页；
2. 核对报告段（全景/三透镜/四维/贡献/趋势/优劣）与声明文案；
3. 下载 PDF 本地打开核对；
4. （反分支）在无快照条件（如最近1年）观察报告入口。

**期望结果**
- 报告页含全景/三透镜/四维/贡献/趋势/优劣段；
- 四维段必含逐字声明：「四维评价来自 _ai 过渡结果（is_mock=1，pending_registration），仅用于功能合规展示，不作为正式评价结论。」；
- 局限说明段含：指数结果来自 ADS 跑批快照（D4 当前为 mock 档）＋综合合成等权 1/3×3 为临时默认（Q-SYNTH-02）＋贡献路径为份额分解非因果（Q-SYNTH-E-02）；
- （对照M2修正）趋势段按要素实际数据面书写：无历史年行时报告不含趋势点（同 CASE-ELEM-12 空态口径）；四维过渡表无行时报告显示「四维过渡表暂无可用行，报告不含四维结论」；
- PDF 前端本地生成；**快照缺失分支（单独列）**：无快照报告入口禁用，不伪造数据段。

**数据依赖**
- 消费 CASE-ELEM-01 快照（要素八表最新批 `mock_20261105_elem_seed`）；
- `ai.synth_elem_four_dim_score`（四维段声明依据，M2 §2.9）。

**演示备注**：能演示出结果；报告为 mock 过渡态，逐段讲解声明文案。

> **（2026-11-08 更新：已闭合——见 SYNTH-DEMO-ACCEPT-LOOP.md R3/R2）** 历史年行补齐后报告趋势段有数据（趋势 [2022,2023,2024]），「不含趋势点」空态口径失效，matrix 判定改 supported；四维声明与局限说明口径不变。

---

## CASE-ELEM-14 · 任务态「重新分析」force 重跑

| 项 | 内容 |
|---|---|
| 用例名 | 任务态「重新分析」（force 重跑，新批次快照） |
| 需规叶 | 137 要素评价模型（任务链重跑语义） |

**前置条件**
- 已有一条成功任务（可由 CASE-ELEM-04/05/06 或默认条件任务产生）；
- 「重新分析」按钮仅在 mode=task 且默认条件时露出（`onStartAnalysis(true)`）。

**操作步骤**
1. 打开一条成功任务的结果态（URL `mode=result&task_id=...`）；
2. 点击「重新分析」；
3. 等待新任务完成，进入新结果态；
4. 对比新旧 `snapshotId` / `calc_batch_id`。

**期望结果**
- 同指纹新批次任务建立；新 `snapshotId` ≠ 旧 `snapshotId`；
- 旧 snapshotId 仍可回溯（显式批可回查，不串批）；
- `is_latest` 改指新批；旧批结果不被覆盖删除；
- `is_mock=1` 🧪。
- **失败分支（单独列）**：重跑失败 → 过程页失败阶段 +「重新尝试」，旧快照仍是可回退的最新成功批。

**数据依赖**
- 任务链 + `ads.synth_elem_*` 重跑新批语义（重跑批为新 `calc_batch_id`，M2 §2.0 批次结构）。

**演示备注**：能演示出结果；重点讲「A/B 批隔离与旧批可回溯」。

---

## 附录 A · 对照 M2 修正索引（M3 以本册为准）

| CASE | 修正要点 | M2 依据 |
|---|---|---|
| CASE-ELEM-01 | 补 D-03 数值口径注记（同源 ± 扰动演示值，不当真实差异） | D-03 |
| CASE-ELEM-02/03 | 非默认窗期望收敛为「404/引导开始分析」，ADS 面不承诺出数；四维卡为全窗口唯一数据面例外（过渡态可出） | §2.0 G-01 / §2.9 |
| CASE-ELEM-04/05/06 | 补 D-01 城市名展示风险 + D-03 数值口径注记 | D-01 / D-03 |
| CASE-ELEM-08 | 补「三窗全齐唯一数据面」结论与缺表分支依据 | §2.9 |
| CASE-ELEM-09 | 全景为全域汇聚不按城市过滤（换城计数不变属预期），不承诺按城筛选 | §2.10 / G-08 |
| CASE-ELEM-11 | 补非深圳上下文排名 0 行空态 + D-03 注记 | §2.7 G-02 / D-03 |
| CASE-ELEM-12 | 主期望修正为「暂无数据」诚实空态（要素 ADS 无历史年行，与活力不同） | §2.1 |
| CASE-ELEM-13 | 趋势段按实际数据面收敛（无历史年行不出趋势点）+ 四维声明逐字化 | §2.1 / §2.9 |

## 附录 B · 本叶复核

- CASE 计数：**14 条**（CASE-ELEM-01～14，与总册一致，零增删）；
- 每条含：用例名+需规叶 / 前置条件 / 操作步骤 / 期望结果（含 404/空态/失败分支与过渡标识）/ 数据依赖（含 M2 实际状态）/ 演示备注 六要素；
- reason 值保留清单：`IntelBatchSnapshotNotFound` / `metric_not_registered` / `panorama_filtered_fetch_failed`（本叶涉及）；标识保留清单：`pending_registration` / `is_mock=1`。
