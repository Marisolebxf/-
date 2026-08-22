# METRIC-OPEN-DS-08-科技指数-核对记录

> **任务**：DS-08-METRIC-OPEN-L01（METRIC-OPEN-LOOP Round 15 / 波 B）  
> **角色**：product-agent（口径草稿）+ algorithm-agent / data-agent（协作核对，本叶不改 seed）  
> **监管人**：`human:淮政玮`  
> **日期**：2026-08-22  
> **上游**：无独立四件套 / PACK-L01；本工作流书面 **SRS 02 科技指数 + 详设 04 顶 PACK**（给人说明 §8.4 甲）  
> **范围**：展示 catalog `ds_id=DS-08` **全部 3 个** `page_id` 的 ④ 指标语义卡 + ⑤ 开放项。不替甲方拍板；公式 / `algorithm_type` **不签**，标 `pending_cosign: human:唐绍祖`（8/25 前不派唐绍祖开工本 loop）。  
> **Q-TINDEX-01 / 03**：保持 **待登 / 🟡**，不升 🟢，不新建撞号 `Q0xx`。本叶可建 `Q-MO-DS08-nn`（见 §赋号表）。  
> **SYNTH 三兄弟**：已有 OPEN。本叶 **禁止改挂** `M_SYNTH_*` 为本页正式 ID；可 mapped 同源说明。  
> **预测 / 综合 501**：本叶无预测专叶（预测在 DS-09）；综合指数计算在智库后台（Q-TINDEX-01）。展示侧 **不标 501**、**不把差集改 mapped**。  
> **Wave B 赋号**（2026-08-22）：`TEMP_*` 非终态；正式草稿 ID 见 **§赋号表**；**未写** seed。

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ 适用且文档闭合（口径草稿） | 3 页中 **2 页 kit**、**1 页整页 N/A + 依据**（`DS-08-INDICATOR`）。SRS 02 / 详设 04 / A2 页 yaml **未挂**任何正式 `metric_id`；metric-registry 查 `TINDEX` / 「科技指数」**0 条** → 卡面只用 **`TEMP_DS08_*`**。**禁止**发明正式 `M_*` / `M_TINDEX_*` 写入 seed。 |
| #5 开放项 | ✅ 适用且已登记（本记录） | 沿用已有待登项 `Q-TINDEX-01`～`04` 与影响力统称 `Q069` / `Q071`，以及 A2 语义债 `RANK-B01..B02` / `VIZ-B01..B02` / `TI-B01..B02`。**不新建** `Q0xx`（避免与展示企业 Q010～Q019、政策 QPOL、指数 Q-TINDEX 撞号）。本叶不改 `客户决策清单跟踪表.md`、不升 🟢、不新建 `data-gap-catalog`（文案真源 = 本 §4 + A2 `semantic_debt`）。 |
| PDR-05 自检 | ⏳ 有条件 | 无 TRACE/WF 第 6 列；本记录 + A2 `pages/DS-08-*.yaml` 可回指。门 1 完整闭合仍须正式 ID 会签（不发明）+ 公式会签 + 甲方 🟡。 |
| PDR-06 自检 | ⏳ 有条件 | RANK / VIZ 看板可写演示 STAT；H 指数 / 活跃度实现类 third_party、权重 / 分类树 / 综合合成公式 `pending_cosign`。 |
| 语义 Owner（本工作流） | `human:淮政玮` | 口径 / 8 件套身份项 / 适用性 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop 不签公式、不改 seed `algorithm_type` |

**结论**：DS-08 **非整包 N/A**。指标展示页整页 N/A（字典 / 配置说明壳）；排行榜与可视化有榜单分值 / 指数读数 / 专家 H·活跃度 → **出卡**。甲方 🟡 / 公式未签 **不阻断**定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。**OPEN present 不是覆盖证明。本页 A=0，不得把 other_system / third_party 改成 missing 或 mapped。**

### §1.1 本叶必须消费本核对记录（catalog 3 页）

| 页 `page_id` | 中文（需规五级） | ④ | 消费的 ID | 禁止 |
|--------------|------------------|----|-----------|------|
| `DS-08-RANK` | 排行榜 | **kit** | `TEMP_DS08_RANK_SCORE` | 改挂 `M_SYNTH_VIT_RANK` / `M_SYNTH_ELEM_RANK` / `M_CHAIN_SZ_ADVANTAGE_RANK`；also_in DS-04-CARRIER-RANK / DS-04-CITY / DS-05 / DS-06；按号 mapped 05 seq 171–177；发明 `M_TINDEX_*`；把 Q-TINDEX-01 升 🟢 |
| `DS-08-VIZ` | 指数可视化展示 | **kit** | `TEMP_DS08_TINDEX_VALUE` · `TEMP_DS08_VIZ_INFLUENCE` · `TEMP_DS08_VIZ_HINDEX` · `TEMP_DS08_VIZ_ACTIVITY` | 改挂 `M_SYNTH_VIT_*` / `M_SYNTH_ELEM_*` / `M_CHAIN_ACADEMIC_POWER`；按号 mapped 05 seq 164–170（人才招引/政策深度）；also_in DS-09 预警 / DS-04-REALTIME seq 71 / DS-07-SCI-CREATE seq 139；智库 xlsx 122/134/135/144；TOPIC-QUERY |
| `DS-08-INDICATOR` | 指标展示 | **N/A + 依据** | 无 TEMP_ | 发明 `M_TINDEX_*`；因「计算方法/权重」整页 mapped 182–191；改挂 `M_SYNTH_*` / `M_CHAIN_COMPETITIVENESS_INDEX`；复制 DS-05-GBA-INDICATOR / DS-06-INDICATOR 判定；把字典壳写成 A 类 missing |

**本叶不消费**：专题 TOPIC-ENT / TOPIC-QUERY / SYNTH Job 正式 ID；展示 ENT-MOD-*；DS-04 载体/城市排名；DS-05 湾区；DS-06 深圳监测/载体；DS-07 评估四页；DS-09 规划预警；DS-13～16 人才态势。B 轨已有 ID **不得 missing、不得改挂**为本页正式 ID。

**SYNTH 三兄弟（已有 OPEN，本叶零改挂）**：`SYNTH-VITALITY` / `SYNTH-ELEMENT` / `SYNTH-COLLAB` 已登记 OPEN。本页可 **mapped 同源说明**（对照 05 seq 186–191 区域综合），对象=**区域**，≠ 科技成果榜、≠ 展示侧科技指数字典、≠ 专家 H/活跃度图。metric-registry：`M_SYNTH_VIT_INDEX`（区域创新活力指数）/`M_SYNTH_VIT_RANK`（对比范围活力排名）等 **seed 已在**；**禁止**改挂为本页正式 ID，禁止把专题 `M_SYNTH_ELEM_CONTRIB` / `M_SYNTH_COLLAB_OUTPUT_CORR` missing 重列或改 mapped。

### §1.2 需规 19 叶 × 差集（对照 A2；本叶不改判定）

| 五级 | seq | 招标叶子 | A2 差集（保持） | ④ |
|------|-----|----------|-----------------|----|
| 指标展示 | 159 | 指标项展示 | other_system | **整页 N/A** |
| 指标展示 | 160 | 指标概述查看 | other_system | 整页 N/A |
| 指标展示 | 161 | 指标计算方法说明 | n/a_ops | 整页 N/A |
| 指标展示 | 162 | 指标意义解读 | other_system | 整页 N/A |
| 指标展示 | 163 | 指标权重展示 | n/a_ops | 整页 N/A（配置读数，非独立核） |
| 可视化 | 164 | 专家H指数排行可视化 | **third_party** seq 162 | **kit** TEMP_HINDEX |
| 可视化 | 165 | 科技指数分布区域可视化 | other_system | **kit**（消费 TEMP_TINDEX_VALUE） |
| 可视化 | 166 | 科技影响力趋势可视化 | other_system | **kit** TEMP_INFLUENCE；**不是**预测、不 501 |
| 可视化 | 167 | 专家活跃度可视化 | **third_party** seq 162 | **kit** TEMP_ACTIVITY |
| 可视化 | 168–170 | 大屏导航 / 图交互 / 图导出 | n/a_ops ×3 | 无独立核 |
| 排行榜 | 171 | 科技成果综合排名 | other_system | **kit** TEMP_RANK_SCORE |
| 排行榜 | 172 | 分类排名展示 | other_system | 无独立核（切面消费 TEMP_RANK_SCORE） |
| 排行榜 | 173 | 排名详情查看 | n/a_ops | 无独立核 |
| 排行榜 | 174 | 排名历史变化 | other_system | 无独立核（时序消费 TEMP_RANK_SCORE） |
| 排行榜 | 175 | 排名对比分析 | other_system | 无独立核 |
| 排行榜 | 176–177 | 筛选搜索 / 结果导出 | n/a_ops ×2 | 无独立核 |

**本三页 A=0。库缺口 missing 行：无。** 不得因本 OPEN `present` 把 other_system / third_party 改成 mapped，也不得因「05 无科技成果综合排名专叶」改打 missing。专题已记 missing 7 条不重列。

xlsx 行 92「科技指数值」：RANK yaml 指向 INDICATOR，VIZ yaml 指向 INDICATOR，INDICATOR yaml 指向 VIZ。**本叶收口**：数值读面宿主 = **VIZ**（`TEMP_DS08_TINDEX_VALUE`）；INDICATOR 只做字典壳，不抢该 TEMP_。

### §1.3 TRACE / A2 语义层指针（Round 18 才回写 catalog 正文）

本叶 **不改** `metrics/request/展示系统/A2-GAP-page-catalog.yaml` 与 pages yaml 正文。指针写入 `_work/open-loop/DS-08-METRIC-OPEN-L01-a2-patch.yaml`（**不**写共享 `METRIC-OPEN-LOOP-a2-patch.yaml` / `LOOP-state.yaml`）。

| 层 | 路径 | 本叶要求的指针 |
|----|------|----------------|
| 核对记录 | **本文件** | DS-08 三页唯一 OPEN 真源 |
| A2 页 yaml | `metrics/request/展示系统/pages/DS-08-*.yaml` | 应收口：`metric_open_status: present`；`metric_open_path` = 本文件；`metric_open_task: DS-08-METRIC-OPEN-L01`。**库缺口判定不动**（本页本无 A 类 missing）。`DS-08-INDICATOR` 升 present + 本文件 N/A 依据。 |
| A2 catalog | `A2-GAP-page-catalog.yaml` 的 `ds_id=DS-08` 三页 | 删「无 METRIC-OPEN → 只记语义欠账」中已被本叶覆盖的句；RANK 的 catalog 注「展示侧指数；智库管理 Q-TINDEX-01」**保留**（口径仍待登） |
| TRACE / WF | **无**展示四件套 | `trace_metrics` / `wireframe_metric_ids` 保持空；不从 02 叙述发明 `M_*` |
| PACK | 无独立 `DS-08-PACK-L01` | SRS 02 + 详设 04 顶 PACK；FDS **不顶** OPEN |

口径会签：`owner_semantic = human:淮政玮`；公式 / `algorithm_type` 共签仍 `human:唐绍祖`。页面要哪些指标主责（展示）= `human:李伟`（给人说明），**不定**本叶清单、不改挂。

---

## §2 模块消费矩阵（TEMP_ 草稿 · 禁止正式 M_*）

> `TEMP_*` ≠ 正式 `M_*`：只存在于本核对记录与机器卡；**禁止**写入 `metrics/registry/` seed。  
> `algorithm_type` 列为 **草稿建议**，未会签。差集列维持 A2 已写判定。

| temp_id | 主落点 | 适用 | 建议 type（未签） | 差集保持 | pending |
|---------|--------|------|-------------------|----------|---------|
| TEMP_DS08_RANK_SCORE | RANK seq 171（seq 172/174/175 消费同一分值/名次） | ✅ kit | STAT | other_system | RANK-B02；Q-TINDEX-01/03；禁 SYNTH 排名 ID、禁 DS-04 CITY/载体榜 |
| TEMP_DS08_TINDEX_VALUE | VIZ seq 165 + xlsx 92/93 | ✅ kit | STAT | other_system | Q-TINDEX-01/02；禁 mapped 186/98/116；禁改挂 `M_SYNTH_VIT_INDEX` |
| TEMP_DS08_VIZ_INFLUENCE | VIZ seq 166 + xlsx 91 | ✅ kit | STAT | other_system | Q069/Q071；**不是预测、不 501**；禁 DS-09 / DS-04 seq 71 / DS-07 seq 139 |
| TEMP_DS08_VIZ_HINDEX | VIZ seq 164 + xlsx 95 | ✅ kit | third_party | third_party 162 | VIZ-B02；禁 `M_CHAIN_ACADEMIC_POWER`；禁伪展开 Hirsch 公式 |
| TEMP_DS08_VIZ_ACTIVITY | VIZ seq 167 + xlsx 90 | ✅ kit | third_party | third_party 162 | VIZ-B02（项目/学术活动无专核）；禁 mapped 157；禁智库活跃度行 |

**5/5 TEMP_ 均 present。** 不得因「口径未冻 / D1 missing / 无正式 M_* / 可 501」把上表改成差集 `mapped`，也不得把 other_system 改成 missing。

---

## §赋号表（TEMP → 正式 `M_*` · 建议类型未签）

> **日期**：2026-08-22 · product-agent · 监管 `human:淮政玮`  
> ELEMENT=`INNOV`。机器卡 `demands` **5/5** 新建，**reuse=0**。`algorithm_type_suggested` 一律 `suggested_unsigned`，不替唐绍祖签。  
> 注释 `TEMP_RANK_SCORE` / `TEMP_TINDEX_VALUE` **不是**额外 ID。**INDICATOR 整页 N/A 不造号**。  
> **禁止改挂** `M_SYNTH_VIT_*` / `M_CHAIN_ACADEMIC_POWER`（顶 H/活跃度）/ `M_INNOV_SCHOLAR_INFLUENCE`。  
> **未写** seed / 展示 catalog / 共享 QUESTIONS / 客户决策清单。Q-TINDEX-01 / 03 **保持待登**。501 在 DS-09，本页不标 501、不改 mapped。

| temp_id | metric_id | reuse | 建议 type（未签） | Q |
|---------|-----------|-------|-------------------|---|
| TEMP_DS08_RANK_SCORE | M_INNOV_SCIINDEX_RANK_SCORE | 不 reuse `M_SYNTH_VIT_RANK` / `M_INNOV_CITY_RANK_GLOBAL` / `M_INNOV_ACHIEVE_VALUE` | STAT | Q-TINDEX-01（待登）；权重跟 Q-TINDEX-03（待登） |
| TEMP_DS08_TINDEX_VALUE | M_INNOV_SCIINDEX_VALUE | 不 reuse `M_SYNTH_VIT_INDEX` | STAT | Q-MO-DS08-01；分类树 Q-TINDEX-02（待登） |
| TEMP_DS08_VIZ_INFLUENCE | M_INNOV_SCIINDEX_INFLUENCE | 不 reuse `M_INNOV_IMPACT_SCORE` / `M_INNOV_IMPACT_FORECAST` | STAT | Q069 / Q071（待登）；**不 501** |
| TEMP_DS08_VIZ_HINDEX | M_INNOV_EXPERT_HINDEX | 不 reuse `M_CHAIN_ACADEMIC_POWER` / `M_INNOV_SCHOLAR_INFLUENCE` / `M_TALENT_ACADEMIC_SCORE` | third_party | Q-MO-DS08-02 |
| TEMP_DS08_VIZ_ACTIVITY | M_INNOV_EXPERT_ACTIVITY | 不 reuse `M_CHAIN_ACADEMIC_POWER` / `M_TALENT_FLOW_TRACK` / `M_SYNTH_ELEM_TYPE_SCORE` | third_party | Q-MO-DS08-03 |

**计数**：赋号 5 · 复用 0 · 新 Q 3（Q-MO-DS08-01…03）· 类型 STAT 3 / third_party 2。INDICATOR 0 号。

叶级卡：`metrics/request/_work/id-assign/DS-08-METRIC-OPEN-L01.yaml` + `-questions.yaml`。

---

## §3 ④ 指标语义卡（按 page_id · 不写 seed）

身份项由淮政玮本工作流确认适用。公式 / 权重 / `algorithm_type` 一律 `pending_cosign: human:唐绍祖`。源表以详设 04「DS-08 = M · ADS · 展示侧；智库管理 Q-TINDEX-01」+ A1 双表未交为准，**不**把项目 DWD 反推成 ODS `full`。metric-registry：TINDEX 域 **0 条**；`M_SYNTH_VIT_INDEX` / `M_SYNTH_VIT_RANK` seed 已在且 D1=`missing` → **只作同源对照，不改挂**。

8 件套草稿字段（TEMP_ 共同）：metric_id=下表 temp_id；源系统=科技信息展示系统·科技指数 / 智库已发布指数封装；更新频率=未定；version=`draft-open-ds08`；源表=ADS / 智库指数读面（A1 表2 未交 → 本叶不填伪 full）。

### §3.1 `DS-08-RANK` · kit（seq 171–177）

catalog 注：**展示侧指数口径强依赖 Q-TINDEX-01**。对象=**科技成果**（综合榜 / 分类切面），不是城市、不是创新载体、不是区域 SYNTH 排名。排序读 ADS / 智库指数，原文未点名「基于数据模型计算排名」→ 差集 **other_system** 保持。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS08_RANK_SCORE | 科技成果综合得分与名次 | 展示科技成果综合排名榜单：前 N 名、综合得分、较上一期升降；分类切面（领域/成果类型/机构类型/地域）与历史名次曲线、多成果对比均消费**同一套已落库分值/名次**。对象≠载体（DS-04-CARRIER-RANK）、≠城市（DS-04-CITY）、≠区域活力排名（`M_SYNTH_VIT_RANK`） | 演示：ADS / 智库指数已发布综合分排序；权重跟 Q-TINDEX-03，未签。禁止用 05 seq 171 政策布局、182–191、`M_CHAIN_SZ_ADVANTAGE_RANK` 顶替 | STAT |

半成品 xlsx 行 94「科技指数排名名次」= 本 TEMP_ 的排序键。上期升降=已落库名次差，不另开 missing，不是 seq 174 独立算法。

#### 本页 ④ 不适用（N/A + 依据）

| 项 | 差集 | N/A 依据 |
|----|------|----------|
| 分类排名展示（seq 172） | other_system | 同一 TEMP_RANK_SCORE 按分类切面排序；筛选宿主 seq 176。禁 also_in CARRIER seq 74 / CITY seq 84 |
| 排名详情查看（seq 173） | n/a_ops | 详情壳；计算方法全文归 INDICATOR seq 161，本叶不抢 |
| 排名历史变化（seq 174） | other_system | 历史名次序列读 ADS；消费 TEMP_RANK_SCORE；不是预测、不是 05 技术力 |
| 排名对比分析（seq 175） | other_system | 多选成果并排已有得分；未点名对标模型。禁 mapped 186/191 |
| 排名筛选与搜索（seq 176） | n/a_ops | 关键词 / 排名范围 / 得分区间 / 时间过滤壳 |
| 排名结果导出（seq 177） | n/a_ops | Excel/PDF/排名报告导出壳；禁与 VIZ seq 170 混挂 |

禁止湾区 DS-05、深圳 DS-06 排名页混挂。xlsx 行 90/91/93/95 / 行 92 不进本页。

### §3.2 `DS-08-VIZ` · kit（seq 164–170）

本页是展示侧指数图与专家 H/活跃度图，不跑专题 TALENT / SYNTH Job，不进专家智库后台。

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_DS08_TINDEX_VALUE | 科技指数值（含区域分布读数） | 已发布「科技指数」数值本身；GIS 热力/区域图（seq 165 / xlsx 93）落同一读数。对象=指数空间切面，不是 186 区域创新活力综合评价，不是 seq 98 人才省/国分布 | 演示：ADS / 智库已发布指数；分类树跟 Q-TINDEX-02。禁止改挂 `M_SYNTH_VIT_INDEX` / mapped 186 | STAT |
| TEMP_DS08_VIZ_INFLUENCE | 科技影响力趋势 | 科技影响力随时间的折线/面积读数（xlsx 91）；可按时间范围、领域切换，支持多指标并排。原文=字面读 ADS 时序，**未点名预测模型**。影响力统称口径见 Q069/Q071 | 演示：ADS 时序聚合。**禁止 501**。禁 mapped 186 趋势预测、182 成果综评、DS-09 预警、DS-04 seq 71、DS-07 seq 139 | STAT |
| TEMP_DS08_VIZ_HINDEX | 专家H指数排行 | 柱/雷达展示专家 H 指数排行；可按学科/机构/地域筛选。对照 05 seq 162 人才学术力（学术影响力分项含 H）。实现类 **third_party**，禁止伪展开 Hirsch 公式。排行对象=**专家**，不是 RANK 科技成果榜 | 未签；覆盖判定跟 162。禁 `M_CHAIN_ACADEMIC_POWER`；禁智库 xlsx 122 | third_party |
| TEMP_DS08_VIZ_ACTIVITY | 专家科研活跃度 | 热力/时间轴展示论文数量等科研活跃读面；对照同一 162 叶成果数量/动态更新。项目数/学术活动参与度 05 无专核 → VIZ-B02，不另开 A、不发明 M_* | 未签；third_party。禁 mapped 157 人才流动；禁智库 xlsx 135/134/144；禁 xlsx 29 市场活跃度 | third_party |

知识图谱 / 招入推荐 / 政策深度分析 **不进本页**（展示序号 164–170 碰巧撞 05 人才/政策号，一律禁止按号 mapped）。

#### 本页 ④ 不适用 / 无独立核

| 项 | 差集 | 依据 |
|----|------|------|
| GIS 缩放平移 / 区域下钻壳（seq 165 交互） | other_system | 与 TEMP_TINDEX_VALUE 同一读面；不拆到 DS-01-MAP |
| 大屏导航切换（seq 168） | n/a_ops | 导航/全屏/轮播；大屏内数字仍走本页 TEMP_ |
| 可视化图表交互（seq 169） | n/a_ops | 筛选/维度/指标/时间范围壳 |
| 可视化结果导出（seq 170） | n/a_ops | 图/PDF/可视化报告壳；禁与 RANK seq 177 混挂 |

**501 纪律**：本页趋势 **不是**预测。详设 04 写「预警模型可 501」的是 **DS-09**，不是 DS-08。禁止把 166 标 501 或改 mapped。

### §3.3 `DS-08-INDICATOR` · **整页 N/A**（seq 159–163）

A2 已记五叶均为 metrics catalog / 智库已发布配置的**字典与说明壳**：目录树、概述文案、计算方法**说明**、意义解读、权重**展示**。未点名当场跑综合评价 / AHP / 熵权。指数计算若在智库后台 → 本页只展示（Q-TINDEX-01 待登）。**无独立统计核 / 无模型产出义务**。

与 DS-05-GBA-INDICATOR / DS-06-INDICATOR **只学 schema、禁止复制判定**（那两页有产出值/十一维监测 KPI；本页没有）。

| 项 | 差集 | N/A 依据 |
|----|------|----------|
| 指标项展示（seq 159） | other_system | 一/二/三级指标树读面；不是 05「构建指标体系」。Q-TINDEX-02 分类树待确认 ≠ missing。禁 mapped 182–191、禁 mapped 05 seq 159 |
| 指标概述查看（seq 160） | other_system | catalog / 智库定义文案；禁 mapped 182–191 评价报告 |
| 指标计算方法说明（seq 161） | n/a_ops | 原文是「说明」不是当场跑加权；禁因「计算方法」整页 mapped 182–191；禁 mapped 05 seq 161 |
| 指标意义解读（seq 162） | other_system | 解读文案；未点名生成模型。展示序号 ≠ 人才 162 学术力。禁 mapped 191 |
| 指标权重展示（seq 163） | n/a_ops | 智库 `cfg_index_weight` 已发布配置展示，不是本页 AHP/熵权。Q-TINDEX-03 40/30/20/10 待确认：展示 + ⚠️，不 missing、不发明 `M_TINDEX_*`。禁 mapped 182/188。禁 Q-SYNTH-V-01 活力权重复用为本页 |

禁止发明 `M_TINDEX_*` / `M_IND_*`。xlsx 行 90–95 均非本五级宿主（行 92 收口到 VIZ）。Q-TINDEX-04 菜单并存策略不进算法差集。

---

## §4 ⑤ 开放项（已登记 · 不升 🟢 · 不新建 Q0xx）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| 文件级 OPEN | **本叶闭合**：三页 `metric_open_status: present`（INDICATOR 为 present + N/A 依据） | 语义欠账→有指针；非把差集改 mapped |
| **Q-TINDEX-01** | **引用已有待登项**；展示侧 19 叶 vs 同行评议专家智库管理（遴选/登记/推荐/管理 + 评议公示）是否拆独立后台 | **保持待登 / 🟡**；**不升 🟢**；临时默认：本期只做展示侧，评议后台不进本三页。RANK 口径强依赖本项 |
| Q-TINDEX-02 | 引用；分类树 / 评价范围 | 待登 🟡；INDICATOR 只展示已发布树；不发明 `M_TINDEX_*` |
| Q-TINDEX-03 | 引用；一级权重 40/30/20/10 与熵权/AHP 边界 | 待登 🟡；RANK 综合分 / INDICATOR 权重展示跟已发布配置 + ⚠️ |
| Q-TINDEX-04 | 引用；「科技指数New」与老菜单并存 | 待登 🟡；菜单策略不进算法差集 |
| Q069 / Q071 | 引用；影响力统称分列 | 待登 🟡；VIZ 影响力趋势不另开 A |
| Q070 | 本页不改挂 | 展示指数 vs 专题 `M_SYNTH_VIT_INDEX` 等是 analog 不是 exact |
| RANK-B01 / VIZ-B01 / TI-B01 | 无四件套 / TRACE | 本叶补指针后文件级闭合；不发明 M_* |
| RANK-B02 | 成果综合得分/名次无正式 ID | 语义债；差集 other_system 不动 |
| VIZ-B02 | H 指数/活跃度分项无正式 ID；项目/学术活动无专核 | 语义债；third_party 162 不动 |
| TI-B02 | 指标树与权重无正式 ID | 语义债；other_system / n/a_ops 不动 |
| Q010～Q019 / QPOL-* | 展示企业 / 政策口径族 | **本页不改挂、不关闭** |

未关闭任何甲方项。未改 `客户决策清单跟踪表.md`。未新建 `data-gap-catalog`（⑤ = 本表已有待登项 + A2 `semantic_debt`，**N/A 于新 Q0xx**）。赋号歧义另见叶级 `Q-MO-DS08-01…03`（🟡，不进本表升绿）。

---

## §5 贴源摘要（data-agent 协作 · 不改 registry）

| 层 | 结论 |
|----|------|
| 调用链 | 前端态势菜单 → Java display BFF 拼 metrics catalog + GIS + ADS；智库已发布指数封装只读。Java 不写 NLP / 不直连 nGQL。不在本页跑专题 SYNTH / TALENT Job。 |
| 准入 / ODS | A1 双表未交 → 本叶 D3 不得伪 `full`。V1 读 ADS **不等于** mapped 05。 |
| 预测 / 501 | **本叶不标 501**。趋势可视化 = ADS 时序；预测/预警在 DS-09。综合指数计算在智库后台（Q-TINDEX-01），展示页不跑模型 → **差集不得改 mapped**。 |
| 算法库 05 | H/活跃度 third_party seq 162。GIS/趋势/成果榜 = other_system。INDICATOR 字典不覆盖 182–191。展示序号 159–177 碰巧撞人才/政策/服务链号 → **一律禁止按号 mapped**。 |
| metric-registry | `TINDEX` / 「科技指数」**0 条**。`M_SYNTH_VIT_INDEX`、`M_SYNTH_VIT_RANK`、`M_SYNTH_ELEM_CONTRIB`、`M_SYNTH_COLLAB_OUTPUT_CORR` seed 已在；本叶 **零改挂**。`M_CHAIN_ACADEMIC_POWER` seed 在、矩阵缺 → 不顶替 H 指数。 |
| 本叶不做 | 不写任何 `cfg_metric-*-seed.yaml`；不发明 `M_TINDEX_*` / `M_RANK_*` / `M_VIZ_*`；不改挂 B 轨 / SYNTH / CHAIN / SVC / ENT；不改 A2 catalog 正文；不写共享 LOOP-state / 共享 a2-patch。 |

---

## §6 UI / 评审挂载要求（给 V1 / 迁移叶）

- 凡统计数字：ⓘ MetricSpecCard。seed **无**本页正式 ID → 回指 **本记录 §赋号表草稿** `M_INNOV_SCIINDEX_*` / `M_INNOV_EXPERT_*`（TEMP_ 对照仍有效），**禁止**点开 `M_SYNTH_*` / `M_CHAIN_*` / `M_SVC_*` / `M_ENT_*` / `M_INNOV_SCHOLAR_INFLUENCE` 伪 8 件套
- Wave 0：🧪 MockBadge
- 维名/权重/分类树/展示侧 vs 评议后台未冻：⚠️「待甲方确认」（文案走 Q-TINDEX-01/02/03，不要把评议后台 ID 写进展示 DOM）
- TEMP_ 未入 seed：D1 按 `missing`/`draft` 诚实；红问号或 draft ⓘ，**不显伪 8 件套**
- 关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-TINDEX-*` / `Q0xx` / 就绪度字样
- 功能实现 Owner（展示页要哪些指标）= `human:李伟`；STAT → GDF ADS + Java 聚合；智库封装只读；H/活跃度 third_party 计算仍归唐绍祖监管通道（本 loop 不派）

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录（含 §赋号表） | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-08-科技指数-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/DS-08-METRIC-OPEN-L01.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/DS-08-METRIC-OPEN-L01.yaml` |
| 叶级 Q | `metrics/request/_work/id-assign/DS-08-METRIC-OPEN-L01-questions.yaml` |
| A2 指针补丁（分叶） | `metrics/request/_work/open-loop/DS-08-METRIC-OPEN-L01-a2-patch.yaml` |
| 薄 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-08-METRIC-OPEN-L01.md` |
| **未改** | `metrics/registry/` seed / 矩阵；A2 catalog 正文（Round 18）；共享 `LOOP-state.yaml` / `METRIC-OPEN-LOOP-a2-patch.yaml` / `METRIC-SEMANTIC-QUESTIONS.md`；客户决策清单 |

---

## §8 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _口径草稿已出；三页：RANK / VIZ **kit**；INDICATOR **N/A**；Q-TINDEX-01 **保持待登**；**零改挂** `M_SYNTH_*`；本页 A=0 差集不动；Wave B 赋号草稿 5 条见 §赋号表，**零**正式 `M_*` 入 seed；类型未签_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）_ | |
| 展示页指标清单（李伟） | — | 本叶不定清单、不改挂 | |
| 甲方既有 Q-TINDEX / Q069 / Q071 | — | 不改挂、不升 🟢 | |
