# 学者研究方向总体分布·领域构成（M_SCIUI_TALENTPF_003）

> **类型**：无业务逻辑数值类（构成分布卡）｜ **域**：科技信息展示系统·重点科技人才画像·研究领域图谱（分层展示）｜ **UI 挂载**：科技信息展示系统 → 重点科技人才画像 → 研究领域图谱 → `ProfileFieldMapPanel.jsx:9`（DRILL_LEVELS[0]「overview 总体方向」+ 主题演化堆叠面积图）
> **数据支持度**：**完全转换支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径；「领域构成」为派单书定名口径，双口径并列待裁）｜ **口径归属**：需求明列行为叶（主需求 :2251 多级展开「支持从专家总体研究方向逐级深入细分学科领域」——「总体研究方向」明列），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TALENTPF_003.py`｜ **产物**：`code/M_SCIUI_TALENTPF_003_out.json`
> **四判定摘要**：直接结构 = 无（「构成分布」现成结果面三源均无）；直接数据 = 无（同左）；依赖结构 = 是（久新 OpenAlex 四级维表 + potential_result 主领域 + yearly_discipline 年度聚合面三层结构在）；依赖数据 = 是（field 维 26 个、主领域覆盖 99,998/100,000 即 100.0%、年度面 3,790,547 行 12 个年份全在）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev`）逐一探针留证；`demo_*` 禁引。三源中久新为领域构成数据源（gkx/dev 零承载不影响判档，探针留证在案）。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。** 三源均无现成「学者领域构成分布」结果面（一条 GROUP BY 即得、但确实未物化），但依赖侧结构+数据双达标且**现转已跑通**：领域体系用 OpenAlex 四级（domain 4 / field 26 / subfield 252 / topic 4,516——久新维表实测与 OpenAlex 官方层级逐层吻合），人才级主领域承载在 `ads_talent_potential_result.primary_field_id`（非空 99,998/100,000，派生键 `jiuxin_primary_field_coverage_pct=100.0`，四舍五入显示值；注意 `ads_talent_profile` 无此列——主领域不在主画像），年度构成承载在 `ads_talent_yearly_discipline`（3,790,547 行、99,998 人、2015-2026 共 12 个年份）。**双口径现转读数均落产物**：口径 A（人才×年×Field 去重行构成，演化面积图数据源）Top1 领域占比 11.1%（420,750/3,790,547）；口径 B（Primary Field 构成，每人才每年唯一主领域 is_primary_discipline=1，schema 明载按 paper_count DESC 确定唯一）Top1 占比 3.39%（128,595/3,790,547）。gkx 零承载已探针留证（dwd_scholar/dwd_scholar_papers 列级三零）；dev 命中 4 表均为元数据/主题级非学者领域面——按三源铁律，久新即数据源，判完全转换支持。

### 批次通用纪律摘要（S3-03 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实；久新表数写「实测 210 张（探测日）」 |
| B3 | 同基相除 | 三个派生比分子分母均同表同 WHERE（99,998/100,000；420,750/3,790,547；128,595/3,790,547） |
| B4 | 负结论带探针 | gkx/dev 零承载与需求算式缺的 absence_probe（§3.3） |
| B5 | 确定性 | Top12 双键排序（计数降序+field_id 升序）；维表样例按 field_id 升序 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 改脚本→重跑；产物零手改 |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | 2026 为 PARTIAL_YEAR（schema 口径只展示不入正式对比），构成读数按 2025 完整年切片 |
| B10 | 口径裁定保守交付 | 构成算式双口径并列（A 人才行构成 / B 主领域构成），选型留裁定；升档/降档触发器写死 |
| B11 | 多本账互推 | field 26/subfield 252 与 OpenAlex 官方层级及 X_015 件对账零漂移 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 依赖结构+数据双够吗？ | 双够 | 维表 4 层 + 主领域 100.0% + 年度面 3,790,547 行（§2.2/§2.3） |
| 现转跑通了吗？ | 跑通 | 双口径 Top12 + 2025 切片 + 演化序列全落产物（§2.3/§2.4） |
| 有现成结果面吗？ | 无（故非完全直接） | 三源无物化「构成分布」面，本件 GROUP BY 现转 |

## 摘要

「学者研究方向总体分布（领域构成）」是研究领域图谱分层展示的第一级：`ProfileFieldMapPanel.jsx:9` DRILL_LEVELS 首项「总体方向」（overview），配主题演化堆叠面积图（按 label 堆叠各年份 count，data.js:904-908 researchEvolution mock）。需求侧「总体研究方向」明列（主需求 :2251 多级展开「支持从专家总体研究方向逐级深入细分学科领域、核心关键词及不同阶段关注点」），「领域构成」为派单书定名的构成面口径——构成算式（按人才数还是按论文数）需求无定义，本件双口径并列。数据侧久新三层结构齐备：OpenAlex 四级维表（field 26 个，与官方层级逐层吻合）、人才级主领域（potential_result.primary_field_id 99,998/100,000 非空）、年度聚合面（yearly_discipline 3,790,547 行、2015-2026 十二年）。双口径现转读数：口径 A Top12 领域以工程学 420,750 行居首（Top1 占比 11.1%）；口径 B 主领域构成医学 128,595 行居首（Top1 占比 3.39%）——两口径排序不同（医学在 B 口径居首、A 口径第二）正是「按人还是按行」的口径差实证。2025 完整年切片（工程学论文 377,500/被引 1,209,613）。判**完全转换支持**。脚本已跑通，产物与正文数字逐一对应。

- 需求判定：**需求明列行为叶**（「总体研究方向」在 :2251 明列），构成算式无——双口径并列（B10）。
- 复现状态：脚本已跑通；双口径 Top12、2025 切片、年度序列、维表四层读数全落产物。
- 档位结论：**完全转换支持**（三源无现成面 + 久新依赖结构数据双够 + 现转跑通）。
- 关键事实：`ads_talent_profile` 无 primary_field_id——主领域承载在 potential_result/capability 面，画像面只出人数分母；直查画像面会误判「无领域数据」。
- 口径裁定点：构成算式选 A（人才行）还是 B（主领域）——两口径 Top1 不同（工程学 vs 医学）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技人才态势/**重点科技人才画像·研究领域图谱·研究领域分层展示**（主需求 1.1.1.1.4.3.3.6.1(1) 多级展开）。UI 实际容器是人才画像页研究领域面板（`ProfileFieldMapPanel.jsx`）顶部的 `DRILL_LEVELS` 四级 Segmented——总体方向（overview）/细分学科（discipline）/核心关键词（keyword）/阶段关注（period），本件挂第一级；主体图区是主题演化堆叠面积图（`areaOption`）：panorama+overview 视态下各领域 series 按 `stack: 'total'` 堆叠、x 轴为年份（dataZoom 可缩放）、局部视态取最近年计数 Top2/Top3 聚焦；数据源 `talent.researchEvolution`（mock：fields × 2020-2026 年 × random count）。本件的语义是**个体画像内的领域构成**（该学者各研究方向的数量构成与演化），区别于池级「全库领域分布」——但计算调研落在同一原子问题：人才×领域×年份的构成怎么算。组件还挂分层展开的下钻承诺（总体方向→细分学科→关键词→阶段），OpenAlex 四级体系（domain→field→subfield→topic）与 UI 四级逐级可映射。

### 1.2 为什么需要本指标

领域图谱的业务问题是「这位学者做什么、重心在哪、怎么变的」三问：总体分布回答「做什么」（构成饼/堆叠底），多级展开回答「做到多细」（学科→关键词），动态时间轴回答「怎么变」（年度演化）。需求 :2241 总述把这套能力定位于「为用户提供清晰的学术成长路径和领域分布全貌，助力科技人才评价和学科布局分析」——构成面是演化与下钻的共同地基：没有总体构成，下钻没有入口、演化没有堆叠项。数据侧的关键前置是**领域体系选型**：构成读数的可比性完全取决于分类体系是否标准化（26 个 field 还是自由文本关键词），OpenAlex 四级是当前开放学术数据的事实标准（R2），久新整套维表与之逐层吻合——这让构成读数天然可与国际语料对齐。本件的调研重心因此是「三层链路（维表-主领域-年度面）是否齐、双口径差异有多大、哪些年份可用」。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「总体研究方向」作为行为词明列（:2251），但构成的计数单元（人才数？论文数？人才×年行数？）与归一方式（占比？绝对量？）无一字；:2241 总述的「精准提取专家在不同时期关注的关键词、主题领域以及学科交叉点」是 NLP 侧提取要求（语义识别层），不是统计构成算式。「领域构成」定名在三真源 0 命中（派单书定名）。UI mock 的 random count 是演示值，不构成口径证据。本件按 B10 交双口径（A 人才行构成 / B 主领域构成）。

### 1.4 类似指标权威方法可行性分析概要

「研究领域构成」的权威方法锚分三层。其一，学科分类体系标准：OpenAlex Fields of Study（R2）四级层级（4 domains → 26 fields → 252 subfields → 4,516 topics），每作品经 ML 主题推断获得唯一 primary 归属（刻意设计：按论文自身文本而非期刊学科分类）——久新维表实测 4/26/252/4,516 与官方逐层吻合，构成读数的体系即此标准；其上游是 Scopus ASJC 类目。其二，R&D 统计分类传统：OECD Frascati Manual（R1）确立科技统计的领域分类纪律（分类体系标准化是跨主体可比的前提）——构成读数必须钉在标准分类上而非自由标签。其三，国内学科分类：《学科分类与代码》国家标准（GB/T 13745-2009，方法论背景）给出国内一级/二级/三级学科体系——与 OpenAlex field 级粗粒度可映射但非同物，跨体系对齐属口径裁定。方法族对照：

| 方法族 | 代表 | 体系/规则 | 数据要求 | 与三源匹配 |
|---|---|---|---|---|
| OpenAlex 四级 | R2（官方文档） | 4/26/252/4516 + 唯一 primary | 维表+归属面 | **有**（维表逐层吻合 + 主领域 100.0%） |
| Frascati 分类纪律 | OECD（R1） | 标准化分类前提 | 分类体系 | 有（体系即标准） |
| 国内学科国标 | GB/T 13745（背景） | 一二三级学科 | 映射维表 | 无（需跨体系映射，未立项） |
| 前端演示 | UI random 演化 | — | mock 常量 | 结构披露（不作源） |

结论：体系选型已被库内事实锁定（OpenAlex 四级），双口径差异（§2.3/§2.4）是唯一待裁点。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/talent-trend/components/ProfileFieldMapPanel.jsx:9-12`（DRILL_LEVELS 四级，首项 overview 总体方向）；`:92-113`（areaOption 堆叠面积图，按 label 堆叠各年 count）。
- 数值语义源：`repos/demo-ui-science/src/pages/talent-trend/data.js:904-908`（researchEvolution mock 生成器）。
- 主需求：`科技信息展示系统和科技专题服务系统.md`:2251（多级展开）、:2241（领域图谱总述）、:2255-2257（分类聚合显示/动态时间轴），原文见附录 A。
- 权威方法：R1 OECD Frascati Manual 2015；R2 OpenAlex Fields of Study 官方文档。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（须披露口径不闭合）**——双口径并列：

- **口径 A（人才×年×Field 行构成，演化面积图数据源）**：$C_A(f) = |\{(t, y) : \text{field}(t,y) = f\}|$，即 yearly_discipline 中该领域的去重人才×年份行数；堆叠面积图各 series 的年度值即此口径的年度切片。Top1 占比 11.1%（工程学）。
- **口径 B（Primary Field 构成，每人才每年唯一主领域）**：$C_B(f) = |\{(t, y) : \text{primary\_field}(t,y) = f\}|$（is_primary_discipline=1，schema 明载按 paper_count DESC 确定唯一）；人才级静态构成则用 potential_result.primary_field_id（每人一个主领域，Top12：工程学 17,776/医学 15,911/计算机科学 8,411…）。Top1 占比 3.39%（医学）。
- 两口径分母同（3,790,547 总行数），排序不同是口径差实证：A 口径度量「领域的人年体量」（多领域学者在每领域都计行），B 口径度量「主领域归属」——面积图堆叠用 A、画像卡主领域用 B，混用即错。

**降档/升档触发器**：①甲方裁定构成算式（A 或 B）→ 口径闭合，仍为完全转换支持（现转已通，无档位变化）；②若要求「按论文数构成」→ yearly_discipline 的 paper_count 列在（2025 切片已落产物），第三口径零成本可加；③若要求国内学科国标体系 → 需跨体系映射维表（未立项），在该映射建成前维持 OpenAlex 体系口径。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在需求文档 | 主需求《科技信息展示系统和科技专题服务系统.md》 |
| 所属四级功能 | 1.1.1.1.4.3.3 重点科技人才画像（4 个 L5） |
| 所属 L5 | 研究领域图谱（1.1.1.1.4.3.3.6，4 叶） |
| 本件叶 | **多级展开（.6.1(1)）首级「总体研究方向」——需求明列行为词** |
| 同 L5 相邻叶 | 可视化操作与交互（.2）/ 智能挖掘与趋势分析（.3，TALENTPF_006 热度件承接 .3(3) 动态热点标记）/ 详情展示与溯源（.4） |
| 同面板承接件 | TALENTPF_006（领域热度，同面板 influence 卡）；TALENTREG_001（基础面板成果卡） |
| UI 容器 | `ProfileFieldMapPanel.jsx:9` DRILL_LEVELS 首项 + 演化面积图 |

本件与 TALENTPF_006 共享领域年度面（yearly_discipline）与维表族——006 是热度的「时间导数侧」（增长/份额），本件是构成的「存量侧」（分布/占比），族内读数零漂移；与 X_015 件（subfield 级 252 读数）同体系不同层（field vs subfield）。

## 二、计算过程

### 2.1 方法选择（文献依据）

体系选 **OpenAlex Fields of Study 四级**（R2）：选择理由有三——其一，久新维表与官方层级逐层吻合（4/26/252/4,516，§2.2 实测），体系已工程化落地，无需自建分类；其二，R2 的「唯一 primary 归属」设计（按论文自身文本而非期刊学科）与库内 is_primary_discipline=1（按 paper_count DESC 确定唯一）同构，主领域口径有官方语义；其三，Frascati 分类纪律（R1）要求构成统计钉在标准分类上，OpenAlex 四级即当前开放学术数据的事实标准。构成算式双口径（A 人年行 / B 主领域）并列，依据需求原文无算式（B10）——A 口径服务演化面积图（堆叠项需覆盖学者全部领域年行），B 口径服务画像主领域卡（每人唯一归属），两口径用途不同不互替。

### 2.2 装载与三层链路定位

经 `_gkxdb.py` 连 gkx、直连 dev 与久新（三源串行只读）。久新实测 210 张表（探测日）。三层链路逐一实测：**维表层**——`ads_discipline_domain` 4 行 / `ads_discipline_field` 26 行 / `ads_discipline_subfield` 252 行 / `ads_discipline_topic` 4,516 行，与 OpenAlex 官方四级（4 domains → 26 fields → 252 subfields → 4,516 topics，R2）逐层吻合；field 维表样例（field_id 升序前 5）：神经科学/化学/计算机科学/化学工程/物理学与天文学（fld_* 哈希 ID + 中英双名）。**主领域层**——`ads_talent_profile`（100,000 行）**无 primary_field_id 列**（实测登记 0），人才级主领域承载在 `ads_talent_potential_result`（100,000 行，primary_field_id 非空 99,998）；**年度面层**——`ads_talent_yearly_discipline` 3,790,547 行、去重人才 99,998 人、年份 2015-2026 共 12 档（`jiuxin_yearly_discipline_years`），fld_* 哈希 ID 与 potential_result 同体系可直接 JOIN。三层齐备 + ID 体系同源，构成读数的转换链一条 JOIN + 一条 GROUP BY 即闭合。

### 2.3 口径 B：主领域构成读数（现转）

人才级主领域构成（potential_result.primary_field_id 全年面，JOIN field 维表取名，人数降序 Top12）：工程学 17,776 / 医学 15,911 / 计算机科学 8,411 / 生物化学·遗传学与分子生物学 8,023 / 农业与生物科学 6,024 / 环境科学 5,902 / 材料科学 5,868 / 物理学与天文学 4,271 / 社会科学 3,491 / 地球与行星科学 2,915 / 化学 2,843 / 商业·管理与会计 2,763。年度形态（is_primary_discipline=1 的 yearly_discipline 行）Top5：医学 128,595 / 工程学 102,464 / 计算机科学 73,691 / 生化遗传 69,172 / 环境科学 63,988——派生键 `jiuxin_yd_primary_top1_field_share_pct=3.39`（128,595/3,790,547）。注意人才级与年度级 B 口径的 Top1 不同（工程学 vs 医学）：年度面按「每年主领域」计行（学者主领域跨年漂移会逐年计行），人才级按「当前主领域」计人——两形态都落产物，用途区分随行披露。

```sql
SELECT p.primary_field_id, f.name_zh, COUNT(*) AS talents
FROM ads_talent_potential_result p
LEFT JOIN ads_discipline_field f ON f.field_id = p.primary_field_id
WHERE p.primary_field_id IS NOT NULL
GROUP BY p.primary_field_id, f.name_zh
ORDER BY COUNT(*) DESC, p.primary_field_id ASC LIMIT 12;
-- → 工程学 17776 / 医学 15911 / 计算机科学 8411 / …（B5 双键排序）
```

### 2.4 口径 A 与年度演化序列（面积图数据源）

口径 A（人才×年×Field 去重行构成）Top12：工程学 420,750 / 医学 363,527 / 生化遗传 316,759 / 环境科学 237,259 / 材料科学 234,424 / 计算机科学 234,382 / 农业与生物科学 180,593 / 社会科学 168,815 / 化学 166,644 / 物理学与天文学 143,298 / 神经科学 132,077 / 免疫与微生物（fld_c636…）118,564——派生键 `jiuxin_yd_top1_field_share_pct=11.1`（420,750/3,790,547）。A/B 排序差实证：医学在 B 主领域口径居首（15,911 人）、在 A 行口径第二（363,527），工程学反转——多领域学者（每年多个领域行）在 A 口径按领域逐行计入、在 B 口径只计主领域。**2025 完整年切片**（演化面积图最近可用年，576,621 行）：按论文数 Top12 工程 377,500（被引 1,209,613）/医学 323,175（874,191）/生化遗传 213,573（576,747）/材料 187,548（789,754）/计算机 158,169（314,053）……第三口径（论文数构成）的物料同面齐备。2026 年在年度序列中存在但按 schema 口径 PARTIAL_YEAR 只展示不入正式对比，构成读数不取 2026。

### 2.5 三源排除探针

**gkx**：280 表 scholar×field/keyword/topic/discipline 交叉词族 0 命中；`dwd_scholar` 27 列与 `dwd_scholar_papers` 列级 field/discipline/topic/keyword/direction 词族均 0 命中（`gkx_scholar_field_like_cols=[]` / `gkx_scholar_papers_field_like_cols=[]`）——gkx 学者域无结构化学科列，构成只能从论文文本（zh_abstract/en_abstract）自建分类，属重工程非现成。**dev**：field/keyword/topic/discipline 词族命中 5 表——`gkxlumenx_ads.topic_burst`（主题突发，主题级无人才绑定）、`gkxlumenx_dwd.industry_analysis_topics`（产业分析主题）、`gkxlumenx_bi.jimu_report_db_field` / `gkxlumenx_codegen.gen_field_type`（报表与代码生成器元数据）等，均非学者领域业务面，不构成本件承载。**久新**：三层链路全在（§2.2）——按三源铁律，久新即数据源，gkx/dev 零承载不降档（探针留证在案）。

### 2.6 稳健性与口径敏感性

四个敏感性登记：其一，A/B 口径 Top1 反转（工程学 vs 医学）——UI 选错口径会把「主领域第一」显示成「人年体量第一」，两口径不得混用（§2.4 实证）；其二，人才级 vs 年度级 B 口径也有形态差（当前主领域 vs 每年主领域，跨年漂移学者在年度形态多计行）；其三，PARTIAL_YEAR 纪律——2026 行只展示不入构成读数，正式构成切片取 2025；其四，OpenAlex ML 主题推断的体系性偏差（R2 披露：按论文文本分类，跨学科论文只获唯一 primary）——跨学科高频领域（如生物信息）的构成会被 single-primary 设计压低，这是体系内生偏差，登记不修正。所有敏感性随口径裁定（触发器①）一次性关闭。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TALENTPF_003.py`（三源串行只读；gkx 经 `_gkxdb.py`；dev/久新直连；零 `demo_*`）；运行 `python3 code/M_SCIUI_TALENTPF_003.py`。
- 产物：`code/M_SCIUI_TALENTPF_003_out.json`。正文数字与产物键逐一对应：`jiuxin_table_count=210`（§2.2，探测日）、维表四键 `jiuxin_ads_discipline_domain_rows=4` / `jiuxin_ads_discipline_field_rows=26` / `jiuxin_ads_discipline_subfield_rows=252` / `jiuxin_ads_discipline_topic_rows=4516` + `jiuxin_field_dim_sample5`（§2.2）、`jiuxin_profile_rows=100000` + `jiuxin_profile_primary_field_id_nonnull=0`（列不存在登记）+ `jiuxin_potential_result_rows=100000` + `jiuxin_potential_pf_nonnull=99998` + 派生键 `jiuxin_primary_field_coverage_pct=100.0`（§2.2）、`jiuxin_potential_primary_field_top12` 十二组（§2.3）、`jiuxin_yearly_discipline_rows=3790547` + `jiuxin_yearly_discipline_talents=99998` + `jiuxin_yearly_discipline_years`（2015-2026 十二档）+ `jiuxin_yd_talentyear_by_field_top12`（口径 A）+ `jiuxin_yd_primary_by_field_top12`（口径 B 年度形态）+ 派生键 `jiuxin_yd_top1_field_share_pct=11.1` + `jiuxin_yd_primary_top1_field_share_pct=3.39`（§2.4）、`jiuxin_yd_2025_rows=576621` + `jiuxin_yd_2025_field_papers_cites_top12`（§2.4）、`jiuxin_topic_profile_rows=6846951` + `jiuxin_topic_profile_talents=99998`（更细粒度可选面）、`gkx_table_count=280` + `gkx_talent_field_like_tables=[]` + `gkx_scholar_field_like_cols=[]` + `gkx_scholar_papers_field_like_cols=[]` + `dev_field_like_tables`（4 张非业务面）（§2.5/§3.3）。
- 结果解读：三层链路读数（维表四层吻合官方、主领域 100.0%、年度面 12 年全）+ 双口径 Top12（A/B 排序差实证）+ 2025 完整年切片——构成读数的转换链全通。
- 对照需求功能要求的评审：「支持从专家总体研究方向逐级深入细分学科领域、核心关键词及不同阶段关注点」——**满足**：总体构成（本件双口径现转）+ 下钻物料（subfield 252/topic 4,516 维表 + topic_profile 6,846,951 行更细粒度面）+ 时间轴（2015-2026 年度面）；「按需放大至单一主题或时段的领域分布」——满足（年度面按 field×year 切片即得）。待裁点仅构成算式选型（A/B/论文数三候选）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | 久新实测表数 | `jiuxin_table_count` | 210（探测日） |
| 维表 | 四级层级行数 | `jiuxin_ads_discipline_*_rows` | 4 / 26 / 252 / 4,516（=OpenAlex 官方） |
| 维表 | field 样例 | `jiuxin_field_dim_sample5` | 神经科学/化学/计算机科学/…（中英双名） |
| 主领域 | potential 覆盖 | `jiuxin_potential_pf_nonnull` / `_rows` | 99,998 / 100,000（100.0%） |
| 主领域 | 画像列缺失 | `jiuxin_profile_primary_field_id_nonnull` | 0（列不存在，承载面在 potential） |
| 口径 B | 人才级 Top12 | `jiuxin_potential_primary_field_top12` | 工程学 17,776 / 医学 15,911 / … |
| 口径 B | 年度形态 Top1 | `jiuxin_yd_primary_by_field_top12[0]` | 医学 128,595（占比 3.39%） |
| 口径 A | 人年行 Top1 | `jiuxin_yd_talentyear_by_field_top12[0]` | 工程学 420,750（占比 11.1%） |
| 年度面 | 总行数/人才/年份 | `jiuxin_yearly_discipline_rows/_talents/_years` | 3,790,547 / 99,998 / 2015-2026（12 档） |
| 切片 | 2025 行数 | `jiuxin_yd_2025_rows` | 576,621 |
| 切片 | 2025 论文 Top1 | `jiuxin_yd_2025_field_papers_cites_top12[0]` | 工程学 377,500 篇 / 被引 1,209,613 |
| 细粒度 | topic_profile 面 | `jiuxin_topic_profile_rows/_talents` | 6,846,951 / 99,998 |
| 排除 | gkx 列级三零 | `gkx_talent_field_like_tables` 等三键 | [] / [] / [] |
| 排除 | dev 命中定性 | `dev_field_like_tables` | 4 张（元数据/主题级，非承载） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 领域体系维表 | jiuxin | `ads_discipline_*` 四表 | 4/26/252/4,516 | 直查 | **有（=OpenAlex 官方层级）** |
| D2 | 人才级主领域 | jiuxin | `potential_result.primary_field_id` | 99,998（100.0%） | 直查 | **有** |
| D3 | 年度构成面 | jiuxin | `ads_talent_yearly_discipline` | 3,790,547（99,998 人×12 年） | 直查/聚合 | **有** |
| D4 | 细粒度可选面 | jiuxin | `ads_talent_topic_profile` | 6,846,951 | 直查 | 有（topic 级下钻） |
| D5 | 现成「构成分布」结果面 | 三源 | — | — | **不存在** | 无（现转即得，故非完全直接支持） |
| D6 | gkx 学科结构列 | gkx | `dwd_scholar`/`dwd_scholar_papers` | — | **不存在** | 无（久新替代，探针在案） |
| D7 | UI 演示值 | UI | data.js researchEvolution | — | mock | 边界证据（不作源） |

`support_judgment="完全转换支持"`、产物与文首一致。

### 3.2 D1-D3 三层链路的覆盖与量级（久新）

三层链路的「结构+数据」双达标是本件判档的支撑面：维表四层与 OpenAlex 官方逐层吻合（4/26/252/4,516，R2 文档数字——含久新侧对 X_015 件 subfield 252 读数的同源对账）；主领域 99,998/100,000（100.0%）近满覆盖（缺 2 人为领域判定不合格者）；年度面 3,790,547 行均摊 99,998 人×12 年≈每人每年 3.2 个领域行——多领域覆盖（非仅主领域）正是口径 A 的语义基础。ID 体系同源（fld_* 哈希）使 potential↔yearly_discipline JOIN 零转换成本。

### 3.3 D5/D6 非承载侧的 absence_probe 全记录

否定性证据三件套：**查了什么**——gkx 280 表 scholar×field/keyword/topic/discipline 交叉词族 + `dwd_scholar` 27 列与 `dwd_scholar_papers` 全列列级词族；dev `gkxlumenx_*` field/keyword/topic/discipline 词族；三份需求真源「领域构成/总体分布」算式检索。**条件**——表级+列级存在性 + 需求算式命中。**命中**——gkx 三零（表/两表列）；dev 5 表均为元数据或主题级非学者领域面（topic_burst 主题级无人才绑定、jimu_report_db_field 报表元数据等）；需求侧 hits=1（:2251 行为词命中，构成算式无定义）。缺失情形归属：D5 属「未物化」——数据全在依赖面，一条 GROUP BY 可得（这正是完全转换支持的判据）；D6 属「列不存在」——gkx 侧修复须自建文本分类（重工程），但三源铁律下久新已承载，不构成缺口。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| 维表四层 | 4/26/252/4,516 = OpenAlex 官方（R2）逐层吻合 |
| 主领域覆盖 | 99,998/100,000 = 100.0%（显示值；实际缺 2） |
| 年度面年份 | 2015-2026 共 12 档（2026 PARTIAL_YEAR 不入构成） |
| 2025 切片 | 576,621 行；工程学论文 377,500/被引 1,209,613 |
| 双口径排序差 | A 首工程学（11.1%）vs B 首医学（3.39%）——口径差实证 |
| gkx 列级 | 两表词族列 0 命中 |
| 脚本形态 | 三源串行只读；零 demo_* |

## 四、数据缺失情况

### 4.1 现成结果面未物化（唯一「缺」，轻量）

三源无物化的「学者领域构成分布」结果面——但依赖面（维表+主领域+年度面）数据全、ID 同源、SQL 一条 GROUP BY 即得（本件已跑通双口径）——这是「未物化」而非「缺数据」，正是完全转换支持的教科书判据。若上线高频查询，建议把双口径构成预聚合到 ADS 中间表（工程量小）。

### 4.2 口径与体系裁定点（待裁，非缺）

两个待裁点：其一，构成算式三候选（A 人年行 / B 主领域 / 论文数）——A/B Top1 反转实证已交付，选型权在甲方（触发器①/②）；其二，国内学科国标体系映射（GB/T 13745 → OpenAlex field）未立项——若甲方要求国内学科话语体系，需建跨体系映射维表（触发器③）。两待裁点均不阻塞即期交付（OpenAlex 体系 + 双口径并列可先上）。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径裁定（触发器①②） | 口径裁定 | 本件即期 | A/B/论文数三选一或双轨 |
| 构成预聚合中间表 | ADS 工程 | 本件 + 画像页性能 | 高频查询物化 |
| 国标学科映射维表 | 映射工程 | 本件 + 学科话语体系 | 触发器③（中期） |
| 2026 年回补 | 上游数据 | 年度序列 | PARTIAL_YEAR 转正式年后自动并入 |

档位说明：本件已处**完全转换支持**，上述动作不升档（本档即「现转可得」顶档的下一档是完全直接支持——需物化结果面，预聚合表落地后即达）。

## 参考文献

1. OECD. Frascati Manual 2015: Guidelines for Collecting and Reporting Data on Research and Experimental Development[EB/OL]. OECD. https://www.oecd.org/en/publications/frascati-manual-2015_9789264239012-en.html （R1，2026-11-01 WebSearch 核验可达——R&D 统计的国际标准，领域分类体系标准化是构成统计跨主体可比前提的纪律来源）
2. OpenAlex. Fields of Study: Domains, Fields, Subfields, Topics[EB/OL]. OpenAlex Help. https://help.openalex.org/data/fields/ （R2，2026-11-01 WebSearch 核验可达——四级层级官方文档（4 domains → 26 fields → 252 subfields → 4,516 topics）与「唯一 primary 归属按论文自身文本」设计，久新维表与主领域口径的体系真源；subfield/domain 页同站核验）
3. 中华人民共和国国家质量监督检验检疫总局. 学科分类与代码（GB/T 13745-2009）[EB/OL]. 国家标准全文公开系统. https://openstd.samr.gov.cn/ （R3，2026-11-01 WebSearch 核验可达——国内一二三级学科分类国标，跨体系映射（触发器③）的目标话语体系）

# 附件

## 附录 A 原始需求原文摘录

主需求《科技信息展示系统和科技专题服务系统.md》:2251（1.1.1.1.4.3.3.6.1(1) 多级展开）：

> 支持从专家总体研究方向逐级深入细分学科领域、核心关键词及不同阶段关注点，用户可按需放大至单一主题或时段的领域分布。

:2241（研究领域图谱总述）：

> 研究领域图谱通过自然语言处理（NLP）、主题建模等技术，对专家发表的论文进行深度语义分析和内容挖掘，自动识别并梳理其研究兴趣的演变轨迹。……精准提取专家在不同时期关注的关键词、主题领域以及学科交叉点，动态捕捉其学术方向的变化和拓展。……将专家研究领域的发展趋势和兴趣热点以图形化方式直观展现，为用户提供清晰的学术成长路径和领域分布全貌，助力科技人才评价和学科布局分析。

:2255-2257（分类聚合显示/动态时间轴）：

> 按学科类别、主题标签等维度将所有研究领域自动聚合分组，清晰展现专家学术兴趣的分布格局和演变脉络。
> 以时间线方式动态展示专家在各研究方向上的关注变化，实现不同年份领域热点的对比与追溯。

「领域构成」定名在三真源 0 命中（派单书定名）；「总体研究方向」行为词 :2251 明列——构成算式（按人才数/论文数）无定义。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 领域构成 | 三份需求真源 | 0（派单书定名） |
| 研究方向总体分布 | 三份需求真源 | 0（卡片级） |
| 总体研究方向 | 主需求 | :2251（多级展开首级，明列） |
| 分布格局 | 主需求 | :2255（分类聚合显示） |
| 领域分布全貌 | 主需求 | :2241（总述） |
| researchEvolution | UI data.js | :904-908（mock 生成器） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TALENTPF_003_out.json`（2026-11-01 实跑：维表四层 + 双口径 Top12 + 2025 切片 + 三源排除）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（久新 talent 族表清单——B11 锚）。
- 族内对账：subfield 252（=X_015 件同读数）；yearly_discipline/potential_result/维表族（=TALENTPF_006 件共享面，零漂移）。

### B.2 本件产物逐键清单（`code/M_SCIUI_TALENTPF_003_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.jiuxin_table_count` | 计数 | 210（探测日实测） | §2.2 |
| `facts.jiuxin_ads_discipline_domain_rows` | 计数 | 4 | §2.2/§3.2 |
| `facts.jiuxin_ads_discipline_field_rows` | 计数 | 26 | §2.2/§3.2 |
| `facts.jiuxin_ads_discipline_subfield_rows` | 计数 | 252 | §2.2/§3.2 |
| `facts.jiuxin_ads_discipline_topic_rows` | 计数 | 4,516 | §2.2/§3.2 |
| `facts.jiuxin_field_dim_sample5` | 样例 | 5 组（中英双名） | §2.2 |
| `facts.jiuxin_profile_rows` | 计数 | 100,000 | §2.2 |
| `facts.jiuxin_profile_primary_field_id_nonnull` | 探针 | 0（列不存在登记） | §2.2/§3.2 |
| `facts.jiuxin_potential_result_rows` | 计数 | 100,000 | §2.2 |
| `facts.jiuxin_potential_pf_nonnull` | 覆盖 | 99,998 | §2.2 |
| `facts.jiuxin_potential_primary_field_top12` | 分布 | 12 组（人才级口径 B） | §2.3 |
| `facts.jiuxin_yearly_discipline_rows` | 计数 | 3,790,547 | §2.4/§3.2 |
| `facts.jiuxin_yearly_discipline_talents` | 计数 | 99,998 | §2.4 |
| `facts.jiuxin_yearly_discipline_years` | 序列 | 2015-2026（12 档） | §2.4 |
| `facts.jiuxin_yd_talentyear_by_field_top12` | 分布 | 12 组（口径 A） | §2.4 |
| `facts.jiuxin_yd_primary_by_field_top12` | 分布 | 12 组（口径 B 年度形态） | §2.3/§2.4 |
| `facts.jiuxin_yd_2025_rows` | 计数 | 576,621 | §2.4 |
| `facts.jiuxin_yd_2025_field_papers_cites_top12` | 分布 | 12 组（论文/被引） | §2.4 |
| `facts.jiuxin_topic_profile_rows` | 计数 | 6,846,951 | §2.7 |
| `facts.jiuxin_topic_profile_talents` | 计数 | 99,998 | §2.7 |
| `facts.gkx_table_count` | 计数 | 280 | §2.5 |
| `facts.gkx_talent_field_like_tables` | 探针 | [] | §2.5/§3.3 |
| `facts.gkx_scholar_field_like_cols` | 探针 | [] | §2.5/§3.3 |
| `facts.gkx_scholar_papers_field_like_cols` | 探针 | [] | §2.5/§3.3 |
| `facts.dev_field_like_tables` | 探针 | 4 张（非业务面） | §2.5/§3.3 |
| `derived[0].jiuxin_primary_field_coverage_pct` | 派生比 | 100.0（99,998/100,000） | §2.2 |
| `derived[1].jiuxin_yd_top1_field_share_pct` | 派生比 | 11.1（420,750/3,790,547） | §2.4 |
| `derived[2].jiuxin_yd_primary_top1_field_share_pct` | 派生比 | 3.39（128,595/3,790,547） | §2.3/§2.4 |
| `absence_probe` | 探针 | 三件（gkx/dev/doc） | §3.3 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

### B.3 共享与族内读数消费

本件消费族内锚：subfield 252（=X_015 件）、yearly_discipline 3,790,547 与维表族（=TALENTPF_006 件）、potential_result 100,000（=013 件 cohort 机制面）——批内零漂移（B11）。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 体系/规则 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| OpenAlex 四级体系 | R2 官方文档 | 4/26/252/4516 + 唯一 primary | 维表逐层吻合 + is_primary 同构 | **最高（体系已落地）** |
| Frascati 分类纪律 | OECD（R1） | 标准分类前提 | 体系即标准 | 高（纪律来源） |
| 国内学科国标 | GB/T 13745（R3） | 一二三级学科 | 需映射维表（未立项） | 中（触发器③） |
| 前端演示 | UI random 演化 | — | mock 常量 | 结构披露（不作源） |

### C.2 数据矩阵

| 依赖 | gkx | dev | jiuxin |
|---|---|---|---|
| 领域维表（四级） | 无 | 无 | **4/26/252/4,516** |
| 人才级主领域 | 无列 | 无 | **99,998（100.0%）** |
| 年度构成面 | 无列 | 无 | **3,790,547（12 年）** |
| topic 级细粒度 | 无 | 主题级无人才绑定 | 6,846,951 |
| 现成构成结果面 | 无 | 无 | 无（现转即得） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 双口径构成（A/B 并列）+ 2025 切片 + 演化序列接入面积图 | 口径裁定（触发器①②） |
| v2 | 构成预聚合 ADS 中间表（高频查询物化） | ADS 工程 |
| v3 | 国标学科映射双体系展示 | 映射维表立项（触发器③） |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| A/B 口径混用（Top1 反转） | **高** | 双口径并列交付 + UI 用途绑定（面积图 A/画像卡 B） |
| 2026 行误入构成读数 | 中 | PARTIAL_YEAR 纪律随行；切片固定 2025 |
| single-primary 压低跨学科领域 | 中 | 体系内生偏差登记（R2 披露） |
| 画像面误判「无领域数据」 | 中 | §2.2 写死承载面在 potential_result |

### C.5 总判

**完全转换支持**：三源无现成面但久新三层链路（维表-主领域-年度面）结构+数据双达标、ID 同源、双口径现转跑通；gkx/dev 零承载已探针留证（久新即数据源）。待裁点仅构成算式选型（三候选）与国标映射（中期），不阻塞即期交付。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TALENTPF_003.py` | 退出码 0，落 `_out.json` |
| 数据入口 | `_gkxdb.py`（gkx）+ 直连 dev/久新 | demo_* 直接 raise |
| 判档一致 | 文首 vs `support_judgment` | 完全转换支持 |
| B11 对账 | field 26/subfield 252=OpenAlex 官方=X_015；年度面=006 件 | 零漂移 |
| 幂等重跑 | SQL 全只读无随机 | 逐位一致 |
| 伪分残留 | 无评分合成 | 无伪值 |
| mock 残留检查 | `rg "researchEvolution" repos/demo-ui-science/src/pages/talent-trend` | 正式版替换后无引用 |
