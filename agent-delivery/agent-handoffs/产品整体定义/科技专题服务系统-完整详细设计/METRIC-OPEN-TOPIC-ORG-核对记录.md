# METRIC-OPEN-TOPIC-ORG-核对记录

> **任务**：TOPIC-ORG-METRIC-OPEN-L01（METRIC-OPEN-LOOP Round 4）  
> **角色**：product-agent（口径草稿）+ algorithm-agent / data-agent（协作核对，本叶不改 seed）  
> **监管人**：`human:淮政玮`  
> **日期**：2026-08-22  
> **上游**：无独立四件套 / PACK-L01；本工作流书面 **SRS 04 + 05.4 顶 PACK**（给人说明 §8.4 甲）  
> **范围**：专题科研机构分析 **一整包** `page_id=TOPIC-ORG-05` 的 ④ 指标语义卡 + ⑤ 开放项。覆盖 05.4 **十招标叶子**里进算法差集的那些。不替甲方拍板；公式 / `algorithm_type` **不签**，标 `pending_cosign: human:唐绍祖`（8/25 前不派唐绍祖开工本 loop）。

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ 适用且文档闭合（口径草稿） | 十招标叶子均有覆盖 / 趋势 / 网络 / 指数 / 名单规模 → **出卡**。05.4 与 SRS 04 **未挂**任何 `metric_id` → 卡面只用 **`TEMP_TOPIC_ORG_*`**。**禁止**消费产业服务链 `M_SVC_ORG_*` / `M_SVC_REC_*` / SVCCHAIN OPEN；**禁止**消费产业链 `M_CHAIN_INSTITUTION_*` / `M_CHAIN_REG_RESEARCH_ORG` / `M_CHAIN_ACADEMIC_POWER` 等形近 ID；**禁止**发明正式 `M_ORG_*` 写入 seed。实现类倾向 `third_party` → 公式栏只写 **「第三方不展开」**，禁止编论文×权重+专利×权重伪公式。 |
| #5 开放项 | ✅ 适用且已登记（本记录） | 页级语义债 TORG-B01…B10。本叶不改 `客户决策清单跟踪表.md`、不升 🟢、不新建 `Q-TOPIC-ORG-*`。 |
| PDR-05 自检 | ⏳ 有条件 | 无 TRACE/WF 第 6 列；本记录 + A2 `pages/TOPIC-ORG-05.yaml` 可回指。门 1 完整闭合仍须正式 ID 会签（不发明）+ 公式会签 + 甲方 🟡。 |
| PDR-06 自检 | ⏳ 有条件 | 口径方向可写；**公式一律不展开**。维名 04≠05≠catalog R-* 显式挂 TORG-B02…B10。 |
| 语义 Owner（本工作流） | `human:淮政玮` | 口径 / 8 件套身份项 / 适用性 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop 不签公式、不改 seed `algorithm_type` |

**结论**：本页 **④ 适用（kit）**，**非整页 N/A**。历程 CMS、筛选/配置壳、门户 R-29~32、运营 R-33/34、图谱基建无独立统计核、产业服务「服务机构」→ **N/A + 依据**（§3.12）。甲方 🟡 不阻断定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。

### §1.1 本页必须消费本核对记录

| 页 `page_id` | 中文 | ④ | 消费的 ID | 禁止 |
|--------------|------|----|-----------|------|
| `TOPIC-ORG-05` | 专题科研机构分析（整包） | **kit** | 赋号草稿 `M_ORG_*`（§8；TEMP 仅对照） | 挂 `METRIC-OPEN-SVCCHAIN-核对记录`；消费 `M_SVC_ORG_*` / `M_SVC_REC_*` / `M_SVC_GRAPH_*`；消费 `M_CHAIN_INSTITUTION_*` 形近 ID；把草稿写入 seed；把本页 A=0 改成 missing；把 `third_party` 改判 missing |

**产业服务链（A2 W2 / Round 1）**：本叶 **不消费**。服务机构 ≠ 科研机构（05.4 边界；TOPIC-ORG-05 `scope_exclusions.svcchain_service_orgs`）。`SVCCHAIN-ORG-ANALYSIS` / `ECOSYSTEM` / `RECOMMEND` / `PORTAL` 的 OPEN 与全部 `M_SVC_ORG_*` **不是**本页语义层。

**产业链机构形近 ID**：`M_CHAIN_INSTITUTION_COUNT` / `M_CHAIN_SZ_INSTITUTION_COUNT` / `M_CHAIN_REG_RESEARCH_ORG` / `M_CHAIN_ACADEMIC_POWER` / `M_CHAIN_REG_PAPERS` / `M_CHAIN_REG_PATENT` 口径是链/区域/四力，**禁止**当本页 metric。

### §1.2 05.4 十招标叶子 × 差集

| 招标叶子 | 05.4 算法 | 标签 | 差集 | ④ |
|----------|-----------|------|------|----|
| 产业 | `.1`（1）基础指标 | M | mapped（TORG-D02） | kit |
| 技术领域布局 | `.6.1` seq 149 | M/G1 | mapped（TORG-D03） | kit |
| 新增动态 | `.1`（4） | M | mapped（TORG-D05 / D06 关注度同叶） | kit |
| 深圳现状 | `.1` + `.6.1` | M | mapped（TORG-D08） | kit |
| 合作关系链 | `.6.5` seq 153 | **G1 A 面** | mapped（TORG-D10） | kit |
| 技术力对比 | `.6` 评价（**【算法补】**） | M | **third_party**（TORG-D12；不算我方库公式缺失） | kit |
| 引入推荐 | `.6.6` seq 154 | **G3 Job** | mapped（TORG-D13） | kit |
| 培育（扶持）推荐 | `.6.7` seq 155 | **G3 Job** | mapped（TORG-D14） | kit |
| 深圳优势 | `.6.3` seq 151 | G3 | mapped（TORG-D15） | kit |
| 痛难点 | `.6.4` seq 152 | G3 | mapped（TORG-D16） | kit |

历程 **不是**十招标叶子：`.6.2` = **CMS** → `n/a_ops`（TORG-D17；05 seq 150 叶存在禁止 missing）。

技术力对比：**05 十叶无专叶**，差集保持 `third_party`，④ 仍出卡（有得分/雷达/排名语义）。**禁止**因此打 missing，**禁止** mapped 到服务机构技术力。

### §1.3 TRACE / A2 语义层指针（Round 17 才回写 catalog 正文）

本叶 **不改** `metrics/request/专题系统/A2-GAP-page-catalog.yaml` 与 pages yaml 正文。指针写入 `_work/open-loop/TOPIC-ORG-METRIC-OPEN-L01-a2-patch.yaml`（**不改**共享 `METRIC-OPEN-LOOP-a2-patch.yaml` / `LOOP-state.yaml`，由 coordinator 合流）。

| 层 | 路径 | 本叶要求的指针 |
|----|------|----------------|
| 核对记录 | **本文件** | `TOPIC-ORG-05` 唯一 OPEN 真源 |
| A2 页 yaml | `metrics/request/专题系统/pages/TOPIC-ORG-05.yaml` | 应收口：`metric_open_status: present`；`metric_open_path` = 本文件；`metric_open_task: TOPIC-ORG-METRIC-OPEN-L01`。**库缺口 `missing` 不动**（本页 A 类本就为空）。`metric_id` 保持 null，**禁止**把 TEMP_ 回写进 pages。仍 **禁止** `M_SVC_ORG_*` / `M_ORG_*`。 |
| A2 catalog | `A2-GAP-page-catalog.yaml` 的 `TOPIC-ORG-05` | 删「无 METRIC-OPEN → 只记语义欠账」中已被本叶覆盖的句（TORG-B01 文件级闭合） |
| TRACE / WF | **无**专题科研机构四件套 | `trace_metrics` / `wireframe_metric_ids` 保持空；不从 04 叙述发明 `M_*` |
| PACK | 无独立 `TOPIC-ORG-PACK-L01` | SRS 04 + `05.4-科研机构.md` 顶 PACK |

口径会签：`owner_semantic = human:淮政玮`；公式 / `algorithm_type` 共签仍 `human:唐绍祖`。

---

## §2 模块消费矩阵（TEMP_ 草稿 · 禁止 M_SVC_ORG_* / M_ORG_*）

> 差集列维持 A2 已写 **mapped**（A=0；技术力 = `third_party`）。本表只闭合语义层：落点 + 适用性 + 开放项。`algorithm_type` 列为 **草稿建议**，未会签。  
> **`TEMP_*` ≠ 正式 `M_*`**：只存在于本核对记录与机器卡；**禁止**写入 `metrics/registry/` seed，**禁止**写入 A2 pages `metric_id`。  
> **公式**：一律 **第三方不展开**（A1 科研机构维同档）。本表不写伪加权式。

| temp_id | 招标叶子 / 主落点 | 适用 | 建议 type（未签） | pending |
|---------|-------------------|------|-------------------|---------|
| TEMP_TOPIC_ORG_INDUSTRY_COVER | 产业：涉及领域覆盖 / 增长率 | ✅ kit | STAT | 参与度量化无独立核；禁 `M_SVC_ORG_COVERAGE_*` |
| TEMP_TOPIC_ORG_TECH_LAYOUT | 技术领域布局 | ✅ kit | STAT | 领域科技综合实力无独立 ID → TORG-B08 |
| TEMP_TOPIC_ORG_NEW_TREND | 新增：选定领域新增机构数量趋势 | ✅ kit | STAT | 05 seq 99(4) 正文混入「服务机构」字样仍是本核；禁 `M_SVC_ORG_NEW_COUNT` |
| TEMP_TOPIC_ORG_ATTENTION | 新增同叶：科研关注度 | ✅ kit | STAT | 04 要新增数+增速；05 未单列 → TORG-B02 |
| TEMP_TOPIC_ORG_SZ_STATUS | 深圳现状解读（优势与不足报告） | ✅ kit | MIXED | 配置壳 N/A；优势/痛点专叶见下，不重复算覆盖 |
| TEMP_TOPIC_ORG_COLLAB_CHAIN | 合作关系链：强度 / 类型 / 核心节点 | ✅ kit | GRAPH | G1 **A 面**；TORG-B05；禁 `M_SVC_GRAPH_*` / `M_SYNTH_COLLAB_*` |
| TEMP_TOPIC_ORG_TECH_SCORE | 技术力评价与对比 | ✅ kit | MODEL | **【算法补】**；差集 `third_party`；禁 `M_SVC_ORG_TECH_SCORE`；禁用综合科研实力冒充 |
| TEMP_TOPIC_ORG_ATTRACT_SCORE | 引入推荐指数 + 名单规模 | ✅ kit | MODEL | G3 **Job**；TORG-B04；禁 `M_SVC_REC_ATTRACT_SCORE` |
| TEMP_TOPIC_ORG_CULTIVATE_SCORE | 扶持/培育推荐指数 + 名单规模 | ✅ kit | MODEL | G3 **Job**；TORG-B04；禁 `M_SVC_REC_CULTIVATE_SCORE` |
| TEMP_TOPIC_ORG_SZ_ADVANTAGE | 深圳科研机构优势 | ✅ kit | MODEL | G3；维名 04≠05≠R-13 → TORG-B09 |
| TEMP_TOPIC_ORG_PAINPOINT | 深圳科研机构痛难点 | ✅ kit | MODEL | G3；维名 04≠05≠R-14/R-28 → TORG-B10 |

**11/11 TEMP_ 均 mapped 或 third_party + 本叶 present。** 不得因「口径未冻 / D1 missing / 无正式 M_* / 第三方不展开」把上表改成差集 `missing`。不得把上表改写成 `M_SVC_ORG_*`。正式草稿 ID 见 **§8 赋号表**（TEMP 非终态）。

---

## §3 ④ 指标语义卡（按招标叶子 · 不写 seed）

身份项（temp_id / 中文名 / 口径）由淮政玮本工作流确认适用。公式 / 权重 / `algorithm_type` 一律 `pending_cosign: human:唐绍祖`。源表以 05.4「Java `/topic/v1/institution/**` 只读 ADS」+ A1 科研机构维 ODS 判定为准，**不**把项目 DWD 反推成 ODS `full`。A1 双表未交 → 本叶不填伪 full。

8 件套草稿字段（TEMP_ 共同）：正式草稿 metric_id=§8；本节 temp_id 仅对照；源系统=科技专题服务系统·科研机构维；更新频率=未定；version=`draft-open-r4`；源表=ADS 专题科研机构（A1 表2 未交）；公式=**第三方不展开**。

### §3.1 产业 · kit（Bid seq 60；05 `.1`（1） / seq 99（1）；R-03/R-19）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ORG_INDUSTRY_COVER | 科研机构产业领域覆盖 | 选定机构（或选定产业范围下的机构集合）参与的产业链领域覆盖及趋势。筛选壳本身见 §3.12 | 第三方不展开。禁止编领域数加权伪公式 | STAT |

R-19「各领域参与度」无独立核 → 不发明 `TEMP_…_DEPTH`。禁止 `M_SVC_ORG_COVERAGE_BREADTH` / `M_SVC_ORG_COVERAGE_DEPTH`。

### §3.2 技术领域布局 · kit（Bid seq 62；05 `.6.1` / seq 149；R-11/R-20）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ORG_TECH_LAYOUT | 科研机构技术领域布局 | 所选机构在核心学科 / 前沿方向 / 产业技术链中的布局特征 | 第三方不展开。seq 149 输出「各领域科技综合实力」**不另造 ID**（TORG-B08），也**不得**冒充 §3.7 可配置多机构技术力 | STAT |

### §3.3 新增动态 · kit（Bid seq 64–65；05 `.1`（4） / seq 99（4）；R-06/R-21）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ORG_NEW_TREND | 新增科研机构趋势 | 选定产业/技术领域内，新增科研机构数量随时间变化 | 第三方不展开。**禁止**因 seq 99(4) 正文混写「服务机构」而挂 `M_SVC_ORG_NEW_COUNT` | STAT |
| TEMP_TOPIC_ORG_ATTENTION | 科研关注度 | 由新增数量及增长速率得到的领域科研关注度趋势（04 seq 65） | 第三方不展开。05 未单列「关注度」专叶，能对上基础指标变化分析 → mapped，不是 missing（TORG-B02） | STAT |

领域选择（seq 63）是筛选壳 → §3.12。禁止发明 `M_ORG_ATTENTION`。

### §3.4 深圳现状 · kit（Bid seq 67；05 `.1` + `.6.1`）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ORG_SZ_STATUS | 深圳科研机构现状解读 | 深圳科研机构在该产业的优势与不足报告，突出关键指标表现 | 第三方不展开。优势专叶 seq 151、痛点专叶 seq 152 **不在本条重复算覆盖** | MIXED |

评价框架配置（seq 66）是交互 → §3.12。不得用 `M_CHAIN_SZ_INSTITUTION_COUNT` 顶替。

### §3.5 合作关系链 · kit（Bid seq 70–71；05 `.6.5` **G1 A 面** / seq 153；R-15/R-23）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ORG_COLLAB_CHAIN | 科研合作关系链条 | 从论文/专利等构建合作网络；展示合作强度、类型及核心节点 | 第三方不展开。强度/紧密度/频率/中心性 **不编公式**（TORG-B05） | GRAPH |

**A 面当前图（Nebula）**，不是产业服务图谱。图谱 seq 115 为前置抽取，本条不改挂 115。禁止 `M_SVC_GRAPH_*` / `M_SYNTH_COLLAB_*`。配置壳 seq 69 → §3.12。

### §3.6 引入推荐 · kit（Bid seq 75–77；05 `.6.6` **G3 Job** / seq 154；R-16/R-25）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ORG_ATTRACT_SCORE | 科研机构招引推荐指数 | 对候选科研机构多维评估后的招引优先级得分；名单规模为同核 STAT 面，不另造 CNT ID | 第三方不展开。04 招引维 vs 05 学术影响力/科技成果/团队实力 vs R-16 产业关联/区域互补/科研实力/政策契合 → TORG-B04 | MODEL |

**Job，不是服务机构招引。** 推荐理由文本无独立 ID。禁止 `M_SVC_REC_ATTRACT_SCORE` / `M_SVC_REC_CANDIDATE_CNT`。配置壳 seq 75 → §3.12。

### §3.7 技术力对比 · kit（Bid seq 72–74；05.4 **【算法补】**；R-24）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ORG_TECH_SCORE | 科研机构技术力评价与对比 | 用户从技术力指标库多选并设权后，计算各机构技术力得分；支撑雷达/条形对比与综合排名 | **第三方不展开**。05 十叶无专叶 → 差集 `third_party`，**不是** missing，**不是** mapped 到 seq 99(3) 综合科研实力或 seq 149 领域科技综合实力 | MODEL |

评价指标参数配置（seq 72）是交互 → §3.12。**禁止** `M_SVC_ORG_TECH_SCORE`（服务机构技术力 ≠ 科研机构技术力）。不发明 `M_ORG_TECH_*`。

### §3.8 培育（扶持）推荐 · kit（Bid seq 78–79；05 `.6.7` **G3 Job** / seq 155；R-17/R-26）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ORG_CULTIVATE_SCORE | 科研机构扶持推荐指数 | 对深圳本地科研机构评估后的培育/扶持优先级得分 + 建议名单规模；「一院一策」为文本，无独立 ID | 第三方不展开。04 培育维 vs 05 成果/经费效率/人才结构 vs R-17 产出质量/创新/合作潜力/区域贡献 → TORG-B04 | MODEL |

**Job。** 禁止 `M_SVC_REC_CULTIVATE_SCORE`。

### §3.9 深圳优势 · kit（Bid seq 80–81；05 `.6.3` / seq 151；R-13/R-27）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ORG_SZ_ADVANTAGE | 深圳科研机构优势 | 选定产业下深圳科研机构相对全国（或对照集合）的优势分析报告 | 第三方不展开。04 用户选指标 vs 05 成果/经费/人才 vs R-13 成果/创新/学术影响力/合作活跃度 → TORG-B09 | MODEL |

**G3。** 指标选择壳 seq 80 → §3.12。

### §3.10 痛难点 · kit（Bid seq 82–83；05 `.6.4` / seq 152；R-14/R-28）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ORG_PAINPOINT | 深圳科研机构痛难点 | 识别痛难点并给出改进建议与分析报告 | 第三方不展开。04 用户选业务指标 vs 05 项目/转化/人才/产业合作 vs R-14 投入/转化/人才引进/国际合作 vs R-28 转化率低、人才流失 → TORG-B10 | MODEL |

**G3。** 禁止用企业痛点 `M_ENT_PAINPOINT_*` 或服务机构口径顶替。

### §3.11 基础指标(2)(3) · 无独立招标核（不另造 TEMP）

seq 99（2）重点科研机构阈值识别、（3）综合科研实力及趋势：**不是** 05.4 十招标叶子。服务于产业/现状等展示，**禁止**发明 `TEMP_TOPIC_ORG_KEY_*` / `TEMP_TOPIC_ORG_STRENGTH` 正式化进 seed；**禁止**用综合科研实力冒充 §3.7 可配置技术力（TORG-B07）。差集不打 missing。

### §3.12 ④ 不适用（N/A + 依据）

整页 N/A：**无**（十招标叶子均有统计/指数/网络）。

| 宿主 | 项 | 差集判定 | N/A 依据 |
|------|----|----------|----------|
| 历程 `.6.2` | 科研机构发展历程时间线（TORG-D17 / seq 150） | **`n/a_ops`** | 05.4 明文 CMS。04 二十五条无独立历程需规。CMS **不进算法差集主清单**。seq 150 叶存在 → **禁止 missing**，也不把 CMS 改判 mapped。 |
| 交互壳 | 机构选取 / 领域选择 / 评价框架 / 合作数据源 / 技术力指标权 / 招引条件 / 优势指标选择 / 痛点业务指标（TORG-D01/D04/D07/D09/D11；seq 59/61/63/66/68/69/72/75/80/82） | **`n/a_ops`** | 检索/筛选/配置壳不进算法库；统计核仍走对应 TEMP_。严禁用图谱 seq 114 冒充检索算法。 |
| 图谱基建 | 实体识别 / 关系抽取（seq 114/115） | other_system（差集）/ ④ **无独立核** | 服务合作 A 面当前图；04 无独立「实体识别」叶。不发明图谱统计 `M_*`。 |
| 本叶范围外 | 产业服务链服务机构（SVCCHAIN 四页） | **`other_system`** | **禁止**消费 Round 1 OPEN 与全部 `M_SVC_ORG_*` / `M_SVC_REC_*` / `M_SVC_GRAPH_*`。05 产业服务 seq 172–181 不算本页覆盖或 missing。 |
| 本叶范围外 | 产业链机构形近 ID | **`other_system`** | `M_CHAIN_INSTITUTION_*` / `REG_RESEARCH_ORG` / `ACADEMIC_POWER` / `REG_PAPERS` / `REG_PATENT` 不是专题科研机构分析。 |
| 本叶范围外 | 门户 R-29~32（全球概况 / 领先 top20 / 深圳介绍） | **`other_system`** | catalog 快速入口；A2.2 / W5 门户另对。不列本页 demands。 |
| 本叶范围外 | 运营 R-33/R-34；`TOPIC-OPS` / `TOPIC-DATAREQ` | `n/a_ops` | 给人说明 §8.4：运营/需求面走 N/A，不算缺 OPEN 任务。 |
| 产品不做 | 独立机构本体（05.4 §7） | 不记 A 类 | 存储域未建，同构 ENT/CHAIN，禁止平行 stores。 |
| 无独立核的分项 | 领域参与度、重点机构阈值、综合科研实力、领域科技综合实力、招引/扶持分维、合作强度分项、优势/痛点分维 | 语义债 TORG-B02…B10 | **禁止**发明正式 `M_ORG_*` 或把 TEMP_ 写入 seed |

---

## §4 ⑤ 开放项（已登记 · 不升 🟢）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| TORG-B01 | **本叶闭合文件级**：核对记录 present。A2 catalog 正文 Round 17 才改指针 | 语义欠账→有指针；非 A 类 missing |
| TORG-B02 | 「科研关注度」无正式口径与 metric_id | 语义债；不发明 `M_ORG_ATTENTION` |
| TORG-B03 | 技术力对比无专叶、无正式 ID（【算法补】） | 语义债；差集保持 third_party；不消费 `M_SVC_ORG_TECH_SCORE` |
| TORG-B04 | 招引/扶持推荐指数分项无正式 ID；04/05/R-* 维名未冻 | 语义债；禁 `M_SVC_REC_*` |
| TORG-B05 | 合作强度/类型/核心节点无正式 ID | 语义债；禁 `M_SVC_GRAPH_*` |
| TORG-B06 | PDR-05/06 本包有条件未会签 | ⏳；不把「未会签」写成 A 类 missing |
| TORG-B07 | 重点机构阈值 / 综合科研实力非十招标独立叶 | 语义债；禁冒充技术力；不另造 TEMP 进 seed |
| TORG-B08 | 布局「领域科技综合实力」无独立 ID | 语义债；禁与 D12 混挂 |
| TORG-B09 | 优势对标维 04≠05≠R-13 | 语义债 |
| TORG-B10 | 痛点诊断维 04≠05≠R-14/R-28 | 语义债 |

未关闭任何甲方项。未改 `客户决策清单跟踪表.md`。赋号 loop 叶级 `Q-MO-ORG-01`…`09` 见 `id-assign/TOPIC-ORG-METRIC-OPEN-L01-questions.yaml`（🟡 内部默认）；**尚未**写入共享 QUESTIONS / `Q-TOPIC-ORG-*`。本记录 + A2 `semantic_debt` 仍为 OPEN 语义债真源。

---

## §5 贴源摘要（data-agent 协作 · 不改 registry）

| 层 | 结论 |
|----|------|
| 调用链 | 前端 → Java `/topic/v1/institution/**` → 只读 ADS。引入/扶持 = Job；合作链 = A 面 G1（Nebula 当前图）。Java 不写 NLP / 不直连 nGQL。 |
| 准入 / ODS | 机构主数据走要素库；A1 科研机构维表2 未交 → 本叶 D3 不得伪 `full`。服务机构 ODS **不**自动当作科研机构核。 |
| 算法库 05 | 基础指标 1 + 图谱 2 + 深度 7 = 10 叶。能对上招标叶子 → mapped。技术力无专叶 → third_party。历程 CMS → n/a_ops。A1 双表未交 → `A1需规ID` 空。 |
| 实现类 | `third_party`：公式不伪展开；mapped 只表示库已涉及，不是「已有正式 M_*」。 |
| 本叶不做 | 不写 `cfg_metric-*-seed.yaml`；不发明 `M_ORG_*`；不把 `M_SVC_ORG_*` 改挂本页；不新建 `data-gap-catalog`（文案真源仍 A2 `semantic_debt` + 本 §4）。 |

---

## §6 UI / 评审挂载要求（给 V1 / 迁移叶）

- 凡统计数字：ⓘ MetricSpecCard。seed **无**本页正式 ID → 回指 **本记录 TEMP_**，**禁止**点开 `M_SVC_ORG_*` / `M_CHAIN_INSTITUTION_*` 伪 8 件套
- Wave 0：🧪 MockBadge
- 维名/权重未冻：⚠️「待甲方确认」（文案走 TORG-B*）
- TEMP_ 未入 seed：D1 按 `missing`/`draft` 诚实；红问号或 draft ⓘ，**不显伪 8 件套**
- 关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / 就绪度字样
- 功能实现 Owner = **待指定**（给人说明 §2.1 / §2.2：技术链/科研机构/人才功能 Owner 未点名，**禁止猜填**）。指标清单 + 九新对接 = `human:郭万迎`（`JIUXIN-TECH-ORG-TALENT-L01`；李伟辅助抽清单）。STAT → GDF ADS + Java 聚合（Owner 指定前不猜填 Java 负责人）；MODEL/GRAPH/Job 计算仍归唐绍祖监管 Python

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录 | `产品整体定义/科技专题服务系统-完整详细设计/METRIC-OPEN-TOPIC-ORG-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/TOPIC-ORG-METRIC-OPEN-L01.yaml` |
| A2 指针补丁（本叶） | `metrics/request/_work/open-loop/TOPIC-ORG-METRIC-OPEN-L01-a2-patch.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/TOPIC-ORG-METRIC-OPEN-L01.yaml` |
| 叶级 Question | `metrics/request/_work/id-assign/TOPIC-ORG-METRIC-OPEN-L01-questions.yaml` |
| 薄 handoff | `agent-handoffs/算法库联调-ALGO-LIB/TOPIC-ORG-METRIC-OPEN-L01.md` |
| **未改** | `metrics/registry/` seed / 矩阵；A2 catalog 正文（Round 17）；共享 `METRIC-OPEN-LOOP-a2-patch.yaml`；`LOOP-state.yaml`；`METRIC-SEMANTIC-QUESTIONS.md`；展示 catalog；其它 OPEN 叶 |

---

## §8 赋号表（TEMP → M_* · 草稿 · 类型未签）

> **日期**：2026-08-22 · `owner_semantic=human:淮政玮` · `algorithm_type_status=suggested_unsigned`（不替唐绍祖签）  
> **ELEMENT**=`ORG`。机器卡 11 条 `TEMP_TOPIC_ORG_*` 全转正草稿，**reuse=0**（seed `domain=ORG` 为 0；所拟 11 号 getMetric 均 missing）。  
> **禁止改挂** `M_SVC_ORG_*` / `M_SVC_REC_*` / `M_SVC_GRAPH_*` / `M_CHAIN_INSTITUTION_*` / `M_SYNTH_COLLAB_*` / `M_ENT_*` 形近 ID（可 mapped 说明）。**禁止写入 seed**。  
> 歧义只进叶级 `id-assign/TOPIC-ORG-METRIC-OPEN-L01-questions.yaml`（Q-MO-ORG-01…09），不写共享 QUESTIONS。

| temp_id | metric_id | reuse | 建议 type（未签） | pending |
|---------|-----------|-------|-------------------|---------|
| TEMP_TOPIC_ORG_INDUSTRY_COVER | M_ORG_INDUSTRY_COVER | — | STAT | — |
| TEMP_TOPIC_ORG_TECH_LAYOUT | M_ORG_TECH_LAYOUT | — | STAT | Q-MO-ORG-03 |
| TEMP_TOPIC_ORG_NEW_TREND | M_ORG_NEW_TREND | — | STAT | Q-MO-ORG-01 |
| TEMP_TOPIC_ORG_ATTENTION | M_ORG_ATTENTION_TREND | — | COMPUTE | Q-MO-ORG-02 |
| TEMP_TOPIC_ORG_SZ_STATUS | M_ORG_SZ_STATUS | — | MIXED | Q-MO-ORG-04 |
| TEMP_TOPIC_ORG_COLLAB_CHAIN | M_ORG_COLLAB_CHAIN | — | GRAPH | Q-MO-ORG-05 |
| TEMP_TOPIC_ORG_TECH_SCORE | M_ORG_TECH_SCORE | — | MODEL | Q-MO-ORG-06 |
| TEMP_TOPIC_ORG_ATTRACT_SCORE | M_ORG_ATTRACT_SCORE | — | MODEL | Q-MO-ORG-07 |
| TEMP_TOPIC_ORG_CULTIVATE_SCORE | M_ORG_CULTIVATE_SCORE | — | MODEL | Q-MO-ORG-07 |
| TEMP_TOPIC_ORG_SZ_ADVANTAGE | M_ORG_SZ_ADVANTAGE | — | MODEL | Q-MO-ORG-08 |
| TEMP_TOPIC_ORG_PAINPOINT | M_ORG_SZ_PAINPOINT | — | MODEL | Q-MO-ORG-09 |

**计数**：赋号 11 / 复用 0 / 新建 11 / Q 9。建议类型：STAT 3 · COMPUTE 1 · MIXED 1 · GRAPH 1 · MODEL 5。

关注度 OPEN Round 4 曾标 STAT；本 loop 按「新增数+增速合成」改为建议 **COMPUTE**（未签）。形近对照与口径草稿见赋号卡 `lookalike_*` / `definition_draft`。

---

## §9 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _口径草稿已出；适用性：TOPIC-ORG-05 **kit**；赋号草稿 11 条 `M_ORG_*`（reuse=0，§8）；历程 CMS / 筛选壳 / 门户 / 图谱无独立核 / 服务机构 N/A 见 §3.12；**零改挂** `M_SVC_ORG_*` / `M_CHAIN_INSTITUTION_*`；**未写入** seed；公式第三方不展开；类型 suggested_unsigned_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）_ | |
| 甲方口径 | — | 叶级 `Q-MO-ORG-01`…`09` 🟡（内部默认）；未写入共享 QUESTIONS / 客户决策清单；不升 🟢 | |
