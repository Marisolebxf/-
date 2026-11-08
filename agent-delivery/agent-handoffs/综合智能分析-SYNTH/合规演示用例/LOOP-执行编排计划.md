# SYNTH 合规演示用例 · LOOP 执行编排计划（M5 产物）

- **任务 ID**：`SYNTH-DEMO-CASE-M5-ORCH-L01`（长任务 `SYNTH-DEMO-CASE-CTL-L01` 段 M5；architect 人格）
- **日期**：2026-11-07
- **总控真源**：`../SYNTH-合规演示用例-长任务总控.md`
- **上游产物**：`00-用例总册.md`（M1a）· `vitality-cases.md`（16）· `element-cases.md`（14）· `collab-cases.md`（17）（M1b）· `data-survey-20261107.md`（M2）· `condition-fill-matrix.yaml`（M3，47 条 = supported 36 / gap 5 / partial 6）
- **M4 交叉核对**：`gap-summary.md` 编写时未产出（M4 并行中），本计划缺口引用一律以 M3 矩阵 `gap_refs` 为准（详见 §5）；M4 产出后按 §5 清单回核编号即可，不回改本计划轮次结构。

## 状态行（LOOP 执行状态 · 每轮结束必须回写本节，不回写不算收尾）

| 项 | 值 |
|---|---|
| 模块 | 综合智能分析（活力 / 要素 / 协同） |
| 验收单 | `SYNTH-DEMO-ACCEPT-LOOP`（tech_task · qa-agent · 当前 **ready**，建单不认领） |
| 监管人 | `human:徐滕强`（当次会话真人，§6.5.7；`done` 操作人以 registry 闸门为准，§6.5.2 缺省 `human:淮政玮`） |
| token 文件 | `~/.gkx/topic-loop-token`（单行 access_token；请求头加 `systemCode: topic`；不进 git / handoff / 聊天） |
| 执行依据 | 《产品实现规程》§6.5（纯后端两段：只读库核对样本 + 带 token 调接口对照期望）· §6.5.7 监管人九步 |
| 对照物 | `condition-fill-matrix.yaml` 可演行 = supported 36 + 拦截分支 supported 3（gap 5 条不判通过，只做诚实空态演示核验；`覆盖不到` 归 DATA 缺口） |
| 当前状态 | **done（LOOP 完成，2026-11-08 10:22 签收）**——三条件齐备后按 §6.5.7 步 5/6 收尾：Q1 缺口单签收 done（监管人口令授权）；验收单 done（操作人 human:淮政玮，registry 已推 8e1c1f85）。全轮次记录见 handoff「运行」节。非阻塞尾巴：矩阵 M3 增补轮（gap 5 条改已闭合）、6 叶 definition 积压签收 |
| 最近一轮 | 2026-11-08 / R3 复测+签收收尾 / deploy:topic 绿 + 四城三窗全 200 / 无新缺口 / Q1→done、验收单→done / 完成 ✅ |

## 0. 编排原则（先读）

1. **合规演示 = 「能出结果的主演轮」+「诚实空态/拦截的验证轮」双结构**。主演轮展示产品能力，验证轮展示数据血缘诚实性（404 引导、拦截 reason、空态不补 0）——两者都是合规行为，验证轮不是演示事故。
2. **过渡标识必须出现在演示口径中**：凡出数画面，讲解词必含 `🧪 is_mock=1`（活力/要素/协同全部 ADS/gapfill 行）；137 四维必含「功能合规过渡 · pending_registration」；协同全叶必含 `dataSource=gapfill_transitional`；临时权重口径带 ⚠️「待甲方确认」角标（Q-SYNTH-01/V-01/V-02）。口头讲法统一：「这是带标识的过渡演示数据，不作为正式业务结论」。
3. **每条 CASE 只归属一轮**（本轮首次执行的唯一轮次）；**验证轮可含主演轮已演条目的复测项，复测必须标注「复测」且不改变归属**（本计划复测项：R6 内 ELEM-12 前的活力/要素空态对照口述、无跨轮重复执行项）。
4. **gap 用例（verdict=gap，5 条）一律不进主演轮**：VIT-04 / VIT-05 / VIT-09 / VIT-15 / ELEM-12 全部集中 R6 验证轮。partial 6 条允许进主演轮（主结果可出），其降级子区块按 §3.2 话术处理。
5. **切条件不自动建任务**（Q-ANALYSIS-01）：所有「开始分析」动作必须显式点击——这是每轮的隐性断言，禁止演示员替客户预点。
6. 页面状态依赖决定轮内顺序：先默认秒开、再改条件；任务结果态依赖任务完成；报告页依赖快照在场。
7. 每轮结束按退出条件核对后才进入下一轮；任一轮门禁失败先按 §4 排障，不跳轮硬闯。

---

## §1 轮次总览

**共 6 轮**：R1–R4 主演（覆盖 supported 36 + partial 6 = 42 条），R5–R6 验证（拦截类 3 条 + gap/空态类 8 条，含 partial 3 条——其主期望即 404/空态，天然属验证轮）。分轮理由：

- M3 分布为「活力 12s+4g / 要素 10s+3p+1g / 协同 14s+3p」，出数用例集中在默认三元组与 3y 窗，活力/要素 1y/5y 窗全空（G-01）——主演按「默认秒开 → 变窗换城 → 权重档 → 协同深链与报告」分层递进，与数据事实严格对应；
- 拦截类（R5）与数据空态类（R6）分离：R5 零/低数据依赖（参数校验、存量任务、只读坏快照）可灵活排期，R6 依赖 G-01 空窗数据事实与任务链失败触发路径，各自就绪门不同；
- 协同深链单列 R4：图谱筛选/相关性/策略/报告是操作链最长的一组，且 COLLAB-15 依赖 LLM 可用性分支选择，独立成轮便于就绪门（§4 第 4 条）生效。

| 轮号 | 主题 | CASE 集（归属清单） | 前置数据条件（表+批次状态） | 通过判定 | 退出条件 |
|---|---|---|---|---|---|
| **R1** | 默认三元组主演（三叶秒开 + 指数/四维/图谱主结果面） | VIT-01 · VIT-13 · VIT-14 · VIT-16 · ELEM-01 · ELEM-07 · ELEM-08 · ELEM-09 · ELEM-10 · ELEM-11 · COLLAB-01 · COLLAB-07 · COLLAB-13（**13 条，全 supported**） | 活力四表深圳 3y 最新批（`mock_20261106_vit_seed_*` 档位批）+ 历史年批 `mock_20261107_vit_trend_*` + rank 24 行；要素八表 3y 批 `mock_20261105_elem_seed` + ai 四维 48 行批 `mock_20261106_four_dim_seed` + DWD 四源表有行；协同 batch_meta 深圳 is_latest=`task:ANA-20261107-011` + gapfill 三表深圳行 | 三叶默认页全部秒开 200；全部画面带 🧪（137 四维另带 pending_registration、协同带 gapfill_transitional）；VIT-16 趋势 2022–2024；协同图谱节点/边以 API 实际返回为准 | 三叶默认页无红错、无串批双值（D-02 断言过）→ 面板巡检通过 |
| **R2** | 条件变窗主演（默认城市换窗/换城，supported 内非默认组合 + 任务链重跑语义） | VIT-06 · VIT-07 · VIT-08 · ELEM-04 · ELEM-05 · ELEM-06 · ELEM-14 · COLLAB-02 · COLLAB-03 · COLLAB-04 · COLLAB-05 · COLLAB-06（**12 条 = supported 9 + partial 3**） | 活力/要素四城 3y 行在库（index：深圳 12、广州/东莞/惠州各 9）；协同 gapfill：深圳 15（3 类）/广州 10（2 类）/东莞 5、惠州 5（单类）；东莞/惠州无 batch_meta（G-06） | 换城/换窗均回待分析态且不自动建任务；显式「开始分析」后任务实算出数（协同 1y/5y 可出、活力/要素 3y 换城可出）；ELEM-14 新旧 snapshotId 隔离断言过；城市名以条件栏为准（D-01 不作为数据错误讲解） | 12 条各自出数画面或任务完成态在场；co_project=0 等诚实 0 值按 §3 话术讲过 |
| **R3** | 权重档主演（活力两档 + 档位隔离） | VIT-02 · VIT-03 · VIT-12（**3 条，全 supported**） | `synth_vit_weight` 60 行三档齐（INDEX_MAIN/EQUAL/WEIGHT_MAIN，`TEMP_*` 0 行 G-03）；两档位批为最新批（`mock_20261106_vit_seed_equal` / `_weight_main` 系） | EQUAL/WEIGHT_MAIN 两档快照秒开且与 INDEX_MAIN 数值互不相同（四段指纹隔离）；换档不复用他档 | 两档画面 + 指纹隔离断言过 |
| **R4** | 协同深链 + 报告（产业筛选/集群复核/相关性/策略/报告 PDF） | COLLAB-08 · COLLAB-09 · COLLAB-10 · COLLAB-11 · COLLAB-12 · COLLAB-14 · COLLAB-15 · COLLAB-16（**8 条，全 supported**） | 深圳 3y 快照在场（R1 已核）+ relation_year 深圳行带 industry_code/industry_label；output_year 深圳 5 年序列（Pearson n=5）；LLM（gkx-zhipu-llm）可用性不限（两分支均可演） | 产业筛选服务端过滤重拉、前端叠加过滤统计同步；co_project=0 诚实 0 值；指数三卡+排名 4 城高亮；Pearson status=ok；策略建议两分支择一且全部待审核；报告七段式+PDF、不建报告任务 | COLLAB-16 PDF 本地打开成功 + 任务中心无新增报告任务行 |
| **R5** | 验证轮一（拦截类，零/低数据依赖）：legacy_unknown / WEIGHT_PROFILE_INVALID / batch_meta_missing | VIT-10 · VIT-11 · COLLAB-17（**3 条，全 supported 拦截分支**） | VIT-11 零表写入任意时候可跑（合法枚举对照 = 库内三正档 G-03）；COLLAB-17 只读分支（构造 `task:never_exists` 不存在 snapshotId，深圳/广州快照在场用于验证不回落）；VIT-10 依赖任务中心存量旧三段指纹任务（非 ADS，演示前人工确认，缺失则记「演示前置缺失」） | 400 WEIGHT_PROFILE_INVALID 逐字文案（不默改档不回落）；legacy_unknown reason 逐字 + 不自动复用/单飞命中；batch_meta_missing 逐字文案 + nodes=[]（禁回落最新批） | 三条拦截 reason 逐字保留、无静默回落，零表写入断言过 |
| **R6** | 验证轮二（gap/空态类：诚实空态 + 404/引导 + 失败态） | VIT-04 · VIT-05 · VIT-09 · VIT-15 · ELEM-02 · ELEM-03 · ELEM-12 · ELEM-13（**8 条 = gap 5 + partial 3**） | 活力/要素 ADS 全部表 1y/5y = **0 行**（G-01，空态数据事实）；`ai.synth_elem_four_dim_score` 三窗全齐（1y/5y 各 16 行，四维例外可出）；要素默认快照仍在场（ELEM-12/13 回默认态）；VIT-15 触发路径 = VIT-05 提交的 5y 任务在任务链失败（failed 只存在于任务链，全库 calc_status 均 succeeded） | 切窗不自动建任务 → 404（IntelBatchSnapshotNotFound 语义）→ no_batch 引导「开始分析」；ELEM-02/03 四维卡例外可出且带 pending_registration；VIT-15 过程页失败阶段 + errorMsg + 重新尝试；ELEM-12 趋势「暂无数据」不补 0；ELEM-13 报告不含趋势点 + 四维声明逐字 | 空态/拦截画面全部按 §3 话术讲完；任务失败文案在场且未被误读为事故 |

**归属计数核对**：R1 = 13（VIT-01/13/14/16 + ELEM-01/07/08/09/10/11 + COLLAB-01/07/13）；R2 = 12（VIT-06/07/08 + ELEM-04/05/06/14 + COLLAB-02/03/04/05/06）；R3 = 3（VIT-02/03/12）；R4 = 8（COLLAB-08/09/10/11/12/14/15/16）；R5 = 3（VIT-10/11 + COLLAB-17）；R6 = 8（VIT-04/05/09/15 + ELEM-02/03/12/13）。**13+12+3+8+3+8 = 47 ✅** 逐叶核对：VIT 16/16（R1×4 + R2×3 + R3×3 + R5×2 + R6×4）、ELEM 14/14（R1×6 + R2×4 + R6×4）、COLLAB 17/17（R1×3 + R2×5 + R4×8 + R5×1）——每条恰好归属一轮，零跨轮重复归属。

> 分轮偏差说明（对照派单参考分轮）：① ELEM-12（gap）按铁律从主演轮移入 R6 验证轮——其演示口径即诚实空态本身，与 VIT-04/05/09/15 同轮集中讲「为什么空态是合规行为」，话术更连贯；② VIT-10 / COLLAB-17 归位 R5 拦截轮（与派单参考分轮 R5 拦截类清单一致），避免主演轮混入反例打断出数叙事；③ ELEM-14（任务链重跑语义）归 R2 末尾——它依赖 R2 换城任务产生的成功任务作前置（叶册前置条件允许 ELEM-04/05/06 任务承接），紧随其后执行链路最短。

---

## §2 每轮执行脚本要点

### R1 · 默认三元组主演（预计 40 分钟）

**轮首数据核对清单（全部通过才开场）：**

```sql
-- ① 活力默认快照数据（最新档位批，深圳 3y）
SELECT COUNT(*) FROM demo_gkxlumenx_ads.synth_vit_index
 WHERE region_code='深圳市' AND window_label='最近3年';            -- 期望 = 12（2024 6 + 2022/2023 各 3，含双批次与历史年批）
SELECT COUNT(*) FROM demo_gkxlumenx_ads.synth_vit_index
 WHERE window_label='最近3年' AND year IN (2022,2023);             -- 期望 ≥ 24（VIT-16 趋势历史行，批 mock_20261107_vit_trend_*）
-- ② 要素默认批（单批无冗余）
SELECT COUNT(*) FROM demo_gkxlumenx_ads.synth_elem_index
 WHERE window_label='最近3年';                                     -- 期望 = 4（批 mock_20261105_elem_seed）
SELECT COUNT(*) FROM demo_gkxlumenx_ai.synth_elem_four_dim_score
 WHERE region_code='深圳市' AND window_label='最近3年';            -- 期望 = 4（批 mock_20261106_four_dim_seed）
-- ③ 全景 DWD 源（全域计数，实时聚合输入）
SELECT COUNT(*) FROM demo_gkxlumenx_ods.dwd_org_base_info WHERE is_deleted=0;          -- 期望 ≈ 189116
-- ④ 协同默认快照
SELECT COUNT(*) FROM demo_gkxlumenx_ads.synth_collab_batch_meta
 WHERE region_code='深圳市' AND is_latest=1;                       -- 期望 = 1（task:ANA-20261107-011）
SELECT COUNT(*) FROM demo_gkxlumenx_ads.gapfill_synth_collab_relation_year
 WHERE region_code='深圳市';                                       -- 期望 = 15（3 类 × 2021–2025）
```

**轮内 CASE 顺序（页面状态依赖）：**
1. VIT-01 秒开（默认页先到，一切后续状态机的起点）→ 2. VIT-13 排名卡（依赖 VIT-01 结果态在场）→ 3. VIT-16 趋势卡（同页，读 2022–2024）→ 4. VIT-14 报告页 + PDF（依赖 VIT-01 快照在场）→ 5. ELEM-01 秒开 → 6. ELEM-07 三透镜（依赖 ELEM-01 结果态）→ 7. ELEM-08 四维卡（同页）→ 8. ELEM-09 全景五类筛选（同页；非默认禁用分支只口述，实演归 R6 ELEM-02 承接）→ 9. ELEM-10 贡献路径 → 10. ELEM-11 排名 → 11. COLLAB-01 秒开 → 12. COLLAB-07 图谱 + 高亮（依赖 COLLAB-01 快照 snapshotId）→ 13. COLLAB-13 集群 + 孤立主体定位（依赖图谱在场）。
14. **轮尾注意**：R1 不含 gap 用例——要素趋势卡（ELEM-12）路过时不展开讲解，正式演示归 R6；活力页勿切窗，保持默认态收轮。

### R2 · 条件变窗主演（预计 50 分钟）

**轮首数据核对清单：**

```sql
-- ① 换城行齐（活力/要素四城 3y）
SELECT region_code, COUNT(*) FROM demo_gkxlumenx_ads.synth_vit_index
 WHERE window_label='最近3年' GROUP BY region_code;                -- 期望 深圳 12、广州/东莞/惠州各 9
SELECT COUNT(*) FROM demo_gkxlumenx_ads.synth_elem_index;          -- 期望 = 4（四城各 1）
-- ② 协同 gapfill 城市分布（R2 关系类型差异的事实依据）
SELECT region_code, COUNT(*) FROM demo_gkxlumenx_ads.gapfill_synth_collab_relation_year
 GROUP BY region_code;                                             -- 期望 深圳15/广州10/东莞5/惠州5
-- ③ 快照版图（东莞/惠州必须无快照——G-06 是 COLLAB-05/06 走实算路径的依据）
SELECT region_code, COUNT(*) FROM demo_gkxlumenx_ads.synth_collab_batch_meta
 GROUP BY region_code;                                             -- 期望 仅深圳(5)/广州(1) 有行
```

**轮内 CASE 顺序（换窗/换城都从默认态出发，显式开始分析）：**
1. VIT-06 广州（换城 → config 待分析态断言 → 开始分析 → 完成查看）→ 2. VIT-07 东莞 → 3. VIT-08 惠州（三城连讲 D-01 城市名以条件栏为准）→ 4. ELEM-04 广州 → 5. ELEM-05 东莞 → 6. ELEM-06 惠州 → 7. **ELEM-14 重新分析 force 重跑**（承接本轮成功任务：叶册前置允许 ELEM-04/05/06 任务承接；若按钮仅在默认条件露出，则以默认条件显式任务的产物承接，两种承接路径均为叶册口径）→ 8. COLLAB-02 深圳 1y（任务实算，发布 1y 快照）→ 9. COLLAB-03 深圳 5y（对比三窗图谱密度）→ 10. COLLAB-04 广州（快照命中秒开 + 无 talent_flow 降级话术）→ 11. COLLAB-05 东莞（无快照实算 + 单类关系话术）→ 12. COLLAB-06 惠州（同东莞口径）。

### R3 · 权重档主演（预计 20 分钟）

**轮首数据核对清单：**

```sql
SELECT weight_profile_code, COUNT(*) FROM demo_gkxlumenx_ads.synth_vit_weight
 GROUP BY weight_profile_code;       -- 期望 INDEX_MAIN/EQUAL/WEIGHT_MAIN 三档有行、TEMP_* 0 行（G-03）
SELECT COUNT(*) FROM demo_gkxlumenx_ads.synth_vit_index
 WHERE weight_profile_code='EQUAL' AND window_label='最近3年';      -- 期望 ≥ 9（四城三批年）
```

**轮内 CASE 顺序：**
1. VIT-02 EQUAL 档秒开（从 R1 默认态切档）→ 2. VIT-03 WEIGHT_MAIN URL 直达（先讲「下拉未露出」再直达）→ 3. VIT-12 EQUAL→INDEX_MAIN 换档不复用（依赖 VIT-02 在场，四段指纹断言）。

### R4 · 协同深链 + 报告（预计 35 分钟）

**轮首数据核对清单：**

```sql
-- ① 产业筛选字段在场
SELECT COUNT(*) FROM demo_gkxlumenx_ads.gapfill_synth_collab_relation_year
 WHERE region_code='深圳市' AND industry_code IS NOT NULL AND industry_code<>'';   -- 期望 ≥ 1
-- ② Pearson 输入（深圳 5 年序列）
SELECT COUNT(*) FROM demo_gkxlumenx_ads.gapfill_synth_collab_output_year
 WHERE region_code='深圳市';                                       -- 期望 = 5（n=5 ≥ 3 → status=ok）
-- ③ LLM 可用性人工核对：gkx-zhipu-llm 配置可达 → LLM 分支；不可达 → 确定性建议 ≥2 条降级分支（两分支均合规，见 §4 第 4 条）
```

**轮内 CASE 顺序：**
1. COLLAB-08 产业筛选（依赖 R1 图谱在场，服务端过滤重拉）→ 2. COLLAB-09 主体/关系类型前端叠加（依赖 COLLAB-08 复位「全部」）→ 3. COLLAB-10 网络统计三卡 + 关系输入（co_project=0 重点讲）→ 4. COLLAB-11 指数三卡 + 排名点击切区 → 5. COLLAB-12 趋势 2021–2025 → 6. COLLAB-14 相关性散点 Pearson → 7. COLLAB-15 策略建议（按轮首 LLM 核对结果选分支）→ 8. COLLAB-16 报告 + PDF（依赖深圳快照在场；东莞/惠州「先完成分析」反分支口述）。

### R5 · 验证轮一：拦截类（预计 15 分钟）

**轮首核对（零表写入，核对轻量）：**
- VIT-11：直达 URL 已备好（`weight_profile=FOO`）；
- VIT-10：任务中心「分析记录」人工点查存量旧三段指纹任务在场；缺失 → 本条记「演示前置缺失」按叶册口径说明，不编造旧任务；
- COLLAB-17：构造参数 `task:never_exists` 已备好；深圳/广州最新快照在场（用于验证「不回落」）。

**轮内 CASE 顺序：**
1. VIT-11（URL 直达 → 400 逐字文案；演示「任意时候可跑、零表写入」）→ 2. VIT-10（工作台分析记录 Tab → legacy_unknown 拦截逐字 + 新 INDEX_MAIN 请求禁自动复用/单飞命中）→ 3. COLLAB-17（携带不存在 snapshotId → HTTP 200 + nodes=[] + batch_meta_missing 逐字文案；断言深圳最新快照在场仍不回落）。

### R6 · 验证轮二：gap/空态类（预计 35 分钟）

**轮首数据核对清单（G-01 空窗事实必须在场，否则本轮主期望失效）：**

```sql
SELECT COUNT(*) FROM demo_gkxlumenx_ads.synth_vit_index   WHERE window_label='最近1年';  -- 期望 = 0
SELECT COUNT(*) FROM demo_gkxlumenx_ads.synth_vit_index   WHERE window_label='最近5年';  -- 期望 = 0
SELECT COUNT(*) FROM demo_gkxlumenx_ads.synth_elem_index  WHERE window_label='最近1年';  -- 期望 = 0
SELECT COUNT(*) FROM demo_gkxlumenx_ads.synth_elem_index  WHERE window_label='最近5年';  -- 期望 = 0
SELECT COUNT(*) FROM demo_gkxlumenx_ads.synth_collab_batch_meta WHERE window_label IN ('最近1年','最近5年'); -- 期望 = 0（1y/5y 无快照）
```

**轮内 CASE 顺序（VIT-05 提交的任务是 VIT-15 的失败态触发器）：**
1. VIT-04 深圳 1y（切窗不自动建任务 → 404/引导）→ 2. VIT-05 深圳 5y（同构 + **显式点击「开始分析」提交任务**，该任务即 VIT-15 的触发器）→ 3. VIT-09 广州 5y（组合条件不预填）→ 4. VIT-15 失败态（回到过程页等待步骤 2 任务进入失败阶段：errorMsg +「重新尝试」；failed 批不被结果源读取）→ 5. ELEM-02 深圳 1y（404/引导 + 四维卡例外可出带 pending_registration）→ 6. ELEM-03 深圳 5y（同构）→ 7. ELEM-12 要素趋势诚实空态（切回默认 3y 秒开态——要素默认快照仍在场；趋势卡「暂无数据」不补 0，与活力「演示历史」对照讲解）→ 8. ELEM-13 报告趋势段空态（依赖默认快照；报告不含趋势点 + 四维声明逐字 + 局限说明段口径）。

---

## §3 gap / partial 轮的降级策略（演示话术）

### 3.1 gap 5 条（VIT-04 / 05 / 09 / 15 / ELEM-12，全部 R6）：「为什么空态是合规行为」

统一话术骨架（40 秒版）：
> 「这个条件下库里没有可支撑的数据行——不是功能坏了，是**数据源还没覆盖这个窗口**（活力/要素 ADS 只有最近3年窗）。系统如实告诉我们『暂无结果，可开始分析』，而不是编一个数出来。这是数据血缘治理的要求：每个数字都要能追溯到源表，追溯不到就不显示。我们点『开始分析』，任务会诚实地计算并返回空值/失败，同样不伪造。」

分条要点：

| CASE | 场景 | 讲解要点（含缺口引用） |
|---|---|---|
| VIT-04 | 深圳 × 1y 切窗 | 404（IntelBatchSnapshotNotFound）→ no_batch 待分析态显式引导「开始分析」；**切条件不自动建任务**是第二个考点（Q-ANALYSIS-01）；引用缺口 G-01（活力 ADS 1y/5y 全 0 行）。若任务已实算：空值字段 null+reason 诚实展示，不补 0 |
| VIT-05 | 深圳 × 5y 切窗 | 同 VIT-04 话术；补充「本任务也是失败分支演示的触发器」——为下一镜（VIT-15）铺垫，把「可能失败」预告为设计行为 |
| VIT-09 | 广州 × 5y（组合条件） | 强调**组合条件也不预填**：改窗+改区后仍 404/引导；同指纹当天复用单飞机制依然成立（同条件二次进入直接恢复任务，无论成败） |
| VIT-15 | 过程页失败态 | 「失败态只存在于任务链，库里 calc_status 全部 succeeded——失败批永不被结果源读取」；errorMsg +「重新尝试」是预期交互，**不是演示事故**；重新尝试建立同指纹新任务 |
| ELEM-12 | 要素趋势卡（默认态） | 「暂无数据」不补 0、不画伪线；与活力叶对照讲解——活力补过 2022/2023 演示历史行（标「演示历史」），要素没有，**差异如实呈现**（引用 G-01：要素 ADS 无历史年行，趋势历史种子仅活力侧补过） |

### 3.2 partial 6 条：「哪块出数、哪块空态 + 过渡标识」

统一话术骨架（30 秒版）：
> 「这个页面主体能出结果，个别子区块的数据源还没覆盖，那块我们如实显示空态/收窄口径——出的数带过渡标识（🧪 / pending_registration / gapfill_transitional），空的地方不补。」

| CASE | 出数子区块 | 空态/降级子区块 + 讲法 | 缺口引用 |
|---|---|---|---|
| ELEM-02（R6） | 四维卡（ai 四维表 1y 16 行，唯一全窗数据面） | 指数/透镜/贡献/排名 ADS 面 → 404/引导 + 诚实空值；讲法：「四维是过渡表例外可出（带 pending_registration），ADS 面该窗无行如实空」 | G-01 |
| ELEM-03（R6） | 四维卡（5y 16 行同上） | 同 ELEM-02 | G-01 |
| ELEM-13（R6） | 全景/三透镜/四维/贡献/优劣段（消费默认快照） | 趋势段 →「报告不含趋势点」空态口径；四维段逐字声明「is_mock=1，pending_registration，不作为正式评价结论」；局限说明段念 Q-SYNTH-02 / Q-SYNTH-E-02 | G-01 |
| COLLAB-04（R2） | 快照秒开（task:ANA-20261107-006）+ co_patent/co_project 两类关系图谱 | 关系类型 talent_flow 缺 →「广州图谱比深圳少一类关系，是过渡数据的现状，如实呈现」；演示中不让观众误以为功能缺按钮 | G-05 |
| COLLAB-05（R2） | 任务实算出数 + 排名（四城派生）+ 孤立主体 2 个 | 图谱仅 co_patent 单类可筛 + 边数明显少于深圳（5 vs 15）→「单类图谱是数据事实不是功能缺陷」；无快照路径本身就是 G-06 的合规演示点（走实算并发布快照） | G-05 + G-06 |
| COLLAB-06（R2） | 同 COLLAB-05 结构 | 口径同东莞（单类关系 + 无快照任务路径）；失败分支 = 过程页失败 + 重新尝试 | G-05 + G-06 |

### 3.3 通用铁律

- 空态/拦截画面**禁止**：补 0、画伪线、伪造下拉选项、静默回落他批/他档、把 mock 说成真值；
- 所有出数画面的过渡标识（🧪 / ⚠️ / pending_registration / gapfill_transitional）按 §0 原则 2 口头+角标双呈现；
- partial 用例讲完降级子区块后，回到出数子区块收尾，避免以空态结束一镜（R2 协同三城、R6 要素四维例外均适用）。

---

## §4 演示前置就绪门（演示日开始前 checklist）

| # | 检查项 | 方法/SQL | 不通过时的处置 |
|---|---|---|---|
| 1 | 活力默认批在场且为最新档位批 | §2 R1 核对 ①；`SELECT MAX(calc_batch_created_at) FROM synth_vit_index WHERE region_code='深圳市' AND window_label='最近3年'` 与 `mock_20261106_vit_seed_*` 档位批时间对照 | 重跑种子或按 D-02 口径向演示员交底「页面按最新批取数」 |
| 2 | 深圳 index/weight/dim_score/indicator 无同键双值（D-02 断言） | 同键两批各查一行对比；页面不应出现同键双值 | 通知数据侧按 `calc_batch_created_at DESC` 口径修复查询；演示词加「取最新批」说明 |
| 3 | 要素默认批 + 四维过渡表 | §2 R1 核对 ② | 重灌 `mock_20261105_elem_seed` / `mock_20261106_four_dim_seed` |
| 4 | **LLM（gkx-zhipu-llm）可用性 → R4 COLLAB-15 分支选择** | 配置可达性探测 | 可用 → 演示证据锚定建议（全部待审核）；不可用 → 演示确定性事实建议 ≥2 条降级分支，话术：「降级建议是合规回退不是故障」（两分支都过验收） |
| 5 | 协同深圳/广州快照在场（报告 PDF 依赖） | `SELECT region_code, task_id FROM synth_collab_batch_meta WHERE is_latest=1` → 期望深圳 `task:ANA-20261107-011` + 广州 `task:ANA-20261107-006` | 缺失 → 先跑一次协同默认条件分析发布快照（COLLAB-01 路径），再开场；**报告页依赖快照存在性：无快照时报告入口禁用是预期分支，不得伪造 PDF** |
| 6 | 1y/5y 空窗事实（R6 主期望依据，G-01） | §2 R6 核对清单 = 全 0 | 若有人补灌了 1y/5y 行 → **变更 M3 判定前提**，暂停 R6 并回报总控，不得沿用本计划空态话术 |
| 7 | 东莞/惠州无快照（G-06 路径依据） | `SELECT region_code, COUNT(*) FROM synth_collab_batch_meta GROUP BY region_code` → 东莞/惠州 0 行 | 若出现快照 → COLLAB-05/06 改走秒开路径并在演示词注明与 M3 判定的偏差 |
| 8 | VIT-10 存量旧任务在场（legacy_unknown 前提，非 ADS 任务表） | 任务中心「分析记录」人工点查历史旧三段指纹任务 | 无存量 → VIT-10 记「演示前置缺失」，按叶册口径说明，不编造旧任务 |
| 9 | 三叶页面可达 + 全景 DWD 源行数正常 | 打开三叶默认 URL；§2 R1 核对 ③ | 超时/5xx → 检查服务与 AR-8 降级提示；演示词准备「超时降级为诚实空态」口径 |
| 10 | 城市名串显风险预演（D-01） | 在广州/东莞/惠州结果页观察 dim_score/indicator 区城市名 | 若串显「深圳」→ 按 M2 D-01 缺陷口径向演示员交底「城市名以条件栏为准」，不作为数据错误现场发挥 |

---

## §5 与缺口表交叉引用

**gap-summary.md 状态**：本计划编写时（2026-11-07）`gap-summary.md` 未产出（M4 并行中），本节清单以 **M3 矩阵 `gap_refs` 为唯一依据**；M4 产出后按本清单核对 §A 编号一致性即可，无需改本计划。

**本计划引用的 G 编号全集**（与 M3 矩阵一致，共 8 个）：

| 编号 | 引用处（本计划） | 用途 | 引用它的 M3 CASE（verdict 级） |
|---|---|---|---|
| G-01 | §1 R6 · §3.1 全部 gap 条 · §4 第 6 条 | 1y/5y 空窗数据事实（活力/要素 ADS 全表） | VIT-04 · VIT-05 · VIT-09 · VIT-15 · ELEM-02 · ELEM-03 · ELEM-12 · ELEM-13（8 条） |
| G-05 | §1 R2 · §3.2 COLLAB-04/05/06 行 | 东莞/惠州关系类型单类（无 co_project/talent_flow） | COLLAB-04 · COLLAB-05 · COLLAB-06（3 条） |
| G-06 | §1 R2 · §2 R2 核对 ③ · §3.2 COLLAB-05/06 行 · §4 第 7 条 | 东莞/惠州无 batch_meta 快照（走实算路径 + 报告入口禁用现场） | COLLAB-05 · COLLAB-06（2 条） |
| G-02 | §2 R1（ELEM-11 空态注记口径） | rank 仅深圳上下文，非深圳上下文 0 行为诚实空态 | （语义级，M3 未作 verdict 引用） |
| G-03 | §1 R3 · §2 R3 核对 · §2 R5 | TEMP_* 反例档 0 行；合法枚举对照三正档 | （语义级） |
| G-04 | §2 R4（COLLAB-10/11 判定口径） | 协同 ADS 六结果表全空 = 合规诚实态，展示走实时计算 | （语义级） |
| G-07 | §2 R4（COLLAB-10 讲解点） | co_project=0 值行 = 诚实 0 值展示（非空态非缺行） | （语义级） |
| G-08 | §2 R1（ELEM-09 全景口径） | 全景 DWD 源全域汇聚不按城过滤，换城计数不变属预期 | （语义级） |

- 数据缺陷 D-01 / D-02 / D-03 不进缺口引用（M3 口径：缺陷非缺口），仅体现在 §2/§4 的演示注记与就绪门（第 2、10 条）。
- Q-SYNTH-01 / V-01 / V-02（临时权重 ⚠️）、Q-SYNTH-02、Q-SYNTH-E-02、Q-SYNTH-C-02/C-03/C-04、Q-ANALYSIS-01 在 §0/§2/§3 作为口径引用，登记状态以《客户决策清单跟踪表》为准。
- M4 产出 `gap-summary.md` 后：核对本表 G-01（8 条）/ G-05（3 条）/ G-06（2 条）的 verdict 级引用与其 §A 归并结果一致；若 M4 新登记编号，归 M4 责任，不回填本计划。

---

## 附：本计划复核

- 轮次数：**6 轮**（R1–R4 主演 + R5–R6 验证）；
- CASE 覆盖：**47/47**，每条恰好归属一轮（R1=13、R2=12、R3=3、R4=8、R5=3、R6=8）；逐叶 VIT 16 / ELEM 14 / COLLAB 17 全覆盖，无重复归属、无遗漏；
- gap 5 条（VIT-04/05/09/15/ELEM-12）全部集中 R6 验证轮，零进入主演轮；partial 6 条分布 R2×3 / R6×3，降级话术见 §3.2；
- 依赖核对清单：轮首 SQL 核对 **16 组 SQL + R4 人工 1 项 = 17 项**（R1×4 组标签 7 条 SQL + R2×3 + R3×2 + R4×1 SQL + 1 人工 + R6×5 条查询）+ 就绪门 checklist **10 条**（§4，含 SQL 5 条 + 人工核对 5 条）；
- reason 逐字保留清单（本计划涉及）：`IntelBatchSnapshotNotFound` / `legacy_unknown` / `WEIGHT_PROFILE_INVALID` / `batch_meta_missing` / `no_year_on_source` / `cluster_rule_unclosed` / `insufficient` / `metric_not_registered` / `panorama_filtered_fetch_failed`；
- 铁律自检：只读输入 ✅（未改 matrix/叶册/registry）· 未 git 操作 ✅ · 47 条全覆盖且每条单轮归属 ✅ · gap 不进主演轮 ✅ · 复测项标注（本计划无跨轮复测执行项，仅 §2 R1 对 ELEM-12 注明「路过不展开」的规避口径）✅。
