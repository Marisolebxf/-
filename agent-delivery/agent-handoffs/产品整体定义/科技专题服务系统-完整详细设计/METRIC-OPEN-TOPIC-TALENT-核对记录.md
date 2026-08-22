# METRIC-OPEN-TOPIC-TALENT-核对记录

> **任务**：TOPIC-TALENT-METRIC-OPEN-L01（METRIC-OPEN-LOOP Round 5）  
> **角色**：product-agent（口径草稿）+ algorithm-agent / data-agent（协作核对，本叶不改 seed）  
> **监管人**：`human:淮政玮`  
> **日期**：2026-08-22  
> **上游**：无独立四件套 / PACK-L01；本工作流书面 **SRS 04 + 05.5 顶 PACK**（给人说明 §8.4 甲）  
> **范围**：专题人才分析 **一整包** `page_id=TOPIC-TALENT-05` 的 ④ 指标语义卡 + ⑤ 开放项。覆盖 05.5 **十一招标叶子**里进算法差集的那些，外加 05 `.7.2` 流动（有流入/流出/留存统计核）。不替甲方拍板；公式 / `algorithm_type` **不签**，标 `pending_cosign: human:唐绍祖`（8/25 前不派唐绍祖开工本 loop）。  
> **赋号（2026-08-22）**：`TEMP_*` **不再作页面终态**。正式草稿 ID 见 **§赋号表**（ELEMENT=`TALENT`，12/12 新号、0 复用）。类型 = `suggested_unsigned`。歧义仅叶级 `Q-MO-TALENT-nn`。未写 seed / 展示 catalog / DS-13～16。

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ 适用且文档闭合（口径草稿） | 十一招标叶子 + 流动 `.7.2` → **出卡**。正式草稿 ID 见 **§赋号表**（TEMP 对照）。**无** `cfg_metric-TALENT-seed.yaml`。**禁止**把草稿 `M_TALENT_*` 写入 seed。**禁止**消费展示 DS-13～16 OPEN（本批也没建）。 |
| #5 开放项 | ✅ 适用且已登记（本记录） | 页级语义债 TAL-B01…B12。展示人才态势 OPEN **本批未建**，不改挂为本页 Q。本叶不改 `客户决策清单跟踪表.md`、不升 🟢。 |
| PDR-05 自检 | ⏳ 有条件 | 无 TRACE/WF 第 6 列；本记录 + A2 `pages/TOPIC-TALENT-05.yaml` 可回指。门 1 完整闭合仍须正式 ID 会签（不发明）+ 公式会签 + 甲方 🟡。 |
| PDR-06 自检 | ⏳ 有条件 | 实现类草稿 = **third_party**（algo-catalog 人才 `default_hint`）。**禁止伪展开 COUNT / 加权公式**。维名 04≠05 显式挂 TAL-B03…B08。 |
| 语义 Owner（本工作流） | `human:淮政玮` | 口径 / 8 件套身份项 / 适用性 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop 不签公式、不改 seed `algorithm_type` |

**结论**：本页 **④ 适用（kit）**，**非整页 N/A**。筛选壳、报告面、重点人才识别前置、图谱基建无独立统计核、展示 DS-13～16、智库人才、综合 seq 184 → **N/A + 依据**（§3.13）。甲方 🟡 不阻断定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。

### §1.1 本页必须消费本核对记录

| 页 `page_id` | 中文 | ④ | 消费的 ID | 禁止 |
|--------------|------|----|-----------|------|
| `TOPIC-TALENT-05` | 专题人才分析（整包） | **kit** | **§赋号表** `M_TALENT_*` 草稿（TEMP 对照） | 挂展示 DS-13～16 OPEN；消费 `M_CHAIN_*` 人才形近 ID / `M_SVC_REC_*` / `M_ENT_ATTRACT_*` / `M_SYNTH_VIT_DIM_SCORE` / ZHIKU-TALENT-*；把草稿 ID 写入 seed；把本页 A=0 改成 missing |

**展示人才态势（A2.2 / DS-13～16）**：本叶 **不消费**。`DS13-16-TALENT-METRIC-OPEN-L01` **本批未建**；即使日后建成，核对记录 **不是**本页语义层（05.5 §5–7；给人说明 §8.4 甲「与展示 DS-13～16 **分叶，勿混**」）。同源 `.7.5` / `.7.9` 覆盖 **算在本专题叶 mapped**，展示侧不重开、本页不把展示包当看板。

### §1.2 05.5 十一招标叶子 × 差集

| 招标叶子 | 05.5 算法 | 标签 | 差集 | ④ |
|----------|-----------|------|------|----|
| 区域分布 | `.1` 基础指标 | M | mapped（TAL-D01） | kit |
| 机构分布 | `.1` | M | mapped（TAL-D02） | kit |
| 供给 | `.1` | M | mapped（TAL-D03） | kit |
| 关系链 | `.7.5` | **G1**（可与展示 DS-15 **同源**，不消费展示 OPEN） | mapped（TAL-D04） | kit |
| 深圳现状 | `.1` + `.7.4` 优劣势【算法补】 | M/G3 | mapped（TAL-D05） | kit |
| 学术力 | `.7.7` | M | mapped（TAL-D06） | kit |
| 产业力 | `.7.8` | M | mapped（TAL-D07） | kit |
| 引入推荐 | `.7.9` | **G3 Job**（可与展示 DS-16 **复用**，不消费展示 OPEN） | mapped（TAL-D08） | kit |
| 培育推荐 | `.7.10` | **G3 Job** | mapped（TAL-D09） | kit |
| 高校新培育 | `.7.3` | M | mapped（TAL-D10） | kit |
| 深圳供需 | `.7.6` | M | mapped（TAL-D11） | kit |

非十一招标、但 05 有叶：流动 `.7.2` → mapped（TAL-D13）+ ④ **kit**（有流入/流出/留存核）。重点人才识别 `.7.1` → mapped（TAL-D12）+ ④ **无独立招标页核**（§3.13）。

### §1.3 TRACE / A2 语义层指针（Round 17 才回写 catalog 正文）

本叶 **不改** `metrics/request/专题系统/A2-GAP-page-catalog.yaml` 与 pages yaml 正文。指针写入 `_work/open-loop/TOPIC-TALENT-METRIC-OPEN-L01-a2-patch.yaml`（**不**写共享 `METRIC-OPEN-LOOP-a2-patch.yaml`）。

| 层 | 路径 | 本叶要求的指针 |
|----|------|----------------|
| 核对记录 | **本文件** | `TOPIC-TALENT-05` 唯一 OPEN 真源 |
| A2 页 yaml | `metrics/request/专题系统/pages/TOPIC-TALENT-05.yaml` | 本 loop **不改** pages 正文。库缺口 `missing` 不动。仍 **禁止**把草稿 ID 写入 seed / 展示 DS-13～16 catalog。 |
| A2 catalog | `A2-GAP-page-catalog.yaml` 的 `TOPIC-TALENT-05` | 删「无 METRIC-OPEN → 只记语义欠账」中已被本叶覆盖的句（TAL-B01 文件级闭合） |
| TRACE / WF | **无**专题人才四件套 | `trace_metrics` / `wireframe_metric_ids` 保持空；不从 04 叙述发明 `M_*` |
| PACK | 无独立 `TOPIC-TALENT-PACK-L01` | SRS 04 + `05.5-人才.md` 顶 PACK；FDS **不顶** OPEN |

口径会签：`owner_semantic = human:淮政玮`；公式 / `algorithm_type` 共签仍 `human:唐绍祖`。展示 DS-13～16 **不升、不改挂、不混叶**。

---

## §2 模块消费矩阵（TEMP 对照 · 正式草稿见 §赋号表 · 禁 DS-13～16）

> 差集列维持 A2 已写 **mapped**（A=0）。本表只闭合语义层：落点 + 适用性 + 开放项。`algorithm_type` 列为 **草稿建议**，未会签。实现类草稿 = **third_party**，公式栏写「第三方不展开」，**禁止伪 COUNT / 伪加权**。  
> **`TEMP_*` 已升正式草稿 ID**：见 **§赋号表**。TEMP 仅对照。`algorithm_type` = `suggested_unsigned`。实现类草稿 = **third_party**，禁止伪 COUNT / 伪加权。**禁止**写入 `metrics/registry/` seed / 展示 catalog / 改挂 DS-13～16。

| temp_id | 招标叶子 / 主落点 | 适用 | 建议 type（未签） | pending |
|---------|-------------------|------|-------------------|---------|
| TEMP_TOPIC_TALENT_REGIONAL_DIST | 区域分布：地理数量/对比 | ✅ kit | STAT | 第三方不展开；禁 `M_CHAIN_REG_TALENT_STRUCTURE` / `M_CHAIN_SZ_TALENT` |
| TEMP_TOPIC_TALENT_ORG_DIST | 机构分布：前 N 机构集中度 | ✅ kit | STAT | 04 人才数排名 vs 05 区域机构数 → TAL-B03 |
| TEMP_TOPIC_TALENT_SUPPLY | 供给：历年曲线 + 存量结构 | ✅ kit | STAT | 04 职称/年龄 vs 05 学位毕业 → TAL-B04 |
| TEMP_TOPIC_TALENT_RELATION | 关系链：网络/路径/节点规模 | ✅ kit | GRAPH | G1；可与 DS-15 **同源**，**不消费**展示 OPEN；路径/画像无独立 ID → TAL-B11 |
| TEMP_TOPIC_TALENT_SZ_STATUS | 深圳现状：对比 + 优劣势 | ✅ kit | MIXED | 计数走 `.1`；短板走 `.7.4`；禁 `M_CHAIN_SZ_TALENT`；报告壳见 §3.13 |
| TEMP_TOPIC_TALENT_ACADEMIC_SCORE | 学术力指数 + 名单排名 | ✅ kit | MODEL | 04 H 指数等 vs 05 成果/影响力/技能 → TAL-B05；禁 `M_CHAIN_ACADEMIC_POWER` |
| TEMP_TOPIC_TALENT_INDUSTRY_SCORE | 产业力指数 + 排名 | ✅ kit | MODEL | 04 个人转化 vs 05 企业人才综合实力 → TAL-B06 |
| TEMP_TOPIC_TALENT_ATTRACT_SCORE | 引入推荐指数 + 名单规模 | ✅ kit | MODEL | G3 **Job**；可与 DS-16 **复用**，**不消费**展示 OPEN；分项 → TAL-B08；禁 `M_SVC_REC_*` |
| TEMP_TOPIC_TALENT_CULTIVATE_SCORE | 培育推荐指数 + 名单规模 | ✅ kit | MODEL | G3 **Job**；建议文本无 ID → TAL-B08 |
| TEMP_TOPIC_TALENT_UNIV_NEW | 高校新培育：新增/趋势 | ✅ kit | MODEL | 3–5 年预测/新兴/校企无专核 → TAL-B07 |
| TEMP_TOPIC_TALENT_SZ_SUPPLY_DEMAND | 深圳供需评价指数 | ✅ kit | MODEL | 禁止伪展开「供给−需求」；禁 `M_CHAIN_BOTTLENECK_TALENT` |
| TEMP_TOPIC_TALENT_FLOW | 流动：流入/流出/留存（非招标页） | ✅ kit | GRAPH | `.7.2` 关系+时间；**禁止轨迹引擎** → TAL-B10；04 未单列流动页，叶存在禁止 missing |

**12/12 TEMP_ 均 mapped + 本叶 present。** 不得因「口径未冻 / D1 missing / 无正式 M_* / 第三方不展开」把上表改成差集 `missing`。正式草稿 ID 只写 **§赋号表** / `id-assign/`，**禁止**写入 seed 或展示 DS-13～16 catalog。

---

## §赋号表（TEMP → 正式草稿 `M_*` · 类型未签）

> 本 loop：`METRIC-ID-ASSIGN-LOOP`。ELEMENT=`TALENT`。机器卡 `demands` 已换 `M_*`（保留 `temp_id`）。叶级卡：`metrics/request/_work/id-assign/TOPIC-TALENT-METRIC-OPEN-L01.yaml`。Q 仅 `…-questions.yaml`。  
> 撞号：TALENT 域 seed/矩阵 **0 条**；12 个拟号 `getMetric` 均 NOT_FOUND。形近 ENT 招引/培育、CHAIN 学术力/深圳人才维、SYNTH 活力维、SVC 关系密度 **不同口径不复用**。流动 `.7.2` 一并赋号。

| temp_id | metric_id | reuse | 中文名 | 建议 type（未签） | pending |
|---------|-----------|-------|--------|-------------------|---------|
| TEMP_TOPIC_TALENT_REGIONAL_DIST | M_TALENT_REGIONAL_DIST | — | 重点人才区域分布 | STAT | Q-MO-TALENT-10 |
| TEMP_TOPIC_TALENT_ORG_DIST | M_TALENT_ORG_DIST | — | 重点人才机构分布 | STAT | Q-MO-TALENT-01 |
| TEMP_TOPIC_TALENT_SUPPLY | M_TALENT_SUPPLY_STRUCT | — | 人才供给情况 | STAT | Q-MO-TALENT-02 |
| TEMP_TOPIC_TALENT_RELATION | M_TALENT_RELATION_NET | — | 重点人才关系链结构 | GRAPH | Q-MO-TALENT-08 |
| TEMP_TOPIC_TALENT_SZ_STATUS | M_TALENT_SZ_STATUS | — | 深圳人才现状与优劣势 | MIXED | Q-MO-TALENT-07 |
| TEMP_TOPIC_TALENT_ACADEMIC_SCORE | M_TALENT_ACADEMIC_SCORE | — | 人才学术力指数 | MODEL | Q-MO-TALENT-03 |
| TEMP_TOPIC_TALENT_INDUSTRY_SCORE | M_TALENT_INDUSTRY_SCORE | — | 人才产业力指数 | MODEL | Q-MO-TALENT-04 |
| TEMP_TOPIC_TALENT_ATTRACT_SCORE | M_TALENT_ATTRACT_SCORE | — | 引入人才推荐指数 | MODEL | Q-MO-TALENT-06 |
| TEMP_TOPIC_TALENT_CULTIVATE_SCORE | M_TALENT_CULTIVATE_SCORE | — | 培育人才推荐指数 | MODEL | Q-MO-TALENT-06 |
| TEMP_TOPIC_TALENT_UNIV_NEW | M_TALENT_UNIV_NEW | — | 高校新培育人才 | MODEL | Q-MO-TALENT-05 |
| TEMP_TOPIC_TALENT_SZ_SUPPLY_DEMAND | M_TALENT_SZ_SUPPLY_DEMAND | — | 深圳人才供需评价 | MODEL | Q-MO-TALENT-09 |
| TEMP_TOPIC_TALENT_FLOW | M_TALENT_FLOW_TRACK | — | 人才流动追踪 | GRAPH | — |

**12 赋号 / 0 复用 / 0 废弃 / 10 Q。** 类型分布：STAT 3 · MODEL 6 · GRAPH 2 · MIXED 1。全部 `suggested_unsigned`。未改挂 DS-13～16。

---

## §3 ④ 指标语义卡（按招标叶子 · 不写 seed）

身份项（temp_id / 中文名 / 口径）由淮政玮本工作流确认适用。公式 / 权重 / `algorithm_type` 一律 `pending_cosign: human:唐绍祖`。取值口径 = **第三方不展开**（对接人才库/论文库/专利库/招聘源）；**禁止**把 05 叙述改写成可落地加权公式或伪 COUNT。源表以 05.5「Java `/topic/v1/talent/**` 只读 ADS」+ A1 人才维 ODS 判定为准，**不**把项目 DWD 反推成 ODS `full`。人才存储域未建 → TAL-B09（数据缺口，不是算法库缺口）。

8 件套草稿字段：metric_id 以 **§赋号表** 为准（TEMP 对照）；源系统=科技专题服务系统·人才维；更新频率=未定；version=`draft-id-assign-20260822`；源表=ADS 专题人才（A1 表2 未交 → 本叶不填伪 full）；algorithm_type=§赋号表建议（未签）。

### §3.1 区域分布 · kit（Bid seq 84–85；05 `.1` / seq 98（1）（3））

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TALENT_REGIONAL_DIST | 重点人才区域分布 | 选定产业/技术领域下全国/全球人才地理分布及多领域并列对照 | **第三方不展开**；禁止伪 `COUNT GROUP BY region` | STAT |

筛选壳（自定义产业/领域）见 §3.13。地图可视化不进算法库。不消费 `M_CHAIN_REG_TALENT_STRUCTURE` / `M_CHAIN_SZ_TALENT`。

### §3.2 机构分布 · kit（Bid seq 86–87；05 `.1` / seq 98（2））

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TALENT_ORG_DIST | 重点人才机构分布 | 高校/院所/企业等类型下，特定产业或技术领域内人才最集中的前 N 家机构及其人才数量与占比 | **第三方不展开**；04 机构→人才数排名 vs 05「省/国家拥有的人才机构数」→ TAL-B03 | STAT |

类型勾选交互见 §3.13。叶已列 → mapped，不因口径差改 missing。不发明机构人才数/占比正式 `M_*`。

### §3.3 供给 · kit（Bid seq 88–89；05 `.1` / seq 98（4））

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TALENT_SUPPLY | 人才供给情况 | 特定领域人才供给历年变化 + 当前存量结构 | **第三方不展开**；05 为学士/硕士/博士历年毕业数量；04 学历/职称/年龄 → TAL-B04 | STAT |

禁止发明职称/年龄结构正式 `M_*`。领域过滤可走 seq 98（3），不另造 TEMP。

### §3.4 关系链 · kit（Bid seq 90–92；05 `.7.5` **G1** / seq 160）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TALENT_RELATION | 重点人才关系链结构 | 论文/专利/组织/项目多源融合后的合作、引用等多元关系网络；支撑最短路径与节点洞察 | **第三方不展开**；图指标未签。可视化拖拽缩放是呈现，不进 A 类 | GRAPH |

**G1 当前图（Nebula）。** 可与展示 DS-15 **同源**；覆盖算本专题叶；**禁止**把展示人才态势包 / DS-15 目录当本页 OPEN。路径/画像无独立 ID → TAL-B11。实体/关系基建见 §3.13。不发明路径类 `M_*`。

### §3.5 深圳现状 · kit（Bid seq 93–94；05 `.1` + `.7.4`【算法补】 / seq 159）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TALENT_SZ_STATUS | 深圳人才现状与优劣势 | 统一评价框架下深圳 vs 全国/重点城市横向对比；仪表盘/雷达展示所选产业或技术领域的优势与短板 | **第三方不展开**；禁止伪加权。计数可走 seq 98；对比/短板走 seq 159 | MIXED |

供需指数归 §3.11，不混用。简报导出见 §3.13。不得用 `M_CHAIN_SZ_TALENT` 顶替。

### §3.6 学术力 · kit（Bid seq 96–98；05 `.7.7` / seq 162）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TALENT_ACADEMIC_SCORE | 人才学术力指数 | 用户组合指标与权重后的学术力评分、排名与名单对比榜 | **第三方不展开**；禁止伪展开 H 指数公式。04 论文/被引/H 指数/期刊影响力/合作广度 vs 05 成果数量/学术影响力/专业技能 → TAL-B05 | MODEL |

参数配置壳见 §3.13。分项维 **无独立 ID**。不得用 `M_CHAIN_ACADEMIC_POWER`（链学术力）顶替。不消费综合活力「人才」维 `M_SYNTH_VIT_DIM_SCORE`。

### §3.7 产业力 · kit（Bid seq 99–100；05 `.7.8` / seq 163）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TALENT_INDUSTRY_SCORE | 人才产业力指数 | 特定产业领域内人才产业转化贡献的评分与排名 | **第三方不展开**；禁止伪展开转化率。04 专利转化/项目/商业化 vs 05 企业人才综合实力（影响力/产业覆盖/媒体知名度）→ TAL-B06 | MODEL |

叶名已对上 `.7.8` → mapped，不因口径差改 missing。禁止发明转化率正式 `M_*`。

### §3.8 引入推荐 · kit（Bid seq 101–102；05 `.7.9` **G3 Job** / seq 164）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TALENT_ATTRACT_SCORE | 引入人才推荐指数 | 全球库中与深圳产业发展方向契合的外部人才综合分；名单规模为同核 STAT 面（共 N 人），不另造 CNT ID | **第三方不展开**；05 学术力/产业力/产品匹配度/深圳连接度。分项无 ID → TAL-B08 | MODEL |

**Job，不是关系链 G1 图算。** 推荐理由/画像文本无独立 ID。展示 DS-16 可复用本叶，本页 **不算**展示包、**不消费**展示 OPEN。禁止 `M_SVC_REC_*`。

### §3.9 培育推荐 · kit（Bid seq 103–104；05 `.7.10` **G3 Job** / seq 165）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TALENT_CULTIVATE_SCORE | 培育人才推荐指数 | 高成长潜力人才综合分 + 建议名单规模；培育方向建议为文本，无独立 ID | **第三方不展开**；05 产业相关度/潜力/学术力/产业力。建议文本 → TAL-B08 | MODEL |

**Job。** 不消费 `M_SVC_REC_*`。不发明匹配度/潜力分项正式 `M_*`。

### §3.10 高校新培育 · kit（Bid seq 105–107；05 `.7.3` / seq 158）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TALENT_UNIV_NEW | 高校新培育人才 | 目标技术领域高校新增人才培养识别、培养趋势、学科/技术方向与校际对比 | **第三方不展开**。04 三句（3–5 年毕业生预测、新专业/研究中心、校企合作）05 未单列专核 → TAL-B07 | MODEL |

产品叶已对上 → mapped，不另开 A 类 missing，不发明预测/新兴/校企正式 `M_*`。

### §3.11 深圳供需 · kit（Bid seq 108；05 `.7.6` / seq 161）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TALENT_SZ_SUPPLY_DEMAND | 深圳人才供需评价 | 特定产业/技术领域深圳人才供需平衡（缺口或盈余）及趋势 | **第三方不展开**；**禁止**伪展开「供给−需求」。结构化报告见 §3.13 | MODEL |

不得用 `M_CHAIN_BOTTLENECK_TALENT` 顶替。与 §3.5 现状对比不混核。

### §3.12 流动 · kit（非招标页；05 `.7.2` / seq 157）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_TALENT_FLOW | 人才流动追踪 | 区域/行业人才流入、流出、留存的时间序列；用关系+时间属性，**禁止 GIS 轨迹引擎** | **第三方不展开**。04 二十六叶未单列流动页；seq 157 叶存在 → mapped，禁止因「不做轨迹」打 missing（TAL-B10） | GRAPH |

展示 DS-14 同样非轨迹引擎，属 A2.2，**本页不 missing、不消费展示 OPEN**。

### §3.13 ④ 不适用（N/A + 依据）

整页 N/A：**无**（十一招标叶子均有统计/指数；流动有流入流出留存核）。

| 宿主 | 项 | 差集判定 | N/A 依据 |
|------|----|----------|----------|
| 交互壳 | 分析维度筛选与权重配置（TAL-D16 / seq 84、86、97） | **`n/a_ops`** | 检索/筛选/权重壳不进算法库；区域/学术力计算仍走 TEMP_REGIONAL / TEMP_ACADEMIC。严禁用展示检索 OPEN 冒充。 |
| 报告面 | 现状简报与供需结构化报告（TAL-D17 / seq 95、109） | **`other_system`** | 系统报告面/导出。分析产出仍走 TEMP_SZ_STATUS / TEMP_SZ_SUPPLY_DEMAND。禁止把报告壳打成库 missing。 |
| 识别前置 | 重点人才识别（TAL-D12 / `.7.1` / seq 156） | mapped（差集）/ ④ **无独立招标页核** | 非十一招标页；服务区域/机构「重点人才」集合前置。04 未单列识别叶。不发明识别正式 `M_*`，也不另造 TEMP 进 seed。 |
| 图谱基建 | 人才实体识别 / 关系抽取（TAL-D14/D15；seq 110/111） | mapped（差集）/ ④ **无独立核** | 服务关系链 G1 与流动时间属性；04 无独立「实体识别」叶。不发明图谱统计 `M_*`。不把企业/科研图谱叶算进本页。 |
| 本叶范围外 | 展示系统科技人才态势 DS-13～16（TAL-D18） | **`other_system`** | A2.2 / 建议日后 `DS13-16-TALENT-METRIC-OPEN-L01`（**本批未建**）。05.5：展示页只引用同一 A 面。同源 `.7.5`/`.7.9` 已在 TEMP_RELATION / TEMP_ATTRACT。**严禁**混叶、严禁消费展示 OPEN / `06-功能-科技人才态势.md` / `科技人才态势-DS15/`。 |
| 本叶范围外 | 智库科技人才地图/库（TAL-D19） | **`other_system`** | 03 系统。禁止 ZHIKU-TALENT-* 改挂。 |
| 本叶范围外 | 综合 seq 184 区域产业创新人才 | **`other_system`** | SYNTH-VITALITY 输入 / SYNTH-REGION 索引。禁止 `M_SYNTH_VIT_DIM_SCORE` 当本页学术力/产业力。 |
| 本叶范围外 | `TOPIC-OPS` / `TOPIC-DATAREQ` | `n/a_ops` | 给人说明 §8.4：运营/需求面走 N/A，不算缺 OPEN 任务。 |
| 无独立核的分项 | 机构口径差、供给职称年龄、学术力分维、产业力转化率、高校预测/新兴/校企、招引/培育分项、路径画像、第三方不展开 | 语义债 TAL-B03…B12 | **禁止**发明正式 `M_*` 或把 TEMP_ 写入 seed |

---

## §4 ⑤ 开放项（已登记 · 不升 🟢）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| TAL-B01 | **本叶闭合文件级**：核对记录 present。A2 catalog 正文 Round 17 才改指针 | 语义欠账→有指针；非 A 类 missing |
| TAL-B02 | PDR-05/06 有条件；公式未签；第三方不展开 | ⏳ |
| TAL-B03 | 机构分布 04 人才数排名 vs 05 区域机构数 | 语义债 |
| TAL-B04 | 供给 04 职称年龄 vs 05 学位毕业数量 | 语义债 |
| TAL-B05 | 学术力 04 分项（H 指数等）无正式 ID | 语义债；禁止伪 H 指数公式 |
| TAL-B06 | 产业力 04 个人转化 vs 05 企业人才综合实力 | 语义债 |
| TAL-B07 | 高校新培育 预测/新兴/校企无专核 | 语义债；TAL-D10 保持 mapped |
| TAL-B08 | 引入/培育分项维与建议文本无正式 ID | 语义债；不消费 `M_SVC_REC_*` |
| TAL-B09 | 人才存储域未建 | 数据/存储缺口，不是 05 人才 13 叶缺失 |
| TAL-B10 | 流动禁止轨迹引擎 | 产品约束；TAL-D13 / TEMP_FLOW 保持 mapped |
| TAL-B11 | 关系路径与节点画像无独立 metric_id | 语义债 |
| TAL-B12 | 实现类第三方不展开 | 13 叶 mapped 不因第三方改 missing |
| DS-13～16 | **展示人才态势**（本批无 OPEN 叶） | 保持分叶；**本页不改挂、不关闭、不混入** |

未关闭任何甲方项。未改 `客户决策清单跟踪表.md`、未改共享 `METRIC-SEMANTIC-QUESTIONS.md`。口径歧义叶级 **`Q-MO-TALENT-01…10`**（🟡 内部默认）；TAL-B03…B12 仍作语义债对照。

---

## §5 贴源摘要（data-agent 协作 · 不改 registry）

| 层 | 结论 |
|----|------|
| 调用链 | 前端 → Java `/topic/v1/talent/**` → 只读 ADS。引入/培育 = Job；关系链 = A 面 G1（Nebula 当前图）；流动 = 关系+时间，禁止轨迹引擎。Java 不写 NLP / 不直连 nGQL。 |
| 准入 / ODS | 人才主数据走要素库/第三方；A1 人才维表2 未交 → 本叶 D3 不得伪 `full`。存储域未建 = TAL-B09，不是 A 类 missing。 |
| 算法库 05 | 基础指标 / 图谱×2 / 识别 / 流动 / 高校新培育 / 深圳优劣势 / 关系链 / 供需 / 学术力 / 产业力 / 招入 / 培育 — 能对上 → mapped。A1 双表未交 → `A1需规ID` 空。 |
| 本叶不做 | 不写 `cfg_metric-TALENT-seed.yaml`；`M_TALENT_*` **仅**赋号草稿（核对记录 / 机器卡 / `id-assign/`）；不消费展示/智库/综合/B 轨/企业招引培育形近 ID；不新建 `data-gap-catalog`。 |

---

## §6 UI / 评审挂载要求（给 V1 / 迁移叶）

- 凡统计数字：ⓘ MetricSpecCard。seed **仍无**本页 ID → 回指 **§赋号表草稿** + 本记录，**禁止**点开展示人才 / `M_CHAIN_*` / `M_ENT_ATTRACT_*` 伪 8 件套
- Wave 0：🧪 MockBadge
- 维名/权重未冻：⚠️「待甲方确认」（文案走 TAL-B*，不要写展示 DS-13～16 字样到专题 DOM）
- TEMP_ 未入 seed：D1 按 `missing`/`draft` 诚实；红问号或 draft ⓘ，**不显伪 8 件套**
- 关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / 就绪度字样
- 「页面要哪些指标」人才维 = `human:郭万迎`（对北京九新；李伟辅助抽清单，`JIUXIN-TECH-ORG-TALENT-L01`）。**功能实现 Owner 待指定**（给人说明文首）；STAT → GDF ADS + Java 聚合（Owner 待指定；郭万迎不对九新写 Java）；MODEL/GRAPH/Job 计算仍归唐绍祖监管 Python。实现类 **third_party** 禁止伪展开公式

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录 | `产品整体定义/科技专题服务系统-完整详细设计/METRIC-OPEN-TOPIC-TALENT-核对记录.md`（含 §赋号表） |
| 机器卡 | `metrics/request/_work/open-loop/TOPIC-TALENT-METRIC-OPEN-L01.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/TOPIC-TALENT-METRIC-OPEN-L01.yaml` |
| 叶级 Q | `metrics/request/_work/id-assign/TOPIC-TALENT-METRIC-OPEN-L01-questions.yaml` |
| A2 指针补丁（本叶） | `metrics/request/_work/open-loop/TOPIC-TALENT-METRIC-OPEN-L01-a2-patch.yaml`（本轮未改） |
| 薄 handoff | `agent-handoffs/算法库联调-ALGO-LIB/TOPIC-TALENT-METRIC-OPEN-L01.md` |
| **未改** | `metrics/registry/` seed / 矩阵；A2 catalog / 专题 pages 正文；展示 catalog / DS-13～16；`LOOP-state.yaml`；共享 QUESTIONS；其它 OPEN 叶 |

---

## §8 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _口径草稿已出；适用性：TOPIC-TALENT-05 **kit**；**赋号草稿** 12 条 `M_TALENT_*`（0 复用，类型未签）见 §赋号表；筛选壳 / 报告面 / 识别前置 / 图谱无独立核 / 展示 DS-13～16 / 智库 / 综合人才维 N/A 见 §3.13；**零混入** DS-13～16；**零**正式 ID 进 seed_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）；实现类 third_party 不展开_ | |
| 甲方 / 展示 DS-13～16 | — | 保持分叶；本批无展示人才 OPEN；不改挂本页 | |
