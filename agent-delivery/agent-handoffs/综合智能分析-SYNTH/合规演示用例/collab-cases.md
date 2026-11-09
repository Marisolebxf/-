# SYNTH 合规演示用例 · 协同叶细化（CASE-COLLAB-01～17）

- **日期**：2026-11-07
- **任务 ID**：`SYNTH-DEMO-CASE-M1-CASES-L01`（长任务 `SYNTH-DEMO-CASE-CTL-L01` 段 M1b；doc-agent 人格）
- **上游输入**：`00-用例总册.md`（M1a，CASE-COLLAB-01～17 编号/条件/入口真源）；`data-survey-20261107.md`（M2 实库调研，2026-11-07）
- **铁律**：
  1. 编号不变（17 条 CASE-COLLAB-01～17，与总册一一对应），不新增/改名/删除；
  2. 期望分支与代码一致：`batch_meta_missing`（禁回落最新批）/ `no_year_on_source` / `cluster_rule_unclosed` / `graph_request_rejected` / `graph_upstream_unavailable` 等 reason 值逐字保留；404 = `IntelBatchSnapshotNotFound`（no_batch 引导「开始分析」）；
  3. 协同 ADS 六结果表全空（M2 G-04）→ 全部展示面走 **`gapfill_transitional` + 实时计算**路径，禁止按「查 ADS 结果表」写期望；禁止编造数值、禁止把 mock 写成真值；
  4. **M3 以本册为准**：凡标注**（对照M2修正）**的条目为总册期望与 M2 实库事实矛盾/细化后的修正版（修正索引见文末附录 A）。

---

## 0. 本叶 M2 数据事实速览（细化期望的事实依据）

| # | 事实 | 出处 | 对用例的影响 |
|---|---|---|---|
| F1 | 协同 ADS 六结果表全空：`synth_collab_node` / `edge` / `network_stat` / `index` / `output_corr` / `cluster` 均 **0 行** | M2 §3.4 / G-04 | 图谱/网络/指数/相关性一律按**实时计算 + gapfill 输入**路径演示；响应必带 `dataSource=gapfill_transitional` |
| F2 | `gapfill_synth_collab_relation_year` 35 行：**深圳 15**（2021–2025 × 3 关系类型）/ **广州 10**（co_patent+co_project）/ **东莞 5、惠州 5**（仅 co_patent）；`source_has_year` 全 0（模拟无年份真源回填）；批 `mock_20261106_collab_gapfill_seed` | M2 §3.1 / G-05 | 四城三窗任务链均可按 event_year 回推实算；东莞/惠州图谱关系类型仅单类可筛 |
| F3 | `gapfill_synth_collab_output_year` 20 行（四城 × 2021–2025 各 1 行；collab_score 逐年上升）；`gapfill_synth_collab_isolate_year` 8 行（四城 × 2 实体：独立研究所C + 独立服务机构C，connection_count=0） | M2 §3.2 / §3.3 | 相关性 Pearson n=5（status=ok 可出）；孤立主体每城 2 个 |
| F4 | `synth_collab_batch_meta` 6 行：`is_latest=1` 仅**深圳市**（`task:ANA-20261107-011`）/ **广州市**（`task:ANA-20261107-006`），`calc_batch_id` 均 = `gapfill_transitional`；深圳另有 4 条历史快照；**东莞/惠州无任何快照；1y/5y 窗无快照** | M2 §3.6 / G-06 | 秒开仅深圳/广州 × 3y；报告用例限这两城；坏快照用例用无映射 snapshotId |
| F5 | `synth_collab_relation_input` 仅深圳 × 最近3年 3 行：co_patent 6477 / **co_project 0** / talent_flow 18553（co_project 为 0 值行） | M2 §3.5 / G-07 | 关系输入三卡深圳可出；co_project=0 为诚实 0 值展示分支 |
| F6 | 全 gapfill/seed 表 `is_mock=1` 100%；`batch_meta` 无 is_mock 列（快照元数据非数据行） | M2 §0.3 | 出数用例必带 🧪 |
| F7 | 节点/边数「8 节点/9 边」为审计文（需规功能一致性审计-20261107 §139）当日接口实测记录；M2 未复测 API 返回 | M2 §7 / 审计文逐叶对账 | 图谱用例期望写「以 API 实际返回为准，审计文记录 8 节点/9 边」；空图 reason 分支单独列 |

---

## CASE-COLLAB-01 · 协同默认三元组秒开（gapfill 过渡快照）

| 项 | 内容 |
|---|---|
| 用例名 | 协同默认三元组秒开（深圳 × 全国重点城市 × 最近3年，过渡快照） |
| 需规叶 | 139 主体关系图谱 / 140 协同度模型 / 141 协同效果评估（需规 seq 139–141，Excel 行 140–142） |

**前置条件**
- `ads.synth_collab_batch_meta` 存在深圳市 `is_latest=1` 快照（`task:ANA-20261107-011`，`calc_batch_id=gapfill_transitional`，M2 F4）；
- gapfill 三表深圳行在库（relation_year 15 / output_year 5 / isolate_year 2，M2 F2/F3）；
- ADS 六结果表 0 行（走实时计算，M2 F1）。

**操作步骤**
1. 打开 `/intelligence/collaboration`；
2. 确认 URL 为 `?region=深圳&compare=全国重点城市&window=3y`（默认三元组）；
3. 不点击按钮，等待结果区渲染（instant 过渡快照）。

**期望结果**
- 200 过渡快照：指数仪表 + 完整度/中心度/密度 + 关系输入三卡 + 图谱 + 集群 + 孤立主体 + 排名（4 城）+ 趋势 + 策略建议；
- **响应 `dataSource=gapfill_transitional`**；页面/报告标「功能合规过渡 · gapfill is_mock=1」（🧪）；
- ADS 六结果表 0 行不影响展示（值来自实时计算，快照元数据仅登记 batch，M2 F1/F4）；
- 快照溯源行显示 snapshotId（`task:ANA-20261107-011`）；
- **404 分支（单独列）**：默认快照不存在时（快照被清理/环境重置）→ `IntelBatchSnapshotNotFound` → no_batch 引导「开始分析」，不 fixture 填数。

**数据依赖**
- `ads.synth_collab_batch_meta`（6 行；深圳 is_latest=1 行）——M2 §3.6；
- `ads.gapfill_synth_collab_relation_year`（深圳 15 行）/ `gapfill_synth_collab_output_year`（深圳 5 行）/ `gapfill_synth_collab_isolate_year`（深圳 2 行）——M2 §3.1–3.3；
- `ads.synth_collab_relation_input`（深圳 3y 3 行）——M2 §3.5；
- ADS 六结果表 0 行（实时计算不落表）——M2 §3.4。

**演示备注**：能演示出结果——全程过渡态，讲解必带「gapfill 过渡 + 实时计算」口径。

---

## CASE-COLLAB-02 · 深圳 × 最近1年（改窗任务走 gapfill 实算）

| 项 | 内容 |
|---|---|
| 用例名 | 非默认窗（最近1年）待分析态 → 显式开始分析 → gapfill 实算 |
| 需规叶 | 139 主体关系图谱（时间窗选择） |

**前置条件**
- 1y 窗**无已发布快照**（M2 F4/G-06：batch_meta 仅 3y 快照）；
- gapfill relation_year 深圳行覆盖 2021–2025（任务链可按最大 event_year 回推 1y 窗截取 2025，M2 F2）；
- 任务中心无同三段指纹当天成功任务。

**操作步骤**
1. 从默认秒开态把时间窗切「最近1年」→ URL 变 `?region=深圳&compare=全国重点城市&window=1y`；
2. 观察结果区：无该窗快照 → 待分析态（不自动建任务）；
3. 点击「开始分析」→ 任务过程页（五阶段**协同文案**）；
4. 完成后点击「查看分析结果」。

**期望结果**
- 无快照（404 `IntelBatchSnapshotNotFound` 语义）→ 待分析态引导「开始分析」；切条件不自动建任务（Q-ANALYSIS-01）；
- 任务链走 gapfill 过渡实算 1y 窗（relation_year 按 event_year 回推）；完成后任务结果可出（`dataSource=gapfill_transitional`，🧪）；
- **任务链仍发布 `synth_collab_batch_meta`**（1y 快照登记入 batch_meta，A/B 批隔离）；
- 同指纹当天复用单飞成立。
- **空窗分支（单独列）**：若 gapfill 关系行不覆盖该窗年份（`no_year_on_source` 语义）→ 图谱空图 + 该文案，指数/网络统计为空；深圳 2021–2025 全覆盖，本分支在四城默认环境不触发，仅供降级演示参考。

**数据依赖**
- `ads.synth_collab_batch_meta`（1y 无行 → 待分析态依据）——M2 §3.6 / G-06；
- `ads.gapfill_synth_collab_relation_year`（深圳 2025 年行在库）——M2 §3.1。

**演示备注**：能演示出结果（任务实算过渡态）——与活力/要素叶不同，协同 gapfill 输入带年份，非默认窗任务可实算出数。

---

## CASE-COLLAB-03 · 深圳 × 最近5年（改窗任务走 gapfill 实算）

| 项 | 内容 |
|---|---|
| 用例名 | 非默认窗（最近5年）待分析态 → 显式开始分析 → gapfill 实算 |
| 需规叶 | 139 主体关系图谱 |

**前置条件**：同 CASE-COLLAB-02 结构（5y 无快照；relation_year 深圳 2021–2025 覆盖 5 年）。

**操作步骤**
1. 时间窗切「最近5年」→ URL 变 `?region=深圳&compare=全国重点城市&window=5y`；
2. 观察待分析态；3. 点击「开始分析」；4. 完成后「查看分析结果」。

**期望结果**
- 同 CASE-COLLAB-02 结构：404 语义待分析态 → 显式开始分析 → gapfill 实算（2021–2025 全量关系行）→ 任务结果出数（`gapfill_transitional` 🧪）；发布 batch_meta；
- **空窗分支（单独列）**：`no_year_on_source` 空图文案分支同 COLLAB-02（本环境不触发）。

**数据依赖**
- `ads.synth_collab_batch_meta`（5y 无行）——M2 §3.6；
- `ads.gapfill_synth_collab_relation_year`（深圳 15 行全量覆盖）——M2 §3.1。

**演示备注**：能演示出结果；可对比 1y/3y/5y 三窗图谱密度差异（演示口径：数据为过渡 mock）。

---

## CASE-COLLAB-04 · 广州 × 最近3年（换城任务走 gapfill 实算）

| 项 | 内容 |
|---|---|
| 用例名 | 区域切广州 → 显式开始分析 → gapfill 实算 |
| 需规叶 | 139 主体关系图谱（灵活选择区域） |

**前置条件**
- 广州有 `is_latest=1` 快照（`task:ANA-20261107-006`，M2 F4）——广州秒开可命中快照；
- gapfill 广州 10 行（co_patent+co_project 两类，2021–2025，M2 F2）。

**操作步骤**
1. 区域切「广州」→ URL 变 `?region=广州&compare=全国重点城市&window=3y`；
2. 观察结果区：**广州快照命中 → 秒开过渡快照**（区别于东莞/惠州）；
3. 若进入待分析态则点击「开始分析」走任务。

**期望结果**
- 广州过渡快照秒开或任务实算（两者都合规，以快照存在与否为准）；排名含广州行；
- `dataSource=gapfill_transitional` 🧪；图谱关系类型含 co_patent 与 co_project 两类（ talent_flow 缺——广州 relation_year 无 talent_flow 行，M2 F2）；
- 快照溯源显示 `task:ANA-20261107-006`；
- **失败分支（单独列）**：任务失败 → 过程页失败阶段 +「重新尝试」。

**数据依赖**
- `ads.synth_collab_batch_meta`（广州 is_latest=1 行）——M2 §3.6；
- `ads.gapfill_synth_collab_relation_year`（广州 10 行）/ `output_year`（广州 5 行）/ `isolate_year`（广州 2 行）——M2 §3.1–3.3。

**演示备注**：能演示出结果；广州图谱比深圳少一类关系（无 talent_flow），讲解时按过渡数据事实说明。

---

## CASE-COLLAB-05 · 东莞 × 最近3年（换城任务走 gapfill 实算）

| 项 | 内容 |
|---|---|
| 用例名 | 区域切东莞 → 显式开始分析 → gapfill 实算（无快照路径） |
| 需规叶 | 139 主体关系图谱 |

**前置条件**
- **东莞无任何 batch_meta 快照**（M2 F4/G-06）；
- gapfill 东莞 5 行（仅 co_patent × 2021–2025，M2 F2）。

**操作步骤**
1. 区域切「东莞」→ URL 变 `?region=东莞&compare=全国重点城市&window=3y`；
2. 观察结果区：无快照 → 待分析态；3. 点击「开始分析」；4. 完成后「查看分析结果」。

**期望结果**
- 无快照 → 待分析态引导「开始分析」→ 任务走 gapfill 实算出数（`gapfill_transitional` 🧪）；任务链发布 batch_meta；
- （对照M2修正）**东莞图谱关系类型仅 co_patent 单类**（M2 G-05）：关系类型过滤在此城只有单选项；图谱边数明显少于深圳（5 关系行 vs 15）；孤立主体 2 个（东莞 isolate_year 2 行）；
- 排名含东莞行（四城网络结果派生）。
- **失败分支（单独列）**：同 COLLAB-04。

**数据依赖**
- `ads.synth_collab_batch_meta`（东莞无行）——M2 §3.6 / G-06；
- `ads.gapfill_synth_collab_relation_year`（东莞 5 行）/ `isolate_year`（东莞 2 行）——M2 §3.1/§3.3。

**演示备注**：能演示出结果（任务实算）；单类关系图谱是数据事实，不是功能缺陷。

---

## CASE-COLLAB-06 · 惠州 × 最近3年（换城任务走 gapfill 实算）

| 项 | 内容 |
|---|---|
| 用例名 | 区域切惠州 → 显式开始分析 → gapfill 实算（无快照路径） |
| 需规叶 | 139 主体关系图谱 |

**前置条件**
- 惠州无任何 batch_meta 快照（M2 F4/G-06）；
- gapfill 惠州 5 行（仅 co_patent × 2021–2025）+ isolate 2 行 + output 5 行（M2 §3.1–3.3）。

**操作步骤**
1. 区域切「惠州」→ URL 变 `?region=惠州&compare=全国重点城市&window=3y`；
2. 观察结果区：无快照 → 待分析态；3. 点击「开始分析」；4. 完成后「查看分析结果」。

**期望结果**
- 无快照 → 待分析态引导「开始分析」→ 任务走 gapfill 实算出数（`dataSource=gapfill_transitional` 🧪）；任务链发布 batch_meta；
- （对照M2修正）**惠州图谱关系类型仅 co_patent 单类**（M2 G-05）：关系类型过滤在此城只有单选项；图谱边数明显少于深圳（5 关系行 vs 15）；孤立主体 2 个（惠州 isolate_year 2 行）；
- 排名含惠州行（四城网络结果派生）；
- **失败分支（单独列）**：同 CASE-COLLAB-05（过程页失败阶段 +「重新尝试」，`failed` 批不被读取）。

**数据依赖**
- `ads.synth_collab_batch_meta`（惠州无行）——M2 §3.6 / G-06；
- `ads.gapfill_synth_collab_relation_year`（惠州 5 行）/ `output_year`（惠州 5 行）/ `isolate_year`（惠州 2 行）——M2 §3.1–3.3。

**演示备注**：能演示出结果；口径同东莞。

---

## CASE-COLLAB-07 · 图谱查看 + 中心主体点击高亮

| 项 | 内容 |
|---|---|
| 用例名 | 图谱查看（独立 API）+ 中心主体 TOP 点击高亮 |
| 需规叶 | 139 主体关系图谱（企业-机构-人才图） |

**前置条件**
- CASE-COLLAB-01 秒开态在场（快照 `task:ANA-20261107-011` 在场，图谱请求带 snapshotId）；
- gapfill relation_year 深圳 15 行在库。

**操作步骤**
1. 在 COLLAB-01 结果页定位图谱区，观察图谱先于/随结果顺序化加载（先结果后图谱，C2 顺序化）；
2. 核对节点类型标签（enterprise / research / talent / park / service）与关系类型（joint_patent / project / talent_flow）；
3. 点击中心度最高的主体节点 → 观察高亮；再点击空白/该节点 → 取消高亮；
4. 观察子图统计三卡随高亮同步。

**期望结果**
- 独立 graph API（`GET /topic/v1/synth/collaboration/graph`）带 `snapshotId` 返回（A/B 批不串）；
- （对照M2修正）节点/边数**以 API 实际返回为准**（审计文当日实测记录为 8 节点/9 边，M2 未复测；演示前先核对实际数，不把记录值当硬断言）；节点类型映射统一：`institution→research`、`service_org→service`；关系映射：`co_patent→joint_patent`、`co_project→project`；
- 点击高亮 → 子图统计三卡同步；再点取消；
- `dataSource=gapfill_transitional` 🧪。
- **空图分支（单独列）**：图谱返回空 + reason（三态文案见 collabGraphSource）→ 图谱区显示对应 reason 文案，不 500、不串批。

**数据依赖**
- `ads.synth_collab_batch_meta`（graph_batch_id 解析）+ `ads.gapfill_synth_collab_relation_year`（深圳 15 行构图）——M2 §3.6/§3.1。

**演示备注**：能演示出结果；节点/边计数先看 API 实际返回再讲解（审计文 8/9 为当日记录）。

---

## CASE-COLLAB-08 · 产业筛选（服务端过滤）

| 项 | 内容 |
|---|---|
| 用例名 | 图谱产业筛选下拉选择（服务端过滤重拉） |
| 需规叶 | 139 主体关系图谱（产业筛选） |

**前置条件**
- CASE-COLLAB-07 图谱在场；
- gapfill relation_year 深圳行带行业字段（industry_code/industry_label，M2 §4.1 表设计）。

**操作步骤**
1. 在图谱区打开产业筛选下拉，核对选项 = 响应节点 `industry_code` 去重；
2. 选择一个产业 → 观察图谱重拉（请求带 `industry` 参数）；
3. 核对节点/边与子图统计同步变化；再选回全部。

**期望结果**
- 下拉项 = 节点 industry_code 去重；选择后**服务端过滤**重拉（非前端裁剪）；
- 重拉后节点/边/子图统计同步；`snapshotId` 保持绑定（批不串）；🧪；
- **无产业行分支（单独列）**：响应无产业信息时下拉禁用（不静默换图、不伪造选项）。
- （对照M2修正）本用例**限深圳/广州**执行（M2 G-05：东莞/惠州关系行仅 co_patent 单类，图谱产业选项覆盖弱，不做多产业筛选演示）；东莞/惠州产业筛选预期选项极少或禁用，属数据事实。

**数据依赖**
- graph 响应节点 industry_code/industry_label（源自 `gapfill_synth_collab_relation_year` 行业字段）——M2 §3.1 / §4.1（功能合规过渡设计）。

**演示备注**：能演示出结果；强调「服务端过滤 + 快照绑定」两个语义。

---

## CASE-COLLAB-09 · 主体类型 / 关系类型过滤（前端叠加）

| 项 | 内容 |
|---|---|
| 用例名 | 主体类型过滤 + 关系类型过滤（前端叠加） |
| 需规叶 | 139 主体关系图谱（关系类型筛选） |

**前置条件**
- CASE-COLLAB-07 图谱在场（深圳 3y）；
- 深圳关系含 3 类（joint_patent / project / talent_flow，M2 F2）。

**操作步骤**
1. 主体类型过滤依次勾选/取消（enterprise/research/talent/park/service）→ 观察图面与子图统计；
2. 关系类型过滤依次勾选/取消三类 → 观察边与统计；
3. 组合过滤至无节点 → 观察局部空态。

**期望结果**
- kindFilter/edgeFilter **前端叠加过滤**；过滤后节点数、边数与子图三卡一致；
- 筛选后无节点 → 图谱局部空态 + 统计 0（不 500、不回退全图）；🧪；
- （对照M2修正）**三类关系筛选仅深圳/广州可演示**（M2 G-05：东莞/惠州仅 co_patent 单类，无多类型切换）——换城演示时关系类型过滤只有单选项属预期；
- （对照M2修正）co_project→project 关系在深圳图谱中有边（深圳 relation_year 含 co_project 行）；`synth_collab_relation_input.co_project=0` 值行（M2 G-07）不影响图谱边（图谱读 gapfill 关系行，非 relation_input 表）。

**数据依赖**
- 同 CASE-COLLAB-07（前端分支，无新表）；深圳 relation_year 三类关系行——M2 §3.1 / G-05。

**演示备注**：能演示出结果；重点讲「前端叠加过滤与统计同步」。

---

## CASE-COLLAB-10 · 网络统计三卡 + 关系输入构成

| 项 | 内容 |
|---|---|
| 用例名 | 网络统计三卡（子图口径）+ 关系输入三数字卡与条形图 |
| 需规叶 | 140 协同度模型（三类指标之网络统计/关系输入） |

**前置条件**
- CASE-COLLAB-01 秒开态在场；
- `synth_collab_relation_input` 深圳 3 行在库（co_patent 6477 / co_project 0 / talent_flow 18553，M2 F5）；
- ADS `synth_collab_network_stat` 0 行（值由实时计算回显，M2 F1）。

**操作步骤**
1. 定位网络统计三卡（子图节点/边/完整度·中心度·密度），核对「子图口径」区分标注；
2. 定位关系输入构成卡：读取联合专利/合作项目/人才流动三数字卡与条形图；
3. 与图谱筛选联动核对（COLLAB-09 过滤后子图统计变化）。

**期望结果**
- 子图三卡 = 节点/边/完整度·中心度·密度（**子图口径**，与全网指标区分标注）；数值随图谱过滤同步；
- 关系输入三卡 + 条形图渲染（canonical `M_SYNTH_COLLAB_RELATION_INPUT`；过渡期由 gapfill 实时计算回显，ADS 表 0 行不拦截展示）；
- （对照M2修正）**合作项目数字卡 = 0**（`synth_collab_relation_input.co_project=0` 值行，M2 G-07）——按诚实 0 值展示（有行有值），不是空态也不是缺行；条形图含 0 高项目柱属预期；讲解口径「过渡演示数据中合作项目为 0」；
- ADS 六结果表 0 行不影响展示（M2 F1：一律按实时计算路径判定）；
- **缺行分支（单独列）**：关系输入无行 → null「—」不补 0。

**数据依赖**
- `ads.synth_collab_relation_input`（深圳 3y 3 行；co_project=0）——M2 §3.5 / G-07；
- `ads.synth_collab_network_stat`（0 行；展示值来自实时计算）——M2 §3.4 / G-04。

**演示备注**：能演示出结果；co_project=0 是本条的关键讲解点（诚实 0 值）。

---

## CASE-COLLAB-11 · 协同指数三卡 + 横向排名 + 点击切区

| 项 | 内容 |
|---|---|
| 用例名 | 协同指数/完整度/中心度密度三卡 + 排名表 + 点击切区回 config |
| 需规叶 | 140 协同度模型（协同指数） |

**前置条件**
- CASE-COLLAB-01 秒开态在场；
- ADS `synth_collab_index` 0 行（值由实时计算回显，M2 F1）；排名由四城网络结果派生（M2 §4.3 功能合规过渡设计）。

**操作步骤**
1. 定位协同指数仪表与完整度/中心度/密度卡，读取数值与 vs 对比均值/同比；
2. 定位横向排名表（4 城），核对当前区域高亮；
3. 点击排名行「广州」→ 观察 URL 与结果区状态。

**期望结果**
- 指数/完整度/中心度/密度有值（过渡实时计算；`windowEmpty` 分态：空窗显示「—」+ PUBLIC_EMPTY，不补 0）；
- 排名 4 城当前（深圳）高亮；点击他区 → 回 config 待重分析（不自动建任务）；🧪；
- （对照M2修正）ADS `synth_collab_index` 0 行不是缺口（G-04：正式表空是合规诚实态）——展示值以过渡实时计算响应为准；M3 判定本条时按 gapfill 输入齐备即 supported（过渡）；
- **空窗分支（单独列）**：指数 null → 「—」+ PUBLIC_EMPTY。

**数据依赖**
- `ads.synth_collab_index`（0 行，过渡响应为准）——M2 §3.4 / G-04；
- `ads.gapfill_synth_collab_relation_year`（四城行齐，排名派生输入）——M2 §3.1。

**演示备注**：能演示出结果；排名四城为过渡派生值，讲解带 🧪 口径。

---

## CASE-COLLAB-12 · 纵向趋势查看（2021–2025）

| 项 | 内容 |
|---|---|
| 用例名 | 协同纵向趋势查看（gapfill 年度输入回推） |
| 需规叶 | 141 协同效果评估（趋势维度） |

**前置条件**
- CASE-COLLAB-01 秒开态在场；
- gapfill output_year 深圳 5 行（2021–2025）/ relation_year 深圳 15 行（3 类 × 5 年）在库（M2 F2/F3）。

**操作步骤**
1. 定位趋势卡，读取 2021–2025 年度点；
2. 核对趋势值来源标注（gapfill 产出/关系年输入回推）；
3. 切到 1y/5y 窗核对趋势点窗口截取（延伸 COLLAB-02/03）。

**期望结果**
- 趋势 2021–2025 演示年度渲染（`fill_method=demo_year_series` 过渡行，🧪）；同比取最近两个年度点；
- 1y 窗趋势仅 2025 点、5y 窗全量 5 点（窗口由 event_year 回推）；
- **无行分支（单独列）**：无行「暂无数据」不补 0。

**数据依赖**
- `ads.gapfill_synth_collab_output_year`（深圳 2021–2025 5 行）/ `gapfill_synth_collab_relation_year`（深圳 15 行）——M2 §3.1/§3.2。

**演示备注**：能演示出结果；趋势是 gapfill 演示序列，讲解带「演示年度」口径。

---

## CASE-COLLAB-13 · 集群卡 + 孤立主体 + 点击定位

| 项 | 内容 |
|---|---|
| 用例名 | 集群卡查看（过渡规则）+ 孤立主体表 + 点击孤立主体定位图谱 |
| 需规叶 | 140 协同度模型（集群与孤立主体） |

**前置条件**
- CASE-COLLAB-07 图谱在场；
- gapfill isolate_year 深圳 2 行（独立研究所C/institution + 独立服务机构C/service，connection_count=0）；
- ADS `synth_collab_cluster` **0 行**（正式集群归属不派生，M2 F1）。

**操作步骤**
1. 定位集群卡：读取集群数量与内部关系密度分；
2. 核对过渡规则标注（响应与方法摘要标过渡态）；
3. 定位孤立主体表（预期 2 行：独立研究所C / 独立服务机构C）；
4. 点击孤立主体行 → 观察图谱定位/高亮。

**期望结果**
- （对照M2修正）集群展示为**过渡规则结果**（关系图连通分量；集群分=内部关系密度；响应与方法摘要标过渡态；正式 C-02 规则待甲方定稿 🟡）：深圳默认快照集群 1 个（审计文记录，演示以 API 实际返回为准）；正式 ADS `synth_collab_cluster` 0 行（`cluster_rule_unclosed` 语义：C-02 定稿前不派生正式集群归属，空表不是缺陷）；
- 孤立主体 2 个（每城 2 个、全表 8 行，M2 §3.3），带 `connectionFact` + 待审核建议；
- 点击孤立主体 → 图谱定位/高亮零度节点；🧪。

**数据依赖**
- `ads.gapfill_synth_collab_isolate_year`（8 行；深圳 2 行）——M2 §3.3；
- `ads.synth_collab_cluster`（0 行；`cluster_rule_unclosed` 语义）——M2 §3.4。

**演示备注**：能演示出结果；集群讲「过渡规则」、孤立主体讲「待审核建议」两个口径。

---

## CASE-COLLAB-14 · 相关性散点 + Pearson（status=ok）

| 项 | 内容 |
|---|---|
| 用例名 | 相关性散点查看 + Pearson 相关系数（仅关联非因果） |
| 需规叶 | 141 协同效果评估（相关性） |

**前置条件**
- CASE-COLLAB-01 秒开态在场；
- gapfill output_year 深圳 5 行（collab_score 与 joint_patent_count 各 5 个年度点，n=5 ≥ 3，M2 F3）；
- ADS `synth_collab_output_corr` 0 行（实时计算，M2 F1）。

**操作步骤**
1. 定位关联散点区，读取产出指标/样本范围/方法状态三字段；
2. 核对 Pearson 系数与散点（年度点 tooltip）；
3. 核对「仅关联，非因果」文案（Q-SYNTH-C-03 🟡）。

**期望结果**
- effectEval **status=ok**：相关系数 + 散点渲染（年度点 tooltip）；样本范围/方法状态显性；文案「仅关联，非因果」；🧪；
- ADS `synth_collab_output_corr` 0 行不影响展示（值来自 gapfill 序列实时 Pearson，M2 F1/G-04）；
- **`insufficient` 分支（单独列）**：n<3 → status=`insufficient` → 合法态「样本不足，暂无法给出关联结论」，不画伪线、不算失败批（深圳 n=5 本环境不触发，降级演示参考）；
- **缺行分支（单独列）**：output_year 无行 → status 缺行诚实空态。

**数据依赖**
- `ads.gapfill_synth_collab_output_year`（深圳 5 年序列；Pearson 输入）——M2 §3.2；
- `ads.synth_collab_output_corr`（0 行；实时计算不落表）——M2 §3.4 / G-04。

**演示备注**：能演示出结果；相关系数为过渡演示值，讲解必带「仅关联非因果 + mock」双口径。

---

## CASE-COLLAB-15 · 策略建议查看（LLM 优先 / 事实回退）

| 项 | 内容 |
|---|---|
| 用例名 | 策略建议查看（LLM 优先，LLM 不可用时确定性建议降级） |
| 需规叶 | 141 协同效果评估（优化路径建议） |

**前置条件**
- CASE-COLLAB-01 秒开态在场；
- 装包 LLM（`gkx-zhipu-llm`）配置可用性不限（两条分支都要能演示）；
- 关系输入/相关性事实数据在库（COLLAB-10/14 依赖，M2 F5/F3）。

**操作步骤**
1. 定位策略建议表，逐条读取建议内容 + evidenceRefs + reviewStatus；
2. 核对全部建议「待审核」Tag；
3. （降级分支）LLM 不可用环境（或配置关闭）重进结果态，观察建议来源切换。

**期望结果**
- LLM 可用：证据锚定建议渲染，全部 `reviewStatus=待审核` Tag（Q-SYNTH-C-04 🟡）；
- **LLM 不可用降级**：确定性事实建议 ≥2 条（审计文记录 2 条，基于关系输入与相关性事实），仍全部待审核，**禁编造数值**；🧪；
- **空分支（单独列）**：无建议 → `strategies=[]` + reason，不伪造条目。

**数据依赖**
- 装包 LLM（`gkx-zhipu-llm`）+ 关系输入/相关性事实（无专表；事实输入 = `gapfill_synth_collab_relation_year` / `output_year`，M2 §3.1/§3.2）。

**演示备注**：能演示出结果（两条分支择一现场可演示）；降级建议是合规回退不是故障。

---

## CASE-COLLAB-16 · 生成协同效率报告（读快照，不建任务）

| 项 | 内容 |
|---|---|
| 用例名 | 生成协同效率报告 → 报告页 → 导出 PDF（不创建报告任务） |
| 需规叶 | 141 协同效果评估（效率报告） |

**前置条件**
- CASE-COLLAB-01 快照在场（深圳 `task:ANA-20261107-011`）；或广州快照（`task:ANA-20261107-006`）；
- **东莞/惠州无快照**（M2 F4/G-06）——反分支用。

**操作步骤**
1. 在 COLLAB-01 结果页点击「生成协同效率报告」→ 进入 `/intelligence/collaboration` 报告页；
2. 核对报告七段式结构（identity/…/limitations）与过渡标识；
3. 导出 PDF 本地核对；
4. （反分支）切到东莞/惠州（无快照）观察报告入口；
5. 核对任务中心：确认**没有**新建 `region_innovation_collaboration_report` 任务。

**期望结果**
- **不创建 `region_innovation_collaboration_report` 任务**：直接携父任务/条件读成功快照渲染报告（任务中心无新增报告任务行）；
- 报告七段式（identity/…/limitations）含 `dataSource=gapfill_transitional` 过渡标识；PDF 前端导出；🧪；
- **无快照分支（单独列）**：快照 404/空 → 报告页「先完成分析」提示，不伪造数据段、不生成空白 PDF 冒充（东莞/惠州即此分支现场）。

**数据依赖**
- 消费 CASE-COLLAB-01 快照（`ads.synth_collab_batch_meta` 溯源；深圳/广州 is_latest 快照）——M2 §3.6 / G-06。

**演示备注**：能演示出结果（深圳/广州）；东莞/惠州演示「入口禁用」诚实分支。

---

## CASE-COLLAB-17 · 坏快照 `batch_meta_missing` 反例

| 项 | 内容 |
|---|---|
| 用例名 | 指定无映射 snapshotId 打开图谱（`batch_meta_missing` 拦截，禁回落） |
| 需规叶 | 139 主体关系图谱（快照追溯边界） |

**前置条件**
- 无数据前置（只读拦截分支，不写库）；
- 可用不存在的快照 ID（`task:never_exists` 语义：batch_meta uk(snapshotId) 无行，M2 F4 快照清单外）。

**操作步骤**
1. 打开协同工作台，构造图谱请求携带不存在的 snapshotId（如从任务结果以 `task:<不存在ID>` 打开，或地址栏直达带该参数的结果态）；
2. 观察图谱区响应与文案；
3. 核对不回落最新批（默认快照在场也不回落）。

**期望结果**
- **`batch_meta_missing`**：HTTP 200 + `nodes=[]` + reason 文案逐字「指定快照在批次登记表中无映射，禁止回落最新批；请重新完成分析后查看」；
- **不回落最新批**（即使深圳最新快照在场）；不 500、不空白卡死；
- （对照M2修正）构造方式明确为**不存在的 snapshotId**（`task:never_exists` 语义，batch_meta 无该行）——不使用深圳 4 条历史快照做坏快照（历史快照有 meta 行，属合法回溯快照，不是坏快照；M2 §3.6）；若需演示「历史快照切换」，另行按合法快照回溯演示，不改本条编号语义。

**数据依赖**
- `ads.synth_collab_batch_meta`（uk(snapshotId) 无行分支；深圳/广州快照在场用于验证「不回落」）——M2 §3.6。

**演示备注**：演示拦截反例——「禁止回落」是本条唯一考点；只读分支零数据写入，任意时候可跑。

---

## 附录 A · 对照 M2 修正索引（M3 以本册为准）

| CASE | 修正要点 | M2 依据 |
|---|---|---|
| CASE-COLLAB-01 | 展示值全部来自实时计算（ADS 六表 0 行）；快照溯源 snapshotId 明确 | §3.4 G-04 / §3.6 |
| CASE-COLLAB-04 | 广州可快照秒开（batch_meta 有 is_latest 快照）且无 talent_flow 关系类 | §3.6 / §3.1 |
| CASE-COLLAB-05/06 | 东莞/惠州无快照 → 走任务实算路径；图谱仅 co_patent 单类 | §3.6 G-06 / §3.1 G-05 |
| CASE-COLLAB-07 | 节点/边数以 API 实际返回为准（8/9 为审计文当日记录，M2 未复测） | §7 / 审计文 |
| CASE-COLLAB-08 | 产业筛选限深圳/广州（东莞/惠州关系行单类，选项覆盖弱） | G-05 |
| CASE-COLLAB-09 | 三类关系筛选限深圳/广州；co_project=0 值行不拦图谱边 | G-05 / G-07 |
| CASE-COLLAB-10 | co_project 数字卡=诚实 0 值展示（有行有值非空态）；ADS 0 行不算缺口 | §3.5 G-07 / §3.4 G-04 |
| CASE-COLLAB-11 | `synth_collab_index` 0 行不是缺口（空表是合规诚实态），按过渡响应判定 | §3.4 G-04 |
| CASE-COLLAB-13 | 集群=过渡规则结果；正式 `synth_collab_cluster` 0 行=`cluster_rule_unclosed` 语义非缺陷 | §3.3 / §3.4 |
| CASE-COLLAB-17 | 坏快照构造方式=不存在 snapshotId（`task:never_exists` 语义），不用历史快照冒充坏快照 | §3.6 |

## 附录 B · 本叶复核

- CASE 计数：**17 条**（CASE-COLLAB-01～17，与总册一致，零增删）；
- 每条含：用例名+需规叶 / 前置条件 / 操作步骤 / 期望结果（含 404/空图/失败分支与过渡标识）/ 数据依赖（含 M2 实际状态）/ 演示备注 六要素；
- reason 值保留清单：`IntelBatchSnapshotNotFound` / `batch_meta_missing` / `no_year_on_source` / `cluster_rule_unclosed` / `graph_request_rejected` / `graph_upstream_unavailable` / `insufficient`（本叶涉及）；标识保留清单：`gapfill_transitional` / `is_mock=1` / `dataSource=gapfill_transitional`。
