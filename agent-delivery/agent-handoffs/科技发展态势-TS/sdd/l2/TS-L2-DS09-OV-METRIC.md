# TS-L2-DS09-OV-METRIC · 综合发展规划 · 后台指标设计

> **任务**：`TS-L2-DS09-OV-METRIC`（definition，不写业务代码、不改 metrics seed、不发明 `M_*`）
> **日期**：2026-11-06 · **作者**：agent:zcode 会话代跑 algorithm-agent · **监管**：`human:王梓真`
> **状态**：草案待会签（architect / api / algorithm / data，意见落 `sdd/l2/会签/综合发展规划-会签.md`）
> **公式与 `algorithm_type` 一律 `pending_cosign: human:唐绍祖`，本分册不签**

**输入真源**

| 用途 | 真源 |
|---|---|
| 指标唯一真源（本分册一切口径逐字抄录自此） | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-09-科技发展规划-核对记录.md`（§赋号表 13 条 TEMP→`M_INNOV_*`、§2 消费矩阵、§3.1 COMPREHENSIVE 页语义卡、§4 开放项） |
| 硬依赖架构稿 | `agent-handoffs/科技发展态势-TS/sdd/l2/TS-L2-DS09-OV-ARCH.md`（D18 逐叶判定、G-B4/G-B5/G-B6、§4 逐叶架构） |
| 契约草案（批 4 未冻结） | `agent-handoffs/科技发展态势-TS/API-TS-M9.md` §3.1–§3.6（各端点 `metric_id` 字位） |
| 需规 7 叶 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技发展规划.md` seq 178–184 |

**范围**：DS-09 `DS-09-COMPREHENSIVE` 页（FE-TS-09a）7 叶（seq 178–184）的后台指标设计：逐叶判定、5 条 `M_INNOV_PLAN_*` 明细卡、`M_INNOV_PLAN_DIRECTION_ALERT` 501 pending 语义、禁改挂清单、未决项 U5/U6 与 UI 角标对应、纪律声明。RESEARCH / KEY-DOMAIN 两页的另 8 条 `M_INNOV_*` 赋号不在本分册展开（归各自分册），仅在 §4 禁改挂清单整表收口。**口径一律逐字抄录核对记录，不改写语义。**

---

## 1. 逐叶指标判定表（7 叶）

### 1.1 总表

| seq | 叶 | metric_id（草稿） | 中文名 | 公式状态 | algorithm_type 建议（未签） | D1 | D3 | D4 | UI 角标要求 |
|---|---|---|---|---|---|---|---|---|---|
| 178 | 全球热点技术捕捉 | `M_INNOV_PLAN_HEAT` / `M_INNOV_PLAN_GROWTH` | 热度指数 / 增长速度 | 未签（不伪展开） | MIXED / MIXED | draft（未入 seed） | 不伪 full | D18 表读数 = mock | 🧪 MockBadge + 统计数 ⓘ draft 语义卡 + ⚠️「待甲方确认」（U5 权重未冻，文案走 COMP-B02） |
| 179 | 多维度指标体系展示 | 无（N/A + 依据见 §1.2） | — | N/A | N/A | N/A（无指标行） | n/a（运营壳） | 演示种子值（mock，无 metric 行不挂 D4 维） | 🧪（演示种子）；无 metric_id → 不挂 ⓘ 语义卡、不显伪 8 件套；评审模式 DOM 零泄漏 |
| 180 | 技术与产业热点动态跟踪 | 无独立核（消费 178 两指标） | — | N/A | N/A | N/A | n/a（无指标行，随宿主 HEAT/GROWTH，D3=不伪 full） | D18 表读数 = mock | 🧪 + ⓘ 回指 HEAT/GROWTH 草稿卡；空间分布语义债走 COMP-B03（禁硬挂 133） |
| 181 | 本地特色与优势分析 | `M_INNOV_PLAN_LOCAL_ADV` | 本地科技创新特色与优势 | 未签（模型未签） | MODEL | draft（未入 seed） | 不伪 full | D18 表读数 = mock | 🧪 + ⓘ draft（Q-MO-DS09-01）+ ⚠️（模型未签；「示例抽样」标注保持至正式态换真源） |
| 182 | 科技人才流动监控 | `M_INNOV_PLAN_TALENT_FLOW` | 科技人才流动（产业界↔学术界） | 未签（模型未签） | MODEL | draft（未入 seed） | 不伪 full | D18 表读数 = mock | 🧪 + ⓘ draft（Q-MO-DS09-02）+ ⚠️「待甲方确认」（U6 法务未决） |
| 183 | 科创资源整合与推送 | 无（N/A + 依据见 §1.2） | — | N/A | N/A | N/A | n/a（复用 app_user 订阅家族） | 真读+真写（非 D18，无统计数，无 D4 可标） | 无指标角标；DOM 零泄漏纪律仍适用 |
| 184 | 潜在科技发展方向预警 | `M_INNOV_PLAN_DIRECTION_ALERT` | 潜在科技发展方向预警 | 未签（模型未签；501 pending） | MODEL | draft（未入 seed） | 不伪 full | 未接入（501 通道；V1 零行，无读数） | 无 🧪（无展示数）；⚠️「预警模型未注册」+ 空态 + 报告导出禁用；不显伪卡 |

**D1 / D3 / D4 通用注**（适用全表）：

- **D1**：5 条 kit 指标口径草稿已认（语义 Owner `human:淮政玮`），公式 / `algorithm_type` 未签，未入 seed → 按核对记录 §6「TEMP_ 未入 seed：D1 按 `missing`/`draft` 诚实」，本分册记 **draft**；从注册表视角该 ID 不存在（missing），不伪称已定义完。
- **D3**：A1 双表未交 → **不伪 `full`**；8 件套草稿源表只到「ADS/ES display」层级（V1 实读 = D18 `ts_plan_*` 表），不把项目 DWD 反推成 ODS `full`，「V1 看板字段走 display ADS，不自动等于 mapped 05」（核对记录 §5）。
- **D4**：D18 铁律——表读数是 demo 冻结种子灌数、非真算 → **D4 仍 mock**，🧪 MockBadge 保留至 D4 翻转（ARCH G-B5）；184 无读数（501 通道）；183 无统计数。

### 1.2 口径与 N/A 依据（核对记录 §3.1 逐字抄录）

**seq 178（两条，口径列原文）**：

> 「热门技术领域在当前周期内的受关注程度与活跃水平；宿主=全球热点技术捕捉（自动识别热门领域 + 热点列表）。对象=技术领域，不是论文/专利条目计数。对照 05 seq 134 热点指数；与 TOPIC-TECH-05 / SCI-D03 **同叶不同页**」（HEAT）
>
> 「热门技术领域的发展速度与增长变化。⊂ 134 研究热度/趋势。宿主仍是 seq 178，不是独立 A、不是 seq 184 预警」（GROWTH）

**seq 179 · N/A 依据**（核对记录 §3.1「本页 ④ 不适用」原文条目）：

> 「多维度指标体系展示（seq 179）｜n/a_ops｜大屏多库指标 + 自定义布局/联动 = 展示运营壳；无计算模型原文。禁止 missing「库无多维指标体系」。禁止硬挂 186–190」

**seq 180 · N/A 依据**（同表原文条目 + §3.1 seq 180 正文）：

> 「热点动态跟踪（seq 180）｜third_party｜与捕捉同叶 134 读面；时间轴 ≠ 132 历程。无独立 TEMP_」
>
> 「seq 180 热点动态跟踪：选领域全球动态 + 时间轴 = 同一 134 叶动态监测/阶段可视化 → **④ 无独立统计核**（消费 TEMP_HEAT/GROWTH）。空间分布无 134 地理专核 → COMP-B03，不另开 A，禁止硬挂 133。」

**seq 181 / 182 / 184（三条，口径列原文）**：

> 「本地优势领域、创新资源分布，及与全球水平对比。对象=规划页「本地」，不是深圳城市竞争力拆项（xlsx 60–63 / DS-06），不是区域创新活力四维指数」（LOCAL_ADV）
>
> 「核心技术人才在**产业界和学术界**之间的流动趋势 + 预警。对象≠人才 05 seq 157（社交/招聘区域或行业流入流出，无学界任职/论文流动、无流动预警）」（TALENT_FLOW）
>
> 「结合论文、专利、项目、人才、产业和政策多源，对**潜在科技发展方向**持续监测与预警。招标父句「潜在的科技发展方向预警」收口本叶。对象≠ 134 已识别热点的趋势预测」（DIRECTION_ALERT）

**seq 183 · N/A 依据**（「本页 ④ 不适用」原文条目）：

> 「科创资源整合与推送（seq 183）｜n/a_ops｜关注领域 + 推送条件 + 定期推送 = 订阅壳。不编制规划文本。禁止 missing；禁止 `M_SVC_REC_*` / seq 164」

---

## 2. `M_INNOV_PLAN_*` 五条明细卡

> 全部为**赋号草稿 · 类型未签 · 未入 seed**（核对记录 §赋号表 2026-08-22；协议 `METRIC-ID-ASSIGN-LOOP-循环工程.md`，ELEMENT=`INNOV`，reuse=0）。8 件套草稿公共字段（TEMP_ 共同，核对记录 §3 原文）：「源系统=科技信息展示系统·科技发展规划 / display；更新频率=未定；version=`draft-open-ds09`；源表=ADS/ES display（A1 表2 未交 → 本叶不填伪 full）。`algorithm_type` 为建议、未签。」

### 2.1 `M_INNOV_PLAN_HEAT` · 热度指数 —— 赋号草稿 · 类型未签 · 未入 seed

| 字段 | 值（真源：核对记录 §赋号表 / §2 / §3.1） |
|---|---|
| temp_id 对照 | `TEMP_DS09_COMP_HEAT` |
| 主落点 | COMPREHENSIVE seq 178 / xlsx 96 |
| 口径 | 见 §1.2 seq 178 逐字抄录（HEAT 段） |
| 公式（未签，原文） | 「不伪展开；随 134 实现类 / 第三方。禁止用产业化潜力（135）或历程（132）顶替」 |
| 建议 type | MIXED（未签） |
| reuse_of（禁用清单） | 不复用 `M_TECH_HEAT_INDEX` / `M_TECH_TOPIC_HEAT` |
| pending_ref | —（语义债 COMP-B02：热度指数/增长速度无正式 metric_id，差集 third_party 134 不动） |
| §2 消费矩阵 pending | COMP-B02；禁伪公式；禁改挂 132/135 |
| 差集保持 | third_party 134 |
| 落地表 / 读取接口 | `ts_plan_hot_tech`（heat 列）+ `ts_plan_hot_tech_series` / 契约 §3.2 `hot-technologies`（`caliber_note` 必返，文案由表行携带而非 Java 硬编码，ARCH §4.1） |
| UI | 🧪 + 统计数 ⓘ draft 语义卡（回指 §赋号表，不显伪 8 件套）+ ⚠️「待甲方确认」（U5 权重 40/30/20/10 未冻） |

### 2.2 `M_INNOV_PLAN_GROWTH` · 增长速度 —— 赋号草稿 · 类型未签 · 未入 seed

| 字段 | 值 |
|---|---|
| temp_id 对照 | `TEMP_DS09_COMP_GROWTH` |
| 主落点 | COMPREHENSIVE seq 178 / xlsx 97 |
| 口径 | 见 §1.2 seq 178 逐字抄录（GROWTH 段） |
| 公式（未签，原文） | 「不伪展开。禁止把增速改挂方向预警」 |
| 建议 type | MIXED（未签） |
| reuse_of（禁用清单） | 不复用 `M_INNOV_FACTOR_GROWTH` / 专题热度同核 |
| pending_ref | —（语义债 COMP-B02） |
| §2 消费矩阵 pending | COMP-B02；禁改挂 seq 184 |
| 差集保持 | third_party 134 |
| 落地表 / 读取接口 | 同 2.1（`ts_plan_hot_tech` growth 列 / §3.2 `hot-technologies`） |
| UI | 同 2.1 |

### 2.3 `M_INNOV_PLAN_LOCAL_ADV` · 本地科技创新特色与优势 —— 赋号草稿 · 类型未签 · 未入 seed

| 字段 | 值 |
|---|---|
| temp_id 对照 | `TEMP_DS09_COMP_LOCAL_ADV` |
| 主落点 | COMPREHENSIVE seq 181 |
| 口径 | 见 §1.2 seq 181 逐字抄录 |
| 公式（未签，原文） | 「模型未签；05 无专叶。禁止硬挂 186 / 按号 182 / 133 / 140 / 159 / 187。禁止 `M_CHAIN_SZ_ADVANTAGE_RANK`」 |
| 建议 type | MODEL（未签） |
| reuse_of（禁用清单） | 不复用 `M_CHAIN_SZ_ADVANTAGE_*` / 186 |
| pending_ref | **Q-MO-DS09-01** |
| §2 消费矩阵 pending | 禁硬挂 186；禁 `M_CHAIN_SZ_ADVANTAGE_*` |
| 差集保持 | **missing**（05 无专叶，不伪闭合） |
| 落地表 / 读取接口 | `ts_plan_local_adv`（base_region/compare_to + 维度行 + `reference_stats` JSON，含 FE 补两维 lumen_seed 标注）/ 契约 §3.4 `local-advantage`（`reference_stats.source` 必返；「示例抽样」字样 Mock 态保留，正式态须换真源标注） |
| UI | 🧪 + ⓘ draft + ⚠️（模型未签 Q-MO-DS09-01） |

### 2.4 `M_INNOV_PLAN_TALENT_FLOW` · 科技人才流动（产业界↔学术界） —— 赋号草稿 · 类型未签 · 未入 seed

| 字段 | 值 |
|---|---|
| temp_id 对照 | `TEMP_DS09_COMP_TALENT_FLOW` |
| 主落点 | COMPREHENSIVE seq 182 / xlsx 108 |
| 口径 | 见 §1.2 seq 182 逐字抄录 |
| 公式（未签，原文） | 「模型未签。禁止 mapped 157；禁止按号综合 182（成果指数）；禁止改挂 184 人才存量结构。半成品行108 智库=路由启发式，不改 other_system」 |
| 建议 type | MODEL（未签） |
| reuse_of（禁用清单） | 不复用 `M_TALENT_FLOW_TRACK` / seq 157 |
| pending_ref | **Q-MO-DS09-02** |
| §2 消费矩阵 pending | 禁 mapped 157 / 综合 182；禁 also_in TAL-D13 / DS-13～16 |
| 差集保持 | **missing** |
| 落地表 / 读取接口 | `ts_plan_talent_flow`（**仅聚合计数行**：stats 汇总 + institution_flows + records 聚合（from/to 机构级、`person_count` 计数、flow_type 三枚举、risk_level）；**无姓名/证件/个人 ID 列**——U6 在表结构级落实）/ 契约 §3.5 `talent-flow`（`flow_type`/`risk_level` Query；`person_count` 只聚合计数，不返个人明细） |
| UI | 🧪 + ⓘ draft + ⚠️「待甲方确认」（Q-MO-DS09-02 + U6 法务未决） |

### 2.5 `M_INNOV_PLAN_DIRECTION_ALERT` · 潜在科技发展方向预警 —— 赋号草稿 · 类型未签 · 未入 seed

| 字段 | 值 |
|---|---|
| temp_id 对照 | `TEMP_DS09_COMP_DIRECTION_ALERT` |
| 主落点 | COMPREHENSIVE seq 184 |
| 口径 | 见 §1.2 seq 184 逐字抄录 |
| 公式（未签，原文） | 「模型未签。**实现通道可 501 / pending**。05 无方向预警专叶 → **差集保持 missing**，**禁止**因 501 改 mapped。禁止改挂 134/132/138–140；禁止 also_in DS-04-REALTIME seq 71 / DS-07-SCI-CREATE seq 139」 |
| 建议 type | MODEL（未签）；「建议 MODEL 不是 501 覆盖证明；差集 missing 保持」（§赋号表原文） |
| reuse_of（禁用清单） | 不复用 134 趋势 / `M_INNOV_IMPACT_FORECAST` |
| pending_ref | —（501 pending，非覆盖证明） |
| §2 消费矩阵 pending | **501 pending**；禁改挂 134；**不改 mapped** |
| 差集保持 | **missing**（501 非覆盖证明，详见 §3） |
| 落地表 / 读取接口 | `ts_plan_direction_warning`（建表，结构对齐契约 §3.1 items + sources 六源 JSON + metric_id 列；**V1 零行，永不灌演示行**）/ 契约 §3.1 `direction-warnings`（模型未注册 → HTTP 501，正常信封不出现；注册后 `items[].metric_id` + `data.metric_ids[]`） |
| UI | 无 🧪（无展示数）；⚠️「预警模型未注册」+ 空态 + 报告导出禁用；**不显伪卡** |

### 2.6 各端点 `metric_id` 字位（契约 §3.1–§3.6）

| 端点（契约 §） | `metric_id` 字位 | 本分册落位（草稿） |
|---|---|---|
| §3.1 `direction-warnings` | `items[].metric_id` + `data.metric_ids[]` | `M_INNOV_PLAN_DIRECTION_ALERT`（未注册 → 501，正常信封不出现） |
| §3.2 `hot-technologies` | `items[].metric_id` + `data.metric_ids[]` | `M_INNOV_PLAN_HEAT` / `M_INNOV_PLAN_GROWTH` |
| §3.3 `tracking` | `data.metric_ids[]`（契约示例即 `[]`） | 无独立核——契约空数组与核对记录「无独立统计核」逐字一致，不得回填他号 |
| §3.4 `local-advantage` | `data.metric_ids[]` | `M_INNOV_PLAN_LOCAL_ADV` |
| §3.5 `talent-flow` | `data.metric_ids[]` | `M_INNOV_PLAN_TALENT_FLOW` |
| §3.6 `resource-push`（GET/PUT） | 无 `metric_id` 字段 | N/A（订阅壳） |
| 第 9 端点 `metric-system`（G-B2 方案 A，OV-API 分册起草） | 待契约冻结 | N/A（运营壳，无 metric_id） |

**占位符警告**：契约 §3.1/§3.2/§3.4/§3.5 示例中的 `"metric_id": "Q0xx"` 是**字位占位符，不是真 ID**。实现回填用本分册 §2 草稿 ID（回填动作归 OV-API 分册 / 实现单，本分册不代填契约正文）；**不得取 `Q010`～`Q019` / `QPOL-*` 段**——那是展示企业 / 政策口径族，核对记录 §4 明令「本页不改挂、不关闭」。前端另守核对记录 §6：「关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / `501` / 就绪度字样」。

---

## 3. `M_INNOV_PLAN_DIRECTION_ALERT` 501 pending 语义（专节）

**定位：501 是实现通道，不是覆盖证明。**

- **真源原句**（核对记录）：§1「**501 不是覆盖证明。**」；卷首「catalog / 详设 04 写**可 501**（收口 `DS-09-COMPREHENSIVE` seq 184）；**禁止**因此把差集改成 mapped（不伪闭合）」；§4 开放项「seq 184 501｜潜在方向预警可走 501；**未注册本页 ID**｜语义债；**missing + 501 pending**；不伪闭合」。
- **差集 missing 保持**：05 无方向预警专叶 → 差集保持 missing，禁止因 501 改 mapped。模型注册与否**不改变**差集判定，也不改变 §赋号表状态（草稿、未入 seed）。
- **模型注册前（V1 行为，ARCH §4.7）**：
  - 接口 `GET /v1/situation/planning/direction-warnings` 按**模型注册检测**短路：未注册 → **HTTP 501 + 错误信封**（沿用「Job 未注册则 501」先例，POL PC-4 模式；检测载体 = 配置/字典开关，OV-API 分册定信封与开关名）。
  - `ts_plan_direction_warning` 建表 **V1 零行、永不灌演示行**（「空态不得用假规划正文 / 假预警行填」，ARCH §1 明确不做项 #5）。
  - 前端（G-B6）：预警区空态 + ⚠️「预警模型未注册」；`source_averages` 六源均分为**空集**（服务端语义，前端不自算）；报告导出走 M1 §3.8 任务中心 `content_key=planning-direction-warning`，模型未注册时**导出入口禁用**。
- **模型注册后（未来）**：由 Python（`M_INNOV_PLAN_DIRECTION_ALERT` 实现方）写 `ts_plan_direction_warning`，接口读表返回；届时 `source_averages`「由服务端按当前可见 `items` 计算（对齐 demo L1331–L1337），前端不自算」（契约 §3.1 边界原文）。
- **501 纪律**（核对记录 §3.1 原文）：「只给 seq 184 一条实现通道注释。未注册本页正式 ID。不把 DS-03 跟踪、DS-07 趋势预测、REALTIME seq 71、seq 182–191 当已覆盖。捕捉/跟踪的 134 **趋势输出不得改挂本预警叶**。」
- **范围限定**（核对记录 §5 原文）：「仅 COMPREHENSIVE seq 184 可走 501 实现通道；**未注册 metric_id**；差集 **missing**。父句预测可视化已收口 134，**不得**借 501 伪覆盖捕捉/跟踪。RESEARCH / KEY-DOMAIN **不得**进 501。KEY-DOMAIN seq 190 模拟预测 = 建议壳，不是 501。」

---

## 4. 禁改挂清单（Java / FE 实现单防误用）

整理自核对记录 §赋号表 reuse_of 列 + 尾注、§1.1「禁止」列、§2 pending 列、§3.1 公式列与 N/A 表、§5「本叶不做」、§6。**本清单为收口视图，语义以核对记录原文为准。**

### 4.1 reuse=0：既有正式 ID 一律不复用（§赋号表 reuse_of 列）

| 本页草稿 ID | 禁复用对象 |
|---|---|
| `M_INNOV_PLAN_HEAT` | `M_TECH_HEAT_INDEX` / `M_TECH_TOPIC_HEAT` |
| `M_INNOV_PLAN_GROWTH` | `M_INNOV_FACTOR_GROWTH` / 专题热度同核 |
| `M_INNOV_PLAN_LOCAL_ADV` | `M_CHAIN_SZ_ADVANTAGE_*`（含 `M_CHAIN_SZ_ADVANTAGE_RANK`）/ 186 |
| `M_INNOV_PLAN_TALENT_FLOW` | `M_TALENT_FLOW_TRACK` / seq 157 |
| `M_INNOV_PLAN_DIRECTION_ALERT` | 134 趋势 / `M_INNOV_IMPACT_FORECAST` |

§赋号表尾注：「Wave A `M_TECH_HEAT_INDEX` / `M_TALENT_FLOW_TRACK` / `M_INNOV_GBA_CAPACITY_INDEX` 等不同口径，不 reuse。」

### 4.2 形近 ID 一律不消费（撞号核查结论，§赋号表尾注）

`M_CHAIN_HOTSPOT_*` / `M_CHAIN_COMPETITIVENESS_INDEX` / `M_CHAIN_SZ_ADVANTAGE_*` / `M_ENT_COMPETITIVENESS_*` / `M_SYNTH_VIT_*`

### 4.3 序号 / 口径禁改挂（§1.1 禁止列 + §3.1 公式列 + N/A 表）

- 按号 mapped 综合 182/184；硬挂 186 当本地优势；mapped 157 当人才流动；把 134 趋势 / 501 改挂 seq 184（§1.1 COMPREHENSIVE「禁止」列）
- 135（产业化潜力）/ 132（历程）顶替热度；增速改挂 seq 184 预警（HEAT / GROWTH 公式列）
- LOCAL_ADV：硬挂 186 / 按号 182 / 133 / 140 / 159 / 187
- TALENT_FLOW：按号综合 182（成果指数）；改挂 184 人才存量结构
- DIRECTION_ALERT：改挂 134 / 132 / 138–140
- 179 运营壳：硬挂 186–190；180：硬挂 133（空间分布）；183：`M_SVC_REC_*` / seq 164

### 4.4 also_in 禁入（§1.1 + §3.1）

DS-03 跟踪 / DS-07 评估 / DS-07-SCI-CREATE seq 139 / DS-04-REALTIME seq 71 / TOPIC-TECH / TOPIC-TALENT / SYNTH / TAL-D13 / DS-13～16

### 4.5 UI 禁点伪 8 件套（§6）

统计数 ⓘ MetricSpecCard 只回指核对记录 §赋号表 `M_INNOV_*`（TEMP_ 对照）；**禁止**点开 `M_CHAIN_*` / `M_SVC_*` / `M_SYNTH_*` / `M_ENT_*` / `M_TALENT_*` / `M_SYNTH_COLLAB_*`

### 4.6 禁止发明的新 ID 形态（§5「本叶不做」原文清单）

`M_PLAN_*` / `M_HOTSPOT_*` / `M_LOCAL_ADV_*` / `M_TALENT_FLOW_*` / `M_DIRECTION_ALERT_*` / `M_OVERLAP_*` / `M_CI_*` / `M_KEYDOMAIN_*` / `M_SPATIAL_*`

### 4.7 Q 段保护（§4）

`Q010`～`Q019` / `QPOL-*`（展示企业 / 政策口径族）与 `Q-TINDEX-01`（DS-08 智库指数）：本页不改挂、不关闭；不得把 `Q-TINDEX-01` 写进 `/display` 规划 DOM（§6）；契约占位 `"Q0xx"` 回填不得取该段（见 §2.6）。

---

## 5. 未决项与 UI ⚠️「待甲方确认」角标对应

| 未决项 | 内容（真源） | 涉及叶 / 指标 | UI ⚠️ 对应 |
|---|---|---|---|
| **U5** | 热度构成权重 40/30/20/10 为规划口径（ALGO 参考），**待 M0 定稿**。契约 §3.2：`caliber_note` 必返「热度 = 论文 40% / 专利 30% / 项目 20% / 资讯 10%（口径待 M0 定稿，U5）」；ARCH：文案由表行携带而非 Java 硬编码 | 178 · HEAT / GROWTH | 热度/增速统计数旁 ⚠️「待甲方确认」（「维名/权重/501 未冻：⚠️『待甲方确认』（文案走 COMP/KEYD/RES-B*）」，核对记录 §6；本页走 COMP-B02），与 🧪、ⓘ draft 并存 |
| **U6** | `person_count` 涉及个人信息 → **只聚合计数，不返个人明细**（合规，U6；契约 §3.5）；表结构级落实：只存聚合计数行、无姓名/证件/个人 ID 列；FE 写死 18932/12458 不得当正式数（G-B4） | 182 · TALENT_FLOW | 人才流动区 ⚠️「待甲方确认」（Q-MO-DS09-02 + U6 法务未决，ARCH §4.5） |

附注：U4（`delta` 字符串百分比数值化待 M0）、U7（`frequency` 枚举 `realtime`/`daily`/`weekly` 待 M0 产品侧）已由 ARCH §7 消费，属接口 / 产品面，不产生本分册指标语义与角标，不在本分册展开。

---

## 6. 纪律声明

1. **不写 seed**：本分册不写 `metrics/registry/` seed / 矩阵 / 任何 `cfg_metric-*-seed.yaml`；13 条 `M_INNOV_*`（含本页 5 条 `M_INNOV_PLAN_*`）均为赋号草稿、**未入 seed**，seed 侧零改动（核对记录 §5「本叶不做」原文：「不写任何 `cfg_metric-*-seed.yaml`」）。
2. **不改 `algorithm_type`**：MIXED / MODEL 均为核对记录草稿建议、未签；公式与 `algorithm_type` 一律 `pending_cosign: human:唐绍祖`，本分册不签、不改 seed 既有类型。
3. **不改差集判定**：7/7 库缺口 missing 行保持 missing（本页涉及 181/182/184 三条）；third_party 134 / n/a_ops / mapped 判定不动；501 非覆盖证明、不伪闭合（§3）。
4. **指标查询纪律**：对既有指标身份只经 metric-registry MCP（`metric-get` / `metric-query`）查询，不整文件读 seed、不自行撞号判定；本分册为定义稿、未发起新查询，撞号结论沿用核对记录 §赋号表「13 个拟号全部 miss」（其核查经 `metric-registry-lib` / MCP）。
5. **不发明 `M_*`、不改 task-registry、不 git 提交**：本分册只写本文件一个，口径全部逐字抄录核对记录，不改写语义。

---

**会签路径**：同 ARCH §9——四角色会签（意见落 `sdd/l2/会签/综合发展规划-会签.md`）→ 全部同意后由 `actor=human:淮政玮` 签收；公式与 `algorithm_type` 的签署另行走 `pending_cosign: human:唐绍祖`（核对记录 §8 签署区），不在本分册闭合。

---

## 会签修订记录 v2

- **日期**：2026-11-06 · **触发**：四角色会签（architect / api / algorithm 三家已审：同意，必改一处）
- **裁定**（algorithm 会签人）：§1.1 总表 seq 180 的 D3 记法由「不伪 full」改为「**n/a（无指标行，随宿主 HEAT/GROWTH，D3=不伪 full）**」——180 叶无独立指标行，防误读为叶级 D3 判定；其宿主 HEAT/GROWTH 两指标的 D3 仍按「不伪 full」记（§1.1 通用注不变）。
- **变更范围**：仅 §1.1 总表 180 行 D3 单元格 + 本记录小节；其余内容（口径逐字抄录、明细卡、§3 501 语义、§4 禁改挂清单、§5 未决项、§6 纪律声明）零改动。
