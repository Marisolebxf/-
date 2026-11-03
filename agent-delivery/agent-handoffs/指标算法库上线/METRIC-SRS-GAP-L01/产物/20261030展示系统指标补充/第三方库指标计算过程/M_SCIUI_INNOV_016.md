# 区域指标趋势对标（M_SCIUI_INNOV_016）

> **类型**：BENCHMARK（基准窗 vs 近期窗对比，双口径 A 中国双窗 / 口径 B 中美共同主题对标）｜ **域**：科技发展态势·全球创新监测·城市创新能力分析视图第 1 项｜ **UI 挂载**：`cityInnovationAnalysisModel.js:9`（视图枚举首项『趋势对标』）+ `:649`（导出报告章节）+ `:624`（报告文本第八章『趋势概览』年度领先城序列）
> **数据支持度**：**完全直接支持**｜ **公式定义人**：上游已内置（snapshot 内置双窗+增长率+方向判定，本件仅消费）｜ **口径归属**：UI 推导叶（指标名三份说明书 0 命中，但语义与 SRS seq 85 城市对标高度重合）
> **复现脚本**：`code/M_SCIUI_INNOV_016.py`｜ **产物**：`code/M_SCIUI_INNOV_016_out.json`
> **四判定摘要**：直接结构 = 是（久新 ads_topic_country_snapshot 209,517 行内置 baseline 2020-2022 / recent 2023-2025 双窗 + paper_growth_rate + trend_direction + growth_rank 全链路列）；直接数据 = 是（4,467 主题 × 224 国全量）；依赖结构 = 不需要；依赖数据 = 不需要
> **数据源口径**：本件支持度按「开发库 gkxlumenx_*（禁 demo_*）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新 jiuxin（47.93.119.170:29030 只读）」三源评估（20261101 三源铁律）。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全直接支持。** 「基准对比」的全部要件——基准窗、近期窗、变化率、方向判定、增长排名——在久新 `ads_topic_country_snapshot` **一表内置**：209,517 行（4,467 主题 × 224 国）自带 `baseline_start/end_year`（2020-2022）、`recent_start/end_year`（2023-2025）、`baseline/recent_avg_annual_paper_count`（双窗年均）、`paper_growth_rate`（双窗增长率）、`trend_direction`（UP/DOWN/STABLE/INSUFFICIENT_EVIDENCE 四值）、`growth_rank`（组内增长排名）——「区域指标趋势对标」逐字段命中，无需任何转换。实测口径 A（中国双窗）：有效判定主题 3,669 个（4,219 行剔除证据不足 550）中 UP 3,426（**93.3769%** 上行）、DOWN 163、STABLE 80；UP 增长率 Top3——数字取证与网络取证（baseline 年均 0.3333 → recent 年均 11.3333，+33.0）、商业与管理研究（0.3333→8.0，+23.0）、表面处理与涂层（0.3333→7.3333，+21.0）。口径 B（中美共同 Top5 主题双窗并排）：先进光催化（CN 2,986→5,123 年均 vs US 214.3333→279）、电池材料（CN 738.6667→3,076 vs US 98.6667→421.6667）、地球物理与重力测量（US 65.3333→3,803.3333 暴涨 +57.2143 vs CN 84.3333→243）——美方在地球物理类反超的样本。覆盖率警示：全表 INSUFFICIENT_EVIDENCE 占 67.9668%（小国×冷门主题），但中国侧仅 13.02%——**头部国家可用性远高于长尾**，回填须带 coverage_status 过滤。判**完全直接支持**。

### 批次通用纪律摘要（批 S3-01 共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | UP 占比分子分母同国同表（剔除 INSUFFICIENT_EVIDENCE 口径声明） |
| B4 | 负结论带探针 | gkx baseline/benchmark/trend 0 表 + dev 趋势类 2 表 0 行 |
| B5 | 确定性 | 榜单按 growth_rate DESC；方向判定为上游内置（幂等直读） |
| B6 | 闸门自身被闸 | 不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 手改禁令；改脚本→重跑 |
| B8 | 回执不复收 | 派单方抽硬证据复验 |
| B9 | 单位/日期陷阱 | 双窗 2020-2022/2023-2025 上游内置（不重选窗）；增长率小数 vs 百分比标注 |
| B10 | 口径裁定保守交付 | 双口径 + 覆盖率过滤警示 + 小基数增长率绝对值并排披露 |
| B11 | 多本账互推 | snapshot 209,517 与 011/017 件同表同值；CN 方向分布与口径 A 一致 |

### 判档自检三问（本件 = 完全直接支持）

| 问 | 答 | 证据 |
|---|---|---|
| 双窗对比是现成结果面吗？ | 是（五列内置） | snapshot DESC + CN 双窗实测 |
| 方向判定可信吗？ | 可信（上游四值制 + 证据不足自弃） | INSUFFICIENT_EVIDENCE 67.9668% 自弃率 |
| 需要本件重算吗？ | 不需要（本件仅直读+过滤） | 脚本无聚合公式，纯 SELECT |

## 摘要

「区域指标趋势对标」是城市创新能力分析页的**视图首项**（`cityInnovationAnalysisModel.js:9`，四视图之首），导出报告自带『趋势对标』章节与『趋势概览』年度领先城序列（:649/:624）。本件是全批少有的**完全直接支持**件：久新 `ads_topic_country_snapshot` 把「基准对比」做成了内置列——baseline 2020-2022 与 recent 2023-2025 双窗年均、双窗增长率、UP/DOWN/STABLE/INSUFFICIENT_EVIDENCE 四值方向判定、组内增长排名，209,517 行（4,467 主题 × 224 国）全量直读，无需任何转换加工。实测口径 A（中国双窗）：有效判定主题 4,219 个，UP 3,426 个（**93.3769%** 上行）——中国在几乎所有有数据的中国主题上处于双窗上行通道；UP 增长率榜首「数字取证与网络取证」从 baseline 年均 0.3333 冲到 recent 年均 11.3333（+33.0 倍率制增长率），但**绝对量仅 11 篇/年**——小基数暴涨样本，读数必须绝对值并排。口径 B（中美共同 Top5 主题）：中方在能源/材料类全面领跑（先进光催化 2,986→5,123 vs 美 214.3333→279），美方在「地球物理与重力测量」反超（65.3333→3,803.3333，+57.2143）——对标视图的「你强我弱」分布实数据。覆盖率警示：全表 67.9668% 行 INSUFFICIENT_EVIDENCE（小国×冷门主题证据自弃），中国侧仅 13.02%——头部国家可用、长尾自弃的分界清晰，回填带 coverage_status 过滤即可。判**完全直接支持**：即期回填，方向+增长率+排名三件套一次到位。

- 需求判定：**UI 推导叶**（指标名 0 命中；语义与 seq 85 城市对标『展示各城市在创新投入、创新产出、创新环境等方面的差异』高度重合——对比视图语义直给）。
- 复现状态：脚本已跑通（纯 SELECT 直读）；双口径方向分布 + 增长率榜 + 中美对标矩阵 + 三源负结论全部落产物。
- 档位结论：**完全直接支持**（双窗五列内置，结构+数据双满配）。
- 关键事实：中国 93.3769% 主题双窗上行 + 美方地球物理类反超样本——对标视图可立即上屏的两个 headline。
- 升档路径：已满档；扩展方向是城市级双窗（当前 topic×country 粒度，城市级需 geo 池自算双窗——002 件路径）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/**全球创新监测**/城市创新能力分析（视图首项）。挂载点实查：

- `src/pages/global-innovation/tabs/cityInnovationAnalysisModel.js:9`：`cityAnalysisViewOptions { key: 'trend', label: '趋势对标', title: '趋势对标' }`——分析视图第 1 项（趋势对标/关键指标对比/创新能力要素分析/创新政策建议四选一）。
- `cityInnovationAnalysisModel.js:649`：`buildCityReportExportConfig contentItems { key: 'trend', label: '趋势对标' }`——导出报告章节。
- `cityInnovationAnalysisModel.js:624`：`reportText` 第八章『趋势概览』——`${row.year}：领先城市 ${row.bestCity}` 年度领先城序列（UI 消费的是 year×bestCity 形态）。

消费结构：视图枚举 + 导出章节双入口；UI 期待「年度序列 × 领先城」形态，上游给的是「国×主题×双窗方向」形态——回填时以方向+增长率驱动趋势带、bestCity 由同窗排名派生（§1.6）。

### 1.2 为什么需要本指标

单点计数（论文数 533,316——011 件产物键）回答「多不多」，趋势对标回答「**在涨还是在跌、涨多快、比别人快还是慢**」——把存量指标变成方向性判断，是决策者最关心的形态。本指标承担三职：①**方向预警**（UP/DOWN/STABLE 三值判定直接上色）；②**增速对比**（增长率横比——中国在涨但美国在地球物理涨更快）；③**基准锚定**（和自己的基准期比还是和上一期比——本件上游选定为 2020-2022 vs 2023-2025 双窗制）。数据侧本件是「内置结果面」的代表：上游把方法学（双窗制、年均化、方向四值制）全部固化进 snapshot 列——这类件的判档是「结构+数据+公式三满配」，与 014 件（三缺一）形成方法论两极对照。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「区域指标趋势对标/趋势对标」作为指标名三份说明书 0 命中。全球创新监测.md seq 85 最近锚：『用户可选择多个城市进行创新对标分析，系统提供对比视图，展示各城市在创新投入、创新产出、创新环境等方面的差异』——「对比视图」语义命中但对象是**城市间横向对比**，本件上游是**同对象双窗纵向对比**——横向/纵向语义在 UI 与数据间有错位（§1.6 处置）；seq 12 总述『利用数据模型开展趋势预测和判断』次之（趋势判断语义）。双窗制（2020-2022 vs 2023-2025）与方向四值制（含 INSUFFICIENT_EVIDENCE 自弃）均为上游内置，需求文档未涉及——本件直接采信上游方法学。

### 1.4 类似指标权威方法可行性分析概要

基准对比的权威范式有三支。**UK Department for Science Innovation 国际对比报告**（R1）：CAGR（复合年增长率）+ 固定基准窗（如 2018-2022 五年窗）——「声明基准窗+年均化」范式，且明言 2023 数据因引用滞后不完整故止于 2022（**窗口完整性治理**标杆）；**NSF NCSES 出版物产出报告**（R2）：分数计数下的国别 CAGR 长窗对比（1996-2020），强调「不同计数制下的增长率不可互比」；**上游内置范式**（R3，本件消费）：双窗年均对比制（(recent 年均−baseline 年均)/baseline 年均）+ 四值方向判定（证据不足自弃）——比 CAGR 更保守（两窗均值抑制单年抖动），INSUFFICIENT_EVIDENCE 自弃机制是权威报告罕见的**诚实证治理**。方法族对照：

| 方法族 | 窗口制 | 增长式 | 三源承载 | 匹配度 |
|---|---|---|---|---|
| UK CAGR 固定窗（R1） | 五年固定窗 | CAGR | snapshot 双窗列可算 | 中高（可加算） |
| NSF 长窗 CAGR（R2） | 25 年长窗 | CAGR（分数计数） | topic 池全窗列在 | 中（计数制须声明） |
| 上游双窗年均制（R3） | 2020-2022 vs 2023-2025 | 双窗均值差比 | **内置列直读** | **高（即期）** |

结论：上游双窗制与 UK 范式的「年均化+声明窗」精神一致且更保守；本件直读内置列，CAGR 作为可加算变体留 v2。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/global-innovation/tabs/cityInnovationAnalysisModel.js:9/:624/:649`（视图+报告文本+导出章节）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md` seq 85（对比视图锚）、seq 12（趋势判断总述锚）。
- 数据：`code/_snapshots/_probe_lane5_s3_01_out.json`（snapshot COUNT/DESC/样例 #2/#3/#4——双窗列结构原值）。

### 1.6 推测原意与推测定义

**定义（上游内置，本件仅消费声明）**：

- **双窗制（上游内置）**：baseline 2020-2022 / recent 2023-2025（snapshot 列自带，分析窗 2015-2025）；年均化 = 窗内总量/3。
- **增长率（上游内置）**：`paper_growth_rate = (recent_avg − baseline_avg) / baseline_avg`（小数制，33.0 = 33 倍）。
- **方向判定（上游内置）**：UP / DOWN / STABLE / INSUFFICIENT_EVIDENCE 四值——证据不足自弃不硬判。
- **口径 A（中国双窗对标）**：CN 侧方向分布 + UP 增长率 Top10。实测 UP 3,426 / 4,219 有效 = **93.3769%**；Top3 增长率见 §〇。
- **口径 B（中美对标样本）**：中/美共同论文 Top5 主题双窗并排——先进光催化 CN 2,986→5,123 vs US 214.3333→279（增长率 0.7157 vs 0.3017）；地球物理与重力测量 US 65.3333→3,803.3333（+57.2143）vs CN 84.3333→243（+1.8814）——美方反超样本。
- **UI 形态适配**：trendRows（year×bestCity）由「同窗排名派生 bestCity + 双窗方向上色」装配——上游列足够，不需新数据。

**降档/升档触发器（B10 模板）**：本件已满档（完全直接支持）。扩展触发器：①城市级双窗（当前 topic×country 粒度不含城市）→ geo 池 CITY 级自算双窗（002 件年度序列路径）→ 城市卡另立件；②CAGR 变体（R1 范式加算）→ v2 增强不换档。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md` |
| 所属四级功能 | 全球创新监测（33 叶）· 城市创新能力分析 |
| 本件挂载视图 | 分析视图首项（主）+ 导出报告趋势章节 |
| 需求叶对应 | 无同名叶；最近 seq 85/seq 12 语义级 |
| 批内相邻件 | M_SCIUI_INNOV_002（趋势演进——同 geo 池年度序列，本件是 topic 池双窗件）；M_SCIUI_INNOV_011（区域论文数——同 topic 池存量列）；M_SCIUI_INNOV_017（领域排名——同池 output_rank）；M_SCIUI_TECHTRK_024（指标趋势序列——技术跟踪侧同族） |
| 跨模块参照 | 技术发展跟踪（趋势判断语境） |

本件与 002 是「双窗/序列」姊妹：002 消费 geo 池年度序列（time 维），本件消费 topic 池双窗判定（window 维）——前者画连续曲线、后者给区间判定，两件合覆盖趋势类展示的两形态。与 011 共享 topic 池的存量列（paper_count），本件增量为双窗列——「一池两吃」的典型。

## 二、计算过程

### 2.1 装载与规模校验

久新 `ads_topic_country_snapshot` 209,517 行（`facts.jiuxin_topic_country_rows`，官方快照 #2 原值断言通过）= 4,467 主题 × 224 国（`jiuxin_topic_country_distinct_topics/distinct_countries`）。双窗五列 + 方向列 + 排名列全在（官方快照 #3 DESC）：baseline/recent_avg_annual_paper_count、paper_growth_rate、trend_direction、growth_rank——**基准对比全链路一表内置**。

### 2.2 gkx/dev 侧负结论（absence_probe）

gkx baseline/benchmark/trend 三关键字表扫描：**0 表**；dev `enterprise_growth_trend` / `sz_city_benchmark` 趋势对标类 2 表 **0 行**（013 件官方探针原值消费，`dev_trend_benchmark_rows=[0,0]`）——两库均无内置基准对比承载，判档依据独落久新。

### 2.3 方向分布（全表 + 中国）

全表：UP 54,244 / DOWN 9,895 / STABLE 2,976 / INSUFFICIENT_EVIDENCE 142,402（`jiuxin_trend_direction_distribution`）——自弃率 67.9668%（`derived.jiuxin_global_insufficient_pct`）。中国：UP 3,426 / DOWN 163 / STABLE 80 / INSUFFICIENT_EVIDENCE 550（`jiuxin_cn_trend_direction_distribution`）——**UP 占有效比 93.3769%**（`derived.jiuxin_cn_up_share_of_valid_pct`，分母 4,219 剔除自弃行）。

### 2.4 口径 A：中国 UP 增长率 Top10

```sql
SELECT dt.name_zh, s.paper_growth_rate, s.baseline_avg_annual_paper_count, s.recent_avg_annual_paper_count
FROM ads_topic_country_snapshot s JOIN ads_discipline_topic dt ON s.topic_id=dt.topic_id
WHERE s.country_code='CN' AND s.trend_direction='UP'
ORDER BY s.paper_growth_rate DESC LIMIT 10
```

Top3：数字取证与网络取证（0.3333→11.3333，+33.0）、商业与管理研究（0.3333→8.0，+23.0）、表面处理与涂层（0.3333→7.3333，+21.0）（`jiuxin_cn_up_growth_top10`）——**小基数警示**：Top3 的 baseline 年均均 0.3333（三年 1 篇），增长率读数必须与绝对量并排（B10 披露）。

### 2.5 口径 B：中美共同 Top5 主题双窗并排

中/美各取全主题集合，按论文量取共同 Top5（`jiuxin_cn_us_common_top5_topics`）：

| 主题 | CN baseline→recent 年均 | CN 增长 | US baseline→recent 年均 | US 增长 |
|---|---|---|---|---|
| 先进光催化技术 | 2,986→5,123 | 0.7157 | 214.3333→279 | 0.3017 |
| 能源转换电催化剂 | 2,667→5,024 | 0.8838 | 376→518 | 0.3777 |
| 电池材料研究进展 | 738.6667→3,076 | 3.1643 | 98.6667→421.6667 | 3.2736 |
| 金属有机框架的合成与应用 | 1,038.3333→1,879 | 0.8096 | 215.6667→295 | 0.3679 |
| 地球物理与重力测量 | 84.3333→243 | 1.8814 | 65.3333→3,803.3333 | 57.2143 |

——中方能源材料类量级碾压（5-10 倍），美方地球物理类 recent 窗暴增（3,803.3333 年均 vs 中方 243）——**对标视图「你强我弱」分布的实数据**。

### 2.6 复现代码结果展示

| 产物键 | 值（节选） |
|---|---|
| `jiuxin_trend_direction_distribution` | UP 54,244 / DOWN 9,895 / STABLE 2,976 / IE 142,402 |
| `jiuxin_cn_trend_direction_distribution` | UP 3,426 / DOWN 163 / STABLE 80 / IE 550 |
| `jiuxin_cn_up_growth_top10[0]` | 数字取证与网络取证 +33.0（0.3333→11.3333） |
| `jiuxin_cn_us_common_top5_topics[4]` | 地球物理与重力测量（US +57.2143 反超样本） |
| `derived.jiuxin_cn_up_share_of_valid_pct` | 93.3769 |
| `derived.jiuxin_global_insufficient_pct` | 67.9668 |

### 2.7 分步证据对照表

| 步骤 | SQL/操作 | 产物键 | 结果 |
|---|---|---|---|
| S1 规模断言 | COUNT snapshot | `jiuxin_topic_country_rows` | 209,517 零漂移 |
| S2 gkx 探测 | 三关键字 LIKE | absence_probe | 0 表 |
| S3 dev 消费 | 013 件探针原值 | `dev_trend_benchmark_rows` | [0,0] |
| S4 方向分布 | GROUP BY trend_direction ×2 | 双分布键 | CN UP 3,426 |
| S5 口径 A | CN+UP Top10 | `jiuxin_cn_up_growth_top10` | 数字取证榜首 |
| S6 口径 B | 中美 JOIN 并排 | `jiuxin_cn_us_common_top5_topics` | 地球物理美方反超 |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 源表 | 行数 | 库别 | 状态 |
|---|---|---|---|---|
| D1 双窗判定面 | ads_topic_country_snapshot | 209,517 | jiuxin | **全量内置（主承载）** |
| D2 主题字典 | ads_discipline_topic | 4,516 | jiuxin | 全量（name_zh 反查，行数 017 件同值登记） |
| D3 gkx 对标类 | — | 0 表 | gkx | 三关键字 0 命中 |
| D4 dev 趋势类 | enterprise_growth_trend 等 | 0 行 | dev | 空载 |

### 3.2 D1 主承载明细

双窗五列全量非空（自弃行 INSUFFICIENT_EVIDENCE 的双窗列可能有值但方向列自弃——过滤即用）；CN 侧 4,219 有效行 + 550 自弃行与方向分布一致（B5 幂等）。`growth_rank` 本件未主消费（方向+增长率已足），留作 v2 排名视图。

### 3.3 D3/D4 负结论面

gkx 无内置双窗/基准承载（LIKE 0 表）；dev 两张名字最像的表（enterprise_growth_trend/sz_city_benchmark）均 0 行——两库趋势对标面完全空载，负结论双登记。

### 3.4 现场复核清单

- `SELECT COUNT(*) FROM ads_topic_country_snapshot` → 209,517
- `SELECT trend_direction, COUNT(*) FROM ads_topic_country_snapshot WHERE country_code='CN' GROUP BY trend_direction` → UP 3,426 / DOWN 163 / STABLE 80 / IE 550
- `SELECT paper_growth_rate FROM … WHERE country_code='CN' AND trend_direction='UP' ORDER BY paper_growth_rate DESC LIMIT 1` → 33.0（主题：数字取证与网络取证）

## 四、数据缺失情况

### 4.1 长尾自弃率高（覆盖率缺口）

全表 67.9668% 行 INSUFFICIENT_EVIDENCE——小国×冷门主题双窗证据不足自弃。**修复建议**：回填带 coverage_status 过滤 + 自弃行灰显（不硬判）。**影响面**：小国视图大量空态（自弃是诚实设计，非数据 bug）。

### 4.2 城市级双窗缺位（粒度缺口）

UI 挂载是城市分析页（cityInnovationAnalysisModel），上游 snapshot 是 country 粒度——城市级双窗须由 geo 池 CITY 级自算（002 件年度序列路径）。**修复建议**：城市卡 v2 接 geo 池自算双窗。**影响面**：城市视图初期以国家级数据代理或延后。

### 4.3 小基数增长率误读风险（读数缺口）

UP 榜首增长率 +33.0 的绝对量仅 11.3333 篇/年（baseline 0.3333）——小基数暴涨。**修复建议**：增长率卡片强制带双窗绝对值并排（口径 B 表式）。**影响面**：只看增长率榜会产生「中方全线上涨 33 倍」的误导 headline。

## 参考文献

1. International comparison of the UK research base, 2025[EB/OL]. UK Department for Science, Innovation and Technology. https://www.gov.uk/government/publications/international-comparison-of-the-uk-research-base-2025/international-comparison-of-the-uk-research-base-2025 （R1，固定基准窗+CAGR+窗口完整性治理范式，2026-11-01 WebSearch 核验可达）
2. Publications Output: U.S. Trends and International Comparisons[EB/OL]. NSF NCSES. https://ncses.nsf.gov/pubs/nsb20214/publication-output-by-country-region-or-economy-and-scientific-field （R2，国别增长率长窗对比与计数制声明，2026-11-01 WebSearch 核验可达）
3. Growth rates of modern science[EB/OL]. Palgrave Communications. https://doi.org/10.1057/s41599-021-00903-w （R4，科学增长率的分段回归与增长率方法论，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

**「区域指标趋势对标/趋势对标」未作为指标名出现在三份说明书。** 检索记录（2026-11-01）：

| 检索词 | 范围 | 命中 |
|---|---|---|
| 趋势对标 | 全球创新监测.md | 0 |
| 对标 | 全球创新监测.md | seq 85（城市对标分析）+ seq 12（趋势判断总述） |
| trend | UI 源码 | cityInnovationAnalysisModel.js:9/:624/:649（本件挂载） |

最近语义原文：
- seq 85：『用户可选择多个城市进行创新对标分析，系统提供对比视图，展示各城市在创新投入、创新产出、创新环境等方面的差异。』
- seq 12：『支持全球创新成果与热点的检索分析、展示最新的创新动态、利用数据模型开展趋势预测和判断、对全球城市进行创新能力分析。』

### A.2 检索记录逐行

（检索工具：ripgrep 于 SRS 目录与 repos/demo-ui-science/src；时间 2026-11-01；命中行号已实查 ±10 行上下文。）

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INNOV_016_out.json`（20261101 实跑：双口径方向分布 + 增长率榜 + 中美矩阵 + 三源负结论在案）。
- 本 lane 共享探针：`code/_snapshots/_probe_lane5_s3_01_out.json`（snapshot COUNT/DESC/样例 #2/#3/#4）。
- 姊妹件探针：`code/M_SCIUI_INNOV_013_out.json` 的 dev 趋势类 2 表 0 行（本件消费原值）。

### B.2 本件产物逐键清单（`code/M_SCIUI_INNOV_016_out.json`，20261101 实跑）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `jiuxin_topic_country_rows` | 计数 | 209,517 | §2.1 |
| `jiuxin_topic_country_distinct_topics/countries` | 基数 | 4,467 / 224 | §2.1 |
| `jiuxin_topic_country_windows` | 窗口 | 三窗内置 | §2.1 |
| `jiuxin_trend_direction_distribution` | 分布 | 四值全表 | §2.3 |
| `jiuxin_cn_trend_direction_distribution` | 分布 | 四值中国 | §2.3 |
| `jiuxin_cn_up_growth_top10` | 榜单 | 10 主题双窗+增长率 | §2.4 |
| `jiuxin_cn_us_common_top5_topics` | 矩阵 | 5 主题中美双窗 | §2.5 |
| `dev_trend_benchmark_rows` | 负结论 | [0,0] | §2.2 |
| `derived.jiuxin_cn_up_share_of_valid_pct` | 派生比 | 93.3769 | §2.3 |
| `derived.jiuxin_global_insufficient_pct` | 派生比 | 67.9668 | §2.3 |
| `absence_probe` | 探针 | gkx 0 表 + dev 0 行 | §2.2 |
| `support_judgment` | 判档 | 完全直接支持 | §〇 |

### B.3 共享快照消费（B11 零漂移）

本件消费：官方 lane5 快照 #2（209,517）作规模登记值；#3（DESC 双窗列）作结构证据；013 件 dev 探针（2 表 0 行）作 dev 侧负结论原值。全部引用原值零漂移。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 窗口制 | 三源承载 | 贴合度 |
|---|---|---|---|
| UK CAGR 固定窗（R1） | 五年窗 | snapshot 列可加算 | 中高（v2 变体） |
| NSF 长窗 CAGR（R2） | 25 年窗 | topic 池全窗列在 | 中（计数制声明） |
| 上游双窗年均制（R3） | 2020-2022 vs 2023-2025 | **内置列直读** | **高（即期）** |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 质量 | 缺口 |
|---|---|---|---|
| snapshot 双窗面 | 209,517 | 五列内置 | 长尾 67.9668% 自弃 |
| 主题字典 | 4,516 | name_zh 全量 | 无 |
| gkx 对标类 | 0 表 | — | 结构缺失 |
| dev 趋势类 | 0 行 | — | 空载 |
| 城市级双窗 | 无内置 | — | geo 池自算（v2） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 方向+增长率对标卡（口径 A/B 直给）+ coverage 过滤 | 无（内置列直读） |
| v2 | CAGR 变体 + growth_rank 排名视图 | R1 范式加算 |
| v3 | 城市级双窗 | geo 池 CITY 级自算 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 小基数增长率误读 | **高** | 双窗绝对值并排强制 |
| 长尾空态被当故障 | 中 | 自弃行灰显+说明 |
| 城市/国家粒度混用 | 中 | 城市卡 v2 分离 |
| 增长率小数/倍率混读 | 低 | 单位标签（+33.0 = 33 倍） |

### C.5 总判

**完全直接支持**：双窗五列一表内置（结构+数据+公式三满配，全批唯二即期直读件之一），覆盖率过滤与小基数并排两个读数纪律随行。扩展路径（CAGR/城市级）不换档。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INNOV_016.py` | 退出码 0，落 `_out.json` |
| 数据入口 | jiuxin 直连只读；gkx 经 `_gkxdb.py` | demo_* 直接 raise |
| 方向分布复算 | CN 四值加总 | 3,426+163+80+550=4,219 |
| UP 占比复算 | 3,426/(3,426+163+80) | 3,426/3,669=93.3769%（有效口径） |
| 判档一致 | MD 文首 vs 产物 `support_judgment` | 完全直接支持 |
| mock 残留检查 | `rg "trendRows" repos/demo-ui-science/src/pages/global-innovation/tabs/cityInnovationAnalysisModel.js` | 正式版替换后无 mock |
