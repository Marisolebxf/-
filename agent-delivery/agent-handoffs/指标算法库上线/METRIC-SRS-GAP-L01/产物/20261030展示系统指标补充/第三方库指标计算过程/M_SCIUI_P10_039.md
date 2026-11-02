# M_SCIUI_P10_039 全球研究主体时空分布（Q0210）—— 指标信息 MD

> **类型**：无业务逻辑数值类｜ **域**：科技成果展示·科技时空演进展示New·全球研究主体地域时空分布（SpaceTimeEvolutionNewPage.jsx:845-852，清单序号 555 实查定位）
> **数据支持度**：**完全转换支持**｜ **UI 挂载**：科技信息展示系统 → 科技时空演进展示（New）→「全球研究主体时空分布地图」卡（`SpaceTimeEvolutionNewPage.jsx:845-852` + `mockData.js:33`）｜ **公式定义人**：无（指标名三源 0 命中；Q0210 为 UI 内部编号；时空分布=geo_yearly 聚合面现成语义）
> **复现脚本**：`code/M_SCIUI_P10_039.py`（薄壳，指向共享探针 `code/_shared_s308_laneC.py`）｜ **产物**：`code/M_SCIUI_P10_039_out.json`
> **口径归属**：UI 挂载件，SRS 无同名指标（上位叶 1.1.1.1.4.6.3 全球研究主体地域时空分布展示）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（三源无 Q0210 现成结果面）；直接数据=无；依赖结构=完全（久新 ads_geo_yearly_metrics 171,736 行 31 列含 institution_count×statistics_year×三层级）；依赖数据=完全（2000-2026 共 27 年无空年份，国家/省州/城市层级实算可落图）

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。** 久新 `ads_geo_yearly_metrics`（171,736 行，31 列）直接含 `institution_count`（研究主体数）/`paper_count`/`talent_count` 等强度列 × `statistics_year`（2000-2026 共 27 年无空年份）× `location_level`（CONTINENT/COUNTRY/PROVINCE/CITY 四档）——「时间轴播放 × 国家/省州/城市层级切换 × 分布密度落图」整链聚合转换即得；配套 `ads_institution_profile` 83,745 行（68,226 行带经纬度）可作机构点层放大，`ads_geo_yearly_institution_type_metrics` 349,396 行可作主体类型维切片。三源均无「Q0210」命名的现成结果面（需从年度×地域聚合面转换加工），判完全转换支持。

### 批次通用纪律摘要（S3-08 批共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 演化读数同表同年同层聚合（share_basis 注记） |
| B4 | 负结论带探针 | dev/gkx 零承载留证（§3.2/附录 B） |
| B5 | 确定性 | Top12 按主体数降序（共享脚本 ORDER BY） |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 产物只由脚本产出 | 薄壳脚本重跑产出，手改禁令 |
| B8 | 回执不复收 | 硬证据可复验（共享快照可重跑） |
| B9 | 单位/日期陷阱 | statistics_year 数值型；2026 截断标注 |
| B10 | 口径裁定保守交付 | 库口径（论文域主体池）与 UI mock（四维画像）差异披露，降档触发器写死（§1.6） |
| B11 | 多本账互推 | 与共享快照 `_shared_s308_laneC_out.json` 零漂移 |
| F 系 | 历史写法错误 | 无域级兜底（F1）、mock 值披露不当数据（F2）、文献带 URL（F9） |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成时空分布结果面吗？ | 近似有 | geo_yearly_metrics 即年度×地域×层级聚合面（主体数/论文/人才列齐） |
| 需要口径转换吗？ | 需要 | 聚合面→Q0210 交互序列（时轴/层级/密度）需转换加工；强度列以 institution_count 为主 |
| 数据量充分吗？ | 充分 | 171,736 行 27 年无空年份；三层级齐备（CITY 8,475/PROVINCE 1,753/COUNTRY 216@2024） |

## 摘要

「全球研究主体时空分布（Q0210）」是科技时空演进展示（New）页首屏「全球研究主体时空分布地图」卡的口径信息位（`SpaceTimeEvolutionNewPage.jsx:845-852` MetricInfo + `:856-865` WorldEvolutionMap）：交互式时空地图，时间轴播放 2018→当年，密度热力层 + 热点红圈 + 密度中心迁徙红线，国家/省州/城市三档层级切换。数据侧判定：**完全转换支持**——久新 `ads_geo_yearly_metrics`（171,736 行）以 location_id×statistics_year×location_level 组织，`institution_count` 主体数列 2000-2026 共 27 年全序列，2024 年国家级 Top3 为美国 9,811 / 中国 4,369 / 法国 2,490；中国城市级 2024 Top3 为北京 798 / 上海 287 / 广州 183（深圳 108 居第 7）；主体类型维（education/company/facility 等 8 类）由 `ads_geo_yearly_institution_type_metrics`（349,396 行）切片；机构坐标面 `ads_institution_profile` 83,745 行（68,226 带经纬度）支撑点层放大。dev/gkx 零承载（542/280 表无时空序列面）。

- 需求判定：**UI 挂载件**（SRS 无同名；上位功能 1.1.1.1.4.6.3 交互式时空地图分布呈现/地域模型多层级切换覆盖）。
- 复现状态：薄壳已跑通；Top12/类型分布/双强演化落本件产物。
- 档位结论：**完全转换支持**（年度×地域×层级聚合面转换即活）。
- 关键事实：geo_yearly_metrics 171,736 行 / 27 年无空年——OpenAlex 语义主体池，2026 不完整年截断标注。
- 升档路径：久新建 Q0210 专题视图（时轴+层级预聚合）→ 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技成果展示/科技时空演进展示（New）/首屏三栏。本件挂载于中央地图卡（`:845-853` 卡头「全球研究主体时空分布地图」+ 年份/层级 Tag + 热点计数 + MockBadge + `:849-852` MetricInfo title=全球研究主体时空分布（Q0210），content 描述「自动定位分布密度与演化轨迹 + 2018→当年密度中心迁徙红线 + 热力层=分布密度」）；`:856-865` WorldEvolutionMap 接收 mapRegions（regions 强度）/mapFlows（协作通道）/densityTrack（迁徙线）/showHeat/focus。页面 KpiTile 行另有「研究主体总数」（`:670`，metricId=Q0201 另号位）。mock 数据源（`mockData.js:33-53`）以 20 个全球核心城市画像（base 2018 基准 × growth 年增 × 正弦波动）确定性生成论文/专利/资金/人才四维度序列，支撑时间轴播放。

### 1.2 为什么需要本指标

时空分布回答「全球研究力量在哪、往哪迁」：决策者拖时间轴看主体密度演化（美中双强格局变化），切层级看省/州与城市集群，用迁徙线把握创新集群迁移趋势（SRS :27「帮助决策者了解区域科技力量变化，把握全球创新集群迁移趋势」）。它是科技时空演进展示页的骨架功能——全页四个 tab（时空分布/专业主题/流动协同/分析报告）都以它为底图。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「全球研究主体时空分布（Q0210）」指标名与 Q0210 编号在三份需求说明书中未出现；SRS 科技时空演进展示章给出的是交互行为（时间轴选择/层级切换/密度定位/回放），没有分布的口径定义（主体判定、强度算法、层级边界）。

### 1.4 类似指标权威方法可行性分析概要

全球研究主体时空分布的权威基准是 **OpenAlex Institutions 数据集**（R1，机构实体 + 国家/省/市地理归属 + 逐年论文计数，本库 geo 族的直接上游）与 **Nature Index 全球科研城市榜单**（R2，城市级论文份额聚合）及 **WIPO 全球创新指数（GII）科技集群排名**（R3，PCT 专利+科学出版物密度聚类）。方法族对照：

| 方法族 | 强度轴 | 地理层级 | 数据要求 | 与本库匹配 |
|---|---|---|---|---|
| OpenAlex 机构地理（库同构） | 机构数/论文数 | 国/省/市 | 机构画像+年度地域序列 | **有（geo_yearly 族即此语义）** |
| Nature Index 城市榜单 | 论文份额（fractional） | 城市 | 期刊加权论文 | 有（paper_fractional_count 列现成） |
| GII 科技集群 | 专利+论文密度聚类 | 城市群 | PCT+SCI 双源 | 部分（专利维度需另表） |

结论：库表面与 OpenAlex 方法族完全同构（机构数/论文数/分权论文列齐备），转换工程量集中在「聚合面→交互序列」而非口径重建。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:845-852`（MetricInfo Q0210）；`:856-865`（WorldEvolutionMap）；`:660`（页副标题引用需规 §1.1.1.1.4.6.3）；`:670`（Q0201 KpiTile）。
- mock：`space-time-evolution-new/mockData.js:33-53`（CITY_PROFILES 20 城/LEVELS 三档/YEARS 2018-2026，演示值，不参与支持度结论）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技成果展示/科技时空演进展示.md:17-27`（交互式时空地图分布呈现）/`:34-39`（地域模型多层级切换）。
- 外部：OpenAlex（R1）、Nature Index（R2）、WIPO GII（R3）。

### 1.6 推测原意与推测定义

**推测定义（本件可实算）**：

- 主强度：$S(l, y) = \text{institution\_count}(l, y)$——地域 $l$（国/省/市层级）在年 $y$ 的活跃研究主体数；密度落图按 $S$ 归一化着色；
- 演化轨迹：密度中心 $\arg\max_l S(l, y)$ 随 $y$ 的迁徙序列（UI 红线）；
- 类型切片：$S(l, y, t) = \text{institution\_count}$ 按 `institution_type` 8 类下钻（geo_yearly_institution_type_metrics）。

**降档触发器**：若 UI 强约束「资金维度」强度轴（mock funding 语义）且 project_count 近似不被接受 → 该维度降部分支持（geo_yearly 无资金专列）。**升档触发器**：久新建 Q0210 预聚合视图（时轴+层级+类型立方体）→ 完全直接支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技成果展示/科技时空演进展示.md` |
| 所属四级功能 | 1.1.1.1.4.6 科技成果展示（域） |
| 所属页面 | 1.1.1.1.4.6.3 科技时空演进展示（New 页） |
| 所属面板 | 首屏全球研究主体时空分布地图卡 |
| 本件叶 | 全球研究主体时空分布（Q0210）（UI 挂载件，SRS 无同名叶；上位叶=1.1.1.1.4.6.3.1 交互式时空地图分布呈现/1.1.1.1.4.6.3.2 地域模型多层级切换） |
| 相邻叶 | 热点区域自动识别与预警（1.1.1.1.4.6.3.3）/空间聚集与优势区分析（1.1.1.1.4.6.3.4）/P10_001 专利交易与创新流动（同页流动族，路B 件） |
| UI 容器 | `SpaceTimeEvolutionNewPage` 首屏三栏 + WorldEvolutionMap |

## 二、计算过程

### 2.1 口径裁定（B10 多口径并列）

- **口径①（机构数强度，已实现）**：$S(l,y)=\text{institution\_count}$，geo_yearly_metrics 主列直出，2024 国家级 Top12 + 中国城市级 Top12 + 类型分布实算（§2.2-2.3）。
- **口径②（论文份额强度，未实现登记）**：$S(l,y)=\text{paper\_fractional\_count}$（Nature Index 语义），列现成（31 列含该列），本件未跑——升档路径登记。
- **裁定**：口径①结构与数据均足（27 年×三层级），判完全转换支持；口径②登记为等价变体非本件判档依据。

### 2.2 探针读数（聚合面装载与规模校验）

```sql
SELECT statistics_year, COUNT(*) FROM ads_geo_yearly_metrics GROUP BY statistics_year ORDER BY 1;
-- 年度地域行数：2000:3,812 → 2015:8,456（加厚台阶）→ 2024:10,450 → 2025:11,156 → 2026:6,775
```

全表 171,736 行（产物 `jiuxin_geo_yearly_metrics_rows`，与共享快照零漂移），2000-2026 共 27 个年份无空年（`jiuxin_geo_yearly_year_count=27`）。2024 年层级分布：CITY 8,475 / PROVINCE 1,753 / COUNTRY 216 / CONTINENT 6——三档交互层级全承载。机构坐标面 `ads_institution_profile` 83,745 行、经纬度覆盖 68,226 行（81.4%）；地域维表 `ads_location` 22,229 行（CITY 19,729/PROVINCE 2,252/COUNTRY 232/CONTINENT 7/DISTRICT 9）。

### 2.3 同基核对（国家级与中国城市级读数）

2024 年国家级主体数 Top12（产物 `derived[0]`）：United States 9,811 / China 4,369 / France 2,490 / United Kingdom 2,464 / Germany 2,107 / India 1,863 / Japan 1,704 / Canada 1,159 / Italy 1,013 / Spain 981 / Russia 809 / Australia 802——同表同年同层聚合（B3 同基）。中国城市级 Top12（`derived[1]`）：北京市 798 / 上海 287 / 广州市 183 / 南京市 139 / 杭州市 134 / 武汉市 133 / **深圳 108** / 天津市 103 / 成都市 98 / 西安市 96……主体类型维（`derived[2]`，国家级 2024）：教育机构 12,118 / 医疗机构 8,084 / 企业 7,317 / 科研设施 7,135 / 非营利机构 3,481 / 政府机构 2,909 / 其他机构 1,836 / 档案与文化机构 558。

### 2.4 稳健性与口径敏感性

双强演化读数（`derived[3]`）：US 7,792（2018）→ 9,811（2024）→ 11,423（2025）；China 4,038（2018）→ 4,369（2024）——美国主体池绝对量领先、中国论文量领先（2024 China 373,017 篇 vs US 112,003 篇），强度轴选择（机构数 vs 论文数）会改变排序叙事，两列并列披露。`name_zh` 在英文官方名国家多为 NULL（美国/法国等 10/12 国），落图需 fallback `name_en`——中文名标注工程量小非缺口。2026 年 6,775 地域行（61% of 2025）不完整，时序使用截断标注。

### 2.5 基期年份可用性

`base_years_used`=2000-2026 全序列（27 年）、`missing=[]`（无空年）、基期建议 2015（序列加厚段起点：年度地域行 3,009→8,456 台阶，与 OpenAlex 收录加厚一致）或 2000（全序列首年）；2026 截断标注——note 详附录 B。

### 2.6 需求符合性预评

SRS「时间轴任意时间段选择」——27 年序列充分（超 mock 的 2018-2026 九时点）；「国家、省/州、市层级一键切换」——三层级数据齐备；「自动定位分布密度与演化轨迹」——密度=主体数归一化、轨迹=密度中心迁徙线，转换可算；「动态筛选与回放」——年份+层级+类型三维筛选立方体可预聚合。唯一口径差：UI mock 四维强度（论文/专利/资金/人才）中资金维度无专列（project_count 近似），降档触发器 §1.6 已写死。

### 2.7 复现代码结果展示

复现入口 `code/M_SCIUI_P10_039.py`（薄壳：快照断言 171,736 行/27 年/Top3 校验 + 判档落盘），共享探针真源 `code/_shared_s308_laneC.py`；运行 `python3 code/M_SCIUI_P10_039.py`。产物 `code/M_SCIUI_P10_039_out.json` 键名见附录 B 逐键清单；关键读数：`derived[0]` 国家级 Top12、`derived[1]` 中国城市 Top12、`derived[2]` 类型分布、`derived[3]` US/China 双强演化。

### 2.8 分步证据对照表

| 步 | MD 论断 | 产物键 |
|---|---|---|
| 1 | 全表 171,736 行 | facts.jiuxin_geo_yearly_metrics_rows |
| 2 | 2000-2026 共 27 年无空年 | facts.jiuxin_geo_yearly_year_count / year_counts |
| 3 | 2024 国家级 Top3 9,811/4,369/2,490 | derived[0] |
| 4 | 中国城市 2024 深圳第 7（108） | derived[1] |
| 5 | 类型分布 8 类（教育 12,118 首） | derived[2] |
| 6 | US/China 双强演化 7,792→9,811→11,423 | derived[3] |
| 7 | 坐标面 83,745/68,226 | facts.jiuxin_profile_* |
| 8 | 判档 完全转换支持 | support_judgment |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 年度×地域×层级主体序列 | jiuxin `ads_geo_yearly_metrics` | **有**（171,736 行，2000-2026） |
| 主体类型维 | jiuxin `ads_geo_yearly_institution_type_metrics` + `ads_institution_type` 字典 | **有**（349,396 行 / 8 类） |
| 机构级坐标（点层放大） | jiuxin `ads_institution_profile.latitude/longitude` | **有**（83,745 行 / 68,226 带坐标） |
| 地域维（层级/中英名） | jiuxin `ads_location` | **有**（22,229 行） |
| dev 时空序列面 | gkxlumenx_* | **无**（geo 词族仅静态维表） |
| gkx 时空序列面 | — | **0 命中**（280 表） |

### 3.2 现场复核清单

UI 链实读：`SpaceTimeEvolutionNewPage.jsx:845-852` 卡头与 MetricInfo（Q0210 content 全文）；`:856-865` WorldEvolutionMap 五参数；`:660` 页副标题自引需规 §1.1.1.1.4.6.3；mock 源 `mockData.js:33-53`（20 城 profile/LEVELS/YEARS）。久新实连复核（共享探针）：geo_yearly_metrics 年度分布 27 键；2024 层级分布 CITY 8,475/PROVINCE 1,753/COUNTRY 216/CONTINENT 6；Top12 断言（US 9,811 首位、China 4,369 次位）通过；profile COUNT=83,745 断言通过。dev/gkx 词族扫描 0 时空序列命中（absence_probe 两条留证）。

## 四、数据缺失情况

### 4.1 缺口清单

①资金维度强度列缺（mock funding 语义；project_count/project_fractional_count 可近似需口径裁定）；②Q0210 命名的预聚合视图未建（展示系统直查需转换层）；③`name_zh` 英文名国家 NULL（落图需 name_en fallback）；④2026 年不完整（6,775 地域行，61% of 2025，收录滞后）；⑤dev 库无镜像（若展示系统要求 dev 直连需 ETL 回灌，171,736 行量级可行）。

### 4.2 修复建议与影响面

短期：久新建 Q0210 预聚合视图（statistics_year×location_level×institution_type 立方体）→ 本件完全直接支持；name_zh 回补字典。中期：dev 回灌 geo_yearly 聚合面 → 展示系统 dev 直查；资金维度裁定（project_count 近似或接入资助库）。远期：迁徙线/热点预警专用面（density track 预计算）→ UI 全交互零延迟。同页流动族（P10_001 专利交易与创新流动，路B 件）可复用 ads_geo_yearly 专利列。

### 4.3 影响面

科技时空演进页首屏地图卡可切真实数（27 年×三层级×8 类主体）；mock 20 城演示值退役；「研究主体总数」KpiTile（Q0201 另号位）同步可算（2024 全球国家级合计口径）。

## 参考文献

1. OpenAlex. Institutions dataset — 机构实体与地理归属、逐年计数 [EB/OL]. https://openalex.org （R1，2026-11-02 可达；本库 geo 族直接上游语义）
2. Springer Nature. Nature Index 全球科研城市/机构榜单（论文份额口径）[EB/OL]. https://www.natureindex.com （R2，2026-11-02 可达）
3. WIPO. Global Innovation Index — Science and Technology Cluster ranking [EB/OL]. https://www.wipo.int/gii （R3，2026-11-02 可达；PCT+SCI 密度聚类口径）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技成果展示/科技时空演进展示.md》1.1.1.1.4.6.3.1 交互式时空地图分布呈现：

> 用户可通过时间轴和地图交互选择任意时间段，支持自动定位全球各区域研究主体的分布密度与演化轨迹。高亮显示科研活跃区，支持动态筛选与回放功能，帮助决策者了解区域科技力量变化，把握全球创新集群迁移趋势。

1.1.1.1.4.6.3.2 地域模型多层级切换：

> 用户可一键切换显示国家、省/州、市等不同空间层级，支持同步更新分布及流动数据。支持实时统计各层级科研主体数量和变化趋势，助力政府和科研机构进行分区资源对比、精准制定国际合作策略。

「全球研究主体时空分布（Q0210）」指标名与 Q0210 编号在三份说明书未出现（检索记录：`rg 全球研究主体时空分布|Q0210` 三份说明书 + 主需求 → 指标名 0 命中；Q0210 仅见 UI MetricInfo/mock metricId）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_039_out.json`）

facts（ui_mount/ui_kpi/ui_mock/jiuxin_table/jiuxin_geo_yearly_metrics_rows=171736/jiuxin_geo_yearly_year_span=2000-2026/jiuxin_geo_yearly_year_count=27/year_counts 27 键/jiuxin_geo_levels/jiuxin_profile_rows=83745/jiuxin_profile_rows_with_coords=68226/jiuxin_type_dict_table/named_in_srs=false/named_note）；derived[0]（国家级 Top12_2024）/derived[1]（中国城市 Top12_2024，深圳 108 第 7）/derived[2]（类型分布 8 类）/derived[3]（US/China 双强演化）；absence_probe（dev 0/gkx 0/jiuxin 正结论 4 表）；support_judgment=完全转换支持；base_years 三键（used=2000-2026 全 27 年 / missing=[] / note 含 2015 加厚建议+2026 截断）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：OpenAlex 机构地理（库同构，机构数/论文/分权论文列齐）→ Nature Index 城市份额（fractional 列现成）→ GII 科技集群（专利维度需另表）。数据矩阵：久新主面 171,736 行 27 年三层级；类型面 349,396 行；坐标面 83,745/68,226；dev/gkx 零镜像。分期方案：一期 Q0210 预聚合视图（完全直接支持）、二期 dev 回灌 + name_zh 字典、三期迁徙线/热点专用面。风险登记：强度轴选择改变排序叙事（机构数 vs 论文数并列披露）、2026 收录滞后、资金维度口径未定。总判：完全转换支持（聚合即活，降档触发器=资金维度强约束）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_039.py` | 退出码 0，落 `_out.json` |
| 共享探针 | `python3 code/_shared_s308_laneC.py` | 快照键与本件 facts 零漂移 |
| 判档一致 | MD 文首「完全转换支持」= out.json | 一致 |
| 断言 | rows=171736 / years=27 / US 9,811 首位 | 脚本内 assert 通过 |
| mock 披露 | mock 20 城/四维仅 §1.1 语义描述 | 不参与支持度结论 |
