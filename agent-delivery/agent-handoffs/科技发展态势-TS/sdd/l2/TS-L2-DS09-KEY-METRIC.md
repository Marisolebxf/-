# TS-L2-DS09-KEY-METRIC · 重点领域规划 · 后台指标设计

> **任务**：`TS-L2-DS09-KEY-METRIC`（definition，不写业务代码、不改 metrics seed、不发明 `M_*`）
> **日期**：2026-11-06 · **作者**：agent:zcode 会话代跑 algorithm-agent · **监管**：`human:王梓真`
> **状态**：草案待会签（architect / api / algorithm / data，意见落 `sdd/l2/会签/重点领域规划-会签.md`）
> **公式与 `algorithm_type` 一律 `pending_cosign: human:唐绍祖`，本分册不签**

**输入真源**

| 用途 | 真源 |
|---|---|
| 指标唯一真源（本分册一切口径逐字抄录自此） | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-09-科技发展规划-核对记录.md`（§赋号表 4 条 KEYD TEMP→`M_INNOV_KEYD_*`、§2 消费矩阵、§3.3 KEY-DOMAIN 页语义卡与「本页 ④ 不适用」、§4 开放项 KEYD-B01..B03） |
| 硬依赖架构稿 | `agent-handoffs/科技发展态势-TS/sdd/l2/TS-L2-DS09-KEY-ARCH.md`（D18 逐叶判定 9 表 61 行、§5 差异收口、§7.1/§7.2 U8 裁定建议、§7.3 撞号禁令） |
| 契约草案（批 4 未冻结） | `agent-handoffs/科技发展态势-TS/API-TS-M9.md` §3.7 `key-areas`（`metric_id` 字位：`clusters[].metric_id` + `data.metric_ids[]`；五维 / `land_benefit` 定名 U8） |
| 需规 6 叶 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技发展规划.md` seq 185–190（L110–L199；六叶 bid_desc 均空、沿用 excel_row 181 继承句） |

**范围**：DS-09 `DS-09-KEY-DOMAIN` 页（重点领域规划页签 Tab2，FE-TS-09b）6 叶（seq 185–190）的后台指标设计：逐叶判定表、4 条 `M_INNOV_KEYD_*` 明细卡、撞号禁令专节、U8 未决与角标、190 建议壳纪律、纪律声明。COMPREHENSIVE 5 条 `M_INNOV_PLAN_*`（OV-METRIC 分册）与 RESEARCH 4 条 `M_INNOV_RES_*`（RES 分册）不在本分册展开，仅在 §3 撞号禁令整表收口。**口径一律逐字抄录核对记录，不改写语义。**

---

## 1. 逐叶指标判定表（6 叶）

### 1.1 总表

| seq | 叶 | metric_id（草稿） | 中文名 | 公式状态 | algorithm_type 建议（未签） | D1 | D3 | D4 | UI 角标要求 |
|---|---|---|---|---|---|---|---|---|---|
| 185 | 区域科技创新空间布局分析 | `M_INNOV_KEYD_SPATIAL` | 空间密度与集聚度 | 未签（`pending_cosign: human:唐绍祖`；GIS + ADS 图层读数，不伪展开） | STAT | draft（未入 seed） | 不伪 full | D18 表读数 = mock | 🧪 MockBadge + 统计数 ⓘ draft 语义卡 + ⚠️「待甲方确认」（类型未签；真算密度/集聚度待 GIS 图层真源，V1 为集聚归属演示） |
| 186 | 竞争力水平与潜力评估 | `M_INNOV_KEYD_COMPETITIVENESS` / `M_INNOV_KEYD_POTENTIAL` | 区域科技创新竞争力水平 / 区域科技创新发展潜力 | 未签（`pending_cosign: human:唐绍祖`；「演示：随 186；权重未签」） | MIXED / MIXED | draft（未入 seed） | 不伪 full | D18 表读数 = mock | 🧪 + 统计数 ⓘ draft 语义卡 + ⚠️「待甲方确认」（维名/权重未冻 U8-1，文案走 KEYD-B02/B03；Q-MO-DS09-04） |
| 187 | 土地用途与效益分析 | `M_INNOV_KEYD_LAND` | 土地创新产出效益与利用效率 | 未签（`pending_cosign: human:唐绍祖`；GIS + ADS 读数） | STAT | draft（未入 seed） | 不伪 full | D18 表读数 = mock | 🧪 + 统计数 ⓘ draft 语义卡 + ⚠️「待甲方确认」（亩均/容积率正式值待数据侧，U8-2） |
| 188 | 科技载体分布展示 | 无（N/A other_system，依据见 §1.2） | — | N/A | N/A | N/A（无指标行） | n/a（other_system：GIS 落图，无独立统计核） | D18 演示读数 = mock（类型计数 2856/128/… 为 demo 全市口径） | 🧪（演示计数）；无 metric_id → 不挂 ⓘ 语义卡、计数旁不显伪 8 件套（ARCH §4.4）；评审模式 DOM 零泄漏 |
| 189 | 产业与领域筛选联动 | 无（N/A n/a_ops，依据见 §1.2） | — | N/A | N/A | N/A（无指标行） | n/a（交互壳，无指标行；随宿主 185/188 表行） | 演示种子值（随 185/188 表行，无独立读数、无独立端点） | 无指标角标；无 metric_id → 不挂 ⓘ、不显伪 8 件套；DOM 零泄漏纪律仍适用 |
| 190 | 资源配置优化建议 | 无（N/A n/a_ops 建议壳，依据见 §1.2） | — | N/A | N/A | N/A（无指标行） | n/a（建议壳，无指标行） | D18 表读数 = mock（3 方案 plans 行 demo 逐字，非生成物） | 🧪（演示行）；无 metric_id（表行 `metric_id` 列 NULL）→ 不挂 ⓘ、不显伪卡；详见 §4.3 建议壳纪律 |

**D1 / D3 / D4 通用注**（适用全表）：

- **D1**：4 条 kit 指标口径草稿已认（语义 Owner `human:淮政玮`），公式 / `algorithm_type` 未签，未入 seed → 按核对记录 §6「TEMP_ 未入 seed：D1 按 `missing`/`draft` 诚实」，本分册记 **draft**；从注册表视角该 ID 不存在（missing），不伪称已定义完。
- **D3**：A1 双表未交 → **不伪 `full`**；8 件套草稿源表只到「ADS/ES display」层级（V1 实读 = D18 `ts_plan_key_area_*` 9 表），不把项目 DWD 反推成 ODS `full`，「V1 看板字段走 display ADS，不自动等于 mapped 05」（核对记录 §5）。
- **D4**：D18 铁律——9 表 61 行读数是 demo 冻结种子灌数、非真算 → **D4 仍 mock**，🧪 MockBadge 保留至 D4 翻转（ARCH G-B5 沿袭）；188 / 190 无 metric 行不挂 D4 维，但演示计数 / 方案行仍属 mock 读数；189 无表无端点（消费 185/188 表行，ARCH §4.5）。

### 1.2 口径与 N/A 依据（核对记录 §3.3 逐字抄录）

**seq 185（口径列原文）**：

> 「创新资源在地理空间上的分布密集程度与集聚水平（xlsx 100/101）。宿主=区域科技创新空间布局分析。对象=GIS 地理密度，不是协同网络密度（seq 191）」

**seq 186（两条，口径列原文）**：

> 「规划页**区域**对象的竞争力水平分值（xlsx 102）+ 指标体系/对标。对照 05 综合 186 活力指数/单维评分（语义，不是展示序号 186）。与 SYNTH-VITALITY / DS-04-CITY / DS-06-CITY **同叶不同页**」（COMPETITIVENESS）
>
> 「同上叶的发展潜力评分（xlsx 103；186 正文含发展潜力）。对象=区域，不是某项技术的产业化潜力（技术链 135）」（POTENTIAL）

**seq 187（口径列原文）**：

> 「土地利用类型上的创新产出效益（xlsx 104）与土地利用效率（xlsx 105）。宿主=土地用途与效益分析。对象=GIS 用地/产出图层，不是要素类型综合评价（综合 187）」

**seq 188 / 189 / 190 · N/A 依据**（核对记录 §3.3「本页 ④ 不适用」原文条目）：

> 「科技载体分布展示（seq 188）｜other_system｜GIS 载体点位 + ADS 详情；不是载体价值排名。禁止抢 DS-06-CARRIER missing；禁止 mapped 116 / 综合 188」
>
> 「产业与领域筛选联动（seq 189）｜n/a_ops｜大门类/细分 + 地图联动壳；xlsx 98 技术规模 / 99 技术发展状态随壳展示，不另开 missing。禁止 mapped 综合 189 / 技术链 133/137」
>
> 「资源配置优化建议（seq 190）｜n/a_ops｜投入建议 / 布局优化 / 方案模拟与效果预测 = **建议壳**。原文未点名生成模型。禁止 missing 模拟叶；禁止借 501；禁止按号综合 190；禁止改挂 186 附录建议、技术链 140、`M_CHAIN_LAYOUT_*`；禁止 also_in `M_POLICY_INDUSTRY_FIT`。不编制规划文本」

差集对照（核对记录 §1.2 原文行）：185 other_system / 186 **mapped** 综合 186（语义）/ 187 other_system / 188 other_system / 189 n/a_ops / 190 n/a_ops——「**7/7 库缺口 missing 行保持 missing**（综合 3 + 研究 4；KEY-DOMAIN A=0）」，本分册不改任何判定。

---

## 2. `M_INNOV_KEYD_*` 四条明细卡

> 全部为**赋号草稿 · 类型未签 · 未入 seed**（核对记录 §赋号表 2026-08-22；协议 `METRIC-ID-ASSIGN-LOOP-循环工程.md`，ELEMENT=`INNOV`，reuse=0；真源机器卡全部 `TEMP_DS09_*`（COMP 5 + RES 4 + KEYD 4），13 条赋号里 KEYD 占 4：STAT 2 · MIXED 2）。8 件套草稿公共字段（TEMP_ 共同，核对记录 §3 原文）：「源系统=科技信息展示系统·科技发展规划 / display；更新频率=未定；version=`draft-open-ds09`；源表=ADS/ES display（A1 表2 未交 → 本叶不填伪 full）。`algorithm_type` 为建议、未签。」Q-MO-DS09-04 登记于 `metrics/request/_work/id-assign/DS-09-METRIC-OPEN-L01-questions.yaml`（核对记录 §7 产物清单；本分册不读不改）。

### 2.1 `M_INNOV_KEYD_SPATIAL` · 空间密度与集聚度 —— 赋号草稿 · 类型未签 · 未入 seed

| 字段 | 值（真源：核对记录 §赋号表 / §2 / §3.3） |
|---|---|
| temp_id 对照 | `TEMP_DS09_KEYD_SPATIAL` |
| 主落点 | KEY-DOMAIN seq 185 / xlsx 100–101 |
| 口径 | 见 §1.2 seq 185 逐字抄录 |
| 公式（未签，原文） | 「GIS + ADS 图层读数；不伪挂 191。禁止因「库无空间密度专叶」写成 missing」 |
| 建议 type | STAT（未签） |
| reuse_of（禁用清单，§赋号表逐字） | 不复用 seq 191 / `M_ENT_AGGLOMERATION_INDEX` |
| pending_ref | —（语义债 KEYD-B02：竞争力/潜力/密度/土地效益无正式 metric_id，差集 mapped/other_system 不动） |
| §2 消费矩阵 pending | 禁 mapped 191 网络密度；禁 missing |
| 差集保持 | other_system |
| 落地表 / 读取接口 | `ts_plan_key_area`（3 集群行，`metric_id` 列=SPATIAL 草稿）+ `ts_plan_key_area_carrier`（22 载体行提供地图落点，7 行 cluster_id NULL 诚实空）/ 契约 §3.7 `key-areas` clusters + carriers 块（ARCH §4.1） |
| UI | 🧪 + 统计数 ⓘ draft 语义卡（回指核对记录 §赋号表，不显伪 8 件套）+ ⚠️「待甲方确认」（类型未签；真算密度/集聚度待 GIS 图层服务接入，V1 为集聚归属演示，非网络密度） |

### 2.2 `M_INNOV_KEYD_COMPETITIVENESS` · 区域科技创新竞争力水平 —— 赋号草稿 · 类型未签 · 未入 seed

| 字段 | 值 |
|---|---|
| temp_id 对照 | `TEMP_DS09_KEYD_COMPETITIVENESS` |
| 主落点 | KEY-DOMAIN seq 186 / xlsx 102 |
| 口径 | 见 §1.2 seq 186 逐字抄录（COMPETITIVENESS 段） |
| 公式（未签，原文） | 「演示：随 186；权重未签。禁止企业 141、`M_CHAIN_COMPETITIVENESS_INDEX` / `M_CHAIN_REGION_INDEX`」 |
| 建议 type | MIXED（未签） |
| reuse_of（禁用清单，§赋号表逐字） | 不复用 `M_SYNTH_VIT_*` / GBA/CITY 186 号 |
| pending_ref | **Q-MO-DS09-04** |
| §2 消费矩阵 pending | KEYD-B03；禁改挂 `M_SYNTH_VIT_*` |
| 差集保持 | mapped 186（仅语义允许，同叶不同页，不改挂 SYNTH ID；见 §3） |
| 落地表 / 读取接口 | `ts_plan_key_area_competitiveness`（5 指标卡行：potential 行挂 POTENTIAL、其余 4 行挂本号）+ `ts_plan_key_area_dimension`（五维行 `metric_id`=本号，`dim_key` U8-1 定名）+ `ts_plan_key_area_benchmark`（对标 5 行 `metric_id`=本号）/ 契约 §3.7 `key-areas` competitiveness_metrics / dimension_scores / benchmark_rows 三块（ARCH §4.2、§5 平铺 9 块） |
| UI | 🧪 + 统计数 ⓘ draft 语义卡 + ⚠️「待甲方确认」（维名/权重未冻 U8-1；「竞争力水平」vs「区域创新活力」文案走 KEYD-B03；Q-MO-DS09-04） |

### 2.3 `M_INNOV_KEYD_POTENTIAL` · 区域科技创新发展潜力 —— 赋号草稿 · 类型未签 · 未入 seed

| 字段 | 值 |
|---|---|
| temp_id 对照 | `TEMP_DS09_KEYD_POTENTIAL` |
| 主落点 | KEY-DOMAIN seq 186 / xlsx 103 |
| 口径 | 见 §1.2 seq 186 逐字抄录（POTENTIAL 段） |
| 公式（未签，原文） | 「随 186。禁止挂 135，也不因此 missing」 |
| 建议 type | MIXED（未签） |
| reuse_of（禁用清单，§赋号表逐字） | 不复用 `M_TECH_POTENTIAL_SCORE` / 135 |
| pending_ref | **Q-MO-DS09-04** |
| §2 消费矩阵 pending | 禁技术链 135 |
| 差集保持 | mapped 186（同 2.2） |
| 落地表 / 读取接口 | `ts_plan_key_area_competitiveness` 的 potential 行（`metric_key=potential` 专用行挂本号；ARCH §7.1「配套」：指标卡块与五维画像并存不合并，英文键沿用 demo 原键）/ 同端点 competitiveness_metrics 块 |
| UI | 同 2.2 |

### 2.4 `M_INNOV_KEYD_LAND` · 土地创新产出效益与利用效率 —— 赋号草稿 · 类型未签 · 未入 seed

| 字段 | 值 |
|---|---|
| temp_id 对照 | `TEMP_DS09_KEYD_LAND` |
| 主落点 | KEY-DOMAIN seq 187 / xlsx 104–105 |
| 口径 | 见 §1.2 seq 187 逐字抄录 |
| 公式（未签，原文） | 「GIS + ADS 读数。禁止按号 mapped 187；禁止 missing。土地句里的优化建议不改挂 seq 190」 |
| 建议 type | STAT（未签） |
| reuse_of（禁用清单，§赋号表逐字） | 不复用综合 187 |
| pending_ref | —（语义债 KEYD-B02） |
| §2 消费矩阵 pending | 禁按号 mapped 综合 187；禁 missing |
| 差集保持 | other_system |
| 落地表 / 读取接口 | `ts_plan_key_area_land`（6 区级行，`metric_id`=本号；逐载体 `land_benefit` JSON V1 全 NULL 诚实空，字段定名 U8-2）/ 契约 §3.7 `key-areas` land_use 块（ARCH §4.3、§7.2） |
| UI | 🧪 + 统计数 ⓘ draft 语义卡 + ⚠️「待甲方确认」（亩均/容积率正式值待数据侧接入 GIS 用地图层后回填，U8-2；空态不显伪数） |

### 2.5 端点 `metric_id` 字位（契约 §3.7）

| 端点（契约 §） | `metric_id` 字位（草案示例） | 本分册落位（草稿） |
|---|---|---|
| §3.7 `GET /v1/situation/planning/key-areas` | 示例仅 `clusters[].metric_id` + `data.metric_ids[]`（均为 `"Q0xx"` 占位） | ARCH §5 已裁定响应改**平铺 9 块**：`metric_id` 下沉到各块表行——clusters 行=SPATIAL；competitiveness_metrics 行=potential 行挂 POTENTIAL、余挂 COMPETITIVENESS；dimension_scores / benchmark_rows 行=COMPETITIVENESS；land_use 行=LAND；carriers / carrier_types / district_baselines / plans 块无核叶 `metric_id` 置 NULL（188 other_system、190 n/a_ops；ARCH §4.4/§4.6、§6「每表带 `metric_id` 列（无核叶置 NULL）」）；`data.metric_ids[]` 汇总四条 KEYD 草稿号。新响应示例由 KEY-API 分册起草，批 4 冻结时改约（本分册不代填契约正文） |

**占位符警告**：契约 §3.7 示例中的 `"metric_id": "Q0xx"` / `"metric_ids": ["Q0xx"]` 是**字位占位符，不是真 ID**。实现回填用本分册 §2 草稿 ID（回填动作归 KEY-API 分册 / 实现单）；**不得取 `Q010`～`Q019` / `QPOL-*` 段**——那是展示企业 / 政策口径族，核对记录 §4 明令「本页不改挂、不关闭」。前端另守核对记录 §6：「关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / `501` / 就绪度字样」。

---

## 3. 撞号禁令专节（硬边界，随稿冻结）

### 3.1 整段撞号与 186 仅语义允许（核对记录 §3.3 头部原文）

> 「本页 A=0。catalog 无 501（预警只挂 COMPREHENSIVE）。规划读面不跑 SYNTH Job，**禁止**改挂 `M_SYNTH_VIT_*` 为本页正式 ID。展示 seq 185–190 与 05 综合 185–190 **整段撞号，禁止按号 mapped**（186 仅按语义允许）。」

- **整段撞号**：展示 seq 185–190 与综合 05 seq 185–190 是两套编号，**禁止按号 mapped**（不得把展示 185 对号综合 185、……、展示 190 对号综合 190）。
- **186 仅语义允许**：对照的是 05 综合 186 的**语义**（活力指数/单维评分），「（语义，不是展示序号 186）」「与 SYNTH-VITALITY / DS-04-CITY / DS-06-CITY **同叶不同页**」（§3.3 口径原文）；核对记录 §1.2 差集行原文「**mapped** 综合 186（语义）｜**kit**（TEMP_，不改挂 SYNTH ID）」——演示随 186，**不改挂** `M_SYNTH_VIT_*` / GBA/CITY 186 读面号，也不在本页跑 SYNTH Job。
- **§1.1 禁止列原文**（KEY-DOMAIN 行）：「展示 185–190 对号入座综合 185–190（186 仅语义允许）；改挂 `M_SYNTH_VIT_*` / 技术链 135 / 企业 141；载体分布写成 DS-06-CARRIER 价值排名 missing；建议壳借 501 / missing 模拟模型」

### 3.2 逐叶禁改挂（§3.3 公式列 + N/A 表原文 + §2 pending 列；ARCH §7.3 同口径）

- **185**：禁 mapped 191 网络密度；禁复用 `M_ENT_AGGLOMERATION_INDEX`；禁因「库无空间密度专叶」写成 missing
- **186**：禁改挂 `M_SYNTH_VIT_*` / GBA/CITY 186 读面号；禁企业 141；禁 `M_CHAIN_COMPETITIVENESS_INDEX` / `M_CHAIN_REGION_INDEX`；禁挂技术链 135（POTENTIAL 亦禁 `M_TECH_POTENTIAL_SCORE`）
- **187**：禁按号 mapped 综合 187；禁 missing；土地句里的「优化建议」不改挂 seq 190
- **188**：禁抢 DS-06-CARRIER missing；禁 mapped 116 / 综合 188
- **189**：禁 mapped 综合 189 / 技术链 133/137
- **190**：禁按号综合 190；禁改挂 186 附录建议 / 技术链 140 / `M_CHAIN_LAYOUT_*`；禁 also_in `M_POLICY_INDUSTRY_FIT`；禁 missing 模拟叶；禁借 501（§4.3）

### 3.3 全族禁改挂与跨 DS 禁混挂（§赋号表头部/尾注 + §3.3 尾句原文）

- **§赋号表头部原文**：「**reuse=0**：热度 ≠ `M_TECH_HEAT_INDEX` / `M_TECH_TOPIC_HEAT`；流动 ≠ `M_TALENT_FLOW_TRACK`；竞争力/潜力 ≠ `M_SYNTH_VIT_*` / 湾区·全球城市 186 读面号。禁止改挂 `M_CHAIN_*` / 专题人才 ID。」（KEYD 直接相关：竞争力/潜力两条；专题人才 ID（seq 157 / TOPIC-TALENT 族）本页不消费——核对记录 §1.1「本叶不消费」列明「专题 TOPIC-ENT / TOPIC-TECH / TOPIC-TALENT / SYNTH / CHAIN / SVC / POLICY OPEN」）
- **四条 `M_INNOV_KEYD_*`** 均赋号草稿·未签·pending `human:唐绍祖`；禁改挂 `M_SYNTH_VIT_*` / `M_ENT_*` / `M_CHAIN_*` 及 B 轨 / SYNTH / CHAIN / SVC / TECH 全族（ARCH §7.3）。
- **§3.3 尾句原文**：「禁止湾区 DS-05、深圳 DS-06-CITY/CARRIER/DOMAIN、DS-07 产业发展潜力、DS-08 指数混挂。」
- **形近 ID 一律不消费**（§赋号表尾注原文）：「形近 `M_CHAIN_HOTSPOT_*` / `M_CHAIN_COMPETITIVENESS_INDEX` / `M_CHAIN_SZ_ADVANTAGE_*` / `M_ENT_COMPETITIVENESS_*` / `M_SYNTH_VIT_*` 一律不消费。Wave A `M_TECH_HEAT_INDEX` / `M_TALENT_FLOW_TRACK` / `M_INNOV_GBA_CAPACITY_INDEX` 等不同口径，不 reuse。」撞号核查结论沿用核对记录：「13 个拟号全部 miss」（经 `metric-registry-lib` / MCP，未整文件读 seed）。

### 3.4 UI 禁点伪 8 件套与禁发明新 ID（§6 + §5 原文）

- 统计数 ⓘ MetricSpecCard 只回指核对记录 §赋号表 `M_INNOV_*`（TEMP_ 对照）；**禁止**点开 `M_CHAIN_*` / `M_SVC_*` / `M_SYNTH_*` / `M_ENT_*` / `M_TALENT_*` / `M_SYNTH_COLLAB_*` 伪 8 件套（核对记录 §6）；「计数旁不显伪 8 件套」（ARCH §4.4，188）。
- 禁止发明的新 ID 形态（核对记录 §5「本叶不做」原文清单，KEYD 相关加粗）：「不发明 `M_PLAN_*` / `M_HOTSPOT_*` / `M_LOCAL_ADV_*` / `M_TALENT_FLOW_*` / `M_DIRECTION_ALERT_*` / `M_OVERLAP_*` / `M_CI_*` / **`M_KEYDOMAIN_*`** / **`M_SPATIAL_*`**」。

---

## 4. U8 未决与角标 · 190 建议壳纪律

### 4.1 未决项 → UI ⚠️「待甲方确认」对应

| 未决项 | 内容（真源） | 涉及叶 / 指标 | UI ⚠️ 对应 |
|---|---|---|---|
| **U8-1** | 竞争力五维 key 定名。契约 §3.7 边界原文：「竞争力五维 key 定稿 U8」。ARCH §7.1 裁定建议：五维以 demo `keyAreaDimensionScores` 五中文名为权威——创新资源 / 科研产出 / 产业竞争力 / 人才支撑 / 开放协同；英文键建议 `innovation_resources` / `research_output` / `industry_competitiveness` / `talent_support` / `open_collaboration`；契约示例五维「技术/产业/空间/人才/政策」与 demo 两数组均不符（草案虚构），弃用；不引「空间维」以免与 185 SPATIAL 混淆 | 186 · COMPETITIVENESS / POTENTIAL（`ts_plan_key_area_dimension.dim_key` 新列） | 五维画像 / 指标卡统计数旁 ⚠️「待甲方确认」（维名/权重未冻，文案走 KEYD-B02/B03；核对记录 §6「维名/权重/501 未冻：⚠️『待甲方确认』（文案走 COMP/KEYD/RES-B*）」），与 🧪、ⓘ draft 并存 |
| **U8-2** | `land_benefit`（土地效益）字段定名。契约 §3.7 边界原文：「`land_benefit`（土地效益：容积率 / 亩均产出）字段名待数据侧定名（U8）」。ARCH §7.2 裁定建议：沿用契约示例 `plot_ratio`（容积率）/ `output_per_mu`（亩均产出）；V1 该 JSON 列全 NULL（demo 冻结种子无逐载体土地数据，诚实空，禁编造容积率/亩产）；187 读数由 `ts_plan_key_area_land` 区级行承载，正式态接入 GIS 用地图层后回填真值 | 187 · LAND（+ carrier 表 `land_benefit` 预留列） | 土地效益读数旁 ⚠️「待甲方确认」（亩均/容积率正式值待数据侧），与 🧪、ⓘ draft 并存；空态不显伪数 |

两项归属：**M0 + 数据侧拍板**（ARCH §7.4「本稿消费：U8（§7.1/§7.2 给裁定建议，M0 + 数据侧拍板）」）；定名落库归 KEY-DATA 分册 DDL 冻结，本分册只给指标侧落位（2.2 / 2.4 落地表行）。

### 4.2 语义债沿袭（不升 🟢）

- **KEYD-B01**：本页无四件套 / TRACE——文件级闭合；不发明 `M_*`
- **KEYD-B02**：竞争力/潜力/密度/土地效益无正式 metric_id——语义债；差集 mapped/other_system 不动
- **KEYD-B03**：「竞争力水平」vs「区域创新活力」；五级名重点领域 vs 叶文区域——语义债；不另开 A、不发明竞争力 `M_*`

三项保持（核对记录 §4；ARCH §7.4「语义债沿袭：KEYD-B01..B03 保持；差集不动」），不升 🟢、不关闭、不新建 Q0xx、不改 `客户决策清单跟踪表.md`。

### 4.3 seq 190 建议壳纪律（专条）

**定位：建议壳，不是 501，也不是 missing 模拟模型。**

- **本页 catalog 无 501**（§3.3 头部原文）：「catalog 无 501（预警只挂 COMPREHENSIVE）」；501 实现通道只给 COMPREHENSIVE seq 184（核对记录 §5）。
- **真源原句**（核对记录 §5）：「仅 COMPREHENSIVE seq 184 可走 501 实现通道；**未注册 metric_id**；差集 **missing**。父句预测可视化已收口 134，**不得**借 501 伪覆盖捕捉/跟踪。RESEARCH / KEY-DOMAIN **不得**进 501。KEY-DOMAIN seq 190 模拟预测 = 建议壳，不是 501。」
- **N/A 依据原文**（§3.3「本页 ④ 不适用」，逐字见 §1.2）：投入建议 / 布局优化 / 方案模拟与效果预测 = **建议壳**；原文未点名生成模型；禁止 missing 模拟叶；禁止借 501；禁止按号综合 190；禁止改挂 186 附录建议、技术链 140、`M_CHAIN_LAYOUT_*`；禁止 also_in `M_POLICY_INDUSTRY_FIT`；不编制规划文本。
- **落地（ARCH §4.6 / §5）**：`ts_plan_key_area_plan` 3 行为 demo 种子逐字（`summary` / `actions` 非生成物），**plans 为页级**（非集群级）；表行 `metric_id` 列 NULL（n/a_ops 建议壳，演示读数不挂 ID）；「方案模拟」Modal = FE 交互，效果预测值即表行 `expected_effect`（demo 逐字），**无模拟端点、无 501**；不编制规划正文 / 优化建议文本。

---

## 5. 纪律声明

1. **不写 seed**：本分册不写 `metrics/registry/` seed / 矩阵 / 任何 `cfg_metric-*-seed.yaml`；4 条 `M_INNOV_KEYD_*`（连同全 DS-09 13 条）均为赋号草稿、**未入 seed**，seed 侧零改动（核对记录 §5「本叶不做」原文：「不写任何 `cfg_metric-*-seed.yaml`」；§赋号表：「身份草稿只在本表 + `id-assign/`；**不写 seed / 展示 catalog / 共享 QUESTIONS。**」）。
2. **不改 `algorithm_type`**：STAT / MIXED 均为核对记录草稿建议、未签；公式与 `algorithm_type` 一律 `pending_cosign: human:唐绍祖`，本分册不签、不改 seed 既有类型。
3. **不改差集判定**：KEY-DOMAIN A=0，「7/7 库缺口 missing 行保持 missing」；本页差集 SPATIAL/LAND other_system、COMPETITIVENESS/POTENTIAL mapped 186（仅语义）、188 other_system、189/190 n/a_ops 全部不动；186 mapped 是语义对照非按号，不伪闭合。
4. **指标查询纪律**：对既有指标身份只经 metric-registry MCP（`metric-get` / `metric-query`）查询，不整文件读 seed、不自行撞号判定；本分册为定义稿、未发起新查询，撞号结论沿用核对记录 §赋号表「13 个拟号全部 miss」（其核查经 `metric-registry-lib` / MCP）。
5. **不发明 `M_*`、不改 task-registry、不 git 提交**：本分册只写本文件一个；口径全部逐字抄录核对记录，不改写语义；开放项状态不动（KEYD-B01..B03 保持、不升 🟢、不新建 Q0xx）。

---

**会签路径**：同 KEY-ARCH §9——四角色会签（architect / api / algorithm / data，意见落 `sdd/l2/会签/重点领域规划-会签.md`）→ 全部同意后由 `actor=human:淮政玮` 签收；公式与 `algorithm_type` 的签署另行走 `pending_cosign: human:唐绍祖`（核对记录 §8 签署区），不在本分册闭合。
