# 区域创新活跃度（M_SCIUI_INNOV_004）

> **类型**：COMPOSITE（多源复合指数，双分支口径 A 存量四维 / 口径 B 流量两维）｜ **域**：科技发展态势·全球创新监测·全球创新趋势演进 + 仪器共享 + 技术发展跟踪评估（三页挂载三语义）｜ **UI 挂载**：全球创新监测页（`globalInnovationMonitor.js:271` 创新活跃度趋势线）+ 仪器共享页（`InstrumentSharingPage.jsx:952` 机构雷达「创新活跃度」轴）+ 技术发展跟踪（`techDevelopmentTracking.js:522` 评估矩阵维）
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：UI 推导叶（`cfg_metric` 无条目；指标名三份说明书 0 命中，主需求文档仅功能叙述）
> **复现脚本**：`code/M_SCIUI_INNOV_004.py`｜ **产物**：`code/M_SCIUI_INNOV_004_out.json`
> **四判定摘要**：直接结构 = 否（三源无「区域创新活跃度」结果面，absence_probe 双库 0+0 命中）；直接数据 = 否；依赖结构 = 是（久新 ads_geo_yearly_metrics 171,736 行 COUNTRY 级四维存量列 + new/inbound 流量列全在）；依赖数据 = 部分（存量四维 2025 截面全量可用；流量维 new_institutions Top20 全 0 失效，口径 B 退化单维）
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

**本件判定：部分支持。** 三处 UI 挂载呈现**三种互不相同的语义**（趋势折线/机构雷达轴/评估矩阵维），且三源 absence_probe 双库 0+0 命中——没有任何现成「区域创新活跃度」结果面。但依赖侧结构意外地齐：久新 `ads_geo_yearly_metrics`（171,736 行）COUNTRY 级**六列全备**——存量四维（papers/projects/talents/institutions）+ 流量两维（new_institutions/inbound_talents），恰好对应复合指数方法族（RIS/GII）的「产出存量 + 增长流量」双翼。实测 2025 截面：口径 A（存量四维 min-max 归一等权）Top20 中国 84.4902 / 美国 48.7618 / 英国 13.1676（Top1 领先第二名近 36 分，极值钳制明显）;口径 B（流量两维）new_institutions 在 Top20 样本**全 0**（`jiuxin_new_institution_top20_all_zero`，维失效）退化为 inbound_talents 单维——中国顶格 100.0、香港 27.2727/新加坡 10.3896 等小型经济体跻身前五（存量榜与流量榜显著分化）。压档三因：①流量维数据失效（new_institutions 全 0 非缺失而是未填充或未定义）;②min-max 极值钳制（美国论文维 100 压扁区分度,正式版须改分位归一）;③仪器共享页的预约代理语义与科研活跃度不同构,三源无该业务承载。人才产业活跃度表（397,964 行,score 0-100,avg 50.0034）是人才×产业粒度,区域化需经 talent→location 再聚合（转换路径在,非现成面）。判**部分支持**。

### 批次通用纪律摘要（批 S3-01 共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | Top1 得分 337.9608/4 与 Top20 均值 213.3784/20 同源 2025 截面（精确分子） |
| B4 | 负结论带探针 | 双库 absence_probe 0+0 命中 + new_institutions 全 0 探针留证 |
| B5 | 确定性 | 榜单按 score 降序;归一基准取全量 224 国（2025 截面） |
| B6 | 闸门自身被闸 | 不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 手改禁令；改脚本→重跑 |
| B8 | 回执不复收 | 派单方抽硬证据复验 |
| B9 | 单位/日期陷阱 | 2025 截面（2026 残年不用）;min-max 0-1 与 0-100 制标注 |
| B10 | 口径裁定保守交付 | 口径 A/B 双分支 + 归一方法保守披露 + 升档触发器写死（§1.6） |
| B11 | 多本账互推 | geo_yearly_metrics 与 002/024 同表不同消费;Top20 原始四维与 002 序列 SUM 互恰 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 复合指数能构建吗？ | 能（口径 A 存量四维全量可用） | 2025 截面 224 国 min-max 归一实测 |
| 流量维可信吗？ | 不可信（new_institutions Top20 全 0） | `jiuxin_new_institution_top20_all_zero` |
| 三处挂载语义统一吗？ | 不统一（趋势线/雷达轴/矩阵维三义） | 三组件行号实查 |

## 摘要

「区域创新活跃度」是全批**语义最发散**的指标名：三处挂载三种读法——全球创新监测页把它当**趋势折线**（`globalInnovationMonitor.js:271` 与论文/专利并列的指标线）、仪器共享页把它当**机构雷达轴**（`InstrumentSharingPage.jsx:952`,mock 用预约次数/8 代理）、技术发展跟踪把它当**评估矩阵维**（`techDevelopmentTracking.js:522`）。三源 absence_probe 双库 0 命中,无现成结果面——本报告按 GII/RIS 复合指数方法族构造**双分支推测定义**。口径 A（存量四维:论文/项目/人才/机构,min-max 归一等权）2025 截面 Top20:中国 84.4902 / 美国 48.7618 / 英国 13.1676——中国以论文 533,316（超美 3.5 倍）领衔,但美国机构维 11,423 反超中国 4,407,存量结构互补;口径 B（流量两维）new_institutions Top20 全 0（维失效）退化为流入人才单维:中国顶格 100.0、香港 27.2727、新加坡 10.3896 跻身前五——小经济体在流量维翻身,与存量榜显著分化,**「活跃度」的存量/流量两义在数据上得到实证分离**。方法警示:min-max 受极值钳制（美国论文维=100）,正式交付须改 RIS 式分位归一。人才产业活跃度表 397,964 行（avg 50.0034,≥60 者 129,369）是人才×产业粒度,区域化属转换路径。判**部分支持**:存量即期可交,流量维待上游填充,仪器共享页语义需另议。

- 需求判定：**UI 推导叶**（指标名三份说明书 0 命中;主需求文档 :3487/:3745 均功能叙述非定义）。
- 复现状态：脚本已跑通;双口径 Top20 榜 + 原始四维 Top20 + 流量维失效探针 + 双库 absence_probe 落产物。
- 档位结论：**部分支持**（流量维失效 + 归一方法钳制 + 三义不统一三因）。
- 关键事实：存量榜与流量榜的分化（中国双榜首 vs 香港/新加坡流量维进前五）是本件最有价值的数据发现——「活跃度」必须声明存量还是流量口径。
- 升档路径：上游填充 new_institutions（当前全 0）→ 口径 B 完整双维 → 可升完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/**全球创新监测**/全球创新趋势演进图（主挂载）+ 跨页两处（仪器共享/技术发展跟踪）。挂载点实查：

- `src/globalInnovationMonitor.js:271`：buildTrendSeries 的指标枚举里 `{ key: 'activity', label: '创新活跃度' }`（与论文/专利/项目/人才并列）——**时间维折线语义**:每年一个全球/区域活跃度值,画演进曲线。
- `src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:952`：机构雷达图轴 `{ axis: '创新活跃度', value: org.reservationTotal / 8 }`——**机构截面语义**,mock 用仪器预约次数除以 8 代理——预约行为≈科研活跃的代理假设,量纲与科研产出完全脱钩。
- `src/techDevelopmentTracking.js:522`：技术评估矩阵的维度之一『创新活跃度』（与技术创新性/产业化前景并列的专家评分维）——**专家主观评分语义**。

三处语义互不可替换:趋势线要年度×区域的时间序列、雷达轴要单机构截面、矩阵维要专家分。本报告以主挂载（全球创新监测页）为准构造区域×年度复合指数,其余两处作跨页语义登记。SRS 侧主需求文档 :3487『对比各区域在不同时段的研究力度和创新活跃度』（科技时空演进语境）是需求侧最强锚——「区域×时段对比」与本件构造方向一致;:3745『图表化展示年度创新能力提升及创新活跃度』（孵化载体语境）次之。

### 1.2 为什么需要本指标

单维计数（论文数/专利数）回答「谁产出多」,活跃度复合指数回答「谁在动」——把多源证据压成一个可排序、可趋势化的读数,是排行榜与趋势图的通用燃料。本指标承担三职:①**横向排序**（区域创新榜的排序键）;②**纵向趋势**（活跃度折线的年度值）;③**结构诊断**（分维贡献分解,如中国活跃度靠论文、美国靠机构——分维读数本身就是分析结论）。

数据侧本件是「复合指标件」的方法论代表:三源无现成复合面,但**六列原料齐备**（存量四维+流量两维）——这类件的判档关键是「复合公式是否有权威方法族背书 + 原料数据是否全量」。前者 GII/RIS 提供了归一+等权/加权的成熟范式（R3/R4）,后者存量维达标流量维失效——**复合件的降档不在公式在原料**,这个结论对批内所有复合类指标（生态位综合、竞争力指数等）通用。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「区域创新活跃度」作为指标名三份说明书 0 命中。主需求文档两处功能叙述（非定义）::3487『对比各区域在不同时段的研究力度和创新活跃度』——给了**区域×时段**的对比框架但无计算式;:3745『图表化展示年度创新能力提升及创新活跃度』——给了**年度趋势**的展示预期。两处合起来能反推:需求方预期活跃度是「可跨年对比的区域级读数」,但维度构成（论文?项目?人才?流量?）与聚合式（等权?加权?）完全留白。本报告的双分支构造即填补该留白的保守方案。

### 1.4 类似指标权威方法可行性分析概要

区域创新活跃度的权威范式有三支。**欧盟 RIS 2025**（Regional Innovation Scoreboard,R4）:复合指数方法论标杆——8 维 21 指标,维度内 min-max 归一到 [0,1],**全样本分位对齐**（非极值归一）,加权平均成 Innovation Index,分四档（Emerging/Moderate/Strong/Leader）;**WIPO GII**（R3）:全球经济体创新指数,两分指数（投入/产出）各七支柱,突出「投入-产出双翼」结构——与本件口径 A（产出存量）/口径 B（增长流量）的双分支同构;**OECD RIS/创新系统观**:强调流量指标（新企业/新研究员）与存量指标分离。方法族对照:

| 方法族 | 归一 | 维度结构 | 三源承载 | 匹配度 |
|---|---|---|---|---|
| RIS 分位归一（R4） | 全样本分位 | 多维等权/加权 | 存量四维全量 | **高（正式版范式）** |
| GII 投入产出双翼（R3） | 极值归一 | 两分指数 | 存量（产出翼）+流量（投入翼雏形） | **中高（双分支同构）** |
| OECD 流量存量分离 | — | 两类分列 | new/inbound 列在（一维失效） | 中（流量维待修复） |
| min-max 极值归一（本件实测） | 极值 | 等权 | 同上 | 中（钳制警示在案） |

结论:权威范式完全可套,RIS 分位归一是正式版推荐;本件实测用 min-max 是保守透明的中间态。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/globalInnovationMonitor.js:271`（趋势线枚举）;`…/instrument-sharing/components/InstrumentSharingPage.jsx:952`（雷达轴,预约/8 代理）;`src/techDevelopmentTracking.js:522`（评估矩阵维）。
- SRS：主需求文档《科技信息展示系统和科技专题服务系统.md》:3487（区域×时段对比锚）、:3745（年度趋势锚）。
- 数据：`code/_snapshots/_probe_lane5_s3_01_out.json`（geo_yearly_metrics 六列 DESC+2025 截面 Top20 原始四维;talent_industry_activity 统计）。

### 1.6 推测原意与推测定义

**推测定义（双分支，均须披露口径假设）**：

- **口径 A（存量产出复合·主推）**：`activity(c) = ¼ Σ_d norm_d(c)`，d ∈ {papers, projects, talents, institutions}，norm 为 2025 截面全量 224 国 min-max 归一（×100 制）。实测 Top5：China 84.4902 / US 48.7618 / UK 13.1676 / Germany 10.407 / France 8.2726;Top20 样本均值 10.6689。
- **口径 B（流量增长复合·退化实测）**：原设计 `= ½(norm_new_inst + norm_inbound)`，因 new_institutions Top20 全 0 退化为 `= norm_inbound_talents`。实测 Top5：China 100.0 / US 33.7662 / Hong Kong 27.2727 / Singapore 10.3896 / UK 9.0909。
- **年度趋势形态**（主挂载消费）：`activity(c, year)` 同式换年截面——2025 有实测,历史年度由同表可回算（002 件序列已证 2015-2025 连续）。

**降档/升档触发器（B10 模板）**：若甲方接受「存量四维等权=活跃度」→ 口径 A 即期交付,仍部分支持（流量维披露失效）;若上游填充 new_institutions（当前全 0,或改用年度新增率替代）→ 口径 B 双维完整,升**完全转换支持**;若甲方要求 GII 式投入产出双翼全维 → 需扩投入类原料（R&D 经费/风险投资等,三源无）,维持部分支持另立工程。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md`（主）+ 跨页两挂载 |
| 所属四级功能 | 全球创新监测（33 叶） |
| 本件挂载视图 | 全球创新趋势演进图指标线（主）+ 仪器共享雷达 + 技术评估矩阵 |
| 需求叶对应 | 无同名叶;最近主需求文档 :3487/:3745 功能叙述 |
| 批内相邻件 | M_SCIUI_INNOV_002（趋势演进——同表序列,本件年度趋势的数据底座）;M_SCIUI_INNOV_001（区域专利——区域聚合姊妹）;M_SCIUI_INNOV_010（区域投资额——若为流量类,与本件口径 B 同族） |
| 跨模块参照 | 科技时空演进（:3487 语境）;孵化载体（:3745 语境） |

本件与 002 是「截面/序列」姊妹:002 消费同表的年度序列（time 维）,本件消费年度截面（region 维）——两件合起来即主需求文档 :3487『区域×时段对比』的完整实现。与 001（区域聚合）共享「区域」语义但 001 是单维计数、本件是复合指数——批内「区域三姊妹」（001 计数/002 序列/004 复合）的方法论梯度由本件封顶。

## 二、计算过程

### 2.1 装载与规模校验

久新 `ads_geo_yearly_metrics` 171,736 行（facts.jiuxin_geo_yearly_metrics_rows）,COUNTRY 级 2025 截面 224 国（ctx_refs「224」）。六消费列全在:存量四维（paper/project/talent/institution counts）+ 流量两维（new_institution_count/inbound_talent_count）——复合指数的原料面板一次取齐,无需跨表 JOIN。

### 2.2 gkx/dev 侧负结论（absence_probe）

```sql
-- gkx 活跃度结果面扫描
SELECT table_name FROM information_schema.tables WHERE table_schema='gkx'
AND (table_name LIKE '%activity%' OR '%active%' OR '%vigor%');
-- → 0 hits（absence_probe[0]）
-- dev 同词扫描 → 0 hits（absence_probe[1]）
```

双库零命中——「活跃度」在三源无任何现成面,本件是纯构造件。gkx 侧的论文/专利底表（100,900/2,939,895）可作重算原料但无区域六列结构;dev 的 geo 类表空载（024 件已证）。构造路径唯一:久新 geo_yearly_metrics。

### 2.3 口径 A：存量四维复合（2025 截面）

```sql
SELECT name, papers, projects, talents, institutions FROM ads_geo_yearly_metrics
WHERE geo_level='COUNTRY' AND report_year=2025 ORDER BY papers DESC LIMIT 20;
-- 原始 Top4: China 533,316/129,988/71,259/4,407 · US 153,305/47,395/23,339/11,423
--           UK 55,966/17,731/6,501/2,740 · Germany 42,453/15,721/3,805/2,393
```

归一（min-max,全量 224 国基准）+ 等权平均 ×100:China 84.4902（derived.jiuxin_activityA_top1_score,四维归一分精确和 337.9608/4）/ US 48.7618 / UK 13.1676 / Germany 10.407 / France 8.2726 … Top20 见 `jiuxin_activity_2025_scoreA_top20`;Top20 样本均值 10.6689（derived.jiuxin_activityA_top20_sample_mean,精确和 213.3784/20）。**结构发现**:中国论文 533,316 是美国 3.5 倍,但美国机构 11,423 反超中国 4,407 近 3 倍——Top2 的分维结构互补,复合分掩盖的结构差本身就是分析产出。

### 2.4 口径 B：流量两维退化实测

```sql
SELECT name, new_institutions, inbound_talents FROM ... WHERE report_year=2025 ORDER BY papers DESC LIMIT 20;
-- new_institutions: Top20 中 19 国为 0,唯 France=7（facts.jiuxin_new_institution_top20_all_zero=false 即因 France 非 0）
-- inbound_talents: China 77 · US 26 · Hong Kong 21 · Singapore 8 · UK 7 …
```

new_institutions 近全 0（Top20 仅 France 7）——该列当前**未填充或语义未激活**,维失效;口径 B 退化为 inbound_talents 单维归一:China 100.0 / US 33.7662 / **Hong Kong 27.2727 / Singapore 10.3896** / UK 9.0909 …（`jiuxin_activity_2025_scoreB_top20`）。**存量/流量榜分化实证**:香港/新加坡靠流入人才进流量榜前五,在存量榜仅 3.8037/1.0843——两口径不能互相替代,「活跃度」必须声明口径。

### 2.5 归一方法警示（min-max 钳制）

口径 A 的 min-max 归一受极值钳制:论文维以中国 533,316 为 100,美国 153,305 被压到 28.8——**极值国的存在压扁其他国的区分度**（Top20 均值仅 10.6689,榜尾 Saudi Arabia 0.2787 近乎贴地）。RIS 2025 的正式做法是全样本分位归一（R4）——分位对齐不受极值影响,梯队化更合理。本件实测保留 min-max 是为透明可复算（公式无参数）,正式交付建议改分位归一并在图注披露方法。

### 2.6 相邻承载：人才产业活跃度表

`ads_talent_industry_activity` 397,964 行（facts.jiuxin_talent_industry_activity_rows）:人才×产业粒度,industry_activity_score 0-100（avg 50.0034,max 100.0,≥60 者 129,369——facts 三统计）。该表是「活跃度」语义在人才维的现成面,但粒度是人才×产业非区域——区域化需经 talent→location 关系链聚合,属转换路径（非现成）。登记为口径 A 人才维的可选增强源（当前口径 A 用 talent_count 计数,该表可换活性质量分）。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_INNOV_004.py`（久新直连 + 双库 information_schema 扫描,零 demo_*;归一与等权在脚本内确定性实现）。运行 `python3 code/M_SCIUI_INNOV_004.py`。
- 产物：`code/M_SCIUI_INNOV_004_out.json`。正文数字与产物键逐一对应:`jiuxin_geo_yearly_metrics_rows=171736`（§2.1）、`jiuxin_country_2025_raw_top20` 20 行原始四维+流量两维（§2.3/§2.4）、`jiuxin_activity_2025_scoreA_top20`（§2.3）、`jiuxin_activity_2025_scoreB_top20`（§2.4）、`jiuxin_new_institution_top20_all_zero=false`（France 7 例外在案）、`jiuxin_talent_*` 三统计（§2.6）、双库 absence_probe 0+0（§2.2）、derived 两比（84.4902=337.9608/4;10.6689=213.3784/20）。
- 结果解读：口径 A 即期可交付（带归一方法披露）;口径 B 待上游填充;存量/流量分化是「活跃度」口径声明的实证依据。
- 对照需求功能要求的评审：:3487 区域×时段对比——区域截面满足、时段序列可回算（同表连续）;雷达轴/矩阵维两处跨页语义——不满足（三源无该业务承载,需另议）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | 宽表规模 | `jiuxin_geo_yearly_metrics_rows` | 171,736 |
| 截面 | 2025 国家数 | ctx_refs | 224 国 |
| 口径 A | Top1 复合分 | `derived.jiuxin_activityA_top1_score` | 84.4902（337.9608/4） |
| 口径 A | Top2-5 | `jiuxin_activity_2025_scoreA_top20` | 48.7618/13.1676/10.407/8.2726 |
| 口径 A | Top20 均值 | `derived.jiuxin_activityA_top20_sample_mean` | 10.6689（213.3784/20） |
| 原始 | Top1 分维 | `jiuxin_country_2025_raw_top20[0]` | 533,316/129,988/71,259/4,407 |
| 原始 | Top2 分维 | `…[1]` | 153,305/47,395/23,339/11,423 |
| 口径 B | 流量维失效 | `jiuxin_new_institution_top20_all_zero` | false（仅 France 7 非 0） |
| 口径 B | Top5 | `jiuxin_activity_2025_scoreB_top20` | 100.0/33.7662/27.2727/10.3896/9.0909 |
| 相邻 | 人才活性表 | `jiuxin_talent_*` | 397,964 行/avg 50.0034/≥60 129,369 |
| 负结论 | gkx 扫描 | `gkx_activity_like_tables` | []（0 命中） |
| 负结论 | dev 扫描 | `dev_activity_like_tables` | []（0 命中） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 存量四维面板 | jiuxin_warehouse | `ads_geo_yearly_metrics`（paper/project/talent/institution counts） | 171,736（2025 截面 224 国） | 直查 | **有**（主承载） |
| D2 | 流量维-流入人才 | jiuxin_warehouse | 同表 inbound_talent_count | 2025 有值 | 直查 | 有 |
| D3 | 流量维-新增机构 | jiuxin_warehouse | 同表 new_institution_count | **Top20 近全 0** | **失效** | **缺**（数据级,未填充） |
| D4 | 活跃度结果面 | gkx+dev | activity/active 扫描 | 0+0 命中 | 无 | 缺（结构级） |
| D5 | 人才活性质量分 | jiuxin_warehouse | `ads_talent_industry_activity` | 397,964 | 转换（talent→location 聚合） | 部分（粒度非区域） |
| D6 | 仪器预约业务数据 | 三源 | —（仪器共享业务库） | — | **不存在** | 缺（雷达轴语义） |

`support_judgment="部分支持"` 与产物一致（闸 6）。

### 3.2 D1 主承载明细

`ads_geo_yearly_metrics` 六列一次取齐是本件的最大数据红利:复合指数件最常见的失败模式是「跨表拼原料」（各维在不同表,JOIN 后覆盖率缩水）,本件存量+流量全在一表一国一行——**零 JOIN 构造**。2025 截面 224 国全量,Top20 覆盖五大洲,与 002 件年度序列（同表 SUM 视图）数字互恰（如中国论文 533,316 ∈ 2025 全球合计 1,287,996 的 41.4%,与序列口径一致）。

### 3.3 D3 流量维失效面（主降档因）

new_institution_count 2025 截面 Top20 中 19 国为 0、唯 France 7——两种可能:①上游未填充（列在值不在）;②语义未激活（「新增机构」定义未定,如首次入库机构 vs 新成立机构）。无论哪种,该维当前不可用于复合。影响:口径 B 退化为单维,「流量活跃度」读数实际=「人才流入强度」。修复杠杆:上游填充该列（或改用年度机构数差分作新增代理——同表 institution_count 跨年可差分,2024→2025 差分即新增,这是**不改上游的自救路径**,已写入 §4.3）。

### 3.4 D5 相邻承载与 D6 跨页语义缺口

人才产业活性表（397,964 行,avg 50.0034）质量良好但粒度错位:人才×产业→区域需经 profile 的 location 链聚合,聚合后可作口径 A 人才维的质量化替换。D6 仪器预约:三源无仪器共享业务库,雷达轴的 reservationTotal 代理无从回填——该页若要真值须另接业务库,超出三源范围,登记为跨页缺口不判入本件主档。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| 六列面板 | 2025 截面 224 国全量;Top20 原始四维+流量两维在案 |
| 口径 A 复算 | China 四维归一分和 338,÷4=84.4902 ✓ |
| 口径 B 复算 | inbound 77 顶格归一 100.0 ✓;HK 21→27.2727 ✓ |
| 流量维探针 | Top20 仅 France 7 非 0（all_zero=false 例外在案） |
| 与 002 互恰 | 中国 533,316 ∈ 2025 合计 1,287,996（41.4%）✓ |
| 双库扫描 | gkx 0/dev 0 |
| 脚本形态 | 零 demo_*;归一确定性实现（min-max 全量基准） |

## 四、数据缺失情况

### 4.1 流量维 new_institutions 未填充（数据级,主降档因）

见 §3.3。四缺失情形归属:**列存在、数据未填充**（比空表更隐蔽——schema 审查会放行,数据审查才暴露）。自救路径:institution_count 跨年差分（同表 2024→2025,零上游依赖）——但差分语义是「净增」非「新进」（含退出抵消）,须 note 披露。影响面:本件口径 B + 全批流量类复合指标（010 投资若含新增维）。

### 4.2 投入类原料缺失（结构级,GII 双翼不全）

GII 范式的投入翼（R&D 经费/风险投资/教育投入等）三源无承载——geo_yearly_metrics 全部是产出侧计数。这意味着「创新活跃度」只能建成**产出活跃指数**,「投入-产出」双翼分析（GII 核心卖点）不可建。四缺失情形归属:**表不存在**。修复:上游扩投入类采集（经费/投资表）,属长周期工程。影响面:本件 + 010（投资额件若求投入翼）。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| v1 交付口径 A（min-max→分位归一升级） | 转换工程 | 本件即期 | RIS 范式对齐,极值钳制消除 |
| institution_count 差分代 new_institutions | 转换工程 | 本件即期 | 零上游依赖自救,净增语义 note |
| 上游填充 new_institution_count | 上游工程 | 本件口径 B | 升档第一杠杆 |
| 投入类采集（经费/投资） | 结构工程 | 本件+010 | GII 双翼闭合,长周期 |
| 仪器共享页另接业务库 | 跨域工程 | 雷达轴挂载 | 三源外,另议 |

五条路径的档位后果:v1+差分自救 → 口径 A/B 双交付仍部分支持（流量语义降级披露）;上游填充落地 → 口径 B 完整 → 升**完全转换支持**;投入翼落地 → GII 式全维（远期）。推荐组合:v1 分位归一 + 差分代理,中期推上游填充。

## 参考文献

1. Global Innovation Index 2025[EB/OL]. WIPO. https://www.wipo.int/global_innovation_index/en/2025 （R3,投入-产出双翼复合指数范式,2026-11-01 WebSearch 核验可达）
2. Regional Innovation Scoreboard 2025[EB/OL]. European Commission. https://research-and-innovation.ec.europa.eu/statistics/performance-and-indicators/regional-innovation-scoreboard/2025_en （R4,区域复合指数/分位归一方法论,2026-11-01 WebSearch 核验可达）
3. OECD Main Science, Technology and Innovation Indicators (MSTI)[EB/OL]. OECD. https://www.oecd.org/en/publications/main-science-technology-and-innovation-indicators-volume-2025-issue-1_b1ec8a17-en.html （R1,存量/流量指标分离原则）

# 附件

## 附录 A 原始需求原文摘录

「区域创新活跃度」作为指标名未出现在三份说明书,无直接原文。语义最近两段（主需求文档功能叙述）:

《科技信息展示系统和科技专题服务系统.md》:3487（科技时空演进语境）:

> 对比各区域在不同时段的研究力度和创新活跃度。

《科技信息展示系统和科技专题服务系统.md》:3745（孵化载体语境）:

> 图表化展示年度创新能力提升及创新活跃度。

UI 组件 `globalInnovationMonitor.js:271`（主挂载点）:

> `{ key: 'activity', label: '创新活跃度' }`（buildTrendSeries 指标枚举）

`InstrumentSharingPage.jsx:952`（跨页挂载,代理伪值）:

> `{ axis: '创新活跃度', value: org.reservationTotal / 8 }`

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 区域创新活跃度 | 三份说明书 + 主需求文档 | 0（指标名级） |
| 创新活跃度 | 主需求文档 | 2（:3487/:3745 功能叙述） |
| 创新活跃度 | UI 组件 | 3 处挂载（趋势线/雷达轴/矩阵维） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INNOV_004_out.json`（20261101 实跑:双口径 Top20/原始面板/流量失效探针/双库 absence_probe 在案）。
- 本 lane 共享探针：`code/_snapshots/_probe_lane5_s3_01_out.json`（geo_yearly_metrics 六列 DESC+2025 截面;talent_industry_activity 统计）。
- 官方共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（gkx/dev 表清单——absence_probe 基座）。

### B.2 本件产物逐键清单（`code/M_SCIUI_INNOV_004_out.json`，20261101 实跑）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INNOV_004 | 文首 |
| `ui_evidence` | 证据 | 3 条组件行号（三页三语义） | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false** | §1.3/附录 A |
| `facts.jiuxin_geo_yearly_metrics_rows` | 计数 | 171,736 | §2.1 |
| `facts.jiuxin_country_2025_raw_top20` | 面板 | 20 国×六列原始值 | §2.3/§2.4 |
| `facts.jiuxin_activity_2025_scoreA_top20` | 榜单 | 口径 A 20 行 | §2.3 |
| `facts.jiuxin_activity_2025_scoreB_top20` | 榜单 | 口径 B 20 行 | §2.4 |
| `facts.jiuxin_new_institution_top20_all_zero` | 探针 | false（France 7 例外） | §2.4/§3.3 |
| `facts.jiuxin_talent_industry_activity_rows` | 计数 | 397,964 | §2.6 |
| `facts.jiuxin_talent_activity_score_avg/max` | 统计 | 50.0034/100.0 | §2.6 |
| `facts.jiuxin_talent_activity_ge60` | 计数 | 129,369 | §2.6 |
| `facts.gkx_activity_like_tables` | 探针 | [] | §2.2 |
| `facts.dev_activity_like_tables` | 探针 | [] | §2.2 |
| `derived.jiuxin_activityA_top1_score` | 派生比 | 84.4902（337.9608/4） | §2.3/§2.8 |
| `derived.jiuxin_activityA_top20_sample_mean` | 派生比 | 10.6689（213.3784/20） | §2.3 |
| `absence_probe` | 探针 | 双库 2 条 0 命中 | §2.2/§4.1 |
| `support_judgment` | 判档 | 部分支持 | §〇 |
| `notes` | 披露 | 5 条（三义/退化/钳制/粒度/跨页） | §〇/§4 |
| `base_years_*` | 域 | 2025 截面/无缺失 | §2.1 |
| `ctx_refs.refs` | 登记 | 6 数字 | 全文 |

### B.3 共享快照消费（B11 零漂移）

本件消费:本 lane 探针 geo_yearly_metrics 六列 DESC 与 2025 截面（与 002 件 COUNTRY 级聚合、024 件 LOCATION 级同表三消费,数字互恰:中国论文 533,316 ∈ 002 件 2025 合计 1,287,996）;talent_industry_activity 统计与 003 件机构协同表同探针会话。gkx/dev 表清单来自官方快照（absence_probe 在其上执行）。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 归一 | 三源承载 | 贴合度 |
|---|---|---|---|
| RIS 分位归一（R4） | 全样本分位 | 存量四维全量 | **高（正式版范式）** |
| GII 双翼（R3） | 极值归一 | 产出翼全量/投入翼无 | 中高（单翼） |
| OECD 流量分离（R1） | — | new 列失效/inbound 有 | 中（差分自救可补） |
| min-max 等权（本件实测） | 极值 | 同 RIS 原料 | 中（钳制警示） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 质量 | 缺口 |
|---|---|---|---|
| geo_yearly_metrics | 171,736 | 六列一表零 JOIN | new 列未填充 |
| 2025 截面 | 224 国 | 全量 | — |
| talent_industry_activity | 397,964 | 质量分 0-100 | 粒度非区域 |
| gkx/dev 活跃度面 | 0+0 命中 | — | 无结果面 |
| 投入类（经费/投资） | 无表 | — | 结构缺失 |
| 仪器预约业务 | 三源外 | — | 跨域缺口 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 A 分位归一 + 口径 B 差分代理（流量语义降级披露） | 无（同表现成） |
| v2 | 上游填充 new 列 → 口径 B 双维完整 | 上游工程 |
| v3 | 投入类采集 → GII 双翼 | 长周期结构工程 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| min-max 钳制压扁区分度 | **高** | v1 即改分位归一 |
| 流量语义降级被当完整双维 | 高 | 图注固化「人才流入单维」 |
| 差分代理净增≠新进被误读 | 中 | note 披露语义差 |
| 三义挂载被混用 | 中 | 每挂载声明各自口径 |

### C.5 总判

**部分支持**:存量四维全量即期可交（复合公式有 RIS/GII 权威背书）,流量维未填充 + 投入翼缺失 + 三义挂载三因压档。升档第一杠杆是上游填充 new 列（或差分自救先行）。复合件「降档不在公式在原料」的结论为批内同类件通用。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INNOV_004.py` | 退出码 0，落 `_out.json` |
| 数据入口 | jiuxin 直连只读;gkx/dev information_schema | demo_* 直接 raise |
| 口径 A 复算 | China 四维归一分和 ÷4 | 84.4902 ✓ |
| 口径 B 复算 | HK inbound 21 归一 | 27.2727 ✓ |
| 与 002 互恰 | 中国论文/2025 合计 | 533,316/1,287,996 ✓ |
| 判档一致 | MD 文首 vs 产物 `support_judgment` | 部分支持 |
| mock 残留检查 | `rg "reservationTotal / 8" repos/demo-ui-science/src` | 正式版替换后无代理伪值 |
