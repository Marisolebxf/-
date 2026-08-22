# METRIC-OPEN-DS-05-湾区创新监测-核对记录

> **任务**：DS-05-METRIC-OPEN-L01（METRIC-OPEN-LOOP Round 8–16 态势叶 · 湾区）  
> **角色**：product-agent（口径草稿）+ algorithm-agent / data-agent（协作核对，本叶不改 seed）  
> **监管人**：`human:淮政玮`  
> **日期**：2026-08-22  
> **上游**：无独立四件套 / PACK-L01；本工作流书面 **SRS 02 + 详设 04 顶 PACK**（给人说明 §8.4 甲）  
> **范围**：展示 catalog `ds_id=DS-05` **全部 4 页**的 ④ 指标语义卡 + ⑤ 开放项。不替甲方拍板；公式 / `algorithm_type` **不签**，标 `pending_cosign: human:唐绍祖`（8/25 前不派唐绍祖开工本 loop）。

**catalog 真源 `page_id`（禁止用短名当机器键）**：

| 短名（派单口语） | catalog `page_id` | 五级 |
|------------------|-------------------|------|
| GBA-ANALYSIS | `DS-05-GBA-ANALYSIS` | 粤港澳大湾区创新能力分析 |
| GBA-INDICATOR | `DS-05-GBA-INDICATOR` | 粤港澳大湾区创新指标数据 |
| GBA-ACHIEVE | `DS-05-GBA-ACHIEVE` | 粤港澳大湾区创新成果综合展示 |
| GBA-CAPACITY | `DS-05-GBA-CAPACITY` | 粤港澳大湾区创新能力 |

SRS：`bid-reference/srs/02-科技信息展示系统/科技发展态势/湾区创新监测.md`（seq 89–111 / excel_row 92–114 / 23 叶）。详设 04：DS-05 = **M · ADS · V1**。无 TRACE / WF 第 6 列。

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ 适用且文档闭合（口径草稿） | 四页均有统计数字 / 指数 / 识别结果 → **出卡**。SRS 与 TRACE **未挂**任何 `metric_id` → 卡面只用 **`TEMP_DS05_GBA_*`**。**禁止**发明正式 `M_GBA_*` 写入 seed；**禁止**改挂 `M_SYNTH_VIT_*` / `M_SYNTH_ELEM_CONTRIB` / B 轨 `M_CHAIN_*` / `M_SVC_*`。 |
| #5 开放项 | ✅ 适用且已登记（本记录） | 页级语义债 GA/GI/GAH/GC-B*。客户决策清单 **无** 湾区口径 `Q0xx` → ⑤ 的 Q 栏 **N/A + 依据**。无 DS-05 `data-gap-catalog` → 文案真源 = A2 `semantic_debt` + 本 §4。本叶不改 `客户决策清单跟踪表.md`、不升 🟢、不改挂 Q-SYNTH-*。 |
| PDR-05 自检 | ⏳ 有条件 | 无 TRACE/WF 第 6 列；本记录 + A2 `pages/DS-05-GBA-*.yaml` 可回指。门 1 完整闭合仍须正式 ID 会签（不发明）+ 公式会签 + 甲方 🟡。 |
| PDR-06 自检 | ⏳ 有条件 | STAT 类可写演示公式；MODEL 公式 `pending_cosign`。招标四因子 vs 05 seq 186 四维显式挂 GC-B03。 |
| 语义 Owner（本工作流） | `human:淮政玮` | 口径 / 8 件套身份项 / 适用性。展示「页面要哪些指标」功能实现主责仍 `human:李伟`（给人说明 §8.4）。 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop 不签公式、不改 seed `algorithm_type` |

**结论**：四页 **④ 均适用（kit）**，**无整页 N/A**。图壳 / 勾选 / 导出 / 阈值告警 / 字面对比 / 详情读面 → **N/A + 依据**（§3.5）。甲方 🟡 不阻断定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。

### §1.1 本叶必须消费本核对记录（各页 kit / N/A）

| 页 `page_id` | 中文 | ④ 页级 | 消费的 ID | 页内 N/A（详见 §3.5） |
|--------------|------|---------|-----------|------------------------|
| `DS-05-GBA-ANALYSIS` | 创新能力分析 | **kit** | `TEMP_DS05_GBA_FACTOR_STAT` + 四象限 `TEMP_DS05_GBA_SWOT_*` | SWOT 图壳；报告 PDF/Word 导出 |
| `DS-05-GBA-INDICATOR` | 创新指标数据 | **kit** | 目录六统计 `TEMP_DS05_GBA_OUTPUT_VALUE` 等 | GIS 落图壳；勾选管理；来源/计算说明；字面对比；导出 |
| `DS-05-GBA-ACHIEVE` | 创新成果综合展示 | **kit** | `TEMP_DS05_GBA_HOTSPOT`（密度 + 主要类型） | 落点 GIS；飞线/高亮壳；分类筛选；成果详情读面 |
| `DS-05-GBA-CAPACITY` | 创新能力 | **kit** | `TEMP_DS05_GBA_CAPACITY_INDEX` + 四子 + 贡献度 | 仪表盘读面（同核）；阈值告警 |

**禁止**：把本四页挂专题 `SYNTH-MOD-VITALITY-METRIC-OPEN`；用 DS-04-CITY / DS-06 深圳监测 / DS-08 指数页顶替；按展示序号 mapped 05 seq 95/96/97/104/105。

### §1.2 23 招标叶子 × 差集（A2 已裁 · 本叶不改判定）

| 五级页 | seq | 叶子 | 差集 | ④ |
|--------|-----|------|------|----|
| ACHIEVE | 89 | 地理位置落点展示 | other_system | N/A（无独立核） |
| ACHIEVE | 90 | 多样化可视化效果 | n/a_ops | N/A |
| ACHIEVE | 91 | 创新成果分类筛选 | other_system | N/A |
| ACHIEVE | 92 | 创新热点区域识别 | **missing** | **kit** |
| ACHIEVE | 93 | 创新成果详情查看 | other_system | N/A |
| CAPACITY | 94 | 创新能力指标计算 | mapped（05 seq 186） | **kit** |
| CAPACITY | 95 | 指标数值展示 | other_system | 同核读面，不另造 ID |
| CAPACITY | 96 | 指标构成分析 | mapped（186） | **kit** |
| CAPACITY | 97 | 指标预警功能 | n/a_ops | N/A |
| ANALYSIS | 98 | SWOT分析展示 | n/a_ops | N/A（图壳） |
| ANALYSIS | 99 | 创新能力因素统计 | other_system | **kit** |
| ANALYSIS | 100–103 | 优/短板/机会/威胁因素分析 | **missing** ×4 | **kit** |
| ANALYSIS | 104 | 分析报告生成 | n/a_ops | N/A |
| INDICATOR | 105 | GIS地图指标展示 | other_system | N/A（落图壳；数字走目录 TEMP_） |
| INDICATOR | 106 | 指标体系管理 | n/a_ops | 勾选壳 N/A；目录成员 **kit** |
| INDICATOR | 107 | 指标数据详情查看 | other_system | 同比/趋势 = 目录 TEMP_ 的 STAT 面，不另造 ID |
| INDICATOR | 108 | 数据来源说明 | other_system | N/A（D9 说明读面） |
| INDICATOR | 109 | 数据计算方式说明 | n/a_ops | N/A |
| INDICATOR | 110 | 指标对比分析 | n/a_ops | N/A（字面并排） |
| INDICATOR | 111 | 指标数据导出 | n/a_ops | N/A |

库缺口 **保持 missing**（ANALYSIS 四象限 + ACHIEVE 热点 = A 类 5）。不得因本 OPEN 存在改成 mapped。

### §1.3 TRACE / A2 语义层指针（Round 18 才回写 catalog 正文）

本叶 **不改** `metrics/request/展示系统/A2-GAP-page-catalog.yaml` 与 pages yaml 正文，**不改** 共享 `_work/METRIC-OPEN-LOOP-a2-patch.yaml`。指针写入叶级 `metrics/request/_work/open-loop/DS-05-METRIC-OPEN-L01-a2-patch.yaml`，由 coordinator 合流。

| 层 | 路径 | 本叶要求的指针 |
|----|------|----------------|
| 核对记录 | **本文件** | DS-05 四页唯一 OPEN 真源 |
| A2 页 yaml | `metrics/request/展示系统/pages/DS-05-GBA-*.yaml` | 应收口：`metric_open_status: present`；`metric_open_path` = 本文件；`metric_open_task: DS-05-METRIC-OPEN-L01`。**库缺口 `missing` 不动**。仍 **禁止** `M_GBA_*` / `M_SYNTH_VIT_*`。 |
| A2 catalog | `ds_id=DS-05` 四行 | 删「无 METRIC-OPEN → 只记语义欠账」中已被本叶覆盖的句（GA/GI/GAH/GC-B01 文件级闭合） |
| TRACE / WF | **无** DS-05 四件套 | `trace_metrics` / `wireframe_metric_ids` 保持空；不从 02 叙述发明 `M_*` |
| PACK | 无独立 `DS-05-PACK-L01` | SRS 02 + 详设 04 顶 PACK；FDS **不顶** OPEN |

口径会签：`owner_semantic = human:淮政玮`；公式 / `algorithm_type` 共签仍 `human:唐绍祖`。Q-SYNTH-01 / V-01 / V-02 **不改挂**本页。

---

## §2 模块消费矩阵（TEMP_ 草稿 · 禁止正式 M_*）

> 差集列维持 A2 已写判定。本表只闭合语义层。`algorithm_type` 列为 **草稿建议**，未会签。  
> **`TEMP_*` ≠ 正式 `M_*`**：只存在于本核对记录与机器卡；**禁止**写入 `metrics/registry/` seed。

| temp_id | 主落点 | 适用 | 建议 type（未签） | pending |
|---------|--------|------|-------------------|---------|
| TEMP_DS05_GBA_FACTOR_STAT | ANALYSIS seq 99：资源/机构/机制/环境分布 | ✅ kit | STAT | ≠ CAPACITY 四子指数；xlsx 41–44/48 不进本页 |
| TEMP_DS05_GBA_SWOT_STRENGTH | ANALYSIS seq 100：优势因素影响程度 | ✅ kit | MODEL | 库 missing；禁硬挂 182–191 / `M_CHAIN_SZ_ADVANTAGE_*` |
| TEMP_DS05_GBA_SWOT_WEAKNESS | ANALYSIS seq 101：短板因素 | ✅ kit | MODEL | 禁 `M_CHAIN_BOTTLENECK_*` / `M_SVC_CHAIN_BOTTLENECK` |
| TEMP_DS05_GBA_SWOT_OPPORTUNITY | ANALYSIS seq 102：机会因素 | ✅ kit | MODEL | 05 无 Opportunities 象限 |
| TEMP_DS05_GBA_SWOT_THREAT | ANALYSIS seq 103：威胁因素 | ✅ kit | MODEL | 禁 `M_CHAIN_TECH_BARRIER_*` |
| TEMP_DS05_GBA_OUTPUT_VALUE | INDICATOR 目录：创新产值 | ✅ kit | STAT | xlsx 49；禁 mapped 05 |
| TEMP_DS05_GBA_INNOV_RATIO | INDICATOR 目录：创新比例 | ✅ kit | STAT | xlsx 50；分子分母未冻 → GI-B02 |
| TEMP_DS05_GBA_INVEST | INDICATOR 目录：创新投入 | ✅ kit | STAT | xlsx 51 |
| TEMP_DS05_GBA_TECH_CONTRACT | INDICATOR 目录：创新技术合同交易额 | ✅ kit | STAT | xlsx 52 |
| TEMP_DS05_GBA_PATENT_PAPER | INDICATOR 目录：专利及论文数量 | ✅ kit | STAT | 半成品无行；禁 `M_CHAIN_PATENT_COUNT` / `M_CHAIN_REG_PAPERS` |
| TEMP_DS05_GBA_PATENT_GRANT | INDICATOR 目录：专利授权量 | ✅ kit | STAT | xlsx 53；禁 `M_CHAIN_REG_PATENT` / `M_CHAIN_SZ_PATENT` |
| TEMP_DS05_GBA_HOTSPOT | ACHIEVE seq 92：热点区域密度 + 主要类型 | ✅ kit | MODEL | 库 missing；禁硬挂 seq 134 / 182–191 |
| TEMP_DS05_GBA_CAPACITY_INDEX | CAPACITY seq 94/xlsx 45：湾区创新能力总指标 | ✅ kit | MODEL | 对上 186 **读面**；禁改挂 `M_SYNTH_VIT_INDEX`；对象=湾区≠ CITY |
| TEMP_DS05_GBA_RES_INDEX | CAPACITY 创新资源指数 | ✅ kit | MODEL | 同核 186；禁 mapped 190 |
| TEMP_DS05_GBA_ORG_INDEX | CAPACITY 创新机构指数 | ✅ kit | MODEL | 同核 186 |
| TEMP_DS05_GBA_MECH_INDEX | CAPACITY 创新机制指数 | ✅ kit | MODEL | 同核 186 |
| TEMP_DS05_GBA_ENV_INDEX | CAPACITY 创新环境指数 | ✅ kit | MODEL | 同核 186 |
| TEMP_DS05_GBA_SUBINDEX_CONTRIB | CAPACITY 子指标贡献度 | ✅ kit | MODEL | 186 权重分布；禁 `M_SYNTH_ELEM_CONTRIB` / `M_SYNTH_VIT_WEIGHT` |

**18/18 TEMP_ 语义层 present。** 不得因「口径未冻 / D1 missing / 无正式 M_*」把上表改成差集 `missing`（SWOT / 热点的 **库** missing 仍保留在 A2 demands）。不得把上表改写成 `M_GBA_*` 或 `M_SYNTH_VIT_*`。

正式身份见下方 **§赋号表**（`M_INNOV_GBA_*` 草稿；未入 seed；类型未签）。

---

## §赋号表（TEMP → 正式 `M_*` · 建议类型未签）

> **日期**：2026-08-22 · product-agent · 监管 `human:淮政玮`  
> ELEMENT=`INNOV`。18/18 新建，**reuse=0**。`algorithm_type_suggested` 一律 `suggested_unsigned`，不替唐绍祖签。  
> **未写** seed / 展示 catalog / 共享 QUESTIONS。SWOT 四象限 + 热点 **库 missing 保持**。CAPACITY 对 seq 186 **mapped 读面**，**禁止改挂** `M_SYNTH_VIT_*`（口径：湾区四因子 ≠ 城市/专题四维）。  
> 歧义 `Q-MO-DS05-nn`（🟡），叶级 `id-assign/DS-05-METRIC-OPEN-L01-questions.yaml`。

| temp_id | metric_id | reuse | 建议 type（未签） | Q |
|---------|-----------|-------|-------------------|---|
| TEMP_DS05_GBA_FACTOR_STAT | M_INNOV_GBA_FACTOR_STAT | — | STAT | — |
| TEMP_DS05_GBA_SWOT_STRENGTH | M_INNOV_GBA_SWOT_STRENGTH | — | MODEL | —（库 missing 保持） |
| TEMP_DS05_GBA_SWOT_WEAKNESS | M_INNOV_GBA_SWOT_WEAKNESS | — | MODEL | —（库 missing 保持） |
| TEMP_DS05_GBA_SWOT_OPPORTUNITY | M_INNOV_GBA_SWOT_OPPORTUNITY | — | MODEL | —（库 missing 保持） |
| TEMP_DS05_GBA_SWOT_THREAT | M_INNOV_GBA_SWOT_THREAT | — | MODEL | —（库 missing 保持） |
| TEMP_DS05_GBA_OUTPUT_VALUE | M_INNOV_GBA_OUTPUT_VALUE | — | STAT | Q-MO-DS05-04 |
| TEMP_DS05_GBA_INNOV_RATIO | M_INNOV_GBA_INNOV_RATIO | — | STAT | Q-MO-DS05-01 |
| TEMP_DS05_GBA_INVEST | M_INNOV_GBA_INVEST | — | STAT | Q-MO-DS05-05 |
| TEMP_DS05_GBA_TECH_CONTRACT | M_INNOV_GBA_TECH_CONTRACT | — | STAT | — |
| TEMP_DS05_GBA_PATENT_PAPER | M_INNOV_GBA_PATENT_PAPER | — | STAT | Q-MO-DS05-03 |
| TEMP_DS05_GBA_PATENT_GRANT | M_INNOV_GBA_PATENT_GRANT | — | STAT | — |
| TEMP_DS05_GBA_HOTSPOT | M_INNOV_GBA_HOTSPOT | — | MODEL | —（库 missing 保持） |
| TEMP_DS05_GBA_CAPACITY_INDEX | M_INNOV_GBA_CAPACITY_INDEX | 不 reuse `M_SYNTH_VIT_INDEX` | MODEL | Q-MO-DS05-02 |
| TEMP_DS05_GBA_RES_INDEX | M_INNOV_GBA_RES_INDEX | 不 reuse `M_SYNTH_VIT_DIM_SCORE` | MODEL | Q-MO-DS05-02 |
| TEMP_DS05_GBA_ORG_INDEX | M_INNOV_GBA_ORG_INDEX | 不 reuse `M_SYNTH_VIT_DIM_SCORE` | MODEL | Q-MO-DS05-02 |
| TEMP_DS05_GBA_MECH_INDEX | M_INNOV_GBA_MECH_INDEX | 不 reuse `M_SYNTH_VIT_*` | MODEL | Q-MO-DS05-02 |
| TEMP_DS05_GBA_ENV_INDEX | M_INNOV_GBA_ENV_INDEX | 不 reuse `M_SYNTH_VIT_*` | MODEL | Q-MO-DS05-02 |
| TEMP_DS05_GBA_SUBINDEX_CONTRIB | M_INNOV_GBA_SUBINDEX_CONTRIB | 不 reuse `M_SYNTH_VIT_WEIGHT` / `M_SYNTH_ELEM_CONTRIB` | MODEL | Q-MO-DS05-02 |

**计数**：赋号 18 · 复用 0 · Q 5（Q-MO-DS05-01…05）· 类型 STAT 7 / MODEL 11。

近义不复用（registry 检索）：`M_ENT_INNOVATION_INDEX`（企业 0–100）· `M_ENT_PATENT_GRANT_COUNT`（企业第一专利权人）· `M_CHAIN_HOTSPOT_*`（产业链环节）· `M_CHAIN_PATENT_COUNT`（产业链关联专利）· `M_SYNTH_VIT_*`（四维活力）。

---

## §3 ④ 指标语义卡（按页 · 不写 seed）

身份项由淮政玮本工作流确认适用。公式 / 权重 / `algorithm_type` 一律 `pending_cosign: human:唐绍祖`。源表以详设「V1 读 ADS」+ A1 双表未交为准，**不**把项目 DWD 反推成 ODS `full`。

8 件套草稿字段（TEMP_ 共同）：metric_id=下表 temp_id；源系统=科技信息展示系统·湾区创新监测；更新频率=未定；version=`draft-open-ds05`；源表=ADS 湾区（A1 表2 未交 → 本叶不填伪 full）。

### §3.1 `DS-05-GBA-ANALYSIS` · kit（seq 98–104）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS05_GBA_FACTOR_STAT | 湾区创新能力因素统计 | 选定湾区范围下，创新资源 / 机构 / 机制 / 环境等促成因素的数量、结构与分布（seq 99）。**不是**四子指数与贡献度（归 CAPACITY） | 演示 `COUNT/SUM GROUP BY factor_type, region` | STAT |
| TEMP_DS05_GBA_SWOT_STRENGTH | 湾区创新能力优势因素 | 识别 Strengths 并给出表现与影响程度（seq 100） | 模型未签；禁止把 seq 186/188 优劣清单当 SWOT | MODEL |
| TEMP_DS05_GBA_SWOT_WEAKNESS | 湾区创新能力短板因素 | 识别 Weaknesses，含表现与改进建议（seq 101） | 模型未签；改进建议不改挂 05 seq 140 | MODEL |
| TEMP_DS05_GBA_SWOT_OPPORTUNITY | 湾区创新能力机会因素 | 识别 Opportunities（政策/市场/技术突破/国际合作等）及利用建议（seq 102） | 模型未签 | MODEL |
| TEMP_DS05_GBA_SWOT_THREAT | 湾区创新能力威胁因素 | 识别 Threats（竞争/壁垒/政策变化/环境风险等）及应对策略（seq 103） | 模型未签 | MODEL |

算法定义卡（草稿）：SWOT 四象限识别 **无** 05 专叶 → 库 missing；本卡只定「要识别结果」。禁止 mapped 05 seq 104（技术实体识别构建，序号碰巧相同）。

### §3.2 `DS-05-GBA-INDICATOR` · kit（seq 105–111）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS05_GBA_OUTPUT_VALUE | 创新产值 | 区域创新活动经济产出规模（seq 106 目录；xlsx 49） | 演示 `SUM(output_value)`；口径未冻 | STAT |
| TEMP_DS05_GBA_INNOV_RATIO | 创新比例 | 创新相关产出或投入在总体中的占比（xlsx 50） | 演示 `创新相关 / 总体`；分子分母未冻 → GI-B02 | STAT |
| TEMP_DS05_GBA_INVEST | 创新投入 | 资金/资源/研发投入强度（xlsx 51） | 演示 `SUM(invest)` | STAT |
| TEMP_DS05_GBA_TECH_CONTRACT | 创新技术合同交易额 | 技术合同成交金额（xlsx 52） | 演示 `SUM(contract_amt)` | STAT |
| TEMP_DS05_GBA_PATENT_PAPER | 专利及论文数量 | seq 106 原文目录成员；与授权量分列；半成品无行 | 演示 `COUNT(patent)+COUNT(paper)`；分列规则未冻 | STAT |
| TEMP_DS05_GBA_PATENT_GRANT | 专利授权量 | 期内授权专利件数（xlsx 53） | 演示 `COUNT(granted_patent)` | STAT |

同比环比 / 历史趋势（seq 107 / xlsx 54–55）= 上表各 TEMP_ 的时间差与序列面，**不另造 TEMP_**。禁止 mapped 186 趋势预测。GIS 落图只消费上表数字，不另造地图核。

### §3.3 `DS-05-GBA-ACHIEVE` · kit（seq 89–93）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS05_GBA_HOTSPOT | 湾区创新热点区域 | 自动识别并标注大湾区内创新热点区域；读面给出创新密度与主要创新类型（seq 92） | 空间聚类/密度模型未签。**不是**专题技术前沿领域（05 seq 134），**不是**区域综合评价指数（182–191） | MODEL |

密度与主要类型共核，不另造 CNT ID。详情里的「创新价值」本页只读 ADS 字段，禁止 also_in DS-04-ACHIEVE-OVERVIEW 全球创新价值 missing。

### §3.4 `DS-05-GBA-CAPACITY` · kit（seq 94–97）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS05_GBA_CAPACITY_INDEX | 粤港澳大湾区创新能力指标 | 对湾区创新资源/机构/机制/环境综合分析得到的总指数（seq 94；xlsx 45）。实现路径对照 05 seq 186 **展示读面**，不跑 SYNTH-VITALITY Job | 演示加权综合；四因子 vs 186 四维（科技/产业/人才/政策）→ GC-B03 | MODEL |
| TEMP_DS05_GBA_RES_INDEX | 创新资源指数 | 总指数子指标（xlsx 44 / seq 96） | 随 186 单维评分；标签「资源」≠ 186「科技」维，见 GC-B03 | MODEL |
| TEMP_DS05_GBA_ORG_INDEX | 创新机构指数 | 子指标（xlsx 42） | 同上 | MODEL |
| TEMP_DS05_GBA_MECH_INDEX | 创新机制指数 | 子指标（xlsx 41） | 同上 | MODEL |
| TEMP_DS05_GBA_ENV_INDEX | 创新环境指数 | 子指标（xlsx 43） | 同上 | MODEL |
| TEMP_DS05_GBA_SUBINDEX_CONTRIB | 子指标贡献度 | 四子对总指数的贡献（xlsx 48） | 随 186 权重分布；禁止要素贡献路径 `M_SYNTH_ELEM_CONTRIB` | MODEL |

算法定义卡（草稿）：模型叶 = `综合/综合分析.md#区域创新活力综合分析模型`（seq 186）。与 SYNTH-VITALITY / DS-04-CITY **同一 05 叶、不同对象/不同 OPEN**。禁止按号 mapped 05 seq 95/96/97。禁止 `M_CHAIN_REGION_INDEX` / `M_CHAIN_COMPETITIVENESS_INDEX`。半成品行 45 建议取值误写「城市」→ 本页对象仍是湾区，不重列 CITY 行。

seq 95 仪表盘 = 总指标读面，不另造 TEMP_。

### §3.5 ④ 不适用（N/A + 依据）

整页 N/A：**无**（四页均有统计或识别核）。

| 宿主 | 项 | 差集判定 | N/A 依据 |
|------|----|----------|----------|
| ANALYSIS seq 98 | SWOT 四象限图壳 | n/a_ops | 展示框架，不是识别模型；识别走四 TEMP_SWOT_* |
| ANALYSIS seq 104 | 分析报告生成 / 导出 PDF·Word | n/a_ops | 模板拼装 + 导出壳。禁止 mapped 05 seq 104 |
| INDICATOR seq 105 | GIS 地图指标落图 | other_system | GIS+ADS 坐标；数字走目录 TEMP_。禁止 mapped 05 seq 105 / seq 116 |
| INDICATOR seq 106 壳 | 指标体系勾选开关 | n/a_ops | 目录配置；成员统计见 §3.2 |
| INDICATOR seq 108–109 | 来源说明 / 计算方式说明 | other_system / n/a_ops | D9 说明读面与 MetricSpecCard 文案，不是当场跑模型。指数计算归 CAPACITY |
| INDICATOR seq 110 | 多区域/多指标字面对比 | n/a_ops | 未点名对标模型。禁止 mapped 186/188/191；禁止 `M_SVC_SZ_COMPARE_METRIC`；禁止复制 DS-04-CITY |
| INDICATOR seq 111 | 指标数据导出 | n/a_ops | 导出壳 |
| ACHIEVE seq 89 | 成果/机构/企业坐标落点 | other_system | GIS+ADS。禁止 mapped seq 116 |
| ACHIEVE seq 90 | 高亮/闪烁/飞线与用户偏好 | n/a_ops | 前端效果。热点识别见 HOTSPOT |
| ACHIEVE seq 91 | 类型/领域/时间筛选 | other_system | ADS 过滤。禁止 mapped 185；禁止把全球 OVERVIEW 分类算进本页 |
| ACHIEVE seq 93 | 成果详情（描述/价值/时间/机构） | other_system | 单条读面。创新价值只读已落库字段 |
| CAPACITY seq 95 | 数值/仪表盘/进度条 | other_system | 同核 INDEX 读面（xlsx 47） |
| CAPACITY seq 97 | 阈值配置 + 越限告警 | n/a_ops | 不是预警模型；详设 501 只在 DS-09。禁止 mapped 186 趋势预测；禁止按号 mapped 05 seq 97 |
| 本叶范围外 | DS-04-CITY / DS-06 / DS-08 / SYNTH-* / DS-13～16 | other_system | 各有 OPEN 叶；禁止混挂 |
| 无独立核 | 同比环比、历史趋势、目录勾选态、地图缩放平移 | 见上 | 不另造 TEMP_ / 不发明 `M_*` |

---

## §4 ⑤ 开放项（已登记 · 不升 🟢）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| GA-B01 / GI-B01 / GAH-B01 / GC-B01 | **本叶闭合文件级**：核对记录 present。A2 catalog 正文 Round 18 才改指针 | 语义欠账→有指针；非 A 类 missing |
| GA-B02 | SWOT 四象限无正式 metric_id | 已赋 `M_INNOV_GBA_SWOT_*` 草稿（未入 seed）；**库 missing 保持** |
| GA-B03 | PDR-05/06 有条件；公式未签 | ⏳ |
| GI-B02 | 目录统计数字无正式 ID；创新比例分子分母未冻 | 已赋目录六号草稿；分子分母 → Q-MO-DS05-01（🟡）；覆盖判定仍 other_system |
| GAH-B02 | 热点区域识别无正式 metric_id | 已赋 `M_INNOV_GBA_HOTSPOT` 草稿（未入 seed）；**库 missing 保持** |
| GC-B02 | 总指数/四子/贡献度无正式 metric_id | 已赋 `M_INNOV_GBA_*_INDEX` / `SUBINDEX_CONTRIB` 草稿；**不 reuse** `M_SYNTH_VIT_*`；覆盖判定仍 mapped 186 |
| GC-B03 | 招标四因子 vs 186 四维；xlsx 45 误写城市 | 内部默认四因子身份 → Q-MO-DS05-02（🟡）；不另开 A |
| Q0xx（湾区口径） | **N/A + 依据**（客户清单不新编） | 叶级 `Q-MO-DS05-01…05` 只写 `id-assign/*-questions.yaml`，coordinator 再合流。禁止撞 Q010～Q019 / Q-SYNTH-* |
| data-gap-catalog | **N/A + 依据** | 无 `DS-05-data-gap-catalog.yaml`。Pending 文案真源 = A2 缺口说明 + 本 §4。本叶不新建 catalog（不挡 UX/V1） |
| Q-SYNTH-01 / V-01 / V-02 | **不改挂** | 专题活力 OPEN 所有；本页只对照 186 读面 |
| Q030 | **不改挂** | 展示页用户级别，不是湾区指标口径 |

未关闭任何甲方项。未改 `客户决策清单跟踪表.md`。

---

## §5 贴源摘要（data-agent 协作 · 不改 registry）

| 层 | 结论 |
|----|------|
| 调用链 | 前端 → Java REST → 只读 ADS。详设 V1 不跑专题综合 Job、不跑技术链热点 Job。Java 不写 NLP / 不直连 nGQL。 |
| 准入 / ODS | A1 双表未交 → 本叶 D3 不得伪 `full`。半成品「科技指数计算」= 展示侧上层结果，不自动 mapped 05。 |
| 算法库 05 | CAPACITY 对上 seq 186 → mapped（读面）。SWOT 四象限与地理热点 **无专叶** → missing 保持。INDICATOR / 落点 / 筛选 / 导出不对上 182–191。 |
| 序号碰撞 | 展示 seq 104 ≠ 05 技术实体识别；展示 seq 105 ≠ 05 关系抽取；展示 seq 95/96/97 ≠ 产业链/技术/企业基础指标。禁止按号 mapped。 |
| 本叶不做 | 不写 `cfg_metric-*-seed.yaml`；不改挂 `M_SYNTH_VIT_*`；不新建 `data-gap-catalog`；不改 A2 catalog 正文。 |

---

## §6 UI / 评审挂载要求（给 V1 / 迁移叶）

- 凡统计数字：ⓘ MetricSpecCard。seed **仍无**本页 ID → 回指 **本记录 §赋号表 `M_INNOV_GBA_*` 草稿**，**禁止**点开 `M_SYNTH_VIT_*` / `M_CHAIN_*` 伪 8 件套
- Wave 0：🧪 MockBadge
- 四因子/比例口径未冻：⚠️「待甲方确认」（文案走 GC-B03 / GI-B02，不要写 Q-SYNTH 字样到展示 DOM）
- TEMP_ 未入 seed：D1 按 `missing`/`draft` 诚实；红问号或 draft ⓘ，**不显伪 8 件套**
- 关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / 就绪度字样
- 功能实现 Owner（展示「要哪些指标」）= `human:李伟`；STAT → GDF ADS + Java 聚合；MODEL 计算仍归唐绍祖监管 Python（给人说明 §2.3）。本工作流语义 Owner = 淮政玮

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录（含 §赋号表） | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-05-湾区创新监测-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/DS-05-METRIC-OPEN-L01.yaml` |
| 叶级赋号卡 | `metrics/request/_work/id-assign/DS-05-METRIC-OPEN-L01.yaml` |
| 叶级 Questions | `metrics/request/_work/id-assign/DS-05-METRIC-OPEN-L01-questions.yaml` |
| A2 指针补丁（叶级） | `metrics/request/_work/open-loop/DS-05-METRIC-OPEN-L01-a2-patch.yaml` |
| 薄 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-05-METRIC-OPEN-L01.md` |
| **未改** | `metrics/registry/` seed / 矩阵；A2 catalog / pages 正文；共享 `METRIC-OPEN-LOOP-a2-patch.yaml`；`LOOP-state.yaml`；`METRIC-SEMANTIC-QUESTIONS.md` |

---

## §8 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _口径草稿 + **赋号草稿**（18×`M_INNOV_GBA_*`，类型未签）；四页 kit；**零 reuse** `M_SYNTH_VIT_*` / `M_GBA_*`；SWOT/热点库 missing 保持_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）_ | |
| 甲方湾区口径 Q | — | 清单无 DS-05 Q0xx；保持 N/A；不改挂 Q-SYNTH-* | |
