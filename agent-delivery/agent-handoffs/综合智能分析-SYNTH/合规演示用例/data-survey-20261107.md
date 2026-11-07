# SYNTH 合规演示用例 · demo 库数据情况调研（M2）

> **task-id**：`SYNTH-DEMO-CASE-M2-DB-L01`（长任务 M2 叶）
> **调研时间**：2026-11-07 16:31–16:45（UTC+8）
> **执行**：agent:data-agent（子智能体）
> **总控真源**：`../SYNTH-合规演示用例-长任务总控.md` §3
> **调研方式**：**实查**（database-mcp 只读连接 `gkx-mysql/demo-gkxlumenx-ods`，实例 `10.50.11.76:3306`，账号 `gkxlumenx`；全部 SELECT/SHOW，零写库；口令不入本文件）
> **调查受阻表**：无（28/28 全部实查成功；DWD 汇聚源 4 表同样实查）

---

## 0. 结论速览（给 M3 判定直接引用）

1. **28 张 synth/gapfill 表全部实查**（demo_gkxlumenx_ads 27 + demo_gkxlumenx_ai 1）。与 2026-11-07 审计文行数声明**全部一致**，零差异。
2. **窗口覆盖只有「最近3年」**：活力/要素 ADS 全部表 `window_label` 均只有 `最近3年`；1y/5y 窗仅存在于 `demo_gkxlumenx_ai.synth_elem_four_dim_score`（137 四维过渡表）。
3. **`is_mock=1` 全表 100%**（除 `synth_collab_batch_meta` 6 行无 is_mock 列；六条快照元数据不算数据行）。**没有任何真实业务行**。
4. **协同 ADS 六表全空**（node/edge/network_stat/index/output_corr/cluster 均为 0 行），前端演示走 `gapfill_synth_*` 三表 + `synth_collab_relation_input`（3 行）+ `synth_collab_batch_meta`（6 快照，其中 2 个城市最新）+ 实时计算任务链（cache_key 城市维度）。非深圳城市没有已发布快照，但有快照的键（深圳市/广州市）各留有历史版本 → 可做"坏快照切换"类用例。
5. **三类风险数据缺陷**（M3/M4 必须知道）：
   - `synth_vit_dim_score` / `synth_vit_indicator`、要素 7 表：**非深圳行的 `region_name` 全部误标「深圳」**（`region_code` 正确）。API 按 `region_code` 过滤则无影响，按名称展示会串城市名。
   - `synth_vit_index/rank/weight`、`synth_vit_dim_score/indicator`：**深圳行存在双批次冗余**（通用 seed + 档位 seed 各一份，除 trend 历史外）；查询若不按 `calc_batch_created_at` 取最新会双值。
   - `synth_elem_index` 四城市指数值来自同一目标值 ± 扰动（仅一个 index 数值口径），非独立计算。
6. **`synth_vit_trend` 表不存在**——总控 §3 清单所列此表在库中不存在；趋势数据 = `synth_vit_index` 同键 2022/2023 历史年批次（`mock_20261107_vit_trend_*`）。见 §1.5。

---

## 1. 活力（133–135）

### 1.1 `synth_vit_index`（活力指数；趋势由历史年批次承载）

| 项 | 值 |
|---|---|
| 总行数 | **39** |
| 窗口 | 全部 `最近3年`（1y/5y = **0 行**） |
| 年份分布 | 2022:12 / 2023:12 / 2024:15（2024 内深圳 6 行：双批次冗余） |
| 批次 | 最新 `mock_20261106_vit_seed_equal`（2024 当年行）；历史年行批次 `mock_20261107_vit_trend_{profile}_{year}` |
| calc_status | 全部 `succeeded` |
| is_mock=1 | **39/39**（100%） |

region × window × 年份分布（每格含 3 个 weight_profile）：

| region | 最近3年·2022 | 最近3年·2023 | 最近3年·2024 | 备注 |
|---|---|---|---|---|
| 深圳 | 3 | 3 | **6** | 2024 双批次冗余（`vit_seed` + `vit_seed_equal/index_main/weight_main`） |
| 广州 | 3 | 3 | 3 | |
| 东莞 | 3 | 3 | 3 | |
| 惠州 | 3 | 3 | 3 | |

**覆盖缺口**：广州/东莞/惠州 × 最近1年、最近5年 = **0 行**（全部城市同此窗口缺口）；LEGACY 权重档行 2024 年也有（深圳多出 `vit_seed` 通用批），`TEMP_*` 档 0 行。

### 1.2 `synth_vit_weight`（权重）

| 项 | 值 |
|---|---|
| 总行数 | **60** |
| 窗口 | 全部 `最近3年` |
| 分布 | 4 城市 × 3 档（INDEX_MAIN / EQUAL / WEIGHT_MAIN）× 4 维（tech/talent/industry/policy）× 行；深圳每组合 2 行（双批次冗余）、其余城市 1 行 |
| 最新批次 | `mock_20261106_vit_seed_equal`（非深圳） / `mock_20261106_vit_seed_*_main`（深圳，与通用 seed 并存） |
| calc_status | 全部 `succeeded` |
| is_mock=1 | **60/60** |

**覆盖缺口**：1y/5y 窗 0 行；`TEMP_*` 反例档 0 行（反例用例只能用 `WEIGHT_MAIN` 档）。

### 1.3 `synth_vit_dim_score`（四维分）

| 项 | 值 |
|---|---|
| 总行数 | **96** |
| 窗口 | 全部 `最近3年`，year=2024 |
| region_code | 四城各 24 行 ✅ |
| ⚠️ region_name | **非深圳三城全部误标「深圳」**（region_code 正确） |
| 深圳双批次 | `vit_seed`（通用）+ `vit_seed_{profile}`（档位）两批并存（深圳合计 24 行 = 2 批次 × 3 档 × 4 维） |
| 最新批次 | `mock_20261106_vit_seed_weight_main` |
| calc_status | 全部 `succeeded` |
| is_mock=1 | **96/96** |

每城构成：4 维 × 3 档 × 4 行 = 48 行（深圳含通用批 48 + 档位批 48 中的 24…实际：深圳 24 = 2 批次 × 3 档 × 4 维；非深圳各 24 = 3 档 × 4 维 × 1 批次）。

### 1.4 `synth_vit_indicator`（活力分项）

| 项 | 值 |
|---|---|
| 总行数 | **288** |
| 窗口 | 全部 `最近3年` |
| region_code | 四城各 72 行 ✅ |
| ⚠️ region_name | **非深圳三城全部误标「深圳」** |
| 指标数 | 12 个 indicator_code × 4 维；status 混合 `ok / mock / missing / proxy` |
| 深圳双批次 | 同 1.3 模式 |
| 最新批次 | `mock_20261106_vit_seed_equal` |
| calc_status | 全部 `succeeded` |
| is_mock=1 | **288/288** |

status 取值分布为混合（`ok,proxy,mock,missing` 均存在）——演示"分项状态诚实性"用例可直接用 status 列；M3 判定按 indicator×城市粒度细查时需带 status 条件。

### 1.5 `synth_vit_rank`（排名）

| 项 | 值 |
|---|---|
| 总行数 | **24** |
| 窗口 | 全部 `最近3年` |
| 分布 | 仅 `region_code=深圳市` 上下文 24 行：4 个 rank_city（深圳=rank1·is_current=1，广州 rank2，东莞 rank3，惠州 rank4）× 3 档 × 2 批次 |
| 最新批次 | `mock_20261106_vit_seed_equal` |
| calc_status | 全部 `succeeded` |
| is_mock=1 | **24/24** |

**注意**：rank 行的 `region_code` 只有深圳市——若 API 对"东莞排名视图"要求 region=东莞 的行，则**全部非深圳排名视图 0 行**；若排名页按 `rank_city` 读取深圳上下文 24 行则可演示。M3 需按接口实际查询键判定。

### 1.6 `synth_vit_trend`（趋势）——**表不存在**

总控 §3 清单所列 `synth_vit_trend` 在两个库中**均不存在**（information_schema 零命中）。趋势演示数据 = `synth_vit_index` 同键 2022/2023 历史年行（seed 05 脚本生成，批次 `mock_20261107_vit_trend_*`，仅扩展 year 维度、不作为最新批次）。**M3 判定趋势类用例时按 `synth_vit_index` 计，不按本表。**

### 1.7 活力 gapfill 三表（缺项输入；审计文行数声明 = 各 4）

| 表 | 总行数 | 分布 | is_mock=1 | 批次 | 缺口 |
|---|---|---|---|---|---|
| `gapfill_synth_new_product_sales_ratio` | **4** | city（深圳/广州/东莞/惠州，全称「深圳市」等）× 2024 各 1 行 | 4/4 | `mock_20261107_vit_gapfill_seed` | 无（年覆盖=2024 单年，窗口由活力链路换算） |
| `gapfill_synth_rd_employee` | **4** | 同上 | 4/4 | 同上 | 无 |
| `gapfill_synth_policy_effect` | **4** | 同上 | 4/4 | 同上 | 无 |

列结构注意：**三表无 region_code / window_label / calc_batch_id / calc_status 列**，城市键 = `city`（全称），年份键 = `year`，批次键 = `gapfill_batch_id`。M3 引用时按此键名。

---

## 2. 要素（136–138）

### 2.0 ADS `synth_elem_*` 共性

- 窗口：全部只有 `最近3年`；`compare_scope` 全部只有 `全国重点城市`。
- `region_code` 四城齐；**除 `synth_elem_index`（名称正确）与 `synth_elem_rank`（仅深圳上下文）外，其余 7 表非深圳行 `region_name` 全部误标「深圳」**。
- `calc_status` 全部 `succeeded`；`is_mock=1` 占比全部 100%。
- 双行构成 = 同数据复制到 4 个 `region_code`（深圳/广州/东莞/惠州同名值；index 表四城值 ± 扰动）。

### 2.1 `synth_elem_index`（要素指数）

| 项 | 值 |
|---|---|
| 总行数 | **4**（每城 1 行；region_name 正确） |
| 最新批次 | `mock_20261105_elem_seed` |
| 缺口 | 1y/5y 窗 0 行；城市指数值 = 同一目标值 ± 扰动（非独立口径） |

### 2.2 `synth_elem_type_score`（类型分，136 全景分类）

| 项 | 值 |
|---|---|
| 总行数 | **56**（4 城 × 14：7 类型 T-ENT/T-FUN/T-POL/T-RSI/T-SPA/T-SRV/T-TAL × 2 行） |
| ⚠️ region_name 误标 | 是（非深圳三城） |
| 最新批次 | `mock_20261105_elem_seed` |
| is_mock | 56/56 |

### 2.3 `synth_elem_level_score`（层次分）

| 项 | 值 |
|---|---|
| 总行数 | **56**（结构同 2.2，7 层次 L-* × 2 行 × 4 城） |
| ⚠️ region_name 误标 | 是 |
| is_mock | 56/56 |

### 2.4 `synth_elem_domain_score`（领域分）

| 项 | 值 |
|---|---|
| 总行数 | **20**（4 城 × 5 领域 D1-COV/D2-TEC/D3-OUT/D4-TAL/D5-ECO） |
| ⚠️ region_name 误标 | 是 |
| is_mock | 20/20 |

### 2.5 `synth_elem_indicator`（分项指标，双透镜）

| 项 | 值 |
|---|---|
| 总行数 | **108**（4 城 × 27：lens=type 68 行 + lens=domain 40 行；27 个 indicator_code） |
| status | 混合 `ok / mock / proxy / degenerate` |
| ⚠️ region_name 误标 | 是 |
| is_mock | 108/108 |

### 2.6 `synth_elem_contrib`（138 贡献度）

| 项 | 值 |
|---|---|
| 总行数 | **32**（4 城 × 8：4 要素 ENT/FUN/RSI/TAL × 2 行） |
| caliber_flag | 24 行 NULL + 8 行 `B`（每城 2 行 B 口径） |
| ⚠️ region_name 误标 | 是 |
| is_mock | 32/32 |

### 2.7 `synth_elem_rank`（要素排名）

| 项 | 值 |
|---|---|
| 总行数 | **4**，**仅 `region_code=深圳市` 上下文**（4 个排名城市行；region_name 正确） |
| 缺口 | 非深圳上下文 0 行（同活力 rank 模式，M3 按接口键判定） |
| is_mock | 4/4 |

### 2.8 `synth_elem_weight`（要素权重）

| 项 | 值 |
|---|---|
| 总行数 | **12**（4 城 × 3 行；⚠️ region_name 误标） |
| is_mock | 12/12 |

### 2.9 `demo_gkxlumenx_ai.synth_elem_four_dim_score`（137 四维过渡；审计文声明 48）

| 项 | 值 |
|---|---|
| 总行数 | **48** = 4 城 × 3 窗（**最近1年 / 最近3年 / 最近5年 全齐**）× 4 维（scale/quality/structure/activity）各 1 行 |
| compare_scope | 全部 `全国重点城市` |
| metric_status | 全部 `pending_registration`（过渡标识②，演示期望结果必带） |
| calc_status | 全部 `succeeded`；score 无 NULL（48/48 有值） |
| 批次 | 唯一 `mock_20261106_four_dim_seed` |
| is_mock | 48/48 |
| region_name | **正确**（本表无赋名缺陷） |

**本表是三叶中唯一全窗口覆盖的数据面**。M3 判定 137 用例可全条件 supported（mock 过渡态）。

### 2.10 136 要素全景 DWD 汇聚源（无 ADS 表；实时聚合）

| ODS 源表（demo_gkxlumenx_ods） | 总行数 | is_deleted=0 | 用途 |
|---|---|---|---|
| `dwd_org_base_info` | 175,058 | 189,116 | 企业 + 空间（园区关键词 6 个：园区/孵化/众创/高新区/产业基地/创业园 → **128 行**） |
| `dwd_research_institute_base_info` | 1,934 | 2,074 | 机构 |
| `dwd_scholar` | 18,049 | 21,316 | 人才（H 指数 TopN） |
| `dwd_org_financing_info` | 25,488 | 25,654 | 资金（融资记录） |

注：information_schema `table_rows` 为估算值（InnoDB），is_deleted=0 为精确 COUNT。全景面板按查询实时聚合（无表、3 秒超时降级 AR-8），非深圳城市**未按城市过滤**（全景是全域汇聚）——M3 判定 136 用例时城市维度不构成缺口。

---

## 3. 协同（139–141）

### 3.1 `gapfill_synth_collab_relation_year`（C-05 关系年化；审计文声明 35）

| 项 | 值 |
|---|---|
| 总行数 | **35** ✅ |
| region × 年分布 | **深圳 15**（2021–2025 × 3 关系类型）/ **广州 10**（2021–2025，co_patent+co_project）/ **东莞 5**（co_patent×5 年）/ **惠州 5**（co_patent×5 年） |
| relation_type | co_patent / co_project / talent_flow（深圳 3 类；广州 2 类；东莞/惠州仅 co_patent） |
| source_has_year | 全部 0（模拟 C-05 无年份真源回填场景） |
| 批次 | 唯一 `mock_20261106_collab_gapfill_seed` |
| is_mock | 35/35 |

**缺口**：东莞/惠州缺 co_project、talent_flow 关系 → 图谱"关系类型筛选"用例在东莞/惠州只有单类型可选。

### 3.2 `gapfill_synth_collab_output_year`（C-05 产出序列；审计文声明 20）

| 项 | 值 |
|---|---|
| 总行数 | **20** ✅（4 城 × 5 年 2021–2025 各 1 行） |
| 列 | collab_score + joint_patent_count（深圳 62→82 / 广州 50.84→67.24 / 东莞 42.16→55.76 / 惠州 33.48→44.28，逐年上升） |
| 批次 | `mock_20261106_collab_gapfill_seed`；is_mock 20/20 |

**缺口**：无（相关性 Pearson 计算按 5 年序列，四城全可演示）。

### 3.3 `gapfill_synth_collab_isolate_year`（孤立主体；审计文声明 8）

| 项 | 值 |
|---|---|
| 总行数 | **8** ✅（4 城 × 2 实体：`独立研究所C`(institution) + `独立服务机构C`(service)，event_year=2025，connection_count=0） |
| 批次 | `mock_20261106_collab_gapfill_seed`；is_mock 8/8 |

**注意**：审计文"逐叶对账"处写"孤立主体 2 个"是**深圳单城**口径（每城均为 2 个实体）。全表 8 行 = 4 城 × 2。

### 3.4 `synth_collab_node` / `synth_collab_edge` / `synth_collab_network_stat` / `synth_collab_index` / `synth_collab_output_corr` / `synth_collab_cluster`

| 表 | 总行数 | 状态 |
|---|---|---|
| synth_collab_node | **0** | 空 |
| synth_collab_edge | **0** | 空 |
| synth_collab_network_stat | **0** | 空 |
| synth_collab_index | **0** | 空 |
| synth_collab_output_corr | **0** | 空 |
| synth_collab_cluster | **0** | 空 |

**结论**：协同 ADS 结果面整体为空。图谱/网络/相关性/指数/集群展示由任务链实时计算（输入 = 3.1–3.3 三张 gapfill 表 + 3.6 relation_input），**落表持久化链路未启用**（gapfill_transitional 批次仅元数据登记）。M3 判定协同用例一律按"实时计算 + gapfill 输入"路径，不得按"查 ADS 结果表"路径。

### 3.5 `synth_collab_relation_input`（关系输入 ADS 面）

| 项 | 值 |
|---|---|
| 总行数 | **3**（仅深圳 × 最近3年：co_patent 6477 / co_project 0 / talent_flow 18553，year=2024） |
| 批次 | `mock_20261105_collab_seed`；is_mock 3/3 |

**缺口**：非深圳 0 行；co_project 在深圳上下文也是 0 值行（有行无值）。140"关系输入完整性"用例需注意 co_project=0 的空态分支。

### 3.6 `synth_collab_batch_meta`（快照元数据；无 is_mock 列）

| 项 | 值 |
|---|---|
| 总行数 | **6** |
| is_latest=1 | **2 条**：深圳市（`task:ANA-20261107-011`，2026-11-07 10:32）/ 广州市（`task:ANA-20261107-006`，2026-11-07 02:38）；calc_batch_id 均 = `gapfill_transitional` |
| 历史/非最新 | 4 条（深圳 4 个旧快照 + 1 条旧批次 `mock_20261105_collab_seed`） |
| 缺口 | **东莞/惠州无任何快照**；1y/5y 窗无快照 |

用途：141 报告 PDF"读取已发布快照"用例可演示（深圳市/广州市）；**深圳同键 4 条历史快照**可支撑"坏快照/快照切换"类用例；东莞/惠州走实时计算（无快照依赖）路径。

---

## 4. 与审计文行数声明对账（需规功能一致性审计-20261107.md §本次实库修复）

| 表 | 审计文声明 | 实查 | 判定 |
|---|---:|---:|---|
| `synth_elem_four_dim_score`（demo_gkxlumenx_ai） | 48 | **48** | ✅ 一致 |
| `gapfill_synth_collab_relation_year` | 35 | **35** | ✅ 一致 |
| `gapfill_synth_collab_output_year` | 20 | **20** | ✅ 一致 |
| `gapfill_synth_collab_isolate_year` | 8 | **8** | ✅ 一致 |
| `gapfill_synth_new_product_sales_ratio` | 4 | **4** | ✅ 一致 |
| `gapfill_synth_rd_employee` | 4 | **4** | ✅ 一致 |
| `gapfill_synth_policy_effect` | 4 | **4** | ✅ 一致 |

**对账结论：7/7 全部一致，零差异，无种子重跑或批次新增迹象**（唯一批次 ID 与审计文当日工作吻合；活力侧 `mock_20261107_vit_trend_*` 历史批次是 05 脚本对既有 index 表的年份扩展，不改变上述 7 表行数）。

任务派单中的对账预期「四维48/关系年35/产出20/孤立8/活力gapfill三表各4」全部命中。

---

## 5. 额外发现（总控 §3 清单外的 synth/gapfill 相关表）

| 库.表 | 行数 | 说明 |
|---|---:|---|
| `gkxlumenx_gapfill.gapfill_synth_new_product_sales_ratio` | 4 | **正式 gapfill 库也有同构 3 表**（各 4 行）——正式环境种子已落 |
| `gkxlumenx_gapfill.gapfill_synth_rd_employee` | 4 | 同上 |
| `gkxlumenx_gapfill.gapfill_synth_policy_effect` | 4 | 同上 |
| `gkxlumenx_ads`（正式）/ `gkxlumenx_ai`（正式） | — | **无任何 synth 表**（正式 ADS/AI 面尚未建 SYNTH 表；demo 独有） |

另：`demo_gkxlumenx_ads` 内 `chain_*` 大表为 0 行（产业链域，非本管线范围）；`policy_effect`（155 行）为政策域既有表，**与** `gapfill_synth_policy_effect` **不是同一张表**，M3 引用时勿混。

---

## 6. 覆盖缺口总表（M3 判 `gap` / M4 登记直接引用）

| # | 缺口 | 影响叶 | 建议处理 |
|---|---|---|---|
| G-01 | 活力/要素 ADS 全部表仅 `最近3年` 窗；1y/5y 窗 0 行 | 133–136 | 非默认窗用例引 `SYNTH-*-data-gap-catalog.yaml` 既有缺口；或按实时计算链路演示（137 四维表除外） |
| G-02 | `synth_vit_rank` / `synth_elem_rank` 仅深圳上下文行 | 135 / 138 排名视图 | 按接口实际查询键判定；若按 rank_city 读取则不缺口 |
| G-03 | `TEMP_*` 反例权重档 0 行 | 134 反例用例 | legacy 反例仅 `WEIGHT_MAIN` 档可演示；`legacy_unknown` 禁复用（总控 §1） |
| G-04 | 协同 ADS 六结果表全空 | 139–141 | 一律按实时计算路径演示；不按 ADS 结果表判定 |
| G-05 | 东莞/惠州无 co_project、talent_flow 关系 | 139 图谱筛选 | 关系类型筛选在东莞/惠州仅单类型；多类型筛选用例限深圳/广州 |
| G-06 | 东莞/惠州无 batch_meta 快照 | 141 报告 | 报告用例限深圳市/广州市；东莞/惠州走实时任务路径 |
| G-07 | `synth_collab_relation_input` 仅深圳 3 行（co_project=0 值行） | 140 关系输入 | co_project 空态分支单独建用例 |
| G-08 | 136 全景 DWD 源无城市过滤（全域聚合） | 136 | 城市维度不构成缺口；但"按城筛选全景"类期望需按 AR-8 降级行为写 |
| D-01 ⚠️ | 非深圳行 `region_name` 误标「深圳」（vit dim/indicator + elem 7 表） | 133–138 | 数据缺陷（非缺口）：`region_code` 正确。建议 M4 登记修复项（seed UPDATE 语句可修）；用例期望若含城市名展示，API 必须按 region_code 返回正确名称 |
| D-02 ⚠️ | 深圳 index/weight/dim/indicator 双批次冗余（通用 seed + 档位 seed 并存） | 133–135 | 数据缺陷：查询必须按 `calc_batch_created_at DESC` 取最新批次，否则双值。M3 判定 supported 时按"接口已取最新批次"口径 |
| D-03 ⚠️ | `synth_elem_index` 四城值同源 ± 扰动 | 136/138 | 演示可用；不得当真实城市差异结论 |

---

## 7. 调查过程记录（可追溯）

- 路径 1 database-mcp：`conn_list` 命中既有分组 `gkx-mysql` 连接 `demo-gkxlumenx-ods`（host 10.50.11.76:3306，mode read-write——**本叶全程仅执行 SELECT，未写任何库**）；`conn_switch` 后 22 次 execute_query 全部成功。
- 路径 2 SSH（已按授权直接调用，未弹认证）：`zphz-jump` 可连，但机上无 mysql 客户端、无 pymysql/mysql-connector、docker 无 mysql 容器、kubectl 被 JMS 登录页拦截 → 判定不可用，未深入第 3 次尝试（符合"同一意图最多 2 次"）。
- 本叶未读取 seed SQL 明细值（静态对照仅用于列名/批次命名确认，行数以实查为准）。
- 中途 SSH 出现 3 次「Connection not found」闪断，重连后恢复；未做任何探活空转。

---

## 8. 架构合规自检（总控 §6 / 公约模板精简版）

| 铁律 | 自检 |
|---|---|
| 只读 demo 库 | ✅ 全程 SELECT；execute_query 只读面；未触碰正式 gkxlumenx_* 数据（仅 information_schema 计数） |
| 调用链/算法/图谱铁律 | ✅ 本叶零代码、零业务仓改动，不涉及 |
| 口令不进产物 | ✅ 连接复用 database-mcp 既有配置；本文件无口令/连接串 |
| cicd: skip | ✅ 纯编排仓文档 |
| ponytail | 本叶为数据调研（非编码任务），无代码产物；重复查询用聚合 SQL 压缩到 22 次内完成 28 表，未建中间产物文件 |
| 失败重试纪律 | ✅ SSH 2 次即停；database-mcp 一次成功；SQL 报错即改写不重试原句 |

---

*产物落点核对：本文件 = 总控 §1.7 `data-survey-20261107.md` 唯一产物；M3 消费本文件 §0/§6 做逐条判定。*
