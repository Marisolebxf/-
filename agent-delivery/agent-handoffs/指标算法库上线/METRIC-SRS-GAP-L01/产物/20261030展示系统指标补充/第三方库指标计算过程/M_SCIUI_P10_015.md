# M_SCIUI_P10_015 地域流动明细与历史回溯（时空回放）—— 指标信息 MD

> **类型**：简单统计类｜ **域**：时空演进 New·全球研究主体地域时空分布·地域流动明细（`SpaceTimeEvolutionNewPage.jsx:984`）｜ **UI 挂载**：科技信息展示系统 → 创新载体孵化载体 New（时空演进页）→「地域流动明细与历史回溯（时空回放）」年表+回放按钮
> **数据支持度**：**完全转换支持**｜ **公式定义人**：无（指标名三源无同名面；回放表=年份×首位热点×蝉联/新晋三段式可由年度面聚合重建）｜ **口径归属**：UI 挂载件 = SRS 功能叶 501 的落位区块（同名）
> **复现脚本**：`code/M_SCIUI_P10_015.py`（薄壳实算，共享探针 `code/_shared_s308_laneb_probe.py`）｜ **产物**：`code/M_SCIUI_P10_015_out.json`
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（三源无「回放表」现成结果面）；直接数据=无；依赖结构=完全（jiuxin ads_geo_yearly_metrics 171,736 行 27 年四级地域含流动列 + ads_talent_mobility_yearly_flow 51,489 行 LOCATION 维）；依赖数据=完全（2018-2025 回放窗口 8 年实算 + 2000-2025 二十六年流量序列）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：完全转换支持。**（久新双面承载：`ads_geo_yearly_metrics` 171,736 行年度地域面 + `ads_talent_mobility_yearly_flow` 51,489 行流动对；回放表一步聚合转换即得）。**派单预判「大概率零承载」被实测推翻**——本批实连久新发现时空双面，预判修正记录在案。

### 批次通用纪律摘要（S3-08 批共用）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 热点取 Top 同表同年同层级（share_basis 注记） |
| B4 | 负结论带探针 | dev/gkx trajectory 词族污染留证（absence_probe） |
| B5 | 确定性 | 年份 sorted；同值热点按 talent_count 降序取首 |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 产物只由脚本产出 | 薄壳实算脚本重跑产出 |
| B8 | 回执不复收 | 实算读数可重跑复验 |
| B9 | 单位/日期陷阱 | 2026 为不完整年（talent 流动 0 行）截断标注 |
| B10 | 口径裁定保守交付 | 回放维度四选一裁定（talent 维首选），触发器写死 §1.6 |
| 基期三键 | base_years_used/missing/note | 产物全键 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成回放结果面吗？ | 无 | 无「年份×首位热点×蝉联」现成表——需聚合转换 |
| 年度地域面数据量够吗？ | 够 | ads_geo_yearly_metrics 171,736 行（2000-2026 四级地域） |
| 流动语义面有吗？ | 有 | LOCATION 维 28,672 行 from→to 对流量（2000-2025） |

## 摘要

「地域流动明细与历史回溯（时空回放）」是全球研究主体地域时空分布 tab 的明细卡（`SpaceTimeEvolutionNewPage.jsx:984`）：年表五行（年份/首位热点区域/值/增速/蝉联-新晋-基准）+「从 2018 回放」按钮；mock 侧 `historyRows`（`:343-361`）由 26 城外推热点逐年构建。数据侧判定：**完全转换支持**——久新双面实测：①`ads_geo_yearly_metrics`（171,736 行，2000-2026 二十七年，CITY 132,975/PROVINCE 33,518/COUNTRY 5,081/CONTINENT 162 四级地域，含 `inbound_talent_count`/`outbound_talent_count`/`mobility_event_count` 流动列）承载「分布演变历程」；②`ads_talent_mobility_yearly_flow`（51,489 行，其中 LOCATION 维 28,672 行）承载「地域流动」from→to 语义。实算回放窗口 2018-2025 八年：talent 维 COUNTRY 级首位热点连续八年为 China（44,020→71,259 人单调上行）；LOCATION 维流量 2,652（2018）→1,905（2024）→975（2025）。蝉联/新晋列由相邻年比较导出（与 mock 构建逻辑同构）。地名解析由 `ads_location`（22,229 行四级字典含经纬度）承接，回放地图坐标同源。

- 需求判定：**SRS 功能叶 501 同名落位**（需规原文「依时间轴回溯研究主体流动和分布演变历程」）。
- 复现状态：薄壳实算已跑通；回放行/流量序列落产物。
- 档位结论：**完全转换支持**（派单预判修正：非零承载，双面实证）。
- 关键事实：2018-2025 talent 维首位热点全序列 China 蝉联——中国科研人才存量八年 44,020→71,259 人。
- 升档路径：久新建「年份×层级×维度」热点回放物化视图 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 时空演进展示（New 页族）→「全球研究主体地域时空分布展示」tab →「地域流动明细与历史回溯（时空回放）」卡（`SpaceTimeEvolutionNewPage.jsx:984` SectionCard，extra=回放按钮 `handleReplay`）。表体 `historyRows`（`:343-361` useMemo）：YEARS（2018-2026）逐年取 `getHotspots(level, dimension, y, 1)[0]` 为首位热点，与前一年同名标「蝉联」、异名标「新晋」、首年标「基准」；`:355-363` `historySummary` 生成演变摘要句。mock 热点由 `CITY_PROFILES` 外推（dimension 可切 papers/patents/funding/talent 四维，`:343` 依赖）。

### 1.2 为什么需要本指标

回放回答「全球科研重心怎么移」：按时间轴回看首位热点更替与流动量起伏，识别区域创新能级提升路径（SRS 501 需规原文「分析全球科技布局变化和区域创新能级提升路径」）——它是分布展示 tab 的纵深（快照→时序）。

### 1.3 需求文档是否给出定义方法

**三份说明书未给出该指标的计算方法。** SRS 501 只给功能行为（时空回放、依时间轴回溯、自动生成趋势报告），无热点判据（哪一维取首）、无回放粒度（年/季）、无蝉联判定式——三段式（年份×首位热点×蝉联/新晋）为 UI 构建逻辑自设，本件按同构重建。

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①Nature Index 科学城市（年度城市科研产出排名时序，份额份额法）——首位热点年度序列的直接权威对齐；②Scopus/Elsevier 科研景观（institution-level yearly metrics）——与 `ads_geo_yearly_metrics` 同构；③OECD 科学技术指标（国家科研人员存量年度序列）。三族均落在「地域×年度×指标」立方体上——久新双面（geo_yearly + talent_flow）正是该立方体，权威方法可直接落地。完整版见附录 C。

### 1.5 引用来源

1. Nature Index. Science cities（年度城市科研份额排名）. https://www.nature.com/nature-index/
2. Elsevier. SciVal research landscape（机构/地域年度指标）. https://www.scival.com/
3. OECD. MSTI Manual（Main Science and Technology Indicators，国家科研人员口径）. https://www.oecd.org/sti/msti.htm

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **口径 A（talent 维回放，已实现）**：首位热点 = COUNTRY 级 `talent_count` 最大地点（逐年）；蝉联/新晋 = 相邻年同名/异名；流动量 = LOCATION 维 `talent_count` 年合计。
- **口径 B（papers 维回放，可算未跑）**：同构换 `paper_count` 列。
- **降档触发器**：若 UI 强约束城市级（CITY）回放含 2026 实时年，2026 不完整年（talent 流动 0 行）将致末年缺流动——截断至 2025 即可维持完全转换支持。
- **升档触发器**：久新建热点回放物化视图（年份×层级×维度预聚合）→ 完全直接支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技成果展示/科技时空演进展示.md` |
| 所属四级功能 | 1.1.1.1.4.6 科技成果展示（域）|
| 所属页面 | 时空演进 New（创新载体孵化载体 New 页族）|
| 本件叶 | 序号 501「地域流动明细与历史回溯」（SRS 同名功能叶的 UI 落位区块）|
| 相近叶 | 序号 497 交互式时空地图分布呈现（含「动态筛选与回放」，同 tab）/序号 502 分布数据对比与报告输出；P10_025 科研主体路径追踪（主体级，同族不同粒度）|
| UI 容器 | `SpaceTimeEvolutionNewPage.jsx:984-1010` SectionCard |

## 二、计算过程

### 2.1 口径裁定（B10 多口径并列）

- **口径 A（talent 维回放，已实现）**：热点判据= talentoount，流动=LOCATION 对流量——库面最全（inbound/outbound 列现成）。
- **口径 B（papers 维回放，可算未跑）**：同构换 paper_count（列在，未实算）。
- **裁定**：A 为本件判档依据（结构+数据均足）；B 登记为扩展位。mock 的 patents/funding 两维在库面无对应列（该两维维持 mock，披露于 notes）。

### 2.2 探针读数实测

```sql
-- 回放明细面（分布演变）
SELECT statistics_year, location_id, talent_count
FROM ads_geo_yearly_metrics
WHERE location_level='COUNTRY' AND statistics_year BETWEEN 2018 AND 2025
ORDER BY statistics_year, talent_count DESC;
-- 流动语义面（LOCATION 对流量）
SELECT statistics_year, SUM(talent_count)
FROM ads_talent_mobility_yearly_flow
WHERE flow_dimension='LOCATION' AND statistics_year>=2018
GROUP BY statistics_year;
```

实读：回放窗口 2018-2025 八年 COUNTRY 级 talent 维首位热点全序列 **China 蝉联**（44,020/48,918/54,241/58,255/62,439/65,765/69,523/71,259 人，单调上行 +61.9%）；LOCATION 维年流量 2,652（2018）/2,921（2019）/2,153（2020）/2,597（2021）/2,567（2022）/2,184（2023）/1,905（2024）/975（2025，不完整年）。

### 2.3 读数落盘与同基核对

回放行（年份→[首位热点, talent_count]）落 `derived[0]`——同表同年同层级取 Top（B3 同基注记）；流量序列落 `derived[1]`；mock「从 2018 回放」起点作 ui_demo_fallback 披露（库序列 2000 起更长，2018 为 UI 习惯窗口）。

### 2.4 稳健性与口径敏感性

2026 为不完整年（talent 流动 0 行、geo 面 talent_count 36,730 仅存量）——回放序列截断至 2025；2025 流量 975 亦偏低（收录滞后），趋势解读须标注；蝉联判定对并列值敏感（同值按 talent_count 降序取首，B5 确定性破平局）；若切 CITY 级（132,975 行），热点更替将更频繁——层级敏感性已在口径 A 固定为 COUNTRY。

### 2.5 基期年份可用性

`base_years_used`=2018-2025（回放窗口八年）；`missing`=[]（窗口内无空年）；基期建议 2018（UI 回放起点习惯）；全序列 2000-2026 更长可用（2026 截断）。note 详附录 B。

### 2.6 需求符合性预评

对 SRS 501 三语义：依时间轴回溯——满足（二十六年全序列）；流动明细——满足（LOCATION 对流量）；自动生成趋势报告——数据面就绪（historySummary 句式可后端化）。talent/papers 维可切真，patents/funding 维维持 mock（列缺）。

### 2.7 复现代码结果展示

复现入口 `python3 code/M_SCIUI_P10_015.py`（薄壳直连久新实算：geo_yearly 聚合 + flow 求和 + ads_location 地名解析）；产物 `code/M_SCIUI_P10_015_out.json`；关键读数：`derived[0]` 八年回放行、`derived[1]` 流量序列。

### 2.8 分步证据对照表

| 步 | MD 论断 | 产物键 |
|---|---|---|
| 1 | geo 面 171,736 行 27 年四级 | facts.jiuxin_geo_rows / jiuxin_geo_year_span |
| 2 | flow 面 51,489 行（LOCATION 28,672） | facts.jiuxin_flow_rows / jiuxin_flow_location_dim_rows |
| 3 | 八年首位热点 China 蝉联 44,020→71,259 | derived[0] |
| 4 | LOCATION 流量 2,652→975 | derived[1] |
| 5 | dev/gkx trajectory 词族污染 | absence_probe[0]/[1] |
| 6 | 判档 完全转换支持 | support_judgment |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 地域年度面（分布演变） | jiuxin `ads_geo_yearly_metrics` | **有**（171,736 行，2000-2026 四级地域） |
| 流动对（from→to 流量） | jiuxin `ads_talent_mobility_yearly_flow` | **有**（LOCATION 维 28,672 行） |
| 流动入出列（净流动） | geo 面 `inbound_talent_count`/`outbound_talent_count` | **有**（列现成） |
| 地名字典（含坐标） | jiuxin `ads_location` | **有**（22,229 行四级含 lat/lng） |
| 回放表（现成结果面） | dev/gkx/jiuxin | **无**（需聚合转换——判转换支持的依据） |
| dev/gkx 轨迹面 | dev `sys_route_conf` 等 / gkx `dwd_drug` | **语义污染**（路由配置/药代轨迹） |

### 3.2 现场复核清单

UI 链实读：`SpaceTimeEvolutionNewPage.jsx:984` 卡标题+回放按钮、`:989-997` 表五列、`:343-361` historyRows 构建+蝉联/新晋判定。久新实连复核（本件脚本）：geo 面 COUNT=171,736、层级分布 CITY 132,975/PROVINCE 33,518/COUNTRY 5,081/CONTINENT 162、年跨度 2000-2026；flow 面 COUNT=51,489、维度分布 LOCATION 28,672/INSTITUTION 17,064/DISCIPLINE 5,753；ads_location 22,229 行。dev/gkx 词族污染见 absence_probe。

## 四、数据缺失情况

### 4.1 缺口清单

①回放物化视图未建（每次现算，判「转换」不判「直接」的唯一缺口）；②patents/funding 维年度列缺（该两维回放维持 mock）；③2026 不完整年（talent 流动 0 行）；④2025 流量偏低（975，收录滞后标注）。

### 4.2 修复建议与影响面

短期：回放表切口径 A 真数（八年序列现成）+维度选择器限 talent/papers。中期：久新建热点回放物化视图 → 完全直接支持（一次解回放+摘要句+地图坐标）。远期：patents/funding 年度列补齐 → 四维全开。同族联动：P10_025（主体路径）共用 ads_talent_mobility 族，双件一次升档。

### 4.3 影响面

分布展示 tab 的回放卡可切真（talent 维）；「从 2018 回放」按钮语义落地；SRS 501「自动生成趋势报告」数据面就绪。

## 参考文献

1. Nature Index. Science cities. https://www.nature.com/nature-index/
2. Elsevier. SciVal. https://www.scival.com/
3. OECD. Main Science and Technology Indicators. https://www.oecd.org/sti/msti.htm

# 附件

## 附录 A 原始需求原文摘录

- SRS《科技时空演进展示.md》序号 501（excel_row 504，path=…/全球研究主体地域时空分布展示/地域流动明细与历史回溯）：「支持时空回放功能，用户可依时间轴回溯研究主体流动和分布演变历程，自动生成趋势变化报告，方便分析全球科技布局变化和区域创新能级提升路径。」
- 检索记录：`rg 地域流动明细|时空回放` 三份说明书 → 功能叶 501 命中（本件即该叶 UI 落位；清单挂点 SpaceTimeEvolutionNewPage.jsx:984 直核）。
- mock 参照：回放起点 2018（YEARS[0]）；热点由 CITY_PROFILES 外推。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_015_out.json`）

metric_id/batch=S3-08/ui_evidence（2 条组件行号）/requirement_trace（named_in_srs=false + SRS 锚 501 同名落位）/facts（ui_mount/ui_history_builder/ui_mock_note/jiuxin_geo_table/jiuxin_geo_rows=171736/jiuxin_geo_year_span/jiuxin_geo_levels/jiuxin_geo_flow_columns/jiuxin_flow_table/jiuxin_flow_rows=51489/jiuxin_flow_location_dim_rows=28672/jiuxin_flow_yearly_location_sum/jiuxin_location_dict/replay_rows_talent_top/dev_traj_word_hits/gkx_traj_note/dev_table_total=542/gkx_table_count=280/jiuxin_table_count_live=218）/derived[0]（八年回放行）/derived[1]（LOCATION 流量序列）/derived[2]（mock 参照披露）/absence_probe（三源三条，含 dev/gkx 污染留证）/support_judgment=完全转换支持/notes（5 条，含派单预判修正记录）/base_years 三键/ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：Nature Index 科学城市（年度份额排名）→ SciVal 科研景观（地域年度指标）→ OECD MSTI（国家人员存量）——三族同落「地域×年度×指标」立方体，久新双面即该立方体。数据矩阵：geo 面 171,736 行 27 年；flow 面 51,489 行 26 年；ads_location 字典 22,229 行；现成回放面无（转换点）。分期方案：一期回放表切真（talent 维）、二期物化视图（完全直接）、三期补列（四维全开）。风险登记：2026 截断、2025 收录滞后、层级敏感性（COUNTRY 固定）、维度局限（patents/funding 无列）。总判：完全转换支持（派单预判修正：实测双面承载）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_015.py` | 退出码 0，落 `_out.json` |
| 共享探针 | `python3 code/_shared_s308_laneb_probe.py` | 快照词族面零漂移 |
| 实算复核 | derived[0] 首位热点全序列 China | 重跑一致 |
| 判档一致 | MD 文首「完全转换支持」= out.json `support_judgment` | 一致 |
| mock 披露 | 回放起点 2018 仅 UI 习惯窗口 | 不参与支持度结论 |
