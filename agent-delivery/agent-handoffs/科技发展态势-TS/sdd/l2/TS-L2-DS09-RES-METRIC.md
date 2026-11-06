# TS-L2-DS09-RES-METRIC · 研究领域分析 · 后台指标设计

> **任务**：`TS-L2-DS09-RES-METRIC`（definition，不写业务代码、不改 metrics seed、不发明 `M_*`）
> **日期**：2026-11-06 · **作者**：agent:zcode 会话代跑 algorithm-agent · **监管**：`human:王梓真`
> **状态**：草案待会签（architect / api / algorithm / data，意见落 `sdd/l2/会签/研究领域分析-会签.md`）
> **公式与 `algorithm_type` 一律 `pending_cosign: human:唐绍祖`，本分册不签**

**输入真源**

| 用途 | 真源 |
|---|---|
| 指标唯一真源（本分册一切口径逐字抄录自此） | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-09-科技发展规划-核对记录.md`（§赋号表 4 条 RES TEMP→`M_INNOV_RES_*`、§2 消费矩阵、§3.2 RESEARCH 页语义卡与「本页 ④ 不适用」、§1.1 禁止列、§1.2 差集、§4 开放项 RES-B01..B03） |
| 硬依赖架构稿 | `agent-handoffs/科技发展态势-TS/sdd/l2/TS-L2-DS09-RES-ARCH.md`（D18 逐叶判定 11 表 68 行、§0 结论速览、§4 逐叶架构、§5 契约差异收口、§7.2 U3 阈值建议、§7.4 禁改挂清单） |
| 契约草案（批 4 未冻结） | `agent-handoffs/科技发展态势-TS/API-TS-M9.md` §3.8 `research-analysis`（`metric_id` 字位：`fields[].metric_id` / `competing_enterprises[].metric_id` / `data.metric_ids[]`；U3 四档逐字标签与阈值） |
| 兄弟分册模板 | `sdd/l2/TS-L2-DS09-OV-METRIC.md` / `TS-L2-DS09-KEY-METRIC.md`（逐叶判定表 / 明细卡 / 纪律专节同构） |
| 需规 6 叶 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技发展规划.md` seq 191–196（L200–L289；六叶 bid_desc 均空、沿用 excel_row 181 继承句） |

**范围**：DS-09 `DS-09-RESEARCH` 页（研究领域分析页签 Tab3，FE-TS-09c）6 叶（seq 191–196）的后台指标设计：逐叶指标判定表、4 条 `M_INNOV_RES_*` 明细卡、端点 `metric_id` 字位、U3 四档阈值与标签字典落位、纪律专节、纪律声明。COMPREHENSIVE 5 条 `M_INNOV_PLAN_*`（OV-METRIC 分册）与 KEY-DOMAIN 4 条 `M_INNOV_KEYD_*`（KEY-METRIC 分册）不在本分册展开，仅在 §4 禁改挂专节整表收口。**口径一律逐字抄录核对记录，不改写语义。**

---

## 1. 逐叶指标判定表（6 叶）

### 1.1 总表

| seq | 叶 | metric_id（草稿） | 中文名 | 公式状态 | algorithm_type 建议（未签） | D1 | D3 | D4 | UI 角标要求 |
|---|---|---|---|---|---|---|---|---|---|
| 191 | 研究领域重叠度分析 | `M_INNOV_RES_OVERLAP` | 研究领域重叠度 | 未签（`pending_cosign: human:唐绍祖`；模型未签，05 无重叠度专叶） | MODEL | draft（未入 seed） | 不伪 full | D18 表读数 = mock（6 真值对 demo 冻结种子，9 对诚实空） | 🧪 MockBadge + 统计数 ⓘ draft 语义卡 + ⚠️「待甲方确认」（类型未签；文案走 RES-B02；G-B4 哈希演示算法替换，无真值对显空「—（暂无重叠数据）」） |
| 192 | 研究领域等级划分 | `M_INNOV_RES_GRADE` | 研究领域等级划分 | 未签（`pending_cosign: human:唐绍祖`） | MODEL | draft（未入 seed） | 不伪 full | D18 表读数 = mock（4 档卡 + 5 领域字典 demo 种子表行化） | 🧪 + 统计数 ⓘ draft 语义卡（Q-MO-DS09-03）+ ⚠️「待甲方确认」（四档阈值 U3 建议值 80/65/45 未拍板，未拍板前列灌建议值并标 draft） |
| 193 | 多企业竞争情报比对 | `M_INNOV_RES_CI_LEVEL` / `M_INNOV_RES_CI_COMPARE` | 竞争情报等级 / 多企业竞争情报比对 | 未签（`pending_cosign: human:唐绍祖`；两条均未签） | MODEL / MIXED | draft（未入 seed） | 不伪 full | D18 表读数 = mock（六企 level_tag + 6 真值对；均值 = Java 表行确定性现算，非 mock 非模型） | 🧪 + 统计数 ⓘ draft 语义卡 + ⚠️「待甲方确认」（类型未签；CI_LEVEL 亦挂 Q-MO-DS09-03；文案走 RES-B02） |
| 194 | 研究领域知识图谱展示 | 无（mapped 116，无独立核，依据见 §1.2） | — | N/A | N/A | N/A（无指标行，不另造 TEMP_） | n/a（mapped 116 无独立统计核，无指标行） | 演示骨架读数 = mock（14 节点 / 13 星型边 demo 种子；专家类节点需规提及、种子无，诚实缺位） | 🧪（演示骨架）；无 metric_id → 不挂 ⓘ 语义卡、计数旁不显伪 8 件套、`metric_ids` 不收录；评审模式 DOM 零泄漏 |
| 195 | 竞争情报分析报告 | 无（N/A other_system，依据见 §1.2） | — | N/A | N/A | N/A（无指标行） | n/a（报告读面/导出，无指标行） | D18 表读数 = mock（4 行情报 + 6 行模板 demo 逐字，非生成物） | 🧪（演示行）；无 metric_id（表行 `metric_id` 列 NULL）→ 不挂 ⓘ、不显伪卡；**禁因重叠度 missing 把报告改打 missing**（§4.2）；导出禁用只随 501 纪律面，不随 missing |
| 196 | 企业发展战略建议 | 无（N/A other_system 建议读面，依据见 §1.2） | — | N/A | N/A | N/A（无指标行） | n/a（建议读面，无指标行；派生块消费 195/KEY 组既有表行） | 派生行 = 既有表行 demo 逐字（insight 行扩列 + benchmark 行 + KEY 组方案行，非生成物）→ 读数仍 mock | 🧪（派生演示行）；无 metric_id（不进 `metric_ids`）→ 不挂 ⓘ、不显伪卡；建议读面纪律见 §4.3；方案模拟 = FE Modal 交互壳，非 501 |

**D1 / D3 / D4 通用注**（适用全表）：

- **D1**：4 条 kit 指标口径草稿已认（语义 Owner `human:淮政玮`），公式 / `algorithm_type` 未签，未入 seed → 按核对记录 §6「TEMP_ 未入 seed：D1 按 `missing`/`draft` 诚实」，本分册记 **draft**；从注册表视角该 ID 不存在（missing），不伪称已定义完。
- **D3**：A1 双表未交 → **不伪 `full`**；8 件套草稿源表只到「ADS/ES display」层级（V1 实读 = D18 `ts_plan_research_*` 11 表 68 行），不把项目 DWD 反推成 ODS `full`，「V1 看板字段走 display ADS，不自动等于 mapped 05」（核对记录 §5）。
- **D4**：D18 铁律——表读数是 demo 冻结种子灌数、非真算 → **D4 仍 mock**，🧪 MockBadge 保留至 D4 翻转（ARCH G-B5 沿袭）；194 / 195 / 196 无 metric 行不挂 D4 维，但演示骨架 / 情报行 / 派生文案仍属 mock 读数；193 象限散点均值为 Java 表行确定性现算（非 mock 非模型），其**输入**仍为 mock 表行。

### 1.2 口径与 N/A 依据（核对记录 §3.2 逐字抄录）

**§3.2 头部原句**：

> 「本页是企业研究领域分析读面，不是 SYNTH-COLLAB 协同工作台。501 预警 **不进本页**。」

**seq 191（口径列原文）**：

> 「基于企业－专家－学术文献－研究关键词知识图谱，衡量**两家企业**在研究领域上的重叠程度，产出计算结果与可视化。对象≠ 05 seq 191 区域创新协同（完整度/中心度/密度 → 区域协同指数）；≠ 116 两实体通用语义相似度」（OVERLAP）

**seq 192（口径列原文）**：

> 「对重叠度做量化等级划分；可查看标准与结果，支持自定义阈值。阈值是同一缺口的参数面，不另开 missing」（GRADE）

**xlsx 107（口径列原文）**：

> 「半成品独立主项：用量化指标对重叠度划分等级，反映企业间竞争情报强弱（等级/分值）。与 GRADE 同族，比对交互归 COMPARE」（CI_LEVEL）

**seq 193（口径列原文）**：

> 「比对多家企业竞争情报等级，产出**竞争矩阵与战略定位图**。企业维 11 叶均对不上该输出（141=深圳 vs 全国竞争力；145 对标=技术力；146 跨企业=商业力）」（CI_COMPARE）

**seq 194（§3.2 表后正文原文）**：

> 「知识图谱展示（seq 194）= mapped seq 116 实体检索 / 关系查询 / 可视化；**④ 无独立统计核**（不另造 TEMP_）。禁止用 116 语义相似度或网络密度/中心度顶替重叠度。禁止改挂 108/109。禁止 `M_SVC_GRAPH_*`。禁止抢 DS-21/DS-23。」

**seq 195 / 196 · N/A 依据**（核对记录 §3.2「本页 ④ 不适用」原文条目；194 行一并收录）：

> 「研究领域知识图谱展示（seq 194）｜mapped｜无独立 metric_id；116 展示/查询 API 不覆盖重叠度」
>
> 「竞争情报分析报告（seq 195）｜other_system｜报告读面/导出；禁止因重叠度 missing 把报告改打 missing；禁止 n/a_ops」
>
> 「企业发展战略建议（seq 196）｜other_system｜建议读面（技术路线/资源配置/合作机会 + 方案模拟壳）；禁止 missing 模拟模型；禁止硬挂 147/148；不编制规划文本」

差集对照（核对记录 §1.2 原文行）：191 **missing** · kit / 192 **missing** · kit / 193 **missing** · kit / 194 **mapped** seq 116 · 无独立核 / 195 other_system · N/A（报告读面/导出）/ 196 other_system · N/A（建议读面；不编制规划文本）；「半成品 xlsx 行107「竞争情报等级」= RESEARCH 额外 missing 行（RES-D03），④ 出 `TEMP_DS09_RES_CI_LEVEL`」；「**7/7 库缺口 missing 行保持 missing**（综合 3 + 研究 4；KEY-DOMAIN A=0）」——本分册不改任何判定（禁 n/a_ops 也不许：195/196 已判 other_system，ARCH §1 不做项 #8）。

---

## 2. `M_INNOV_RES_*` 四条明细卡

> 全部为**赋号草稿 · 类型未签 · 未入 seed**（核对记录 §赋号表 2026-08-22；协议 `METRIC-ID-ASSIGN-LOOP-循环工程.md`，ELEMENT=`INNOV`，reuse=0；真源机器卡全部 `TEMP_DS09_*`（COMP 5 + RES 4 + KEYD 4），13 条赋号里 RES 占 4：MODEL 3 · MIXED 1）。8 件套草稿公共字段（TEMP_ 共同，核对记录 §3 原文）：「源系统=科技信息展示系统·科技发展规划 / display；更新频率=未定；version=`draft-open-ds09`；源表=ADS/ES display（A1 表2 未交 → 本叶不填伪 full）。`algorithm_type` 为建议、未签。」Q-MO-DS09-03 登记于 `metrics/request/_work/id-assign/DS-09-METRIC-OPEN-L01-questions.yaml`（核对记录 §7 产物清单；本分册不读不改）。

### 2.1 `M_INNOV_RES_OVERLAP` · 研究领域重叠度 —— 赋号草稿 · 类型未签 · 未入 seed

| 字段 | 值（真源：核对记录 §赋号表 / §2 / §3.2） |
|---|---|
| temp_id 对照 | `TEMP_DS09_RES_OVERLAP` |
| 主落点 | RESEARCH seq 191 / xlsx 106 |
| 口径 | 见 §1.2 seq 191 逐字抄录 |
| 公式（未签，原文） | 「模型未签；05 无重叠度专叶。禁止 also_in `M_SYNTH_COLLAB_OUTPUT_CORR`」 |
| 建议 type | MODEL（未签） |
| reuse_of（禁用清单，§赋号表逐字） | 不复用 seq 191 / 116 / `M_SYNTH_COLLAB_*` |
| pending_ref | —（语义债 RES-B02：重叠度 / 等级 / 比对 / 图谱展示无正式 metric_id，库缺口 RES-D01..D04 保持 missing；撞号对照纪律 RES-B03，见 §4.5） |
| §2 消费矩阵 pending | RES-B03；禁按号 05 seq 191；禁 116 相似度 |
| 差集保持 | **missing** |
| 落地表 / 读取接口 | `ts_plan_research_overlap`（6 行真值对，值域 45–72，`metric_id`=本号；六企 C(6,2)=15 对中 9 对无种子真值**不灌行、不造数**，V1 诚实空）+ `ts_plan_research_company`（7 行，`level_tag` 列挂 CI_LEVEL）/ `overlap_rule`（3 档）/ `time_factor`（3 行复算系数）/ `overlap_benchmark`（3 行对标读数；`metric_id` 列落位随 RES-DATA 分册 DDL 冻结，本分册建议挂本号草稿）/ 契约 §3.8 `research-analysis`（companies / overlap_matrix / overlap_rules / time_scopes / overlap_benchmarks 块）。G-B4：FE `getDeterministicOverlap` 名称哈希兜底在接线单移除，无真值对显空「—（暂无重叠数据）」；复算口径（领域匹配 ×1.08/×0.96、时间系数）保留 FE 拼装层确定性计算，系数与阈值全部表行下发 |
| UI | 🧪 + 统计数 ⓘ draft 语义卡（回指核对记录 §赋号表，不显伪 8 件套）+ ⚠️「待甲方确认」（类型未签，文案走 RES-B02；重叠值旁不显伪数，空对显「—」） |

### 2.2 `M_INNOV_RES_GRADE` · 研究领域等级划分 —— 赋号草稿 · 类型未签 · 未入 seed

| 字段 | 值 |
|---|---|
| temp_id 对照 | `TEMP_DS09_RES_GRADE` |
| 主落点 | RESEARCH seq 192 |
| 口径 | 见 §1.2 seq 192 逐字抄录（含「阈值是同一缺口的参数面，不另开 missing」——U3 落位依据，见 §3） |
| 公式（未签，原文） | 「未签。禁止 mapped 141/145/146 竞争力/技术力/商业力分档」 |
| 建议 type | MODEL（未签） |
| reuse_of（禁用清单，§赋号表逐字） | 不复用 141/145/146 |
| pending_ref | **Q-MO-DS09-03** |
| §2 消费矩阵 pending | 禁 mapped 141/145/146 |
| 差集保持 | **missing** |
| 落地表 / 读取接口 | `ts_plan_research_grade`（4 行逐字：lead 领先级 92 / advantage 优势级 76 / catching 追赶级 58 / potential 潜力级 34；列含 `threshold_low`（U3 建议值 80/65/45/0，未拍板前列灌建议值并标 draft）/ patent / papers / top_papers / score / `metric_id`=本号）+ `ts_plan_research_field`（5 行领域字典：人工智能/量子科技/合成生物学/集成电路/新能源，191/192 筛选项表行化，无统计核不挂号）/ 同端点（level_cards + fields 块）。「自定义阈值」V1 = 三档规则预设下拉读面承载（ARCH §1 不做项 #9），写面待 M0 |
| UI | 🧪 + 统计数 ⓘ draft 语义卡（Q-MO-DS09-03）+ ⚠️「待甲方确认」（四档阈值 U3 建议值未拍板，见 §3） |

### 2.3 `M_INNOV_RES_CI_LEVEL` · 竞争情报等级 —— 赋号草稿 · 类型未签 · 未入 seed

| 字段 | 值 |
|---|---|
| temp_id 对照 | `TEMP_DS09_RES_CI_LEVEL` |
| 主落点 | RESEARCH xlsx 107（**半成品 xlsx 独立主项**：核对记录 §1.2 原文「半成品 xlsx 行107「竞争情报等级」= RESEARCH 额外 missing 行（RES-D03），④ 出 `TEMP_DS09_RES_CI_LEVEL`」——与 GRADE **分核不合并**，§赋号表 reuse_of 列原文「与 GRADE 分核，不合并」） |
| 口径 | 见 §1.2 xlsx 107 逐字抄录（与 GRADE 同族，比对交互归 COMPARE） |
| 公式（未签，原文） | 「未签。半成品标专题封装，覆盖判定跟算法缺口，不改 other_system」 |
| 建议 type | MODEL（未签） |
| reuse_of（禁用清单，§赋号表逐字） | 与 GRADE 分核，不合并 |
| pending_ref | **Q-MO-DS09-03** |
| §2 消费矩阵 pending | 与 GRADE 同族、半成品独立主项 |
| 差集保持 | **missing**（RES-D03 额外 missing 行，随「7/7 库缺口 missing 保持」一并不动） |
| 落地表 / 读取接口 | `ts_plan_research_company.level_tag` 列（六企行：华为 S / 腾讯 S / 阿里 A / 字节 A / 百度 A / 小米 B；目标主体行 level/color NULL）——193 复用 191 表行，**不新建 193 专用表**（契约 §4 `ts_plan_compete_intel` 弃用，ARCH §5）/ 同端点 companies 块 + competing_enterprises 块（每企 level 字段读该列） |
| UI | 🧪 + 统计数 ⓘ draft 语义卡（Q-MO-DS09-03）+ ⚠️「待甲方确认」（类型未签，文案走 RES-B02）；等级标签由表行下发，Java/FE 不硬编码 |

### 2.4 `M_INNOV_RES_CI_COMPARE` · 多企业竞争情报比对 —— 赋号草稿 · 类型未签 · 未入 seed

| 字段 | 值 |
|---|---|
| temp_id 对照 | `TEMP_DS09_RES_CI_COMPARE` |
| 主落点 | RESEARCH seq 193 |
| 口径 | 见 §1.2 seq 193 逐字抄录（企业维 11 叶均对不上该输出） |
| 公式（未签，原文） | 「未签。禁止 `M_CHAIN_COMPETITIVENESS_INDEX` / `M_ENT_*`。选企壳不另开 missing」 |
| 建议 type | MIXED（未签；MIXED = 表行真值 + 均值计算，ARCH §4.3——象限散点值由 Java 对表行均值**确定性现算**，非 mock 非模型） |
| reuse_of（禁用清单，§赋号表逐字） | 不复用 `M_CHAIN_COMPETITIVENESS_INDEX` / `M_ENT_*` |
| pending_ref | —（语义债 RES-B02） |
| §2 消费矩阵 pending | 禁 `M_CHAIN_COMPETITIVENESS_INDEX` / `M_ENT_*` |
| 差集保持 | **missing** |
| 落地表 / 读取接口 | 复用 191 `ts_plan_research_company`（六企行 level_tag=CI_LEVEL 读数）+ `ts_plan_research_overlap`（6 真值对）+ `overlap_rule`；不新建表；同端点 competing_enterprises 块（每企 avg_overlap + level + 逐对 sourceTag 明细，Java 现算下发；四象限轴线标签「技术深度/商业化能力」与象限名为 FE 既有呈现，不改） |
| UI | 🧪 + 统计数 ⓘ draft 语义卡 + ⚠️「待甲方确认」（类型未签，文案走 RES-B02）；选企壳不另开 missing、不显伪 8 件套 |

### 2.5 端点 `metric_id` 字位（契约 §3.8）

| 端点（契约 §） | `metric_id` 字位（草案示例） | 本分册落位（草稿，随 ARCH §5 平铺收口） |
|---|---|---|
| §3.8 `GET /v1/situation/planning/research-analysis` | 示例仅 `fields[].metric_id` / `competing_enterprises[].metric_id` / `data.metric_ids[]`（均为 `"Q0xx"` 占位） | ARCH §5 已裁定响应改**平铺多块**（fields / companies / overlap_matrix / overlap_rules / time_scopes / level_cards / overlap_benchmarks / graph / intelligence_rows / report_export / strategy_advice），`metric_id` 下沉到各块表行——overlap 行=OVERLAP；level_cards 行=GRADE；companies 行 `level_tag`=CI_LEVEL；competing_enterprises 块=CI_LEVEL（企等级行）+ CI_COMPARE（比对块汇总）；fields（领域字典）/ overlap_rules / time_scopes / graph / intelligence_rows / report_export / strategy_advice 无核叶不挂号（表 `metric_id` 列置 NULL 或块不收录，ARCH §6「每表带 `metric_id` 列（无核叶置 NULL）」）；`data.metric_ids[]` 汇总四条 RES 草稿号。新响应示例由 RES-API 分册起草，批 4 冻结时改约（本分册不代填契约正文） |

**契约边界原文消费**（§3.8 边界，逐字）：

> 「`intelligence_level`（竞争情报分级）为算法产物；报告产物走 M1 §3.8 导出任务中心（`report_ref` 引用 `job_id`）。」
>
> 「重叠度 `overlap_score` 口径（ALGO：重叠度分析）待算法侧登记 `metric_id`。」

「待算法侧登记」= 走 id-assign / 公式会签流程（`pending_cosign: human:唐绍祖`，核对记录 §8 签署区），**不是**写 seed；当前落位即 §赋号表草稿号 `M_INNOV_RES_OVERLAP`。`intelligence_level` 的算法产物语义当前由 CI_LEVEL 草稿承载（D4 仍 mock，正式态由 Python 实现方落表——MODEL 计算归唐绍祖监管 Python，核对记录 §6）。

**占位符警告**：契约 §3.8 示例中的 `"metric_id": "Q0xx"` / `"metric_ids": ["Q0xx"]` 是**字位占位符，不是真 ID**。实现回填用本分册 §2 草稿 ID（回填动作归 RES-API 分册 / 实现单）；**不得取 `Q010`～`Q019` / `QPOL-*` 段**——那是展示企业 / 政策口径族，核对记录 §4 明令「本页不改挂、不关闭」。前端另守核对记录 §6：「关闭评审模式 DOM 零泄漏 `metric_id` / `TEMP_` / `Q-*` / `501` / 就绪度字样」。

---

## 3. U3 落位：四档阈值与标签字典（GRADE 缺口的参数面）

**定位：阈值是 GRADE 同一缺口的参数面，不另开 missing、不新造 TEMP_/`M_*`。**

- **真源原句**（核对记录 §3.2 GRADE 行口径列原文）：「对重叠度做量化等级划分；可查看标准与结果，支持自定义阈值。阈值是同一缺口的参数面，不另开 missing」→ 四档阈值属于 `M_INNOV_RES_GRADE` 缺口自身的参数面，**不另开 missing**、不因「阈值未拍板」新增差集行或新草稿号。
- **U3 归属**（契约 §5 原文行）：「U3｜`research_grade` 四档逐字标签与阈值｜M0 + 算法侧」。ARCH §7.2 给建议值：对 0–100 重叠度分制四档 `threshold_low` = **领先级 ≥80 · 优势级 ≥65 · 追赶级 ≥45 · 潜力级 <45**（落表 80/65/45/0）。依据：种子吻合——benchmark 三行 82（华为）→领先、67（腾讯）→优势、48（大疆）→追赶；与 balanced 规则三档（high≥70 / medium≥55 / low<55）量级兼容；与 overlapMatrix 值域 45–72 相容（72→优势级顶部，不误入领先）。**未拍板前列灌建议值并标 draft**（ARCH §4.2），UI 配 ⚠️「待甲方确认」。
- **标签字典后端下发**：四档逐字标签（领先级 lead / 优势级 advantage / 追赶级 catching / 潜力级 potential，四卡带 description/patent/papers/topPapers/score 92/76/58/34）由 `ts_plan_research_grade` 字典行下发，**Java / FE 不硬编码**（D18）；表行 `metric_id` 挂 GRADE 草稿号。
- **并存不合并**：四档等级阈值（U3）与三档规则阈值（strict/balanced/wide 的 75/60/59、70/55/54、65/50/49，逐字表行下发）**并存不合并**——前者是等级划分标准、后者是 191 重叠复算档位（ARCH §7.2）；「自定义阈值」V1 = 三档预设下拉读面承载，写面待 M0（ARCH §1 不做项 #9）。
- **拍板后动作**：M0 + 算法侧拍板 → RES-DATA 分册更新 `ts_plan_research_grade.threshold_low` 灌数值并去 draft 标注；公式与 `algorithm_type` 签署另行走 `pending_cosign: human:唐绍祖`，不在本分册闭合。

---

## 4. 纪律专节（硬边界，随稿冻结）

### 4.1 本页禁 501

- **真源原句**：核对记录 §3.2 头部「501 预警 **不进本页**」；§1.1 禁止列末项「501 进本页」；§5「仅 COMPREHENSIVE seq 184 可走 501 实现通道；**未注册 metric_id**；差集 **missing**。……RESEARCH / KEY-DOMAIN **不得**进 501。」
- **落地**（ARCH §1 不做项 #1）：catalog 501 通道只给 COMPREHENSIVE seq 184；RESEARCH **任何叶**（191–196）不得进 501，也不得借「模型未注册」造空态话术；195 报告不因任何模型未注册而禁用（V1 静态模板行）；接口无 501 分支。184 的 501 通道**不外溢**到本页。

### 4.2 seq 195 报告纪律：禁因重叠度 missing 改打 missing

- **真源原句**（核对记录 §3.2「本页 ④ 不适用」195 行，逐字见 §1.2）：「报告读面/导出；禁止因重叠度 missing 把报告改打 missing；禁止 n/a_ops」。
- **落地**（ARCH §4.5）：`ts_plan_research_insight`（4 行逐字）+ `ts_plan_research_report_template`（6 行模板，文案表行携带，Java/Python 不硬编码）均为 demo 逐字、非生成物，`metric_id=NULL`；报告**不随** OVERLAP/GRADE/CI_COMPARE 任一条 missing 缺失或禁用；导出统一走 M1 §3.8 任务中心（`content_key=planning-research-intelligence`（建议值），`report_ref` 引用 `job_id`；PDF 沿浏览器打印），不另造下载通道；LLM 润色（DN-A11-03）待甲方，本页不含生成面。

### 4.3 seq 196 建议读面 N/A 纪律

- **真源原句**（核对记录 §3.2「本页 ④ 不适用」196 行，逐字见 §1.2）：「建议读面（技术路线/资源配置/合作机会 + 方案模拟壳）；禁止 missing 模拟模型；禁止硬挂 147/148；不编制规划文本」。
- **落地**（ARCH §4.6 / §7.1，G-B3 方案 A 待会签）：无新表、无独立端点；并入 §3.8 响应 `strategy_advice` 派生块（`insight.plan_id` 扩列承载 demo `resolveStrategyPlan` 映射，高→方案A / 含「追赶」→方案B / 否则→方案C）；三节文案由 FE 按 report_template 建议节模板 + 既有表行渲染（insight 行 / benchmark 行 / KEY 组 `ts_plan_key_area_plan` 跨组只读引用），**不编制规划文本**；方案模拟 Modal = FE 交互壳（同 KEY 190 性质，非 501）；不进 `metric_ids`、表行无核列置 NULL。

### 4.4 seq 194 图谱纪律：禁 116 顶替、禁抢 DS-21/23

- **真源原句**（核对记录 §3.2 表后正文 + N/A 表，逐字见 §1.2）：「禁止用 116 语义相似度或网络密度/中心度顶替重叠度。禁止改挂 108/109。禁止 `M_SVC_GRAPH_*`。禁止抢 DS-21/DS-23。」「无独立 metric_id；116 展示/查询 API 不覆盖重叠度」。
- **落地**（ARCH §4.4）：V1 演示骨架 14 节点 / 13 星型边落表（星型边逻辑从 FE builder 落表，Java 不硬编码拓扑；专家类节点需规提及、种子无，留位不灌、诚实缺位）；`metric_ids` 不收录、计数旁不显伪 8 件套；U9 降级（节点 ≤100 或边 ≤300，超限 graph 块只返 `truncated` 元信息指向 M2 §3.1，不在本接口内嵌全量图）属接口面，归 ARCH §7.3 / RES-API 分册，本分册无指标语义牵涉。

### 4.5 撞号 RES-B03 与全族禁改挂

- **RES-B03 原文**（核对记录 §4 开放项表）：「展示 seq 191 与 05 seq 191 编号撞车｜对照纪律；禁止按号 mapped」。展示 seq 191（重叠度）≠ 05 综合 seq 191（区域创新协同：完整度/中心度/密度 → 区域协同指数，OVERLAP 口径原文对象句），**禁按号 mapped**；亦 ≠ 116 两实体通用语义相似度。
- **§1.1 禁止列全文**（RESEARCH 行原文）：「按号 mapped 05 seq 191；116 语义相似度顶替重叠度；mapped 141/145/146；`M_SYNTH_COLLAB_*` / `M_SVC_GRAPH_*` / `M_ENT_*`；501 进本页」。
- **reuse=0 收口**（§赋号表 reuse_of 列逐字，明细见 §2 各卡）：OVERLAP 不复用 seq 191 / 116 / `M_SYNTH_COLLAB_*`；GRADE 不复用 141/145/146；CI_LEVEL 与 GRADE 分核不合并；CI_COMPARE 不复用 `M_CHAIN_COMPETITIVENESS_INDEX` / `M_ENT_*`。
- **形近 ID 一律不消费**（§赋号表尾注原文）：「形近 `M_CHAIN_HOTSPOT_*` / `M_CHAIN_COMPETITIVENESS_INDEX` / `M_CHAIN_SZ_ADVANTAGE_*` / `M_ENT_COMPETITIVENESS_*` / `M_SYNTH_VIT_*` 一律不消费。」（本页直接相关：`M_CHAIN_COMPETITIVENESS_INDEX` / `M_ENT_COMPETITIVENESS_*`）。撞号核查结论沿用核对记录「13 个拟号全部 miss」（经 `metric-registry-lib` / MCP，未整文件读 seed）。
- **196 硬挂禁令**：禁硬挂 147/148（§3.2 N/A 表原文）。
- **全族 / 跨 DS 禁挂**（核对记录 §5「本叶不做」+ ARCH §7.4）：不改挂 B 轨 / SYNTH / CHAIN / SVC / ENT / TECH 全族；禁 `M_SYNTH_COLLAB_*` / `M_SVC_GRAPH_*` / `M_SYNTH_VIT_*`；不混写 DS-03 / DS-07 / 专题 TALENT；禁湾区 DS-05、深圳 DS-06、DS-07、DS-08 混挂；不把报告/建议打 missing 或 n/a_ops。
- **UI 禁点伪 8 件套**（核对记录 §6）：统计数 ⓘ MetricSpecCard 只回指核对记录 §赋号表 `M_INNOV_*`（TEMP_ 对照）；**禁止**点开 `M_CHAIN_*` / `M_SVC_*` / `M_SYNTH_*` / `M_ENT_*` / `M_TALENT_*` / `M_SYNTH_COLLAB_*` 伪 8 件套。
- **禁发明新 ID 形态**（核对记录 §5「本叶不做」原文清单，RES 相关加粗）：「不发明 `M_PLAN_*` / `M_HOTSPOT_*` / `M_LOCAL_ADV_*` / `M_TALENT_FLOW_*` / `M_DIRECTION_ALERT_*` / **`M_OVERLAP_*`** / **`M_CI_*`** / `M_KEYDOMAIN_*` / `M_SPATIAL_*`」。
- **Q 段保护**（§4）：`Q010`～`Q019` / `QPOL-*` 与 `Q-TINDEX-01` 本页不改挂、不关闭；契约占位 `"Q0xx"` 回填不得取该段（§2.5）。

**语义债沿袭**（核对记录 §4，不升 🟢）：RES-B01（本页无四件套 / TRACE，文件级闭合；不发明 `M_*`）/ RES-B02（重叠度 / 等级 / 比对 / 图谱展示无正式 metric_id；库缺口 RES-D01..D04 保持 missing）/ RES-B03（191 撞号对照纪律）——三项保持，不升 🟢、不关闭、不新建 Q0xx、不改 `客户决策清单跟踪表.md`（ARCH §7.5 同口径）。

---

## 5. 纪律声明

1. **不写 seed**：本分册不写 `metrics/registry/` seed / 矩阵 / 任何 `cfg_metric-*-seed.yaml`；4 条 `M_INNOV_RES_*`（连同全 DS-09 13 条）均为赋号草稿、**未入 seed**，seed 侧零改动（核对记录 §5「本叶不做」原文：「不写任何 `cfg_metric-*-seed.yaml`」；§赋号表：「身份草稿只在本表 + `id-assign/`；**不写 seed / 展示 catalog / 共享 QUESTIONS。**」）。
2. **不改 `algorithm_type`**：MODEL / MIXED 均为核对记录草稿建议、未签；公式与 `algorithm_type` 一律 `pending_cosign: human:唐绍祖`，本分册不签、不改 seed 既有类型。
3. **不改差集判定**：研究 4 missing（191/192/193 + xlsx 107 RES-D03）保持 missing；194 mapped 116、195/196 other_system 保持（禁 n/a_ops 也不许）；「7/7 库缺口 missing 行保持 missing」，不升 🟢、不伪闭合。
4. **指标查询纪律**：对既有指标身份只经 metric-registry MCP（`metric-get` / `metric-query`）查询，不整文件读 seed、不自行撞号判定；本分册为定义稿、未发起新查询，撞号结论沿用核对记录 §赋号表「13 个拟号全部 miss」（其核查经 `metric-registry-lib` / MCP）。
5. **不发明 `M_*`、不改 task-registry、不 git 提交**：本分册只写本文件一个；口径全部逐字抄录核对记录，不改写语义；开放项状态不动（RES-B01..B03 保持）。

---

**会签路径**：同 RES-ARCH §9——四角色会签（architect / api / algorithm / data，意见落 `sdd/l2/会签/研究领域分析-会签.md`）→ 全部同意后由 `actor=human:淮政玮` 签收；公式与 `algorithm_type` 的签署另行走 `pending_cosign: human:唐绍祖`（核对记录 §8 签署区），不在本分册闭合。
