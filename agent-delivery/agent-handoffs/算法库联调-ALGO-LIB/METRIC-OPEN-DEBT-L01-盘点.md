# METRIC-OPEN-DEBT-L01 · 盘点表

> 对照 `给人说明` §8.4 甲/乙/丙/丁。现网 MCP：2026-08-22（`*-METRIC-OPEN-L01` **26** 条匹配，其中真正 OPEN 叶 = 原 15 + 态势 9 + 本 DEBT 1；`ENT-MOD-EVAL-READINESS-UI-L01` **不算** OPEN）。  
> **每一行有且仅有一种处置。** 口径/8 件套/适用性主责本工作流 = `human:淮政玮`；公式/`algorithm_type` = `human:唐绍祖`。不改 seed。不替甲方 🟡→🟢。不挡 A1。  
> 本文件由 `METRIC-OPEN-DEBT-L01` 交付；甲表 **禁止本叶 `task-create`**。

**处置合计**：签收 **0** · 原叶扩 **15** · 建 backlog **7** · 书面顶 PACK **9** · 不建 **16**。

---

## 甲、从未建叶 → 建 backlog（7）

专题政策 **禁止**另开 `TOPIC-POLICY-METRIC-OPEN-L01`（扩 `POLICY-METRIC-OPEN-L01`，见乙）。无 PACK 一律 `depends_on: []`，**不得 ready**。

| ID | 覆盖 | 现网 | 处置 | 建议 epic | depends_on |
|----|------|------|------|-----------|------------|
| `SVCCHAIN-METRIC-OPEN-L01` | 机构分析/生态/招引/门户（A2：SVCCHAIN-* 四页） | Epic `E7-产业服务链分析` 仅前端 R1/R2/R2C，**0** OPEN | 建 backlog | `E7-产业服务链分析` | `[]`（R1/R2/R2C 已声称五件套，**不是** `*-PACK-L01`） |
| `TOPIC-ENT-METRIC-OPEN-L01` | 专题企业 `TOPIC-ENT-05`（欠账 12） | registry 0；**禁止**挂 `ENT-MOD-*-METRIC-OPEN` | 建 backlog | `E-ALGO-LIB-DEMO`（现网无专题企业 Epic；邻近展示企业 = `E-ENT-SCRUM-PDR` **不可挂**） | `[]`（无 PACK，仅 `05.3-企业.md`） |
| `TOPIC-TECH-METRIC-OPEN-L01` | 专题技术链 `TOPIC-TECH-05`（欠账 6） | registry 0 | 建 backlog | `E-ALGO-LIB-DEMO`（邻近 `JIUXIN-TECH-ORG-TALENT-L01`） | `[]`（`05.1-技术链.md`） |
| `TOPIC-ORG-METRIC-OPEN-L01` | 专题科研机构 `TOPIC-ORG-05`（欠账 6） | registry 0 | 建 backlog | `E-ALGO-LIB-DEMO` | `[]`（`05.4`） |
| `TOPIC-TALENT-METRIC-OPEN-L01` | 专题人才 `TOPIC-TALENT-05`（欠账 12） | registry 0；与展示 DS-13～16 **分叶** | 建 backlog | `E-ALGO-LIB-DEMO` | `[]`（`05.5`） |
| `TOPIC-QUERY-METRIC-OPEN-L01` | 专题查询 `TOPIC-QUERY`（欠账 5） | registry 0；有统计数字不能口头 N/A | 建 backlog | `E-TOPIC-SEARCH` | `[]` |
| `ZHIKU-METRIC-OPEN-L01` | 智库（核对记录已在盘） | registry **无** OPEN；④⑤ 草稿已有 | 建 backlog | `E-ZHIKU-PROTOTYPE-110` | `[]`（补登记，不是从零做④⑤） |

建单 JSON 字段级清单见 handoff「给 coordinator 的下步」。

---

## 乙、叶已在 · 覆盖错位 → 原叶扩（4）

本 DEBT 叶 **已改文档**，不是只写待执行。

| 页 | 已有任务 | 现网状态 | 处置 | 本叶改了什么 |
|----|----------|----------|------|--------------|
| 专题 E7-POLICY | `POLICY-METRIC-OPEN-L01` | integration | 原叶扩 | 核对记录 §1.1/§1.2：P-70/P-72/P-73 **必须消费**；TRACE/A2 指针；**禁止** `TOPIC-POLICY-METRIC-OPEN-L01` |
| ENT-E33 | `ENT-MOD-KEYPANO-METRIC-OPEN-L01` | integration | 原叶扩 | 核对记录封面 + §8：PACK=E-33 vs 目录 E-20/E-22；catalog 不得再标 E-33 missing OPEN |
| ENT-E35 | `ENT-MOD-SHENZHEN-METRIC-OPEN-L01` | ready_to_sign | 原叶扩 | 核对记录 §8：**E-35 列**（相对 E-25）；TRACE `metric_id` 全 null 在本叶补，不新建 |
| ENT-COMPARE | `ENT-MOD-COMPARE-METRIC-OPEN-L01` | **done** | 原叶扩 | **新建** `ENT-COMPARE/METRIC-OPEN-ENT-COMPARE-核对记录.md`；任务保持 done |

智库补登记见甲表 ZHIKU，不在本表「原叶扩」。

---

## 丙、叶已有 · ④⑤ 没写清 → 原叶扩（12；与乙重叠 POLICY 1 条）

独立 11 条 + POLICY 的 QPOL/展示政策债（并进乙的 POLICY 行）。**禁止平行新开 OPEN。** CHAIN **禁止**打 missing。SYNTH **不要**标 done。

| Task ID | 状态 | 缺什么 ④⑤ | 建议补在 | 挡签收？ |
|---------|------|-----------|----------|----------|
| `CHAIN-METRIC-OPEN-L01` | **done** | 深圳对比四维已在核对记录（`M_CHAIN_SZ_ADVANTAGE_SCORE` 等 + QC08）；B 轨已有 `M_CHAIN_*` | `METRIC-OPEN-CHAIN-核对记录.md` 保持；口径会签改挂淮政玮（纪要/note），**禁止** A2/catalog 打 missing | **否**（已签）。本 DEBT 只禁止误打 missing |
| `SYNTH-MOD-VITALITY-METRIC-OPEN-L01` | ready_to_sign | ④ 5 条公式 `pending_algorithm`；⑤ Q-SYNTH-01/V-01/V-02 已登记未闭合 | `METRIC-OPEN-SYNTH-VITALITY-核对记录.md`；公式仍待唐绍祖 | **保持 ready_to_sign**，不标 done |
| `SYNTH-MOD-ELEMENT-METRIC-OPEN-L01` | ready_to_sign | ④ 10 条 `pending_algorithm`；⑤ Q-SYNTH-02/E-01/E-02/E-04 | `METRIC-OPEN-SYNTH-ELEMENT-核对记录.md` | 同上 |
| `SYNTH-MOD-COLLAB-METRIC-OPEN-L01` | ready_to_sign | ④ 6 条公式 pending；⑤ Q-SYNTH-03/C-01～C-05 | `METRIC-OPEN-SYNTH-COLLAB-核对记录.md` | 同上 |
| `POLICY-METRIC-OPEN-L01` | integration | 展示 DS-10/11/12 口径未定 / QPOL-01/02/03/05/07 全 🟡；专题三页指针见乙 | `METRIC-OPEN-E7-DS10-12-核对记录.md`（已加 §1.2）；QPOL 不升 🟢 | 挡门 1「无条件闭合」；不挡本 DEBT |
| `ENT-MOD-SEARCH-METRIC-OPEN-L01` | done | 口径会签仍写王惠；Q011/Q033～Q037/Q019 🟡 | `METRIC-OPEN-ENT-SEARCH-核对记录.md` 加本工作流 `owner_semantic=淮政玮` | 否（已签） |
| `ENT-MOD-EVAL-METRIC-OPEN-L01` | done | Q014 权重 / Q019 市场份额未闭合 | `METRIC-OPEN-ENT-EVAL-核对记录.md` 改挂口径主责 | 否 |
| `ENT-MOD-RISK-METRIC-OPEN-L01` | done | Q017/Q018 阈值 🟡；GRAPH 步骤未终签 | `METRIC-OPEN-ENT-RISK-核对记录.md` | 否 |
| `ENT-MOD-RECRUIT-METRIC-OPEN-L01` | done | Q015 权重；GAP-RECRUIT-METRIC-01～05 无正式 ID | `METRIC-OPEN-ENT-RECRUIT-核对记录.md` | 否 |
| `ENT-MOD-OVERVIEW-E32-METRIC-OPEN-L01` | done | ④ `M_ENT_RESEARCHER_COUNT` 等 pending；⑤ Q-E32-01/02；PDR-05/06 待会签 | `METRIC-OPEN-ENT-E32-核对记录.md` | 否（已签）；公式仍待唐绍祖 |
| `ENT-MOD-STAR-METRIC-OPEN-L01` | integration | Q041/Q048 明星定义 🟡；CMS 侧 2 条 | `METRIC-OPEN-ENT-STAR-核对记录.md` | 挡该叶签收（待口径会签改挂淮政玮） |
| `ENT-MOD-OPS-METRIC-OPEN-L01` | integration | #4 N/A（CMS）已有据；⑤ Q-OPS-* / Q020 等；王惠会签未做 | `METRIC-OPEN-ENT-OPS-核对记录.md` | 挡该叶签收；口径 N/A 仍改挂淮政玮审开放项 |

**SYNTH 三叶建议**：保持 `ready_to_sign`；口径会签改挂 `human:淮政玮`；公式/`algorithm_type` 仍待 `human:唐绍祖`。**不要**擅自标 done。

---

## 丁、与 8/25 / A2 的边界 → 不建

| 东西 | 是缺 OPEN 叶？ | 处置 |
|------|----------------|------|
| A2 `missing` 专题 **7** | 否（库覆盖差） | **不建** |
| A2 `missing` 展示 **70** | 否 | **不建** |
| A2 语义欠账（111+247） | 多数是丙或乙，少数是甲 | 甲已建单清单；其余不把差集当缺叶 |

**不把丁写进甲表。** 不签收 `TOPIC-ALGO-GAP-L01` / `DS-ALGO-GAP-L01`。

---

## 态势 9 叶 · 书面顶 PACK（已建，保持 backlog）

| Task ID | 状态 | 处置 |
|---------|------|------|
| `DS-01-METRIC-OPEN-L01` … `DS-09-METRIC-OPEN-L01` | 全 **backlog** · epic `E-DISPLAY-ALIGN` | **书面顶 PACK**（本叶 **不**标 ready；SRS `02` + `04-功能-科技发展态势.md` 顶 PACK 须淮政玮 **另批**） |

FDS **不顶** PACK/OPEN。9 叶 **不** `depends_on` 尚不存在的 FDS。

---

## 其余展示缺叶 / N/A · 不建（本批只记录）

| 对象 | 处置 | 说明 |
|------|------|------|
| `DS13-16-TALENT-METRIC-OPEN-L01` | 不建 | 与专题人才 **分叶**；本批不建 |
| `DS21-24-GRAPH-METRIC-OPEN-L01` | 不建 | |
| `DS25-29-ACHIEVE-METRIC-OPEN-L01` | 不建 | |
| `DS30-SVC-METRIC-OPEN-L01` | 不建 | |
| DS-17～20 数据资源 | 不建 | catalog 默认 `n/a_ops`；过门 1 另写 **N/A 核对记录**，不必算法语义卡 |
| `TOPIC-POLICY-METRIC-OPEN-L01` | 不建 | **禁止**；扩 POLICY 叶 |
| SYNTH-REGION 父索引 | 不建 | 三兄弟已有 OPEN |
| `TOPIC-OPS` / `TOPIC-DATAREQ` | 不建 | N/A + 依据，不算缺 OPEN |
| `ENT-MOD-EVAL-READINESS-UI-L01` | 不建 | 前端刷新，**不算** OPEN |
| `TOPIC/DS-METRIC-INVENTORY-L01`、`TOPIC/DS-METRIC-CLASSIFY-L01` | 不建 | **废作**，勿碰、不标 done |

---

## 现网 15 条原 OPEN 叶（对照 §8.4 丙清单）

`CHAIN` · `POLICY` · `SYNTH-VITALITY` · `SYNTH-ELEMENT` · `SYNTH-COLLAB` · `ENT-SEARCH` · `ENT-COMPARE` · `ENT-KEYPANO` · `ENT-STAR` · `ENT-SHENZHEN` · `ENT-EVAL` · `ENT-RISK` · `ENT-RECRUIT` · `ENT-OPS` · `ENT-OVERVIEW-E32`

外加态势 9 条 backlog + 本 DEBT 叶。甲表 7 条 **尚未**在 registry。
