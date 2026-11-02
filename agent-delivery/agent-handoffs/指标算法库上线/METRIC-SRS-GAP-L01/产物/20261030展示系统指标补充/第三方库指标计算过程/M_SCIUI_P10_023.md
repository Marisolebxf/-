# M_SCIUI_P10_023 科技人员流动动态可视化 —— 指标信息 MD

> **类型**：简单统计类｜ **域**：时空演进 New·要素总览·人员流动下钻（`SpaceTimeEvolutionNewPage.jsx:1261-1282`）｜ **UI 挂载**：科技信息展示系统 → 创新载体孵化载体 New（时空演进页）→ SectionCard「科技人员流动动态可视化」三标签区（聚集热点/迁徙热点/高成长区）
> **数据支持度**：**完全转换支持**｜ **公式定义人**：无（三标签口径逐一可转换：聚集=存量排序/迁徙=对流量 to 端排序/高成长=同比自关联；mock 计算式已证外推）｜ **口径归属**：UI 挂载件（SRS 序号 507 功能叶同名区块；卡片 P10_022 为同根总量卡）
> **复现脚本**：`code/M_SCIUI_P10_023.py`（薄壳实算，共享探针 `code/_shared_s308_laneb_probe.py`）｜ **产物**：`code/M_SCIUI_P10_023_out.json`
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（无现成热点三标签结果面）；直接数据=无；依赖结构=完全（jiuxin geo 面存量+growth 列/flow 面 LOCATION 对流量/event 面跨域三标志——三面齐备）；依赖数据=完全（2024 三标签 Top3 实算落产物）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：完全转换支持。**（久新三面齐备一步转换：聚集=geo 面 talent_count 排序；迁徙=flow 面 to 端入流量排序；高成长=geo 面同比自关联——2024 三标签 Top3 实算落产物）。

### 批次通用纪律摘要（S3-08 批共用）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除/相减 | 高成长=同表自关联相除（share_basis 注记） |
| B4 | 负结论带探针 | dev/gkx 热点面缺失留证（absence_probe） |
| B5 | 确定性 | 年份 sorted；Top3 排序断言 |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 产物只由脚本产出 | 薄壳实算脚本重跑产出 |
| B8 | 回执不复收 | 实算读数可重跑复验 |
| B9 | 单位/日期陷阱 | 2026 不完整年截断；单位人/% |
| B10 | 口径裁定保守交付 | 存量/同比（mock 式）vs tooltip 净流入复合增速变体双口径披露，触发器写死 §1.6 |
| 基期三键 | base_years_used/missing/note | 产物全键 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成热点三标签结果面吗？ | 无直出面 | 需三列排序/聚合一步转换（geo/flow 两面现成列） |
| 三标签原料数据量够吗？ | 够 | geo 171,736 行（talent_count 列）+ flow 51,489 行（LOCATION 维） |
| 层级切得动吗？ | 切得动 | COUNTRY/PROVINCE/CITY 三级全有（5,081/33,518/132,975 行） |

## 摘要

「科技人员流动动态可视化」是时空演进 New 页「科技人员流动动态可视化」SectionCard（`SpaceTimeEvolutionNewPage.jsx:1261`，id=`ste-b-talent`，desc「聚集热点 / 迁徙热点 / 高成长区」）：三行标签区渲染 `talentHotspots` 三元组——聚集热点（红 Tag，`talent_count` 存量 Top3 城市名单+人数）；迁徙热点（橙红 Tag，FLOW_PATHS talent 型按年度流量排序去重 to 端 Top3 目的地）；高成长区（绿 Tag，`growth.talent` Top3 城市+增速%）。数据侧判定：**完全转换支持**——久新三面承载：①`ads_geo_yearly_metrics`（171,736 行）`talent_count` 存量列承载聚集（COUNTRY 级 2024 Top3：China 69,523/United States 18,891/United Kingdom 5,265 人）；②`ads_talent_mobility_yearly_flow`（51,489 行）LOCATION 维 to 端入流量承载迁徙目的地（2024 Top3：China 127/United States 64/Hong Kong 39 人）；③geo 面同比自关联承载高成长（2023→2024：South Korea +26.1%/Hong Kong +20.1%/Taiwan +18.0%，>1000 人门槛防微基数）。口径披露：mock 热点为 26 城外推（聚集如北京/深圳）；层级口径 mock=城市级、库默认 COUNTRY 级（CITY 132,975 行亦可切）；tooltip `:1282` 变体「近三年人才净流入复合增速」可算但小基数敏感（Hong Kong 三年和 18→40=+122.2%），仅敏感性披露。gkx 学者履历面（57,117 工作经历行）为备选路径。

- 需求判定：**UI 挂载件**（SRS 序号 507 功能叶同名区块——「展示人才聚集、迁徙热点及高成长区」原文与本区块三标签一一对应；卡片 P10_022 为同根总量卡）。
- 复现状态：薄壳实算已跑通；三标签 Top3+变体口径落产物。
- 档位结论：**完全转换支持**（三标签全部一步转换可算）。
- 关键事实：聚集与迁徙 Top1 同为 China（存量磁极与流量磁极重叠）；高成长 Top3 为东亚圈（South Korea/Hong Kong/Taiwan）。
- 升档路径：久新建热点三标签物化视图 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 时空演进展示（New 页族）→ SectionCard「科技人员流动动态可视化」（`SpaceTimeEvolutionNewPage.jsx:1259-1282`，id=`ste-b-talent`）：`:1268-1270` 聚集热点行（红 Tag）gather.map 渲染 `name（talent 人）`；`:1272-1273` 迁徙热点行（橙红 Tag）migrate.join 渲染目的地名单+「（人才流动路径主要目的地）」；`:1276-1277` 高成长区行（绿 Tag）rising.map 渲染 `name（+growth.talent% ）`；`:1282` tooltip「迁徙热点按人才流动路径年度规模排序；高成长区按近三年人才净流入复合增速排序」。数据源 `mockData.js:482-502` `getTalentHotspots(year)`；`:534` `talentHotspots = useMemo(getTalentHotspots(year))`。上钻位：要素总览第四卡（P10_022，`:1089`）onClick `scrollToBlock('ste-b-talent')` 跳本区块。

### 1.2 为什么需要本指标

热点三标签回答「人才往哪里聚、往哪里流、哪里长得快」三问：聚集=存量磁极（团队建设目标地）；迁徙=流量目的地（战略引导方向）；高成长=增速领先区（新兴磁极预警）。SRS 507 需规原文「智能识别跨区和跨领域流动趋势，展示人才聚集、迁徙热点及高成长区」——本区块即该功能叶的可视化落位，与 P10_022 总量卡构成总-分结构。

### 1.3 需求文档是否给出定义方法

**三份说明书未给出该指标的计算方法。**SRS 序号 507 给出功能行为（展示聚集/迁徙/高成长三标签）但无计算口径：聚集的存量口径（在册学者数 vs 活跃学者数）、迁徙的流量窗口（年度 vs 三年滚动）、高成长的增速基期（同比 vs 复合）均未定义；tooltip `:1282` 自带口径描述（「迁徙按年度规模、高成长按近三年净流入复合增速」）与 mock 计算式（growth.talent 存量增速）存在内部不一致——口径选择登记为本件转换点。

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①OECD 科学家流动测量（国家间净流动+热点国家排序，履历法）——聚集/迁徙标签与 OECD 热点国口径同构；②欧盟 Horizon Europe 人才流动监测（mobility flows 仪表板：净流量矩阵+top destinations）——迁徙标签=其 top destinations 榜；③中国科技人才流入监测报告（人才集聚度指数：存量+增速复合）——高成长标签与其增速分项同构。久新 geo/flow 两面即①②的原料物化（存量列+对流量列现成），权威方法可直接落地。完整版见附录 C。

### 1.5 引用来源

1. OECD. Handbook on Measuring the Mobility of Scientists（热点国排序口径）. https://www.oecd.org/sti/sci-tech/
2. European Commission. Horizon Europe Mobility Flows Monitoring（top destinations 榜）. https://erc.europa.eu/
3. 中国科学技术发展战略研究院. 中国科技人才流入监测报告（人才集聚度指数）. https://www.most.gov.cn/kjbgz/

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **口径①（存量三标签，已实现）**：聚集 = talent_count 降序 Top3；迁徙 = LOCATION 维 SUM(talent_count) to 端降序 Top3；高成长 = talent_count 同比增速降序 Top3（>1000 人门槛）。
- **口径②（tooltip 变体，已实现）**：高成长 = 近三年净流入合计增速（Σ2022-2024 对 Σ2021-2023）；迁徙同口径①。
- **口径③（mock 式，弃用披露）**：26 城 base.talent 外推+growth×0.8 外推——ui_demo_fallback。
- **降档触发器**：若 UI 强约束城市级三标签且 CITY 级 flow 对流量覆盖不足（LOCATION 维城市端关联系待验证），降部分支持。
- **升档触发器**：久新建热点三标签物化视图（年份×层级×标签预聚合）→ 完全直接支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技成果展示/科技时空演进展示.md` |
| 所属四级功能 | 1.1.1.1.4.6 科技成果展示（域）|
| 所属页面 | 时空演进 New（创新载体孵化载体 New 页族）|
| 本件叶 | SectionCard「科技人员流动动态可视化」三标签区（UI 挂载件；SRS 序号 507 功能叶同名区块）|
| 相近叶 | P10_022 总量卡（同根上钻位）/P10_025 主体路径（同页邻区块）；序号 510 科学家协作网络（同域邻叶）|
| UI 容器 | `SpaceTimeEvolutionNewPage.jsx:1259-1282` SectionCard |

## 二、计算过程

### 2.1 口径裁定（B10 多口径并列）

- **口径①（存量三标签，已实现，判档依据）**：聚集/迁徙/高成长三标签均由 geo+flow 两面现成列排序/聚合一步产出（COUNTRY 级默认，层级为口径参数）。
- **口径②（tooltip 净流入复合变体，已实现）**：高成长改净流入三年窗口——可算但小基数敏感（见 2.4）。
- **口径③（mock 式）**：外推弃用——ui_demo_fallback 对照。
- **裁定**：①结构+数据均足判完全转换支持；②登记为口径变体非判档依据。

### 2.2 探针读数实测

```sql
-- 聚集：geo 面 COUNTRY 级 2024 存量 Top3
SELECT l.name, g.talent_count FROM ads_geo_yearly_metrics g JOIN ads_location l
  ON g.location_id=l.location_id WHERE g.location_level='COUNTRY' AND g.statistics_year=2024
  ORDER BY g.talent_count DESC LIMIT 3;
-- 迁徙：flow 面 LOCATION 维 2024 to 端入流量 Top3
SELECT l.name, SUM(f.talent_count) s FROM ads_talent_mobility_yearly_flow f
  JOIN ads_location l ON f.to_entity_id=l.location_id
  WHERE f.flow_dimension='LOCATION' AND f.statistics_year=2024
  GROUP BY f.to_entity_id, l.name ORDER BY s DESC LIMIT 3;
-- 高成长：geo 面 2023→2024 同比 Top3（>1000 人门槛）
SELECT l.name, ROUND((b.talent_count-a.talent_count)/a.talent_count*100,1) g
  FROM ads_geo_yearly_metrics a JOIN ads_geo_yearly_metrics b
  ON a.location_id=b.location_id AND b.statistics_year=a.statistics_year+1
  JOIN ads_location l ON a.location_id=l.location_id
  WHERE a.location_level='COUNTRY' AND a.statistics_year=2023 AND a.talent_count>1000
  ORDER BY g DESC LIMIT 3;
```

实读（2024）：聚集 Top3 = China 69,523 / United States 18,891 / United Kingdom 5,265 人；迁徙 Top3 = China 127 / United States 64 / Hong Kong 39 人；高成长 Top3 = South Korea +26.1% / Hong Kong +20.1% / Taiwan +18.0%（门槛 2023 年 talent_count>1000）。变体口径②（tooltip）Top3 见 `derived[3]`（Hong Kong 三年和 18→40 = +122.2%，小基数敏感）。

### 2.3 读数落盘与同基核对

三标签 Top3 落 `derived[0-2]`（facts.hotspots_2024 汇总）；高成长为同表自关联相除（B3 同基注记，share_basis 字段落盘）；聚集/迁徙分列落不同表（geo 面 vs flow 面）但同年份同层级口径对齐（COUNTRY 级 2024），跨表读数在 facts 内注明各自来源。mock 26 城外推值仅作 ui_demo_fallback 披露，不混入真读数。

### 2.4 稳健性与口径敏感性

①门槛敏感性：高成长 >1000 人门槛防微基数——若取消门槛，小国（千人以下）增速噪声将进入 Top3（变体口径②的 +133.3%（三年和 −6→+2）即为该噪声实证）；②层级敏感性：COUNTRY 级最稳（5,081 行），CITY 级 132,975 行可切但迁徙标签需 to_entity_id 关联 CITY 字典覆盖待验证（降档触发器）；③窗口敏感性：同比（2023→2024）vs 三年复合（tooltip 口径）结果不同（口径① South Korea 领衔 vs 口径② 噪声国领衔）——正式口径建议口径①+门槛；④2026 为不完整年截断。

### 2.5 基期年份可用性

`base_years_used`=[2023, 2024]（同比自关联两年；迁徙/聚集为 2024 时点读数）；`missing`=[]；全序列 2000-2025 可复算任意年（基期随 year 选择器联动）；2026 不完整截断。note 详附录 B。

### 2.6 需求符合性预评

三标签区可直切真数（口径① Top3 名单+数值现成）；层级默认 COUNTRY 与 mock 城市级不一致需 UI 对齐（或切 CITY 级）；tooltip `:1282` 口径描述建议同步修正（现描述=口径②，实际交付=口径①）；「跨区和跨领域流动趋势」（507 需规）由 event 面三跨域标志承载（P10_022 已采序列），本区块为主呈现位。

### 2.7 复现代码结果展示

复现入口 `python3 code/M_SCIUI_P10_023.py`（薄壳直连久新实算：聚集/迁徙/高成长三查询+变体口径②聚合+Top3 断言）；产物 `code/M_SCIUI_P10_023_out.json`；关键读数：`derived[0-2]` 三标签 Top3、`derived[3]` 变体口径、`facts.hotspots_2024` 汇总。

### 2.8 分步证据对照表

| 步 | MD 论断 | 产物键 |
|---|---|---|
| 1 | 三面行数 171,736/51,489/298,384 | facts.jiuxin_*_table |
| 2 | 聚集 Top3 China 69,523/US 18,891/UK 5,265 | derived[0] |
| 3 | 迁徙 Top3 China 127/US 64/HK 39 | derived[1] |
| 4 | 高成长 Top3 KR +26.1/HK +20.1/TW +18.0 | derived[2] |
| 5 | 变体口径② HK +122.2% 小基数敏感 | derived[3] |
| 6 | 层级分布 5,081/33,518/132,975 | facts.geo_level_rows |
| 7 | dev/gkx 热点面缺失 | absence_probe[0]/[1] |
| 8 | 判档 完全转换支持 | support_judgment |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 聚集存量列 | jiuxin `ads_geo_yearly_metrics` | **有**（talent_count，COUNTRY/PROVINCE/CITY 三级） |
| 迁徙对流量 | jiuxin `ads_talent_mobility_yearly_flow` | **有**（LOCATION 维 28,672 行 to 端可聚合） |
| 高成长增速 | geo 面自关联 | **有**（同表同比，无现成 growth 列——转换点） |
| 区域字典 | jiuxin `ads_location` | **有**（22,229 行） |
| 跨域趋势（507 语义） | jiuxin `ads_talent_mobility_event` | **有**（三跨域标志，P10_022 采证） |
| 热点现成结果面 | 三源 | **无**（三列排序/聚合一步转换——判转换支持的依据） |
| dev 热点面 | dev | **无**（scholar 名录+链热点（行业链语义），非人才流动热点） |
| gkx 履历面 | gkx `dwd_scholar_work_experience` | **备选**（57,117 行需自建聚合） |

### 3.2 现场复核清单

UI 链实读：`SpaceTimeEvolutionNewPage.jsx:1259-1282` SectionCard id=ste-b-talent 三标签行（:1268/:1272/:1276 Tag 色红/橙红/绿）+ `:1282` tooltip 口径描述；`:534` useMemo 绑定；`mockData.js:481-502` getTalentHotspots 构建式（byScale/byGrowth 排序+migrateTargets 去重）。久新实连复核（本件脚本）：三查询 Top3 实算+断言通过（China 69,523/China 127/South Korea 26.1）；变体口径②聚合复核（Hong Kong 18→40=+122.2%）；geo 面 location_level 分布 COUNTRY 5,081/PROVINCE 33,518/CITY 132,975/CONTINENT 162；ads_location 22,229 行。共享探针快照 `_snapshots/_shared_s308_laneb_probe_out.json` 三源表数 542/280/218 与本次实算交叉一致。

## 四、数据缺失情况

### 4.1 缺口清单

①热点三标签物化视图未建（现算排序，判「转换」不判「直接」）；②CITY 级迁徙标签需 to_entity_id→CITY 字典关联覆盖验证（降档触发器）；③专业主题维（507 需规「各专业主题下」）DISCIPLINE 粒度到领域非 UI 六主题，映射未做；④mock 城市级与库 COUNTRY 级默认不一致（层级参数需 UI 对齐）。

### 4.2 修复建议与影响面

短期：三标签切口径①真数（Top3 名单+数值现成）+tooltip 口径描述修正。中期：久新建热点物化视图（年份×层级×标签）→ 完全直接支持（联动 P10_022/025 三件联升）。远期：CITY 级迁徙关联验证+DISCIPLINE→UI 六主题映射。同族联动：P10_022（总量卡）/P10_025（主体路径）共用三面，一次物化三件升档。

### 4.3 影响面

三标签区为 507 功能叶主呈现位，本件与 P10_022 同批可切真；层级对齐后数据链完整；P10_025 主体路径为同页剩余缺口。

## 参考文献

1. OECD. Handbook on Measuring the Mobility of Scientists. https://www.oecd.org/sti/sci-tech/
2. European Commission. Horizon Europe Mobility Flows Monitoring. https://erc.europa.eu/
3. 中国科学技术发展战略研究院. 中国科技人才流入监测报告. https://www.most.gov.cn/kjbgz/

# 附件

## 附录 A 原始需求原文摘录

- SRS《科技时空演进展示.md》序号 507（excel_row 510）：「支持主动跟踪各专业主题下的科技人员流动，智能识别跨区和跨领域流动趋势，展示人才聚集、迁徙热点及高成长区。用户可导出流动趋势报告，辅助团队建设和全球人才战略引导。」——「展示人才聚集、迁徙热点及高成长区」与本区块三标签一一对应。
- 检索记录：`rg 科技人员流动动态可视化` 三份说明书 → 区块名 0 命中（507 族功能覆盖；挂点 :1261 实查定位）。
- 实查定位链：`rg 聚集热点|迁徙热点|高成长区` achievement-preview 页族 → `SpaceTimeEvolutionNewPage.jsx:1268/1272/1276`（三 Tag 行）→ `mockData.js:481-502`（getTalentHotspots 构建式）；测试锚 `SpaceTimeEvolutionNewPage.test.jsx`（ste-b-talent 区块断言）。
- mock 参照（`mockData.js:481-502`）：26 城 byScale/byGrowth 排序+talent 型 FLOW_PATHS to 端去重 Top3。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_023_out.json`）

metric_id/batch=S3-08/ui_evidence（3 条组件行号）/requirement_trace（named_in_srs=false + SRS 锚 507 同名区块）/facts（ui_mount/ui_hotspot_builder/ui_mock_note/jiuxin_geo_table/jiuxin_flow_table/jiuxin_event_table/hotspots_2024/geo_level_rows/ads_location_rows/gkx_note/dev_table_total=542/gkx_table_count=280/jiuxin_table_count_live=218）/derived[0]（聚集 Top3）/derived[1]（迁徙 Top3）/derived[2]（高成长 Top3）/derived[3]（变体口径②）/absence_probe（三源三条）/support_judgment=完全转换支持/notes（5 条）/base_years 三键/ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：OECD 热点国排序（存量+净流量）→ Horizon Europe top destinations 榜（对流量 to 端）→ 中国科技人才集聚度指数（存量+增速复合）——geo/flow 两面即三方法的原料物化。数据矩阵：geo 171,736 行 talent_count 三级层级；flow 51,489 行 LOCATION 维；event 298,384 行跨域三标志；物化视图无（转换点）。分期方案：一期切口径①真数、二期物化视图（完全直接，三件联升）、三期 CITY 级+主题映射。风险登记：小基数增速噪声（+133.3% 实证）、层级口径不一致（mock 城市 vs 库 COUNTRY）、tooltip 口径描述与交付口径偏差。总判：完全转换支持（三标签全部一步转换可算；层级参数+CITY 关联验证为前置动作）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_023.py` | 退出码 0，落 `_out.json` |
| 实算复核 | derived[0] China 69,523 / derived[1] China 127 / derived[2] KR 26.1 | 重跑一致 |
| 判档一致 | MD 文首「完全转换支持」= out.json `support_judgment` | 一致 |
| 负证据 | dev/gkx 热点面缺失两条 | 逐一可复验 |
| mock 披露 | 26 城外推仅 §1.1/§2.3 语义描述 | 不参与支持度结论 |
