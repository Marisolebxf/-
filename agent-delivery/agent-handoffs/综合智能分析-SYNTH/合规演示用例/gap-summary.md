# SYNTH 合规演示用例 · 缺口归并与修复登记汇总（M4）

> **任务 ID**：`SYNTH-DEMO-CASE-M4-GAP-L01`（长任务 `SYNTH-DEMO-CASE-CTL-L01` 段 M4；doc-agent 人格）
> **日期**：2026-11-07
> **执行**：agent:doc-agent（子智能体）
> **本文件职责**：归并 M3 判定出的缺口与数据缺陷，交叉核对既有缺口真源，登记修复建议与责任方。**只读汇编，不改任何真源文件；修数不派单不开单**（落库修复属后续任务）。
> **cicd: skip**（纯编排仓文档）

## 2026-11-08 闭合更新（SYNTH-DEMO-CASE-M6-MATRIX-UPDATE-L01）

> 本节为 M6 增量补记；下文 §A–§D 为 2026-11-07 M4 时的历史判定快照，保留不改。证据真源：`../SYNTH-DEMO-ACCEPT-LOOP.md`（R2/R3 + Q1 单）。

**时间线**：2026-11-07 下午灌数（活力 1y/5y 窗各 60 行、要素八表三窗全齐 `mock_20261107_elem_delivery_{1y|3y|5y}` 三窗各 304 行、要素历史年行 `mock_20261107_elem_hist_*` 共 48 条）→ 当晚 R2 复测暴露活力 1y/5y 假 404（**Q1 QUERY 缺口**：Java 两跳丢参）→ Q1 修复上线（lumen-svc-platform commit `558d43c`，pipeline [#4243](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/4243) `deploy:topic` success）→ **R3 复测（2026-11-08 02:20）全绿**（四城三窗全 200，VIT-01/02/16 回归无恙）。

- **G-01 ✅ 已闭合**：活力/要素 ADS 仅 3y 窗 + 要素无历史年行的前提全部失效。受影响 8 条（VIT-04/05/09/15、ELEM-02/03/12/13）在 matrix 中已全部改判 supported，`meta.summary` 重算为 **44/0/3**（supported 44 / gap 0 / partial 3；COLLAB-04/05/06 因 G-05/G-06 仍开放而维持 partial，见下两行）。本表下文 §5 汇总第 1/2 条中 G-01 相关判定同步作废，以 matrix 为准。
- **G-05 ⚠️ 仍开放**（2026-11-08 复核无变化）：东莞/惠州单类关系（仅 co_patent）未补种，COLLAB-04/05/06 仍 partial。
- **G-06 ⚠️ 仍开放**（2026-11-08 复核无变化）：东莞/惠州无 batch_meta 快照、1y/5y 无快照，走实算路径口径不变。
- **VIT-15 特别注记**：5y 出数后「5y 空窗任务失败」触发路径失效，失败态演示改为**可选演示**（任务链失败态需另造触发，属过程页行为），默认轮次不安排。

---

## 真源清单（本文件全部输入，均只读）

| # | 真源 | 角色 |
|---|---|---|
| 1 | `condition-fill-matrix.yaml`（M3，47 条 = 36 supported / 5 gap / 6 partial） | 缺口引用唯一判定源（gap_refs / m2_annotation） |
| 2 | `data-survey-20261107.md`（M2）§6 覆盖缺口 G-01~G-08 + 数据缺陷 D-01~D-03 | 缺口/缺陷编号定义真源 |
| 3 | `vitality-cases.md` / `element-cases.md` / `collab-cases.md`（M1b 三叶册） | 缺口上下文与用例期望收敛口径 |
| 4 | `SYNTH-{VITALITY\|ELEMENT\|COLLAB}-data-gap-catalog.yaml`（E8 既有真源，引用核对不改动） | metric 级 pending 真源（键 = metric_id，pending_ref = Q-SYNTH-*） |
| 5 | `agent-delivery/客户决策清单跟踪表.md`（Q-SYNTH-* / Q-ANALYSIS-01） | 业务口径决策真源 |
| 6 | `../SYNTH-合规演示用例-长任务总控.md` | 本长任务总控 |

## 对账声明（M4 ↔ M3）

- M3 矩阵 47 条中，**带缺口引用（gap_refs 非空）的 CASE = 5 gap + 6 partial = 11 条**，与 M3 summary（gap: 5, partial: 6）完全一致，零缺格、零多判。
- 去重后涉及 G 编号共 **3 个**：
  - **G-01**（活力/要素 ADS 仅最近3年窗 + 要素无历史年行）→ 8 条（gap 5 + partial 3）；
  - **G-05**（东莞/惠州/广州关系类型覆盖不全）→ 3 条（partial）；
  - **G-06**（东莞/惠州无 batch_meta 快照）→ 2 条（partial）。
- 其余 G 编号出现但**不构成 verdict 级缺口**：G-04 为合规诚实态（非缺口）；G-02 / G-03 / G-07 / G-08 仅出现在 supported 用例的空态/拦截分支注记中，不进 gap_refs。
- M4 登记行数与 M3 对账：§A 归并 8 个 G 编号（3 个 verdict 级 + 1 个合规态 + 4 个分支注记级）；§B 登记 3 项数据缺陷；§D 新登记 **0**（M3 零新造成立，核对依据见 §D）。

---

## §A 缺口归并表（按 G 编号归并）

> 「verdict 级」= 出现在 gap/partial 用例的 gap_refs 中；「分支注记级」= 仅出现在 supported 用例的空态/拦截分支依据中。全部 G 编号定义出自 M2 §6，本表不新增不改名。

| 编号 | 名称 | verdict 级影响 CASE | 分支注记级出现 | 根因（一句话） | 既有真源引用 | 修复路径建议 | 责任方 | 阻塞级别 |
|---|---|---|---|---|---|---|---|---|
| **G-01** | 活力/要素 ADS 全部表仅「最近3年」窗；1y/5y 窗 0 行；要素另无历史年行（趋势空态） | CASE-VIT-04 / 05 / 09 / 15（gap）、CASE-ELEM-02 / 03 / 13（partial）、CASE-ELEM-12（gap） | VIT-04/09 注记（Q-ANALYSIS-01）、ELEM-12 叶册 §2.1 | demo 种子仅灌最近3年窗，活力历史年批（mock_20261107_vit_trend_*）只补了活力侧、要素侧未补；1y/5y 窗活力/要素 ADS 全系无行 | **catalog 无直接键**（窗口数据面缺口，catalog 均为公式/口径类 pending，不同层）；间接关联 Q-SYNTH-V-02 🟡（默认三元组与秒开/改条件口径）、Q-ANALYSIS-01 🟡（切条件不自动建任务、当天复用）；公式层正交缺口另见 catalog 键 `M_SYNTH_VIT_INDEX`（Q-SYNTH-01）/ `M_SYNTH_ELEM_INDEX`（Q-SYNTH-02） | 后续派单由 data-agent 扩 seed：①活力/要素 ADS 补 1y/5y 窗行（或确认实时计算链路为正式路径）；②要素补 2022/2023 历史年行（对齐活力 trend 口径）；137 四维表已三窗全齐无需动 | 数据（data-agent） | **✅ 已闭合（2026-11-08）**——本行与「修复路径建议」均为 2026-11-07 M4 历史判定：11-07 下午已由 data-agent 灌数闭合（活力 1y/5y 各 60 行 + 要素三窗各 304 行 + 历史年行 48 条），再经 Q1 QUERY 修复（558d43c / pipeline 4243）后 R3 复测全绿；8 条 CASE 已全部改判 supported，见文首「2026-11-08 闭合更新」 |
| **G-05** | 东莞/惠州关系行仅 co_patent 单类（缺 co_project、talent_flow）；广州缺 talent_flow | CASE-COLLAB-04 / 05 / 06（partial） | COLLAB-08 / 09 注记（产业/关系筛选限深圳/广州执行） | C-05 gapfill 种子按城市分档灌入关系类型（深圳 3 类 / 广州 2 类 / 东莞惠州 1 类），非深圳城关系数据面覆盖不全 | catalog 键 `M_SYNTH_COLLAB_RELATION_INPUT`（pending_ref Q-SYNTH-C-01；hint 内引 Q-SYNTH-C-05）；客户决策清单 Q-SYNTH-C-05 ✅ 行 283（taxonomy 与 ODS→DWD 字段可用性 🟡） | 过渡态：data-agent 补种东莞/惠州 co_project/talent_flow 行（seed 扩展）；正式态：三方真实关系数据接入后由数据工厂按 Q-SYNTH-C-05 贴源映射 | 数据（data-agent）+ 甲方（真实三方数据） | **⚠️ 仍开放（2026-11-08 复核无变化）**——单类关系未补种，COLLAB-04/05/06 维持 partial 不改判 |
| **G-06** | 东莞/惠州无任何 batch_meta 快照；1y/5y 窗无快照 | CASE-COLLAB-05 / 06（partial） | COLLAB-16 注记（报告限深圳/广州；东莞/惠州为无快照反分支现场） | 演示环境仅预发布了深圳/广州 × 最近3年的 is_latest 快照，其余城市/窗口未走任务链发布 | **catalog 无直接键**；间接关联 Q-SYNTH-V-02 🟡（秒开承诺范围 = 默认三元组，改条件走任务） | 演示即按「无快照 → 待分析态 → 显式开始分析 → 任务实算并发布 batch_meta」路径（叶册已消化，COLLAB-02/03 同构）；如需秒开现场，可演示前由任务链预跑东莞/惠州 3y 快照（演示环境准备，非库结构修复） | 数据（data-agent，演示环境准备） | **⚠️ 仍开放（2026-11-08 复核无变化）**——无快照走实算路径口径不变，COLLAB-05/06 维持 partial 不改判 |
| **G-04** | 协同 ADS 六结果表全空（node/edge/network_stat/index/output_corr/cluster 均 0 行） | 无（不进任何 gap_refs） | COLLAB-01 / 10 / 11 / 13 / 14 注记 | **不是真缺口**：功能合规过渡口径下正式结果表不落数，展示值全部来自 gapfill 输入 + 实时计算（`dataSource=gapfill_transitional`）；cluster 空表另含 `cluster_rule_unclosed` 语义（C-02 定稿前不派生正式集群归属） | 依据 = `sdd/功能合规过渡设计-137与C05.md`（C-05）；集群判据口径 Q-SYNTH-C-02 ✅ 行 280（🟡 待甲方定稿）；catalog 键 `M_SYNTH_COLLAB_INDEX`（Q-SYNTH-C-02）为公式层正交条目 | **合规态，无需修复**——禁止按「查 ADS 结果表」写判定/补种结果行；正式落表链路启用与否属架构后续决策，不在演示管线范围 | 无（合规设计态） | 不适用 |
| **G-02** | `synth_vit_rank` / `synth_elem_rank` 仅深圳上下文行 | 无 | VIT-13 / ELEM-11 注记（非深圳上下文排名 0 行 = 诚实空态） | 种子仅灌深圳市上下文的排名行（4 个 rank_city 行挂在深圳 region_code 下） | catalog 键 `M_SYNTH_VIT_RANK`（Q-SYNTH-01）/ `M_SYNTH_ELEM_RANK`（Q-SYNTH-02）——排名正式态依赖指数公式闭合，禁止对外决策展示 | 先由 api/algorithm 确认接口查询键（按 rank_city 读深圳上下文 24/4 行则非缺口，M2 判定口径）；若按 region 上下文查询且产品要求非深圳排名视图，再由 data-agent 补行 | 算法/api（查询键确认）+ 数据（如需补行） | 不阻塞演示（深圳上下文可演示；非深圳为诚实空态分支） |
| **G-03** | `TEMP_*` 反例权重档 0 行 | 无 | VIT-10 / VIT-11 注记（legacy 反例仅 WEIGHT_MAIN 档可演示；非法档走参数校验） | TEMP_* 档未登记进种子，库内仅 INDEX_MAIN / EQUAL / WEIGHT_MAIN 三正档 | catalog 键 `M_SYNTH_VIT_WEIGHT`（Q-SYNTH-V-01 ✅ 行 275——权重档正式规则待确认 🟡） | **无需补行**——未登记档被参数校验/`legacy_unknown` 拦截即预期行为（拦截即演示价值）；是否登记 TEMP_* 档属 Q-SYNTH-V-01 甲方确认范畴 | 产品/甲方（Q-SYNTH-V-01） | 不阻塞演示（VIT-11 零数据依赖任意时候可跑） |
| **G-07** | `synth_collab_relation_input` 仅深圳 3 行（co_project=0 值行） | 无 | COLLAB-09 / 10 注记（co_project=0 为诚实 0 值展示；不影响图谱边——图谱读 gapfill 关系行） | 关系输入 ADS 面种子仅灌深圳 × 最近3年；co_project 灌了 0 值行（有行无值） | catalog 键 `M_SYNTH_COLLAB_RELATION_INPUT`（pending_ref Q-SYNTH-C-01 ✅ 行 279——主体匹配/事件去重/有效性规则待确认 🟡） | 过渡态：data-agent 如需可补非深圳 relation_input 行（演示价值有限，COLLAB-10 限深圳即可）；正式态随 Q-SYNTH-C-01/C-05 贴源接入 | 数据（data-agent）+ 甲方（真实 co_project 数据） | 不阻塞演示（深圳上下文三卡 + 0 值柱是 COLLAB-10 关键讲解点） |
| **G-08** | 136 全景 DWD 源无城市过滤（全域聚合） | 无 | ELEM-09 注记（换城全景计数不变属预期，不承诺按城筛选） | 全景面板设计为全域实时聚合（装包内聚合、无 ADS 表、3 秒超时降级 AR-8），城市维度本就不在查询键中 | **catalog 无直接键**（全景无独立 ADS metric 键，走 DWD 实时聚合） | **设计口径，无需修复**——由产品侧管理期望：不得演示/承诺「按城市过滤的全景计数」；如甲方要求按城筛选，另立需求（不在本管线） | 产品（期望口径管理） | 不阻塞演示 |

---

## §B 数据缺陷修复登记（D-01~D-03，非缺口单列）

> 数据缺陷 ≠ 缺口：不进 verdict，不引 G 编号；按 M3 口径仅在涉及 CASE 的 m2_annotation 注明，在此登记修复建议。**结论：三项均不阻塞演示**，演示按 M2 建议处理（城市名以条件栏为准 / 取最新批次 / 同源扰动不当真实差异）。

| 编号 | 缺陷 | 修复建议 | 责任方 | 是否阻塞演示 |
|---|---|---|---|---|
| **D-01** | 非深圳行 `region_name` 误标「深圳」（活力 `synth_vit_dim_score` / `synth_vit_indicator` + 要素 7 表；`region_code` 正确） | **SQL 侧（首选）**：seed 按 `region_code` 回填正确 `region_name`（UPDATE 语句可修，行数少：vit 两表非深圳行 72+216（=288），elem 7 表非深圳行合计约 213）；**查询侧（兜底）**：API/前端展示城市名一律以条件栏 `ctx.region` / `region_code` 映射为准，不信任数据行 name 字段（此口径已写入 VIT-06/07/08、ELEM-04/05/06 叶册期望）；**口径侧**：无需动作 | data-agent（seed UPDATE 修复，后续派单） | **否**——API 按 `region_code` 过滤则取数无影响；仅当页面直接展示数据行内城市名时可能串显，演示口径已约定「城市名以条件栏为准，若串名按 D-01 缺陷口径说明」 |
| **D-02** | 深圳 `synth_vit_index/rank/weight/dim_score/indicator` 双批次冗余（通用 seed + 档位 seed 并存，同键双值） | **查询侧（已固化）**：快照/趋势读取一律按 `calc_batch_created_at DESC` 取最新档位批（此口径已写入 VIT-01/02/03/12/16 叶册期望与 M3 判定）；**SQL 侧（可选）**：清理旧通用批避免歧义，或保留作 A/B 批对照演示；**口径侧**：快照选择规则文档化「同键多批取最新档位批」 | data-agent（可选清理）/ algorithm（查询口径已定，接口侧确认落地） | **否**——接口按最新批次口径取数即无双值；叶册与 M3 已按此口径写死断言 |
| **D-03** | `synth_elem_index` 四城市指数值 = 同一目标值 ± 扰动（同源，非独立计算口径）；要素排名/四维 `fill_method=demo_index_offset` 同理 | **口径侧（首选，零改动）**：演示讲解口径明确「同源 ± 扰动演示值，非独立真实城市差异，禁当真实结论」（已写入 ELEM-01/04/05/06/11 叶册期望）；**SQL 侧（可选，非必需）**：如需更真实的城市差异，由 data-agent 按独立目标值重灌（ponytail：演示目的下非必需，不建议本期做）；**查询侧**：无需动作 | algorithm（演示值生成口径）+ 产品/演示执行（讲解口径）；如重灌则 data-agent | **否**——演示可用，带 🧪 标识与讲解口径即可 |

---

## §C 与既有真源交叉引用核对

### C.1 客户决策清单（Q 编号）核对

本管线（M2 §6 + M3 matrix + 三叶册）实际引用的 Q 编号逐条核对 `客户决策清单跟踪表.md`：

| Q 编号 | 清单行 | 状态 | 本管线引用点 |
|---|---|---|---|
| Q-SYNTH-01 | 行 274 | ✅ 命中（🟡） | VIT-01 临时权重角标；G-01/G-02 间接关联（INDEX/RANK catalog 键） |
| Q-SYNTH-02 | 行 277 | ✅ 命中（🟡） | ELEM-13 局限说明段；`M_SYNTH_ELEM_INDEX/RANK` catalog 键 |
| Q-SYNTH-V-01 | 行 275 | ✅ 命中（🟡） | VIT-01 ⚠️ 角标；G-03（权重档规则） |
| Q-SYNTH-V-02 | 行 276 | ✅ 命中（🟡） | 默认三元组/秒开/改条件口径；G-01/G-06 间接关联 |
| Q-SYNTH-C-01 | 行 279 | ✅ 命中（🟡） | G-05/G-07（`M_SYNTH_COLLAB_RELATION_INPUT`） |
| Q-SYNTH-C-02 | 行 280 | ✅ 命中（🟡） | COLLAB-13 集群过渡规则；G-04 cluster 语义 |
| Q-SYNTH-C-03 | 行 281 | ✅ 命中（🟡） | COLLAB-14 仅关联非因果 |
| Q-SYNTH-C-04 | 行 282 | ✅ 命中（🟡） | COLLAB-15 建议待审核 |
| Q-SYNTH-C-05 | 行 283 | ✅ 命中（🟡） | G-05（关系类型 taxonomy 与贴源字段） |
| Q-SYNTH-E-02 | 行 186 | ✅ 命中（🟡） | ELEM-10 贡献路径仅关联非因果；ELEM-13 局限段 |
| Q-ANALYSIS-01 | 行 363 | ✅ 命中（🟡，2026-08-20 锁定临时基线） | 全部「切条件不自动建任务 / 当天复用 / 重新分析」用例（VIT-04/05/09、ELEM-02/03、COLLAB-02/03 等） |

**小结：本管线引用的 11 个 Q 编号全部命中，0 错位。**

### C.2 data-gap-catalog 键核对

G-01~G-08 是 **M2 调研报告 §6 自建的「覆盖缺口编号」**；三份 data-gap-catalog 按 **metric_id** 组织（pending_ref 指向 Q-SYNTH-*），两者是不同层级的编号体系，**不存在 G-* 与 catalog 键的直映关系，也无编号冲突**。逐项定位结果：

| G 编号 | catalog 定位 | 结果 |
|---|---|---|
| G-01 | catalog 无直接键（公式类 pending 不覆盖窗口数据面层） | 层不同，非错位；间接 Q-SYNTH-V-02 / Q-ANALYSIS-01 已在 §A 注明 |
| G-02 | `M_SYNTH_VIT_RANK`（Q-SYNTH-01）/ `M_SYNTH_ELEM_RANK`（Q-SYNTH-02） | ✅ 可定位 |
| G-03 | `M_SYNTH_VIT_WEIGHT`（Q-SYNTH-V-01） | ✅ 可定位 |
| G-04 | 无 metric 键；依据 = `sdd/功能合规过渡设计-137与C05.md`（C-05）+ Q-SYNTH-C-02（cluster 判据） | ✅ 可定位（设计文档 + Q 层） |
| G-05 | `M_SYNTH_COLLAB_RELATION_INPUT`（Q-SYNTH-C-01；hint 内引 Q-SYNTH-C-05） | ✅ 可定位 |
| G-06 | catalog 无直接键 | 层不同，非错位；间接 Q-SYNTH-V-02 已在 §A 注明 |
| G-07 | `M_SYNTH_COLLAB_RELATION_INPUT`（Q-SYNTH-C-01） | ✅ 可定位 |
| G-08 | catalog 无直接键（136 全景为 DWD 实时聚合，无独立 ADS metric 键） | 层不同，非错位 |

### C.3 发现的既有真源错位（如实登记，不改真源）

**错位 1 处（涉及 2 个 Q 编号；既有真源间问题，非本管线引入）：**

- ELEMENT catalog（`SYNTH-ELEMENT-data-gap-catalog.yaml`）中 **6 个条目引用 `Q-SYNTH-E-01`**（M_SYNTH_ELEM_TYPE_INDEX / TYPE_SCORE / LEVEL_INDEX / LEVEL_SCORE / DOMAIN_INDEX / WEIGHT）、**2 个条目提及 `Q-SYNTH-E-04`**（TYPE_SCORE / INDICATOR 的资金/空间数据缺口注）——经全文检索 `客户决策清单跟踪表.md`，**`Q-SYNTH-E-01` 与 `Q-SYNTH-E-04` 两个编号在清单中不存在（零命中）**，属 catalog → 清单引用断链。
- **影响评估：不影响本管线 M3/M4 判定**——本管线用例在要素叶实际引用的 Q 编号仅 Q-SYNTH-02 与 Q-SYNTH-E-02（均命中），未引用 E-01/E-04。
- **处置建议（后续任务，不在本叶范围）**：由 PM 核对 E8 定义包历史产物，将 E-01/E-04 补录进客户决策清单，或由 data-agent 将 catalog 条目的 pending_ref 改挂既有编号（E-01 疑似应并入 Q-SYNTH-02/E-02 族；E-04 资金/空间缺口语义疑似已被 Q-SYNTH-E-02 或贴源类 Q 覆盖）。**本叶不改动任何真源文件。**

**§C 核对结论：Q 编号 11/11 全命中（错位 0）；G 编号 8 个中 5 个可定位 catalog/Q 层、3 个属「层不同无直接键」（已在 §A 逐行注明，非编号错位）；catalog 侧反向引用清单发现断链 2 个编号（Q-SYNTH-E-01 / Q-SYNTH-E-04），不影响本管线判定。**

---

## §D 新登记区

**新登记数 = 0（预期达成，M3 零新造成立）。**

核对依据：M2 §6 的 G-01~G-08 + D-01~D-03 已覆盖本管线全部数据面观察；M3 gap_refs 引用集合 {G-01, G-05, G-06} 全部落在既有编号内；supported 用例的全部空态/拦截分支（G-02/03/07/08、batch_meta_missing、no_year_on_source、cluster_rule_unclosed、insufficient、no_year_on_source 不触发分支等）均有既有编号或叶册 reason 语义承接。

排查过的「疑似新缺口」候选及其归属判定（防硬塞也防漏登，逐条留痕）：

| 候选 | 判定 | 依据 |
|---|---|---|
| `synth_vit_trend` 表不存在（总控 §3 清单所列，M2 §1.6 实查零命中） | **非新缺口** | 本质 = 要素/活力趋势历史年行缺失（G-01 组成部分）+ 总控清单笔误（表不该存在）；已被 M1b/M3「趋势依赖 `synth_vit_index` 历史年行」口径完全消化（VIT-14/16 附录 A 修正索引） |
| 协同 1y/5y 窗无快照 | **非新缺口** | G-06 定义已含「1y/5y 窗无快照」子句（M2 §3.6 / F4）；且协同 gapfill 输入带年份，非默认窗任务可实算（COLLAB-02/03 supported），与活力/要素 1y/5y 空窗（G-01）语义不同、编号未混用 |
| 任务链表（#102–#105）非 ADS、M2 未覆盖（VIT-10/15 演示前置依赖存量任务） | **非缺口，属演示前置核对项** | 任务链表非 ADS 数据面，超出 M2 调研范围（总控 §3 清单未列）；VIT-10 已按叶册口径登记「演示前置缺失」处置（需演示前人工确认存量旧任务），不新增编号 |
| 全景 DWD 四源表 `table_rows` 估算值与 `is_deleted=0` 精确计数不一致 | **非缺口** | InnoDB `table_rows` 本为估算值，M2 已按 is_deleted=0 精确计数为准；ELEM-09 期望写「真实 DWD 汇聚计数」，无判定冲突 |

> 如后续执行中发现本表之外的真缺口，须另开任务登记并按 M2 §6 编号规则顺延（G-09 起），不在本文件追加。

---

## §5 汇总

1. **gap 计 5，全部引 G-01**：CASE-VIT-04 / 05 / 09 / 15（活力 1y/5y 空窗：404/引导开始分析、失败分支确定性触发器）+ CASE-ELEM-12（要素趋势：无历史年行 → 「暂无数据」诚实空态）。
2. **partial 计 6**：CASE-ELEM-02 / 03 / 13（引 G-01，主期望收敛 404/引导或趋势段空态，137 四维过渡卡例外可出）+ CASE-COLLAB-04 / 05 / 06（引 G-05 / G-06，图谱关系类型降级 / 无快照任务实算路径）。
3. **数据缺陷 3 项（D-01 / D-02 / D-03）均不阻塞演示**：按 M2 建议口径处理——城市名以条件栏为准（D-01）、快照按 `calc_batch_created_at` 取最新批（D-02）、同源 ± 扰动不当真实差异结论（D-03）；修复建议见 §B，**落库修复属后续派单，本长任务不修库**。
4. **缺口正式修复全部走后续派单**（不在本长任务范围）：G-01 seed 窗口扩展（data-agent）、G-05 关系类型补种（data-agent）/三方贴源（数据工厂）、G-06 快照预发布（演示环境准备）；G-04 为合规诚实态无需修复；G-02/03/07/08 为分支注记级，按 §A 各行责任方处理。
5. **交叉引用结论**：Q 编号 11/11 全命中；G 编号无错位；既有真源断链 1 处（catalog 引 Q-SYNTH-E-01 / E-04 清单缺失，不影响本管线，建议后续任务处置）；**新登记 0**。
6. **对账闭环**：M4 §A verdict 级缺口引用（11 条 CASE × {G-01, G-05, G-06}）与 M3 summary（gap 5 + partial 6）完全一致，总验收条件「M4 缺口数 = M3 gap 数」达成。
