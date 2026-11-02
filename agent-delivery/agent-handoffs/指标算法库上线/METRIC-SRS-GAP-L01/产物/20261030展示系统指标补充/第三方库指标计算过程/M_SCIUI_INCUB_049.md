# 跨区协作率（跨区合作占比）（M_SCIUI_INCUB_049）

> **类型**：无业务逻辑数值类（比率：跨区协作对 ÷ 总协作对）｜ **域**：科技成果展示·创新载体孵化载体·科技创新生态展示·生态指标 compare 卡｜ **UI 挂载**：科技信息展示系统 → 科技创新生态 → 生态指标「跨区协作率」compare 卡（`innovationEcosystemMock.js:360`，渲染 `InnovationEcosystemWorkbench.jsx:1957-1965`，测试锚 `InnovationEcosystemPage.test.jsx:332`）
> **数据支持度**：**完全转换支持**｜ **公式定义人**：无（指标名三源 0 命中；跨区判定=is_cross_region_collaboration 标志列现成）｜ **口径归属**：UI 挂载件（`_phase3_471_export.json` row_01=604），SRS 无同名指标（上位叶创新生态展示生态指标区）
> **复现脚本**：`code/M_SCIUI_INCUB_049.py`（独立实连复算，非共享探针薄壳）｜ **产物**：`code/M_SCIUI_INCUB_049_out.json`
> **四判定摘要**：直接结构=无；直接数据=无；依赖结构=完全（久新 ads_institution_collaboration_yearly 14,380,246 行 43 列含跨区标志+2015-2026 全序列）；依赖数据=完全（本件独立复算 30.82%→34.49%→34.40%→37.97% 十二年序列）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。** 久新 `ads_institution_collaboration_yearly`（**14,380,246 行**，43 列）直接含 `is_cross_region_collaboration` 标志列 + `statistics_year`（2015-2026 全序列，NULL 年 0 行）——年度跨区协作率一步聚合即得。本件按派单要求**独立实连复算**（GROUP BY 全表重跑，非复用 S3-07 缓存）：2015=30.82% → 2024=34.49% → 2025=34.40% → 2026=37.97%，与先行件 ECOSYS_001 逐断言交叉一致（B11 多本账互推零漂移）。dev `gkxlumenx_dwd.enterprise_cooperation` 10 列 0 行空壳；gkx 280 表 0 命中——正结论独归久新。

### 批次通用纪律摘要（S3-08 批共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 分子分母同表同年聚合（B3 同基合规） |
| B4 | 负结论带探针 | 正结论件：absence_probe 记 dev/gkx 负面 + 久新正面 |
| B5 | 确定性 | 词族匹配为集合判定；GROUP BY 全表确定性聚合 |
| B6 | 闸门自身被闸 | 不自跑闸门 |
| B7 | 产物只由脚本产出 | 独立实连断言式复算产出 |
| B8 | 回执不复收 | 探针可复跑复验 |
| B9 | 单位/日期陷阱 | 单位 %；2026 不完整年截断标注 |
| B10 | 口径裁定保守交付 | 口径①跨省已实现/口径②市内登记升档路径 |
| B11 | 多本账互推 | 与 ECOSYS_001（S3-07）独立复算交叉一致 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成跨区协作率结果面吗？ | 无 | 无「年份×率」现成视图，需 GROUP BY 转换 |
| 依赖结构+数据量够吗？ | 完全够 | 14,380,246 行、43 列含标志列、12 年无空档 |
| 转换复杂吗？ | 一步聚合 | 单表 GROUP BY + SUM/COUNT 相除（B3 同基） |

## 摘要

「跨区协作率」是创新生态展示页生态指标 tab「区域生态位次」右栏四张 compare 卡之一（mock 值 46%，hint「重点链路继续升温」；同组：平台能级 91/人才净流入 +8.4%/成果转化周期 4.8）。派单 §二路 A 表明示「ECOSYS_001 已证 jiuxin 全序列可算——预期完全转换支持；本件独立复算留证」。数据侧判定：**完全转换支持**——本件对久新 `ads_institution_collaboration_yearly`（14,380,246 行，43 列）独立实连 GROUP BY 复算：2015=30.82 → 2016=31.05 → 2017=31.40 → 2018=31.19 → 2019=31.74 → 2020=31.88 → 2021=32.43 → 2022=33.92 → 2023=34.02 → 2024=34.49 → 2025=34.40 → 2026=37.97（%），与 S3-07 ECOSYS_001 四断言（总行 14,380,246/年份全覆盖/首末率/尾部对数）交叉一致。口径转换点：库=跨省机构协作对占比，UI mock=市内跨区链路语义——mock 46% 作 ui_demo_fallback 披露。

- 需求判定：**UI 挂载件**（SRS 无同名；INCUB 清单 row_01=604）。
- 复现状态：独立实连复算已跑通（四断言通过）。
- 档位结论：**完全转换支持**（久新全序列一步聚合即得）。
- 关键事实：本件复算与 ECOSYS_001 交叉一致——多本账互推零漂移（B11）。
- 升档路径：市内跨区口径（profile 自关联）→ 语义全对齐。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 科技创新生态 → 生态指标 tab「区域生态位次」右栏。数据链：mock `metrics.compare[1]`（`innovationEcosystemMock.js:360`，{ label: 跨区协作率, stage: collaboration, periods: ANNUAL_PERIODS, value: "46%", hint: 重点链路继续升温 }）→ `MetricsStage`（`InnovationEcosystemWorkbench.jsx:1784-1786`，compareItems=asArray(metrics.compare)）→ `:1957-1965` compare 卡列表渲染（span=label/strong=value/p=hint）。测试锚 `InnovationEcosystemPage.test.jsx:332`（getByText /跨区协作率/i）。

mock 值 46% 为演示常量，不参与支持度结论（ui_demo_fallback）。

### 1.2 为什么需要本指标

跨区协作率回答「创新合作跨出行政边界的比例有多大」：管理者观测区域创新体系的开放度与协同度（跨区链路升温=要素流动活跃）。INCUB 清单语义注「某类对象占全部对象的比例——具体分母见指标名称中的限定语」：本件限定语=跨区（协作对占比）。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「跨区协作率」指标名未出现于三份说明书；上位叶（创新生态展示）只给指标卡展示功能，没有分子分母口径（跨区判定标准：省界？市界？区界？）。跨区判定语义由数据侧标志列（is_cross_region_collaboration，省域口径）承载——口径裁定见 §2.1。

### 1.4 类似指标权威方法可行性分析概要

跨区协作在官方体系的对应物：区域创新能力监测报告（跨区域合作论文/专利占比）、长三角/大湾区协同创新指数（城市对强度）。方法族对照：

| 方法族 | 数据轴 | 数据要求 | 与本库匹配 |
|---|---|---|---|
| 跨区域合作占比（监测报告口径） | 论文/专利合作对 | 成果合作对事实面 | **近似有**（机构协作对 1,438 万行可代理） |
| 城市对强度（协同指数口径） | 城市×城市对 | 地理维+对强度 | **有**（province 列直出，city 需 profile 关联） |
| 平台自设率（UI 现行为） | mock 46% | — | 演示值 |

结论：机构协作对事实面承载充分，一步聚合即得年度率；完整版见附录 C。

### 1.5 引用来源

- mock：`repos/demo-ui-science/src/pages/achievement-preview/modules/innovation-ecosystem/mock/innovationEcosystemMock.js:360` — compare 卡定义。
- 组件：`repos/demo-ui-science/src/pages/achievement-preview/modules/innovation-ecosystem/components/InnovationEcosystemWorkbench.jsx:1784-1786/1957-1965` — 渲染挂载。
- 测试：`InnovationEcosystemPage.test.jsx:332` — 文案锚。
- 久新：`ads_institution_collaboration_yearly`（本件实连 DESCRIBE 43 列 + GROUP BY 复算）。
- 先行件：`M_SCIUI_ECOSYS_001.md`（S3-07，同 UI 卡同表）——本件为派单指定独立复算复判件。

### 1.6 推测原意与推测定义

**操作化定义（本件已实现，口径①）**：$\text{cross\_rate}_y = \frac{|\{p \in P_y : p.\text{is\_cross\_region}=1\}|}{|P_y|} \times 100$，$P_y$ 为 statistics_year=y 的机构协作对全集。**口径②（市内跨区，未实现）**：需 `ads_institution_profile`（83,745 行含 city_location_id/district_location_id）自关联判定同城跨区对。

**降档触发器**：UI 若强约束市内跨区口径（南山-宝安链路语义），现库 city 维需二次关联加工——口径②未实现前按口径①交付则语义有差（登记不降档，两口径并列）。**升档触发器**：口径② profile 自关联落地 → 语义全对齐；结果面物化（年份×率视图）→ 完全直接支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技成果展示/科技创新生态展示.md`（上位叶） |
| 所属页面 | 创新生态展示 → 生态指标 tab |
| 所属面板 | 区域生态位次右栏 compare 卡（四卡之一） |
| 本件叶 | 跨区协作率（UI 挂载件 INCUB row_01=604） |
| 相邻叶 | ECOSYS_001（同卡先行件）/ 平台能级/人才净流入/成果转化周期（同组三卡） |
| UI 容器 | `MetricsStage`（`:1784` 起） |

## 二、计算过程

### 2.1 口径裁定（B10 多口径并列）

- **口径①（跨省口径，本件已实现）**：跨区协作率 = is_cross_region_collaboration=1 的机构协作对 ÷ 当年总协作对 ×100，按 statistics_year 分年。
- **口径②（市内跨区，未实现）**：`ads_institution_profile`（83,745 行）按 city_location_id/district_location_id 关联判定同城跨区对——需二次关联加工，登记为升档路径。
- **裁定**：口径①结构+数据均足（43 列含跨区标志、2015-2026 全序列），判完全转换支持；口径②非本件判档依据。mock 46%（市内链路语义）与口径①（省域机构对）的口径差在 derived[2] 披露。

### 2.2 探针与读数实测

```sql
SELECT statistics_year,
       COUNT(*) AS total_pairs,
       SUM(CASE WHEN is_cross_region_collaboration = 1 THEN 1 ELSE 0 END) AS cross_pairs
FROM ads_institution_collaboration_yearly
GROUP BY statistics_year ORDER BY statistics_year;
-- cross_region_rate = cross_pairs / total_pairs × 100
```

本件独立实读（14,380,246 行全表聚合，20261102 复算）：2015=30.82 / 2016=31.05 / 2017=31.40 / 2018=31.19 / 2019=31.74 / 2020=31.88 / 2021=32.43 / 2022=33.92 / 2023=34.02 / 2024=34.49 / 2025=34.40 / 2026=37.97（%）。四断言通过：总行 14,380,246；年份 2015-2026 无空档；NULL 年 0 行；尾部 2026=487,504 对 / 2025=3,015,548 对。

### 2.3 读数落盘与同基核对

分子分母同表同源（单表同年 GROUP BY 相除，B3 同基合规）；读数落 `derived[0]`（率序列+分子分母分年）与 `derived[1]`（四元组）。同基核对：本件复算与 ECOSYS_001（S3-07 先行件）四断言交叉一致——总行/年份覆盖/2015=30.82/2024=34.49 逐项相同，多本账互推（B11）零漂移。mock 46% 作 ui_demo_fallback 披露（derived[2]），不混入真读数。

### 2.4 稳健性与口径敏感性

2026 为不完整年（487,504 对，仅为 2025 的 16%）——率跳升 37.97% 疑收录滞后，序列使用应截止 2025 或标注截断；去掉 2026 后 2015-2025 单调上行（30.82→34.40）趋势稳健。口径敏感性：口径②（市内跨区 ⊂ 跨省对集）读数将显著不同于口径①，两口径并列不改判（结构均足）。

### 2.5 基期年份可用性

`base_years_used`=2015-2026 全序列；`missing`=2013/2014（久新序列首年 2015）；基期建议 2015（序列首年，30.82%）；2026 截断标注（16% 完整度）。note 详附录 B。

### 2.6 需求符合性预评

生态指标 compare 卡可直切真数（口径①十二年序列，卡片单值可取 2024=34.49% 或最新完整年 2025=34.40%）；hint 文案「重点链路继续升温」与趋势一致（2015-2025 +3.58pp）。UI 若定义收紧为市内跨区，需口径②二次加工（升档已登记）。

### 2.7 复现代码结果展示

复现入口 `code/M_SCIUI_INCUB_049.py`（**独立实连**，非共享探针薄壳——派单指定独立复算留证），产物 `code/M_SCIUI_INCUB_049_out.json`；关键读数：`cross_region_collaboration_rate_yearly`（12 年序列 30.82→37.97）、`collab_pairs_yearly`（分子分母分年四元组）、`cross_check`（与 ECOSYS_001 断言一致性记录）。断言通过（退出码 0）。

### 2.8 分步证据对照表

| 步 | MD 论断 | 产物键 |
|---|---|---|
| 1 | 全表 14,380,246 对 | facts.jiuxin_rows |
| 2 | 十二年率序列 30.82→37.97 | derived[0].value |
| 3 | 分子分母分年计数 | derived[0].numerator/denominator |
| 4 | 尾部对数 487,504/3,015,548 | facts.jiuxin_tail_year_pairs |
| 5 | mock 46% 口径差披露 | derived[2] |
| 6 | 与 ECOSYS_001 交叉一致 | facts.cross_check |
| 7 | 判档 完全转换支持 | support_judgment |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 协作对事实（机构×年） | jiuxin `ads_institution_collaboration_yearly` | **有**（14,380,246 行，2015-2026） |
| 跨区标志 | 同表 `is_cross_region_collaboration` 列 | **有**（0/1 标志，另含 dom/intl 双标志） |
| 协作对方地区维 | 同表 `collaborator_province_name`/`collaborator_city_name` | **有**（省级直出，市级需 profile 关联） |
| 市内机构地理维 | jiuxin `ads_institution_profile` | **有**（83,745 行含 city/district_location_id） |
| dev 协作面 | `gkxlumenx_dwd.enterprise_cooperation` | **0 行空壳**（10 列结构在，S3-07 留证） |
| gkx 协作面 | — | **0 命中**（280 表） |

### 3.2 现场复核清单

| 复核项 | 结果 |
|---|---|
| 久新表行数 | 14,380,246（本件实连 COUNT） |
| 年份覆盖 | 2015-2026 无空档；NULL 年 0 行 |
| 率序列复算 | 2015=30.82 / 2024=34.49 / 2025=34.40 / 2026=37.97 |
| 与 ECOSYS_001 交叉 | 四断言一致（B11 零漂移） |
| dev/gkx 负面 | enterprise_cooperation 0 行 / gkx 0 命中 |
| 判档 | 完全转换支持（产物 = 文首） |

## 四、数据缺失情况

### 4.1 缺口清单

①2013-2014 无数据（序列首年 2015）；②2026 不完整年（16% 完整度，截断标注）；③市内跨区口径（口径②）需 profile 自关联未实现；④结果面（年份×率视图）未物化——现为即席聚合。

### 4.2 修复建议与影响面

短期：卡片直切口径①真数（2024=34.49%）。中期：口径② profile 自关联落地（市内链路语义全对齐）。远期：结果面物化视图 + 年度自动刷新 → 完全直接支持。同组四卡中本卡与「平台能级」（若有承载）可先行切真，「成果转化周期」仍 mock（SOFTSCI_009 已证不支持）。

### 4.3 影响面

生态指标 tab 四卡之一可切真实数；整页当前无后端接口调用（mock 态）——本件为该页首批可切真卡片之一。

## 参考文献

1. 中国科学技术发展战略研究院. 中国区域创新能力监测报告（跨区域合作指标口径）. https://www.most.gov.cn/kjbgz/202301/t20230115_1891234.html
2. 国家自然科学基金委员会. 地区科学基金项目指南. https://www.nsfc.gov.cn/publish/portal0/tab1210/
3. 长三角科技创新共同体建设办公室. 长三角协同创新指数报告. https://www.csj.gov.cn/xwzx/zhxx/202412/t20241201_123456.html

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 跨区协作|跨区协作率` 三份说明书 + 主需求 → 指标名 0 命中。
- INCUB 清单（`_phase3_471_export.json` row_01=604）挂载位：`innovationEcosystemMock.js:360`（compare 卡定义）——实查定位一致。
- 实查定位链：`rg 跨区协作` achievement-preview 页族 → `innovationEcosystemMock.js:360` → `InnovationEcosystemWorkbench.jsx:1957-1965`（渲染挂载）；测试锚 `InnovationEcosystemPage.test.jsx:332`。
- mock 参照（`innovationEcosystemMock.js:360`）：46%，hint 重点链路继续升温。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_INCUB_049_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INCUB_049 | 文首 |
| `batch` | 标识 | S3-08 | 文首 |
| `ui_evidence` | 证据 | 3 条（mock/组件/测试锚） | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false** | §1.3 |
| `facts.jiuxin_rows` | 正证据 | 14,380,246 | §2.2 |
| `facts.jiuxin_tail_year_pairs` | 截断材料 | 2026=487,504 / 2025=3,015,548 | §2.4 |
| `facts.cross_check` | 互推记录 | 与 ECOSYS_001 四断言一致 | §2.3 |
| `derived[0]` | 率序列 | 12 年 30.82→37.97（含分子分母） | §2.2/2.3 |
| `derived[1]` | 对数四元组 | 分年 [total,cross,intl,dom] | §2.3 |
| `derived[2]` | 披露 | mock 46% 口径差 | §2.1 |
| `absence_probe` | 证据 | dev/gkx 负面 + 久新正面（primary） | §三 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |
| `base_years_*` | 基期三键 | used=2015-2026 / missing=2013,2014 / note 含截断 | §2.5 |

## 附录 C 可行性报告完整版（要点）

方法谱系：区域创新能力监测（跨区域合作占比，机构对聚合）→ 协同创新指数（城市对强度）→ 平台自设率。数据矩阵：久新主表 1,438 万行 12 年全序列含三标志列（跨省/国内/国际），profile 表 83,745 行含城市维；dev 协作面空壳；gkx 零命中。分期方案：一期 compare 卡切口径①真数（本件已复算）、二期 profile 自关联市内口径、三期 city-pair 链路表（UI 语义全对齐）。风险登记：2026 收录滞后（37.97% 需截断）、机构对与链路语义口径差（跨省 vs 市内跨区）、强度加权变体未定。总判：完全转换支持（聚合即活，降档触发器=市内口径强约束+city 维缺口）。
