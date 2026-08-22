# METRIC-OPEN-TOPIC-ENT-核对记录

> **任务**：TOPIC-ENT-METRIC-OPEN-L01（METRIC-OPEN-LOOP Round 2）  
> **角色**：product-agent（口径草稿）+ algorithm-agent / data-agent（协作核对，本叶不改 seed）  
> **监管人**：`human:淮政玮`  
> **日期**：2026-08-22  
> **上游**：无独立四件套 / PACK-L01；本工作流书面 **SRS 04 + 05.3 顶 PACK**（给人说明 §8.4 甲）  
> **范围**：专题企业分析 **一整包** `page_id=TOPIC-ENT-05` 的 ④ 指标语义卡 + ⑤ 开放项。覆盖 05.3 **十招标叶子**里进算法差集的那些。不替甲方拍板；公式 / `algorithm_type` **不签**，标 `pending_cosign: human:唐绍祖`（8/25 前不派唐绍祖开工本 loop）。
>
> **Wave A 赋号（2026-08-22）**：12 条 `TEMP_*` 已升正式 `M_*` 或同口径逐条 reuse，见 **§9 赋号表**。非整页改挂展示 60 个 ID。`algorithm_type` 仅建议、未签。

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ 适用且文档闭合（口径草稿） | 十招标叶子均有统计 / 指数 / 名单规模 → **出卡**。05.3 与 SRS 04 **未挂**任何 `metric_id` → 卡面只用 **`TEMP_TOPIC_ENT_*`**。**禁止**消费 `cfg_metric-ENT-seed` 的 60 个 `M_ENT_*`；**禁止**发明正式 `M_*` 写入 seed。 |
| #5 开放项 | ✅ 适用且已登记（本记录） | 页级语义债 ENT-B03…B12。展示侧 Q010～Q019 **不改挂**为本页 Q。本叶不改 `客户决策清单跟踪表.md`、不升 🟢。 |
| PDR-05 自检 | ⏳ 有条件 | 无 TRACE/WF 第 6 列；本记录 + A2 `pages/TOPIC-ENT-05.yaml` 可回指。门 1 完整闭合仍须正式 ID 会签（不发明）+ 公式会签 + 甲方 🟡。 |
| PDR-06 自检 | ⏳ 有条件 | COUNT 类可写演示公式；MODEL/GRAPH 公式 `pending_cosign`。维名 04≠05 显式挂 ENT-B04…B11。 |
| 语义 Owner（本工作流） | `human:淮政玮` | 口径 / 8 件套身份项 / 适用性 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop 不签公式、不改 seed `algorithm_type` |

**结论**：本页 **④ 适用（kit）**，**非整页 N/A**。历程 CMS、筛选壳、运营/需求面、展示企业门户、图谱基建无独立统计核 → **N/A + 依据**（§3.11）。甲方 🟡 不阻断定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。

### §1.1 本页必须消费本核对记录

| 页 `page_id` | 中文 | ④ | 消费的 ID | 禁止 |
|--------------|------|----|-----------|------|
| `TOPIC-ENT-05` | 专题企业分析（整包） | **kit** | 仅 `TEMP_TOPIC_ENT_*`（§2） | 挂展示 `ENT-MOD-*-METRIC-OPEN`；消费 60 个 `M_ENT_*`；用 `M_CHAIN_*` / `M_SVC_REC_*` 顶替；把本页 A=0 改成 missing |

**展示企业（A2.2）**：本叶 **不消费**。KEYPANO / SEARCH / EVAL / SHENZHEN / RECRUIT / RISK / E32 / STAR / OPS 核对记录 **不是**本页语义层（05.3 §7；给人说明 §8.4 甲「禁止挂展示 ENT-MOD-*-METRIC-OPEN」）。

### §1.2 05.3 十招标叶子 × 差集

| 招标叶子 | 05.3 算法 | 标签 | 差集 | ④ |
|----------|-----------|------|------|----|
| 类型 | `.1.3` 基础指标 | M | mapped（ENT-D01；地理 ENT-D02） | kit |
| 领域分布 | `.1.3` | M | mapped（ENT-D03） | kit |
| 技术力 | `.5.5` | M/G3 | mapped（ENT-D04） | kit |
| 商业力 | `.5.6` | M/G3 | mapped（ENT-D05） | kit |
| 深圳现状 | `.1.3` + `.5.1` 对标 | M | mapped（ENT-D06 / D07） | kit |
| 招引推荐 | `.5.7` | **G3 Job** | mapped（ENT-D08） | kit |
| 培育推荐 | `.5.8` | **G3 Job** | mapped（ENT-D09） | kit |
| 供应链 | `.5.4` | **G1/G2 · A 面**（CUT-D6，不进 B 面） | mapped（ENT-D10） | kit |
| 痛难点 | `.5.3` | **G3 Job** | mapped（ENT-D11） | kit |
| 竞争力 | `.5.1` | M/G3 | mapped（ENT-D12） | kit |

历程 **不是**十招标叶子：`.5.2` = **CMS** → `n/a_ops`（ENT-D15；05 seq 142 叶存在禁止 missing）。

### §1.3 TRACE / A2 语义层指针（Round 17 才回写 catalog 正文）

本叶 **不改** `metrics/request/专题系统/A2-GAP-page-catalog.yaml` 与 pages yaml 正文。指针先写入 `_work/METRIC-OPEN-LOOP-a2-patch.yaml`。

| 层 | 路径 | 本叶要求的指针 |
|----|------|----------------|
| 核对记录 | **本文件** | `TOPIC-ENT-05` 唯一 OPEN 真源 |
| A2 页 yaml | `metrics/request/专题系统/pages/TOPIC-ENT-05.yaml` | 应收口：`metric_open_status: present`；`metric_open_path` = 本文件；`metric_open_task: TOPIC-ENT-METRIC-OPEN-L01`。**库缺口 `missing` 不动**（本页 A 类本就为空）。仍 **禁止** `M_ENT_*`。 |
| A2 catalog | `A2-GAP-page-catalog.yaml` 的 `TOPIC-ENT-05` | 删「无 METRIC-OPEN → 只记语义欠账」中已被本叶覆盖的句（ENT-B01 文件级闭合） |
| TRACE / WF | **无**专题企业四件套 | `trace_metrics` / `wireframe_metric_ids` 保持空；不从 04 叙述发明 `M_*` |
| PACK | 无独立 `TOPIC-ENT-PACK-L01` | SRS 04 + `05.3-企业.md` 顶 PACK；FDS **不顶** OPEN |

口径会签：`owner_semantic = human:淮政玮`；公式 / `algorithm_type` 共签仍 `human:唐绍祖`。展示 Q010～Q019 **不升**、不改挂。

---

## §2 模块消费矩阵（TEMP_ 草稿 · 禁止 M_ENT_*）

> 差集列维持 A2 已写 **mapped**（A=0）。本表只闭合语义层：落点 + 适用性 + 开放项。`algorithm_type` 列为 **草稿建议**，未会签。  
> **`TEMP_*` ≠ 正式 `M_*`**：只存在于本核对记录与机器卡；**禁止**写入 `metrics/registry/` seed。

| temp_id | 招标叶子 / 主落点 | 适用 | 建议 type（未签） | pending |
|---------|-------------------|------|-------------------|---------|
| TEMP_TOPIC_ENT_TYPE_DIST | 类型：数量/占比/趋势 | ✅ kit | STAT | 类型字典≠展示 Q010；不消费 `M_ENT_TYPE_*` |
| TEMP_TOPIC_ENT_REGIONAL_COUNT | 类型/基础指标：全国→城市数量·规模·占比 | ✅ kit | STAT | 三级地图是产品呈现；不消费 `M_ENT_REGIONAL_*` |
| TEMP_TOPIC_ENT_DOMAIN_DIST | 领域分布 | ✅ kit | STAT | 深度/多元化无核 → ENT-B03 |
| TEMP_TOPIC_ENT_TECH_SCORE | 技术力指数 | ✅ kit | MODEL | 04 指标库 vs 05 五维 → ENT-B04 |
| TEMP_TOPIC_ENT_BIZ_SCORE | 商业力指数 | ✅ kit | MODEL | 04 vs 05 六维 → ENT-B05 |
| TEMP_TOPIC_ENT_SZ_LIST | 深圳现状：本地清单 + 链中角色标注 | ✅ kit | STAT | 角色依赖关系抽取；不消费 `M_ENT_SZ_*` / `M_CHAIN_SZ_ENTERPRISE*` |
| TEMP_TOPIC_ENT_CITY_COMPARE | 深圳现状：多城市横向对标 | ✅ kit | MIXED | 04 北上苏 vs 05 全国 → ENT-B06 |
| TEMP_TOPIC_ENT_ATTRACT_SCORE | 招引推荐指数 + 名单规模 | ✅ kit | MODEL | G3 **Job**；04/05 三维名 → ENT-B07；禁 `M_SVC_REC_*` |
| TEMP_TOPIC_ENT_CULTIVATE_SCORE | 培育推荐指数 + 名单规模 | ✅ kit | MODEL | G3 **Job**；ENT-B08 |
| TEMP_TOPIC_ENT_SUPPLY_STRUCT | 供应链结构（供应商数 / 中心性 / 密度） | ✅ kit | GRAPH | **A 面 G1/G2**，不进 B 面；备份方案无核 → ENT-B09 |
| TEMP_TOPIC_ENT_PAINPOINT | 痛难点诊断 / 瓶颈清单 | ✅ kit | MODEL | G3 **Job**；ENT-B10 |
| TEMP_TOPIC_ENT_COMPETITIVENESS | 综合竞争力指数 | ✅ kit | MODEL | 自选框架无核 → ENT-B11；禁 `M_CHAIN_COMPETITIVENESS_*` / `M_CHAIN_ENTERPRISE_POWER` |

**12/12 TEMP_ 均 mapped + 本叶 present。** 不得因「口径未冻 / D1 missing / 无正式 M_*」把上表改成差集 `missing`。不得把上表改写成 `M_ENT_*`。

---

## §3 ④ 指标语义卡（按招标叶子 · 不写 seed）

身份项（temp_id / 中文名 / 口径）由淮政玮本工作流确认适用。公式 / 权重 / `algorithm_type` 一律 `pending_cosign: human:唐绍祖`。源表以 05.3「Java `/topic/v1/enterprise/**` 只读 ADS」+ A1 企业维 ODS 判定为准，**不**把项目 DWD 反推成 ODS `full`。

8 件套草稿字段（TEMP_ 共同）：metric_id=下表 temp_id；源系统=科技专题服务系统·企业维；更新频率=未定；version=`draft-open-r2`；源表=ADS 专题企业（A1 表2 未交 → 本叶不填伪 full）。

### §3.1 类型 · kit（Bid seq 40；05 `.1.3` / seq 97（1）（2））

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ENT_TYPE_DIST | 重点企业类型分布 | 选定产业下，外企/高企/小微/上市等类型的企业去重数量、占比与环比。筛选壳本身见 §3.5 | `COUNT(DISTINCT ent_id) GROUP BY type_tag`；占比=类型数/当期集合 | STAT |
| TEMP_TOPIC_ENT_REGIONAL_COUNT | 区域企业数量规模占比 | 全国到城市下钻的企业数量、规模及占比（seq 41）。地图可视化不进算法库 | `COUNT/SUM GROUP BY region_level` | STAT |

阈值「何为重点企业」未冻 → 不发明提取核 ID；seq 97（5）新增可支撑趋势，04 无独立新增叶 → ENT-B12，**不新造 TEMP_ NEW**。

### §3.2 领域分布 · kit（Bid seq 42；05 `.1.3` / seq 97（3））

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ENT_DOMAIN_DIST | 企业领域分布 | 年报/专利/产品映射至产业或技术领域后的领域指标与增长率 | `COUNT(ent) GROUP BY field_id`；增长率未签 | STAT |

「各领域参与深度 / 多元化」无独立核 → ENT-B03。禁止发明 `TEMP_…_DEPTH` 正式化进 seed。

### §3.3 技术力 · kit（Bid seq 43–44；05 `.5.5` / seq 145）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ENT_TECH_SCORE | 企业技术力指数 | 用户组合赋权后的技术力 0–100（或 05 五维加权指数）；支撑两家雷达/排名/差距 | 演示：Σ 维归一×权重；04 专利/引用/研发人员/核心技术覆盖 vs 05 人才/创新/转化/合作/投入 → ENT-B04 | MODEL |

分项维 **无独立 ID**。对比交互是产品，模型叶已覆盖。不消费 `M_ENT_TECH_POWER_SCORE` / Q014。

### §3.4 商业力 · kit（Bid seq 45–46；05 `.5.6` / seq 146）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ENT_BIZ_SCORE | 企业商业力指数 | 商业力综合评分、排名与分维/行业对比 | 演示：Σ 维归一×权重；04 营收/利润率/客户集中/品牌声量 vs 05 市场/产品/品牌/技术合作/链覆盖/关键环节 → ENT-B05 | MODEL |

不消费 `M_ENT_BUSINESS_POWER_SCORE` / `M_ENT_MARKET_SHARE` / Q019。

### §3.5 深圳现状 · kit（Bid seq 47–48；05 `.1.3` + `.5.1`）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ENT_SZ_LIST | 深圳企业清单与链中角色 | 选定产业链下深圳相关企业去重清单；链中角色依赖关系抽取（ENT-D14），不另造定位 ID | `COUNT/LIST WHERE city=深圳 AND field∈chain` | STAT |
| TEMP_TOPIC_ENT_CITY_COMPARE | 多城市企业群对标值 | 深圳 vs 对照城市（04：北京/上海/苏州；05 seq 141：全国加权）的平均技术力、商业力、企业密度等 | 演示：城市聚合后再比；密度无独立核 → ENT-B06 | MIXED |

不消费 `M_ENT_CITY_*` / `M_ENT_SZ_CHAIN_POSITION` / Q016。不得用产业链 B 轨 `M_CHAIN_SZ_ENTERPRISE*` 顶替。

### §3.6 招引推荐 · kit（Bid seq 49–50；05 `.5.7` **G3 Job** / seq 147）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ENT_ATTRACT_SCORE | 招引推荐指数 | 全国库中与深圳重点产业契合的外部目标企业综合分；名单规模为同核 STAT 面（共 N 家），不另造 CNT ID | 演示 `Σ(维×权重)`；04 技术匹配/成长性/区域适配 vs 05 产业相关/政策匹配/深圳连接 → ENT-B07 | MODEL |

**Job，不是供应链 A 面图算。** 推荐理由/合作价值文本无独立 ID。禁止 `M_ENT_ATTRACT_*` / `M_SVC_REC_*`。

### §3.7 培育推荐 · kit（Bid seq 51–52；05 `.5.8` **G3 Job** / seq 148）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ENT_CULTIVATE_SCORE | 培育推荐指数 | 深圳本地高潜力企业综合分 + 建议名单规模；「一企一策」支持标注为文本，无独立 ID | 演示 `Σ(维×权重)`；04 技术壁垒/市场增速/团队背景 vs 05 产业相关/政策匹配/企业潜力 → ENT-B08 | MODEL |

**Job。** 不消费 `M_ENT_CULTIVATE_*`。

### §3.8 供应链 · kit（Bid seq 53–54；05 `.5.4` **A 面 G1/G2** / seq 144）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ENT_SUPPLY_STRUCT | 供应链结构指标 | 多级供应商/客户网络上的供应商数量、距离/稳定性、密度/紧密度、中心性；支撑断链风险标注 | 图指标未签；N&lt;2 不计算密度。**不进 B 面**（CUT-D6） | GRAPH |

实体识别 / 关系抽取（seq 108/109）是本叶基建，**无独立统计核** → §3.9。备份方案为决策文本 → ENT-B09。不消费 `M_ENT_SUPPLY_CHAIN_RISK` / `M_CHAIN_KEY_NODE_COUNT`。图：企业–环节–政策 **当前图**（Nebula）。

### §3.9 痛难点 · kit（Bid seq 55–56；05 `.5.3` **G3 Job** / seq 143）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ENT_PAINPOINT | 发展痛难点诊断 | 问题/瓶颈清单及建议报告（问题描述、成因、实践、方案） | 模型未签；04 研发/市场/融资/管理 vs 05 经营/盈利/效率/人才 → ENT-B10 | MODEL |

**Job。** 不消费 `M_ENT_PAINPOINT_*` / Q018。

### §3.10 竞争力 · kit（Bid seq 57–58；05 `.5.1` / seq 141）

| temp_id | 中文名 | 口径（适用性已认） | 公式（未签） | 建议 type |
|---------|--------|--------------------|--------------|-----------|
| TEMP_TOPIC_ENT_COMPETITIVENESS | 综合竞争力指数 | 多维赋权后的综合得分、雷达、排名与短板；05 固定规模/财务/人力/市场并与全国对比 | 演示加权综合；用户自选框架无核 → ENT-B11 | MODEL |

不得用 `M_CHAIN_COMPETITIVENESS_INDEX` / `M_CHAIN_ENTERPRISE_POWER` 顶替。不消费 `M_ENT_COMPETITIVENESS_*`。

### §3.11 ④ 不适用（N/A + 依据）

整页 N/A：**无**（十招标叶子均有统计/指数）。

| 宿主 | 项 | 差集判定 | N/A 依据 |
|------|----|----------|----------|
| 历程 `.5.2` | 企业发展历程时间线（ENT-D15 / TOPIC-ENT-015 / seq 142） | **`n/a_ops`** | 05.3 明文 CMS。04 十功能未单列历程。CMS/内容时间线 **不进算法差集主清单**。seq 142 叶存在 → **禁止 missing**，也不把 CMS 改判 mapped。不消费 `M_ENT_DEV_HISTORY`。 |
| 交互壳 | 产业与企业类型筛选 / 列表检索（ENT-D16 / seq 40 勾选） | **`n/a_ops`** | 检索/筛选壳不进算法库；类型分布计算仍走 TEMP_TYPE_DIST。严禁用展示 E1 SEARCH OPEN 冒充。 |
| 图谱基建 | 企业实体识别 / 关系抽取（ENT-D13/D14；seq 108/109） | mapped（差集）/ ④ **无独立核** | 服务供应链 A 面与企业–环节–政策当前图；04 无独立「实体识别」叶。不发明图谱统计 `M_*`。股权/社交全景切面按 05.3 §7 **不做**，不因此打 missing。 |
| 本叶范围外 | 展示系统企业门户 E1 / E-20～E-35（ENT-D17） | **`other_system`** | A2.2 / DS-ALGO-GAP。**禁止**消费 KEYPANO / SEARCH / EVAL / SHENZHEN / RECRUIT / RISK / E32 / STAR / OPS 核对记录与全部 `M_ENT_*`。 |
| 本叶范围外 | `TOPIC-OPS` / `TOPIC-DATAREQ` | `n/a_ops` | 给人说明 §8.4：运营/需求面走 N/A，不算缺 OPEN 任务。 |
| 无独立核的分项 | 领域深度/多元化、技术力/商业力分维、城市密度、招引/培育分项、断链备份方案、痛难点分维、竞争力自选框架、新增企业、资讯 CMS 喂数 | 语义债 ENT-B03…B12 | **禁止**发明正式 `M_*` 或把 TEMP_ 写入 seed |

---

## §4 ⑤ 开放项（已登记 · 不升 🟢）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| ENT-B01 | **本叶闭合文件级**：核对记录 present。A2 catalog 正文 Round 17 才改指针 | 语义欠账→有指针；非 A 类 missing |
| ENT-B02 | PDR-05/06 有条件；公式未签 | ⏳ |
| ENT-B03 | 领域深度/多元化无核 | 语义债 |
| ENT-B04 | 技术力 04 vs 05 维名 | 语义债；不消费 Q014 |
| ENT-B05 | 商业力 04 vs 05 维名 | 语义债 |
| ENT-B06 | 对标城市集合与密度 | 语义债；不消费 Q016 |
| ENT-B07 | 招引三维名称 | 语义债；不消费 Q015 |
| ENT-B08 | 培育三维名称 | 语义债 |
| ENT-B09 | 断链备份方案无核 | 语义债；不消费 Q017 |
| ENT-B10 | 痛难点诊断维 | 语义债；不消费 Q018 |
| ENT-B11 | 竞争力自选框架 | 语义债 |
| ENT-B12 | 资讯/新增未单列 | 语义债 |
| Q010～Q019 | **展示企业**口径族（wireframe E-21 等 / `M_ENT_*`） | 🟡 保持；**本页不改挂、不关闭** |

未关闭任何甲方项。未改 `客户决策清单跟踪表.md`。专题企业口径债 **尚未**单列 `Q-TOPIC-ENT-*`（避免与展示 Q 撞号）；本记录 + A2 `semantic_debt` 为真源。

---

## §5 贴源摘要（data-agent 协作 · 不改 registry）

| 层 | 结论 |
|----|------|
| 调用链 | 前端 → Java `/topic/v1/enterprise/**` → 只读 ADS。推荐/痛难点 = Job；供应链 = A 面 G1/G2（Nebula 当前图）。Java 不写 NLP / 不直连 nGQL。 |
| 准入 / ODS | 企业主数据走要素库；A1 企业维 11 叶表2 未交 → 本叶 D3 不得伪 `full`。展示 Q010 类型字典 **不**自动当作专题类型核。 |
| 算法库 05 | 基础指标 / 图谱×2 / 竞争力 / 历程 CMS / 痛难点 / 供应链 / 技术力 / 商业力 / 招引 / 培育 — 能对上 → mapped。A1 双表未交 → `A1需规ID` 空。 |
| 本叶不做 | 不写 `cfg_metric-ENT-seed.yaml`；不把 60 个 `M_ENT_*` 改挂；不新建 `data-gap-catalog`（文案真源仍 A2 `semantic_debt` + 本 §4）。 |

---

## §6 UI / 评审挂载要求（给 V1 / 迁移叶）

- 凡统计数字：ⓘ MetricSpecCard。seed **无**本页正式 ID → 回指 **本记录 TEMP_**，**禁止**点开展示 `M_ENT_*` 伪 8 件套
- Wave 0：🧪 MockBadge
- 维名/权重未冻：⚠️「待甲方确认」（文案走 ENT-B*，不要写展示 Q010 字样到专题 DOM）
- TEMP_ 未入 seed：D1 按 `missing`/`draft` 诚实；红问号或 draft ⓘ，**不显伪 8 件套**
- 关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / 就绪度字样
- 功能实现 Owner = `human:徐滕强`（专题企业）；STAT → GDF ADS + Java 聚合；MODEL/GRAPH/Job 计算仍归唐绍祖监管 Python（给人说明 §2.3）

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录 | `产品整体定义/科技专题服务系统-完整详细设计/METRIC-OPEN-TOPIC-ENT-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/TOPIC-ENT-METRIC-OPEN-L01.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/TOPIC-ENT-METRIC-OPEN-L01.yaml` |
| 赋号 Question | `metrics/request/_work/id-assign/TOPIC-ENT-METRIC-OPEN-L01-questions.yaml` |
| A2 指针补丁 | `metrics/request/_work/METRIC-OPEN-LOOP-a2-patch.yaml`（`TOPIC-ENT-05` present 一条） |
| 薄 handoff | `agent-handoffs/算法库联调-ALGO-LIB/TOPIC-ENT-METRIC-OPEN-L01.md` |
| **未改** | `metrics/registry/` seed / 矩阵；A2 catalog 正文（Round 17）；Round 1 SVCCHAIN 产物；共享 QUESTIONS.md / LOOP-state |

---

## §8 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _口径草稿已出；适用性：TOPIC-ENT-05 **kit**；历程 CMS / 筛选壳 / 展示门户 / 图谱无独立核 N/A 见 §3.11；OPEN 阶段零消费 `M_ENT_*`；Wave A 见下行_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）_ | |
| 甲方展示 Q010…Q019 | — | 保持 🟡；不改挂本页 | |
| Wave A 赋号 | 淮政玮（本会话 product-agent 代拟） | 12/12 已赋号；reuse 5；新号 7；Q-MO-ENT-01…10 均 🟡；类型未签 | 2026-08-22 |

---

## §9 赋号表（METRIC-ID-ASSIGN Wave A）

> `TEMP_*` 不是终态。同口径 reuse 展示 `M_ENT_*` 并 `also_in` 本页；不同口径 `VARIANT=TOPIC`。  
> `algorithm_type` = **建议未签**（`suggested_unsigned`）。不写 seed。撞号走 `metric-registry-lib`（本会话 MCP 未挂）。

| temp_id | metric_id | reuse | 建议类型 | Q |
|---------|-----------|-------|----------|---|
| TEMP_TOPIC_ENT_TYPE_DIST | M_ENT_TYPE_DIST_TOPIC | — | STAT | Q-MO-ENT-01 |
| TEMP_TOPIC_ENT_REGIONAL_COUNT | M_ENT_REGIONAL_COUNT_TOPIC | — | STAT | Q-MO-ENT-02 |
| TEMP_TOPIC_ENT_DOMAIN_DIST | M_ENT_DOMAIN_DIST_TOPIC | — | STAT | — |
| TEMP_TOPIC_ENT_TECH_SCORE | M_ENT_TECH_POWER_SCORE | reuse | MODEL | Q-MO-ENT-03 |
| TEMP_TOPIC_ENT_BIZ_SCORE | M_ENT_BUSINESS_POWER_SCORE | reuse | MODEL | Q-MO-ENT-04 |
| TEMP_TOPIC_ENT_SZ_LIST | M_ENT_SZ_LIST_TOPIC | — | STAT | Q-MO-ENT-05 |
| TEMP_TOPIC_ENT_CITY_COMPARE | M_ENT_CITY_COMPARE_TOPIC | — | MIXED | Q-MO-ENT-06 |
| TEMP_TOPIC_ENT_ATTRACT_SCORE | M_ENT_ATTRACTION_INDEX | reuse | MODEL | Q-MO-ENT-07 |
| TEMP_TOPIC_ENT_CULTIVATE_SCORE | M_ENT_CULTIVATION_INDEX | reuse | MODEL | Q-MO-ENT-08 |
| TEMP_TOPIC_ENT_SUPPLY_STRUCT | M_ENT_SUPPLY_STRUCT_TOPIC | — | GRAPH | — |
| TEMP_TOPIC_ENT_PAINPOINT | M_ENT_PAINPOINT_TOPIC | — | MODEL | Q-MO-ENT-09 |
| TEMP_TOPIC_ENT_COMPETITIVENESS | M_ENT_COMPETITIVENESS_SCORE | reuse | MODEL | Q-MO-ENT-10 |

**计数**：12 赋号 / 0 废弃；reuse **5**；新号 **7**；Q **10**（全 🟡）。  
建议类型：STAT 4 · MODEL 6 · MIXED 1 · GRAPH 1。

**reuse 5 条（also_in `TOPIC-ENT-05`，非整页改挂）**：`M_ENT_TECH_POWER_SCORE` / `M_ENT_BUSINESS_POWER_SCORE` / `M_ENT_ATTRACTION_INDEX` / `M_ENT_CULTIVATION_INDEX` / `M_ENT_COMPETITIVENESS_SCORE`。依据：05.3 维名与 seed 定义逐条相同（policy §3.4）。不 reuse demo 快路径 `M_ENT_ATTRACT_SCORE` / `M_ENT_CULTIVATE_SCORE`。

**不 reuse 的形近号**：`M_ENT_TYPE_*` / `M_ENT_REGIONAL_*` / `M_ENT_DOMAIN_COVERAGE_*` / `M_ENT_SZ_COUNT` / `M_ENT_CITY_*` / `M_ENT_SUPPLIER_COUNT` / `M_ENT_PAINPOINT_COUNT` / 全部 `M_CHAIN_*` / `M_SVC_REC_*`。

**Q 默认（内部，待甲方）**：类型=招标四类；区域规模=营收合计；技术力/商业力/招引/培育/竞争力跟 05.3；深圳=总部在深圳；对标=全国加权；痛难点=05 经营/盈利/效率/人才。不改挂 Q010～Q019。
