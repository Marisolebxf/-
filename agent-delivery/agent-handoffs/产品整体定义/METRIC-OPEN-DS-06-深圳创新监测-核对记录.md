# METRIC-OPEN-DS-06-深圳创新监测-核对记录

> **任务**：DS-06-METRIC-OPEN-L01（METRIC-OPEN-LOOP Round 13 / 波 B）  
> **角色**：product-agent（口径草稿）+ algorithm-agent / data-agent（协作核对，本叶不改 seed）  
> **监管人**：`human:淮政玮`（DoD 里「淮政瑎」是错字，以玮为准）  
> **日期**：2026-08-22  
> **上游**：无独立四件套 / PACK-L01；本工作流书面 **SRS 02 深圳创新监测 + 详设 04 顶 PACK**（给人说明 §8.4 甲）  
> **范围**：展示 catalog `ds_id=DS-06` **全部 4 个** `page_id` 的 ④ 指标语义卡 + ⑤ 开放项。不替甲方拍板；公式 / `algorithm_type` **不签**，标 `pending_cosign: human:唐绍祖`（8/25 前不派唐绍祖开工本 loop）。  
> **预测 / 501**：详设 04 DS-06 **未给**预测 501；CITY seq 134 趋势跟 186，差集 **mapped 保持**，预测公式未冻走 SZCITY-B04，**禁止**借 501 伪闭合、禁止改 missing。

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ 适用且文档闭合（口径草稿） | 4 页 **全部 kit**（无整页 N/A）。CITY 有城际对比/排名/指数/竞争力/趋势/人才指数；CARRIER 有载体价值排名；INDICATOR 有十一维看板数；DOMAIN 有领域四字段。SRS 02 / 详设 04 / A2 页 yaml **未挂**任何正式 `metric_id` → 卡面只用 **`TEMP_DS06_*`**。**禁止**发明正式 `M_*` 写入 seed。 |
| #5 开放项 | ✅ 适用且已登记（本记录） | 沿用 A2 已写语义债 `SZCITY-B01..B04` / `CAR-B01` / `IND-B01..B02` / `DOM-B01..B02`。**不新建** `Q0xx`（避免与展示企业 Q010～Q019、政策 QPOL、指数 Q-TINDEX-01 撞号）。本叶不改 `客户决策清单跟踪表.md`、不升 🟢、不新建 `data-gap-catalog`（文案真源 = 本 §4 + A2 `semantic_debt`）。 |
| PDR-05 自检 | ⏳ 有条件 | 无 TRACE/WF 第 6 列；本记录 + A2 `pages/DS-06-*.yaml` 可回指。门 1 完整闭合仍须正式 ID 会签（不发明）+ 公式会签 + 甲方 🟡。 |
| PDR-06 自检 | ⏳ 有条件 | STAT 看板可写演示公式；CITY 对比/排名/竞争力/趋势与 CARRIER 价值排名的 MIXED/MODEL 公式 `pending_cosign`。招标对比分项 vs 186 四维显式挂 SZCITY-B03。 |
| 语义 Owner（本工作流） | `human:淮政玮` | 口径 / 8 件套身份项 / 适用性 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop 不签公式、不改 seed `algorithm_type` |

**结论**：DS-06 **非整包 N/A**。四页均有统计数字 / 排名 / 看板 → **出卡**。GIS / 筛选 / 订阅 / 导出 / 建议文案 **N/A + 依据**。甲方 🟡 / 公式未签 **不阻断**定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。**501 不是本页覆盖通道。**

### §1.1 本叶必须消费本核对记录（catalog 4 页）

| 页 `page_id` | 中文（需规五级） | ④ | 消费的 ID | 禁止 |
|--------------|------------------|----|-----------|------|
| `DS-06-CITY` | 科技发展城市分析展示 | **kit** | `TEMP_DS06_CITY_COMPARE` · `TEMP_DS06_CITY_RANK` · `TEMP_DS06_CITY_INDEX` · `TEMP_DS06_CITY_COMPETE` · `TEMP_DS06_CITY_TALENT_INDEX` · `TEMP_DS06_CITY_TREND` | 改挂 `M_SYNTH_VIT_*` / `M_SYNTH_ELEM_*`；按号 mapped 技术链 130–135；混挂 DS-04-CITY 全球页行 / DS-05 湾区 SWOT；用 CITY 趋势顶替 INDICATOR seq 121 |
| `DS-06-CARRIER` | 深圳市创新载体综合展示 | **kit** | `TEMP_DS06_CARRIER_VALUE_RANK` | 改挂 `M_SVC_ORG_TECH_SCORE` / seq 141/151/182–191；按号 mapped 图谱 API seq 116；混挂 `DS-04-CARRIER-RANK` 全球榜为本页正式 ID（同源缺口只 `also_in`） |
| `DS-06-INDICATOR` | 科技发展指标展示 | **kit** | `TEMP_DS06_IND_KPI_BOARD` | 按号 mapped 产业链 118–123；改挂 `M_CHAIN_REG_*` / `M_SVC_SZ_COMPARE_METRIC`；复制 GBA-CAPACITY 指标计算 / GBA-INDICATOR 勾选判定；用 CITY seq 130/134 顶替本页字面对比/时序 |
| `DS-06-DOMAIN` | 深圳市各科技领域分布展示 | **kit** | `TEMP_DS06_DOMAIN_KPI` | 硬挂技术链 seq 133 / 189；改挂 `M_SVC_PT_SZ_FIELD_DIST` / `M_CHAIN_SZ_*`；把 CITY 竞争力「优势领域」或 seq 133 城市建议算进 seq 128 |

**本叶不消费**：专题 TOPIC-ENT / SYNTH / CHAIN / SVC / POLICY OPEN；展示 ENT-MOD-*；DS-04 CITY/CARRIER 正式 ID；DS-05 湾区；DS-08 指数 / Q-TINDEX-01；DS-10–12 / POLICY。B 轨已有 ID **不得 missing、不得改挂**为本页正式 ID。已 mapped 的 186 **不得改挂** `M_SYNTH_*`。

### §1.2 需规 24 叶 × 差集（对照 A2；本叶不改判定）

| 五级 | seq | 招标叶子 | A2 差集（保持） | ④ |
|------|-----|----------|-----------------|----|
| 载体综合 | 112 | 多层级地理展示 | other_system | 无独立核（GIS） |
| 载体综合 | 113 | 载体详情查看 | other_system | 无独立核；排名消费 TEMP_VALUE_RANK |
| 载体综合 | 114 | 创新价值排名展示 | **missing** | **kit** |
| 载体综合 | 115–117 | 订阅 / 筛选搜索 / 载体对比 | n/a_ops ×3 | 无独立核 |
| 指标展示 | 118 | 指标体系展示 | other_system | 无独立核（catalog 口径树） |
| 指标展示 | 119 | 多维度指标展示 | other_system | **kit**（看板） |
| 指标展示 | 120–123 | 可视化 / 字面时序 / 字面对比 / 详情 | other_system ×4 | 无独立核（同一看板读面） |
| 领域分布 | 124 / 126 | 热力图 / 空间分布分析 | other_system | 无独立核（GIS） |
| 领域分布 | 125 / 128 | 领域筛选 / 分析与建议 | n/a_ops | 无独立核 |
| 领域分布 | 127 | 详细数据指标展示 | other_system | **kit** |
| 城市分析 | 129 / 135 | 城市选择 / 报告导出 | n/a_ops | 无独立核 |
| 城市分析 | 130–132 / 134 | 指标对比 / 排名 / 竞争力 / 趋势 | **mapped** 186 | **kit**（TEMP_，不改挂 SYNTH ID） |
| 城市分析 | 133 | 发展建议提供 | other_system | 无独立核 |
| 城市（半成品） | — | 行57 排名 / 行58 指数 | **mapped** 186 | kit（RANK / INDEX） |
| 城市（半成品） | — | 行59 深圳重点人才指数 | other_system（智库） | kit TEMP_TALENT_INDEX（不 mapped 184） |
| 城市（半成品） | — | 行60–63 竞争力四子项 | **mapped** 186 | kit（消费 TEMP_COMPETE） |

**库缺口 missing 行保持 missing（本 catalog 仅 CARRIER seq 114 = 1 条）。** 不得因本 OPEN `present` 改 mapped。CITY 对比/排名/竞争力/趋势已 mapped 186，本叶只补语义卡，不改差集、不改挂 `M_SYNTH_VIT_*`。

### §1.3 TRACE / A2 语义层指针（Round 18 才回写 catalog 正文）

本叶 **不改** `metrics/request/展示系统/A2-GAP-page-catalog.yaml` 与 pages yaml 正文。指针写入 `_work/open-loop/DS-06-METRIC-OPEN-L01-a2-patch.yaml`（**不**写共享 `METRIC-OPEN-LOOP-a2-patch.yaml`）。

| 层 | 路径 | 本叶要求的指针 |
|----|------|----------------|
| 核对记录 | **本文件** | DS-06 四页唯一 OPEN 真源 |
| A2 页 yaml | `metrics/request/展示系统/pages/DS-06-*.yaml` | 应收口：`metric_open_status: present`；`metric_open_path` = 本文件；`metric_open_task: DS-06-METRIC-OPEN-L01`。**库缺口 `missing` 不动**。 |
| A2 catalog | `A2-GAP-page-catalog.yaml` 的 `ds_id=DS-06` 四页（DW5 三页 + DW6 DOMAIN） | 删「无 METRIC-OPEN → 只记语义欠账」中已被本叶覆盖的句 |
| TRACE / WF | **无**展示四件套 | `trace_metrics` / `wireframe_metric_ids` 保持空；不从 02 叙述发明 `M_*` |
| PACK | 无独立 `DS-06-PACK-L01` | SRS 02 + 详设 04 顶 PACK；FDS **不顶** OPEN |

口径会签：`owner_semantic = human:淮政玮`；公式 / `algorithm_type` 共签仍 `human:唐绍祖`。页面要哪些指标主责（展示）= `human:李伟`（给人说明），**不定**本叶清单、不改挂。

---

## §2 模块消费矩阵（TEMP_ 草稿 · 禁止写入 seed）

> OPEN 阶段 `TEMP_*` ≠ 正式 `M_*`。赋号后正式 ID 见 **§赋号表** / `id-assign/`；**仍禁止**写入 `metrics/registry/` seed。  
> 下表 `algorithm_type` 为 OPEN 草稿；赋号建议以 §赋号表为准（人才指数 OPEN=STAT → 赋号建议 `third_party`，未签）。差集列维持 A2 已写判定。

| temp_id | 主落点 | 适用 | 建议 type（未签） | 差集保持 | pending |
|---------|--------|------|-------------------|----------|---------|
| TEMP_DS06_CITY_COMPARE | CITY seq 130 | ✅ kit | MIXED | mapped 186 | SZCITY-B03 分项≠四维；禁技术链 130；禁改挂 `M_SYNTH_VIT_INDICATOR` |
| TEMP_DS06_CITY_RANK | CITY seq 131 + xlsx 行57 | ✅ kit | MIXED | mapped 186 | SZCITY-B02；禁 `M_SYNTH_VIT_RANK` / seq 182 |
| TEMP_DS06_CITY_INDEX | CITY xlsx 行58 | ✅ kit | MIXED | mapped 186 | 排名底物；禁 `M_SYNTH_VIT_INDEX`；≠ INDICATOR 指标树 |
| TEMP_DS06_CITY_COMPETE | CITY seq 132 + xlsx 行60–63 | ✅ kit | MIXED | mapped 186 | 非湾区 SWOT；禁硬挂 188–190；禁 `M_CHAIN_BOTTLENECK_*` |
| TEMP_DS06_CITY_TALENT_INDEX | CITY xlsx 行59 | ✅ kit | STAT | other_system | 智库封装；禁 mapped 184 |
| TEMP_DS06_CITY_TREND | CITY seq 134 | ✅ kit | MIXED | mapped 186 | SZCITY-B04 预测未冻；**无 501**；禁技术链 134；禁 INDICATOR seq 121 |
| TEMP_DS06_CARRIER_VALUE_RANK | CARRIER seq 114 + xlsx 行56 | ✅ kit | MODEL | **missing** | CAR-B01；also_in DS-04-CARRIER-RANK（不改挂）；禁 `M_SVC_ORG_TECH_SCORE` |
| TEMP_DS06_IND_KPI_BOARD | INDICATOR seq 119（118/120–123 消费同一读面） | ✅ kit | STAT | other_system | IND-B02；十一维不拆行；禁产业链 118–123；禁 CITY 对标顶替 |
| TEMP_DS06_DOMAIN_KPI | DOMAIN seq 127 | ✅ kit | STAT | other_system | DOM-B02；四字段不拆 M_*；禁 `M_CHAIN_SZ_*` / 133 |

**9/9 TEMP_ 均 present。** 不得因「口径未冻 / D1 missing / 无正式 M_*」把上表改成差集 `mapped`，也不得把 CARRIER missing 改成 mapped。

---

## §赋号表（TEMP → M_* · 2026-08-22 · 类型未签）

> 协议：`METRIC-ID-ASSIGN-LOOP-循环工程.md`。ELEMENT=`INNOV`。真源机器卡 `TEMP_DS06_*` → 正式 ID（VARIANT=`SZ`）。  
> **reuse=0**：CITY/载体与 `M_SYNTH_VIT_*` / `M_SYNTH_ELEM_*`、DS-04 全球城市/全球载体、DS-05 湾区 **不同口径**，禁止改挂。  
> CITY 对 seq 186 **mapped 读面保持**；正式号是 `M_INNOV_CITY_*_SZ`，**禁止**改挂 `M_SYNTH_VIT_*`。  
> CARRIER 价值排名 **missing 保持**；`also_in` DS-04-CARRIER-RANK，**不改挂** `M_INNOV_CARRIER_*_GLOBAL`。  
> 身份草稿只在本表 + `id-assign/`；**不写 seed / 展示 catalog / 共享 QUESTIONS。**

| temp_id | metric_id | reuse_of | 建议 type | pending_ref |
|---------|-----------|----------|-----------|-------------|
| TEMP_DS06_CITY_COMPARE | M_INNOV_CITY_COMPARE_SZ | 不复用 `M_SYNTH_VIT_INDICATOR` / `M_INNOV_CITY_BENCHMARK_GLOBAL` | MIXED | Q-MO-DS06-01 |
| TEMP_DS06_CITY_RANK | M_INNOV_CITY_RANK_SZ | 不复用 `M_SYNTH_VIT_RANK` / `M_INNOV_CITY_RANK_GLOBAL` | MIXED | — |
| TEMP_DS06_CITY_INDEX | M_INNOV_CITY_INDEX_SZ | 不复用 `M_SYNTH_VIT_INDEX` / `M_INNOV_GBA_CAPACITY_INDEX` | MIXED | — |
| TEMP_DS06_CITY_COMPETE | M_INNOV_CITY_COMPETE_SZ | 不复用 `M_INNOV_GBA_SWOT_*` | MIXED | Q-MO-DS06-03 |
| TEMP_DS06_CITY_TALENT_INDEX | M_INNOV_CITY_TALENT_INDEX_SZ | 不复用 DS-04 GLOBAL / seq 184 | third_party | Q-MO-DS06-02 |
| TEMP_DS06_CITY_TREND | M_INNOV_CITY_TREND_SZ | 不复用 CITY 预测号顶 INDICATOR 121 | MIXED | —（无 501；SZCITY-B04 公式未冻） |
| TEMP_DS06_CARRIER_VALUE_RANK | M_INNOV_CARRIER_VALUE_RANK_SZ | 不复用 `M_INNOV_CARRIER_*_GLOBAL` / `M_SVC_ORG_TECH_SCORE` | MODEL | —（missing 保持；also_in DS-04） |
| TEMP_DS06_IND_KPI_BOARD | M_INNOV_KPI_BOARD_SZ | 不复用 `M_INNOV_KPI_BOARD` | STAT | — |
| TEMP_DS06_DOMAIN_KPI | M_INNOV_DOMAIN_KPI_SZ | 不复用 `M_CHAIN_SZ_*` / `M_SVC_PT_SZ_FIELD_DIST` | STAT | — |

**计数**：赋号 9 / reuse 0 / 新建 9 / Q 3 / 废弃 0。类型分布：MIXED 5 · STAT 2 · MODEL 1 · third_party 1（无 UNKNOWN）。叶级卡：`metrics/request/_work/id-assign/DS-06-METRIC-OPEN-L01.yaml`；Q：`…/DS-06-METRIC-OPEN-L01-questions.yaml`。

撞号（`metric-registry-lib`，MCP 本会话未挂载，未整文件读 seed）：拟号 9 条 seed 全 MISS；Wave A 已占 `M_INNOV_CITY_*_GLOBAL` / `M_INNOV_CARRIER_*_GLOBAL` / `M_INNOV_KPI_BOARD` / `M_INNOV_GBA_*`，本叶用 `_SZ` 变体不撞。`M_SYNTH_VIT_RANK`=对比范围活力排名（专题 Job）；`M_ENT_CITY_RANK`=企业多城市对标（禁消费）。

---

## §3 ④ 指标语义卡（按 page_id · 不写 seed）

身份项由淮政玮本工作流确认适用。公式 / 权重 / `algorithm_type` 一律 `pending_cosign: human:唐绍祖`。源表以详设 04「DS-06 = M/G1 · ADS；可选 A；以 M 为主」+ A1 双表未交为准，**不**把项目 DWD 反推成 ODS `full`。

8 件套草稿字段（TEMP_ 共同）：正式 `metric_id` 见 **§赋号表**（下表仍列 `temp_id` 对照）；源系统=科技信息展示系统·深圳创新监测 / display；更新频率=未定；version=`draft-open-ds06`；源表=ADS（A1 表2 未交 → 本叶不填伪 full）。调用链：前端 `/display` → Java display BFF（GIS 图层 + metrics catalog）→ 只读 ADS；Java 不写 NLP / 不直连 nGQL。CITY 对照 186 **不在本页跑专题 SYNTH Job**。`algorithm_type` 为建议、未签。

### §3.1 `DS-06-CITY` · kit（seq 129–135）

对象=**深圳 vs 对标城市**（国内主要城市 + 国际创新城市）。catalog 对照 05 综合 186。本页是**深圳城市读面**，不跑专题 SYNTH-VITALITY Job，**禁止**改挂 `M_SYNTH_VIT_*` 为本页正式 ID。与 DS-04-CITY **同叶不同页**：可同源 mapped 186，**禁止**复制全球页行、禁止把全球 TEMP_DS04_CITY_* 当本页 ID。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS06_CITY_COMPARE | 深圳科技发展指标对比 | 深圳市与选定城市在研发投入、专利数量、高新技术企业数量、创新人才等指标上的对比分析。对象=城市，不是载体、不是湾区。对照 05 seq 186 横向对比 + 单维/分项评分。招标分项 ≠ 186 四维（科技/产业/人才/政策）→ SZCITY-B03，不另开 A | 演示：随 186 横向对比；权重未签。禁止拼 182–185、禁止 mapped 191 | MIXED |
| TEMP_DS06_CITY_RANK | 深圳城市科技发展排名 | 深圳在不同科技发展指标上的全国或全球排名（名次）。半成品行57「深圳创新排名」同叶消费。对照 seq 186 指数排序；与 SYNTH-VITALITY / DS-04-CITY **同叶不同页** | 演示：186 指数排序；禁止 seq 182 成果指数顶替综合排名 | MIXED |
| TEMP_DS06_CITY_INDEX | 深圳创新能力指数 | 衡量深圳在创新资源、创新主体、创新环境等方面综合水平的指数值；排名底物。不是 CARRIER 行56，不是 INDICATOR 指标树 | 随 186 活力指数；禁止改挂 `M_SYNTH_VIT_INDEX` | MIXED |
| TEMP_DS06_CITY_COMPETE | 深圳科技竞争力 | 对深圳市科技竞争力的分析读面：优势领域、薄弱环节、发展潜力、发展水平。对照 seq 186「优势与短板分析报告」+ 模型目的「发展潜力」。**不是**湾区 SWOT 四象限（禁止套用 DS-05-GBA-ANALYSIS missing） | 随 186；禁止硬挂 188–190；禁止 `M_CHAIN_BOTTLENECK_*`；禁止按号 mapped 技术链 132 | MIXED |
| TEMP_DS06_CITY_TALENT_INDEX | 深圳重点人才指数 | 综合反映深圳重点人才质量、活跃度与贡献度。调用系统=新型高端智库 / 科技人才智慧服务。不是 186 人才维评分，不是 seq 130 对比里的「创新人才」字段 | 智库封装读数；禁止挂 seq 184 | STAT |
| TEMP_DS06_CITY_TREND | 深圳与对标城市趋势 | 深圳与对标城市科技发展指标的历史变化趋势和未来预测。05 seq 186 已列区域趋势分析/趋势预测 → 差集 **mapped 保持**。预测算法未冻 → SZCITY-B04，不另开 A。详设 DS-06 **未给 501** | 随 186 趋势；不伪展开预测公式；禁止因「无 501」改 missing | MIXED |

#### 本页 ④ 不适用（N/A + 依据）

| 项 | 差集 | N/A 依据 |
|----|------|----------|
| 城市选择功能（seq 129） | n/a_ops | 对标范围筛选壳（列表/搜索）；禁止 mapped 182–191；不是 DS-04-CITY 订阅、不是 CARRIER 载体筛选 |
| 发展建议提供（seq 133） | other_system | 报告/文案读面，未点名生成模型；禁止硬挂 seq 185 / 技术链 140/138–139；186 策略建议是附录，不改挂 mapped；DOMAIN seq 128 不进本页 |
| 报告生成与导出（seq 135） | n/a_ops | PDF/Word 导出壳；禁止按号 mapped 技术链 135；不是 GBA seq 104 |

禁止混挂 DS-04-CITY / DS-05 / DS-08。xlsx 行56 载体价值排名 **不进本页**。xlsx 行55 湾区历史趋势 **不进本页**。

### §3.2 `DS-06-CARRIER` · kit（seq 112–117）

对象=**深圳创新载体**（高校 / 研究机构 / 企业 / 工作室），不是城市、不是区域、不是全球载体榜。05 无「创新载体」专叶。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS06_CARRIER_VALUE_RANK | 深圳创新载体创新价值排名 | 按各深圳载体创新成果等数据计算的创新价值名次，供识别高价值载体；详情页与筛选键「创新价值」、对比视图价值列消费同一结果。半成品行56。同构 DS-04-CARRIER-RANK seq 73/74（全球载体指数/多维排名已 missing）→ **also_in**，地域不同，**禁止**把全球 TEMP_DS04_CARRIER_* 或任何 `M_*` 改挂为本页正式 ID | 模型未签；05 无载体指数专叶。上层封装「科技指数计算」≠ mapped 05、≠ DS-08 / Q-TINDEX-01 | MODEL |

**库缺口保持 missing。** 不得因 OPEN present 改 mapped。

#### 本页 ④ 不适用

| 项 | 差集 | N/A 依据 |
|----|------|----------|
| 多层级地理展示（seq 112） | other_system | GIS + ADS 点位；区/街道/产业园/园区→主体钻取；不是构图；禁止 mapped 图谱 API seq 116 |
| 载体详情查看（seq 113） | other_system | ADS 介绍/成果列表；排名数字消费 TEMP_VALUE_RANK，不另开 missing；不抢 DS-04-CARRIER-RANK seq 76 |
| 载体订阅功能（seq 115） | n/a_ops | 订阅 + 推送通道；禁 `M_SVC_REC_*`；禁改挂 DS-04 MONITOR seq 80 / CITY seq 87 |
| 载体筛选与搜索（seq 116） | n/a_ops | 类型/领域/价值/关键词过滤壳；**禁止**因序号相同 mapped 05 seq 116 图谱 API |
| 载体对比分析（seq 117） | n/a_ops | 用户自选并排视图，不是相似载体匹配算法；价值列消费 TEMP_VALUE_RANK；禁 `M_SVC_SZ_COMPARE_METRIC`；xlsx 行62 发展潜力归 CITY |

禁止 `M_SVC_ORG_TECH_SCORE`、企业 seq 141、机构 seq 99/149/151/152、综合 182–191、CITY 城市排名、DS-08 顶替。

### §3.3 `DS-06-INDICATOR` · kit（seq 118–123）

对象=**深圳市创新监测指标体系读面**（metrics catalog + ADS），不是湾区 GBA-CAPACITY 指标计算页，不是 CITY 城际对标。原文未点名趋势预测或对标模型 → A2 六叶 **other_system 保持**。有看板统计数字 → **出卡**，不口头 N/A。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS06_IND_KPI_BOARD | 深圳科技发展指标看板 | 从论文、期刊、专利、专家学者、会议、组织机构、课题、项目、资金、政策、基础设施等维度切换查看的深圳科技发展指标计数/比率；图表（柱/折/饼/雷达）、字面时序、字面多指标/多时段对比、详情口径为同一套数的读面。十一维是过滤切面，**不拆十一条、不发明 M_***。十一维 ≠ 186 四维 ≠ 187 七要素 | 演示：ADS / metrics catalog V1 字段聚合；**不是** 05 综合评价公式，**不是** CITY seq 130 城际对比 | STAT |

#### 本页 ④ 不适用 / 无独立核

| 项 | 差集 | 依据 |
|----|------|------|
| 指标体系展示（seq 118） | other_system | 一/二/三级目录 + 定义/计算方法/数据来源 = catalog 口径树；禁止 mapped 182–191「设计指标体系」；禁止按号 mapped 产业链 seq 118；不复制 GBA-INDICATOR 勾选 n/a_ops |
| 指标数据可视化（seq 120） | other_system | 与 KPI_BOARD 同一读面；「变化趋势」=已落库值的图表呈现，不是预测；禁 mapped 186 / 产业链 120 / 图谱 116 |
| 指标时间趋势分析（seq 121） | other_system | 字面 ADS 时间序列，未点名预测模型；禁止 mapped 186；禁止用 CITY seq 134（含未来预测）顶替 |
| 指标对比分析（seq 122） | other_system | 多指标或多时间段并排，对象≠城市≠载体；禁止 mapped 186/188/191；禁 `M_SVC_SZ_COMPARE_METRIC` |
| 指标详情查看（seq 123） | other_system | ADS 详情 + 口径说明 + 解读文案，未点名生成模型；禁 mapped 182–191 评价报告 |

半成品行 56–63 **均非本五级宿主**，不进本页。禁止发明 `M_SZ_INDICATOR_*` / `M_SZ_PAPER_*` / `M_SZ_PATENT_*`。

### §3.4 `DS-06-DOMAIN` · kit（seq 124–128）

对象=**深圳市各科技领域空间分布**。热力/空间= GIS 聚合，**不对**技术链 seq 133（给定某项技术预测细分领域覆盖率/集中度 ≠ 全市领域热力的范围/中心/扩散）。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS06_DOMAIN_KPI | 深圳科技领域明细指标 | 各科技领域的企业数量、专利数量、研发投入、人才数量（分领域 ADS 明细表）。四字段不拆正式 `M_*`。不是 INDICATOR 十一维，不是 182–185 区域综合评价 | 演示：ADS 分领域计数/金额聚合；禁止改挂 `M_CHAIN_SZ_ENTERPRISE_COUNT` / `M_CHAIN_SZ_PATENT` / `M_CHAIN_SZ_TALENT` | STAT |

#### 本页 ④ 不适用

| 项 | 差集 | N/A 依据 |
|----|------|----------|
| 热力图展示（seq 124） | other_system | GIS + ADS 密度图层；禁止 mapped 133 / 189 / 产业链 120/124；05 无 GIS 热力专叶 ≠ missing |
| 领域筛选功能（seq 125） | n/a_ops | 信息技术/生物医药/新材料/新能源图层开关，四类不拆行；不是 CARRIER 载体筛选、不是 CITY 选城 |
| 空间分布分析（seq 126） | other_system | 分布范围/中心位置/扩散方向 = GIS 空间统计；领域类型由筛选给定，不要求领域识别模型；禁止硬挂 133；禁止 mapped 186（本叶「发展趋势」=空间扩散，不是城市指标预测） |
| 分析与建议（seq 128） | n/a_ops | 领域现状评估与未来建议报告读面，未点名生成模型；禁止硬挂 186/185/188–190；禁止 CITY seq 133；禁止 also_in `M_POLICY_INDUSTRY_FIT` |

禁止发明 `M_SZ_DOMAIN_*` / `M_HEATMAP_*` / `M_SZ_FIELD_*`。禁止 `M_SVC_PT_SZ_FIELD_DIST` 顶替。

---

## §4 ⑤ 开放项（已登记 · 不升 🟢 · 不新建 Q0xx）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| 文件级 OPEN | **本叶闭合**：四页 `metric_open_status: present` | 语义欠账→有指针；非把 missing 改 mapped |
| SZCITY-B01 | 无四件套 / TRACE | 本叶补指针后文件级闭合；不发明 M_* |
| SZCITY-B02 | 排名/对比/竞争力/趋势无正式 metric_id | 语义债；差集 mapped 186 不动 |
| SZCITY-B03 | 招标对比分项（投入/专利/高企/人才）vs 186 四维 | 语义债；不另开 A、不发明分项 M_* |
| SZCITY-B04 | 招标「未来预测」vs 186 趋势预测未冻 | 语义债；差集 mapped；详设无 501，不把无 501 写成 A |
| CAR-B01 | 载体创新价值排名无正式 ID | 语义债；库缺口 CAR-D03 **保持 missing** |
| IND-B01 / IND-B02 | 无 OPEN 叶（本叶闭合文件级）/ 十一维与目录无正式 ID | 语义债；差集 other_system 不动 |
| DOM-B01 / DOM-B02 | 无 OPEN 叶（本叶闭合文件级）/ 领域四字段与热力密度无正式 ID | 语义债；差集 other_system / n/a_ops 不动 |
| Q-TINDEX-01 | 智库指数后台（DS-08） | **本页不改挂** |
| Q010～Q019 / QPOL-* | 展示企业 / 政策口径族 | **本页不改挂、不关闭** |

未关闭任何甲方项。未改 `客户决策清单跟踪表.md`。未新建 `data-gap-catalog`（⑤ = 本表 + A2 `semantic_debt`，**N/A 于新 Q0xx**）。

---

## §5 贴源摘要（data-agent 协作 · 不改 registry）

| 层 | 结论 |
|----|------|
| 调用链 | 前端 `/display` → Java display BFF（GIS 图层 + metrics catalog）→ 只读 ADS；可选 graph/view **不进本四页义务**。Java 不写 NLP / 不直连 nGQL。CITY 对照 186 **不在本页跑专题 Job**。 |
| 准入 / ODS | A1 双表未交 → 本叶 D3 不得伪 `full`。V1 看板字段走 display ADS，不自动等于 05 综合/技术链公式。 |
| 预测 / 501 | 详设 04 DS-06 未给 501。CITY seq 134 跟 186 mapped；预测未冻走 SZCITY-B04。**禁止**借 501 伪覆盖 CARRIER 价值排名或 INDICATOR 字面时序。 |
| 算法库 05 | CITY 对比/排名/竞争力/趋势 mapped 186。CARRIER 价值排名 **无对口叶 → missing 保持**（also_in 全球载体榜，不改挂）。INDICATOR / DOMAIN 不对 182–191 / 133。展示序号 116/118–135 与 05 大量撞号 → **禁止按号 mapped**。 |
| 本叶不做 | 不写任何 `cfg_metric-*-seed.yaml`；正式 `M_INNOV_*_SZ` 只在 §赋号表 / `id-assign/`；禁止发明 `M_SZCITY_*` / `M_CITY_*` / `M_CARRIER_*` / `M_SZ_INDICATOR_*` / `M_SZ_DOMAIN_*`；不改挂 B 轨 / SYNTH / CHAIN / SVC / ENT / DS-04 GLOBAL / DS-05 GBA；不改 A2 catalog 正文；不混写 DS-08/TOPIC/POLICY。 |

metric-registry MCP 本会话未挂载；未整文件读 seed。形近 ID 以 A2 `b_track_lookalikes` / `srs05_do_not_map` 为准，一律不消费。

---

## §6 UI / 评审挂载要求（给 V1 / 迁移叶）

- 凡统计数字：ⓘ MetricSpecCard。seed **无**本页正式 ID → 回指 **本记录 TEMP_ / §赋号表 `M_INNOV_*_SZ`**，**禁止**点开 `M_CHAIN_*` / `M_SVC_*` / `M_SYNTH_*` / `M_ENT_*` / `TEMP_DS04_*` / `M_INNOV_*_GLOBAL` 伪 8 件套
- Wave 0：🧪 MockBadge
- 维名/权重/预测未冻：⚠️「待甲方确认」（文案走 SZCITY/CAR/IND/DOM-B*，不要把 Q-TINDEX-01 写进 `/display` DOM）
- TEMP_ 未入 seed：D1 按 `missing`/`draft` 诚实；红问号或 draft ⓘ，**不显伪 8 件套**
- 关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / `501` / 就绪度字样
- 功能实现 Owner（展示页要哪些指标）= `human:李伟`；STAT → GDF ADS + Java 聚合；MODEL 计算仍归唐绍祖监管 Python

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录 | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-06-深圳创新监测-核对记录.md`（含 §赋号表） |
| 机器卡 | `metrics/request/_work/open-loop/DS-06-METRIC-OPEN-L01.yaml`（demands 已换 `M_*`，保留 temp_id_map） |
| A2 指针补丁（分叶） | `metrics/request/_work/open-loop/DS-06-METRIC-OPEN-L01-a2-patch.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/DS-06-METRIC-OPEN-L01.yaml` |
| 叶级 Q | `metrics/request/_work/id-assign/DS-06-METRIC-OPEN-L01-questions.yaml` |
| 薄 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-06-METRIC-OPEN-L01.md` |
| **未改** | `metrics/registry/` seed / 矩阵；A2 catalog 正文（Round 18）；共享 `LOOP-state.yaml` / `METRIC-OPEN-LOOP-a2-patch.yaml` / `METRIC-SEMANTIC-QUESTIONS.md` / 客户决策清单 |

---

## §8 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _口径草稿已出；赋号草稿 9 条 `M_INNOV_*_SZ`（reuse=0）；四页全部 **kit**；CARRIER 价值排名 **missing 保持**；CITY 186 **mapped 不改挂 SYNTH**；**零**正式 `M_*` 入 seed；⑤ N/A 于新 Q0xx（叶级 Q-MO-DS06 未进客户决策清单）_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）_ | |
| 展示页指标清单（李伟） | — | 本叶不定清单、不改挂 | |
| 甲方既有 Q 项 | — | 不改挂、不升 🟢 | |
