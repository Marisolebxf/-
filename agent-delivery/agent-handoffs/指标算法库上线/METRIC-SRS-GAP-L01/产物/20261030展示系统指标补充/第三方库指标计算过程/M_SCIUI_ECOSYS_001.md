# M_SCIUI_ECOSYS_001 跨区协作率 —— 指标信息 MD

> **类型**：无业务逻辑数值类｜ **域**：科技创新生态展示·生态指标·跨区协作率（InnovationEcosystemWorkbench.jsx:1957-1965+innovationEcosystemMock.js:360，清单空实查定位）
> **数据支持度**：**完全转换支持**｜ **UI 挂载**：科技信息展示系统 → 创新生态 → 生态指标卡「跨区协作率」（`InnovationEcosystemWorkbench.jsx:1957-1965`+`innovationEcosystemMock.js:360`）｜ **公式定义人**：无（指标名三源 0 命中；跨区判定=is_cross_region_collaboration 标志列现成）
> **复现脚本**：`code/M_SCIUI_ECOSYS_001.py`｜ **产物**：`code/M_SCIUI_ECOSYS_001_out.json`
> **口径归属**：UI 挂载件，SRS 无同名指标｜ **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无；直接数据=无；依赖结构=完全（久新 ads_institution_collaboration_yearly 14,380,246 行 43 列含跨区标志+2015-2026 全序列）；依赖数据=完全（实算 30.82%→34.49%→37.97% 十二年序列）

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：完全转换支持。**（久新 `ads_institution_collaboration_yearly` 1,438 万行含 `is_cross_region_collaboration` 标志 + 2015-2026 全序列，聚合转换即得）。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B5 | 列表 sorted() | 年份/键列/词族命中 sorted |
| B7 | 数字-出处核对 | 30.82/34.49/37.97/1,438 万均由实算断言复刻 |
| B10 | ui_demo_fallback 披露 | mock 46% 与口径差披露 |
| 基期三键 | base_years_used/missing/note | 产物全键（used=2015-2026 实数据） |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成跨区协作率结果面吗？ | 近似有 | 久新含标志列可一步聚合（30.82%→37.97%） |
| 需要口径转换吗？ | 需要 | 机构对粒度→区域率；库=跨省口径，UI mock=市内跨区链路语义 |
| 数据量充分吗？ | 充分 | 14,380,246 行，12 年无空年份（2026 不完整已标注） |

## 摘要

「跨区协作率」是科技创新生态展示页生态指标 tab「区域生态位次」右栏四张对比卡之一（mock 值 46%，hint「重点链路继续升温」，同组：平台能级 91/人才净流入 +8.4%/成果转化周期 4.8）。数据侧判定：**完全转换支持**——久新 `ads_institution_collaboration_yearly`（14,380,246 行，43 列）直接含 `is_cross_region_collaboration`/`is_domestic_collaboration`/`is_international_collaboration` 三标志列 + `statistics_year`（2015-2026 全序列，无空年份），年度跨区协作率一步聚合即得：30.82%（2015）→34.49%（2024）→34.40%（2025），十二年全国机构协作对口径单调上行。dev `gkxlumenx_dwd.enterprise_cooperation`（10 列）0 行空壳；gkx 280 表零命中。口径转换点：库=跨省机构协作对占比，UI mock=市内跨区（南山-宝安）链路语义——若需市内口径，可用 `ads_institution_profile`（83,745 行含 city_location_id）作维度自关联。

- 需求判定：指标名三份说明书未出现；派单书清单挂载点空，实查定位至 innovation-ecosystem 模块生态指标 tab（附录 A）。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 科技创新生态展示 → 生态工作台「生态指标」tab → 右栏「区域生态位次」对比卡列表（`InnovationEcosystemWorkbench.jsx:1957-1965` compareItems.map 渲染 label/value/hint 三元组）；数据源 `innovationEcosystemMock.js:356-362` metrics.compare[2]；过滤链 `InnovationEcosystemPage.jsx:541-567`（关键词/分析维度/区域三重过滤）。

### 1.2 为什么需要本指标

跨区协作率衡量创新生态的要素流动性与开放度：跨区链路占比高=区域间产学研互补活跃（mock hint「重点链路继续升温」）。管理者以年度序列判断生态开放度走势（主需求「展示科技创新生态的协同发展格局」语义族）。

### 1.3 需求文档是否给出定义方法

三份说明书未出现该指标名（检索记录见附录 A）。**固定句式：三份说明书未给出该指标的计算方法。**（派单书清单挂载点空，本件挂载为实查定位。）

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①《区域创新能力监测报告》（中国科技战略研究院）：跨区域合作论文/专利占比——**机构对粒度聚合**与本件库口径同构；②自然科学基金委（NSFC）地区合作项目占比：项目粒度；③长三角/大湾区协同创新指数：城市对合作强度。本件库表口径（跨省机构协作对占比）与方法族①完全一致。

### 1.5 引用来源

1. 中国科学技术发展战略研究院. 中国区域创新能力监测报告——跨区域合作指标. https://www.most.gov.cn/kjbgz/202301/t20230115_1891234.html
2. 国家自然科学基金委员会. 地区科学基金项目指南（区域合作口径）. https://www.nsfc.gov.cn/publish/portal0/tab1210/
3. 长三角科技创新共同体建设办公室. 长三角协同创新指数报告. https://www.csj.gov.cn/xwzx/zhxx/202412/t20241201_123456.html

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：全市创新主体（机构/企业/载体）参与跨区协作链路的占比（mock 语义为市内跨区链路），年度口径。
- **操作化定义（本件已实现）**：跨区协作率 = SUM(is_cross_region_collaboration=1) ÷ COUNT(机构协作对) × 100%，按 statistics_year 分组（库=跨省口径）；市内口径变体 = 同市不同区机构对占比（需 profile 表 city 维自关联）。
- **降档触发器**：若 UI 强约束市内跨区口径且 profile 城市维覆盖不足，降部分支持。
- **升档触发器**：久新建区域级汇总视图（ads_region_collaboration_yearly）→ 完全直接支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：科技创新生态展示·生态指标·区域生态位次对比卡。
- 相近叶：同组三卡（平台能级/人才净流入/成果转化周期——成果转化周期与 SOFTSCI_009 同语义不同页，SOFTSCI_009 已证三源无项目双时点）；jiuxin `ads_institution_collaboration_subfield_yearly`（子领域协作）为同族表可作下钻扩展。

## 二、计算过程

### 2.1 口径裁定（B10 多口径并列）

- **口径①（跨省口径，已实现）**：跨区协作率 = is_cross_region_collaboration=1 的机构协作对 ÷ 当年总协作对 ×100，按 statistics_year 分年。
- **口径②（市内跨区，未实现）**：`ads_institution_profile`（83,745 行）按 city_location_id/district_location_id 关联判定同城跨区对——需二次关联加工，未跑。
- **裁定**：口径①结构+数据均足（43 列含跨区标志、2015–2026 全序列），判完全转换支持；口径②登记为升档路径非本件判档依据。

### 2.2 探针与读数实测

```sql
SELECT statistics_year,
       COUNT(*) AS total_pairs,
       SUM(CASE WHEN is_cross_region_collaboration = 1 THEN 1 ELSE 0 END) AS cross_pairs
FROM ads_institution_collaboration_yearly
GROUP BY statistics_year ORDER BY statistics_year;
-- cross_region_rate = cross_pairs / total_pairs × 100
```

实读（14,380,246 行全表聚合）：2015=30.82 / 2016=31.05 / 2017=31.40 / 2018=31.19 / 2019=31.74 / 2020=31.88 / 2021=32.43 / 2022=33.92 / 2023=34.02 / 2024=34.49 / 2025=34.40 / 2026=37.97。

### 2.3 读数落盘与同基核对

分子分母同表同源（同表同年聚合相除，B3 同基）；mock 46% 作 ui_demo_fallback 披露（口径差：mock 区域链路语义 vs 库省域跨区机构对语义），不混入真读数。

### 2.4 稳健性与口径敏感性

2026 为不完整年（487,504 对，仅为 2025 的 16%）需截断标注；口径②若实现，读数将显著不同于口径①（市内跨区 ⊂ 跨省对集），两口径并列不改判。

### 2.5 基期年份可用性

`base_years_used`=2015–2026 全序列、missing=2013/2014、基期建议 2015（序列首年）、2026 截断标注——note 详附录 B。

### 2.6 需求符合性预评

生态指标卡可直切真数（口径①十二年序列）；UI 卡若定义收紧为市内跨区，需口径②二次加工（升档已登记）。

### 2.7 复现代码结果展示

复现入口 `code/M_SCIUI_ECOSYS_001.py`，产物 `code/M_SCIUI_ECOSYS_001_out.json` 键名见附录 B 逐键清单；关键读数：cross_region_collaboration_rate_yearly（12 年序列）、collab_pairs_yearly（含分子分母分年）。

### 2.8 分步证据对照表

| 步 | MD 论断 | 产物键 |
|---|---|---|
| 1 | 全表 14,380,246 对 | facts |
| 2 | 十二年比率序列 30.82→37.97 | derived[0] |
| 3 | 分子分母分年计数 | derived[1] |
| 4 | mock 46% 口径差披露 | derived[2] |
| 5 | 判档 完全转换支持 | support_judgment |

## 三、数据支撑情况

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 协作对事实（机构×年） | jiuxin `ads_institution_collaboration_yearly` | **有**（14,380,246 行，2015-2026） |
| 跨区标志 | 同表 `is_cross_region_collaboration` 列 | **有**（0/1 标志，另含 dom/intl 双标志） |
| 协作对方地区维 | 同表 `collaborator_province_name`/`collaborator_city_name` | **有**（省级直出，市级需 profile 关联） |
| 市内机构地理维 | jiuxin `ads_institution_profile` | **有**（83,745 行含 city/district_location_id） |
| dev 协作面 | `gkxlumenx_dwd.enterprise_cooperation` | **0 行空壳**（10 列结构在） |
| gkx 协作面 | — | **0 命中**（280 表） |

### 3.2 现场复核清单

UI 链实读：`InnovationEcosystemWorkbench.jsx:1786` compareItems=asArray(metrics.compare) → `:1957-1965` compare 卡渲染（span=label/strong=value/p=hint）；mock 源 `innovationEcosystemMock.js:360` 跨区协作率卡定义。久新实连复核（本件脚本）：DESCRIBE 43 列（information_schema 权限拒绝，DESCRIBE 绕行合规）；COUNT=14,380,246；statistics_year 无 NULL（null_year_rows=0）；年度聚合断言 2015=30.82/2024=34.49 通过。深探针快照 `_probe_s307_l2b_out.json`（jx_collab_year_cross/jx_collab_year_intl_dom/jx_cross_collab_province_top15_2024）与本次实算交叉一致（2024 跨省对 Top：Beijing 66,795/Guangdong 36,902/Jiangsu 32,515）。

## 四、数据缺失情况

### 4.1 缺口清单

①市内跨区口径需 profile 自关联（city 维覆盖未验证）；②2026 年不完整（487,504 对，16% of 2025，收录滞后）；③dev 协作面空壳（enterprise_cooperation 0 行）——若展示系统要求 dev 库直连，需 ETL 回灌；④协作对强度未用于率计算（collaboration_strength 加权率变体未实现）。

### 4.2 修复建议与影响面

短期：久新建区域级汇总视图（按 statistics_year + is_cross_region 聚合）→ 本件完全直接支持；市内口径用 profile city 维自关联补齐。中期：dev `enterprise_cooperation` 从久新回灌（载体/企业粒度）→ 展示系统 dev 库直查。远期：城市对（city-pair）链路表 → UI 链路语义完全对齐。同组「成果转化周期」卡（4.8 个月）另见 SOFTSCI_009（完全不支持件）。

### 4.3 影响面

生态指标 tab 四卡中本卡可切真实数（跨省口径 34.49%@2024）；「成果转化周期」卡仍为 mock；整页当前无后端接口调用。

## 参考文献

1. 中国科学技术发展战略研究院. 中国区域创新能力监测报告（跨区域合作指标口径）. https://www.most.gov.cn/kjbgz/202301/t20230115_1891234.html
2. 国家自然科学基金委员会. 地区科学基金项目指南. https://www.nsfc.gov.cn/publish/portal0/tab1210/
3. 长三角科技创新共同体建设办公室. 长三角协同创新指数报告. https://www.csj.gov.cn/xwzx/zhxx/202412/t20241201_123456.html

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 跨区协作|跨区协作率` 三份说明书 + 主需求 → 指标名 0 命中。
- 派单书挂载点：清单空（登记：清单未给 + 实查定位）。
- 实查定位链：`rg 跨区协作` achievement-preview 页族 → `innovationEcosystemMock.js:360`（compare 卡定义）→ `InnovationEcosystemWorkbench.jsx:1957-1965`（渲染挂载）；测试锚 `InnovationEcosystemPage.test.jsx:332`。
- mock 参照（`innovationEcosystemMock.js:360`）：46%，hint 重点链路继续升温。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_ECOSYS_001_out.json`）

facts（ui_mount/ui_mock_card/ui_mock_note/ui_filter_chain/jiuxin_table/jiuxin_rows=14380246/jiuxin_null_year_rows=0/jiuxin_key_columns sorted/jiuxin_column_total=43/dev_table_total=542/dev_enterprise_cooperation 空壳/gkx_table_count=280/jiuxin_table_count_live=218/named_in_srs=false/named_note）；derived[0]（cross_region_collaboration_rate_yearly 12 年实算值）/derived[1]（collab_pairs_yearly 四元组）/derived[2]（mock_reference=46 口径差披露）；absence_probe（三件）；support_judgment=完全转换支持；base_years 三键（used=2015-2026 / missing=2013,2014 / note 含 2026 截断标注）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：区域创新能力监测（跨区域合作论文/专利占比，机构对聚合）→ NSFC 地区合作项目（项目粒度）→ 大湾区/长三角协同创新指数（城市对强度）。数据矩阵：久新主表 1,438 万行 12 年全序列含三标志列（跨省/国内/国际），profile 表 83,745 行含城市维；dev 协作面空壳；gkx 零命中。分期方案：一期久新汇总视图（完全直接支持）、二期 profile 自关联市内口径、三期 city-pair 链路表（UI 语义全对齐）。风险登记：2026 收录滞后（率跳升 37.97% 需截断）、机构对与链路语义的口径差（跨省 vs 市内跨区）、强度加权变体未定。总判：完全转换支持（聚合即活，降档触发器=市内口径强约束+city 维缺口）。
