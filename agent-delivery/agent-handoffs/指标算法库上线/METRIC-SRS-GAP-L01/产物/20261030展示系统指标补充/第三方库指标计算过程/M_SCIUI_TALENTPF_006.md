# 研究领域热度值·关注/产出活跃度（M_SCIUI_TALENTPF_006）

> **类型**：无业务逻辑数值类（领域热度条）｜ **域**：科技信息展示系统·重点科技人才画像·学术影响力量化（引进参考）｜ **UI 挂载**：科技信息展示系统 → 重点科技人才画像 → 人才画像总览 → `ProfileBasicPanel.jsx:373`（学术影响力量化卡 influence-bars 末行「领域热度」条，取值 `Math.round(academicInfluence.fieldHotness×100)`，0-100 整数）
> **数据支持度**：**完全转换支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径；「热度值（关注/产出活跃度）」为派单书定名双口径，合成算式待裁）｜ **口径归属**：需求明列行为叶（主需求 :2290-2292 动态热点标记「对近期高频关注领域和最新研究热点进行自动高亮标记」——「研究热点」明列；「热度值」数值定名三份真源 0 命中），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TALENTPF_006.py`｜ **产物**：`code/M_SCIUI_TALENTPF_006_out.json`
> **四判定摘要**：直接结构 = 无（「学者×领域热度值」现成分三源均无）；直接数据 = 无（同左）；依赖结构 = 是（久新领域年度面 + emerging_topic 全套热度面 + 潜力面主领域绑定链三层结构在）；依赖数据 = 是（年度面 3,790,547 行、emerging_topic 快照 4,496 行/年度 53,952 行、主领域绑定覆盖率 100.0%（99,998/100,000））
> **数据源口径**：三源（开发库 live `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev`）逐一探针留证；`demo_*` 禁引。三源中久新为领域热度的唯一数据源（gkx/dev 零承载不影响判档，探针留证在案）。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。** 三源均无「fieldHotness 型学者级领域热度」现成分（久新 `ads_talent_profile` 列级 hot/heat 词族扫 0 命中——画像面无热度列），但两条转换链结构+数据双达标且**现在就能算**：**产出侧**——`ads_talent_yearly_discipline`（3,790,547 行、2023-2025 三完整年论文总量 1,452,744/1,876,508/2,344,931）按 field×year 聚合直查，2025 年 Top1 领域产出份额 16.0986%（377,500/2,344,931，派生键 `jiuxin_2025_top1_field_paper_share_pct`）即「领域热度=份额×100」读数样例；**关注/演进侧**——`ads_emerging_topic_*` 全套官方热度指标（快照 4,496 行含 relative_growth/新作者占比、年度面 53,952 行），快照 Top1 相对增长 7,127,871.0（`jiuxin_emerging_top1_relative_growth`，库内官方口径非本件自算）。**学者绑定链完整**：`ads_talent_potential_result.primary_field_id` 非空 99,998/100,000（覆盖率 100.0%，派生键 `jiuxin_primary_field_coverage_pct`）→ 领域年度面一条 JOIN 即得「学者所研究领域的热度值」；第二绑定路径 `ads_talent_topic_profile` 近窗活跃底料在（recent_3y 合计 6,927,354 篇、近 3 年活跃 topic 3,664,345 个）。gkx 280 表热度词族 0 命中、dev 命中 3 表均为产业链/企业级非学者领域级——按三源铁律久新即数据源，判完全转换支持。合成算式（份额×100 还是增长加成）双口径并列待裁（B10）。

### 批次通用纪律摘要（S3-03 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实；久新表数写「实测 210 张（探测日）」 |
| B3 | 同基相除 | 三个派生比分子分母均同表同 WHERE（377,500/2,344,931；99,998/100,000） |
| B4 | 负结论带探针 | gkx/dev 零承载与需求算式缺的 absence_probe（§3.3） |
| B5 | 确定性 | Top10 双键排序（SUM 降序+field_id 升序）；heat_like_tables 列表 sorted() |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | py 冻结产物 22:13 落盘；本 MD 为二次重派后父代理依产物补写，零手改产物 |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | fieldHotness 为 0-1 浮点、UI 渲染 ×100；2026 为 PARTIAL_YEAR 不入正式窗口；relative_growth 数值量级达 7 位数（非百分比） |
| B10 | 口径裁定保守交付 | 双口径并列（产出份额/演进增长），选型留裁定；升档/降档触发器写死 |
| B11 | 多本账互推 | field 26/subfield 252 维表与 PF_003、X_015 对账同体系；fld_* 哈希 ID 同源 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 依赖结构+数据双够吗？ | 双够 | 年度面 3,790,547 行 + emerging_topic 快照 4,496/年度 53,952 行 + 绑定链覆盖率 100.0%（§2.2/§2.3） |
| 现转跑通了吗？ | 跑通 | 2024/2025 Top10、三年总量、快照 Top5、近窗合计全落产物（§2.3/§2.4） |
| 有现成结果面吗？ | 无（故非完全直接） | profile 列级 0 命中；三源无「学者×领域热度」物化面 |

## 摘要

「研究领域热度值」是人才画像「学术影响力量化（引进参考）」卡五条 influence-bars 的末行「领域热度」：`ProfileBasicPanel.jsx:373` 取 `academicInfluence.fieldHotness`（0-1 浮点）渲染为 `Math.round(×100)` 的 0-100 进度条（mock 生成器 `data.js:862` `randomFloat(0.62,0.95,2)` 演示值，不作数据证据）。语义=**学者所研究领域的外部热度**（领域侧关注度/活跃度），区别于该卡前四条的学者自身贡献结构（论文贡献/引用影响/项目贡献/热点对齐）。需求侧「研究热点」行为明列（主需求 :2290-2292 动态热点标记「对近期高频关注领域和最新研究热点进行自动高亮标记」），「热度值」数值定名三份真源 0 命中——派单书定名「关注/产出活跃度」双口径。数据侧久新双链齐备：产出侧 `ads_talent_yearly_discipline` 2025 年 Top1 领域（fld_f797…）论文 377,500/被引 1,209,613、全池份额 16.0986%；关注侧 `ads_emerging_topic_snapshot`（4,496 topic）Top1 相对增长 7,127,871.0、年度面三年论文 437,871→609,129→852,391 稳增；学者绑定 `potential_result.primary_field_id` 覆盖 99,998/100,000（100.0%）。判**完全转换支持**。脚本已跑通，产物与正文数字逐一对应；本 MD 由父代理依冻结产物补写（前两任子代理连接中断，py/产物无损）。

- 需求判定：**需求明列行为叶**（「研究热点」:2290-2292 明列），热度合成算式无——双口径并列（B10）。
- 复现状态：脚本已跑通（21:56-22:13 任内）；Top10/总量/快照/绑定链读数全落产物。
- 档位结论：**完全转换支持**（三源无现成分 + 久新双链结构数据双够 + 现转跑通）。
- 关键事实：`ads_talent_profile` 无 primary_field_id 也无热度列——主领域与年度面绑定承载在 potential_result/yearly_discipline，直查画像面会误判「无领域数据」（与 PF_003 共证）。
- 口径裁定点：合成算式选产出份额口径（16.0986% 型读数）还是演进增长口径（7,127,871.0 型读数）——量纲差 8 个数量级，必须裁。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 重点科技人才画像（人才画像总览页） → 学术影响力量化（引进参考）卡 → influence-bars 第 5 行「领域热度」。同卡四条姊妹读数：论文贡献/引用影响/项目贡献（disciplineContribution 结构）与热点对齐（hotspotAlignment）；本条是唯一的**领域侧**读数（其余为学者自身结构）。

### 1.2 为什么需要本指标

人才引进决策不能只看学者自身产出，还要看其**所在领域的势**：领域在上升期（高热度）则学者成果的边际价值与成长空间更大，领域在衰退期则反之。「领域热度」条把领域侧外部信号并入画像卡，与「热点对齐」条（学者方向与热点的重合度）构成「领域热不热 + 学者贴不贴」的二维引进参考——这是引进参考功能块的原始动机（主需求 :2241 总述「将专家研究领域的发展趋势和兴趣热点以图形化方式直观展现……助力科技人才评价」）。

### 1.3 需求文档是否给出定义方法

**需求文档未给出「热度值」算式。** 三份需求真源「热度值」数值定名 0 命中；最近义两处均为**行为**描述非算式：主需求 :2290-2292（动态热点标记）「对近期高频关注领域和最新研究热点进行自动高亮标记，辅助管理决策和学术评价」+ :2241 总述「兴趣热点以图形化方式直观展现」。算法库 :349「投资的领域热度」是投融资分析语境（投资领域分布维度），非学者画像语义。「关注/产出活跃度」双口径为派单书定名。

### 1.4 类似指标权威方法可行性分析概要

领域热度测量两族先例：①**产出活跃度系**（ scientometrics 标准）：领域论文产出份额/增速——OpenAlex topics 体系按 works_count 时序监测领域规模演进（官方 API 即支持按 topic 分组计数）；②**新兴主题探测系**（库内已物化）：relative_growth 型相对增长 + 新作者占比 + 作者/机构扩散——CWTS Leiden 分类体系（OpenAlex 四级层级的学术基础）的成熟扩展。两族在本库**均有结构化承载**（产出侧 yearly_discipline、演进侧 emerging_topic 官方窗口），区别只在合成算式选型。完整版见附录 C。

### 1.5 引用来源

- UI：`repos/demo-ui-science/src/pages/talent-trend/components/ProfileBasicPanel.jsx:373-374`（领域热度条渲染，`Math.round(fieldHotness×100)`）；`repos/demo-ui-science/src/pages/talent-trend/data.js:855-866`（academicInfluence 结构：score/hIndex/citations/fieldHotness/hotspotAlignment；:862 mock 生成器 `randomFloat(0.62,0.95,2)` 演示值，不作数据证据）。
- 需求：主需求 :2241（总述）、:2251（多级展开）、:2290-2292（动态热点标记）。
- 数据：久新 `ads_talent_yearly_discipline` / `ads_emerging_topic_snapshot` / `ads_emerging_topic_yearly_metrics` / `ads_talent_potential_result` / `ads_talent_topic_profile`（实测 210 张 ads_* 内，探测日 2026-11-01）。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测原意**：给引进决策人一条「这个学者所在领域现在有多热」的 0-100 直观读数，与「热点对齐」配合判断学者方向是否踩在势头上。

**推测定义（双口径并列，待裁）**：
- 口径 P（产出侧份额）：领域热度 = 学者主领域当年论文数 ÷ 全池当年论文总数 × 100（读数样例 16.0986，2025 Top1 领域）；
- 口径 E（演进侧增长）：领域热度 = 学者主领域（topic 级）的 relative_growth（库内官方新兴度分，读数样例 7,127,871.0）或其归一化映射。

| 触发器 | 条件 | 动作 |
|---|---|---|
| 升档→完全直接支持 | 久新物化「学者×领域热度」结果面（profile 增列或独立快照表）且数值与 emerging_topic 官方口径一致 | 改判并引用官方面 |
| 降档→部分支持 | yearly_discipline 年度面停更（2025 后断年）或 primary_field_id 覆盖跌破 95% | 绑定链/分母失效，重判 |
| 口径裁定 | 甲方锁定 P 或 E | 锁定侧写死入 UI 映射，另一侧留档 |

### 1.7 需求叶定位与相近叶关系

- 本叶：学术影响力量化卡·领域热度条（:2290 动态热点标记的读数化叶）。
- 姊妹叶 PF_003（领域构成）：同一 annual 面不同读数——PF_003 问「分布长什么样」（构成占比），本件问「某领域有多热」（份额/增长）——共享维表与年度面，族内对账零漂移。
- 邻叶「热点对齐」（hotspotAlignment，同卡第 4 条）：学者方向与热点的**重合度**（人-领域夹角），本件是领域自身的**热度**（领域侧强度）——两者相乘才是「踩在热点的学者」完整语义，-hotspotAlignment 未单独立项（export 行语义并入画像卡族）。
- X_015（subfield 中心性）：同体系不同层——X_015 在 subfield 252 层做网络中心性，本件在 field 26/topic 层做热度，fld_*/subfield ID 同源可互推（B11）。

## 二、计算过程

### 2.1 方法选择（文献依据）

双口径的方法论锚：产出侧采用 scientometrics 的领域份额监测（OpenAlex 官方 API 按 topic 分组 works_count 时序即标准操作，见 R1/R2）；演进侧采用新兴主题探测的 relative_growth 族（CWTS Leiden 分类体系 + 突发检测传统，见 R3 temporal n-gram burst 检测的近期方法学）。两族在库内均有官方物化（yearly_discipline / emerging_topic 官方窗口），本件不自创算式、只做选型登记——保守纪律（B10）。

### 2.2 装载与三层链路定位

装载三源连接（dev live `gkxlumenx_*` 非 demo + gkx 只读 + 久新只读）后，热度的承载链定位为三层（久新）：**维表层**（OpenAlex 四级：domain 4/field 26/subfield 252/topic 4,516，与 PF_003/X_015 对账同体系）→ **年度面层**（`ads_talent_yearly_discipline` 3,790,547 行，field×year 论文/被引聚合；`ads_emerging_topic_yearly_metrics` 53,952 行，topic×year 全套热度指标）→ **绑定层**（`ads_talent_potential_result.primary_field_id` 99,998/100,000 非空 + `ads_talent_topic_profile` 近窗活跃 recent_3y/recent_5y 论文计数）。dev/gkx 的排除证据见 §2.5/§3.3。

### 2.3 产出侧读数（口径 P，现转）

`ads_talent_yearly_discipline` 按统计年切片聚合（全量非采样）：2025 年 Top10 领域论文数榜首 fld_f797dcaaa15048f1b006886c37a93810 = 377,500 篇（被引 1,209,613），全池论文 2,344,931 篇 → Top1 份额 16.0986%（派生键 `jiuxin_2025_top1_field_paper_share_pct`，分子分母同表同年同 WHERE 池）；2024 年同领域 260,916 篇居首（全池 1,876,508）。三年全池总量 2023/2024/2025 = 1,452,744/1,876,508/2,344,931（`jiuxin_yd_paper_total_by_year`，年增约 25%-29%——全池本身在涨，份额口径天然扣除大盘膨胀）。Top10 双键排序（SUM 降序+field_id 升序，B5）。

### 2.4 关注/演进侧读数（口径 E，现转）

**Top10 排名漂移（2024→2025，热度指标的核心观测量）**：Top2 稳定（fld_f797… 260,916→377,500、fld_90d1… 218,098→323,175，同序）；**fld_1f46… 是典型降温域**——2024 年第 3（181,650）→ 2025 年第 6（150,989），绝对量逆势下降 12.5%的同时全池增 25%，份额口径下降幅更深；fld_6b99…（2024 第 10，63,072）跌出 2025 Top10（替补 fld_f9a7… 66,886）。这正是份额口径优于绝对量的实证：若按绝对量，全池 61.4% 的三年增幅会全面虚高所有领域。

`ads_emerging_topic_snapshot`（4,496 topic）官方快照面：Top1 相对增长 topic_df1d9d2d0e8e4e4f8989ed893db4c91c = 7,127,871.0（relative_growth=（近期年均份额+1e-12)/(对照年均份额+1e-12)，库内官方口径非本件自算，`jiuxin_emerging_top1_relative_growth`），Top2 = 6,565,778.0（0.933333 新作者占比）。年度面 `ads_emerging_topic_yearly_metrics`（53,952 行）三年总量：论文 437,871→609,129→852,391、作者 2,765,121→4,043,779→5,788,392、机构 734,702→1,011,371→1,406,154（2023→2025，全稳增）。官方窗口纪律（schema 明载）：观察窗 2017-2025、对照窗 2020-2022、近期窗 2023-2025，撤稿与 paratext 不入有效总体，2026 为 PARTIAL_YEAR 只展示不进窗口（B9）。快照 Top5 按 relative_growth 降序+topic_id 升序双键排序（B5）。

### 2.5 三源排除探针

**gkx**：280 表 heat/hot/trend/momentum/emerging 词族扫 0 命中——gkx 是科技要素库（论文/专利/机构/政策），无任何热度/趋势结果面；dwd_scholar 亦无 field 列（PF_003 探针在案），学者领域热度无从构建。**dev**：`gkxlumenx_*` 同词族扫命中 3 表——`gkxlumenx_ads.chain_hotspot`/`industry_chain_graph_snapshot`（产业链热点图谱）与 `gkxlumenx_dwd.enterprise_growth_trend`（企业成长趋势）——产业链/企业级非学者领域级，且无人才×领域绑定，不构成本件承载。**久新画像面**：`DESC ads_talent_profile` 后 hot/heat 词族列扫 0 命中——profile 无学者级领域热度现成分（这正是「需转换」而非「直接」的判据）。三源逐库留证入 absence_probe（§3.3）。

### 2.6 稳健性与口径敏感性

两条稳健性证据：①**份额口径对大盘膨胀免疫**——2025 全池较 2023 增 61.4%，绝对量口径会全面虚高，份额口径自动归一（Top1 读数 16.0986% vs 绝对量 377,500——两种读数差 4 个数量级，选型影响巨大）；②**演进侧官方窗口已做对照归一**——relative_growth 以 2020-2022 对照窗为基线，非裸增速，突发检测领域标准做法。敏感性风险一处：fld_* 哈希 ID 无名称列直查（需维表 JOIN 展开，见 §4.2），Top10 表以 ID 呈现在案不影响份额计算但影响可读性——登记为轻量缺口非判档项。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TALENTPF_006.py`（三源探针 + 产出侧/演进侧现转读数 + 派生三键，S3-03 Lane 5）
- 产物：`code/M_SCIUI_TALENTPF_006_out.json`（判档「完全转换支持」，基期 2023-2025 完整年）
- 关键读数（逐键对应产物）：产出侧——年度面 3,790,547 行（`jiuxin_yearly_discipline_rows`）、2025 Top1 领域 377,500 篇/被引 1,209,613、份额 16.0986%（`derived[0]`）；演进侧——快照 4,496 行（`jiuxin_emerging_topic_snapshot_rows`）、Top1 相对增长 7,127,871.0（`derived[1]`）、年度面 53,952 行三年稳增（`jiuxin_emerging_topic_year_totals`）；绑定链——primary_field_id 覆盖 99,998/100,000 = 100.0%（`derived[2]`）。

### 2.8 分步证据对照表

| 步 | 产物键 | 读数 | 章节 |
|---|---|---|---|
| 表覆盖扫 | jiuxin_table_count / jiuxin_heat_like_tables | 实测 210 张（探测日）；heat 词族命中 15 张（emerging_topic/hotspot/research_problem 等） | §2.2 |
| 产出侧年度面 | jiuxin_yearly_discipline_rows | 3,790,547 行 | §2.3 |
| 2025 Top1 份额 | derived[0] | 16.0986%（377,500/2,344,931） | §2.3 |
| 三年全池 | jiuxin_yd_paper_total_by_year | 1,452,744/1,876,508/2,344,931 | §2.3 |
| 演进侧快照 | jiuxin_emerging_snapshot_growth_top5 | Top1 相对增长 7,127,871.0 | §2.4 |
| 演进侧年度 | jiuxin_emerging_topic_yearly_rows / year_totals | 53,952 行；2025 论文 852,391 | §2.4 |
| 绑定链 | derived[2] + jiuxin_potential_pf_nonnull | 99,998/100,000 = 100.0% | §2.2 |
| 近窗活跃底料 | jiuxin_topic_profile_recent_sums / recent3y_positive_topics | recent_3y 合计 6,927,354；活跃 topic 3,664,345 | §2.2 |
| gkx 排除 | gkx_heat_like_tables | []（280 表 0 命中） | §2.5 |
| dev 排除 | dev_heat_like_tables | 3 表均产业链/企业级 | §2.5 |
| 画像面列扫 | jiuxin_profile_primary_field_id_nonnull | 0（列不存在，披露在案） | §2.5 |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载 | 库 | 量级 | 判 |
|---|---|---|---|---|
| D1 领域维表（OpenAlex 四级） | ads_* 维表层（field 26） | 久新 | 与 PF_003/X_015 对账同体系 | 结构+数据在 |
| D2 领域年度面 | ads_talent_yearly_discipline | 久新 | 3,790,547 行 | 结构+数据在 |
| D3 演进热度面 | ads_emerging_topic_snapshot + yearly_metrics | 久新 | 4,496 + 53,952 行 | 结构+数据在 |
| D4 学者绑定 | ads_talent_potential_result.primary_field_id | 久新 | 99,998/100,000 非空 | 结构+数据在 |
| D5 近窗活跃（第二绑定路径） | ads_talent_topic_profile | 久新 | recent_3y 合计 6,927,354 | 结构+数据在 |
| D6 gkx 热度面 | — | gkx | 0 命中 | 零承载（不影响判档） |
| D7 dev 热度面 | chain_hotspot 等 3 表 | dev | 产业链/企业级 | 语义错位不采 |

### 3.2 覆盖与量级（久新侧）

绑定链覆盖率 100.0%（99,998/100,000，同表全量非采样）；年度面覆盖 2023-2025 三完整年（基期字段 base_years_used=[2023,2024,2025]，无缺年——base_years_missing=[]）；演进侧官方窗口近期窗恰为 2023-2025 与产出侧基期重合，双口径同基可比。画像面 100,000 人全覆盖于潜力面分母（potential_result 全量）。

### 3.3 结构化承载 absence_probe 全记录

否定性证据四件套：**其一（gkx）**——280 表热度词族 0 命中（gkx 无热度/趋势结果面；dwd_scholar 无 field 列共证）；**其二（dev）**——命中 3 表均为产业链热点/企业成长语义，无人才×领域绑定不采；**其三（jiuxin 画像面）**——profile 列级 hot/heat 词族 0 命中，无学者级领域热度现成分（转换判据）；**其四（doc）**——三份需求真源「热度值」数值定名 0 命中，最近义 :2290-2292 为热点「行为」明列、热度「算式」无（B4 全记录入产物 absence_probe 数组）。

### 3.4 现场复核清单

复核人按 `code/M_SCIUI_TALENTPF_006.py` 逐段重跑（幂等只读），五步核数：

| 步 | 操作 | 预期读数 | 对应产物键 |
|---|---|---|---|
| ① 表覆盖 | 久新 SHOW TABLES → sorted() 计数 + heat/hot/trend/momentum/emerging/growth 词族过滤 | 实测 210 张（探测日，活库会增）；heat 词族 15 张 | jiuxin_table_count / jiuxin_heat_like_tables |
| ② 产出侧切片 | SELECT field_id, SUM(paper_count), SUM(cited_by_count) FROM ads_talent_yearly_discipline WHERE statistics_year=2025 GROUP BY field_id ORDER BY SUM(paper_count) DESC, field_id ASC LIMIT 10 | Top1 fld_f797… 377,500/1,209,613 | jiuxin_yd_2025_field_output_top10 |
| ③ 演进侧快照 | SELECT … FROM ads_emerging_topic_snapshot ORDER BY relative_growth DESC, topic_id ASC LIMIT 5 | Top1 top_df1d… 7,127,871.0 | jiuxin_emerging_snapshot_growth_top5 |
| ④ 绑定链 | SELECT COUNT(primary_field_id), COUNT(*) FROM ads_talent_potential_result | 99,998 / 100,000 | derived[2] |
| ⑤ 双排除 | dev information_schema 词族扫 + gkx SHOW TABLES 词族扫 | dev 3 表（产业链/企业级）；gkx [] | dev_heat_like_tables / gkx_heat_like_tables |

全部 SELECT 只读、无窗口函数依赖、Doris 兼容（久新 information_schema 无权限，一律 SHOW TABLES + DESC 替代——B5 排序纪律全程适用）。

## 四、数据缺失情况

### 4.1 现成分未物化（唯一「缺」，轻量）

「fieldHotness 型学者×领域热度」现成分三源均无（久新画像面列扫 0 命中）——但两条转换链已跑通且绑定链覆盖 100.0%，属「一条 JOIN 未物化」级轻缺口：物化建议=按口径裁定结果在 potential_result 增列 `primary_field_hotness`（口径 P）或挂 emerging_topic topic 级分（口径 E）， nightly 快照即可。

### 4.2 口径与体系裁定点（待裁，非缺）

| # | 待裁 | 选项 | 影响 |
|---|---|---|---|
| 1 | 合成算式 | P 产出份额（0-100 天然贴 UI）/ E 演进增长（官方分但量级 7 位数需归一） | 读数量纲差 8 个数量级 |
| 2 | fld_* 可读性 | 维表 JOIN 展开 field 名称 vs ID 直呈 | Top10 表可读性（不影响数值） |
| 3 | 学者级聚合 | 主领域单点（primary_field_id）vs topic_profile 多 topic 加权 | 绑定路径选型（两路径数据都在） |

### 4.3 修复建议与影响面

| 阶段 | 动作 | 改造点 | 影响面 |
|---|---|---|---|
| 短期（口径裁定后即可做） | potential_result 增列 `primary_field_hotness`（口径 P：主领域当年份额×100，nightly 快照） | 久新增列 + ETL 一条 | 画像卡渲染层一处映射（fieldHotness 语义从 mock 0.62-0.95 换真读数），无跨页依赖 |
| 中期 | 口径 E 并列：emerging_topic 官方分归一化（log10 或百分位）后与 P 并排双条 | 渲染层 + 归一函数 | 与「热点对齐」条的融合方案随画像族统一规划（038/046/053 共享「画像卡四读数」立项面） |
| 长期 | topic 级学者热度（多 topic 加权）：topic_profile recent_3y/5y 底料已在 | 加权重法则裁定 + 聚合层 | 仅新增读数，不动现有条 |

升档/降档触发器见 §1.6；本件缺口唯一且轻量（§4.1），不构成部分支持判据——转换链已跑通、绑定链 100.0%。

## 参考文献

1. OpenAlex. Topics: automatically assigned research areas[EB/OL]. OpenAlex Help Center. https://help.openalex.org/data/topics/ （R1，2026-11-01 WebSearch 核验可达——topics 四级层级与自动指派机制官方文档；产出侧份额监测的体系真源）
2. OpenAlex. List topics – API Reference[EB/OL]. OpenAlex Developers. https://developers.openalex.org/api-reference/topics/list-topics （R2，2026-11-01 WebSearch 核验可达——按 topic 过滤/分组/计数（works_count 时序）的官方 API 参考，领域活跃度监测标准操作）
3. Identifying and evaluating emerging scientific trends through temporal n-gram analysis[EB/OL]. Scientometrics. https://doi.org/10.1007/s11192-026-05744-5 （R3，2026-11-01 WebSearch 核验可达——OpenAlex 语料 n-gram 时序 + Kleinberg/MACD 突发检测的新兴趋势方法学，演进侧 relative_growth 口径的学术同源）

# 附件

## 附录 A 原始需求原文摘录

### A.1 原文（主需求《科技信息展示系统和科技专题服务系统.md》）

- :2241（研究领域图谱总述）：「研究领域图谱通过自然语言处理（NLP）、主题建模等技术，对专家发表的论文进行深度语义分析和内容挖掘……最终，采用图表、时间轴和关系图谱等可视化技术，将专家研究领域的发展趋势和兴趣热点以图形化方式直观展现，为用户提供清晰的学术成长路径和领域分布全貌，助力科技人才评价和学科布局分析。」
- :2251（多级展开）：「支持从专家总体研究方向逐级深入细分学科领域、核心关键词及不同阶段关注点，用户可按需放大至单一主题或时段的领域分布。」
- :2290-2292（动态热点标记，本件最近义）：「对近期高频关注领域和最新研究热点进行自动高亮标记，辅助管理决策和学术评价。」

### A.2 检索记录逐行

| 库/文档 | 检索式 | 命中 |
|---|---|---|
| 主需求 | rg 热度值/领域热度/fieldHotness | 0（数值定名无） |
| 主需求 | rg 热点/研究热点 | :2241/:2251/:2290-2292（行为明列） |
| 核增需求 | rg 热度/热点 | 0 |
| 算法库 | rg 领域热度 | :349（投融资分析语境，语义错位不采） |

## 附录 B 历史库表探测证据

### B.1 探测方法与三源快照

三源连接纪律与共享快照：本件直查（`M_SCIUI_TALENTPF_006.py` 自跑三源），SHOW TABLES 均经 sorted()（B5）；久新实测 210 张 ads_*（活库，探测日 2026-11-01，表数随上游增长）；dev 侧 `gkxlumenx_*` 全 schema 扫词族；gkx 经 `_gkxdb.py` 只读连接 280 表。

### B.2 本件产物逐键清单（`code/M_SCIUI_TALENTPF_006_out.json`）

| 键 | 值 | 章节 |
|---|---|---|
| jiuxin_table_count | 210 | §2.2 |
| jiuxin_heat_like_tables | 15 张（emerging_topic×3/hotspot×5/research_problem×5/其他×2） | §2.2 |
| jiuxin_yearly_discipline_rows | 3,790,547 | §2.3 |
| jiuxin_yd_2025_field_output_top10 | Top1 fld_f797… 377,500/1,209,613 | §2.3 |
| jiuxin_yd_2024_field_output_top10 | Top1 fld_f797… 260,916 | §2.3 |
| jiuxin_yd_paper_total_by_year | 2023-2025: 1,452,744/1,876,508/2,344,931 | §2.3 |
| jiuxin_emerging_topic_snapshot_rows | 4,496 | §2.4 |
| jiuxin_emerging_snapshot_growth_top5 | Top1 top_df1d… 7,127,871.0 | §2.4 |
| jiuxin_emerging_topic_yearly_rows | 53,952 | §2.4 |
| jiuxin_emerging_topic_year_totals | 2025 论文 852,391/作者 5,788,392/机构 1,406,154 | §2.4 |
| jiuxin_profile_rows / profile_primary_field_id_nonnull | 100,000 / 0（列不存在，披露） | §2.5 |
| jiuxin_potential_pf_nonnull / potential_result_rows | 99,998 / 100,000 | §2.2 |
| jiuxin_topic_profile_recent_sums | recent_3y 6,927,354 / recent_5y 10,995,191 | §2.2 |
| jiuxin_topic_profile_recent3y_positive_topics | 3,664,345 | §2.2 |
| gkx_table_count / gkx_heat_like_tables | 280 / [] | §2.5 |
| dev_heat_like_tables | 3 表（chain_hotspot/industry_chain_graph_snapshot/enterprise_growth_trend） | §2.5 |
| derived[0] jiuxin_2025_top1_field_paper_share_pct | 16.0986（377,500/2,344,931） | §2.3 |
| derived[1] jiuxin_emerging_top1_relative_growth | 7,127,871.0（官方口径） | §2.4 |
| derived[2] jiuxin_primary_field_coverage_pct | 100.0（99,998/100,000） | §2.2 |
| support_judgment | 完全转换支持 | 全文 |
| base_years_used / missing / note | [2023,2024,2025] / [] / 2026 PARTIAL_YEAR 不入正式窗口 | §2.3/§2.4 |

### B.3 共享与族内读数消费

- 与 PF_003 共享：yearly_discipline 年度面（3,790,547 行同数）、field 维表 26 个、primary_field_id 绑定（99,998/100,000 同数）——族内对账零漂移。
- 与 X_015 共享：subfield 252 维表同体系（fld_*/subfield ID 同源），层级不同（field vs subfield）。
- 本件新增直查：emerging_topic 快照/年度面读数（Lane 5 首探）。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 数据要求 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 产出活跃度（份额/增速） | OpenAlex works_count 时序（R1/R2） | 领域×年论文计数 | yearly_discipline 3,790,547 行现成 | 高（口径 P） |
| 新兴主题探测（相对增长/扩散） | relative_growth + 新作者占比（CWTS 体系，R3） | topic×年全套热度 | emerging_topic 快照 4,496/年度 53,952 行官方物化 | 高（口径 E） |
| 文本突发检测（n-gram burst） | Kleinberg/MACD（R3） | 全文题录时序 | OpenAlex 语料可及但本库未物化 n-gram 面 | 中（演进侧同族，不必自建） |
| 学者级加权合成 | 主领域单点 vs 多 topic 加权 | 绑定链 | primary_field_id 100.0% + topic_profile 双路径 | 高（待裁选型） |

### C.2 数据矩阵

| 维 | 产出侧（P） | 演进侧（E） | 裁定考量 |
|---|---|---|---|
| 时间覆盖 | 2023-2025 完整三年（base_years_used 全在） | 官方窗 2017-2025（近期窗 2023-2025） | 双口径近期窗重合，同基可比 |
| 分母基准 | 全池同年论文总量（2,344,931 @2025） | 对照窗 2020-2022 年均份额 | P 扣大盘膨胀；E 扣领域自身基线 |
| 读数样例 | Top1 份额 16.0986%（377,500/2,344,931） | Top1 相对增长 7,127,871.0 | 量纲差 8 个数量级 |
| 稳健性 | 份额对全池 61.4% 三年增幅免疫 | 官方窗口已做撤稿/paratext 剔除 | 双侧均有归一纪律 |
| UI 贴合 | ×100 即 0-100 条（与 fieldHotness×100 渲染天然对齐） | 需归一映射（log/百分位） | P 改造量小 |
| 学者绑定 | primary_field_id→年度面一条 JOIN（覆盖 100.0%） | topic_profile 多 topic 现成（recent_3y 6,927,354） | P 单点简；E 可多 topic 加权 |
| 物化成本 | potential_result 增列 nightly 快照 | 官方面已在，只做归一映射层 | 双低 |

### C.3 分期方案

一期（随画像族统一规划）：口径 P 物化（算式最简、UI 天然贴合）——potential_result 增列 + 渲染层换真读数；二期：口径 E 并列展示（官方分归一化）或与「热点对齐」条融合；三期（如需）：topic 级学者热度（多 topic 加权，法则待裁）。

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 口径 P/E 选型悬置致 UI 语义不清 | 中 | 双口径读数样例已落产物，裁定即接 |
| fld_* 哈希 ID 可读性 | 低 | 维表 JOIN 展开（§4.2） |
| emerging_topic 窗口滚动（2026 入窗时基线变） | 低 | 官方 schema 纪律在案，滚动时重跑快照对账 |
| 画像面 profile 无主领域列致误判 | 低 | 本件与 PF_003 双重共证，绑定面=potential_result 已写死入触发器 |

### C.5 总判

依赖结构+数据双达标、两条转换链现转跑通、学者绑定链覆盖率 100.0%——判**完全转换支持**；唯一悬置是合成算式选型（P/E 量纲差 8 个数量级，必须裁），已按 B10 双口径并列交付并写死升档/降档触发器。

## 附录 D 复现与对照清单

复现步骤（约 30-60 秒，三源各一连接）：

1. `cd local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code && python3 M_SCIUI_TALENTPF_006.py` → 覆盖生成 `M_SCIUI_TALENTPF_006_out.json`（幂等只读，重跑应零漂移）；
2. 对照 §2.8 分步证据对照表逐键核数（重点三个派生键：份额 16.0986 / 相对增长 7,127,871.0 / 绑定覆盖率 100.0）；
3. 族内对账：`jiuxin_yearly_discipline_rows`（3,790,547）与 `jiuxin_potential_pf_nonnull`（99,998）须与 PF_003 产物同数（零漂移）；field 26 个维表与 X_015 subfield 252 同体系；
4. 判档一致性：MD 文首 / 摘要 / §〇 / 产物 `support_judgment` 四处均「完全转换支持」；
5. 参考文献三条 URL 可达性抽查（2026-11-01 WebSearch 已核验）；
6. 活库提示：久新表数重跑可能 >210（上游持续加表）——`jiuxin_table_count` 漂移属正常，判档与关键读数不受影响（教训 6）。
